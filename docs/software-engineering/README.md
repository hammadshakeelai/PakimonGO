# Software Engineering Artifact Set

## Purpose

This folder follows the reusable methodology from:

`C:/Users/HP/Documents/GitHub/projects/SE-Hakari-Bankai/docs/Software Engineering Process/METHODOLOGY.md`

The chain is:

```txt
Inception -> Requirements/SRS -> Process Model -> Use Cases -> Domain Model
-> DFDs -> Design Class Diagram -> SSDs -> Operation Contracts
-> Packages & CRC -> Final Report
```

## Artifact Index

- `00_INCEPTION.md`: problem, vision, scope, actors, technology, repo setup.
- `01_PROCESS_MODEL.md`: selected software process and fallback.
- `02_USE_CASES.md`: diagram, high-level use cases, and expanded use cases.
- `03_DOMAIN_MODEL.md`: conceptual domain classes, attributes, and relationships.
- `04_DATA_FLOW_DIAGRAMS.md`: Level 0, Level 1, key Level 2 flows, and hierarchy.
- `05_DESIGN_CLASS_DIAGRAM.md`: planned software classes, methods, interfaces, and boundaries.
- `06_SYSTEM_SEQUENCE_DIAGRAMS.md`: SSDs for essential use cases.
- `07_OPERATION_CONTRACTS.md`: Larman-style contracts for system operations.
- `08_PACKAGES_CRC.md`: package dependencies and CRC cards.
- `09_FINAL_REPORT_PLAN.md`: final assembled report order and build plan.
- `../diagrams/`: canonical Mermaid diagram pack for report and Obsidian reuse.

## Traceability Rule

Every feature must trace:

```txt
FR -> Use Case -> Domain Concept -> Design Class/Operation -> SSD Event -> Operation Contract -> Test Case
```
