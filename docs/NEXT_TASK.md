# Next Task

## Current Next Task

The old "next: Tier 1/Tier 2" guidance is stale. Tier 1 is done, and the major
Tier 2 implementation items are recorded as done in `docs/REMAINING_WORK.md`:
Postgres wiring, Flutter error handling, onboarding, age gate, Firebase auth,
Groq vision, rate limiting, and APK optimization.

**Recommended next design action:** review the V2 brainstorm in
`docs/ux/SOCIAL_GAME_UI_CONCEPT.md`, compare it against the V1 screenshots in
`docs/assets/COMPLETE UI SCREENSHOTS - V1/`, inspect the polished clickable
prototype at `docs/prototypes/v2-ui-html/index.html`, and choose the first V2
wireframe pack.

**Recommended next implementation after that:** accessibility hardening.

Why this is the grounded default:

- It needs no new cloud credentials.
- It directly supports app-store quality and safer use by younger users.
- `docs/REMAINING_WORK.md` still lists accessibility as unfinished.
- The latest task log already points to "loading shimmers, accessibility" after
  moderation and map polish landed.
- The new social/game UI ideas are intentionally concept backlog, not code scope
  yet.

## Sprint 2-26 Complete

This section name is retained because `tools/qa/pre_task_check.py` verifies it
as a required handoff anchor. The content is now broader than the original
Sprint 2-26 window: the original sprint packets through Sprint 46 are complete,
and post-sprint hardening has continued with deployment, auth/vision live
checks, Postgres verification, APK optimization, age gate, onboarding,
user-facing moderation, map overhaul, and UI polish.

## Do Not Rebuild Unless Broken

Avoid treating these as the next task unless a regression is found:

- Mapbox local wiring and map marker overhaul.
- Firebase Google sign-in path.
- Groq vision provider wiring.
- Submission rate limiting.
- APK split/R8 optimization.
- Postgres migrations and Render Postgres smoke verification.
- Flutter error/retry UI across data screens.
- Age gate and onboarding.
- User-facing report/block flows.

## Next Work Queue

| Priority | Task | Credential Needed | Grounded Scope |
|---|---|---:|---|
| 1 | Promote/trim V2 social UI concept | No | Review `docs/ux/SOCIAL_GAME_UI_CONCEPT.md`, `docs/assets/V2 UI CONCEPT PANELS/README.md`, and the polished prototype at `docs/prototypes/v2-ui-html/index.html`; decide which ideas become requirements, V2 wireframes, or future backlog. |
| 2 | Accessibility pass | No | Add semantic labels, verify screen-reader order, check tap targets, add widget tests for key screens. |
| 3 | Loading shimmers/skeletons | No | Replace obvious `CircularProgressIndicator` states where a skeleton improves perceived quality. |
| 4 | Real-device E2E testing | Device/account | Cover camera, map, upload, scoring, auth, and main navigation on a physical Android device. |
| 5 | Release keystore/Firebase SHA-1 | Yes | Register release SHA-1 so production Google sign-in works outside debug builds. |
| 6 | Durable object storage | Yes | Configure S3/GCS or equivalent; local storage is not production-safe. |
| 7 | Moderator console/appeals | No/Maybe | Build moderator review tooling, appeals, takedowns, and audit workflows after scoping. |
| 8 | Store readiness docs | No/Legal review | Privacy policy, terms, store listing, age rating, reviewer accounts, screenshots. |

## How To Start

1. Read `CLAUDE.md`.
2. Run `python tools/qa/pre_task_check.py`.
3. Read `docs/CURRENT_TASK.md`, this file, `docs/CURRENT_THINKING.md`, and
   `docs/REMAINING_WORK.md`.
4. For accessibility work, read the relevant UX/accessibility docs and the
   screens under `apps/mobile/pakimon_go_app/lib/features/`.
5. Keep files small and update state docs after the work burst.
