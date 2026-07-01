# S0-008: Add Capture Draft Model Shell

## Goal

Represent local capture draft metadata without implementing full camera behavior.

## Requirements

- `FR-CAP-001`
- `FR-CAP-003`
- `FR-CAP-004`
- `FR-CAP-019`
- `NFR-MAINT-001`

## Owned Files

- `apps/mobile/pakimon_go_app/lib/features/capture/`
- `apps/mobile/pakimon_go_app/test/`

## Forbidden Files

- real camera plugin integration.
- upload implementation.
- scoring implementation.

## Acceptance Criteria

- Draft model includes local id, media reference, created time, context state, and lifecycle state.
- Draft can be created, restored, and deleted at model/test level.
- No exact location is required for local draft creation.

## Verification

```powershell
flutter test
```

Run from `apps/mobile/pakimon_go_app/` after Flutter shell exists.

## Rollback

Revert `feat(capture): add draft model shell`.

## Commit Target

`feat(capture): add draft model shell`
