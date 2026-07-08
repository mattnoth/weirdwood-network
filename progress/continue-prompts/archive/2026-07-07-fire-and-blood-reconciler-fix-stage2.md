# SESSION 199 (continued) — Fire & Blood: Stage-2 smoke → eval → threshold tuning → apply-go prep
> **This is still Session 199.** An earlier S199 window completed the reconciler fix (everything under "The fixes" below) but **never closed out — its work sits UNCOMMITTED in the working tree and `worklog.md` has NO Session 199 entry.** You inherit that work and continue the same session number. Stamp `### Session 199` at endsession, covering BOTH the fix and your Stage-2 work.
> **Recommended model:** **Fable** (Matt's pick for the continuation — Stage-2 quality eval + auto-accept tuning + apply-go judgment). The Stage-2 *extraction* is a separate Opus `claude -p` worker, **Matt-fired from iTerm** (`feedback_no_extraction_without_asking`).

## ✅ ALREADY DONE (2026-07-07, uncommitted) — do NOT redo
> **READ FIRST: `working/fire-and-blood/smoke/v1/EVAL-stage1-reconciler-fix.md`** — the verification of record. All 5 fixes below are applied in `scripts/fab-reconcile-candidates.py` (+ lockstep `scripts/mint_enrichment.py` patch), **plus a 6th discovered fix: event-type-aware routing** (an event defers to review only when a candidate is itself an existing `events` node — caught event-vs-event dupes the EVAL missed: `Submission of Rosby`≈`yielding-of-rosby`, `Surrender of Storm's End`≈`taking-of-storms-end`, `Battle at the Wailing Willows`≈`wailing-willows`). Build-time tests `scripts/test-fab-reconcile.py` **23/23 pass** (incl. R1 trap). Re-reconcile on the Stage-1 proposal (fresh output `working/fire-and-blood/smoke/v1/recon-after/`): **CREATEs 36→6** (all genuinely-new `event.*`), quarantine 14→4 (96.7% located; residuals are 1 empty-quote edge + 3 real extractor punctuation deviations, correctly flagged), contradictions → **1 genuine flag** (Edmyn Tully sworn to Harren Hoare vs `house-tully`), trap edges 0. The optional fresh-verify also ran: **5 of 6 CREATEs safe; `aegons-second-coronation` is a semantic dupe of existing `aegons-coronations` → disposition at apply = fold in as UPDATE, don't CREATE.** The wrap-aware mint change is logged in `working/fire-and-blood/architecture-batch-s198.md`.
> Sanity-check the inherited tree before proceeding: `python3 scripts/test-fab-reconcile.py` must still pass 23/23; `git status` should show the reconciler/mint/architecture-batch diffs.

## Where S198 left this (background — the fix half is now done, see above)
S198 built the whole F&B pipeline and ran the **Stage-1 smoke** (`fab-aegons-conquest-03`, Matt-fired). Fresh-eval verdict = **PASS-WITH-CONCERNS** (`working/fire-and-blood/smoke/v1/EVAL-stage1.md` — READ IT FIRST, plus `history/session-details/session-198.md`). The **extraction half is strong — do NOT touch `working/fire-and-blood/prompts/fab-enrichment-v1.md`.** All fixes are in **`scripts/fab-reconcile-candidates.py`** (+ one lockstep patch to `scripts/mint_enrichment.py`).

Nothing is minted — the graph is untouched. This is still a dry run; **node/edge writes stay gated on Matt** (`feedback_no_graph_mutation_without_goahead`).

## The fixes — ✅ ALL APPLIED (kept for reference; see the DONE block above)
1. **CREATE guard too weak → duplicate-mint (BLOCKER).** Routing currently mints CREATEs for names where the resolver returned status `candidates` (fuzzy matches exist) — design §5.1 rule 3 says those go to **review**, never CREATE. Evidence: 9 house dupes (`blackwoods`→existing `house-blackwood`, etc.), `daenys`→`daenys-targaryen`, `arrec`→`arrec-durrandon`. Fix: only CREATE on a **clean `miss`** (no fuzzy candidates) AND a full/unique name AND no cluster collision AND the slug doesn't already exist. Any `candidates`/`ambiguous` status → review. Re-check singular/plural + house-name forms against `graph/nodes/houses/` and the alias table before minting a house node.
2. **Composite/collective cells minted as nodes (BLOCKER).** 7 junk `character.human` nodes from unsplit `;`-joined Event-table cells (`mern-ix-gardener-loren-i-lannister`) and collective referents (`the-targaryen-fleet`, "the Faith"). Fix: split `;`/`,`/`and`-joined roster+event cells into individual names BEFORE resolution; skip obvious collectives (a small stop-list + a "starts with 'the ' and plural/again-collective" heuristic → route to review, don't CREATE).
3. **Quote locator misses paragraph-spanning quotes (HIGH, cheap).** All 14 Stage-1 quarantines recover under whitespace-collapse; the locator only joins 2 physical lines. Make it wrap-aware (collapse whitespace across a small window, e.g. 3–4 lines). **CRITICAL: mirror the SAME change in `scripts/mint_enrichment.py:authoritative_line`** — the reconciler's grep and mint's grep MUST stay byte-identical, else a reconciler-"located" quote aborts mint at apply time. (This is a real mint code change — flag it in the S198 architecture batch / worklog Active Decision when it lands.)
4. **Contradictions report polluted by the dupe bug.** Re-diff on canonical slugs after fix 1.
5. **New-node type defaults to `character.human`.** Carry the extractor's `Type guess` roster column into the CREATE node's `type:` frontmatter (map guesses → schema types; fall back to `character.human` only when blank).

## Steps (UPDATED 2026-07-07 evening — Stage-2 eval + tuning DONE; next = out-of-sample validation)
> **DONE this window (S199 continued, uncommitted):** Stage-2 smoke reconciled + fresh-evaled
> (**PASS-WITH-CONCERNS**, `EVAL-stage2.md`); quote repair built (63.7%→98.9% located);
> §5.1 tuned (discriminator margin rule + parent/spouse base-name + punctuation-token scorer
> fixes → 15/23 accepts, 0 wrong; exact-1.0 + positive-type-agree rule → 130 clean would-accepts);
> BOTH eval blockers fixed (type-agreement gate — caught `Lorath`→jaqen AND `Sea Snake`→corlys;
> `run_id`/cites now keep `-pMM`); review-candidate probes, type normalization, merge-plan hygiene,
> `matched.jsonl` + `quotes-repaired.jsonl` sidecars, year-aware `era:`. Tests **51/51**.
> Full record: `working/fire-and-blood/smoke/v1/EVAL-stage2-reconciler-tuning.md` (+ §2b).
> Stage-2 CREATE fresh-verify: `baelon-avenges-aemon-on-tarth` = DUPE of existing `myrish-bloodbath` — fold at apply (`recon-heirs-15-p01/fresh-verify-creates.md`).

1. ~~Stage-1 fixes~~ ✅ / 2. ~~Stage-2 smoke~~ ✅ / 3. ~~reconcile + fresh-eval + fresh-verify~~ ✅ / 4a. ~~threshold tuning~~ ✅ / 4b. ~~out-of-sample validation~~ ✅ **GATE PASSED — 0 wrong accepts / 66 rows** (`EVAL-oos-accept-validation.md`; p02 quote-wrap drift fixed same window, dispute machinery confirmed at disputed_rate 0.101; CREATE dupes: `EVAL-oos-create-verify.md`) / 4c. ~~§7.2 dispute-axis gate~~ ✅ **PASS after fix** — v1 audit FAIL (26.9% tier inflation, passage-scope hedges) → dispute-proximity quarantine built (`dispute-review.jsonl`; strong-terms lexicon; romance-class hold; tests 63/63) → v2 audit **0.0%/0.0%**, quarantine recall 100% (`EVAL-dispute-axis-audit{,-v2}.md`). **ALL pre-bulk gates are now green.**
5. **NEXT — Matt's apply-go.** Pre-apply checklist (all recorded in `EVAL-stage2-reconciler-tuning.md`):
   - ~~Schema decision~~ ✅ DECIDED (Matt 2026-07-07): 4 novel event subtypes ADOPTED + added to architecture.md type table (incl. `birth-of-<canonical-char-slug>` slug convention). Undocumented pre-existing subtypes (`event.death`/`capture`/`ceremony`/`council`) flagged as todo.
   - ~~`identity_line` wire-vs-waive~~ ✅ DECIDED (Matt 2026-07-07): **WIRED** — reconciler derives a book-grounded Identity line from Node-Prose bullet 1 (pronoun/length guards; merge writer still swaps ONLY boilerplate lines). 58/58 merge-plan entries carry it across the 4 smoke units; strip-track sequencing premise preserved.
   - Folds (semantic dupes, 3-for-3 units): `aegons-second-coronation`→`aegons-coronations`; `baelon-avenges-aemon-on-tarth`→`myrish-bloodbath`; `accession-melee-at-maidenpool`→`tourney-for-king-viserys-is-accession`; `death-of-alyn-stokeworth`→`harren-the-reds-rebellion`; `daemon-slays-craghas-crabfeeder`→fold or PART_OF `war-for-the-stepstones`.
   - Renames: `birth-of-aegon`→`birth-of-aegon-ii-targaryen`; `birth-of-maegor-targaryen`→`birth-of-maegor-i-targaryen`; adopt `birth-of-<canonical-char-slug>` convention.
   - Edges to add on CREATE: `summoning-of-vaegon` CAUSES → `great-council-of-101-ac`.
   - Graph hygiene (small writes at apply): strip junk `"Lorath"` alias off `jaqen-hghar`.
   - Incidental flags for triage (NOT this track): `vaegon`/`vaegon-targaryen` dupe pair; `great-council-of-101-ac` mistyped `event.battle` + empty body; `manfred-hightower-aegons-conquest` has `type: event.war` on a character node; no node for the historical Ronnel Arryn (Moon Door, ~37 AC).
   - The architecture batch + both mint patches (wrap-aware locator + norm `''`-collapse + blank-start skip) land as ONE worklog Active Decision; commit inherited + new S199 work together; `### Session 199` worklog entry at endsession (Matt-gated).
   - **`identity_line` gap — surface it for Matt's wire-vs-waive decision (found 2026-07-07, NOT yet fixed):** `fab_merge_node.py` carries full Identity-swap machinery, but the reconciler never populates `identity_line` in any merge plan (0 refs in `fab-reconcile-candidates.py`; 0 in `recon-after/merge-plan.json`). As-is, a real apply appends `## Fire & Blood` sections but leaves every boilerplate Identity line untouched. This matters beyond F&B: **the strip-boilerplate track was parked behind F&B on the premise that F&B swaps those lines** (`working/node-enrichment-wiki-prose/reconcile-strip-vs-fab-RECOMMENDATION.md`) — waiving weakens that sequencing. Wiring it = derive a book-grounded Identity sentence per UPDATE node and thread it into the merge plan.
   - `aegons-second-coronation` → fold into `aegons-coronations` (UPDATE, not CREATE).
   - The architecture batch (`working/fire-and-blood/architecture-batch-s198.md`) + both mint patches land as one worklog Active Decision.
   - Commit the inherited S199 fix work together with yours; write the `### Session 199` worklog entry at endsession (Matt-gated as always).

## Read first
- `working/fire-and-blood/smoke/v1/EVAL-stage1-reconciler-fix.md` (the DONE fix record: before/after, 6th fix, fresh-verify finding)
- `working/fire-and-blood/smoke/v1/EVAL-stage1.md` (the original verdict + specific dupe examples)
- `history/session-details/session-198.md` (full build narrative + interfaces)
- `working/fire-and-blood/build-spec-s198.md` (the locked interfaces the reconciler must honor)
- `working/fire-and-blood/fire-and-blood-enrichment-design.md` §5.1 / §5.3 / §7

## Open questions for Matt: ONE — the `identity_line` wire-vs-waive decision (step 5); raise it at apply-go prep, not before. Stage-2 extraction is Matt-fired; apply stays gated.
## DO NOT
- Do NOT redo reconciler fixes 1–5 or the event-routing fix — they're applied + verified in the uncommitted tree. Don't discard/checkout those diffs.
- Do NOT touch the extraction prompt (it passed) or re-split `sources/chapters/fab/`.
- Do NOT write `graph/nodes/`, `edges.jsonl`, or run mint/merge for real without Matt's apply-go.
- Do NOT run `--smoke`/`--resume` extraction yourself (Matt fires from iTerm) or auto-run `/endsession`.
- Do NOT re-fetch the wiki.
- Do NOT touch the strip-boilerplate track — it is PARKED behind this track's FULL apply cycle (all packs), `working/node-enrichment-wiki-prose/reconcile-strip-vs-fab-RECOMMENDATION.md`.
