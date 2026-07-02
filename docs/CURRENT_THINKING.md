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

Next: Sprint 31 — Offline draft persistence, map markers from API, or other backlog item (see BACKLOG.md).