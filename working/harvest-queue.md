# Harvest Queue — deferred-capture ledger

> **Purpose.** A cheap breadcrumb log for anything *notable but not your current task* that an agent
> notices **while already reading a passage** (a dip, arc research, an audit — any pass over the text).
> You **point**, you do **not** extract. One line per find. A later **harvest pass** batches the
> pointers and does the context-expensive part (slug resolution, dedup, minting node `## Quotes` /
> `object.food` nodes / appearance & description fields / edges).
>
> **Why it exists.** Attaching a find inline mid-task costs real context (resolve the slug, dedup against
> the graph, mint the edge). Dropping a `book / chapter:line / kind / one-liner` pointer costs almost
> nothing and you're already in the text. The graph still gets enriched — just batched, later, by a pass
> whose *whole job* is harvesting. Companion to the FIRM `feedback_capture_quotes_during_research` rule.
>
> **Consumer.** A future "harvest pass" (own track / todo) reads `status: open` rows, opens each
> `chapter:line`, attaches to the graph, and flips the row to `done`. Until then this is a queue, not
> graph state — nothing here is authoritative. Append-only; don't rewrite others' rows.

## `kind` enum (kept tight — split where the graph home differs)

| kind | use for | likely graph home |
|------|---------|-------------------|
| `quote` | a homeless load-bearing line with no beat-node home yet | node `## Quotes` / edge `evidence_quote` |
| `food` | food, drink, or a consumable served (lemon cakes, Arbor gold, sweet beer) | `object.food` node |
| `appearance` | a **character's** physical look — face, body, hair, scars, dress, sigil-worn (first-class for cross-identity matching) | character node appearance field / `## Description` |
| `place` | a **location's** look, layout, or atmosphere (a hall, a godswood, a ruin) | `place.location` node description |
| `object` | an **artifact/material's** look, material, or provenance (a sword's blade, a crown) | `object.artifact` / `object.material` node |
| `hospitality` | guest-right, host-guest custom, a feast-as-event, bread-and-salt | `event.feast` / `GUEST_OF` / custom edges |
| `foreshadowing` | a planted detail / Chekhov's gun | `FORESHADOWS` edge → event |
| `relationship` | an asserted tie worth an edge that isn't your task | typed edge |
| `other` | notable but none of the above — say what in `note` | triage at harvest |

> **Bucket evolution — smoke test, don't pre-engineer (Matt, S108):** this enum is a starting point.
> **Review gate: after the next ~2 dips' worth of rows**, check (a) which buckets actually filled,
> (b) whether any need splitting/merging (e.g. `place` dividing into layout-vs-atmosphere), and
> (c) whether to harden the push from memory → CLAUDE.md/hook. Until then: leave the enum and the
> memory-only push as-is. Don't pre-engineer buckets nobody is filling.
>
> **2-dip review outcome (S109, 2026-06-19):** queue now **~28 open rows** (S108 ×6 + S109 ×22 from 3
> text-reading subagents: dip + arc-research + verify). The **push works** — every subagent dropped rows.
> Bucket fill: `quote` ~10 · `appearance` ~8 · `food` ~4 · `place` ~2 · `relationship` ~2 · `object`/`foreshadowing` ~1 ·
> `hospitality`/`other` 0. **No split/merge yet** — `place` has only ~2 rows (too few to justify the
> layout-vs-atmosphere split), no bucket is overflowing, the enum holds. **Push stays memory-only** (it's
> already reliable; no CLAUDE.md/hook hardening needed). **Next action: the queue is now big enough to be
> worth a batched harvest pass** (the MEDIUM backlog item) — run it before the queue grows stale.

## Paste-into-every-dip/research-subagent-prompt snippet (canonical — copy verbatim)

> While you read these chapters/passages for your task, ALSO drop one-line pointers to anything
> *notable-but-not-your-task* into `working/harvest-queue.md` — append a row:
> `| open | <kind> | <book> | <chapter:line> | <short note or verbatim snippet> | <this session/track> |`.
> Kinds: `quote` (homeless load-bearing line) · `food` (food/drink/hospitality consumable) · `appearance`
> (a character's physical look/dress) · `place` (a location's look/atmosphere) · `object` (an
> artifact/material's look or provenance) · `hospitality` (guest-right/host-guest custom) ·
> `foreshadowing` · `relationship` · `other`. POINT, don't extract; don't stop your task to attach it;
> don't pre-dedup. If nothing notable comes up, add nothing.

## Queue

> **HARVEST PASS RUN — S110, 2026-06-20 (all 28 open rows → done).** Every cited `chapter:line` was
> opened and verified before attaching; a fresh-subagent verify confirmed 23/24 SUPPORTED + 1 wording
> drift (fixed). Outcomes by kind: **quotes** → node `## Quotes` (eddard-stark, jaime-lannister,
> tyrion-lannister, robb-weds-jeyne [expanded], fall-of-astapor [new ## Quotes], jaime-frees-tyrion,
> trial-of-tyrion, assassination-of-tywin [foreshadowing]); **appearance** → `## Appearances & Description`
> (renly, petyr-baelish, varys, jaime, gregor, oberyn — book `chapter:line` overlay onto wiki-cite prose,
> the high-value bit); **food** → minted **`bread`** node + attached to `beer`/`cheese`/`dragon-pepper`;
> **place** → black-cells (four-level + dragon-mosaic juncture); **object** → shae (Hand's golden chain);
> **relationship** → minted **ADVISES** edge rodrik-harlaw→balon-greyjoy (`wiki-historical-anchor`, Tier-2,
> edges.jsonl 22,272→22,273). **DATA FIX:** `milk-of-the-poppy` retyped `object.food`→`concept.medical`,
> moved foods/→medical/, indexes rebuilt. **DEDUP (no-op):** row 67 (Jeyne appearance) + row 77 (Tywin
> "shit gold" quote) already in their nodes. **JUDGMENT CALLS FOR MATT** (in worklog S110): (a) possible
> dup `greyjoy-rebellion` (event.war) vs `greyjoys-rebellion` (event.battle); (b) whether to mint granular
> dish nodes (applecakes/blood-sausage/eggs) or a `chamber-of-the-dragon-mosaic` place node — deferred, not minted.

> **HARVEST PASS RUN — S113, 2026-06-20 (settling pass; 23 rows → done, 5 left open).** Folded in the
> **parallel demo-window's 9 verified attachments** (commit `6ec6caafe`: rows 104/106/112/117 → battle-of-the-blackwater
> + stannis-retreats book-cite overlays; **122 → execution-of-eddard-stark NEW `## Quotes`** [Matt-flagged Ned-exec
> harvest — Joffrey "bring me his head!" + Arya "he has Ice!"]; 116 → tywin-lannister war-armor; 110 → mace/loras/garlan
> Tyrell dress; 115 → salladhor-saan shipboard hospitality) + confirmed-no-op rows 107/108/111/113/114. **This (S113)
> pass attached 5 net-new:** 109 → `joffrey-sets-sansa-aside…` NEW `## Quotes` (Cersei "set Sansa Stark aside");
> 124 → tytos-blackwood book-cite overlay onto wiki appearance (`agot-catelyn-11:19`); 123 → riverrun `## Quotes`
> godswood-on-eve-of-proclamation (cite fixed `:127`→`:125`); 127 + 128 → `robb-proclaimed-king-in-the-north` `## Quotes`
> (Robb's motive + Catelyn's Frey-bride **Red-Wedding foreshadowing**). 125 (Edmure) flipped done — context covered by
> the node Identity + CAUSES edge, not separately homed. **LEFT OPEN (5):** 105 (Garlan-as-Renly cite WRONG, re-resolve);
> 118–121 (Essos conspiracy/Drogo-vow/Jorah-channel — gated to the Essos-bridge arc mints, not a harvest pass).

| status | kind | book | chapter:line | note | found during |
|--------|------|------|--------------|------|--------------|
| done | appearance | agot | agot-eddard-13:35 | Renly in bloodied hunting greens just after the boar kills Robert | S108 B3 research |
| done | quote | agot | agot-eddard-13:169 | Ned refuses to seize Cersei's children while Robert dies: "I will not dishonor his last hours on earth by shedding blood in his halls" — homeless load-bearing (Ned's fatal honor); no beat-node home | S108 B3 research |
| done | food | agot | agot-eddard-14:43 | "a cup of sweet beer" offered to Pycelle in the Hand's solar — hospitality detail | S108 B3 research |
| done | appearance | agot | agot-eddard-14:49 | Littlefinger "blue velvets and silver mockingbird cape … boots dusty from riding" | S108 B3 research |
| done | appearance | agot | agot-eddard-14:51 | Varys "in a wash of lavender, pink from his bath, his plump face scrubbed and freshly powdered, his soft slippers all but soundless" | S108 B3 research |
| done | food | agot | agot-eddard-15:157 | "bread and cheese and the milk of the poppy" — `object.food` (bread/cheese) + `concept.medical` (milk of the poppy); the quote itself already attached to `ned-confesses-to-treason` | S108 B3 research |
| done | appearance | asos | wiki:Jeyne_Westerling | "curly chestnut hair, heart-shaped face, shy smile, doe-like soft brown eyes; slender and willowy, small apple-sized breasts" — first-class appearance record, no chapter:line yet | S109 fresh-arc-dip |
| done | quote | asos | wiki:Storming_of_the_Crag / asos-catelyn-02 | Robb: "I took her castle and she took my heart. … I took an arrow in the arm … Jeyne had me taken to her own bed, and she nursed me until the fever passed. And she was with me when the Greatjon brought me the news … That night, she … she comforted me, Mother." — load-bearing quote for robb-weds-jeyne-westerling beat, no node quote yet | S109 fresh-arc-dip |
| done | food | acok | wiki:Storming_of_the_Crag / acok-catelyn-07 | smallfolk at Riverrun celebrate with "nut-brown ale" after Crag victory + Edmure's return — hospitality/food detail | S109 fresh-arc-dip |
| done | relationship | acok | wiki:Greyjoy's_Rebellion | Rodrik Harlaw "unsuccessfully advised Balon against rebelling" — ADVISES/OPPOSES edge between harlaw and balon-greyjoy or greyjoy-rebellion may be missing | S109 fresh-arc-dip |
| done | quote | asos | wiki:Fall_of_Astapor / asos-daenerys-03 | Daenerys keeps secret that she understands Kraznys's High Valyrian while he insults her — tactical deception, load-bearing for fall-of-astapor; no quote on that node yet | S109 fresh-arc-dip |
| done | quote | asos | asos-tyrion-11.md:27 | "Handless and Noseless, the Lannister boys." — Tyrion's greeting to Jaime in the black cells; appearance + dark comedy double | S109 tywin-arc research |
| done | appearance | asos | asos-tyrion-11.md:25 | "Jaime was gaunt, his hair hacked short" — Jaime's post-captivity appearance on the first page of the freeing scene | S109 tywin-arc research |
| done | quote | asos | asos-tyrion-11.md:119 | "Cersei is a lying whore, she's been fucking Lancel and Osmund Kettleblack and probably Moon Boy for all I know." — Tyrion's bombshell revelation to Jaime; load-bearing for Cersei-adultery arc | S109 tywin-arc research |
| done | object | asos | asos-tyrion-11.md:197 | Shae's "chain of linked golden hands, each holding the next" — Tywin's personal token/gift worn as collar; named artifact detail | S109 tywin-arc research |
| done | place | asos | asos-tyrion-11.md:145 | Varys describes the four dungeon levels under the Red Keep — vivid atmosphere of 4th-level dark cells; "once a man is taken down to the fourth level, he never sees the sun again" | S109 tywin-arc research |
| done | quote | asos | asos-tyrion-11.md:267-269 | "Lord Tywin Lannister did not, in the end, shit gold." — the chapter's last line; iconic; no quote on assassination-of-tywin-lannister node yet | S109 tywin-arc research |
| done | quote | asos | asos-jaime-07.md:209 | "He is still my brother. I am in no fit state to be killing anyone." — Jaime refusing Cersei in the sept; captures Jaime's moral stance at the trial period | S109 tywin-arc research |
| done | quote | asos | asos-tyrion-10.md:249 | "He never heard his father speak the words that condemned him." — POV gap: Tyrion's condemnation is narrated obliquely; load-bearing for how the sentence lands | S109 tywin-arc research |
| done | food | asos | asos-tyrion-10.md:101 | Tyrion's pre-combat breakfast: fried bread, blood sausage, applecakes, double eggs with onions and fiery Dornish peppers — named dish detail, Dornish peppers notable | S109 tywin-arc verify |
| done | appearance | asos | asos-tyrion-10.md:167-173 | Gregor's full pre-combat armour description: flat-topped greathelm bolted to gorget, breaths at mouth/nose, narrow vision slit, stone fist crest, 7-pointed star painted over Clegane hounds; Oberyn's: copper scales, removed visor, round polished shield, soft red gloves, ash spear 8ft with 2ft steel leaf-head | S109 tywin-arc verify |
| done | quote | asos | asos-tyrion-10.md:43 | "I saved you all, Tyrion thought. I saved this vile city and all your worthless lives." — Tyrion watching the laughter at "my giant of Lannister"; core bitterness quote; no quote on trial-of-tyrion-lannister node yet | S109 tywin-arc verify |
| done | appearance | asos | asos-tyrion-11.md:25 | Jaime's appearance when he enters the black cells: "gaunt, his hair hacked short... I left a hand at Harrenhal" — stump of right wrist; first appearance-flagged reunion beat | S109 tywin-arc verify |
| done | appearance | asos | asos-tyrion-11.md:197-198 | Shae wearing "a chain of linked golden hands, each holding the next" — the Hand's collar; notable visual / object detail; Tywin's possessiveness made visible | S109 tywin-arc verify |
| done | place | asos | asos-tyrion-11.md:153-157 | The juncture below the Tower of the Hand: round chamber, five iron-barred doors + ceiling shaft with rungs, ornate dragon's-head brazier with orange-glowing coals, mosaic three-headed dragon in red and black tiles; below the Tower of the Hand; Varys says "We are below the Tower of the Hand" | S109 tywin-arc verify |
| done | quote | asos | asos-tyrion-11.md:63 | "Thank you, Brother. For my life." / "It was... a debt I owed you." — Jaime's guilty debt admission; no quote attached to jaime-frees-tyrion-from-the-black-cells node yet | S109 tywin-arc verify |
| done | relationship | asos | asos-tyrion-11.md:133 | "Your brother can be most persuasive." — Varys confirming it was Jaime who recruited him to the escape; clarifies the Jaime-as-instigator vs Varys-as-orchestrator dynamic | S109 tywin-arc verify |
| done | foreshadowing | asos | asos-tyrion-10.md:159 | "We are puppets dancing on the strings of those who came before us, and one day our own children will take up our strings and dance on in our steads." — Tyrion reflecting on dynastic causation; foreshadows his patricide breaking the chain | S109 tywin-arc verify |
| done | quote | acok | acok-davos-03 | "A wall of red-hot steel, blazing wood, and swirling green flame stretched before him. The mouth of the Blackwater Rush had turned into the mouth of hell." — Davos; wildfire atmosphere; no quote on battle-of-the-blackwater node | 2026-06-20 arc-dip |
| open | quote | acok | acok-sansa-08 | "It was Lord Renly! Lord Renly with his tall spear in his hand!" — Dontos to Sansa; Garlan-as-Renly; load-bearing for joffrey-sets-sansa-aside node (no quote currently) | 2026-06-20 arc-dip **[S113: cite WRONG — line not in acok-sansa-08; Garlan-as-Renly's-ghost is a Blackwater Sansa chapter, re-resolve before attach]** |
| done | place | asos | asos-tyrion-01 | "My hirelings betray me, my friends are scourged and shamed, and I lie here rotting." — Tyrion post-Blackwater wound recovery bitterness; atmosphere/quote for battle-of-the-blackwater aftermath | 2026-06-20 arc-dip |
| done | quote | acok | acok-sansa-08:19 | "Joffrey had to step gingerly around it as he descended to embrace his grandfather and proclaim him Savior of the City." — Sansa POV; sharp tone; no direct-quote on savior-of-the-city or tywin-named node | 2026-06-20 Q12 research |
| done | quote | acok | acok-sansa-08:21 | "Joff fastened the Hand's chain of office around his neck." — Tywin restored as Hand; link to tywin-named-savior-of-the-city event; no book-quote on Hand-of-the-King node | 2026-06-20 Q12 research |
| done | quote | acok | acok-sansa-08:41 | "'set Sansa Stark aside. The Lady Margaery will make you a far more suitable queen.'" — Cersei's explicit framing of the Stark dismissal; load-bearing for joffrey-sets-sansa-aside node ## Quotes | 2026-06-20 Q12 research |
| done | appearance | acok | acok-sansa-08:23 | Mace Tyrell description: "a once-powerful man gone to fat, yet still handsome"; Tyrells' identical green velvet trimmed with sable; physical appearance for Mace/Loras/Garlan nodes | 2026-06-20 Q12 research |
| done | quote | asos | asos-davos-02:25 | "Captain Khorane had told him of the end of Stannis's hopes, on the night the river burned. The Lannisters had taken him from the flank, and his fickle bannermen had abandoned him by the hundreds in the hour of his greatest need." — grounding for stannis-retreats-to-dragonstone | 2026-06-20 Q12 research |
| done | place | asos | asos-davos-02:153 | "Thousands sailed up the Blackwater Rush, and hundreds came back." — Dragonstone dock streets post-battle; atmosphere/body-count; potential quote for battle-of-the-blackwater node ## Aftermath | 2026-06-20 Q12 research |
| done | quote | asos | asos-davos-02:89 | "'Since the battle, he sees no one, but broods in his Stone Drum.'" — Salladhor Saan on Stannis post-Blackwater isolation on Dragonstone; character state; useful for stannis-retreats node | 2026-06-20 Q12 research |
| done | quote | acok | acok-sansa-08:19 | "Joffrey had to step gingerly around it as he descended to embrace his grandfather and proclaim him Savior of the City." — exact cite for tywin-named-savior-of-the-city ## Quotes; already used in node | 2026-06-20 Q12 verify |
| done | hospitality | asos | asos-davos-02:45 | Salladhor Saan offers Davos cracked green olives, white cheese, hot red wine with cloves and lime in cabin of Bountiful Harvest — lavish shipboard hospitality scene; Salla food moment | 2026-06-20 Q12 verify |
| done | appearance | acok | acok-sansa-08:15 | Tywin's war armor: "all burnished red steel, inlaid with golden scrollwork... rondels were sunbursts... ruby eyes... cloth-of-gold cloak... gilded horse armor" — best physical description of Tywin armored | 2026-06-20 Q12 verify |
| done | quote | asos | asos-davos-02:35 | "Did none keep faith?" / "Some few... The queen's kin, them in chief. We took off many who wore the fox-and-flowers." — loyalty snapshot post-Blackwater; useful for House Florent and loyalty edges | 2026-06-20 Q12 verify |
| open | quote | agot | agot-eddard-08:13 | "The whore is pregnant! ... I want them dead, mother and child both, and that fool Viserys as well." — Robert's council order to kill Daenerys; key causal load-bearing quote for Robert-orders-Dany-assassination event node (currently only Ned's cancellation is modeled) | 2026-06-20 plan-review |
| open | quote | agot | agot-daenerys-06:179 | "I will take my khalasar west to where the world ends, and ride the wooden horses across the black salt water as no khal has done before." — Drogo's westward vow immediately after the wine merchant assassination attempt; load-bearing for MOTIVATES edge from assassination-attempt → drogo-s-westward-vow node (neither node nor edge exists) | 2026-06-20 plan-review |
| open | quote | agot | agot-arya-03:89-93 | Varys-Illyrio underground meeting: "If one Hand can die, why not a second?" + "The princess is with child. The khal will not bestir himself until his son is born." + "the wolf and the lion will soon be at each other's throats, whether we will it or no." — earliest on-page evidence of Varys-Illyrio conspiracy; AGOT Arya III ch33; strong load-bearing quote for varys-illyrio edge | 2026-06-20 plan-review |
| open | relationship | agot | agot-daenerys-07:147 | Ser Jorah produces Illyrio's letter: "Robert Baratheon offers lands and lordships for your death, or your brother's." — confirms Jorah's information-channel role to Varys/Robert; load-bearing for JORAH_INFORMS_FOR / spy relationship edge | 2026-06-20 plan-review |
| done | quote | agot | agot-arya-05:161 | execution-of-eddard-stark node has NO ## Quotes block (major event, bare) — attach Joffrey's "So long as I am your king, treason shall never go unpunished. Ser Ilyn, bring me his head!" (the trigger line, currently only an edge evidence-quote) + Ned's confession framing. Matt-flagged: do in next 3-5 sessions. | 2026-06-20 strategy review |
| done | place | agot | agot-catelyn-11.md:127 | Riverrun godswood: "green canopy of leaves, surrounded by tall redwoods and great old elms … a slender weirwood with a face more sad than fierce" — lords kneeling before it; notable setting for the proclamation prayer scene | S113 J3 research |
| done | appearance | agot | agot-catelyn-11.md:19 | Lord Tytos Blackwood: "hard pike of a man with close-cropped salt-and-pepper whiskers and a hook nose … bright yellow armor inlaid with jet in elaborate vine-and-leaf patterns, cloak sewn from raven feathers" — first-class appearance for tytos-blackwood node | S113 J3 research |
| done | quote | agot | agot-catelyn-11.md:25 | Edmure to Catelyn on hearing of Ned: "When we heard about Lord Eddard … the Lannisters will pay, I swear it, you will have your vengeance." — first on-page confirmation that news of Ned's execution has reached Riverrun; load-bearing for causal arc | S113 J3 research |
| done | quote | agot | agot-catelyn-11.md:155 | Galbart Glover to Robb at the council: "You cannot mean to hold to Joffrey, my lord. He put your father to death." — explicit citation of Ned's execution as the council's political crisis; load-bearing causal link | S113 J3 research |
| done | quote | agot | agot-catelyn-11.md:179 | Robb to Catelyn: "My lady, they murdered my lord father, your husband … This is the only peace I have for Lannisters." — unsheathed longsword; Robb's grief-as-war-mandate; load-bearing for MOTIVATES edge | S113 J3 research |
| done | foreshadowing | agot | agot-catelyn-11.md:205 | "She looked at her son, watched him as he listened to the lords debate … He had pledged himself to marry a daughter of Walder Frey, but she saw his true bride plain before her now: the sword he had laid on the table." — Catelyn's ominous framing; Frey bride foreshadows Red Wedding | S113 J3 research |
| done | quote | agot | agot-catelyn-11.md:209 | Greatjon's proclamation speech: "Why shouldn't we rule ourselves again? It was the dragons we married, and the dragons are all dead!" + "The King in the North!" — the secession rationale and the proclamation line together; primary load-bearing quote for robb-proclaimed-king-in-the-north | S113 J3 research |
| done | quote | agot | agot-catelyn-11.md:215 | "bending their knees and shouting the old words that had not been heard in the realm for more than three hundred years, since Aegon the Dragon had come to make the Seven Kingdoms one" — establishes historical weight of the proclamation; no direct quote on robb-proclaimed-king node yet | S113 J3 research |
| open | quote | asos | asos-tyrion-10 | `gregor-confesses-and-kills-oberyn` node is BARE (no `## Quotes`) — surfaced by the S112 Loremaster demo as a graph gap. Attach Gregor's confession + Oberyn's death (the Red Viper vs the Mountain trial-by-combat: "Elia Martell … I killed her screaming whelp … then I raped her … then I smashed her fucking head in"). Find exact line in asos-tyrion-10. Matt demo note #3. | S113 demo-window note |
| open | quote | affc | affc-cersei-10 | `cersei-is-captured-in-the-sept` node is a bare Plate-3 skeleton (no `## Quotes`) — has role edges (the-faith AGENT_IN, high-sparrow COMMANDS_IN). Attach the High Sparrow's arrest line "seize her at the altar of the Mother" + charges (murder/treason/regicide). Surfaced by AFFC smoke test. | 2026-06-20 affc-smoke |
| open | quote | affc | affc-cersei VIII | `cersei-plots-against-margaery` node is a bare Plate-3 skeleton (no `## Quotes`) — the false-adultery frame-up against Margaery. Attach Cersei's scheming + the Blue Bard plot. | 2026-06-20 affc-smoke |
| open | quote | affc | affc (Cersei) | `cersei-is-stripped-and-imprisoned` bare skeleton (no `## Quotes`) — Cersei's confinement in the Sept cell before the walk. Find chapter:line. | 2026-06-20 affc-smoke |
| open | quote | affc | affc-cersei (walk) | `walk-of-atonement` is a generic wiki custom node (empty aliases, no `## Quotes`); Cersei's walk of shame ("Shame. Shame. Shame.") has no in-saga quote attached. Add spaced aliases + the walk quote when the Cersei arc is built. | 2026-06-20 affc-smoke |
| open | quote | affc | affc-dorne (Arianne/Hotah) | `arrest-of-the-sand-snakes` bare skeleton (no `## Quotes`) — Doran jails the Sand Snakes after the failed plot to crown Myrcella. Find chapter:line. | 2026-06-20 affc-smoke |
| open | foreshadowing | affc | affc-cersei-01.md:13 | Cersei's dream: sitting the Iron Throne naked, the dwarf laughing — direct foreshadowing of the walk of atonement ("she realized she was naked"; "the throne engulfed her"); Maggy prophecy parallel. Load-bearing opening image. | 2026-06-20 cersei-arc research |
| done | quote | affc | affc-cersei-06.md:265 | "The Faith Militant reborn … that would be the answer to three hundred years of prayer, Your Grace." High Sparrow leaping at Cersei's bait — the rearming offer. Load-bearing for cersei-rearms-the-faith node. | 2026-06-20 cersei-arc research |
| done | quote | affc | affc-cersei-06.md:273 | "This debt shall be forgiven, and King Tommen will have his blessing. The Warrior's Sons shall escort me to him … reborn as Poor Fellows as of old." — the deal: Cersei trades debt forgiveness + legal arming in exchange for Tommen's blessing. | 2026-06-20 cersei-arc research |
| open | quote | affc | affc-cersei-09.md:311 | "you must take yourself to the Great Sept of Baelor this very night and speak with the High Septon … Tell him how you bedded Margaery and her cousins." — Cersei's script to Osney. Load-bearing for the frame-up execution beat. | 2026-06-20 cersei-arc research |
| open | foreshadowing | affc | affc-cersei-09.md:329 | "The best lies have some truth in 'em … you want me to go tell how I fucked a queen …" — Osney half-confessing that he has slept with Cersei; foreshadows his true confession naming her instead. | 2026-06-20 cersei-arc research |
| open | quote | affc | affc-cersei-10.md:49 | "No golden shrouds, no valonqar, I am free of your croaking malice at last." — Cersei celebrating Margaery's arrest, believing herself proof against Maggy's prophecy, just as the trap closes. Irony quote for the arc. | 2026-06-20 cersei-arc research |
