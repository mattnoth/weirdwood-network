# RR Enrichment — Lens 3 Proposal (Secondary-Event Nodes, Role Edges, Bare-Node Depth)
# Session S133 · 2026-06-22

> **5-line summary:**
> - 2 NEW event nodes proposed: `knight-of-the-laughing-tree-incident`, `exile-of-jon-connington`
> - 8 ROLE EDGES proposed across the 2 new nodes + `wildfire-plot` enrichment
> - 4 OVERLAY items: bare-node depth / book-cite upgrades for `wildfire-plot`, `battle-of-the-bells`, `abduction-of-lyanna`, `battles-at-summerhall`
> - **Highest-value node:** `knight-of-the-laughing-tree-incident` — unblocks Lens 2's SUSPECTED_OF substrate; links the identity-mystery to the tourney; currently the character node has 1 edge and the incident has no home at all
> - DEDUP NOTE: `murder-of-elia-martell-and-rhaegars-children` ALREADY EXISTS with full role edges — not re-proposed here

---

## Section 1 — NEW NODES

---

### NODE-1: `knight-of-the-laughing-tree-incident`

| Field | Value |
|---|---|
| slug | `knight-of-the-laughing-tree-incident` |
| name | "Knight of the Laughing Tree incident" |
| type | `event.incident` |
| aliases | "Knight of the Laughing Tree", "mystery knight incident", "Laughing Tree incident at Harrenhal" |
| confidence | tier-1 (incident demonstrably occurred; identity is gated tier-2/3) |
| era | roberts-rebellion |
| occurred.ac_year | 281 |
| occurred.precision | year |
| occurred.basis_source | book-chapter |
| occurred.date_confidence | tier-2 |
| pass_origin | s133-rr-enrich-lens3 |
| node_version | 1 |

**1-line description:** During the Tourney at Harrenhal, a mystery knight in patchwork armor bearing a weirwood heart-tree shield appeared, defeated three champions whose squires had beaten the crannogman Howland Reed, and demanded only that the knights "teach your squires honor" as ransom — then vanished when Aerys sent Rhaegar to unmask him.

**Parent:** SUB_BEAT_OF `tourney-at-harrenhal`

**Dedup check:** `find graph/nodes -iname '*laughing-tree-incident*'` → no match. `find graph/nodes -iname '*kotlt*'` → no match. The character node `knight-of-the-laughing-tree` exists; this is its **incident** counterpart. The theories node `knight-of-the-laughing-tree-theories` also exists and is unaffected. NEW.

**Anchor quote:**
> "Whoever he was, the old gods gave strength to his arm. The porcupine knight fell first, then the pitchfork knight, and lastly the knight of the two towers. None were well loved, so the common folk cheered lustily for the Knight of the Laughing Tree, as the new champion soon was called. When his fallen foes sought to ransom horse and armor, the Knight of the Laughing Tree spoke in a booming voice through his helm, saying, 'Teach your squires honor, that shall be ransom enough.'"

— Meera Reed to Bran, `asos-bran-02.md:225`

**Secondary quote (Aerys sends Rhaegar to unmask):**
> "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree. It was the dragon prince who won that tourney in the end."

— `asos-bran-02.md:229`

---

### NODE-2: `exile-of-jon-connington`

| Field | Value |
|---|---|
| slug | `exile-of-jon-connington` |
| name | "Exile of Jon Connington" |
| type | `event.incident` |
| aliases | "Connington stripped and exiled", "stripping of Connington's titles", "Jon Connington sent into exile" |
| confidence | tier-1 |
| era | roberts-rebellion |
| occurred.ac_year | 283 |
| occurred.precision | year |
| occurred.basis_source | book-chapter |
| occurred.date_confidence | tier-2 |
| pass_origin | s133-rr-enrich-lens3 |
| node_version | 1 |

**1-line description:** After Jon Connington's failure to kill Robert at the Battle of the Bells, King Aerys stripped him of his titles and sent him into exile — the event that removed House Targaryen's chief Hand-level field commander, directly enabling the circumstances under which Connington would later raise Young Griff (Aegon VI claimant) in the AEGON-container arc.

**Parent:** SUB_BEAT_OF `battle-of-the-bells` (the exile is the immediate consequence of the defeat)

**Dedup check:** `find graph/nodes -iname '*connington-exile*'` → no match. `find graph/nodes -iname '*exile-of-jon*'` → no match. Jon Connington character node exists; this is the precipitating event node. NEW.

**Anchor quote:**
> "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion, the lands and lordship had remained within House Connington, passing to his cousin Ser Ronald, the man whom Jon had made his castellan when he went to King's Landing to attend Prince Rhaegar."

— Jon Connington's POV, `adwd-the-griffin-reborn-01.md:57`

**Secondary quote (the self-reckoning that makes this a graph beat, not just backstory):**
> "I rose too high, loved too hard, dared too much. I tried to grasp a star, overreached, and fell."

— Jon Connington's POV, `adwd-the-griffin-reborn-01.md:55`

**Jaime's corroborating account (book-cite upgrade for battle-of-the-bells node):**
> "After dancing griffins lost the Battle of the Bells, Aerys exiled him. He had finally realized that Robert was no mere outlaw lord to be crushed at whim, but the greatest threat House Targaryen had faced since Daemon Blackfyre."

— `asos-jaime-05.md:53`

---

## Section 2 — ROLE EDGES

### On NODE-1: `knight-of-the-laughing-tree-incident`

**EDGE R-1**
- Type: `SUB_BEAT_OF`
- Source → Target: `knight-of-the-laughing-tree-incident` → `tourney-at-harrenhal`
- Evidence: `asos-bran-02.md:213` ("the mystery knight appeared in the lists")
- Quote: "But late on the afternoon of that second day, as the shadows grew long, a mystery knight appeared in the lists."
- Tier: 1
- Rationale: The incident is embedded within the tournament's days of jousting.
- Dedup: NEW (no SUB_BEAT_OF edge from this slug exists)

**EDGE R-2**
- Type: `FIGHTS_IN`
- Source → Target: `knight-of-the-laughing-tree` → `knight-of-the-laughing-tree-incident`
- Evidence: `asos-bran-02.md:225`
- Quote: "Whoever he was, the old gods gave strength to his arm. The porcupine knight fell first, then the pitchfork knight, and lastly the knight of the two towers."
- Tier: 1
- Rationale: The mystery knight is the primary participant; this relocates the existing FIGHTS_IN `tourney-at-harrenhal` to the sub-beat (or supplements it — keep both; the character fought at the tourney AND in the incident specifically).
- Dedup: Currently `knight-of-the-laughing-tree FIGHTS_IN tourney-at-harrenhal` exists; this is a finer-grained companion edge to the incident node. NEW.

**EDGE R-3**
- Type: `AGENT_IN`
- Source → Target: `howland-reed` → `knight-of-the-laughing-tree-incident`
- Evidence: `asos-bran-02.md:179` (the squires beat the crannogman; his prayer is answered by the mystery knight)
- Quote: "The little crannogman was walking across the field, enjoying the warm spring day and harming none, when he was set upon by three squires. They were none older than fifteen, yet even so they were bigger than him, all three."
- Tier: 1
- Rationale: Howland Reed is the catalyzing victim whose beating leads to the incident; he is an agent/witness at minimum.
- Note: If vocab requires VICTIM_IN for the beaten party, that is preferred; but Howland survives and the incident is on his behalf — AGENT_IN is defensible.
- Dedup: NEW

**EDGE R-4**
- Type: `WITNESS_IN`
- Source → Target: `aerys-ii-targaryen` → `knight-of-the-laughing-tree-incident`
- Evidence: `asos-bran-02.md:229`
- Quote: "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree."
- Tier: 1
- Rationale: Aerys attended, became wroth, dispatched Rhaegar — his reaction is plot-load-bearing (establishes the king's paranoia sub-arc within the tourney).
- Dedup: NEW

**EDGE R-5**
- Type: `AGENT_IN`
- Source → Target: `rhaegar-targaryen` → `knight-of-the-laughing-tree-incident`
- Evidence: `asos-bran-02.md:229`
- Quote: "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree."
- Tier: 1
- Rationale: Rhaegar is sent to unmask the knight — an active agency; he found only the abandoned shield.
- Dedup: NEW

---

### On NODE-2: `exile-of-jon-connington`

**EDGE R-6**
- Type: `SUB_BEAT_OF`
- Source → Target: `exile-of-jon-connington` → `battle-of-the-bells`
- Evidence: `adwd-the-griffin-reborn-01.md:57`
- Quote: "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile…"
- Tier: 1
- Rationale: The exile is the direct consequence of losing the battle; it is a discrete decision-event SUB_BEAT following the battle.
- Dedup: NEW

**EDGE R-7**
- Type: `VICTIM_IN`
- Source → Target: `jon-connington` → `exile-of-jon-connington`
- Evidence: `adwd-the-griffin-reborn-01.md:57`
- Quote: "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion"
- Tier: 1
- Rationale: Connington is the subject on whom the exile is visited.
- Dedup: NEW

**EDGE R-8**
- Type: `COMMANDS_IN`
- Source → Target: `aerys-ii-targaryen` → `exile-of-jon-connington`
- Evidence: `adwd-the-griffin-reborn-01.md:57`
- Quote: "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion"
- Tier: 1
- Rationale: Aerys is the commanding actor who stripped Connington and sent him to exile.
- Dedup: NEW

---

### Wildfire-plot: role-edge enrichment (OVERLAY on existing node)

**EDGE R-9** (OVERLAY on `wildfire-plot`)
- Type: `AGENT_IN`
- Source → Target: `rossart` → `wildfire-plot`
- Evidence: `asos-jaime-05.md:55`
- Quote: "with Rossart, Belis, and Garigus coming and going night and day… Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer."
- Tier: 1
- Rationale: Rossart is the lead pyromancer organizing the cache placement; he is the primary human agent of the wildfire-plot itself (distinct from `aerys-commands-the-city-burned`, where Rossart is sent to carry the order). This edge lives on the *planning* node.
- Dedup: Rossart currently has only an incoming `KILLS ← jaime-lannister` edge; no AGENT_IN wildfire-plot. OVERLAY (new edge on existing node).

**EDGE R-10** (OVERLAY on `wildfire-plot`)
- Type: `COMMANDS_IN`
- Source → Target: `aerys-ii-targaryen` → `wildfire-plot`
- Evidence: `asos-jaime-05.md:53`
- Quote: "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself."
- Tier: 1
- Rationale: Aerys is the commanding authority who ordered the entire plot. Currently `wildfire-plot` has no incoming COMMANDS_IN or AGENT_IN edges despite Aerys being its architect.
- Dedup: OVERLAY (new edge on existing node).

---

## Section 3 — OVERLAYS (Bare-Node Depth / Book-Cite Upgrades)

### OVERLAY-1: `wildfire-plot` — book-cite upgrade + agent role edges

**What's missing:** The node's `## Edges` section lists only `FIGHTS_IN: Robert's Rebellion` (a junk/misparsed edge) and `DEFEATS: Jaime Lannister`. No role-bearing participants. The Quotes section already has wiki-sourced content but cites wiki-formatted refs, not navigable `chapter:line` cites.

**Proposed `## Book Citations` section addition:**
```
## Book Citations

### ASOS Jaime V (asos-jaime-05.md)

> So His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself.
— asos-jaime-05.md:53 (Jaime's bath-house confession to Brienne)

> The traitors want my city, I heard him tell Rossart, but I'll give them naught but ashes. Let Robert be king over charred bones and cooked meat. The Targaryens never bury their dead, they burn them. Aerys meant to have the greatest funeral pyre of them all.
— asos-jaime-05.md:57 (Aerys's words as recalled by Jaime; also cited in aerys-commands-the-city-burned node)

> When I came on Rossart, he was dressed as a common man-at-arms, hurrying to a postern gate. I slew him first. Then I slew Aerys, before he could find someone else to carry his message to the pyromancers.
— asos-jaime-05.md:63
```

**Tier of upgrade:** Tier-1 book provenance (from Tier-2 wiki cite_refs). High value per memory `feedback_book_citation_overlay_value`.

---

### OVERLAY-2: `battle-of-the-bells` — AGENT_IN / COMMANDS_IN edges + book-cite

**What's missing:** The node has a rich prose body (wiki-sourced) but zero role-bearing participant edges. Connington COMMANDED the royalist force; Robert emerged to fight. The Connington-exile beat is a direct consequence.

**Proposed role edges:**
- `jon-connington COMMANDS_IN battle-of-the-bells` — evidence: `asos-jaime-05.md:53` ("After dancing griffins lost the Battle of the Bells, Aerys exiled him") + `adwd-the-griffin-reborn-01.md:57` (full POV recall)
- `robert-baratheon AGENT_IN battle-of-the-bells` — evidence: `asos-tyrion-09.md` Harwin's account (source already captured in wiki node; `asos-jaime-05.md:53` also names him implicitly as the surviving rebel)

**Anchor quote for Connington COMMANDS_IN:**
> "After dancing griffins lost the Battle of the Bells, Aerys exiled him. He had finally realized that Robert was no mere outlaw lord to be crushed at whim, but the greatest threat House Targaryen had faced since Daemon Blackfyre."
— `asos-jaime-05.md:53`

**Note:** The wiki node has the Battle's prose narrative with full battle detail, including Connington wounding Hoster, killing Denys Arryn, and retreating. The book-cite upgrade path is from wiki-sourced narrative → navigable `chapter:line` anchor quotes. These are at `asos-jaime-05.md:53`, `adwd-the-griffin-reborn-01.md:55-57`, and `asos-tyrion-09.md` (Harwin's account line numbers should be verified separately).

---

### OVERLAY-3: `abduction-of-lyanna` — AGENT_IN + VICTIM_IN + description depth

**What's missing:** 2 edges total (CAUSES execution-of-brandon, incoming CAUSES from tourney). No AGENT_IN rhaegar-targaryen, no VICTIM_IN lyanna-stark. Also the aliases are kebab-style ("abduction-of-lyanna-stark") — flag for fix per memory `project_node_alias_spaced_phrases`.

**Proposed role edges:**
- `rhaegar-targaryen AGENT_IN abduction-of-lyanna`
  - Evidence: wiki:Robert's_Rebellion (primary, already in node prose) + `agot-eddard-15.md:45` (Ned's fever dream, Lyanna's name at the tourney crowning)
  - Quote: "Instead of crowning his wife, the Dornish princess Elia Martell, Rhaegar rode past her and crowned Lyanna Stark of Winterfell instead." — `agot-eddard-15.md:45` (this is the crowning that precedes the abduction; use as the chain anchor; the abduction itself has no direct eyewitness book quote)
  - Tier: 1 (abduction canon per all POV accounts)

- `lyanna-stark VICTIM_IN abduction-of-lyanna`
  - Evidence: same; the entire node's identity section asserts this
  - Tier: 1

**Alias fix (flag):**
- Current aliases: `["abduction-of-lyanna-stark", "rhaegar-takes-lyanna"]` — both kebab-style, will not match natural-language queries per resolver. Proposed replacements: "abduction of Lyanna Stark", "Rhaegar takes Lyanna". Flag for correction — NOT a node re-mint.

---

### OVERLAY-4: `battles-at-summerhall` — COMMANDS_IN + AGENT_IN

**What's missing:** 2 edges (PART_OF + PRECEDES). No participants. Robert won all three engagements here.

**Proposed role edges:**
- `robert-baratheon AGENT_IN battles-at-summerhall`
  - Evidence: wiki:Battles_at_Summerhall (in local cache `sources/wiki/_raw/Battles_at_Summerhall.json`); Jaime references these as Robert's campaign prior to the Trident in `asos-jaime-05.md` (indirect). Primary wiki cite.
  - Tier: 1 (well-attested; Robert is the victor at all three)

**Note:** No verbatim book quote directly names these three battles in a single navigable chapter. The wiki node already has the full narrative. The role-edge addition is the value here, not a quote upgrade. Book-cite upgrade is deferred until a chapter passage is found.

---

## Section 4 — OFF-VOCAB FLAGS

**None newly discovered.** The existing `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` edge (on rhaegar-targaryen → lyanna-stark, flagged in baseline.md) is pre-existing; not re-flagged here. No new edge types invented.

---

## Section 5 — THEORY GATING NOTE

**KotLT identity (who is the mystery knight):** The incident node (`knight-of-the-laughing-tree-incident`) is proposed at **tier-1** for the incident itself — it demonstrably occurred per Meera's account. The proposed role edges attach Howland Reed (AGENT_IN, as the catalyzing victim), Aerys (WITNESS_IN), and Rhaegar (AGENT_IN, sent to unmask) — all tier-1. The **identity** of the mystery knight is NOT proposed. The theories node `knight-of-the-laughing-tree-theories` handles that. Lens 2's SUSPECTED_OF edge (which will propose Lyanna Stark SUSPECTED_OF being the knight) should target the new incident node as its event reference.

---

## Dedup Summary Table

| Item | Type | Status |
|---|---|---|
| `murder-of-elia-martell-and-rhaegars-children` | Event node | ALREADY EXISTS — not re-proposed |
| `aerys-commands-the-city-burned` | Event node | ALREADY EXISTS — not re-proposed |
| `knight-of-the-laughing-tree-incident` | Event node | NEW |
| `exile-of-jon-connington` | Event node | NEW |
| Wildfire-plot COMMANDS_IN aerys + AGENT_IN rossart | Role edges | OVERLAY on existing node |
| Battle-of-the-bells COMMANDS_IN connington | Role edge | OVERLAY |
| Abduction-of-lyanna AGENT_IN rhaegar / VICTIM_IN lyanna | Role edges | OVERLAY |
| Abduction-of-lyanna alias fix (kebab → spaced phrases) | Schema fix | FLAG (not a node mint) |
| Battles-at-summerhall AGENT_IN robert | Role edge | OVERLAY |
| Wildfire-plot book-cite upgrade | Overlay | OVERLAY |
| Battle-of-the-bells book-cite upgrade | Overlay | OVERLAY |
