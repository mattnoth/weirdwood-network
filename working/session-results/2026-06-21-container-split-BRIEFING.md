# Container-split advisory fan-out — shared briefing (S121)

> Read this, then do ONLY your assigned lens (your dispatch prompt names it). Read-only — write ONLY
> your one report file. No external fetches; everything is local.

## Vocabulary (paste — you don't load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · step (lowercase) = ordered piece inside a track ·
Tier = confidence 1–5 ONLY (never a stage of work). A **container** = a big storyline tackled as a build
unit (Essos, WO5K). Don't invent capitalized process words.

## The model (read these files first)
- `working/session-results/2026-06-21-container-advisory-board.md` — the prior board that named two missing containers.
- `graph-concepts-explainer.md` (gitignored, on disk) — chain-as-arc, NO umbrella parent node; an arc is a
  walkable causal PATH, not a bag-node; a **container is a frontmatter TAG** (`containers: [essos]`), NOT a
  graph object; §7 covers convergence/divergence hubs.
- `reference/architecture.md` §"`containers:` field" — the adopted design (array tag; bag-retrieval via
  `--container`; seam nodes carry BOTH containers, e.g. `[wo5k, essos]`, built once; never `[]`).
- `reference/foreshadowing-events.md` — the 30 anchored dark events that need container homes.
- `working/essos-decomposition.md` + `working/wo5k-decomposition.md` — the two existing container decomps
  (format exemplar + the seam annotations already added this session).
- `working/dyad-queue.md` — E7 (Varys/Illyrio → AEGON) + E8 (Jorah) extracted out of Essos as dyads.

## Ground every claim against the live graph
`python scripts/graph-query.py --neighbors <slug>` · `--causal-chain <slug>` · `--full-chain <slug>`
(NEW: follows ENABLES too) · `--container <name>` (NEW: bag-retrieval) · `python scripts/event_alias_resolver.py --lookup "<phrase>"`.

## Current state (S121)
- Built containers: **ESSOS** (Daenerys spine E1–E5 done; 15 nodes now tagged `containers: [essos]`) and
  **WO5K** (partially built; `robert-orders-daenerys-assassination` tagged `[essos, wo5k]` as a seam,
  `littlefinger-betrays-ned` tagged `[wo5k]`).
- The S120 board named two MISSING containers: **NORTH/Wall** (Watch/wildling/political theater — NOT
  "the White Walkers", which are sparse in the text) and **AEGON / Targaryen-restoration**
  (Varys/Illyrio tunnel conspiracy → JonCon/fAegon → Golden Company landing → Varys kills Kevan).

## The four causal edge types (use ONLY these; never invent edge types)
CAUSES (produces, mediation ok) · TRIGGERS (immediate spark) · ENABLES (precondition, doesn't force —
preserves third-party/dragon/human agency) · MOTIVATES (drives an ACTOR's decision; target = character).

## The four lenses (you do ONE)
- **LENS A — set + scope.** Is {Essos, WO5K, NORTH, AEGON} the right partition of the remaining major
  storylines, or are others needed / some better as sub-threads? Map each of the 30 foreshadowed events to
  its best container (flag any that fit none). Scope NORTH and AEGON: boundary (in/out), spine root +
  terminus, 4–8 candidate junctures each with a one-line build-readiness note (`--neighbors` to check node
  existence). Confirm Essos E7 belongs to AEGON. List boundary collisions between containers your scoping
  exposes. → `working/session-results/2026-06-21-container-split-lensA-set-scope.md`
- **LENS B — Jon/Bran granularity.** Are Jon Snow and Bran big enough to be their OWN containers vs
  sub-threads of NORTH? Containers are multi-valued tags (a node can carry `[north, jon]`), so "own
  container" and "part of NORTH" are NOT exclusive. Inventory Jon's + Bran's buildable junctures (use
  `reference/pov-characters.md` counts + foreshadowed events + `--neighbors`/`--causal-chain`); compare to
  Essos (~8) / WO5K (~6–10) as the container-size bar. Analyze how much each intersects NORTH vs stands
  apart. Recommend ONE: (a) Jon+Bran each own container; (b) both sub-threads tagged `[north]` only; (c)
  hybrid dual-tag the overlap. Give concrete example slugs + their `containers:` arrays. Note build-order
  dependency vs NORTH. Avoid micro-containers nobody queries; never `[]`.
  → `working/session-results/2026-06-21-container-split-lensB-jon-bran.md`
- **LENS C — seams + dual-membership.** Enumerate ALL cross-container seams (known: `robert-orders…` =
  WO5K∩Essos; `capture-of-winterfell`/`sack-of-winterfell` + the Theon/Reek arc = WO5K∩NORTH; Dany's
  Westeros thread = Essos∩AEGON). Look hard for non-obvious ones (Stannis: Blackwater[WO5K]→Wall[NORTH];
  the Pink Letter linking Ramsay[NORTH]↔Stannis[WO5K]; Davos). For each: which containers, which node(s),
  built or not (`--neighbors`/`--causal-chain`). Give the **build-once ownership rule** (which container
  authors the node, which just adds its tag — propose a simple rule and pressure-test on Theon/Reek: WO5K
  or NORTH? recommend). Clarify **bridge vs seam** (a bridge has causal edges crossing the boundary; a
  pure seam is claimed by both but causation doesn't cross). Give a builder checklist for boundary nodes
  (prevent: double-built dups, orphans claimed by neither, tag-in-X-but-spine-roots-in-Y).
  → `working/session-results/2026-06-21-container-split-lensC-seams.md`
- **LENS D — retro-grouping standalones.** The ~12 already-built standalone arcs (RR · Bran's fall · Sack
  of KL · Purple Wedding · Tywin's death · B1 Red-Wedding-upstream · B2 Greyjoy→Theon-ward · B3
  Ned's-downfall · the 4 AFFC arcs · the new littlefinger-betrays-ned) are currently UNtagged. Classify each:
  clean single container / dual / genuine standalone (stays null). Build a table arc→root slug→recommended
  `containers:` value. Cost/benefit of retro-tagging now vs deferring (note: a half-tagged graph makes
  `--container` MISLEADING — is partial worse than none?). Recommend ONE: (a) tag all now, (b) tag only the
  clean subset now + leave standalones null, (c) defer entirely (stamp-as-built going forward). Confirm the
  float policy (omit key or `null`, NEVER `[]`). Weigh against architecture's "retro-tagging is a separate
  decision, not automatic." → `working/session-results/2026-06-21-container-split-lensD-retrogroup.md`

## Output discipline
Tight report to your named file. Final chat message = 8–12 line executive summary with your single clear
recommendation. Causal edges cap at Tier-2. Don't assert unproven agency as fact (that's `SUSPECTED_OF`, Tier-2).
