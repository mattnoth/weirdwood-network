---
session: 77
date: 2026-05-27
model: Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×3
title: Haiku-vs-Sonnet Events decision → candidate slug fix → paced runner built + hardened → bulk LAUNCHED
---

# Session 77 — Events enrichment: model decided (Haiku), candidates fixed, run launched

## Purpose
Inherited `progress/continue-prompts/2026-05-27-haiku-events-comparison.md`: run the SAME first 600 Events rows on Haiku, diff vs the paused Sonnet run, decide the model for the remaining ~82%. The session went well past that — it picked the model, fixed the surfaced root cause, built + hardened the run apparatus, and started the bulk.

## 1. The Haiku-vs-Sonnet comparison (sample 1, AGOT 600)
- Built `scripts/stage4-model-run-diff.py` — diffs two classifier runs on the SAME candidate rows. **Match key = `(source_slug, target_slug, evidence_chapter, hint_raw)`** — NOT the continue prompt's proposed `evidence_ref`, which only exists on emit rows (rejected/classify_failed rows lack it). Self-diff (Sonnet vs Sonnet) = 100% agreement, validating the tool.
- **Caught a real bug before it cost anything:** `--smoke N` was silently ignored under `--input-dir` (gated on `args.input_dir is None`, classifier line 1613). The first launch started the FULL 415-batch bulk on Haiku, not a 600-row smoke. Killed at batch 1 ($0.00 — the `claude -p` child was SIGTERM'd mid-flight). Fixed (sequential truncation for input-dir mode) + regression test.
- Result: Haiku **~85% strict** (hand-read of all 59 emits), 87.8% verdict agreement, 0 walls, $1.83. The over-emit bucket (21) was NOT 21 errors — ~4 were edges Haiku caught that Sonnet wrongly rejected, ~12 true-but-momentary TRAVELS_WITH, ~5 weak. Haiku's real cost vs Sonnet is **recall** (40 misses), not pollution — the *acceptable* failure mode per project values.

## 2. Decision + 2nd validation (ACOK 600, out-of-sample)
- Matt chose "2nd validation first" (his ≥2-fresh-samples policy). Ran Haiku on first 600 ACOK rows (`--book acok`), a different book.
- **~90% strict** (hand-read of all 65 emits), 84.8% agreement, 0 walls, $1.80. Stable / slightly better than sample 1.
- **Cross-cutting finding:** residual errors in BOTH samples were dominated by **bad candidate slugs**, not Haiku misclassification — `lord-tywin` (resolves to a ship artifact, not the man), `four-storms` ("Four brothers"), `bastard`/`dog`/`hunt-of-the-poor-fellows` (common words → title/species/event nodes). These PASS the existence/slug-quality gate because they resolve to *real* (wrong) nodes, and a merge-time orphan filter wouldn't catch them either — it's a *disambiguation* problem, not a *validation* one.
- **Decision: Haiku for the full run.** Matt then chose "fix candidates first" over "run now, fix at merge."

## 3. Candidate slug-disambiguation fix
- Root cause (script-builder): `stage4-pass1-extra-tables.py` never passed `slug_category` to the resolver, so the S72/v1.3 title-person rung (`_resolve_char_restricted`) never fired — "Lord Tywin" exact-matched the ship slug. Plus a bootstrap present-slugs seeding bug.
- Fix: wire `slug_category` through `_scan_text_for_entities` + `_build_present_slugs` + all generator call sites; add a small explicit `ENDPOINT_BLOCKLIST` (`bastard`, `dog`, `four-storms`, `hunt-of-the-poor-fellows`).
- Regenerated candidates: pass1_events **16,572 → 16,502**; all 5 bad-slug classes → 0 (`lord-tywin`: 44 remapped to `tywin-lannister`, 15 dropped). Backup `_extra-tables.pre-slugfix-20260527/`.
- New collision classes surfaced (`cat` 62, `wolf` 36, `others` 30, `gold` 24, `dragon` 23, `duck` 23, `bear` 18) — **deliberately NOT blocklisted**: they're MIXED (real refs + a few wrong; `duck`=Rolly Duckfield, `gold`=City Watch, both missing nodes; `others`=White Walkers is correct). Blanket-dropping would delete real edges → defer to merge-time triage.

## 4. Run apparatus: built + hardened
- Classifier: `--sleep-between N` (inter-batch pacing), `--validate-every N` + `--reject-rate-floor` (mechanical drift check → hard-stop exit 43 on schema break or reject-rate < 0.70). Validation cadence (Matt): every 25 batches + drift-stop; precision reads at first checkpoint + end.
- Wrapper `scripts/stage4-events-bulk-run.sh` — paced auto-resume, fresh datestamped output dir, `--skip-existing` resume.
- **DISCOVERED duplication:** `scripts/stage4-tail-bulk-forever.sh` already existed (proven burst-model loop). Kept both; cross-referenced the new paced variant. (script-builder wasn't told to check first — orchestrator miss.)
- **"Sleeps but never restarts" hardening (Matt-flagged):** the historical fix is `sleep_with_stop_check` in `stage4-haiku-loop.sh:100` — sleep in 60s chunks, re-check the stop-file each chunk (a bare multi-hour `sleep` can't be interrupted → looks dead). Applied to the wrapper (all sleeps) AND the classifier's `--sleep-between` (chunked 30s, checks `/tmp/stage4-stop`, flushes + exits cleanly mid-sleep). Also: wrapper now treats **exit 130 (Ctrl-C) as terminal** (was relaunching it); `MAX_ITER=200`; removes stop-file at exit.
- **Test-count scare:** the hardening agent reported "956/956 green" — a miscount/partial run. Direct re-run showed the real suite is **1072 passed, 0 failures**. (Lesson: verify agent-reported test counts.)

## 5. Launch — and the hardening proved itself live
- Started in Matt's iTerm at `STAGE4_SLEEP_BETWEEN=1800` (concurrent-safe while he uses Opus). Batch 1: 4 typed / 36 rejected, $0.10, 114s — healthy 90% reject.
- Matt saw only **2% of the 5h cap** consumed → lowered to **600s**. The stop+relaunch worked perfectly: stop-file detected mid-sleep → flush → exit 130 → no relaunch; relaunch skipped 80 already-typed rows (flushed on the clean stop) and resumed at 411 batches. **The exact "sleeps but never restarts" failure mode, now behaving correctly in production.**
- First 4 flushed emits all correct (`BONDED_TO nymeria`, `WIELDS needle`, `RESENTS sansa`, `MOURNS mycah`); no slug garbage — the candidate fix is holding.

## Calibration note
Matt pushed back on "borderline grounding" — clarified it referred to *citation-quote directness*, a separate softer axis from *edge correctness*. Agreed all four early emits are correct. Going forward, precision reads judge **edge correctness** as the bar; only flag a quote when it actively fails to support the type.

## Operational state at session close
- Events Haiku bulk RUNNING in Matt's iTerm: `STAGE4_OUT=.../_events-haiku-bulk`, 600s pacing, validate-every 25. ~411 batches remaining, ~3.5 days at 600s.
- **TEMP-SLEEP note in worklog Active Decisions:** a session must LOWER sleep further if needed / the 600s is already set; the original "lengthen for concurrent, shorten before travel" is satisfied (now at 600s, fine for both).
- 3 gated core-cleanups still await Matt's before/after sign-off.
- Nothing merged into `graph/edges/edges.jsonl` — the merge/formalize remains a separate gated milestone.
