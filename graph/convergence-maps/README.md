# Convergence Maps — the braid layer (charter)

> **Status:** design charter, no outputs yet (dir was empty through S117). Seeded by Matt's
> "overlapping chains" insight (S117) — captured here so it isn't lost. NOT yet built.

## The idea (Matt, S117)

Causal chains are not isolated lines — they **overlap**, and the overlaps are themselves
the interesting structure. Three shapes:

1. **Divergence (shared start, different ends).** One node fans out into multiple chains
   that never re-meet. *Live example:* `gregor-confesses-and-kills-oberyn` forks into the
   Dorne thread (`arrest-of-the-sand-snakes` → Arianne) **and** the Tywin/Cersei thread
   (`jaime-frees-tyrion` → Tysha → Tywin's death → Cersei's downfall).
2. **Convergence (different starts, shared end).** Multiple independent causes feed one
   event. *(We deliberately HARD-STOP before multi-attributed termini like
   `war-of-the-five-kings` — but softer convergences are real and worth surfacing.)*
3. **Offset / partial overlap (shared middle).** Two chains run through a common segment
   but enter and exit at different points.

The reframe this gives the **"everything roots at the hairnet" worry** (S117): the
`sansa-receives-the-poisoned-hairnet` super-attractor is not a bug — it's a major
**divergence hub** (one cause → 14 downstream beats fanning across Joffrey's death,
Tyrion's trial+escape, Tywin's death, Cersei's downfall, the Dorne arrest). The braid view
is the right lens: the interesting question isn't "what's the deepest root" but **where do
the fanned-out chains share spine, fork, and (rarely) re-converge.**

This is also why GRRM's plot *feels* tightly woven: the same node participates in multiple
arcs. The graph already encodes this (it's a DAG of causal edges); what's missing is
**tooling to surface the overlaps** — that's what this directory is for.

## What a convergence map is (the deliverable)

A read-only, deterministic analysis over `graph/edges/edges.jsonl` (Python-before-agent).
Given **two or more terminal events**, walk each one's causal chain (the `--causal-chain`
primitive already exists) and emit the **braid**: the shared segments, the fork nodes
(out-degree ≥ 2 in causal edges), the join nodes (in-degree ≥ 2), and where each chain
enters/exits a shared run. Output per map: a small JSON + a human-readable markdown (and
later maybe a rendered diagram) under this directory, one file per named convergence.

## Tooling sketch (when built — NOT this session)

- A new `scripts/graph-query.py` mode or a sibling `scripts/convergence-map.py`:
  - `--braid <terminusA> <terminusB> [...]` — walk all chains, intersect node sets, label
    shared-segment / fork / join.
  - `--fork-hubs [--min-out N]` — list divergence hubs (the hairnet, Oberyn's death, the
    Tysha reveal) ranked by downstream fan-out — the "super-attractor" report.
  - `--join-hubs [--min-in N]` — list convergence points (respecting the multi-attributed
    HARD-STOP — these are exactly the nodes we refuse to chain *into*, so they're the
    natural convergence catalogue).
- Pure DAG analysis; no LLM. A subagent only if we later want narrative naming of a braid.

## Why it's deferred (not built now)

It's an *analysis/visualization* layer over the causal edges — it gets more valuable the
denser the causal layer is. Right now we're still in the **spine-build phase** (AFFC done
S117; Essos + WO5K next). Build convergence maps once there's enough braid to map — a
natural companion to the **arc-enrichment phase** (see `working/arc-enrichment-backlog.md`),
or sooner if a demo/QA pass wants the fork/join reports. Pairs with the deferred Pass-4
foreshadowing layer (FORESHADOWS edges add a second, non-causal thread to braid against).
