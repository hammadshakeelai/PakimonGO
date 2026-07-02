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

**Sprint 22 — API versioning complete.**

Sprint 22 delivered:
- All API routes now under /v1/ prefix via main app
- Version negotiation middleware: Accept-Version header → v1/v2 selection, API-Version response header
- Module routers: users (/users), leaderboard (/leaderboard), submissions (/submissions), media (/media)
- Internal paths updated: /media/upload/{id}, /media/files/thumbs|public/{id}
- OpenAPI has `x-versions: [v1, v2]` metadata and v2 health endpoint placeholder
- 150 total tests passing (75 API + 61 scoring-rules + 14 Flutter)

Sprint 0-22 stats:
- 150 total tests (75 API + 61 scoring-rules + 14 Flutter)
- 22 real endpoints + 8 planned in OpenAPI
- 8 GitHub Actions CI jobs
- All 17 ADRs accepted or revised

Next: Sprint 23 — Open for implementation.