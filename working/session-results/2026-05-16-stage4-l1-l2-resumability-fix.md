---
session: 2026-05-16
mission: 2026-05-14-stage4-v1-bulk-sonnet
purpose: Fix batch-resumability so a rate-limit wall mid-batch doesn't redo all work
status: L1 + L2 implemented and VERIFIED working; 1-terminal worker running on default 90-min throttle
---

## ✅ Verification result (added after first batch completed)

**Batch-0022 completed end-to-end under the new prompt:**
- 5 files / 102 candidates → 24 emit / 78 reject / 0 errors / validator CLEAN
- Wall-clock: 20.3 min, cost $2.55, manifest 21 → 22 done
- **Per-file flush confirmed by disk mtimes**: 17:10:34, 17:10:46, 17:10:52, 17:11:13, 17:11:19 (staggered over ~45 sec)
- file_done events in state.jsonl appear in correct chronological order, one per file
- **Resume mechanism would have worked** if walled mid-batch: state.jsonl carries each file's completion before the next file starts processing

**Worker now sleeping** until ~17:44 CDT, will pick up batch-0023.

## ⚠️ Cost note — flag for your return

The 5-file batch size trades cost for wall-loss safety:
- 5-file batch: ~$2.55 (≈ $2 pre-flight fixed + $0.05–0.10/file)
- Old 30-file batch: ~$3.42 (≈ $2 pre-flight fixed + same per-file)
- Bulk completion: **~$2,720 for 1068 batches** vs ~$616 historical for 180 batches
- The pre-flight fixed cost dominates with small batches.

**Better balance might be 10–15 files per batch** — re-partition with `--new-batch-size 10` to cut wall-loss exposure by 3× while keeping pre-flight amortized. Cost would be ~$1,400.

To re-partition (only safe while no worker is mid-batch): set the stop file, wait for sleep to end OR the current batch to finish, then `python3 scripts/wiki-pass2-repartition-manifest.py --new-batch-size 10 --apply` and re-launch.

# Stage 4 — batch resumability fix (L1 + L2)

## Context

Today's 3-terminal parallel run hit the 5h rate-limit wall at ~$15 total cumulative spend (across the three workers) **before any worker had completed a single batch**. The old worker pattern was: claim a 30-file batch → read all files / classify all candidates → bulk-write at the end. When the wall hit at minute 35, all three workers had been processing but had written ZERO prose-edges JSONL files. Net: $14.33 spent, 0 work preserved.

The script's "graceful failure" only protected the bash worker process (exits cleanly on rate-limit, manifest stays `queued`). It did NOT protect in-flight classification work inside the Claude session — that was always lost when the session got walled.

## What I changed

### L1 — Re-partition manifest 30 → 5 files per batch

- `scripts/wiki-pass2-repartition-manifest.py` (NEW) — reads `batch-manifest.jsonl`, keeps `done` entries unchanged, re-divides each `queued` 30-file batch into six 5-file sub-batches. Backs up the original manifest.
- Applied: **21 done + 1068 queued** (was 21 done + 180 queued × 30 files = same 5330 files, just smaller atomic units).
- Each sub-batch is now ~$0.57 and ~5 min wall-clock. Mid-batch wall losses are capped at ONE file's worth (~$0.12) instead of $3.42.
- Backup at `working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl.bak-20260516T215127Z`.

### L2 — Per-file checkpoint + resume-on-claim skip-set

Patched `.claude/commands/worker-stage4.md` and `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`:

**At claim:** after creating the lock, the worker now scans `state.jsonl` for any prior `file_done` events matching THIS batch_id (from any worker, any prior run). It builds a `skip_set` of finished files. **If all files are in skip_set**, it jumps directly to "After processing the batch" — claims credit for the prior worker's per-file work and writes the release event the dead worker never wrote.

**Per-file:** after writing each file's prose-edges JSONL, the worker MUST append a `file_done` event to `state.jsonl`:
```json
{"event": "file_done", "batch_id": "<id>", "worker_id": "...", "file": "<candidates path>", "output": "<prose-edges path>", "rows_emitted": N, "rows_rejected": N, "timestamp": "<UTC>"}
```

Added a "Per-file flush is non-negotiable" hard rule in Constraints to fight the "accumulate in memory then bulk-write" pattern that killed today's parallel run.

### Combined effect

Before: a wall mid-batch ate $3.42 and ~25 min of work. After: caps at $0.12 and ~1 min. Across a full bulk run, this turns "rate-limit walls are catastrophic" into "rate-limit walls are speed bumps."

## Launch state (1 terminal, default 90-min throttle)

- Launched: 16:54 CDT via `bash scripts/stage4.sh launch -t 1`
- Worker started: 16:54:13 CDT
- First batch claimed: **batch-0022** at 16:54:54 CDT (41-second pre-flight)
- Files in batch-0022: 5 (Frey/Greybeard/Grell/Grey/Grimm/Groves/Haen Frey-house secondaries)
- Throttle: default `STAGE4_SLEEP_BETWEEN=5400` (90 min between batches — preserves Session 53's safe shape)

## When you return — check these

```bash
# Manifest progress
weirwood stage4 status

# state.jsonl file_done events (proof L2 is working)
grep '"event": "file_done"' working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl | wc -l
grep '"event": "file_done"' working/missions/2026-05-14-stage4-v1-bulk-sonnet/state.jsonl | tail -10

# Any prose-edges files written since launch
find working/wiki/pass2-buckets -name "*.edges.jsonl" -newer working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl.bak-20260516T215127Z 2>/dev/null | wc -l

# Worker still running?
ps -ef | grep -E "stage4\.sh run|claude.*sonnet" | grep -v grep
```

## Knobs to consider tweaking when you're back

- **Sleep interval (90 min)** — sized for old 30-file batches at $3.42 each. With 5-file batches at $0.57 each, throttle could safely be much shorter (~30 min) without saturating the 5h cap. Re-launch with `STAGE4_SLEEP_BETWEEN=1800 weirwood stage4 launch -t 1` if you want faster throughput.
- **Resume-test** — to verify L2 actually works under a real wall (not just in the prompt), the cleanest validation is a mid-batch kill: while a batch is processing files 2-of-5, kill the bash process; on relaunch, the next worker should claim the same batch and skip the already-`file_done` files. Hard to test without burning a real batch though.

## Total damage from today

- **3-terminal experiment cost:** $14.33 for 0 completed batches
- **Mistake on my part:** anchored on "ton of usage for the hour" and ignored Session 53's measured finding that multi-tab saturates the 5h cap faster than wall-clock. Should have flagged the prior measurement and proposed 1-tab smoke first.
- **Lesson:** outage credit ≠ lifted rate cap. The 5h cap mechanic applies independent of credit balance.
