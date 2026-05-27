# Session 75 — Graph-exercise follow-ups (conflict-pair audit + query tool)

**Date:** 2026-05-26
**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2 (background, parallel)
**Spend:** ~$0 (both builds deterministic, no LLM); orchestration only
**Source continue prompt:** `progress/continue-prompts/2026-05-26-graph-exercise-followups.md`
**Status:** Both builds COMPLETE + verified. UNCOMMITTED (awaiting Matt).

## What shipped (uncommitted)

### Task 1 — conflict-pair audit (HIGHEST VALUE)
- NEW `scripts/graph-conflict-pairs.py` + `tests/test_graph_conflict_pairs.py` (29 tests green).
- Read-only over `graph/edges/edges.jsonl`; **does NOT modify it**.
- Outputs: `working/wiki/data/graph-conflict-pairs.md` (reviewer-facing) + `.jsonl` (machine).
- **Result: 1,978 pairs analyzed → 32 flagged** (14 same-direction = strongest signal, 11 opposite-only, 7 both).
  - By type: DISTRUSTS×TRUSTS 15 · ALLIES_WITH×OPPOSES 12 · LOVES×HATES 5 · PROTECTS×ASSAULTS 3.
  - All 9 incompatibility types confirmed present in the data (no dead entries).
- `INCOMPATIBLE_PAIRS` is a conservative, easily-extended module constant. Same- vs opposite-direction is tracked per pair (`conflict_directionality`).

### Task 2 — graph query tool
- EXTENDED existing `scripts/graph-query.py` (S39, 656-line node-inspection tool) **without overwriting** — original positional/`--edges-only`/`--inbound-only`/`--json` modes preserved; positional slug made optional so new flags run standalone.
- NEW `tests/test_graph_query_edges.py` (29 tests). **Full suite: 920 green, no regressions.**
- New modes read canonical `graph/edges/edges.jsonl`:
  - `--neighbors <slug>` — incoming/outgoing edges grouped by type, with `evidence_ref` + quote.
  - `--path <slugA> <slugB>` — direct edges + 2-hop bridges (type on each leg), capped 50.
  - `--health` — node/edge counts, edge-type distribution, orphan audit, degree leaders.
  - `--edges <path>` override; all honor `--json`.

## --health snapshot (real data)
- 8,299 node files · 3,811 edges · 898 unique endpoints · **0 orphans** (confirms S74).
- 105 edge types. Top: GUEST_OF 404, OPPOSES 265, SERVES 255, DISTRUSTS 204, HATES 173.
- Degree leaders: jon-snow 317, tyrion-lannister 315, daenerys-targaryen 248, cersei-lannister 229, arya-stark 198.

## Key finding — the 32 conflicts are mostly TEMPORAL ARCS, not deletions
The flags cluster on relationships that genuinely change across 5 books:
- Dany→Jorah: TRUSTS (AGOT) + DISTRUSTS (ADWD post-exile) — both correct.
- Catelyn→Littlefinger: TRUSTS (AGOT) + DISTRUSTS (ACOK post-betrayal).
- Tyrion→Bronn: TRUSTS (tactical) + DISTRUSTS (sellsword wariness), same period.

This validates the S74 read: the real structural fix is **edge temporal-scoping** (per-edge chapter anchor → relationship-phase queries), not auto-delete. A *few* look like genuine mis-attributions to correct manually (e.g. Catelyn→Tyrion TRUSTS sourced from a Jaime/Cleos-Frey line — wrong pair/label).

## How this connects to enrichment (Matt, this session)
Matt confirmed he DOES want enrichment — step by step, **Events next**, but **gated behind the precision changes landing first** and **not this session**. This conflict-pair audit IS the first of those precision changes (clean the core before layering). Captured in memory `project_enrichment_wanted_events_next`.

## What's next
- **Matt decides:** review the 32-pair queue → apply the handful of true mis-attribution corrections to `edges.jsonl` (show before/after) vs. leave as-is pending temporal-scoping.
- Commit decision (everything currently uncommitted).
- Deferred (bigger): **edge temporal-scoping** design — the real fix the audit points to.
- Future session: precision-gated **Events enrichment**.
