# Shared Packages

Shared packages hold contracts and pure rules that need to be reused by app, API, workers, tests, or documentation generators.

Initial package boundaries:

- `contracts`: OpenAPI/JSON Schema/event schemas.
- `scoring-rules`: versioned score formulas and tests.
- `taxonomy`: taxonomy IDs, aliases, region status, imports.
- `geo-rules`: location privacy, geofence, cell, and suppression rules.
- `moderation-rules`: report categories and policy decision helpers.
- `privacy-rules`: reusable privacy classifications and transforms.
- `observability`: logging, tracing, metric naming, and alert conventions.

Keep packages small, provider-neutral, and heavily tested.
