# Events Haiku Bulk Run — Analysis & Promotion Plan

**Date:** 2026-05-29
**Source dir:** `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/`
**Wrapper:** `scripts/stage4-events-bulk-run.sh` (counting bug patched in this session)
**Final run id:** `tail-llm-20260529T011614` (ran 282 batches over ~16h, 2026-05-29)

## 1. Completeness

Run is **complete** across all 5 books. The "stuck on 2900 rows" stop message at the end was a wrapper-side counting bug (total counted raw rows, done-set deduped by `(src, tgt, chapter)`; the 2,900 phantom rows are duplicate input keys). Bug patched in `scripts/stage4-events-bulk-run.sh::count_remaining`.

| Book  | Input rows | Emits | Rejected | needs-qual | Sum check |
|-------|-----------:|------:|---------:|-----------:|:---------:|
| agot  |      2,664 |   236 |    2,428 |          0 | ✓         |
| acok  |      3,185 |   387 |    2,798 |          0 | ✓         |
| asos  |      4,368 |   414 |    3,954 |          0 | ✓         |
| affc  |      2,789 |   239 |    2,549 |          1 | ✓ (with NQ) |
| adwd  |      3,496 |   341 |    3,155 |          0 | ✓         |
| **Total** | **16,502** | **1,617** | **14,884** | **1** | ✓ |

Reject rate ≈ 90.2% (consistent with validation gates throughout: `reject_rate=0.907` at last check).

## 2. Cost & runs

- Final segment cost: **$34.13** (11,263 rows, claimed by run `T011614`)
- Plus prior partial segments (`T194340`, `T203255`, `T233748`) that contributed 554 of the 1,617 emits
- **Single prompt:** all 1,617 emits used `prompt_version=v5-precision-rules`, `prompt_sha=d31ca56c4768` → drift-clean across all contributing runs
- **Single model:** all 1,617 typed by `haiku`
- **0 conform_violations**, **0 classify_failed**, **1 needs_qualifier**

## 3. Edge-type distribution

100 distinct edge types emitted. Top events-shaped predicates lead, as expected:

| Edge type        | Count | Share |
|------------------|------:|------:|
| TRAVELS_WITH     |   127 |  7.9% |
| COMMANDS         |   121 |  7.5% |
| TRAVELS_TO       |   115 |  7.1% |
| LOCATED_AT       |    90 |  5.6% |
| SERVES           |    84 |  5.2% |
| OPPOSES          |    67 |  4.1% |
| REVEALS_TO       |    66 |  4.1% |
| SIBLING_OF       |    49 |  3.0% |
| ATTACKS          |    43 |  2.7% |
| SEEKS            |    39 |  2.4% |
| (long tail)      | 916   | 56.6% |

Per-book top-3 matches book-internal narrative shape:
- **agot**: TRAVELS_WITH, ATTACKS, SIBLING_OF (Stark family + early war)
- **acok**: COMMANDS, SERVES, OPPOSES (full war)
- **asos**: COMMANDS, TRAVELS_TO, TRAVELS_WITH (Red Wedding armies on the move)
- **affc**: TRAVELS_TO, LOCATED_AT, TRAVELS_WITH (Brienne wandering, Sansa at Eyrie)
- **adwd**: TRAVELS_WITH, COMMANDS, TRAVELS_TO (Tyrion/Quentyn travelogues)

## 4. Schema-field health

- **`confidence_tier`**: tier 1 = 256, tier 2 = 1,342, tier 3 = 19. Real calibration (unlike v1's all-tier-1).
- **`locate_status`**: verbatim 1,610 / chapter-level 7 → 99.6% verbatim. Quote-relevance is strong.
- **`qualifier`**: 170/1,617 = 10.5% — modest, qualifiers are optional but valuable.
- **`evidence_kind`**: all 1,617 = `book-pass1` ✓
- **`typed_by`**: all 1,617 = `haiku` ✓
- **`prompt_version` / `prompt_sha`**: identical across all rows ✓

## 5. Known schema gap (NOT a blocker)

Rejected rows carry **no `reject_reason` field** — only `decision: rejected` + the input hint. So we can't do quantitative rejection-cause analysis. Sample inspection shows rejects are mostly real "no clean type fits" cases (e.g., "Arya quotes Jon about Joffrey"); a few might be over-conservative but the rate looks reasonable.

For future bulk runs: consider adding `reject_reason` to the classifier output schema (e.g., `not-in-vocab`, `no-relation-asserted`, `incomplete-evidence`).

## 6. Overlap with existing `graph/edges/edges.jsonl` (v1.3, 3,811 edges)

| Granularity                 | Existing | New (events) | Overlap |
|-----------------------------|---------:|-------------:|--------:|
| Pairs (src, tgt)            |    2,461 |        1,039 |     444 |
| Triples (src, type, tgt)    |    3,734 |        1,277 |     289 |
| Quads (src, type, tgt, qual)|    3,811 |        1,286 |     278 |

**Net-new contribution if promoted: ~988 unique triples / ~1,008 unique quads.**

The 444 pair-overlaps are additive (same characters, different facts) — these aren't conflicts, they're enrichment of known pairs with new event-shaped predicates.

### Net-new triples by edge type (top 20)

| Edge type    | Net-new |
|--------------|--------:|
| TRAVELS_TO   |     105 |
| TRAVELS_WITH |     103 |
| LOCATED_AT   |      71 |
| COMMANDS     |      59 |
| REVEALS_TO   |      58 |
| ATTACKS      |      39 |
| OPPOSES      |      35 |
| DREAMS_OF    |      33 |
| SERVES       |      33 |
| SEEKS        |      18 |
| DISTRUSTS    |      18 |
| MEMBER_OF    |      17 |
| SIBLING_OF   |      16 |
| RESCUES      |      14 |
| HOLDS_TITLE  |      13 |
| RULES        |      13 |
| KILLS        |      12 |
| APPOINTS    |      12 |
| TRUSTS       |      12 |
| PARENT_OF    |      12 |

This is exactly the v2 enrichment the `graph/edges/README.md` roadmap calls out:

> **v2 — enrichment:** Events + Dialogue tables typed by Haiku (locked-down prompt, Rule 11 anti-pattern gates), precision-filtered, layered on top.

The Dialogue half is still pending; Events half is now ready to layer.

---

## 7. Promotion plan

### 7.1 Where the data goes

`graph/edges/edges.jsonl` is currently the consolidated v1.3 layer, built by `scripts/stage4-formalize-edges.py` from three sources:

1. **SPINE** — `pass1-derived/{book}/*.edges.jsonl`
2. **S67 TAIL** — `pass1-derived/_tail-typed/{book}/*.jsonl` (Sonnet)
3. **HOSPITALITY** — extra-tables hospitality rows

The Events Haiku bulk output lives in `_events-haiku-bulk/{book}/*.edges.jsonl` and constitutes a **fourth source**. The wrapper's own log notes the canonical location is `_tail-typed/` but it was redirected to `_events-haiku-bulk/` for this run to avoid co-mingling with S67 Sonnet output.

### 7.2 Required steps (in order)

1. **Drift-detection audit** (memory rule `feedback_drift_detection_mandatory`). Before promotion:
   - Mechanical schema validator: confirm all 1,617 emits parse against `pass1-derived-v1` schema. (Already strong: 0 conform_violations in run output.)
   - Cross-model sample audit: pull a stratified ~50-row sample, have a fresh general agent (or Sonnet) re-type with the same v5-precision-rules prompt; compute agreement rate. Floor for go: ≥70% triple-level agreement, ≥85% pair-level. (Same gates the validation step used during the run.)
   - **Decision gate:** only proceed past this if audit passes.

2. **Extend `stage4-formalize-edges.py` to add a fourth source: EVENTS-HAIKU.**
   - Read from `_events-haiku-bulk/{book}/*.edges.jsonl` instead of (or in addition to) `_tail-typed/{book}/*.jsonl`.
   - Tag with `source_set: events-haiku` (new value alongside spine/tail/hospitality).
   - Run through the same merge → endpoint-gate → dedup → precision-filter pipeline as v1.
   - Output to staging `_formalized/edges-v2.jsonl` (do NOT overwrite v1).

3. **Type-contract validation.** Run the same contract checks that produced v1.2 (the −17-edge fix). The new types likely to fail in unexpected ways:
   - TRAVELS_TO target must be a place
   - LOCATED_AT target must be a place
   - REVEALS_TO target must be a character
   - COMMANDS target: character or faction (we know this from v1.2)
   - Any new edge type that wasn't in v1's contract map needs a contract row added.

4. **Resolver pass.** Re-run `stage4_name_resolver.py` on the v2 candidate to catch any new title-person collisions (e.g., new `lord-tywin` ships, new `princess-myrcella` references).

5. **Precision-filter pass.** Sample-audit the merged v2 candidate at the same effort as v1 (200-row reviewer audit). If precision >= ~75% triple-level, ship as v2.0.

6. **Promote.** Replace (or extend) `graph/edges/edges.jsonl` with `edges-v2.jsonl`; update README with v2 build lineage; commit.

### 7.3 Open questions for Matt (before step 2)

- **Replace v1.3 entirely, or layer additively?** Two options:
  - (a) Full re-merge: rebuild from SPINE + S67 TAIL + HOSPITALITY + EVENTS-HAIKU, dedup all four sources together → one consolidated v2 jsonl.
  - (b) Additive overlay: keep `edges.jsonl` (v1.3) as-is, write `edges-events-v2.jsonl` next to it, treat as a sibling layer.

  Recommendation: **(a) full re-merge.** It's what `formalize-edges.py` is shaped for, it dedups overlaps cleanly, and the v2 README already implies a layered single file. (b) creates a query-time problem ("which file owns this edge?") with no real upside.

- **Dialogue source: in or out for this push?** README roadmap pairs Events + Dialogue as v2 together. We could:
  - Ship Events-only as v2.0 now, Dialogue arrives as v2.1, OR
  - Wait for Dialogue to complete and ship both as v2 together.

  Recommendation: **ship Events-only as v2.0.** Dialogue is a separate bulk run we haven't done yet; gating Events promotion on it adds weeks of latency for no precision benefit.

- **`reject_reason` schema gap fix-now or fix-later?** Adding it requires a classifier-script edit + would invalidate the existing 14,884 rejects (no reason captured). Recommendation: **fix-later**, in the Dialogue run prep.

## 8. Recommended next action

Run the **drift-detection cross-model audit** before any promotion work. That's the next item gated on Matt's go/no-go for which audit form (fresh general agent vs. Sonnet reclassification) and sample size.

If the audit clears, the formalize-edges.py extension is a ~1-hour script edit + dry-run + commit.
