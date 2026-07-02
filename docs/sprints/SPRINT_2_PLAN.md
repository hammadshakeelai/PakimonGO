# Sprint 2 Plan: Database Models And Alembic Setup

## Sprint Goal

Replace Sprint 1's in-memory stores with SQLAlchemy models and Alembic migrations against local PostgreSQL, then wire existing endpoints to DB-backed services.

## Sprint Status

**Complete.** Both tasks done and verified.

## Sprint Inputs

- Sprint 1 complete: upload intent, submission DTO, derivative stubs — all in-memory
- Data dictionary: `docs/data/DATA_DICTIONARY.md` (143 columns across 43 tables)
- ERD: `docs/data/DATABASE_ERD.md`
- First migration slice defined (7 groups)
- Docker compose: `infrastructure/docker/docker-compose.local.yml` (pgvector)

## In Scope

- SQLAlchemy 2.0 model classes for first migration slice tables
- Alembic configuration + initial migration
- Database session dependency for FastAPI
- Migration of UploadIntentStore to DB-backed media_assets
- Migration of SubmissionStore to DB-backed submissions + submission_attributes
- Migration of DerivativeService to DB-backed media_derivatives
- Tests use in-memory SQLite or test transactions

## Out Of Scope

- Real cloud database provisioning
- Social tables (posts, comments, likes, etc.)
- Full user auth integration (user_id is a placeholder for now)
- Production deployment
- Real PostGIS geography columns (use text/json fallback until PostGIS is verified)

## Sprint Backlog

| ID | Status | Task | Owned Paths | Forbidden Paths | Acceptance | Verification |
|---|---|---|---|---|---|---|
| S2-001 | ✅ DONE | Core DB models + Alembic | `services/api/src/infrastructure/database/`, `services/api/alembic/` | real cloud DB, social tables | 10+ model classes, Alembic config, migration creates tables | all 45 tests pass |
| S2-002 | ✅ DONE | Wire DB into services | `services/api/src/modules/media/`, `services/api/src/modules/submissions/` | real cloud storage | UploadIntentStore, SubmissionStore, DerivativeService use DB | all 45+ tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/src/infrastructure/database/` | Backend agent | SQLAlchemy models, session, Alembic |
| `services/api/src/modules/media/` | Backend agent | DB-backed upload + derivative |
| `services/api/src/modules/submissions/` | Backend agent | DB-backed submission |

## Commit Sequence

1. ✅ `feat(db): add sqlalchemy models + alembic`
2. ✅ `feat(media): migrate to db-backed services`

## Acceptance Criteria

- 10+ SQLAlchemy model classes covering users, media_assets, submissions, capture_locations, score_events, etc.
- Alembic initial migration creates all Sprint 1 tables
- Upload intent creates/reads from database
- Submission creates/reads from database
- Derivative reads from database
- All tests pass (test DB isolation via transactions)
- Docker Compose pgvector is used for local testing

## Security And Privacy Notes

- Restricted columns (exact coordinates, originals) remain never-public
- Migration scripts must not contain secrets
- Database URLs use env vars only

## Rollback

- Alembic `downgrade -1` reverts migration
- Revert the affected commit

## Definition Of Done

- All Sprint 2 tasks complete or explicitly blocked
- Commands/tests run recorded
- State docs updated
