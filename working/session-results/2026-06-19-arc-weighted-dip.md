# Arc-Weighted Mode-3 Grounded-Agent Dip — 2026-06-19

**Method:** Consumer agent answers 10 arc/consequence-shaped reader questions using ONLY
graph tools (`--causal-chain`, `--neighbors`, `--path`, `--event-participants`, alias resolver),
then grades each answer against `sources/wiki/_raw/` and `sources/chapters/` ground truth.
Phase 1 (graph-only) is fully separated from Phase 2 (grading).

**Graph state at test time (`--health | head -20`):**
```
Node files (*.node.md)  :   8,533
Edge count              :  22,215
Unique edge endpoints   :   5,993
Orphan endpoints        :      62
Edge types              :   128
Dense: SWORN_TO (4148), HOLDS_TITLE (3401), CULTURE_OF (3252), PARENT_OF (1686),
       DIED_AT (915), BORN_AT (835)
```

Shipped arcs under test: Robert's Rebellion, Bran's fall, Sack of King's Landing, Purple Wedding
(all minted in S104–S106 via `--causal-chain` primitive).

---

## §1 Per-Query Table

| # | Question | Tool calls (in order) | Graph's answer | Ground truth (cite file) | Grade | Failure mode |
|---|----------|-----------------------|----------------|--------------------------|-------|--------------|
| 1 | What set Tyrion's capture (arrest by Catelyn) in motion? | `resolver --lookup "Tyrion Lannister's capture"` → MISS (candidates only, no confident HIT) → `resolver --lookup "Catelyn arrests Tyrion"` → candidate HIT `catelyn-seizes-the-moment-and-arrests-tyrion` → `--causal-chain catelyn-seizes-the-moment-and-arrests-tyrion` | **FULL ARC (4 upstream):** bran-witnesses-jaime-and-cersei → jaime-pushes-bran-from-the-tower → bran-s-direwolf-kills-the-assassin → littlefinger-names-the-dagger-as-tyrion-s → catelyn-seizes-the-moment-and-arrests-tyrion. Downstream: leads to gregor-raids-the-riverlands + motivates tywin-lannister. | Correct causal chain: Bran witnesses Jaime/Cersei → Jaime pushes Bran → assassin sent → Littlefinger frames Tyrion → Catelyn arrests Tyrion at crossroads inn. (`sources/wiki/_raw/Purple_Wedding.json`; `sources/chapters/agot/agot-catelyn-05.md`) | **correct** | slug-discoverability (first phrase MISS; second fuzzy phrase found the node — the arc data was perfect) |
| 2 | Who poisoned Joffrey / who is to blame for his death? | `resolver --lookup "poisoning of Joffrey Baratheon"` → HIT `death-of-joffrey-baratheon` → `--causal-chain death-of-joffrey-baratheon` → `--neighbors death-of-joffrey-baratheon` | Upstream: sansa-receives-the-poisoned-hairnet CAUSES death-of-joffrey-baratheon. AGENT_IN: Olenna Tyrell (with book-chapter quote). COMMANDS_IN: Petyr Baelish. VICTIM_IN: Joffrey. Downstream: TRIGGERS tyrion-accused → trial-of-tyrion-lannister. | Orchestrators: Petyr Baelish + Olenna Tyrell. Perpetrator/physical actor: Olenna (stole strangler from hairnet). Dontos as delivery mechanism. (`sources/wiki/_raw/Purple_Wedding.json` infobox: "Orchestrator: Petyr Baelish, Olenna Tyrell; Perpetrator: Olenna Redwyne, Dontos Hollard"; `sources/chapters/asos/asos-sansa-06.md`) | **correct** | — (AGENT_IN on Olenna + COMMANDS_IN on Littlefinger both present; causal chain from hairnet to death is complete) |
| 3 | What were the consequences of the Battle of the Trident? | `resolver --lookup "Battle of the Trident"` → HIT `battle-of-the-trident` → `--causal-chain battle-of-the-trident` | Downstream (2 edges): battle-of-the-trident CAUSES sack-of-kings-landing; sack-of-kings-landing CAUSES coronation-of-robert-i-baratheon. Upstream: none (arc starts here). | Aftermath: Rhaegar's death → Aerys sends Rhaella/Viserys to Dragonstone, keeps Elia as hostage, Tywin approaches with Lannister forces → Sack of King's Landing → Robert's coronation. Also: Rhaegar killed, loyalist army broken. (`sources/wiki/_raw/Battle_of_the_Trident.json` Aftermath section) | **partial** | causal-dark (partial — the main consequence chain to Sack→Coronation IS present; missing: death of Rhaegar as named outcome, Aerys's hostage-taking of Elia, Dragonstone evacuation — these are aftermath beats not yet reified as causal nodes) |
| 4 | What caused Robert's Rebellion? | `resolver --lookup "Robert's Rebellion"` → HIT `roberts-rebellion` → `--causal-chain roberts-rebellion` | **FULL UPSTREAM ARC (4 edges):** tourney-at-harrenhal CAUSES abduction-of-lyanna; abduction-of-lyanna CAUSES execution-of-brandon-and-rickard-stark; execution-of-brandon-and-rickard-stark TRIGGERS aerys-demands-ned-and-robert; aerys-demands-ned-and-robert TRIGGERS roberts-rebellion. Downstream: 0 edges (arc stops at rebellion, no consequences). | Correct: tourney at Harrenhal → Rhaegar crowns Lyanna → abduction → Stark executions by Aerys → Ned/Robert refuse summons → rebellion begins. (`sources/wiki/_raw/Robert's_Rebellion.json`) | **correct** | — (shipped arc; full 4-step upstream chain is present and accurate) |
| 5 | What did Jaime pushing Bran from the tower lead to? | `resolver --lookup "Bran pushed from tower"` → CANDIDATES (top match: `jaime-pushes-bran-from-the-tower` score 0.90) → `--causal-chain jaime-pushes-bran-from-the-tower` | **FULL ARC (1 upstream + 5 downstream):** Upstream: bran-witnesses-jaime-and-cersei TRIGGERS this event. Downstream chain: → bran-s-direwolf-kills-the-assassin → littlefinger-names-the-dagger-as-tyrion-s → catelyn-seizes-the-moment-and-arrests-tyrion → (CAUSES gregor-raids-the-riverlands; MOTIVATES tywin-lannister). | Correct: Jaime pushes Bran → assassin sent to silence Bran → direwolf kills assassin → Catelyn investigates → Littlefinger names Tyrion → Catelyn arrests Tyrion → Tywin retaliates. (`sources/chapters/agot/agot-bran-02.md`, `agot-catelyn-05.md`) | **correct** | slug-discoverability (resolver returned CANDIDATES, not clean HIT — agent must read score=0.90 as usable; a strict-HIT-only policy would MISS) |
| 6 | What set the War of the Five Kings in motion? | `resolver --lookup "War of the Five Kings"` → HIT `war-of-the-five-kings` → `--causal-chain war-of-the-five-kings` → (0 edges both directions) → `--neighbors war-of-the-five-kings` | Causal chain: empty (0 upstream, 0 downstream). Neighbors: 1 PRECEDES outbound (battle-on-the-green-fork); 69 PART_OF inbound (battles/events within the war). Greyjoy-rebellion PRECEDES war-of-five-kings (structural sequencing edge). No CAUSES/TRIGGERS edges pointing at war-of-five-kings from Ned's arrest, Joffrey's accession, or any spark event. | The war was triggered by: Robert's death → Joffrey's contested succession + Ned's arrest/execution → Robb/Stannis/Renly/Balon each declaring. Immediate sparks: arrest-of-eddard-stark, death of Jon Arryn (deeper), execution-of-eddard-stark. (`sources/wiki/_raw/War_of_the_Five_Kings.json` Prelude section) | **failed** | causal-dark (hub-absent for the causal layer: `war-of-the-five-kings` node exists but carries ZERO causal edges; `arrest-of-eddard-stark` node also has 0 causal edges; no arc connecting the spark events to this umbrella hub) |
| 7 | What caused the Red Wedding — what chain of events led Robb Stark there? | `resolver --lookup "Red Wedding"` → HIT `red-wedding` → `--causal-chain red-wedding` → (0 edges both directions) → `--neighbors red-wedding` | Causal chain: empty (0 upstream, 0 downstream). Neighbors: 12 SUB_BEAT_OF inbound (the event's own beats); PART_OF → war-of-five-kings; PRECEDES → purple-wedding. No edges representing Robb's broken Frey oath, Jeyne Westerling marriage, Roose Bolton's conspiracy, or Tywin's orchestration as causes. | Causes: Robb broke marriage pact with House Frey by wedding Jeyne Westerling. Walder Frey conspired with Roose Bolton (who'd wed Walda Frey) and Tywin Lannister orchestrated. (`sources/wiki/_raw/Red_Wedding.json`: "revenge for Robb's breaking of a marriage pact…Walder secretly begins corresponding with Roose") | **failed** | hub-absent (causal layer): the Red Wedding hub exists as an on-page event (beat-reified, 12 sub-beats) but the upstream causal arc — Robb's oath-breaking → Frey conspiracy → Tywin's coordination — is entirely missing. This is Tier-B arc B1's direct justification. |
| 8 | What were the consequences of the Greyjoy Rebellion — and how did Theon become a ward of the Starks? | `resolver --lookup "Greyjoy Rebellion"` → HIT `greyjoy-rebellion` → `--causal-chain greyjoy-rebellion` → (0 edges both directions) → `--neighbors greyjoy-rebellion` + `--path greyjoy-rebellion theon-greyjoy` | Causal chain: empty (0 upstream, 0 downstream). Neighbors: 11 PRECEDES outbound (but to WoFK sub-battles, not consequences of the rebellion). Participants/roles: Balon/Robert/Ned/Stannis COMMANDS_IN; 7 FIGHTS_IN edges; Rodrik+Maron Greyjoy VICTIM_IN. Path to Theon: 1 direct edge `theon-greyjoy UNCLE_OF greyjoy-rebellion` (wrong type — Theon isn't an uncle, this edge is malformed). Also: `theon-greyjoy WARD_OF eddard-stark` edge exists separately. | Consequences: Balon submits, swears fealty; Theon (age ~9) given to Ned Stark as hostage/ward. (`sources/wiki/_raw/Greyjoy's_Rebellion.json`: "His surviving son, the nine-year-old Theon, was given into the care of Lord Stark as a hostage to ensure Balon's good behavior"). | **partial** | causal-dark (consequence layer absent) + prose-only for hostage link (WARD_OF edge exists on Theon node, but no causal edge from greyjoy-rebellion to theon-greyjoy's ward status; also UNCLE_OF edge from Theon to greyjoy-rebellion is a malformed edge — Theon has no uncles who are events) |
| 9 | What set the Sack of King's Landing in motion, and what did it cause? | `resolver --lookup "Sack of King's Landing"` → HIT `sack-of-kings-landing` → `--causal-chain sack-of-kings-landing` | **TWO UPSTREAM causes:** battle-of-the-trident CAUSES sack-of-kings-landing; pycelle-opens-the-gates-of-kings-landing CAUSES sack-of-kings-landing. **ONE DOWNSTREAM:** sack-of-kings-landing CAUSES coronation-of-robert-i-baratheon. | Correct: Battle of Trident (Rhaegar dead, loyalists broken) + Pycelle opening the gates → Sack → Robert crowned. Missing shipped arc detail: Jaime killing Aerys (Kingslayer moment), Elia Martell's death — not yet in causal chain. (`sources/wiki/_raw/Sack_of_King's_Landing.json`) | **correct** | — (shipped arc; both upstream causes present; main downstream correct; the Elia/Jaime facts are partial/absent but the question as asked is answered) |
| 10 | Who is to blame for Ned's execution, and what set it in motion? | `resolver --lookup "Ned Stark execution"` → HIT `execution-of-eddard-stark` → `--causal-chain execution-of-eddard-stark` → (0 edges both directions) → `--neighbors execution-of-eddard-stark` | Causal chain: empty (0 upstream, 0 downstream). Neighbors: AGENT_IN Ilyn Payne, COMMANDS_IN Joffrey Baratheon, VICTIM_IN Eddard Stark, WIELDED_IN Ice, LOCATED_AT great-sept-of-baelor. Who is to blame: graph can name the direct actors but can say nothing about what led to this moment. | Blame: Joffrey (ordered it against counsel); Cersei (orchestrated Ned's arrest); Littlefinger (betrayed Ned). What led to it: Ned discovered Joffrey's illegitimacy → tried to warn Stannis → Littlefinger betrayed the gold cloaks → Cersei had Ned arrested → Ned confessed under duress expecting mercy → Joffrey had him executed anyway. (`sources/wiki/_raw/Eddard_Stark.json`) | **partial** | causal-dark (the execution hub itself names Joffrey as COMMANDS_IN correctly, but the upstream chain — Ned's discovery → betrayal → arrest → forced confession → Joffrey's defiance of counsel — is entirely absent) |

**Tally: 5 correct, 3 partial, 2 failed.**

---

## §2 Failure-Mode Tally

| Failure mode | Count | Queries |
|---|---|---|
| causal-dark (hub exists, zero causal edges in/out) | 5 | Q3 (partial), Q6, Q7, Q8 (partial), Q10 (partial) |
| hub-absent (causal layer missing, not the hub itself) | 1 | Q7 (upstream arc to Red Wedding entirely absent) |
| slug-discoverability | 2 | Q1 (first phrase MISS), Q5 (CANDIDATES not clean HIT) |
| prose-only / malformed-edge | 1 | Q8 (WARD_OF exists on character node; UNCLE_OF edge from Theon to rebellion is semantically wrong) |

Notes:
- Q3, Q8, Q10 are graded **partial** because the hubs have *some* useful content (role edges on Q10, structural context on Q8, partial downstream on Q3) but the causal spine is thin or absent.
- Q6 and Q7 are graded **failed** because the graph returns nothing causally useful and the role content doesn't exist either.
- slug-discoverability is now a **secondary** failure mode — 2 of the 2 cases were recoverable by trying an alternate phrase (Q1) or trusting a 0.90-score candidate (Q5).

---

## §3 What Works

### Shipped arcs validated

All four shipped arcs deliver correct, traversable answers:

- **Robert's Rebellion (Q4):** Full 4-step upstream chain. tourney-at-harrenhal → abduction-of-lyanna → execution-of-brandon-and-rickard-stark → aerys-demands-ned-and-robert → roberts-rebellion. This is the arc in its intended form — a reader asking "what caused Robert's Rebellion?" gets a complete, ordered chain.

- **Bran's fall (Q5):** Full 1+5 edge chain (1 upstream trigger + 5 downstream consequences), connecting to Q1's answer. The arc demonstrates that a single event (Bran witnessing Jaime/Cersei) cascades through 4 intermediate nodes to Tywin's military retaliation. This is the graph's best-in-class demonstration of multi-hop causal reasoning.

- **Sack of King's Landing (Q9):** Two upstream causes (Trident battle + Pycelle opening the gates) + one downstream (Robert's coronation). Partial but correct as far as it goes; the arc connects to the Trident chain via `battle-of-the-trident CAUSES sack-of-kings-landing`.

- **Purple Wedding / Joffrey's death (Q2):** AGENT_IN (Olenna Tyrell) + COMMANDS_IN (Petyr Baelish) with chapter-cited quotes, upstream sansa-receives-the-poisoned-hairnet chain, downstream Tyrion's trial. This is the most complex of the four shipped arcs and it answers the "who is to blame" shape correctly and completely.

### Cross-arc connectivity

Q1 and Q5 are answered by the **same Bran arc** traversed from different entry points. The consumer agent reaches the correct answer by hitting `catelyn-seizes-the-moment-and-arrests-tyrion` and getting the full upstream chain for free. This demonstrates that a well-constructed arc answers multiple reader questions simultaneously.

### Structural layer (non-causal)

`--path` and `--neighbors` for structural facts remain strong. Q8's WARD_OF edge (`theon-greyjoy WARD_OF eddard-stark`) is correct and cited; the `--path` query returns it as a direct edge immediately. The 15 role edges on `greyjoy-rebellion` name the correct commanders and victims. The `--neighbors` output on `execution-of-eddard-stark` correctly names Ilyn Payne (AGENT_IN), Joffrey (COMMANDS_IN), Ice (WIELDED_IN), and the Great Sept — the execution's direct participants are well-covered.

---

## §4 Re-Ranking Signal for Tier-B Arcs

### The two candidates

**B1 — Catelyn-frees-Jaime → Robb's host turns → Jeyne Westerling marriage → feeds Red Wedding**
**B2 — Greyjoy Rebellion → Theon-as-hostage → ironborn invasion of the North**

### What the dip shows

**Q7 (Red Wedding causes) is the single clearest justification for B1.** The Red Wedding hub exists with 12 beautifully reified sub-beats — the on-page event is fully covered. But the upstream causal arc is completely absent. Asked "what chain of events led Robb Stark there?", the graph returns 0 causal edges and falls back to structural context only. The ground truth requires: Robb's oath-breaking (Jeyne Westerling marriage) → Frey conspiracy → Roose Bolton's alignment with Tywin → the setup at the Twins. None of this is encoded as causal edges. B1's arc would fill exactly this gap — it is the upstream prelude that the Red Wedding hub is dark on.

**Q6 (War of Five Kings in motion) is arc-shaped but is NOT a B1 or B2 arc problem — it is a hub-level gap.** The `war-of-five-kings` node has 0 causal edges despite 69 PART_OF events inside it. The upstream sparks (Ned's arrest, Joffrey's accession, Robert's death) are not connected causally to this umbrella node. This is a separate, larger structural problem — not what B1 or B2 addresses.

**Q8 (Greyjoy Rebellion consequences / Theon-as-hostage) partially justifies B2.** The `greyjoy-rebellion` hub has 0 causal edges, and the hostage relationship (`theon-greyjoy WARD_OF eddard-stark`) is captured as a character-level dyad but is not connected to the rebellion as a causal consequence. B2's arc would add: greyjoy-rebellion-ends CAUSES theon-sent-as-ward → theon-as-hostage-grows-up-at-winterfell → theon-invades-north (motivates). However, Q8's core fact — that Theon is a ward/hostage of Ned — IS already in the graph as a direct WARD_OF edge, reachable by `--path`. A reader asking the second half of Q8 ("how did Theon come to be a ward?") gets the WARD_OF edge but not the causal mechanism. B2 would help, but the urgency is lower than B1 because the key fact survives as a structural dyad.

### Verdict

**Build B1 next.** Q7 is the direct, unambiguous failing question that B1 answers. The Red Wedding hub is otherwise the graph's best-covered on-page event (12 sub-beats, all cited), and its upstream causal darkness is the most conspicuous gap in the arc layer. A reader asking about the Red Wedding's causes gets nothing from causal queries — and it is the most asked-about event in ASOIAF.

**B2 is indicated but lower-urgency.** The Greyjoy Rebellion hub is causal-dark, and B2 would connect it to Theon's arc. But Q8 is partially answered by existing dyadic edges (WARD_OF, COMMANDS_IN, FIGHTS_IN) — the question gets a partial rather than a failed grade. B2 is the right *second* Tier-B arc.

**Q6 (War of Five Kings) is a separate problem** — it needs a `TRIGGERS` or `CAUSES` edge from the spark events (`execution-of-eddard-stark`, `arrest-of-eddard-stark`, `death-of-robert-baratheon`) to the umbrella `war-of-five-kings` node. This is not an arc (no multi-step chain to build) — it is a small set of ~3 causal attachment edges that could be added to the existing nodes deterministically. Flag separately.

---

## §5 Bottom Line for Matt

The four shipped arcs (Robert's Rebellion, Bran's fall, Sack of KL, Purple Wedding) all validate: they return correct, multi-hop causal answers for the questions they cover (Q1, Q2, Q4, Q5, Q9), and the Bran arc's cross-arc connectivity — answering both Q1 and Q5 from the same chain — demonstrates that a well-constructed arc is a force multiplier. The score improved from the prior dip's 4/10 to 5/10 correct (3 partial, 2 failed), entirely because the shipped arcs now answer Q1, Q2, Q4, Q5, Q9 where the prior dip had failures.

The two hard failures are both causal-dark events: **Q6 (War of Five Kings)** and **Q7 (Red Wedding causes)**. Q6 is a structural attachment problem (a few `TRIGGERS` edges needed from spark-events to the umbrella node). Q7 is what **Tier-B arc B1** exists to solve — the upstream prelude chain to the Red Wedding (Robb's broken oath → Frey conspiracy) is entirely missing, and the Red Wedding hub is otherwise the most complete on-page event in the graph.

**Build B1 (Catelyn-frees-Jaime → Jeyne Westerling marriage → feeds Red Wedding) next. Then attach Q6's spark events causally to `war-of-five-kings` (cheap, ~3 edges). Then B2 (Greyjoy Rebellion → Theon-as-ward → ironborn invasion).**

---

## §6 Orchestrator corrections + action taken (S107, 2026-06-19)

**Q6 re-frame — do NOT attach sparks to `war-of-the-five-kings`.** The dip's §5 recommendation to add `TRIGGERS`/`CAUSES` edges from spark events (Ned's execution, Robert's death) to the `war-of-five-kings` umbrella node **conflicts with the project's hard-stop discipline**: the standing rule (S105, `reference/narrative-arc-glossary.md`) is to never assert `X CAUSES war-of-the-five-kings` — it is the canonical multi-attributed terminus ("a thesis, not an edge"). The Bran's-fall arc deliberately hard-stopped short of WO5K for exactly this reason. So `war-of-five-kings` remaining causal-dark (Q6) is **correct by policy, not a gap to fill**. Q6 is therefore re-graded `failed` → working-as-intended (no backfill). This is the dip agent making a reasonable-looking suggestion it lacked the policy context to vet — flagged and overruled by the orchestrator.

**B1 SHIPPED this session.** Q7's gap is closed. Minted the B1 Red Wedding upstream arc as **two parallel consequence-chains** (the source check confirmed they are parallel, not a single sequential chain — the Karstark loss did NOT cause the Red Wedding; the broken Frey pact did):
- *Catelyn frees Jaime* → CAUSES → *Karstark murders the prisoners* → CAUSES → *execution of Rickard Karstark* (the cost of freeing Jaime: Robb loses the Karstarks).
- *Robb weds Jeyne Westerling* → TRIGGERS → *Red Wedding conspiracy* → CAUSES → *Red Wedding* / *Robb is killed* (the broken pact → betrayal).

5 new beat-nodes + 21 edges (16 role Tier-1 + 5 causal Tier-2); all 5 causal edges fresh-subagent CONFIRMED (`working/causal-arc-strategy-b1-redwedding-verify.md`). `--causal-chain red-wedding` now returns the upstream chain — Q7 answerable. Hard-stop held (no edge to WO5K). The agency-collapse fix is the `red-wedding-conspiracy` event.conspiracy beat-node, which carries the conspirators' decisions as role edges (Walder COMMANDS_IN, Roose AGENT_IN, Tywin COMMANDS_IN-Tier-2) rather than collapsing them into a blunt event→event arrow.

**B2 (Greyjoy→Theon-as-ward) NOT built** — Q8 was only partial (the `theon-greyjoy WARD_OF eddard-stark` dyad already answers the core fact). Per dip-driven cadence, it waits for a future dip to show genuine fumbling. Re-dip before building it.
