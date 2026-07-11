from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.dependencies import get_optional_user
from src.infrastructure.database.repositories import (
    get_blocked_user_ids,
    get_following_ids,
    get_leaderboard,
    get_user_local_cell,
    get_users_in_cell,
)
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("")
def get_leaderboard_endpoint(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="totalScore", enum=["totalScore", "userId", "submissionCount"]),
    sort_order: str = Query(default="desc", enum=["asc", "desc"]),
    scope: str = Query(default="global", pattern="^(global|friends|local)$"),
    include_sensitive: bool = Query(
        default=False, description="Include sensitive species (requires elevated permissions)"
    ),
    db: Session = Depends(get_db),
    user=Depends(get_optional_user),
):
    """Get the leaderboard with pagination and sorting.

    Aggregates total scores across users. Excludes sensitive species and
    blocked users (FR-MOD-003). ``scope=friends`` restricts to the
    people the caller follows (plus themselves) and requires auth.
    """
    exclude = get_blocked_user_ids(db, user.user_id) if user else None
    include_only = None
    empty = {"entries": [], "pagination": {"limit": limit, "offset": offset, "total": 0}}
    if scope == "friends":
        if user is None:
            return empty
        include_only = get_following_ids(db, user.user_id) | {user.user_id}
    elif scope == "local":
        if user is None:
            return empty
        cell = get_user_local_cell(db, user.user_id)
        if cell is None:
            # No geolocated captures yet — nothing to anchor a local ranking.
            return empty
        include_only = get_users_in_cell(db, cell[0], cell[1])
    entries, total = get_leaderboard(
        db=db,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
        include_sensitive=include_sensitive,
        exclude_user_ids=exclude,
        include_only_user_ids=include_only,
    )
    return {
        "entries": entries,
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }
