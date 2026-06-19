# POST-B1 VERIFICATION RE-DIP
Date: 2026-06-19
Method: Consumer-agent re-dip — all answers sourced from graph tools only (Phase 1), then graded against local wiki/chapter cache (Phase 2). Internet never consulted.
Graph state (graph-query.py --health, first 8 lines):
```
GRAPH HEALTH REPORT
  Node files (*.node.md)  :   8,538
  Edge count              :  22,236
  Unique edge endpoints   :   5,998
  Orphan endpoints        :      62  (endpoints with no node file)
```
This is the POST-B1 verification re-dip. The B1 arc ("Red Wedding upstream") was minted to add causal antecedents to `red-wedding` and `robb-is-killed`.

---

## §1 Per-Query Table

| # | Question | Tool calls (resolver status) | Graph's answer | Grade | vs prior dip |
|---|----------|------------------------------|----------------|-------|--------------|
| Q1 | What set Tyrion's arrest in motion? | resolver "Catelyn arrests Tyrion" → CANDIDATES, top=`catelyn-seizes-the-moment-and-arrests-tyrion` (used). `--causal-chain catelyn-seizes-the-moment-and-arrests-tyrion` | Full upstream chain: bran-witnesses → jaime-pushes-bran → direwolf-kills-assassin → littlefinger-names-dagger → catelyn-arrests-tyrion (4-hop). | **correct** | same (was correct) |
| Q2 | Who poisoned Joffrey / who is to blame? | resolver "Purple Wedding" → HIT (`purple-wedding`). `--causal-chain purple-wedding` → 0 edges. Tried `--neighbors purple-wedding` → found `death-of-joffrey-baratheon` as SUB_BEAT_OF. `--causal-chain death-of-joffrey-baratheon` → upstream: `sansa-receives-the-poisoned-hairnet`. `--neighbors death-of-joffrey-baratheon` → AGENT_IN: `olenna-tyrell`; COMMANDS_IN: `petyr-baelish`; VICTIM_IN: `joffrey-baratheon`. `--neighbors sansa-receives-the-poisoned-hairnet` → AGENT_IN: `dontos-hollard`; COMMANDS_IN: `petyr-baelish`. | Graph names Olenna Tyrell as AGENT_IN and Petyr Baelish as COMMANDS_IN for the poisoning. The causal chain is hairnet → death-of-joffrey. `purple-wedding` hub itself is causally dark, but sub-beats are fully wired. | **correct** (with a navigation step needed — can't go directly through `purple-wedding` hub; must navigate to `death-of-joffrey-baratheon`) | same (was correct via sub-beat navigation) |
| Q3 | What were the consequences of the Battle of the Trident? | resolver "Battle of the Trident" → HIT. `--causal-chain battle-of-the-trident` | Downstream: battle-of-the-trident → CAUSES → sack-of-kings-landing → CAUSES → coronation-of-robert-i-baratheon. Upstream: none. | **partial** (Phase 2 wiki confirms additional consequences: end of Targaryen dynasty, death of Rhaegar, opening for Aerys's later killing — these are not in the causal chain; only the Sack and Coronation paths are wired) | same (was partial) |
| Q4 | What caused Robert's Rebellion? | resolver "Robert's Rebellion cause" → CANDIDATES, top=`roberts-rebellion` (used). `--causal-chain roberts-rebellion` | Upstream 4-hop: tourney-at-harrenhal → abduction-of-lyanna → execution-of-brandon-and-rickard-stark → aerys-demands-ned-and-robert → roberts-rebellion. Downstream: none. | **correct** (upstream spark chain complete; downstream absence is a separate arc gap) | same (was correct) |
| Q5 | What did Jaime pushing Bran from the tower lead to? | resolver "Bran pushed from tower" → CANDIDATES, top=`jaime-pushes-bran-from-the-tower` (used). `--causal-chain jaime-pushes-bran-from-the-tower` | Downstream 5-hop: jaime-pushes → direwolf-kills-assassin → littlefinger-names-dagger → catelyn-arrests-tyrion → gregor-raids-riverlands / tywin-lannister (motivates). Upstream: bran-witnesses-jaime → jaime-pushes. | **correct** | same (was correct) |
| Q6 | What set the War of the Five Kings in motion? | resolver "War of the Five Kings" → HIT. `--causal-chain war-of-the-five-kings` | 0 upstream, 0 downstream. | **correct-to-stop-short / working-as-intended** (per project policy: war-of-the-five-kings is a multi-attributed terminus; no spark edges should be attached; empty causal chain is correct behavior) | same (policy-compliant, not a failure) |
| Q7 | What caused the Red Wedding — what chain of events led Robb there? | resolver "Red Wedding" → HIT. `--causal-chain red-wedding` | **UPSTREAM NOW POPULATED:** robb-weds-jeyne-westerling → TRIGGERS → red-wedding-conspiracy → CAUSES → red-wedding. Conspirators named via `--neighbors red-wedding-conspiracy`: COMMANDS_IN: walder-frey, tywin-lannister; AGENT_IN: roose-bolton. Parallel chain via `--causal-chain catelyn-releases-jaime-lannister`: catelyn-releases-jaime → CAUSES → karstark-murders-prisoners → CAUSES → execution-of-rickard-karstark. | **correct (IMPROVED — B1 confirmed landed)** | **IMPROVED** (was failed/partial; now correctly traces upstream cause chain) |
| Q8 | Consequences of Greyjoy Rebellion; how did Theon become Stark ward? | resolver "Greyjoy Rebellion" → HIT. `--causal-chain greyjoy-rebellion` → 0 upstream, 0 downstream. `--path greyjoy-rebellion theon-greyjoy` → 2-hop: theon-greyjoy → WARD_OF → eddard-stark (bridge); eddard-stark → COMMANDS_IN → greyjoy-rebellion. `--neighbors theon-greyjoy` confirms WARD_OF: eddard-stark with book quote. | Graph answers the Theon-as-ward fact via dyadic edge (WARD_OF). The rebellion itself is causally dark — no CAUSES/TRIGGERS out-edges. The "consequences" question is partially answered (ward status reachable) but the rebellion's causal consequences are absent. | **partial** (dyad answers wardship; consequences of the rebellion are not traversable via causal chain) | same (was partial) |
| Q9 | What set the Sack of King's Landing in motion, and what did it cause? | resolver "Sack of King's Landing" → HIT. `--causal-chain sack-of-kings-landing` | Upstream (2 edges): battle-of-the-trident → CAUSES → sack; pycelle-opens-the-gates-of-kings-landing → CAUSES → sack. Downstream: sack → CAUSES → coronation-of-robert-i-baratheon. | **correct** | same (was correct) |
| Q10 | Who is to blame for Ned Stark's execution, and what set it in motion? | resolver "Ned Stark execution" → HIT (`execution-of-eddard-stark`). `--causal-chain execution-of-eddard-stark` → 0 upstream, 0 downstream. `--neighbors execution-of-eddard-stark` → COMMANDS_IN: joffrey-baratheon; AGENT_IN: ilyn-payne; VICTIM_IN: eddard-stark. | Graph correctly names Joffrey as commanding the execution and Ilyn Payne as the executioner. But no upstream causal chain explains what led to the execution — the arc from Ned confronting Cersei → Littlefinger's betrayal → arrest → Joffrey's impulsive order is not wired. | **partial** (blame correct via COMMANDS_IN; upstream cause chain absent) | same (was partial/failed) |

---

## §2 Tally + Before/After

**Prior dip tally:** 5 correct / 3 partial / 2 failed

**Post-B1 tally:** 6 correct / 3 partial / 1 correct-to-stop-short

Breakdown:
- Q1: correct → **correct** (same)
- Q2: correct → **correct** (same)
- Q3: partial → **partial** (same)
- Q4: correct → **correct** (same)
- Q5: correct → **correct** (same)
- Q6: correct-to-stop-short → **correct-to-stop-short** (same; policy unchanged)
- Q7: **IMPROVED** — prior: failed/partial → now: **correct** (B1 landed)
- Q8: partial → **partial** (same)
- Q9: correct → **correct** (same)
- Q10: partial → **partial** (same)

**One question moved:** Q7 (Red Wedding upstream) upgraded from failed/partial to correct.

Restated without Q6 (policy-compliant non-answer):
- 6 correct (Q1, Q2, Q4, Q5, Q7, Q9)
- 3 partial (Q3, Q8, Q10)
- 0 failed

---

## §3 Q7 Deep-Confirm

**`--causal-chain red-wedding` output (actual):**
```
CAUSAL CHAIN: red-wedding
  Red Wedding (event.wedding)
  walks CAUSES / MOTIVATES / TRIGGERS (transitive, both directions)

UPSTREAM — what led to this  (2 edges)
------------------------------------------------------------------------
    robb-weds-jeyne-westerling --[TRIGGERS]--> red-wedding-conspiracy
  red-wedding-conspiracy --[CAUSES]--> red-wedding

DOWNSTREAM — what this led to  (0 edges)
------------------------------------------------------------------------
  (none — no causal consequences)

SUMMARY: red-wedding  |  2 upstream + 0 downstream = 2 causal edges
```

**`--causal-chain robb-is-killed` output (actual):**
```
CAUSAL CHAIN: robb-is-killed
  Robb is killed (event.death)
  walks CAUSES / MOTIVATES / TRIGGERS (transitive, both directions)

UPSTREAM — what led to this  (2 edges)
------------------------------------------------------------------------
    robb-weds-jeyne-westerling --[TRIGGERS]--> red-wedding-conspiracy
  red-wedding-conspiracy --[CAUSES]--> robb-is-killed

DOWNSTREAM — what this led to  (0 edges)
------------------------------------------------------------------------
  (none — no causal consequences)

SUMMARY: robb-is-killed  |  2 upstream + 0 downstream = 2 causal edges
```

**Confirmation:** A reader asking "what led to the Red Wedding?" now gets a traversable answer: Robb married Jeyne Westerling (breaking his oath to Walder Frey) → triggered the Red Wedding conspiracy (with Walder Frey, Tywin Lannister commanding; Roose Bolton as agent) → caused the Red Wedding. The `red-wedding-conspiracy` node also names the plotters via COMMANDS_IN and AGENT_IN edges (walder-frey, tywin-lannister, roose-bolton) with book quotes.

**Parallel Karstark chain (`--causal-chain catelyn-releases-jaime-lannister`):**
```
DOWNSTREAM — what this led to  (2 edges)
  catelyn-releases-jaime-lannister --[CAUSES]--> karstark-murders-prisoners-at-riverrun
    karstark-murders-prisoners-at-riverrun --[CAUSES]--> execution-of-rickard-karstark
```
This chain is intact and traversable. The arc correctly captures how Catelyn's unilateral act cost Robb a key ally and weakened his position — a contributing factor to his eventual isolation that makes the Red Wedding possible.

**Note on `robb-weds-jeyne-westerling` upstream gap:** The `robb-weds-jeyne-westerling` event has no upstream causal edges — there is no arc from the fall of the Crag (or Jeyne nursing a wounded Robb) that TRIGGERS his impulsive marriage. That is a potential B1-extension or future arc, but it is a refinement, not a critical failure: the current chain is accurate as far as it goes.

---

## §4 What Still Fumbles + Re-Ranking

### Q3 — Battle of the Trident consequences (partial)
Phase 2 check (local wiki `Battle_of_the_Trident.json`) confirms the battle's consequences include: death of Rhaegar Targaryen, opening of King's Landing to sack, end of the Targaryen dynasty. The graph wires only sack → coronation. Missing: Rhaegar's death as a consequence (no VICTIM_IN edge pointing out from battle-of-the-trident), no edge to the end of House Targaryen's rule. This is a modest gap — the key structural chain (battle → sack → coronation) is correct.

### Q8 — Greyjoy Rebellion consequences + Theon wardship (partial)
Phase 2 check (`Theon_Greyjoy.json`) confirms: "At the end of Greyjoy's Rebellion, Theon was taken to Winterfell as a hostage and ward to Lord Eddard Stark." The graph answers the wardship question via dyadic edge `theon-greyjoy --[WARD_OF]--> eddard-stark` with a book citation. This is reachable via `--path greyjoy-rebellion theon-greyjoy` (2-hop bridge) and via `--neighbors theon-greyjoy`. 

However, `--causal-chain greyjoy-rebellion` returns nothing — the rebellion is causally dark. The arc "Greyjoy Rebellion → Theon taken as ward → Theon grows up at Winterfell" is not encoded as a CAUSES/TRIGGERS chain. A **B2 arc** would add: `greyjoy-rebellion --[CAUSES]--> theon-taken-as-ward-of-starks` (possibly a new event node, or a CAUSES edge directly to the `theon-greyjoy --WARD_OF--> eddard-stark` dyad's provenance event).

**B2 warranted?** The wardship dyad is findable via path traversal, which is workable. But the "consequences of the rebellion" question is a natural one and the causal chain returns nothing — a genuine fumble for a consumer agent with no fallback. **B2 is justified** but not urgent. The dyadic fallback partially saves it.

### Q10 — Ned Stark's execution (partial)
The graph correctly names Joffrey as COMMANDS_IN and Ilyn Payne as AGENT_IN. But upstream: why was Ned executed? Phase 2 wiki reveals the chain: Ned discovers Joffrey's illegitimacy → plans to flee → Sansa warns Cersei → Ned confronts Cersei → Littlefinger betrays Ned → arrest → Joffrey's impulsive order overrides the "send him to the Wall" plan. None of this is a wired causal chain in the graph. A **B3 arc** would add spark nodes: Ned-discovers-bastard-secret → Ned-confronts-Cersei → littlefinger-betrays-ned → execution-of-eddard-stark. This is the most narrative-dense missing arc in the set.

### Re-ranking signal

| Priority | Arc | Question it fixes | Justification |
|----------|-----|-------------------|---------------|
| B2 | Greyjoy → Theon wardship | Q8 | Single CAUSES edge (or new event node); clear, low-effort |
| B3 | Ned's downfall arc | Q10 | Richer, 3-4 events; highly sought narrative; Ned's story is central to AGOT |
| B4 | Trident downstream extensions | Q3 | Add Rhaegar VICTIM_IN + Targaryen-dynasty end-edge; modest scope |
| — | robb-weds-jeyne upstream | Q7 refinement | Optional extension; not a critical failure |

---

## §5 Bottom Line

B1 landed cleanly. `--causal-chain red-wedding` and `--causal-chain robb-is-killed` both now return the two-step upstream chain (Robb weds Jeyne → Red Wedding conspiracy → Red Wedding/Robb killed), and the parallel Karstark chain (`catelyn-releases-jaime-lannister → karstark-murders → Karstark execution`) is also traversable. The arc layer moved from 5 correct / 2 failed to 6 correct / 3 partial / 0 failed (excluding the policy-compliant Q6 non-answer). The most valuable next arc is B3 (Ned Stark's downfall — what set his execution in motion), which is the only remaining "who is to blame + what led to it" question returning a partial answer due to absent upstream chain. B2 (Greyjoy → Theon wardship) is achievable with a single edge or small event node and would close the one remaining clean miss on a "consequences of" question.
