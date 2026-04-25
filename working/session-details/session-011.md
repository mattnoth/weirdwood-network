# Session 011 — Extract.sh Instrumentation: Worklog Auto-Update & Versioned CSV

**Date:** 2026-04-24
**Type:** Infrastructure / tooling improvement
**Duration:** Short session

## Context

Matt had run 6 waves of AGOT v3 extractions (30/73 chapters) via the `weirwood` terminal pipeline between sessions. When he asked for a status report, Claude read `worklog.md` — which still said "0/73 — ready for fresh run" — and reported stale data. The actual progress was visible in the filesystem (30 extraction files) and in `working/progress.md` (6 wave entries), but the worklog hadn't been updated because nothing automated that step.

Matt pointed this out: the extraction script should update the worklog automatically so that a new Claude session (or a session-limited continuation) comes in informed.

## What Changed

### 1. Versioned CSV paths

The extraction stats CSV was a single flat file (`working/extraction-stats.csv`) that accumulated rows across prompt versions. This made it hard to archive a run's stats alongside its extractions, and when a new session started it couldn't tell v2 data from v3.

**Change:** `extract.sh` now derives the stats path from book/pass/version:
```
working/extraction-stats/extraction-stats-{book}-{pass}-{version}.csv
```

The existing CSV was split: 30 rows from Apr 23 (v2 run) moved back to the v2 CSV, 51 rows from Apr 24 (v3 run) stayed in the new v3 file.

Variables `PASS="pass1"` and `VERSION="v3"` are set at the top of `extract.sh`. These will need manual update when the pass/version changes — acceptable since prompt version changes are deliberate.

### 2. Worklog auto-update after each wave

New `update_worklog()` function in `extract.sh`:
- Counts completed extractions from the filesystem (same `is_complete` check the status command uses)
- Identifies which waves are fully done
- Sed-updates the matching `Pass 1 v3 run on {BOOK}` line in `worklog.md`
- Called at the end of every `cmd_run` invocation, right after the progress.md append

This means after every wave completes, `worklog.md` reflects reality. A new Claude session reading the worklog will see accurate progress.

### 3. Manual worklog update this session

Updated the stale "0/73" line to "30/73 — waves 1, 2, 3, 4, 5, 6 complete" to reflect current state.

## Decisions

- **Single PASS/VERSION at script top, not per-invocation flags:** Prompt version changes are rare and deliberate. Hardcoding at the top is simpler than adding CLI flags. The developer (Matt) updates these when the prompt changes.
- **Worklog update uses filesystem truth, not CSV:** The `is_complete` function checks the actual extraction file (exists, >100 lines, has required sections). This is the same check the status command uses. More reliable than counting CSV rows.
- **extraction-status.sh also updated** to use the new per-book CSV path.

## No Surprises

Straightforward infrastructure change. The v2/v3 CSV split was clean — dates clearly separated the runs.
