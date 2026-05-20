# Stage 4 Haiku — Throughput Analysis + Resume Strategy (Session 62 resumption)

> **Recommended model: Opus 4.7** for the throughput-strategy decision (architectural
> reasoning, cost/time tradeoffs). After the decision, downstream execution
> work (validation runs, log inspection, mission housekeeping) can downgrade
> to Sonnet. Haiku is the BULK WORKER, not the analyst.

> **Mandate:** Session 61 added 5 vocab types + verb-gate enforcement + loop
> infrastructure, then launched an overnight Haiku bulk run. The run completed
> 12 full batches + 1 partial (40 files into batch-0013) before hitting the
> Claude Code 5-hour quota wall. Across the night that translates to ~13 of
> 1089 batches — far too slow to finish in reasonable wall-clock time. **The
> mandate now is to (a) validate what we got and (b) decide a faster strategy
> before resuming.**

---

## TL;DR for the wake-up reader

1. Session 61's vocab + schema work is **uncommitted to git**. Multiple files
   modified, scripts added. Section "Files modified Session 61" below lists
   exactly what — commit as one coherent unit after triage.

2. Overnight Haiku run **completed 12 full + 1 partial batches** (~$38 spend),
   then hit the 5h Claude Code quota at 08:35 CDT 2026-05-20 and stopped
   producing useful work for 3 more batches before Matt touched the stop file
   at 09:49 CDT. **Output: 375 .edges.jsonl files across 85 buckets.**

3. **Throughput math:** at current pace (28 min/batch wall-clock × ~12 batches
   per 5h quota window × ~10h between full-quota cycles), 1089 batches takes
   **~38 days** and costs **~$3,200**. Unsustainable as-is.

4. **The 20-min inter-batch sleep does NOT help throughput** — Claude Code
   rate limit is per-5h-window-usage, not per-burst-rate. Sleeping just delays
   hitting the wall without raising the wall. **Removing/reducing sleep is the
   single largest immediate lever** (~3x speedup).

5. **Anthropic Batch API** would be a 50% cost cut + no interactive rate limit
   — but requires rewriting the worker off `claude` CLI onto the Anthropic SDK
   directly. Bigger engineering investment, not the immediate next move.

6. **Quality has NOT been validated yet.** Run the validator (command below)
   on the 375 fresh files before any decision to scale.

---

## Session 61 — what was done (still uncommitted)

This session locked the vocab and built the bulk-run plumbing. Tasks 1-6 of
the in-session task list completed; tasks 7-8 (residual-apply + post-validate)
were superseded by the D3 fresh re-run path.

### Vocab additions (159 → 164)

Added to `reference/architecture.md`:

| Type | Subsection | Direction | Notes |
|---|---|---|---|
| `IMPRISONED_AT` | Spatial & Temporal | Captive → Location | Distinct from LOCATED_AT (presence), IMPRISONS (judicial), PRISONER_OF (state) |
| `TRAVELS_WITH` | Spatial & Temporal | Symmetric | Road OR court/retinue co-presence |
| `PRISONER_EXCHANGE_FOR` | Military & Conflict | Symmetric captive↔captive | Distinct from RANSOMS (payer→captive) |
| `GUARDS` | Military & Conflict | Custodian → Subject | Physical custody (protective OR custodial); distinct from PROTECTS (beneficiary axis) and IMPRISONS (judicial) |
| `ENCOUNTERS` | Emotional & Perceptual | Symmetric | Verb-gated; first meetings, road crossings, set-piece confrontations |

Vocab callout in architecture.md bumped 159→164 with full Session 61 narrative.

### CRITICAL RULE 6 — ENCOUNTERS verb gate

New rule in `.claude/commands/stage4-haiku-classify.md`. Modeled on Rule 2
KNOWS-STOP precedent. Whitelisted staging verbs: `met`, `meets`, `meeting`,
`came face to face`, `face-to-face`, `confronted`, `found himself/herself
before`, `stood before`, `appeared before`, `encountered`. Without one of
these in the `evidence_snippet`, ENCOUNTERS rejects with reason
`temporal-cooccurrence-not-relational`.

### Validator schema enforcement (architectural advancement)

Added `VERB_GATE` dict + new `verb-gate-failure` violation type to
`scripts/wiki-pass2-validate-edge-jsonl.py`. **First time the lock-down covers
verb gates as schema, not just prompt-text.** Initial config covers only
ENCOUNTERS; KNOWS retrofit deferred pending audit of existing rows. The KNOWS
case is documented in the script's docstring as a known follow-up.

Also added 5 new `TYPE_CONTRACTS` entries (IMPRISONED_AT, TRAVELS_WITH,
PRISONER_EXCHANGE_FOR, GUARDS, ENCOUNTERS).

### Normalizer alias

`scripts/stage4-haiku-normalize-edge-types.py`:
- `ACCOMPANIES` → `TRAVELS_WITH` added to `ALIAS_TABLE` (first semantic-synonym
  entry in the table; previous rule was inflection-only).
- Removed IMPRISONED_AT, TRAVELS_WITH, ENCOUNTERS, GUARDS from
  `SEMANTIC_DISTINCT_TYPES` — they're canonical now.

### Loop infrastructure (the bulk-run plumbing)

Two new shell scripts:

- `scripts/stage4-haiku-loop.sh` — iterates batches sequentially, calls
  `stage4-haiku-run.py --batches batch-NNNN`. Stop-file controlled
  (`/tmp/stage4-haiku-stop`). Env-tunable sleep + concurrency + chunk-size.
  On per-batch failure: sleeps `STAGE4_HAIKU_RATE_LIMIT_SLEEP` (default 1h)
  and continues to next batch. Stop file checked every 60s during all sleeps.

- `scripts/stage4-haiku-run-forever.sh` — outer resilience wrapper. If inner
  loop exits non-zero (crash, terminal disconnect), sleeps
  `STAGE4_HAIKU_RELAUNCH_SLEEP` (default 10 min) and relaunches. Mirrors
  Sonnet's `stage4-run-forever.sh` pattern.

Both write logs to `working/missions/2026-05-19-stage4-haiku/loop-logs/`.

### Sonnet mission verified untouched

`working/missions/2026-05-14-stage4-v1-bulk-sonnet/`, `scripts/stage4.sh`,
`scripts/stage4-run-forever.sh`, `.claude/commands/worker-stage4.md` — all
unchanged. Verified via `git diff --stat`.

### Pre-run cleanup (archive)

Before launching the overnight run, archived all pre-vocab-164 Haiku output
to `working/wiki/pass2-buckets/_archive/haiku-pre-vocab164-2026-05-20/`:

- 20 buckets' previous `prose-edges-haiku/` subdirs (70 .edges.jsonl files)
- Mission state files: `unresolved-edges-log.jsonl`, `residual-resolutions.jsonl`,
  `run-logs/`, `results/` (all pre-vocab-164)

This was per Matt's instruction "start brand new run, archive existing haiku
like we've done sonnet." The archive directory contains a `mission-state/`
subdir holding the old mission logs alongside the bucket subdirs.

---

## Overnight run — what actually happened

### How it was launched

```bash
# At 02:54 CDT 2026-05-20, via osascript to a new iTerm window:
osascript -e 'tell application "iTerm" ...' (creates window, runs)

# The window ran:
bash /tmp/run-haiku-forever.sh

# Which is a thin shell wrapper baking in the project cwd:
cd /Users/mnoth/source/asoiaf-chat
exec bash scripts/stage4-haiku-run-forever.sh batch-0001
```

The `/tmp/run-haiku-forever.sh` wrapper exists because iTerm's default cwd
is `/Users/mnoth/source/`, not the project dir — per the iTerm cwd memory.

### What completed

- **batch-0001 through batch-0012**: full success, 30/30 files each, ~$3.20/batch
- **batch-0013**: partial — chunks 00-03 finished (12/30 files), chunks 04-09
  hit rate-limit and failed with 0 outputs each
- **batch-0014, 0015, 0016**: every chunk in each batch instantly rate-limited
  (1-2s, $0 spent) — these are all "wasted attempts" that the inner loop
  treated as completed batches. **Real progress: 12.4 batches.**
- **Stop file detected at 09:49 CDT** mid-sleep after batch-0016. Inner loop
  exited cleanly, outer wrapper exited cleanly.

### Rate-limit window

- Limit hit: ~08:35 CDT 2026-05-20 (mid-batch-0013)
- Reset announced: 2026-05-20 15:40 UTC = 10:40 CDT
- So ~5.5 hours from launch until quota wall, then 2h until reset
- The inner loop kept calling Haiku through batches 14-16 because it didn't
  know to wait for the reset — it just slept 20 min between batches and
  burned attempts. **This is a flaw in the loop logic**: it should detect
  rate-limit events and sleep until reset.

### Output produced

| Metric | Value |
|---|---|
| Batches with results JSON | 16 (batches 0001-0016) |
| Edge files emitted | 375 .edges.jsonl |
| Buckets touched | 85 |
| Total Haiku spend (estimated) | ~$38 (batches 0001-0013 active work) |
| Rate-limit events logged | 36 |

The 16 results JSONs are in `working/missions/2026-05-19-stage4-haiku/results/`.
Edge files are in `working/wiki/pass2-buckets/<bucket>/prose-edges-haiku/<slug>.edges.jsonl`.

### Per-batch decision profile (sample)

batch-0005: emit_edge 150, reject_just_mention 676, escalate_cross_identity 8 ($3.23)
batch-0006: emit_edge 124, reject_just_mention 375 ($2.88)
batch-0007: emit_edge 202, reject_just_mention 174, escalate_disambiguation 1 ($3.27)
batch-0008: emit_edge 147, reject_just_mention 278, escalate_disambiguation 1 ($2.77)
batch-0009: emit_edge 252, reject_just_mention 380, escalate_disambiguation 1 ($3.40)
batch-0010: emit_edge 350, reject_just_mention 413 ($3.23)
batch-0011: emit_edge 256, reject_just_mention 558, escalate_cross_identity 2 ($3.36)
batch-0012: emit_edge 117, reject_just_mention 229, escalate_cross_identity 2 ($2.83)

**emit/reject ratio averages ~30/70.** Reject-rate is high partly because
co-presence rejections under Rule 6 (and pre-existing KNOWS rejections) work
as designed.

---

## Throughput analysis — why so slow

### Cost per batch
~$2.80–$3.40 (mean ~$3.10). Stable; not the bottleneck.

### Wall-clock per batch (active work)
- 4 concurrent chunks × ~150-200s per chunk = ~7-9 min total
- Plus 20-min `STAGE4_HAIKU_SLEEP_BETWEEN` sleep
- **Total wall-clock per batch: ~28 min**

### Claude Code 5h quota wall
- The bottleneck is NOT API rate-limit-per-second. It's the Claude Code
  subscription's **per-5h-window total token quota**.
- At ~$3/batch × 12 batches = ~$36 worth of Haiku tokens per 5h window
- Sleeping 20 min between batches does NOT increase what fits in the window.
  Active work fills the same total quota regardless of how it's paced.

### Projection at current pace
- 12 batches per 5h window, then 5h sleep until reset
- 12 batches per 10h cycle = 28.8 batches/day
- 1089 batches / 28.8 = **37.8 days** to finish
- Cost: 1089 × $3.10 = **$3,376** in Haiku spend
- That's ignoring the overhead of restart, supervision, error recovery

This is the "absurdly painful process" you flagged.

---

## Speed levers — ranked by leverage

### LEVER 1: Remove the inter-batch sleep ★★★★★ (biggest immediate win)

Set `STAGE4_HAIKU_SLEEP_BETWEEN=60` (one minute, just enough to flush logs
and check stop-file). With 8-min active work + 1-min sleep, you fit ~33
batches per 5h window vs. 12 today. **Almost 3x throughput per window.**

Cost-neutral — you're using the same quota faster, not paying more per batch.

```bash
STAGE4_HAIKU_SLEEP_BETWEEN=60 bash scripts/stage4-haiku-run-forever.sh batch-0017
```

Projection at this pace: 1089 batches / ~66 batches/day = **~16.5 days.**

### LEVER 2: Have the loop wait for rate-limit reset, not just sleep ★★★★

The inner loop currently treats a rate-limited batch as "completed with 0
files" and continues. It should instead:

1. Detect rate-limit events in `rate-limit-events.jsonl` after each batch
2. If the batch had ANY rate-limit events, parse the reset timestamp
3. Sleep until reset + 60s buffer, then resume

This prevents the wasted batches-14-15-16 pattern where the loop kept
trying for 60 min while quota was exhausted.

**Code change required** in `scripts/stage4-haiku-loop.sh`. ~30 min of work.
Massive throughput improvement when combined with LEVER 1 — no wasted
post-quota attempts.

### LEVER 3: Increase chunk-size ★★★

Default is 3 files per Haiku call. Per the Session 61 continue prompt:
"Chunk-size sweep on a BIG batch (batch-0020 = 30 files; the 8-wave
batches were 5 files each = single chunk, so chunk-15 never actually
bound)." Larger chunks (5-10 files) reduce total Haiku invocations,
which reduces per-call overhead (each call has prompt-rendering, tool
authentication, etc. fixed cost).

Risk: each chunk now consumes more context per call. Validate quality
doesn't degrade.

```bash
STAGE4_HAIKU_CHUNK_SIZE=5 bash scripts/stage4-haiku-run-forever.sh batch-0017
```

### LEVER 4: Concurrency above 4 ★★

Current default is 4. The script supports higher. Tradeoff: more parallel
calls hit rate-limit faster within the 5h window, but also finish each
batch faster. **Likely net-neutral** with quota-bounded throughput — you
get the same total batches per window. Worth testing at concurrency=6 or
8 to see if it surfaces quality issues.

### LEVER 5: Anthropic Batch API (structural fix) ★★★★★ but expensive to build

Anthropic's Message Batches API processes batches asynchronously at **50%
discount** with **no interactive rate-limit**. Submit up to 100k requests,
get results within 24h.

Pros:
- Cost: $3,376 → $1,688
- Time: 1089 batches submittable in ~hours; results back same-day
- No more 5h quota walls

Cons:
- Requires rewriting `stage4-haiku-run.py` to use the Anthropic SDK
  directly instead of `claude` CLI subprocesses
- Different output format — would need an adapter to fit into the existing
  `working/missions/.../results/` + per-bucket `.edges.jsonl` layout
- Lose Claude Code's prompt-caching, tool-result feedback, etc.
- Engineering: ~1-2 days of focused work

**Prior history — re-check before dismissing.** Batch API was floated in
Session 34 (2026-05-04, `history/session-details/session-034.md` line 93)
as one of 8 brainstorm ideas to halve weekly burn. **It was deprioritized
at the time, NOT investigated and rejected.** Matt's memory of "we looked
at it and it wasn't feasible" likely conflates two real blockers:

1. **Batch API doesn't support tool use.** The current Stage 4 Haiku worker
   uses the `Read` tool to load candidate files + node prose + alias maps
   during classify. A pure prompt-in → response-out API can't do that.
2. **This blocker is COUPLED to the pre-loading re-architecture** (also
   discussed in Session 61's continue prompt as the "deepest speed/cost
   lever" — inline candidate rows + node prose into the prompt so Haiku
   does zero reads at classify time).

In other words: **Batch API + pre-loading = single architectural change,
evaluated as a package, not independently.** Without pre-loading, Batch
API is infeasible. With pre-loading, it becomes feasible AND captures
the prompt-caching benefit even on the interactive path.

**Recommendation:** evaluate after LEVER 1 + 2 are in place. If those get
us to 2-week finish, maybe acceptable. If we're still looking at >3 weeks,
the pre-loading + Batch API package becomes the right next investment.

### LEVER 6: Reduce scope ★★★

Do we need all 1089 batches? Some categories:

- **`battles-*` buckets** (~200-300 batches): rich relational data, high value
- **`characters-house-*` buckets** (~400+ batches): some sparse minor houses,
  could defer the tail
- **comention batches** (per-chapter pairs): potentially huge but might be
  noisy
- **pass1_relationship batches**: low cost per batch (small)

Triage strategy: process battle/major-house buckets first, defer minor-house
+ low-value comention batches to a v2 pass. Get 60% coverage in 30% of the
cost.

**Discuss this with Matt before acting** — scope is his decision.

---

## What the next session should do (decision tree)

### Step 1: Validate the 375 fresh files

```bash
python3 scripts/wiki-pass2-validate-edge-jsonl.py \
    --arch reference/architecture.md \
    --qualifier-vocab reference/edge-qualifier-vocab.md \
    --graph-nodes graph/nodes \
    $(find working/wiki/pass2-buckets -path '*/prose-edges-haiku/*.edges.jsonl' \
        -not -path '*/_archive/*' | sed 's/^/--file /') \
    2>&1 | grep -oE '\[[a-z-]+\]' | sort | uniq -c | sort -rn
```

**Pay particular attention to:**
- `verb-gate-failure` — should be near 0 if Rule 6 is working in production
- `edge-type-not-canonical` — should be near 0 (vocab is now comprehensive)
- `type-contract-violation` — pre-existing background level expected, but
  watch for new patterns in the 5 new types' contracts
- New emit types: count `IMPRISONED_AT`, `TRAVELS_WITH`, `PRISONER_EXCHANGE_FOR`,
  `GUARDS`, `ENCOUNTERS` rows to confirm Haiku reaches for them when appropriate

### Step 2: If validation surfaces patterns, decide whether to harden prompt

If e.g. ENCOUNTERS is being emitted for things it shouldn't (verb gate not
caught because Haiku found a workaround verb), add more anti-fallback
language to Rule 6. Worth one more round of prompt-hardening before
scaling further.

### Step 3: Decide throughput strategy

Discuss with Matt:
- LEVER 1 (zero sleep) — fastest to deploy, ~3x throughput
- LEVER 2 (reset-aware sleep) — pairs with LEVER 1 for clean overnight
  unattended runs
- LEVER 5 (Batch API) — engineering investment, much faster + cheaper
- LEVER 6 (reduce scope) — strategic, get 60% in 30% of cost

The right answer probably combines LEVER 1+2 for the next overnight,
*then* evaluate whether Batch API is worth building.

### Step 4: Commit Session 61 work + write Session 61/62 worklog entry

The vocab work + loop infrastructure is uncommitted. Group as one logical
commit ("Stage 4 Haiku: vocab 159→164 + verb-gate schema enforcement +
overnight bulk-run plumbing"). Then write the worklog entry covering
Sessions 61 + 62 together (or split if substantive enough).

The previous overnight continue prompt at
`progress/continue-prompts/2026-05-20-stage4-haiku-overnight-watch.md`
should be DELETED — its decision tree is stale; this prompt supersedes it.

### Step 5: Resume the run with new settings

After LEVER 1 + 2 are deployed:

```bash
# Resume from batch-0017 (or wherever validation says to start fresh)
STAGE4_HAIKU_SLEEP_BETWEEN=60 bash scripts/stage4-haiku-run-forever.sh batch-0017
```

---

## Files modified Session 61 (uncommitted vs HEAD)

```
# Vocab + schema work
M reference/architecture.md
M .claude/commands/stage4-haiku-classify.md
M .claude/agents/prose-edge-classifier.md
M scripts/wiki-pass2-validate-edge-jsonl.py
M scripts/stage4-haiku-normalize-edge-types.py
M scripts/stage4-haiku-residual-resolve.py
M scripts/stage4-haiku-run.py

# Regenerated vocab reference file
M working/missions/2026-05-19-stage4-haiku/locked-edge-vocab-159.md
  (filename stays as -159 per stage4-haiku-run.py hardcoded reference;
   content auto-regenerates to 164 entries)

# New loop infrastructure
?? scripts/stage4-haiku-loop.sh
?? scripts/stage4-haiku-run-forever.sh

# Archived old Haiku output (pre-vocab-164)
?? working/wiki/pass2-buckets/_archive/haiku-pre-vocab164-2026-05-20/

# New mission outputs (overnight run)
?? working/missions/2026-05-19-stage4-haiku/loop-logs/
?? working/missions/2026-05-19-stage4-haiku/rate-limit-events.jsonl
+ 375 new .edges.jsonl files under working/wiki/pass2-buckets/<bucket>/prose-edges-haiku/
+ 16 batch results in working/missions/2026-05-19-stage4-haiku/results/
+ run-summary.json in working/missions/2026-05-19-stage4-haiku/

# Continue prompts
?? progress/continue-prompts/2026-05-20-stage4-haiku-overnight-watch.md  (STALE — delete)
?? progress/continue-prompts/2026-05-20-stage4-haiku-throughput-and-resume.md  (THIS FILE)
```

---

## Memories added Session 61

- `feedback_print_questions_on_chat.md` — re-print AskUserQuestion options
  verbatim when user picks "chat about this"
- `feedback_iterm_cwd_wrapper.md` — iTerm cwd is `/Users/mnoth/source/`,
  not the project dir; use a `/tmp/run-XYZ.sh` shell wrapper, not inline
  cd in osascript

Memories that may want to be added Session 62 based on this work:
- The 5h quota wall behavior + the loop's failure mode of "wasting batches
  while waiting for reset" (recommend creating `project_haiku_5h_quota_wall`
  memory after LEVER 2 is built)
- The "sleep doesn't increase throughput, quota does" insight
  (`project_quota_not_rate_limit` or similar)

---

## /endsession status

**Session 61 NOT yet /endsession'd.** Matt went to bed mid-session and ran
the overnight in the background. The worklog entry has not been written.
When the next session finishes triage + decides next-step, run /endsession
with explicit permission and roll Sessions 61 + 62 together into the
worklog (or split if substantial enough).

---

## Stop sequences (still valid)

- Graceful: `touch /tmp/stage4-haiku-stop` — current batch finishes; outer
  wrapper exits cleanly
- Hard: kill the run-forever.sh PID — outer wrapper tries to relaunch unless
  stop file is also touched
- Resume from specific batch: `bash scripts/stage4-haiku-run-forever.sh batch-NNNN`
