# ADR-008: Moderation And UGC Safety

## Status

Proposed

## Context

PakimonGO includes public/friends posts, comments, reposts, groups, hashtags, reports, blocks, and animal safety risks. Public exposure must not launch before moderation controls exist.

## Options

### Gated Social With Built-In Moderation

- Pros: Enables social roadmap while blocking risky exposure until controls pass.
- Cons: More upfront implementation than private-only MVP.

### Public Social First

- Pros: Faster growth loop.
- Cons: High risk for harassment, unsafe content, privacy leaks, and store rejection.

### Private-Only Alpha

- Pros: Safer.
- Cons: Delays validation of key social mechanics.

## Internal Challenge

Moderation tooling may feel heavy before many users exist, but lack of tooling blocks safe public UGC.

## Decision

Build social features behind gates. Require report, block, hide/delete, moderation queue, appeals path, audit logs, and critical feature-disable switches before broad public exposure.

## Consequences

- Public feed/comments/groups remain feature-flagged.
- Moderator evidence access must be purpose-limited.
- Store policy readiness becomes a release gate.

## Reversal Conditions

- Product scope narrows to private-only collection.
- A third-party moderation platform is chosen and replaces internal tooling.

## References

- Requirements: FR-SOC-007, FR-MOD-001 through FR-MOD-020
- Related docs: `docs/SECURITY_PRIVACY_PLAN.md`, `docs/BUGS_AND_RISKS.md`
