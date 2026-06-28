# Lens D — Existing-node↔existing-node causal wiring — A2.5 WO5K-battles proposal (S164, PASS 2)

## Proposed NEW nodes

None. All nodes for this spine exist. The synthesis pass should confirm that `taking-of-ashemark` exists
as a node slug (it appears in the baseline islanded-hub table, so treated as present).

---

## Proposed NEW edges

### THE WESTWARD-RAID SPINE (4 hops; one is the DEDUP seam)

**ANTECEDENT CHOICE: `robb-proclaimed-king-in-the-north` ENABLES `battle-of-oxcross`**

Rationale for picking `robb-proclaimed-king-in-the-north` over `battle-of-the-camps` as the antecedent:
The text makes clear that the westward offensive was only possible once Robb had been crowned and had
secured the Riverrun relief (both completed by `battle-of-the-camps` and the crowning). The ACOS catelyn-06
chapter enumerates the victories in reverse-chronological order ("At Stone Mill, at Oxcross, in the Battle
of the Camps, at the Whispering Wood") treating the crowning/relief-rise as the prior condition. The
Blackfish's ASOS explanation of strategic purpose ("why we remained in the west so long after Oxcross")
presupposes Robb was already operating as king with the freedom to choose where he marched. Being proclaimed
king is the status-change that gave Robb political and military license to carry the war offensively into
Lannister heartland; `robb-proclaimed-king-in-the-north` is the more precise node (the crowning itself, not
the battle that preceded it). `battle-of-the-camps` is the ENABLES-antecedent of `robb-proclaimed-king-in-the-north`
and is already in the PASS-1 chain; chaining from the crowning keeps the spine clean and avoids a double-hop.

---

**Edge 1 (NEW — the key spine-opener)**

`robb-proclaimed-king-in-the-north` **ENABLES** `battle-of-oxcross`
| Tier-2 | no qualifier |
Quote: "The only mystery is how your brother reached him. Our forces still hold the stronghold at the Golden Tooth, and they swear he did not pass." — `acok-sansa-03:157`
Rationale: The quote establishes that Robb's westward march into Lannister heartland was an offensive
strategic *choice* that puzzled even Tyrion — possible only because Robb was now a sovereign king with a
freed Riverrun as his base. Being crowned opened the political + military precondition for the offensive;
Robb then chose to carry the war past the Golden Tooth. ENABLES (not CAUSES): the crowning made it
*possible*; Robb's free decision produced the march. Tier-2 because the text proves the strategic sequence
inferentially (Tyrion's surprise, Catelyn's enumeration of victories) rather than a single explicit sentence
stating "being crowned let him march west."

---

**Edge 2 (NEW)**

`battle-of-oxcross` **ENABLES** `taking-of-ashemark`
| Tier-2 | no qualifier |
Quote: "The northmen crept into my uncle's camp and cut his horse lines, and Lord Stark sent his wolf among them. Even war-trained destriers went mad. Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster." — `acok-sansa-03:153`
Rationale: Tyrion's account makes explicit that Stafford's raw host — "apprentice boys, miners, fieldhands,
fisherfolk, the sweepings of Lannisport" — was the only organized Lannister force between Robb and the
Westerlands interior. With it destroyed at Oxcross, the Westerlands lay open to the raid: Robb's host then
moved on Ashemark and the gold mines. ENABLES (not CAUSES): the destruction of Stafford's host is the
military precondition that made the raid possible; Robb's host then freely chose to march deeper. Tier-2
because the Oxcross→Ashemark sequence is asserted in baseline wiki prose and confirmed by the chapter order
(Ashemark is mentioned downstream of Oxcross across all three chapters) but no single sentence reads
"because of Oxcross we could take Ashemark."

---

**Edge 3 (NEW)**

`taking-of-ashemark` **ENABLES** `storming-of-the-crag`
| Tier-2 | no qualifier |
Quote: "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." — `asos-catelyn-02:185`
Rationale: This line establishes the raid's battle sequence in order (Oxcross → Ashemark → the Crag),
with Ashemark as an intermediate beat before the Crag. The raid rolled through Ashemark en route to the
Crag (confirmed by baseline wiki note: "takes castles … including Ashemark … move on to the Crag"). ENABLES
(not CAUSES): taking Ashemark was the precondition that positioned Robb's host to reach the Crag; the
storming was still a distinct assault Robb chose to execute. Tier-2: the text proves the sequence but not
an explicit cause-and-effect sentence.

---

**Edge 4 — DEDUP / seam-close (do NOT re-propose)**

`storming-of-the-crag` **ENABLES** `robb-weds-jeyne-westerling` — **ALREADY EXISTS.** The spine closes here.
Noted only to confirm the seam: the three new edges above wire the raid hubs to the already-built marriage spine.

---

### SECONDARY SPINE EDGE (strategic-purpose wire — distinct from the raid beats)

**Edge 5 (NEW — the stated purpose of the westward strategy)**

`battle-of-oxcross` **ENABLES** `battle-of-the-fords` [**BORDERLINE — see note**]

NOTE: The Blackfish's speech at `asos-catelyn-02:223-229` states the explicit purpose of remaining in the
west after Oxcross was to draw Tywin away from King's Landing so Stannis could strike — "I wanted Lord
Tywin to come west." This is a strategic ENABLES relationship (the prolonged Westerlands presence is the
precondition that draws Tywin west, which in turn creates the window for Stannis). However, `battle-of-the-fords`
is the Edmure fords battle and is a PASS-1 node; the chain into it and its downstream (Tywin marching east,
Stannis's defeat) is PASS-3 material. **DROPPING this edge to PASS-3; see Dropped section.** Noting it here
as a strong candidate for the next pass.

---

## Dropped / considered-but-rejected

**1. Strategic-purpose MOTIVATES edge ("draw Tywin west")**
The Blackfish explicitly states the strategic PURPOSE of the westward raid at `asos-catelyn-02:223-229`: "I
wanted Lord Tywin to come west… we planned to run Lord Tywin a merry chase up and down the coast." This
*could* be modeled as `robb-stark MOTIVATES [draw-tywin-west strategy]` or as a MOTIVATES edge to Robb's
decision-node. However: (a) MOTIVATES must target a CHARACTER, not an event; (b) there is no event node for
"the-westward-strategy" — that granularity is node-prose territory; (c) the downstream consequence (Tywin
drawn east, joins Tyrell, defeats Stannis) is explicitly PASS-3. **Decision: leave as node-prose on
`battle-of-oxcross` and note for PASS-3.** A PASS-3 pass should model the `battle-of-the-fords ENABLES
[Tywin-east-march]` → `[battle-of-the-blackwater]` chain once those nodes exist.

**2. `robb-stark MOTIVATES [westward offensive]`**
MOTIVATES → character only (per LENS-SHARED). No character target. Dropping.

**3. `battle-of-oxcross DEFEATS stafford-lannister`**
`stafford-lannister VICTIM_IN battle-of-oxcross` + `stafford-lannister DIED_AT oxcross` BOTH ALREADY EXIST
per baseline dedup. A `DEFEATS` edge would be redundant — the outcome is fully captured by the existing
VICTIM_IN + DIED_AT pair. Dropping.

**4. `robb-stark DEFEATS stafford-lannister`** — same logic; VICTIM_IN on the event node covers this.
Dropping.

**5. `battle-of-the-camps ENABLES battle-of-oxcross` (alternative antecedent)**
Considered as the antecedent for hop 1 instead of `robb-proclaimed-king-in-the-north`. Rejected because
`robb-proclaimed-king-in-the-north` is the cleaner node: the text frames the Oxcross offensive as a king's
strategic choice, and the crowning is the formal status-change that licensed the westward march. Using
`battle-of-the-camps` would double-hop through an already-built chain edge
(`battle-of-the-camps ENABLES robb-proclaimed-king-in-the-north`) and would conflate the crowning with
the pre-crowning battle. `robb-proclaimed-king-in-the-north` is the better ENABLES source.

**6. Downstream Stannis chain (`battle-of-the-fords ENABLES [Tywin march east]` etc.)**
The Blackfish's speech makes this extremely clear as a causal chain, but every node in it (the fords battle,
Tywin's east march, Renly's camp at Bitterbridge, the Battle of the Blackwater) is PASS-3 material. Hard
scope rule: PASS 2 ONLY. Noting for PASS-3.

**7. `lymond-vikary VICTIM_IN battle-of-oxcross`**
This is Lens A (roster) territory, not Lens D (causal wiring). The baseline explicitly assigns Lymond Vikary
to the Oxcross roster gap. Not my lens. Deferring to Lens A.

**8. Crag roster edges (Smalljon AGENT_IN, Black Walder AGENT_IN, rolph-spicer COMMANDS_IN, LOCATED_AT, jeyne HEALS robb)**
All roster and role edges on the Crag node belong to Lens A/B. Lens D's mandate is causal
existing-node↔existing-node wiring only. Dropping all roster proposals — they are on-target but not my lens.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|--------------|------|
| food/drink | ACOK | acok-catelyn-06:181 | Rymund sings the Oxcross victory song after supper; "half of the hall was howling along with him, even Desmond Grell, who was well in his cups" — celebration feast detail after Stone Mill victory news |
| food/drink | ACOK | acok-catelyn-06:211 | Catelyn allows "breaking open some casks in honor of Stone Mill" — casks of drink opened; garrison morale context |
| food/drink | ACOK | acok-catelyn-06:129 | "a serving girl brought a platter of cheese and bread and olives, with a flagon of cold water" — Sansa's food in the Tower of the Hand (ACOS/Sansa file; flagging as cross-reference: actually acok-sansa-03:129) |
| quote (load-bearing) | ACOK | acok-sansa-03:153 | Tyrion's full Oxcross account verbatim: "The northmen crept into my uncle's camp and cut his horse lines, and Lord Stark sent his wolf among them. Even war-trained destriers went mad. Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster." — anchor quote for battle-of-oxcross node |
| quote (load-bearing) | ACOK | acok-sansa-03:153 | "Ser Stafford was slain as he chased after a horse. Lord Rickard Karstark drove a lance through his chest." — confirms Karstark's kill; battle-of-oxcross evidence quote |
| quote (load-bearing) | ACOK | acok-sansa-03:153 | "Ser Rubert Brax is also dead, along with Ser Lymond Vikary, Lord Crakehall, and Lord Jast." — full casualty list, Oxcross |
| quote (load-bearing) | ACOK | acok-sansa-03:157 | "Sorcery is the sauce fools spoon over failure to hide the flavor of their own incompetence." — Tyrion on Lancel's warg propaganda; vivid characterization quote for tyrion-lannister node |
| quote (load-bearing) | ASOS | asos-catelyn-02:143 | "I took her castle and she took my heart… The Crag was weakly garrisoned, so we took it by storm one night. Black Walder and the Smalljon led scaling parties over the walls, while I broke the main gate with a ram. I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered. Jeyne had me taken to her own bed, and she nursed me until the fever passed." — master anchor quote for storming-of-the-crag + jeyne-westerling HEALS robb-stark |
| quote (load-bearing) | ASOS | asos-catelyn-02:185 | "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." — compact raid-sequence confirmation; anchor for Grey Wind fight edges |
| quote (load-bearing) | ACOK | acok-catelyn-06:181 | Rymund song fragment: "And the stars in the night were the eyes of his wolves, and the wind itself was their song." — for battle-of-oxcross Quotes section |
| description | ASOS | asos-catelyn-02:223-229 | Blackfish explains strategic PURPOSE of the westward raid post-Oxcross — "I wanted Lord Tywin to come west… we planned to run Lord Tywin a merry chase up and down the coast, then slip behind him to take up a strong defensive position athwart the gold road" — load-bearing strategic prose for battle-of-oxcross node body |
| description | ACOK | acok-sansa-03:153 | "His host was raw—apprentice boys, miners, fieldhands, fisherfolk, the sweepings of Lannisport." — vivid description of Stafford's green host; stafford-lannister node / battle-of-oxcross body |
| description | ASOS | asos-catelyn-02:29 | "War had melted all the softness from his face and left him hard and lean." — Robb's physical description returning from the western campaign; robb-stark node Quotes |
| hospitality | ASOS | asos-catelyn-02:143 | "Jeyne had me taken to her own bed" — hospitality/nursing context at the Crag; Westerling household receiving Robb; pairs with jeyne HEALS robb |
| foreshadowing | ASOS | asos-catelyn-02:185-193 | Grey Wind bares teeth at Rolph Spicer + Catelyn urges Robb to send him away; Robb refuses — Chekhov's gun for the Spicer betrayal; PASS-3 thread |
