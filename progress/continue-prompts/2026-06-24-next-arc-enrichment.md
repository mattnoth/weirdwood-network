# SESSION 139 — Enrichment: next dip (board-pick the arc first)
> **This is Session 139.** Stamp your worklog entry `### Session 139` at endsession (in `worklog.md` — graph track).
> **Recommended model:** Sonnet 4.6 lenses/verify + Opus 4.8 orchestrator (same machine as S133–S138).
> **D&E Pass-1 is PARKED** (Matt). Stage only your own files by explicit path; never `git add -A`.

## Where we are
The enrichment phase is the primary track, descending major arcs → sub-plots → characters. **Five major-arc dips shipped: RR (S133) · Red Wedding (S134) · Purple Wedding (S135) · Ned's Downfall (S137) · Blackwater (S138).** All 5 approved containers are spine-complete (essos/wo5k/north/aegon/bran).

## STEP 0 — pick the next unit (this dip has NO pre-picked target)
Unlike S137/S138 (board pre-picked), there is **no target chosen**. Two forks — surface both to Matt, recommend the first:
1. **Continue the L1 major-arc descent.** Remaining L1 arcs: **Tywin's death** (has an S109 spine — could enrich directly), **Sack of KL** (FLAGGED a double-dip — its core was wired in the S133 RR pass; check before picking), **Cersei's downfall** (S114 spine), **Brienne→Stoneheart** (S115 spine). Run a quick 3-advisor board (saga-demand / graph-gaps / tractability) OR a demand-dip to pick — same as S135/S136. Note: some "remaining" arcs may need a spine-build before they're enrich-ready.
2. **The L2-granular planning session (Matt S130).** After the major-arc round, Matt wants a dedicated session to *enumerate + scope the granular sub-plot/character dip list* before diving into L2. If Matt judges the major-arc round "done enough," do this instead.

Recommend fork 1 (keep the arc momentum) unless Matt steers to the planning session. **Confirm the pick with Matt if ambiguous.**

## STEP 1 — run the proven S133–S138 machine (once the target is picked)
Dump the cluster (`graph-query.py --neighbors / --full-chain / --container`) → `baseline.md` → fan out **4 fresh Sonnet lenses** PROPOSE-only:
(1) downstream-causal/consequence · (2) secondary-character sub-arcs + SUSPECTED_OF/WITNESS substrate · (3) descriptive/quote/object depth · (4) **existing-node↔existing-node causal-wiring** (the cross-arc seam lens — ALWAYS include, standing policy S134).
**Paste into every lens:** the locked vocab (170 types, `grep -oE '^\| \`[A-Z_]+\`' reference/architecture.md`), the **line-check rule** (every quote a VERBATIM CONTIGUOUS span incl. internal dialogue quote marks; never splice across a `," said X, "` attribution; exact begin-line number), the agency rules (NO CAUSES between sibling/constitutive beats; MOTIVATES→character only; ENABLES=door-opener), and **SPLIT THE BAR** (tight edge bar; WIDE-OPEN harvest — capture EVERY meal/food/drink maximally incl. the grim/starvation register, plus descriptions/quotes/foreshadowing as `chapter:line / kind / note` pointers).

Then: Opus synthesizes + **line-checks every quote against the files** (the S123/S138 recurring catch: dialogue-attribution splices + off-by-N line refs — verify-edge-quotes will widen-match; fix the ref) → mint via `scripts/mint_<unit>_enrichment_s139.py` (copy `scripts/mint_blackwater_enrichment_s138.py` as the template; `mint_arc_lib.precheck_slugs`, backup to `_regrounding/`, re-run guard, NEW_NODE_SLUGS excluded from precheck) → `python3 scripts/verify-edge-quotes.py --run-id <id>` (0 drift) → `bash scripts/weirwood-refresh.sh` only IF new nodes minted → **independent fresh-verify** (a fresh Sonnet that did NOT propose; adversarial — agency-collapse, temporal inversion, incidental-co-location ENABLES, mistargets/wrong-book, WITNESS text-anchor, SUSPECTED overclaim; apply verdicts, flip `verified_by` pending→fresh) → `--full-chain` smoke → consume/append harvest rows to `working/harvest-queue.md` → increment the ledger + Session-139 worklog entry.

## Read first
- `working/arc-enrichment-backlog.md` (the ledger + the "scope model" top section — read it if "why event-arcs not containers?" confuses you)
- `scripts/mint_blackwater_enrichment_s138.py` (the mint template) + memory `project_arc_enrichment_track`
- `worklog.md` Session 138 entry (the most recent dip, for the machine in action)

## DO NOT
mass-mint · CAUSES between sibling/constitutive beats (agency-collapse) · launch the PARKED graph-wide causal track · pull TWOW/gated-theory READINGS into the causal map · scope a standalone "harvest every book" session (Matt never asked) · run extractions without asking · `/endsession` without permission · un-park D&E · `git add -A`.

## Blackwater (S138) pass-2 candidates (if a dip ever returns to it)
the Antler Men wiring (needs member nodes / clearer event model); `battle-of-oxcross`/`battle-of-the-fords ENABLES` the battle (WO5K-internal seams → WO5K enrichment); a `tyrion-loses-the-handship` node (Tywin/battle CAUSES it); the full named-ship WIELDED_IN roster (~20 ships in `acok-davos-03.md:47` — **deterministic Python batch**, not an LLM pass); the `Gentle Mother` `object.text` song node + a Sandor's-white-cloak artifact; the `joffrey-sets-sansa-aside → purple-wedding` seam (belongs in a Purple-Wedding pass-2).
