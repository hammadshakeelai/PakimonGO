# Commit Policy

## Purpose

PakimonGO should move in short, reviewable bursts so humans and AI agents can understand exactly what changed, why it changed, and who changed it.

## Short-Burst Rule

Prefer small semantic commits after each coherent unit of work:

- planning doc update
- scaffold folder/package addition
- one module skeleton
- one API contract group
- one domain rule plus tests
- one bug fix plus regression test

Avoid giant mixed commits. If a change touches multiple domains, split it by intent unless the files must land together to keep the repo working.

## Commit Message Format

Use concise semantic subjects:

```txt
docs(process): add short-burst commit policy
scaffold(api): add submissions module shell
test(scoring): cover zoo score cap
fix(upload): make completion idempotent
```

Recommended types:

- `docs`
- `scaffold`
- `feat`
- `fix`
- `test`
- `refactor`
- `chore`
- `security`
- `perf`

## Required Commit Body For AI Work

Every AI-authored commit should include trailers:

```txt
AI-Agent: Codex GPT-5
AI-Work-Mode: autonomous|pairing|review
AI-Commit-Time: 2026-07-01T04:10:00+05:00
Work-Package: WP-001
Requirements: FR-CAP-011, NFR-SEC-001
Process-Docs-Updated: yes
```

Use local ISO 8601 time with timezone. If the exact model/surface changes, name it plainly.

## Before Commit Checklist

- Work package or task state is clear.
- Changes are scoped to one semantic purpose.
- Requirement IDs are referenced where useful.
- Tests or verification were run, or the reason is recorded.
- `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`, backlog, risk, or debt docs are updated if the task changed them.
- No secrets, private photos, exact locations, or generated build artifacts are staged.

## Commit Cadence

During implementation, commit after each stable mini-milestone. Examples:

- after adding a module README and empty contract shell
- after adding a domain model plus tests
- after wiring one endpoint and contract test
- after fixing one failing test

Do not commit broken code unless the commit is intentionally marked as a WIP checkpoint on a private branch and the next task explains the recovery path.
