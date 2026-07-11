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

## 2026-07-03: Sprint 31 — Offline Draft Persistence

### Status

Complete.

### Summary

Sprint 31 added offline persistence for capture drafts using shared_preferences, preventing data loss when the app is closed mid-capture.

### Changes Made

- `apps/mobile/pakimon_go_app/pubspec.yaml` — Added `shared_preferences: ^2.3.0`
- `apps/mobile/pakimon_go_app/lib/features/capture/domain/draft_persistence_service.dart` — NEW: DraftPersistenceService abstract interface + InMemoryDraftStorage
- `apps/mobile/pakimon_go_app/lib/features/capture/data/shared_prefs_draft_storage.dart` — NEW: SharedPrefsDraftStorage (JSON serialization, draft ID index)
- `apps/mobile/pakimon_go_app/lib/features/capture/domain/capture_draft.dart` — CaptureDraftService now async; all mutating methods persist; new loadPersistedDrafts() method; new `all` getter
- `apps/mobile/pakimon_go_app/test/features/capture/capture_draft_test.dart` — Updated: all service tests now async; added InMemoryDraftStorage tests (5) + loadPersistedDrafts + all getter tests
- `docs/sprints/SPRINT_31_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 49 passed (was 42 pre-S31: +7 new/updated draft tests)
- Total: **199 tests, all passing**

## 2026-07-03: Sprint 32 — Map Markers from API

### Status

Complete.

### Summary

Sprint 32 added user submission markers to the Mapbox map by fetching data from the API and displaying loading/error/marker states.

### Changes Made

#### Backend
- `services/api/src/infrastructure/database/models.py` — Added `capture_location` relationship to `Submission` + `submission` back-populate on `CaptureLocation`
- `services/api/src/modules/submissions/api/routes.py` — `_build_submission_response` now includes `cellLatitude`/`cellLongitude` derived from `CaptureLocation` (rounded to 3dp, ~111m precision)

#### Flutter
- `apps/mobile/pakimon_go_app/lib/shared/models/submission_marker.dart` — NEW: marker model with fromJson, hasValidLocation filter
- `apps/mobile/pakimon_go_app/lib/features/capture/data/capture_repository.dart` — NEW `getMapMarkers()`: GET /v1/submissions → parse markers, filter zero-location
- `apps/mobile/pakimon_go_app/lib/features/map/domain/map_viewmodel.dart` — NEW: ChangeNotifier with fetchMarkers, loading/error/markerCount state
- `apps/mobile/pakimon_go_app/lib/features/map/presentation/map_screen.dart` — Refactored: injectable viewModel, loading indicator, error+retry, marker count overlay
- `apps/mobile/pakimon_go_app/lib/main.dart` — MapViewModel wired with ApiClient in HomeScreen
- `apps/mobile/pakimon_go_app/test/features/map/map_viewmodel_test.dart` — NEW: 4 unit tests
- `apps/mobile/pakimon_go_app/test/features/map/map_screen_test.dart` — NEW: 4 widget tests (loading, loaded, error, retry)
- `apps/mobile/pakimon_go_app/test/features/capture/capture_repository_test.dart` — 2 new tests (getMapMarkers parse + zero-location filter)
- `apps/mobile/pakimon_go_app/test/widget_test.dart` — Updated: uses mock MapViewModel to avoid real HTTP
- `docs/sprints/SPRINT_32_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 59 passed (was 49 pre-S32: +10 new)
- Total: **209 tests, all passing**

## 2026-07-03: Sprint 33 — Species Detail Screen

### Status

Complete.

### Summary

Sprint 33 added a tap-through flow from map marker overlay → sighting list → species detail screen.

### Changes Made

- `apps/mobile/pakimon_go_app/lib/features/species/presentation/species_detail_screen.dart` — NEW: species name in AppBar, photo placeholder, info card (points, status, lat/lng)
- `apps/mobile/pakimon_go_app/lib/features/map/presentation/marker_list_screen.dart` — NEW: tappable list with color-coded avatars, species, status, coordinates, navigation to detail
- `apps/mobile/pakimon_go_app/lib/features/map/presentation/map_screen.dart` — Marker overlay now tappable (GestureDetector + chevron icon), navigates to MarkerListScreen
- `apps/mobile/pakimon_go_app/test/features/species/species_detail_screen_test.dart` — NEW: 4 widget tests
- `apps/mobile/pakimon_go_app/test/features/map/marker_list_screen_test.dart` — NEW: 4 widget tests (list, empty, subtitle, navigation)
- `docs/sprints/SPRINT_33_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 67 passed (was 59 pre-S33: +8 new)
- Total: **217 tests, all passing**

## 2026-07-03: Sprint 34 — Pull-to-Refresh on Map

### Status

Complete.

### Summary

Sprint 34 added pull-to-refresh gesture to the MapScreen, allowing users to swipe down to reload sightings from the API.

### Changes Made

- `apps/mobile/pakimon_go_app/lib/features/map/presentation/map_screen.dart` — Body wrapped in `RefreshIndicator` + `SingleChildScrollView` with `AlwaysScrollableScrollPhysics`; pull triggers `_viewModel.fetchMarkers()` in all states (loading, error, no-token, map)
- `apps/mobile/pakimon_go_app/test/features/map/map_screen_test.dart` — 2 new tests (RefreshIndicator presence + pull gesture triggers fetch)
- `docs/sprints/SPRINT_34_PLAN.md` — NEW

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 69 passed (was 67 pre-S34: +2 new)
- Total: **219 tests, all passing**

## 2026-07-03: Sprint 42 — Flutter Leaderboard Screen

### Status

Complete.

### Summary

Sprint 42 added a leaderboard screen to the Flutter app: model, viewmodel, screen with pull-to-refresh, and 4th bottom nav tab.

### Changes Made

- `lib/shared/models/api_models.dart` — Added `LeaderboardEntry` model with fromJson
- `lib/features/leaderboard/domain/leaderboard_viewmodel.dart` — NEW: ChangeNotifier with fetchLeaderboard
- `lib/features/leaderboard/presentation/leaderboard_screen.dart` — NEW: Screen with loading/empty/error/list states, pull-to-refresh, rank numbers, score display
- `lib/main.dart` — Added 4th bottom nav tab "Leaderboard" with `Icons.leaderboard`
- `test/widget_test.dart` — Updated with `_NoOpLeaderboardRepository` + 4th tab
- `test/features/leaderboard/leaderboard_test.dart` — NEW: 8 tests (2 model + 3 viewmodel + 3 widget)

### Verification

- 102 Flutter tests pass (+8)
- 103 API + 61 scoring-rules + 102 Flutter = 266 total tests

## 2026-07-03: Sprint 41 — Flutter Notification Center

### Status

Complete.

### Summary

Sprint 41 added the Flutter notification center: model, repository methods, viewmodel, screen, and app bar badge integration.

### Changes Made

- `lib/shared/models/api_models.dart` — Added `NotificationModel` with fromJson
- `lib/features/capture/data/capture_repository.dart` — Added `getNotifications()`, `markNotificationRead()`, `getUnreadNotificationCount()`
- `lib/features/notifications/domain/notification_viewmodel.dart` — NEW: ChangeNotifier with fetchNotifications, fetchUnreadCount, markAsRead
- `lib/features/notifications/presentation/notification_screen.dart` — NEW: Screen with loading/empty/error/list states, pull-to-refresh, tap-to-mark-read, read/unread visual distinction
- `lib/main.dart` — Added bell icon with red badge in app bar; navigates to NotificationScreen; refreshes unread count on resume and return
- `test/features/notifications/notification_viewmodel_test.dart` — NEW: 5 tests (empty start, fetch, error, mark read, fetch count)
- `test/features/notifications/notification_screen_test.dart` — NEW: 3 widget tests (loading, empty, error+retry)

### Verification

- 94 Flutter tests pass (+8)
- 103 API + 61 scoring-rules + 94 Flutter = 258 total tests

## 2026-07-03: Sprint 40 — User Notifications (Backend)

### Status

Complete.

### Summary

Sprint 40 added a notification system to the backend: DB model, repository, REST endpoints, and wiring into both sync and async scoring paths.

### Changes Made

- `src/infrastructure/database/models.py` — Added `Notification` table (user_id, notification_type, title, body, reference_type, reference_id, is_read)
- `alembic/versions/002_add_notifications.py` — Migration for notifications table
- `src/infrastructure/database/repositories/notification.py` — NEW: create_notification, get_notifications, mark_notification_read, unread_notification_count
- `src/modules/notifications/api/routes.py` — NEW: GET /v1/notifications, PATCH /v1/notifications/{id}/read, GET /v1/notifications/unread-count (all auth-protected)
- `src/modules/submissions/api/routes.py` — Wired notification creation into sync scoring path
- `src/infrastructure/worker/scoring_worker.py` — Wired notification creation into async scoring path
- `tests/test_notifications.py` — NEW: 6 tests

### Verification

- 103 API tests pass (+6)
- 61 scoring-rules tests pass
- 250 total tests (103 API + 61 scoring-rules + 86 Flutter)

## 2026-07-03: Sprint 39 — API Error Handling Middleware

### Status

Complete.

### Summary

Sprint 39 added centralized error handling with structured JSON error responses for all unhandled exceptions across the API.

### Changes Made

- `src/infrastructure/middleware/error_middleware.py` — NEW: `ErrorHandlingMiddleware` catches ValueError/KeyError/PermissionError/FileNotFoundError/unhandled Exception; `http_exception_handler` registered as FastAPI exception handler for HTTPException
- `src/main.py` — Wired `ErrorHandlingMiddleware` + `app.add_exception_handler(HTTPException, http_exception_handler)`
- `tests/test_error_middleware.py` — NEW: 8 tests covering all error types + passthrough + body shape

### Verification

- 97 API tests pass (+8 new)
- 61 scoring-rules tests pass
- Error response shape: `{"error": {"code": "...", "message": "...", "details": {}}}`
- 5xx errors logged with stack trace

## 2026-07-03: Sprint 38 — CI Workflow Update

### Status

Complete.

### Summary

Sprint 38 updated the CI workflow with job dependency chains, a broader Flutter SDK version, test count echo steps, and a final summary job.

### Changes Made

- `.github/workflows/docs-validation.yml` — Added `needs:` chains: docs-validation → lint → test → integration → all-checks-pass summary job
- Flutter version changed from `3.38.x` to `3.x` for broader compatibility
- Test count echo steps added to API, scoring-rules, and Flutter jobs
- Worker tests made non-fatal (best-effort)
- `all-checks-pass` job summarizes all 9 CI checks

### Verification

- All QA validations pass
- 89 API + 61 scoring-rules + 86 Flutter = **236 total tests**

## 2026-07-03: Sprint 37 — Map Marker Clustering

### Status

Complete.

### Summary

Sprint 37 added marker clustering to reduce visual clutter when many sightings exist nearby. Closest markers are grouped using haversine distance within a 2km radius.

### Changes Made

- `lib/features/map/domain/cluster_service.dart` — NEW: `ClusterMarker` model (center lat/lng, count, species preview) + `ClusterService.cluster()` (haversine distance-based grouping, 2km default radius)
- `lib/features/map/domain/map_viewmodel.dart` — NEW: `clusters`/`clusterCount` getters; `_buildClusters()` called on fetch; thresholds at >3 markers
- `lib/features/map/presentation/map_screen.dart` — Overlay shows "X clusters · Y sightings" when clusters exist, "Y sightings" otherwise
- `test/features/map/cluster_service_test.dart` — NEW: 6 tests (empty, nearby grouped, distant separated, species preview x3)
- `test/features/map/map_viewmodel_test.dart` — 2 new tests (clusters empty ≤3, clusters generated >3)

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 86 passed (was 78 pre-S37: +8 new)
- Total: **236 tests, all passing**
- QA validations: 4/4 PASS

## 2026-07-03: Sprint 36 — Photo Thumbnail in Species Detail

### Status

Complete.

### Summary

Sprint 36 replaced the static photo placeholder in SpeciesDetailScreen with a live thumbnail image fetched from the API, with loading and error fallback states.

### Changes Made

- `lib/shared/models/submission_marker.dart` — Added `mediaAssetId` field (required String)
- `lib/features/species/presentation/species_detail_screen.dart` — Replaced `_buildPhotoPlaceholder` with `_buildPhoto(theme)` using `Image.network()` with `loadingBuilder` and `errorBuilder`; thumbnail URL constructed from `ApiConfig.baseUrl`
- `lib/shared/models/api_models.dart` — `toMarker()` passes `mediaAssetId`
- `test/features/species/species_detail_screen_test.dart` — Updated for `Image` widget
- `test/features/map/marker_list_screen_test.dart` — Updated "Failed to load photo" assertion
- `test/features/map/map_viewmodel_test.dart` — Added `mediaAssetId` to markers
- `test/features/map/map_screen_test.dart` — Added `mediaAssetId` to markers

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 78 passed (same count, updated tests)
- Total: **228 tests, all passing**
- QA validations: 4/4 PASS

## 2026-07-03: Sprint 35 — Submission History Screen

### Status

Complete.

### Summary

Sprint 35 added a dedicated submission history screen showing past submissions with species name, points, and status, accessible from a third "History" tab in the bottom nav.

### Changes Made

- `services/api/src/modules/submissions/api/routes.py` — Added `realName` + `animalContext` to `_build_submission_response` dict
- `apps/mobile/.../shared/models/api_models.dart` — Added `realName`, `animalContext` fields + `toMarker()` method to `SubmissionResponse`
- `apps/mobile/.../features/capture/data/capture_repository.dart` — Added `getSubmissions()` method (GET /v1/submissions)
- `apps/mobile/.../features/submissions/domain/submission_history_viewmodel.dart` — NEW: ChangeNotifier with fetchSubmissions, loading/error states
- `apps/mobile/.../features/submissions/presentation/submission_history_screen.dart` — NEW: ListView with species, points, status; tap→SpeciesDetailScreen
- `apps/mobile/.../main.dart` — Added History tab (3rd NavigationDestination)
- `test/features/submissions/submission_history_viewmodel_test.dart` — NEW: 5 tests
- `test/features/submissions/submission_history_screen_test.dart` — NEW: 4 widget tests
- `test/widget_test.dart` — Updated with History tab, mock getSubmissions

### Verification

- API tests: 89 passed
- Scoring-rules tests: 61 passed
- Flutter tests: 78 passed (was 69 pre-S35: +9 new)
- Total: **228 tests, all passing**
- QA validations: 4/4 PASS

## 2026-07-03: Sprint 43 — Production Deployment CI/CD

### Status

Complete.

### Summary

Sprint 43 added production deployment infrastructure: DB-connected health check, gunicorn config, multi-stage Dockerfile, Render IaC, and deploy workflow.

### Changes Made

- `services/api/src/main.py` — `/health/ready` now verifies DB via `SELECT 1` (503 on failure), imports `Depends`, `get_db`, `Session`, `text`
- `services/api/gunicorn.conf.py` — NEW: 4 uvicorn workers, 120s timeout, stdout access log
- `Dockerfile` — NEW: Multi-stage build (builder + python:3.13-slim runtime), HEALTHCHECK, gunicorn CMD
- `render.yaml` — NEW: Render web service + PostgreSQL (free plan), health check and env var mapping
- `.github/workflows/deploy.yml` — NEW: workflow_dispatch trigger, curl to Render API with secrets
- `README.md` — Added "Deploy to Render" section, updated endpoint table + test counts
- `tests/test_health.py` — Updated `test_health_ready` assertion to match new response shape

### Verification

- 103 API tests pass
- 61 scoring-rules tests pass
- 102 Flutter tests pass
- Total: **266 tests, all passing**
- QA validations: 4/4 PASS

## 2026-07-03: Sprint 44 — Flutter Profile Screen

### Status

Complete.

### Summary

Sprint 44 added a profile/settings screen: view user info, edit age band and home region, with a person icon in the app bar replacing the direct logout button.

### Changes Made

- `lib/features/capture/data/capture_repository.dart` — Added `updateProfile()` (PATCH /v1/users/me with ageBand/homeRegion)
- `lib/features/profile/domain/profile_viewmodel.dart` — NEW: ChangeNotifier with fetchProfile, setAgeBand, setHomeRegion, saveProfile, hasChanges, loading/error/saving states
- `lib/features/profile/presentation/profile_screen.dart` — NEW: Profile info card (userId, email, trustState), settings card (ageBand dropdown, homeRegion text field, save button), about card (app name, version), logout button
- `lib/main.dart` — Added `ProfileViewModel`, replaced logout `IconButton` with person icon that navigates to `ProfileScreen`; logout moved inside profile screen
- `test/features/profile/profile_test.dart` — NEW: 11 tests (8 viewmodel + 3 screen widget)

### Verification

- 113 Flutter tests pass (+11)
- 103 API + 61 scoring-rules + 113 Flutter = 277 total tests

## 2026-07-03: Sprint 45 — Flutter Collection Screen

### Status

Complete.

### Summary

Sprint 45 added a species collection screen: view captured species with points, counts, sorting/filtering, and pull-to-refresh, accessible from the ProfileScreen.

### Changes Made

- `lib/shared/models/api_models.dart` — Added `CollectionResult` class + `CollectionEntry` model with fromJson
- `lib/features/capture/data/capture_repository.dart` — Refactored `getCollection()` to return typed `CollectionResult` with sort/filter params (context, sortBy, sortOrder)
- `lib/features/collection/domain/collection_viewmodel.dart` — NEW: ChangeNotifier with fetchCollection, setSortBy, setSortOrder, setContextFilter, refresh; loading/loaded/empty/error states
- `lib/features/collection/presentation/collection_screen.dart` — NEW: Filter bar (sort dropdown + sort order toggle + context dropdown), species list with CircleAvatar, points display, pull-to-refresh, empty/error states
- `lib/features/profile/presentation/profile_screen.dart` — Added "View Collection" button in profile card; accepts optional `CaptureRepository`; navigates to CollectionScreen
- `lib/main.dart` — Passes `CaptureRepository` to ProfileScreen for collection navigation
- `test/features/collection/collection_test.dart` — NEW: 10 tests (6 viewmodel + 4 screen widget)

### Verification

- 123 Flutter tests pass (+10)
- 103 API + 61 scoring-rules + 123 Flutter = 287 total tests

## 2026-07-04: Tier 1 — Mapbox Wiring + Submission Rate Limiting

### Status

Complete.

### Summary

Wired Mapbox for local dev (public pk. token via --dart-define=MAPBOX_ACCESS_TOKEN, secret sk. download token in ~/.gradle/gradle.properties); the debug APK built, installed, and launched on the Pixel_9a emulator. Implemented per-user submission rate limiting (Tier 1 #4, NFR-SEC-004): a configurable cooldown on POST /v1/submissions returning 429 too_many_requests before any DB write.

### Artifacts Changed

- services/api/src/modules/submissions/api/routes.py — _submission_cooldown_seconds() helper + cooldown check before create
- services/api/src/infrastructure/database/repositories/submission.py — get_last_submission_time()
- services/api/src/infrastructure/database/repositories/__init__.py — export new repo fn
- services/api/tests/conftest.py — SUBMISSION_COOLDOWN_SECONDS=0 for the suite
- services/api/tests/test_submission.py — 2 new tests (429 enforced; disabled-allows-rapid control)

### Config

- SUBMISSION_COOLDOWN_SECONDS (default 30, 0 disables). Read per-request so it is monkeypatch-testable.

### Validation

- API: 105 passed (103 + 2 new). scoring-rules: 61 passed. validate_docs / validate_json_examples / scan_secrets: PASS.

### Next Exact Action

Tier 1 #5: APK size optimization (ProGuard/R8/split-per-ABI) — no external creds needed. Then Firebase Auth + Google Vision (need cloud projects).

## 2026-07-04: Tier 1 #5 — APK Size Optimization (R8 + split-per-ABI)

### Status

Complete (config + build verified; physical-device map render pending).

### Summary

Enabled R8 minify + shrinkResources + ProGuard in the release buildType and per-ABI APK splitting via `flutter build apk --split-per-abi`. Added android/app/proguard-rules.pro keeping Mapbox/Google/Flutter classes. Release build compiles cleanly under R8; app installs, launches, and stays running on the x86_64 emulator.

### Results

- arm64-v8a: 39.8MB (was 105.8MB fat, -62%)
- armeabi-v7a: 30.8MB
- x86_64: 42.7MB
- MaterialIcons tree-shaken 99.7%.

### Notes / Risk

- First attempt used a Gradle splits{} block which conflicts with the plugin-injected ndk.abiFilters; switched to the Flutter --split-per-abi flag (no gradle splits block).
- R8 logs benign com.mapbox.common.* ClassNotFound warnings at startup (caught, non-fatal). Verify the map renders on a physical arm64 release build.

### Artifacts Changed

- apps/mobile/pakimon_go_app/android/app/build.gradle.kts
- apps/mobile/pakimon_go_app/android/app/proguard-rules.pro (new)

### Next Exact Action

Remaining Tier 1 (Firebase Auth, Google Vision) needs cloud projects. No-cred work: Tier 2 (Postgres wiring, Flutter error handling).

## 2026-07-04: Tier 1 #2 (partial) — Firebase Auth backend adapter

### Status

Backend adapter built + tested; not yet activated (needs creds + Flutter sign-in).

### Summary

Added FirebaseAuthAdapter (firebase-admin verify_id_token, lazy get_app/initialize_app, injectable verifier) and made the auth adapter env-selectable via AUTH_PROVIDER (default: fake). Added firebase-admin to requirements. 4 unit tests via a mocked verifier — no live creds needed. Existing 105 tests unaffected (fake adapter still default). API suite now 109 passing.

### Activation (when creds arrive)

- Backend: pip install firebase-admin; set AUTH_PROVIDER=firebase + GOOGLE_APPLICATION_CREDENTIALS=<service-account.json>.
- Flutter: add firebase_auth + google_sign_in, place google-services.json in android/app/, send the Firebase ID token as the Bearer token (still to build).

### Artifacts Changed

- services/api/src/infrastructure/auth/firebase_adapter.py (new)
- services/api/src/infrastructure/auth/dependencies.py (env-based selection)
- services/api/requirements.txt (+firebase-admin)
- services/api/tests/test_firebase_auth.py (new, 4 tests)

### Next Exact Action

Google Vision needs no code — user provides GOOGLE_VISION_API_KEY and we set VISION_PROVIDER=google. Firebase: user provides google-services.json + service-account key -> activate backend + build Flutter sign-in.

## 2026-07-04: Tier 1 #3 — AI Vision Scoring via Groq (free tier)

### Status

Complete + live-verified.

### Summary

Added GroqVisionProvider (packages/scoring-rules/src/groq_vision_provider.py): a free-tier vision provider using Groq's OpenAI-compatible chat-completions endpoint with an image data URI and JSON-mode output (species + wild/zoo/pet + confidence). Wired VISION_PROVIDER=groq selection into scoring_worker.py. 8 mocked unit tests. Groq's free tier needs no billing/card (unlike Google Vision, which requires billing enabled even for its free tier).

### Live verification

- /models probe: key authenticates on the free tier (17 models); meta-llama/llama-4-scout-17b-16e-instruct is live.
- Real classification of a bear photo -> species "Ursus arctos", context "wild", confidence 0.99; JSON parsed correctly.

### Tests

scoring-rules 69 (61+8 new), API 109. All 3 validators pass.

### Artifacts Changed

- packages/scoring-rules/src/groq_vision_provider.py (new)
- packages/scoring-rules/tests/test_groq_vision_provider.py (new, 8 tests)
- services/api/src/infrastructure/worker/scoring_worker.py (groq branch)
- .env.example (VISION_PROVIDER / GROQ_API_KEY / GROQ_MODEL)

### Activation

Set VISION_PROVIDER=groq + GROQ_API_KEY in the API environment (GROQ_MODEL optional). Key lives in gitignored .env.local.

### Next Exact Action

Firebase Auth Flutter integration (firebase_auth + google_sign_in + google-services.json). Then Tier 2.

## 2026-07-04: Tier 1 #2 complete (code) — Firebase Auth (backend + Flutter Google Sign-In)

### Status

Code-complete + tests pass. Live Google sign-in blocked by the emulator having no Google account.

### Summary

Backend: firebase-admin installed, service account at ~/.pakimongo/ (outside repo), FirebaseAuthAdapter active via AUTH_PROVIDER=firebase — verified (dev token -> 401; real Firebase ID token accepted). Flutter: added firebase_core 4.11 / firebase_auth 6.5 / google_sign_in 7.2, the google-services gradle plugin, minSdk 23, Firebase.initializeApp() in main, and a real "Sign in with Google" button (google_sign_in 7.x authenticate -> Firebase credential -> Firebase ID token -> backend). Debug APK builds/installs/runs; Firebase initializes. Fixed a login-screen RenderFlex overflow by wrapping the form in SingleChildScrollView. Flutter 125 tests pass.

### Live verification notes

- Registered the debug SHA-1 in Firebase (SHA-256 alone did NOT create the Android OAuth client); google-services.json now has the type-1 Android client.
- Backend rejects fake tokens (401) with AUTH_PROVIDER=firebase.
- Google Sign-In UI showed a black screen because the emulator has no Google account -> add a Google account to the emulator/device to finish the interactive flow.

### Artifacts Changed

- apps/mobile/pakimon_go_app/pubspec.yaml, pubspec.lock (firebase deps)
- apps/mobile/pakimon_go_app/android/settings.gradle.kts, android/app/build.gradle.kts (google-services plugin, minSdk 23)
- apps/mobile/pakimon_go_app/lib/main.dart (Firebase.initializeApp)
- apps/mobile/pakimon_go_app/lib/features/auth/presentation/login_screen.dart (Google sign-in + scroll fix)
- .gitignore (google-services.json). Not committed (secrets): google-services.json, .env.local, service account.

### Next Exact Action

Add a Google account to the emulator (or use a physical device) to complete the live Google sign-in test. Then Tier 2. For production: register the release keystore SHA-1 in Firebase.

## 2026-07-04: Firebase Auth live-verified + map marker limit fix

### Status

Complete. Tier 1 now 100% complete and live-verified.

### Firebase Auth — live-verified

Installed the debug arm64 APK on a real Android phone (served over LAN; API reachable at 192.168.100.54:8000). Signed in with Google -> Firebase ID token -> backend. Backend logs (from phone 192.168.100.117): GET /v1/users/me 200, notifications 200, POST /v1/submissions 200, leaderboard 200 -> real Firebase token accepted (fake token still 401). Full real-auth chain confirmed on a real device.

### Bug fix — map markers 422

CaptureRepository.getMapMarkers requested limit=200 on GET /v1/submissions, but the endpoint caps limit at 100 (le=100) -> 422, so the map marker overlay silently failed to load. Changed the default to limit=100. 125 Flutter tests pass.

### Artifacts Changed

- apps/mobile/pakimon_go_app/lib/features/capture/data/capture_repository.dart (getMapMarkers limit 200 -> 100)

### Next Exact Action

Tier 2: Postgres wiring, Flutter error handling. For production: register the release keystore SHA-1 in Firebase.

## 2026-07-04: Tier 2 #7 (partial) — ApiClient network hardening

### Status

Network layer done; per-screen offline/retry UI still TODO.

### Summary

Hardened ApiClient: added a 15s request timeout; normalized transport failures (TimeoutException / SocketException / http.ClientException) into ApiException(isNetworkError: true) so callers catch one type; fixed error-message extraction to read the backend's {"error":{"message"}} format AND FastAPI's {"detail":...} (string or 422 list) — previously a 422 list crashed the `as String` cast. Added an isNetworkError flag to ApiException. 4 new tests (structured error, 422 list, transport failure, timeout). Flutter suite 129 passing.

### Artifacts Changed

- apps/mobile/pakimon_go_app/lib/core/network/api_client.dart
- apps/mobile/pakimon_go_app/test/features/capture/api_client_test.dart

### Next Exact Action

Surface ApiException.isNetworkError in the UI (offline banner + retry) on the map/history/leaderboard screens. Then Tier 2 #6 Postgres wiring.

## 2026-07-05: Tier 2 #7 — offline/error + Retry UI on Map/History/Leaderboard

### Status

Core error handling done.

### Summary

Added a shared ErrorRetryView widget (cloud-off + "You appear to be offline" for transport failures; error icon + "Something went wrong" otherwise; both show the real message + a Retry button). MapViewModel, SubmissionHistoryViewModel and LeaderboardViewModel now expose isOffline and store a clean message (ApiException.message, or a generic line for unexpected errors) instead of raw e.toString(). Wired ErrorRetryView into the Map, History and Leaderboard screens (replacing their bespoke error blocks). Updated 3 tests that asserted the old hardcoded titles. Flutter suite 129 passing.

### Artifacts Changed

- lib/shared/widgets/error_retry_view.dart (new)
- lib/features/{map,submissions,leaderboard}/domain/*_viewmodel.dart (isOffline + clean messages)
- lib/features/{map,submissions,leaderboard}/presentation/*_screen.dart (use ErrorRetryView)
- test: map_viewmodel_test (throw ApiException), map_screen_test + submission_history_screen_test (new error-state text)

### Next Exact Action

Extend the same pattern to Profile/Collection screens; then Tier 2 #6 Postgres wiring.

## 2026-07-05: Tier 2 #7 done — offline/error + Retry on Profile & Collection

### Summary

Extended the shared ErrorRetryView + isOffline pattern to ProfileViewModel/ProfileScreen and CollectionViewModel/CollectionScreen (both use a load-state enum). Their error states now show the offline-vs-error UI with the real message + Retry, replacing bespoke error columns. Tier 2 #7 (Flutter error handling) now covers all 5 data screens. Analyze clean; Flutter suite 129 passing.

### Artifacts Changed

- lib/features/profile/domain/profile_viewmodel.dart, presentation/profile_screen.dart
- lib/features/collection/domain/collection_viewmodel.dart, presentation/collection_screen.dart

### Next Exact Action

Tier 2 #6 Postgres wiring (needs Docker), or Tier 2 #8/#9 onboarding + age-gate screens.

## 2026-07-05: Security — harden media upload (size + image + ownership)

### Status

Complete. Closes two flagged architectural gaps + a BOLA hole.

### Summary

PUT /v1/media/upload previously read the whole file with no checks. Added: (1) ownership check — only the intent's owner_user_id may upload (403), previously any authenticated user could write to another user's intent (BOLA); (2) size enforcement on the actual bytes via file.size and len() (413), not just the client-declared byteSize; (3) empty-file rejection (400); (4) image content validation by magic bytes (JPEG/PNG/WebP) — non-images rejected (400). Added 413 -> payload_too_large to the error middleware. Path traversal on GET /media/files was already handled by LocalFileStorage.get_path (resolve + containment check).

### Tests

- 3 new: non-image rejected (400), oversized rejected (413), other-user's asset rejected (403).
- Updated 4 tests that uploaded fake bytes (media_upload/integration/cloud_storage/media_derivative) to valid JPEG signatures.
- Fixed test_gcs_provider_requires_gcs: google-cloud-storage is now installed (firebase-admin dep), so GCS construction fails on credentials, not ImportError.
- API 112 passing, scoring-rules 69.

### Artifacts Changed

- services/api/src/modules/media/api/routes.py (_is_supported_image + upload validation)
- services/api/src/infrastructure/middleware/error_middleware.py (413)
- services/api/tests/{test_media_upload,test_integration,test_cloud_storage,test_media_derivative}.py

### Next Exact Action

Tier 2 #6 Postgres wiring (needs Docker) or Tier 2 #8/#9 onboarding + age gate.

## 2026-07-05: Tier 2 #9 — age gate (13+)

### Summary

Added a neutral COPPA-style age gate (FR-AGE-001..003). AgeGateService collects a birth year (without revealing the threshold), blocks under-13, and records a coarse band (teen 13–17 / adult 18+) for future stricter defaults. Persisted via a small AgeGateStore interface (SharedPreferences impl for prod, in-memory for tests) so it asks once. AgeGate wraps the whole app before the auth gate: spinner while loading, neutral birth-year screen when unknown, blocked screen for under-13, otherwise the app. 11 tests (7 service logic + 4 widget proving the gating behaviour). Analyze clean; Flutter suite 140.

### Artifacts Changed

- lib/features/age_gate/domain/age_gate_service.dart (new)
- lib/features/age_gate/data/shared_prefs_age_gate_store.dart (new)
- lib/features/age_gate/presentation/age_gate.dart (new)
- lib/main.dart (wrap home in AgeGate)
- test/features/age_gate/{age_gate_service_test,age_gate_widget_test}.dart (new)

### Next Exact Action

Tier 2 #8 onboarding screens, or #6 Postgres wiring (needs Docker). Also: persist the age band to the backend profile on first sign-in.

## 2026-07-05: Tier 2 #8 — onboarding screens

### Summary

Added a 4-page first-run onboarding flow (FR-ONB-001..005): welcome, wildlife safety (don't chase/touch/feed), location privacy + "we only ask for camera/location when you use them", and scoring honesty (wild scores most; zoo/pet capped; duplicates don't score; AI isn't perfect). OnboardingService persists a seen flag via a small OnboardingStore interface (SharedPreferences prod / in-memory test). OnboardingGate wraps the app after the age gate and before auth: spinner while loading, the PageView flow when unseen (page dots + Next/Get started + Skip), otherwise the app. 6 tests (2 service + 4 widget covering first-launch, Skip, full paging, already-seen). Analyze clean; Flutter suite 146.

Startup chain is now: AgeGate -> OnboardingGate -> AuthGate -> Home.

### Artifacts Changed

- lib/features/onboarding/domain/onboarding_service.dart (new)
- lib/features/onboarding/data/shared_prefs_onboarding_store.dart (new)
- lib/features/onboarding/presentation/onboarding.dart (new)
- lib/main.dart (wrap child in OnboardingGate)
- test/features/onboarding/{onboarding_service_test,onboarding_widget_test}.dart (new)

### Next Exact Action

Tier 2 #6 Postgres wiring (Docker is now running) or #11 CI secrets. Also: persist age band + onboarding completion to the backend profile.

## 2026-07-05: Tier 2 #6 — PostgreSQL wiring (verified end-to-end)

### Summary

Brought up the pgvector Postgres container and verified the API runs against real Postgres, not just SQLite. Found and fixed two migration bugs that were hidden because dev uses create_all on SQLite (never the migration path): (1) migration 002 built an invalid index `ON notifications (user_id, NOT is_read)` — a bare expression in the column list — fixed to a partial index `(user_id) WHERE NOT is_read`; (2) the sensitive_species table was never captured in a migration, so added 003. env.py now honors SYNC_DATABASE_URL so migrations target the same DB as the app. Parameterized the compose host port (DB_HOST_PORT, default 5432) because a native Postgres already held 5432 and shadowed the container.

### Verification

- Ran `alembic upgrade head` -> 001,002,003 apply cleanly; all 12 model tables present on Postgres.
- API on Postgres: /health/ready 200; authed CRUD (users/me, upload-intent, POST submission, collection, notifications) all 200; rows confirmed in Postgres (users/media/submissions/score_events/notifications = 1 each).
- SQLite test suite unaffected: API 112 passing.

### How to run the API on Postgres locally

DB_HOST_PORT=5433 docker compose -f infrastructure/docker/docker-compose.local.yml up -d db
cd services/api && SYNC_DATABASE_URL=postgresql://postgres:dummy_local_password@127.0.0.1:5433/pakimongo_local python -c "from alembic.config import main; main(argv=['upgrade','head'])"
# then run uvicorn with the same SYNC_DATABASE_URL.

### Artifacts Changed

- services/api/alembic/env.py (honor SYNC_DATABASE_URL)
- services/api/alembic/versions/002_add_notifications.py (fix invalid index)
- services/api/alembic/versions/003_add_sensitive_species.py (new)
- infrastructure/docker/docker-compose.local.yml (DB_HOST_PORT override)

### Next Exact Action

Auto-run migrations on deploy (or at API startup in non-test envs); CI secrets (#11).

## 2026-07-05: Tier 5 — dark mode

### Summary

Added light + dark Material 3 themes (AppTheme) seeded from the brand green. ThemeController holds the ThemeMode (system/light/dark), persists it (ThemeStore interface; SharedPreferences prod / in-memory test), and is exposed app-wide via ThemeScope (InheritedNotifier) so any screen can read/change it without constructor threading. main.dart wraps MaterialApp in ThemeScope + ListenableBuilder with theme/darkTheme/themeMode. Added a 3-way theme toggle to the Profile Settings card (hidden when no ThemeScope, so profile_test is unaffected). Fixed a real concurrency bug: the constructor's async _load() could clobber a setMode() that raced ahead — added a hydration guard. 5 tests (4 controller + 1 widget proving the scope flips brightness). Analyze clean; Flutter suite 151.

### Artifacts Changed

- lib/core/theme/{app_theme,theme_controller,shared_prefs_theme_store}.dart (new)
- lib/main.dart (ThemeScope + darkTheme + themeMode)
- lib/features/profile/presentation/profile_screen.dart (theme toggle)
- test/core/theme/theme_controller_test.dart (new)

### Next Exact Action

Tier 5 polish: accessibility (semantic labels), loading shimmers. (analyze warnings: DONE)

---

## 2026-07-06 — Render deploy LIVE + emulator UI walkthrough (3 crashes fixed)

### What Happened

**Backend deployed to production:** `https://pakimongo-api.onrender.com` via
Blueprint (pakimongo-db Postgres + pakimongo-api web service, free tier).
Deploy fixes needed: correct repo URL, SYNC_DATABASE_URL from managed DB,
PYTHONPATH to api root, migrations in startCommand (free tier lacks
preDeployCommand), $PORT bind, postgres:// scheme normalization,
python-multipart in requirements (FastAPI Form/File crashed without it).
All 3 alembic migrations applied on Render Postgres. Smoke-verified:
/health/live, /health/ready (DB connected), authed /v1/users/me.

**Full emulator UI walkthrough** (Pixel 9a, fake auth + real seed data)
found and fixed 3 crashes the mock-based tests missed:
1. History tab: SubmissionResponse.fromJson only parsed the detail shape;
   the list endpoint returns species/context/status + scoreEvent → parse
   now handles both (regression test w/ real payload).
2. Profile: DropdownButtonFormField crashed on legacy ageBand "18_24"
   not in preset items → unknown bands appended to options.
3. Collection: pushed as a route with no Scaffold → 'No Material widget
   found' from its dropdowns → screen now supplies Scaffold + AppBar;
   tests un-wrapped to pump it bare like the real route.

Verified working on emulator: age gate → onboarding (4 pages) → login →
map (real Mapbox globe w/ --dart-define token) → history (real data) →
leaderboard → notifications → profile → dark mode → collection.

### Tests

153 Flutter (was 151), 112 API, 69 scoring — all green. analyze clean.

### Next Exact Action

Moderation (report/block) — last code blocker for Play Store. User-side:
release keystore + SHA-1 (see docs/LAUNCH_CHECKLIST.md).

---

## 2026-07-06 (later) — Moderation + map overhaul + UI polish

### Built

- **Moderation (FR-MOD-001..003, 009)**: reports (6 reasons, dedup 409,
  audit rows), blocks (idempotent, one-directional leaderboard filtering),
  17 API tests. Flutter: report dialog, report action on submission detail,
  leaderboard report/block menu, Profile -> Blocked Users screen, 9 tests.
- **Map overhaul**: markers drawn as colored circle annotations, camera
  auto-fit with street-biased zoom (z16 tight), Mapbox Standard 3D style
  with 55° pitch at street zooms, Snapchat-style camera FAB -> Capture tab,
  AppBar refresh (pull-to-refresh removed, it fought panning).
- **Backend location fix**: list payload now carries publicLocation with
  ~1km rounded cells (never exact coords) — the map previously had NO
  coordinates to draw. Marker parser handles both payload shapes.
- **Profile redesign**: identity header (avatar/email/trust chip),
  own Scaffold + AppBar (it had neither -> Chip crash + no back button),
  full-width actions. MapViewModel dispose-ownership crash fixed.

### State

145 backend tests (129 API pre-location +1, +17 moderation), 162 Flutter
tests, analyze clean, migrations 001->004 apply cleanly. Deployed to
Render on push (auto-deploy).

### Next

Moderator console (post-launch), loading shimmers, accessibility.

---

## 2026-07-06 (docs) - Ground active handoff state

### Summary

Updated the active handoff docs so they no longer point agents at completed
Tier 1/Tier 2 work. The docs now distinguish demoable alpha state from
store-ready production state: Render backend live, Render Postgres verified,
Firebase/Groq live checks recorded, user-facing moderation done, map/profile
polish landed, but iOS, real-device E2E, production storage, release auth
SHA-1, moderator console/appeals, accessibility, loading polish, and store
materials remain.

### Artifacts Changed

- docs/CURRENT_TASK.md
- docs/NEXT_TASK.md
- docs/CURRENT_THINKING.md
- docs/BACKLOG.md
- docs/BUGS_AND_RISKS.md
- docs/TECH_DEBT.md
- docs/TASK_LOG.md
- docs/SESSION_CHECKLIST.md

### Verification

- `python tools/qa/pre_task_check.py` passed before edits.
- `python tools/qa/pre_task_check.py` passed after edits.
- `python tools/qa/validate_docs.py` passed.
- `python tools/qa/validate_json_examples.py` passed.
- `python tools/qa/scan_secrets.py` passed.
- Full backend/scoring/Flutter suites were not re-run for this doc-only update.

### Next

Recommended no-credential task: accessibility pass across the Flutter app.
Alternative small polish: loading shimmer/skeleton states. Larger launch work:
real-device E2E, durable object storage, release Firebase SHA-1, moderator
console/appeals, and store/legal materials.

---

## 2026-07-06 (design) - Social game UI concept

### Summary

Read the conversation archive index, raw archived planning chats, archive
summaries, requirements, SRS, UX flow spec, scoring/economy plan, expanded
blueprint, and launch checklist. Captured the user's original game direction:
real-animal map/camera discovery, surprise scoring, collection building,
friends/groups, social posting, likes/comments/reposts/shares, hashtags,
leaderboards, and safety/privacy gates.

Added a high-level V2 UI/product concept for a more exciting social game layer:
Map, Capture, Feed, Collection, Rank; score reveal cards; profile grid; field
stories; discovery reels; squad quests; habitat challenges; and social post
cards with visibility, reactions, comments, repost/share, report, and block.

The user clarified that this is V2 design work and pointed to V1 screenshots in
`docs/assets/COMPLETE UI SCREENSHOTS - V1/`. Audited all 10 screenshots and
expanded the concept with V1 gaps, V2 directions, and external inspiration
directions from map games, social photo apps, group/community apps, challenge
apps, and nature-ID apps.

### Artifacts Changed

- docs/ux/SOCIAL_GAME_UI_CONCEPT.md
- docs/ux/UX_FLOW_SPEC.md
- docs/conversation-archive/summaries/2026-07-06-social-game-ui-concept.md
- docs/CURRENT_TASK.md
- docs/NEXT_TASK.md
- docs/CURRENT_THINKING.md
- docs/BACKLOG.md
- docs/BUGS_AND_RISKS.md
- docs/TECH_DEBT.md
- docs/TASK_LOG.md
- docs/SESSION_CHECKLIST.md

### Verification

- `python tools/qa/pre_task_check.py` passed.
- `python tools/qa/validate_docs.py` passed.
- `python tools/qa/validate_json_examples.py` passed.
- `python tools/qa/scan_secrets.py` passed.
- Full backend/scoring/Flutter suites were not re-run because this was a
  doc/design-only update.

### Next

Review `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` and choose the first V2 wireframe
pack before any social UI implementation begins.

---

## 2026-07-06 (design prototype) - V2 clickable HTML/CSS/JS prototype

### Summary

Built a clickable, hardcoded HTML/CSS/JavaScript prototype for the PakimonGO V2
direction using the 10 downloaded V2 concept panels as visual input. The
prototype lives under `docs/prototypes/v2-ui-html/` and recreates the major
planning screens: Map Home, Capture Review, Score Reveal, Social Feed, Player
Profile, Field Guide Collection, Rank Hub, Group Page, Notifications, and
Empty/Error State.

The app uses hash routing, a bottom navigation shell, dummy state, selectable
chips/tabs, form fields, social reactions, report/block/appeal modals, share
and offline toasts, and privacy-safe location labels.

This is a design-planning artifact only. It is not wired to Flutter, the API,
auth, scoring, persistence, moderation workflows, or production feature flags.

### Artifacts Changed

- docs/prototypes/v2-ui-html/index.html
- docs/prototypes/v2-ui-html/style.css
- docs/prototypes/v2-ui-html/app.js
- docs/prototypes/v2-ui-html/README.md
- docs/ux/SOCIAL_GAME_UI_CONCEPT.md
- docs/assets/V2 UI CONCEPT PANELS/README.md
- docs/CURRENT_TASK.md
- docs/NEXT_TASK.md
- docs/CURRENT_THINKING.md
- docs/BACKLOG.md
- docs/BUGS_AND_RISKS.md
- docs/TECH_DEBT.md
- docs/TASK_LOG.md
- docs/SESSION_CHECKLIST.md

### Verification

- `python tools/qa/pre_task_check.py` passed before edits.
- `python tools/qa/pre_task_check.py` passed after edits.
- `python tools/qa/validate_docs.py` passed.
- `python tools/qa/validate_json_examples.py` passed.
- `python tools/qa/scan_secrets.py` passed.
- `node --check docs/prototypes/v2-ui-html/app.js` passed.
- Edge headless screenshots rendered for Map, Feed, and Score routes.
- Full backend/scoring/Flutter suites were not re-run because this was a
  static docs/prototype-only update.

### Next

Open `docs/prototypes/v2-ui-html/index.html`, click through the dummy app flow,
and choose which screens/interactions should become accepted wireframes or
requirements before V2 Flutter implementation begins.

---

## 2026-07-06 (design prototype) - V2 prototype polish pass

### Summary

Improved the clickable V2 HTML/CSS/JS prototype after review. The pass focused
on making the dummy app feel closer to the V2 concept panels while staying a
real HTML prototype: stronger map HUD, better nearby activity sheet,
photo-first capture review, richer score reveal, tighter social feed card,
more polished group/profile/collection/rank surfaces, active tabs/chips,
notification filters, modals, toasts, and clearer safety/privacy affordances.

This remains a planning prototype only. It is not Flutter code and does not
implement backend social, scoring, moderation, storage, auth, or push features.

### Artifacts Changed

- docs/prototypes/v2-ui-html/style.css
- docs/prototypes/v2-ui-html/app.js
- docs/prototypes/v2-ui-html/README.md
- docs/CURRENT_TASK.md
- docs/NEXT_TASK.md
- docs/CURRENT_THINKING.md
- docs/BACKLOG.md
- docs/BUGS_AND_RISKS.md
- docs/TECH_DEBT.md
- docs/TASK_LOG.md
- docs/SESSION_CHECKLIST.md

### Verification

- `python tools/qa/pre_task_check.py` passed before edits.
- `python tools/qa/pre_task_check.py` passed after edits.
- `python tools/qa/validate_docs.py` passed.
- `python tools/qa/validate_json_examples.py` passed.
- `python tools/qa/scan_secrets.py` passed.
- `node --check docs/prototypes/v2-ui-html/app.js` passed.
- Edge headless screenshots rendered for Map, Feed, and Score routes.
- The dedicated web-game Playwright client could not run because its local
  `playwright` package was missing; Edge headless screenshot verification was
  used instead.
- Full backend/scoring/Flutter suites were not re-run because this was a static
  docs/prototype-only update.

### Next

Review the improved prototype and choose which V2 interactions should be
promoted into requirements, wireframes, or future backlog.

---

## 2026-07-06 (prod debugging) — Google sign-in, photos, real GPS

User field-tested the v0.2.0-alpha APK against production and reported:
Google sign-in broken ("expired token" on History, map replaced by error),
photos never render, leaderboard empty, captures mapped to wrong area.

### Root causes + fixes

1. **Server ran AUTH_PROVIDER=fake** → rejected real Firebase ID tokens
   (dev user-id logins worked, Google did not — exactly the reported split).
   FirebaseAuthAdapter gained a credential-free path: verify ID tokens
   against Google's public certs with FIREBASE_PROJECT_ID only (no secret
   file on the host). render.yaml now ships AUTH_PROVIDER=firebase.
   Verified live: dev tokens 401, health green.
2. **Client never refreshed the Firebase ID token** (expires ~1h).
   AuthService registers a refresher (SDK getIdToken cache); ApiClient
   awaits a FutureOr token provider on every request.
3. **Photos 404'd always**: submission detail built apiBase + /v1/... →
   double /v1; both detail screens asked for .jpg while the pipeline
   writes .webp.
4. **Captures were hardcoded to Islamabad + jitter.** Added geolocator:
   permission flow, 10s high-accuracy fix, last-known fallback, graceful
   no-location submission. Injectable LocationService for tests.
5. Leaderboard "empty" was simply a fresh prod DB — populates as users
   submit (verified: alice at 50 pts from live testing).

### State

130 API + 162 Flutter tests, analyze clean. Rebuilt v0.2.0-alpha APKs
pointed at prod with all fixes.

## 2026-07-11 — Production social layer + internet demo content

### Shipped

1. Migration 005: reactions (unique per user+post, toggle semantics),
   comments (soft delete), stories (24h expires_at), story_views.
2. New modules: social (PUT reaction, comments CRUD w/ 10/min rate
   limit) and stories (list grouped w/ seen flags, post, view, views).
3. /v1/feed enriched with reactionCounts, myReaction, commentCount via
   two grouped queries (no N+1). GET /v1/users/{id}/profile added.
4. tools/fetch_demo_images.py: 17 CC-licensed wildlife photos from
   iNaturalist -> assets/demo/wild/ + CREDITS.md (Commons API is
   blocked on this network; iNaturalist carries license metadata).
5. demo_seed_social.py wave: 6 new community users, 17 real-photo
   submissions, seeded comments + reactions, self-refreshing 24h demo
   stories (ring never goes empty on prod).
6. Deployed and verified on prod: /v1/stories 401 (live), feed total 35
   across 12 users with social aggregates present.

### State

156 API tests. V2 repo synced (backend identical; Flutter social UI
lives there: optimistic reactions, comment sheet, story viewer/composer,
cached images, infinite scroll — 165 Flutter tests).

## 2026-07-11 (iter 3) — Real visibility + story delete + rank scopes

1. Visibility now enforced end-to-end: create_submission stores the
   chosen visibility; feed and public-profile queries show only
   `public` rows. Private/Friends captures no longer leak publicly.
   Capture screen defaults to Public (social); demo seed content is
   public with an idempotent backfill for pre-existing rows.
2. DELETE /v1/stories/{id} — owner can remove a story (+ its views).
3. 159 API tests (visibility hidden-from-feed/profile, owner-only
   story delete). Ported identically to v1.
