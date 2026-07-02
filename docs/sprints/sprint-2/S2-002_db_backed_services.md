# S2-002: Wire DB Into Services

## Goal

Replace in-memory stores in media and submission modules with database-backed services using SQLAlchemy sessions.

## Requirements

- `FR-CAP-011`
- `FR-CAP-012`
- `NFR-SEC-001`

## Owned Files

- `services/api/src/modules/media/`
- `services/api/src/modules/submissions/`
- `services/api/tests/`

## Forbidden Files

- final scoring formula.
- real cloud storage.

## Acceptance Criteria

- `UploadIntentStore` creates and reads from database.
- `SubmissionStore` creates and reads submissions from database.
- `DerivativeService` reads derivative records from database.
- Tests use in-memory SQLite or rolled-back transactions.
- All 45+ existing tests pass.

## Verification

```powershell
python -m pytest services/api/tests
```

## Rollback

Revert `feat(media): migrate to db-backed services`.

## Commit Target

`feat(media): migrate to db-backed services`
