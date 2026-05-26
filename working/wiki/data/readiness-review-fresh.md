# Fresh-Eyes Readiness Review — Stage 4 Pass-1-Derived Enrichment (~$75 Haiku run)

**Reviewer:** independent fresh-eyes pass (READ-ONLY, skeptical mandate).
**Date:** 2026-05-25.
**Question on the table:** GO or NOT-YET on a book-sharded Haiku enrichment run over the
Events+Dialogue Pass-1 tables (~21k rows, ~$75), to add breadth at ~80% post-filter precision
on top of the committed v1 (3,842 cited edges, `graph/edges/edges.jsonl`).

**Verdict up front: NOT-YET — but a *narrow* not-yet.** The plan is closer to sound than the
prior NO-GO was, and most of my objections are about *the number being reported*, not about the
strategy. One cheap test (≈$1.20 + ~40 min of reviewer time) converts this to a defensible GO.
The single most important caveat: **the headline "~80–91% post-filter" is partly circular and the
deterministic filters are demonstrably destroying TRUE edges, including a confirmed false-drop
of a TRUE `daenerys SPOUSE_OF drogo` and a TRUE `ygritte LOVES jon`. The post-filter precision
number is real-ish; the post-filter *recall cost* is unmeasured and worse than the team thinks.**

I verified every number below against the actual smoke5 files, not the task summary.

---

## 0. What I confirmed independently (so the rest is grounded)

- `_smoke5-haiku/run-summary.json`: 400 rows in, **40 typed, 360 rejected**, model
  `claude-haiku-4-5`, cost **$1.205742**. The 10% emit rate is real.
- The sample is genuinely fresh: `_fresh-relocate-4242/` (seed 4242, locator v2,
  **2.2% overlap with the old sample** per the staging manifest). This is the single best thing
  about smoke5 and it materially weakens the overfitting worry (see §1).
- I ran `stage4-type-contract-validator.py` on the 40 emits myself: it drops **5, not 4**
  (drop rate 12.5%). I ran `stage4-quote-relevance-filter.py`: it drops **4** more.
- Cost basis checks out: smoke5 = $0.00301/row → Events+Dialogue (20,994 rows) ≈ **$63**.
  The report's "$182 / $0.0068/row" figure is the *Sonnet* S67 rate and does not apply to a
  Haiku run. The ~$75 estimate is honest (slightly conservative). **No cost objection.**

---

## 1. Overfitting check (the most important question) — PARTIALLY circular, but less than feared

**The good news the team should get credit for:** smoke5 was scored on a **fresh sample with 2.2%
overlap** with the data the prompt overhaul and the older contracts were tuned on. So the 72.5%
*raw* model number is a genuine out-of-sample number for the prompt. That is the right thing to do
and it is not circular.

**Where it IS circular:** the *post-filter* lift (the jump from 72.5% raw to "~80–91%") is the part
that was designed-then-validated on the same 40 rows. The brief says the 3 newest type contracts
were designed from the exact 7 wrong rows in smoke5 and then "validated" on those same 40 emits.
That is textbook in-sample evaluation of the *filter*. When I ran the validator myself, the contracts
that fired were:

| Contract fired | row | true verdict |
|---|---|---|
| `CONTRACTED_WITH_object_target` ×2 | `illyrio CONTRACTED_WITH summer-sun` / `…josos-prank` | correct drops (both are ships/objects; one quote, two bogus targets) |
| `MEMBER_OF_direction_reversed` | `nights-watch MEMBER_OF jon-snow` | drop is right, but the TRUE edge `jon MEMBER_OF nights-watch` is lost, not recovered |
| `HOLDS_TITLE_location_target` | `robb-stark HOLDS_TITLE north` | **this is "King in the North" — a TRUE fact.** The contract kills a real edge on a slug-shape technicality |
| `SPOUSE_OF_non_char_endpoint` | `queen-cersei SPOUSE_OF robert` | **TRUE edge** (Cersei IS Robert's spouse) lost because `queen-cersei` didn't resolve to a character slug |

So of the 5 contract drops on smoke5: **2–3 are correct, and 2 are FALSE DROPS of true edges**
(`robb HOLDS_TITLE north`, `queen-cersei SPOUSE_OF robert`). The validator is *not* the clean
"4 wrong dropped, 0 false drops" tool the brief reports. It trades precision for recall and the
trade is invisible because nobody scored the kept-vs-dropped TRUE/FALSE on the drops.

**Honest out-of-sample prediction.** Strip the in-sample filter credit and you get: raw model
~72.5%, *minus* the over-confident contracts re-firing on patterns they weren't tuned for, *plus*
the genuinely-mechanical contracts (object targets, empty-quote) that generalize. My prediction for
a **truly fresh** out-of-sample post-filter number is **~76–82%**, not 91%. The 91% ceiling is an
artifact of measuring the filter on its own training rows. **Do not plan around 91%. Plan around ~78%.**

**How to get an honest number (cheap):** the contracts are *deterministic* — they don't need an LLM
re-run to evaluate. Take the existing `_tail-typed/` canonical Sonnet tail OR draw a *second* fresh
400-row stratified sample (different seed), run only the deterministic validator over it, and have a
reviewer label the drops as TRUE-drop / FALSE-drop. That gives an out-of-sample false-drop rate for
the filter at near-zero cost (no Haiku tokens — the validator is pure Python). That is the test that
tells you whether the filter is a precision tool or a recall shredder.

---

## 2. Is 72.5% raw good enough to lay down breadth? — Defensible, BUT the project's own rules push back

72.5% raw is *worse* than the v1 core that already shipped (worklog: v1 ≈ 78% strict). So the
enrichment layer will be measurably noisier than the spine it sits on. That is fine **if and only
if** the layer is queryably distinguishable from the spine so a traversal consumer can choose to
trust it less. Two things make me less worried than the prior NO-GO:

- Every enrichment edge carries `evidence_ref` (file:line) — a runtime re-verify is possible.
- The strategy ("breadth fast, patch later on a traversable graph") is legitimate **for a recall-
  expansion layer**, which is what this is.

But the framing is doing some rationalizing. Two specific places:

- **"post-filter ~80% (floor)"** leans on the circular filter credit (§1). The honest floor is the
  raw 72.5% minus whatever the filters *correctly* remove minus whatever they *wrongly* remove.
  Until the false-drop rate is measured out-of-sample, "80% floor" is a hope, not a floor.
- The project's own memory says the primary deliverable is **graph quality for agent traversal**
  and that "a wrong cited edge is graph pollution — worse than no edge." A 72.5%-raw layer means
  ~1 in 4 emitted edges asserts a false relationship *with a real-looking citation*. Citations make
  wrong edges MORE dangerous to a downstream agent, not less, because they look verified. The
  "patch later" plan has no scheduled patcher — there is no runtime re-verify built, only the
  *possibility* of one. Shipping 21k×~25%-wrong = **~5,000+ plausibly-cited wrong edges** into a
  graph whose stated purpose is agent traversal, with the cleanup deferred indefinitely, is the
  part I'd push back on hardest.

Verdict on Q2: 72.5% is *good enough for a clearly-segregated, clearly-lower-trust enrichment layer*,
**not** good enough to merge undifferentiated into the spine. The mitigation must be a hard
provenance tag (`candidate_kind: pass1_events|pass1_dialogue`, `enrichment_tier: 2`) so queries can
exclude it. Confirm that tag survives into `graph/edges/` before spending the $75.

---

## 3. The 10% emit rate (40/400) — defensible as a number, but it is hiding real losses

The team's claim ("raw pool, ~90%-reject is the norm, not a recall collapse") is **half right.**
The candidate pool is genuinely noisy (entity-pairs auto-generated from prose rows), so a high reject
rate is expected. I do not think 10% per se signals collapse.

**But the rejects are not all noise, and the team has direct evidence of that it is underweighting.**
The `bowen-marsh → jon-snow KILLS` reject is the canary. I pulled the row:

```
source: bowen-marsh   target: jon-snow   (rejected)
hint_raw:       "For the Watch." [While stabbing Jon; tears on his cheeks]
evidence_chapter: adwd-jon-13
evidence_quote: "Snow, snow, snow." Jon shooed him off, had Satin start a fire,
                then sent him out after Bowen Marsh and Othell Yarwyck.
```

This is **Jon Snow's assassination** — one of the most important edges in the entire corpus. The
*hint* states it explicitly and correctly. The model rejected it **correctly**, because the LOCATOR
attached a completely unrelated quote ("Snow, snow, snow…") that does not support KILLS. This is not
a model failure and not a prompt failure — it is the **locator mis-pairing the evidence**, the exact
"structural candidate-noise ceiling" the prior NO-GO (gate-result.md §2) identified as NOT
prompt-fixable. smoke5 used **locator v2** and it *still* mis-located the single most important edge
in the sample.

This matters more than the 6% headline false-reject rate because it reveals the failure is
**systematic and concentrated on the highest-value edges**: dramatic, plot-pivotal actions (a murder,
a key betrayal) are exactly the rows where the prose around the action is dialogue-heavy and the
locator grabs the wrong line. The 90% reject pile is not uniformly noise — it contains an unknown
number of true, important, mis-located edges that the model is *correctly* throwing away. The team
is measuring "of my emits, how many are right" (precision) and "of a reject sample, how many were
arguable" (6%), but **nobody is measuring "of the true high-value edges in the pool, how many made
it through the locator intact."** That is the recall number that actually matters and it is unmeasured.

So: the 10% emit rate is defensible; the **silent loss of mis-located high-value edges is not
something the team has quantified**, and it has a worked example sitting in its own reject pile.

---

## 4. Blind spots — what is NOT being measured before $75

1. **Filter false-drop rate, out-of-sample.** (§1) The biggest one. The validator and quote-filter
   are *destroying* true edges (`daenerys SPOUSE_OF drogo`, `ygritte LOVES jon`, `robb HOLDS_TITLE
   north`, `queen-cersei SPOUSE_OF robert` — I confirmed all four) and the rate is being reported as
   "0 false drops" because it was measured in-sample. **Cheapest fix: run the two filters over a
   second fresh sample, pure Python, $0, and label the drops.**

2. **Locator true-edge survival rate.** (§3) What fraction of genuinely-important edges in the pool
   get a CORRECT quote attached? `bowen-marsh KILLS jon` got a wrong one. The cheapest probe: take
   ~30 *known* canonical high-value edges (assassinations, key betrothals, major kills), look them up
   in the candidate pool, and check whether the located quote actually supports them. If even half are
   mis-located, the enrichment layer's recall on the edges anyone will actually query is poor and the
   "breadth" claim is hollow.

3. **The quote-relevance filter's recall cost specifically.** I measured it: on smoke5 it dropped
   4/40, and **2 of those 4 are TRUE edges lost to pronoun/speaker-not-named artifacts**
   (`daenerys SPOUSE_OF drogo`, `ygritte LOVES jon`). That is a ~50% false-drop rate on this sample.
   The team's own `v1-refine-proposal` notes ~50.9% of v1 quotes don't name both endpoints lexically.
   **This filter should be a SOFT FLAG, not a hard drop** — applying it as a gate will shred recall.
   Confirm it is wired as soft-flag-only before the run (both prompt reviews explicitly recommended
   soft-flag; verify the production pipeline honors that).

4. **Per-table precision split.** Events (16,572) and Dialogue (4,422) are different beasts. Dialogue
   rows are likely higher-precision (a quote IS the dialogue); Events rows are where the locator has to
   guess. The smoke mixed them. **Shard the smoke too:** score Events-only vs Dialogue-only precision
   before committing. It may be that Dialogue clears 80% and Events sits at 68% — in which case run
   Dialogue, defer Events, and save both money and pollution.

5. **Cross-model drift / schema validation on the bulk.** Memory flags this as mandatory for every
   Stage 4+ bulk run. smoke5 had `conform_violations: 0` which is good, but a 21k-row run is 525×
   larger; the drift detector + schema validator must run *during* the shards with a verdict-gates-
   resumption, not just at the end.

**The single cheapest test that would change the decision:** re-run the *deterministic filters only*
(no Haiku) over a fresh second sample and have a reviewer label every DROP as true-drop/false-drop.
Pure Python, ~$0, ~30 min of reviewer time. If the filter false-drop rate is <5%, the post-filter
number is trustworthy and this is a GO. If it's the ~50% I measured on the quote-filter, the filters
must be downgraded to soft-flags first. **This test directly attacks the one circular number in the
whole readiness case.**

---

## 5. Net recommendation

**NOT-YET — but one specific, cheap thing, then GO.**

Do this before spending $75 (total cost ≈ $1.20 of Haiku + reviewer time):

1. **Measure the filters out-of-sample.** Second fresh 400-row sample (new seed), run *only* the
   deterministic validator + quote-relevance filter (no LLM), label every drop true/false. This
   gives the honest post-filter precision AND the honest false-drop rate the current case lacks.
2. **Demote the quote-relevance filter to a SOFT FLAG** (it has a confirmed ~50% false-drop rate on
   true pronoun-referenced edges — `daenerys SPOUSE_OF drogo`, `ygritte LOVES jon`). It must annotate,
   not gate.
3. **Shard the smoke by table** (Events-only vs Dialogue-only precision) so you can run the clean
   table and defer the dirty one if they diverge.
4. **Confirm the enrichment provenance tag** (`enrichment_tier`/`candidate_kind`) survives into
   `graph/edges/` so a traversal query can exclude this layer. A 72.5%-raw layer MUST be queryably
   second-class.

If steps 1–3 show post-filter precision ≥~78% **with** a measured filter false-drop rate <~8%, then
**GO** — start book-sharded, AGOT-Events first as proposed, with drift-detection live during the run.

**The single most important caveat, restated:** the reported "~80–91% post-filter" is inflated by
in-sample filter evaluation, and the deterministic filters are silently deleting confirmed TRUE edges
(I verified `daenerys SPOUSE_OF drogo`, `ygritte LOVES jon`, `robb HOLDS_TITLE north`,
`queen-cersei SPOUSE_OF robert` all dropped). Get the out-of-sample false-drop number — it's free —
before you trust the precision number or spend the $75. The `bowen-marsh KILLS jon` mis-location is
the proof that the *recall* story (not the precision story) is the real risk: the locator is mangling
the highest-value edges, and that loss is currently unmeasured.

---

### Appendix — verification commands run

```
# confirmed 40 emits / 360 rejects
cat _smoke5-haiku/run-summary.json

# type-contract validator on the 40 emits → 5 dropped (NOT 4)
python3 scripts/stage4-type-contract-validator.py --input /tmp/smoke5-emits.jsonl ...
#   CONTRACTED_WITH_object_target: 2  (correct)
#   MEMBER_OF_direction_reversed: 1   (true edge lost, reversed)
#   HOLDS_TITLE_char/location_target:1 (robb HOLDS_TITLE north = King in the North = FALSE DROP)
#   SPOUSE_OF_non_char_endpoint: 1    (queen-cersei SPOUSE_OF robert = FALSE DROP)

# quote-relevance filter on the 40 emits → 4 dropped, 2 are TRUE edges
#   daenerys SPOUSE_OF drogo  (UNMATCHED_BOTH — pronouns)   = FALSE DROP
#   ygritte LOVES jon-snow    (UNMATCHED_SOURCE — speaker not named) = FALSE DROP
#   doran TRAVELS_TO volantis, roelle REVEALS_TO brienne    = defensible drops

# bowen-marsh KILLS jon assassination, rejected on a mis-located quote
grep '"For the Watch' _smoke5-haiku/adwd/adwd-tail.rejected.jsonl
```
