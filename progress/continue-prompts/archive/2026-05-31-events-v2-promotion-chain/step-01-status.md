# Step 01 — Drift-detection audit · STATUS

**Date:** 2026-05-31 → 2026-06-01 (UTC)
**Chain step:** `01-drift-audit`
**State:** **COMPLETE — NO-GO (borderline, see fresh-eyes review). Chain halted at step 1; step 2 will not start until Matt picks an escalation path.**

> **2026-06-01 fresh-eyes review** (general-purpose subagent, cold reading of all 22 Sonnet REJECTs against V5 rules):
> - Audit's overall verdict holds, but ~3-4 Sonnet over-rejections confirmed (judge_idx 2 Edmure-TRAVELS_WITH-on-the-march; 6 Jaime-TRAVELS_TO-Harrenhal; 14 Ramsay-REVEALS_TO-Roose; 16 Haldon-TRAVELS_WITH-Duck).
> - **The smoke-run reference in §4 is mis-cited** — actual session is **S77** (not S69), and S77 measured *hand-read precision on fresh candidates*, not *Sonnet judges Haiku emits*. Different metric on different sample shape; the apparent "smoke said opposite" contradiction is measurement-shape, not drift.
> - Adjusted triple agreement crediting all over-rejections + all ambiguous: ~56-70 %, at or below the 70 % floor.
> - Methodology: no script bugs.
> - Verdict: No-Go stands but borderline; Option (C) (Sonnet-filter named-type rows only) is the right-shape escalation.

## Top-line verdict

| Gate | Floor | Observed | Pass? |
|------|------:|---------:|:-----:|
| Triple-level agreement | ≥ 70 % | **48.0 %** (24/50) | ✗ |
| Pair-level agreement | ≥ 85 % | **56.0 %** (28/50) | ✗ |
| No edge type <50 % with >5 samples | — | **TRAVELS_TO 17 % (1/6)** | ✗ |

22 of 50 Haiku emits (44 %) were rejected by Sonnet.

Full report: **`working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md`**

## What ran

1. **Wrote** `scripts/events-drift-audit.py` (sha `576cc815649c`) — 327-line single-purpose throwaway, imports canonical prompt-renderer + `claude -p` subprocess from `stage4-tail-classifier.py` (parity, not framework).
2. **Dry-run** (no args): 1,617 emits loaded; 163-edge locked vocab; prompt SHA `d31ca56c4768` matches Haiku bulk-run SHA exactly. Wrote `audit-sample-50.jsonl` (seed=531, 50 stratified rows).
3. **Apply** (Matt approved): 5 batches × 10 rows × Sonnet 4.6 cwd=/tmp; **$0.93 total**; wrote `audit-sample-50-judged.jsonl`.
4. **Manual inspection** of 5 high-disagreement rows: in every case Haiku is the side that drifted (treating `hint_raw` as evidence on par with `evidence_quote`, violating Rule 4a / V5-R2). Documented in cross-model-audit.md §3.
5. **Authored** `cross-model-audit.md` with the agreement-rate table, per-edge-type breakdown, manual inspection cases, root-cause hypothesis, and 5 escalation paths (A–E) for Matt to choose between.

## Failure pattern (one line)

Haiku consistently emits LOCATED_AT / TRAVELS_TO / TRAVELS_WITH from hint
descriptions that the quote does not support — V5-R2 (evidence-grounding)
and Rule 12 (CO-PRESENCE) violations at scale, despite the lockdown.

## Why this contradicts the S69 smoke runs

The S69 smoke runs scored Sonnet-vs-Haiku ~85 % AGOT / ~90 % ACOK on Events.
That number does *not* generalize to the bulk-run output — either the smoke
sample was different (cleaner candidates) or Haiku degrades over a long
bulk run. Not re-investigated here; the audit's job was to surface the
problem, not diagnose it.

## Provenance (header on every output file)

```json
{
  "chain_step": "01-drift-audit",
  "script_path": "scripts/events-drift-audit.py",
  "script_sha": "576cc815649c",
  "judge_model": "claude-sonnet-4-6",
  "judge_cwd": "/tmp",
  "expected_prompt_sha": "d31ca56c4768",   // matches Haiku bulk run
  "sample_seed": 531,
  "sample_n": 50,
  "judged_count": 50,
  "judged_cost_usd": 0.9274
}
```

## Hard rules observed

- Did NOT touch `graph/edges/edges.jsonl` or anything under `graph/`.
- Did NOT re-launch the Events bulk classifier.
- Did NOT use an Agent subagent for the judge step.
- `events-drift-audit.py` is single-purpose; no framework abstraction.
- Default `--dry-run`; `--apply` ran only after Matt's explicit go.

## What step 02 needs from step 01

**Step 02 (`02-extend-formalize.md`) does NOT start.** The chain halts here
per the No-Go gate. Resumption requires Matt to choose one of the
escalation paths in `cross-model-audit.md §6`:

- **(A)** Re-run Events bulk on Sonnet (~$340 for the full corpus; contradicts `project_stage4_haiku_not_sonnet` memory).
- **(B)** Promote only the long-tail types from the Haiku output, drop the named-type buckets.
- **(C)** Filter the Haiku output by Sonnet on the rejection-bearing types only (~700 rows).
- **(D)** Tighten Haiku prompt to v6 and re-run.
- **(E)** Abandon Events bulk for v2.0; wait for Dialogue.

After Matt picks: the chain README + downstream prompts need updating per
the chosen path, then step 02 (or its replacement) can begin.

## Files on disk after this step

- `scripts/events-drift-audit.py` *(new)* — sha `576cc815649c`.
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50.jsonl` *(new)* — 51 lines.
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50-judged.jsonl` *(new)* — 51 lines.
- `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` *(new)* — the full audit report.
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` *(this file)*.
