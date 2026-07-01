# Data Dictionary

## Purpose

This dictionary translates the ERD into table-level implementation guidance before migrations are written. It is not final SQL. Exact column names, enum names, and migration tool syntax will be locked during the backend scaffold.

## Global Conventions

| Convention | Rule |
|---|---|
| Primary keys | Use `uuid` IDs unless an external provider ID is explicitly required. |
| Time fields | Use `created_at timestamptz`, `updated_at timestamptz`, and nullable `deleted_at timestamptz` where soft-delete applies. |
| Ownership | User-owned rows include `user_id uuid` and authorization indexes. |
| Status fields | Use enums or constrained text for state machines. |
| Metadata | Use `jsonb` only for provider payloads, versioned evidence, or flexible audit metadata; core query fields stay typed. |
| Location | Use PostGIS `geography(Point,4326)` for exact capture points and derived cell IDs for public map output. |
| Vectors | Use pgvector `vector(n)` only after embedding dimension is selected. |
| Public APIs | Public DTOs must not expose restricted columns such as exact coordinates, raw EXIF, private URLs, phone/email, or moderation evidence. |

## Privacy Classes

| Class | Meaning | Examples |
|---|---|---|
| Restricted | Highest sensitivity; access is tightly role-limited and audited. | exact coordinates, original media, raw EXIF, auth IDs, phone/email, private signed URLs |
| Sensitive | Non-public operational/product data. | AI evidence, embeddings, friend graph, score explanations, moderation records |
| Controlled Public | User-visible if visibility and moderation allow it. | display name, public captions, approved derivatives |
| Aggregate Public | Coarsened or aggregated data safe for broad display. | public map cells, leaderboard rows, species summaries |
| Operational | Internal system records with no raw private data. | trace IDs, job state, provider run status, feature flags |

## Retention Classes

| Class | Default Posture |
|---|---|
| User Deletable | Delete or anonymize through account deletion flow. |
| User Controlled | User can delete/unpublish directly, subject to legal/moderation exceptions. |
| Audit Exception | Retain minimal restricted audit record for integrity/legal reasons. |
| Derived Regenerable | Can be deleted and regenerated from canonical records if still allowed. |
| Time-Limited Evidence | Retain only for defined moderation/appeal/review period. |
| Permanent Policy | Retain policy/version records for reproducibility. |

Exact retention windows are deferred by ADR-009.

## Identity And Account Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `users` | Canonical product account. | `id uuid`, `status text`, `age_band text`, `home_region text`, `trust_state text`, timestamps | unique active account; index `(status)`, `(home_region)` | Sensitive | User Deletable with audit exceptions |
| `auth_identities` | Provider identity links. | `id uuid`, `user_id uuid`, `provider text`, `provider_subject text`, `linked_at timestamptz` | unique `(provider, provider_subject)`; index `(user_id)` | Restricted | User Deletable |
| `user_profiles` | Display profile and public settings. | `user_id uuid`, `display_name text`, `avatar_asset_id uuid`, `bio text`, `public_stats_enabled boolean` | PK `user_id`; display name policy constraints | Controlled Public/Sensitive | User Controlled |
| `user_settings` | Privacy, notification, analytics, teen defaults. | `user_id uuid`, `settings jsonb`, `analytics_opt_out boolean`, `teen_defaults_applied boolean` | PK `user_id` | Sensitive | User Deletable |
| `consent_records` | Policy acceptance evidence. | `id uuid`, `user_id uuid`, `policy_version_id uuid`, `consent_type text`, `accepted_at timestamptz` | index `(user_id, accepted_at)` | Sensitive | Audit Exception |
| `account_deletion_requests` | Account deletion workflow. | `id uuid`, `user_id uuid`, `status text`, `requested_at timestamptz`, `completed_at timestamptz` | unique active request per user | Restricted | Audit Exception |
| `data_export_requests` | User data export workflow. | `id uuid`, `user_id uuid`, `status text`, `requested_at timestamptz`, `expires_at timestamptz` | index `(user_id, status)` | Restricted | Time-Limited Evidence |

## Media And Submission Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `media_assets` | Original/crop/derivative media metadata. | `id uuid`, `owner_user_id uuid`, `storage_key text`, `asset_kind text`, `processing_state text`, `sha256 text`, `byte_size bigint` | unique `(sha256, owner_user_id)` optional; index `(owner_user_id, created_at)`, `(processing_state)` | Restricted for originals; Controlled Public for approved derivatives | User Controlled / Time-Limited Evidence |
| `media_derivatives` | Thumbnail/public derivative records. | `id uuid`, `media_asset_id uuid`, `size_label text`, `storage_key text`, `exif_stripped boolean`, `visibility_state text` | unique `(media_asset_id, size_label)` | Controlled Public/Sensitive | Derived Regenerable |
| `media_processing_jobs` | Image processing job state. | `id uuid`, `media_asset_id uuid`, `job_type text`, `status text`, `attempt_count int`, `last_error text` | index `(status, created_at)` | Operational | Derived Regenerable |
| `submissions` | User capture submitted for scoring. | `id uuid`, `user_id uuid`, `primary_media_asset_id uuid`, `status text`, `visibility text`, `submitted_at timestamptz` | index `(user_id, submitted_at)`, `(status)` | Sensitive | User Controlled with audit exceptions |
| `submission_attributes` | User-entered capture context. | `submission_id uuid`, `animal_context text`, `real_name text`, `cute_name text`, `caption text`, `tags text[]` | PK `submission_id`; text length constraints | Sensitive/Controlled Public | User Controlled |
| `observations` | One or more animal observations in a submission. | `id uuid`, `submission_id uuid`, `role text`, `wild_eligibility text`, `taxon_id uuid`, `confidence numeric` | index `(submission_id)`, `(taxon_id)` | Sensitive | User Controlled |
| `encounter_groups` | Groups same encounter/photo replacement events. | `id uuid`, `user_id uuid`, `representative_submission_id uuid`, `group_reason text` | index `(user_id, created_at)` | Sensitive | User Controlled |

## Evidence And AI Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `image_hashes` | Exact and perceptual hash records. | `id uuid`, `media_asset_id uuid`, `hash_type text`, `hash_value text`, `algorithm_version text` | index `(hash_type, hash_value)` | Sensitive | Derived Regenerable |
| `image_embeddings` | Image/crop vector embeddings. | `id uuid`, `media_asset_id uuid`, `embedding vector(n)`, `model_version text`, `scope text` | vector index after benchmark; index `(media_asset_id)` | Sensitive | Derived Regenerable / Time-Limited if deletion |
| `animal_crops` | Detected animal crop metadata. | `id uuid`, `media_asset_id uuid`, `bbox jsonb`, `confidence numeric`, `crop_asset_id uuid` | index `(media_asset_id)` | Sensitive | Derived Regenerable |
| `ai_runs` | AI provider run envelope. | `id uuid`, `submission_id uuid`, `provider text`, `model text`, `prompt_version text`, `status text`, `cost_estimate numeric` | index `(submission_id)`, `(provider, model)` | Sensitive | Time-Limited Evidence |
| `ai_run_outputs` | Structured AI output. | `id uuid`, `ai_run_id uuid`, `schema_version text`, `output jsonb`, `confidence numeric` | index `(ai_run_id)` | Sensitive | Time-Limited Evidence |
| `identifications` | Taxon identification candidates. | `id uuid`, `observation_id uuid`, `source text`, `taxon_id uuid`, `confidence numeric`, `accepted boolean` | index `(observation_id)`, `(taxon_id)` | Sensitive | User Controlled / Derived Regenerable |
| `duplicate_edges` | Exact/near/semantic duplicate relationships. | `id uuid`, `source_submission_id uuid`, `target_submission_id uuid`, `match_type text`, `confidence numeric`, `threshold_version text` | unique edge pair per type; index `(source_submission_id)`, `(target_submission_id)` | Sensitive | Audit Exception for score integrity |

## Animal Knowledge Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `taxa` | Canonical animal taxon records. | `id uuid`, `external_source text`, `external_id text`, `rank text`, `accepted_name text`, `status text` | unique `(external_source, external_id)`; index `(accepted_name)` | Operational/Public taxonomy | Permanent Policy |
| `taxon_aliases` | Common names, synonyms, local names. | `id uuid`, `taxon_id uuid`, `name text`, `locale text`, `alias_type text` | index `(taxon_id)`, `(locale, name)` | Operational/Public taxonomy | Permanent Policy |
| `taxon_regions` | Regional establishment and rarity. | `id uuid`, `taxon_id uuid`, `region_code text`, `establishment_means text`, `rarity_band text` | unique `(taxon_id, region_code)` | Operational | Permanent Policy |
| `taxonomy_imports` | Import/version metadata. | `id uuid`, `source text`, `version text`, `imported_at timestamptz`, `status text` | unique `(source, version)` | Operational | Permanent Policy |
| `sensitive_taxon_rules` | Suppression/coarsening policy. | `id uuid`, `taxon_id uuid`, `region_code text`, `rule_level text`, `policy_version_id uuid` | index `(taxon_id, region_code)` | Sensitive policy | Permanent Policy |
| `rarity_snapshots` | Rarity source snapshots. | `id uuid`, `taxon_id uuid`, `region_code text`, `rarity_score numeric`, `source_version text` | index `(taxon_id, region_code)` | Operational | Permanent Policy |

## Geo Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `capture_locations` | Restricted exact location evidence. | `submission_id uuid`, `point geography(Point,4326)`, `accuracy_meters numeric`, `source text`, `captured_at timestamptz` | GiST `(point)`; PK `submission_id` | Restricted | User Deletable / Audit Exception if needed |
| `public_location_cells` | Derived public map/rank cells. | `id uuid`, `submission_id uuid`, `cell_id text`, `precision_label text`, `available_after timestamptz`, `suppressed_reason text` | index `(cell_id, available_after)`, `(submission_id)` | Aggregate Public/Sensitive | Derived Regenerable |
| `geofences` | Zoo/captive/sensitive/policy polygons. | `id uuid`, `source_id uuid`, `geofence_type text`, `geometry geometry(MultiPolygon,4326)`, `confidence numeric` | GiST `(geometry)`; index `(geofence_type)` | Operational/Sensitive policy | Permanent Policy |
| `geofence_sources` | Source/version metadata. | `id uuid`, `source_name text`, `source_version text`, `license text`, `imported_at timestamptz` | unique `(source_name, source_version)` | Operational | Permanent Policy |
| `local_regions` | Privacy-safe local leaderboard regions. | `id uuid`, `region_type text`, `cell_id text`, `min_users int`, `enabled boolean` | index `(region_type, cell_id)` | Aggregate Public | Permanent Policy |
| `map_activity_snapshots` | Precomputed map activity summaries. | `id uuid`, `cell_id text`, `window_start timestamptz`, `window_end timestamptz`, `summary jsonb` | index `(cell_id, window_end)` | Aggregate Public | Derived Regenerable |

## Scoring And Leaderboard Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `score_formula_versions` | Versioned score rules. | `id uuid`, `version text`, `status text`, `config jsonb`, `activated_at timestamptz` | unique `(version)` | Permanent Policy | Permanent Policy |
| `score_events` | Immutable score ledger entries. | `id uuid`, `submission_id uuid`, `user_id uuid`, `ledger text`, `points int`, `event_type text`, `formula_version_id uuid`, `explanation jsonb` | append-only; index `(user_id, created_at)`, `(submission_id)`, `(ledger)` | Sensitive | Audit Exception |
| `score_totals` | Current denormalized user totals. | `user_id uuid`, `ledger text`, `total_points int`, `updated_at timestamptz` | unique `(user_id, ledger)` | Sensitive/Aggregate Public when visible | Derived Regenerable |
| `leaderboard_entries` | Projected leaderboard rows. | `id uuid`, `scope text`, `period text`, `region_key text`, `user_id uuid`, `rank int`, `score int` | index `(scope, period, region_key, rank)` | Aggregate Public/Sensitive | Derived Regenerable |
| `leaderboard_snapshots` | Snapshot metadata for ranks. | `id uuid`, `scope text`, `period text`, `region_key text`, `snapshot_at timestamptz`, `status text` | index `(scope, period, snapshot_at)` | Operational | Derived Regenerable |
| `trust_events` | Abuse/trust changes. | `id uuid`, `user_id uuid`, `event_type text`, `delta numeric`, `source text`, `reason text` | index `(user_id, created_at)` | Sensitive | Audit Exception |

## Social Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `posts` | Social wrapper around submissions. | `id uuid`, `submission_id uuid`, `author_user_id uuid`, `visibility text`, `moderation_state text` | unique `(submission_id)`; index `(author_user_id, created_at)`, `(visibility, moderation_state)` | Controlled Public/Sensitive | User Controlled |
| `post_visibility_rules` | Selected-friend/group visibility. | `id uuid`, `post_id uuid`, `rule_type text`, `target_id uuid` | index `(post_id)`, `(target_id)` | Sensitive | User Controlled |
| `comments` | Post comments. | `id uuid`, `post_id uuid`, `author_user_id uuid`, `body text`, `moderation_state text` | index `(post_id, created_at)` | Controlled Public/Sensitive | User Controlled |
| `likes` | Like reactions. | `id uuid`, `post_id uuid`, `user_id uuid`, `created_at timestamptz` | unique `(post_id, user_id)` | Sensitive/Aggregate Public | User Controlled |
| `reposts` | Repost/share records. | `id uuid`, `post_id uuid`, `user_id uuid`, `visibility text` | index `(post_id)`, `(user_id)` | Controlled Public/Sensitive | User Controlled |
| `hashtags` | Normalized hashtags. | `id uuid`, `tag text`, `status text` | unique `(tag)` | Controlled Public | User Controlled / Policy |
| `post_hashtags` | Post-to-hashtag join. | `post_id uuid`, `hashtag_id uuid` | PK `(post_id, hashtag_id)` | Controlled Public | User Controlled |
| `friendships` | Friend graph. | `id uuid`, `requester_id uuid`, `addressee_id uuid`, `status text`, `accepted_at timestamptz` | unique user pair; index both directions | Sensitive | User Controlled |
| `groups` | Group records. | `id uuid`, `owner_user_id uuid`, `name text`, `visibility text`, `moderation_state text` | index `(owner_user_id)` | Controlled Public/Sensitive | User Controlled |
| `group_memberships` | Group membership and roles. | `group_id uuid`, `user_id uuid`, `role text`, `status text` | PK `(group_id, user_id)` | Sensitive | User Controlled |
| `blocks` | User block relationships. | `id uuid`, `blocker_user_id uuid`, `blocked_user_id uuid`, `created_at timestamptz` | unique `(blocker_user_id, blocked_user_id)` | Sensitive | User Controlled |

## Moderation And Operations Tables

| Table | Purpose | Key Fields | Constraints And Indexes | Privacy | Retention |
|---|---|---|---|---|---|
| `reports` | User reports. | `id uuid`, `reporter_user_id uuid`, `target_type text`, `target_id uuid`, `category text`, `notes text` | index `(target_type, target_id)`, `(reporter_user_id)` | Sensitive | Time-Limited Evidence / Audit Exception |
| `moderation_cases` | Review queue case. | `id uuid`, `case_type text`, `priority text`, `status text`, `assigned_to uuid`, `opened_at timestamptz` | index `(status, priority, opened_at)` | Restricted/Sensitive | Time-Limited Evidence / Audit Exception |
| `moderation_actions` | Actions on cases/content/scores. | `id uuid`, `case_id uuid`, `actor_user_id uuid`, `action_type text`, `reason text`, `created_at timestamptz` | index `(case_id)`, `(actor_user_id)` | Restricted | Audit Exception |
| `appeals` | User appeals. | `id uuid`, `user_id uuid`, `target_type text`, `target_id uuid`, `status text`, `outcome text` | index `(user_id, created_at)`, `(status)` | Sensitive | Time-Limited Evidence / Audit Exception |
| `policy_versions` | Terms/privacy/community/scoring policies. | `id uuid`, `policy_type text`, `version text`, `status text`, `effective_at timestamptz` | unique `(policy_type, version)` | Permanent Policy | Permanent Policy |
| `evidence_access_grants` | Purpose-bound moderator evidence access. | `id uuid`, `case_id uuid`, `user_id uuid`, `scope text`, `expires_at timestamptz` | index `(case_id)`, `(user_id, expires_at)` | Restricted | Audit Exception |
| `audit_logs` | Append-only system audit trail. | `id uuid`, `actor_user_id uuid`, `action text`, `target_type text`, `target_id uuid`, `metadata jsonb`, `created_at timestamptz` | append-only; index `(actor_user_id, created_at)`, `(target_type, target_id)` | Restricted/Operational | Audit Exception |
| `outbox_events` | Reliable async event outbox. | `id uuid`, `event_type text`, `aggregate_type text`, `aggregate_id uuid`, `payload jsonb`, `status text` | index `(status, created_at)`, `(aggregate_type, aggregate_id)` | Operational/Sensitive payload dependent | Derived Regenerable / Audit Exception |
| `idempotency_keys` | Mutation idempotency store. | `key text`, `user_id uuid`, `operation text`, `request_hash text`, `response_ref text`, `expires_at timestamptz` | PK `(key, user_id, operation)` | Sensitive | Time-Limited Evidence |
| `feature_flags` | Feature and incident switches. | `key text`, `enabled boolean`, `scope jsonb`, `updated_by uuid`, `updated_at timestamptz` | PK `key` | Operational | Permanent Policy / Audit |
| `region_configs` | Region feature/legal config. | `region_code text`, `config jsonb`, `status text`, `effective_at timestamptz` | PK `region_code` | Operational | Permanent Policy |
| `provider_runs` | External provider call tracking. | `id uuid`, `provider text`, `operation text`, `status text`, `latency_ms int`, `cost_estimate numeric` | index `(provider, operation, created_at)` | Operational/Sensitive if linked | Time-Limited Evidence |

## First Migration Slice

The first migration should be limited to WP-015 needs:

1. `users`, `auth_identities`, `user_profiles`, `user_settings`, `consent_records`.
2. `media_assets`, `media_derivatives`, `submissions`, `submission_attributes`, `observations`.
3. `capture_locations`, `public_location_cells`.
4. `score_formula_versions`, `score_events`.
5. `image_hashes`, `duplicate_edges`.
6. `geofences`, `geofence_sources`.
7. `audit_logs`, `outbox_events`, `idempotency_keys`, `feature_flags`.

## Open Data Decisions

- Exact enum names and migration tool.
- Embedding dimension and vector index type.
- H3 vs geohash vs custom cell IDs.
- Exact retention windows from ADR-009.
- Whether social fanout cache appears before beta.
- Whether AI evidence outputs are encrypted field-level or table-level restricted.
