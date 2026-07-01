# Privacy Location Flow

```mermaid
flowchart LR
  A["Device foreground location"] --> B["Private capture location"]
  B --> C["Accuracy validation"]
  C --> D["Geofence overlap check"]
  C --> E["Sensitive species policy"]
  D --> F["Eligibility decision"]
  E --> G["Suppression/coarsening decision"]
  B --> H["Restricted exact coordinate table"]
  G --> I["Public cell / cluster"]
  G --> J["Delay window"]
  I --> K["Map activity API"]
  J --> K
  K --> L["User-facing map summary"]

  H -.never normal public API.-> X["No exact public pin"]
```

## Public Output Rules

- Public APIs return cells/clusters, not exact normal capture coordinates.
- Sensitive species can be delayed, coarsened, hidden, or sent to review.
- Waypoints target general areas, not exact animal pins.
