# ADR-004: AI Scoring Pipeline

## Status

Accepted

## Context

PakimonGO needs to identify animals, evaluate rarity, detect duplicates, handle zoo/pet/captive context, assess image quality/aesthetics, and assign fair points.

## Options

### Single LLM Vision Call

- Pros: Fast to prototype, flexible reasoning.
- Cons: Expensive, hard to test, inconsistent, weak against duplicates and location abuse.

### Deterministic Rules Only

- Pros: Predictable, cheap, testable.
- Cons: Weak at visual interpretation, species ambiguity, aesthetics, and caption/name evaluation.

### Hybrid Evidence Pipeline

- Pros: Combines deterministic checks, image hashes, embeddings, geofences, taxonomy, and AI structured output.
- Cons: More complex to build and test.

## Internal Challenge

Hybrid architecture may slow MVP. A smaller LLM prototype could validate user delight before building the full evidence pipeline.

## Decision

Use a hybrid evidence pipeline. MVP may start with fewer stages, but the architecture must preserve versioned evidence, structured AI outputs, and deterministic prechecks.

## Consequences

- Async jobs are required.
- Gold datasets are required before launch scoring.
- Score explanations and versions must be stored.
- AI provider can be swapped behind adapters.

## Reversal Conditions

- AI cost or latency is unacceptable.
- Deterministic scoring satisfies MVP without LLM reasoning.
- Legal/privacy constraints limit AI image processing.

## References

- Requirements: FR-SCORE-001 through FR-SCORE-007
- Related docs: `docs/SCORING_AND_ECONOMY_PLAN.md`, `docs/QA_AND_TEST_STRATEGY.md`
