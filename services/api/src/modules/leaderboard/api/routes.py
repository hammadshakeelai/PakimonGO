from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.dependencies import get_optional_user
from src.infrastructure.database.repositories import get_leaderboard
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/leaderboard", tags=["leaderboard"])


@router.get("")
def get_leaderboard_endpoint(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    sort_by: str = Query(default="totalScore", enum=["totalScore", "userId", "submissionCount"]),
    sort_order: str = Query(default="desc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    _=Depends(get_optional_user),
):
    entries, total = get_leaderboard(
        db=db,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return {
        "entries": entries,
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }
