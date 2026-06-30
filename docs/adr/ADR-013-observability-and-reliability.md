# ADR-013: Observability And Reliability

## Status

Proposed

## Context

The system needs reliable capture upload, scoring jobs, moderation queues, privacy transforms, leaderboards, and incident response.

## Options

### Observability From First Runnable Service

- Pros: Easier debugging, safer alpha, supports SLOs.
- Cons: More setup during scaffold.

### Add Observability Later

- Pros: Faster initial code.
- Cons: Harder to diagnose scoring, privacy, and upload failures.

## Internal Challenge

Over-instrumentation can slow early work, but missing traces will make async failures painful.

## Decision

Add trace IDs, structured logs, metrics naming, and health endpoints from the first runnable backend service. Use Crashlytics for mobile and OpenTelemetry-compatible backend patterns.

## Consequences

- Logs must avoid exact coordinates, raw tokens, private URLs, and raw EXIF.
- Alerts become release-gate artifacts.
- Worker dead-letter queues and replay tools are required before broad alpha.

## Reversal Conditions

- Chosen deployment platform supplies equivalent managed observability.
- Product remains local prototype only.

## References

- Requirements: NFR-OBS-001 through NFR-OBS-003, NFR-REL-001 through NFR-REL-003
- Related docs: `docs/QA_AND_TEST_STRATEGY.md`, `docs/BUGS_AND_RISKS.md`
