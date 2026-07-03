# Current Thinking

## Working Thesis

PakimonGO should now move from pre-code planning into Sprint 0 scaffold implementation. The repo has enough structure to avoid chaotic growth, and additional useful test work now depends on actual scaffold/code files.

## Current Baseline

- Product: 13+ real-animal discovery, capture, scoring, collections, map, social, and leaderboard app.
- Scope posture: full social target, but public/global exposure is gated.
- Mobile: Flutter direction.
- Backend: FastAPI-style modular monolith direction.
- Data: PostgreSQL/PostGIS/pgvector as canonical product state.
- Auth/integrity: Firebase Auth/App Check, Play Integrity on Android.
- Storage: object storage for originals and derivatives.
- AI: hybrid evidence pipeline, not LLM-only scoring.
- Safety: no rewards for unsafe animal interaction; no exact public animal pins.

## Important Process Decisions

- Short-burst semantic commits are required for implementation work.
- AI-authored commits must include agent/time/work-package/requirements/process-doc trailers.
- Full visible conversations or summaries should be archived in `docs/conversation-archive/` when they change direction or they change direction or decisions.
- Empty scaffold folders use `.gitkeep` so future agents see intended module boundaries.
- The external Software Engineering methodology is now a required artifact chain.
- `docs/TRACEABILITY_MATRIX.md` is the current source for requirement-to-test mapping.
- ADR review is complete: 17 ADRs accepted or revised, zero deferred.
- Data dictionary and Sprint 0 plan are the current rails for first migrations/toolchain work.
- Pre-code QA is operationalized with focused specs.
- The test layer has concrete catalogue, BDD acceptance scenarios, API examples, JSON fixtures, failure-mode matrix, release gates, JSON syntax validator, secret scanner, and GitHub Actions docs workflow.

## Current Implementation Posture

**Sprint 28 — Connect Flutter mobile to API (complete).**

Sprint 28 delivered:
- `ApiClient` HTTP wrapper with auth, GET/POST/PATCH/putFile
- 6 API response models with `fromJson`
- `CaptureRepository` with 8 API methods
- `CaptureScreen` with species/context/caption fields, upload→submit flow
- `main.dart` HomeScreen with bottom nav (Map + Capture tabs)
- 10 new Flutter unit tests + 2 widget tests for capture screen
- 27 Flutter tests total, all passing
- 89 API tests + 61 scoring-rules + 27 Flutter = **177 total tests, all passing**

**Sprint 29 — Camera plugin integration (complete).**

Sprint 29 delivered:
- `CaptureMediaService` abstract interface with `pickFromCamera()` / `pickFromGallery()`
- `ImagePickerService` real implementation using `image_picker` plugin
- `CaptureScreen` two-phase flow: Camera/Gallery buttons → image preview → form → submit
- Broken image fallback via `errorBuilder` for invalid/missing image data
- 4 new widget tests (form rendering, camera pick, gallery pick, submit button state)
- 29 Flutter tests total, all passing
- 89 API tests + 61 scoring-rules + 29 Flutter = **179 total tests, all passing**

**Sprint 30 — Auth/onboarding UI (complete).**

Sprint 30 delivered:
- `AuthService` ChangeNotifier: loginWithUserId/loginWithToken/logout/isAuthenticated
- `ApiClient` dynamic token provider pattern (`String Function()`)
- `LoginScreen` with user ID entry + token paste mode + Sign In button + getProfile verification
- `AuthGate` routing: shows login when unauthenticated, home after auth; logout button in app bar
- 13 new tests (8 AuthService unit + 5 LoginScreen widget)
- 42 Flutter tests total, all passing
- 89 API tests + 61 scoring-rules + 42 Flutter = **192 total tests, all passing**

**Sprint 34 — Pull-to-refresh on map (complete).**

Sprint 34 delivered:
- MapScreen body wrapped in `RefreshIndicator` + `SingleChildScrollView` with `AlwaysScrollableScrollPhysics`
- Pull-to-refresh triggers `_viewModel.fetchMarkers()` for all states (loading, error, no-token, map)
- 2 new widget tests (RefreshIndicator presence + pull-gesture triggers fetch)
- 89 API tests + 61 scoring-rules + 69 Flutter = **219 total tests, all passing**

**Sprint 35 — Submission history screen (complete).**

Sprint 35 delivered:
- Backend: `realName` + `animalContext` fields in `_build_submission_response`
- Flutter: `SubmissionHistoryViewModel` ChangeNotifier + `SubmissionHistoryScreen` with species, points, status list
- Tap a submission → `SpeciesDetailScreen` via `toMarker()` conversion
- History tab in bottom nav (Map / Capture / History)
- 9 new Flutter tests (5 viewmodel + 4 widget)
- 89 API tests + 61 scoring-rules + 78 Flutter = **228 total tests, all passing**

**Sprint 36 — Photo thumbnail in species detail (complete).**

Sprint 36 delivered:
- `mediaAssetId` added to `SubmissionMarker` model
- `SpeciesDetailScreen` shows `Image.network()` with thumbnail via `/v1/media/files/thumbs/{id}.jpg`
- Loading/error fallback states for thumbnail image
- All SubmissionMarker constructors updated across 4 test files
- 89 API tests + 61 scoring-rules + 78 Flutter = **228 total tests, all passing**

**Sprint 37 — Map marker clustering (complete).**

Sprint 37 delivered:
- `ClusterMarker` model + `ClusterService` utility (haversine distance-based, 2km default radius)
- `MapViewModel` exposes `clusters`/`clusterCount`; clusters built when markers > 3
- `MapScreen` overlay shows "X clusters · Y sightings" when clustered
- 8 new tests (6 cluster service + 2 viewmodel)
- 89 API tests + 61 scoring-rules + 86 Flutter = **236 total tests, all passing**

**Sprint 38 — CI workflow update (complete).**

Sprint 38 delivered:
- `needs:` dependency chain (docs → lint → test → integration → summary)
- Flutter version broadened from `3.38.x` to `3.x`
- Test count echo steps in API, scoring-rules, and Flutter jobs
- `all-checks-pass` summary job
- 89 API tests + 61 scoring-rules + 86 Flutter = **236 total tests**

**Sprint 39 — API error handling middleware (complete).**

Sprint 39 delivered:
- `ErrorHandlingMiddleware` + `http_exception_handler`
- Structured JSON responses: `{"error": {"code": "...", "message": "...", "details": {}}}`
- 8 new tests; 97 API + 61 scoring-rules = 158 Python tests
- 244 total tests (97 API + 61 scoring-rules + 86 Flutter)

**Sprint 40 — User notifications (backend) (complete).**

Sprint 40 delivered:
- Notification model + migration 002 + repository
- GET/PATCH notifications endpoints
- Notifications scored in both sync and async scoring paths
- 6 new tests; 103 API + 61 scoring-rules = 164 Python tests, 250 total

**Sprint 41 — Flutter notification center (complete).**

Sprint 41 delivered:
- NotificationModel + repository methods + NotificationViewModel
- NotificationScreen (loading/empty/error/list) with pull-to-refresh + tap-to-mark-read
- Bell icon with unread badge in HomeScreen app bar
- 8 new Flutter tests; 103 API + 61 scoring-rules + 94 Flutter = 258 total

**Sprint 42 — Flutter leaderboard screen (complete).**

Sprint 42 delivered:
- LeaderboardEntry model + LeaderboardViewModel + LeaderboardScreen
- 4th bottom nav tab with rank/scores display
- 8 new Flutter tests; 103 API + 61 scoring-rules + 102 Flutter = 266 total

**Sprint 43 — Production deployment CI/CD (complete).**

Sprint 43 delivered:
- `/health/ready` now verifies DB connectivity via `SELECT 1` (returns 503 on failure)
- `gunicorn.conf.py` — 4 uvicorn workers, 120s timeout, stdout access log
- `Dockerfile` — multi-stage build (Python 3.13-slim), HEALTHCHECK, gunicorn CMD
- `render.yaml` — Render Infrastructure as Code (web service + PostgreSQL, free plan)
- `.github/workflows/deploy.yml` — manual-trigger deploy via Render API
- README updated: deploy section + endpoint table + test count refresh
- 103 API + 61 scoring-rules + 102 Flutter = **266 total tests**, all passing

Next: Sprint 44 — further Flutter features (see BACKLOG.md).