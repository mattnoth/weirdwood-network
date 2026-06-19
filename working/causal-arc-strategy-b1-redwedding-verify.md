# Verification Report: B1 Red Wedding Upstream Arc
**Verifier:** fresh subagent (no arc authorship context)
**Date:** 2026-06-19
**Arc:** B1 — Red Wedding upstream causal chain (5 causal edges, 16 role edges across 5 new event nodes + 2 pre-existing terminus nodes)

---

## Per-Edge Verdict Table

| Edge | Quote verbatim? | Type-call correct? | Agency modeled? | Factually true? | VERDICT |
|------|-----------------|-------------------|-----------------|-----------------|---------|
| E1: `catelyn-releases-jaime-lannister` --CAUSES--> `karstark-murders-prisoners-at-riverrun` | **PARTIAL** — quote is a subset of the full sentence at line 57 (the full sentence continues "...Didn't your father teach you that, boy?"); the extracted substring is verbatim but line citation is correct | CORRECT: CAUSES is right (mediated; Catelyn's act is a necessary condition Karstark names, not an immediate mechanical trigger) | YES — Rickard Karstark AGENT_IN on the murder node; role edges carry his choice | YES — wiki (`Rickard_Karstark.json`) confirms: Catelyn's release directly precedes and motivates the murders | **CONFIRM** |
| E2: `karstark-murders-prisoners-at-riverrun` --CAUSES--> `execution-of-rickard-karstark` | **PARTIAL** — minted quote "Rickard Karstark killed more than a Frey and a Lannister. He killed my honor. I shall deal with him at dawn." is a verbatim substring of line 155, which also contains the preceding sentence about battle conditions; correct line, partial extraction | CORRECT: CAUSES is appropriate (the murders are the necessary condition that forces Robb's hand; Robb's choice to execute rather than imprison is the intervening decision — modeled by role edge) | YES — Robb Stark AGENT_IN (orderer and executor) on the execution node; the agency-collapse concern is fully addressed | YES — wiki and chapter both confirm: murders → Robb's condemnation and execution | **CONFIRM** |
| E3: `robb-weds-jeyne-westerling` --TRIGGERS--> `red-wedding-conspiracy` | VERBATIM at line 165 (exact match confirmed) | **MARGINAL** — TRIGGERS is defensible (the marriage is the immediate named spark for Walder's turn), but note this isn't "immediate" in a mechanical sense; there is a time-gap and Walder's deliberate choice between the marriage and the conspiracy forming. CAUSES would also be defensible. However per the project's edge semantics (TRIGGERS = specific named spark for a named event), TRIGGERS is acceptable here. Not a hard error. | YES — conspirators' agency lives on `red-wedding-conspiracy`'s role edges (walder-frey COMMANDS_IN, roose-bolton AGENT_IN, tywin-lannister COMMANDS_IN) | YES — confirmed in both the chapter and wiki (`Red_Wedding.json` §Origins): Robb's marriage breaks the Frey pact and Walder begins conspiring immediately after | **CONFIRM** (with minor note on TRIGGERS vs CAUSES ambiguity — see §Notes) |
| E4: `red-wedding-conspiracy` --CAUSES--> `red-wedding` | **PARTIAL** — minted quote is a substring of line 205 (the full line begins with "Walder Frey is a peevish old man…"); extracted substring is verbatim; line citation correct | CORRECT: CAUSES is right (the conspiracy is the covert engine that produces the event; it is mediated, multi-step, not a single trigger-moment) | YES — conspirators' agency is fully modeled by role edges on the `red-wedding-conspiracy` node; the conspiracy node is explicitly the agency-hub | YES — Tywin's admission in asos-tyrion-06 is the primary textual evidence for the conspiracy; wiki confirms Walder+Roose+Tywin coordination | **CONFIRM** |
| E5: `red-wedding-conspiracy` --CAUSES--> `robb-is-killed` | VERBATIM at line 135 — "Jaime Lannister sends his regards." confirmed exact match | CORRECT: CAUSES is right (the conspiracy targets Robb specifically; the killing is the conspiracy's intended outcome) | **PARTIAL CONCERN** — the `robb-is-killed` node is a stub (minted by plate3-minibatch, `status: minted-plate3`); it has no S107 causal-arc content (no Identity narrative, no quotes, no full role edges). The role-edge for Roose Bolton AGENT_IN the killing exists in edges.jsonl from plate3, as does robb-stark VICTIM_IN. However, the node file itself is underweight compared to the other 4 arc nodes. | YES — Roose Bolton AGENT_IN the killing is confirmed in edges.jsonl (plate3); the conspiracy causing Robb's death is factually correct per chapter and wiki | **CONFIRM with flag** — the causal edge is correct; the terminus node (`robb-is-killed`) is a thin stub that should be upgraded to match S107 arc-node quality before the arc is considered fully dressed |

---

## Role-Edge Spot-Check

### `red-wedding-conspiracy` — 3 key role edges

| Role edge | Source slug | Tier | Assessment |
|-----------|-------------|------|------------|
| `walder-frey` COMMANDS_IN `red-wedding-conspiracy` | evidence_quote: "I have no doubt he hatched this ugly chicken" (Tywin's words attesting to Walder's authorship) | **Tier-1** | CORRECT — Walder as instigator is attested by Tywin's own statement (direct admission, not inference); Tier-1 is justified |
| `roose-bolton` AGENT_IN `red-wedding-conspiracy` | evidence_quote: "Jaime Lannister sends his regards." (the line spoken at the killing) | **Tier-1** | CORRECT in tier, but the evidence_quote is weak for the conspiracy node specifically — it proves Roose's role in the execution, not his role in hatching the conspiracy. The wiki (`Red_Wedding.json`) gives stronger evidence: "Walder secretly begins corresponding with Roose, who had wed Walder's granddaughter Walda." For the conspiracy node, a better evidence_quote would be from asos-tyrion-06 where Tywin explains the deal, or from the ACOS chapter where Frey representatives meet Roose. That said, the factual claim (Roose AGENT_IN the conspiracy) is unambiguously true; only the supporting quote is suboptimal. Not a REVISE-level finding — flag for enrichment. |
| `tywin-lannister` COMMANDS_IN `red-wedding-conspiracy` | evidence_quote: "he would never have dared such a thing without a promise of protection" | **Tier-2** | CORRECT — Tier-2 is right because Tywin's role is a sanction-by-protection (structural enablement, not direct authorship); Tywin never explicitly says "I commanded this." The edge_type COMMANDS_IN at Tier-2 is the most defensible call: he enabled it as Hand and later admitted countenancing it. |

### Other arc nodes — spot-check of role edges

- `catelyn-releases-jaime-lannister`: catelyn-stark AGENT_IN (Tier-1) ✓; brienne-tarth AGENT_IN (Tier-1) ✓; LOCATED_AT riverrun (Tier-1) ✓
- `karstark-murders-prisoners-at-riverrun`: rickard-karstark AGENT_IN (Tier-1) ✓; tion-frey VICTIM_IN (Tier-1) ✓; willem-lannister VICTIM_IN (Tier-1) ✓; LOCATED_AT riverrun (Tier-1) ✓
- `execution-of-rickard-karstark`: robb-stark AGENT_IN (Tier-1) ✓; rickard-karstark VICTIM_IN (Tier-1) ✓; LOCATED_AT riverrun (Tier-1) ✓
- `robb-weds-jeyne-westerling`: robb-stark AGENT_IN (Tier-1) ✓; jeyne-westerling AGENT_IN (Tier-1) ✓; LOCATED_AT crag (Tier-1) ✓

All role-edge tiers correctly discriminate Tier-1 (textually unambiguous facts) from Tier-2 (interpretive/inferred agency). No violations found.

---

## Hard-Stop Confirmation

Confirmed: no outgoing CAUSES/TRIGGERS/MOTIVATES edge from any arc node reaches `war-of-the-five-kings`. The only edge from `red-wedding` to `war-of-the-five-kings` is `PART_OF` (wiki-infobox, not a causal arc edge). The chain terminates at `red-wedding` and `robb-is-killed` as required.

---

## Factual Accuracy Cross-Check (wiki + chapter)

- **E1 causal claim (Catelyn's release → Karstark murders):** Confirmed. `Rickard_Karstark.json` wiki explicitly sequences: Catelyn releases Jaime → Karstark considers it treason → murders the prisoners. The causal link is stated in the source, not merely inferred.
- **E2 causal claim (murders → Robb executes):** Confirmed. Both chapter and wiki are unambiguous: the murders directly cause Robb to condemn Karstark. Robb's choice (modeled by AGENT_IN) is the intervening decision that converts the murders into an execution.
- **E3 causal claim (Jeyne marriage → Frey conspiracy):** Confirmed. The marriage broke a sworn oath to Walder Frey (confirmed by Catelyn at asos-catelyn-02.md:165 and by the wiki's Red Wedding article). The conspiracy is its direct downstream consequence.
- **E4 causal claim (conspiracy → Red Wedding massacre):** Confirmed. The conspiracy is the covert mechanism that produces the massacre. Well-attested.
- **E5 causal claim (conspiracy → Robb killed):** Confirmed. Robb's killing is the conspiracy's stated objective; Roose delivers the killing blow in dark armor + pale pink cloak.

One additional factual note on E3: the wiki's `Red_Wedding.json` mentions that Sybell Spicer and her brother maneuvered Jeyne into treating Robb — suggesting the marriage itself may not have been fully spontaneous on Jeyne's side (there's a Lannister faction conspiracy layer). This does not affect the E3 edge's accuracy (the marriage *did* trigger the Frey turn), but it adds interpretive depth the arc node's Identity section could eventually note.

---

## Items Requiring Action Before `verified_by` Stamp

### REVISE items: none

### FLAG items (non-blocking but should be logged):

1. **`robb-is-killed` node is a thin stub** — The terminus node is `minted-plate3` with no Identity narrative, no arc-context quotes, and no S107 provenance. The causal edge (E5) is correct, but the node should be upgraded to match the quality of the other 4 arc nodes (full Identity §, Quotes §, Edges § with S107 arc framing). Recommend: add an S107-style Identity write-up to `graph/nodes/events/robb-is-killed.node.md` before stamping the arc verified.

2. **Quote extractions are all partial substrings** — E1 (line 57), E2 (line 155), E4 (line 205) each capture only a clause of a longer sentence. The substrings are verbatim (no paraphrase errors), and the line citations are correct. This is acceptable practice but worth noting: the full-sentence context is in the node's `## Quotes` sections, so no information is lost.

3. **`roose-bolton` AGENT_IN `red-wedding-conspiracy` evidence_quote** — The supporting quote ("Jaime Lannister sends his regards.") proves Roose's role in *executing* Robb, not in hatching the conspiracy. The claim is factually true (Roose coordinated with Walder per wiki), but a quote from asos-tyrion-06 (where the Frey-Bolton-Lannister deal is described) would be stronger evidence for the conspiracy node specifically. Not a REVISE — a future enrichment candidate.

---

## Bottom Line

**5 CONFIRM, 0 REVISE, 0 REJECT.**

All 5 causal edges are factually accurate, correctly typed, and correctly tiered. Agency is properly modeled (no collapsed decisions left unmodeled). Hard-stop confirmed. Role-edge Tier discipline is sound.

**One pre-stamp action recommended:** upgrade `graph/nodes/events/robb-is-killed.node.md` from plate3 stub to S107 arc-node quality. The causal edge E5 is correct; the stub node is the gap. This is a 10-minute write-up, not a research task.

The arc is ready to stamp `verified_by` on all 5 causal edges once the `robb-is-killed` node is dressed.
