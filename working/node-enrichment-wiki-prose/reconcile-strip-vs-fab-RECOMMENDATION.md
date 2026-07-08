# Reconciling the boilerplate strip and the Fire & Blood merge-writer — recommendation

> **Status:** read-only analysis. Nothing applied, no script edited, no node touched, worklog.md untouched.
> **Author's note on scope:** this document answers the ordering-collision question posed in
> `reconcile-strip-vs-fab-analysis-prompt.md`. It does not implement anything — Matt decides, a later
> session implements.

## Verdict up front

**Recommend Option B: patch `scripts/fab_merge_node.py`'s boilerplate shape-detection** (it is still
apply-gated and has never run for real) so it recognizes a stripped-tail Identity line as
swap-equivalent and an empty `## Identity` section as insert-equivalent. This restores **true**
order-independence — neither track has to know about, wait for, or sequence itself relative to the
other, ever again — and it does not block the strip for even one day. Ship the strip now.

Two numbers carry this recommendation:

1. **1,108** — of F&B's own deterministic target-set proxy (the 1,526-node candidate-pack union, built
   from existing wiki `Rfab*` cite anchors), only 1,108 nodes currently carry a boilerplate Identity line
   that matches F&B's exact regex today. That's the *real* stakes, not the graph-wide 5,632 theoretical
   max quoted in the analysis prompt (5,632 is 6 out of every 7 boilerplate nodes graph-wide; F&B will
   only ever plausibly touch 1 in 6 of them).
2. **0** — the number of Identity-line swaps F&B's reconciler (`scripts/fab-reconcile-candidates.py`)
   currently emits, on any unit, including the one completed smoke unit. `identity_line` is not wired
   up anywhere in the reconciler's `merge_plan.append(...)` call (verified by reading the code — see
   §2.3). The collision this whole analysis is about is **currently inert** in the real pipeline; it
   only becomes live once someone builds the (currently-missing) step that derives a book-grounded
   Identity sentence and threads it into `merge-plan.json`.

Given a real stakes-ceiling under 20% of the theoretical max, a collision mechanism that doesn't exist
in the pipeline yet, and an F&B apply-go that is several gated sessions away, blocking a ready,
Matt-approved, zero-risk script (Option A) is the wrong trade. Patching F&B's own shape-detection
(Option B) is cheaper than the coordination overhead of any scheme that keeps the two tracks aware of
each other (Option C), and it's a natural fit for a script that's already mid-fix this same week (S199).

---

## 1. Spot-verifying the load-bearing facts (done as a full deterministic count, not a sample)

Rather than eyeballing a handful of rows, I re-ran the exact regexes from both scripts over the live
`graph/nodes/` tree and got numbers that match the analysis prompt's "confirmed collision" section
**exactly**:

| | rich (5,490) | thin (1,221) | total (6,711) |
|---|---|---|---|
| currently match F&B's `BOILERPLATE_RE` | **4,682** | **950** | **5,632** |

- `scripts/strip-wiki-boilerplate.py`'s `BOILERPLATE_LINE_RE` = `^(.*?) (is an? )(.+?) from the AWOIAF wiki\.$` — any gloss text, "is a"/"is an" both handled. This is the **broader, correct** detector (it's what actually matches the generator's real output).
- `scripts/fab_merge_node.py`'s `BOILERPLATE_RE` = `^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$` — hardcodes "is a " (not "is an ") and restricts the gloss to lowercase letters + dots only, no spaces/slashes/parens. This is why it **already misses 808 rich + 271 thin nodes today**, independent of the strip (e.g. `"House Ambrose is a noble house from the AWOIAF wiki."` never matched F&B's regex, strip or no strip — "noble house" has a space).
- One rich example, spot-checked: `graph/nodes/houses/house-antaryon.node.md` — `"House Antaryon is a organization.house from the AWOIAF wiki."` → strip produces `"House Antaryon is a organization.house."`; this no longer contains the literal substring `"from the AWOIAF wiki"` at all, so it drops out of F&B's regex (and out of the strip's own `grep -rl` re-scan — confirming the "0 nodes have it twice" claim: once a line changes shape, neither script's boilerplate detector fires on it again).
- One thin example: `graph/nodes/prophecies/the-song-of-ice-and-fire.node.md` — thin-drop leaves `## Identity` with no line under it. `fab_merge_node.get_identity_line()` returns `(None, -1, -1)` for that section text; `process_entry`'s `if line_text is not None and BOILERPLATE_RE.match(...)` is false (because `line_text` is `None`), so control falls to `else: identity_action = "left_alone_real_identity"` — **confirmed**, this is a real bug independent of whether it was caused by the strip: the code has no branch for "section header present, no content line."
- The 46-content-bearing-nodes-misclassified-as-thin nit: independently re-counted at **46** (27 `## Heraldry & Sigil`, 15 `## Culture`, 4 `## Aftermath` by my count vs. the prompt's 27/15/6 — trivial counting-method variance, the total matches exactly). Doesn't change the ordering question; noted for whoever eventually fixes the strip's `RICH_SECTIONS_RE` allowlist.
- Reverse order (strip-after-F&B) is confirmed structurally safe: F&B's swap replaces the whole line with book-grounded prose containing no `"from the AWOIAF wiki"` substring, so the strip's own `grep -rl` scan will never re-select that file.

**Conclusion: the prompt's "confirmed collision" facts are accurate as stated.** The theoretical-max
5,632 is real. The question is how much of it F&B will ever touch.

## 2. Quantifying the true stakes

### 2.1 F&B's target-set proxy: the candidate-pack union

F&B's target set isn't materialized yet (1 of 23 candidate-packs has a real reconcile run), but there
*is* a solid deterministic proxy for it: `scripts/fab-build-candidate-packs.py`'s output
(`working/fire-and-blood/candidate-packs/fab-*.json`), built by scanning every node's existing wiki
`cite_ref-Rfab<section>` anchors — this is data the wiki itself already encodes (1,634 nodes carry at
least one such anchor), not a guess. Union across all 23 packs:

```
union of expected_slugs across all 23 packs: 1,526
```

This matches the design doc's own count (`working/fire-and-blood/fire-and-blood-enrichment-design.md`
§5.0: "1,526 nodes mapped") and worklog S198's session entry, so it's a stable, cross-checked number.

### 2.2 Intersecting the two target sets

Joining the 1,526 candidate-pack slugs against the current live boilerplate state of `graph/nodes/`:

| | count |
|---|---|
| candidate-pack union (F&B's real touch-set proxy) | 1,526 |
| … of those, currently carry *any* boilerplate Identity line | 1,302 |
| … of those, currently match F&B's exact `BOILERPLATE_RE` (**the real ordering-collision stakes**) | **1,108** |
| … broken down: rich | 1,106 |
| … broken down: thin (the undesigned-4th-shape risk, *within F&B's actual scope*) | **2** |

So: **1,108 of 6,711** boilerplate nodes graph-wide (16.5%) — and **1,108 of the 5,632** theoretical-max
strip/F&B collision set (19.7%) — are nodes F&B might plausibly touch. The other 80%+ of the strip's
sweep is houses, locations, artifacts, foods, titles, species, chapters, etc. that F&B's
Targaryen-history-only scope will never reach. And within F&B's real scope, the "4th shape" (empty
Identity section after a thin-drop) is a **2-node** problem, not a 950-node one — reassuring, but the
underlying code bug is still real and still worth fixing (§2.1).

**Caveat, stated directly (per the analysis task's instruction to reason under uncertainty):** the
candidate-pack union is a *superset* proxy — "this node's wiki prose cites an Rfab anchor in this
section" is necessary but not sufficient for "the reconciler will route this node to an Identity swap."
The one completed smoke unit is concrete evidence of how much smaller the true touch-set is (next
section) — so 1,108 should be read as a **ceiling**, not an estimate of the eventual real count.

### 2.3 The concrete evidence — and the more important finding

The smoke unit `fab-aegons-conquest-03` is the only unit with a real reconciler run
(`working/fire-and-blood/smoke/v1/recon-after/`, post-S199-fix). Its candidate pack lists 111 nodes;
its actual `merge-plan.json` has **14 entries**. So in the one real data point available, only ~13% of
a pack's listed nodes end up as merge-plan candidates at all — reinforcing that 1,108 overstates the
true touch-set by a wide margin.

But reading `scripts/fab-reconcile-candidates.py`'s merge-plan construction (lines 1074–1096) surfaces
something more load-bearing than the count:

```python
merge_plan.append({
    "slug": slug,
    "fab_section_md": "\n".join(lines_md),
    "run_id": run_id,
})
```

**There is no `identity_line` key anywhere in this script.** `grep -n "identity_line" scripts/fab-reconcile-candidates.py`
returns nothing. The reconciler only ever populates `fab_section_md` (the `## Fire & Blood` prose
block); it never derives a short book-grounded Identity sentence from the extraction's `## Node Prose`
table and never sets `identity_line`. Confirmed on the live smoke output: all 14 `merge-plan.json`
entries for `fab-aegons-conquest-03` have `identity_line` absent.

`fab_merge_node.py`'s own logic treats a missing `identity_line` as "leave the boilerplate line alone"
(`identity_action = "boilerplate_line_but_no_identity_line_provided_left_alone"`). So **today, running
F&B's real pipeline end-to-end performs zero Identity-line swaps, strip or no strip.** The
Identity-upgrade half of F&B's stated purpose (design §1: *"upgrades the graph's existing wiki-derived
Targaryen-history layer to Tier-1 book-cited provenance"* — the Identity-line half of that, as opposed
to the `## Fire & Blood` section append, which *does* work today) is simply unbuilt. It isn't in the
5-item S199 fix list (`progress/continue-prompts/2026-07-07-fire-and-blood-reconciler-fix-stage2.md`)
either — those fixes are CREATE-routing, composite-splitting, quote-locating, contradictions, and
type-guessing, none of them Identity-line derivation.

This doesn't mean the collision is fake — the design doc clearly intends the swap (§5.3 step 2,
Fable-ruling §11 #1), and it would be a real gap in F&B's stated goal if that capability never lands.
It means **the runway before the collision can happen in practice is longer than "F&B's apply-go"** —
someone still has to build identity_line derivation first. That's more time, not less, for the strip
to sit blocked under Option A.

## 3. Weighing timing

The strip is a single Python script, dry-run-clean, Matt-approved, zero external dependency. It could
apply today.

F&B's remaining runway to its *first* real apply (per `worklog.md` S198/S199 and the S199 continue
prompt) is: reconciler fix (in progress) → re-run reconcile on the smoke unit → Stage-2 smoke
(`fab-heirs-of-the-dragon-15`, Matt-fired from iTerm) → judge quality/disputed-tagging → tune §5.1
auto-accept thresholds → validate on ≥2 **fresh, out-of-sample** units → *then* Matt's apply-go (which
also lands the architecture.md batch) → *then* the actual bulk run across the remaining ~34–40 units
under `longrun.sh` (§9: "an overnight-ish background run," incremental, `LONGRUN_SLEEP_BETWEEN`
1200–1800s). And as shown in §2.3, identity_line derivation — the actual source of the collision —
isn't even scoped yet within that runway.

Sequencing the strip after F&B (Option A) means picking one of two bad waits:
- Wait for F&B's *entire* bulk run to finish applying (all ~34–40 units) before the strip can safely
  sweep "the untouched remainder" — a multi-session, likely multi-week wait for a script that's ready
  now — or
- Run the strip after each unit's apply on just that unit's untouched remainder, repeated ~34–40 times,
  which is real recurring process overhead for a track billed as "cheap, one Python script."

Either way, "the remainder" is a moving target exactly as the analysis prompt warned, because F&B is
incremental, not atomic.

## 4. Evaluating the options

**(A) Sequence — F&B's first apply before the strip.**
Zero code. Provably safe in the narrow sense (once F&B has actually swapped a line, the strip will
never re-touch it). But: blocks a ready, zero-risk, Matt-approved script for a wait measured in
multiple gated sessions (§3), the "remainder" is a moving target under an incremental bulk run, and it
buys safety for a collision that (per §2.3) doesn't have a live trigger yet anyway. **Rejected as the
primary path** — the cost is real and ongoing; the benefit is deferred and, on current evidence, small.

**(B) Patch F&B's shape-detection.** ★ **Recommended.**
`fab_merge_node.py` has never run for real (design doc: "apply-gated, so no rework" needed) and is
already mid-revision this same week (S199 reconciler fixes land in its sibling script). Two small,
testable changes:
1. Recognize a **stripped-tail** Identity line as swap-equivalent, in addition to the original
   wiki-tail line. Cheapest, safest implementation: reuse `strip-wiki-boilerplate.py`'s own
   `BOILERPLATE_LINE_RE` (which is already the *correct*, broader detector — see §1) to recognize the
   pre-strip form, and match the **closed list of ~31 known type-gloss strings** (`character.human`,
   `location`, `noble house`, `event.battle`, `artifact (named weapon, ship, or object)`, … — enumerable
   from `working/node-enrichment-wiki-prose/strip-boilerplate-dryrun.md`'s type-gloss table, or
   regenerated deterministically) against `"<name> is a/an <known-gloss>."` for the post-strip form.
   A closed-vocabulary match is precise — it cannot accidentally swap a genuine short prose Identity
   sentence, because real prose won't equal one of the ~31 known gloss strings verbatim.
2. Add the missing branch for the **empty-but-present `## Identity` section** (§1's thin-node bug,
   independently real, not caused by the strip): when `identity_span` is found but `get_identity_line`
   returns `None`, and an `identity_line` is provided, insert it into the existing empty section
   (do not duplicate a new `## Identity` heading, unlike the true no-section case).
3. **Bonus, same surface, same regex reuse:** switching to `strip-wiki-boilerplate.py`'s broader
   `BOILERPLATE_LINE_RE` for the *original* wiki-tail case also closes the pre-existing 808-node
   freeform-gloss gap (§1) that F&B's narrow regex misses today, strip or no strip.

This restores **true** order-independence — `fab_merge_node.py` no longer cares what the strip did or
didn't do, so nobody has to remember a sequencing rule, and the strip ships unblocked today. It is the
smallest possible change that closes both the ordering hazard and two adjacent, independently-real bugs
in the same script, at the same time it's already being touched.

**(C) Make the strip F&B-aware (skip F&B's target nodes).**
Also cheap in isolation, but structurally worse than B: it couples a finished, ready-to-ship,
deterministic script to another track's **not-yet-materialized, still-being-fixed** target list. Per
§2.3, the candidate-pack union over-defers by roughly 8× relative to what the reconciler actually
routes to UPDATE (111 pack nodes → 14 real merge-plan entries on the one measured unit), so a
pack-based skip-list would leave ~1,500 otherwise-safe nodes un-stripped for the full multi-week F&B
runway for no real benefit. It also doesn't fix the pre-existing 808-node regex gap or the empty-section
bug, and it re-creates exactly the "who runs first" coordination cost the analysis is trying to
eliminate — the skip-list itself has to be kept in sync with a moving-target pack file. **Rejected.**

**(D) A better option?** Not found. B is a strict improvement over both A (unblocks today) and C
(no coupling, fixes more bugs, smaller diff).

## 5. Recommendation, implementation sketch, and what would change the answer

**Ship the strip now** (`scripts/strip-wiki-boilerplate.py --apply`, Matt's go already given per the
docstring) — it is not actually blocked by anything live in the F&B pipeline today (§2.3).

**Patch `scripts/fab_merge_node.py`** (small, testable, does not need to happen before the strip ships —
but should land before F&B's reconciler is extended to emit `identity_line`, since that's the moment
the dormant collision goes live):

- Add the closed-vocabulary post-strip detector + reuse `strip-wiki-boilerplate.py`'s broader
  `BOILERPLATE_LINE_RE` for the pre-strip form (§4.B.1/.3).
- Add the empty-section insert branch (§4.B.2).
- Test cases (extend the existing `scripts/test-fab-reconcile.py`-style fixture pattern):
  1. Rich node, original wiki-tail boilerplate + `identity_line` → swapped (regression).
  2. Same node, **pre-stripped** (`"X is a organization.house."`) + `identity_line` → swapped (new).
  3. Thin node, **pre-stripped-and-dropped** (empty `## Identity` section) + `identity_line` →
     inserted into the existing section, no duplicate heading (new — closes the 4th-shape bug).
  4. Rich node with a pre-existing **freeform-gloss** original boilerplate (`"noble house"`,
     `"artifact (named weapon, ship, or object)"`) + `identity_line` → swapped (new — closes the
     808-node gap).
  5. Rich node with **real, non-boilerplate** prose Identity → left alone (regression / false-positive
     guard — the closed-vocabulary match must not fire on genuine prose).
  6. No-`## Identity`-section node (shape c) → unchanged insert-new-section behavior (regression).
  7. Idempotency: same `run_id` applied twice → second run no-op (regression).
  8. **The actual order-independence proof:** run strip→merge and merge→strip on two copies of the same
     fixture set; assert byte-identical final output regardless of order.

**What would change this answer:** if F&B's real touch-set (once more than 1/23 packs are reconciled)
turns out to be far larger than the 1,108-node ceiling — e.g. if the reconciler's routing logic changes
such that most candidate-pack members really do get merge-plan entries, not the ~13% seen on the one
measured unit — the *stakes* argument in §2 weakens, but the *recommendation* doesn't change: Option B
is still cheaper and structurally better than A or C regardless of the collision's eventual size, because
it eliminates the hazard rather than routing around it. The one fact that would actually flip the
recommendation toward Option A is if `fab_merge_node.py` had *already run for real* against production
nodes — it hasn't (confirmed: no real apply has happened; the design doc and worklog both describe it
as smoke-tested on copies only), so "no rework" genuinely holds.

## Drift flagged against worklog.md

Per the task's instruction to trust `worklog.md` and flag disagreements: **worklog.md's own Session 197
entry is the source of the now-disproven "parallel-safe" claim.** It reads: *"Boilerplate-strip cleanup
(independent, deterministic): … Safe to run alongside S198."* The `2026-07-06-strip-wiki-boilerplate-identity.md`
continue prompt inherits the same framing in its header (*"Track: graph cleanup (parallel-safe with the
F&B build track — touches different code/nodes)"*). Both were written before the follow-up review
(`progress/continue-prompts/2026-07-07-verify-boilerplate-strip-safe.md`) established that the two
tracks are **not** order-independent as originally built. This document (and the analysis prompt it
answers) supersede that S197 framing; worklog.md should be corrected at the next session that touches
either track, to note the collision was found and reconciled via Option B rather than carrying the
stale "parallel-safe" claim forward.
