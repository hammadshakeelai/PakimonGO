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
- Full visible conversations or summaries should be archived in `docs/conversation-archive/` when they change direction or decisions.
- Empty scaffold folders use `.gitkeep` so future agents see intended module boundaries.
- The external Software Engineering methodology is now a required artifact chain.
- `docs/TRACEABILITY_MATRIX.md` is the current source for requirement-to-test mapping.
- ADR review is complete: 17 ADRs accepted or revised, zero deferred.
- Data dictionary and Sprint 0 plan are the current rails for first migrations/toolchain work.
- Pre-code QA is operationalized with focused specs.
- The test layer has concrete catalogue, BDD acceptance scenarios, API examples, JSON fixtures, failure-mode matrix, release gates, JSON syntax validator, secret scanner, and GitHub Actions docs workflow.

## Current Implementation Posture

**Sprint 18 is complete.**

Sprint 18 delivered:
- OPENAPI_DRAFT.yaml updated with pagination parameters for 3 endpoints
- 4 new paginated response schemas (Pagination, PaginatedCollectionResponse, PaginatedLeaderboardResponse, PaginatedSubmissionListResponse)
- 31 total schemas (up from 27), 20 paths

Sprint 0-18 stats:
- 136 total tests (61 API + 61 scoring-rules + 14 Flutter)
- 20 real endpoints + 8 planned in OpenAPI
- 8 GitHub Actions CI jobs
- All 17 ADRs accepted or revised

Next: Sprint 19 — Sensitive species suppression or API versioning.