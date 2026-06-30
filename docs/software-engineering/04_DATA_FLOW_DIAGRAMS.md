# 04 Data Flow Diagrams

## Level 0 Context Diagram

```mermaid
flowchart LR
  Player["Player"] -->|capture, context, auth actions| System["PakimonGO System"]
  System -->|score state, collection, map, feed, leaderboards| Player
  Moderator["Moderator"] -->|case decisions| System
  System -->|case queues, evidence summaries| Moderator
  Admin["Admin"] -->|policy versions, feature flags| System
  System -->|audit reports, health state| Admin
  Provider["External Providers"] -->|auth, AI, map, taxonomy, storage results| System
  System -->|token checks, upload requests, evidence requests| Provider
```

## Level 1 Processes And Data Stores

```mermaid
flowchart LR
  P["Player"] --> P1["1.0 Identity and Consent"]
  P --> P2["2.0 Capture and Media"]
  P2 --> P3["3.0 Submission and Evidence"]
  P3 --> P4["4.0 Scoring and Eligibility"]
  P4 --> P5["5.0 Collections and Social"]
  P4 --> P6["6.0 Maps and Leaderboards"]
  P --> P7["7.0 Moderation and Appeals"]
  M["Moderator"] --> P7
  A["Admin"] --> P8["8.0 Policy and Operations"]

  D1[("D1 Users and Consent")]
  D2[("D2 Media Assets")]
  D3[("D3 Submissions and Observations")]
  D4[("D4 Evidence and AI Runs")]
  D5[("D5 Scores and Leaderboards")]
  D6[("D6 Social Content")]
  D7[("D7 Geo, Taxonomy, Geofences")]
  D8[("D8 Moderation and Audit")]

  P1 <--> D1
  P2 <--> D2
  P3 <--> D3
  P3 <--> D4
  P4 <--> D5
  P4 <--> D7
  P5 <--> D6
  P6 <--> D5
  P6 <--> D7
  P7 <--> D8
  P8 <--> D7
  P8 <--> D8
```

## Level 2: 3.0 Submission And Evidence

```mermaid
flowchart TD
  A["Uploaded media ready"] --> B["3.1 Validate media"]
  B --> C["3.2 Strip unsafe metadata"]
  C --> D["3.3 Generate derivatives and crops"]
  D --> E["3.4 Compute hashes and embeddings"]
  E --> F["3.5 Collect taxonomy and location context"]
  F --> G["3.6 Run structured AI evidence"]
  G --> H["3.7 Store evidence records"]
  H --> I["Queue scoring"]
```

## Level 2: 4.0 Scoring And Eligibility

```mermaid
flowchart TD
  A["Submission evidence"] --> B["4.1 Check duplicate edges"]
  A --> C["4.2 Check zoo/captive/pet eligibility"]
  A --> D["4.3 Check sensitive species"]
  B --> E["4.4 Apply score formula"]
  C --> E
  D --> E
  E --> F["4.5 Create immutable score event"]
  F --> G["4.6 Update projections"]
  G --> H["Return score state"]
```

## Functional Hierarchy

```txt
PakimonGO
  1.0 Identity and Consent
  2.0 Capture and Media
  3.0 Submission and Evidence
    3.1 Validate media
    3.2 Strip unsafe metadata
    3.3 Generate derivatives and crops
    3.4 Compute hashes and embeddings
    3.5 Collect taxonomy and location context
    3.6 Run structured AI evidence
    3.7 Store evidence records
  4.0 Scoring and Eligibility
    4.1 Duplicate checks
    4.2 Zoo/captive/pet checks
    4.3 Sensitive species checks
    4.4 Score formula
    4.5 Score event
    4.6 Projection update
  5.0 Collections and Social
  6.0 Maps and Leaderboards
  7.0 Moderation and Appeals
  8.0 Policy and Operations
```

## Balancing Notes

- Player capture/context inputs from Level 0 appear in Level 1 as identity, capture, submission, social, and moderation inputs.
- Provider evidence inputs from Level 0 appear in Level 1 as auth, storage, map, taxonomy, and AI provider flows.
- Moderator/admin actions from Level 0 appear in Level 1 as moderation, audit, policy, and operations flows.
