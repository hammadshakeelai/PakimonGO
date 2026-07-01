# Knowledge System

## Purpose

The project must survive long timelines, context-window limits, and handoff between many AI agents. The knowledge system turns scattered decisions into durable, searchable project memory.

## Layers

### Human Docs

`docs/` contains readable planning and governance:

- Product prompt
- Discovery
- Requirements
- SRS
- Architecture
- Process
- ADRs
- Backlog
- Bugs and risks
- Technical debt
- Release checklists

### OKF-Style Knowledge

`knowledge/okf/` contains structured, machine-readable Markdown/YAML-style summaries. Use one concept per file. These files should be short and explicit so future agents can ingest them quickly.

Use OKF entries for:

- Product concepts
- Requirement summaries
- Architecture entities
- Data models
- Relationships between modules
- Decision records
- Risk and debt summaries

Recommended areas:

- `knowledge/okf/product/`
- `knowledge/okf/requirements/`
- `knowledge/okf/architecture/`
- `knowledge/okf/decisions/`
- `knowledge/okf/risks/`
- `knowledge/okf/domain/`
- `knowledge/okf/ai-scoring/`
- `knowledge/okf/privacy/`
- `knowledge/okf/tasks/`

### Obsidian

Treat the repo as an Obsidian-compatible vault:

- Use Markdown files.
- Use stable headings.
- Use links like `[[Requirements]]` where helpful.
- Maintain an index file.
- Keep decision and requirement IDs searchable.
- Use canvas later for maps of domains, services, and flows if useful.

Obsidian is for thinking, browsing, and human navigation; the repo remains the source of truth.

Current vault home:

- `docs/OBSIDIAN_VAULT_INDEX.md`

Current canonical Mermaid diagram pack:

- `docs/diagrams/README.md`

### Graphify

Use Graphify or equivalent code-graph tooling after code exists. Store generated outputs under `knowledge/graph/graphify-out/`.

Planned uses:

- Generate code relationship graphs.
- Connect modules to requirement IDs.
- Detect large or overly connected files.
- Help future AI agents understand call paths before edits.
- Support impact analysis before large changes.
- Produce a quick-read `GRAPH_REPORT.md` and deeper `graph.json`.

Graphify should read code and docs; it should not become the only source of truth.

Current Graphify plan:

- `tools/graphify/GRAPHIFY_PLAN.md`

Current OKF export plan:

- `tools/okf-export/OKF_EXPORT_PLAN.md`

## Required State Files

Every agent should inspect these first:

1. `docs/CURRENT_TASK.md`
2. `docs/NEXT_TASK.md`
3. `docs/CURRENT_THINKING.md`
4. `docs/REQUIREMENTS.md`
5. `docs/PROCESS.md`

Every task should update relevant state files before completion.

## Token-Safe Handoff Pattern

When context is limited, read in this order:

1. `docs/NEXT_TASK.md`
2. `docs/CURRENT_TASK.md`
3. `docs/CURRENT_THINKING.md`
4. Relevant module README.
5. Relevant requirement IDs.
6. Relevant ADRs.
7. Only then source files.

This prevents agents from rereading the whole repo.

## Knowledge Entry Template

```md
---
id:
type:
status:
updated:
source_docs:
related_requirements:
related_adrs:
---

# Title

## Summary

## Relationships

## Open Questions

## Handoff Notes
```

## Update Rules

- Update OKF files when requirements, architecture, or process changes.
- Update Obsidian links when files are renamed.
- Regenerate Graphify/code graphs after large refactors.
- Keep generated graph files separate from source code.
- If a doc and OKF entry disagree, fix both and record the correction in `CURRENT_THINKING.md`.
