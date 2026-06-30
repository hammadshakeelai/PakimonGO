# 06 System Sequence Diagrams

## SSD: UC-004 Submit Capture For Scoring

```mermaid
sequenceDiagram
  actor Player
  participant System as PakimonGO System
  Player->>System: requestSignedUpload(draftId, mediaMetadata)
  System-->>Player: uploadIntent(uploadUrl, mediaAssetId, expiresAt)
  Player->>System: completeUpload(mediaAssetId, checksum)
  System-->>Player: mediaReady(mediaAssetId)
  Player->>System: submitCaptureForScoring(draftId, attributes, visibility)
  System-->>Player: submissionAccepted(submissionId, scoreStatePending)
  Player->>System: getSubmissionScoreState(submissionId)
  System-->>Player: scoreState(status, explanationSummary)
```

## SSD: UC-006 Explore Map Activity

```mermaid
sequenceDiagram
  actor Player
  participant System as PakimonGO System
  Player->>System: getMapActivity(viewport, filters)
  System-->>Player: mapActivity(cells, clusters, suppressedReason?)
  Player->>System: setWaypoint(targetArea)
  System-->>Player: waypointRoute(generalAreaRoute)
```

## SSD: UC-010 Report Or Block

```mermaid
sequenceDiagram
  actor Player
  participant System as PakimonGO System
  Player->>System: reportContent(targetId, category, notes)
  System-->>Player: reportAccepted(caseId)
  Player->>System: blockUser(targetUserId)
  System-->>Player: blockConfirmed(blockId)
```

## SSD: UC-013 Review Moderation Case

```mermaid
sequenceDiagram
  actor Moderator
  participant System as PakimonGO System
  Moderator->>System: openModerationQueue(filters)
  System-->>Moderator: moderationCases(caseSummaries)
  Moderator->>System: reviewModerationCase(caseId)
  System-->>Moderator: caseEvidenceSummary(caseNeededEvidence)
  Moderator->>System: applyModerationAction(caseId, action, reason)
  System-->>Moderator: actionRecorded(auditId, resultingState)
```

## System Operation Names

The SSD messages are the canonical operation names for contracts:

- `requestSignedUpload(draftId, mediaMetadata)`
- `completeUpload(mediaAssetId, checksum)`
- `submitCaptureForScoring(draftId, attributes, visibility)`
- `getSubmissionScoreState(submissionId)`
- `getMapActivity(viewport, filters)`
- `setWaypoint(targetArea)`
- `reportContent(targetId, category, notes)`
- `blockUser(targetUserId)`
- `openModerationQueue(filters)`
- `reviewModerationCase(caseId)`
- `applyModerationAction(caseId, action, reason)`
