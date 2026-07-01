
from sqlalchemy.orm import Session

from ..models import ScoreEvent


def create_score_event(
    db: Session,
    submission_id: str,
    user_id: str | None,
    ledger: str,
    points: int | None,
    event_type: str,
    formula_version: str | None = None,
    explanation_category: str | None = None,
    previous_state: str | None = None,
    new_state: str | None = None,
    actor: str = "system",
) -> ScoreEvent:
    event = ScoreEvent(
        submission_id=submission_id,
        user_id=user_id,
        ledger=ledger,
        points=points,
        event_type=event_type,
        formula_version=formula_version,
        explanation_category=explanation_category,
        previous_state=previous_state,
        new_state=new_state or event_type,
        actor=actor,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_latest_score_event(db: Session, submission_id: str) -> ScoreEvent | None:
    return (
        db.query(ScoreEvent)
        .filter(ScoreEvent.submission_id == submission_id)
        .order_by(ScoreEvent.created_at.desc())
        .first()
    )
