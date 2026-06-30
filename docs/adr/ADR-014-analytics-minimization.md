# ADR-014: Analytics Minimization

## Status

Proposed

## Context

The product needs metrics for onboarding, capture, scoring, retention, cost, and abuse, but user photos, exact locations, contacts, and minor-related data are sensitive.

## Options

### Minimal Product Analytics

- Pros: Lower privacy risk and clearer disclosures.
- Cons: Less behavioral detail for growth analysis.

### Broad Event Tracking

- Pros: More product insight.
- Cons: Greater consent, privacy, and compliance burden.

## Internal Challenge

Analytics are useful for balancing game loops, but the product should not normalize excessive tracking.

## Decision

Use minimized analytics: collect only events tied to success metrics, safety, reliability, and cost. Avoid exact coordinates, raw media, contacts, and unnecessary identifiers.

## Consequences

- Analytics events need a schema and review.
- Opt-out or consent controls may be required by region.
- Product metrics should rely on aggregate/derived data where possible.

## Reversal Conditions

- Legal review requires stricter consent or disables analytics in some regions.
- A privacy-preserving analytics provider is chosen with stronger guarantees.

## References

- Requirements: FR-CONSENT-005, NFR-COST-002, NFR-PRIV-001
- Related docs: `docs/DATA_MODEL_PLAN.md`, `docs/SECURITY_PRIVACY_PLAN.md`
