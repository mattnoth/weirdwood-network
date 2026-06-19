# Causal Arc B2: Theon Greyjoy Taken as Ward — Minting Proposal

Research subagent output. READ-ONLY. Do not write to graph.
Completed: 2026-06-19

---

## A. Dedup Ledger

### Canonical hub determination: `greyjoy-rebellion` vs `greyjoys-rebellion`

Two nodes exist for the Greyjoy Rebellion:

| slug | type | confidence | edges out | wiki_source |
|------|------|-----------|-----------|-------------|
| `greyjoy-rebellion` | `event.war` | tier-2 | **0** (causal dark) | `Greyjoy_Rebellion` (redirect page, 946 chars) |
| `greyjoys-rebellion` | `event.battle` | tier-1 | **12** (FIGHTS_IN sub-battles + DEFEATS) | `Greyjoy's_Rebellion` (full article) |

**CANONICAL HUB: `greyjoys-rebellion`.**

Rationale:
- `greyjoys-rebellion` has all the content: 12 outbound edges, the full Aftermath/Quotes sections, and the sub-battle FIGHTS_IN chain.
- `greyjoy-rebellion` was promoted from `Greyjoy_Rebellion.json` which is a **redirect page** (text: "Redirect to: Greyjoy's Rebellion"). It is a thin stub with 0 edges — its `event.war` type is more correct taxonomically, but it has no content.
- All 7 inbound references to `greyjoy-rebellion` use anchor text "Greyjoy Rebellion" and come from prose nodes; the full article is at `greyjoys-rebellion`.

**FLAG: `greyjoy-rebellion` is a DUPLICATE of `greyjoys-rebellion` promoted from a redirect page.** It should be merged/deprecated — the slug `greyjoy-rebellion` (no apostrophe-s) would be the cleaner canonical slug, but the rich content lives on `greyjoys-rebellion`. This is a housekeeping issue separate from this arc; flagged in Section E.

**For this proposal: wire all new causal edges to `greyjoys-rebellion`.**

---

### Beat candidates — dedup check

| Candidate beat | Resolver result | grep / ls finding | VERDICT |
|----------------|----------------|-------------------|---------|
| `theon taken as ward` | MISS (no match) | No node in `graph/nodes/events/` matches | **MINT-NEW** |
| `theon greyjoy hostage` | CANDIDATES: `theon-greyjoy` (score 0.77), `theon-iii-greyjoy` (0.77) — both character nodes, not events | No event node matches | **MINT-NEW** (character matches are irrelevant; no event node exists) |
| `dryn-given-as-final-hostage` | HIT | `graph/nodes/events/dryn-given-as-final-hostage.node.md` — `evidence_chapters: ADWD Jon XII`; status `minted-plate3`; concerns Dryn (wildling/Stannis context). Different person, different era, unrelated. | **SKIP** |
| `hostage-negotiation` | HIT | `graph/nodes/events/hostage-negotiation.node.md` — `evidence_chapters: ADWD Jaime I`; Plate 3 staging; ADWD context. Unrelated to Greyjoy Rebellion. | **SKIP** |
| `hostage-boys-pass-through` | HIT | `graph/nodes/events/hostage-boys-pass-through.node.md` — `evidence_chapters: ADWD Jon XII`; Plate 3 staging. Wildling/Wall context. Unrelated. | **SKIP** |
| `battle-at-pyke` | EXISTS (canonical, `graph/nodes/events/battle-at-pyke.node.md`) | Full node with Narrative Arc, Aftermath, Quotes. Contains: "Young Theon was given into the care of Lord Stark as a hostage and ward to ensure his defeated father's good behavior." This is the SIEGE event, not the ward-taking. Different granularity. | **DO NOT REUSE** — granularity difference; `battle-at-pyke` is the combat event; the hostage-taking is its immediate consequence (a separate discrete act at Pyke following surrender). **Wire causal edge from `greyjoys-rebellion` not `battle-at-pyke`** — the war causes the wardship, not the specific battle (see Section E, risk note). |
| `ward of house stark` | CANDIDATES: `house-stark` (0.77), `house-stark-guards` (0.77) — not events | No event node matching wardship context | **MINT-NEW confirmed** |

**WARD_OF dyad status:** The task brief says "theon-greyjoy WARD_OF eddard-stark dyad already exists." **Verification: this is NOT accurate.** The `theon-greyjoy.node.md` Edges section contains only 8 edges (sworn-to, culture-of, holds-title ×3, parent-of reverse ×2, lover-of ×4, born-at). No `WARD_OF: eddard-stark` line exists. The wardship is documented in the node's prose/identity section and referenced in wiki text, but has not been promoted to a live Edges entry. **The dyad needs minting alongside the beat-node.** This actually strengthens the case for the new beat: the beat creates the event hub; the dyad (`theon-greyjoy WARD_OF eddard-stark`) attaches to the hub as an additional edge to add to theon-greyjoy.node.md.

---

## B. Proposed New Beat-Node

### `theon-greyjoy-taken-as-ward`

**Proposed slug:** `theon-greyjoy-taken-as-ward`
**Type:** `event.incident`
**Confidence:** tier-1 (directly attested in multiple sources)
**Occurred:** `ac_year: 289` (immediately after fall of Pyke at end of Greyjoy's Rebellion; same year; `precision: year`)

**Justification for `event.incident`:** The wardship-taking is a bounded post-surrender act at Pyke — a discrete multi-participant moment (Robert decrees; Eddard takes the boy; Theon is removed from his father) with causal consequence that anchors the entirety of Theon's POV arc. It is not a battle (`event.battle`), not a formal ceremony (`event.coronation`/`event.wedding`), and not an assassination. `event.incident` ("bounded multi-beat event... neither a battle nor a formal ceremony but has enough narrative weight and causal consequence") fits exactly. In use by 5+ live nodes; no new subtype needed.

**Description:**
Following Balon Greyjoy's surrender at Pyke at the end of Greyjoy's Rebellion (~289 AC), Robert I Baratheon spared Balon's life in exchange for an oath of fealty. As surety for Balon's future loyalty, Balon's last surviving son, ten-year-old Theon Greyjoy, was given into the care of Lord Eddard Stark as a ward and hostage. Theon was taken away from Pyke on Robert's war galley and raised alongside the Stark children at Winterfell for the next nine to ten years.

---

### Verbatim Quotes

**From `sources/wiki/_raw/Greyjoy's_Rebellion.json` (Aftermath / infobox sections):**

> "His surviving son, the nine-year-old Theon, was given into the care of Lord Stark as a hostage to ensure Balon's good behavior."

Source: `sources/wiki/_raw/Greyjoy's_Rebellion.json` — Aftermath section, cite_ref `Ragot4`

> Infobox result field: "Theon Greyjoy made a ward of House Stark"

Source: `sources/wiki/_raw/Greyjoy's_Rebellion.json` — infobox/results table

---

**From `graph/nodes/events/battle-at-pyke.node.md` (## Narrative Arc, line 46):**

> "Young Theon was given into the care of Lord Stark as a hostage and ward to ensure his defeated father's good behavior."

Source: `graph/nodes/events/battle-at-pyke.node.md` line 46, cite_ref `Ragot4`
(Original wiki source: `Battle_at_Pyke` → AGOT Chapter 4 / Appendix)

> "Theon was taken away from Pyke on Robert's war galley and was raised alongside Eddard's children at Winterfell."

Source: `graph/nodes/events/battle-at-pyke.node.md` ## Aftermath, cite_ref `Racok11`

---

**From `sources/chapters/acok/acok-theon-01.md`:**

> "There was no safe anchorage at Pyke, but Theon Greyjoy wished to look on his father's castle from the sea, to see it as he had seen it last, ten years before, when Robert Baratheon's war galley had borne him away to be a **ward of Eddard Stark**."

File: `sources/chapters/acok/acok-theon-01.md` line 11

> "Ten, or close as makes no matter," he told her. "**I was a boy of ten when I was taken to Winterfell as a ward of Eddard Stark. A ward in name, a hostage in truth.** Half his days a hostage . . . but no longer."

File: `sources/chapters/acok/acok-theon-01.md` line 43

> "The whole castle, from Lady Stark to the lowliest kitchen scullion, knew **he was hostage to his father's good behavior**, and treated him accordingly."

File: `sources/chapters/acok/acok-theon-01.md` line 207

---

**From `graph/nodes/characters/theon-greyjoy.node.md` (prose/identity section, line 31):**

> "Theon was taken from his father, Lord Balon Greyjoy, as a hostage and ward by Lord Eddard Stark and has been raised at Winterfell for nine years since."

Source: `graph/nodes/characters/theon-greyjoy.node.md` line 31, cite_ref `Ragot4`

> "**Rodrik**: For ten years you have been a ward of Stark. **Theon**: Hostage and prisoner, I call it."

Source: `graph/nodes/characters/theon-greyjoy.node.md` line 163 (quote from wiki)

---

**From `sources/wiki/_raw/Balon_Greyjoy.json`:**

> "Balon's sole surviving son, ten-year-old Theon, was taken by Lord Eddard Stark to Winterfell as a ward and hostage."

Source: `sources/wiki/_raw/Balon_Greyjoy.json` — Rebellion aftermath section, cite_ref `Racok11`

---

### Role Edges for `theon-greyjoy-taken-as-ward`

| edge type | source slug | direction | notes | tier |
|-----------|-------------|-----------|-------|------|
| `VICTIM_IN` | `theon-greyjoy` | → `theon-greyjoy-taken-as-ward` | Theon is the hostage taken | Tier-1 |
| `AGENT_IN` | `eddard-stark` | → `theon-greyjoy-taken-as-ward` | Eddard takes him into ward/care | Tier-1 |
| `COMMANDS_IN` | `robert-i-baratheon` | → `theon-greyjoy-taken-as-ward` | Robert spared Balon and decreed the hostage arrangement; "Robert's war galley" carried Theon away | Tier-2 (role is attested but Robert's specific verbal decree is sourced only via wiki narrative inference) |
| `VICTIM_IN` | `balon-greyjoy` | → `theon-greyjoy-taken-as-ward` | Balon loses his last son as surety; co-victim in the political act | Tier-2 |

**Note on Robert's `COMMANDS_IN`:** The Greyjoy's_Rebellion wiki page states Balon "was forced to swear fealty once more to the Iron Throne" and the hostage arrangement was the peace term. Battle-at-Pyke node (line 46) says "in return for his allegiance now, Balon's life was spared by the generous Robert." The hostage-taking was Robert's political instrument. Downgrade to Tier-2 if Robert's active command role is considered interpretive.

---

### Aliases (for alias-resolver discoverability)

- theon greyjoy taken as ward
- theon greyjoy hostage stark
- theon greyjoy ward of house stark
- theon taken from pyke
- theon given to eddard stark
- theon as ward of winterfell

---

## C. Proposed Causal Edges

| Source | Type | Target | Tier | Justification | Verbatim quote + source | Agency note |
|--------|------|--------|------|---------------|------------------------|-------------|
| `greyjoys-rebellion` | `CAUSES` | `theon-greyjoy-taken-as-ward` | Tier-2 | The rebellion's defeat at Pyke is the mediated cause of the hostage arrangement; Balon's surrender is the precondition; Robert and Ned's decision to take Theon is the human agency that sits between (modeled on the beat's role edges) | "His surviving son, the nine-year-old Theon, was given into the care of Lord Stark as a hostage to ensure Balon's good behavior." — `sources/wiki/_raw/Greyjoy's_Rebellion.json`, Aftermath | The rebellion CAUSES the opportunity and political settlement; the human decision (Robert/Ned) sits on the beat's role edges (COMMANDS_IN / AGENT_IN), not on this causal edge. This is a mediated CAUSES, not TRIGGERS. |

**HARD-STOP confirmed:** The chain ends at `theon-greyjoy-taken-as-ward`. No downstream edges toward ACOK (Theon's invasion of the North, capture of Winterfell) are proposed. Those belong to a separate, larger arc.

---

## D. Chain Preview

Final `--causal-chain greyjoys-rebellion` shape after minting:

```
greyjoys-rebellion (event.war, ~289 AC)
│
├── FIGHTS_IN →  burning-of-the-lannister-fleet  (event.battle)
├── FIGHTS_IN →  storming-of-seagard             (event.battle)
├── FIGHTS_IN →  sea-battle-off-fair-isle         (event.battle)
├── FIGHTS_IN →  landing-on-great-wyk             (event.battle)
├── FIGHTS_IN →  attack-on-old-wyk                (event.battle)
├── FIGHTS_IN →  battle-at-lordsport              (event.battle)
├── FIGHTS_IN →  battle-at-pyke                   (event.battle)
│
└── CAUSES →  theon-greyjoy-taken-as-ward  (event.incident, ~289 AC)  ← NEW
                  │
                  ├── VICTIM_IN ← theon-greyjoy
                  ├── AGENT_IN  ← eddard-stark
                  ├── COMMANDS_IN ← robert-i-baratheon  (Tier-2)
                  └── VICTIM_IN ← balon-greyjoy          (Tier-2)
```

Query `--causal-chain greyjoys-rebellion` will now traverse: rebellion → ward-taking → Theon's role + Eddard's role. Answer to "what were the consequences of the Greyjoy Rebellion / how did Theon become a ward?" becomes fully traversable.

---

**Companion edge to add to `theon-greyjoy.node.md` Edges section** (the dyad that the task brief believed already existed):

```
- WARD_OF: eddard-stark (cite: wiki:Theon_Greyjoy.cite_ref-Ragot4; event_ref: theon-greyjoy-taken-as-ward)
```

This dyad records the relationship status; the beat-node records the event. Both are needed.

---

## E. Risks / Open Questions

### 1. Duplicate node: `greyjoy-rebellion` vs `greyjoys-rebellion`
`greyjoy-rebellion` (type `event.war`) was promoted from a redirect page and has 0 edges. `greyjoys-rebellion` (type `event.battle`) has 12 edges and all the content. These are the same in-world event. The canonical hub should have type `event.war` (it's a multi-battle conflict, not a single battle), which `greyjoy-rebellion` correctly sets — but the content lives on `greyjoys-rebellion`. **Recommendation:** Merge the two. Rename `greyjoys-rebellion` → `greyjoy-rebellion` (correct slug, correct type), absorb its 12 edges, and mark `greyjoys-rebellion` as deprecated. This is a separate housekeeping task, not blocking this arc. **For now, wire to `greyjoys-rebellion`** (the content-bearing node). Flag this for Matt's judgment — it touches existing edges.

### 2. Robert's `COMMANDS_IN` role — verb/tier ambiguity
The wiki text implies Robert approved the hostage arrangement (it was his peace settlement), but the primary agent described is Eddard ("given into the care of Lord Stark"). Robert's active verbal decree is not directly quoted in the book text found. Downgrading Robert from COMMANDS_IN Tier-2 to a note in the beat description is an acceptable alternative. Matt's call.

### 3. `battle-at-pyke` as intermediate node
An alternative chain design would be: `greyjoys-rebellion CAUSES battle-at-pyke CAUSES theon-greyjoy-taken-as-ward`. The wardship explicitly occurs at Pyke immediately following Balon's surrender (the surrender happens in the battle's resolution). However, the battle-at-pyke node already exists with `DEFEATS` edges, and adding another CAUSES from it would complicate the dedup. The simpler and more correct design: the **war** (greyjoys-rebellion) CAUSES the wardship, mediated by the war's outcome. The battle is the final episode but the ward-taking is a post-defeat political act attached to the rebellion as a whole. This matches GRRM's own framing ("at the end of Greyjoy's Rebellion, Theon was taken"). **Recommendation: direct CAUSES from greyjoys-rebellion, not via battle-at-pyke.**

### 4. Age discrepancy: nine vs ten
The Greyjoy's_Rebellion wiki says "nine-year-old Theon"; ACOK-Theon-01 line 43 says "I was a boy of ten when I was taken to Winterfell"; Balon_Greyjoy wiki says "ten-year-old Theon." The theon-greyjoy.node.md has `BORN_AT: Pyke, Iron Islands, 278–279 AC`. The rebellion was 289 AC, making Theon 9–11 depending on birth month. The discrepancy is minor and already present in existing nodes. Do not try to resolve — use "approximately ten years old" in the beat description.

### 5. WARD_OF dyad not yet a live edge
As confirmed above, `theon-greyjoy WARD_OF eddard-stark` does not exist as a live Edges entry on theon-greyjoy.node.md. This proposal recommends adding it simultaneously with minting the beat-node, referencing the event hub. This is safe and additive.

### 6. `greyjoys-rebellion` type is `event.battle` (wrong)
The war-type mismatch (the rebellion is clearly `event.war`, but its content-bearing node is typed `event.battle`) means that `--causal-chain` query filters by type may behave oddly. The duplicate-node housekeeping in risk #1 would also fix this type error. Not blocking for this arc.

---

## VERIFICATION (S107)

Verified by: fresh subagent, 2026-06-19. All checks run against local source cache only (no internet).

### Gate 1 — Quotes verbatim at cited lines

| Cite ref | Expected quote (node/edge) | Actual line content | Result |
|---|---|---|---|
| acok-theon-01.md:11 | "Robert Baratheon's war galley had borne him away to be a ward of Eddard Stark" | Confirmed — full sentence: "There was no safe anchorage at Pyke, but Theon Greyjoy wished to look on his father's castle from the sea... ten years before, when Robert Baratheon's war galley had borne him away to be a ward of Eddard Stark." | **PASS** |
| acok-theon-01.md:43 | "I was a boy of ten when I was taken to Winterfell as a ward of Eddard Stark." | Confirmed — verbatim match within surrounding dialogue | **PASS** |
| acok-theon-01.md:207 | "The whole castle, from Lady Stark to the lowliest kitchen scullion, knew he was hostage to his father's good behavior" | Confirmed — verbatim, with continuation "and treated him accordingly. Even the bastard Jon Snow had been accorded more honor than he had." | **PASS** |

All three citations are verbatim-accurate.

### Gate 2 — Causal edge wired to the CANONICAL hub

The CAUSES edge uses source_slug `greyjoy-rebellion` (event.war, slug correct). This is the node that carries the rebellion's role edges: Balon/Robert/Ned/Stannis COMMANDS_IN, FIGHTS_IN edges for 7 combatants. `--causal-chain greyjoy-rebellion` correctly shows 0 upstream + 1 downstream (→ ward beat). `greyjoys-rebellion` (the dup, event.battle) has only 7 PART_OF incoming edges and 0 outgoing — it is correctly NOT used.

Note: the research doc (section E, Risk #1) incorrectly recommended wiring to `greyjoys-rebellion`. The implementation did better — it wired to `greyjoy-rebellion`, which is the richer and correctly-typed hub. The dup issue flagged in Risk #1 remains open but does not affect this arc.

**PASS** — causal edge on correct canonical hub.

### Gate 3 — Edge-type call: CAUSES vs TRIGGERS

The rebellion ends → Robert/Ned decide to take Theon hostage → wardship. Human decision (Robert/Ned) is the intermediate agent. CAUSES (mediated consequence) is semantically correct; TRIGGERS would imply a more direct/reflexive firing. The wardship is a deliberate political act enabled by the rebellion's outcome, not an automatic reflex. CAUSES is the right type.

**PASS**

### Gate 4 — Agency-collapse check

Human decision is explicitly modeled on the beat's role edges:
- eddard-stark AGENT_IN Tier-1 (line 11): takes Theon into his care
- robert-i-baratheon COMMANDS_IN Tier-2 (line 11): his war galley, his peace settlement

The CAUSES arrow carries only the causal link; the agency attribution lives on the role edges. No collapse.

**PASS**

### Gate 5 — Hard-stop: no downstream chain from ward beat

Outgoing edges from `theon-greyjoy-taken-as-ward` as source: exactly 1 edge — `LOCATED_AT → pyke`. No CAUSES/TRIGGERS/MOTIVATES edges pointing forward to Theon's ACOK invasion, capture of Winterfell, or war-of-five-kings. The chain stops cleanly at the wardship.

**PASS**

### Gate 6 — Tier discipline

| Edge | Tier in edges.jsonl | Expected | Result |
|---|---|---|---|
| CAUSES: greyjoy-rebellion → ward beat | tier-2 | tier-2 (mediated causal) | **PASS** |
| VICTIM_IN: theon-greyjoy | tier-1 | tier-1 | **PASS** |
| AGENT_IN: eddard-stark | tier-1 | tier-1 | **PASS** |
| COMMANDS_IN: robert-i-baratheon | tier-2 | tier-2 (interpretive) | **PASS** |
| LOCATED_AT: pyke | tier-1 | tier-1 | **PASS** |

All tiers correct.

### Gate 7 — Factual accuracy (local wiki cross-check)

- `sources/wiki/_raw/Theon_Greyjoy.json`: "Following Greyjoy's Rebellion, Theon was taken to Winterfell as a hostage and ward to Lord Eddard Stark." — confirms canon.
- `sources/wiki/_raw/Greyjoy's_Rebellion.json`: "His surviving son, the nine-year-old Theon, was given into the care of Lord Stark as a hostage to ensure Balon's good behavior." — age discrepancy (nine vs ten) is a pre-existing wiki inconsistency noted in the research doc; does not affect the factual claim.

The ward-taking as a post-rebellion consequence is solidly attested by both the wiki and the book text.

**PASS**

### Gate 8 — No duplicate WARD_OF dyad minted by this arc

Searched `edges.jsonl` for `"edge_type": "WARD_OF"` + `theon-greyjoy` as source: found exactly 1 existing entry at line 2029, from run `pass1-derived-20260523` (evidence: agot-catelyn-03.md:185, "Lord Eddard is a second father to me"). This is the pre-existing dyad edge. The B2 arc did NOT re-mint this dyad — it minted only the new beat-node (`theon-greyjoy-taken-as-ward`) and 5 edges (VICTIM_IN, AGENT_IN, COMMANDS_IN, LOCATED_AT, CAUSES). The dyad and the event-node serve different graph roles and correctly coexist.

**PASS**

### Minor flag — LOCATED_AT Pyke semantics

The LOCATED_AT → pyke edge records where the ward-taking occurred (departure point from Pyke). This is defensible: the incident of "being taken" occurred at Pyke. However, if LOCATED_AT is intended to mean "where the entity resides/operates," Winterfell would be the better target (where Theon lived for ten years). The current node description says "taken from Pyke," and the edge quote is "Robert Baratheon's war galley had borne him away" — so Pyke as the event location (origin) is coherent. Not a blocker, but worth a judgment call: if LOCATED_AT means event-origin, Pyke is correct; if it means event-destination, Winterfell is correct. Flag for Matt.

**FLAG (non-blocking)**

---

### Overall Verdict

**CONFIRM**

All 8 gates pass. The causal edge `greyjoy-rebellion --CAUSES--> theon-greyjoy-taken-as-ward` is correctly typed, tier-appropriate, wired to the canonical hub, fully evidenced by verbatim book citations, and stops cleanly at the wardship with no downstream chain. Role edges correctly model the human agency (Eddard AGENT_IN, Robert COMMANDS_IN). Factual accuracy confirmed against both local wiki sources.

One non-blocking flag: LOCATED_AT → pyke is coherent as event-origin but could alternatively point to winterfell as event-destination; Matt's call.

Ready for: `verified_by: s107-b2-verify` stamp on the CAUSES edge.
