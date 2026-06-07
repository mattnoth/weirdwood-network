# Edge-Modeling Reification — Master Design Document

**Status:** PLAN ONLY. Nothing here has been applied. Every plate is independently approvable.
**Authored:** Session 82+ (2026-06-05), orchestrator synthesis.
**Lineage:** `lineage/EDGE_INVENTORY_ANALYSIS_PROMT.md` (brief) → `lineage/EDGE_INVENTORY_REPORT.md` (inventory) → `lineage/EDGE_MODELING_DECISION.md` (in-session run, repo-aware) + `lineage/EDGE_MODELING_DECISION-cleanroom.md` (independent clean-room run, repo-blind) → `lineage/EDGE_MODELING_PLAN.md` (S82 verification pass) → **this document** (improvements folded in, sectioned for multi-session execution). All lineage files moved from repo root → `working/edge-modeling/lineage/` in Session 83 (2026-06-05) for tidiness.
**Vehicle decision:** The agent fleet is **design-stage only** (no runnable orchestrator/dispatcher/daemon as of S82). The watcher/worker mission pattern targets parallel waves of bounded items; this work is tightly sequenced. **Therefore: hand-authored session prompts, one per plate (§7), launched one at a time.** Not a fleet mission.

---

## 0. How to use this document

This is the single source of truth for the edge-modeling reification project. It is built to survive across multiple sessions and context windows.

- **§1–§4** are the *why* and the *vocabulary*. Read once.
- **§5** is the plate overview (the work breakdown).
- **§6** is the dependency/sequencing graph.
- **§7** is the payload: **each subsection is a complete, copy-pasteable session prompt.** To run a plate, open a fresh Claude Code session and paste that subsection. Each prompt is self-contained — it names its prerequisites, its acceptance criteria, its out-of-scope boundaries, the files it may touch, and a **Recommended model** line (per CLAUDE.md rule on continue-prompts).
- **§9** lists the decisions still owned by Matt.

**Trust hierarchy:** if this document and `worklog.md` ever disagree on project state, **`worklog.md` wins** (CLAUDE.md rule #9). This doc is a task-scoped snapshot; the worklog is live state.

---

## 1. The problem (condensed)

The graph stores two structurally different things as the same `source → target` edge:

- **True binary relations** (`PARENT_OF`, `SIBLING_OF`): exactly two participants, fixed asymmetric roles, **one correct edge shape**. Nothing to decide.
- **Events** (`KILLS`, `ATTACKS`, `BETRAYS`, the Red Wedding): many participants — agent, victim, location, instigator, executor, instrument, outcome — most optional, **no natural head**. Nothing in the world says an attack is "about" its attacker rather than its target.

Flattening an event onto one edge **forces** you to nominate one participant as `source`. Because there's no canonical rule for which, each extraction independently picks a *different* projection of the same event. Downstream that reads as inconsistency or "the model hallucinated different answers." The precise term is **underdetermination**: a single deterministic edge is not uniquely determined by a head-less event. The fix is not "make the model more accurate" — it is "remove the underdetermination by imposing a canonical form."

**Two compounding origins, both confirmed against the repo:**

1. **Grammatical-subject leakage at Pass-1.** `mechanical-extractor.md:176-178` has a `| Character A | Relationship | Character B |` table with **no head-selection rule**. The `python-map` typer then locks direction by column position, and the column was filled from the POV sentence's grammatical subject. Self-witnessing evidence in the live data: `cressen KILLS melisandre` (`asserted_relation: "Killed by"`), `arya CAPTURES sandor`, `tyrion BETRAYS shae`. **232 unordered pairs carry the same edge type in both directions.**
2. **The reification target exists but is empty.** 371 event nodes exist (`graph/index/events/_summary.json`: 304 battle + 35 tournament + 32 war) — but they are structurally empty hubs. The Red Wedding node has **3 outbound edges** (`FIGHTS_IN`, `DEFEATS`, `DEFEATS`) and **zero edges from its participants** (Walder Frey, Roose Bolton, Robb, Catelyn). The project's own S58 audit named this: the classifier "targets the person or the venue instead of the event node — because the event node frequently does not exist… so there is nothing correct to point at."

**The strategy:** finish the event-node architecture the project already began. Reify the multi-party set-pieces onto event-node hubs via role-typed edges; canonicalize the genuinely-dyadic acts with one agent-based head rule; leave the true binaries untouched.

---

## 2. Verification — cleanroom claims vs. actual repo

Matt's verification pass (S82+) checked the clean-room decision doc against the repo. One substantive divergence; it reshapes the backfill plate.

| # | Cleanroom claim | Verified state | Status |
|---|---|---|---|
| 1 | Event-node count is 371 | `graph/index/events/_summary.json` `entity_count: 371` (304 battle + 35 tournament + 32 war) | Confirmed |
| 2 | Red Wedding has 3 outbound edges, none from participants | `red-wedding.node.md` `## Edges`: `FIGHTS_IN`, `DEFEATS`, `DEFEATS` | Confirmed |
| 3 | Pass-1 prompt has a Relationships Observed table with no head rule | `mechanical-extractor.md:176-178` — table exists, no head rule | Confirmed |
| 4 | Haiku emit rows carry a `**title**` field that groups reifiable events | **FALSE as written.** Zero JSON `title` field on emits. The bold-prefix pattern lives in `asserted_relation`/`hint_raw` 100% of the time, but as **per-row narrative micro-beats**, not a groupable event key. Only **5 of 1,617 rows** reference an existing event-node slug. | **DIVERGENT — the cleanroom's backfill lever does not exist** |
| 5 | KILLS edge counts consistent with assumptions | Sample-matched | Confirmed |
| 6 | Proposed role edges absent from architecture.md | `AGENT_IN`/`VICTIM_IN`/`COMMANDER_OF`/`INSTRUMENT_IN`: zero matches. BUT `COMMANDS_IN` (line 214) and `WIELDED_IN` already cover the commander/instrument roles under different names. | Confirmed — **schema delta is 2 net-new types, not 4** |

**Consequences of the verification:**
- (#4) The backfill plate is **not** a filter over existing Haiku emits keyed on `**title**`. It is a fresh deterministic+LLM mining pass over Pass-1 source. See Plate 3.
- (#6) Reuse `COMMANDS_IN` (orderer/instigator) and `WIELDED_IN` (instrument). Add only `AGENT_IN` + `VICTIM_IN`. Vocab goes 163 → 165, not +4.

---

## 3. Key design decisions (improvements folded in)

These are the orchestrator's improvements on the cleanroom Execution Plan. Each is either **resolved here** or **explicitly deferred to a verification plate**.

### D1 — Reuse existing role-edge vocabulary (resolved)
Add `AGENT_IN` + `VICTIM_IN` only. Use `COMMANDS_IN` for the orderer/instigator role and `WIELDED_IN` for the instrument role. Net-new vocab = 2. Honors the project's anti-sprawl instinct ("edge types are cheaper than lost information" is balanced against "one SERVES, not five synonyms").

### D2 — The replace-vs-supplement-vs-project question is THE decision, and it is gated on a repo check (deferred → Plate 2)
Reification only fixes the inconsistency if the scattered binaries are **removed or regenerated**, not merely augmented. If you add `roose-bolton AGENT_IN red-wedding` + `robb-stark VICTIM_IN red-wedding` but *keep* the old `roose-bolton BETRAYS robb-stark` / `walder-frey BETRAYS robb-stark` rows, "who killed Robb" still returns the inconsistent binaries — you've added rows without fixing the bug. Three options:
- **(a) Replace** — deprecate the scattered binaries; participants reach each other only through the hub (pure 2-hop).
- **(b) Supplement** — keep both; accept the redundancy. **Rejected** — re-imports the inconsistency.
- **(c) Project** — keep one *canonical* binary (agent→patient) deterministically generated from the hub, so 1-hop queries survive AND are consistent.
**The choice between (a) and (c) hinges on whether `graph/scripts/graph-query.py` can transparently traverse `person → event → person`.** If it can, (a) is clean. If it can't, (c)'s materialized dyad is required to keep the project's headline query ("who killed X", "who betrayed Robb") working. **Plate 2 verifies this and decides.** Do not start backfill (Plate 3) until D2 is resolved.

### D3 — The hubs to anchor to mostly don't exist; backfill needs a node-minting step (resolved → built into Plate 3)
All 371 event nodes are battle/war/tournament. There are **zero** fine-grained nodes for individual killings/poisonings/defenestrations. The Red Wedding anchors fine (filed under `event.battle`), but **Bran's defenestration, Tywin's privy death, and the Purple Wedding poisoning have no hub** — i.e. exactly the cases that motivated reification. Plate 3 therefore includes a **node-minting sub-step**, and Plate 2 produces the gating count ("how many Pass-1 events have a node vs. need one minted").

> **D3 RE-EXAMINED — 2026-06-05 (Plate 2 findings; this note corrects the paragraph above).**
> Plate 2's coverage join (`working/edge-modeling/plate2-event-coverage.{md,json}`) showed the
> claim above is **partly wrong**, and the real shape is different and more important:
> - **Tywin's privy death and the Purple Wedding poisoning DO have nodes today** —
>   `graph/nodes/events/assassination-of-tywin-lannister.node.md` and
>   `graph/nodes/events/purple-wedding.node.md` both exist. What they lack is **chapter linkage**,
>   not existence. (Bran's defenestration genuinely has no node — original claim holds there.)
> - The real problem is **coverage, not absence**: of 8,384 Pass-1 event entries (8,317 distinct
>   titles), only **1** exact-matched an event-node slug, and only **38 of 371** event nodes have
>   any Pass-1 chapter linkage. The chapter→event index was built from the Wars & Conflicts column,
>   so it catches historical names, not narrative beats.
> - Pass-1 events are overwhelmingly **narrative micro-beats** ("Departure at daybreak"), not named
>   events. A naive reify-all would mint ~8,300 junk hubs.
> **Consequences for Plate 3:** (1) it needs a **chapter-rebind sub-step** for existing nodes (not
> just minting) — a plan addition; (2) reification MUST be **selective** (a kill/death/attack/
> poisoning/wedding/betrayal/capture trigger list), not all-events — this is open Matt question Q1;
> (3) a **fuzzy-title reuse pass** should precede minting so `tywin-privy-death` rebinds to the
> existing `assassination-of-tywin-lannister` rather than minting a duplicate — open Matt question Q2.

### D8 — Reify on n-ary STRUCTURE, not event TYPE (2026-06-06; sharpens Q1 and the §2 disposition)
The disposition table (§2) says "reify the killing/ceremony/siege families." That is too coarse:
it would put a hub around clean one-on-one killings that have no head problem. **The trigger is
structure, not type:**
- **Clean dyad** (single agent + single patient, no instigator/ordering third party, not a
  shared named occasion) → **keep as a direct typed edge** (`KILLS source→target`), direction-fixed
  by Plate 0. **No hub. No hops added.** (Empirically: 0 of the 102 current `KILLS` rows carry an
  instigator signal — almost all are clean dyads. Jaime/Aerys is the archetype: nobody disputes the
  agent, so no hub.)
- **N-ary event** (instigator ≠ executor, multiple killers/victims, OR a named set-piece other
  edges reference) → **reify onto an event hub**, connect participants via role edges, and *Replace*
  the scattered binaries **for that event only**. (Red Wedding, Renly's shadow-death, ordered
  assassinations.)
**Consequence:** D2=Replace applies ONLY to reified (n-ary) events. Clean dyads are never reified,
so the 2-hop only ever exists where the head was genuinely contested — i.e. exactly where the
divergent-collapse bug lives. This also shrinks node-minting to near-zero: the reify-family is ~280
edge instances collapsing to ~100–200 distinct events, and the named set-pieces (sacks, assassinations,
weddings, tourneys) **already have nodes**. **Reuse-before-mint is mandatory** (see Plate 2.5 inventory).

### D4 — Retroactive cleanups are cheap, high-value, and were dropped by the plan; promote them to a first plate (resolved → Plate 0)
- **Head-direction inversion sweep** (the "normalizer", see §4): a deterministic, ~$0, no-LLM script that flips the existing inverted edges using the self-witnessing `asserted_relation` field. Fixes `cressen KILLS melisandre` et al. and the 232 bidirectional pairs on the live graph. The Pass-1 head rule (Plate 1) only fixes *future* extractions; this fixes the *existing* 3,811 edges.
- **Aerys slug-split merge**: `aerys-targaryen` (2 edges, incl. the regicide `KILLS`) vs. canonical `aerys-ii-targaryen` (~8 edges). Both node files exist; traversal is bisected. **Must run before any reification** — reifying onto a phantom slug relocates the bug rather than fixing it.

### D5 — Costing correction (resolved)
The sub-bullet path (Plate 1b) helps only *future* Pass-1 extractions, and no Pass-1 rerun is planned. So **today there are zero sub-bullet-bearing rows**; a "bullets-only" backfill produces nothing. All real Plate 3 backfill against existing data is the legacy/Sonnet path (~$2–10). State the cost honestly as the legacy path, not "≈$0".

### D6 — Haiku-bulk promotion must pass the normalizer first (resolved → Plate 4)
The 1,617 Haiku emits **failed the S74 drift gate** (48% triple-level agreement vs. 70% gate; 56% pair vs. 85%) — and that failure *was* subject-selection drift, which corrupts binary edges too. Promoting ~1,360 "as-is" without first running the head-direction normalizer re-imports the inversion class. Plate 4 routes all promote-candidates through the Plate 0 normalizer before merge, and requires a fresh bucketing review (the counts in the original plan were sample-derived).

### D7 — Causation modeling (resolved — both independent runs converged)
**One event node carrying both roles** (`AGENT_IN` for executor, `COMMANDS_IN` for orderer) — **not** two event nodes joined by a causal edge. "Who was behind Robb's death" is a one-hop role scan; two-node-causal reintroduces the fragmentation. `GATE 2` in the Stage-4 prompt already refuses the merged `instigator → victim` edge, so the role just gives the orderer a home. **Exception:** when the ordering is itself a separately-attested, distinctly-narrated occasion (a documented council/decree), model it as its own node linked via the existing `CAUSES`/`TRIGGERS`. Minority case. *(Both the repo-aware and clean-room runs reached this independently — treat as settled.)*

### D2 RESOLVED — 2026-06-05 (Plate 2)

**Decision: option (a) Replace.** Reification onto event-node hubs is sufficient. Scattered person→person binaries that are superseded by a reified hub get marked `superseded_by` (NOT deleted; CLAUDE.md hard rule on source data + per D4 normalizer's same convention). No materialized agent→patient dyad will be generated. `--path` traverses person→event→person transparently — the 2-hop headline query ("who killed Robb", "who betrayed X") survives without any new binary projection.

**Why this decision:**
- `scripts/graph-query.py:794-809` (`cmd_path`) performs an untyped 2-hop bridge intersection over the whole `edges.jsonl`. No node-type filter, no edge-type filter. Any common neighbor — character, house, location, **event** — appears as a bridge.
- Live probes confirmed: `--path eddard-stark robb-stark` already returns bridges through `winterfell` (location.castle) and `house-frey` (house.*); `--path robb-stark roose-bolton` returns 12 bridges including `house-frey` and `hornwood`. Plate 3's role edges onto event-node hubs will appear via the same mechanism — `--path walder-frey robb-stark` will surface the `red-wedding` bridge with `AGENT_IN`/`VICTIM_IN` legs once the role edges land. Engineering work needed to make this happen: zero.
- Option (c) Project's deterministic materialized dyad was attractive insurance, but it solves a problem `graph-query.py` doesn't have, and re-introduces the **underdetermination problem D2 was designed to kill**: which participant becomes the canonical `source`? Even a deterministic rule (e.g. AGENT_IN → VICTIM_IN) picks ONE projection of an event that has many — and once you have a binary on the books, downstream consumers can't tell whether `walder-frey BETRAYS robb-stark` came from the hub projection or from the legacy edges. Option (a) keeps the data model honest: events live as nodes, full stop.
- Full evidence: `working/edge-modeling/plate2-graphquery-traversal.md`.

**Consequence for Plate 3:**
- Plate 3 emits role edges (`AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, `WIELDED_IN`, `LOCATED_AT`) onto event-node hubs and STOPS THERE — no canonical dyad generation step.
- Plate 3 (or a sibling sub-step) marks superseded person→person binaries with `superseded_by: <hub_slug>` so the legacy edges remain (per CLAUDE.md) but no longer participate in primary traversal. The exact deprecation-marking mechanism is a Plate 3 / Plate 5 detail.
- Result for queries: "who killed X" returns 2-hop walks through the event hub (rich, multi-role); 1-hop walks return either nothing or the legacy edge marked superseded.

**Open follow-up (out of scope for Plate 2):**
- Whether `--path` should expose a `--prefer-event-bridges` flag to rank event-mediated bridges higher than incidental character bridges. Presentation polish; not a blocker.
- Whether per-node `## Edges` display bullets (the unsynced markdown layer) should be regenerated to show the hub-mediated 2-hop walks. Plate 5 line item.

---

## 4. Glossary

- **Reify / reification** — promote an event from an edge to a first-class **node**, and hang each participant off it as a labeled role-typed edge. The associative-entity / junction-table move ("a Prescription is a record, not a foreign key"). Lossless — every role survives.
- **Role edge** — an edge whose type names the participant's thematic role in an event: `AGENT_IN` (executor), `VICTIM_IN` (patient), `COMMANDS_IN` (instigator/orderer), `WIELDED_IN` (instrument), `LOCATED_AT` (place). Source = participant, target = `event.*` node.
- **Head / head-selection** — when forced to flatten an n-ary event onto one edge, the "head" is the participant nominated as `source`. An event has no natural head; a binary relation does (`PARENT_OF` head is always the parent).
- **Head-direction normalization (the "normalizer")** — a deterministic, no-LLM repair pass over the existing `edges.jsonl` that **flips inverted rows** so `source` always holds the semantic agent. It keys on the row's own `asserted_relation`/`hint_raw` field, which self-witnesses the bug (`"Killed by"`, `"Betrayed by"`, `"Captor of"`, passive `"was …ed by"`). Where a row carries a reverse-signal, swap `source_slug ↔ target_slug`; where direction is ambiguous and unsignaled, flag for review rather than guess. It is the retroactive twin of the Plate-1 Pass-1 head rule.
- **Materialized dyad** — option (c) in D2: a single canonical `agent → patient` binary edge **deterministically generated from a reified hub** (not guessed by an extractor), preserving 1-hop query ergonomics while killing underdetermination (one projection, reproducible).
- **Underdetermination** — the desired output (one deterministic edge) is not uniquely determined by the input (a head-less event). The root pathology behind the "hallucination-look".

---

## 5. Plate overview

| Plate | What | Cost | Reversibility | Depends on | Status |
|---|---|---|---|---|---|
| **0** | Deterministic existing-graph fixes: head-direction normalizer (0a) + Aerys slug merge (0b) | $0 (no LLM) | Backup-gated; full revert via `_regrounding` backup | — | **Recommended, run first** |
| **1** | Doc foundation: Pass-1 head rule (1a) + Events role sub-bullets (1b) + schema `AGENT_IN`/`VICTIM_IN` + widen `COMMANDS_IN` + validator contract (1c) | $0 (doc-only) | Full (git revert) | — | **Recommended apply** |
| **2** | Verify the two gating unknowns + resolve D2: node-existence count (2a) + `graph-query.py` traversal check (2b) → decide replace-vs-project + size node-minting | $0 (repo-local) | N/A (analysis) | — (reads current graph) | **Gate for Plate 3** |
| **3** | Backfill pipeline: mine Pass-1 `## Events & Actions` → role edges on event nodes, **incl. node-minting**; staging-only output | $2–10 (legacy Sonnet path) | Staging throwaway; merge separate | 1c, 2 | **Held** |
| **4** | Disposition of the 1,617 Haiku bulk emits: fresh bucketing review → normalize → promote/hold/drop | $5–15 (Sonnet filter) | Staging-only until merge | 0a | **Held — needs review** |
| **5** | Gated merge of staging → `edges.jsonl` (before/after sign-off) + carried-forward S77 cleanups | $0 | The merge is the irreversible step; backups retained | 3, 4 | **Held — Matt sign-off** |

**Carried-forward S77 cleanups** (folded into Plate 5, not in scope unless Matt raises): drop 2 `cersei↔tyrion` `LOVES` edges; retype ~22 `ASSAULTS → ATTACKS` (ASSAULTS is sexual-only); merge-time `OWNS → BONDED_TO` for direwolf/dragon targets.

---

## 6. Sequencing

```
Plate 0  (deterministic fixes on existing graph)  ─┐
  0a normalizer        0b Aerys merge               │  run first; independent of architecture
                                                    │
Plate 1  (doc foundation, $0)  ────────────────────┤  can run in parallel with Plate 0
  1a head rule  1b sub-bullets  1c schema+validator │
                                                    ▼
Plate 2  (verify gating unknowns; resolve D2)  ─────  reads current graph; blocks Plate 3
  2a node-existence count   2b graph-query traversal
                                                    ▼
Plate 3  (backfill pipeline + node-minting)  ──────  needs 1c (valid vocab) + 2 (decisions)
  → working/edge-modeling/role-edges-staging.jsonl
                                                    ▼
Plate 4  (Haiku-bulk disposition)  ────────────────  needs 0a (normalizer) for promote-as-is rows
  → working/edge-modeling/haiku-bulk-disposition.jsonl
                                                    ▼
Plate 5  (gated merge to edges.jsonl + S77 cleanups)  ── Matt before/after sign-off
```

**Minimum first move:** Plate 1 (doc-only, $0, fully reversible) + Plate 0 (deterministic, backup-gated). Everything downstream is held until Plate 2's decisions land.

---

## 7. Session prompts

Each subsection below is a **complete, self-contained session prompt**. Open a fresh Claude Code session and paste the block. They follow the house continue-prompt style: Recommended-model line, prerequisites, numbered steps with done-criteria, out-of-scope, files-touched. (To wire any of these into `/continue`, save the block as its own file under `progress/continue-prompts/` — see §8.)

---

### 7.0 — Plate 0: Deterministic existing-graph fixes

```markdown
# Plate 0 — Head-Direction Normalizer + Aerys Slug Merge

> **Recommended model:** Sonnet (delegate the script to `script-builder`; the logic is
>   deterministic — no reasoning-heavy work). Opus not needed.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D4), §4 (glossary).

## Why
Two deterministic, ~$0 fixes on the LIVE graph (`graph/edges/edges.jsonl`, 3,811 rows),
independent of the reification architecture, that must land before any reification:
- The python-map anchored `source` on the grammatical subject, producing inverted edges
  (`cressen KILLS melisandre`, `arya CAPTURES sandor`, `tyrion BETRAYS shae`; 232 same-type
  bidirectional pairs). The rows self-witness the bug via `asserted_relation`/`hint_raw`.
- The Aerys regicide lands on a phantom slug: `KILLS jaime-lannister → aerys-targaryen`,
  while the canonical Mad King node is `aerys-ii-targaryen` (both node files exist; ~8 other
  Jaime↔Aerys edges resolve to the canonical slug). Reifying onto the phantom relocates the bug.

## Prerequisites
1. Read the design doc §3 (D4) and §4 (head-direction normalization definition).
2. Confirm `graph/edges/_regrounding/` backup mechanism exists (it does — reuse it).
3. NOTE: this touches `edges.jsonl`. Back up first; produce a before/after diff for Matt.

## Steps
1. **Build the normalizer** (`script-builder`, new `scripts/edge-direction-normalizer.py`):
   - Read `edges.jsonl`. For each row, scan `asserted_relation` + `hint_raw` against a
     reverse-signal lexicon: "killed by", "betrayed by", "captured by", "captor of",
     "<role> of <subject>" possessive-patient forms, passive "was <verb>ed by", etc.
   - On match: swap `source_slug ↔ target_slug` (and any direction-bearing resolution-status
     fields). On no-signal-but-known-symmetric type: leave. On ambiguous: write to a
     `flagged-for-review.jsonl`, do NOT guess.
   - Output a candidate file + a human-readable diff (old → new) for every flip.
   - Done-criterion: every confirmed inversion in the design doc §1 is flipped; counts of
     {flipped, left, flagged} reported.
2. **Aerys slug merge** (deterministic): repoint the 2 `aerys-targaryen` edges to
   `aerys-ii-targaryen`. Verify no legitimate distinct entity (`aerys-i-targaryen` is a
   DIFFERENT king — do not touch). Confirm against the gated Haiku bulk, which already has the
   corrected slug. Quarantine/redirect the now-empty `aerys-targaryen` node per the project's
   `_conflicts/` convention; do NOT delete source data.
3. **Do NOT merge into `edges.jsonl`.** Write candidates + diff to `working/edge-modeling/`.
   The merge is Plate 5 (gated). Surface the before/after counts to Matt for sign-off.

## Out of scope
- Reification, role edges, schema changes (Plates 1, 3).
- Any LLM pass — this is purely deterministic.
- Merging to the canonical edge file.

## Files this session may create/modify
- CREATE `scripts/edge-direction-normalizer.py`
- CREATE `working/edge-modeling/normalizer-candidates.jsonl`,
  `working/edge-modeling/normalizer-diff.md`, `working/edge-modeling/flagged-for-review.jsonl`
- CREATE `working/edge-modeling/aerys-merge-candidates.jsonl`
- Do NOT modify `graph/edges/edges.jsonl`.
```

---

### 7.1 — Plate 1: Doc foundation

```markdown
# Plate 1 — Pass-1 Head Rule + Events Sub-bullets + Schema Additions

> **Recommended model:** Sonnet. These are careful prose edits to an agent prompt and the
>   schema reference; no heavy reasoning. Opus not needed.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D1, D5), §2 (#6).
> **CLAUDE.md rule #6:** when you change the schema, `architecture.md` and the agent prompt must
>   stay in sync — this plate does both in one commit.

## Why
Stop grammatical-subject leakage in FUTURE Pass-1 extractions, capture event role structure
inline, and add the minimal reification vocabulary. All doc-only, $0, fully reversible.

## Steps
1. **1a — Pass-1 head rule.** In `.claude/agents/mechanical-extractor.md`, after the
   `## Relationships Observed` table description (~line 178), insert:
   > **Head rule:** Column A is always the SEMANTIC AGENT of the relationship, never the
   > grammatical subject of the source sentence and never the POV character. For passive
   > sentences ("X was killed by Y"), put the by-phrase agent (Y) in Column A. For ordered
   > acts ("Tywin had the Mountain attack the Riverlands"), the EXECUTOR (Mountain) goes in
   > Column A; record the orderer (Tywin) in the Events & Actions Instigator slot, not in
   > Column A. Never anchor on the grammatical subject — the same event is phrased many ways,
   > and surface syntax must not leak into the data model.
2. **1b — Events & Actions role sub-bullets.** In the same file's `## Events & Actions`
   section (~line 134), extend the format to allow OPTIONAL indented role sub-bullets
   (Agent / Patient / Instrument / Location / Instigator / Outcome). Backwards-compatible:
   entries without sub-bullets stay valid. VERIFY the parser at
   `scripts/stage4-pass1-extra-tables.py:522` reads only the first line of each numbered item,
   so sub-bullets don't break ingestion (state the verification result in your summary).
3. **1c — Schema additions.** In `reference/architecture.md`:
   - In the Military & Conflict table (after `TORTURES`, ~line 236) add:
     `| AGENT_IN | Acts as the agent/executor of an event | Person/House → Event |`
     `| VICTIM_IN | Receives the action of an event as victim/patient | Person/House → Event |`
   - Widen the existing `COMMANDS_IN` row (~line 214) to cover the orderer/instigator role for
     events where the commander did not personally execute.
   - Note in the doc that `WIELDED_IN` (already artifact→event) serves the instrument role.
   - Vocab count goes 163 → 165. Update any vocab-count references.
4. **1c validator contract (SAME commit):** add a target-type contract to the Stage-4 type
   validator (`scripts/stage4-type-contract-validator.py`): `AGENT_IN` and `VICTIM_IN` targets
   MUST be `event.*`; sources may be `character.*` or `house.*`. This prevents the new vocab
   from being emitted unguarded.

## Done-criteria
- mechanical-extractor.md has the head rule + optional role sub-bullets.
- architecture.md has AGENT_IN + VICTIM_IN, widened COMMANDS_IN, vocab=165.
- Validator rejects AGENT_IN/VICTIM_IN with non-event targets.
- No Pass-1 rerun is triggered (existing 344 extractions stay as-is; prompt change benefits
  only future runs).

## Out of scope
- Backfilling any edges (Plate 3). Touching `edges.jsonl`. Rerunning Pass-1.

## Files this session may modify
- `.claude/agents/mechanical-extractor.md`
- `reference/architecture.md`
- `scripts/stage4-type-contract-validator.py`
```

---

### 7.2 — Plate 2: Verify gating unknowns + resolve D2

```markdown
# Plate 2 — Node-Existence Count + graph-query Traversal Check → Resolve Replace-vs-Project

> **Recommended model:** Opus for the D2 decision (it sets the whole backfill shape and the
>   query contract); the two underlying counts/inspections are mechanical and can be done
>   inline or delegated to Sonnet/`Explore`.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D2, D3).

## Why
Two cheap, repo-local, deterministic checks that convert the project's two biggest open
questions into decisions. Backfill (Plate 3) is BLOCKED until these resolve.

## Steps
1. **2a — Node-existence count (sizes node-minting + backfill cost).** Across the 344
   `extractions/mechanical/{book}/*.extraction.md` files, enumerate the `## Events & Actions`
   entries. For each, determine whether an `event.*` node already exists that includes that
   chapter as evidence (join against `graph/index/events/`). Report: how many Pass-1 events
   ALREADY have a node vs. how many would need MINTING. Spot-check the motivating cases —
   confirm that Bran's defenestration, Tywin's privy death, and the Purple Wedding poisoning
   have NO node today (expected, per §3 D3). This count is the gating number for Plate 3 scope
   and cost.
2. **2b — graph-query traversal check (decides D2).** Inspect `scripts/graph-query.py`
   (modes incl. `--path`, `--neighbors`). Determine: can it transparently traverse
   `person → event → person` (so "who killed X" works via the hub at 2 hops), or does it
   assume person→person edges for relationship queries? Run a concrete probe if possible
   (e.g. a `--path` between two Red Wedding participants through the event node after a
   hypothetical role edge — or read the traversal code and state definitively).
3. **Resolve D2** (Opus): given 2b, choose:
   - **(a) Replace** (pure 2-hop hub) — if graph-query traverses person→event→person cleanly.
   - **(c) Project** (keep a materialized agent→patient dyad generated from the hub) — if it
     cannot, so 1-hop headline queries survive.
   Record the decision + rationale in the design doc (append a "D2 RESOLVED" note) and in
   `worklog.md`. This decision is an input to Plate 3.

## Done-criteria
- A number: Pass-1 events with-node vs. needs-minting.
- A definitive answer on graph-query.py person→event→person traversal.
- D2 resolved to (a) or (c), written into the design doc + worklog.

## Out of scope
- Building anything. Modifying the graph. This is analysis + one decision.

## Files this session may create/modify
- CREATE `working/edge-modeling/plate2-findings.md`
- APPEND a "D2 RESOLVED" note to `working/edge-modeling/edge-modeling-reification-design.md`
- Update `worklog.md` with the decision.
```

---

### 7.3 — Plate 3: Backfill pipeline (+ node-minting)

```markdown
# Plate 3 — Reify: Mine Pass-1 Source → Role Edges on Event Nodes (HELD until Plate 1c + Plate 2)

> **Recommended model:** Sonnet — pipeline construction via `script-builder` (deterministic
>   join + lift), plus a Sonnet `claude -p` pass for legacy rows lacking role sub-bullets.
>   Opus only if Plate 2 surfaced ambiguity in event identity.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D2,D3,D5,D7).
> **PRECONDITION:** Plate 1c (AGENT_IN/VICTIM_IN in schema + validator) landed AND Plate 2's
>   D2 decision + node-existence count are recorded. If not, STOP and run those first.

## Why
Populate role edges (`AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, `WIELDED_IN`, `LOCATED_AT`) on
event-node hubs by mining Pass-1 source. NOTE (§2 #4): the Haiku `**title**` field is NOT a
usable grouping key (per-row micro-beats; only 5/1617 reference a slug) — this is a fresh
mining pass over Pass-1, not a filter over Haiku emits. NOTE (§3 D5): the sub-bullet path
covers ~0 existing rows (no Pass-1 rerun), so existing data goes through the legacy Sonnet
path — cost ~$2–10, not ~$0.

## Steps
1. **Node-minting sub-step (from Plate 2 count, §3 D3):** for Pass-1 events lacking a node,
   mint fine-grained `event.*` nodes (e.g. `event.death`/`event.wedding` or reuse existing
   leaves per architecture). Deterministic slug from event title + occasion; DEDUP across
   chapters (the Red Wedding spans 3 chapters → ONE node, or the fragmentation returns).
2. **Deterministic join:** for each chapter, match `## Events & Actions` rows to event-node
   slugs (existing or newly minted) that include that chapter as evidence.
3. **Lift roles:** if role sub-bullets present (future Pass-1 output), lift directly. If absent
   (all current legacy entries), run a Sonnet `claude -p` pass (cwd=/tmp) per row to extract
   {agent, patient, instrument, location, instigator} from the narrative line, applying the
   §3 D7 causation rule (executor → AGENT_IN; orderer → COMMANDS_IN; never collapse
   instigator→victim — GATE 2).
4. **Apply D2:** if Plate 2 chose (c) Project, also emit the materialized canonical agent→patient
   dyad from each hub; if (a) Replace, mark the superseded scattered binaries for deprecation
   (do NOT delete — mark `superseded_by`, keep backups).
5. **Output staging only:** `working/edge-modeling/role-edges-staging.jsonl` +
   `working/edge-modeling/minted-event-nodes/`. Do NOT write `graph/edges/edges.jsonl` or
   `graph/nodes/` canonically. Produce a summary + sample for Matt.

## Done-criteria
- Every reifiable Pass-1 event has a hub (existing or minted) and ≥1 role edge.
- Red Wedding hub populated (the §1 worked example) as a smoke test.
- Validator passes on all staged role edges (AGENT_IN/VICTIM_IN → event.*).
- D2 decision applied consistently across all rows.

## Out of scope
- Merging to canonical files (Plate 5). The Haiku bulk (Plate 4).

## Files this session may create/modify
- CREATE `scripts/edge-reify-backfill.py`
- CREATE `working/edge-modeling/role-edges-staging.jsonl`,
  `working/edge-modeling/minted-event-nodes/`, summary md.
- Do NOT modify canonical `graph/` files.
```

---

### 7.4 — Plate 4: Haiku-bulk disposition

```markdown
# Plate 4 — Disposition of the 1,617 Haiku Bulk Emits (HELD — needs fresh review)

> **Recommended model:** Opus for the bucketing-review decision (the source FAILED its drift
>   gate; this is a judgment call); Sonnet for any filter `claude -p` pass.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §3 (D6).
> **PRECONDITION:** Plate 0a (head-direction normalizer) exists — promote-as-is rows must pass
>   through it first.

## Why
The gated 1,617-row Events Haiku bulk (`working/wiki/pass2-buckets/pass1-derived/
_events-haiku-bulk/`) FAILED the S74 drift gate (48% triple agreement vs 70%; 56% pair vs 85%)
— a subject-selection drift failure that corrupts binary edges too. The prior bucketing was
sample-derived. Decide disposition rigorously before any promotion.

## Steps
1. **Fresh bucketing review:** re-classify the 1,617 rows under the reify/canonicalize/keep
   lens. State whether the classification is per-row or sample-extrapolated; if extrapolated,
   do a real per-row pass. Expected buckets (validate, don't trust the prior counts):
   canon-structural, keep-binary, canon-dyadic-act, reify@occasion, reify-hard,
   keep-role-edge, unbucketed-drift.
2. **Normalize before promote:** run EVERY promote-candidate through the Plate 0a normalizer.
   Any row whose direction flips is NOT "promote as-is" — it was carrying the inversion bug.
3. **Compose the action** and write it to staging (NOT canonical):
   - PROMOTE: keep-binary + canon-structural + keep-role-edge survivors (post-normalize).
   - SONNET-FILTER: canon-dyadic-act (and ambiguous structural) → promote survivors.
   - HOLD: reify candidates → feed Plate 3's hub backfill.
   - DROP: unbucketed drift.
4. Output `working/edge-modeling/haiku-bulk-disposition.jsonl` + a per-bucket summary for Matt.

## Done-criteria
- Per-row disposition for all 1,617 rows.
- Promote-set has passed the normalizer (zero inverted rows promoted as-is).
- Reify candidates routed to Plate 3.

## Out of scope
- Merging to `edges.jsonl` (Plate 5).

## Files this session may create/modify
- CREATE `working/edge-modeling/haiku-bulk-disposition.jsonl` + summary md.
- Do NOT modify canonical `graph/` files.
```

---

### 7.5 — Plate 5: Gated merge + S77 cleanups

```markdown
# Plate 5 — Gated Merge to edges.jsonl + Carried-Forward Cleanups (HELD — Matt sign-off)

> **Recommended model:** Sonnet for the deterministic merge + validation; Matt provides
>   before/after sign-off (this is the one irreversible step).
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9).
> **Context doc:** `working/edge-modeling/edge-modeling-reification-design.md` §5 (carried-forward).
> **PRECONDITION:** Plates 0, 3, 4 staged outputs exist and Matt approved them.

## Why
Single gated step that writes all staged work into the canonical graph, with full backup and a
before/after diff. This is the only irreversible plate — treat with care.

## Steps
1. Back up `graph/edges/edges.jsonl` to `graph/edges/_regrounding/` (project convention).
2. Merge, in order, with a validation pass after each: (a) Plate 0 normalizer flips + Aerys
   merge; (b) Plate 3 role edges + minted event nodes; (c) Plate 4 promote/drop set.
3. **Carried-forward S77 cleanups** (only if Matt confirms): drop 2 `cersei↔tyrion` LOVES;
   retype ~22 `ASSAULTS → ATTACKS` (ASSAULTS = sexual-only); merge-time `OWNS → BONDED_TO` for
   direwolf/dragon targets.
4. Run the full schema-drift + orphan-edge + type-contract validators. Regenerate the per-node
   `## Edges` display bullets (they are NOT auto-synced to the JSONL).
5. Produce a before/after diff + final counts. Update `worklog.md`.

## Done-criteria
- All staged work merged; all validators green; no new orphan edges.
- Per-node display lists regenerated.
- Backup retained; before/after diff archived.

## Out of scope
- Any new analysis or extraction. This plate only commits prior staged work.

## Files this session may modify
- `graph/edges/edges.jsonl` (the gated write), `graph/nodes/events/` (minted nodes),
  per-node display bullets, `worklog.md`.
```

---

## 8. Reversibility & safety

- **Plates 0 & 3 & 4 write to `working/edge-modeling/` only.** Throwaway staging. `graph/edges/edges.jsonl` is untouched until Plate 5.
- **Plate 1 is doc-only** — revert = `git revert` of `mechanical-extractor.md` + `architecture.md` + the validator.
- **No plate triggers a Pass-1 rerun.** The 344 existing extractions stay as-is; the Plate-1 prompt change benefits only future runs.
- **Plate 5 is the single irreversible step**, and it backs up to `_regrounding/` first and produces a before/after diff for sign-off.
- **Source data is never deleted** (CLAUDE.md hard rule): superseded edges get `superseded_by`, collided nodes go to `_conflicts/`.
- **To wire prompts into `/continue`:** copy any §7 block into its own file at
  `progress/continue-prompts/2026-06-05-edge-modeling-plate-N-<slug>.md`. Each already carries the
  required Recommended-model line and is self-contained.

---

## 9. Open decisions owned by Matt

1. **Apply Plate 0 + Plate 1 now?** (Deterministic + doc-only; the safe first move.)
2. **D2 — replace vs. project** is *delegated to Plate 2's repo check*, but Matt may pre-state a
   preference (keep 1-hop "who killed X" via a materialized dyad, or accept pure 2-hop hub).
3. **Plate 4 — review the bucketing first, or accept a composed promote/hold/drop?** (Recommend
   review: the source failed its drift gate and the prior counts were sample-derived.)
4. **Plate 3 legacy backfill cost** — approve the ~$2–10 Sonnet legacy path (the only path that
   touches existing data; bullets-only would backfill nothing today)?
5. **Causation (D7)** — confirm one-node-with-`COMMANDS_IN`-orderer (both independent runs agreed).
6. **S77 carried-forward cleanups** — fold into Plate 5, or handle separately?
```
