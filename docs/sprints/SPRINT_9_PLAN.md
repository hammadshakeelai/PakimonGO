# Sprint 9 Plan: AI Scoring Pipeline Stub

## Sprint Goal

Add a real (stub) scoring pipeline that evaluates submissions after precheck, assigns points, stores ScoreEvents, and returns visible points in API responses.

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- Precheck runs on submission creation (sets ai_evaluated for wild, capped for zoo/pet/duplicate)
- ScoreState machine with AI_EVALUATED → SCORED transition
- ScoreEvent DB model exists
- StubScoringService returns deterministic mock scores

## In Scope

- Scoring service protocol + stub implementation in scoring-rules package
- Repository functions: create_score_event, get_latest_score_event
- Wire scoring into submission creation — runs immediately after precheck
- ScoreEvent stored in DB for every submission
- visiblePoints returned in API response
- `GET /v1/submissions/{id}` reads latest score event

## Out Of Scope

- Real AI provider integration (uses StubScoringService)
- Async scoring worker
- Scoring formula customization
- Leaderboard aggregation

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S9-001 | ✅ DONE | Scoring service contract + stub | ScoringService protocol, StubScoringService with deterministic points (wild=25, zoo=1, pet=1, dup=0) | 6 package tests pass |
| S9-002 | ✅ DONE | Repository functions | create_score_event, get_latest_score_event in repositories.py | all API tests pass |
| S9-003 | ✅ DONE | Wire scoring into submission flow | POST /v1/submissions runs scoring after precheck, returns visiblePoints | 54 API tests pass |
| S9-004 | ✅ DONE | Tests | Updated submission tests for scored state + visible points | 101 total tests pass |

## File Ownership

| Area | Owner |
|---|---|
| `packages/scoring-rules/src/scoring_service.py` | Domain agent |
| `packages/scoring-rules/tests/test_scoring_service.py` | Domain agent |
| `services/api/src/infrastructure/database/repositories.py` | Backend agent |
| `services/api/src/modules/submissions/api/routes.py` | Backend agent |
| `services/api/tests/test_submission.py` | Backend agent |

## Security

- No AI provider calls — stub only
- Scores still server-authoritative (client cannot set scores)
- All ScoreEvents logged with actor field (default "system")
