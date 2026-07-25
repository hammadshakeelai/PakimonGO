import os
import sys
import traceback
from pathlib import Path

from sqlalchemy.orm import Session

from src.infrastructure.database.repositories import create_notification
from src.infrastructure.database.repositories import create_score_event
from src.infrastructure.database.repositories import get_media_asset
from src.infrastructure.database.repositories import get_submissions_pending_scoring
from src.infrastructure.database.repositories import update_submission_status
from src.infrastructure.database.session import get_session_local
from src.infrastructure.queue.queue import Job, InMemoryJobQueue

MAX_JOB_ATTEMPTS = 3

_score_pkg = Path(__file__).resolve().parents[5] / "packages" / "scoring-rules" / "src"
sys.path.insert(0, str(_score_pkg))

from scoring_service import AIScoringService  # noqa: E402
from vision_provider import DummyVisionProvider  # noqa: E402

_VISION_IMPL = DummyVisionProvider()
_vision_env = os.environ.get("VISION_PROVIDER", "dummy").lower()
if _vision_env in ("google", "gcp"):
    try:
        from google_vision_provider import GoogleVisionProvider
        _VISION_IMPL = GoogleVisionProvider()
    except (ImportError, ValueError):
        pass
elif _vision_env == "groq":
    try:
        from groq_vision_provider import GroqVisionProvider
        _VISION_IMPL = GroqVisionProvider()
    except (ImportError, ValueError):
        pass


def process_score_job(job: Job, scoring_service: AIScoringService | None = None) -> None:
    svc = scoring_service or AIScoringService(vision_provider=_VISION_IMPL)
    submission_id = job.payload.get("submission_id", "")
    media_asset_id = job.payload.get("media_asset_id", "")
    animal_context = job.payload.get("animal_context", "unknown")
    explanation_category = job.payload.get("explanation_category", "normal")
    user_id = job.payload.get("user_id")

    db: Session = get_session_local()()
    try:
        upload_base = os.environ.get("UPLOAD_BASE", "data/uploads")
        asset = get_media_asset(db, media_asset_id) if media_asset_id else None
        media_path = None
        if asset and asset.storage_key:
            candidate = Path(upload_base) / asset.storage_key
            if candidate.exists():
                media_path = str(candidate)

        scoring_result = svc.evaluate(
            animal_context,
            explanation_category,
            media_path=media_path,
        )

        new_state = "scored" if explanation_category == "normal" else "capped"
        update_submission_status(db, submission_id, new_state)

        create_score_event(
            db=db,
            submission_id=submission_id,
            user_id=user_id,
            ledger=scoring_result.ledger,
            points=scoring_result.points,
            event_type=new_state,
            formula_version=scoring_result.formula_version,
            explanation_category=scoring_result.explanation_category,
            previous_state="ai_evaluated",
            new_state=new_state,
        )
        if user_id:
            points = scoring_result.points
            if points is not None:
                n_title = f"Submission scored: {points} pts"
                n_body = f"Your submission received {points} points ({scoring_result.explanation_category})."
            else:
                n_title = "Submission reviewed"
                n_body = f"Your submission has been reviewed ({scoring_result.explanation_category})."
            create_notification(
                db=db,
                user_id=user_id,
                notification_type="submission_scored",
                title=n_title,
                body=n_body,
                reference_type="submission",
                reference_id=submission_id,
            )
            # This capture may have pushed a group quest over the line —
            # celebrate with the whole squad (never blocks scoring).
            try:
                from src.infrastructure.database.repositories.quest import (
                    notify_completed_quests,
                )

                notify_completed_quests(db, user_id)
            except Exception:  # noqa: BLE001
                pass
    finally:
        db.close()


def process_pending_jobs(queue: InMemoryJobQueue, scoring_service: AIScoringService | None = None) -> int:
    """Drain whatever is queued right now (not jobs added mid-drain by a
    retry below - those wait for the next poll tick, so a persistently
    failing job can't spin this loop instead of backing off)."""
    count = 0
    for _ in range(queue.pending_count):
        job = queue.dequeue()
        if job is None:
            break
        try:
            process_score_job(job, scoring_service)
        except Exception:  # noqa: BLE001
            # A single bad job (transient vision-provider error, etc.) must
            # never take down the worker loop - every future submission
            # would silently stop scoring forever, with no queue drained.
            traceback.print_exc()
            _handle_job_failure(queue, job)
        count += 1
    return count


def _handle_job_failure(queue: InMemoryJobQueue, job: Job) -> None:
    attempt = job.payload.get("retry_count", 0) + 1
    if attempt < MAX_JOB_ATTEMPTS:
        # retry_count travels in the payload, not on the Job itself -
        # enqueue() always mints a fresh Job with a fresh id/retry_count,
        # so carrying it any other way would silently reset it to 0 forever.
        queue.enqueue(job.job_type, {**job.payload, "retry_count": attempt})
        return
    _mark_submission_for_review(job)


def _mark_submission_for_review(job: Job) -> None:
    """Exhausted retries: park the submission in the existing REVIEW state
    (a valid transition from ai_evaluated - no new terminal state needed)
    instead of leaving it silently stuck at ai_evaluated forever."""
    submission_id = job.payload.get("submission_id", "")
    user_id = job.payload.get("user_id")
    if not submission_id:
        return
    try:
        db: Session = get_session_local()()
        try:
            update_submission_status(db, submission_id, "review")
            create_score_event(
                db=db,
                submission_id=submission_id,
                user_id=user_id,
                ledger="scoring_failed",
                points=None,
                event_type="review",
                previous_state="ai_evaluated",
                new_state="review",
            )
            if user_id:
                create_notification(
                    db=db,
                    user_id=user_id,
                    notification_type="submission_scored",
                    title="Submission needs another look",
                    body="We couldn't automatically score this one - it's "
                         "been queued for review.",
                    reference_type="submission",
                    reference_id=submission_id,
                )
        finally:
            db.close()
    except Exception:  # noqa: BLE001
        # Best-effort: even this must never re-crash the worker loop.
        traceback.print_exc()


def recover_orphaned_jobs(queue: InMemoryJobQueue) -> int:
    """Re-enqueue submissions left at ai_evaluated by a server restart that
    lost the previous process's in-memory queue. Call once at process
    startup, before the poll loop begins."""
    db: Session = get_session_local()()
    try:
        rows = get_submissions_pending_scoring(db)
        for sub, attr in rows:
            queue.enqueue("score_submission", {
                "submission_id": sub.id,
                "media_asset_id": sub.primary_media_asset_id,
                "animal_context": attr.animal_context if attr else "unknown",
                "explanation_category": "normal",
                "user_id": sub.user_id,
                "retry_count": 0,
            })
        return len(rows)
    finally:
        db.close()
