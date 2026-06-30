# Methodology Compliance Checklist

## Source

`C:/Users/HP/Documents/GitHub/projects/SE-Hakari-Bankai/docs/Software Engineering Process/METHODOLOGY.md`

## Checklist

| Stage | Required Artifact | PakimonGO File | Status |
|---|---|---|---|
| Stage 0 | Inception | `docs/software-engineering/00_INCEPTION.md` | Complete draft |
| Stage R | SRS | `docs/SRS.md`, `docs/REQUIREMENTS.md` | Complete draft |
| Assignment 01 | Process model | `docs/software-engineering/01_PROCESS_MODEL.md` | Complete draft |
| Assignment 02 | Use cases | `docs/software-engineering/02_USE_CASES.md` | Complete draft |
| Assignment 03 | Domain model | `docs/software-engineering/03_DOMAIN_MODEL.md` | Complete draft |
| Assignment 04 | DFDs | `docs/software-engineering/04_DATA_FLOW_DIAGRAMS.md` | Complete draft |
| Assignment 05 | Design class diagram | `docs/software-engineering/05_DESIGN_CLASS_DIAGRAM.md` | Complete draft |
| Assignment 06 | SSDs | `docs/software-engineering/06_SYSTEM_SEQUENCE_DIAGRAMS.md` | Complete draft |
| Assignment 07 | Operation contracts | `docs/software-engineering/07_OPERATION_CONTRACTS.md` | Complete draft |
| Packages & CRC | Package diagram and CRC | `docs/software-engineering/08_PACKAGES_CRC.md` | Complete draft |
| Assignment 08 | Final report plan | `docs/software-engineering/09_FINAL_REPORT_PLAN.md` | Planned |
| Traceability | FR -> UC -> concept -> class/op -> SSD -> contract -> test | `docs/TRACEABILITY_MATRIX.md` | Complete draft |

## Remaining Methodology Work

- Render diagrams for final report visuals.
- Build combined report document once content is accepted.
- Add generated table of contents and page numbers if exporting to `.docx` or PDF.
- Create automated consistency checks for requirement IDs and trace rows.
- Add detailed fully-dressed use cases beyond the three most critical flows.

## Rule For Future Changes

When a requirement changes, update all downstream artifacts in the traceability chain before committing:

```txt
SRS -> use case -> domain model -> DFD/design class -> SSD -> contract -> tests
```
