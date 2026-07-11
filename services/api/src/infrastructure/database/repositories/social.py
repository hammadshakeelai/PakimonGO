from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Comment, Reaction, Submission

REACTION_KINDS = {"wow", "cute", "rare", "safe_shot"}
MAX_COMMENT_LEN = 500


def _submission_exists(db: Session, submission_id: str) -> bool:
    return db.query(Submission.id).filter(Submission.id == submission_id).first() is not None


def toggle_reaction(
    db: Session, user_id: str, submission_id: str, kind: str
) -> str | None:
    """Set/replace/remove the caller's reaction on a post.

    Same kind again = remove (toggle off); different kind = replace.
    Returns the resulting kind ("" when removed), or None if the
    submission doesn't exist.
    """
    if not _submission_exists(db, submission_id):
        return None
    existing = (
        db.query(Reaction)
        .filter(Reaction.user_id == user_id, Reaction.submission_id == submission_id)
        .first()
    )
    if existing is None:
        db.add(Reaction(user_id=user_id, submission_id=submission_id, kind=kind))
        result = kind
    elif existing.kind == kind:
        db.delete(existing)
        result = ""
    else:
        existing.kind = kind
        result = kind
    db.commit()
    return result


def get_reaction_summary(
    db: Session, submission_ids: list[str], viewer_id: str | None
) -> dict[str, dict]:
    """Per-submission reaction counts by kind + the viewer's own reaction.

    One GROUP BY over the page's IDs (no N+1); a second small query for
    the viewer's rows.
    """
    summary: dict[str, dict] = {
        sid: {"counts": {}, "myReaction": None} for sid in submission_ids
    }
    if not submission_ids:
        return summary
    rows = (
        db.query(Reaction.submission_id, Reaction.kind, func.count(Reaction.id))
        .filter(Reaction.submission_id.in_(submission_ids))
        .group_by(Reaction.submission_id, Reaction.kind)
        .all()
    )
    for sid, kind, count in rows:
        summary[sid]["counts"][kind] = count
    if viewer_id:
        mine = (
            db.query(Reaction.submission_id, Reaction.kind)
            .filter(
                Reaction.user_id == viewer_id,
                Reaction.submission_id.in_(submission_ids),
            )
            .all()
        )
        for sid, kind in mine:
            summary[sid]["myReaction"] = kind
    return summary


def get_comment_counts(db: Session, submission_ids: list[str]) -> dict[str, int]:
    counts = {sid: 0 for sid in submission_ids}
    if not submission_ids:
        return counts
    rows = (
        db.query(Comment.submission_id, func.count(Comment.id))
        .filter(Comment.submission_id.in_(submission_ids), Comment.deleted_at.is_(None))
        .group_by(Comment.submission_id)
        .all()
    )
    for sid, count in rows:
        counts[sid] = count
    return counts


def create_comment(
    db: Session, user_id: str, submission_id: str, body: str
) -> Comment | None:
    """Add a comment. Returns None if the submission doesn't exist."""
    if not _submission_exists(db, submission_id):
        return None
    comment = Comment(submission_id=submission_id, user_id=user_id, body=body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(
    db: Session, submission_id: str, limit: int = 50, offset: int = 0
) -> tuple[list[dict], int]:
    query = db.query(Comment).filter(
        Comment.submission_id == submission_id, Comment.deleted_at.is_(None)
    )
    total = query.count()
    rows = query.order_by(Comment.created_at.asc()).limit(limit).offset(offset).all()
    items = [
        {
            "commentId": c.id,
            "userId": c.user_id,
            "body": c.body,
            "createdAt": c.created_at.isoformat() if c.created_at else None,
        }
        for c in rows
    ]
    return items, total


def soft_delete_comment(db: Session, user_id: str, comment_id: str) -> bool:
    """Delete the caller's own comment. Returns False if absent or not theirs."""
    comment = (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
            Comment.user_id == user_id,
            Comment.deleted_at.is_(None),
        )
        .first()
    )
    if comment is None:
        return False
    comment.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return True


def get_submission_owner(db: Session, submission_id: str) -> str | None:
    row = db.query(Submission.user_id).filter(Submission.id == submission_id).first()
    return row[0] if row else None
