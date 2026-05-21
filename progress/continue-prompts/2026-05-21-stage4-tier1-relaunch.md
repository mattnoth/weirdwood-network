# Stage 4 — Tier-1 Relaunch + ENCOUNTERS Hardening + Scope Decision (Session 63 resumption)

> **Recommended model: Opus 4.7** for the ENCOUNTERS prompt hardening + the scope-reduction strategic call. After those are settled, Sonnet 4.6 is fine for the mechanical Rule-6 prompt-text edit + relaunch ops.

> **Where we are:** Sessions 61-62 closed. LEVER 2 (rate-limit-aware loop + orchestrator `--skip-existing`) is shipped, tested, pushed. 71 Python tests bootstrapped. Quality analysis vs Sonnet done. **The next bulk run should give ~3× per-window throughput**, but two issues block firing it confidently: (a) the LEVER 1 env-var change hasn't happened, (b) ENCOUNTERS verb-gate fails 80% of the time, wasting tokens on rejected emits.

---

## TL;DR

1. **LEVER 1** (env var only, 5 sec): set `STAGE4_HAIKU_SLEEP_BETWEEN=60` and relaunch the bulk run.
2. **ENCOUNTERS prompt hardening** (one round of Rule 6 strengthening before relaunch): 61/76 emissions failed the verb gate. Validator catches them; prompt isn't preventing them. Strengthen the anti-fallback language + add a rejection example.
3. **Matt's scope-reduction call** (LEVER 6): decide whether to triage 1089 batches to ~60% coverage (battles + major houses first; defer minor-house tail + low-value comentions) or run all 1089.
4. **Relaunch** with LEVER 1 + 2 in effect. Expected: ~33 batches per 5h window vs the 12 we got. ~16.5 days at current cost ($3,200) — or fewer at reduced scope.

---

## What's done (don't redo)

### Sessions 57-58: Vocab lockdown
- 132 → 159 edge types in `reference/architecture.md`
- `reference/edge-qualifier-vocab.md`: 18 enum-bearing types (8 Tier-1 REQUIRED + 10 Tier-2 OPTIONAL)
- `notes` field deleted from emit_edge schema entirely
- Validator extended with type-contract + qualifier-enum + notes-rejection checks
- Suspicious-edges flagger with 6 pattern classes

### Session 58 STEP 2: [LINK] resolver
- 4,744 candidate files rewritten: `[LINK]` → `«anchor»` substitution
- `scripts/wiki-pass2-build-edge-candidates.py` patched for future generations

### Session 59-60: Haiku worker
- `scripts/stage4-haiku-run.py` Python orchestrator (concurrency, chunking, rate-limit detection)
- `.claude/commands/stage4-haiku-classify.md` thin classify-only prompt
- Deterministic edge-type normalizer (morphological only — no semantic remaps)
- No-silent-drop 6-stage pipeline with `unresolved-edges-log.jsonl`

### Session 61: Vocab 159 → 164 + verb gate + loop infra
- 5 new types: `IMPRISONED_AT`, `TRAVELS_WITH`, `PRISONER_EXCHANGE_FOR`, `GUARDS`, `ENCOUNTERS`
- CRITICAL RULE 6 — ENCOUNTERS verb gate (`met`/`meets`/`confronted`/`encountered`/etc.)
- `VERB_GATE` dict in validator — first time the lock-down covers verb gates as schema
- `stage4-haiku-loop.sh` + `stage4-haiku-run-forever.sh`
- Overnight launch → 12 batches + partial 13 + $38 spend + 363 edge files

### Session 62: LEVER 2 + tests
- Bash loop: rate-limit-aware, parses `resets_at_ts` from `rate-limit-events.jsonl`, sleeps until reset+60s, doesn't advance on rate-limit
- Orchestrator: `--skip-existing` CLI flag → `plan_batch_chunks(..., skip_if_output_exists=True)` filters files with existing outputs
- End-to-end verified: `batch-0001 --skip-existing --dry-run` → "skipped 30 file(s)" → 0 chunks
- 71 Python tests bootstrapped (`tests/`, stdlib unittest, no external deps)
- 3 regression tests freeze historical bugs (vocab parser 161→164, normalizer ATTACKED_BY over-reach, notes-field deletion)

---

## Pending decisions (for Matt)

### Decision 1: LEVER 6 — scope reduction

Run all 1089 batches, or triage?

- **Option A — full 1089.** ~16.5 days at LEVER-1+2 throughput. ~$3,200 cost.
- **Option B — triage to ~60% coverage.** Battle buckets first (~200-300, rich relational data), major-house buckets next (~150-200). Defer minor-house tail (~400+, sparse) + comention batches (per-chapter pairs, potentially noisy). ~6-10 days. ~$1,200-1,800 cost.
- **Option C — battle + major-house only, then re-evaluate.** Get the most-valuable ~30% done, then look at the data, decide whether the tail is worth running.

Recommend **Option C** — bounded commitment + informed by partial-corpus signal. But it's Matt's strategic call.

### Decision 2: ENCOUNTERS prompt hardening — how aggressive?

Two paths:

- **Light touch:** add 1-2 rejection examples + 1 sentence reinforcing "no verb = no ENCOUNTERS, full stop." Validator catches the rest.
- **Heavy touch:** add a `## When NOT to emit ENCOUNTERS` block with 4-5 concrete bad-prose patterns from the overnight run (e.g., "Both fought in the same campaign" → reject), modeled on the existing KNOWS-STOP block.

Recommend **heavy touch** — overnight evidence shows the validator is catching, but Haiku is wasting ~$0.30/batch on rejected emits. Heavier prompt = fewer rejected emits = lower cost AND better signal-to-noise in the output.

---

## Step-by-step plan for Session 63

### STEP 0: Verify the LEVER 2 loop fix mechanically (15 min)

Synthetic-fixture test to confirm rate-limit detection works:

```bash
# Create a fake batch result with rate_limit_events_count > 0 + a near-future reset_ts
# (See Session 62 detail file for the unittest pattern.)
# Confirm the loop sleeps until reset+60s and re-runs with --skip-existing.
```

Or skip — the unit tests cover the Python side and end-to-end smoke verified the orchestrator. Live test only if you want belt-and-suspenders.

### STEP 1: ENCOUNTERS prompt hardening (~20-30 min, Opus 4.7)

Edit `.claude/commands/stage4-haiku-classify.md` Rule 6:
1. Pull 5-10 example rows from `[verb-gate-failure]` violations in `/tmp/haiku-v164-validator.log` (or re-run validator if log gone).
2. Categorize the failure patterns (co-presence-in-campaign vs co-membership-of-faction vs same-chapter-mention vs ...).
3. Add a `## When NOT to emit ENCOUNTERS` block with the bad-pattern categories + counter-examples.
4. Rebuild `working/missions/2026-05-19-stage4-haiku/locked-edge-vocab-159.md` if needed (it's regenerated from architecture.md).
5. Smoke test on 1-2 buckets that had high ENCOUNTERS rates.

### STEP 2: Make the LEVER 6 scope call (Matt)

Pick Option A/B/C above. If B or C, build the prioritized batch list:

```bash
python3 -c "
import json
manifest = open('working/missions/2026-05-14-stage4-v1-bulk-sonnet/batch-manifest.jsonl')
for line in manifest:
    d = json.loads(line)
    bucket = d.get('files', ['?'])[0].split('/')[3] if d.get('files') else '?'
    if bucket.startswith('battles-') or bucket.startswith('characters-house-stark') or ...:
        print(d['batch_id'], bucket)
" | head -50
```

### STEP 3: LEVER 1 + relaunch (~5 min)

```bash
# Stop any current run
touch /tmp/stage4-haiku-stop

# Relaunch with low sleep
STAGE4_HAIKU_SLEEP_BETWEEN=60 bash scripts/stage4-haiku-run-forever.sh batch-0013
# (or whichever batch is next after triage)
```

Per LEVER 2, the loop will:
- Re-run batch-0013 with `--skip-existing` → just the 18 stragglers
- Advance to batch-0014 cleanly
- On hitting the 5h wall, sleep until reset+60s, NOT burn wasted attempts

### STEP 4: Monitor + iterate

Same patterns as before: tail `working/missions/2026-05-19-stage4-haiku/loop-logs/loop-*.log` in a separate terminal. Touch the stop file when you want to pause.

---

## Files modified in Session 62 (uncommitted? — NO, all pushed)

```
✓ scripts/stage4-haiku-loop.sh           — LEVER 2 patch (committed: ecd948f0c)
✓ scripts/stage4-haiku-run.py            — --skip-existing flag (committed: ecd948f0c)
✓ working/todos.md                       — LEVER 2 note (committed: ecd948f0c)
✓ tests/                                 — 71 tests, NEW (committed: e1da3c5db)
```

Plus Session 57-61 backlog committed across 6 prior commits this session (869b574f9 through fcf8a0be6).

All on origin/main.

---

## Open questions / risks

1. **Pre-loading + Batch API** (LEVER 5) — defer until after Tier-1 numbers settle. If post-LEVER-1+2 finish projection is <2 weeks, skip. If >3 weeks, build (1-2 day investment, 50% cost cut + no interactive rate limit).

2. **KNOWS verb-gate retrofit** — Session 58 audit showed 82.3% of KNOWS emits are fallbacks. Same pattern as ENCOUNTERS. Defer until ENCOUNTERS fix is proven; then apply the same VERB_GATE + Rule pattern to KNOWS.

3. **74 invented edge types** in the overnight output (~3.1% of emits). Mostly singletons but recurring: PURSUES 6×, KNOWS_OF 3×, HIRES 3×, DEFEATED 3×. Real vocab gaps the bulk run is surfacing. Decision: triage at the end of the full run, decide which (if any) to adopt as vocab 165, 166, ... rather than now.

4. **Test coverage gaps** — current 71 tests cover stage4 Python pipeline only. Future test passes could cover: chapter-splitter, wiki ingester scripts, candidate-builder. Low priority — those scripts haven't been the active fire.

---

## How to verify state cold-start

```bash
# Confirm tests pass
python3 -m unittest discover tests
# expected: Ran 71 tests in <10ms, OK

# Confirm git status clean
git status
# expected: nothing to commit, working tree clean (after committing this continue prompt)

# Confirm worklog has 5 entries
grep '^### Session' worklog.md | wc -l
# expected: 5

# Confirm archives
ls history/worklog-archives/
# expected: archive001.md ... archive012.md (012 now full at 5/5)
```
