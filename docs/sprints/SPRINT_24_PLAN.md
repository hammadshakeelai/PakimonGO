# Sprint 24 Plan: Real Storage and AI Integration

## Sprint Goal

Wire real cloud storage (S3/GCS) for media and connect real AI provider with actual API calls. This sprint moves from stubs to functional backends.

## Sprint Status

Planned.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S24-001 | Pending | Real storage adapter for S3/GCS | Media upload stores to cloud, derivatives generated on completion | Integration test with bucket |
| S24-002 | Pending | AI provider with real API key | Submission triggers actual vision API call | End-to-end test with real key |
| S24-003 | Pending | Environment configuration | VISION_PROVIDER, STORAGE_BASE_URL env vars documented | .env.example updated |
| S24-004 | Pending | File cleanup/rotation | Old uploads cleaned, derivative retention policy | Cleanup runs on schedule |
| S24-005 | Pending | Tests for real integrations | Secrets not committed, tests pass in CI | CI job configured |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/src/infrastructure/storage/` | Backend agent | Cloud storage adapter |
| `services/api/src/infrastructure/ai/` | Backend agent | AI provider configuration |
| `docs/` | Lead agent | Environment docs |