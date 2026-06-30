# 00 Inception

## Problem Statement

- Animal discovery can be joyful, but many existing tools are either scientific, generic social media, or fictional location games.
- A real-animal game can create bad incentives if it rewards unsafe proximity, touching, feeding, chasing, trespass, or zoo farming.
- Animal photos, pet ownership, exact locations, teen users, and public social features create high privacy and moderation risk.
- AI-assisted scoring needs strong deterministic checks, evidence records, versioning, and appeal paths to feel fair.
- Long-running AI-assisted development needs durable context, small modules, traceability, and state docs.

## Vision

PakimonGO is a mobile system that turns safe real-world animal observations into scored collections, learning, map discovery, and social competition through privacy-preserving capture, AI-assisted evidence, and server-authoritative game rules for 13+ users.

## In Scope

- 13+ onboarding, safety education, consent, auth, and account management.
- Camera capture, local drafts, upload, private originals, and public derivatives.
- Foreground location, private exact coordinates, and public privacy-safe map cells.
- AI-assisted evidence, deterministic scoring rules, duplicate detection, zoo/captive detection, and appeals.
- Collections, profiles, friends, groups, posts, comments, likes, reposts, hashtags, reports, blocks, moderation, and leaderboards.
- Android APK first, Play release later, iOS/TestFlight after Android readiness.

## Out Of Scope For Alpha-0

- Under-13 accounts.
- Background location.
- Public exact animal pins.
- Full public social launch.
- LLM-only scoring.
- Client-side final scoring.
- Contacts import as a required path.
- Scientific authority claims.

## Actors

| Actor | Goal |
|---|---|
| Player | Capture animals, earn score, build collection, compete. |
| Teen Player | Use the game with strict safety and privacy defaults. |
| Friend | Interact with visible posts and compare friend scores. |
| Pet Owner | Accept or reject shared owner credit. |
| Moderator | Review reports, appeals, unsafe behavior, and suspicious scores. |
| Admin | Manage policies, geofences, taxonomy, scoring, regions, and incidents. |
| Store Reviewer | Validate compliance and app behavior. |
| External Provider | Supply auth, map, AI, taxonomy, storage, or notification service. |

## Technology Decisions

| Area | Decision | Protected Boundary |
|---|---|---|
| Mobile | Flutter | Platform services behind feature adapters. |
| Backend | FastAPI-style modular monolith | HTTP contracts and module interfaces. |
| Workers | Python async worker deployable | Job contracts and idempotency keys. |
| Database | PostgreSQL/PostGIS/pgvector | Repository interfaces and migrations. |
| Auth | Firebase Auth/App Check | Auth adapter and domain user model. |
| Storage | Cloud Storage/Firebase Storage | Media storage adapter. |
| Maps | Mapbox-first, Google challenger | Map provider adapter and server-generated map data. |
| AI | Hybrid deterministic plus structured vision | AI evidence adapter and schema validation. |

## Project Setup

- Root process: `AGENTS.md`, `docs/PROCESS.md`, `docs/COMMIT_POLICY.md`.
- SRS and requirements: `docs/SRS.md`, `docs/REQUIREMENTS.md`.
- Methodology artifacts: `docs/software-engineering/`.
- Source scaffold: `apps/`, `services/`, `packages/`, `infrastructure/`, `data/`, `tools/`.
- Knowledge: `knowledge/okf/`, `knowledge/graph/graphify-out/`, Obsidian-compatible Markdown docs.

## Exit Criteria

- Problem, vision, scope, actors, technology direction, and repo setup are documented.
- SRS follows the methodology structure.
- Traceability artifacts exist before feature code starts.
