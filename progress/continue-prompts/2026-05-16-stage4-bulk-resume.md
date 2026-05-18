# Stage 4 Bulk Run — Resume in One Terminal

> **Continue prompt — self-contained for a fresh session.**
>
> **Recommended model:** Sonnet 4.6 (`claude-sonnet-4-6`) for workers (~$3.42/batch, ~20-25 min each). Orchestrator/auditor: Opus 4.7 if you need it for checkpoint reviews, but the workers run themselves via `/loop 20m /worker-stage4` and don't need Opus.
>
> **Drafted:** 2026-05-16 end-of-session. 21 batches done out of 201 (10%). 180 remaining. Spend so far ~$37 (sessions 53-55 combined).

---

## Goal

Resume the Stage 4 v1 bulk classification on Sonnet 4.6, processing the 180 queued batches one at a time in a single terminal via the `/worker-stage4` slash command + `/loop` cadence. Accept the 5-7% baseline error rate; build a "suspicious-edges" worklist for later Opus review.

This is **Path 1** from Matt's decision (keep firing, accept baseline, build post-cleanup mechanism rather than blocking on schema-lockdown).

## Mission context

- Mission: `2026-05-14-stage4-v1-bulk-sonnet`
- Mission dir: `working/missions/2026-05-14-stage4-v1-bulk-sonnet/`
- Manifest: **21 done / 180 queued** (all 180 are tier-1 source_target, except a few tier-2/3/4 comention + pass1 batches at the end of the queue)
- Worker NOT running. Stop file `/tmp/stage4-stop` is removed. Locks dir is empty.
- Recent batches under the strengthened prompt: 0019/0020/0021 all CLEAN per validator, with KNOWS soft-fallback observed in 0020 (Frey-t-z bucket). See `working/session-results/2026-05-16-stage4-bulk-run-checkpoint.md` for the full per-batch table.

## What to do

### Step 1 — Fire up one worker terminal

Open a fresh Claude Code session (or use this one), set model to Sonnet 4.6, then run:

```
/loop 20m /worker-stage4
```

The 20-minute loop cadence matches the ~15-25 min per-batch runtime. Each loop iteration: worker claims the next queued batch via lock file, processes 30 files, runs validator, marks done, releases lock, exits. The loop re-fires every 20 min until no batches remain or you stop the loop.

**The `/worker-stage4` slash command is pre-built** at `.claude/commands/worker-stage4.md`. It pastes in the full worker body from `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`.

### Step 2 — Monitor (light-touch)

While the loop runs, check progress every ~30-60 min:

```bash
# Manifest status
python3 -c "
import json
done = queued = 0
for l in open('working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl'):
    if not l.strip(): continue
    r = json.loads(l)
    if r['status'] == 'done': done += 1
    elif r['status'] == 'queued': queued += 1
print(f'{done}/{done+queued} done, {queued} queued')
"

# Locks (should normally be 0 or 1 = current worker)
ls working/missions/2026-05-14-stage4-v1-bulk-sonnet/locks/

# Latest batch results
ls -t working/missions/2026-05-14-stage4-v1-bulk-sonnet/results/ | head -5
```

If a lock file is **older than ~45 minutes** AND no worker is running, the worker probably died (rate limit, network glitch). Delete the stale lock + leave the batch as-is (next worker will re-claim it).

### Step 3 — Validator + spot-audit per N batches

Every ~5 batches, run the independent validator + a quick type-contract audit:

```bash
# Validator on a specific batch
python3 scripts/wiki-pass2-validate-edge-jsonl.py --batch-id batch-NNNN --mission working/missions/2026-05-14-stage4-v1-bulk-sonnet
```

The worker runs the validator before marking done, so it should always be CLEAN. If it's NOT clean post-worker, that's a worker bug — investigate.

### Step 4 — Build the "suspicious edges" worklist (Matt's idea — implement BEFORE resuming bulk if possible)

**Status: implemented in Session 55 end-of-session.** Script lives at `scripts/wiki-pass2-flag-suspicious-edges.py`. Re-run periodically during bulk:

```bash
python3 scripts/wiki-pass2-flag-suspicious-edges.py
# Outputs:
#   working/wiki/data/stage4-suspicious-edges.jsonl   (full flagged rows + enrichment)
#   working/wiki/data/stage4-suspicious-edges-summary.md  (counts + samples per pattern)
```

Baseline (21 batches, 9,705 rows): 291 flagged (~3%). Dominant patterns: `knows-without-knowing-prose` (182), `contemporary-with-character-target` (40), `target-type-mismatch-attends` (30). Watch for new patterns and rate spikes.

Original spec (kept for reference):

1. Walks all emit_edge rows across all completed batches
2. Tags rows matching these patterns (does NOT block them — flags them):
   - `KNOWS` with no explicit "X knows Y" prose in the snippet (soft-fallback signal) — heuristic: snippet doesn't contain "knew", "known", "learned of", "informed", "told"
   - `ATTENDS` with target type not starting with `event.*`
   - `FIGHTS_IN` with target type not `event.*` or `organization.*`
   - `TRAVELS_TO`, `LOCATED_AT`, `BORN_AT`, `DIED_AT` with target type not `place.*`
   - `SPOUSE_OF` with target type not `character.*`
   - `WIELDS` with target type not `object.artifact`
   - `confidence_tier: 3` rows (model self-flagged as low confidence)
   - `CONTEMPORARY_WITH` with target type `character.*` (any character-pair CONTEMPORARY is suspicious per the patched prompt)
3. Writes flagged rows to `working/wiki/data/stage4-suspicious-edges.jsonl` with the original row + the matched pattern names
4. Produces a summary report at `working/wiki/data/stage4-suspicious-edges-summary.md`: count by pattern, sample rows per pattern

Then a future Opus-audit task processes `stage4-suspicious-edges.jsonl` in chunks and either confirms or retracts each flagged edge. This is the **durable answer to "schema lockdown"** — we don't lock the prompt, we lock the audit pipeline.

Optionally: run the flag-script periodically during bulk (every ~10 batches) to watch the suspicious-edge rate. If it spikes (e.g., a new failure mode), pause + investigate.

### Step 5 — Bulk done? Run the cleanup pipeline

When all 201 batches are done:

1. **cross-identity-detector** processes the 4+ cross-identity escalations across the session.
2. **Opus suspicious-edges audit** processes the worklist from Step 4.
3. **prose-edges promoter** (`scripts/wiki-pass2-promote-prose-edges.py` — write this script if it doesn't exist yet) reads accepted edges from per-batch JSONLs and appends them to node bodies under `## Edges (prose-derived)`. Skips suspicious-edges until the Opus audit confirms or retracts them.
4. **Stage 4 done.** Move to Pass 3+ planning (voice analysis, foreshadowing, theory-informed extraction).

## Known issues to watch for during the bulk run

### Issue 1 — Soft-fallback whack-a-mole

The model finds new soft-fallback types each session:
- batch-0014 (pre-patch): CONTEMPORARY_WITH at 14 emits
- batch-0018 (post-patch-1): CONTEMPORARY_WITH at 21 emits (regression in dense bucket)
- batch-0020 (post-patch-2): KNOWS at 163 emits / 37% of all emits (new fallback)

Future batches may surface MORE patterns (ALLIES_WITH-as-default, SERVES-as-default, RELATED_TO if it gets invented). The validator's suspicious-flag check (Step 4) is the right defense. Don't patch the prompt reactively each time — let it ride and flag for review.

### Issue 2 — Schema-repair episodes

batch-0019 + 0020 had schema-repair episodes — worker emitted with missing required fields, validator caught it, worker wrote post-hoc Python to repair. The repaired output is acceptable but the underlying drift means each new worker session re-derives schema understanding from the prompt. The validator is what holds it.

If you see a worker spending a long time on "schema repair" before completing, investigate — the repaired metadata (especially `confidence_tier` if auto-assigned) may not reflect the model's actual reasoning, just a default. Acceptable but worth knowing.

### Issue 3 — Dense-kinship buckets are higher error

Frey buckets (batches 0018, 0019, 0020) had the highest error rates. Lannister, Stark, Tyrell, Targaryen, Bolton buckets are also dense and likely will too. Don't be surprised by a spike in those batches.

### Issue 4 — Graph-typing mismatches inflate type-contract counts

Some graph nodes are typed in ways that conflict with the edge contracts:
- `kingsmoot` typed as `concept.culture` but actually an event
- `trial-by-combat` typed as `concept.custom` but the specific Vardis-vs-Bronn trial is an event
- `209-ac` typed as `character.human` (parsing bug for year-pages)

These cause type-contract false-positives in audits. A separate graph-cleanup pass can re-type these correctly. Don't blame the classifier for them.

## Decisions Matt deferred from Session 55

- Re-run batch-0018 or leave as-is? (Has ~18 wrong CONTEMPORARY_WITH edges.) **Recommend: leave for now, retract via the suspicious-edges pipeline post-bulk.**
- batch-0019 and batch-0020 schema-repair episodes — accept the repaired output. **Done implicitly.**
- 4 pending vocab gaps from prior session beyond the 7 already added (CROWNS_QUEEN_OF_LOVE_AND_BEAUTY rejected; OFFERED_AS_BRIDE / CONSPIRES_WITH / HOSTAGE_OF surfaced in audit). **Recommend: defer until bulk done; add together once we see them at scale.**

## Cost budget

- Spent so far: ~$37
- Remaining: 180 batches × ~$3.42 = ~$615
- Total Stage 4 v1: ~$650

If you want to throttle: Matt has lots of weekly usage but the 5h sliding window may hit. The `/loop 20m` cadence + sequential single-worker config naturally throttles — if you hit limits, the loop pauses on next firing and you can resume later.

## Do NOT

- Don't run multiple parallel workers in different terminals — lock conflicts + stale locks + race conditions. Stick to single-terminal sequential.
- Don't run `/endsession` without Matt's explicit per-turn permission.
- Don't auto-resolve cross-identity escalations — that's a separate Stage 4 sub-pipeline (`cross-identity-detector` + `cross-identity-reviewer`).
- Don't patch the prompt reactively for every new soft-fallback you discover. Use the suspicious-edges worklist instead. The prompt is "done" — it's the audit that takes over.
- Don't read or surface anything from `scratch` or `scratch-do-not-delete.txt` — Matt's private notes.

## Files for the record

- Mission state: `working/missions/2026-05-14-stage4-v1-bulk-sonnet/`
- Classifier prompt: `.claude/agents/prose-edge-classifier.md` (patched Session 55 with Common failure patterns section)
- Worker template: `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md`
- Worker slash command: `.claude/commands/worker-stage4.md`
- Validator: `scripts/wiki-pass2-validate-edge-jsonl.py`
- Architecture: `reference/architecture.md` (~132 canonical edge types after Session 55)
- This session checkpoint: `working/session-results/2026-05-16-stage4-bulk-run-checkpoint.md`
- Status + open questions: `working/session-results/2026-05-16-stage4-current-status-and-open-questions.md`
- Provenance explainer: `working/session-results/2026-05-15-stage4-edge-provenance-explained.md`
- Drift detection rule (memory): `feedback_drift_detection_mandatory.md`

## Related references

- Mission spec: `working/agent-fleet-specs/missions/2026-05-14-stage4-v1-bulk-sonnet.md`
- Vocab candidates ledger: `curation/edge-vocabulary-candidates.md`
- Architecture changelog: Sessions 53 (14 types added) + 54 (4 types added) + 55 (7 types added) = vocab grew from ~96 → ~132
