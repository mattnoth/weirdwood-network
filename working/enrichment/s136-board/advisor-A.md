# Advisor A — S136 Enrichment Dip Recommendation

**PICK: Ned's Downfall (`execution-of-eddard-stark`)**

**Ranking: 1. Ned's Downfall → 2. Sack of King's Landing → 3. Blackwater**

---

## Candidate Analysis

### 1. Ned's Downfall — RECOMMENDED #1

**Enrichment yield:** The execution hub itself has only 2 role edges (Ned + Cersei) and 1 beat. The conspiracy substrate that *causes* the execution is minted but causally unwired: `littlefinger-betrays-ned` has 2 total edges and no MOTIVATES/SUSPECTED_OF backwiring; `cersei-orders-ned-s-arrest` has 4 edges but no upstream cause explaining *why* Cersei moved when she did. Unwired entirely: Renly's offer to Ned (a counterfactual hinge), Varys's role as double-informant (SUSPECTED_OF → frame for treason), the Catspaw-dagger chain that pressured Littlefinger, and the exact mechanism by which Joffrey overrode Cersei's mercy deal. WITNESS_IN edges for Sansa and Arya exist only for Sansa at the execution itself; Arya's POV at the moment is unattached. At least 6–8 new edges + 2–3 new sub-beat nodes are readily supportable from Tier-1 text.

**Dead-end-fix value:** HIGH. `littlefinger-betrays-ned` is functionally a dead-end stub — 1 outgoing SUB_BEAT_OF, 1 incoming AGENT_IN, nothing forward-wired to the Joffrey ascendancy or the WO5K arc. Wiring Littlefinger's betrayal forward (ENABLES joffrey-baratheon-ascends-the-throne → ENABLES war-of-the-five-kings) would close the single most important causal gap in the AGOT arc.

**Theory risk:** LOW. The conspiracy facts are on-page in AGOT (Ned's own chapters, Sansa's witness chapter). No R+L=J entanglement. No speculative readings required.

---

### 2. Sack of King's Landing — #2

**Enrichment yield:** Hub is already moderately rich (17 total edges, 4 beats, 10 role edges). Gap is on the upstream MOTIVATES/SUSPECTED_OF layer: Tywin's *calculated* timing (waiting to see who won the Trident before committing) is COMMANDS_IN but lacks a SUSPECTED_OF edge modeling deliberate atrocity as political signal. The wildfire-cache discovery (post-sack, Jaime's secret) is not wired to any downstream consequence. Could add: `tywin-times-the-sack-for-maximum-loyalty-signal` (SUSPECTED_OF), `jaime-discovers-wildfire-caches` sub-beat, and MOTIVATES edges from Elia's murder → Dornish grievance arc.

**Dead-end-fix value:** MEDIUM. The downstream edge (`coronation-of-robert`) exists; the orphan problem is upstream theory-adjacent (Tywin's intent). The Dornish grievance chain (Oberyn's whole arc) is the real payoff, but it crosses into ASOS territory.

**Theory risk:** LOW-MEDIUM. Tywin's exact intent is contested but clearly on-page; Jaime's Bath Chapter is Tier-1. Safe.

---

### 3. Blackwater — #3

**Enrichment yield:** Has 0 upstream causal edges (causally orphaned), but the 2 ENABLES preconditions (`stannis-absorbs-renly-s-host`, `littlefinger-brokers-tyrell-lannister-alliance`) exist — the upstream wiring gap is real but the preconditions are already minted. Internal beats are almost empty: 2 beats covering ~2% of what actually happened (Tyrion's chain gambit, Sandor's desertion, Cersei/Lancel in the holdfast, the Tyrell charge that ends the battle). Each of those is a mintable sub-beat with clear role edges. Rich, but **quantity not quality** — these are narrative events, not load-bearing conspiracy/SUSPECTED_OF material.

**Dead-end-fix value:** LOW-MEDIUM. The three downstream CAUSES edges are already wired. Adding upstream CAUSES (Tyrion's preparations ENABLES wildfire-chain ignition) helps, but the battle's downstream consequences are already captured. The Sandor desertion thread is high-value but strictly character-level, not structural-graph.

**Theory risk:** ZERO. Pure battle logistics. No R+L=J, no secret identity, no prophetic reading. This is the safest pick but also the least structurally impactful.

---

## Why Ned's Downfall Wins

Blackwater is tractable and safe but adds breadth, not depth — its downstream consequences are already wired and the new edges would mostly be battle-beat sub-plots. Sack of KL is already the graph's best-wired hub (17 edges); marginal return of another enrichment dip is lower.

Ned's Downfall has the sharpest dead-end problem in AGOT: `littlefinger-betrays-ned` sits with 2 edges and no forward wire into the Joffrey ascendancy or the WO5K. Fixing that one stub connects three arcs (AGOT Ned-downfall → Joffrey → WO5K) through a single enrichment dip. The conspiracy substrate (Littlefinger's motive chain, Varys as double-agent, Renly's counterfactual offer, Joffrey overriding Cersei's mercy deal) is entirely on-page, Tier-1, and unwired — maximum yield per dip-hour with zero theory risk.
