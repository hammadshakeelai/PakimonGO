from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import (
    create_notification,
    get_blocked_user_ids,
)
from src.infrastructure.database.repositories.story import (
    STORY_REACTION_EMOJI,
    create_story,
    delete_story,
    get_active_stories,
    get_story_views,
    mark_story_viewed,
    react_to_story,
)
from src.infrastructure.database.session import get_db
from src.infrastructure.middleware.rate_limit import allow

router = APIRouter(prefix="/stories", tags=["stories"])

MAX_CAPTION_LEN = 280
STORIES_PER_HOUR = 20


@router.get("")
def list_stories(
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-003: active (24h) stories grouped per user, own ring first."""
    blocked = get_blocked_user_ids(db, user.user_id)
    groups = get_active_stories(db, user.user_id, blocked)
    return {"groups": groups, "total": sum(len(g["stories"]) for g in groups)}


@router.post("", status_code=201)
def post_story(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    media_asset_id = payload.get("mediaAssetId")
    caption = payload.get("caption")
    if not media_asset_id or not isinstance(media_asset_id, str):
        raise HTTPException(status_code=400, detail="mediaAssetId is required")
    if caption is not None and (
        not isinstance(caption, str) or len(caption) > MAX_CAPTION_LEN
    ):
        raise HTTPException(
            status_code=400, detail=f"caption must be at most {MAX_CAPTION_LEN} chars"
        )
    if not allow(f"story:{user.user_id}", STORIES_PER_HOUR, 3600.0):
        raise HTTPException(status_code=429, detail="Too many stories — try again later")
    story = create_story(db, user.user_id, media_asset_id, caption)
    if story is None:
        raise HTTPException(status_code=404, detail="Media asset not found or not yours")
    return {
        "storyId": story.id,
        "mediaAssetId": story.media_asset_id,
        "caption": story.caption,
        "createdAt": story.created_at.isoformat() if story.created_at else None,
        "expiresAt": story.expires_at.isoformat(),
    }


@router.delete("/{story_id}")
def remove_story(
    story_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Delete the caller's own story."""
    if not delete_story(db, user.user_id, story_id):
        raise HTTPException(status_code=404, detail="Story not found")
    return {"status": "ok", "storyId": story_id}


@router.post("/{story_id}/view")
def view_story(
    story_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-004: record that the caller viewed a story (idempotent)."""
    if not mark_story_viewed(db, user.user_id, story_id):
        raise HTTPException(status_code=404, detail="Story not found or expired")
    return {"status": "ok", "storyId": story_id}


@router.post("/{story_id}/react", status_code=201)
def react(
    story_id: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-008: quick emoji reaction to someone's story. Re-reacting
    replaces the emoji; the first reaction notifies the owner."""
    emoji = payload.get("emoji")
    if emoji not in STORY_REACTION_EMOJI:
        raise HTTPException(
            status_code=400,
            detail=f"emoji must be one of {sorted(STORY_REACTION_EMOJI)}",
        )
    result = react_to_story(db, user.user_id, story_id, emoji)
    if result is None:
        raise HTTPException(status_code=404, detail="Story not found or expired")
    if result.get("own"):
        raise HTTPException(
            status_code=400, detail="You cannot react to your own story")
    if result["isNew"]:
        create_notification(
            db,
            user_id=result["ownerId"],
            notification_type="story_reaction",
            title="Story reaction",
            body=f"{user.user_id} reacted to your story.",
            reference_type="user",
            reference_id=user.user_id,
        )
    return {"status": "ok", "storyId": story_id, "emoji": emoji}


@router.get("/{story_id}/views")
def story_views(
    story_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Viewer list — only for the story's owner."""
    result = get_story_views(db, user.user_id, story_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Story not found")
    items, total = result
    return {"items": items, "total": total}
