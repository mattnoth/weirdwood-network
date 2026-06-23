# Robert's Rebellion — ENRICHMENT PROPOSAL (opus-ab, independent blind run)

> Single max-effort analyst, full scope. PROPOSE-only — nothing minted.
> Dedup truth = `working/enrichment/rr/baseline.md` "ALREADY EXISTS" list + my own `--neighbors` re-confirms.
> **Blind-experiment compliance:** I treated as NON-EXISTENT the parallel-run nodes
> (`knight-of-the-laughing-tree-incident`, `exile-of-jon-connington`, `murder-of-jon-arryn`,
> `slaying-of-aerys-ii-the-kingslaying`, `aerys-commands-the-city-burned`,
> `murder-of-elia-martell-and-rhaegars-children`, `pycelle-opens-the-gates-of-kings-landing`) and every
> `run_id: rr-enrichment-s133` edge I happened to see in live `--neighbors` output. I did NOT read the
> lens1/2/3/synthesis files. Where I independently judge a parallel-minted item worth it, I re-propose it and
> tag it `confirmed-absent` (= absent per baseline.md, my dedup contract).

---

## SELF-ASSESSMENT

**Totals proposed by category**
- NEW secondary-event nodes (with full mint spec): **7**
- New role edges onto existing + new nodes: **18**
- CAUSAL / DOWNSTREAM / CROSS-ARC edges: **9**
- SUSPECTED_OF / WITNESS_IN substrate edges: **8**
- Bare-node book-cite OVERLAYS (wiki cite_ref → navigable chapter:line): **7**
- RECAST recommendations (off-vocab / junk): **2**
- **Grand total proposed items: 51** (+ 2 recast/drop flags)

**3 HIGHEST-VALUE items**
1. **Cross-arc bridge: RR → AEGON.** `combat-at-the-tower-of-joy` and the Sack atrocity together create the
   condition the entire `aegon` container exists to undo. Concretely: `murder-of-elia-martell-and-rhaegars-children
   MOTIVATES landing-of-the-golden-company` (Aegon's claim is "the child who *wasn't* murdered") + `battle-of-the-bells
   CAUSES exile-of-jon-connington` + `exile-of-jon-connington ENABLES aegon-revealed-to-the-golden-company`. This is the
   single biggest yield: the RR cluster currently dead-ends with 0 real outgoing edges; this wires it forward into a
   built present-day arc.
2. **Jon-Arryn-murder substrate, Tier-1, theory-safe.** `lysa-arryn AGENT_IN murder-of-jon-arryn` + `petyr-baelish
   SUSPECTED_OF murder-of-jon-arryn` + `murder-of-jon-arryn CAUSES catelyn-receives-the-letter-blaming-the-lannisters`,
   anchored on Lysa's verbatim moon-door confession (asos-sansa-07:287). This is the literal hinge between RR's
   aftermath and the War of the Five Kings — and it can be built at Tier 1 (Lysa) / Tier 2 (Petyr) without asserting
   any gated reading.
3. **Wildfire-plot + Kingslaying book-cite overlay + MOTIVATES edge.** Jaime's bath confession (asos-jaime-05:49–63)
   gives navigable Tier-1 book provenance for the wildfire caches AND establishes that the kingslaying was *motivated by*
   the plot (`wildfire-plot MOTIVATES slaying-of-aerys-ii-the-kingslaying`) — upgrading three wiki-only cite_refs to
   openable chapter:line cites in one pass.

**Items CONSIDERED but REJECTED (informative negatives)**
- `tourney-at-harrenhal CAUSES roberts-rebellion` — REJECTED as agency-collapse / too-distal. The tourney CAUSES the
  abduction (already in graph); the war is triggered by `aerys-demands-ned-and-robert` (already in graph). A direct
  tourney→war CAUSES would launder several intervening agents' decisions into one edge. Keep the existing 4-link chain.
- `rhaegar-targaryen SUSPECTED_OF murder-of-elia-martell-and-rhaegars-children` — REJECTED. No textual basis; Rhaegar
  died at the Trident before the Sack. Would be a category error.
- `knight-of-the-laughing-tree-incident CAUSES abduction-of-lyanna` — REJECTED as a gated-reading smuggle. The causal
  link only exists *through* the unproven KotLT=Lyanna reading. I propose the incident node + a non-committal
  `SUB_BEAT_OF tourney-at-harrenhal` only; no causal edge to the abduction.
- `siege-of-storms-end CAUSES ...` downstream — REJECTED for now. Storm's End's relief (Davis's onion run) feeds
  Stannis/Davos backstory, but there is no built node to bridge *to* yet; would be an orphan. Left as overlay-only.
- `barristan-selmy WITNESS_IN slaying-of-aerys-ii-the-kingslaying` — REJECTED. Barristan was at the Trident, not in the
  throne room for the kingslaying; placing him there would be a factual error.
- A `murders-of-rhaenys-and-aegon` node SEPARATE from `murder-of-elia-martell-and-rhaegars-children` — REJECTED as
  granularity overclaim. One atrocity-beat node covering Elia + both children is the right grain; splitting Rhaenys from
  Aegon adds no traversal value and fractures the victim role-edges.

---

## NEW NODES (full mint spec)

> Slugs chosen independently. Where the parallel run already minted a same-meaning node, tagged `confirmed-absent`
> (absent per baseline) — Matt/merge-step dedups against live graph at mint time; if the parallel slug is kept, attach
> my role-edges/overlays to it instead.

### N1 — `slaying-of-aerys-ii-the-kingslaying`  `confirmed-absent`
- **name:** Slaying of Aerys II (the Kingslaying) · **type:** event.assassination
- **aliases:** the kingslaying, killing of the Mad King, Jaime slays Aerys, death of Aerys II
- **parent:** SUB_BEAT_OF → `sack-of-kings-landing`
- **role edges:**
  - `jaime-lannister AGENT_IN slaying-of-aerys-ii-the-kingslaying` — Tier 1 — asos-jaime-05:63 —
    `"Then I slew Aerys, before he could find someone else to carry his message to the pyromancers."`
  - `aerys-ii-targaryen VICTIM_IN slaying-of-aerys-ii-the-kingslaying` — Tier 1 — asos-jaime-05:41 —
    `"The oathbreaker who murdered poor sad Aerys Targaryen."`
- **anchor quote (node body):** asos-jaime-05:63 (above).
- **rationale:** The Sack currently has Jaime AGENT_IN the *whole* Sack; the specific regicide — the series' most
  scrutinised act — has no beat node. Enables the MOTIVATES edge from the wildfire-plot (C-edges below).

### N2 — `aerys-commands-the-city-burned`  `confirmed-absent`
- **name:** Aerys Commands the City Burned · **type:** event.incident
- **aliases:** burn them all, Aerys's wildfire order, the pyromancers' command
- **parent:** SUB_BEAT_OF → `sack-of-kings-landing`
- **role edges:**
  - `aerys-ii-targaryen AGENT_IN aerys-commands-the-city-burned` — Tier 1 — asos-jaime-05:61 —
    `"My man came back with a royal command. ‘Bring me your father’s head, if you are no traitor.’"`
    (companion body cite asos-jaime-05:57: `"The traitors want my city ... but I’ll give them naught but ashes."`)
- **anchor quote:** asos-jaime-05:57 (above).
- **rationale:** The in-world *cause* of the kingslaying. Without this node the kingslaying's motive is uncited; with it
  the chain `wildfire-plot → aerys-commands-the-city-burned → slaying-of-aerys` is fully grounded. Theory-safe (no R+L).

### N3 — `murder-of-elia-martell-and-rhaegars-children`  `confirmed-absent`
- **name:** Murder of Elia Martell and Rhaegar's Children · **type:** event.death
- **aliases:** the Sack atrocities, murder of Elia and the children, deaths of Rhaenys and Aegon, killing of Princess Elia
- **parent:** SUB_BEAT_OF → `sack-of-kings-landing`
- **role edges:**
  - `gregor-clegane AGENT_IN murder-of-elia-martell-and-rhaegars-children` — Tier 1 — asos-tyrion (Oberyn account; see
    OVERLAY O6 for the exact line) — rationale: Gregor is AGENT_IN the Sack already; this re-targets to the specific killings.
  - `amory-lorch AGENT_IN murder-of-elia-martell-and-rhaegars-children` — Tier 1 — same Oberyn account.
  - `elia-martell VICTIM_IN murder-of-elia-martell-and-rhaegars-children` — Tier 1
  - `rhaenys-targaryen-daughter-of-rhaegar VICTIM_IN ...` — Tier 1
  - `aegon-targaryen-son-of-rhaegar VICTIM_IN ...` — Tier 1 (note: the in-world *claim* this child survived is the AEGON arc — VICTIM_IN encodes the canonical Sack outcome; the survival claim lives on the aegon-arc nodes, not here)
  - `tywin-lannister COMMANDS_IN murder-of-elia-martell-and-rhaegars-children` — **Tier 2** — flagged: Tywin's ordering
    of the child-murders is strongly implied (he presents the bodies to Robert) but not stated as a direct command;
    propose as Tier-2 COMMANDS_IN with body-cite, NOT Tier 1. If a verbatim command line can't be found, demote to
    `SUSPECTED_OF` instead.
- **anchor quote:** see OVERLAY O6.
- **rationale:** Highest cross-arc value — this is the beat the AEGON arc inverts (C-edges). Currently only the umbrella
  Sack has these victims; the specific atrocity beat is missing per baseline #4.

### N4 — `pycelle-opens-the-gates-of-kings-landing`  `confirmed-absent`
- **name:** Pycelle Opens the Gates of King's Landing · **type:** event.incident
- **aliases:** opening the gates to Tywin, Pycelle's betrayal, the sack of the gates
- **parent:** SUB_BEAT_OF → `sack-of-kings-landing`; also `pycelle-opens-the-gates-of-kings-landing CAUSES sack-of-kings-landing`
- **role edges:**
  - `pycelle AGENT_IN pycelle-opens-the-gates-of-kings-landing` — Tier 1 — asos-jaime-05:59 —
    `"Pycelle convinced the king that his Warden of the West had come to defend him, so he opened the gates."`
- **rationale:** baseline says the CAUSES edge to the Sack exists (parallel-minted); the node + Pycelle's agency role
  is the substrate. Theory-safe.

### N5 — `knight-of-the-laughing-tree-incident`  `confirmed-absent`
- **name:** Knight of the Laughing Tree Incident · **type:** event.incident
- **aliases:** the mystery knight of Harrenhal, the laughing tree challenge, the three squires' shaming
- **parent:** SUB_BEAT_OF → `tourney-at-harrenhal`  *(NO causal edge to abduction — see rejections)*
- **role edges (substrate ONLY — identity GATED):**
  - `aerys-ii-targaryen WITNESS_IN knight-of-the-laughing-tree-incident` — Tier 1 — asos-bran-02:229 —
    `"the king himself urged men to challenge him, declaring that the face behind that helm was no friend of his."`
  - `rhaegar-targaryen AGENT_IN knight-of-the-laughing-tree-incident` — Tier 1 — asos-bran-02:229 —
    `"the king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree."`
    (role = the searcher; AGENT_IN of the search, not of the disguise)
- **GATED — do NOT mint:** any edge asserting `lyanna-stark IS knight-of-the-laughing-tree` or `howland-reed IS ...`.
  KotLT identity is a gated reading. The `knight-of-the-laughing-tree` CHARACTER node already exists (baseline) as the
  unidentified persona; leave it unlinked to Lyanna.
- **anchor quote:** asos-bran-02:217 — `"The device upon his shield was a heart tree of the old gods, a white weirwood with a laughing red face."`
- **rationale:** baseline #4 — the character exists, the incident does not. High value as a self-contained mystery beat;
  carefully built to carry the in-world FACTS (Aerys's hostility, Rhaegar's search) without the gated identity.

### N6 — `murder-of-jon-arryn`  `confirmed-absent`
- **name:** Murder of Jon Arryn · **type:** event.assassination
- **aliases:** poisoning of Jon Arryn, death of the Hand, the tears of Lys murder
- **parent:** none structural to RR (post-RR aftermath). It is the bridge beat between RR's settlement and the WO5K.
- **role edges:**
  - `lysa-arryn AGENT_IN murder-of-jon-arryn` — **Tier 1** — asos-sansa-07:287 —
    `"You told me to put the tears in Jon’s wine, and I did."`
  - `jon-arryn VICTIM_IN murder-of-jon-arryn` — Tier 1 — same line.
- **SUSPECTED_OF (Tier 2):** `petyr-baelish SUSPECTED_OF murder-of-jon-arryn` — see SUBSTRATE S1.
- **rationale:** highest-value mystery node. Lysa's confession is verbatim and unambiguous about *her* act; Petyr's
  authorship is confessed-by-Lysa but he never admits it himself → correctly Tier-2 SUSPECTED_OF. No gated reading needed.

### N7 — `exile-of-jon-connington`  `confirmed-absent`
- **name:** Exile of Jon Connington · **type:** event.incident
- **aliases:** Connington's banishment, the stripping of the griffin lord, Aerys exiles his Hand
- **parent:** none structural; links via causal edges (C-edges).
- **role edges:**
  - `jon-connington VICTIM_IN exile-of-jon-connington` — Tier 1 — asos-jaime-05:53 —
    `"After dancing griffins lost the Battle of the Bells, Aerys exiled him."`
  - `aerys-ii-targaryen AGENT_IN exile-of-jon-connington` — Tier 1 — same line.
- **rationale:** This is THE node that bridges RR forward into the AEGON arc. Connington's exile is the seed of his later
  role smuggling "Young Griff." baseline #3 names the Connington-defeat-and-exile beat as missing from battle-of-the-bells.

---

## CAUSAL / DOWNSTREAM / CROSS-ARC EDGES

> Guarded against sibling-CAUSES. Each is real causation, not sequence.

### Internal RR causal gaps
- **C1** `wildfire-plot MOTIVATES slaying-of-aerys-ii-the-kingslaying` — Tier 1 — asos-jaime-05:63 —
  `"Then I slew Aerys, before he could find someone else to carry his message to the pyromancers."` —
  rationale: Jaime kills Aerys *specifically to stop the wildfire detonation*. MOTIVATES (not CAUSES) is exact: the plot
  is the motive, the kingslaying is the chosen act. `NEW` (parallel may have a variant; baseline lists no such edge).
- **C2** `aerys-commands-the-city-burned MOTIVATES slaying-of-aerys-ii-the-kingslaying` — Tier 1 — asos-jaime-05:61 —
  `"My man came back with a royal command. ‘Bring me your father’s head, if you are no traitor.’"` — rationale: the
  immediate command that triggers the act. `NEW`.
- **C3** `battle-of-the-bells CAUSES exile-of-jon-connington` — Tier 1 — asos-jaime-05:53 —
  `"After dancing griffins lost the Battle of the Bells, Aerys exiled him."` — `confirmed-absent`
  (baseline lists battle-of-the-bells with PART_OF+PRECEDES only; the live graph shows a parallel variant — re-propose).

### Cross-arc bridges — RR → AEGON (the headline yield)
- **C4** `exile-of-jon-connington ENABLES aegon-revealed-to-the-golden-company` — Tier 2 — asos-jaime-05:53 +
  aegon-arc nodes — rationale: Connington's exile is the precondition for his later guardianship of the supposed Aegon;
  ENABLES (not CAUSES) because many other factors intervene. `confirmed-absent` (baseline; parallel variant seen live).
- **C5** `murder-of-elia-martell-and-rhaegars-children MOTIVATES landing-of-the-golden-company` — Tier 2 —
  rationale: the AEGON arc's entire premise is that the child reportedly murdered in this beat *survived* and now returns
  to claim the throne; the (claimed) atrocity is the motive engine of the invasion. MOTIVATES is the safe, exact verb —
  it does NOT assert the survival is true. `NEW`. **High value.**
- **C6** `sack-of-kings-landing MOTIVATES landing-of-the-golden-company` — REJECTED-redundant: C5 carries this more
  precisely; do not also add the umbrella edge (would double-count).

### Cross-arc bridges — RR → WO5K
- **C7** `murder-of-jon-arryn CAUSES catelyn-receives-the-letter-blaming-the-lannisters` — Tier 1 — asos-sansa-07:287 —
  `"And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."` — rationale: Lysa's
  false letter is the direct cause of the chain that becomes the WO5K. **Conditional:** only mint if a target node
  exists; if `catelyn-receives-the-letter...` is absent, instead add **C7-alt** `murder-of-jon-arryn MOTIVATES
  arrest-of-eddard-stark` is too distal — REJECT C7-alt, leave C7 pending node creation. `NEW`.
- **C8** `murder-of-jon-arryn CAUSES eddard-stark-becomes-hand` — Tier 1 — agot-eddard-01/02 (Robert rides north to ask
  Ned *because* Jon Arryn died) — **Conditional** on a "Ned named Hand" node existing; if absent, leave as a prose note,
  do not orphan. rationale: Jon Arryn's death vacates the Handship that pulls Ned into the capital. `NEW (gated on node)`.

### RR → present (Robert/Targaryen-restoration motive)
- **C9** `roberts-rebellion MOTIVATES robert-orders-daenerys-assassination` — Tier 1 — agot-eddard-08:13 —
  `"I want them dead, mother and child both, and that fool Viserys as well."` — rationale: Robert's standing order to
  kill the last Targaryens is the *direct continuation* of the war that put him on the throne; this is a clean
  RR-hub → WO5K-container outgoing edge that fixes the "hub has 0 real outgoing edges" problem at the cluster head.
  `NEW`. (Distinct from the existing `robert-baratheon AGENT_IN robert-orders-daenerys-assassination` role edge.)

---

## SUSPECTED_OF / WITNESS_IN SUBSTRATE (the mystery layer)

> Tier-2 for SUSPECTED_OF; never asserts the act. WITNESS_IN is Tier-1 presence. All theory READINGS stay GATED.

- **S1** `petyr-baelish SUSPECTED_OF murder-of-jon-arryn` — **Tier 2** — asos-sansa-07:287 —
  `"You told me to put the tears in Jon’s wine, and I did. ... just as you said."` — rationale: Lysa names Petyr as the
  one who told her; Petyr never confesses → his agency is contested/unproven from his own mouth = exactly SUSPECTED_OF.
  `confirmed-absent` (baseline: "No SUSPECTED_OF substrate anywhere").
- **S2** `lysa-arryn WITNESS_IN ...` — N/A, she is AGENT (see N6). (noted to prevent double-encoding.)
- **S3** `howland-reed WITNESS_IN combat-at-the-tower-of-joy` — Tier 1 — agot-eddard-10:93 —
  `"only two had lived to ride away; Eddard Stark himself and the little crannogman, Howland Reed."` —
  `confirmed-absent` per baseline (live graph shows parallel variant — re-propose; he is the sole non-Ned survivor,
  the key living witness to whatever happened at the tower). Substrate ONLY — does NOT assert R+L=J.
- **S4** `eddard-stark WITNESS_IN combat-at-the-tower-of-joy` — Tier 1 — agot-eddard-10:93 (same line) —
  `confirmed-absent` per baseline. The other survivor. Substrate ONLY.
- **S5** `lyanna-stark VICTIM_IN combat-at-the-tower-of-joy` — REJECTED as overclaim. Lyanna is *at* the tower (dies
  there) but is not a combatant/victim *of the combat*. Better: `lyanna-stark LOCATED_AT tower-of-joy` (structural) —
  propose that instead, Tier 1, agot-eddard-10:11 `"a tower long fallen, and Lyanna in her bed of blood."` `NEW`.
- **S6** `arthur-dayne WITNESS_IN combat-at-the-tower-of-joy` — REJECTED. Already FIGHTS_IN (baseline). WITNESS would be
  redundant/weaker than the existing combat role. Do not add.
- **S7** `varys SUSPECTED_OF murder-of-jon-arryn` — REJECTED. No in-text basis; the only confessed thread is Lysa→Petyr.
  Adding Varys would be inventing a suspect. Do not add.
- **S8** `cersei-lannister SUSPECTED_OF murder-of-jon-arryn` — Tier 2 — agot-eddard era: Ned *believes* Cersei behind it;
  this is the in-world red herring the narrative deliberately plants. — rationale: encoding the *in-world suspicion*
  (not the truth) is legitimate SUSPECTED_OF substrate and captures the mystery's misdirection. **Propose with caution**;
  cite agot-eddard chapter where Ned suspects the Lannisters (needs exact line confirm at mint). `NEW (cite-pending)`.

---

## BARE-NODE BOOK-CITE OVERLAYS (wiki cite_ref → navigable chapter:line)

> memory `feedback_book_citation_overlay_value`: do it even when the wiki node already states the fact.
> All quotes verbatim contiguous.

- **O1** `wildfire-plot` (currently wiki-only) — overlay book cite asos-jaime-05:53 —
  `"So His Grace commanded his alchemists to place caches of wildfire all over King’s Landing."` — Tier 1. `OVERLAY`.
- **O2** `wildfire-plot` Rossart agency — overlay asos-jaime-05:55 —
  `"Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer."` — Tier 1.
- **O3** `battle-of-the-trident` (Robert kills Rhaegar) — overlay agot-eddard-10:171 —
  `"I killed him, Ned, I drove the spike right through that black armor into his black heart, and he died at my feet."`
  — Tier 1. (existing trident edges cite wiki — this is the navigable book line.) `OVERLAY`.
- **O4** `combat-at-the-tower-of-joy` (the threefold standoff) — overlay agot-eddard-10:15 —
  `"They waited before the round tower, the red mountains of Dorne at their backs, their white cloaks blowing in the wind."`
  — Tier 1. `OVERLAY`.
- **O5** `combat-at-the-tower-of-joy` (aftermath / cairns) — overlay agot-eddard-10:93 —
  `"Ned had pulled the tower down afterward, and used its bloody stones to build eight cairns upon the ridge."` — Tier 1.
- **O6** `murder-of-elia-martell-and-rhaegars-children` anchor — needs the Oberyn/Tyrion account line. Candidate location
  asos-tyrion (Oberyn names Gregor as Elia's killer). **Cite-pending** — at mint, grep asos-tyrion chapters for
  `"Elia"` + `"Mountain"`; do not mint the node body until the verbatim line is captured. Flagged so the node isn't
  shipped with a wiki-only anchor. `OVERLAY (pending)`.
- **O7** `sack-of-kings-landing` (Pycelle opens the gates) — overlay asos-jaime-05:59 —
  `"Pycelle convinced the king that his Warden of the West had come to defend him, so he opened the gates."` — Tier 1.

---

## RECAST / DROP FLAGS (recommend, do not unilaterally churn)

- **R1 — DROP junk edge.** baseline #1: `roberts-rebellion GUEST_OF winterfell` with quote
  `"Take the books away…healthy appetites"` is a misparse. Recommend DROP. (GUEST_OF is also off the locked vocab.)
  This is what's making the hub's single outgoing edge garbage; C9 above gives it a real outgoing edge to replace it.
- **R2 — RECAST off-vocab.** baseline: `rhaegar-targaryen CROWNS_QUEEN_OF_LOVE_AND_BEAUTY lyanna-stark` uses a
  non-vocab type. **Recommendation: do NOT force it into the locked set** — the crowning is a discrete symbolic act that
  the abduction-causal chain already routes around (`tourney CAUSES abduction`). Cleanest: convert to a beat node
  `crowning-at-harrenhal` (event.ceremony, SUB_BEAT_OF tourney-at-harrenhal) with `rhaegar AGENT_IN` + `lyanna ...` —
  **but I flag this as `NEEDS_VOCAB` territory** for the recipient-of-honor role (no locked role fits "was crowned").
  `NEEDS_VOCAB: a role for "honored/designated recipient of a ceremonial title" (queen of love and beauty); current
  roles AGENT/VICTIM/COMMANDS/WITNESS/OFFICIATES don't cover an honoree.` STOP — do not invent; leave the existing
  off-vocab edge in place + flagged until vocab decision.

---

## DEDUP LEDGER (quick scan)
- Re-confirmed via `--neighbors`: roberts-rebellion (0 real out), wildfire-plot, battle-of-the-bells, abduction-of-lyanna,
  combat-at-the-tower-of-joy, sack-of-kings-landing, coronation, death-of-robert-baratheon,
  robert-orders-daenerys-assassination, landing-of-the-golden-company, aegon-revealed-to-the-golden-company.
- Existing role layers (Trident ×8 FIGHTS_IN, ToJ ×10 FIGHTS_IN, Harrenhal ×16 ATTENDS, Sack AGENT/COMMANDS/VICTIM) —
  NOT re-proposed.
- Existing causal spine (tourney→abduction→execution; aerys-demands→RR; trident→sack→coronation) — NOT re-proposed.
- `abduction-of-lyanna` already has `rhaegar SUSPECTED_OF abduction` — NOT re-proposed (baseline lists it; good — that
  is the contested-agency encoding I would otherwise have added).
