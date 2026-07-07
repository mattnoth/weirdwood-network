# SESSION 199 — Fire & Blood: reconciler fix → re-reconcile → Stage-2 smoke
> **This is Session 199.** Stamp your worklog entry `### Session 199` at endsession.
> **Recommended model:** **Sonnet** (the fixes are deterministic Python — `feedback_python_before_agent`). The Stage-2 *extraction* is a separate Opus `claude -p` worker, **Matt-fired from iTerm** (`feedback_no_extraction_without_asking`).

## Where S198 left this
S198 built the whole F&B pipeline and ran the **Stage-1 smoke** (`fab-aegons-conquest-03`, Matt-fired). Fresh-eval verdict = **PASS-WITH-CONCERNS** (`working/fire-and-blood/smoke/v1/EVAL-stage1.md` — READ IT FIRST, plus `history/session-details/session-198.md`). The **extraction half is strong — do NOT touch `working/fire-and-blood/prompts/fab-enrichment-v1.md`.** All fixes are in **`scripts/fab-reconcile-candidates.py`** (+ one lockstep patch to `scripts/mint_enrichment.py`).

Nothing is minted — the graph is untouched. This is still a dry run; **node/edge writes stay gated on Matt** (`feedback_no_graph_mutation_without_goahead`).

## The fixes (all in `scripts/fab-reconcile-candidates.py` unless noted) — ranked
1. **CREATE guard too weak → duplicate-mint (BLOCKER).** Routing currently mints CREATEs for names where the resolver returned status `candidates` (fuzzy matches exist) — design §5.1 rule 3 says those go to **review**, never CREATE. Evidence: 9 house dupes (`blackwoods`→existing `house-blackwood`, etc.), `daenys`→`daenys-targaryen`, `arrec`→`arrec-durrandon`. Fix: only CREATE on a **clean `miss`** (no fuzzy candidates) AND a full/unique name AND no cluster collision AND the slug doesn't already exist. Any `candidates`/`ambiguous` status → review. Re-check singular/plural + house-name forms against `graph/nodes/houses/` and the alias table before minting a house node.
2. **Composite/collective cells minted as nodes (BLOCKER).** 7 junk `character.human` nodes from unsplit `;`-joined Event-table cells (`mern-ix-gardener-loren-i-lannister`) and collective referents (`the-targaryen-fleet`, "the Faith"). Fix: split `;`/`,`/`and`-joined roster+event cells into individual names BEFORE resolution; skip obvious collectives (a small stop-list + a "starts with 'the ' and plural/again-collective" heuristic → route to review, don't CREATE).
3. **Quote locator misses paragraph-spanning quotes (HIGH, cheap).** All 14 Stage-1 quarantines recover under whitespace-collapse; the locator only joins 2 physical lines. Make it wrap-aware (collapse whitespace across a small window, e.g. 3–4 lines). **CRITICAL: mirror the SAME change in `scripts/mint_enrichment.py:authoritative_line`** — the reconciler's grep and mint's grep MUST stay byte-identical, else a reconciler-"located" quote aborts mint at apply time. (This is a real mint code change — flag it in the S198 architecture batch / worklog Active Decision when it lands.)
4. **Contradictions report polluted by the dupe bug.** Re-diff on canonical slugs after fix 1.
5. **New-node type defaults to `character.human`.** Carry the extractor's `Type guess` roster column into the CREATE node's `type:` frontmatter (map guesses → schema types; fall back to `character.human` only when blank).

## Steps
1. Read `EVAL-stage1.md` + `history/session-details/session-198.md` + design §5.1/§5.3.
2. Apply fixes 1–5. Re-run the reconciler's build-time unit tests (the `_recon-test` fixture) — they must still pass, especially the trap-routing (`aegon-targaryen` never accepted).
3. **Re-run reconcile on the Stage-1 output** (deterministic, no API $): `python3 scripts/fab-reconcile-candidates.py --proposal working/fire-and-blood/smoke/v1/fab-aegons-conquest-03.enrichment.md --smoke`. Success = CREATEs drop **36 → ~14**, quarantine → **~0**, the 9 house dupes gone, no composite nodes, contradictions report clean. Show the run-summary before/after.
4. **(Optional, cheap) fresh-verify** a sample of the corrected CREATEs/matches with a subagent — confirm no remaining dupe-mint risk before Stage 2.
5. **Hand Matt the Stage-2 smoke command** (ONE fenced block, `feedback_one_handoff_per_block`) — he fires from iTerm:
   `cd /Users/mnoth/source/asoiaf-chat && python3 working/fire-and-blood/fire-and-blood-extraction.py --smoke --only fab-heirs-of-the-dragon-15-p01 --prompt-version v1`
   Stage 2 = the Dance prelude: the ambiguity/dispute **quality** test (same-name routing under real load, disputed-tagging density, node-prose quality, UPDATE/CREATE mix). Reconcile its output with `--smoke` (auto-accept still disabled), fresh-eval quality.
6. After Stage 2 passes: tune the §5.1 auto-accept thresholds and validate on **≥2 fresh units** out-of-sample (`feedback_fresh_review_and_out_of_sample`) — do NOT tune on the unit you measured.
7. Then it's Matt's **apply-go**: that's when the architecture batch (`working/fire-and-blood/architecture-batch-s198.md`) + the 3-line mint patch land (one worklog Active Decision), and the first real mint/merge/refresh runs.

## Read first
- `working/fire-and-blood/smoke/v1/EVAL-stage1.md` (the verdict + specific dupe examples)
- `history/session-details/session-198.md` (full build narrative + interfaces)
- `working/fire-and-blood/build-spec-s198.md` (the locked interfaces the reconciler must honor)
- `working/fire-and-blood/fire-and-blood-enrichment-design.md` §5.1 / §5.3 / §7

## Open questions for Matt: none — reconciler fix is a go; Stage-2 extraction is Matt-fired; apply stays gated.
## DO NOT
- Do NOT touch the extraction prompt (it passed) or re-split `sources/chapters/fab/`.
- Do NOT write `graph/nodes/`, `edges.jsonl`, or run mint/merge for real without Matt's apply-go.
- Do NOT run `--smoke`/`--resume` extraction yourself (Matt fires from iTerm) or auto-run `/endsession`.
- Do NOT re-fetch the wiki.
