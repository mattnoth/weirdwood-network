# Extraction Commands Reference

Two interfaces to the same extraction system. `weirwood` is the shortcut that wraps `extract.sh`.

---

## weirwood (shell function)

The easy interface. Source `scripts/weirwood.zsh` in your shell, or set `WEIRWOOD_PROJECT_DIR` if the repo isn't at `~/source/asoiaf-chat`.

### Commands

```
weirwood                              Help + all-books overview
weirwood <book>                       Detailed status for one book
weirwood <book> <terminals> <waves>   Launch extraction
weirwood <book> <t> <w> <model>       Launch with specific model
weirwood stop                         Soft stop
```

### Examples

```bash
weirwood                     # What's the state of everything?
weirwood acok                # Show ACOK wave table, costs, what's left
weirwood acok 2 3            # Launch 2 iTerm tabs, 3 waves each
weirwood acok 2 3 claude-sonnet-4-6   # Same, but use Sonnet
weirwood stop                # Halt after the current wave finishes
```

---

## extract.sh (the script underneath)

`weirwood` calls this. You can use it directly if you prefer flags, or if you're scripting.

### Subcommands

#### status

Show extraction progress for a book.

```
./scripts/extract.sh status <book>
```

Displays: chapters done/remaining, completed waves, a table of incomplete waves with their missing chapters, cost summary from the stats CSV, and a suggested `weirwood` command.

**weirwood equivalent:** `weirwood <book>`

#### launch

Open iTerm2 tabs and start extracting.

```
./scripts/extract.sh launch <book> -t <terminals> -w <waves> [-m <model>]
```

| Flag | What | Default |
|------|------|---------|
| `-t, --terminals` | Number of iTerm tabs to open | (required) |
| `-w, --waves` | Waves per terminal | (required) |
| `-m, --model` | Claude model | `claude-opus-4-6` |

Finds the next incomplete waves, distributes them across terminals, opens iTerm tabs. Each tab runs its waves sequentially. If fewer incomplete waves remain than requested, it rebalances automatically.

**weirwood equivalent:** `weirwood <book> <terminals> <waves> [model]`

#### run

Run a single wave. This is what the iTerm tabs execute — you rarely call it directly.

```
./scripts/extract.sh run <book> --wave <N> [-m <model>] [--force]
```

| Flag | What | Default |
|------|------|---------|
| `--wave, -w` | Wave number to run | (required) |
| `--model, -m` | Claude model | `claude-opus-4-6` |
| `--force` | Re-run even if chapters are already complete | off |

Runs each chapter in the wave sequentially. Skips chapters that are already complete (unless `--force`). Appends per-chapter stats to `working/extraction-stats.csv`. Appends wave summary to `working/progress.md`.

**weirwood equivalent:** none (launch handles this)

---

## Mapping: weirwood to extract.sh

| You type | What runs |
|----------|-----------|
| `weirwood` | (inline help + overview, no extract.sh call) |
| `weirwood acok` | `extract.sh status acok` |
| `weirwood acok 2 3` | `extract.sh launch acok -t 2 -w 3` |
| `weirwood acok 2 3 claude-sonnet-4-6` | `extract.sh launch acok -t 2 -w 3 -m claude-sonnet-4-6` |
| `weirwood stop` | `touch $HOME/source/claude-cwd/tmp/extraction-stop` |

---

## Soft Stop

`weirwood stop` (or `touch $HOME/source/claude-cwd/tmp/extraction-stop`) creates a marker file. Running terminals check for this file **between waves** — after one wave finishes and before the next starts.

**What it does:**
- The current wave runs to completion (all 5 chapters finish)
- The terminal sees the stop file and exits instead of starting the next wave
- Each terminal discovers the file independently

**What it doesn't do:**
- Never interrupts a chapter mid-extraction
- Never kills a process or sends a signal

**Where to run it:**
- Any terminal tab (doesn't need to be one running extractions)
- Claude Code: `! weirwood stop` or `! touch $HOME/source/claude-cwd/tmp/extraction-stop`

**Cleanup:**
- The stop file is automatically deleted when you `launch` again
- Or manually: `rm $HOME/source/claude-cwd/tmp/extraction-stop`

---

## Completion Validation

A chapter extraction is considered complete when both conditions are met:
1. The output file has **at least 100 lines**
2. It contains **all four required sections**: `## Characters`, `## Events`, `## Locations`, `## Relationships`

Incomplete or truncated extractions are flagged as "tarnished" and automatically re-run on the next launch.

---

## Files Written

| File | What | Written by |
|------|------|-----------|
| `extractions/mechanical/{book}/{chapter}.extraction.md` | The extraction output | `run` |
| `working/extraction-stats.csv` | Per-chapter timing, tokens, cost | `run` |
| `working/progress.md` | Wave summaries (appended) | `run` |
| `$HOME/source/claude-cwd/tmp/extraction-{chapter}.json` | Raw claude stream-json output | `run` |
| `$HOME/source/claude-cwd/tmp/extraction-{chapter}.log` | Readable text from claude output | `run` |
| `$HOME/source/claude-cwd/tmp/extraction-stop` | Soft stop marker | `stop` |

---

## Books

| Code | Book | Chapters |
|------|------|----------|
| `agot` | A Game of Thrones | 73 |
| `acok` | A Clash of Kings | 70 |
| `asos` | A Storm of Swords | 82 |
| `affc` | A Feast for Crows | 46 |
| `adwd` | A Dance with Dragons | 73 |
