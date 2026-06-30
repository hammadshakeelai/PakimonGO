# Agile Software Requirements Specification

## 1. Purpose

PakimonGO is a 13+ mobile animal photography, discovery, scoring, collection, map, and social competition app. This SRS defines the current gated Alpha-0 baseline for phased Agile delivery.

## 2. Scope

The system will let users photograph real animals, submit context, receive server-scored points, build collections, share posts selectively, explore privacy-safe animal activity on a map, and compete on global, country, local, and friends leaderboards.

Android APK/internal testing comes first. Android App Bundle, Google Play release, iOS/TestFlight, and App Store release come later.

## 3. Product Goals

- Make real animal discovery playful and rewarding.
- Encourage safe, respectful, honest animal observation.
- Build fair scoring that resists spam, duplicate farming, zoo farming, and collusive social abuse.
- Preserve privacy around exact locations, homes, pets, schools, minors, routines, and sensitive species.
- Support long-term growth into groups, social feeds, collections, and competitive leaderboards.
- Keep the codebase modular enough for many humans and AI agents to extend safely.

## 4. Product Non-Goals For Alpha-0

- No under-13 accounts.
- No background location.
- No exact public animal pins.
- No public release without moderation.
- No LLM-only scoring.
- No client-side final scoring.
- No required contacts import.
- No scientific authority claims.
- No reward for unsafe animal interaction.
- No unreviewed public rare/sensitive animal map.

## 5. Users And Stakeholders

- Player: captures animals, earns points, posts, and competes.
- Teen player: 13-17 user with stricter privacy/social defaults.
- Friend: interacts through leaderboards, groups, comments, likes, and shared posts.
- Pet owner: can receive tagged credit after consent when another user photographs their pet.
- Moderator: reviews reports, unsafe content, scoring appeals, and suspicious activity.
- Admin: manages taxonomies, scoring versions, geofences, policies, and operations.
- Bystanders/landowners: protected from unwanted location and social exposure.
- Animals and sensitive habitats: protected through safety rules and suppressed location behavior.

## 6. Gated Alpha-0 Boundaries

Alpha-0 is a product specification, not an unlimited public launch. Full social is planned in the design, but public/global exposure is feature-flagged until safety gates pass.

Initial implementation should prioritize:

- 13+ onboarding and safety education.
- Google and email/password auth.
- Camera draft capture.
- Foreground location only.
- Signed upload.
- Private collection.
- Pending score and score result state.
- Basic deterministic score event path.
- Duplicate and zoo/captive prechecks.
- Privacy-safe map cells.
- Invite-only friends path.
- Report/block foundations.

Social, groups, public feed, public comments, reposts, and global leaderboards are enabled only after moderation, privacy, and abuse gates pass.

## 7. Epics

### Epic 1: Identity, Age, And Consent

Users can create, access, recover, export, and delete accounts while respecting age and consent constraints.

Related requirements: `FR-AUTH-*`, `FR-AGE-*`, `FR-CONSENT-*`.

Acceptance:

- Google sign-in works.
- Email/password works.
- Password reset works.
- 13+ gate blocks under-13 accounts.
- Account deletion and export flows exist before store release.
- Consent version is stored before posting.

### Epic 2: Onboarding And Permissions

Users understand safety, privacy, scoring honesty, and permissions before capture or posting.

Related requirements: `FR-ONB-*`, `FR-PERM-*`.

Acceptance:

- Camera, foreground location, and optional contacts are explained just in time.
- Permission denial has usable fallbacks.
- Background location is not requested in Alpha-0.

### Epic 3: Capture, Drafts, Uploads, And Media

Users can capture animal photos, save drafts, add context, and upload safely.

Related requirements: `FR-CAP-*`.

Acceptance:

- Draft survives restart.
- Upload uses scoped signed URL and idempotent completion.
- Originals remain private.
- Public derivatives strip GPS EXIF.
- Unsupported files fail clearly.

### Epic 4: Taxonomy And Animal Context

The system stores user-provided names separately from AI/taxonomy evidence and supports corrections.

Related requirements: `FR-TAX-*`.

Acceptance:

- Taxon candidates and confidence are versioned.
- Low-confidence identification caps score or enters review.
- Sensitive species rules can override map behavior.

### Epic 5: Scoring And Economy

The server evaluates evidence, creates immutable score events, and updates leaderboards from valid events only.

Related requirements: `FR-SCORE-*`.

Acceptance:

- Client never assigns final score.
- Users do not see final points until scoring completes.
- Score explanation, formula version, evidence IDs, and state are stored.
- Zoo, pet, social, wild, and participation scoring remain separated.

### Epic 6: Duplicate And Zoo/Captive Controls

The system detects duplicate/repost farming and classifies zoo, captive, pet, and wild eligibility.

Related requirements: `FR-DUP-*`, `FR-ZOO-*`.

Acceptance:

- Hash, perceptual hash, crop, embedding, and encounter windows are modeled.
- Duplicate edges are stored and appealable.
- Zoo/captive uncertainty routes to capped/review state rather than brittle punishment.

### Epic 7: Collections, Profiles, And Privacy

Users can manage captures, collection pages, visibility, and profile exposure.

Related requirements: `FR-COL-*`.

Acceptance:

- Private captures remain private unless published.
- Visibility changes affect feed, map, and derivatives.
- Profiles show only user-approved content.

### Epic 8: Social, Friends, Groups, And UGC

Users can share selectively and interact with content behind trust and moderation gates.

Related requirements: `FR-SOC-*`.

Acceptance:

- Visibility supports private, public, friends, and selected friends.
- Invite links work before contacts import.
- Report/block/hide/delete are available before public exposure.
- Groups cannot bypass block or visibility rules.

### Epic 9: Maps, Routes, And Location Privacy

Users can explore game-like map activity without exposing exact animal locations.

Related requirements: `FR-MAP-*`.

Acceptance:

- Public map uses cells, clusters, delay, fuzzing, and suppression.
- Waypoint route targets general areas, not exact pins.
- Map queries are viewport bounded.
- Provider content terms are respected.

### Epic 10: Leaderboards And Competition

Users can compete globally, by country, locally, and with friends from server-valid score events.

Related requirements: `FR-LB-*`.

Acceptance:

- Quarantined scores do not rank.
- Rollbacks update projections.
- Local regions are privacy-safe.
- Social score cannot dominate wild discovery rank.

### Epic 11: Moderation, Appeals, Safety, And Admin

The system handles UGC abuse, unsafe animal interaction, scoring appeals, and admin policy operations.

Related requirements: `FR-MOD-*`.

Acceptance:

- Reports, blocks, appeals, takedowns, restoration, quarantine, rollback, and audit exist.
- Critical incidents can disable public posting, map, or rank features.
- Moderators only see case-needed evidence.

### Epic 12: Notifications, Settings, And Support

Users can manage notifications, privacy settings, blocked users, deletion/export, and support paths.

Related requirements: `FR-NOTIF-*`, `FR-SET-*`, `FR-SUP-*`.

Acceptance:

- Notification categories are opt-out.
- Notifications do not reveal exact sensitive locations.
- Privacy center exposes core choices and account actions.

## 8. Non-Functional Baseline

Use `docs/REQUIREMENTS.md` as the authoritative NFR catalogue. Launch-blocking NFR themes:

- Performance: startup, feed/rank, map query, upload pending state, async scoring latency.
- Scale: beta DAU/concurrency, leaderboard event volume, duplicate/vector lookup.
- Reliability: API availability, retry recovery, no visible capture loss.
- Privacy: exact coordinates private, public cells coarse/delayed, EXIF stripped, deletion target.
- Security: server-authoritative writes, authz, attestation, rate limits, no secrets.
- Accessibility: WCAG 2.2 AA-equivalent mobile behavior and screen-reader labels.
- Maintainability: usually <=300-line source files, module READMEs, tests, traceability.
- Observability: trace IDs, Crashlytics, alerts, audit trails, cost telemetry.
- Portability: iOS compile spike before Android production.

## 9. Agile Delivery Model

Use small work packages and short-burst semantic commits. Each coding task must have:

- Work package ID.
- Requirement IDs.
- Owned files/modules.
- Acceptance criteria.
- Test plan.
- Privacy/security notes.
- Rollback plan.
- State-doc update plan.
- Commit plan with AI attribution trailers where AI-authored.

## 10. Definition Of Ready

A story is ready only when:

- Requirement IDs are known.
- UX flow or API contract is clear.
- Data changes are described.
- Security/privacy impact is reviewed.
- Test approach is known.
- Dependencies are identified.
- Feature flags/readiness gates are defined where exposure is risky.

## 11. Definition Of Done

A story is done only when:

- Code is implemented in the correct module boundary.
- Tests are written and passing where practical.
- Manual verification is recorded for device, camera, map, or permission flows.
- Relevant docs, ADRs, OKF files, and state files are updated.
- No unresolved critical security/privacy issue remains.
- Commit is semantic, scoped, and includes required AI/handoff trailers when applicable.

## 12. Open Questions

- Which backend framework ADR is formally accepted?
- Will Mapbox or Google Maps win the prototype?
- Which AI provider mix gives best cost/accuracy/privacy?
- What is the first rarity taxonomy?
- What exact catch-up formula keeps the game fair?
- Which countries/regions are enabled first?
- What retention periods apply to originals, AI evidence, moderation evidence, and backups?
- Who moderates beta reports?
