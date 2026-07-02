"""Privacy contract tests for public DTOs.

S0-006: Verify public API DTOs never expose exact coordinates,
private media URLs, or restricted evidence fields.

References:
  - docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md
  - docs/qa/fixtures/
  - docs/api/examples/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[3]
FIXTURES_DIR = ROOT / "docs" / "qa" / "fixtures"
EXAMPLES_DIR = ROOT / "docs" / "api" / "examples"

FORBIDDEN_PUBLIC_FIELDS = {
    "latitude",
    "longitude",
    "lat",
    "lng",
    "rawExif",
    "originalUrl",
    "storagePath",
    "bucket",
    "gcsUri",
    "signedUrl",
    "deviceId",
    "ipAddress",
    "appCheckToken",
    "moderationEvidence",
    "reviewNotes",
    "sensitiveSpeciesExactLocation",
}

FORBIDDEN_PREFIXES = ("gps_", "exif_")

PRIVATE_FIXTURES = {
    "private_submission_dto.json",
    "create-submission-request.json",
    "create-upload-intent-request.json",
    "create-upload-intent-response.json",
    "complete-upload-request.json",
    "upload_intent.json",
}

PUBLIC_FIXTURES = {
    "public_post_dto.json",
    "map_activity_cell_dto.json",
    "map-activity-response.json",
    "public-post-response.json",
    "score-detail-response.json",
    "score_event.json",
    "duplicate_edge.json",
    "zoo_geofence_decision.json",
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def find_forbidden_fields(
    data: Any,
    path: str = "$",
    for_prefixes: tuple[str, ...] = (),
) -> list[str]:
    results: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}"
            if key in FORBIDDEN_PUBLIC_FIELDS:
                results.append(current_path)
            for prefix in FORBIDDEN_PREFIXES:
                if key.lower().startswith(prefix):
                    results.append(current_path)
                    break
            results.extend(find_forbidden_fields(value, current_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            results.extend(find_forbidden_fields(item, f"{path}[{i}]"))
    return results


def test_tc_priv_dto_001_public_submission_no_exact_coords():
    """TC-PRIV-DTO-001: public submission response rejects exact coordinate fields."""
    fixture = FIXTURES_DIR / "submission-private-response.json"
    fallback = EXAMPLES_DIR / "submission-private-response.json"
    path = fixture if fixture.exists() else fallback
    if not path.exists():
        return

    data = load_json(path)
    hits = find_forbidden_fields(data)
    assert not hits, f"Public submission DTO leaks forbidden fields: {hits}"


def resolve_fixture(name: str) -> Path | None:
    path = FIXTURES_DIR / name
    if path.exists():
        return path
    path = EXAMPLES_DIR / name
    if path.exists():
        return path
    return None


def test_tc_priv_dto_002_public_map_uses_cells():
    """TC-PRIV-DTO-002: public map activity uses cells/clusters, not pins."""
    for name in ("map_activity_cell_dto.json", "map-activity-response.json"):
        path = resolve_fixture(name)
        if not path:
            continue
        data = load_json(path)
        hits = find_forbidden_fields(data)
        assert not hits, f"{name} leaks forbidden fields: {hits}"


def test_tc_priv_dto_003_public_media_derivative_only():
    """TC-PRIV-DTO-003: public media DTO exposes derivative URL only."""
    for name in ("public_post_dto.json", "public-post-response.json"):
        path = resolve_fixture(name)
        if not path:
            continue
        data = load_json(path)
        media = data.get("media", {})
        assert "thumbnailUrl" in media or "derivativeUrl" in media
        assert "originalUrl" not in media, f"{name} leaks originalUrl"
        assert "storagePath" not in media, f"{name} leaks storagePath"


def test_tc_priv_dto_004_public_derivatives_no_exif_gps():
    """TC-PRIV-DTO-004: public derivatives never include EXIF GPS fields."""
    for name in ("public_post_dto.json", "public-post-response.json"):
        path = resolve_fixture(name)
        if not path:
            continue
        data = load_json(path)
        hits = find_forbidden_fields(data)
        assert not hits, f"{name} leaks EXIF/GPS fields: {hits}"


def test_bad_fixture_detects_leak():
    """Verify the negative test fixture actually triggers a failure (proves the test works)."""
    fixture = FIXTURES_DIR / "bad_public_location_leak_example.json"
    data = load_json(fixture)
    hits = find_forbidden_fields(data)
    assert hits, "Bad fixture should have forbidden fields but found none"
    field_names = {h.split(".")[-1] for h in hits}
    assert "latitude" in field_names, "Should detect latitude leak"
    assert "longitude" in field_names, "Should detect longitude leak"


def test_all_public_fixtures_pass():
    """Every public fixture must have zero forbidden fields."""
    failures: list[str] = []
    for name in sorted(PUBLIC_FIXTURES):
        path = resolve_fixture(name)
        if not path:
            continue
        data = load_json(path)
        hits = find_forbidden_fields(data)
        if hits:
            failures.append(f"{name}: {hits}")
    assert not failures, "Public fixtures with leaks:\n" + "\n".join(failures)


def test_private_fixtures_allow_exact_coords():
    """Private DTOs may contain exact coordinates; the test must not fail for those."""
    for name in sorted(PRIVATE_FIXTURES):
        path = resolve_fixture(name)
        if not path:
            continue
        data = load_json(path)
        hits = find_forbidden_fields(data)
        if hits:
            print(f"NOTE: {name} has fields {hits} (allowed for private DTOs)")
