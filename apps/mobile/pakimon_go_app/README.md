# PakimonGO Flutter App Scaffold

This folder is reserved for the Flutter app. The current scaffold defines intended module boundaries only; production Dart code will be added after SRS/ADR acceptance.

## Planned Layout

- `lib/app/`: app bootstrap, top-level providers, shell, and routing composition.
- `lib/core/`: cross-cutting app concerns such as config, errors, permissions, network, routing, and theme.
- `lib/features/`: feature-first slices with `data`, `domain`, `application`, and `presentation` subfolders.
- `lib/shared/`: small reusable widgets and models with no feature ownership.
- `lib/l10n/`: user-facing strings once localization starts.
- `test/`: unit and widget tests.
- `integration_test/`: device/integration tests for camera, upload, auth, map, and scoring flows.

## Feature Rules

Each feature owns its UI, state, use cases, models, and tests unless a concept is truly shared. Feature code must reference server contracts instead of inventing client-only scoring or privacy rules.

## First Future Vertical Slice

The first implementation slice should be onboarding, auth shell, camera draft, signed upload stub, private collection placeholder, and pending score state.
