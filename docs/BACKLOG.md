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

- Choose Flutter project template and package structure.
- Choose backend framework and API style.
- Create database schema and migrations.
- Create object storage layout for originals, thumbnails, and AI crops.
- Create AI scoring service contract with structured outputs.
- Create duplicate matching benchmark dataset.
- Create zoo/geofence test dataset.
- Create CI pipeline for lint, tests, security checks, and generated docs validation.
- Create local development environment using Docker Compose.
- Create ADRs for platform, database, maps, AI scoring, auth, and storage.
- Create ADRs for backend framework, moderation platform, deployment, analytics, and release process.
- Prototype Flutter camera plus foreground location on Android.
- Prototype Mapbox and Google Maps map UX/cost/legal constraints.
- Prototype AI scoring schema on a small licensed/local image set.
- Build first duplicate/zoo gold dataset.

## Process Backlog

- Create task-state update checklist.
- Create ADR template.
- Create story template.
- Create test-plan template.
- Create release checklist.
- Create AI handoff template.
- Create Obsidian vault index.
- Create OKF export files.
- Add Graphify generation workflow after first code exists.
- Add docs lint and link-check workflow.
- Add max-file-size warning workflow once code exists.
- Add full visible conversation text to `docs/conversation-archive/raw/FULL_CONVERSATION_COPY_PASTE_HERE.txt` after user pastes export.
- Create traceability matrix mapping requirements to modules, tests, ADRs, and work packages.
- Create first Alpha-0 vertical slice work package before feature code.
