# ADR-007: Backend Framework

## Status

Accepted

## Context

PakimonGO needs authenticated APIs, signed uploads, submission state, social features, map queries, scoring reads, moderation operations, and integration with workers.

## Options

### FastAPI Modular Monolith

- Pros: Strong OpenAPI support, Python AI/data ecosystem, fast iteration, clear module boundaries.
- Cons: Requires disciplined structure to avoid a loose script-style backend.

### Node/NestJS

- Pros: Strong TypeScript contracts and web ecosystem.
- Cons: AI/data integrations may need more cross-language glue.

### Go

- Pros: Excellent performance and deployment simplicity.
- Cons: Slower iteration for AI-heavy experiments and less ergonomic for early product discovery.

## Internal Challenge

FastAPI can become messy if modules bypass domain boundaries or put provider code into business logic.

## Decision

Use a FastAPI-style modular monolith for the initial API unless a spike proves another framework is better.

## Consequences

- Keep module layout explicit: `api`, `application`, `domain`, `infrastructure`.
- Generate OpenAPI early.
- Keep AI/provider adapters isolated.

## Reversal Conditions

- Python performance or deployment limits block NFRs.
- Team capacity strongly favors TypeScript or Go.
- Contract generation or testing becomes painful.

## References

- Requirements: NFR-PORT-002, NFR-MAINT-002, NFR-OBS-001
- Related docs: `docs/ARCHITECTURE.md`, `services/api/README.md`
