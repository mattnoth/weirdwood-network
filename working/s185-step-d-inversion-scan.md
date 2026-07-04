# S185 Step D — same-year intra-chapter inversion scan

Deterministic scan (read-only) closing the S184 caveat: S184 found 0 causal
inversions at YEAR granularity; the composite key is now chapter-resolution, so
re-scan same-year causal edges at chapter level.

**Method:** for every CAUSES/TRIGGERS/MOTIVATES edge whose source & target share
`occurred.ac_year` AND both carry a composite, compare full composites; flag
`source_composite > target_composite` (a cause narrated after its effect).

**Result (2026-07-03):**
- same-year causal edges with both composites: **53**
- genuine intra-chapter inversions: **0**
- flagged-but-artifact: **5** — every one has a target composite of `{year}.0.000`,
  i.e. the target event is dated (has ac_year) but has **no chapter anchor**
  (book_order/chapter absent → composite tail `.0.000`, which sorts before any real
  chapter that year). These are data-completeness gaps, NOT ordering bugs — do not flip.

The 5 chapter-anchor gaps (targets to backfill an `evidence_chapters` anchor for,
a Step C follow-on — NOT an edge-direction flip):
- robb-weds-jeyne-westerling (0299)
- fall-of-moat-cailin (0299)
- harrying-of-the-stony-shore (0299)
- landing-of-the-golden-company (0300)
- stannis-retreats-to-dragonstone (0299)

**Conclusion:** the causal layer is chronologically sound at chapter resolution.
No edge direction needs flipping. The render bug was purely traversal-order (fixed
in walkChain, S185 Step A), never bad data.
