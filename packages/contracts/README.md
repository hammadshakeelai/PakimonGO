# Contracts Package

This package acts as the source-of-truth for shared schemas between the Flutter mobile app and the backend API.

The primary contract definition is located at `../../docs/api/OPENAPI_DRAFT.yaml`.

## Validation

To validate the OpenAPI draft, run the QA tool from the repository root:
```powershell
python tools/qa/validate_docs.py
```
