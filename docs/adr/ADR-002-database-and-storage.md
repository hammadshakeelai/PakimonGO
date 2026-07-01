# ADR-002: Database And Storage

## Status

Accepted

## Context

PakimonGO needs relational social data, leaderboards, geospatial queries, duplicate detection, AI audit trails, and fast media delivery.

## Options

### PostgreSQL + PostGIS + pgvector + Object Storage

- Pros: Strong relational integrity, geospatial indexes, vector similarity, score auditability, mature migrations.
- Cons: More backend work than Firebase-only, requires database operations discipline.

### Firebase-Only

- Pros: Fast mobile development, realtime sync, simple client integration.
- Cons: Weaker fit for complex joins, geospatial rules, vector search, versioned scoring, and audit-heavy leaderboards.

### Hybrid Firebase + PostgreSQL

- Pros: Firebase handles auth/app integrity/storage integration; PostgreSQL handles canonical relational, geo, and vector truth.
- Cons: More moving parts and synchronization boundaries.

## Internal Challenge

Hybrid systems can become over-engineered early. Firebase-only would speed MVP learning if scoring and map queries are simplified.

## Decision

Use a hybrid approach: Firebase Auth/App Check/Storage where useful, with PostgreSQL as canonical product database using PostGIS and pgvector.

## Consequences

- Server-side APIs must mediate access to canonical data.
- Database schema and migrations matter early.
- Media must be stored in object storage, not PostgreSQL.

## Reversal Conditions

- Prototype shows PostgreSQL operational burden is too high for team capacity.
- Firebase Data Connect or similar managed paths cover the needed SQL workflow cleanly.
- Product scope narrows enough to remove geospatial/vector/audit needs.

## References

- Requirements: FR-SCORE-001, FR-MAP-002, FR-LB-001, NFR-SEC-001
- Related docs: `docs/ARCHITECTURE.md`
- External: https://postgis.net/, https://github.com/pgvector/pgvector, https://firebase.google.com/docs/data-connect
