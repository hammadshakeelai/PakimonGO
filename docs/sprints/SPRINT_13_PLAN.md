# Sprint 13 Plan: Map Prototype Spike

## Sprint Goal

Begin Mapbox Flutter SDK integration: add dependency, create MapScreen, wire into app navigation, and verify rendering works.

## Sprint Status

**Complete.** 14 Flutter tests + 112 Python tests all passing.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S13-001 | ✅ DONE | Add mapbox_maps_flutter dependency | `pubspec.yaml` updated, `flutter pub get` succeeds | `flutter test` passes |
| S13-002 | ✅ DONE | Create AppConfig with MAPBOX_ACCESS_TOKEN env var support | Token read from `--dart-define`, fallback to empty string | `AppConfig.hasMapboxToken` works |
| S13-003 | ✅ DONE | Create MapScreen with MapWidget | Shows Mapbox map when token present, placeholder when absent | MapScreen renders without crash |
| S13-004 | ✅ DONE | Update main.dart with PakimonGoApp | Home screen is MapScreen, MapboxOptions.setAccessToken on start | App starts without crash |
| S13-005 | ✅ DONE | Update widget tests | Replace counter test with map presence test | 14 Flutter tests pass |

## Token Configuration

```bash
# Run with token:
flutter run --dart-define=MAPBOX_ACCESS_TOKEN=pk.eyJ...

# Test (no token needed, shows placeholder):
flutter test
```

## File Ownership

| Area | Owner |
|---|---|
| `pubspec.yaml` | Flutter app |
| `lib/core/config/app_config.dart` | Config |
| `lib/features/map/presentation/map_screen.dart` | Map feature |
| `lib/main.dart` | App entry point |
| `test/widget_test.dart` | Widget tests |
