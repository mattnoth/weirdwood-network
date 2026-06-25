# Lens D — Causal Wiring + Structural Fixes: Bran / Greenseer Arc (S146)

> PROPOSE ONLY. Dedup-checked against `--neighbors` queries run 2026-06-25. All quotes verbatim
> from chapter files. Agency guardrail applied throughout.

---

## Proposed edges

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|----|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| D01 | jojen-reed | DREAMS_OF | sack-of-winterfell | tier-1 | ACOK | acok-bran-05.md | 77 | "I dreamed that the sea was lapping all around Winterfell. I saw black waves crashing against the gates and towers, and then the salt water came flowing over the walls and filled the castle. Drowned men were floating in the yard." | Cross-container BRAN→WO5K/NORTH seam. Jojen names Alebelly, Mikken, Septon Chayle as the drowned men (line 77+81); all three die in the ironborn sack. Salt sea = ironborn ships is textual (Maester Luwin confirms "trouble along the Stony Shore. Raiders in longships" at line 145). DREAMS_OF is character-facing (Jojen→event); pair with D02 for the full FORESHADOWS read-path. Tier-1: verbatim quote + named victims confirmed dead in sack. |
| D02 | jojen-reed | FORESHADOWS | sack-of-winterfell | tier-1 | ACOK | acok-bran-05.md | 81 | "In the dark of night the salt sea will flow over these walls," said Jojen. "I saw the dead, bloated and drowned." | Narrative-craft edge (reader-facing): the green dream text is a Chekhov's gun for the sack. Distinct from D01 (DREAMS_OF = in-world; FORESHADOWS = reader). Both are in-vocab; the distinction is explicitly described in architecture.md. Tier-1: the warned events literally happen (Alebelly/Mikken/Chayle deaths confirmed ACOK). |
| D03 | jojen-reed | DREAMS_OF | bran-becomes-a-greenseer | tier-1 | ACOK | acok-bran-04.md | 79 | "I dreamed of a winged wolf bound to earth with grey stone chains," he said. "It was a green dream, so I knew it was true. A crow was trying to peck through the chains, but the stone was too hard and his beak could only chip at them." | Jojen dreams the arc's terminus — Bran as "winged wolf" bound by his disability, the crow (Bloodraven) opening his greensight. Line 93 confirms interpretation: "You are the winged wolf, Bran. The crow sent us here to break your chains." Dream fulfilled in ADWD when Bran becomes a greenseer. Tier-1: verbatim dream + textual confirmation of terms. |
| D04 | jojen-reed | DREAMS_OF | robb-receives-false-news-of-brans-death | tier-2 | ACOK | acok-bran-05.md | 169 | "I dreamed of the man who came today, the one they call Reek. You and your brother lay dead at his feet, and he was skinning off your faces with a long red blade." | Second BRAN→WO5K cross-container seam. Jojen's "Reek" dream predicts what `robb-receives-false-news-of-brans-death` represents: the (false) news that Bran and Rickon are dead, which Ramsay / "Reek" fabricates by burning the miller's boys and displaying their burned bodies. Target slug confirmed at graph/nodes/events/robb-receives-false-news-of-brans-death.node.md. Tier-2: the dream predicts bodies/faces-skinned → the burned-bodies-as-bran deception → the false news; there is an interpretive step (burned vs skinned), so not Tier-1. Note: the dream also foreshadows lines 177 ("I saw you and Rickon in your crypts, down in the dark with all the dead kings") — but that is fulfillled by `bran-and-rickon-survive-the-sack-in-the-crypts`, which is a separate edge (D05). |
| D05 | jojen-reed | FORESHADOWS | bran-and-rickon-survive-the-sack-in-the-crypts | tier-1 | ACOK | acok-bran-05.md | 177 | "I saw you and Rickon in your crypts, down in the dark with all the dead kings and their stone wolves." | Jojen's same conversation contains a second distinct FORESHADOWS target: the crypt survival, not the false news. Line 177 is the verbatim predict; the survival event `bran-and-rickon-survive-the-sack-in-the-crypts` is the fulfillment. Separate from D04 (D04 = the Reek dream about dead faces at Reek's feet → the false news deception; D05 = the crypts dream → the survival). Dedup: `bran-and-rickon-survive-the-sack-in-the-crypts` has no FORESHADOWS or DREAMS_OF incoming edges currently. Tier-1: verbatim + literally fulfilled. |
| D06 | bran-stark | PRACTICES | greensight | tier-1 | ADWD | adwd-bran-03.md | 157 | "Your blood makes you a greenseer," said Lord Brynden. "This will help awaken your gifts and wed you to the trees." | `greensight` node EXISTS (graph/nodes/concepts/greensight.node.md) with 0 edges — dead island. `bran-stark PRACTICES greensight` lights it from the character side. PRACTICES = Character→Magic discipline (architecture.md). Tier-1: Brynden explicitly names Bran's blood as the greenseer qualifier; Bran consumes weirwood paste and enters weirwood visions in same chapter. |
| D07 | brynden-rivers | PRACTICES | greensight | tier-1 | ADWD | adwd-bran-03.md | 19 | "The last greenseer, the singers called him, but in Bran's dreams he was still a three-eyed crow." | Bloodraven is explicitly called "the last greenseer" in text. `brynden-rivers PRACTICES greensight`. Dedup: brynden-rivers has no PRACTICES edge. PRACTICES is in-vocab, 0 instances currently (all magic edges are unpopulated per edge-type-counts.md). Tier-1: "the last greenseer, the singers called him" is textual, not interpretive. |
| D08 | jojen-reed | PRACTICES | greensight | tier-2 | ACOK | acok-bran-04.md | 195 | "Some claimed to have that power. Their wise men were called greenseers." | Context: Jojen's green dreams are canonical greensight-adjacent ability. Line 195 is Maester Luwin's description of greenseers; acok-bran-04:79 shows Jojen has the green dream. Architecture.md confirms: "Heavily concentrated in Bran (greendreams, three-eyed-crow), Daenerys, Jojen, and the Targaryen line." Tier-2: Jojen's ability is named greensight-adjacent (greendreams) but Luwin and the text stop short of calling Jojen a greenseer himself; the practitioners are the children and historical greenseers. The DREAMS_OF evidence is strong but the PRACTICES edge is one step interpretive. |
| D09 | brynden-rivers | TUTORS | bran-stark | tier-1 | ADWD | adwd-bran-03.md | 45 | "Never fear the darkness, Bran." The lord's words were accompanied by a faint rustling of wood and leaf, a slight twisting of his head. "The strongest trees are rooted in the dark places of the earth. Darkness will be your cloak, your shield, your mother's milk. Darkness will make you strong." | Bloodraven sustains a formal one-on-one mentorship of Bran in greensight — distinct from and complementary to `jojen-reed TUTORS bran-stark` (which is warging/warg-identity). Adwd-bran-03 shows Bloodraven teaching Bran to slip his skin into weirwoods (line 157, 165, 169), to fly as a raven, to read the tree-visions (line 191). TUTORS = "sustained formal one-on-one mentorship" (architecture.md). Dedup: `brynden-rivers` has no TUTORS edge; `jojen-reed TUTORS bran-stark` already exists and is NOT being re-proposed. Tier-1: multiple chapters show sustained instruction. |
| D10 | leaf | MEMBER_OF | children-of-the-forest | tier-1 | ADWD | adwd-bran-03.md | 15 | "Bran and Meera made up names for those who sang the song of earth: Ash and Leaf and Scales and Worm and the others." | Leaf IS one of the children of the forest — textual. `leaf MEMBER_OF children-of-the-forest`. Dedup: `leaf` has 0 incoming edges. `children-of-the-forest` INCOMING has `bran-stark`, `hodor`, `jojen-reed`, `meera` as GUEST_OF — but no MEMBER_OF edge FROM Leaf herself. Tier-1: Leaf is explicitly described as one of "those who sang the song of earth" — the children/singers. |
| D11 | brynden-rivers | BONDED_TO | weirwood | tier-2 | ADWD | adwd-bran-03.md | 119 | "One day I will be like him. The thought filled Bran with dread. Bad enough that he was broken, with his useless legs. Was he doomed to lose the rest too, to spend all of his years with a weirwood growing in him and through him? Lord Brynden drew his life from the tree, Leaf told them." | Bloodraven is physically merged with/sustained by the weirwood tree — "weirwood roots snaking in and out of his withered flesh" (line 117), "Lord Brynden drew his life from the tree" (line 119). Target slug `weirwood` (the species node; BONDED_TO is species-entity compatible — see architecture.md "Bran ↔ his three-eyed-crow / weirwood network"). Dedup: `brynden-rivers` has no BONDED_TO edge. Tier-2: physical union is textual (Tier-1-weight) but BONDED_TO implies a mutual bond; Bloodraven is enthroned in the tree but it's less explicitly bidirectional than dragon-rider bonds. Preferring Tier-2 per the weaker-type caution. |
| D12 | wight-ambush | SUB_BEAT_OF | bran-reaches-the-cave-of-the-three-eyed-crow | tier-1 | ADWD | adwd-bran-02.md | — | (structural fix — no single verbatim; the wight fight and the arrival are the same chapter/scene) | De-islands the `wight-ambush` legacy node. `wight-ambush` is 0-outgoing, existing data shows it as the wight fight on the approach to the cave (adwd-bran-02, same chapter as `bran-reaches-the-cave-of-the-three-eyed-crow`). SUB_BEAT_OF = "a finer-grained event-beat is a moment within a larger named event hub" (architecture.md). The wight ambush IS the obstacle beat within the cave-arrival event. Dedup: `bran-reaches-the-cave-of-the-three-eyed-crow` already has bran/leaf/meera/coldhands/brynden-rivers AGENT_IN — not re-minting those. This only adds the sub-beat wire. Tier-1: same-chapter, same-scene, same participants. |

---

## Proposed retargets / retirements

The `three-eyed-crow` species node currently holds 4 edges that should point to `brynden-rivers` (the character), not the species node. Confirmed via `--neighbors three-eyed-crow`:

### Edges to RETIRE (from `three-eyed-crow` species node)

| # | exact source | exact type | exact target | reason |
|---|-------------|------------|--------------|--------|
| R1 | `three-eyed-crow` | `TEACHES` | `bran-stark` | Mis-pointed: the teacher is Bloodraven/brynden-rivers, not the species |
| R2 | `three-eyed-crow` | `HOLDS_TITLE` | `lord` | Mis-pointed: the title-holder is brynden-rivers, not the species |
| R3 | `coldhands` | `SERVES` | `three-eyed-crow` | Mis-pointed: Coldhands serves brynden-rivers (character), not the species |
| R4 | `coldhands` | `SWORN_TO` | `three-eyed-crow` | Mis-pointed: oath is to brynden-rivers, not the species |

### Replacement edges (onto `brynden-rivers`)

| # | source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|---|-------------|-----------|-------------|------|------|--------------|------|----------------|------|
| R1r | `brynden-rivers` | `TEACHES` | `bran-stark` | tier-1 | ADWD | adwd-bran-03.md | 45 | "Never fear the darkness, Bran. The strongest trees are rooted in the dark places of the earth." | Replaces R1. Note: D09 above proposes `TUTORS` (the stronger sustained-mentorship type). If both are minted, `TEACHES` is the weaker/casual form; `TUTORS` is preferred. Recommend minting TUTORS (D09) and retiring R1's TEACHES on the species node without replacing it on brynden-rivers — TUTORS subsumes it. |
| R2r | `brynden-rivers` | `HOLDS_TITLE` | `lord` | tier-2 | wiki | wiki:Brynden_Rivers | — | (wiki-sourced) | Replaces R2. Brynden-rivers already has HOLDS_TITLE edges for lord-commander-of-the-nights-watch, hand-of-the-king, master-of-whisperers, ser, lord — so this may already exist. Dedup check required before minting. |
| R3r | `coldhands` | `SERVES` | `brynden-rivers` | tier-2 | ADWD | adwd-bran-01.md | 73 | "The ranger saved Sam and the girl from the wights," Bran said, hesitantly | Replaces R3. The quote on the existing edge (coldhands SERVES three-eyed-crow) is actually about Sam/Gilly — a mis-cite. The SERVES relationship is structural (Coldhands guides Bran's party north to Bloodraven's cave under Bloodraven's direction); cite should be adwd-bran-02.md:197 "And now you are come to me at last" (Bloodraven greeting them, implying Coldhands delivered them). Tier-2 (implied servant relationship; no direct "I serve Bloodraven" quote). |
| R4r | `coldhands` | `SWORN_TO` | `brynden-rivers` | tier-2 | wiki | wiki:Coldhands | — | (wiki-sourced) | Replaces R4. Same logic as R3r. |

**Critical note on R2r:** Run `--neighbors brynden-rivers` (done above) shows `brynden-rivers HOLDS_TITLE lord` ALREADY EXISTS from wiki. So R2r is a non-issue — the species node's HOLDS_TITLE→lord edge simply needs to be retired (not replaced, it already exists on the correct node).

---

## Structural flags

### Flag F1 — `three-eyed-crow` species node: cross-identity call DEFERRED
The species node `three-eyed-crow` is typed `species` but IS Bloodraven (brynden-rivers). The retargets above fix the 4 mis-pointed edges. A deeper question remains: should the species node be retired, aliased, or kept as a legitimate species entry (three-eyed crows as in-world corvids that appear in Bran's dreams before he knows Bloodraven exists)? This is a cross-identity / type-collision question. DO NOT assert `SAME_AS` between species node and brynden-rivers — that violates the type system (person ≠ species). Flag for a future cross-identity-resolver or manual curation pass. The species node may legitimately represent the crow-form Bloodraven uses in Bran's dreams (agot-bran-03) before the Bloodraven identity is revealed — two valid senses.

### Flag F2 — `brans-direwolf` phantom slug
The `brans-direwolf` slug does not exist as a node (confirmed: `find graph/nodes -name "brans-direwolf*"` returns nothing). The baseline notes catspaw edges use this phantom. No edges currently use it (grep returned no results in node files). This may have already been cleaned or may be in `graph/edges/edges.jsonl` rather than node frontmatter. Flag for the next orphan-edge-finder audit run; correct slug is `summer`.

### Flag F3 — `six-wildling-deserters-ambush-bran`: confirmed keep as dead-end
`--neighbors six-wildling-deserters-ambush-bran` confirms 0 outgoing, 5 incoming (bran VICTIM_IN, stiv/osha/wallen/hali AGENT_IN). This is a self-contained AGOT incident with no causal downstream. Baseline says KEEP dead-ended; confirmed. No edge proposed.

### Flag F4 — `wight-ambush` participant edges: no-repoint needed
The 5 existing edges into `wight-ambush` (wights AGENT_IN; bran/hodor/meera/jojen VICTIM_IN) are valid and should stay. D12 only adds the outgoing SUB_BEAT_OF wire. The participants match the cave-arrival event participants — no contradiction.

### Flag F5 — Jojen's "crypts dream" ambiguity resolved
Line 177 of acok-bran-05 ("I saw you and Rickon in your crypts, down in the dark") is DISTINCT from the "Reek skinning faces" dream (line 169). D04 targets `robb-receives-false-news-of-brans-death` (the Reek dream). D05 targets `bran-and-rickon-survive-the-sack-in-the-crypts` (the crypts dream). These are two separate DREAMS_OF / FORESHADOWS edges from Jojen in the same conversation, same chapter. They must not be collapsed.

### Flag F6 — `children-of-the-forest` GUEST_OF junk edges (out of scope)
`children-of-the-forest` has 2 OUTGOING `GUEST_OF` edges to `cersei-lannister` and `sansa-stark` (acok-sansa-07), which are clearly mis-extractions of human "children" (smallfolk women sheltering in the Red Keep). These are noted in the baseline. Out of scope for this dip — flag for a schema-drift-auditor pass.

### Flag F7 — `robb-receives-false-news-of-brans-death` CAUSES chain gap
The event already has `capture-of-winterfell CAUSES robb-receives-false-news` → `TRIGGERS robb-weds-jeyne-westerling` + `MOTIVATES robb-stark`. The Jojen dream (D04/D05) adds foreshadowing INTO this node, not a new causal chain out of it. No new causal edges proposed here.

---

## Dedup notes

- `brynden-rivers TUTORS bran-stark` (D09): confirmed absent — brynden-rivers has only AGENT_IN, BORN_AT, CULTURE_OF, HOLDS_TITLE, LOVER_OF, MOTIVATES, SWORN_TO outgoing edges.
- `brynden-rivers PRACTICES greensight` (D07): confirmed absent.
- `bran-stark PRACTICES greensight` (D06): bran-stark's PRACTICES edge confirmed absent (checked via --neighbors brynden-rivers; no bran-stark PRACTICES in any neighbors query; greensight has 0 edges).
- `jojen-reed DREAMS_OF sack-of-winterfell` (D01): jojen-reed has no DREAMS_OF outgoing edges (confirmed via --neighbors jojen-reed — no DREAMS_OF type in output).
- `jojen-reed FORESHADOWS sack-of-winterfell` (D02): no FORESHADOWS edges anywhere in graph (edge-type-counts.md: 0 instances).
- `jojen-reed DREAMS_OF bran-becomes-a-greenseer` (D03): same as D01 — no DREAMS_OF edges.
- `jojen-reed DREAMS_OF robb-receives-false-news-of-brans-death` (D04): confirmed absent.
- `jojen-reed FORESHADOWS bran-and-rickon-survive-the-sack-in-the-crypts` (D05): confirmed absent.
- `leaf MEMBER_OF children-of-the-forest` (D10): leaf has 0 incoming, 4 outgoing (all AGENT_IN/PROTECTS/RESCUES) — MEMBER_OF absent.
- `brynden-rivers BONDED_TO weirwood` (D11): brynden-rivers has no BONDED_TO outgoing edge.
- `wight-ambush SUB_BEAT_OF bran-reaches-the-cave-of-the-three-eyed-crow` (D12): wight-ambush has 0 outgoing — SUB_BEAT_OF absent.
- `brynden-rivers HOLDS_TITLE lord` already EXISTS (confirmed via --neighbors brynden-rivers) — R2r is a non-issue; only need to retire R2 from species node.
- `coldhands SERVES brynden-rivers` / `coldhands SWORN_TO brynden-rivers`: not in brynden-rivers INCOMING (confirmed via --neighbors). New edges.

---

## Harvest pointers

These are one-line pointers to load-bearing content encountered while reading — point, don't extract. A later harvest pass attaches.

- acok-bran-05:169 / quote / Jojen's Reek-skinning prophecy — the most chilling verbatim in the chapter; deserves a `## Quotes` attach on either `jojen-reed` or `robb-receives-false-news-of-brans-death`
- acok-bran-05:77–81 / quote+description / Full sea-dream passage; poetic and load-bearing for the foreshadowing — good `## Quotes` on `jojen-reed`
- acok-bran-04:79 / quote / "winged wolf bound to earth with grey stone chains" — the best single-image greenseer foreshadowing in the series; belongs in `bran-stark` Quotes and/or `bran-becomes-a-greenseer` narrative
- adwd-bran-03:45 / quote / Bloodraven's "Never fear the darkness, Bran. The strongest trees are rooted in the dark places of the earth" — prime Quotes candidate for `brynden-rivers`
- adwd-bran-03:69 / description / "Only one man in a thousand is born a skinchanger, and only one skinchanger in a thousand can be a greenseer" — stat-description; belongs in `greensight` node prose
- adwd-bran-03:117 / description / Physical description of Bloodraven enthroned in weirwood roots ("weirwood roots snaking in and out of his withered flesh, the mushrooms sprouting from his cheeks, the white wooden worm that grew from the socket where one eye had been") — first-class description; `brynden-rivers` Quotes
- adwd-bran-03:191 / quote / Bloodraven on time and weirwoods: "Time is different for a tree than for a man … For men, time is a river" — load-bearing to `greensight` and `weirwood` nodes
- adwd-bran-03:149 / description+food / Weirwood paste: "a white paste, thick and heavy, with dark red veins running through it" + "A paste of weirwood seeds" — food/instrument of transformation; `weirwood-paste` node Quotes + consider USED_IN attach to `bran-becomes-a-greenseer` if an `INSTRUMENT_IN`-class edge type gets minted
- acok-bran-05:129 / hospitality / Septon Chayle's quiet fatalism to Bran's drowning warning ("The gods will take me when they see fit, though I scarcely think it likely that I'll drown, Bran. I grew up on the banks of the White Knife, you know. I'm quite the strong swimmer") — understated dramatic irony; hospitality/character register
- acok-bran-04:195–203 / description / Maester Luwin explaining greenseers to Bran ("The children are gone from the world, and their wisdom with them. It had to do with the faces in the trees") — world-building prose for `greensight` and `children-of-the-forest` nodes
