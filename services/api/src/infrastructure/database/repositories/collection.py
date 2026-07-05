
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import ScoreEvent, SensitiveSpecies, Submission, SubmissionAttribute, User


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
    include_sensitive: bool = False,
    exclude_user_ids: set[str] | None = None,
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
