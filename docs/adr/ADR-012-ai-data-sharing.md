# ADR-012: AI Data Sharing

## Status

Proposed

## Context

AI providers may process photos, captions, metadata, location-derived context, and prior user/submission context. This data can be sensitive.

## Options

### Minimal Structured AI Context

- Pros: Lower privacy/cost risk and easier auditability.
- Cons: May reduce model accuracy.

### Full Context To AI Provider

- Pros: Better reasoning potential.
- Cons: Higher privacy exposure and cost.

## Internal Challenge

AI needs enough context to distinguish wild, pet, zoo, duplicate, and unsafe interaction cases, but not raw private data unless necessary.

## Decision

Send minimized, purpose-bound, structured context to AI providers. Prefer derived/fuzzed fields over exact coordinates, record model/prompt versions, and keep deterministic checks outside the LLM.

## Consequences

- AI runs need audit records and schema validation.
- Provider terms and data retention settings must be reviewed.
- Goldsets must test model drift and structured-output compliance.

## Reversal Conditions

- AI provider policy is incompatible with privacy needs.
- Local/on-device or self-hosted models become accurate and affordable enough.

## References

- Requirements: FR-SCORE-001, FR-SCORE-004, NFR-AUDIT-001, NFR-COST-001
- Related docs: `docs/SCORING_AND_ECONOMY_PLAN.md`, `docs/QA_AND_TEST_STRATEGY.md`
