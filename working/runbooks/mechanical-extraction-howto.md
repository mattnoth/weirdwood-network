# Pass 1 Mechanical Extraction — How To

> **STATUS: Pass 1 is COMPLETE — 344/344 chapters across all five books.** Nothing here
> needs re-running; the outputs are committed under `extractions/mechanical/{book}/`.
> This runbook documents the machinery in case a re-extraction is ever *deliberately*
> required (a prompt-version bump, a corrupted source). **Launching one is a decision, not
> a setup step** — extraction runs cost real money and burn usage windows, so per
> `CLAUDE.md` they are never kicked off without asking Matt first. If you just want to work
> with the graph, you want `weirwood query` (root [`README.md`](../../README.md)), not this file.

## What This Does

Runs a Claude agent against every chapter file to produce a structured extraction (characters, locations, food, hospitality, physical descriptions, spatial layout, etc.). One extraction per chapter, written to `extractions/mechanical/{book}/`.

## Prerequisites

- Chapter files exist in `sources/chapters/{book}/` (run the splitter first if they don't)
- Raw book text in `sources/raw/` (gitignored, not distributed)
- iTerm2 installed
- `claude` CLI available in your PATH

## Commands

The launcher is the `weirwood` shell function (`scripts/weirwood.zsh`, wrapping
`scripts/extract.sh`). Source it once:

```bash
echo 'source ~/source/asoiaf-chat/scripts/weirwood.zsh' >> ~/.zshrc
source ~/.zshrc
```

If the repo isn't at `~/source/asoiaf-chat`, set `WEIRWOOD_PROJECT_DIR` to its path first.

| Command | What it does |
|---------|-------------|
| `weirwood` | Help + overview across all books |
| `weirwood check` | Verify source files, chapters, and prerequisites |
| `weirwood <book>` | Detailed status: wave table, costs, suggested next command |
| `weirwood <book> <terminals> <waves>` | Launch iTerm tabs to run extractions |
| `weirwood <book> <t> <w> <model>` | Launch with a specific model (default: `claude-opus-4-6`) |
| `weirwood <book> <t> <w> --delay 2h --chain` | Auto-advance: wait 2h between batches, re-launch automatically |
| `weirwood stop` | Soft stop — halt after the current wave finishes |

Books: `agot` · `acok` · `asos` · `affc` · `adwd`.

## Waves

Chapters are grouped into **waves** of 5, distributed across iTerm tabs. `weirwood acok 3 2`
finds the next 6 incomplete waves and assigns 2 to each of 3 tabs — each tab runs its waves
sequentially, so 3 chapters extract concurrently at any moment.

```bash
# Batch: 2 terminals, 3 waves each
weirwood acok 2 3

# Auto-advance across usage windows: next batch launches after a 2h wait
weirwood acok 2 1 --delay 2h --chain
```

**Auto-advance** (`--delay` + `--chain`) spreads a long multi-batch run across API usage
windows without manual re-launching. Details: [`pass1-auto-advance-mode.md`](pass1-auto-advance-mode.md).

## Resuming

The script checks which extractions already exist on disk and skips completed chapters. Run
the same command again and it picks up where it left off — you never track your place
manually.

An extraction counts as complete when the output file has at least 100 lines and contains
all required sections (`## Characters`, `## Events`, `## Locations`, `## Relationships`).
Incomplete extractions are automatically re-extracted on the next launch.

## Soft stop

```bash
weirwood stop
```

Writes a marker file that running terminals check *between* waves — the current wave always
finishes, then the terminal exits instead of starting the next. Run it from any terminal;
it's cleared automatically on the next launch.

## Rate limits

If the API rate limit is hit mid-wave, the script halts immediately and reports the reset
time rather than burning attempts on chapters that would fail instantly.

## Tuning the terminal count

- More terminals = faster, but more parallel API calls = higher chance of hitting limits
- Fewer terminals = slower but safer
- 4 terminals worked well for the AGOT v1 run without hitting usage limits

## Timing

- ~2-3 minutes per chapter
- ~10-12 minutes per wave (5 chapters)
- With 4 terminals: ~3 hours per book

## Checking Results

```bash
# How many extractions exist?
ls extractions/mechanical/agot/ | wc -l

# Per-chapter timing, token usage (incl. cache hits), and cost
ls working/extraction-stats/

# Aggregate stats for a book
weirwood agot
```

## Book Order

| Book | Chapters | Waves | Est. time (4 terminals) |
|------|----------|-------|------------------------|
| AGOT | 73 | 15 | ~3 hours |
| ACOK | 70 | 14 | ~3 hours |
| ASOS | 82 | 17 | ~3.5 hours |
| AFFC | 46 | 10 | ~2 hours |
| ADWD | 73 | 15 | ~3 hours |

## What the Agent Extracts

Each chapter produces a `.extraction.md` file with these sections:

- Chapter Metadata (with time markers)
- Physical Environment (weather, season, lighting, sounds, smells)
- Characters Present
- Character Appearances (hair, eyes, build, scars, clothing, weapons, age)
- Characters Referenced
- Locations
- Location Descriptions (defensive features, architecture, interiors, scale, condition, terrain)
- Artifacts & Objects
- Food & Drink (dishes, ingredients, who eats with whom, preparation details)
- Hospitality & Guest Right (bread and salt, guest right, violations)
- Events & Actions
- Spatial Layout & Movement (phase-based positioning)
- Information Revealed
- Dialogue of Note
- POV Character's Internal State
- Relationships Observed
- Unanswered Questions
- Raw Entity List
