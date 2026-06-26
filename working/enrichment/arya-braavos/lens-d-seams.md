# Lens D: Arya Braavos — Existing-Node↔Existing-Node Causal Seams

Generated: 2026-06-26
Session: D&E or graph enrichment (Lens D run)
Lens scope: `arya-stark` Braavos / HoBaW arc (ASOS 75, AFFC Arya I–II, AFFC Cat of the Canals, ADWD Blind Girl, ADWD Ugly Little Girl) + Sam II–III for Dareon stranding.

---

## SEAM 1 — Iron Coin / Harrenhal → Braavos Departure (STRONGEST)

**Edge:** `jaqen-hghar ENABLES departure-to-braavos`
*(or, if a departure node doesn't exist: `jaqen-hghar ENABLES arya-stark` — see NOTE below)*

**Tier:** 1

**chapter:line:** `sources/chapters/acok/acok-arya-09.md:339`

**Verbatim quote:**
> "If the day comes when you would find me again, give that coin to any man from Braavos, and say these words to him—valar morghulis."

**Departure confirmation** (the coin is the direct mechanism):
`sources/chapters/asos/asos-arya-13.md:255`
> "It's not silver." Her fingers closed on it. "It's iron. Here." She pressed it into his hand, the small black iron coin that Jaqen H'ghar had given her, so worn the man whose head it bore had no features.

`sources/chapters/asos/asos-arya-13.md:259–261`
> "Valar morghulis," she said, as loud as if she'd known what it meant. "Valar dohaeris," he replied, touching his brow with two fingers. "Of course you shall have a cabin."

**Arcs joined:** Harrenhal / ACOK Arya arc (Jaqen/three-deaths cluster) → Braavos / HoBaW arc.

**Rationale:** The iron coin is the literal precondition that unlocks Arya's sea passage from Saltpans. Without the Harrenhal gift, Arya has no money (she sold Craven for a pittance; she explicitly lacked silver) and no cultural key. The TEACHES edge `jaqen-hghar → arya-stark` (graph confirmed, acok-arya-09:339) encodes the coin-gift. The causal chain is: Jaqen gifts coin (Harrenhal) → coin preconditions the captain's offer of passage (ASOS 13) → Arya arrives in Braavos (AFFC Arya I). This is the structural spine wiring the two arcs. The edge should originate from `jaqen-hghar` as agent, not from an event node (no departure event node exists yet in the graph; the spine lens would mint it).

**NOTE on target:** No "departure to Braavos" or "arya arrives in braavos" event node confirmed in graph. Propose the edge with target `arya-stark` using type ENABLES if no event node; or flag for spine lens to mint `departure-to-braavos` first. The existing TEACHES edge captures the coin-gift; this ENABLES edge captures the *forward consequence* — they are complementary, not duplicate.

---

## SEAM 2 — Dareon's Desertion ENABLES Sam's Stranding (STRONG)

**Edge:** `dareon ENABLES maester-aemon-dies-in-braavos`
*(or closest existing node: `dareon ENABLES samwell-tarly` — see NOTE)*

**Tier:** 1

**chapter:line:** `sources/chapters/affc/affc-samwell-03.md:193`

**Verbatim quote:**
> "Coin that might have bought us food, Sam thought, coin that might have bought wood, so Maester Aemon could keep warm."

**Supporting quote** (Dareon announces desertion):
`sources/chapters/affc/affc-samwell-03.md:219`
> "I'm done with black." Dareon tore his cloak off his naked bride and tossed it in Sam's face.

**Arcs joined:** Night's Watch / Oldtown arc (Sam-Aemon-Dareon journey) → Braavos / HoBaW arc (Cat's parallel existence in same city).

**Rationale:** Dareon's desertion is the direct cause of Sam's group being stranded without passage money in Braavos. The Dareon node already has `BETRAYS → nights-watch` (affc-samwell-03:219, graph confirmed). The new seam is the downstream consequence: Dareon spending the group's silver on whores and wine rather than wood/food meant Aemon could not keep warm. Sam explicitly connects Dareon's spending to Aemon's deteriorating condition (sam-03:193). The passive murder-by-neglect framing makes `ENABLES` the correct type (Dareon's choices precondition Aemon's weakening). `MOTIVATES` would need a character target and does not fit.

**NOTE on "Dareon held the money":** The prompt's briefing said "Dareon held their coin." The text is more nuanced: Sam says it was "the last of their silver" that went to the healer (sam-03:43) and Dareon boasted "I still have coin enough" at the Happy Port (sam-03:191 — his own singing money). The group had one shared supply; Dareon did NOT embezzle a separate purse he held. The causal mechanism is Dareon *not contributing* his singing earnings plus deserting before buying the promised wood and food, not a literal "Dareon held and spent their specific purse." Edge should not claim he "held their coin" — the mechanism is his abandonment.

---

## SEAM 3 — Dareon's Desertion MOTIVATES Arya's Execution of Him (STRONG)

**Edge:** `dareon MOTIVATES arya-stark`
*(specifically: Ned Stark's justice ethos — deserters die — MOTIVATES Arya to kill Dareon)*

**Tier:** 1

**chapter:line:** `sources/chapters/affc/affc-cat-of-the-canals-01.md:142`

**Verbatim quote:**
> "He is a man of the Night's Watch," she thought, as he sang about some stupid lady throwing herself off some stupid tower because her stupid prince was dead. "The singer should be on the Wall."

**Execution confirmation:**
`sources/chapters/adwd/adwd-the-blind-girl-01.md:141`
> "Dareon had been a deserter from the Night's Watch; he had deserved to die."

**Arcs joined:** Ned Stark / justice arc (Ned's ethic: a lord rides when he pronounces the sentence) → Braavos / HoBaW arc.

**Rationale:** Arya's interior voice in `adwd-blind-girl-01:141` explicitly cites his desertion as the moral justification ("he had deserved to die"). This is the same Stark ethic that Ned modeled in AGOT — the lord who passes the sentence swings the sword. The Dareon node already has `BETRAYS → nights-watch`. The missing seam is `dareon MOTIVATES arya-stark` (his desertion activates the Stark-justice reflex that drives her to kill him). `MOTIVATES` is correct (arya-stark is a character).

**Additional sub-edge (also MINT-WORTHY):**
`arya-stark EXECUTES dareon` — graph shows `arya-stark KILLS dareon` at `adwd-blind-girl-01:141`. A richer framing is EXECUTES (she acts as executioner for a crime, not simple homicidal violence). Check if EXECUTES is in locked vocab — YES it is. Propose **upgrade**: change `KILLS` to `EXECUTES` with the same cite, adding note that the FM kindly man subsequently punishes her precisely because she *judged* rather than killed on FM assignment.

---

## SEAM 4 — Lysa-Death News Reaches Cat (WEAK — prefer HARVEST)

**Proposed edge (if forced):** `death-of-lysa-arryn REVEALS_TO arya-stark`

**Tier:** 2

**chapter:line:** `sources/chapters/affc/affc-cat-of-the-canals-01.md:113–115`

**Verbatim quote:**
> "Lady Lysa," she said, "is she . . . ?" ". . . dead?" finished the freckled boy whose head was full of courtesans. "Aye. Murdered by her own singer."

**Arcs joined:** Vale / Lysa arc (`death-of-lysa-arryn`, `marillion` the framed singer) → Braavos / HoBaW arc.

**VERDICT: WEAK — prefer HARVEST, not a causal edge.**

**Reasoning:** This is an overheard rumor from Gulltown sailors, received by Cat who is actively suppressing her Stark identity ("It's nought to me. Cat of the Canals never had an aunt."). No causal consequence flows from this: Cat does not act, does not tell anyone, does not change behavior. The "Murdered by her own singer" detail resonates with the Sansa/Vale arc (Marillion was framed) but that connection exists in `death-of-lysa-arryn`'s own node, not in Cat's reaction. `REVEALS_TO` technically fits the grammar (news reaches Cat) but the edge would be purely informational with zero downstream causal weight on either arc. The most honest encoding is:

**Harvest pointer:** `affc-cat-of-the-canals-01.md:113–115 / dramatic-irony / Cat overhears that Lysa Arryn was "murdered by her own singer" — Sansa's two sisters unknowingly share Braavosi airspace at this moment (Sansa in the Vale scheming with Littlefinger; Cat on the docks); neither knows the other is alive.`

The dramatic irony (two Stark sisters orbiting the same truth from opposite arcs) is high value as a **thematic note**, not a causal edge. A later analytical pass or foreshadowing lens owns it.

---

## SEAM 5 — Hardhome Slaves News Reaches Blind Beth (WEAK — prefer HARVEST)

**Proposed edge (if forced):** `hardhome-catastrophe REVEALS_TO arya-stark`

**Tier:** 2

**chapter:line:** `sources/chapters/adwd/adwd-the-blind-girl-01.md:185`

**Verbatim quote:**
> "I know where the slaves came from. They were wildlings from Westeros, from a place called Hardhome. An old ruined place, accursed."

**Arcs joined:** Jon / Hardhome arc (`hardhome-catastrophe`) → Braavos / HoBaW arc (Beth's intelligence-gathering).

**VERDICT: WEAK — prefer HARVEST, not a causal edge.**

**Reasoning:** Beth reports the Hardhome news to the kindly man as one of her three required intelligence items. The information produces no downstream action in the Braavos arc and arrives months after the actual catastrophe. `hardhome-catastrophe` already has outgoing edges into Jon's arc (`MOTIVATES jon-snow`, `ENABLES the-shieldhall-speech`); the seam to Beth is purely informational. Beth recognizes the name from Old Nan's stories at Winterfell — this is a characterization beat (her Stark memories bleed through her "no one" identity), not a causal edge between two event nodes.

**Harvest pointer:** `adwd-the-blind-girl-01.md:185 / characterization / Blind Beth recognizes "Hardhome" from Old Nan's tales — her Stark memories are not erased by FM training despite "no one" self-claim; companion to other Winterfell-memory bleeds (wolf dreams, fire smells, Jon).`

---

## SEAM 6 — Kill-List CONTRASTS No-One Training (STRONG — internal seam)

**Edge:** `kill-list-recitation-before-sleep CONTRASTS faceless-men`
*(or: `kill-list-recitation-before-sleep MOTIVATES arya-stark` — see choice rationale)*

**Tier:** 1

**chapter:line:** `sources/chapters/affc/affc-arya-02.md:11`

**Verbatim quote:**
> Each night before sleep, she murmured her prayer into her pillow. "Ser Gregor," it went. "Dunsen, Raff the Sweetling, Ser Ilyn, Ser Meryn, Queen Cersei."

**Tension quote** (the list versus "no one"):
`sources/chapters/adwd/adwd-the-blind-girl-01.md:15`
> Ser Gregor, she thought. Dunsen, Raff the Sweetling. Ser Ilyn, Ser Meryn, Queen Cersei. Her morning prayer. Or was it? No, she thought, not mine. I am no one. That is the night wolf's prayer.

**Arcs joined:** Internal seam within the Braavos arc — but wires `kill-list-recitation-before-sleep` (event node, confirmed in graph) to the `faceless-men` faction / HoBaW training arc.

**Rationale:** The `kill-list-recitation-before-sleep` node has zero outgoing edges (graph confirmed). The list is the central obstacle to Arya becoming "no one": the kindly man explicitly discovers it (affc-arya-02:13 — "No whisper was too faint to be heard"), confronts her about it, and it becomes the recurring diagnostic of her incomplete identity surrender. The FM training CONTRASTS the kill list (they demand she surrender all hate; the list is crystallized hate). The list also MOTIVATES her continued resistance — she will not surrender the wolf identity.

**Edge choice:** `kill-list-recitation-before-sleep CONTRASTS faceless-men` is structurally cleanest (event vs faction, neither is a character so MOTIVATES doesn't apply to this pairing). This wires a currently isolated event node into the Braavos faction cluster. If the preferred framing is actor-to-event: `arya-stark RESENTS faceless-men` would capture her ambivalence, but that is a different edge.

**Recommend minting:** `kill-list-recitation-before-sleep CONTRASTS faceless-men` | Tier 1 | affc-arya-02:11 with the affc-arya-02:15 quote as the tensioning confirmation.

---

## SEAM 7 — Syrio Forel / Sealord Connection → Braavos Setting (INFORMATIONAL — harvest, not causal)

**VERDICT: HARVEST only.**

**Reasoning:** Syrio Forel is already a node with `BORN_AT → braavos` and `SWORN_TO → sealord-of-braavos`. Arya mentions him fondly in Braavos (affc-arya-01:23: "Syrio was from Braavos, and Jaqen might be there as well"; affc-arya-02:81: "Syrio used to say that too, Arya remembered"). This is characterization resonance — Braavos grounds Arya in Syrio's homeland. But no causal edge connects Syrio's memory to any Braavos event. The Sealord connection (Syrio served the Sealord; Cat once pushes her barrow near the Sealord's pleasure barge) is co-location, not causation. A `syrio-forel PARALLELS arya-stark` edge within the Braavos arc could be minted by a thematic lens, but it is not a cross-arc causal seam.

---

## SUMMARY: MINT-WORTHY vs HARVEST-ONLY

| # | Seam | Verdict | Edge |
|---|------|---------|------|
| 1 | Iron coin → Braavos departure | **MINT** (highest priority) | `jaqen-hghar ENABLES [departure-to-braavos / arya-stark]` |
| 2 | Dareon desertion → Aemon stranded | **MINT** | `dareon ENABLES [maester-aemon-dies-in-braavos / samwell-tarly]` |
| 3 | Dareon's crime MOTIVATES Arya to execute him | **MINT** | `dareon MOTIVATES arya-stark` (+ upgrade `KILLS` → `EXECUTES`) |
| 6 | Kill-list CONTRASTS FM training | **MINT** | `kill-list-recitation-before-sleep CONTRASTS faceless-men` |
| 4 | Lysa-death news to Cat | **HARVEST only** | dramatic-irony pointer, affc-cat-01:113 |
| 5 | Hardhome slaves news to Beth | **HARVEST only** | characterization pointer, adwd-blind-girl-01:185 |
| 7 | Syrio resonance | **HARVEST only** | thematic pointer, no causal edge |

**Seam 1 is architecturally the most important:** it is the only edge that wires the Harrenhal/ACOK cluster *forward* into the Braavos/AFFC arc, making the HoBaW storyline reachable from the ACOK graph via a traversal chain. Without it, Braavos floats as an island.

**Seam 2+3 wire Dareon's desertion** into both the Sam/Night's Watch arc and the Braavos arc simultaneously — Dareon's node currently has `BETRAYS nights-watch` but no downstream consequences on either arc.

**Seam 6 gives the kill-list node its first outgoing edge**, connecting the isolated recitation event into the faction-level HoBaW identity-war.
