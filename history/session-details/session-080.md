# Session 80 — Events Haiku bulk completed: wrapper bug fixed, run analyzed, 7-step v2.0 promotion chain authored (2026-05-31)

**Model:** Opus 4.7 (orchestrator; diagnosis + analysis + planning + prompt authoring). No code beyond a single Python counting bugfix in `scripts/stage4-events-bulk-run.sh`. **Commit:** this endsession commit.

## Frame

Matt returned from travel. The Events Haiku bulk run he'd left running on 2026-05-28 had completed in the meantime — the terminal showed all 282 batches landed cleanly, then the wrapper printed "2 consecutive no-progress iterations. Stuck on 2900 rows" and exited. Matt's question: "all batches may have finished? we may have missed some."

The session goal that emerged: confirm what happened, fix the wrapper's false-alarm message, write the analysis, and stage everything to promote the Events output into `graph/edges/edges.jsonl` as v2.0. Matt explicitly endorsed the plan and asked to store the promotion plan as a prompt chain, with Dialogue flagged as the next thing after promotion.

## What the "stuck on 2900 rows" message actually meant

The classifier's final summary was clean: 11,263 rows in / 1,063 typed / 10,199 rejected / 0 classify_failed / 1 needs_qualifier. Combined with the 554 emits from earlier (S77-S79) segments, **1,617 typed edges total** across the 5 books with the same `prompt_version=v5-precision-rules`, `prompt_sha=d31ca56c4768`, `typed_by=haiku`.

After the final batch, the wrapper looped twice more — the classifier reported "Skipped 16,502 already-typed rows; 0 remaining" both times, but the wrapper's own `count_remaining` returned 2,900 instead. Two consecutive identical positive remainders → "no progress" → exit.

Diagnosis: `count_remaining` counts total candidate **rows** but the done-set is a **set of `(source_slug, target_slug, evidence_chapter)` keys**. The input has duplicate keys (multiple Pass 1 event rows can share a triple — e.g., the same TRAVELS_WITH pair recurring across a chapter's table). When all unique keys are classified, `total_rows - len(done_keys) = duplicate_count`, not zero. The 2,900 == count of duplicate input keys, verified by recomputing both sides with the same key.

Per-book accounting verified all 16,502 inputs landed in emit + rejected + (one) needs-qualifier. Nothing missing.

**Fix:** Patched `count_remaining` to count input as a set of the same key tuple, not raw rows. Verified by re-running it on the current state — returns 0. (Minor functional impact going forward: future bulk runs won't false-alarm-stop at the end. The patched function is in `scripts/stage4-events-bulk-run.sh` lines ~100-152.)

## Run analysis (full report at `working/audits/events-haiku-bulk-2026-05-29/analysis.md`)

Highlights worth carrying forward:

- **Cost:** Final segment $34.13; cumulative across all four contributing runs ~$38-40.
- **Drift-clean:** Single prompt_sha across all 1,617 emits. Single model. 0 conform_violations. 0 classify_failed (the one needs-qualifier row is sitting in `_needs-qualifier/`, not lost).
- **Calibration is real now:** tier-1 256 / tier-2 1,342 / tier-3 19. Unlike v1 (all tier-1), Haiku used the tier range as designed.
- **Locator strong:** 99.6% verbatim quote attachment (1,610 verbatim / 7 chapter-level out of 1,617). This was the dominant v1.3 residual issue; v2's locator output is much cleaner.
- **Qualifier coverage:** 10.5% — modest but reasonable; qualifiers are optional.
- **Edge-type distribution:** 100 distinct types. Top 5 = TRAVELS_WITH (127), COMMANDS (121), TRAVELS_TO (115), LOCATED_AT (90), SERVES (84) — exactly the event-shaped predicates the v1 relationship-spine doesn't carry.
- **Per-book narrative shape matches book content:** agot leads with TRAVELS_WITH/ATTACKS/SIBLING_OF (Stark family + early war); acok with COMMANDS/SERVES/OPPOSES (full war); asos with COMMANDS/TRAVELS (RW armies); affc with TRAVELS_TO/LOCATED_AT (Brienne wandering, Sansa at Eyrie); adwd with TRAVELS_WITH (Tyrion/Quentyn travelogues).
- **Overlap with v1.3:** 444 pair-overlaps, 289 triple-overlaps, 278 quad-overlaps. **988 net-new triples** if promoted. The overlap is enrichment-on-pair (same characters, new fact-types), not conflict.

One **noted schema gap** worth fixing in Dialogue prep: rejected rows carry no `reject_reason` field. So we can't do quantitative rejection-cause analysis on the 14,884 rejects. Sample inspection shows they're mostly real non-edges, but a `reject_reason` enum would make future runs auditable. Matt's decision: **fix-later, in Dialogue prep**, not now.

## Promotion plan — chain of 7 self-contained prompts

Lives at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/`:

| # | Step | Recommended model | Gate |
|---|------|-------------------|------|
| 1 | Cross-model drift audit (~50-row sample) | Sonnet+Opus | ≥70% triple / ≥85% pair |
| 2 | Extend `stage4-formalize-edges.py` with EVENTS-HAIKU as 4th source | Opus | dry-run reviewed |
| 3 | Type-contract validation on v2 candidate | Sonnet | drop/retype counts |
| 4 | Title-person resolver pass on v2 | Sonnet | remap diff |
| 5 | 200-row precision audit (strict) | Opus | ≥75% strict overall |
| 6 | Promote to `graph/edges/edges.jsonl` v2.0 + README + commit | Opus | Matt before/after sign-off |
| 7 | Hand-off to Dialogue v2.1 chain | Opus | smoke-test design |

Each step writes a `step-NN-status.md` declaring whether the next step can proceed. The chain README captures three open questions Matt answered up front so each step inherits the same context:

1. **Full re-merge vs. additive overlay?** → Full re-merge (one consolidated v2 jsonl, not a sibling layer).
2. **Ship Events-only as v2.0 or wait for Dialogue?** → Events-only. Dialogue lands as v2.1.
3. **`reject_reason` schema fix-now or fix-later?** → Fix-later, in Dialogue prep.

Hard rule carried across every step: **never modify `graph/edges/edges.jsonl` without Matt's before/after sign-off.** Step 6 has explicit pre-commit gates (backup v1.3 to `_versions/`, diff summary to Matt, await Go).

Step 7 is the bridge to Dialogue work — it explicitly closes out this chain and points to building a parallel chain at `progress/continue-prompts/<date>-dialogue-v2.1-chain/` modeled on the same structure. Notes on what Dialogue should inherit from Events learnings: vocab lockdown is the same (v5-precision-rules); reject-rate expectation similar (~90%); fix `reject_reason` + the recurring `classify_failed` parse-fail block before Dialogue bulk; smoke-test at 85% strict before launching.

## Why this chain shape (vs. one big prompt)

A monolithic "promote the Events output" prompt would force a single agent session to span ~6 distinct review-gated steps (drift audit, script edit, contract validation, resolver, precision audit, commit). Each step has its own Matt-sign-off gate, and the work surfaces between sessions (Matt reviews step 1 → decides on step 2 → reviews step 2's dry-run → etc.). A chain matches the actual work cadence: one self-contained prompt per session, each with prerequisites and deliverables that gate the next.

The model recommendation is split per step: mechanical work (contracts, resolver) → Sonnet 4.6; judgment work (drift interpretation, precision audit, sensitive write) → Opus 4.7. Per the project's model-fit policy.

## What was NOT done this session

- No work touched `graph/edges/edges.jsonl`.
- No re-run of the Events bulk classifier (it's complete; the source artifact is frozen).
- No work on the 3 gated core-cleanups (cersei↔tyrion LOVES drops, ASSAULTS→ATTACKS retypes, OWNS→BONDED_TO merge). These remain queued, separate from v2.0 promotion.
- No work on Dialogue (correctly deferred to step 7's chain spawn).
- No fix applied to the `classify_failed`-not-a-skip-key bug (S79 loose end). Queued in todos.md; should land before the Dialogue bulk.

## Carrying over to next session

- The 2026-05-27-events-haiku-bulk-monitor.md continue prompt is now **stale** — it described monitoring an in-flight run that has since completed. Should be archived. Its "completion-read + slug long-tail triage + MERGE" obligations are absorbed by the new chain (drift audit covers the precision read; slug triage is part of step 4 resolver; merge is step 6).
- Next session starts at step 1 of the chain (drift audit). Self-contained handoff in the file at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/01-drift-audit.md`.
