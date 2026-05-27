# Session 75 — Graph-exercise follow-ups + enrichment direction change

**Date:** 2026-05-26
**Model:** Opus 4.7 (orchestrator) + script-builder (Sonnet 4.6) ×2, run in parallel/background
**Commit:** this endsession commit
**Session-results:** `working/session-results/2026-05-26-graph-followups.md`

## Purpose

Picked up via `/continue` ("what's next? I missed the handoff"). The S74 handoff (`progress/continue-prompts/2026-05-26-graph-exercise-followups.md`) queued two $0 deterministic graph builds. Matt approved "both," then mid-session reshaped the forward plan around enrichment.

## What was built (both uncommitted → committed at endsession)

Delegated to two parallel background script-builder agents (no file overlap):

1. **`scripts/graph-conflict-pairs.py`** (+ `tests/test_graph_conflict_pairs.py`, 29 green) — read-only audit over `graph/edges/edges.jsonl`. Groups edges by unordered entity pair, flags semantically incompatible co-occurring types (`INCOMPATIBLE_PAIRS` constant: LOVES×HATES, ALLIES_WITH×OPPOSES, TRUSTS×DISTRUSTS, PROTECTS×ATTACKS/ASSAULTS), tracks same- vs opposite-direction. Output: `working/wiki/data/graph-conflict-pairs.{md,jsonl}`. **Result: 1,978 pairs → 32 flagged** (14 same-dir / 11 opposite / 7 both). Does NOT modify edges.jsonl.

2. **`scripts/graph-query.py`** EXTENDED (not overwritten) — the file already existed from Session 39 (656-line node-inspection tool reading node `## Edges` sections + `cross-references.jsonl`). Surfaced this collision before touching it (the S74 continue prompt assumed the file didn't exist). Preserved all S39 modes; made the positional slug optional; added `--neighbors` / `--path` / `--health` / `--edges` reading the canonical `edges.jsonl`. `tests/test_graph_query_edges.py` (29 green); full suite **920 green**, no regressions.

`--health` on real data: 8,299 node files · 3,811 edges · 898 endpoints · **0 orphans** · 105 edge types (GUEST_OF 404, OPPOSES 265, SERVES 255 lead) · degree leaders jon-snow 317, tyrion 315, dany 248, cersei 229, arya 198.

## Key finding — conflicts are temporal arcs, not errors

The 32 flagged pairs are dominated by relationships that legitimately change across the 5 books: Dany→Jorah TRUSTS(AGOT)+DISTRUSTS(ADWD); Catelyn→Littlefinger pre/post-betrayal; Tyrion→Bronn tactical-trust + sellsword-wariness. Only a handful are true mis-attributions (e.g. `catelyn-stark → tyrion-lannister` TRUSTS sourced from a Jaime/Cleos-Frey line). This validates the S74 read: **the real structural fix is per-edge temporal scoping, not deletion.**

Verified the temporal idea is largely DETERMINISTIC: all 3,811 edges already carry `evidence_book` + `evidence_chapter`; chapter frontmatter carries `chapter_number` (global in-book reading order). So a `(book_order, chapter_number)` temporal key can be derived at $0, which would reclassify cross-time "conflicts" as resolved arcs and shrink the true-conflict set sharply.

## Direction change — enrichment un-shelved

Two Matt messages reframed the plan:
1. **Enrichment is wanted** — softens the S74 "NO-GO/SHELVED" Active Decision to a *deferral*. Step by step; **Events is the next surface**; gated behind "the recommended changes before we do that take effect" (= the conflict-pair precision cleanup + the kept v5 precision rules). Captured in memory `project_enrichment_wanted_events_next`.
2. **Endorsed temporal flagging** ("when a particular edge applies — shrewd idea").
3. At session close, chose to **end here and set the next continue prompt to edge enrichment with Events**, rather than launch an unattended run tonight.

Note: I would NOT have launched the full ~$270 Events bulk blind overnight — it failed the 75% precision gate (S74 smokes 74.5%/62.5%) and that contradicts the project value "a wrong cited edge is graph pollution." The Events continue prompt is written to fold in the precision groundwork (conflict-pair cleanup + temporal scoping + v5 rules) BEFORE/with any scaled spend.

## Next

`progress/continue-prompts/2026-05-26-stage4-events-enrichment.md` (Events edge enrichment, precision-gated). The 32-pair review queue + temporal-scoping build are the precision precursors folded into that track.
