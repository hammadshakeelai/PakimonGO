# S0-009: Add CI Validation Checks

## Goal

Add non-deploy CI or documented validation commands for docs, OpenAPI, privacy checks, and scaffold tests.

## Requirements

- `NFR-MAINT-003`
- `NFR-SEC-005`
- `NFR-OBS-001`

## Owned Files

- `.github/workflows/`
- `tools/qa/`
- `README.md`

## Forbidden Files

- production deploy credentials.
- cloud deployment workflow.
- release signing keys.

## Acceptance Criteria

- CI does not deploy.
- CI does not require secrets.
- CI runs or documents `python tools/qa/validate_docs.py`.
- Future Flutter/backend test commands are present only when toolchains exist.

## Verification

```powershell
python tools/qa/validate_docs.py
git status --short
```

## Rollback

Revert `ci: add scaffold validation checks`.

## Commit Target

`ci: add scaffold validation checks`
