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
- `docs/TRACEABILITY_MATRIX.md` is the current source for requirement-to-test planning.
- ADR review is complete enough to begin Sprint 0: 13 accepted, 1 revised, 2 deferred.
- Data dictionary and Sprint 0 plan are the current rails for first migrations/toolchain work.
- Toolchain readiness is checked: Flutter doctor passes, Python is available, and docs validation scripts pass.
- Sprint 0 tasks are now split into individual agent packets.
- Pre-code QA is now operationalized with focused specs for requirement-to-test coverage, Sprint 0 validation, privacy contracts, scoring state, goldsets, zoo/duplicate benchmarks, Android QA, security checks, CI gates, and ready/done rules.
- The test layer now has a concrete catalogue, BDD acceptance scenarios, API examples, JSON fixtures, failure-mode matrix, release gates, a JSON syntax validator, secret scanner, and GitHub Actions docs workflow.
- Final pre-code governance now includes ADR-017 test tooling standards, test harness architecture, coverage/flaky policy, local PR checklist, architecture fitness rules, CODEOWNERS, PR/issue templates, reusable docs templates, and a pre-code completion audit.

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

Sprint 0 scaffold work should start now with S0-001 or S0-002. Additional real test artifacts should be created alongside scaffold code. Public/social/map-provider-specific implementation should still wait until the relevant deferred decisions and gates are resolved.
