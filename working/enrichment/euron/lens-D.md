# Lens D — Existing-node ↔ existing-node causal wiring (cross-arc seams) — A1.6 Kingsmoot / Euron proposal (S157)

## Node-existence audit (pre-proposal)

All proposed targets were verified via `graph-query.py --neighbors` before proposing any edge.

**CONFIRMED EXISTING (relevant nodes):**
- `taking-of-the-shields` — event.battle (2 out / 2 in; NO participant roles, NO LOCATED_AT, cOut=2 all causal)
- `victarion-slays-multiple-defenders` — event.incident (cOut=0, **islanded** — only cIn edges from AGENT_IN/VICTIM_IN)
- `silence` — object.artifact (0 edges graph-wide)
- `iron-victory` — object.artifact (0 edges graph-wide)
- `dragonbinder` — object.artifact (1 edge: WIELDED_IN → voyage beat)
- `mander` — place.location (0 edges graph-wide)
- `shield-islands` — place.location (5 in, 0 out)
- `naggas-hill` — place.location (0 edges graph-wide)
- `naggas-cradle` — place.location (0 edges graph-wide)
- `highgarden` — place.location (exists)
- `arbor` — place.location (exists)
- `oldtown` — place.location (exists)
- `redwyne-straits` — place.location (0 edges graph-wide)
- `anarchy-in-the-reach` — event.battle (**0 edges graph-wide — completely islanded**)
- `battle-of-the-shield-islands` — event.battle (same_as redirect to `taking-of-the-shields` — do NOT wire to this; use canonical slug)
- `paxter-redwyne` — character.human (17 edges, none connecting to taking-of-the-shields)
- `mace-tyrell` — character.human (29 edges, none connecting to taking-of-the-shields)
- `randyll-tarly` — character.human (exists; mentioned at the feast, "Lord Tarly bears the greatsword Heartsbane")
- `harras-harlaw` — character.human (7 out / 1 in; `HOLDS_TITLE lord-of-greyshield` exists, but NO AGENT_IN taking-of-the-shields)
- `nute-the-barber` — character.human (3 out / 1 in; `HOLDS_TITLE lord-of-oakenshield` exists, NO AGENT_IN taking-of-the-shields)
- `andrik-the-unsmiling` — character.human (`HOLDS_TITLE lord-of-southshield` exists, NO AGENT_IN)
- `maron-volmark` — character.human (`HOLDS_TITLE lord-of-greenshield` exists, NO AGENT_IN)
- `ragnor-pyke` — character.human (exists)
- `torwold-browntooth` — character.human (0 edges graph-wide)
- `rodrik-harlaw` — character.human (OPPOSES euron-greyjoy exists; NO PARTICIPATES_IN kingsmoot or taking)
- `burning-of-the-lannister-fleet` — event.battle (1 out; NO agent roles for Euron or Victarion)
- `kingsmoot-on-old-wyk` — event.ceremony (10 total edges; NO LOCATED_AT)
- `aeron-greyjoy` — character.human (OFFICIATES / PARTICIPATES gap confirmed; AGENT_IN kingsmoot exists)

**CONFIRMED NON-EXISTENT or wrong for wiring:**
- No `redwyne-fleet` faction node (only `house-redwyne` and `paxter-redwyne` as character).
- `battle-of-the-shield-islands` is a `same_as` redirect stub — do NOT wire to it; use `taking-of-the-shields`.
- The Redwyne fleet retaking of the Shields is TWOW-only — do NOT propose it.
- No `greyjoys-rebellion` node found (wiki has `greyjoy-rebellion`); `burning-of-the-lannister-fleet` PART_OF that event exists.

---

## Proposed NEW nodes

None. All proposable entities already exist as nodes. This lens is edge-only.

---

## Proposed NEW edges

### Block 1 — Taking of the Shields: participant roles (Gap #1 from baseline.md)

**D-01**
`victarion-greyjoy` **COMMANDS_IN** `taking-of-the-shields` | Tier-1 | no qualifier needed |
"The drums were pounding out a battle beat as the Iron Victory swept forward" + "The Drowned God had not shaped Victarion Greyjoy to fight with words at kingsmoots … This was why he had been put on earth" `affc-the-reaver-01:39`
Rationale: Victarion personally leads the assault on Southshield; the chapter is his POV throughout the taking. COMMANDS_IN (not AGENT_IN) because he directs the fleet action while also personally fighting — the distinction of strategic command from personal combat participation is preserved; he also gives orders to Nute etc.

**D-02**
`victarion-greyjoy` **AGENT_IN** `taking-of-the-shields` | Tier-1 | no qualifier |
"He vaulted over the gunwale, landing on the deck below with his golden cloak billowing behind him." `affc-the-reaver-01:13`
Rationale: Victarion personally boards, fights, and kills multiple defenders during the taking — AGENT_IN captures his direct participation as opposed to COMMANDS_IN's strategic role. Both edges are warranted by the text.

**D-03**
`victarion-slays-multiple-defenders` **SUB_BEAT_OF** `taking-of-the-shields` | Tier-1 |
"By then his ironborn had followed him down onto the deck of the broken longship." `affc-the-reaver-01:21`
Rationale: `victarion-slays-multiple-defenders` is causally islanded (cOut=0). The combat beat occurs during the attack on Southshield's defending longship — it is unambiguously a sub-beat of the taking-of-the-shields. This is the fix the baseline gap-list explicitly flagged.

**D-04**
`harras-harlaw` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"Rise, Ser Harras Harlaw, Lord of Greyshield." `affc-the-reaver-01:181`
Rationale: Euron awards Harras the lordship of Greyshield at the post-battle feast for "The Knight took Grimston by himself … he slew them all" during the taking. Harras is a direct participant. `HOLDS_TITLE lord-of-greyshield` already exists but AGENT_IN the taking event is not wired.

**D-05**
`nute-the-barber` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"Rise, Nute the Barber, Lord of Oakenshield." `affc-the-reaver-01:181`
Rationale: Nute is present throughout the assault (he reports "the day is ours," catches the captain's post-battle orders), and Euron elevates him to Lord of Oakenshield for his role. `HOLDS_TITLE lord-of-oakenshield` exists; AGENT_IN is not wired.

**D-06**
`andrik-the-unsmiling` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"Rise, Andrik the Unsmiling, Lord of Southshield." `affc-the-reaver-01:181`
Rationale: Andrik is present at the feast with plunder ("Andrik the Unsmiling staggered by with a woman under each arm"), awarded Southshield lordship for the taking. `HOLDS_TITLE lord-of-southshield` exists; AGENT_IN not wired.

**D-07**
`maron-volmark` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"Rise, Maron Volmark, Lord of Greenshield." `affc-the-reaver-01:181`
Rationale: Volmark receives Greenshield lordship at the post-battle feast. `HOLDS_TITLE lord-of-greenshield` exists; AGENT_IN not wired.

**D-08**
`torwold-browntooth` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"Euron had sent Torwold Browntooth and the Red Oarsman up the Mander with a dozen swift longships, so the lords of the Shield Islands would spill forth in pursuit." `affc-the-reaver-01:67`
Rationale: Torwold executes the decoy/diversion role that enables the main assault — direct AGENT_IN. Node is 0 edges; this is the load-bearing wiring for him.

**D-09**
`ragnor-pyke` **AGENT_IN** `taking-of-the-shields` | Tier-1 |
"He gave the captured ship to Ragnor Pyke, named a dozen men to crew her." `affc-the-reaver-01:53`
Rationale: Ragnor fights in the assault ("Victarion would have killed a third, but Ragnor cut him down first"), earns the prize of a captured longship. Direct combat participant in the taking.

**D-10**
`taking-of-the-shields` **LOCATED_AT** `shield-islands` | Tier-1 |
"Greyshield, Greenshield, and Southshield fell before the sun came up. Oakenshield lasted half a day longer." `affc-the-reaver-01:69`
Rationale: The taking is entirely set on the four Shield Islands. `shield-islands` node exists (5 in, 0 out); no LOCATED_AT edge from taking to it.

---

### Block 2 — Ship + horn: lighting the 0-edge artifact nodes (Gap #2, #3, #4)

**D-11**
`euron-greyjoy` **CAPTAIN_OF** `silence` | Tier-1 | qualifier: `{vessel: silence}` |
"The Silence was amongst the ships they passed." `affc-the-reaver-01:113`
Rationale: Silence is Euron's flagship (named repeatedly as "his ship," "red ship"). `CAPTAIN_OF` is the locked type for captain → vessel (object.artifact). `silence` has 0 edges; this is the single most glaring gap for a marquee ship.

**D-12**
`victarion-greyjoy` **CAPTAIN_OF** `iron-victory` | Tier-1 | qualifier: `{vessel: iron-victory}` |
"The drums were pounding out a battle beat as the Iron Victory swept forward" `affc-the-reaver-01:11`
Rationale: Iron Victory is Victarion's personal flagship throughout the arc. `iron-victory` has 0 edges; Victarion already has `CAPTAIN_OF iron-fleet` (fleet-level), but `iron-victory` the individual ship is unwired.

**D-13**
`euron-greyjoy` **OWNS** `dragonbinder` | Tier-1 |
"That horn you heard I found amongst the smoking ruins that were Valyria." `affc-the-drowned-man-01:185`
Rationale: Euron claims the horn as his own property, found in Valyria. `dragonbinder` has 1 edge (WIELDED_IN voyage beat) but no ownership/possession edge. OWNS → euron is the correct relationship before the GIFTED_TO victarion in the commission.

**D-14**
`dragonbinder` **GIFTED_TO** `victarion-greyjoy` | Tier-1 |
"Will you go to Slaver's Bay and bring my love to me?" `affc-the-reaver-01:261`
Rationale: The commission scene is where Euron offers the dragon horn to Victarion as the instrument for binding Daenerys's dragons — confirmed in ADWD iron suitor (already S132 wired). The GIFTED_TO edge is flagged as unwired in baseline gap #4. Verbatim anchor from the scene context: Euron gives Victarion Dragonbinder as part of the fetch commission (the ADWD chapter confirms the gift). The affc-the-reaver-01 commission scene at line 261 is the best AFFC anchor for the gift transaction. **[BORDERLINE]** — The horn is explicitly discussed as the binding instrument in the commission, but the word "gives" does not appear verbatim in affc-the-reaver-01; it is confirmed in adwd-the-iron-suitor-01. The gate should decide whether the AFFC commission context is sufficient for a Tier-1 cite or if this requires an ADWD reference.

---

### Block 3 — Kingsmoot site + officiant (Gap #6)

**D-15**
`kingsmoot-on-old-wyk` **LOCATED_AT** `naggas-hill` | Tier-1 |
"On the crown of the hill four-and-four monstrous stone ribs rose from the earth like the trunks of great pale trees." `affc-the-drowned-man-01:19`
Rationale: The kingsmoot is held explicitly at Nagga's Hill / the Grey King's Hall on Old Wyk. `naggas-hill` has 0 edges. This is the straightforward physical location.

**D-16**
`aeron-greyjoy` **OFFICIATES** `kingsmoot-on-old-wyk` | Tier-1 |
"When the Damphair raised his bony hands the kettledrums and the warhorns fell silent, the drowned men lowered their cudgels, and all the voices stilled." `affc-the-drowned-man-01:37`
Rationale: Aeron Damphair calls, convenes, and ritually runs the kingsmoot — he pours seawater on Victarion's brow, recites the liturgy, repeatedly asks "Who shall be king over us?" He is the officiating priest, not merely a participant. OFFICIATES is the locked type for "performs the religious/ceremonial rite at an event." His AGENT_IN kingsmoot already exists; OFFICIATES captures the distinct priestly-officiant role.

---

### Block 4 — Cross-arc seam: Iron Islands → the Reach (Gap #9, highest-value seam)

**D-17** ← **HIGHEST-VALUE CROSS-ARC SEAM**
`taking-of-the-shields` **CAUSES** `anarchy-in-the-reach` | Tier-2 |
"Highgarden," replied the Reader. "Soon enough all the power of the Reach will be marshaled against us, Barber, and then you may learn that some roses have steel thorns." `affc-the-reaver-01:135`
Rationale: `anarchy-in-the-reach` exists as an event node with **0 edges** — completely islanded. The taking of the Shields is the direct trigger for Reach instability: the ironborn seizure of the four islands opens the Mander to ironborn raiding ("The Mander is open to us now, as it was of old"), forces the Redwynes and Tyrells to redirect military resources to their own coast, and — as Rodrik the Reader states explicitly in the scene — produces the Reach's political-military crisis that spans AFFC. CAUSES is the right edge type (the taking directly produces the anarchy state; no free-choice intermediary breaks the link — the Reach lords have no option but to respond). This is the cleanest Iron Islands → Reach cross-arc seam in the text.

**D-18**
`taking-of-the-shields` **ENABLES** `mander` **[BORDERLINE — edge targets a location, not an event]**

*Withdrawn from proposal.* The Mander becoming open to ironborn raiding is stated as a board effect, not a discrete event node. There is no `ironborn-raid-up-the-mander` event node to wire to. The correct modeling is prose in `anarchy-in-the-reach` node body + the D-17 CAUSES edge. Do not mint a new event.

**D-19**
`rodrik-harlaw` **PARTICIPATES_IN** `taking-of-the-shields` | Tier-1 |
"In the yard Victarion came on Gorold Goodbrother and old Drumm, speaking quietly with Rodrik Harlaw." `affc-the-reaver-01:129`
Rationale: The Reader is present at Oakenshield post-battle and is the one who frames the strategic consequence ("We have won some stones and trees and trinkets, and the enmity of House Tyrell"). He is at the battle site, participating in the campaign's immediate aftermath. PARTICIPATES_IN (non-combat involvement) is correct. This also begins to wire rodrik-harlaw into the arc events beyond just OPPOSES/ADVISES.

---

### Block 5 — Rodrik Harlaw: Reader backing Asha at the moot (Gap #5 partial)

**D-20**
`rodrik-harlaw` **PARTICIPATES_IN** `kingsmoot-on-old-wyk` | Tier-1 |
"VICTORY!" shouted Rodrik the Reader, his hands cupped about his mouth. "Victory, and Asha!" `affc-the-drowned-man-01:135`
Rationale: The Reader vocally backs Asha at the kingsmoot — he is not just present, he is an active voice. PARTICIPATES_IN captures his non-combat but decisive role. Distinct from the AGENT_IN edges for the three main contenders (Euron/Asha/Victarion/Aeron).

---

### Block 6 — Burning of the Lannister fleet: Euron's AGENT_IN (cross-arc, Greyjoy rebellion)

**D-21**
`euron-greyjoy` **AGENT_IN** `burning-of-the-lannister-fleet` | Tier-1 |
"It was me sailed into Lannisport to singe the lion's tail." `affc-the-drowned-man-01:103` [Victarion speaking]
Rationale: Both Victarion and Asha confirm Euron "hatched the scheme" for the burning of the Lannister fleet at Lannisport during the Greyjoy rebellion. The event node exists (`burning-of-the-lannister-fleet`) with 0 incoming edges. Euron was the strategic architect. AGENT_IN rather than COMMANDS_IN because Euron is not confirmed to have been at Lannisport in command — he devised the plan. **[BORDERLINE]** — Victarion says "I flung the first torch" while Asha says "The Crow's Eye hatched the scheme." This is a complex shared-agency event. The synthesis should decide whether AGENT_IN (planner) or a separate COMMANDS_IN (strategic architect) is cleaner, or whether both get AGENT_IN with different roles captured in edge prose.

**D-22**
`victarion-greyjoy` **AGENT_IN** `burning-of-the-lannister-fleet` | Tier-1 |
"I burnt the lion's fleet," Victarion insisted. "With mine own hands I flung the first torch onto his flagship." `affc-the-iron-captain-01:265`
Rationale: Victarion explicitly and repeatedly claims personal execution of the Lannisport burning. Clean Tier-1 verbatim.

---

### Block 7 — Causal: Euron's gold/prizes MOTIVATES the kingsmoot captains

**D-23**
`euron-greyjoy` **MANIPULATES** `kingsmoot-on-old-wyk` | Tier-2 | qualifier: `via_bribe` |
"Euron had seduced them with his glib tongue and smiling eye and bound them to his cause with the plunder of half a hundred distant lands; gold and silver, ornate armor, curved swords with gilded pommels…" `affc-the-reaver-01:57`
Rationale: Euron's plunder-gifts are the material mechanism by which he secures kingsmoot votes — Victarion explicitly recognizes it ("Now he has given them conquest, and they are his for good and all"). The `via_bribe` qualifier is exact: he literally distributes treasure chests to the captains and kings at the moot. `kingsmoot-on-old-wyk` is an event node, and MANIPULATES targets an event here — **[BORDERLINE]**: the locked type note says MANIPULATES is for "genuine using-as-a-tool," and the usual target pattern is a character (MANIPULATES → character). Manipulating an event/outcome rather than a person may not fit the type contract. Flag for gate review: the synthesis may prefer `euron MOTIVATES kingsmoot-captains` → but no `kingsmoot-captains` node exists. May drop.

---

### Block 8 — Euron ↔ AEGON board (cross-arc, light)

**D-24** **[BORDERLINE — edge type uncertain]**
`taking-of-the-shields` **PARALLELS** `aegon-targaryen-lands-in-westeros` | Tier-3 |
"Why, it has been done before … Aegon Targaryen conquered Westeros with dragons." `affc-the-drowned-man-01:183`
Rationale: At the kingsmoot, Euron explicitly invokes Aegon's conquest as the template for his dragon-backed plan — the structural parallel between "ironborn with a dragon horn + fleet seizing the Reach as a base" and "Aegon with dragons landing at the Reach" is textually asserted. However, this is a PARALLELS (structural echo) between two events, and `aegon-targaryen-lands-in-westeros` is not a confirmed existing node slug. **Dropping this proposal** pending node-slug verification — do not propose an edge to a target the reviewer cannot confirm. Include in Dropped section.

---

## Dropped / considered-but-rejected

**`battle-of-the-shield-islands` wiring** — This is a `same_as` redirect stub to `taking-of-the-shields`. All wiring goes to the canonical slug. Rejected.

**Redwyne fleet retaking of the Shields** — TWOW-only. Paxter Redwyne is mentioned only as a strategic threat ("Galleys guard the Redwyne Straits") in the AFFC text. The actual Redwyne counter-offensive is post-AFFC / unpublished. Rejected.

**`taking-of-the-shields` ENABLES `mander` (location)** — Ironborn access to the Mander is a board effect, but there is no event node to wire to (no `ironborn-raid-up-the-mander`). The effect is captured via D-17 (CAUSES anarchy-in-the-reach) + node prose. Not proposing a location-target ENABLES.

**`taking-of-the-shields` MOTIVATES `paxter-redwyne`** — Paxter is not mentioned in the AFFC Iron Islands chapters; his response to the taking is show-adjacent and implied, not textually supported with a verbatim quote from the assigned chapters. Rejected.

**`taking-of-the-shields` CAUSES `mace-tyrell` actions** — Mace Tyrell is mentioned by name in the Reader's warning ("all the power of the Reach"), but MOTIVATES requires a character-target and the specific motivating connection to Mace needs a quote. Rodrik's warning is indirect inference. CAUSES anarchy-in-the-reach (D-17) captures the board effect at the event level without over-specifying the character chain. Rejected in favor of D-17.

**Euron ↔ Bloodraven** — GATED. Theory assertion. Rejected.

**Dragonbinder = Horn of Joramun** — GATED. Theory assertion. Rejected.

**`aeron-greyjoy` VOWS_TO `drowned-god`** — Aeron's general religious vocation is already captured via CLERGY_OF. The specific kingsmoot vow is more a prayer than a formal VOWS_TO contract. Not proposable with a clean verbatim single-line anchor.

**`aegon-targaryen-lands-in-westeros` PARALLELS** — Could not confirm node slug exists. Dropped (D-24 above).

**`euron-greyjoy` MANIPULATES `kingsmoot-on-old-wyk`** (D-23) — Borderline target type; included as flagged but likely will be dropped at synthesis if MANIPULATES requires character target.

**`torwold-browntooth` AGENT_IN `taking-of-the-shields` (decoy role)** — Already proposed as D-08; valid.

**`talbert-serry` VICTIM_IN `taking-of-the-shields`** — `talbert-serry` already has `DIED_AT shield-islands` (wiki) and `RESPECTS ← victarion-greyjoy`. A VICTIM_IN edge to the taking is redundant with the `DIED_AT shield-islands` wiki edge at the same event-location level. **[BORDERLINE]**: `VICTIM_IN` is more specific than `DIED_AT` — the synthesis may still want it. Dropping in favor of not duplicating what DIED_AT already encodes; flagged here for gate review.

**`rodrik-harlaw` UNCLE_OF `asha-greyjoy`** — baseline.md gap #5 mentions this explicitly. NOT a cross-arc seam (it's a kinship edge). Lens D scope is causal/consequence existing-node→existing-node. Flagged for Lens A or B.

**`euron-greyjoy` AGENT_IN `taking-of-the-shields`** — Euron does NOT personally participate in the assault; he is "Back on Oakenshield, lazing in a castle" per Victarion's bitter observation. He COMMANDS_IN (strategic order), not AGENT_IN. Proposing COMMANDS_IN instead:

**D-25**
`euron-greyjoy` **COMMANDS_IN** `taking-of-the-shields` | Tier-1 |
"Euron had sent Torwold Browntooth and the Red Oarsman up the Mander with a dozen swift longships, so the lords of the Shield Islands would spill forth in pursuit." `affc-the-reaver-01:67`
Rationale: Euron devised and ordered the entire tactical plan for the taking (decoy fleet up the Mander, main assault timed to the sunset blind spot, no warning ravens from the beacon towers). He is the strategic commander. COMMANDS_IN not AGENT_IN because he is not personally present at the assault.

---

## Summary table — proposed NEW edges

| ID | Source | Edge type | Target | Tier | Qualifier | BORDERLINE? |
|----|--------|-----------|--------|------|-----------|-------------|
| D-01 | victarion-greyjoy | COMMANDS_IN | taking-of-the-shields | 1 | — | |
| D-02 | victarion-greyjoy | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-03 | victarion-slays-multiple-defenders | SUB_BEAT_OF | taking-of-the-shields | 1 | — | |
| D-04 | harras-harlaw | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-05 | nute-the-barber | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-06 | andrik-the-unsmiling | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-07 | maron-volmark | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-08 | torwold-browntooth | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-09 | ragnor-pyke | AGENT_IN | taking-of-the-shields | 1 | — | |
| D-10 | taking-of-the-shields | LOCATED_AT | shield-islands | 1 | — | |
| D-11 | euron-greyjoy | CAPTAIN_OF | silence | 1 | vessel:silence | |
| D-12 | victarion-greyjoy | CAPTAIN_OF | iron-victory | 1 | vessel:iron-victory | |
| D-13 | euron-greyjoy | OWNS | dragonbinder | 1 | — | |
| D-14 | dragonbinder | GIFTED_TO | victarion-greyjoy | 1 | — | **BORDERLINE** |
| D-15 | kingsmoot-on-old-wyk | LOCATED_AT | naggas-hill | 1 | — | |
| D-16 | aeron-greyjoy | OFFICIATES | kingsmoot-on-old-wyk | 1 | — | |
| D-17 | taking-of-the-shields | CAUSES | anarchy-in-the-reach | 2 | — | |
| D-19 | rodrik-harlaw | PARTICIPATES_IN | taking-of-the-shields | 1 | — | |
| D-20 | rodrik-harlaw | PARTICIPATES_IN | kingsmoot-on-old-wyk | 1 | — | |
| D-21 | euron-greyjoy | AGENT_IN | burning-of-the-lannister-fleet | 1 | — | **BORDERLINE** |
| D-22 | victarion-greyjoy | AGENT_IN | burning-of-the-lannister-fleet | 1 | — | |
| D-23 | euron-greyjoy | MANIPULATES | kingsmoot-on-old-wyk | 2 | via_bribe | **BORDERLINE** |
| D-25 | euron-greyjoy | COMMANDS_IN | taking-of-the-shields | 1 | — | |

**Total proposed: 23 edges** (3 BORDERLINE flagged for gate scrutiny).

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | affc | affc-the-reaver-01:145 | "a riotous feast" at Lord Hewett's castle: roast ox (rare and bloody), stuffed ducks, buckets of fresh crabs, wine; captains eating off solid silver platters |
| food | affc | affc-the-reaver-01:73 | pre-battle: Victarion goes below and wants wine; "After a battle he always wanted wine" |
| food | affc | affc-the-reaver-01:101 | post-sex: "Fetch me another skin of wine … a skin of sour red" — pours the rest in the sea for the dead |
| food | affc | affc-the-iron-captain-01:73 | Victarion's pre-kingsmoot feast: "roast kid, salted cod, and lobster" — Aeron "ate fish and drank water, whilst the captains quaffed enough ale to float the Iron Fleet" |
| food | affc | affc-the-iron-captain-01:93 | finger dance; "Will Humble lost a wager and had to eat his boot" — the comedy of the feast; Qarl and Eldred Codd dance, finger lands in wine cup |
| food | affc | affc-the-drowned-man-01:27 | kingsmoot dawn: "gutting fish for the captains and the kings to break their fasts" + "throwing aside their sealskin blankets as they called for their first horn of ale" |
| food | affc | affc-the-drowned-man-01:129 | Asha's kingsmoot gifts: chest 1 = grey/black/white sea-worn pebbles ("wealth of the Stony Shore"), chest 2 = pinecones ("riches of Deepwood"), chest 3 = yellow turnips ("gold of Winterfell"); she stabs one with a dirk — deliberate anti-feast as political rhetoric |
| description | affc | affc-the-iron-captain-01:37 | Silence described at anchor: "a single-masted galley, lean and low, with a dark red hull … sails black as a starless sky … prow … a black iron maiden with one arm outstretched, waist slender, breasts high and proud, legs long and shapely, windblown mane of black iron hair, eyes of mother-of-pearl, but she had no mouth" |
| description | affc | affc-the-reaver-01:113 | Silence's figurehead at Oakenshield: "the iron figurehead at her prow, the mouthless maiden with the windblown hair and outstretched arm. Her mother-of-pearl eyes seemed to follow him. She had a mouth like any other woman, till the Crow's Eye sewed it shut." |
| description | affc | affc-the-drowned-man-01:151 | Dragonbinder sounded: "shiny black and twisted, taller than a man … bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled" — and after: "A thin wisp of smoke was rising from the horn, and the priest saw blood and blisters upon the lips of the man who'd sounded it. The bird on his chest was bleeding too." |
| description | affc | affc-the-drowned-man-01:145 | Dragonbinder's sound: "a shivering hot scream that made a man's bones seem to thrum within him" + "It was a terrible sound, a wail of pain and fury that seemed to burn the ears." |
| description | affc | affc-the-reaver-01:227 | Euron physical description: "He wore the sable cloak he took from Blacktyde, his red leather eye patch, and nothing else … his bruised blue lips curled in a half smile" |
| description | affc | affc-the-iron-captain-01:137 | Euron description at the feast tent: "His hair was still black as a midnight sea, with never a whitecap to be seen, and his face was still smooth and pale beneath his neat dark beard. A black leather patch covered Euron's left eye, but his right was blue as a summer sky … His lips looked very dark in the lamplight, bruised and blue." |
| quote | affc | affc-the-reaver-01:63 | Load-bearing Victarion quote: "The Mander is open to us now, as it was of old." — establishes the strategic consequence of the taking; attaches to taking-of-the-shields or anarchy-in-the-reach node |
| quote | affc | affc-the-reaver-01:131 | Rodrik Harlaw's warning: "We have won some stones and trees and trinkets, and the enmity of House Tyrell." — key strategic-assessment quote; attaches to taking-of-the-shields or rodrik-harlaw |
| quote | affc | affc-the-reaver-01:135 | Rodrik Harlaw: "Soon enough all the power of the Reach will be marshaled against us, Barber, and then you may learn that some roses have steel thorns." — key cross-arc seam quote |
| quote | affc | affc-the-drowned-man-01:165 | Euron kingsmoot speech: "I am Balon's brother, Quellon's eldest living son … I have sailed farther than any of them. Only one living kraken has never known defeat." |
| quote | affc | affc-the-drowned-man-01:185 | Euron on Dragonbinder: "That horn you heard I found amongst the smoking ruins that were Valyria, where no man has dared to walk but me … It is a dragon horn, bound with bands of red gold and Valyrian steel graven with enchantments." |
| quote | affc | affc-the-reaver-01:269 | Euron on marriage: "When the kraken weds the dragon, brother, let all the world beware." — high-value quote for euron-commissions node or euron node ## Quotes |
| quote | affc | affc-the-iron-captain-01:83 | Baelor Blacktyde: "Balon was mad, Aeron is madder, and Euron is maddest of them all." — attach to euron-greyjoy or baelor-blacktyde node ## Quotes |
| description | affc | affc-the-reaver-01:173 | Falia Flowers (the Hewett bastard): "A pretty, buxom girl of seventeen or eighteen years … barefoot and disheveled, her arms around his neck" — TWOW-relevant character but the AFFC description is publishable evidence; harvest for node prose only, no edge proposal |
| description | affc | affc-the-drowned-man-01:19 | Nagga's Hill / Grey King's Hall: "four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees … nine wide steps had been hewn from the stony hilltop. Behind rose the howling hills of Old Wyk, with mountains in the distance black and cruel." |
| hospitality | affc | affc-the-reaver-01:167-175 | Lord Hewett's humiliation: Euron makes Lady Hewett and her seven daughters/good-daughters serve the feast as their hostesses then forces them to undress and continue serving naked; Lord Hewett bound to his chair with a radish shoved in his mouth — ironborn feast-as-dominance scene |
