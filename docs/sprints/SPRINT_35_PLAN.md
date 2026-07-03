# Sprint 35: Submission History Screen

**Status**: completed  
**Period**: 2026-07-03  
**Requirement IDs**: FR-MAP-004

## Goal

Add a dedicated submission history screen that shows past submissions with scores, statuses, and species names, accessible from the main bottom navigation.

## Tasks

| ID   | Description | Status | Notes |
|------|-------------|--------|-------|
| S35-001 | Backend: add realName + animalContext to `_build_submission_response` | Done | Previously missing from returned dict |
| S35-002 | Flutter: add `realName` field to `SubmissionResponse` model | Done | Also added `toMarker()` conversion |
| S35-003 | Flutter: add `getSubmissions()` to `CaptureRepository` | Done | Calls GET /v1/submissions with params |
| S35-004 | Flutter: create `SubmissionHistoryViewModel` | Done | ChangeNotifier with fetch/loading/error |
| S35-005 | Flutter: create `SubmissionHistoryScreen` | Done | List with species, points, status; tap→SpeciesDetailScreen |
| S35-006 | Flutter: wire into `main.dart` as third History tab | Done | NavigationBar with Icons.history |
| S35-007 | Tests: 5 viewmodel + 4 widget + backend + widget_test | Done | 9 new Flutter tests |

## Verification

- 89 API tests pass (no regressions from realName addition)
- 61 scoring-rules tests pass
- 78 Flutter tests pass (69 old + 9 new)
- **228 total**, all passing
- QA validation: all 7 checks pass

## Next

Sprint 36: Photo thumbnail in species detail (fetch actual submission photo from API).
