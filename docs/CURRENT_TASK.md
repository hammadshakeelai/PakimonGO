# Current Task

## Active Phase

**Post-sprint launch hardening and store-readiness.**

The original sprint packets through Sprint 46 are complete, and later hardening
work has continued beyond that sprint structure. The app is now a demoable
alpha candidate with a live Render backend, a working Android/emulator flow,
and user-facing moderation basics. It is still not Play Store ready.

Use `docs/REMAINING_WORK.md` and the newest entries in `docs/TASK_LOG.md` as
the current source of truth before starting implementation.

## Grounded Current State

Last recorded in `docs/TASK_LOG.md` on 2026-07-06:

- Backend deployed to `https://pakimongo-api.onrender.com` on Render.
- Render Postgres is connected; Alembic migrations 001 through 004 apply cleanly.
- `/health/live`, `/health/ready`, and authenticated `/v1/users/me` were smoke-verified.
- Android emulator walkthrough covered age gate, onboarding, login, Mapbox map,
  history, leaderboard, notifications, profile, dark mode, and collection.
- User-facing moderation exists: report submission/user, block/unblock, audit
  rows, leaderboard filtering, and a Blocked Users screen.
- Map now uses coarse public locations, Mapbox Standard 3D styling, annotations,
  auto-fit camera behavior, and a capture FAB.
- Latest recorded automated suite: 145 backend tests, 69 scoring tests, 162
  Flutter tests, and `flutter analyze` clean.

This doc update did not re-run the full backend/scoring/Flutter suites. It did
re-run the required pre-task guard and doc/JSON/secret validation scripts.

## What Is Still Not Real

- No iOS build has been attempted.
- No automated real-device E2E suite covers camera, map, upload, auth, and scoring.
- Release keystore SHA-1 still needs to be registered for production Firebase auth.
- Production Mapbox token/CI injection still needs a final path.
- Production object storage is not configured; local storage is still the default.
- Moderator console, appeals, takedown workflow, and moderation staffing are not built.
- Privacy policy, terms, app-store listing assets, store review test accounts, and
  privacy questionnaire are not done.
- Push notifications are not implemented; notifications are still in-app polling.
- The in-process scoring worker still has no persistent queue, retries, or DLQ.

## Active Task

**V2 social-layer improvement loop (iters 1-39 shipped).** The V2 app
(PakimonGO-V2 repo) is a full wildlife social network wired to this
backend: posts with reactions/comments/share, 24h stories, follow graph,
Following feed, user search, all 4 Rank scopes, follower lists, real
Groups with member feed + leaderboard + quests, living map with 3D camera
and species markers, streaks/confetti/haptics/coach marks, and (iter 39)
the start of an accessibility pass (bottom-nav semantics, icon-button
tooltips — see `docs/TECH_DEBT.md` TD-001 for what's still open). Every
core UI control is functional — no preview/dummy features remain. See
the newest `docs/TASK_LOG.md` entries for the per-iteration record.

Backend state: migrations 001-010 (010 = comment_likes), 211 API tests,
222 V2 + 163 V1 Flutter tests, demo seed is idempotent + self-refreshing
(stories, quest windows).

## Current Next Action

Recommended no-credential implementation path (fun/game-feel focus):

1. Game-feel polish: score-reveal/quest-complete celebration moments,
   streaks, playful empty states.
2. Post detail screen (inline comments), story replies/reactions,
   group create-from-UI with cover selection.
3. Accessibility pass: semantic labels, screen reader review, tap-target
   checks, and widget tests for critical screens.
4. Loading shimmer/skeleton polish where the app still uses plain spinners.

Credential or account-dependent path:

- Register the release keystore SHA-1 in Firebase.
- Configure production Mapbox token injection.
- Configure durable object storage.
- Configure GitHub/Render deploy secrets if GitHub Actions deploys remain desired.
