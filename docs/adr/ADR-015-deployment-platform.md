# ADR-015: Deployment Platform

## Status

Deferred

Google Cloud/Firebase-first remains the accepted alpha planning direction. Final production deployment approval is deferred until cloud project, budget, region, and compliance review.

## Context

The API, workers, database, storage, queues, auth, and monitoring need a deployable cloud path that fits Firebase, Cloud SQL, object storage, and mobile releases.

## Options

### Google Cloud/Firebase First

- Pros: Natural fit for Firebase Auth/App Check, Cloud SQL, Cloud Storage, Cloud Run, and Play ecosystem.
- Cons: Vendor concentration and cost-management needs.

### Multi-Cloud Early

- Pros: Avoids lock-in.
- Cons: Too much operational burden before product validation.

### Self-Hosted VPS

- Pros: Simple cost floor.
- Cons: Weak fit for managed mobile auth, storage, observability, and scale.

## Internal Challenge

Google Cloud makes sense for the chosen services, but costs and regional constraints must be monitored.

## Decision

Use Google Cloud/Firebase-first deployment for alpha planning: Cloud Run for API/workers, Cloud SQL PostgreSQL, Cloud Storage, Firebase Auth/App Check, and managed logging/monitoring.

## Consequences

- Infrastructure docs should live under `infrastructure/`.
- Secrets must use managed secret storage, not repo files.
- Cost budgets and region policy must be defined before beta.

## Reversal Conditions

- Cost, region, compliance, or vendor terms block launch needs.
- Another cloud offers materially better app integrity/auth/database fit.

## References

- Requirements: NFR-SEC-005, NFR-COST-002, NFR-PORT-002
- Related docs: `docs/RESEARCH_BASELINE.md`, `infrastructure/README.md`
