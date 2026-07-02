# S2-001: Core DB Models + Alembic

## Goal

Add SQLAlchemy 2.0 model classes, Alembic configuration, and the initial migration for Sprint 1's tables.

## Requirements

- `NFR-MAINT-002`
- `NFR-SEC-003`

## Owned Files

- `services/api/src/infrastructure/database/`
- `services/api/alembic/`
- `services/api/requirements.txt`

## Forbidden Files

- real cloud database provisioning.
- social tables.
- production secrets.

## Tables To Model (first migration slice)

1. `users` — canonical account
2. `media_assets` — replaces UploadIntentStore
3. `media_derivatives` — replaces DerivativeService
4. `submissions` — replaces SubmissionStore
5. `submission_attributes` — user context
6. `capture_locations` — private coordinates
7. `score_events` — immutable ledger
8. `audit_logs` — append-only audit
9. `idempotency_keys` — mutation guard
10. `public_location_cells` — derived cell records

## Acceptance Criteria

- 10+ SQLAlchemy model classes defined with proper types, constraints, indexes.
- Alembic `env.py` configured for async PostgreSQL.
- `alembic revision --autogenerate` produces a migration creating all tables.
- Migration can be applied and rolled back.
- Database session dependency exists for FastAPI.

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `feat(db): add sqlalchemy models + alembic`.

## Commit Target

`feat(db): add sqlalchemy models + alembic`
