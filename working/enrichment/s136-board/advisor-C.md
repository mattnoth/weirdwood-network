# Advisor C — S136 Arc Pick

**PICK: Ned's Downfall (`execution-of-eddard-stark`)**

**Ranking: 1. Ned's Downfall → 2. Blackwater → 3. Sack of King's Landing**

---

## Candidate Analysis

### 1. Ned's Downfall — PICK #1

**Enrichment yield:** Highest of the three. The causal chain has 5 edges (3 upstream + 2 downstream), but the PARTICIPANT layer is almost bare: 2 role edges, 2 distinct participants. The conspiracy that *produces* the execution — Littlefinger pre-bribing Janos Slynt, the gold cloaks turning on Ned's household, Cersei's order to arrest, Renly's offer that Ned refused, Varys threading both sides, the throne-room massacre — is almost entirely unwired at the event hub. `littlefinger-betrays-ned` exists but is explicitly flagged as staging-only with role edges unpopulated; `gold-cloaks-betray-ned` is the same: staging stub, no role edges, no upward causal wiring into the arrest or execution. The `SUSPECTED_OF` tool is tailor-made for Littlefinger's role as hidden architect and for Varys's unknowable complicity.

**Dead-end fix value:** Extremely high. The execution node has one `CAUSES` downstream (Robb proclaimed King in the North) — but this is the event that detonates the entire wo5k container. The execution *should* radiate out to Catelyn's grief-arc, Arya's flight, Sansa's captivity, and the general North/South split. All of those nodes exist; the edges don't.

**Theory risk:** Essentially zero. Every beat — the double-cross, the throne-room fight, Ilyn Payne — is Tier-1 book text across AGOT Eddard XIII/XIV and Arya V/Sansa VI. Nothing here requires theory readings.

**Double-dip risk:** None. S133 was Robert's Rebellion (pre-conquest era). This arc is AGOT narrative.

---

### 2. Blackwater — #2

**Enrichment yield:** Good but bounded. The event hub has 0 upstream causal edges — causally orphaned — and only 2 ENABLES preconditions. A dip can wire Stannis's path from Renly's death → Storm's End → the march south, add the Sandor-desertion thread, the Tyrion-Mandon-Moore assassination attempt (SUSPECTED_OF: Cersei or Joffrey), and the Sansa/Hound tower scene. That's real material. The node is rich in prose and quotes; the gap is the role-edge layer (4 role edges across 4 participants for a battle with dozens of named commanders).

**Dead-end fix value:** High. Fixing the 0-upstream causal orphan alone makes this worth doing. The Tyrell alliance as enabling condition is already wired via `littlefinger-brokers-tyrell-lannister-alliance`, but Stannis's full approach sequence isn't.

**Theory risk:** Zero. This is the cleanest battle in the series for Tier-1 substrate.

**Why it's #2 not #1:** More of the interesting material is already in the node's prose (the Narrative Arc and Origins sections are extremely detailed); the *graph* gap is real but narrower than Ned's downfall. The execution's conspiracy web is genuinely hollow; Blackwater's main hub is well-described, just under-edged.

---

### 3. Sack of King's Landing — ACTIVELY AVOID

**Enrichment yield:** Superficially attractive but severely compromised by overlap. The key sub-beats — `slaying-of-aerys-ii-the-kingslaying`, `murder-of-elia-martell-and-rhaegars-children`, `aerys-commands-the-city-burned`, `pycelle-opens-the-gates-of-kings-landing`, `wildfire-plot` — are all **already minted, identity-filled, and role-wired** from the S133 Robert's Rebellion pass. The node already has 39 edges in `edges.jsonl` referencing Sack sub-events. A dip here would mostly re-verify what S133 already landed.

**Remaining gaps are thin:** The main un-wired threads — Qarlton Chelsted's resignation and murder, Jaime killing Belis/Garigus post-Sack, Doran Martell's secret Targaryen restoration plotting as downstream of Elia's death — are real but minor compared to Ned's conspiracy web. The Chelsted sub-beat is interesting (`SUSPECTED_OF` on Tywin for Chelsted's death?) but doesn't light up a causally-thin hub.

**Theory risk:** The "Young Griff = Aegon" thread is attached to this event's wiki node and tempts theory-gated reading. A dip risks pulling that in.

---

## Why My #1 Wins

Ned's downfall is the series' most consequential unwired event: the gap between its 11 total graph edges and the actual richness of the conspiracy is the largest mismatch of any ready candidate. S133 cleared the RR/Sack quadrant well; this is the next highest-value hollow hub. Blackwater is a legitimate #2 and a cleaner build, but fixing a 0-upstream orphan is less urgent than wiring the betrayal-conspiracy that ignites the entire war. Skip the Sack entirely — the yield is marginal and the double-dip risk is real.
