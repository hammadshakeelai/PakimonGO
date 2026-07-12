from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Group, GroupMember, User


def member_count(db: Session, group_id: str) -> int:
    return (
        db.query(func.count(GroupMember.user_id))
        .filter(GroupMember.group_id == group_id)
        .scalar()
        or 0
    )


def group_member_ids(db: Session, group_id: str) -> set[str]:
    rows = db.query(GroupMember.user_id).filter(GroupMember.group_id == group_id).all()
    return {r[0] for r in rows}


def is_member(db: Session, group_id: str, user_id: str) -> bool:
    return (
        db.query(GroupMember.user_id)
        .filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        .first()
        is not None
    )


def _to_dict(db: Session, g: Group, viewer_id: str | None) -> dict:
    return {
        "groupId": g.id,
        "name": g.name,
        "description": g.description,
        "coverAsset": g.cover_asset,
        "isPublic": g.is_public,
        "memberCount": member_count(db, g.id),
        "isMember": is_member(db, g.id, viewer_id) if viewer_id else False,
        "createdAt": g.created_at.isoformat() if g.created_at else None,
    }


def list_groups(db: Session, viewer_id: str | None) -> list[dict]:
    groups = db.query(Group).order_by(Group.created_at.asc()).all()
    return [_to_dict(db, g, viewer_id) for g in groups]


def get_group(db: Session, group_id: str, viewer_id: str | None) -> dict | None:
    g = db.query(Group).filter(Group.id == group_id).first()
    if g is None:
        return None
    return _to_dict(db, g, viewer_id)


def join_group(db: Session, group_id: str, user_id: str) -> bool:
    """Join a group (idempotent). False if the group doesn't exist."""
    if db.query(Group.id).filter(Group.id == group_id).first() is None:
        return False
    if not is_member(db, group_id, user_id):
        db.add(GroupMember(group_id=group_id, user_id=user_id))
        db.commit()
    return True


def leave_group(db: Session, group_id: str, user_id: str) -> bool:
    row = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        .first()
    )
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True


def list_members(db: Session, group_id: str) -> list[str]:
    rows = (
        db.query(GroupMember.user_id)
        .filter(GroupMember.group_id == group_id)
        .order_by(GroupMember.joined_at.asc())
        .all()
    )
    return [r[0] for r in rows]


def create_group(
    db: Session,
    name: str,
    description: str | None = None,
    cover_asset: str | None = None,
    created_by: str | None = None,
) -> Group:
    g = Group(
        name=name,
        description=description,
        cover_asset=cover_asset,
        created_by=created_by,
    )
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


def get_group_by_name(db: Session, name: str) -> Group | None:
    return db.query(Group).filter(Group.name == name).first()


def add_member(db: Session, group_id: str, user_id: str, role: str = "member") -> None:
    if not is_member(db, group_id, user_id):
        if db.query(User.id).filter(User.id == user_id).first() is not None:
            db.add(GroupMember(group_id=group_id, user_id=user_id, role=role))
            db.commit()
