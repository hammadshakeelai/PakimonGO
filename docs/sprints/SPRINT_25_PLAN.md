# Sprint 25 Plan: Integration Testing and Documentation

## Sprint Goal

Create integration tests for the full capture flow and improve documentation for production readiness.

## Sprint Status

**Complete.**

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S25-001 | Done | Integration test: end-to-end capture flow | Upload → submit → score → collection | 6 tests pass (wild, zoo, duplicate, multiuser, list, health) |
| S25-002 | Done | Add API endpoint documentation | All endpoints have docstrings | Docstrings added to all 14 endpoints |
| S25-003 | Done | Update README.md | Build/run instructions | README reflects current state |
| S25-004 | Done | Add OpenAPI schema validation | Schema validates against examples | validate_docs: openapi_examples PASS (15 examples) |
| S25-005 | Done | Add CI job for integration tests | Job runs in CI | integration-tests job added (9 total jobs) |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/tests/` | Backend agent | Integration tests |
| `docs/` | Lead agent | Documentation updates |