# 07 Operation Contracts

Contracts use Larman-style postconditions in past tense.

## Contract: requestSignedUpload(draftId, mediaMetadata)

| Field | Detail |
|---|---|
| Cross-references | UC-004, `FR-CAP-011`, `FR-CAP-017`, `NFR-SEC-005` |
| Preconditions | User was authenticated; draft existed; media metadata was valid enough for upload intent. |
| Postconditions | An upload intent was created. A media asset placeholder was created in pending upload state. A short-lived scoped upload URL was associated with the media asset. An audit/log correlation id was recorded. |

## Contract: completeUpload(mediaAssetId, checksum)

| Field | Detail |
|---|---|
| Cross-references | UC-004, `FR-CAP-012`, `FR-CAP-013`, `FR-CAP-014` |
| Preconditions | Upload intent existed, belonged to the user, and had not expired beyond retry policy. |
| Postconditions | The media asset state was changed to uploaded or verified. Duplicate completion attempts were recognized idempotently. Original media remained private. Media processing job was queued. |

## Contract: submitCaptureForScoring(draftId, attributes, visibility)

| Field | Detail |
|---|---|
| Cross-references | UC-004, `FR-CAP-*`, `FR-SCORE-003`, `FR-SCORE-008` |
| Preconditions | User was authenticated; uploaded media asset existed; required attributes passed validation; visibility was allowed. |
| Postconditions | A submission was created. Submission attributes were recorded. Location evidence was stored privately when available. Initial scoring state was set to pending or review. Evidence/scoring jobs were queued. No final score was exposed. |

## Contract: getSubmissionScoreState(submissionId)

| Field | Detail |
|---|---|
| Cross-references | UC-004, `FR-SCORE-003`, `FR-SCORE-004`, `FR-LB-010` |
| Preconditions | User was authorized to view the submission. |
| Postconditions | Query operation; no state changed. Score state, visible explanation summary, and pending/review/capped status were returned according to visibility rules. |

## Contract: getMapActivity(viewport, filters)

| Field | Detail |
|---|---|
| Cross-references | UC-006, `FR-MAP-*`, `NFR-PRIV-*`, `NFR-PERF-003` |
| Preconditions | Map feature was enabled for the region; viewport and filters were valid. |
| Postconditions | Query operation; no canonical state changed. Public activity cells or clusters were returned. Exact normal capture coordinates were not returned. Sensitive or risky locations were coarsened, delayed, or suppressed. |

## Contract: setWaypoint(targetArea)

| Field | Detail |
|---|---|
| Cross-references | UC-006, `FR-MAP-008`, `FR-MAP-009` |
| Preconditions | Target area was a privacy-safe area, not an exact animal pin. |
| Postconditions | A waypoint preference was created or updated for the user session. A route summary to a general area was returned. Background tracking was not enabled. |

## Contract: reportContent(targetId, category, notes)

| Field | Detail |
|---|---|
| Cross-references | UC-010, `FR-MOD-001`, `FR-SOC-007` |
| Preconditions | User was authenticated; target existed and was reportable; rate limits allowed report creation. |
| Postconditions | A report was created. A moderation case was created or linked. Reporter trust and abuse signals were updated. Audit metadata was recorded. |

## Contract: blockUser(targetUserId)

| Field | Detail |
|---|---|
| Cross-references | UC-010, `FR-MOD-003`, `FR-SOC-006` |
| Preconditions | User was authenticated; target user existed; target was not the same user. |
| Postconditions | A block relationship was created or refreshed. Restricted content visibility was changed for both parties according to policy. Future interactions were prevented. |

## Contract: applyModerationAction(caseId, action, reason)

| Field | Detail |
|---|---|
| Cross-references | UC-013, `FR-MOD-007`, `FR-MOD-008`, `FR-MOD-009`, `FR-SCORE-020` |
| Preconditions | Moderator had required role; case existed; action was valid for the case type. |
| Postconditions | A moderation action was created. Case status was changed. Affected content, score event, group, or account state was updated. Audit record was appended. Notification was queued where safe/legal. Leaderboard rollback was queued if score state changed. |
