import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import CaptureLocation, MediaAsset, MediaDerivative, ScoreEvent, Submission, SubmissionAttribute, User


def create_media_asset(
    db: Session,
    file_name: str,
    content_type: str,
    byte_size: int,
    sha256: str,
    owner_user_id: str | None = None,
) -> MediaAsset:
    media_asset_id = f"media_{uuid.uuid4().hex[:24]}"
    asset = MediaAsset(
        id=media_asset_id,
        owner_user_id=owner_user_id,
        file_name=file_name,
        content_type=content_type,
        byte_size=byte_size,
        sha256=sha256,
        storage_key=f"originals/{media_asset_id}",
        processing_state="pending",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_media_asset(db: Session, media_asset_id: str) -> MediaAsset | None:
    return db.query(MediaAsset).filter(MediaAsset.id == media_asset_id).first()


def update_media_asset_storage_key(db: Session, media_asset_id: str, storage_key: str) -> MediaAsset | None:
    asset = get_media_asset(db, media_asset_id)
    if asset is None:
        return None
    asset.storage_key = storage_key
    asset.processing_state = "uploaded"
    asset.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(asset)
    return asset


def complete_media_asset(db: Session, media_asset_id: str, sha256: str) -> MediaAsset | None:
    asset = get_media_asset(db, media_asset_id)
    if asset is None or asset.sha256 != sha256:
        return None
    asset.processing_state = "ready"
    asset.updated_at = datetime.now(timezone.utc)

    deriv = MediaDerivative(
        media_asset_id=media_asset_id,
        size_label="thumbnail",
        storage_key=f"thumbs/{media_asset_id}.webp",
        exif_stripped=True,
        visibility_state="public",
    )
    db.add(deriv)

    deriv_public = MediaDerivative(
        media_asset_id=media_asset_id,
        size_label="public",
        storage_key=f"public/{media_asset_id}.webp",
        exif_stripped=True,
        visibility_state="public",
    )
    db.add(deriv_public)

    db.commit()
    db.refresh(asset)
    return asset


def get_derivatives(db: Session, media_asset_id: str) -> list[MediaDerivative]:
    return (
        db.query(MediaDerivative)
        .filter(MediaDerivative.media_asset_id == media_asset_id)
        .all()
    )


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
    from .models import Submission, SubmissionAttribute

    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if sub is None:
        return None
    attr = (
        db.query(SubmissionAttribute)
        .filter(SubmissionAttribute.submission_id == submission_id)
        .first()
    )
    return sub, attr


def create_score_event(
    db: Session,
    submission_id: str,
    user_id: str | None,
    ledger: str,
    points: int | None,
    event_type: str,
    formula_version: str | None = None,
    explanation_category: str | None = None,
    previous_state: str | None = None,
    new_state: str | None = None,
    actor: str = "system",
) -> ScoreEvent:
    event = ScoreEvent(
        submission_id=submission_id,
        user_id=user_id,
        ledger=ledger,
        points=points,
        event_type=event_type,
        formula_version=formula_version,
        explanation_category=explanation_category,
        previous_state=previous_state,
        new_state=new_state or event_type,
        actor=actor,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_latest_score_event(db: Session, submission_id: str) -> ScoreEvent | None:
    return (
        db.query(ScoreEvent)
        .filter(ScoreEvent.submission_id == submission_id)
        .order_by(ScoreEvent.created_at.desc())
        .first()
    )


def get_or_create_user(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        user = User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def update_user(db: Session, user_id: str, age_band: str | None = None, home_region: str | None = None) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    if age_band is not None:
        user.age_band = age_band
    if home_region is not None:
        user.home_region = home_region
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


def get_user_collection(
    db: Session,
    user_id: str,
    limit: int = 100,
    offset: int = 0,
    context: str | None = None,
    sort_by: str = "totalPoints",
    sort_order: str = "desc",
) -> tuple[list[dict], int]:
    query = (
        db.query(
            SubmissionAttribute.real_name,
            SubmissionAttribute.animal_context,
            func.sum(ScoreEvent.points).label("total_points"),
            func.count(Submission.id).label("capture_count"),
            func.max(ScoreEvent.created_at).label("last_captured"),
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .filter(Submission.user_id == user_id)
        .filter(Submission.status.in_(["scored", "capped"]))
        .group_by(SubmissionAttribute.real_name, SubmissionAttribute.animal_context)
    )
    if context:
        query = query.filter(SubmissionAttribute.animal_context == context)

    # Total count before pagination
    total = query.count()

    # Sorting
    sort_column = {
        "totalPoints": func.sum(ScoreEvent.points),
        "species": SubmissionAttribute.real_name,
        "captureCount": func.count(Submission.id),
        "lastCaptured": func.max(ScoreEvent.created_at),
    }.get(sort_by, func.sum(ScoreEvent.points))

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    rows = query.limit(limit).offset(offset).all()

    items = [
        {
            "species": row.real_name,
            "context": row.animal_context,
            "totalPoints": row.total_points or 0,
            "captureCount": row.capture_count,
            "lastCaptured": row.last_captured.isoformat() if row.last_captured else None,
        }
        for row in rows
    ]
    return items, total


def get_leaderboard(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "totalScore",
    sort_order: str = "desc",
) -> tuple[list[dict], int]:
    query = (
        db.query(
            User.id.label("user_id"),
            User.age_band,
            User.home_region,
            func.sum(ScoreEvent.points).label("total_score"),
            func.count(ScoreEvent.id).label("submission_count"),
        )
        .select_from(ScoreEvent)
        .join(User, User.id == ScoreEvent.user_id)
        .filter(ScoreEvent.points.isnot(None))
        .group_by(User.id, User.age_band, User.home_region)
    )

    total = query.count()

    sort_column = {
        "totalScore": func.sum(ScoreEvent.points),
        "userId": User.id,
        "submissionCount": func.count(ScoreEvent.id),
    }.get(sort_by, func.sum(ScoreEvent.points))

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    rows = query.limit(limit).offset(offset).all()

    items = [
        {
            "userId": row.user_id,
            "ageBand": row.age_band,
            "homeRegion": row.home_region,
            "totalScore": row.total_score or 0,
            "submissionCount": row.submission_count,
        }
        for row in rows
    ]
    return items, total


def get_submissions(
    db: Session,
    user_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
    status: str | None = None,
    animal_context: str | None = None,
    sort_by: str = "createdAt",
    sort_order: str = "desc",
) -> tuple[list[dict], int]:
    from .models import Submission, SubmissionAttribute, ScoreEvent

    query = (
        db.query(
            Submission.id,
            Submission.user_id,
            Submission.primary_media_asset_id,
            Submission.status,
            Submission.submitted_at,
            Submission.created_at,
            SubmissionAttribute.real_name,
            SubmissionAttribute.animal_context,
            SubmissionAttribute.cute_name,
            SubmissionAttribute.caption,
            ScoreEvent.points,
            ScoreEvent.ledger,
            ScoreEvent.explanation_category,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id, isouter=True)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id, isouter=True)
    )

    if user_id:
        query = query.filter(Submission.user_id == user_id)
    if status:
        query = query.filter(Submission.status == status)
    if animal_context:
        query = query.filter(SubmissionAttribute.animal_context == animal_context)

    total = query.count()

    sort_column = {
        "createdAt": Submission.created_at,
        "submittedAt": Submission.submitted_at,
        "status": Submission.status,
        "points": ScoreEvent.points,
        "species": SubmissionAttribute.real_name,
    }.get(sort_by, Submission.created_at)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    rows = query.limit(limit).offset(offset).all()

    items = []
    for row in rows:
        score_event = None
        if row.points is not None:
            score_event = {
                "points": row.points,
                "ledger": row.ledger,
                "explanation": row.explanation_category,
            }
        items.append(
            {
                "submissionId": row.id,
                "userId": row.user_id,
                "mediaAssetId": row.primary_media_asset_id,
                "status": row.status,
                "submittedAt": row.submitted_at.isoformat() if row.submitted_at else None,
                "createdAt": row.created_at.isoformat() if row.created_at else None,
                "species": row.real_name,
                "context": row.animal_context,
                "cuteName": row.cute_name,
                "caption": row.caption,
                "scoreEvent": score_event,
            }
        )
    return items, total
