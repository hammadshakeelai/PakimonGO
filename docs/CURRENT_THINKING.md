# Current Thinking

## Working Thesis

PakimonGO should now move from deep planning into careful scaffold-first implementation readiness. The repo has enough structure to avoid chaotic growth, but feature coding should wait until the missing ADRs and first Alpha-0 work package are accepted.

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

Scaffold-only work is allowed. Production feature implementation should begin only after the ADR completion pack and first Alpha-0 vertical slice are defined.
