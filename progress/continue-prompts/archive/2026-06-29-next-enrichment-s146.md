# SESSION 146 — Next enrichment dip (the reopened L1 round continues)

> **This is Session 146.** Stamp your worklog entry `### Session 146` in `worklog.md`.
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 5 of the machine in `working/arc-enrichment-backlog.md`). Run it yourself at the end once harvests are accounted for.

## Where we are
The reopened L1 round (S143, Matt "9 isn't enough") has now done **2 of the 4 spine-only heavyweight arcs**: Daenerys/Meereen (S144) + Jon/the Wall (S145). The KL/Riverlands/backstory cluster (9 arcs) is fully enriched. What remains in the round (per `working/enrichment-coverage-plan.md`):
- **A1 — spine-built, enrich-ready (same proven machine, NO build needed):** **AEGON** (the Golden Company invasion; spine built S128, container `aegon`=12) · **Bran** (the greenseer arc; spine built S130, container `bran`=13; pairs with the flagged Bloodraven character work).
- **A2 — needs build+enrich first (heavier):** Sansa/Vale (`littlefinger-smuggles-sansa` has 0 causal downstream — the whole Vale arc is dark) · Theon/Reek (Winterfell→Dreadfort→Jeyne-as-Arya).
- **B — cheap L2 interleaves inside the 9 enriched arcs** (lighter sessions): B1 Red-Wedding Frey-pies/GNC · B4 Ned's-downfall black-cells (the `varys-visits-ned` ENABLES→confession island) · B7 the Kingslayer-quote/Jaime-reputation concept.

## STEP 0 — surface the fork to Matt (don't auto-pick)
Prior dips (S140–S142) surfaced the genuine fork via AskUserQuestion at STEP 0. Do the same. **Recommended default:** the next spine-only heavyweight — **Bran** (enrich-ready, greenfield-lit, and it sets up the long-flagged Bloodraven character dip via the shared cave cluster) or **AEGON** (enrich-ready). The cheap L2 interleave (B1/B4/B7) is the lighter alternative if Matt wants a shorter session. Confirm the unit, then run the machine.

## The machine (proven 11×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--container`/`--full-chain` of the unit's hub + satellites + dedup checks; write `working/enrichment/<unit>/baseline.md`. Load the locked vocab from `working/wiki/data/edge-type-counts.md` (170 canonical types; verify membership exactly — `MANIPULATES`/`DISGUISED_AS`/`WARGS_INTO` ARE in it).
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup-check every node: (a) secondary-character sub-arcs, (b) the whodunit/revelation thread + SUSPECTED_OF layer, (c) descriptive/quote/object depth, (d) **the existing-node↔existing-node causal-wiring lens** (cross-container seams — the highest-value structural fixes). Paste the canonical vocab terms (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) + the harvest snippet (split-the-bar WIDE-OPEN on food incl. the grim register) — subagents don't load CLAUDE.md.
3. **Synthesize + decide** (Opus). Encode as `candidates.json`. **Whole-file line-check every quote** (reuse `working/enrichment/jon-wall/verify_lines.py` — greps the WHOLE chapter file for the true line; the `.md` files store each paragraph as one long line). Mint via a `scripts/mint_<unit>_enrichment.py` (reads candidates.json, re-greps for the authoritative line, backup + re-run guard + slug pre-check). Node aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal edges + any proposed modifications (vs LOCAL cache). Apply via a `finalize_<unit>.py` (drops/adjusts/retirements + stamp `verified_by`). Re-run the 0-drift check. `weirwood-refresh`. Smoke `--full-chain`/`--container`.
5. **Consume harvest** (attach load-bearing quotes inline; park food/description in `working/harvest-queue.md`).
6. **Close out — run `/endsession`** (pre-authorized).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · assert theory readings (R+L=J / Azor Ahai / the Bloodraven theories stay GATED — evidence edges only) · perpetuate the stray `containers: [jon]` tag (use approved containers only: essos/wo5k/north/aegon/bran).

## Read first
- `working/enrichment-coverage-plan.md` (the S143 ranking + scope cards)
- `working/arc-enrichment-backlog.md` (ledger + the enrichment-pass machine + the scope model)
- `worklog.md` S145 entry + the STATUS block · memory `project_arc_enrichment_track`
- For a Bran/AEGON pick: the prior decomposition dips `working/bran-decomposition.md` / `working/aegon-container-decomposition.md` (archived continue prompts) + memory `project_bloodraven_enrichment_dip` (if Bran).
