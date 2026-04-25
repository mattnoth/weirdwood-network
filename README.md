# The Weirwood Network

A structured knowledge graph for A Song of Ice and Fire (ASOIAF). Extracts characters, locations, events, relationships, and more from the source texts into a queryable graph with spoiler gating.

## Running Extractions

The extraction pipeline processes chapters in **waves** (groups of 5 chapters). You control how many waves to run and how many iTerm terminals to use.

### Prerequisites

- iTerm2 (launches tabs automatically)
- `claude` CLI installed and authenticated
- The `weirwood` shell function loaded in your shell (see Setup below)

### Setup

Source the shell function in your `.zshrc`:

```bash
source ~/source/asoiaf-chat/scripts/weirwood.zsh
```

If the repo isn't at `~/source/asoiaf-chat`, set the env var:

```bash
export WEIRWOOD_PROJECT_DIR="/path/to/asoiaf-chat"
source "$WEIRWOOD_PROJECT_DIR/scripts/weirwood.zsh"
```

Or use `./scripts/extract.sh` directly — see `reference/extraction-commands.md` for the full flag-level reference.

### Quick Start

```bash
# See what's done across all books
weirwood

# Detailed status for one book (wave table, costs)
weirwood acok

# Launch extraction: 2 terminals, 3 waves each
weirwood acok 2 3

# Launch with a specific model (default: claude-opus-4-6)
weirwood acok 2 3 claude-sonnet-4-6

# Soft stop — halt after the current wave finishes
weirwood stop
```

### How It Works

1. **Check status** — `weirwood acok` shows which waves are complete, which have missing chapters, and suggests the next command to run.

2. **Launch** — `weirwood acok 2 3` finds the next 6 incomplete waves, assigns 3 to each of 2 iTerm tabs, and starts them. Each tab runs its waves sequentially (wave 1, then wave 2, then wave 3).

3. **Resume** — When a session ends (or you close your laptop), just run the same command again. The script checks which extractions are already complete and picks up from the next incomplete wave. You never need to manually track where you left off.

4. **Repeat** — Keep running until `weirwood <book>` says "All chapters extracted!"

### Soft Stop

`weirwood stop` creates a marker file (`/tmp/extraction-stop`) that running terminals check **between waves**. It never interrupts a chapter mid-extraction — the current wave finishes normally, then the terminal sees the stop file and exits instead of starting the next wave.

- Run it from **any terminal** — a third tab, Claude Code (`! weirwood stop`), wherever. It doesn't communicate with the running terminals directly; they discover the file on their own.
- The stop file is **automatically cleared** the next time you launch a run.
- Use it when you need to pause early — closing your laptop, switching models, or just done for the day.

### Extraction Validation

A chapter extraction is considered complete when:
- The output file has at least 100 lines
- It contains all required sections: `## Characters`, `## Events`, `## Locations`, `## Relationships`

Incomplete extractions are automatically re-run on the next launch. No manual cleanup needed.

### Stats & Cost Tracking

Every extraction logs to `working/extraction-stats.csv` with per-chapter timing, token usage (including cache hits), and cost. View aggregate stats with `weirwood <book>`.

### Command Reference

| Command | What it does |
|---------|-------------|
| `weirwood` | Help + overview across all books |
| `weirwood <book>` | Detailed status: wave table, costs, suggested next command |
| `weirwood <book> <terminals> <waves>` | Launch iTerm tabs to run extractions |
| `weirwood <book> <t> <w> <model>` | Launch with a specific Claude model |
| `weirwood stop` | Soft stop — halt after current wave finishes |

### Books

| Code | Book |
|------|------|
| `agot` | A Game of Thrones |
| `acok` | A Clash of Kings |
| `asos` | A Storm of Swords |
| `affc` | A Feast for Crows |
| `adwd` | A Dance with Dragons |

## Extraction Pipeline

The project builds the knowledge graph through a sequence of extraction passes, each layering on top of the last.

| Pass | Agent | What it does |
|------|-------|-------------|
| 1 | **Mechanical Extractor** | Raw facts from the text — characters, locations, events, relationships, food/hospitality, physical descriptions, spatial layout. No interpretation, no inference. One extraction per chapter. |
| 2 | **Wiki Ingester** | Structures AWOIAF wiki pages into entity nodes. Enriches the graph with canonical details the text doesn't state explicitly (birth years, house words, etc.). 17,945 wiki pages already scraped. |
| 3 | **Voice Analyzer** | Builds POV character voice profiles and cross-POV perception mappings — how Cersei describes Tyrion vs. how Tyrion describes himself, how different POVs see the same event. |
| 4 | **Foreshadowing Scanner** | Scans extractions for textual hints that foreshadow known future events. Works from a curated list of 26 events + 15 Chekhov's guns. |
| 5 | **Theory Extractor** | Finds textual evidence for and against known fan theories (R+L=J, Gravedigger, etc.). Collects passages, tags confidence. |
| 6 | **Discovery Agent** | Open-ended pattern finding across the full extraction corpus. The "what did we miss?" pass — runs after everything else. |

Pass 1 is the foundation — everything else reads from its outputs. Pass 2 (wiki) runs independently. Passes 3-6 are analytical and build on Pass 1 extractions.

Currently: Pass 1 complete for AGOT, in progress for ACOK. Passes 2-6 have agent stubs but prompts are not yet written.

## Project Structure

```
asoiaf-chat/
├── sources/chapters/{book}/     Chapter files (gitignored)
├── extractions/mechanical/{book}/  Pass 1 extraction outputs
├── graph/nodes/                 Entity files (characters, locations, etc.)
├── graph/edges/                 Relationship files
├── scripts/extract.sh           Unified extraction script
├── working/                     Scratchpad, stats, runbooks
└── progress/                    Wave logs, handoffs, scratch notes
```

See `CLAUDE.md` for the full architecture and agent system documentation.
