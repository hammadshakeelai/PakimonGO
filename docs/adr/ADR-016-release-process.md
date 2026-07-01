# ADR-016: Release Process

## Status

Accepted

## Context

PakimonGO needs Android APK internal testing first, Google Play production later, and iOS/TestFlight/App Store support after Android readiness.

## Options

### Ring-Based Release

- Pros: Controls risk, supports feature flags, store review, staged rollout, and rollback.
- Cons: Requires release discipline and environment config.

### Direct Public Launch

- Pros: Faster.
- Cons: Unsafe for UGC, maps, scoring, privacy, and moderation.

## Internal Challenge

The full product vision is broad, so release gates must prevent unfinished social/global features from leaking early.

## Decision

Use ring-based releases: local/staging, internal APK, invited Android alpha, closed Play testing, open beta, Android production, iOS TestFlight, iOS production.

## Consequences

- Feature flags and region config are release requirements.
- Store disclosures and demo accounts must be prepared before store review.
- Production release requires observability, security review, load tests, and incident runbooks.

## Reversal Conditions

- Product scope narrows to offline/private prototype.
- Store requirements force a different sequencing.

## References

- Requirements: NFR-PORT-001, FR-LB-001, FR-SOC-010
- Related docs: `docs/ROADMAP.md`, `docs/EXPANDED_BLUEPRINT.md`
