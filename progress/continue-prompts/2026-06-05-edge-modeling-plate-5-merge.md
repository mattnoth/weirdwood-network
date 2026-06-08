# Plate 5 — Gated merge to edges.jsonl + carried-forward cleanups

> **Recommended model:** Sonnet for the deterministic merge + validation. Matt provides before/after sign-off (this is the one irreversible step).
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context docs:**
>   - `working/edge-modeling/PLATE5-READINESS.md` — **READ FIRST** — exhaustive inventory of every staged change across all plates with delta math.
>   - `working/edge-modeling/edge-modeling-reification-design.md` §5 (carried-forward cleanups), §8 (reversibility/safety)
>   - `working/edge-modeling/SESSION-2026-06-07-AUTONOMOUS-REPORT.md` — full context of Plate 3 + Plate 4-cluster runs
> **PRECONDITIONS:**
> - All Plate 0/3/4-cluster staged outputs exist under `working/edge-modeling/`.
> - Matt has reviewed PLATE5-READINESS.md and explicitly approved the merge.
> - D2 RESOLVED → **(a) Replace** (no materialized agent→patient dyads to emit; superseded scattered binaries get `superseded_by` flag, not deletion).
> - **Open design question to resolve BEFORE running:** dual-taxonomy vs single-tier for chapter-beat mints. See `progress/continue-prompts/2026-06-08-alias-and-display-design.md`. If Matt picks dual-taxonomy, Plate-3 mints go to a sibling directory (`graph/nodes/events-pass1-beats/`) with `event_tier: pass1-beat` and `SUB_BEAT_OF` edges linking to canonical events.

## Why

Single gated step that writes all staged work into the canonical graph, with full backup and a before/after diff. This is the only irreversible plate — treat with care.

## Steps

1. **Backup** `graph/edges/edges.jsonl` to `graph/edges/_regrounding/edges-pre-reification-<ISO date>.jsonl` (project convention — `_regrounding/` is the existing backup dir).
2. **Merge in order** with a validation pass after each step (use the existing validators: `scripts/stage4-type-contract-validator.py`, schema-drift, orphan-edge):
   - **(a)** Apply Plate 0 normalizer flips (10 flipped rows) — overwrite in place using `working/edge-modeling/normalizer-candidates.jsonl`.
   - **(a')** Apply Aerys slug merge (3 edges repointed `aerys-targaryen` → `aerys-ii-targaryen`) from `working/edge-modeling/aerys-merge-candidates.jsonl`. Quarantine the now-empty `aerys-targaryen` node to `graph/nodes/_conflicts/` per project convention (do NOT delete).
   - **(b)** Append Plate 3 role edges from `working/edge-modeling/plate3-full/role-edges-staging.jsonl` (914 edges). Mint event nodes from `working/edge-modeling/plate3-full/minted-event-nodes/` (219 nodes; or sibling dir per dual-taxonomy decision). Mark superseded scattered binaries (55 candidates at `working/edge-modeling/plate3-full/supersede-candidates.jsonl`) with `superseded_by: <hub-slug>` (do not delete — CLAUDE.md source-data rule).
   - **(b')** Triage `working/edge-modeling/plate3-full/hub-review-queue.jsonl` (109 entries) — Matt's decisions on which borderline mints to keep vs drop. Triage list at `HUB-REVIEW-TRIAGE-LIST.md`.
   - **(c)** Apply Plate 4-cluster staged edges: 54 cluster edges from `working/edge-modeling/plate4-wiki-cluster/cluster-edges-staging.jsonl` (51 SUB_BEAT_OF + 3 DUPLICATE_OF). The 3 DUPLICATE_OF imply mint→wiki node merges — repoint mint's role edges to the wiki event-node, then mark mint as superseded.
   - **(c')** Apply Plate 2.5 schema fixes: 27 event-type corrections from `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl` (event.battle → event.wedding/feast/coronation/trial). Also apply 12 drift retypes (event.battle → meta.chapter) from `working/edge-modeling/drift-reclassify-candidates.jsonl` + 4 collision merges from `collision-merge-candidates.jsonl`.
   - **(d)** Add new edge types to `reference/architecture.md` if not already: `SUB_BEAT_OF`, `DUPLICATE_OF`. Add new event sub-types: `event.wedding`, `event.feast`, `event.coronation`, `event.trial`, `event.assassination`, `event.execution`, `event.conspiracy` (the missing-enum bug root cause).
3. **Carried-forward S77 cleanups** (only if Matt confirms — these were deferred from Session 77 and should not surprise the merge):
   - Drop 2 `cersei ↔ tyrion LOVES` edges (confirmed false from S77 conflict-pairs review).
   - Retype ~22 `ASSAULTS → ATTACKS` edges (`ASSAULTS` is sexual-only per architecture).
   - Merge-time `OWNS → BONDED_TO` for direwolf/dragon targets.
4. **Run the full validator suite**: schema-drift, orphan-edge, type-contract. ZERO new orphan edges allowed. Confirm 0 nodes lost their last edge.
5. **Regenerate per-node `## Edges` display bullets** (they are NOT auto-synced to the JSONL — there's a script for this; if not, run the appropriate `scripts/build-node-display-edges.py` or equivalent — check `graph/nodes/README.md` if unsure).
6. **Produce a before/after diff** + final counts. Update `worklog.md` (Current State + new session entry).

## Done-criteria

- All staged work merged; all validators green; no new orphan edges.
- Per-node display lists regenerated.
- Backup retained at `graph/edges/_regrounding/edges-pre-reification-<date>.jsonl`.
- Before/after diff archived under `working/edge-modeling/plate5-merge-diff.md`.
- Red Wedding smoke test passes: `python scripts/graph-query.py --neighbors red-wedding` shows role-typed participants.

## Out of scope

- Any new analysis, extraction, or LLM pass. This plate only commits prior staged work.

## Files this session may modify

- `graph/edges/edges.jsonl` (the gated write)
- `graph/nodes/events/` (minted event nodes)
- `graph/nodes/_conflicts/aerys-targaryen.node.md` (quarantine move)
- Per-node display bullets across `graph/nodes/`
- `worklog.md`
- CREATE `working/edge-modeling/plate5-merge-diff.md`
- APPEND `## Plate 5 — gated merge (Session N)` to `SESSION-LOG.md`
