# Lens C — descriptive / quote / object depth — A2.5 WO5K-battles proposal (S164, PASS 2)

## Proposed node Quotes

These are verbatim single-line quotes to be overlaid onto existing nodes as `## Quotes` entries.
Each is a contiguous substring of exactly one text line; chapter:line cites given.

---

### Target: `battle-of-oxcross`

**Q1 — Tyrion's definitive tactical account (the marquee Oxcross description)**
> "The northmen crept into my uncle's camp and cut his horse lines, and Lord Stark sent his wolf among them."
- Source: `acok-sansa-03:153`
- Why load-bearing: The single most authoritative book-cited account of HOW the battle was won — the horse-line cutting + Grey Wind among the destriers. Converts the node's wiki prose to a Tier-1 navigable cite.

**Q2 — The destrier panic and the trampling of knights**
> "Even war-trained destriers went mad. Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster."
- Source: `acok-sansa-03:153`
- Why load-bearing: The vivid physical mechanism of the rout — maddened destriers trampling armored knights in their pavilions. Core descriptive content for the node. (Note: this is a single long sentence spanning the same line as Q1; cite the same line.)

**Q3 — Stafford's death and the casualty roll**
> "Ser Stafford was slain as he chased after a horse. Lord Rickard Karstark drove a lance through his chest. Ser Rubert Brax is also dead, along with Ser Lymond Vikary, Lord Crakehall, and Lord Jast."
- Source: `acok-sansa-03:153`
- Why load-bearing: The only book-cited casualty list for Oxcross, naming Stafford's exact cause of death and the full dead roster. Overlaying this onto `battle-of-oxcross` upgrades the node from wiki-cite to Tier-1 provenance.

**Q4 — Rymund's Oxcross victory song refrain**
> "And the stars in the night were the eyes of his wolves, and the wind itself was their song."
- Source: `acok-catelyn-06:181`
- Why load-bearing: The canonical in-world artistic response to Oxcross — the line half the Great Hall was howling along to. It is the cultural signature of the battle and belongs on the `battle-of-oxcross` node's `## Quotes`. Also applies to `grey-wind`.

---

### Target: `storming-of-the-crag`

**Q5 — Robb's own account of the storming (the marquee Crag description)**
> "The Crag was weakly garrisoned, so we took it by storm one night. Black Walder and the Smalljon led scaling parties over the walls, while I broke the main gate with a ram."
- Source: `asos-catelyn-02:143`
- Why load-bearing: The ONLY first-person book-cited account of the mechanics of the assault. This is the single line that makes the Crag roster entries navigable. Overlays onto `storming-of-the-crag`.

**Q6 — The arrow wound and Jeyne nursing him**
> "I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered. Jeyne had me taken to her own bed, and she nursed me until the fever passed."
- Source: `asos-catelyn-02:143`
- Why load-bearing: Establishes the wound (the `HEALS` edge anchor), Rolph's surrender, and Jeyne's role in a single book-cited passage. Applies to both `storming-of-the-crag` and `robb-weds-jeyne-westerling`.

**Q7 — "I took her castle and she took my heart" / "we took it by storm one night"**
> "I took her castle and she took my heart."
- Source: `asos-catelyn-02:143` (Robb's exact words, earlier in the same speech)
- Why load-bearing: The canonical in-world formulation of the Crag-to-marriage sequence. This is the sentence GRRM chose to deliver the causation. Belongs on both `storming-of-the-crag` and `robb-weds-jeyne-westerling`.

---

### Target: `grey-wind`

**Q8 — Grey Wind's kill count across the three battles**
> "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross."
- Source: `asos-catelyn-02:185`
- Why load-bearing: The only book-cited tally of Grey Wind's kills across all three PASS-2 battles, in one line. Essential for `grey-wind` node and anchors the `FIGHTS_IN` edges at all three battle nodes.

---

### Target: `robb-stark`

**Q9 — The propaganda version (Lancel's account at court)**
> "Using some vile sorcery, your brother fell upon Ser Stafford Lannister with an army of wargs, not three days ride from Lannisport. Thousands of good men were butchered as they slept, without the chance to lift sword. After the slaughter, the northmen feasted on the flesh of the slain."
- Source: `acok-sansa-03:39`
- Why load-bearing: The Lannister court's PERCEIVED_AS framing of Robb as a sorcerer/warg-commander. Useful for the `robb-stark` node's `## Quotes` to document how he was perceived by enemies, and contrasts with Tyrion's debunking on the same chapter.

---

## Proposed NEW nodes

None. All relevant entity nodes exist. The Crag roster and battles are all present.

---

## Proposed NEW edges

### 1. HEALS gap — the clean priority edge
| source | edge_type | target | tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| `jeyne-westerling` | HEALS | `robb-stark` | Tier-1 | — | "Jeyne had me taken to her own bed, and she nursed me until the fever passed" `asos-catelyn-02:143` | Explicit in Robb's own words to Catelyn. Identified as a gap in baseline.md. |

### 2. Crag roster — AGENT_IN / COMMANDS_IN / FIGHTS_IN gaps
The storming-of-the-crag node has ZERO participant edges. All of these are in the Q5 / Q6 text anchors above.

| source | edge_type | target | tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| `robb-stark` | AGENT_IN | `storming-of-the-crag` | Tier-1 | — | "I broke the main gate with a ram" `asos-catelyn-02:143` | Robb personally broke the gate. |
| `robb-stark` | COMMANDS_IN | `storming-of-the-crag` | Tier-1 | — | "we took it by storm one night… while I broke the main gate with a ram" `asos-catelyn-02:143` | Robb commanded and led the storm; Rolph yielded to him. |
| `jon-umber-son-of-jon` | AGENT_IN | `storming-of-the-crag` | Tier-1 | — | "Black Walder and the Smalljon led scaling parties over the walls" `asos-catelyn-02:143` | The Smalljon = `jon-umber-son-of-jon`. Explicit scaling-party role. |
| `walder-frey-son-of-ryman` | AGENT_IN | `storming-of-the-crag` | Tier-1 | — | "Black Walder and the Smalljon led scaling parties over the walls" `asos-catelyn-02:143` | Black Walder = `walder-frey-son-of-ryman`. Explicit scaling-party role. |
| `grey-wind` | FIGHTS_IN | `storming-of-the-crag` | Tier-1 | — | "Grey Wind killed a man at the Crag" `asos-catelyn-02:185` | Direct book-cited kill at the Crag. |
| `rolph-spicer` | COMMANDS_IN | `storming-of-the-crag` | Tier-1 | — | "just before Ser Rolph yielded us the castle" `asos-catelyn-02:143` | Rolph was the defending castellan who surrendered; COMMANDS_IN from the defending side. |
| `storming-of-the-crag` | LOCATED_AT | `crag` | Tier-1 | — | "The Crag was weakly garrisoned, so we took it by storm one night" `asos-catelyn-02:143` | The node has NO LOCATED_AT edge per baseline.md gap list. Named in the battle title. |

### 3. Oxcross roster gap
| source | edge_type | target | tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| `lymond-vikary` | VICTIM_IN | `battle-of-oxcross` | Tier-1 | — | "Ser Lymond Vikary, Lord Crakehall, and Lord Jast" `acok-sansa-03:153` | Named dead at Oxcross; baseline identifies this as a gap (node exists, core_in=0). |

### 4. Grey Wind FIGHTS_IN gaps (Ashemark and Oxcross already have AGENT_IN but kill-cite is new)
Baseline shows `grey-wind AGENT_IN battle-of-oxcross` already EXISTS. Check for `taking-of-ashemark`:

| source | edge_type | target | tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| `grey-wind` | FIGHTS_IN | `taking-of-ashemark` | Tier-1 | — | "Grey Wind killed a man at the Crag, another at Ashemark" `asos-catelyn-02:185` | Direct book-cited kill at Ashemark. Baseline lists `grey-wind AGENT_IN battle-of-oxcross` but Ashemark is not listed. If AGENT_IN already exists at Ashemark, drop this; otherwise FIGHTS_IN fills the gap. **[BORDERLINE — verify against baseline whether any grey-wind role at Ashemark exists; if AGENT_IN exists, drop]** |

### 5. Robb wound — AFFLICTED_BY
**[BORDERLINE]** There is no named attacker for Robb's arrow wound at the Crag, so no KILLED_BY / ASSAULTS edge is possible. However, there is a structural edge:

| source | edge_type | target | tier | qualifier | quote + cite | rationale |
|--------|-----------|--------|------|-----------|--------------|-----------|
| `robb-stark` | AFFLICTED_BY | `storming-of-the-crag` | Tier-2 | — | "I took an arrow in the arm just before Ser Rolph yielded us the castle. It seemed nothing at first, but it festered." `asos-catelyn-02:143` | Robb's wound was taken during the storming. AFFLICTED_BY is in the locked vocab. **[BORDERLINE — AFFLICTED_BY usually targets a disease/condition, not an event; the synthesis should decide if this maps cleanly or if it should be node-prose only]** |

---

## Dropped / considered-but-rejected

- **Lancel's warg-sorcery propaganda as PERCEIVED_AS edge** — `lancel-lannister PERCEIVED_AS robb-stark [warg-commander]` — The PERCEIVED_AS type targets how a subject is perceived, not the perceiver's action. The quote belongs in node `## Quotes`, not an edge.
- **Rymund the Rhymer DEPICTED_IN edge** — `rymund-the-rhymer DEPICTED_IN battle-of-oxcross` — wrong direction; more correctly `rymund-the-rhymer WRITTEN_BY [song]` or the song DEPICTS the battle, but there is no `song-of-oxcross` node and minting one is out of scope for this lens.
- **Catelyn's victory roll-call** (`acok-catelyn-06:217`: "At Stone Mill, at Oxcross, in the Battle of the Camps, at the Whispering Wood") — a list of prior battles as temporal context, not a new edge; those events are already wired.
- **Westerling seashell banner as HELD_BY / OWNS** — Catelyn notices the seashell banner on the Westerling knight in the Great Hall (`asos-catelyn-02:37`). This is scene-setting; no new edge needed. Harvest instead.
- **Calyn notices Grey Wind absent from hall** — `asos-catelyn-02:81` — this is characterization of Robb distancing himself from his wolf post-marriage, a PASS-3 foreshadowing detail (wolf-bond degradation leading to the Red Wedding). Noted for PASS 3; not mintable now.
- **`robb-stark GUEST_OF westerling-household`** — Robb was nursed in Jeyne's own bed at the Crag. While structurally a guest relationship, `robb-stark GUEST_OF crag` would violate guest-right's canonical meaning (the sacred host-guest bond) and the marriage supersedes it. Skip.
- **`taking-of-ashemark ENABLES storming-of-the-crag`** — this is the CAUSAL RAID SPINE, correctly assigned to Lens D (causal spine) per the prompt. I note it here for completeness and to confirm I am NOT proposing it — it belongs to the lens that handles the causal ladder.
- **`battle-of-oxcross ENABLES taking-of-ashemark`** — same: Lens D territory, not Lens C.
- **Maester Vyman's report of Robb's wound** (`asos-catelyn-01:101-102`) — confirms the wound but adds no new quote sharper than Robb's own account in `asos-catelyn-02:143`. Use Robb's version as the anchor.
- **`black-walder-frey` twin disambiguation** — baseline already flags this. I used `walder-frey-son-of-ryman` throughout per instruction.
- **SUSPECTED_OF for Rolph Spicer** — `grey-wind OPPOSES rolph-spicer` already exists per baseline. The Spicer-trap whodunit is fully wired. Zero new SUSPECTED_OF proposed.
- **Grey Wind's kills as KILLS edges** (e.g., `grey-wind KILLS [unnamed knight at Crag]`) — the targets are unnamed; no node can be the target of a KILLS edge without a slug. FIGHTS_IN is the right type here.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food/drink | ACOK | acok-catelyn-06:211 | "agreed when he suggested breaking open some casks in honor of Stone Mill" — casks broken at Riverrun to celebrate the ford victory; victory-feast provisioning moment |
| food/drink | ACOK | acok-catelyn-06:181 | Great Hall supper while Rymund sings the Oxcross victory song — "Catelyn listened to girlish laughter … Rymund played his harp, accompanied by a pair of drummers and a youth with a set of reed pipes" — the Riverrun Oxcross celebration feast |
| food/drink | ASOS | asos-catelyn-01:81 | Catelyn's supper in confinement: "a modest supper of bread, cheese, and boiled beef with horseradish" — domestic provisioning under house-arrest |
| food/drink | ASOS | asos-catelyn-02:173 | Robb: "I would kill for a cup of wine" (after the Great Hall revelation scene) — food/drink as social lubricant at the key political moment |
| description/physical | ACOK | acok-sansa-03:153 | "Even war-trained destriers went mad. Knights were trampled to death in their pavilions" — the maddened destriers and the trampling; vivid physical mechanism of the rout |
| description/physical | ACOK | acok-sansa-03:153 | "the rabble woke in terror and fled, casting aside their weapons to run the faster. Ser Stafford was slain as he chased after a horse" — Stafford's ignominious death detail |
| description/physical | ASOS | asos-catelyn-02:143 | "It seemed nothing at first, but it festered" — the festering arrow wound; vivid detail of the wound that triggers the marriage |
| description/physical | ASOS | asos-catelyn-02:29 | Robb's changed appearance on return: "War had melted all the softness from his face and left him hard and lean. He had shaved his beard away, but his auburn hair fell uncut to his shoulders. The recent rains had rusted his mail and left brown stains on the white of his cloak" |
| description/physical | ASOS | asos-catelyn-02:29 | "On his head was the sword crown they had fashioned him of bronze and iron. He bears it more comfortably now. He bears it like a king." — the bronze-and-iron crown description |
| description/physical | ASOS | asos-catelyn-02:37 | "a young knight in a sand-colored surcoat blazoned with seashells" — the Westerling seashell banner; first physical description of the sigil on a knight's surcoat |
| description/physical | ASOS | asos-catelyn-02:111 | Jeyne's physical description: "pretty, undeniably, with her chestnut curls and heart-shaped face, and that shy smile. Slender, but with good hips" — Catelyn's physical assessment of the new queen |
| quote/propaganda | ACOK | acok-sansa-03:39 | Lancel's "army of wargs … feasted on the flesh of the slain" propaganda — the Lannister court's PERCEIVED_AS construction of Robb-as-warg-monster |
| quote/song | ACOK | acok-catelyn-06:181 | Rymund's refrain: "And the stars in the night were the eyes of his wolves, and the wind itself was their song" — the canonical in-world artistic response to Oxcross; half the hall howling along |
| quote/character | ASOS | asos-catelyn-02:143 | "I took her castle and she took my heart" — Robb's own formulation of the Crag→marriage causation |
| quote/character | ASOS | asos-catelyn-02:185 | "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross" — the only book-cited kill tally across all three PASS-2 battles |
| foreshadowing | ASOS | asos-catelyn-02:181-189 | Grey Wind bares teeth at Rolph Spicer; Catelyn urges Robb to send him away; Robb refuses; wolf-bond degradation and Spicer-whodunit foreshadow — PASS-3 thread, noted here, not minted |
| hospitality/Westerling | ASOS | asos-catelyn-02:143 | "Jeyne had me taken to her own bed" — Westerling hospitality: the wounded enemy king nursed in the lord's daughter's own bed; the hospitality moment that seals the marriage |
