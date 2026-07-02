# Sprint 28 Plan: Connect Flutter Mobile to API

## Sprint Goal

Wire the Flutter mobile app to the FastAPI backend so mobile users can upload photos, submit captures, and view results — all via real HTTP calls.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S28-001 | Done | Add `http` package to pubspec.yaml | `http: ^1.6.0` in dependencies | `flutter pub get` succeeds |
| S28-002 | Done | Create `ApiClient` HTTP wrapper | Base URL, auth token, GET/POST/PATCH/putFile, ApiException | 5 mock HTTP tests pass |
| S28-003 | Done | Create `ApiConfig` env-var reader | `--dart-define` vars for API_URL and AUTH_TOKEN | Config returns correct defaults |
| S28-004 | Done | Create API response models | 6 fromJson models: UploadIntentResponse, CompleteUploadResponse, DerivativeUrls, ScoreState, SubmissionResponse, UserProfileResponse | Models parse fixture JSON |
| S28-005 | Done | Create `CaptureRepository` | createUploadIntent, uploadFile, completeUpload, createSubmission, getSubmission, getProfile, getCollection, getLeaderboard | 5 mock repository tests pass |
| S28-006 | Done | Build `CaptureScreen` UI | Species/context/caption fields, dropdown, submit button, status + result cards | Widget renders on device |
| S28-007 | Done | Update `main.dart` with tab nav | HomeScreen with bottom nav (Map + Capture) | Widget test confirms nav works |
| S28-008 | Done | Write `ApiClient` unit tests | 5 tests: GET, POST, 404 error, 400 with detail, GET without auth | All 5 pass |
| S28-009 | Done | Write `CaptureRepository` unit tests | 5 tests: uploadIntent, completeUpload, createSubmission, getProfile, error handling | All 5 pass |
| S28-010 | Done | Write `CaptureScreen` widget tests | 2 tests: renders form fields, submit button triggers flow | Both pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/core/network/api_client.dart` | Mobile agent | HTTP wrapper |
| `lib/core/network/api_config.dart` | Mobile agent | Env-var reader |
| `lib/shared/models/api_models.dart` | Mobile agent | Response DTOs |
| `lib/features/capture/data/capture_repository.dart` | Mobile agent | API methods |
| `lib/features/capture/presentation/capture_screen.dart` | Mobile agent | Capture UI |
| `lib/main.dart` | Mobile agent | Tab navigation |
| `test/features/capture/` | Mobile agent | All tests |
