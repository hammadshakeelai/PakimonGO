# Sprint 36: Photo Thumbnail in Species Detail

**Status**: completed  
**Period**: 2026-07-03  
**Requirement IDs**: FR-MAP-004

## Goal

Replace the photo placeholder in SpeciesDetailScreen with a real thumbnail image served from the API, with fallback states for loading and error.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S36-001 | Add `mediaAssetId` to `SubmissionMarker` model | Done | Required for URL construction |
| S36-002 | Replace photo placeholder with `Image.network(thumbnailUrl)` | Done | Thumbnail via `/v1/media/files/thumbs/{id}.jpg` |
| S36-003 | Handle loading (placeholder) and error (fallback message) states | Done | `loadingBuilder`/`errorBuilder` on `Image.network` |
| S36-004 | Update all SubmissionMarker constructors across tests | Done | 4 test files updated |
| S36-005 | Update species_detail_screen_test for Image widget | Done | |

## Verification

- 89 API tests pass
- 61 scoring-rules tests pass
- 78 Flutter tests pass
- **228 total**, all passing
- QA validation: all 7 checks pass

## Next

Sprint 37: Map marker clustering or CI workflow update.
