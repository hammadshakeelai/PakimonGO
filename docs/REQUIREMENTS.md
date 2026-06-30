# Requirements

## Requirement Rules

Use stable IDs in stories, tests, code comments, ADRs, bug reports, and commit messages. The client never owns final scoring or leaderboard truth; server-side rules and audit records are authoritative.

## Functional Requirements

### Identity, Accounts, Age, And Consent

| ID | Requirement |
|---|---|
| FR-AUTH-001 | Users can sign in with Google. |
| FR-AUTH-002 | Users can sign up and sign in with email/password. |
| FR-AUTH-003 | Users can reset password by email. |
| FR-AUTH-004 | Phone verification/recovery is supported only after abuse/cost policy is defined. |
| FR-AUTH-005 | iOS release supports Sign in with Apple if third-party login is offered. |
| FR-AUTH-006 | Users can request account deletion in-app. |
| FR-AUTH-007 | Account deletion starts immediately and completes/anonymizes eligible data within the defined retention window. |
| FR-AUTH-008 | Users can export user-provided data in a machine-readable format. |
| FR-AUTH-009 | Provider linking prevents duplicate account takeover. |
| FR-AUTH-010 | Sensitive account actions require reauthentication. |
| FR-AUTH-011 | Users can sign out from the device. |
| FR-AUTH-012 | Suspicious account activity can trigger risk review. |
| FR-AGE-001 | App launch includes a neutral age gate. |
| FR-AGE-002 | Under-13 users are blocked or diverted until family mode exists. |
| FR-AGE-003 | 13-17 users receive stricter privacy/social defaults. |
| FR-CONSENT-001 | Users accept current Terms, Privacy Policy, and Community Rules before posting. |
| FR-CONSENT-002 | Consent records store policy version, timestamp, and user ID. |
| FR-CONSENT-003 | Policy updates can require re-acknowledgement before further posting. |
| FR-CONSENT-004 | Users can review permission/privacy choices in settings. |
| FR-CONSENT-005 | Users can opt out of non-essential analytics where required. |

### Onboarding, Education, And Permissions

| ID | Requirement |
|---|---|
| FR-ONB-001 | Onboarding explains animal safety, privacy, scoring honesty, social conduct, and permissions in plain language. |
| FR-ONB-002 | Onboarding states exact capture locations are not shown publicly by default. |
| FR-ONB-003 | Onboarding states zoo/pet/captive photos can be saved but do not earn normal wild score. |
| FR-ONB-004 | Onboarding states unsafe animal interaction can reduce score or trigger review. |
| FR-ONB-005 | Onboarding states AI can be wrong and appeals exist. |
| FR-PERM-001 | Camera permission is requested only when opening capture. |
| FR-PERM-002 | Foreground location permission is requested only for map or submission. |
| FR-PERM-003 | Background location is not requested in Alpha-0. |
| FR-PERM-004 | Contacts permission is not required for core play. |
| FR-PERM-005 | Invite links work without contacts access. |
| FR-PERM-006 | Permission denial shows a usable fallback state. |
| FR-PERM-007 | Permission explanations are short, contextual, and non-coercive. |

### Capture, Drafts, Uploads, And Media

| ID | Requirement |
|---|---|
| FR-CAP-001 | Users can open in-app camera. |
| FR-CAP-002 | Users can capture animal photo. |
| FR-CAP-003 | Capture creates local draft before upload. |
| FR-CAP-004 | Draft survives app restart until submitted or deleted. |
| FR-CAP-005 | Users can mark context as wild, pet, zoo/captive, or unknown. |
| FR-CAP-006 | Users can add real name, cute name, caption, and optional tags. |
| FR-CAP-007 | Users choose visibility before publishing. |
| FR-CAP-008 | Default visibility is private until changed. |
| FR-CAP-009 | Location accuracy is recorded with submission when permission exists. |
| FR-CAP-010 | Location denial allows private/no-score or limited-score submission depending on policy. |
| FR-CAP-011 | Upload uses short-lived signed URL. |
| FR-CAP-012 | Upload completion is idempotent. |
| FR-CAP-013 | Failed upload can retry without duplicate submission. |
| FR-CAP-014 | Originals are private. |
| FR-CAP-015 | Public derivatives strip EXIF GPS. |
| FR-CAP-016 | Feeds and collections use thumbnails by default. |
| FR-CAP-017 | Unsupported/corrupt/oversized files are rejected with clear error. |
| FR-CAP-018 | Multi-animal photos create one primary observation and optional secondary candidates. |
| FR-CAP-019 | Users can delete a draft. |
| FR-CAP-020 | Users can delete or unpublish their post subject to moderation/legal retention rules. |

### Animal Identification, Taxonomy, And Context

| ID | Requirement |
|---|---|
| FR-TAX-001 | System stores taxon candidates with confidence. |
| FR-TAX-002 | Taxa use stable external IDs where available. |
| FR-TAX-003 | Taxonomy imports are versioned. |
| FR-TAX-004 | Accepted names, synonyms, and common names are tracked. |
| FR-TAX-005 | Regional species status can be recorded. |
| FR-TAX-006 | Establishment means and degree of establishment are modeled. |
| FR-TAX-007 | Sensitive species rules can override public map behavior. |
| FR-TAX-008 | Low-confidence identification caps score or sends to review. |
| FR-TAX-009 | User-provided name is stored separately from AI/taxonomy result. |
| FR-TAX-010 | Users can appeal or correct animal identification. |

### Scoring And Economy

| ID | Requirement |
|---|---|
| FR-SCORE-001 | Server evaluates species, rarity, image quality, aesthetics, safety, novelty, duplicates, and abuse signals. |
| FR-SCORE-002 | Client never assigns final score. |
| FR-SCORE-003 | Users cannot see final points until server scoring completes. |
| FR-SCORE-004 | Every score stores explanation fields. |
| FR-SCORE-005 | Score events are immutable. |
| FR-SCORE-006 | Corrections use reversal/adjustment events. |
| FR-SCORE-007 | Scoring formula version is stored on every score event. |
| FR-SCORE-008 | Scoring state machine supports pending, prechecked, AI evaluated, scored, capped, review, rejected. |
| FR-SCORE-009 | Zoo/captive photos save to collection but skip normal wild leaderboard score. |
| FR-SCORE-010 | Honest zoo disclosure can receive tiny bounded participation credit. |
| FR-SCORE-011 | Repeated zoo uploads hit strict diminishing returns. |
| FR-SCORE-012 | Pet photos can receive pet/cute/social score but not wild rarity score. |
| FR-SCORE-013 | Pet owner tagging can award bounded shared credit after owner acceptance. |
| FR-SCORE-014 | Social engagement points are capped and fraud-damped. |
| FR-SCORE-015 | Wild score, pet/social score, and participation score are separate ledgers. |
| FR-SCORE-016 | Unsafe animal interaction reduces score or triggers review. |
| FR-SCORE-017 | High-risk submissions can be quarantined from leaderboards. |
| FR-SCORE-018 | New/low-score users can receive catch-up boosts. |
| FR-SCORE-019 | High-score users face diminishing returns for repetition. |
| FR-SCORE-020 | Score rollback updates all affected leaderboard projections. |

### Duplicate, Repost, And Encounter Grouping

| ID | Requirement |
|---|---|
| FR-DUP-001 | Exact duplicate images are detected by hash. |
| FR-DUP-002 | Near duplicates are detected by perceptual hash. |
| FR-DUP-003 | Crop-level duplicate matching is supported. |
| FR-DUP-004 | Semantic duplicate matching uses embeddings where available. |
| FR-DUP-005 | Duplicate checks use sane windows: user/device/time/location/species. |
| FR-DUP-006 | Duplicate relationships are stored as edges, not silent deletion. |
| FR-DUP-007 | Same-encounter photos can be grouped. |
| FR-DUP-008 | Users can replace a photo without farming points. |
| FR-DUP-009 | Material animal change can create a new score-eligible event. |
| FR-DUP-010 | Web-scraped/reposted image suspicion can zero score or trigger review. |
| FR-DUP-011 | False duplicate decisions can be appealed. |
| FR-DUP-012 | Duplicate thresholds are versioned. |

### Zoo, Captive, Pet, And Wild Eligibility

| ID | Requirement |
|---|---|
| FR-ZOO-001 | System classifies submissions as wild eligible, pet likely, zoo likely, captive uncertain, sensitive taxon, or needs review. |
| FR-ZOO-002 | Zoo/captive classification uses geofences, self-disclosure, GPS accuracy, image context, and venue data. |
| FR-ZOO-003 | GPS uncertainty overlapping a zoo boundary routes to capped score or review, not automatic penalty. |
| FR-ZOO-004 | Geofence datasets are versioned. |
| FR-ZOO-005 | OSM/curated zoo/aquarium/petting zoo/sanctuary sources can seed geofences. |
| FR-ZOO-006 | User honesty about zoo/pet/captive context is rewarded more than punished. |
| FR-ZOO-007 | Repeated misleading wild claims lower trust. |
| FR-ZOO-008 | Pet owner consent is required before owner-credit public display. |
| FR-ZOO-009 | Domestic species default toward pet/captive review unless evidence supports wild/feral/naturalized. |
| FR-ZOO-010 | Captive/wild decisions are appealable. |

### Collections, Profiles, And Privacy

| ID | Requirement |
|---|---|
| FR-COL-001 | Users can view personal collection. |
| FR-COL-002 | Collection entries show pending/scored/review/capped state. |
| FR-COL-003 | Entries label wild, pet, zoo/captive, unknown, or review state. |
| FR-COL-004 | Users can create collection pages. |
| FR-COL-005 | Users can organize captures by animal, region, date, tag, or custom collection. |
| FR-COL-006 | Private captures remain private unless published. |
| FR-COL-007 | Users can change visibility after posting. |
| FR-COL-008 | Visibility changes update feed/map/public derivative availability. |
| FR-COL-009 | Profiles show only user-approved public/visible content. |
| FR-COL-010 | Profile privacy settings control public stats and collection previews. |

### Social, Friends, Groups, And UGC

| ID | Requirement |
|---|---|
| FR-SOC-001 | Posts support private, public, friends, and selected-friends visibility. |
| FR-SOC-002 | Users can like posts. |
| FR-SOC-003 | Users can comment on posts. |
| FR-SOC-004 | Users can repost/share when allowed by visibility rules. |
| FR-SOC-005 | Users can add captions and hashtags. |
| FR-SOC-006 | Blocked users cannot view or interact with blocker's restricted content. |
| FR-SOC-007 | Reporting is available on posts, comments, profiles, groups, and messages if messages ever exist. |
| FR-SOC-008 | Users can hide/delete their own posts. |
| FR-SOC-009 | Feed respects visibility, block, moderation, and sensitive-location rules. |
| FR-SOC-010 | Public feed is feature-flagged until moderation gate passes. |
| FR-SOC-011 | Friends can be added by invite link. |
| FR-SOC-012 | Contacts import is deferred and optional. |
| FR-SOC-013 | Friend leaderboard works without contacts upload. |
| FR-SOC-014 | Groups support owner, moderator, member roles. |
| FR-SOC-015 | Group posts cannot bypass post visibility or block rules. |
| FR-SOC-016 | Group membership and posting can be moderated. |
| FR-SOC-017 | Hashtags cannot expose exact location or sensitive species. |
| FR-SOC-018 | Likes/reposts from suspicious accounts are damped. |
| FR-SOC-019 | Public comments can be limited, hidden, or disabled. |
| FR-SOC-020 | Users can appeal moderation decisions. |

### Maps, Routes, And Location Privacy

| ID | Requirement |
|---|---|
| FR-MAP-001 | Map shows player location only with permission. |
| FR-MAP-002 | Map uses game-like styling. |
| FR-MAP-003 | Public animal activity uses cells/clusters/delay/fuzzing. |
| FR-MAP-004 | Public APIs never return exact capture coordinates for normal posts. |
| FR-MAP-005 | Sensitive species/home/school-like areas are coarser or suppressed. |
| FR-MAP-006 | Map queries are viewport-bounded. |
| FR-MAP-007 | Map shows species/activity summaries by area. |
| FR-MAP-008 | Waypoint route points to general area, not exact animal pin. |
| FR-MAP-009 | Route feature works without background location. |
| FR-MAP-010 | Map provider content terms are respected. |
| FR-MAP-011 | Map outage falls back to cached/list view. |
| FR-MAP-012 | OSM-derived data includes required attribution where exposed. |
| FR-MAP-013 | Local leaderboard regions use privacy-safe cells. |
| FR-MAP-014 | Public map data is delayed by default. |
| FR-MAP-015 | User can view why a location is hidden/coarsened where safe to explain. |

### Leaderboards And Competition

| ID | Requirement |
|---|---|
| FR-LB-001 | Global leaderboard exists behind readiness gate. |
| FR-LB-002 | Country leaderboard exists behind region policy. |
| FR-LB-003 | Local leaderboard uses privacy-safe regions. |
| FR-LB-004 | Friends leaderboard is supported. |
| FR-LB-005 | Leaderboards use valid score events only. |
| FR-LB-006 | Quarantined scores do not rank. |
| FR-LB-007 | Leaderboard periods support all-time and rolling windows. |
| FR-LB-008 | Leaderboard ties are deterministic. |
| FR-LB-009 | Score rollback updates all leaderboards. |
| FR-LB-010 | Users can see pending/reviewed score status. |
| FR-LB-011 | Catch-up mechanics are transparent enough to feel fair. |
| FR-LB-012 | High-score diminishing returns are testable. |
| FR-LB-013 | Local leaderboard hides regions with too few users if privacy risk exists. |
| FR-LB-014 | Social score cannot dominate wild discovery rank. |
| FR-LB-015 | Admins can disable leaderboard scopes by region. |

### Moderation, Appeals, Safety, And Admin

| ID | Requirement |
|---|---|
| FR-MOD-001 | Users can report content. |
| FR-MOD-002 | Users can report users. |
| FR-MOD-003 | Users can block users. |
| FR-MOD-004 | Users can hide/delete own content. |
| FR-MOD-005 | Moderator console supports report review. |
| FR-MOD-006 | Moderator console supports score appeal review. |
| FR-MOD-007 | Moderator console supports takedown and restoration. |
| FR-MOD-008 | Moderator console supports score rollback/quarantine. |
| FR-MOD-009 | Every moderation action is audited. |
| FR-MOD-010 | Users are notified of major moderation decisions where safe/legal. |
| FR-MOD-011 | Appeals can uphold, reverse, or modify decisions. |
| FR-MOD-012 | Repeated abusive appeals are rate-limited. |
| FR-MOD-013 | P0/P1 reports have SLA and escalation path. |
| FR-MOD-014 | Unsafe animal-interaction signals trigger review or penalty. |
| FR-MOD-015 | Community rules explicitly ban feeding, chasing, touching wild animals, trespass, harassment, and location abuse. |
| FR-MOD-016 | Admin changes require elevated access and audit. |
| FR-MOD-017 | Admins can manage geofence/taxonomy/scoring policy versions. |
| FR-MOD-018 | Moderators see only case-needed evidence. |
| FR-MOD-019 | False reports can reduce reporter trust. |
| FR-MOD-020 | Critical incidents can temporarily disable public posting/map/rank features. |

### Notifications, Settings, And Support

| ID | Requirement |
|---|---|
| FR-NOTIF-001 | Users can receive score completion notification. |
| FR-NOTIF-002 | Users can receive friend/social notifications. |
| FR-NOTIF-003 | Users can disable notification categories. |
| FR-NOTIF-004 | Push tokens can be registered and revoked. |
| FR-NOTIF-005 | Notifications do not reveal sensitive exact locations. |
| FR-SET-001 | Users can manage privacy settings. |
| FR-SET-002 | Users can manage blocked users. |
| FR-SET-003 | Users can manage account deletion/export. |
| FR-SET-004 | Users can view app safety/community rules. |
| FR-SET-005 | Users can view scoring explanation policy. |
| FR-SUP-001 | Users can access support/contact path for moderation/privacy issues. |
| FR-SUP-002 | Store-review demo accounts can be provisioned later without exposing real data. |

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-PERF-001 | App cold start to usable home p95 <= 3s on mid-range Android; block alpha if >4s. |
| NFR-PERF-002 | Feed/leaderboard cached reads p95 <= 500ms; uncached <= 900ms. |
| NFR-PERF-003 | Map viewport query p95 <= 800ms for up to 100 visible clusters/cells. |
| NFR-PERF-004 | Submission returns durable pending state <= 2s p95 after upload completes. |
| NFR-PERF-005 | Automated scoring p50 <= 45s and p95 <= 3min, excluding manual review. |
| NFR-PERF-006 | Feeds never download original images by default. |
| NFR-SCALE-001 | Beta backend supports 10k DAU, 1k concurrent users, 100 RPS read peak. |
| NFR-SCALE-002 | Leaderboards handle 1M score events/day with <5min projection lag. |
| NFR-SCALE-003 | Duplicate/vector lookup p95 <= 1.5s at 1M image embeddings. |
| NFR-REL-001 | API availability: 99.5% beta, 99.9% production. |
| NFR-REL-002 | Submission pipeline job success >= 99%; retryable failures recover within 30min. |
| NFR-REL-003 | No user-visible loss of submitted captures. |
| NFR-PRIV-001 | Public map cells never expose exact coordinates. |
| NFR-PRIV-002 | Public location precision defaults to roughly 250m radius or coarser. |
| NFR-PRIV-003 | Public animal activity delayed >= 30min unless less precise. |
| NFR-PRIV-004 | EXIF GPS stripped from every public derivative. |
| NFR-PRIV-005 | Account deletion completes/anonymizes eligible data within defined retention, target <=30 days. |
| NFR-SEC-001 | All score and leaderboard writes are server-authoritative. |
| NFR-SEC-002 | 100% protected endpoints require valid auth and authorization. |
| NFR-SEC-003 | App Check/attestation enforced for scoring/upload where available. |
| NFR-SEC-004 | Rate limits exist for upload, scoring, comments, likes, reports, auth-sensitive flows. |
| NFR-SEC-005 | No secrets in repo, client, or release artifacts. |
| NFR-ACCESS-001 | Core flows meet WCAG 2.2 AA-equivalent mobile expectations. |
| NFR-ACCESS-002 | Primary touch targets >= 44x44 platform-equivalent where practical. |
| NFR-ACCESS-003 | All actionable controls have screen-reader labels. |
| NFR-MAINT-001 | Source files usually <=300 lines; >500 requires debt entry or generated-code exception. |
| NFR-MAINT-002 | Every non-trivial module has tests and module README. |
| NFR-MAINT-003 | Requirement IDs are linked in stories/tests/comments where useful. |
| NFR-OBS-001 | 100% API requests have trace/request ID, latency, status, and lawful user correlation. |
| NFR-OBS-002 | Crash-free sessions >=99.5% beta, >=99.8% production. |
| NFR-OBS-003 | Alerts exist for API errors, queue backlog, scoring latency, upload failures, location-leak incident class. |
| NFR-AUDIT-001 | 100% score changes store formula version, evidence IDs, model/prompt version, actor/source. |
| NFR-AUDIT-002 | 100% moderation/admin/deletion actions are append-only audited. |
| NFR-AUDIT-003 | Audit records query by user/submission/action within p95 <=5s at 1M rows. |
| NFR-COST-001 | Automated scoring variable cost target <= $0.05 average per submitted capture. |
| NFR-COST-002 | Monthly cloud cost forecast keeps 30% headroom against approved budget. |
| NFR-PORT-001 | iOS compile spike succeeds before Android production launch. |
| NFR-PORT-002 | Backend local setup completes within 30min on a fresh machine after scaffold exists. |
| NFR-LOC-001 | User-facing strings externalized by beta. |
| NFR-LOC-002 | Layout supports 30% longer strings and RTL smoke test. |
| NFR-ENERGY-001 | 15-minute map/capture session drains <=5% battery on mid-range Android. |
| NFR-ENERGY-002 | No continuous camera/GPS after leaving flow. |

## Requirement Traceability

Each story, test plan, ADR, and meaningful commit should list related requirement IDs. For work without direct user-facing behavior, use NFR or work-package IDs.
