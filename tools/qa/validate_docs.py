"""Validate PakimonGO planning docs before code changes.

This script is intentionally dependency-light and safe to run locally. It checks
traceability, OpenAPI parseability, local Markdown links, Mermaid diagram files,
and future source-file size limits.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
FR_RE = re.compile(r"(?<![A-Z])FR-[A-Z]+-\d{3}")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"\[\[([^|\]]+)(?:\|[^\]]+)?\]\]")
SOURCE_EXTS = {".py", ".dart", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".kt"}
SOURCE_ROOTS = ("apps", "services", "packages", "tools")


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: list[str]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unique_matches(pattern: re.Pattern[str], text: str) -> set[str]:
    return set(pattern.findall(text))


def check_traceability() -> CheckResult:
    req_path = ROOT / "docs" / "REQUIREMENTS.md"
    trace_path = ROOT / "docs" / "TRACEABILITY_MATRIX.md"
    req_ids = unique_matches(FR_RE, read(req_path))
    trace_ids = unique_matches(FR_RE, read(trace_path))
    missing = sorted(req_ids - trace_ids)
    extra = sorted(trace_ids - req_ids)
    details = [
        f"functional_requirements={len(req_ids)}",
        f"traceability_ids={len(trace_ids)}",
        f"missing={len(missing)}",
        f"extra={len(extra)}",
    ]
    details.extend(f"missing: {item}" for item in missing[:20])
    details.extend(f"extra: {item}" for item in extra[:20])
    return CheckResult("traceability", not missing, details)


def check_openapi() -> CheckResult:
    path = ROOT / "docs" / "api" / "OPENAPI_DRAFT.yaml"
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        return CheckResult("openapi", False, [f"PyYAML unavailable: {exc}"])

    try:
        data = yaml.safe_load(read(path))
    except Exception as exc:
        return CheckResult("openapi", False, [f"YAML parse failed: {exc}"])

    details = [
        f"openapi={data.get('openapi')}",
        f"paths={len(data.get('paths', {}))}",
        f"schemas={len(data.get('components', {}).get('schemas', {}))}",
    ]
    required = ["openapi", "info", "paths", "components"]
    missing = [key for key in required if key not in data]
    details.extend(f"missing section: {key}" for key in missing)
    return CheckResult("openapi", not missing, details)


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0]


def is_external(target: str) -> bool:
    lower = target.lower()
    return (
        lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("#")
        or lower.startswith("tel:")
    )


def resolve_markdown_link(source: Path, target: str) -> Path | None:
    clean = unquote(strip_anchor(target).strip())
    if not clean or is_external(clean):
        return None
    if clean.startswith("<") and clean.endswith(">"):
        clean = clean[1:-1]
    candidate = Path(clean)
    if not candidate.is_absolute():
        candidate = source.parent / candidate
    return candidate.resolve()


def wiki_candidates(source: Path, target: str) -> list[Path]:
    clean = target.strip()
    if not clean:
        return []
    base = source.parent / clean
    candidates = [base, base.with_suffix(".md")]
    repo_base = ROOT / clean
    candidates.extend([repo_base, repo_base.with_suffix(".md")])
    return [item.resolve() for item in candidates]


def check_markdown_links() -> CheckResult:
    broken: list[str] = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        text = read(path)
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1).strip()
            resolved = resolve_markdown_link(path, target)
            if resolved and not resolved.exists():
                rel = path.relative_to(ROOT)
                broken.append(f"{rel}: missing link {target}")
        for match in WIKI_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not any(candidate.exists() for candidate in wiki_candidates(path, target)):
                rel = path.relative_to(ROOT)
                broken.append(f"{rel}: missing wiki link [[{target}]]")
    details = [f"broken_links={len(broken)}"]
    details.extend(broken[:50])
    return CheckResult("markdown_links", not broken, details)


def check_mermaid_diagrams() -> CheckResult:
    diagram_dir = ROOT / "docs" / "diagrams"
    missing: list[str] = []
    files = [path for path in diagram_dir.glob("*.md") if path.name != "README.md"]
    for path in files:
        if "```mermaid" not in read(path):
            missing.append(str(path.relative_to(ROOT)))
    return CheckResult(
        "mermaid_diagrams",
        not missing,
        [f"diagram_files={len(files)}", f"missing_mermaid={len(missing)}", *missing],
    )


def check_file_sizes() -> CheckResult:
    warnings: list[str] = []
    hard_failures: list[str] = []
    for root_name in SOURCE_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SOURCE_EXTS:
                continue
            rel = path.relative_to(ROOT)
            line_count = len(read(path).splitlines())
            if line_count > 500:
                hard_failures.append(f"{rel}: {line_count} lines")
            elif line_count > 300:
                warnings.append(f"{rel}: {line_count} lines")
    details = [
        f"warnings_over_300={len(warnings)}",
        f"failures_over_500={len(hard_failures)}",
    ]
    details.extend(f"warn: {item}" for item in warnings[:20])
    details.extend(f"fail: {item}" for item in hard_failures[:20])
    return CheckResult("file_sizes", not hard_failures, details)


def run_checks() -> list[CheckResult]:
    return [
        check_traceability(),
        check_openapi(),
        check_markdown_links(),
        check_mermaid_diagrams(),
        check_file_sizes(),
    ]


def main() -> int:
    results = run_checks()
    failed = [result for result in results if not result.ok]
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.name}")
        for detail in result.details:
            print(f"  {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
