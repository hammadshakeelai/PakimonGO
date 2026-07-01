# QA Fixture Payloads

## Purpose

These JSON fixtures are planning fixtures for future unit, contract, and integration tests. They contain dummy data only.

## Fixtures

- `public_post_dto.json`: safe public post shape.
- `private_submission_dto.json`: authenticated owner/private shape with exact location.
- `map_activity_cell_dto.json`: privacy-safe map cell.
- `score_event.json`: immutable score event shape.
- `upload_intent.json`: scoped upload intent shape.
- `duplicate_edge.json`: duplicate graph edge.
- `zoo_geofence_decision.json`: zoo/captive eligibility decision.
- `bad_public_location_leak_example.json`: negative fixture that privacy tests must reject.

## Test Rule

Public DTO tests should recursively fail on forbidden public fields such as exact coordinates, original storage paths, raw EXIF, moderator evidence, or private signed URLs.
