---
session: DE-3 (occupies the S221 slot in Matt's global ledger; ran parallel with S220 UI-toggle)
date: 2026-07-18 → 2026-07-19 (overnight)
model: Fable 5 (orchestrator) · Haiku 4.5 (judge/audit subagents) · claude-opus-4-8 (extraction worker)
track: Dunk & Egg Pass-1
---

# Session DE-3 — v4 promoted, full run fired and completed, two harness bugs found and fixed

## Arrival state (undocumented)
The handoff expected "judge the THK smoke." On disk: Matt had already run BOTH smokes via CLI on
2026-06-23 (THK twice — first run 47k output tokens, second 107k; the on-disk file is the second; TSS
once) AND materialized split-A (`dunk-egg-scene-splitter.py` → 7/8/9 parts + `queue-parts.jsonl`).
None of it was logged — the F&B track (S198–S218) consumed every session between. First act was
reconstructing this from mtimes + telemetry.

## Judging → promote
Two cold Haiku `extraction-quality-auditor` judges (checklist from the continue prompt): THK 8/8 PASS
(73 relationship rows, 0 vocab violations, 5 SAME_AS, no checkpoint seams despite the double run),
TSS 8/8 PASS (54/54 rows). Orchestrator spot-check confirmed `(inferred)` is a sanctioned flag. v4
promoted without iteration. Fire-gate steps executed: worker graduated to `scripts/`, track registered
READY, split-A pinned (parts verified lossless — delta-0 words ×3), architecture.md principle #9
corrected (the free-text fossil; S131 Active Decision updated to LANDED).

## Infra: term-launch + the env-propagation finding
Matt asked for terminal-triggering from inside a session ("doesn't have to be iterm"). Built
`scripts/term-launch.sh`. Two findings worth remembering:
1. **`open -a Terminal` PROPAGATES the Claude Code session's environment** (CLAUDECODE, CLAUDE_CODE_*
   OAuth vars, ANTHROPIC_BASE_URL) into the launched app when it launches the app fresh — so even a
   "real terminal" window inherits the DE-1 401 contamination. The launcher therefore runs its payload
   under `env -i … /bin/zsh -lc` (fresh login shell rebuilds PATH; `claude` authenticates from Matt's
   own credentials). Proof chain: 0 contaminating env vars, then a live `claude -p` AUTH-OK probe.
2. **iTerm AppleScript needs one-time TCC consent** from the calling app; until granted the Apple Event
   times out. `--iterm` is opt-in; Terminal.app mode (no consent needed) is the default.

## Pre-fire bug: the 250-line validation floor
`_validate_output` required ≥250 lines — calibrated on whole novellas (smokes: 817/715 lines). Parts
average ~90–117 lines, so EVERY part-unit would have failed validation → crash-retry → longrun gives up
after 5. Fixed before firing: floor scales 250 (whole) / 60 (part) via the queue row's `unit_part`.

## The run (Matt's go: "Hit rate limit? Fire")
`term-launch → weirwood run start dunk-egg-pass1` (longrun.sh, LONGRUN_SLEEP_BETWEEN=600). 24 units,
avg ~8 min each, ~$51.10 total, THK 3,009 lines vs the 817-line whole-novella smoke (~3.7× fidelity —
the split-A argument confirmed empirically). One rate-limit wall at 23:10 self-healed after the 60-min
sleep. Zero crashes.

## Incident: the wall-lock false-complete (23/24)
The walled unit `tss-dunk-01-p08` was **silently skipped on every post-wall resume**, and the run
**false-exited 0 at 23/24** ("Queue drained"). Root cause, two defects compounding:
1. The worker's wall path `return 2`'d WITHOUT releasing the unit's lock file (the crash path did
   unlink it) — so every resume saw "claimed elsewhere, skip."
2. The end-of-loop "drained" check didn't compare against the manifest — pending-but-locked units
   fell through to `exit(0)`.
Both fixed: wall path unlinks the lock; the drained check now exits 10 with a loud warning naming the
stuck units. Stale lock cleared; the missing unit re-ran clean ($2.07). Detection credit: the iteration
count didn't add up (23 exit-10s + 1 exit-0 vs 24 queue rows) — the telemetry/manifest cross-check
caught what the supervisor log hid.

## Process lesson: three grep false-positives in a row
Three successive watcher scripts false-alarmed by grepping the longrun log for "crash"/"wall"/"giving
up" — ALL THREE strings appear in the supervisor's startup banner (`max_crashes`, `wall_sleep`,
`…before giving up`). The fix that stuck: stop grepping prose logs entirely; watch the manifest count +
supervisor pid liveness. Generalizable: match machine-formatted lines (`exit_code=`) or state files,
never free prose containing your keywords.

## Verify pass (run-plan §5, all three legs)
1. Deterministic validator: 24/24 pass (10,416 lines; 0 `NEEDS_VOCAB`; 59 `SAME_AS`).
2. Fresh Haiku audits: THK/TSS **PASS clean** — part-mode isolation held (Egg→Aegon only in the parts
   whose text reveals it; no training-knowledge leaks). TMK **PASS** with 4 epithet-SAME_AS rows
   flagged (`Dunk | SAME_AS | the Gallows Knight` — epithet vs concealed identity). NOT auto-deleted:
   epithets may be wanted as alias capture at graph-build. Left as DE-4 adjudication for Matt.
3. Harvest sidecar: 55 → 372 rows (THK 124/TSS 115/TMK 133). Format note: slash-delimited
   harvest-queue lines despite the `.jsonl` name; THK/TSS rows may partially duplicate the 55
   smoke-era rows — dedup at drain time.

## Numbers
- Extractions: 24 files, 10,416 lines, `extractions/mechanical/{thk,tss,tmk}/`
- Spend: ~$51.10 run (+ ~$12.40 Matt's June smokes incl. the duplicated THK)
- Wall-clock: ~7h50m + ~25 min recovery unit
- Artifacts: `JUDGE-{thk,tss}.md`, `AUDIT-{tmk,thk-tss}-full-run.md`, `manifest-v4.json`, telemetry
  ledger, per-unit stream logs, `working/logs/term-launch/` audit snippets

## Open at close
- DE-4 (Matt): adjudicate the 4 epithet rows → freeze `worklog-dunk-egg.md` to `history/`.
- Downstream (todos): D&E graph-build integration · harvest sidecar drain (dedup) · v4 locked-vocab
  back-port to the general `mechanical-extractor`.
