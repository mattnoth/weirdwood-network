# Pass 1 Mechanical Extraction — How To

## What This Does

Runs a Claude agent against every chapter file to produce a structured extraction (characters, locations, food, hospitality, physical descriptions, spatial layout, etc.). One extraction per chapter, written to `extractions/mechanical/{book}/`.

## Prerequisites

- Chapter files exist in `sources/chapters/{book}/` (run the splitter first if they don't)
- iTerm2 installed
- `claude` CLI available in your PATH

## Commands

### Shell function (preferred)

```bash
# Source it (auto-sourced if terminal-collection is set up)
source ~/source/terminal-collection/functions/weirwood-mechanical.zsh
```

| Command | What it does |
|---------|-------------|
| `weirwood-mechanical agot 4` | Waves 1-4, one per terminal, then stops |
| `weirwood-mechanical agot 4 9` | Waves 9-12, one per terminal |
| `weirwood-mechanical --chain agot 4` | All remaining waves, chained across 4 terminals |
| `weirwood-mechanical --chain agot 4 9` | Chain from wave 9 |
| `weirwood-mechanical --stop` | Stop chained run after current wave finishes |

### Direct script (same args)

```bash
./scripts/launch-extraction.sh agot 4
./scripts/launch-extraction.sh --chain agot 4
```

## Default workflow

Run one batch at a time, check results, then continue:

```bash
# Batch 1: waves 1-4
weirwood-mechanical agot 4

# ... wait ~12 min, check results ...

# Batch 2: waves 5-8
weirwood-mechanical agot 4 5

# Batch 3: waves 9-12
weirwood-mechanical agot 4 9

# Batch 4: waves 13-15 (only 3 waves left, 4th terminal is idle)
weirwood-mechanical agot 4 13
```

## Chained workflow

Fire and forget, with a kill switch:

```bash
# Launch everything
weirwood-mechanical --chain agot 4

# Changed your mind? Stop after current wave:
weirwood-mechanical --stop

# Or equivalently:
touch /tmp/extraction-stop
```

## Tuning the terminal count

- **4 terminals** worked well for the AGOT v1 run without hitting usage limits
- More terminals = faster but more API calls in parallel = higher chance of hitting limits
- Fewer terminals = slower but safer
- Start with 4, adjust from there

## Timing

- ~2-3 minutes per chapter
- ~10-12 minutes per wave (5 chapters)
- With 4 terminals: ~3 hours per book

## If Something Crashes

If a terminal dies mid-wave or you hit a usage limit:

1. Note which waves finished (each terminal prints its wave number)
2. Check progress: `tail -20 working/progress.md`
3. Re-launch from where you left off:

```bash
# Resume AGOT from wave 9 (waves 1-8 already done)
weirwood-mechanical agot 4 9
```

The script overwrites existing extractions, so re-running a wave that partially completed is fine.

## Checking Results

```bash
# How many extractions exist?
ls extractions/mechanical/agot/ | wc -l

# Check the stats log
cat working/extraction-stats.csv

# Look at progress notes
tail -20 working/progress.md
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
