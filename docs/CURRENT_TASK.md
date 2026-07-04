# Current Task

## Active Phase

**Handoff from code-complete to production-hardening.**

46 sprints done. 291 tests pass. 92 commits. The app is a working technical prototype. Honest remaining work is documented in `docs/REMAINING_WORK.md`.

## What Exists

All code is built. Full inventory in `CLAUDE.md` and `PROJECT_COMPLETE.md`.

## What's Real

The app works **locally** with dev providers (SQLite, fake auth, dummy AI, local storage). It is **not production-ready**. Key gaps:

- Firebase Auth wired (backend adapter + Flutter Google sign-in, AUTH_PROVIDER=firebase); FakeAuthAdapter is the dev default. Live sign-in needs a Google account on the device.
- Real AI scoring available via Groq free tier (VISION_PROVIDER=groq, live-verified); DummyVisionProvider is the default
- Map wired to Mapbox (local dev token); production token still needed
- Submission rate limiting implemented (per-user cooldown, NFR-SEC-004)
- APK optimized: split-per-ABI + R8, arm64 39.8MB (was 105.8MB); release-build map render still to verify on a physical device
- No iOS build at all
- No social features
- No moderation

## Active Task

Hardening the prototype for production. See `docs/REMAINING_WORK.md` for the full queue.

## Current Next Action

Tier 1 continued: APK size optimization (no creds needed), then Firebase Auth + Google Vision (need cloud projects).
