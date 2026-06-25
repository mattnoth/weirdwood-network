# SESSION 147 — Next enrichment dip (the reopened L1 round — last spine-only heavyweight)

> **This is Session 147.** Stamp your worklog entry `### Session 147` in `worklog.md`.
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 5 of the machine in `working/arc-enrichment-backlog.md`). Run it yourself at the end once harvests are accounted for.

## Where we are
The reopened L1 round (S143, Matt "9 isn't enough") has now done **3 of the 4 spine-only heavyweight arcs**: Daenerys/Meereen (S144) · Jon/the Wall (S145) · Bran/greenseer (S146). The KL/Riverlands/backstory cluster (9 arcs) is fully enriched. What remains in the round (per `working/enrichment-coverage-plan.md`):
- **A1 — spine-built, enrich-ready (same proven machine, NO build needed):** **AEGON** (the Golden Company invasion; spine built S128, container `aegon`=12) — **the LAST spine-only heavyweight.** Heavy **Varys** character-web overlap (a dip here builds most of the C1 Varys residual). Also feeds the Connington/greyscale + Blackfyre-lineage texture.
- **A2 — needs build+enrich first (heavier):** Sansa/Vale (`littlefinger-smuggles-sansa` has 0 causal downstream — the whole Vale arc is dark; highest cross-arc payoff, builds most of Petyr) · Theon/Reek (Winterfell→Dreadfort→Jeyne-as-Arya; the flagged cross-identity Reek=Theon case).
- **B — cheap L2 interleaves inside the 9 enriched arcs** (lighter sessions): B1 Red-Wedding Frey-pies/GNC · B4 Ned's-downfall black-cells (the `varys-visits-ned` ENABLES→confession island) · B7 the Kingslayer-quote/Jaime-reputation concept.

## STEP 0 — surface the fork to Matt (don't auto-pick)
Prior dips (S140–S146) surfaced the genuine fork via AskUserQuestion at STEP 0. Do the same. **Recommended default:** **AEGON** — the LAST spine-only heavyweight, closes the reopened L1 round, and builds most of the Varys web for free. The cheap L2 interleave (B1/B4/B7) is the lighter alternative; A2 Sansa/Vale or Theon/Reek is the heavier build+enrich. Confirm the unit, then run the machine.

## The machine (proven 12×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--container`/`--full-chain` of the unit's hub + satellites + dedup checks; write `working/enrichment/<unit>/baseline.md`. Load the locked vocab from `working/wiki/data/edge-type-counts.md` (170 canonical types; verify membership exactly — `MANIPULATES`/`DISGUISED_AS`/`WARGS_INTO`/`DREAMS_OF`/`PRACTICES` ARE in it).
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup-check every node: (a) secondary-character sub-arcs, (b) the whodunit/revelation thread + SUSPECTED_OF layer, (c) descriptive/quote/object depth, (d) **the existing-node↔existing-node causal-wiring lens** (cross-container seams — the highest-value structural fixes; for AEGON the RR→AEGON `exile-of-jon-connington ENABLES aegon-revealed` seam is already wired — look for new ones). Paste the canonical vocab terms (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) + the harvest snippet (split-the-bar WIDE-OPEN on food incl. the grim register) — subagents don't load CLAUDE.md.
3. **Synthesize + decide** (Opus). Encode as `candidates.json`. **Whole-file line-check every quote** (reuse `working/enrichment/bran/verify_lines.py` — point it at your unit's candidates.json; it greps the WHOLE chapter file for the true line). Mint via a `scripts/mint_<unit>_enrichment.py` (reads candidates.json, re-greps for the authoritative line, backup + re-run guard + slug pre-check). Node aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal edges + any proposed modifications (vs LOCAL cache). Apply via a `finalize_<unit>.py` (drops/adjusts/retirements/re-points + stamp `verified_by`). Re-run the 0-drift check. (Edge-only dips don't need `weirwood-refresh`; node-adding dips do.) Smoke `--full-chain`/`--container`.
5. **Consume harvest** (attach load-bearing quotes inline; park food/description in `working/harvest-queue.md`).
6. **Close out — run `/endsession`** (pre-authorized).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · assert theory readings (the Aegon-is-a-Blackfyre / fAegon-babe-swap / R+L / Azor Ahai / Bloodraven theories stay GATED — evidence edges only) · perpetuate the stray `containers: [jon]` tag (use approved containers only: essos/wo5k/north/aegon/bran).

## Read first
- `working/enrichment-coverage-plan.md` (the S143 ranking + scope cards — AEGON = card A1.3)
- `working/arc-enrichment-backlog.md` (ledger + the enrichment-pass machine + the scope model)
- `worklog.md` S146 entry + the STATUS block · memory `project_arc_enrichment_track`
- For an AEGON pick: the prior decomposition `working/aegon-container-decomposition.md` + the S128 spine-build (worklog archive) + memory `project_bloodraven_enrichment_dip` if the Varys/Connington threads pull toward it.
