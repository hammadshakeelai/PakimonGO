# Next Task

## Current Next Task

Sprint 22 continued — Version negotiation (header + URL path) + OpenAPI v2 placeholder.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-22 Complete

### Sprint 22 (in progress)

Sprint 22 delivered: **API versioning - v1 prefix added to all routes**.

- Main app includes all routers with prefix="/v1"
- All module routers updated: users (/users), leaderboard (/leaderboard), submissions (/submissions), media (/media)
- Internal paths updated: /media/upload/{id}, /media/files/thumbs|public/{id}
- 69 API tests + 61 scoring-rules + 14 Flutter = **144 total tests, all passing**

### Sprint 21 Complete

Sprint 21 delivered: **OPENAPI_DRAFT.yaml update for include_sensitive params**.

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
- **Version negotiation** — Accept-Version header + URL path negotiation
- **API v2 placeholder** — OpenAPI spec for future breaking changes