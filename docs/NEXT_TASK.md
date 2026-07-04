# Next Task

## Current Next Task

Tier 1 code-complete: ✅ Mapbox, ✅ rate limiting, ✅ APK optimization, ✅ AI vision (Groq), ✅ Firebase Auth (backend + Flutter Google sign-in). Live Google sign-in needs a Google account on the emulator/device. Next: Tier 2 (Postgres wiring, Flutter error handling).

## Sprint 2-26 Complete

All sprints 2-26 complete. Full backend implemented: DB, auth, upload, user profiles, precheck, scoring, AI vision, async worker, map prototype, collection/leaderboard, pagination, sensitive species suppression, API versioning, cloud storage, Docker Compose, integration tests.

## Sprint 46 Complete

All 46 sprints complete. 291 tests pass. App is a working prototype.

## Tier 1 Queue (Alpha)

The app is code-complete as a prototype. The next phase is production-hardening. See `docs/REMAINING_WORK.md` for the full prioritized queue.

| Priority | Task | Effort | Status |
|----------|------|--------|--------|
| 1 | Provision Mapbox token | 10 min | ✅ Done (local dev; prod token pending) |
| 2 | Create Firebase project + configure Auth | 1-2 days | ✅ Code done (backend + Flutter Google sign-in); live sign-in needs a Google account on the device |
| 3 | AI vision scoring | 1 day | ✅ Done via Groq free tier (live-verified) |
| 4 | Add rate limiting on submissions | 0.5 day | ✅ Done (NFR-SEC-004) |
| 5 | Optimize APK size (ProGuard, R8, split) | 1 day | ✅ Done (arm64 39.8MB, −62%) |

## How To Start

1. Read `docs/REMAINING_WORK.md` for full context
2. Read `CLAUDE.md` for codebase grounding
3. Pick the first task from Tier 1
4. Execute per the mandatory workflow in `AGENTS.md`
