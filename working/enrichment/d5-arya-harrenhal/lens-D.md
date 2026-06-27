# Lens D — existing-node↔existing-node causal wiring (cross-arc seams) — D5 Arya/Harrenhal proposal (S154)

> **Scope reminder:** Lens D finds real causal edges between ALREADY-BUILT nodes, especially cross-arc seams. It
> does NOT mint new nodes; that is other lenses' work. Every proposal here is a new *edge* between two nodes that
> already exist in `graph/nodes/`.

---

## Proposed NEW nodes

*None.* Lens D is edge-only. All node proposals are routed to Lens A / Lens B.

---

## Proposed NEW edges

### Seam 1 — Tywin's war strategy → the holdfast attack

**Background:** The key causal gap in the D5 spine is that `fight-at-the-holdfast` has zero incoming causal edges.
The chain Tywin → chevauchée → holdfast attack → capture → Harrenhal is documented in Tywin's node prose and in
`acok-arya-07.md` but not wired in the graph. Two edges close this gap.

---

**Edge D-01**

| field | value |
|---|---|
| source | `tywin-lannister` |
| edge type | `COMMANDS_IN` |
| target | `fight-at-the-holdfast` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"He'd sent Gregor Clegane and Vargo Hoat to destroy Roose Bolton and remove the dagger from his back"` acok-arya-07:71 |
| rationale | Tywin commanded the chevauchée that sent Gregor Clegane and Amory Lorch sweeping through the Riverlands; that same raiding operation is what brought Amory's column into contact with Yoren's band at the holdfast by the Gods Eye. Gregor `COMMANDS_IN fight-at-the-holdfast` already exists; Tywin is one level above, orderer of the whole campaign. The text quote puts Tywin as the sender of Gregor+Hoat into the Riverlands theater; the holdfast fight is a direct product of that raiding sweep. |

---

**Edge D-02**

| field | value |
|---|---|
| source | `gregor-raids-the-riverlands` |
| edge type | `CAUSES` |
| target | `fight-at-the-holdfast` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"One of the women said that his men had ridden all the way around the lake chasing Beric Dondarrion and slaying rebels"` acok-arya-07:77 |
| rationale | The holdfast fight is a moment *within* the broader raiding sweep: Amory Lorch's column, executing the Riverlands chevauchée ordered by Tywin, encountered Yoren's band while returning. `gregor-raids-the-riverlands` (event.incident, AGOT-origin node, already wired to Tywin via COMMANDS_IN) extends into ACOK as the same ongoing campaign — the holdfast attack is a direct causal product. A mediated CAUSES is correct (the chevauchée produces the encounter; a free actor — Amory — makes the decision to attack). **[BORDERLINE]** on whether this should be ENABLES (chevauchée put soldiers in the area; Amory chose to attack) vs CAUSES (the raiding sweep directly produced the holdfast battle). I lean CAUSES because the attack is mission-execution, not an independent free choice. Gate should adjudicate. |

---

**Edge D-03**

| field | value |
|---|---|
| source | `fight-at-the-holdfast` |
| edge type | `CAUSES` |
| target | `arya-captured` |
| tier | Tier-1 |
| qualifier | — |
| evidence | `"Eight days she had lingered there before the Mountain gave the command to march, and every day she had seen someone die"` acok-arya-06:13 |
| rationale | `arya-captured` is already a `SUB_BEAT_OF fight-at-the-holdfast`; that structural edge is correct (it is a finer beat within the battle). But the cluster also needs a causal CAUSES because the battle directly produced the captive state. SUB_BEAT_OF is not a causal type — it is structural containment. The battle CAUSES the capture. This is the marquee gap: the fight-at-the-holdfast has 0 causal edges out. This closes the most urgent one. |

> Note: `gendry-captured` and `lommy-yields-and-is-killed` are also SUB_BEATs of the same hub. The same CAUSES
> logic applies; the synthesis may wish to add `fight-at-the-holdfast CAUSES gendry-captured` in parallel.

---

### Seam 2 — Beric Dondarrion as the hunt's stated motivation (the Tickler interrogations)

**Background:** The Tickler's interrogations ("where is Lord Beric Dondarrion?") are explicitly the stated
*purpose* of Gregor's men brutalizing captives in acok-arya-06. `beric-dondarrion` exists as a node with
COMMANDS brotherhood-without-banners. The interrogation event node `daily-interrogations-and-killings` has
Gregor COMMANDS_IN and Tickler + Chiswyck AGENT_IN — but no outgoing motive link. The target of the questioning
is Beric; the act of interrogating is driven by Gregor/Tywin's hunt for him.

---

**Edge D-04**

| field | value |
|---|---|
| source | `daily-interrogations-and-killings` |
| edge type | `SEEKS` |
| target | `beric-dondarrion` |
| tier | Tier-1 |
| qualifier | — |
| evidence | `"Where was Lord Beric Dondarrion? Which of the village folk had aided him? When he rode off, where did he go?"` acok-arya-06:25 |
| rationale | The interrogations' explicit stated purpose is to locate Beric and determine his numbers. `SEEKS` (source actively tries to find/acquire target) maps perfectly. This closes the dangling motive on the Tickler's torture event, wiring it into the Beric/Brotherhood-Without-Banners arc. |

---

**Edge D-05**

| field | value |
|---|---|
| source | `tywin-lannister` |
| edge type | `SEEKS` |
| target | `beric-dondarrion` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"There was always talk of Beric Dondarrion. … Lannister men in the riverlands are harassed by the outlaw brotherhood of Lord Beric Dondarrion"` (Tywin node prose: wiki:Tywin_Lannister) |
| rationale | Tywin's hunt for Beric is the strategic motivation behind the Riverlands chevauchée. The arc: Tywin SEEKS Beric → Tywin COMMANDS_IN gregor-raids-the-riverlands → gregor-raids-the-riverlands CAUSES fight-at-the-holdfast. This completes the causal chain from Tywin's strategic priority all the way to the D5 cluster. Tier-2 because the direct "Tywin ordered men to find Beric" is in the node prose/wiki, not a direct verbatim book quote from the D5 chapters. |

---

### Seam 3 — fall-of-harrenhal → red-wedding (Roose departs Harrenhal for the Twins)

**Background:** The fall-of-harrenhal currently has only PART_OF war-of-the-five-kings and PRECEDES battle-of-the-blackwater as outgoing edges. Roose Bolton's departure from Harrenhal to attend the Red Wedding is text-direct in acok-arya-10 (he is being leeched while discussing strategy, intending to leave Harrenhal to Vargo Hoat). This is the highest-value seam connecting the D5 cluster to the WO5K spine at the Red Wedding.

---

**Edge D-06**

| field | value |
|---|---|
| source | `fall-of-harrenhal` |
| edge type | `ENABLES` |
| target | `red-wedding-conspiracy` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"I mean to give Harrenhal to Lord Vargo when I return to the north"` acok-arya-10:185 |
| rationale | Roose Bolton taking Harrenhal (fall-of-harrenhal) is the enabling step for Roose's subsequent departure northward to the Twins, where he participates in the Red Wedding conspiracy. Without holding Harrenhal to "give to Vargo," Roose would have had no Riverlands base from which to strategically reposition toward the Red Wedding. ENABLES rather than CAUSES: the fall puts Roose in position, but Roose and Tywin/Frey still make the free choices that constitute the conspiracy. |

---

**Edge D-07**

| field | value |
|---|---|
| source | `roose-bolton` |
| edge type | `RULES` |
| target | `harrenhal` |
| tier | Tier-1 |
| qualifier | `ACOK` (book qualifier) |
| evidence | `"'On your knees for the Lord of the Dreadfort!' shouted his squire … and Harrenhal knelt"` acok-arya-09:355 |
| rationale | Roose Bolton is confirmed as ruler of Harrenhal during ACOK (post-fall). The graph has RULES harrenhal from shella-whent (AGOT) and petyr-baelish (ADWD) via infobox, but no ACOK ruler. Roose's hold over Harrenhal is what enables his subsequent control of the region and the Frey/Bolton planning toward the Red Wedding. This directly wires roose-bolton into the location that is central to D5. |

> Note: `tywin-lannister RULES harrenhal` (ACOK, pre-fall) would be the mirror edge for the Lannister phase.
> That edge does not appear to exist in the graph. It is equally supported by the chapter text: `"They were being
> taken to serve Lord Tywin Lannister at Harrenhal, the Mountain told them"` acok-arya-06:37. I flag it as a
> second proposal here but defer to synthesis since Tywin's HOLDS_TITLE castellan relationship may already cover
> this semantically via `amory-lorch HOLDS_TITLE castellan`.

---

### Seam 4 — iron-coin origin seam (CONFIRM + complete)

**Task:** Verify that `iron-coin ENABLES arya-departs-for-braavos` exists and is coherent end-to-end.

**Verified:** `iron-coin ENABLES arya-departs-for-braavos` EXISTS (acok-arya-09:327 re: ASOS recollection cite).
`iron-coin WIELDED_IN arya-departs-for-braavos` EXISTS.
`iron-coin GIFTED_TO arya-stark` EXISTS (ASOS cite, recollection).

**Gap found:** The iron coin's `GIFTED_TO` edge cites the ASOS recollection, not the actual acok-arya-09 gifting scene. The primary scene at acok-arya-09:327 is the actual text event: `"He lifted her hand and pressed a small coin into her palm"`. Lens B is proposing the origin event node `jaqen-gives-arya-the-iron-coin`; if Lens B's node is minted, the iron-coin WIELDED_IN / GIFTED_TO edges should be regrounded to that node.

**The downstream Braavos seam is coherent:** iron-coin ENABLES arya-departs-for-braavos ENABLES arya-arrives-at-the-house-of-black-and-white. The acok-arya-10 use of the coin (Arya uses it to distract the gate guard before killing him) is a *different* wielding than the Braavos use, and deserves its own WIELDED_IN edge:

---

**Edge D-08**

| field | value |
|---|---|
| source | `iron-coin` |
| edge type | `WIELDED_IN` |
| target | (the escape-from-harrenhal event, if Lens A/B mint it — slug TBD, e.g. `arya-escapes-harrenhal`) |
| tier | Tier-1 |
| qualifier | — |
| evidence | `"Her fingers dug down beneath her tunic and came out clutching the coin Jaqen had given her. In the dark the iron could pass for tarnished silver. She held it out . . . and let it slip through her fingers"` acok-arya-10:307 |
| rationale | Arya uses the iron coin (passing it as silver to the gate guard, then letting it drop so he kneels) as the specific instrument enabling her to kill the gate guard and open the postern. This is a distinct wielding from the Braavos departure scene. If `arya-escapes-harrenhal` is minted, iron-coin WIELDED_IN arya-escapes-harrenhal should be added. **[CONDITIONAL]** on the escape event node being minted. |

---

### Seam 5 — incident-at-the-trident → Arya's kill-list / vengefulness

**Task:** Assess whether `incident-at-the-trident MOTIVATES arya-stark` is text-grounded.

**Finding:** The text connects Mycah's death and the Trident incident to Arya's vengefulness, but the direct
causal expression is through the kill-list (already built: `kill-list-recitation-before-sleep`). The Hound
appears on the kill-list explicitly for Mycah ("the Hound for killing the butcher's boy Mycah" — acok-arya-06:57).

MOTIVATES has target = character, which means `incident-at-the-trident MOTIVATES arya-stark` is structurally
valid. However, examining the existing graph, `dareon MOTIVATES arya-stark` already exists (ADWD). The question
is whether the Trident incident is the *origin* of Arya's kill-list habit (it is one of the origins, alongside
her father's execution and other events). The text in acok-arya-06:57 frames it as one item on the list ("the
Hound for killing the butcher's boy Mycah"), not as the single motivator.

**Decision:** PROPOSE as Tier-2 with tight scope — the incident-at-the-trident as co-motivator of Arya's kill-list practice specifically, grounded in the kill-list naming Sandor for Mycah.

---

**Edge D-09**

| field | value |
|---|---|
| source | `incident-at-the-trident` |
| edge type | `MOTIVATES` |
| target | `arya-stark` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"the Hound for killing the butcher's boy Mycah"` acok-arya-06:57 |
| rationale | The incident at the Trident (Mycah's death + Lady's death) is explicitly named as one of the origin events that populates Arya's kill-list. The kill-list habit is the outward expression of her vengefulness, and the Trident incident is textually cited as one of its causes. Tier-2 (strong inference: the text names the kill-list entry, but does not say "the Trident motivated me"). The 0-outgoing dead-end on incident-at-the-trident is the structural gap this closes. |

---

### Seam 6 — Cersei's hunt for Gendry → why the gold-cloaks came to Yoren's band

**Background:** `cersei-lannister SEEKS gendry` EXISTS (acok-arya-02:155). `gendry-captured` SUB_BEAT_OF
`fight-at-the-holdfast` EXISTS. The gap: there is no edge from `cersei-lannister SEEKS gendry` → the eventual
capture. The gold-cloaks arrived at Yoren's band on the road (acok-arya-02), Yoren turned them away; later
Gregor's men captured Gendry at the holdfast. The gold-cloak visit is the first attempt; the holdfast capture is
the second-order consequence of Gendry traveling with Yoren's band (which Yoren's protection of him set in motion).

The most defensible wiring is a causal edge from Cersei's hunt to Yoren's protective decision, or from the
gold-cloak attempt (which pushed Gendry deeper into the Riverlands journey) to the eventual holdfast capture.
However, Gregor's men at the holdfast were NOT hunting Gendry specifically — they were Amory Lorch's raiders
on the chevauchée, who captured everyone present. The connection is real but mediated by many actors.

**Decision:** The seam is genuine but too mediated for a direct CAUSES edge. Closer: `cersei-lannister SEEKS
gendry` as an existing edge already captures the intent. What's missing is a CAUSES from the gold-cloak visit
specifically. The gold-cloak visit node would need to be built first (a Lens A/B candidate). Without that node,
propose only the following:

---

**Edge D-10**

| field | value |
|---|---|
| source | `cersei-lannister` |
| edge type | `CAUSES` |
| target | `gendry-captured` |
| tier | Tier-2 |
| qualifier | — |
| evidence | `"Who is it wants this boy?" The other gold cloaks were dismounting to stand beside Yoren"` acok-arya-02:155 |
| rationale | Cersei's manhunt for Robert's bastards (SEEKS gendry exists) is the driving force that put Gendry on the run in Yoren's band. The gold-cloaks attempted to seize Gendry on the road (acok-arya-02). Yoren turned them away but the danger was real and ongoing. Gendry's presence in Yoren's band — rather than safely at his smithing — is directly attributable to Cersei's purge; that's what landed him at the holdfast and made him a captive. The capture event is a downstream consequence of the hunt. **[BORDERLINE]** — the causal chain has several mediating steps (Yoren's protection, the Riverlands journey, Amory's raid). Synthesis should assess whether CAUSES is too strong and ENABLES is more honest. |

---

### Seam 7 — Roose Bolton departs Harrenhal (the Red Wedding → departure seam)

The `capture-of-harrenhal` node (wiki-sourced) describes Roose's *departure* from Harrenhal to go to the
Red Wedding. This departure is in acok-arya-10 text:

---

**Edge D-11**

| field | value |
|---|---|
| source | `roose-bolton` |
| edge type | `TRAVELS_TO` |
| target | `the-twins` |
| tier | Tier-1 |
| qualifier | — |
| evidence | `"I mean to give Harrenhal to Lord Vargo when I return to the north"` acok-arya-10:185 |
| rationale | Roose explicitly states his intention to leave Harrenhal to Vargo and return north. The destination is the Twins (Red Wedding context). `the-twins` exists as a node (House Frey seat). This departure is the causal link between the D5 Harrenhal cluster and the Red Wedding arc. Tier-1 from the direct quote; northward return destination = the Twins per the Red Wedding conspiracy timeline. **[BORDERLINE]** on whether `the-twins` is the correct target slug (it is the Frey stronghold and the Red Wedding location). |

---

### Seam 8 — brave-companions' allegiance flip (Lannister → Bolton)

**Context:** `brave-companions BETRAYS house-lannister` EXISTS (ASOS cite). `brave-companions SWORN_TO
roose-bolton` EXISTS. The D5 angle is the *mechanism* of the flip: Vargo Hoat approached Roose Bolton's
encampment before the fall and struck a deal (per fall-of-harrenhal node prose). This is relevant in acok-arya-09
where the Bloody Mummers arrive with Bolton prisoners, establishing the quid-pro-quo.

**Edge:** `brave-companions CAUSES fall-of-harrenhal` — the Brave Companions' double-cross of the Lannister
garrison (killing them in their beds) is the proximate act that hands Harrenhal to Bolton. `vargo-hoat BETRAYS
amory-lorch` EXISTS already. The group-level parallel:

---

**Edge D-12**

| field | value |
|---|---|
| source | `brave-companions` |
| edge type | `CAUSES` |
| target | `fall-of-harrenhal` |
| tier | Tier-1 |
| qualifier | — |
| evidence | `"Them Bloody Mummers killed some of Ser Amory's lot in their beds, and the rest at table after they were good and drunk"` acok-arya-09:349 |
| rationale | The fall of Harrenhal to Bolton is directly caused by the Brave Companions' mass killing of the Lannister garrison. The group-level CAUSES edge complements the existing individual-level `vargo-hoat BETRAYS amory-lorch`. No group-to-event causal edge exists; this is the highest-value structural seam closing the gap. |

---

## Node-tangle flag

### `capture-of-harrenhal` conflation warning

**Nodes involved:**
- `capture-of-harrenhal` (event.battle, wiki-sourced, bucket battles-b-d, 0 incoming edges)
- `fall-of-harrenhal` (event.battle, wiki-sourced, bucket battles-d-f, 5 total edges, the D5 working node)
- `yielding-of-harrenhal` (event.battle, wiki-sourced, 3 edges — references the AGOT Lannister seizure from House Whent)
- `assault-on-harrenhal` (event.battle, wiki-sourced, 14 edges — DANCE OF THE DRAGONS era, completely different event)

**What each actually denotes:**

| slug | what it actually is |
|---|---|
| `fall-of-harrenhal` | ACOK (299 AC): Bolton/Brave Companions take Harrenhal from Amory Lorch's Lannister garrison — the D5 event |
| `capture-of-harrenhal` | ASOS/AFFC: Gregor Clegane retakes Harrenhal from Vargo Hoat on Tywin's orders (the Brave Companions flee/are destroyed) — completely different event, different book, different actors |
| `yielding-of-harrenhal` | AGOT (298 AC): Lady Shella Whent yields Harrenhal to Tywin's invading Lannister host — prewar AGOT event |
| `assault-on-harrenhal` | Dance of the Dragons (circa 130 AC) — 170 years earlier, dragons-era, no overlap |

**The confusion:** `capture-of-harrenhal` in the wiki article describes Gregor Clegane's ASOS retaking of Harrenhal (for Tywin, after Vargo Hoat's capture and decay). Its `ENABLES raid-on-saltpans` edge confirms this is the AFFC aftermath (the Brave Companions scatter after losing Harrenhal, some go to Saltpans). This is NOT the ACOK fall at all.

**Current graph state:** `capture-of-harrenhal` has 0 incoming edges and 2 outgoing (ENABLES raid-on-saltpans, PART_OF war-of-the-five-kings). It is a structurally isolated correct node that is simply named confusingly relative to `fall-of-harrenhal`.

**Recommended hygiene action:** No deletion. No merge. These are three distinct events in the same location across different books. Recommended actions:
1. Add `aliases: ["Lannister recapture of Harrenhal", "Gregor takes Harrenhal"]` to `capture-of-harrenhal` to distinguish it from `fall-of-harrenhal`.
2. Add `aliases: ["Bolton takeover of Harrenhal", "weasel-soup takeover"]` to `fall-of-harrenhal` to anchor it in the ACOK context.
3. Add `aliases: ["Lannister yielding", "Whent yields to Tywin"]` to `yielding-of-harrenhal` to anchor it in AGOT.
4. Do NOT wire edges intended for `fall-of-harrenhal` to `capture-of-harrenhal` — they are separate events.
5. This is purely an alias/metadata hygiene pass, not a graph structure change.

---

## Dropped / considered-but-rejected

- **`tywin-lannister RULES harrenhal` (ACOK):** Valid Tier-1 edge with direct text ("taken to serve Lord Tywin Lannister at Harrenhal" acok-arya-06:37), but semantically the pre-fall Lannister hold is arguably already captured by `amory-lorch HOLDS_TITLE castellan` and `tywin-lannister COMMANDS amory-lorch`. Deferred to synthesis to decide if a direct RULES edge is additive or redundant.

- **`fight-at-the-holdfast LOCATED_AT gods-eye`:** Text supports it (the storehouse was beside the Gods Eye; Praed's DIED_AT gods-eye already exists). This is a straightforward gap in the baseline (gap #8 mentions this), but it is a Lens A/B event-role edge, not a cross-arc seam. Routing to synthesis as a note.

- **`yoren VICTIM_IN fight-at-the-holdfast`:** Gap #8 in baseline. Valid, but it's an event-role edge on an existing node pair, not a cross-arc seam. Lens A territory.

- **`incident-at-the-trident MOTIVATES arya-stark` for Lady's death:** Lady's death is a distinct sub-beat; the kill-list text names specific actors, not Lady. Not proposing — too inferential.

- **`gregor-raids-the-riverlands ENABLES fight-at-the-holdfast` (alternative to CAUSES D-02):** ENABLES is more conservative (puts soldiers in the area; Amory makes the choice to attack). The synthesis gate should decide between CAUSES and ENABLES for D-02; I lean CAUSES because the attack is mission-execution of the chevauchée, not an independent decision.

- **`red-wedding-conspiracy ENABLES fall-of-harrenhal`:** Reversed causality — the Red Wedding conspiracy was organized AFTER Roose held Harrenhal, not before it. The fall ENABLES the conspiracy, not vice versa.

- **`brave-companions ENABLES fall-of-harrenhal`:** CAUSES (D-12) is the right type here — the Brave Companions' attack is the proximate cause, not merely a precondition.

- **Any theory-gated edges re Jaqen's identity, the Faceless Men cosmology, or the iron coin as magic:** Gated per HARD RULES.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | ACOK | acok-arya-09:47 | Arya filches a fruit-and-cheese-and-nut tart from Hot Pie's tray; "stuffed with chopped nuts and fruit and cheese, the crust flaky and still warm" — vivid specific food description |
| food | ACOK | acok-arya-09:47 | The midnight kitchen scene: ham carved cold, spit rabbits basted with honey, onions and carrots chopped for broth — full kitchen catalogue |
| food | ACOK | acok-arya-09:239 | Biter tears into half-charred rabbit right off the spit, "honey dripped between his fingers" then licks grease off fingers — savage eating vignette |
| food | ACOK | acok-arya-09:263 | The dungeon massacre setup: boiling broth in heavy iron kettles — the "weasel soup" — described in operational detail: broth "boiling hot," "thin" per the cook |
| food | ACOK | acok-arya-09:283 | Biter sits on a dead guard "holding a limp hand as he gnawed at the fingers. Bones cracked between his teeth" — grim register: cannibalism |
| food | ACOK | acok-arya-10:161 | Roose Bolton's supper: "barley bread, butter, and boar" + "hot spice wine" (a heavy sweet red with crumbled spices, heated in a kettle, wrapped in towel to stay warm) — specific lord's meal |
| food | ACOK | acok-arya-10:165 | Kitchen scene: oatcakes, fish being boned, boar on spit — full kitchen inventory during Bolton's tenure |
| food | ACOK | acok-arya-09:149 | Ser Aenys Frey's war-council speech about the food situation at Harrenhal: "The country is ash, the villages given over to wolves, the harvest burnt or stolen. Autumn is on us, yet there is no food in store and none being planted. We live on forage, and if the Lannisters deny that to us, we will be down to rats and shoe leather in a moon's turn" — strategic food-scarcity quote |
| food | ACOK | acok-arya-06:27 | The Tickler's interrogation haul: "a little gold, a little silver, a great sack of copper pennies, and a dented goblet set with garnets" + from prisoners: "he had ten starvelings with him, or else a hundred mounted knights" — the starveling detail (famine register) |
| food | ACOK | acok-arya-06:51 | Gregor's chevauchée plunder list: "a dozen pigs, a cage of chickens, a scrawny milk cow, and nine wagons of salt fish" — war-forage register, specific quantities |
| food | ACOK | acok-arya-09:45 | Hot Pie's kitchen at midnight: "bread and tarts" — the oven scene; also the Brave Companions' arrival demanding food and drink ("clamored for drink") |
| physical description | ACOK | acok-arya-06:65 | Harrenhal's towers described in full: "five immense towers… the shortest of them was half again as tall as the highest tower in Winterfell… they did not soar the way a proper tower did… like some old man's gnarled, knuckly fingers groping after a passing cloud… each tower was more grotesque and misshapen than the last, lumpy and runneled and cracked" |
| physical description | ACOK | acok-arya-06:63 | The stone melted in dragon fire: "the stone had melted and flowed like candlewax down the steps and in the windows, glowing a sullen searing red as it sought out Harren where he hid" |
| physical description | ACOK | acok-arya-09:355 | Roose Bolton's physical description on first appearance: "plain face, beardless and ordinary, notable only for his queer pale eyes… black ringmail and a spotted pink cloak. The sigil on his banner looked like a man dipped in blood" |
| hospitality / guest right | ACOK | acok-arya-10:17 | Post-fall executions for having served Tywin: "Tothmure had been sent to the axe for dispatching birds to Casterly Rock and King's Landing the night Harrenhal had fallen, Lucan the armorer for making weapons for the Lannisters, Goodwife Harra for telling Lady Whent's household to serve them, the steward for giving Lord Tywin the keys to the treasure vault" — guest-service as treason |
| quote (load-bearing) | ACOK | acok-arya-06:59 | Arya's prayer-list in full: "Ser Gregor. Dunsen, Polliver, Chiswyck, Raff the Sweetling. The Tickler and the Hound. Ser Amory, Ser Ilyn, Ser Meryn, King Joffrey, Queen Cersei" — canonical kill-list text anchor |
| quote (load-bearing) | ACOK | acok-arya-09:339 | Iron coin giving: "He lifted her hand and pressed a small coin into her palm" and the valar morghulis exchange — the origin scene verbatim |
| quote (load-bearing) | ACOK | acok-arya-10:311 | Gate guard kill: "'Valar morghulis,' she whispered as he died" — Arya's first deliberate solo kill with Needle, plus the iron coin used as distraction |
| quote (load-bearing) | ACOK | acok-arya-09:117 | "Jaqen made me brave again. He made me a ghost instead of a mouse" — Arya's internal reflection on Jaqen's effect on her, strong character-voice anchor |
| foreshadowing | ACOK | acok-arya-10:157 | "the Titan of Braavos" named in Arya's fantasy of flying: foreshadows her Braavos arc |
| foreshadowing | ACOK | acok-arya-07:71 | "He'd sent Gregor Clegane and Vargo Hoat to destroy Roose Bolton" — the strategic framing that shows Tywin intended Roose's destruction; Roose's survival sets up his betrayal |
