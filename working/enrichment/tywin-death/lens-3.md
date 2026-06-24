# LENS 3 — Descriptive / Quote / Object Depth
## Unit: assassination-of-tywin-lannister
## Source chapters: asos-tyrion-08, -09, -10, -11

---

## (A) MINT-NODE PROPOSALS

### A-1 — `tywins-crossbow`
- **Type:** `object.artifact`
- **1-line:** The crossbow hung on the wall of the Tower of the Hand's bedchamber; Tyrion takes it down and uses it to kill Tywin in the privy tower.
- **Description quote (asos-tyrion-11, line 211):**
  > "A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls. The poleaxe would be clumsy to wield inside a castle, and the mace was too high to reach, but a large wood-and-iron chest had been placed against the wall directly under the crossbow. He climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot into the stirrup, and pushed down until the bowstring cocked. Then he slipped a bolt into the notch."
- **Mint rationale:** This is the murder weapon for one of the most consequential killings in the series. "Crossbow" alone is too generic; the hanging on Tywin's own bedchamber wall (ironic weapon of hospitality turned on its owner) is precisely described and story-load-bearing. The quiver of quarrels is part of the same object-set. It also recurs — Tyrion's reputation as a crossbow-killer follows him through ADWD. MINT.

---

### A-2 — `hands-chain-of-office`
- **Type:** `object.artifact`
- **1-line:** The physical golden chain of linked hands worn by the Hand of the King; Tyrion uses it to strangle Shae in Tywin's bed.
- **Description quote (asos-tyrion-11, line 197):**
  > "She sat up, letting the blanket slide down to her lap. Beneath it she was naked, but for the chain about her throat. A chain of linked golden hands, each holding the next."
- **Murder-act quote (asos-tyrion-11, line 209):**
  > "Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck."
- **Mint rationale:** Distinct from the `hand-of-the-king` TITLE node — this is the physical object. The chain's visual design (linked golden hands) is explicitly described. It is doubly iconic: it is the emblem of the office Tyrion once held, and it becomes the murder weapon of the woman he loved. MINT. (Note: the chain is on Tywin's neck at court, then around Shae's throat in Tywin's bed — that transfer is its own story detail, and confirms its importance as a recurring physical prop.)

---

### A-3 — `oberyn-spear` — **BORDERLINE / LEAN MINT**
- **Type:** `object.artifact`
- **1-line:** Oberyn Martell's personal fighting spear: eight-foot turned-ash shaft with a slender leaf-shaped steel head, oil (or poison) glistening on the shaft; the weapon he wounds Gregor with.
- **Description quote (asos-tyrion-10, lines 123–124):**
  > "The spear was turned ash eight feet long, the shaft smooth, thick, and heavy. The last two feet of that was steel: a slender leaf-shaped spearhead narrowing to a wicked spike. The edges looked sharp enough to shave with. When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison? Tyrion decided that he would sooner not know."
- **Mint rationale:** The spear is physically described in detail and is the instrument that both wounds Gregor (enabling his slow venom-death) and breaks dramatically during the leap. However, it is never given a name, and its fame derives almost entirely from who wields it and what it's coated with, not from any named artifact identity. It sits at the threshold. **Decision: MINT** — the description is specific enough, the spear is the vector for the manticore-venom wound that triggers the entire downstream Dornish arc, and the shaft-snap moment is structurally distinct. But mark as lower-priority than A-1 and A-2.

---

## (B) EDGE PROPOSALS

### B-1
```
tywins-crossbow --[WIELDED_IN]--> assassination-of-tywin-lannister
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, line 259):**
  > "Tyrion's finger clenched. The crossbow whanged just as Lord Tywin started to rise. The bolt slammed into him above the groin and he sat back down with a grunt."
- **Line:** 259
- **Rationale:** Direct: the crossbow is the murder instrument; `WIELDED_IN` = artifact → event. Unambiguous.

---

### B-2
```
tyrion-lannister --[WIELDS]--> tywins-crossbow
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, line 211):**
  > "He climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot into the stirrup, and pushed down until the bowstring cocked. Then he slipped a bolt into the notch."
- **Line:** 211
- **Rationale:** `WIELDS` = person → artifact (active possession/use). Tyrion physically takes the crossbow, cocks it, and fires it.

---

### B-3
```
tywin-lannister --[KILLED_WITH]--> tywins-crossbow
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, line 259):**
  > "The bolt slammed into him above the groin and he sat back down with a grunt. The quarrel had sunk deep, right to the fletching."
- **Line:** 259
- **Rationale:** `KILLED_WITH` = victim → artifact (death by named weapon). Tywin is the victim of the crossbow bolt. Confirmed dead lines 267–269.

---

### B-4
```
hands-chain-of-office --[WIELDED_IN]--> tyrion-kills-shae-in-tywins-bed
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, line 209):**
  > "Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck."
- **Line:** 209
- **Rationale:** `WIELDED_IN` = artifact → event. The chain is the strangulation instrument.

---

### B-5
```
tyrion-lannister --[WIELDS]--> hands-chain-of-office
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, line 209):**
  > "Tyrion slid a hand under his father's chain, and twisted."
- **Line:** 209
- **Rationale:** `WIELDS` = person → artifact. Tyrion physically takes hold of the chain and uses it as a weapon.

---

### B-6
```
shae --[KILLED_WITH]--> hands-chain-of-office
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-11, lines 209–210):**
  > "Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck. 'For hands of gold are always cold, but a woman's hands are warm,' he said. He gave cold hands another twist as the warm ones beat away his tears."
- **Line:** 209–210
- **Rationale:** `KILLED_WITH` = victim → artifact. The chain is the weapon of Shae's death.

---

### B-7
```
oberyn-spear --[WIELDED_IN]--> gregor-confesses-and-kills-oberyn
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-10, line 239):**
  > "he screamed, as he drove the spear down with the whole weight of his body behind it. The crack of the ashwood shaft snapping was almost as sweet a sound as Cersei's wail of fury"
- **Line:** 239
- **Rationale:** `WIELDED_IN` = artifact → event. The spear is Oberyn's weapon throughout the trial-by-combat and is used to wound Gregor fatally (with manticore venom). The shaft-snap at the moment of the decisive thrust marks the end of the weapon's role.

---

### B-8
```
oberyn-martell --[WIELDS]--> oberyn-spear
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-10, line 119):**
  > "Daemon, my spear!" Ser Daemon tossed it to him, and the Red Viper snatched it from the air."
- **Line:** 119
- **Rationale:** `WIELDS` = person → artifact. Oberyn calls for the spear personally, catches it, and carries it into battle.

---

### B-9
```
manticore-venom --[WIELDED_IN]--> gregor-confesses-and-kills-oberyn
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-10, line 123–124):**
  > "When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison? Tyrion decided that he would sooner not know."
- **Line:** 123–124
- **Rationale:** `WIELDED_IN` = substance/concept → event. The poison on the spear is the mechanism by which Gregor receives his wound that will kill him slowly. The ASOS text only implies poison here (the identification as manticore venom comes from later chapters); Tier 1 is justified because the glistening substance is confirmed as the intended kill vector in AFFC/ADWD. Keep cite as is (this chapter) with a note that the identification is confirmed downstream.

---

### B-10
```
oberyn-martell --[POISONS]--> gregor-clegane
```
- **Tier:** 1
- **Evidence quote (asos-tyrion-10, line 233):**
  > "Prince Oberyn's spear flashed like lightning and found the gap in the heavy plate, the joint under the arm. The point punched through mail and boiled leather."
- **Line:** 233
- **Rationale:** `POISONS` = poisoner → poisoned. Oberyn deliberately coated his spear (the black glistening substance). The wound at the armpit joint delivers the venom. This edge captures intentionality; it is distinct from B-7 (artifact→event) and B-9 (substance→event).

---

### B-11
```
tyrion-lannister --[WIELDS]--> oberyn-spear
```
**REJECTED.** Tyrion never touches the spear. Self-reject.

---

### B-12
```
tywins-crossbow --[WIELDED_IN]--> tyrion-kills-shae-in-tywins-bed
```
**REJECTED.** The crossbow is taken from the wall *after* Shae is killed. The timeline in asos-tyrion-11 is: (1) Tyrion finds Shae, (2) strangles her with the chain, (3) then finds Tywin's dagger and takes the crossbow. The crossbow plays no role in Shae's death. Self-reject.

---

## (C) QUOTE-ATTACH PROPOSALS

### C-1 — `tywin-lannister` / `## Quotes` / The privy revelation
- **Node:** `tywin-lannister`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-11, line 267–269):**
  > "For once, his father did what Tyrion asked him. The proof was the sudden stench, as his bowels loosened in the moment of death. Well, he was in the right place for it, Tyrion thought. But the stink that filled the privy gave ample evidence that the oft-repeated jape about his father was just another lie.\n\nLord Tywin Lannister did not, in the end, shit gold."
- **Line:** 267–269
- **Rationale:** The single most famous line in the Tywin death scene. Load-bearing verbatim. Attach to `tywin-lannister` node quotes section; also applicable to `assassination-of-tywin-lannister` event node if it has a quotes section.

---

### C-2 — `tyrion-lannister` / `## Quotes` / The confession speech
- **Node:** `tyrion-lannister`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-09, lines 57–62):**
  > "'Guilty,' he said, 'so guilty. Is that what you wanted to hear?'\n\nLord Tywin said nothing. Mace Tyrell nodded. Prince Oberyn looked mildly disappointed. 'You admit you poisoned the king?'\n\n'Nothing of the sort,' said Tyrion. 'Of Joffrey's death I am innocent. I am guilty of a more monstrous crime.' He took a step toward his father. 'I was born. I lived. I am guilty of being a dwarf, I confess it. And no matter how many times my good father forgave me, I have persisted in my infamy.'"
- **Line:** 53–57 (asos-tyrion-09)
- **Rationale:** The "I am guilty of being a dwarf" speech is the thematic climax of the trial sequence. Load-bearing direct speech, contiguous block.

---

### C-3 — `tyrion-lannister` / `## Quotes` / The demand and curse
- **Node:** `tyrion-lannister`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-09, line 65):**
  > "'I did not do it. Yet now I wish I had.' He turned to face the hall, that sea of pale faces. 'I wish I had enough poison for you all. You make me sorry that I am not the monster you would have me be, yet there it is. I am innocent, but I will get no justice here. You leave me no choice but to appeal to the gods. I demand trial by battle.'"
- **Line:** 65 (asos-tyrion-09)
- **Rationale:** Companion to C-2. The demand-for-trial speech and the "monster" line are structurally paired with the "guilty of being a dwarf" speech; both attach to `tyrion-lannister`.

---

### C-4 — `gregor-clegane` / `## Quotes` / The confession during combat
- **Node:** `gregor-clegane`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-10, lines 246–247):**
  > "'Elia of Dorne,' they all heard Ser Gregor say, when they were close enough to kiss. His deep voice boomed within the helm. 'I killed her screaming whelp.' He thrust his free hand into Oberyn's unprotected face, pushing steel fingers into his eyes. 'Then I raped her.' Clegane slammed his fist into the Dornishman's mouth, making splinters of his teeth. 'Then I smashed her fucking head in. Like this.'"
- **Line:** 246–247 (asos-tyrion-10)
- **Rationale:** Gregor's confession is the narrative payload of the entire trial-by-combat scene and the culmination of the Dornish justice arc begun at AGOT. This verbatim quote should also attach to `murder-of-elia-martell-and-rhaegars-children` as evidence. Primary attach: `gregor-clegane`; secondary: the Elia murder event node.

---

### C-5 — `shae` / `## Quotes` / "My giant of Lannister" (betrayal)
- **Node:** `shae`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-09, line 39):**
  > "'Unspeakable things.' As the tears rolled slowly down that pretty face, no doubt every man in the hall wanted to take Shae in his arms and comfort her. 'With my mouth and . . . other parts, m'lord. All my parts. He used me every way there was, and . . . he used to make me tell him how big he was. My giant, I had to call him, my giant of Lannister.'"
- **Line:** 39 (asos-tyrion-09)
- **Rationale:** "My giant of Lannister" is the phrase that breaks Tyrion and triggers his confession speech — it recurs in asos-tyrion-11 (line 205) in the moment before he strangles her. It is the pivotal verbal object connecting betrayal → murder. Attach as verbatim to `shae` node.

---

### C-6 — `shae` / `## Quotes` / Last words before strangulation
- **Node:** `shae`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-11, line 205–207):**
  > "'More than anything,' she said, 'my giant of Lannister.'\n\nThat was the worst thing you could have said, sweetling."
- **Line:** 205–207 (asos-tyrion-11)
- **Rationale:** Her last spoken words, and the direct trigger for the strangulation. The interiority line that follows is Tyrion's POV, making this a clean contiguous block. Pair with C-5 across the two chapters.

---

### C-7 — `hands-chain-of-office` / `## Quotes` / The murder-song line
- **Node:** `hands-chain-of-office`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-11, lines 209–210):**
  > "Tyrion slid a hand under his father's chain, and twisted. The links tightened, digging into her neck. 'For hands of gold are always cold, but a woman's hands are warm,' he said."
- **Line:** 209–210 (asos-tyrion-11)
- **Rationale:** The line "For hands of gold are always cold, but a woman's hands are warm" is from the Symon Silver Tongue song Tyrion has been unable to forget. Reciting it at the moment of strangulation with the golden chain is the scene's central irony. Load-bearing verbatim for the artifact node.

---

### C-8 — `oberyn-martell` / `## Quotes` / Pre-combat declaration
- **Node:** `oberyn-martell`
- **Section:** `## Quotes`
- **Verbatim (asos-tyrion-10, line 171):**
  > "'I am going to kill that,' her lover replied carelessly."
- **Line:** 171 (asos-tyrion-10)
- **Rationale:** Oberyn's response to Ellaria ("You are going to fight that?") is a clean one-line character moment — confidence, brevity, foreshadowed reversal. Attach to `oberyn-martell`.

---

### C-9 — `murder-of-elia-martell-and-rhaegars-children` / `## Quotes` / Gregor's confession
- **Node:** `murder-of-elia-martell-and-rhaegars-children`
- **Section:** `## Quotes`
- **Verbatim:** (same as C-4 above — asos-tyrion-10, lines 246–247)
- **Rationale:** The Gregor confession quote should attach to both `gregor-clegane` (C-4) and `murder-of-elia-martell-and-rhaegars-children` as book-confirmatory evidence (vs. prior wiki/rumor tier). This is the only direct first-person admission in the text.

---

## SELF-REJECTED PROPOSALS

| Candidate | Reason |
|---|---|
| `tywins-dagger` as separate artifact | Tyrion takes "Lord Tywin's dagger" from the bedside table (asos-tyrion-11, line 211) and puts it in his belt, but it plays no active role in the events of this unit — he uses the crossbow, not the dagger. Quote-attach to Tyrion if relevant to a later unit, but no WIELDED_IN edge here. |
| `widow's-wail --[WIELDED_IN]--> assassination-of-tywin-lannister` | Widow's Wail is used to cut the wedding pie (asos-tyrion-08, line 265–279), not in the assassination. The scene establishes it's Joffrey's sword, not a murder weapon here. |
| `tyrion-lannister KILLED_WITH tywins-crossbow` | KILLED_WITH is victim→weapon. Tyrion is the killer, not the victim. Correct framing is B-3 (tywin-lannister KILLED_WITH tywins-crossbow). |
| `manticore-venom --[KILLED_WITH]--> gregor-clegane` | KILLED_WITH is for the immediate combat death weapon. Gregor's death from the venom is slow (confirmed in AFFC); the event where he "dies" is outside this unit's scope. Hold for later enrichment. |
| `oberyn-spear --[ANCESTRAL_WEAPON_OF]--> oberyn-martell` | ANCESTRAL_WEAPON_OF is for heritable house weapons (e.g., Ice). Oberyn's spear has no named lineage or inheritance. Wrong type. |
| `gregor-clegane AFFLICTED_BY manticore-venom` | Tempting. But gregor-confesses-and-kills-oberyn is the event node, not a separate affliction event. The POISONS edge (B-10) carries this meaning adequately within the locked vocab. A separate AFFLICTED_BY could be proposed for a dedicated `gregor-dying-of-manticore-venom` event node if one is minted, but that event falls outside this unit. |

---

## HARVEST

*Chapter:line / kind / note — POINT, don't extract*

- `asos-tyrion-08:133` / food / First wedding feast dish: "creamy soup of mushrooms and buttered snails, served in gilded bowls" — opening of the 77-course feast
- `asos-tyrion-08:145` / food / Second course: "pstry coffyn filled with pork, pine nuts, and eggs"
- `asos-tyrion-08:153` / food / "sweetcorn fritters and hot oatbread baked with bits of date, apple, and orange, and gnawed on the rib of a wild boar"
- `asos-tyrion-08:155` / food / "trout cooked in a crust of crushed almonds … roast herons and cheese-and-onion pies … crabs boiled in fiery eastern spices, trenchers filled with chunks of chopped mutton stewed in almond milk with carrots, raisins, and onions, and fish tarts fresh from the ovens"
- `asos-tyrion-08:157` / food / "honey-ginger partridge … Peacocks were served in their plumage, roasted whole and stuffed with dates"
- `asos-tyrion-08:171` / food / "bowls of blandissory, a mixture of beef broth and boiled wine sweetened with honey and dotted with blanched almonds and chunks of capon … buttered pease, chopped nuts, and slivers of swan poached in a sauce of saffron and peaches"
- `asos-tyrion-08:171` / food / "skewers of blood sausage … sizzling"
- `asos-tyrion-08:203` / food / "Roundels of elk stuffed with ripe blue cheese"
- `asos-tyrion-08:205` / food / "leche of brawn, spiced with cinnamon, cloves, sugar, and almond milk"
- `asos-tyrion-08:281` / food / "pigeon pie … a spoon of lemon cream" — the pie Joffrey eats from, death vessel
- `asos-tyrion-09:57` / food (prison) / "porridge and apples … a horn of ale" — Tyrion's breakfast before trial day 3
- `asos-tyrion-09:163` / food (prison) / "boiled eggs, burned bacon, and fried bread" — Tyrion's trial-day breakfast
- `asos-tyrion-09:319` / food (prison) / "porridge and honey" — morning of confession day; he flings the bowl
- `asos-tyrion-10:1` / food (prison) / cannot face food before combat day
- `asos-tyrion-10:101` / food (prison) / "fried bread, blood sausage, applecakes, and a double helping of eggs cooked with onions and fiery Dornish peppers" — pre-combat breakfast; Tyrion vomits this during the Mountain's killing of Oberyn (line 247)
- `asos-tyrion-10:247` / food (vomit) / what comes back up: "bacon and sausage and applecakes, and that double helping of fried eggs cooked up with onions and fiery Dornish peppers" — unusual instance of eaten food named in the vomit; dark-register harvest
- `asos-tyrion-10:79` / food (cell) / "cheese, bread, and olives" — Podrick sent to fetch after trial-by-combat demand
- `asos-tyrion-11:57` / logistics / Varys drugs the guards with sweetsleep in their wine — a use of a named substance for incapacitation (not a death)
- `asos-tyrion-11:145` / description / Varys describes all 4 dungeon levels in detail — rich physical description of Red Keep underground; relevant to any location enrichment of black-cells or dungeons
- `asos-tyrion-11:153` / description / The underground junction: mosaic of three-headed dragon in red and black tiles, ornate brazier fashioned as a dragon's head — physical description of the passage below Tower of the Hand
- `asos-tyrion-11:183` / description / Tyrion overhears guards Lum and Lester betting on how he'll die — character color, the everyday soldiers' view of Tyrion
- `asos-tyrion-11:211` / object / Tywin's bedchamber weapons: "A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls" — three weapons; the mace and poleaxe are not used but may be worth noting for any Tywin-personal-effects enrichment
- `asos-tyrion-11:259` / foreshadowing / "The bolt slammed into him above the groin" — Tywin killed by a crossbow bolt to the belly, echoing his life's irony (privy, golden words, mortality of powerful men); resonates with the shit-gold line
- `asos-tyrion-08:265–271` / object / `widow's-wail` used to cut the wedding pie — first named use of Joffrey's Valyrian steel sword in a mundane act; Sansa recognizes its provenance ("What has Ser Ilyn done with my father's sword?") — foreshadowing-adjacent, book-cite opportunity for widows-wail node
- `asos-tyrion-09:247` / object / Pycelle's poisons table at trial: greycap, nightshade, sweetsleep, demon's dance, blindeye, widow's blood, wolfsbane, basilisk venom, tears of Lys — all named but none is the strangler (the actual poison); rich pharmacopoeia for any `concept.medical` enrichment
- `asos-tyrion-09:251` / concept / "the strangler" named by Pycelle as the rare poison that kills by blocking breath — the actual murder weapon; if a `strangler-poison` concept node doesn't exist, this is the canonical naming scene
- `asos-tyrion-08:117` / hospitality / Lady Olenna offers Sansa an invitation to Highgarden ("perhaps you would like to accompany me for a little visit") — hospitality gesture, possibly significant (she has just poisoned Joffrey)
- `asos-tyrion-10:173` / description / Oberyn's armor for the trial-by-combat: "greaves, vambraces, gorget, spaulder, steel codpiece … supple leather and flowing silks … scales of gleaming copper … half-helm lacking even a nasal … round steel shield … sun-and-spear in red gold, yellow gold, white gold, and copper" — full armor description; attach to `oberyn-martell` physical description
- `asos-tyrion-10:167–168` / description / Mountain's armor: "heavy plate over chainmail … boiled leather and a layer of quilting … flat-topped greathelm … breaths around the mouth and nose … narrow slit for vision … crest atop it was a stone fist … a massive thing of heavy oak rimmed in black iron" for the shield — attach to `gregor-clegane` physical description
