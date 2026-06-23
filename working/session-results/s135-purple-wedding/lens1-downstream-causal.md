# Lens 1 — Downstream Causal / Consequence Wiring
## Purple Wedding enrichment dip · S135

> PROPOSE-ONLY. All proposals are new; nothing in baseline.md is re-proposed.
> Tier-1 = on-page role/participant fact. Tier-2 = causal/interpretive inference from text.

---

## Edge Proposals

| src_slug | edge_type | tgt_slug | tier | evidence (file:line) | verbatim quote | rationale |
|---|---|---|---|---|---|---|
| death-of-joffrey-baratheon | ENABLES | wedding-of-tommen-i-baratheon-and-margaery-tyrell | 2 | sources/chapters/asos/asos-sansa-06.md:193 | "Her son was determined to make Margaery a queen, and for that he needed a king . . . but he did not need Joffrey. We shall have another wedding soon, wait and see. Margaery will marry Tommen." | Littlefinger states on-page that Joffrey's death is the enabling condition for Tommen's accession and the Tommen-Margaery wedding. Node `wedding-of-tommen-i-baratheon-and-margaery-tyrell` already exists; this causal wire is absent. |
| death-of-joffrey-baratheon | MOTIVATES | cersei-lannister | 2 | sources/chapters/asos/asos-tyrion-08.md:323 | "Arrest my brother," she commanded him. "He did this, the dwarf. Him and his little wife. They killed my son. Your king. Take them! Take them both!" | Cersei's accusation and vendetta against Tyrion (and Sansa) is her direct, on-page response to Joffrey's death. Grounds her role in `tyrion-accused-of-poisoning-joffrey` (which already has her as AGENT_IN) but the causal motivation from grief/rage is unwired. |
| death-of-joffrey-baratheon | TRIGGERS | littlefinger-smuggles-sansa-out-of-kings-landing | 2 | sources/chapters/asos/asos-sansa-05.md:47 | "Hush, you'll be the death of us. I did nothing. Come, we must away, they'll search for you. Your husband's been arrested." | Dontos explicitly states the escape is triggered by Joffrey's death and the arrest of Tyrion. The existing beat `littlefinger-smuggles-sansa-out-of-kings-landing` has no inbound causal edge; the death is the direct trigger for the exfiltration. |
| littlefinger-smuggles-sansa-out-of-kings-landing | TRIGGERS | sansa-assumes-alayne-stone-identity | 2 | sources/chapters/asos/asos-sansa-06.md:105 | "Varys has informers everywhere. If Sansa Stark should be seen in the Vale, the eunuch will know within a moon's turn, and that would create unfortunate . . . complications. It is not safe to be a Stark just now. So we shall tell Lysa's people that you are my natural daughter." | Littlefinger's smuggling of Sansa necessitates her identity replacement as "Alayne Stone." This is a load-bearing downstream consequence — Sansa's arc through AFFC/ADWD runs on this identity. Proposes a new node (see below). |
| tyrion-accused-of-poisoning-joffrey | MOTIVATES | bronn-of-the-blackwater | 2 | sources/chapters/asos/asos-tyrion-09.md:87 | "The boy begged, or I wouldn't have come at all. I am expected at Castle Stokeworth for supper." | Cersei uses the accusation window to detach Bronn from Tyrion by arranging his marriage to Lollys Stokeworth. Bronn's defection is a direct downstream consequence of Tyrion's imprisonment. `bronn-of-the-blackwater` node exists; causal wire is absent. |
| death-of-joffrey-baratheon | ENABLES | cersei-plots-against-margaery | 2 | sources/chapters/asos/asos-sansa-06.md:193 | "The old woman understood something else as well. Her son was determined to make Margaery a queen, and for that he needed a king . . . but he did not need Joffrey." | With Joffrey dead, Margaery is no longer protected by a husband with a Lannister army. Cersei now has both motive and political latitude to move against her. The node `cersei-plots-against-margaery` already exists with 0 edges; this wire opens the causal path from death → opportunity. Tier-2: the causation is stated obliquely in Littlefinger's analysis of the Tyrell position, inferring Cersei's opening rather than stating it outright. |
| sansa-receives-the-poisoned-hairnet | DECEIVES | sansa-stark | 1 | sources/chapters/asos/asos-tyrion-08.md:101 | "I was very sorry to hear about your losses . . . There, that's better." Lady Olenna smiled. | On-page enactment of Olenna straightening Sansa's hair net and extracting the Strangler crystal — Sansa is the unwitting deceived party. This is the canonical deception moment. Tier-1: on-page participant fact. |
| tyrion-accused-of-poisoning-joffrey | SUSPECTED_OF | tyrion-lannister | 1 | sources/chapters/asos/asos-tyrion-08.md:319 | "My son was poisoned." She looked to the white knights standing helplessly around her. "Kingsguard, do your duty. . . . Arrest my brother . . . He did this, the dwarf." | Establishes the in-world false accusation layer that the baseline notes is missing. Cersei's accusation is the inaugural SUSPECTED_OF claim in the diegesis. Existing edge: `cersei-lannister AGENT_IN tyrion-accused-of-poisoning-joffrey` — this `SUSPECTED_OF` runs from the *event* to the *accused person* (the whodunit layer), which is a different semantic. |

---

## Proposed new nodes

### `sansa-assumes-alayne-stone-identity` (event.deception)

**Justification:** Sansa's adoption of the "Alayne Stone" alias is not a minor detail — it is the political-survival mechanism that enables her entire AFFC/ADWD arc. It is caused by the exfiltration (which is itself caused by Joffrey's death). No existing node covers this identity-replacement event. It is on-page, load-bearing, and a distinct event from `littlefinger-smuggles-sansa-out-of-kings-landing` (the smuggling happens first; the identity construction happens after landfall).

**Suggested slug:** `sansa-assumes-alayne-stone-identity`  
**Type:** `event.deception`  
**Anchor quote:** `"Varys has informers everywhere. If Sansa Stark should be seen in the Vale, the eunuch will know within a moon's turn, and that would create unfortunate . . . complications. It is not safe to be a Stark just now. So we shall tell Lysa's people that you are my natural daughter."` — asos-sansa-06.md:105  
**Participants:** petyr-baelish AGENT_IN, sansa-stark VICTIM_IN  
**Note:** This node is also the natural target for a `PART_OF littlefinger-smuggles-sansa-out-of-kings-landing` or `SUB_BEAT_OF` relationship, and for `ENABLES` edges into Sansa's Vale arc.

---

## Harvest finds

- `sources/chapters/asos/asos-sansa-05.md:23` / **object / quote-depth** — "The web of spun silver hung from her fingers, the fine metal glimmering softly, the stones black in the moonlight. Black amethysts from Asshai. One of them was missing." — richest physical description of the Strangler hairnet; no quote depth attached to `sansa-receives-the-poisoned-hairnet`
- `sources/chapters/asos/asos-sansa-05.md:13` / **quote** — "Far across the city, a bell began to toll. 'Joffrey is dead,' she told the trees, to see if that would wake her." — Sansa's first reaction to the death; haunting opening for the node
- `sources/chapters/asos/asos-sansa-05.md:17` / **quote / emotional texture** — "He was dead, he was dead, he was dead, dead, dead. Why was she crying, when she wanted to dance? Were they tears of joy?" — her joy/grief conflation; high-value for character voice layer
- `sources/chapters/asos/asos-tyrion-08.md:155` / **food/feast** — seventy-seven course feast: mushroom-and-snail soup, pork coffyn pastry, sweetcorn fritters, trout in almond crust, pigeon pie, roasted elk stuffed with blue cheese — zero feast-texture attached to `purple-wedding` hub; massive food-extraction opportunity
- `sources/chapters/asos/asos-tyrion-08.md:301` / **quote** — "Prince Tommen was screaming and crying." — Tommen's on-page witness of his brother's death; potential `WITNESS_IN` edge to `death-of-joffrey-baratheon`
- `sources/chapters/asos/asos-tyrion-08.md:315` / **quote** — "Lord Tywin said. He put his gloved hand on his daughter's shoulder . . . 'The boy is gone, Cersei. Unhand him now. Let him go.'" — Tywin's immediate response to Joffrey's death; characterization of Tywin's control vs. Cersei's grief
- `sources/chapters/asos/asos-sansa-06.md:187` / **foreshadowing** — "Toss Joffrey, Margaery, and Loras in a pot, and you've got the makings for kingslayer stew." — Littlefinger's analysis of why Olenna had to act; could wire to `tyrell-plot-revealed` as rationale evidence
- `sources/chapters/asos/asos-tyrion-09.md:379` / **political consequence** — Oberyn's point that by Dornish law Myrcella should inherit over Tommen: "He may indeed crown Tommen, here in King's Landing. Which is not to say that my brother may not crown Myrcella, down in Sunspear." — Dornish succession dispute as downstream consequence of Joffrey's death; unconnected to any existing node
