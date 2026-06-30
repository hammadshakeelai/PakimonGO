# OKF Export Plan

## Purpose

OKF files are compact AI-readable summaries. They should help future agents load high-value context quickly without rereading all long-form docs.

## Current Inputs

- `docs/SRS.md`
- `docs/REQUIREMENTS.md`
- `docs/TRACEABILITY_MATRIX.md`
- `docs/ADR_REVIEW_PACK.md`
- `docs/WORK_PACKAGE_BOARD.md`
- `docs/security/THREAT_MODEL.md`
- `docs/data/DATABASE_ERD.md`
- `docs/software-engineering/`

## Current Outputs

- `knowledge/okf/index.md`
- `knowledge/okf/product/product-concept.md`
- `knowledge/okf/architecture/system-architecture.md`
- `knowledge/okf/requirements/requirements-core.md`
- `knowledge/okf/requirements/traceability-map.md`
- `knowledge/okf/software-engineering/methodology-chain.md`
- `knowledge/okf/privacy/location-privacy.md`
- `knowledge/okf/ai-scoring/scoring-pipeline.md`
- `knowledge/okf/tasks/current-task.md`

## Future Automation

Later scripts should:

- extract requirement IDs from docs
- check missing trace rows
- summarize ADR status
- produce compact module summaries
- update OKF files after accepted major changes

Generated OKF updates should be reviewed before commit.
