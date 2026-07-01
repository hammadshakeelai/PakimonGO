# Next Task

## Current Next Task

Sprint 19 — Sensitive species suppression or API versioning.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-18 Complete

### Sprint 18 Complete

Sprint 18 delivered: **OPENAPI_DRAFT.yaml update for pagination params and paginated response schemas**.

- Added 4 new schemas: Pagination, PaginatedCollectionResponse, PaginatedLeaderboardResponse, PaginatedSubmissionListResponse
- GET /v1/users/me/collection: limit (1-500), offset, context filter, sort_by, sort_order
- GET /v1/leaderboard: limit (1-500), offset, sort_by, sort_order
- GET /v1/submissions: limit (1-100), offset, status filter, sort_by, sort_order
- OPENAPI_DRAFT.yaml: 20 paths (up from 20, includes new /submissions GET), 31 schemas (up from 27)
- 136 total tests all passing

### Sprint 17 Complete

Sprint 17 delivered: **API enhancements - pagination, filtering, sorting**.

### Sprint 16 Complete

Sprint 16 delivered: **Goldset integration for precheck/zoo benchmark**.

### Sprint 15 Complete

Sprint 15 delivered: **Collection and Leaderboard Endpoints**.

### Sprint 14 Complete

Sprint 14 delivered: **Real Google Vision Provider implementation**.

Next sprint candidates:
- **Sensitive species suppression** — location suppression and policy behavior fixtures
- **API versioning** — v1/v2 strategy for breaking changes