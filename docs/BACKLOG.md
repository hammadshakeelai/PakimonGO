# Backlog

## Intake

New ideas must be added here before implementation. Each item should later become an issue, story, or ADR.

## Product Backlog

- Define MVP animal capture flow.
- Define scoring formula and point economy.
- Define animal rarity taxonomy and source of truth.
- Define duplicate detection thresholds for same animal, same species, same owner pet, and changed appearance.
- Define zoo detection using geofences, Places/OSM data, user disclosure, and review.
- Define anti-spam and negative-point rules.
- Define catch-up mechanics so new and low-score users can progress.
- Define private/public/friends-only visibility and post sharing rules.
- Define groups, collections, hashtags, comments, likes, reposts, and captions.
- Define pet owner tagging and shared credit.
- Define four leaderboard scopes: global, country, local, and friends.
- Define map layers for recent animals, species density, hotspots, and privacy-blurred points.
- Define waypoint routing behavior.
- Define contacts import, friend matching, invites, blocking, and reporting.
- Define moderation queues and appeal flows.

## Engineering Backlog

- ~~S31-001: Add shared_preferences dependency~~ ✅ DONE
- ~~S31-002: Create DraftPersistenceService interface + SharedPrefsDraftStorage~~ ✅ DONE
- ~~S31-003: Update CaptureDraftService for persistence~~ ✅ DONE
- ~~S31-005: Update tests + write new persistence tests~~ ✅ DONE
- ~~S30-001: Create AuthService (token storage/retrieval)~~ ✅ DONE
- ~~S30-002: Update ApiClient to use dynamic token provider~~ ✅ DONE
- ~~S30-003: Create LoginScreen UI~~ ✅ DONE
- ~~S30-004: Create AuthGate + update main.dart routing~~ ✅ DONE
- ~~S30-005: Write tests for auth flow~~ ✅ DONE
- ~~S29-001: Add image_picker dependency to pubspec.yaml~~ ✅ DONE
- ~~S29-002: Create CaptureMediaService interface + ImagePickerService~~ ✅ DONE
- ~~S29-003: Update CaptureScreen with camera/gallery buttons~~ ✅ DONE
- ~~S29-004: Write tests for camera integration~~ ✅ DONE
- ~~S28-001: Add `http` package to pubspec.yaml~~ ✅ DONE
- ~~S28-002: Create `ApiClient` HTTP wrapper~~ ✅ DONE
- ~~S28-003: Create `ApiConfig` env-var reader~~ ✅ DONE
- ~~S28-004: Create API response models~~ ✅ DONE
- ~~S28-005: Create `CaptureRepository`~~ ✅ DONE
- ~~S28-006: Build `CaptureScreen` UI~~ ✅ DONE
- ~~S28-007: Update `main.dart` with tab nav~~ ✅ DONE
- ~~S28-008: Write `ApiClient` unit tests~~ ✅ DONE
- ~~S28-009: Write `CaptureRepository` unit tests~~ ✅ DONE
- ~~S28-010: Write `CaptureScreen` widget tests~~ ✅ DONE

- ~~S35-001: Backend: add realName + animalContext to response~~ ✅ DONE
- ~~S35-002: Flutter: update SubmissionResponse model~~ ✅ DONE
- ~~S35-003: Flutter: add getSubmissions() to CaptureRepository~~ ✅ DONE
- ~~S35-004: Flutter: create SubmissionHistoryViewModel~~ ✅ DONE
- ~~S35-005: Flutter: create SubmissionHistoryScreen~~ ✅ DONE
- ~~S35-006: Flutter: wire History tab in main.dart~~ ✅ DONE
- ~~S35-007: Tests for submission history~~ ✅ DONE
- ~~S36-001: Photo thumbnail in species detail screen~~ ✅ DONE
- ~~S37-001: Map marker clustering~~ ✅ DONE
- S38-001: CI workflow update for new Flutter test count or API error handling middleware
- ~~S0-001: Generate Flutter project template~~ ✅ DONE
- ~~S0-002: Implement FastAPI project scaffold~~ ✅ DONE
- ~~S0-006: Privacy DTO tests~~ ✅ DONE
- ~~S0-007: Score state model/tests~~ ✅ DONE
- ~~S0-008: Capture draft model~~ ✅ DONE
- ~~S0-009: Extend CI pipeline~~ ✅ DONE
- ~~S1-001: Upload intent DTO and validation~~ ✅ DONE
- ~~S1-002: Submission DTO and create endpoint~~ ✅ DONE
- ~~S1-003: Derivative stub response DTO~~ ✅ DONE
- ~~S1-004: Health endpoint + CI coverage~~ ✅ DONE
- ~~S2-001: Core DB models + Alembic~~ ✅ DONE
- ~~S2-002: Wire DB into services~~ ✅ DONE
- ~~S3-001: Auth adapter + dependency~~ ✅ DONE
- ~~S3-002: Protect media routes~~ ✅ DONE
- ~~S3-003: Protect submission routes~~ ✅ DONE
- ~~S5-001: User repository~~ ✅ DONE
- ~~S5-002: GET /v1/users/me~~ ✅ DONE
- ~~S5-003: PATCH /v1/users/me~~ ✅ DONE
- ~~S6-001: Precheck service~~ ✅ DONE
- ~~S6-002: Wire into submission flow~~ ✅ DONE
- ~~S6-003: Package + API tests~~ ✅ DONE
- ~~S7-001: Inventory all real endpoints~~ ✅ DONE
- ~~S7-002: Rewrite OPENAPI_DRAFT.yaml~~ ✅ DONE
- ~~S7-003: Update API examples~~ ✅ DONE
- ~~S8-001: Ruff config + linting fixes~~ ✅ DONE
- ~~S8-002: Mypy config + type fixes~~ ✅ DONE
- ~~S8-003: CI workflow update~~ ✅ DONE
- ~~S9-001: Scoring service contract + stub~~ ✅ DONE
- ~~S9-002: Repository functions~~ ✅ DONE
- ~~S9-003: Wire scoring into submission flow~~ ✅ DONE
- ~~S9-004: Tests~~ ✅ DONE
- ~~S10-001: Review ADR-003~~ ✅ DONE
- ~~S10-002: Review ADR-015~~ ✅ DONE
- ~~S10-003: Update ADR review pack~~ ✅ DONE
- ~~S11-001: VisionProvider protocol~~ ✅ DONE
- ~~S11-002: AIScoringService~~ ✅ DONE
- ~~S11-003: DummyVisionProvider~~ ✅ DONE
- ~~S11-004: GoogleVisionProvider placeholder~~ ✅ DONE
- ~~S11-005: Wire into routes~~ ✅ DONE
- ~~S11-006: Tests~~ ✅ DONE
- ~~S12-001: JobQueue protocol~~ ✅ DONE
- ~~S12-002: ScoringWorker~~ ✅ DONE
- ~~S12-003: Async submission flow~~ ✅ DONE
- ~~S12-004: Background worker thread~~ ✅ DONE
- ~~S12-005: Tests~~ ✅ DONE
- ~~S13-001: Mapbox dependency~~ ✅ DONE
- ~~S13-002: AppConfig token setup~~ ✅ DONE
- ~~S13-003: MapScreen widget~~ ✅ DONE
- ~~S13-004: Update main.dart~~ ✅ DONE
- ~~S13-005: Widget tests~~ ✅ DONE
- Create database schema and migrations.
- Create object storage layout for originals, thumbnails, and AI crops.
- Create AI scoring service contract with structured outputs.
- Create duplicate matching benchmark dataset.
- Create zoo/geofence test dataset.
- Create local development environment using Docker Compose.
- Add future ADRs for final map provider, migration tooling, scoring formula, and production deployment when those decisions become implementation blockers.
- Prototype Flutter camera plus foreground location on Android.
- Prototype Mapbox and Google Maps map UX/cost/legal constraints.
- Prototype AI scoring schema on a small licensed/local image set.
- Build first duplicate/zoo gold dataset.
- Implement benchmark runners from `docs/qa/ZOO_DUPLICATE_BENCHMARK_SPEC.md` once fixture manifests exist.
- Convert `docs/qa/TEST_CASE_CATALOGUE.md` into module-local automated tests as code appears.
- Convert `docs/qa/BDD_ACCEPTANCE_SCENARIOS.md` into E2E/manual acceptance suites after runnable flows exist.
- Validate API examples against generated OpenAPI schemas once contract tooling exists.

## Process Backlog

- Expand templates only when a real process gap appears during implementation.
- Add Graphify generation workflow after first code exists.
- Extend docs lint and link-check workflow if Markdown formatting rules become necessary.
- Make `.github/workflows/docs-validation.yml` a required branch check once repository settings are configured.
- Add max-file-size warning workflow once code exists.
- Add full visible conversation text to `docs/conversation-archive/raw/FULL_CONVERSATION_COPY_PASTE_HERE.txt` after user pastes export.
- Add OpenAPI linting and schema consistency checks.
- Add a generated final Software Engineering report after artifacts are accepted.
