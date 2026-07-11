from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Follow, User


def follow_user(db: Session, follower_id: str, followee_id: str) -> bool:
    """Follow a user (idempotent). Returns False if self-follow or the
    followee doesn't exist."""
    if follower_id == followee_id:
        return False
    if db.query(User.id).filter(User.id == followee_id).first() is None:
        return False
    existing = (
        db.query(Follow)
        .filter(Follow.follower_id == follower_id, Follow.followee_id == followee_id)
        .first()
    )
    if existing is None:
        db.add(Follow(follower_id=follower_id, followee_id=followee_id))
        db.commit()
    return True


def unfollow_user(db: Session, follower_id: str, followee_id: str) -> bool:
    """Unfollow. Returns False if the edge didn't exist."""
    edge = (
        db.query(Follow)
        .filter(Follow.follower_id == follower_id, Follow.followee_id == followee_id)
        .first()
    )
    if edge is None:
        return False
    db.delete(edge)
    db.commit()
    return True


def is_following(db: Session, follower_id: str, followee_id: str) -> bool:
    return (
        db.query(Follow.follower_id)
        .filter(Follow.follower_id == follower_id, Follow.followee_id == followee_id)
        .first()
        is not None
    )


def get_following_ids(db: Session, follower_id: str) -> set[str]:
    rows = db.query(Follow.followee_id).filter(Follow.follower_id == follower_id).all()
    return {r[0] for r in rows}


def get_follower_ids(db: Session, followee_id: str) -> set[str]:
    rows = db.query(Follow.follower_id).filter(Follow.followee_id == followee_id).all()
    return {r[0] for r in rows}


def follow_counts(db: Session, user_id: str) -> tuple[int, int]:
    """(followers, following) for a user."""
    followers = (
        db.query(func.count(Follow.follower_id))
        .filter(Follow.followee_id == user_id)
        .scalar()
        or 0
    )
    following = (
        db.query(func.count(Follow.followee_id))
        .filter(Follow.follower_id == user_id)
        .scalar()
        or 0
    )
    return int(followers), int(following)


def list_follows(db: Session, user_id: str, direction: str) -> list[str]:
    """Ordered list of user ids. direction='followers' or 'following'."""
    if direction == "followers":
        rows = (
            db.query(Follow.follower_id)
            .filter(Follow.followee_id == user_id)
            .order_by(Follow.created_at.desc())
            .all()
        )
    else:
        rows = (
            db.query(Follow.followee_id)
            .filter(Follow.follower_id == user_id)
            .order_by(Follow.created_at.desc())
            .all()
        )
    return [r[0] for r in rows]
