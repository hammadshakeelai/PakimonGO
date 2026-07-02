# Next Task

## Current Next Task

Sprint 37 — Map marker clustering or CI workflow update (see BACKLOG.md).

## Sprint 36 Complete

Sprint 36 delivered: **Photo thumbnail in species detail.**

- `mediaAssetId` added to `SubmissionMarker` model
- SpeciesDetailScreen now shows `Image.network()` with thumbnail from `/v1/media/files/thumbs/{id}.jpg`
- Loading state shows placeholder text "Loading photo…"; error state shows "Failed to load photo"
- All SubmissionMarker constructors across 4 test files updated
- 89 API tests + 61 scoring-rules + 78 Flutter = **228 total tests, all passing**

## Sprint 35 Complete

Sprint 35 delivered: **Submission history screen.**

- Backend: `realName` + `animalContext` added to `_build_submission_response`
- Flutter: `SubmissionResponse.toMarker()`, `CaptureRepository.getSubmissions()`, `SubmissionHistoryViewModel`
- `SubmissionHistoryScreen` with species name, points, status — tap navigates to `SpeciesDetailScreen`
- History tab in bottom nav (Map / Capture / History)
- 9 new Flutter tests (5 viewmodel + 4 screen widget)
- 89 API tests + 61 scoring-rules + 78 Flutter = **228 total tests, all passing**

## Sprint 2-26 Complete

Sprints 2-26 delivered the core API: DB-backed repositories, auth, file upload, user profiles, duplicate/zoo precheck, OpenAPI, CI, scoring pipeline, AI adapter framework, async worker, map prototype, Google Vision provider, collection/leaderboard endpoints, goldset benchmarks, pagination/filtering/sorting, sensitive species suppression, API version negotiation, and cloud storage infrastructure.

89 API tests + 61 scoring-rules + 14 Flutter = **164 total tests, all passing**.

## Sprint 2-27 Complete

### Sprint 27 Complete

Sprint 27 delivered: **Docker Compose local dev environment.**

- `services/api/Dockerfile` (Python 3.13-slim, uvicorn on 8000)
- `infrastructure/docker/docker-compose.local.yml` expanded with `api` + `db` services (health check, named volumes)
- `infrastructure/docker/.env.docker` for compose env overrides
- README updated with Docker as primary dev path
- 89 API tests + 61 scoring-rules + 14 Flutter = **164 total tests, all passing**

### Sprint 34 Complete

Sprint 34 delivered: **Pull-to-refresh on map.**

- `RefreshIndicator` + `SingleChildScrollView` wrapping MapScreen body
- Pull-to-refresh triggers `_viewModel.fetchMarkers()` in all states
- 2 new widget tests
- 89 API tests + 61 scoring-rules + 69 Flutter = **219 total tests, all passing**

### Sprint 33 Complete

Sprint 33 delivered: **Species detail screen.**

- `SpeciesDetailScreen` (species name, points, status, coordinates, photo placeholder)
- `MarkerListScreen` (tappable list → detail navigation)
- MapScreen overlay tappable with chevron
- 8 new widget tests
- 89 API tests + 61 scoring-rules + 67 Flutter = **217 total tests, all passing**

### Sprint 32 Complete

Sprint 32 delivered: **Map markers from API.**

- Backend: cell centroid in publicLocation (cellLatitude/cellLongitude)
- `SubmissionMarker` model + `CaptureRepository.getMapMarkers()`
- `MapViewModel` ChangeNotifier + `MapScreen` with loading/error/marker states
- 10 new tests (4 viewmodel + 4 screen widget + 2 repository)
- 89 API tests + 61 scoring-rules + 59 Flutter = **209 total tests, all passing**

### Sprint 31 Complete

Sprint 31 delivered: **Offline draft persistence.**

- `DraftPersistenceService` abstract interface + `SharedPrefsDraftStorage` impl
- `CaptureDraftService` now async with persistence (create/save/restore/delete persist)
- `InMemoryDraftStorage` for tests (5 new tests)
- 89 API tests + 61 scoring-rules + 49 Flutter = **199 total tests, all passing**

### Sprint 30 Complete

Sprint 30 delivered: **Auth/onboarding UI.**

- `AuthService` ChangeNotifier: loginWithUserId/loginWithToken/logout/isAuthenticated
- `ApiClient` dynamic token provider pattern (`String Function()`)
- `LoginScreen` with user ID entry + token paste modes, Sign In with getProfile verification
- `AuthGate` routing: login screen → home screen, logout button in app bar
- 13 new tests (8 AuthService + 5 LoginScreen)
- 89 API tests + 61 scoring-rules + 42 Flutter = **192 total tests, all passing**

### Sprint 29 Complete

Sprint 29 delivered: **Camera plugin integration.**

- `CaptureMediaService` abstract interface + `ImagePickerService` real impl
- `CaptureScreen` two-phase flow: Camera/Gallery buttons → preview → submit
- Broken image fallback via `errorBuilder`
- 4 new widget tests
- 89 API tests + 61 scoring-rules + 29 Flutter = **179 total tests, all passing**

### Sprint 28 Complete

Sprint 28 delivered: **Connect Flutter mobile to API.**

- `ApiClient` HTTP wrapper with auth, GET/POST/PATCH/putFile, ApiException
- 6 API response models (`fromJson`)
- `CaptureRepository` with 8 API methods
- `CaptureScreen` UI with species/context/caption fields, upload→submit flow
- `main.dart` HomeScreen with bottom nav (Map + Capture tabs)
- 10 new Flutter unit tests + 2 widget tests
- 89 API tests + 61 scoring-rules + 27 Flutter = **177 total tests, all passing**

### Sprint 26 Complete

Sprint 26 delivered: **Cloud storage wired into media flow.**

- `generate_derivative_stubs()` added to `StorageProvider` interface and both cloud implementations
- Media routes use `get_storage_provider()` factory (env-based selection: local/s3/gcs)
- 8 cloud storage tests (factory defaults, S3/GCS URL formats, ImportError checks, media roundtrip)
- 89 API tests + 61 scoring-rules + 14 Flutter = **164 total tests, all passing**

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