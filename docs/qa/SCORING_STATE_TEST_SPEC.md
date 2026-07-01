# Scoring State Test Spec

## Purpose

The scoring state machine protects fairness. The client can submit evidence, but only the server can finalize score events or leaderboard eligibility.

## States

| State | Meaning |
|---|---|
| `pending` | submission exists, durable, not prechecked |
| `prechecked` | deterministic validation completed |
| `ai_evaluated` | AI/vision evidence stored but not final |
| `scored` | score finalized and eligible if no quarantine |
| `capped` | score saved with cap due to zoo/pet/uncertainty/duplicate rules |
| `review` | manual or automated review required |
| `rejected` | no score due to invalid, unsafe, abusive, or impossible submission |
| `rolled_back` | previous score reversed through immutable adjustment |

## Valid Transitions

| From | To | Trigger |
|---|---|---|
| `pending` | `prechecked` | upload complete and deterministic checks pass |
| `pending` | `review` | missing evidence, risk signal, or uncertain location |
| `pending` | `rejected` | corrupt media, forbidden content, or invalid request |
| `prechecked` | `ai_evaluated` | structured AI evidence accepted |
| `prechecked` | `capped` | deterministic cap: duplicate, zoo disclosure, pet context |
| `prechecked` | `review` | duplicate/zoo/location uncertainty |
| `ai_evaluated` | `scored` | final server scoring succeeds |
| `ai_evaluated` | `capped` | AI plus rules require bounded score |
| `ai_evaluated` | `review` | low confidence or safety concern |
| `review` | `scored` | moderator/reviewer approves score |
| `review` | `capped` | moderator/reviewer applies cap |
| `review` | `rejected` | moderator/reviewer rejects |
| `scored` | `rolled_back` | immutable rollback event |
| `capped` | `rolled_back` | immutable rollback event |

## Invalid Transitions

Never allow:

- client-sent final state changes
- `pending -> scored`
- `rejected -> scored`
- `rolled_back -> scored`
- `scored -> scored` mutation without a new adjustment event
- `capped -> scored` mutation without review/adjustment event

## Required Test Cases

| ID | Test | Requirement |
|---|---|---|
| `TC-SCORE-STATE-001` | valid transition table accepts all allowed edges | `FR-SCORE-008` |
| `TC-SCORE-STATE-002` | invalid direct finalization is rejected | `FR-SCORE-002`, `FR-SCORE-003` |
| `TC-SCORE-STATE-003` | every final state stores formula version | `FR-SCORE-007` |
| `TC-SCORE-STATE-004` | score event is append-only, not overwritten | `FR-SCORE-005`, `FR-SCORE-006` |
| `TC-SCORE-STATE-005` | zoo disclosure can cap but still save collection entry | `FR-SCORE-009`, `FR-SCORE-010` |
| `TC-SCORE-STATE-006` | duplicate detection can cap/review without deleting submission | `FR-DUP-006`, `FR-DUP-007` |
| `TC-SCORE-STATE-007` | unsafe interaction routes to review/rejection | `FR-SCORE-016`, `FR-MOD-014` |
| `TC-SCORE-STATE-008` | rollback updates leaderboard projection | `FR-SCORE-020`, `FR-LB-009` |

## Property Tests

When code exists, add generated/property tests for:

- every state has at least one valid inbound path except `pending`
- every terminal state is immutable except through adjustment/rollback
- no transition skips audit for final score changes
- leaderboard eligibility is false for `pending`, `review`, `rejected`, and `rolled_back`

## Explanation Rule

Every final user-visible score state must include a short explanation category. The exact formula can stay hidden, but the reason class must be testable: `normal`, `duplicate_cap`, `zoo_cap`, `pet_cap`, `review_required`, `unsafe_rejected`, or `low_confidence`.
