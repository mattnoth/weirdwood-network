# Stage 4 Events Haiku Bulk Run — Runbook

Unattended multi-day run typing 16,502 `pass1_events` candidate rows via
`stage4-tail-classifier.py` on Haiku (`claude-haiku-4-5-20251001`).

---

## One-liner to start in iTerm

```
STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 bash /Users/mnoth/source/asoiaf-chat/scripts/stage4-events-bulk-run.sh
```

Run this from any working directory; the script resolves paths relative to the repo root automatically.

---

## Where output lands

- **Output dir:** `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk-YYYYMMDD/`
  (datestamped at start; override with `STAGE4_OUT=/path/to/dir` env var)
- **Log:** `$OUT/run.log` — full stdout/stderr from every classifier invocation
- **Typed edges:** `$OUT/{book}/{book}-tail.edges.jsonl`
- **Rejected:** `$OUT/{book}/{book}-tail.rejected.jsonl`
- **classify_failed:** `$OUT/{book}/{book}-tail.classify_failed.jsonl`
- **Run summary:** `$OUT/run-summary.json`

---

## How to stop it cleanly

### Option A — stop-file (recommended for unattended runs)

```bash
touch /tmp/stage4-stop
```

Takes effect within **one batch + up to 60s** — whichever comes first:
- The classifier checks the stop-file between every 30s sleep chunk mid-sleep.
- The classifier also checks between batches (even when `--sleep-between 0`).
- The wrapper checks the stop-file immediately after the classifier returns.
- The wrapper's `sleep_with_stop_check()` also checks every 60s during wall/crash sleeps.

Both the classifier and wrapper exit cleanly with flushed output.
The wrapper removes `/tmp/stage4-stop` automatically when the loop exits.

### Option B — Ctrl-C

Sends SIGINT to the classifier. The classifier's signal handler sets a flag that
fires after the current batch, flushes partial output, and exits with code 130.
The wrapper treats exit 130 as **TERMINAL** — it logs "interrupted by signal —
stopping (not relaunching)" and exits. `--skip-existing` will resume from where
you left off.

---

## Resuming after stop

```bash
STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 bash scripts/stage4-events-bulk-run.sh
```

`--skip-existing` is always passed to the classifier. Rows already written to
the output dir are skipped deterministically — no re-processing.

**Important:** The output dir is datestamped at the time the wrapper first starts
(`_events-haiku-bulk-YYYYMMDD`). If you stop on day N and resume on day N+1, the
default `STAGE4_OUT` will produce a **new datestamped dir** and start fresh.
To continue the same run, pass the same output dir explicitly:

```bash
STAGE4_OUT=/path/to/asoiaf-chat/working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk-20260527 \
  STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 \
  bash scripts/stage4-events-bulk-run.sh
```

---

## Sleep-change procedure

Matt will lengthen `STAGE4_SLEEP_BETWEEN` when running concurrently with heavy
interactive (Opus) use, then shorten it before travelling.

**To change the inter-batch sleep:**

1. Stop the current run:
   ```bash
   touch /tmp/stage4-stop
   ```
   Wait for the current batch to finish (watch the log: `tail -f $OUT/run.log`).

2. Re-launch with the new sleep and the SAME output dir:
   ```bash
   STAGE4_SLEEP_BETWEEN=1800 STAGE4_OUT=/path/to/existing/dir \
     STAGE4_VALIDATE_EVERY=25 \
     bash scripts/stage4-events-bulk-run.sh
   ```
   `--skip-existing` will pick up exactly where it left off.

**Recommended pacing values:**
| Scenario | `STAGE4_SLEEP_BETWEEN` |
|----------|----------------------|
| Concurrent with heavy Opus interactive use | `1800` (30 min) |
| Unattended overnight / no other Claude usage | `600` (10 min) |
| Burst (use the `stage4-tail-bulk-forever.sh` predecessor instead) | `0` + no inter-batch sleep |

---

## Exit code map

| Code | Meaning | Wrapper action |
|------|---------|---------------|
| 0    | Normal completion (or no rows remaining after --skip-existing) | Check remaining rows; stop if 0, loop if >0 |
| 42   | Rate-limit wall detected (N consecutive all-classify_failed batches) | Sleep `${STAGE4_WALL_SLEEP:-3600}s` (1h default) with stop-file check every 60s, then resume |
| 43   | Drift halt — output schema or reject-rate anomaly detected | **DO NOT auto-resume.** Wrapper stops with loud alert. Inspect output before retrying |
| 130  | SIGINT / SIGTERM / stop-file inside classifier | **TERMINAL** — wrapper logs "interrupted by signal" and exits. Does NOT relaunch |
| other | Crash | Sleep 300s (chunked, stop-file aware), retry up to 5 consecutive crashes then give up |

---

## Pacing defaults

| Env var | Default | Meaning |
|---------|---------|---------|
| `STAGE4_SLEEP_BETWEEN` | `600` | Seconds to sleep between batches (inside the classifier, chunked 30s for stop-file responsiveness) |
| `STAGE4_VALIDATE_EVERY` | `25` | Run drift-detection validation every N batches |
| `STAGE4_WALL_SLEEP` | `3600` | Seconds to sleep after a rate-limit wall (exit 42) |
| `STAGE4_MAX_ITER` | `200` | Maximum loop iterations before giving up |

---

## Checking progress

```bash
# Count done keys (emit + rejected)
python3 - <<'EOF'
import json
from pathlib import Path
out = Path("working/wiki/pass2-buckets/pass1-derived")
for d in sorted(out.glob("_events-haiku-bulk-*")):
    emits = rejects = failed = 0
    for f in d.rglob("*.edges.jsonl"):
        emits += sum(1 for l in f.read_text(errors="replace").splitlines() if l.strip())
    for f in d.rglob("*.rejected.jsonl"):
        rejects += sum(1 for l in f.read_text(errors="replace").splitlines() if l.strip())
    for f in d.rglob("*.classify_failed.jsonl"):
        failed += sum(1 for l in f.read_text(errors="replace").splitlines() if l.strip())
    total = emits + rejects + failed
    print(f"{d.name}: emit={emits} reject={rejects} failed={failed} total={total}")
EOF
```

Total candidate rows = 16,502. Subtract total from 16,502 to get remaining.

---

## Drift halt recovery

If the wrapper stops with exit 43 (DRIFT HALT):

1. Check `$OUT/run.log` — the `DRIFT HALT:` line explains the specific reason.
2. Common reasons:
   - `reject_rate=X < floor=0.70` — Haiku started over-emitting. Review recent `*.edges.jsonl` rows.
   - `out_of_vocab=N` — An edge type not in the locked vocab appeared (structural bug).
   - `schema_violations=N` — A required field is missing from emit rows.
3. If the output looks okay and the halt was a false alarm (e.g., early batches before
   the rate check has enough data), adjust `--reject-rate-floor` downward or increase
   `--validate-every` and re-run with `--skip-existing`.
4. To resume after fixing: re-run the wrapper with `STAGE4_OUT=...` pointing to the
   same output dir (`--skip-existing` picks up exactly where it left off).
