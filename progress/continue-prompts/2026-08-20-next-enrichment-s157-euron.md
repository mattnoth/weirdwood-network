# SESSION 157 — A-arc roundup #3: A1.6 Kingsmoot / Euron enrichment

> **This is Session 157.** Stamp your worklog entry `### Session 157` in `worklog.md` (GRAPH track, global S-number).
> **Recommended model:** Sonnet 4.6 for the lens subagents + fresh-verify; Opus 4.8 for orchestration/synthesis.
> **One enrichment dip per session** (Matt S131). **D&E Pass-1 is PARKED** — stage only your own files by path; never `git add -A`.
> **`/endsession` is PRE-AUTHORIZED for an enrichment dip** (Matt S142/S144; step 6 of the machine). OFFER it, don't auto-run.

## The unit is LOCKED — no STEP-0 fork this session
Matt directed (S154): **round up the remaining A arcs** as a multi-session campaign. **S155 Stannis + S156 Dorne shipped.**
Per the order, **S157 = A1.6 Kingsmoot / Euron.** So **do NOT surface a fork** — go straight to baselining Euron and running
the machine. (The A-roundup order after this: A2.6 Jaime/Riverlands → A2.4 Tyrion-Essos → A2.5 WO5K-battles [LAST,
multi-pass] → A2.8 Davos/Sam residual. Full plan: `working/enrichment-coverage-plan.md` § A1.6 + the 🅰 banner.)

## Where we are
**20 major-arc enrichment dips done** (through S156 Dorne). Edges **23,132**, nodes **8,689**. Ledger + the machine:
`working/arc-enrichment-backlog.md`. The exemplar to copy this session: **`working/enrichment/dorne/`** (S156 — baseline +
baseline_pull.py + LENS-SHARED + 4 lens files + candidates.json + quotecheck.py + fresh-verify.md + the mint/finalize pair).

## A1.6 Euron — scope (spine + 1 early enrichment S116; DEDUP HEAVY)
Unlike the other A1s, the Kingsmoot/Euron arc already had a spine **+ one early enrichment** (S116, pre-formal-L1) **+ a
remainder wire** (S132 Victarion voyage, `[essos]`-tagged). So this is **WIRE+ENRICH with a heavy dedup** — much of the
kingsmoot is built. **BASELINE FIRST** to see exactly what exists (the death-of-balon → euron-seizes-the-seastone-chair →
kingsmoot-on-old-wyk → taking-of-the-shields spine; `euron-greyjoy SUSPECTED_OF death-of-balon-greyjoy`; the 3 S116 bridge
nodes [asha-proxy-marriage, euron-commissions-victarion, euron-hunts-aeron]; the S132 voyage cluster). The dip's value:
- **Euron's expansion / the Shield Islands** (`taking-of-the-shields` built — enrich the participants + the Reach-raiding).
- **The Reader** (Rodrik Harlaw — Asha's uncle/ally; the bookish lord) + the Harlaw faction.
- **Dragonbinder / the dragon-horn** (`dragonbinder` exists, WIELDED_IN the S132 voyage-reveal): the theft-from-Valyria
  narrative Euron tells, the hellhorn lore — **the Joramun/Valyria provenance stays node-prose/gated.**
- **The Crow's-Eye backstory** (the warlock-killing / the mutes / the dusky woman / the Silence's stitched-mute crew /
  Euron's exile by Balon — `euron BANISHES`-class already? check) — mostly node-prose + light role edges.
- **The Aeron/Euron rupture** (Aeron's flashbacks; Euron's blasphemy) — **published only.** **The Forsaken (Aeron Euron's
  prisoner) is TWOW — DO NOT use it.**
- **Cross-arc seams (lens 4):** Iron-Islands ↔ the Reach (taking-of-the-shields → Mander-raiding preoccupies Highgarden,
  a real WO5K-board seam Obara names in adwd-the-watcher) ; Euron ↔ Daenerys (the Victarion-fetch-Dany commission, S116/
  S132 — dedup); Euron ↔ AEGON board.

**Source chapters** (AFFC Iron Islands — map exact filenames in the baseline): `affc-the-prophet-01` (Aeron, opens the Iron
Islands), `affc-the-kraken-s-daughter-01` (Asha), `affc-the-reaver-01` + `affc-the-iron-captain-01` (Victarion), `affc-the-drowned-man-01`
(Aeron — **the kingsmoot itself**, Euron crowned). **Baseline FIRST** — `--neighbors euron-greyjoy` / `victarion-greyjoy` /
`aeron-greyjoy` / `asha-greyjoy` / the kingsmoot + voyage hubs + a dedup pull of existing internal edges in the core node-set
(the S116 + S132 work means a big chunk is wired — expect the dedup to kill several lens proposals).

## The machine (proven 20×; see `working/arc-enrichment-backlog.md` § "The enrichment-pass machine")
1. **Baseline dump** — `graph-query.py --neighbors`/`--full-chain` of the Euron/Kingsmoot core + a **dedup pull of all existing
   internal edges** (small Python pull modeled on `working/enrichment/dorne/baseline_pull.py`; dedup BEFORE proposing). Write
   `working/enrichment/euron/baseline.md`. Load locked vocab from `working/wiki/data/edge-type-counts.json` (170 types).
   edges.jsonl uses `edge_type`/`source_slug`/`target_slug`.
2. **Fan out 4 fresh Sonnet lenses** PROPOSE-don't-mint + dedup every node/edge: (a) spine + secondary-character sub-arcs
   (Victarion, Asha, Aeron, the Reader), (b) whodunit/hidden-agency + SUSPECTED_OF (Euron's kinslaying/manipulation — the
   Balon-death suspicion is built; look for the Damphair/blasphemy + the dusky-woman + the warlock/Pyat-Pree-class), (c)
   descriptive/quote/object depth (the Silence + the stitched-mute crew, Dragonbinder/the hellhorn, Euron's blue smiling lips
   & eyepatch, the Seastone Chair, the Iron Islands' bleak register), (d) **existing-node↔existing-node causal wiring** (the
   Reach-raiding seam, the Victarion-fetch-Dany dedup). Reuse the LENS-SHARED template from `working/enrichment/dorne/LENS-SHARED.md`
   (adapt the unit + chapters). Paste the canonical vocab terms + the locked 170-type list + the harvest snippet (split-the-bar
   WIDE on food incl. the Ironborn register — salt cod, the drowned-god feast, finger dancing, the bleak fare).
3. **Synthesize + decide** (Opus). Encode as `candidates.json` (schema = `scripts/mint_dorne_enrichment_s156.py`). **Whole-file
   line-check every quote** (`quotecheck.py`; the mint re-greps via norm()). **Qualifier rule (validator-enforced):** Tier-1
   types (MANIPULATES/WARD_OF/SIBLING_OF/SPOUSE_OF/PARENT_OF/HOLDS_TITLE/VOWS_TO/SWORN_TO) REQUIRE an enum-valid `qualifier`;
   Tier-3 must NOT; event-role + causal types take none. Mint via `scripts/mint_euron_enrichment_s157.py` (re-greps, backup +
   re-run guard + `mint_arc_lib.precheck_slugs`). Aliases = natural SPACED phrases.
4. **Independent Sonnet fresh-verify** the interpretive/causal + borderline edges (vs LOCAL cache). Apply drops/adjusts via
   `finalize_euron_s157.py` (+ stamp `verified_by`). Re-run `scripts/verify-edge-quotes.py --run-id`. **Node-adding dips need
   `bash scripts/weirwood-refresh.sh`.** Smoke `--full-chain`/`--neighbors`.
5. **Consume harvest inline** (marquee quotes → new node `## Quotes`; food/description rows → `working/harvest-queue.md`, table
   `| status | kind | book | chapter:line | note | source-dip |`, source-dip = `S157 euron`).
6. **Close out — OFFER `/endsession`** (pre-authorized; don't auto-run without Matt's nod). Set the next live prompt to the
   next A-roundup unit (**A2.6 Jaime / Riverlands**).

## DO NOT
run extractions without asking · un-park D&E · `git add -A` (stage your own files by path) · **assert theory readings (GATED):**
the Euron↔Bloodraven thread / the Dragonbinder-is-the-Horn-of-Joramun reading / the dusky-woman-is-X / the Euron-as-eldritch-
herald reading — evidence/possession edges only, the readings stay node-prose · use **TWOW** material (The Forsaken — Aeron as
Euron's prisoner — is unpublished; only the 5 books) · claim "first-use" without grepping edges.jsonl · over-mint speculative
seam edges (node-prose when unsure) · re-mint the S116 kingsmoot spine / the 3 S116 bridge nodes / the S132 voyage cluster
(DEDUP against the baseline) · use a container tag outside the approved 5 (essos/wo5k/north/aegon/bran) — **Iron-Islands is NOT
an approved container; default NO container tag** (the S132 voyage beats are `[essos]` because the fleet sails to Slaver's Bay,
NOT because Iron-Islands is a container).

## Read first
- `working/enrichment-coverage-plan.md` (§ A1.6 + the 🅰 A-roundup banner) · `working/arc-enrichment-backlog.md` (ledger — 20
  dips + the machine + the scope model) · `working/enrichment/dorne/` (S156 exemplar: baseline_pull + LENS-SHARED + candidates.json
  + quotecheck + mint/finalize pattern)
- `worklog.md` S156 entry + the STATUS block · memory `project_arc_enrichment_track`, `feedback_enrichment_board_causal_lens`
  (the 4th causal-wiring lens), `project_theories_track_deferred` (the gating)
- **Carried small-fix flags (NOT this dip):** the Harrenhal node-tangle alias-hygiene (S154); the House-of-Black-and-White node
  mis-type; the `fight-at-the-fist`/`battle-of-the-fist-of-the-first-men` dup-merge. → `working/todos.md` § Small Fixes.
