---
session: 98
date: 2026-06-15
title: "Script consolidation Session 1 — orchestration/pacer build + design-doc anti-drift convention"
model: claude-opus-4-8 (orchestrator) + script-builder subagent (build)
track: script-consolidation (continue-prompt 2026-06-15-script-consolidation.md, Session 1 of 2)
commit: this endsession commit
---

# Session 98 — Orchestration/Pacer Build (Session 1 of script-consolidation)

## Purpose

Execute **Session 1** of the two-session script-consolidation track per
`working/orchestration-pacer-design-2026-06-15.md` (§14 honest scope split). Session 1 = the part with
real correctness stakes: build the pacer + telemetry ledger + worker-contract template, folding in the
binding §13 M1–M4 amendments from the fresh review. Session 2 (mechanical cleanup/CLI/README) deferred.

## Startup reconciliation (CLAUDE.md rule #9)

The continue prompt and `worklog.md` were **consistent** — both named Session 1 (orchestration/pacer) as
the recommended next track. No contradiction.

One stale instruction caught: the continue prompt's **step 2 said "resolve §11 open questions with Matt
FIRST,"** but the design doc's **§12 records those were already resolved 2026-06-15 after fresh review**
(ledger = per-track files; pacer = advisory-only; default = sequential; v1 = report-only). Trusted the
updated doc; did NOT re-ask Matt. This is itself an instance of the drift the session later addressed.

## What was built (delegated to script-builder)

Heavy deterministic Python → delegated with a precise spec (all 6 input schemas mapped up front by the
orchestrator, plus the §13 M-amendments as hard requirements). Deliverables:

1. **`scripts/pace.py`** (Class A-pacer) — three faces:
   - `backfill` — normalizes 6 heterogeneous stat schemas → per-track `working/telemetry/<track>.jsonl`.
   - `report` — per-`(track, model, unit_type)` baselines + conservative `LONGRUN_SLEEP_BETWEEN` + honest
     M3 wall-cadence disclaimer. **v1 = report-only** (no ETA/headroom/concurrency — wall data too thin).
   - `emit_telemetry_row(...)` — importable helper workers call to append one atomic JSONL row/unit.
2. **Telemetry ledger** — schema (§5 + S6 `unit_type`) defined once in pace.py; backfilled to 484 rows
   across 9 tracks.
3. **`scripts/worker-template.py`** — copy-me reference worker implementing the §4 contract + §13
   amendments: resumable+idempotent (`--resume`), one bounded chunk → `exit(10)`, `exit(0)` on drain;
   **M2** atomic state writes (`os.replace`) + **O_EXCL** unit claiming; **M1** positive-wall `exit(2)`
   only on confirmed `"rateLimitType"` (crash otherwise) + writes `<track>.next-eligible`; **M4**
   single-worker-durable in v1 (multi-worker burst gated).
4. **`tests/test_pace.py`** — 40 tests (each schema, status-filter, dedup, header-drift, median).

## The 6 input schemas (the §14 time-sink)

| Source | Shape | Mapping notes |
|---|---|---|
| Pass-1 CSV 13-col (agot/asos/affc) | `chapter,book,…,cost_usd` | unit=chapter; model=opus (project fact) |
| Pass-1 CSV 16-col (acok/ADWD) | +`last_heartbeat,terminal_id,retry_at` | DictReader → col-count agnostic |
| wiki-pass2 CSV 20-col (core/secondary) | `bucket,tier,…` | unit=bucket; model=opus |
| Stage-4 `timing.jsonl` (sonnet mission) | near-target already | `cache_creation`/`elapsed_s` (no `_tokens`/`duration_s`) |
| `run-summary.json` (haiku mission) | `chunk_timings[]` | 1 row per chunk; tokens null |
| `rate-limit-events.jsonl` | wall events | NOT work-rows — counted for the M3 note only |

**Normalization rules that mattered:** filter to `status ∈ {ok,done}` with non-empty timing (drops 1990
`failed-stale`/no-timing rows); dedup `(track,unit)` keeping larger `elapsed_s` — this is the exact
`acok-davos-02` dup-row race (6s placeholder vs 247s real) the per-worker-JSONL design retires.

## Verification (orchestrator did this directly, not just trusting the subagent)

- `pytest` → **1231 pass / 3 documented pre-existing fails** (vocab 166≠163 ×2; cwd-is-tmp). Was 1191.
- `pace.py report` → baseline table correct; `acok-davos-02` kept the 247s row (dedup works).
- Grepped `worker-template.py` to confirm **M1** (`"rateLimitType"` + `exit(2)` + next-eligible) and
  **M2** (`os.replace`, `O_EXCL`) are actually implemented, not just claimed.

## Drift discussion + the anti-drift convention (Matt's concern)

Matt flagged the recurring risk: design docs, the scripts they describe, and actual state drift apart.
The session had just created a small instance (the doc still said "Status: DESIGN — before build").

Resolution — a three-layer mechanism, implemented now:
1. **Design-doc §0 Implementation Status table** — one row per component: BUILT/DEFERRED/NOT-STARTED/**DRIFT**
   + implementing file + proving test. Makes drift visible in the doc itself. Added; Status header flipped
   DESIGN → PARTIALLY BUILT.
2. **`scripts/README.md` = existence-truth** (design §11.3 already mandates a row per script). Doc =
   intent, README = reality; they must agree. Reconciled in Session 2's README refresh.
3. **Fable doc-truth audit** (the S92 pattern) makes doc↔code↔pytest parity an explicit checklist item.

Plus an **anti-drift gate at definition-of-done** added to the continue prompt, and a new memory
`feedback_design_doc_implementation_status`. Honest limit: the §0 table is a convention, not code-enforced;
the only mechanical check is the narrower `weirwood refresh --check` (§11.6). Fable audit = periodic backstop.

## Data quirk noted (not a defect)

`extraction-stats-agot-pass1-v3.csv` holds a few stray ACOK rows (same multi-terminal append race), so
backfill tags them `track=pass1-agot`. `unit` is self-describing; chapter-duration baselines unaffected.
Captured in design §0 + the Session-2 prompt as a CSV-archival decision (archive frozen CSVs vs leave as
backfill source — Pass 1 is 344/344, nothing appends anymore).

## What's next

- **Session 2** (cleanup/CLI/README) — same continue prompt, steps 5–8. Sonnet 4.6. Archive 24 one-offs +
  resolve 2 blocked; legacy-wrapper disposition (do NOT archive edge-reify); `weirwood graph/resolve/refresh`
  aliasing; README class/provenance refresh; the anti-drift gate reconciliation.
- Queued elsewhere: historical-anchor #9 wave 2; narrative-arc wave-1 mint (gated on Matt's 3 decisions).
