# Session 1 — Project Scaffolding & Cleanup

**Date:** 2026-04-13

---

## What Triggered This Session

Session 0 produced an architecture, but it was all in documents — no directory structure, no tooling, no git repo discipline. The architecture spec described a directory tree that didn't exist yet. Before any extraction work could begin, the project needed its skeleton built and its safety rails installed.

## What Happened

### .gitignore First

The very first action was creating `.gitignore`, before any other file. This was deliberate sequencing: the source texts (all five ASOIAF novels, the Dunk and Egg novellas, The World of Ice and Fire) are copyrighted material that must never enter git history. Not "should be excluded" — MUST never appear in a commit. Once a file enters git history, it's there forever (short of history rewriting), and this is a project that will eventually have a public GitHub repo.

The `.gitignore` excludes `sources/raw/` (the original .txt files), `sources/chapters/` (the split chapter files), `sources/reference/` (non-narrative source material), and later `sources/wiki/` (scraped wiki content). These directories exist locally for processing but are invisible to git.

### Building the Directory Skeleton

With the safety rail in place, the full directory structure was created from the architecture spec. This meant building out the tree that Session 0 designed:

- `sources/` with subdirectories for raw texts, split chapters (per book), and wiki content
- `extractions/` with subdirectories per pass type (mechanical, voice, foreshadowing, patterns) and per book within mechanical
- `graph/` with `nodes/` (per entity type: characters, locations, factions, houses, artifacts, prophecies, theories) and `edges/`
- `index/` for the trigger table (not yet populated)
- `curation/` for candidates awaiting human review
- `progress/` for tracking extraction progress
- `reference/` for architectural documents
- `working/` as the project scratchpad

### Subagent Definitions

Seven subagent definitions were created in `.claude/agents/`. The project uses Claude Code's subagent system — the orchestrator (Claude, guided by CLAUDE.md) delegates specialized work to purpose-built agents:

- **script-builder** — Writes Python tooling (chapter splitter, wiki scraper, any automation)
- **mechanical-extractor** — Runs Pass 1 extraction against chapter files

The remaining five were stubs with TODO markers, since their prompts depended on earlier pipeline stages completing first:
- **wiki-ingester** (Pass 2)
- **voice-analyzer** (Pass 3)
- **foreshadowing-scanner** (Pass 4)
- **theory-extractor** (Pass 5)
- **discovery-agent** (Pass 6)

Each stub file documented what the agent would eventually do, what inputs it would need, and what it would produce — enough to inform the architecture without requiring premature prompt engineering.

### Root Cleanup

The root directory had accumulated spec documents from Session 0 that didn't belong there. These were moved into `reference/`:
- Architecture spec became `reference/architecture.md`
- Foreshadowing events list became `reference/foreshadowing-events.md`
- POV character lookup table became `reference/pov-characters.md`

Original files at the root were deleted after confirming the moves. The goal: root contains CLAUDE.md, worklog.md, and directory-level config only.

### Working Directory Setup

`working/` was initialized with `progress.md` (later split into per-book files in `progress/`) and `todos.md` for actionable items. The working directory would become the project's scratchpad — anything in-progress, uncertain, or awaiting triage goes here rather than being discarded.

## Key Decisions and Why

| Decision | Reasoning |
|----------|-----------|
| `.gitignore` created before any other file | Copyrighted content entering git history is irrecoverable without destructive history rewriting. The safety rail had to exist before anything else. |
| Local dir stays `asoiaf-chat`, GitHub repo will be `the-weirwood-network` | The local name reflects how the project started (as a chat-based exploration); the public name reflects what it became. No reason to rename locally — git remote handles the mapping. |
| Later-pass agents as stubs with TODOs | Writing agent prompts before the pipeline reaches their stage would mean guessing at inputs and schemas. Stubs document intent without committing to premature specifics. |
| Reference docs moved out of root | Root should be navigational (CLAUDE.md, worklog) not archival. Reference material has its own directory. |

## What Was Left Open

- No code had been written yet — the chapter splitter and wiki scraper were next
- The mechanical extractor prompt existed in draft form from Session 0 but hadn't been tested against actual chapter text
- The `working/` directory conventions were loose — it would take several sessions to develop the two-tier documentation pattern (lean worklog entries + full session narratives)
- No git commits had been made yet — the project existed only on disk. The first commit wouldn't happen until 2026-04-22, nine days later, after substantial extraction work was complete
