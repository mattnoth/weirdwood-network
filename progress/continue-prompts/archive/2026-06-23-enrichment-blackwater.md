# SESSION 138 — Enrichment dip #5: Blackwater
> **This is Session 138.** Stamp your worklog entry `### Session 138` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 lenses/verify + Opus 4.8 orchestrator (same machine as S133–S137).
> **D&E Pass-1 is PARKED** (Matt). Stage only your own files by explicit path; never `git add -A`.

## Where we are
The enrichment phase is the primary track, descending major arcs → sub-plots → characters. **Four major-arc dips shipped: RR (S133) · Red Wedding (S134) · Purple Wedding (S135) · Ned's Downfall (S137).** This is the **5th**.

## STEP 1 — target is already chosen: **Blackwater**
The S136 board flagged **Blackwater** as the clean #2 (after Ned's Downfall). No need to re-board. Dump the cluster yourself with `graph-query.py --neighbors battle-of-the-blackwater` / `--full-chain` / `--event-participants` + the surrounding nodes to build `baseline.md`. (S111 already wired 3 downstream CAUSES from `battle-of-the-blackwater`; S123 wired the J2+J9 upstream `stannis-absorbs-renly-s-host` + `littlefinger-brokers-tyrell-lannister-alliance` ENABLES. So the spine exists — the gap is the off-spine substrate: the wildfire chain mechanics, the chain-boom, Tyrion's sortie + the burning, Garlan-as-Renly's-ghost, the Hound's retreat, the Antler Men, Stannis's assault waves, the participants/witnesses.)

## STEP 2 — run the proven S133–S137 machine
Shared dedup `baseline.md` → fan out **4 fresh Sonnet lenses** PROPOSE-only (paste the locked vocab + the harvest snippet + the **line-check rule**: every quote a VERBATIM CONTIGUOUS span INCLUDING internal dialogue quote marks). The 4 lenses: (1) downstream-causal/consequence · (2) secondary-character sub-arcs + SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring** (the cross-arc seam lens — ALWAYS include it, standing policy S134). →
**SPLIT THE BAR (paste into every lens prompt):** the edge bar is TIGHT (high-confidence, fresh-verifiable) but the **harvest bar is LOW and WIDE-OPEN.** **Capture EVERY meal / food / drink — maximal, including the grim end (gruel, prison rations, bark, starvation, peasants with no food); Matt wants ALL meals.** Plus every physical/clothing description, notable quote, foreshadowing beat. Over-capture is the goal; pre-dedup is NOT the lens's job. →
Opus synthesizes + **line-checks every quote against the files** → mint via `scripts/mint_blackwater_enrichment_s138.py` (copy `scripts/mint_neds_downfall_enrichment_s137.py` as the template; `mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard) → `python3 scripts/verify-edge-quotes.py --run-id <id>` (0 drift) → `bash scripts/weirwood-refresh.sh` only IF new nodes minted →
**independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — agency-collapse [no CAUSES between constitutive/sibling beats, S120], temporal inversions, incidental-co-location ENABLES, mistargets [the S137 Varys-node + AFFC-wrong-book catches]; apply verdicts) → `--full-chain battle-of-the-blackwater` smoke test → consume the adjacent harvest rows → increment the ledger (`Blackwater | arc/cluster | 1`) + Session-138 worklog entry.

## Read first
- `working/arc-enrichment-backlog.md` (the ledger + the "scope model" top section)
- `scripts/mint_neds_downfall_enrichment_s137.py` (the mint template) + memory `project_arc_enrichment_track`

## Harvest note (Matt, S137 — STANDING RULE, not a separate session)
Maximal meal capture happens **inside the dip's harvest bar** (split-the-bar), not as a standalone full-corpus pass. Any time anyone eats — feast to bark to empty bellies — capture it. The 82 open queue rows + whatever this dip refills get drained opportunistically / in periodic queue passes, NOT by sweeping whole books.

## DO NOT
Refetch wiki / any HTTP · mass-mint · CAUSES between sibling/constitutive beats (agency-collapse) · re-board the target · launch the PARKED graph-wide causal track · pull TWOW/gated-theory READINGS into the causal map · scope a separate "harvest every book" session (Matt: never asked for that) · run extractions without asking · `/endsession` without permission · un-park D&E · `git add -A`.
