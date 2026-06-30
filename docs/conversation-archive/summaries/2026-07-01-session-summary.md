# Session Summary: 2026-07-01

## User Intent

The user wants PakimonGO planned and scaffolded as a large-scale, modular, AI-agent-friendly mobile project before feature implementation begins. The app is inspired by location-based creature games but uses real animal photography, scoring, collections, social features, maps, route waypoints, leaderboards, and privacy/safety controls.

## Key User Requirements

- Android APK first, iOS later.
- Camera and map features for phone.
- Google login plus email/password and recovery.
- Social features: friends, groups, captions, likes, comments, reposts, hashtags, collection pages.
- Four leaderboard scopes: global, country, local, friends.
- AI-assisted animal identification, rarity, aesthetic scoring, duplicate detection, and zoo/captive detection.
- Zoo photos save but do not earn normal wild score; honest disclosure may earn tiny capped participation credit.
- Same animal should not repeatedly count unless materially different.
- Public map must show animal activity without exposing exact risky locations.
- Full SDLC and Agile process before coding.
- Small files, usually 200-300 lines.
- Persistent docs for current task, current thinking, next task, backlog, bugs, risks, tech debt, and handoff.
- OKF, Obsidian, and Graphify-style knowledge workflows.
- Short-burst semantic commits with AI attribution.
- A conversation archive where future AIs can read the original prompts and responses.

## Work Completed In This Session

- Repaired broken Git metadata with fresh `git init`.
- Added a large monorepo scaffold for mobile, API, workers, packages, infrastructure, data goldsets, tools, and knowledge graph outputs.
- Added root `README.md`, `.editorconfig`, `.gitignore`, and `.gitmessage.txt`.
- Added `docs/COMMIT_POLICY.md` for short-burst semantic commits with AI trailers.
- Added `docs/EXPANDED_BLUEPRINT.md`.
- Replaced `docs/REQUIREMENTS.md` with the expanded 145-functional-requirement catalogue and measurable NFRs.
- Replaced `docs/SRS.md` with the gated Alpha-0 SRS.
- Added this conversation archive area.

## Active Decisions

- 13+ launch, not under-13.
- Full social target, but gated by moderation/privacy/abuse readiness.
- Android first, iOS later.
- Flutter mobile direction.
- FastAPI-style modular monolith direction.
- PostgreSQL/PostGIS/pgvector canonical state.
- Firebase Auth/App Check.
- Server-authoritative scoring.
- No exact public animal pins.
- No background location in Alpha-0.
- Invite links before contacts import.

## Next Task

Finish reconciling state docs and ADRs after scaffold, then define the first Alpha-0 vertical slice before production feature code begins.
