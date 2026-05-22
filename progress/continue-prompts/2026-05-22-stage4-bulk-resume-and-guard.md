# Stage 4 bulk — resume remaining batches + add single-instance guard (Session 65)

> **Recommended model: Sonnet 4.6** for the guard + relaunch + monitor ops. Opus 4.7 only for the post-run analyzer / any incident debug.

## State at end of Session 64 (trust worklog.md over this if they differ)
- Stage 4 Tier-1 (Option C, 222 batches) bulk RAN, then stopped. **60/222 distinct batches done.**
- On disk: **5,723 edge rows / 201 files** in `working/wiki/pass2-buckets/*/prose-edges-haiku/`. $55.66 Haiku spent.
- Prior schema output archived to `_archive/haiku-pre-bulk-enrich-2026-05-21/`. Current output is v163-enriched schema.
- **Incident:** a duplicate `run-forever` chain launched at 04:36 (PID 8471) alongside the 22:58 chain. Double quota burn exhausted the 5h window and hung Chain A's worker ~5h. Both stopped (Chain B via stop file, Chain A via SIGTERM). ~$15-20 wasted on ~26 redundant batches. No data loss. See `history/session-details/session-064.md`.
- Quality at batch ~16: 3.89% (healthy); ENCOUNTERS verb-gate working (1/2237); one bucket (`hightower-j-w`) had empty `evidence_section` (Haiku quirk, backfillable).

## DO THIS, IN ORDER

### 1. Guard against the dual-run incident recurring (BEFORE relaunch)
- Add a **single-instance guard** to `scripts/stage4-haiku-run-forever.sh`: on start, check a PID/lockfile (e.g. `working/missions/2026-05-19-stage4-haiku/.run-forever.lock`); if a live instance owns it, log + `exit 1`. Release on clean exit.
- **Fix the stop-file delete-race:** today both inner loops shared `/tmp/stage4-haiku-stop`; the first to detect it `rm`'d it, so the second kept running. Either (a) don't `rm` the stop file on exit (let the launcher clear it — the launch cmd already does `rm -f` at start), or (b) per-instance stop files. Pick (a) — simplest.
- Add a unit test for the guard if cheap. `python3 -m unittest discover tests` must stay green (90 tests).

### 2. Resume the remaining ~162 batches (Option C positions 61-222), SINGLE chain
- `--skip-existing` protects the 60 done (orchestrator skips files with existing output).
- **Confirm with Matt before launching** (standing rule `feedback_no_extraction_without_asking`). Launch ONE chain only.
- Launch (verify the guard works first): write/reuse `/tmp/launch-stage4-bulk.sh` (self-contained, absolute paths — do NOT inline a relative-path command into osascript; that caused 4 stray windows in S64). Same env: SLEEP=60, CHUNK=5, CONC=4, BATCH_LIST=option-c-batch-order.txt. The run-forever resumes; `--skip-existing` is applied per the loop's resume logic.
- Monitor ALERT-ONLY (S64 pattern): `tail -n 0 -F` the loop+wrapper logs, grep `rate.limit|ERROR|exited rc=|Files failed: [1-9]|Launching inner loop \(attempt [2-9]|All [0-9]+ batches complete|Stop file detected`. Do NOT alert on per-chunk `WARNING: claude exited non-zero` (self-heals via retry).

### 3. Analyzer for the completed output (can run in a separate window / Opus)
- Validate full corpus: concat `prose-edges-haiku/*.edges.jsonl` → `--file <concat> --graph-nodes graph/nodes` (NOTE: `--batch-id` mode fails — Haiku results JSON lacks `output_files` key; add that key as a cheap fix).
- Run the **`evidence_section` backfill**: for rows with empty `evidence_section`, join to enriched candidate on `source_slug+target_slug+edge_type`, copy `source_section`→`evidence_section`. Affects `hightower-j-w` + any later recurrences.

### 4. Commit
- Session 64 left 711 uncommitted working-tree changes (archive move + new edge files + worklog/session-detail). Commit them with a clear message. Verify `.gitignore` still excludes `prose-edge-candidates-enriched/`.

## DO NOT
- Launch more than one run-forever chain. Verify guard first.
- Modify the classify prompt / vocab without smoke evidence.
- Refetch wiki. Write to graph/nodes/. Run /endsession without explicit permission.
