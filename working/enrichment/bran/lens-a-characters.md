# Bran / greenseer arc enrichment — Lens A: Secondary-character sub-arcs (S146)

> **PROPOSE, don't mint.** All edges below are proposals for orchestrator synthesis, line-check,
> and fresh-verify. Nothing here goes straight to the graph.

---

## Proposed edges

### MEERA REED — protector / carrier / companion

**A-01** Missing: `meera-reed TRAVELS_WITH bran-stark`
| field | value |
|-------|-------|
| source | `meera-reed` |
| edge | `TRAVELS_WITH` |
| target | `bran-stark` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-01.md` |
| line | ~21 |
| quote | "Behind the ranger, Meera Reed wrapped her arms around her brother, to shelter him from the wind and cold with the warmth of her own body." |
| note | Jojen already has `TRAVELS_WITH bran-stark` (acok-bran-07:119). Meera does NOT — gap confirmed by dedup check. She is the physical escort of the whole journey north of the Wall, carrying Jojen and guarding Bran. This edge is clean and missing. |

**A-02** Missing: `meera-reed RESCUES bran-stark` (wight-fight, adwd-bran-02)
| field | value |
|-------|-------|
| source | `meera-reed` |
| edge | `RESCUES` |
| target | `bran-stark` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-02.md` |
| line | 113 |
| quote | "Meera Reed was there, driving her frog spear deep into the wight's back." |
| note | Meera already has `PROTECTS bran-stark` (general protective relationship, acok). This is a distinct rescue event — she drives off the wight that was reaching for Bran during the wight-ambush. `RESCUES` is in the canonical vocab (unpopulated, high-value). Distinct from PROTECTS. Dedup: no `meera-reed RESCUES bran-stark` edge exists. |

**A-03** Propose: `meera-reed AGENT_IN wight-ambush`
| field | value |
|-------|-------|
| source | `meera-reed` |
| edge | `AGENT_IN` |
| target | `wight-ambush` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-02.md` |
| line | 113 |
| quote | "Meera Reed was there, driving her frog spear deep into the wight's back." |
| note | Meera is a VICTIM_IN wight-ambush (existing) but also an active AGENT (she fights back with her frog spear and burns wights with the torch). The agent-vs-victim distinction matters. Dedup: no `meera-reed AGENT_IN wight-ambush` edge exists. Leaf has the AGENT_IN (torch), Coldhands has the AGENT_IN (sword); Meera fought too. |

---

### HODOR — warg-in-combat (adwd-bran-02 fight; distinct from existing asos-bran-03 edge)

**A-04** Propose: `bran-stark WARGS_INTO hodor` — second instance, cave-approach wight fight
| field | value |
|-------|-------|
| source | `bran-stark` |
| edge | `WARGS_INTO` |
| target | `hodor` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-02.md` |
| line | 111 |
| quote | "And suddenly he was not Bran, the broken boy crawling through the snow, suddenly he was Hodor halfway down the hill, with the wight raking at his eyes." |
| note | The EXISTING `bran-stark WARGS_INTO hodor` edge cites `asos-bran-03:23` (the weirwood-pool scene). The adwd-bran-02 wight-fight warging is a *separate, higher-stakes* instance where Bran seizes Hodor in combat to save him and fight the wights — a crucial escalation showing Bran's growing power and willingness to subvert Hodor's will under duress. The graph currently anchors this edge only at the asos scene. Dedup check: only one `bran-stark WARGS_INTO hodor` instance exists, citing asos-bran-03:23. This does NOT duplicate it; it adds the adwd combat instance as a second edge on the same source→target pair, with a distinct cite_ref. Orchestrator should decide whether to add a second instance or to upgrade the existing edge with an additional cite_ref — either is defensible. |

**A-05** Propose: `hodor SERVES bran-stark` (adwd cave navigation — confirms and extends)
| field | value |
|-------|-------|
| source | `hodor` |
| edge | `SERVES` |
| target | `bran-stark` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 205 |
| quote | "Hodor carried Bran back to his chamber, muttering 'Hodor' in a low voice as Leaf went before them with a torch." |
| note | `hodor SERVES bran-stark` already EXISTS (cited agot-bran-02:21). This would be a second instance with a cave-specific cite. Defer to orchestrator — may not need a second cite_ref if the existing one covers the relationship adequately. Lower priority than A-01–A-04. Flag rather than push. |

---

### OSHA — the split and Rickon escort

**A-06** Propose: `osha TRAVELS_WITH rickon-stark`
| field | value |
|-------|-------|
| source | `osha` |
| edge | `TRAVELS_WITH` |
| target | `rickon-stark` |
| tier | 1 |
| book | ACOK |
| chapter-file | `acok-bran-07.md` |
| line | 191 |
| quote | "I will take Rickon with me." |
| note | Osha already has `PROTECTS rickon-stark` (existing) but NO `TRAVELS_WITH rickon-stark`. After the split she becomes Rickon's sole escort, traveling with him. Dedup: no `osha TRAVELS_WITH rickon-stark` exists. Clean gap. |

**A-07** Propose: `osha RESCUES bran-stark` (crypt survival, acok-bran-07)
| field | value |
|-------|-------|
| source | `osha` |
| edge | `RESCUES` |
| target | `bran-stark` |
| tier | 2 |
| book | ACOK |
| chapter-file | `acok-bran-07.md` |
| line | 99 |
| quote | "I'll grope my way up." |
| note | Osha has `AGENT_IN bran-and-rickon-survive-the-sack-in-the-crypts` and `ENABLES` that event. The RESCUES type captures that she personally extracted Bran from the crypt (she goes up first to check safety, then leads the group out). `RESCUES` is stronger than the existing general PROTECTS edge. However, Osha's existing AGENT_IN + ENABLES on the crypt event may already cover this sufficiently — orchestrator should judge whether adding RESCUES adds graph value or is redundant. Flagging as Tier 2 (implied by her ENABLES role, not a verbatim rescue-quote). |

---

### JOJEN REED — green dreams (baseline gap #1)

**A-08** Propose: `jojen-reed DREAMS_OF sack-of-winterfell`
| field | value |
|-------|-------|
| source | `jojen-reed` |
| edge | `DREAMS_OF` |
| target | `sack-of-winterfell` |
| tier | 1 |
| book | ACOK |
| chapter-file | `acok-bran-05.md` |
| line | 77–81 |
| quote | "It is the sea that comes. I dreamed that the sea was lapping all around Winterfell. I saw black waves crashing against the gates and towers, and then the salt water came flowing over the walls and filled the castle. Drowned men were floating in the yard. When I first dreamed the dream, back at Greywater, I didn't know their faces, but now I do. That Alebelly is one, the guard who called our names at the feast. Your septon's another. Your smith as well." |
| note | Jojen's "sea" green dream is the ironborn sack of Winterfell. The named drowned men (Alebelly, Septon Chayle, Mikken) all die in the sack. This is a BRAN↔WO5K cross-container seam: the "sea" = ironborn. DREAMS_OF is canonical (Prophecy category, unpopulated). Dedup: no `jojen-reed DREAMS_OF sack-of-winterfell` edge exists. |

**A-09** Propose: `jojen-reed DREAMS_OF bran-becomes-a-greenseer`
| field | value |
|-------|-------|
| source | `jojen-reed` |
| edge | `DREAMS_OF` |
| target | `bran-becomes-a-greenseer` |
| tier | 1 |
| book | ACOK |
| chapter-file | `acok-bran-05.md` |
| line | 113 |
| quote | "You are the winged wolf, but you will never fly. Unless you open your eye." |
| note | The "winged wolf bound with grey stone chains, a crow pecking through" dream (referenced in baseline at acok-bran-04:79/93) is the direct foretelling of bran-becomes-a-greenseer. The above quote is Jojen interpreting his own green dream imagery to Bran. The baseline confirms this edge as a target (gap #1). Orchestrator should also check acok-bran-04:79 for the verbatim dream description to attach as second cite. Dedup: no such edge exists. |

**A-10** Propose: `jojen-reed FORESHADOWS robb-receives-false-news-of-brans-death` (via Reek dream)
| field | value |
|-------|-------|
| source | `jojen-reed` |
| edge | `FORESHADOWS` |
| target | `robb-receives-false-news-of-brans-death` |
| tier | 1 |
| book | ACOK |
| chapter-file | `acok-bran-05.md` |
| line | 169 |
| quote | "I dreamed of the man who came today, the one they call Reek. You and your brother lay dead at his feet, and he was skinning off your faces with a long red blade." |
| note | This dream directly foreshadows the miller's-boys deception — Reek (Ramsay) skins the faces of two boys and presents them as Bran and Rickon, causing the false-news event. FORESHADOWS (Narrative & Literary, unpopulated) fits better than DREAMS_OF here because the dream's subject is not the target event directly but rather an action that foreshadows it. **VERIFY** target slug exists before minting — check `find graph/nodes -name "*false-news*"`. If the slug doesn't exist, use `DREAMS_OF jojen-reed` pointing at the Reek/ramsay event that actually happened, or flag for slug lookup. |

---

### JOJEN REED — REVEALS_TO / cross-arc seam

**A-11** Propose: `jojen-reed REVEALS_TO bran-stark` (warg identity)
| field | value |
|-------|-------|
| source | `jojen-reed` |
| edge | `REVEALS_TO` |
| target | `bran-stark` |
| tier | 1 |
| book | ACOK |
| chapter-file | `acok-bran-05.md` |
| line | 97 |
| quote | "Warg," said Jojen Reed." |
| note | Jojen names Bran as a warg — this is a revelation that fundamentally changes how Bran understands himself. REVEALS_TO (Knowledge & Information, unpopulated) captures the information-transfer aspect that TUTORS doesn't; this is a single disclosure, not a curriculum. Dedup: no `jojen-reed REVEALS_TO bran-stark` edge exists. `jojen-reed TUTORS bran-stark` already exists but cites the later training scene (acok-bran-05:127). This is the earlier naming moment. |

---

### BLOODRAVEN — textual mentorship (cave only)

**A-12** Propose: `brynden-rivers TUTORS bran-stark`
| field | value |
|-------|-------|
| source | `brynden-rivers` |
| edge | `TUTORS` |
| target | `bran-stark` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 51–52 |
| quote | "A wild stallion will buck and kick when a man tries to mount him, and try to bite the hand that slips the bit between his teeth," Lord Brynden said, "but a horse that has known one rider will accept another. Young or old, these birds have all been ridden. Choose one now, and fly." |
| note | Brynden-Rivers teaches Bran to slip into the ravens and through the weirwood net — distinct from Jojen's TUTORS (which covers warg/third-eye coaching in ACOK). TUTORS is canonical (Knowledge & Information, unpopulated). Dedup: no `brynden-rivers TUTORS bran-stark` edge exists; the existing `brynden-rivers AGENT_IN bran-becomes-a-greenseer` captures his presence at the terminus but not the months of mentorship leading to it. |

**A-13** Propose: `brynden-rivers BONDED_TO weirwood`
| field | value |
|-------|-------|
| source | `brynden-rivers` |
| edge | `BONDED_TO` |
| target | `weirwood` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 119 |
| quote | "Lord Brynden drew his life from the tree, Leaf told them. He did not eat, he did not drink. He slept, he dreamed, he watched." |
| note | Brynden is physically merged with the weirwood throne — he draws literal sustenance from the tree. BONDED_TO (Magic & Supernatural, unpopulated) captures the organic/mystical union, not mere sitting. Dedup: no `brynden-rivers BONDED_TO weirwood` exists. **Verify `weirwood` slug** — check `find graph/nodes -name "weirwood.node.md"` before minting. If only `weirwood-tree` exists, adjust target slug. |

---

### LEAF & THE CHILDREN OF THE FOREST

**A-14** Propose: `leaf MEMBER_OF children-of-the-forest`
| field | value |
|-------|-------|
| source | `leaf` |
| edge | `MEMBER_OF` |
| target | `children-of-the-forest` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-02.md` |
| line | 135–141 |
| quote | "The First Men named us children," the little woman said. "The giants called us woh dak nag gran, the squirrel people, because we were small and quick and fond of trees, but we are no squirrels, no children. Our name in the True Tongue means those who sing the song of earth." |
| note | Baseline explicitly flags `leaf MEMBER_OF children-of-the-forest` as missing. `children-of-the-forest` exists as a species node (confirmed by `find`). Dedup: no `leaf MEMBER_OF children-of-the-forest` edge exists. Clean. |

**A-15** Propose: `leaf TEACHES bran-stark` (explains singers/greenseer cosmology in cave)
| field | value |
|-------|-------|
| source | `leaf` |
| edge | `TEACHES` |
| target | `bran-stark` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 25 |
| quote | "Most of him has gone into the tree," explained the singer Meera called Leaf. "He has lived beyond his mortal span, and yet he lingers. For us, for you, for the realms of men. Only a little strength remains in his flesh. He has a thousand eyes and one, but there is much to watch. One day you will know." |
| note | Leaf explains Brynden's condition and the nature of greenseers to Bran. She also administers the weirwood paste, warns about going into the deep passages, and answers Bran's questions about the children. TEACHES (Knowledge & Information, populated, 3 instances) fits: she is the primary informant on the children's nature and cave cosmology. Distinct from Brynden's TUTORS (magic training). Dedup: no `leaf TEACHES bran-stark` edge exists. |

---

### GREENSIGHT CONCEPT — lighting the dead node

**A-16** Propose: `bran-stark PRACTICES greensight`
| field | value |
|-------|-------|
| source | `bran-stark` |
| edge | `PRACTICES` |
| target | `greensight` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 69 |
| quote | "Only one man in a thousand is born a skinchanger," Lord Brynden said one day, after Bran had learned to fly, "and only one skinchanger in a thousand can be a greenseer." |
| note | Greensight node exists (confirmed) with 0 edges — completely isolated. This is its highest-value incoming wire. PRACTICES (Magic & Supernatural, unpopulated) is the right type for Character→Magic discipline. Bran is confirmed as a greenseer by Brynden's teaching. Dedup: no edges on `greensight` at all. |

**A-17** Propose: `brynden-rivers PRACTICES greensight`
| field | value |
|-------|-------|
| source | `brynden-rivers` |
| edge | `PRACTICES` |
| target | `greensight` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-03.md` |
| line | 19 |
| quote | "The last greenseer, the singers called him, but in Bran's dreams he was still a three-eyed crow." |
| note | Brynden is explicitly "the last greenseer" — the singers' own name for him. PRACTICES greensight is the graph connection. Dedup: no `brynden-rivers PRACTICES greensight` edge exists. Clean. |

---

### WIGHT-AMBUSH STRUCTURAL FIX (baseline gap #6)

**A-18** Propose: `wight-ambush SUB_BEAT_OF bran-reaches-the-cave-of-the-three-eyed-crow`
| field | value |
|-------|-------|
| source | `wight-ambush` |
| edge | `SUB_BEAT_OF` |
| target | `bran-reaches-the-cave-of-the-three-eyed-crow` |
| tier | 1 |
| book | ADWD |
| chapter-file | `adwd-bran-02.md` |
| line | 91 (approximate) |
| quote | "All around him, wights were rising from beneath the snow." |
| note | Baseline explicitly flags `wight-ambush` as a 0-outgoing orphan that IS the cave-approach fight, duplicating what's already encoded on `bran-reaches-the-cave…`. SUB_BEAT_OF (Military & Conflict, 1 existing instance) de-islands it cleanly. Dedup: `wight-ambush` has 0 outgoing edges (confirmed). This adds its sole outgoing edge. |

---

### SLUG TRAP FLAG — Coldhands SERVES/SWORN_TO mis-pointing

**A-FLAG-01** (NOT AN EDGE PROPOSAL — structural alert for Lens D and orchestrator)

The baseline flagged this and it is confirmed live:
- `coldhands SERVES three-eyed-crow` (exists — pointing at `three-eyed-crow` SPECIES node)
- `coldhands SWORN_TO three-eyed-crow` (exists — same bad target)

The correct target is `brynden-rivers`. The quote anchoring both is `adwd-bran-01.md:73`: "The ranger saved Sam and the girl from the wights… and he's taking me to the three-eyed crow." The character identity Bloodraven = `brynden-rivers` is established at adwd-bran-03:19.

**Recommend:** Orchestrator/Lens D proposes retargeting these two edges from `three-eyed-crow` → `brynden-rivers`. This is a SAME_AS-adjacent call (higher stakes) but the textual link is unambiguous — Brynden is the three-eyed crow in the text ("the greenseer," "Lord Brynden said"). Do NOT propose SAME_AS here; propose edge retargeting only.

Similarly: `three-eyed-crow TEACHES bran-stark` (if it exists) should be retargeted → `brynden-rivers TUTORS bran-stark` (overlaps with A-12 above). Orchestrator should check this edge.

---

## Proposed new nodes

**None.** All targets referenced above already exist in the graph. I considered proposing a `weirwood-net` or `cave-of-the-three-eyed-crow` node for A-13, but `weirwood` is likely already a node (needs slug verification), and the cave is already encoded as the event `bran-reaches-the-cave-of-the-three-eyed-crow`. Leaf already has a node. Children-of-the-forest already exist as a species node.

---

## Dedup notes

Checked via `python3 scripts/graph-query.py --neighbors <slug>` for each of:

- `meera-reed` (11 out / 8 in): NO `TRAVELS_WITH bran-stark`, NO `RESCUES bran-stark`, NO `AGENT_IN wight-ambush` → gaps confirmed (A-01, A-02, A-03)
- `bran-stark` outgoing: HAS `WARGS_INTO hodor` (1 instance only, citing asos-bran-03:23); the adwd-bran-02 combat warg is unrepresented (A-04)
- `hodor` (10 out / 6 in): HAS `SERVES bran-stark`, `COMPANION_OF bran-stark`; VICTIM_IN wight-ambush ✓; no WARGS_INTO (those are on bran-stark outgoing) — A-05 would be duplicate on SERVES, flagged as low-priority
- `osha` (22 out): HAS `PROTECTS rickon-stark`, `AGENT_IN bran-and-rickon-survive-the-sack`, `ENABLES` crypt event; NO `TRAVELS_WITH rickon-stark` → gap (A-06); RESCUES = Tier 2 redundancy-flag (A-07)
- `jojen-reed` (19 out): NO `DREAMS_OF` anything; NO `FORESHADOWS`; NO `REVEALS_TO` → gaps confirmed (A-08, A-09, A-10, A-11)
- `brynden-rivers` (15 out): NO `TUTORS`; NO `BONDED_TO`; NO `PRACTICES` → gaps confirmed (A-12, A-13, A-17)
- `leaf` (4 out): NO `MEMBER_OF`; NO `TEACHES` → gaps confirmed (A-14, A-15)
- `greensight` (0 out, 0 in): COMPLETELY ISOLATED → gaps A-16, A-17
- `wight-ambush` (0 out): ORPHANED → gap A-18
- `children-of-the-forest` node: EXISTS at `/Users/mnoth/source/asoiaf-chat/graph/nodes/species/children-of-the-forest.node.md` ✓
- `wight-ambush` node: EXISTS at `/Users/mnoth/source/asoiaf-chat/graph/nodes/events/wight-ambush.node.md` ✓
- Coldhands SERVES/SWORN_TO `three-eyed-crow` slug trap: CONFIRMED LIVE — both edges point at the species node, not `brynden-rivers`

Edges I confirmed ALREADY EXIST (did not re-propose):
- `jojen-reed TUTORS bran-stark` ✓
- `jojen-reed PROTECTS bran-stark` ✓
- `jojen-reed TRAVELS_WITH bran-stark` ✓
- `meera-reed PROTECTS bran-stark` ✓
- `osha PROTECTS bran-stark` ✓, `osha PROTECTS rickon-stark` ✓
- `bran-stark WARGS_INTO summer` ✓, `bran-stark WARGS_INTO hodor` ✓ (asos cite)
- `leaf PROTECTS bran-stark` ✓, `leaf RESCUES bran-stark` ✓, `leaf AGENT_IN bran-becomes-a-greenseer` ✓
- `brynden-rivers MOTIVATES bran-s-coma-and-the-three-eyed-crow` ✓
- `bran-stark SEEKS brynden-rivers` ✓
- `old-nan TEACHES bran-stark` ✓ (existing; did not re-propose)
- `hodor FEARS crypt-of-winterfell` ✓

---

## Harvest pointers

Reading the Bran chapters for this lens, the following are notable-but-not-task finds:

1. `adwd-bran-03.md:89` / **food** / Cave subsistence diet described: "A hundred kinds of mushrooms grew down here. Blind white fish swam in the black river … They had cheese and milk from the goats that shared the caves with the singers, even some oats and barleycorn and dried fruit … almost every day they ate blood stew, thickened with barley and onions and chunks of meat. Jojen thought it might be squirrel meat, and Meera said that it was rat. Bran did not care. It was meat and it was good."

2. `adwd-bran-03.md:163` / **food + ritual** / Weirwood paste ingestion described: "It had a bitter taste, though not so bitter as acorn paste … The rest he spooned up eagerly. Why had he thought that it was bitter? It tasted of honey, of new-fallen snow, of pepper and cinnamon and the last kiss his mother ever gave him." ← load-bearing sensory description; ties to `weirwood-paste` node in foods/

3. `adwd-bran-02.md:65` / **food + starvation + hospitality (grim register)** / Elk as final food source: "It had been twelve days since the elk had collapsed for the third and final time, since Coldhands had knelt beside it in the snowbank and murmured a blessing in some strange tongue as he slit its throat. Bran wept like a little girl when the bright blood came rushing out … he'd eaten twice, once in his own skin and once in Summer's." ← starvation + Bran eating as a wolf; also Coldhands' strange ritual blessing

4. `adwd-bran-02.md:141–149` / **physical description** / Leaf's first description: "It was a girl, but smaller than Arya, her skin dappled like a doe's beneath a cloak of leaves. Her eyes were queer—large and liquid, gold and green, slitted like a cat's eyes … Her hair was a tangle of brown and red and gold, autumn colors, with vines and twigs and withered flowers woven through it." ← first appearance description of a child of the forest; should attach to Leaf node

5. `adwd-bran-02.md:191–195` / **physical description** / Brynden Rivers' first in-person description: "Before them a pale lord in ebon finery sat dreaming in a tangled nest of roots, a woven weirwood throne that embraced his withered limbs as a mother does a child … What skin the corpse lord showed was white, save for a bloody blotch that crept up his neck onto his cheek … A spray of dark red leaves sprouted from his skull, and grey mushrooms spotted his brow." ← vivid physical description; should attach to brynden-rivers node

6. `adwd-bran-03.md:93–99` / **physical description** / Extended description of children of the forest species: "They were small compared to men, as a wolf is smaller than a direwolf … They had nut-brown skin, dappled like a deer's with paler spots, and large ears that could hear things that no man could hear … Their hands had only three fingers and a thumb, with sharp black claws instead of nails." ← species physical description; attach to children-of-the-forest node

7. `acok-bran-07.md:147` / **hospitality / guest-right (inverted — the dead gods)** / Luwin dying under the heart tree: "On the edge of the black pool, beneath the shelter of the heart tree, Maester Luwin lay on his belly in the dirt." ← Luwin dies in the godswood as a kind of sacred hospitality of the old gods; Osha performs mercy (implied); notable hospitality/guest-right adjacency — the godswood as sanctuary

8. `adwd-bran-01.md:71–72` / **foreshadowing / Old Nan lore** / Old Nan's tales recalled beyond the Wall: "Bran found himself remembering the tales Old Nan had told him when he was a babe. Beyond the Wall the monsters live, the giants and the ghouls, the stalking shadows and the dead that walk, she would say … but they cannot pass so long as the Wall stands strong and the men of the Night's Watch are true." ← Old Nan's lore proven true; strong foreshadowing of TWOW Others threat; cite to Old Nan node

9. `acok-bran-05.md:77–81` / **foreshadowing** / Jojen's sea dream naming Alebelly, Septon Chayle, Mikken — all of whom die in the sack of Winterfell → already proposed as A-08, but note the NAMED drowned men are a harvest find: three minor characters whose deaths are foreseen by name before the event; rich text for the sack-of-winterfell node
