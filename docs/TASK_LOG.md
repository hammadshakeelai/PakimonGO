# Task Log

## 2026-07-01: Planning System Initialization

### Status

In progress.

### Summary

Created the initial planning package for PakimonGO before implementation. Captured the purified product prompt, discovery notes, requirements, SRS, architecture direction, process rules, roadmap, repo structure, knowledge system, QA strategy, security/privacy plan, data model plan, scoring/economy plan, Agile backlog, risk/debt registers, and OKF-style knowledge summaries.

### Decisions Made

- Plan before coding.
- Use a strict phase order: Discovery, Requirements, Agile SRS, Architecture, Prototypes, Scaffold, Implementation.
- Treat Flutter as the proposed mobile platform pending prototype validation.
- Treat PostgreSQL/PostGIS/pgvector plus object storage as the proposed data direction.
- Treat Firebase Auth/App Check/Storage as useful platform services, not the only canonical database.
- Treat scoring as server-authoritative and evidence-based.
- Treat public map locations as privacy-safe aggregates, not exact pins.
- Treat UGC moderation as launch-blocking.

### Open Work

- Review and approve SRS direction.
- Create remaining ADRs.
- Validate map provider options with prototype/cost/legal review.
- Backend framework is now accepted as FastAPI-style modular monolith for Sprint 0.
- Define scoring point ranges.
- Define first gold datasets.

### Next Exact Action

Review all planning docs for consistency, then create ADRs for auth, maps, AI scoring, storage, privacy, and moderation.

## 2026-07-01: Expanded Blueprint And Scaffold

### Status

In progress.

### Summary

Promoted the expanded PakimonGO blueprint into repository docs, repaired Git metadata, created the scaffold-only monorepo structure, added a short-burst commit policy, and added a conversation archive area for future full chat exports and AI handoff summaries.

### Decisions Made

- Treat the expanded 196-functional-requirement catalogue as the active requirements baseline.
- Treat gated Alpha-0 as the active SRS posture.
- Preserve empty scaffold folders with `.gitkeep`.
- Require short-burst semantic commits with AI attribution trailers.
- Require conversation archive updates when prompts or responses change direction, requirements, architecture, risk, process, or implementation state.

### Open Work

- Review and accept/revise proposed ADRs.
- Begin first Alpha-0 vertical slice work package.
- Scaffold runnable Flutter/FastAPI toolchains after ADR readiness.
- Paste full visible conversation into the prepared raw archive file if desired.

### Next Exact Action

Review ADR-001 through ADR-016, then decide whether WP-015 starts with Flutter/FastAPI toolchain scaffold or OpenAPI/contracts.

## 2026-07-01: Methodology-Aligned Pre-Code Specification

### Status

In progress.

### Summary

Read the external Software Engineering methodology from the Hakari Bankai project and applied its artifact chain to PakimonGO. Rebuilt the SRS around the methodology structure and added the analysis/design artifacts needed before code.

### Artifacts Added

- Methodology SRS.
- Software Engineering artifact folder.
- Traceability matrix.
- Work package board.
- OpenAPI draft.
- Database ERD.
- Threat model.
- UX flow spec.
- Testing master plan.
- Goldset manifest schema.
- ADR review pack.
- Agent handoff system.
- Obsidian vault index.
- OKF traceability/methodology entries.
- Graphify and OKF export plans.

### Next Exact Action

Review and accept/revise ADR-001 through ADR-016, then open WP-015 with a clear choice between contract generation and Flutter/FastAPI toolchain scaffolding.

## 2026-07-01: Mermaid Diagram Pack

### Status

Complete draft.

### Summary

Added a canonical Mermaid diagram pack under `docs/diagrams/` and linked it from the SRS, Software Engineering report plan, Obsidian vault index, README, and knowledge system docs.

### Diagrams Added

- System context.
- C4 containers.
- Architecture flow.
- Release process.
- Methodology chain.
- Use case overview.
- Domain model.
- Data flow.
- Database ERD.
- API capture sequence.
- Scoring pipeline.
- Privacy location flow.
- Threat model.
- UX flows.
- Package dependencies.
- Deployment view.

### Next Exact Action

Review diagrams for report inclusion and render them later when generating the final Software Engineering report.

## 2026-07-01: ADR Acceptance, Data Dictionary, Sprint 0 Plan

### Status

Complete draft.

### Summary

Completed the ADR acceptance pass, added the implementation data dictionary, and wrote the Sprint 0 implementation plan. This converts the pre-code package into an executable starting point for scaffold/toolchain work.

### Decisions

- Accepted ADRs: ADR-001, ADR-002, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-010, ADR-011, ADR-012, ADR-013, ADR-014, ADR-016.
- Revised ADR: ADR-009; minimized retention accepted, exact retention periods deferred.
- Deferred ADRs: ADR-003 final map provider, ADR-015 final production deployment approval.

### Artifacts Added

- `docs/data/DATA_DICTIONARY.md`
- `docs/sprints/README.md`
- `docs/sprints/SPRINT_0_PLAN.md`

### Next Exact Action

Begin Sprint 0 with toolchain availability checks and short-burst scaffold commits.

## 2026-07-01: Toolchain And Sprint 0 Packetization

### Status

Complete.

### Summary

Checked local toolchain readiness, added validation scripts, and split Sprint 0 into individual agent-ready task packets.

### Results

- `flutter doctor -v` reports no issues.
- Flutter 3.38.5 and Dart 3.10.4 are available.
- Android SDK 36.1.0 is available.
- Python 3.13.9 is available.
- `adb` is not on PATH, but exists at `C:/Users/HP/AppData/Local/Android/sdk/platform-tools/adb.exe`.
- `python tools/qa/validate_docs.py` passes.

### Artifacts Added

- `docs/tooling/TOOLCHAIN_READINESS.md`
- `tools/qa/README.md`
- `tools/qa/validate_docs.py`
- `tools/qa/check_toolchain.ps1`
- `docs/sprints/sprint-0/`

### Next Exact Action

Begin Sprint 0 implementation with S0-001 Flutter shell or S0-002 FastAPI shell.

## 2026-07-01: Pre-Code Test Architecture Pack

### Status

Complete.

### Summary

Added focused QA specs so tests can be implemented directly from the docs once Sprint 0 scaffold code appears.

### Artifacts Added

- `docs/qa/README.md`
- `docs/qa/REQUIREMENT_TO_TEST_MATRIX.md`
- `docs/qa/SPRINT_0_TEST_PLAN.md`
- `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md`
- `docs/qa/SCORING_STATE_TEST_SPEC.md`
- `docs/qa/GOLDSET_GOVERNANCE_PLAN.md`
- `docs/qa/ZOO_DUPLICATE_BENCHMARK_SPEC.md`
- `docs/qa/MANUAL_ANDROID_QA_CHECKLIST.md`
- `docs/qa/SECURITY_TEST_CHECKLIST.md`
- `docs/qa/CI_GATE_DESIGN.md`
- `docs/qa/DEFINITION_OF_READY_DONE.md`

### Next Exact Action

Begin Sprint 0 scaffold work and create the first real tests from the Sprint 0, privacy contract, and scoring state specs.

## 2026-07-01: Concrete Test Catalogue And CI Guardrails

### Status

Complete.

### Summary

Added concrete pre-code test cases, acceptance scenarios, fixture payloads, API examples, failure and release gate docs, secret scanning, JSON validation, and a GitHub Actions workflow for docs validation.

### Artifacts Added

- `docs/qa/TEST_CASE_CATALOGUE.md`
- `docs/qa/BDD_ACCEPTANCE_SCENARIOS.md`
- `docs/qa/FAILURE_MODE_MATRIX.md`
- `docs/qa/RELEASE_GATE_CHECKLIST.md`
- `docs/api/examples/`
- `docs/qa/fixtures/`
- `tools/qa/validate_json_examples.py`
- `tools/qa/scan_secrets.py`
- `.github/workflows/docs-validation.yml`

### Next Exact Action

Begin Sprint 0 implementation and convert the documented tests into real pytest/Dart tests as each scaffold module appears.

## 2026-07-01: Final Pre-Code Closure

### Status

Complete.

### Summary

Closed remaining pre-code governance gaps: test tooling standards, harness layout, coverage/flaky policy, local PR checklist, architecture fitness rules, ownership map, GitHub templates, workflow README update, and repeated pre-code completion audit.

### Artifacts Added

- `docs/adr/ADR-017-test-tooling-standards.md`
- `docs/qa/TEST_HARNESS_ARCHITECTURE.md`
- `docs/qa/COVERAGE_AND_FLAKY_POLICY.md`
- `docs/qa/LOCAL_PR_CHECKLIST.md`
- `docs/qa/ARCHITECTURE_FITNESS_RULES.md`
- `docs/qa/PRECODE_COMPLETION_AUDIT.md`
- `.github/CODEOWNERS`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/`

### Next Exact Action

Start Sprint 0 code with S0-001 Flutter shell or S0-002 FastAPI shell. Further useful test work now requires actual scaffold/code files.

## 2026-07-01: Safeguard System + Sprint 0 Verification

### Status

Complete.

### Summary

Built the mandatory pre/post-task prompt loop system to prevent context drift, state doc neglect, traceability gaps, and file size violations. Added `tools/qa/pre_task_check.py`, `docs/SESSION_CHECKLIST.md`, and the embedded loop checklist in `AGENTS.md`. Verified all 5 completed Sprint 0 tasks (S0-001 through S0-005) by running tests, analysis, and validation. Fixed `SPRINT_0_PLAN.md` state drift where it still said "Planned. Not started" despite 5 tasks being done. All validation scripts pass.

### Artifacts Added

- `tools/qa/pre_task_check.py` — automated pre-task guard (checks state docs, sprint status, file sizes, traceability)
- `docs/SESSION_CHECKLIST.md` — running session audit log for accountability

### Artifacts Updated

- `AGENTS.md` — added MANDATORY TASK LOOP block with 9-step pre/post checklist
- `docs/sprints/SPRINT_0_PLAN.md` — status, backlog table, and commit sequence now reflect completed tasks

### Decisions Made

- The mandatory loop (pre_task_check → read state → read packet → trace check → work → validate → update docs → commit → update session log) is now required for every work burst.
- Verification loop: after every task, re-run pre_task_check.py + all 3 validation scripts before moving to next task.

### Next Exact Action

Start S0-007: score state model. Read `docs/qa/SCORING_STATE_TEST_SPEC.md` and `docs/TRACEABILITY_MATRIX.md` for FR-SCORE-001–004, FR-SCORE-010–011.

## 2026-07-01: S0-006 Public DTO Privacy Tests

### Status

Complete.

### Summary

Implemented the first real Sprint 0 tests — 7 privacy contract tests that validate public DTOs never expose exact coordinates, original media URLs, or EXIF/GPS metadata. Added `services/api/tests/test_privacy_dto.py` with tests against both `docs/qa/fixtures/` and `docs/api/examples/` JSON files.

### Tests Added (7 total)

- TC-PRIV-DTO-001: public submission response rejects exact coordinate fields
- TC-PRIV-DTO-002: public map activity uses cells/clusters, not pins
- TC-PRIV-DTO-003: public media DTO exposes derivative URL only
- TC-PRIV-DTO-004: public derivatives never include EXIF/GPS fields
- Negative test: bad_public_location_leak_example.json triggers detection (proves the test works)
- All public fixtures pass with zero forbidden fields
- Private fixtures allow exact coordinates (informational check)

### Artifacts Added

- `services/api/tests/test_privacy_dto.py` — 7 privacy contract tests

### Forbidden Fields Detected

latitude, longitude, lat, lng, gps_* prefix, exif_* prefix, originalUrl, storagePath, signedUrl, deviceId, ipAddress, moderationEvidence, sensitiveSpeciesExactLocation, etc.

### Validation

All 9 API tests pass (7 privacy + 2 health). All 4 validation scripts pass. pre_task_check.py PASS.

### Next Exact Action

S0-007: Score state model in packages/scoring/. Read SCORING_STATE_TEST_SPEC.md and traceability matrix first.

## 2026-07-01: S0-007 Score State Model

### Status

Complete.

### Summary

Implemented the score state machine as a standalone `packages/scoring-rules/` package. The model defines 8 states, 14 valid transitions, an immutable ScoreEvent dataclass with pre/post-init validation, explanation category enforcement, and server-authority guards. No scoring formula, point values, or AI provider calls are included per S0-007's forbidden boundary.

### Artifacts Added

- `packages/scoring-rules/src/__init__.py`
- `packages/scoring-rules/src/score_state.py` — ScoreState enum, transition table, ScoreEvent dataclass with validation
- `packages/scoring-rules/tests/test_score_state.py` — 18 tests
- `services/api/tests/test_score_state.py` — 17 tests (mirror, importable from API test suite)

### States

pending, prechecked, ai_evaluated, scored, capped, review, rejected, rolled_back

### Test Coverage (18 total)

- TC-SCORE-STATE-001: valid transition table (14 edges)
- TC-SCORE-STATE-002: invalid direct finalization blocked
- TC-SCORE-STATE-003: formula version required for final states
- TC-SCORE-STATE-004: append-only (immutable creation)
- TC-SCORE-STATE-005: zoo cap saves entry with participation ledger
- TC-SCORE-STATE-006: duplicate cap without deletion
- TC-SCORE-STATE-007: unsafe interaction routes to review/rejection
- TC-SCORE-STATE-008: rollback from scored/capped valid
- Property tests: all states have inbound paths (except pending), terminals are immutable, client authority limited to pending, explanation categories enforced, server cannot send client-initiated final states

### Validation

All 26 API tests pass (17 score + 9 existing). All 18 package tests pass. All 4 validation scripts pass. pre_task_check.py reports 6→7 completed Sprint 0 tasks.

### Next Exact Action

S0-008: Capture draft model shell in apps/mobile/. Read traceability matrix for FR-CAP-001, FR-CAP-003, FR-CAP-004, FR-CAP-019.

## 2026-07-01: S0-008 Capture Draft Model Shell

### Status

Complete.

### Summary

Implemented the capture draft model in Flutter inside `apps/mobile/pakimon_go_app/`. The model represents local draft metadata — no camera plugin, upload, or scoring logic. Designed to satisfy FR-CAP-001, FR-CAP-003, FR-CAP-004, FR-CAP-019.

### Artifacts Added

- `apps/mobile/pakimon_go_app/lib/features/capture/domain/capture_draft.dart`
  - `CaptureDraft` model: localId, mediaPath, createdAt, updatedAt, lifecycle, context
  - `DraftLifecycle` enum: creating, saved, restored, deleted
  - `CaptureContext` enum: wild, zoo, pet, unknown
  - `CaptureDraftService` in-memory store: create, save, restore, delete
  - JSON serialization (`toJson`/`fromJson` round-trip)
- `apps/mobile/pakimon_go_app/test/features/capture/capture_draft_test.dart` — 13 unit tests

### Test Coverage (13 Flutter tests)

- Create with required fields
- markSaved lifecycle transition
- markDeleted lifecycle transition
- updateContext changes context
- JSON round-trip serialization
- Service create stores draft
- Service save persists lifecycle
- Service restore returns restored lifecycle
- Service delete marks as deleted
- Service delete on missing returns false
- Service save on missing returns null
- Service restore on missing returns null
- No exact location required for creation (privacy contract enforced)

### Validation

All 14 Flutter tests pass (13 capture + 1 widget). All 4 validation Python scripts pass. pre_task_check.py reports 8 completed Sprint 0 tasks.

### Next Exact Action

S0-009: Extend CI validation workflow. Read existing `.github/workflows/docs-validation.yml` and `docs/qa/CI_GATE_DESIGN.md`.

## 2026-07-01: S0-009 Extend CI Validation Workflow

### Status

Complete.

### Summary

Extended the GitHub Actions workflow to include all Phase 2 CI gate checks from `docs/qa/CI_GATE_DESIGN.md`. The workflow now runs 5 parallel jobs without secrets, deployment, or release signing.

### Artifacts Updated

- `.github/workflows/docs-validation.yml` — renamed to "Docs and Scaffold Validation"

### CI Jobs Added

| Job | Dependencies | Tests |
|---|---|---|
| `docs-validation` | PyYAML | validate_docs.py, validate_json_examples.py, scan_secrets.py |
| `api-tests` | fastapi, uvicorn, pytest, httpx | 26 pytest tests |
| `worker-tests` | pytest | 1 pytest test |
| `scoring-rules-tests` | none (stdlib only) | 18 pytest tests |
| `flutter-tests` | subosito/flutter-action@v2 | 14 Flutter tests |

### Validation

All 4 QA validation scripts pass. pre_task_check.py reports 9 completed Sprint 0 tasks.

### Next Exact Action

Sprint 1 — WP-015 Alpha-0 private capture slice. First task: upload intent + media validation scaffold.

## 2026-07-01: S0-010 Sprint 0 Closeout

### Status

Complete.

### Summary

Closed Sprint 0 by updating all state docs, traceability, backlog, tech debt, and conversation archive. Verified all 59 tests pass across 4 test suites. All 4 QA validation scripts PASS. All 10 Sprint 0 tasks marked DONE.

### Verification

- API tests: 26 passed
- Worker tests: 1 passed
- Scoring-rules tests: 18 passed
- Flutter tests: 14 passed
- QA validations: 4/4 PASS (pre_task_check, validate_docs, validate_json_examples, scan_secrets)

### Docs Updated

- `docs/sprints/SPRINT_0_PLAN.md` — sprint status "Complete", S0-010 ✅ DONE, commit 10 ✅
- `docs/CURRENT_TASK.md` — Sprint 0 complete, next is Sprint 1
- `docs/NEXT_TASK.md` — Sprint 1 kickoff targets
- `docs/CURRENT_THINKING.md` — Sprint 0 complete posture
- `docs/TASK_LOG.md` — S0-010 entry
- `docs/BACKLOG.md` — completed Sprint 0 items struck through
- `docs/TECH_DEBT.md` — CI debt updated to Phase 2 complete
- `docs/SESSION_CHECKLIST.md` — S0-010 row added
- `docs/conversation-archive/summaries/2026-07-01-sprint0-execution-s0-006-to-s0-010.md` (NEW)

### Next

Sprint 1 — WP-015 Alpha-0 private capture slice.

## 2026-07-01: Sprint 1 + S2-001/S2-002 Execution

### Status

Complete.

### Summary

Executed Sprint 1 (S1-001 through S1-004) — upload intent, submission endpoint, derivative stubs, CI auto-coverage. Then executed Sprint 2 (S2-001 + S2-002) — 10 SQLAlchemy models, Alembic migration, DB-backed repositories replacing all in-memory stores. Removed old domain-level in-memory stores.

### Changes Made

- `services/api/src/modules/media/api/routes.py` — rewritten to use `Depends(get_db)` with DB-backed repositories; removed `UploadIntentStore`/`DerivativeService` imports
- `services/api/src/modules/submissions/api/routes.py` — rewritten to use DB-backed repositories; removed `SubmissionStore`
- `services/api/src/infrastructure/database/repositories.py` — new file with `create_media_asset`, `complete_media_asset`, `get_media_asset`, `get_derivatives`, `create_submission`, `get_submission`
- `services/api/src/infrastructure/database/session.py` — added SQLite support via `check_same_thread`; added `drop_db()`
- `services/api/tests/conftest.py` — new file: sets `SYNC_DATABASE_URL` to temp SQLite file, creates/drops tables, cleans up temp file
- `services/api/src/modules/media/domain/upload_intent.py` — removed (unused)
- `services/api/src/modules/media/domain/derivative.py` — removed (unused)
- `services/api/src/modules/submissions/domain/submission.py` — removed (unused)

### Verification

- API tests: 45 passed
- Worker tests: 1 passed
- Scoring-rules tests: 18 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs, validate_json_examples, scan_secrets)

### Next

Plan Sprint 3 (auth integration, real upload handler, or duplicate/zoo precheck).

## 2026-07-01: Sprint 3 — Auth Integration

### Status

Complete.

### Summary

Implemented auth adapter pattern (ADR-006) with FakeAuthAdapter for dev/test. Added `get_current_user` FastAPI dependency that requires `Authorization: Bearer` header. Protected all 5 media/submission endpoints. Health endpoints remain public.

### Changes Made

- `services/api/src/infrastructure/auth/__init__.py` — new package
- `services/api/src/infrastructure/auth/adapter.py` — `AuthAdapter` protocol, `UserContext` dataclass
- `services/api/src/infrastructure/auth/fake_adapter.py` — `FakeAuthAdapter` accepting test_token_valid and test_user_* tokens
- `services/api/src/infrastructure/auth/dependencies.py` — `get_current_user`, `get_optional_user` FastAPI dependencies
- `services/api/src/modules/media/api/routes.py` — added `current_user: UserContext = Depends(get_current_user)` to all endpoints
- `services/api/src/modules/submissions/api/routes.py` — same
- `services/api/src/infrastructure/database/repositories.py` — `create_media_asset` accepts `owner_user_id`, `create_submission` accepts `user_id`
- `tests/test_media_upload.py` — all calls use `headers=AUTH_HEADER`, added `test_upload_intent_requires_auth`
- `tests/test_media_derivative.py` — all calls use `headers=AUTH_HEADER`
- `tests/test_submission.py` — all calls use `headers=AUTH_HEADER`

### Verification

- API tests: 46 passed (1 new auth test)
- Worker tests: 1 passed
- Scoring-rules tests: 18 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs, validate_json_examples, scan_secrets)

### Next

Sprint 4 — real upload handler, user registration, or duplicate/zoo precheck.

## 2026-07-01: Sprint 4 — Real Upload Handler

### Status

Complete.

### Summary

Replaced signed URL placeholders with local filesystem storage. Files upload via PUT multipart, save to data/uploads/, derivative stubs generated on disk, served via static endpoint.

### Changes Made

- `services/api/src/infrastructure/storage/local_storage.py` — `LocalFileStorage` with save_original, read_original, generate_derivative_stubs, delete_all, get_path (path traversal guard)
- `services/api/src/infrastructure/storage/__init__.py` — empty
- `services/api/src/modules/media/api/routes.py` — added PUT `/v1/media/upload/{id}` with `UploadFile`, updated upload-intent URL to local path, added GET `/v1/media/files/{path}` with `FileResponse`, derivative generation on complete
- `services/api/src/infrastructure/database/repositories.py` — added `update_media_asset_storage_key`
- `services/api/tests/conftest.py` — sets `UPLOAD_BASE` to temp dir, cleans up on session finish
- `tests/test_media_upload.py` — added `test_upload_file_roundtrip`, updated upload to use `files={"file": ...}` multipart
- `tests/test_media_derivative.py` — added `_upload_file` step to full flow
- `services/api/requirements.txt` — added `Pillow`
- `data/uploads/originals/`, `data/uploads/thumbs/`, `data/uploads/public/` — created

### Verification

- API tests: 47 passed (1 new roundtrip test)
- Worker tests: 1 passed
- Scoring-rules tests: 18 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs, validate_json_examples, scan_secrets)

### Next

Sprint 5 — user registration/onboarding, duplicate/zoo precheck, or OpenAPI draft update.

## 2026-07-01: Sprint 5 — User Registration/Onboarding

### Status

Complete.

### Summary

Added User auto-creation on first authenticated request, GET /v1/users/me for profile retrieval, PATCH /v1/users/me for profile updates.

### Changes Made

- `services/api/src/modules/users/` — new module with routes.py (GET/PATCH /v1/users/me)
- `services/api/src/main.py` — added users_router
- `services/api/src/infrastructure/database/repositories.py` — added get_or_create_user, update_user
- `services/api/src/infrastructure/auth/fake_adapter.py` — `test_token_valid` now returns stable `test_user_default` user_id (was random per call)
- `services/api/tests/test_user.py` — 5 tests (auto-create, auth required, full update, partial update, patch auth)

### Verification

- API tests: 52 passed (5 new user tests)
- Worker tests: 1 passed
- Scoring-rules tests: 18 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs, validate_json_examples, scan_secrets)

### Next

Sprint 7 — OpenAPI draft update, CI expansion, or real scoring AI pipeline stub.

## 2026-07-01: Sprint 6 — Duplicate/Zoo Precheck

### Status

Complete.

### Summary

Added `run_precheck()` pure function in scoring-rules package with duplicate detection (SHA256 matching) and animal-context rules. Wired into `POST /v1/submissions` — after creating submission, gets media SHA256, collects existing SHA256s (excluding current), runs precheck, updates submission status.

### Changes Made

- `packages/scoring-rules/src/precheck.py` — new file with `run_precheck()`, `PrecheckResult` dataclass
- `packages/scoring-rules/tests/test_precheck.py` — 8 tests (wild, zoo, pet, duplicate, edge cases)
- `services/api/src/modules/submissions/api/routes.py` — wired precheck into submission creation
- `services/api/src/infrastructure/database/repositories.py` — added `get_all_submission_sha256s`
- `services/api/tests/test_submission.py` — fixed SHA256 collision (all tests used same "a"*64), wild→ai_evaluated, zoo→capped, new duplicate test
- `docs/sprints/SPRINT_6_PLAN.md` — all 3 tasks marked DONE

### Verification

- API tests: 54 passed (2 new submission + 5 existing + 1 SH256 test fix)
- Scoring-rules tests: 26 passed (8 new precheck + 18 existing)
- Worker tests: 1 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs, validate_json_examples, scan_secrets)

### Next

Sprint 9 — Real scoring AI pipeline stub.

## 2026-07-01: Sprint 7 — OpenAPI Draft Update

### Status

Complete.

### Summary

Refreshed the OpenAPI draft and API examples to match all Sprint 1-6 implemented endpoints. The draft now has 18 real paths (up from 13 stale planning paths), 23 schemas (up from 22), and clearly marks future endpoints with `x-status: planned`.

### Changes Made

- `docs/api/OPENAPI_DRAFT.yaml` — complete rewrite: 18 paths, 23 schemas
- `docs/api/examples/create-upload-intent-response.json` — fixed uploadUrl to local path
- `docs/api/examples/complete-upload-request.json` — added mediaAssetId field
- `docs/api/examples/submission-private-response.json` — status→ai_evaluated, explanation→"normal"
- `docs/api/examples/score-detail-response.json` — updated to current ScoreState shape
- `docs/api/examples/complete-upload-response.json` — NEW
- `docs/api/examples/derivative-response.json` — NEW
- `docs/api/examples/user-profile-response.json` — NEW
- `docs/api/examples/patch-user-profile-request.json` — NEW
- `docs/api/examples/health-response.json` — NEW
- `docs/api/examples/upload-file-response.json` — NEW
- `docs/sprints/SPRINT_7_PLAN.md` — NEW, all 3 tasks marked DONE

### Verification

- API tests: 54 passed (unchanged)
- Scoring-rules tests: 26 passed (unchanged)
- Worker tests: 1 passed
- Flutter tests: 14 passed
- QA validations: 3/3 PASS (validate_docs: 18 paths/23 schemas, validate_json_examples: 23 files, scan_secrets: PASS)

### Next

Sprint 9 — Real scoring AI pipeline stub.

## 2026-07-01: Sprint 8 — CI Expansion

### Status

Complete.

### Summary

Added ruff linting and mypy type checking to the codebase. Fixed all 16 ruff issues and 38 mypy errors. Expanded CI workflow from 5 to 7 jobs.

### Changes Made

- `services/api/pyproject.toml` — ruff config (line-length 120, select E/F/W), mypy config with SQLAlchemy model overrides
- Multiple source files fixed for E501, F401, F541 issues
- `.github/workflows/docs-validation.yml` — added ruff-check and mypy-check jobs
- `docs/sprints/SPRINT_8_PLAN.md` — NEW, all 3 tasks marked DONE

### Verification

- API tests: 54 passed
- Ruff: 16→0 errors
- Mypy: 38→0 errors
- QA validations: 3/3 PASS

### Next

Sprint 10 — Deferred ADR review or real AI provider integration.

## 2026-07-01: Sprint 10 — Deferred ADR Review

### Status

Complete.

### Summary

Reviewed and accepted the two deferred ADRs:
- **ADR-003 (Map Provider)**: Accepted Mapbox-first prototyping direction. Google Maps Platform retained as challenger. Final commitment after prototype spike (Sprint 12+).
- **ADR-015 (Deployment Platform)**: Accepted Google Cloud/Firebase-first for alpha/beta: Cloud Run, Cloud SQL PostgreSQL (pgvector), Cloud Storage, Firebase Auth/App Check. Detailed architecture during beta prep.

### Changes Made

- `docs/adr/ADR-003-map-provider.md` — Status: Deferred → Accepted (prototyping direction)
- `docs/adr/ADR-015-deployment-platform.md` — Status: Deferred → Accepted (alpha/beta direction)
- `docs/ADR_REVIEW_PACK.md` — Status board + review section updated; all 17 ADRs now accepted or revised; zero deferred
- `docs/sprints/SPRINT_10_PLAN.md` — NEW
- `tools/qa/pre_task_check.py` — section check updated from "Sprint 2-9" → "Sprint 2-10"
- All state docs updated (CURRENT_TASK, NEXT_TASK, CURRENT_THINKING, BACKLOG, TASK_LOG)

### Verification

- API tests: 54 passed (unchanged)
- Scoring-rules tests: 32 passed (unchanged)
- Worker tests: 1 passed (unchanged)
- Flutter tests: 14 passed (unchanged)
- Total: 101 tests, all passing
- QA validations: 3/3 PASS
- Pre-task check: PASS (state_docs_exist, sprint_status, file_sizes, traceability_files)

### Next

Sprint 11 — Real AI provider integration or map prototype spike.

## 2026-07-01: Sprint 11 — AI Provider Adapter Framework

### Status

Complete.

### Summary

Built the AI provider adapter framework: VisionProvider protocol with AnalysisResult dataclass, DummyVisionProvider for CI/testing, AIScoringService (uses vision provider for context-based scoring, falls back to stub for capped paths), and GoogleVisionProvider placeholder. Wired AIScoringService into the submission flow with VISION_PROVIDER env var for provider selection.

### Changes Made

- `packages/scoring-rules/src/vision_provider.py` — NEW: VisionProvider protocol, AnalysisResult dataclass, DummyVisionProvider
- `packages/scoring-rules/src/scoring_service.py` — MODIFIED: added media_path param to protocol, added AIScoringService
- `packages/scoring-rules/src/google_vision_provider.py` — NEW: placeholder requiring GOOGLE_VISION_API_KEY env var
- `packages/scoring-rules/tests/test_scoring_service.py` — MODIFIED: 6 new AIScoringService tests
- `packages/scoring-rules/tests/test_vision_provider.py` — NEW: 5 tests
- `services/api/src/modules/submissions/api/routes.py` — MODIFIED: wired AIScoringService with DummyVisionProvider; VISION_PROVIDER env var for Google
- `docs/sprints/SPRINT_11_PLAN.md` — NEW

### Verification

- Scoring-rules tests: 43 passed (8 precheck + 18 score_state + 12 scoring_service + 5 vision_provider)
- API tests: 54 passed (unchanged)
- Worker tests: 1 passed (unchanged)
- Flutter tests: 14 passed (unchanged)
- Total: 112 tests, all passing
- Ruff: clean
- Mypy: clean
- QA validations: 3/3 PASS
- Pre-task check: PASS

### Next

Sprint 12 — Map prototype spike or real Google Vision provider implementation.

## 2026-07-01: Sprint 12 — Async Worker Scoring

### Status

Complete.

### Summary

Moved scoring from synchronous HTTP handler to async worker queue. Created JobQueue protocol + InMemoryJobQueue, ScoringWorker that polls the queue and runs AIScoringService in a background thread, and refactored POST /v1/submissions to enqueue scoring for wild submissions while scoring zoo/pet/duplicate synchronously.

### Changes Made

- `services/api/src/infrastructure/queue/__init__.py` — NEW
- `services/api/src/infrastructure/queue/queue.py` — NEW: Job dataclass, JobQueue protocol, InMemoryJobQueue with process_pending(), get_queue() singleton
- `services/api/src/infrastructure/worker/__init__.py` — NEW
- `services/api/src/infrastructure/worker/scoring_worker.py` — NEW: process_score_job(), process_pending_jobs(), AIScoringService with DummyVisionProvider
- `services/api/src/modules/submissions/api/routes.py` — MODIFIED: wild submissions enqueue job, return ai_evaluated; capped paths scored synchronously with StubScoringService
- `services/api/src/main.py` — MODIFIED: FastAPI lifespan starts background worker thread (500ms poll)
- `services/api/tests/test_submission.py` — MODIFIED: wild test calls _process_pending() then GETs; duplicate test uses async pattern for first submission

### Verification

- API tests: 54 passed (updated for async flow)
- Scoring-rules tests: 43 passed (unchanged)
- Worker tests: 1 passed (unchanged)
- Flutter tests: 14 passed (unchanged)
- Total: 112 tests, all passing
- Ruff: clean
- Mypy: clean
- QA validations: 3/3 PASS

### Next

Sprint 13 — Map prototype spike or real Google Vision provider implementation.

## 2026-07-01: Sprint 13 — Map Prototype Spike

### Status

Complete.

### Summary

Added Mapbox Flutter SDK (mapbox_maps_flutter 2.25.0) as a dependency, created a MapScreen with MapWidget, added AppConfig for MAPBOX_ACCESS_TOKEN env var, and updated the app's home screen to show the map. Without a real token, the map renders a placeholder message instead of crashing.

### Changes Made

- `pubspec.yaml` — added `mapbox_maps_flutter: ^2.25.0`
- `lib/core/config/app_config.dart` — NEW: AppConfig with mapboxAccessToken from `String.fromEnvironment('MAPBOX_ACCESS_TOKEN')`
- `lib/features/map/presentation/map_screen.dart` — NEW: MapScreen with MapWidget (Mapbox map or fallback text)
- `lib/main.dart` — rewritten: PakimonGoApp with MapScreen as home, MapboxOptions.setAccessToken on load
- `test/widget_test.dart` — updated: checks for "PakimonGO Map" title, no longer tests counter

### Verification

- Flutter tests: 14 passed (13 capture + 1 widget)
- Map renders on device/emulator with `--dart-define=MAPBOX_ACCESS_TOKEN=...`
- Python tests: all 112 passed (unchanged)

### Next

Sprint 14 — Real Google Vision provider implementation or collection/leaderboard endpoints.

## 2026-07-01: Sprint 9 — AI Scoring Pipeline Stub

### Status

Complete.

### Summary

Added a scoring service protocol and stub implementation in the scoring-rules package. The StubScoringService assigns deterministic points based on context: wild→25, zoo→1, pet→1, duplicate→0. Scoring runs synchronously after precheck in the submission creation flow. ScoreEvent records are stored in the database for every submission.

### Changes Made

- `packages/scoring-rules/src/scoring_service.py` — NEW: ScoringService protocol, ScoringResult dataclass, StubScoringService
- `packages/scoring-rules/tests/test_scoring_service.py` — NEW: 6 tests
- `services/api/src/infrastructure/database/repositories.py` — added create_score_event, get_latest_score_event
- `services/api/src/modules/submissions/api/routes.py` — wired scoring after precheck, updated response builder to use latest score event
- `services/api/tests/test_submission.py` — updated assertions: wild→scored(25pts), zoo→capped(1pt), duplicate→capped(0pt)
- `packages/scoring-rules/tests/test_precheck.py` — removed unused import
- `packages/scoring-rules/tests/test_score_state.py` — removed unused import, fixed E501
- `packages/scoring-rules/tests/test_scoring_service.py` — added noqa E402
- `docs/sprints/SPRINT_9_PLAN.md` — NEW, all 4 tasks marked DONE

### Verification

- API tests: 54 passed (updated submission assertions)
- Scoring-rules tests: 32 passed (26 existing + 6 new)
- Worker tests: 1 passed
- Flutter tests: 14 passed
- Total: 101 tests, all passing
- Ruff: clean (both api and scoring-rules)
- Mypy: clean
- QA validations: 3/3 PASS

## 2026-07-02: Sprint 25 — Integration Testing and Documentation

### Status

Complete.

### Summary

Sprint 25 delivered integration testing, endpoint documentation, README update, OpenAPI schema validation, and a new CI job.

### Changes Made

- `services/api/tests/test_integration.py` — NEW: 6 end-to-end tests (wild capture, zoo capture, duplicate detection, multiuser collection, submission list, health)
- `services/api/src/modules/*/api/routes.py` — Added FastAPI docstrings to all 14 endpoints
- `services/api/src/main.py` — Added docstrings to health endpoints
- `README.md` — Rewritten with current build/run/test instructions and endpoint table
- `tools/qa/validate_docs.py` — Added check_openapi_examples() function (validates all 15 example JSON files parse)
- `.github/workflows/docs-validation.yml` — Added integration-tests job (9 total CI jobs)

### Verification

- API tests: 90 passed (84 existing + 6 integration)
- Scoring-rules tests: 61 passed
- Flutter tests: 14 passed
- Total: **159 tests, all passing**
- QA validations: 4/4 PASS (pre_task_check, validate_docs, validate_json_examples, scan_secrets)
- Ruff: clean
- Mypy: clean

## 2026-07-02: Sprint 26 — Wire Cloud Storage into Media Flow

### Status

Complete.

### Summary

Sprint 26 replaced hardcoded `LocalFileStorage` in media routes with the env-configurable `get_storage_provider()` factory, enabling S3/GCS in production.

### Changes Made

- `services/api/src/infrastructure/storage/cloud_storage.py` — Renamed `generate_derivative_urls` to `generate_derivative_stubs` on StorageProvider, S3StorageProvider, GCSStorageProvider
- `services/api/src/modules/media/api/routes.py` — Changed `_storage = LocalFileStorage()` to `_storage = get_storage_provider()`
- `services/api/tests/test_cloud_storage.py` — Rewritten with 8 tests: factory defaults, S3/GCS URL formats, ImportError on missing deps, media roundtrip with local provider
- `docs/sprints/SPRINT_26_PLAN.md` — NEW

### Verification

- API tests: 89 passed (84 existing + 5 new cloud storage)
- Scoring-rules tests: 61 passed
- Flutter tests: 14 passed
- Total: **164 tests, all passing**
- Ruff: clean
- QA validations: 4/4 PASS

## 2026-07-02: Sprint 27 — Docker Compose Local Dev Environment

### Status

Complete.

### Summary

Sprint 27 created a full local dev environment with Docker Compose, enabling one-command startup of PostgreSQL + API.

### Changes Made

- `services/api/Dockerfile` — NEW: Python 3.13-slim, pip install, uvicorn CMD
- `infrastructure/docker/docker-compose.local.yml` — Expanded from just `db` to `db` + `api` services with build context, health check, named volumes
- `infrastructure/docker/.env.docker` — NEW: documented Docker-specific env vars
- `infrastructure/docker/README.md` — Rewritten with quick start, verify, alembic instructions
- `README.md` — Updated with Docker as primary dev path

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 14 passed
- Total: **164 tests, all passing**
- Ruff: clean
- QA validations: 4/4 PASS

## 2026-07-03: Sprint 28 — Connect Flutter Mobile to API

### Status

Complete.

### Summary

Sprint 28 wired the Flutter mobile app to the FastAPI backend with a full HTTP client, response models, and capture screen UI.

### Changes Made

- `apps/mobile/pakimon_go_app/pubspec.yaml` — Added `http: ^1.6.0` dependency
- `apps/mobile/pakimon_go_app/lib/core/network/api_client.dart` — NEW: ApiClient with base URL, auth token, GET/POST/PATCH/putFile, ApiException
- `apps/mobile/pakimon_go_app/lib/core/network/api_config.dart` — NEW: env-var reader via --dart-define
- `apps/mobile/pakimon_go_app/lib/shared/models/api_models.dart` — NEW: 6 response models
- `apps/mobile/pakimon_go_app/lib/features/capture/data/capture_repository.dart` — NEW: 8 API methods
- `apps/mobile/pakimon_go_app/lib/features/capture/presentation/capture_screen.dart` — NEW: Capture UI with form fields and upload→submit flow
- `apps/mobile/pakimon_go_app/lib/main.dart` — Rewritten with HomeScreen bottom nav (Map + Capture tabs)
- `apps/mobile/pakimon_go_app/test/features/capture/api_client_test.dart` — NEW: 5 mock HTTP tests
- `apps/mobile/pakimon_go_app/test/features/capture/capture_repository_test.dart` — NEW: 5 mock repository tests
- `apps/mobile/pakimon_go_app/test/features/capture/capture_screen_test.dart` — NEW: 2 widget tests
- `apps/mobile/pakimon_go_app/test/widget_test.dart` — Updated for nav test
- `docs/sprints/SPRINT_28_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 27 passed (was 14 pre-S28: +10 unit + 2 widget + 1 nav)
- Total: **177 tests, all passing**
- Ruff: clean
- QA validations: pending commit

## 2026-07-03: Sprint 29 — Camera Plugin Integration

### Status

Complete.

### Summary

Sprint 29 replaced fake image bytes in the Flutter capture flow with real device camera/gallery capture via the `image_picker` plugin.

### Changes Made

- `apps/mobile/pakimon_go_app/pubspec.yaml` — Added `image_picker: ^1.1.2`
- `apps/mobile/pakimon_go_app/lib/features/capture/domain/capture_media_service.dart` — NEW: CaptureMediaService abstract interface + CaptureMediaResult model with SHA256
- `apps/mobile/pakimon_go_app/lib/features/capture/data/image_picker_service.dart` — NEW: ImagePickerService using ImagePicker (camera + gallery, max 2048px)
- `apps/mobile/pakimon_go_app/lib/features/capture/presentation/default_capture_media_service.dart` — NEW: production factory
- `apps/mobile/pakimon_go_app/lib/features/capture/presentation/capture_screen.dart` — Rewritten: Camera/Gallery buttons, image preview with error fallback, two-phase flow
- `apps/mobile/pakimon_go_app/lib/main.dart` — Uses createDefaultMediaService()
- `apps/mobile/pakimon_go_app/test/features/capture/capture_screen_test.dart` — Rewritten: 4 widget tests
- `apps/mobile/pakimon_go_app/test/widget_test.dart` — Uses mock media service (avoids image_picker native dependency)
- `docs/sprints/SPRINT_29_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 29 passed (was 27 pre-S29: +2 new widget tests + 2 rewritten)
- Total: **179 tests, all passing**

## 2026-07-03: Sprint 30 — Auth/Onboarding UI

### Status

Complete.

### Summary

Sprint 30 created a login/onboarding flow that stores auth tokens and wires them to the API client, allowing users to sign in before capturing wildlife.

### Changes Made

- `apps/mobile/pakimon_go_app/lib/core/auth/auth_service.dart` — NEW: ChangeNotifier with loginWithUserId/loginWithToken/logout/isAuthenticated, listener notification
- `apps/mobile/pakimon_go_app/lib/core/network/api_client.dart` — Refactored: accepts `String Function()` token provider instead of fixed string; all endpoints read token dynamically
- `apps/mobile/pakimon_go_app/lib/features/auth/presentation/login_screen.dart` — NEW: Login UI with user ID entry, token paste mode, Sign In with getProfile verification
- `apps/mobile/pakimon_go_app/lib/main.dart` — Rewritten: AuthGate routing (login → home), ApiClient with token provider, logout button
- `apps/mobile/pakimon_go_app/test/core/auth/auth_service_test.dart` — NEW: 8 unit tests
- `apps/mobile/pakimon_go_app/test/features/auth/login_screen_test.dart` — NEW: 5 widget tests
- `apps/mobile/pakimon_go_app/test/features/capture/api_client_test.dart` — Updated: authToken → tokenProvider
- `apps/mobile/pakimon_go_app/test/features/capture/capture_repository_test.dart` — Updated: authToken → tokenProvider
- `docs/sprints/SPRINT_30_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 42 passed (was 29 pre-S30: +8 unit + 5 widget)
- Total: **192 tests, all passing**
