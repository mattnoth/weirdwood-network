# Lens D — Existing-node ↔ Existing-node Causal Wiring — A2.4 Tyrion / Essos proposal (S161)

## Scope
Four chapters read in full: `adwd-tyrion-01`, `adwd-tyrion-05`, `adwd-tyrion-11`, `adwd-tyrion-12`.
Cross-checked `adwd-tyrion-06` lines 21–23 for the river-rescue confirmation (Griff/Jon Connington pulled
Tyrion out; Lemore forced water from his lungs — greyscale infection occurs at the moment of river contact).

Focus: wiring EXISTING nodes to EXISTING nodes across the four highest-value seams the prompt identifies.
New spine node proposals (terminus nodes Lenses A/C will mint) are noted where needed for wiring but NOT
minted here — this lens proposes the causal edges only.

---

## Proposed NEW nodes

### Node 1
- **slug:** `tyrion-arrives-in-pentos`
- **name:** Tyrion Arrives in Pentos
- **type:** event.incident
- **body:** Tyrion is smuggled across the Narrow Sea in a wine cask by Varys's agents and decanted in Illyrio
  Mopatis's cellar in Pentos, arriving as a fugitive following Tywin's murder. The arrival inaugurates his
  Essos exile and places him under Illyrio's protection. This is the forward terminus that makes
  `varys-smuggles-tyrion-out-of-kings-landing` non-islanded.
- **anchor quote:** "My house is yours. Any friend of my friend across the water is a friend to Illyrio
  Mopatis, yes." — `adwd-tyrion-01:65`

### Node 2
- **slug:** `tyrion-joins-second-sons`
- **name:** Tyrion Joins the Second Sons
- **type:** event.incident
- **body:** Tyrion, Penny, and Jorah Mormont walk into the Second Sons camp under cover of fetching water for
  the dying Yezzan. Tyrion negotiates with Brown Ben Plumm — signing promissory notes for 100,000 dragons,
  a castle, and a lordship — and formally joins the company by signing the book in blood. This is the ADWD
  terminus that wires the Tyrion-Essos arc into the Meereen siege. (The cloak-turn-back to Daenerys is TWOW —
  not in scope here.)
- **anchor quote:** "I am now a Second Son." — `adwd-tyrion-12:121`

---

## Proposed NEW edges

### Seam 1 — Smuggling forward into Pentos arrival (ISLANDED HUB wire)

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `varys-smuggles-tyrion-out-of-kings-landing` | ENABLES | `tyrion-arrives-in-pentos` | Tier-1 | — | "He found a fresh skin of wine instead and sucked at it as if it were a woman's breast." (`adwd-tyrion-01:47`) — Tyrion is still at sea in the cask on the voyage Varys arranged | The smuggling operation IS the transport; arrival in Pentos is causally enabled by it. Varys arranged passage; Tyrion decanted in Illyrio's cellar is the direct product. |
| `tyrion-arrives-in-pentos` | ENABLES | `shy-maid` (voyage/departure beat, if minted) | Tier-2 | — | "My little friend and I shall eat and drink and make great plans, yes?" (`adwd-tyrion-01:93`) | Pentos sojourn → departure with Illyrio is the precondition for boarding. Tier-2: the exact departure-event node may not exist yet; gate to synthesis. |

**Note on the quote for the first edge:** The smuggling → Pentos causal link is established by chapter 01's
opening scene (cask arrival, Illyrio's cellar), not a single quote on the smuggling-event node itself. Best
single-line anchor for the arrival side: "My house is yours. Any friend of my friend across the water is a
friend to Illyrio Mopatis, yes." (`adwd-tyrion-01:65`) — this is the moment Illyrio acknowledges Tyrion's
arrival as Varys's ward, making the Varys→Illyrio→Tyrion chain explicit. Use this for the arrival node's
anchor; the ENABLES edge's evidence_quote should cite the cask-decanting passage at line 53:
"Through the wooden staves he heard men shouting … the lid cracked open suddenly." (`adwd-tyrion-01:53`)

Revised table entry for edge 1A:
- `varys-smuggles-tyrion-out-of-kings-landing` ENABLES `tyrion-arrives-in-pentos` | Tier-1 | "the lid cracked open suddenly. Light came flooding in, and cool air as well. Tyrion gasped greedily" `adwd-tyrion-01:53` | The smuggling operation delivers Tyrion to the cask; cracking the lid open IS the arrival, directly caused by Varys's plan.

---

### Seam 2 — Stone-men-attack-the-shy-maid: causal IN and OUT (ISLANDED HUB wire)

The event hub `stone-men-attack-the-shy-maid` currently has cOut=0, cIn=0. Two wires needed:

**Causal IN — the Sorrows approach:**
The Shy Maid entered the Sorrows (the flooded ruins of Chroyane) and drifted toward the Bridge of Dream;
the attack was inevitable because the current carried them under the bridge. The geography causes the
encounter — but this is a SEQUENCE (travel → location → attack), not a strict CAUSES chain. The right
type is ENABLES: the voyage through the Sorrows made the bridge encounter possible; the stone men then
acted (third-party agency). The specific enabling moment is when the current took them past the point of
no return:

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `shy-maid` (vessel/voyage) | ENABLES | `stone-men-attack-the-shy-maid` | Tier-1 | — | "The current had them in its teeth. They drifted inexorably toward the bridge." `adwd-tyrion-05:203` | The river current carrying the Shy Maid under the Bridge of Dream is the direct physical precondition; the stone men jumping is the third-party act. ENABLES is correct (not CAUSES). |

**Causal OUT — Jon Connington infected (greyscale seam):**

The attack is where Griff (Jon Connington) pulled Tyrion from the Rhoyne — the river contact is when he
was infected. The existing edge `jon-connington AFFLICTED_BY greyscale` is a STATE edge; the attack
EVENT is what caused the infection exposure. The chain: attack → Griff enters the river to pull Tyrion out
→ greyscale infection. The AFFLICTED_BY edge already exists; what is missing is the event→state temporal
link.

Since AFFLICTED_BY is a state edge on a character (not an event), the correct wiring is:
- The attack ENABLES the infection exposure (the rescue is what caused Griff's contact with Rhoyne water).
- `greyscale` as a disease entity: `stone-men-attack-the-shy-maid` CAUSES the infection event / ENABLES
  the AFFLICTED_BY state.

The ENABLES-to-a-state-edge problem: we cannot draw ENABLES to `jon-connington AFFLICTED_BY greyscale`
directly (that's an edge, not a node). The correct wire is from the attack event to `jon-connington`
himself, typed MOTIVATES? No — MOTIVATES is for character decisions. The right approach: the rescue
(Griff-pulled-Tyrion-from-river) is itself a SUB-BEAT of the stone-men-attack event. If a
`jon-connington-rescues-tyrion-from-rhoyne` beat node exists or is minted (check Lens C), it would
be the direct link. Without that node, the best available edge is:

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `stone-men-attack-the-shy-maid` | CAUSES | `jon-connington` [greyscale infection] | Tier-1 | — | "it was Lemore who forced the water from your lungs after Griff had pulled you up. You were as cold as ice" `adwd-tyrion-06:21` | Griff entered Rhoyne water to rescue Tyrion during the attack; that river contact is where he contracted greyscale. The attack CAUSES the exposure event. **[BORDERLINE]** on edge shape — CAUSES with target `jon-connington` is ungrammatical (CAUSES should target an event, not a character); flag for synthesis to decide whether to mint a `griff-rescues-tyrion-from-rhoyne` sub-beat or route via MOTIVATES/ENABLES. |

**Cleaner alternative — ENABLES to the AFFLICTED_BY state, treating greyscale as the target entity:**

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `stone-men-attack-the-shy-maid` | ENABLES | `greyscale` (disease entity, already in graph) | Tier-2 | — | "it was Lemore who forced the water from your lungs after Griff had pulled you up." `adwd-tyrion-06:21` | The attack event is the proximate enabler of Griff's greyscale exposure. Tier-2 because the exposure is confirmed but the precise infection moment (river water during rescue) is narrated one chapter later, in Tyrion VI rather than in the attack chapter itself. **[BORDERLINE]** — synthesis should decide whether ENABLES(attack → greyscale-disease-entity) is the right shape or whether a sub-beat node is warranted. |

**Preferred recommendation to synthesis:** mint a small `griff-rescues-tyrion-from-rhoyne` sub-beat
(SUB_BEAT_OF `stone-men-attack-the-shy-maid`), assign `jon-connington AGENT_IN` + `tyrion VICTIM_IN`
(rescued) + `jon-connington AFFLICTED_BY greyscale` already exists → the sub-beat carries the
temporal anchor. Then the attack ENABLES the sub-beat (via the current → bridge passage), and the sub-beat
ENABLES the affliction state. This resolves the grammar problem cleanly. Lens C (which reads ch05) may
have already proposed this; flag as DEDUP candidate.

---

### Seam 3 — Pale mare kills Yezzan → enables escape → enables Second Sons joining (the SEQUENCE terminus)

`bloody-flux` node exists with 0 edges. Wire it:

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `bloody-flux` | CAUSES | `yezzan-zo-qaggaz` [death, via DIED_OF, if minted] | Tier-1 | — | "The pale mare," the man told Sweets. … "The noble Yezzan's life is in the hands of the gods." `adwd-tyrion-11:12-16` | The healer's diagnosis confirms Yezzan is dying of the pale mare / bloody flux. The CAUSES here is disease→character-death; the target should ideally be a death event node, but if none exists, flag for synthesis. |
| `bloody-flux` | ENABLES | `tyrion-joins-second-sons` | Tier-1 | — | "Yezzan has more urgent matters to concern him than three missing slaves. He's riding the pale mare." `adwd-tyrion-11:295` | Yezzan's pale-mare illness → the three nephews fled the camp → Nurse already dead → no one would notice three slaves missing. The flux is the direct precondition that makes the escape possible. |
| `yezzan-zo-qaggaz` | — | death event (DIED_OF bloody-flux) | Tier-1 | — | "Their mammoth master had died on the day of their escape, Brown Ben Plumm had told him." `adwd-tyrion-12:279` | Confirmation of death. The DIED_OF edge (yezzan → bloody-flux) is a candidate for Lens A/C; flag here for dedup. |

**The full seam chain (synthesis view):**
`bloody-flux` ENABLES escape from Yezzan's camp → `tyrion-joins-second-sons` ENABLES `siege-of-meereen`
(Tyrion's faction now inside the Second Sons at the Meereen siege lines).

---

### Seam 4 — Tyrion joins Second Sons → feeds into siege of Meereen (ARC TERMINUS wire)

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `tyrion-joins-second-sons` | ENABLES | `siege-of-meereen` | Tier-1 | — | "Oh, I know. The Second Sons are on the losing side. They need to turn their cloaks again and do it now." `adwd-tyrion-12:283` | Tyrion joining the Second Sons is his entry into the Meereen siege (the S144 event already exists). The ENABLES is correct: he joins → he is now at the siege, with agency inside the company. The cloak-turn-back is TWOW and is not proposed. |
| `tyrion-joins-second-sons` | AGENT_IN `tyrion-lannister` | — | Tier-1 | role edge | "I am now a Second Son." `adwd-tyrion-12:121` | Participant role on the joining event. |
| `tyrion-joins-second-sons` | AGENT_IN `jorah-mormont` | — | Tier-1 | role edge | "Jorah Mormont? Is that you? … Give me a sword and you can call me what you like, Ben." `adwd-tyrion-11:331-333` | Jorah co-joins with Tyrion; his signature is immediately above Tyrion's in the book. |
| `tyrion-joins-second-sons` | AGENT_IN `penny` | — | Tier-1 | role edge | "Can I sign too?" `adwd-tyrion-12:123` | Penny travels with Tyrion into the camp and is provisioned with armor; she is a participant even if she doesn't sign. |
| `tyrion-joins-second-sons` | LOCATED_AT `second-sons` (unit/camp) | — | Tier-1 | — | "Those are the tents we want, there." `adwd-tyrion-11:243` | Location anchor for the event. |

---

### Seam 5 — Murder of Tywin MOTIVATES Tyrion's entire exile (character motivation wire)

The `assassination-of-tywin-lannister` is already built and `varys-smuggles-tyrion-out-of-kings-landing`
is the immediate next event. The MOTIVATES edge (Tywin's murder → Tyrion's character motivation) bridges
the psychological launch to the exile:

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `assassination-of-tywin-lannister` | MOTIVATES | `tyrion-lannister` | Tier-1 | — | "He drank his way across the narrow sea." `adwd-tyrion-01:11` | The guilt + grief over Tywin's killing drives Tyrion's entire arc (suicidal drinking, exile, refusing Illyrio's mushrooms out of half-wanting death). MOTIVATES→character is correct here: the murder motivates Tyrion's psychological state of dissolution. |

**Note:** the MOTIVATES from `jaime-reveals-the-truth-of-tysha` to Tyrion also exists per baseline (check
dedup) — that's a separate edge targeting a different motivation (the Tysha revelation drives the immediate
killing of Tywin). The edge here is the murder itself → Tyrion's post-murder psychological arc. Likely
distinct; flag for synthesis to confirm no exact duplicate.

---

### Seam 6 — Cross-arc seam: Tyrion witnesses Aegon-is-Young-Griff reveal (S147 left out)

The baseline notes `tyrion MANIPULATES aegon` already exists. The S147 dedup hot zone covers Aegon-side
wiring. What S147 may have left islanded on the TYRION side: Tyrion is the character whose deduction
first exposes Aegon's identity on the boat. This is more dyad/perception territory (Lens B's domain) but
the causal seam for Lens D is:

`stone-men-attack-the-shy-maid` → the chaos of the attack is what provokes Tyrion's immediate
post-bridge confrontation with Aegon (ch05 lines 155–178: "Why am I everything?" → Tyrion reveals he
knows Aegon's identity). This is a short causal hop that produces a potentially load-bearing edge:

| source | edge type | target | Tier | qualifier / note | verbatim quote + chapter:line | rationale |
|--------|-----------|--------|------|-------------------|-------------------------------|-----------|
| `stone-men-attack-the-shy-maid` | TRIGGERS | `tyrion-lannister` [REVEALS_TO aegon identity knowledge] | Tier-2 | — | "By then the Shy Maid was well downstream of the Bridge of Dream … Why am I everything?" `adwd-tyrion-05:161` | The attack and its aftermath (Tyrion saving Young Griff → Aegon's gratitude → "You know who I am") is the TRIGGER that opens the identity confrontation. **[BORDERLINE]** — this is really TRIGGERS→an-event (the reveal conversation), not TRIGGERS→a-character. Synthesis should decide if a `tyrion-identifies-aegon` beat node is warranted (Lens B may have proposed it). If that node exists, the edge is `stone-men-attack-the-shy-maid` TRIGGERS `tyrion-identifies-aegon`. |

---

## Dropped / considered-but-rejected

1. **`illyrio-mopatis MOTIVATES tyrion-lannister`** via the dinner conversation and dragon revelation
   (`adwd-tyrion-01:271` "A dragon with three heads"): Illyrio's dinner pitch at the end of ch01 is
   clearly load-bearing motivation, but the edge `illyrio INFORMS tyrion` / MOTIVATES→tyrion may already
   exist in the 180-edge web. Flagged as DEDUP — Lens B reads ch01-02 and likely covers this. Not
   proposing to avoid collision.

2. **`assassination-of-tywin-lannister` TRIGGERS `varys-smuggles-tyrion-out-of-kings-landing`**: This
   is the most natural TRIGGERS in the chain, but it almost certainly exists in the S109/S139 KL web that
   the baseline explicitly says NOT to re-mint. Dropped (dedup).

3. **`tyrion-arrives-in-pentos` GUEST_OF `illyrio-mopatis`**: The dyad `tyrion GUEST_OF illyrio` already
   exists per baseline. Not re-proposing the bare dyad; the arrival node is the structural fix, not a
   new dyad.

4. **`bloody-flux` KILLS `nurse`** (adwd-tyrion-11:69 "Watered wine and lemonsweet and some nice hot
   dogtail soup, with slivers of mushroom in the broth … The last word Nurse ever said was, 'No.'" "):
   This is not pale-mare; Tyrion poisoned Nurse with mushrooms. The death is attributed to flux in
   public but is actually Tyrion's doing (the mushroom soup + "A Lannister always pays his debts" line).
   Edge type would be `tyrion KILLS nurse` (via mushroom soup). This is a significant edge but is
   dyad-territory (Lens A/B) and is inside the dense dyad web that already has `tyrion KILLS` entries.
   Flagged for Lens A; not proposing here.

5. **`greyscale MOTIVATES jon-connington`** already exists per baseline. Not re-proposing.

6. **Tyrion-Jorah dyad edges at the brothel (capture) seam**: `jorah-mormont CAPTURES tyrion-lannister`
   is a bare dyad per baseline. Lens B reads ch07 and will handle the event node build. Dropping from
   Lens D scope.

7. **Pure travel sequence edges** (Pentos → Rhoyne → Volantis → Slaver's Bay → Meereen): The shared
   instructions explicitly prohibit a false travel-causes-travel ladder. Every TRAVELS_TO hop is
   character→destination; not proposing any of them as causal chains.

8. **The Second Sons cloak-turn-back**: Tyrion says "they need to turn their cloaks again and do it now"
   (`adwd-tyrion-12:283`) and "Leave that to me." This is in-ADWD scheming only; the execution is TWOW.
   Hard rule: not proposed.

9. **`second-sons BETRAYS daenerys` / `ben-plumm-defects-to-yunkai`**: already in the S144 dedup hot
   zone. Not touched.

10. **`bloody-flux CAUSES daenerys-siege-of-meereen` disruption**: the flux sweeping the Yunkish camp
    is clearly consequential for the S144 siege arc, but the Dany-side Meereen spine is explicitly off
    limits (dedup). Not proposing cross-spine causal edges into the Dany web.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food | ADWD | adwd-tyrion-01:179 | The full Illyrio dinner feast: "broth of crab and monkfish, and cold egg lime soup … quails in honey, a saddle of lamb, goose livers drowned in wine, buttered parsnips, and suckling pig" — exceptional food description, first-class extraction target |
| food | ADWD | adwd-tyrion-01:213 | Second course: "heron stuffed with figs, veal cutlets blanched with almond milk, creamed herring, candied onions, foul-smelling cheeses, plates of snails and sweetbreads, and a black swan in her plumage" |
| food | ADWD | adwd-tyrion-01:247 | Dessert: "serving men spooned out bowls of black cherries in sweet cream for them both" |
| food | ADWD | adwd-tyrion-01:187 | The mushroom dish: "Mushrooms … Kissed with garlic and bathed in butter. I am told the taste is exquisite" — Illyrio offers suspected poison mushrooms; Tyrion declines then later tests them (they're safe, Illyrio eats two) |
| food | ADWD | adwd-tyrion-01:107 | Cellar wine inventory: "sweet reds from the Reach and sour reds from Dorne, pale Pentoshi ambers, the green nectar of Myr, three score casks of Arbor gold, even wines from the fabled east, from Qarth and Yi Ti and Asshai by the Shadow" |
| food | ADWD | adwd-tyrion-01:103 | Kitchen forage: "cheese, bread, and figs" |
| food | ADWD | adwd-tyrion-11:69 | Nurse's death meal: "Watered wine and lemonsweet and some nice hot dogtail soup, with slivers of mushroom in the broth" — the mushrooms-in-soup is the weapon (load-bearing quote, possible node anchor for Tyrion-kills-Nurse) |
| food | ADWD | adwd-tyrion-12:183–184 | Kem's nostalgia: "There was this pot shop, though. No one ever made a bowl o' brown like them. So thick you could stand your spoon up in the bowl, with chunks of this and that" — Flea Bottom bowl o' brown, classic hospitality/food reference |
| description | ADWD | adwd-tyrion-01:55 | Illyrio physical description: "a grotesque fat man with a forked yellow beard … His bedrobe was large enough to serve as a tourney pavilion … a huge white belly and a pair of heavy breasts that sagged like sacks of suet covered with coarse yellow hair. He reminded Tyrion of a dead sea cow" |
| description | ADWD | adwd-tyrion-01:159 | Illyrio's rings: "Jewels danced when he moved his hands; onyx and opal, tiger's eye and tourmaline, ruby, amethyst, sapphire, emerald, jet and jade, a black diamond, and a green pearl" |
| description | ADWD | adwd-tyrion-05:127 | Bridge of Dream / stone men approach: "shuffling aimlessly around the lamps like slow grey moths. Some were naked, others clad in shrouds" — vivid stone-men description |
| description | ADWD | adwd-tyrion-05:225 | Summer Islander stone man: "his jaw and half his cheek had turned to stone, but his skin was black as midnight where it was not grey … Where he had grasped the torch, his skin had cracked and split. Blood was seeping from his knuckles" |
| description | ADWD | adwd-tyrion-12:209–210 | Jorah in company armor: "His left greave did not match his right, his gorget was spotted with rust … a gauntlet of lobstered steel, on his left a fingerless mitt of rusted mail. The nipples on his muscled breastplate had a pair of iron rings through them. His greathelm sported a ram's horns, one of which was broken." |
| quote | ADWD | adwd-tyrion-01:29–31 | Tyrion's memory of immediately post-murder moment: "I've killed my father … in the same tone a man might use to say, 'I've stubbed my toe.'" + "You should not have climbed that ladder" — load-bearing for Varys/Tyrion relationship and Tyrion's psychological state |
| quote | ADWD | adwd-tyrion-05:235 | Tyrion sinking: "There are worse ways to die than drowning. And if truth be told, he had perished long ago, back in King's Landing." — thematic self-description, good node prose anchor |
| quote | ADWD | adwd-tyrion-12:81 | Second Sons' famous members listed in the book: "Aegor Rivers served a year with us, before he left to found the Golden Company … Aerion Targaryen, he was a Second Son. And Rodrik Stark, the Wandering Wolf" — book-citation overlay for those three characters |
| quote | ADWD | adwd-tyrion-12:283 | Tyrion's plan: "The Second Sons are on the losing side. They need to turn their cloaks again and do it now … Leave that to me." — the TWOW plan is spoken aloud; keep as node prose |
| foreshadowing | ADWD | adwd-tyrion-12:145 | "His father counted for at least that many, surely. Lord of Casterly Rock, Warden of the West, Shield of Lannisport, Hand of the King, husband, brother, father, father, father." — Tyrion counting his father's "lives" in the "nine men I've killed" answer |
| hospitality | ADWD | adwd-tyrion-01:65 | "My house is yours. Any friend of my friend across the water is a friend to Illyrio Mopatis, yes." — formal hospitality offer to Tyrion, classic guest-right register |
| hospitality | ADWD | adwd-tyrion-01:197 | Illyrio violates hospitality norms (offers possibly-poisoned mushrooms to guest): "Magister Ordello was poisoned by a mushroom not half a year ago … Why die with the taste of blood in your mouth when it could be butter and garlic?" — hostile hospitality inversion |
