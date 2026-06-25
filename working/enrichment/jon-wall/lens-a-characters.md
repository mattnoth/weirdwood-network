# Lens A — Secondary-character sub-arcs (Jon / the Wall, S145)

**Scope:** Bowen Marsh, Melisandre, Stannis Baratheon, Tormund, Val, Mance Rayder, Selyse Florent, Wun Wun, Othell Yarwyck, the wildling hostages/spearwives, Alys Karstark, the Weeper.

**Source chapters read:** `adwd-melisandre-01`, `adwd-jon-01` through `adwd-jon-13`.

---

## NODE proposals

### N-1: `mance-glamour-of-rattleshirt` (event)

| Field | Value |
|---|---|
| Proposed slug | `mance-glamour-of-rattleshirt` |
| Type | `event.incident` |
| Natural SPACED aliases | "the glamouring of Mance Rayder", "Melisandre's glamour of the Lord of Bones" |
| 1-line gloss | Melisandre uses a ruby-anchored glamour to swap the apparent identities of Mance Rayder and Rattleshirt (Lord of Bones), so Rattleshirt burns in Mance's place while Mance operates as Rattleshirt at Castle Black. |
| Dedup status | Checked: MISSING. `find graph/nodes -name "mance-glamour*.node.md"` → no result. |
| Why mint | This is a pivotal deception event with multiple role participants. Currently the graph only has `COMMANDS melisandre → mance-rayder` and `COMMANDS melisandre → lord-of-bones`; the swap itself — which is what makes the Pink Letter's revelation plot-legible — is not an event node. The Shieldhall speech references "Rattleshirt and his spearwives" precisely because the glamour was still operative; without this node the downstream MOTIVATES/TRIGGERS chains are incomplete. |

---

### N-2: `val-sent-to-fetch-tormund` (event)

| Field | Value |
|---|---|
| Proposed slug | `val-sent-to-fetch-tormund` |
| Type | `event.incident` |
| Natural SPACED aliases | "Val's mission beyond the Wall", "Jon sends Val to find Tormund" |
| 1-line gloss | Jon Snow releases Val beyond the Wall to find Tormund Giantsbane and bring Jon's offer of food/shelter/peace, sending her on the half-blind garron on the night of the half-moon. |
| Dedup status | Checked: MISSING. No event node found. `val` has `PRISONER_OF stannis-baratheon` but no event node captures the mission dispatch. |
| Why mint | Val's release is the hinge that leads Tormund's arrival, which leads the wildling pass-through, which sharpens Bowen Marsh's grievance. It also produces the `jon-snow MARRIES_OFF alys-karstark` chain — Tormund returns to the wedding. A key command-decision event with two main participants, worth a node. |

---

### N-3: `alys-karstark-flight-to-the-wall` (event)

| Field | Value |
|---|---|
| Proposed slug | `alys-karstark-flight-to-the-wall` |
| Type | `event.incident` |
| Natural SPACED aliases | "Alys Karstark's flight to Castle Black", "Alys rides to Jon Snow" |
| 1-line gloss | Alys Karstark rides alone and nearly dies reaching Castle Black, fleeing Cregan Karstark's pursuit to avoid a forced marriage; she arrives as the grey girl of Melisandre's vision. |
| Dedup status | Checked: MISSING. `alys-karstark` has `OPPOSES alys-karstark → arnolf-karstark` and `SEEKS cregan-karstark → alys-karstark` but the flight event is not a node. |
| Why mint | Corrects Melisandre's misread of her own vision (she thought "grey girl on dying horse" = Arya); this event is a revelation beat about prophetic fallibility. Also the causal precursor to the Karstark-Thenn marriage. |

---

### N-4: `karstark-thenn-marriage` (event)

| Field | Value |
|---|---|
| Proposed slug | `karstark-thenn-marriage` |
| Type | `event.incident` |
| Natural SPACED aliases | "the marriage of Alys Karstark and the Magnar", "wedding of Alys and Sigorn" |
| 1-line gloss | Jon Snow officiates the R'hllor-rite marriage of Alys Karstark to Sigorn, Magnar of Thenn, before the Wall at Castle Black, witnessed by Queen Selyse and the assembled wildling and NW company. |
| Dedup status | Checked: MISSING. `SPOUSE_OF alys-karstark → sigorn` and `MARRIES_OFF jon-snow → alys-karstark` exist but no event node. |
| Why mint | This event is a deliberate political act by Jon (binding two peoples), witnessed by Selyse, and the direct trigger for Cregan Karstark's imprisonment. It also marks Selyse's presence at the Wall and Jon's use of Melisandre's rite despite his own skepticism. |

---

## EDGE proposals

### E-1: Melisandre glamours Mance Rayder

`melisandre --IMPERSONATES--> mance-rayder`

Wait — `IMPERSONATES` runs *impersonator → impersonated*. Mance is impersonating Rattleshirt; Melisandre is the agent enabling it. Better structure:

**E-1a:** `mance-rayder --DISGUISED_AS--> lord-of-bones`

- Tier: 1
- Evidence quote: "The widow's peak dissolved. The brown mustache, the knobby chin, the sallow yellowed flesh and small dark eyes, all melted … Jon Snow's grey eyes grew wider. 'Mance?' … 'She burned the Lord of Bones.'"
- Chapter:line: `adwd-melisandre-01.md:251` (dissolution of glamour) and `adwd-melisandre-01.md:257–259` (confirmation)
- Dedup: MISSING — `lord-of-bones` has `DIED_AT castle-black` but no DISGUISED_AS or IMPERSONATES edges. `mance-rayder` has no identity-disguise edges.
- Rationale: Canonical identity swap; Mance physically operates as Lord of Bones for most of ADWD until the Pink Letter. The `DISGUISED_AS` edge is the correct type (character disguised as another).

**E-1b:** `melisandre --PRACTICES--> glamour-magic`

- Tier: 1
- Evidence quote: "Glamor, seeming, illusion. R'hllor is Lord of Light, Jon Snow, and it is given to his servants to weave with it, as others weave with thread."
- Chapter:line: `adwd-melisandre-01.md:263`
- Dedup: MISSING — `melisandre` has `WORSHIPS rhllor` but no `PRACTICES` edge. `glamour-magic` would need to be minted as a `concept` node, or the edge can target `rhllor` as the magic-source. Flag for minting decision.
- Rationale: Low-priority but useful for magic taxonomy. Defer if minting the concept node is out of scope.

---

### E-2: Mance AGENT_IN the glamour / execution

`melisandre --AGENT_IN--> mance-glamour-of-rattleshirt` (requires N-1)
`lord-of-bones --VICTIM_IN--> mance-glamour-of-rattleshirt`
`mance-rayder --AGENT_IN--> mance-glamour-of-rattleshirt`
`jon-snow --WITNESS_IN--> mance-glamour-of-rattleshirt`

- Tier: 1
- Evidence quote (for Rattleshirt as victim): "She burned the Lord of Bones."
- Chapter:line: `adwd-melisandre-01.md:259`
- Dedup: MISSING — no role edges around this event (event node itself missing, see N-1).
- Rationale: Required companion edges if N-1 is minted.

---

### E-3: Weeper — responsible for eyeless-rangers incident

`weeper --AGENT_IN--> rangers-found-eyeless` *(requires a new event node, or wire to existing Black Jack Bulwer / ranger context)*

More precisely, propose without a new node — wire to the returning-ranger context:

`weeper --ATTACKS--> nights-watch`

- Tier: 1
- Evidence quote: "Cutting out the eyes, that's the Weeper's work. The best crow's a blind crow, he likes to say."
- Chapter:line: `adwd-melisandre-01.md:105`
- Dedup: `weeper` has only `SWORN_TO mance-rayder` and `CULTURE_OF free-folk`. MISSING all hostile edges.
- Rationale: Establishes the Weeper's threat identity within ADWD; the three impaled eyeless ranger heads (Black Jack Bulwer, Hairy Hal, Garth Greyfeather) are the concrete demonstration of his method. Tier 1 — Mance-as-Rattleshirt explicitly attributes the practice.

`weeper --OPPOSES--> nights-watch`

- Tier: 1
- Evidence quote: "Snow's been assuming the free folk would turn to Tormund to lead them … If it's the Weeper, though … that's not good. Not for him, and not for us."
- Chapter:line: `adwd-melisandre-01.md:105`
- Dedup: MISSING.
- Rationale: Distinguishes Weeper as a hostile faction-leader distinct from Tormund, which is plot-critical (the ranger deaths happen before Tormund arrives).

`weeper --FIGHTS_IN--> battle-beneath-the-wall`

- Tier: 2 (inferred, consistent with his forces being active in the area)
- Skip — no direct text confirms Weeper at the battle itself. Do not propose.

---

### E-4: Bowen Marsh — injury at Bridge of Skulls

`bowen-marsh --FIGHTS_IN--> battle-at-the-bridge-of-skulls` *(need to check if this event exists)*

The node `bridge-of-skulls` (location) EXISTS. The text says:

> "Bowen Marsh edged his mount up next to Jon's. … The Lord Steward had thinned notably since suffering a head wound at the Bridge of Skulls. Part of one ear was gone."
> — `adwd-jon-03.md:101`

And in `adwd-jon-13.md:161`: "Bowen Marsh rubbed at the scar he had won at the Bridge of Skulls."

`bowen-marsh --DIED_AT--> bridge-of-skulls` — WRONG, he survived.

Propose: `bowen-marsh --FIGHTS_IN--> great-ranging` (existing event, ASOS context) — no, the Bridge of Skulls battle is a separate pre-ADWD engagement.

**E-4a — mint a battle node first:**
Flag: consider minting `battle-at-the-bridge-of-skulls` (event.battle). Checking: `find graph/nodes -name "*bridge-of-skulls*battle*"` — not found. This battle is referenced in `adwd-jon-01.md:181` ("Ser Denys Mallister … sees fires in the mountains on the far side of the Gorge. Wildlings massing … going to try to force the Bridge of Skulls again") and the injuries to Bowen Marsh. Worth minting.

**E-4b:** `bowen-marsh --FIGHTS_IN--> battle-at-the-bridge-of-skulls` (pending mint)
- Tier: 1
- Evidence: "The Lord Steward had thinned notably since suffering a head wound at the Bridge of Skulls. Part of one ear was gone." `adwd-jon-03.md:101`
- Rationale: Bowen's wound shapes his psychology toward the stabbing; missing from all his current edges which are purely relational.

---

### E-5: Val — mission dispatch edges (to existing nodes)

`jon-snow --COMMANDS--> val` (to fetch Tormund)

- Tier: 1
- Evidence quote: "'I sent her to find Tormund Giantsbane and bring him my offer.'"
- Chapter:line: `adwd-jon-08.md:185`
- Dedup: No COMMANDS edge jon → val exists. `jon-snow` has `PROTECTS val`, `TRUSTS val`, `LOVES val`, `RESPECTS val`, `MARRIES_OFF val` (the Norrey/Flint gossip subthread). MISSING explicit command.
- Rationale: Jon exercises command authority over Val as a prisoner; this is the decision Bowen Marsh confronts him about in the same chapter. High-value for the command-chain reading.

`val --TRAVELS_TO--> beyond-the-wall` (on the mission)

- Tier: 1
- Evidence quote: "Val glanced at the sky. The moon was but half-full. 'Look for me on the first day of the full moon.' … Val wheeled the garron toward the north."
- Chapter:line: `adwd-jon-08.md:29–78`
- Dedup: MISSING — `val` has no TRAVELS_TO edge.
- Rationale: Grounds her agency in the physical journey rather than purely relational edges.

---

### E-6: Selyse Florent — at Castle Black, political friction with Jon

`selyse-florent --OPPOSES--> jon-snow` (on Hardhome/wildling policy)

- Tier: 1
- Evidence quote: "'Let them die,' said Queen Selyse. … 'Do what you must.' … 'you will answer for it when the king returns.'"
- Chapter:line: `adwd-jon-13.md:12–31`
- Dedup: `selyse-florent` has `DISTRUSTS jon-snow` — does not have `OPPOSES`. Check: `OPPOSES selyse → jon-snow` absent. MISSING — add.
- Rationale: Selyse explicitly opposes the Hardhome ranging and threatens Jon with accountability; this is a distinct political OPPOSES, not just distrust.

`selyse-florent --GUEST_OF--> jon-snow` (at Castle Black for wedding and stay)

- Tier: 1
- Evidence quote: "Queen Selyse descended upon Castle Black with her daughter … Jon met the queen's party by the stables."
- Chapter:line: `adwd-jon-09.md:1–12`
- Dedup: `selyse-florent` has multiple GUEST_OF edges (to Cotter Pyke, salladhor-saan, etc.) but NOT `GUEST_OF → jon-snow`. Checking: `GUEST_OF jon-snow → selyse-florent` EXISTS (Jon hosts her). `selyse-florent --GUEST_OF--> jon-snow` MISSING.
- Note: The direction should be `selyse-florent GUEST_OF jon-snow` (she is the guest, he is the host). Dedup check confirms this direction is absent. Propose.

---

### E-7: Othell Yarwyck — CONSPIRES_WITH Bowen Marsh

`othell-yarwyck --CONSPIRES_WITH--> bowen-marsh`

- Tier: 1
- Evidence quote: "Bowen Marsh stood there before him, tears running down his cheeks. 'For the Watch.' He punched Jon in the belly." (Yarwyck is listed earlier as slipping out with Marsh after the Shieldhall speech)
- Chapter:line: `adwd-jon-13.md:323` (the stabbing) / `adwd-jon-13.md:283` (Marsh and Yarwyck exit together)
- Dedup: `CONSPIRES_WITH alliser-thorne → othell-yarwyck` EXISTS and `CONSPIRES_WITH alliser-thorne → bowen-marsh` EXISTS, but `othell-yarwyck --CONSPIRES_WITH--> bowen-marsh` is MISSING.
- Rationale: They exit together from the Shieldhall, are repeatedly paired in opposition, and Yarwyck's presence at the stabbing-site is implicit from the text. Tier 1 — they are shown acting in concert throughout.

`othell-yarwyck --SUSPECTED_OF--> jon-is-stabbed-repeatedly`

- Tier: 2 (not shown wielding a knife; text has Wick Whittlestick and Bowen Marsh as named stabbers, Yarwyck is a co-conspirator)
- Evidence quote: "Yarwyck and Marsh were slipping out, he saw, and all their men behind them."
- Chapter:line: `adwd-jon-13.md:299`
- Dedup: `othell-yarwyck` has `AGENT_IN jon-overhears-the-conspiracy` but NOT `SUSPECTED_OF jon-is-stabbed-repeatedly`. MISSING.
- Rationale: Yarwyck leaves the Shieldhall immediately before the stabbing with Marsh's faction; he is a co-conspirator but not a direct stabber. `SUSPECTED_OF` is the correct Tier-2 label per project convention.

---

### E-8: Tormund — arrival and role edges

`tormund --AGENT_IN--> jon-allows-free-folk-through-the-wall`

- Tier: 1
- Evidence quote: "Tormund Giantsbane had come at last." (Jon-10 final line); and "He is settled his people at Oakenshield and will be back this afternoon with eighty fighting men."
- Chapter:line: `adwd-jon-10.md:305` and `adwd-jon-13.md:107`
- Dedup: `tormund` has `AGENT_IN dryn-given-as-final-hostage` and `AGENT_IN hostage-boys-pass-through`, but NOT `AGENT_IN jon-allows-free-folk-through-the-wall`. MISSING.
- Rationale: Tormund is the wildling leader who negotiated and executed the free-folk passage Jon authorised.

`tormund --COMPANION_OF--> jon-snow` (Shieldhall / Hardhome planning)

- Tier: 1
- Evidence quote: "'Well spoken, crow. Now bring out the mead! … We'll make a wildling o' you yet, boy.'"
- Chapter:line: `adwd-jon-13.md:299`
- Dedup: `COMPANION_OF tormund → jon-snow` — checking… EXISTS. Already wired. Do NOT re-propose.

---

### E-9: Alys Karstark — key missing edges

`alys-karstark --REVEALS_TO--> jon-snow` (Arnolf's treachery against Stannis)

- Tier: 1
- Evidence quote: "Arnolf is rushing to Winterfell, 'tis true, but only so he might put his dagger in your king's back. He cast his lot with Roose Bolton long ago … Lord Stannis is marching to a slaughter."
- Chapter:line: `adwd-jon-09.md:329–332`
- Dedup: `alys-karstark` has `OPPOSES alys-karstark → arnolf-karstark` — no `REVEALS_TO` edges. MISSING.
- Rationale: Alys is the intelligence vector who warns Jon of Arnolf's betrayal. This is the chain that leads to the raven to Stannis warning him of the trap.

`jon-snow --PROTECTS--> alys-karstark` (sheltering her from Cregan)

- Tier: 1
- Evidence quote: "Protect me. … The Night's Watch has no quarrel with Karhold, nor with you."
- Chapter:line: `adwd-jon-09.md:333` (Alys's plea) and `adwd-jon-09.md:319` (Jon's response)
- Dedup: `PROTECTS jon-snow → alys-karstark` — checking… EXISTS. Already wired. Do NOT re-propose.

`cregan-karstark --IMPRISONED_AT--> castle-black`

- Tier: 1
- Evidence quote: "Fortunately they had a dozen ice cells. Room for all."
- Chapter:line: `adwd-jon-10.md:82–83`
- Dedup: `cregan-karstark` has only `SEEKS cregan-karstark → alys-karstark` and `CLAIMS cregan-karstark → alys-karstark`. `IMPRISONED_AT` is MISSING.
- Rationale: Cregan's imprisonment is the direct consequence of his pursuit and a concrete outcome of Jon's action; it also sets up the "take the black or rot" negotiation.

---

### E-10: Wun Wun — kill of Ser Patrek and trigger edges

`wun-weg-wun-dar-wun --KILLS--> patrek-of-kings-mountain`

- Dedup: EXISTS (`KILLS wun-weg-wun-dar-wun → patrek-of-kings-mountain`). DO NOT re-propose.

`patrek-of-kings-mountain --COURTS--> val`

- Tier: 1
- Evidence quote: "Queen Selyse pursed her lips. 'Lord Snow, as Lady Val is a stranger to our ways, … It is past time that this woman Val was settled … she shall wed my good and leal knight, Ser Patrek of King's Mountain.' … 'No man has ever had cause to question my courage. No woman ever will.'"
- Chapter:line: `adwd-jon-13.md:59–66`
- Dedup: `COURTS justin-massey → val` EXISTS. `COURTS patrek-of-kings-mountain → val` — MISSING.
- Rationale: Patrek's pursuit of Val (by Queen Selyse's command, with his own swagger) is what provoked the confrontation with Wun Wun that immediately precedes Jon's stabbing — a direct causal node in the chain.

`patrek-of-kings-mountain --AGENT_IN--> jon-is-stabbed-repeatedly`

- Tier: 2 — indirect
- Actually: Patrek's death triggers Wun Wun's rampage which provides the confusion screen for the stabbers. But the text doesn't name Patrek as a conspirator.
- Do NOT propose as AGENT_IN; the causal chain is more properly a PRECEDES / TRIGGERS. Not wired here — flag for lens-B (causal wiring).

`wun-weg-wun-dar-wun --CAUSES--> jon-is-stabbed-repeatedly`

- Tier: 2 — the rampage created the cover. Evidence: Wick slashes Jon's throat while Jon is shouting at Wun Wun.
- Evidence quote: "When Wick Whittlestick slashed at his throat, the word turned into a grunt."
- Chapter:line: `adwd-jon-13.md:319`
- Dedup: MISSING.
- Rationale: Causal: Wun Wun's rampage (triggered by Patrek's attempt to "steal" Val) provided the confusion that allowed the assassins to act. Tier 2 — the link is inferential but strongly supported. Propose as `CAUSES`.

---

### E-11: Stannis — offer of Winterfell to Jon (ASOS, but shapes all ADWD Jon)

`stannis-baratheon --APPOINTS--> jon-snow` (legitimization + Winterfell offer)

- Dedup: `APPOINTS stannis-baratheon → jon-snow` — checking edges… EXISTS (from Pass 1 tail-llm run). DO NOT re-propose.

`jon-snow --OPPOSES--> stannis-baratheon` (refusal of the offer)

- Dedup: EXISTS. DO NOT re-propose.

---

### E-12: Melisandre's prophecy misread — Alys not Arya

`melisandre --DECEIVED_BY--> melisandre` — self-referential, not useful.

Better:

`alys-karstark --PARALLELS--> arya-stark` (prophecy-misread: Melisandre saw Alys as Arya)

- Tier: 2 (interpretive)
- Evidence quote: "A grey girl on a dying horse. Melisandre's fires had not lied, it would seem … But she was too old … 'Alys Karstark.' … 'You were not right. Alys is not Arya.' 'The vision was a true one. It was my reading that was false.'"
- Chapter:line: `adwd-jon-09.md:257` and `adwd-jon-10.md:138–143`
- Dedup: MISSING — no PARALLELS edge in the graph.
- Rationale: A rare case where GRRM explicitly has a character admit the misread in-text. Evidence that R'hllor's visions are accurate but interpretation is fallible. Tier 2 — the parallel is real but literary/structural.

---

### E-13: Selyse Florent — Melisandre alliance texture

`selyse-florent --ATTENDS--> karstark-thenn-marriage` (N-4)

- Tier: 1
- Evidence quote: "Queen Selyse … 'Her Grace approves. I am close to her, so I know her mind. King Stannis will approve as well.'"
- Chapter:line: `adwd-jon-10.md:261` (Ser Axell speaks for Selyse's approval)
- Dedup: MISSING. Requires N-4 to be minted.

`selyse-florent --DISTRUSTS--> ghost` (Jon's direwolf)

- Tier: 1
- Evidence quote: "The queen glanced at Ghost suspiciously, then raised her head to Jon."
- Chapter:line: `adwd-jon-10.md:105`
- Dedup: `FEARS selyse-florent → ghost` EXISTS. Close enough — do NOT add DISTRUSTS for the same relationship; FEARS covers it.

---

### Summary table

| # | Proposal | Type | Tier | Status |
|---|---|---|---|---|
| N-1 | `mance-glamour-of-rattleshirt` | NODE (event.incident) | — | MISSING |
| N-2 | `val-sent-to-fetch-tormund` | NODE (event.incident) | — | MISSING |
| N-3 | `alys-karstark-flight-to-the-wall` | NODE (event.incident) | — | MISSING |
| N-4 | `karstark-thenn-marriage` | NODE (event.incident) | — | MISSING |
| E-1a | `mance-rayder --DISGUISED_AS--> lord-of-bones` | EDGE | 1 | MISSING |
| E-3a | `weeper --ATTACKS--> nights-watch` | EDGE | 1 | MISSING |
| E-3b | `weeper --OPPOSES--> nights-watch` | EDGE | 1 | MISSING |
| E-4b | `bowen-marsh --FIGHTS_IN--> battle-at-the-bridge-of-skulls` | EDGE | 1 | MISSING (event node also missing) |
| E-5a | `jon-snow --COMMANDS--> val` | EDGE | 1 | MISSING |
| E-5b | `val --TRAVELS_TO--> beyond-the-wall` | EDGE | 1 | MISSING |
| E-6a | `selyse-florent --OPPOSES--> jon-snow` | EDGE | 1 | MISSING |
| E-7a | `othell-yarwyck --CONSPIRES_WITH--> bowen-marsh` | EDGE | 1 | MISSING |
| E-7b | `othell-yarwyck --SUSPECTED_OF--> jon-is-stabbed-repeatedly` | EDGE | 2 | MISSING |
| E-8 | `tormund --AGENT_IN--> jon-allows-free-folk-through-the-wall` | EDGE | 1 | MISSING |
| E-9a | `alys-karstark --REVEALS_TO--> jon-snow` | EDGE | 1 | MISSING |
| E-9b | `cregan-karstark --IMPRISONED_AT--> castle-black` | EDGE | 1 | MISSING |
| E-10a | `patrek-of-kings-mountain --COURTS--> val` | EDGE | 1 | MISSING |
| E-10b | `wun-weg-wun-dar-wun --CAUSES--> jon-is-stabbed-repeatedly` | EDGE | 2 | MISSING |
| E-12 | `alys-karstark --PARALLELS--> arya-stark` | EDGE | 2 | MISSING |

---

## HARVEST

`adwd-melisandre-01.md:93` / food / Melisandre's breakfast order: "nettle tea, a boiled egg, and bread with butter. Fresh bread, if you please, not fried" — Hobb delivers warm brown bread; Rattleshirt/Mance eats it while Jon watches; contrast of spy breakfast and politicking.

`adwd-melisandre-01.md:150` / food / Hobb cooks fresh-baked loaves that Melisandre leaves for Mance-as-Rattleshirt; Devan is sent to fetch them and instructed to leave them. Hobb's baking as communal provision at Castle Black — small hospitality detail.

`adwd-jon-01.md:32–33` / food / Hobb's morning menu: "boiled eggs, black sausage, and apples stewed with prunes" — the Dolorous Edd prune speech is both comedy and texture of NW subsistence diet in winter.

`adwd-jon-03.md:167` / food / Post-execution supper: "boiled beef and beets" (Hobb out of horseradish). Classic grim NW ration — Dolorous Edd's "what good is boiled beef without horseradish?" is a memorable food-complaint quote.

`adwd-jon-08.md:93` / food / Jon's post-duel breakfast: "three duck's eggs fried in drippings, a strip of bacon, two sausages, a blood pudding, and half a loaf of bread still warm from the oven. He ate the bread and half an egg." The raven steals the bacon. Sparse eating from a commander under pressure.

`adwd-jon-09.md:197` / food / Selyse's arrival: "a hot meal awaits you in our common room" — offstage provision; reveals Jon's duty-of-hospitality habits. The queen is described as disdaining food and comfort.

`adwd-jon-10.md:195–197` / food / Wedding feast: "onion broth flavored with bits of goat and carrot … coarse brown bread, warm from the oven. Salt and butter on the tables. The last of the butter would be gone within a moon's turn." — dire stores note; also mulled wine with cinnamon and cloves.

`adwd-jon-10.md:247` / food / Feast continues: "The elk was being carved. It smelled better than Jon had any reason to expect." Hobb's complaint about never having done a wedding feast. The fish course (pike being boned) follows.

`adwd-jon-13.md:195` / food / Tormund arrives demanding "a horn of ale and something hot to eat."

`adwd-jon-08.md:213` / food / Wun Wun's diet: "This giant ate no meat at all, though he was a holy terror when served a basket of roots, crunching onions and turnips and even raw hard neeps between his big square teeth." — notable that the giant is vegetarian, contrary to legend.

`adwd-jon-01.md:317` / foreshadowing / Melisandre: "Ice, I see, and daggers in the dark. Blood frozen red and hard, and naked steel. It was very cold." — direct foreshadowing of the stabbing. Already in text before the Shieldhall speech.

`adwd-melisandre-01.md:29` / foreshadowing / Melisandre's vision: "Skulls. A thousand skulls, and the bastard boy again. Jon Snow." — recurring skull imagery = death imagery around Jon; parallels the fire-vision in the chapter.

`adwd-jon-03.md:94–97` / description / Mance-as-Rattleshirt in public (before the reveal): Sigorn kneels first, then Rattleshirt in clattering armor — "Under the bones lurked a ruined and wretched creature with cracked brown teeth and a yellow tinge to the whites of his eyes." The description is of Mance-as-Rattleshirt, not Mance himself.

`adwd-jon-09.md:59–83` / description / Giant encounter: Wun Wun kneels before the queen with "Kneel queen. Little queen." — Shireen's awe and Selyse's disgust. Physical description of giant as taller than a man even kneeling, eating from a basket of roots and vegetables.

`adwd-jon-13.md:307–313` / description / Wun Wun dismembers Ser Patrek: "swinging it like a morningstar when menaced by vegetables … The dead man's sword arm was yards away … smashed [head] against the grey stone of the tower, again and again … the man's head was red and pulpy as a summer melon." — visceral description; also "like a child pulling petals off a daisy" for the arm-tearing.

`adwd-jon-03.md:37` / description / Val at the execution: "Val stood beside him, tall and fair. They had crowned her with a simple circlet of dark bronze, yet she looked more regal in bronze than Stannis did in gold." — key Val description quote, notable for the bronze-vs-gold comparison making Val seem more queenly than a king.

`adwd-jon-08.md:11–44` / description / Val departure scene: the half-blind garron, Val's bearskin cloak, the half-moon. Her food pack listed precisely. Good logistical / departure description.

`adwd-jon-01.md:192` / hospitality / Gilly given "freedom of the castle" by Stannis — Jon uses this detail to explain how she heard gossip about Rattleshirt land grants. Hospitality with limits (freedom-of-castle ≠ formal guest right).

`adwd-jon-03.md:147` / hospitality / Jon considers Night's Watch hospitality obligations to Stannis: "He is still a rebel … but he is our guest besides. The laws of hospitality protect him." Jon explicitly invokes guest right as a constraint on action.

`adwd-jon-09.md:99` / hospitality / Selyse's arrival: Jon offers "a hot meal" and quarters in the King's Tower. The GUEST_OF chain here. Axell Florent's later demand re: Val violates the spirit of hospitality.

`adwd-jon-10.md:198` / hospitality / Old Flint and The Norrey attend the wedding, given "places of high honor just below the dais" — small lords accepting wildling-rite wedding in exchange for guest right treatment. Subtle binding-through-hospitality.

