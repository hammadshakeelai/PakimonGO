# QA And Test Strategy

## QA Philosophy

PakimonGO's riskiest behavior is not simple UI failure; it is unfair scoring, unsafe incentives, duplicate farming, zoo farming, location leaks, and social abuse. QA must test product rules as deeply as code.

## Detailed QA Specs

The executable-style QA planning docs live in `docs/qa/`. Start with `docs/qa/README.md`, then use the focused privacy, scoring, goldset, security, Android, CI, and ready/done specs for implementation work.

## Test Pyramid

- Unit tests: pure domain logic, scoring components, validators, privacy transforms.
- Integration tests: API, database, storage, queue, scoring jobs.
- Contract tests: mobile/backend schemas and event payloads.
- Golden dataset tests: animal recognition, duplicate detection, zoo detection, scoring stability.
- End-to-end tests: sign-in, capture, upload, score, collection, map, leaderboard.
- Manual QA: camera devices, permissions, map usability, store-review flows.

## Required Gold Datasets

Create controlled datasets under `data/goldsets/`:

- Wild animal photos.
- Pet photos.
- Zoo/captive photos.
- No-animal photos.
- Multi-animal photos.
- Blurry/occluded/low-light photos.
- Same-animal duplicate photos.
- Cropped, compressed, filtered, screenshot, and reposted variants.
- Common and rare species examples by region.

## Duplicate Matching Tests

Measure:

- Exact duplicate detection.
- Perceptual duplicate precision and recall.
- Crop-level duplicate detection.
- Embedding similarity thresholds.
- False positives between similar animals.
- False negatives after crop, filter, compression, or screenshot transformations.

Benchmark before any public scoring launch.

## Zoo Detection Tests

Measure:

- Inside zoo polygon.
- Near zoo boundary.
- GPS uncertainty overlaps boundary.
- Zoo-like exhibit context without geofence.
- Legitimate animal near a zoo but outside it.
- User honestly marked zoo.
- User hides zoo context.

Expected behavior: uncertain cases go to review or capped score, not confident false penalties.

## AI Scoring Tests

Measure:

- Top-1 and top-3 species candidate accuracy.
- Confidence calibration.
- Animal-present false positives.
- Pet/wild/captive classification.
- Aesthetic score stability.
- Score stability across model and prompt versions.
- Structured output schema compliance.
- Offensive or unsafe name/caption suggestions.

## Economy Tests

Test:

- New user catch-up.
- High-score diminishing returns.
- Zoo upload cap.
- Duplicate penalty.
- Social-like fraud damping.
- Country/local/global/friends ranking updates.
- Score rollback after moderation.

## Security And Abuse Tests

Test:

- GPS spoofing.
- Mock location flags.
- Impossible movement speed.
- EXIF spoofing.
- Web-scraped images.
- Bot uploads.
- Collusive likes.
- Repost farming.
- Contact spam.
- Report abuse.

## Release Gates

Alpha gate:

- Auth, capture, upload, private collection work.
- No exact public location leaks.
- Basic duplicate and zoo checks exist.

Beta gate:

- Gold datasets exist.
- UGC report/block exists.
- Score events are auditable.
- Crash reporting and monitoring exist.

Production gate:

- App-store privacy and UGC requirements complete.
- Moderation process staffed or clearly defined.
- Security review complete.
- Load test complete.
- Incident response plan complete.
