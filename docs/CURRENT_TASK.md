# Current Task

## Active Phase

**Handoff from code-complete to production-hardening.**

49 sprints done. 289 tests pass. The app is a working technical prototype. Honest remaining work is documented in `docs/REMAINING_WORK.md`.

## What Exists

All code is built. Full inventory in `CLAUDE.md` and `PROJECT_COMPLETE.md`.

## What's Real

The app works **locally** with dev providers (SQLite, fake auth, dummy AI, local storage). It is **not production-ready**. Key gaps:

- No real auth (FakeAuthAdapter)
- No real AI scoring (DummyVisionProvider)
- Map wired to Mapbox (local dev token); production token still needed
- Submission rate limiting implemented (per-user cooldown, NFR-SEC-004)
- APK is 105.8MB (needs optimization)
- No iOS build at all
- No social features
- No moderation

## Active Task

Hardening the prototype for production. See `docs/REMAINING_WORK.md` for the full queue.

## Current Next Action

Tier 1 continued: APK size optimization (no creds needed), then Firebase Auth + Google Vision (need cloud projects).
