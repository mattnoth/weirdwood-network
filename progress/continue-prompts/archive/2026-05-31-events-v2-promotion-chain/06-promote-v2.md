# Step 6 — Promote: `edges.jsonl` v1.3 → v2.0

> **Recommended model:** Opus 4.7. This is the sensitive write. **Write allowed** but every write to `graph/edges/edges.jsonl` is gated on Matt's before/after sign-off in this exact session — no inferred authorization.
>
> **Trust `worklog.md` over this prompt** if they disagree.

## Prerequisite

- **Step 5 status file** shows `proceed_to_step_6: yes` with Matt's **explicit Go** recorded.
- `_v2-refine/edges-v2-resolved.jsonl` exists and matches the precision-audit.md sample.
- All steps 1-5 status files are present in this chain directory.

## What this step does

Replaces `graph/edges/edges.jsonl` (v1.3, 3,811 edges) with v2.0 (v1.3 + ~988 net-new EVENTS-HAIKU triples, post all filters). Updates `graph/edges/README.md` with the v2 build lineage. Commits.

## What to do

1. **Sanity recompute v2 stats.** Read the final candidate `_v2-refine/edges-v2-resolved.jsonl`:
   - Total edges (call this N_v2).
   - Per source_set counts (spine / tail / hospitality / events-haiku).
   - Per edge-type counts; flag any type whose count changed >2× vs v1.3 — surface to Matt as a "watch this in the next audit cycle" note.
   - Per-`typed_by` counts (python-map / sonnet / hospitality-table / hospitality-table-violation / haiku — the new value).
   - Net-new triples vs v1.3 baseline.
   - Confidence-tier distribution.

2. **Diff v1.3 → v2.0** at the level of:
   - **Adds**: triples present in v2 but not v1.3.
   - **Drops**: triples in v1.3 not in v2 — there should be ~zero unless step 3/4 dropped a v1.3 row, which would be unexpected. If non-zero, **stop and ask Matt** — v1.3 was the reviewed baseline.
   - **Modifies**: same triple, different qualifier/quote/tier. Surface to Matt; usually safe but worth seeing.

3. **Write the change summary** to `_v2-refine/v2-promotion-diff.md` with the three tables above.

4. **Get Matt's before/after sign-off.** The hard rule from CLAUDE.md and prior chains: never modify `graph/edges/edges.jsonl` without it. Surface:
   - v1.3 stats (3,811 edges, sources spine/tail/hospitality, 4 typed_by values)
   - v2.0 stats (N_v2 edges, sources +events-haiku, 5 typed_by values)
   - Precision-audit verdict (from step 5)
   - The change summary file path
   - Ask: **"Approve promotion to v2.0?"**

5. **On Matt's Go**:
   - Back up the current `graph/edges/edges.jsonl` → `graph/edges/_versions/edges-v1.3-2026-05-25.jsonl` (create the `_versions/` dir if it doesn't exist). This is reversibility insurance.
   - Strip advisory `_`-prefixed fields (from step 3's annotated layer) before writing the committed JSONL.
   - Write `_v2-refine/edges-v2-resolved.jsonl` (clean schema) → `graph/edges/edges.jsonl`.
   - Update `graph/edges/README.md`:
     - Header: change v1.3 → v2.0 with date and provenance.
     - Add new `typed_by` row: `haiku` with count + source label "S80 EVENTS-HAIKU bulk — Haiku typed the residual pass1_events table".
     - Add new build-lineage block showing the v1.3 → v2.0 step (input N_v1.3 + EVENTS-HAIKU N → endpoint-gate → contracts → resolver → audit-survivors → v2.0 N).
     - Update the Roadmap section: mark "v2 enrichment Events half" as **done**; surface Dialogue half as next (step 7).
     - Update the Quality section with the v2 precision-audit numbers.
   - Commit with a message like `S80: Promote graph/edges/edges.jsonl v1.3 → v2.0 (Events Haiku enrichment, +988 net-new triples)`.

6. **Do NOT push.** Matt pushes when ready.

7. **Write `step-06-status.md`** with: pre/post counts, commit SHA, files changed, the precision-audit verdict carried forward, **explicit hand-off to step 7 (Dialogue)**.

8. **Update `worklog.md`** with a v2.0 promotion session entry (per CLAUDE.md rule #4 — every session must update worklog; this is a structural state change).

## Gates

- **Approve to commit**: Matt's explicit Go on the change summary diff.
- **No-go**: any unexpected drop in step 2 → pause, investigate, do not promote.
- **Post-commit verify**: run `wc -l graph/edges/edges.jsonl` and confirm it matches N_v2. If not, revert from `_versions/` and re-investigate.

## Deliverables for step 7

- `graph/edges/edges.jsonl` v2.0 — committed.
- `graph/edges/README.md` updated.
- `graph/edges/_versions/edges-v1.3-2026-05-25.jsonl` — backup.
- `_v2-refine/v2-promotion-diff.md` — the diff summary.
- `step-06-status.md`.
- `worklog.md` — new session entry.

## Hard rules

- **NEVER push** without Matt asking.
- **NEVER skip the backup step.** Restoring v1.3 must be possible with a single `cp`.
- **NEVER delete** v1.3 staging artifacts under `_formalized/` — they're the audit trail for the v1.x line.
