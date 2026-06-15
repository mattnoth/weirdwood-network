# Continue — Script Consolidation + Orchestration/Pacer Build (one dedicated session)

> **Recommended model:** Sonnet 4.6 for the mechanical work (git mv, README, shell/python plumbing);
> Opus only if a coupled-script judgment call comes up.
> **Trust worklog.md over this prompt** (CLAUDE.md rule #9). Do NOT auto-`/endsession`.
> **READ FIRST — the design spec this session executes:** `working/orchestration-pacer-design-2026-06-15.md`
> (Matt-reviewed design doc: supervisor/worker/pacer/front-door architecture, exit-code contract,
> telemetry ledger, concurrency model, CLI surface, migration plan, + §11 open questions).

## SCOPE — this is TWO sessions, not one (fresh review + backfill reality, design §14)

Do **Session 1 (orchestration/pacer) FIRST** — it has the real correctness stakes — then Session 2 (cleanup)
as the mechanical follow-up. Cramming both risks a rushed, half-tested pacer.
**Before building, read design §12 (decisions), §13 (BINDING spec amendments M1–M4 / S5–S9), §14 (scope).**
The M1–M4 amendments (positive wall-detect or exit-crash; atomic state writes; honest backfill; shared
`next-eligible` for concurrency) must be written into the worker contract from the start.

### SESSION 1 — Orchestration/pacer build (design §2–§9, as amended by §13)
1. **`longrun.sh` supervisor — DONE + TESTED already** (`tests/test_longrun_supervisor.py`, 6 tests pass:
   exit-10→sleep+resume, exit-2→wall, exit-0→done, crash→give-up, streak-reset, MAX_ITER). Don't rebuild.
2. **Build `scripts/pace.py`** (the Python brain) per design §6: ingest a JSONL telemetry ledger →
   per-`(track,model)` baselines (median unit duration, tokens/unit, $/unit, wall cadence) → report
   recommended `LONGRUN_SLEEP_BETWEEN` + ETA + headroom + $ projection. Resolve §11 open questions with
   Matt FIRST (ledger location; advisory-vs-automatic; sequential-default-vs-auto-burst; v1 scope).
3. **Telemetry ledger** (design §5): define the JSONL row schema; **backfill** from existing data
   (`working/extraction-stats/*.csv`, `working/missions/*/timing.jsonl`, `*/run-summary.json`). Per-worker
   JSONL keyed by `worker_id` — NEVER a shared CSV (that caused the dup-row race: `acok-davos-02` twice in
   `extraction-stats-agot-pass1-v3.csv`).
4. **Worker contract + recipe** (design §4, §9): write a tiny reference worker / template so a future agent
   can stamp out a task-specific resumable worker (`--resume`, one bounded chunk, emits 0/2/10, one
   telemetry row/unit) and launch it via `weirwood run start custom -- python3 scripts/<task>.py --resume`.

### SESSION 2 — Script cleanup / aliasing / README (design §10 + §11 + Matt's "all aliased")
5. **Archive the 24 verified-safe one-offs** → `scripts/archive/`. The grep-guard is DONE (see below) —
   24 CLEAN, 2 BLOCKED. Use `git mv` (one per file; history preserved). The 2 blocked:
   - `stage4-haiku-smoke-prep.py` — only ref is sibling `stage4-haiku-smoke-cleanup.py` (also archiving) →
     **false block, move both together.**
   - `migrate-stats-csv.py` — referenced by LIVE `scripts/extract.sh:374` (`python3 scripts/migrate-stats-csv.py ... || true`).
     Decide: de-reference in extract.sh (the migration is one-time-complete per README) then archive, OR keep in place. Matt's call.
   - **WARNING — the Bash tool runs zsh, which does NOT word-split unquoted `$var`.** Loop with `while IFS= read -r f; do … done < list.txt` under `bash -c`, or `${(f)...}` in zsh. (A naive `for f in $CANDS` iterates once on the whole string — it silently no-ops and falsely reports "all clean".)
6. **6 legacy wrappers** (design §10.2): fold their good ideas (rate-limit detect, sleep defaults) into
   `pace.py`; archive the wrappers (tracks shelved/shipped); `stage4-run-forever.sh` = proven reference
   (`project_stage4_run_forever_wrapper`). Update the `weirwood-run.sh` registry notes after.
7. **`weirwood` CLI — "everything aliased going forward"** (design §8 + the §1.5 class taxonomy):
   long jobs (class A) always via `weirwood run start custom -- python3 …`; add `weirwood <tool>`
   subcommands for repeated standing tools (class C, e.g. `weirwood graph` → `graph-query.py`); add a
   **`weirwood refresh`** that re-runs all class-C/D derived-artifact builders (indexes + alias resolver)
   as the standard post-node-mutation step. Document **how to run a script + how to pass an arbitrary
   python script** in `weirwood --help` and the README so it's obvious.
8. **Refresh `scripts/README.md`** (design §10.3): add a **class column (A/B/C/D per design §1.5)** +
   per-script purpose + **session-provenance column** + invocation line. Add this session's new scripts:
   `historical-anchor-{candidates,validate,mint}.py` (B/C), `pace.py` (A-pacer),
   `tests/test_longrun_supervisor.py`. KEEP the 27 comention scripts (S73 — do NOT archive). NOTE the
   resolver/library scripts (class D: `event_alias_resolver.py`, `stage4_name_resolver.py`) are LIVE
   infrastructure — never archive them.

## The grep-guard result (already computed this session — reuse, don't redo)
24 CLEAN (safe to `git mv` to `scripts/archive/`): classify-prose-edges-haiku.py, classify-prose-edges-house-mormont.py,
classify-prose-edges-randyll-tarly.py, classify-ramsay-snow.py, classify-wyman-manderly.py, events-drift-audit.py,
stage4-classify-manderly.py, stage4-classify-prose-edges-haiku.py, stage4-classify-prose-edges.py,
stage4-comention-classifier.py, stage4-complete-classifier.py, stage4-haiku-classify-batch.py,
stage4-haiku-classify-comention.py, stage4-haiku-classify-karstark.py, stage4-haiku-classify-prose-edges.py,
stage4-haiku-classify-test.py, stage4-haiku-classify-v2.py, stage4-haiku-classify.py, stage4-haiku-proper-classify.py,
stage4-haiku-smoke-cleanup.py, stage4-haiku-smoke-finish.sh, stage4-prose-edge-classifier.py, stage4-real-classifier.py,
temp-classify-glovers.py.
2 BLOCKED (handle per step 5): stage4-haiku-smoke-prep.py (false block), migrate-stats-csv.py (real — extract.sh).

## Hard rules
- `sources/` immutable; `graph/` NOT touched (hygiene only); `history/` contents never edited.
- Every move: `git mv` + grep-guard vs LIVING files first (records like worklog/session-details/audits don't block).
- ~24 scripts cross-reference each other — move conservatively; `python3 -m pytest -q` after each batch
  (expect 3 documented pre-existing fails: vocab-count 166≠163 ×2, cwd-is-tmp — now +6 longrun tests passing).
- Don't touch a wrapper while its track has a live run.

## Definition of done
`scripts/` organized (central scripts obvious, one-offs archived/CLI-folded); ALL long-runs go through ONE
proven path (`longrun.sh` via `weirwood run`); `pace.py` reports baselines + recommended sleep from
backfilled stats; README current with purpose + session-provenance + invocation; tests green (minus the 3
documented fails). Downstream after this: narrative-arc wave-1 mint (still gated on Matt's 3 decisions);
historical-anchor #9 wave 2.
