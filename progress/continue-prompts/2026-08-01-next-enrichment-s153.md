# SESSION 153 — Next enrichment dip (the A2/Class-D fork: a remaining A2 arc OR a big Class-D event cluster)

> **This is Session 153.** Stamp your worklog entry `### Session 153` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131; the S151 cheap-L2 batch was a one-time relaxation). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 6 of the machine). OFFER it, don't auto-run.

## Where we are
The reopened L1 round is COMPLETE (Dany S144 · Jon S145 · Bran S146 · AEGON S147); all three big build+enrich A2 arcs are done (Sansa/Vale S148 · Theon/Reek S149 · Arya/Braavos S150); the **cheap L2 round** (B1/B2/B3/B4/B7) shipped S151; and **the dedicated harvest pass DRAINED the queue S152** (225 open → 0; +5 food nodes / +4 edges → edges **22,988**, nodes **8,633**). The breadcrumb backlog is clear, so this session is back to a normal **one enrichment dip**. Full ranked plan + scope cards: `working/enrichment-coverage-plan.md`; ledger + the machine: `working/arc-enrichment-backlog.md`.

## STEP 0 — surface the fork to Matt (don't auto-pick)
Every dip S140–S151 surfaced the fork via AskUserQuestion at STEP 0. Do the same. With the A2 *cross-identity* arcs and the cheap-L2 round done, the fork is now **remaining A2 arcs** vs **the new Class-D event clusters** (Matt S151: *"some big event clusters not listed"*):
- **Class D — big current-narrative event clusters** (`enrichment-coverage-plan.md` § Class D; NOT yet density-baselined — baseline each before picking):
  - **D1 Battle of Castle Black** (ASOS) — the Wall defense (Mance's assault, the gate burning, Ygritte's death, Donal Noye, Stannis's relief). **Plan's top pick — highest salience; cross-cuts Jon + wildlings + Stannis; the *battle* no POV arc owns** (Jon/Wall S145 enriched leadership, not this battle).
  - **D5 Arya's AGOT→ACOK flight & Harrenhal** — Yoren's recruits, Needle's first kill, the capture, Harrenhal (the Tickler, weasel soup, Jaqen's three deaths, **the iron-coin's origin**), the Bloody Mummers. **Natural follow-on to S150** — it's the origin of the iron-coin seam the Arya/Braavos arc hangs off.
  - D2 Hand's Tourney (AGOT; Gregor/Sandor/Loras set-piece) · D3 Greyjoy's Rebellion (289 AC backstory hub) · D4 Riot of KL (ACOK) · D6 Rebellion prelude (theory-adjacent, gated).
- **Remaining A2 arcs (heavier build+enrich):** A2.4 Tyrion/ADWD-Essos journey · A2.5 WO5K battles (Whispering Wood/Camps/Oxcross/Fords — flagged "needs many passes") · A2.6 Jaime/Riverlands-command (AFFC) · A2.7 Stannis.
- **Recommendation:** surface D1 (highest salience) and D5 (S150 follow-on) as the strongest defaults, plus the A2 remainder; confirm the unit with Matt, then run the machine. Baseline the picked Class-D cluster's existing density FIRST (these aren't graph-verified).

## The machine (proven 17×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--full-chain`/`--container` of the unit's hub + satellites + **a dedup pull of all existing edges within the core node-set** (S149/S150 lesson: dedup BEFORE proposing). Write `working/enrichment/<unit>/baseline.md`. Load locked vocab from `working/wiki/data/edge-type-counts.md` (170 types; verify membership against the JSON list but DON'T claim "first-use" from the per-type counts — they're infobox-only; grep edges.jsonl to confirm). edges.jsonl uses `edge_type`/`source_slug`/`target_slug`.
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup every node/edge: (a) spine + secondary-character sub-arcs, (b) whodunit/revelation + SUSPECTED_OF, (c) descriptive/quote/object depth, (d) **existing-node↔existing-node causal-wiring** (cross-container seams — the 4th lens, standing since S133). Paste the canonical vocab terms (Pass/Track/Tier/lowercase-step; Tier=confidence 1–5 only) + the harvest snippet (split-the-bar WIDE-OPEN on food incl. the grim register) — subagents don't load CLAUDE.md.
3. **Synthesize + decide** (Opus). Encode as `candidates.json` (schema = `scripts/mint_arya_braavos_enrichment_s150.py`). **Whole-file line-check every quote** (the mint script re-greps; a quote must be a single contiguous substring, never spliced across a `," said X, "` attribution). **Qualifier rule (validator-enforced):** Tier-1 relationship types (MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/PARENT_OF/HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid `qualifier`; Tier-3 must NOT; Tier-2 optional; event-role + causal types take none. Mint via `scripts/mint_<unit>_enrichment_s153.py` (re-greps, backup + re-run guard + `mint_arc_lib.precheck_slugs`). Aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal edges + borderline mints (vs LOCAL cache). Apply drops/adjusts/retirements via `finalize_<unit>_s153.py` (+ stamp `verified_by`). Re-run `scripts/verify-edge-quotes.py --run-id <run>`. **Node-adding dips need `bash scripts/weirwood-refresh.sh`.** Smoke `--full-chain`/`--container`. A flagged-borderline edge that fresh-verify rejects → drop it (propose-then-gate).
5. **Consume harvest inline** (attach load-bearing quotes + book-cite overlays onto wiki nodes; push food/description breadcrumbs to `working/harvest-queue.md` — now at 0 open / 53 parked after S152).
6. **Close out — OFFER `/endsession`** (pre-authorized; don't auto-run without Matt's nod).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · assert theory readings (Robert-Strong=Gregor, gravedigger=Sandor, fAegon/Blackfyre, R+L, Azor Ahai, Faceless-Men cosmology — GATED, evidence edges only) · claim "first-use" without grepping edges.jsonl · over-mint speculative foreshadowing/seam edges (node-prose when unsure) · use a container tag outside the approved 5 (essos/wo5k/north/aegon/bran; A2/Class-D arcs that aren't in a container get none).

## Read first
- `working/enrichment-coverage-plan.md` (§ Class D candidates D1–D6 + § A2.4–A2.7) · `working/arc-enrichment-backlog.md` (ledger — 17 dips + the machine + the scope model)
- `worklog.md` S152 entry + the STATUS block · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens` (the 4th causal-wiring lens)
- **Out-of-harvest follow-up surfaced S152 (→ § Small Fixes, todos.md):** the House of Black and White node is mis-typed `organization.house` (filed under `houses/`) but is a TEMPLE (`place.location`) — a careful node re-type/re-file + index rebuild + edge-source update; NOT this dip.
