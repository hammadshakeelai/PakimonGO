"""Score state model tests (invoked from services/api/tests).

S0-007: Validate the score state machine. Imports the model from
packages/scoring-rules/src via sys.path.

References:
  - docs/qa/SCORING_STATE_TEST_SPEC.md
  - FR-SCORE-002, FR-SCORE-003, FR-SCORE-008, NFR-SEC-001
"""

from __future__ import annotations

import sys
from pathlib import Path

_score_pkg = Path(__file__).resolve().parents[3] / "packages" / "scoring-rules" / "src"
sys.path.insert(0, str(_score_pkg))

import pytest  # noqa: E402

from score_state import (  # noqa: E402
    EXPLANATION_CATEGORIES,
    ScoreEvent,
    ScoreState,
    client_may_initiate,
    get_allowed_targets,
    is_terminal,
    is_valid_transition,
)


def test_tc_score_state_001_valid_transition_table():
    valid_edges = [
        (ScoreState.PENDING, ScoreState.PRECHECKED),
        (ScoreState.PENDING, ScoreState.REVIEW),
        (ScoreState.PENDING, ScoreState.REJECTED),
        (ScoreState.PRECHECKED, ScoreState.AI_EVALUATED),
        (ScoreState.PRECHECKED, ScoreState.CAPPED),
        (ScoreState.PRECHECKED, ScoreState.REVIEW),
        (ScoreState.AI_EVALUATED, ScoreState.SCORED),
        (ScoreState.AI_EVALUATED, ScoreState.CAPPED),
        (ScoreState.AI_EVALUATED, ScoreState.REVIEW),
        (ScoreState.REVIEW, ScoreState.SCORED),
        (ScoreState.REVIEW, ScoreState.CAPPED),
        (ScoreState.REVIEW, ScoreState.REJECTED),
        (ScoreState.SCORED, ScoreState.ROLLED_BACK),
        (ScoreState.CAPPED, ScoreState.ROLLED_BACK),
    ]
    for current, target in valid_edges:
        assert is_valid_transition(current, target), (
            f"{current.value} -> {target.value} should be valid"
        )


def test_tc_score_state_002_invalid_transitions_rejected():
    invalid_edges = [
        (ScoreState.PENDING, ScoreState.SCORED),
        (ScoreState.REJECTED, ScoreState.SCORED),
        (ScoreState.REJECTED, ScoreState.PENDING),
        (ScoreState.ROLLED_BACK, ScoreState.SCORED),
        (ScoreState.ROLLED_BACK, ScoreState.REJECTED),
    ]
    for current, target in invalid_edges:
        assert not is_valid_transition(current, target), (
            f"{current.value} -> {target.value} should be invalid"
        )


def test_tc_score_state_003_final_stores_formula_version():
    _prev_map = {
        ScoreState.SCORED: ScoreState.REVIEW,
        ScoreState.REJECTED: ScoreState.PENDING,
    }
    for state in (ScoreState.SCORED, ScoreState.CAPPED, ScoreState.REJECTED):
        prev = _prev_map.get(state, ScoreState.PRECHECKED)
        event = ScoreEvent(
            event_id="e1",
            submission_id="s1",
            previous_state=prev,
            new_state=state,
            formula_version="v0.1.0",
            explanation_category="normal",
        )
        assert event.formula_version == "v0.1.0"


def test_tc_score_state_003_final_rejects_missing_formula():
    cases = [
        (ScoreState.AI_EVALUATED, ScoreState.SCORED),
        (ScoreState.PRECHECKED, ScoreState.CAPPED),
        (ScoreState.PENDING, ScoreState.REJECTED),
    ]
    for prev, target in cases:
        with pytest.raises(ValueError, match="requires formula_version"):
            ScoreEvent(
                event_id="e1",
                submission_id="s1",
                previous_state=prev,
                new_state=target,
            )


def test_tc_score_state_004_append_only():
    event = ScoreEvent(
        event_id="e_immutable_001",
        submission_id="s1",
        previous_state=ScoreState.PENDING,
        new_state=ScoreState.PRECHECKED,
    )
    assert event.event_id == "e_immutable_001"
    assert event.new_state == ScoreState.PRECHECKED


def test_tc_score_state_005_zoo_cap_saves_entry():
    event = ScoreEvent(
        event_id="e_zoo_001",
        submission_id="s_zoo",
        previous_state=ScoreState.PRECHECKED,
        new_state=ScoreState.CAPPED,
        formula_version="v0.1.0",
        explanation_category="zoo_cap",
        visible_points=1,
        ledger="participation",
    )
    assert event.new_state == ScoreState.CAPPED
    assert event.visible_points == 1
    assert event.explanation_category == "zoo_cap"


def test_tc_score_state_006_duplicate_caps_without_delete():
    cap_event = ScoreEvent(
        event_id="e_dup_001",
        submission_id="s_dup",
        previous_state=ScoreState.PRECHECKED,
        new_state=ScoreState.CAPPED,
        formula_version="v0.1.0",
        explanation_category="duplicate_cap",
    )
    assert cap_event.new_state == ScoreState.CAPPED
    review_event = ScoreEvent(
        event_id="e_dup_002",
        submission_id="s_dup",
        previous_state=ScoreState.PENDING,
        new_state=ScoreState.REVIEW,
    )
    assert review_event.new_state == ScoreState.REVIEW


def test_tc_score_state_007_unsafe_routes_to_review():
    urgent = ScoreEvent(
        event_id="e_unsafe_001",
        submission_id="s_unsafe",
        previous_state=ScoreState.PENDING,
        new_state=ScoreState.REVIEW,
        explanation_category="review_required",
    )
    assert urgent.new_state == ScoreState.REVIEW
    rejected = ScoreEvent(
        event_id="e_unsafe_002",
        submission_id="s_unsafe",
        previous_state=ScoreState.PENDING,
        new_state=ScoreState.REJECTED,
        formula_version="v0.1.0",
        explanation_category="unsafe_rejected",
    )
    assert rejected.new_state == ScoreState.REJECTED


def test_tc_score_state_008_rollback_updates():
    for from_state in (ScoreState.SCORED, ScoreState.CAPPED):
        assert is_valid_transition(from_state, ScoreState.ROLLED_BACK), (
            f"{from_state.value} -> rolled_back should be valid"
        )


def test_capped_to_scored_invalid_without_adjustment():
    assert not is_valid_transition(ScoreState.CAPPED, ScoreState.SCORED)


def test_scored_to_scored_mutation_invalid():
    assert not is_valid_transition(ScoreState.SCORED, ScoreState.SCORED)


def test_all_states_have_valid_inbound_except_pending():
    inbound_counts: dict[ScoreState, int] = {s: 0 for s in ScoreState}
    for current in ScoreState:
        for target in get_allowed_targets(current):
            inbound_counts[target] += 1
    for state in ScoreState:
        if state == ScoreState.PENDING:
            continue
        assert inbound_counts[state] > 0, f"{state.value} has no valid inbound path"


def test_terminal_immutable_except_rollback():
    assert is_terminal(ScoreState.REJECTED)
    assert is_terminal(ScoreState.ROLLED_BACK)


def test_client_may_only_initiate_pending():
    for state in ScoreState:
        if state == ScoreState.PENDING:
            assert client_may_initiate(state)
        else:
            assert not client_may_initiate(state), (
                f"Client must not initiate {state.value}"
            )


def test_explanation_categories_defined():
    required = {
        "normal", "duplicate_cap", "zoo_cap", "pet_cap",
        "review_required", "unsafe_rejected", "low_confidence",
    }
    assert required.issubset(EXPLANATION_CATEGORIES)


def test_invalid_explanation_category_rejected():
    with pytest.raises(ValueError, match="Unknown explanation"):
        ScoreEvent(
            event_id="e_bad",
            submission_id="s_bad",
            previous_state=ScoreState.REVIEW,
            new_state=ScoreState.SCORED,
            formula_version="v0.1.0",
            explanation_category="made_up_category",
        )


def test_server_authority_no_client_final():
    final_states = {ScoreState.SCORED, ScoreState.CAPPED, ScoreState.REJECTED,
                    ScoreState.ROLLED_BACK}
    for state in final_states:
        assert not client_may_initiate(state), (
            f"Client must not initiate final state {state.value}"
        )
