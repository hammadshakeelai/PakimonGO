# Bugs And Risks

## Current Bugs

No known blocking bugs are recorded after the latest emulator walkthrough and
moderation/map hardening pass.

Latest recorded automated suite in `docs/TASK_LOG.md`: 145 backend tests, 69
scoring tests, 162 Flutter tests, and `flutter analyze` clean. This file update
did not re-run those full suites; it re-ran the pre-task guard and validation
scripts.

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
