# Sprint 37: Map Marker Clustering

**Status**: completed  
**Period**: 2026-07-03  
**Requirement IDs**: FR-MAP-004

## Goal

Group nearby map markers into clusters when there are many sightings, reducing visual clutter and providing a species preview in the overlay.

## Tasks

| ID | Description | Status | Notes |
|---|---|---|---|
| S37-001 | Create `ClusterMarker` model + `ClusterService` utility | Done | Haversine distance-based clustering, 2km default radius |
| S37-002 | Update `MapViewModel` to expose `clusters` | Done | `_buildClusters()` runs on fetch; thresholds at >3 markers |
| S37-003 | Update `MapScreen` overlay with cluster info | Done | Shows "X clusters · Y sightings" when clustered |
| S37-004 | Write tests (6 cluster service + 2 viewmodel) | Done | |

## Verification

- 89 API tests pass
- 61 scoring-rules tests pass
- 86 Flutter tests pass (78 old + 8 new cluster tests)
- **236 total**, all passing
- QA validation: all 7 checks pass

## Next

Sprint 38: CI workflow update for new Flutter test count, or API error handling middleware.
