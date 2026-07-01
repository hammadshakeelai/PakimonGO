from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from precheck import run_precheck
from score_state import ScoreState


_SS_MAP: dict[str, ScoreState] = {
    "pending": ScoreState.PENDING,
    "prechecked": ScoreState.PRECHECKED,
    "ai_evaluated": ScoreState.AI_EVALUATED,
    "scored": ScoreState.SCORED,
    "capped": ScoreState.CAPPED,
    "review": ScoreState.REVIEW,
    "rejected": ScoreState.REJECTED,
    "rolled_back": ScoreState.ROLLED_BACK,
}


@dataclass
class GoldsetReport:
    dataset_id: str
    dataset_type: str
    total: int
    passed: int
    failed: int
    failures: list[dict] = field(default_factory=list)


def load_manifest(path: str | Path) -> dict:
    with open(path, "r") as f:
        manifest = yaml.safe_load(f)
    return validate_manifest(manifest)


def validate_manifest(manifest: dict) -> dict:
    _validate_manifest_structure(manifest)
    return manifest


def _validate_manifest_structure(manifest: dict) -> None:
    required = {"dataset_id", "dataset_type", "version", "items"}
    missing = required - set(manifest.keys())
    if missing:
        raise ValueError(f"Manifest missing required fields: {missing}")
    if not isinstance(manifest.get("items"), list):
        raise ValueError("Manifest must have an 'items' list")
    for item in manifest["items"]:
        if "item_id" not in item:
            raise ValueError("Each item must have an 'item_id'")


def run_scenario(item: dict) -> dict:
    inp = item["input"]
    ctx = inp.get("animal_context")
    existing = set(inp.get("existing_sha256s", []))
    current = inp.get("current_sha256")

    result = run_precheck(ctx, existing, current)

    expected = item["expected"]
    expected_state = _SS_MAP.get(expected.get("suggested_state", ""))

    errors = []
    if result.duplicate_found != expected.get("duplicate_found", False):
        errors.append(
            f"duplicate_found: got {result.duplicate_found}, "
            f"expected {expected.get('duplicate_found')}"
        )
    if result.explanation_category != expected.get("explanation_category", ""):
        errors.append(
            f"explanation_category: got {result.explanation_category}, "
            f"expected {expected.get('explanation_category')}"
        )
    if expected_state and result.suggested_state != expected_state:
        errors.append(
            f"suggested_state: got {result.suggested_state.value}, "
            f"expected {expected.get('suggested_state')}"
        )
    if result.context != expected.get("context", ""):
        errors.append(
            f"context: got {result.context}, expected {expected.get('context')}"
        )

    return {
        "item_id": item["item_id"],
        "description": item.get("description", ""),
        "passed": len(errors) == 0,
        "errors": errors,
        "result": {
            "duplicate_found": result.duplicate_found,
            "explanation_category": result.explanation_category,
            "suggested_state": result.suggested_state.value,
            "context": result.context,
        },
    }


def run_manifest(manifest: dict) -> GoldsetReport:
    report = GoldsetReport(
        dataset_id=manifest["dataset_id"],
        dataset_type=manifest["dataset_type"],
        total=len(manifest["items"]),
        passed=0,
        failed=0,
    )

    for item in manifest["items"]:
        outcome = run_scenario(item)
        if outcome["passed"]:
            report.passed += 1
        else:
            report.failed += 1
            report.failures.append(outcome)

    return report


def run_manifest_path(path: str | Path) -> GoldsetReport:
    manifest = load_manifest(path)
    return run_manifest(manifest)
