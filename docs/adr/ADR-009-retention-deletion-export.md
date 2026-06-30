# ADR-009: Retention, Deletion, And Export

## Status

Proposed

## Context

The app stores account data, photos, exact locations, posts, comments, score events, AI evidence, moderation evidence, audit logs, and backups. Users need deletion and export flows.

## Options

### Minimized Retention With Legal/Audit Exceptions

- Pros: Privacy-preserving and easier to explain.
- Cons: Requires careful dependency mapping and deletion jobs.

### Long Retention By Default

- Pros: Easier debugging and abuse analysis.
- Cons: Higher privacy risk and harder compliance posture.

## Internal Challenge

Score integrity and moderation audits may require retaining some records after user deletion, but this must be minimized and documented.

## Decision

Use minimized retention by default. Delete, anonymize, or detach user-provided data within target retention windows while keeping legally required audit records in restricted form.

## Consequences

- Data model needs deletion state and anonymization paths.
- Backup deletion limitations must be disclosed.
- Export must cover user-provided machine-readable data.

## Reversal Conditions

- Legal review mandates different retention.
- Abuse/moderation requirements require longer restricted evidence retention.

## References

- Requirements: FR-AUTH-006, FR-AUTH-007, FR-AUTH-008, NFR-PRIV-005
- Related docs: `docs/DATA_MODEL_PLAN.md`, `docs/SECURITY_PRIVACY_PLAN.md`
