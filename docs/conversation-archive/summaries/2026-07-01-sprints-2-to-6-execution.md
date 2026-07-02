# Sprints 2-6 Execution: DB, Auth, Upload, Users, Precheck

## Date
2026-07-01

## Summary
Executed Sprints 2 through 6 in sequence: DB-backed repositories, auth integration, real file upload, user profiles, and duplicate/zoo precheck.

## Key Decisions
- S2-002: DB-backed repositories use `Depends(get_db)` with sync sessions. SQLite temp file for tests (shared file path, not `:memory:`). conftest sets `SYNC_DATABASE_URL` + `UPLOAD_BASE`.
- S3: Auth adapter pattern (ADR-006) — `FakeAuthAdapter` validates `test_token_valid` and `test_user_{id}` tokens.
- S4: Two-step upload flow (intent→PUT file→complete). Multipart via `UploadFile`. Derivative generation falls back to file copy if PIL fails.
- S5: User rows auto-created on first `GET /v1/users/me`. No separate registration endpoint.
- S6: Precheck is pure function in `scoring-rules` package (no DB dependency). API layer collects SHA256s and calls it. Duplicate exclusion uses `exclude_media_asset_id`.

## Files Changed
- `services/api/src/infrastructure/database/repositories.py` — all DB-backed operations
- `services/api/src/infrastructure/database/session.py` — SQLite support via `check_same_thread`
- `services/api/src/infrastructure/auth/` — adapter.py, fake_adapter.py, dependencies.py
- `services/api/src/infrastructure/storage/local_storage.py` — LocalFileStorage with PIL
- `services/api/src/modules/media/api/routes.py` — auth-protected media endpoints + upload + file serving
- `services/api/src/modules/submissions/api/routes.py` — auth-protected submissions + precheck
- `services/api/src/modules/users/api/routes.py` — GET/PATCH /v1/users/me
- `services/api/src/main.py` — app factory with all routers
- `services/api/tests/conftest.py` — SQLite temp DB + upload temp dir
- `packages/scoring-rules/src/precheck.py` — run_precheck() pure function
- `packages/scoring-rules/tests/test_precheck.py` — 8 precheck tests
- `services/api/tests/test_submission.py` — 7 tests (wild→ai_evaluated, zoo→capped, duplicate→capped)
- `services/api/tests/test_user.py` — 5 user profile tests
- `services/api/tests/test_media_upload.py` — roundtrip test, auth test
- Removed: `upload_intent.py`, `derivative.py`, `submission.py` (domain files, replaced by DB)

## Test Counts
- 54 API tests
- 1 worker test
- 26 scoring-rules tests
- 14 Flutter tests
- **95 total, all passing**

## Next Steps
Sprint 7 — OpenAPI draft update, CI expansion, or real scoring AI pipeline stub.
