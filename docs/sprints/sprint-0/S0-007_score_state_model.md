# S0-007: Add Score State Model Shell

## Goal

Represent the score state machine without implementing the final scoring formula.

## Requirements

- `FR-SCORE-002`
- `FR-SCORE-003`
- `FR-SCORE-008`
- `NFR-SEC-001`

## Owned Files

- `packages/scoring-rules/`
- `services/api/src/modules/scoring/`
- corresponding tests

## Forbidden Files

- final point values.
- rarity formula.
- AI provider calls.
- leaderboard projection implementation.

## Acceptance Criteria

- States exist: pending, prechecked, ai_evaluated, scored, capped, review, rejected.
- Invalid transitions are testable or explicitly deferred.
- Client authority is not implied anywhere.

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `feat(scoring): add score state model`.

## Commit Target

`feat(scoring): add score state model`
