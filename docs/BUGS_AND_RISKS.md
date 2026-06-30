# Bugs And Risks

## Current Bugs

No app code exists yet, so there are no implementation bugs.

## Repository Health Notes

- Previous broken Git metadata was repaired with fresh `git init` on 2026-07-01.
- Empty scaffold folders now contain `.gitkeep` placeholders so Git can track the intended structure.

## Product Risks

- Users may harass, chase, touch, or endanger animals to gain points.
- Exact public location sharing may expose homes, routines, pets, children, or endangered species.
- Zoo detection may falsely deny valid photos near zoos or falsely allow zoo photos.
- Duplicate detection may punish legitimate repeated encounters or allow spam.
- AI scoring may be biased toward attractive photos, common animals, or well-lit environments.
- Contacts-based friend discovery may feel invasive if permissions are requested too early.
- Leaderboards may discourage new users if high-score users pull too far ahead.
- Social features create moderation, abuse, impersonation, and privacy obligations.

## Technical Risks

- Map rendering, camera capture, and upload may stress low-end phones.
- AI scoring costs may grow quickly with image volume.
- Animal recognition accuracy may be weak for local species, mixed animals, pets, blurry photos, or partial views.
- Real-time leaderboards and map feeds may need caching, denormalization, and rate limits.
- App-store review may reject unsafe animal interaction incentives or weak UGC moderation.
- Large future conversations may exceed context windows unless raw archives and summaries are maintained.

## Required Mitigations

- Reward distance-respectful and safe observation; do not reward risky petting of unknown or wild animals.
- Blur or cell-aggregate public map locations by default.
- Use deterministic prechecks before AI scoring.
- Keep all score writes server-side.
- Add rate limits, cooldowns, duplicate checks, and negative-point rules.
- Provide report, block, delete, moderation, and appeal flows.
- Add catch-up mechanics and diminishing returns for repetitive uploads.

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
