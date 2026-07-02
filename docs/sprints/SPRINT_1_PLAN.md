# Sprint 1 Plan: WP-015 Alpha-0 Private Capture Slice

## Sprint Goal

Build the backend capture pipeline — upload intent, media validation, submission private DTO, and derivative processing — without real cloud storage, AI scoring, or public/social features. Extends Sprint 0's scaffold with working HTTP endpoints and unit tests.

## Sprint Status

Complete. All 4 tasks finished.

## Sprint Inputs

- Sprint 0 complete: Flutter shell, FastAPI shell, worker shell, score state model, capture draft model, CI workflow
- ADRs: 13 accepted, 1 revised (ADR-009), 2 deferred (ADR-003 map provider, ADR-015 production deployment)
- Contract draft: `docs/api/OPENAPI_DRAFT.yaml` (13 paths, 22 schemas)
- Data dictionary: `docs/data/DATA_DICTIONARY.md`
- Existing tests: 59 total (26 API + 1 worker + 18 scoring-rules + 14 Flutter)

## In Scope

- Upload intent creation and completion endpoints (signed URL placeholder, no real cloud storage).
- Media file validation (size, type, hash verification).
- Submission private DTO with scoring-state hook.
- Media derivative pipeline (thumbnail URL placeholder, EXIF stripping contract, no real image processing).
- CI extension for any new test categories.

## Out Of Scope

- Real cloud storage integration.
- AI scoring or AI provider calls.
- Public feed, social features, leaderboards.
- Map provider SDK integration.
- Real camera plugin flow (capture draft model already exists).
- Database migrations or real persistence (in-memory services only).
- Real image processing (derivative stubs only).
- Production deployment or secrets.

## Sprint Backlog

| ID | Status | Task | Owned Paths | Forbidden Paths | Acceptance | Verification |
|---|---|---|---|---|---|---|
| S1-001 | ✅ DONE | Upload intent + media validation | `services/api/src/modules/media/` | real cloud storage, AI calls | POST `/v1/media/upload-intent` + POST `/v1/media/complete-upload` exist; media validated; tests pass | 45 API tests pass |
| S1-002 | ✅ DONE | Submission private DTO | `services/api/src/modules/submissions/` | public DTO exposure, final scoring | POST `/v1/submissions` creates pending submission; privacy-safe response; score state hook exists | 45 API tests pass |
| S1-003 | ✅ DONE | Media derivative pipeline | `services/api/src/modules/media/` | real image processing libs, cloud storage | derivative stubs for thumbnail URL + EXIF strip contract; no real pixel ops | 45 API tests pass |
| S1-004 | ✅ DONE | Extend CI with Phase 2/3 checks | `.github/workflows/` | deploy secrets | new test categories wired as non-deploy checks | CI auto-runs all 45 tests |

## File Ownership

| Area | Owner Type | Notes |
|---|---|---|
| `services/api/src/modules/media/` | Backend agent | Upload, validation, derivative endpoints |
| `services/api/src/modules/submissions/` | Backend agent | Submission DTO, scoring state hook |
| `.github/workflows/` | DevOps agent | CI extension |
| `docs/` | Lead agent | State and traceability updates |

## Commit Sequence

1. ✅ `feat(media): add upload intent + validation`
2. ✅ `feat(submissions): add private submission dto`
3. ✅ `feat(media): add derivative stubs`
4. ✅ `ci: add phase 2/3 checks`

## Acceptance Criteria

- Upload intent endpoint exists and validates file metadata.
- Media completion endpoint verifies hash and transitions draft to ready.
- Submission endpoint creates pending submission with privacy-safe response.
- Derivative endpoint stubs exist without real cloud/image processing.
- All tests pass; no secrets introduced.
- State docs updated before sprint close.

## Security And Privacy Notes

- Use signed URL placeholders only — no real storage credentials.
- Submission response must not leak exact coordinates or original URLs.
- EXIF stripping must be contractually required before public derivatives.
- Keep server-authority invariant: client cannot finalize score state.

## Rollback Plan

- Revert the affected short-burst commit for each task.
- In-memory services lose no data; no migration rollback needed.

## Definition Of Done

- All Sprint 1 tasks complete or explicitly blocked.
- Commands/tests run are recorded.
- State docs updated.
- Commit sequence matches plan with AI attribution trailers.
