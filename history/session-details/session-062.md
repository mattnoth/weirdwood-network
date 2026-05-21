---
session: 62
date: 2026-05-21
model: Opus 4.7
focus: Stage 4 — overnight Haiku triage + LEVER 2 ship + Python test suite bootstrap
---

# Session 62 — Stage 4 Triage + LEVER 2 + Test Bootstrap

## What this session covered

Three distinct workstreams in one session:

1. **Triage of Session 61's overnight Haiku run** — commit the uncommitted Sessions 57-61 backlog (4,753 modified files + 129 untracked spanning 5 sessions of work), delete orphan/partial batch outputs, run quality comparison across three corpora.

2. **LEVER 2 implementation** — make the bash loop rate-limit-aware so the next overnight run doesn't waste batches after the 5h quota wall.

3. **Python test suite bootstrap** — first-ever tests for this project. Matt's call after I told him the orchestrator skip-existing was true (it wasn't): "i think it's time we write some tests on the python parts of this."

## Commit triage (Sessions 57-61 backlog)

Found: Session 56 was the last commit, but Sessions 57, 58, 59, 60, 61 all had uncommitted work (vocab lockdown, Haiku worker, normalizer, loop infrastructure, overnight outputs). 4,753 modified files (most under `working/wiki/pass2-buckets/` — the [LINK]→«anchor» rewrite from Session 58). 129 untracked files (new scripts, mission outputs, session details, archives).

Split into **6 logical commits + pushed**:

1. `869b574f9` — Stage 4 lockdown: vocab 132→159 + qualifier-enum tiers + validator/flagger extensions (19 files)
2. `486948954` — Stage 4: resolve [LINK] placeholder → «anchor» across 4,744 candidate files
3. `5d8fbcf18` — Stage 4 Haiku worker: orchestrator + normalizer + residual + smoke scaffolding (17 files)
4. `07e50c5e4` — Stage 4 Haiku: overnight bulk-run plumbing (loop + run-forever wrapper)
5. `e20dc0277` — Stage 4 Haiku overnight run: 12 batches × ~30 files = 363 edges (post-cleanup) (635 files)
6. `fcf8a0be6` — Sessions 57-60 worklog + session details + continue-prompt rotation (11 files)

Plus this session's two commits:
7. `ecd948f0c` — Stage 4 LEVER 2: rate-limit-aware loop + orchestrator --skip-existing
8. `e1da3c5db` — Bootstrap Python test suite: 71 tests across 4 Stage 4 modules

## Pre-commit cleanup: orphan/partial batch outputs

Per Matt's instruction "If a batch made it half way through, idk, prob just delete it":

- **12 .edges.jsonl files deleted** from batch-0013 (the partial-batch — 12 done / 18 failed). Identified by parsing chunk-log Write tool_use calls minus failed_outputs.
- **4 result JSONs deleted**: `batch-001{3,4,5,6}.json` (batch-0013 partial; 0014/0015/0016 were $0 zero-yield wasted attempts after the wall).
- **40 run-logs deleted**: `batch-00{13,14,15,16}-chunk-*.jsonl` (10 chunks per batch).
- **Stale `run-summary.json`** deleted (overwritten per-invocation; final write was batch-0016's failure summary, misleading).
- Result: 363 edge files (12 successful batches × ~30 each) cleanly preserved.

## Quality comparison — three corpora

**Validator violation rates (apples-to-apples, stripping Sonnet's pre-lockdown schema-drift noise):**

| Corpus | rows | "quality" violations | rate |
|---|---|---|---|
| Haiku v164 (overnight, 12 batches) | 6,740 | 267 | 3.96% |
| Haiku pre-v164 (Sessions 59-60 smoke) | 1,752 | 47 | 2.68% |
| Sonnet control (Sessions 50-58) | 14,501 | ~619 | ~4.3% |

**Net verdict:** Haiku v164 ~on par with Sonnet, ~1.3pp behind its own pre-vocab-lock baseline (smaller sample, no Rule 6 ENCOUNTERS gate to fail).

**Wins from the vocab lock-down:**
- `notes` field cleanup: Sonnet 193 violations → Haiku v164 zero. Field gone, respected.
- Vocab breadth: Haiku uses 168 unique edge types (164 canonical + 4 invented) vs Sonnet 109. Expanded vocab is being used end-to-end.
- Qualifier-enum compliance: Haiku v164 `qualifier-not-in-enum=0` (vs Sonnet 380).
- Inflection drift caught: only 2 each of `TRAVELED_TO`/`ENCOUNTERED`. Way down.

**Losses / open issues:**
- **ENCOUNTERS verb-gate fails 80% of the time** (61 verb-gate violations / 76 ENCOUNTERS emissions). The gate IS catching the mis-emissions, but Haiku is still reaching for ENCOUNTERS without verb support. Validator works; prompt-level prevention doesn't. **Biggest finding.**
- 74 invented edge types (~3.1% of emits). Mostly singletons. Recurring: PURSUES 6×, KNOWS_OF 3×, HIRES 3×, DEFEATED 3×.
- 80 type-contract violations (~1.2% of emits) — wrong target type for edge.
- Slightly higher emit rate (35.0% v164 vs 31.7% pre-v164 vs 28.7% Sonnet) — Haiku more permissive. Recall vs precision is the open question.

## Throughput analysis — why only 12 batches overnight

From actual `chunk_timings` data:
- Per-batch active wall-clock: ~7.8 min mean (range 5.9-9.0)
- `STAGE4_HAIKU_SLEEP_BETWEEN` = 20 min between every batch
- **70.2% of the wall-clock was sleep, not work**
- 5h window ÷ (7.8 + 20) min = ~10.8 batches per window → matched the 12 we got
- 5h Claude Code quota wall hit mid-batch-13 at 08:35 CDT

**Matt's overnight observation explained:** Quota wall ALSO hit a SECOND window's worth (he saw 100% at wake-up). Likely cause: pre-bed Opus planning session left Window-A partially consumed; script ran through the last ~30 min of Window-A (no wall — Haiku alone didn't fill it) then ALL of Window-B (5h) until 08:35 CDT hit Window-B's 100%. Mission logs only captured ONE wall event because Window-A never crossed 100% on Haiku alone.

**Bottom line:** the 20-min inter-batch sleep is half the wall-clock and produces zero throughput benefit (quota is the binding constraint, not API rate-limit-per-second). LEVER 1 (drop to 60s) is a pure ~3× speedup.

## LEVER 2 implementation

**Design decision (Matt 2026-05-20):** on rate-limit reset, re-run the same batch with `--skip-existing` (not advance past it). The orchestrator now filters files whose `.edges.jsonl` already exists, so re-running batch-0013 processes only the 18 stragglers — no wasted tokens on the 12 already-done files.

I told Matt earlier that "the orchestrator already skips files whose .edges.jsonl exists." **That was wrong.** Caught it while reading `plan_batch_chunks` — the function had no skip filter. Surfaced the correction explicitly to Matt before adding the fix.

**Bash loop changes (`scripts/stage4-haiku-loop.sh`):**
- Switched `for batch in BATCHES` → `while idx < total` so the same batch can re-run after a rate-limit reset.
- After each batch, parses `rate_limit_events_count` from the result JSON. If > 0, looks up the latest `resets_at_ts` for that batch_id in `rate-limit-events.jsonl` and sleeps until `reset + 60s`.
- Reuses `sleep_with_stop_check` for graceful stop-file interrupts during long sleeps.
- `current_batch_attempt_count` tracks retries; re-runs pass `--skip-existing` to the orchestrator.
- Fallback: if no reset_ts found, uses fixed `STAGE4_HAIKU_RATE_LIMIT_SLEEP` (default 1h).

**Orchestrator changes (`scripts/stage4-haiku-run.py`):**
- New `--skip-existing` CLI flag.
- `plan_batch_chunks(..., skip_if_output_exists: bool = False)` filters out files whose output `.edges.jsonl` already exists non-empty.
- Wired through `run_batch`, `run_all_parallel`, and `main` paths.
- Emits INFO warning `skipped N file(s) whose output already exists`.

**End-to-end smoke verified:** `--batches batch-0001 --skip-existing --dry-run` → "skipped 30 file(s)" → 0 chunks (batch-0001 fully complete).

**Reset detection — how we know the 5h thing:** the Claude Code CLI explicitly emits stream-json `rate_limit_event` events with `resetsAt` (Unix timestamp), `rateLimitType: "five_hour"`, `status: "rejected"`. We don't guess. Captured at two levels: per-chunk stream logs + mission-level append log (`rate-limit-events.jsonl`).

## Python test suite bootstrap

First-ever Python tests for this project. Hermetic, stdlib `unittest`, no external dependencies, no subprocess to claude.

**Layout:**
- `tests/_helpers.py` — `load_script(name)` uses `importlib.util.spec_from_file_location` to load hyphenated script filenames (`stage4-haiku-run.py`) as Python modules without renaming.
- `tests/__init__.py` — empty, marks the package.

**Coverage — 71 tests across 4 Stage 4 modules:**

| Module | Tests | Notable |
|---|---|---|
| `test_stage4_haiku_run.py` | 21 | Test-drove the LEVER 2 fix (RED→GREEN). Covers `candidate_to_haiku_output` (3 shapes), `plan_batch_chunks` (chunking + skip-existing), `detect_rate_limit` (stream-json parsing), `verify_outputs`. |
| `test_validate_edge_jsonl.py` | 18 | **Regression-locks** the Session 60 vocab-parser bug (now 164 canonical, excludes LOCATED_IN / FOSTERED_BY). ENCOUNTERS verb gate freezeze. Notes-field-rejection. |
| `test_normalize_edge_types.py` | 11 | **Regression-locks** Session 60's normalizer over-reach: ATTACKED_BY MUST NOT be in ALIAS_TABLE (would silently launder semantic error → KILLED_BY); belongs in SEMANTIC_DISTINCT_TYPES. |
| `test_flag_suspicious_edges.py` | 21 | All 6 pattern detectors with inline fixtures. |

**Run:** `python3 -m unittest discover tests` (~7ms for full suite).

**Three regression tests freeze known historical bugs:**
1. vocab parser miscount (Session 60: 161→159; now 164)
2. normalizer ATTACKED_BY→KILLED_BY over-reach (Session 60)
3. notes-field deletion (Session 57)

## Pending work (deferred to next session)

1. **LEVER 1: drop `STAGE4_HAIKU_SLEEP_BETWEEN` 1200s → 60s.** Pure env-var change. Combined with LEVER 2 = ~3× per-window throughput.
2. **ENCOUNTERS prompt hardening** — 80% verb-gate-failure rate means Haiku wastes tokens on rejected emits. Rule 6 needs stronger anti-fallback example.
3. **LEVER 6 scope reduction call** — Matt's strategic decision: triage 1089 batches (battles + major-house first; defer minor-house tail + low-value comentions)?
4. **Batch API + pre-loading** (LEVER 5) — defer evaluation until after Tier-1 overnight numbers settle. If we're tracking <2 weeks, skip. If >3 weeks, build (1-2 day investment).
5. **KNOWS verb-gate retrofit** — VERB_GATE only covers ENCOUNTERS today. Session 58 audit showed 82.3% of KNOWS emits are fallbacks. Same pattern as ENCOUNTERS; same treatment owed.

## Memory rule observed

I corrected myself mid-session on the "orphan auto-skip" claim. Surfaced the correction explicitly rather than silently fix it. Per the memory rule on misstatements (no specific rule, but per general accuracy norms — and Matt's standing rule about not "narrating internal deliberation" — this counts as productive correction).

`/endsession` was explicitly authorized by Matt at session close — not auto-triggered.
