# LENS 2 — Secondary-character sub-arcs + WITNESS_IN / SUSPECTED_OF substrate
## Unit: assassination-of-tywin-lannister (ASOS Tyrion VIII–XI)
## Session 139 enrichment pass, Lens 2

---

## PROPOSALS — Role edges onto event hubs

All deduped against 35 existing edges in baseline.md. No proposal duplicates an existing edge.

---

### 1. Trial judges: Mace Tyrell and Oberyn Martell as PARTICIPATES_IN

**mace-tyrell --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"He has asked Lord Tyrell and Prince Oberyn to sit in judgment with him."` (asos-tyrion-09.md:15)
- Rationale: Mace Tyrell is named as one of the three sitting judges at the trial — an administrative/judicial role that is PARTICIPATES_IN (non-combat logistical/administrative). The existing edge is `tywin-lannister AGENT_IN trial-of-tyrion-lannister` (Tywin as primary executor/convener); the other two judges take PARTICIPATES_IN as they co-preside but don't command.
- NEW-NODE: no

**oberyn-martell --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"He has asked Lord Tyrell and Prince Oberyn to sit in judgment with him."` (asos-tyrion-09.md:15)
- Rationale: Oberyn Martell named as co-judge alongside Tyrell. Same reasoning as Tyrell above — PARTICIPATES_IN for the judicial role.
- NEW-NODE: no

---

### 2. Kingsguard witnesses (Ser Balon Swann, Ser Meryn Trant, Ser Boros Blount, Ser Osmund Kettleblack) as WITNESS_IN the trial

These are the parade of witnesses who testify against Tyrion. They were voluntarily present at the trial to give formal sworn testimony — they ATTENDS as audience is the wrong frame; their function is testimony, which is the charged administrative/legal act inside the trial hub. PARTICIPATES_IN captures formal procedural participant; WITNESS_IN would require they *perceived* the original killing (they did not — they testify to prior conduct). They are trial-participants in their testimonial role.

**ser-balon-swann --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"The first man ushered in was Ser Balon Swann of the Kingsguard."` (asos-tyrion-09.md:191)
- Rationale: Balon Swann appears as a formal sworn witness — his participation is documented in the legal proceeding against Tyrion. PARTICIPATES_IN fits (formal procedural role in the trial). He did not witness the poisoning; he testifies to past conduct. WITNESS_IN does NOT apply here.
- NEW-NODE: **yes** — `ser-balon-swann` (character.knight, Kingsguard) — if not already in graph

**ser-meryn-trant --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"Ser Meryn Trant was pleased to expand on Ser Balon's account, when he took his place as witness."` (asos-tyrion-09.md:201)
- Rationale: Formally testifies at the trial. Same logic as Balon Swann.
- NEW-NODE: **yes** — `ser-meryn-trant` (character.knight, Kingsguard) — if not already in graph

**ser-boros-blount --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"Blount himself came next, to echo that sorry tale."` (asos-tyrion-09.md:207)
- Rationale: Formally testifies. PARTICIPATES_IN.
- NEW-NODE: **yes** — `ser-boros-blount` (character.knight, Kingsguard) — if not already in graph

**osmund-kettleblack --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"Ser Osmund Kettleblack, a vision of chivalry in immaculate scale armor and white wool cloak, swore that King Joffrey had long known that his uncle Tyrion meant to murder him."` (asos-tyrion-09.md:221)
- Rationale: Formal sworn testimony at the trial. Same as above.
- NEW-NODE: **yes** — `osmund-kettleblack` (character.knight, Kingsguard) — if not already in graph

---

### 3. Pycelle and Varys as PARTICIPATES_IN the trial (testimony roles)

**grand-maester-pycelle --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"Then they brought forth Grand Maester Pycelle, leaning heavily on a twisted cane and shaking as he walked"` (asos-tyrion-09.md:245)
- Rationale: Pycelle gives formal sworn expert testimony identifying poisons and accusing Tyrion of stealing them. Key participant.
- NEW-NODE: **yes** — `grand-maester-pycelle` (character.maester) — if not already in graph

**varys --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `'"Lord Varys," the herald said, "master of whisperers."'` (asos-tyrion-09.md:321)
- Rationale: Varys testifies in person at the trial with documentary evidence. Formal procedural participant. Note: Varys is already in the existing node list; this is a new edge only.
- NEW-NODE: no

---

### 4. Shae — PARTICIPATES_IN the trial (her testimony IS the spine trigger)

The baseline wires Shae as `VICTIM_IN tyrion-kills-shae-in-tywins-bed` and `VICTIM_IN tyrion-resolves-to-wed-shae-to-ser-tallad`. Her AGENT role in the trial as Cersei's final witness is not captured.

**shae --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"They plotted it together," she said, this girl he'd loved. "The Imp and Lady Sansa plotted it after the Young Wolf died."` (asos-tyrion-10.md:31)
- Rationale: Shae gives the climactic final testimony at the trial that breaks Tyrion's composure and triggers his demand for trial by combat. She is an active agent in the legal proceeding, not merely a victim. This completes her participation arc across this cluster.
- NEW-NODE: no

Note on WITNESS_IN for Shae: Shae did not witness the poisoning of Joffrey in any verified prose sense — her testimony is fabricated. WITNESS_IN (as a perceiver of a charged/violent event) does NOT apply to her trial role.

---

### 5. Cersei as COMMANDS_IN the trial (she orchestrates the witness parade)

The baseline has `cersei-lannister AGENT_IN tyrion-accused-of-poisoning-joffrey` and `cersei-lannister COMMANDS_IN gregor-confesses-and-kills-oberyn`. Her command role over the trial proceedings themselves (she assembled and directed all witnesses, and is named as their orchestrator) is not captured.

**cersei-lannister --[COMMANDS_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"'Have we heard it all?' Lord Tywin asked his daughter as Varys left the hall. 'Almost,' said Cersei. 'I beg your leave to bring one final witness before you, on the morrow.'"` (asos-tyrion-09.md:327–330)
- Rationale: Cersei explicitly controls the witness queue, determines who testifies, and saves Shae for last as her coup de grâce. She is the operational commander of the prosecution. COMMANDS_IN = orderer who didn't personally execute.
- NEW-NODE: no

---

### 6. Trial by combat (gregor-confesses-and-kills-oberyn): FIGHTS_IN edges

The existing edge `gregor-clegane AGENT_IN gregor-confesses-and-kills-oberyn` is correct for the AGENT of the death. But FIGHTS_IN is the appropriate edge for COMBATANTS in trial by combat (both participants). Gregor should also get FIGHTS_IN; Oberyn should get FIGHTS_IN (his VICTIM_IN already exists — same person can hold both).

**oberyn-martell --[FIGHTS_IN]--> gregor-confesses-and-kills-oberyn**
- Tier: 1
- Quote: `"He does, my lord." Prince Oberyn of Dorne rose to his feet. "The dwarf has quite convinced me."` (asos-tyrion-09.md:75 — Oberyn declares as champion); combat prose at asos-tyrion-10.md:183–247.
- Rationale: Oberyn voluntarily takes the field as Tyrion's champion and fights Gregor to the death. FIGHTS_IN = combatant. The existing `oberyn-martell VICTIM_IN gregor-confesses-and-kills-oberyn` captures the patient role; FIGHTS_IN captures the combatant role. One person, two edges, different slots.
- NEW-NODE: no

**gregor-clegane --[FIGHTS_IN]--> gregor-confesses-and-kills-oberyn**
- Tier: 1
- Quote: `"Cersei seemed half a child herself beside Ser Gregor. In his armor, the Mountain looked bigger than any man had any right to be."` (asos-tyrion-10.md:167)
- Rationale: Gregor fights as Cersei's champion. AGENT_IN already captures his executioner role; FIGHTS_IN adds the combatant dimension cleanly.
- NEW-NODE: no

---

### 7. Ellaria Sand — WITNESS_IN the death of Oberyn

WITNESS_IN gate applied strictly: does prose show Ellaria SEES the charged violent moment?

**ellaria-sand --[WITNESS_IN]--> gregor-confesses-and-kills-oberyn**
- Tier: 1
- Quote: `'"You are going to fight that?" Ellaria Sand said in a hushed voice.'` (asos-tyrion-10.md:169–170) and `'Ellaria Sand wailed in terror, and Tyrion's breakfast came boiling back up.'` (asos-tyrion-10.md:247)
- Rationale: Ellaria is physically present at the combat, speaks during it (line 203: "Oberyn is toying with him"), and the text records her wailing in terror at the moment Gregor crushes Oberyn's skull — confirming she perceives the charged violent moment. WITNESS_IN gate = PASS. This is not merely ATTENDS (she is a perceiver of the killing itself, not just the staged spectacle).
- NEW-NODE: no

---

### 8. Varys — AGENT_IN the escape (guiding Tyrion through the tunnels)

The existing edge `varys COMMANDS_IN jaime-frees-tyrion-from-the-black-cells` captures Varys's role in authorizing/enabling the jailbreak. But Varys is physically present and personally guides Tyrion through the fourth-level tunnels and sewers to the river — he is an active agent in the physical escape sequence, not just its commander.

There is no existing event hub for "the escape from King's Landing" as distinct from the jailbreak. The jailbreak event (`jaime-frees-tyrion-from-the-black-cells`) is located at the Black Cells. Varys's escort of Tyrion through the tunnels below the Tower of the Hand and out to the river is a distinct beat but may be sub-beat of the same escape.

**Assessment:** The escape through the tunnels is not a minted event hub yet. A mint candidate would be `tyrion-flees-kings-landing` (as signaled in baseline note: "a Varys-smuggles-Tyrion / Tyrion-flees-into-exile beat"). If that node is minted, Varys takes AGENT_IN. Without a hub, this edge cannot land. Flag for MINT-NODE proposals below.

---

### 9. Cersei — COMMANDS_IN the trial by combat (she selected Gregor as champion)

**cersei-lannister --[COMMANDS_IN]--> gregor-confesses-and-kills-oberyn**
- Already in baseline: `cersei-lannister COMMANDS_IN gregor-confesses-and-kills-oberyn` — **DEDUP. Skip.**

---

### 10. Osfryd Kettleblack and Osney Kettleblack as PARTICIPATES_IN the trial

**osfryd-kettleblack --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: `"The Kettleblacks came next, all three of them in turn. Osney and Osfryd told the tale of his supper with Cersei before the Battle of the Blackwater, and of the threats he'd made."` (asos-tyrion-09.md:217)
- Rationale: Both testify formally at the trial as part of Cersei's witness parade.
- NEW-NODE: **yes** — `osfryd-kettleblack` (character) — if not already in graph

**osney-kettleblack --[PARTICIPATES_IN]--> trial-of-tyrion-lannister**
- Tier: 1
- Quote: same as above (asos-tyrion-09.md:217–219: "Osney and Osfryd told the tale...")
- Rationale: Same as Osfryd.
- NEW-NODE: **yes** — `osney-kettleblack` (character) — if not already in graph

---

### 11. Tyrion — WITNESS_IN Shae's death / Tywin's death?

WITNESS_IN = perceiver of charged/violent event. Tyrion is AGENT_IN both deaths (he commits them). An AGENT cannot simultaneously be WITNESS_IN the same event — the subject IS the charged act; there is no separate perceiver slot for the perpetrator. **Self-rejected below.**

---

### 12. Jaime — AGENT_IN jaime-reveals-the-truth-of-tysha (already wired)

Already in baseline: `jaime-lannister AGENT_IN jaime-reveals-the-truth-of-tysha`. **DEDUP. Skip.**

---

### 13. Tywin — AGENT_IN jaime-reveals-the-truth-of-tysha (he commanded the lie and the punishment)

The reveal scene makes clear Tywin is the author of both the lie Jaime told and the original punishment of Tysha. He is the COMMANDS_IN figure for the Tysha deception that Jaime now discloses.

**tywin-lannister --[COMMANDS_IN]--> jaime-reveals-the-truth-of-tysha**
- Tier: 1
- Quote: `"That was a lie that Father commanded me to tell."` (asos-tyrion-11.md:79)
- Rationale: The revelation event is Jaime telling Tyrion the truth. Tywin commanded the original lie — making him the commander of the deception whose unraveling IS the event. COMMANDS_IN (orderer who didn't personally execute the revelation, but whose command created it) fits cleanly.
- NEW-NODE: no

---

### 14. Tysha — VICTIM_IN jaime-reveals-the-truth-of-tysha

The event "Jaime reveals the truth of Tysha" is about what was done to Tysha. She is the absent patient.

**tysha --[VICTIM_IN]--> jaime-reveals-the-truth-of-tysha**
- Tier: 1
- Quote: `"She was no whore. I never bought her for you. That was a lie that Father commanded me to tell. Tysha was . . . she was what she seemed to be. A crofter's daughter, chance met on the road."` (asos-tyrion-11.md:79–80)
- Rationale: The revelation event is the disclosure of what was done to Tysha (forced gang assault, false accusation). She is the victim of the underlying act that the revelation event discloses. VICTIM_IN captures her patient role in this event hub.
- NEW-NODE: no (tysha already in node list)

---

### 15. Tyrion — WITNESS_IN anything in ch.11?

Tyrion witnesses Shae in Tywin's bed (she is his) and then kills her — he is AGENT_IN. He witnesses Tywin in the privy and kills him — AGENT_IN. No distinct WITNESS_IN slot. The only thing Tyrion purely *perceives* without being the agent is: when he hears through the tunnel wall that guards are betting on how he'll die (asos-tyrion-11.md:183). That is not a charged violent event — it's casual speech. **No WITNESS_IN edge for Tyrion in this cluster.**

---

## MINT-NODE PROPOSALS

### A. `tyrion-escapes-kings-landing` (event.incident)

Baseline signals this: "a Varys-smuggles-Tyrion / Tyrion-flees-into-exile beat." The escape through the fourth-level tunnels and out to the river galley is narratively distinct from the jailbreak itself (`jaime-frees-tyrion-from-the-black-cells` = Black Cells; the tunnel escape = below Tower of the Hand, out to Blackwater Bay).

Proposed node: `tyrion-escapes-kings-landing`
- Type: event.incident
- Located: tunnels below red-keep / blackwater-bay (not inside the black cells)
- Agents: tyrion-lannister (AGENT_IN), varys (AGENT_IN — he physically leads and unlocks gates)
- Sub-beat of: assassination-of-tywin-lannister (or its causal chain)
- Enables: tyrion's exile; the cover-up collapses without this

If minted:
- `varys --[AGENT_IN]--> tyrion-escapes-kings-landing` (Tier 1: "Varys produced a key. They stepped through..." asos-tyrion-11.md:153)
- `tyrion-lannister --[AGENT_IN]--> tyrion-escapes-kings-landing` (Tier 1)
- `tyrion-escapes-kings-landing LOCATED_AT red-keep` (Tier 1)
- `jaime-frees-tyrion-from-the-black-cells CAUSES tyrion-escapes-kings-landing` (Tier 1: the jailbreak enables the escape)
- `assassination-of-tywin-lannister CAUSES tyrion-escapes-kings-landing` (Tier 1: Tyrion must flee after the killings)

### B. `hand-of-the-king-chain` (artifact)

Baseline: "The Hand's chain-of-office Shae is strangled with" — listed as no-node. It is the murder weapon in `tyrion-kills-shae-in-tywins-bed` and it is loaded with symbolic significance (the chain of office Tywin wore, now used as a weapon by Tyrion).

Proposed node: `hand-of-the-king-chain`
- Type: artifact.object
- Quote anchor: `"She sat up, letting the blanket slide down to her lap. Beneath it she was naked, but for the chain about her throat. A chain of linked golden hands, each holding the next."` (asos-tyrion-11.md:197)
- Edges if minted:
  - `tyrion-lannister --[KILLS]--> shae` + `EXECUTED_WITH hand-of-the-king-chain` (Tier 1)
  - `tyrion-kills-shae-in-tywins-bed EXECUTED_WITH hand-of-the-king-chain` — wait, EXECUTED_WITH takes person→person with weapon. The correct structure is edge `tyrion-lannister --[EXECUTED_WITH]--> shae` with instrument, or a prose evidence_quote on the kill event. Since no INSTRUMENT edge type exists in the locked vocab, the weapon is best captured as a node with prose/quote tied to the event, or as a `KILLS` edge with evidence_quote. Flag for architecture review.

### C. `tywin-crossbow` (artifact)

Baseline: "the crossbow Tywin is killed with" — listed as no-node.

Proposed node: `tywin-crossbow`
- Type: artifact.weapon
- Quote anchor: `"A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls... He climbed up, pulled down the bow and a leather quiver packed with quarrels, jammed a foot into the stirrup, and pushed down until the bowstring cocked."` (asos-tyrion-11.md:211)
- Additional: `"'Is that my crossbow? Put it down.'"` (asos-tyrion-11.md:225) — Tywin identifies it as his own crossbow.
- Located at: tower-of-the-hand (hung on the wall of what was Tyrion's bedchamber)
- Edges if minted:
  - `tywin-lannister --[OWNS]--> tywin-crossbow` (Tier 1: Tywin says "Is that my crossbow")
  - `tyrion-lannister --[WIELDS]--> tywin-crossbow` during assassination-of-tywin-lannister (Tier 1)
  - `tywin-crossbow WIELDED_IN assassination-of-tywin-lannister` (Tier 1)

### D. `oberyn-poisoned-spear` (artifact)

Baseline flags this. The spear is a named, described weapon central to the combat and to Oberyn's strategy. It carries manticore venom (already a node: `manticore-venom`).

Proposed node: `oberyn-poisoned-spear`
- Type: artifact.weapon
- Quote anchor: `"The spear was turned ash eight feet long, the shaft smooth, thick, and heavy. The last two feet of that was steel: a slender leaf-shaped spearhead narrowing to a wicked spike. The edges looked sharp enough to shave with. When Oberyn spun the haft between the palms of his hand, they glistened black. Oil? Or poison?"` (asos-tyrion-10.md:123)
- Edges if minted:
  - `oberyn-martell --[WIELDS]--> oberyn-poisoned-spear` (Tier 1)
  - `oberyn-poisoned-spear WIELDED_IN gregor-confesses-and-kills-oberyn` (Tier 1)
  - `oberyn-poisoned-spear --[AFFLICTED_BY]--> manticore-venom` — wait, AFFLICTED_BY takes living entities. Better: `manticore-venom` is applied to the spear. No clean vocab edge for "poison coats artifact." Flag for architecture. Prose evidence_quote on the gregor node captures the poison-wounding.

---

## SELF-REJECTED

1. **Tyrion WITNESS_IN gregor-confesses-and-kills-oberyn** — Tyrion SEES the combat, but his role in the event hub is VICTIM_IN (his life is on the line as the accused). He is the interested party, not purely a perceiver. Also, the trial is a public spectacle he is forced to witness — ATTENDS would be wrong (this isn't voluntary), and WITNESS_IN requires perceiving the *charged moment* (the killing). Tyrion does perceive it but his prior VICTIM_IN of the trial and his stakes in the combat make adding a WITNESS_IN slot redundant and muddying. Rejected — VICTIM_IN in the upstream trial is sufficient; no additional edge needed.

2. **Mace Tyrell WITNESS_IN gregor-confesses-and-kills-oberyn** — Tyrell is on the judicial platform during the combat. Prose does not confirm he witnesses the skull-crush specifically (the POV shifts entirely to Tyrion). He is present as a spectator/judge but the WITNESS_IN gate requires prose showing the character SEES the charged moment. Not confirmed. Rejected.

3. **Osmund Kettleblack AGENT_IN gregor-confesses-and-kills-oberyn** — Osmund brings Gregor his shield before the combat (asos-tyrion-10.md:181: "Ser Osmund Kettleblack brought Clegane his shield"). This is a logistical assist, not an AGENT_IN or PARTICIPATES_IN of the killing event itself. The shield delivery is too minor to warrant an edge on the death hub. Rejected.

4. **Margaery Tyrell WITNESS_IN death-of-joffrey-baratheon** — She is present when Joffrey collapses at the wedding feast (asos-tyrion-08.md:293: "Queen Margaery gasped"). This is in a different event hub (death-of-joffrey, not in scope for this unit). Rejected from scope.

5. **Tyrion WITNESS_IN tyrion-kills-shae-in-tywins-bed** — The perpetrator is not also the perceiver for WITNESS_IN. Rejected by definition.

6. **Shae SUSPECTED_OF tyrion-kills-shae-in-tywins-bed** — She is the victim, not an unproven agent. Rejected.

7. **Varys SUSPECTED_OF assassination-of-tywin-lannister** — Varys enables the escape but is not an unproven agent of the killing. The text is plain: Tyrion shoots Tywin. Varys had no foreknowledge of Tyrion's detour (he waited below). Rejected.

8. **Cersei SUSPECTED_OF trial-of-tyrion-lannister** — Cersei's role is AGENT/COMMANDS, not "suspected." The acts are proven in the text. SUSPECTED_OF is for unproven-but-load-bearing claims. Rejected.

9. **Oberyn Martell SUSPECTED_OF death-of-joffrey-baratheon** — Oberyn himself raises this possibility ("Who knows more of poison than the Red Viper of Dorne? … Who has better reason to want to keep the Tyrells far from the crown?"), asos-tyrion-09.md:379. This is a self-conscious deflection / irony in the text, not a genuine unresolved whodunit, as the series eventually resolves the true killers as Olenna Tyrell and Littlefinger. Adding SUSPECTED_OF here would be misleading and is not load-bearing for the arc. Rejected.

10. **High Septon PARTICIPATES_IN trial-of-tyrion-lannister** — The High Septon opens each day with a prayer (asos-tyrion-09.md:173: "The High Septon began with a prayer"). He is a ceremonial opener, not a substantive trial participant. Rejected as too peripheral.

11. **Stableboy VICTIM_IN gregor-confesses-and-kills-oberyn** — During the combat, Gregor accidentally kills a bystander stableboy (asos-tyrion-10.md:219: "The luckless stableboy behind him was not so quick. As his arm rose to protect his face, Gregor's sword took it off between elbow and shoulder"). The stableboy is incidental collateral death, unnamed, and not a node. The event hub is already named for Gregor's killing of Oberyn. A bystander death by a nameless NPC does not warrant node-minting or an edge to an existing hub. Rejected.

---

## HARVEST

### Food / drink

- asos-tyrion-08.md:133 / food / wedding feast first course: "a creamy soup of mushrooms and buttered snails, served in gilded bowls"
- asos-tyrion-08.md:145 / food / second course: "a pastry coffyn filled with pork, pine nuts, and eggs"
- asos-tyrion-08.md:153 / food / multiple courses during singers: "sweetcorn fritters and hot oatbread baked with bits of date, apple, and orange, and gnawed on the rib of a wild boar"
- asos-tyrion-08.md:155 / food / dense multi-dish passage: "trout cooked in a crust of crushed almonds," "roast herons and cheese-and-onion pies," "crabs boiled in fiery eastern spices, trenchers filled with chunks of chopped mutton stewed in almond milk with carrots, raisins, and onions, and fish tarts fresh from the ovens"
- asos-tyrion-08.md:157 / food / peacocks: "Peacocks were served in their plumage, roasted whole and stuffed with dates"
- asos-tyrion-08.md:171 / food / dense passage: "blandissory, a mixture of beef broth and boiled wine sweetened with honey and dotted with blanched almonds and chunks of capon," "buttered pease, chopped nuts, and slivers of swan poached in a sauce of saffron and peaches," "skewers of blood sausage"
- asos-tyrion-08.md:203 / food / elk course: "Roundels of elk stuffed with ripe blue cheese"
- asos-tyrion-08.md:205 / food / brawn: "Tyrion was toying with a leche of brawn, spiced with cinnamon, cloves, sugar, and almond milk"
- asos-tyrion-08.md:261 / food / pigeon pie: the great wedding pie, "Two yards across it was, crusty and golden brown" — doves inside (live)
- asos-tyrion-08.md:281 / food / "A serving man placed a slice of hot pigeon pie in front of Tyrion and covered it with a spoon of lemon cream"
- asos-tyrion-08.md:129 / drink / wedding chalice: "poured a whole flagon of dark Arbor red into the golden wedding chalice" — the murder weapon of Joffrey's death
- asos-tyrion-10.md:101 / food / last breakfast before battle: "fried bread, blood sausage, applecakes, and a double helping of eggs cooked with onions and fiery Dornish peppers" — Tyrion vomits this up when Oberyn dies (line 247: "his breakfast came boiling back up... bacon and sausage and applecakes, and that double helping of fried eggs cooked up with onions and fiery Dornish peppers")
- asos-tyrion-10.md:11 / food / opening: "Tyrion stabbed listlessly at a greasy grey sausage, wishing it were his sister" — grim register

### Grim / violence

- asos-tyrion-10.md:219 / violence / collateral kill: Gregor accidentally kills a stableboy bystander during the combat — decapitation by greatsword, arm severed first
- asos-tyrion-10.md:247 / violence / Oberyn's death: Gregor crushes Oberyn's skull with gauntleted fist after gouging his eyes and shattering his teeth — one of the series' most visceral deaths
- asos-tyrion-11.md:259 / violence / Tywin shot: "The bolt slammed into him above the groin and he sat back down with a grunt. The quarrel had sunk deep, right to the fletching. Blood seeped out around the shaft, dripping down into his pubic hair and over his bare thighs."
- asos-tyrion-11.md:267 / death detail / Tywin: "the sudden stench, as his bowels loosened in the moment of death" — pays off the "Tywin Lannister doesn't shit gold" jape; privy setting is deliberate

### Objects / descriptions

- asos-tyrion-10.md:123 / artifact / Oberyn's spear: full physical description — turned ash, 8 feet, leaf-shaped steel spearhead; shaft glistening black (oil or poison); quote-anchor available
- asos-tyrion-10.md:161 / artifact / Oberyn's helm: "a high golden helm with a copper disk mounted on the brow, the sun of Dorne. The visor had been removed" — effective half-helm
- asos-tyrion-10.md:167 / description / Gregor's armor: full battle kit — heavy plate over chainmail, boiled leather, quilting, flat-topped greathelm with stone fist crest; seven-pointed star painted over the Clegane dogs
- asos-tyrion-11.md:197 / artifact / Hand's chain: "A chain of linked golden hands, each holding the next" — full physical description; murder weapon for Shae
- asos-tyrion-11.md:211 / artifact / crossbow: "A lion-headed mace, a poleaxe, and a crossbow had been hung on the walls" — full inventory of weapons in Tywin's bedchamber
- asos-tyrion-11.md:153 / location detail / junction below Tower of the Hand: mosaic of three-headed dragon in red and black tiles; ornate dragon-head brazier; five iron-barred doors + ceiling rungs — the secret room Shae described to Tyrion when Varys first brought her to his bed

### Foreshadowing / thematic

- asos-tyrion-08.md:17–25 / foreshadowing / Tyrion's extended meditation on Joffrey's role in sending the catspaw assassin to kill Bran — connects Littlefinger's dagger to Joffrey; this is Tyrion working out the truth at the purple wedding
- asos-tyrion-09.md:387 / foreshadowing / Oberyn to Tyrion: "Your father may not live forever" — direct prophetic line just before the trial by combat that leads to Tywin's death
- asos-tyrion-10.md:79 / thematic / Tyrion reflects that by demanding trial by combat he has "kicked Lord Tywin's plans to splinters" and inflamed Highgarden vs Dorne regardless of outcome — shows political sophistication even at nadir
- asos-tyrion-11.md:267 / thematic / "Lord Tywin Lannister did not, in the end, shit gold" — payoff of the jape; Tywin dying on the privy is framed as a deflation of his entire mystique

### Character perception / voice

- asos-tyrion-09.md:395 / perception / Oberyn: "You look so very guilty that I am convinced of your innocence" — Oberyn's reading of Tyrion; perception-mapper fodder
- asos-tyrion-09.md:231 / voice / Oberyn to Cersei on Tyrion: "The day I fear a dwarf's wrath is the day I drown myself in a cask of red" — character voice line
- asos-tyrion-10.md:43 / perception / Tyrion: "I saved you all... I saved this vile city and all your worthless lives" — Tyrion's self-perception at moment of breakdown; key POV-perception edge
- asos-tyrion-11.md:119 / confession / Tyrion to Jaime: "Yes, I killed your vile son" — ambiguous; Tyrion may be lying to hurt Jaime after the Tysha reveal. This is NOT plain guilt — it is a moment of weaponized confession. Flag for theory-layer: is Tyrion telling the truth or inflicting pain?
