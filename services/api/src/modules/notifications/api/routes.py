from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import get_notifications, mark_notification_read, unread_notification_count
from src.infrastructure.database.session import get_db

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    items, total = get_notifications(db, user.user_id, limit=limit, offset=offset, unread_only=unread_only)
    return {
        "items": [
            {
                "id": n.id,
                "notificationType": n.notification_type,
                "title": n.title,
                "body": n.body,
                "referenceType": n.reference_type,
                "referenceId": n.reference_id,
                "isRead": n.is_read,
                "createdAt": n.created_at.isoformat() if n.created_at else None,
            }
            for n in items
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.patch("/{notification_id}/read")
def read_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    n = mark_notification_read(db, notification_id, user.user_id)
    if not n:
        return {"status": "not_found"}
    return {
        "status": "ok",
        "notification": {
            "id": n.id,
            "isRead": n.is_read,
        },
    }


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    count = unread_notification_count(db, user.user_id)
    return {"count": count}
