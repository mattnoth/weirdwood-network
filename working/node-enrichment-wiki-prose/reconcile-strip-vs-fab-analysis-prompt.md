# Analysis task: what is the BEST way to reconcile the boilerplate-strip track with the Fire & Blood merge-writer?

> **Recommended model:** Sonnet (reading two scripts + a design doc + deterministic quantification + a structured trade-off recommendation; no bulk pass). Bump to Opus only if you want the deepest reasoning on the sequence-vs-patch trade-off.
> **Gate: READ-ONLY.** Do NOT run `--apply`, do NOT edit `scripts/strip-wiki-boilerplate.py`, `scripts/fab_merge_node.py`, the F&B design doc, or any node. Do NOT re-fetch the wiki. Do NOT run `/endsession`. Your deliverable is a written recommendation; Matt decides, a later session implements.

## Your job
Two graph tracks both rewrite the auto-generated `## Identity` boilerplate line (`"<Name> is a <type> from the AWOIAF wiki."`) on the same ~6,700 wiki nodes, and a prior review proved they are **NOT order-independent** despite the worklog/todos calling them "safe alongside F&B" / "parallel-safe." Your task: **analyze the collision and recommend the single best way to reconcile the two tracks** so both can land without one silently defeating the other. You are free to pick one of the three options below, combine them, or propose a better one — but commit to a recommendation and justify it.

## Background — the two tracks
1. **Boilerplate strip** (`scripts/strip-wiki-boilerplate.py`, Matt-approved approach, unapplied). Sweeps all 6,711 boilerplate nodes. **Rich** nodes (5,490, have real body prose) → strips only the ` from the AWOIAF wiki` tail, keeping `"<Name> is a <raw-dotted-gloss>."` (Matt likes the raw `organization.house` gloss — do NOT humanize). **Thin** nodes (1,221, Identity+Edges only) → drops the line entirely, leaving an empty `## Identity` section.
2. **Fire & Blood merge-writer** (`scripts/fab_merge_node.py`, built S198, dry-run only, apply gated). On its Targaryen-history target nodes it detects the boilerplate Identity line via `BOILERPLATE_RE = ^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$` and **swaps** it for book-grounded prose, then appends a `## Fire & Blood` section. No-Identity nodes get an Identity section inserted. Real (non-boilerplate) Identity is left alone.

## The confirmed collision (verified end-to-end on the real code — you may spot-check, don't re-derive from scratch)
Running the strip **before** F&B permanently defeats F&B's Identity swap, because the strip removes the exact ` from the AWOIAF wiki.` tail F&B keys on:
- **Rich (4,682 nodes):** stripped line `"House Antaryon is a organization.house."` no longer matches F&B's `BOILERPLATE_RE` → F&B reports `left_alone_real_identity` → book-grounded swap never happens; the bare stub persists forever.
- **Thin (950 of 1,221):** post-strip empty `## Identity` → F&B's `get_identity_line()` returns `None` → also `left_alone_real_identity` → book-grounded line never inserted (an undesigned 4th shape F&B has no branch for).
- **Total interface breakage: 5,632 nodes** (theoretical max; the real damage = the intersection with F&B's actual target set — see task 2).
- **Reverse order is provably safe:** strip-*after*-F&B leaves F&B-swapped nodes alone (the phrase is confined to exactly one line per node — 0 nodes have it twice — so once F&B swaps the Identity the node stops `grep`-matching and the strip never revisits it).
- **Separate script nit (independent of the ordering question):** the strip's `RICH_SECTIONS_RE` allowlist misclassifies **46 content-bearing nodes** (27 `## Heraldry & Sigil`, 15 `## Culture`, 6 `## Aftermath`) as "thin" and drops their Identity line, leaving an empty section on a node that has content. Note it in your recommendation if it affects the reconciliation, but the core question is the ordering.

## Files to read
- `scripts/strip-wiki-boilerplate.py` and `scripts/fab_merge_node.py` (the two scripts — read both in full).
- `working/node-enrichment-wiki-prose/strip-boilerplate-dryrun.md` (the strip's scope report: rich/thin counts + type-gloss distribution).
- `working/fire-and-blood/fire-and-blood-enrichment-design.md` (F&B design — §node-shapes ~L42-44, §5.3 merge-writer ~L281).
- F&B's **target-set artifacts** to estimate the real overlap: `scripts/fab-build-candidate-packs.py` + its output, `scripts/fab-reconcile-candidates.py` + its output, and the one completed smoke unit under `working/fire-and-blood/fab-aegons-conquest-03/` (reconciler UPDATE-routed slugs = concrete F&B targets). Only 1 of ~23 candidate-packs has been processed — the full target set is NOT yet materialized (see task 2).
- `worklog.md` Session Log S198 + `progress/continue-prompts/2026-07-07-fire-and-blood-reconciler-fix-stage2.md` for F&B's remaining runway to apply (reconciler fix → re-reconcile → Stage-2 smoke → apply-go). **worklog.md is authoritative for project state** — if any doc disagrees, trust it and flag the drift.

## Analysis tasks
1. **Spot-verify the load-bearing facts** above (cheap — confirm the two regexes and one rich + one thin example; don't rebuild the whole review).
2. **Quantify the true stakes.** The 5,632 is the theoretical max; F&B only enriches its Targaryen target subset. Estimate how many nodes F&B will *actually* touch from the candidate-packs / reconciler output / the smoke unit. Key constraint: F&B's full target set is not yet determined (dry-run, 1/23 packs). So reason about the decision **under that uncertainty** — a clean one-time sequence bets on a target set that doesn't fully exist yet.
3. **Weigh timing.** The strip is ready now (Matt approved). F&B is several gated steps from its first apply (S199+). Sequence-first means the strip **waits on F&B's entire apply cycle** — factor that cost.
4. **Evaluate the reconciliation options** on real criteria — correctness, effort, risk, how long each track is blocked, whether it restores *true* order-independence (so neither track has to remember to run first), and complexity added to a mid-build F&B script that still has a known reconciler bug (S199):
   - **(A) Sequence:** F&B's first real apply runs before the strip; strip then sweeps the untouched remainder (zero code; strip-after-F&B is provably safe; but strip is blocked and the "remainder" is a moving target while F&B is incremental).
   - **(B) Patch F&B's shape-detection** (it's still apply-gated, so no rework): teach it that a stripped-tail one-liner is boilerplate-equivalent → swap, and an empty `## Identity` section is insert-equivalent → insert. Optionally broaden its regex to also catch the freeform-gloss boilerplate it *already* misses (808 rich nodes like `"House X is a noble house from the AWOIAF wiki."` — F&B currently leaves the wiki-tail on those even before any strip; worth surfacing).
   - **(C) Make the strip F&B-aware** (e.g., skip/defer nodes on F&B's target list, or leave a machine-detectable marker), or any hybrid.
   - **(D) Your own better option** if you see one.
5. **Commit to a recommendation:** the single best path + justification, the quantified stakes it's based on, a concrete implementation sketch (what changes, where, and the test cases that would prove it), and a one-line reason each rejected option loses. If your recommendation depends on a fact you couldn't pin down (e.g., F&B's final target size), say so and state what would change the answer.

## Deliverable
Write your analysis to `working/node-enrichment-wiki-prose/reconcile-strip-vs-fab-RECOMMENDATION.md` and return a tight summary (the recommended path + the one or two numbers it hinges on + the top reason). Do not apply anything, edit any script/node, or touch the worklog.
