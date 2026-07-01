# Test Harness Architecture

## Purpose

This document defines where tests, fixtures, fakes, and helpers should live once code appears. Keep tests close to modules, but share only stable contract fixtures.

## Backend Layout

Use this target layout for `services/api/`:

```txt
services/api/
  src/
    modules/<module>/
      api/
      application/
      domain/
      infrastructure/
  tests/
    unit/<module>/
    contract/
    integration/
    abuse/
    conftest.py
```

Rules:

- Unit tests use domain/application fakes only.
- Contract tests assert OpenAPI and public DTO behavior.
- Integration tests may use test database/storage fakes.
- Abuse tests simulate adversarial flows such as spoofing, duplicate farming, and authz bypass.

## Worker Layout

```txt
services/workers/
  src/jobs/<job_family>/
  tests/
    unit/
    integration/
```

Workers must accept fake clocks, fake IDs, fake provider adapters, and test queues. No worker test should call a live AI, map, storage, or auth provider.

## Flutter Layout

```txt
apps/mobile/pakimon_go_app/
  lib/features/<feature>/
  test/features/<feature>/
  integration_test/
  test_support/
```

Rules:

- Feature tests stay under `test/features/<feature>/`.
- Widget tests use fake repositories/providers.
- Integration tests cover capture, permissions, upload retry, and collection flows after scaffold exists.
- Manual device QA evidence links to `docs/qa/MANUAL_ANDROID_QA_CHECKLIST.md`.

## Shared Fixtures

- API examples live in `docs/api/examples/`.
- QA fixtures live in `docs/qa/fixtures/`.
- Generated test fixtures may later live under `packages/contracts/tests/fixtures/`.
- Do not store real user photos, credentials, exact sensitive locations, or production exports in fixtures.

## Required Test Helpers

Add these as modules need them:

- fake clock
- fake ID generator
- fake authenticated user
- fake App Check/integrity result
- fake storage adapter
- fake AI evidence provider
- fake map/geofence provider
- fake notification sender
- database transaction cleanup fixture

## Test Naming

Use requirement-aware names when testing product rules:

```txt
test_public_map_response_omits_exact_coordinates_FR_MAP_004
test_score_state_rejects_pending_to_scored_FR_SCORE_008
```

Infrastructure-only tests may use work-package IDs instead.
