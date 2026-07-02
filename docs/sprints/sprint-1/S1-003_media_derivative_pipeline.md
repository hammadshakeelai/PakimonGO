# S1-003: Media Derivative Pipeline

## Goal

Create media derivative stubs for thumbnail URL, EXIF stripping contract, and private/public path separation — no real image processing or cloud storage.

## Requirements

- `FR-CAP-015`
- `FR-CAP-016`
- `FR-COL-008`

## Owned Files

- `services/api/src/modules/media/`
- `services/api/tests/`

## Forbidden Files

- real image processing libraries (Pillow, OpenCV, etc.).
- real cloud storage credentials.
- real pixel operations.

## Acceptance Criteria

- Derivative stub endpoint or service method generates a placeholder thumbnail URL.
- Derivative service strips EXIF in contract — marked as stripped without real pixel ops.
- Private originals are never exposed via public URL.
- Public derivatives have a separate URL namespace.
- Tests assert EXIF stripping is contractually enforced (privacy contract test).

## Verification

```powershell
python -m pytest services/api/tests
python tools/qa/validate_docs.py
```

## Rollback

Revert `feat(media): add derivative stubs`.

## Commit Target

`feat(media): add derivative stubs`
