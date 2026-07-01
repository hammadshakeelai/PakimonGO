# Sprint 15 Plan: Collection & Leaderboard Endpoints

## Sprint Goal

Implement user collection and global leaderboard API endpoints backed by the ScoreEvent/Submission repository queries.

## Sprint Status

**Complete.** 61 API tests + 49 scoring-rules + 14 Flutter = 124 total, all passing.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S15-001 | ✅ DONE | Repository functions: get_user_collection, get_leaderboard | Queries join Submission ↔ ScoreEvent ↔ User, aggregate by species/user | All tests pass |
| S15-002 | ✅ DONE | `GET /v1/users/me/collection` | Returns species grouped by real_name with total_points, capture_count, last_captured | Collection test passes |
| S15-003 | ✅ DONE | `GET /v1/leaderboard` | Returns users ordered by total_score descending, public endpoint, limit param (1-500) | Leaderboard test passes |
| S15-004 | ✅ DONE | 7 tests | Collection: species, empty, auth. Leaderboard: entries, public, limit, invalid limit | 7/7 pass |
| S15-005 | ✅ DONE | Update OpenAPI | 2 new paths, 4 new schemas (CollectionResponse, CollectionEntry, LeaderboardResponse, LeaderboardEntry) | Validation passes |

## API Summary

```http
GET /v1/users/me/collection
Authorization: Bearer <token>

Response:
{
  "userId": "test_user_default",
  "species": [
    {
      "species": "Aquila chrysaetos",
      "context": "wild",
      "totalPoints": 50,
      "captureCount": 2,
      "lastCaptured": "2026-07-01T..."
    }
  ]
}
```

```http
GET /v1/leaderboard?limit=100

Response:
{
  "entries": [
    {
      "userId": "user1",
      "ageBand": null,
      "homeRegion": null,
      "totalScore": 50,
      "submissionCount": 2
    }
  ],
  "totalReturned": 1
}
```

## File Ownership

| Area | Owner |
|---|---|
| `services/api/src/infrastructure/database/repositories.py` | Repository queries |
| `services/api/src/modules/users/api/routes.py` | Collection endpoint |
| `services/api/src/modules/leaderboard/api/routes.py` | Leaderboard endpoint |
| `services/api/src/main.py` | Router registration |
| `services/api/tests/test_collection_leaderboard.py` | Tests |
| `docs/api/OPENAPI_DRAFT.yaml` | API spec |
