# Test Case Catalogue

## Purpose

This catalogue turns requirements into concrete tests before implementation. Test IDs should be reused in code, CI reports, manual QA sheets, and release gate evidence.

## Priority And Automation

| Priority | Meaning |
|---|---|
| P0 | blocks launch or feature exposure |
| P1 | blocks internal alpha APK |
| P2 | blocks beta or public social/map/rank exposure |
| P3 | polish, regional, or later-scale coverage |

| Automation | Meaning |
|---|---|
| unit | pure function/model test |
| contract | schema/API/event test |
| integration | API, DB, storage, worker, provider adapter |
| e2e | full app/backend flow |
| goldset | controlled dataset benchmark |
| manual | device, accessibility, operational, or human review |
| abuse | adversarial/security simulation |

## Catalogue

| ID | Requirement IDs | Priority | Automation | Gate | Expected Result |
|---|---|---|---|---|---|
| TC-AUTH-001 | FR-AUTH-001 | P1 | e2e | alpha auth | Google sign-in creates or resumes account |
| TC-AUTH-002 | FR-AUTH-002 | P1 | e2e | alpha auth | email/password signup creates account |
| TC-AUTH-003 | FR-AUTH-002 | P1 | e2e | alpha auth | email/password signin resumes account |
| TC-AUTH-004 | FR-AUTH-003 | P1 | integration | alpha auth | password reset email can be requested |
| TC-AUTH-005 | FR-AUTH-004 | P2 | integration | beta auth | phone recovery obeys abuse and cost policy |
| TC-AUTH-006 | FR-AUTH-005 | P2 | manual | iOS gate | Sign in with Apple exists when iOS offers third-party login |
| TC-AUTH-007 | FR-AUTH-006 | P1 | e2e | account settings | deletion request can be started in app |
| TC-AUTH-008 | FR-AUTH-007 | P1 | integration | account settings | deletion/anonymization job records completion |
| TC-AUTH-009 | FR-AUTH-008 | P2 | integration | privacy gate | export returns machine-readable user data |
| TC-AUTH-010 | FR-AUTH-009 | P1 | abuse | auth security | provider linking cannot take over another account |
| TC-AUTH-011 | FR-AUTH-010 | P1 | integration | auth security | sensitive action requires reauthentication |
| TC-AUTH-012 | FR-AUTH-011 | P1 | e2e | alpha auth | user can sign out |
| TC-AUTH-013 | FR-AUTH-012 | P2 | abuse | beta abuse | suspicious account activity can trigger risk review |
| TC-AGE-001 | FR-AGE-001 | P0 | e2e | account gate | launch includes neutral age gate |
| TC-AGE-002 | FR-AGE-002 | P0 | e2e | account gate | under-13 path is blocked or diverted |
| TC-AGE-003 | FR-AGE-003 | P0 | unit | privacy gate | teen defaults are stricter than adult defaults |
| TC-CONSENT-001 | FR-CONSENT-001 | P1 | e2e | posting gate | user must accept current policies before posting |
| TC-CONSENT-002 | FR-CONSENT-002 | P1 | integration | audit gate | consent stores version, timestamp, user ID |
| TC-CONSENT-003 | FR-CONSENT-003 | P1 | integration | posting gate | policy update can force re-acknowledgement |
| TC-CONSENT-004 | FR-CONSENT-004 | P2 | e2e | settings | user can review permission/privacy choices |
| TC-CONSENT-005 | FR-CONSENT-005 | P2 | e2e | privacy gate | analytics opt-out is available where required |
| TC-ONB-001 | FR-ONB-001 | P1 | manual | alpha APK | onboarding explains safety, privacy, scoring, conduct, permissions |
| TC-ONB-002 | FR-ONB-002 | P0 | manual | map gate | onboarding says exact locations are not public by default |
| TC-ONB-003 | FR-ONB-003 | P0 | manual | score gate | onboarding says zoo/pet/captive photos do not earn normal wild score |
| TC-ONB-004 | FR-ONB-004 | P0 | manual | safety gate | onboarding says unsafe interaction can reduce score or trigger review |
| TC-ONB-005 | FR-ONB-005 | P1 | manual | score gate | onboarding says AI can be wrong and appeals exist |
| TC-PERM-001 | FR-PERM-001 | P1 | manual | alpha APK | camera permission asks only on capture |
| TC-PERM-002 | FR-PERM-002 | P1 | manual | alpha APK | foreground location asks only for map/submission |
| TC-PERM-003 | FR-PERM-003 | P0 | manual | alpha APK | background location is not requested |
| TC-PERM-004 | FR-PERM-004 | P1 | manual | social gate | contacts permission is not required |
| TC-PERM-005 | FR-PERM-005 | P1 | e2e | social gate | invite links work without contacts |
| TC-PERM-006 | FR-PERM-006 | P1 | manual | alpha APK | permission denial shows usable fallback |
| TC-PERM-007 | FR-PERM-007 | P1 | manual | alpha APK | permission explanations are contextual and non-coercive |
| TC-CAP-001 | FR-CAP-001 | P1 | manual | alpha APK | in-app camera opens |
| TC-CAP-002 | FR-CAP-002 | P1 | manual | alpha APK | photo capture creates image evidence |
| TC-CAP-003 | FR-CAP-003 | P1 | unit | capture slice | local draft is created before upload |
| TC-CAP-004 | FR-CAP-004 | P1 | e2e | capture slice | draft survives restart |
| TC-CAP-005 | FR-CAP-005 | P1 | e2e | capture slice | user can mark wild, pet, zoo/captive, unknown |
| TC-CAP-006 | FR-CAP-006 | P2 | e2e | collection | real name, cute name, caption, tags can be saved |
| TC-CAP-007 | FR-CAP-007 | P1 | e2e | privacy gate | visibility is chosen before publishing |
| TC-CAP-008 | FR-CAP-008 | P0 | unit | privacy gate | default visibility is private |
| TC-CAP-009 | FR-CAP-009 | P1 | integration | capture slice | location accuracy is stored when permission exists |
| TC-CAP-010 | FR-CAP-010 | P1 | e2e | capture slice | location denial follows private/limited-score policy |
| TC-UPLOAD-001 | FR-CAP-011 | P0 | integration | upload gate | signed upload URL is short-lived |
| TC-UPLOAD-002 | FR-CAP-012 | P0 | integration | upload gate | upload completion is idempotent |
| TC-UPLOAD-003 | FR-CAP-013 | P1 | e2e | upload gate | failed upload retries without duplicate submission |
| TC-MEDIA-001 | FR-CAP-014 | P0 | contract | privacy gate | originals remain private |
| TC-MEDIA-002 | FR-CAP-015 | P0 | integration | privacy gate | public derivatives strip EXIF GPS |
| TC-MEDIA-003 | FR-CAP-016 | P2 | e2e | feed gate | feeds and collections use thumbnails by default |
| TC-MEDIA-004 | FR-CAP-017 | P1 | integration | upload gate | unsupported/corrupt/oversized files are rejected |
| TC-MEDIA-005 | FR-CAP-018 | P3 | integration | beta capture | multi-animal photo creates primary plus candidates |
| TC-CAP-011 | FR-CAP-019 | P1 | e2e | capture slice | user can delete draft |
| TC-CAP-012 | FR-CAP-020 | P1 | e2e | content control | user can delete or unpublish eligible post |
| TC-TAX-001 | FR-TAX-001 | P2 | integration | AI gate | taxon candidates store confidence |
| TC-TAX-002 | FR-TAX-002 | P2 | unit | taxonomy gate | taxa use stable external IDs where available |
| TC-TAX-003 | FR-TAX-003 | P2 | integration | taxonomy gate | taxonomy imports are versioned |
| TC-TAX-004 | FR-TAX-004 | P2 | unit | taxonomy gate | accepted names, synonyms, common names are tracked |
| TC-TAX-005 | FR-TAX-005 | P2 | unit | region gate | regional species status can be recorded |
| TC-TAX-006 | FR-TAX-006 | P2 | unit | region gate | establishment means and degree are modeled |
| TC-TAX-007 | FR-TAX-007 | P0 | contract | sensitive species gate | sensitive taxon overrides public map behavior |
| TC-TAX-008 | FR-TAX-008 | P0 | unit | score gate | low confidence caps score or sends review |
| TC-TAX-009 | FR-TAX-009 | P1 | unit | collection | user name stored separately from AI/taxonomy result |
| TC-TAX-010 | FR-TAX-010 | P2 | e2e | appeals | user can appeal or correct identification |
| TC-SCORE-001 | FR-SCORE-001 | P0 | unit | score gate | scoring uses species, rarity, quality, safety, novelty, duplicate, abuse signals |
| TC-SCORE-002 | FR-SCORE-002 | P0 | abuse | score gate | client cannot assign final score |
| TC-SCORE-003 | FR-SCORE-003 | P1 | e2e | score gate | user cannot see points until server scoring completes |
| TC-SCORE-004 | FR-SCORE-004 | P1 | contract | score gate | score stores explanation fields |
| TC-SCORE-005 | FR-SCORE-005 | P0 | integration | audit gate | score events are immutable |
| TC-SCORE-006 | FR-SCORE-006 | P0 | integration | audit gate | corrections use reversal/adjustment events |
| TC-SCORE-007 | FR-SCORE-007 | P0 | unit | score gate | formula version stored on every score event |
| TC-SCORE-008 | FR-SCORE-008 | P0 | unit | score gate | state machine supports required states |
| TC-SCORE-009 | FR-SCORE-009 | P0 | integration | zoo gate | zoo/captive photos save but skip normal wild leaderboard score |
| TC-SCORE-010 | FR-SCORE-010 | P2 | unit | economy gate | honest zoo disclosure receives tiny bounded credit |
| TC-SCORE-011 | FR-SCORE-011 | P0 | unit | economy gate | repeated zoo uploads hit diminishing returns |
| TC-SCORE-012 | FR-SCORE-012 | P1 | unit | pet gate | pets receive pet/social score but not wild rarity |
| TC-SCORE-013 | FR-SCORE-013 | P2 | integration | pet gate | pet owner credit waits for owner acceptance |
| TC-SCORE-014 | FR-SCORE-014 | P2 | abuse | economy gate | social engagement points are capped and fraud-damped |
| TC-SCORE-015 | FR-SCORE-015 | P1 | unit | economy gate | wild, pet/social, participation ledgers are separate |
| TC-SCORE-016 | FR-SCORE-016 | P0 | abuse | safety gate | unsafe interaction reduces score or triggers review |
| TC-SCORE-017 | FR-SCORE-017 | P0 | integration | score gate | high-risk submissions are quarantined from leaderboards |
| TC-SCORE-018 | FR-SCORE-018 | P2 | unit | economy gate | new/low-score users can receive catch-up boosts |
| TC-SCORE-019 | FR-SCORE-019 | P2 | unit | economy gate | high-score users face diminishing returns |
| TC-SCORE-020 | FR-SCORE-020 | P0 | integration | leaderboard gate | rollback updates leaderboard projections |
| TC-DUP-001 | FR-DUP-001 | P0 | unit | duplicate gate | exact duplicate hash detects same file |
| TC-DUP-002 | FR-DUP-002 | P0 | goldset | duplicate gate | perceptual hash detects near duplicates |
| TC-DUP-003 | FR-DUP-003 | P0 | goldset | duplicate gate | crop-level duplicate matching catches cropped repost |
| TC-DUP-004 | FR-DUP-004 | P0 | goldset | duplicate gate | embeddings detect semantic duplicate candidates |
| TC-DUP-005 | FR-DUP-005 | P0 | integration | duplicate gate | duplicate window uses user/device/time/location/species |
| TC-DUP-006 | FR-DUP-006 | P0 | integration | duplicate gate | duplicate relationships are stored as edges |
| TC-DUP-007 | FR-DUP-007 | P1 | integration | capture slice | same-encounter photos can be grouped |
| TC-DUP-008 | FR-DUP-008 | P2 | e2e | collection | replacement photo does not farm points |
| TC-DUP-009 | FR-DUP-009 | P2 | goldset | score gate | material animal change can create score-eligible event |
| TC-DUP-010 | FR-DUP-010 | P0 | abuse | abuse gate | web-scraped/reposted suspicion zeroes score or triggers review |
| TC-DUP-011 | FR-DUP-011 | P2 | e2e | appeals | false duplicate can be appealed |
| TC-DUP-012 | FR-DUP-012 | P0 | unit | duplicate gate | duplicate thresholds are versioned |
| TC-ZOO-001 | FR-ZOO-001 | P0 | integration | zoo gate | system classifies wild/pet/zoo/captive/sensitive/review |
| TC-ZOO-002 | FR-ZOO-002 | P0 | integration | zoo gate | zoo decision uses geofence, disclosure, GPS, image context, venue data |
| TC-ZOO-003 | FR-ZOO-003 | P0 | integration | zoo gate | GPS uncertainty overlap routes to cap/review, not automatic penalty |
| TC-ZOO-004 | FR-ZOO-004 | P0 | unit | zoo gate | geofence datasets are versioned |
| TC-ZOO-005 | FR-ZOO-005 | P2 | integration | zoo gate | OSM/curated sources can seed geofences |
| TC-ZOO-006 | FR-ZOO-006 | P1 | unit | economy gate | honest zoo/pet/captive context is rewarded more than punished |
| TC-ZOO-007 | FR-ZOO-007 | P0 | abuse | abuse gate | repeated misleading wild claims lower trust |
| TC-ZOO-008 | FR-ZOO-008 | P2 | e2e | pet gate | owner consent required before public owner-credit display |
| TC-ZOO-009 | FR-ZOO-009 | P1 | unit | pet gate | domestic species default toward pet/captive review |
| TC-ZOO-010 | FR-ZOO-010 | P2 | e2e | appeals | captive/wild decision is appealable |
| TC-COL-001 | FR-COL-001 | P1 | e2e | collection | user can view personal collection |
| TC-COL-002 | FR-COL-002 | P1 | e2e | collection | collection entries show pending/scored/review/capped |
| TC-COL-003 | FR-COL-003 | P1 | e2e | collection | entries label wild, pet, zoo/captive, unknown, review |
| TC-COL-004 | FR-COL-004 | P2 | e2e | collections | user can create collection pages |
| TC-COL-005 | FR-COL-005 | P2 | e2e | collections | user can organize by animal, region, date, tag, custom collection |
| TC-COL-006 | FR-COL-006 | P0 | contract | privacy gate | private captures remain private unless published |
| TC-COL-007 | FR-COL-007 | P1 | e2e | privacy gate | visibility can be changed after posting |
| TC-COL-008 | FR-COL-008 | P1 | integration | privacy gate | visibility changes update feed/map/public derivatives |
| TC-COL-009 | FR-COL-009 | P1 | contract | profile gate | profiles show only approved visible content |
| TC-COL-010 | FR-COL-010 | P2 | e2e | profile gate | profile privacy controls stats and previews |
| TC-SOC-001 | FR-SOC-001 | P0 | contract | social gate | private/public/friends/selected-friends visibility works |
| TC-SOC-002 | FR-SOC-002 | P2 | e2e | social gate | users can like visible posts |
| TC-SOC-003 | FR-SOC-003 | P2 | e2e | social gate | users can comment on visible posts |
| TC-SOC-004 | FR-SOC-004 | P2 | e2e | social gate | repost/share follows visibility |
| TC-SOC-005 | FR-SOC-005 | P2 | e2e | social gate | captions and hashtags save |
| TC-SOC-006 | FR-SOC-006 | P0 | abuse | social gate | blocked users cannot view restricted content |
| TC-SOC-007 | FR-SOC-007 | P0 | e2e | moderation gate | reporting exists for UGC surfaces |
| TC-SOC-008 | FR-SOC-008 | P1 | e2e | content control | users can hide/delete their own posts |
| TC-SOC-009 | FR-SOC-009 | P0 | contract | social gate | feed respects visibility/block/moderation/sensitive rules |
| TC-SOC-010 | FR-SOC-010 | P0 | integration | social gate | public feed is feature-flagged until moderation gate passes |
| TC-SOC-011 | FR-SOC-011 | P2 | e2e | friends | friends can be added by invite link |
| TC-SOC-012 | FR-SOC-012 | P2 | manual | contacts | contacts import is optional/deferred |
| TC-SOC-013 | FR-SOC-013 | P2 | e2e | friends | friend leaderboard works without contacts upload |
| TC-SOC-014 | FR-SOC-014 | P2 | integration | groups | groups support owner/mod/member roles |
| TC-SOC-015 | FR-SOC-015 | P0 | contract | groups | group posts cannot bypass visibility/block |
| TC-SOC-016 | FR-SOC-016 | P2 | integration | groups | group membership/posting can be moderated |
| TC-SOC-017 | FR-SOC-017 | P0 | contract | hashtag gate | hashtags cannot expose exact location/sensitive species |
| TC-SOC-018 | FR-SOC-018 | P2 | abuse | social abuse | suspicious likes/reposts are damped |
| TC-SOC-019 | FR-SOC-019 | P2 | e2e | comments | public comments can be limited/hidden/disabled |
| TC-SOC-020 | FR-SOC-020 | P2 | e2e | appeals | users can appeal moderation decisions |
| TC-MAP-001 | FR-MAP-001 | P1 | manual | map gate | map shows player location only with permission |
| TC-MAP-002 | FR-MAP-002 | P3 | manual | UX gate | map uses game-like styling |
| TC-MAP-003 | FR-MAP-003 | P0 | contract | map gate | public activity uses cells/clusters/delay/fuzzing |
| TC-MAP-004 | FR-MAP-004 | P0 | contract | privacy gate | public APIs never return exact capture coordinates |
| TC-MAP-005 | FR-MAP-005 | P0 | contract | sensitive species gate | sensitive/home/school-like areas are coarser/suppressed |
| TC-MAP-006 | FR-MAP-006 | P1 | integration | map gate | queries are viewport-bounded |
| TC-MAP-007 | FR-MAP-007 | P2 | e2e | map gate | map shows species/activity summaries by area |
| TC-MAP-008 | FR-MAP-008 | P0 | e2e | route gate | waypoint routes to general area, not exact animal pin |
| TC-MAP-009 | FR-MAP-009 | P1 | manual | route gate | route feature works without background location |
| TC-MAP-010 | FR-MAP-010 | P2 | manual | provider gate | map provider content terms are respected |
| TC-MAP-011 | FR-MAP-011 | P2 | e2e | resilience | map outage falls back to cached/list view |
| TC-MAP-012 | FR-MAP-012 | P2 | manual | OSM gate | OSM attribution appears where required |
| TC-MAP-013 | FR-MAP-013 | P0 | contract | leaderboard gate | local leaderboard regions use privacy-safe cells |
| TC-MAP-014 | FR-MAP-014 | P0 | contract | privacy gate | public map data is delayed by default |
| TC-MAP-015 | FR-MAP-015 | P2 | e2e | UX gate | user can view safe explanation for hidden/coarsened location |
| TC-LB-001 | FR-LB-001 | P2 | integration | leaderboard gate | global leaderboard is gated |
| TC-LB-002 | FR-LB-002 | P2 | integration | region gate | country leaderboard respects region policy |
| TC-LB-003 | FR-LB-003 | P0 | contract | privacy gate | local leaderboard uses privacy-safe regions |
| TC-LB-004 | FR-LB-004 | P2 | e2e | friends | friends leaderboard is supported |
| TC-LB-005 | FR-LB-005 | P0 | integration | leaderboard gate | only valid score events rank |
| TC-LB-006 | FR-LB-006 | P0 | integration | abuse gate | quarantined scores do not rank |
| TC-LB-007 | FR-LB-007 | P2 | unit | leaderboard gate | periods support all-time and rolling windows |
| TC-LB-008 | FR-LB-008 | P2 | unit | leaderboard gate | ties are deterministic |
| TC-LB-009 | FR-LB-009 | P0 | integration | leaderboard gate | score rollback updates all leaderboards |
| TC-LB-010 | FR-LB-010 | P1 | e2e | score gate | pending/review status is visible |
| TC-LB-011 | FR-LB-011 | P2 | manual | economy gate | catch-up mechanics feel fair |
| TC-LB-012 | FR-LB-012 | P2 | unit | economy gate | high-score diminishing returns are testable |
| TC-LB-013 | FR-LB-013 | P0 | contract | privacy gate | local leaderboard hides too-small regions |
| TC-LB-014 | FR-LB-014 | P0 | unit | economy gate | social score cannot dominate wild rank |
| TC-LB-015 | FR-LB-015 | P2 | integration | region gate | admins can disable leaderboard scopes by region |
| TC-MOD-001 | FR-MOD-001 | P0 | e2e | moderation gate | user can report content |
| TC-MOD-002 | FR-MOD-002 | P0 | e2e | moderation gate | user can report user |
| TC-MOD-003 | FR-MOD-003 | P0 | e2e | moderation gate | user can block user |
| TC-MOD-004 | FR-MOD-004 | P1 | e2e | content control | user can hide/delete own content |
| TC-MOD-005 | FR-MOD-005 | P0 | manual | social gate | moderator console supports report review |
| TC-MOD-006 | FR-MOD-006 | P0 | manual | score gate | moderator console supports score appeal review |
| TC-MOD-007 | FR-MOD-007 | P0 | integration | moderation gate | takedown/restoration are supported |
| TC-MOD-008 | FR-MOD-008 | P0 | integration | moderation gate | score rollback/quarantine supported |
| TC-MOD-009 | FR-MOD-009 | P0 | integration | audit gate | moderation actions are audited |
| TC-MOD-010 | FR-MOD-010 | P2 | integration | moderation gate | users are notified of major decisions where safe/legal |
| TC-MOD-011 | FR-MOD-011 | P2 | integration | appeals | appeals can uphold/reverse/modify decisions |
| TC-MOD-012 | FR-MOD-012 | P2 | abuse | moderation abuse | repeated abusive appeals are rate-limited |
| TC-MOD-013 | FR-MOD-013 | P0 | manual | ops gate | P0/P1 reports have SLA and escalation path |
| TC-MOD-014 | FR-MOD-014 | P0 | abuse | safety gate | unsafe animal interaction triggers review/penalty |
| TC-MOD-015 | FR-MOD-015 | P0 | manual | safety gate | rules ban feeding/chasing/touching wild animals, trespass, harassment, location abuse |
| TC-MOD-016 | FR-MOD-016 | P0 | integration | admin gate | admin changes require elevated access and audit |
| TC-MOD-017 | FR-MOD-017 | P2 | integration | policy gate | admins can manage geofence/taxonomy/scoring policy versions |
| TC-MOD-018 | FR-MOD-018 | P0 | contract | privacy gate | moderators see only case-needed evidence |
| TC-MOD-019 | FR-MOD-019 | P2 | abuse | moderation abuse | false reports can reduce reporter trust |
| TC-MOD-020 | FR-MOD-020 | P0 | integration | incident gate | incident switch disables public posting/map/rank |
| TC-NOTIF-001 | FR-NOTIF-001 | P2 | manual | beta | score completion notification can be received |
| TC-NOTIF-002 | FR-NOTIF-002 | P2 | manual | beta | friend/social notification can be received |
| TC-NOTIF-003 | FR-NOTIF-003 | P2 | e2e | settings | notification categories can be disabled |
| TC-NOTIF-004 | FR-NOTIF-004 | P2 | integration | beta | push tokens register and revoke |
| TC-NOTIF-005 | FR-NOTIF-005 | P0 | contract | privacy gate | notification payloads do not reveal exact locations |
| TC-SET-001 | FR-SET-001 | P1 | e2e | settings | privacy settings can be managed |
| TC-SET-002 | FR-SET-002 | P1 | e2e | settings | blocked users can be managed |
| TC-SET-003 | FR-SET-003 | P1 | e2e | settings | deletion/export paths are available |
| TC-SET-004 | FR-SET-004 | P1 | e2e | settings | safety/community rules are viewable |
| TC-SET-005 | FR-SET-005 | P1 | e2e | score gate | scoring explanation policy is viewable |
| TC-SUP-001 | FR-SUP-001 | P2 | manual | beta | support/contact path exists for moderation/privacy |
| TC-SUP-002 | FR-SUP-002 | P3 | manual | store gate | store-review demo accounts can be provisioned safely |

## Use Rule

When implementation starts, do not create a new ad hoc test ID if a catalogue ID already matches. If a behavior is missing, add the test here first, then add code.
