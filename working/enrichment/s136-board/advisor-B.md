# Advisor B — S136 Arc Enrichment Recommendation

**PICK: Ned's Downfall** (`execution-of-eddard-stark`)

**Ranking: 1. Ned's Downfall → 2. Sack of King's Landing → 3. Blackwater**

---

## Per-candidate assessment

### 1. Ned's Downfall (execution-of-eddard-stark) — RECOMMENDED #1

**Enrichment yield:** The conspiracy substrate is already minted but disconnected: `littlefinger-betrays-ned` has exactly 2 edges total (1 in, 1 out) and zero CAUSES link forward to the execution; `ned-discovers-the-truth-of-joffrey-s-parentage` has 3 edges but no CAUSES edge forward to the arrest (the causal link is simply absent). Varys — who visits Ned in the black cells, confirms Cersei's role in Robert's death, and shapes whether Ned confesses — has zero edges into the execution event node. Renly's throne-room offer (the fork that Ned refuses), which is a direct upstream cause of his vulnerability, has no event node at all. The Janos Slynt bribery chain (Cersei pays Slynt; Slynt commands gold cloaks; gold cloaks betray Ned) is partially minted but causally unlinked from Cersei's decision to move against Ned.

**Dead-end fix value:** This is the thinnest causally wired hub of any series-defining event. The `robb-proclaimed-king-in-the-north` and `war-of-the-five-kings` downstream are live but floating — the whole WO5K dead-end closes here. Adding SUSPECTED_OF (was Littlefinger always planning to let Ned die even if he confessed?), WITNESS_IN (Arya at the Sept), and the Varys-visits-Ned sequence would wire this node forward AND backward with high-density, high-confidence edges.

**Theory risk:** Negligible. The betrayal actors (Littlefinger, Janos Slynt, Cersei, the gold cloaks) and their motivations are Tier-1 on-page. Varys's deeper game is gated — only his observable cell-visit actions are fair game, not his endgame theory.

---

### 2. Sack of King's Landing (sack-of-kings-landing) — #2

**Enrichment yield:** Solid. The atrocity sub-events (Elia/Aegon/Rhaenys murders) are minted and well-wired (9 edges on the murder node). The wildfire-plot → kingslaying chain is wired forward. What's missing: the wildfire-cache-discovery seam that Jaime confesses in ASOS (his trauma monologue), a SUSPECTED_OF edge for Tywin's calculated timing (arriving after the battle was decided, not to help Robert but to secure Lannister loyalty), and the downstream Dorne seam (Elia's death MOTIVATES the entire Martell arc). 

**Dead-end fix value:** Moderate. The Sack already has 14 incoming edges — it is not a dead-end hub. The bigger gap is its downstream: only 1 CAUSES edge out (coronation). The Dorne seam and Jaime-trauma thread are the high-value additions, but they are specific sub-arcs, not a broad unwired conspiracy layer.

**Theory risk:** Low. SUSPECTED_OF on Tywin's timing is defensible at Tier-2 (Jaime text supports it explicitly). Aegon/Young Griff connection is gated — don't go near it.

---

### 3. Blackwater (battle-of-the-blackwater) — #3

**Enrichment yield:** Good narrative texture — Sandor's desertion, Sansa's thread, Tyrion's chain gambit, the Cersei/Lancel dynamic — but most of these are character-layer enrichments, not causal wiring. The battle is already the strongest in terms of downstream edges (3 CAUSES out, 5 total outgoing). Sub-events like `fleet-forms-battle-lines` and `a-knight-attacks-tyrion-s-shield` are already minted.

**Dead-end fix value:** Lower priority. The battle's 0 upstream causal edges is a real gap, but it already has 2 ENABLES preconditions (Tyrell alliance + Stannis absorbs Renly's host) — the upstream story is told via a different edge type. The Sandor-desertion and Sansa threads, while dramatically vivid, lead forward into character arcs (Sansa's captivity, Hound's wandering) that are better served by character-unit enrichment, not a battle-arc dip.

**Theory risk:** Zero. Cleanest candidate for theory contamination, but that strength matters less when yield and dead-end-fix value are lower.

---

## Why Ned's Downfall wins

The Ned execution is the series hinge — everything downstream (WO5K, Robb's arc, Sansa's captivity, Arya's exile) flows from it, yet its conspiracy layer is almost entirely unwired. Four named actors (Littlefinger, Varys, Janos Slynt, Cersei) have nodes, participate in events that are already minted, but the causal chain connecting their decisions to the execution event is broken in multiple places. A single enrichment dip here closes more graph traversal dead-ends per edge minted than either alternative, at low theory-entanglement risk, using entirely Tier-1 book evidence that is already cited in the chapter files.
