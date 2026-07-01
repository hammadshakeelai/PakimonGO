from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from goldset_runner import (
    GoldsetReport,
    load_manifest,
    run_manifest,
    run_manifest_path,
    run_scenario,
    validate_manifest,
)

_DUP_MANIFEST = Path(__file__).resolve().parents[3] / "data" / "goldsets" / "duplicate-detection" / "manifest.yaml"
_ZOO_MANIFEST = Path(__file__).resolve().parents[3] / "data" / "goldsets" / "zoo-detection" / "manifest.yaml"


def test_duplicate_manifest_exists():
    assert _DUP_MANIFEST.exists(), f"Manifest not found: {_DUP_MANIFEST}"


def test_zoo_manifest_exists():
    assert _ZOO_MANIFEST.exists(), f"Manifest not found: {_ZOO_MANIFEST}"


def test_load_duplicate_manifest():
    manifest = load_manifest(str(_DUP_MANIFEST))
    assert manifest["dataset_id"] == "goldset-duplicate-detection-v0.1.0"
    assert len(manifest["items"]) == 9


def test_load_zoo_manifest():
    manifest = load_manifest(str(_ZOO_MANIFEST))
    assert manifest["dataset_id"] == "goldset-zoo-detection-v0.1.0"
    assert len(manifest["items"]) == 9


def test_run_scenario_passes():
    item = {
        "item_id": "test-001",
        "input": {
            "animal_context": "wild",
            "existing_sha256s": ["sha1"],
            "current_sha256": "sha2",
        },
        "expected": {
            "duplicate_found": False,
            "explanation_category": "normal",
            "suggested_state": "ai_evaluated",
            "context": "wild",
        },
    }
    outcome = run_scenario(item)
    assert outcome["passed"] is True
    assert outcome["errors"] == []


def test_run_scenario_fails():
    item = {
        "item_id": "test-002",
        "input": {
            "animal_context": "wild",
            "existing_sha256s": ["sha1"],
            "current_sha256": "sha2",
        },
        "expected": {
            "duplicate_found": True,
            "explanation_category": "normal",
            "suggested_state": "ai_evaluated",
            "context": "wild",
        },
    }
    outcome = run_scenario(item)
    assert outcome["passed"] is False
    assert len(outcome["errors"]) >= 1


def test_run_full_duplicate_manifest():
    manifest = load_manifest(str(_DUP_MANIFEST))
    report = run_manifest(manifest)
    assert isinstance(report, GoldsetReport)
    assert report.total == 9
    assert report.failed == 0
    assert report.passed == 9


def test_run_full_zoo_manifest():
    report = run_manifest_path(str(_ZOO_MANIFEST))
    assert isinstance(report, GoldsetReport)
    assert report.total == 9
    assert report.failed == 0
    assert report.passed == 9


def test_invalid_manifest_missing_fields():
    with pytest.raises(ValueError, match="missing required fields"):
        validate_manifest({"items": []})


def test_invalid_manifest_no_items():
    with pytest.raises(ValueError, match="must have an 'items' list"):
        validate_manifest({"dataset_id": "x", "dataset_type": "x", "version": "1", "items": "not_list"})


def test_invalid_manifest_item_no_id():
    with pytest.raises(ValueError, match="must have an 'item_id'"):
        validate_manifest({"dataset_id": "x", "dataset_type": "x", "version": "1", "items": [{"input": {}}]})


def test_run_manifest_path_not_found():
    with pytest.raises(FileNotFoundError):
        run_manifest_path("/nonexistent/manifest.yaml")
