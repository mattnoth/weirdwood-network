# WO5K Battles Pass 3 — Lens B
## Duskendale & Ruby Ford participant/role/whodunit edges

Session: S166 | Date: 2026-06-28 | Source: orchestrator research lens

---

## Canonical-slug confirmation

### battle-at-duskendale
- **Correct slug: `battle-at-duskendale`** (node exists at `graph/nodes/events/battle-at-duskendale.node.md`, type `event.battle`, tier-1).
- Wiki cache at `sources/wiki/_raw/Battle_at_Duskendale.json` confirms: "Battle at Duskendale — Conflict: War of the Five Kings — Date: 299 AC — Place: Duskendale — Result: Iron Throne victory." This is the ASOS Glover/Tallhart battle, NOT the historical Aerys/Darklyn `Defiance_of_Duskendale` (a separate wiki page) or the Dance-era `Sack_of_Duskendale` (also a separate wiki page). Both alternative slugs confirmed present and distinct in cache.
- **Not touching:** `defiance-of-duskendale` / `sack-of-duskendale`.

### fighting-at-the-fords-of-the-trident
- **Correct slug: `fighting-at-the-fords-of-the-trident`** (node exists at `graph/nodes/events/fighting-at-the-fords-of-the-trident.node.md`, type `event.battle`, tier-1).
- Wiki cache at `sources/wiki/_raw/Fighting_at_the_fords_of_the_Trident.json` confirms: "Fighting at the fords of the Trident — Conflict: War of the Five Kings — Date: 299 AC — Place: Ruby ford of the Trident in the riverlands — Result: Lannister victory." This is the ASOS Roose/Gregor Ruby-Ford fight, not the ACOK Edmure/Tywin Red-Fork defense.
- `sources/wiki/_raw/Battle_of_the_Ruby_Ford.json` is a redirect page pointing to `Fighting_at_the_fords_of_the_Trident` — confirms `battle-of-the-ruby-ford` is a `same_as` alias only; the canonical target is `fighting-at-the-fords-of-the-trident`.
- **Not touching:** `battle-of-the-fords` (that is the ACOK Edmure battle).

---

## Proposed edges

### battle-at-duskendale roster

**Edge 1**
```
COMMANDS_IN | randyll-tarly | battle-at-duskendale | ASOS | asos-catelyn-04 | tier-1 | verify: true
```
Quote: `"the battle at Duskendale, where Lord Randyll Tarly had shattered Robett Glover and Ser Helman Tallhart"`
Source: `asos-catelyn-04.md:91`
Rationale: Tarly was the Lannister-side commander who destroyed the northern host; "shattered" is the book's own action verb for the battle outcome. Wiki confirms "Lord Randyll Tarly catches Robett Glover outside of Duskendale" as the named commander. COMMANDS_IN is correct (he led the force, not just participated).

---

**Edge 2**
```
VICTIM_IN | robett-glover | battle-at-duskendale | ASOS | asos-catelyn-04 | tier-1 | verify: true
```
Quote: `"the battle at Duskendale, where Lord Randyll Tarly had shattered Robett Glover and Ser Helman Tallhart"`
Source: `asos-catelyn-04.md:91`
Secondary confirmation (survival/capture): `"Galbart Glover was relieved to hear that his brother Robett had been put on a ship at Duskendale"` — `asos-catelyn-05.md:29`
Rationale: Robett's host was shattered and he was subsequently captured (then exchanged). VICTIM_IN is the right role: he commanded the northern force but was on the losing/suffering side.

---

**Edge 3**
```
VICTIM_IN | helman-tallhart | battle-at-duskendale | ASOS | asos-catelyn-04 | tier-1 | verify: true
```
Quote: `"the battle at Duskendale, where Lord Randyll Tarly had shattered Robett Glover and Ser Helman Tallhart"`
Source: `asos-catelyn-04.md:91`
Rationale: The wiki node for `battle-at-duskendale` (already in graph) states "Ser Helman Tallhart is killed during the fierce battle" (citing AFFC appendix). The book text names him as one of the two commanders shattered at Duskendale; the wiki confirms he died there. VICTIM_IN covers both "defeated" and "killed" — correct for Tallhart. The death itself can be noted in a separate DIES_IN edge if that type exists; if not, VICTIM_IN carries it.

---

**Edge 4**
```
LOCATED_AT | battle-at-duskendale | duskendale | ASOS | asos-catelyn-04 | tier-1 | verify: true
```
Quote: `"the battle at Duskendale, where Lord Randyll Tarly had shattered Robett Glover and Ser Helman Tallhart"`
Source: `asos-catelyn-04.md:91`
Secondary: `"Lord Randyll Tarly held Maidenpool, Duskendale, and the kingsroad"` — `asos-tyrion-08.md:77` (shows Tarly's post-battle hold on the town itself)
Rationale: Battle is named after the location; wiki infobox confirms "Place: Duskendale." The location node `duskendale` exists.

---

**Edge 5**
```
COMMANDS_IN | roose-bolton | battle-at-duskendale | ASOS | asos-catelyn-04 | tier-2 | verify: true
```
Quote: `"Duskendale, on the narrow sea? Why would they go to Duskendale?"`
Source: `asos-catelyn-04.md:91`
Supporting wiki node text (already in `battle-at-duskendale.node.md` ## Origins): "Lord Roose Bolton learns of Stannis Baratheon's defeat… He orders Helman to kill his Lannister captives… and then march with Robett Glover to Duskendale."
Rationale: Robb's bafflement is precisely the seam: as King, Robb did not order this march; Roose Bolton, as his Harrenhal commander, did. The wiki node (sourced from ACOK Ch. 64) explicitly records Bolton ORDERING the Duskendale march. Robb's "Why would they go?" signals he was not the decision-maker. Role here is COMMANDS_IN in the sense of "the commander who ordered/dispatched the force" — the orderer role at the strategic level, distinct from battlefield command. This is a tier-2 edge (sourced from wiki/indirect book implication rather than a direct POV witnessing), but the ordering is documented in the existing node prose.

---

### fighting-at-the-fords-of-the-trident roster

**Edge 6**
```
COMMANDS_IN | gregor-clegane | fighting-at-the-fords-of-the-trident | ASOS | asos-catelyn-06 | tier-1 | verify: true
```
Quote: `"Gregor Clegane attacked with heavy horse and drove them into the river."`
Source: `asos-catelyn-06.md:281`
Secondary: `"Ser Gregor Clegane had crossed the Trident and seized the ruby ford"` — `asos-tyrion-08.md:77`
Rationale: Gregor is the named Lannister attacking commander. "Attacked with heavy horse" = active battlefield command. COMMANDS_IN is correct (he led the cavalry assault).

---

**Edge 7**
```
COMMANDS_IN | roose-bolton | fighting-at-the-fords-of-the-trident | ASOS | asos-catelyn-06 | tier-1 | verify: true
```
Quote: `"I delayed too long before leaving Harrenhal. Aenys Frey departed several days before me and crossed the Trident at the ruby ford, though not without difficulty. But by the time we came up the river was a torrent."`
Source: `asos-catelyn-06.md:281`
Rationale: This is Roose Bolton speaking in the first person about the march and crossing. He was the northern commander whose host was engaged at the ford. COMMANDS_IN applies even though he ended up on the wrong side of the river — he commanded the army throughout.

---

**Edge 8**
```
VICTIM_IN | wylis-manderly | fighting-at-the-fords-of-the-trident | ASOS | asos-catelyn-06 | tier-1 | verify: true
```
Quote: `"Norrey, Locke, and Burley men chiefly, with Ser Wylis Manderly and his White Harbor knights as rear guard."`
Source: `asos-catelyn-06.md:281`
Secondary confirmation (captured): wiki node already records "others are taken captive, including Wylis" (citing same ASOS Ch. 49 passage). Ser Wendel Manderly's exclamation at line 245 of same chapter — `"Lannisters on the Trident," said Ser Wendel unhappily. "My brother is taken again."` — confirms capture.
Rationale: Wylis commanded the rear-guard, was driven into the river, and was taken captive. VICTIM_IN is correct (he suffered the attack's worst consequences).

---

**Edge 9**
```
LOCATED_AT | fighting-at-the-fords-of-the-trident | ruby-ford | ASOS | asos-catelyn-06 | tier-1 | verify: true
```
Quote: `"Aenys Frey departed several days before me and crossed the Trident at the ruby ford, though not without difficulty."`
Source: `asos-catelyn-06.md:281`
Secondary: wiki infobox — "Place: Ruby ford of the Trident in the riverlands."
Rationale: Both the chapter text and wiki infobox name the ruby ford as the location. The location node `ruby-ford` exists.

---

## Whodunit verdict

### SUSPECTED_OF edges — honest adjudication

**Claim A: `roose-bolton SUSPECTED_OF battle-at-duskendale`**

**PROPOSE. Tier-2.**

Strongest supporting in-text basis:

1. Roose ordered the march (documented in the node prose, sourced from ACOK Ch. 64, now in graph). Robb had no knowledge of it: `"Duskendale, on the narrow sea? Why would they go to Duskendale?"` (`asos-catelyn-04.md:91`). A king baffled by a strategic decision his own army made is the clearest possible signal he did not authorize it.

2. The identities of the men sent: the wiki node confirms northern participants were Houses Cerwyn, Glover, Hornwood, Karstark, and Tallhart — all men from northern bannerman houses, NOT Dreadfort/Bolton men. Roose's troops at the Twins were "Dreadfort men, in chief, and some from Karhold" (`asos-catelyn-06.md:297`). He preserved his own house's strength while sending rival northern lords to be destroyed.

3. Roose's post-battle framing shifts blame to Glover: `"A folly, but Glover was heedless after he learned that Deepwood Motte had fallen. Grief and fear will do that to a man."` (`asos-catelyn-06.md:293`). This is Roose volunteering a cover story that exculpates himself (grief/fear = Glover acted alone) in front of the very king who is asking questions. The self-serving nature of this explanation is a significant textual signal.

4. The wiki's own node prose (already in graph) states: "It is later revealed that Roose Bolton had secretly defected to the Lannister side and in his attempt to diminish the northern lords' ability to attack him, he had sent much of the northern army to its destruction."

Strongest contradicting passage: The text never has any POV character explicitly accuse Roose of deliberately sacrificing the Duskendale force. Robb's bewilderment could be mere surprise at a poor decision, not evidence of betrayal. Roose's explanation (Glover's grief after Deepwood fell) is diegetically plausible — grief-driven bad decisions happen. No one in the text connects these dots aloud until AFFC/ADWD.

**Verdict: PROPOSE as SUSPECTED_OF, tier-2.** The evidence substrate is genuinely load-bearing: the combination of (a) Robb's explicit non-authorization, (b) Bolton-men conspicuously absent from the destroyed force, and (c) Roose's self-serving cover story constitutes more than a conspiracy-theory over-read. The causal chain is also stated outright in the existing wiki-sourced node prose. This is not proven within the POV text of ASOS alone, so tier-1 is off the table; tier-2 with an honest `evidence_basis: "inferred from strategic pattern + wiki-confirmed defection context"` is correct.

---

**Claim B: `roose-bolton SUSPECTED_OF fighting-at-the-fords-of-the-trident`**

**PROPOSE. Tier-2. But with a significant note on evidentiary strength vs. Claim A.**

Strongest supporting in-text basis:

1. Roose's own account opens with a self-flagellating phrase — `"I blame myself. I delayed too long before leaving Harrenhal."` (`asos-catelyn-06.md:281`) — and immediately provides an explanation (flooding, too few boats) that is impossible to disprove and conveniently exonerates him. A man deliberately sacrificing his rear-guard would give exactly this account.

2. The men caught in the trap were disproportionately NOT Bolton men: `"Norrey, Locke, and Burley men chiefly"` were the rear-guard casualties; Roose arrives at the Twins with "some five hundred horse and three thousand foot, my lady. Dreadfort men, in chief, and some from Karhold." (`asos-catelyn-06.md:297`). His own house's strength survived intact; the Norrey/Locke/Burley/Manderly rear-guard absorbed the losses.

3. Robb praises him for the ford defense he left behind — `"You did well, my lord"` (`asos-catelyn-06.md:287`) — while Roose is actively on his way to betray Robb at the Red Wedding. The praise-while-deceiving moment is the authorial signal.

Strongest contradicting passage: The Ruby Ford fight is more ambiguous than Duskendale. The flooding is a natural circumstance; the attack by Gregor Clegane came from the Lannister side without visible coordination with Bolton's "delay." Roose's delay could genuinely be incompetence or caution rather than deliberate positioning of enemy-house infantry as sacrificial rear-guard. Unlike Duskendale, there is no in-text moment of Robb wondering "why would they go there?" — the crossing simply went wrong.

**Verdict: PROPOSE as SUSPECTED_OF, tier-2.** The strongest evidence is structural rather than explicit: Roose's men survive, Stark-loyal bannermen die, and Roose delivers a rehearsed-sounding self-blame that explains everything away. This is consistent with deliberate sacrifice but cannot be read as proof. Tier-2, `evidence_basis: "structural pattern — Bolton men spared, rival northern houses' men destroyed; Roose's self-exculpatory account"`. Be explicit in any node prose annotation that this edge is pattern-based, not confession-based.

---

## Container tag recommendation

Both `battle-at-duskendale` and `fighting-at-the-fords-of-the-trident` are Red-Wedding-upstream WO5K beats. Recommend adding `containers: [wo5k]` to both nodes' frontmatter (orchestrator to handle node edits).

---

## Dropped

**`roose-bolton AGENT_IN battle-at-duskendale`** — DROPPED. AGENT_IN would imply Roose was a direct actor in the battle; he was not present at Duskendale. He ordered the march (COMMANDS_IN in the dispatch sense), but AGENT_IN suggests personal battlefield agency. Use COMMANDS_IN (Edge 5) + SUSPECTED_OF (whodunit) instead.

**`gregor-clegane AGENT_IN battle-at-duskendale`** — DROPPED. Gregor cut off the northern retreat near the kingsroad after the main battle; he was not the battle's commander (Tarly was). His role at Duskendale is subordinate to Tarly's command. The existing node prose in `battle-at-duskendale.node.md` mentions him capturing Robett. A separate edge `gregor-clegane COMMANDS_IN battle-at-duskendale` is weaker than COMMANDS_IN on Tarly; if we want Gregor, the right edge is `gregor-clegane AGENT_IN battle-at-duskendale` for the kingsroad intercept role — but the task brief says do not re-propose what is already in the node prose without a separate role edge. Hold for the orchestrator to decide if the intercept role needs a distinct edge vs. leaving it in prose.

**`wylis-manderly COMMANDS_IN fighting-at-the-fords-of-the-trident`** — DROPPED in favor of VICTIM_IN. Wylis did rally the rear-guard (`"Ser Wylis rallied our men as best he could"`) but he was on the losing/captured side. VICTIM_IN captures his status accurately; COMMANDS_IN would overstate his successful agency when the outcome was defeat and capture. If the schema supports BOTH edges on one node, a reviewer could add COMMANDS_IN alongside VICTIM_IN; this lens prefers VICTIM_IN as the primary characterization.

**`harrion-karstark VICTIM_IN battle-at-duskendale`** — DROPPED from this pass. The node `harrion-karstark` was not confirmed present in the existing slug inventory check. The wiki confirms Harrion was sent by Roose and was captured (held at Maidenpool), but without confirming the node slug exists, proposing the edge risks an orphan. Flag for the orchestrator to check if `harrion-karstark` node exists before adding this edge.

---

## Harvest queue entries

(appended separately to `working/harvest-queue.md`)
