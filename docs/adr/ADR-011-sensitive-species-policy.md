# ADR-011: Sensitive Species Policy

## Status

Proposed

## Context

Public maps and leaderboards can expose rare, endangered, or easily disturbed animals. Exact locations can enable harm or harassment.

## Options

### Suppress/Coarsen Sensitive Species

- Pros: Protects animals and habitats.
- Cons: Less exciting map detail for some captures.

### Show All Public Observations

- Pros: Richer discovery map.
- Cons: Unacceptable safety and conservation risk.

## Internal Challenge

Users may be confused when their exact location is hidden or score/map behavior changes.

## Decision

Sensitive species rules can coarsen, delay, suppress, or review public map outputs and local leaderboard regions.

## Consequences

- Taxonomy data needs sensitivity rules and policy versions.
- Explanations should be shown where safe.
- Exact coordinates remain restricted.

## Reversal Conditions

- Legal/conservation guidance requires stricter suppression.
- Product narrows to private-only collections.

## References

- Requirements: FR-TAX-007, FR-MAP-005, FR-MAP-015, NFR-PRIV-001
- Related docs: `docs/ARCHITECTURE.md`, `docs/DATA_MODEL_PLAN.md`
