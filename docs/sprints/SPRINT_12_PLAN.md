# Sprint 12 Plan: Async Worker Scoring

## Sprint Goal

Move scoring from synchronous HTTP handler to async worker queue. Wild submissions return immediately after precheck; a background worker processes scoring asynchronously.

## Sprint Status

**Complete.** 112 total tests all passing. Ruff and mypy clean.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S12-001 | ✅ DONE | JobQueue protocol + InMemoryJobQueue with process_pending() | Queue singleton with enqueue/dequeue/process_pending | `tests/test_submission.py` calls `_process_pending()` |
| S12-002 | ✅ DONE | ScoringWorker — polls queue, runs AIScoringService, stores ScoreEvent in DB | Worker creates own DB session, evaluates, writes score event, closes session | `services/api/src/infrastructure/worker/scoring_worker.py` |
| S12-003 | ✅ DONE | Async submission flow | POST /v1/submissions enqueues for wild; capped paths sync | `routes.py` — ai_evaluated→enqueue, capped→sync |
| S12-004 | ✅ DONE | Background worker thread in FastAPI lifespan | Daemon thread polls queue every 500ms | `main.py` lifespan handler |
| S12-005 | ✅ DONE | Tests updated | Wild: POST→process_pending→GET(verified) | All 112 tests pass |

## Architecture

```
POST /v1/submissions (wild)
  → precheck (sync)
  → enqueue("score_submission", payload)
  → return {status: "ai_evaluated", points: null}

Background thread (every 500ms):
  → dequeue job
  → SessionLocal()
  → AIScoringService.evaluate()
  → create_score_event()
  → session.close()

GET /v1/submissions/{id}
  → get_latest_score_event()
  → return {status: "scored", points: 25}
```

## File Ownership

| Area | Owner |
|---|---|
| `services/api/src/infrastructure/queue/` | API infrastructure |
| `services/api/src/infrastructure/worker/scoring_worker.py` | API infrastructure |
| `services/api/src/modules/submissions/api/routes.py` | API routes |
| `services/api/src/main.py` | API app factory |
| `services/api/tests/test_submission.py` | API tests |
