# SESSION 141 — Enrichment: last L1 arc OR the L2-granular planning session
> **This is Session 141.** Stamp your worklog entry `### Session 141` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 lenses/verify + Opus 4.8 orchestrator (same machine as S133–S140).
> **D&E Pass-1 is PARKED** (Matt). Stage only your own files by explicit path; never `git add -A`.

## Where we are
The enrichment phase is the primary track, descending major arcs → sub-plots → characters. **Seven major-arc
dips shipped: RR (S133) · Red Wedding (S134) · Purple Wedding (S135) · Ned's Downfall (S137) · Blackwater
(S138) · Tywin's Death (S139) · Cersei's Downfall (S140).** All 5 approved containers are spine-complete.

## STEP 0 — pick the next unit. The L1 round is now ALL BUT EXHAUSTED — surface both forks, don't auto-pick.
1. **Continue the L1 major-arc descent.** Only ONE clean enrich-ready L1 arc remains:
   - **Brienne → Stoneheart** (S115 AFFC spine) — off-spine: the Brotherhood-without-banners' hangings, the
     Saltpans atrocity, Hyle Hunt / Podrick capture, the sword-or-noose hanging-tree choice, the Gendry/inn
     thread, Stoneheart's vengeance campaign. Cross-book root already wired (`catelyn-is-killed` → Stoneheart).
   - **Sack of KL** — FLAGGED a double-dip: core wired in the S133 RR pass + the S139 Elia-murder→Oberyn seam.
     **Check overlap before picking** — likely lower marginal yield. Off-spine remnants: the wildfire, the
     sack's atrocities (Elia/Aegon/Rhaenys), Lannister-host-enters-the-city.
2. **The L2-granular planning session (Matt S130) — now the LEADING option.** With the L1 round essentially
   done (1 clean arc left), Matt wants a dedicated session to *enumerate + scope the granular sub-plot/
   character dip list* before diving into L2. The seeds are in `working/arc-enrichment-backlog.md` (character
   roster, event-unit candidates, the WO5K multi-pass note); the planning session turns those into a real
   ranked list now that we know far more about what each cluster needs.

**Confirm the pick with Matt** (the round is winding down — genuinely surface both forks; if Matt judges the
L1 round "done enough," do the planning session). If fork 1, Brienne→Stoneheart over the Sack-of-KL double-dip.

## STEP 1 — run the proven S133–S140 machine (if a dip is picked)
Dump the cluster (`graph-query.py --neighbors / --full-chain / --container`) → `working/enrichment/<unit>/baseline.md`
→ fan out **4 fresh Sonnet lenses** PROPOSE-only: (1) downstream-causal/consequence · (2) secondary-character
sub-arcs + SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node
causal-wiring** (the cross-arc seam lens — ALWAYS include, standing policy S134).
**Paste into every lens:** the locked vocab (170 types, `grep -oE '^\| \`[A-Z_]+\`' reference/architecture.md`),
the **line-check rule** (every quote a VERBATIM CONTIGUOUS span incl. internal dialogue quote marks; never splice
across a `," said X, "` attribution; exact begin-line number), the agency rules (NO CAUSES between sibling/
constitutive beats; MOTIVATES→character only; ENABLES=door-opener), and **SPLIT THE BAR** (tight edge bar;
WIDE-OPEN harvest — EVERY meal/food/drink incl. the grim/starvation register, plus descriptions/quotes/
foreshadowing as `chapter:line / kind / note` pointers into `working/harvest-queue.md`).

Then: Opus synthesizes + **line-checks every quote against the files via grep** (the recurring catch — always
grep the anchor phrase to confirm chapter:line before minting; S140 overrode a SUSPECTED_OF→COMMANDS_IN on a
POV-confirmed agency, and dropped 3 already-in-graph dups — always dedup new edges against edges.jsonl) → mint
via `scripts/mint_<unit>_enrichment_s141.py` (copy `scripts/mint_cersei_downfall_enrichment_s140.py` as the
template; `mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard, NEW_NODE_SLUGS excluded from
precheck, optional `qualifier` field) → `python3 scripts/verify-edge-quotes.py --run-id <id>` (0 drift) →
flip `verified_by` pending→confirmed on confirmed interpretive edges → `bash scripts/weirwood-refresh.sh` only
IF new nodes minted → **independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — agency-
collapse, temporal inversion, incidental-co-location ENABLES, mistargets/wrong-book, WITNESS text-anchor,
SUSPECTED overclaim, over-read of unconfirmed facts) → `--full-chain` smoke → push harvest rows into
`working/harvest-queue.md` → increment the ledger + Session-141 worklog entry. **Check first-use edge types
against the in-use count** (report which types are newly activated, e.g. S140 first-used FORESHADOWS+INFORMS).

## Read first
- `working/arc-enrichment-backlog.md` (the ledger + the "scope model" top section + the character/event seeds)
- `scripts/mint_cersei_downfall_enrichment_s140.py` (the mint template) + memory `project_arc_enrichment_track`
- `worklog.md` Session 140 entry (the most recent dip — the machine in action)

## STEP 2 (if planning session instead) — scope the L2-granular dip list
Produce a ranked, scoped list of granular sub-plot + event-unit + character dips (the seeds in the backlog's
"Next-pass scope" sections become the input). For each: what's already built (by-product of the arc passes),
what's missing, rough mint size, and the dependency order. Output to `working/arc-enrichment-backlog.md` (extend
the ledger) or a dedicated `working/l2-granular-plan.md`. No minting — this is a planning deliverable.

## DO NOT
mass-mint · CAUSES between sibling/constitutive beats (agency-collapse) · assert facts the chapter leaves
unconfirmed (S139 dropped `oberyn POISONS gregor`; S140 used COMMANDS_IN only because Cersei's POV confirmed it) ·
launch the PARKED graph-wide causal track · pull TWOW/gated-theory READINGS into the causal map · run extractions
without asking · `/endsession` without permission · un-park D&E · `git add -A`.

## Parked harvest rows (5 NEW S140 + the older parks; if a future harvest/dip wants them)
S140 parked: `aurane-waters-deserts-with-the-fleet` node (affc-cersei-10:303); `kevan-assumes-the-regency`
(ADWD completion); `creation-of-robert-strong` event + the Mountain-to-Qyburn cite (Robert-Strong/Gregor
character unit); the Gardener-coin clue-prop. Plus the older S139/S138 parks (ship-roster Python batch, the
Kettleblack cross-identity web, the Ashara-Harrenhal seam, the Antler Men wiring).
