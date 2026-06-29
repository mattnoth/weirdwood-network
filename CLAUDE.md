# The Weirwood Network

You are the orchestrator for the Weirwood Network project — a structured knowledge graph for A Song of Ice and Fire (ASOIAF).

## First Steps — Every Session

1. Read `reference/architecture.md` for the data model: entity types, edge types, confidence tiers, file naming conventions, and spoiler gating
2. Read `worklog.md` for current project state, active decisions, and recent session history. **Track-aware:** if you are working the **D&E Pass-1 track**, read **`worklog-dunk-egg.md`** instead (its own Current State + Session Log) — you may SKIP the giant graph Current State — and skim only the `worklog.md` STATUS cross-track block for awareness. `worklog.md` always holds the **shared** state (Active Decisions, Ideas & Backlog, Principles) for **every** track.
3. Read `working/todos.md` for actionable items and agent improvement notes
4. Determine what needs to happen next based on the Current State checklist (in `worklog.md`, or `worklog-dunk-egg.md` for the D&E track)
5. Update **your track's worklog** at the end of every session — `worklog.md` for graph/meta sessions, `worklog-dunk-egg.md` for D&E Pass-1 (numbered DE-N) — with what was done, decisions made, and ideas that surfaced. Shared/project-wide decisions always go to `worklog.md` Active Decisions regardless of track.

## Project Overview

This project builds a queryable knowledge graph for ASOIAF by:
1. Splitting source text files into per-chapter markdown files
2. Running structured extraction passes against those chapters (mechanical → analytical)
3. Ingesting wiki data as a reference layer
4. Building an index (trigger table) and graph (typed nodes + edges) from the extractions
5. Enabling spoiler-gated queries that traverse connections between characters, locations, artifacts, theories, and prophecies

## Critical Rule: The Wiki Is Already Local — Never Re-Fetch (with one narrow exception)

**The entire AWOIAF wiki (17,945 pages fetched → 17,657 unique JSON files on disk; the delta is case-collision/redirect overwrites; 377 MB) is cached locally at `sources/wiki/_raw/`.** Every Pass 2+ workflow reads from this cache. There is no re-fetching of page bodies. No `WebFetch`, no full re-crawls, no resurrection of the archived Playwright scraper.

**Narrow exception — completion-of-original-crawl operations.** A single bounded fetch is permitted ONLY to fill specific metadata gaps the original crawl missed (e.g., MediaWiki categories, which the `action=parse` API stripped from the HTML footer). Each exception requires explicit per-use approval, must target one specific data field, must NOT write to `sources/`, and must hit the MediaWiki API endpoint via a lightweight client (`cloudscraper` for Cloudflare bypass — verified 2026-04-30). The Playwright-based scraper at `scripts/archive/wiki-scraper.py.archive` remains archived and should NOT be restored — exception fetches use the lighter `cloudscraper` path. New exception-fetch scripts are short, single-purpose, throttled, and write to `working/wiki/data/`.

If you think you need to fetch a page's body content, you don't — read it from `sources/wiki/_raw/<Page_Name>.json` instead.

**Approved exception fetches (audit log):**
- `2026-04-30` — MediaWiki categories backfill (`scripts/wiki-fetch-categories.py` → `working/wiki/data/page-categories.jsonl`). Reason: original crawl used `action=parse` which strips catlinks footer; the entity categorizer in the archived scraper depended on category data and never ran for `characters/`, `locations/`, `events/`, `artifacts/` (~17k pages misclassified as `unknown`).

**Never drop anything from `sources/`.** Stub pages, redirect pages, list articles, year articles, disambiguation pages — all stay. Tier them, label them, defer them, but never delete them. Source data is read-only and additive-only. **Exception fetches must NOT write to `sources/`** — outputs land in `working/wiki/data/` or `graph/`.

## Pipeline Sequence

The build follows this order. Each step depends on prior steps completing:

| Step | What | Status | How |
|------|------|--------|-----|
| 0 | **Scaffold** | ✅ Done | Directory structure created |
| 1 | **Chapter Splitter** | ✅ Done | `scripts/chapter-splitter.py` — splits .txt source files into per-chapter markdown with YAML frontmatter |
| 2 | **Run Splitter** | ✅ Done | All 5 books split (344 chapters) + 3 D&E novellas |
| 3 | **Wiki Scrape** | ✅ Done | 17,945 pages fetched, cached locally in `sources/wiki/` as 17,657 unique JSON files (case-collision/redirect overwrites account for the delta). One-time crawl, scraper archived to `scripts/archive/`. All Pass 2+ work reads local cache only — never re-fetch. |
| 4 | **Pass 1: Mechanical Extraction** | ✅ Done | v3 schema, all 5 books complete (344/344 as of 2026-05-06) |
| 5 | **Pass 2: Wiki Ingestion** | ✅ Done | Ran 2026-04-26 → 05-01 (855 agent-promoted nodes Stage 1 + ~7,000 Python promotions Stages 3/3c/Path B). `graph/nodes/` ≈ 8,261 nodes. Pipeline: `working/runbooks/wiki-pass2-pipeline.md` |
| 6 | **Build Index** | ✅ Done | Entity + chapter indexes built S38–S44, extended to all 21 categories S72 (`scripts/build-entity-indexes.py` → `graph/index/`). Trigger table still open |
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
├── worklog.md                        # Living project history + current state (GRAPH track + shared state; global S-numbers)
├── worklog-dunk-egg.md               # D&E Pass-1 track's OWN worklog (DE-N numbering; does NOT archive to history/)
├── .claude/
│   ├── agents/                       # Subagent definitions (28 agents as of 2026-06-11)
│   └── commands/                     # Custom slash commands
├── scripts/                          # Python tooling (chapter-splitter, wiki-pass2 pipeline, etc.)
│   └── archive/                      # Retired scripts (Playwright wiki-scraper) — DO NOT restore
├── sources/
│   ├── raw/                          # Original .txt files (GITIGNORED)
│   ├── chapters/                     # Split chapter files (git-TRACKED — 347 files; the chat-UI bundles these)
│   │   ├── agot/ acok/ asos/ affc/ adwd/
│   ├── reference/                    # Non-narrative sources — TWOIAF, etc. (GITIGNORED)
│   └── wiki/                         # Scraped AWOIAF wiki cache (git-TRACKED — ~35k files; only sources/raw is ignored)
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
│   └── wiki/                         # Wiki pipeline workspace (see working/wiki/README.md)
│       ├── data/                     # Permanent reference products (alias-resolver, infobox-data, page-index, etc.)
│       ├── pass2-buckets/            # 536 per-bucket workspaces from Pass 2 promotion run
│       └── pass2-staging/            # Run-specific Pass 2 staging artifacts (triage, draft-buckets, summaries)
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

## Vocabulary (canonical — DECIDED 2026-06-16, S103)

Use these words for **new** work. Full definitions + the retired-term decode list: `reference/glossary.md`.

- **Pass** — a big numbered sweep over the whole book corpus (Passes 1–6). Grandfathered.
- **Track** — a *named* chunk of work toward one deliverable (e.g. *the infobox-merge track*). Never lettered/numbered as its identifier — use the name.
- **step** (lowercase) — an ordered piece inside a Track ("step 2 of the X track"). Replaces the old Stage/Plate/Phase/Wave habit — don't mint a fresh word when you sequence work.
- **Tier** — confidence rating **1–5 only**. Never used for work or process (it's stamped on the data — a stray meaning corrupts the graph). Other graded systems use class/level/priority.

Rules: adding a new capitalized term needs a worklog Active Decision; version numbers attach only to artifacts (prompt v5, `edges.jsonl` v1.3), never to efforts. Retired terms (Stage/Plate/Mode/Wave/Bucket/Phase, letter-tracks) are valid only when citing past sessions. Script/skill/command names are exempt. **When you spawn a subagent that will name a Track, number steps, or label a sequence, paste these terms into its prompt** — subagents don't load this file.

**Session numbering (parallel tracks, split 2026-06-22, S132c):** graph + meta sessions number globally (**S133, S134…**) in `worklog.md`; **D&E Pass-1** sessions number **DE-1, DE-2…** in `worklog-dunk-egg.md`. The two number-spaces are **independent** — there is no cross-track write-order tiebreaker anymore (it now only orders same-day graph/meta sessions). Don't re-collide them (the ambiguity S132/S132b/S132c worked around).

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

A file named `scratch` (or `scratch.md` / `scratch.txt`) at the repo root is **Matt's private notes**, not project state. It is gitignored. **Do not read it, surface it, or act on its contents — ever — unless Matt explicitly tells you to in the current turn.** This includes `/endsession`: scratch is NOT triaged as part of any checklist. Treat scratch as if it doesn't exist until Matt says otherwise.

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
8. **Worklog Session Log holds at most 5 entries.** When a 6th session lands, archive the oldest to `history/worklog-archives/archiveNNN.md`. Each archive file holds exactly 5 entries (start a new `archiveNNN.md` when the current one is full). The worklog itself keeps Current State, Active Decisions, Ideas & Backlog, Principles, and the 5 most recent session entries. **This rule applies to `worklog.md` only.** The D&E track's `worklog-dunk-egg.md` is **exempt** — it does NOT archive to `history/worklog-archives/`; if it ever exceeds 5 entries it self-contains overflow in an `## Archived sessions` section at its own foot, and the whole file is frozen to `history/` when D&E Pass-1 completes.
9. **When a continue prompt's project-state claims contradict `worklog.md`, trust `worklog.md` and flag the contradiction.** Continue prompts are task-scoped snapshots written at end-of-session under context pressure; they may lag worklog by multiple sessions. `worklog.md` is the authoritative state file, updated every session. **Per-track authority (split 2026-06-22, S132c):** `worklog.md` is authoritative for the **graph track + all shared state** (Active Decisions, Ideas & Backlog, Principles); **`worklog-dunk-egg.md` is authoritative for D&E Pass-1 status.** Defer to whichever file owns the claim; project-wide decisions live in `worklog.md` Active Decisions even when first made in a D&E session. The STATUS cross-track pointer in `worklog.md` is deliberately dateless — it names the D&E file, never mirrors its number/status, so it can't drift. If a continue prompt says "X is incomplete" but `worklog.md` says "X is done" (or vice versa), say so explicitly at session start before proceeding: *"The continue prompt states [X claim], but worklog.md says [Y claim]. Trusting worklog.md. The continue prompt may need updating."* Do not silently propagate the stale claim into your session work. The same rule applies to memory entries — they're point-in-time snapshots, not live state. (Root cause precedent: Session 55, 2026-05-18, stale "ACOK 20/70" propagation.)
