# Repo Audit + Strategy Reconciliation + Memory Consolidation

> **Recommended model:** Opus 4.7 — this is judgment-heavy reconciliation across 84 sessions of accumulated state; not mechanical.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **TIMING:** Run AFTER Plate 3 (edge-modeling reification full sweep) completes, so the audit reflects a settled edge-layer state, not a mid-flight one. Until then this is queued, not active.
> **MODE:** Read-only proposals FIRST → Matt approves → then apply. Do NOT mass-edit worklog/memory/continue-prompts without showing the diff first. Source data stays read-only/additive (CLAUDE.md hard rule).

## Why
84 sessions have left strategy sediment: multiple edge strategies layered over each other, stale worklog checkboxes, superseded continue prompts, and point-in-time memory entries. Matt's concern (2026-06-07): "disjointed strategies… I don't want to lose this direction." The edge-modeling reification direction (S82-84) is the current through-line and must end up as the unambiguous canonical thrust.

## Scope (produce a proposal doc per item, then apply on approval)

1. **Edge-strategy reconciliation map.** One authoritative statement of the CURRENT edge strategy + how the dead branches relate, so a fresh session can't be confused:
   - wiki-comention → DEPRECATED (S65)
   - Pass-1-derived deterministic spine → SHIPPED `graph/edges/edges.jsonl` v1.3 (3,811); reification operates ON this
   - Events Haiku bulk → NO-GO (S81); absorbed by Plate 4, not promoted as-is
   - Stage-4 LLM enrichment (Events/Dialogue) → SHELVED (S74)
   - edge-modeling reification → ACTIVE (S82-84); the current direction
   (Memory entry `project_edge_modeling_reification_direction` already captures this — verify it's still accurate post-Plate-3 and is THE reference.)

2. **Worklog Current State cleanup.** Fix stale/contradictory checkboxes — e.g. `[ ] Pass 2 wiki ingestion agent prompt written` and `[ ] Pass 2 wiki ingestion complete` sit above the completed Stage 1-3 lines. Reconcile every `[~]`/`[ ]` against reality. Don't delete history; correct state.

3. **Active Decisions cleanup.** Re-tag resolved/superseded ones (e.g. the Events Haiku "OPEN" decision is largely absorbed by Plate 4; D2 is RESOLVED). Keep genuinely-open ones.

4. **Continue-prompt hygiene.** Archive/remove superseded prompts + their `→ continue:` links in todos.md: `2026-06-04-edge-modeling-cleanroom-execution.md` (executed), `2026-06-01-events-bulk-escalation-pick.md` (reframed), `2026-05-31-events-v2-promotion-chain/` (halted/superseded by Plate 4). Confirm each is truly done before removing.

5. **Memory consolidation.** Run `anthropic-skills:consolidate-memory` (merge dupes, fix stale completion-state claims, prune the index). Pay attention to the entries that assert completion state (they're snapshots) — reconcile against worklog. Confirm the reification-direction entry is present + accurate.

6. **Repo structure audit (lighter touch).** Scan `scripts/` (132 files; ~40 stage4-*, 27 comention kept as a recall lever — do NOT re-propose archiving those per S73), the `working/edge-modeling/` staging (what's promotable vs throwaway), the skeleton-untrack decision (7,180 tracked stale skeletons — its own decision, deferred), and the `_conflicts/` quarantine. Produce a findings list, not mass edits.

## Done-criteria
- A single canonical "current direction" statement exists and is linked from worklog + memory.
- Worklog Current State has zero contradictory checkboxes.
- Stale continue prompts archived; todos `→ continue:` links accurate.
- Memory consolidated; reification-direction entry verified.
- A repo-structure findings list for Matt to triage (no surprise deletions).

## Out of scope
- Touching `graph/` data (this is doc/state hygiene, not graph edits).
- The top-level `scratch*` files (Matt's private notes — do not read/act per CLAUDE.md).
- Re-running any extraction or LLM pass.
