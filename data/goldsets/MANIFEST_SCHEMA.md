# Goldset Manifest Schema

## Purpose

Goldsets benchmark AI/scoring behavior without committing private or unlicensed media directly into the repository.

## Storage Rule

Do not commit private user photos, exact real capture locations, contact data, moderation evidence, or licensed assets without documented permission. Store large/private assets outside Git and reference them through manifests.

## Manifest Format

Use one manifest per dataset:

```yaml
dataset_id: zoo-detection-alpha-001
dataset_type: zoo-detection
version: 0.1.0
license: synthetic-or-approved
created_at: 2026-07-01
owner: ai-data-lead
description: Boundary and captive/wild examples for zoo detection.
items:
  - item_id: zoo-boundary-001
    media_ref: external://goldsets/zoo-boundary-001.jpg
    expected_labels:
      animal_present: true
      eligibility: captive_uncertain
      should_rank_wild: false
    location_case:
      has_exact_location: false
      geofence_relation: overlaps_boundary
      gps_accuracy_case: coarse
    transformations:
      - original
      - compressed
    notes: synthetic or approved sample only
```

## Required Fields

| Field | Meaning |
|---|---|
| `dataset_id` | Stable dataset identifier. |
| `dataset_type` | One of duplicate-detection, zoo-detection, species-identification, scoring-calibration, sensitive-species. |
| `version` | Semantic dataset version. |
| `license` | Legal permission category. |
| `owner` | Person or role responsible. |
| `items[].item_id` | Stable item identifier. |
| `items[].media_ref` | External path or synthetic fixture path. |
| `items[].expected_labels` | Ground truth labels. |

## Benchmark Metrics

Duplicate:

- exact duplicate recall
- perceptual duplicate precision/recall
- crop duplicate precision/recall
- embedding similarity false-positive rate

Zoo/captive:

- inside geofence accuracy
- boundary uncertainty handling
- honest disclosure behavior
- false penalty near zoos

Species:

- top-1 candidate accuracy
- top-3 candidate accuracy
- confidence calibration
- no-animal false positives

Scoring:

- score stability by formula version
- catch-up and diminishing return behavior
- social score cap behavior
- rollback correctness

Sensitive species:

- suppression correctness
- public cell coarsening
- local leaderboard sparse-region hiding
