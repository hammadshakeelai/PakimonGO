# Repository Structure Plan

## Goals

- Support a large mobile, backend, AI, and data product from day one.
- Keep files small enough for humans and AI agents to reason about.
- Make ownership boundaries obvious.
- Avoid future mass refactors by separating domains early.
- Keep documentation, requirements, decisions, and code connected.

## Implemented Scaffold Layout

The following scaffold folders now exist. Empty folders are intended boundaries and will receive code only after the relevant work package is ready.

```txt
PakimonGO/
  apps/
    mobile/
      pakimon_go_app/
        lib/
          app/
          core/
          features/
          shared/
          l10n/
        test/
        integration_test/
        android/
        ios/
  services/
    api/
      src/
        modules/
          auth/
          submissions/
          media/
          scoring/
          geo/
          social/
          leaderboards/
          moderation/
          notifications/
        platform/
        common/
      tests/
    workers/
      src/
        jobs/
        pipelines/
        adapters/
      tests/
  packages/
    contracts/
    scoring-rules/
    taxonomy/
    geo-rules/
    moderation-rules/
  infrastructure/
    docker/
    terraform/
    firebase/
    database/
      migrations/
      seeds/
      fixtures/
  data/
    goldsets/
      duplicate-detection/
      zoo-detection/
      species-identification/
    synthetic/
  docs/
    adr/
    templates/
  knowledge/
    okf/
      product/
      architecture/
      process/
      data/
  tools/
    graphify/
    okf-export/
    qa/
    scripts/
```

Current status:

- `apps/mobile/pakimon_go_app/` exists as the Flutter app home.
- `services/api/` exists as the backend API home.
- `services/workers/` exists as the async worker home.
- `packages/` exists for contracts and pure shared rules.
- `infrastructure/` exists for DB, Firebase, Docker, Cloud Run, and IaC.
- `data/goldsets/` exists for benchmark datasets.
- `tools/` and `knowledge/graph/graphify-out/` exist for future repo automation and graph outputs.

## Mobile Feature Layout

Use feature-first modules inside Flutter:

```txt
lib/features/capture/
  data/
  domain/
  presentation/
  application/
  capture_feature.dart
```

Each feature should own its UI, state, models, and tests unless shared by multiple features.

Expected features:

- `auth`
- `capture`
- `submission_review`
- `map`
- `feed`
- `collections`
- `profile`
- `friends`
- `groups`
- `leaderboards`
- `notifications`
- `settings`
- `moderation`

## Backend Module Layout

Each backend module should include:

```txt
modules/<name>/
  api/
  application/
  domain/
  infrastructure/
  tests/
  README.md
```

Module rules:

- `domain/` contains business rules and pure logic.
- `application/` orchestrates use cases.
- `api/` exposes HTTP or RPC endpoints.
- `infrastructure/` integrates database, queues, storage, or external APIs.
- Tests mirror the same subfolders.

## Package Strategy

Use shared packages for cross-service contracts and rules:

- `contracts`: request/response schemas and event schemas.
- `scoring-rules`: versioned scoring formula code and tests.
- `taxonomy`: animal taxonomy adapters and cached snapshots.
- `geo-rules`: geofence, H3/geohash, and privacy region rules.
- `moderation-rules`: report categories, policy checks, and safety flags.

## File Size Standard

Target:

- Source files: 200-300 lines.
- Test files: 150-350 lines.
- Documentation files: split once they become difficult to scan.

Split triggers:

- More than one domain concept in a file.
- More than one reason to change.
- More than 3 public classes or major functions.
- Complex function longer than 40-60 lines.
- Tests needing multiple unrelated setup styles.

## Context Preservation

Every module README should answer:

- What this module owns.
- What it must not own.
- Important requirement IDs.
- Important ADRs.
- Main tests.
- Common failure modes.

Code comments may reference:

- `REQ <id>`
- `ADR-<id>`
- `TD-<id>`
- `R-<id>`

## Anti-Refactor Rules

- Do not let UI call database or storage directly.
- Do not let mobile compute final score.
- Do not mix social popularity score with wild rarity score.
- Do not put AI provider-specific fields into core domain objects.
- Do not let map provider SDK types leak into backend contracts.
- Do not let Firebase-specific auth state leak into domain user models.
