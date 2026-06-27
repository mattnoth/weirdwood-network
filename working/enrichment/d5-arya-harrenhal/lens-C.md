# Lens C — Descriptive / Quote / Object Depth + Harvest — D5 Arya/Harrenhal proposal (S154)

> Lens focus: object nodes and their edges (Needle, iron-coin, dagger, bear pit); descriptive depth → `## Quotes` for
> existing nodes; maximal food harvest across the full arc; vivid physical descriptions of the cast harvested for
> node-body enrichment. YOU PROPOSE — YOU DO NOT MINT. All quotes verbatim with chapter:line.

---

## Proposed NEW nodes

### 1. `stableboy-killing` (event.death)
**Slug:** `stableboy-killing`  
**Type:** event.death  
**Body:** Arya kills an unnamed stableboy in the Red Keep stables during the Lannister coup, driving Needle upward through
his belly. This is Needle's first kill and Arya's first killing of a human being. The boy confronted her while she
retrieved Needle from a spilled chest; she struck in "a wild, hysterical strength" drawing on Jon Snow's first lesson
("stick him with the pointy end"), not Syrio's training. The act haunts her throughout the march north (she expects his
ghost in the dark corridors).

**Anchor quote:** "She stuck him with the pointy end, driving the blade upward with a wild, hysterical strength."
(agot-arya-04:169)

**Second anchor (outcome):** "When she took it out, he died." (agot-arya-04:173)

---

### 2. `death-of-weese` (event.death)
**Slug:** `death-of-weese`  
**Type:** event.death  
**Body:** Weese, understeward of the Wailing Tower at Harrenhal, is killed when his own spotted dog tears out his throat
— the second of Jaqen H'ghar's three deaths at Arya's direction. The method is indirect: Jaqen's means remain opaque
(Arya herself cannot explain how the dog turned). Weese's body is found in the ward the morning Lord Tywin departs.

**Anchor quote:** "Weese was sprawled across the cobbles, his throat a red ruin, eyes gaping sightlessly up at a bank
of grey cloud. His ugly spotted dog stood on his chest, lapping at the blood pulsing from his neck, and every so often
ripping a mouthful of flesh out of the dead man's face." (acok-arya-08:113)

---

### 3. `jaqen-gives-arya-the-iron-coin` (event.transaction / event.incident)
**Slug:** `jaqen-gives-arya-the-iron-coin`  
**Type:** event.incident  
**Body:** In the godswood of Harrenhal after the weasel-soup dungeon massacre and the fall of Harrenhal (ACOK Arya IX),
Jaqen H'ghar — having just changed his face — presses the iron coin into Arya's hand with the instructions "valar
morghulis" and explains that giving the coin to any man from Braavos will find him. This is the origin event of the
iron-coin's later power in the Braavos arc (S150). The coin is described as iron, no larger than a penny, rusted along
the rim, with worn writing on one side and a worn man's head on the other (acok-arya-10:53).

**Anchor quote (the giving):** "He lifted her hand and pressed a small coin into her palm." (acok-arya-09:327)  
**Anchor quote (the instruction):** "If the day comes when you would find me again, give that coin to any man from
Braavos, and say these words to him—valar morghulis." (acok-arya-09:339)

---

### 4. `arya-escapes-harrenhal` (event.escape / event.incident)
**Slug:** `arya-escapes-harrenhal`  
**Type:** event.incident  
**Body:** Arya, Gendry, and Hot Pie slip out of Harrenhal through the postern gate of the Tower of Ghosts in the small
hours before dawn, with three stolen horses, bread and cheese, a map, and Bolton's dagger. Arya kills the gate guard
(a Dreadfort northman) with the dagger — NOT with Needle. The iron coin is used as a decoy to draw the guard's head
down. This is the terminus of the Harrenhal cluster and the departure point for Arya's further flight toward Riverrun
(ASOS material).

**Anchor quote (the kill):** "Arya slid her dagger out and drew it across his throat, as smooth as summer silk."
(acok-arya-10:309)  
**Anchor quote (departure):** "'You killed him!' Hot Pie gasped. 'What did you think I would do?'" (acok-arya-10:314)

---

### 5. `harrenhal-bear-pit` (location.feature — sub-location of harrenhal)
**Slug:** `harrenhal-bear-pit`  
**Type:** location.feature  
**Body:** A pit within Harrenhal's middle ward, beneath the arched bridge between outer and middle wards. The Brave
Companions hang the captured bear's cage from the bridge span on their return (ACOK Arya IX); later, when Harrenhal
falls, Ser Amory Lorch is thrown naked into the pit. Women punished after the Lannister departure are stripped and
left beside it, "for the use of any man." The bear is described as "all in black, like Yoren" by Arya.

**Anchor quote:** "Rorge pulled him loose, and Shagwell kicked him down into the bear pit. The bear is all in black,
Arya thought. Like Yoren." (acok-arya-09:391–393)

---

## Proposed NEW edges

All edges are PROPOSED, not minted. Deduped against 146-edge baseline. Edge format: `source [EDGE_TYPE] target | Tier | quote + chapter:line | rationale`.

---

### Needle edges (new — needle currently has 0 outgoing)

**E1.** `needle [WIELDED_IN] stableboy-killing` | Tier 1 |
"She stuck him with the pointy end, driving the blade upward with a wild, hysterical strength." (agot-arya-04:169) |
Needle is the named instrument of this event; the only named artifact at the kill.

**E2.** `the-stableboy [KILLED_WITH] needle` | Tier 1 |
"Needle went through his leather jerkin and the white flesh of his belly and came out between his shoulder blades."
(agot-arya-04:171) | Victim→named-weapon per the KILLED_WITH convention (victim→artifact).

**E3.** `arya-stark [AGENT_IN] stableboy-killing` | Tier 1 |
"She stuck him with the pointy end." (agot-arya-04:169) | Arya is the sole agent.

**E4.** `stableboy-killing [LOCATED_AT] red-keep` | Tier 1 |
(The whole chapter is within the Red Keep stables — the kill takes place in the stable where Arya had hidden Needle.)
"She crossed in back of the wagon … as she crossed in back of the wagon, a fallen chest caught her eye." / "A stableboy
stood behind her." (agot-arya-04:149–155) | Scene is explicitly the Red Keep stables throughout agot-arya-04.

**E5.** `stableboy-killing [ENABLES] arya-flees-red-keep` [BORDERLINE — node does not yet exist; would need to be
minted as a wrap event for the underground escape] | Tier 2 |
After the kill, Arya cannot use the gates, which pushes her to find the dragon-skull cellars and the route out.
The killing is not the direct cause but removes the immediate threat and hardens her resolve. Only propose if the
broader flight is reified.

**E6.** `needle [WIELDED_IN] arya-escapes-harrenhal` | **[BORDERLINE — VERIFY]** | Tier 2 |
NOTE: The text is unambiguous that Arya kills the postern guard with Bolton's dagger, NOT Needle: "Arya slid her
dagger out and drew it across his throat." (acok-arya-10:309). Needle is NOT mentioned in the escape itself.
**DO NOT propose a Needle-WIELDED_IN edge for the escape.** Dropped. (See Dropped section.)

---

### Iron-coin origin edges (confirmed — origin is ACOK Arya IX)

**E7.** `jaqen-hghar [AGENT_IN] jaqen-gives-arya-the-iron-coin` | Tier 1 |
"He lifted her hand and pressed a small coin into her palm." (acok-arya-09:327) | Jaqen is the giver.

**E8.** `arya-stark [PARTICIPATES_IN] jaqen-gives-arya-the-iron-coin` | Tier 1 |
Same scene; arya is the recipient. (No GIFTED_TO on arya-stark — she is the beneficiary not a passive node.) |
The receiving actor in the transaction.

**E9.** `iron-coin [WIELDED_IN] jaqen-gives-arya-the-iron-coin` | Tier 1 |
"He lifted her hand and pressed a small coin into her palm." (acok-arya-09:327) | The coin is the artifact-instrument.

**E10.** `jaqen-gives-arya-the-iron-coin [ENABLES] arya-departs-for-braavos` | Tier 2 |
The coin is the mechanism Arya uses to find passage to Braavos (already wired in S150 from the ASOS/ADWD end).
This proposes the origin-end ENABLES link, completing the Harrenhal→Braavos seam. **Do NOT re-touch the downstream
Braavos arc; this edge terminates at `arya-departs-for-braavos` only.**

**E11.** `jaqen-gives-arya-the-iron-coin [LOCATED_AT] harrenhal` | Tier 1 |
The scene takes place in the Harrenhal godswood immediately after the fall-of-harrenhal. (acok-arya-09, entire chapter
is set in Harrenhal.) | Standard event-place wiring.

**E12.** `jaqen-gives-arya-the-iron-coin [SUB_BEAT_OF] fall-of-harrenhal` | Tier 2 |
The coin-giving happens immediately in the aftermath of the dungeon massacre / the Mummers seizing Harrenhal; same
chapter, same night. It is a post-action beat of the fall cluster. | Temporal contiguity.

---

### Iron-coin decoy use at the postern (escape)

**E13.** `iron-coin [WIELDED_IN] arya-escapes-harrenhal` | Tier 1 |
"Her fingers dug down beneath her tunic and came out clutching the coin Jaqen had given her. In the dark the iron
could pass for tarnished silver. She held it out… and let it slip through her fingers." (acok-arya-10:307–308) |
The coin is used as a deliberate decoy to drop the guard's guard; instrumental in the escape kill.

---

### Escape event role edges

**E14.** `arya-stark [AGENT_IN] arya-escapes-harrenhal` | Tier 1 |
Arya plans and executes the escape — steals horses, kills the guard, opens the gate. (acok-arya-10, throughout) |
Lead agent.

**E15.** `gendry [AGENT_IN] arya-escapes-harrenhal` | Tier 1 |
"Gendry was wearing oiled chainmail under his cloak, and he had his blacksmith's hammer slung across his back."
(acok-arya-10:285) / Gendry obtains the swords and accompanies the escape. | Active participant.

**E16.** `hot-pie [AGENT_IN] arya-escapes-harrenhal` | Tier 1 |
"Hot Pie's red round face peered out from under a hood. He had a sack of bread dangling from his right hand and a big
wheel of cheese under his left arm." (acok-arya-10:285) | Active participant.

**E17.** `arya-escapes-harrenhal [LOCATED_AT] harrenhal` | Tier 1 |
Scene is explicitly at Harrenhal's postern gate. (acok-arya-10, throughout) | Standard event-place.

**E18.** `arya-escapes-harrenhal [ENABLES] arya-departs-for-braavos` | Tier 2 |
The physical departure from Harrenhal is the necessary precondition for Arya's eventual road to Braavos; the escape
ENABLES the journey, though many intermediate steps intervene. [BORDERLINE — long causal chain; only propose if the
synthesis considers the seam load-bearing.] | The escape → Riverrun/BWB wandering → eventally → Braavos departure.

---

### Stableboy-killing causal wiring

**E19.** `stableboy-killing [MOTIVATES] arya-stark` | Tier 2 |
The killing is the first moment Arya recognizes herself as someone who kills, and it marks a psychological turning
point she explicitly revisits throughout the arc ("I killed a boy. If he jumped out at her she'd kill him again."
agot-arya-04:211). It shapes her capacity for lethal action in the Harrenhal chapters. | Actor-MOTIVATES-character
convention. [BORDERLINE — the text shows internal effect, not a single named decision.]

---

### Weese / death-of-weese edges

**E20.** `arya-stark [COMMANDS_IN] death-of-weese` | Tier 1 |
"Jaqen H'ghar closed his eyes again… 'A man shall attend him at his leisure.'" (acok-arya-08:85); Arya whispered
Weese's name to Jaqen, commanding the death. Same pattern as `chiswyck-dies-three-days-later` (already built). |
Parallel to the built Chiswyck hub.

**E21.** `jaqen-hghar [AGENT_IN] death-of-weese` | Tier 1 |
"Jaqen H'ghar was leaning up against the side of the Wailing Tower. When he saw her looking, he lifted a hand to his
face and laid two fingers casually against his cheek." (acok-arya-08:123) | Jaqen's silent acknowledgment of the kill;
his agent role in Chiswyck's death is already established (parallel pattern). Weese's dog was the instrument, but
Jaqen arranged the turn.

**E22.** `weese [VICTIM_IN] death-of-weese` | Tier 1 |
"Weese was sprawled across the cobbles, his throat a red ruin." (acok-arya-08:113) | Weese is the victim.

**E23.** `death-of-weese [LOCATED_AT] harrenhal` | Tier 1 |
The body is found in Harrenhal's ward. (acok-arya-08:113) | Standard.

**E24.** `death-of-weese [SUB_BEAT_OF] chiswyck-dies-three-days-later` | **[BORDERLINE — wrong parent; DROP]**
No — these are sibling events within the three-deaths thread, not parent/child. Better: both are SUB_BEATs of the
unnamed "jaqen's-three-deaths" arc, but no parent hub exists. Do not propose a bad parent.

**E25.** `arya-stark [WITNESS_IN] death-of-weese` | Tier 1 |
Arya arrives and sees the body directly: "Arya squirmed between them. Weese was sprawled across the cobbles." She
observes the scene firsthand. (acok-arya-08:112–113) | She actually SEES the result; qualifies as WITNESS_IN the
death event (she perceives the killing's aftermath directly, same scene).

---

### Harrenhal descriptive / location edges

**E26.** `harrenhal-bear-pit [PART_OF] harrenhal` | Tier 1 |
The bear pit is explicitly a feature of Harrenhal's ward. (acok-arya-09:391) | Sub-location wiring.

**E27.** `ser-amory-lorch-executed [LOCATED_AT] harrenhal-bear-pit` | Tier 1 |
"Shagwell kicked him down into the bear pit." (acok-arya-09:391) | The execution event already exists; add the more
precise location (harrenhal-bear-pit rather than just harrenhal).

---

### Bolton's dagger (the escape weapon — NOT Needle)

**E28.** `bolton-dagger [WIELDED_IN] arya-escapes-harrenhal` | Tier 1 |
"The lord's dagger… she took that too, just in case Gendry lost his courage." / "Arya slid her dagger out and drew
it across his throat." (acok-arya-10:263, acok-arya-10:309) | The escape guard is killed with Bolton's dagger; this
is the correct weapon edge, not Needle. [NOTE: `bolton-dagger` is not a current graph node — would require minting.
If the synthesis judges it too thin for its own node, this edge can be dropped and the fact folded into node-prose
on arya-escapes-harrenhal.]

**E29.** `arya-stark [OWNS] bolton-dagger` | Tier 2 [BORDERLINE] |
Arya takes the dagger from Bolton's table: "He'd left his dagger on the table as well, so she took that too."
(acok-arya-10:263) | Opportunistic OWNS at point of taking; she retains it through the escape. Only worth minting
if the dagger node is minted.

---

## Dropped / considered-but-rejected

**Needle WIELDED_IN the escape (postern guard kill):** The text is unambiguous — the escape guard is killed with
Bolton's stolen dagger, not Needle ("Arya slid her dagger out"). Needle is NOT drawn during the escape sequence.
Do not propose this edge; it would be false to the text.

**`capture-of-harrenhal` tangle:** Baseline flags this as a wiki node that conflates the AFFC Lannister re-capture
(Jaime/AFFC) with the ACOK Arya-era fall (`fall-of-harrenhal`). I confirm: `fall-of-harrenhal` is the correct hub
for the weasel-soup/Bolton takeover. Do not wire into `capture-of-harrenhal`. Flag for hygiene pass.

**Brave Companions' gear as nodes:** Vargo Hoat's goat-helm is described vividly (acok-arya-07:39-40) and Gendry's
bull-horned helm is a recurring prop (stolen by Dunsen). These are described objects but neither drives an edge
not already captured. Harvest pointer only (see Harvest table).

**Harrenhal five towers as separate location nodes:** All five towers are named (Tower of Dread / Widow's Tower /
Wailing Tower / Tower of Ghosts / Kingspyre Tower, acok-arya-07:11) and differentiated functionally, but they are
sub-features of harrenhal, not independent nodes. Harvest quotes only.

**The Tickler TORTURES villagers (acok-arya-06):** The victims of the Tickler's interrogations are unnamed villagers,
not graph nodes. Cannot be reified as VICTIM_IN edges without target nodes. The TORTURES relationship is node-prose
for the Tickler, not a mintable edge. Folded to Harvest description pointer.

**Arya WITNESS_IN the Tickler interrogations:** The LENS-SHARED rule requires the witness to *actually see* the
torture, not just be present. Arya watches and hears the torture in the storehouse (acok-arya-06), but the torture
victims are not nodes, so there is no valid WITNESS_IN target. Dropped.

**`incident-at-the-trident MOTIVATES arya-stark`:** Considered (baseline gap #9). The text in agot-arya-04 shows
Arya thinking of Mycah/Nymeria (implicitly), but the explicit causal chain from the Trident incident to Arya's
vengefulness runs through many chapters. It is node-prose for arya-stark, not a direct-quote-backed edge.
The Trident incident already exists as a hub (0-outgoing noted); adding MOTIVATES would be speculative.
Dropped for this dip.

**Jaqen TEACHES arya (the face-change moment):** "I want to do it too." / "If you would learn, you must come with
me." (acok-arya-09:317–319). `jaqen TEACHES arya-stark` is already in the baseline web. Do not re-propose.

**Weirwood / godswood of Harrenhal as a node:** Arya uses the godswood repeatedly (hiding her broomstick, practicing
water-dancing, the naming-gambit confrontation with Jaqen, the coin-giving aftermath). The godswood is a sub-location
of harrenhal; the heart tree deserves a vivid-description harvest entry but is not node-worthy on its own within this
dip. The weirwood face is described (acok-arya-09:131).

---

## Harvest

Key to columns: `kind` = food | quote | description | foreshadowing | hospitality | object  
Food entries split wide: every eating/hunger/drink moment including the grim register.

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | AGOT | agot-arya-05:11-13 | Arya hunts pigeons on Street of Flour with stick-sword; catches a fat speckled pigeon by snapping its neck |
| food | AGOT | agot-arya-05:19-27 | Arya tries to trade a pigeon for a lemon tart (3 coppers) at a pushcart; refused; stares at warm tarts (blueberry, lemon, apricot); goes hungry |
| food | AGOT | agot-arya-05:41-43 | Flea Bottom survival: pot-shops, "bowl o' brown" (barley, carrots, onions, turnips, sometimes apple, film of grease); Arya trades half a pigeon for heel of bread + bowl; tries not to think about the meat; "Once she had gotten a piece of fish" |
| food | AGOT | agot-arya-05:41 | "She feared so much pigeon was making her sick. A couple she'd eaten raw, before she found Flea Bottom." — raw pigeon hunger eating |
| food | AGOT | agot-arya-05:47 | Silver bracelet stolen; often goes to bed hungry rather than risk pot-shop stares |
| food | AGOT | agot-arya-05:79 | Pigeon falls off her belt and is gone; she has to search for another; "for a bit of bubbling brown" |
| food | ACOK | acok-arya-01:91 | Yoren gives Arya sourleaf to chew for the sting of a beating; "it'll help with the sting"; taste described as "foul" and "made her spit look like blood" |
| food | ACOK | acok-arya-02:29-35 | Inn at the crossroads: Yoren's band gets hot pork pies and baked apples; innkeeper gives round of beer on the house; Arya sips beer cautiously between spoonfuls of pie "still warm from the oven"; pepper anecdote |
| food | ACOK | acok-arya-02:31 | Band's wagons loaded with salt fish, hard bread, lard, turnips, sacks of beans and barley, wheels of yellow cheese leaving KL (acok-arya-01:23) — supplies eaten by the time they reach the Gods Eye area |
| food | ACOK | acok-arya-03:29-31 | Foraging: Koss and Kurz sent ahead as poachers; return with deer on poles or quail; boys pick blackberries along road, climb fences for apples |
| food | ACOK | acok-arya-03:31 | Arya kills a rabbit with stick; Yoren stews it with mushrooms and wild onions; Arya given a whole leg (her rabbit); shares with Gendry; each of the three in manacles gets a spoonful |
| food | ACOK | acok-arya-03:33 | Cornfield: field hands demand coin for sweet corn; Yoren pays coppers; they roast the ears in husks with long forked sticks; Arya thinks it "tasted wonderful" |
| food | ACOK | acok-arya-03:77 | Night after burnt holdfast: "Supper was a handful of wild radishes Koss found, a cup of dry beans, water from a nearby brook. The water had a funny taste to it, and Lommy told them it was the taste of bodies, rotting someplace upstream." — grim register |
| food | ACOK | acok-arya-03:79 | "Arya drank too much water, just to fill her belly with something." — hunger eating |
| food | ACOK | acok-arya-04:27 | Yoren allows cookfire at the holdfast; Gendry splits wood; Dobber tells Arya to pluck a chicken; they also have a goose and chickens from the deserted town; "When the food was ready, Arya ate a chicken leg and a bit of onion." |
| food | ACOK | acok-arya-04:85 | Hot Pie offered a bit of goose to the crying girl; she "gobbled it down and looked for more" |
| food | ACOK | acok-arya-05:37 | Post-holdfast survival: Arya breaks fast on "some acorn paste and a handful of bugs"; bugs described as "not so bad when you got used to them"; worms "worse"; Hot Pie retched beetle; Gendry and Lommy "wouldn't even try"; Gendry caught a frog / shared with Lommy; Hot Pie found blackberries, stripped bush bare; "mostly they had been living on water and acorns"; acorn paste made with rocks (Kurz's method), "tasted awful" |
| food | ACOK | acok-arya-05:81 | Lommy suggests catching and roasting crows "like chickens"; Gendry forbids fire |
| food | ACOK | acok-arya-05:245 | Lannister soldiers after the gibbet: hunting party returns with deer; gut it and build cookfire; "smell of cooking meat mingled queerly with the stench of corruption"; Arya's "empty belly roiled and she thought she might retch" — food and death smell |
| food | ACOK | acok-arya-05:247 | Squire brings meat and bread to guards at storehouse; later wine skin passed hand to hand |
| food | ACOK | acok-arya-06:11 | Harrenhal march: "stale bread and the blisters on her toes" — daily ration summary |
| food | ACOK | acok-arya-06:51 | Mountain's column brings back "a dozen pigs, a cage of chickens, a scrawny milk cow, and nine wagons of salt fish" from foraging |
| food | ACOK | acok-arya-07:11 | At Harrenhal: "there was bread every day, and barley stews with bits of carrot and turnip, and once a fortnight even a bite of meat" — Weasel's daily ration under Weese in the Wailing Tower |
| food | ACOK | acok-arya-08:92 | Weese promises a "plump crisp capon" as Arya's reward; eats almost all of it himself (giving a wing to the woman sharing his bed); Arya gets nothing; he eats "the grease running down in a shiny line through the boils at the corner of his mouth" — capon as cruelty |
| food | ACOK | acok-arya-08:99 | Lord Tywin marches day: breakfast is oatcakes; Arya "picked at her oaten cake" |
| food | ACOK | acok-arya-08:91 | Supper: "thin stew of barley, onion, and carrots, with a wedge of stale brown bread" |
| food | ACOK | acok-arya-09:13-16 | Late-night kitchen visit: Hot Pie making morning bread; Ser Amory's tart (nuts, fruit, cheese in flaky crust "still warm from the oven"); Arya filches one and eats it on the way out — "eating Ser Amory's tart made Arya feel daring" |
| food | ACOK | acok-arya-09:45-46 | Weasel-soup origin: the broth is described as "bubbling hot" in "black iron kettles hung over the flames"; "the broth was boiling hot, and the kettles were heavy"; used as a weapon — the weasel-soup massacre |
| food | ACOK | acok-arya-09:239 | Biter "grabbed a handful of half-charred rabbit right off the spit, and tore into it with his pointed teeth while honey dripped between his fingers" — vivid grim eating |
| food | ACOK | acok-arya-09:243 | Jaqen and Arya wrestle the hot broth kettle between them using padded mitts; Biter grabs two kettles "hissing in pain when the handles burned his hands" — the soup-as-weapon preparation |
| food | ACOK | acok-arya-10:13 | Tarred heads on the gatehouse; Arya must pass them every morning fetching water |
| food | ACOK | acok-arya-10:161 | Roose Bolton: "barley bread, butter, and boar" supper requested; a spit boy is turning a boar; the cook fills a kettle with "a heavy, sweet red" for hot spice wine and Hot Pie crumbles in the spices |
| food | ACOK | acok-arya-10:165-173 | Bolton's supper served with hot spice wine in a towel-wrapped flagon; Bolton reads a book then puts it in the fire; eats alone by the hearth |
| food | ACOK | acok-arya-10:285 | Hot Pie carries "a sack of bread dangling from his right hand and a big wheel of cheese under his left arm" for the escape — escape provisions |
| hospitality | ACOK | acok-arya-02:29-35 | Inn at ivy-covered crossroads: innkeeper gives Yoren's band a hot meal + round of beer "on the house" out of sentiment for a brother taken to the Wall; named the most explicit hospitality beat in the arc |
| hospitality | ACOK | acok-arya-03:33 | Field hands take coppers for corn; Yoren notes the break from the old custom: "Time was, a man in black was feasted from Dorne to Winterfell, and even high lords called it an honor to shelter him under their roofs" — hospitality's erosion under war |
| quote | AGOT | agot-arya-04:39-53 | Syrio's "true seeing" speech (cat / Sealord anecdote) — candidate `## Quotes` for syrio-forel node; "The heart lies and the head plays tricks with us, but the eyes see true. Look with your eyes. Hear with your ears. Taste with your mouth. Smell with your nose. Feel with your skin." (line 53) |
| quote | AGOT | agot-arya-04:81-82 | Syrio's last stand opens — "Arya child, we are done with dancing for the day. Best you are going now." + "The first sword of Braavos does not run." — candidate `## Quotes` for syrio-forel node |
| quote | AGOT | agot-arya-04:167-168 | Jon Snow's lesson overrides Syrio's at the kill moment: "the only lesson Arya could remember was the one Jon Snow had given her, the very first. She stuck him with the pointy end." — load-bearing for jon-snow and needle nodes |
| quote | AGOT | agot-arya-05:43 | "bowl o' brown" description: "It usually had barley in it, and chunks of carrot and onion and turnip, and sometimes even apple, with a film of grease swimming on top. Mostly she tried not to think about the meat." — Flea Bottom food color; good node-prose for arya-stark |
| quote | ACOK | acok-arya-06:62-69 | Harrenhal approach: "Arya thought they looked like some old man's gnarled, knuckly fingers groping after a passing cloud… each tower was more grotesque and misshapen than the last, lumpy and runneled and cracked." — THE key architectural quote for harrenhal node `## Quotes` |
| quote | ACOK | acok-arya-07:31 | Scale of Harrenhal: "Harrenhal covered thrice as much ground as Winterfell… its stables housed a thousand horses, its godswood covered twenty acres, its kitchens were as large as Winterfell's Great Hall, and its own great hall, grandly named the Hall of a Hundred Hearths even though it only had thirty and some…" — key node-body quote for harrenhal |
| quote | ACOK | acok-arya-07:21 | Kingspyre Tower: "Lord Tywin kept his apartments in Kingspyre Tower, still the tallest and mightiest of all, though lopsided beneath the weight of the slagged stone that made it look like some giant half-melted black candle." — quote for harrenhal node |
| quote | ACOK | acok-arya-07:11 | Five tower names: "They were called the Tower of Dread, the Widow's Tower, the Wailing Tower, the Tower of Ghosts, and Kingspyre Tower." — foundational location fact for harrenhal node |
| quote | ACOK | acok-arya-09:311-312 | Jaqen's face-change: "Jaqen passed a hand down his face from forehead to chin, and where it went he changed. His cheeks grew fuller, his eyes closer; his nose hooked, a scar appeared on his right cheek where no scar had been before. And when he shook his head, his long straight hair, half red and half white, dissolved away to reveal a cap of tight black curls." — candidate `## Quotes` for jaqen-hghar node |
| quote | ACOK | acok-arya-09:327-343 | Iron coin description and "valar morghulis" — full coin-giving dialogue; candidate `## Quotes` for iron-coin node: "A coin of great value… it is not meant for the buying of horses… If the day comes when you would find me again, give that coin to any man from Braavos, and say these words to him—valar morghulis." |
| quote | ACOK | acok-arya-10:53 | Iron coin's appearance: "a piece of iron no larger than a penny and rusted along the rim. One side had writing on it, queer words she could not read. The other showed a man's head, but so worn that all his features had rubbed off." — key description for iron-coin node |
| quote | ACOK | acok-arya-09:393 | "The bear is all in black, Arya thought. Like Yoren." — resonant line; candidate quote for arya-stark node connecting bear-pit to Yoren's death |
| quote | ACOK | acok-arya-10:213-219 | Godswood prayer scene: "Tell me what to do, you gods… You are Arya of Winterfell, daughter of the north. You told me you could be strong. You have the wolf blood in you." / "'The wolf blood.' Arya remembered now. 'I'll be as strong as Robb. I said I would.'" — candidate quote for arya-stark node; wolf-blood motif |
| quote | ACOK | acok-arya-10:293 | The ghost/escort vision: "it felt as though Syrio Forel walked beside her, and Yoren, and Jaqen H'ghar, and Jon Snow" — candidate quote for arya-stark node (her internal "pack") |
| description | AGOT | agot-arya-04:201 | Dragon skulls in Red Keep cellars: "dragons," she whispered. She slid Needle out from under her cloak. The slender blade seemed very small and the dragons very big." — candidate for a dragon-skulls or red-keep node |
| description | ACOK | acok-arya-07:37-40 | Vargo Hoat's appearance: "a man stick-thin and very tall, with a drawn emaciated face made even longer by the ropy black beard… The helm that hung from his saddle horn was black steel, fashioned in the shape of a goat's head. About his neck he wore a chain made of linked coins of many different sizes, shapes, and metals." — key description for vargo-hoat node |
| description | ACOK | acok-arya-07:82-85 | Jaqen's physical appearance on re-entry: "His garb was still ragged and filthy, but he had found time to wash and brush his hair. It streamed down across his shoulders, red and white and shiny, and Arya heard the girls giggling to each other in admiration." — candidate `## Quotes` for jaqen-hghar node |
| description | ACOK | acok-arya-07:21-22 | Weese's description: "a squat man with a fleshy carbuncle of a nose and a nest of angry red boils near one corner of his plump lips" — key description for weese node |
| description | ACOK | acok-arya-06:93 | Weese's self-description/rule: "My nose never lies. I can smell defiance, I can smell pride, I can smell disobedience. I catch a whiff of any such stinks, you'll answer for it. When I sniff you, all I want to smell is fear." — candidate quote for weese node |
| description | ACOK | acok-arya-06:23 | Tickler's described appearance: "His face was so ordinary and his garb so plain that Arya might have thought him one of the villagers before she had seen him at his work." — key description for tickler node |
| description | ACOK | acok-arya-06:25 | Tickler's interrogation formula: "Was there gold hidden in the village? Silver, gems? Was there more food? Where was Lord Beric Dondarrion?" — the fixed questions; candidate quote for tickler node |
| description | ACOK | acok-arya-09:355 | Roose Bolton's first appearance: "He had a plain face, beardless and ordinary, notable only for his queer pale eyes. Neither plump, thin, nor muscular, he wore black ringmail and a spotted pink cloak." — key description for roose-bolton node |
| description | ACOK | acok-arya-10:69-70 | Roose Bolton leeching: "Leeches clung to the inside of his arms and legs and dotted his pallid chest, long translucent things that turned a glistening pink as they fed. Bolton paid them no more mind than he did Arya." — vivid description for roose-bolton node |
| description | ACOK | acok-arya-01:21 | Jaqen, Rorge, Biter first introduced: "One had no nose, only the hole in his face where it had been cut off, and the gross fat bald one with the pointed teeth and the weeping sores on his cheeks had eyes like nothing human." — Rorge and Biter descriptions; candidate for their nodes |
| description | ACOK | acok-arya-02:81-93 | Jaqen H'ghar's first name/introduction: "slender, fine-featured, always smiling. His hair was red on one side and white on the other, all matted and filthy from cage and travel." — key description for jaqen-hghar node |
| description | ACOK | acok-arya-09:391-393 | Ser Amory thrown naked into the bear pit: "Ser Amory pleaded and sobbed and clung to the legs of his captors, until Rorge pulled him loose, and Shagwell kicked him down into the bear pit." — key quote for ser-amory-lorch-executed event; adds the bear pit as location |
| description | ACOK | acok-arya-09:47-48 | Bear: "a huge black bear rolled by, caged in the back of a wagon… The boys from the stables were tossing stones to make the bear roar and grumble… It had been hung from the arched span of the bridge that divided the outer and middle wards, suspended on heavy chains, a few feet off the ground." — description for harrenhal-bear-pit |
| foreshadowing | ACOK | acok-arya-09:339 | "Valar morghulis" — the phrase Arya will use in Braavos (S150 already built); this is its origin-moment. The coin is the seam. |
| foreshadowing | ACOK | acok-arya-10:151-152 | Arya discovers a map: "THE LANDS OF THE TRIDENT… There's Harrenhal at the top of the big lake… where's Riverrun? Then she saw. It's not so far…" — foreshadows her planned flight toward Riverrun (ASOS material) |
| foreshadowing | ACOK | acok-arya-10:213-219 | Wolf-blood / Arya breaks the broomstick: "I am a direwolf, and done with wooden teeth" — closing of the Harrenhal chapter; foreshadows water-dancing resumption in ASOS |
| object | AGOT | agot-arya-04:149-151 | Needle hidden in chest under "silks and satins and velvets," discovered as the chest spilled; retrieved by feel. The hiding place and the retrieval scene. |
| object | AGOT | agot-arya-04:169-173 | Needle's first kill: the blade goes "through his leather jerkin and the white flesh of his belly and came out between his shoulder blades"; then "his hands closed around the blade"; "When she took it out, he died." — definitive scene for needle node |
| object | ACOK | acok-arya-10:263 | Bolton's dagger: Arya takes it from the table: "He'd left his dagger on the table as well, so she took that too, just in case Gendry lost his courage." — the weapon for the escape kill |
| object | ACOK | acok-arya-10:307-309 | Iron coin used as decoy: passed for silver in the dark; Arya lets it slip through her fingers; the guard goes to a knee; she draws the dagger; "Valar morghulis" as he dies. Coin and dagger both instrumental in one action. |
| object | ACOK | acok-arya-03:21 | Gendry's horned helm: "a beautiful helm, rounded and curved, with a slit visor and two great metal bull's horns. Arya would watch him polish the metal with an oilcloth, shining it so bright you could see the flames of the cookfire reflected in the steel. Yet he never actually put it on his head." — key description for gendry node |
