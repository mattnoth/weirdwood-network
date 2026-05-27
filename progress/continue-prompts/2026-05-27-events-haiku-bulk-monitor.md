# Events Haiku bulk — monitor in-flight run, then validate + merge

> **Recommended model:** **Opus 4.7** — the work is judgment (precision spot-reads, drift interpretation, the merge/formalize decision + the 3 gated core-cleanups). Deterministic sub-steps (dedup, validators) can go to script-builder/Sonnet.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). State at write time: Session 77, 2026-05-27.

## What's running (started by Matt in his iTerm, Session 77)
- **Fresh all-Haiku** typing pass over the **16,502 cleaned `pass1_events`** candidate rows (`working/wiki/pass2-buckets/pass1-derived/_extra-tables/`, `candidate_kind=pass1_events`).
- Command: `STAGE4_OUT=.../_events-haiku-bulk STAGE4_SLEEP_BETWEEN=600 STAGE4_VALIDATE_EVERY=25 bash scripts/stage4-events-bulk-run.sh`
- Output: `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` (gitignored). Log: `…/_events-haiku-bulk/run.log`.
- ~411 batches @ ≤40 rows, 600s between batches → **~3.5 days**. Auto-resumes rate-limit walls (exit 42 → 1h sleep); **hard-stops on drift (exit 43)**; `touch /tmp/stage4-stop` or Ctrl-C stops cleanly + resumable via `--skip-existing`.
- Model = Haiku (`claude-haiku-4-5-20251001`), `prompt_version=v5-precision-rules`. Validated pre-run at **~85% (AGOT) / ~90% (ACOK) strict** across 2 fresh samples. Report: `working/session-results/2026-05-27-haiku-vs-sonnet-events.md`.

## Your job — MONITOR (while it runs)
1. **Read `run.log`.** Healthy: each batch ~90% reject, ~$0.10-0.18, then `sleeping 600s before next batch...`. The automated `validate@batch N: ... reject_rate=.. OK` line prints every 25 batches.
2. **Precision spot-read owed at:** the first flush (~batch 5), the first validate checkpoint (~batch 25), and at completion. Method: pull emitted edges, check `edge_type` vs `evidence_quote`. **Bar = EDGE CORRECTNESS** (is the relationship right?) — do NOT down-flag an edge merely because the cited quote is less-than-verbatim (Matt's S77 calibration). Read tool: `python3` over `_events-haiku-bulk/**/*.edges.jsonl`.
3. **If you see `DRIFT HALT (exit 43)`** in the log: the run stopped itself (reject-rate <0.70 or schema break). Inspect `_events-haiku-bulk/` + the run.log validate line; diagnose before any resume.
4. **Sleep change (only if Matt asks):** stop (`touch /tmp/stage4-stop`), wait for clean exit, relaunch SAME command with a new `STAGE4_SLEEP_BETWEEN` and the **same `STAGE4_OUT`**.

## Your job — on COMPLETION (run.log shows "mission complete")
1. **Full validation:** total typed/rejected/failed, cumulative reject-rate, cost; a final ~25-emit strict precision read; confirm `typed_by=haiku` throughout.
2. **Slug long-tail triage** (deferred from S77, NOT garbage — mixed): `cat`(62) `wolf`(36) `others`(30) `gold`(24) `dragon`(23) `duck`(23) `bear`(18). `others`=White Walkers is CORRECT; `duck`=Rolly Duckfield + `gold`=City Watch are correct referents with MISSING nodes; `cat/wolf/dragon/bear` are mixed. Decide per-class: drop / remap / create-node — do NOT blanket-drop (loses real edges).
3. **MERGE / FORMALIZE into `graph/edges/edges.jsonl`** — the gated milestone. Sub-steps: dedup (same `(source,target,chapter)` collapses; the run already de-dups within the typing pass but cross-check); apply merge-time `OWNS→BONDED_TO` for direwolf/dragon targets (core-cleanup #3); run the type-contract validator; **before/after edge counts to Matt for sign-off** (do NOT modify `edges.jsonl` without it).

## DO NOT
- Modify `graph/edges/edges.jsonl` without Matt's before/after sign-off.
- Touch the Sonnet baseline `_events-run-20260527/` or the two cmp dirs (`_events-haiku-cmp-20260527/`, `_events-haiku-cmp2-acok-20260527/`).
- Re-run candidate generation (candidates are fixed + clean; backup at `_extra-tables.pre-slugfix-20260527/`).
- Run `/endsession` without explicit permission.

## Also gated on Matt (carried from S76 — independent of this run)
3 core-cleanups to `edges.jsonl`, await before/after sign-off: (1) drop 2 `cersei↔tyrion` LOVES mis-types; (2) retype ~22 physical `ASSAULTS`→`ATTACKS` (+ fix the spine phrase→type map; `ASSAULTS`=sexual only, architecture.md:233); (3) merge-time `OWNS→BONDED_TO` (folds into the merge above).

## Watcher note
This run logs to `run.log`, NOT a mission-manifest, so `/watcher` (mission-protocol) does not directly apply. Lightweight monitoring = read `run.log` + the `_events-haiku-bulk/**/*.jsonl` tallies. If formal watcher-style monitoring is wanted, that's a small follow-up (wire the run as a working/missions/ entry) — not required.
