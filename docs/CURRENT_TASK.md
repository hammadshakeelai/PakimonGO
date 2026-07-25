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
- Latest recorded automated suite as of 2026-07-06: 145 backend tests, 69
  scoring tests, 162 Flutter tests, and `flutter analyze` clean. This is a
  dated historical snapshot, not the current count - see "Active Task"
  below for the latest (211 API / 78 scoring / 270 V2 + 163 V1 Flutter as
  of iter 44, 2026-07-25).

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

**V2 social-layer improvement loop (iters 1-45 shipped).** The V2 app
(PakimonGO-V2 repo) is a full wildlife social network wired to this
backend: posts with reactions/comments/share, 24h stories, follow graph,
Following feed, user search, all 4 Rank scopes, follower lists, real
Groups with member feed + leaderboard + quests, living map with 3D camera
and species markers, streaks/confetti/haptics/coach marks, and a complete
accessibility pass across iters 39-42 (bottom-nav semantics, icon-button
tooltips, reaction selected-state, non-map sightings list for the Mapbox
markers, WCAG-AA contrast audit — `docs/TECH_DEBT.md` TD-001 is now
closed). See the newest `docs/TASK_LOG.md` entries for the per-iteration
record.

Every core UI control is functional. As of iter 45, the map HUD's mission
strip and the Rank Hub's season card no longer show fabricated content
either, as of iter 46 the HUD header's "Lvl N" badge is real too (derived
from actual lifetime points), as of iter 48 the Profile screen's
"verified" checkmark and fake motto tagline are fixed/removed, and as of
iter 49 the HUD's real points/level refresh correctly after a **wild**
capture too (iter 47 only fixed the capped/zoo/pet path) - see below.
The avatar image itself stays a placeholder asset (no per-user avatar
upload exists anywhere in the app - the same legitimate default-asset
pattern as `V2Dummy.groupHero`), which is not counted as fake user
state. One known live-path fake remains open: `feed_post_card.dart` shows
the same unconditional "verified" checkmark next to every poster in the
feed - see `docs/TECH_DEBT.md` TD-004 (needs a `/v1/feed` response
change, not just a client fix).

Backend state: migrations 001-010 (010 = comment_likes), 216 API tests,
290 V2 + 163 V1 Flutter tests, demo seed is idempotent + self-refreshing
(stories, quest windows).

**Iter 43 (2026-07-25):** full end-to-end verification at the user's
request - Render prod confirmed healthy, backend test suites re-run
green, a real local-dev bug found and fixed (`run_local.ps1` was silently
masking a failed seed step - see `docs/BUGS_AND_RISKS.md` R-002), and the
V2 app built + ran on an Android emulator against the repaired local
backend with a full manual walkthrough (login, map/HUD, the new
all-sightings list, feed, leaderboard, notifications) - all confirmed
working against real data, no broken paths found.

**Iter 45 (2026-07-25):** de-faked the last two live-path preview
surfaces flagged by review. (1) The map HUD's mission strip always showed
hardcoded dummy quest text tagged " preview" for every real user; it now
fetches the viewer's own group quests (`GroupRepository.listGroups` +
`getQuests`, already backed by real `GET /v1/groups/{id}/quests` data)
via a new `MissionViewModel`, shows the nearest-to-ending real quest with
a real countdown and tap-through to that group, and shows an honest
"join a squad" / "no active quest" empty state instead of fake content
when there's nothing to show. (2) The Rank Hub showed a fully fabricated
"Wild Chronicles · Ends in 24d 6h" / "Season 2" - no season concept
exists server-side - while the tier ladder underneath it was already
real (computed from the viewer's actual lifetime points); removed the
fake name/countdown and reframed it as a permanent Rank Tier card.
Also split the now-310-line `rank_hub_parts.dart` (over the 300-line
rule) into `rank_hub_parts.dart` + `season_card.dart`, deleted the dead
`V2Dummy.leaderboard`/`missions`/`season*` fields these left unused, and
fixed a genuinely vacuous widget test (the 320dp skeleton-overflow
regression test from iter 44 would have passed against the pre-fix
fixed-width code at any width tried, because Flutter clamps a
fixed-width child to its parent's constraints in a Column's cross axis
instead of throwing - verified empirically, then replaced with a test
that asserts the actual `width` property and does fail against the old
code). A same-iteration follow-up review then caught a real dead end in
the mission strip's own empty state (joining a group and backing out
never refreshed the strip - `GroupsListScreen.open` didn't return its
push `Future` for the caller to chain a refetch onto) and a matching
wiring-test gap (the new tests never mounted `MapHudScreen` itself with
a real `MissionViewModel`); both are fixed, with an end-to-end join-flow
test verified to fail without the fix and pass with it. 280 V2 Flutter
tests green (was 270), `flutter analyze` clean.

**Iter 46 (2026-07-25):** closed `docs/TECH_DEBT.md` TD-002 - the map
HUD's "Lvl N" badge was the one hardcoded number iter 45 had scoped out
as needing a backend change. Added `GET /v1/users/me`'s `totalPoints`
field (backed by a new single-user `get_user_total_points()` query -
deliberately not a reuse of the paginated/sensitive-filtered
`get_leaderboard` query, which would have undercounted a user's own real
total) and a client-side `levelForPoints()` formula (50 pts/level,
uncapped) kept deliberately separate from `SeasonCard.tiers` (that
5-tier ladder would make an "always climbing" HUD number stall at "Lvl
5" forever past 1500 points). 216 API tests (was 211), 285 V2 Flutter
tests (was 280), `flutter analyze` clean on both repos.

**Iter 47 (2026-07-25):** the HUD's real streak/level (iter 46) turned
out to only refresh when the user opened the Profile screen, never right
after the capture that actually changed the score - `fetchProfile()` ran
exactly once, in `MapHudScreen.initState()`, which never re-runs since
the Map tab lives in an `IndexedStack` and is built once at launch.
`CaptureReviewScreen` now refreshes the shared `ProfileViewModel`/
`MissionViewModel` in the background immediately after a successful
submission, before Score Reveal even opens. Also gave `CaptureHero` an
`errorBuilder` for corrupt/unreadable photo bytes (V1's capture screen
already had this; V2's never got it - found while writing the
first-ever widget test for `CaptureReviewScreen`). 286 V2 Flutter tests
(was 285), `flutter analyze` clean.

**Iter 48 (2026-07-25):** removed a fake "Explorer. Observer. Protector."
motto line under every real user's name/email on the Profile screen (no
backend "bio" field exists to back it - the honest fix is removing it,
not inventing a different fake), and fixed an unconditional "verified"
checkmark next to the name that showed for every user regardless of
actual trust state. Before touching the checkmark, verified `'verified'`
is a real, reachable value (seed scripts explicitly set it for demo
users) rather than trusting `docs/api/OPENAPI_DRAFT.yaml`'s stale
`trustState` enum, which doesn't list it - avoided breaking an
already-correct check elsewhere by "fixing" it to match a wrong doc.
Deferred: `feed_post_card.dart` has the same unconditional checkmark for
every feed poster, but needs a backend `/v1/feed` change (`FeedItem` has
no trust-state field at all) - opened as `docs/TECH_DEBT.md` TD-004
rather than expanding this iteration's scope. 289 V2 Flutter tests (was
286), `flutter analyze` clean.

**Iter 49 (2026-07-26):** corrected an incomplete fix from iter 47.
`CaptureReviewScreen`'s immediate post-submit `fetchProfile()`/
`fetchMission()` only reads the real new total on the **capped**
(zoo/pet/duplicate) path, which is scored synchronously - for a **wild**
capture (the highest-point, most-used path) `POST /submissions` returns
before the async worker has written a `ScoreEvent`, so that immediate
fire still saw the pre-capture total. Fixed by also firing both
refreshes from `ScoreRevealScreen._refresh()`, at the point its existing
poll (scheduled 3s auto-check + manual "Check score" retry) detects the
pending->scored/capped transition - i.e. where the worker's real result
actually lands. Both refresh points now coexist: iter 47's immediate
fire covers capped submissions (never pending, so `_refresh()` never
runs for them); this iteration's covers wild ones. 290 V2 Flutter tests
(was 289), `flutter analyze` clean. See `docs/TASK_LOG.md` iter 49 for
the full verification record (empirically confirmed to fail without the
fix).

## Current Next Action

Items 1-4 from the prior version of this list (game-feel polish, post
detail/story replies/group creation, accessibility pass, loading
shimmers) are all done - see `docs/TASK_LOG.md` iters 36-45. The HUD
"Lvl N" badge (former item 1 here) is also done as of iter 46. Recommended
no-credential path from here:

1. TD-004 (`docs/TECH_DEBT.md`): enrich `GET /v1/feed` with each poster's
   trust state so `feed_post_card.dart`'s unconditional "verified"
   checkmark can be gated on real data, matching the iter 48 profile-screen
   fix.
2. Priority 1 from the Next Work Queue below: review
   `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` and the HTML prototype, and decide
   which remaining concept ideas become real requirements vs. backlog.
3. Moderator console/appeals tooling (no credential needed, larger scope
   - see Next Work Queue item 7).
3. TD-003 (`docs/TECH_DEBT.md`): PakimonGO-V2 has no automated 300-line
   file-size check of its own - add a small script inside that repo.

Credential or account-dependent path:

- Register the release keystore SHA-1 in Firebase.
- Configure production Mapbox token injection.
- Configure durable object storage.
- Configure GitHub/Render deploy secrets if GitHub Actions deploys remain desired.
- Build + publish signed V2 release APKs to the PakimonGO-V2 GitHub
  Releases page (currently empty) - blocked on a production Mapbox token
  and a release signing keystore, both of which need the user to supply
  or generate them.
