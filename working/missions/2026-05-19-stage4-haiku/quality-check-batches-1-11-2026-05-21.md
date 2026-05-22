# Stage 4 Tier-1 bulk — interim quality check (batches 1–11)

**When:** 2026-05-21 ~23:40 CDT, after first 11/222 batches landed.
**Trigger:** continue-prompt instruction to check aggregates after first 5–10 batches.
**Verdict: HEALTHY — keep running. No stop, no prompt change.**

## Aggregate (2,237 rows across 105 edge files)

| Axis | Value | Baseline | Verdict |
|---|---|---|---|
| Wall-clock | ~2.9 min/batch avg | 4.6 min smoke | ✅ better |
| Cost | $2.70–$3.10/batch | $2.73 smoke | ✅ on-baseline |
| Files failed | 0 / 30 every batch | 0 | ✅ clean |
| Rate-limit events | 0 | 0 | ✅ clean |
| Violation rate (distinct rows) | 87/2237 = **3.89%** | 2.80% smoke / 3.96% v164 / 4.3% Sonnet | ✅ under 5% stop threshold |

Violation histogram: bad-evidence-section 44, missing-required-fields 26,
qualifier-required-missing 12, type-contract-violation 3, edge-type-not-canonical 3,
invalid-candidate-kind 2, **verb-gate-failure 1**.

## Two findings

1. **ENCOUNTERS verb-gate working.** Just 1 verb-gate-failure in 2,237 rows (~0.04%),
   vs the smoke's ~2% of emits. Heavy ENCOUNTERS hardening (Session 63) is effective.

2. **`bad-evidence-section` (44, ~half of all violations) is one localized bucket, not drift.**
   - All 43–44 empty-`evidence_section` rows are in `characters-house-hightower-j-w`
     (3 files: leyton-/lynesse-/lyonel-hightower). No other bucket has any.
   - Root cause: a Haiku **output quirk** for that bucket — it emitted `evidence_section: ""`
     even though the enriched candidate carried the section under `source_section`
     (e.g. `## Origins`). Confirmed the data was available: **0.0% empty `source_section`
     across 76,009 candidate rows** corpus-wide. So this is NOT an enrichment gap and NOT
     systematic; it's a ~1%-of-files Haiku omission.
   - The edges themselves are CORRECT (e.g. `leyton-hightower ALLIES_WITH renly-baratheon`,
     evidence "Lord Leyton supports Renly Baratheon"). Only the `evidence_section` provenance
     field is blank.
   - Excluding this one bucket, the real violation rate is ~(87−43)/2237 ≈ **2.0%** — better
     than the smoke.

## Recommended follow-up (NOT urgent, NOT before continuing)

- **Deterministic `evidence_section` backfill** (post-run cleanup): for any output row with
  empty `evidence_section`, join back to the enriched candidate on
  `source_slug + target_slug + edge_type` and copy `source_section` → `evidence_section`.
  Recovers all affected rows with zero Haiku re-runs. Add to todos.
- Do NOT change the classify prompt for this — it's a low-frequency quirk and the handoff
  forbids prompt edits without smoke evidence. If the backfill is built, it covers it.
- Validator invocation note: `--batch-id` mode fails on Haiku results JSON because the
  orchestrator doesn't write an `output_files` key (validator reads `data["output_files"]`).
  Workaround used here: concat `prose-edges-haiku/*.edges.jsonl` → one file →
  `--file <concat> --graph-nodes graph/nodes`. Consider adding `output_files` to the Haiku
  results JSON, or a `--mission-glob` mode, so per-batch validation works directly.
