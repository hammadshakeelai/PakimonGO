# Sprint 45: Flutter Collection Screen

**Status**: completed
**Period**: 2026-07-03

## Goal

Add a species collection screen to the Flutter app: view captured species with points, counts, sorting, and context filtering.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S45-001 | `CollectionEntry` + `CollectionResult` models in api_models.dart | Done | api_models.dart |
| S45-002 | Typed `getCollection()` on CaptureRepository (sort, filter, pagination) | Done | capture_repository.dart |
| S45-003 | `CollectionViewModel` ChangeNotifier (fetch, sort, context filter, loading/empty/error) | Done | collection_viewmodel.dart |
| S45-004 | `CollectionScreen` with filter bar, species list, points, pull-to-refresh | Done | collection_screen.dart |
| S45-005 | "View Collection" button in ProfileScreen → CollectionScreen | Done | profile_screen.dart |
| S45-006 | 10 Flutter tests (6 viewmodel + 4 screen widget) | Done | collection_test.dart |

## Verification

- 123 Flutter tests pass (+10)
- 103 API + 61 scoring-rules + 123 Flutter = 287 total tests

## Next

Sprint 46: Further Flutter features.
