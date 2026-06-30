# API Service Scaffold

This is the planned backend API home. It is intentionally scaffold-only for now.

## Planned Responsibilities

- Verify Firebase Auth/App Check tokens.
- Issue scoped signed upload URLs.
- Own submissions, media metadata, posts, social graph, moderation, and score read APIs.
- Enforce authorization, visibility, privacy transforms, rate limits, and idempotency.
- Publish async work for media/evidence/scoring jobs.

## Module Layout

Each module should follow:

```txt
modules/<name>/
  api/
  application/
  domain/
  infrastructure/
```

`domain` must stay provider-neutral. Firebase, storage, queue, map, AI, and database adapters belong in `infrastructure`.
