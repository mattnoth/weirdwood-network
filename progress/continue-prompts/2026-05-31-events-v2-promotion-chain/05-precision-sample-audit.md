# Step 5 — Precision-filter 200-row reviewer audit

> **Recommended model:** Opus 4.7. Precision judgment is the entire point of this step; do not downgrade. **Read-and-write** for audit artifacts. **Do NOT promote** to `graph/`.
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 4 status file** shows `proceed_to_step_5: yes` with Matt's sign-off.
- `_v2-refine/edges-v2-resolved.jsonl` exists and is the input to this step.

## Why this step exists

v1.3 was scored against a **200-row head-to-head reviewer audit** that yielded "strict precision ≈ 78%" (graph/edges/README.md). The dominant residual issue was evidence-quote mis-location (right type/pair, wrong quote attached). We're going to apply the same audit to v2.

We need this step because: contract validation (step 3) and resolver (step 4) catch *categorical* errors but not *semantic* errors. A `TRAVELS_WITH` edge can pass contracts and resolver while still being wrong — e.g., source travels *to meet* target rather than *with* target. That class of error is only catchable by human-style reading.

## What to do

1. **Locate v1.3's audit methodology.** Look for the head-to-head reviewer audit artifact from 2026-05-25 (see `graph/edges/README.md` §Quality and `history/session-details/session-72*.md` if present). Reuse its sampling and scoring rubric so v2 is comparable.

2. **Draw a 200-row stratified sample** from `edges-v2-resolved.jsonl`:
   - **120 rows from events-haiku** (the new layer — this is what's being audited).
   - **80 rows distributed across spine / tail / hospitality** (to confirm v1.3 didn't regress under the new dedup tie-break).
   - Stratify the events-haiku 120 by edge-type proportional to emit counts; weight toward the high-volume types (TRAVELS_WITH, COMMANDS, TRAVELS_TO, LOCATED_AT, SERVES) plus ≥3 from each long-tail type that emitted ≥10 rows total.
   - Seed the draw (`seed=531`) and write to `working/audits/events-v2-promotion-2026-05-31/audit-sample-200.jsonl`.

3. **Score each row strictly.** For each sample row, an Opus session:
   - Reads `evidence_ref` (file:line) → opens the chapter file → reads 10-20 lines of surrounding context.
   - Verdict on each of: **(a) edge_type correct**, **(b) source_slug correct**, **(c) target_slug correct**, **(d) direction correct**, **(e) evidence_quote actually supports the edge** (the v1.3 weakness).
   - Strict precision = all 5 correct. Pair precision = (b)+(c) correct regardless of type. Type precision = (a) correct given (b)+(c).
   - Optional notes per row in `audit-sample-200-scored.jsonl`.

4. **Compute aggregate scores**:
   - Strict precision overall
   - Strict precision per edge-type
   - Per source_set (spine/tail/hospitality/events-haiku) — is events-haiku the weak link or has v1.3 held?
   - Failure-mode breakdown (wrong-type / wrong-direction / wrong-quote / wrong-slug / etc.)

5. **Write `working/audits/events-v2-promotion-2026-05-31/precision-audit.md`** with:
   - Methodology + sampling + seed
   - Aggregate scores in the table format above
   - Failure-mode breakdown with sample rows
   - **Go/No-Go recommendation** against the gate below
   - Comparison to v1.3's 78% baseline

## Gates

- **Go**: strict precision overall ≥75% **AND** events-haiku strict precision ≥70% **AND** no edge type with strict <50% and >10 samples.
- **No-Go**: anything below those floors → escalate to Matt; the v2 layer is not ready and may need either targeted re-typing or a wholesale shift back to Sonnet for the events tail.
- **Borderline (70-75% overall, or events-haiku 60-70%)**: surface failure modes; Matt decides whether to fix-then-ship or to ship-with-caveat (update README's Quality section to call out the lower-precision class).

## Deliverables for step 6

- `working/audits/events-v2-promotion-2026-05-31/audit-sample-200.jsonl`
- `working/audits/events-v2-promotion-2026-05-31/audit-sample-200-scored.jsonl`
- `working/audits/events-v2-promotion-2026-05-31/precision-audit.md`
- `step-05-status.md` — explicitly records the Go/No-Go verdict and Matt's sign-off.

## Hard rules

- **Do not adjust the sample after scoring starts.** The seed locks the sample; the score is what it is.
- **Do not silently rescue borderline rows.** A row that "could be right with a generous reading" scores as wrong-strict. The point is to measure what we have.
- **Do NOT promote** to `graph/` — that's step 6, after this step's Go.
