from __future__ import annotations

import sys
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import create_notification
from src.infrastructure.database.repositories import create_score_event
from src.infrastructure.database.repositories import create_submission as db_create_submission
from src.infrastructure.database.repositories import get_all_submission_sha256s
from src.infrastructure.database.repositories import get_latest_score_event
from src.infrastructure.database.repositories import get_media_asset
from src.infrastructure.database.repositories import get_submission as db_get_submission
from src.infrastructure.database.repositories import get_submissions
from src.infrastructure.database.repositories import is_sensitive_species
from src.infrastructure.database.repositories import update_submission_status
from src.infrastructure.database.session import get_db
from src.infrastructure.queue.queue import get_queue

_score_pkg = Path(__file__).resolve().parents[6] / "packages" / "scoring-rules" / "src"
sys.path.insert(0, str(_score_pkg))

from precheck import run_precheck  # noqa: E402
from scoring_service import StubScoringService  # noqa: E402

router = APIRouter(prefix="/submissions", tags=["submissions"])
_scoring = StubScoringService()


def _build_submission_response(sub, attr, score_event=None, db: Session | None = None) -> dict:
    status = sub.status or "pending"
    animal_context = attr.animal_context if attr else "unknown"
    real_name = attr.real_name if attr else ""
    points = score_event.points if score_event else None
    explanation = score_event.explanation_category if score_event else "Scoring is pending."
    ledger = score_event.ledger if score_event else (animal_context if animal_context != "unknown" else None)

    # Check if species is sensitive
    is_sensitive = False
    if db and real_name:
        is_sensitive = is_sensitive_species(db, real_name)

    # Derive cell centroid from capture location (rounded to ~111m precision)
    loc = sub.capture_location
    cell_lat = round(loc.latitude, 3) if loc and loc.latitude is not None else None
    cell_lng = round(loc.longitude, 3) if loc and loc.longitude is not None else None

    # For sensitive species, suppress exact location in public APIs
    if is_sensitive:
        public_location = {
            "cellId": "cell_suppressed",
            "precisionLabel": "suppressed",
            "suppressedReason": "sensitive_species",
            "cellLatitude": cell_lat,
            "cellLongitude": cell_lng,
        }
    else:
        public_location = {
            "cellId": f"cell_{uuid.uuid4().hex[:8]}",
            "precisionLabel": "coarse",
            "cellLatitude": cell_lat,
            "cellLongitude": cell_lng,
        }

    return {
        "submissionId": sub.id,
        "mediaAssetId": sub.primary_media_asset_id,
        "realName": real_name,
        "animalContext": animal_context,
        "scoreState": {
            "status": status,
            "visiblePoints": points,
            "explanationSummary": explanation,
            "ledger": ledger,
        },
        "visibility": "private",
        "publicLocation": public_location,
    }


def _notify_scored(db, user_id, submission_id, points, explanation):
    if points is not None:
        title = f"Submission scored: {points} pts"
        body = f"Your submission received {points} points ({explanation})."
    else:
        title = "Submission reviewed"
        body = f"Your submission has been reviewed ({explanation})."
    create_notification(
        db=db,
        user_id=user_id,
        notification_type="submission_scored",
        title=title,
        body=body,
        reference_type="submission",
        reference_id=submission_id,
    )


@router.post("")
def create_submission_endpoint(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Create a new submission (capture record).

    Runs precheck (duplicate detection + context rules).
    Wild submissions are enqueued for async AI scoring; capped
    contexts (zoo/pet/duplicate) are scored synchronously.
    """
    media_asset_id = body.get("mediaAssetId")
    animal_context = body.get("animalContext", "unknown")
    real_name = body.get("realName", "")
    cute_name = body.get("cuteName", "")
    caption = body.get("caption", "")
    tags = body.get("tags", [])
    foreground_location = body.get("foregroundLocation")

    if not media_asset_id:
        raise HTTPException(status_code=400, detail="Missing mediaAssetId")

    latitude = None
    longitude = None
    accuracy_meters = None
    if foreground_location:
        latitude = foreground_location.get("latitude")
        longitude = foreground_location.get("longitude")
        accuracy_meters = foreground_location.get("accuracyMeters")

    sub, attr = db_create_submission(
        db=db,
        media_asset_id=media_asset_id,
        animal_context=animal_context,
        real_name=real_name,
        cute_name=cute_name,
        caption=caption,
        tags=tags,
        user_id=current_user.user_id,
        latitude=latitude,
        longitude=longitude,
        accuracy_meters=accuracy_meters,
    )

    asset = get_media_asset(db, media_asset_id)
    current_sha256 = asset.sha256 if asset else None
    existing_sha256s = get_all_submission_sha256s(db, exclude_media_asset_id=media_asset_id)

    precheck_result = run_precheck(animal_context, existing_sha256s, current_sha256)
    suggested = precheck_result.suggested_state
    update_submission_status(db, sub.id, suggested.value)

    if suggested.value == "ai_evaluated":
        _enqueue_score_job(sub.id, media_asset_id, animal_context,
                           precheck_result.explanation_category, current_user.user_id)
        return _build_submission_response(sub, attr, db=db)

    scoring_result = _scoring.evaluate(animal_context, precheck_result.explanation_category)
    new_state = "capped"
    update_submission_status(db, sub.id, new_state)
    score_event = create_score_event(
        db=db,
        submission_id=sub.id,
        user_id=current_user.user_id,
        ledger=scoring_result.ledger,
        points=scoring_result.points,
        event_type=new_state,
        formula_version=scoring_result.formula_version,
        explanation_category=scoring_result.explanation_category,
        previous_state=suggested.value,
        new_state=new_state,
    )
    _notify_scored(db, current_user.user_id, sub.id, scoring_result.points, scoring_result.explanation_category)
    return _build_submission_response(sub, attr, score_event, db)


def _enqueue_score_job(
    submission_id: str,
    media_asset_id: str,
    animal_context: str,
    explanation_category: str,
    user_id: str | None = None,
) -> None:
    queue = get_queue()
    queue.enqueue("score_submission", {
        "submission_id": submission_id,
        "media_asset_id": media_asset_id,
        "animal_context": animal_context,
        "explanation_category": explanation_category,
        "user_id": user_id,
    })


@router.get("/{submission_id}")
def get_submission_endpoint(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Get a single submission by ID with current score state.

    Returns score status, visible points, explanation, and
    public location (coarsened or suppressed for sensitive species).
    """
    result = db_get_submission(db, submission_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub, attr = result
    score_event = get_latest_score_event(db, submission_id)
    return _build_submission_response(sub, attr, score_event, db)


@router.get("")
def list_submissions_endpoint(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(
        default=None,
        enum=[
            "pending",
            "prechecked",
            "ai_evaluated",
            "scored",
            "capped",
            "review",
            "rejected",
            "rolled_back",
        ],
    ),
    sort_by: str = Query(default="createdAt", enum=["createdAt", "submittedAt", "status", "points", "species"]),
    sort_order: str = Query(default="desc", enum=["asc", "desc"]),
):
    """List submissions for the current user with pagination/filtering/sorting.

    Supports status filter, multiple sort options, and sensitive species
    suppression by default.
    """
    items, total = get_submissions(
        db=db,
        user_id=current_user.user_id,
        limit=limit,
        offset=offset,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        include_sensitive=False,
    )
    return {"submissions": items, "pagination": {"limit": limit, "offset": offset, "total": total}}
