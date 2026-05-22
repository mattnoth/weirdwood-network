# Session 64 — Stage 4 Tier-1 bulk launch + dual-run incident (2026-05-22)

**Model:** Opus 4.7 (launch + monitor ops; incident debug).

## What happened
Launched the Stage 4 Tier-1 (Option C, 222-batch) Haiku bulk run per the
`2026-05-22-stage4-bulk-relaunch` continue prompt. Confirmed SLEEP=60 / CHUNK=5 /
CONC=4 with Matt. Archived all prior Haiku output (89 buckets / 393 edge files →
`_archive/haiku-pre-bulk-enrich-2026-05-21/`, 363 v164 + 30 smoke) + prior mission
metrics, so the run regenerated cleanly under the current v163-enriched schema.

Launch took 5 attempts: I repeatedly pasted an osascript `CMD` that lacked the
`cd` prefix → 4 stray iTerm windows opening at `~` ("script not found"). Fixed by
writing `/tmp/launch-stage4-bulk.sh` (self-contained, absolute paths) and running
that. Lesson: for osascript-into-iTerm, never inline a relative-path command;
write a script file and verify its contents first.

## Quality checkpoint (batch ~16, 2237 rows)
3.89% validation rate (under 5% stop threshold; on par with v164 3.96% / Sonnet
4.3%). ENCOUNTERS verb-gate **working**: 1 failure in 2237 (~0.04%) vs smoke ~2%.
The lone cluster — 44 `bad-evidence-section` (empty `evidence_section`) — was
**entirely one bucket** (`hightower-j-w`): a Haiku output quirk, NOT an enrichment
gap (`source_section` is 0.0% empty across 76,009 candidate rows corpus-wide). Edges
themselves correct; deterministically backfillable post-run (join output→enriched
candidate on source+target+edge_type, copy `source_section`→`evidence_section`).
Recorded in `working/missions/2026-05-19-stage4-haiku/quality-check-batches-1-11-2026-05-21.md`.

## The incident: duplicate concurrent run → quota exhaustion → 5h hang
A **second `run-forever` chain launched at 04:36 AM** (PID 8471), separate from the
22:58 launch (PID 39197). Source unknown — I launched only once; the wrapper only
re-spawns its *inner* loop, never a new wrapper, so Chain B came from outside (Matt
re-pasting the command, or a stray window firing). Chain B restarted from the top of
Option C and **redundantly re-ran ~26 already-done batches**, overwriting their output.

Two chains burning quota in parallel 04:36–09:31 exhausted the 5h window. Chain A's
`batch-0409` worker then **blocked for ~5h** (claude CLI hung on the walled quota, near-zero
CPU, no output). The single rate-limit event Matt saw was a symptom. A single chain
would almost certainly have rolled through with LEVER 2 recovering normally.

**Stop:** stop file stopped Chain B cleanly (it won the delete-race and removed the file,
so Chain A kept running — the predicted single-stop-file race with concurrent loops).
Chain A's hung worker needed a graceful SIGTERM (`rc=143`); loop.sh then saw the
re-asserted stop file and exited. No `-9`, no data loss (hung batch wrote nothing).

## Final state
- 60/222 distinct batches done · 5,723 edge rows / 201 files · $55.66 Haiku (~$15-20 wasted on the duplicate).
- All processes down, stop file cleared, monitors stopped. Nothing committed.

## Follow-ups
1. **Single-instance guard** in `run-forever.sh` (PID/lockfile; refuse 2nd instance). Also fix
   the delete-race: don't `rm` the stop file on exit, or use a per-chain stop file.
2. **`evidence_section` backfill** script (post-run, deterministic).
3. Add `output_files` to the Haiku results JSON so `--batch-id` validation works
   (worked around via concat + `--file`).
4. Resume remaining ~162 batches (Option C positions 61-222) single-chain; `--skip-existing`
   protects the 60 done.
