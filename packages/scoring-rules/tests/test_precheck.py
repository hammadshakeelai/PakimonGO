from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from precheck import run_precheck
from score_state import ScoreState


def test_wild_submission_no_duplicate():
    result = run_precheck("wild", set(), "sha001")
    assert result.duplicate_found is False
    assert result.explanation_category == "normal"
    assert result.suggested_state == ScoreState.AI_EVALUATED
    assert result.context == "wild"


def test_zoo_submission_no_duplicate():
    result = run_precheck("zoo", set(), "sha002")
    assert result.duplicate_found is False
    assert result.explanation_category == "zoo_cap"
    assert result.suggested_state == ScoreState.CAPPED
    assert result.context == "zoo"


def test_pet_submission_no_duplicate():
    result = run_precheck("pet", set(), "sha003")
    assert result.duplicate_found is False
    assert result.explanation_category == "pet_cap"
    assert result.suggested_state == ScoreState.CAPPED
    assert result.context == "pet"


def test_duplicate_detected():
    result = run_precheck("wild", {"sha001", "sha002"}, "sha001")
    assert result.duplicate_found is True
    assert result.explanation_category == "duplicate_cap"
    assert result.suggested_state == ScoreState.CAPPED
    assert result.context == "duplicate"


def test_duplicate_takes_priority_over_zoo():
    result = run_precheck("zoo", {"sha001"}, "sha001")
    assert result.duplicate_found is True
    assert result.explanation_category == "duplicate_cap"
    assert result.context == "duplicate"


def test_unknown_context_no_duplicate():
    result = run_precheck("unknown", set(), "sha004")
    assert result.duplicate_found is False
    assert result.explanation_category == "normal"
    assert result.suggested_state == ScoreState.AI_EVALUATED
    assert result.context == "unknown"


def test_empty_sha256_not_duplicate():
    result = run_precheck("wild", {"sha001", "sha002"}, "")
    assert result.duplicate_found is False
    assert result.explanation_category == "normal"


def test_none_sha256_not_duplicate():
    result = run_precheck("wild", {"sha001"}, None)
    assert result.duplicate_found is False
    assert result.explanation_category == "normal"
