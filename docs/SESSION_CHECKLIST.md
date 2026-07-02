# Session Checklist

Update this after every work burst. Each row tracks one task cycle.

| # | Task | pre_task_check | State Docs Updated | Validation Pass | Commit Done | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Create pre_task_check.py | ✅ PASS | ✅ | ✅ | ❌ no commit | New file, part of safeguard system |
| 2 | Fix SPRINT_0_PLAN.md drift | ✅ PASS | ✅ | ✅ | ❌ no commit | Marked S0-001–005 complete |
| 3 | Verify S0-001–005 completeness | ✅ PASS | ✅ TASK_LOG.md | ✅ ALL PASS | ❌ no commit | All 5 completed tasks verified clean |
| 4 | Update AGENTS.md + SESSION_CHECKLIST.md | ✅ PASS | ✅ CURRENT_THINKING.md, NEXT_TASK.md, TASK_LOG.md | ✅ ALL PASS | ❌ no commit | Safeguard system complete |
| 5 | Preparing for S0-006 | ✅ PASS | ✅ CURRENT_TASK.md | ✅ | ❌ pre-code read phase | Must read priv spec + traceability first |
| 6 | S0-006 public DTO privacy tests | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 7 tests in services/api/tests/, all pass |
| 7 | S0-007 score state model | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 18 pkg tests + 17 API tests, all pass |
| 8 | S0-008 capture draft model | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 14 Flutter tests, all pass |
| 9 | S0-009 extend CI workflow | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 jobs, all non-deploy |
| 10 | S0-010 Sprint 0 closeout | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Sprint 0 complete — 59 tests, 4/4 validations |
| 11 | Sprint 1 plan + S1-001 upload intent | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 9 tests, 2 endpoints, 45 total |
| 12 | S1-002 submission private DTO | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 tests, 2 endpoints, pending state hook |
| 13 | S1-003 media derivative stubs | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 tests, EXIF strip contract, CDN URLs |
| 14 | S1-004 CI extension | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | CI auto-covers 45 tests |
| 15 | S2-001/S2-002 DB models + wire DB | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 45 API tests, SQLAlchemy + Alembic |
| 16 | Sprint 3 auth integration | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 46 API tests, auth adapter pattern |
| 17 | Sprint 4 real upload handler | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 47 API tests, LocalFileStorage, PUT upload |
| 18 | Sprint 5 user profiles | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 52 API tests, GET/PATCH /v1/users/me |
| 19 | Sprint 6 duplicate/zoo precheck | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 54 API + 26 scoring-rules = 95 total |
| 20 | Sprint 7 OpenAPI draft update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 18 paths, 23 schemas, 14 examples |
| 21 | Sprint 8 CI expansion | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | ruff 16→0, mypy 38→0, CI 5→7 jobs |
| 22 | Sprint 9 AI scoring pipeline stub | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 101 total tests, scoring wired into submissions |
| 23 | Sprint 10 deferred ADR review | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | ADR-003 + ADR-015 accepted; zero deferred remain |
| 24 | Sprint 11 AI provider adapter framework | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 112 total tests, AIScoringService wired |
| 25 | Sprint 12 async worker scoring | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 112 tests, worker thread, async scoring |
| 26 | Sprint 13 map prototype spike | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Mapbox SDK wired, MapScreen with fallback |
| 27 | Sprint 14 real Google Vision provider | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Real REST API impl, 6 mock tests, 117 total |
| 28 | Sprint 15 collection/leaderboard endpoints | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 7 tests, 61 API total, 2 new paths, 4 new schemas |
| 29 | Sprint 16 goldset integration | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 2 manifests (18 scenarios), goldset_runner, 12 tests, CI job |
| 30 | Sprint 17 API pagination/filter/sort | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 3 endpoints enhanced, 7 tests updated, 136 total tests |
| 31 | Sprint 18 OPENAPI_DRAFT.yaml update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 4 new schemas, 3 endpoints documented, 31 schemas total |
| 32 | Sprint 19 sensitive species suppression | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | SensitiveSpecies model, location suppression, 4 tests |
| 33 | Sprint 20 sensitive species filtering | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Filtering in collection/leaderboard/submissions, 6 tests, 7 repo modules |
| 34 | Sprint 21 OPENAPI_DRAFT.yaml update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | include_sensitive params, fixed duplicate path, 31 schemas |
| 35 | Sprint 22 API v1 prefix routing | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ✅ COMMIT | /v1 prefix at app level, 4 module routers updated, internal paths fixed |
| 36 | Sprint 22 API version negotiation | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | Accept-Version header, API-Version response, 6 tests, 150 total tests |
| 37 | Sprint 23 corpus staging and commits | ✅ PASS | ✅ CURRENT_TASK.md, NEXT_TASK.md | ✅ ALL PASS | ✅ COMMIT | All Sprints 0-22 files committed, 150 tests verified |
| 38 | Sprint 23 complete + state docs | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | All files staged, TECH_DEBT updated, validations pass |
| 39 | Sprint 24 cloud storage interface | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | StorageProvider interface, S3/GCS implementations, .env updated |
| 40 | Sprint 24 complete + Sprint 25 prep | ✅ PASS | ✅ CURRENT_THINKING.md, NEXT_TASK.md | ✅ ALL PASS | ❌ staging | Ready for integration testing phase |
| 41 | Sprint 25 integration tests + docs | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | 6 e2e tests, docstrings, README, validate_docs extended, CI job |
| 42 | Sprint 26 cloud storage wired into media | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | StorageProvider factory in routes, 8 tests, 164 total |
| 43 | Sprint 27 Docker Compose local dev | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | Dockerfile, compose with api+db, .env.docker, README |
| 44 | Sprint 28 Flutter API client | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | ApiClient, response models, CaptureRepository, CaptureScreen, 27 Flutter tests, 177 total |
| 45 | Sprint 29 camera plugin integration | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | CaptureMediaService, ImagePickerService, CaptureScreen two-phase flow, 29 Flutter tests, 179 total |
| 46 | Sprint 30 auth/onboarding UI | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | AuthService, ApiClient tokenProvider, LoginScreen, AuthGate routing, 42 Flutter tests, 192 total |
| 47 | Sprint 31 offline draft persistence | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | DraftPersistenceService, SharedPrefsDraftStorage, async CaptureDraftService, 49 Flutter tests, 199 total |
| 48 | Sprint 32 map markers from API | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | SubmissionMarker model, MapViewModel, MapScreen with loading/error/markers, back-end cell centroid in publicLocation, 59 Flutter tests, 209 total |
| 49 | Sprint 33 species detail screen | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | SpeciesDetailScreen, MarkerListScreen, tappable overlay → list → detail, 67 Flutter tests, 217 total |
| 50 | Sprint 34 pull-to-refresh on map | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | RefreshIndicator on MapScreen body, pull triggers fetchMarkers, 2 new tests, 69 Flutter tests, 219 total |
| 51 | Sprint 35 submission history screen | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | History tab, SubmissionHistoryScreen, 9 new Flutter tests, 78 Flutter, 228 total |
| 52 | Sprint 36 photo thumbnail in species detail | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | Image.network, mediaAssetId in SubmissionMarker, loading/error fallback, 228 total |
| 53 | Sprint 37 map marker clustering | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ staging | ClusterService, haversine clustering, overlay shows cluster count, 8 new tests, 236 total |
