# PakimonGO

PakimonGO is a planned 13+ mobile app for real-animal photography, discovery, collections, map exploration, privacy-safe social sharing, and server-scored competition.

This repository is currently in scaffold-plus-planning state. It contains the project process, expanded requirements, architecture direction, and a modular monorepo skeleton. It does not yet contain production feature implementation.

## Current Phase

Phase 5: repository scaffold and implementation readiness.

Before production coding starts, finish the SRS/ADR acceptance pass and define the first Alpha-0 vertical slice.

## Repository Layout

- `apps/mobile/pakimon_go_app/`: Flutter app home, organized by feature.
- `services/api/`: FastAPI-style modular monolith shell.
- `services/workers/`: async media, evidence, scoring, moderation, privacy, and leaderboard jobs.
- `packages/`: shared contracts and domain rule packages.
- `infrastructure/`: database, Firebase, Docker, Cloud Run, and IaC assets.
- `data/goldsets/`: duplicate, zoo, species, scoring, and sensitive-species benchmark datasets.
- `docs/`: SRS, requirements, process, decisions, risks, roadmap, and templates.
- `knowledge/`: OKF, Obsidian, and future Graphify/code-graph knowledge outputs.
- `tools/`: repo automation, graph export, QA, and utility scripts.

## Contributor Start

1. Read `AGENTS.md`.
2. Read `docs/CURRENT_TASK.md`.
3. Read `docs/NEXT_TASK.md`.
4. Read `docs/PROCESS.md`.
5. Read the relevant module README before editing.

## Build Status

No runnable app or backend exists yet. Do not expect `flutter test`, backend tests, or CI to pass until toolchains are scaffolded in a later task.
