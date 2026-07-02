# Current Task

## Active Phase

Phase 6: Feature implementation with auth, DB, API scaffolds, file storage, user profiles, duplicate/zoo precheck, AI adapter framework, async worker scoring, and map prototype.

Sprints 1-27 complete. 89 API tests all passing.

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

## Sprint 13 Progress

- S13-001: ✅ DONE — Added mapbox_maps_flutter dependency to pubspec.yaml
- S13-002: ✅ DONE — Created AppConfig with MAPBOX_ACCESS_TOKEN env var support
- S13-003: ✅ DONE — Created MapScreen with MapWidget (Mapbox map fallback message if no token)
- S13-004: ✅ DONE — Updated main.dart: PakimonGO app with MapScreen as home, MapboxOptions.setAccessToken on start
- S13-005: ✅ DONE — Updated widget tests for new app structure (14 Flutter tests pass)

## Sprint 22 Progress

- S22-001: ✅ DONE — Added /v1 prefix at app level; updated all module routes to remove internal v1 prefixes
- S22-002: ✅ DONE — Version negotiation via header + URL path
- S22-003: ✅ DONE — OpenAPI spec version info and v2 placeholder
- S22-004: ✅ DONE — Tests for version negotiation
- 75 API tests + 61 scoring-rules + 14 Flutter = **150 total tests, all passing**

## Sprint 24 Progress

- S24-001: ✅ DONE — Add cloud storage provider interface (StorageProvider, S3/GCS implementations)
- S24-002: ✅ DONE — Add environment configuration (.env.example updated with STORAGE_PROVIDER, S3/GCS vars)
- S24-003: ✅ DONE — Add storage tests (3 tests for URL format/env defaults)
- S24-004: ✅ DONE — Fix derivative URLs to use /v1/media/files prefix
- S24-005: ✅ DONE — State docs updated
- 78 API tests + 61 scoring-rules + 14 Flutter = **153 total tests**

## Sprint 23 Progress

- S23-001: ✅ DONE — Stage and commit all implementation files (Sprints 0-22 corpus)
- S23-002: ✅ DONE — Stage scoring-rules package files
- S23-003: ✅ DONE — Stage infrastructure files (auth, storage, queue, database, session)
- S23-004: ✅ DONE — Run full test suite validation (150 tests pass, all validations)
- S23-005: ✅ DONE — Updated state docs and TECH_DEBT

## Sprint 22 Progress

- S21-001: ✅ DONE — Updated GET /v1/users/me/collection with include_sensitive param
- S21-002: ✅ DONE — Updated GET /v1/leaderboard with include_sensitive param
- S21-003: ✅ DONE — Added GET /v1/submissions endpoint documentation with include_sensitive
- S21-004: ✅ DONE — Added PaginatedSubmissionListResponse schema
- OPENAPI_DRAFT.yaml: 20 paths, 31 schemas, fixed duplicate /submissions: path

## Sprint 20 Progress

- S20-001: ✅ DONE — `get_user_collection` excludes sensitive species by default, optional `include_sensitive` flag
- S20-002: ✅ DONE — `get_leaderboard` excludes sensitive species submissions, `include_sensitive` flag
- S20-003: ✅ DONE — `get_submissions` filters sensitive species, `include_sensitive` param (default false)
- S20-004: ✅ DONE — 6 new tests for collection/leaderboard sensitive species exclusion
- S20-005: (Pending) — OPENAPI_DRAFT.yaml update for include_sensitive params
- Refactored repositories into 7 modules (media_asset, submission, score_event, user, collection, submission_list, sensitive_species)
- 69 API tests + 61 scoring-rules + 14 Flutter = **144 total tests, all passing**

## Sprint 19 Progress

- S19-001: ✅ DONE — SensitiveSpecies model with scientific_name (unique), common_name, suppression_level, reason
- S19-002: ✅ DONE — `is_sensitive_species` and `get_or_create_sensitive_species` repository functions
- S19-003: ✅ DONE — `_build_submission_response` checks sensitivity and returns suppressed location (cell_suppressed, precisionLabel=suppressed)
- S19-004: ✅ DONE — `create_sensitive_species` and `get_or_create_sensitive_species` for seeding
- S19-005: ✅ DONE — 4 tests: detection, suppression, normal cell, create response
- S19-006: (Pending) — Update collection/leaderboard to handle sensitive species (optional)
- 65 API tests + 61 scoring-rules + 14 Flutter = **140 total tests, all passing**

## Sprint 18 Progress

- S18-001: ✅ DONE — Added Pagination, PaginatedCollectionResponse, PaginatedLeaderboardResponse, PaginatedSubmissionListResponse schemas
- S18-002: ✅ DONE — Updated GET /v1/users/me/collection with limit, offset, context, sort_by, sort_order params
- S18-003: ✅ DONE — Updated GET /v1/leaderboard with limit, offset, sort_by, sort_order params
- S18-004: ✅ DONE — Added GET /v1/submissions list endpoint with pagination, status filter, sorting
- S18-005: ✅ DONE — Added PaginatedSubmissionListResponse schema
- OPENAPI_DRAFT.yaml: 20 paths, 31 schemas (up from 27)

## Sprint 17 Progress

- S17-001: ✅ DONE — `GET /v1/users/me/collection` with pagination (limit/offset), filtering (context), sorting (totalPoints, species, captureCount, lastCaptured asc/desc)
- S17-002: ✅ DONE — `GET /v1/leaderboard` with pagination (limit/offset), sorting (totalScore, userId, submissionCount asc/desc)
- S17-003: ✅ DONE — `GET /v1/submissions` list endpoint with pagination, filtering (status, user_id), sorting (createdAt, submittedAt, status, points, species)
- S17-004: ✅ DONE — Repository functions updated: `get_user_collection`, `get_leaderboard`, `get_submissions` all return (items, total) tuples
- S17-005: ✅ DONE — Tests updated for pagination/filtering/sorting
- S17-006: (Pending) — OPENAPI_DRAFT.yaml update
- 61 API tests + 61 scoring-rules + 14 Flutter = **136 total tests, all passing**

## Sprint 16 Progress

- S16-001: ✅ DONE — duplicate-detection manifest.yaml (9 scenarios: exact dup, new SHA, empty set, null/empty current, dup overrides zoo/pet, zoo/pet without dup)
- S16-002: ✅ DONE — zoo-detection manifest.yaml (9 scenarios: zoo, pet, wild, unknown, empty/null context, case insensitivity, dup overrides zoo, zoo with existing unrelated SHA)
- S16-003: ✅ DONE — goldset_runner.py: load_manifest, validate_manifest, run_scenario, run_manifest, run_manifest_path
- S16-004: ✅ DONE — 12 goldset tests (manifest exists, load, run scenario pass/fail, full manifests pass, invalid manifests, path not found)
- S16-005: ✅ DONE — CI goldset-smoke job runs test_goldset_runner.py
- 73 scoring-rules tests + 61 API tests + 14 Flutter = **148 total tests, all passing**

## Sprint 15 Progress

- S15-001: ✅ DONE — Repository functions: `get_user_collection` (species, points, count, last_captured) and `get_leaderboard` (user_id, score, submission count)
- S15-002: ✅ DONE — `GET /v1/users/me/collection` endpoint (auth required, returns species grouped by real_name)
- S15-003: ✅ DONE — `GET /v1/leaderboard` endpoint (public, optional `limit` param, 1-500)
- S15-004: ✅ DONE — 7 tests: collection (species, empty, auth), leaderboard (entries, public, limit, invalid limit)
- S15-005: ✅ DONE — OpenAPI updated: 2 new paths (leaderboard, collection), 4 new schemas (CollectionResponse, CollectionEntry, LeaderboardResponse, LeaderboardEntry)
- 61 API tests + 49 scoring-rules + 14 Flutter = 124 total, all passing

## Sprint 14 Progress

- S14-001: ✅ DONE — GoogleVisionProvider with real REST API call (base64 encode, POST to vision.googleapis.com, parse response)
- S14-002: ✅ DONE — Parse labels + objects: detects species from OBJECT_LOCALIZATION, classifies context (zoo/pet/wild)
- S14-003: ✅ DONE — Added `requests` dependency to requirements.txt
- S14-004: ✅ DONE — Mock API tests (6 tests: zoo, wild, pet, empty, error, HTTP error, file-not-found)
- S14-005: ✅ DONE — Updated SESSION_CHECKLIST.md

## Sprint 12 Progress

- S12-001: ✅ DONE — JobQueue protocol + InMemoryJobQueue with process_pending()
- S12-002: ✅ DONE — ScoringWorker (polls queue, runs AIScoringService, stores result in DB)
- S12-003: ✅ DONE — Async submission flow: precheck sync, scoring async via queue
- S12-004: ✅ DONE — Background worker thread in FastAPI lifespan
- S12-005: ✅ DONE — Tests updated for async flow (process_pending after POST, GET to verify)

## Sprint 27 Progress

- S27-001: ✅ DONE — Created `services/api/Dockerfile` (Python 3.13-slim, uvicorn)
- S27-002: ✅ DONE — Expanded `docker-compose.local.yml` with `api` service (build, DB health check, volumes)
- S27-003: ✅ DONE — Added `infrastructure/docker/.env.docker` example
- S27-004: ✅ DONE — Updated README with Docker instructions (primary dev path)
- 89 API tests + 61 scoring-rules + 14 Flutter = **164 total tests, all passing**

## Sprint 26 Progress

- S26-001: ✅ DONE — Added `generate_derivative_stubs` to `StorageProvider` interface; renamed from `generate_derivative_urls`; implemented on `S3StorageProvider` and `GCSStorageProvider`
- S26-002: ✅ DONE — Replaced hardcoded `LocalFileStorage()` in media routes with `get_storage_provider()` factory
- S26-003: ✅ DONE — Added 8 cloud storage tests (factory defaults, S3/GCS URL formats, ImportError on missing deps, media roundtrip)
- S26-004: ✅ DONE — Sprint 26 plan created, state docs updated
- 89 API tests + 61 scoring-rules + 14 Flutter = **164 total tests, all passing**

## Sprint 25 Progress

- S25-001: ✅ DONE — Integration test: end-to-end capture flow (6 tests: wild, zoo, duplicate, multiuser, list, health)
- S25-002: ✅ DONE — API endpoint documentation (docstrings) added to all 14 endpoints
- S25-003: ✅ DONE — README.md updated with current build/run/test instructions
- S25-004: ✅ DONE — OpenAPI schema validation added to validate_docs.py (15 examples parsed)
- S25-005: ✅ DONE — CI job `integration-tests` added to docs-validation.yml (9 total jobs)

## Sprint 28 Progress

- S28-001: ✅ DONE — `http` package added to pubspec.yaml
- S28-002: ✅ DONE — `ApiClient` HTTP wrapper (base URL, auth, GET/POST/PATCH/putFile, ApiException)
- S28-003: ✅ DONE — `ApiConfig` env-var reader (`--dart-define`)
- S28-004: ✅ DONE — 6 API response models (UploadIntentResponse, CompleteUploadResponse, DerivativeUrls, ScoreState, SubmissionResponse, UserProfileResponse)
- S28-005: ✅ DONE — `CaptureRepository` (createUploadIntent, uploadFile, completeUpload, createSubmission, getSubmission, getProfile, getCollection, getLeaderboard)
- S28-006: ✅ DONE — `CaptureScreen` UI (species/context/caption fields, dropdown, submit button, status card)
- S28-007: ✅ DONE — `main.dart` HomeScreen with bottom nav (Map + Capture tabs)
- S28-008: ✅ DONE — 5 `ApiClient` unit tests (GET, POST, 404, 400 with detail, no-auth GET)
- S28-009: ✅ DONE — 5 `CaptureRepository` unit tests (uploadIntent, completeUpload, createSubmission, getProfile, error)
- S28-010: ✅ DONE — 2 `CaptureScreen` widget tests (form rendering, submit tap)
- 89 API tests + 61 scoring-rules + 27 Flutter = **177 total tests, all passing**

## Sprint 29 Progress

- S29-001: ✅ DONE — `image_picker: ^1.1.2` added to pubspec.yaml
- S29-002: ✅ DONE — `CaptureMediaService` abstract interface + `ImagePickerService` real impl
- S29-003: ✅ DONE — `CaptureScreen` two-phase flow: Camera/Gallery buttons → preview → fill form → submit
- S29-004: ✅ DONE — 4 new widget tests (form rendering, camera pick, gallery pick, broken image fallback)
- 89 API tests + 61 scoring-rules + 29 Flutter = **179 total tests, all passing**

## Sprint 34 Progress

- S34-001: ✅ DONE — MapScreen body wrapped in `RefreshIndicator` + `SingleChildScrollView`
- S34-002: ✅ DONE — Pull-to-refresh triggers `_viewModel.fetchMarkers()`
- S34-003: ✅ DONE — 2 new widget tests (RefreshIndicator present + pull triggers fetch)
- 89 API tests + 61 scoring-rules + 69 Flutter = **219 total tests, all passing**

## Current Next Action

Sprint 34 complete. Next: Sprint 35 (see BACKLOG.md).
