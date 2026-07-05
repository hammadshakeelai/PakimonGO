from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ..models import AuditLog, Block, Report, User

REPORT_TARGET_TYPES = {"submission", "user"}
REPORT_REASONS = {
    "inappropriate",
    "spam",
    "harassment",
    "unsafe_animal_interaction",
    "location_abuse",
    "other",
}


def _audit(db: Session, actor_user_id: str, action: str, target_type: str, target_id: str, meta: dict | None = None) -> None:
    db.add(
        AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            metadata_json=json.dumps(meta) if meta else None,
        )
    )


def create_report(
    db: Session,
    reporter_user_id: str,
    target_type: str,
    target_id: str,
    reason: str,
    details: str | None = None,
) -> Report | None:
    """Create a report. Returns None if this reporter already reported this target."""
    existing = (
        db.query(Report)
        .filter(
            Report.reporter_user_id == reporter_user_id,
            Report.target_type == target_type,
            Report.target_id == target_id,
        )
        .first()
    )
    if existing:
        return None
    report = Report(
        reporter_user_id=reporter_user_id,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        details=details,
    )
    db.add(report)
    _audit(db, reporter_user_id, "report_created", target_type, target_id, {"reason": reason})
    db.commit()
    db.refresh(report)
    return report


def create_block(db: Session, blocker_user_id: str, blocked_user_id: str) -> Block | None:
    """Block a user. Returns None if already blocked or the target doesn't exist."""
    if not db.query(User).filter(User.id == blocked_user_id).first():
        return None
    existing = (
        db.query(Block)
        .filter(
            Block.blocker_user_id == blocker_user_id,
            Block.blocked_user_id == blocked_user_id,
        )
        .first()
    )
    if existing:
        return existing
    block = Block(blocker_user_id=blocker_user_id, blocked_user_id=blocked_user_id)
    db.add(block)
    _audit(db, blocker_user_id, "user_blocked", "user", blocked_user_id)
    db.commit()
    db.refresh(block)
    return block


def delete_block(db: Session, blocker_user_id: str, blocked_user_id: str) -> bool:
    block = (
        db.query(Block)
        .filter(
            Block.blocker_user_id == blocker_user_id,
            Block.blocked_user_id == blocked_user_id,
        )
        .first()
    )
    if not block:
        return False
    db.delete(block)
    _audit(db, blocker_user_id, "user_unblocked", "user", blocked_user_id)
    db.commit()
    return True


def get_blocks(db: Session, blocker_user_id: str) -> list[Block]:
    return (
        db.query(Block)
        .filter(Block.blocker_user_id == blocker_user_id)
        .order_by(Block.created_at.desc())
        .all()
    )


def get_blocked_user_ids(db: Session, blocker_user_id: str) -> set[str]:
    rows = db.query(Block.blocked_user_id).filter(Block.blocker_user_id == blocker_user_id).all()
    return {r[0] for r in rows}
