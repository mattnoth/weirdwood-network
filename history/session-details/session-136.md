---
session: 136
title: Enrichment scope-model clarification + 4th-arc board (pre-run)
track: graph
date: 2026-06-23
model: Opus 4.8 orchestrator + Sonnet 4.6 advisory board
graph_writes: none
---

# Session 136 — Enrichment scope-model clarification + 4th-arc board

## What this session was

The continue prompt fired this as "the fourth major-arc enrichment dip." It did **not** run the dip.
Instead it (a) ran the 3-advisor board that the prompt's STEP 1 calls for, and (b) — prompted by a
sharp question from Matt — surfaced and resolved a long-latent conceptual confusion about *what scale*
enrichment operates at, then codified the resolution. The dip itself was deferred to S137 at Matt's
direction ("let's just do the S136 dip next session now that I understand it"). No nodes or edges were
minted; the only graph-adjacent artifacts are the three advisor writeups.

## The board (STEP 1 — done)

Three independent Sonnet advisors picked the fourth arc from the READY candidates (Sack of King's
Landing / Ned's downfall / Blackwater). **Unanimous: Ned's Downfall** (`execution-of-eddard-stark`).
- All three: Ned's-downfall is the highest yield-per-edge dip — the conspiracy actors (Littlefinger,
  Janos Slynt, the gold cloaks, Cersei, Renly's offer, Varys) and several sub-events are *already minted
  nodes* but the causal links between them are simply absent. `littlefinger-betrays-ned` has 2 edges
  total and no forward CAUSES. Near-zero theory risk.
- **Sack of KL flagged by all as a double-dip risk** — its richest material (Jaime's kingslaying, the
  wildfire plot, the Elia/Aegon murders) was already wired in the S133 Robert's-Rebellion pass; ~39
  edges already reference its sub-events. Advisor C would actively avoid it.
- **Blackwater = clean #2** (causally orphaned upstream; Sandor-desertion + Mandon-Moore attempt +
  Tyrion-wounding all unwired) — but its hub prose is already rich, so the *graph* gap is narrower.

Writeups: `working/enrichment/s136-board/advisor-{A,B,C}.md`.

## The confusion, and the resolution (the real content of the session)

Matt asked why the dips (and the S136 candidates) are *event-scale* arcs (Red Wedding, Ned's-downfall)
while he'd been picturing the **containers** (WO5K, Essos, North) as "the major narrative arcs." Working
through it:

- He first thought we'd already *enriched* the containers. We hadn't — we **built their spines**
  (S119–S130). Build ≠ enrich; the ledger counts them separately. The containers have 0 enrichment
  passes; only 3 events (RR/RW/PW) have been enriched.
- Then: *why* event-scale and not container-scale? The honest answer is that **it was never a deliberate
  choice** — it falls out of two earlier structural decisions that leave nothing else to grab:
  1. **No umbrella/parent nodes** (S105/S106): an arc is an *edge-chain*, there is no
     `war-of-the-five-kings` node.
  2. **A "container" is a frontmatter tag, not a node** (S121): WO5K/Essos/etc. are labels on bags of
     event nodes, queried via `--container` (bag-retrieval).
  → So "enrich WO5K" has no object to point a dip at. The only enrichable things on disk are **event
  nodes and the edges between them**, making the event-arc the largest *graspable* unit.
- A secondary tangle: "granular." Matt had Ned's-downfall filed as granular; in the descent taxonomy it
  is **level 1** (a major arc). "Granular" (level 2) = the sub-plots *inside* an arc (the gold-cloak
  bribery mechanics, the Frey-pies layer). Small ≠ granular.
- The container-level connective tissue *is* being built — node-by-node, via **lens 4**
  (existing-node↔existing-node causal-wiring), which fires both within a container and across (the S133
  RR→AEGON / RR→Essos seams). That's the mechanism that serves the "wire the whole theater together"
  instinct.

One root-cause note: Matt's own S131 descent text lists **both scales at level 1** ("Red Wedding,
Robert's Rebellion, the Essos/Dany spine, the AEGON invasion, the WO5K") — which is exactly the wording
that made it feel like execution had dropped down a level when it hadn't.

## Codified

- **`working/arc-enrichment-backlog.md`** — new top section **"The scope model — why we enrich EVENTS,
  not 'containers'"** (read-first framing for the whole ledger).
- Memory **`project_arc_enrichment_track`** — a SCOPE MODEL paragraph as a recall trigger pointing back
  to the ledger section.

Chosen homes deliberately: long form in the ledger (durable, read-first by every enrichment session),
short form in memory (recall). Not the worklog (Session Log churns; this is stable reference).

## Process note (a wrinkle worth remembering)

One `AskUserQuestion` this session offered an option ("Something else — let me explain") that Matt found
"damn near insulting" — it handed his direct question back to him instead of answering. Lesson: when a
question is a genuine "why did we decide X," answer it from the record directly; reserve clarifying
questions for forks where the user's answer actually changes what gets done.

## Minor flags surfaced

- A stray `containers: [jon]` tag exists on 4 nodes (North-build leak) — not one of the approved 5
  containers. Cleanup item (logged to todos § Small Fixes).
- `reference/architecture.md` is uncommitted-modified in the working tree but was **not** touched this
  session — likely a parked-D&E-track artifact (the owed `:161` doc-fix). Left unstaged + flagged.

## Next

S137 = the Ned's-downfall enrichment dip. Board already chose, so S137 skips STEP 1 and runs the 4-lens
machine directly. Continue: `progress/continue-prompts/2026-06-23-enrichment-phase-s137-neds-downfall.md`.
