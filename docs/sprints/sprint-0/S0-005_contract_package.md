# S0-005: Add Contract Package Shell

## Goal

Create the shared contract package shell and connect it to `docs/api/OPENAPI_DRAFT.yaml`.

## Requirements

- `FR-CAP-011`
- `FR-CAP-012`
- `FR-SCORE-008`
- `FR-MAP-004`
- `NFR-MAINT-003`

## Owned Files

- `packages/contracts/`
- `docs/api/OPENAPI_DRAFT.yaml`
- `tools/qa/`

## Forbidden Files

- generated clients until generator choice is recorded.
- backend route implementation.
- mobile API client implementation.

## Acceptance Criteria

- Contract package README explains source-of-truth contract file.
- OpenAPI validation command is documented.
- Package shell can later host generated or hand-maintained schemas.

## Verification

```powershell
python tools/qa/validate_docs.py
```

## Rollback

Revert `scaffold(contracts): add openapi package shell`.

## Commit Target

`scaffold(contracts): add openapi package shell`
