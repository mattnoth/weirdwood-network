# Haiku vs Sonnet — Events edge-typing comparison (model decision for the remaining ~82%)

> **Recommended model:** **Opus 4.7** as conductor (the verdict-diff judgment + precision read are the reasoning part). **Haiku 4.5** (`claude-haiku-4-5-20251001`) is the *worker under test*. The diff is a tiny deterministic script (inline or via script-builder/Sonnet). Do NOT run the Sonnet bulk while this is pending.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9).

## Why this exists
The Events edge-typing run (Stage-4 Pass-1-derived, `pass1_events` candidates) is **~18% done on Sonnet** at **~82-86% strict precision** (audited across 5 checkpoints, 2026-05-27). It **paused on a shared-account rate-limit wall** — a sustained Sonnet run trips Matt's account cap (~75 batches per ~5-hour window) and competes with his interactive sessions. Matt's standing policy puts the *bulk* on **Haiku** (`project_stage4_haiku_not_sonnet`) precisely for quota reasons; the v5 precision rules + gated-vocab lockdown were built to make Haiku safe. **But Haiku has never been tested on the CURRENT setup.** Earlier Haiku smokes were **~60-62% strict** — genuinely below bar — but those ran on the **old v4 prompt, before** the candidate-gen fixes (slug-gate, direction-validation) and **before v5**. This track measures Haiku on the current setup, apples-to-apples, to decide the model for the remaining ~82%.

## State you inherit (2026-05-27)
- **Sonnet run output:** `working/wiki/pass2-buckets/pass1-derived/_events-run-20260527/` — **369 typed / 2,631 rejected / 240 classify_failed** over the first **75 batches (~3,000 rows)**. 273 unique edges after dedup. Stamped `prompt_version=v5-precision-rules`, `model=claude-sonnet-4-6`. **$20.81 spent.** Paused at the wall (batches 76-80 returned empty → clean exit 42).
- **Candidates:** `working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/*.extra-tables.jsonl`, `candidate_kind=pass1_events`, **16,572 untyped rows total = 415 batches @ 40.** Load order is deterministic (chapter order AGOT→ADWD), so `--smoke N` reproduces the EXACT first N rows Sonnet processed.
- **Classifier:** `scripts/stage4-tail-classifier.py` now has `--flush-every N` (cursor-based incremental flush, default 5) + SIGINT/SIGTERM flush handler (lossless kill, resumable). 1011 tests green.
- **Worker invocation pattern (memory `reference_llm_pass_via_claude_p`):** classifier shells `claude -p` from /tmp; pass `--model <id>`.
- **graph/edges/edges.jsonl = 3,811 deterministic core, UNTOUCHED.** None of the Events edges are merged yet — the merge/formalize is a separate gated milestone.

## The comparison — exact steps
1. **Run Haiku on the SAME first 600 rows** (= first 15 of the batches Sonnet already did). NO `--skip-existing` (we want those exact rows), separate output dir:
   ```bash
   cd /Users/mnoth/source/asoiaf-chat
   OUT=working/wiki/pass2-buckets/pass1-derived/_events-haiku-cmp-20260527
   mkdir -p "$OUT"
   python3 scripts/stage4-tail-classifier.py --apply \
     --input-dir working/wiki/pass2-buckets/pass1-derived/_extra-tables \
     --candidate-kinds pass1_events \
     --smoke 600 \
     --model claude-haiku-4-5-20251001 \
     --output-dir "$OUT" \
     --chunk-size 40 --flush-every 5 \
     --abort-after-consecutive-failures 5 \
     > "$OUT/run.log" 2>&1   # run in background; ~25-40 min, <$1, negligible quota
   ```
2. **Build the verdict diff** (deterministic, $0). Match Haiku rows to Sonnet rows by a row key = `(source_slug, target_slug, evidence_chapter, evidence_ref)` (every emit/rejected/classify_failed row carries these). For the overlapping rows compute:
   - **Agreement rate**: same `edge_type`, or both REJECT.
   - **Divergence buckets**: Sonnet-typed/Haiku-REJECT (Haiku misses), Sonnet-REJECT/Haiku-typed (Haiku over-emits — the dangerous one), both-typed-different-type.
   - **Haiku standalone strict precision**: read a sample (~25) of Haiku's *emits* against their evidence_quote (same method as the Sonnet checkpoints).
3. **Report**: agreement %, the divergence lists (read the over-emits especially — those are graph-pollution risk), Haiku strict precision, Haiku batch-time + cap impact (measure from run.log), and a clear **Sonnet-vs-Haiku recommendation** for the remaining ~82%.

## The decision this feeds
- **If Haiku ≥~80% strict AND over-emit divergence is low** → switch the remaining ~340 batches to Haiku (lighter quota, won't wall/block Matt's sessions), wrapped in a **sleep-until-reset auto-resume loop** so walls cost ~5h not a whole idle night.
- **Else** → finish on Sonnet WITH the auto-resume wrapper (≈2 days of ~5h bursts), or pace Sonnet. Matt chooses.

## Carry-over context (Step 1 precursors — DONE this session)
- **Temporal scoping built** (`scripts/stage4-edge-temporal-scope.py`, 58 tests): 31/32 conflict pairs are legitimate temporal arcs, not errors. Annotations in `working/wiki/data/edges-temporal-scoped.jsonl`; report `graph-conflict-pairs-temporal.md`.
- **Conflict-pair mis-attribution review:** only genuine mis-types = the **2 `cersei↔tyrion` LOVES edges** (sarcasm/accusation mis-typed). Recommended drop (3,811→3,809) — **awaiting Matt's OK; do NOT modify edges.jsonl without before/after sign-off.**
- **Merge-time TODO (task #6):** normalize `OWNS→BONDED_TO` when target is a direwolf (ghost/grey-wind/lady/nymeria/summer/shaggydog) or dragon (drogon/rhaegal/viserion); `OWNS needle`/horses stay. (~4/21 of checkpoint-1 emits.)

## DO NOT
- Merge any typed Events edges into `graph/edges/edges.jsonl` (separate gated milestone).
- Touch the Sonnet output dir `_events-run-20260527/` (it's the comparison baseline).
- Run the Sonnet bulk-resume while the Haiku comparison is pending the decision.
- Run `/endsession` without explicit permission.
