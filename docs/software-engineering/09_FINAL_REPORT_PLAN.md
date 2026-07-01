# 09 Final Report Plan

## Report Order

The final Software Engineering report should follow the methodology order:

1. Title page.
2. Table of contents.
3. Process model.
4. Requirements and use cases.
5. Domain model.
6. Data flow diagrams.
7. Design class diagram.
8. System sequence diagrams.
9. Operation contracts.
10. Packages and CRC cards.
11. Supporting material.

## Source Files

| Report Chapter | Source |
|---|---|
| Process model | `docs/software-engineering/01_PROCESS_MODEL.md` |
| Requirements | `docs/SRS.md`, `docs/REQUIREMENTS.md` |
| Use cases | `docs/software-engineering/02_USE_CASES.md` |
| Domain model | `docs/software-engineering/03_DOMAIN_MODEL.md` |
| DFDs | `docs/software-engineering/04_DATA_FLOW_DIAGRAMS.md` |
| Design class diagram | `docs/software-engineering/05_DESIGN_CLASS_DIAGRAM.md` |
| SSDs | `docs/software-engineering/06_SYSTEM_SEQUENCE_DIAGRAMS.md` |
| Operation contracts | `docs/software-engineering/07_OPERATION_CONTRACTS.md` |
| Packages and CRC | `docs/software-engineering/08_PACKAGES_CRC.md` |
| Supporting material | ADRs, threat model, OpenAPI, data model, QA plan, traceability matrix |
| Diagram appendix | `docs/diagrams/` |

## Build Principle

The final report should be assembled from the same source docs instead of being hand-written separately. That prevents the standalone artifacts and final report from drifting.

## Future Output Targets

- Markdown combined report.
- `.docx` report with generated table of contents.
- PDF export for visual QA.
- Diagram images or rendered Mermaid diagrams with figure captions.

## Mermaid Diagram Sources

Use the canonical Mermaid sources in `docs/diagrams/` when assembling the report:

- System context and C4 containers.
- Methodology chain and use case overview.
- Domain model, DFDs, design class view, ERD.
- API sequence, scoring pipeline, privacy location flow.
- Threat model, UX flows, package dependencies, deployment view.
