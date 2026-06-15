# Step 2 — Extend `stage4-formalize-edges.py` to add EVENTS-HAIKU as a 4th source

> **Recommended model:** Opus 4.7 (script edit + interpreting dry-run stats + judgment on dedup tie-breaks). Sub-tasks (the actual code edit) can route through script-builder if the diff is mechanical. **Write allowed** for the script + staging artifacts. **Do NOT write to `graph/edges/`.**
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 1 status file exists** at `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` and shows `proceed_to_step_2: yes` with Matt's sign-off.
- Cross-model audit report at `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` met the ≥70% triple / ≥85% pair gates.

If those aren't true, **stop and ask Matt** — do not proceed.

## What this step does

Currently `scripts/stage4-formalize-edges.py` merges three sources:
1. **SPINE** — `pass1-derived/{book}/*.edges.jsonl`
2. **S67 TAIL** — `pass1-derived/_tail-typed/{book}/*.jsonl` (Sonnet)
3. **HOSPITALITY** — extra-tables hospitality rows

We're adding a **fourth source**: **EVENTS-HAIKU** at `pass1-derived/_events-haiku-bulk/{book}/*.edges.jsonl`.

Decision made up front: **full re-merge** (one consolidated v2 jsonl), not additive overlay.

## What to do

1. **Read `scripts/stage4-formalize-edges.py` end-to-end** so you understand the merge pipeline: source loading → endpoint gate → tail-violation quarantine → dedup → precision filter → staging output. The README at `graph/edges/README.md` describes the v1 build lineage; the new step has to fit that shape.

2. **Edit the script** to add the fourth source:
   - Add a loader function for `_events-haiku-bulk/{book}/*.edges.jsonl` that reads only `decision == "emit_edge"` rows with non-empty `edge_type`.
   - Tag every loaded row with `source_set: "events-haiku"` (new value alongside `spine`/`tail`/`hospitality`).
   - Route through the same endpoint-gate + dedup pipeline. **Dedup tie-break rule (NEW):** when an events-haiku row collides with a spine/tail row on `(source, edge_type, target, qualifier)`, **prefer spine > tail > events-haiku > hospitality** for the "kept" row, but always increment `dup_count`. Document this tie-break in the script docstring.
   - Apply the existing tail-violation detectors (HOLDS_TITLE→place, ENCOUNTERS-no-verb) to events-haiku rows too. They've been gated through validate@N during the run but a belt-and-braces second check is cheap.
   - Output to **a new staging file**: `_formalized/edges-v2-candidate.jsonl` (do NOT touch existing `_formalized/edges.jsonl` v1 artifacts).

3. **Run with `--dry-run` first.** Inspect: input counts per source, post-endpoint-gate counts, dedup overlap counts (events-haiku ∩ spine, events-haiku ∩ tail, etc.), final candidate count. The analysis predicts ~988 net-new triples; the dry-run should land near that.

4. **Run for real** (no flag) and produce `_formalized/edges-v2-candidate.jsonl` + a fresh `formalize-report.md` showing the v2 build lineage in the same format as the v1 README.

5. **Sanity-check the output**:
   - Count: total edges, per-source counts (spine/tail/hospitality/events-haiku), per-edge-type counts.
   - Confirm zero schema-version mismatches; every row has `evidence_kind`, `evidence_ref`, `confidence_tier`.
   - Verify dup_count distribution: most should be 1; high-dup_count rows (≥3) are interesting and worth eyeballing 5-10 of them.

6. **Surface to Matt**: before/after counts vs v1.3 (3,811 → expected ~4,800ish v2 candidate), build lineage diagram, any anomalies. **Wait for sign-off** before moving to step 3.

## Gates

- **Go to step 3**: dry-run numbers match analysis predictions within ±10%, no schema breakage, Matt approves the lineage.
- **No-go**: surface to Matt — could be a loader bug, contract-violation surge, or dedup pathology.

## Deliverables for step 3

- Updated `scripts/stage4-formalize-edges.py` (committed locally — do NOT push without Matt's go).
- `working/wiki/pass2-buckets/pass1-derived/_formalized/edges-v2-candidate.jsonl`
- `working/wiki/pass2-buckets/pass1-derived/_formalized/formalize-report-v2.md`
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-02-status.md`

## Hard rules

- **Do NOT modify** `graph/edges/edges.jsonl` or any v1 staging artifact under `_formalized/`.
- **Do NOT promote** v2 candidate anywhere; it's a staging artifact for steps 3-5.
- **Do NOT delete** the v1 artifacts; they remain as the baseline for diffing.
