# Narrative-Arc / Causal-Arc Glossary

> **Status:** Consolidation doc — *documents* terminology already decided and in use across Sessions
> S82–S105. Coins nothing new; changes no decision. Read-only companion to two other reference files.
>
> **What this doc is.** A definitions index for the causal / narrative-arc layer of the graph: the
> concepts, node kinds, edges, method gates, and tooling the project uses when it reifies a GRRM
> consequence-chain into structured nodes + edges. Each entry is tight and cross-references the
> authoritative source rather than restating it.
>
> **Relation to the other two reference files (do not duplicate them):**
> - `reference/glossary.md` is the **process vocabulary** — Pass / Track / Tier / lowercase `step`.
>   That file owns *how we name and sequence work*. This file owns *the data-model / method terms*.
> - `reference/architecture.md` is the **edge & node-type schema** — the authoritative definitions of
>   every edge type (`CAUSES`, `TRIGGERS`, `PART_OF`, `AGENT_IN`, …) and every `event.*` node type.
>   Where this doc names an edge, the formal definition lives there; we summarize and cross-link.
>
> **A note on `Tier`.** Per `reference/glossary.md`, `Tier` means **confidence 1–5 ONLY** — never a
> work-class or process label. Every "Tier-1 / Tier-2" mention below is a confidence rating on data.

---

## Arc concepts

### causal arc
A reified consequence-chain: a set of beat-nodes wired together with causal edges (`CAUSES` /
`TRIGGERS` / `MOTIVATES`) so the graph carries the *consequence* logic a reader narrates, not just
sequence. Synonymous in practice with **narrative arc** as the project uses the terms; "causal" stresses
that the connective tissue is consequence edges. *Used in:* `working/causal-arc-strategy-2026-06-18.md`.
*Example:* the Robert's-Rebellion spark chain `tourney-at-harrenhal → abduction-of-lyanna →
executions → aerys-demands-ned-and-robert → roberts-rebellion` (S104).

### causal chain
The concrete ordered path of beats joined by causal edges — the runtime object the
`--causal-chain` query primitive recovers. The project's settled shape for an arc is a *chain*, not a
parent node (see **chain-as-arc model**). *Example:* the Bran's-fall chain
`bran-witnesses-jaime-and-cersei → jaime-pushes-bran-from-the-tower →
bran-s-direwolf-kills-the-assassin → littlefinger-names-the-dagger-as-tyrion-s →
catelyn-seizes-the-moment-and-arrests-tyrion → gregor-raids-the-riverlands` (S105).

### narrative arc
The narrative-craft framing of the same object — the consequence-chain GRRM writes in. The graph
historically stored *events* (battles, weddings) but not the arcs connecting them; the narrative-arc
reification track (surfaced S95, memory `project_narrative_arc_reification`) applies event-hub
reification "one level up" to capture these chains. *Used in:* memory `project_narrative_arc_reification`;
first instance shipped S95 (the Incident-at-the-Trident arc).

---

## Node concepts

### beat / beat-node
A single reified narrative moment that anchors role edges and participates in a chain — a node for a
*moment within* a larger event, finer-grained than a battle or ceremony hub. Beat-nodes are minted only
when the moment is reader-named, load-bearing in a chain, and lacks an existing node. *Example:*
`jaime-pushes-bran-from-the-tower` (a beat inside the Bran's-fall arc, S105).

### hub / event-hub
A reified event node that other nodes attach to via role edges and containment — the n-ary event
"reification target." Coarse hubs are whole events (a battle, a wedding); finer hubs are beat-nodes.
See `reference/architecture.md` `event.*` node types (e.g. `event.incident`, `event.deception`).
*Example:* `red-wedding` is a hub with `SUB_BEAT_OF` children; `sack-of-kings-landing` is a hub in the
Trident→Sack pilot.

### spark-node (a.k.a. spark-beat)
A beat-node minted specifically to name the *immediate spark* that `TRIGGERS` a downstream event —
the discrete moment a coarse parent node doesn't name on its own. *Used in:* worklog S104 ("3
spark-beat nodes"). *Example:* `aerys-demands-ned-and-robert`, minted S104 so the chain could assert
`aerys-demands-ned-and-robert --TRIGGERS--> roberts-rebellion`.

### thin hub
An event-hub minted with little or no structure attached — no role edges naming who acted, who was
acted upon, who ordered, what instrument was used. A thin hub is a near-empty placeholder: it exists
but doesn't answer "who did what to whom here," so traversals through it return nothing. The standing
rule is therefore: **every minted beat should carry role edges** (see **role edges**) so it is a real,
queryable hub rather than a thin one. *Used in:* the reification direction, memory
`project_edge_modeling_reification_direction`.

---

## Edge concepts

> All edge definitions below are summaries; the authoritative text lives in `reference/architecture.md`.

### role edges — `AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, `WIELDED_IN`
The four reification participant-slot edges that attach characters / houses / artifacts to an event
hub, replacing (or supplementing) a flat dyadic edge:
- `AGENT_IN` — the executor who performed the act (person/house → event).
- `VICTIM_IN` — the patient on whom the act was performed (person/house → event).
- `COMMANDS_IN` — the orderer/instigator who did *not* personally execute (person → event/war); also
  covers military command.
- `WIELDED_IN` — the instrument used in the event (artifact → event).

Together they cover the standard slots (no `INSTRUMENT_IN` type needed — `WIELDED_IN` fills it). Role
edges record *factual presence* and so stay **Tier-1**. Every minted beat should carry them so it isn't
a **thin hub**. *Defs:* `reference/architecture.md` (AGENT_IN/VICTIM_IN/COMMANDS_IN rows + the
"Reification role vocabulary note"; WIELDED_IN in Possession & Artifacts). *Example:* the Bran's-fall
beats each carry role edges (S105); `capture` additionally carries the actor's `COMMANDS_IN`.

### `CAUSES` vs `TRIGGERS` vs `MOTIVATES` vs `PRECEDES`
The four edges most often confused in this layer. Distinctions (per `reference/architecture.md`
Causal & Plot / Temporal & Sequencing):
- `CAUSES` — Event A leads to Event B; the *mediated / coarse* causal link. **S104 rule:** at coarse hub
  granularity (a whole-battle node) use `CAUSES`, because the node doesn't name a specific spark.
- `TRIGGERS` — the **immediate, specific spark** (narrower than `CAUSES`). Use only when a named
  spark-beat is the trigger. *Example:* `bran-witnesses-jaime-and-cersei --TRIGGERS-->
  jaime-pushes-bran-from-the-tower` ("The things I do for love"), S105.
- `MOTIVATES` — event/condition → **actor**: the link drives a *character's* decision rather than
  directly producing the next event. Used by the agency-collapse fix. *Example:* `capture MOTIVATES
  tywin` (S105) — Tywin's choice to retaliate sits between the capture and the raids.
- `PRECEDES` — **pure chronology, NOT causal.** Derived deterministically from `occurred.ac_year`;
  asserts only that one event is earlier. If `PRECEDES` already captures the relationship and there is no
  consequence, do **not** add `CAUSES`/`TRIGGERS` ("sequence masquerading as cause" anti-signal).

(`ENABLES` = condition makes B possible; `PREVENTS` = action blocks B — same Causal & Plot section,
less central to the shipped arcs.)

### containment edges — `PART_OF` vs `SUB_BEAT_OF`
Two containment edges kept deliberately distinct because they operate at different scopes:
- `PART_OF` — **event-in-war** scope: a battle/sub-event is a component of a larger war (battle → war),
  coarse-grained.
- `SUB_BEAT_OF` — **beat-in-event** scope: a finer beat is a moment *inside* a named event hub (beat →
  parent event), enabling temporal-granular "what happened before X started" queries that collapse away
  if the beat is folded into the parent.

They are not interchangeable: a beat inside the Red Wedding is `SUB_BEAT_OF red-wedding`, never
`PART_OF`; a battle inside a war is `PART_OF`, never `SUB_BEAT_OF`. Keeping them separate preserves the
two distinct query shapes. *Defs:* `reference/architecture.md` `PART_OF` / `SUB_BEAT_OF` rows.

---

## Method & policy

### reification
The core modeling move: turn an n-ary event into an **event-hub node** and attach participants via
**role edges**, instead of forcing it into a flat dyadic edge. Two altitudes:
- **event-hub reification** — reify the event itself (a wedding, a battle) to a hub with `AGENT_IN` /
  `VICTIM_IN` / `COMMANDS_IN` / `WIELDED_IN` role edges (S82–S87 direction, memory
  `project_edge_modeling_reification_direction`).
- **arc reification ("one level up")** — apply the same principle to the *consequence-chain* connecting
  events: mint beat-nodes and wire causal edges so the arc is structured, not implicit (S95, memory
  `project_narrative_arc_reification`).

### chain-as-arc model (NO umbrella parent nodes)
The settled shape for an arc: deliver it as a **causal chain of beats walkable by query**, with **no
umbrella parent node** owning the arc and **no `event.arc` type**. The parent's only real value
("show me the whole arc") is delivered by the `--causal-chain` traversal primitive instead.
**Settled S105** via a 4-lens advisory board (narrative-craft / graph-modeling / canon / skeptic) plus
the arrival of the `--causal-chain` primitive. The decisive objection came from the **skeptic**: a
single beat belongs to *many overlapping arcs* (Bran's fall sits in ≥5), so no single parent can own a
beat — the rejected `event.arc` parent-hub alternative would force a false single-owner. *Status:* the
recommendation awaits Matt's ratification (worklog S105). *Source:* `working/causal-arc-strategy-2026-06-18.md` §7.

### agency-collapse check
A hard wiring-gate: before emitting `A CAUSES B`, ask **whose human decision sits between A and B.** If
a person *chooses* to act, model that agency rather than letting it vanish inside a blunt event→event
arrow — either insert the decision as its own beat-node (if it's a scene) **or** use `MOTIVATES` →
actor plus the actor's `COMMANDS_IN` / `AGENT_IN` on B (if it's a choice). The causal-layer analogue of
the reification principle. *Source:* `working/causal-arc-strategy-2026-06-18.md` §7. *Examples (both S105):*
`catspaw-fails → capture` hid Littlefinger's lie → inserted `littlefinger-names-the-dagger-as-tyrion-s`
as a beat; `capture → gregor-raids` hid Tywin's choice → `capture MOTIVATES tywin` + Tywin's role edge.

### pre-mint dedup lookup
A **mandatory** step before minting any beat-node: run its description through
`weirwood query resolve "<phrase>"` and eyeball the fuzzy index (every match
≥ ~0.6) before creating the node. Slug-guessing misses pre-existing beats — the ~200 verbose-slug
"Plate-3" reified beats are the main collision surface. *Source:* `working/causal-arc-strategy-2026-06-18.md`
§6. *Example (S105):* `catelyn-seizes-the-moment-and-arrests-tyrion` already existed as a Plate-3 beat; a
hand-rolled slug guess minted a duplicate that had to be deleted and repointed.

### hard-stop discipline
Don't chain `CAUSES` into a **multi-attributed terminus**. Past a certain point causation is a thesis,
not an edge — e.g. do **not** assert anything `CAUSES war-of-the-five-kings`. Stop the chain where the
next link would require attributing a multi-causal historical outcome to one beat. *Source:*
`working/causal-arc-strategy-2026-06-18.md` §7. *Example (S105):* the Bran's-fall chain hard-stops at
`gregor-raids-the-riverlands` — no edge onward to WO5K.

### Tier-2 cap policy (causal / interpretive edges)
Causal/interpretive edges cap at **Tier-2**, even when both endpoints have Tier-1 chapter quotes,
because the *events* may be canon but the causal **link** is an interpretation. **Role edges** (factual
presence) stay **Tier-1**. (`Tier` = confidence 1–5 only — never a work-class.) *Source:*
`working/causal-arc-strategy-2026-06-18.md` §5 Q1 + §6. *Example (S105):* every Bran's-fall causal edge is
Tier-2; the role edges on those beats are Tier-1.

### evidence_kind values (this layer)
The `evidence_kind` discriminators that tag causal/arc edges by provenance:
- `book-pass1` — grounded in in-saga POV chapter text (Pass-1 source). *(Bran's-fall arc, S105.)*
- `wiki-historical-anchor` — grounded in wiki-attested deep-lore / pre-narrative history (Tier-2 cap).
  *(Robert's-Rebellion chain, S104.)*
- `derived-chronology` — deterministically derived ordering (`PRECEDES` from `occurred.ac_year`), Tier-3.
- `causal-curator-pilot` — the curator-minted causal pilot edges. *(Trident→Sack→Coronation, S104.)*

---

## Tooling & cadence

### `chain` query primitive
`weirwood query chain <slug>` — walks `CAUSES` / `TRIGGERS` / `MOTIVATES`
transitively **in both directions** from any beat, recovering the whole consequence-chain (ancestors +
descendants) regardless of which beat you start from. This primitive is what makes the **chain-as-arc
model** viable: it delivers "show me the whole arc" without a parent node, and dissolves the
multi-parent-ownership trap (any beat reaches its arcs by walking). *Status:* prerequisite to build
(Track 7 query-tooling) before the first real arc batch; worklog S105 NEXT TRACK. *Source:*
`working/causal-arc-strategy-2026-06-18.md` §6–§7.

### dip / Mode-3 grounded-agent dip / "dip-driven" cadence
A **dip** (a.k.a. the *Mode-3 grounded-agent dip*) is a validation probe: an agent restricted to
**graph-only** answers is posed reader-style questions; the queries it fumbles — for lack of structure —
are the evidence that *orders what gets built next*. **"dip-driven"** cadence means arc work proceeds in
small batches (3–5), shipping a validating batch and then re-running an arc-weighted dip to let *its*
failures re-rank the next batch — **not** mass-minting up front. *Source:*
`working/causal-arc-strategy-2026-06-18.md` §4 ("Cadence recommendation: dip-driven, small batches… NOT
mass-mint") + the rubric's Query-value signal ("would a grounded-agent dip fumble an arc-shaped question
here?"). ("Mode 3" is a retired term decoded by `reference/glossary.md` = "the grounded-agent dip.")
