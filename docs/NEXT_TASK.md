# Next Task

## Current Next Task

Sprint 20 — Sensitive species handling in collection/leaderboard or API versioning.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-19 Complete

### Sprint 19 Complete

Sprint 19 delivered: **Sensitive species location suppression**.

- `SensitiveSpecies` model: scientific_name (unique), common_name, suppression_level, reason
- Repository: `is_sensitive_species`, `get_or_create_sensitive_species`, `create_sensitive_species`
- Response suppression: sensitive species get `cellId="cell_suppressed"`, `precisionLabel="suppressed"`, `suppressedReason="sensitive_species"`
- 4 tests: detection, suppression, normal cell, create response
- 65 API tests + 61 scoring-rules + 14 Flutter = **140 total tests, all passing**

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
- **Sensitive species in collection/leaderboard** — exclude or flag sensitive species in public listings
- **API versioning** — v1/v2 strategy for breaking changes