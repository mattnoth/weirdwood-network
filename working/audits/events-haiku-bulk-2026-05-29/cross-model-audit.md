# Events Haiku Bulk — Cross-Model Drift Audit

**Date:** 2026-06-01 (UTC) · **Chain step:** `01-drift-audit`
**Source artifact:** `working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk/` (1,617 emits)
**Audit script:** `scripts/events-drift-audit.py` (sha `576cc815649c`) — throwaway, single-purpose
**Sample:** `audit-sample-50.jsonl` (seed=531, 50 rows, reproducible)
**Judged:** `audit-sample-50-judged.jsonl` (50/50 judged)
**Cost:** $0.93 (5 batches × 10 rows, Sonnet 4.6, cwd=/tmp)

---

> **2026-06-01 update (fresh-eyes review):** Pressure-tested by an independent
> general-purpose subagent that cold-read all 22 Sonnet REJECTs against the V5
> rules. Headline corrections:
> - **Sonnet over-rejected ~3-4 rows** (judge_idx 2 / 6 / 14 / 16). The audit's
>   sweep of "Haiku drifted on all 22" was overstated.
> - **The S69 smoke citation in §4 is wrong** — the actual session was **S77**,
>   and it measured *hand-read precision* on *fresh candidate rows*, NOT
>   Sonnet-judges-Haiku-emit on stratified emits-only. The two are not
>   directly comparable; the apparent contradiction with the smoke numbers is
>   measurement-shape, not drift.
> - **Adjusted numbers** crediting all over-rejections + all ambiguous-rows
>   to Haiku: triple agreement ≈ 56-70 %, at or below the 70 % floor.
> - **The No-Go still stands** — even with the corrections, named-type
>   precision (TRAVELS_TO, TRAVELS_WITH, LOCATED_AT) is under the gate. But
>   the failure is *borderline*, not catastrophic. Option (C) — Sonnet-filter
>   only the named-type rows — is the right-shape escalation; Option (D)
>   (Haiku re-prompt) is risky because V5 already named the failure modes.
> - **Methodology**: no audit-script bugs found.
>
> See subagent transcript in worklog for the full cold-read.

## Verdict: **NO-GO (borderline)** — do not promote Events Haiku bulk to `edges.jsonl` v2.0 as-is.

| Gate | Floor | Observed | Pass? |
|------|------:|---------:|:-----:|
| Triple-level agreement  | ≥ 70 % | **48.0 %** (24/50) | ✗ |
| Pair-level agreement    | ≥ 85 % | **56.0 %** (28/50) | ✗ |
| No edge type <50 % with >5 samples | — | **TRAVELS_TO: 17 % (1/6)** | ✗ |

22 of 50 Haiku emits (44 %) were rejected outright by the Sonnet judge.
Step 2 (`02-extend-formalize.md`) is **blocked**; chain halts pending Matt's call.

---

## 1. Method

- **Sample:** 50 rows drawn with `seed=531`. Pre-reserved ≥3 of each named type
  (TRAVELS_WITH / COMMANDS / TRAVELS_TO / LOCATED_AT / SERVES / REVEALS_TO);
  remainder proportional by book. Final distribution:

  - Books: agot 7 / acok 11 / asos 11 / affc 7 / adwd 14.
  - Named types: TRAVELS_TO 6, SERVES 6, LOCATED_AT 5, COMMANDS 4, TRAVELS_WITH 4, REVEALS_TO 3.
  - Long tail: 22 rows / 19 distinct types.

- **Judge setup:**
  - Model: `claude-sonnet-4-6`.
  - Subprocess: `claude -p --output-format json`, **cwd=`/tmp`** (no project CLAUDE.md load).
  - Prompt: reused canonical `render_classify_prompt()` from
    `scripts/stage4-tail-classifier.py` (same `_PROMPT_PREAMBLE` Haiku used).
  - Prompt SHA: `d31ca56c4768` — **byte-identical** to the Haiku bulk-run SHA. Parity confirmed at audit start.
  - Locked vocab: 163 edge types via `build-edge-type-counts.extract_canonical_types()`.
  - Gated types: `DEFAULT_GATED_TYPES` (13 types) — same as Haiku bulk.
  - Batches: 5 × 10 rows, $0.16–$0.23/batch.

- **Why a `claude -p` subprocess (not an Agent subagent):** an Agent subagent
  inherits ~28k tokens of project CLAUDE.md + filesystem tools Haiku never had —
  that contaminates the audit (it measures setup-vs-setup, not model-vs-model).
  Only `cwd=/tmp` enforces parity with Haiku's bulk-run conditions. (Cost is
  *not* the load-bearing reason; ~50 rows is pennies either way.)

- **What "agreement" means here:**
  - *Triple*: same `(source_slug, edge_type, target_slug)`.
  - *Pair*: same `(source_slug, target_slug)` — i.e. judge emitted *any* type
    (not REJECT) with the same endpoints.
  - *Disagree-shape*: judge emitted REJECT for a row Haiku emitted.

---

## 2. Per-edge-type triple agreement

| Edge type    | Total | Agree | % | Flag |
|--------------|------:|------:|---:|:----:|
| TRAVELS_TO   |     6 |     1 | 17 % | **⚠ BELOW 50% FLOOR, n>5** |
| SERVES       |     6 |     4 | 67 % |   |
| LOCATED_AT   |     5 |     1 | 20 % | n=5 (edge of floor rule) |
| COMMANDS     |     4 |     2 | 50 % |   |
| TRAVELS_WITH |     4 |     0 |  0 % | n=4 (below floor rule's n>5 trigger, but 0 %) |
| OPPOSES      |     3 |     1 | 33 % |   |
| REVEALS_TO   |     3 |     2 | 67 % |   |
| (long tail, n=1 each — limited signal) | 22 | 14 | 64 % |   |

The named-type buckets, which are the largest volume in the bulk run, are
the ones underperforming. The long-tail buckets are mostly fine on their tiny
sample sizes (most n=1, single-row agreement is high-variance).

**Reject distribution by Haiku type** (judge_edge_type == "REJECT"):

| Haiku type    | Sampled | Rejected by judge | Rejection rate |
|---------------|--------:|-------:|----:|
| TRAVELS_TO    |       6 |      5 | 83 % |
| TRAVELS_WITH  |       4 |      3 | 75 % |
| LOCATED_AT    |       5 |      3 | 60 % |
| COMMANDS      |       4 |      2 | 50 % |
| OPPOSES       |       3 |      1 | 33 % |
| SERVES        |       6 |      1 | 17 % |
| REVEALS_TO    |       3 |      1 | 33 % |

Top type-swaps (judge picked a different type, n≥1):
`LOCATED_AT → TRAVELS_TO`, `SERVES → SWORN_TO`, `TRAVELS_WITH → RESCUES`, `OPPOSES → FEARS`.

---

## 3. Manual inspection of 5 high-disagreement rows

The chain prompt requires reading 5 disagreement rows to decide which side is
the drift. **In every case below, Sonnet's call is consistent with the V5
precision rules; Haiku is the side that drifted.**

### 3.1  judge_idx=2 — `LOCATED_AT asha-greyjoy → ten-towers` (affc)

> *Quote:* "She **remembered** breathless races up and down the steps and along wallwalks and covered bridges, fishing off the Long Stone Quay, days and nights lost amongst her uncle's wealth of books."

- Haiku emitted LOCATED_AT.
- Judge: **REJECT.**
- **Verdict: Haiku drift.** The quote is Asha's *childhood memory*, not her standing location. Rule 4a / V5-R2: "Do NOT supply a relationship from world-knowledge … even if the hint asserts it." The hint says "Asha walks through Ten Towers" but the quote does not stage that motion. Memory ≠ standing fact.

### 3.2  judge_idx=3 — `LOCATED_AT tyrion-lannister → pentos` (adwd)

> *Quote:* "'Slaver's Bay is a long way from Pentos.' Tyrion speared a goose liver on the point of his knife."

- Haiku emitted LOCATED_AT.
- Judge: **REJECT.**
- **Verdict: Haiku drift.** Quote is dialogue *mentioning* Pentos plus an unrelated action. V5-R2 fails: nothing in the quote anchors Tyrion *at* Pentos. The hint ("Tyrion observes Pentos from window") was discarded scaffolding the model should not have promoted to fact.

### 3.3  judge_idx=21 — `TRAVELS_WITH tyrion-lannister → podrick-payne` (acok)

> *Quote:* "On the left, Tyrion was surprised to see Podrick Payne, a sword in his hand."

- Haiku emitted TRAVELS_WITH.
- Judge: **REJECT.**
- **Verdict: Haiku drift, classic Rule 12 violation.** The CO-PRESENCE PRINCIPLE is explicit: "Two entities sharing a scene, room, meal, march, battle … is NOT, by itself, a typed relationship." TRAVELS_WITH carve-out also explicit: "Standing in the same room, court, or hall is NOT travel." A single battle moment of co-presence is not a shared journey.

### 3.4  judge_idx=32 — `LOCATED_AT jon-snow → frostfangs` (acok)

> *Quote:* "Yet as the dusk deepened and darkness seeped into the hollows between the trees, Jon's sense of foreboding grew."

- Haiku emitted LOCATED_AT.
- Judge: **REJECT.**
- **Verdict: Haiku drift.** Jon is on the ringwall *looking at* the Frostfangs. Neither the quote nor a plain reading of the hint puts him at the Frostfangs. V5-R1 + V5-R2 both fail. (The Frostfangs in the hint are an item in a list of things visible from the ringwall, not a location of Jon.)

### 3.5  judge_idx=37 — `TRAVELS_TO sansa-stark → fingers` (asos)

> *Quote:* "The ladder to the forecastle was steep and splintery, so Sansa accepted a hand up from Lothor Brune."

- Haiku emitted TRAVELS_TO.
- Judge: **REJECT.**
- **Verdict: Haiku drift.** Quote is about climbing a ladder on the ship; the Fingers (her destination) are not in the quote. Hint says "they approach the Fingers." V5-R2 fails: the *quote* doesn't stage the motion to the Fingers. Approaching ≠ travels-to-the-destination as a completed fact in the quote.

### Borderline (not used for verdict, noted for completeness)

- **judge_idx=13** (`LOCATED_AT jon → kings-tower` vs judge `TRAVELS_TO`): "In the King's Tower, Jon was stripped of his weapons and admitted…" Genuine type ambiguity (motion-into vs state). Judge picked `TRAVELS_TO`; either is defensible.
- **judge_idx=38** (`TRAVELS_WITH varys → tyrion` vs judge `RESCUES`): Varys leading Tyrion through escape tunnels — `RESCUES` is the tighter call. Judge picked the better-fitting type.

---

## 4. Failure pattern (root cause hypothesis)

Across the inspected disagreements, **Haiku consistently treats the `hint_raw`
field as evidence on par with `evidence_quote`**. The hint is a Pass-1
chapter-summary header that describes the chapter event; it is *not* a quote.
The prompt is explicit (Rule 4a, V5-R2): the *quote* is the only proof.

The 22 unanimous rejections from the Sonnet judge cluster around five
hint-vs-quote failure modes:

1. **Memory / dream / hypothetical staged as fact** (Asha at Ten Towers).
2. **Mention-of-place treated as location-at-place** (Tyrion + Pentos).
3. **Co-presence in a single scene treated as TRAVELS_WITH** (Tyrion + Podrick; Haldon + Duck).
4. **Looking-at / approaching treated as LOCATED_AT / TRAVELS_TO** (Jon + Frostfangs; Sansa + the Fingers; the *Shy Maid* + Ny Sar).
5. **Quoted intent / overheard plan treated as completed action** (Urswyck + Harrenhal).

These are exactly the failure modes V5-R2 and Rule 12 were authored to prevent.
The lockdown did not, in fact, prevent them at the scale of the bulk run.

A secondary concern: this contradicts the **S69 smoke runs** (Sonnet-vs-Haiku
agreement ~85 % AGOT / ~90 % ACOK strict). The smoke runs were the prior basis
for "Haiku is safe under the V5 lockdown." Two possible explanations, neither
re-checked here:
- **Sample selection in the smoke runs:** different input candidates (maybe
  cleaner, maybe pre-filtered) producing different agreement than the full
  events-bucket population.
- **Drift across the long bulk run:** Haiku stable on small batches but
  degrading over a 16-hour run / 282 batches (cache pressure, prompt rehearsal
  loss). The 0 conform_violations across the run rules out *vocab* drift but
  not *gating* drift.

Either way, the smoke-run number does not generalize to the bulk artifact.

---

## 5. What this means for the v2.0 plan

- **Cannot ship Events Haiku bulk as v2.0 in its current state.** Even with the
  44 % rejection rate corrected away (i.e., dropping all judge-REJECT rows),
  we would still be looking at ~17 % type-swap on the survivors. That's not a
  v2 enrichment — it's a noise injection.

- **Layering on top of v1.3 would be worse.** The 444 pair-overlaps in
  `analysis.md §6` mean ~28 % of the bulk's new emits are on already-asserted
  endpoint pairs, where a wrong type *contradicts* a stronger existing
  classification.

- **The v5 prompt SHA is correct** — that's not the issue. The prompt was
  authored well; Haiku is not honoring it at scale.

---

## 6. Recommended escalation paths (for Matt)

Not deciding these here. Surfacing options for Matt's call:

1. **(A) Re-run Events bulk on Sonnet 4.6**, accept the cost. We're confident
   Sonnet honors V5-R2 + Rule 12 (this audit shows it). Estimated cost vs
   Haiku: ~10× per row → ~$340 for the same 16,502-row corpus, or scoped to
   just the rejection-bearing types. (This contradicts the
   `project_stage4_haiku_not_sonnet` memory — Matt's call whether the
   precision floor changes that.)

2. **(B) Promote *only the long-tail types* from the Haiku output** —
   the manual inspection showed n=1 long-tail buckets mostly agreeing.
   Drop everything in {TRAVELS_TO, TRAVELS_WITH, LOCATED_AT, COMMANDS,
   OPPOSES} (the 22 named-type rows = 13 % of total emits) and re-audit
   the remainder. Risk: this audit lacks per-type statistical power for the
   long tail (most n=1).

3. **(C) Filter the Haiku output by Sonnet on the rejection-bearing types
   only** — re-run Sonnet on the ~700 rows of TRAVELS_TO/WITH/LOCATED_AT/
   COMMANDS/OPPOSES Haiku emits, drop the rejects, retype the swaps.
   Smaller blast radius than (A); preserves Haiku for the cheap types where
   it agreed.

4. **(D) Tighten the Haiku prompt and re-run** — add specific anti-patterns
   for the 5 failure modes above (memory-as-fact, mention-as-location,
   co-presence-as-TRAVELS_WITH, looking-at-as-LOCATED_AT, approaching-as-
   TRAVELS_TO). Re-launch on Haiku with the new SHA. Risk: V5 already named
   most of these and Haiku ignored them; v6 may have the same problem.

5. **(E) Abandon Events bulk for v2.0** — push v2.0 to wait for the Dialogue
   bulk (originally planned as v2.1) and re-evaluate Events later. Cheapest
   short-term but loses the audit signal.

---

## 7. Files on disk after this step

- `scripts/events-drift-audit.py` (sha `576cc815649c`) — throwaway, single-purpose audit script.
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50.jsonl` — 51 lines (metadata + 50 sampled emits, seed=531).
- `working/audits/events-haiku-bulk-2026-05-29/audit-sample-50-judged.jsonl` — 51 lines (metadata + 50 judge decisions).
- `working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md` — this file.
- `progress/continue-prompts/2026-05-31-events-v2-promotion-chain/step-01-status.md` — chain handoff (updated to No-Go).

## 8. Provenance (anchor — fail closed if mismatched on re-run)

| Field | Value |
|---|---|
| `judge_model` | `claude-sonnet-4-6` |
| `judge_cwd` | `/tmp` |
| `expected_prompt_sha` | `d31ca56c4768` |
| `actual_prompt_sha` | `d31ca56c4768` ✓ |
| `sample_seed` | 531 |
| `sample_n` | 50 |
| `judged_count` | 50 |
| `judged_cost_usd` | 0.9274 |
| `chain_step` | `01-drift-audit` |
| `script_path` | `scripts/events-drift-audit.py` |
| `script_sha` | `576cc815649c` |
| `timestamp_utc` | `2026-06-01T03:50:21Z` (sample) / `2026-06-01T04:25Z` (judged) |
