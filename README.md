# The Weirwood Network

A structured knowledge graph for A Song of Ice and Fire (ASOIAF). Extracts characters, locations, events, relationships, and more from the source texts into a queryable graph with spoiler gating.

## Getting Started

### Prerequisites

- **iTerm2** (the extraction launcher opens tabs automatically)
- **`claude` CLI** installed and authenticated ([claude.ai/code](https://claude.ai/code))
- **Python 3** (for the chapter splitter and stats)
- **Source text files** — plain `.txt` files of the five ASOIAF novels (you provide these)

### 1. Clone and set up the shell function

```bash
git clone <repo-url> ~/source/asoiaf-chat
cd ~/source/asoiaf-chat

# Add the weirwood function to your shell
echo 'source ~/source/asoiaf-chat/scripts/weirwood.zsh' >> ~/.zshrc
source ~/.zshrc
```

If the repo isn't at `~/source/asoiaf-chat`:

```bash
export WEIRWOOD_PROJECT_DIR="/path/to/asoiaf-chat"
source "$WEIRWOOD_PROJECT_DIR/scripts/weirwood.zsh"
```

### 2. Place your source files

> **Already have `sources/raw/`, `sources/chapters/`, and `sources/wiki/` populated?** Skip to step 4 (`weirwood check`).

Put your plain-text `.txt` source files in `sources/raw/`:

| File | Book |
|------|------|
| `GoT.txt` | A Game of Thrones |
| `ACOK.txt` | A Clash of Kings |
| `ASOS.txt` | A Storm of Swords |
| `AFFC.txt` | A Feast for Crows |
| `ADWD.txt` | A Dance with Dragons |

These are `.txt` files converted from EPUB. The chapter splitter expects them.

> **Don't have .txt files?** Tell Claude Code where your source files are (EPUB, PDF, whatever) and it can help convert and place them. Just say: *"My books are at /path/to/files, help me get them set up."*

> **Important:** Source files are gitignored and must never be committed. The `sources/raw/` and `sources/chapters/` directories are protected by `.gitignore`.

### 3. Split chapters

The chapter splitter breaks each book into individual chapter files with YAML frontmatter:

```bash
python3 scripts/chapter-splitter.py sources/raw/GoT.txt agot
python3 scripts/chapter-splitter.py sources/raw/ACOK.txt acok
python3 scripts/chapter-splitter.py sources/raw/ASOS.txt asos
python3 scripts/chapter-splitter.py sources/raw/AFFC.txt affc
python3 scripts/chapter-splitter.py sources/raw/ADWD.txt adwd
```

This creates files like `sources/chapters/agot/agot-bran-01.md`, one per chapter.

### 4. Verify everything is in place

```bash
weirwood check
```

This checks raw source files, split chapters, extraction progress, and prerequisites. If anything is missing, it tells you exactly what to do.

### 5. Run extractions

```bash
# See what's done across all books
weirwood

# Detailed status for one book (wave table, costs, suggested command)
weirwood acok

# Launch extraction: 2 terminals, 3 waves each
weirwood acok 2 3

# Launch with a specific model (default: claude-opus-4-6)
weirwood acok 2 3 claude-sonnet-4-6
```

That's it. The script finds incomplete waves, opens iTerm tabs, and each tab runs its assigned waves. When you come back later, run the same command — it picks up where it left off.

## How Extraction Works

Chapters are grouped into **waves** of 5. When you launch, the script distributes incomplete waves across iTerm tabs. Each tab runs its waves one at a time.

```
weirwood acok 3 2
```

This finds the next 6 incomplete waves and assigns 2 to each of 3 iTerm tabs. Each tab runs its 2 waves sequentially — so you have 3 chapters extracting concurrently at any moment.

### Resuming

The script checks which extractions already exist on disk. Run the same command again and it skips completed chapters automatically. You never need to track where you left off.

### Soft Stop

```bash
weirwood stop
```

Creates a marker file that running terminals check between waves. It never interrupts mid-chapter — the current wave finishes, then the terminal exits instead of starting the next wave. Run it from any terminal. The marker is cleared automatically on the next launch.

### Rate Limits

If the API rate limit is hit mid-wave, the script detects it, halts immediately, and reports the reset time. No wasted attempts on chapters that would fail instantly.

### Validation

A chapter extraction is considered complete when:
- The output file has at least 100 lines
- It contains all required sections (`## Characters`, `## Events`, `## Locations`, `## Relationships`)

Incomplete extractions are automatically re-extracted on the next launch.

### Stats & Cost Tracking

Every extraction logs to `working/extraction-stats/` with per-chapter timing, token usage (including cache hits), and cost. View aggregate stats with `weirwood <book>`.

## Command Reference

| Command | What it does |
|---------|-------------|
| `weirwood` | Help + overview across all books |
| `weirwood check` | Verify source files, chapters, and prerequisites |
| `weirwood <book>` | Detailed status: wave table, costs, suggested next command |
| `weirwood <book> <terminals> <waves>` | Launch iTerm tabs to run extractions |
| `weirwood <book> <t> <w> <model>` | Launch with a specific Claude model |
| `weirwood stop` | Soft stop — halt after current wave finishes |

### Books

| Code | Book | Chapters |
|------|------|----------|
| `agot` | A Game of Thrones | 73 |
| `acok` | A Clash of Kings | 70 |
| `asos` | A Storm of Swords | 82 |
| `affc` | A Feast for Crows | 46 |
| `adwd` | A Dance with Dragons | 73 |

## Extraction Pipeline

The project builds the knowledge graph through a sequence of extraction passes, each layering on top of the last.

| Pass | Agent | What it does |
|------|-------|-------------|
| 1 | **Mechanical Extractor** | Raw facts from the text — characters, locations, events, relationships, food/hospitality, physical descriptions, spatial layout. No interpretation. One extraction per chapter. |
| 2 | **Wiki Ingester** | Structures AWOIAF wiki pages into entity nodes. Enriches the graph with canonical details the text doesn't state explicitly (birth years, house words, etc.). |
| 3 | **Voice Analyzer** | POV character voice profiles and cross-POV perception mappings. |
| 4 | **Foreshadowing Scanner** | Scans extractions for textual hints that foreshadow known future events. |
| 5 | **Theory Extractor** | Finds textual evidence for and against known fan theories. |
| 6 | **Discovery Agent** | Open-ended pattern finding across the full extraction corpus. |

Pass 1 is the foundation — everything else reads from its outputs. Currently: Pass 1 complete for AGOT (73/73), remaining books ready to run.

## Project Structure

```
asoiaf-chat/
├── sources/
│   ├── raw/                         Source .txt files (GITIGNORED)
│   └── chapters/{book}/             Split chapter files (GITIGNORED)
├── extractions/
│   ├── mechanical/{book}/           Pass 1 extraction outputs
│   └── archives/                    Prior-version extractions
├── graph/
│   ├── nodes/                       Entity files (characters, locations, etc.)
│   └── edges/                       Relationship files
├── scripts/
│   ├── extract.sh                   Extraction runner (waves, stats, rate-limit detection)
│   ├── weirwood.zsh                 Shell function wrapper
│   └── chapter-splitter.py          Splits .txt into per-chapter markdown
├── reference/
│   ├── architecture.md              Data model: entity types, edge types, confidence tiers
│   ├── pov-characters.md            POV lookup table + expected chapter counts
│   └── foreshadowing-events.md      26 events + 15 Chekhov's guns
├── working/                         Stats, session details, TODOs, runbooks
├── progress/                        Wave logs, continue prompts
└── CLAUDE.md                        Full architecture and agent system documentation
```

See `CLAUDE.md` for the complete orchestrator guide, agent definitions, and project conventions.
