# Next Task

## Current Next Task

The old "next: Tier 1/Tier 2" guidance is stale. Tier 1 is done, and the major
Tier 2 implementation items are recorded as done in `docs/REMAINING_WORK.md`:
Postgres wiring, Flutter error handling, onboarding, age gate, Firebase auth,
Groq vision, rate limiting, and APK optimization.

**Status as of iter 49 (2026-07-26):** iters 1-38 shipped the full social
layer (posts, stories, follows, search, groups, quests), game-feel polish
(streaks, confetti, haptics, coach marks, feed skeleton, double-tap Wow,
new-posts pill), and living-map/3D-camera work. Iters 39-42 ran the full
accessibility pass to completion (`docs/TECH_DEBT.md` TD-001 closed).
Iter 44 added loading skeletons to the remaining spinner screens. Iter 45
de-faked the map HUD mission strip and the Rank Hub season card, iter 46
closed TD-002 (real HUD "Lvl N" badge), iter 47 fixed the HUD streak/
level actually going stale after a capture (not just the badge itself
being real) - but iter 49 found that fix only covered the capped
(zoo/pet/duplicate) path, not the wild-capture path where the worker
scores async, and closed that gap too (plus a related unmount-safety
gap in the fix itself), iter 48 removed a fake profile "motto" tagline
and fixed an unconditional "verified" checkmark on the Profile screen,
and iter 49 closed the matching bug on the Feed screen too (TD-004:
`GET /v1/feed` now returns each poster's real `trustState`). See
`docs/TASK_LOG.md` for the full per-iteration record.

**Status check: no known live-path fake data remains in the app.** The
"de-fake the live UI" thread that ran iters 45-49 has no further scoped
items in it. TD-003 also turned out already closed on inspection -
PakimonGO-V2's `tools/qa/validate_docs.py`/`pre_task_check.py` already
had a working file-size check (since Sprints 22-25); the real gap was
that this improvement loop only ever ran v1's validators, never V2's own
copy. Fixed that (excluded `.dart_tool` build output from the scan,
split the 2 files this loop's own edits had pushed over 300 lines) and
closed TD-003 with a corrected removal condition: run V2's own
validators for V2 edits going forward, the same as v1's for v1 edits.

**Honest handoff state: no unblocked no-credential implementation item
remains.** All three items previously listed here need a user decision
before any of them can become autonomous implementation work, not just
a caveat attached to a recommendation:

1. Review `docs/ux/SOCIAL_GAME_UI_CONCEPT.md`/the HTML prototype and
   decide which concept ideas become real requirements - a **product**
   decision (which features, for whom, at what cost to scope).
2. Moderator console/appeals tooling (Next Work Queue item 7, marked
   "No/Maybe" credential, "after scoping" - scoping itself requires
   deciding who counts as a moderator, which actions are reversible, what
   the appeals SLA is, and whether a takedown hides or deletes - the
   `User` model has only `status`/`trust_state`, no role/permission
   concept exists anywhere yet). This is a **policy** decision for a
   13+ app with real enforcement consequences, not a UI/architecture
   one - the same class of call as #1, with more weight.
3. `RemoteTrigger`/cloud-routine setup - explicitly **declined by the
   user already** ("skip this all"); do not raise it again unprompted.
   See `docs/BUGS_AND_RISKS.md` R-001 for the gap this would close if the
   user ever reopens it.

None of these three should be started without the user picking one, and
#3 should never be started without the user bringing it up first.

**2026-07-26 update:** the file-size cleanup this section used to point
to as the fallback unblocked item is done. All 5 files
(`map_hud_screen.dart`, `group_screen.dart`, `story_viewer.dart`,
`api_models.dart`, `mission_strip_test.dart` in the PakimonGO-V2 repo)
are split under the 300-line rule; `validate_docs.py` there now reports
`warnings_over_300=0` for the first time. See that repo's
`docs/TECH_DEBT.md` (2026-07-26 entry) for the per-file split detail.
**This means there is currently no known unblocked, no-credential,
no-product-decision engineering item left in either repo.** An agent
landing here with the directive to keep going and no fresh user input
should re-derive one from a fresh read of both repos' `BUGS_AND_RISKS.md`/
`TECH_DEBT.md`/source tree rather than assume this list is still
current - it was exhausted, not just trimmed.

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
| 2 | Accessibility pass | No | DONE (iters 39-42, `docs/TECH_DEBT.md` TD-001 closed). |
| 3 | Loading shimmers/skeletons | No | DONE (iter 44). |
| 3b | Real "Lvl N" HUD badge | No | DONE (iter 46). TD-002 closed. |
| 3c | Feed's unconditional "verified" checkmark | No | DONE (iter 49). TD-004 closed. |
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
