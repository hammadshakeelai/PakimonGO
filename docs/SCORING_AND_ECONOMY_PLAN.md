# Scoring And Economy Plan

## Goals

- Make scoring surprising and exciting without being random.
- Reward safe, honest, high-quality animal observation.
- Prevent duplicate farming, zoo farming, repost farming, and collusive likes.
- Let new users progress while keeping high-score play challenging.
- Keep every score auditable, versioned, and reversible.

## Score Event Model

Never store only one mutable score number. Store immutable score events:

- Base capture score.
- Species confidence adjustment.
- Rarity adjustment.
- Safety/respect adjustment.
- Image quality adjustment.
- Aesthetic/artistic adjustment.
- Naming/caption effort adjustment.
- Duplicate/cooldown adjustment.
- Zoo/captive adjustment.
- Pet owner tag credit.
- Social engagement score.
- Moderation rollback or penalty.

Total leaderboard score is computed from valid events.

## Suggested Components

### Animal Present

If no animal is detected or confidence is too low, score is zero or review-only.

### Species Confidence

Higher confidence can unlock rarity score. Low confidence should cap total score and ask for review or more context.

### Rarity

Rarity should be regional and seasonal where possible. It should not blindly reward species that are rare in biased datasets but common locally.

### Closeness And Safety

Do not reward dangerous closeness to wild animals. Estimate photographic closeness from crop size, sharpness, and occlusion, then combine with safety rules. Reward respectful distance for wild animals.

### Aesthetic And Artistic Quality

Use bounded points for composition, lighting, sharpness, moment, and creativity. Keep this lower weight than novelty and safety so expensive phones do not dominate.

### Names And Captions

Award small bonuses for real species names, useful notes, or creative cute names. Filter offensive names and avoid AI-generated unsafe suggestions.

### Zoo And Captive

Zoo photos:

- Save to collection.
- Can receive a tiny honesty/participation point if self-disclosed.
- Cannot receive normal wild rarity score.
- Hit strict diminishing returns after a small number of uploads.

### Pets

Pet photos can earn cute, social, and collection points. They should not receive wild rarity points. If the owner is tagged and accepts, both photographer and owner can receive bounded credit.

### Social Score

Likes, comments, reposts, and shares can add capped points. Social points must be fraud-damped by account age, relationship strength, rate limits, repeated interaction patterns, and moderation status.

## Catch-Up And Diminishing Returns

Use progression bands:

- New users receive onboarding quests and first-time discovery boosts.
- Low-score users receive mild catch-up multipliers.
- High-score users face stronger diminishing returns for common species, repeated locations, repeated zoo photos, and repeated social patterns.
- Rare, safe, high-quality, novel captures remain valuable for everyone.

## Negative Points

Negative or zero-score cases:

- Repeated duplicate farming.
- Web-scraped image reposting.
- Misleading zoo/captive context.
- Unsafe animal interaction.
- Spam uploads.
- Collusive likes or bot behavior.

Apply penalties carefully and explain them. Severe cases should trigger review.

## Versioning

Every score must store:

- Scoring formula version.
- AI model and prompt version.
- Evidence snapshot IDs.
- Geofence dataset version.
- Taxonomy version.
- Duplicate thresholds version.

Changing the formula should create new events or a migration plan, not silently rewrite history.

## Open Questions

- Exact point ranges.
- Rarity source and calibration.
- Whether pet score and wild score should be separate leaderboards.
- How much social score should matter.
- Whether negative points should affect public score or only trust score.
