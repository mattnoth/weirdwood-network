# SESSION 155 — A-arc roundup #1: A2.7 Stannis enrichment (build+enrich)

> **This is Session 155.** Stamp your worklog entry `### Session 155` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 6 of the machine). OFFER it, don't auto-run.

## The unit is LOCKED — no STEP-0 fork this session
Matt directed (S154): **round up the remaining A arcs** as a multi-session campaign, **starting with A2.7 Stannis.**
So **do NOT surface a fork** — go straight to baselining Stannis and running the machine. (The A-roundup order for
later sessions: A1.5 Dorne → A1.6 Euron → A2.6 Jaime/Riverlands → A2.4 Tyrion-Essos → A2.5 WO5K-battles [LAST,
multi-pass] → A2.8 Davos/Sam residual. Full plan: `working/enrichment-coverage-plan.md` § the 🅰 banner + § A2.)

## Where we are
**18 major-arc enrichment dips done.** The reopened L1 round closed (Dany/Jon/Bran/AEGON S144–S147); the three A2
cross-identity build+enrich arcs shipped (Sansa/Theon/Arya S148–S150); the cheap L2 round (S151) + the dedicated
harvest pass (S152) ran; **D1 Battle of Castle Black (S153)** and **D5 Arya/Harrenhal (S154)** were the two Class-D
event clusters. Edges **23,065**, events/ 726. Ledger + the machine: `working/arc-enrichment-backlog.md`.

## A2.7 Stannis — scope (build+enrich, but CHEAPER than the label)
Much of Stannis is **already wired** via the Blackwater (S138) and NORTH (S125–126) spines — so this is WIRE +
ENRICH more than a from-scratch build. Stannis is **not a POV**; his arc lives across other POVs/containers, so
**baseline carefully** (he has a large dyadic web already). The dip's value = the **MOTIVATES/causal substrate** the
spine lacks:
- **Dragonstone self-isolation** → the R'hllor conversion / Melisandre's arrival; `stannis SUBMITS/PRACTICES`-class
  relationships (use the locked vocab — likely `WORSHIPS r'hllor`, `melisandre ADVISES/MANIPULATES stannis`).
- **Renly's war + the shadow-baby:** the `shadow-assassination-of-renly` node exists (built) — wire its agency
  (melisandre AGENT_IN / SACRIFICES?, stannis COMMANDS_IN/SUSPECTED_OF — check what's already there first) and the
  **Renly-kinslaying MOTIVATES stannis** substrate (guilt thread). The Catelyn/Brienne witness layer.
- **Blackwater:** mostly built (S138) — only add un-wired Stannis-side beats (his refusal to retreat, the chain).
- **The Wall + the march:** built via NORTH (Stannis-saves-the-Wall, the march on Winterfell, Crofter's Village) —
  add the MOTIVATES (why Stannis goes north — Davos's "save the realm to win the throne" argument; the Pink Letter
  is Jon's, not Stannis's). The Mance-glamour / Rattleshirt thread is S145 (Jon/Wall) — don't re-touch.
- **Cross-arc seams (lens 4):** Stannis ↔ Robert's Rebellion (the Storm's End siege/onions backstory → Davos);
  Stannis ↔ the Iron Throne claim (the twincest revelation he learned from Jon Arryn/Stannis's letters).

**Source chapters** (spread — map them in the baseline): acok-davos-01..03, asos-davos-01..06, adwd-davos-01..04
(Stannis's arc via Davos); acok-catelyn (the shadow-baby/Renly's death is Catelyn's POV — find the right chapter);
the adwd Melisandre chapter; Jon's adwd Wall chapters for the march context. **Baseline FIRST** — check
`--neighbors stannis-baratheon`, `--neighbors shadow-assassination-of-renly`, `--neighbors melisandre`, and a
dedup pull of existing edges in the core node-set before proposing (Stannis is heavily pre-wired — expect the dedup
to kill many lens proposals).

## The machine (proven 18×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--full-chain` of Stannis + the satellite event nodes + a dedup
   pull of all existing edges within the core node-set (small Python pull; dedup BEFORE proposing). Write
   `working/enrichment/stannis/baseline.md`. Load locked vocab from `working/wiki/data/edge-type-counts.json` (170
   types; `type_counts` key). edges.jsonl uses `edge_type`/`source_slug`/`target_slug`.
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup every node/edge: (a) spine + secondary-character
   sub-arcs, (b) whodunit/revelation + SUSPECTED_OF (the shadow-baby agency; Renly's death), (c) descriptive/quote/
   object depth (Lightbringer, the chain, the nightfires; Dragonstone), (d) **existing-node↔existing-node causal
   wiring** (cross-container seams — the standing 4th lens). Paste the canonical vocab terms (Pass/Track/Tier/
   lowercase-step; Tier=confidence 1–5 only) + the locked 170-type list + the harvest snippet (split-the-bar
   WIDE-OPEN on food incl. the grim register — Dragonstone's leeches, the burning sacrifices). Reuse the LENS-SHARED
   template from `working/enrichment/d5-arya-harrenhal/LENS-SHARED.md` (adapt the unit + chapters).
3. **Synthesize + decide** (Opus). Encode as `candidates.json` (schema = `scripts/mint_d5_arya_harrenhal_enrichment_s154.py`
   — edges array; node bodies in the mint script). **Whole-file line-check every quote** (the mint re-greps via
   norm()). **Qualifier rule (validator-enforced):** Tier-1 types (MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/PARENT_OF/
   HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid `qualifier` (`reference/edge-qualifier-vocab.md`); Tier-3 must
   NOT; event-role + causal types take none. Mint via `scripts/mint_stannis_enrichment_s155.py` (re-greps, backup +
   re-run guard + `mint_arc_lib.precheck_slugs`). Aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal + borderline edges (vs LOCAL cache). Apply drops/
   adjusts via `finalize_stannis_s155.py` (+ stamp `verified_by`). Re-run `scripts/verify-edge-quotes.py --run-id`.
   **Node-adding dips need `bash scripts/weirwood-refresh.sh`.** Smoke `--full-chain`/`--container`.
5. **Consume harvest inline** (marquee quotes → new node `## Quotes`; food/description rows → `working/harvest-queue.md`,
   table `| status | kind | book | chapter:line | note | source-dip |`).
6. **Close out — OFFER `/endsession`** (pre-authorized; don't auto-run without Matt's nod). Set the next live prompt
   to the next A-roundup unit (**A1.5 Dorne** — or pair Dorne+Euron if Matt OKs the relaxation).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · **assert theory readings
(GATED):** Azor Ahai / Stannis-as-the-prince-that-was-promised / R'hllor cosmology / the king's-blood magic mechanics
/ Shireen-as-future-sacrifice — evidence/possession edges only, the prophecy READING stays gated · claim "first-use"
without grepping edges.jsonl · over-mint speculative seam edges (node-prose when unsure) · re-touch the NORTH-spine
Mance-glamour thread (S145) or the Blackwater wildfire (S138) · use a container tag outside the approved 5
(essos/wo5k/north/aegon/bran) — Stannis nodes spread across containers; tag only when the node clearly belongs to one.

## Read first
- `working/enrichment-coverage-plan.md` (the 🅰 A-roundup banner + § A2.7 Stannis) · `working/arc-enrichment-backlog.md`
  (ledger — 18 dips + the machine + the scope model) · `working/enrichment/d5-arya-harrenhal/` (S154 exemplar: baseline +
  LENS-SHARED + candidates.json + mint/finalize pattern)
- `worklog.md` S154 entry + the STATUS block · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens`
  (the 4th causal-wiring lens), `project_theories_track_deferred` (the gating)
- **Carried small-fix flags (NOT this dip):** the Harrenhal node-tangle alias-hygiene (S154); the House-of-Black-and-White
  node mis-type; the `fight-at-the-fist`/`battle-of-the-fist-of-the-first-men` dup-merge. → `working/todos.md` § Small Fixes.
