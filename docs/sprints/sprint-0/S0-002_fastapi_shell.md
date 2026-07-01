# S0-002: Scaffold FastAPI API Shell

## Goal

Create a minimal FastAPI API shell with health endpoints and module package structure.

## Requirements

- `NFR-SEC-002`
- `NFR-OBS-001`
- `NFR-MAINT-002`
- `NFR-PORT-002`

## Owned Files

- `services/api/`
- `services/api/src/`
- `services/api/tests/`

## Forbidden Files

- `apps/mobile/`
- final scoring formula
- real provider credentials

## Acceptance Criteria

- API app imports successfully.
- `/health/live` and `/health/ready` exist.
- Test harness exists.
- Health endpoints reveal no secrets.

## Verification

```powershell
python --version
python -m pytest services/api/tests
```

If dependencies are not installed yet, document exact setup blocker.

## Rollback

Revert `scaffold(api): add fastapi shell`.

## Commit Target

`scaffold(api): add fastapi shell`
