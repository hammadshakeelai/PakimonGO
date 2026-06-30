# Data Model Plan

## Database Direction

Use PostgreSQL as canonical product state. Add PostGIS for location/geofence queries and pgvector for image/crop similarity search. Store photos in object storage, not in PostgreSQL.

## Core Entities

### Identity

- `users`
- `auth_identities`
- `user_profiles`
- `account_deletion_requests`
- `user_settings`

### Social Graph

- `friendships`
- `contact_invites`
- `blocks`
- `groups`
- `group_memberships`

### Media And Submissions

- `media_assets`
- `media_derivatives`
- `submissions`
- `submission_attributes`
- `observations`
- `collections`
- `collection_items`

### Animal Knowledge

- `taxa`
- `taxon_aliases`
- `taxon_regions`
- `rarity_snapshots`
- `identifications`

### AI Evidence

- `ai_runs`
- `ai_run_outputs`
- `image_hashes`
- `image_embeddings`
- `animal_crops`
- `quality_metrics`
- `duplicate_edges`
- `encounter_groups`

### Geospatial

- `capture_locations`
- `public_location_cells`
- `geofences`
- `geofence_sources`
- `map_activity_tiles`
- `local_regions`

### Scoring

- `score_events`
- `score_totals`
- `score_formula_versions`
- `leaderboard_entries`
- `leaderboard_snapshots`
- `trust_events`

### Social Content

- `posts`
- `post_visibility_rules`
- `captions`
- `hashtags`
- `post_hashtags`
- `likes`
- `comments`
- `reposts`
- `shares`

### Moderation

- `reports`
- `moderation_queue_items`
- `moderation_actions`
- `appeals`
- `policy_versions`
- `audit_logs`

## Indexing Strategy

- B-tree indexes for IDs, owners, status, timestamps, and foreign keys.
- GiST indexes for PostGIS geometries/geographies.
- pgvector indexes for embedding similarity after benchmark validation.
- Partial indexes for active public posts, pending moderation, and leaderboard windows.
- Composite indexes for feed and leaderboard query paths.

## Media Storage Strategy

Object storage paths:

```txt
originals/{user_id}/{submission_id}/{asset_id}
derivatives/{visibility}/{asset_id}/{size}
ai-crops/{submission_id}/{crop_id}
moderation/{case_id}/{asset_id}
```

Rules:

- Originals private.
- Public derivatives generated after policy checks.
- Immutable paths.
- Metadata stored in database.
- Signed URLs for private reads/writes.

## Data Privacy

- Exact coordinates live in restricted tables.
- Public map cells are derived and fuzzed.
- EXIF GPS removed from public derivatives.
- Contact data should not be stored in MVP.
- Account deletion must cascade, anonymize, or retain only legally necessary audit records.

## Migration Rules

- All schema changes use migrations.
- Migrations include rollback notes where possible.
- Data migrations include dry-run queries.
- Scoring formula changes must not silently mutate score history.

## Open Questions

- Backend framework and migration tool.
- H3 vs geohash vs custom local region cells.
- Whether comments/likes need Firestore fanout cache later.
- Retention period for originals, deleted posts, and moderation evidence.
