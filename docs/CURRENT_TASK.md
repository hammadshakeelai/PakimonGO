# Current Task

## Active Phase

Phase 5: Repo scaffold and implementation readiness.

Production feature code has not started. The repository now contains a planning baseline plus a scaffolded monorepo structure that future implementation work can fill in.

## Active Task

Implement the expanded planning baseline as repository files and create the scaffold-only project structure for PakimonGO.

## Current Inputs

- Android APK first; iOS later.
- 13+ launch posture.
- Full social target, gated by moderation/privacy/abuse readiness.
- Flutter mobile direction.
- FastAPI-style modular monolith direction.
- PostgreSQL/PostGIS/pgvector canonical state.
- Firebase Auth/App Check.
- Server-authoritative scoring.
- Privacy-safe map and no exact public animal pins.
- Small files, usually 200-300 lines.
- Persistent process, state, backlog, risk, debt, and conversation archive files.
- Short-burst semantic commits with AI attribution.

## Progress This Pass

- Repaired broken Git metadata with fresh `git init`.
- Added root `README.md`, `.editorconfig`, `.gitignore`, and `.gitmessage.txt`.
- Configured Git commit template to `.gitmessage.txt`.
- Added `docs/COMMIT_POLICY.md`.
- Added `docs/EXPANDED_BLUEPRINT.md`.
- Replaced `docs/REQUIREMENTS.md` with expanded functional and non-functional requirements.
- Replaced `docs/SRS.md` with gated Alpha-0 SRS.
- Scaffolded monorepo folders for mobile, API, workers, packages, infrastructure, data goldsets, tools, and knowledge graph outputs.
- Added `.gitkeep` placeholders so nested scaffold folders are tracked.
- Added conversation archive vault under `docs/conversation-archive/`.
- Updated `AGENTS.md` and `docs/PROCESS.md` with conversation archive and short-burst commit rules.
- Added ADR-007 through ADR-016 as proposed decision drafts.
- Added `docs/ALPHA_0_VERTICAL_SLICE.md` and `docs/WORK_PACKAGES.md`.

## Current Next Action

Review and accept the ADR completion pack, then begin WP-015: Alpha-0 private capture slice.
