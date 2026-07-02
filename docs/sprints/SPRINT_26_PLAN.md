# Sprint 26 Plan: Wire Cloud Storage into Media Flow

## Sprint Goal

Replace the hardcoded `LocalFileStorage` dependency in media routes with the configurable `get_storage_provider()` factory, enabling S3/GCS storage in production.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S26-001 | Done | Add `generate_derivative_stubs` to StorageProvider interface | All providers implement `generate_derivative_stubs()` | Interface method exists on StorageProvider, S3StorageProvider, GCSStorageProvider |
| S26-002 | Wire `get_storage_provider()` into media routes | Routes use factory instead of hardcoded LocalFileStorage | All 89 API tests pass with local provider default |
| S26-003 | Done | Cloud storage integration tests | Factory, S3/GCS URL formats, media upload roundtrip | 8 cloud storage tests pass |
| S26-004 | Done | Sprint 26 plan + state docs | All docs updated | validate_docs, pre_task_check pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/src/infrastructure/storage/cloud_storage.py` | Backend agent | StorageProvider, S3StorageProvider, GCSStorageProvider |
| `services/api/src/modules/media/api/routes.py` | Backend agent | Uses get_storage_provider() |
| `services/api/tests/test_cloud_storage.py` | Backend agent | Factory, S3/GCS URL, media roundtrip tests |
