# Worker Service Scaffold

Async workers handle slow or risky tasks outside request/response paths.

Planned job families:

- `media`: validate images, strip EXIF, generate thumbnails/crops.
- `evidence`: hashes, perceptual hashes, embeddings, AI vision outputs.
- `scoring`: score state machine, formula versioning, rollback events.
- `moderation`: report enrichment, safety queues, takedown workflows.
- `leaderboards`: snapshot/projection updates from immutable score events.
- `privacy`: public cell generation, suppression, delay, and sensitive species transforms.

Workers must be idempotent and auditable. Retried jobs must not duplicate score events or public posts.
