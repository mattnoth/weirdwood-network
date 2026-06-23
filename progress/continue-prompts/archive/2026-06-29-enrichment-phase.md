# SESSION 133 — Enrichment phase opens: harvest-consume on-ramp → first major narrative-arc enrichment

> **This is Session 133.** Stamp your worklog entry `### Session 133` at endsession.

> **Recommended model:** Sonnet 4.6 (Opus 4.8 orchestrator + Sonnet-class `general-purpose` subagents: the enrichment fan-out lenses + independent fresh-verify). Same machine family as the container builds.

> **Parallel-safe** with the Dunk & Egg track (`2026-06-29-dunk-egg-pass1-smoke.md`) — different windows, no shared files.

## Context — the phase boundary
**All 5 approved containers are spine-complete** (essos / wo5k / north / aegon / bran) AND **both low-value remainders are now CLEARED** (S132: AEGON Victarion-voyage wire + NORTH N6 Stannis-marches-south). The roadmap therefore crosses into the **enrichment phase** — second-pass deepening of already-built units. Running ledger + full machine: `working/arc-enrichment-backlog.md` (memory `project_arc_enrichment_track`).

**Matt's S132 sequencing (FIRM):**
- **One enrichment dip per session** — enrichment is its own session each time; don't bolt it onto a build.
- **The order is a top-down DESCENT:** (1) **major narrative arcs FIRST** → (2) **granular clusters / sub-plots WITHIN those arcs** → (3) **individual characters (maybe, LAST)**. Deepen the arc whole before zooming in; most of a character's web gets built as a by-product of the arcs they appear in.
- **No "lead," broad roster.** Within any level everything matters — no standing #1. **Bloodraven is ONE of many character candidates, NOT the focus** ("there should be more characters so we don't focus solely on him"). If characters are ever ranked, Jon Snow + Daenerys are the raw heavyweights.
- **A dedicated PLANNING session sits between the arc phase and the granular phase** — it enumerates/scopes the granular dip list once the arc work is done (the granular entries in the ledger are seeds, not the plan).

## STEP 0 (this session's on-ramp) — HARVEST-CONSUME the queue
**The harvest-consume is the on-ramp to enrichment, not an afterthought** (this is the fix for the silent accumulation — 18 Bran rows sat un-consumed across S129–S131). `working/harvest-queue.md` is at **33 open** rows. Consume them as the first act:
- **18 Bran rows** (`bran-dip` / `bran-build-batchA` / `bran-build-batchB`) — attach quotes/descriptions to the 8 BR beat-nodes' `## Quotes` sections; **several are MINT candidates** (weirwood-paste food node, the Black Gate as a place, cave floor-bones place) — those are genuine enrichment decisions that **fold into the Bloodraven/Bran character unit** when it runs; mint or defer per the descent (don't rush a node at on-ramp time if it wants the full Bran dip's context).
- **9 Victarion-voyage rows + 6 N6 rows** (`S132 …`) — attach to the just-built Victarion/Stannis nodes' `## Quotes` (Moqorro's fire-visions, the dual-gods motif, the horse-eating attrition, Arnolf's description, etc.).
- Verify every cite against the chapter file before attaching (subagents reconstruct quotes — always check); mark rows `done` / `parked` (homeless).

## STEP 1 — first major narrative-arc enrichment
After the on-ramp, pick ONE **major narrative arc** (level 1 of the descent) and run the enrichment machine on it. Candidates (all at pass 0 except Kingsmoot→Euron at pass 1 — see ledger table): Red Wedding · Robert's Rebellion · the Essos/Dany spine · the AEGON invasion · WO5K (needs many passes) · Purple Wedding · Tywin's death · Blackwater · Ned's downfall · Sack of KL · Cersei's-downfall · Brienne→Stoneheart · Dorne/Queenmaker. Pick by readiness / what a quick dip shows demand for.

**The enrichment machine** (from the ledger, smoke-tested S116): fan out 2–3 fresh subagents, each a different LENS on the built arc (secondary-character sub-arcs · thread/revelation + contemporaneous events + unproven-but-load-bearing claims · descriptive/quote/object depth) → PROPOSE-don't-mint, dedup-check every node → synthesize + decide (forward-dangling cross-book nodes defer) → verify cited lines → mint via `scripts/mint_<unit>_enrichment.py` (backup + re-run guard) → **independent fresh-verify** the interpretive edges → rebuild derived artifacts (`weirwood refresh`) → `verify-edge-quotes` (0 drift) → consume the harvest pointers the dip refills. `SUSPECTED_OF` is available for unproven-but-load-bearing agency (Tier-2, never asserts the act). Increment the unit's **pass count** in the ledger when it ships.

## Vocabulary (PASTE into every naming/sequencing subagent — they do NOT load CLAUDE.md)
Edge types = locked set: CAUSES / TRIGGERS / ENABLES / MOTIVATES / CONSPIRES_WITH / SUSPECTED_OF (+ roles AGENT_IN / VICTIM_IN / COMMANDS_IN / WITNESS_IN / GUARDS / WIELDED_IN + structural SUB_BEAT_OF / PART_OF / LOCATED_AT). "Pass" = corpus sweep · "Track" = named workstream · lowercase "step" = ordered piece · "Tier" = confidence 1–5 ONLY. No new capitalized terms.

## DO NOT
Refetch wiki / any HTTP · mass-mint · mint CAUSES between sibling/sequence beats (granularity overclaim) · pull TWOW-unwritten or gated-theory readings into the causal map (enrichment builds the Tier-1/2 evidence substrate; theory READINGS stay GATED, `project_theories_track_deferred`) · run extractions without asking (`feedback_no_extraction_without_asking`) · `/endsession` without explicit permission.

## Open question for Matt (at session start)
Which major narrative arc to enrich first (or let a quick demand-dip pick)? Default if unspecified: do the harvest on-ramp, then dip across 2–3 arc candidates and enrich the one that shows the most off-spine depth.
