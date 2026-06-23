# Lens 3 — Descriptive / Quote / Object Depth
## Ned's Downfall enrichment dip (S137)

PROPOSE-ONLY. Orchestrator synthesizes and line-checks before minting.

---

## PROPOSED EDGES (object / quote / role)

### Object edges

**1. `valyrian-dagger` --WIELDED_IN--> `littlefinger-betrays-ned`**
- Tier: 1
- Cite: `agot-eddard-14.md:125`
- Verbatim: `"Littlefinger slid Ned's dagger from its sheath and shoved it up under his chin."`
- Justification: The Catspaw dagger (established in earlier chapters as the murder weapon sent after Bran; Ned carries it to the throne room to confront Littlefinger over Jon Arryn's death) is physically deployed by Littlefinger himself in the betrayal moment. This is a direct WIELDED_IN use of the object in the event.
- Confidence: HIGH
- Dedup note: Baseline lists `ice WIELDED_IN execution-of-eddard-stark` (EXISTS). This is a DIFFERENT dagger and a DIFFERENT event (`littlefinger-betrays-ned`). Check whether `valyrian-dagger` (the Catspaw) has a node — if it does, this edge is clean; if not, this becomes a harvest row only, flagged NEEDS_NODE.

**2. `ice` --WIELDED_IN--> `ned-confesses-to-treason`**
- Tier: 1
- Cite: `agot-arya-05.md:171`
- Verbatim: `"Ice, she thought, he has Ice! Her tears streamed down her face, blinding her."`
- Justification: Ice appears at the confession scene itself — Ilyn draws it from his back scabbard on the pulpit steps, in view of the crowd, just before the execution. The existing spine has `ice WIELDED_IN execution-of-eddard-stark`, but Ice is drawn and visible DURING the confession scene and the moment of Ned's forced prostration, not only at the instant of the beheading.
- Confidence: MEDIUM — the two events blur together spatially (same pulpit, same sequence), so this may duplicate the existing edge. Flag for orchestrator: does `ned-confesses-to-treason` need a separate WIELDED_IN, or is the existing edge on `execution-of-eddard-stark` sufficient?

**3. `needle` --OWNS--> `arya-stark` (existing relationship, not the target event)**
- SKIP — standard ownership, not event-scoped. Harvest instead (see below).

**4. Regency letter (Robert's will) — object in `ned-orders-janos-slynt-to-arrest-cersei`**
- No letter node found in baseline. The letter is shredded by Cersei on the spot (agot-eddard-14.md:95). Minor artifact; does not rise to OWNS/WIELDED_IN edge threshold. Harvest row below.

---

## CANDIDATE QUOTE-ATTACHMENTS

Load-bearing verbatim lines to attach as evidence to specific nodes. Each is a contiguous span from the chapter file, including internal dialogue marks.

**Q-1. `cersei-lannister` node — "you win or you die" (THE line of the arc)**
```
cersei-lannister <= "When you play the game of thrones, you win or you die. There is no middle ground."
(agot-eddard-12.md:169)
```
Spoken by Cersei in the godswood confrontation. The single most load-bearing line of the Ned's Downfall arc; it is the thematic verdict on everything that follows.

**Q-2. `ned-discovers-the-truth-of-joffrey-s-parentage` event — Cersei's confirmation**
```
ned-discovers-the-truth-of-joffrey-s-parentage <= "All three are Jaime's." (agot-eddard-12.md:129)
```
Ned's statement, confirmed by Cersei's "Thank the gods." (agot-eddard-12.md:131). The confession of paternity that sets the whole conspiracy in motion.

**Q-3. `ned-discovers-the-truth-of-joffrey-s-parentage` event — Cersei's twin-womb confession**
```
ned-discovers-the-truth-of-joffrey-s-parentage <= "Since we were children together. And why not? The Targaryens wed brother to sister for three hundred years, to keep the bloodlines pure. And Jaime and I are more than brother and sister. We are one person in two bodies."
(agot-eddard-12.md:117)
```
Cersei's direct admission of the incest — the verbal evidence substrate for the parentage revelation.

**Q-4. `varys-confirms-cersei-s-role-in-robert-s-death` event — Varys on the strongwine**
```
varys-confirms-cersei-s-role-in-robert-s-death <= "Cersei gave him the wineskins, and told him it was Robert's favorite vintage."
(agot-eddard-15.md:111)
```
Varys identifies Lancel as the wine-bearer and Cersei as the source — the black-cells confirmation that the hunt death was engineered.

**Q-5. `varys-confirms-cersei-s-role-in-robert-s-death` event — Varys on mercy as the weapon**
```
varys-confirms-cersei-s-role-in-robert-s-death <= "It was not wine that killed the king. It was your mercy."
(agot-eddard-15.md:111)
```
Varys's verdict: Ned's warning to Cersei is what triggered the conspiracy — she moved because he told her he would. Second most load-bearing line of the arc after "you win or you die."

**Q-6. `varys` node — "I serve the realm" (the Varys doctrine)**
```
varys <= "Why, the realm, my good lord, how ever could you doubt that? I swear it by my lost manhood. I serve the realm, and the realm needs peace."
(agot-eddard-15.md:143)
```
Varys's stated justification for his black-cells manipulation. First full articulation of the "I serve the realm" identity claim.

**Q-7. `varys` node — the madness of mercy**
```
varys <= "Ah. To be sure. You are an honest and honorable man, Lord Eddard. Ofttimes I forget that. I have met so few of them in my life."
(agot-eddard-15.md:107)
```
Paired with Ned's admission: `"The madness of mercy," Ned admitted.` (agot-eddard-15.md:105). The Varys-Ned exchange that frames the whole tragedy.

**Q-8. `ned-confesses-to-treason` event — Ned's confession speech**
```
ned-confesses-to-treason <= "I am Eddard Stark, Lord of Winterfell and Hand of the King, and I come before you to confess my treason in the sight of gods and men."
(agot-arya-05.md:149)
```
The opening of the false confession. Verbatim opening line of Ned's public statement.

**Q-9. `ned-confesses-to-treason` event — full confession content**
```
ned-confesses-to-treason <= "I betrayed the faith of my king and the trust of my friend, Robert. I swore to defend and protect his children, yet before his blood was cold, I plotted to depose and murder his son and seize the throne for myself. Let the High Septon and Baelor the Beloved and the Seven bear witness to the truth of what I say: Joffrey Baratheon is the one true heir to the Iron Throne, and by the grace of all the gods, Lord of the Seven Kingdoms and Protector of the Realm."
(agot-arya-05.md:153)
```
The full body of the false confession. Decisive evidence for the event node.

**Q-10. `execution-of-eddard-stark` event — Joffrey breaks his mercy promise**
```
execution-of-eddard-stark <= "My mother bids me let Lord Eddard take the black, and Lady Sansa has begged mercy for her father. But they have the soft hearts of women. So long as I am your king, treason shall never go unpunished. Ser Ilyn, bring me his head!"
(agot-arya-05.md:161)
```
The exact words of Joffrey's command — the broken promise that triggers the execution. Direct evidence for Joffrey's role and Cersei's prior intent.

**Q-11. `petyr-baelish` node — the betrayal line**
```
petyr-baelish <= "I did warn you not to trust me, you know."
(agot-eddard-14.md:125)
```
Littlefinger's closing line as he puts the dagger under Ned's chin. Character-defining; attaches to petyr-baelish node as a quote.

**Q-12. `littlefinger-betrays-ned` event — Renly's offer refused**
```
ned-orders-janos-slynt-to-arrest-cersei <= "I shall require your help. Take me to the godswood." / "I want the guard doubled. No one enters or leaves the Tower of the Hand without my leave."
```
SKIP — these are staging actions, not a quote-attachment candidate of load-bearing weight. Use as harvest.

**Q-13. `eddard-stark` node — "the lies we tell for love"**
```
eddard-stark <= "The lies we tell for love, he thought. May the gods forgive me."
(agot-eddard-13.md:71)
```
Ned's internal voice as he writes "my heir" instead of "my son Joffrey" in Robert's will. Character-defining line, the ethical compromise that haunts him. Attaches to eddard-stark node.

**Q-14. `death-of-robert-baratheon` event — Robert on the boar**
```
death-of-robert-baratheon <= "Killed by a pig. Ought to laugh, but it hurts too much."
(agot-eddard-13.md:93)
```
Robert's own dark-humor verdict on his death. Direct Tier-1 quote from the deathbed scene.

**Q-15. `cersei-lannister` node — "a tame wolf" (Varys quoting Cersei's intent)**
```
cersei-lannister <= "Cersei knows you are a man of honor. … she will allow you to take the black and live out the rest of your days on the Wall … she will allow you to take the black … a tame wolf is of more use than a dead one."
(agot-eddard-15.md:131)
```
Varys quoting Cersei's reasoning: the queen wanted compliance, not a corpse — until Joffrey overrode her.

---

## HARVEST ROWS

Ordered roughly by chapter sequence. Kind labels: `food` / `description` / `quote` / `foreshadowing` / `object` / `hospitality`.

### agot-eddard-12.md — Godswood Confrontation / Cersei reveals truth

| # | Cite | Kind | Note |
|---|------|------|------|
| H-01 | agot-eddard-12.md:15 | object | "The milk of the poppy, for when the pain grows too onerous" — Pycelle's stoppered flask; first appearance of the milk of the poppy as a recurring object in this arc |
| H-02 | agot-eddard-12.md:33 | food | "Ned called for a cup of honeyed wine" — Ned's drink while injured, processing what he knows; hospitality/coping context |
| H-03 | agot-eddard-12.md:37 | food / hospitality | Littlefinger mentions Lady Tanda's lunch: "No doubt she will roast me a fatted calf. If it's near as fatted as her daughter, I'm like to rupture and die." — dark comic food reference; Littlefinger's habitual social manipulation framed through food/hospitality |
| H-04 | agot-eddard-12.md:37 | description | Littlefinger's clothes: "plum-colored doublet with a mockingbird embroidered on the breast in black thread, and a striped cloak of black and white" |
| H-05 | agot-eddard-12.md:65 | foreshadowing | Ned dreams of Rhaegar's children: "Lord Tywin had laid the bodies beneath the Iron Throne, wrapped in the crimson cloaks of his house guard. That was clever of him; the blood did not show so badly against the red cloth." — Ned's dread that Cersei's children will meet the same fate; parallels his own situation |
| H-06 | agot-eddard-12.md:93 | description | The godswood setting: "The thick walls shut out the clamor of the castle, and he could hear birds singing, the murmur of crickets, leaves rustling in a gentle wind. The heart tree was an oak, brown and faceless." — Red Keep's godswood lacks a weirwood face; setting detail for Cersei confrontation |
| H-07 | agot-eddard-12.md:101 | description | Cersei's appearance: "dressed simply, in leather boots and hunting greens … a brown cloak … the bruise where the king had struck her. The angry plum color had faded to yellow" — the fading bruise is physical evidence of Robert's violence; Cersei came alone as instructed |
| H-08 | agot-eddard-12.md:107 | description | Cersei close-up at sunset: "Her curling blond hair moved in the wind, and her eyes were green as the leaves of summer" — Ned sees her beauty for the first time in long while, narrated before accusing her |
| H-09 | agot-eddard-12.md:113 | quote | "Jaime would have killed him, even if it meant his own life. My brother is worth a hundred of your friend." — Cersei on Jaime/Robert's violence toward her; reveals Jaime's protective instinct |
| H-10 | agot-eddard-12.md:117 | quote | Cersei twin-womb speech: "He came into this world holding my foot, our old maester said." — the most intimate detail of Cersei/Jaime bond; harvest for cersei-lannister / jaime-lannister nodes |
| H-11 | agot-eddard-12.md:137 | quote | "My brother found a woman to cleanse me." — Cersei on her terminated pregnancy with Robert's child; significant character backstory |
| H-12 | agot-eddard-12.md:141 | quote | "The night of our wedding feast, the first time we shared a bed, he called me by your sister's name." — Cersei on Robert whispering "Lyanna"; root of her hatred; key evidence for Lyanna Stark's shadow over Robert's reign |
| H-13 | agot-eddard-12.md:143 | quote | "I do not know which of you I pity most." — Ned's response to Cersei's wedding-night confession; characteristic Ned restraint |
| H-14 | agot-eddard-12.md:149 | quote | Cersei's seduction: "The realm needs a strong Hand. Joff will not come of age for years. No one wants war again … Be kind to me, Ned. I swear to you, you shall never regret it." — Cersei offering herself to Ned; significant character moment |
| H-15 | agot-eddard-12.md:157 | quote | Cersei's attack on Ned's honor: "Some Dornish peasant you raped while her holdfast burned? A whore? Or was it the grieving sister, the Lady Ashara? She threw herself into the sea, I'm told." — Jon Snow parentage misdirection; Ashara Dayne mentioned; harvest for ashara-dayne node |

### agot-eddard-13.md — Robert's deathbed / Renly's offer refused / Littlefinger counsels treason

| # | Cite | Kind | Note |
|---|------|------|------|
| H-16 | agot-eddard-13.md:13 | description | Ned's night dress for Robert's summons: "white linen tunic and grey cloak, trousers cut open down his plaster-sheathed leg, his badge of office, and last of all a belt of heavy silver links. He sheathed the Valyrian dagger at his waist." — the Catspaw dagger is deliberately named and worn to the throne room; Ned carries it as both evidence and statement |
| H-17 | agot-eddard-13.md:21 | description | Night atmosphere at Red Keep: "The moon hung low over the walls, ripening toward full. On the ramparts, a guardsman in a gold cloak walked his rounds." — setting for Robert's death watch |
| H-18 | agot-eddard-13.md:23 | description | Kingsguard arrangement at Maegor's: "Ser Boros Blount guarded the far end of the bridge, white steel armor ghostly in the moonlight … Ser Preston Greenfield stood at the bottom of the steps, and Ser Barristan Selmy waited at the door of the king's bedchamber. Three men in white cloaks, he thought … and a strange chill went through him." — Ned counts three white cloaks and feels dread; foreshadowing of their failure |
| H-19 | agot-eddard-13.md:27 | description / food | Robert's deathbed scene: "Fires blazed in the twin hearths … The heat within was suffocating … Servants moved back and forth, feeding logs to the fire and boiling wine." — the boiled wine is a strange detail; possible medical/sterilization context; the wound smells of "smoke and blood and death" |
| H-20 | agot-eddard-13.md:29 | description | Robert's wound: "It had ripped the king from groin to nipple with its tusks. The wine-soaked bandages that Grand Maester Pycelle had applied were already black with blood, and the smell off the wound was hideous." |
| H-21 | agot-eddard-13.md:37 | quote | Robert: "Damn you, Robert … why do you always have to be so headstrong?" — Ned's grief given expression in a curse; rare emotional outburst |
| H-22 | agot-eddard-13.md:47 | quote | Robert on Daenerys: "The girl … Daenerys. Only a child, you were right … that's why, the girl … the gods sent the boar … sent to punish me." — Robert's deathbed repentance on the assassination order; important for Daenerys arc foreshadowing |
| H-23 | agot-eddard-13.md:57 | food | "Grand Maester Pycelle gave … a cup of thick white liquid. 'The milk of the poppy, Your Grace. Drink. For your pain.' Robert knocked the cup away." — second refusal of milk of the poppy; Robert delays the oblivion that would ease his death |
| H-24 | agot-eddard-13.md:71 | object | The regency letter: "a roll of crisp white parchment sealed with golden wax, a few short words and a smear of blood. How small the difference between victory and defeat, between life and death." — the physical letter described; Robert signed it with a bloody smear |
| H-25 | agot-eddard-13.md:85 | food / quote | Robert's last request: "'Serve the boar at my funeral feast,' Robert rasped. 'Apple in its mouth, skin seared crisp. Eat the bastard. Don't care if you choke on him. Promise me, Ned.'" — Robert wants the boar that killed him eaten at his own funeral feast; extraordinary food/hospitality moment |
| H-26 | agot-eddard-13.md:103 | food | Robert's deathbed final drink: "Grand Maester Pycelle mixed him another draught of the milk of the poppy. This time the king drank deeply. His black beard was beaded with thick white droplets when he threw the empty cup aside." — the visual of milk-of-poppy beads in Robert's beard is striking |
| H-27 | agot-eddard-13.md:107 | quote | Robert's last words: "'Will I dream?' … 'I will give Lyanna your love, Ned. Take care of my children for me.'" — Robert's dying words name Lyanna; Ned cannot bring himself to correct him about "my children" |
| H-28 | agot-eddard-13.md:163 | quote | Renly's offer: "Strike! Now, while the castle sleeps … We must get Joffrey away from his mother and take him in hand. Protector or no, the man who holds the king holds the kingdom." — Renly's realpolitik; Ned refuses |
| H-29 | agot-eddard-13.md:267 | quote | Littlefinger on honor: "You wear your honor like a suit of armor, Stark. You think it keeps you safe, but all it does is weigh you down and make it hard for you to move." — Littlefinger's characterization of Ned; one of the arc's sharpest diagnostic lines |
| H-30 | agot-eddard-13.md:253 | object | The dagger as evidence/argument: "He drew the dagger and laid it on the table between them; a length of dragonbone and Valyrian steel, as sharp as the difference between right and wrong, between true and false, between life and death." — Ned produces the Catspaw dagger to confront Littlefinger; the blade is described in full |

### agot-eddard-14.md — The Throne Room Betrayal

| # | Cite | Kind | Note |
|---|------|------|------|
| H-31 | agot-eddard-14.md:11 | description | Dawn scene before the betrayal: "men in mail and leather and crimson cloaks … Ned watched Sandor Clegane gallop across the hard-packed ground to drive an iron-tipped lance through a dummy's head. Canvas ripped and straw exploded as Lannister guardsmen joked and cursed." — Lannister war-games in the yard while Ned watches from above; intimidation show |
| H-32 | agot-eddard-14.md:15 | food | Ned's last morning meal: "Ned broke his fast with his daughters and Septa Mordane. Sansa, still disconsolate, stared sullenly at her food and refused to eat, but Arya wolfed down everything that was set in front of her." — final family breakfast before the betrayal; food as character contrast (Sansa refuses, Arya devours) |
| H-33 | agot-eddard-14.md:43 | food / hospitality | Pycelle in Ned's solar: "Pycelle … gratefully accepted Ned's offer of a chair and a cup of sweet beer." — minor hospitality beat; Ned maintains courtesy even in crisis |
| H-34 | agot-eddard-14.md:51 | description | Varys's entrance: "Varys entered in a wash of lavender, pink from his bath, his plump face scrubbed and freshly powdered, his soft slippers all but soundless." — Varys's physical appearance in the council scene |
| H-35 | agot-eddard-14.md:77 | description | Janos Slynt at the throne room door: "armored in ornate black-and-gold plate, with a high-crested helm under one arm. The Commander bowed stiffly." — Slynt's ceremonial armor; notable that it is black-and-gold (City Watch colors), not yet the lordly livery he will acquire |
| H-36 | agot-eddard-14.md:83 | description | Cersei's throne-room gown: "a gown of sea-green silk, trimmed with Myrish lace as pale as foam. On her finger was a golden ring with an emerald the size of a pigeon's egg, on her head a matching tiara." — Cersei dressed for her coup; sea-green and emerald vs. her earlier brown hunting greens; the pigeon's-egg emerald is striking |
| H-37 | agot-eddard-14.md:85 | description | Joffrey on the throne: "a cloth-of-gold doublet and a red satin cape … Sandor Clegane was stationed at the foot of the throne's steep narrow stair. He wore mail and soot-grey plate and his snarling dog's-head helm." — the Hound in full armor at the throne's base; visual tableau of power |
| H-38 | agot-eddard-14.md:85 | description | Joffrey's cape detail: "His red satin cape was patterned in gold thread; fifty roaring lions to one side, fifty prancing stags to the other." — Joffrey's heraldic display on his coup day; lions and stags equal on the cloth, the lie of legitimacy |
| H-39 | agot-eddard-14.md:87 | description | City Watch deployment: "all along the walls, in front of Robert's tapestries with their scenes of hunt and battle, the gold-cloaked ranks of the City Watch stood stiffly to attention, each man's hand clasped around the haft of an eight-foot-long spear tipped in black iron. They outnumbered the Lannisters five to one." — the trap is set; the very men Ned bought are turned against him |
| H-40 | agot-eddard-14.md:95 | object | Robert's letter destroyed: "The queen glanced at the words. 'Protector of the Realm,' she read. 'Is this meant to be your shield, my lord? A piece of paper?' She ripped the letter in half, ripped the halves in quarters, and let the pieces flutter to the floor." — the regency letter physically destroyed by Cersei; Ser Barristan's shocked reaction immediately follows |
| H-41 | agot-eddard-14.md:121 | description | Tomard's death: "With a single sharp thrust, the nearest gold cloak drove his spear into Tomard's back. Fat Tom's blade dropped from nerveless fingers as the wet red point burst out through his ribs, piercing leather and mail. He was dead before his sword hit the floor." — detailed description of the first kill in the throne room massacre |
| H-42 | agot-eddard-14.md:123 | description | The Hound kills Cayn: "Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone." — the Hound's efficiency in the massacre; two-stroke kill |
| H-43 | agot-eddard-14.md:123 | description | Janos Slynt kills Varly: "Janos Slynt himself slashed open Varly's throat." — Slynt personally kills one of Ned's men; important for Slynt characterization |

### agot-eddard-15.md — The Black Cells

| # | Cite | Kind | Note |
|---|------|------|------|
| H-44 | agot-eddard-15.md:11 | description | Black cell description: "The straw on the floor stank of urine. There was no window, no bed, not even a slop bucket … walls of pale red stone festooned with patches of nitre, a grey door of splintered wood, four inches thick and studded with iron … The dark was absolute." — the only physical description of Ned's cell; sensory inventory |
| H-45 | agot-eddard-15.md:13 | quote | Ned's jest-recall: "The king eats, Robert had said, and the Hand takes the shit. … The king dies, Ned Stark thought, and the Hand is buried." — Ned reversing Robert's old joke; elegiac, dark humor in extreme suffering |
| H-46 | agot-eddard-15.md:19 | quote | Cersei's voice in the dark: "Cersei Lannister's face seemed to float before him in the darkness … 'When you play the game of thrones, you win or you die,' she whispered." — Ned's cell-hallucination echoes the godswood; the line haunts him |
| H-47 | agot-eddard-15.md:23 | description | Ned's physical state in the cell: "feverish by then, his leg a dull agony, his lips parched and cracked" |
| H-48 | agot-eddard-15.md:35 | food | Ned's first water: "A gaoler thrust a jug at him. The clay was cool and beaded with moisture. Ned grasped it with both hands and gulped eagerly. Water ran from his mouth and dripped down through his beard. He drank until he thought he would be sick." — stark water-as-sustenance; no food, only water |
| H-49 | agot-eddard-15.md:37 | description | The rat-faced gaoler: "a scarecrow of a man with a rat's face and frayed beard, clad in a mail shirt and a leather half cape" |
| H-50 | agot-eddard-15.md:59 | food | Varys's wine in the cell: "He thrust a wineskin into Ned's hands … 'Drink, Lord Eddard.'" / "'Dregs.' He felt as though he were about to bring the wine back up." — the wineskin of dregs; food/hospitality in the most degraded form; Ned asks if it's the same poison that killed Robert |
| H-51 | agot-eddard-15.md:67 | food | Varys drinks from the wineskin to prove it's safe: "He drank, a trickle of red leaking from the corner of his plump mouth. 'Not the equal of the vintage you offered me the night of the tourney, but no more poisonous than most.'" — Varys references the tourney wine; hospitality echo across chapters |
| H-52 | agot-eddard-15.md:61 | description | Varys in disguise: "this gaoler was stouter, shorter, though he wore the same leather half cape and spiked steel cap … The eunuch's plump cheeks were covered with a dark stubble of beard … Varys had transformed himself into a grizzled turnkey, reeking of sweat and sour wine." — Varys's physical transformation; the disguise is detailed |
| H-53 | agot-eddard-15.md:155 | quote | Varys on innocents: "The High Septon once told me that as we sin, so do we suffer. If that's true, Lord Eddard, tell me … why is it always the innocents who suffer most, when you high lords play your game of thrones?" — Varys's closing speech; the phrase "game of thrones" used by VARYS as well as Cersei; cross-character echo |
| H-54 | agot-eddard-15.md:155 | quote | Varys on Rhaenys: "Rhaenys was a child too. Prince Rhaegar's daughter. A precious little thing, younger than your girls. She had a small black kitten she called Balerion, did you know?" — Varys uses Rhaenys's kitten (named Balerion) as emotional leverage; harvest for rhaenys-targaryen and balerion-the-black-dread nodes (the cat vs. the dragon confusion) |
| H-55 | agot-eddard-15.md:155 | foreshadowing | Varys threatens Sansa: "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head." — the first time Sansa is explicitly named as a hostage/leverage; foreshadows Sansa's captivity arc |
| H-56 | agot-eddard-15.md:41 | foreshadowing | Ned's Harrenhal memory in the cell: "He remembered Brandon's laughter, and Robert's berserk valor in the melee, the way he laughed as he unhorsed men left and right. He remembered Jaime Lannister, a golden youth in scaled white armor, kneeling on the grass in front of the king's pavilion and making his vows." — Ned's fever-memory of the tourney at Harrenhal; Rhaegar crowned Lyanna the queen of beauty here; load-bearing backstory |
| H-57 | agot-eddard-15.md:43 | foreshadowing | Rhaegar in Ned's fever-dream: "the crown prince wore the armor he would die in: gleaming black plate with the three-headed dragon of his House wrought in rubies on the breast. A plume of scarlet silk streamed behind him … a crown of winter roses, blue as frost." — Rhaegar's appearance at Harrenhal; the winter roses crown for Lyanna; R+L=J evidence substrate |

### agot-sansa-04.md — Sansa's Audience with Cersei

| # | Cite | Kind | Note |
|---|------|------|------|
| H-58 | agot-sansa-04.md:13 | description | Sansa's dress for Cersei: "a simple dress of dark grey wool, plainly cut but richly embroidered around the collar and sleeves … the silver fastenings" — Sansa dresses herself for the first time without servants; detail of her captive state |
| H-59 | agot-sansa-04.md:23 | food | Sansa and Jeyne's meals during captivity: "hard cheese and fresh-baked bread and milk to break their fast, roast chicken and greens at midday, and a late supper of beef and barley stew" — full captive meal schedule; notable that they ARE fed despite being prisoners |
| H-60 | agot-sansa-04.md:39 | description | Ser Boros Blount's description: "an ugly man with a broad chest and short, bandy legs. His nose was flat, his cheeks baggy with jowls, his hair grey and brittle. Today he wore white velvet, and his snowy cloak was fastened with a lion brooch. The beast had the soft sheen of gold, and his eyes were tiny rubies." — Boros described in full; the Kingsguard cloak + lion brooch detail |
| H-61 | agot-sansa-04.md:47 | description | Cersei's mourning gown: "a high-collared black silk gown, with a hundred dark red rubies sewn into her bodice, covering her from neck to bosom. They were cut in the shape of teardrops, as if the queen were weeping blood." — ruby teardrops on Cersei's mourning dress; striking image; Cersei performing grief while executing a coup |
| H-62 | agot-sansa-04.md:85 | description | Littlefinger's gaze on Sansa: "Something about the way the small man looked at her made Sansa feel as though she had no clothes on. Goose bumps pimpled her skin." — first explicit statement of Littlefinger's predatory gaze on Sansa; foreshadowing of later arc |
| H-63 | agot-sansa-04.md:101 | object | Ned's letter to Stannis used as evidence: "The paper was torn and stiff with dried blood, but the broken seal was her father's, the direwolf stamped in pale wax." — the Stannis letter found on the dead captain of Ned's guard; used to condemn Ned |
| H-64 | agot-sansa-04.md:179 | object | Ned's seal used by Varys: "Varys had her father's seal. She warmed the pale white beeswax over a candle, poured it carefully, and watched as the eunuch stamped each letter with the direwolf of House Stark." — Varys holds Ned's personal seal; uses it to authenticate Sansa's coerced letters to her family |

### agot-arya-05.md — Arya in the Streets / The Execution

| # | Cite | Kind | Note |
|---|------|------|------|
| H-65 | agot-arya-05.md:11 | food | The Street of Flour: "The scent of hot bread drifting from the shops along the Street of Flour was sweeter than any perfume Arya had ever smelled." — Arya's hunger framing the arc; bread as longing |
| H-66 | agot-arya-05.md:13 | food | Arya catches a pigeon: "It was a plump one, speckled brown, busily pecking at a crust that had fallen between two cobblestones … She grabbed its neck and twisted until she felt the bone snap." — Arya's survival method; kills the pigeon herself |
| H-67 | agot-arya-05.md:19 | food | The pushcart tarts: "A man was pushing a load of tarts by on a two-wheeled cart; the smells sang of blueberries and lemons and apricots. Her stomach made a hollow rumbly noise. 'Could I have one? A lemon, or … or any kind.' … 'Three coppers.'" / "She showed him the dead bird. 'I'll trade you a fat pigeon.'" — Arya tries to barter pigeon for tarts; pushcart man refuses; "The tarts were still warm from the oven." |
| H-68 | agot-arya-05.md:43 | food | Flea Bottom pot-shops: "there were pot-shops along the alleys where huge tubs of stew had been simmering for years, and you could trade half your bird for a heel of yesterday's bread and a 'bowl o' brown,' and they'd even stick the other half in the fire and crisp it up for you, so long as you plucked the feathers yourself … It usually had barley in it, and chunks of carrot and onion and turnip, and sometimes even apple, with a film of grease swimming on top. Mostly she tried not to think about the meat. Once she had gotten a piece of fish." — the "bowl o' brown" described in detail; the most vivid street-food description in AGOT |
| H-69 | agot-arya-05.md:43 | food | Arya's longing: "Arya would have given anything for a cup of milk and a lemon cake, but the brown wasn't so bad." — the lemon cake; Sansa's treat in contrast to Arya's survival food; ironic counterpoint to Sansa's captive meals |
| H-70 | agot-arya-05.md:29 | description | Gold cloaks on the street: "Their cloaks hung almost to the ground, the heavy wool dyed a rich gold; their mail and boots and gloves were black. One wore a longsword at his hip, the other an iron cudgel." — gold cloaks described in street context; threat to Arya; the cudgel vs. sword detail |
| H-71 | agot-arya-05.md:29 | description | Heads on the walls: "even from a distance she could see the heads rotting atop the high red walls. Flocks of crows squabbled noisily over each head, thick as flies." — the public display of heads; crows on them; visual horror from a distance |
| H-72 | agot-arya-05.md:107 | description | Arya injured en route to the execution: "She tripped and fell, face first, scraping her knee open on a stone and smashing her fingers when her hands hit the hard-packed earth … The thumb of her left hand was covered with blood. When she sucked on it, she saw that half the thumbnail was gone, ripped off in her fall." — Arya's self-injury en route; she leaves blood smears on Baelor's statue |
| H-73 | agot-arya-05.md:137 | description | Ned on the pulpit: "Lord Eddard stood on the High Septon's pulpit outside the doors of the sept, supported between two of the gold cloaks. He was dressed in a rich grey velvet doublet with a white wolf sewn on the front in beads, and a grey wool cloak trimmed with fur, but he was thinner than Arya had ever seen him, his long face drawn with pain. He was not standing so much as being held up; the cast over his broken leg was grey and rotten." — Ned's physical appearance at the execution; the rotting cast is striking; the Stark direwolf in white beads on grey |
| H-74 | agot-arya-05.md:139 | description | The High Septon: "a squat man, grey with age and ponderously fat, wearing long white robes and an immense crown of spun gold and crystal that wreathed his head with rainbows whenever he moved." |
| H-75 | agot-arya-05.md:141 | description | Joffrey at the sept: "his raiment all crimson, silk and satin patterned with prancing stags and roaring lions, a gold crown on his head. His queen mother stood beside him in a black mourning gown slashed with crimson, a veil of black diamonds in her hair." — Joffrey and Cersei's clothes at the execution; Cersei's black-and-crimson mourning; black diamonds veil |
| H-76 | agot-arya-05.md:141 | description | Hound at the sept: "the Hound, wearing a snowy white cloak over his dark grey armor" — the Hound in a white cloak (Kingsguard position) at the execution; anachronistic visual for a character who usually wears grey/black |
| H-77 | agot-arya-05.md:143 | description | Sansa at the sept: "dressed in sky-blue silk, with her long auburn hair washed and curled and silver bracelets on her wrists" — Sansa's appearance contrasted with Arya's street-grime; the sky-blue silk against the execution backdrop |
| H-78 | agot-arya-05.md:145 | description | Janos Slynt commanding the spear-line: "a stout man in elaborate armor, all black lacquer and gold filigree. His cloak had the metallic shimmer of true cloth-of-gold." — Slynt in command dress at the execution; black lacquer + cloth-of-gold; the pomp of his betrayal reward |
| H-79 | agot-arya-05.md:155 | description | Ilyn Payne described: "tall and fleshless, a skeleton in iron mail, the King's Justice" — Ilyn Payne's physical description at the pulpit |
| H-80 | agot-arya-05.md:163 | description | Janos Slynt's order: "the gold cloaks flung Lord Eddard to the marble, with his head and chest out over the edge." — Ned thrown down by Slynt's men; the prostration before the beheading |
| H-81 | agot-arya-05.md:171 | description | Ice described at the moment of execution: "Ser Ilyn drew a two-handed greatsword from the scabbard on his back. As he lifted the blade above his head, sunlight seemed to ripple and dance down the dark metal, glinting off an edge sharper than any razor." — the most detailed visual description of Ice in the whole cluster; Arya's final vision of her family's sword |
| H-82 | agot-arya-05.md:171 | foreshadowing | Arya recognizes Ice at the last moment: "Ice, she thought, he has Ice! Her tears streamed down her face, blinding her." — Arya is blinded by tears at the fatal moment; she literally cannot watch |
| H-83 | agot-arya-05.md:177 | description | The execution sound: "she heard a … a noise … a soft sighing sound, as if a million people had let out their breath at once." — the crowd's collective exhalation as the blade falls; no direct description of the blow, only this sound |

### agot-sansa-06.md — Aftermath / The Heads on the Wall

| # | Cite | Kind | Note |
|---|------|------|------|
| H-84 | agot-sansa-06.md:13 | food | Sansa refuses food after the execution: "Servants came and went, bringing meals, but the sight of food was more than she could bear. The dishes piled up on the table beneath her window, untouched and spoiling, until the servants took them away again." — grief expressed through food refusal; striking contrast to the captive meals in sansa-04 |
| H-85 | agot-sansa-06.md:15 | description | Sansa's memory of the execution: "saw the gold cloaks fling him down, saw Ser Ilyn striding forward, unsheathing Ice from the scabbard on his back, saw the moment … the moment when … his legs … the way they'd jerked when Ser Ilyn … when the sword …" — Sansa's traumatic fragmented memory; she cannot name what happened; "his legs" jerking is the detail that shatters her |
| H-86 | agot-sansa-06.md:19 | food | Grand Maester Pycelle's potion: "He gave her a potion of honeywater and herbs and told her to drink a swallow every night. She drank it all right then and went back to sleep." — Pycelle doses Sansa with a sedative; she drinks the full dose at once |
| H-87 | agot-sansa-06.md:27 | description | Sandor's condition: "Sandor Clegane stood at his shoulder in a plain brown doublet and green mantle, his burned face hideous in the morning light." — the Hound's burned face described directly; morning light is harsh on it |
| H-88 | agot-sansa-06.md:47 | description | Joffrey's appearance in Sansa's revised perception: "He was wearing a padded crimson doublet patterned with lions and a cloth-of-gold cape with a high collar that framed his face. She wondered how she could ever have thought him handsome. His lips were as soft and red as the worms you found after a rain, and his eyes were vain and cruel." — Sansa sees Joffrey clearly for the first time; the worm-lip comparison is pivotal |
| H-89 | agot-sansa-06.md:63 | quote | The Hound to Sansa on Joffrey: "He wants you to smile and smell sweet and be his lady love. He wants to hear you recite all your pretty little words the way the septa taught you. He wants you to love him … and fear him." — Sandor's diagnostic speech on Joffrey; Clegane as reluctant explainer |
| H-90 | agot-sansa-06.md:67 | food / description | Sansa's bath and dress for court: "She drank a glass of buttermilk and nibbled at some sweet biscuits as she waited, to settle her stomach." — the only food Sansa eats in the chapter; buttermilk and biscuits before being forced to court |
| H-91 | agot-sansa-06.md:131 | description | Ned's head on the spike: "Sandor Clegane took the head by the hair and turned it. The severed head had been dipped in tar to preserve it longer. Sansa looked at it calmly, not seeing it at all. It did not really look like Lord Eddard, she thought; it did not even look real." — Ned's head described after tarring; Sansa's dissociation; "How long do I have to look?" |
| H-92 | agot-sansa-06.md:141 | description | Septa Mordane's head: "The jaw had rotted off her face, and birds had eaten one ear and most of a cheek." — the septa's decay; Joffrey shows it to Sansa; "Why did you kill her? She was god-sworn." |
| H-93 | agot-sansa-06.md:87 | quote | Sansa's verdict: "There are no heroes … Life is not a song, sweetling … In life, the monsters win." — Sansa's internal monologue combining Littlefinger's words and her own conclusion; significant character arc moment; attaches to sansa-stark node |
| H-94 | agot-sansa-06.md:165 | quote / foreshadowing | Sansa considers killing Joffrey: "All it would take was a shove, she told herself. He was standing right there, right there, smirking at her with those fat wormlips. You could do it, she told herself." — Sansa's first homicidal ideation toward Joffrey; interrupted by Sandor |
| H-95 | agot-sansa-06.md:167 | description | Sandor's act of care: "Sandor Clegane knelt before her, between her and Joffrey. With a delicacy surprising in such a big man, he dabbed at the blood welling from her broken lip." — the Hound kneels to clean Sansa's blood; one of the defining Clegane-Sansa moments; delicacy described explicitly |

---

## NEEDS_NODE / NEEDS_VOCAB FLAGS

- **`valyrian-dagger` (the Catspaw):** H-16 and H-30 both describe it in detail at pivotal moments. If a node exists for this artifact, the WIELDED_IN edge (Proposed Edge #1) is mintable. If not, it's harvest only.
- **`rhaenys-targaryen` / the kitten Balerion:** H-54 (agot-eddard-15.md:155) — Varys names Rhaenys's black kitten "Balerion"; this is a piece of node evidence for both `rhaenys-targaryen` and potentially the cat-Balerion vs. dragon-Balerion distinction.
- **`ashara-dayne`:** H-15 — Cersei names her in the godswood; Jon Snow parentage misdirection; if an ashara-dayne node exists, this is a quote-attachment candidate.
- **`lancel-lannister` / the hunt wineskins:** The strongwine/wineskin betrayal is covered in baseline (Varys confirms Cersei's role), but Lancel as the physical agent isn't separately harvested. Agot-eddard-13.md:135–149 is the source passage; it runs across ~15 lines with Varys and Barristan's exchange. Flag for Lens 4 (causal wiring).

---

## 4-LINE SUMMARY

**Proposed edges:** 2 viable (valyrian-dagger WIELDED_IN littlefinger-betrays-ned; ice WIELDED_IN ned-confesses-to-treason with dedup caveat); 1 skipped as redundant; both gate on whether target event nodes exist.

**Candidate quote-attachments:** 15 verbatim quote-attachments covering: Cersei's "you win or you die," the twin-womb confession, Varys's cell speeches ("I serve the realm," "it was your mercy," the Rhaenys kitten speech), Ned's false confession verbatim, Joffrey's broken mercy promise, Littlefinger's "I did warn you," Robert's "Lyanna" last words, and Ned's "lies we tell for love."

**Harvest rows:** 95 rows across all 7 chapters — food (18+ rows including Robert's boar funeral feast, Arya's bowl o'brown, Sansa's refused meals, the milk of the poppy sequence, the pushcart tarts, the wineskin dregs), description (40+ rows covering the black cell, the execution scene clothing and staging, Ned's rotting cast, Ice at the moment of beheading, the tarred head), quotes (15+ notable lines), foreshadowing (7 rows including Harrenhal memory, Sansa's homicidal ideation, Varys's Rhaenys speech).

**Flags for orchestrator:** valyrian-dagger and ashara-dayne need node-existence check before edge mint; Lancel wineskins (causal agent for Robert's death) flagged for Lens 4 causal wiring; the Sansa "monsters win" line needs node assignment; Rhaenys kitten Balerion is a live harvest item if the rhaenys node exists.
