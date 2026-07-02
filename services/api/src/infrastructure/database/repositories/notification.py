from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import Notification


def create_notification(
    db: Session,
    user_id: str,
    notification_type: str,
    title: str,
    body: str | None = None,
    reference_type: str | None = None,
    reference_id: str | None = None,
) -> Notification:
    n = Notification(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        body=body,
        reference_type=reference_type,
        reference_id=reference_id,
    )
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def get_notifications(
    db: Session,
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    unread_only: bool = False,
) -> tuple[list[Notification], int]:
    q = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        q = q.filter(Notification.is_read == False)
    total = q.count()
    items = q.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
    return items, total


def mark_notification_read(db: Session, notification_id: str, user_id: str) -> Notification | None:
    n = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id,
    ).first()
    if n:
        n.is_read = True
        db.commit()
        db.refresh(n)
    return n


def unread_notification_count(db: Session, user_id: str) -> int:
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False,
    ).count()
