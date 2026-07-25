# Technical Debt Register

## Current Known Debt

Original sprint packets through Sprint 46 are complete, and post-sprint
hardening has continued beyond that structure. Latest recorded suite in
`docs/TASK_LOG.md` (as of iter 45, 2026-07-25): 211 API tests, 78 scoring
tests, 280 V2 + 163 V1 Flutter tests, and clean Flutter analysis on both
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

## TD-002: Map HUD header shows a placeholder "Lvl N" badge, not a real level

- Area: V2 Flutter app (PakimonGO-V2 repo), `map_hud_screen.dart`'s
  `_hudRow` (`PhotoAvatar(levelBadge: 'Lvl ${V2Dummy.level}')`).
- Introduced: original V2 panel-prototype build; surfaced explicitly
  during the iter 45 (2026-07-25) "de-fake the live UI" pass, which fixed
  the two more severe cases (mission strip, Rank Hub season card) found
  by the same review but scoped this one out as smaller and requiring a
  backend response change rather than a client-only fix.
- Reason: `GET /v1/users/me` does not currently return the viewer's
  total lifetime points, so there is no real value to derive a level
  from without a backend change first. The avatar photo itself is not
  counted as fake - no avatar-upload feature exists anywhere in the app,
  so a placeholder image there is a legitimate default asset (the same
  pattern as `V2Dummy.groupHero` for groups without a cover photo), not
  fabricated user state.
- Risk: Low - a static number in a small HUD badge, not a progress claim
  with a fake countdown (the season card's bug) or fake feature content
  (the mission strip's bug). Cosmetically inconsistent with the real,
  live-computed tier ladder `SeasonCard.tiers` already shows on the Rank
  Hub for the same user.
- Removal plan: add total points to the `/v1/users/me` response
  (`services/api/src/modules/users/api/routes.py` - the leaderboard
  repository already computes this per user), add the field to
  `UserProfileResponse`, and derive the badge from `SeasonCard.tiers`
  client-side (tier index, not a fabricated number) for consistency with
  the Rank Hub.
- Owner: V2 improvement loop.
- Review date: opened 2026-07-25 (iter 45).

## TD-003: The 300-line file-size rule has no automated check in PakimonGO-V2

- Area: cross-repo tooling. `tools/qa/validate_docs.py`'s
  `check_file_sizes()` only walks `SOURCE_ROOTS` inside this (v1) repo;
  PakimonGO-V2 is a separate git repository with no `tools/qa/` of its
  own, so CLAUDE.md rule #8 ("source files stay <=300 lines") is enforced
  in the V2 Flutter app entirely by an agent/contributor remembering to
  run `wc -l` by hand.
- Introduced: always true since PakimonGO-V2 was split into its own repo;
  surfaced during the iter 45 (2026-07-25) review, which found
  `rank_hub_parts.dart` had already drifted to 310 lines unnoticed (fixed
  same iter - see the closed history below) and noted two earlier close
  calls (`map_hud_parts.dart` at 337, `groups_list_screen.dart` at 305)
  that were only caught by manual inspection during iters 41 and 44.
- Risk: Low-medium - it's a discipline/maintainability rule, not a
  correctness one, but it has already silently slipped at least three
  times, meaning it will keep slipping without tooling.
- Removal plan: add an equivalent lightweight size-check script inside
  PakimonGO-V2 itself (that repo has no CI/validator suite yet at all),
  rather than reaching across repos from this validator, which would be
  fragile (depends on a specific sibling-checkout layout that isn't
  guaranteed).
- Owner: V2 improvement loop.
- Review date: opened 2026-07-25 (iter 45).

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
