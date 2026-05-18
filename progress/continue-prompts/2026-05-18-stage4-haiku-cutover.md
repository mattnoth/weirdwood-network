# Stage 4 — Sonnet→Haiku Cutover Investigation & Vocab Lock

> **Recommended model:** Sonnet 4.6 for the investigation work (data analysis, vocab review, smoke-test design). Opus 4.7 ONLY if the vocab-lock decisions get genuinely contested (multi-edge-type collisions, hard semantic calls). The Haiku smoke run itself uses claude-haiku-4-5-20251001.
>
> **Drafted:** 2026-05-18 evening, end-of-session (Matt at 96% of 5h cap; deferred actual work to next session).
> **Status:** Investigation queued. No code or schema changed yet. Running Sonnet worker is UNTOUCHED.

---

## Why this exists

Matt is running the Stage 4 v1 prose-edge classifier bulk run on Sonnet 4.6 (mission `2026-05-14-stage4-v1-bulk-sonnet`). Current state: ~75 of 1,089 batches done (~7%). At Sonnet pace + 270s sleep + 5h-cap walls, finishing the remaining ~1,015 batches projects to **~$2,800 and ~340 hours of wall-clock compute**, with weekly Sonnet cap already at 12% after 7% of the work. Matt is a solo dev on one Claude Max account — **this pace is not feasible** without locking up the account for a month.

**Goal:** evaluate moving the remaining ~1,015 batches to Haiku 4.5 (`claude-haiku-4-5-20251001`). Estimated ~$800 / ~170 hours / ~12-14% weekly cap. Lower per-token cost AND faster wall-clock per batch.

**Hard rule from memory:** every model change in a bulk LLM run requires drift detection (see `feedback_drift_detection_mandatory.md`). No mid-corpus model swap without a smoke test that compares Haiku output to Sonnet output on the SAME inputs.

---

## What I learned at end-of-session that the next agent needs to know

### The schema picture (corrected)

I initially told Matt that rejects and evidence quotes were being thrown away. **Both claims were wrong.** Verified state:

- **10,342 reject rows persisted** across 892 prose-edges JSONL files (`working/wiki/pass2-buckets/*/prose-edges/*.jsonl`). Each reject row has `decision: "reject_just_mention"`, `source`, `target`, and a one-clause `reason`. They're on disk.
- **3,466 of 4,129 emits (~84%) carry `evidence_snippet`** (≤200-char verbatim prose) + `evidence_section` (## heading) + `evidence_paragraph_index`. Sufficient to re-find the passage on disk OR re-classify the emit row without re-reading prose. **This is the "batch 11 fix" Matt remembered — it's real and mostly being honored.**
- **The non-compliance rate** (emits missing snippets) is ~16%. Some files like `daemon-sand.edges.jsonl` were emit-only with no snippet field. Unclear whether this is per-batch drift, per-file drift, or per-worker drift. Worth a deeper audit before the Haiku smoke runs.
- **Real remaining gap:** rejects have `reason` but no `evidence_snippet`. So re-classifying rejects later (e.g., a new edge type that might cover some prior rejections) requires re-reading the source prose file. Per-prose-file cost, not per-row cost.

### What "authoritative" means

Pass 1 mechanical extraction reads the actual book text and pulls verbatim book quotes per chapter. **All 5 books complete: AGOT 73/73, ACOK 70/70, ASOS 82/82, AFFC 46/46, ADWD 73/73 (344/344 total, completed 2026-05-06 — verified against worklog.md lines 62-66 and file counts in `extractions/mechanical/`).** Stage 4's `pass1_relationship` candidate shape consumes those Pass 1 rows directly — book-tier edges for all 5 books are already extracted as candidates the classifier turns into edges. The "book wins over wiki" reconciliation happens at promotion time, not now.

**Note (2026-05-18 fix):** the prior version of this paragraph said "Status from memory: AGOT done, AFFC done, ACOK 20/70, ASOS pending, ADWD pending" — that was stale (drafted from a 13-day-old memory file without verifying against worklog.md). Corrected after a root-cause investigation. See Session 55 history.

### Second-account math

A 2nd Claude Max literally doubles the weekly cap. Doubles throughput AND doubles cost (~$5,600 instead of $2,800 for Sonnet). Haiku at ~$800 on one account is the same dollars as a 2nd-account Sonnet run at 1/7th the cost. **Matt's stated goal: switch to Haiku, not buy a 2nd account.**

---

## The three-step plan Matt greenlit

### Step 1 — Pull vocab-gap questions + compare to existing schema

The classifier filed `vocabulary-gap` questions whenever it saw a relational pattern with no fitting type in the locked ~121-type vocab (per `reference/architecture.md` § "Edge Types"). These live at:

```
working/wiki/pass2-buckets/questions-for-matt.jsonl
```

(Confirm path — also check `working/missions/2026-05-14-stage4-v1-bulk-sonnet/` for mission-local questions if the bucket-level file is sparse.)

Pull every `"type": "vocabulary-gap"` row, dedupe by `proposed_edge_type`, group by frequency. From summaries already seen across batches 0062-0072, the surfaced gaps include at least:

- **COMPANION_OF** — explicit personal friendship/camaraderie (distinct from ALLIES_WITH for political alliance and TRUSTS for one-directional confidence). Examples: patrek-mallister/edmure-tully, patrek/theon, marq-piper/edmure/patrek triples.
- **PARTICIPATES_IN** — non-combat administrative/logistical involvement in named events (FIGHTS_IN requires combat; ATTENDS requires non-combatant ceremony presence). Example: Medrick Manderly transporting prisoners during the Hour of the Wolf.
- **DIED_OF** — cause of death by named disease/condition (Winter Fever, Shivers, Spring Sickness, greyscale). KILLED_BY requires a person-killer; DIED_AT captures location.
- **AFFLICTED_BY** — same disease-relationship problem for living characters (Jorah Mormont/greyscale, Shireen Baratheon/greyscale).
- **Infrastructure-not-vocabulary:** `trial-of-seven` is typed `concept.custom` but should likely be `event.battle` or `event.tournament` (type-contract violation that blocked a FIGHTS_IN emit).

For each gap:
1. Read the proposed_edge_type + ≥3 example sentences from the question.
2. Compare to the locked vocab in `reference/architecture.md` — does any existing type *almost* fit? (e.g., MOURNS exists; would AFFLICTED_BY conflict with PERCEIVED_AS or RESENTS in any cross-type way?)
3. Decide: **accept** (add to architecture.md + update classifier prompt's "Type discipline" section), or **hard-reject** (mark the gap closed with reason: "use existing type X" or "this is not a graph-traversable relationship").
4. Lock the vocab — once decided, the classifier prompt should say "this list is final, do NOT file vocabulary-gap questions for the remaining batches." This rigidity is exactly what Matt asked for: a fully-closed decision surface for Haiku.

**Deliverable:** a vocab-lock decision file at `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md` listing each gap + Matt's decision + the architecture.md diff.

### Step 2 — Reject-reason sample from complex batches

Pick complex/large source-target files Sonnet processed (>50 candidates), sample 20-30 of their reject rows, and gauge whether the reasons are sound. This establishes the **Sonnet baseline** that Haiku must match.

Candidate complex pages from observed batch summaries:
- `wyman-manderly` (168 candidates, batch-0066)
- `wylis-manderly` (112 candidates, batch-0065)
- `bowen-marsh` (66 candidates, batch-0068)
- `taena-merryweather` (53 candidates, batch-0072)
- `hallis-mollen` (71 candidates, batch-0072)

For each, look at the rejected rows' `reason` field. Are the reasons consistent? Do they fall into recognizable buckets (reverse-direction, temporal co-occurrence, duplicate-of-infobox, type-contract-violation, no-fitting-type)? Or are there reasons that seem wrong/sloppy/inconsistent?

**Deliverable:** a short writeup — `working/audits/stage4-sonnet-reject-quality-2026-05-18.md` — with the top reject-reason categories, frequency, and any concerning patterns. This is what the Haiku smoke run will be diffed against.

### Step 3 — Haiku smoke-test spec

Once vocab is locked + Sonnet reject baseline is established, design the smoke test. Constraints:

- **Never overwrite Sonnet output.** Haiku writes to `working/missions/2026-05-14-stage4-v1-bulk-sonnet/haiku-smoke/<batch_id>/` (parallel dir).
- **Don't change the running worker.** The Sonnet wrapper + worker keep running (or Matt halts them; see `weirwood stage4 stop` which touches `/tmp/stage4-stop`).
- **Pick complex + diverse smoke batches** — not 3 trivial ones. Specifically:
  - One large `source_target` batch (e.g., a batch containing wyman-manderly or similar 100+-candidate page).
  - One `pass1_relationship` batch (book-tier candidates from AGOT or AFFC Pass 1 output).
  - One `comention` batch (chapter-summary-driven, where two entities co-occur in a meta.chapter node).
- **Use the locked vocab.** The classifier prompt should be updated (in a copy specific to the smoke run, NOT overwriting the main one) to say "vocabulary is FINAL — do NOT file vocab-gap questions, instead reject_just_mention with reason `no-fitting-type-vocab-locked`."
- **Diff metrics to capture per batch:**
  - Per-decision agreement: of the candidates where Sonnet emitted, does Haiku emit (same edge_type) or reject?
  - Edge-type agreement on emits: when both emit, do they agree on the type? (use confusion matrix)
  - Confidence-tier agreement on emits where types match.
  - Snippet capture rate (Haiku may drop the snippet field — that's a regression to flag).
  - Cost + wall-clock per batch.
- **Pass threshold:** something like "≥90% emit/reject agreement and ≥85% edge-type agreement on matched-emit rows" — final threshold Matt's call.

### Matt's "Haiku-flags-low-confidence-for-Opus-cleanup" idea

Worth designing into the smoke spec: when Haiku emits at `confidence_tier: 3` (hinted only), an Opus pass over flagged-only rows is cheap (each row has the snippet + paragraph index already). The infra is in place — just need a script to filter `confidence_tier == 3` from Haiku output and feed those into an Opus re-classify pass. Defer the Opus pass until Haiku bulk is done; cheap to add later.

---

## Constraints (hard rules)

- **Don't touch the running Sonnet worker prompt** (`.claude/agents/prose-edge-classifier.md`, `.claude/commands/worker-stage4.md`). Any vocab-lock changes go into a fork or a parallel prompt file for the Haiku smoke. The Sonnet bulk run, if Matt resumes it, uses the original prompt.
- **Don't overwrite any Sonnet-completed batch output.** Smoke output lives in a parallel `haiku-smoke/` directory.
- **Smoke batches must be complex/diverse.** Not 3 trivial pages.
- **Drift detection is mandatory** — schema-validator + cross-model audit + verdict gate before authorizing Haiku for the remaining ~1,015 batches.
- **Cheapest viable model** — Sonnet 4.6 for the investigation; Opus 4.7 only if a vocab-lock decision turns hard.
- **Python before Agent** — analyzing the questions JSONL, the reject rows, and the diff is python work, not agent work.
- **Never auto-run /endsession or any extraction launch without asking.**

---

## When the next session opens

1. Verify Sonnet worker state: is it running, stopped, or stalled? `weirwood stage4` (status command) is canonical.
2. Read this prompt + `reference/architecture.md` § "Edge Types" + `.claude/agents/prose-edge-classifier.md` (the schema spec at lines 60-115 for the emit/reject row shapes).
3. Start with Step 1 (vocab-gap pull + compare to schema). Output goes to `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md`.
4. Don't proceed to Step 3 (Haiku smoke) until Matt has reviewed and approved the Step 1 vocab-lock decisions.

## Open questions for Matt at the start of next session

- **Vocab-lock threshold:** for each filed gap, do you want to see ≥3 examples in the question + your gut call, or do you want me to recommend accept/reject?
- **Smoke pass threshold:** what agreement % between Sonnet and Haiku is "good enough"? Default proposal: 90% emit/reject agreement, 85% edge-type agreement on matched emits.
- **Haiku non-compliance audit:** if Haiku writes 60% of emits with snippets (vs Sonnet's 84%), is that disqualifying or acceptable? My instinct: disqualifying — snippet is what makes the emit re-classifiable from disk.
- **What to do about the running Sonnet worker:** stop it now (preserve weekly cap for the smoke), let it keep going while we investigate, or pause it after current batch?
