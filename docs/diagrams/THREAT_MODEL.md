# Threat Model Diagram

```mermaid
flowchart TB
  subgraph Client["Untrusted Client Zone"]
    App["Mobile App"]
    DeviceSignals["GPS / Camera / Integrity Signals"]
  end

  subgraph TrustedBackend["Trusted Backend Zone"]
    API["API"]
    Workers["Workers"]
    Policy["Policy Engine"]
  end

  subgraph RestrictedData["Restricted Data Zone"]
    DB[("PostgreSQL")]
    Storage[("Private Originals")]
    Audit[("Audit Logs")]
  end

  subgraph External["External Provider Zone"]
    Auth["Firebase Auth/App Check"]
    AI["AI Provider"]
    Maps["Map Provider"]
    Push["Push Provider"]
  end

  App -->|"spoofing, replay, tampering risk"| API
  DeviceSignals -->|"GPS spoof / unsafe metadata risk"| API
  API --> Auth
  API --> DB
  API --> Storage
  API --> Workers
  Workers --> AI
  Workers --> DB
  API --> Maps
  API --> Push
  Policy --> API
  Policy --> Workers
  API --> Audit
  Workers --> Audit

  LocationLeak["Location leak"] -.mitigated by.-> Policy
  DuplicateFraud["Duplicate/zoo fraud"] -.mitigated by.-> Workers
  UGCAbuse["UGC abuse"] -.mitigated by.-> Policy
  AdminMisuse["Admin misuse"] -.mitigated by.-> Audit
```

## STRIDE Anchors

- Spoofing: auth, App Check, Play Integrity, risk signals.
- Tampering: server-authoritative scoring, idempotency, immutable score events.
- Repudiation: audit logs and trace IDs.
- Information disclosure: DTO tests, EXIF stripping, public cells.
- Denial of service: rate limits, queues, cost caps.
- Elevation of privilege: role checks and case-needed evidence.
