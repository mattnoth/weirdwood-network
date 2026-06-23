# Lens 2 — Participants, Witnesses, Suspected Agents, Secondary Sub-arcs
## Battle of the Blackwater enrichment dip (S138)

> Lens: secondary-character sub-arcs + SUSPECTED_OF / WITNESS_IN / participant substrate  
> Source chapters: acok-davos-03, acok-tyrion-12, acok-tyrion-13, acok-tyrion-14, acok-tyrion-15, acok-sansa-06, acok-sansa-07  
> Deduped against: `working/enrichment/blackwater/baseline.md`

---

## PROPOSED NODES

### N1 — `wildfire-trap-on-the-blackwater` (event.incident)
Tyrion's secret wildfire deployment: hulks stuffed with wildfire jars positioned in the river, detonated when Stannis's fleet was committed. Distinct from `wildfire-plot` (Aerys/283AC — baseline dedup trap confirmed). The actual trap event.
- Status: propose-new
- Tier: 1 (directly described across davos-03 + tyrion-13)
- Evidence anchors: acok-davos-03:131 ("wildfire jars"), acok-tyrion-13:19 ("He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames")

### N2 — `the-chain-boom-on-the-blackwater` (artifact.weapon / device)
The iron chain boom stretched across the mouth of the Blackwater Rush between two newly built towers. Commissioned and deployed by Tyrion; operated by Bronn at the winch towers. Trapped Stannis's fleet after the wildfire detonation.
- Status: propose-new
- Tier: 1
- Evidence anchors: acok-davos-03:57 ("A chain boom"), acok-davos-03:145 ("The chain. Gods save us, they've raised the chain.")

### N3 — `sandor-clegane-deserts-the-kingsguard` (event.incident)
Sandor Clegane's failure of nerve at the King's Gate during the battle — he refuses the final sortie command, demands wine, and later that night abandons the Kingsguard entirely, appearing in Sansa's chambers before leaving the city.
- Status: propose-new
- Tier: 1
- Evidence anchors: acok-tyrion-13:53–67 (refusal at King's Gate), acok-sansa-07:69–129 (Sansa's chambers, cloak left behind)

### N4 — `garlan-tyrell-as-renly-s-ghost` (event.incident)
Garlan Tyrell wore Renly Baratheon's green armor at the Battle of the Blackwater; his appearance in the relief vanguard psychologically routed Stannis's host. Distinct from `shadow-assassination-of-renly` (baseline dedup confirmed).
- Status: propose-new
- Tier: 1 (reported by Dontos, confirmed by multiple in-world witnesses at acok-sansa-07:145)
- Evidence anchors: acok-sansa-07:145 ("It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers!")

### N5 — `tyrion-s-sortie-at-the-king-s-gate` (event.battle)
Tyrion personally leads the mounted sortie out of the King's Gate sally port after Sandor refuses, disperses the battering-ram assault, then leads his troop along the riverfront, routing men coming off the burning ships.
- Status: propose-new (sub-beat of `battle-of-the-blackwater`)
- Tier: 1
- Evidence anchors: acok-tyrion-13:77–88, acok-tyrion-14:1–55

---

## PROPOSED EDGES

### Role edges on `battle-of-the-blackwater` (hub)

---

**E1** `tyrion-lannister --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:27 | "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep; the chain was ponderous heavy, and the great winches turned but slowly…"  
Rationale: Tyrion commands the city's defense — he ordered the chain, positioned the wildfire hulks, directed sortie timing, and led the King's Gate sortie himself. Side: Lannister/King's Landing defense.

---

**E2** `imry-florent --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03:13 | "Ser Imry had decreed that they would enter the river on oars alone, so as not to expose their sails to the scorpions and spitfires on the walls of King's Landing."  
Rationale: Ser Imry Florent is named Lord High Captain, commanding Stannis's fleet from Fury. Side: Stannis/Baratheon fleet.

---

**E3** `stannis-baratheon --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:21 | "He would command from the rear, from the reserve, much as Lord Tywin Lannister was wont to do. Like as not, he was sitting a warhorse right now, clad in bright armor, his crown upon his head."  
Rationale: Stannis commands the south-bank host and overall Baratheon-side operation. Side: Stannis/Baratheon army.

---

**E4** `tywin-lannister --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-15:115 | "They rode through the ashes and took the usurper Stannis in the rear. It was a great victory, and now Lord Tywin has settled into the Tower of the Hand…"  
Rationale: Maester Ballabar confirms Tywin commanded the right wing of the relief force on the north side of the river. Side: Lannister/Tyrell relief.

---

**E5** `mace-tyrell --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:141 | "Lord Tywin himself had their right wing on the north side of the river, with Randyll Tarly commanding the center and Mace Tyrell the left…"  
Rationale: Dontos relays eyewitness accounts naming Mace Tyrell commanding the left wing of the relief force. Side: Lannister/Tyrell relief.

---

**E6** `randyll-tarly --COMMANDS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:141 | "…with Randyll Tarly commanding the center and Mace Tyrell the left…"  
Rationale: Named as commanding the center of the relief column. Side: Lannister/Tyrell relief.

---

**E7** `sandor-clegane --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03:87 | "Davos recognized the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach."  
Rationale: Davos directly observes the Hound fighting on the riverbank against Stannis's archers.

---

**E8** `bronn --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:27 | "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep…"  
Rationale: Bronn commanded the winch towers to raise the chain; Tyrion XV:129 confirms he was knighted for his role ("They made him a knight"). Actively deployed in the battle.

---

**E9** `tyrion-lannister --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-14:23 | "He smashed the man in the face with all the weight of axe and arm and charging horse, taking off half his head."  
Rationale: Tyrion personally leads and fights in the King's Gate sortie and the bridge-of-ships melee.

---

**E10** `mandon-moore --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-14:23 | "Ser Mandon Moore took the place to his right, flames shimmering against the white enamel of his armor, his dead eyes shining passionlessly through his helm."  
Rationale: Rides in Tyrion's sortie, fights in the riverfront melee.

---

**E11** `podrick-payne --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-14:14 | "On the left, Tyrion was surprised to see Podrick Payne, a sword in his hand."  
Rationale: Pod rides in the sortie against Tyrion's order to go back and fights through the bridge-of-ships melee.

---

**E12** `balon-swann --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-14:45 | "Ser Balon Swann wore the same armor, but his horse trappings bore the battling black-and-white swans of his House. Every bit of Ser Balon was spattered with gore and smudged by smoke."  
Rationale: Tyrion encounters Balon Swann actively fighting on the riverfront; they then ride together to the quay.

---

**E13** `garlan-tyrell --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:145 | "They plunged through Stannis like a lance through a pumpkin, every man of them howling like some demon in steel. And do you know who led the vanguard?"  
Rationale: Garlan Tyrell led the vanguard of the relief force, routing Stannis's host.

---

**E14** `imry-florent --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03:13 | "Fury herself would center the first line of battle…From her decks Stannis Baratheon had commanded the assault on Dragonstone sixteen years before, but this time he had chosen to ride with his army, trusting Fury and the command of his fleet to his wife's brother Ser Imry…"  
Rationale: Imry commanded from Fury, the flagship in the first battle line, personally in the river fight.

---

**E15** `davos-seaworth --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03:99 | '"Ramming speed!" Davos shouted.' / acok-davos-03:117 | 'Davos grasped his sword in both hands and drove it up point first into the man's belly.'  
Rationale: Davos commands Black Betha, rams Lady's Shame, boards White Hart, and fights sword-in-hand before the wildfire explosion.

---

**E16** `guyard-morrigen --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:145 | "They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well."  
Rationale: Ser Guyard Morrigen is named as fighting in the battle and being killed by the vanguard (Garlan-as-Renly).

---

**E17** `salladhor-saan --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03:31 | "…Salladhor Saan and his Lyseni, who would stand out in the bay in case the Lannisters had other ships hidden up along the coast…"  
Rationale: Salladhor commanded the Lyseni rear guard in Blackwater Bay — actively assigned to battle disposition.  
Note: He is positioned in the bay, not in the river melee; FIGHTS_IN is marginal but defensible as active combat deployment. If vocab preference is PARTICIPATES_IN for non-melee roles, flag here.

---

**E18** `lancel-lannister --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:13 | "Ser Lancel's surcoat was soaked with the blood seeping out under his arm."  
Rationale: Lancel arrives in the queen's ballroom wounded from the fighting; acok-sansa-06:13 confirms he was at the Mud Gate area. He was actively fighting before being wounded.

---

### Role edges on `a-knight-attacks-tyrion-s-shield` (existing stub)

---

**E19** `mandon-moore --AGENT_IN--> a-knight-attacks-tyrion-s-shield`  
Tier: 1 | acok-tyrion-14:68 | "The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain."  
Rationale: Mandon Moore makes the attack; he first extends his left hand (deceptively), then cuts Tyrion's face.

---

**E20** `tyrion-lannister --VICTIM_IN--> a-knight-attacks-tyrion-s-shield`  
Tier: 1 | acok-tyrion-14:68 | "The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain."  
Rationale: Tyrion is the victim — face slashed, loses most of his nose.

---

**E21** `podrick-payne --KILLS--> mandon-moore`  
Tier: 1 | acok-tyrion-14:72–73 | "And suddenly he lurched to the left, staggering into the rail. Wood split, and Ser Mandon Moore vanished with a shout and a splash." / acok-tyrion-15:141 | '"Dead? You're, certain? Dead?" He shuffled his feet, sheepish. "Drowned."'  
Rationale: Pod shoves Mandon into the river (confirmed drowned in Tyrion XV). The text doesn't name Pod's action explicitly in tyrion-14, but tyrion-15:125 confirms: "How can a boy so bold in battle be so frightened in a sickroom?" + Pod's stutter at :137 when asked about Mandon ("I n-never meant to k-k-k-k—"). Combined with the physical description (someone kneeling over Tyrion after Mandon vanishes, voice is "A boy's voice"), attribution is textually secure.

---

**E22** `podrick-payne --AGENT_IN--> a-knight-attacks-tyrion-s-shield`  
Tier: 1 | acok-tyrion-14:73 | "An instant later, the hulks came slamming together again, so hard the deck seemed to jump. Then someone was kneeling over him."  
Rationale: Pod intervenes to end the attack — he is the agent who kills Mandon and saves Tyrion.

---

### Role edges on `the-antler-men-conspiracy` (existing stub)

---

**E23** `cersei-lannister --AGENT_IN--> the-antler-men-conspiracy`  
Tier: 1 | acok-tyrion-13:41 | "Joff had the Antler Men trussed up naked in the square below, antlers nailed to their heads…'The Whores are yours.'…Some of the gold cloaks had been wagering on whether the traitors would fly all the way across the Blackwater."  
Rationale: Cersei ordered the execution; Tyrion gave the trebuchets to Joffrey and Joffrey flung them, but it was Cersei who had them detained and sentenced (Tyrion XII establishes the conspiracy was handed off to her judgment). The actual execution order here is Joffrey/Tyrion at the trebuchet, but Cersei originated the conspiracy exposure and punishment plan.  
Note: If a tighter COMMANDS_IN onto the execution event is preferred over AGENT_IN on the conspiracy, flag.

---

**E24** `joffrey-baratheon --AGENT_IN--> the-antler-men-conspiracy`  
Tier: 1 | acok-tyrion-13:41 | "Joff had the Antler Men trussed up naked in the square below, antlers nailed to their heads. When they'd been brought before the Iron Throne for justice, he had promised to send them to Stannis…'Be quick about it, Your Grace,' he told Joffrey."  
Rationale: Joffrey physically orders and oversees the trebuchet execution of the Antler Men.

---

### SUSPECTED_OF — Mandon Moore's attempt on Tyrion

**E25** `cersei-lannister --SUSPECTED_OF--> a-knight-attacks-tyrion-s-shield`  
Tier: 2 (cap — unproven) | acok-tyrion-15:97 | "Cersei must have paid him to see that I never came back from the battle. Why else? I never did Ser Mandon any harm that I know of. Tyrion touched his face, plucking at the proud flesh with blunt thick fingers. Another gift from my sweet sister."  
Rationale: Tyrion's in-text reasoning directly names Cersei as the suspected orchestrator. SUSPECTED_OF is the correct type: it encodes unproven-but-load-bearing agency without asserting the act. Tier-2 cap mandatory.

---

### WITNESS_IN — text-anchor gate evaluation

**W-EVAL-1: Sansa witnessing the burning river** (acok-sansa-07:57–61)  
Text: "When she ripped back the drapes, her breath caught in her throat. The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below. Baleful green tides moved against the bellies of the clouds, and pools of orange light spread out across the heavens."  
Verdict: **EMIT.** Sansa is in her bedchamber window, directly perceiving the wildfire afterglow from the battle on the river. She sees the *charged violent aftermath* directly — the smoke, the green light, the embers. This is unambiguous sensory perception of the battle's violence.

**E26** `sansa-stark --WITNESS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:59 | "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires that burned below. Baleful green tides moved against the bellies of the clouds, and pools of orange light spread out across the heavens."  
Rationale: Sansa at her bedchamber window directly perceives the burning river. She does not see the melee itself, but the violent spectacle of wildfire and fire reflecting against the sky — the battle is the thing she is perceiving. Text-anchor gate satisfied.

---

**W-EVAL-2: Davos witnessing his sons burn** (acok-davos-03:139)  
Text: "My sons, Davos thought, but there was no way to look for them amidst the roaring chaos."  
Verdict: **NO EMIT for WITNESS_IN.** Davos *thinks* of his sons but cannot see them or their deaths. He is in the water being swept downstream; he is a VICTIM_IN / FIGHTS_IN the broader battle. He does not witness the charged incident of their deaths. Correct type for Davos → FIGHTS_IN (already proposed E15 above).

---

**W-EVAL-3: Joffrey on the walls during the wildfire** (acok-tyrion-13:23, acok-sansa-06:51)  
Text (tyrion-13:23): "Joffrey's voice cracked as he shouted up from the wallwalk, where he huddled with his guards behind the ramparts…'Look, that's Seaflower, there.'"  
Verdict: **EMIT for sub-beat perception** — Joffrey directly watches the wildfire burning his fleet from the wall. But `battle-of-the-blackwater` is the hub; WITNESS_IN is reserved for perception of charged/violent/secret incidents. Joffrey observing from the walls is better captured as FIGHTS_IN (he is a participant on the walls, commanding crossbowmen per sansa-06:51: "he's walking the walls with the Hand, telling the men to be brave"). Use FIGHTS_IN (already logically covered by his role as reigning king during the battle).

**E27** `joffrey-baratheon --FIGHTS_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:23 | "Joffrey's voice cracked as he shouted up from the wallwalk, where he huddled with his guards behind the ramparts. The golden circlet of kingship adorned his battle helm."  
Rationale: Joffrey is on the walls during the battle in armor; acok-sansa-06:51 confirms "He's at the Mud Gate with the Hand and the Kingsguard." Participant in the defense.

---

### BREAKS_VOW — Sandor Clegane

**E28** `sandor-clegane --BREAKS_VOW--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:57 | '"Bugger that. And you." … "Bugger the King's Hand." … "Someone bring me a drink."'  
Rationale: Sandor explicitly refuses the Hand's command, violates his Kingsguard oath of obedience, and then deserts entirely — acok-sansa-07:127–129 confirms he leaves his white cloak behind in Sansa's chambers, physically abandoning the Kingsguard. BREAKS_VOW is in the locked vocabulary and fits precisely: the vow is his Kingsguard oath; the event-anchor is the battle.

---

### Secondary sub-arc edges

**E29** `sandor-clegane --KILLS--> guyard-morrigen`  
Verdict: **REJECT** — acok-sansa-07:145 attributes Guyard Morrigen's death to Garlan Tyrell ("It was Lord Renly! Lord Renly in his green armor…They say he killed Ser Guyard Morrigen himself in single combat"). Not Sandor.

**E30** `garlan-tyrell --KILLS--> guyard-morrigen`  
Tier: 2 (reported by Dontos — in-world hearsay, not direct witness) | acok-sansa-07:145 | "They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well."  
Rationale: In-world report ("they say") — not a Tier-1 direct witness, but load-bearing: Guyard Morrigen is a named Stannis bannerman and his death is significant. Tier-2 appropriate given "they say" attribution.

---

**E31** `ilyn-payne --PARTICIPATES_IN--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-06:115 | "Ser Ilyn opened his mouth and emitted a choking rattle. His pox-scarred face had no expression… 'He's here for us, he says,' the queen said. 'Stannis may take the city and he may take the throne, but I will not suffer him to judge me. I do not mean for him to have us alive.'"  
Rationale: Ilyn Payne is stationed in Maegor's Holdfast with a specific combat assignment — to execute the women (including the queen and Sansa) if the castle falls, using Ice. He holds an active battlefield role; PARTICIPATES_IN rather than FIGHTS_IN because he never fights — his role is standing guard against a contingency.

---

**E32** `tyrion-lannister --COMMANDS_IN--> tyrion-s-sortie-at-the-king-s-gate`  
Tier: 1 | acok-tyrion-13:77–81 | '"Very well, I'll lead the sortie." … "Me. Ser Mandon, you'll bear the king's banner. Pod, my helm." The boy ran to obey.'  
Rationale: Tyrion assumes command of the sortie himself after Sandor refuses.

---

**E33** `tyrion-s-sortie-at-the-king-s-gate --SUB_BEAT_OF--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:77–88, acok-tyrion-14:1–55  
Rationale: The sortie is a bounded tactical incident within the larger battle.

---

**E34** `sandor-clegane-deserts-the-kingsguard --SUB_BEAT_OF--> battle-of-the-blackwater`  
Tier: 1 | acok-tyrion-13:53–67, acok-sansa-07:65–129  
Rationale: Sandor's desertion arc begins during and concludes immediately after the battle.

---

**E35** `garlan-tyrell-as-renly-s-ghost --SUB_BEAT_OF--> battle-of-the-blackwater`  
Tier: 1 | acok-sansa-07:141–145  
Rationale: The "Renly's ghost" rout is the decisive tactical sub-event within the relief column's assault.

---

**E36** `wildfire-trap-on-the-blackwater --SUB_BEAT_OF--> battle-of-the-blackwater`  
Tier: 1 | acok-davos-03, acok-tyrion-13  
Rationale: The wildfire detonation is the central tactical moment of the battle.

---

**E37** `tyrion-lannister --AGENT_IN--> wildfire-trap-on-the-blackwater`  
Tier: 1 | acok-tyrion-13:19 | "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames."  
Rationale: Tyrion positioned the wildfire hulks and ordered the chain — the trap is his design and execution.

---

**E38** `hallyne --AGENT_IN--> wildfire-trap-on-the-blackwater`  
Tier: 1 | acok-tyrion-13:31 | "Hallyne said that sometimes the substance burned so hot that flesh melted like tallow."  
Rationale: Hallyne and the Alchemists' Guild produced and supplied the wildfire. Hallyne is the pyromancer liaison directly named.

---

**E39** `bronn --AGENT_IN--> wildfire-trap-on-the-blackwater`  
Tier: 1 | acok-tyrion-13:27 | "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep; the chain was ponderous heavy, and the great winches turned but slowly…"  
Rationale: Bronn operated the chain-boom winch mechanism at the tower; his action is what closed the trap.

---

**E40** `the-chain-boom-on-the-blackwater --WIELDED_IN--> wildfire-trap-on-the-blackwater`  
Tier: 1 | acok-davos-03:145 | "The chain. Gods save us, they've raised the chain."  
Rationale: The chain boom is the physical artifact deployed in the wildfire trap event — it seals the river and prevents the burning fleet from escaping.

---

**E41** `garlan-tyrell --IMPERSONATES--> renly-baratheon`  
Tier: 1 | acok-sansa-07:145 | "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers!"  
Rationale: Garlan wears Renly's distinctive armor to create the psychological effect of Renly's ghost. IMPERSONATES fits: deliberate adoption of another's identity/appearance. The deception is tactical and intentional.

---

## HARVEST

`acok-sansa-06:19` / drink / Cersei drinking Arbor gold heavily during the battle — "a golden vintage from the Arbor, fruity and rich"; "the wine only seemed to make her more beautiful"  
`acok-sansa-06:23` / food / Ballroom menu during the battle: broth → salad of apples/nuts/raisins → crabclaw pies → mutton roasted with leeks and carrots in trenchers of hollowed bread → goat cheese with baked apples  
`acok-sansa-06:23` / food / Cersei's salad "untouched" despite the crabclaw pies and mutton being served — fear kills appetite  
`acok-sansa-06:107` / drink / Cersei forces Sansa to drain a cup of "cloyingly sweet, very strong" sweet plum wine  
`acok-sansa-06:61` / food / Lollys Stokeworth eats too fast, retches over herself and her sister; Lord Gyles drinks repeatedly and passes out face-first in his trencher in a puddle of wine  
`acok-tyrion-12:49` / food / Tyrion dines with Cersei: "creamy chestnut soup, crusty hot bread, and greens dressed with apples and pine nuts. Then came lamprey pie, honeyed ham, buttered carrots, white beans and bacon, and roast swan stuffed with mushrooms and oysters" — Tyrion notes the swan "too rich for his taste"  
`acok-tyrion-12:59` / food / "We have Lady Tanda to thank for the pig" — Tyrion carves slices of ham at Cersei's table; the ham is Lady Tanda's gift/bribe  
`acok-tyrion-12:115` / food / "I hope you like blackberry tarts" — final course at Cersei's dinner  
`acok-sansa-07:13` / description / Lancel arrives "soaked with the blood seeping out under his arm" — makes women scream  
`acok-sansa-07:59` / description / Sansa's window view: "The southern sky was aswirl with glowing, shifting colors, the reflections of the great fires…Baleful green tides moved against the bellies of the clouds…The air itself smelled burnt, the way a soup kettle sometimes smelled if it was left on the fire too long and all the soup boiled away. Embers drifted through the night air like swarms of fireflies." — extraordinary sensory description of wildfire aftermath  
`acok-sansa-07:103` / description / Sandor in Sansa's dark room: "a stink of sweat and sour wine and stale vomit, and over it all the reek of blood, blood, blood" — physical description of the Hound post-battle  
`acok-sansa-07:65–68` / quote / Sandor's appearance in Sansa's chamber: "She saw him for a moment, all black and green, the blood on his face dark as tar, his eyes glowing like a dog's in the sudden glare" — load-bearing for character description  
`acok-sansa-07:73` / quote / "I only know who's lost. Me." — Sandor on the battle; characterization  
`acok-sansa-07:77` / quote / "Bloody dwarf. Should have killed him. Years ago." — Sandor on Tyrion; foreshadowing? (Arya road)  
`acok-tyrion-14:39` / quote / Battle fever description — Jaime's words through Tyrion: "You stop feeling, you stop thinking, you stop being you, there is only the fight…death is all around you but their swords move so slowly, you can dance through them laughing" — Tyrion experiencing it for the first time  
`acok-tyrion-13:15` / description / Wildfire's color described: "The low clouds caught the color of the burning river and roofed the sky in shades of shifting green, eerily beautiful. A terrible beauty. Like dragonfire." — Tyrion comparing wildfire to Aegon's Field of Fire  
`acok-davos-03:87` / description / Davos sees Sandor: "the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach" — physical action description  
`acok-davos-03:39` / description / Davos's armor philosophy: "A jerkin of boiled leather and a pothelm at his feet were his only armor. At sea, heavy steel was as like to cost a man his life as to save it" — contrasts with highborn captains who "glittered"  
`acok-tyrion-15:95` / description / Tyrion's wound: "The gash was long and crooked, starting a hair under his left eye and ending on the right side of his jaw. Three-quarters of his nose was gone, and a chunk of his lip." — canonical physical disfigurement description  
`acok-tyrion-12:49` / food/hospitality / Tyrion eats only what Cersei eats (suspicion of poison) — "he offered his sister the choice portions of every dish, and made certain he ate only what she did. Not that he truly thought she'd poison him, but it never hurt to be careful."  
`acok-sansa-07:141` / quote / Dontos's relief announcement names all the Tyrell/Lannister bannermen's heraldry in detail: "the golden rose and golden lion and all the others, the Marbrand tree and the Rowan, Tarly's huntsman and Redwyne's grapes and Lady Oakheart's leaf" — heraldry harvest  
`acok-davos-03:11` / description / Davos's missing fingers: "Davos took a long pull" (on the pouch of finger-bones) — recurring detail  
`acok-sansa-07:109–123` / quote / Sansa's song in the dark: "Gentle Mother, font of mercy / save our sons from war, we pray / stay the swords and stay the arrows / let them know a better day. / Gentle Mother, strength of women / help our daughters through this fray / soothe the wrath and tame the fury / teach us all a kinder way." — full verbatim text; sung under Sandor's dagger  

---

## NOTES

1. **Mandon Moore's attribution (E21/E22):** The text does not name Pod in the moment Mandon vanishes (acok-tyrion-14:73). The attribution is triangulated from: (a) "someone" kneeling over Tyrion with "A boy's voice"; (b) Tyrion's immediate thought "It sounded almost like Pod"; (c) acok-tyrion-15:125–141 where Pod flinches and stutters when asked about Mandon. This is textually unambiguous but multi-step — the edge is Tier 1, not Tier 2, because the text closes the loop in tyrion-15.

2. **Salladhor Saan / FIGHTS_IN marginal call (E17):** Salladhor is assigned to Blackwater Bay as rear guard, per Ser Imry's orders. He does not enter the river melee. If policy preference is PARTICIPATES_IN for command-but-not-melee roles, swap from FIGHTS_IN. Flagged here rather than auto-corrected.

3. **Ilyn Payne / Ice:** Sansa-06:115 shows Ilyn carrying Ice (Ned's sword, now Cersei's executioner's blade). This is load-bearing for Ice's provenance chain — if a `wields` or `wielded-in` edge on the artifact is desired, it belongs in a Lens 3 artifact-focused pass, not here.

4. **Garlan Tyrell / `garlan-tyrell-as-renly-s-ghost` node:** The in-world reception calls him "Lord Renly's ghost" (Dontos) and attributes the rout psychologically to this appearance. The node captures the tactical event. A separate IMPERSONATES edge (E41) captures the identity-level action. Both are needed.

5. **`sandor-clegane-deserts-the-kingsguard` spans two chapters:** The failure-of-nerve begins in tyrion-13 (King's Gate refusal) and completes in sansa-07 (Sansa's chambers, cloak left behind). The node spans both; cite_refs should reference both loci.

6. **`wildfire-trap-on-the-blackwater` vs. the Tyrion XIII opening:** The trap (hulks + chain) is Tyrion's design executed before and during the battle. The node is the event of its execution, not just the planning. Both tyrion-13 (Tyrion watching) and davos-03 (Davos in the river experiencing it) provide strong Tier-1 evidence.
