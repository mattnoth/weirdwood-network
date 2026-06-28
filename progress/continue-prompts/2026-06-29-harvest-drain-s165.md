# SESSION 165 — Harvest-queue drain (the S152/S157 disjoint-dir parallel-attacher machine)

> **This is Session 165.** Stamp your worklog entry `### Session 165` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Opus 4.8 for orchestration/routing/central-flip; Sonnet 4.6 for the parallel attacher subagents + the fresh-verify sample.
> **One live continue prompt** (Matt). This drain is the live track; **A2.5 WO5K-battles PASS 3** is the documented step-after (set it live at close-out).
> **`/endsession`: a harvest-drain is a MAINTENANCE pass, NOT an enrichment dip — the enrichment auto-run bypass does NOT apply. ASK Matt before running `/endsession`** (`feedback_endsession_requires_permission`).

## Why now
The S163 (WO5K PASS 1) + S164 (WO5K PASS 2) dips refilled `working/harvest-queue.md` to **35 open rows** (`grep -c '^| open ' working/harvest-queue.md`), crossing the ~30 auto-drain bar (endsession step 0). This is the dedicated drain.

## The machine (proven S110/S118/S120/S125/S139/S152/S162 — read the S152 + S139 ledger rows in `working/todos.md` § "Harvest pass")
1. **Extract + route (Python + Opus).** Read all `^| open ` rows. Route each to ONE owner by its eventual graph home, so attachers write to **DISJOINT node dirs** (zero write-collision):
   - **FOODS** owner → `graph/nodes/foods/` (`object.food` nodes; dedup vs existing — ale/wine/cheese/dreamwine/milk-of-the-poppy etc. likely EXIST → add book-cite or dedup-out; mint new only when genuinely absent).
   - **CHARACTERS** owner → `graph/nodes/characters/` (`## Description` appearance + `## Quotes` for character-targeted rows: robb-stark, jeyne-westerling, rolph-spicer, brynden-tully, catelyn-stark, tyrion-lannister, theon-greyjoy, tytos-blackwood, hoster-tully).
   - **EVENTS** owner → `graph/nodes/events/` (`## Quotes` on event nodes: robb-weds-jeyne-westerling, battle-in-the-whispering-wood, etc. — NOTE battle-of-oxcross + storming-of-the-crag ALREADY got S164 book-cite overlays; dedup).
   - **LOCATIONS** owner → `graph/nodes/locations/` (`## Description` on place nodes: the-twins, godswood-of-riverrun) + **HOUSES** heraldry rows (house-westerling/house-spicer sigils).
   - **DEFER (do NOT attach — keep `open` or mark a `parked` status):** the foreshadowing / plot-reveal / PASS-3 / theory-gated rows (e.g. asos-catelyn-02:189 Grey-Wind-distrusts-Rolph = PASS-3; agot-catelyn-09:211 Jon-Arryn-foster reveal = theory; agot-catelyn-09:241 Frey-pact = RW-upstream). These are forward-pointers, not attachable now. Park them with a one-line reason; they get consumed when their target arc is built.
2. **Line-check at attach.** Each attacher RE-READS the cited `chapter:line` before attaching (queue cite-drift is common — S152/S139/S120 each caught several; S164 already caught one drift, acok-catelyn-07:15). Fix the cite in the row if drifted.
3. **Parallel Sonnet attachers, one per disjoint dir.** Each owns its dir ONLY, attaches its rows, and reports back (a) what it attached/minted, (b) which row line-numbers are now `done`, (c) any it parked + why. Attachers do NOT edit `working/harvest-queue.md` (avoids the central write-conflict).
4. **Fresh-verify a stratified sample** (independent Sonnet, ~10–15 rows across owners) vs the LOCAL book/wiki cache — verbatim quote + correct home + no dup. Fix any issues.
5. **Central flip (orchestrator).** Flip the attached rows `open → done` in `working/harvest-queue.md` in ONE pass (Opus owns the queue file). Park the deferred rows. Confirm `grep -c '^| open '` ≈ 0 (only true deferrals remain).
6. **Rebuild derived artifacts IF nodes were added** — new `object.food` nodes need `bash scripts/weirwood-refresh.sh` (rebuilds indexes + alias resolver) so they're discoverable (memory `project_rebuild_derived_artifacts_after_node_mutation`). Edge/quote/description-only changes do NOT.

## Scope notes
- The 35 rows: ~10 quote / 8 food / 7 description / 4 appearance / 2 place / 2 foreshadowing / 1 plot-reveal / 1 hospitality. found-during stamps: `S163 wo5k-battles` (20) + `S164 wo5k-battles-pass2` (15).
- Mint `object.food` nodes per the architecture `object.food` schema (regions/ingredients/culture); book-citation overlay = high value (memory `feedback_book_citation_overlay_value`).
- `## Description` / `## Quotes` appends onto existing nodes are the bulk of the work; dedup before appending.

## DO NOT
re-fetch the wiki · run extractions · un-park D&E · `git add -A` (stage by path) · attach the deferred foreshadowing/theory/PASS-3 rows · re-overlay the battle-of-oxcross / storming-of-the-crag quotes (S164 already did them) · auto-run `/endsession` (ASK — not an enrichment dip).

## Read first
- `working/todos.md` § "Harvest pass — consume `working/harvest-queue.md`" (the S152 + S139 + S162 ledger rows = the exact machine + the disjoint-dir owner split) · `working/harvest-queue.md` header (row-status values, the line-check rule) · `working/arc-enrichment-backlog.md` harvest section · memory `feedback_harvest_queue`, `feedback_capture_quotes_during_research`, `feedback_book_citation_overlay_value`, `project_rebuild_derived_artifacts_after_node_mutation`.
- After the drain → set the next live prompt to **A2.5 WO5K-battles PASS 3** (the Fords / Duskendale → RW-upstream; the prior session's Lens B logged a 7-edge Spicer-betrayal thread list in `working/enrichment/wo5k-battles-pass2/lens-B.md` § "PASS-3 thread list" — fold it in). Then **A2.8 Davos/Sam residual** closes the A-roundup.
