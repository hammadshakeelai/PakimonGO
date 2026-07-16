from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.infrastructure.auth.adapter import UserContext
from src.infrastructure.auth.dependencies import get_current_user
from src.infrastructure.database.repositories import create_notification
from src.infrastructure.database.repositories.social import (
    MAX_COMMENT_LEN,
    REACTION_KINDS,
    create_comment,
    get_comments,
    get_reaction_summary,
    get_submission_owner,
    soft_delete_comment,
    toggle_comment_like,
    toggle_reaction,
)
from src.infrastructure.database.session import get_db
from src.infrastructure.middleware.rate_limit import allow

router = APIRouter(tags=["social"])

COMMENTS_PER_MINUTE = 10


def _notify_owner(
    db: Session, actor_id: str, submission_id: str, kind: str, title: str, body: str
) -> None:
    owner = get_submission_owner(db, submission_id)
    if owner and owner != actor_id:
        create_notification(
            db,
            user_id=owner,
            notification_type=kind,
            title=title,
            body=body,
            reference_type="submission",
            reference_id=submission_id,
        )


@router.put("/submissions/{submission_id}/reaction")
def set_reaction(
    submission_id: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-001: toggle/replace the caller's reaction on a post."""
    kind = payload.get("kind")
    if kind not in REACTION_KINDS:
        raise HTTPException(
            status_code=400, detail=f"kind must be one of {sorted(REACTION_KINDS)}"
        )
    result = toggle_reaction(db, user.user_id, submission_id, kind)
    if result is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    if result:
        _notify_owner(
            db,
            user.user_id,
            submission_id,
            "reaction",
            "New reaction on your capture",
            f"{user.user_id} reacted {result.replace('_', ' ')} to your capture.",
        )
    summary = get_reaction_summary(db, [submission_id], user.user_id)[submission_id]
    return {
        "submissionId": submission_id,
        "myReaction": summary["myReaction"],
        "counts": summary["counts"],
    }


@router.get("/submissions/{submission_id}/comments")
def list_comments(
    submission_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    items, total = get_comments(
        db, submission_id, limit=limit, offset=offset, viewer_id=user.user_id)
    return {
        "items": items,
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }


@router.post("/submissions/{submission_id}/comments", status_code=201)
def post_comment(
    submission_id: str,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-002: comment on a post (rate limited)."""
    body = payload.get("body")
    if not body or not isinstance(body, str) or not body.strip():
        raise HTTPException(status_code=400, detail="body is required")
    body = body.strip()
    if len(body) > MAX_COMMENT_LEN:
        raise HTTPException(
            status_code=400, detail=f"body must be at most {MAX_COMMENT_LEN} chars"
        )
    if not allow(f"comment:{user.user_id}", COMMENTS_PER_MINUTE, 60.0):
        raise HTTPException(
            status_code=429, detail="Slow down — too many comments, try again shortly"
        )
    comment = create_comment(db, user.user_id, submission_id, body)
    if comment is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    _notify_owner(
        db,
        user.user_id,
        submission_id,
        "comment",
        "New comment on your capture",
        f'{user.user_id}: "{body[:120]}"',
    )
    return {
        "commentId": comment.id,
        "submissionId": submission_id,
        "userId": comment.user_id,
        "body": comment.body,
        "createdAt": comment.created_at.isoformat() if comment.created_at else None,
    }


@router.post("/comments/{comment_id}/like", status_code=201)
def like_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """FR-SOC-009: toggle a heart on a comment."""
    result = toggle_comment_like(db, user.user_id, comment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"commentId": comment_id, **result}


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    db: Session = Depends(get_db),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Delete the caller's own comment (soft delete)."""
    if not soft_delete_comment(db, user.user_id, comment_id):
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"status": "ok", "commentId": comment_id}
