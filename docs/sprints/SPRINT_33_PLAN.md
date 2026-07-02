# Sprint 33 Plan: Species Detail Screen

## Sprint Goal

Create a detail screen showing species info, points, status, and location when tapping a map marker, with a marker list screen as an intermediate step.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S33-001 | Done | Create `SpeciesDetailScreen` | Shows species name, photo placeholder, points, status, lat/lng in info card | 4 widget tests pass |
| S33-002 | Done | Create `MarkerListScreen` | Tappable list of markers with color-coded avatars, navigation to detail | 4 widget tests pass |
| S33-003 | Done | Update MapScreen marker overlay | Overlay is tappable (GestureDetector + chevron), opens MarkerListScreen | widget_test.dart passes |
| S33-004 | Done | Widget tests | 8 total (4 species detail + 4 marker list) | 67 Flutter tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/features/species/presentation/species_detail_screen.dart` | Mobile agent | Detail screen |
| `lib/features/map/presentation/marker_list_screen.dart` | Mobile agent | Marker list |
| `lib/features/map/presentation/map_screen.dart` | Mobile agent | Overlay navigation |
| `test/features/species/species_detail_screen_test.dart` | Mobile agent | Detail tests |
| `test/features/map/marker_list_screen_test.dart` | Mobile agent | List tests |
