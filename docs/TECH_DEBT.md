# Technical Debt Register

## Current Known Debt

Original sprint packets through Sprint 46 are complete, and post-sprint
hardening has continued beyond that structure. Latest recorded suite in
`docs/TASK_LOG.md` (as of iter 49, 2026-07-26): 218 API tests, 78 scoring
tests, 293 V2 + 163 V1 Flutter tests, and clean Flutter analysis on both
repos. (The 145/69/162 figures were the pre-V2-loop sprint-era baseline.)

Current debt items:

## Implementation Debt

- API versioning uses middleware but no v2 routes exist yet.
- Storage uses local filesystem by default; needs durable cloud storage
  (S3/GCS/equivalent) before deployed media can be treated as production-safe.
- AI vision: Groq provider is live-verified (`VISION_PROVIDER=groq`, free tier,
  no billing). Google Vision path exists but is not live-verified with billing.
  `GROQ_MODEL` default may need updating as Groq deprecates vision models.
- Firebase auth is live-verified on a real phone (Google sign-in -> backend
  `/v1/users/me` 200). firebase-admin is installed; service account is outside
  the repo; `google-services.json` is gitignored. Production still needs the
  release keystore SHA-1 registered.
- Mapbox is wired for local dev (`--dart-define` app token plus Gradle download
  token). Production token and CI injection still need final handling.
- Database uses SQLite for default local dev. Local pgvector Postgres and Render
  Postgres have both been verified; long-term production DB choice/ops remain
  open.
- APK is optimized (R8 minify, resource shrinking, split-per-ABI, arm64 around
  39.8MB). Verify map rendering on a physical arm64 release build; emulator
  x86_64 does not fully prove Mapbox native release behavior.
- No iOS build has been tested.
- Submission rate limiting uses a single-instance DB-query cooldown. A
  multi-instance deployment needs a shared limiter such as Redis.
- User-facing moderation exists, but moderator console, appeals,
  takedown/restore tooling, and staffing workflows are still unbuilt.
- The scoring worker is still in-process and lacks persistent queueing, retries,
  and dead-letter handling.
- `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` contains the V2 social/game UI brainstorm
  and candidate ideas that are not yet accepted requirements or traced test
  cases.
- `docs/prototypes/v2-ui-html/index.html` is a clickable V2 planning prototype.
  It is not production UI and has no Flutter, API, auth, persistence, or scoring
  integration.
- The V2 prototype uses static dummy data, compact hardcoded rendering, and
  cropped concept-panel textures. Accepted screens need real Flutter widgets,
  approved assets, accessibility labels, state management, tests, and traced
  requirements.
- `services/api/pakimongo_dev.db` is a tracked binary dev-seed database.
  Running the backend or its pytest suite locally regularly dirties it
  (`git status` shows it modified after nearly every local test run).
  This is expected local-dev churn, not a real change - do not stage it
  into unrelated commits; if it ever needs a genuine update, commit it
  alone with a clear message.

## Decision Debt

- Scoring point ranges and economy formulas intentionally remain undefined
  until product review.
- Moderation staffing/tooling is not fully defined.
- The V2 social/game UI concept needs a product decision and wireframe pass
  before implementation work begins.
- The V2 HTML/CSS/JS prototype needs product review before any screen is
  promoted into app implementation scope.
- Species rarity taxonomy needs a formal source of truth.
- GitHub CODEOWNERS uses placeholder teams.
- Branch protection is not enabled in GitHub repository settings.
- adb is not on PATH (SDK path: `AppData/Local/Android/sdk/platform-tools`).
- Full conversation export has not been pasted to raw archive; only summaries
  exist.

## Future Debt Controls

- Files should usually stay near 200-300 lines. If a file grows larger, split
  by responsibility or document why not.
- Every module needs a local README or module overview once it becomes
  non-trivial.
- Every shortcut must be logged here with owner, reason, and removal condition.
- No generated code should be hand-edited unless the generator workflow is
  documented.
- Any temporary scoring or moderation rule must include an expiry review date.

## TD-001: Accessibility pass — CLOSED (iter 42, 2026-07-25)

- Area: V2 Flutter app (PakimonGO-V2 repo) + shared collection_screen.dart.
- Introduced: iter 39 (2026-07-24) closed the icon-button/tooltip and
  bottom-nav-selected-state gaps. Iter 40 (same day) closed the "selected
  reaction" gap on PostReactionRow and StoryReactionBar (both now expose
  `Semantics(selected:)` instead of only a visual color/scale change).
  Correction to the original iter-39 note: double-tap-to-Wow already had a
  non-gesture fallback (the persisted PostReactionRow buttons below every
  photo) - it just wasn't marked "selected" for assistive tech, which iter
  40 fixed. No new gesture-only dead end was found. Iter 41 (2026-07-25)
  closed the Mapbox marker gap: PointAnnotations are native GL layers, not
  Flutter widgets, and structurally cannot carry Semantics, so the fix is
  a full non-map path instead - AllSightingsScreen lists every marker the
  map knows about (not just the "Nearby Activity" sheet's top 3), each row
  independently focusable/tappable, reached via a "View all" action. Iter
  42 (same day) ran the WCAG AA contrast audit: every foreground the theme
  paints as text/icons (text, muted, green, lime, amber, red, blue,
  violet), checked against every background surface (bg, surface, card,
  card2), plus button-label text and the one reduced-opacity text spot
  (amber@0.8 in the score reveal) - all 34 pairings already clear 4.5:1,
  no token values needed to change. Locked in with a contrast-ratio
  utility (`core/theme/contrast.dart`) and a test
  (`test/core/theme/contrast_test.dart`) so a future color edit can't
  silently regress it.
- Reason: scoped to the lowest-risk, most-used surfaces first (nav, HUD
  header, comments, story viewer, profile, collection, reactions, map,
  color palette) since this ships to a public prod app every cycle
  unattended.
- Risk: none open under this ticket. Any *new* screen/component should
  still get semantic labels and be checked against `contrastRatio()`
  before shipping - this closes the backlog item, not the discipline.
- Removal plan: n/a - closed.
- Owner: V2 improvement loop.
- Review date: closed 2026-07-25 (iter 42).

## TD-002: Map HUD header showed a placeholder "Lvl N" badge — CLOSED (iter 46, 2026-07-25)

- Area: backend `services/api/src/modules/users/api/routes.py` +
  `infrastructure/database/repositories/user.py`; V2 Flutter app
  (PakimonGO-V2 repo), `map_hud_screen.dart`'s `_hudRow`.
- Introduced: original V2 panel-prototype build; surfaced explicitly
  during the iter 45 (2026-07-25) "de-fake the live UI" pass, which fixed
  the two more severe cases (mission strip, Rank Hub season card) in that
  same iteration but scoped this one out as smaller and requiring a
  backend response change rather than a client-only fix.
- Fix (iter 46): added `get_user_total_points(db, user_id)` to
  `repositories/user.py` (sums `ScoreEvent.points` for the user's
  submissions - same semantics `get_leaderboard` ranks by, but as a
  single-user query rather than reusing the paginated/sensitive-filtered
  leaderboard query, which would have undercounted a user's own real
  total). Added `"totalPoints"` to the `GET /v1/users/me` response.
  Client: added `totalPoints` to `UserProfileResponse`, and a new
  `levelForPoints()` helper (`features/v2/domain/level.dart`) - a
  deliberately separate, uncapped points-per-level formula (50 pts/level)
  rather than reusing `SeasonCard.tiers` (that ladder has only 5 named
  tiers and would make the HUD number stall at "Lvl 5" forever past 1500
  points, which reads as broken progress on a HUD element whose whole
  point is to keep climbing). `map_hud_screen.dart`'s `_hudRow` now shows
  `levelForPoints(profile.totalPoints)` instead of `V2Dummy.level`;
  removed the now-dead `V2Dummy.level` field.
- Reason it was low-risk while open: a static number in a small HUD
  badge, not a progress claim with a fake countdown (the season card's
  bug) or fake feature content (the mission strip's bug).
- Verification: 5 new backend tests (`test_user_total_points.py`) +
  5 new Flutter tests (`level_test.dart` for the pure formula,
  `hud_streak_test.dart` for the real wiring, including a "no
  ProfileViewModel yet -> Lvl 1" case) - 216 API tests (was 211), 285 V2
  Flutter tests (was 280).
- Owner: V2 improvement loop.
- Review date: opened 2026-07-25 (iter 45), closed 2026-07-25 (iter 46).

## TD-003: The 300-line check exists in PakimonGO-V2 but was never being run — CLOSED (iter 49, 2026-07-26)

- Area: PakimonGO-V2 repo, `tools/qa/validate_docs.py`,
  `tools/qa/pre_task_check.py`.
- **Correction to the original framing (opened iter 45, 2026-07-25):**
  this ticket originally claimed PakimonGO-V2 "has no `tools/qa/` of its
  own" and needed a script built from scratch. That was wrong - checking
  before building (iter 49) found `tools/qa/validate_docs.py` and
  `tools/qa/pre_task_check.py` already exist in that repo, complete with
  a `check_file_sizes()` function, and have since Sprints 22-25 (`git log`
  confirms, well before this ticket was opened). The real problem was
  never a missing script: this session's workflow only ever ran the
  **v1** repo's validators (`ROOT = Path(__file__).resolve().parents[2]`
  resolves to whichever repo the script lives in, and every `python
  tools/qa/validate_docs.py` call this whole improvement loop was run
  from the v1 checkout) - so V2's own copy of the same check has been
  sitting there, correct, and simply never invoked against V2's edits
  for all of iters 1-49.
- Consequence found by finally running it: 8 files over 300 lines,
  including 2 introduced by this session's own iter-49 edits
  (`score_reveal_screen.dart` grew to 333 lines adding the wild-capture
  refresh fix; `capture_refresh_test.dart` grew to 315 adding its two new
  regression tests) - proof the rule really had been silently slipping,
  exactly as the original ticket suspected, just for the reason of an
  unrun check rather than a nonexistent one.
- Fix: (1) `check_file_sizes()` was flagging
  `.dart_tool/flutter_build/dart_plugin_registrant.dart`, a Flutter build
  artifact, as a false positive - `pre_task_check.py`'s own file-size
  check already excluded `.dart_tool`/`build`/`.pytest_cache`, so
  `validate_docs.py` was made consistent with it. (2) Split the two
  files this session had pushed over the limit:
  `score_reveal_screen.dart` (333 -> 243 lines) had its score-summary
  card and dummy breakdown-tile row extracted into a new
  `score_reveal_parts.dart` (138 lines); `capture_refresh_test.dart`
  (315 -> 168 lines) had its ~100 lines of duplicated mock-client/media-
  service/location-service scaffolding extracted into
  `capture_refresh_test_harness.dart` (101 lines), shared by all three
  tests. (3) Left the 5 remaining pre-existing warnings
  (`group_screen.dart` 314, `map_hud_screen.dart` 361,
  `story_viewer.dart` 314, `api_models.dart` 304, `mission_strip_test.dart`
  359) untouched this iteration - all are >300 WARN, not >500 FAIL, none
  were touched this session, and splitting files with no other reason to
  open them this iteration is unscoped churn with its own regression
  risk. Logged here as known, accepted warnings for a future iteration
  that has its own reason to be in those files.
- Verification: 293 V2 Flutter tests (unchanged count - these were pure
  refactors, not new behavior), `flutter analyze` clean, all 3 of V2's
  own QA scripts (`validate_docs.py`, `pre_task_check.py`,
  `scan_secrets.py`) now PASS when run from the V2 checkout.
- Removal condition met: V2's own `validate_docs.py`/`pre_task_check.py`
  now need to be run from the V2 checkout as part of every V2 edit going
  forward, the same way v1's validators are run for v1 edits - this is a
  workflow correction, not a one-time fix, so future iterations touching
  the V2 repo should include this step.
- Owner: V2 improvement loop.
- Review date: opened 2026-07-25 (iter 45), reframed and closed
  2026-07-26 (iter 49).

## TD-004: Feed shows an unconditional "verified" checkmark for every poster — CLOSED (iter 49, 2026-07-26)

- Area: backend `services/api/src/modules/feed/api/routes.py`; V2
  Flutter app (PakimonGO-V2 repo), `feed_post_card.dart` (the main
  social feed's post-header row) and `feed_viewmodel.dart`.
- Introduced: original V2 panel-prototype build; surfaced during the
  iter 48 (2026-07-25) profile-screen de-fake pass, which found and fixed
  the identical bug on `profile_v2_screen.dart` (an unconditional
  `Icon(Icons.verified)` next to the viewer's own name) but scoped this
  one out because it needs a backend change, not just a client fix.
- Fix (iter 49): `build_feed_page()` now joins `User` (outer join on
  `Submission.user_id`) and returns each item's `trustState` (defaulting
  to `"neutral"` if the join misses). `FeedItem` gained a `trustState`
  field (default `'neutral'`, so every existing test constructor stayed
  valid without changes), and `feed_post_card.dart`'s checkmark is now
  gated on `item.trustState == 'verified'`, matching the iter-48
  profile-screen pattern exactly. While in the same file, also fixed
  `docs/api/OPENAPI_DRAFT.yaml`'s `UserProfile.trustState` enum - it
  still listed `[trusted, normal, low, restricted]`, none of which the
  code has ever produced; the two real, reachable values are `neutral`
  (the DB column default) and `verified` (set only by the seed scripts).
  Replaced the invented moderation-tier values with the real enum rather
  than leaving speculative values that caused the exact "which one is
  right" confusion iter 48 had to work around.
- Reason it was medium risk while open: more visible than the
  profile-screen instance (shows once per post, every time the feed is
  viewed, for every poster) and slightly more misleading (implies every
  member of the community has been vetted).
- Verification: 2 new backend tests (`test_social.py` -
  `test_feed_shows_neutral_trust_state_by_default`,
  `test_feed_shows_verified_trust_state_for_a_verified_poster`) and 2 new
  Flutter tests (`feed_post_card_test.dart` - checkmark shows for a
  verified poster, hides for a neutral one, mirroring iter 48's
  show/hide pair rather than only testing the show case). Both pairs
  confirmed empirically to fail against the pre-fix code (backend:
  `KeyError: 'trustState'`; Flutter: unconditional icon found when none
  expected) and pass after. 218 API tests (was 216), 293 V2 Flutter tests
  (was 291).
- Owner: V2 improvement loop.
- Review date: opened 2026-07-25 (iter 48), closed 2026-07-26 (iter 49).

## Debt Entry Template

```md
## TD-000: Title

- Area:
- Introduced:
- Reason:
- Risk:
- Removal plan:
- Owner:
- Review date:
```
