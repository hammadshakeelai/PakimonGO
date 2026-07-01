# Next Task

## Current Next Task

Sprint 21 — OPENAPI_DRAFT.yaml update for include_sensitive params + API versioning.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-20 Complete

### Sprint 20 Complete

Sprint 20 delivered: **Sensitive species filtering in collection/leaderboard**.

- `get_user_collection`: excludes sensitive species by default, `include_sensitive` flag
- `get_leaderboard`: excludes sensitive species submissions, `include_sensitive` flag
- `get_submissions`: filters sensitive species, `include_sensitive` param (default false)
- 6 new tests for collection/leaderboard sensitive species exclusion
- Refactored repositories into 7 modules (media_asset, submission, score_event, user, collection, submission_list, sensitive_species)
- 69 API tests + 61 scoring-rules + 14 Flutter = **144 total tests, all passing**

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
- **OPENAPI_DRAFT.yaml update** — document include_sensitive params
- **API versioning** — v1/v2 strategy for breaking changes