# ADR-006: Auth Platform

## Status

Proposed

## Context

PakimonGO needs Google sign-in, email/password, password recovery, phone verification/recovery, account deletion, and later iOS support.

## Options

### Firebase Authentication

- Pros: Supports Google, email/password, phone, Apple, account linking, mobile SDKs, and integration with Firebase App Check.
- Cons: Provider-specific flows need careful abstraction and deletion handling.

### Custom Auth

- Pros: Full control.
- Cons: High security burden and slower delivery.

### Auth0/Supabase Auth

- Pros: Strong managed auth alternatives.
- Cons: Different ecosystem fit; Firebase pairs naturally with mobile/App Check and storage.

## Internal Challenge

Firebase can create vendor lock-in, and phone auth has quota/cost/abuse issues. A custom backend will still need clean domain abstractions.

## Decision

Use Firebase Authentication behind an auth adapter. Do not let Firebase-specific user objects leak into domain models.

## Consequences

- iOS must add Sign in with Apple if required by App Store rules.
- Phone auth should be limited and abuse-controlled.
- Account deletion must be designed with backend data deletion/anonymization.

## Reversal Conditions

- Firebase pricing, region, or product limits block required flows.
- Backend framework offers a better compliant auth strategy.
- Legal review requires different identity handling.

## References

- Requirements: FR-AUTH-001 through FR-AUTH-006
- Related docs: `docs/SECURITY_PRIVACY_PLAN.md`, `docs/RESEARCH_BASELINE.md`
