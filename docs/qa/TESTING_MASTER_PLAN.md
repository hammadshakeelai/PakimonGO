# Testing Master Plan

## Test Strategy

PakimonGO's highest-risk failures are unfair scoring, unsafe incentives, duplicate/zoo farming, privacy leaks, UGC abuse, and AI drift. Tests must prove product rules, not just code paths.

## Operational Specs

Use these focused docs when creating implementation tests:

- `docs/qa/REQUIREMENT_TO_TEST_MATRIX.md`
- `docs/qa/SPRINT_0_TEST_PLAN.md`
- `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md`
- `docs/qa/SCORING_STATE_TEST_SPEC.md`
- `docs/qa/GOLDSET_GOVERNANCE_PLAN.md`
- `docs/qa/ZOO_DUPLICATE_BENCHMARK_SPEC.md`
- `docs/qa/MANUAL_ANDROID_QA_CHECKLIST.md`
- `docs/qa/SECURITY_TEST_CHECKLIST.md`
- `docs/qa/CI_GATE_DESIGN.md`
- `docs/qa/DEFINITION_OF_READY_DONE.md`

## Test Levels

| Level | Purpose | Examples |
|---|---|---|
| Unit | Pure functions and state machines | scoring formula, visibility, score state, privacy transforms |
| Contract | API and event schemas | OpenAPI validation, DTO privacy checks |
| Integration | API, DB, storage, workers | signed upload, submission, scoring job, moderation action |
| Goldset | AI/duplicate/zoo/scoring quality | duplicate recall, zoo false positives, species confidence |
| E2E | user flows | sign in, capture, upload, pending score, collection |
| Manual Device | platform behavior | camera, permissions, map, battery, low-end Android |
| Abuse/Security | adversarial behavior | GPS spoofing, bot uploads, collusive likes, exact-location leaks |

## Test ID Families

- `TC-AUTH-*`: identity and account management.
- `TC-AGE-*`: age gate and teen defaults.
- `TC-CONSENT-*`: policy acceptance and analytics opt-out.
- `TC-ONB-*`: onboarding comprehension and safety messaging.
- `TC-PERM-*`: camera/location/contacts permission behavior.
- `TC-CAP-*`: capture, drafts, uploads, EXIF, derivatives.
- `TC-TAX-*`: taxonomy and sensitivity.
- `TC-SCORE-*`: score state, ledgers, versioning, rollback.
- `TC-DUP-*`: duplicate and encounter grouping.
- `TC-ZOO-*`: zoo/captive/pet/wild eligibility.
- `TC-COL-*`: collections and profile privacy.
- `TC-SOC-*`: social and visibility rules.
- `TC-MAP-*`: map privacy and waypoint routing.
- `TC-LB-*`: leaderboard projections and rollbacks.
- `TC-MOD-*`: moderation, appeals, audit.
- `TC-NOTIF-*`, `TC-SET-*`, `TC-SUP-*`: notifications, settings, support.
- `TC-SEC-*`: authz, attestation, secrets, role checks.
- `TC-PRIV-*`: exact coordinate, EXIF, deletion, public DTO leaks.
- `TC-ABUSE-*`: spam, spoofing, collusion, harassment.
- `TC-AUDIT-*`: immutable audit and score event records.

## Launch-Blocking Test Suites

| Suite | Must Prove |
|---|---|
| Privacy DTO Suite | No public API returns exact normal capture coordinates, private URLs, raw EXIF, or restricted evidence. |
| Upload Suite | Upload intent is scoped, short-lived, idempotent, and retry-safe. |
| Score State Suite | Client cannot set final score; pending/review/capped/rejected/scored transitions are valid. |
| Zoo/Duplicate Suite | Zoo/captive and duplicate signals cap or review instead of blindly ranking. |
| Moderation Suite | Report, block, hide/delete, appeal, audit, and incident disable switch work before public social exposure. |
| Accessibility Suite | Core capture, collection, map/list, report/block, and settings flows meet mobile accessibility expectations. |
| Abuse Suite | GPS spoofing, bot uploads, collusive likes, repeated zoo uploads, reposted images, and false reports are controlled. |

## Goldset Benchmarks

Goldsets live under `data/goldsets/` and follow `data/goldsets/MANIFEST_SCHEMA.md`.

Minimum benchmark categories:

- duplicate-detection
- zoo-detection
- species-identification
- scoring-calibration
- sensitive-species

## CI Plan

Phase 1 docs CI:

- Markdown link check.
- File-size warning.
- Requirements/traceability ID consistency check.
- OpenAPI schema validation.

Phase 2 code CI:

- Flutter format/analyze/test.
- Backend lint/type/test.
- Contract tests.
- Secret scan.
- Dependency audit.

Phase 3 benchmark CI:

- Small goldset smoke tests.
- Privacy DTO regression tests.
- Score formula snapshot tests.

## Manual QA Gates

- Low-end Android camera capture.
- Foreground location permission and denial.
- Upload retry after network loss.
- Map fallback/list mode.
- Battery drain smoke test.
- Store-review demo account flow.
