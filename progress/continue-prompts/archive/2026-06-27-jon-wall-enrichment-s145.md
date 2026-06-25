# SESSION 145 — Jon Snow / the Wall enrichment (pass 1) — the L1 round continues

> **This is Session 145.** Stamp your worklog entry `### Session 145` in `worklog.md`.
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; codified as step 5 of the machine in `working/arc-enrichment-backlog.md`). Run it yourself at the end once harvests are accounted for.

## Why this, and why now
S143 REOPENED the L1 round (Matt "9 isn't enough" — the 9 dips clustered in KL/Riverlands/backstory). **S144 did the first heavyweight = Daenerys/Meereen.** Jon/the Wall is the **co-equal next pick** per `working/enrichment-coverage-plan.md` (A1.2): the NORTH spine is built but Jon has **348 edges / 0 arc-connected** — his connections are wiki-dyadic social web, not the causal event substrate. Same proven machine.

## The unit: Jon Snow / the Wall (the Watch leadership arc)
- **Already built (DON'T re-mint — dedup against the graph, query `edges.jsonl` / `graph-query.py`, not node prose):** the NORTH spine N1–N6 — `great-ranging` → `fist-of-the-first-men` → `mutiny-at-castle-black` (Craster's) → `battle-beneath-the-wall` → `jon-elected-lord-commander` → Slynt-execution → `jon-allows-free-folk-through-the-wall` → `pink-letter-delivered` → `jon-is-stabbed-repeatedly`; plus `roose-bolton-made-warden`, the Stannis-march, Crofter's-village. Nodes exist for `bowen-marsh`, `mance-rayder`, `val`, `hardhome`, etc.
- **The gap a dip fills (the missing texture):**
  - **The Bowen-Marsh assassination conspiracy — THE MARQUEE WHODUNIT.** The Shieldhall speech is the trigger; the conspirators' agency is thin. Who else was in on it? Wick Whittlestick, Bowen Marsh ("for the Watch"), Othell Yarwyck, Bowen's faction. Mint a `the-shieldhall-speech` trigger node (MISSING — confirmed) + wire `bowen-marsh` + co-conspirators `AGENT_IN`/`SUSPECTED_OF` the stabbing; `jon-allows-free-folk... MOTIVATES bowen-marsh` (the grievance). This is our SUSPECTED_OF / unproven-agency wheelhouse.
  - **The Mance/"Rattleshirt" glamour deception** — Melisandre glamours Mance as Rattleshirt; `rattleshirt` node MISSING — check, then `mance-rayder DISGUISED_AS`/`IMPERSONATES` + Melisandre AGENT_IN the glamour. (Prologue Varamyr + Melisandre chapter.)
  - **Hardhome as a revelation-event** — the wildling-rescue catastrophe (the Hardhome letter); wire as a beat + its role in Jon's MOTIVATES substrate.
  - **The wildling-integration politics** — the free-folk-through-the-Wall decision's cost to Jon's standing; Tormund (check slug `tormund-giantsbane` vs `tormund`), Val, the hostages, the spearwives.
  - **The Stannis-at-the-Wall relationship texture** — Stannis's offer of Winterfell/legitimization; Jon's refusal; the Pink Letter fallout.
  - **Slynt-execution color** (the node exists — add participant/witness texture).
  - **Jon's MOTIVATES substrate (C5)** — the leadership decisions above the spine.
- **Cross-arc / hygiene to watch:** `mutiny-at-castle-black` (Craster's, ASOS) vs the Bowen-Marsh stabbing (`jon-is-stabbed-repeatedly`, ADWD) — DON'T conflate (the S125/S126 merge already canonicalized `jon-is-stabbed-repeatedly`). Watch for `tormund` slug variants. Theory-adjacent (Jon's parentage / Azor Ahai) stays GATED — evidence edges only, no theory readings.

## The machine (proven 10×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Fan out 4 fresh Sonnet lens subagents** on the built unit, each a different lens, PROPOSE-don't-mint + dedup-check every node against the graph:
   (a) secondary-character sub-arcs (Bowen Marsh / Melisandre / Stannis / Tormund / Val / Mance / Selyse),
   (b) **the assassination conspiracy + whodunit thread** (who stabbed Jon, the Shieldhall trigger, the SUSPECTED_OF layer) + revelation-events (Hardhome, the glamour),
   (c) descriptive/quote/object depth (the Wall, Longclaw, the horn, Ghost, the weirwood),
   (d) **the 4th causal-wiring lens** (existing-node↔existing-node CAUSES/ENABLES/MOTIVATES the topic-lenses miss — incl. cross-container seams: NORTH↔WO5K [Stannis], NORTH↔Essos? no; the free-folk decision → the stabbing chain).
   Paste the locked vocab + the harvest snippet (split-the-bar WIDE-OPEN on food incl. the grim register — the Wall has Hobb's stew, the ranging starvation, Craster's). Paste the canonical vocab terms (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) — subagents don't load CLAUDE.md.
   Chapters: ADWD `adwd-jon-01.md`…`adwd-jon-13.md`, `adwd-melisandre-01.md`, `adwd-prologue.md` (Varamyr); plus ASOS Jon chapters for the Mance/wildling backstory if needed.
2. **Synthesize + decide** what to mint vs defer.
3. **Verify every cited line against the chapter files** (deterministic line-check — reuse the pattern in `working/enrichment/dany-meereen/verify_lines.py`; quote a single contiguous substring, never splice across a dialogue attribution). Mint via a `scripts/mint_jon_wall_enrichment.py` (backup `_regrounding/edges-pre-jon-wall-enrichment-<date>.jsonl` + re-run guard). Node aliases = natural SPACED phrases.
4. **Fresh-verify the interpretive/causal edges** (independent Sonnet, vs LOCAL cache). Stamp, rebuild derived artifacts (`weirwood refresh`). **Consume** the harvest pointers. Smoke-test `--full-chain` / `--container north`.
5. **Close out — run `/endsession`** (pre-authorized; see header).

## STEP 0 — light confirm
Confirm Jon/the Wall is still the pick (co-equal per S143 plan; the alternate is interleaving a cheap L2 — B1 Frey-pies/GNC, B4 Ned black-cells, B7 Kingslayer quote). Then run the machine.

## DO NOT
launch the PARKED graph-wide causal-wiring track · run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · assert theory readings (Jon's parentage / Azor Ahai stay GATED — evidence edges only).

## Read first
- `working/enrichment-coverage-plan.md` (the S143 plan — scope card A1.2 + the full ranking)
- `working/arc-enrichment-backlog.md` (scope model + ledger + the enrichment-pass machine)
- `worklog.md` S144 entry + the STATUS block · memory `project_arc_enrichment_track`
