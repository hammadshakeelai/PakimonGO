# Sprint 34 Plan: Pull-to-Refresh on Map

## Sprint Goal

Add pull-to-refresh gesture to the MapScreen so users can swipe down to reload sightings from the API.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S34-001 | Done | Wrap MapScreen body in `RefreshIndicator` | All body states refreshable (loading, error, no-token, map) | MapScreen renders with RefreshIndicator |
| S34-002 | Done | Connect pull to `fetchMarkers()` | `onRefresh` calls `_viewModel.fetchMarkers()` | Pull gesture triggers loading state |
| S34-003 | Done | 2 new widget tests | RefreshIndicator present + pull triggers fetch | 69 Flutter tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/features/map/presentation/map_screen.dart` | Mobile agent | RefreshIndicator wrapping |
| `test/features/map/map_screen_test.dart` | Mobile agent | Pull-to-refresh tests |
