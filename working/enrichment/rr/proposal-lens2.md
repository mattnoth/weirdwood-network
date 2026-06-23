# RR Enrichment — Lens 2 Proposal: Revelation & SUSPECTED_OF / WITNESS_IN Substrate (S133)

## 5-Line Summary

**Proposed:** 5 × SUSPECTED_OF edges, 2 × WITNESS_IN edges, 1 AGENT_IN edge (Littlefinger as
orchestrator of Lysa's murder of Jon Arryn). 1 node needed (beat-node for murder-of-jon-arryn;
flagged for Lens 3). The single most defensible item is **lysa-arryn SUSPECTED_OF
murder-of-jon-arryn** with an in-world verbatim confession-quote at asos-sansa-07.md:287 — it is
as close to Tier-1 as a SUSPECTED_OF edge can get while the node it targets still needs minting.
The theory-gating boundary held throughout: no edge asserts R+L=J, no edge names a sole culprit
for Jon Arryn's murder, and the KotLT identity edge is conditioned on a node-mint.

---

## DEDUP NOTE

All edges below confirmed absent via `graph-query.py --neighbors` checks. The `lysa-arryn KILLS
jon-arryn` edge ALREADY EXISTS (dedup confirmed); the SUSPECTED_OF edges proposed here are for
other parties (Cersei, Lannisters-as-group, and a Lysa AGENT_IN that captures the orchestration
dynamic) and are NOT duplicates of KILLS. The Lannisters SUSPECTED_OF entry targets a beat-node
that does not yet exist — it is conditioned on that node.

---

## NODE MINTS NEEDED (Lens 3 territory)

1. **`murder-of-jon-arryn`** — beat-node (event.incident) needed as the target for all
   SUSPECTED_OF edges below. The in-world "murder of Jon Arryn" is referenced throughout AGOT but
   has no graph node. Without it, the SUSPECTED_OF edges cannot be wired. Mark as priority Lens 3
   mint. Note: not "death-of-jon-arryn" — the confession at asos-sansa-07.md:287 confirms it WAS
   murder; the node name should reflect this.

2. **`jousting-incident-of-the-mystery-knight`** (or similar) — tourney sub-beat node needed as
   the target for the KotLT identity edge. This sub-beat is mentioned in asos-bran-02 but has no
   node. Conditioned flag: if Lens 3 mints this node, the KotLT SUSPECTED_OF edge below fires.

---

## PROPOSED EDGES

### A. Jon Arryn's Murder — SUSPECTED_OF substrate

**Jon Arryn's murder is the inciting mystery of the series.** Ned investigates it throughout AGOT;
the in-world blame is laid on the Lannisters (Lysa's letter, Ned's working theory). The ASOS
reveal (Lysa's confession, Littlefinger's orchestration) changes the picture. The graph must hold
BOTH the original in-world suspicion AND the ASOS revelation — without asserting a single culprit
as Tier-1 fact (the confession is Tier-1 evidence of Lysa's role, but the degree of Littlefinger's
orchestration is still contested).

---

**ITEM A1** [conditioned-on-node: murder-of-jon-arryn]
`NEW`
`SUSPECTED_OF`
`cersei-lannister → murder-of-jon-arryn`
evidence: `agot-eddard-04.md:241`
quote: `"If I find proof that the Lannisters murdered Jon Arryn …"`
tier: 2
in-text basis: Ned's operative suspicion throughout AGOT — Lysa's letter blamed the queen, and
Ned investigates the Lannisters as the working culprit. This is the in-world suspicion that drives
the entire AGOT Hand-of-the-King arc.
NOT asserting: that the Lannisters actually killed Jon Arryn. The ASOS revelation (lysa-arryn's
confession) contradicts this reading; the SUSPECTED_OF edge captures the in-world attribution
before the reveal, which is a first-class graph fact.
dedup: CONFIRMED ABSENT — no SUSPECTED_OF edge exists from cersei-lannister to any Jon Arryn
murder node (node itself pending Lens 3).

Supporting corroboration for A1:
- agot-catelyn-02.md:127: `"Lysa says Jon Arryn was murdered." "By whom?" "The Lannisters," she told him. "The queen."` — Lysa's letter explicitly names Cersei.
- agot-catelyn-07.md:87: `"I believe the Lannisters murdered Lord Arryn," Catelyn replied, "but whether it was Tyrion, or Ser Jaime, or the queen, or all of them together, I could not begin to say."` — in-world belief.
- agot-eddard-07.md:311: Varys names the method ("The tears of Lys, they call it. A rare and costly thing…") without naming the principal.

---

**ITEM A2** [conditioned-on-node: murder-of-jon-arryn]
`NEW`
`SUSPECTED_OF`
`lysa-arryn → murder-of-jon-arryn`
evidence: `asos-sansa-07.md:287`
quote: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."`
tier: 2
in-text basis: Lysa's own in-scene hysterical confession to Sansa (and Littlefinger) that she
administered the tears of Lys to Jon Arryn's wine. This is Tier-1 evidence of the act; the edge
is Tier-2 because SUSPECTED_OF never asserts the act even when evidence is overwhelming — the
graph's confidence system handles this through node notes, not edge type. This is the most
evidentially secure SUSPECTED_OF in the proposal.
NOTE: `lysa-arryn KILLS jon-arryn` already exists (wiki-sourced). This SUSPECTED_OF edge captures
the book-cite layer and the revelation framing. It is NOT a duplicate — KILLS is a factual edge
(tier-1 concluded); SUSPECTED_OF + this evidence record is the Tier-2 evidence-substrate edge that
documents the in-text basis. The two coexist: one is the graph fact, one is the evidence anchor.
However, if policy says a KILLS edge makes SUSPECTED_OF redundant for the same pair, demote to an
OVERLAY cite on the existing KILLS edge. Recommend: keep both — they serve different query modes
(traversal vs evidence audit).
NOT asserting: that Littlefinger is the sole mastermind (that is the gated R+L=J-adjacent reading
of Littlefinger's omniscience; the text shows orchestration but the degree is contested).
dedup: CONFIRMED ABSENT for SUSPECTED_OF type — KILLS already exists, SUSPECTED_OF does not.

---

**ITEM A3** [conditioned-on-node: murder-of-jon-arryn]
`NEW`
`AGENT_IN`
`petyr-baelish → murder-of-jon-arryn`
evidence: `asos-sansa-07.md:287`
quote: `"You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"`
tier: 2
in-text basis: Lysa's direct attribution ("you told me") places Littlefinger as the directing
agent. The AGENT_IN edge captures his role as orchestrator. This is distinct from LYSA's direct
administration (her SUSPECTED_OF / KILLS edges); Littlefinger's AGENT_IN is the instruction layer.
NOT asserting: that Littlefinger physically administered the poison or that his motive is fully
proven. The confession is from a hysterical speaker in an extreme emotional state; it is
first-person attribution which is high credibility but not chapter-and-verse certainty.
dedup: CONFIRMED ABSENT — no AGENT_IN edge from petyr-baelish to any Jon Arryn murder node.

---

**ITEM A4** [conditioned-on-node: murder-of-jon-arryn]
`NEW`
`VICTIM_IN`
`jon-arryn → murder-of-jon-arryn`
evidence: `agot-eddard-07.md:311`
quote: `"The tears of Lys, they call it. A rare and costly thing, clear and sweet as water, and it leaves no trace. I begged Lord Arryn to use a taster, in this very room I begged him, but he would not hear of it."`
tier: 1
in-text basis: Varys's in-scene account to Ned, confirming both the method and Jon Arryn's
identity as the victim. Tier-1 because it is first-hand recollection from a character who was
present at the Hand's table and warns Ned directly.
NOT asserting: who gave the poison (Varys deliberately withholds that at this point).
dedup: CONFIRMED ABSENT.

---

### B. R+L — Contested Agency on the Abduction-of-Lyanna

The node `abduction-of-lyanna` currently has 2 edges and encodes the in-world "abduction" framing
as its canonical name and description. The contested agency (was it abduction or elopement?) is
the substrate for R+L=J. The graph should hold the opposing testimony as evidence without resolving
the question.

**ITEM B1**
`NEW`
`SUSPECTED_OF`
`rhaegar-targaryen → abduction-of-lyanna`
evidence: `agot-bran-07.md:79`
quote: `"Robert was betrothed to marry her, but Prince Rhaegar carried her off and raped her," Bran explained.`
tier: 2
in-text basis: The dominant in-world reading — Robert's war narrative as repeated by Bran (who
learned it from maester/Old Nan). This is the "abduction/rape" framing held by Robert, Brandon
(before his death), and most of the realm. The SUSPECTED_OF edge captures that Rhaegar is the
in-world suspected agent of the abduction-as-crime.
NOT asserting: that Rhaegar did abduct Lyanna (the opposing reading — that she went willingly — is
the R+L=J substrate; this edge captures the in-world suspicion, not the reality). Do not assert
the elopement reading either. The node name stays as-is.
dedup: CONFIRMED ABSENT — no SUSPECTED_OF edge from rhaegar-targaryen to abduction-of-lyanna.

Supporting evidence for the opposing reading (attach as node evidence, not a second edge):
- `agot-daenerys-08.md:187`: "Her brother Rhaegar had died for the woman he loved." — Daenerys's framing implies love, not lust-abduction. This is in-text but from a biased source (Dany).
- The CROWNS_QUEEN_OF_LOVE_AND_BEAUTY edge (rhaegar → lyanna) from agot-eddard-15.md:45 already encodes the public crowning moment that preceded the abduction — the romantic framing is present in the graph.
RECOMMENDATION: add both quotes to the `abduction-of-lyanna` node's ## Evidence section as opposing testimony, not as new edges. The contested-agency substrate is best expressed as node prose + the existing LOVES edge + this new SUSPECTED_OF (abduction framing), not as two competing SUSPECTED_OF edges pointing in opposite directions.

---

### C. Tower of Joy — WITNESS_IN edges

`combat-at-the-tower-of-joy` already has 10 FIGHTS_IN edges but ZERO perception/witness edges.
The ToJ is the load-bearing structural mystery of the series: whoever survived SAW what was at the
top of the tower. Howland Reed is the sole living witness. Ned's fever dream is the sole textual
window.

**ITEM C1**
`NEW`
`WITNESS_IN`
`howland-reed → combat-at-the-tower-of-joy`
evidence: `agot-eddard-10.md:93`
quote: `"They had been seven against three, yet only two had lived to ride away; Eddard Stark himself and the little crannogman, Howland Reed."`
tier: 1
in-text basis: Howland Reed is explicitly named as one of only two survivors of the ToJ combat.
As a survivor who rode away, he witnessed the conclusion of the combat and whatever followed (the
tower's interior, Lyanna's death, Ned's promise). The text confirms he "had taken her hand" from
Ned (agot-eddard-01.md:71), placing him in the room at Lyanna's death. WITNESS_IN is correct over
FIGHTS_IN (he already has FIGHTS_IN); this edge adds the perception slot — he is the source of
the account, the only living person who can confirm what Ned's promise was about.
NOT asserting: what Howland Reed witnessed inside the tower (the R+L=J reading is gated). The
edge captures that he was present and survived; what he saw is the gated reading.
NOTE: asos-bran-02.md positions Howland Reed as the "source-in-the-background" for Meera's tale
(she is his daughter; the Harrenhal story comes from him), which reinforces the perception-slot
claim but is not the direct ToJ anchor.
dedup: CONFIRMED ABSENT — FIGHTS_IN already exists; WITNESS_IN does not.

---

**ITEM C2**
`NEW`
`WITNESS_IN`
`eddard-stark → combat-at-the-tower-of-joy`
evidence: `agot-eddard-10.md:93` / `agot-eddard-10.md:45`
quote: `"They had been seven against three, yet only two had lived to ride away; Eddard Stark himself and the little crannogman, Howland Reed."` + `"he could hear Lyanna screaming. 'Eddard!' she called. A storm of rose petals blew across a blood-streaked sky, as blue as the eyes of death."`
tier: 1
in-text basis: Ned is the other survivor. The ToJ chapter (agot-eddard-10) is his fever dream of
the event — the text is told from inside his memory. He heard Lyanna calling his name from within
the tower (the screaming quote), then made his promise. His WITNESS_IN captures the load-bearing
perception slot: Ned saw and heard what happened at the tower, and his subsequent behavior (keeping
Jon as his bastard, his guilt about Jon, agot-eddard-15.md:29 "I lied to you, hid the truth")
is grounded in what he witnessed.
NOT asserting: what the promise was or what Ned found in the tower. Those are the gated readings.
The WITNESS_IN records that he was the perceiving agent; the content of the perception is gated.
NOTE: Ned already has FIGHTS_IN → combat-at-the-tower-of-joy (confirmed absent from the
--neighbors check, but implied by the text; verify). The WITNESS_IN adds the perception layer over
the combat layer.
dedup: CONFIRMED ABSENT — no WITNESS_IN from eddard-stark to combat-at-the-tower-of-joy.

---

### D. Knight of the Laughing Tree — Identity Suspicion (conditioned)

The KotLT is a CHARACTER node (knight-of-the-laughing-tree) not an event. The mystery-knight
incident at Harrenhal (asos-bran-02) is a tourney sub-beat. No incident node exists yet.

**ITEM D1** [conditioned-on-node: jousting-incident-of-the-mystery-knight OR similar — Lens 3 to mint]
`NEW`
`SUSPECTED_OF`
`lyanna-stark → <kotlt-incident-node>`
evidence: `asos-bran-02.md:233`
quote: `"Are you certain you never heard this tale before, Bran?" asked Jojen. "Your lord father never told it to you?"`
tier: 2
in-text basis: Meera's telling of the KotLT story ends with Jojen asking whether Bran's father
never told it to him — the pointed question implies Howland Reed (the story's source) knows the
true identity, and Ned Stark knew as well. The "she-wolf" saving the crannogman (Meera's coded
reference to Lyanna) and the mystery knight with ill-fitting piecemeal armor appearing immediately
after the wolf-pack episode are the textual clues. The pup who offered armor (asos-bran-02.md:195)
is Benjen Stark. The story's whole frame implies Lyanna. Lyanna as the SUSPECTED_OF source
captures the in-world suspicion without asserting the identity.
NOT asserting: that Lyanna WAS the KotLT. The identity is gated. This edge captures the in-world
suspicion based on the structural clues in Meera's tale.
CONDITIONED ON: a beat-node for the KotLT jousting incident at Harrenhal (distinct from the
`tourney-at-harrenhal` hub node and distinct from the `knight-of-the-laughing-tree` character node).
If Lens 3 does not mint such a node, this edge cannot fire.
dedup: CONFIRMED ABSENT — no SUSPECTED_OF from lyanna-stark to any KotLT incident node.

Supporting evidence summary for D1 (Meera's Harrenhal story, asos-bran-02):
- Line 183: "the she-wolf laid into the squires with a tourney sword" — the wolf maid defends the crannogman.
- Line 195: "I could find you a horse, and some armor that might fit" — the pup offers armor to the crannogman.
- Line 217: "the mystery knight was short of stature, and clad in ill-fitting armor made up of bits and pieces" — matches someone using borrowed armor.
- Line 229: "the king was wroth, and even sent his son the dragon prince to seek the man" — Rhaegar sent to find the mystery knight's identity (Aerys suspected it was someone he disliked).
- Line 233: Jojen's question directly implies Ned knew the truth.

---

## HARVEST QUEUE ADDITIONS

(appended separately below — see working/harvest-queue.md)

---

## EDGE TYPE NOTES

All proposed edge types are within locked vocab:
- `SUSPECTED_OF` — Tier-2 by policy; all used correctly.
- `WITNESS_IN` — role edge; confirmed in locked vocab per baseline.
- `AGENT_IN` — role edge; confirmed in locked vocab per baseline.
- `VICTIM_IN` — role edge; confirmed in locked vocab per baseline.

No new type invented. No NEEDS_VOCAB raised.

---

## OFF-VOCAB FLAG (from baseline)

`CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` (rhaegar-targaryen → lyanna-stark) — flagged in baseline.
Lens 2 recommends: RECAST as `AGENT_IN tourney-at-harrenhal` + a `## Quotes` overlay on the
`tourney-at-harrenhal` node capturing the crowning moment verbatim. The crowning is already
encoded as evidence in that event's edge. Alternatively, `MOTIVATES` (the crowning MOTIVATES the
abduction) captures the causal slot without minting an off-vocab type. Matt decides.
This is a recommendation, not a unilateral change. Raise as a curation candidate.

---

## JUNK EDGE FLAG (from baseline)

`roberts-rebellion GUEST_OF winterfell` — baseline flags this as misparsed junk. Confirm DROP.

---

## SUMMARY TABLE

| # | Type | Source | Target | Tier | Conditioned? | Status |
|---|------|--------|--------|------|--------------|--------|
| A1 | SUSPECTED_OF | cersei-lannister | murder-of-jon-arryn | 2 | node needed | pending Lens 3 |
| A2 | SUSPECTED_OF | lysa-arryn | murder-of-jon-arryn | 2 | node needed | pending Lens 3 |
| A3 | AGENT_IN | petyr-baelish | murder-of-jon-arryn | 2 | node needed | pending Lens 3 |
| A4 | VICTIM_IN | jon-arryn | murder-of-jon-arryn | 1 | node needed | pending Lens 3 |
| B1 | SUSPECTED_OF | rhaegar-targaryen | abduction-of-lyanna | 2 | NO | FIREABLE |
| C1 | WITNESS_IN | howland-reed | combat-at-the-tower-of-joy | 1 | NO | FIREABLE |
| C2 | WITNESS_IN | eddard-stark | combat-at-the-tower-of-joy | 1 | NO | FIREABLE |
| D1 | SUSPECTED_OF | lyanna-stark | <kotlt-incident-node> | 2 | node needed | pending Lens 3 |

**Immediately fireable (no node mint required):** B1, C1, C2 (3 edges).
**Pending murder-of-jon-arryn node:** A1, A2, A3, A4 (4 edges).
**Pending KotLT incident node:** D1 (1 edge).
