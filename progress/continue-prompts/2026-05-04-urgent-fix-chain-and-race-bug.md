# URGENT — Fix `weirwood --chain` terminal explosion + race condition

**Created:** 2026-05-04 (Session 33 incident response)
**Priority:** BLOCKER — no further extraction launches until both bugs are fixed
**Model:** Sonnet 4.6 (this is shell-script editing + a small lock-file pattern; do NOT use Opus)
**Estimated work:** 30–60 minutes for the script changes; +30 minutes if you also smoke-test before re-launching ACOK.

---

## Why this exists

Session 33 launched `weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain` and discovered two distinct bugs that compounded into a terminal-explosion event. Five iTerm tabs ended up running simultaneously, racing on the same waves, overwriting each other's extraction outputs. Wasted ~$19 in duplicated extractions plus uncounted in-flight calls killed during cleanup. See `working/session-details/session-033.md` for the full incident timeline.

**No more `--chain` launches until this is fixed.** Matt is also rightly tired of "terminal bullshit" — this is the second time this kind of thing has happened.

---

## The two bugs (both in `scripts/extract.sh`)

### Bug A — Terminal explosion

**Location:** `scripts/extract.sh:689-695` (the `--chain` block in `cmd_launch`).

**Symptom:** every spawned terminal independently re-launches `extract.sh launch -t N --chain`. With 2 starting terminals, after each delay you get 2 → 4 → 8 → 16 tabs.

**Root cause:** the chain command appended to every spawned terminal's command line is:

```bash
sleep <duration>
./scripts/extract.sh launch <book> -t <terminals> -w <waves_per> ... --chain
```

Every terminal does this. `extract.sh launch` then opens N more iTerm tabs. Combinatorial.

### Bug B — Race condition on `is_complete()`

**Location:** `scripts/extract.sh:117-127` (`is_complete`) + `cmd_run` main extraction loop (around line 383+).

**Symptom:** two terminals can both read "no extraction file exists" and BOTH start extracting the same chapter. Last-writing terminal overwrites the first. No lock, no atomic test-and-set, no claim file.

**Root cause:** `is_complete()` only checks for a *finished* file. There's no signal that another terminal has already *claimed* the chapter and is mid-extraction.

Even without Bug A, Bug B fires any time a user accidentally launches two extraction runs against overlapping waves. So Bug B must be fixed regardless of how Bug A is resolved.

---

## What to do

### Step 0 — Pre-flight

Verify no extraction processes are running:

```bash
pgrep -af "extract.sh"
pgrep -af "claude -p"
pgrep -af "sleep 7200"
```

If any return PIDs, STOP. Read session-033.md before doing anything else — `pkill -f` is the wrong tool here. The right tool is closing the iTerm tabs.

### Step 1 — Fix Bug A (chain explosion) — DECIDED: drop `--chain` entirely

Decision (Matt, Session 33 endsession): remove the `--delay` and `--chain` flags from `cmd_launch` and from `weirwood.zsh`. Update the help text. If hands-off pacing returns later, it'll be as a single coordinator process — not as every-terminal-relaunches.

**What to remove:**

- `scripts/extract.sh` — the entire `if [[ "$chain" == "true" && -n "$delay" ]]` block (lines ~690-696), the `--delay`/`--chain` argparse cases (lines ~616-617), the `delay`/`chain` locals, and the `parse_duration_to_seconds()` helper if no other caller uses it.
- `scripts/weirwood.zsh` — the `--delay`/`--chain` pass-through in the argparse loop, the auto-advance examples in the help blocks (`weirwood acok 2 1 --delay 2h --chain` references).
- Help text updates: drop the "Auto-advance" sections.

Verify nothing else in the repo references `--chain` or `--delay` for extract.sh:

```bash
grep -rn -- "--chain\|--delay" scripts/ working/ progress/ .claude/ | grep -v "wiki" | grep -v ".claude/agents/.git"
```

(The `wiki` filter excludes wiki-pass2.sh which has its own unrelated flags.)

### Step 2 — Fix Bug B (race on parallel extraction) — DESIGN: per-chapter status enum

Stronger than a `.lock` file: extend the existing stats CSV to be the **single source of truth** for per-chapter status. Each terminal claims a chapter by writing a `started` row before calling `claude -p`, and updates to `done`/`failed-*` on completion. Other terminals checking that chapter see the row and skip.

#### The enum

```
not_started     — no row in stats CSV (default)
started         — terminal claimed the chapter; claude -p call about to begin
working         — claude -p running; heartbeat updated every ~30s
done            — extraction complete and is_complete() == true
failed-rate     — claude -p hit rate limit (existing rejected-status detection)
failed-error    — claude -p returned non-zero exit, not rate-limit
failed-stale    — startup sweep found started/working row older than 30 min (terminal died)
skipped-done    — file already complete at claim time (renames existing skip-done)
skipped-claimed — another terminal holds started/working (replaces the lock-file path)
```

Existing CSV statuses (`ok`, `fail`, `skip-done`, `skip-no-source`, `skip-rate-limit`) map cleanly: `ok→done`, `fail→failed-error`, `skip-done→skipped-done`, etc. Migrate them in the same patch.

#### CSV schema change

Add two columns to `working/extraction-stats/extraction-stats-{book}-pass1-v3.csv`:

- `status` (existing column — values change per the enum)
- `last_heartbeat` (NEW — ISO8601 timestamp, updated by the running terminal every ~30s during `working` state)
- `terminal_id` (NEW — `${HOSTNAME}-${PID}`, so the user can tell at a glance which terminal owns a `working` row)

The header line (extract.sh:359) needs the new columns. Existing CSVs need a one-time migration: any row with `status=ok` becomes `status=done`; missing `last_heartbeat`/`terminal_id` cells stay empty.

#### Atomic claim via `flock`

`flock` is on macOS via Homebrew (`brew install flock`) — verify available before starting; if not present, fall back to `mkdir` on a `.claim` directory wrapping the CSV update (atomic).

Pseudocode at the top of each chapter loop in `cmd_run`:

```bash
# Acquire CSV lock for atomic read-modify-write
(
  flock -x 9
  current_status=$(awk -F, -v ch="$ch" -v wave="$wave" \
    '$1==ch && $3==wave {print $4}' "$STATS_FILE" | tail -1)
  current_heartbeat=$(awk -F, -v ch="$ch" -v wave="$wave" \
    '$1==ch && $3==wave {print $14}' "$STATS_FILE" | tail -1)

  case "$current_status" in
    done|skipped-done)
      claim_action="skip-already-done" ;;
    started|working)
      # Stale check: heartbeat > 30 min ago?
      if is_stale "$current_heartbeat"; then
        claim_action="claim-after-stale"
      else
        claim_action="skip-claimed-by-other"
      fi ;;
    ""|not_started|failed-*)
      claim_action="claim" ;;
  esac

  if [[ "$claim_action" == "claim"* ]]; then
    # Append a started row with terminal_id + heartbeat
    echo "$ch,$book,$wave,started,...,${TERMINAL_ID},$(now_iso)" >> "$STATS_FILE"
  fi
) 9>"${STATS_FILE}.lock"

case "$claim_action" in
  skip-already-done)    echo "⏭️  SKIP: $ch already done"; continue ;;
  skip-claimed-by-other) echo "⏭️  SKIP: $ch claimed by ${current_terminal_id}"; continue ;;
  claim|claim-after-stale) ;; # proceed to extraction
esac
```

Then run `claude -p`. After it returns:

```bash
# Update row to done/failed-*
(
  flock -x 9
  # Replace the started/working row for this chapter+wave with the final-status row
  python3 -c "<read CSV, find row, replace, write atomically via tempfile+rename>"
) 9>"${STATS_FILE}.lock"
```

Heartbeat updates during `claude -p` execution: spawn a background `( while sleep 30; do flock CSV; update_heartbeat; done ) &` and `kill` it when claude -p returns.

Trap on SIGINT/SIGTERM: write `failed-error` row (so the chapter doesn't get stuck in `started` forever).

#### Startup stale sweep

In `cmd_run` BEFORE the per-chapter loop:

```bash
# Sweep stale claims (terminals died without cleanup)
python3 scripts/extract-status-sweep.py "$STATS_FILE" \
  --heartbeat-max-age 90 \
  --row-max-age 1800
```

The sweep rewrites stale `started`/`working` rows to `failed-stale` so other terminals can re-claim. Two thresholds:

- **`--heartbeat-max-age 90`** (primary) — if `last_heartbeat` exists and is older than 90 seconds, the terminal is dead. Heartbeat updates every 30s during normal operation, so 90s = three missed heartbeats. Safe even for slow waves because liveness is what matters, not duration.
- **`--row-max-age 1800`** (fallback) — if the row was written more than 30 min ago AND has no `last_heartbeat` cell, the terminal died before writing its first heartbeat (within the first ~30s after claiming). Catches the early-death edge case.

Wall-clock age alone would false-positive on slow-but-running waves (longest observed ~38 min); heartbeat alone misses pre-heartbeat deaths. Combined, they cover both without flagging legitimate runs.

#### `weirwood <book>` status output

`cmd_status` already prints a wave table. Extend with conditional live mode:

- **If the CSV contains zero rows with `status = started` or `status = working`** (no run currently active): print the existing static wave/missing-chapters summary unchanged. Don't show per-chapter rows for `not_started` chapters — that's just clutter when no work is in flight.
- **If at least one `started` or `working` row exists** (a run is active): print the per-chapter status table for that wave/those waves only. Include terminal_id and heartbeat age.

Active-mode output:

```
Wave 6 — chapters 26-30 of 70
  acok-jon-01     done       (mac-12345, 4m 12s)
  acok-jon-02     working    (mac-67890, last heartbeat 14s ago)
  acok-jon-03     started    (mac-67890, claimed 23s ago)
  acok-jon-04     not_started
  acok-jon-05     failed-rate (mac-12345, retry after 19:30 UTC)
```

`failed-rate` rows include the `resetsAt`-derived retry timestamp, parsed at fail-time and stored in the CSV (low cost, high information value for "when can I re-launch").

This is the user-visible payoff: at a glance, Matt can see exactly what every terminal is doing while a run is active, and gets a clean static summary otherwise.

#### Migration of existing CSVs

Existing `extraction-stats-{book}-pass1-v3.csv` files (AGOT 73 rows, AFFC 46 rows, ACOK partial) have the OLD column set (no `last_heartbeat`, no `terminal_id`, no `retry_at`) and OLD status values (`ok`, `fail`, `skip-done`, `skip-no-source`, `skip-rate-limit`). The patched extract.sh expects the new schema, so first launch after the patch must migrate them.

**Auto-migrate at launch:**

In `cmd_run` BEFORE `mkdir -p "$STATS_DIR"`:

```bash
python3 scripts/migrate-stats-csv.py "$STATS_FILE"
```

The migration script:
1. Reads the existing CSV header. If it already has `last_heartbeat`, exit (already migrated).
2. Else: copy `${STATS_FILE}` → `${STATS_FILE}.bak` (backup, never overwritten on subsequent runs).
3. Rewrite the CSV: add `last_heartbeat`, `terminal_id`, `retry_at` columns (empty for existing rows). Rewrite status values: `ok`→`done`, `fail`→`failed-error`, `skip-done`→`skipped-done`, `skip-no-source`→`skipped-no-source`, `skip-rate-limit`→`failed-rate`.
4. Atomic rename (tempfile + `os.replace`) so a crashed migration doesn't leave a partial file.

After migration, all subsequent code can assume the new schema. The `.bak` files stay around forever — never deleted — as a safety net.

Verify on existing AGOT/AFFC/ACOK CSVs that the migration round-trips cleanly (same row count, same chapter slugs, statuses correctly mapped) before relying on it.

#### What's GAINED vs. simple lock-file

- **Visibility:** `weirwood <book>` becomes a live dashboard.
- **Stale recovery:** automatic, not a separate sweep step.
- **Audit:** the CSV is already preserved across sessions; bug history is permanent.
- **Single source of truth:** no separate `.lock` files to drift out of sync with the CSV.

### Step 2.5 — Terminal log cleanup (do in same patch)

The terminal output during a wave is currently noisy and unhelpful. Fix in the same patch since it's all in `cmd_run` (extract.sh:374-510 area).

#### Drop dollar amounts entirely

Token/cost reporting is misleading when usage-limit and context-window pressure are the real constraints, and dollar math from `cost_usd` doesn't cleanly capture either.

- **Per-chapter line:** drop the `$0.6259...` field. Print only `(269s | in:7 cache_create:40769 cache_read:163737 out:11545)`.
- **Wave summary:** drop the "Cost: $X.XXXX" line. Drop "Cost so far / Estimated remaining / avg $/chapter" from `cmd_status` (extract.sh:230-254).
- **Progress.md log line:** drop `, $X.XXXX` from the per-wave append (extract.sh:595-599).
- **Stats CSV:** keep the `cost_usd` column (low-cost, future-proof if we want it back), just stop printing it.

#### Drop the broken events/relationships/locations counters

The `0\n0 events | 0\n0 relationships` line is doubly broken: (a) the greps target an old schema, so they always return 0; (b) the `|| echo 0` fallback prints a second 0 on its own line. Just delete the whole "extraction summary from the output file" block (extract.sh:497-506) — keep only `n_lines`.

Replace with a single clean line: `📋 357 lines`. That's enough; the file is on disk and Matt can inspect it directly.

#### Phase the output into clear sections

Current flow is dense and hard to scan. Restructure each chapter's output into three labeled phases with blank-line separators:

```
─────────────────────────────────────────────────
Chapter 3 of 5: acok-arya-08
─────────────────────────────────────────────────

[1/3] Preparing
  Source:   sources/chapters/acok/acok-arya-08.md
  Output:   extractions/mechanical/acok/acok-arya-08.extraction.md
  Model:    claude-opus-4-6
  Started:  2026-05-04 16:41:58

[2/3] Extracting (claude -p running)
  <streaming claude output appears here — see below>

[3/3] Complete
  Duration: 231s
  Tokens:   in:6  cache_create:51,103  cache_read:110,964  out:10,386
  Output:   274 lines
```

Wave start/end banners similarly:

```
═════════════════════════════════════════════════
ACOK Wave 2 of 14 — chapters 6 to 10 of 70
Model: claude-opus-4-6
═════════════════════════════════════════════════
```

End-of-wave summary:

```
═════════════════════════════════════════════════
ACOK Wave 2 complete
═════════════════════════════════════════════════
  Succeeded:  5 / 5
  Failed:     0
  Wall time:  23m 34s
  Tokens:     888,436 in  /  60,584 out
```

#### Stream Claude's output during extraction

Yes — Claude is the actual extractor; surfacing its progress would be a huge UX win. The current code already requests `--output-format stream-json` and pipes to a tempfile (extract.sh:437-438). The fix: tee the stream-json to BOTH the tempfile (for parsing) AND a live extractor that pretty-prints assistant text blocks to the terminal as they arrive.

Cheapest implementation: wrap the `claude -p` call with a small Python streamer.

```bash
claude -p --dangerously-skip-permissions --model "$model" --verbose \
  --output-format stream-json "$prompt" 2>&1 \
  | tee "$jsonfile" \
  | python3 scripts/stream-claude-output.py
```

`scripts/stream-claude-output.py` reads stdin line-by-line, parses JSON, and prints to stderr (so it doesn't pollute the captured stdout):

```python
import json, sys
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    t = obj.get("type")
    if t == "assistant" and "message" in obj:
        for block in obj["message"].get("content", []):
            if block.get("type") == "text":
                # Indent so it's visually inside the [2/3] block
                for chunk in block["text"].splitlines():
                    print(f"  │ {chunk}", file=sys.stderr, flush=True)
            elif block.get("type") == "tool_use":
                print(f"  │ [tool_use: {block.get('name')}]", file=sys.stderr, flush=True)
    elif t == "result":
        # Don't print the raw result — extract.sh's existing parser handles it
        pass
```

Considerations:

- **stderr vs stdout:** the existing pipeline parses stdout for the JSON `result` event. Stream output to stderr so it doesn't get captured in `$jsonfile`. The `tee` keeps the JSON intact.
- **Verbosity (Matt-decided 2026-05-04):** stream EVERYTHING — full assistant text + tool_use lines. Yes, a 357-line extraction streams 357 lines, but Matt wants to know exactly where each terminal is at any moment. The `│ ` prefix makes it obvious where it begins/ends and visually distinct from the `[N/3]` framing. Terminal output is purely visual; it does NOT enter Claude's context, so verbosity is free.
- **macOS `tee` works fine** — no flags needed.
- **Cleanup:** kill the streamer python if `claude -p` is killed (the trap from the heartbeat updater can handle this — same pattern).

If the streaming proves too noisy in practice, a flag like `WEIRWOOD_QUIET=1` can suppress the streamer (just drop the pipe). Don't add that flag preemptively — see how it feels first.

**Smoke-test 1 — race condition (run in two iTerm tabs simultaneously):**

```bash
# Tab 1
weirwood acok 2 1 claude-haiku-4-5   # cheapest model is fine for smoke testing

# Tab 2 (immediately, while Tab 1 is running)
weirwood acok 2 1 claude-haiku-4-5
```

Expected: Tab 2 reads the CSV, sees Tab 1's `started`/`working` rows, prints `⏭️ SKIP: <ch> claimed by <terminal-id>`, writes `skipped-claimed` rows to the CSV. No file overwrites. `weirwood acok` mid-run shows the live status table with both terminals' current chapters.

**Smoke-test 2 — stale recovery:**

```bash
# Tab 1
weirwood acok 2 1 claude-haiku-4-5
# Wait until status shows "working" for some chapter
# Force-quit Tab 1's iTerm window (simulate kill -9)

# Wait 31 minutes (or temporarily set --max-age 60 in the sweep)

# Tab 2
weirwood acok 2 1 claude-haiku-4-5
# Sweep should rewrite the abandoned 'started'/'working' rows to 'failed-stale'
# Tab 2 should re-claim those chapters
```

Expected: stale rows promoted to `failed-stale`; chapters re-extract cleanly.

**Smoke-test 3 — chain removal:**

```bash
weirwood acok 2 1 --chain --delay 2h
```

Expected: error message about unknown flag, OR the flags are silently ignored (depending on implementation choice). Either way, no chain re-launch behavior.

### Step 4 — Re-launch ACOK

Once the fix lands, re-extract the remaining v2 chapters. As of session 33 end:

- Waves 1–4 v3 already in `extractions/mechanical/acok/` (re-extracted with the buggy chain — outputs are valid v3, just paid 2x for some).
- **Waves 5–10 still v2 in `extractions/archives/acok-v2-original-2026-05-04/`** — these are what need re-running.
- Waves 11–14 already v3 from Session 30.

Recommended re-launch:

```bash
weirwood acok 2 3 claude-opus-4-6
# 2 terminals × 3 waves = 6 waves = 30 chapters
# No --chain. No --delay. ~3-4 hrs wall-clock.
# When done, re-run for any remaining waves.
```

Pre-launch: confirm `weirwood acok` shows "Wave 5..10 missing" and not "1..4."

### Step 5 — Commit and update worklog

One commit for the script fix; a second commit (or amend) once the smoke-test is green. Update `worklog.md` Session 34 entry with the fix outcome. Delete this continue prompt only after the fix is in place AND ACOK has progressed cleanly through waves 5–10.

---

## Hard rules / DO NOT

- **DO NOT** re-launch ACOK with `--chain` until Bug A is fixed. The bug recurs deterministically.
- **DO NOT** re-launch ACOK without Bug B fixed either. Even one accidental double-launch will fire Bug B.
- **DO NOT** use `pkill -f "extract.sh"` or `pkill -f "sleep 7200"` to stop an in-flight run. The shell's `;` chain advances on each kill, spawning more tabs. The correct stop is `weirwood stop` (writes `/tmp/extraction-stop`) which terminals check between waves, OR closing iTerm tabs manually.
- **DO NOT** use Opus for this fix. Bash editing + `mkdir`-based locking is Sonnet/Haiku territory.
- **DO NOT** delete the existing v3 extractions in `extractions/mechanical/acok/`. They're valid (waves 1–4 are good v3, even if duplicated).
- **DO NOT** run `/endsession` without explicit Matt permission.

---

## Scope creep to AVOID

- Don't redesign the whole extraction pipeline. Two surgical bug fixes only.
- Don't add a database, message queue, or coordinator service.
- Don't switch to Python wrappers — `extract.sh` is fine, just needs the lock + chain fix.
- Don't refactor `weirwood.zsh` beyond removing flags if Option 1 is chosen.
- Don't try to recover the lost first-version extractions. They're gone, and the second-version is fine.

---

## Acceptance criteria

- [ ] `--chain` and `--delay` flags removed from `extract.sh` and `weirwood.zsh`. No grep hits for `--chain` outside of wiki-pass2 references.
- [ ] CSV schema extended with `last_heartbeat` + `terminal_id` columns; status enum migrated (`ok→done`, etc.).
- [ ] Existing AGOT/AFFC/ACOK extraction-stats CSVs migrated cleanly (no data loss).
- [ ] Atomic claim via `flock` (or `mkdir` fallback) implemented at top of each chapter loop.
- [ ] Heartbeat updater spawned during `claude -p` execution; killed on completion.
- [ ] `extract-status-sweep.py` script written; invoked at start of `cmd_run`; defaults `--heartbeat-max-age 90` (primary) + `--row-max-age 1800` (fallback for pre-heartbeat deaths).
- [ ] `cmd_status` (`weirwood <book>`) prints the per-chapter live table only when at least one row has status `started` or `working`; otherwise prints the existing static wave summary.
- [ ] `failed-rate` rows store the `resetsAt`-derived retry timestamp in a new `retry_at` CSV column; live status table renders it as "retry after HH:MM UTC".
- [ ] `scripts/migrate-stats-csv.py` written; invoked at start of `cmd_run`; auto-detects old schema, writes `.bak` backup, atomic rename. Round-trip verified on existing AGOT/AFFC/ACOK CSVs.
- [ ] Dollar amounts removed from per-chapter line, wave summary, status command, and progress.md log line. (Stats CSV keeps the `cost_usd` column.)
- [ ] Broken events/relationships/locations counter block (extract.sh:497-506) deleted; replaced with single `📋 N lines` line.
- [ ] Per-chapter output structured into `[1/3] Preparing` / `[2/3] Extracting` / `[3/3] Complete` phases with banner separators.
- [ ] Wave start/end banners use `═` separators with chapter range and model.
- [ ] `scripts/stream-claude-output.py` written; piped via `tee` so it doesn't pollute the JSON capture; output goes to stderr with `│ ` prefix.
- [ ] All three smoke tests pass (race, stale recovery, chain removal).
- [ ] `weirwood stop` still works.
- [ ] One or two commits on `main`. No commits with copyrighted content (sources/raw, sources/chapters, full-txt-files).
- [ ] After the fix lands AND ACOK waves 5–10 re-extracted: this continue prompt is deleted, todos.md updated, worklog Session 34 written.

---

## Files to read before editing

- `scripts/extract.sh` (the whole file is ~860 lines; relevant: 117-127, 329-604 for `cmd_run`, 606-717 for `cmd_launch`).
- `scripts/weirwood.zsh` (the wrapper; help text + flag pass-through).
- `working/session-details/session-033.md` (full incident timeline + lessons).
- `worklog.md` Session 32 entry (what the launch *intended* to be).
