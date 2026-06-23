---
session: 133
date: 2026-06-22
track: graph
model: Opus 4.8 orchestrator + Sonnet 4.6 fan-out/verify subagents + 1 Opus A/B agent
title: Enrichment phase opens — harvest on-ramp + first major-arc enrichment (Robert's Rebellion) + a Sonnet-board-vs-Opus A/B
---

# Session 133 — Enrichment phase opens

## Purpose
First session of the **enrichment phase** (all 5 containers spine-complete + low-value remainders cleared as of S132).
Per Matt's sequencing: one enrichment dip per session; descent = major arcs → sub-plots → characters. STEP 0 =
harvest-consume on-ramp; STEP 1 = first major narrative-arc enrichment. Matt also requested a **model A/B**: after the
standard dip, re-run the same enrichment with a "super-max-effort Opus" agent to see if the high-effort tier differs.

## STEP 0 — harvest on-ramp (the fix for silent accumulation)
The 33 open harvest rows (18 Bran + 9 Victarion-voyage + 6 N6) were consumed FIRST, by 3 parallel Sonnet
general-purpose subagents (disjoint node sets, no write conflict). Result: **31 attached + 2 no-op dups, 0 homeless.**
- Mostly **book-cite overlays** onto wiki-cited prose (the high-value pattern) + appearance/description/foreshadowing
  attachments to existing nodes (Victarion, Moqorro, dragonbinder, Arnolf, Bran beats, Bloodraven cave-form, etc.).
- 4 cite-drifts corrected at attach; the N6 subagent attached but didn't flip its 6 queue rows → orchestrator flipped them.
- **Rule-#9 catch:** the continue prompt said weirwood-paste / black-gate / cave-of-the-three-eyed-crow were
  "mint candidates, defer" — all 3 already exist as nodes. So no deferred mints; all rows had existing homes.
- Bran-resonance flagged: the frozen-lake-island weirwood ("frozen blood") at Stannis's stall site (N6) — attached as
  prose only, no cross-container edge (a later Bran/cross-container dip can consider one).

## STEP 1 — arc selection: a 3-advisor board (Matt-requested)
Matt asked to "fan out an advisory board on which arc to do — or demand-dip." Ran 3 independent, graph-grounded Sonnet
advisors, each a distinct lens: **A = off-spine yield · B = leverage/connectivity · C = reader-importance/theory-substrate.**
**Unanimous verdict: Robert's Rebellion.** Convergent rationale: RR is rich wiki prose but a barren causal/revelation
layer (the cluster head `roberts-rebellion` had 1 outgoing edge — junk), anchoring the two deepest mysteries
(R+L=J, Jon Arryn's murder), with its downstream into present-day arcs = 0 edges. C flagged **Essos as the trap**
(theory-entangled). Reconciled an A-vs-B discrepancy (rule #9): the RR participant layer DOES exist (S97 historical-anchor
backfill — Trident 16, ToJ 10, Harrenhal 25, Sack 14); Advisor A's "0/0" was a `--event-participants` artifact (it counts
reified beats, not FIGHTS_IN/ATTENDS). So participant edges were NOT re-minted.

## STEP 1 — the enrichment machine
3 fresh Sonnet lenses (causal/downstream · SUSPECTED_OF/WITNESS substrate · new-nodes/depth), all sharing a written
dedup baseline (`working/enrichment/rr/baseline.md`), PROPOSE-only. Orchestrator synthesized → `synthesis.md` (locked set,
every quote line-checked) → script-builder minted via `scripts/mint_rr_enrichment_s133.py` (backup + re-run guard +
precheck_slugs) → verify-edge-quotes (4 smart-quote flags fixed to byte-exact spans → 0 drift) → `weirwood refresh` →
**independent fresh-verify** (a 4th Sonnet agent, not a proposer) → applied verdicts via `finalize_rr_enrichment_s133.py`.

**Shipped:** 3 nodes (`knight-of-the-laughing-tree-incident`, `exile-of-jon-connington`, `murder-of-jon-arryn`) +
22 edges (−1 junk `GUEST_OF` drop, −1 ENABLES rejected at fresh-verify) + 4 book-cite overlays + 1 alias kebab→spaced fix.
Fresh-verify = **6 CONFIRM / 2 ADJUST / 1 REJECT:**
- REJECT **E4** `wedding-of-robert-and-cersei ENABLES death-of-robert-baratheon` — agency-collapse + ungrounded in the
  cited line (the RR→WO5K death-link is deferred to a properly-sourced MOTIVATES from Cersei's later chapters).
- ADJUST **E2** `exile-of-jon-connington ENABLES aegon-revealed` tier 1→2 (cross-book inferential bridge).
- ADJUST **E21** `lyanna SUSPECTED_OF kotlt-incident` re-anchored to the she-wolf line (asos-bran-02:187), the real
  identity signal, off Jojen's weaker hint.
- Orchestrator nit fixed: **E9** rhaegar AGENT_IN kotlt quote → the "dragon prince to seek the man" span.

**Cross-arc bridges now traverse:** RR→AEGON (`battle-of-the-bells CAUSES exile-of-jon-connington ENABLES aegon-revealed
→ … → landing/siege/assassinations`) + RR→WO5K (`coronation ENABLES wedding-of-robert-and-cersei`). Jon-Arryn-murder
reified (lysa AGENT_IN T1; petyr + cersei SUSPECTED_OF T2 — instigator + the false in-world misdirection); R+L
contested-agency `rhaegar SUSPECTED_OF abduction-of-lyanna` (theory held gated; opposing testimony attached as node prose).

## The A/B experiment — Sonnet board vs. max-effort Opus
One **Opus** agent did the ENTIRE RR scope as a single blind pass (deduped vs baseline.md only; did not read the
lens/synthesis files; treated the parallel-minted nodes as non-existent). Proposal: `proposal-opus-ab.md` (51 items).
**Verdict — modest but real difference; orchestration > proposer-tier:**
- **~90% convergence on the high-value core** — same 3 nodes, same RR→AEGON bridge, same Jon-Arryn substrate, same ToJ
  witnesses, same overlays, same junk-drop, same `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` NEEDS_VOCAB hold. **Validates the
  cheaper Sonnet board.**
- **Opus caught a coverage SEAM the lens-division missed:** causal edges between *already-existing* nodes that no single
  topic-lens owned. Two were genuine structural-gap fixes and were **minted as A/B bonus** (`mint_rr_ab_bonus_s133.py`,
  run_id `rr-enrichment-s133-ab`): `roberts-rebellion MOTIVATES robert-orders-daenerys-assassination` (the RR hub's FIRST
  real outgoing edge — and a clean RR→Essos seam) + `wildfire-plot MOTIVATES slaying-of-aerys-ii-the-kingslaying`
  (Jaime's stated motive for the kingslaying). Both line-verified, 0 drift.
- Opus was slightly NOISIER on dedup (re-proposed 4 already-existing nodes; would have needed a synthesis pass to filter).
- **Caveat (not a clean RCT):** the Sonnet path also had Opus synthesis + a fresh-verify layer; the Opus path was a raw
  single agent. Honest lesson: **the model tier of the proposal agents is not the bottleneck — the orchestration is.** The
  lens DIVISION created the only real gap.
- **Action banked:** ADD a 4th "existing-node↔existing-node causal-wiring" lens to the enrichment board (don't default to
  Opus-as-proposer). Memory `feedback_enrichment_board_causal_lens`. **Bigger-scope option Matt raised** (OPEN, see below).

## Final graph state
edges.jsonl 22,497 → **22,520** (+24 RR net, −1 junk); 8,602 nodes (+3); 62 orphans (unchanged — 0 new); 132 edge types
(no new). All 24 S133 edges pass verify-edge-quotes (0 drift). Indexes + alias resolver rebuilt.

## OPEN decisions (Matt fired /endsession mid-clarification — these are unanswered)
1. **Causal-wiring scope** — is the fix the in-dip 4th lens (arc-scoped), a standing graph-wide causal-wiring track
   (cross-arc, its own pass — analogue of the S97 historical-anchor *participant* backfill, but for *causal* edges), or
   both? The two A/B-found edges were cross-arc, which only the standing track reliably catches. Matt: "bigger than it
   seems." AskUserQuestion options A–D presented; he asked "what is KotLT" then fired /endsession before answering.
2. **The off-vocab `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge** (rhaegar→lyanna, the Harrenhal crowning, agot-eddard-15:45) —
   provenance is the auto-generated Stage-4 tail-LLM (`run_id tail-llm-20260523`, candidate_kind pass1_relationship),
   NOT a deliberate decision; it's pre-lockdown off-vocab leakage. Options: convert to a `crowning-of-lyanna-at-harrenhal`
   beat-node (honoree role = NEEDS_VOCAB) / leave tolerated+flagged / add a locked ceremonial-honor type via Active
   Decision. Unanswered. (Context Matt recalled: the Harrenhal/KotLT *node* cluster was discussed in the S28/S29 audits —
   KotLT stays a separate node from Lyanna, identity gated — but the CROWNS *edge* itself was never decided.)

## Hygiene flag (low severity, pre-existing — NOT this session)
verify-edge-quotes reports **58 whole-graph mismatches**, concentrated in the May-2026 Stage-4 bulk runs
(`pass1-derived-20260523`, `tail-llm-20260523*`, `pass1-extra-tables-20260525`) — a mix of attribution/offset
false-positives and genuine paraphrase drift. A rougher probe suggests the near-miss set is larger. Candidate for a
dedicated "quote re-grounding" cleanup pass; out of scope for enrichment.

## Artifacts
`working/enrichment/rr/{baseline,synthesis,proposal-lens1,proposal-lens2,proposal-lens3,proposal-opus-ab}.md`;
`scripts/mint_rr_enrichment_s133.py`, `scripts/finalize_rr_enrichment_s133.py`, `scripts/mint_rr_ab_bonus_s133.py`;
backups in `graph/edges/_regrounding/edges-pre-rr-{enrichment,quotefix,finalize,ab-bonus}-2026-06-22.jsonl`.
