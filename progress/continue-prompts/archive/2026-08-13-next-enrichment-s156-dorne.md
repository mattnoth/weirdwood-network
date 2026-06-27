# SESSION 156 — A-arc roundup #2: A1.5 Dorne / Queenmaker enrichment

> **This is Session 156.** Stamp your worklog entry `### Session 156` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 6 of the machine). OFFER it, don't auto-run.

## The unit is LOCKED — no STEP-0 fork this session
Matt directed (S154): **round up the remaining A arcs** as a multi-session campaign. **S155 Stannis shipped** (the first
A-roundup dip). Per the order, **S156 = A1.5 Dorne / Queenmaker.** So **do NOT surface a fork** — go straight to baselining
Dorne and running the machine. (The A-roundup order after this: A1.6 Euron → A2.6 Jaime/Riverlands → A2.4 Tyrion-Essos →
A2.5 WO5K-battles [LAST, multi-pass] → A2.8 Davos/Sam residual. Full plan: `working/enrichment-coverage-plan.md` § A1.5 + the 🅰 banner.)

## Where we are
**19 major-arc enrichment dips done** (through S155 Stannis). Edges **23,096**, events/ **729**. Ledger + the machine:
`working/arc-enrichment-backlog.md`. The exemplar to copy this session: **`working/enrichment/stannis/`** (S155 — baseline +
baseline_pull.py + LENS-SHARED + 4 lens files + candidates.json + quotecheck.py + fresh-verify.md + the mint/finalize pair).

## A1.5 Dorne — scope (spine built S117, 0 dips; the whodunit/informer wheelhouse)
The Dorne spine was built S117 (the Queenmaker plot) and **19 harvest rows were already pushed** then — but **0 enrichment
dips**. This is squarely our whodunit/participant wheelhouse. Expect (BASELINE FIRST to confirm) a thin causal spine + an
under-wired conspirator web. The dip's value:
- **The Queenmaker plot** (Arianne's plot to crown Myrcella): wire the conspiracy hub + the participant agency (Arianne
  AGENT_IN; Arys Oakheart, Drey, Garin, Sylva, Spotted Sylva, Darkstar as CONSPIRES_WITH / AGENT_IN / MEMBER_OF).
- **The "someone always tells" informer mystery** (the marquee whodunit): who betrayed the plot to Doran? (Text leaves it
  pointed-but-unproven → `SUSPECTED_OF`-class; the reveal is the Sand-Snakes/Arianne misdirection. Check what the text actually
  proves before asserting an informer.)
- **Arys Oakheart's seduction → his death** (the soiled knight; Arianne SEDUCES/MANIPULATES; his suicide-by-charge when the
  plot collapses; Hotah KILLS arys). **Myrcella maimed by Darkstar** (`myrcella-is-maimed-by-darkstar` may already exist from
  S117 — DEDUP; arianne WITNESS_IN already minted S117 — confirm, don't re-mint).
- **The conspirator dispersal** (the downstream-dark terminus): Drey→Norvos, Garin→Tyrosh, Sylva married off to Greenstone,
  Darkstar's escape. Mostly node-prose / light role edges.
- **Cross-arc seams (lens 4):** Dorne ↔ the Iron Throne (Myrcella's claim under Dornish law); Dorne ↔ AEGON (Doran's "fire and
  blood" pact / Quentyn-to-Dany — `murder-of-elia MOTIVATES doran` may already exist from S139/S142 — DEDUP). Doran's long-game
  patience MOTIVATES substrate.

**Source chapters** (AFFC Dorne — map exact filenames in the baseline): the Areo Hotah "Captain of Guards" opener, the Arys
Oakheart "Soiled Knight", the Arianne "Queenmaker", the Arianne "Princess in the Tower"; + the ADWD Areo "The Watcher"
(Myrcella-maimed reveal / Doran's reveal). **Baseline FIRST** — `--neighbors arianne-martell` / `doran-martell` /
`arys-oakheart` / the Queenmaker hub + a dedup pull of existing internal edges in the core node-set (the S117 spine + the
19-harvest residue means a chunk is already wired — expect the dedup to kill several lens proposals).

## The machine (proven 19×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--full-chain` of the Dorne core (Arianne, Doran, Arys, the Queenmaker
   hub, the Sand Snakes, Darkstar, Myrcella, Hotah) + a **dedup pull of all existing internal edges** in the core node-set
   (small Python pull modeled on `working/enrichment/stannis/baseline_pull.py`; dedup BEFORE proposing). Write
   `working/enrichment/dorne/baseline.md`. Load locked vocab from `working/wiki/data/edge-type-counts.json` (170 types;
   `type_counts` key). edges.jsonl uses `edge_type`/`source_slug`/`target_slug`.
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup every node/edge: (a) spine + secondary-character sub-arcs,
   (b) **whodunit/informer + SUSPECTED_OF** (the "someone always tells" mystery — the marquee lens for Dorne), (c) descriptive/
   quote/object depth (the Water Gardens, the Old Palace, Darkstar, the spear-and-sun, Dornish food/wine), (d) **existing-node↔
   existing-node causal wiring** (cross-container seams — Dorne↔Iron-Throne, Dorne↔AEGON). Reuse the LENS-SHARED template from
   `working/enrichment/stannis/LENS-SHARED.md` (adapt the unit + chapters). Paste the canonical vocab terms (Pass/Track/Tier/
   lowercase-step; Tier=confidence 1–5 only) + the locked 170-type list + the harvest snippet (split-the-bar WIDE-OPEN on food
   incl. the Dornish register — blood oranges, the Water Gardens, snake-and-scorpion venom, the unsullied-of-the-table).
3. **Synthesize + decide** (Opus). Encode as `candidates.json` (schema = `scripts/mint_stannis_enrichment_s155.py` — edges
   array; node bodies in the mint script). **Whole-file line-check every quote** (write a `quotecheck.py` like S155's; the mint
   re-greps via norm()). **Qualifier rule (validator-enforced):** Tier-1 types (MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/
   PARENT_OF/HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid `qualifier` (`reference/edge-qualifier-vocab.md`); Tier-3 must
   NOT; event-role + causal types take none. Mint via `scripts/mint_dorne_enrichment_s156.py` (re-greps, backup + re-run guard
   + `mint_arc_lib.precheck_slugs`). Aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal + borderline edges (vs LOCAL cache). Apply drops/adjusts via
   `finalize_dorne_s156.py` (+ stamp `verified_by`). Re-run `scripts/verify-edge-quotes.py --run-id`. **Node-adding dips need
   `bash scripts/weirwood-refresh.sh`.** Smoke `--full-chain`/`--neighbors`.
5. **Consume harvest inline** (marquee quotes → new node `## Quotes`; food/description rows → `working/harvest-queue.md`, table
   `| status | kind | book | chapter:line | note | source-dip |`, source-dip = `S156 dorne`).
6. **Close out — OFFER `/endsession`** (pre-authorized; don't auto-run without Matt's nod). Set the next live prompt to the
   next A-roundup unit (**A1.6 Euron**).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · **assert theory readings (GATED):**
the Aegon-is-real/fAegon question / the full "fire and blood" Dornish-vengeance prophecy reading / any R+L-adjacent Elia/Rhaegar
theory — evidence/possession edges only, the readings stay gated · claim "first-use" without grepping edges.jsonl · over-mint
speculative seam edges (node-prose when unsure) · re-mint the S117 Queenmaker spine or `myrcella-is-maimed-by-darkstar` /
`arianne WITNESS_IN` if they already exist (DEDUP against the baseline) · use a container tag outside the approved 5
(essos/wo5k/north/aegon/bran) — **Dorne is NOT one of the approved containers; default NO container tag** (like the S148–S155
arcs).

## Read first
- `working/enrichment-coverage-plan.md` (§ A1.5 Dorne + the 🅰 A-roundup banner) · `working/arc-enrichment-backlog.md` (ledger —
  19 dips + the machine + the scope model) · `working/enrichment/stannis/` (S155 exemplar: baseline_pull + LENS-SHARED +
  candidates.json + quotecheck + mint/finalize pattern)
- `worklog.md` S155 entry + the STATUS block · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens`
  (the 4th causal-wiring lens), `project_theories_track_deferred` (the gating)
- **Carried small-fix flags (NOT this dip):** the Harrenhal node-tangle alias-hygiene (S154); the House-of-Black-and-White node
  mis-type; the `fight-at-the-fist`/`battle-of-the-fist-of-the-first-men` dup-merge. → `working/todos.md` § Small Fixes.
