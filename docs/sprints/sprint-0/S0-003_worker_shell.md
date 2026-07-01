# S0-003: Scaffold Worker Shell

## Goal

Create a minimal worker shell for async media, evidence, scoring, moderation, privacy, and leaderboard jobs.

## Requirements

- `NFR-REL-002`
- `NFR-AUDIT-001`
- `NFR-MAINT-002`

## Owned Files

- `services/workers/`
- `services/workers/src/`
- `services/workers/tests/`

## Forbidden Files

- API route implementation beyond shared imports.
- real provider calls.
- final scoring formula.

## Acceptance Criteria

- Worker package imports.
- No-op runner/job registry exists.
- Job interfaces are idempotency-aware in naming/docs.
- Tests or import smoke pass.

## Verification

```powershell
python -m pytest services/workers/tests
```

## Rollback

Revert `scaffold(workers): add worker shell`.

## Commit Target

`scaffold(workers): add worker shell`
