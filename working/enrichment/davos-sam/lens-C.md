# Lens-C — Causal-Wiring (Davos / Sam residual)

**Lens:** Causal-Wiring (Lens 4)
**Dip:** Davos / Sam residual — A-roundup
**Date:** 2026-06-29
**Status:** PROPOSE ONLY — do not write to edges.jsonl

---

## Proposed Edges

### C-01
| field | value |
|-------|-------|
| id | C-01 |
| edge_type | ENABLES |
| source_slug | `wyman-manderly-stages-fake-execution-of-davos` |
| target_slug | `davos-sent-to-fetch-rickon-from-skagos` |
| book | ADWD |
| evidence_chapter | adwd-davos-04 |
| evidence_ref | `sources/chapters/adwd/adwd-davos-04.md:79` |
| evidence_quote | "It would not do for you to be seen, my lord. You are supposed to be dead." |
| confidence_tier | 1 |
| verify | yes |
| note | The staged death IS the cover story that makes the covert Skagos mission possible. Davos can only travel unseen as a "dead man" — his official death is what grants him the invisibility the mission requires. ENABLES (precondition created by deception). CAUTION: `davos-sent-to-fetch-rickon-from-skagos` does not yet exist as a node; this edge should be minted alongside the new hub. |

---

### C-02
| field | value |
|-------|-------|
| id | C-02 |
| edge_type | PART_OF |
| source_slug | `wyman-manderly-stages-fake-execution-of-davos` |
| target_slug | `grand-northern-conspiracy` |
| book | ADWD |
| evidence_chapter | adwd-davos-04 |
| evidence_ref | `sources/chapters/adwd/adwd-davos-04.md:105` |
| evidence_quote | "The rancor I showed you in the Merman's Court was a mummer's farce put on to please our friends of Frey." |
| confidence_tier | 1 |
| verify | yes |
| note | The staged execution is a discrete sub-operation inside the GNC, not a separate conspiracy. PART_OF (containment). Wyman himself names it "the mummer's farce" — the GNC's watchword — making this near-verbatim tier-1. Check that no PART_OF edges were emitted in the S93 restructure batch described in the node's ## Edges section before minting. |

---

### C-03
| field | value |
|-------|-------|
| id | C-03 |
| edge_type | PART_OF |
| source_slug | `manderly-bakes-the-frey-pies` |
| target_slug | `grand-northern-conspiracy` |
| book | ADWD |
| evidence_chapter | adwd-davos-04 |
| evidence_ref | `sources/chapters/adwd/adwd-davos-04.md:125` |
| evidence_quote | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home." |
| confidence_tier | 2 |
| verify | yes |
| note | The Frey-pies event (at Winterfell feast, later ADWD) is explicitly positioned as part of the same vendetta Wyman describes here. The GNC node's prose already states "the political engine behind the Frey pies." PART_OF (containment; the actual pie event is a GNC action). Cite is from ADWD Davos IV where GNC intent is stated; the minter should add the Winterfell feast chapter as a second evidence_chapter when minting. Tier-2 (the containment is narratively clear but the pie event occurs offstage in a different chapter). |

---

### C-04
| field | value |
|-------|-------|
| id | C-04 |
| edge_type | ENABLES |
| source_slug | `execution-of-davos-lookalike-at-white-harbor` |
| target_slug | `frey-witnesses-attest-davos-dead-at-small-council` |
| book | ADWD |
| evidence_chapter | adwd-davos-04 |
| evidence_ref | `sources/chapters/adwd/adwd-davos-04.md:97` |
| evidence_quote | "Lord Davos, you will not know, but you are dead." |
| confidence_tier | 1 |
| verify | yes |
| note | The displayed head and hands of the lookalike are the physical evidence the Frey witnesses see and later attest to at the small council. Without the substitute beheading, there is nothing physical for them to witness. ENABLES (physical precondition created). Sub-beat to sub-beat causation within the deception; both nodes already exist per the wyman-manderly-stages node description. |

---

### C-05
| field | value |
|-------|-------|
| id | C-05 |
| edge_type | ENABLES |
| source_slug | `frey-witnesses-attest-davos-dead-at-small-council` |
| target_slug | `grand-northern-conspiracy` |
| book | ADWD |
| evidence_chapter | adwd-davos-04 |
| evidence_ref | `sources/chapters/adwd/adwd-davos-04.md:111` |
| evidence_quote | "I did not dare defy King's Landing so long as my last living son remained a captive." |
| confidence_tier | 2 |
| verify | yes |
| note | The attestation causes Cersei to release Wylis Manderly (per AFFC Cersei IV). Releasing Wylis removes the Lannister leverage that was the sole constraint preventing Wyman from acting on the GNC. Prerequisite-state lifted → ENABLES. This is the cross-arc seam that threads the White Harbor deception into the GNC's activation: the deception unlocks the conspiracy. The quote is Wyman's own explanation of the constraint; the AFFC chapter where Cersei acts is the attestation chapter. Orchestrator may want to verify the AFFC Cersei IV attestation chapter exists as evidence_chapter on `frey-witnesses-attest-davos-dead-at-small-council` node. |

---

### C-06
| field | value |
|-------|-------|
| id | C-06 |
| edge_type | MOTIVATES |
| source_slug | `battle-of-the-blackwater` |
| target_slug | `davos-seaworth` |
| book | ASOS |
| evidence_chapter | asos-davos-01 |
| evidence_ref | `sources/chapters/asos/asos-davos-01.md` |
| evidence_quote | "I have a knife... A knife to cut out Melisandre's heart." |
| confidence_tier | 2 |
| verify | yes |
| note | Davos's sons all died in the Blackwater battle (flagship lost in the wildfire). This drives him to return to Dragonstone seeking revenge against Melisandre, which is what puts him in Axell Florent's path and triggers his re-arrest. DISTINCT from the already-built `leeching-of-edric-storm MOTIVATES davos-seaworth` (which covers the Edric smuggling motivation). This edge covers the SEPARATE motivation: Melisandre-grief for sons creates the return-trip that restarts his Dragonstone arc. MOTIVATES (event → character grievance-motive driving a course of action). The built Blackwater→Dragonstone→Wall chain of structural edges already exists; this is a MOTIVATES edge capturing Davos's personal grievance-as-driver, not a structural path edge. |

---

### C-07
| field | value |
|-------|-------|
| id | C-07 |
| edge_type | MOTIVATES |
| source_slug | `leeching-of-edric-storm` |
| target_slug | `death-of-maester-aemon` |
| book | AFFC |
| evidence_chapter | affc-samwell-01 |
| evidence_ref | `sources/chapters/affc/affc-samwell-01.md:217` |
| evidence_quote | "His life will be at risk. I am aware of that, Sam, but the risk is greater here. Stannis knows who Aemon is. If the red woman requires king's blood for her spells . . ." |
| confidence_tier | 1 |
| verify | yes |
| note | Jon explicitly cites the leeching-of-Edric-Storm pattern as the reason the king's blood threat is credible and why Aemon must leave the Wall. The leeching established the precedent that Melisandre uses noble blood for magic — this pattern MOTIVATES Jon's decision to send Aemon south (the journey that ultimately kills him). Near-explicitly stated in text → tier-1. CAUTION: `death-of-maester-aemon` does not yet exist as a node. Minting it is a prerequisite. The evidence_chapter for the node should include AFFC Samwell I (the decision to send him) and AFFC Samwell IV (his death at sea). The quote in AFFC Samwell IV is: "Or else she might have burned him. The red woman. She wanted king's blood for her fires." (Gilly confirming the motive posthumously). |

---

### C-08
| field | value |
|-------|-------|
| id | C-08 |
| edge_type | ENABLES |
| source_slug | `mutiny-at-crasters-keep` |
| target_slug | `jon-elected-lord-commander` |
| book | ASOS |
| evidence_chapter | asos-samwell-02 |
| evidence_ref | `sources/chapters/asos/asos-samwell-02.md:261` |
| evidence_quote | "You must. Must tell them. All. The Fist. The wildlings. Dragonglass. This. All." |
| confidence_tier | 2 |
| verify | yes |
| note | Mormont's murder at Craster's creates the leaderlessness that is the structural precondition for the LC succession crisis. The existing `battle-beneath-the-wall ENABLES jon-elected-lord-commander` edge captures the post-battle external pressure (Stannis threatening to impose a choice). This C-08 edge captures the upstream enabling event: the Watch had no commander BECAUSE Mormont was killed at Craster's. Without Mormont's death, there is no choosing. ENABLES (prerequisite-state removed: the Watch is leaderless). NOTE: Verify that no existing `mutiny-at-crasters-keep ENABLES/CAUSES jon-elected-lord-commander` edge already exists — grep confirmed none as of 2026-06-29. |

---

### C-09
| field | value |
|-------|-------|
| id | C-09 |
| edge_type | ENABLES |
| source_slug | `bran-meets-coldhands` |
| target_slug | `coldhands-rescues-sam-and-gilly` |
| book | ASOS |
| evidence_chapter | asos-samwell-03 |
| evidence_ref | `sources/chapters/asos/asos-samwell-03.md` |
| evidence_quote | "\"Brother!\" the rider called." |
| confidence_tier | 3 |
| verify | yes |
| note | Coldhands addresses Sam as "brother" (Night's Watch term) and rescues him from the wights in the haunted forest. Coldhands is already escorting Bran's party when this occurs. The causal claim: Bran's meeting with Coldhands put Coldhands in the haunted forest where he was positioned to divert and rescue Sam. This is structurally inferential — the texts show both events but don't explicitly connect them — hence tier-3. ENABLES (Bran's meeting brings Coldhands into the region where Sam's rescue becomes possible). CAUTION: `coldhands-rescues-sam-and-gilly` does not yet exist as a node. Minting is a prerequisite. This is a weaker edge than C-01 through C-08 — consider deprioritizing. The Bran arc and Sam arc only brush via Coldhands; this is a structural seam but a thin one. |

---

## DEDUP / CONVERGENCE NOTES

**C-02 vs C-05 vs C-07 (deception-trunk / GNC wiring):**
- C-02 (PART_OF: staged-execution → GNC) = containment; the operation is inside the conspiracy.
- C-05 (ENABLES: frey-witnesses-attest → GNC) = activation; the deception's final step lifts the constraint and activates the conspiracy.
- These are not redundant — they model different structural relationships. Both should be minted. C-07 (MOTIVATES: leeching → death-of-maester-aemon) is a separate arc entirely (Sam/Wall cluster → Aemon's death).
- Orchestrator should check S93 batch description ("Role edges, SUB_BEAT_OF beats, and the CONSPIRES_WITH alliance edge are emitted") to confirm that PART_OF containment edges were NOT already emitted in that batch before minting C-02.

**C-06 vs existing Blackwater → Dragonstone chain:**
- Existing: `battle-of-the-blackwater CAUSES stannis-retreats-to-dragonstone` → `stannis-retreats-to-dragonstone ENABLES stannis-moves-to-the-wall` (structural chain).
- C-06 is a MOTIVATES edge on a DIFFERENT target entity (`davos-seaworth` the character, not a location-move event). It captures grievance-motive, not structural movement. Not a dup.

**C-08 vs existing `battle-beneath-the-wall ENABLES jon-elected-lord-commander`:**
- These are complementary, not redundant. `battle-beneath-the-wall ENABLES` captures the post-battle external pressure (Stannis threatening to force the issue). C-08 captures the upstream leaderlessness: Mormont was already dead from the Craster's mutiny, which is why a new choosing was needed at all. The mutiny predates the battle by several books. Not a dup.

**Sam's election scheme (ENABLES → `jon-elected-lord-commander`):**
- Sam's manipulation of Cotter Pyke and Denys Mallister (ASOS Samwell V) is a real CAUSES/ENABLES causal event but the event hub does not yet exist as a node. Out of scope for this causal-only dip. Flag as build candidate: `sam-schemes-jon-election` → `jon-elected-lord-commander` (CAUSES tier-1, near-explicitly stated). Very high value; mint when building the LC election cluster more fully.

**C-09 (Bran meets Coldhands ENABLES Coldhands rescues Sam):**
- Weaker than other proposals (tier-3, two missing node hubs). Deprioritize unless building out the Coldhands character cluster specifically.

---

## DUP-FLAG

`battle-of-the-fist-of-the-first-men` (0-edge node) confirmed at:
`/Users/mnoth/source/asoiaf-chat/graph/nodes/events/battle-of-the-fist-of-the-first-men.node.md`

Canonical node with all edges is `fight-at-the-fist`. The dup node carries no edges and should be merged/redirected. Recommend: add `battle-of-the-fist-of-the-first-men` as an alias on `fight-at-the-fist.node.md`, then delete (or tombstone) the dup node file.

---

## HARVEST

Items found while reading chapter files — point, don't extract; a later harvest pass attaches:

| kind | book | ref | note |
|------|------|-----|-------|
| quote (load-bearing) | ADWD | adwd-davos-04:79 | "It would not do for you to be seen, my lord. You are supposed to be dead." — Glover to Davos; anchor quote for the cover-story / fake-death |
| food / hospitality | ADWD | adwd-davos-04:93 | Wyman's feast in Merman's Court: "lamprey pie and venison with roasted chestnuts" — the decoy feast staged while Davos is brought in secretly |
| hospitality (sinister) | ADWD | adwd-davos-04:45 | "I shall present each of them with a palfrey as a guest gift" — Wyman to Frey companions; palfreys as cover for later disappearances (sinister hospitality inversion) |
| appearance | ASOS | asos-samwell-03 | Coldhands on elk: "A man muffled head to heels in mottled blacks and greys sat astride an elk... The elk was huge, a great elk, ten feet tall at the shoulder, with a rack of antlers near as wide." |
| quote (dragonglass) | ASOS | asos-samwell-01 | Other melting: "In twenty heartbeats its flesh was gone, swirling away in a fine white mist. Beneath were bones like milkglass, pale and shiny, and they were melting too." |
| foreshadowing (Aemon + Dany) | AFFC | affc-samwell-04:21 | Aemon's dying clarity: "No one ever looked for a girl... The language misled us all for a thousand years. Daenerys is the one, born amidst salt and smoke." — load-bearing prophecy quote, attach to Aemon node |
| oath / witness | ASOS | asos-samwell-04:85 | Sam's oath to Coldhands: "Swear it, Samwell of the Night's Watch. Swear it for the life you owe me." — Coldhands extracting secrecy about Bran |
| food / atmosphere | ASOS | asos-samwell-02:261 | Craster's farewell feast: "horsemeat dripped with grease as Craster's wives turned the spits" — last meal before mutiny |

---

## Build Candidates (new hubs needed before these edges can be minted)

1. **`davos-sent-to-fetch-rickon-from-skagos`** — for C-01. Evidence: ADWD Davos IV (the mission assignment scene). Hub description: Wyman's commission to Davos to smuggle Rickon Stark home from Skagos as proof of a surviving Stark heir.
2. **`death-of-maester-aemon`** — for C-07. Evidence chapters: AFFC Samwell I (decision to send him), AFFC Samwell IV (death at sea). Hub description: Aemon's death during the voyage to Oldtown, driven south by Jon's fear of the king's-blood threat.
3. **`sam-schemes-jon-election`** (out-of-scope flag) — ASOS Samwell V. Very high value causal event; mint before or alongside any further LC-election enrichment.
4. **`coldhands-rescues-sam-and-gilly`** — for C-09 (deprioritized). ASOS Samwell III.
