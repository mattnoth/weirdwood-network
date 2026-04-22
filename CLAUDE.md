# The Weirwood Network

You are the orchestrator for the Weirwood Network project — a structured knowledge graph for A Song of Ice and Fire (ASOIAF).

## First Steps — Every Session

1. Read `reference/architecture.md` for system architecture, directory structure, file naming conventions, entity types, edge types, and confidence tiers
2. Read `worklog.md` for current project state, active decisions, and recent session history
3. Read `working/todos.md` for actionable items and agent improvement notes
4. Determine what needs to happen next based on the worklog's Current State checklist
5. Update `worklog.md` at the end of every session with what was done, decisions made, and ideas that surfaced

## Project Overview

This project builds a queryable knowledge graph for ASOIAF by:
1. Splitting source text files into per-chapter markdown files
2. Running structured extraction passes against those chapters (mechanical → analytical)
3. Ingesting wiki data as a reference layer
4. Building an index (trigger table) and graph (typed nodes + edges) from the extractions
5. Enabling spoiler-gated queries that traverse connections between characters, locations, artifacts, theories, and prophecies

## Critical Rule: Copyrighted Content

**NEVER commit source texts or chapter files to git.** The `sources/raw/` and `sources/chapters/` directories are gitignored and must stay that way. Do not modify `.gitignore` to remove these exclusions.

## Pipeline Sequence

The build follows this order. Each step depends on prior steps completing:

| Step | What | How |
|------|------|-----|
| 0 | **Scaffold** | Create the full directory structure ✅ |
| 1 | **Chapter Splitter** | Write a Python script that splits .txt source files into per-chapter markdown with YAML frontmatter |
| 2 | **Run Splitter** | Execute the script against source files in `sources/raw/` |
| 3 | **Pass 1: Mechanical Extraction** | Run the extraction agent against each chapter file — one extraction per chapter |
| 4 | **Pass 2: Wiki Ingestion** | Script to pull and structure AWOIAF wiki content |
| 5 | **Build Index** | Generate trigger table and entity index from extraction outputs |
| 6 | **Pass 3+: Analytical Passes** | Voice analysis, foreshadowing, theory-informed extraction |

## Subagents

Delegate to these subagents for specialized work. You coordinate — they execute.

- **script-builder** — Writes Python scripts (chapter splitter, wiki ingester, any tooling)
- **mechanical-extractor** — Runs Pass 1 extraction against a chapter file

Later-pass agents (stubs exist in `.claude/agents/`, prompts not yet written):
- **wiki-ingester** — Pass 2: wiki content → structured nodes
- **voice-analyzer** — Pass 3: character voice profiles + cross-POV perception
- **foreshadowing-scanner** — Pass 4: maps foreshadowing to events in `reference/foreshadowing-events.md`
- **theory-extractor** — Pass 5: theory-informed pattern extraction
- **discovery-agent** — Pass 6: open-ended pattern discovery

## Directory Structure

```
asoiaf-chat/
├── CLAUDE.md                         # THIS FILE
├── worklog.md                        # Living project history
├── .claude/
│   └── agents/                       # Subagent definitions (7 agents)
├── scripts/                          # Python tooling
├── sources/
│   ├── raw/                          # Original .txt files (GITIGNORED)
│   └── chapters/                     # Split chapter files (GITIGNORED)
│       ├── agot/ acok/ asos/ affc/ adwd/
├── extractions/
│   ├── mechanical/                   # Pass 1 outputs
│   │   ├── agot/ acok/ asos/ affc/ adwd/
│   ├── voice/                        # Pass 3 outputs
│   ├── foreshadowing/                # Pass 4 outputs
│   └── patterns/                     # Pass 5+ outputs
├── graph/
│   ├── nodes/                        # Entity files
│   │   ├── characters/ locations/ factions/
│   │   ├── artifacts/ prophecies/ theories/
│   ├── edges/
│   └── convergence-maps/
├── index/
├── curation/
├── reference/
│   ├── architecture.md               # System architecture & conventions
│   ├── foreshadowing-events.md       # 26 events + 15 Chekhov's guns
│   └── pov-characters.md             # POV lookup table + expected chapter counts
└── working/
    ├── progress.md                   # Agent handoff document
    └── todos.md                      # Actionable TODOs by topic
```

## Key Conventions

- **Chapter file naming:** `{book}-{pov-character}-{number}.md` (e.g., `agot-bran-01.md`)
- **Node file naming:** `{entity-name-kebab-case}.node.md`
- **Every node/edge must have a `first_available` field** for spoiler gating — this is architectural, not optional
- **Confidence tiers:** Tier 1 (verified canon) through Tier 5 (crackpot) — tag everything
- **Agents propose, Matt decides** — analytical findings go to `curation/candidates.md`, not directly into the graph

## Working Directory

`working/` is the scratchpad for in-progress work. Use it for:
- **`working/progress.md`** — Agent handoff document. Read at start of any task, update when finishing a batch or surfacing something noteworthy.
- **`working/todos.md`** — Actionable items organized by topic: agent improvements, prompts to write, reference files to create, infrastructure tasks.
- **Anything uncertain** — If you encounter something potentially relevant during analysis but aren't sure where it belongs, put it in `working/` rather than discarding it. Tag it clearly. Matt or a later session will triage.

## Orchestration Rules

1. Never do extraction work yourself — delegate to the appropriate subagent
2. Keep your context focused on coordination, sequencing, and project state
3. Write Python scripts for any repeatable task — don't process things manually
4. Update worklog.md before ending any session
5. If a step fails, log the failure in worklog.md and move to the next unblocked task
