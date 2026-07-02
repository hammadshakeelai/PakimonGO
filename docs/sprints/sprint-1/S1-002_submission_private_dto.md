# S1-002: Submission Private DTO

## Goal

Create a private submission DTO with scoring state hook, privacy-safe response, and server-authority invariant.

## Requirements

- `FR-CAP-005`
- `FR-CAP-006`
- `FR-CAP-009`
- `FR-CAP-010`
- `FR-CAP-014`
- `FR-SCORE-002`
- `FR-SCORE-003`

## Owned Files

- `services/api/src/modules/submissions/`
- `services/api/tests/`

## Forbidden Files

- public DTO exposure (exact lat/lng, original URLs).
- final scoring formula.
- real cloud storage.

## Acceptance Criteria

- POST `/v1/submissions` accepts mediaAssetId + animalContext + names/caption/tags + private foregroundLocation.
- Response includes submissionId, scoreState (pending), visibility (private by default), publicLocation (cell placeholder).
- Response must NOT contain exact latitude/longitude.
- Server-authority invariant: client cannot set score final state.
- In-memory storage only; no database.

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `feat(submissions): add private submission dto`.

## Commit Target

`feat(submissions): add private submission dto`
