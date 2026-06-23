# RR Enrichment — Lens 1 Proposal: Causal Wiring & Downstream Bridges (S133)

## Summary (5 lines)
**Edges proposed:** 10 NEW edges + 1 DROP + 1 RECAST recommendation.
**Single highest-value bridge:** `coronation-of-robert-i-baratheon ENABLES wedding-of-robert-i-baratheon-and-cersei-lannister ENABLES death-of-robert-baratheon` — this two-hop chain connects the final RR beat to the WO5K arc's opening cause; the wedding node currently has 0 edges in or out.
**Node mints handed to Lens 3:** 1 — `connington-stripped-and-exiled-by-aerys` (new event beat needed to wire battle-of-the-bells → aegon container; see Target 2 below). Once Lens 3 mints it, the CAUSES edges in this proposal become live.
**Also flagged:** DROP the `roberts-rebellion GUEST_OF winterfell` junk edge (confirmed sole outgoing edge on RR hub).
**Theory-gated items:** 0 — all proposals are Tier-1 or Tier-2 structural beats, no R+L=J assertion, no Jon-Arryn-murder culprit assertion.

---

## Target 1 — Downstream into the present: coronation → Cersei marriage → WO5K seeds

The `coronation-of-robert-i-baratheon` node has 0 outgoing edges and does not connect forward to any present-day arc.
The `wedding-of-robert-i-baratheon-and-cersei-lannister` node has 0 edges total — completely isolated.
Together these form the primary downstream dead-end: the Lannister alliance forged at the end of RR is the direct structural seed of the entire WO5K.

### 1a
`[NEW]  ENABLES  coronation-of-robert-i-baratheon -> wedding-of-robert-i-baratheon-and-cersei-lannister`
- **evidence:** agot-eddard-07.md:101
- **quote:** "I have Jon Arryn to thank for her. I had no wish to marry after Lyanna was taken from me, but Jon said the realm needed an heir. Cersei Lannister would be a good match, he told me, she would bind Lord Tywin to me should Viserys Targaryen ever try to win back his father's throne"
- **tier:** 1
- **rationale:** Robert's coronation directly enabled the political need for the Lannister marriage; Robert himself cites the succession imperative as the reason for it. ENABLES (not CAUSES) because the marriage was a political choice following from kingship, not automatic.
- **dedup:** confirmed-absent (0 edges on coronation target, 0 edges on wedding target)

### 1b
`[NEW]  ENABLES  wedding-of-robert-i-baratheon-and-cersei-lannister -> death-of-robert-baratheon`
- **evidence:** agot-eddard-07.md:101
- **quote:** "I have Jon Arryn to thank for her. I had no wish to marry after Lyanna was taken from me, but Jon said the realm needed an heir. Cersei Lannister would be a good match, he told me, she would bind Lord Tywin to me should Viserys Targaryen ever try to win back his father's throne"
- **tier:** 2
- **rationale:** The Cersei marriage placed a Lannister queen with motive (and proximity) to arrange Robert's death; the poisoned wine plot (executed through Lancel) is structurally enabled by Cersei's position as queen. This is the RR→WO5K macro-causal seam.
- **dedup:** confirmed-absent

### 1c
`[NEW]  MOTIVATES  wedding-of-robert-i-baratheon-and-cersei-lannister -> red-wedding-conspiracy`
- **evidence:** affc-cersei-01.md (see cersei node), wiki:Wedding_of_Robert_I_Baratheon_and_Cersei_Lannister
- **quote:** "If she had only married Rhaegar as the gods intended, he would never have looked twice at the wolf girl. Rhaegar would be our king today and I would be his queen, the mother of his sons. She had never forgiven Robert for killing him. But then, lions were not good at forgiving."
- **tier:** 2
- **rationale:** Cersei's decades-long resentment of Robert, established on the wedding night (Robert whispered Lyanna's name), drives her turn toward plotting. This MOTIVATES the conspiratorial posture that eventually includes the Red Wedding conspiracy (through Lannister-Tyrell alignment). This is a structural motivation bridge, not a direct CAUSES.
- **dedup:** confirmed-absent
- **NEEDS_VOCAB review:** MOTIVATES is in locked vocab; this use is correct per the motivation-chain model. No new vocab needed.

### 1d — Overlay: book cite onto coronation node
`[OVERLAY]  book-cite on coronation-of-robert-i-baratheon`
- The coronation node currently cites only `wiki:Coronation_of_Robert_I_Baratheon`. The moment of Robert's accession is directly evoked at agot-eddard-07.md:93: "Damn you, Ned Stark. You and Jon Arryn, I loved you both. What have you done to me? You were the one should have been king, you or Jon." This attaches a Tier-1 navigable cite to a currently wiki-only node.
- **evidence:** agot-eddard-07.md:93
- **quote:** "Damn you, Ned Stark. You and Jon Arryn, I loved you both. What have you done to me? You were the one should have been king, you or Jon."
- **tier:** 1
- **rationale:** Upgrades wiki-only provenance to book-navigable Tier-1; the only cite on this node currently is wiki.
- **dedup:** confirmed-absent (no existing cite_ref on this node's edges)

---

## Target 2 — Battle-of-the-Bells → Connington exile → AEGON container

`battle-of-the-bells` has 3 edges (PART_OF, PRECEDES, PRECEDES) and no agents, no causal DOWNSTREAM.
Jon Connington's exile (stripped by Aerys after Bells) is the direct premise of the entire AEGON container — he spends 15 years in exile, joins the Golden Company, raises Young Aegon. But NO edge in the graph runs from RR to the aegon container.

**Node needed (Lens 3 territory):** `connington-stripped-and-exiled-by-aerys` — a new event.incident capturing Aerys stripping Connington of titles and exiling him after the Battle of the Bells. Evidence: adwd-the-griffin-reborn-01.md:57. Once Lens 3 mints this node, edges 2a–2c below become live.

### 2a
`[NEW]  CAUSES  battle-of-the-bells -> connington-stripped-and-exiled-by-aerys` (pending Lens 3 mint)
- **evidence:** adwd-the-griffin-reborn-01.md:57
- **quote:** "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion, the lands and lordship had remained within House Connington"
- **tier:** 1
- **rationale:** The battle's outcome (Connington failed to capture/kill Robert) directly caused Aerys to strip and exile him. Genuine CAUSES: Connington's defeat at Bells produced this consequence.
- **dedup:** confirmed-absent

### 2b
`[NEW]  AGENT_IN  aerys-ii-targaryen -> connington-stripped-and-exiled-by-aerys` (pending Lens 3 mint)
- **evidence:** adwd-the-griffin-reborn-01.md:57
- **quote:** "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion"
- **tier:** 1
- **rationale:** Aerys is the active agent in the stripping/exile — his act, his decision.
- **dedup:** confirmed-absent

### 2c
`[NEW]  VICTIM_IN  jon-connington -> connington-stripped-and-exiled-by-aerys` (pending Lens 3 mint)
- **evidence:** adwd-the-griffin-reborn-01.md:57
- **quote:** "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile"
- **tier:** 1
- **rationale:** Connington is the direct victim of the stripping.
- **dedup:** confirmed-absent

### 2d
`[NEW]  ENABLES  connington-stripped-and-exiled-by-aerys -> aegon-revealed-to-the-golden-company` (pending Lens 3 mint)
- **evidence:** adwd-the-lost-lord-01.md:89; adwd-the-griffin-reborn-01.md:57
- **quote:** "Even the men who'd ridden with him might not recognize the exile lord Jon Connington" (adwd-the-lost-lord-01.md:89) + "I failed the father, but I will not fail the son." (adwd-the-griffin-reborn-01.md:71)
- **tier:** 1
- **rationale:** Connington's exile is what positions him to find Young Aegon and raise him in secret via the Golden Company; without the exile there is no Connington-as-regent and no Aegon reveal. This is the critical RR→AEGON macro bridge.
- **dedup:** confirmed-absent

---

## Target 3 — Rhaegar's death → Targaryen exile (Tier-1 only, no prophecy)

`battle-of-the-trident` already has `CAUSES → sack-of-kings-landing` and `PRECEDES → assault-on-dragonstone`. The Trident→sack→coronation chain exists. But no edge wires the Trident (Rhaegar death) to the Targaryen exile-from-Kings-Landing that precedes the assault on Dragonstone — and `assault-on-dragonstone` itself does not CAUSE anything in the essos or aegon containers.

### 3a
`[NEW]  CAUSES  battle-of-the-trident -> assault-on-dragonstone`
- **evidence:** agot-daenerys-01.md:37; also sources/wiki/_raw/Assault_on_Dragonstone.json (node prose)
- **quote:** "The midnight flight to Dragonstone, moonlight shimmering on the ship's black sails. Her brother Rhaegar battling the Usurper in the bloody waters of the Trident and dying for the woman he loved. The sack of King's Landing by the ones Viserys called the Usurper's dogs"
- **tier:** 1
- **rationale:** Rhaegar's death at the Trident triggered Aerys to send Rhaella and Viserys to Dragonstone (wiki confirms: "After the Mad King learned that Crown Prince Rhaegar had been killed…he sent Rhaella with Prince Viserys…to Dragonstone"). Currently only a PRECEDES edge exists; CAUSES is warranted because the death event caused the specific flight, not mere sequence.
- **dedup:** confirmed-absent (existing edge is PRECEDES, not CAUSES — this is a RECAST from structural to causal; keep PRECEDES and ADD CAUSES alongside it, or replace PRECEDES with CAUSES — recommend adding CAUSES and dropping the PRECEDES since CAUSES subsumes the ordering)

### 3b
`[NEW]  CAUSES  assault-on-dragonstone -> viserys-targaryen`
- **NEEDS_VOCAB:** There is no edge type for "caused someone to enter exile." CAUSES is entity→event or event→event; an event→character edge would need a role type. The closest is VICTIM_IN (Viserys and Dany are "victims" of the assault in the sense it forces their exile), but that reads as physical harm, not exile. Recommend Lens 3 consider an `exile-of-viserys-and-daenerys` event node instead; this would be event→event CAUSES. Marking NEEDS_VOCAB for current edge type; the intent is to capture that assault-on-dragonstone directly caused the Targaryen exile into the essos container.
- **tier:** 1
- **dedup:** confirmed-absent

---

## Target 4 — Internal cluster causality gaps

Checked the full upstream spine: `tourney-at-harrenhal CAUSES abduction-of-lyanna CAUSES execution-of-brandon-and-rickard-stark TRIGGERS aerys-demands-ned-and-robert TRIGGERS roberts-rebellion`. This is complete and tight.

Checked `wildfire-plot`, `battle-of-the-bells`, `battles-at-summerhall`, `taking-of-gulltown`: all linked only by PART_OF/PRECEDES. No genuine CAUSES gaps inside the cluster beyond what Target 2 addresses (bells→connington-exile is the real causal gap, not a sibling-battle gap).

**Guard note applied:** The sibling battles (Ashford → Bells → Summerhall → Gulltown → Trident → Sack) are sequential, not causally chained in the sense that winning/losing one directly caused the next. Rhaegar returning from Dorne triggered the Trident, but that is a character-motivation bridge already partially covered (rhaegar-targaryen COMMANDS_IN battle-of-the-trident). No false CAUSES edges recommended here.

**One genuine gap found:** `battle-of-ashford` has a PRECEDES to `battle-of-the-bells`, but the `battle-of-the-bells` has no AGENT_IN or COMMANDS_IN edges at all (confirmed via --neighbors). This is Lens 2 territory (character participant layers), not Lens 1 causal wiring — flagging for Lens 2 awareness.

### 4a — Intermediate node check: abduction-of-lyanna → Brandon-rides-to-KL → execution
The `execution-of-brandon-and-rickard-stark` has one CAUSES in from `abduction-of-lyanna`. The wiki establishes that Brandon rode to KL to confront Rhaegar after the abduction — this could be an intermediate beat node. However, the existing `abduction-of-lyanna CAUSES execution-of-brandon-and-rickard-stark` is defensible as a compressed causal edge (the abduction is what drove Brandon to confront Aerys, which led to the execution). An intermediate `brandon-rides-to-kings-landing` beat would improve granularity but is Lens 3 territory. Flagging: **Lens 3 node candidate**: `brandon-rides-to-kings-landing-to-confront-rhaegar` as a SUB_BEAT_OF abduction-of-lyanna.

---

## Target 5 — DROP the junk edge

`[DROP]  roberts-rebellion GUEST_OF winterfell`
- **evidence:** This edge exists as the sole outgoing edge on the hub (`roberts-rebellion GUEST_OF winterfell`, ref agot-catelyn-03.md:13, quote: "Take the books away." "My lady, the king's party had healthy appetites.")
- **rationale:** Misparsed edge. The ref is Robert's entourage visiting Winterfell in AGOT — a present-day event, not part of Robert's Rebellion. `GUEST_OF` is not in the locked edge vocab anyway. Clear parser error. Should be deleted without replacement.
- **dedup:** confirmed (matches baseline description exactly)

---

## Off-vocab edge flag (from baseline)

`[RECAST]  rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna-stark`
- This edge type is not in the locked vocab. The locked vocab does not have a direct equivalent for the crown-the-queen-of-love-and-beauty gesture. Options: (a) recast as `MOTIVATES` (the crowning MOTIVATES the abduction interpretation, but that's interpretive); (b) recast as `SUB_BEAT_OF tourney-at-harrenhal` with participant edges; (c) leave with a `NEEDS_VOCAB: ceremonial-crowning` tag and let Matt decide on a vocab addition. Recommend option (c) — the gesture is a first-class ASOIAF moment and may warrant a canonical edge type (e.g. `HONORS` with a qualifier). Not dropping it.
- **NEEDS_VOCAB:** CROWNS_QUEEN_OF_LOVE_AND_BEAUTY → candidate replacement `HONORS` (does not exist in locked vocab; requires Active Decision to add)

---

## Nodes proposed to Lens 3 (summary)
1. `connington-stripped-and-exiled-by-aerys` — event.incident, ~283 AC, PART_OF roberts-rebellion. Evidence: adwd-the-griffin-reborn-01.md:57. Critical for wiring battle-of-the-bells → aegon container.
2. `brandon-rides-to-kings-landing-to-confront-rhaegar` — event.incident, ~282 AC, SUB_BEAT_OF abduction-of-lyanna. Evidence: agot-catelyn-05.md (multiple Catelyn refs). Lower priority than #1.
3. `exile-of-viserys-and-daenerys` — event.incident, ~283 AC, CAUSES← assault-on-dragonstone, CAUSES→ (essos arc entry). Evidence: agot-daenerys-01.md:41. Needed to complete Target 3b.

---

## Edge count summary
| Status | Count |
|--------|-------|
| NEW edges proposed | 9 |
| OVERLAY (book cite) | 1 |
| RECAST recommendation | 1 (CROWNS_QUEEN_OF_LOVE_AND_BEAUTY) |
| DROP | 1 |
| NEEDS_VOCAB items | 2 |
| Node mints (Lens 3) | 3 |
| Pending Lens 3 mint | 4 (edges 2a–2d) |
