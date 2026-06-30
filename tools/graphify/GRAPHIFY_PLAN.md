# Graphify Plan

## Purpose

Graphify is prepared for future code-graph analysis after real source code exists. It should help future agents understand module relationships, dependency direction, requirement references, and risky file growth before edits.

## Planned Inputs

- `apps/mobile/pakimon_go_app/lib/`
- `services/api/src/`
- `services/workers/src/`
- `packages/`
- `docs/TRACEABILITY_MATRIX.md`
- `docs/adr/`

## Planned Outputs

Write generated outputs to `knowledge/graph/graphify-out/`:

- `graph.json`: machine-readable code graph.
- `GRAPH_REPORT.md`: human-readable summary.
- `requirement-links.csv`: requirement ID to file/module references.
- `hotspots.csv`: large, highly connected, or high-risk files.

## Analysis Rules

- Flag files over 300 lines for review.
- Flag source files over 500 lines as technical debt unless generated.
- Flag imports that bypass package/module boundaries.
- Flag mobile code referencing final scoring internals.
- Flag public DTOs that include exact coordinate fields.
- Flag provider SDK types leaking into domain objects.

## Activation Gate

Do not run Graphify as a required process until real code exists. Until then, this file defines expected graph behavior only.
