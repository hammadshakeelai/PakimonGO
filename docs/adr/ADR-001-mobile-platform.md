# ADR-001: Mobile Platform

## Status

Proposed

## Context

PakimonGO needs Android APK/internal testing first, Google Play production later, and iOS support after that. The app needs camera, maps, animation, uploads, auth, and a polished game-like experience.

## Options

### Flutter

- Pros: One codebase for Android and iOS, strong custom UI, mature mobile build tooling, good fit for map/camera-heavy UI.
- Cons: Native SDK integrations may need platform-specific code, and the team must validate map/camera performance.

### Native Android First

- Pros: Best Android platform control and direct CameraX/Play API access.
- Cons: iOS later becomes a second app and may force duplicated product logic.

### React Native

- Pros: Strong if team already uses React, broad ecosystem.
- Cons: Game-like map/camera polish can require native bridging and careful performance work.

## Internal Challenge

Native Android may be faster for the APK target and lower risk for camera/location APIs. If the iOS version is far away, cross-platform abstraction might slow the first release.

## Decision

Use Flutter as the default platform, pending prototype validation for camera, map rendering, upload reliability, and low-end Android performance.

## Consequences

- Shared product code can move to iOS later.
- Native platform channels may be needed for advanced camera, integrity, or location checks.
- UI and feature modules must be kept small and feature-first.

## Reversal Conditions

- Flutter camera/map prototype fails performance or reliability targets.
- Required SDK features are unavailable or unstable in Flutter.
- Team capacity strongly favors native Android and accepts a separate iOS build later.

## References

- Requirements: FR-CAP-001, FR-MAP-001, FR-AUTH-001
- Related docs: `docs/RESEARCH_BASELINE.md`, `docs/REPO_STRUCTURE.md`
- External: https://docs.flutter.dev/deployment/android
