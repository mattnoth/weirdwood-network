# Pass 1 Auto-Advance Mode — Multi-Batch Extraction with Delays

## What This Does

Spreads a multi-wave extraction run across multiple API usage windows by automatically waiting between batches before launching the next one. Useful for long runs (50+ chapters) where you want to avoid hammering the API in a single session.

**Example:** ACOK re-run (50 chapters = 10 waves)
```bash
weirwood acok 2 1 --delay 2h --chain
```
- Waves 1-2 run (2 terminals in parallel)
- Wait 2 hours
- Auto-launch waves 3-4
- Wait 2 hours
- Continue: 5-6, 7-8, 9-10
- Total: ~10 hours wall-clock across ~5 sessions

## Syntax

```bash
weirwood <book> <terminals> <waves> --delay <duration> --chain
```

| Param | Required? | Example | Meaning |
|-------|-----------|---------|---------|
| `<book>` | Yes | `acok` | Book code |
| `<terminals>` | Yes | `2` | Number of iTerm tabs |
| `<waves>` | Yes | `1` | Waves per terminal per batch |
| `--delay` | Yes (with `--chain`) | `2h`, `30m`, `120s` | Wait time between batches |
| `--chain` | Yes (with `--delay`) | (flag) | Auto-advance to next batch |

## Duration Formats

- `2h` → 2 hours (7200 seconds)
- `30m` → 30 minutes (1800 seconds)
- `120s` → 120 seconds
- `1h 30m` → NOT supported; use `90m` instead

## How It Works

1. **First batch launches immediately:**
   ```
   Terminal 1: wave 1
   Terminal 2: wave 2
   ```
   (~30 min for ACOK, 2 terminals, 1 wave each = 5 chapters per terminal)

2. **After both terminals finish:**
   - Waits for `--delay` duration (2 hours)
   - Auto-launches next batch (waves 3-4)
   - Repeats until no incomplete waves remain

3. **Automatic exit:** When all waves complete, the script exits cleanly.

## Monitoring

### During the run:

```bash
# Check what's currently extracting
ps aux | grep "extract.sh run"

# Check progress so far
tail -20 history/worklog-archives/extraction-progress.md

# Check token/cost stats
tail -10 working/extraction-stats/extraction-stats-<book>-pass1-v3.csv
```

### Between batches (during the wait):

```bash
# Current extraction progress
weirwood <book>

# Sample a random extraction from the completed batch
head -50 extractions/mechanical/<book>/<chapter>.extraction.md
```

## Stopping

If you need to halt mid-run:

```bash
weirwood stop
```

This creates a marker file (`/tmp/extraction-stop`) that the running terminal checks between waves. It never interrupts a wave mid-chapter — the current wave finishes, then the terminal sees the marker and exits.

**Important:** The next batch will NOT auto-launch if you use `weirwood stop`. You must manually relaunch:

```bash
# After aborting a run, resume from the next incomplete wave
weirwood <book> <terminals> <waves> --delay <duration> --chain
```

## Soft vs. Hard Stop

| Type | Command | Behavior |
|------|---------|----------|
| Soft stop | `weirwood stop` | Current wave finishes, terminal exits, next auto-advance does NOT happen |
| Hard stop | (Ctrl+C in terminal) | Immediate terminal kill, mid-wave loss possible, next batch auto-advances after delay anyway |

**Use soft stop** (`weirwood stop`) for graceful halting. Avoid Ctrl+C unless truly stuck.

## Examples

### ACOK re-run: 50 chapters, 2h waits between batches

```bash
weirwood acok 2 1 --delay 2h --chain
```

Runs waves 1-2 (~30 min), waits 2h, runs 3-4, waits 2h, ... finishes at waves 9-10.
**Total wall-clock:** ~10 hours across 5 API sessions.

### Slower book with longer waits: ASOS (82 chapters), 3h waits, 1 terminal

```bash
weirwood asos 1 1 --delay 3h --chain
```

Runs wave 1 (5 chapters, ~15 min), waits 3h, runs wave 2, ... continues until done.
**Total:** 17 waves × 3h waits = ~51+ hours wall-clock, but ultra-safe on API limits.

### Faster mode: smaller waits, more terminals

```bash
weirwood adwd 4 2 --delay 1h --chain
```

Runs waves 1-8 in parallel (4 terminals × 2 waves = 8 waves = 40 chapters), waits 1h, continues.
**Total:** Faster, but higher concurrent API load.

## Cost Considerations

Each batch consumes tokens based on:
- Number of chapters (terminal count × waves per terminal × 5 chapters/wave)
- Model used (Opus is default; Sonnet is cheaper)
- Cache hit rate (subsequent chapters reuse cached prompts)

**Example: ACOK waves 1-2 (10 chapters) at Opus:**
- Typically $2-3 for 10 chapters (including cache hits)
- 5 batches for 50 chapters = $10-15 total

View stats:
```bash
cat working/extraction-stats/extraction-stats-acok-pass1-v3.csv | tail
```

## Troubleshooting

### Batch doesn't auto-advance after waiting

**Symptoms:** Delayed 2 hours, but no new iTerm tab opens.

**Causes:**
1. Previous batch failed silently → use `weirwood stop`, then manually relaunch
2. Script crashed → check terminal for error messages
3. Rate limit hit → script paused and awaits manual intervention

**Fix:** Manually check progress and relaunch:
```bash
weirwood <book>  # See which waves remain
weirwood <book> 2 1 --delay 2h --chain  # Relaunch
```

### One terminal finished before the other

**Normal.** If Terminal 1 finishes wave 1 in 10 min and Terminal 2 finishes wave 2 in 20 min, both sit idle until BOTH complete. Then the delay timer starts and the next batch launches.

### Hit a rate limit during a batch

**Automatic handling:** The script detects rate limits mid-wave, halts immediately, and reports the reset time. The batch does NOT auto-advance — you must manually relaunch when ready:

```bash
weirwood <book> 2 1 --delay 2h --chain
```

The script will skip already-completed waves and continue from the incomplete one.

## See Also

- `README.md` — Command reference and overview
- `mechanical-extraction-howto.md` — General Pass 1 workflow
- `.claude/agents/mechanical-extractor.md` — Agent prompt (12-category schema)
