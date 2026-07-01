# Next Task

## Current Next Task

Sprint 15 — Collection/leaderboard endpoints or database-backed user scoring history.

## Sprint 14 Complete

Sprint 14 delivered: **Real Google Vision Provider implementation**.

- Replaced placeholder with actual REST API calls to `vision.googleapis.com/v1/images:annotate`
- Parses label annotations + localized object annotations → detects species, confidence, context
- Context classification: zoo keywords → "zoo", pet keywords → "pet", else "wild" (or "unknown" if no labels)
- Mock-tested 6 scenarios: zoo, wild, pet, empty response, error/HTTP error, file-not-found
- 49 scoring-rules tests + 54 API tests = 103 Python + 14 Flutter = **117 total tests, all passing**

Next sprint candidates:
- **Collection/leaderboard endpoints** — API endpoints for user collections and leaderboard data
- **Real data (zoo flag, golden set)** — integrate goldset fixtures for precheck/duplicate testing
