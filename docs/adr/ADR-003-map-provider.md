# ADR-003: Map Provider

## Status

Deferred

Final map provider selection is deferred. Mapbox-first prototyping remains the accepted spike direction, with Google Maps Platform retained as challenger.

## Context

PakimonGO needs a polished game-like map, player location, animal activity overlays, privacy-safe clusters, and simple waypoint routes.

## Options

### Mapbox First

- Pros: Strong custom styling, layers, clustering, vector tiles, and game-like visual control.
- Cons: Google POI/routing content may not be freely mixed; cost and Flutter SDK maturity need validation.

### Google Maps Platform First

- Pros: Familiar map quality, strong routing, Places, POI, and platform trust.
- Cons: Less game-like by default, content terms may constrain custom non-Google map combinations.

### OSM-Only Stack

- Pros: Maximum control and open data potential.
- Cons: More operations burden, routing/tiles/geocoding quality require significant work.

## Internal Challenge

Google Maps may be safer for a consumer app if Places and Routes quality matter more than visual customization. Choosing Mapbox too early could create legal/content integration issues.

## Decision

Prototype Mapbox first for the game-like map. Reopen if Google Places/Routes quality becomes essential or Mapbox Flutter performance/cost fails.

## Consequences

- Public animal map should use backend-generated clusters or vector tiles.
- Zoo data should come from backend geofences and license-compatible sources.
- Legal review is needed before mixing provider data.

## Reversal Conditions

- Prototype map performance is poor.
- Google POI/routing becomes core to MVP.
- Provider cost model is unacceptable.
- Terms prevent required data display.

## References

- Requirements: FR-MAP-001 through FR-MAP-005
- Related docs: `docs/ARCHITECTURE.md`, `docs/RESEARCH_BASELINE.md`
