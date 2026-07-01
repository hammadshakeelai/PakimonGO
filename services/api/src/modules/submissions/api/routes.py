from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import create_score_event
from src.infrastructure.database.repositories import create_submission as db_create_submission
from src.infrastructure.database.repositories import get_all_submission_sha256s
from src.infrastructure.database.repositories import get_latest_score_event
from src.infrastructure.database.repositories import get_media_asset
from src.infrastructure.database.repositories import get_submission as db_get_submission
from src.infrastructure.database.repositories import update_submission_status
from src.infrastructure.database.session import get_db

_score_pkg = Path(__file__).resolve().parents[6] / "packages" / "scoring-rules" / "src"
sys.path.insert(0, str(_score_pkg))

from precheck import run_precheck  # noqa: E402
from scoring_service import AIScoringService  # noqa: E402
from vision_provider import DummyVisionProvider  # noqa: E402

_VISION_IMPL = DummyVisionProvider()
_vision_provider_env = os.environ.get("VISION_PROVIDER", "dummy").lower()
if _vision_provider_env in ("google", "gcp"):
    try:
        from google_vision_provider import GoogleVisionProvider  # noqa: E402
        _VISION_IMPL = GoogleVisionProvider()
    except (ImportError, ValueError):
        pass

router = APIRouter(prefix="/v1/submissions", tags=["submissions"])
_scoring = AIScoringService(vision_provider=_VISION_IMPL)


def _build_submission_response(sub, attr, score_event=None) -> dict:
    status = sub.status or "pending"
    animal_context = attr.animal_context if attr else "unknown"
    points = score_event.points if score_event else None
    explanation = score_event.explanation_category if score_event else "Scoring is pending."
    ledger = score_event.ledger if score_event else (animal_context if animal_context != "unknown" else None)

    return {
        "submissionId": sub.id,
        "mediaAssetId": sub.primary_media_asset_id,
        "scoreState": {
            "status": status,
            "visiblePoints": points,
            "explanationSummary": explanation,
            "ledger": ledger,
        },
        "visibility": "private",
        "publicLocation": {
            "cellId": f"cell_{uuid.uuid4().hex[:8]}",
            "precisionLabel": "coarse",
        },
    }


@router.post("")
def create_submission_endpoint(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
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

    upload_base = os.environ.get("UPLOAD_BASE", "data/uploads")
    media_path = None
    if asset and asset.storage_key:
        candidate = Path(upload_base) / asset.storage_key
        if candidate.exists():
            media_path = str(candidate)

    scoring_result = _scoring.evaluate(
        animal_context,
        precheck_result.explanation_category,
        media_path=media_path,
    )
    new_state = "scored" if suggested.value == "ai_evaluated" else "capped"
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

    return _build_submission_response(sub, attr, score_event)


@router.get("/{submission_id}")
def get_submission_endpoint(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    result = db_get_submission(db, submission_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub, attr = result
    score_event = get_latest_score_event(db, submission_id)
    return _build_submission_response(sub, attr, score_event)
