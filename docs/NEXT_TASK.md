# Next Task

## Current Next Task

Tier 1 production-hardening. ✅ Mapbox token wired (local dev) and ✅ submission rate limiting implemented. Next: APK size optimization (no creds needed), then Firebase Auth + Google Vision (need cloud projects).

## Sprint 2-26 Complete

All sprints 2-26 complete. Full backend implemented: DB, auth, upload, user profiles, precheck, scoring, AI vision, async worker, map prototype, collection/leaderboard, pagination, sensitive species suppression, API versioning, cloud storage, Docker Compose, integration tests.

## Sprint 49 Complete

All 49 sprints complete. 289 tests pass. App is a working prototype.

## Tier 1 Queue (Alpha)

The app is code-complete as a prototype. The next phase is production-hardening. See `docs/REMAINING_WORK.md` for the full prioritized queue.

| Priority | Task | Effort | Status |
|----------|------|--------|--------|
| 1 | Provision Mapbox token | 10 min | ✅ Done (local dev; prod token pending) |
| 2 | Create Firebase project + configure Auth | 1-2 days | ⬜ Needs cloud project |
| 3 | Enable Google Vision API + create key | 1 day | ⬜ Needs cloud project |
| 4 | Add rate limiting on submissions | 0.5 day | ✅ Done (NFR-SEC-004) |
| 5 | Optimize APK size (ProGuard, R8, split) | 1 day | ⬜ Next (no creds needed) |

## How To Start

1. Read `docs/REMAINING_WORK.md` for full context
2. Read `CLAUDE.md` for codebase grounding
3. Pick the first task from Tier 1
4. Execute per the mandatory workflow in `AGENTS.md`
