# ADR-010: Age And Minor Policy

## Status

Proposed

## Context

The product is game-like and animal-focused, so it may attract minors. The user selected a 13+ launch posture, not an under-13 family product.

## Options

### 13+ Launch

- Pros: Avoids the heavy scope of a child-directed product while still allowing teens with stricter defaults.
- Cons: Requires clear age gate and non-child-directed positioning.

### All Ages Including Under-13

- Pros: Larger audience.
- Cons: Major COPPA/Families/privacy/location/social obligations.

## Internal Challenge

Even with a 13+ posture, the animal/game theme may be perceived as child-attractive.

## Decision

Launch as 13+ with neutral age gate, teen-safe defaults, and no under-13 accounts until a family mode is intentionally designed.

## Consequences

- Marketing and app-store copy must avoid child-directed positioning.
- Teen privacy defaults should be stricter.
- Under-13 attempts are blocked or diverted.

## Reversal Conditions

- Business chooses a family/children product.
- Legal review requires different age handling in target regions.

## References

- Requirements: FR-AGE-001 through FR-AGE-003
- Related docs: `docs/SRS.md`, `docs/SECURITY_PRIVACY_PLAN.md`
