# Fresh Arc Dip — 2026-06-20 (S111 pre-build)

> **Purpose:** Re-confirm the S109 fumble re-ranking after S110's harvest pass. Verify all
> previously-built arcs still pass on control questions, re-grade the known fumbles, and
> confirm whether Q12 (Battle of the Blackwater) remains #1. Read-only grading against
> LOCAL graph + wiki cache only — no internet fetches.

---

## Graph Health (at dip time)

```
GRAPH HEALTH REPORT
  Node files (*.node.md)  :   8,546
  Edge count              :  22,273
  Unique edge endpoints   :   6,006
  Orphan endpoints        :      62
  Causal edge types       :  CAUSES (22) · TRIGGERS (10) · MOTIVATES (5) = 37 causal
```

Delta from S109 dip: +4 nodes, +18 edges, +6 causal (the Q14 Tywin arc shipped last session).

---

## Tally

| Grade | Count | Questions |
|-------|-------|-----------|
| correct | 3 | Control-A (Tyrion trial), Control-B (Roberts Rebellion), Control-C (Tywin death) |
| correct-to-stop-short | 0 | — |
| partial | 4 | Q5, Q6, Q13, Q11 (upgraded from failed — alias now resolves) |
| failed | 1 | Q12 (0 causal edges, confirmed) |

**Total: 7 probes. 3 correct · 4 partial · 1 failed.**

---

## Control Questions

---

### Control-A — "What led to Tyrion's trial?" → `trial-of-tyrion-lannister`

**Alias:** `trial-of-tyrion-lannister` — not tested (slug is unambiguous).

**Graph output:**
```
UPSTREAM — (3 edges)
    sansa-receives-the-poisoned-hairnet --[CAUSES]--> death-of-joffrey-baratheon
  death-of-joffrey-baratheon --[TRIGGERS]--> tyrion-accused-of-poisoning-joffrey
tyrion-accused-of-poisoning-joffrey --[CAUSES]--> trial-of-tyrion-lannister

DOWNSTREAM — (6 edges)
  trial → gregor-confesses-and-kills-oberyn → jaime-frees-tyrion → jaime-reveals-the-truth-of-tysha
    → assassination-of-tywin-lannister
    → tyrion-kills-shae-in-tywins-bed
    → tyrion-lannister [MOTIVATES]
```

**Grade: correct.** 3 upstream + 6 downstream = 9 causal edges. Arc is intact; the Tywin
chain (Q14, shipped S109) extends cleanly downstream. No regression.

---

### Control-B — "What set Robert's Rebellion in motion?" → `roberts-rebellion`

**Alias:** `roberts-rebellion` — HIT.

**Graph output:**
```
UPSTREAM — (4 edges)
      tourney-at-harrenhal --[CAUSES]--> abduction-of-lyanna
    abduction-of-lyanna --[CAUSES]--> execution-of-brandon-and-rickard-stark
  execution-of-brandon-and-rickard-stark --[TRIGGERS]--> aerys-demands-ned-and-robert
aerys-demands-ned-and-robert --[TRIGGERS]--> roberts-rebellion

DOWNSTREAM — (0 edges)
```

**Grade: correct.** 4-beat upstream chain intact; downstream causal-dark by policy (sub-battles
are PART_OF, not CAUSES). No regression.

---

### Control-C — "What were the consequences of Tywin's death?" → `assassination-of-tywin-lannister`

**Alias lookup (was the critical double-failure in S109):**
- "death of Tywin" → `assassination-of-tywin-lannister` — HIT ✓
- "Tyrion kills Tywin" → `assassination-of-tywin-lannister` — HIT ✓

**Graph output:**
```
UPSTREAM — (7 edges)
  sansa-receives-the-poisoned-hairnet → death-of-joffrey → tyrion-accused → trial-of-tyrion
  → gregor-confesses-and-kills-oberyn → jaime-frees-tyrion → jaime-reveals-the-truth-of-tysha
  → assassination-of-tywin-lannister

DOWNSTREAM — (0 edges)
```

**Grade: correct.** Q14 remains fixed: alias resolved (both natural phrases), 7-edge upstream
chain intact. Downstream is correctly empty (Cersei-regent / Tommen-reign nodes don't exist;
a long-distance ASOS→ADWD CAUSES would overclaim). No regression.

---

## Queue Questions

---

### Q12 — Consequences of the Battle of the Blackwater (presumed #1)

**Alias lookup:** `battle-of-the-blackwater` — HIT.

**Graph output:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors (non-causal):
  OUTGOING: PART_OF war-of-the-five-kings | PRECEDES battle-outside-the-gates-of-winterfell
  INCOMING: DIED_AT × 2 | PRECEDES fall-of-harrenhal | SUB_BEAT_OF × 2
```

**Grade: failed.** Confirmed 0 causal edges upstream or downstream. No change from S109.

**Downstream beats verified against node content + wiki cache:**

The `battle-of-the-blackwater.node.md` ## Aftermath section is rich — it documents:
1. **Stannis retreats to Dragonstone** with a fraction of his army — his threat to King's Landing
   removed for years. (No downstream event node for "Stannis retreats to Dragonstone" exists.)
2. **Joffrey sets Sansa aside and agrees to wed Margaery** — node
   `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` EXISTS but has 0 causal edges.
   The node's INCOMING edges are all role edges (AGENT_IN/COMMANDS_IN/VICTIM_IN), not causal.
3. **Tywin named Savior of the City and resumes as Hand of the King** — no event node for this
   moment exists (no `tywin-resumes-as-hand` or similar).
4. **Lannister-Tyrell alliance cemented** — no event node for the alliance exists; the
   `joffrey-sets-sansa-aside` node IS the concrete expression of this alliance, so an explicit
   alliance node is probably not needed as an intermediate step.

**Agency-collapse analysis for proposed edges:**

The key question: does `battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` collapse agency? Strictly: the small council (Tywin, Petyr Baelish) brokered
the Tyrell deal before and during the battle — Littlefinger traveled to Bitterbridge (per
the node's ## Origins section) to win Tyrell allegiance, and the throne room ceremony was
Garlan Tyrell (COMMANDS_IN) publicly making the proposal. But the battle's outcome is what
made the deal real and possible: the relief force arrived, the city was saved, the Tyrells
proved their worth, and the throne room ceremony followed. The causal chain is:

> battle → Lannister-Tyrell alliance proven in blood → small council + Tywin greenlight
> Garlan's proposal → Joffrey fakes unwillingness → ceremony

This is a mediated CAUSES (a person's decision sits between A and B), which is the correct
use of CAUSES rather than TRIGGERS. TRIGGERS = immediate specific spark. MOTIVATES = event
→ actor. The Sansa-aside ceremony is the direct observable outcome of the alliance, and the
alliance is the direct outcome of the battle, so `battle CAUSES joffrey-sets-sansa-aside`
is a valid mediated causal chain. No agency-collapse flag needed — CAUSES is the right type
precisely because it allows mediated causation.

**Proposed edges and node existence:**

| Proposed edge | Type | Targets exist? |
|---|---|---|
| `battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` | CAUSES | YES — node exists, 0 causal edges |
| `battle-of-the-blackwater CAUSES stannis-retreats-to-dragonstone` | CAUSES | NO — new node needed |
| `battle-of-the-blackwater CAUSES tywin-named-savior-and-resumes-as-hand` | CAUSES | NO — new node needed |

The cheapest meaningful addition is the first edge (cheap wiring, node exists). The
stannis-retreat and tywin-hand nodes are worth minting but each needs a new node. The
`joffrey-sets-sansa` wiring alone already makes the arc answerable.

**Scope estimate:** 1 edge (cheap wiring, node exists) to make Q12 answerable; +2 nodes
+2 edges for full coverage of the three most load-bearing downstream beats.

---

### Q11 — Daenerys / Fall of Astapor → Slaver's Bay campaign

**Alias lookups:**
- "fall of Astapor" → `fall-of-astapor` — HIT ✓
- "Daenerys conquest of Slaver's Bay" → NO CONFIDENT MATCH (top: `targaryen-campaign-in-slavers-bay` at 0.55 fuzzy, no confident single match) — alias gap persists.

**Graph output — fall-of-astapor:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF targaryen-campaign-in-slavers-bay (1 outgoing)
```

**Graph output — targaryen-campaign-in-slavers-bay:**
```
OUTGOING: (0 edges)
INCOMING: 7 × PART_OF (battle-near-yunkai, fall-of-astapor, etc.)
```

**Grade: partial** (upgraded from S109's "failed" — the alias for "fall of Astapor" now resolves
cleanly to a HIT; but "Daenerys conquest of Slaver's Bay" still misses, and structural causal
wiring is 0).

**What's missing confirmed against local wiki cache:**

The `targaryen-campaign-in-slavers-bay.node.md` ## Origins section confirms: Jorah convinces
Daenerys to divert from Pentos → Astapor to buy Unsullied. This is the upstream cause of the
whole Slaver's Bay campaign. The `fall-of-astapor.node.md` ## Aftermath confirms: Daenerys
leaves a council to rule; Cleon deposes it; siege of Astapor follows. These are real,
in-saga, arc-shaped beats. Downstream sub-battles (`battle-near-yunkai`, `siege-of-meereen`)
exist as PART_OF nodes with 0 causal wiring.

**Alias gap for campaign node:** `targaryen-campaign-in-slavers-bay` needs aliases like
"Daenerys conquest of Slaver's Bay" and "Dany's Essos campaign" to resolve on natural phrases.
The campaign node itself also has 0 causal upstream (what triggered the campaign) and 0
downstream (what it led to in Westeros terms — e.g., Daenerys returning to Westeros, though
that's ADWD scope).

**Scope estimate:** 1-2 alias additions + 2-3 beats + 3-5 edges. Larger than Q12 and requires
new beats.

---

### Q5 — Robb weds Jeyne Westerling upstream

**Alias lookup:** `robb-weds-jeyne-westerling` — HIT (top fuzzy candidate, resolves).

**Graph output:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (3 edges)
  robb-weds-jeyne-westerling --[TRIGGERS]--> red-wedding-conspiracy
  red-wedding-conspiracy --[CAUSES]--> red-wedding
  red-wedding-conspiracy --[CAUSES]--> robb-is-killed
```

**Grade: partial.** Downstream is correct (B1 arc intact). Upstream still 0 edges.

**Upstream verified against local wiki (storming-of-the-crag node):**

The `storming-of-the-crag.node.md` ## Aftermath section states verbatim: "Robb is nursed back
to health by Lady Jeyne Westerling. After hearing of the supposed deaths at Winterfell of his
brothers, Bran and Rickon, Robb deflowers Jeyne, and, to spare her dishonor, marries her
shortly thereafter." And the node includes the exact canonical quote from Robb explaining the
sequence (Catelyn: "And you wed her the next day.").

Node `storming-of-the-crag` EXISTS in the graph but has only:
- OUTGOING: PART_OF war-of-the-five-kings + **PRECEDES purple-wedding** (anomalous — a
  PRECEDES edge from the Crag storm to the Purple Wedding is a loose chronological link
  with no causal content; not a bug worth fixing here but noted)
- INCOMING: PRECEDES wedding-of-drogo-and-daenerys-targaryen (also anomalous)

The causal chain is: `storming-of-the-crag CAUSES robb-weds-jeyne-westerling` — mediated
by Robb's wounding + Jeyne nursing him + news of Bran/Rickon deaths + the deflowering that
leads to the honor-marriage. This is a single mediated CAUSES edge with the intermediate
steps suppressed to the sub-beat level. Alternatively with finer grain: `capture-of-winterfell
CAUSES robb-weds-jeyne-westerling` (the news is about Winterfell's capture) — but
`capture-of-winterfell` exists as a separate node (correctly referring to Theon's takeover,
not the news reaching Robb). The simplest clean arc: `storming-of-the-crag CAUSES
robb-weds-jeyne-westerling`.

**Scope estimate:** 1 edge (storming-of-the-crag already exists); optionally 1 sub-beat for
the Bran/Rickon news-of-deaths intermediate.

---

### Q6 — What caused the Battle of the Trident?

**Alias lookup:** `battle-of-the-trident` — HIT.

**Graph output:**
```
UPSTREAM — (0 edges — no causal antecedents)
DOWNSTREAM — (2 edges)
  battle-of-the-trident --[CAUSES]--> sack-of-kings-landing
  sack-of-kings-landing --[CAUSES]--> coronation-of-robert-i-baratheon
```

**Grade: partial.** Still 0 upstream edges — `roberts-rebellion CAUSES battle-of-the-trident`
edge not present. The Trident is the decisive battle OF the Rebellion; it was directly caused
by the Rebellion's escalation. Scope: 1 edge. Remains the known Step B refinement.

---

### Q13 — What led to Theon's Sack of Winterfell?

**Alias lookup:** `sack-of-winterfell` — HIT.

**Graph output — sack-of-winterfell:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF war-of-the-five-kings | PRECEDES purple-wedding | LOCATED_AT winterfell
```

**Graph output — capture-of-winterfell:**
```
OUTGOING: PART_OF war-of-the-five-kings | PRECEDES sack-of-winterfell
INCOMING: PRECEDES battle-outside-the-gates-of-winterfell | SUB_BEAT_OF (Rodrik+levies beat)
```

**Graph output — theon-greyjoy-taken-as-ward (B2 endpoint):**
```
UPSTREAM: greyjoy-rebellion --[CAUSES]--> theon-greyjoy-taken-as-ward
DOWNSTREAM: (0 edges)
```

**Grade: partial.** The B2 arc ends at `theon-greyjoy-taken-as-ward` (1 upstream edge), but
doesn't continue through to the Sack. Two edges would extend B2 to its logical conclusion:
`theon-greyjoy-taken-as-ward MOTIVATES capture-of-winterfell` (Theon's ward-history drives
his identity crisis and his decision to take Winterfell) and `capture-of-winterfell CAUSES
sack-of-winterfell` (the Bolton betrayal/Sack follows directly from the capture). The
`capture-of-winterfell` node exists and already has a PRECEDES sack-of-winterfell edge — the
PRECEDES is a temporal fact; the CAUSES would add the causal claim. The intermediate beat
(Theon decides to capture Winterfell after Balon sends him to raid rather than KL) is missing
as a node but could be collapsed into the MOTIVATES edge.

**Scope estimate:** 2 edges (both targets exist); optionally 1 intermediate beat node.

---

## Fumble Re-Ranking

### #1 — Q12: Battle of the Blackwater downstream (CONFIRMED #1)

**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | cheapest path ✓ | beats-mostly-exist PARTIAL

- Confirmed 0 causal edges — same as S109.
- `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` EXISTS and is causally unlinked.
  Adding `battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside…` is a single cheap-wiring
  edge that makes Q12 answerable without minting any new node.
- Two additional load-bearing beats (Stannis retreats, Tywin named Hand) each need a new
  node + edge, but are not blockers for the minimum viable fix.
- Agency: CAUSES is the correct type for mediated causation (battle → alliance → ceremony).
  No agency-collapse flag.
- **Minimum viable scope:** 1 edge, 0 new nodes. Full coverage: 2 new nodes + 3 edges.

**Recommended approach:** Wire the existing `joffrey-sets-sansa-aside` node first; then
dip again to decide if Stannis-retreat and Tywin-Hand nodes are worth building.

---

### #2 — Q5: Robb-Weds-Jeyne upstream (extends B1)

**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist YES (storming-of-the-crag exists) | scope MINIMAL

- 1 edge to wire: `storming-of-the-crag CAUSES robb-weds-jeyne-westerling`.
- Source node and target node both exist; wiki confirms the causal chain explicitly.
- CAUSES is correct type (mediated — wounding + nursing + news + dishonor → marriage).
- This extends the B1 Red Wedding upstream chain by one more step.
- Smaller scope than Q11; moved up from #4 (S109) because S109's #1 (Q14) is now built.
- **Scope:** 1 edge, 0 new nodes minimum; optional sub-beat for the news-of-Bran/Rickon.

---

### #3 — Q11: Daenerys / Fall of Astapor (new Essos territory)

**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | alias-gap on campaign node ✓ | beats-mostly-exist PARTIAL | scope MODERATE

- "Daenerys conquest of Slaver's Bay" still misses (alias gap on `targaryen-campaign-in-slavers-bay`).
- `fall-of-astapor` has 0 causal edges; sub-battles exist as PART_OF but are causally dark.
- Needs: alias additions to campaign node + 1-2 upstream beats (Jorah convinces Dany to
  divert to Astapor) + 2-3 downstream edges wiring sub-battles causally.
- Richer arc but more new work than #1 or #2.

---

### Known partials confirmed still-partial (lower priority)

- **Q6 (Battle of the Trident upstream):** Still 0 inbound CAUSES. `roberts-rebellion CAUSES
  battle-of-the-trident` is 1 edge. Trivially cheap but lower reader-demand than #1–#3.
- **Q13 (Sack of Winterfell / B2 extension):** 2 edges to add, both targets exist. Would
  complete the B2 arc's logical endpoint. Moderate priority.

---

## Agency-Collapse Flags (Q12 specific)

For each proposed Blackwater downstream edge:

**`battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside-and-agrees-to-wed-margaery`**
- Agency: Tywin + small council decided the Tyrell deal; Littlefinger brokered it at
  Bitterbridge; Garlan Tyrell proposed publicly in the throne room; Joffrey consented.
- Assessment: Multiple agency steps sit between A and B. CAUSES (mediated) is the correct
  type precisely for this pattern — "the battle created the conditions that led to the
  ceremony" is a textbook mediated CAUSES chain. No intermediate node is needed unless the
  alliance itself becomes a standalone query target.
- Flag: **CLEAR for CAUSES. No agency-collapse.**

**`battle-of-the-blackwater CAUSES stannis-retreats-to-dragonstone`** (if minted)
- Agency: Stannis decided to retreat. But his retreat was a direct and inevitable consequence
  of the battle's outcome (losing most of his fleet and army). No meaningful human decision
  stands between "lost the battle" and "retreats with survivors."
- Flag: **CLEAR for CAUSES. Borderline TRIGGERS** (the battle's outcome immediately caused
  the retreat, making TRIGGERS defensible), but CAUSES is also fine given the scale.

**`battle-of-the-blackwater CAUSES tywin-named-savior-and-resumes-as-hand`** (if minted)
- Agency: Joffrey/small council formally named Tywin Hand. But this was also a direct and
  planned consequence of the Lannister-Tyrell alliance.
- Flag: **CAUSES preferred** (mediated through formal court process). Could also be a separate
  beat: `joffrey-sets-sansa-aside CAUSES tywin-named-savior-and-resumes-as-hand` (Tywin
  got both rewards at the same throne room session). If only one edge is built, the Sansa-Margaery
  swap is more reader-load-bearing.

---

## Harvest Queue Additions

While reading the `battle-of-the-blackwater.node.md` ## Quotes section:

| open | quote | acok | acok-davos-03 / acok-tyrion-14 | "A wall of red-hot steel, blazing wood, and swirling green flame stretched before him. The mouth of the Blackwater Rush had turned into the mouth of hell." — Davos; load-bearing wildfire atmosphere | 2026-06-20 arc-dip |
| open | quote | acok | acok-sansa-08 | "Lord Renly! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat" — Dontos to Sansa; Garlan-as-Renly appearance detail; no quote on joffrey-sets-sansa-aside node yet | 2026-06-20 arc-dip |
| open | place | acos | asos-tyrion-01 | "My hirelings betray me, my friends are scourged and shamed, and I lie here rotting." — Tyrion's post-battle wound/recovery bitterness; atmosphere of the recovery period; could enrich battle-of-the-blackwater ## Quotes | 2026-06-20 arc-dip |
| open | food | asos | asos-daenerys-03 | "Dany let them argue, sipping the tart persimmon wine" — Daenerys's drink while concealing her Valyrian during negotiations in Astapor; beverage detail; fall-of-astapor node now has this via the node's ## Quotes | 2026-06-20 arc-dip |

---

## Summary Verdict

**The arc layer scores 3/7 correct · 4/7 partial · 1/7 failed on this dip.**

All three control questions (Tyrion trial, Robert's Rebellion, Tywin's death) pass cleanly —
no regressions from S109's builds. Q14's alias fix holds: "death of Tywin" and "Tyrion kills
Tywin" both resolve correctly.

**Q12 (Battle of the Blackwater) is confirmed #1 for the next build.** It is the only outright
FAILED question in the queue, has the cheapest path to an answer (one edge wiring an existing
node), and is a genuine reader-load-bearing question ("what did the Blackwater lead to?").

**Confirmed re-ranked queue (dip-driven):**
1. **Q12 — Battle of the Blackwater downstream** — 1 edge minimum (wire existing node),
   optionally +2 nodes +2 edges for Stannis retreat + Tywin Hand.
2. **Q5 — Robb-Weds-Jeyne upstream** — 1 edge (both source/target nodes exist, storming-of-the-crag confirmed).
3. **Q11 — Daenerys / Fall of Astapor** — new Essos territory; alias fix + 2-3 beats + 3-5 edges.
4. **Q13 — Sack of Winterfell (B2 extension)** — 2 edges, both targets exist.
5. **Q6 — Battle of the Trident upstream** — 1 edge (`roberts-rebellion CAUSES battle-of-the-trident`).

*Dip conducted: 2026-06-20. Session: S111. Model: claude-sonnet-4-6.*
*Sources consulted: `graph/nodes/events/battle-of-the-blackwater.node.md`,*
*`graph/nodes/events/joffrey-sets-sansa-aside-and-agrees-to-wed-margaery.node.md`,*
*`graph/nodes/events/storming-of-the-crag.node.md`,*
*`graph/nodes/events/fall-of-astapor.node.md`,*
*`graph/nodes/events/targaryen-campaign-in-slavers-bay.node.md`,*
*`graph/nodes/events/theon-greyjoy-taken-as-ward.node.md`,*
*`sources/wiki/_raw/Storming_of_the_Crag.json` (Crag aftermath + Robb/Jeyne chain)*

---

## POST-BUILD CONFIRMATION (S111, same session) — Q12 Blackwater downstream SHIPPED

The dip-confirmed #1 fumble (Q12) was built this session (dip-driven, one validating batch). After mint + fresh-subagent verify (all 3 CONFIRM):

- **2 new beat-nodes minted** (`event.incident`, Tier-1, `occurred.ac_year: 299`): `stannis-retreats-to-dragonstone` (ASOS Davos II grounding) + `tywin-named-savior-of-the-city` (ACOK Sansa VIII grounding). Both carry `## Quotes` with verified verbatim cites; aliases are natural SPACED phrases (resolver HIT on all tested phrasings).
- **3 causal Tier-2 CAUSES edges** wired from `battle-of-the-blackwater` (was 0 causal): → `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` (existing node) · → `stannis-retreats-to-dragonstone` · → `tywin-named-savior-of-the-city`. `evidence_kind: book-pass1`, `run_id: causal-arc-blackwater-20260620`, all `verified_by: subagent-local-source-check-2026-06-20`.
- **Smoke test:** `--causal-chain battle-of-the-blackwater` now returns 3 downstream CAUSES (was 0). All natural-phrase lookups for the new nodes HIT. Agency-collapse: verifier confirmed all 3 CLEAR for mediated CAUSES (edge 1's Tyrell-compact agency already carried by the existing `tywin-lannister COMMANDS_IN` role edge on the Sansa-aside node); no intermediate beat mandatory.
- Health: nodes 8,546 → 8,548; edges 22,273 → 22,276; orphans unchanged (62); pytest 1307 pass / 1 documented env-fail. Backup: `graph/edges/_regrounding/edges-pre-blackwater-arc-2026-06-20.jsonl`.
- **Q12 grade: failed → CORRECT.** Downstream-of-downstream (Stannis's northern gambit; Tommen's reign under Tywin-as-Hand) DEFERRED — would chain toward multi-attributed territory.

**Remaining re-ranked queue (dip-driven, NOT mass-mint — re-dip before building each):** #1 Q5 robb-weds-jeyne upstream (storming-of-the-crag CAUSES robb-weds-jeyne; both nodes exist per this dip — 1 edge) · #2 Q11 Daenerys/Slaver's-Bay (new Essos territory, alias fix + 2-3 beats + 3-5 edges) · #3 Q13 Sack-of-Winterfell (extends B2, 2 edges, targets exist) · Q6 Trident inbound CAUSES (1 edge).

*Build conducted: 2026-06-20. Session: S111. Orchestrator model: Opus 4.8; subagents (dip/research/verify): Sonnet 4.6.*
