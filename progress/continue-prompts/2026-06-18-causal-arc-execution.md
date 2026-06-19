# Continue — Causal-arc execution: traversal primitive + first Tier-A batch

> **Recommended model:** Sonnet 4.6 (deterministic script work for the primitive; subagent-driven arc minting). Opus only if a hard interpretive judgment needs it.
> **Gated on:** Matt ratifying the S105 parent-node recommendation (see below). If he's pushed back, re-read his direction first.

## Where this stands (S105, 2026-06-18)

The causal/narrative-arc **technique is proven twice** (Robert's Rebellion S104; Bran's fall S105) and the **scaling strategy is written**: `working/causal-arc-strategy-2026-06-18.md` (rubric + prioritized arc list + cost model + 7 policy Qs + smoke-test analysis + advisory-board outcome + the agency-collapse lesson). Read it first — it is the spec for this track.

**Parent-node decision (S105 recommendation, awaiting Matt's ratification):** **causal-chain-as-arc, NO umbrella parent nodes.** Deliver "show me the whole arc" via a `--causal-chain` query primitive, not a parent hub. This supersedes the umbrella-vs-chain fork in the parked `archive/2026-06-15-arc-wave1-mint.md`. Do NOT mint `event.arc` parent nodes unless Matt overrides.

## The work, in order

### Step 1 — build the `--causal-chain` directed-traversal primitive (Track 7 prerequisite)
In `scripts/graph-query.py`, add `--causal-chain <slug>` that walks **CAUSES / TRIGGERS / MOTIVATES** edges forward AND backward from the given node (transitively), returning the ordered consequence-chain. This is what makes a causal arc actually queryable ("what set X in motion / what did X lead to"). Without it the chains are latent. Smoke-test it on the Bran's-fall arc (`bran-witnesses-jaime-and-cersei` → … → `gregor-raids-the-riverlands`). Deterministic; add tests.

### Step 2 — first Tier-A arc batch (dip-gated, small)
Mint 1–2 Tier-A arcs from the strategy's prioritized list — **Sack of King's Landing** and/or **Purple Wedding**. Reuse the RR/Bran template, with the two S105 lessons folded in as HARD steps:
- **Pre-mint dedup lookup (mandatory):** before minting ANY beat-node, run its description through `python3 scripts/event_alias_resolver.py --lookup "<phrase>"` AND eyeball the all-node fuzzy index for matches ≥0.6. The ~200 verbose-slug Plate-3 beats are the collision surface — slug-guessing misses them (S105 minted a dup this way).
- **Agency-collapse check:** before emitting `A CAUSES B`, ask whose decision sits between them. If a person chooses to act, model the agency — insert the decision as a beat node (if it's a scene, e.g. Littlefinger's lie) OR `MOTIVATES`→actor + the actor's `COMMANDS_IN`/`AGENT_IN` on B (if it's a choice, e.g. Tywin).
- Don't mint thin hubs — every new beat gets role edges (AGENT_IN/VICTIM_IN/COMMANDS_IN/LOCATED_AT) like the Plate-3 beats.

## Policy / guardrails (FIRM)
- **Tier:** causal edges capped **Tier-2** (interpretive link); role edges Tier-1 (factual presence).
- **CAUSES vs TRIGGERS:** TRIGGERS = immediate specific spark; CAUSES = mediated cause (S104 rule).
- **Hard-stop discipline:** don't chain CAUSES into a multi-attributed terminus (e.g. don't assert `X CAUSES war-of-the-five-kings`).
- **Verification:** every causal edge verified by a **fresh subagent vs the LOCAL cache** (chapters + `sources/wiki/_raw/`); never re-fetch. Matt gates at policy level, not per-edge.
- **Node ADD → rebuild** targeted indexes (`build-entity-indexes.py --type events --slug <s>`) + `event_alias_resolver.py --build`. Back up `edges.jsonl` to `_regrounding/` before mutation.
- **Vocabulary:** Pass/Track/Tier + lowercase `step`; Tier = confidence 1–5 ONLY. (paste into any naming/sequencing subagent.)

## Open questions for Matt
- Ratify (or revise) the parent-node recommendation before Step 2.
- Which Tier-A arc first — Sack of KL (extends shipped RR/Trident work, answers dip Q10) or Purple Wedding (beats partly exist from FIX-22)?

## Vocabulary to paste into subagents
Pass (numbered corpus sweep) · Track (named workstream) · step (lowercase, ordered piece) · Tier (confidence 1–5 ONLY). Source: `reference/glossary.md`.
