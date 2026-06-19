# Session 106 — Causal-arc execution: traversal primitive + two Tier-A arcs (2026-06-19)

**Model:** Opus 4.8 orchestrator + 1 background `general-purpose` doc agent + 4 `general-purpose` subagents (2 arc-research, 2 fresh edge-verification).
**Predecessor:** S105 produced the causal-arc scaling strategy + the parent-node recommendation, gated on Matt's ratification. This session executed against it.
**Continue prompt consumed:** `progress/continue-prompts/2026-06-18-causal-arc-execution.md` (Step 1 fully done; Step 2 partially — 2 of the Tier-A arcs shipped, rest dip-gated).

---

## What was decided

### 1. Chain-as-arc ratified (no umbrella parent nodes)
Matt asked for the advisory board's recommendation before ratifying. The board (narrative-craft / graph-modeling / canon / skeptic, S105) had recommended **chain-as-arc**: an arc IS its `CAUSES`/`TRIGGERS`/`MOTIVATES` edges, queried via a `--causal-chain` primitive — NOT a minted `event.arc`/`event.conspiracy` parent hub. The skeptic's decisive point: a single beat belongs to many overlapping arcs (Bran's fall is in ≥5), so no one parent can own it. Matt ratified. **This supersedes the S96 "PARENT-SHAPE RULE"** (mint an `event.conspiracy` hub wrapping the event) and the parked `archive/2026-06-15-arc-wave1-mint.md` built on it. Memory `project_narrative_arc_reification` was rewritten to record the reversal so a future session isn't misled.

### 2. Scope = 2 Tier-A arcs as one validating batch — NOT a fleet
Matt floated a batch-job/fleet ("orchestrator spawns agents to mint all the main arcs of the 5 books"), then caught himself against the strategy's anti-mass-mint discipline. The reasoning that confirmed it: arc-minting is **low-volume + judgment-heavy + write-conflicting** — the opposite of what a fleet wins on. Specifically (a) the load-bearing in-saga arc set is small (~5, not hundreds); (b) the agency-collapse check is exactly what a blind worker collapses; (c) parallel minting reintroduces the dup-pollution the dedup gate exists to prevent (the dedup lookup checks the *committed* graph, not a sibling agent's concurrent mint). So: 2 Tier-A arcs serial, then re-dip. Side note (Matt): **D&E is main-arc in priority** (Bloodraven-in-the-flesh seeds theory anchors) — it waits only because its chapters aren't Pass-1-extracted, not because it's minor.

### 3. "dip" documented as a live process term
Matt asked what a "dip" is and to document it. The term was only *decoded as retired* ("Mode 3 → the dip") in `reference/glossary.md`, never defined. Added a **"Method terms (live)"** section to glossary.md defining `dip` (a grounded-agent validation probe — an agent restricted to graph-only answers is posed reader-style questions; the ones it fumbles *for lack of structure* rank what to build next) + `dip-driven` cadence.

---

## What was built (both arcs used the same proven machine)

The reusable machine, now run 4× (RR S104, Bran S105, Sack + PW S106):
1. **Research subagent** (read-only, local cache) — identify beats, dedup-check each, gather verbatim quotes file:line, propose edges.
2. **Orchestrator trims + mints** — I cut over-mints, then a `scripts/mint_<arc>_arc.py` script (backup + re-run guard) appends edges; beat-node `.md` files written directly.
3. **Rebuild** targeted event index + alias resolver.
4. **Fresh-subagent verify** each causal edge + agency split vs local cache; causal edges minted `verified_by: pending-*`, stamped on CONFIRM.
5. **Smoke-test** `--causal-chain` + natural-phrase discoverability.

### Step 1 — `--causal-chain` primitive
`scripts/graph-query.py --causal-chain <slug>` walks CAUSES/TRIGGERS/MOTIVATES transitively both directions (PRECEDES excluded — pure chronology), cycle-safe, BFS depth-tagged. +10 tests. This is what makes "no umbrella parent" workable: the whole-arc query works from any beat.

### Sack of King's Landing (4 beats, 21 edges)
Beats: `pycelle-opens-the-gates` (event.deception), `aerys-commands-the-city-burned` (event.incident), `slaying-of-aerys-ii-the-kingslaying` (event.assassination), `murder-of-elia-martell-and-rhaegars-children` (event.assassination). Causal spine: `pycelle-opens-gates CAUSES sack`; `aerys-burn-order TRIGGERS kingslaying`; `murders MOTIVATES ned`.
- **Dedup catch:** the gate flagged `fall-of-kings-landing` as a possible collision — it's the *Dance of the Dragons* fall (Rhaenyra takes the city from Aegon II), a distinct event ~130 yrs prior. Kept separate. Also found the sack hub already carried a flat role-edge layer (from `historical-anchor-w1`); the new beats *decompose* it (flat = summary, beats = structure) rather than duplicate.
- **Agency-collapse keystone:** `asos-tyrion-06.md:187-191` (Tywin's confession) grounds the whole murder beat AND the split — Tywin `COMMANDS_IN` (ordered the children dead) but explicitly NOT the rape/brutality ("even you will not accuse me of giving that command"); Gregor/Amory `AGENT_IN` (executed, and exceeded the order). Verifier: "textually exact."

### Purple Wedding (4 beats, 20 edges)
Beats: `sansa-receives-the-poisoned-hairnet` (event.deception), `tyrion-accused-of-poisoning-joffrey` (event.incident), `trial-of-tyrion-lannister` (event.trial), `littlefinger-smuggles-sansa-out-of-kings-landing` (event.deception). Spine: `hairnet CAUSES joffrey-death TRIGGERS accusation CAUSES trial`.
- **Whodunnit integrity (the hard part):** the in-story frame is that Tyrion did it; the text doesn't establish that. So **zero** `tyrion KILLS/POISONS joffrey` edges — Tyrion is `VICTIM_IN` the accusation and trial only. The real conspiracy (Littlefinger architect, Olenna hand) was *already modeled* on the existing `death-of-joffrey-baratheon` node — the dedup gate caught it, so it wasn't duplicated. Verifier grepped for `tyrion …POISONS… joffrey` → zero hits. CONFIRM.
- One node quote was a paraphrase on first write (the trial node's "trial by battle" speech); caught by verifying the line and fixed to the verbatim `asos-tyrion-10.md:65`.

---

## Verification + integrity
Both arcs' causal edges were checked by **independent fresh subagents** against the local cache — both returned **ALL-CONFIRM** (verbatim-faithful, correct CAUSES/TRIGGERS/MOTIVATES type calls, agency split faithful, no overclaim, hard-stops respected). I never had to review edges by hand — the concrete answer to "I can't review 100 of these." All 6 causal edges are Tier-2 (interpretive link); role edges Tier-1 (factual presence), with two Tier-2 role edges where the attribution rests on a later confession (petyr COMMANDS_IN the hairnet; cersei AGENT_IN the accusation).

Totals: nodes 8,525→8,533 (+8), edges 22,174→22,215 (+41), orphans 62 unchanged, edge types 128 (no new types), 0 pending verifications, pytest 1307 pass / 1 pre-existing `cwd-is-tmp` fail. Backups + reproducible mint scripts retained. No extractions ran (no Pass-1 work) — extraction-archive rules N/A this session.

## Next
Per the dip-driven cadence: **re-run an arc-weighted Mode-3 dip before any Tier-B minting** (Catelyn-frees-Jaime→Red-Wedding-feed; Greyjoy→Theon-hostage→Northern-invasion). Two small cleanups for the backlog: duplicate `robert-baratheon`/`robert-i-baratheon` node; sack hub's junk `DEFEATS: Elia of Dorne` infobox edge.
