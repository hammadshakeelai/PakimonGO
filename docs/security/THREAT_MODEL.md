# Threat Model

## Scope

This threat model covers Alpha-0 through gated social exposure: mobile app, API, workers, PostgreSQL, object storage, AI providers, map providers, auth, moderation, and public outputs.

## Assets

- User accounts, auth identities, emails, phone numbers.
- Photos, originals, derivatives, crops, EXIF.
- Exact capture coordinates and movement patterns.
- Friend graph, groups, comments, reports, blocks.
- AI evidence, embeddings, score explanations.
- Score events, leaderboards, trust signals.
- Moderation evidence and admin actions.
- Provider secrets, signed URLs, push tokens.

## Trust Boundaries

| Boundary | Risk |
|---|---|
| Mobile app to API | forged requests, replay, client tampering |
| API to Firebase Auth/App Check | token validation and provider dependency |
| API to database | authorization bugs, query leaks |
| API/worker to object storage | private URL leak, unsafe derivatives |
| Worker to AI provider | sensitive photo/context sharing |
| Backend to map/taxonomy/geofence sources | licensing, poisoned data, stale policy |
| Moderator/admin tools | insider misuse, excessive evidence access |
| Public APIs | exact location, sensitive species, privacy leaks |

## STRIDE Matrix

| Threat | Example | Impact | Mitigations | Tests |
|---|---|---|---|---|
| Spoofing | fake auth token, emulator abuse, GPS spoofing | fraudulent scores and abuse | Firebase token verification, App Check, Play Integrity, risk signals | TC-SEC-001, TC-GEO-001 |
| Tampering | client changes score, upload replay, modified metadata | unfair leaderboards | server-authoritative scoring, idempotency, checksums, immutable events | TC-SCORE-002, TC-CAP-012 |
| Repudiation | user denies upload, moderator denies action | audit gaps | append-only audit logs, trace IDs, action actor/source | TC-AUDIT-001 |
| Information disclosure | exact location returned in map/feed DTO | stalking, animal harm | public cells, delay, suppression, EXIF stripping, DTO tests | TC-PRIV-001 |
| Denial of service | bot uploads, comment spam, AI cost attack | cost and outage | rate limits, queues, caps, provider circuit breakers | TC-ABUSE-001 |
| Elevation of privilege | user accesses moderator API | privacy breach | role checks, scoped admin, case-needed evidence | TC-SEC-002 |

## Abuse Cases

| ID | Abuse Case | Control |
|---|---|---|
| AB-001 | User repeatedly uploads zoo photos as wild. | geofence, self-disclosure comparison, trust signals, caps, review |
| AB-002 | User posts same animal repeatedly. | hash, perceptual hash, crop embedding, encounter grouping |
| AB-003 | User posts web-scraped animal images. | repost detection, metadata signals, review, zero score |
| AB-004 | User tries to reveal rare animal location. | sensitive species policy, map suppression, moderation |
| AB-005 | User harasses another user through comments/groups. | block, report, hide, moderation, rate limits |
| AB-006 | Collusive accounts inflate likes and reposts. | social score caps, fraud dampening, trust graph |
| AB-007 | User photographs someone else's pet and tags owner without consent. | owner acceptance before public owner credit |
| AB-008 | AI provider receives unnecessary exact location. | minimized structured context, derived fields |
| AB-009 | Moderator opens private evidence without need. | purpose-bound access grants and audit |
| AB-010 | Account deletion leaves public personal data behind. | deletion workflow, anonymization, verification report |

## Launch-Blocking Security Controls

- Auth and authorization on every protected endpoint.
- App Check/attestation enforcement for scoring/upload before public alpha.
- Short-lived signed upload URLs.
- Public DTO tests proving exact coordinates and private URLs are absent.
- EXIF GPS stripping for every public derivative.
- Rate limits for upload, scoring, comments, likes, reports, appeals, and auth-sensitive flows.
- Report, block, hide/delete, moderation queue, appeals, and audit before public social exposure.
- Incident switch to disable public posting, public map, and leaderboard scopes.

## Open Security Questions

- Exact provider retention settings for AI images and metadata.
- Production key management provider and rotation schedule.
- Beta moderator staffing and escalation ownership.
- Data residency and region-specific feature gates.
- Account deletion backup-retention disclosure.
