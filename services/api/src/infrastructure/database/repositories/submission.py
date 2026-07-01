import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import CaptureLocation, MediaAsset, Submission, SubmissionAttribute


def create_submission(
    db: Session,
    media_asset_id: str,
    animal_context: str,
    real_name: str,
    cute_name: str,
    caption: str,
    tags: list[str],
    user_id: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    accuracy_meters: float | None = None,
) -> tuple:
    submission_id = f"sub_{uuid.uuid4().hex[:20]}"

    sub = Submission(
        id=submission_id,
        user_id=user_id,
        primary_media_asset_id=media_asset_id,
        status="pending",
    )
    db.add(sub)

    attr = SubmissionAttribute(
        submission_id=submission_id,
        animal_context=animal_context,
        real_name=real_name,
        cute_name=cute_name,
        caption=caption,
        tags=",".join(tags) if tags else None,
    )
    db.add(attr)

    if latitude is not None and longitude is not None:
        loc = CaptureLocation(
            submission_id=submission_id,
            latitude=latitude,
            longitude=longitude,
            accuracy_meters=accuracy_meters,
        )
        db.add(loc)

    db.commit()
    db.refresh(sub)
    return sub, attr


def get_all_submission_sha256s(db: Session, exclude_media_asset_id: str | None = None) -> set[str]:
    query = (
        db.query(MediaAsset.sha256)
        .join(Submission, Submission.primary_media_asset_id == MediaAsset.id)
        .filter(MediaAsset.sha256.isnot(None))
    )
    if exclude_media_asset_id:
        query = query.filter(Submission.primary_media_asset_id != exclude_media_asset_id)
    return {r[0] for r in query.all() if r[0]}


def update_submission_status(db: Session, submission_id: str, status: str) -> None:
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if sub:
        sub.status = status
        sub.updated_at = datetime.now(timezone.utc)
        db.commit()


def get_submission(db: Session, submission_id: str) -> tuple | None:
    from ..models import Submission, SubmissionAttribute

    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if sub is None:
        return None
    attr = (
        db.query(SubmissionAttribute)
        .filter(SubmissionAttribute.submission_id == submission_id)
        .first()
    )
    return sub, attr
