# Lens A — Secondary-character sub-arcs
## AEGON / Golden Company enrichment pass 1 (S147)

> **Scope:** Shy Maid household (guardians/tutors) + Golden Company officer corps + Strickland's reluctance / the broken Yunkai contract.
> **Propose only.** No mints or edits.
> **Source chapters read:** adwd-tyrion-03.md, adwd-tyrion-04.md, adwd-tyrion-05.md, adwd-tyrion-06.md, adwd-the-lost-lord-01.md, adwd-the-griffin-reborn-01.md
> **Dedup discipline:** All existing edges verified via `graph-query.py --neighbors` + `grep` in edges.jsonl before proposing.

---

## Proposed edges

> Column order: `source --TYPE--> target | tier | book chapter-file:line | "verbatim quote" | HIT/NEW-NODE | rationale`

### 1. Shy Maid Household — crew aboard / protective relations

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `yandry` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 2 | adwd-tyrion-04.md:55 | "He and his wife were Greenblood born, a pair of Dornish orphans come home to Mother Rhoyne." | HIT | Yandry poles the Shy Maid the full Rhoyne journey with Aegon aboard; existing ysilla COMPANION_OF Aegon edge but Yandry has 0 incoming edges; co-presence on boat throughout chapters 3–6 confirms sustained TRAVELS_WITH. |
| `ysilla` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-05.md:13 | "Rolly Duckfield was pushing at the starboard pole, Yandry at the larboard. Ysilla had the tiller." | HIT | Ysilla captains the Shy Maid tiller throughout the Rhoyne run; she has existing VICTIM_IN the stone-men attack and a COMPANION_OF Aegon already, but TRAVELS_WITH is the route-relationship that models the journey itself. Note: ysilla has COMPANION_OF Aegon — consider TRAVELS_WITH as additive (journey vs general companionship). Tier 1 because direct physical co-presence throughout. |
| `rolly-duckfield` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-04.md:91–95 | "Duck punched Young Griff in the shoulder. 'Time to raise some bruises. Swords today, I think.'" | HIT | Duck pushes pole / trains Aegon aboard Shy Maid; slug trap flagged: canonical node is `rolly-duckfield` but Pass-1 edges use `duck`. Use `rolly-duckfield`. |
| `haldon` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-04.md:145 | "The Volantene dialect was as new to him as it was to Tyrion, so every day they learned a few more words whilst Haldon corrected their mistakes." | HIT | Haldon teaches Aegon in his cabin aboard the Shy Maid; has existing TUTORS edge. TRAVELS_WITH models the journey co-presence separately. |
| `lemore` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-04.md:119 | "Whilst Young Griff went off with Septa Lemore to be instructed in the mysteries of the Faith…" | HIT | Lemore has existing TUTORS + GUARDS + PROTECTS Aegon; TRAVELS_WITH adds the journey layer. |
| `jon-connington` | `TRAVELS_WITH` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-03.md:189 | "Griff had commanded him to set down all he knew of dragonlore." | HIT | Griff/JonCon is aboard the Shy Maid throughout the Rhoyne journey, keeping the night watch (adwd-tyrion-04:19 "Griff sat wrapped in a wolfskin cloak beside an iron brazier … keeping the night watch by himself"). Has PARENT_OF + COMMANDS + PROTECTS Aegon. TRAVELS_WITH captures the shared journey. |
| `rolly-duckfield` | `PROTECTS` | `aegon-targaryen-young-griff` | 1 | adwd-the-griffin-reborn-01.md:187 | "Before them went Ser Rolly Duckfield, a snow-white cloak streaming from his shoulders." | HIT | Duck is named Kingsguard (white cloak at Griffin's Roost); "sworn shield" role confirmed. No PROTECTS edge currently on `rolly-duckfield` (he has 0 incoming, 0 event-role outgoing). |
| `rolly-duckfield` | `TEACHES` | `aegon-targaryen-young-griff` | 1 | adwd-tyrion-04.md:91–97 | "When they fought with mace or blunted longaxe, Ser Rolly's greater size and strength would quickly overwhelm his charge; with swords the contests were more even." | HIT | Duck trains Aegon in arms daily aboard the Shy Maid. Pass-1 edges capture `duck TEACHES aegon` but under the `duck` slug, not `rolly-duckfield`. This uses the canonical node slug and attaches to the correct target. Note: existing `TEACHES duck -> aegon-targaryen-young-griff` in edges.jsonl uses stale `duck` slug — this proposal uses canonical slug. |
| `yandry` | `MEMBER_OF` | `golden-company` | 3 | adwd-tyrion-04.md:23 | "If it had been up to Griff, the Shy Maid would continue downstream by night as well as day, but Yandry and Ysilla refused to risk their poleboat in the dark." | HIT | Yandry/Ysilla are not GC members — they are independent Greenblood-born poleboat owners. **REJECT this one.** See Dropped section. |

### 2. Crew departures after the reveal

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `jon-connington` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:127 | "My lords, I give you Aegon Targaryen, firstborn son of Rhaegar… soon, with your help, to be Aegon, the Sixth of His Name." | HIT | JonCon delivers the reveal speech personally; this is the load-bearing event. No PARTICIPATES_IN or AGENT_IN for JonCon on this event exists. AGENT_IN would also fit (he performs the action), but PARTICIPATES_IN covers the role as the announcer/author of the reveal without overclaiming command. Actually AGENT_IN is stronger — he is the agent of the reveal act. Prefer AGENT_IN. |
| `aegon-targaryen-young-griff` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:175 | "Then Prince Aegon spoke. 'Then put your hopes on me,' he said." | HIT | Aegon is the subject of the reveal and speaks directly at the war council; his speech ("sail west not east") tips the vote. PARTICIPATES_IN. |
| `harry-strickland` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:130 | "I give you Aegon Targaryen… Silence greeted his announcement. Someone cleared his throat." | HIT | Strickland presides at the war council; he is the audience/responder. He knew already ("When did you tell them?" → "When we reached the river"). Strickland's existing `OPPOSES jon-connington` edge does NOT capture his presence at the revelation event. PARTICIPATES_IN is correct here — he's the audience, not the commander of the reveal. |
| `tristan-rivers` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:215 | "Prince Aegon,' said Tristan Rivers, 'we are your men. Is this your wish, that we sail west instead of east?'" | HIT | Rivers asks Aegon the deciding question at the war council, directly tipping the sailing-west decision. Key participant. |
| `laswell-peake` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:213 | "Even after a century, some of us still have friends in the Reach. The power of Highgarden may not be what Mace Tyrell imagines." | HIT | Peake speaks at the council in support of sailing west. |
| `franklyn-flowers` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:181 | "Franklyn Flowers laughed. 'I like it. Sail west, not east. Leave the little queen to her olives…'" | HIT | Flowers endorses the plan at the war council. |
| `marq-mandrake` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:219 | "Marq Mandrake chuckled and responded, 'Me, I'd sooner live, win lands and some great castle'" | HIT | Mandrake is one of the voices tipping the vote. |
| `lysono-maar` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:147 | "'I assume you know that the Targaryen girl has not started for the west?' [Lysono Maar]" | HIT | Lysono-maar opens the intelligence briefing that frames the vote. He is present and speaking. |
| `gorys-edoryen` | `PARTICIPATES_IN` | `aegon-revealed-to-the-golden-company` | 1 | adwd-the-lost-lord-01.md:163 | "'Allow the Yunkai'i to transport us to the east, then return their gold beneath the walls of Meereen.' [Gorys Edoryen]" | HIT | Edoryen proposes the Yunkai alternative. Present at the war council. |

### 3. Golden Company sails for Westeros — crew + officer participation

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `harry-strickland` | `PARTICIPATES_IN` | `golden-company-sails-for-westeros` | 1 | adwd-the-lost-lord-01.md:223 | "One by one, the men of the Golden Company rose, knelt, and laid their swords at the feet of his young prince. The last to do so was Homeless Harry Strickland, blistered feet and all." | HIT | Strickland's reluctant participation is the closing act of the war council → sail decision. The crossing is his command to execute. |
| `rolly-duckfield` | `PARTICIPATES_IN` | `golden-company-sails-for-westeros` | 1 | adwd-the-lost-lord-01.md:229 | "Ride back to the Shy Maid and return with Lady Lemore and Ser Rolly. We'll need Illyrio's chests as well." | HIT | Duck is recalled from the Shy Maid to join the march / embark. Confirmed participant in the crossing. |
| `lemore` | `PARTICIPATES_IN` | `golden-company-sails-for-westeros` | 1 | adwd-the-lost-lord-01.md:229 | "Ride back to the Shy Maid and return with Lady Lemore and Ser Rolly." | HIT | Lemore crosses with the company. |

### 4. The Stormlands Campaign — simultaneous-column takings

> **REMINDER: DO NOT add CAUSES between sibling takings** (per §4 of decomposition). They are simultaneous. Only COMMANDS_IN / AGENT_IN per column commander.

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `jon-connington` | `COMMANDS_IN` | `taking-of-griffins-roost` | 1 | adwd-the-griffin-reborn-01.md:21–31 | "He sent the archers in first. Black Balaq commanded one thousand bows… For this, two hundred proved sufficient." / "Griff rode up the throat on a white courser… And quick as that, Griffin's Roost was his again." | HIT | JonCon personally leads the Griffin's Roost column. He presides from the Griffin Seat that night. Already has COMMANDS_IN on sub-beat children but NOT on the parent `taking-of-griffins-roost` event itself — adding the parent level. |
| `black-balaq` | `COMMANDS_IN` | `taking-of-griffins-roost` | 1 | adwd-the-griffin-reborn-01.md:11 | "He sent the archers in first. Black Balaq commanded one thousand bows… They proved it again at Griffin's Roost." | HIT | Balaq commands all archers at Griffin's Roost; existing edge is `AGENT_IN defenders-killed-on-battlements` (sub-beat). The parent taking also needs his COMMANDS_IN. |
| `franklyn-flowers` | `COMMANDS_IN` | `taking-of-griffins-roost` | 1 | adwd-the-griffin-reborn-01.md:25 | "The woods had been allowed to encroach on the field beyond the gatehouse, so Franklyn Flowers was able to use the brush for concealment and lead his men within twenty yards of the gates." | HIT | Flowers leads the ram assault / ground force at Griffin's Roost. Has ATTACKS griffins-roost and AGENT_IN sub-beats, but not COMMANDS_IN on the parent event. |
| `harry-strickland` | `PARTICIPATES_IN` | `taking-of-griffins-roost` | 1 | adwd-the-griffin-reborn-01.md:41 | "Even Homeless Harry was impressed by the swiftness of their victory. 'I never thought that it would be so easy,' the captain-general said." | HIT | Strickland rides up the throat alongside Connington; he is physically present in the taking. PARTICIPATES_IN (not COMMANDS_IN — JonCon commands, Strickland is present but not directing). |
| `tristan-rivers` | `COMMANDS_IN` | `taking-of-crows-nest` | 1 | adwd-the-griffin-reborn-01.md:93 | "Ser Tristan Rivers had set off simultaneously for the seat of House Morrigen at Crow's Nest…" | HIT | Rivers commands the Crow's Nest column explicitly. No event-role edge on Rivers currently (4 outgoing, 0 incoming). |
| `laswell-peake` | `COMMANDS_IN` | `taking-of-rain-house` | 1 | adwd-the-griffin-reborn-01.md:93 | "…and Laswell Peake for Rain House, the stronghold of the Wyldes, each with a force of comparable size." | HIT | Peake commands the Rain House column explicitly. He has existing ATTACKS rain-house (dyad) but not COMMANDS_IN on the event hub. This upgrades the direct-attack dyad to an event-role edge. |
| `marq-mandrake` | `COMMANDS_IN` | `taking-of-greenstone` | 1 | adwd-the-griffin-reborn-01.md:143 | "Word's reached the camp from Marq Mandrake. The Volantenes put him ashore on what turned out to be Estermont, with close to five hundred men. He's taken Greenstone." | HIT | Mandrake commands the accidental Estermont/Greenstone column. Has existing CAPTURES greenstone but not COMMANDS_IN on the event hub. |
| `gorys-edoryen` | `COMMANDS_IN` | `landing-of-the-golden-company` | 1 | adwd-the-griffin-reborn-01.md:93 | "The rest of their men had remained in camp to guard their landing site and prince, under the command of the company's Volantene paymaster, Gorys Edoryen." | HIT | Edoryen commands the landing camp / rear guard while the columns fan out. He already has GUARDS landing (the overall guard role as a dyad). COMMANDS_IN on the landing event represents his command role. |

### 5. Siege of Storm's End — Aegon insists on leading

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `aegon-targaryen-young-griff` | `COMMANDS_IN` | `siege-of-storms-end-300` | 1 | adwd-the-griffin-reborn-01.md:201 | "I want the attack to go ahead … with one change. I mean to lead it." | HIT | Aegon explicitly insists on commanding the Storm's End assault over JonCon's objections. No existing event-role edge on Aegon for this event. |
| `rolly-duckfield` | `PARTICIPATES_IN` | `siege-of-storms-end-300` | 1 | adwd-the-griffin-reborn-01.md:187 | "The prince arrived to join them four days later, riding at the head of a column of a hundred horse, with three elephants lumbering in his rear. Lady Lemore was with him, garbed once more in the white robes of a septa. Before them went Ser Rolly Duckfield, a snow-white cloak streaming from his shoulders." | HIT | Duck accompanies Aegon to Griffin's Roost (before the Storm's End march); as Kingsguard he goes wherever the prince goes, including Storm's End. PARTICIPATES_IN rather than COMMANDS_IN. |
| `lemore` | `PARTICIPATES_IN` | `siege-of-storms-end-300` | 1 | adwd-the-griffin-reborn-01.md:187 | "Lady Lemore was with him, garbed once more in the white robes of a septa." | HIT | Lemore rides with Aegon's column; accompanying the prince to Storm's End. |
| `harry-strickland` | `PARTICIPATES_IN` | `siege-of-storms-end-300` | 1 | adwd-the-griffin-reborn-01.md:173 | "He would wait until all seven hells were frozen if he could rather than risk another bout of blisters." / "We did not cross half the world to wait. I mean to take Storm's End." | HIT | Strickland's reluctance is explicitly opposed by Connington's Storm's End decision at the war council (adwd-the-griffin-reborn-01:183–185). Strickland is forced to participate; his reluctance is the defining character note. PARTICIPATES_IN rather than COMMANDS_IN. |

### 6. Harry Strickland reluctance — the broken Yunkai contract

| source | type | target | tier | book chapter-file:line | verbatim quote | HIT/NEW-NODE | rationale |
|--------|------|--------|------|------------------------|----------------|--------------|-----------|
| `golden-company` | `NEGOTIATES_WITH` | `yunkai` | 2 | adwd-the-lost-lord-01.md:135 | "The Yunkishmen. The envoy that they sent to woo Volantis has already dispatched three free companies to Slaver's Bay. He wishes us to be the fourth and offers twice what Myr was paying us, plus a slave for every man in the company…" | HIT (check: `golden-company` node exists? See note) | The Yunkai envoy made a formal contract offer. Strickland said "I told him I would think on his proposal" — he didn't formally accept but was actively negotiating. NEGOTIATES_WITH is the right type for an ongoing back-and-forth offer not yet formalized. Tier 2 because it is told in reported speech. Note: need to verify `golden-company` node slug — see node-check below. |
| `harry-strickland` | `OPPOSES` | `golden-company-sails-for-westeros` | 1 | adwd-the-lost-lord-01.md:163 | "'One broken contract is stain enough upon the honour of the company… It seems plain to me that the Targaryen girl is never coming west.'" | HIT | Strickland explicitly argues against the westward sail multiple times, fearing the risk and the broken GC founding contract. He has existing OPPOSES jon-connington and OPPOSES breaking but NOT OPPOSES on the sail event itself. This edge gives the reluctance a causal target. |

---

## Node / slug checks (flag for synthesizer)

- `golden-company` node slug — verify exists at `graph/nodes/factions/golden-company.node.md` or equivalent before minting edge #6 above. If it only exists as a `SWORN_TO` target (faction node), the edge is a HIT once confirmed.
- `taking-of-crows-nest`, `taking-of-rain-house`, `taking-of-greenstone`, `fall-of-mistwood`, `invasion-of-tarth` — confirmed HIT via baseline §Per-node state. Edge endpoints are HITs.
- `aegon-revealed-to-the-golden-company`, `golden-company-sails-for-westeros` — both are MISS (mints queued in decomp Ranks 4 and 1). All edges to these nodes are contingent on the mints landing first. Mark as **PENDING-MINT** in synthesis.

---

## Proposed nodes

None. No genuinely missing character or event nodes identified.

**Slug trap (for synthesizer):** The Pass-1 edge file uses `duck` as source slug (e.g. `duck SERVES jon-connington`, `duck TEACHES aegon-targaryen-young-griff`). The canonical node is `rolly-duckfield`. When minting new edges, use `rolly-duckfield`. The existing `duck`-slug edges in edges.jsonl should be alias-resolved or flagged for a dedup sweep — this is out of scope for this lens but noted for downstream.

---

## Dropped / considered-but-no

| What was considered | Why dropped |
|---------------------|-------------|
| **CAUSES edges between the 6 sibling takings** (e.g. taking-of-griffins-roost CAUSES taking-of-crows-nest) | HARD SKIP. §4 of decomposition: all three columns set off simultaneously. "Ser Tristan Rivers had set off *simultaneously* for the seat of House Morrigen at Crow's Nest, and Laswell Peake for Rain House" (adwd-the-griffin-reborn-01:93). Greenstone was an accident (Volantenes dumped Mandrake on Estermont). Siblings, not a chain. PART_OF landing is the correct structure. |
| **yandry MEMBER_OF golden-company / yandry SERVES jon-connington** | Yandry and Ysilla are independent Greenblood poleboat owners, not GC members. Connington explicitly thanks them and releases them ("Their part in this is done" — adwd-the-lost-lord-01:229). They serve the mission opportunistically, not as members. Their existing SWORN_TO house-targaryen (wiki) is the only formal alignment. No MEMBER_OF or SERVES proposed. |
| **ysilla MEMBER_OF golden-company** | Same as above. |
| **lemore MEMBER_OF golden-company** | Lemore is a septa — she is an independent contractor in the conspiracy, not a GC soldier. She has existing SWORN_TO house-targaryen and faith-of-the-seven. No GC membership. |
| **haldon MEMBER_OF golden-company** | Haldon is a "chainless maester" (ex-Citadel, expelled or dropped chain) serving the Connington/Aegon mission. Not a GC officer. His existing SWORN_TO house-targaryen is sufficient. No GC membership. |
| **rolly-duckfield MEMBER_OF golden-company** | Duck does have existing SWORN_TO golden-company (wiki-sourced). The additional MEMBER_OF would be redundant (SWORN_TO serves the same graph function here). Skip. |
| **Aegon's identity / "mummer's dragon" edges** | HARD GATED. Tyrion explicitly says "I have noble features for a dead boy" and "Who better to raise Prince Rhaegar's infant son than Prince Rhaegar's dear friend Jon Connington" (adwd-tyrion-05:177) — and Young Griff confirms the Pisswater boy story. These are on-page identity claims asserted by characters, NOT graph claims about identity. The whole identity question is GATED. No SUSPECTED_OF or identity edges proposed. |
| **Tyrion MOTIVATES golden-company-sails-for-westeros (via cyvasse speech)** | Tyrion's speech to Aegon in adwd-tyrion-06:133–147 is the canonical goad ("If I were you? I would go west instead of east"). This is a MOTIVATES edge. **However, it is scope for Lens B (whodunit/revelation/manipulation) or Lens D (causal wiring), not Lens A (secondary-character sub-arcs).** Flagging here so Lens B/D captures it. Quote: "Be certain you reach Westeros before my sister falls" (adwd-tyrion-06:137). |
| **Haldon COMMANDS_IN the war council** | Haldon is present at the war council (adwd-the-lost-lord-01:117 confirms he attended Strickland's council) but he speaks only about ointments for Strickland's feet and receives orders (go back to the Shy Maid). He is a participant but not a decision-maker. PARTICIPATES_IN could be proposed, but it adds low value compared to the officers who actively shape the vote. Dropped for quality over volume. |
| **Black Balaq PARTICIPATES_IN landing-of-the-golden-company** | Balaq commands archers on the ship-distribution and is at Griffin's Roost; his role at the landing itself is the parent event is implicit but not quoted. His sub-beat AGENT_IN defenders-killed-on-battlements is the grounded edge. PARTICIPATES_IN landing is inferential. Dropped — not quote-backed enough. |
| **yandry VICTIM_IN stone-men-attack-the-shy-maid** | Yandry is polling the boat when the stone men jump (adwd-tyrion-05:13 "Yandry at the larboard"). He is present but not explicitly attacked; no "Yandry was grabbed/hurt" text. Ysilla "let out a shriek" (205) and is already VICTIM_IN. Yandry is not clearly a victim. Dropped. |
| **Malo Jayn COMMANDS_IN taking-of-griffins-roost** | Malo Jayn is given a sub-assignment at Griffin's Roost ("Malo, do the same with the maester's tower and the armory" — adwd-the-griffin-reborn-01:33) but this is a small internal task under Connington's command, not independent column command. His existing node has no event edges. The sub-task is too granular and better captured as Connington's command (already proposed). Dropped. |
| **GC CONTRACTED_WITH Volantis/Yunkai (formal)** | The chapter text says Strickland "told him I would think on it" — the Yunkai contract was never formally signed. It was an open negotiation only. NEGOTIATES_WITH is the right type; a formal CONTRACTED_WITH would overclaim. |
| **Aegon KINGSGUARD_APPOINTS rolly-duckfield** | No KINGSGUARD_APPOINTS edge type in the locked vocab. Aegon gives Duck the white cloak explicitly ("He had tried his best to dissuade the prince from giving Duckfield that cloak" — adwd-the-griffin-reborn-01:189). The relationship is captured via rolly-duckfield's existing SWORN_TO kingsguard (wiki). A NEEDS_VOCAB: APPOINTS could be flagged if synthesizer wants to model it. |

---

## Harvest

> Pointer format: `chapter:line / kind / note`. POINT, don't extract.

| chapter:line | kind | note |
|---|---|---|
| adwd-tyrion-03.md:147 | food | Salt pork and cold white beans washed down with ale — supper for Haldon + Duck + Tyrion on the road to Ghoyan Drohe. "Tyrion found the plain fare a pleasant change from all the rich food he had eaten with Illyrio." |
| adwd-tyrion-04.md:51–65 | food | Ysilla's biscuits and bacon over the brazier — the daily breakfast aboard the Shy Maid. Honeyed biscuits, bacon, Tyrion snatching a biscuit, Duck receiving a spoon-smack. Hospitality from Ysilla. |
| adwd-tyrion-04.md:51–53 | description | Lemore's morning bathing ritual — strips naked, swims, climbs back aboard dripping. Physical description. Stretch marks noted. |
| adwd-tyrion-04.md:77 | description | Young Griff's appearance (as seen by Tyrion): "beardless boy could have any maiden in the Seven Kingdoms… Those eyes of his would melt them… By lamplight they turned black, and in the light of dusk they seemed purple." Key physical description of the claimant. |
| adwd-tyrion-04.md:161 | food | Yandry and Ysilla return to the Shy Maid with provisions: "salt and flour, fresh-churned butter, slabs of bacon wrapped in linen, sacks of oranges, apples, and pears. Yandry had a wine cask on one shoulder, while Ysilla had slung a pike over hers." — resupply scene, specific goods. |
| adwd-tyrion-06.md:161 | food | The pike cooking: "the pike was spitting and sizzling over the brazier whilst Ysilla hovered over it with a lemon, squeezing" — a fish feast at Selhorys. |
| adwd-tyrion-04.md:143 | description | Haldon's cabin: "One wall was lined with bookshelves and bins stacked with old scrolls and parchments; another held racks of ointments, herbs, and potions." — the Halfmaester's workspace. |
| adwd-tyrion-06.md:67–68 | quote | Haldon on Tyrion's greyscale risk: "Truly? Never. You swallowed half the river. You may be going grey even now, turning to stone from inside out, starting with your heart and lungs." — the greyscale medical knowledge (quote for jon-connington AFFLICTED_BY or node prose). |
| adwd-tyrion-06.md:85 | description | Lemore changes out of septa's robes into merchant-wife clothing at Selhorys. "Who is she, really? Why is she here?" — Tyrion's suspicion, Lemore's mysterious background (stretch marks → bore a child). Physical description, foreshadowing. |
| adwd-the-lost-lord-01.md:93–99 | description | GC officer corps assembled for war council: bastard names (Rivers, Hill, Stone), exile surnames (Strong, Peake, Mudd, Mandrake, Lothston, Cole). "Every man wore a lord's ransom in golden arm rings. Each ring signified one year's service." — description of the GC leadership, hospitality of war-gold. |
| adwd-the-lost-lord-01.md:97 | quote | Bittersteel's skull on the pike: "He died defeated and alone, a broken man in an alien land. On his deathbed, Ser Aegor Rivers had famously commanded his men to boil the flesh from his skull, dip it in gold, and carry it before them when they crossed the sea to retake Westeros." — foreshadowing / parallel for Aegon/Bittersteel arc; foundational GC history quote. |
| adwd-the-griffin-reborn-01.md:53 | quote | Prince Rhaegar visiting Griffin's Roost: "'Your father's lands are beautiful,' Prince Rhaegar had said, standing right where Jon was standing now." — JonCon/Rhaegar relationship evidence; physical description of Cape Wrath; emotional weight. |
| adwd-the-griffin-reborn-01.md:189 | quote | JonCon on Duck as Kingsguard: "He had tried his best to dissuade the prince from giving Duckfield that cloak, pointing out that the honor might best be held in reserve for warriors of greater renown…  'Duck will die for me if need be,' he had said, 'and that's all I require in my Kingsguard.'" — Aegon's character/agency, Duck's loyalty; foreshadowing of Kingsguard theme. |
| adwd-the-griffin-reborn-01.md:135 | food | Griffin's Roost first breakfast after recapture: "Boiled eggs, fried bread, and beans. And a jug of wine. The worst wine in the cellar." — already in harvest-queue.md (aegon-dip 2026-06-22). Confirming still open. |
| adwd-tyrion-03.md:103 | quote | Illyrio farewell to Tyrion's party: "Good fortune. Tell the boy I am sorry that I will not be with him for his wedding. I will rejoin you in Westeros. That I swear, by my sweet Serra's hands." — Illyrio's Serra reference; foreshadowing of his promised westward crossing; evidence for Illyrio MOTIVATES aegon-revealed arc. |
