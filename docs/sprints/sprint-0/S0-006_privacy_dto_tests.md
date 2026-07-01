# S0-006: Add Public DTO Privacy Tests

## Goal

Add tests that fail if public schemas expose exact coordinates, private signed URLs, raw EXIF, or restricted evidence.

## Requirements

- `FR-MAP-004`
- `FR-CAP-014`
- `FR-CAP-015`
- `NFR-PRIV-001`
- `NFR-PRIV-004`

## Owned Files

- `services/api/tests/`
- `packages/contracts/`
- `tools/qa/`

## Forbidden Files

- actual map provider SDK integration.
- exact public location output.

## Acceptance Criteria

- Test names reference privacy DTO behavior.
- Tests distinguish private input location from public output cells.
- Tests run locally or exact blocker is recorded.

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `test(contracts): guard public dto privacy`.

## Commit Target

`test(contracts): guard public dto privacy`
