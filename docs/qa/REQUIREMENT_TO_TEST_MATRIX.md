# Requirement-To-Test Matrix

## Purpose

This matrix maps requirement families to test families before code exists. Detailed test cases should keep the test ID prefix listed here and cite the requirement IDs in the test name, fixture, or test metadata.

## Test Priority

| Priority | Meaning | Gate |
|---|---|---|
| P0 | Launch-blocking safety, privacy, scoring, or security rule | Must pass before exposure |
| P1 | Core Alpha-0 behavior | Must pass before internal APK |
| P2 | Important beta behavior | Must pass before closed beta |
| P3 | Long-tail, polish, or regional behavior | Backlog unless risk changes |

## Functional Requirement Coverage

| Requirement Family | Planned Test IDs | Main Test Types | Priority | Gate |
|---|---|---|---|---|
| `FR-AUTH-*` | `TC-AUTH-*`, `TC-SEC-AUTH-*` | unit, integration, E2E | P1 | auth scaffold and alpha |
| `FR-AGE-*` | `TC-AGE-*`, `TC-PRIV-TEEN-*` | unit, E2E, manual | P0 | before account creation |
| `FR-CONSENT-*` | `TC-CONSENT-*`, `TC-AUDIT-CONSENT-*` | unit, integration | P1 | before posting |
| `FR-ONB-*` | `TC-ONB-*`, `TC-A11Y-ONB-*` | manual, E2E | P1 | before APK alpha |
| `FR-PERM-*` | `TC-PERM-*`, `TC-ANDROID-PERM-*` | manual device, E2E | P1 | before APK alpha |
| `FR-CAP-*` | `TC-CAP-*`, `TC-UPLOAD-*`, `TC-PRIV-MEDIA-*` | unit, integration, manual | P0/P1 | capture slice |
| `FR-TAX-*` | `TC-TAX-*`, `TC-GOLD-SPECIES-*` | goldset, unit | P2 | before AI scoring |
| `FR-SCORE-*` | `TC-SCORE-*`, `TC-ECON-*`, `TC-AUDIT-SCORE-*` | unit, property, integration | P0 | before leaderboard score |
| `FR-DUP-*` | `TC-DUP-*`, `TC-GOLD-DUP-*` | goldset, integration | P0 | before public ranking |
| `FR-ZOO-*` | `TC-ZOO-*`, `TC-GOLD-ZOO-*` | goldset, geo integration | P0 | before public ranking |
| `FR-COL-*` | `TC-COL-*`, `TC-PRIV-COL-*` | unit, E2E | P1 | private collection |
| `FR-SOC-*` | `TC-SOC-*`, `TC-MOD-*`, `TC-ABUSE-SOC-*` | unit, integration, abuse | P0/P2 | before public social |
| `FR-MAP-*` | `TC-MAP-*`, `TC-PRIV-LOC-*` | contract, geo integration, manual | P0 | before public map |
| `FR-LB-*` | `TC-LB-*`, `TC-ECON-LB-*` | unit, integration, load smoke | P2 | before rankings |
| `FR-MOD-*` | `TC-MOD-*`, `TC-AUDIT-MOD-*` | integration, manual ops | P0 | before public UGC |
| `FR-NOTIF-*` | `TC-NOTIF-*`, `TC-PRIV-NOTIF-*` | unit, manual device | P2 | beta |
| `FR-SET-*` | `TC-SET-*`, `TC-PRIV-SET-*` | E2E, manual | P1 | account settings |
| `FR-SUP-*` | `TC-SUP-*`, `TC-MOD-SUP-*` | manual, integration | P2 | beta support |

## Non-Functional Requirement Coverage

| NFR Family | Planned Test IDs | Evidence Required |
|---|---|---|
| `NFR-PERF-*` | `TC-PERF-*` | benchmark logs, device class, p95/p99 values |
| `NFR-SCALE-*` | `TC-SCALE-*` | load-test report and projection lag metrics |
| `NFR-REL-*` | `TC-REL-*` | retry, queue, outage, and no-loss tests |
| `NFR-PRIV-*` | `TC-PRIV-*` | DTO leak tests, EXIF strip tests, map precision tests |
| `NFR-SEC-*` | `TC-SEC-*` | authz, rate limit, App Check, secret scan evidence |
| `NFR-ACCESS-*` | `TC-A11Y-*` | screen-reader, text scale, touch target checklist |
| `NFR-MAINT-*` | `TC-MAINT-*` | docs validator, file-size checks, module READMEs |
| `NFR-OBS-*` | `TC-OBS-*` | request IDs, traces, alerts, crash reporting |
| `NFR-AUDIT-*` | `TC-AUDIT-*` | append-only records and query tests |
| `NFR-COST-*` | `TC-COST-*` | cost counters and budget guardrails |
| `NFR-PORT-*` | `TC-PORT-*` | Android build and iOS compile spike |
| `NFR-LOC-*` | `TC-LOC-*` | externalized strings and layout expansion smoke |
| `NFR-ENERGY-*` | `TC-ENERGY-*` | battery session measurement |

## Traceability Rule

Every test file added after Sprint 0 must reference at least one requirement or ADR when the tested behavior implements a product rule. Use names such as:

```txt
test_public_map_cells_omit_exact_coordinates_FR_MAP_004_NFR_PRIV_001
score_state_transition_pending_to_scored_FR_SCORE_008
```

If a test covers infrastructure only, reference the work package instead.
