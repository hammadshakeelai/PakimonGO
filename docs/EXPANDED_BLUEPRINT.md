# PakimonGO Expanded Deep Planning Blueprint

## 1. Executive Summary

PakimonGO is a 13+ real-animal discovery, photography, map, collection, scoring, and social competition app. Users notice real animals, photograph them safely, submit context, receive a surprise server-side score, grow collections, share selectively, and compete without exposing exact locations or incentivizing animal harm.

The active baseline is a gated Alpha-0. Full social capability is planned in the product and architecture, but public/global exposure stays behind moderation, privacy, abuse, scoring, and legal readiness gates.

Recommended architecture:

- Mobile: Flutter.
- Auth: Firebase Auth, App Check, Play Integrity on Android, Sign in with Apple later for iOS.
- Backend: FastAPI modular monolith plus worker.
- Data: Cloud SQL PostgreSQL with PostGIS and pgvector.
- Storage: Cloud Storage/Firebase Storage backed by GCS.
- Maps: Mapbox-first prototype, Google Maps challenger.
- AI: hybrid evidence pipeline with structured vision outputs, deterministic checks, taxonomy/range grounding, duplicate detection, geofence checks, and review states.
- Delivery: Android APK for internal testing, Android App Bundle for Play production, iOS/TestFlight later.

The product must avoid becoming an animal bounty app. No points should reward chasing, touching, feeding, disturbing, baiting, trespassing, zoo farming, duplicate spam, or exact-location exposure.

## 2. Current-State Assessment

Existing state:

- Planning docs and scaffold exist.
- No production app/backend implementation exists yet.
- Git was repaired with a fresh repository initialization on 2026-07-01.
- Scaffolded monorepo folders now exist for mobile, backend, workers, packages, infrastructure, data, tools, and knowledge outputs.

Main remaining readiness gaps:

- Missing ADRs remain for backend framework, moderation, retention/deletion/export, age policy, sensitive species, AI data sharing, observability, analytics, deployment, and release process.
- Detailed requirement cards still need story-level acceptance criteria.
- Alpha-0 implementation sequence must be frozen before feature coding.

## 3. Product Definition

Vision: a respectful real-world animal discovery game where players capture moments, learn about animals, build collections, and compete safely.

Problem: existing tools are split between scientific observation apps, social media, and fictional location games. PakimonGO aims for a playful animal-photo game with credible welfare, privacy, anti-cheat, and UGC safety.

Primary success metrics:

- First capture completion rate.
- Capture-to-score completion rate.
- Percentage of submissions with understandable score explanations.
- Duplicate/zoo false-positive and false-negative rates.
- Public exact-location leak count: zero.
- Report/block SLA compliance.
- Retention after first scored capture.
- Score appeal reversal rate.
- Crash-free sessions.
- AI/scoring cost per submitted capture.
- Low-end Android capture/upload success rate.

Alpha-0 non-goals:

- No under-13 accounts.
- No background location.
- No exact public animal pins.
- No public release without moderation.
- No LLM-only scoring.
- No client-side final scoring.
- No required contacts import.
- No scientific authority claims.
- No reward for unsafe animal interaction.
- No unreviewed public map of rare or sensitive animals.

## 4. Release Model

Release rings:

- Ring 0: local developer/staging.
- Ring 1: internal APK.
- Ring 2: invited Android alpha.
- Ring 3: closed Play testing.
- Ring 4: open beta with limited public social.
- Ring 5: Android production.
- Ring 6: iOS TestFlight.
- Ring 7: iOS production.

Alpha-0 can be globally designed, but runtime availability must be controlled by region configuration and feature flags.

## 5. Architecture Baseline

Use a modular monolith first:

- Flutter mobile app.
- FastAPI API deployable.
- Python worker deployable.
- PostgreSQL/PostGIS/pgvector canonical state.
- Object storage for originals, derivatives, crops, and moderation evidence.
- Firebase Auth/App Check for identity and app attestation.
- Cloud Tasks first; Pub/Sub later for broader fan-out.
- Redis/Valkey later for cache only, not source of truth.
- OpenTelemetry backend, Crashlytics mobile, Cloud Logging/Monitoring.
- Provider adapters for AI, maps, auth, storage, taxonomy, geofences, and notifications.

Rejected first moves:

- Firebase-only product backend.
- Native Android-only implementation.
- Distributed microservices first.
- LLM-only scoring.
- Exact public pins.

## 6. Quality Gates

| Gate | Evidence Required |
|---|---|
| Product Readiness | Refined problem, 13+ policy, gated Alpha-0 scope, non-goals, success metrics. |
| SRS Readiness | Expanded requirements, measurable NFRs, traceability, contradiction register resolved. |
| Architecture Readiness | ADRs accepted, alternatives compared, source of truth defined, provider boundaries defined. |
| Security/Privacy Readiness | Threat model, data inventory, exact-location leak tests planned, UGC controls specified. |
| AI/Scoring Readiness | Goldsets planned, thresholds defined, versioning/review/appeal states specified. |
| Implementation Readiness | Work packages, acceptance criteria, test plan, rollback, state-doc workflow. |
| Alpha Readiness | Auth/capture/upload/private collection/scoring state works; no exact public leaks. |
| Social Exposure Readiness | Report/block/hide/delete/moderation/appeals/SLA/audit are operational. |
| Global Exposure Readiness | Region config, privacy notices, rarity/taxonomy/geofence policy, legal review. |
| Production Readiness | Observability, runbooks, DR, backups, store disclosures, security review, load tests. |

## 7. Delivery Roadmap

Stage 0: planning closure and repo health.

- Repair Git.
- Update docs with expanded plan.
- Accept or revise ADRs.
- Draft missing ADRs.
- Define Alpha-0 gates.
- Freeze planning baseline.

Stage 1: spec and UX validation.

- Expand requirement cards.
- Create UX flows.
- Validate onboarding, privacy, and scoring comprehension.
- Run abuse tabletop.

Stage 2: technical spikes.

- Flutter camera/location/upload.
- Mapbox vs Google.
- FastAPI local stack.
- PostGIS/geofence/privacy-cell queries.
- pgvector duplicate benchmark.
- AI structured scoring benchmark.
- Moderation workflow.

Stage 3: scaffold and foundation.

- Flutter shell.
- API/worker shell.
- Local DB.
- OpenAPI.
- Signed upload.
- CI checks.

Stage 4: vertical slice.

- 13+ onboarding.
- Auth.
- Capture.
- Upload.
- Private collection.
- Pending score.
- Basic deterministic score.
- Zoo/duplicate flags.
- Privacy transform.

Stage 5: gated social/map/rank.

- Friends/invites.
- Feed/comments/likes/reposts.
- Groups.
- Report/block/moderation.
- Privacy-safe map.
- Four leaderboard scopes behind flags.

Stage 6: hardening.

- Goldsets.
- Fraud/abuse testing.
- Accessibility.
- Performance.
- Observability.
- Incident response.
- Store policy.

Stage 7: Android alpha/beta.

- Signed APK.
- Internal users.
- AAB closed testing.
- Crash/performance/moderation monitoring.

Stage 8: production and iOS.

- Android production.
- iOS compile spike.
- Sign in with Apple.
- TestFlight.
- App Store release.

## 8. Work Breakdown Structure

| ID | Work Package | Owner Type | Dependencies | Acceptance |
|---|---|---|---|---|
| WP-001 | Repair Git/repo health | Dev lead | none | `git status` works or repo intentionally initialized. |
| WP-002 | Expand SRS/requirements | Product/BA | blueprint | 100+ requirements accepted. |
| WP-003 | ADR completion pack | Architect | SRS | missing ADRs drafted. |
| WP-004 | UX safety blueprint | UX lead | age policy | core flows and states approved. |
| WP-005 | Security/privacy model | Security lead | data model | threat model and controls mapped. |
| WP-006 | Data governance plan | Data lead | architecture | retention/source-of-truth accepted. |
| WP-007 | API contract pack | Backend lead | architecture | OpenAPI/event standards accepted. |
| WP-008 | AI scoring benchmark plan | AI/data lead | goldset plan | thresholds and datasets defined. |
| WP-009 | Map provider spike plan | Mobile/geo lead | ADR-003 | validation criteria accepted. |
| WP-010 | Moderation operations plan | Trust/safety lead | UGC scope | queues, roles, SLA, runbooks defined. |
| WP-011 | Reliability plan | SRE | NFRs | SLOs, alerts, runbooks, DR targets accepted. |
| WP-012 | Alpha implementation strategy | TPM/architect | all above | workstreams, sequencing, gates defined. |
| WP-013 | Scaffold monorepo skeleton | Dev lead | WP-001 | module folders and README boundaries exist. |
| WP-014 | Commit workflow policy | Dev lead | WP-001 | short-burst commit policy and template exist. |

## 9. Risk Register

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---:|---:|---|
| R-001 | Product incentivizes animal harm | Medium | Critical | Safety scoring, no unsafe interaction reward, review. |
| R-002 | Exact location leak | Medium | Critical | Private exact coords, cells, delay, tests, incident runbook. |
| R-003 | Sensitive species exposure | Medium | Critical | Sensitive taxon policy, suppression, review. |
| R-004 | UGC moderation overload | High | High | Gated social, moderation console, SLA, report/block first. |
| R-005 | AI scoring feels unfair | High | High | Explanations, confidence thresholds, appeals, goldsets. |
| R-006 | Duplicate/zoo farming corrupts rankings | High | High | Geofences, hashes, embeddings, trust scores, rollback. |
| R-007 | Full global/social Alpha-0 is too wide | High | High | Feature flags, release rings, gates. |
| R-008 | Under-13 accidental use creates compliance exposure | Medium | High | Neutral age gate, 13+ launch, no child-directed positioning. |
| R-009 | Cloud/AI costs exceed budget | Medium | High | Cost telemetry, caps, staged AI pipeline. |
| R-010 | Map provider terms block desired UX | Medium | High | Provider ADR, avoid incompatible data mixing. |
| R-011 | Backend overcomplexity slows MVP | Medium | Medium | Modular monolith, no microservices first. |
| R-012 | Low-end Android performance poor | Medium | High | Device testing, startup/upload/battery NFRs. |
| R-013 | Store/privacy docs incomplete | Medium | High | Store checklist, data inventory, privacy labels. |
| R-014 | Moderator/admin misuse | Low/Medium | High | Purpose-bound access, audit logs, time-limited grants. |

## 10. Assumptions And Decisions

Accepted for planning:

- 13+ launch, not child-directed.
- Full social target with gated exposure.
- No public exact animal pins.
- Server-authoritative scoring.
- Hybrid AI evidence pipeline.
- Modular monolith first.
- PostgreSQL/PostGIS/pgvector canonical state.
- Firebase Auth/App Check.
- Android first, iOS later.
- APK internal, AAB production.
- Mapbox-first prototype, Google challenger.
- Contacts deferred; invite links default.
- Background location excluded.
- Immutable score events.
- Sensitive species policy required.

Deferred:

- Exact scoring formula.
- Exact rarity taxonomy.
- Retention periods.
- Analytics provider.
- Moderation staffing model.
- Public launch regions.
- iOS parity date.
- Map provider final selection.
- AI provider mix and budget.

## 11. Implementation Handoff

Before implementation:

- Read `AGENTS.md`.
- Read `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`, and `docs/PROCESS.md`.
- Read this blueprint.
- Do not implement feature code until SRS/ADR acceptance is recorded.
- Keep code files usually 200-300 lines.
- Use requirement/ADR comments only where they preserve important context.
- Each work item must include requirement IDs, tests, privacy/security notes, rollback, state-doc updates, and short-burst commit plan.
