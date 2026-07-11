
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import CaptureLocation, ScoreEvent, SensitiveSpecies, Submission, SubmissionAttribute, User


def _representatives_for(db: Session, user_id: str) -> dict:
    """Latest scored submission per (species, context) group for a user.

    Uses a row_number() window (SQLite >=3.25 and Postgres both support it)
    so the collection can show a representative photo and a coarse location
    for each species entry.
    """
    rn = func.row_number().over(
        partition_by=(SubmissionAttribute.real_name, SubmissionAttribute.animal_context),
        order_by=(ScoreEvent.created_at.desc(), Submission.created_at.desc()),
    ).label("rn")
    subq = (
        db.query(
            Submission.id.label("submission_id"),
            Submission.primary_media_asset_id.label("media_asset_id"),
            SubmissionAttribute.real_name.label("real_name"),
            SubmissionAttribute.animal_context.label("animal_context"),
            CaptureLocation.latitude.label("latitude"),
            CaptureLocation.longitude.label("longitude"),
            rn,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .join(CaptureLocation, CaptureLocation.submission_id == Submission.id, isouter=True)
        .filter(Submission.user_id == user_id)
        .filter(Submission.status.in_(["scored", "capped"]))
        .subquery()
    )
    rows = db.query(subq).filter(subq.c.rn == 1).all()
    return {(r.real_name, r.animal_context): r for r in rows}


def get_user_collection(
    db: Session,
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    context: str | None = None,
    sort_by: str = "totalPoints",
    sort_order: str = "desc",
    include_sensitive: bool = False,
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

    if not include_sensitive:
        sensitive_subq = (
            db.query(SensitiveSpecies.scientific_name)
            .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
            .exists()
        )
        query = query.filter(~sensitive_subq)

    total = query.count()

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

    reps = _representatives_for(db, user_id)
    items = []
    for row in rows:
        rep = reps.get((row.real_name, row.animal_context))
        # Coarse cell only (~1km rounding) — same privacy rule as the
        # submission list; the exact capture spot is never exposed.
        public_location = None
        if rep is not None and rep.latitude is not None and rep.longitude is not None:
            cell_lat = round(rep.latitude, 2)
            cell_lng = round(rep.longitude, 2)
            public_location = {
                "cellId": f"cell_{cell_lat:.2f}_{cell_lng:.2f}",
                "cellLatitude": cell_lat,
                "cellLongitude": cell_lng,
            }
        items.append(
            {
                "species": row.real_name,
                "context": row.animal_context,
                "totalPoints": row.total_points or 0,
                "captureCount": row.capture_count,
                "lastCaptured": row.last_captured.isoformat() if row.last_captured else None,
                "submissionId": rep.submission_id if rep is not None else None,
                "mediaAssetId": rep.media_asset_id if rep is not None else None,
                "publicLocation": public_location,
            }
        )
    return items, total


def get_leaderboard(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "totalScore",
    sort_order: str = "desc",
    include_sensitive: bool = False,
    exclude_user_ids: set[str] | None = None,
    include_only_user_ids: set[str] | None = None,
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
        .join(Submission, Submission.id == ScoreEvent.submission_id)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .filter(ScoreEvent.points.isnot(None))
    )
    if not include_sensitive:
        sensitive_subq = (
            db.query(SensitiveSpecies.scientific_name)
            .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
            .exists()
        )
        query = query.filter(~sensitive_subq)

    # FR-MOD-003: hide users the requester has blocked.
    if exclude_user_ids:
        query = query.filter(~User.id.in_(exclude_user_ids))

    # Friends scope: restrict to a specific set (followed users + self).
    if include_only_user_ids is not None:
        if not include_only_user_ids:
            return [], 0
        query = query.filter(User.id.in_(include_only_user_ids))

    query = query.group_by(User.id, User.age_band, User.home_region)

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
