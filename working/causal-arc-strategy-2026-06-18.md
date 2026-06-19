# Causal / Narrative-Arc Edges — Scaling Strategy (pure-analysis)

**Date:** 2026-06-18 (S105) · **Model:** Opus 4.8 orchestrator · **Status:** plan for Matt review — **NO graph writes were made this session.**
**Question (from `progress/continue-prompts/2026-06-17-causal-edges-and-spark-nodes.md`):** how far, and in what order, should causal/narrative-arc structure be built across the whole graph?
**Predecessor:** Robert's Rebellion shipped as the exemplar (S104). Technique settled; only the *scaling policy* is open. Generalizes [[project_narrative_arc_reification]].

---

## 1. Inventory — where the causal layer stands today

Measured 2026-06-18 against `graph/nodes/events/` (593 nodes) and `graph/edges/edges.jsonl` (22,157 edges).

### Event-node connectivity

| Bucket | Count | Reading |
|---|---|---|
| Total `event.*` nodes | 593 | the universe of reifiable beats/hubs |
| Fully isolated (degree 0) | **132** | mostly deep-lore wiki-only wars/battles — the dark zone |
| Barely connected (degree 1–2) | 145 | usually just a PART_OF or a lone dyad |
| In the `PRECEDES` chronology chain | **117** | the deterministic timeline backbone (S104) |
| Touched by a causal edge (CAUSES/TRIGGERS/ENABLES/MOTIVATES/PREVENTS) | **12** | the entire causal layer reaches 12 of 593 events |
| Neither causal **nor** chronology | **466** | 79% of event nodes carry no temporal/causal structure at all |

### The causal layer in full (8 edges, 3 micro-arcs + 1 pilot)

```
CAUSES   tourney-at-harrenhal → abduction-of-lyanna           (RR spark chain, S104)
CAUSES   abduction-of-lyanna → execution-of-brandon-and-rickard-stark
TRIGGERS execution-of-brandon-and-rickard-stark → aerys-demands-ned-and-robert
TRIGGERS aerys-demands-ned-and-robert → roberts-rebellion
CAUSES   battle-of-the-trident → sack-of-kings-landing        (Trident→Sack pilot, S104)
CAUSES   sack-of-kings-landing → coronation-of-robert-i-baratheon
TRIGGERS cersei-maneuvers-for-lady-s-death → death-of-mycah   (Trident incident arc, S95)
TRIGGERS attack-on-ned...streets → cersei-claims-ned-s-men-attacked-first (street-brawl, S91)
```

All causal edges are concentrated in **one historical arc (Robert's Rebellion)** plus **two small AGOT incidents**. Everything else is structurally causal-dark.

### Containment / chronology layers (these DO have reach)

- `PART_OF` 168 · `SUB_BEAT_OF` 66 · `PRECEDES` 174 (117 events) · `PARALLELS` 14.
- **War of the Five Kings** is the one densely-modelled conflict: **69 PART_OF battle-children + 40 internal PRECEDES** orderings — but **zero internal CAUSES/TRIGGERS**. The reader's "Robb wins every battle but loses the war" causal logic is absent; only sequence and containment exist.
- **Greyjoy Rebellion**: degree 26 (participants attached in historical-anchor wave 1) but **0 PART_OF, 0 causal** — partial scaffolding, no chain.
- The remaining 29 `event.war` nodes (Targaryen Conquest, Blackfyre Rebellion, Dance of the Dragons*, Century of Blood, the Ghiscari/Rhoynish/turtle wars…) are **degree 0–4, effectively isolated**.

\* Data-quality note (not for this analysis to fix, → todos § Small Fixes): `roberts-rebellion` and `dance-of-the-dragons` are mistyped `event.battle`, not `event.war`.

### What the inventory says
The graph has **three of four layers** of temporal/causal structure: dyads (dense), containment (PART_OF, partial), chronology (PRECEDES, 117 events). The **causal consequence layer is a 12-node proof-of-concept**. The backbone to hang causal edges on (dated events + PRECEDES ordering) already exists — so the marginal cost of a causal edge is low where the beat-nodes are present.

---

## 2. Criteria for "worth reifying" — a rubric

Score each candidate arc 0–2 on six signals; treat **Grounding** and **Beat-readiness** as the cost axes and the rest as value axes.

| Signal | 0 | 1 | 2 |
|---|---|---|---|
| **Query-value** — would a grounded-agent dip fumble an arc-shaped question here? | never asked | plausible | dip already failed it (Q5/Q10-class) |
| **Reader-salience** — is the chain load-bearing in canon? | trivia | minor thread | a chain readers narrate ("X led to Y") |
| **Cross-POV reach** — how many POVs converge on it? | 1 | 2 | 3+ (high traversal payoff) |
| **Causal load** — does the chain carry *consequence*, not just sequence? | pure sequence (PRECEDES already covers it) | mixed | each step *causes* the next |
| **Beat-readiness (cost)** — do the sub-event nodes already exist? | none exist | some exist | all/most exist → wiring only |
| **Grounding (cost + Tier ceiling)** — in-saga POV text vs wiki-only deep-lore? | wiki-only (Tier-2 cap, expensive) | mixed | in-saga POV (Tier-1 quotes available) |

**Decision rule (proposed):** reify when **value ≥ 7/12 AND not (Grounding = 0 with Query-value < 2)**. In plain terms: build arcs that are reader-load-bearing and either already have their beat-nodes or are grounded in book text — and *don't* spend effort lighting up wiki-only deep-lore that nobody is querying yet (that work belongs to the TWOIAF/F&B ingestion track, not here).

Two anti-signals that should *block* an edge regardless of score:
- **Sequence masquerading as cause.** If `PRECEDES` already captures the relationship and there's no consequence, don't add CAUSES/TRIGGERS. Causal edges are for consequence the reader feels, not for ordering (which is deterministic and already shipped).
- **Granularity overclaim.** S104's finding: at coarse hub granularity (a whole battle node) use **CAUSES**, not TRIGGERS — TRIGGERS asserts a specific spark that a coarse node doesn't name. Codify (open question Q3).

---

## 3. Prioritized list — the next arcs to treat

Sequenced by value-per-cost, leaning on the rubric. **In-saga + beats-mostly-exist rises to the top; wiki-only deep-lore sinks.**

### Tier A — cheap, high-value (wire existing beats; little/no minting)

1. **Sack of King's Landing chain** — Jaime-kills-Aerys → Mountain-kills-Elia/Rhaenys/Aegon → Tywin's sack → Robert overlooks it. *Why first:* directly extends the already-shipped RR/Trident work (the `Trident → Sack → Coronation` pilot is already in); answers dip **Q10** ("consequences of the Battle of the Trident"); in-saga POV recall (ASOS Jaime) gives Tier-1/2 quotes. Some beat-nodes exist (sack hub, Trident); 1–2 mints likely (kingslaying, Elia's murder).
2. **Bran's fall → Catelyn hunts the catspaw → Tyrion accused → trial at the Eyrie** — *Why:* rich existing dyad coverage, fully in-saga (AGOT Bran/Catelyn/Tyrion), reader-central first-act engine, beats largely exist → mostly wiring. High cross-POV reach (Bran, Catelyn, Tyrion).
3. **Purple Wedding** (Sansa's hairnet → Joffrey poisoned → Tyrion accused/tried) — *Why:* FIX-22 already minted `death-of-joffrey-baratheon` + ceremony beats; in-saga (ASOS Sansa, AFFC Cersei); the canonical whodunnit, a top agent-question shape. Mostly wiring + the Olenna/Littlefinger causal attribution.

### Tier B — medium (a few new beats; ~half-session each)

4. **Catelyn frees Jaime → Robb's host turns on her → Jeyne Westerling marriage → (feeds) Red Wedding** — *Why:* in-saga ASOS; connects *upstream* into the already-reified Red Wedding hub (S87), closing one of GRRM's tightest cause-chains. Beats partially exist.
5. **Greyjoy Rebellion → Theon-as-hostage → ironborn invasion of the North** — *Why:* participants already attached (historical-anchor wave 1, degree 26) so half the scaffolding is up; needs PART_OF battles + the Theon-ward causal link. Spans AGOT/ACOK.

### Tier C — defer

- **War of the Five Kings full causal mesh** — epic (69 battles already PART_OF + PRECEDES-ordered). Causal-link only the *load-bearing* junctures later (e.g. Blackwater → Tyrell defection → siege lifted), never the full mesh.
- **Deep-lore wiki-only wars** (Targaryen Conquest, Dance of the Dragons, Blackfyre Rebellions, Century of Blood, Long Night) — isolated, Tier-2 ceiling, near-zero current query demand. **Route these to the TWOIAF / Fire & Blood ingestion track** (worklog Ideas&Backlog), not to in-graph curator minting. Lighting them up before there's book-grounded text would mint a Tier-2 lattice nobody queries.

---

## 4. Approach + cost per arc (reuse the RR template)

The Robert's-Rebellion exemplar (S104) is the reusable recipe:

1. **Identify beats** from local sources (chapters + wiki cache) — the reader-named load-bearing moments.
2. **Mint missing beat-nodes** only where a load-bearing beat lacks a node (RR minted 3: abduction / executions / demand). In-saga beats carry a `## Quotes` block with verbatim Tier-1 chapter quotes.
3. **Rebuild** the targeted index + alias-resolver (node ADD → required per [[project_rebuild_derived_artifacts_after_node_mutation]]).
4. **Wire** `CAUSES` / `TRIGGERS` between beats (CAUSES at coarse granularity; TRIGGERS only for a named spark).
5. **Verify** with a **fresh subagent against the LOCAL cache** — all CONFIRM before commit ([[feedback_subagent_verify_not_matt]]). Matt gates at policy level, not per-edge.

**Cost estimate (subagent-driven, local cache only):**

| Arc class | New beat-nodes | Subagent passes | Rough effort |
|---|---|---|---|
| Tier A (wiring-heavy) | 0–2 | 1 research + 1 verify | ~1 hour, < $5 |
| Tier B | 3–6 | 1–2 research + 1 verify | ~half session |
| Tier C epic | 20+ | many | defer / own track |

**Cadence recommendation: dip-driven, small batches of 3–5 — NOT mass-mint.** This is the standing lean (memo Q1, [[project_narrative_arc_reification]]) and the Mode 3 dip confirms it: only 2/10 dip questions were arc-shaped, and the dominant failure was slug-discoverability (Track 7), not missing arcs. So: ship Tier A (1–3) as one validating batch, then **re-run a Mode 3 dip weighted toward arc/consequence questions** and let *its* failures re-rank Tier B. Don't pre-commit beyond the first batch.

**Sequencing against the live queue:** Track 7 (alias-resolver) is the higher-leverage fix and is reportedly done (S96/S101) — confirm it before arc work, because an un-discoverable arc hub is invisible regardless of how well it's wired. Arc-minting should sit *after* resolver confidence, *parallel-or-after* historical-anchor structural attachment (which feeds the same hubs).

---

## 5. Open design questions for Matt (policy calls before execution)

1. **Tier policy for causal edges — the big one.** Causation is an *inference* even when both endpoints are on-page. Options: (a) causal edges grounded in a direct book quote may be **Tier-1**; (b) **cap all causal/interpretive edges at Tier-2** regardless of grounding, because the *link* is interpretive even if the *events* are canon. The RR chain used Tier-2 (`wiki-historical-anchor`) because it was pre-narrative; in-saga arcs (Bran's fall) could justify Tier-1 on quote strength. **Recommend (b) Tier-2 cap** for consistency and to keep Tier-1 meaning "verified canon fact," not "curator's causal reading." Needs your call.
2. **Causal-edge density** (memo Q3): TRIGGERS/CAUSES between *every* adjacent beat, or only *load-bearing* junctures? **Recommend load-bearing only** — PRECEDES already carries adjacency/sequence; reserve causal edges for consequence, to avoid causal-sprawl polluting traversals.
3. **CAUSES vs TRIGGERS rule** (S104 finding): codify "coarse hub → CAUSES; named specific spark → TRIGGERS" as a written gate in the verify step. Confirm wording.
4. **Beat-node minting aggressiveness:** how freely to mint new spark-beat nodes? **Recommend: mint only when the beat is (i) reader-named, (ii) load-bearing in a causal chain, and (iii) lacks an existing node** — the RR bar. Otherwise lean on existing hubs + dyads.
5. **Overlap with the parked `arc-wave1` mint prompt** (`progress/continue-prompts/archive/2026-06-15-arc-wave1-mint.md`, gated on your 3 decisions: RW-4 role edges / arc boundaries / RECIPIENT_IN). Does this strategy **supersede and fold in** that prompt, or do they run as two tracks? They target the same layer; recommend merging into one arc track governed by this plan.
6. **`event.arc` type?** (memo Q2): we now have 3 arc instances (RR, Trident, + the street-brawl micro-arc). The memo said defer an `event.arc` parent-type until 5+ arcs. After Tier A we'll have ~5 — **revisit then**, not now.
7. **Deep-lore routing:** confirm that wiki-only historical wars (Conquest/Dance/Blackfyre/Long Night) are **out of scope for curator causal-minting** and belong to the TWOIAF/F&B ingestion track. This keeps the causal track in-saga and Tier-disciplined.

---

## Bottom line

The causal layer is a **12-of-593 proof of concept** sitting on top of an already-built chronology backbone (117 events in `PRECEDES`) — so causal edges are *cheap to add where beat-nodes exist* and the technique is proven (RR). The right policy is **dip-driven, in-saga-first, small batches, Tier-2-capped, load-bearing-junctures-only**, reusing the RR template with fresh-subagent verification. Ship Tier A (Sack of KL → Bran's fall → Purple Wedding) as one validating batch, re-dip with arc-weighted questions, then let those failures re-rank Tier B. Defer the WO5K causal mesh and route deep-lore wiki-only wars to the TWOIAF/F&B ingestion track. Seven policy calls above gate execution — Tier policy (#1) is the load-bearing one.

---

## 6. Smoke test #2 — the "Bran's fall" arc (executed S105, analyzed against the plan)

After writing §1–5, Matt authorized building **one** arc as a second smoke test against the Robert's-Rebellion exemplar. Built the **Bran's-fall causal chain** (a genuine A→B→C consequence chain, deliberately chosen as the *most contrasting* profile to RR's historical/wiki grounding):

```
bran-witnesses-jaime-and-cersei  --TRIGGERS-->  jaime-pushes-bran-from-the-tower
jaime-pushes-bran-from-the-tower  --CAUSES-->   bran-s-direwolf-kills-the-assassin
bran-s-direwolf-kills-the-assassin --CAUSES-->  catelyn-seizes-the-moment-and-arrests-tyrion
```

**Shipped:** 2 new beat-nodes minted + 1 pre-existing node enriched (the catspaw) + 1 pre-existing node reused (the capture). 3 causal edges, all **Tier-2**, `evidence_kind: book-pass1`, all with verbatim AGOT chapter quotes, all **subagent-verified CONFIRM** against the local cache. `edges.jsonl` 22,157 → 22,160; nodes 8,521 → 8,523; 62 orphans unchanged; pytest 1297 pass / 1 documented env-fail. Backup: `graph/edges/_regrounding/edges-pre-bran-arc-2026-06-18.jsonl`.

### What the plan got RIGHT (validated)
- **The RR template generalized cleanly** to an in-saga present-narrative arc — same 5 steps (identify → mint → index/alias rebuild → wire → verify) worked end-to-end.
- **Fresh-subagent verification is a real gate, and it scales.** The subagent confirmed all 3 edges, *independently validated the CAUSES-vs-TRIGGERS type calls*, and confirmed the two anti-overclaim moves (unasserted catspaw sender; the dagger framed as "what Catelyn *believed* Littlefinger's claim was," not factually Tyrion's). This is the concrete answer to "I can't review 100 of these" — the per-edge review happened, I never had to.
- **Tier-2 cap (policy-Q1) applied cleanly** even though every endpoint had a Tier-1 chapter quote — good live demonstration that "the events are canon, the *causal link* is interpretive → Tier-2" is workable.
- **CAUSES/TRIGGERS discipline held** (S104 rule): 1 TRIGGERS (immediate spark — "The things I do for love") + 2 CAUSES (mediated links).
- **Capture-quotes-during-research paid off** — enriched 2 bare Plate-3 stub nodes with verbatim quotes in passing.

### What the smoke test EXPOSED (plan corrections — the real value of running it)
1. **🔴 The minting step MUST have a pre-mint dedup gate — this is the biggest finding.** I minted a **duplicate**: `catelyn-seizes-the-moment-and-arrests-tyrion` already existed as a Plate-3 reified beat (verbose descriptive slug, same chapter, `inn-at-the-crossroads` location, 6 role edges). My hand-rolled existence check guessed slugs (`catelyn-captures-tyrion`, `capture-of-tyrion-lannister`…) and missed the Plate-3 phrasing. The alias resolver caught it only *after* the mint; I then deleted the dup, repointed the edge, and enriched the canonical node. **Plan fix: make "run every candidate beat-description through `event_alias_resolver.py --lookup` + the all-node fuzzy index, eyeball every match ≥0.6, before minting" a HARD step.** The ~200 Plate-3 verbose-slug beats are the primary collision surface and they're exactly the ones slug-guessing misses.
2. **🟠 The §4 cost model "Tier A = mostly wiring, low mint" is half-wrong.** Reality is a *patchwork*: the **dyads** exist densely, but the **beat-hubs** exist only where Plate 3 happened to mint them — and you can't tell which without the dedup lookup. Real per-arc cost ≈ "mint 2–3 + discover-and-reuse 1–2 pre-existing," same shape as RR. Re-label Tier A as "low-to-moderate mint," not "wiring-only."
3. **🟠 New arc nodes inherit the Track 7 discoverability gap.** "Bran's fall" → resolver returns `fall-of-dragonstone` (wrong). Natural-phrasing lookup of the new beats is weak. **Arc-minting value is gated on the Track 7 resolver fix** — an un-discoverable arc hub is invisible to a consumer agent no matter how well it's wired. Sequence accordingly.
4. **🟠 Tooling gap: no directed-chain traversal.** `graph-query.py --path` only finds direct + 2-hop bridges, so it cannot answer "what set Tyrion's capture in motion, 3 steps back" — the exact consumer query the arc track exists to serve. Need an ancestor/descendant directed-chain primitive (`--causal-chain <node>` walking CAUSES/TRIGGERS/PRECEDES). Add to Track 7 scope.

### Verdict
The **technique generalizes and the verification gate scales** — the two things the smoke test most needed to prove. But the plan needs three concrete amendments before batch execution: **(a) a mandatory pre-mint dedup lookup** (highest priority — it prevents duplicate-node pollution), **(b) a corrected "patchwork" cost model**, and **(c) explicit sequencing behind the Track 7 resolver fix + a new directed-chain query primitive.** With those folded in, the first real batch (Tier A: Sack of KL, Purple Wedding) is ready to run dip-gated.

---

## 7. Advisory-board outcome + parent-node decision (S105)

Matt fanned out a 4-lens advisory board (narrative-craft / graph-modeling / canon / skeptic) on the arc-shape question. Outcome:

**Consensus fixes applied this session (all subagent-verified vs local cache):**
- **Inserted the missing causal hinge** `littlefinger-names-the-dagger-as-tyrion-s` (`event.deception`): canon + craft advisors both flagged that `catspaw → capture` skipped Littlefinger's false attribution of the dagger — the *actual* cause of the capture. Old direct edge removed; chain now routes catspaw → CAUSES → littlefinger-lie → CAUSES → capture.
- **Extended one hop, hard-stop**: minted `gregor-raids-the-riverlands` (`event.incident`), wired `capture → CAUSES → gregor-raids`. Explicitly did NOT add `CAUSES → war-of-the-five-kings` (skeptic + canon: causation past this point is multi-attributed — "a thesis, not an edge").

**Parent-node recommendation (my rec, for Matt's policy call): causal-chain-as-arc, NO umbrella parent nodes.** Deliver the parent's only real value ("show me the whole arc") as a query-tool **directed-chain primitive** (`--causal-chain <any-beat>` walking CAUSES/TRIGGERS both directions), not as a graph node. This dissolves both objections at once: graph-modeler gets the whole-arc query from any beat; skeptic's multi-parent-ownership trap never arises (Bran's fall belongs to ≥5 overlapping arcs — no single parent can own a beat). No curator-invented names, no premature `event.arc` type. Revisit `event.arc` only if a concrete query emerges that a chain-walk genuinely can't serve. **Prerequisite to flag:** the directed-chain primitive must be built (Track 7 query-tooling) — without it the causal chain is latent/unwalkable.

**This supersedes** the "umbrella parent vs chain" fork in the parked arc-wave1 prompt: recommend the chain model + traversal primitive, not parent hubs.

### Generalizable lesson — the "agency-collapse" check (S105, Matt-surfaced twice)

The single most valuable finding from smoke-test #2: an event→event `CAUSES` edge frequently **hides a human decision** in the middle, and collapsing it overclaims. Both of Matt's catches were this same class:
- `catspaw-fails → Tyrion-captured` skipped **Littlefinger's lie** (a scene) → fix: insert the decision as a **beat node**.
- `capture → gregor-raids` skipped **Tywin deciding to retaliate** (a character choice) → fix: `capture MOTIVATES tywin` + the actor's existing `COMMANDS_IN` role on the effect event.

**Add to the wiring template as a hard check:** before emitting `A CAUSES B`, ask *whose decision sits between A and B*. If a person chooses to act, model the agency — insert the decision-event as a node (if it's a scene) OR use `MOTIVATES` (event→actor) + the actor's `COMMANDS_IN`/`AGENT_IN` on B (if it's a choice). This is the causal-layer analogue of the reification principle: don't let a person's pivotal choice vanish inside a blunt event→event arrow.
