# Mobile Features

Every feature folder uses this shape:

```txt
feature_name/
  data/
  domain/
  application/
  presentation/
```

- `domain`: pure models and business concepts owned by the feature.
- `application`: use cases, state machines, and orchestration.
- `data`: adapters to API, local storage, permissions, or platform plugins.
- `presentation`: screens, widgets, controllers, and view state.

Do not put final scoring, moderation authority, or leaderboard writes in mobile features. Those are backend-owned.
