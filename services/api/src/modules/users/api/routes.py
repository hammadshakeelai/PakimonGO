from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import (
    get_or_create_user,
    get_public_profile,
    get_user_collection,
    update_user,
)
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Get the current user's profile.

    Auto-creates a user row on first access. Returns userId,
    email, ageBand, homeRegion, trustState, and status.
    """
    user = get_or_create_user(db, current_user.user_id)
    return {
        "userId": user.id,
        "email": current_user.email,
        "status": user.status,
        "ageBand": user.age_band,
        "homeRegion": user.home_region,
        "trustState": user.trust_state,
        "createdAt": user.created_at.isoformat() if user.created_at else None,
    }


@router.get("/{user_id}/profile")
def get_user_public_profile(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Public profile of another player: stats + recent captures.

    No exact locations, no email — safe to show to any signed-in user.
    """
    profile = get_public_profile(db, user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@router.get("/me/collection")
def get_my_collection(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    context: str | None = Query(default=None, enum=["wild", "zoo", "pet", "unknown"]),
    sort_by: str = Query(default="totalPoints", enum=["totalPoints", "species", "captureCount", "lastCaptured"]),
    sort_order: str = Query(default="desc", enum=["asc", "desc"]),
    include_sensitive: bool = Query(
        default=False, description="Include sensitive species (requires elevated permissions)"
    ),
):
    """Get the current user's species collection with pagination.

    Groups captured species by common name with total points, capture
    count, and last capture date, plus a representative (most recent)
    submission's mediaAssetId and coarse publicLocation cell for the
    detail view. Excludes sensitive species by default unless
    include_sensitive=true.
    """
    collection, total = get_user_collection(
        db=db,
        user_id=current_user.user_id,
        limit=limit,
        offset=offset,
        context=context,
        sort_by=sort_by,
        sort_order=sort_order,
        include_sensitive=include_sensitive,
    )
    return {
        "userId": current_user.user_id,
        "species": collection,
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }


@router.patch("/me")
def patch_my_profile(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    """Update the current user's profile (ageBand, homeRegion).

    Accepts partial updates — only provided fields are changed.
    """
    age_band = body.get("ageBand")
    home_region = body.get("homeRegion")

    user = update_user(db, current_user.user_id, age_band=age_band, home_region=home_region)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "userId": user.id,
        "email": current_user.email,
        "status": user.status,
        "ageBand": user.age_band,
        "homeRegion": user.home_region,
        "trustState": user.trust_state,
        "createdAt": user.created_at.isoformat() if user.created_at else None,
    }
