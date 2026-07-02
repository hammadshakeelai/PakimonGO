from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ScoreState(str, Enum):
    PENDING = "pending"
    PRECHECKED = "prechecked"
    AI_EVALUATED = "ai_evaluated"
    SCORED = "scored"
    CAPPED = "capped"
    REVIEW = "review"
    REJECTED = "rejected"
    ROLLED_BACK = "rolled_back"


SCORE_STATE_VALUES: set[str] = {s.value for s in ScoreState}


_TRANSITIONS: dict[ScoreState, set[ScoreState]] = {
    ScoreState.PENDING: {
        ScoreState.PRECHECKED,
        ScoreState.REVIEW,
        ScoreState.REJECTED,
    },
    ScoreState.PRECHECKED: {
        ScoreState.AI_EVALUATED,
        ScoreState.CAPPED,
        ScoreState.REVIEW,
    },
    ScoreState.AI_EVALUATED: {
        ScoreState.SCORED,
        ScoreState.CAPPED,
        ScoreState.REVIEW,
    },
    ScoreState.REVIEW: {
        ScoreState.SCORED,
        ScoreState.CAPPED,
        ScoreState.REJECTED,
    },
    ScoreState.SCORED: {
        ScoreState.ROLLED_BACK,
    },
    ScoreState.CAPPED: {
        ScoreState.ROLLED_BACK,
    },
    ScoreState.REJECTED: set(),
    ScoreState.ROLLED_BACK: set(),
}


_INVALID_TRANSITIONS: dict[ScoreState, set[ScoreState]] = {
    ScoreState.PENDING: {ScoreState.SCORED},
    ScoreState.REJECTED: {ScoreState.SCORED, ScoreState.PENDING, ScoreState.PRECHECKED,
                          ScoreState.AI_EVALUATED, ScoreState.CAPPED, ScoreState.REVIEW},
    ScoreState.ROLLED_BACK: {ScoreState.SCORED, ScoreState.PENDING, ScoreState.PRECHECKED,
                             ScoreState.AI_EVALUATED, ScoreState.CAPPED, ScoreState.REVIEW,
                             ScoreState.REJECTED},
    ScoreState.SCORED: {ScoreState.SCORED},
    ScoreState.CAPPED: {ScoreState.SCORED},
}


def is_valid_transition(current: ScoreState, target: ScoreState) -> bool:
    return target in _TRANSITIONS.get(current, set())


def get_allowed_targets(state: ScoreState) -> set[ScoreState]:
    return _TRANSITIONS.get(state, set())


def is_terminal(state: ScoreState) -> bool:
    return len(_TRANSITIONS.get(state, set())) == 0


def client_may_initiate(state: ScoreState) -> bool:
    return state in {ScoreState.PENDING}


EXPLANATION_CATEGORIES = frozenset({
    "normal",
    "duplicate_cap",
    "zoo_cap",
    "pet_cap",
    "review_required",
    "unsafe_rejected",
    "low_confidence",
})


@dataclass
class ScoreEvent:
    event_id: str
    submission_id: str
    previous_state: ScoreState | None
    new_state: ScoreState
    formula_version: str | None = None
    explanation_category: str | None = None
    visible_points: int | None = None
    ledger: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = "system"

    def __post_init__(self) -> None:
        if self.previous_state is not None and not is_valid_transition(
            self.previous_state, self.new_state
        ):
            raise ValueError(
                f"Invalid transition: {self.previous_state.value} -> {self.new_state.value}"
            )
        if self.new_state in {ScoreState.SCORED, ScoreState.CAPPED, ScoreState.REJECTED}:
            if self.formula_version is None:
                raise ValueError(
                    f"Final state {self.new_state.value} requires formula_version"
                )
        if self.explanation_category is not None:
            if self.explanation_category not in EXPLANATION_CATEGORIES:
                raise ValueError(
                    f"Unknown explanation category: {self.explanation_category}"
                )
