# Sprint 8 Plan: CI Expansion

## Sprint Goal

Add type checking (mypy) and linting (ruff) to the CI workflow. Fix existing lint/type issues in the codebase.

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- Existing CI workflow: 5 parallel jobs (docs, api-tests, worker-tests, scoring-rules-tests, flutter-tests)
- No linting or type checking configured
- All 95 tests passing

## In Scope

- Add ruff config and fix all existing lint issues
- Add mypy config and fix all existing type issues
- Add ruff-check + mypy-check jobs to CI workflow

## Out Of Scope

- Adding sqlalchemy2-stubs or migrating to SQLAlchemy 2.0 Mapped types (would resolve all model type errors but is a larger refactor)
- Ruff format enforcement (format style is a future concern)
- Security scanning expansion

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S8-001 | ✅ DONE | Ruf config + linting fixes | ruff check --fix passes clean on src/ and tests/ | ruff check returns 0 errors |
| S8-002 | ✅ DONE | Mypy config + type fixes | mypy passes clean on src/main.py | mypy returns 0 errors |
| S8-003 | ✅ DONE | CI workflow update | CI has ruff-check and mypy-check jobs | workflow YAML valid |

## File Ownership

| Area | Owner |
|---|---|
| `services/api/pyproject.toml` | Backend agent |
| `.github/workflows/docs-validation.yml` | Lead agent |

## Security

- No new dependencies beyond ruff/mypy in CI
- No secrets exposed
