# PakimonGO — Agent Context

## Identity

Full-stack wildlife discovery app (13+). Flutter mobile + FastAPI backend. 291 tests. 46 sprints. 92 commits. **Working prototype — not production-ready.**

**⚠️ WARNING: Read `docs/REMAINING_WORK.md` before adding features.** The app uses dev-only providers (FakeAuthAdapter, DummyVisionProvider, SQLite, local storage). Real security, scoring, and storage are NOT active.

## Quick Start

```powershell
.\run_local.ps1                              # API on localhost:8000 (SQLite + seed data)
cd apps/mobile/pakimon_go_app; flutter run   # Mobile app
flutter build apk --release                  # Release APK
python -m pytest services/api/tests/ -q      # 103 API tests
python -m pytest packages/scoring-rules/tests/ -q  # 61 rules tests
flutter test                                 # 125 Flutter tests
```

**Login token for dev:** `test_user_seed_user_alpha`

## Repository Map

### Backend (`services/api/src/`)

| Path | Purpose |
|------|---------|
| `main.py:45` | FastAPI app creation, middleware stack, router registration |
| `main.py:64` | `GET /health/live` |
| `main.py:70` | `GET /health/ready` (DB check) |
| `infrastructure/database/models.py` | 10 SQLAlchemy models |
| `infrastructure/database/session.py` | SQLite/Postgres session factory |
| `infrastructure/database/repositories/` | 9 repo files (DB queries) |
| `infrastructure/auth/adapter.py` | `AuthAdapter` protocol + `UserContext` dataclass |
| `infrastructure/auth/fake_adapter.py:11` | `FakeAuthAdapter` — `test_user_*` tokens |
| `infrastructure/auth/dependencies.py` | `get_current_user` FastAPI dependency |
| `infrastructure/storage/base.py:6` | `StorageProvider` interface |
| `infrastructure/storage/local_storage.py:15` | `LocalFileStorage` (dev) |
| `infrastructure/storage/cloud_storage.py` | `S3StorageProvider`, `GCSStorageProvider` |
| `infrastructure/queue/queue.py` | `InMemoryJobQueue` — async scoring |
| `infrastructure/worker/scoring_worker.py` | Background scoring worker thread |
| `infrastructure/middleware/error_middleware.py:28,41` | Error handler + middleware |
| `infrastructure/middleware/version_middleware.py` | API versioning |
| `modules/users/api/routes.py:14` | `GET /v1/users/me` |
| `modules/users/api/routes.py:36` | `GET /v1/users/me/collection` |
| `modules/users/api/routes.py:72` | `PATCH /v1/users/me` |
| `modules/submissions/api/routes.py:104` | `POST /v1/submissions` |
| `modules/submissions/api/routes.py:198` | `GET /v1/submissions/{id}` |
| `modules/submissions/api/routes.py:217` | `GET /v1/submissions` |
| `modules/media/api/routes.py:25` | `POST /v1/media/upload-intent` |
| `modules/media/api/routes.py:58` | `PUT /v1/media/upload/{id}` |
| `modules/media/api/routes.py:80` | `POST /v1/media/complete-upload` |
| `modules/media/api/routes.py:119` | `GET /v1/media/derivatives/{id}` |
| `modules/media/api/routes.py:149` | `GET /v1/media/files/{path}` |
| `modules/notifications/api/routes.py:18` | `GET /v1/notifications` |
| `modules/notifications/api/routes.py:47` | `PATCH /v1/notifications/{id}/read` |
| `modules/notifications/api/routes.py:65` | `GET /v1/notifications/unread-count` |
| `modules/leaderboard/api/routes.py:13` | `GET /v1/leaderboard` |

### Repository Functions

| File | Functions |
|------|-----------|
| `repositories/user.py` | `get_or_create_user`, `update_user` |
| `repositories/media_asset.py` | `create_media_asset`, `get_media_asset`, `update_media_asset_storage_key`, `complete_media_asset`, `get_derivatives` |
| `repositories/submission.py` | `create_submission` (returns tuple), `get_all_submission_sha256s`, `update_submission_status`, `get_submission` (returns tuple) |
| `repositories/submission_list.py` | `get_submissions` (returns `tuple[list[dict], int]`) |
| `repositories/score_event.py` | `create_score_event`, `get_latest_score_event` |
| `repositories/collection.py` | `get_user_collection`, `get_leaderboard` (both return `tuple[list[dict], int]`) |
| `repositories/notification.py` | `create_notification`, `get_notifications` (returns tuple), `mark_notification_read`, `unread_notification_count` |
| `repositories/sensitive_species.py` | `is_sensitive_species`, `get_or_create_sensitive_species`, `get_sensitive_species`, `create_sensitive_species` |

### Flutter (`apps/mobile/pakimon_go_app/lib/`)

| Path | Type | Description |
|------|------|-------------|
| `main.dart:32` | Screen | `PakimonGoApp` (root) |
| `main.dart:51` | Screen | `_AuthGate` — login vs home router |
| `main.dart:102` | Screen | `HomeScreen` — 4-tab bottom nav |
| `main.dart:116` | State | `_HomeScreenState` — creates all viewmodels |
| `features/auth/presentation/login_screen.dart` | Screen | `LoginScreen` / `_LoginScreenState` |
| `features/capture/presentation/capture_screen.dart` | Screen | `CaptureScreen` / `_CaptureScreenState` |
| `features/map/presentation/map_screen.dart` | Screen | `MapScreen` / `_MapScreenState` |
| `features/map/presentation/marker_list_screen.dart` | Screen | `MarkerListScreen` (StatelessWidget) |
| `features/species/presentation/species_detail_screen.dart` | Screen | `SpeciesDetailScreen` (StatelessWidget) |
| `features/submissions/presentation/submission_history_screen.dart` | Screen | `SubmissionHistoryScreen` |
| `features/submissions/presentation/submission_detail_screen.dart` | Screen | `SubmissionDetailScreen` |
| `features/notifications/presentation/notification_screen.dart` | Screen | `NotificationScreen` |
| `features/leaderboard/presentation/leaderboard_screen.dart` | Screen | `LeaderboardScreen` |
| `features/profile/presentation/profile_screen.dart` | Screen | `ProfileScreen` |
| `features/collection/presentation/collection_screen.dart` | Screen | `CollectionScreen` |
| `core/network/api_client.dart` | Service | `ApiClient` — GET/POST/PATCH/putFile/close |
| `core/network/api_config.dart` | Config | `ApiConfig` — baseUrl from `--dart-define` |
| `core/auth/auth_service.dart` | Service | `AuthService` — login/logout/token mgmt |
| `core/config/app_config.dart` | Config | `AppConfig` — MAPBOX_ACCESS_TOKEN |
| `features/capture/data/capture_repository.dart` | Data | All API calls: upload, submit, profile, collection, leaderboard, notifications, markers |
| `shared/models/api_models.dart` | Model | `UploadIntentResponse`, `CompleteUploadResponse`, `DerivativeUrls`, `ScoreState`, `SubmissionResponse`, `UserProfileResponse`, `NotificationModel`, `LeaderboardEntry`, `CollectionResult`, `CollectionEntry` |
| `shared/models/submission_marker.dart` | Model | `SubmissionMarker` (fromJson, hasValidLocation) |

### ViewModels

| File | Class | Key Methods |
|------|-------|-------------|
| `features/map/domain/map_viewmodel.dart` | `MapViewModel` | `fetchMarkers()`, exposes `clusters`, `markers`, `isLoading`, `error` |
| `features/map/domain/cluster_service.dart` | `ClusterService` | `static cluster(markers, {maxDistanceKm=2.0})` — haversine |
| `features/capture/domain/capture_draft.dart` | `CaptureDraftService` | `create/save/restore/delete`, persists via interface |
| `features/submissions/domain/submission_history_viewmodel.dart` | `SubmissionHistoryViewModel` | `fetchSubmissions()` |
| `features/notifications/domain/notification_viewmodel.dart` | `NotificationViewModel` | `fetchNotifications`, `fetchUnreadCount`, `markAsRead`, `getSubmissionById` |
| `features/leaderboard/domain/leaderboard_viewmodel.dart` | `LeaderboardViewModel` | `fetchLeaderboard()` |
| `features/profile/domain/profile_viewmodel.dart` | `ProfileViewModel` | `fetchProfile`, `setAgeBand`, `setHomeRegion`, `saveProfile`, `hasChanges` |
| `features/collection/domain/collection_viewmodel.dart` | `CollectionViewModel` | `fetchCollection`, `setSortBy`, `setSortOrder`, `setContextFilter`, `refresh` |

### Shared Package (`packages/scoring-rules/src/`)

| File | Purpose |
|------|---------|
| `score_state.py` | `ScoreState` enum (8 states, 14 transitions), `ScoreEvent` dataclass |
| `precheck.py` | `run_precheck()` — duplicate SHA256 + animal context rules |
| `vision_provider.py` | `VisionProvider` protocol, `AnalysisResult`, `DummyVisionProvider` |
| `scoring_service.py` | `ScoringService` protocol, `StubScoringService` (wild=25, zoo=1, pet=1, dup=0), `AIScoringService` |
| `google_vision_provider.py` | Real Google Vision REST API caller |
| `goldset_runner.py` | Manifest YAML runner for duplicate/zoo benchmarks |

## Architecture Conventions

**Route registration:** All API routers registered in `main.py:57-61` with `prefix="/v1"`. Module-level routers use bare paths (e.g. `@router.get("")`, `@router.post("")`).

**Dependency injection:** FastAPI `Depends()` pattern everywhere. DB session via `get_db`, auth via `get_current_user`, optional auth via `get_optional_user`.

**Response format (error):** `{"error": {"code": "...", "message": "...", "details": {}}}`.

**Response format (success):** Module-specific dicts, typically with `items`, `total`, `limit`, `offset` for paginated endpoints.

**DB models:** SQLAlchemy declarative base. 10 models in `models.py`. Key relationships: Submission→MediaAsset, Submission→CaptureLocation, Submission→ScoreEvent.

**Auth token format:** `test_user_{user_id}` for dev. `Bearer test_user_seed_user_alpha` in Authorization header.

**Storage:** Env var `STORAGE_PROVIDER=local|s3|gcs`. Dev uses `LocalFileStorage` at `data/uploads/`.

**Scoring flow:** POST /v1/submissions → precheck (sync) → capped paths scored sync, wild enqueued → worker thread processes async → ScoreEvent stored.

## Testing

**API:** `services/api/tests/` — 16 files, 103 tests. Uses SQLite temp DB (conftest.py). Auth header constant `AUTH_HEADER`.

**Scoring:** `packages/scoring-rules/tests/` — 5 files, 61 tests. Pure functions, no DB.

**Flutter:** `apps/mobile/pakimon_go_app/test/` — 19 files, 125 tests. Mock HTTP client pattern in all repository/viewmodel tests.

**CI:** `.github/workflows/docs-validation.yml` — 9 jobs, dependency chain, summary job.

## Critical Rules

1. **Read `docs/REMAINING_WORK.md` before proposing new features.** The app is a prototype — most features need hardening, not expansion.
2. Run `python tools/qa/pre_task_check.py` before any edit.
3. Run `python tools/qa/validate_docs.py` + `validate_json_examples.py` + `scan_secrets.py` after.
4. All 3 validation scripts must PASS before commit.
5. Update ALL state docs after every task (CURRENT_TASK, NEXT_TASK, CURRENT_THINKING, TASK_LOG, BACKLOG, BUGS_AND_RISKS, TECH_DEBT).
6. Short-burst semantic commits with AI trailers.
7. Never commit secrets/keys/credentials.
8. Source files stay ≤300 lines.
9. Read `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md` before starting work.

## What's NOT built — see `docs/REMAINING_WORK.md` for full queue

| Item | Where | What's needed |
|------|-------|---------------|
| Mapbox map | `app_config.dart` | `MAPBOX_ACCESS_TOKEN` from mapbox.com |
| Firebase Auth | `auth/adapter.py` | Firebase project + google-services.json |
| Google Vision | `google_vision_provider.py` | `GOOGLE_VISION_API_KEY` |
| Render deploy | `render.yaml` | Render account + PostgreSQL |
| Real Postgres | `session.py` | `SYNC_DATABASE_URL` connection string |
| S3/GCS storage | `cloud_storage.py` | Cloud bucket credentials |
| APK on device | — | Physical Android device or emulator |
| iOS build | — | macOS + Xcode |

## Navigation Flow (Flutter)

```
LoginScreen ──(auth success)──▶ HomeScreen (bottom nav)
                                 ├── Tab 0: MapScreen ──▶ MarkerListScreen ──▶ SpeciesDetailScreen
                                 ├── Tab 1: CaptureScreen
                                 ├── Tab 2: SubmissionHistoryScreen ──▶ SubmissionDetailScreen ──▶ SpeciesDetailScreen
                                 ├── Tab 3: LeaderboardScreen
                                 ├── AppBar bell: NotificationScreen ──▶ SubmissionDetailScreen
                                 └── AppBar person: ProfileScreen ──▶ CollectionScreen ──▶ SpeciesDetailScreen
```
