# ADR-005: Location Privacy

## Status

Accepted

## Context

Animal photos and public maps can expose homes, routines, pet owners, private property, and sensitive animal locations.

## Options

### Exact Public Pins

- Pros: Best exploration precision.
- Cons: High privacy and safety risk.

### User-Selectable Exact Sharing

- Pros: Gives advanced users control.
- Cons: Users may not understand long-term location risk.

### Privacy-Safe Aggregates By Default

- Pros: Safer for homes, pets, rare animals, and minors.
- Cons: Less precise exploration and route planning.

## Internal Challenge

Too much fuzzing could make the map less fun and reduce the Pokemon-Go-like feeling.

## Decision

Store exact coordinates privately, but expose public animal activity through clusters, cells, delayed display, or fuzzed points by default.

## Consequences

- Backend must derive public map cells.
- Local leaderboards use regions rather than raw coordinates.
- Exact sharing, if ever added, must be explicit and safety-reviewed.

## Reversal Conditions

- User testing shows map is unusable without more precision.
- Legal review requires stronger limits.
- Sensitive-species policy requires broader obfuscation.

## References

- Requirements: FR-MAP-002, FR-MAP-005, NFR-PRIV-001
- Related docs: `docs/SECURITY_PRIVACY_PLAN.md`, `knowledge/okf/privacy/location-privacy.md`
