# Next Task

## Current Next Task

Sprint 18 — OPENAPI_DRAFT.yaml update for pagination params + sensitive species suppression.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-17 Complete

### Sprint 17 Complete

- `GET /v1/users/me/collection` — `limit` (1-500), `offset`, `context` filter, `sort_by` (totalPoints/species/captureCount/lastCaptured), `sort_order` (asc/desc)
- `GET /v1/leaderboard` — `limit` (1-500), `offset`, `sort_by` (totalScore/userId/submissionCount), `sort_order` (asc/desc)
- `GET /v1/submissions` — list endpoint with `limit`, `offset`, `status` filter, `sort_by` (createdAt/submittedAt/status/points/species), `sort_order` (asc/desc)
- Repository functions updated: `get_user_collection`, `get_leaderboard`, `get_submissions` all return `(items, total)` tuples
- 7 updated tests for pagination/filtering/sorting
- 136 total tests (61 API + 61 scoring-rules + 14 Flutter) all passing

## Sprint 16 Complete

Sprint 16 delivered: **Goldset integration for precheck/zoo benchmark**.

## Sprint 15 Complete

Sprint 15 delivered: **Collection and Leaderboard Endpoints**.

## Sprint 14 Complete

Sprint 14 delivered: **Real Google Vision Provider implementation**.

Next sprint candidates:
- **OPENAPI_DRAFT.yaml update** — document new pagination/filter/sort params and response schemas
- **Sensitive species suppression** — location suppression and policy behavior fixtures