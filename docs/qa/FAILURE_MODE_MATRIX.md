# Failure Mode Matrix

## Purpose

This matrix names likely failures before code exists. Every P0/P1 failure needs detection, mitigation, and rollback evidence before related features are exposed.

| Area | Failure | User/Business Impact | Detection | Test IDs | Mitigation | Rollback |
|---|---|---|---|---|---|---|
| auth | invalid token accepted | account takeover or data leak | authz negative tests, logs | TC-SEC-AUTH-001..003 | Firebase token verification, server authz checks | disable protected endpoint or reject all until fixed |
| auth | provider linking takeover | account hijack | abuse tests | TC-AUTH-010 | reauth, verified provider ownership | disable linking |
| age | under-13 enters normal flow | compliance exposure | E2E age gate | TC-AGE-002 | neutral age gate and hard block/divert | disable signup |
| consent | outdated policy still allows posting | legal/privacy gap | consent integration test | TC-CONSENT-003 | policy version gate | disable posting |
| upload | signed URL reusable too long | private media abuse | signed URL expiry test | TC-UPLOAD-001 | short expiry, scoped object path | invalidate upload intents |
| upload | retry creates duplicate media/submission | score farming, bad UX | idempotency test | TC-UPLOAD-002, TC-UPLOAD-003 | idempotency keys and unique constraints | quarantine duplicate submissions |
| media | EXIF GPS on public derivative | exact location leak | EXIF strip test | TC-MEDIA-002 | derivative pipeline strips metadata | unpublish derivatives |
| media | original URL exposed publicly | private photo leak | privacy DTO scan | TC-MEDIA-001 | public derivative-only DTOs | revoke URLs and rotate object access |
| capture | draft lost on restart | user loses photo | mobile E2E/manual | TC-CAP-004 | durable local draft store | pause capture release |
| location | exact coordinate in public map | stalking/sensitive species risk | contract scan | TC-MAP-004 | public cells, fuzzing, delay | disable map activity endpoint |
| location | background location requested | store/privacy violation | manual Android QA | TC-PERM-003 | foreground-only permission policy | remove permission and rebuild APK |
| sensitive species | rare species shown too precisely | wildlife harm | sensitive taxon tests | TC-TAX-007, TC-MAP-005 | suppression/coarsening policy | disable species layer |
| zoo | inside-zoo photo earns wild score | leaderboard corruption | geofence benchmark | TC-ZOO-001..003 | geofence cap/review | rollback score events |
| zoo | near-boundary wild photo penalized | unfair scoring | boundary tests | TC-ZOO-003 | uncertainty routes to review/cap | adjust decision and trust score |
| pet | pet gets wild rarity score | economy abuse | pet/wild tests | TC-ZOO-009, TC-SCORE-012 | domestic species review/default pet ledger | rollback score |
| duplicate | exact repost earns points | farming | exact hash test | TC-DUP-001 | hash uniqueness/edge | rollback score and trust |
| duplicate | cropped repost missed | farming | crop goldset | TC-DUP-003 | pHash/embedding/crop detection | adjust threshold and rerun |
| duplicate | similar animals falsely merged | user frustration | false-positive benchmark | TC-DUP-009 | review threshold and appeal | reverse duplicate edge |
| scoring | client sets final score | total economy compromise | abuse API test | TC-SCORE-002 | server-authoritative finalization | disable scoring writes |
| scoring | score event overwritten | audit gap | immutable event test | TC-SCORE-005 | append-only ledger | restore from audit/backup |
| scoring | unsafe interaction rewarded | animal harm incentive | moderation/abuse test | TC-SCORE-016 | safety penalty/review | quarantine score rule |
| scoring | formula drift not versioned | unexplainable ranks | unit/audit test | TC-SCORE-007 | formula version on event | freeze scoring deploy |
| leaderboard | quarantined score ranks | unfair public competition | projection test | TC-LB-006 | eligibility filter | rebuild projections |
| leaderboard | rollback not projected | stale ranks | integration test | TC-LB-009 | projection invalidation | force projection rebuild |
| social | blocked user sees content | harassment/privacy risk | visibility abuse test | TC-SOC-006 | block-aware queries | disable social feed |
| social | group bypasses visibility | privacy breach | contract test | TC-SOC-015 | visibility central policy | disable groups |
| social | public feed enabled before moderation | UGC risk | feature flag test | TC-SOC-010 | gated flags | disable public feed flag |
| moderation | reports not auditable | ops/legal gap | audit test | TC-MOD-009 | append-only moderation audit | freeze moderation actions |
| moderation | moderator overexposure | privacy/internal misuse | contract test | TC-MOD-018 | case-needed evidence scopes | revoke moderator access |
| notifications | exact location in push | privacy leak | payload test | TC-NOTIF-005 | safe payload templates | disable push category |
| settings | deletion path broken | legal/privacy gap | E2E/integration | TC-SET-003 | deletion request workflow | disable new public accounts |
| observability | no request IDs | incident debugging failure | logging test | TC-OBS-* | trace/request ID middleware | block beta |
| CI | docs/tests not run | drift and hidden failures | CI status | TC-MAINT-* | required GitHub checks | block merge |
| secrets | real credential committed | platform compromise | secret scan | TC-SEC-SUPPLY-001 | scan, ignore, rotate | rotate key and purge history if needed |
| performance | cold start too slow | poor adoption | manual/perf run | TC-PERF-* | profiling and lazy loading | block APK ring |
| battery | GPS/camera stay active | battery/privacy issue | manual device QA | TC-ENERGY-* | lifecycle cleanup | disable map/capture build |
