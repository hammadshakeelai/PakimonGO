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
    db: Session = Depends(get_db),
    _=Depends(get_optional_user),
):
    entries = get_leaderboard(db, limit=limit)
    return {"entries": entries, "totalReturned": len(entries)}
