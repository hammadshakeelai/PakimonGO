# Current Thinking

## Working Thesis

PakimonGO should now move from pre-code planning into Sprint 0 scaffold implementation. The repo has enough structure to avoid chaotic growth, and additional useful test work now depends on actual scaffold/code files.

## Current Baseline

- Product: 13+ real-animal discovery, capture, scoring, collections, map, social, and leaderboard app.
- Scope posture: full social target, but public/global exposure is gated.
- Mobile: Flutter direction.
- Backend: FastAPI-style modular monolith direction.
- Data: PostgreSQL/PostGIS/pgvector as canonical product state.
- Auth/integrity: Firebase Auth/App Check, Play Integrity on Android.
- Storage: object storage for originals and derivatives.
- AI: hybrid evidence pipeline, not LLM-only scoring.
- Safety: no rewards for unsafe animal interaction; no exact public animal pins.

## Important Process Decisions

- Short-burst semantic commits are required for implementation work.
- AI-authored commits must include agent/time/work-package/requirements/process-doc trailers.
- Full visible conversations or summaries should be archived in `docs/conversation-archive/` when they change direction or they change direction or decisions.
- Empty scaffold folders use `.gitkeep` so future agents see intended module boundaries.
- The external Software Engineering methodology is now a required artifact chain.
- `docs/TRACEABILITY_MATRIX.md` is the current source for requirement-to-test mapping.
- ADR review is complete: 17 ADRs accepted or revised, zero deferred.
- Data dictionary and Sprint 0 plan are the current rails for first migrations/toolchain work.
- Pre-code QA is operationalized with focused specs.
- The test layer has concrete catalogue, BDD acceptance scenarios, API examples, JSON fixtures, failure-mode matrix, release gates, JSON syntax validator, secret scanner, and GitHub Actions docs workflow.

## Current Implementation Posture

**Sprint 28 — Connect Flutter mobile to API (complete).**

Sprint 28 delivered:
- `ApiClient` HTTP wrapper with auth, GET/POST/PATCH/putFile
- 6 API response models with `fromJson`
- `CaptureRepository` with 8 API methods
- `CaptureScreen` with species/context/caption fields, upload→submit flow
- `main.dart` HomeScreen with bottom nav (Map + Capture tabs)
- 10 new Flutter unit tests + 2 widget tests for capture screen
- 27 Flutter tests total, all passing
- 89 API tests + 61 scoring-rules + 27 Flutter = **177 total tests, all passing**

Next: Sprint 29 (see BACKLOG.md).