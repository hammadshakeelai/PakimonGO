# Next Task

## Current Next Task

Sprint 16 — Real data integration (zoo flag, golden set) or API enhancements.

## Sprint 2-13 Complete

Sprints 2-13 delivered: DB-backed services, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI update, CI expansion, AI scoring, ADR review, AI adapter framework, async worker scoring, and Mapbox prototype. 112 Python + 14 Flutter tests all passing.

## Sprint 14-15 Complete

Sprint 15 delivered: **Collection and Leaderboard Endpoints**.

- `GET /v1/users/me/collection` — returns species grouped by real_name with total points, capture count, last captured
- `GET /v1/leaderboard` — returns top scorers ordered by total points (public, `limit` param, 1-500)
- Repository queries: `get_user_collection`, `get_leaderboard` using `func.sum` + joins
- 7 new tests covering collection (species, empty, auth) and leaderboard (entries, public, limit, invalid)
- OpenAPI updated: 2 new paths, 4 new schemas (CollectionResponse, CollectionEntry, LeaderboardResponse, LeaderboardEntry)
- 61 total API tests + 49 scoring-rules + 14 Flutter = **124 total tests, all passing**

## Sprint 14 Complete

Sprint 14 delivered: **Real Google Vision Provider implementation**.

- Replaced placeholder with actual REST API calls to `vision.googleapis.com/v1/images:annotate`
- Parses label annotations + localized object annotations → detects species, confidence, context
- Context classification: zoo keywords → "zoo", pet keywords → "pet", else "wild" (or "unknown" if no labels)
- Mock-tested 6 scenarios: zoo, wild, pet, empty response, error/HTTP error, file-not-found
- 49 scoring-rules tests + 54 API tests = 103 Python + 14 Flutter = **117 total tests, all passing**

Next sprint candidates:
- **Real data integration (zoo flag, golden set)** — integrate goldset fixtures for precheck/duplicate testing
- **API enhancements** — pagination, filtering, sorting for existing endpoints
