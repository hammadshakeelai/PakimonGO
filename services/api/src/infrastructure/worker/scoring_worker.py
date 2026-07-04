import os
import sys
from pathlib import Path

from sqlalchemy.orm import Session

from src.infrastructure.database.repositories import create_notification
from src.infrastructure.database.repositories import create_score_event
from src.infrastructure.database.repositories import get_media_asset
from src.infrastructure.database.repositories import update_submission_status
from src.infrastructure.database.session import get_session_local
from src.infrastructure.queue.queue import Job, InMemoryJobQueue

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
    finally:
        db.close()


def process_pending_jobs(queue: InMemoryJobQueue, scoring_service: AIScoringService | None = None) -> int:
    count = 0
    while True:
        job = queue.dequeue()
        if job is None:
            break
        process_score_job(job, scoring_service)
        count += 1
    return count
