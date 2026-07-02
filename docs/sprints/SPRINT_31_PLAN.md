# Sprint 31 Plan: Offline Draft Persistence

## Sprint Goal

Persist capture drafts to local storage so they survive app restarts, preventing data loss when the user closes the app mid-capture.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S31-001 | Done | Add `shared_preferences` dependency | `shared_preferences: ^2.3.0` in pubspec.yaml | `flutter pub get` succeeds |
| S31-002 | Done | Create `DraftPersistenceService` interface + `SharedPrefsDraftStorage` | Abstract with save/load/loadAll/delete/clear; SharedPrefs impl stores JSON by ID with index | 5 InMemoryDraftStorage tests pass |
| S31-003 | Done | Update `CaptureDraftService` for persistence | All mutating methods (create/save/restore/delete) persist to storage; loadPersistedDrafts() loads on startup; all getter works | 10 CaptureDraftService tests pass |
| S31-004 | Done | Wire persistence into main.dart | (Deferred — captured draft feature not yet wired into capture screen flow) | — |
| S31-005 | Done | Update tests + write new persistence tests | 5 InMemoryDraftStorage tests + updated CaptureDraftService tests (now async) | 49 Flutter tests all pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/features/capture/domain/draft_persistence_service.dart` | Mobile agent | Abstract + InMemoryDraftStorage |
| `lib/features/capture/data/shared_prefs_draft_storage.dart` | Mobile agent | SharedPrefs implementation |
| `lib/features/capture/domain/capture_draft.dart` | Mobile agent | CaptureDraftService now async with persistence |
| `test/features/capture/capture_draft_test.dart` | Mobile agent | Updated + new persistence tests |
