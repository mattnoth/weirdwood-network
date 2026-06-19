---
session: 105
date: 2026-06-18
model: Opus 4.8 (1M context) orchestrator + 5 Sonnet 4.6 general-purpose subagents (2 verification + 1 first-arc verify + 4-lens advisory board... see below)
title: Causal-arc scaling strategy + second smoke test (Bran's fall) + advisory board
---

# Session 105 — Causal-arc strategy + Bran's-fall smoke test + advisory board

## Purpose

Continuation of the S104 causal-edges track. The continue prompt (`2026-06-17-causal-edges-and-spark-nodes.md`) framed this as a **pure-analysis** session: produce a written strategy for how far/in what order to build causal/narrative-arc structure across the whole graph. Matt then expanded scope mid-session — first authorizing a **second smoke-test arc** (after Robert's Rebellion, S104), then a **4-lens advisory board** on the arc-shape question. So the session ran analysis → execution → adversarial design review, all in one.

## Part 1 — the strategy (pure analysis)

Surveyed the causal layer. Key inventory (2026-06-18):
- 593 `event.*` nodes; **only 12 touched by any causal edge** (CAUSES/TRIGGERS/ENABLES/MOTIVATES/PREVENTS); 466 (79%) have neither causal nor `PRECEDES` chronology.
- The causal layer was 8 edges in 3 micro-arcs (RR spark chain, Trident incident, street-brawl) + the Trident→Sack pilot.
- Containment/chronology layers DO have reach: `PART_OF` 168, `SUB_BEAT_OF` 66, `PRECEDES` 174 (117 events). WO5K has 69 PART_OF battles + 40 internal PRECEDES but **zero internal causality**.
- Data-quality aside: `roberts-rebellion` and `dance-of-the-dragons` are mistyped `event.battle` (→ todos).

Wrote `working/causal-arc-strategy-2026-06-18.md`: a 6-signal reify-worthiness rubric; a prioritized arc list (Tier A = Sack of KL / Bran's fall / Purple Wedding — in-saga, beats partly exist; Tier C defer = WO5K mesh + deep-lore wiki-only wars → route to TWOIAF/F&B ingestion); cost model; and 7 open policy questions (the load-bearing one: **cap causal edges at Tier-2** because causation is interpretive even when endpoints are canon).

## Part 2 — second smoke test: the Bran's-fall arc

Picked Bran's fall deliberately as the **maximum contrast** to RR's historical/wiki profile (on-page present-narrative AGOT). Built `witness → push → catspaw → capture` (4 beats), all Tier-2 causal + role edges, verbatim AGOT quotes, fresh-subagent-verified (all CONFIRM).

**Findings the smoke test exposed (the real value):**
1. **🔴 Duplicate-node mint.** `catelyn-captures-tyrion-at-the-crossroads-inn` (my mint) collided with the pre-existing Plate-3 beat `catelyn-seizes-the-moment-and-arrests-tyrion` (verbose slug, 6 role edges). My slug-guessing existence check missed it; the alias resolver caught it post-mint. Deleted the dup, repointed the edge, enriched the canonical node. **→ pre-mint dedup lookup is now a mandatory template step.**
2. **Cost model correction.** "Tier A = mostly wiring" is half-wrong — dyads exist densely but beat-hubs are a patchwork (only where Plate 3 minted them). Real cost ≈ "mint 2-3 + discover-and-reuse 1-2."
3. **Thin-hub gap.** The two beats I minted carried only causal edges (no participants/location); the two Plate-3 beats were rich. Filled role edges (AGENT_IN/VICTIM_IN/LOCATED_AT) on the new beats after Matt asked "shouldn't there be more edges connected to this?"
4. New arc nodes inherit the Track-7 alias-discoverability weakness; `--path` can't walk a 3-hop directed chain (tooling gap).

## Part 3 — advisory board (Matt-requested)

Fanned out 4 parallel Sonnet advisors (narrative-craft / graph-modeling / canon / skeptic) on the arc-shape question. Outcomes:

**Consensus fixes applied (all subagent-verified):**
- **Inserted the missing causal hinge** `littlefinger-names-the-dagger-as-tyrion-s` (`event.deception`): canon + craft both flagged that `catspaw → capture` skipped Littlefinger's false attribution of the dagger — the *actual* cause. Removed the over-collapsed direct edge; routed catspaw → littlefinger-lie → capture. Added DECEIVES petyr→catelyn.
- **Extended one hop, hard-stop:** minted `gregor-raids-the-riverlands` (`event.incident`), wired `capture CAUSES gregor-raids`. Did NOT chain to `war-of-the-five-kings` (skeptic + canon: causation past this point is multi-attributed).

**Parent-node decision (my recommendation, for Matt's ratification): causal-chain-as-arc, NO umbrella parent nodes.** Deliver "show me the whole arc" via a `--causal-chain` traversal primitive instead of a parent hub. Dissolves both the graph-modeler's "no landing zone" need and the skeptic's multi-parent-ownership trap (Bran's fall belongs to ≥5 overlapping arcs — no single parent can own a beat). No curator-invented names, no premature `event.arc` type. Supersedes the umbrella-vs-chain fork in the parked arc-wave1 prompt. Prerequisite: build the directed-chain primitive (Track 7).

## Part 4 — Matt's agency-collapse catch (generalizable lesson)

Matt then questioned `capture CAUSES gregor-raids` — shouldn't it be "capture causes **Tywin to order** Gregor to raid"? Correct, and the same agency-collapse class as the Littlefinger hinge. Used the locked `MOTIVATES` (event→actor) for the first time: added `capture MOTIVATES tywin-lannister`; the existing `tywin COMMANDS_IN gregor-raids` completes the agency chain. Kept the coarse `CAUSES` as the event→event summary.

**Distilled into a standing rubric check** (added to the strategy doc §): *before emitting `A CAUSES B`, ask whose decision sits between them. If a person chooses to act, model the agency — insert the decision as a beat node (if it's a scene, e.g. Littlefinger) OR `MOTIVATES`→actor + the actor's COMMANDS_IN/AGENT_IN on B (if it's a choice, e.g. Tywin).*

## Final arc + state

```
bran-witnesses-jaime-and-cersei ─TRIGGERS→ jaime-pushes-bran-from-the-tower
  ─CAUSES→ bran-s-direwolf-kills-the-assassin
    ─CAUSES→ littlefinger-names-the-dagger-as-tyrion-s   (DECEIVES catelyn)
      ─CAUSES→ catelyn-seizes-and-arrests-tyrion
        ─CAUSES→ gregor-raids-the-riverlands             ← HARD STOP
        └─MOTIVATES→ tywin (COMMANDS_IN gregor-raids; gregor AGENT_IN)
```

- `edges.jsonl` 22,157 → **22,174** (net +17 this session's run_id; 1 weak edge removed during the Littlefinger fix). Edge types **127 → 128** (`MOTIVATES` now live).
- Nodes 8,521 → **8,525** (5 new beat nodes minted, 1 dup deleted; 2 pre-existing beats enriched).
- 62 orphans unchanged. pytest 1297 pass / 1 documented `cwd-is-tmp` env-fail.
- Backups: `_regrounding/edges-pre-bran-arc-2026-06-18.jsonl`, `edges-pre-bran-arc-littlefinger-fix-2026-06-18.jsonl`.

## What's next
- **Matt ratifies the parent-node recommendation** (causal-chain + traversal primitive, no parent hubs).
- Build the `--causal-chain` directed-traversal primitive (Track 7 query-tooling) — prerequisite for arc value.
- First real arc batch (Tier A: Sack of KL, Purple Wedding) — dip-gated, with the pre-mint dedup lookup + agency-collapse check folded in.
