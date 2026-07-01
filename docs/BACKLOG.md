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

- Generate Flutter project template and lock exact package structure during S0-001.
- Implement FastAPI project scaffold using ADR-007 and ADR-017 standards.
- Create database schema and migrations.
- Create object storage layout for originals, thumbnails, and AI crops.
- Create AI scoring service contract with structured outputs.
- Create duplicate matching benchmark dataset.
- Create zoo/geofence test dataset.
- Extend CI pipeline for lint, tests, security checks, and generated docs validation after scaffold code exists.
- Create local development environment using Docker Compose.
- Add future ADRs for final map provider, migration tooling, scoring formula, and production deployment when those decisions become implementation blockers.
- Prototype Flutter camera plus foreground location on Android.
- Prototype Mapbox and Google Maps map UX/cost/legal constraints.
- Prototype AI scoring schema on a small licensed/local image set.
- Build first duplicate/zoo gold dataset.
- Implement tests from `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md` once public DTO schemas exist.
- Implement tests from `docs/qa/SCORING_STATE_TEST_SPEC.md` once score state code exists.
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
