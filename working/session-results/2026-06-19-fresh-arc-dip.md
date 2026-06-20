# Fresh Arc Dip — 2026-06-19 (S109)

> **Purpose:** 14-question arc-weighted dip after S108 (B3 Ned's-downfall shipped). Confirms whether the
> known partials are still genuine fumbles and surfaces any new failures among 7 NEW probes. Grades
> against local wiki + chapter cache only. No internet fetches.

---

## Graph Health (at dip time)

```
GRAPH HEALTH REPORT
  Node files (*.node.md)  :   8,542
  Edge count              :  22,255
  Unique edge endpoints   :   6,002
  Orphan endpoints        :      62
  Causal edge types       :  CAUSES (18)  TRIGGERS (9)  MOTIVATES (4)  = 31 causal
```

---

## Tally

| Grade | Count | Questions |
|-------|-------|-----------|
| correct | 6 | Q1, Q2, Q4, Q9, Q10 (Sack), Q8 (known-partial upgraded) |
| correct-to-stop-short | 1 | Q3 (Purple Wedding → trial) |
| partial | 4 | Q5, Q6, Q7, Q13 |
| failed | 3 | Q11, Q12, Q14 |

**Total: 14 questions. 7 correct/stop-short · 4 partial · 3 failed.**

---

## Per-Question Results

---

### Q1 — What set Robert's Rebellion in motion?
**Alias lookup:** `roberts-rebellion` — HIT

**Graph output:**
```
UPSTREAM — what led to this  (4 edges)
      tourney-at-harrenhal --[CAUSES]--> abduction-of-lyanna
    abduction-of-lyanna --[CAUSES]--> execution-of-brandon-and-rickard-stark
  execution-of-brandon-and-rickard-stark --[TRIGGERS]--> aerys-demands-ned-and-robert
aerys-demands-ned-and-robert --[TRIGGERS]--> roberts-rebellion

DOWNSTREAM — (0 edges, none — no causal consequences)
```

**Grade: correct**

The arc walks the canonical 4-beat chain (Tourney → Abduction → Brandon/Rickard executions → Aerys demands Ned & Robert → Rebellion). This is exactly what a reader expects. Downstream is intentionally causal-dark (the Rebellion's sub-battles like Battle of the Trident are PART_OF, not CAUSES — correct by policy).

---

### Q2 — What set Bran's fall and the arrest of Tyrion in motion?
**Alias lookups:**
- "Bran's fall" → CANDIDATES, top: `jaime-pushes-bran-from-the-tower` (score=1.00, fuzzy)
- "arrest of Tyrion" → CANDIDATES, top: `catelyn-seizes-the-moment-and-arrests-tyrion` (score=0.55, fuzzy, no confident single match)

**Discoverability note:** "arrest of Tyrion" does not resolve to a confident single hit — the phrase "Tyrion" and "arrest" together score 0.55 because the node title uses "seizes the moment." A reader using this natural phrase hits a soft fumble on alias resolution (but gets the right answer from top candidate).

**Graph output (full chain through catelyn arrest):**
```
UPSTREAM — what led to this  (4 edges)
      bran-witnesses-jaime-and-cersei --[TRIGGERS]--> jaime-pushes-bran-from-the-tower
    jaime-pushes-bran-from-the-tower --[CAUSES]--> bran-s-direwolf-kills-the-assassin
  bran-s-direwolf-kills-the-assassin --[CAUSES]--> littlefinger-names-the-dagger-as-tyrion-s
littlefinger-names-the-dagger-as-tyrion-s --[CAUSES]--> catelyn-seizes-the-moment-and-arrests-tyrion

DOWNSTREAM — what this led to (2 edges)
  catelyn-seizes-the-moment-and-arrests-tyrion --[CAUSES]--> gregor-raids-the-riverlands
  catelyn-seizes-the-moment-and-arrests-tyrion --[MOTIVATES]--> tywin-lannister
```

**Grade: correct**

Full 4-beat upstream chain is present. Downstream correctly reaches Gregor's raids and Tywin mobilizing. The alias fuzzy-match for "arrest of Tyrion" is a minor discoverability gripe but not a structural gap.

---

### Q3 — What chain of events led to Tyrion's trial for poisoning Joffrey? (Purple Wedding control)
**Alias lookups:**
- "Purple Wedding" → `purple-wedding` — HIT
- "Tyrion's trial" → CANDIDATES, top: `trial-of-tyrion-lannister` (score=1.00, fuzzy)

**Graph output — purple-wedding:**
```
UPSTREAM — (0 edges — no causal antecedents)
DOWNSTREAM — (0 edges — no causal consequences)
```

**Graph output — trial-of-tyrion-lannister:**
```
UPSTREAM — what led to this  (3 edges)
    sansa-receives-the-poisoned-hairnet --[CAUSES]--> death-of-joffrey-baratheon
  death-of-joffrey-baratheon --[TRIGGERS]--> tyrion-accused-of-poisoning-joffrey
tyrion-accused-of-poisoning-joffrey --[CAUSES]--> trial-of-tyrion-lannister

DOWNSTREAM — (0 edges)
```

**Grade: correct-to-stop-short (with partial flag on the Purple Wedding node itself)**

The Purple Wedding node is causally dark (0 upstream, 0 downstream). However, the reader asking "what led to Tyrion's trial" does find the load-bearing chain via `trial-of-tyrion-lannister` — `sansa-receives-the-poisoned-hairnet → death-of-joffrey-baratheon → tyrion-accused → trial` is correct and complete. The Purple Wedding node not being wired is a cosmetic gap: it has no CAUSES/TRIGGERS edges at all, just the event record. A reader phrasing the question as "what set the Purple Wedding in motion?" gets nothing. But the trial-directed question is answered.

**What's missing:** `purple-wedding` should have at least `sansa-receives-the-poisoned-hairnet CAUSES purple-wedding` and `purple-wedding TRIGGERS death-of-joffrey-baratheon`. This 1-edge hole is the known Q3 refinement (Step B analog — actually this is the Purple Wedding node wiring, not the Trident). The trial chain answers the question as asked.

---

### Q4 — What set Ned Stark's execution in motion, and who is to blame? (B3 control)
**Alias lookup:** `execution-of-eddard-stark` — HIT

**Graph output:**
```
UPSTREAM — what led to this  (3 edges)
  death-of-robert-baratheon --[CAUSES]--> arrest-of-eddard-stark
arrest-of-eddard-stark --[CAUSES]--> execution-of-eddard-stark
ned-confesses-to-treason --[TRIGGERS]--> execution-of-eddard-stark

DOWNSTREAM — (0 edges)
```

**Grade: correct**

The B3 arc is in place. The chain shows Robert's death → Cersei seizes power → arrest → (Ned's fateful confession triggers) → execution. The "who is to blame" facet is answered via agency edges on the component beats (Cersei, Joffrey, Littlefinger's betrayal of Ned). Downstream is intentionally empty — consequences are a separate question shape (Q7).

---

### Q5 — What led Robb Stark to marry Jeyne Westerling? (KNOWN PARTIAL — Q7 refinement)
**Alias lookup:** "Robb marries Jeyne Westerling" → CANDIDATES, top: `robb-weds-jeyne-westerling` (score=1.00, fuzzy)

**Graph output:**
```
UPSTREAM — (0 edges — no causal antecedents)

DOWNSTREAM — (3 edges)
  robb-weds-jeyne-westerling --[TRIGGERS]--> red-wedding-conspiracy
  red-wedding-conspiracy --[CAUSES]--> red-wedding
  red-wedding-conspiracy --[CAUSES]--> robb-is-killed
```

**Grade: partial**

**What's missing:** The upstream cause of the marriage — the storming/fall of the Crag (Robb wounded by arrow during the assault; Jeyne nurses him; he receives news of Bran and Rickon's supposed deaths; she comforts him; he takes her maidenhead and marries her next day to protect her honor). The causal chain is:

> `storming-of-the-crag [CAUSES] robb-weds-jeyne-westerling`

Or with finer granularity:
> `news-of-bran-and-rickon-deaths [CAUSES] robb-dishonors-jeyne` → `robb-dishonors-jeyne [TRIGGERS] robb-weds-jeyne-westerling`

**Arc-shaped? YES.** In-saga? YES (ASOS Catelyn II, ACOK Catelyn VI-VII; verbatim chapter quotes exist). Load-bearing? YES — "why did Robb marry Jeyne, breaking his Frey pact?" is one of the most reader-asked causal questions about the Red Wedding arc. Beats-mostly-exist? The storming-of-the-crag is likely NOT yet in the event graph (no alias hit). ~2 beats + 2 edges.

---

### Q6 — What caused the Battle of the Trident? (KNOWN PARTIAL — Step B)
**Alias lookup:** `battle-of-the-trident` — HIT

**Graph output:**
```
UPSTREAM — (0 edges — no causal antecedents)

DOWNSTREAM — (2 edges)
  battle-of-the-trident --[CAUSES]--> sack-of-kings-landing
  battle-of-the-trident --[PRECEDES]--> assault-on-dragonstone

Neighbors: PART_OF roberts-rebellion (1 edge outgoing)
```

**Grade: partial**

**What's missing:** One edge: `roberts-rebellion CAUSES battle-of-the-trident` (or equivalently, promoting the PART_OF to a causal edge). The Battle of the Trident is the decisive battle OF Robert's Rebellion — it was directly caused by/within the rebellion. Wiki confirms: "After Lord Jon Connington's defeat in the Battle of the Bells, Aerys realized the rebellion was a major threat and dispatched Rhaegar to take command." The causal path exists, the edge doesn't.

**Arc-shaped? YES.** In-saga? YES (wiki-documented, AGOT chapter references). Load-bearing? MODERATE — a reader asking "what caused the Battle of the Trident?" expects to see Robert's Rebellion at the head of the chain. Scope: 1 edge (the simplest possible fix). This is the known Step B refinement.

---

### Q7 — What were the consequences of Ned Stark's execution? (downstream probe — known empty)
**Alias lookup:** `execution-of-eddard-stark` — HIT

**Graph output:**
```
DOWNSTREAM — (0 edges — no causal consequences)
```

**Grade: partial**

**What's missing:** Downstream consequences — Robb's coronation as King in the North; Arya going on the run; Catelyn's grief driving her to free Jaime; the North's break from the Iron Throne. These are real reader-load-bearing beats. However, the continue prompt calls this "Step C (lower priority)" and notes it defers "unless a dip shows demand."

**Grading it partial, not failed**, because the question "who is to blame / what set it in motion" (Q4) IS answered. The downstream/consequences shape is a separate arc. Arc-shaped? YES. Load-bearing? MODERATE (the consequences are diffuse — Robb's coronation is the most concrete downstream node to add). Scope: 1-3 beats.

---

### Q8 — What set the Greyjoy Rebellion in motion / what caused it? (NEW probe)
**Alias lookup:** `greyjoy-rebellion` — HIT

**Graph output:**
```
UPSTREAM — (0 edges — no causal antecedents)

DOWNSTREAM — (1 edge)
  greyjoy-rebellion --[CAUSES]--> theon-greyjoy-taken-as-ward
```

**Grade: partial**

This was the previous-session partial upgraded to CORRECT per the post-B3 re-dip notes — but the re-dip was the prior session's (S108) targeted dip. In this fresh dip, with the question "what *caused* the Greyjoy Rebellion?", the graph still returns **0 upstream edges**. The "caused" facet (Balon's ambition, Quellon dying at the Mander supporting Robert, Balon's rejection of his father's alliances) has no causal arc in the graph.

**What's missing:** The upstream cause — Quellon Greyjoy died at the Battle of the Mander near the end of Robert's Rebellion; Balon succeeded him, rejected his father's pro-Westeros stance, built the Iron Fleet over 5 years, and declared himself King of the Iron Islands. The chain is shallow:

> `death-of-quellon-greyjoy-at-the-mander [CAUSES] balon-greyjoy-inherits-pyke` → `balon-greyjoy-inherits-pyke [MOTIVATES] greyjoy-rebellion`

Or simpler: a 1-edge `roberts-rebellion MOTIVATES greyjoy-rebellion` (Balon perceived Robert's position as weak post-war; the Rebellion created the power vacuum). 

**Arc-shaped? YES.** Wiki-only (deep-lore — no AGOT/ACOK POV chapters cover the Greyjoy Rebellion's political origins in-saga; only retrospective mentions). Load-bearing? MODERATE. This is new territory — previously the S108 re-dip called this "correct" because the B2 arc answered the downstream question; the upstream is a different shape. Scope: 1-2 beats.

---

### Q9 — What led to the Red Wedding? (B1 control)
**Alias lookup:** `red-wedding` — HIT

**Graph output:**
```
UPSTREAM — (2 edges)
  robb-weds-jeyne-westerling --[TRIGGERS]--> red-wedding-conspiracy
red-wedding-conspiracy --[CAUSES]--> red-wedding

DOWNSTREAM — (0 edges)
```

**Grade: correct**

The B1 arc is present: Robb's marriage → red-wedding-conspiracy → Red Wedding. The chain correctly stops before WO5K terminus (correct-by-policy). The "why did Robb marry Jeyne" sub-question (Q5) is the upstream that's missing, but the Red Wedding question itself is answered.

---

### Q10 — What did the Sack of King's Landing lead to? (Sack arc control)
**Alias lookup:** `sack-of-kings-landing` — HIT

**Graph output:**
```
UPSTREAM — (2 edges)
  battle-of-the-trident --[CAUSES]--> sack-of-kings-landing
  pycelle-opens-the-gates-of-kings-landing --[CAUSES]--> sack-of-kings-landing

DOWNSTREAM — (1 edge)
  sack-of-kings-landing --[CAUSES]--> coronation-of-robert-i-baratheon
```

**Grade: correct**

The Sack arc (Tier-A) is intact: battle-of-the-trident + Pycelle's betrayal → Sack → Robert's coronation. This is the correct and complete load-bearing chain. No downstream causal consequences beyond the coronation are needed (policy-stop-short would apply for anything branching into the entire Baratheon reign).

---

### Q11 — What set Daenerys's conquest of Slaver's Bay in motion / what did the sack of Astapor lead to? (NEW probe)
**Alias lookups:**
- "Daenerys conquest of Slaver's Bay" → NO CONFIDENT MATCH (MISS on natural phrase; `targaryen-campaign-in-slavers-bay` found via fuzzy at 0.55)
- "sack of Astapor" → `fall-of-astapor` — HIT

**Graph output — fall-of-astapor:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF targaryen-campaign-in-slavers-bay (1 outgoing)
```

**Graph output — targaryen-campaign-in-slavers-bay:**
```
OUTGOING — (0 edges)
INCOMING — 7 PART_OF edges (sub-battles)
```

**Grade: failed**

**Discoverability failure:** "Daenerys conquest of Slaver's Bay" is a MISS — the natural phrase doesn't resolve. The canonical node is `targaryen-campaign-in-slavers-bay` which is not a phrase a reader would naturally use.

**Structural failure:** `fall-of-astapor` has 0 causal edges in either direction. No upstream "what motivated this" (Jorah convinces Daenerys she needs an army; she redirects from Pentos to Astapor), and no downstream "what did this lead to" (Daenerys marches on Yunkai; the Targaryen Slaver's Bay campaign; Cleon's butcher-king instability in Astapor). The campaign parent node is similarly causal-dark.

**What's missing:**
- Upstream: `jorah-convinces-daenerys-to-buy-unsullied CAUSES fall-of-astapor` (or broader: Daenerys's need for an army after leaving Qarth). Wiki-only (ASOS Daenerys I-IV); in-saga quoted in Daenerys chapters. Load-bearing? YES — "why did Dany sack Astapor?" is a reader-level question.
- Downstream: `fall-of-astapor CAUSES [march on Yunkai]` and eventually `siege-of-meereen`. The campaign sub-battles exist as PART_OF nodes already; they just need causal wiring.
- Alias: `fall-of-astapor` needs natural-language aliases like "sack of Astapor" (already resolves on lookup), "Dany takes Astapor" — moderate gap.

**Arc-shaped? YES.** In-saga? YES (ASOS Daenerys chapters). Load-bearing? YES. Beats-mostly-exist? PARTIALLY (the PART_OF sub-battles exist; causal wiring is missing). Scope: ~3-5 beats + 4-6 edges.

---

### Q12 — What were the consequences of the Battle of the Blackwater? (NEW probe)
**Alias lookup:** `battle-of-the-blackwater` — HIT

**Graph output:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF war-of-the-five-kings (1 outgoing)
           PRECEDES battle-outside-the-gates-of-winterfell (1 outgoing)
```

**Grade: failed**

**What's missing:** The Battle of the Blackwater is one of the most consequential battles in the saga. Its downstream consequences are major load-bearing beats:
1. Stannis retreats to Dragonstone, crippled — his threat to King's Landing removed for years.
2. The Lannister-Tyrell alliance is cemented (Tywin arrives with Tyrell forces to break the siege).
3. Joffrey sets Sansa aside and agrees to wed Margaery Tyrell (node exists: `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` — but has 0 causal edges).
4. Tywin named Savior of the City and resumes as Hand of the King.

The `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` node exists in the graph but has no upstream causal link to `battle-of-the-blackwater`. That single edge would be the most load-bearing addition.

**Arc-shaped? YES.** In-saga? YES (ACOK Tyrion chapters, Davos chapters; ASOS aftermath). Load-bearing? YES — "what did the Blackwater lead to?" is a genuine reader question for the WO5K juncture. Beats-mostly-exist? PARTIALLY (Sansa-Margaery swap node exists). Scope: 2-3 edges (the downstream wiring to existing nodes).

---

### Q13 — What led to Theon's sack of Winterfell? (NEW probe)
**Alias lookups:**
- "Theon's sack of Winterfell" → CANDIDATES: `sack-of-winterfell` (0.77, fuzzy), `theon-greyjoy-taken-as-ward` (0.72)
- "sack of Winterfell" → `sack-of-winterfell` — HIT

**Graph output — sack-of-winterfell:**
```
UPSTREAM — (0 edges — no causal antecedents)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF war-of-the-five-kings (1 outgoing)
           PRECEDES purple-wedding (1 outgoing)
           LOCATED_AT winterfell (1 outgoing)
```

**Also checked: capture-of-winterfell:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)
```

**Grade: partial** (not failed — the B2 arc covers the upstream of the upstream: greyjoy-rebellion → theon-ward, but the chain doesn't continue through to the sack)

The B2 arc ends at `theon-greyjoy-taken-as-ward`. The next beats in the chain (Theon returns to Pyke; Balon sends him to raid the North rather than King's Landing; Theon departs from his assigned mission and captures Winterfell; the Sack follows) are not wired.

**What's missing:**
- `theon-greyjoy-taken-as-ward CAUSES/MOTIVATES theon-captures-winterfell` (Theon's ward-history shapes his identity crisis driving the capture)
- `capture-of-winterfell CAUSES sack-of-winterfell` (the sack is the Bolton betrayal that follows the siege; `capture-of-winterfell` exists but has 0 causal edges)
- The B2 arc's logical endpoint should be `sack-of-winterfell`, not `theon-greyjoy-taken-as-ward`

**Arc-shaped? YES (extends B2).** In-saga? YES (ACOK Theon chapters). Load-bearing? YES — "what led to the sack of Winterfell?" connects Theon's ward history to his eventual betrayal. Scope: 2-3 beats extending B2's downstream.

---

### Q14 — What were the consequences of Tywin Lannister's death? (NEW probe)
**Alias lookups:**
- "Tywin Lannister's death" → NO CONFIDENT MATCH (candidates include `assassination-of-tywin-lannister` at 0.77)
- "death of Tywin" → `tyrion-processes-the-assassination-attempt` (1.00, WRONG — this is a sub-beat of a different event)

**Graph output — assassination-of-tywin-lannister:**
```
UPSTREAM — (0 edges)
DOWNSTREAM — (0 edges)

Neighbors: PART_OF war-of-the-five-kings (1 outgoing)
```

**Grade: failed**

**Discoverability failure (double):**
- "Tywin Lannister's death" → no confident single match (0.77 for correct node)
- "death of Tywin" → WRONG top hit (`tyrion-processes-the-assassination-attempt`)

This is both an alias gap and a structural gap.

**What's missing:**
1. **Alias:** `assassination-of-tywin-lannister` needs aliases "death of Tywin Lannister", "Tywin's death", "Tyrion kills Tywin" for natural discoverability.
2. **Upstream:** `trial-of-tyrion-lannister CAUSES assassination-of-tywin-lannister` (Tyrion's conviction and Jaime's freeing of him leads to Tyrion finding Shae with Tywin, then killing Tywin). The trial chain exists (Q3) but doesn't continue through to Tywin's death.
3. **Downstream:** Tywin's death has massive downstream consequences — Cersei gains control of the small council, Kevan Lannister's reluctant stewardship, the collapse of Lannister coordination, Tommen's weak reign, Cersei's increasingly poor decisions. These all flow from Tywin's death.

**Arc-shaped? YES.** In-saga? YES (ASOS/AFFC). Load-bearing? YES — Tywin's death is a hinge event. Scope: moderate (2-3 upstream beats extending Q3 chain; 3-5 downstream beats).

---

## Fumble Re-Ranking

Genuine fumbles worth building, sorted by priority:

### #1 — Q14: Assassination of Tywin (double failure: alias + structural)
**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist PARTIAL | scope MODERATE
- The alias failure is severe: "death of Tywin" returns the WRONG node at score 1.00
- The Q3 trial chain already exists; adding `trial-of-tyrion → assassination-of-tywin` extends a built arc cheaply
- Downstream consequences (Cersei's solo rule, Tommen's weakness) are load-bearing plot spine for AFFC
- **Recommended approach:** Fix alias first (quick), then extend Q3 chain upstream + add downstream beats

### #2 — Q12: Battle of the Blackwater consequences
**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist PARTIAL (Sansa-Margaery node exists) | scope SMALL
- The node `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` already exists — one `battle-of-the-blackwater CAUSES joffrey-sets-sansa-aside` edge would wire 2 halves of an existing chain
- Stannis's retreat to Dragonstone + Lannister-Tyrell alliance cemented are the other key beats
- Cheapest real-gap fix (2-3 edges to existing or near-existing nodes)
- **Recommended approach:** Add 2-3 downstream CAUSES edges from `battle-of-the-blackwater`

### #3 — Q11: Daenerys / Fall of Astapor (full arc absent + alias gap)
**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist PARTIAL (PART_OF sub-battles exist) | scope MODERATE-LARGE
- "Daenerys conquest of Slaver's Bay" = MISS natural phrase (alias gap on the campaign node)
- Fall of Astapor has 0 causal edges; the sub-battles exist as PART_OF but have no causal spine
- This is entirely new territory (no prior arc work in the Essos theater)
- **Note:** Scope is larger than #1 or #2; suggest doing #1 and #2 first

### #4 — Q5: Robb-Weds-Jeyne upstream (known partial, Step A)
**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist NO (storming-of-the-crag not in graph) | scope SMALL
- 1-2 beats + 2 edges to extend B1
- Already identified as Step A in the continue prompt; this dip confirms it's still a genuine fumble
- Lowest scope of the genuine fumbles

### #5 — Q13: Sack of Winterfell (B2 extension)
**Score:** arc-shaped ✓ | in-saga ✓ | load-bearing ✓ | beats-mostly-exist PARTIAL (capture-of-winterfell exists, 0 causal edges) | scope SMALL-MODERATE
- B2 ends at `theon-greyjoy-taken-as-ward`; 2-3 beats to continue to sack
- Less urgent than #1-3 since the sack itself is relatively self-contained

### Known partials confirmed still-partial (but lower priority)
- **Q6 (Battle of the Trident upstream):** Still 0 inbound CAUSES; `roberts-rebellion CAUSES battle-of-the-trident` is 1 edge. Remains the known Step B refinement.
- **Q7 (Ned execution downstream):** Still 0 downstream; remains Step C (lower priority).
- **Q8 (Greyjoy Rebellion upstream):** The upstream cause (Quellon's death, Balon's ambition) is wiki-only lore; no in-saga chapter covers this in narrative. Lower priority; deep-lore/wiki-only causal arc.

---

## Summary Verdict

**The arc layer scores 7/14 correct-or-stop-short, 4 partial, 3 failed.** 

The three genuine failed questions (Q11, Q12, Q14) are ALL new probes — none of the previously-built arcs failed on control questions. The known partials (Q5, Q6, Q7) remain partial as expected. Q8 (Greyjoy upstream) is newly confirmed as partial rather than correct.

**#1 build recommendation: Tywin's death arc (Q14)** — alias fix + extend Q3 chain + add downstream. Double failure (alias + structural), extends a built arc (Q3 trial chain), and unlocks AFFC/ADWD consequence territory. Scope: small-to-moderate.

If Q14 is done first, Q12 (Blackwater consequences, 2-3 edges, very cheap) makes a strong #2 because existing nodes just need wiring. Q11 (Slaver's Bay, new territory) is the richer but larger project for a later step.

---

---

## POST-BUILD CONFIRMATION (S109, same session) — Q14 Tywin-death arc SHIPPED

The #1 fumble (Q14) was built this session (dip-driven, one validating batch). After the mint + fresh-subagent verify:
- **Discoverability FIXED:** "death of Tywin" / "Tyrion kills Tywin" now resolve to `assassination-of-tywin-lannister` (was the wrong node at 1.00). Root cause + fix: frontmatter aliases must be **natural spaced phrases**, not kebab slugs — the resolver normalizes "death of Tywin" → `death of tywin` (spaces kept), which a kebab alias `death-of-tywin` never matches. Rewrote all 4 nodes' aliases spaced + rebuilt the resolver.
- **Structural FIXED:** `--causal-chain assassination-of-tywin-lannister` now returns a **7-edge upstream chain** — `sansa-receives-the-poisoned-hairnet → death-of-joffrey → tyrion-accused → trial-of-tyrion → gregor-kills-oberyn → jaime-frees-tyrion → tysha-revelation → assassination`. The new arc connects the already-built Purple-Wedding arc straight through to the patricide.
- Node repaired (event.battle→event.assassination, junk infobox prose removed); 3 new beats + 17 edges (11 role Tier-1 + 6 causal Tier-2, all verified CONFIRM; edge #1 retyped CAUSES→TRIGGERS per verifier).
- **Q14 grade: failed → CORRECT** (blame/cause facet). Downstream consequences DEFERRED (no Cersei-regent / Tommen-reign nodes exist; a long-distance ASOS→ADWD CAUSES would overclaim).

**Remaining re-ranked queue (dip-driven, NOT mass-mint):** #1 Q12 Battle-of-the-Blackwater downstream (cheapest — `joffrey-sets-sansa-aside…` node exists, 2-3 edges) · #2 Q11 Daenerys/Slaver's-Bay (new Essos territory, larger) · #3 Q5 robb-weds-jeyne upstream (storming-of-the-Crag beat) · Q6 Trident inbound CAUSES (1 edge) · Q13 Sack-of-Winterfell (extends B2). Re-dip before building each.

*Dip conducted: 2026-06-19. Session: S109. Model: claude-sonnet-4-6.*
*Sources consulted (Phase 2): `sources/wiki/_raw/Jeyne_Westerling.json`, `Storming_of_the_Crag.json` (redirected from `Battle_of_the_Crag.json`), `Robert's_Rebellion.json`, `Battle_of_the_Trident.json`, `Greyjoy's_Rebellion.json`, `Fall_of_Astapor.json`, `Targaryen_campaign_in_Slaver's_Bay.json`, `Battle_of_the_Blackwater.json`, `Sack_of_Winterfell.json`, `Assassination_of_Tywin_Lannister.json`.*
