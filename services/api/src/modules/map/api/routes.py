from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import get_blocked_user_ids
from src.infrastructure.database.repositories.map_sightings import (
    get_public_sightings,
)
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/map", tags=["map"])


@router.get("/sightings")
def sightings(
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """The living map: recent PUBLIC community captures at coarse ~1km
    cells (exact GPS is never exposed). Sensitive species and users the
    caller has blocked are excluded."""
    items = get_public_sightings(
        db, limit=limit, blocked=get_blocked_user_ids(db, user.user_id))
    return {"items": items, "total": len(items)}
