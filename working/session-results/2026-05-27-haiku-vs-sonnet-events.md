# Haiku vs Sonnet — Events edge-typing comparison (2026-05-27)

**Goal:** decide the model for the remaining ~82% of the `pass1_events` run.
**Method:** ran Haiku 4.5 (`claude-haiku-4-5-20251001`) on the **same first 600 rows**
Sonnet processed (deterministic load order, `--smoke 600`, separate dir
`_events-haiku-cmp-20260527/`), then diffed verdicts row-by-row and hand-scored
Haiku's emits against their evidence quotes.

> **Tooling note:** `--smoke` was silently ignored under `--input-dir` (gated on
> `args.input_dir is None`). First launch started the *full 415-batch* bulk on
> Haiku; killed at batch 1 ($0.00). Fixed (`scripts/stage4-tail-classifier.py`,
> +regression test, 1015 green) → `--smoke 600` now truncates to 15 batches.

## Run facts
| | Sonnet (baseline) | Haiku (candidate) |
|---|---|---|
| rows | first 600 (of its 3,240) | 600 |
| emits | 78 | 59 |
| reject rate | ~87% | ~90% |
| classify_failed | 0 (in first 600) | 0 |
| $/batch | ~$0.25 | ~$0.12 |
| sec/batch | ~220s | ~145s |
| cost (600 rows) | ~$3.75 | **$1.83** |
| rate-limit walls | hits ~75 batches/5h | **0 over 15 batches** |

## Verdict diff (matched on source/target/chapter/hint — 600/600 overlap)
- **Agreement: 527/600 = 87.8%** (26 same-type emits + 501 both-reject).
  *Inflated by the ~90% reject rate — both-reject dominates. Not the deciding metric.*
- **Divergence:**
  - `haiku_over_emit` (Sonnet reject / Haiku emit): **21**
  - `haiku_miss` (Sonnet emit / Haiku reject): **40**
  - `both_typed_diff`: **12**

## Haiku standalone strict precision (hand-read of all 59 emits vs evidence_quote)
- **Clear-correct: ~50/59** (SIBLING_OF, PARENT_OF, KILLS, DUELS, BETROTHED_TO,
  SERVES, IMPRISONS, HELD_BY, TRAVELS_TO, RESENTS, and well-supported TRAVELS_WITH).
- **Genuine errors: ~3–4** — `arya CONTRASTS sansa` (weak/wrong type vs SIBLING_OF);
  `hunt-of-the-poor-fellows PARTICIPATES_IN benjen` (**bad candidate slug** — the
  generator mis-resolved "the hunt"→a religious order; + wrong direction; *Sonnet
  rejected it, Haiku didn't*); `bran LOCATED_AT winterfell` from a coma-dream quote.
- **True-but-momentary / low-value: ~5–6** — single-trip TRAVELS_WITH (6 edges from
  one crypt-descent scene), `OWNS summer` (direwolf → should be BONDED_TO; **auto-fixed
  by merge-rule #6**), `TRAVELS_WITH grey-wind` (direwolf, not caught by merge-rule).
- **Strict precision ≈ 83–86% (point ~85%)** — *comparable to Sonnet's 82–86%*, and
  far above the pre-v5 Haiku smokes (~60–62%). **The v5 rules + cleaned candidates
  fixed Haiku.**

## Reading the divergence
- **Over-emit (21) is NOT 21 errors.** ~4 are edges Haiku caught that Sonnet wrongly
  rejected (`theon KILLS stiv`, `gates-of-the-moon HELD_BY nestor-royce`,
  `catelyn ENCOUNTERS petyr`, `arya MOURNS mycah`). ~12 are true-but-momentary
  TRAVELS_WITH/LOCATED_AT. ~5 are weak/wrong. **Net incremental pollution ≈ 5 rows / 600 (~0.8%).**
- **Miss (40) is the real cost.** Haiku rejects edges Sonnet correctly typed —
  including high-value ones: `catelyn CAPTURES tyrion`, `assassin ATTACKS catelyn`,
  `syrio TUTORS arya`, `bronn ATTACKS/DUELS vardis`, multiple SIBLING_OF/BONDED_TO.
  **Haiku → a sparser Events layer.** Per project value ("a missing edge is recoverable;
  a wrong edge is pollution"), lower recall is the *acceptable* failure mode.
- **Core difference:** Haiku applies the STATE-not-MOMENT gate more loosely (emits
  momentary co-movement) but the FACT/DIRECT gates about as well. Sonnet is stricter
  on standing-vs-momentary, looser on letting borderline through elsewhere.

## Decision rule (from the continue prompt)
> If Haiku ≥~80% strict AND over-emit divergence is low → switch + sleep-until-reset wrapper.
> Else → finish on Sonnet (wrapped).

- Haiku strict ≈ 85% ✓ (≥80%)
- Net over-emit pollution ≈ 0.8% ✓ (low)
- Quota: Haiku 0 walls, ~2× cheaper/faster, won't block Matt's sessions ✓

**→ Both conditions met. Recommendation: SWITCH the remaining ~340 batches to Haiku,
wrapped in `scripts/stage4-run-forever.sh` (sleep-until-reset).**

**Caveats for Matt:**
1. Haiku yields a *thinner* Events layer (lower recall) than Sonnet would.
2. Haiku is inconsistent on direwolf typing; merge-rule #6 (OWNS→BONDED_TO) catches the
   OWNS cases but not TRAVELS_WITH-direwolf. Minor.
3. The bad-slug case (#12) is a **candidate-generation** defect both models received —
   a slug-quality gate (S69 backlog) would remove it upstream regardless of model.
4. Single sample (600 AGOT rows). Sonnet's 82–86% spanned 5 checkpoints / 3,000 rows
   (AGOT+ACOK). If Matt wants the ≥2-fresh-samples bar, run a second Haiku smoke on a
   later slice (e.g. an ACOK/ASOS window) before committing the full bulk.

---

## Sample 2 — ACOK out-of-sample (2026-05-27, Matt chose "2nd validation first")
Ran Haiku on the first 600 **ACOK** `pass1_events` rows (`--book acok --smoke 600`,
dir `_events-haiku-cmp2-acok-20260527/`). Different book = true out-of-sample.

- **65 emits / 535 rejected / 0 classify_failed / $1.80 / ~25 min / 0 walls.**
- **Hand-read of all 65 emits ≈ 89–95% strict (point ~90%)** — *stable, slightly better
  than sample-1's ~85%.* Clean HATES/SERVES/COMMANDS/SEEKS (Arya@Harrenhal) +
  BONDED_TO/DREAMS_OF/RESCUES (Bran). Only ~3 clear errors, all **bad candidate slugs**:
  `four-storms→flowstone-yard` ("Four brothers" mis-slug), `bastard→hornwood DIED_AT`
  (generic slug, unsupported), `bran→chayle REVEALS_TO` (wrong direction). Plus a few
  slug-imprecise-but-valid (`lord-tywin` ship/man ambiguity ×2, `dog`, `hornwood` house-as-person).
- **Diff vs Sonnet's clean ACOK verdicts (368 comparable):** agreement **84.8%**
  (20 same-type + 292 both-reject); over-emit 18, miss 33, diff-type 5. Consistent with sample 1.

### Cross-cutting finding
Residual errors in BOTH samples are dominated by **candidate-generation slug defects**,
not Haiku misclassification. A slug-quality gate (S69 backlog) cleans them regardless of model.

## FINAL VERDICT — ≥2-fresh-samples bar CLEARED
| | Sample 1 (AGOT 600) | Sample 2 (ACOK 600) |
|---|---|---|
| Haiku strict precision | ~85% | ~90% |
| agreement vs Sonnet | 87.8% | 84.8% |
| walls / cost | 0 / $1.83 | 0 / $1.80 |

Two independent samples / two books, both ≥85% strict, stable. **Haiku validated for the bulk.**
**Recommendation: SWITCH the remaining ~82% to Haiku, resume into a COPY of the Sonnet dir
with `--skip-existing` (skips the 3,000 Sonnet-typed rows, RETRIES the 240 wall-failures —
verified: load_existing_keys reads only edges+rejected, not classify_failed), wrapped in
`scripts/stage4-run-forever.sh`. ~$40, mixed provenance preserved via `typed_by`. Sonnet
baseline `_events-run-20260527/` stays pristine.**
