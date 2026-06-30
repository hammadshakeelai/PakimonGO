---
id: okf-software-engineering-methodology-chain
type: methodology
status: draft
updated: 2026-07-01
source_docs:
  - docs/software-engineering/README.md
  - docs/SRS.md
  - docs/TRACEABILITY_MATRIX.md
related_requirements:
  - NFR-MAINT-003
---

# Methodology Chain

## Summary

PakimonGO follows the analysis-and-design chain from the external methodology:

`Inception -> SRS -> Process Model -> Use Cases -> Domain Model -> DFDs -> Design Class Diagram -> SSDs -> Operation Contracts -> Packages & CRC -> Final Report`

## Traceability Rule

Every feature should trace:

`FR -> UC -> Concept -> Class/Operation -> SSD Event -> Operation Contract -> Test`

## Handoff Notes

Future agents should update `docs/TRACEABILITY_MATRIX.md` whenever requirements, use cases, operations, contracts, or tests change.
