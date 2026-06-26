# Lens C — Descriptive / Quote / Object depth
## Theon/Reek arc enrichment dip — S149

Lens: OBJECTS, DESCRIPTIONS, QUOTES. Proposer only; does not mint.

---

## Proposed OBJECT NODES

| slug | type | gloss | book/ch | why load-bearing |
|------|------|-------|---------|-----------------|
| `sea-bitch` | artifact.vessel | Theon's personal longship, newly built by Sigrin for the ironborn invasion; name Theon coins himself; carries him on the Stony Shore raids | ACOK acok-theon-02 | Named ship, Theon's primary command vessel throughout ACOK arc; recurs by name |
| `smiler` | artifact.animal | Theon's black stallion, bought from Lord Botley; present from ACOK raids through the sack of Winterfell; burned alive in the stables during the sack | ACOK acok-theon-02 through acok-theon-06 | Named animal, load-bearing: Theon's mount for capture of Winterfell, the parley, and the final scene — its burning is the last image Theon sees before the sack engulfs him; DEDUP? check for animal nodes |
| `theons-iron-crown` | artifact.regalia | Theon's misshapen iron prince's crown, set with black diamonds and gold nuggets; made by the replacement smith after Mikken's death; described as ugly | ACOK acok-theon-05 | Recurring symbol of his failed lordship; he wears it for the parley with Ser Rodrik; the ugliness is narratively significant |
| `pink-letter` | artifact.document | Ramsay's demand letter to Jon Snow at the Wall: demands return of "his Reek" and the bride, claims Stannis defeated; written in pink ink (or pink wax) — the triggering document for the Jon-North crisis | ADWD (referenced via `pink-letter-delivered`) | The baseline notes `pink-letter-delivered` event EXISTS. **DEDUP?** — does a `pink-letter` artifact NODE exist? Needs check. Highly load-bearing across multiple arcs; distinct from the event node. |
| `ramsays-flaying-knife` | artifact.weapon | The small curved flaying knife with hooked point and razor-sharp edge that Ramsay carries matched with his falchion and long dagger; all three with yellow bone hilts | ADWD adwd-reek-03 | The primary instrument of Theon's torture and mutilation; Ramsay carries it as a constant visible threat; mentioned with precise description |
| `wolf-brooch-brans` | artifact.jewelry | Bran Stark's wolf's-head brooch, silver and jet; found by "Reek" (Ramsay) in his sack during the hunt; used to confirm the miller's boys are the right quarry; melted in the fire that burns the boys' bodies | ACOK acok-theon-04, acok-theon-05 | Load-bearing object: triggers the miller's boy deception; Theon retrieves the melted slag afterward and keeps it; a material trace of his moral nadir |
| `ramsays-falchion` | artifact.weapon | Ramsay's falchion with blade thick as a cleaver; used to hack wedding pie slices at the Ramsay-"Arya" wedding | ADWD adwd-reek-03, adwd-the-prince-of-winterfell-01 | Ramsay's signature weapon; recurs; the hacking of wedding pie is a notable scene — DEDUP? check artifact nodes |
| `stark-direwolf-cloak` | artifact.clothing | The heavy white wool cloak bordered in grey fur, emblazoned with the direwolf of House Stark, that Theon drapes over Jeyne Poole before the wedding; removed by Ramsay at the weirwood and replaced with the Bolton flayed-man cloak | ADWD adwd-the-prince-of-winterfell-01 | Load-bearing ceremonial object: the exchange of cloaks is the symbolic core of the wedding scene; the Stark cloak's removal and Bolton cloak's fastening enacts the Stark-to-Bolton identity transfer on Jeyne |
| `bolton-flayed-man-cloak` | artifact.clothing | Pink cloak spattered with red garnets like drops of blood, with the flayed man of the Dreadfort in stiff red leather on the back; fastened by Ramsay on Jeyne at the weirwood wedding | ADWD adwd-the-prince-of-winterfell-01 | Paired with Stark cloak above; the cloak-exchange IS the northern wedding ceremony's symbolic moment; Ramsay's cloak is described in precise, loaded detail |

---

## Proposed EDGES

| source | EDGE_TYPE | target | tier | book | chapter-file | line | quote | note |
|--------|-----------|--------|------|------|-------------|------|-------|------|
| `theon-greyjoy` | `OWNS` | `sea-bitch` | 1 | ACOK | acok-theon-02 | 64 | "Sea Bitch" | Theon names and owns the longship; proposes to crew and command her |
| `theon-greyjoy` | `OWNS` | `smiler` | 1 | ACOK | acok-theon-02 | 204 | "Does he have a name? / Smiler." | Theon purchased Smiler from Lord Botley; his personal mount for the whole ACOK arc |
| `theon-greyjoy` | `OWNS` | `theons-iron-crown` | 1 | ACOK | acok-theon-05 | 30 | "he donned his crown, a band of cold iron slim as a finger, set with heavy chunks of black diamond and nuggets of gold" | Theon's only-a-prince's-crown; explicitly his |
| `ramsay-snow` | `OWNS` | `ramsays-flaying-knife` | 1 | ADWD | adwd-reek-03 | 21 | "a small curved flaying knife with a hooked point and a razor-sharp edge" | Ramsay carries this at his belt at all times; all three blades matched yellow bone hilts |
| `ramsay-snow` | `WIELDS` | `ramsays-falchion` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 130 | "Ramsay hacked off slices with his falchion" | Uses it at the wedding feast to portion the pies |
| `ramsay-snow` | `OWNS` | `ramsays-falchion` | 1 | ADWD | adwd-reek-03 | 21 | "On one hip he wore a falchion, its blade as thick and heavy as a cleaver" | Ramsay's matched belt-weapons |
| `theon-greyjoy` | `OWNS` | `wolf-brooch-brans` | 1 | ACOK | acok-theon-04 | 245 | "his hand closed into a fist" [after drawing wolf's-head brooch from Reek's sack] | Theon seizes it; later retrieves the melted slag after burning the bodies |
| `bran-stark` | `OWNS` | `wolf-brooch-brans` | 1 | ACOK | acok-theon-04 | 245 | "a wolf's-head brooch, silver and jet" | Identified as Bran's; Reek used it to locate the miller's boys; DEDUP? |
| `ramsay-snow` | `GIFTED_TO` | `reek` | 1 | ADWD | adwd-reek-01 | 75 | "My lord father gave him to me as a token of his love" [Ramsay speaking of the original Reek] | Direction: giver→recipient; Roose GIFTED the original Reek to Ramsay — note this is the ORIGINAL `reek` node not theon-greyjoy |
| `roose-bolton` | `GIFTED_TO` | `reek` | 1 | ADWD | adwd-reek-01 | 93–94 | "Reek has been with me since I was a boy. My lord father gave him to me as a token of his love." | Roose→original-Reek relationship; distinct from Theon |
| `theon-greyjoy` | `FEARS` | `ramsay-snow` | 1 | ADWD | adwd-reek-01 | 15–16 | "he prayed, tearing off one of the rat's legs … the sound of the lock turning was the most terrible of all" | Tier 1; pervasive throughout ADWD chapters; Theon's terror is the dominant emotional register of all Reek chapters |
| `theon-greyjoy` | `FEARS` | `dreadfort` | 1 | ADWD | adwd-reek-01 | 81 | "he did not know how long he had been down there in the dungeons" | Imprisoned at Dreadfort; the location is inseparable from the fear; DEDUP? |
| `jeyne-poole` | `FEARS` | `ramsay-snow` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 23 | "They say he likes to hurt people." | Tier 1; confirmed by her wedding night terror and subsequent broken state in adwd-theon-01 |
| `theon-greyjoy` | `MOURNS` | `robb-stark` | 1 | ADWD | adwd-theon-01 | 188 | "Robb who had been more a brother to Theon than any son born of Balon Greyjoy's loins. Murdered at the Red Wedding, butchered by the Freys. I should have been with him. Where was I? I should have died with him." | Tier 1; explicit grief; one of Theon's rare moments of unguarded feeling |
| `theon-greyjoy` | `RESENTS` | `balon-greyjoy` | 1 | ACOK | acok-theon-02 | 109–111 | "He had not needed to be told that Black Wind was Asha's longship … I've had them to feast every night, while he waited for the last stragglers" | Tier 1; Theon's bitterness at being given 8 ships and a raiding assignment rather than a real command runs through ACOK I–III |
| `theon-greyjoy` | `RESENTS` | `asha-greyjoy` | 1 | ACOK | acok-theon-05 | 39 | "Asha. It was her doing. My own sweet sister, may the Others bugger her with a sword." | Tier 1; explicit resentment of Asha abandoning him at Winterfell |
| `ramsay-snow` | `OWNS` | `stark-direwolf-cloak` | 2 | ADWD | adwd-the-prince-of-winterfell-01 | 79 | "Ramsay undid the cloak that Theon had slipped about his bride's shoulders moments before … In its place he fastened a pink cloak" | Tier 2; Ramsay removes the Stark cloak and replaces it — he effectively claims/controls both cloaks in this ceremony |
| `ramsay-snow` | `GIFTED_TO` | `jeyne-poole` | 1 | ADWD | adwd-the-prince-of-winterfell-01 | 79 | "In its place he fastened a pink cloak, spattered with red garnets like those upon his doublet" | The Bolton cloak is placed on Jeyne by Ramsay; direction giver→recipient |
| `theon-greyjoy` | `PERCEIVED_AS` | `ramsay-snow` | 1 | ADWD | adwd-reek-02 | 25 | "'You will pretend to be a prince,' Lord Ramsay told him last night … 'You're Reek. You'll always be Reek, no matter how sweet you smell.'" | Ramsay perceives/defines Theon as Reek permanently; the core of the identity destruction |
| `theon-greyjoy` | `AFFLICTED_BY` | `capture-of-winterfell` | 2 | ADWD | adwd-reek-01 through adwd-theon-01 | multiple | (see descriptive depth notes) | Tier 2; Theon's entire ADWD arc is the downstream consequence of his own ACOK action; the irony is load-bearing |
| `kyra` | `PRISONER_OF` | `ramsay-snow` | 1 | ADWD | adwd-reek-01 | 63–68 | "That time it had been Kyra with the keys … All night they ran through the darkling wood … Within the hour, they were taken." | Tier 1; Kyra imprisoned at Dreadfort alongside Theon; used as bait for an escape attempt; DEDUP? kyra node exists per baseline |
| `ramsay-snow` | `KILLS` | `kyra` | 1 | ADWD | adwd-reek-01 | 65–67 | "One dog knocked him to the ground, and a second bit Kyra on the leg as she scrambled up a hillside … 'You must be punished.'" | Tier 1 (strongly implied; Kyra is hunted and "punished" — the dogs' names named-after-hunted-girls convention confirmed by adwd-reek-03:65); Ben Bones confirms the naming convention explicitly |
| `ramsay-snow` | `TORTURES` | `theon-greyjoy` | 1 | ADWD | adwd-reek-01 | 115–119 | "He preferred to flay it and let the exposed flesh dry and crack and fester … 'screaming, please, no more, no more, stop it hurting, cut it off,' and Lord Ramsay would oblige. It was a game they played." | Core torture edge; the mechanics of the flaying game described explicitly |
| `theon-greyjoy` | `PRISONER_OF` | `ramsay-snow` | 1 | ADWD | adwd-reek-01 | 11–25 | "Down here in the dark it was hard to tell" [the opening dungeon scene] | Tier 1; Theon imprisoned at Dreadfort throughout; this is the foundational captivity edge |
| `theon-greyjoy` | `IMPRISONED_AT` | `dreadfort` | 1 | ADWD | adwd-reek-01 | 11–25 | (dungeon scene; last cell on the left) | Tier 1 |
| `ramsay-snow` | `IMPERSONATES` | `reek` | 1 | ACOK | acok-theon-06 | 247 | "'I had to pull him off her and shove my clothes into his hands—calfskin boots and velvet doublet, silver-chased swordbelt, even my sable cloak … By the time they put that arrow through his back, I'd smeared myself with the girl's filth and dressed in his rags.'" | First-use IMPERSONATES per baseline; the exact passage where Ramsay explains the switch to Theon; Tier 1 |
| `theon-greyjoy` | `RESCUES` | `jeyne-poole` | 1 | ADWD | adwd-theon-01 | 229–289 | "Theon grabbed Jeyne about the waist and jumped." | Tier 1; the climactic action; Theon physically rescues Jeyne during the escape — the jump from the battlements |
| `mance-rayder` | `RESCUES` | `jeyne-poole` | 1 | ADWD | adwd-theon-01 | 29–30 | "Abel's word … Strong as oak … No matter what, my prince." | Tier 2; Abel/Mance's plan enables the rescue; but the physical act is Theon's; Mance planned it |

---

## Quote attachments

High-value verbatim quotes that belong on existing nodes' `## Quotes` blocks.

| target_node_slug | verbatim quote | book | chapter-file | line | what it shows |
|-----------------|---------------|------|-------------|------|---------------|
| `theon-greyjoy` | "My name is Reek. It rhymes with leek." | ADWD | adwd-reek-01 | 53 | The core identity-destruction formula; first full iteration |
| `theon-greyjoy` | "Reek, Reek, it rhymes with meek." | ADWD | adwd-reek-01 | 77 | Second variation; the mantra as survival mechanism |
| `theon-greyjoy` | "Reek, Reek, it rhymes with freak." | ADWD | adwd-reek-03 | 311 | Third variation; in Roose's presence, the name becoming a plea |
| `theon-greyjoy` | "I am a Greyjoy, and I mean to be my father's heir." | ACOK | acok-theon-03 | 119 | Theon's self-definition at the height of his ambition; contrasts with Reek degradation |
| `theon-greyjoy` | "The noose I wore was not made of hempen rope, that's true enough, but I felt it all the same. And it chafed, Ser Rodrik. It chafed me raw." | ACOK | acok-theon-06 | 131 | Self-awareness of his hostage condition; spoken to Rodrik during the parley; load-bearing for his psychology |
| `theon-greyjoy` | "Theon. My name is Theon." [internal as he answers the gate guards] "Theon Greyjoy. I … I have brought some women for you." | ADWD | adwd-theon-01 | 265 | The identity-reclaim moment: he says his name instead of "Reek" for the first time; the name-break |
| `theon-greyjoy` | "A sword, that's all I ask. Let me die as Theon, not as Reek. … I was ironborn. A son … a son of Pyke, of the islands." | ADWD | adwd-a-ghost-in-winterfell-01 | 243 | Prayer at the heart tree; the full reclaim wish before the weirwood; emotionally peaks before the escape |
| `theon-greyjoy` | "Please." He fell to his knees. "A sword, that's all I ask. Let me die as Theon, not as Reek." | ADWD | adwd-a-ghost-in-winterfell-01 | 243 | (same quote, note: the surrounding "Bran … they know my name" context) |
| `theon-greyjoy` | "Robb who had been more a brother to Theon than any son born of Balon Greyjoy's loins. Murdered at the Red Wedding, butchered by the Freys. I should have been with him. Where was I? I should have died with him." | ADWD | adwd-theon-01 | 187–188 | Grief for Robb; the clearest expression of genuine brotherly feeling Theon ever articulates |
| `theon-greyjoy` | "The world is gone … Only Winterfell remained." | ADWD | adwd-a-ghost-in-winterfell-01 | 139 | Theon's psychological enclosure; Winterfell-as-prison paradox |
| `godswood-of-winterfell` | "Theon," they seemed to whisper, "Theon." / The old gods, he thought. They know me. They know my name. | ADWD | adwd-a-ghost-in-winterfell-01 | 241–242 | The weirwood calling his true name; supernatural identity recognition; belongs on the godswood node |
| `godswood-of-winterfell` | "It was warmer in the godswood, strange to say. … inside the godswood, the ground remained unfrozen, and steam rose off the hot pools, as warm as baby's breath." | ADWD | adwd-the-prince-of-winterfell-01 | 49 | Distinctive physical description of the godswood in winter; contrasted with the frozen ruin of Winterfell |
| `winterfell` | "All the color had been leached from Winterfell until only grey and white remained. The Stark colors." | ADWD | adwd-the-prince-of-winterfell-01 | 97 | Symbolic description of ruined Winterfell; ironic Stark-color survival through destruction |
| `winterfell` | "This was not the castle he remembered from the summer of his youth. This place was scarred and broken, more ruin than redoubt, a haunt of crows and corpses." | ADWD | adwd-the-prince-of-winterfell-01 | 95 | POV description of ruined Winterfell; Theon as the source of the destruction observing it |
| `ramsay-snow` | "He preferred to flay it and let the exposed flesh dry and crack and fester. When he laid the edge of the blade against the swollen throat … the skin split open in a gout of black blood and yellow pus." [Ralf Kenning's mercy-kill with Ramsay's borrowed blade] | ADWD | adwd-reek-02 | 113 | Clinical description of Bolton flaying technique as Theon has absorbed it; also the only time Theon uses a blade in ADWD |
| `ramsay-snow` | "Reek has been with me since I was a boy. My lord father gave him to me as a token of his love." | ADWD | adwd-reek-01 | 93 | Ramsay presenting the original Reek to his guests; the origin-link between Ramsay and cruelty as paternal gift |
| `ramsay-snow` | "You're Reek. You'll always be Reek, no matter how sweet you smell. Your nose may lie to you. Remember your name. Remember who you are." | ADWD | adwd-reek-02 | 25 | Ramsay's explicit identity-destruction speech before the Moat Cailin mission |
| `reek` | "Was it Ramsay who corrupted Reek, or Reek Ramsay?" | ADWD | adwd-reek-03 | 211 | Roose Bolton's question about the original Reek-Ramsay relationship; the chicken-and-egg of their shared cruelty |
| `roose-bolton` | "A peaceful land, a quiet people. That has always been my rule." | ADWD | adwd-reek-03 | 225–226 | Roose's self-description; his signature phrase; belongs on roose-bolton node |
| `roose-bolton` | "The north. The Starks were done and doomed the night that you took Winterfell." | ADWD | adwd-reek-03 | 283 | Roose to Theon; the clearest statement of what Theon's ACOK action achieved for Bolton |
| `capture-of-winterfell` | "I took this castle with fewer than thirty men, a feat to sing of." | ACOK | acok-theon-04 | 23 | Theon's own assessment of the capture; Tier 1; the pride-before-fall inflection |
| `sack-of-winterfell` | "The last thing Theon Greyjoy saw was Smiler, kicking free of the burning stables with his mane ablaze, screaming, rearing …" | ACOK | acok-theon-06 | 263 | Final image of the ACOK arc; closing of the chapter on Theon's consciousness; belongs on the sack event or smiler artifact |
| `theon-greyjoy` | "Not my tongue, though. He will never take my tongue. He likes to hear me plead with him to spare me from the pain. He likes to make me say it." | ADWD | adwd-reek-03 | 57 | Theon's understanding of Ramsay's psychological game; insight into the torture dynamics |
| `theon-greyjoy` | "I have done terrible things … betrayed my own, turned my cloak, ordered the death of men who trusted me … but I am no kinslayer." | ADWD | adwd-theon-01 | 125 | Theon's moral self-inventory; the distinction between his guilt and the one accusation he rejects |
| `jeyne-poole` | "I'll do what he wants … whatever he wants … with him or … or with the dog or … please … he doesn't need to cut my feet off, I won't try to run away, not ever, I'll give him sons, I swear it, I swear it …" | ADWD | adwd-theon-01 | 217 | Jeyne's broken psychological state; the most explicit articulation of what Ramsay has done to her |
| `wedding-of-ramsay-bolton-and-arya-stark` | "Ramsay undid the cloak that Theon had slipped about his bride's shoulders moments before, the heavy white wool cloak bordered in grey fur, emblazoned with the direwolf of House Stark. In its place he fastened a pink cloak, spattered with red garnets like those upon his doublet. On its back was the flayed man of the Dreadfort done in stiff red leather, grim and grisly." | ADWD | adwd-the-prince-of-winterfell-01 | 79 | The cloak exchange; the symbolic heart of the Bolton-Stark transfer |
| `theon-greyjoy` | "He was ironborn. A son of Pyke, of the islands." | ADWD | adwd-a-ghost-in-winterfell-01 | 137 | Internal reclaim; the identity flash that stops him from stabbing Rowan |

---

## Descriptive depth (node-body / ## Quotes material — not edges)

These are physical-condition and setting descriptions that should inform node bodies or Quotes sections rather than edges. Flag for the synthesizer.

**Theon's physical condition after Dreadfort (ADWD Reek I–III):**
- White hair, much fallen out, stiff and dry as straw (adwd-reek-02:49)
- Hollow belly, swollen from starvation; aches preventing sleep (adwd-reek-01:17)
- Missing fingers: two off left hand, pinky off right (adwd-reek-01:119); later confirmed as three off left, one off right (adwd-a-ghost-in-winterfell-01:171)
- Missing toes: little toe off right, three from left (adwd-reek-01:119); "missing toes on his left foot had left him with a crabbed, awkward gait, comical to look upon" (adwd-the-prince-of-winterfell-01:121)
- Broken teeth: "picking small bones from the holes in his gums where teeth had been yanked out" (adwd-reek-01:19); confirmed "broken teeth" making eating an agony (adwd-the-prince-of-winterfell-01:137; adwd-a-ghost-in-winterfell-01:107)
- Skin hanging loosely on bones (adwd-reek-03:193); flesh described as loose, grey, and twitching
- Gloves stuffed with wool to hide missing fingers; wearing them even indoors (adwd-reek-02:51)
- Chains and fetters in Barrowton; one foot-chain a foot long, shortening his stride to a shuffle (adwd-reek-03:11)
- Wears Ramsay's cast-off rags and refuses bath/new clothes out of conditioned terror (adwd-reek-03:265–278)

**Ramsay's physical appearance (adwd-reek-01:91–92):**
- Big-boned, slope-shouldered; fleshy; will run to fat in later life
- Skin pink and blotchy; nose broad; mouth small; hair long, dark, dry
- Wide meaty lips; eyes "ghost grey," nearly colorless, like chips of dirty ice
- Garnet eardrop in right ear cut as a blood drop
- Always wet-lipped when smiling

**Winterfell in ruin (adwd-the-prince-of-winterfell-01:95–96):**
- Roofless towers and collapsed keeps; blackened beams and bones under snow
- Glass Gardens dead and black and frozen, panes shattered
- Icicles long as lances from battlements
- Dead men hanging frozen in hempen ropes around the yard
- Great Hall's roof new-made, raw pale timbers replacing centuries-old smoke-blackened ones
- Tents filling every court; thousands crowded in cellar vaults

**Jeyne Poole's appearance/condition (adwd-the-prince-of-winterfell-01, adwd-theon-01):**
- Small, pale; small pointed breasts; narrow girlish hips; legs skinny as a bird's
- Spider-web of faint thin lines across her back (whip scars) (adwd-the-prince-of-winterfell-01:207)
- Teeth marks on breasts from the wedding night (adwd-theon-01:238)
- Huddled naked under wolfskins, trembling, in darkest corner (adwd-theon-01:199)

**Dreadfort great hall (adwd-reek-01:85–86):**
- Skeletal human hands jutting from walls, grasping torches
- High vaulted ceiling lost in shadow; wooden rafters black from smoke
- Heavy with smells of wine, ale, roasted meat

---

## HARVEST

One-line pointers for food, descriptions, songs, foreshadowing, and other notable finds encountered during this pass. Format: `chapter:line / kind / note`

**FOOD — grim register (Reek/Theon imprisonment)**
- adwd-reek-01:11–19 / food / Theon eating a live rat in Dreadfort dungeon; belly swollen hollow; "warm blood running over his lips"; the sweetness he weeps over; reference to Lady Hornwood eating her own fingers
- adwd-reek-01:138–139 / food / Ramsay's promise of "nice soft porridge … pease pie laced with bacon" to lure Theon from the dungeon; the tender cruelty of comfort food as manipulation
- adwd-reek-02:203 / food / Theon's reward after Moat Cailin: half a chicken, had to fight the dogs for it; "it was the best meal he'd had since Winterfell"; dark wine until he vomited
- adwd-reek-03:61 / food / Barrowton feast on Ramsay's return from the hunt: ox slaughtered; roasts, ribs, barley bread, mash of carrots and pease, prodigious quantities of ale
- adwd-reek-03:51 / food / Ramsay slew an old man on the road for calling him "Lord Snow"; the goat kids were roasted; the old man's head thrown at Theon as a "gift"
- adwd-a-ghost-in-winterfell-01:15–16 / food / garrison breakfast: stale bread fried in bacon grease; lords ate the bacon, common men got the bread; blood sausage, leeks, brown bread at midday
- adwd-a-ghost-in-winterfell-01:47 / food / garrison supper: pease porridge and yesterday's bread; above the salt, lords and knights eating ham; muttering amongst common men
- adwd-a-ghost-in-winterfell-01:105–107 / food / horse slaughter after stable collapse: great slabs of fresh horsemeat charred outside and bloody red within; roast onions and neeps; common soldiers eating as well as lords for once; Theon cannot chew — mashes neeps and onions with flat of dagger, sucks on horsemeat pieces, spits them out
- adwd-theon-01:17–18 / food / Theon's breakfast day of escape: tankard of dark ale, cloudy with yeast, "thick enough to chew on"; Abel's table eating stale brown bread fried in bacon grease

**FOOD — wedding feast (adwd-the-prince-of-winterfell-01:129–131)**
- adwd-the-prince-of-winterfell-01:129 / food / Full Winterfell wedding feast menu deserves complete capture: "cod cakes and winter squash, hills of neeps and great round wheels of cheese, on smoking slabs of mutton and beef ribs charred almost black, and lastly on three great wedding pies, as wide across as wagon wheels, their flaky crusts stuffed to bursting with carrots, onions, turnips, parsnips, mushrooms, and chunks of seasoned pork swimming in a savory brown gravy" — wines black stout, yellow beer, red, gold, purple (Arbor)
- adwd-the-prince-of-winterfell-01:130 / food / Manderly's famous six portions of wedding pie (two from each of three pies); his "best pie you ever tasted, my lords" declaration; Fat Walda manages three slices; Ramsay eats heartily; the bride stares at her portion untouched — load-bearing hospitality/foreshadowing nexus
- adwd-the-prince-of-winterfell-01:139–140 / food/hospitality / Lady Dustin noting Manderly "almost dancing" serving food; "drowning his fears"; "He even serves them pie" — the "pork" pie foreshadowing; Manderly request for "a song about the Rat Cook" is a direct point-at-what-just-happened; HIGH VALUE HARVEST

**FOOD — Barrowton / Stout feast (adwd-reek-03:61)**
- adwd-reek-03:61 / food / Harwood Stout forced to host Ramsay's feast despite exhausted winter stores; cook's complaint about being "fucked when the snows come" is overheard by Theon; hospitality-under-duress

**FOOD — ACOK ironborn**
- acok-theon-02:365 / food / Pyke feast: "a succession of fish stews, black bread, and spiceless goat. The tastiest thing Theon found to eat was an onion pie."
- acok-theon-03:83 / food / Dagmer's Foamdrinker cabin: "horn of sour ale" offered; Theon declines
- acok-theon-06:11–13 / food / Theon before the sack: "platter of oakcakes, honey, and blood sausage" for breakfast; he can't eat it, knocks it aside

**SONGS mentioned in chapters:**
- acok-theon-03:67 / song / Dagmer Cleftjaw's love of reaving songs; unnamed "song" made about the axe that cracked Dagmer's jaw; the old warrior's fondness for glory-songs; Theon exploits this
- acok-theon-05:141 / song / Theon's dream of Ned Stark's feast with King Robert: "the hall rang with music and laughter"; then music turns discordant as the hall fills with the dead — the feast-of-the-dead dream; foreshadowing of his haunted state
- adwd-the-prince-of-winterfell-01:82 / song / Abel (Mance) sings "Two Hearts That Beat as One" at the wedding ceremony exit; his two women harmonize
- adwd-the-prince-of-winterfell-01:112 / song / Abel sings "Fair Maids of Summer" in the feast hall; then called for "The Night That Ended" and "Danny Flint" by Manderly; Manderly calls for "The Rat Cook" — each song request is a pointed commentary
- adwd-a-ghost-in-winterfell-01:109 / song / Abel sings "Iron Lances," then "The Winter Maid," then "The Queen Took Off Her Sandal, the King Took Off His Crown," and "The Bear and the Maiden Fair" to soothe the garrison; Freys join singing; noise frightens horses, singing stops
- adwd-theon-01:87 / song / Abel sings a "sad, soft song" Theon doesn't recognize while the Frey-Manderly fight is being put down; the bard as counterpoint to violence

**DESCRIPTIONS:**
- acok-theon-01:291–292 / description / Lord Balon's physical appearance: "thin as if the gods had boiled every spare ounce of flesh … Bone thin and bone hard … hair turned grey of a winter sea, flecked with whitecaps, unbound past the small of the back" — the same gauntness that Theon will later embody
- acok-theon-01:131–132 / description / Aeron Greyjoy/Damphair: tall, thin, fierce black eyes, beak of a nose, mottled robes of green/grey/blue, waterskin under arm, ropes of dried seaweed braided through waist-long black hair and untrimmed beard
- acok-theon-02:65 / description / Sea Bitch / Theon's longship: "lean black hull a hundred feet long, a single tall mast, fifty long oars, deck enough for a hundred men … great iron ram in the shape of an arrowhead" — still smells of pitch and resin when new
- acok-theon-03:67 / description / Dagmer Cleftjaw's scar: "under a snowy white mane of hair … the most gut-churning scar Theon had ever seen … shattered his front teeth, and left him four lips where other men had but two … a shiny seam of puckered, twisted flesh divided his face like a crevasse through a snowfield"
- acok-theon-06:221–222 / description / Ramsay's first appearance to Theon in person (as Red Helm): "his rounded helm gleamed a sullen red, and a pale pink cloak streamed from his shoulders … helm and gorget were wrought in the shape of a man's face and shoulders, skinless and bloody, mouth open in a silent howl of anguish" — his battle armor; the flayed-man visor
- adwd-reek-03:287–288 / description / Barrow Hall banners described in full: "the flayed man of the Dreadfort, the battle-axe of Cerwyn, Tallhart's pines, the merman of Manderly, old Lord Locke's crossed keys, the Umber giant and the stony hand of Flint, the Hornwood moose … chevrony russet and gold, for Slate, a grey field within a double tressure white … four horseheads … one grey, one black, one gold, one brown" — useful for house-banner reference
- adwd-the-prince-of-winterfell-01:13 / description / Jeyne Poole in bridal dress: "white lambswool trimmed with lace. Her sleeves and bodice were sewn with freshwater pearls, and on her feet were white doeskin slippers—pretty, but not warm. Her face was pale, bloodless. A face carved of ice"
- adwd-the-prince-of-winterfell-01:51 / description / Theon at the wedding: "black and gold, his cloak pinned to his shoulder by a crude iron kraken … under the hood, his hair was white and thin, and his flesh had an old man's greyish undertone"
- adwd-reek-03:89 / description / Roose Bolton's appearance: "face was clean-shaved, smooth-skinned, ordinary, not handsome but not quite plain … bore no scars … unwrinkled … lips so thin that when he pressed them together they seemed to vanish altogether. There was an agelessness about him, a stillness; on Roose Bolton's face, rage and joy looked much the same. His eyes are ice."

**FORESHADOWING:**
- acok-theon-04:26–27 / foreshadowing / Theon's first premonition when the wolves go silent: "He had grown so used to the howling of the direwolves that he scarcely heard it anymore … but some part of him, some hunter's instinct, heard its absence" — the hunter becoming the hunted
- acok-theon-05:137–141 / foreshadowing / Theon's feast-of-the-dead dream: Robert with guts spilling, headless Ned, all the dead of Winterfell including "a slim sad girl who wore a crown of pale blue roses and a white gown spattered with gore" (Lyanna) — remarkable death-catalogue dream; Robb with Grey Wind both bleeding from half a hundred wounds at the door — ADWD prophetic
- acok-theon-06:91 / foreshadowing / "He could sense the boys watching from the empty sockets where their eyes had been" — the tarred miller's boy heads; haunting Theon even before he enters parley
- adwd-the-prince-of-winterfell-01:63 / foreshadowing / "The ravens were the thickest here … muttering to one another in the murderers' secret tongue. / 'Who comes?'" — ravens around the heart tree as witnesses; the weirwood's complicity; connects to the greenseer thread
- adwd-the-prince-of-winterfell-01:141 / foreshadowing / Manderly calling for "a song about the Rat Cook" immediately after the wedding pie is served — explicit signal of what the pie contains; the Rat Cook who served a king the flesh of the king's son; HIGH VALUE for Manderly-pie foreshadowing node if one exists or is proposed
- adwd-a-ghost-in-winterfell-01:241–245 / foreshadowing / The weirwood whispers "Theon" then "Bran" as a leaf falls "five-fingered, like a bloody hand" into the pool; Theon sees Bran's face in the tree — the greenseer/Bran thread present even in the Theon arc
- adwd-theon-01:213–215 / foreshadowing / The warhorn and drums outside; Stannis not yet seen; "Stannis is our only hope, if we can reach him" — the leap will deliver them to Stannis's forces; the pink-letter-delivered event connects

**HOSPITALITY / VIOLATION:**
- acok-theon-03:58–59 / hospitality / Theon sacks the Stony Shore fishing village: "men had been put to the sword … wives and daughters had been claimed for salt wives, those young enough and fair. The crones and the ugly ones had simply been raped and killed, or taken for thralls" — ironborn hospitality violation of coastal villages
- acok-theon-04:45 / hospitality / Theon references throwing Chayle (the septon) down a well as an offering to the Drowned God: "I told them before they threw him down the well, 'you and your gods have no place here now'" — violation of Winterfell's religious hospitality
- acok-theon-06:253–254 / hospitality / Ramsay promises the ironborn garrison at Moat Cailin safe conduct and slaughters them: 63 stakes, one with the unbroken parchment still sealed between his teeth — pure violation of terms, noted in adwd-reek-02
- adwd-the-prince-of-winterfell-01:99 / hospitality / Bolton hangs the squatters he used to rebuild Winterfell "true to his word, he showed them mercy and did not flay a one" — black hospitality irony; they built the hall then were hanged in it
- adwd-the-prince-of-winterfell-01:129 / hospitality / The Winterfell wedding feast as whole-cloth violation of guest right given what Ramsay does to the bride that night; cross-reference with Manderly's Rat Cook reference as explicit invocation of guest-right violation mythology

**QUOTES NOT ATTACHED ABOVE (load-bearing)**
- acok-theon-01:363 / quote / Balon's "a man may own what he pays the iron price for" — burning Robb's letter on the brazier; the founding declaration of Greyjoy philosophy that drives the whole invasion
- acok-theon-05:155–156 / quote / Theon on the miller's boys: "The miller's boys had been of an age with Bran and Rickon, alike in size and coloring, and once Reek had flayed the skin from their faces and dipped their heads in tar, it was easy to see familiar features in those misshapen lumps of rotting flesh. People were such fools. If we'd said they were rams' heads, they would have seen horns." — the moral horror at full clarity
- acok-theon-06:127 / quote / Theon to Rodrik: "It was a dish I tasted myself, or have you forgotten? I was ten when I was taken from my father's house … The noose I wore was not made of hempen rope …" — the hostage-as-noose parallel; his most self-aware ACOK speech
- adwd-reek-03:283 / quote / Roose to Theon: "The north. The Starks were done and doomed the night that you took Winterfell. All this is only squabbling over spoils." — Roose's cold strategic gratitude; load-bearing for `capture-of-winterfell` and Bolton motives
- adwd-reek-01:115 / quote / "It was the sort of pain that drove men mad, and it could not be endured for long. Soon or late the victim would scream, 'Please, no more, no more, stop it hurting, cut it off,' and Lord Ramsay would oblige. It was a game they played. Reek had learned the rules" — description of the flaying game's psychological mechanics

---

## Notes

1. **`pink-letter` artifact node: needs a check.** The event `pink-letter-delivered` exists per baseline, but it is unclear whether a separate artifact node `pink-letter` or `bastard-letter` exists. If not, it's worth proposing: the physical document is cited in multiple arcs (Theon, Jon, the North) and is a cross-arc linchpin.

2. **`smiler` as animal node.** The horse's burning is the final image of ACOK for Theon. Whether this merits an artifact node depends on whether other key animals (Greyworm, direwolves, etc.) have nodes. DEDUP check needed.

3. **`wolf-brooch-brans` — melted slag.** Theon retrieves the melted silver-and-jet slag after burning the bodies (acok-theon-05:67). This slag is what remains. The orchestrator should decide whether to model this as a state change on the same object node or ignore it.

4. **`theons-iron-crown` — deliberate ugliness.** The crown is described twice: once when Theon puts it on, once when Asha mocks it ("the ugliest crown I've ever laid eyes on"). It is made after Mikken's death by the inadequate replacement smith. The ugliness is a material correlate of his failed lordship. If the crown gets a node, both descriptions are worth attaching as Quotes.

5. **Cloak-exchange edge direction.** The Stark direwolf cloak is draped over Jeyne by Theon at the start of the wedding scene, then removed by Ramsay and replaced. The orchestrator will need to decide: does Theon `GIFTED_TO` Jeyne (who has it briefly), or should this be modeled as a ceremonial WIELDS? The baseline confirms `GIFTED_TO` direction = giver→recipient. Suggest: Theon drapes (not a gift), Ramsay removes and GIFTED_TO Jeyne the Bolton cloak.

6. **Kyra edge.** `kyra` node exists per baseline. The `ramsay-snow KILLS kyra` edge is strongly implied but the kill is not shown on-page — it is described retrospectively in Reek I (she was hunted, "punished," and Ben Bones confirms the dog-naming convention in adwd-reek-03). Propose as Tier-2 with the Ben Bones quote: "The ones who give him good sport … The ones who weep and beg and won't run don't get to come back as bitches." (adwd-reek-03:65). The next litter would include a "Kyra" — near-explicit.

7. **Manderly wedding-pie / Rat Cook.** This is a major foreshadowing/subtext moment. Manderly's call for "a song about the Rat Cook" immediately after serving the wedding pies is the text's most explicit signal that the Frey guests are baked into the pies. This does not involve Theon directly, but it is load-bearing for the `wedding-of-ramsay-bolton-and-arya-stark` event and `wyman-manderly` node. Flagging for the synthesizer / Lens A/B to handle the event enrichment; Lens C's contribution is the Manderly "almost dancing" quote and the explicit Rat Cook call at line 141.

8. **Ramsay's ADWD appearance.** The physical description in adwd-reek-01:91–92 is the most complete in the text. Should be added to the `ramsay-snow` node's ## Description section.
