# Lens D — Existing-Node ↔ Existing-Node Causal Wiring
# Jon Snow / the Wall enrichment dip (S145)

> **PROPOSE, don't mint.** All edges verified by `graph-query.py --neighbors` + `find graph/nodes -name`.
> Verb rationale included for each edge. Cross-container seams flagged.
> Dedup confirmed: every listed edge is ABSENT from edges.jsonl.

---

## Seam 1: Stannis chain — NORTH ↔ WO5K

### Current wiring summary (from `--neighbors`)
- `stannis-moves-to-the-wall` → CAUSES → `battle-beneath-the-wall` ✅
- `battle-beneath-the-wall` → CAUSES → `mance-rayder-brought-to-execution` ✅
- `battle-beneath-the-wall` → ENABLES → `jon-elected-lord-commander` ✅
- `battle-beneath-the-wall` → ENABLES → `fight-by-deepwood-motte` ✅ (WO5K side)
- `fight-by-deepwood-motte` → ENABLES → `stannis-march-on-winterfell` ✅
- `stannis-march-on-winterfell` → ENABLES → `stannis-s-army-stalls-at-crofters-village` ✅
- `stannis-s-army-stalls-at-crofters-village` has **0 outgoing edges** — dead end

The Stannis chain at the Wall/North end is largely wired. But:

1. `stannis-s-army-stalls-at-crofters-village` has zero outgoing causal edges despite being the narrative context the Pink Letter arrives against.
2. The Pink Letter explicitly presupposes Stannis's stalled-and-defeated state as its *content* — but `pink-letter-delivered` has no backward causal link to the stall.

---

### EDGE PROPOSAL D-1

**`stannis-s-army-stalls-at-crofters-village` –ENABLES–> `pink-letter-delivered`**

- **Tier:** 2
- **Rationale:** ENABLES (not CAUSES) because the stall is the precondition that allows Ramsay to claim Stannis is defeated and write the letter; it doesn't mechanically produce the letter. The stall puts Stannis's army in a state (snowbound, communications severed) that makes the claim of his defeat plausible and actionable. Jon's internal logic in Jon XIII — "He has Lightbringer. He talks of heads upon the walls of Winterfell … No. There is truth in there" — turns on the letter's details seeming credible, which depends on the stall having actually occurred. Ramsay could not credibly claim "smashed in seven days of battle" unless Stannis had indeed vanished into the snows.
- **VERBATIM QUOTE:**

> Your false king is dead, bastard. He and all his host were smashed in seven days of battle. I have his magic sword. Tell his red whore.

— Jon XIV (adwd-jon-13.md:229); Ramsay's claim presupposes the stall/defeat context.

And:

> "He has Lightbringer. He talks of heads upon the walls of Winterfell. He knows about the spearwives and their number." He knows about Mance Rayder. "No. There is truth in there."

— adwd-jon-13.md:261; Jon accepts the letter as credible because conditions are consistent with Stannis's doom.

- **Dedup status:** `stannis-s-army-stalls-at-crofters-village` EXISTS ✅; `pink-letter-delivered` EXISTS ✅. No outgoing edge from stall to letter in edges.jsonl.
- **Cross-container seam:** YES — NORTH container event (stall) → NORTH event (pink letter). Also bridges WO5K → NORTH causally (Ramsay's Bolton military success that the letter claims).
- **NOTE:** Do NOT wire to an unwritten `battle-of-winterfell` or `battle-of-ice`. The stall is the last wired NORTH state; Ramsay's claim of victory is his assertion, not a confirmed event node.

---

### EDGE PROPOSAL D-2

**`pink-letter-delivered` –ENABLES–> `the-shieldhall-speech`** *(depends on Lens B mint)*

- **Tier:** 1
- **Rationale:** ENABLES (not TRIGGERS) because the letter is the necessary precondition; it is the stimulus Jon reads and deliberates over for "the best part of two hours" before calling the Shieldhall. The speech is Jon's chosen response — a human decision — not an automatic reflex. TRIGGERS would imply the letter itself fired the speech; instead, Jon processes, deliberates, and chooses to call the assembly. The letter ENABLES the speech by supplying the content Jon will announce.

> He cracked the seal, flattened the parchment, and read. … "I think we had best change the plan," Jon Snow said. They talked for the best part of two hours.

— adwd-jon-13.md:227 / 267-269

- **Dedup status:** `pink-letter-delivered` EXISTS ✅; `the-shieldhall-speech` being minted by Lens B — **flag: depends on Lens B mint**.
- **Cross-container:** NORTH internal. High-value structural fix: currently `pink-letter-delivered` TRIGGERS `jon-is-stabbed-repeatedly` directly, collapsing the Shieldhall speech. This edge restores the intermediate beat.

---

### EDGE PROPOSAL D-3

**`jon-allows-free-folk-through-the-wall` –ENABLES–> `the-shieldhall-speech`** *(depends on Lens B mint)*

- **Tier:** 1
- **Rationale:** ENABLES because Jon's policy of integrating the free folk is the reason the Shieldhall itself is populated by wildlings who answer his call — without the free-folk-through-the-wall decree, the Shieldhall crowd is only Night's Watch brothers, not the "five to one" wildling majority that roars to follow Jon south. The speech's success depends structurally on the free folk already being inside the Wall and given castle garrisons. This is a precondition of the scene, not the proximate spark.

> The wildlings outnumbered the crows by five to one, judging by how little black he saw.

— adwd-jon-13.md:283 (Shieldhall scene; the crowd that validates Jon's decision is the result of his free-folk policy)

- **Dedup status:** `jon-allows-free-folk-through-the-wall` EXISTS ✅; `the-shieldhall-speech` depends on Lens B mint.
- **Cross-container:** NORTH internal.

---

## Seam 2: The Conspiracy / Stabbing Chain

### Current wiring
- `execution-of-janos-slynt` –MOTIVATES–> `bowen-marsh` ✅
- `jon-allows-free-folk-through-the-wall` –MOTIVATES–> `bowen-marsh` ✅
- `pink-letter-delivered` –TRIGGERS–> `jon-is-stabbed-repeatedly` ✅
- `bowen-marsh` AGENT_IN `jon-is-stabbed-repeatedly` ✅
- `wick-whittlestick` AGENT_IN `jon-is-stabbed-repeatedly` ✅ (per baseline note)
- `jon-snow` VICTIM_IN `jon-is-stabbed-repeatedly` ✅

### EDGE PROPOSAL D-4

**`othell-yarwyck` –MOTIVATES–> `bowen-marsh`** *(the conspiracy needs a conspires-with edge, but that type is unpopulated — use MOTIVATES as the nearest available)*

**NEEDS FRESH-VERIFY** — see rationale.

- **Tier:** 2
- **Rationale:** The text shows Yarwyck and Marsh acting as a unit throughout Jon XIII, consistently opposing the free-folk integration policy in the same terms, and both are "slipping out" of the Shieldhall together at the moment the conspirators depart (adwd-jon-13.md:299). However, the text does not show Yarwyck personally raising a blade; the stabbing scene shows Wick and Marsh, not Yarwyck. MOTIVATES is the right verb if Yarwyck's sustained resistance provides the ideological rationale that strengthens Marsh's resolve. But the text stops short of proving active conspiracy rather than passive agreement — Yarwyck slipping out is consistent with either cowardice or coordination. NEEDS FRESH-VERIFY: is there any other ADWD passage making Yarwyck's foreknowledge more explicit?

> Yarwyck and Marsh were slipping out, he saw, and all their men behind them.

— adwd-jon-13.md:299 (Shieldhall; the conspirators withdraw before the stabbing)

- **Dedup status:** `othell-yarwyck` EXISTS ✅; `bowen-marsh` EXISTS ✅. Check edges.jsonl for any existing Yarwyck→Marsh or Yarwyck→stabbing edge before minting.

---

### EDGE PROPOSAL D-5

**`jon-allows-free-folk-through-the-wall` –MOTIVATES–> `othell-yarwyck`**

- **Tier:** 1
- **Rationale:** The text explicitly names Yarwyck's grievances over the free-folk integration policy — his specific complaints about Borroq, the wild boar, Stonedoor being "too isolated," the wildling builders being "more trouble than they're worth." The chapter establishes Yarwyck's disapproval as running bone-deep (the same framing used for Marsh). His policy opposition is a documented, explicit motivation for his faction's hostility to Jon's leadership.

> Especially when it concerned the free folk, where their disapproval went bone deep. … As for Borroq, Othell Yarwyck claimed the woods north of Stonedoor were full of wild boars. Who was to say the skinchanger would not make his own pig army?

— adwd-jon-13.md:149

- **Dedup status:** `jon-allows-free-folk-through-the-wall` EXISTS ✅; `othell-yarwyck` EXISTS ✅.

---

## Seam 3: The Glamour / Mance-as-Rattleshirt

### Current state
`mance-rayder` and `melisandre` both exist. `rattleshirt` node does NOT exist (confirmed via `find`). The executed man was Rattleshirt-glamoured-as-Mance; Mance was Mance-glamoured-as-Rattleshirt. The execution scene and its glamour are a causal precondition for the spearwife mission (Mance sent to Winterfell, which the Pink Letter references).

### EDGE PROPOSAL D-6

**`mance-rayder-brought-to-execution` –ENABLES–> `pink-letter-delivered`**

- **Tier:** 1
- **Rationale:** ENABLES because the glamour swap at the execution is the precondition for Mance surviving and going to Winterfell disguised, which is precisely what the Pink Letter reveals and what gives the letter some of its credibility. Ramsay writes "You sent him to Winterfell to steal my bride from me" — Mance's survival and mission (enabled by the execution/glamour) are what the Pink Letter directly responds to. Without the glamour at the execution, Mance is truly dead, there are no spearwives at Winterfell, and the Pink Letter's specific taunts about Mance and the six whores collapse. ENABLES not CAUSES because the letter has multiple causes (Ramsay's intent, Ramsay's capture of Mance); the execution/glamour is the structural precondition of Mance's presence in Winterfell.

> "You told the world you burned the King-Beyond-the-Wall. Instead you sent him to Winterfell to steal my bride from me. … I have him in a cage for all the north to see, proof of your lies. The cage is cold, but I have made him a warm cloak from the skins of the six whores who came with him to Winterfell."

— adwd-jon-13.md:231-233

And the glamour mechanics confirmed:

> "She burned the Lord of Bones." … "Call it what you will. Glamor, seeming, illusion."

— adwd-melisandre-01.md:259 / 263

- **Dedup status:** `mance-rayder-brought-to-execution` EXISTS ✅; `pink-letter-delivered` EXISTS ✅. No such edge in edges.jsonl.
- **Cross-container:** NORTH internal. Highest-value structural fix: closes a genuine logical gap (why can the Pink Letter credibly taunt about Mance at all?).

---

### EDGE PROPOSAL D-7

**`melisandre` –ENABLES–> `mance-rayder-brought-to-execution`**

*(the glamour swap that saves Mance's life)*

- **Tier:** 1
- **Rationale:** ENABLES because Melisandre's glamour is the necessary precondition for the execution producing the result it does (Rattleshirt dies; Mance survives). Without the glamour, the execution kills Mance and the entire downstream (spearwives at Winterfell, Pink Letter content) collapses. This is not CAUSES because the execution itself is caused by Stannis's order and the battle's outcome; Melisandre ENABLES the survival-through-deception outcome that makes the execution narratively consequential.

> When the flames had licked at Rattleshirt, the ruby at her throat had grown so hot that she had feared her own flesh might start to smoke and blacken. Thankfully Lord Snow had delivered her from that agony with his arrows.

— adwd-melisandre-01.md:269

Note: "Lord Snow delivered her from that agony" — Jon's mercy arrows on the burning figure are the proximate termination of the glamour performance.

- **Dedup status:** `melisandre` EXISTS ✅; `mance-rayder-brought-to-execution` EXISTS ✅. Melisandre currently has no outgoing causal edge to the execution event.

---

## Seam 4: Arnolf Karstark Treachery → Stannis Chain

### EDGE PROPOSAL D-8

**`arnolf-karstark` –ENABLES–> `stannis-s-army-stalls-at-crofters-village`**

**NEEDS FRESH-VERIFY** — see rationale.

- **Tier:** 2
- **Rationale:** Alys Karstark explicitly states that Arnolf "cast his lot with Roose Bolton long ago" and is rushing to Winterfell to "put his dagger in your king's back." The betrayal — bringing troops that nominally swell Stannis's force but are actually aligned with Bolton — is a contributing precondition to the march's failure. ENABLES not CAUSES because the stall's immediate cause is the blizzard; Arnolf's treachery is a structural weakness (Bolton intelligence on Stannis's movements, undermined northern support) that ENABLES the army to be caught, starved, and outmaneuvered. However: the published text does not show Arnolf actively betraying Stannis during the stall (the battle is unwritten). NEEDS FRESH-VERIFY: is the stall-ARNOLF link sufficiently grounded in the published text, or is the act of betrayal properly downstream of published chapters?

> "Lord Stannis is marching to a slaughter. So he cannot help me, and would not even if he could."

— adwd-jon-09.md:333 (Alys Karstark names the treachery but the stall's causal connection to Arnolf's betrayal is partially inference)

- **Dedup status:** `arnolf-karstark` EXISTS ✅; `stannis-s-army-stalls-at-crofters-village` EXISTS ✅. `arnolf-karstark` already has BETRAYS→`stannis-baratheon` and ALLIES_WITH→`roose-bolton`. This would add the event-chain link.

---

## Seam 5: bastard-letter artifact ↔ pink-letter-delivered event

### EDGE PROPOSAL D-9

**`bastard-letter` –CAUSES–> `pink-letter-delivered`**

- **Tier:** 1
- **Rationale:** CAUSES because the artifact *is* the event in physical form — the letter's delivery is the event; the object authored it. This is the standard artifact→event-of-delivery wiring. The `bastard-letter` node currently has zero edges despite the node existing. This is a minimal structural hook.

> And the letter was sealed with a smear of hard pink wax.

— adwd-jon-13.md:227 (the artifact delivers itself as the event)

- **Dedup status:** `bastard-letter` EXISTS ✅; `pink-letter-delivered` EXISTS ✅. `bastard-letter` has 0 outgoing and 0 incoming edges — completely isolated.

---

## Edge Summary Table

| # | Source | Type | Target | Tier | Cross-container | Flag |
|---|--------|------|--------|------|-----------------|------|
| D-1 | `stannis-s-army-stalls-at-crofters-village` | ENABLES | `pink-letter-delivered` | 2 | Partial (NORTH→NORTH; WO5K-context) | — |
| D-2 | `pink-letter-delivered` | ENABLES | `the-shieldhall-speech` | 1 | NORTH internal | Depends on Lens B mint |
| D-3 | `jon-allows-free-folk-through-the-wall` | ENABLES | `the-shieldhall-speech` | 1 | NORTH internal | Depends on Lens B mint |
| D-4 | `othell-yarwyck` | MOTIVATES | `bowen-marsh` | 2 | NORTH internal | NEEDS FRESH-VERIFY |
| D-5 | `jon-allows-free-folk-through-the-wall` | MOTIVATES | `othell-yarwyck` | 1 | NORTH internal | — |
| D-6 | `mance-rayder-brought-to-execution` | ENABLES | `pink-letter-delivered` | 1 | NORTH internal | Highest-value fix |
| D-7 | `melisandre` | ENABLES | `mance-rayder-brought-to-execution` | 1 | NORTH internal | — |
| D-8 | `arnolf-karstark` | ENABLES | `stannis-s-army-stalls-at-crofters-village` | 2 | NORTH internal | NEEDS FRESH-VERIFY |
| D-9 | `bastard-letter` | CAUSES | `pink-letter-delivered` | 1 | NORTH internal | Artifact isolation fix |

---

## HARVEST

- adwd-jon-13.md:93 / food / "bean-and-bacon soup" — Rattleshirt (Mance) eating by the fire; Bowen Marsh complaining nearby; hospitality-as-tension scene
- adwd-jon-13.md:131-135 / description / Ghost bristling and baring teeth at Jon before the stabbing — animal-sense foreshadowing; raven screaming "Snow"
- adwd-jon-13.md:157 / food / Satin pours mulled wine for Marsh/Yarwyck conference; Marsh ignores the wine, Yarwyck drinks two cups — character texture
- adwd-jon-13.md:195 / food / Tormund's 50 (not 80) wildling fighters timed arrival after shoveling done — Tormund as Tall-Talker; also note the draft horses / ox context for Hardhome supply logistics
- adwd-jon-13.md:283-295 / description / Shieldhall as location: one of the oldest parts of Castle Black, dark stone, worm-eaten rafters, rat-infested cellars, "sad grey things with faded paint" shields — physical decay of the Watch; high-value for location enrichment of `shieldhall` node
- adwd-jon-13.md:309-313 / description / Wun Wun swinging Ser Patrek's corpse like a morningstar against the tower; "white wool cloak bordered in cloth-of-silver, patterned with blue stars" (Ser Patrek's distinctive heraldry) — vivid physical description; hospitality-violation register (guest killed at castle)
- adwd-melisandre-01.md:47 / food / "greybeards and cripples," gelded soldiers, "two drunkards and a craven" — Melisandre's depleted guard complement; grim hospitality register
- adwd-melisandre-01.md:71 / food / Melisandre's breakfast: "nettle tea, a boiled egg, and bread with butter. Fresh bread, if you please, not fried." — rare detailed food order; the bread ends up being eaten by Mance
- adwd-melisandre-01.md:151-155 / description / Three rangers' severed heads on ash spears, beards full of ice, "white hoods" of snow, "empty sockets … black and bloody holes" — strong physical description for `castle-black` location and the ranging aftermath; foreshadowing of the wight threat
