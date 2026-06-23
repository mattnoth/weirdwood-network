# Lens 3 — Descriptive / Quote / Object Depth
## Purple Wedding enrichment dip · S135 · PROPOSE-ONLY

---

## Proposed edges

All three artifact nodes (`widows-wail`, `strangler`, `wedding-chalice`) exist with 0 outbound edges — these wire them to the cluster for the first time.

| src_slug | edge_type | tgt_slug | tier | evidence | verbatim quote | rationale |
|---|---|---|---|---|---|---|
| widows-wail | WIELDED_IN | death-of-joffrey-baratheon | 1 | asos-tyrion-08.md:265 | "Widow's Wail was not meant for slicing pies." | Margaery names the sword as Joffrey draws it to cut the pie — establishes the weapon's presence at the kill event; same chapter as the poisoning. Tier-1: book-direct. |
| widows-wail | WIELDED_IN | wedding-ceremony-at-the-great-sept-of-baelor | 1 | asos-sansa-04.md:105 | "Widow's Wail!" he cried. "Yes! It shall make many a widow, too!" He slashed again. | Joffrey names and wields the sword at the pre-wedding gift breakfast; by the ceremony it is on his belt. Tier-1: book-direct. |
| widows-wail | OWNS | joffrey-baratheon | 1 | asos-sansa-04.md:93-105 | "Lord Tywin waited until last to present the king with his own gift: a longsword. … 'Widow's Wail!' he cried." | Tywin gifts the blade to Joffrey; Joffrey names it and belts it on. Tier-1: book-direct. |
| strangler | WIELDED_IN | death-of-joffrey-baratheon | 1 | asos-sansa-05.md:43 | "No murder. He choked on his pigeon pie." Dontos chortled. "Oh, tasty tasty pie. Silver and stones, that's all it was, silver and stone and magic." | Dontos confirms the mechanism within the same event node. Tier-1: book-direct. (See also Littlefinger's full confession: asos-sansa-06.md:183-185.) |
| strangler | PART_OF | silver-hairnet-of-sansa-stark | 1 | asos-sansa-05.md:23 | "The web of spun silver hung from her fingers, the fine metal glimmering softly, the stones black in the moonlight. Black amethysts from Asshai. One of them was missing." | The missing Strangler crystal was physically embedded in the hairnet — it is a component of the artifact. (New node proposed below.) |
| wedding-chalice | WIELDED_IN | death-of-joffrey-baratheon | 1 | asos-tyrion-08.md:295 | "It's, kof, the pie, noth—kof, pie." Joff took another drink, or tried to, but all the wine came spewing back out when another spate of coughing doubled him over. His face was turning red. "I, kof, I can't, kof kof kof kof …" The chalice slipped from his hand and dark red wine went running across the dais. | The chalice carries the poison dose; it slips from Joffrey's hand at the moment he dies. Tier-1: book-direct. |
| wedding-chalice | OWNS | joffrey-baratheon | 1 | asos-sansa-04.md:81-87 | "Lord Mace Tyrell came forward to present his gift: a golden chalice three feet tall, with two ornate curved handles and seven faces glittering with gemstones. … 'Margaery and I shall drink deep at the feast, good father.' Joffrey lifted the chalice above his head." | Given to Joffrey as a wedding gift; he claims it at once. Tier-1: book-direct. |
| lives-of-four-kings | WIELDED_IN | wedding-ceremony-at-the-great-sept-of-baelor | 1 | asos-sansa-04.md:109 | "Joff brought Widow's Wail down in a savage two-handed slice, onto the book that Tyrion had given him. The heavy leather cover parted at a stroke." | Joffrey destroys the book with Widow's Wail at the morning gift-giving before the ceremony. Sub-event of the wedding cluster; attaches an object-destruction moment. Tier-1: book-direct. Note: WIELDED_IN is the closest locked verb for "object destroyed at event"; no DESTROYED_AT in vocab — flag NEEDS_VOCAB: DESTROYED_AT if the vocab ever expands. |

---

## Proposed new nodes

### `silver-hairnet-of-sansa-stark`

```yaml
name: "Silver hairnet of Sansa Stark"
type: object.artifact
slug: silver-hairnet-of-sansa-stark
aliases:
  - silver hair net
  - poisoned hairnet
  - Sansa's hairnet
confidence: tier-1
```

**Why a new node?** The Strangler node (`concept.medical`) models the poison itself. The hairnet is a distinct *physical object* — the murder weapon delivery vehicle. It is the item Dontos gives Sansa, Olenna fondles at the feast (palming a crystal), and Sansa pulls from her pocket in the godswood. The event node `sansa-receives-the-poisoned-hairnet` names this object but no artifact node captures it. Three load-bearing edges depend on it: `PART_OF strangler`, `WIELDED_IN death-of-joffrey-baratheon`, `OWNS sansa-stark` → `OWNS olenna-tyrell` (GATED, see below).

**Anchor quote (Sansa V, godswood):**
`sources/chapters/asos/asos-sansa-05.md:23`
> "The web of spun silver hung from her fingers, the fine metal glimmering softly, the stones black in the moonlight. Black amethysts from Asshai. One of them was missing."

**Description anchor (Tyrion VIII, pre-feast):**
`sources/chapters/asos/asos-tyrion-08.md:87`
> "Shae had arranged her hair artfully in a delicate silver net winking with dark purple gemstones."

**Additional proposed edges once node exists:**

| src_slug | edge_type | tgt_slug | tier | note |
|---|---|---|---|---|
| silver-hairnet-of-sansa-stark | WIELDED_IN | death-of-joffrey-baratheon | 1 | the murder weapon |
| silver-hairnet-of-sansa-stark | WIELDED_IN | sansa-receives-the-poisoned-hairnet | 1 | the object of the deception event |
| sansa-stark | OWNS | silver-hairnet-of-sansa-stark | 1 | Dontos gives it to her; she wears it |
| olenna-tyrell | WIELDED_IN | silver-hairnet-of-sansa-stark | 1 | GATED — she palms a crystal from it (Littlefinger's revelation, not in-chapter witnessed directly) |

---

## Harvest finds

All quotes are verbatim, contiguous lines from the cited file. Line numbers are 1-indexed per `cat -n` output.

---

### Widow's Wail — quotes to attach to `widows-wail ## Quotes`

**H1**
`sources/chapters/asos/asos-sansa-04.md:93-95`
kind: descriptive / physical description
> "Lord Tywin waited until last to present the king with his own gift: a longsword. Its scabbard was made of cherrywood, gold, and oiled red leather, studded with golden lions' heads. The lions had ruby eyes, she saw. The ballroom fell silent as Joffrey unsheathed the blade and thrust the sword above his head. Red and black ripples in the steel shimmered in the morning light."
node: `widows-wail` — first book-sourced physical description (complements the wiki quote already in the node)

**H2**
`sources/chapters/asos/asos-sansa-04.md:109-111`
kind: character action / cruelty
> "Joff brought Widow's Wail down in a savage two-handed slice, onto the book that Tyrion had given him. The heavy leather cover parted at a stroke. 'Sharp! I told you, I am no stranger to Valyrian steel.' It took him half a dozen further cuts to hack the thick tome apart, and the boy was breathless by the time he was done."
node: `widows-wail` + `joffrey-baratheon` — Joffrey's first act with the sword is destruction of Tyrion's gift; crystallizes his cruelty

**H3**
`sources/chapters/asos/asos-tyrion-08.md:265`
kind: key moment / restraint
> "Widow's Wail was not meant for slicing pies."
node: `widows-wail` — Margaery restraining Joffrey; the sword is present at the killing; Margaery's intervention is character texture

---

### Wedding feast texture — `purple-wedding` hub / `death-of-joffrey-baratheon`

**H4**
`sources/chapters/asos/asos-sansa-04.md:33`
kind: food / hospitality — feast scale
> "a thousand guests and seventy-seven courses, with singers and jugglers and mummers"
node: `purple-wedding` — canonical feast-scale figure; also `death-of-joffrey-baratheon` context

**H5**
`sources/chapters/asos/asos-tyrion-08.md:133-134`
kind: food / hospitality — feast opening + social commentary
> "The first dish was a creamy soup of mushrooms and buttered snails, served in gilded bowls. Tyrion had scarcely touched the breakfast, and the wine had already gone to his head, so the food was welcome. He finished quickly. One done, seventy-six to come. Seventy-seven dishes, while there are still starving children in this city, and men who would kill for a radish."
node: `purple-wedding` — opening course + Tyrion's acid social conscience; hospitality-as-power-display

**H6**
`sources/chapters/asos/asos-tyrion-08.md:153-155`
kind: food / hospitality — feast profusion
> "Thereafter dishes and diversions succeeded one another in a staggering profusion, buoyed along upon a flood of wine and ale. Hamish left them, his place taken by a smallish elderly bear who danced clumsily to pipe and drum while the wedding guests ate trout cooked in a crust of crushed almonds. Moon Boy mounted his stilts and strode around the tables in pursuit of Lord Tyrell's ludicrously fat fool Butterbumps, and the lords and ladies sampled roast herons and cheese-and-onion pies."
node: `purple-wedding` — food enumeration mid-feast; load-bearing for hospitality layer

**H7**
`sources/chapters/asos/asos-tyrion-08.md:261`
kind: food / hospitality — WO5K pie / theatrical centerpiece
> "Two yards across it was, crusty and golden brown, and they could hear squeaks and thumpings coming from inside it."
node: `purple-wedding` — the great pie; the live-dove pie is the WO5K thematic set-piece (see also proposed object node below)

**H8**
`sources/chapters/asos/asos-tyrion-08.md:279`
kind: food / hospitality — pigeon pie at the kill
> "A serving man placed a slice of hot pigeon pie in front of Tyrion and covered it with a spoon of lemon cream. The pigeons were well and truly cooked in this pie, but he found them no more appetizing than the white ones fluttering about the hall."
node: `purple-wedding` + `death-of-joffrey-baratheon` — the pigeon pie is the cover story for the poisoning ("He choked on his pigeon pie")

**H9**
`sources/chapters/asos/asos-tyrion-08.md:289-291`
kind: food / kill mechanism
> "My uncle hasn't eaten his pigeon pie." Holding the chalice one-handed, Joff jammed his other into Tyrion's pie. "It's ill luck not to eat the pie," he scolded as he filled his mouth with hot spiced pigeon. "See, it's good." Spitting out flakes of crust, he coughed and helped himself to another fistful. "Dry, though. Needs washing down." Joff took a swallow of wine and coughed again, more violently.
node: `death-of-joffrey-baratheon` — the exact sequence: pie eaten → wine drunk → coughing begins; causal mechanism quote

---

### Joffrey cruelty texture — `joffrey-baratheon` + `death-of-joffrey-baratheon`

**H10**
`sources/chapters/asos/asos-tyrion-08.md:223-225`
kind: character cruelty / dwarf jousters
> "Uncle! You'll defend the honor of my realm, won't you? You can ride the pig!" … Tyrion Lannister did not remember rising, nor climbing on his chair, but he found himself standing on the table. The hall was a torchlit blur of leering faces. He twisted his face into the most hideous mockery of a smile the Seven Kingdoms had ever seen. "Your Grace," he called, "I'll ride the pig … but only if you ride the dog!"
node: `joffrey-baratheon` + `tyrion-lannister` — the cupbearer-humiliation escalation sequence; Tyrion's counter; character depth for both

**H11**
`sources/chapters/asos/asos-tyrion-08.md:235-239`
kind: character cruelty / wine-drenching
> "Tyrion turned in his seat. Joffrey was almost upon him, red-faced and staggering, wine slopping over the rim of the great golden wedding chalice he carried in both hands. 'Your Grace,' was all he had time to say before the king upended the chalice over his head. The wine washed down over his face in a red torrent. It drenched his hair, stung his eyes, burned in his wound, ran down his cheeks, and soaked the velvet of his new doublet. 'How do you like that, Imp?' Joffrey mocked."
node: `joffrey-baratheon` + `wedding-chalice` — wine-pouring humiliation; physical description of chalice in action immediately before the kill

**H12**
`sources/chapters/asos/asos-tyrion-08.md:249-253`
kind: character cruelty / cupbearer degradation
> "I have no wine," Joffrey declared. "How can I drink a toast if I have no wine? Uncle Imp, you can serve me. Since you won't joust you'll be my cupbearer." … "It's not meant to be an honor!" Joffrey screamed. "Bend down and pick up my chalice." Tyrion did as he was bid, but as he reached for the handle Joff kicked the chalice through his legs. "Pick it up! Are you as clumsy as you are ugly?" He had to crawl under the table to find the thing.
node: `joffrey-baratheon` — the cupbearer humiliation full sequence; load-bearing Tyrion-framing context

**H13**
`sources/chapters/asos/asos-tyrion-08.md:301-305`
kind: death scene / sensory detail
> "Ser Garlan shoved Tyrion aside and began to pound Joffrey on the back. Ser Osmund Kettleblack ripped open the king's collar. A fearful high thin sound emerged from the boy's throat, the sound of a man trying to suck a river through a reed; then it stopped, and that was more terrible still. … Joffrey began to claw at his throat, his nails tearing bloody gouges in the flesh. Beneath the skin, the muscles stood out hard as stone."
node: `death-of-joffrey-baratheon` — the best single physical description of the Strangler's effect; "the sound of a man trying to suck a river through a reed" is the marquee death quote

**H14**
`sources/chapters/asos/asos-tyrion-08.md:305-307`
kind: death scene / last moment
> "Ser Meryn pried the king's mouth open to jam a spoon down his throat. As he did, the boy's eyes met Tyrion's. He has Jaime's eyes. Only he had never seen Jaime look so scared. The boy's only thirteen. Joffrey was making a dry clacking noise, trying to speak. His eyes bulged white with terror, and he lifted a hand … reaching for his uncle, or pointing …"
node: `death-of-joffrey-baratheon` + `joffrey-baratheon` — the humanizing death beat; "He has Jaime's eyes" is load-bearing for the Jaime-Joffrey biological ambiguity thread

---

### Olenna hairnet-fussing moment — `olenna-tyrell` + `silver-hairnet-of-sansa-stark`

**H15**
`sources/chapters/asos/asos-tyrion-08.md:101`
kind: key plot moment / murder mechanism
> "'You do look quite exquisite, child,' Lady Olenna Tyrell told Sansa when she tottered up to them in a cloth-of-gold gown that must have weighed more than she did. 'The wind has been at your hair, though.' The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net. 'I was very sorry to hear about your losses,' she said as she tugged and fiddled."
node: `olenna-tyrell` + `silver-hairnet-of-sansa-stark` — THIS is the palm moment. In-text it reads as grandmotherly fussing; Littlefinger's confession (asos-sansa-06.md:183) confirms she removed a crystal here. The most important in-scene evidence for `olenna-tyrell WIELDED_IN silver-hairnet-of-sansa-stark`. Attach to both nodes.

**H16**
`sources/chapters/asos/asos-sansa-06.md:183-185`
kind: confession / retrospective proof
> "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you." … "Gentle, pious, good-hearted Willas Tyrell. Be grateful you were spared, he would have bored you spitless. The old woman is not boring, though, I'll grant her that. A fearsome old harridan, and not near as frail as she pretends."
node: `olenna-tyrell` + `petyr-baelish` — Littlefinger's confession narration; the "hair net was crooked" wager is the closest the text gives to an explicit in-universe confession of Olenna's method; attach to `tyrell-plot-revealed`

---

### Hairnet / Strangler delivery chain — `sansa-stark`, `dontos-hollard`, `strangler`

**H17**
`sources/chapters/asos/asos-sansa-05.md:25-26`
kind: horror / discovery
> "A sudden terror filled her. Her heart hammered against her ribs, and for an instant she held her breath. Why am I so scared, it's only an amethyst, a black amethyst from Asshai, no more than that. It must have been loose in the setting, that's all."
node: `sansa-stark` — Sansa's moment of dawning comprehension; her interiority as the murder is realized

**H18**
`sources/chapters/asos/asos-sansa-05.md:41-43`
kind: confirmation / Dontos speech
> "Sansa: You said I must wear the hair net. The silver net with … what sort of stones are those? Dontos: Amethysts. Black amethysts from Asshai, my lady. Sansa: They're no amethysts. Are they? Are they? You lied. Dontos: Black amethysts. There was magic in them. Sansa: There was murder in them!"
node: `dontos-hollard` + `strangler` — the "There was murder in them!" line is the sharpest verbal confirmation; attach to both nodes (the strangler node's ## Quotes block already has the wiki version — this is the book-direct Tier-1 cite)

---

### Sansa's gown / hospitality observation

**H19**
`sources/chapters/asos/asos-tyrion-08.md:87`
kind: descriptive / clothing + object
> "Sansa wore a gown of silvery satin trimmed in vair, with dagged sleeves that almost touched the floor, lined in soft purple felt. Shae had arranged her hair artfully in a delicate silver net winking with dark purple gemstones. Tyrion had never seen her look more lovely, yet she wore sorrow on those long satin sleeves."
node: `sansa-stark` — the pre-feast appearance description; "she wore sorrow on those long satin sleeves" is a Tyrion-POV perception line; relevant to voice/perception layer later

---

### Shae / pigeon-pie appetite foreshadowing

**H20**
`sources/chapters/asos/asos-tyrion-08.md:91`
kind: foreshadowing / irony
> "'My lady,' said Shae wistfully. 'Couldn't I come serve at table? I so want to see the pigeons fly out of the pie.'"
node: `purple-wedding` — Shae's innocent remark about the pie gains retrospective horror; load-bearing for the dove-pie / pigeon-pie conflation that forms Joffrey's cover story ("He choked on his pigeon pie"). Harvest only — doesn't need a graph edge, but the irony is worth attaching to the hub node.

---

## Note on food nodes

Two food objects are load-bearing enough to consider artifact nodes:
1. **The great WO5K live-dove pie** — a theatrical set-piece named in the WO5K container; the doves are cut free by Widow's Wail and Ice. An `object.food` node `wedding-pie` would anchor the Widow's Wail + Ice + dove-release moment and the WO5K symbolism. Proposed but deferred — the food node type needs validation against architecture.md; flag for Matt.
2. **The pigeon pie / Arbor red wine at the kill** — the wine is delivered via `wedding-chalice` (already a node); the pigeon pie is the in-world cover story but not a distinct named artifact. Harvest-only; no new node needed.

---

## Summary

**Edges proposed:** 7 (wiring `widows-wail`, `strangler`, `wedding-chalice`, `lives-of-four-kings` to the cluster for the first time; all Tier-1 book-direct)
**New nodes proposed:** 1 (`silver-hairnet-of-sansa-stark`, `object.artifact`; murder-weapon delivery vehicle, distinct from `strangler` poison concept) + 4 dependent edges on that node
**Harvest finds:** 20 items (H1–H20) spanning death-scene sensory description, feast food/hospitality profusion, cruelty texture, the Olenna palm moment, the Strangler delivery chain, and ironic foreshadowing; bulk attaches to `death-of-joffrey-baratheon`, `joffrey-baratheon`, `widows-wail`, `silver-hairnet-of-sansa-stark`, `olenna-tyrell`, `purple-wedding`
