# Security Test Checklist

## Purpose

Security tests protect accounts, media, exact location, scoring authority, moderation evidence, and public social surfaces.

## Authentication And Authorization

| ID | Check |
|---|---|
| `TC-SEC-AUTH-001` | protected endpoints reject missing token |
| `TC-SEC-AUTH-002` | protected endpoints reject invalid token |
| `TC-SEC-AUTH-003` | user cannot read another user's private submission |
| `TC-SEC-AUTH-004` | sensitive account changes require reauthentication |
| `TC-SEC-AUTH-005` | provider linking prevents duplicate takeover |
| `TC-SEC-AUTH-006` | admin/moderator endpoints reject normal users |

## App Integrity And Rate Limits

| ID | Check |
|---|---|
| `TC-SEC-APP-001` | scoring/upload endpoints enforce App Check where available |
| `TC-SEC-APP-002` | repeated upload attempts hit rate limits |
| `TC-SEC-APP-003` | comment/like/report spam hits rate limits |
| `TC-SEC-APP-004` | idempotency keys stop duplicate mutation on retry |
| `TC-SEC-APP-005` | suspicious activity can enter review/quarantine |

## Media And Uploads

| ID | Check |
|---|---|
| `TC-SEC-MEDIA-001` | signed upload URL is scoped to one object |
| `TC-SEC-MEDIA-002` | expired signed upload URL fails |
| `TC-SEC-MEDIA-003` | upload completion cannot claim another user's object |
| `TC-SEC-MEDIA-004` | public derivatives do not expose original storage path |
| `TC-SEC-MEDIA-005` | unsupported/corrupt files are rejected safely |

## Location And Privacy Abuse

| ID | Check |
|---|---|
| `TC-SEC-LOC-001` | public map cannot return exact coordinates |
| `TC-SEC-LOC-002` | sensitive species locations are suppressed/coarsened |
| `TC-SEC-LOC-003` | mock location/GPS spoofing signals lower trust or review |
| `TC-SEC-LOC-004` | impossible travel speed creates risk signal |
| `TC-SEC-LOC-005` | home/school-like sensitive areas use coarser output |

## Scoring And Economy Abuse

| ID | Check |
|---|---|
| `TC-SEC-SCORE-001` | client cannot submit final score |
| `TC-SEC-SCORE-002` | duplicate uploads do not earn normal points |
| `TC-SEC-SCORE-003` | zoo/captive deception lowers trust or routes to review |
| `TC-SEC-SCORE-004` | social-like collusion is capped/damped |
| `TC-SEC-SCORE-005` | rollback updates leaderboards and audit records |

## UGC And Moderation

| ID | Check |
|---|---|
| `TC-SEC-UGC-001` | blocked user cannot view restricted content |
| `TC-SEC-UGC-002` | report/block/hide/delete work before public social exposure |
| `TC-SEC-UGC-003` | moderation action creates audit record |
| `TC-SEC-UGC-004` | moderator sees only case-needed evidence |
| `TC-SEC-UGC-005` | incident switch can disable public posting/map/rank |

## Secrets And Supply Chain

| ID | Check |
|---|---|
| `TC-SEC-SUPPLY-001` | no secrets committed in repo |
| `TC-SEC-SUPPLY-002` | `.env.example` contains dummy values only |
| `TC-SEC-SUPPLY-003` | dependency audit runs in CI before production |
| `TC-SEC-SUPPLY-004` | release artifacts do not contain private config |

## Evidence Rule

Security test failures must be recorded in `docs/BUGS_AND_RISKS.md` or the issue tracker once it exists. P0 security failures block feature exposure until fixed or formally accepted by an ADR.
