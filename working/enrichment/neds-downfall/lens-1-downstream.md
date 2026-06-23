# Lens 1 — Downstream-Causal / Consequence
## Ned's Downfall enrichment dip (S137)

PROPOSE-ONLY. Synthesizer mints survivors.

---

## PROPOSED EDGES

### E-01: ned-discovers-the-truth-of-joffrey-s-parentage MOTIVATES cersei-lannister (via the pre-arrest warning)

Already exists per baseline. **DO NOT re-propose.**

---

### E-02: ned-discovers-the-truth-of-joffrey-s-parentage ENABLES cersei-orders-ned-s-arrest

**Source → Target:** `ned-discovers-the-truth-of-joffrey-s-parentage` --ENABLES--> `cersei-orders-ned-s-arrest`

**Tier:** 2 (interpretive causal)

**Cite:** `sources/chapters/agot/agot-eddard-12.md:169`

**Verbatim quote:** `"When you play the game of thrones, you win or you die. There is no middle ground."`

**Justification:** The godswood confrontation is the moment Cersei learns Ned WILL go to Robert. His declaration ("I intend to lay the truth before him") is the direct precondition that forces her hand — without it, Cersei could wait. The discovery ENABLES the arrest by eliminating her option to do nothing. This is not a duplicate of the existing MOTIVATES edges (those route through Ned's or Cersei's agency as actors); this captures that the discovery is a structural *precondition* Cersei must respond to. The ENABLES semantic fits: it made the arrest possible by giving Cersei no choice of delay. Distinction from SUB_BEAT: the discovery and the arrest are separate events (different chapters, different days); this is a genuine forward-causal link, not a constitutive beat.

**Confidence:** HIGH — the "win or you die" line is Cersei's explicit statement that the game is now forced. Varys confirms in agot-eddard-15:111: "It was not wine that killed the king. It was your mercy" (= Ned warning Cersei rather than acting immediately = ENABLES the counter-move).

**Slug check:** Both slugs appear in baseline.md as existing nodes.

---

### E-03: varys-confirms-cersei-s-role-in-robert-s-death MOTIVATES eddard-stark (toward the confession)

**Source → Target:** `varys-confirms-cersei-s-role-in-robert-s-death` --MOTIVATES--> `eddard-stark`

**Tier:** 2 (interpretive causal)

**Cite:** `sources/chapters/agot/agot-eddard-15.md:147`

**Verbatim quote:** `"Pity." The eunuch stood. "And your daughter's life, my lord? How precious is that?"`

**Justification:** Varys's visit to the black cells accomplishes two things: (1) he confirms Cersei's guilt (the wineskins via Lancel) and (2) he presents the lever — Sansa's life — that ultimately breaks Ned's resistance and produces the confession. The visit as a whole is what MOTIVATES Ned's eventual decision to confess. The 0-out-edge state of `varys-confirms-cersei-s-role-in-robert-s-death` makes this a real causal island. This is a MOTIVATES (routes agency through Ned's decision) not a CAUSES.

**Confidence:** HIGH — the chapter is entirely about Varys convincing Ned; his capitulation to the confession follows directly and the Sansa threat is the explicit hinge.

**Slug check:** `varys-confirms-cersei-s-role-in-robert-s-death` and `eddard-stark` in baseline/graph. `ned-confesses-to-treason` exists per baseline.

---

### E-04: varys-confirms-cersei-s-role-in-robert-s-death ENABLES ned-confesses-to-treason

**Source → Target:** `varys-confirms-cersei-s-role-in-robert-s-death` --ENABLES--> `ned-confesses-to-treason`

**Tier:** 2 (interpretive causal)

**Cite:** `sources/chapters/agot/agot-eddard-15.md:135`

**Verbatim quote:** `"Tell the queen that you will confess your vile treason, command your son to lay down his sword, and proclaim Joffrey as the true heir."`

**Justification:** Varys explicitly proposes the confession mechanism during this visit. Without the visit Ned would have had no offer on the table and no knowledge that a confession-for-clemency bargain was even available. The visit structurally ENABLES the confession event by delivering the terms. Complements E-03: E-03 captures Ned's motivational response (Sansa threat → his agency), E-04 captures the structural precondition (Varys delivers the pathway). Both are needed; they are not redundant.

**Confidence:** HIGH — the text is direct. Varys lays out the terms; the confession follows.

**Slug check:** Both slugs exist in baseline.

---

### E-05: execution-of-eddard-stark CAUSES sansa-stark-held-hostage-in-kings-landing

**Source → Target:** `execution-of-eddard-stark` --CAUSES--> `sansa-stark-held-hostage-in-kings-landing`

**Tier:** 1 (verified canon event-state)

**Cite:** `sources/chapters/agot/agot-sansa-06.md:39`

**Verbatim quote:** `"I did as the queen asked, I wrote the letters, I wrote what she told me. You promised you'd be merciful. Please, let me go home. I won't do any treason, I'll be good, I swear it, I don't have traitor's blood, I don't. I only want to go home."`

**Justification:** Sansa's capture/hostage status crystallizes after the execution. Pre-execution she was a ward whose marriage was under negotiation; post-execution Cersei explicitly retains her as a political tool ("Mother says I'm still to marry you, so you'll stay here, and you'll obey" — agot-sansa-06:41). The execution is what converts her from a willing guest to a hostage. This is a downstream CAUSES that is currently unwired.

**NEW NODE NEEDED:** `sansa-stark-held-hostage-in-kings-landing` does not appear in baseline.md's node list. It is a sustained state, not a single event — may warrant a note rather than an event node. Alternative: route through `sansa-stark` (character node) with an IMPRISONS edge. **Propose both paths; orchestrator decides.**

**Alt edge (avoids new node):** `cersei-orders-ned-s-arrest` --IMPRISONS--> `sansa-stark` (since the arrest is what first confines Sansa, and the execution locks it in). However this conflates timing. Prefer new node if schema allows sustained-state events.

**Confidence:** HIGH for the causal claim; LOW for the node shape (new node vs. IMPRISONS on existing character).

---

### E-06: execution-of-eddard-stark TRIGGERS robb-stark-calls-his-banners (or existing war-node)

**Source → Target:** `execution-of-eddard-stark` --TRIGGERS--> `war-of-the-five-kings`

**Tier:** 2 (interpretive causal)

**Cite:** `sources/chapters/agot/agot-eddard-15.md:123`

**Verbatim quote:** `"And now your son marches down the Neck with a northern host at his back."`

**Justification:** Baseline notes the execution already has `PART_OF war-of-the-five-kings` and `PRECEDES battle-on-the-green-fork`. The missing link is a TRIGGERS edge directly from the execution to the war (the execution is the proximate spark of open war, distinct from the arrest which was the predicate political crisis). Varys's line above is pre-execution (Robb has already marched in response to the arrest), which complicates the TRIGGERS claim — but the execution escalates the war from defensive march to declared rebellion (evidenced by Robb being proclaimed King in the North post-execution, already wired). So TRIGGERS on the escalation is defensible even though the march preceded the execution.

**Flag:** Baseline already has `PART_OF war-of-the-five-kings` on the execution node. A TRIGGERS edge would create a second causal link to the same war. This may be the cleaner path OR it may be redundant with PART_OF. **Orchestrator: check whether PART_OF and TRIGGERS serve different query purposes — lean toward keeping both if so (PART_OF = membership, TRIGGERS = causal spark).**

**Confidence:** LOW on the precise TRIGGERS framing (the war was already starting), HIGH on the causal significance.

---

### E-07: ned-discovers-the-truth-of-joffrey-s-parentage TRIGGERS ned-warns-cersei-in-the-godswood

**Note:** The godswood confrontation (Cersei "win or you die") appears to be a sub-beat of the discovery event rather than a separate minted node. If the graph has a node for the godswood confrontation specifically, a TRIGGERS edge from the discovery would clean up the causal chain. If it does NOT exist as its own node, this is a mint candidate.

**Mint candidate:** `ned-warns-cersei-in-the-godswood` (event.incident) — Ned reveals he knows the truth and warns Cersei to flee; Cersei delivers the "win or you die" line. This event sits causally between the discovery and the arrest, and is currently the missing middle of the chain.

**Proposed edges if minted:**
- `ned-discovers-the-truth-of-joffrey-s-parentage` --TRIGGERS--> `ned-warns-cersei-in-the-godswood`
- `ned-warns-cersei-in-the-godswood` --ENABLES--> `cersei-orders-ned-s-arrest`
- eddard-stark AGENT_IN `ned-warns-cersei-in-the-godswood`
- cersei-lannister AGENT_IN `ned-warns-cersei-in-the-godswood`
- LOCATED_AT godswood-of-the-red-keep (or kings-landing)

**Cite:** `sources/chapters/agot/agot-eddard-12.md:159`
**Verbatim quote:** `"For a start," said Ned, "I do not kill children. You would do well to listen, my lady. I shall say this only once. When the king returns from his hunt, I intend to lay the truth before him. You must be gone by then."`

**Confidence:** HIGH that this event is load-bearing and currently either uncaptured or underlinked. Flagging for orchestrator to check whether a node exists.

**Slug check:** `ned-discovers-the-truth-of-joffrey-s-parentage` is in baseline. The godswood confrontation node is NOT listed in baseline — **check graph before minting.**

---

### E-08: gold-cloaks-betray-ned CAUSES death-of-ned-s-household-guard (Tomard / Varly / Cayn)

**Source → Target:** `gold-cloaks-betray-ned` --CAUSES--> `[deaths-of-ned-s-household-guard]`

**Tier:** 1 (verified canon)

**Cite:** `sources/chapters/agot/agot-eddard-14.md:121`

**Verbatim quote:** `"With a single sharp thrust, the nearest gold cloak drove his spear into Tomard's back. Fat Tom's blade dropped from nerveless fingers as the wet red point burst out through his ribs, piercing leather and mail."`

**Justification:** The betrayal event directly causes the massacre of Ned's household guard. This is a clean CAUSES (direct material cause, not routed through agency). Tomard, Varly, and Cayn are named victims; Cayn's death is also directly noted ("Sandor Clegane's first cut took off Cayn's sword hand at the wrist; his second drove him to his knees and opened him from shoulder to breastbone" — agot-eddard-14:123). These deaths are downstream consequences of the betrayal with 0 wired edges.

**Node question:** Does the graph have individual nodes for Tomard, Varly, Cayn? If so, VICTIM_IN edges on `gold-cloaks-betray-ned` may already capture this. If individual death-event nodes exist, CAUSES edges needed. If the deaths are not individually nodded, a group event node may be warranted.

**Slug check:** `gold-cloaks-betray-ned` exists in baseline. Individual death nodes for Tomard/Varly/Cayn not listed in baseline — **check graph.**

**Confidence:** HIGH for causal claim; node shape TBD.

---

### E-09: ned-warns-cersei-in-the-godswood (or ned-discovers-the-truth-of-joffrey-s-parentage) MOTIVATES cersei-lannister (toward the wineskin plot / speeding Robert's death)

**Note/Flag:** Varys explicitly states: "The queen would not have waited long in any case. Robert was becoming unruly, and she needed to be rid of him to free her hands to deal with his brothers" (agot-eddard-15:115). Cersei's use of Lancel and the wineskins is described as a separate act that predates or parallels the discovery. This raises the question: does `death-of-robert-baratheon` have a node for Cersei's wineskin manipulation as a sub-beat? If so, there should be a causal or ENABLES link from the discovery/warning to that wineskin plot. However, Varys says the poisoning would have happened anyway — so MOTIVATES is more accurate than ENABLES or CAUSES. The discovery may have *accelerated* her timeline rather than caused it.

**Verdict:** Flag for orchestrator. If `cersei-poisons-robert-with-strongwine` or similar node exists, propose `ned-warns-cersei-in-the-godswood --MOTIVATES--> cersei-lannister` with evidence from this passage. If no such node, this is a mint candidate for a separate enrichment pass. Do NOT mint here without orchestrator direction.

**Confidence:** LOW for edge shape; HIGH for causal relevance of the underlying fact.

---

## HARVEST ROWS

`agot-eddard-12.md:15` / food / Pycelle leaves flask: "The milk of the poppy, for when the pain grows too onerous."

`agot-eddard-12.md:129` / quote / Ned's core dilemma stated: "All three are Jaime's" — verbatim confirmation of parentage discovery.

`agot-eddard-12.md:141` / quote / Cersei on her wedding night: "The night of our wedding feast, the first time we shared a bed, he called me by your sister's name. He was on top of me, in me, stinking of wine, and he whispered Lyanna." — load-bearing motivation quote for Cersei's hatred of Robert.

`agot-eddard-12.md:169` / quote / "When you play the game of thrones, you win or you die. There is no middle ground." — canonical statement; attach to node for the godswood confrontation.

`agot-eddard-13.md:29` / description / Robert's wound: "It had ripped the king from groin to nipple with its tusks. The wine-soaked bandages that Grand Maester Pycelle had applied were already black with blood, and the smell off the wound was hideous."

`agot-eddard-13.md:45` / food / Robert's dying feast command: `"Serve the boar at my funeral feast," Robert rasped. "Apple in its mouth, skin seared crisp. Eat the bastard."` — hospitality/food + darkly ironic last command.

`agot-eddard-13.md:85` / quote / Robert's dying words to Ned: `"I will give Lyanna your love, Ned. Take care of my children for me."` — load-bearing; Ned's response ("I shall … guard your children as if they were my own") is a crucial foreshadowing of his motivations.

`agot-eddard-13.md:103` / food / Robert drinks milk of the poppy draught: "Grand Maester Pycelle mixed him another draught of the milk of the poppy." — last use; Robert dies on it.

`agot-eddard-13.md:271` / quote / Littlefinger's offer to buy the City Watch: `"Ah, but when the queen proclaims one king and the Hand another, whose peace do they protect? … They follow the man who pays them."` — key line establishing the purchase mechanism.

`agot-eddard-14.md:13` / quote / Ned's internal reckoning in the throne room: `"The first time he had come this way, he had been on horseback, sword in hand, and the Targaryen dragons had watched from the walls as he forced Jaime Lannister down from the throne."` — foreshadowing/parallel between Ned's earlier power and his current helplessness.

`agot-eddard-14.md:83` / description / Cersei's appearance in the throne room: `"Cersei Lannister and her two younger children stood behind Ser Boros and Ser Meryn. The queen wore a gown of sea-green silk, trimmed with Myrish lace as pale as foam. On her finger was a golden ring with an emerald the size of a pigeon's egg, on her head a matching tiara."` — physical description, attach to cersei-lannister node.

`agot-eddard-14.md:85` / description / Joffrey on the Iron Throne: `"Above them, Prince Joffrey sat amidst the barbs and spikes in a cloth-of-gold doublet and a red satin cape. Sandor Clegane was stationed at the foot of the throne's steep narrow stair. He wore mail and soot-grey plate and his snarling dog's-head helm."` — physical/clothing description.

`agot-eddard-14.md:125` / quote / Littlefinger's betrayal line (already in baseline as evidence for `littlefinger-betrays-ned`; confirm it is attached): `"As his men died around him, Littlefinger slid Ned's dagger from its sheath and shoved it up under his chin. His smile was apologetic. 'I did warn you not to trust me, you know.'"` — verify this is wired as evidence_quote on the node.

`agot-eddard-15.md:17` / quote / Ned damning everyone from his cell: `"He damned them all: Littlefinger, Janos Slynt and his gold cloaks, the queen, the Kingslayer, Pycelle and Varys and Ser Barristan, even Lord Renly, Robert's own blood, who had run when he was needed most."` — character perception; good for perception-mapper pass.

`agot-eddard-15.md:35` / food (prison ration) / Ned's water: `"A gaoler thrust a jug at him. The clay was cool and beaded with moisture. Ned grasped it with both hands and gulped eagerly. Water ran from his mouth and dripped down through his beard. He drank until he thought he would be sick."` — first water given in the cell (no food yet; starvation conditions).

`agot-eddard-15.md:55` / quote / Ned's deduction about why Cersei keeps him alive: `"If Cersei had wanted him dead, he would have been cut down in the throne room with his men. She wanted him alive. Weak, desperate, yet alive. Catelyn held her brother; she dare not kill him or the Imp's life would be forfeit as well."` — key strategic reasoning.

`agot-eddard-15.md:65` / food (prison) / Varys brings wine: `"Wine," a voice answered. … "Drink, Lord Eddard." He thrust a wineskin into Ned's hands.` — first sustenance beyond water; darkly echoes Robert's poisoned wine.

`agot-eddard-15.md:111` / quote / Varys on Robert's death: `"It was not wine that killed the king. It was your mercy."` — canonical verdict on the causal chain; attach to `death-of-robert-baratheon` node as evidence_quote.

`agot-eddard-15.md:155` / quote / Varys's ultimatum: `"The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head."` — food framing used as threat; load-bearing quote for the confession motivation.

`agot-arya-05.md:27` / food / pushcart tarts: `"A man was pushing a load of tarts by on a two-wheeled cart; the smells sang of blueberries and lemons and apricots."` — Arya's Flea Bottom food; hospitality failure (she can't afford them).

`agot-arya-05.md:43` / food / Flea Bottom pot-shops: `"In the Bottom there were pot-shops along the alleys where huge tubs of stew had been simmering for years, and you could trade half your bird for a heel of yesterday's bread and a 'bowl o' brown,' and they'd even stick the other half in the fire and crisp it up for you … It usually had barley in it, and chunks of carrot and onion and turnip, and sometimes even apple, with a film of grease swimming on top. Mostly she tried not to think about the meat."` — extended food/hospitality description; canonical "bowl o' brown" passage.

`agot-arya-05.md:103` / quote / Arya hears of father's fate: `"The Hand! They'll be carrying his head off, Buu says."` — civilian perspective on Ned's execution.

`agot-arya-05.md:137` / description / Ned on the pulpit (physical): `"Lord Eddard stood on the High Septon's pulpit outside the doors of the sept, supported between two of the gold cloaks. He was dressed in a rich grey velvet doublet with a white wolf sewn on the front in beads, and a grey wool cloak trimmed with fur, but he was thinner than Arya had ever seen him, his long face drawn with pain."` — physical description of Ned at execution; attach to event node.

`agot-arya-05.md:161` / quote / Joffrey rejects mercy despite promises: `"My mother bids me let Lord Eddard take the black, and Lady Sansa has begged mercy for her father." He looked straight at Sansa then, and smiled … "But they have the soft hearts of women. So long as I am your king, treason shall never go unpunished. Ser Ilyn, bring me his head!"` — key characterization of Joffrey; load-bearing quote for `execution-of-eddard-stark`.

`agot-arya-05.md:171` / foreshadowing / Ice used for execution: `"Ser Ilyn drew a two-handed greatsword from the scabbard on his back. As he lifted the blade above his head, sunlight seemed to ripple and dance down the dark metal … Ice, she thought, he has Ice!"` — Ned's own sword used to behead him; critical foreshadowing/irony note.

`agot-sansa-04.md:23` / food / Sansa's rations while confined (full detail): `"They were fed—hard cheese and fresh-baked bread and milk to break their fast, roast chicken and greens at midday, and a late supper of beef and barley stew."` — hospitality-while-prisoner; notable contrast to Ned's starvation.

`agot-sansa-04.md:53` / description / Cersei in mourning clothes: `"The queen wore a high-collared black silk gown, with a hundred dark red rubies sewn into her bodice, covering her from neck to bosom. They were cut in the shape of teardrops, as if the queen were weeping blood."` — physical description, symbolic detail.

`agot-sansa-04.md:101` / foreshadowing / The Stannis letter found on Tomard: `"We found this on the captain of your household guard, Sansa. It is a letter to my late husband's brother Stannis, inviting him to take the crown."` — establishes that the letter to Stannis (written in agot-eddard-13) was intercepted on Tomard; chain-of-custody detail for the `ned-warns-cersei-in-the-godswood` / arrest cluster.

`agot-sansa-06.md:13` / food (refusal) / Sansa in grief: `"When she could not sleep she lay under her blankets shivering with grief. Servants came and went, bringing meals, but the sight of food was more than she could bear. The dishes piled up on the table beneath her window, untouched and spoiling, until the servants took them away again."` — food refusal as grief marker; harvest for hospitality/food track.

`agot-sansa-06.md:67` / food / Sansa steadying herself: `"She drank a glass of buttermilk and nibbled at some sweet biscuits as she waited, to settle her stomach."` — small food detail.

`agot-sansa-06.md:131` / description / Ned's head on the wall (preserved in tar): `"Sandor Clegane took the head by the hair and turned it. The severed head had been dipped in tar to preserve it longer. Sansa looked at it calmly, not seeing it at all. It did not really look like Lord Eddard, she thought; it did not even look real."` — physical description; Sansa dissociation. Attach to execution aftermath.

`agot-sansa-06.md:141` / description / Septa Mordane's head: `"That's your septa there," but Sansa could not even have told that it was a woman. "The jaw had rotted off her face, and birds had eaten one ear and most of a cheek."` — physical detail; confirms Septa Mordane executed.

`agot-sansa-06.md:165` / foreshadowing / Sansa almost pushes Joffrey off the wall: `"You could do it, she told herself. You could. Do it right now. It wouldn't even matter if she went over with him. It wouldn't matter at all."` — major foreshadowing beat; Sansa-as-agent vs. Sansa-as-hostage.

---

*End of Lens 1 proposal file.*
