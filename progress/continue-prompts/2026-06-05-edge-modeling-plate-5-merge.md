# Plate 5 — Gated merge to edges.jsonl + carried-forward cleanups

> **Recommended model:** Opus 4.7 (upgraded from Sonnet 2026-06-08 S86). This is the first plate to write to the canonical `graph/edges/edges.jsonl` (staging → production transition). Technically reversible — Step 1 backs up to `_regrounding/edges-pre-reification-<date>.jsonl` and git tracks the change — but high-friction to undo (would need to restore backup, rebuild downstream indexes, communicate the rollback). Stakes warrant the strongest reasoning, and the merge involves real judgment calls: 109-entry hub-review-queue triage (which borderline mints to keep vs drop), 55 supersede-candidate decisions (which scattered binaries get `superseded_by` flag), 3 `DUPLICATE_OF` mint↔wiki merges (repoint role edges correctly), conflict resolution if staged event-type retypes touch nodes with other metadata. Plus the new S86 scope (SUB_BEAT_OF formalization + title→name rewrite) added since the prompt was first drafted under Sonnet recommendation. Matt provides before/after sign-off.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context docs:**
>   - `working/edge-modeling/PLATE5-READINESS.md` — **READ FIRST** — exhaustive inventory of every staged change across all plates with delta math.
>   - `working/edge-modeling/edge-modeling-reification-design.md` §5 (carried-forward cleanups), §8 (reversibility/safety)
>   - `working/edge-modeling/SESSION-2026-06-07-AUTONOMOUS-REPORT.md` — full context of Plate 3 + Plate 4-cluster runs
>   - `reference/alias-resolver-design.md` (NEW, S86 2026-06-08) — alias-vs-sub-beat substitution test; event sub-type vocabulary expansion rationale; mint schema `title:`→`name:` decision.
> **PRECONDITIONS:**
> - All Plate 0/3/4-cluster staged outputs exist under `working/edge-modeling/`.
> - Matt has reviewed PLATE5-READINESS.md and explicitly approved the merge.
> - D2 RESOLVED → **(a) Replace** (no materialized agent→patient dyads to emit; superseded scattered binaries get `superseded_by` flag, not deletion).
> - **S86 RESOLVED — single-tier mints, NOT dual-taxonomy.** Chapter-beat mints land in `graph/nodes/events/` alongside wiki-derived event-nodes — same directory, same schema, same `name:` field. The distinction is captured by `SUB_BEAT_OF` edges (beat → parent-event), not by directory separation. Rationale in `reference/alias-resolver-design.md`.
> - **S86 RESOLVED — `SUB_BEAT_OF` is canonical.** Added to `reference/architecture.md` this session (vocab 165 → 166). Distinct from `PART_OF` (which is event-in-war scope). The 51 staged `SUB_BEAT_OF` cluster edges land directly with no re-emission. Forward-only — NO existing-edge backfill needed (the 3,811 existing edges are Pass-1-derived chapter-level relationships; none are beat-in-event scope).
> - **S86 RESOLVED — 7 new `event.*` sub-types are in `reference/architecture.md`.** `event.wedding`, `event.feast`, `event.coronation`, `event.trial`, `event.assassination`, `event.execution`, `event.conspiracy`. The 27 staged schema-fix retypes can apply directly (no vocab gap).

## Why

Single gated step that writes all staged work into the canonical graph, with full backup and a before/after diff. This is the first plate to write to `graph/edges/edges.jsonl` — backup-recoverable but high-friction to undo. Treat with care.

## Steps

1. **Backup** `graph/edges/edges.jsonl` to `graph/edges/_regrounding/edges-pre-reification-<ISO date>.jsonl` (project convention — `_regrounding/` is the existing backup dir).
2. **Merge in order** with a validation pass after each step (use the existing validators: `scripts/stage4-type-contract-validator.py`, schema-drift, orphan-edge):
   - **(a)** Apply Plate 0 normalizer flips (10 flipped rows) — overwrite in place using `working/edge-modeling/normalizer-candidates.jsonl`.
   - **(a')** Apply Aerys slug merge (3 edges repointed `aerys-targaryen` → `aerys-ii-targaryen`) from `working/edge-modeling/aerys-merge-candidates.jsonl`. Quarantine the now-empty `aerys-targaryen` node to `graph/nodes/_conflicts/` per project convention (do NOT delete).
   - **(b)** Append Plate 3 role edges from `working/edge-modeling/plate3-full/role-edges-staging.jsonl` (914 edges). Mint event nodes from `working/edge-modeling/plate3-full/minted-event-nodes/` (219 nodes; single-tier — all land in `graph/nodes/events/` per S86 decision). **One-time schema transform on mints (S86):** rename frontmatter field `title:` → `name:` on all 219 mints during the merge — `name:` is the canonical surface field across wiki-derived and chapter-beat-minted event-nodes. Deterministic Python; ~5 lines. Mark superseded scattered binaries (55 candidates at `working/edge-modeling/plate3-full/supersede-candidates.jsonl`) with `superseded_by: <hub-slug>` (do not delete — CLAUDE.md source-data rule).
   - **(b')** Triage `working/edge-modeling/plate3-full/hub-review-queue.jsonl` (109 entries) — Matt's decisions on which borderline mints to keep vs drop. Triage list at `HUB-REVIEW-TRIAGE-LIST.md`.
   - **(c)** Apply Plate 4-cluster staged edges: 54 cluster edges from `working/edge-modeling/plate4-wiki-cluster/cluster-edges-staging.jsonl` (51 SUB_BEAT_OF + 3 DUPLICATE_OF). `SUB_BEAT_OF` is now canonical (S86); these 51 edges land directly with no re-emission needed. The 3 `DUPLICATE_OF` are merge-time staging instructions (NOT a canonical edge type) — for each one, repoint the mint's role edges to the wiki event-node, then mark mint as superseded. After processing, `DUPLICATE_OF` rows do NOT land in `edges.jsonl`.
   - **(c')** Apply Plate 2.5 schema fixes: 27 event-type corrections from `working/edge-modeling/plate2.5-schema-fixes/event-type-corrections.jsonl` (event.battle → event.wedding/feast/coronation/trial/assassination/execution/conspiracy). All target sub-types are now in `reference/architecture.md` (S86). Also apply 12 drift retypes (event.battle → meta.chapter) from `working/edge-modeling/drift-reclassify-candidates.jsonl` + 4 collision merges from `collision-merge-candidates.jsonl`.
   - **(d)** ~~Add new edge types / event sub-types to `reference/architecture.md`~~ — **ALREADY DONE in S86.** Vocabulary additions (`SUB_BEAT_OF` + 7 `event.*` sub-types + Node Frontmatter Conventions + Display Names) all landed in `reference/architecture.md` as of 2026-06-08. No vocab work required this session — verify the architecture changes are present on session start, then proceed.
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
