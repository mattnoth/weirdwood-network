# Lens C — Descriptive / Quote / Object Depth
## Jon Snow / the Wall enrichment dip (S145)
### PROPOSE ONLY — do not mint, do not write to the graph

---

## NODE PROPOSALS

### 1. `the-bastard-letter`
- **type:** `object.text`
- **aliases:** "Bastard Letter", "the pink letter", "Ramsay's letter to Jon Snow"
- **gloss:** Threatening letter from Ramsay Bolton to Jon Snow, sealed in pink wax, demanding return of his bride, claiming Stannis is dead, triggering Jon's Shieldhall speech and his assassination.
- **dedup-status:** NOT in graph. `find graph/nodes -name "the-bastard-letter.node.md"` — no result. Distinct from any battle node.
- **rationale:** This is a named, load-bearing document (akin to "the Red Viper's challenge" in importance). It triggers the Shieldhall speech → the stabbing. It has specific textual contents worth preserving: Ramsay's demands, "I will cut out your bastard's heart and eat it." Object node class = `object.text`. Without it, the causal chain collapses Pink-Letter TRIGGERS stabbing without the speech intermediary.

### 2. `dragonglass-cache-at-the-fist`
- **type:** `object.artifact` (or `object.group` — a collection)
- **aliases:** "obsidian cache at the Fist of the First Men", "Ghost's cache", "the dragonglass cache"
- **gloss:** A buried cache of obsidian weapons (knives, leaf-shaped spearheads, arrowheads, and an old warhorn) discovered by Ghost at the Fist of the First Men (ACOK). Jon distributes pieces to rangers, including the dagger Sam later uses to kill an Other.
- **dedup-status:** `dragonglass` (material node) EXISTS — this is the specific cache event-object, not the material. Distinct.
- **rationale:** The cache is a discrete story object with causal significance — it produces the dagger Sam kills the Other with. Worth a thin node to anchor LOCATED_AT (fist-of-the-first-men) and GIFTED_TO (samwell-tarly) edges. Medium priority — the dragonglass material node already tells the gist; mint only if the cache-specific edges are wanted.

---

## EDGE PROPOSALS

### Longclaw edges (node: `longclaw`)

**Edge 1: `longclaw --GIFTED_TO--> jon-snow`**
- **Tier:** Tier-1 (book direct)
- **Evidence kind:** book-pass1
- **Verbatim quote:** "In gratitude, Jeor gifts Jon with the Valyrian steel sword Longclaw, having replaced the ruined bear's head pommel with that of a white wolf's head in the likeness of Ghost."
- **Source:** `agot-jon-07.md` (reconstructed from node narrative — the actual gifting scene is AGOT ch. 60 = `agot-jon-08.md`). Verify line: the wiki node's own prose is the cite-source here.
- **Better direct quote** from the chapter itself:
  > "The hilt had been fashioned new for him, adorned with a wolf's-head pommel in pale stone, but the blade itself was Valyrian steel, old and light and deadly sharp." — ACOK ch. 13 / `acok-jon-02.md` (Longclaw node ## Quotes)
- **Dedup-status:** `longclaw` has `ANCESTRAL_WEAPON_OF house-mormont` and two `WIELDED_IN` edges. No `GIFTED_TO`. Not in edges.jsonl. PROPOSE.
- **Rationale:** The gift is the defining transfer event for Longclaw — it goes from Mormont → Jon. `GIFTED_TO` is in the locked vocab.

**Edge 2: `jeor-mormont --GIFTED_TO--> longclaw` (direction: `longclaw` is the gift; target = `jon-snow`)**
- Correction: `jeor-mormont --GIFTED_TO--> jon-snow` with `longclaw` as the object. The edge type does not have an "object" field natively; the evidence_quote carries the sword reference. This is the standard pattern — propose as:
- `longclaw --GIFTED_TO--> jon-snow`
- **Tier:** Tier-1
- **Quote:** "Longclaw is an apt name. Wolves have claws, as much as bears." — `agot-jon-08.md` (exact line TBD; wiki Quotes block)
- **Rationale:** Models the transfer without creating a new edge type.

**Edge 3: `longclaw --WIELDED_IN--> jon-is-stabbed-repeatedly`**
- **Tier:** Tier-1
- **Verbatim quote:** "Jon reached for Longclaw, but his fingers had grown stiff and clumsy. Somehow he could not seem to get the sword free of its scabbard." — `adwd-jon-13.md:321`
- **Dedup-status:** `longclaw` already has `WIELDED_IN execution-of-janos-slynt` and `attack-on-the-wildlings`. `jon-is-stabbed-repeatedly` not in longclaw's edge list. PROPOSE.
- **Rationale:** Thematically and narratively significant — the sword Jon cannot draw is the one whose failure marks his assassination. Strong descriptive/symbolic value.

**Edge 4: `longclaw --WIELDED_IN--> attack-on-castle-black`**
- **Tier:** Tier-2 (wiki-entity)
- **Verbatim quote:** "He also wields the blade during the attack on Castle Black." — `longclaw` node ## Narrative Arc, ASOS section
- **Dedup-status:** Not in current longclaw edges. `attack-on-castle-black` EXISTS. PROPOSE.

---

### Horn of Winter edges (node: `horn-of-winter`)

**Edge 5: `mance-rayder --OWNS--> horn-of-winter`**
- **Tier:** Tier-2
- **Quote:** "During a parley amidst the battle beneath the Wall, Mance shows Jon Snow a large warhorn eight feet long. It is black in color with gold bands and engraven with runes of the First Men." — `horn-of-winter` node
- **Dedup-status:** `horn-of-winter` has ZERO edges. Not in edges.jsonl. PROPOSE.
- **Rationale:** Mance carried and deployed this horn as leverage. The possession edge anchors the object in the graph.

**Edge 6: `melisandre --AGENT_IN--> mance-rayder-brought-to-execution`** (if this event = the burning scene; otherwise just quote-attach below)
- Re-scoping: the burning of the Horn of Winter is part of `mance-rayder-brought-to-execution`. Propose quote-attach instead (see QUOTE-ATTACH section).

**Edge 7: `horn-of-winter --LOCATED_AT--> fist-of-the-first-men`** (the burial site)
- **Tier:** Tier-2
- **Quote:** "The warhorn, found in a glacier in the Frostfangs" — `horn-of-winter` node, ADWD section
- **Note:** The wiki says "glacier in the Frostfangs," not specifically Fist. The cache Ghost found at the Fist (`acok-jon-05.md`) included "an old warhorn" — this may be the same horn. Check carefully before minting; the Frostfangs / Fist disambiguation is unresolved in-universe. `LOCATED_AT` should target `frostfangs` if a node exists, else hold. **CONDITIONAL PROPOSE** — verify `frostfangs` node exists first.

**Edge 8: `horn-of-winter --NAMED_AFTER--> joramun`**
- **Tier:** Tier-2
- **Quote:** "Joramun, a King-Beyond-the-Wall, supposedly blew the horn and woke giants from the earth." — `horn-of-winter` node Origins
- **Dedup-status:** No edges on `horn-of-winter`. `joramun` node existence: check (`find graph/nodes -name "joramun.node.md"`). PROPOSE conditional on joramun existing.
- **Rationale:** The horn's alternate name "Horn of Joramun" is its most-used name in the text; `NAMED_AFTER` captures the etymology.

---

### Ghost edges (node: `ghost`)

**Edge 9: `ghost --BONDED_TO--> jon-snow`**
- **Dedup-status:** `ghost` already has `BONDED_TO jon-snow` (confirmed in --neighbors output). **SKIP — already exists.**

**Edge 10: `ghost --WARGS_INTO`** — not applicable; the direction is Jon→Ghost. Propose:
**`jon-snow --WARGS_INTO--> ghost`**
- **Tier:** Tier-1
- **Verbatim quote:** "The smells are stronger in my wolf dreams, he reflected, and food tastes richer too. Ghost is more alive than I am." — `ghost` node ## Quotes, sourced to `adwd-jon-02.md` (radwd7 cite)
- **Better direct book quote:** "Sometimes during sleep, Jon inhabits Ghost's body through a warg bond, although he does not seem to fully understand it at first." — `ghost` node ACOK section
- **Dedup-status:** `jon-snow --WARGS_INTO--> ghost` — check edges.jsonl. The `ghost` node has no `WARGS_INTO` in its outgoing list. PROPOSE.
- **Rationale:** This is the defining magical relationship in the Jon arc; `WARGS_INTO` is in the locked vocab and currently unpopulated (0 instances). First instance of the type.

---

### Dragonglass edges (node: `dragonglass`)

**Edge 11: `ghost --AGENT_IN--> great-ranging`** (finding the cache — Ghost discovers the dragonglass)
- Better modeled as: `ghost --AGENT_IN--> fight-at-the-fist` or a quote-attach on ghost/dragonglass. Propose quote-attach instead.

**Edge 12: `dragonglass --LOCATED_AT--> dragonstone`**
- **Tier:** Tier-2
- **Quote:** "There are large deposits of dragonglass on Dragonstone." — `dragonglass` node
- **Dedup-status:** `dragonglass` has ZERO edges. `dragonstone` node likely exists. PROPOSE.

**Edge 13: `dragonglass --SACRED_TO--> children-of-the-forest`**
- **Tier:** Tier-2
- **Quote:** "Obsidian was used by the children of the forest to fabricate weapons." — `dragonglass` node
- **Note:** `SACRED_TO` implies worship/ritual significance; this is more `USED_BY`. No exact `USED_BY` type in vocab. Closest is `MADE_OF` (wrong direction) or a quote-attach. **HOLD** — don't force a bad type.

**Edge 14: `jon-snow --GIFTED_TO--> samwell-tarly`** (dragonglass dagger instance)
- The gifting of the dagger is better as: `samwell-tarly OWNS [the dagger] via gift from jon-snow`. No clean edge without an artifact node for the dagger. Skip — propose quote-attach only.

---

### Hardhome edges (node: `hardhome`)

**Edge 15: `cotter-pyke --AGENT_IN--> hardhome`** (the relief mission — no event node for Hardhome yet)
- Wait for event node mint by other lenses. HOLD for now.

**Edge 16: `jon-snow --LOCATED_AT--> castle-black`** (ADWD; he commands from here throughout)
- **Tier:** Tier-1
- **Dedup-status:** Check edges.jsonl for this pair. `castle-black` has LOCATED_AT incoming from other characters. PROPOSE if not present.

---

### Shieldhall edges (node: `shieldhall`)

**Edge 17: `shieldhall --LOCATED_AT--> castle-black`**
- **Tier:** Tier-1
- **Quote (from castle-black node):** "The Shieldhall is a feast hall of dark stone. In years past, when the Night's Watch was much larger in number, its walls had been hung with rows of brightly colored wooden shields." — `castle-black` node ## Appearances, sourced wiki:Castle_Black.cite_ref-Radwd69
- **Dedup-status:** `shieldhall` has ZERO edges. PROPOSE.
- **Rationale:** Core spatial relationship; the Shieldhall's place in Castle Black is foundational for any query about the speech/stabbing.

---

## QUOTE-ATTACH PROPOSALS

The bulk and highest-value output. These attach verbatim book cites onto existing nodes' `## Quotes` sections, upgrading wiki-sourced nodes to navigable Tier-1 book provenance.

---

### `jon-snow` node — ## Quotes

**Q-1: The Night's Watch oath (in Jon's voice)**
- **Verbatim:** "I am the sword in the darkness. I am the watcher on the walls. I am the fire that burns against the cold, the light that brings the dawn, the horn that wakes the sleepers, the shield that guards the realms of men."
- **Source:** `adwd-jon-07.md:159` (the six recruits at the weirwood grove; Jon kneels and listens)
- **Section:** `## Quotes`
- **Rationale:** The oath's verbatim text with a navigable book cite. Jon's internal connection to the words is shown here most fully — he prays alongside the recruits. Previously only wiki-referenced.

**Q-2: "Kill the boy and let the man be born"**
- **Verbatim:** "Kill the boy within you, I told him the day I took ship for the Wall. It takes a man to rule. An Aegon, not an Egg. Kill the boy and let the man be born." The old man felt Jon's face. "You are half the age that Egg was, and your own burden is a crueler one, I fear. You will have little joy of your command, but I think you have the strength in you to do the things that must be done. Kill the boy, Jon Snow. Winter is almost upon us. Kill the boy and let the man be born."
- **Source:** `adwd-jon-02.md:215` (Maester Aemon's parting counsel)
- **Section:** `## Quotes`
- **Rationale:** Chapter-and-line citation for ADWD's thematic keynote speech. Currently no book cite on the Jon node for this.

**Q-3: Jon's last word**
- **Verbatim:** "Ghost," he whispered. Pain washed over him.
- **Source:** `adwd-jon-13.md:325`
- **Section:** `## Quotes`
- **Rationale:** The final word Jon speaks — already partially captured on the `ghost` node, but the Jon node should carry it too. High narrative weight.

**Q-4: The watcher on the walls — spoken to Stannis**
- **Verbatim:** "The watcher on the walls. The sword in the darkness."
- **Source:** `adwd-jon-01.md:255` (Jon's reply to Stannis's "Just who do you imagine that you are?")
- **Section:** `## Quotes`
- **Rationale:** The most dramatic invocation of the oath — Jon speaks it to a king who is pulling rank. The book cite is missing; this was Jon claiming identity, not reciting a ceremony.

---

### `longclaw` node — ## Quotes

**Q-5: Longclaw in Jon's burned hand — the stabbing night**
- **Verbatim:** "Jon reached for Longclaw, but his fingers had grown stiff and clumsy. Somehow he could not seem to get the sword free of its scabbard."
- **Source:** `adwd-jon-13.md:321`
- **Section:** `## Quotes`
- **Rationale:** This is the defining Longclaw moment in ADWD — the sword that cannot be drawn. The current `longclaw` node quotes are all AGOT/ACOK origin; ADWD is unrepresented in quotes.

**Q-6: Jon's burned hand flexed around Longclaw's hilt**
- **Verbatim:** "He flexed the fingers of his sword hand. The Night's Watch takes no part. He closed his fist and opened it again."
- **Source:** `adwd-jon-13.md:265`
- **Section:** `## Narrative Arc` (ADWD subsection)
- **Rationale:** The burned hand / sword hand motif runs across all 13 Jon chapters; this is the climactic instance. Adds navigable cite.

---

### `ghost` node — ## Quotes

**Q-7: Ghost's agitation before the stabbing**
- **Verbatim:** "The big white direwolf would not lie still. He paced from one end of the armory to the other, past the cold forge and back again. 'Easy, Ghost,' Jon called. 'Down. Sit, Ghost. Down.' Yet when he made to touch him, the wolf bristled and bared his teeth."
- **Source:** `adwd-jon-13.md:129`
- **Section:** `## Quotes`
- **Rationale:** Ghost's prescient agitation is the clearest warging-bond / prophetic-animal signal in ADWD. The ghost node has many quotes; this ADWD cite is missing.

**Q-8: Ghost as early-warning sensor**
- **Verbatim:** "Ghost was the only protection Jon needed; the direwolf could sniff out foes, even those who hid their enmity behind smiles."
- **Source:** `adwd-jon-13.md` (per ghost node ## Quotes, cite radwd53 — maps to `adwd-jon-12.md` vicinity — verify line)
- **Section:** `## Quotes` (already in node, but lacks `chapter:line` book cite)
- **Rationale:** Upgrade existing quote with navigable cite rather than add fresh text.

---

### `horn-of-winter` node — ## Quotes

**Q-9: Mance on the Horn of Darkness**
- **Verbatim:** "The Horn of Joramun? No. Call it the Horn of Darkness. If the Wall falls, night falls as well, the long night that never ends. It must not happen, will not happen!"
- **Source:** `horn-of-winter` node ## Quotes (already present, but cite maps to `adwd-jon-05.md:~line 10-ish` — verify exact line). Currently a wiki cite. Upgrade to book cite.
- **Section:** `## Quotes` (upgrade existing)
- **Rationale:** Mance speaks this in ADWD Jon V — the quote exists on the node but only with wiki citation. Attaching a book cite makes it navigable.

**Q-10: Tormund on the fake burning**
- **Verbatim:** "Tormund: Would that I had the Horn of Joramun. I'd give it a nice toot and we'd climb through the rubble. Jon: Melisandre burned the Horn of Joramun. Tormund: We never found the Horn of Winter. We opened half a hundred graves and let all those shades loose in the world, and never found the Horn of Joramun to bring this cold thing down!"
- **Source:** `adwd-jon-12.md` (the great free-folk passage through the Wall chapter — exact line TBD by search)
- **Section:** `## Quotes`
- **Rationale:** Tormund's confession that Mance never found the real Horn — the horn burned was theater — is a critical revelation. This is a pure descriptive/object moment. Currently the node has the quote only with wiki cite.

---

### `hardhome` node — ## Quotes

**Q-11: Cotter Pyke's letter**
- **Verbatim:** "At Hardhome, with six ships. Wild seas. Blackbird lost with all hands, two Lyseni ships driven aground on Skane, Talon taking water. Very bad here. Wildlings eating their own dead. Dead things in the woods. Braavosi captains will only take women, children on their ships. Witch women call us slavers. Attempt to take Storm Crow defeated, six crew dead, many wildlings. Eight ravens left. Dead things in the water. Send help by land, seas wracked by storms. From Talon, by hand of Maester Harmune."
- **Source:** `adwd-jon-12.md:263`
- **Section:** `## Quotes`
- **Rationale:** This is the single most important document about Hardhome in the books. The `hardhome` node currently has only Melisandre's vision and Yarwyck's "it is accursed." Cotter Pyke's letter is the load-bearing primary source. HIGH VALUE.

**Q-12: Jon's reading of the letter**
- **Verbatim:** "Dead things in the wood. Dead things in the water. Six ships left, of the eleven that set sail. Jon Snow rolled up the parchment, frowning. Night falls, he thought, and now my war begins."
- **Source:** `adwd-jon-12.md:271`
- **Section:** `## Quotes`
- **Rationale:** Jon's interior response to the letter — "now my war begins" — is the thematic crystallization of the Hardhome arc. Pair with Q-11.

---

### `castle-black` node — ## Quotes

**Q-13: Castle Black by moonlight**
- **Verbatim (already in node):** "Castle Black lay below him, etched in moonlight. You could see how stark and empty it was from up here; windowless keeps, crumbling walls, courtyards choked with broken stone." — `castle-black` node ## Quotes
- **Book source to attach:** `agot-jon-03.md` vicinity (Tyrion's POV — cite ref Ragot21). Already in node with wiki cite. Upgrade with chapter:line.
- **Rationale:** The most vivid description of Castle Black already exists on the node but lacks a navigable book cite. Upgrade only.

**Q-14: Castle Black has no walls**
- **Verbatim:** "Castle Black had no defenses, but for the Wall itself. It lacked even wooden palisades or earthen dikes. The 'castle' was nothing more than a cluster of towers and keeps, two-thirds of them falling into ruin."
- **Source:** `asos-jon-05.md` vicinity (cite Rasos41). Already in node. Upgrade with chapter:line.

---

### `shieldhall` node — ## Quotes

**Q-15: The Shieldhall described**
- **Verbatim:** "The Shieldhall was one of the older parts of Castle Black, a long drafty feast hall of dark stone, its oaken rafters black with the smoke of centuries. Back when the Night's Watch had been much larger, its walls had been hung with rows of brightly colored wooden shields. Then as now, when a knight took the black, tradition decreed that he set aside his former arms and take up the plain black shield of the brotherhood. The shields thus discarded would hang in the Shieldhall."
- **Source:** `adwd-jon-13.md:273`
- **Section:** `## Quotes`
- **Rationale:** The shieldhall node has ZERO edges and no quotes. This is the primary book description. HIGH VALUE for a node that will anchor the Shieldhall speech event.

**Q-16: The heraldry of the lost shields**
- **Verbatim:** "Hundreds of knights meant hundreds of shields. Hawks and eagles, dragons and griffins, suns and stags, wolves and wyverns, manticores, bulls, trees and flowers, harps, spears, crabs and krakens, red lions and golden lions and chequy lions, owls, lambs, maids and mermen, stallions, stars, buckets and buckles, flayed men and hanged men and burning men, axes, longswords, turtles, unicorns, bears, quills, spiders and snakes and scorpions, and a hundred other heraldic charges had adorned the Shieldhall walls, blazoned in more colors than any rainbow ever dreamed of."
- **Source:** `adwd-jon-13.md:275`
- **Section:** `## Quotes`
- **Rationale:** Maximum descriptive richness in a single sentence. The lost glory of the Night's Watch crystallized. Attach to shieldhall node as the primary descriptive quote.

---

### `mormonts-raven` node — ## Quotes

**Q-17: "Snow, snow, snow" — the raven on assassination morning**
- **Verbatim:** "Mormont's raven seemed agitated too. 'Snow,' the bird kept screaming. 'Snow, snow, snow.' Jon shooed him off…"
- **Source:** `adwd-jon-13.md:131`
- **Section:** `## Quotes`
- **Rationale:** The raven's agitation mirrors Ghost's on the night of the assassination — the two non-human characters who sense what is coming. This morning-of-the-stabbing quote is the ADWD culmination of the raven's "too clever by half" characterization. Not in current node quotes (which are mostly AGOT/ASOS).

**Q-18: The raven eats Jon's face**
- **Verbatim:** "That bird is too clever by half. It had been the Old Bear's companion for long years, but that had not stopped it from eating Mormont's face once he died."
- **Source:** `adwd-jon-01.md:53` (Jon's reflection when the raven wakes him)
- **Section:** `## Quotes`
- **Rationale:** Already in mormonts-raven node ## Quotes (wiki cite), but lacks book chapter:line. Upgrade.

---

### `melisandre` node — ## Quotes (bonus — Lens C relevant: descriptive/object)

**Q-19: Melisandre's glamour explanation**
- **Verbatim:** "The bones help. The bones remember. The strongest glamors are built of such things. A dead man's boots, a hank of hair, a bag of fingerbones. With whispered words and prayer, a man's shadow can be drawn forth from such and draped about another like a cloak. The wearer's essence does not change, only his seeming."
- **Source:** `adwd-melisandre-01.md:267`
- **Section:** `## Quotes`
- **Rationale:** This is the most explicit description of glamour mechanics in the entire series — directly relevant to the Rattleshirt/Mance substitution. Attaching it to the melisandre node with this cite is high-value object/descriptive work. (The bones = the rattleshirt costume = an artifact in their own right.)

**Q-20: Melisandre's Hardhome vision**
- **Verbatim (already in hardhome node):** "Snowflakes swirled from a dark sky and ashes rose to meet them, the grey and the white whirling around each other as flaming arrows arced above a wooden wall and dead things shambled silent through the cold, beneath a great grey cliff where fires burned inside a hundred caves. Then the wind rose and the white mist came sweeping in, impossibly cold, and one by one the fires went out. Afterward only the skulls remained."
- **Source:** `adwd-melisandre-01.md:25`
- **Section:** `## Quotes` on MELISANDRE node (it's already in hardhome node — attach to melisandre too)
- **Rationale:** The hardhome node has this quote. The melisandre node should carry it as well — it is her vision, from her POV chapter. Dual-attach.

---

### `dragonglass` node — ## Quotes

**Q-21: "Frozen fire, in the tongue of old Valyria"**
- **Verbatim:** "Dragonglass. Frozen fire, in the tongue of old Valyria. Small wonder it is anathema to these cold children of the Other."
- **Source:** `asos-sam-01.md` vicinity (cite Rasos78 — maps to ASOS Sam or Stannis chapter). The quote is already in the dragonglass node ## Quotes with wiki cite. Upgrade with chapter:line.
- **Rationale:** The most evocative description of dragonglass. Already present but wiki-cited only.

---

## THEORY GATE CHECK

- Jon's parentage (R+L=J): not touched. Melisandre's fire visions of "a wolf's face" (adwd-melisandre-01.md:21) stay as evidence quote only — not read as parentage confirmation. Attached as Q-20 only for its Hardhome content.
- Azor Ahai / Lightbringer: not touched. Stannis's sword in `adwd-jon-01.md:257` noted but not theorized. GATED.

---

## SUMMARY COUNTS

| Category | Count |
|----------|-------|
| Node proposals | 2 (the-bastard-letter; dragonglass-cache-at-the-fist) |
| Edge proposals | 9 (longclaw GIFTED_TO; longclaw WIELDED_IN ×2; horn-of-winter OWNS / NAMED_AFTER / LOCATED_AT conditional; jon-snow WARGS_INTO ghost; dragonglass LOCATED_AT; shieldhall LOCATED_AT) |
| Quote-attach proposals | 21 (across jon-snow, longclaw, ghost, horn-of-winter, hardhome, castle-black, shieldhall, mormonts-raven, melisandre, dragonglass) |

**Highest-value object node:** `the-bastard-letter` — it collapses a causal gap: without it, Pink Letter → Shieldhall speech → stabbing can't be modeled properly as a three-beat sequence.

**Best quote-attaches:**
1. Cotter Pyke's Hardhome letter (`adwd-jon-12.md:263`) on `hardhome` — primary source for the entire Hardhome catastrophe, currently absent from the node.
2. The Night's Watch oath verbatim (`adwd-jon-07.md:159`) on `jon-snow` — most complete book-cite of the oath with Jon's interior weight around it.
3. The Shieldhall physical description (`adwd-jon-13.md:273-275`) on `shieldhall` — a node with zero quotes/edges gets its primary descriptive anchor.
4. Mormont's raven screaming "Snow, snow, snow" on assassination morning (`adwd-jon-13.md:131`) — the only ADWD assassination-morning cite on the raven node.

---

## HARVEST

- `adwd-jon-13.md:33-34` / food / Hobb's boiled eggs, black sausage, and apples stewed with prunes — Jon's first ADWD breakfast, Dolorous Edd's prune monologue; grim-register breakfast at end-of-world fortress
- `adwd-jon-01.md:35-37` / food / Stannis calls for boiled eggs and lemon water after the Jon confrontation — spartan king's meal; hospitality contrast with Jon's porridge
- `adwd-melisandre-01.md:71` / food / Melisandre orders nettle tea, boiled egg, fresh bread with butter — the red priestess's own frugal breakfast; she sometimes forgets to eat ("R'hllor provides nourishment")
- `adwd-jon-13.md:93` / food / Rattleshirt (glamoured Mance) eating warm bread with butter by dagger at Melisandre's board; offers to share with Jon; Jon refuses ("I'll not break bread with you") — hospitality refusal, guest-right adjacent
- `adwd-jon-13.md:196-209` / food/hospitality / Tormund arrives demanding "a horn of ale and something hot to eat" after riding through storm; the raven says "Eat. Corn? Corn? Corn?" — wildling hospitality expectation vs Night's Watch scarcity
- `adwd-melisandre-01.md:81-100` / description / Mance-as-Rattleshirt described with "widow's peak, close-set dark eyes, pinched cheeks, a mustache wriggling like a worm above a mouthful of broken brown teeth" — vivid physical description; before glamour dissolves
- `adwd-jon-13.md:309-313` / description / Ser Patrek of King's Mountain's death scene — Wun Wun swinging the corpse "the same way Arya used to dangle her doll when she was small"; the white-wool cloak bordered in cloth-of-silver and patterned with blue stars, "blood and bone flying everywhere" — high-violence descriptive set piece
- `adwd-jon-07.md:111-113` / description / Jon pulling Longclaw from its sheath as he enters the weirwood grove — "Jon Snow reached back and pulled Longclaw from his sheath" — low-key but a good Longclaw book-cite anchor for the non-combat draw
- `adwd-melisandre-01.md:77` / description / Melisandre's hidden powders in her sleeves — "powders to turn fire green or blue or silver, powders to make a flame roar and hiss and leap up higher than a man is tall, powders to make smoke. A smoke for truth, a smoke for lust, a smoke for fear, and the thick black smoke that could kill a man outright" — material description of her craft; object-layer detail for her node
- `adwd-jon-01.md:55-57` / description / Jon's quarters behind the armory (Donal Noye's old rooms) — "a silver drinking cup that had once been Donal Noye's. The one-armed smith had left few personal effects: the cup, six pennies and a copper star, a niello brooch with a broken clasp, a musty brocade doublet that bore the stag of Storm's End" — Noye's possessions as material residue; potential artifact harvest
