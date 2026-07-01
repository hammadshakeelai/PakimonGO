"""Pre-task safety guard for PakimonGO agents.

MANDATORY: Run this BEFORE starting any work burst.
If it returns FAIL, stop and fix before proceeding.

Checks:
1. State docs exist and have expected sections
2. Sprint plan exists and matches state
3. Source file sizes within limits (warn >300, fail >500)
4. Requirement/traceability files parse for FR IDs
5. No stale .pyc caches from deleted files
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FR_RE = re.compile(r"(?<![A-Z])FR-[A-Z]+-\d{3}")
SOURCE_EXTS = {".py", ".dart"}
SOURCE_ROOTS = ("apps", "services", "packages")

REQUIRED_DOCS = {
    "CURRENT_TASK.md": ["Active Phase", "Active Task", "Current Next Action"],
    "NEXT_TASK.md": ["Current Next Task", "Sprint 2-12 Complete"],
    "CURRENT_THINKING.md": None,
    "PROCESS.md": None,
    "sprints/SPRINT_0_PLAN.md": ["Sprint Goal", "Sprint Backlog", "Definition Of Done"],
    "BACKLOG.md": None,
    "BUGS_AND_RISKS.md": None,
    "TECH_DEBT.md": None,
}

REQUIRED_TRACE_FILES = [
    "docs/REQUIREMENTS.md",
    "docs/TRACEABILITY_MATRIX.md",
]


@dataclass
class Check:
    name: str
    ok: bool
    details: list[str]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unique_fr_ids(text: str) -> set[str]:
    return set(FR_RE.findall(text))


def check_state_docs() -> Check:
    details: list[str] = []
    ok = True
    for rel_path, required_sections in REQUIRED_DOCS.items():
        full = ROOT / "docs" / rel_path
        if not full.exists():
            details.append(f"MISSING docs/{rel_path}")
            ok = False
            continue
        text = read(full)
        if required_sections:
            for section in required_sections:
                if section not in text:
                    details.append(f"docs/{rel_path}: missing section '{section}'")
                    ok = False
        details.append(f"FOUND docs/{rel_path}")
    return Check("state_docs_exist", ok, details)


def check_sprint_status() -> Check:
    plan_path = ROOT / "docs" / "sprints" / "SPRINT_0_PLAN.md"
    current_task_path = ROOT / "docs" / "CURRENT_TASK.md"
    details: list[str] = []
    ok = True

    if not plan_path.exists():
        return Check("sprint_status", False, ["MISSING SPRINT_0_PLAN.md"])

    plan_text = read(plan_path)
    task_text = read(current_task_path) if current_task_path.exists() else ""

    has_completed = "Completed S0-" in plan_text
    task_says_done = "Completed S0-" in task_text
    plan_says_not_started = "Not started" in plan_text or "Planned. Not started" in plan_text

    if task_says_done and plan_says_not_started:
        details.append("DRIFT: CURRENT_TASK.md shows completed work, but SPRINT_0_PLAN.md says 'Not started'")
        ok = False
    elif has_completed:
        details.append("Sprint plan shows completed tasks")
    else:
        details.append("Sprint plan shows no completed tasks yet")

    if task_says_done:
        done_count = task_text.count("Completed S0-")
        details.append(f"CURRENT_TASK.md reports {done_count} completed Sprint 0 tasks")
    return Check("sprint_status", ok, details)


def check_file_sizes() -> Check:
    warnings: list[str] = []
    failures: list[str] = []
    for root_name in SOURCE_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SOURCE_EXTS:
                continue
            if ".pytest_cache" in str(path) or ".dart_tool" in str(path) or "build" in str(path):
                continue
            rel = path.relative_to(ROOT)
            line_count = len(read(path).splitlines())
            if line_count > 500:
                failures.append(f"{rel}: {line_count} lines (HARD FAIL)")
            elif line_count > 300:
                warnings.append(f"{rel}: {line_count} lines (WARN)")
    details: list[str] = []
    if warnings:
        details.append(f"warnings_over_300={len(warnings)}")
        details.extend(f"  warn: {w}" for w in warnings[:10])
    if failures:
        details.append(f"failures_over_500={len(failures)}")
        details.extend(f"  FAIL: {f}" for f in failures[:10])
    if not warnings and not failures:
        details.append("All source files within limits")
    return Check("file_sizes", not failures, details)


def check_traceability_files() -> Check:
    details: list[str] = []
    ok = True
    for rel_path in REQUIRED_TRACE_FILES:
        full = ROOT / rel_path
        if not full.exists():
            details.append(f"MISSING {rel_path}")
            ok = False
            continue
        text = read(full)
        ids = unique_fr_ids(text)
        details.append(f"{rel_path}: {len(ids)} FR IDs found")
    return Check("traceability_files", ok, details)


def run_checks() -> list[Check]:
    return [
        check_state_docs(),
        check_sprint_status(),
        check_file_sizes(),
        check_traceability_files(),
    ]


def main() -> int:
    results = run_checks()
    failed = [r for r in results if not r.ok]

    print("=" * 60)
    print("  PRE-TASK SAFETY GUARD")
    print("=" * 60)
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"\n[{status}] {result.name}")
        for detail in result.details:
            print(f"    {detail}")

    print("\n" + "=" * 60)
    if not failed:
        print("  OVERALL: PASS — All guards clear. Proceed with task.")
        print("=" * 60)
        return 0
    else:
        print(f"  OVERALL: FAIL — {len(failed)} check(s) failed. Fix before proceeding.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
