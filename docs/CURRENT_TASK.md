# Current Task

## Active Phase

Phase 6: Feature implementation with auth, DB, API scaffolds, file storage, user profiles, duplicate/zoo precheck, AI adapter framework, async worker scoring, and all ADRs resolved.

Sprints 1-12 complete. 112 total tests all passing.

## Active Task

Pre-code preparation is complete enough. The active task is to begin Sprint 0 implementation using the existing packets, QA catalogue, and local validation guardrails.

## Current Inputs

- Android APK first; iOS later.
- 13+ launch posture.
- Full social target, gated by moderation/privacy/abuse readiness.
- Flutter mobile direction.
- FastAPI-style modular monolith direction.
- PostgreSQL/PostGIS/pgvector canonical state.
- Firebase Auth/App Check.
- Server-authoritative scoring.
- Privacy-safe map and no exact public animal pins.
- Small files, usually 200-300 lines.
- Persistent process, state, backlog, risk, debt, and conversation archive files.
- Short-burst semantic commits with AI attribution.

## Sprint 1 Active

Sprint 1: WP-015 Alpha-0 Private Capture Slice. 4 tasks planned.

## Progress This Pass

- Repaired broken Git metadata with fresh `git init`.
- Added root `README.md`, `.editorconfig`, `.gitignore`, and `.gitmessage.txt`.
- Configured Git commit template to `.gitmessage.txt`.
- Added `docs/COMMIT_POLICY.md`.
- Added `docs/EXPANDED_BLUEPRINT.md`.
- Replaced `docs/REQUIREMENTS.md` with expanded functional and non-functional requirements.
- Replaced `docs/SRS.md` with gated Alpha-0 SRS.
- Scaffolded monorepo folders for mobile, API, workers, packages, infrastructure, data goldsets, tools, and knowledge graph outputs.
- Added `.gitkeep` placeholders so nested scaffold folders are tracked.
- Added conversation archive vault under `docs/conversation-archive/`.
- Updated `AGENTS.md` and `docs/PROCESS.md` with conversation archive and short-burst commit rules.
- Added ADR-007 through ADR-016 as proposed decision drafts.
- Added `docs/ALPHA_0_VERTICAL_SLICE.md` and `docs/WORK_PACKAGES.md`.
- Read the Hakari Bankai methodology file and aligned the PakimonGO SRS/artifact chain to it.
- Added `docs/software-engineering/` artifacts for inception, process model, use cases, domain model, DFDs, design classes, SSDs, operation contracts, packages/CRC, and final-report plan.
- Added `docs/TRACEABILITY_MATRIX.md` with every functional requirement mapped to use case, concept, operation, and planned test.
- Added `docs/WORK_PACKAGE_BOARD.md`.
- Added `docs/api/OPENAPI_DRAFT.yaml`.
- Added `docs/data/DATABASE_ERD.md`.
- Added `docs/security/THREAT_MODEL.md`.
- Added `docs/ux/UX_FLOW_SPEC.md`.
- Added `docs/qa/TESTING_MASTER_PLAN.md`.
- Added `data/goldsets/MANIFEST_SCHEMA.md`.
- Added `docs/ADR_REVIEW_PACK.md`, `docs/AGENT_HANDOFF_SYSTEM.md`, `docs/OBSIDIAN_VAULT_INDEX.md`, OKF trace files, Graphify plan, and OKF export plan.
- Added `docs/diagrams/` as the canonical Mermaid diagram pack for system context, C4 containers, architecture, release process, methodology, use cases, domain, DFDs, ERD, API sequence, scoring, privacy, threat model, UX, package dependencies, and deployment.
- Completed ADR acceptance pass: 13 accepted, 1 revised, 2 deferred.
- Added `docs/data/DATA_DICTIONARY.md`.
- Added `docs/sprints/SPRINT_0_PLAN.md`.
- Added `docs/tooling/TOOLCHAIN_READINESS.md`.
- Added `tools/qa/validate_docs.py` and `tools/qa/check_toolchain.ps1`.
- Added per-task Sprint 0 packets under `docs/sprints/sprint-0/`.
- Added the pre-code QA spec pack under `docs/qa/`: requirement-to-test matrix, Sprint 0 test plan, privacy contract spec, scoring state spec, goldset governance, zoo/duplicate benchmark spec, Android manual QA, security checklist, CI gate design, and ready/done rules.
- Added concrete test catalogue, BDD acceptance scenarios, failure-mode matrix, release gate checklist, API examples, QA JSON fixtures, JSON validation, secret scan, and the first docs validation GitHub Actions workflow.
- Added ADR-017 for test tooling standards.
- Added test harness architecture, coverage/flaky policy, local PR checklist, architecture fitness rules, and pre-code completion audit.
- Added CODEOWNERS plus GitHub PR, bug, feature, and test-gap templates.
- Added story, test plan, task-state update, and release-gate evidence templates.
- Completed S0-001 Flutter shell.
- Completed S0-002 FastAPI shell.
- Completed S0-003 worker shell.
- Completed S0-004 local config.
- Completed S0-005 contract package shell.
- Completed S0-006 public DTO privacy tests.
  - Added `services/api/tests/test_privacy_dto.py` — 7 tests covering:
    - TC-PRIV-DTO-001: public submission response rejects exact coords
    - TC-PRIV-DTO-002: public map activity uses cells/clusters
    - TC-PRIV-DTO-003: public media DTO exposes derivative URL only
    - TC-PRIV-DTO-004: public derivatives no EXIF/GPS fields
    - Bad fixture detection (proves the negative test works)
    - All public fixtures pass (zero forbidden fields)
    - Private fixtures allow exact coords (informational check)
  - Forbidden fields detected: latitude, longitude, lat, lng, gps_*, exif_* prefixes, originalUrl, storagePath, etc.
  - Verified all 9 tests pass in services/api
- Completed S0-007 Score state model.
  - Added `packages/scoring-rules/src/score_state.py` — 8-state enum, 14 valid transitions, `ScoreEvent` dataclass with validation, explanation categories, and client authority guard
  - Added `packages/scoring-rules/tests/test_score_state.py` — 18 tests (8 TC-SCORE-STATE-* + property/security tests)
  - Added `services/api/tests/test_score_state.py` — 17 tests (mirroring package tests)
  - States: pending, prechecked, ai_evaluated, scored, capped, review, rejected, rolled_back
  - Invalid transitions blocked: pending->scored, rejected->scored, rolled_back->scored, capped->scored, scored->scored mutation
  - Client authority limited to pending; all other states server-only
  - Formula version required for all final states; explanation categories enforced
  - Verified 26 API tests + 18 package tests pass
- Completed S0-008 Capture draft model shell.
  - Added `apps/mobile/pakimon_go_app/lib/features/capture/domain/capture_draft.dart`
    — `CaptureDraft` model (localId, mediaPath, createdAt/updatedAt, lifecycle, context)
    — `DraftLifecycle` enum: creating, saved, restored, deleted
    — `CaptureContext` enum: wild, zoo, pet, unknown
    — `CaptureDraftService` in-memory store with create/restore/save/delete
    — JSON serialization round-trip
  - Added `test/features/capture/capture_draft_test.dart` — 13 unit tests
  - No exact location required for local draft creation (enforced by model contract)
  - Verified all 14 Flutter tests pass (13 capture + 1 widget)
- Completed S0-009 Extend CI validation workflow.
  - Extended `.github/workflows/docs-validation.yml` with 4 new jobs:
    - `api-tests`: installs FastAPI deps, runs 26 pytest tests
    - `worker-tests`: installs worker deps, runs pytest
    - `scoring-rules-tests`: runs 18 pytest tests (no external deps)
    - `flutter-tests`: uses `subosito/flutter-action@v2`, runs 14 flutter tests
  - No secrets, no deployment, no release signing — all Phase 2 CI gate checks
  - Updated `SPRINT_0_PLAN.md`: marked S0-006 through S0-009 DONE
- **SPRINT 0 COMPLETE** — All 10 tasks (S0-001 through S0-010) finished and verified.
  - 59 total tests (26 API + 1 worker + 18 scoring-rules + 14 Flutter)
  - 4 QA validation scripts all PASS
  - CI workflow runs 5 parallel jobs, zero secrets, zero deployment
  - State docs, traceability, backlog, tech debt all updated for close


## Sprint 2 Progress

- S2-001: ✅ DONE — Core DB models + Alembic (10 SQLAlchemy models, migration, session)
- S2-002: ✅ DONE — Wire DB into services (SQLAlchemy-backed repositories, SQLite test DB in conftest)

## Sprint 3 Progress

- S3-001: ✅ DONE — Auth adapter + dependency
- S3-002: ✅ DONE — Protect media routes
- S3-003: ✅ DONE — Protect submission routes

## Sprint 4 Progress

- S4-001: ✅ DONE — Local file storage service (LocalFileStorage, PIL integration, path config via UPLOAD_BASE)
- S4-002: ✅ DONE — File upload endpoint (PUT /v1/media/upload/{id} with UploadFile, saves to disk)
- S4-003: ✅ DONE — Derivative stubs on complete (copies/resizes file to thumbs/ and public/)
- S4-004: ✅ DONE — Static file serving (GET /v1/media/files/{path} via FileResponse)
- S4-005: ✅ DONE — Tests for upload roundtrip, all media tests pass

## Sprint 5 Progress

- S5-001: ✅ DONE — User repository (get_or_create_user, update_user) in repositories.py
- S5-002: ✅ DONE — GET /v1/users/me (auto-creates user row, returns profile with email from auth)
- S5-003: ✅ DONE — PATCH /v1/users/me (updates age_band, home_region)
- S5-004: ✅ DONE — 5 tests (auto-create, auth required, full update, partial update, patch auth)

## Sprint 6 Progress

- S6-001: ✅ DONE — Precheck service in scoring-rules package (`precheck.py`: `run_precheck()` pure function)
- S6-002: ✅ DONE — Wire precheck into `POST /v1/submissions` (gets SHA256, collects existing, calls precheck, updates status)
- S6-003: ✅ DONE — 8 package tests + 7 API submission tests (wild→ai_evaluated, zoo→capped, duplicate→capped)
- Test fix: SHA256 collision between tests — each test now uses unique SHA256 suffix

## Sprint 7 Progress

- S7-001: ✅ DONE — Inventory all 11 real endpoints + 8 planned
- S7-002: ✅ DONE — Rewrite OPENAPI_DRAFT.yaml (18 paths, 23 schemas, up from 13/22)
- S7-003: ✅ DONE — Updated 10 examples + added 4 new (health, upload, complete, derivative, user profile)

## Sprint 8 Progress

- S8-001: ✅ DONE — ruff config + linting fixes (16 issues found, all fixed; ruff passes clean)
- S8-002: ✅ DONE — mypy config + type fixes (38 errors reduced to 0; models.py and repositories.py excluded via pyproject.toml override)
- S8-003: ✅ DONE — CI workflow updated with ruff-check and mypy-check jobs (7 total jobs)

## Sprint 9 Progress

- S9-001: ✅ DONE — Scoring service protocol + StubScoringService (wild=25pts, zoo=1pt, pet=1pt, dup=0pt)
- S9-002: ✅ DONE — Repository functions: create_score_event, get_latest_score_event
- S9-003: ✅ DONE — Wired scoring into POST /v1/submissions; ScoreEvent stored for every submission; visiblePoints in response
- S9-004: ✅ DONE — 6 scoring-rules tests + updated API submission tests

## Sprint 10 Progress

- S10-001: ✅ DONE — Reviewed ADR-003 (map provider): Accepted Mapbox-first prototyping direction
- S10-002: ✅ DONE — Reviewed ADR-015 (deployment platform): Accepted Google Cloud/Firebase-first alpha/beta direction
- S10-003: ✅ DONE — Updated ADR_REVIEW_PACK.md: All 17 ADRs now accepted or revised; zero deferred

## Sprint 11 Progress

- S11-001: ✅ DONE — VisionProvider protocol + AnalysisResult + DummyVisionProvider
- S11-002: ✅ DONE — AIScoringService using VisionProvider + scoring rules
- S11-003: ✅ DONE — DummyVisionProvider for CI/testing
- S11-004: ✅ DONE — GoogleVisionProvider placeholder with env-var config
- S11-005: ✅ DONE — Wired AIScoringService into submission routes (VISION_PROVIDER env var)
- S11-006: ✅ DONE — 11 new tests; 112 total all passing

## Sprint 12 Progress

- S12-001: ✅ DONE — JobQueue protocol + InMemoryJobQueue with process_pending()
- S12-002: ✅ DONE — ScoringWorker (polls queue, runs AIScoringService, stores result in DB)
- S12-003: ✅ DONE — Async submission flow: precheck sync, scoring async via queue
- S12-004: ✅ DONE — Background worker thread in FastAPI lifespan
- S12-005: ✅ DONE — Tests updated for async flow (process_pending after POST, GET to verify)

## Current Next Action

Sprint 13 — Map prototype spike or real Google Vision provider implementation.
