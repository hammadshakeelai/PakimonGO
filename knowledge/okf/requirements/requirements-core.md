---
id: requirements-core
type: requirements_summary
title: Core Requirements
status: draft
updated: 2026-07-01
source_docs:
  - docs/REQUIREMENTS.md
  - docs/SRS.md
related:
  - product-concept
  - system-architecture
---

# Core Requirements

## Summary

PakimonGO requires authentication, camera capture, foreground location, photo upload, AI-assisted scoring, duplicate detection, zoo/captive detection, collections, social sharing, friends, groups, map discovery, waypoint routes, and four leaderboard scopes.

## Critical Non-Functional Requirements

- Server-authoritative scoring.
- Privacy-safe public map locations.
- UGC moderation before public launch.
- Modular small-file codebase.
- Traceability from requirements to stories, tests, ADRs, and code comments.

## Launch-Critical Areas

- Auth and account deletion.
- Capture/upload reliability.
- Duplicate and zoo detection.
- UGC report/block/review.
- Location privacy.
- Score auditability.
