"""Validate JSON examples and QA fixtures.

This intentionally checks syntax only. Schema-specific validation should be
added after generated contracts exist.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_DIRS = (
    ROOT / "docs" / "api" / "examples",
    ROOT / "docs" / "qa" / "fixtures",
)


@dataclass
class JsonCheck:
    path: Path
    ok: bool
    message: str


def check_json_file(path: Path) -> JsonCheck:
    try:
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
    except Exception as exc:
        return JsonCheck(path, False, str(exc))
    return JsonCheck(path, True, "valid")


def main() -> int:
    paths: list[Path] = []
    for directory in JSON_DIRS:
        if directory.exists():
            paths.extend(sorted(directory.glob("*.json")))

    results = [check_json_file(path) for path in paths]
    failures = [result for result in results if not result.ok]

    print("PASS json_examples" if not failures else "FAIL json_examples")
    print(f"  files={len(results)}")
    print(f"  failures={len(failures)}")
    for failure in failures:
        print(f"  {failure.path.relative_to(ROOT)}: {failure.message}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
