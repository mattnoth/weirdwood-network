---
session_date: 2026-05-16
session_focus: Stage 4 bulk run — 7 Sonnet batches; regression in batch-0018 surfaced patch limits
status: PAUSED — bulk firing stopped after batch-0018 quality regression; needs prompt strengthening before resuming
verdict: YELLOW — first 6 batches CLEAN under patches; batch-0018 shows CONTEMPORARY_WITH-fallback recurrence in dense kinship buckets
model_used: claude-opus-4-7[1m] (orchestrator); claude-sonnet-4-6 (workers)
companion_docs:
  - 2026-05-15-stage4-batch-0012-quality-check.md
  - 2026-05-15-stage4-edge-provenance-explained.md
  - 2026-05-15-stage4-haiku-smoke-verdict.md
---

# Stage 4 Bulk Run — 5-Batch Checkpoint

## Status

**Green. Bulk run proceeding cleanly.** Five Sonnet batches launched sequentially with ~60s sleeps between them (batch-0016 still in flight at write time). All four completed batches passed the validator on the first or second pass. Type discipline holding at 0-3% (well within the 3.9% Sonnet baseline). Cross-identity escalations working. Two new failure modes discovered in batch-0014 were patched into the classifier prompt + worker template mid-run; batch-0015 (first batch under the patches) ran cleanly with zero recurrence.

Mission manifest: **15 done / 186 queued** (was 12/189 at session start).

## Per-batch results

| Batch | Wall | emit | reject | escalate | tier-1/2/3 | distinct types | validator | type-contract | notes |
|---|---|---|---|---|---|---|---|---|---|
| 0012 | 18 min | 63 | 282 | 2 | 59/3/1 | 18 | CLEAN | 1.6% | Canonical re-run; cross-identity caught |
| 0013 | 17 min | 152 | 276 | 0 | 118/30/4 | 17 | CLEAN | 0.0% | Self-corrected 3 non-canonical types during run |
| 0014 | 28 min | 170 | 459 | 0 | 148/21/1 | 23 | CLEAN | 2.9% | **Discovery: CONTEMPORARY_WITH-as-fallback (14×) + reverse-direction vocab gaps (CHILD_OF, HOSTED_BY, RESURRECTED_BY)**; 7 vocab gaps filed; self-corrected 97 non-canonical types |
| 0015 | 22 min | 116 | 355 | 1 | 101/15/0 | 27 | CLEAN | 7.8%* | **CONTEMPORARY_WITH: 0** (patch worked); 0 reverse-direction vocab gaps; 0 vocab gaps total |
| 0016 | 17 min | 119 | 205 | 1 | 100/18/1 | 18 | CLEAN | 6.7%† | First batch under codified prompt patches; CONTEMPORARY_WITH: 0; 1 vocab gap (DEPICTED_IN — character-as-subject-of-in-world-text); 3/3 KILLED_BY correct |
| 0017 | 21 min | 128 | 398 | 0 | — | 26 | CLEAN | 5.5%‡ | 0 vocab gaps; 4/4 KILLED_BY correct; year-page typing bug (`209-ac` typed character.human) correctly rejected by worker |
| 0018 | 25 min | 132 | 640 | 0 | 113/19/0 | — | CLEAN | 6.1% | **REGRESSION**: CONTEMPORARY_WITH count 21 (was 0 in prior 3 batches under patches); Frey-density bucket; KILLED_BY 2/2 possibly miscoded; 1 vocab gap (COUSIN_OF — legit) |
| 0019 | 24 min | 74 | 575 | 0 | 71/3/0 | — | CLEAN | 0.0% | First under strengthened prompt + 7 new vocab types; CONTEMPORARY_WITH: 0; 5/5 KILLED_BY correct; Frey buckets handled cleanly; **schema-drift episode mid-run** — worker initially emitted with missing fields + `notes` instead of `reason`; validator caught it; worker wrote post-hoc repair script. Acceptable bookkeeping outcome but signals the prompt still isn't pinning hard enough |
| 0020 | 31 min | 437 | 314 | 0 | 320/108/9 | 15+ | CLEAN | 3.2% | **NEW soft-fallback: KNOWS at 163 emits (37%)**; 6 ATTENDS-person recurring; 3 wrong-attribution KILLED_BY (Ethan Glover at Tower of Joy ascribed to each of 3 Kingsguard individually); 27 COUSIN_OF (new vocab working); schema-repair episode (4 emit-with-reason, FOUGHT_IN→FIGHTS_IN, DIES_AT→DIED_AT); CONTEMPORARY_WITH 0 |
| 0021 | 12 min | 60 | 196 | 0 | 55/5/0 | 20+ | CLEAN | 0.0% | First WAVE under strengthened prompt; CONTEMPORARY_WITH: 0; 1/1 KILLED_BY correct; 0 vocab gaps; Goodbrother/Grafton/Graceford/Grandison buckets — model behaved exactly as patched |

*batch-0015's 7.8% is mostly graph-typing mismatches (kingsmoot typed as `concept.culture` rather than event; trial-by-combat as `concept.custom`), not classifier errors — real Sonnet error rate ~2-3%.

†batch-0016's 6.7% also dominated by kingsmoot-typed-as-culture (3 of 8). Real classifier errors ~4%: a few FIGHTS_IN-when-should-be-ALLIES_WITH (`franklyn-farman FIGHTS_IN aegon-targaryen-son-of-aenys-i` should be SERVES/ALLIES_WITH), TRAVELS_TO-with-person-target, FIGHTS_IN-with-place-target-when-should-be-SIEGE-event. Recurrent enough that a graph-side normalization (re-type kingsmoot as `event.assembly`, trial-by-combat-of-tyrion as a specific event) would silence the false positive.

‡batch-0017's 5.5% are mostly real classifier errors (no graph-typing dominance this time): two recurring patterns — `FIGHTS_IN <person>` ("X fought alongside Y in the battle" — should be FIGHTS_IN <battle>, ALLIES_WITH <person> as two separate edges) and `ATTENDS <person>` ("X attended the wedding of Y" — should be ATTENDS <wedding-event>). Worth adding a prompt patch on next iteration: when prose says "attended the wedding of A and B", emit ATTENDS the wedding event, not the persons.

## batch-0018 regression — analysis

batch-0018 processed Frey buckets (characters-house-frey-a-e, characters-house-frey-e-m) which have dense kinship + dense intra-house political conspiracy. The CONTEMPORARY_WITH-as-fallback failure mode RESURFACED at 21 emits, after 3 consecutive batches at 0 emits. Audit of all 21:

- **18 of 21 are clearly fallback misuse**, not genuine peer-of-era assertions. Examples:
  - `cersei-frey CONTEMPORARY_WITH robb-stark` (snippet: "presented to Robb Stark when he arrives at the Twins" — should be BETROTHED_CANDIDATE / OFFERED_AS_BRIDE — not in vocab; should reject or file gap, not fallback)
  - `hosteen-frey CONTEMPORARY_WITH wyman-manderly` (snippet: "Hosteen accuses Lord Manderly" — should be OPPOSES)
  - `lothar-frey CONTEMPORARY_WITH roose-bolton` (snippet: "one of the prime engineers of the Red Wedding... with Roose" — should be ALLIES_WITH or CONSPIRES_WITH — gap)
  - `lothar-frey CONTEMPORARY_WITH hoster-tully` ("participates in the funeral of Hoster Tully" — should be ATTENDS-the-funeral-event, not contemporary)
  - `kyra-frey CONTEMPORARY_WITH red-wedding` ("During the Red Wedding, Sandor kills Kyra's brother" — should be ATTENDS or SIBLING_OF-the-victim)
  - `lord-frey CONTEMPORARY_WITH second-blackfyre-rebellion` ("It is not known what punishment Lord Frey suffered for his part" — should be FIGHTS_IN the rebellion)
- **2-3 are borderline-acceptable** (e.g. `aenys-frey CONTEMPORARY_WITH robett-glover` could be co-prisoners or peers).
- **0 are clearly genuine peer-of-era assertions.**

**Type-contract: 6.1%** with the recurring patterns continuing:
- `ATTENDS aenys-frey -> ramsay-snow` (person target, should be event)
- `FIGHTS_IN aenys-frey -> stannis-baratheon` (person target, should be event)
- `ATTENDS amerei-frey -> edmure-tully` (person target — should be the wedding event)
- `TRAVELS_TO cleos-frey -> eddard-stark` (person, not place)

**KILLED_BY** (2 edges, both possibly miscoded):
- `aegon-frey-son-of-stevron KILLED_BY brotherhood-without-banners` — snippet talks about Merrett Frey being hanged; whether the brotherhood specifically killed Aegon (the source) needs cross-check
- `cleos-frey KILLED_BY brave-companions` — Cleos was actually killed by outlaws on the road BEFORE the Brave Companions captured Jaime+Brienne; this attribution looks wrong

### Why the patches didn't hold in this bucket

The CONTEMPORARY_WITH patch in the classifier prompt is one paragraph deep in a long document. When the worker is processing a dense kinship bucket (Frey is the densest house in ASOIAF — Walder has 100+ descendants), the cognitive load of "find the right canonical type" goes up sharply and the worker reaches for fallbacks more readily. The patch reduces the rate but doesn't eliminate it under high-load buckets.

The COUSIN_OF vocab gap (legitimately filed by the worker) is part of the underlying pressure: many Frey relationships are cousin/uncle/aunt patterns that the worker has no canonical type for, so reaches for CONTEMPORARY_WITH instead of rejecting.

## Decision: pause and reassess

Stopping the firing cadence after batch-0018. Reasons:
1. CONTEMPORARY_WITH-fallback failure mode has demonstrated regression-prone behavior under bucket density variation. Future dense-kinship buckets (Lannister, Stark, Targaryen) will hit the same pattern.
2. Type-contract creep on FIGHTS_IN-person and ATTENDS-person patterns continues across batches; needs explicit examples in the prompt.
3. KILLED_BY may have its first 2 wrong-attribution cases — needs verification before they propagate into the graph.

Resume requires one or both of:
- **Prompt strengthening**: Add explicit "do NOT use CONTEMPORARY_WITH for any character-pair relationship; if no canonical type fits, REJECT with reason `no-fitting-type-vocab-gap-filed`" as a top-level rule (not buried in vocab section). Add explicit examples: "Lothar attends Hoster Tully's funeral" → ATTENDS hoster-tullys-funeral, not CONTEMPORARY_WITH hoster-tully. Add COUSIN_OF to the vocabulary (similar reasoning as UNCLE_OF).
- **Bucket triage**: Run a script to identify which queued buckets are dense-kinship (>50 cross-references inside the same house) and either route those through more careful prompts or process them last after vocabulary expansion.

## Headline quality findings

**KILLED_BY directions: 18/18 correct across all 4 audited batches.** Zero direction reversals. (Compare to Haiku's ~55% reversal rate.)

**Edge type vocabulary diversity:** 17-27 distinct types per batch. Well-distributed, no Haiku-style collapse-to-three-defaults. SERVES used 5-24× per batch (~5-15% of emits, appropriate for ASOIAF's feudal density), not the catch-all default Haiku turned it into.

**Tier calibration:** 64-87% tier-1, 10-30% tier-2, 0-3% tier-3 across the 4 batches. Proper distribution of explicit-vs-inferred prose. (Haiku produced 100% tier-2 — uniform under-tiering.)

**Evidence snippets:** 42-185 chars verbatim prose from source bodies. Not section headers. Validator enforces this mechanically.

**Cross-identity escalations:** 3 total across 4 batches — tom-costayne/tommen-costayne-knight pair (batch-0012) and one in batch-0015. All well-formed with rationale.

## Two patches added mid-run

### Patch A: No CONTEMPORARY_WITH-as-fallback

**Discovery (batch-0014):** Worker emitted 14 CONTEMPORARY_WITH edges where the actual relationship was something else (milk-brothers, wet-nurse, knighting, hosting). The worker also filed correct vocab-gap questions for these, but additionally emitted a wrong-fit edge as a "fallback" — polluting the graph with semantically wrong edges while the gap is pending.

**Patch:** Added explicit rule to classifier prompt: "Do NOT emit a wrong-fit canonical type as a 'fallback' when a vocab gap is filed. Specifically, do not use CONTEMPORARY_WITH as a catch-all... The graph would rather have a clean reject + vocab gap than a misleading wrong-edge." Also added to worker template's "Two failure modes to avoid" section.

**Result in batch-0015:** CONTEMPORARY_WITH count dropped from 14 → 0. Worker correctly rejected the relevant candidates with reason `no-fitting-type-vocab-gap-filed` (or no rejection if the relationship wasn't real after all).

### Patch B: No reverse-direction vocab gaps

**Discovery (batch-0014):** Worker filed vocab-gap questions for CHILD_OF (reverse of PARENT_OF), HOSTED_BY (reverse of GUEST_OF), RESURRECTED_BY (reverse of RESURRECTS). These are not missing types — they are intentionally one-sided in the architecture. The edge belongs on the parent's / host's / resurrector's node.

**Patch:** Added "Reverse-direction edges — do NOT file as vocab gaps" section to the classifier prompt with the full list of one-sided types (PARENT_OF, GUEST_OF, RESURRECTS, TUTORS, WIELDS, OWNS, FORGED_BY) vs both-sided types (KILLS/KILLED_BY, UNCLE_OF/NEPHEW_OF, WARD_OF/FOSTERED_BY). When source is the wrong endpoint, reject with reason `reverse-direction-edge-belongs-on-other-node`.

**Result in batch-0015:** Zero reverse-direction vocab gaps filed. Pattern eliminated.

## Vocab-gap candidates pending Matt review

batch-0014 filed 7 vocab gaps (4 legitimate after removing 3 reverse-direction). batch-0016 added 1 more:

1. **MILK_BROTHER_OF** — characters who share a wet-nurse (e.g. Edric Dayne and Jon Snow). Real Westerosi kinship category. Recommend ACCEPT.
2. **NURSED_BY / WET_NURSE_OF** — wet-nursing relationship. Distinct from PARENT_OF; culturally significant in ASOIAF. Recommend ACCEPT (probably as NURSED_BY with WET_NURSE_OF as the reverse-of for symmetry).
3. **KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON** — granting knighthood. Distinct from TUTORS (skill transfer) and APPOINTS (political office). Recurrent — recommend ACCEPT.
4. **CROWNS_QUEEN_OF_LOVE_AND_BEAUTY** — tourney-specific. Very narrow. Recommend REJECT or absorb into ATTENDS with qualifier.
5. **DEPICTED_IN** (batch-0016) — character is the subject of an in-world text/song/ballad (e.g. Danny Flint → "Brave Danny Flint" song). Distinct from WRITTEN_BY (author → work). Probably worth ACCEPTing as it captures the in-universe legacy/folklore layer that ASOIAF is rich in.

Plus the 3 already-accepted-in-architecture types: ATTENDS, UNCLE_OF/NEPHEW_OF, KILLED_WITH (added Session 54 in response to batch-0012's gap questions).

## Cost so far

- batch-0012: ~$3.42 (canonical re-run)
- batch-0013: ~$3.42
- batch-0014: ~$5.71 (longer wall, more self-correction)
- batch-0015: ~$4.42
- batch-0016: ~$3.42
- batch-0017: ~$3.42
- batch-0018: ~$3.42 (regression)

Total this session: **~$27**. Remaining bulk estimate: ~183 batches × ~$3.42 = ~$626 IF firing resumes at current quality. Recommend pausing the bulk fire until prompt strengthening + COUSIN_OF vocab addition is done.

## What I did mid-session (audit trail)

1. Archived broken-Sonnet batch-0012 (pre-schema-fix) — `working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/`
2. Updated `reference/architecture.md` — added UNCLE_OF, NEPHEW_OF, KILLED_WITH, ATTENDS (vocab → ~125 types)
3. Updated `.claude/agents/prose-edge-classifier.md` — added `evidence_kind`, pinned required-fields contract, documented `pass1_relationship` shape
4. Updated `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` — validator step + schema warnings
5. Created `scripts/wiki-pass2-validate-edge-jsonl.py` — mechanical validator
6. Ran Haiku smoke test on batch-0012 — SYSTEMATIC FAILURE — archived + rejected for this task
7. Re-ran batch-0012 on Sonnet — CLEAN
8. Sequential bulk run: batch-0013 → 0014 → 0015 → 0016 with audits + sleep pauses
9. Patched the classifier prompt + worker template with CONTEMPORARY_WITH-fallback rule + reverse-direction rule after batch-0014 revealed both patterns
10. Memory rule saved: `feedback_drift_detection_mandatory.md` (mechanical validator + cross-model audit + verdict-gates-resumption is the standing protocol for any bulk LLM run)

## Recommendation

**Continue the bulk run on Sonnet.** Quality is holding. Patches are in place. Cost is on-budget. The validator + cross-model audit pattern (Opus reviewing Sonnet) caught both real issues this session — the system is working.

**Suggested next moves when Matt returns:**

1. **Pick a check-in cadence.** Currently I've been doing full Opus audit per batch. That's expensive in audit time. The earlier-discussed "adaptive 3 → 10" cadence is appropriate now that Sonnet has 4 CLEAN batches under the patched prompt — drop to 1-in-5 audits, escalate back to 1-in-3 if a concern surfaces.

2. **Review the 4 pending vocab-gap candidates.** MILK_BROTHER_OF, NURSED_BY, KNIGHTED_BY look acceptable; CROWNS_QUEEN_OF_LOVE_AND_BEAUTY likely reject. Update architecture.md + classifier prompt before they re-appear in future batches.

3. **Decide whether to keep firing in this session** or hand off to a fresh worker session running `/loop 20m /worker-stage4`. The mission was designed for the latter; sequential foreground in this conversation works but is slower.

4. **Optional: write a follow-up continue prompt** at `progress/continue-prompts/2026-05-16-stage4-bulk-continuation.md` capturing the patches + the 4-CLEAN-batch baseline, so any resumption has full context.

## Files for the record

- This checkpoint: `working/session-results/2026-05-16-stage4-bulk-run-checkpoint.md`
- Mission state: `working/missions/2026-05-14-stage4-v1-bulk-sonnet/`
- 4 batches' outputs: under `working/wiki/pass2-buckets/<bucket>/prose-edges/` for the c-d-e prefixed houses
- Patched prompts: `.claude/agents/prose-edge-classifier.md`, `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`
- Validator: `scripts/wiki-pass2-validate-edge-jsonl.py`
- Two failed archives: `working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/`, `_archive/batch-0012-haiku-failed-2026-05-15/`
