# Continue — Causal / narrative-arc STRATEGY (pure-analysis session)

> **Recommended model:** Opus (analysis/judgment) or Sonnet 4.6. **This is a PURE-ANALYSIS session — NO graph writes.** Matt's call (S104): the "how far to scale causal edges" question gets its own analysis session first, because the answer governs *all* of narrative-arc reification, not just one arc.
>
> **Status going in (S104, 2026-06-17):** The method is proven and one exemplar is shipped. Robert's Rebellion now has a full causal arc — 3 minted spark-beat nodes (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) + 6 causal edges (`tourney→abduction→executions→demand→rebellion` and `Trident→Sack→Coronation`), all fresh-subagent-verified against the local wiki. The pilot (`CAUSES` Trident→Sack→Coronation) is also in. So the *technique* is settled; what's open is the *strategy*.

## The question to answer
**How far, and in what order, should causal/narrative-arc structure be built across the whole graph?** The graph has ~588 event nodes densely connected by participants and (now) `PRECEDES` chronology, but causal consequence-chains (`CAUSES`/`TRIGGERS`) and reified narrative arcs exist only for a handful (Red Wedding, Trident incident, Robert's Rebellion). Reader-felt arcs ("X led to Y led to Z") are mostly absent. Deciding the scaling policy here sets the direction for the whole narrative-arc-reification track ([[project_narrative_arc_reification]]).

## What this session should PRODUCE (a written plan, no graph edits)
Write findings to `working/` (e.g. `working/causal-arc-strategy-2026-06-NN.md`). Cover:
1. **Inventory.** Survey existing `event.*` nodes + edges. Which major arcs/conflicts already have causal structure, which are isolated chronology-only, which lack nodes for their pivotal beats (like RR's spark beats did). Use `scripts/graph-query.py`, the indexes, and the local wiki cache.
2. **Criteria for "worth reifying."** What makes an arc worth the spark-node + causal-edge investment? Candidate signals: query-value (does a grounded-agent dip fumble it?), reader-salience, beat-nodes missing, cross-POV reach. Propose a rubric.
3. **Prioritized list.** Rank the next N arcs/conflicts to treat (e.g. War of the Five Kings sub-arcs, the Dance of the Dragons, R+L=J, Greyjoy Rebellion, Daenerys's Slaver's Bay campaign…), with the reasoning.
4. **Approach + cost per arc.** Reuse the RR template: mint missing beat-nodes from local sources → index/alias rebuild → wire `CAUSES`/`TRIGGERS` → fresh-subagent verify. Estimate effort/cost per arc and recommend dip-driven vs batch.
5. **Open design questions for Matt** — anything that needs his policy call before execution (e.g. how aggressively to mint beat-nodes, Tier policy for interpretive causal edges, where arc reification overlaps the parked arc-wave1 mint).

## Hard rules
- **NO graph writes this session** — analysis only. Output is a plan Matt reviews.
- Use ONLY the local wiki/book cache; never refetch ([[feedback_no_external_wiki_fetch]]).
- When execution later resumes from this plan, the verification gate is fresh subagents vs the local cache; Matt gates at policy level, not per-edge ([[feedback_subagent_verify_not_matt]]).

## Context / source-of-truth
- `history/session-details/session-104.md` — the RR exemplar, the CAUSES-vs-TRIGGERS granularity finding, the verification method.
- `working/narrative-arcs-design-memo-2026-06-13.md` + memory `project_narrative_arc_reification` — the reification pattern this generalizes.
- Resolved S104 (no action): `shadow-war → targaryen-campaign-in-slavers-bay` PART_OF is correct (subagent-confirmed). Small node-quality fixes on those two nodes are queued in todos § Small Fixes.
