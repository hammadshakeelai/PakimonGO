# Bugs And Risks

## Current Bugs

No known blocking bugs are recorded after the latest emulator walkthrough and
moderation/map hardening pass. See R-002 below for a real local-dev-only bug
found and fixed during the 2026-07-25 verification pass.

Latest recorded automated suite in `docs/TASK_LOG.md` (iter 49, 2026-07-26):
216 API tests, 78 scoring tests, 291 V2 + 163 V1 Flutter tests, and
`flutter analyze` clean on both repos. Iter 49 fixed two real gaps in
iter 47's HUD-refresh fix: it only refreshed the real points/level total
after a capped (zoo/pet/duplicate) capture, not a wild one, and the fix
for that was itself unsafe if the user navigated away from Score Reveal
before its scheduled auto-check fired (an unguarded `setState` after
dispose) - see `docs/TASK_LOG.md` iter 49 for both fixes and their
empirical verification.

## Repository Health Notes

- Original sprint packets through Sprint 46 are complete.
- Post-sprint hardening has continued with Render deploy, Postgres verification,
  Firebase/Groq live checks, APK optimization, user-facing moderation, map
  overhaul, and UI polish.
- Current doc validation scripts PASS.
- Current pre-task check PASS.

## Product Risks

- Users may harass, chase, touch, or endanger animals to gain points.
- Exact public location sharing may expose homes, routines, pets, children, or
  endangered species.
- Zoo detection may falsely deny valid photos near zoos or falsely allow zoo
  photos.
- Duplicate detection may punish legitimate repeated encounters or allow spam.
- AI scoring may be biased toward attractive photos, common animals, or
  well-lit environments.
- Contacts-based friend discovery may feel invasive if permissions are
  requested too early.
- Leaderboards may discourage new users if high-score users pull too far ahead.
- Social features create moderation, abuse, impersonation, and privacy
  obligations.
- User-facing report/block flows exist, but moderator console, appeals,
  takedown/restore workflow, and staffing are not built.
- App-store review may reject unsafe animal interaction incentives, incomplete
  legal docs, missing moderation operations, or weak privacy disclosures.
- Expanding toward Instagram/Facebook-like social features increases UGC,
  harassment, spam, addictive-loop, minor-safety, and moderation load risks.
- The clickable V2 HTML/CSS/JS prototype may make social/game features feel
  closer than they are. It must remain a planning artifact until approved
  requirements, traceability, moderation operations, privacy rules, and
  implementation work exist.
- The V2 prototype uses cropped concept-panel imagery as temporary visual
  texture. Replace it with real approved assets and re-check exact-location,
  sensitive-species, and minor-safety details before production design or app
  implementation.

## Technical Risks

- Map rendering, camera capture, and upload may stress low-end phones.
- No automated real-device E2E suite currently proves camera, map, upload, auth,
  and scoring together.
- No iOS build has been attempted.
- Local/default storage is not durable production object storage.
- In-process scoring worker has no persistent queue, retry policy, or DLQ.
- Push notifications are not implemented; notifications are still in-app polling.
- AI scoring costs may grow quickly with image volume.
- Animal recognition accuracy may be weak for local species, mixed animals,
  pets, blurry photos, or partial views.
- Real-time leaderboards and map feeds may need caching, denormalization, and
  rate limits.
- Large future conversations may exceed context windows unless raw archives and
  summaries are maintained.

## Required Mitigations

- Reward distance-respectful and safe observation; do not reward risky petting
  of unknown or wild animals.
- Blur or cell-aggregate public map locations by default.
- Use deterministic prechecks before AI scoring.
- Keep all score writes server-side.
- Keep submission cooldown/rate limiting active and move to a shared limiter if
  deployment becomes multi-instance.
- Report/block flows are implemented for users. Still provide moderator review,
  takedown/restore, appeals, and operational staffing before wider UGC exposure.
- Add catch-up mechanics and diminishing returns for repetitive uploads.
- Add real-device E2E before claiming beta readiness.
- Configure durable object storage before treating deployed media as production
  data.
- Keep V2 social/game UI ideas in concept/design until they are reviewed against
  V1 screenshots, safety, moderation, privacy, and traceability gates.

## R-001: CronCreate auto-resume timer does not survive session end

- Area: agent-driven autonomous continuation loop (V2 improvement iterations).
- Severity: Medium (breaks the "keep going unattended" workflow, not the product).
- Likelihood: Certain - confirmed on 2026-07-24 by a 7-day gap in TASK_LOG.md
  between iter 38 (2026-07-17) and iter 39, with no cron firing in between.
- Detection: `CronList` returned no scheduled jobs on resume, even though a
  one-shot timer was armed at the end of iter 38. CronCreate's own tool
  description states jobs are session-only and are deleted when the session
  ends - they do not persist across a closed CLI window/session boundary.
- Mitigation: for genuine unattended multi-day continuation, use the
  `RemoteTrigger`/`schedule` cloud-routine mechanism instead (runs in
  Anthropic's cloud, independent of any local session), not `CronCreate`.
  Creating a recurring cloud routine with push access to a public repo is a
  standing-configuration decision that needs the user's explicit sign-off
  (repo scope, cadence, model) - proposed to the user, not created silently.
- Owner: agent loop driver.
- Status: open - local CronCreate re-armed for same-session continuity only;
  cloud routine setup pending user confirmation.

## R-002: run_local.ps1 silently masked a failed seed step, leaving the local dev DB schema stale

- Area: local dev backend bootstrap (`run_local.ps1`, `services/api/scripts/seed.py`).
- Severity: Medium - did not affect the deployed Render/Postgres backend
  (verified healthy: `/health/live`, `/health/ready` both 200, `database:
  connected`, `/v1/feed` and `/v1/leaderboard` return real data). Local-only,
  but it meant the documented Quick Start command in `CLAUDE.md` silently
  produced a broken local database.
- Likelihood: Confirmed 2026-07-25 while verifying the app end-to-end
  (emulator + local backend) at the user's request. `services/api/pakimongo_dev.db`
  was last successfully bootstrapped 2026-07-07 - before migrations 004-010
  (blocks, social, follows, groups, quests, story_reactions, comment_likes)
  existed - so `GET /v1/leaderboard` 500'd locally with `sqlite3.OperationalError:
  no such table: blocks`.
- Detection: `run_local.ps1`'s seed step (`python -c "...exec(seed.py)..."`)
  had been failing with `ModuleNotFoundError: No module named 'sqlalchemy'`
  every run, because bare `python` on this machine's PATH resolves to an
  unrelated tool's virtualenv without this API's dependencies - but the
  script caught any nonzero exit code and printed "Seed completed (database
  may already have data)" regardless, so the failure was invisible.
  `seed.py` itself calls `Base.metadata.create_all()`, which is how the
  schema was meant to stay current between migrations; it just never ran.
- Mitigation: fixed `run_local.ps1` to (1) preflight-check that `python` can
  import fastapi/sqlalchemy/uvicorn before doing anything, printing a clear
  actionable error (with the resolved interpreter path and the
  `pip install -r services/api/requirements.txt` fix) instead of proceeding,
  and (2) stop masking seed failures - a failed seed step now prints the
  real error and exits nonzero instead of claiming success. Manually
  repaired the existing stale dev DB via `Base.metadata.create_all()` +
  `alembic stamp head`; re-verified `/v1/leaderboard`, `/v1/feed`,
  `/v1/users/me/collection`, and `/v1/notifications` all return real data
  locally after the fix.
- Caveat: the `alembic stamp head` marks the dev DB as "at migration 010"
  because `create_all()` built its schema from the current `models.py` -
  it does not prove `models.py` and the migration chain (001-010) agree
  on every column/constraint, only that `create_all()`'s idea of the
  schema now matches what's on disk. If they've drifted, a future
  migration 011 would apply against a dev DB shaped slightly differently
  than one built by replaying 001-010 from scratch on a fresh file. Low
  risk (Postgres prod runs the real migration chain, not `create_all()`),
  but worth knowing the stamp is asserted, not independently verified.
- Owner: local dev tooling.
- Status: fixed 2026-07-25 (iter 43) - script no longer silently swallows
  this failure mode; a future contributor whose `python` lacks the deps
  gets a clear message instead of a stale, silently-broken database.

## Risk Entry Template

```md
## R-000: Title

- Area:
- Severity:
- Likelihood:
- Detection:
- Mitigation:
- Owner:
- Status:
```
