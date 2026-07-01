# Release Process Diagram

```mermaid
stateDiagram-v2
  [*] --> LocalDev: Ring 0
  LocalDev --> InternalAPK: scaffold + local smoke
  InternalAPK --> InvitedAlpha: auth/capture/upload/private collection
  InvitedAlpha --> ClosedPlay: crash/perf/privacy gates
  ClosedPlay --> OpenBeta: moderation/social gates
  OpenBeta --> AndroidProd: production readiness
  AndroidProd --> IOSSpike: iOS compile spike
  IOSSpike --> TestFlight: Apple sign-in + privacy labels
  TestFlight --> IOSProd: App Store approval

  InvitedAlpha --> LocalDev: critical privacy/scoring failure
  ClosedPlay --> InvitedAlpha: moderation or store blocker
  OpenBeta --> ClosedPlay: abuse or reliability regression
  AndroidProd --> OpenBeta: production incident rollback
```

## Gates

- Alpha: no exact public location leaks, capture/upload/private collection work.
- Social: report, block, hide/delete, moderation, appeals, audit.
- Production: observability, runbooks, load tests, store disclosures, security review.
