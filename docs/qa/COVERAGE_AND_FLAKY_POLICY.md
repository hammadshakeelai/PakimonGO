# Coverage And Flaky Test Policy

## Purpose

Coverage should protect product rules without rewarding low-value tests. Flaky tests must not become normal background noise.

## Coverage Targets By Phase

| Phase | Target |
|---|---|
| Sprint 0 scaffold | smoke/import/contract tests exist; no numeric coverage gate |
| Alpha private capture | core domain/application modules target 70% line coverage |
| Beta social/map/rank | critical backend modules target 80% line coverage |
| Production | P0 privacy/scoring/auth/moderation rules have direct regression tests |

Coverage is not a substitute for launch-blocking tests. A module with high coverage still fails the gate if privacy DTO, score state, duplicate/zoo, or authz tests are missing.

## Required Direct Coverage

These areas require named tests even if coverage is high:

- public DTO privacy transforms
- score state transitions
- upload idempotency
- duplicate edge decisions
- zoo/captive eligibility
- leaderboard rollback
- block/report/moderation rules
- account deletion/export workflow

## Flaky Test Policy

- A flaky P0 test blocks merge until fixed or quarantined by lead approval.
- Quarantined tests require owner, reason, expiry date, and replacement coverage.
- Do not delete flaky tests silently.
- Do not retry tests in CI without logging the flake.
- A test that fails due to live provider instability should be converted to a fake-provider test plus a separate provider smoke test.

## Quarantine Template

```txt
Test ID:
File:
Owner:
Reason:
Risk:
Temporary coverage:
Expiry date:
Removal condition:
```

## Coverage Evidence

Every release gate should record:

- command run
- coverage report path or summary
- skipped/quarantined tests
- owner for gaps
- reason any threshold was waived
