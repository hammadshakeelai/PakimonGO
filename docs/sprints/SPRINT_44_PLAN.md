# Sprint 44: Flutter Profile Screen

**Status**: completed
**Period**: 2026-07-03

## Goal

Add a profile/settings screen to the Flutter app: view user info, edit age band and home region, logout.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S44-001 | `updateProfile()` on `CaptureRepository` (PATCH /v1/users/me) | Done | capture_repository.dart |
| S44-002 | `ProfileViewModel` ChangeNotifier (fetch, edit, save, loading/error) | Done | profile_viewmodel.dart |
| S44-003 | `ProfileScreen` (info card, settings with ageBand/homeRegion, about, logout) | Done | profile_screen.dart |
| S44-004 | Person icon in app bar → ProfileScreen (replaces bare logout button) | Done | main.dart |
| S44-005 | 11 Flutter tests (8 viewmodel + 3 screen widget) | Done | profile_test.dart |

## Verification

- 113 Flutter tests pass (+11)
- 103 API + 61 scoring-rules + 113 Flutter = 277 total tests

## Next

Sprint 45: Further Flutter features.
