# Sprint 41: Flutter Notification Center

**Status**: completed
**Period**: 2026-07-03

## Goal

Add a notification center screen and app bar badge to the Flutter app, connecting to the backend notification endpoints.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S41-001 | `NotificationModel` in api_models.dart | Done | fromJson, all fields |
| S41-002 | `CaptureRepository.getNotifications()`, `markNotificationRead()`, `getUnreadNotificationCount()` | Done | |
| S41-003 | `NotificationViewModel` ChangeNotifier | Done | fetchNotifications, fetchUnreadCount, markAsRead |
| S41-004 | `NotificationScreen` with loading/empty/error/list states | Done | Pull-to-refresh, tap to mark read, read/unread styling |
| S41-005 | Bell icon with unread badge in app bar | Done | Navigates to NotificationScreen, refreshes on resume |
| S41-006 | 8 Flutter tests | Done | 5 viewmodel + 3 widget |

## Verification

- 94 Flutter tests pass (+8)
- 103 API + 61 scoring-rules + 94 Flutter = 258 total tests

## Next

Sprint 42: Production deployment CI/CD or further Flutter features.
