from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import (
    create_block,
    create_report,
    delete_block,
    get_blocks,
)
from src.infrastructure.database.repositories.moderation import (
    REPORT_REASONS,
    REPORT_TARGET_TYPES,
)
from src.infrastructure.database.session import get_db

router = APIRouter(tags=["moderation"])

MAX_DETAILS_LEN = 2000


@router.post("/reports", status_code=201)
def submit_report(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-MOD-001/002: report a submission or a user."""
    target_type = payload.get("targetType")
    target_id = payload.get("targetId")
    reason = payload.get("reason")
    details = payload.get("details")

    if target_type not in REPORT_TARGET_TYPES:
        raise HTTPException(status_code=400, detail="targetType must be 'submission' or 'user'")
    if not target_id or not isinstance(target_id, str):
        raise HTTPException(status_code=400, detail="targetId is required")
    if reason not in REPORT_REASONS:
        raise HTTPException(status_code=400, detail=f"reason must be one of {sorted(REPORT_REASONS)}")
    if details is not None and (not isinstance(details, str) or len(details) > MAX_DETAILS_LEN):
        raise HTTPException(status_code=400, detail="details must be a string of at most 2000 chars")
    if target_type == "user" and target_id == user.user_id:
        raise HTTPException(status_code=400, detail="You cannot report yourself")

    report = create_report(db, user.user_id, target_type, target_id, reason, details)
    if report is None:
        raise HTTPException(status_code=409, detail="You have already reported this")
    return {
        "reportId": report.id,
        "targetType": report.target_type,
        "targetId": report.target_id,
        "reason": report.reason,
        "status": report.status,
        "createdAt": report.created_at.isoformat() if report.created_at else None,
    }


@router.get("/blocks")
def list_blocks(
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    blocks = get_blocks(db, user.user_id)
    return {
        "items": [
            {
                "blockedUserId": b.blocked_user_id,
                "createdAt": b.created_at.isoformat() if b.created_at else None,
            }
            for b in blocks
        ],
        "total": len(blocks),
    }


@router.post("/blocks/{blocked_user_id}", status_code=201)
def block_user(
    blocked_user_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-MOD-003: block a user. Their entries disappear from your leaderboard."""
    if blocked_user_id == user.user_id:
        raise HTTPException(status_code=400, detail="You cannot block yourself")
    block = create_block(db, user.user_id, blocked_user_id)
    if block is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "blockedUserId": block.blocked_user_id,
        "createdAt": block.created_at.isoformat() if block.created_at else None,
    }


@router.delete("/blocks/{blocked_user_id}")
def unblock_user(
    blocked_user_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    removed = delete_block(db, user.user_id, blocked_user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Block not found")
    return {"status": "ok", "blockedUserId": blocked_user_id}
