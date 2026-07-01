# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

This SRS defines PakimonGO, a 13+ mobile animal photography, discovery, scoring, collection, map, and social competition app. It follows the reusable Software Engineering methodology from `C:/Users/HP/Documents/GitHub/projects/SE-Hakari-Bankai/docs/Software Engineering Process/METHODOLOGY.md`.

### 1.2 Product Overview

PakimonGO lets users safely photograph real animals, submit context, receive server-side surprise scoring, build collections, share selectively, and compete through privacy-safe leaderboards and map activity.

### 1.3 Problem Statement

- Existing animal apps are split between scientific observation, social posting, and fictional location games.
- Playful animal discovery can accidentally reward unsafe or invasive behavior if scoring is poorly designed.
- Real animal photos, exact locations, pet ownership, teen users, and social content create serious privacy and moderation risks.
- Fair scoring needs evidence, duplicate controls, zoo/captive handling, appeals, and auditability.
- A large AI-assisted project needs traceable requirements and small, modular implementation units to avoid context loss.

### 1.4 Vision

A cross-platform mobile system that turns safe real-world animal observations into scored collections, learning, and social competition through privacy-preserving capture, AI-assisted evidence, and server-authoritative game rules for 13+ users.

## 2. Scope

### 2.1 In Scope

- 13+ onboarding, safety education, consent, and privacy defaults.
- Google sign-in and email/password auth; Apple sign-in later for iOS.
- Camera capture, local drafts, upload retry, and media derivatives.
- Foreground location only; exact coordinates stored privately.
- Server-authoritative scoring with duplicate, zoo/captive, pet, rarity, safety, quality, and review states.
- Collections, profiles, visibility controls, friends, groups, posts, comments, likes, reposts, hashtags, reports, blocks, and appeals.
- Privacy-safe map cells/clusters and simple waypoint routing.
- Global, country, local, and friends leaderboards behind readiness gates.
- Admin/moderation tools, audit logs, score rollback, and incident switches.
- Android APK first, Android App Bundle later, iOS/TestFlight/App Store after Android readiness.

### 2.2 Out Of Scope For Alpha-0

- Under-13 accounts or family mode.
- Background location.
- Exact public animal pins.
- Public launch without moderation.
- LLM-only final scoring.
- Client-side final score or leaderboard writes.
- Required contacts import.
- Scientific authority claims.
- Rewards for unsafe interaction with animals.
- Unreviewed public rare/sensitive animal maps.

## 3. Users And Roles

| Actor | Primary Goal | Characteristics |
|---|---|---|
| Player | Capture animals, earn points, build collections, and compete. | Mobile-first, may be casual or competitive. |
| Teen Player | Use the game with stricter privacy defaults. | 13-17; needs extra privacy and safety defaults. |
| Friend | Interact through shared posts, friend leaderboard, and groups. | Must respect visibility and block rules. |
| Pet Owner | Receive optional shared credit for their pet. | Consent required before public owner-credit display. |
| Moderator | Review reports, appeals, unsafe behavior, and suspicious scores. | Needs purpose-limited evidence access. |
| Admin | Manage policies, geofences, taxonomy, scoring versions, regions, and incident switches. | Requires elevated audited access. |
| Store Reviewer | Validate app behavior and policy compliance. | Needs demo data and safe review flows. |
| External Provider | Supplies auth, map, storage, AI, or taxonomy evidence. | Never canonical product truth. |

## 4. Functional Requirements

The authoritative functional catalogue is `docs/REQUIREMENTS.md`. All requirements use stable IDs and are grouped as:

- `FR-AUTH-*`: identity, recovery, deletion, export, and provider linking.
- `FR-AGE-*`: 13+ launch and teen defaults.
- `FR-CONSENT-*`: policies, consent versions, and analytics opt-out.
- `FR-ONB-*`: onboarding, animal safety, privacy, scoring honesty, and AI fallibility.
- `FR-PERM-*`: just-in-time camera, location, and contacts permissions.
- `FR-CAP-*`: capture, drafts, uploads, media privacy, EXIF, and deletion.
- `FR-TAX-*`: taxonomy candidates, aliases, regional status, sensitivity, and appeals.
- `FR-SCORE-*`: server scoring, score states, ledgers, versioning, caps, rollback, and fairness.
- `FR-DUP-*`: duplicate, repost, encounter grouping, and appeal behavior.
- `FR-ZOO-*`: zoo, captive, pet, wild eligibility, geofences, honesty, and appeals.
- `FR-COL-*`: collection pages, profile privacy, visibility changes, and state labels.
- `FR-SOC-*`: posts, friends, groups, UGC, visibility, reports, blocks, hashtags, and appeals.
- `FR-MAP-*`: map activity, privacy cells, waypoint routing, provider terms, and suppression.
- `FR-LB-*`: global, country, local, friends leaderboards, windows, rollbacks, and gates.
- `FR-MOD-*`: moderation console, reports, appeals, admin policy, audits, and incident response.
- `FR-NOTIF-*`, `FR-SET-*`, `FR-SUP-*`: notifications, settings, support, deletion/export, and store-review support.

## 5. Non-Functional Requirements

The authoritative NFR catalogue is `docs/REQUIREMENTS.md`. Quality groups:

- Performance: startup, feed/rank reads, map queries, upload pending state, scoring latency.
- Scale: beta DAU, concurrent users, read peak, leaderboard volume, vector lookup.
- Reliability: API uptime, retry recovery, capture durability.
- Privacy: exact coordinates private, public cells coarse/delayed, EXIF stripped, deletion target.
- Security: server-authoritative writes, authorization, App Check, rate limits, no secrets.
- Accessibility: WCAG 2.2 AA-equivalent mobile behavior and screen-reader labels.
- Maintainability: small source files, module READMEs, traceability, local tests.
- Observability: trace IDs, Crashlytics, alerts, audit records, cost telemetry.
- Portability: iOS compile spike and reproducible backend setup.
- Energy/localization: no lingering camera/GPS, strings externalized, RTL/long-string smoke tests.

## 6. Constraints And Business Rules

### 6.1 Hard Domain Invariants

- Final scores and leaderboard writes are server-authoritative.
- Exact capture coordinates are never returned by public APIs for normal posts.
- Public animal activity is cell-based, clustered, delayed, fuzzed, or suppressed.
- Zoo/captive photos can be saved but do not earn normal wild leaderboard score.
- Honest zoo disclosure may earn only tiny bounded participation credit.
- Unsafe animal interaction can reduce score or trigger review.
- Sensitive species rules can suppress or coarsen map and local rank behavior.
- Duplicate decisions are stored as relationships and must be appealable.
- Score events are immutable; corrections use reversal or adjustment events.
- Public social exposure requires report, block, hide/delete, moderation, appeals, and audit.
- Under-13 users are blocked until a family mode is intentionally designed.

### 6.2 Technology Constraints

- Mobile direction: Flutter.
- Backend direction: FastAPI-style modular monolith plus workers.
- Data direction: PostgreSQL with PostGIS and pgvector.
- Auth direction: Firebase Auth with App Check and Play Integrity on Android.
- Storage direction: object storage for originals, derivatives, crops, and moderation evidence.
- Map direction: Mapbox-first prototype, Google Maps challenger.
- AI direction: hybrid deterministic checks plus structured vision evidence.

### 6.3 Process Constraints

- Follow the traceability chain: requirement -> use case -> domain concept -> class/operation -> SSD -> operation contract -> test.
- No production feature code before work package readiness.
- Keep implementation files usually <=300 lines.
- Use short-burst semantic commits with AI attribution trailers.
- Update current task, next task, thinking, backlog, risk, debt, and conversation archive when direction changes.

## 7. Validation Criteria

The SRS is valid only when:

- Every FR is testable and appears in `docs/TRACEABILITY_MATRIX.md`.
- Every Alpha-0 story has acceptance criteria and a test plan.
- Conflicts are resolved as scope decisions, not silent implementation choices.
- Risks around safety, privacy, scoring, moderation, and AI cost have explicit gates.
- ADR-001 through ADR-016 are accepted, revised, or deferred before feature implementation.

## 8. Related Artifacts

- Inception: `docs/software-engineering/00_INCEPTION.md`
- Process model: `docs/software-engineering/01_PROCESS_MODEL.md`
- Use cases: `docs/software-engineering/02_USE_CASES.md`
- Domain model: `docs/software-engineering/03_DOMAIN_MODEL.md`
- DFDs: `docs/software-engineering/04_DATA_FLOW_DIAGRAMS.md`
- Design classes: `docs/software-engineering/05_DESIGN_CLASS_DIAGRAM.md`
- SSDs: `docs/software-engineering/06_SYSTEM_SEQUENCE_DIAGRAMS.md`
- Operation contracts: `docs/software-engineering/07_OPERATION_CONTRACTS.md`
- Packages and CRC: `docs/software-engineering/08_PACKAGES_CRC.md`
- Final report plan: `docs/software-engineering/09_FINAL_REPORT_PLAN.md`
- Mermaid diagram pack: `docs/diagrams/README.md`
