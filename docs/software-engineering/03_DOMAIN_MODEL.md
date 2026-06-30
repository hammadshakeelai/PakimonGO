# 03 Domain Model

## Conceptual Model

This is a conceptual vocabulary model, not software classes and not database schema.

```mermaid
classDiagram
  class User {
    user id
    age band
    trust state
    region
  }
  class Profile {
    display name
    privacy settings
    public stats setting
  }
  class ConsentRecord {
    policy version
    accepted at
    consent type
  }
  class CaptureDraft {
    local draft id
    created at
    draft state
  }
  class MediaAsset {
    asset id
    original/private flag
    derivative state
  }
  class Submission {
    submission id
    submitted at
    context
    scoring state
    visibility
  }
  class Observation {
    observation id
    animal context
    wild eligibility
  }
  class Taxon {
    taxon id
    accepted name
    common names
    sensitivity status
  }
  class LocationEvidence {
    exact coordinate
    accuracy
    public cell
  }
  class Geofence {
    venue type
    source version
    confidence
  }
  class ScoreEvent {
    ledger
    points
    formula version
    explanation
  }
  class DuplicateEdge {
    match type
    confidence
    threshold version
  }
  class Post {
    caption
    visibility
    moderation state
  }
  class Friendship {
    status
    created at
  }
  class Group {
    role policy
    visibility
  }
  class ModerationCase {
    category
    priority
    status
  }
  class Appeal {
    reason
    status
    outcome
  }
  class Leaderboard {
    scope
    period
    region policy
  }

  User "1" --> "1" Profile
  User "1" --> "*" ConsentRecord
  User "1" --> "*" CaptureDraft
  CaptureDraft "1" --> "0..1" MediaAsset
  User "1" --> "*" Submission
  Submission "1" --> "1..*" MediaAsset
  Submission "1" --> "1..*" Observation
  Observation "*" --> "0..1" Taxon
  Submission "1" --> "0..1" LocationEvidence
  LocationEvidence "*" --> "0..*" Geofence
  Submission "1" --> "*" ScoreEvent
  Submission "1" --> "*" DuplicateEdge
  Submission "0..1" --> "0..1" Post
  User "*" --> "*" Friendship
  User "*" --> "*" Group
  Post "0..1" --> "*" ModerationCase
  ScoreEvent "0..1" --> "*" Appeal
  Leaderboard "1" --> "*" ScoreEvent
```

## Concept List

| Concept | Meaning | Key Attributes |
|---|---|---|
| User | Account holder recognized by the product. | user id, age band, trust state, region. |
| Profile | User-facing identity and privacy display. | display name, avatar reference, public stats setting. |
| ConsentRecord | Proof that user accepted policy terms. | policy version, timestamp, type. |
| CaptureDraft | Local pre-submission capture. | draft id, device state, local metadata. |
| MediaAsset | Original, derivative, crop, or moderation media. | asset id, storage class, visibility, processing state. |
| Submission | User-submitted capture context. | context, timestamp, visibility, scoring state. |
| Observation | Animal observation within a submission. | primary/secondary, animal context, wild eligibility. |
| Taxon | Animal taxonomy concept. | external id, accepted name, aliases, sensitivity. |
| LocationEvidence | Private exact and derived public location data. | coordinate, accuracy, cell, transform version. |
| Geofence | Zoo, sanctuary, captive venue, or policy region. | geometry, source, venue type, version. |
| ScoreEvent | Immutable scoring ledger event. | ledger, points, formula version, explanation. |
| DuplicateEdge | Relationship between related/reused submissions. | source, target, match type, confidence. |
| Post | Social display wrapper for a submission. | caption, visibility, moderation state. |
| Friendship | Relationship enabling friend visibility and ranks. | status, initiator, accepted at. |
| Group | Social collection of users and posts. | owner, roles, visibility. |
| ModerationCase | Review object for content/user/score/report. | category, priority, status, action. |
| Appeal | User challenge of a scoring/moderation decision. | reason, status, outcome. |
| Leaderboard | Score projection by scope and period. | scope, region, period, snapshot time. |

## Association Rules

- A submission may have multiple observations, but one primary observation drives score display.
- A post wraps a submission only if visibility allows publishing.
- Score events never mutate; reversals are new score events.
- Duplicate edges relate submissions without deleting either submission.
- Exact coordinates belong to restricted location evidence; public map cells are derived.
- Moderation cases can affect posts, users, submissions, score events, groups, or comments.
