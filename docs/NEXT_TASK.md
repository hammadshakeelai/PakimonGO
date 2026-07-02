# Next Task

## Current Next Task

Sprint 23 — Open for implementation (see BACKLOG.md).

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprints 14-22 Complete

### Sprint 22 Complete

Sprint 22 delivered: **API versioning - v1 prefix + Accept-Version header + OpenAPI v2 placeholder.**

- Main app includes all routers with prefix="/v1"
- Version negotiation middleware: Accept-Version header → v1/v2 selection, API-Version response header
- OpenAPI has `x-versions: [v1, v2]` metadata and v2 health endpoint placeholder
- 150 total tests passing (75 API + 61 scoring-rules + 14 Flutter)