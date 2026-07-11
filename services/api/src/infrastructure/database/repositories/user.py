from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import (
    ScoreEvent,
    SensitiveSpecies,
    Submission,
    SubmissionAttribute,
    User,
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


def get_public_profile(db: Session, user_id: str, recent_limit: int = 12) -> dict | None:
    """Public view of another player: stats + recent non-sensitive captures.

    Exact locations are never included (privacy) — only species, points,
    and media for the public feed treatment.
    """
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if user is None:
        return None
    totals = (
        db.query(func.coalesce(func.sum(ScoreEvent.points), 0), func.count(ScoreEvent.id))
        .join(Submission, Submission.id == ScoreEvent.submission_id)
        .filter(Submission.user_id == user_id, ScoreEvent.points.isnot(None))
        .first()
    )
    sensitive_subq = (
        db.query(SensitiveSpecies.scientific_name)
        .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
        .exists()
    )
    recent = (
        db.query(
            Submission.id,
            Submission.primary_media_asset_id,
            Submission.created_at,
            SubmissionAttribute.real_name,
            SubmissionAttribute.animal_context,
            ScoreEvent.points,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .filter(
            Submission.user_id == user_id,
            Submission.status.in_(["scored", "capped"]),
            Submission.visibility == "public",
            ScoreEvent.points.isnot(None),
            ~sensitive_subq,
        )
        .order_by(Submission.created_at.desc())
        .limit(recent_limit)
        .all()
    )
    return {
        "userId": user.id,
        "trustState": user.trust_state,
        "homeRegion": user.home_region,
        "memberSince": user.created_at.isoformat() if user.created_at else None,
        "totalPoints": int(totals[0]) if totals else 0,
        "captureCount": int(totals[1]) if totals else 0,
        "recentCaptures": [
            {
                "submissionId": r.id,
                "mediaAssetId": r.primary_media_asset_id,
                "species": r.real_name,
                "context": r.animal_context,
                "points": r.points,
                "createdAt": r.created_at.isoformat() if r.created_at else None,
            }
            for r in recent
        ],
    }
