# System Context Diagram

```mermaid
flowchart LR
  Player["Player / Teen Player"] -->|"capture, context, social actions"| PakimonGO["PakimonGO System"]
  Friend["Friend"] -->|"likes, comments, groups, friend ranks"| PakimonGO
  PetOwner["Pet Owner"] -->|"owner credit approval"| PakimonGO
  Moderator["Moderator"] -->|"case review, appeals, actions"| PakimonGO
  Admin["Admin"] -->|"policy, region, scoring, incident switches"| PakimonGO
  StoreReviewer["Store Reviewer"] -->|"demo account validation"| PakimonGO

  PakimonGO -->|"score state, collection, feed, map, ranks"| Player
  PakimonGO -->|"visible social content"| Friend
  PakimonGO -->|"credit request/outcome"| PetOwner
  PakimonGO -->|"case queues and evidence summaries"| Moderator
  PakimonGO -->|"audit, health, policy state"| Admin

  PakimonGO <--> Auth["Firebase Auth / App Check"]
  PakimonGO <--> Storage["Object Storage"]
  PakimonGO <--> Maps["Map Provider"]
  PakimonGO <--> AI["AI Vision Provider"]
  PakimonGO <--> Taxonomy["Taxonomy / Geofence Sources"]
  PakimonGO <--> Push["Push Notification Provider"]
```

## Notes

PakimonGO is the system boundary. External providers supply evidence or delivery capability, but PostgreSQL-backed backend state remains canonical product truth.
