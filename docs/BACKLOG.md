# Backlog

## Intake

New ideas must be added here before implementation. Each item should later
become an issue, story, ADR, or explicit work package.

## Current Product Backlog

- Finalize MVP animal capture flow after real-device E2E feedback.
- Define scoring formula and point economy beyond the current prototype values.
- Define animal rarity taxonomy and source of truth.
- Define duplicate detection thresholds for same animal, same species, same
  owner pet, and changed appearance.
- Define zoo detection using geofences, Places/OSM data, user disclosure, and
  review.
- Define anti-spam and negative-point rules beyond the current cooldown and
  deterministic prechecks.
- Define catch-up mechanics so new and low-score users can progress.
- Define private/public/friends-only visibility and post sharing rules.
- Define pet owner tagging and shared credit.
- Define four leaderboard scopes: global, country, local, and friends.
- Define map layers for recent animals, species density, hotspots, and
  privacy-blurred points.
- Define waypoint routing behavior.
- Define contacts import, friend matching, invites, blocking, and reporting
  beyond the current user-facing block/report basics.
- Define moderation queues, moderator actions, appeals, and operational staffing.

## Current Engineering Backlog

Original sprint packets through Sprint 46 are complete. Post-sprint hardening
has continued with Render deploy, Firebase/Groq live verification, APK
optimization, Postgres verification, Flutter error handling, onboarding, age
gate, user-facing moderation, map overhaul, and UI polish.

Remaining work is launch hardening, production operations, app-store readiness,
and larger post-launch features.

### No-Credential / Local Work

- Review the V2 brainstorm in `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` against the
  V1 screenshots and promote approved social/game UI ideas into wireframes,
  requirements, traceability, and implementation tasks.
- Review the clickable V2 HTML/CSS/JS prototype in
  `docs/prototypes/v2-ui-html/index.html` and decide which screens become
  accepted wireframes versus visual inspiration only.
- Review the prototype's dummy interactions: map HUD, score reveal, feed
  reactions, group quests, notification filters, rank scopes, report/block, and
  appeal.
- Accessibility pass across mobile screens: semantic labels, screen-reader
  order, tap targets, and widget tests.
- Loading shimmer/skeleton states where the app still uses generic spinners.
- Automated real-device E2E plan and scripts for camera, map, upload, auth, and
  scoring.
- Moderator console, appeals, takedown/restore workflow, audit review, and
  staffing model.
- OpenAPI cleanup if placeholder v2 entries remain.
- Error analytics integration plan.

### Credential / Account-Dependent Work

- Mapbox production token and CI injection path. Local dev token wiring is done.
- Firebase release keystore SHA-1 registration. Debug Google sign-in was
  live-verified; release auth is not done.
- Durable object storage bucket (S3/GCS/equivalent). Local storage remains the
  default and is not production-safe.
- GitHub/Render deploy secrets if GitHub Actions deploys remain part of the
  release process.
- Long-term production Postgres decision/ops. Local pgvector and Render Postgres
  are verified; Cloud SQL or another durable production plan still needs owner
  sign-off.
- Store-review assets and accounts: screenshots, listing copy, age rating,
  reviewer credentials, privacy questionnaire.

### Future Features

- Field Stories: temporary story-style safe capture posts.
- Discovery Reels: short animal-moment clips after moderation readiness.
- Challenge cards, squad quests, habitat missions, and season leagues.
- Social post cards with visibility, reactions, comments, repost/share,
  hashtags, report, and block.
- Email/password auth (FR-AUTH-002).
- Friends and groups.
- Comments and likes.
- Public feed.
- Sharing and reposts.
- Hashtags and captions.
- Leaderboard scopes beyond the current implemented scope.
- Push notifications.
- iOS build and TestFlight path.

## Completed / Do Not Restart Without Regression Evidence

- FastAPI scaffold, DB models, Alembic baseline, repositories, and API routes.
- Upload intent, media validation, local upload, derivative URL stubs.
- Auth adapter pattern, fake auth, Firebase auth path, and Google sign-in flow.
- User profile endpoints and Flutter profile screen.
- Capture repository, camera picker integration, and offline draft persistence.
- Scoring service contract, Dummy/Groq/Google provider paths, async worker shell.
- Duplicate/zoo prechecks and goldset runner.
- Collection, leaderboard, notifications, pagination, filtering, sorting.
- Sensitive species suppression and public coarse location behavior.
- API version middleware, error middleware, CORS, and Render config.
- Docker Compose local dev and Postgres migration verification.
- Mapbox map prototype plus later marker/3D map overhaul.
- Age gate and onboarding.
- Flutter offline/error retry UI on data screens.
- Dark mode.
- User-facing report/block flows (FR-MOD-001..003, 009).
- APK split/R8 optimization.

## Process Backlog

- Expand templates only when a real process gap appears during implementation.
- Add Graphify generation workflow after a real consumer needs it.
- Extend docs lint and link-check workflow if Markdown formatting rules become
  a recurring issue.
- Make `.github/workflows/docs-validation.yml` a required branch check once
  repository settings are configured.
- Add max-file-size warning workflow once code ownership requires automated
  enforcement beyond `pre_task_check.py`.
- Add full visible conversation text to
  `docs/conversation-archive/raw/FULL_CONVERSATION_COPY_PASTE_HERE.txt` after
  user provides an export.
- Add OpenAPI linting and schema consistency checks.
- Generate final Software Engineering report after artifacts are accepted.
