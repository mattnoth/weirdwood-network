# Lens A — spine + secondary sub-arcs — proposals

> Lens A: spine + secondary-character sub-arcs for the Battle of Castle Black (ASOS Wall defense).
> Source chapters read: asos-jon-05 through asos-jon-11.
> Internal edges deduped against: `internal-edges.txt` (180 edges).
> Date: 2026-06-26

---

## CRITICAL SCOPE CORRECTION (read before synthesis)

**"Grenn holds the inner gate" is an HBO show beat, not book canon.** In ASOS, Donal Noye leads
four unnamed volunteers (two crossbows, two spears) down into the gate tunnel — none named Grenn.
Grenn is atop the Wall rolling oil barrels throughout asos-jon-08. The book tunnel scene is
Noye + Mag only; Noye's four volunteers die unnamed. Do NOT mint a "grenn-holds-the-inner-gate"
node for book-canon graph work. The baseline flag for this beat was drawn from show lore.

**Jon does NOT personally kill Styr.** Styr's last appearance in asos-jon-07:181 is him standing
triumphant on the barricade pointing his weirwood spear at the gate. Then: "Wind and fire did the
rest... the whole lower third of the stair broke off, along with several tons of ice. That was the
last that Jon Snow saw of Styr, the Magnar of Thenn." Styr is killed by the fire/stair-collapse trap
(Jon and Noye's prepared burn), not by Jon in personal combat. The correct agent is the stair/fire
event; Jon COMMANDS_IN or is AGENT_IN the trap that kills him, not KILLS Styr directly.

---

## PROPOSED NODES

### Node 1
- slug: `death-of-ygritte`
  name: "Death of Ygritte"
  type: event.death
  containers: [north]
  description: Ygritte is struck by an arrow (black-shafted, white duck-feather fletched — not Jon's) during the Thenn assault on Castle Black and dies in Jon's arms beneath the Lord Commander's Tower.
  evidence_ref: asos-jon-07.md:189–205
  anchors_edges: E1, E2, E3, E4, E5

### Node 2
- slug: `noye-kills-mag-in-the-tunnel`
  name: "Noye and Mag Kill Each Other in the Tunnel"
  type: event.death
  containers: [north]
  description: Donal Noye and four volunteers hold the gate tunnel against the giant Mag the Mighty; Mag tears the iron grate apart and kills the defenders; Noye drives his sword into Mag's throat, killing them both — mutual death in the tunnel.
  evidence_ref: asos-jon-08.md:165–171
  anchors_edges: E6, E7, E8, E9, E10

### Node 3
- slug: `southern-thenn-assault-on-castle-black`
  name: "Southern Thenn Assault on Castle Black"
  type: event.battle
  containers: [north]
  description: Styr's Thenn force (roughly 120 men) attacks Castle Black from the south via the kingsroad, storms the crescent barricade, fights up the switchback stair, and is destroyed when Noye's prepared oil-and-fire trap collapses the lower stair, killing Styr and ~20 Thenns.
  evidence_ref: asos-jon-07.md:137–181
  anchors_edges: E11, E12, E13, E14, E15, E16, E17, E18

### Node 4
- slug: `styr-death-on-the-stair`
  name: "Death of Styr on the Burning Stair"
  type: event.death
  containers: [north]
  description: Styr the Magnar of Thenn is killed when the fire trap Noye and Jon prepared collapses the lower third of the Wall stair along with several tons of ice; Jon's last sight of Styr is him trapped between two fires as the stair gives way.
  evidence_ref: asos-jon-07.md:181
  anchors_edges: E15, E16, E19, E20

### Node 5
- slug: `jon-takes-command-of-the-wall`
  name: "Jon Snow Takes Command of the Wall"
  type: event.incident
  containers: [north]
  description: When Donal Noye leads his volunteers down to hold the tunnel, he formally hands Jon command of the Wall ("The Wall is yours"), making Jon the de facto commander for the remainder of the battle.
  evidence_ref: asos-jon-08.md:77–83
  anchors_edges: E21, E22, E23

### Node 6
- slug: `jon-sortie-to-mance-camp`
  name: "Jon's Assassination Sortie to Mance's Camp"
  type: event.incident
  containers: [north]
  description: Released from the ice cell by Janos Slynt and Ser Alliser Thorne under the pretext of delivering a parley offer, Jon is actually sent to kill Mance Rayder; the sortie ends when Stannis's cavalry charge reaches the camp before Jon can act.
  evidence_ref: asos-jon-10.md:53–57
  anchors_edges: E24, E25, E26, E27

### Node 7
- slug: `aemon-scarecrow-sentinels-ruse`
  name: "Maester Aemon's Scarecrow Sentinels Ruse"
  type: event.incident
  containers: [north]
  description: Maester Aemon devises the scheme of dressing straw dummies in black cloaks and positioning them with spears and crossbows on every tower top and window to deceive the approaching Thenns about the garrison's strength.
  evidence_ref: asos-jon-07.md:33–35
  anchors_edges: E28, E29

### Node 8
- slug: `bowen-marsh-marches-garrison-away`
  name: "Bowen Marsh Marches the Garrison Away from Castle Black"
  type: event.incident
  containers: [north]
  description: Bowen Marsh leads Castle Black's main garrison away to respond to Mance's feints along the Wall (Harma at Woodswatch, Rattleshirt at Long Barrow, the Weeper at Icemark), leaving only cripples, elderly, and green boys to defend the castle — the enabling condition for the Thenn assault to threaten Castle Black.
  evidence_ref: asos-jon-06.md:49–51
  anchors_edges: E30, E31

---

## PROPOSED EDGES

### Ygritte's death (Node 1)

**E1**
- source_slug | EDGE_TYPE | target_slug | tier | evidence_ref | quote | rationale | status
- `ygritte` | VICTIM_IN | `death-of-ygritte` | tier=1 | asos-jon-07.md:189 | "He found Ygritte sprawled across a patch of old snow beneath the Lord Commander's Tower, with an arrow between her breasts." | Ygritte is the death victim. | status=NEW

**E2**
- `jon-snow` | WITNESS_IN | `death-of-ygritte` | tier=1 | asos-jon-07.md:193 | "When he knelt in the snow beside her, her eyes opened. "Jon Snow," she said, very softly." | Jon is the sole load-bearing witness; the scene is filtered through his POV and he holds her as she dies. | status=NEW

**E3**
- `death-of-ygritte` | SUB_BEAT_OF | `attack-on-castle-black` | tier=1 | asos-jon-07.md:189 | "He found Ygritte sprawled across a patch of old snow beneath the Lord Commander's Tower, with an arrow between her breasts." | Ygritte dies during the southern Thenn assault, a sub-beat of the main battle. | status=NEW

**E4**
- `southern-thenn-assault-on-castle-black` | CAUSES | `death-of-ygritte` | tier=2 | asos-jon-07.md:189 | "He found Ygritte sprawled across a patch of old snow beneath the Lord Commander's Tower, with an arrow between her breasts." | The assault on Castle Black is the direct causal context of her death. | status=NEW

**E5 — UNCERTAIN / LOW-CONFIDENCE — attacker unknown**
- Attacker of Ygritte: The arrow is "black" (Night's Watch fletching is grey goose feathers, not black — but Jon's arrows have "black shaft, grey fletching"). The text says: "The arrow was black, Jon saw, but it was fletched with white duck feathers. Not mine, he told himself, not one of mine." This narrows it to a Watch brother (black shaft) but with non-standard white duck fletching, OR possibly a wildling. Identity unknown. Do NOT mint an AGENT_IN or KILLS edge for an attacker. Jon confirms "My brother" to Tormund (asos-jon-10.md:107) — meaning a Night's Watch brother, not identified. Flag this as an open attribution question in the node prose. No edge proposed for attacker.

> SUSPECTED_OF note: Jon in asos-jon-10:107 says "My brother" when Tormund asks if he killed her — he doesn't know which one. A `SUSPECTED_OF` edge with a generic `nights-watch` source would be speculative beyond what the text supports. Recommend: node prose only.

---

### Tunnel fight / Noye-Mag mutual death (Node 2)

**E6**
- `donal-noye` | AGENT_IN | `noye-kills-mag-in-the-tunnel` | tier=1 | asos-jon-08.md:171 | "Noye's sword was sunk deep in the giant's throat, halfway to the hilt." | Noye is the primary agent — the one who kills Mag. | status=NEW

**E7**
- `mag-mar-tun-doh-weg` | AGENT_IN | `noye-kills-mag-in-the-tunnel` | tier=1 | asos-jon-08.md:167 | "Still the giant found the strength to reach through, twist the head off Spotted Pate, seize the iron gate, and wrench the bars apart." | Mag is also an agent — he broke through and killed the defenders. | status=NEW

**E8**
- `donal-noye` | VICTIM_IN | `noye-kills-mag-in-the-tunnel` | tier=1 | asos-jon-08.md:171 | "The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child." | Noye is killed — victim in the same event. | status=NEW

**E9**
- `mag-mar-tun-doh-weg` | VICTIM_IN | `noye-kills-mag-in-the-tunnel` | tier=1 | asos-jon-08.md:171 | "Noye's sword was sunk deep in the giant's throat, halfway to the hilt." | Mag is killed — victim in the same event. | status=NEW

**E10**
- `noye-kills-mag-in-the-tunnel` | SUB_BEAT_OF | `attack-on-castle-black` | tier=1 | asos-jon-08.md:165 | "The last twenty feet of the tunnel was where they'd fought and died." | The tunnel mutual death is a sub-beat of the main battle hub. | status=NEW

**E10b — DEDUP CHECK** — the existing dyad edges `donal-noye KILLS mag-mar-tun-doh-weg` and `mag-mar-tun-doh-weg KILLS donal-noye` both exist (internal-edges.txt lines 25, 114). These are CHARACTER→CHARACTER dyads. E6–E9 above are CHARACTER→EVENT role edges and are genuinely new — they are NOT duplicating the dyad kill edges.

---

### Southern Thenn assault (Node 3) and Styr's death (Node 4)

**E11**
- `southern-thenn-assault-on-castle-black` | SUB_BEAT_OF | `attack-on-castle-black` | tier=1 | asos-jon-07.md:137 | "Fifty of them were pounding up the kingsroad in tight column, their shields held up above their heads. Others were swarming through the vegetable garden, across the flagstone yard, around the old dry well." | The Thenn attack from the south is explicitly a sub-beat of the main battle. | status=NEW

**E12**
- `styr` | COMMANDS_IN | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:171 | "The Magnar was climbing up the barricade... In his hand was a long weirwood spear with an ornate bronze head. When he saw the gate, he pointed the spear at it and barked something in the Old Tongue to the half-dozen Thenns around him." | Styr commands the southern assault. | status=NEW

**E13**
- `jon-snow` | AGENT_IN | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:141 | "We kill them," Jon shouted back, a black arrow in his hand." | Jon directs the defense from the King's Tower roof against the barricade assault. | status=NEW

**E14**
- `satin` | AGENT_IN | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:145 | "Together they snatched up the thick quilted pads they'd left beside the fire, lifted the heavy kettle of boiling oil, and dumped it down the hole on the Thenns below." | Satin actively participates — pouring boiling oil, firing crossbow, throwing torches. | status=NEW

**E15**
- `styr` | VICTIM_IN | `styr-death-on-the-stair` | tier=1 | asos-jon-07.md:181 | "That was the last that Jon Snow saw of Styr, the Magnar of Thenn. The Wall defends itself, he thought." | Styr dies in the fire/stair collapse. | status=NEW

**E16**
- `styr-death-on-the-stair` | SUB_BEAT_OF | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:181 | "With flames below and flames above, the wildlings had nowhere to go... the whole lower third of the stair broke off, along with several tons of ice." | Styr's death is the climax of the southern assault. | status=NEW

**E17**
- `jon-snow` | COMMANDS_IN | `styr-death-on-the-stair` | tier=2 | asos-jon-07.md:175–177 | "Jon notched a fire arrow to his bowstring, and Satin lit it from the torch. He stepped to the parapet, drew, aimed, loosed... Not Styr. The steps." | Jon ordered and executed the fire trap that killed Styr; he is commander/architect of the trap but did not personally kill Styr. | status=NEW

**E18**
- `satin` | AGENT_IN | `styr-death-on-the-stair` | tier=2 | asos-jon-07.md:175 | "Jon notched a fire arrow to his bowstring, and Satin lit it from the torch." | Satin lit the fire arrows that ignited the oil-and-tinder trap; participates in the fatal trap. | status=NEW

**E19**
- `donal-noye` | COMMANDS_IN | `styr-death-on-the-stair` | tier=2 | asos-jon-07.md:179 | "the old wooden steps had drunk up oil like a sponge, and Donal Noye had drenched them from the ninth landing all the way down to the seventh." | Noye pre-positioned the oil on the stair — he prepared the fatal trap. | status=NEW

**E20**
- `longclaw` | WIELDED_IN | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:143 | "Jon dropped his bow, reached back over his shoulder, ripped Longclaw from its sheath, and buried the blade in the middle of the first head to pop out of the tower." | Jon uses Longclaw to kill the Thenn who breaks through the King's Tower trapdoor. | status=NEW

---

### Jon takes command (Node 5)

**E21**
- `jon-snow` | AGENT_IN | `jon-takes-command-of-the-wall` | tier=1 | asos-jon-08.md:83 | ""Aye," he managed." | Jon accepts command when Noye hands him the Wall before descending to the tunnel. | status=NEW

**E22**
- `donal-noye` | COMMANDS_IN | `jon-takes-command-of-the-wall` | tier=1 | asos-jon-08.md:77–81 | ""Jon, you have the Wall till I return." ... "Lord? I'm a blacksmith. I said, the Wall is yours."" | Noye formally transfers command to Jon. | status=NEW

**E23**
- `jon-takes-command-of-the-wall` | SUB_BEAT_OF | `attack-on-castle-black` | tier=1 | asos-jon-08.md:77 | ""I need two bows and two spears to help me hold the tunnel if they break the gate." More than ten stepped forward, and the smith picked his four. "Jon, you have the Wall till I return."" | The command transfer is a sub-beat of the battle. | status=NEW

**E23b — SECONDARY**: Maester Aemon also formally urges Jon to take permanent command after the battle (asos-jon-08.md:191: "You must lead"), but this is a SECOND command-transfer beat at the end of the battle — distinct from E21–E23 which happen mid-battle. The post-battle beat is already in Aemon's `PROTECTS jon-snow` (asos-jon-09.md:135) relationship. If the synthesizer wants to add a second command node for the post-battle transfer, it is warranted; flagged here as optional.

---

### Jon's sortie to Mance (Node 6)

**E24**
- `jon-snow` | AGENT_IN | `jon-sortie-to-mance-camp` | tier=1 | asos-jon-10.md:57 | "He started walking toward the wildling camp, past the body of a dead giant whose head had been crushed by a stone." | Jon walks to the camp, Longclaw at hand, intending to kill Mance. | status=NEW

**E25**
- `janos-slynt` | COMMANDS_IN | `jon-sortie-to-mance-camp` | tier=1 | asos-jon-10.md:53 | ""We're sending you to kill him." ... "We're sending you, Lord Snow." Ser Alliser smiled." | Slynt and Thorne order the sortie. | status=NEW

**E26**
- `alliser-thorne` | COMMANDS_IN | `jon-sortie-to-mance-camp` | tier=1 | asos-jon-10.md:53 | ""We're not sending you to talk with Mance Rayder," Ser Alliser said. "We're sending you to kill him."" | Thorne explicitly states the assassination mission. | status=NEW

**E27**
- `jon-sortie-to-mance-camp` | SUB_BEAT_OF | `attack-on-castle-black` | tier=2 | asos-jon-10.md:15 | "When he looked straight down past his feet, the ground was lost in shadow, as if he were being lowered into some bottomless pit." | The sortie is a late-battle beat of the Castle Black engagement (the night before Stannis arrives). | status=NEW

> NOTE: `mance-rayder` is the intended VICTIM_IN but the killing never occurs (Stannis arrives). The role edge `mance-rayder VICTIM_IN jon-sortie-to-mance-camp` would be tier=3 (planned but unrealized). Flagged for synthesizer: mint or note in prose only?

---

### Scarecrow sentinels ruse (Node 7)

**E28**
- `aemon-targaryen-son-of-maekar-i` | AGENT_IN | `aemon-scarecrow-sentinels-ruse` | tier=1 | asos-jon-07.md:35 | "Whatever you called them, the straw soldiers had been Maester Aemon's notion." | Aemon devises the ruse. | status=NEW

**E29**
- `aemon-scarecrow-sentinels-ruse` | SUB_BEAT_OF | `attack-on-castle-black` | tier=2 | asos-jon-07.md:33 | "Noye had placed them on every tower and in half the windows. Some were even clutching spears, or had crossbows cocked under their arms." | The ruse is a preparation beat of the same battle. | status=NEW

---

### Bowen Marsh marches garrison away (Node 8)

**E30**
- `bowen-marsh` | AGENT_IN | `bowen-marsh-marches-garrison-away` | tier=1 | asos-jon-06.md:49 | ""Everywhere. Harma Dogshead was seen at Woodswatch-by-the-Pool, Rattleshirt at Long Barrow, the Weeper near Icemark. All along the Wall ... but one glimpse of a black cloak and they're gone."" | Marsh responded to Mance's feints by dispersing the garrison. | status=NEW

**E31**
- `bowen-marsh-marches-garrison-away` | ENABLES | `attack-on-castle-black` | tier=2 | asos-jon-06.md:51 | ""Feints. Mance wants us to spread ourselves thin, don't you see?" And Bowen Marsh has obliged him. "The gate is here. The attack is here."" | The garrison's absence is the enabling condition Mance planned for; Jon names it explicitly. | status=NEW

---

### Causal upstream (gap fix)

**E32**
- `fight-at-the-fist` | ENABLES | `attack-on-castle-black` | tier=2 | asos-jon-08.md:55 | "We are the garrison, Jon told himself, and look at us. The brothers Bowen Marsh had left behind were old men, cripples, and green boys" | The Watch's combat strength was shattered at the Fist, leaving only the dregs — the explicit reason the garrison is so thin. | status=NEW

> NOTE: The existing edge `attack-on-castle-black CAUSES battle-beneath-the-wall` at tier=3 (asos-jon-08.md:55) has a weak quote. A stronger quote is asos-jon-10.md:287 ("STANNIS! Stannis! STANNIS!" as the cavalry charge arrives in response to the siege). The existing `stannis-moves-to-the-wall CAUSES battle-beneath-the-wall` [tier=2] is the cleaner chain. Recommend: leave the `attack → beneath` edge but upgrade its quote to asos-jon-09.md:57 context if worthwhile. Flagged, not a new edge proposal.

---

### Secondary character roles on existing nodes (no new nodes needed)

**E33**
- `pypar` | AGENT_IN | `night-battle-atop-the-wall` | tier=1 | asos-jon-08.md:59 | "Pyp ran down the line with a torch, setting them alight." | Pyp actively lights the oil jars during the night atop the Wall battle; already AGENT_IN mammoth/wildlings-gate beats, not the night-battle node. | status=NEW

**E34**
- `satin` | AGENT_IN | `night-battle-atop-the-wall` | tier=1 | asos-jon-08.md:73 | ""Here," said Satin." (responding to Noye's call for archers on the Wall top) | Satin is a named archer on the Wall top during the night battle. | status=NEW

**E35**
- `grenn` | AGENT_IN | `night-battle-atop-the-wall` | tier=1 | asos-jon-08.md:113 | ""NO!" Grenn shouted." | Grenn is explicitly present and vocal on the Wall during the night battle against Mance's main host. | status=NEW

**E36**
- `aemon-targaryen-son-of-maekar-i` | AGENT_IN | `attack-on-castle-black` | tier=2 | asos-jon-07.md:95 | "Maester Aemon had sent a lot of birds... Wildlings at the gate, the message ran. The realm in danger. Send all the help you can to Castle Black." | Aemon's ravens to 25+ northern lords is a significant battle-prep action — participant in the broader event. PARTICIPATES_IN is also valid; I prefer AGENT_IN as Aemon takes decisive action. | status=NEW

**E37**
- `aemon-targaryen-son-of-maekar-i` | PARTICIPATES_IN | `aemon-scarecrow-sentinels-ruse` | tier=1 | asos-jon-07.md:35 | "the straw soldiers had been Maester Aemon's notion. They had more breeches and jerkins and tunics in the storerooms than they'd had men to fill them, so why not stuff some with straw" | Aemon actively participates in executing the ruse (his idea, his logic). Prefer AGENT_IN (E28 covers this). This is a duplicate of E28 in different type. Synthesizer choose AGENT_IN or PARTICIPATES_IN but NOT both. | status=DEFER-TO-SYNTHESIZER

**E38**
- `deaf-dick-follard` | AGENT_IN | `southern-thenn-assault-on-castle-black` | tier=1 | asos-jon-07.md:127 | "He heard the deep thrum of Deaf Dick's crossbow to his left" | Dick is shooting a crossbow during the southern assault from the King's Tower roof. | status=NEW

> DEDUP CHECK for existing edges reviewed:
> - `donal-noye COMMANDS_IN night-battle-atop-the-wall` EXISTS (line 23 internal-edges) — E33/E34/E35 are role edges for *other* characters on same node, not duplicates.
> - `pypar AGENT_IN wildlings-attack-the-gate` EXISTS and `pypar AGENT_IN mammoth-attacks-gate-below` EXISTS (lines 135–136) — E33 is for `night-battle-atop-the-wall` which is a distinct node; NOT a dup.
> - `satin SERVES jon-snow` EXISTS (line 148) — E14/E34 are AGENT_IN event nodes; NOT dups of SERVES.
> - `grenn AGENT_IN mammoth-attacks-gate-below` and `grenn AGENT_IN wildlings-attack-the-gate` both EXIST (lines 40–41) — E35 adds to `night-battle-atop-the-wall`, distinct; NOT a dup.

---

## NOTES / UNCERTAINTIES

### 1. Jon does not kill Styr (CRITICAL)
The baseline states "jon KILLS styr is ABSENT (verify in-text who kills Styr)" — verified: Jon does not kill Styr. The Wall (stair collapse / fire trap) kills Styr. The correct graph representation is:
- Jon COMMANDS_IN styr-death-on-the-stair (he ordered/executed the trap)
- styr VICTIM_IN styr-death-on-the-stair
- NO `jon-snow KILLS styr` edge should be minted for the books. Jon's prayer "Give me Styr" goes unanswered — the Wall took him.

### 2. Grenn holds the inner gate — show, not book
The "Grenn holds the inner gate against the giant" beat is HBO Season 4. In ASOS, Noye's four tunnel volunteers are unnamed. Grenn is atop the Wall throughout asos-jon-08. A node for this beat would be show-canon contamination and should not be minted for the book graph.

### 3. Ygritte's attacker is deliberately unknown
Jon confirms to Tormund "My brother" (asos-jon-10.md:107) — meaning a Night's Watch brother, not himself, but not identified. The arrow's description (black shaft, white duck-feather fletching) is non-standard for both the Watch (grey goose) and the Thenns (not using Watch arrows). No attacker edge should be minted. Node prose should note the ambiguity.

### 4. Janos Slynt / Alliser Thorne roles
Both are present at Castle Black during the days following the battle (asos-jon-09). They arrest Jon, interrogate him, and send him on the sortie. They are NOT present during the battle itself — they arrive from Eastwatch after the fighting. Their roles attach to `jon-sortie-to-mance-camp` (E25, E26) but NOT to `attack-on-castle-black` directly.

### 5. Queenscrown triple-dup consolidation
The three nodes `ygritte-kills-the-old-man`, `styr-orders-jon-to-kill-the-old-man`, `jon-refuses-to-kill` are three nodes for one scene (asos-jon-05). The baseline flags this as a consolidation candidate. Not proposing new edges here — flagging for the synthesizer as structural surgery requiring fresh-verify.

### 6. fight-at-the-fist possible duplicate
The baseline notes `fight-at-the-fist` vs `battle-of-the-fist-of-the-first-men` may be a duplicate. E32 uses `fight-at-the-fist` as it is the slug that appears in internal-edges.txt (line 39: `great-ranging CAUSES fight-at-the-fist`). Synthesizer should verify slug before minting E32.

### 7. Jon's post-battle command + Aemon's urging
asos-jon-08.md:191: "You must lead... The Wall is yours, Jon Snow." — this is Aemon formally telling Jon to take PERMANENT command after Noye's death. This is distinct from the mid-battle hand-off (Node 5). A second event node `aemon-urges-jon-to-command` is a borderline call — the existing `aemon-targaryen PROTECTS jon-snow` edge (asos-jon-09.md:135) partially covers this. Synthesizer decides whether to mint.

### 8. Stannis's relief charge
The `battle-beneath-the-wall` node already exists with good edge wiring. No new nodes proposed for the Stannis charge itself. The one gap is that Stannis's personal AGENT_IN role on that node should be checked — `stannis-baratheon AGENT_IN stannis-moves-to-the-wall` EXISTS (line 149 internal-edges) but I did NOT see `stannis-baratheon AGENT_IN battle-beneath-the-wall` (he led the charge in person). Flagged for a targeted check rather than proposing here.

---

## HARVEST

- asos-jon-07.md:73–81 / food / Owen brings buns with raisins, pine nuts, dried apple, a wheel of cheese, and a bag of onions to the King's Tower roof — last-meal register before the assault; Dick eats immediately, Satin refuses (too scared); Jon tells Satin "Eat, there's no knowing when you'll have another chance." Classic siege pre-battle food scene.
- asos-jon-07.md:101 / food / Near evenfall Owen brings a loaf of black bread and "a pail of Hobb's best mutton, cooked in a thick broth of ale and onions" — they eat every bit including using bread to wipe the pail. Good domestic-warmth-before-the-storm register.
- asos-jon-07.md:181 / physical description / "That was the last that Jon Snow saw of Styr, the Magnar of Thenn. The Wall defends itself." — haunting close on the battle's most vivid villain, dying off-page.
- asos-jon-07.md:189 / physical description / "The ice crystals had settled over her face, and in the moonlight it looked as though she wore a glittering silver mask." — Ygritte's death image; load-bearing visual.
- asos-jon-07.md:205 / quote / ""You know nothing, Jon Snow," she sighed, dying." — Ygritte's last words; the novel's most iconic recurring phrase at its most load-bearing; must attach to death-of-ygritte node as evidence_quote.
- asos-jon-08.md:25–26 / food / Clydas brings "cups of hot mulled wine" while they wait for the cage; Hobb passes out "chunks of black bread" — Jon gnaws a heel; quiet before the northern assault.
- asos-jon-08.md:85 / food / "Hobb rode up the chain with cups of onion broth, and Owen and Clydas served them to the archers where they stood, so they could gulp them down between arrows." — Hobb serving food on the Wall during the actual fight; hospitality-under-fire.
- asos-jon-08.md:171 / quote / "Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child." — Noye/Mag mutual death visual; load-bearing for death-of-noye/mag node.
- asos-jon-09.md:51 / food / Jon makes himself eat — "bread, bacon, onions, and cheese" — knowing it "might be my last meal" before the turtle assault; siege-starvation register (they are running out of everything).
- asos-jon-09.md:47 / logistics / "Their oil was all but gone, and the last barrel of pitch had been rolled off the Wall two nights ago. They would soon run short of arrows as well, and there were no fletchers making more." — siege logistics / starvation of supplies.
- asos-jon-10.md:85–87 / hospitality / Tormund hands Jon his mead skin in no-man's-land: "To Donal Noye, and Mag the Mighty" — both drink to the fallen enemies; cross-faction toast; hospitality in extremis.
- asos-jon-07.md:63 / hospitality / "Three-Finger Hobb suddenly had more spit boys, kettle stirrers, and onion choppers than he knew what to do with" — Mole's Town refugees integrated into castle kitchen; wartime domestic economy.
- asos-jon-07.md:189–191 / foreshadowing / "The arrow was black... but it was fletched with white duck feathers. Not mine, he told himself, not one of mine." — the unknown Night's Watch archer who killed Ygritte; deliberate non-resolution.
- asos-jon-08.md:165 / physical description / "It was all Jon could do to keep up with Maester Aemon. The ice pressed close around them, and he could feel the cold seeping into his bones, the weight of the Wall above his head. It felt like walking down the gullet of an ice dragon." — the tunnel description; striking simile.
- asos-jon-11.md:39 / quote / Jon to Stannis: "Donal Noye held the gate. He died below in the tunnel, fighting the king of the giants." — Jon explicitly attributes holding the gate to Noye; key attribution quote for noye-kills-mag-in-the-tunnel node.
