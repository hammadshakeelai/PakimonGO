# Sprint 40: User Notifications (Backend)

**Status**: completed
**Period**: 2026-07-03

## Goal

Add a notification system to the backend: DB model, API endpoints, and wiring into scoring events.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S40-001 | Notification DB model + Alembic migration 002 | Done | user_id, type, title, body, reference, is_read |
| S40-002 | Notification repository (create, list, mark_read, unread_count) | Done |  |
| S40-003 | GET /v1/notifications, PATCH /v1/notifications/{id}/read, GET /v1/notifications/unread-count | Done | Auth-protected, paginated, unread filter |
| S40-004 | Wire notifications into scoring (sync + async) | Done | Both routes.py and scoring_worker.py create notifications |
| S40-005 | 6 tests | Done | list, create, unread count, mark read, not found, unread filter |

## Verification

- 103 API tests + 61 scoring-rules + 86 Flutter = 250 total tests
- All QA validations pass

## Next

Sprint 41: Flutter notification center screen or production deployment CI/CD.
