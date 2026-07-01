# Sprint 0 Plan: Alpha-0 Toolchain And Contract Foundation

## Sprint Goal

Create the first runnable technical foundation for PakimonGO without implementing public/social/gameplay features. Sprint 0 should make the repo buildable/testable enough for WP-015, while preserving the architecture, privacy, and traceability decisions already accepted.

## Sprint Status

Planned. Not started.

Task packets are split under `docs/sprints/sprint-0/`.

Toolchain readiness snapshot: `docs/tooling/TOOLCHAIN_READINESS.md`.

## Sprint Inputs

- Accepted ADRs: ADR-001, ADR-002, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-010, ADR-011, ADR-012, ADR-013, ADR-014, ADR-016.
- Revised ADR: ADR-009, exact retention periods deferred.
- Deferred ADRs: ADR-003 final map provider, ADR-015 final production deployment.
- Work package: WP-015 Alpha-0 private capture slice.
- Contract seed: `docs/api/OPENAPI_DRAFT.yaml`.
- Data seed: `docs/data/DATA_DICTIONARY.md`.

## In Scope

- Flutter app toolchain scaffold under `apps/mobile/pakimon_go_app/`.
- FastAPI API toolchain scaffold under `services/api/`.
- Worker toolchain scaffold under `services/workers/`.
- Shared contract package shell under `packages/contracts/`.
- Local development config placeholders without secrets.
- Docs/CI validation plan wired as lightweight checks if tooling is available.
- Minimal health endpoints and empty test harnesses.
- Contract privacy tests proving public DTOs do not contain exact coordinates.

## Out Of Scope

- Full camera implementation.
- Real Firebase login.
- Real AI provider calls.
- Map provider SDK integration.
- Public feed, comments, reposts, groups, contacts import.
- Production deployment.
- Real migrations against cloud database.
- Exact scoring formula.
- Final retention/deletion jobs.

## Sprint Backlog

| ID | Task | Owned Paths | Forbidden Paths | Acceptance | Verification |
|---|---|---|---|---|---|
| S0-001 | Scaffold Flutter project shell | `apps/mobile/pakimon_go_app/` | backend/data docs except state updates | `flutter pub get` can run if Flutter is installed; app has module layout preserved | `flutter --version`, `flutter pub get`, `flutter test` if available |
| S0-002 | Scaffold FastAPI API shell | `services/api/` | mobile feature code | API has app entrypoint, `/health/live`, `/health/ready`, module package structure | `python -m pytest` or import smoke |
| S0-003 | Scaffold worker shell | `services/workers/` | API route implementation beyond queue stubs | worker package imports and has no-op job runner | import smoke/unit test |
| S0-004 | Add local development config examples | `.env.example`, `infrastructure/docker/` | real secrets, private credentials | examples list required vars with dummy values only | secret scan/manual review |
| S0-005 | Add contract package shell | `packages/contracts/` | generated clients until generator chosen | OpenAPI draft copied/referenced and schema validation target documented | OpenAPI parse/lint |
| S0-006 | Add public DTO privacy tests | `services/api/tests/`, `packages/contracts/` | production scoring logic | tests assert public DTO schemas omit exact lat/lng/private URLs | pytest or schema check |
| S0-007 | Add score state enum/model shell | `packages/scoring-rules/`, `services/api/src/modules/scoring/` | final score formula | pending/prechecked/ai_evaluated/scored/capped/review/rejected represented | unit tests |
| S0-008 | Add capture draft model shell | `apps/mobile/pakimon_go_app/lib/features/capture/` | real camera plugin flow | draft metadata model exists and references requirements | Dart unit test if Flutter available |
| S0-009 | Add CI placeholder workflow | `.github/workflows/` | deploy secrets | docs/OpenAPI/test commands described or wired as non-deploy checks | local command parity |
| S0-010 | Update traceability and state docs | `docs/` | none | current/next/thinking/task log reflect sprint start/close | git diff review |

## File Ownership

| Area | Owner Type | Notes |
|---|---|---|
| `apps/mobile/pakimon_go_app/` | Mobile agent | May scaffold Flutter app and capture model only. |
| `services/api/` | Backend agent | May scaffold FastAPI app, health endpoints, contract tests. |
| `services/workers/` | Worker agent | May scaffold no-op worker and job interfaces. |
| `packages/contracts/` | Contract agent | Owns OpenAPI/schema packaging. |
| `packages/scoring-rules/` | Domain agent | Owns score state enum only during Sprint 0. |
| `infrastructure/docker/` | DevOps agent | May add local-only Docker Compose if no secrets. |
| `docs/` | Lead agent | Owns state and traceability updates. |

## Commit Sequence

Use these short-burst commits unless the actual toolchain forces a smaller split:

1. `scaffold(mobile): add flutter shell`
2. `scaffold(api): add fastapi shell`
3. `scaffold(workers): add worker shell`
4. `scaffold(contracts): add openapi package shell`
5. `test(contracts): guard public dto privacy`
6. `feat(scoring): add score state model`
7. `feat(capture): add draft model shell`
8. `chore(dev): add local config examples`
9. `ci: add scaffold validation checks`
10. `docs(state): close sprint 0 scaffold pass`

Every AI-authored commit must include:

- `AI-Agent`
- `AI-Work-Mode`
- `AI-Commit-Time`
- `Work-Package`
- `Requirements`
- `Process-Docs-Updated`

## Acceptance Criteria

- Repo remains clean after committed sprint work.
- No production secrets or private data are introduced.
- Flutter shell is either runnable or documented as blocked by missing local Flutter SDK.
- API shell has health endpoints and import/test smoke.
- Worker shell imports and has no-op runner/job structure.
- OpenAPI draft is validated by at least a YAML parse and preferably an OpenAPI linter.
- Public DTO privacy test exists and fails if exact coordinate fields leak into public map/submission output.
- Score state model has unit coverage.
- Capture draft model has unit coverage where Flutter tooling is available.
- State docs are updated with exact tests run and blockers.

## Security And Privacy Notes

- Use dummy placeholder env values only.
- Do not call live Firebase, AI, map, or cloud storage providers in Sprint 0.
- Do not store real photos, exact locations, or credentials.
- Health endpoints must not reveal secrets or internal config.
- Contract tests must distinguish private input location DTOs from public output location cells.

## Rollback Plan

- Toolchain scaffolds can be reverted by the relevant short-burst commit.
- If a scaffold command generates oversized files, keep generated files only if required by the framework and document exceptions in `docs/TECH_DEBT.md`.
- If a package manager creates lockfiles, keep them only after deciding repo policy and noting it in `docs/PROCESS.md`.
- If local environment lacks Flutter/Python tooling, commit docs and contracts only, then record blocker in `docs/NEXT_TASK.md`.

## Definition Of Done

- All Sprint 0 tasks either complete or have explicit blockers.
- Commands/tests run are recorded.
- New code files stay small unless generated.
- `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`, `docs/TASK_LOG.md`, `docs/TECH_DEBT.md`, and `docs/conversation-archive/` are updated.
- Commit history follows `docs/COMMIT_POLICY.md`.
