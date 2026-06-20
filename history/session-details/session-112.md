# Session 112 — The causal-arc strategy pivot (2026-06-20)

**Model:** Opus 4.8 orchestrator + 6 Sonnet 4.6 subagents (4-lens plan review + WO5K decomposition dip; S111's dip/research/verify overlapped in the same conversation).
**Type:** Design / strategy. No graph writes.
**Predecessor:** S111 (Q12 Blackwater-downstream build, committed separately).

> Human-facing narrative. The terse agent-facing version is the worklog S112 entry. This file is the *why* and the *how we got there*.

## The trigger: a weak session exposed a methodology flaw

S111 shipped Q12 (Blackwater downstream) — 2 beats, 3 edges. Matt's reaction was the whole session: *"this seems like a very weak session compared to the last dip session… I thought we were doing major / overarching events first and I think we've only done a few. Are we going in chronological order or something?"*

He was right, and the diagnosis matters. Recent arc sessions: S106=41 edges, S107=26, S109=17, **S111=3**. The cause wasn't bad luck — it was structural. The **dip ranks fumbles by "cheapest real gap."** Once the big AGOT/ASOS arcs were built, the dip started returning ever-cheaper singletons (Q12 was literally selected *because* it was the cheapest). Meanwhile the genuinely large arcs sat deferred as "Tier C epic."

The deeper realization: **the dip is a precision instrument, not a coverage instrument.** It measures "can an agent answer this arc question," not "are the major events modeled." Verified live: the causal layer reaches only **49 of 619 event nodes (~8%)**, and every one of the 9 built arcs is pre-series/AGOT/ASOS — **zero AFFC/ADWD**. So the dip kept saying "we're basically done" (its continue prompt literally read *"what remains are dip-gated refinements — NOT critical gaps"*) while ~92% of the event layer had no causal structure and the entire back half of the series was untouched.

Chronology came up as an instinct — Matt traced it to the old `first_available` / time-axis idea. We set it aside: the time axis is already captured in the data (`occurred.ac_year` on every beat), so build *order* doesn't need to be chronological to preserve it. Magnitude-first won.

## The decisions (Matt's)

1. **Two tracks, not one.** PRIMARY = a planned, magnitude-ordered major-arc backlog. SECONDARY = the opportunistic cheap dips (kept, not lost — Jeyne Westerling especially, which is theory-loaded). The dip demotes from *prioritizer* to *post-build check*.
2. **Anchor the backlog on what was foreshadowed.** Matt's lens: *"major events that happened in-book that were foreshadowed."* `reference/foreshadowing-events.md` (30 events, written way back) is a pre-curated inventory of the load-bearing arcs — foreshadowed = GRRM-planted = major-by-construction. Building them also seeds the deferred Pass 4 FORESHADOWS layer.
3. **Big containers get decomposed.** A whole war is too big to be one arc — it's a *container* that earns its own decomposition research dip to find its load-bearing constituent arcs. Generalizes to Essos and the AFFC/ADWD layer later.

## The insight that made it click: cross-book chains join themselves

Matt's best observation: late-game arcs have triggers that, followed back, reach the early books — *"Brienne only searches for Sansa because of the Purple Wedding; Cersei spirals because Tywin died; the Faith Militant because Cersei armed them… idk how all of that would be joined."*

The answer is that **it's already designed to join itself.** This is exactly what the S105/S106 *chain-as-arc, no-umbrella-parent* decision was for. We never build one giant arc — we build local junctures, and they stitch into series-spanning chains wherever two arcs **share a node**, walked by `--causal-chain` transitively. No join step, no container node. Live proof shown in-session: `--causal-chain assassination-of-tywin-lannister` already walks 7 hops back to Sansa's poisoned hairnet, because the Tywin and Purple-Wedding arcs share `trial-of-tyrion-lannister`.

So the discipline is just: **root each new arc at its existing upstream node** (Cersei's downfall → `assassination-of-tywin-lannister`; Brienne→Stoneheart → purple-wedding + red-wedding). Then the web assembles itself. And a fun corollary: AFFC — the "boring" book — is the *best* territory for this, because it's nearly all consequence-and-aftermath, which is what a causal layer feeds on.

Westeros↔Essos bridges become first-class under this (Robert's assassination order → Drogo's westward vow; Illyrio↔Varys; Varys-kills-Kevan → clears Aegon). Jorah-spies got demoted from "arc" to an `INFORMS`/`SPIES_ON` dyad — it's an information channel with no specific event-consequence.

## The validation: a 4-lens adversarial review, before minting

Matt asked for a fan-out to pressure-test the plan before committing. Four independent critics (canon/coverage, graph-modeling, reader-salience, skeptic/cost). **Unanimous GO-WITH-CHANGES.** The headline catch, from three of four: **decompose the "WO5K spine."** It is a *container*, not a walkable chain — its "Robb wins battles → loses war" juncture is sequence-masquerading-as-cause (PRECEDES already covers it), two of three junctures lack a clean terminus, and the realistic monolith yield was ~6–10 edges over 1.5–2 sessions (i.e. another "weak session" in disguise if built blindly).

Concrete corrections adopted: two alias-resolver bugs (`bran-s-fall` and `tyrion-kills-tywin` resolve to *nothing* — old hubs predate the spaced-alias rule), a missing `robb-proclaimed-king-in-the-north` beat (the gap between Ned's execution and the Red Wedding), a missing `robert-orders-daenerys-assassination` node (only the Ned-cancels version exists), all three bridges canon-confirmed with cites (Varys-Illyrio = AGOT Arya III tunnel scene; Robert's order = Eddard VIII; Drogo's vow = Daenerys VI).

## The decomposition dip

Ran the WO5K decomposition dip → `working/wo5k-decomposition.md`. WO5K is a **trigger-tree rooted at Robert's death** — which currently fans out to *only* `arrest-of-eddard-stark`; the whole five-way succession fracture is unwired. There are easily 6–10 real junctures (one per king's entry + several falls), not the three the critics first named. Ranked buildable order: **#1 J3 Robb-proclaimed-King-in-the-North** (1 mint + 2 edges, extends B3, cheapest real gap) · #2 Q5 Crag→Jeyne · #3 Blackwater-upstream (Renly→Stannis→Tyrell-realignment, completes #7) · #4 Karstark→Robb-isolation · #5 Balon→Winterfell. Skip the westerlands battle sequence (pure PRECEDES) and "Robb's political isolation" as a unified arc.

Note: the *root* juncture (Robert's death → the fracture) did **not** top the dip's ranking — it optimizes cheap-and-clean, a different axis than root-importance. Flagged for when we get into it; the fracture is more abstract/agency-heavy to model.

## Where it leaves us

The track is no longer dip-driven-cheapest. It's backlog-driven-magnitude, with containers decomposed via their own dips, cheap dips kept as a secondary opportunistic track, and the dip itself relegated to a post-build coverage check. Next build is J3 (cheapest WO5K juncture) as the first test of the decomposed approach. The bigger payoff is structural: as we build the late-game and Essos arcs and root each at its existing upstream node, the graph becomes one walkable web spanning all five books — which was the point all along.
