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

## Critical Rule: The Wiki Is Already Local — Never Re-Fetch (with one narrow exception)

**The entire AWOIAF wiki (17,945 pages, 377 MB) is cached locally at `sources/wiki/_raw/`.** Every Pass 2+ workflow reads from this cache. There is no re-fetching of page bodies. No `WebFetch`, no full re-crawls, no resurrection of the archived Playwright scraper.

**Narrow exception — completion-of-original-crawl operations.** A single bounded fetch is permitted ONLY to fill specific metadata gaps the original crawl missed (e.g., MediaWiki categories, which the `action=parse` API stripped from the HTML footer). Each exception requires explicit per-use approval, must target one specific data field, must NOT write to `sources/`, and must hit the MediaWiki API endpoint via a lightweight client (`cloudscraper` for Cloudflare bypass — verified 2026-04-30). The Playwright-based scraper at `scripts/archive/wiki-scraper.py.archive` remains archived and should NOT be restored — exception fetches use the lighter `cloudscraper` path. New exception-fetch scripts are short, single-purpose, throttled, and write to `working/wiki-parsed/`.

If you think you need to fetch a page's body content, you don't — read it from `sources/wiki/_raw/<Page_Name>.json` instead.

**Approved exception fetches (audit log):**
- `2026-04-30` — MediaWiki categories backfill (`scripts/wiki-fetch-categories.py` → `working/wiki-parsed/page-categories.jsonl`). Reason: original crawl used `action=parse` which strips catlinks footer; the entity categorizer in the archived scraper depended on category data and never ran for `characters/`, `locations/`, `events/`, `artifacts/` (~17k pages misclassified as `unknown`).

**Never drop anything from `sources/`.** Stub pages, redirect pages, list articles, year articles, disambiguation pages — all stay. Tier them, label them, defer them, but never delete them. Source data is read-only and additive-only. **Exception fetches must NOT write to `sources/`** — outputs land in `working/wiki-parsed/` or `graph/`.

## Pipeline Sequence

The build follows this order. Each step depends on prior steps completing:

| Step | What | How |
|------|------|-----|
| Step | What | Status | How |
|------|------|--------|-----|
| 0 | **Scaffold** | ✅ Done | Directory structure created |
| 1 | **Chapter Splitter** | ✅ Done | `scripts/chapter-splitter.py` — splits .txt source files into per-chapter markdown with YAML frontmatter |
| 2 | **Run Splitter** | ✅ Done | All 5 books split (344 chapters) + 3 D&E novellas |
| 3 | **Wiki Scrape** | ✅ Done | 17,945 pages cached locally in `sources/wiki/` (one-time crawl, scraper archived to `scripts/archive/`). All Pass 2+ work reads local cache only — never re-fetch. |
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
├── scripts/                          # Python tooling (chapter-splitter, wiki-pass2 pipeline, etc.)
│   └── archive/                      # Retired scripts (Playwright wiki-scraper) — DO NOT restore
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
│   └── continue-prompts/             # Self-contained prompts for resuming specific work tracks
├── reference/
│   ├── agents.md                     # Agent inventory & status
│   ├── architecture.md               # Data model: entity types, edge types, confidence tiers
│   ├── foreshadowing-events.md       # 26 events + 15 Chekhov's guns
│   └── pov-characters.md             # POV lookup table + expected chapter counts
├── working/                          # Active scratchpad — live work-in-progress only
│   ├── todos.md                      # Actionable TODOs by topic
│   ├── agent-fleet-specs/            # Agent + fleet roadmap (operating manual; reads todos.md)
│   ├── audits/                       # Per-audit folders (each: prompt/, execution/, validation/)
│   ├── extraction-stats/             # Token/timing stats per book-pass
│   ├── runbooks/                     # How-to procedures
│   ├── wiki-parsed/                  # Derived parse outputs (alias-resolver, infobox-data, etc.)
│   └── wiki-pass2/                   # Per-bucket Pass 2 promotion outputs
└── history/                          # Frozen records of past work — not active state
    ├── session-details/              # Full session narratives (human-facing, not loaded by agents)
    ├── worklog-archives/             # Archived older worklog sessions
    └── archive/                      # Retired sketches, design reviews
```

## Key Conventions

- **Chapter file naming:** `{book}-{pov-character}-{number}.md` (e.g., `agot-bran-01.md`)
- **Node file naming:** `{entity-name-kebab-case}.node.md`
- **`first_available` (spoiler gating) is DEFERRED to post-first-release.** Field is optional in v1 nodes; existing values may be wrong (parser bug class — see architecture.md). Do not invest context reasoning out individual values; backfill happens via deterministic script later.
- **Confidence tiers:** Tier 1 (verified canon) through Tier 5 (crackpot) — tag everything
- **Agents propose, Matt decides** — analytical findings go to `curation/candidates.md`, not directly into the graph

## Working Directory

`working/` is the scratchpad for active in-progress work. Frozen historical records (session details, worklog archives, retired sketches) live under top-level `history/`, not here.

- **`working/todos.md`** — Actionable items organized by topic: agent improvements, prompts to write, reference files to create, infrastructure tasks.
- **`working/agent-fleet-specs/`** — Agent + fleet operating manual (`agent-pipeline-plan.md`, `fleet-orchestration-plan.md`, `fleet-runtime-architecture.md`). The fleet was designed to tackle `working/todos.md` automatically.
- **`working/audits/`** — Per-audit folders. Each has its own subfolder with `prompt/`, `execution/`, `validation/`, etc.
- **`working/runbooks/`** — Step-by-step procedures for operational tasks.
- **`working/extraction-stats/`** — Token usage and timing stats, one file per book-pass (e.g., `extraction-stats-agot-pass1-v2.csv`).
- **`history/session-details/`** — Full session narratives (human-facing, NOT loaded by agents). One file per session: `session-NNN.md`. Contains the complete record of what was explored, tried, rejected, and decided — for process documentation and Matt's reference.
- **`history/worklog-archives/`** — Older worklog session entries, archived in 5-entry blocks per CLAUDE.md rule #8.
- **`history/archive/`** — Retired sketches and design reviews preserved with stale-tag preambles.
- **Anything uncertain** — If you encounter something potentially relevant during analysis but aren't sure where it belongs, put it in `working/` rather than discarding it. Tag it clearly. Matt or a later session will triage.

`progress/` tracks extraction progress and resumption context:
- **`progress/pass1-agot.md`** — Wave-by-wave log for AGOT Pass 1. Create new files per book/pass (e.g., `pass1-acok.md`, `pass2-wiki.md`).
- **`progress/continue-prompts/`** — Self-contained prompts for resuming specific work tracks. Use `/continue` to list or run them.

## Top-Level `scratch` File — Ignore It

A file named `scratch` (or `scratch.md` / `scratch.txt`) at the repo root is **Matt's private notes**, not project state. It is gitignored. **Do not read it, surface it, or act on its contents during normal sessions.** The single exception is `/endsession` step 4(a), which is the designated triage moment — that step reads scratch and prompts Matt where each entry should land. Outside `/endsession`, treat scratch as if it doesn't exist.

## Orchestration Rules

1. Never do extraction work yourself — delegate to the appropriate subagent
2. Keep your context focused on coordination, sequencing, and project state
3. Write Python scripts for any repeatable task — don't process things manually
4. Update worklog.md before ending any session — use `/endsession` for the full checklist
5. If a step fails, log the failure in worklog.md and move to the next unblocked task
6. When modifying an agent prompt's schema, update `reference/architecture.md` to match — these two must stay in sync
7. **Session documentation:**
   - **worklog.md session entries** (~20-30 lines): agent-facing, concise. What changed, what was decided, what's next. This file is loaded every session — keep it lean.
   - **history/session-details/session-NNN.md**: optional, *as-needed*. Write one when the session contains design discussion, an incident worth a postmortem, or novel decisions worth a long-form narrative. Pure-execution sessions don't need one — the worklog entry is sufficient. Existing detail files are inconsistently applied (the prior rule was "every session"); audit/backfill is an auxiliary project-story todo, not blocking.
   - **Continue prompts** (`progress/continue-prompts/`): self-contained resumption context for specific work tracks. A fresh agent should be able to pick up the work from the continue prompt alone, without reading session history.
8. **Worklog Session Log holds at most 5 entries.** When a 6th session lands, archive the oldest to `history/worklog-archives/archiveNNN.md`. Each archive file holds exactly 5 entries (start a new `archiveNNN.md` when the current one is full). The worklog itself keeps Current State, Active Decisions, Ideas & Backlog, Principles, and the 5 most recent session entries.
