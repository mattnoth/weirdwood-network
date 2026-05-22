# Stage 4 Bulk Relaunch — FIRE FIRST THING (Session 64 resumption)

> **Recommended model: Sonnet 4.6** — this is launch + monitor ops, not strategic. The decisions are made. Upgrade to Opus 4.7 only if a quality bug surfaces requiring deep debug.

> **Where we are:** Session 63 (2026-05-21) shipped the enriched-candidate pipeline. Smoke on batch-0019 was green (4.6 min, $2.73, 2.80% violation rate — better than overnight baseline on all three axes). Pipeline ready to bulk-run Tier 1 (222 high-value batches, Option C scope).

---

## Action: FIRE THE BULK FIRST THING THIS SESSION

**Matt's instruction at end of Session 63:** "I want to run batches overnight with sleep timer first thing next session, regardless of time."

Translation: regardless of when this session opens, the FIRST action is to launch the Tier 1 bulk run. Per the standing rule (`feedback_no_extraction_without_asking`), confirm with Matt before pasting — but the decision is already made; this is just final-confirmation hygiene.

### Launch command (paste in iTerm or background)

```bash
cd /Users/mnoth/source/asoiaf-chat
rm -f /tmp/stage4-haiku-stop

STAGE4_HAIKU_SLEEP_BETWEEN=60 \
STAGE4_HAIKU_CHUNK_SIZE=5 \
STAGE4_HAIKU_CONCURRENCY=4 \
STAGE4_HAIKU_BATCH_LIST=working/missions/2026-05-19-stage4-haiku/option-c-batch-order.txt \
  bash scripts/stage4-haiku-run-forever.sh batch-0019
```

**Why these env values:**
- `SLEEP_BETWEEN=60` — Matt explicitly asked for "sleep timer". LEVER 1's proven-safe value (overnight ran at 60s; smoke ran at default which orchestrator handles independently). Lower (e.g., 10s) saves wall-clock but burns rate-limit faster; higher (e.g., 300s) is more conservative. Adjust if Matt wants different.
- `CHUNK_SIZE=5` — smoke proved 30 files / 6 chunks at 4.6 min total. chunk=3 was 9 min. **Use 5.**
- `CONCURRENCY=4` — Matt said "brutal on usage but we can try it." Smoke at conc=4 had 0 rate-limit events. If bulk hits rate-limit too fast, drop to 2. Don't preempt — let it run.
- `BATCH_LIST=option-c-batch-order.txt` — 222 prioritized batches (battles + major houses + major characters + pass1 extractions + meta-chapters). Loop reads this instead of manifest order.
- Arg `batch-0019` — sticky resume value; ignored when BATCH_LIST is set (the loop reads the file).

### Expected per smoke baseline

- 4.6 min/batch wall-clock
- 222 batches × 4.6 min ≈ 17 hours of Haiku work
- Split across 5h interactive windows ≈ 4 windows
- ~24-30 hours elapsed with rate-limit waits

### Monitor in a second iTerm tab

```bash
tail -F working/missions/2026-05-19-stage4-haiku/loop-logs/loop-*.log | \
  grep -E "Batch [0-9]|rate.limit|done\]|ERROR|WARN"
```

### Stop cleanly

```bash
touch /tmp/stage4-haiku-stop
```

(LEVER 2 rate-limit-aware loop handles 5h wall recovery automatically — no need to babysit.)

---

## What got done in Session 63 (summary for cold-start context)

Three commits landed on origin/main:

1. **`bd2d05903`** — Heavy ENCOUNTERS hardening + KNOWS deprecation (vocab 164→163) + Option C scope (222 high-value batches).
2. **`caf8dcc79`** — Candidate enrichment pipeline. New script `scripts/wiki-pass2-enrich-candidates.py` walks all 479 buckets, rewrites 5,686 candidate files to `prose-edge-candidates-enriched/` with per-row `target_type`, `evidence_paragraph` (clean prose), `valid_edge_types`, `staging_verbs_present`. Haiku no longer reads source/target node files. Classify prompt + orchestrator updated to route to enriched paths. +18 tests (90 total).
3. Tests passing: `python3 -m unittest discover tests` → 90 OK.

**Smoke verdict (batch-0019, chunk=5, conc=4, enriched):**

| Metric | Overnight baseline | Smoke | Δ |
|---|---|---|---|
| Wall-clock | 9.0 min | 4.6 min | **-49%** |
| Cost | $3.36 | $2.73 | **-19%** |
| Violation rate | 3.96% | 2.80% | **-29%** |
| Files written | 30/30 | 30/30 | clean |
| Rate-limit events | 0 | 0 | clean |

vs Sonnet original (~25-28 min/batch): **~5.5× faster.**

---

## What's deferred (do NOT do unless explicitly asked)

- **F5 (locked-vocab compression in classify prompt)** — would save ~$5-6 across full bulk. Not worth 2-4 hrs of delay. The per-row `valid_edge_types` already does most of F5's job. **Revisit only if mid-bulk evidence shows vocab bloat is hurting throughput or quality** (e.g., if per-call wall-clock creeps up significantly).
- **Full 1077-batch Option A** — at enriched-Haiku rates this is now ~10 days, viable. Decide after Tier 1 lands. Don't preempt Matt's scope call.
- **KNOWS verb-gate retrofit** — same pattern as ENCOUNTERS but KNOWS is deprecated; moot.
- **F4 (Python-side pre-classification)** — risky semantic-decision delegation. Don't.
- **F6 (Python pre-rejection signals)** — risky. Don't.

---

## After bulk relaunch fires

- Track per-batch metrics (wall-clock, cost, violation rate) as they land
- After first 5-10 batches, check the run-summary aggregates:
  - Wall-clock holding near 4.6 min? (If creeping up to 9+, something regressed.)
  - Violation rate holding near 2.80%? (If spiking to 5%+, prompt drift.)
  - ENCOUNTERS verb-gate-failures decreasing as a % of emits? (Smoke had 14/715 ≈ 2.0%; bulk should match or improve.)
- If quality drift detected: stop the loop via `touch /tmp/stage4-haiku-stop`, investigate, fix, re-fire.
- After Tier 1 (222 batches) completes, Matt decides:
  - Stop here (Tier 1 was the deliverable)
  - Extend to Tier 2 (medium-value buckets, ~364 batches, ~28 more hours)
  - Extend to Tier 3 (low-value tier3-*, ~491 batches)
  - Run Option A (full 1077 = Tier 1+2+3)
- **Write `working/session-results/<date>-stage4-bulk-relaunch.md`** with status when bulk completes (Tier 1 or whichever scope landed). Format per `working/session-results/README.md`.

---

## Cold-start verification (run before launching)

```bash
# Tests pass
python3 -m unittest discover tests
# expected: Ran 90 tests in <10ms, OK

# Enriched candidates in place
ls working/wiki/pass2-buckets/characters-house-cassel/prose-edge-candidates-enriched/ | wc -l
# expected: 4

# Option C list present
wc -l working/missions/2026-05-19-stage4-haiku/option-c-batch-order.txt
# expected: ~230 lines (222 batches + header comments)

# Nothing currently running
ps aux | grep -E "stage4-haiku|claude.*haiku" | grep -v grep
# expected: no output

# Stop file absent
ls /tmp/stage4-haiku-stop 2>&1
# expected: No such file

# Worklog has 5 entries
grep '^### Session' worklog.md | wc -l
# expected: 5
```

---

## If anything looks wrong cold-start

The continue prompt is a snapshot. If `worklog.md` says something different about completion state, **trust worklog.md and flag the contradiction** (per CLAUDE.md rule #9). The most up-to-date state of the project always lives in `worklog.md`, not in continue prompts.

The smoke-validation data is in `working/missions/2026-05-19-stage4-haiku/results/batch-0019.json`. The enriched candidates are at `working/wiki/pass2-buckets/*/prose-edge-candidates-enriched/` (gitignored — regenerate with `python3 scripts/wiki-pass2-enrich-candidates.py --apply` in ~13s if missing).
