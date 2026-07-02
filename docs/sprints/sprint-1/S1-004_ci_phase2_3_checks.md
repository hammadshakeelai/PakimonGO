# S1-004: Extend CI With Phase 2/3 Checks

## Goal

Add any new test categories discovered during Sprint 1 to the CI workflow. Wire Ollama-based Flutter test runner if local tooling supports it; otherwise document commands.

## Requirements

- `NFR-MAINT-003`

## Owned Files

- `.github/workflows/`
- `services/api/tests/`
- `tools/qa/`

## Forbidden Files

- deploy secrets.
- cloud deployment workflow.

## Acceptance Criteria

- CI runs or documents any new test categories (submission API, upload validation).
- CI remains non-deploy and secret-free.
- New tests from S1-001 through S1-003 are included in the `api-tests` job.

## Verification

```powershell
python tools/qa/validate_docs.py
git status --short
```

## Rollback

Revert `ci: add phase 2/3 checks`.

## Commit Target

`ci: add phase 2/3 checks`
