---
id: scoring-pipeline
type: ai_scoring
title: AI Scoring Pipeline
status: accepted
updated: 2026-07-01
source_docs:
  - docs/ARCHITECTURE.md
  - docs/QA_AND_TEST_STRATEGY.md
  - docs/adr/ADR-004-ai-scoring-pipeline.md
related:
  - requirements-core
  - location-privacy
---

# AI Scoring Pipeline

## Summary

Scoring uses a layered server-side evidence pipeline, not one AI call. Deterministic checks run before and after AI vision.

## Pipeline

1. Signed upload.
2. Private original storage.
3. Metadata stripping and thumbnail creation.
4. Hashes, perceptual hashes, quality metrics, crops, embeddings.
5. Zoo/captive geofence check.
6. AI vision structured extraction.
7. Taxonomy and rarity grounding.
8. Duplicate edge detection.
9. Versioned score event.
10. Publish, cap, reject, or review.

## Key Rules

- Zoo photos save but skip normal leaderboard score.
- Duplicate same-animal photos cannot farm points.
- Score explanations are stored.
- Social popularity score is capped and separate from wild rarity.
- Uncertain cases go to review.

## Decision State

ADR-004 is accepted. Exact provider mix, prompt format, and scoring formula remain future work.
