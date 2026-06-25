# Lens C — Object / Place / Descriptive Depth
## Bran / greenseer arc enrichment — S146

> **PROPOSE, don't mint.** Orchestrator line-checks and fresh-verifies before minting.
> All dedup checks run against `graph/edges/edges.jsonl` and `find graph/nodes` before this proposal.

---

## Proposed edges

> Format: id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | "verbatim quote" | note

| id | source | edge | target | tier | book | chapter-file | line | verbatim quote | note |
|----|--------|------|--------|------|------|-------------|------|----------------|------|
| CE-01 | `black-gate` | `LOCATED_AT` | `nightfort` | 1 | ASOS | `asos-bran-04.md` | 209 | "There's a gate. A hidden gate, as old as the Wall itself. The Black Gate, he called it." | The Black Gate is embedded in the well of the Nightfort kitchen. Node `nightfort` EXISTS; node `black-gate` EXISTS; no LOCATED_AT edge exists. Direction: the object (black-gate) → its containing structure (nightfort). Tier-1: Sam's own words, verbatim. |
| CE-02 | `black-gate` | `MADE_OF` | `weirwood` | 1 | ASOS | `asos-bran-04.md` | 307 | "It was white weirwood, and there was a face on it." | The door is explicitly weirwood. `weirwood` species node EXISTS. `MADE_OF` schema: artifact → material; `black-gate` is typed `place.location` not `object.artifact` — flag: architecture note at CE-02a below. Tier-1: direct prose statement. |
| CE-03 | `brynden-rivers` | `LOCATED_AT` | `cave-of-the-three-eyed-crow` | 1 | ADWD | `adwd-bran-02.md` | 191–193 | "Before them a pale lord in ebon finery sat dreaming in a tangled nest of roots, a woven weirwood throne that embraced his withered limbs as a mother does a child." | Bloodraven resides in the cave permanently; no LOCATED_AT edge exists from brynden-rivers to the cave node. Slug trap: use `brynden-rivers`, NOT `three-eyed-crow`. `cave-of-the-three-eyed-crow` EXISTS. Tier-1: Bran witnesses directly. |
| CE-04 | `bran-stark` | `LOCATED_AT` | `cave-of-the-three-eyed-crow` | 1 | ADWD | `adwd-bran-03.md` | 43 | "The singers made Bran a throne of his own, like the one Lord Brynden sat, white weirwood flecked with red, dead branches woven through living roots. They placed it in the great cavern by the abyss." | Bran is installed in the cave with his own weirwood throne; his residence there is the arc's terminus state. No LOCATED_AT edge from bran-stark to cave exists. Tier-1. |
| CE-05 | `wight-ambush` | `SUB_BEAT_OF` | `bran-reaches-the-cave-of-the-three-eyed-crow` | 2 | ADWD | `adwd-bran-02.md` | 87–121 | "All around him, wights were rising from beneath the snow." | The wight ambush is a beat INSIDE the cave-approach event. Baseline flags this as a structural fix. `wight-ambush` EXISTS as a node with AGENT_IN/VICTIM_IN edges but zero outgoing causal edges (orphaned). `SUB_BEAT_OF` IS in the locked vocab (1 existing instance). No dedup conflict. Tier-2 (structural). |
| CE-06 | `leaf` | `MEMBER_OF` | `children-of-the-forest` | 1 | ADWD | `adwd-bran-02.md` | 135–141 | "She's a child. A child of the forest. … 'The First Men named us children,' the little woman said." | Leaf is identified as one of the children of the forest. `children-of-the-forest` EXISTS (`species`). `leaf` node should exist — verify slug before mint; if missing, this edge cannot be emitted without the node. Tier-1. |
| CE-07 | `brynden-rivers` | `TUTORS` | `bran-stark` | 1 | ADWD | `adwd-bran-03.md` | 51–52 | "A wild stallion will buck and kick when a man tries to mount him … but a horse that has known one rider will accept another. Young or old, these birds have all been ridden. Choose one now, and fly." | Brynden teaches Bran to warg ravens and to enter the weirwood roots — distinct tutelage from Jojen's naming (which was already wired as `jojen-reed TUTORS bran-stark`). This is the greenseer instruction track. No `brynden-rivers TUTORS bran-stark` edge exists. Tier-1. |
| CE-08 | `brynden-rivers` | `PRACTICES` | `greensight` | 1 | ADWD | `adwd-bran-03.md` | 19–25 | "He has a thousand eyes and one, but there is much to watch. One day you will know." + "Most of him has gone into the tree … He has lived beyond his mortal span." | Brynden is explicitly "the last greenseer" (narrative + Leaf's words). `greensight` EXISTS; no `brynden-rivers PRACTICES greensight` edge in the graph. Tier-1. |
| CE-09 | `bran-stark` | `PRACTICES` | `greensight` | 1 | ADWD | `adwd-bran-03.md` | 167–171 | "'Close your eyes,' said the three-eyed crow. 'Slip your skin … But this time, go into the roots instead.' … Then all at once he was back home again." | Bran successfully looks through the heart tree at Winterfell immediately after eating the paste. `greensight` EXISTS; no `bran-stark PRACTICES greensight` in the graph (he has `bran-stark WARGS_INTO summer` but nothing wired to greensight). Tier-1. |
| CE-10 | `bran-stark` | `PRACTICES` | `greenseer` | 1 | ADWD | `adwd-bran-03.md` | 73 | "'Only one skinchanger in a thousand can be a greenseer.' … 'I thought the greenseers were the wizards of the children,' Bran said." | Bloodraven confirms Bran is becoming a greenseer. `greenseer` EXISTS (concept.magic). No `bran-stark PRACTICES greenseer` edge. Tier-1. |
| CE-11 | `brynden-rivers` | `BONDED_TO` | `weirwood` | 1 | ADWD | `adwd-bran-03.md` | 115–119 | "Seated on his throne of roots in the great cavern, half-corpse and half-tree, Lord Brynden seemed less a man than some ghastly statue made of twisted wood, old bone, and rotted wool … The only thing that looked alive in the pale ruin that was his face was his one red eye … the weirwood roots snaking in and out of his withered flesh." | Bloodraven is physically merged with the weirwood roots — a literal bond. `BONDED_TO` is in vocab (used for warg-animal pairing and dragon bonds). `weirwood` species node EXISTS. Distinct from `bran-stark BONDED_TO summer` pattern. Tier-1. |

> **CE-02a architecture note:** `black-gate` is typed `place.location`, but `MADE_OF` in architecture.md specifies `Artifact → Material`. A weirwood gate embedded in a wall could reasonably be `object.artifact` (it's a named magical object with agency), but the existing node is `place.location`. Options for the orchestrator: (a) emit the `MADE_OF` edge noting the type-bend, since the schema says the edge is for "composition" and this is compositional fact; (b) fold it into a `## Appearances & Description` quote attach only; (c) flag for type-review (is the Black Gate better typed `object.artifact`?). Recommendation: emit the edge with a note (`"architectural element typed as place.location; MADE_OF used for material composition"`), and flag for the multi-type-entity-resolver. Do NOT hold up the quote attach.

---

## Proposed quote / description attaches

> Format: node_slug | section | "verbatim quote" | cite | note

### `brynden-rivers` — `## Appearances & Description`

**QD-01** — Bloodraven's body in the weirwood throne, first sight:
> "Before them a pale lord in ebon finery sat dreaming in a tangled nest of roots, a woven weirwood throne that embraced his withered limbs as a mother does a child. His body was so skeletal and his clothes so rotted that at first Bran took him for another corpse, a dead man propped up so long that the roots had grown over him, under him, and through him. What skin the corpse lord showed was white, save for a bloody blotch that crept up his neck onto his cheek. His white hair was fine and thin as root hair and long enough to brush against the earthen floor. Roots coiled around his legs like wooden serpents. One burrowed through his breeches into the desiccated flesh of his thigh, to emerge again from his shoulder. A spray of dark red leaves sprouted from his skull, and grey mushrooms spotted his brow. A little skin remained, stretched across his face, tight and hard as white leather, but even that was fraying, and here and there the brown and yellow bone beneath was poking through."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:191–194`

**QD-02** — Bloodraven's eye and the one white root:
> "Are you the three-eyed crow?" Bran heard himself say. A three-eyed crow should have three eyes. He has only one, and that one red. Bran could feel the eye staring at him, shining like a pool of blood in the torchlight. Where his other eye should have been, a thin white root grew from an empty socket, down his cheek, and into his neck."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:195`

**QD-03** — Bloodraven's half-corpse, half-tree second description (ADWD Bran III):
> "Seated on his throne of roots in the great cavern, half-corpse and half-tree, Lord Brynden seemed less a man than some ghastly statue made of twisted wood, old bone, and rotted wool. The only thing that looked alive in the pale ruin that was his face was his one red eye, burning like the last coal in a dead fire, surrounded by twisted roots and tatters of leathery white skin hanging off a yellowed skull."
— Bran POV, ADWD Bran III, `adwd-bran-03.md:115`

**QD-04** — Bloodraven's name reveal:
> "When Meera Reed had asked him his true name, he made a ghastly sound that might have been a chuckle. 'I wore many names when I was quick, but even I once had a mother, and the name she gave me at her breast was Brynden.'"
— Bran POV, ADWD Bran III, `adwd-bran-03.md:19`

**QD-05** — "You will never walk again … but you will fly":
> "'You will never walk again, Bran,' the pale lips promised, 'but you will fly.'"
— Brynden Rivers to Bran, ADWD Bran II, `adwd-bran-02.md:205`. [This line echoes the coma-crow's promise and closes the arc's setup; it is THE signature quote for Bloodraven's character role in Bran's story. Already captured on the `bran-reaches-the-cave-of-the-three-eyed-crow` edge as evidence_quote; propose also adding to `## Quotes` on `brynden-rivers` node.]

### `brynden-rivers` — `## Quotes`

**QD-06** — Bloodraven on the weirwood and time:
> "For men, time is a river. We are trapped in its flow, hurtling from past to present, always in the same direction. The lives of trees are different. They root and grow and die in one place, and that river does not move them. The oak is the acorn, the acorn is the oak. And the weirwood … a thousand human years are a moment to a weirwood, and through such gates you and I may gaze into the past."
— Brynden Rivers to Bran, ADWD Bran III, `adwd-bran-03.md:191`

**QD-07** — Bloodraven's thousand eyes:
> "I have watched you for a long time, watched you with a thousand eyes and one. I saw your birth, and that of your lord father before you. I saw your first step, heard your first word, was part of your first dream. I was watching when you fell."
— Brynden Rivers to Bran, ADWD Bran II, `adwd-bran-02.md:197`

**QD-08** — On the ravens:
> "It was the singers who taught the First Men to send messages by raven … but in those days, the birds would speak the words. The trees remember, but men forget, and so now they write the messages on parchment and tie them round the feet of birds who have never shared their skin."
— Brynden Rivers to Bran, ADWD Bran III, `adwd-bran-03.md:63`

### `cave-of-the-three-eyed-crow` — `## Appearances & Description`

**QD-09** — Arrival at the root-filled passage (the weirwood root revelation):
> "The roots were everywhere, twisting through earth and stone, closing off some passages and holding up the roofs of others. All the color is gone, Bran realized suddenly. The world was black soil and white wood. The heart tree at Winterfell had roots as thick around as a giant's legs, but these were even thicker. And Bran had never seen so many of them. There must be a whole grove of weirwoods growing up above us."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:179`. [Already partially in the cave node's `## Quotes` from wiki; this is the verbatim book-cite overlay onto the existing paraphrase — append with explicit `adwd-bran-02.md:179` cite.]

**QD-10** — The bone-floor passage and skull niches:
> "Bran saw a bear skull and a wolf skull, half a dozen human skulls and near as many giants. All the rest were small, queerly formed. Children of the forest. The roots had grown in and around and through them, every one."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:183`. [This quote is already on the cave node as a book-cite overlay, but cited as `:183` — CONFIRMED correct, no change needed. Note: the preceding description "The floor of the passage was littered with the bones of birds and beasts. But there were other bones as well, big ones that must have come from giants and small ones that could have been from children" at `:183` provides the lead-in context worth keeping.]

**QD-11** — The weirwood throne and the chasm (first encounter):
> "Near a natural bridge across the abyss is the three-eyed crow, the last greenseer, sitting on a throne of woven weirwood roots." (wiki paraphrase already on node); book cite: ADWD Bran II, `adwd-bran-02.md:191` (the full description is QD-01 above — point to that).

**QD-12** — Bran's own weirwood throne:
> "The singers made Bran a throne of his own, like the one Lord Brynden sat, white weirwood flecked with red, dead branches woven through living roots. They placed it in the great cavern by the abyss, where the black air echoed to the sound of running water far below. Of soft grey moss they made his seat. Once he had been lowered into place, they covered him with warm furs."
— Bran POV, ADWD Bran III, `adwd-bran-03.md:43`

**QD-13** — Leaf's warning about the cave's depths:
> "'Men should not go wandering in this place,' Leaf warned them. 'The river you hear is swift and black, and flows down and down to a sunless sea. And there are passages that go even deeper, bottomless pits and sudden shafts, forgotten ways that lead to the very center of the earth. Even my people have not explored them all, and we have lived here for a thousand thousand of your man-years.'"
— Leaf to the party, ADWD Bran III, `adwd-bran-03.md:91`. [Already on cave node as a `## Quotes` entry (wiki-sourced); this is the verbatim book cite — append `adwd-bran-03.md:91`.]

**QD-14** — Bloodraven's instruction to Bran: "Never fear the darkness":
> "'Never fear the darkness, Bran.' The lord's words were accompanied by a faint rustling of wood and leaf, a slight twisting of his head. 'The strongest trees are rooted in the dark places of the earth. Darkness will be your cloak, your shield, your mother's milk. Darkness will make you strong.'"
— Brynden Rivers to Bran, ADWD Bran III, `adwd-bran-03.md:45`. [This belongs on BOTH `brynden-rivers ## Quotes` AND as a `## Narrative Arc` note on `cave-of-the-three-eyed-crow`.]

### `weirwood-paste` — `## Quotes` / `## Appearances & Description`

**QD-15** — The paste's appearance (served in a weirwood bowl):
> "Inside was a white paste, thick and heavy, with dark red veins running through it."
— Bran POV, ADWD Bran III, `adwd-bran-03.md:149`. [ALREADY on weirwood-paste node as a book-cite quote — CONFIRMED. No change needed.]

**QD-16** — The paste's taste (full sequence, not abridged):
> "It had a bitter taste, though not so bitter as acorn paste. The first spoonful was the hardest to get down. He almost retched it right back up. The second tasted better. The third was almost sweet. The rest he spooned up eagerly. Why had he thought that it was bitter? It tasted of honey, of new-fallen snow, of pepper and cinnamon and the last kiss his mother ever gave him."
— Bran POV, ADWD Bran III, `adwd-bran-03.md:161–163`. [The node has the last sentence of this; propose adding the FULL sequence (bitter→better→sweet→honey) as it shows the transformation's arc. The existing quote begins at the end — start from `adwd-bran-03.md:161`.]

**QD-17** — Bloodraven's explanation of the paste's purpose:
> "'Your blood makes you a greenseer,' said Lord Brynden. 'This will help awaken your gifts and wed you to the trees.'"
— Brynden Rivers to Bran, ADWD Bran III, `adwd-bran-03.md:157`. [ALREADY on weirwood-paste node as a `## Quotes` entry — CONFIRMED. No change needed. This also belongs on `bran-becomes-a-greenseer` as its evidence_quote, which is already the case in edges.jsonl (edge CE-22468).]

**QD-18** — The paste's role in the greenseer transformation (Narrative Arc attach on weirwood-paste node):
The paste instrument tie to `bran-becomes-a-greenseer` is best handled as a `## Narrative Arc` prose note on the `weirwood-paste` node (not a new graph edge — no clean "ingested-in" type exists in the locked 170-type vocab). Propose adding to the node's `## Narrative Arc / A Dance with Dragons` section: "Bran eats the paste in `adwd-bran-03.md:161–163`; it immediately leads to his first weirwood-sight vision of Winterfell (`adwd-bran-03.md:171–175`) — the literal instrument of `bran-becomes-a-greenseer`."

### `black-gate` — `## Appearances & Description` / `## Quotes`

**QD-19** — First sight of the Black Gate's face:
> "A glow came from the wood, like milk and moonlight, so faint it scarcely seemed to touch anything beyond the door itself, not even Sam standing right before it. The face was old and pale, wrinkled and shrunken. It looks dead. Its mouth was closed, and its eyes; its cheeks were sunken, its brow withered, its chin sagging. If a man could live for a thousand years and never die but just grow older, his face might come to look like that."
— Bran POV, ASOS Bran IV, `asos-bran-04.md:309`. [Already on black-gate node as a `## Quotes` entry with `[book-cite overlay: Bran POV, ASOS Bran IV, sources/chapters/asos/asos-bran-04.md:309]` — CONFIRMED. No change needed.]

**QD-20** — The door opens and speaks:
> "The door opened its eyes. They were white too, and blind. 'Who are you?' the door asked, and the well whispered, 'Who-who-who-who-who-who-who.'"
— Bran POV, ASOS Bran IV, `asos-bran-04.md:311–313`. [Not currently on black-gate node. The existing quote stops at the description; the moment of awakening should be appended as an `## Appearances & Description` continuation: the door's eyes open (`:311`), the question echoes (`:313`).]

**QD-21** — The tear drop from the Black Gate as Bran passes:
> "Hodor ducked, but not low enough. The door's upper lip brushed softly against the top of Bran's head, and a drop of water fell on him and ran slowly down his nose. It was strangely warm, and salty as a tear."
— Bran POV, ASOS Bran IV, `asos-bran-04.md:317`. [Not on the black-gate node. This small sensory detail — the warm salty drop — is load-bearing atmosphere (the weirwood's "tear"). Belongs in `## Appearances & Description`.]

### `nightfort` — `## Appearances & Description`

**QD-22** — The twisted weirwood growing through the kitchen floor:
> "A twisted white weirwood pushing up through the gaping hole in the roof of the domed kitchen. … It made him feel as if the old gods were with him here, at least."
— Bran POV, ASOS Bran IV, `asos-bran-04.md:107`. [Not currently on nightfort node (the node's `## Appearances` mentions a twisted weirwood in the kitchens from wiki, but without the book citation or Bran's emotional response. Append the cite with quote.)]

### `children-of-the-forest` — `## Appearances & Description`

**QD-23** — Leaf's first description (as Bran sees her):
> "It was a girl, but smaller than Arya, her skin dappled like a doe's beneath a cloak of leaves. Her eyes were queer—large and liquid, gold and green, slitted like a cat's eyes. No one has eyes like that. Her hair was a tangle of brown and red and gold, autumn colors, with vines and twigs and withered flowers woven through it."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:135`

**QD-24** — Leaf's voice:
> "That was not Arya's voice, nor any child's. It was a woman's voice, high and sweet, with a strange music in it like none that he had ever heard and a sadness that he thought might break his heart."
— Bran POV, ADWD Bran II, `adwd-bran-02.md:133`

**QD-25** — Leaf on the children's physical nature (ADWD Bran III):
> "They were small compared to men, as a wolf is smaller than a direwolf. That does not mean it is a pup. They had nut-brown skin, dappled like a deer's with paler spots, and large ears that could hear things that no man could hear. Their eyes were big too, great golden cat's eyes that could see down passages where a boy's eyes saw only blackness. Their hands had only three fingers and a thumb, with sharp black claws instead of nails."
— Bran POV, ADWD Bran III, `adwd-bran-03.md:93`

**QD-26** — Leaf on the children's dwindling ("our long dwindling"):
> "'Before the First Men came all this land that you call Westeros was home to us, yet even in those days we were few … Now it sinks, and this is our long dwindling. The giants are almost gone as well, they who were our bane and our brothers.'"
— Leaf to Bran, ADWD Bran III, `adwd-bran-03.md:97`

### `summer` (direwolf) — `## Quotes` / Narrative-Arc attach

**QD-27** — Summer in the wolf-dream sensory texture (acok-bran-03 feast scene):
> "It is cool in the godswood now. Steam is rising off the hot pools, and the red leaves of the weirwood are rustling. The smells are richer than here, and before long the moon will rise and my brother will sing to it."
— Bran POV drifting into Summer, ACOK Bran III, `acok-bran-03.md:37`. [Load-bearing: captures the cross-modal sensory shift when Bran slips into Summer — the "smells are richer" detail is the warging texture in miniature.]

**QD-28** — Summer in the cave (snow-buried undead arm):
> "The moon was a crescent, thin and sharp as the blade of a knife. Summer dug up a severed arm, black and covered with hoarfrost, its fingers opening and closing as it pulled itself across the frozen snow. There was still enough meat on it to fill his empty belly, and after that was done he cracked the arm bones for the marrow. Only then did the arm remember it was dead."
— Bran POV (Summer POV fragment), ADWD Bran III, `adwd-bran-03.md:111`. [Most visually striking wolf-dream passage in the arc. Belongs on `summer` node under `## Narrative Arc` and/or `## Quotes`.]

---

## Proposed new nodes

### OPTIONAL: `weirwood-throne` (object.artifact)

**Assessment:** The cave contains TWO distinct weirwood thrones — one for Brynden Rivers (woven from living roots, pre-existing) and one made for Bran by the children (described separately at `adwd-bran-03.md:43`). The baseline already treats the "weirwood throne" as descriptive depth on existing nodes rather than a standalone node. Recommendation: **DO NOT MINT** a new node. The thrones are fixed architectural features of the cave and are best handled as descriptive content on `brynden-rivers` (`## Appearances & Description`) and `cave-of-the-three-eyed-crow` (`## Narrative Arc`). They are not named artifacts with independent narrative trajectories; minting would violate the enrichment-is-edge-first rule.

### VERDICT on cave-of-the-three-eyed-crow

The cave node EXISTS and is already richly described. No new cave node is needed. Proposed additions: `LOCATED_AT` edges (CE-03, CE-04) + quote/description attaches (QD-09 through QD-14).

---

## Dedup notes

1. **`black-gate` LOCATED_AT `nightfort`** — edges.jsonl search: only `nightfort SEAT_OF nights-watch` exists; no LOCATED_AT between these two nodes. **CLEAR.**
2. **`brynden-rivers` LOCATED_AT `cave-of-the-three-eyed-crow`** — only `brynden-rivers AGENT_IN bran-reaches-the-cave-of-the-three-eyed-crow` exists. No LOCATED_AT. **CLEAR.**
3. **`brynden-rivers` TUTORS `bran-stark`** — only `jojen-reed TUTORS bran-stark` found; `brynden-rivers` has no TUTORS edge. **CLEAR.**
4. **`brynden-rivers` PRACTICES `greensight`** — `greensight` node has 0 edges (confirmed). **CLEAR.**
5. **`bran-stark` PRACTICES `greensight`** — `greensight` node has 0 edges. **CLEAR.**
6. **`brynden-rivers` BONDED_TO `weirwood`** — no BONDED_TO edges from brynden-rivers found. **CLEAR.**
7. **`wight-ambush` SUB_BEAT_OF `bran-reaches-the-cave…`** — existing wight-ambush edges are AGENT_IN/VICTIM_IN only; no SUB_BEAT_OF outgoing. **CLEAR.**
8. **`leaf` MEMBER_OF `children-of-the-forest`** — verify `leaf` node slug before emitting. No MEMBER_OF found in the search. Likely clear but needs node-existence check.
9. **weirwood-paste quotes (QD-15, QD-17)** — ALREADY on the node; confirmed in file read. Do not re-add.
10. **Cave descriptions QD-09, QD-13** — wiki-sourced paraphrases already on cave node; proposals are book-cite overlays (verbatim + line number). Additive, not duplicate.
11. **Black-gate QD-19** — already on node with cite. Confirmed. No change needed.
12. **`black-gate` MADE_OF `weirwood`** — no MADE_OF edges from `black-gate` in edges.jsonl. CLEAR, subject to type-bend flag (CE-02a).
13. **`bran-stark` PRACTICES `greenseer`** — `greenseer` node has 0 edges (confirmed in file). **CLEAR.**

### Slug trap reminders for the orchestrator

- Bloodraven = `brynden-rivers` (NOT `three-eyed-crow`)
- Children of the forest individual = `leaf` (verify slug; another singer named `snowylocks` by Meera but no node)
- `weirwood` = species node (target of BONDED_TO, MADE_OF)
- `black-gate` (not `the-black-gate`)
- `cave-of-the-three-eyed-crow` (full slug)

---

## Harvest pointers

> One-line format: `chapter:line / kind / note`
> POINT don't extract — a later harvest pass attaches.

### Food & drink (grim register)

- `adwd-bran-02.md:65` / food / elk steaks eaten over 7 days after the elk's death — road-starvation and grief meal; Bran "ate twice, once in his own skin and once in Summer's"
- `adwd-bran-03.md:89` / food / cave daily fare: "almost every day they ate blood stew, thickened with barley and onions and chunks of meat" (suspected squirrel or rat); also mushrooms (a hundred kinds), blind white fish, goat cheese, oats, barleycorn, dried fruit
- `adwd-bran-03.md:111` / food / Summer eats a severed wight arm in the snowdrifts — wolf-dream meat, grim and visceral
- `asos-bran-04.md:127` / food / fish boned by Meera cooked in Nightfort kitchen — the first fire in the Nightfort's kitchens in centuries; narrative irony (the Rat Cook's kitchen)
- `adwd-bran-03.md:89` / food / "Jojen thought it might be squirrel meat, and Meera said that it was rat. Bran did not care." — cave-stew ambiguity; hospitality-of-necessity
- `adwd-bran-02.md:59` / food / journey starvation: Jojen "too weak to walk unaided," twelve days since elk died; the group exhausted and starved on approach

### Physical descriptions

- `adwd-bran-02.md:21` / description / Hodor's frozen appearance: "Icicles hung from the brown briar of his beard, and his mustache was a lump of frozen snot, glittering redly in the light of sunset." — extreme cold marker
- `adwd-bran-02.md:191–194` / description / Bloodraven's full corpse-king appearance (see QD-01 above — already captured; here as harvest pointer for cross-character description pass)
- `adwd-bran-03.md:93` / description / Children of the forest: three fingers + thumb, sharp black claws, golden cat-eyes (see QD-25)
- `adwd-bran-02.md:135` / description / Leaf's dappled doe-skin, autumn-color hair (see QD-23)
- `adwd-bran-02.md:93` / description / Wights: "Some wore black cloaks, some ragged skins, some nothing. All of them had pale flesh and black hands. Their eyes glowed like pale blue stars."
- `adwd-bran-03.md:11` / description / Bran's broken boy self-image counterposed to the moon-phase chapter structure ("Under the hill, the broken boy sat upon a weirwood throne, listening to whispers in the dark as ravens walked up and down his arms")
- `adwd-bran-03.md:119` / description / Bran's self-reckoning: "What was he now? Only Bran the broken boy, Brandon of House Stark, prince of a lost kingdom, lord of a burned castle, heir to ruins."

### Hospitality / guest right

- `adwd-bran-02.md:161` / hospitality / "It is warmer down deep, and no one will hurt you there." — Leaf offering protection; cave-as-refuge framing
- `adwd-bran-03.md:43` / hospitality / Children make Bran a weirwood throne with grey moss seat and cover him with warm furs — a guest's welcome given permanent form
- `asos-bran-04.md:127` / hospitality / Meera bones fish and cooks it in the Nightfort — first fire in that cursed kitchen; a small domesticity against the horror
- `adwd-bran-03.md:89` / hospitality / "Under the hill they still had food to eat. A hundred kinds of mushrooms grew down here. Blind white fish swam in the black river … They had cheese and milk from the goats …" — inventory of the cave's larder; children-of-the-forest provisioning

### Foreshadowing / Chekhov's guns

- `adwd-bran-03.md:57–58` / foreshadowing / "Someone else was in the raven … Some girl. I felt her." / Brynden: "A woman, of those who sing the song of earth. Long dead, yet a part of her remains … A shadow on the soul." — foreshadows that Bran will leave a "shadow on the soul" inside animals he wargs (relevant to the Hodor tragedy; theory-gate warning: stop here)
- `adwd-bran-03.md:121` / foreshadowing / "One day I will be like him" — Bran dreads becoming root-woven like Bloodraven; structural foreshadowing of the arc's implied endpoint
- `adwd-bran-03.md:219–223` / foreshadowing / Weirwood vision of a white-haired woman with a bronze sickle slashing a captive's throat at the heart tree; Bran "could taste the blood" — the weirwood-tree/greenseer violence foreshadowing, possibly linked to future events (theory-gate: don't push further)
- `adwd-bran-02.md:57` / foreshadowing / Coldhands: "The white walkers go lightly on the snow. You'll find no prints to mark their passage." — the Walkers' stealth nature, foreshadowing the final season of the series (harvest pointer only)

### Old Nan tales as in-world texts

- `asos-bran-04.md:19–20` / in-world text / Nightfort's ghosts: Night's King, Rat Cook, seventy-nine sentinels, Mad Axe, Danny Flint, Symeon Star-Eyes — Old Nan's stories used as textual texture here; candidate for `DEPICTED_IN` if object.text nodes for Old Nan's tales are ever minted
- `asos-bran-04.md:99–103` / in-world text / Night's King tale: "She always pinched Bran on the nose then … 'He was a Stark of Winterfell, and who can say? Mayhaps his name was Brandon.'" — the NightFort/Night's King story in full; Bran identified with the legend

### Weirwood heart tree at Winterfell

- `adwd-bran-03.md:173` / location-description / Heart tree in the godswood seen through weirwood-sight: "Lord Eddard Stark sat upon a rock beside the deep black pool in the godswood, the pale roots of the heart tree twisting around him like an old man's gnarled arms." — the godswood as seen through greensight; load-bearing quote for any heart-tree-at-winterfell node
- `adwd-bran-03.md:191` / quote / Bloodraven: "You were looking through the eyes of the heart tree in your godswood." — Bloodraven explicitly names the mechanism of greensight

### Ravens

- `adwd-bran-03.md:51–53` / description / Bran's first raven-warg: "quick as that he was not a boy looking at a raven but a raven looking at a boy. The song of the river suddenly grew louder, the torches burned a little brighter than before, and the air was full of strange smells." — the sensory shift of entering raven-skin; richest warg texture in the arc after wolf-dreams
