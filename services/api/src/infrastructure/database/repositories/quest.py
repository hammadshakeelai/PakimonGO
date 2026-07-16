from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import (
    Group,
    GroupMember,
    GroupQuest,
    Notification,
    ScoreEvent,
    Submission,
    SubmissionAttribute,
)

QUEST_KINDS = {"captures", "species", "points"}


def _as_utc(value: datetime | None) -> datetime | None:
    """SQLite hands back naive datetimes; stored values are always UTC."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _measure(db: Session, quest: GroupQuest, user_ids: set[str]) -> int:
    """Progress toward a quest for the given users, inside its window."""
    if not user_ids:
        return 0
    if quest.kind == "species":
        col = func.count(func.distinct(SubmissionAttribute.real_name))
    elif quest.kind == "points":
        col = func.coalesce(func.sum(ScoreEvent.points), 0)
    else:  # captures
        col = func.count(func.distinct(Submission.id))
    value = (
        db.query(col)
        .select_from(Submission)
        .join(SubmissionAttribute, SubmissionAttribute.submission_id == Submission.id)
        .join(ScoreEvent, ScoreEvent.submission_id == Submission.id)
        .filter(Submission.status.in_(["scored", "capped"]))
        .filter(Submission.user_id.in_(user_ids))
        .filter(Submission.created_at >= quest.starts_at)
        .filter(Submission.created_at <= quest.ends_at)
        .scalar()
    )
    return int(value or 0)


def list_group_quests(
    db: Session,
    group_id: str,
    member_ids: set[str],
    viewer_id: str | None = None,
) -> list[dict]:
    """Active quests for a group, with live progress and the viewer's own
    contribution (0 unless the viewer is a member)."""
    now = datetime.now(timezone.utc)
    quests = (
        db.query(GroupQuest)
        .filter(GroupQuest.group_id == group_id, GroupQuest.ends_at > now)
        .order_by(GroupQuest.ends_at.asc(), GroupQuest.created_at.asc())
        .all()
    )
    items = []
    for quest in quests:
        progress = _measure(db, quest, member_ids)
        mine = 0
        if viewer_id is not None and viewer_id in member_ids:
            mine = _measure(db, quest, {viewer_id})
        ends_at = _as_utc(quest.ends_at)
        items.append(
            {
                "questId": quest.id,
                "title": quest.title,
                "description": quest.description,
                "kind": quest.kind,
                "target": quest.target,
                "progress": progress,
                "myContribution": mine,
                "completed": progress >= quest.target,
                "startsAt": _as_utc(quest.starts_at).isoformat() if quest.starts_at else None,
                "endsAt": ends_at.isoformat() if ends_at else None,
                "secondsLeft": max(0, int((ends_at - now).total_seconds())) if ends_at else 0,
            }
        )
    return items


def notify_completed_quests(db: Session, user_id: str) -> int:
    """Called after one of ``user_id``'s captures is scored: any active
    quest in their groups that has now reached its target notifies every
    member (once per quest window — deduped against the notification
    log, scoped to the quest's starts_at so re-armed weekly quests can
    celebrate again). Returns the number of notifications created."""
    from .group import group_member_ids
    from .notification import create_notification

    group_ids = [
        r[0]
        for r in db.query(GroupMember.group_id)
        .filter(GroupMember.user_id == user_id)
        .all()
    ]
    if not group_ids:
        return 0
    now = datetime.now(timezone.utc)
    quests = (
        db.query(GroupQuest)
        .filter(GroupQuest.group_id.in_(group_ids), GroupQuest.ends_at > now)
        .all()
    )
    sent = 0
    for quest in quests:
        members = group_member_ids(db, quest.group_id)
        if _measure(db, quest, members) < quest.target:
            continue
        marker = f'"{quest.title}"'
        already = db.query(Notification.id).filter(
            Notification.notification_type == "quest_complete",
            Notification.reference_id == quest.group_id,
            Notification.body.like(f"{marker}%"),
        )
        if quest.starts_at is not None:
            already = already.filter(Notification.created_at >= quest.starts_at)
        if already.first() is not None:
            continue
        group = db.query(Group).filter(Group.id == quest.group_id).first()
        group_name = group.name if group else "your group"
        for member in members:
            create_notification(
                db,
                user_id=member,
                notification_type="quest_complete",
                title="Quest complete! 🎉",
                body=f"{marker} is done — {group_name} pulled it off!",
                reference_type="group",
                reference_id=quest.group_id,
            )
            sent += 1
    return sent


def create_quest(
    db: Session,
    group_id: str,
    title: str,
    target: int,
    ends_at: datetime,
    description: str | None = None,
    kind: str = "captures",
    starts_at: datetime | None = None,
) -> GroupQuest:
    quest = GroupQuest(
        group_id=group_id,
        title=title,
        description=description,
        kind=kind if kind in QUEST_KINDS else "captures",
        target=target,
        ends_at=ends_at,
    )
    if starts_at is not None:
        quest.starts_at = starts_at
    db.add(quest)
    db.commit()
    db.refresh(quest)
    return quest


def get_quest_by_title(db: Session, group_id: str, title: str) -> GroupQuest | None:
    return (
        db.query(GroupQuest)
        .filter(GroupQuest.group_id == group_id, GroupQuest.title == title)
        .first()
    )
