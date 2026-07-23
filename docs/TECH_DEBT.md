# Technical Debt Register

## Current Known Debt

Original sprint packets through Sprint 46 are complete, and post-sprint
hardening has continued beyond that structure. Latest recorded suite in
`docs/TASK_LOG.md`: 145 backend tests, 69 scoring tests, 162 Flutter tests, and
clean Flutter analysis.

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

## TD-001: Accessibility pass is partial

- Area: V2 Flutter app (PakimonGO-V2 repo) + shared collection_screen.dart.
- Introduced: iter 39 (2026-07-24) closed the icon-button/tooltip and
  bottom-nav-selected-state gaps. Iter 40 (same day) closed the "selected
  reaction" gap on PostReactionRow and StoryReactionBar (both now expose
  `Semantics(selected:)` instead of only a visual color/scale change).
  Correction to the original iter-39 note: double-tap-to-Wow already had a
  non-gesture fallback (the persisted PostReactionRow buttons below every
  photo) - it just wasn't marked "selected" for assistive tech, which iter
  40 fixed. No new gesture-only dead end was found.
- Reason: scoped to the lowest-risk, most-used surfaces first (nav, HUD
  header, comments, story viewer, profile, collection, reactions) since
  this ships to a public prod app every cycle unattended.
- Risk: still open - Mapbox map markers (PointAnnotations drawn as raw PNG
  bytes) have no semantic exposure at all, so the living map has no
  screen-reader path; no color-contrast audit has been run against WCAG AA.
- Removal plan: next accessibility iteration - investigate Mapbox
  annotation semantics or a fallback list view for map sightings, then a
  contrast pass over V2Tokens' dark palette.
- Owner: V2 improvement loop.
- Review date: next accessibility-focused iteration.

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
