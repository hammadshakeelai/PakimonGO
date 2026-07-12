from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.dependencies import get_optional_user
from src.infrastructure.database.models import (
    CaptureLocation,
    ScoreEvent,
    SensitiveSpecies,
    Submission,
    SubmissionAttribute,
)
from src.infrastructure.database.repositories import (
    get_blocked_user_ids,
    get_comment_counts,
    get_following_ids,
    get_reaction_summary,
)
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("")
def get_feed(
    limit: int = Query(default=20, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    scope: str = Query(default="all", pattern="^(all|following)$"),
    db: Session = Depends(get_db),
    user=Depends(get_optional_user),
) -> dict:
    """Timeline of recent scored captures.

    Photo-first feed items with species, points, and a coarse area label —
    exact coordinates never leave the server. Sensitive species are
    excluded; blocked users are hidden (FR-MOD-003). Shows public
    captures plus "friends"-visibility captures from people the viewer
    follows. ``scope=following`` narrows to followed users only.
    """
    return build_feed_page(db, user, limit, offset, scope=scope)


def build_feed_page(
    db: Session,
    user,
    limit: int,
    offset: int,
    scope: str = "all",
    restrict_user_ids: set[str] | None = None,
) -> dict:
    """Shared feed builder. ``restrict_user_ids`` limits results to those
    authors (used by the group feed)."""
    following = get_following_ids(db, user.user_id) if user else set()

    query = (
        db.query(
            Submission.id,
            Submission.user_id,
            Submission.primary_media_asset_id,
            Submission.created_at,
            SubmissionAttribute.real_name,
            SubmissionAttribute.cute_name,
            SubmissionAttribute.animal_context,
            SubmissionAttribute.caption,
            ScoreEvent.points,
            CaptureLocation.latitude,
            CaptureLocation.longitude,
        )
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .join(CaptureLocation, CaptureLocation.submission_id == Submission.id, isouter=True)
        .filter(Submission.status.in_(["scored", "capped"]))
        .filter(ScoreEvent.points.isnot(None))
    )

    # Public captures are visible to everyone; "friends" captures are
    # visible to people the author follows back (i.e. the viewer follows
    # the author). Private captures never appear.
    if following:
        query = query.filter(
            (Submission.visibility == "public")
            | (
                (Submission.visibility == "friends")
                & Submission.user_id.in_(following)
            )
        )
    else:
        query = query.filter(Submission.visibility == "public")

    if scope == "following":
        allowed = following | ({user.user_id} if user else set())
        query = query.filter(Submission.user_id.in_(allowed))

    if restrict_user_ids is not None:
        if not restrict_user_ids:
            return {"items": [], "pagination": {"limit": limit, "offset": offset, "total": 0}}
        query = query.filter(Submission.user_id.in_(restrict_user_ids))

    sensitive_subq = (
        db.query(SensitiveSpecies.scientific_name)
        .filter(SensitiveSpecies.scientific_name.ilike(SubmissionAttribute.real_name))
        .exists()
    )
    query = query.filter(~sensitive_subq)

    if user:
        blocked = get_blocked_user_ids(db, user.user_id)
        if blocked:
            query = query.filter(~Submission.user_id.in_(blocked))

    total = query.count()
    rows = (
        query.order_by(Submission.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    # Social aggregates for the page in two grouped queries (no N+1).
    page_ids = [row.id for row in rows]
    reactions = get_reaction_summary(db, page_ids, user.user_id if user else None)
    comment_counts = get_comment_counts(db, page_ids)

    items = []
    for row in rows:
        area = None
        if row.latitude is not None and row.longitude is not None:
            area = f"cell {round(row.latitude, 2):.2f}, {round(row.longitude, 2):.2f}"
        items.append(
            {
                "submissionId": row.id,
                "userId": row.user_id,
                "mediaAssetId": row.primary_media_asset_id,
                "species": row.real_name,
                "cuteName": row.cute_name,
                "context": row.animal_context,
                "caption": row.caption,
                "points": row.points,
                "area": area,
                "createdAt": row.created_at.isoformat() if row.created_at else None,
                "reactionCounts": reactions[row.id]["counts"],
                "myReaction": reactions[row.id]["myReaction"],
                "commentCount": comment_counts[row.id],
            }
        )
    return {
        "items": items,
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }
