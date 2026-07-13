from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import MediaAsset, Story, StoryReaction, StoryView

STORY_TTL_HOURS = 24
STORY_REACTION_EMOJI = {"heart", "fire", "wow", "clap"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_story(
    db: Session, user_id: str, media_asset_id: str, caption: str | None
) -> Story | None:
    """Post a 24-hour story. Returns None if the media asset isn't the caller's."""
    asset = (
        db.query(MediaAsset)
        .filter(MediaAsset.id == media_asset_id, MediaAsset.owner_user_id == user_id)
        .first()
    )
    if asset is None:
        return None
    story = Story(
        user_id=user_id,
        media_asset_id=media_asset_id,
        caption=caption,
        expires_at=_now() + timedelta(hours=STORY_TTL_HOURS),
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


def get_active_stories(
    db: Session, viewer_id: str | None, blocked: set[str] | None = None
) -> list[dict]:
    """All unexpired stories grouped per user (newest user first), with the
    viewer's seen flag resolved in one extra query (no N+1)."""
    now = _now()
    stories = (
        db.query(Story)
        .filter(Story.expires_at > now)
        .order_by(Story.created_at.asc())
        .all()
    )
    if blocked:
        stories = [s for s in stories if s.user_id not in blocked]
    seen_ids: set[str] = set()
    if viewer_id and stories:
        rows = (
            db.query(StoryView.story_id)
            .filter(
                StoryView.viewer_id == viewer_id,
                StoryView.story_id.in_([s.id for s in stories]),
            )
            .all()
        )
        seen_ids = {r[0] for r in rows}
    grouped: dict[str, dict] = {}
    for s in stories:
        entry = grouped.setdefault(
            s.user_id, {"userId": s.user_id, "stories": [], "allSeen": True}
        )
        seen = s.id in seen_ids
        entry["stories"].append(
            {
                "storyId": s.id,
                "mediaAssetId": s.media_asset_id,
                "caption": s.caption,
                "createdAt": s.created_at.isoformat() if s.created_at else None,
                "expiresAt": s.expires_at.isoformat(),
                "seen": seen,
                "isMine": s.user_id == viewer_id,
            }
        )
        if not seen:
            entry["allSeen"] = False
    # Viewer's own ring first, then users with unseen stories, then the rest.
    groups = list(grouped.values())
    groups.sort(key=lambda g: (g["userId"] != viewer_id, g["allSeen"]))
    return groups


def mark_story_viewed(db: Session, viewer_id: str, story_id: str) -> bool:
    """Record a view (idempotent). Returns False if story missing/expired."""
    story = (
        db.query(Story)
        .filter(Story.id == story_id, Story.expires_at > _now())
        .first()
    )
    if story is None:
        return False
    if story.user_id == viewer_id:
        return True  # own views aren't recorded
    existing = (
        db.query(StoryView)
        .filter(StoryView.story_id == story_id, StoryView.viewer_id == viewer_id)
        .first()
    )
    if existing is None:
        db.add(StoryView(story_id=story_id, viewer_id=viewer_id))
        db.commit()
    return True


def react_to_story(
    db: Session, viewer_id: str, story_id: str, emoji: str
) -> dict | None:
    """Upsert a quick reaction to someone else's active story.

    Returns None when the story is missing/expired, {"own": True} when
    the viewer owns the story, otherwise {"ownerId", "isNew"} — isNew is
    False when the viewer had already reacted (emoji is replaced)."""
    story = (
        db.query(Story)
        .filter(Story.id == story_id, Story.expires_at > _now())
        .first()
    )
    if story is None:
        return None
    if story.user_id == viewer_id:
        return {"own": True}
    row = (
        db.query(StoryReaction)
        .filter(
            StoryReaction.story_id == story_id,
            StoryReaction.viewer_id == viewer_id,
        )
        .first()
    )
    is_new = row is None
    if row is None:
        db.add(StoryReaction(story_id=story_id, viewer_id=viewer_id, emoji=emoji))
    else:
        row.emoji = emoji
    db.commit()
    return {"ownerId": story.user_id, "isNew": is_new}


def get_story_views(db: Session, owner_id: str, story_id: str) -> tuple[list[dict], int] | None:
    """Viewer list (with any quick reactions) for the owner's own story.
    None if not theirs."""
    story = (
        db.query(Story)
        .filter(Story.id == story_id, Story.user_id == owner_id)
        .first()
    )
    if story is None:
        return None
    rows = (
        db.query(StoryView)
        .filter(StoryView.story_id == story_id)
        .order_by(StoryView.viewed_at.desc())
        .all()
    )
    reactions = {
        r.viewer_id: r.emoji
        for r in db.query(StoryReaction)
        .filter(StoryReaction.story_id == story_id)
        .all()
    }
    items = [
        {
            "viewerId": v.viewer_id,
            "viewedAt": v.viewed_at.isoformat() if v.viewed_at else None,
            "reaction": reactions.get(v.viewer_id),
        }
        for v in rows
    ]
    return items, len(items)


def delete_story(db: Session, owner_id: str, story_id: str) -> bool:
    """Delete the owner's own story (and its views). False if not theirs."""
    story = (
        db.query(Story)
        .filter(Story.id == story_id, Story.user_id == owner_id)
        .first()
    )
    if story is None:
        return False
    db.query(StoryView).filter(StoryView.story_id == story_id).delete()
    db.query(StoryReaction).filter(StoryReaction.story_id == story_id).delete()
    db.delete(story)
    db.commit()
    return True


def count_active_stories(db: Session, user_id: str) -> int:
    return (
        db.query(func.count(Story.id))
        .filter(Story.user_id == user_id, Story.expires_at > _now())
        .scalar()
        or 0
    )
