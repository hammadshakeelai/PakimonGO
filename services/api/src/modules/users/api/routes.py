from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import get_or_create_user, get_user_collection, update_user
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
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


@router.get("/me/collection")
def get_my_collection(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
    collection = get_user_collection(db, current_user.user_id)
    return {"userId": current_user.user_id, "species": collection}


@router.patch("/me")
def patch_my_profile(
    body: dict,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user),
):
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
