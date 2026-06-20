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

| status | kind | book | chapter:line | note | found during |
|--------|------|------|--------------|------|--------------|
| open | appearance | agot | agot-eddard-13:35 | Renly in bloodied hunting greens just after the boar kills Robert | S108 B3 research |
| open | quote | agot | agot-eddard-13:169 | Ned refuses to seize Cersei's children while Robert dies: "I will not dishonor his last hours on earth by shedding blood in his halls" — homeless load-bearing (Ned's fatal honor); no beat-node home | S108 B3 research |
| open | food | agot | agot-eddard-14:43 | "a cup of sweet beer" offered to Pycelle in the Hand's solar — hospitality detail | S108 B3 research |
| open | appearance | agot | agot-eddard-14:49 | Littlefinger "blue velvets and silver mockingbird cape … boots dusty from riding" | S108 B3 research |
| open | appearance | agot | agot-eddard-14:51 | Varys "in a wash of lavender, pink from his bath, his plump face scrubbed and freshly powdered, his soft slippers all but soundless" | S108 B3 research |
| open | food | agot | agot-eddard-15:157 | "bread and cheese and the milk of the poppy" — `object.food` (bread/cheese) + `concept.medical` (milk of the poppy); the quote itself already attached to `ned-confesses-to-treason` | S108 B3 research |
| open | appearance | asos | wiki:Jeyne_Westerling | "curly chestnut hair, heart-shaped face, shy smile, doe-like soft brown eyes; slender and willowy, small apple-sized breasts" — first-class appearance record, no chapter:line yet | S109 fresh-arc-dip |
| open | quote | asos | wiki:Storming_of_the_Crag / asos-catelyn-02 | Robb: "I took her castle and she took my heart. … I took an arrow in the arm … Jeyne had me taken to her own bed, and she nursed me until the fever passed. And she was with me when the Greatjon brought me the news … That night, she … she comforted me, Mother." — load-bearing quote for robb-weds-jeyne-westerling beat, no node quote yet | S109 fresh-arc-dip |
| open | food | acok | wiki:Storming_of_the_Crag / acok-catelyn-07 | smallfolk at Riverrun celebrate with "nut-brown ale" after Crag victory + Edmure's return — hospitality/food detail | S109 fresh-arc-dip |
| open | relationship | acok | wiki:Greyjoy's_Rebellion | Rodrik Harlaw "unsuccessfully advised Balon against rebelling" — ADVISES/OPPOSES edge between harlaw and balon-greyjoy or greyjoy-rebellion may be missing | S109 fresh-arc-dip |
| open | quote | asos | wiki:Fall_of_Astapor / asos-daenerys-03 | Daenerys keeps secret that she understands Kraznys's High Valyrian while he insults her — tactical deception, load-bearing for fall-of-astapor; no quote on that node yet | S109 fresh-arc-dip |
| open | quote | asos | asos-tyrion-11.md:27 | "Handless and Noseless, the Lannister boys." — Tyrion's greeting to Jaime in the black cells; appearance + dark comedy double | S109 tywin-arc research |
| open | appearance | asos | asos-tyrion-11.md:25 | "Jaime was gaunt, his hair hacked short" — Jaime's post-captivity appearance on the first page of the freeing scene | S109 tywin-arc research |
| open | quote | asos | asos-tyrion-11.md:119 | "Cersei is a lying whore, she's been fucking Lancel and Osmund Kettleblack and probably Moon Boy for all I know." — Tyrion's bombshell revelation to Jaime; load-bearing for Cersei-adultery arc | S109 tywin-arc research |
| open | object | asos | asos-tyrion-11.md:197 | Shae's "chain of linked golden hands, each holding the next" — Tywin's personal token/gift worn as collar; named artifact detail | S109 tywin-arc research |
| open | place | asos | asos-tyrion-11.md:145 | Varys describes the four dungeon levels under the Red Keep — vivid atmosphere of 4th-level dark cells; "once a man is taken down to the fourth level, he never sees the sun again" | S109 tywin-arc research |
| open | quote | asos | asos-tyrion-11.md:267-269 | "Lord Tywin Lannister did not, in the end, shit gold." — the chapter's last line; iconic; no quote on assassination-of-tywin-lannister node yet | S109 tywin-arc research |
| open | quote | asos | asos-jaime-07.md:209 | "He is still my brother. I am in no fit state to be killing anyone." — Jaime refusing Cersei in the sept; captures Jaime's moral stance at the trial period | S109 tywin-arc research |
| open | quote | asos | asos-tyrion-10.md:249 | "He never heard his father speak the words that condemned him." — POV gap: Tyrion's condemnation is narrated obliquely; load-bearing for how the sentence lands | S109 tywin-arc research |
| open | food | asos | asos-tyrion-10.md:101 | Tyrion's pre-combat breakfast: fried bread, blood sausage, applecakes, double eggs with onions and fiery Dornish peppers — named dish detail, Dornish peppers notable | S109 tywin-arc verify |
| open | appearance | asos | asos-tyrion-10.md:167-173 | Gregor's full pre-combat armour description: flat-topped greathelm bolted to gorget, breaths at mouth/nose, narrow vision slit, stone fist crest, 7-pointed star painted over Clegane hounds; Oberyn's: copper scales, removed visor, round polished shield, soft red gloves, ash spear 8ft with 2ft steel leaf-head | S109 tywin-arc verify |
| open | quote | asos | asos-tyrion-10.md:43 | "I saved you all, Tyrion thought. I saved this vile city and all your worthless lives." — Tyrion watching the laughter at "my giant of Lannister"; core bitterness quote; no quote on trial-of-tyrion-lannister node yet | S109 tywin-arc verify |
| open | appearance | asos | asos-tyrion-11.md:25 | Jaime's appearance when he enters the black cells: "gaunt, his hair hacked short... I left a hand at Harrenhal" — stump of right wrist; first appearance-flagged reunion beat | S109 tywin-arc verify |
| open | appearance | asos | asos-tyrion-11.md:197-198 | Shae wearing "a chain of linked golden hands, each holding the next" — the Hand's collar; notable visual / object detail; Tywin's possessiveness made visible | S109 tywin-arc verify |
| open | place | asos | asos-tyrion-11.md:153-157 | The juncture below the Tower of the Hand: round chamber, five iron-barred doors + ceiling shaft with rungs, ornate dragon's-head brazier with orange-glowing coals, mosaic three-headed dragon in red and black tiles; below the Tower of the Hand; Varys says "We are below the Tower of the Hand" | S109 tywin-arc verify |
| open | quote | asos | asos-tyrion-11.md:63 | "Thank you, Brother. For my life." / "It was... a debt I owed you." — Jaime's guilty debt admission; no quote attached to jaime-frees-tyrion-from-the-black-cells node yet | S109 tywin-arc verify |
| open | relationship | asos | asos-tyrion-11.md:133 | "Your brother can be most persuasive." — Varys confirming it was Jaime who recruited him to the escape; clarifies the Jaime-as-instigator vs Varys-as-orchestrator dynamic | S109 tywin-arc verify |
| open | foreshadowing | asos | asos-tyrion-10.md:159 | "We are puppets dancing on the strings of those who came before us, and one day our own children will take up our strings and dance on in our steads." — Tyrion reflecting on dynastic causation; foreshadows his patricide breaking the chain | S109 tywin-arc verify |
