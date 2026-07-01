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
- Pre-code QA is operationalized with focused specs for requirement-to-test coverage, Sprint 0 validation, privacy contracts, scoring state, goldsets, zoo/duplicate benchmarks, Android QA, security checks, CI gates, and ready/done rules.
- The test layer has concrete catalogue, BDD acceptance scenarios, API examples, JSON fixtures, failure-mode matrix, release gates, JSON syntax validator, secret scanner, and GitHub Actions docs workflow.
- ADR-017 test tooling standards, test harness architecture, coverage/flaky policy, local PR checklist, architecture fitness rules, CODEOWNERS, PR/issue templates, reusable docs templates, and pre-code completion audit in place.

## Internal Debate Log

### Scaffold now vs. wait for every ADR

- Waiting for every ADR would keep architecture cleaner but slow down repo organization.
- Scaffold-only folders and READMEs are low-risk and help future ADR work map to modules.
- Current winner: scaffold directories now, but do not add production feature code until ADR/work-package readiness.

### Store full conversations vs. purified summaries

- Full conversations preserve original nuance and user corrections.
- Summaries are easier for future agents to read.
- Current winner: support both. Use raw copy-paste files for full chat exports and summaries for fast handoff.

## Current Implementation Posture

**Sprint 14 is complete.**

Sprint 14 delivered:
- GoogleVisionProvider with real REST API (base64 encode, POST, label/object annotation parsing)
- Context classification: zoo/pet keywords → "zoo"/"pet", else "wild"/"unknown"
- 6 mock API tests covering zoo, wild, pet, empty, error, file-not-found
- `requests` dependency added to requirements.txt

Sprint 0-14 stats:
- 103 Python tests + 14 Flutter tests = 117 total
- 11 real endpoints + 8 planned in OpenAPI
- 7 GitHub Actions CI jobs
- All 17 ADRs accepted or revised

Next: Sprint 15 — Collection/leaderboard endpoints or scoring history.
