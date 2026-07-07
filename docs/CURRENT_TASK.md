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

Current design pass: **PakimonGO V2 UI/product brainstorm and clickable
HTML/CSS/JS prototype**. Use the V1 screenshots in
`docs/assets/COMPLETE UI SCREENSHOTS - V1/`, the V2 concept panels in
`docs/assets/V2 UI CONCEPT PANELS/`, and the clickable prototype in
`docs/prototypes/v2-ui-html/index.html` before implementing any new
Instagram/Facebook-like features. Do not restart completed Tier 1/Tier 2 work
unless a regression is found.

The current prototype is a polished hardcoded phone shell with dummy state,
route navigation, tabs, chips, modals, toasts, score reveal, feed reactions,
profile/collection/rank views, group interactions, notification filters, and
privacy-safe labels. It is still product-direction material, not accepted
implementation scope.

## Current Next Action

Recommended no-credential implementation path:

1. Review the V2 sections in `docs/ux/SOCIAL_GAME_UI_CONCEPT.md`, the generated
   concept panels, and the polished prototype at
   `docs/prototypes/v2-ui-html/index.html`; decide which ideas should become
   accepted requirements or wireframes.
2. Accessibility pass: semantic labels, screen reader review, tap-target checks,
   and widget tests for critical screens.
3. Loading shimmer/skeleton polish where the app still uses plain spinners.
4. Automated real-device E2E plan and smoke scripts for camera/map/upload/scoring.

Credential or account-dependent path:

- Register the release keystore SHA-1 in Firebase.
- Configure production Mapbox token injection.
- Configure durable object storage.
- Configure GitHub/Render deploy secrets if GitHub Actions deploys remain desired.
