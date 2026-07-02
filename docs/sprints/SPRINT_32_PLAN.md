# Sprint 32 Plan: Map Markers from API

## Sprint Goal

Plot recent user submissions as markers on the Mapbox map by fetching submission locations from the API, with loading/error/marker-count states.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S32-001 | Done | Backend: add cell centroid to publicLocation | `cellLatitude`/`cellLongitude` in response (rounded to 3dp) | 89 API tests pass |
| S32-002 | Done | Create `SubmissionMarker` model | fromJson, hasValidLocation, species/points/status fields | Unit test parses mock response |
| S32-003 | Done | `CaptureRepository.getMapMarkers()` | GET /v1/submissions, parse markers, filter zero-location | 2 repository tests pass |
| S32-004 | Done | `MapViewModel` ChangeNotifier | fetchMarkers, loading/error/markerCount state | 4 unit tests pass |
| S32-005 | Done | Refactor `MapScreen` | Injectable viewModel, loading indicator, error+retry, marker count overlay | 4 widget tests pass |
| S32-006 | Done | Wire MapViewModel in `main.dart` | HomeScreen creates MapViewModel with ApiClient, passes to MapScreen | widget_test.dart passes |
| S32-007 | Done | Add relationship between Submission and CaptureLocation | `capture_location` on Submission + `submission` back-populate | 89 API tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/shared/models/submission_marker.dart` | Mobile agent | Marker model |
| `lib/features/map/domain/map_viewmodel.dart` | Mobile agent | ViewModel |
| `lib/features/map/presentation/map_screen.dart` | Mobile agent | Refactored MapScreen |
| `lib/features/capture/data/capture_repository.dart` | Mobile agent | getMapMarkers method |
| `lib/main.dart` | Mobile agent | ViewModel wiring |
| `test/features/map/` | Mobile agent | Viewmodel + screen tests |
| `test/features/capture/capture_repository_test.dart` | Mobile agent | Repository test additions |
| `services/api/src/infrastructure/database/models.py` | Backend | Submission-CaptureLocation relationship |
| `services/api/src/modules/submissions/api/routes.py` | Backend | cell centroid in response |
