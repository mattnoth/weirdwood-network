---
session: 206
title: Cross-era seams — wire the F&B/Targaryen layer to the main-series graph
date: 2026-07-10
track: graph
model: Sonnet 4.6 orchestrator + 2 Haiku fresh-verifiers
graph_mutation: YES — commissioned by the S206 continue prompt (arc-enrichment dip machine)
---

# Session 206 — Cross-era seams

## Purpose
The S200–S204 work built a whole Fire & Blood / Targaryen-history layer that was an **island**:
causally spined *within* the F&B era (S204) but not connected to the main-series (GoT-era) graph.
This session wired the two eras together, both directions, and absorbed the S204/S205 residue flags.

## What was done

### The two swords (the marquee deliverable)
Both persistent Valyrian steel swords were near-islanded (`dark-sister` had **0 edges**, `blackfyre` had 1).
Their entire holder lineages were present as node prose (wiki-derived) but unwired. Wired them with
**verbatim book/fab/D&E chapter quotes** (the book-citation overlay — navigable, not wiki repetition):
- **Dark Sister 0→10 edges:** Visenya → Maegor (GIFTED) → Jaehaerys → Baelon → Daemon the Rogue Prince
  (GIFTED) → Aemond kill at the Battle Above the Gods Eye → **Bloodraven** (tss). The marquee traversal
  `bran-stark → brynden-rivers (TUTORS) → dark-sister (WIELDS)` now crosses the ~170-year gap: a
  main-series reader reaches the Dance through Bran's own mentor.
- **Blackfyre 1→8 edges:** Aegon I / Maegor / Jaehaerys holders + `WIELDED_IN third-dornish-war` +
  the **D&E seed** `blackfyre GIFTED_TO daemon-i-blackfyre` (tmk) + `maelys FIGHTS_IN
  war-of-the-ninepenny-kings` (BF8; the pre-existing `barristan-selmy KILLS maelys` already reached the
  Blackfyre line's end from the main series). **Matt-flagged dual-house fix:** added `blackfyre
  ANCESTRAL_WEAPON_OF house-targaryen` (tss:1289, "the blade that every Targaryen king had wielded since
  the Conquest") alongside the pre-existing `→ house-blackfyre`. Querying House Targaryen's ancestral
  weapons now correctly returns **both** swords.
- **Dragon skulls:** minted `dragon-skulls-of-the-red-keep` (object.artifact) → `LOCATED_AT red-keep` +
  `MADE_OF dragonbone`, prose naming Balerion/Vhagar/Meraxes — the persistent trace of the F&B dragons
  in the main-series throne room (Tyrion in the cellar, agot-tyrion-02).

Net **+20 edges (19 + 1 supplement), +1 node** (edges 25,293 → 25,313). One dedup skip
(`barristan KILLS maelys` already existed — the graph already had one main-series↔Blackfyre seam).

### D&E clarification (for the record)
The D&E novellas' **source text is ingested** (chapter-splitter ran: `sources/chapters/{thk,tss,tmk}/*.md`
exist and are grep-able). What is **not** done is D&E Pass-1 mechanical extraction (that track is parked).
So this dip read the raw novella chapters directly — exactly as the continue prompt instructed — and
several marquee seams (Bloodraven's Dark Sister, Daemon's Blackfyre) are grounded in navigable D&E cites.

### Residue hygiene (S204/S205 flags, 6 items, all deterministic)
- `lord-rogars-war` **folded** into `third-dornish-war` (confirmed the same event — the third-dornish-war
  node already carried the "smallfolk called it Lord Rogar's War" quote; 0 edges lost). Alias added;
  retyped `event.battle → event.war`.
- `maidens-day-ball → event.feast`; `regency-of-aegon-iii → event.council`; `archon-of-tyrosh-…`
  retyped **`event.war → character.human`** and moved `events/ → characters/` (its infobox fields —
  HOLDS_TITLE Archon of Tyrosh, CULTURE_OF Tyroshi — are person-fields; it is the deposed Archon, a
  person conflated with the war).
- `assault-on-harrenhal DEFEATS blacks → greens` (backwards Result — the blacks *won* the assault).

**Retype rationale for the hard one (`regency-of-aegon-iii`):** genuinely ambiguous between a governance
period and a governing council. Its edge structure decided it — 7 incoming `MEMBER_OF` (the regents) +
`HOLDS_TITLE`/`SWORN_TO` (org-shaped) alongside `PRECEDES`/`TRIGGERS`/`occurred:`/`sort_keys` (event-shaped).
Chose `event.council` (an established F&B type, 9 nodes, matches the great-council-of-101-ac precedent):
it keeps the node in the Event hierarchy (preserving the curated temporal edges + date scaffolding) AND
matches the council-membership semantics — better than forcing it to `organization.faction` (which would
break the temporal edges).

## Discovery: systemic F&B event schema-drift (flagged, NOT fixed — out of scope)
While retyping, found the residue is the tip of a systemic pattern from the F&B bulk apply (S200–S204):
- **`dance-of-dragons`, `hour-of-the-wolf`, `lysene-spring` are all still mistyped `event.battle`** —
  `dance-of-dragons` is THE central F&B event, and it's typed as a single battle (it's a war).
- The F&B pass introduced **~20 off-schema event subtypes not in architecture.md**: `event.death`×141,
  `event.capture`×42, `event.other`×35, `event.ceremony`×24, `event.decree`×10, `event.council`×9,
  `event.voyage`/`negotiation`/`uprising`/`surrender`/`betrayal`/`progress`/`escape`/`disaster`/… ×1–5.
- A proper reconciliation pass should either **sanction** the useful subtypes in architecture.md's type
  table or **retype** to sanctioned leaves, and fix the big mistypes (dance-of-dragons → event.war, etc.).
  This is a schema-drift-auditor-shaped task of its own — queued as backlog, folds naturally with the
  edge-vocab retrofit (both are "make the graph speak the current vocabulary").

## Rigor
- Orchestrator-assembled candidates (WIRE task; substrate was in node prose) → **2 independent adversarial
  Haiku fresh-verify passes, 20/20 CONFIRM, 0 REJECT/0 ADJUST** (incl. same-name Targaryen disambiguation,
  BF5's war-context, the Maelys/last-Blackfyre-pretender identification, dragonbone inference).
- Quote grounding validated by the mint's fail-fast line-check (all 20 located). 0 invented edge/node types.
- Index churn kept surgical: reverted the 8,413 timestamp-only entity-index files, kept only the 10
  meaningful (3 summaries, 3 retypes, 2 adds, 2 orphan deletes). web/data deploy bundle untouched
  (deploy is Matt-gated). pytest **1457 passed** · deno **100 passed**.
- Harvest: 2 open rows at endsession (the 2 pointers this dip dropped — Bittersteel's gilded skull
  adwd-the-lost-lord-01:97; Bloodraven's "a thousand eyes, and one" tss:49). Far below the ~30 drain bar.

## What's next
Graph vocabulary/schema hygiene (edge-vocab retrofit + the F&B event schema-drift found above) →
`progress/continue-prompts/2026-07-10-graph-vocab-hygiene.md`. Strip-boilerplate stays Matt-gated.
