# The Weirwood Network — Project Status & Orientation

**Last updated:** 2026-04-23

> Open this file when you come back after a break. It tells you what exists, what's done, what's next, and where everything lives.

---

## What This Project Is

A structured knowledge graph for A Song of Ice and Fire. We're extracting every character, location, artifact, event, relationship, food description, and physical detail from the books into queryable structured data — then layering on analytical passes for voice profiles, foreshadowing, and theory evidence.

The end state: a spoiler-gated graph you can traverse to answer questions like "who has Littlefinger spoken to privately across all five books?" or "what food is served at every feast in ASOS?" or "what does Tyrion look like according to every POV character who describes him?"

---

## Where Things Stand (2026-04-23)

### What's Done

| What | Status | Details |
|------|--------|---------|
| Repository & scaffold | Done | All directories created, CLAUDE.md, worklog, reference docs |
| Chapter splitter | Done | All 5 books split: 344 chapters total (AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73) |
| D&E novellas | Done | 3 novellas split (THK, TSS, TMK — 1 chapter each, continuous text) |
| TWOIAF OCR | Done | PDF OCR'd to searchable text, 179K words extracted |
| Wiki scrape | Done | 17,945 pages scraped from AWOIAF, 377 MB in `sources/wiki/` |
| Pass 1 v1 (AGOT) | Done | 73/73 chapters, archived to `extractions/archives/agot-v1/` |
| Pass 1 v2 (AGOT) | Done | 73/73 chapters, in `extractions/mechanical/agot/` — expanded schema with food, hospitality, appearances, spatial layout |
| Extraction tooling | Done | Wave-based shell scripts for parallel extraction across terminal tabs |

### What's Next (Roughly In Order)

1. **Compare v1 vs v2 AGOT extractions** — We have two complete runs. Comparing them will show what the expanded schema captured that v1 missed, and validate that v2 quality is good.
2. **Pass 1 on remaining books** — ACOK (70 chapters), ASOS (82), AFFC (46), ADWD (73). Same process as AGOT, using the v2 agent prompt.
3. **Write Pass 2 agent prompt** — Wiki ingestion. Turn the 17,945 scraped wiki pages into structured node files in `graph/nodes/`.
4. **Build the index** — Trigger table and entity index from Pass 1 extractions.
5. **Write Passes 3-6 agent prompts** — Voice analysis, foreshadowing, theory extraction, discovery.
6. **Graph construction** — Nodes and edges from all extraction passes.

### What's Blocked

- Passes 3-6 can't start until Pass 1 covers more books (they need cross-chapter data)
- Pass 2 needs its agent prompt written
- Graph construction needs at least Pass 1 + Pass 2 complete

---

## Where Everything Lives

```
asoiaf-chat/
│
├── CLAUDE.md              # Instructions for Claude Code sessions
├── STATUS.md              # THIS FILE — project orientation
├── worklog.md             # Session-by-session history of all work done
│
├── sources/               # INPUT — raw text, chapter files, wiki data
│   ├── raw/               # Original .txt book files [GITIGNORED]
│   ├── chapters/          # Split per-chapter markdown [GITIGNORED]
│   │   ├── agot/          #   73 chapters
│   │   ├── acok/          #   70 chapters
│   │   ├── asos/          #   82 chapters
│   │   ├── affc/          #   46 chapters
│   │   ├── adwd/          #   73 chapters
│   │   ├── thk/ tss/ tmk/ #   D&E novellas (1 each)
│   └── wiki/              # Scraped AWOIAF pages [GITIGNORED]
│
├── extractions/           # OUTPUT — structured data from extraction passes
│   ├── mechanical/        #   Pass 1 outputs (chapter-level inventories)
│   │   ├── agot/          #     73 files (v2, current)
│   │   ├── acok/          #     empty — not started
│   │   ├── asos/          #     empty — not started
│   │   ├── affc/          #     empty — not started
│   │   └── adwd/          #     empty — not started
│   ├── archives/          #   Old extraction versions
│   │   └── agot-v1/       #     73 files (v1, for comparison)
│   ├── voice/             #   Pass 3 — empty, not started
│   ├── foreshadowing/     #   Pass 4 — empty, not started
│   └── patterns/          #   Pass 5+ — empty, not started
│
├── graph/                 # THE GRAPH — nodes, edges, convergence maps
│   ├── nodes/             #   Entity files (empty — not started)
│   │   ├── characters/ locations/ factions/
│   │   └── artifacts/ prophecies/ theories/
│   ├── edges/             #   Relationship files (empty — not started)
│   └── convergence-maps/  #   High-density intersection docs (empty)
│
├── index/                 # Trigger table & entity index (empty — not started)
│
├── progress/              # Extraction progress tracking
│   └── continue-prompts/  #   Self-contained resumption prompts
│
├── reference/             # Design docs & lookup tables
│   ├── agents.md          #   Inventory of all 8 agents + status
│   ├── architecture.md    #   System architecture & conventions
│   ├── foreshadowing-events.md  # 26 events + 15 Chekhov's guns
│   ├── pass-1-mechanical-extraction.md  # Pass 1 design & schema
│   └── pov-characters.md  #   POV lookup table + chapter counts
│
├── working/               # Scratchpad — TODOs, stats, runbooks
│   ├── todos.md           #   Actionable items by topic
│   ├── extraction-stats/  #   Token/timing CSVs per book-pass
│   ├── taxonomy-candidates.md  # Proposed node types for Pass 2
│   ├── runbooks/          #   How-to procedures
│   └── worklog-archives/  #   Archived worklog sessions
│
├── scripts/               # Python & shell tooling
│   ├── chapter-splitter.py      # Splits .txt → per-chapter markdown
│   ├── dunk-egg-splitter.py     # D&E novella splitter
│   ├── wiki-scraper.py          # AWOIAF wiki scraper (Playwright)
│   ├── run-extraction-wave.sh   # Runs a wave of extractions
│   ├── launch-extraction.sh     # Opens iTerm2 tabs for parallel waves
│   ├── run-extraction-all.sh    # Full book extraction orchestrator
│   └── extraction-status.sh     # Reports extraction progress
│
├── curation/              # Human review queue (empty — not started)
│
└── .claude/
    ├── agents/            # 8 subagent definitions
    ├── commands/          # Slash commands (endsession)
    └── settings.json      # Permission denials (copyrighted content protection)
```

---

## The Six-Pass Pipeline

Each pass reads the output of prior passes and adds a new layer of analysis.

| Pass | Agent | Input | Output | Status |
|------|-------|-------|--------|--------|
| **1. Mechanical** | `mechanical-extractor` | Chapter text | Characters, locations, events, food, hospitality, appearances, spatial layout — one file per chapter | AGOT done (v2). 4 books remaining. |
| **2. Wiki** | `wiki-ingester` | Scraped wiki pages + Pass 1 entity lists | Structured node files in `graph/nodes/` | Agent prompt not yet written. Wiki data ready. |
| **3. Voice** | `voice-analyzer` | All chapters for a given POV character | Voice profiles + cross-POV perception maps (how different POVs see the same person) | Agent prompt not yet written. |
| **4. Foreshadowing** | `foreshadowing-scanner` | Pass 1 extractions + `reference/foreshadowing-events.md` | Mappings from textual details to known future events | Agent prompt not yet written. |
| **5. Theory** | `theory-extractor` | Pass 1 extractions + theory seeds file | Evidence for/against known theories (R+L=J, Bolt-On, etc.) | Agent prompt not yet written. Needs `reference/theory-seeds.md`. |
| **6. Discovery** | `discovery-agent` | Full extraction corpus | Novel patterns nobody has flagged yet | Agent prompt not yet written. Runs last. |

---

## Key Design Principles

- **Spoiler gating is architectural.** Every node, edge, and extraction carries a `first_available` field. You can query the graph at any reading depth.
- **Agents propose, Matt decides.** Analytical findings go to `curation/candidates.md` for human review, not directly into the graph.
- **Chapter isolation in Pass 1.** Each extraction treats its chapter as if no other chapters exist. No "as we saw in Bran I" or "this foreshadows the Red Wedding." Cross-chapter connections are later passes' job.
- **Comprehensiveness over elegance.** GRRM hides Chekhov's guns in food descriptions, heraldry, weather, and architecture. The extractor logs everything.
- **Copyrighted content never enters git.** `sources/raw/` and `sources/chapters/` are gitignored and permission-denied in `.claude/settings.json`.

---

## Cost & Scale So Far

AGOT Pass 1 v2 (73 chapters): ~$35 in API costs, ~8.5M tokens, ~3 hours wall-clock across parallel terminal tabs. See `working/extraction-stats/` for per-chapter breakdowns.

Remaining 4 books at similar rates: ~$140 estimated for full Pass 1 coverage (~271 chapters).

---

## Quick Reference

| I want to... | Go to... |
|---|---|
| Understand the system architecture | `reference/architecture.md` |
| See what happened in past sessions | `worklog.md` |
| See what needs doing | `working/todos.md` |
| Check extraction progress | `progress/pass1-agot.md` |
| Read an extraction example | `extractions/mechanical/agot/agot-prologue.extraction.md` |
| See all agents and their status | `reference/agents.md` |
| Run an extraction batch | `working/runbooks/mechanical-extraction-howto.md` |
| Check token costs | `working/extraction-stats/` |
