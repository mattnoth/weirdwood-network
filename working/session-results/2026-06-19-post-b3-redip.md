# POST-B3 VERIFICATION RE-DIP
Date: 2026-06-19 (S108)
Method: Consumer-agent re-dip — all answers sourced from graph tools only (Phase 1), then graded against local wiki/chapter cache (Phase 2). Internet never consulted. Same 10 arc-weighted questions as the prior dips, for comparability.

Graph state (graph-query.py --health):
```
  Node files (*.node.md)  :   8,542
  Edge count              :  22,255
  Unique edge endpoints   :   6,002
  Orphan endpoints        :      62  (endpoints with no node file)
```
This is the POST-B3 re-dip. **B3 ("Ned's-downfall arc")** added the upstream causal chain to `execution-of-eddard-stark` (Q10). It also captures **B2 ("Greyjoy→Theon-ward")** which landed after the prior re-dip's measurement (Q8).

---

## Tally — before/after

| Grade | Post-B1 re-dip | Post-B3 re-dip |
|-------|----------------|----------------|
| correct | 6 (Q1,Q2,Q4,Q5,Q7,Q9) | **8** (Q1,Q2,Q4,Q5,Q7,Q8,Q9,Q10) |
| correct-to-stop-short (Q6, policy) | 1 | 1 |
| partial | 3 (Q3,Q8,Q10) | **2** (Q3, + Q7-on-strict-reading) |
| failed | 0 | 0 |

**Two questions moved up:**
- **Q10 (Ned's execution): partial → CORRECT** — the goal of this session. `--causal-chain execution-of-eddard-stark` now returns the upstream chain; blame is distributed across role edges.
- **Q8 (Greyjoy→Theon-ward): partial → CORRECT** — B2's `greyjoy-rebellion --CAUSES--> theon-greyjoy-taken-as-ward` is traversable (this re-dip is the first to measure the post-B2 graph).

**Q7 note:** the dip agent re-graded Q7 *partial* on a stricter reading ("what led Robb to marry Jeyne?" is unplumbed — `robb-weds-jeyne-westerling` has no upstream causal edge). It explicitly flagged this as a grading-strictness difference, NOT a graph regression — the B1 structure is unchanged and the prior re-dip's "correct" stands on the same data. The `robb-weds-jeyne` upstream was already logged as a known refinement in the post-B1 re-dip §3.

---

## Q10 deep-confirm — `--causal-chain execution-of-eddard-stark` (actual output)

```
UPSTREAM — what led to this  (3 edges)
    death-of-robert-baratheon --[CAUSES]--> arrest-of-eddard-stark
  arrest-of-eddard-stark --[CAUSES]--> execution-of-eddard-stark
  ned-confesses-to-treason --[TRIGGERS]--> execution-of-eddard-stark
DOWNSTREAM (0)
```
Plus, off the spine:
- `ned-discovers-the-truth-of-joffrey-s-parentage --MOTIVATES--> cersei-lannister` and `--MOTIVATES--> eddard-stark` (why both acted).
- Blame, via role edges: Joffrey `COMMANDS_IN` execution; Ilyn Payne `AGENT_IN` (+ Ice `WIELDED_IN`); Cersei `COMMANDS_IN` the death-of-robert, the betrayal, and the confession; Littlefinger `COMMANDS_IN` the betrayal (+ pre-existing `BETRAYS` dyad); Lancel `AGENT_IN` the death.

A consumer agent asking "who is to blame for Ned's execution and what set it in motion" now assembles the full answer from the graph: Robert's engineered death removed Ned's protector; Ned (motivated by the parentage discovery) moved against Cersei; Littlefinger betrayed him; the arrest led to a forced confession; Joffrey ordered the execution against the mercy deal.

---

## Re-ranking — remaining gaps (dip-driven; do NOT mass-mint)

| Priority | Gap | Question | Scope |
|----------|-----|----------|-------|
| 1 | `robb-weds-jeyne-westerling` has no upstream (why Robb married Jeyne — fall of the Crag / Jeyne nursing him) | Q7 refinement | 1–2 beats; extends B1 |
| 2 | Battle of the Trident has no inbound CAUSES on the causal walk (only PART_OF/PRECEDES) | Q3 | 1 edge (`roberts-rebellion CAUSES battle-of-the-trident`) or PRECEDES→CAUSES promotion |
| 3 | `execution-of-eddard-stark` downstream empty (consequences) | Q10 downstream | lower priority — the asked facet (blame/cause) is covered |
| — | `greyjoy-rebellion` upstream (what caused the rebellion) | not asked in Q8 | open arc slot |

**Recommendation:** the next dip-driven build, if any, is the Q7 `robb-weds-jeyne` upstream refinement (closes the one strict-reading partial and extends the already-shipped B1). But per dip-driven cadence, let a future arc-weighted dip re-confirm demand before building — B3 was the richest remaining gap and it is now closed.
