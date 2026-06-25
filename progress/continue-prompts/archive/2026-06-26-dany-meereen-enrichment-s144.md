# SESSION 144 — Daenerys / Meereen enrichment (pass 1) — the L1 round REOPENS

> **This is Session 144** (graph track). Stamp your worklog entry `### Session 144` in `worklog.md`.
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.

## Why this, and why now (S143 planning outcome)
The S143 planning session (Matt-prompted: *"9 doesn't seem like enough — are there major narrative points we're
missing?"*) found the answer is **yes**: the 9 enriched L1 arcs all cluster in **King's Landing / the Riverlands /
backstory**. The **Daenerys/Essos, Jon/Wall, AEGON, and Bran** halves of the saga got *spine builds* (S119–S130) but
**zero enrichment dips** (verified: 0 rich event-hubs in those containers; Jon 348 edges / 0 arc-connected; Dany
304/0). **Matt chose to REOPEN the L1 round, Daenerys/Meereen first.** Full ranked plan: **`working/enrichment-coverage-plan.md`**.

This is a normal L1 arc-enrichment dip — same machine as RR/Red-Wedding/…/Sack (9 done). The arc's causal SPINE is
already built (Essos E1–E5); this dip adds the **political + whodunit + participant texture** the spine lacks.

## The unit: Daenerys / Meereen (Slaver's Bay political arc)
- **Already built (don't re-mint — dedup against the graph):** the Essos spine E1–E5 — `fall-of-astapor` →
  `battle-near-yunkai` → `siege-of-meereen` → `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` →
  `drogon-returns-to-daznak-pit` → `dany-mounts-drogon-and-flees-meereen` → `dany-lost-on-dothraki-sea`; plus
  `sons-of-the-harpy-kill-twenty-nine`. Nodes exist for `hizdahr-zo-loraq`, `daenerys-targaryen`, etc.
- **The gap a dip fills (the missing texture):**
  - **The Sons of the Harpy insurgency** as a hub — `sons-of-the-harpy-insurgency` does NOT exist yet (flagged
    Essos refinement (a)); the killings + the `shadow war` are currently loose. Mint the insurgency hub + wire the
    night-killings, the Brazen Beasts / `shavepate` (Skahaz mo Kandaq) counter-force.
  - **The Hizdahr-as-the-Harpy whodunit** — `hizdahr-zo-loraq SUSPECTED_OF` the harpy killings / the poisoned-
    locusts attempt at Daznak (Tier-2, never asserts — this is the marquee unproven-agency layer, our wheelhouse).
  - **The poisoned locusts** attempt on Dany (SUSPECTED_OF candidates: Hizdahr / the Harpy / others).
  - **The pit-reopening decision**; the **Astapor plague + the Yunkish/Volantene siege ring** closing on Meereen.
  - **Participant roles** on the thin battle/siege hubs: Barristan Selmy (COMMANDS_IN), Daario Naharis, Grey Worm /
    the Unsullied, Brown Ben Plumm + the Second Sons (and Brown Ben's defection), the Green Grace / `galazza-galare`
    (already a node: `galazza-counsels-the-ghiscari-marriage`).
  - **Quaithe's warnings** (FORESHADOWS — "to go forward you must go back…").
- **Cross-arc / hygiene to resolve FIRST:** the `battle-of-yunkai` redirect-stub **dup** (Essos refinement (b)) —
  dedup before wiring. Watch the `shadow-war` / `targaryen-campaign-in-slavers-bay` mistyped/junk-edge nodes
  (known S104 sub-fix — don't wire into the junk edges).

## The machine (proven 9×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Fan out 3–4 fresh Sonnet lens subagents** on the built unit, each a different lens, PROPOSE-don't-mint +
   dedup-check every node against the graph (not node prose — query `edges.jsonl` / `graph-query.py`):
   (a) secondary-character sub-arcs (Barristan/Daario/Skahaz/Brown Ben/Reznak/Green Grace),
   (b) the insurgency + whodunit thread (Harpy, poisoned locusts, Hizdahr suspicion) + contemporaneous revelation events,
   (c) descriptive/quote/object depth (the pit, the harpy masks, the pyramids, the locusts, Quaithe),
   (d) **the 4th causal-wiring lens** (existing-node↔existing-node CAUSES/ENABLES/MOTIVATES the topic-lenses miss —
   incl. cross-container seams to AGOT-Dany and the Quentyn/Doran pact already wired).
   Paste the locked vocab + the harvest snippet (split-the-bar WIDE-OPEN on food/meals incl. the grim register —
   Meereen has feasts, the locusts, honeyed locusts; Matt S137 standing rule). Paste the canonical vocab terms
   (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) — subagents don't load CLAUDE.md.
2. **Synthesize + decide** what to mint vs defer (forward-dangling cross-book nodes defer).
3. **Verify every cited line against the chapter files** (subagents reconstruct quotes — always check; quote a
   single contiguous substring, never splice across a dialogue attribution). Mint via a
   `scripts/mint_dany_meereen_enrichment.py` (backup `_regrounding/edges-pre-dany-meereen-enrichment-<date>.jsonl`
   + re-run guard). Node aliases = natural SPACED phrases, not kebab.
4. **Fresh-verify the interpretive/causal edges** (independent Sonnet, vs LOCAL cache). Stamp, rebuild derived
   artifacts (indexes + alias resolver if nodes added). **Consume** the harvest pointers the dip refilled.
   Smoke-test `--full-chain` / `--container essos`.

## STEP 0 — light confirm
Confirm Daenerys/Meereen is still the pick (Matt chose it S143). Then run the machine. **One dip this session.**

## After this dip
Next in the plan (`working/enrichment-coverage-plan.md`): **A1.2 Jon/the Wall** (the Bowen-Marsh assassination
whodunit), then interleave the cheap L2s (B1 Frey-pies/GNC, B2 Robert Strong, B3 gravedigger, B4 Ned black-cells,
B7 Kingslayer-quote), then A2.2 Sansa/Vale + A2.1 Theon/Reek, then the rest of A1 (AEGON/Bran/Dorne/Euron).

## DO NOT
launch the PARKED graph-wide causal-wiring track · run extractions without asking · un-park D&E · `/endsession`
without permission · `git add -A` (stage your own files by path).

## Read first
- `working/enrichment-coverage-plan.md` (the S143 plan — scope cards A1.1 + the full ranking)
- `working/arc-enrichment-backlog.md` (scope model + ledger + the enrichment-pass machine)
- `worklog.md` S143 entry + the STATUS block · memory `project_arc_enrichment_track`
