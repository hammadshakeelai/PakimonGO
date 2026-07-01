"""Lightweight secret scan for planning and scaffold files.

This is not a replacement for a production secret scanner. It catches common
mistakes early: committed .env files, private key blocks, and suspicious
credential assignments with long non-placeholder values.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {
    ".git",
    ".dart_tool",
    ".idea",
    ".venv",
    "build",
    "node_modules",
    "__pycache__",
}
TEXT_EXTS = {
    ".env",
    ".example",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(api[_-]?key|secret|password|token|private[_-]?key|client[_-]?secret)"
    r"\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{24,})"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----")
PLACEHOLDER_PREFIXES = (
    "dummy",
    "example",
    "placeholder",
    "changeme",
    "your_",
    "replace_",
    "pakimongo_example",
    "signed-upload-placeholder",
)


@dataclass
class Finding:
    path: Path
    line: int
    reason: str


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)


def is_text_candidate(path: Path) -> bool:
    if path.name in {".env", ".env.example"}:
        return True
    return path.suffix.lower() in TEXT_EXTS


def is_placeholder(value: str) -> bool:
    clean = value.strip().strip("\"'").lower()
    return clean.startswith(PLACEHOLDER_PREFIXES) or "example" in clean


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if path.name == ".env":
        findings.append(Finding(path, 1, "committed .env file"))
        return findings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings

    for line_no, line in enumerate(text.splitlines(), start=1):
        if PRIVATE_KEY_RE.search(line):
            findings.append(Finding(path, line_no, "private key block"))
        match = SECRET_ASSIGNMENT_RE.search(line)
        if match and not is_placeholder(match.group(2)):
            findings.append(Finding(path, line_no, f"suspicious {match.group(1)} assignment"))
    return findings


def main() -> int:
    findings: list[Finding] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or is_skipped(path) or not is_text_candidate(path):
            continue
        findings.extend(scan_file(path))

    print("PASS secret_scan" if not findings else "FAIL secret_scan")
    print(f"  findings={len(findings)}")
    for finding in findings[:50]:
        rel = finding.path.relative_to(ROOT)
        print(f"  {rel}:{finding.line} {finding.reason}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
