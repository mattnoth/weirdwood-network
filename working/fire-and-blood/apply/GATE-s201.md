# S201 — F&B bulk reconcile-apply: systemic §7a health gate + batch plan

Bulk extraction run COMPLETE (all 39 units drained on v1, manifest `88670d51`).
4 smoke units (aegons-conquest-03, heirs-15-p01/p02, sons-05-p01) already APPLIED in S200 —
they were re-extracted by the bulk `--resume` (keys off manifest, not file existence); the
throwaway re-extractions were restored to HEAD (applied versions preserved). **35 units to apply.**

## Systemic gate = PASS (no prompt failure)
- **Dispute machinery alive on every Dance unit** (the prompt-failure canary): heirs-15-p03 (disp 0.179 / 43 held), blacks-greens-16-p01/p02, red-dragon-17-p01..p04, rhaenyra-18-p01/p02, short-sad-19 all show dispute activity via extractor-tags and/or reconciler quarantine. No Dance unit shows disp≈0 AND held≈0. Not a prompt failure.
- **CREATE volume healthy**: 234 total ≈ 6.7/unit (S200 ~6/unit). One outlier: `surfeit-of-rulers-08-p02` = 17 (inspect in Batch 2).
- **4 units < 90% quote-located** (row-level quote quarantine, tolerated, NEVER re-extract): jaehaerys-triumphs-12-p02 (87.6), blacks-greens-16-p02 (88.3), red-dragon-17-p02 (87.1), red-dragon-17-p03 (86.0).
- **3 units flag needs_vocab=1**: prince-into-king-06 (Alyssa regent-for-Jaehaerys — no REGENT type in locked vocab; candidate vocab addition, recurs heavily in F&B regency era — flag Matt), sons-05-p03 (Maegor disinherits Jaehaerys — substance in CREATE event `maegor-names-aerea-heir-disinherits-jaehaerys`, dyad redundant), rhaenyra-18-p02 (TBD in batch).
- **Totals: 234 CREATEs, 1,504 edges** across 35 units.

## Batch plan (chronological, section order)
- **Batch 1** (sec 04–07): reign-of-the-dragon-04, sons-05-p02, sons-05-p03[vocab], prince-into-king-06[vocab], year-of-the-three-brides-07 — 32 CREATEs, **0 disputes**
- **Batch 2** (sec 08–11): surfeit-08-p01, surfeit-08-p02[CREATE=17], time-of-testing-09, birth-death-betrayal-10, jaehaerys-dragonstone-11
- **Batch 3** (sec 12–14): triumphs-12-p01, triumphs-12-p02[loc<90], long-reign-13, long-reign-cont-14-p01, 14-p02
- **Batch 4** (sec 14–16): long-reign-cont-14-p03, 14-p04, heirs-15-p03[Dance], blacks-greens-16-p01[Dance], 16-p02[Dance,loc<90]
- **Batch 5** (sec 17, Dance war): red-dragon-17-p01, 17-p02[loc<90], 17-p03[loc<90], 17-p04
- **Batch 6** (sec 18–21, Dance end): rhaenyra-18-p01[Dance], 18-p02[Dance,vocab], short-sad-19, hour-of-the-wolf-20, hooded-hand-21
- **Batch 7** (sec 22–25, aftermath + appendix): war-peace-cattle-22-p01, 22-p02, voyage-alyn-23, lysene-spring-24-p01, 24-p02, lineages-25

## Per-batch rhythm (S200 §8 pattern)
reconcile (done, upfront) → CREATE fresh-verify subagent (dupe/rename/parent) → dispute
adjudication subagent + orchestrator primary-text verify (Dance batches) → deterministic surgery
on candidates.json/nodes/ → git checkpoint → mint → merge (0 skipped/0 not-found) → commit →
`weirwood refresh` + `test-fab-reconcile.py` after each batch.
