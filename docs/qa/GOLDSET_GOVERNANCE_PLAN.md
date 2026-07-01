# Goldset Governance Plan

## Purpose

Goldsets are controlled benchmark datasets for animal presence, species identification, duplicate detection, zoo/captive detection, sensitive species, and scoring calibration.

## Location

Goldset metadata lives under `data/goldsets/`. Actual images should not be committed unless they are tiny, licensed fixtures approved for repository storage. Prefer object storage or local ignored folders for real benchmark media.

## Dataset Categories

| Category | Purpose |
|---|---|
| `animal-present` | prove animal/no-animal detection |
| `species-identification` | measure top-k taxon candidate accuracy |
| `duplicate-detection` | exact, perceptual, crop, screenshot, compression variants |
| `zoo-detection` | zoo, aquarium, sanctuary, petting zoo, near-boundary, uncertainty cases |
| `pet-vs-wild` | domestic pets, feral cases, livestock, common wild animals |
| `sensitive-species` | location suppression and policy behavior |
| `scoring-calibration` | rarity, novelty, aesthetics, safety, and cap behavior |
| `abuse-fixtures` | spoofed EXIF, reposted images, impossible movement, bot-like bursts |

## Source Rules

- Use only media the project is allowed to store, transform, and benchmark.
- Store license, source, consent status, and removal path in the manifest.
- Do not store exact private home locations in committed fixtures.
- Sensitive species examples must use synthetic/coarsened coordinates unless reviewed.
- User-submitted production photos cannot enter goldsets without explicit policy and consent.

## Manifest Requirements

Every goldset item must follow `data/goldsets/MANIFEST_SCHEMA.md` and include:

- stable item ID
- dataset version
- media reference
- expected labels
- known transformations
- privacy class
- source/license
- reviewer and review timestamp

## Versioning

Use semantic dataset versions:

```txt
goldset-duplicate-detection-v0.1.0
goldset-zoo-detection-v0.1.0
goldset-species-identification-v0.1.0
```

Changing labels, expected outcomes, or fixture composition increments the version. Benchmark reports must record dataset version, code commit, model/provider version, prompt version, and scoring formula version.

## Split Policy

| Split | Use |
|---|---|
| development | tuning thresholds |
| validation | pre-merge benchmark checks |
| holdout | release gate only, never threshold tuning |

Holdout results should be reviewed by a human before public scoring changes.

## Acceptance Metrics

Initial exact thresholds are deferred, but every benchmark report must include:

- precision
- recall
- false-positive examples
- false-negative examples
- abstain/review rate
- average latency
- cost per item when AI is used
- policy violations found

## Review Cadence

- Review goldset quality before Alpha scoring.
- Re-run goldset smoke tests before any AI provider, prompt, model, or duplicate threshold change.
- Archive old reports rather than overwriting them.
- Record any known dataset weakness in `docs/TECH_DEBT.md`.
