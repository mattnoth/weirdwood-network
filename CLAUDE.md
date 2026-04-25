# The Weirwood Network

You are the orchestrator for the Weirwood Network project — a structured knowledge graph for A Song of Ice and Fire (ASOIAF).

## First Steps — Every Session

1. Read `reference/architecture.md` for the data model: entity types, edge types, confidence tiers, file naming conventions, and spoiler gating
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
| Step | What | Status | How |
|------|------|--------|-----|
| 0 | **Scaffold** | ✅ Done | Directory structure created |
| 1 | **Chapter Splitter** | ✅ Done | `scripts/chapter-splitter.py` — splits .txt source files into per-chapter markdown with YAML frontmatter |
| 2 | **Run Splitter** | ✅ Done | All 5 books split (344 chapters) + 3 D&E novellas |
| 3 | **Wiki Scrape** | ✅ Done | `scripts/wiki-scraper.py` — 17,945 pages cached in `sources/wiki/` |
| 4 | **Pass 1: Mechanical Extraction** | In progress | v2 schema, AGOT in progress, 4 books remaining |
| 5 | **Pass 2: Wiki Ingestion** | Not started | Agent prompt not yet written — will promote wiki cache into `graph/nodes/` |
| 6 | **Build Index** | Not started | Generate trigger table and entity index from extraction outputs |
| 7 | **Pass 3+: Analytical Passes** | Not started | Voice analysis, foreshadowing, theory-informed extraction |

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

Utility agents (not part of the extraction pipeline):
- **status-reporter** — Surveys the repo and produces a detailed progress report

See `reference/agents.md` for a full description of each agent and its current status.

## Directory Structure

```
asoiaf-chat/
├── CLAUDE.md                         # THIS FILE — orchestrator guide
├── worklog.md                        # Living project history + current state
├── .claude/
│   ├── agents/                       # Subagent definitions (8 agents)
│   └── commands/                     # Custom slash commands
├── scripts/                          # Python tooling (chapter-splitter, wiki-scraper, etc.)
├── sources/
│   ├── raw/                          # Original .txt files (GITIGNORED)
│   ├── chapters/                     # Split chapter files (GITIGNORED)
│   │   ├── agot/ acok/ asos/ affc/ adwd/
│   ├── reference/                    # Non-narrative sources — TWOIAF, etc. (GITIGNORED)
│   └── wiki/                         # Scraped AWOIAF wiki cache (GITIGNORED)
│       ├── _raw/                     # 17,657 JSON files (page HTML + metadata)
│       ├── characters/ locations/ houses/ events/ artifacts/
│       └── _uncategorized/           # ~17,305 pages awaiting classification
├── extractions/
│   ├── mechanical/                   # Pass 1 outputs
│   │   ├── agot/ acok/ asos/ affc/ adwd/
│   ├── archives/                     # Archived prior-version extractions (e.g., agot-v1/)
│   ├── voice/                        # Pass 3 outputs
│   ├── foreshadowing/                # Pass 4 outputs
│   └── patterns/                     # Pass 5+ outputs
├── graph/
│   ├── nodes/                        # Entity files (one per entity)
│   │   ├── characters/ locations/ factions/ houses/
│   │   ├── artifacts/ prophecies/ theories/
│   ├── edges/
│   └── convergence-maps/
├── index/
├── curation/
├── progress/                         # Progress tracking and resumption context
│   ├── scratch-notes.md              # Observations not yet triaged
│   └── continue-prompts/             # Self-contained prompts for resuming specific work tracks
├── reference/
│   ├── agents.md                     # Agent inventory & status
│   ├── architecture.md               # Data model: entity types, edge types, confidence tiers
│   ├── foreshadowing-events.md       # 26 events + 15 Chekhov's guns
│   └── pov-characters.md             # POV lookup table + expected chapter counts
└── working/
    ├── todos.md                      # Actionable TODOs by topic
    ├── extraction-stats/             # Token/timing stats per book-pass
    ├── runbooks/                     # How-to procedures
    ├── session-details/              # Full session narratives (human-facing, not loaded by agents)
    └── worklog-archives/             # Archived older worklog sessions
```

## Key Conventions

- **Chapter file naming:** `{book}-{pov-character}-{number}.md` (e.g., `agot-bran-01.md`)
- **Node file naming:** `{entity-name-kebab-case}.node.md`
- **Every node/edge must have a `first_available` field** for spoiler gating — this is architectural, not optional
- **Confidence tiers:** Tier 1 (verified canon) through Tier 5 (crackpot) — tag everything
- **Agents propose, Matt decides** — analytical findings go to `curation/candidates.md`, not directly into the graph

## Working Directory

`working/` is the scratchpad for in-progress work:
- **`working/todos.md`** — Actionable items organized by topic: agent improvements, prompts to write, reference files to create, infrastructure tasks.
- **`working/runbooks/`** — Step-by-step procedures for operational tasks.
- **`working/extraction-stats/`** — Token usage and timing stats, one file per book-pass (e.g., `extraction-stats-agot-pass1-v2.csv`).
- **`working/session-details/`** — Full session narratives (human-facing, NOT loaded by agents). One file per session: `session-NNN.md`. Contains the complete record of what was explored, tried, rejected, and decided — for process documentation and Matt's reference.
- **Anything uncertain** — If you encounter something potentially relevant during analysis but aren't sure where it belongs, put it in `working/` rather than discarding it. Tag it clearly. Matt or a later session will triage.

`progress/` tracks extraction progress and resumption context:
- **`progress/pass1-agot.md`** — Wave-by-wave log for AGOT Pass 1. Create new files per book/pass (e.g., `pass1-acok.md`, `pass2-wiki.md`).
- **`progress/continue-prompts/`** — Self-contained prompts for resuming specific work tracks. Use `/continue` to list or run them.
- **`progress/scratch-notes.md`** — Interesting observations not yet triaged.

## Orchestration Rules

1. Never do extraction work yourself — delegate to the appropriate subagent
2. Keep your context focused on coordination, sequencing, and project state
3. Write Python scripts for any repeatable task — don't process things manually
4. Update worklog.md before ending any session — use `/endsession` for the full checklist
5. If a step fails, log the failure in worklog.md and move to the next unblocked task
6. When modifying an agent prompt's schema, update `reference/architecture.md` to match — these two must stay in sync
7. **Two-tier session documentation:**
   - **worklog.md session entries** (~20-30 lines): agent-facing, concise. What changed, what was decided, what's next. This file is loaded every session — keep it lean.
   - **working/session-details/session-NNN.md**: human-facing, full narrative. The complete exploration, reasoning, and process. Agents never load these. Matt reads them for process documentation and context recovery.
   - **Continue prompts** (`progress/continue-prompts/`): self-contained resumption context for specific work tracks. A fresh agent should be able to pick up the work from the continue prompt alone, without reading session history.
8. When the worklog exceeds ~150 lines in the Session Log, archive older sessions to `working/worklog-archives/archiveNNN.md`. The worklog keeps Current State, Active Decisions, Ideas & Backlog, Principles, and only the most recent 1-2 session entries.
