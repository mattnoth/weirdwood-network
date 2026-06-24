# SESSION 140 — Enrichment: next dip OR the L2-granular planning session
> **This is Session 140.** Stamp your worklog entry `### Session 140` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 lenses/verify + Opus 4.8 orchestrator (same machine as S133–S139).
> **D&E Pass-1 is PARKED** (Matt). Stage only your own files by explicit path; never `git add -A`.

## Where we are
The enrichment phase is the primary track, descending major arcs → sub-plots → characters. **Six major-arc dips shipped: RR (S133) · Red Wedding (S134) · Purple Wedding (S135) · Ned's Downfall (S137) · Blackwater (S138) · Tywin's Death (S139).** All 5 approved containers are spine-complete (essos/wo5k/north/aegon/bran). **Harvest queue was DRAINED S139** (124 open → 0; 369 done / 25 parked).

## STEP 0 — pick the next unit (NO pre-picked target). The L1 round is winding down — genuinely surface both forks to Matt.
1. **Continue the L1 major-arc descent.** Remaining enrich-ready L1 arcs (both have built spines):
   - **Cersei's downfall** (S114 AFFC spine) — off-spine: the Blue Bard, the Faith Militant's rise, the Kettleblack triple-agent web (a parked harvest row, asos-sansa-06:163), Margaery's arrest, Osney's confession mechanics.
   - **Brienne → Stoneheart** (S115 AFFC spine) — off-spine: the Brotherhood's hangings, the Saltpans atrocity, Hyle/Pod capture, the hanging-tree choice.
   - **Sack of KL** — FLAGGED a double-dip: its core was wired in the S133 RR pass + the S139 Elia-murder→Oberyn seam. **Check overlap before picking** — likely lower marginal yield than the two AFFC arcs.
   Run a quick 3-advisor board (saga-demand / graph-gaps / tractability) OR a demand-dip to pick — same as S135/S136.
2. **The L2-granular planning session (Matt S130).** After the major-arc round, Matt wants a dedicated session to *enumerate + scope the granular sub-plot/character dip list* before diving into L2. **The major-arc round is now nearly exhausted (only 2 clean L1 arcs left), so this fork is a genuine option this session** — if Matt judges the L1 round "done enough," do this instead.

**Confirm the pick with Matt** (the round is winding down — don't auto-assume fork 1). If fork 1, recommend Cersei's downfall or Brienne→Stoneheart over the Sack-of-KL double-dip.

## STEP 1 — run the proven S133–S139 machine (once the target is picked)
Dump the cluster (`graph-query.py --neighbors / --full-chain / --container`) → `working/enrichment/<unit>/baseline.md` → fan out **4 fresh Sonnet lenses** PROPOSE-only:
(1) downstream-causal/consequence · (2) secondary-character sub-arcs + SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring** (the cross-arc seam lens — ALWAYS include, standing policy S134).
**Paste into every lens:** the locked vocab (170 types, `grep -oE '^\| \`[A-Z_]+\`' reference/architecture.md`), the **line-check rule** (every quote a VERBATIM CONTIGUOUS span incl. internal dialogue quote marks; never splice across a `," said X, "` attribution; exact begin-line number), the agency rules (NO CAUSES between sibling/constitutive beats; MOTIVATES→character only; ENABLES=door-opener), and **SPLIT THE BAR** (tight edge bar; WIDE-OPEN harvest — EVERY meal/food/drink incl. the grim/starvation register, plus descriptions/quotes/foreshadowing as `chapter:line / kind / note` pointers into `working/harvest-queue.md`).

Then: Opus synthesizes + **line-checks every quote against the files** (the recurring catch — S139 caught lenses mis-citing a testimony block to the wrong CHAPTER; always grep the anchor phrase to confirm the chapter:line before minting) → mint via `scripts/mint_<unit>_enrichment_s140.py` (copy `scripts/mint_tywin_death_enrichment_s139.py` as the template; `mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard, NEW_NODE_SLUGS excluded from precheck, optional `qualifier` field supported) → `python3 scripts/verify-edge-quotes.py --run-id <id>` (0 drift) → `bash scripts/weirwood-refresh.sh` only IF new nodes minted → **independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — agency-collapse, temporal inversion, incidental-co-location ENABLES, mistargets/wrong-book, WITNESS text-anchor, SUSPECTED overclaim, over-read of unconfirmed facts; apply verdicts, flip `verified_by` pending→fresh) → `--full-chain` smoke → push any harvest rows the dip surfaced into `working/harvest-queue.md` → increment the ledger + Session-140 worklog entry.

## Read first
- `working/arc-enrichment-backlog.md` (the ledger + the "scope model" top section)
- `scripts/mint_tywin_death_enrichment_s139.py` (the mint template, incl. the `qualifier` field) + memory `project_arc_enrichment_track`
- `worklog.md` Session 139 entry (the most recent dip + harvest pass, for the machine in action)

## DO NOT
mass-mint · CAUSES between sibling/constitutive beats (agency-collapse) · assert facts the chapter leaves unconfirmed (S139 dropped `oberyn POISONS gregor` — ASOS only says "Oil? Or poison?") · launch the PARKED graph-wide causal track · pull TWOW/gated-theory READINGS into the causal map · run extractions without asking · `/endsession` without permission · un-park D&E · `git add -A`.

## Parked harvest rows (25; if a future harvest/dip wants them)
9 NEW S139 parks are edge/future-node/batch candidates: the ~20-ship `WIELDED_IN battle-of-the-blackwater` roster (acok-davos-03:47 — **deterministic Python batch**, not a prose attach); the Kettleblack cross-identity web (asos-sansa-06:163 → cross-identity-detector); the Ashara/Ned/Oberyn Harrenhal-tourney seam; `walder ISOLATES grey-wind` (no vocab type); future-node-blocked beats (Targaryen-exile, Connington-stripped-by-Aerys, tyrion-loses-the-handship). Plus 16 older AFFC/Essos parks.
