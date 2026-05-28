# BEFORE-LEAVE-RESUME — Events Haiku bulk (paused 2026-05-28 16:26 CDT)

You soft-stopped the Events run before powering off. **It stopped cleanly. Nothing was lost.** This note is your "where was I" when you turn the computer back on.

## What's paused
The **Events Haiku bulk** typing pass (`pass1_events` → graph edges). Stopped at **batch 121/411**.

- **512 edges typed** (AGOT 236, ACOK 276), **4,367 rejected**, **4,879 rows done** of 16,502.
- **$14.93 spent** so far (projecting ~$50 total).
- All `typed_by=haiku`, **0 ASSAULTS**, validates @25/50/75/100 all OK (~0.90 reject). Healthy.
- Output dir: `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` (gitignored).

## Resuming is safe and picks up where it left off
Both **typed edges AND rejects** are written to disk and skipped on resume (`--skip-existing` matches on `(source, target, chapter)`). So **the ~4,879 done rows will NOT be reprocessed** — resume only works the remaining ~11,600.

**Relaunch command (drop sleep to 300s, SAME output dir):**
```
STAGE4_OUT=/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk \
STAGE4_SLEEP_BETWEEN=300 STAGE4_VALIDATE_EVERY=25 \
bash /Users/mnoth/source/asoiaf-chat/scripts/stage4-events-bulk-run.sh
```
Run this from your iTerm in `/Users/mnoth/source/asoiaf-chat`. At 300s pacing the remaining ~290 batches finish in roughly a day.

**To stop again later:** `touch /tmp/stage4-stop` (stops cleanly within ~1 batch + 60s; resume with the same command).

## When it finishes (owed work — gated on you for the merge)
1. **Precision read** (~25 emits) + **reject-recall check** (~25 random rejects; expect <~15% unique-edge recall loss).
2. **Slug long-tail triage** (`cat`/`wolf`/`others`/`gold`/`dragon`/`duck`/`bear` — mixed, decide per-class; don't blanket-drop).
3. **MERGE into `graph/edges/edges.jsonl`** — needs your before/after sign-off (never modified without it).

## Also still waiting on your OK (independent of this run)
3 core-cleanups to `edges.jsonl`: drop 2 `cersei↔tyrion` LOVES; retype ~22 physical `ASSAULTS`→`ATTACKS`; merge-time `OWNS→BONDED_TO` for direwolf/dragon targets.

## After Events (just so you remember the lay of the land)
Remaining unmined Pass 1 surfaces, by size: **Info** (~5,130 rows, who-knows-what), **Dialogue** (~4,422 rows, ~1/4 of Events — lowest yield), **Food** (~619), **Hospitality** (529 edges, already deterministic/$0, not yet merged). Best to merge Events first to calibrate whether ~85% Haiku enrichment is worth keeping before opening another surface.

---
*Full handoff: `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` · State: `worklog.md` (Session 78)*
