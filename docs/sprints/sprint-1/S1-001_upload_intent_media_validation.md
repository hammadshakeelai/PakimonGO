# S1-001: Upload Intent + Media Validation

## Goal

Add upload intent creation and media validation endpoints without real cloud storage.

## Requirements

- `FR-CAP-011`
- `FR-CAP-012`
- `FR-CAP-013`
- `FR-CAP-017`
- `NFR-SEC-002`

## Owned Files

- `services/api/src/modules/media/`
- `services/api/tests/`

## Forbidden Files

- real cloud storage credentials or SDK calls.
- AI provider calls.
- final score formula.

## Acceptance Criteria

- POST `/v1/media/upload-intent` accepts fileName/contentType/byteSize/sha256, returns mediaAssetId + placeholder upload URL.
- POST `/v1/media/complete-upload` accepts sha256, transitions intent to ready.
- Media validation rejects oversized files, unsupported content types.
- All responses are privacy-safe (no device IDs, exact locations, signed URLs with real domains).
- In-memory storage only; no database.

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `feat(media): add upload intent + validation`.

## Commit Target

`feat(media): add upload intent + validation`
