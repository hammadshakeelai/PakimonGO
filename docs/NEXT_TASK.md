# Next Task

## Current Next Task

Sprint 22 — API versioning strategy (v1/v2) for breaking changes.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-21 Complete

### Sprint 21 Complete

Sprint 21 delivered: **OPENAPI_DRAFT.yaml update for include_sensitive params**.

- GET /v1/users/me/collection: include_sensitive param (boolean, default false)
- GET /v1/leaderboard: include_sensitive param (boolean, default false)
- GET /v1/submissions: include_sensitive param (boolean, default false)
- Fixed duplicate /submissions: path (merged POST + GET)
- 31 schemas, 20 paths
- 144 total tests (69 API + 61 scoring-rules + 14 Flutter) all passing

### Sprint 20 Complete

Sprint 20 delivered: **Sensitive species filtering in collection/leaderboard**.

### Sprint 19 Complete

Sprint 19 delivered: **Sensitive species location suppression**.

### Sprint 18 Complete

Sprint 18 delivered: **OPENAPI_DRAFT.yaml update for pagination params and paginated response schemas**.

### Sprint 17 Complete

Sprint 17 delivered: **API enhancements - pagination, filtering, sorting**.

### Sprint 16 Complete

Sprint 16 delivered: **Goldset integration for precheck/zoo benchmark**.

### Sprint 15 Complete

Sprint 15 delivered: **Collection and Leaderboard Endpoints**.

### Sprint 14 Complete

Sprint 14 delivered: **Real Google Vision Provider implementation**.

Next sprint candidates:
- **API versioning** — v1/v2 strategy for breaking changes