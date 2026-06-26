# SESSION 148 — Next enrichment dip (the L1 round is CLOSED → descend to L2 / A2)

> **This is Session 148.** Stamp your worklog entry `### Session 148` in `worklog.md`.
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 5 of the machine in `working/arc-enrichment-backlog.md`). Run it yourself at the end once harvests are accounted for.

## Where we are
The reopened L1 round is **COMPLETE** — all 4 spine-only heavyweight arcs are enriched: Daenerys/Meereen (S144), Jon/Wall (S145), Bran/greenseer (S146), AEGON/Golden Company (S147). The 9 KL/Riverlands/backstory L1 arcs were done S133–S142. **There are no un-enriched L1 arcs left** (except the never-spined A2 tier, which needs build+enrich). The descent now drops to **Level 2 (granular sub-plots inside the enriched arcs)** and **A2 (L1-scale arcs that were never spined)**. Full ranked plan + scope cards: `working/enrichment-coverage-plan.md`.

## STEP 0 — surface the fork to Matt (don't auto-pick)
Prior dips (S140–S147) surfaced the genuine fork via AskUserQuestion at STEP 0. Do the same. The fork now:
- **Cheap L2 interleave (lighter; the plan's step 3)** — a high-payoff granular sub-plot inside one of the 13 enriched arcs. Top picks (all in `enrichment-coverage-plan.md` Class B): **B1 Frey-pies / Grand Northern Conspiracy** (Red Wedding; all nodes built, only the GNC hub + the `ENABLES stannis-march-on-winterfell` seam missing; wo5k→north seam; cheapest high-value) · **B2 Robert Strong** (Oberyn POISONS Gregor + Qyburn; closes 2 dead-ends, AFFC names the manticore venom) · **B3 Sandor/gravedigger** (Brienne→Stoneheart; salience 10/10) · **B4 Ned black-cells** (the varys-visits-ned ENABLES→confession gap) · **B7 Kingslayer-quote** (cheapest; the slaying hub has no `## Quotes`).
- **A2 build+enrich (heavier)** — an L1-scale arc that was never spined: **A2.2 Sansa/Vale** (`littlefinger-smuggles-sansa` is a dead-end; the whole Vale arc is dark; **highest cross-arc payoff per dip** — fixes the longest-orphaned node + the hairnet chain + builds most of **Petyr/C2**; Alayne=Sansa SAME_AS case) · **A2.1 Theon/Reek** (the flagged cross-identity Reek=Theon case; Winterfell→Dreadfort→Jeyne-as-Arya).
- **Recommended default:** start the **cheap L2 round** per the plan's sequence (B1 Frey-pies/GNC is the cheapest, fully-ready, reader-salient pick). But Matt has consistently chosen the more-substantive option — A2.2 Sansa/Vale is the highest-payoff single dip if he wants weight. Confirm the unit, then run the machine.

## The machine (proven 13×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--container`/`--full-chain` of the unit's hub + satellites + dedup checks; write `working/enrichment/<unit>/baseline.md`. Load the locked vocab from `working/wiki/data/edge-type-counts.md` (170 canonical types; **verify membership EXACTLY against the JSON schema — edges.jsonl uses `edge_type`/`source_slug`/`target_slug`, NOT `type`; a naive `"type":` grep returns 0 for everything**).
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup-check every node/edge: (a) secondary-character sub-arcs, (b) the whodunit/revelation thread + SUSPECTED_OF layer, (c) descriptive/quote/object depth, (d) **the existing-node↔existing-node causal-wiring lens** (cross-container seams — the highest-value structural fixes). Paste the canonical vocab terms (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) + the harvest snippet (split-the-bar WIDE-OPEN on food incl. the grim register) — subagents don't load CLAUDE.md.
3. **Synthesize + decide** (Opus). Encode as `candidates.json`. **Whole-file line-check every quote** (reuse `working/enrichment/aegon/verify_lines.py`, point it at your unit's candidates.json; it greps the WHOLE chapter file for the true line). Mint via a `scripts/mint_<unit>_enrichment.py` (reads candidates.json, re-greps for the authoritative line, backup + re-run guard + slug pre-check via `mint_arc_lib.precheck_slugs`). Node aliases = natural SPACED phrases. **Check the live edge-direction convention before emitting** (e.g. GIFTED_TO is giver→recipient in the live data, not architecture's artifact→recipient).
4. **Independent Sonnet fresh-verify** the interpretive/causal edges + any borderline mints (vs LOCAL cache). Apply via a `finalize_<unit>.py` (drops/adjusts/retirements/re-points + stamp `verified_by`). Re-run the 0-drift check. (Edge-only dips don't need `weirwood-refresh`; node-adding dips do.) Smoke `--full-chain`/`--container`. **A flagged-borderline node that fresh-verify rejects → drop it in finalize (this is the propose-then-gate flow working; S147 did exactly this with the kevan-reconciles node).**
5. **Consume harvest** (attach load-bearing quotes inline incl. book-cite overlays onto wiki nodes; park food/description in `working/harvest-queue.md`).
6. **Close out — run `/endsession`** (pre-authorized).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · assert theory readings (fAegon/Blackfyre, R+L, Azor Ahai, frey-pies-confirmed-by-text-beyond-the-named-cooks, Robert-Strong-is-Gregor-as-CERTAIN, gravedigger-is-Sandor-as-CERTAIN — these stay GATED, evidence edges only) · perpetuate the stray `containers: [jon]` tag (use approved containers only: essos/wo5k/north/aegon/bran).

## Read first
- `working/enrichment-coverage-plan.md` (the S143 ranking + Class A/B/C scope cards — B1–B8 + A2.1/A2.2)
- `working/arc-enrichment-backlog.md` (ledger — 13 dips logged + the enrichment-pass machine + the scope model)
- `worklog.md` S147 entry + the STATUS block · memory `project_arc_enrichment_track`
- For the picked unit: its decomposition doc if one exists (`working/<unit>-decomposition.md`); for A2 build+enrich, there is NO spine yet — read the chapter files directly + build the spine first (like the S119/S128/S130 spine builds), THEN enrich.
