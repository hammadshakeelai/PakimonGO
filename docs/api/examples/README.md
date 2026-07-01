# API Example Payloads

## Purpose

These examples make the OpenAPI draft easier to test. They are not production data and must not contain real user IDs, photos, coordinates, credentials, or signed URLs.

## Files

- `create-upload-intent-request.json`
- `create-upload-intent-response.json`
- `complete-upload-request.json`
- `create-submission-request.json`
- `submission-private-response.json`
- `public-post-response.json`
- `map-activity-response.json`
- `score-detail-response.json`
- `error-validation-response.json`

## Rules

- Public examples must not include exact `latitude` or `longitude`.
- Private owner examples may include exact location only when the filename and object clearly represent an authenticated owner view.
- Signed URLs must use dummy placeholder domains and values.
- Keep examples aligned with `docs/api/OPENAPI_DRAFT.yaml` until generated examples exist.
