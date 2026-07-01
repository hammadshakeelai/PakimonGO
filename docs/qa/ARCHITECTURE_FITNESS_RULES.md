# Architecture Fitness Rules

## Purpose

Fitness rules are lightweight architecture tests. They should become automated checks as code appears.

## P0 Rules

| ID | Rule | Planned Enforcement |
|---|---|---|
| FIT-PRIV-001 | Public DTOs must not contain exact coordinates, raw EXIF, original URLs, private storage paths, or moderation evidence. | contract tests and schema scan |
| FIT-SCORE-001 | Client/mobile code must not assign final score or leaderboard eligibility. | API contract and backend tests |
| FIT-SCORE-002 | Score changes must be append-only events with formula/version metadata. | domain tests |
| FIT-MAP-001 | Public map APIs must return cells/clusters/delayed data, never exact animal pins. | contract tests |
| FIT-AUTH-001 | Protected endpoints must require auth and authorization. | API abuse tests |
| FIT-UPLOAD-001 | Upload completion must be idempotent and scoped to owner/media asset. | integration tests |
| FIT-SECRET-001 | Secrets, local `.env`, signing keys, and real credentials must not be committed. | secret scan |

## P1 Rules

| ID | Rule | Planned Enforcement |
|---|---|---|
| FIT-MOD-001 | Public social exposure requires report, block, hide/delete, appeal, and audit paths. | release gate checklist |
| FIT-ZOO-001 | Zoo/captive uncertainty routes to cap/review, not confident hard penalty. | goldset/integration tests |
| FIT-DUP-001 | Duplicate decisions are stored as edges, not silent deletion. | domain/integration tests |
| FIT-MODULE-001 | Domain modules must not import provider SDKs directly. | import boundary tests |
| FIT-MODULE-002 | Provider adapters live in infrastructure/provider modules. | import boundary tests |
| FIT-MOBILE-001 | Mobile feature code calls repositories/services, not cloud provider SDKs directly except platform adapters. | code review/import checks |
| FIT-FILE-001 | Source files over 500 lines fail validation unless generated or documented. | `tools/qa/validate_docs.py` |

## Import Boundary Targets

Backend module direction:

```txt
api -> application -> domain
infrastructure -> application/domain interfaces
domain -> no infrastructure/provider imports
```

Mobile feature direction:

```txt
screen/widget -> controller/view_model -> repository/service -> adapter
```

Worker direction:

```txt
job runner -> application service -> domain rule -> provider adapter
```

## Automation Plan

Sprint 0:

- keep rules documented and manually reviewed
- enforce file-size and secret checks

Alpha:

- add import-boundary tests
- add public DTO forbidden-field scanner
- add score state regression tests

Beta:

- add architecture fitness checks to CI required status
- block public/social/map/rank exposure on P0 failure
