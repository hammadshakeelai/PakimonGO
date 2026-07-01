# S0-001: Scaffold Flutter Project Shell

## Goal

Create the first runnable Flutter shell under `apps/mobile/pakimon_go_app/` while preserving the feature-first layout.

## Requirements

- `FR-AGE-001`
- `FR-ONB-001`
- `FR-CAP-001`
- `NFR-MAINT-001`
- `NFR-PORT-001`

## Owned Files

- `apps/mobile/pakimon_go_app/`
- `apps/mobile/pakimon_go_app/README.md`

## Forbidden Files

- `services/`
- `packages/scoring-rules/`
- production Firebase/map/AI config

## Acceptance Criteria

- Flutter project metadata exists.
- Existing feature folders remain readable.
- App shell can run or failure is documented with exact blocker.
- No real provider keys or private config are introduced.

## Verification

```powershell
flutter --version
flutter pub get
flutter test
```

Run from `apps/mobile/pakimon_go_app/` after scaffold exists.

## Rollback

Revert the short-burst commit `scaffold(mobile): add flutter shell`.

## Commit Target

`scaffold(mobile): add flutter shell`
