# Sprint 25 Plan: Integration Testing and Documentation

## Sprint Goal

Create integration tests for the full capture flow and improve documentation for production readiness.

## Sprint Status

Planned.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S25-001 | Pending | Integration test: end-to-end capture flow | Upload → submit → score → collection | Test passes with mock storage |
| S25-002 | Pending | Add API endpoint documentation | All endpoints have docstrings | Docs generated |
| S25-003 | Pending | Update README.md | Build/run instructions | README reflects current state |
| S25-004 | Pending | Add OpenAPI schema validation | Schema validates against examples | validate_docs passes |
| S25-005 | Pending | Add CI job for integration tests | Job runs in CI | CI passes |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/tests/` | Backend agent | Integration tests |
| `docs/` | Lead agent | Documentation updates |