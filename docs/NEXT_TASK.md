# Next Task

## Current Next Task

Sprint 26 — (see BACKLOG.md for next work package).

## Sprint 2-13 Complete

### Sprint 25 Complete

Sprint 25 delivered: **Integration testing and documentation.**

- End-to-end integration tests (6 tests covering wild capture, zoo capture, duplicate detection, multiuser collection, submission list, health)
- API endpoint docstrings on all 14 endpoints
- README.md updated with build/run instructions and endpoint table
- OpenAPI schema validation (check_openapi_examples in validate_docs.py)
- CI job `integration-tests` added (9 total CI jobs)
- 84 API tests + 61 scoring-rules + 14 Flutter = **159 total tests, all passing**

### Sprint 24 Complete

Sprint 24 delivered: **Cloud storage infrastructure - StorageProvider interface with S3/GCS implementations.**

- StorageProvider class with S3StorageProvider and GCSStorageProvider
- Environment configuration (.env.example updated with STORAGE_PROVIDER, S3/GCS vars)
- Fixed derivative URLs to use /v1/media/files prefix
- 153 total tests passing (78 API + 61 scoring-rules + 14 Flutter)

### Sprint 23 Complete

Sprint 23 delivered: **Production readiness foundation — staging and committing all implementation files.**

- All Sprints 0-22 implementation files committed to repository
- 150 total tests passing (75 API + 61 scoring-rules + 14 Flutter)
- TECH_DEBT.md updated with implementation debt items
- All validations and pre-task checks pass

### Sprint 22 Complete

Sprint 22 delivered: **API versioning - v1 prefix + Accept-Version header + OpenAPI v2 placeholder.**

- Main app includes all routers with prefix="/v1"
- Version negotiation middleware: Accept-Version header → v1/v2 selection, API-Version response header
- OpenAPI has `x-versions: [v1, v2]` metadata and v2 health endpoint placeholder
- 150 total tests passing (75 API + 61 scoring-rules + 14 Flutter)