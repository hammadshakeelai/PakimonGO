# Mermaid Diagram Pack

## Purpose

This folder centralizes Mermaid diagrams for PakimonGO so the SRS, Software Engineering report, Obsidian vault, and future agents can reuse one clean set of visual artifacts.

## Diagram Index

- `SYSTEM_CONTEXT.md`: external actors and provider boundaries.
- `C4_CONTAINERS.md`: app, API, workers, database, storage, providers.
- `ARCHITECTURE_FLOW.md`: high-level runtime and evidence flow.
- `RELEASE_PROCESS.md`: release rings and gates.
- `METHODOLOGY_CHAIN.md`: Software Engineering artifact trace chain.
- `USE_CASE_OVERVIEW.md`: actors and major use cases.
- `DOMAIN_MODEL.md`: conceptual domain model.
- `DATA_FLOW.md`: DFD level 0, level 1, and key level 2 processes.
- `DATABASE_ERD.md`: database entity relationship view.
- `API_SEQUENCE_CAPTURE.md`: signed upload and capture scoring sequence.
- `SCORING_PIPELINE.md`: evidence, eligibility, scoring, and leaderboard pipeline.
- `PRIVACY_LOCATION_FLOW.md`: exact-to-public location transformation.
- `THREAT_MODEL.md`: trust boundaries and STRIDE controls.
- `UX_FLOWS.md`: onboarding, capture, map, report/block flows.
- `PACKAGE_DEPENDENCIES.md`: monorepo package and module dependencies.
- `DEPLOYMENT_VIEW.md`: planned Google Cloud/Firebase deployment shape.

## Rules

- Keep diagrams source-controlled as Mermaid in Markdown.
- Prefer one concept per file.
- Add figure captions when diagrams are copied into final reports.
- If a diagram changes a decision or requirement, update `docs/TRACEABILITY_MATRIX.md`, ADRs, and state docs as needed.
