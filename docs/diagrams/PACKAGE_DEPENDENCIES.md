# Package Dependency Diagram

```mermaid
flowchart TD
  Mobile["apps/mobile"] --> Contracts["packages/contracts"]
  Mobile --> MobileCore["mobile core adapters"]
  MobileCore --> Contracts

  API["services/api"] --> Contracts
  API --> ScoringRules["packages/scoring-rules"]
  API --> GeoRules["packages/geo-rules"]
  API --> PrivacyRules["packages/privacy-rules"]
  API --> ModerationRules["packages/moderation-rules"]

  Workers["services/workers"] --> Contracts
  Workers --> ScoringRules
  Workers --> GeoRules
  Workers --> PrivacyRules
  Workers --> ModerationRules

  API --> Infra["infrastructure/database/firebase/cloud-run"]
  Workers --> Infra

  Tools["tools"] --> Docs["docs"]
  Tools --> Knowledge["knowledge/okf + graph"]

  Contracts -.no provider types.-> API
  ScoringRules -.pure logic.-> Workers
```

## Boundary Rules

- Mobile does not compute final score.
- API/domain does not expose provider SDK types.
- Public contracts do not include exact normal capture coordinates.
- Workers are idempotent and append score events rather than mutating history.
