# Session 12 — AGOT v3 Completion, Rate-Limit Detection, Commit Catchup (2026-04-25)

## Context

Matt came in with a wall of terminal output from overnight extraction runs. Three iTerm terminals had been running AGOT v3 waves in parallel. The 5-hour Opus rate limit hit around 11:40pm CT, killing waves mid-run. The script had no rate-limit awareness and kept spawning new claude sessions that instantly failed.

## What Happened

### Diagnosis

Parsed the terminal output to reconstruct what happened:
- **Terminal 1** (waves 7-8): Wave 7 succeeded (5/5). Wave 8 — all 5 failed (Eddard 3-7).
- **Terminal 2** (waves 9-10): Wave 9 succeeded (5/5). Wave 10 — Eddard 13 wrote its extraction before the limit killed it, then Eddard 14-15 + Jon 1-2 failed instantly.
- **Terminal 3** (waves 11-12): Wave 11 succeeded (5/5). Wave 12 — Jon 8 wrote its extraction before dying, then Jon 9 + Prologue + Sansa 1-2 failed instantly.

Key insight: two chapters (Eddard 13, Jon 8) actually completed their Write tool call before the rate limit hit on the *next* API call. The `is_complete` check catches these correctly — they have full content and all required sections.

### Rate-Limit Detection (extract.sh)

Added detection after each chapter failure: checks JSON output for `"status":"rejected"` + `"rateLimitType"`. When detected:
- Prints the limit type and reset time (parsed from `resetsAt` timestamp)
- Marks remaining chapters as `skip-rate-limit` in the stats CSV
- Breaks out of the wave loop immediately

This prevents the cascade of 4 instantly-failing sessions that burn $0 each but clutter the logs.

### Extract.sh UX Improvements

- Replaced `tail -3` raw preview (confusing — showed random text fragments that looked like incomplete data) with structured summary: line count, table rows, events, relationships
- Added emoji indicators: ✅ ❌ 🚫 ⏭️ 🔄 ⚠️ for visual scanning across parallel terminals
- Removed the raw JSON dump on failures (was 10 lines of noise)

### AGOT v3 Completion

Matt ran `weirwood agot 6 1` (6 tabs, 1 wave each) to finish the remaining 26 chapters. All 6 waves completed successfully. Final validation:
- 73/73 files on disk
- All pass schema validation (18 required sections + 12 raw entity headers)
- 1 minor gap: `agot-eddard-01` missing `### Other` header in Raw Entity List
- Line counts: min 234, max 395, avg 290
- Total cost: ~$49 across 92 attempts (includes rate-limit retries), avg $0.53/chapter

### Extraction Rule Strengthened

Updated memory (`feedback_no_extraction_without_asking.md`) to be unambiguous: ALL extractions must be triggered by the user. No exceptions, no single chapters, no background agents, no inline delegation. The orchestrator provides commands — the user executes them.

### Commits

Caught up on all uncommitted work from sessions 8-12 in three logical commits:
1. **Infrastructure** (sessions 8-11): architecture refactor, v3 prompt, tooling, session docs, stale file cleanup (27 files)
2. **Extraction tooling**: extract.sh + weirwood.zsh with rate-limit detection, emojis, stats (4 files)
3. **AGOT Pass 1 v3**: all 73 extractions + archived prior versions + stats CSVs (199 files)

## Decisions

- Rate-limit detection halts the wave, not the terminal — the stop-file mechanism handles cross-wave halting
- Emoji output in extract.sh: visual, not semantic — no emoji in extraction content
- Extraction summary replaces raw preview: structured counts from the output file
- Stat CSVs from all versions (v1, v2, v3) kept as historical record
- ACOK is next but not started — Matt will trigger manually next session

## Anomalies / Notes

- The "92 chapters" in the cost summary includes retries from rate-limited waves that partially ran before failing — the CSV has rows for those attempts
- Eddard-01 missing `### Other` header is a cosmetic gap in the first chapter extracted under v3; all other 72 have it
- Food & Drink section headers are consistent across all 73 files; Matt's observation about "rich food & drink" was from the old preview lines, not the extraction content
