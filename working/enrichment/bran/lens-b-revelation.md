# Lens B — Greendream Catalogue + Revelation/Identity Thread
## Bran / greenseer arc enrichment dip (S146)

> **PROPOSE, don't mint.** All dedup checks done; see `## Dedup notes` below.
> Theory gate honoured: green dreams modeled as DREAMS_OF/FORESHADOWS of events that textually occur.
> Greenseer cosmology (time-travel, Bran-as-architect, Hodor-origin, Jojen-paste) NOT touched.

---

## Proposed edges

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter-file | line | verbatim quote | note |
|----|-------------|-----------|-------------|------|------|-------------|------|----------------|------|
| LB-01 | `jojen-reed` | `DREAMS_OF` | `sack-of-winterfell` | 1 | acok | acok-bran-05 | 77 | "I dreamed that the sea was lapping all around Winterfell. I saw black waves crashing against the gates and towers, and then the salt water came flowing over the walls and filled the castle. Drowned men were floating in the yard. When I first dreamed the dream, back at Greywater, I didn't know their faces, but now I do. That Alebelly is one, the guard who called our names at the feast. Your septon's another. Your smith as well." | "The sea comes to Winterfell" — Alebelly/Septon Chayle/Mikken all die in Theon's sack; salt sea = ironborn. BRAN↔WO5K/NORTH cross-container seam. High value. Verified: three named drowned men fulfill exactly. |
| LB-02 | `jojen-reed` | `FORESHADOWS` | `sack-of-winterfell` | 1 | acok | acok-bran-05 | 81 | "In the dark of night the salt sea will flow over these walls," said Jojen. "I saw the dead, bloated and drowned." | Reader-facing complement to LB-01. FORESHADOWS is the narrative-craft edge (detail→event); DREAMS_OF (LB-01) is the character-facing edge. Propose both — they are distinct relation types per architecture.md. |
| LB-03 | `jojen-reed` | `DREAMS_OF` | `bran-becomes-a-greenseer` | 1 | acok | acok-bran-04 | 79 | "I dreamed of a winged wolf bound to earth with grey stone chains," he said. "It was a green dream, so I knew it was true. A crow was trying to peck through the chains, but the stone was too hard and his beak could only chip at them." | The winged wolf = Bran; grey stone chains = his broken body/earth-bound state; the crow pecking through = Bloodraven freeing him into greensight. Confirmed by acok-bran-04:93 ("The crow sent us here to break your chains"). The terminus event `bran-becomes-a-greenseer` is the textual fulfillment. |
| LB-04 | `jojen-reed` | `FORESHADOWS` | `bran-becomes-a-greenseer` | 2 | acok | acok-bran-04 | 93 | "You are the winged wolf, Bran," said Jojen. "I wasn't sure when we first came, but now I am. The crow sent us here to break your chains." | Jojen explicitly interprets the dream as pointing to Bran's greenseer destiny. Tier 2 (strong textual inference) because the text identifies the dream's meaning but we're connecting it to the arc terminus. |
| LB-05 | `jojen-reed` | `DREAMS_OF` | `robb-receives-false-news-of-brans-death` | 1 | acok | acok-bran-05 | 169 | "Not drowned." Jojen spoke as if every word pained him. "I dreamed of the man who came today, the one they call Reek. You and your brother lay dead at his feet, and he was skinning off your faces with a long red blade." | **Target rationale:** the event Jojen dreams is Reek mounting burned boys as Bran & Rickon — this is the deception that CAUSES `robb-receives-false-news-of-brans-death`. The dream is literarily subverted (the boys aren't actually Bran/Rickon) — but Robb receives the news as real, so the dream "comes true" at the level of the reported event. DREAMS_OF is cleaner than FORESHADOWS here because it's the character-facing vision. BRAN↔WO5K seam (Reek/Bolton). |
| LB-06 | `bran-stark` | `PRACTICES` | `greensight` | 1 | adwd | adwd-bran-03 | 155 | "Will this make me a greenseer?" / "Your blood makes you a greenseer," said Lord Brynden. "This will help awaken your gifts and wed you to the trees." | Bran actively practices greensight after the weirwood paste; the paste awakens the already-present blood gift. Greensight node EXISTS at `graph/nodes/concepts/greensight.node.md` with 0 edges — this lights it. |
| LB-07 | `brynden-rivers` | `PRACTICES` | `greensight` | 1 | adwd | adwd-bran-03 | 19 | "The last greenseer, the singers called him, but in Bran's dreams he was still a three-eyed crow." | The singers' own designation. Brynden sits enthroned in the weirwood roots actively practicing greensight at the time Bran arrives. Strong Tier-1 — the text names him "the last greenseer" via the singers. |
| LB-08 | `jojen-reed` | `PRACTICES` | `greensight` | 1 | acok | acok-bran-04 | 77 | "My brother dreams as other boys do, and those dreams might mean anything," Meera said, "but the green dreams are different." | Meera distinguishes Jojen's green dreams as a distinct faculty. Architecture.md PRACTICES definition: "actively practices a named magical or ritual discipline." Greendreams are explicitly categorized as greensight at acok-bran-04:211 (Maester Luwin: "Call it greensight, if you wish"). This is the discipline, per Luwin's own framing. |
| LB-09 | `brynden-rivers` | `TUTORS` | `bran-stark` | 1 | adwd | adwd-bran-03 | 45 | "Never fear the darkness, Bran." The lord's words were accompanied by a faint rustling of wood and leaf, a slight twisting of his head. "The strongest trees are rooted in the dark places of the earth. Darkness will be your cloak, your shield, your mother's milk. Darkness will make you strong." | Sustained, direct one-on-one teaching of greensight / weirwood-sight to Bran (also adwd-bran-03:69, 191, 199). TUTORS = "sustained formal one-on-one mentorship." Brynden is explicitly called "his teacher" at adwd-bran-03:45. **DEDUP:** `jojen-reed TUTORS bran-stark` already exists. This is a distinct tutor (Bloodraven, not Jojen). Not a duplicate. |
| LB-10 | `brynden-rivers` | `BONDED_TO` | `weirwood` | 1 | adwd | adwd-bran-03 | 115 | "Seated on his throne of roots in the great cavern, half-corpse and half-tree, Lord Brynden seemed less a man than some ghastly statue made of twisted wood, old bone, and rotted wool." | The weirwood roots physically grow through him; he draws life from the tree (adwd-bran-03:119: "Lord Brynden drew his life from the tree, Leaf told them. He did not eat, he did not drink."). BONDED_TO covers the static magical bond "weirwood-bond (Bran ↔ his three-eyed-crow / weirwood network)" per architecture.md. Brynden's bond is deeper — root fusion. **Target note:** slug `weirwood` — verify this exists. If not, `weirwood-heart-tree` or the closest existing node. See Dedup notes. |
| LB-11 | `leaf` | `MEMBER_OF` | `children-of-the-forest` | 1 | adwd | adwd-bran-03 | 93 | "Though the men of the Seven Kingdoms might call them the children of the forest, Leaf and her people were far from childlike." | Leaf is one of the singers / children of the forest. `leaf.node.md` EXISTS; `children-of-the-forest.node.md` EXISTS (species node). MEMBER_OF (Person → Faction/species) is in vocabulary and wired 31 times. Clean gap. |
| LB-12 | `coldhands` | `REVEALS_TO` | `meera-reed` | 1 | adwd | adwd-bran-01 | 211 | "A friend. Dreamer, wizard, call him what you will. The last greenseer." The longhall's wooden door banged open. | Meera directly asks "Who is this three-eyed crow?" (adwd-bran-01:209) and Coldhands answers "The last greenseer." The revelation is to Meera (the questioner); Bran overhears. This is the first IN-WORLD identification of the three-eyed crow as "the last greenseer." Target = `meera-reed`. What is revealed is the identity of the destination. **See Dedup notes on REVEALS_TO qualifier field.** |
| LB-13 | `brynden-rivers` | `REVEALS_TO` | `meera-reed` | 1 | adwd | adwd-bran-03 | 19 | "When Meera Reed had asked him his true name, he made a ghastly sound that might have been a chuckle. 'I wore many names when I was quick, but even I once had a mother, and the name she gave me at her breast was Brynden.'" | Brynden himself reveals his name to Meera (she asked). This is the explicit in-text identity revelation of the three-eyed crow as Brynden Rivers. The CHARACTER node is `brynden-rivers`; this edge is sourced from him as revealer. Target = `meera-reed`. |
| LB-14 | `wight-ambush` | `SUB_BEAT_OF` | `bran-reaches-the-cave-of-the-three-eyed-crow` | 3 | adwd | adwd-bran-02 | 39 | "The cave is warded. They cannot pass." The ranger used his sword to point. "You can see the entrance there. Halfway up, between the weirwoods, that cleft in the rock." | The wight-ambush event (node exists, 0 outgoing, islanded, minted by Plate 3) is the attack that occurs during the approach to the cave — it is a beat WITHIN `bran-reaches-the-cave-of-the-three-eyed-crow`. SUB_BEAT_OF (beat-in-event scope). Tier 3 (structural). De-islands the orphan without re-minting the fight. |

---

## Edge type assessment — DREAMS_OF vs FORESHADOWS for LB-05

The dream at acok-bran-05:169 is literarily partial: Jojen sees "you and your brother lay dead at his feet" and "skinning off your faces." The textual fulfillment is that *two miller's boys* (not Bran and Rickon) are burned and displayed as if Bran and Rickon. So:
- The dream **comes true** at the societal/reported level (Robb receives the news as real; Bran and Rickon are presumed dead)
- The dream is **subverted** at the literal level (the boys are not Bran and Rickon)

DREAMS_OF (LB-05) is the right primary edge type because it's the character-facing prophetic vision. I have NOT proposed a FORESHADOWS edge for this because the partial subversion makes the reader-facing "detail predicts event" mapping weaker than LB-01/LB-02. The orchestrator may want to add FORESHADOWS if the subversion is considered close enough.

---

## Three-eyed-crow slug trap — assessment

Four edges currently point at `three-eyed-crow` (a **species** node):
- `coldhands SERVES three-eyed-crow`
- `three-eyed-crow TEACHES bran-stark`
- `coldhands SWORN_TO three-eyed-crow`
- `three-eyed-crow HOLDS_TITLE lord`

Lens B's in-scope action: propose LB-12 and LB-13 (the identity revelations) onto `brynden-rivers`, not onto the species node. This gives the graph correct edges even before the species-node retargeting is resolved.

The retargeting itself (modifying the existing four mis-pointed edges) is a structural fix for **Lens D** (or a separate pass), not for Lens B. Flagged here for the orchestrator.

---

## Third eye — two distinct events, not conflated

Per the baseline's instruction: these are distinct.
1. **WARG third eye (acok-bran-07:47):** "Here in the chill damp darkness of the tomb his third eye had finally opened. He could reach Summer whenever he wanted" — this is the warg faculty opening in the crypts during the sack. Already modeled indirectly via the `WARGS_INTO` and `BONDED_TO summer` edges.
2. **GREENSEER third eye (adwd-bran-03:155–169):** the weirwood paste awakens greensight / weirwood-seeing. LB-06 (`bran-stark PRACTICES greensight`) covers this; the `bran-becomes-a-greenseer` event node covers the arc terminus.

No new nodes proposed for these events — the existing event nodes + LB-06 capture the distinction adequately.

---

## Proposed new nodes

**None required.** All target nodes exist:
- `greensight` — `graph/nodes/concepts/greensight.node.md` (confirmed, 0 edges)
- `sack-of-winterfell` — `graph/nodes/events/sack-of-winterfell.node.md` (confirmed)
- `bran-becomes-a-greenseer` — confirmed from spine baseline
- `robb-receives-false-news-of-brans-death` — `graph/nodes/events/robb-receives-false-news-of-brans-death.node.md` (confirmed)
- `children-of-the-forest` — `graph/nodes/species/children-of-the-forest.node.md` (confirmed)
- `leaf` — `graph/nodes/characters/leaf.node.md` (confirmed)
- `meera-reed` — confirmed from baseline
- `wight-ambush` — `graph/nodes/events/wight-ambush.node.md` (confirmed, Plate 3 mint, 0 outgoing)
- `bran-reaches-the-cave-of-the-three-eyed-crow` — confirmed from spine

**LB-10 target confirmed:** `weirwood` = `graph/nodes/species/weirwood.node.md` — verified, slug is exact. No new node needed.

---

## Dedup notes

- **LB-01–LB-05 (`jojen-reed DREAMS_OF/FORESHADOWS ...`):** Zero existing DREAMS_OF edges from `jojen-reed` found in edges.jsonl. Only existing DREAMS_OF edges are `bran-stark DREAMS_OF winterfell` (acok-bran-07) and `jon-snow DREAMS_OF bran-stark` (acok-jon-07). Clean.
- **LB-06 (`bran-stark PRACTICES greensight`):** Zero PRACTICES edges found for bran-stark. Clean.
- **LB-07 (`brynden-rivers PRACTICES greensight`):** Zero PRACTICES edges found for brynden-rivers. Clean.
- **LB-08 (`jojen-reed PRACTICES greensight`):** Zero PRACTICES edges found for jojen-reed. Clean.
- **LB-09 (`brynden-rivers TUTORS bran-stark`):** Existing TUTORS edges for bran-stark are from `eddard-stark`, `luwin`, `jojen-reed`, and one inverse `bran-stark→luwin` (misclassification). None from `brynden-rivers`. Clean.
- **LB-10 (`brynden-rivers BONDED_TO weirwood`):** Only existing BONDED_TO edges for brynden-rivers = none found. Clean. **Target slug must be verified (see above).**
- **LB-11 (`leaf MEMBER_OF children-of-the-forest`):** Existing leaf edges: RESCUES, PROTECTS, AGENT_IN (×2). No MEMBER_OF. Clean.
- **LB-12 (`coldhands REVEALS_TO meera-reed`):** No REVEALS_TO edges found for coldhands. Architecture.md: REVEALS_TO allows optional qualifier — qualifier here = "identity of the three-eyed crow." Clean.
- **LB-13 (`brynden-rivers REVEALS_TO meera-reed`):** No REVEALS_TO edges found for brynden-rivers. Clean. Qualifier = "his true name / Brynden."
- **LB-14 (`wight-ambush SUB_BEAT_OF bran-reaches-the-cave-of-the-three-eyed-crow`):** wight-ambush currently has 4 VICTIM_IN/AGENT_IN edges but 0 outgoing. No existing SUB_BEAT_OF from wight-ambush. Clean.

---

## Harvest pointers

Pointers for a later harvest pass — POINT, don't extract:

- **acok-bran-04:79** — verbatim "winged wolf" green dream; already quoted in LB-03, but also usable as a `## Quotes` entry on `greensight.node.md` and on `bran-stark` node.
- **acok-bran-05:77** — "black waves crashing against the gates and towers" — atmospheric/descriptive language for the sea dream; rich for a node prose upgrade on `sack-of-winterfell`.
- **acok-bran-05:131–133** — Mikken laughs at the sea prophecy ("The gods are good, to take such trouble for a poor smith"), Septon Chayle says he's a strong swimmer; Alebelly alone heeds the warning and is scrubbed raw by guards. Darkly comic hospitality/characterization vignette; load-bearing for all three named drowned men.
- **acok-bran-05:155** — "The things I see in green dreams can't be changed" — Jojen on the immutability of green dreams; key greensight-doctrine quote for `greensight.node.md ## Quotes`.
- **acok-bran-05:181** — "The dream was green, Bran, and the green dreams do not lie." — Second immutability declaration; load-bearing for `greensight.node.md`.
- **adwd-bran-03:89–91** — What the cave party eats: mushrooms, blind white fish (taste as good as fish with eyes once cooked), cheese and goat milk, oats and barleycorn, dried fruit, blood stew thickened with barley and onions and "chunks of meat" (Jojen thinks squirrel, Meera thinks rat). Food/starvation register.
- **adwd-bran-03:93** — Physical description of the children of the forest: nut-brown skin dappled like a deer, large ears, "great golden cat's eyes," three fingers + thumb, sharp black claws instead of nails.
- **adwd-bran-03:119** — "Lord Brynden drew his life from the tree, Leaf told them. He did not eat, he did not drink. He slept, he dreamed, he watched." — Descriptive; candidate for `brynden-rivers` node `## Quotes`.
- **adwd-bran-03:163** — The weirwood paste's taste progression: "It had a bitter taste, though not so bitter as acorn paste... It tasted of honey, of new-fallen snow, of pepper and cinnamon and the last kiss his mother ever gave him." — Food + transformation; `weirwood-paste.node.md` quote candidate.
- **adwd-bran-03:25** — Leaf's age claim: "She claimed to have seen two hundred years." — Characterization/description; `leaf.node.md` note.
- **adwd-bran-03:199** — "Once you have mastered your gifts, you may look where you will and see what the trees have seen" — Brynden's explanation of greensight scope; `greensight.node.md` quote candidate, also `brynden-rivers` node.
- **adwd-bran-01:211** — "A friend. Dreamer, wizard, call him what you will. The last greenseer." — Already in LB-12; also prime for `greensight.node.md ## Quotes` and `brynden-rivers` node.
- **acok-bran-04:207–211** — Maester Luwin's skepticism ("Call it greensight, if you wish … but remember as well all those tens of thousands of dreams … that did not come true. No living man has that power.") — Luwin explicitly names greensight and then denies it. Counter-evidence quote for `greensight.node.md`.
