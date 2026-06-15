# Orchestration & Pacing — Design Doc (2026-06-15)

> **Status:** BUILT — Session 1 (orchestration/pacer) shipped 2026-06-15 (S98); Session 2
> (cleanup/CLI/README) shipped 2026-06-15 (S99). See **§0 Implementation Status** below for the per-component truth.
> Companion to `scripts/README.md` (the per-script inventory) and
> `progress/continue-prompts/2026-06-15-script-consolidation.md` (the execution session).
> **Origin:** Matt wants one durable, aliased way to run any long, rate-limited, multi-window job, with
> timing/headroom prediction from past run stats — replacing the 6 divergent run-forever wrappers.

---

## 0. Implementation Status (keep in sync with reality — update the row when a component ships)

> **Anti-drift rule:** this table is the seam between this design doc and the actual scripts. When a
> component is built, flip its row to BUILT + name the implementing file + the test that proves it. When the
> design changes but the code hasn't caught up (or vice-versa), the row says DRIFT and names the gap. A
> doc-truth audit (the Fable pass) checks this table against `scripts/` + `scripts/README.md` and against
> `pytest`. If a row claims BUILT and the file/test is gone, that's the drift to fix.

| Component | Design § | Status | Implementing file | Verified by |
|---|---|---|---|---|
| Supervisor (`longrun.sh`) | §2–§3 | **BUILT** (pre-S98) | `scripts/longrun.sh` | `tests/test_longrun_supervisor.py` (6) |
| Telemetry ledger schema + backfill normalizer | §5 | **BUILT** S98 | `scripts/pace.py` (`backfill`) → `working/telemetry/<track>.jsonl` | `tests/test_pace.py` (40); backfill 476 work rows + 8 wall events / 9 tracks, dup-race deduped |
| Pacer report (v1 = report-only) | §6, §12 | **BUILT** S98 | `scripts/pace.py` (`report`) | `tests/test_pace.py`; prints baselines + conservative sleep + M3 wall note |
| `emit_telemetry_row` helper | §4.4, §6 | **BUILT** S98 | `scripts/pace.py` | imported by `worker-template.py` |
| Worker contract template (M1/M2/M4) | §4, §13 | **BUILT** S98 | `scripts/worker-template.py` | atomic `os.replace` + `O_EXCL` claim + positive-wall `exit(2)` + `next-eligible` verified in-code; demo 10→10→0 + resume |
| Pacer ETA / headroom / concurrency-rec | §6, §7 | **DEFERRED to v2** | — | gated on live wall-cadence rows (M3) |
| Multi-worker burst (shared next-eligible) | §7, §13 M4 | **DEFERRED to v2** | — | v1 ships single-worker-durable; template writes the file |
| Archive 24 one-offs + 2 blocked | §10.1, §13 S7 | **BUILT** S99 | 30 files `git mv`→`scripts/archive/` (24 + smoke-prep sibling + `migrate-stats-csv.py` + 4 wrappers) | grep-guard clean vs living files; README existence-truth cross-check (all live+archived present); pytest 1231 |
| Legacy-wrapper disposition | §10.2, §13 S7 | **BUILT** S99 | 4 shelved wrappers archived; `stage4-run-forever.sh` + `edge-reify-run-forever.sh` KEPT; `weirwood-run.sh` registry paths → `scripts/archive/` | `weirwood run list` renders; `bash -n` clean |
| `weirwood graph/resolve/refresh` aliasing | §8, §11.4, §11.6 | **BUILT** S99 | `scripts/weirwood-refresh.sh` (rebuild + `--check`) + 3 cases in `scripts/weirwood.zsh` | `weirwood refresh --check` = OK; `graph-query.py --health` + `event_alias_resolver.py --stats` pass-throughs run |
| `scripts/README.md` class/provenance refresh | §10.3, §11.3 | **BUILT** S99 | `scripts/README.md` (Class A/B/C/D column + `Added` provenance + invocation + §11.5 checklist preamble) | existence-truth cross-check: 124 live + 32 archived scripts all have a row |

**Known data quirk surfaced at build (S98):** the legacy `working/extraction-stats/*.csv` are messy —
`extraction-stats-agot-pass1-v3.csv` even contains some ACOK rows (the same multi-terminal CSV-append race
that dup'd `acok-davos-02`), so the backfill tags them `track=pass1-agot`. The `unit` field is
self-describing and chapter-duration baselines are unaffected; **this is exactly the mess the per-worker
JSONL ledger retires going forward.** Not worth backfilling around. **Session-2 decision RESOLVED (S99, Matt):**
the frozen CSVs were `git mv`'d to `working/extraction-stats/_archive/` (Pass 1 = 344/344; nothing appends
anymore). `pace.py backfill`, `extract.sh status`, and `weirwood wiki status` all fall back to `_archive/`.

---

## 1. The problem

Long jobs (mechanical Pass-1 extraction, Haiku batch typing, wiki passes, future ad-hoc tasks like
"process chapters X–Y") have to survive: rate-limit walls, 5-hour session windows, crashes, and
multi-hour/overnight unattended runs. Today six wrappers (`stage4-run-forever.sh`,
`edge-reify-run-forever.sh`, `stage4-haiku-run-forever.sh`, `stage4-tail-bulk-forever.sh`,
`stage4-haiku-loop.sh`, `stage4-events-bulk-run.sh` — ~1,200 lines) each re-implement sleep,
rate-limit detection, crash-retry, and resume **differently** (different env var names, defaults
1200/1800/3600/600s, exit-code conventions). The sleep intervals are hard-coded guesses, not derived
from how runs actually behaved.

## 1.5 Where each KIND of script fits — the orchestration covers only ONE class

The supervisor/worker/pacer machinery below governs **only long-run, rate-limited, LLM-driven jobs**.
Most scripts in `scripts/` are not that. Four classes, by how they're run and their lifecycle:

| Class | Examples | How it runs | Aliased as | Lifecycle |
|---|---|---|---|---|
| **A. Long-run jobs** (rate-limited, multi-window, LLM-driven) | mechanical Pass-1 extraction, Haiku batch typing, wiki Pass-2 | `weirwood run` → `longrun.sh` → worker → `pace.py` | `weirwood run start <track>` / `custom` | the orchestration in §3–§9 |
| **B. One-shot mutations** (deterministic, fast, mutate graph/data once) | `historical-anchor-mint.py`, `plate5-merge.py`, `infobox-merge.py`, edge refiners | direct — **never** longrun-wrapped (no walls to survive) | usually direct; a `weirwood <verb>` only if re-run | backup → dry-run → apply → validate; **archive to `scripts/archive/` when spent** |
| **C. Standing tools** (on-demand; read-only or build-an-artifact) | `graph-query.py`, `build-entity-indexes.py`, validators, `historical-anchor-{candidates,validate}.py` | on demand | `weirwood <tool>` (e.g. `weirwood graph`) | LIVE forever; never archived |
| **D. Resolvers / libraries** (build a derived artifact + queried/imported) | `event_alias_resolver.py`, `stage4_name_resolver.py` | `--build` regenerates the artifact; `--lookup`/import queries it | `weirwood refresh` (rebuild all derived artifacts) | LIVE forever; **re-run after any node-changing graph mutation**; never archived |

**Distinctions that matter:**
- **Resolvers (D) are load-bearing infrastructure, NOT one-offs.** They build the derived lookups
  (alias→slug, name→node) that consumer agents and other scripts depend on. After any mutation that
  **adds or renames nodes**, the resolver + indexes must be rebuilt so the new nodes are discoverable.
  (Edge-only mutations — like the 2026-06-15 historical-anchor mint — need no rebuild.) → propose a single
  **`weirwood refresh`** that re-runs all class-C/D builders (indexes + alias resolver) as the standard
  post-mutation step.
- **One-shot mutations (B)** are the opposite of resolvers: run once with backup+dry-run+validate, then
  **spent → archived**. They are neither supervised (A) nor standing (C/D).
- **"Everything aliased" spans all four, but differently:** A via `weirwood run`; C/D via `weirwood <tool>`
  / `weirwood refresh`; B usually direct-but-documented.
- **The README (§10.3) catalogs ALL four classes** — the class tag (A/B/C/D) becomes a column alongside
  purpose / session-provenance / invocation.

## 2. The shape: supervisor / worker / pacer / front-door

Four thin layers. Each talks to the next ONLY through a process boundary + exit code — so the
languages never need to "speak" to each other.

```
  zsh  ── weirwood CLI (front door; the alias)
   └─ bash  ── longrun.sh        SUPERVISOR  (durable outer loop; ALREADY BUILT + TESTED)
        └─ python3  ── worker.py  WORKER     (one bounded, resumable chunk; emits 0/2/10)
                          ▲
                          └─ uses pace.py    PACER  (shared telemetry ledger + prediction)
```

- **Supervisor — `longrun.sh` (bash).** Dumb + durable. Launches the worker, reads its exit code,
  sleeps or relaunches or stops. ~150 lines, no arithmetic. **Done + proven:** `tests/test_longrun_supervisor.py`
  (6 tests: exit-10→sleep+resume, exit-2→wall, exit-0→done, crash→give-up, streak-reset, MAX_ITER).
- **Worker — task-specific Python.** Does the real work; emits the contract exit code. Resumable.
- **Pacer — `pace.py` (Python, NEW).** The brain: one telemetry ledger + prediction (sleep / headroom /
  ETA / concurrency recommendation), fed by historical run stats.
- **Front door — `weirwood` CLI.** How you launch + observe everything (one aliased entry point).

**Why split languages:** the supervisor must *outlive the worker dying*. If a rate-limit wall kills the
Python process, something outside it must relaunch it — so the relaunch loop lives in a separate, tougher
process (bash). Putting the loop inside the same Python process means it dies when the worker dies. This
is the classic supervisor/worker pattern. (All-Python is possible but re-writes the proven bash loop.)

## 3. The exit-code contract (the seam between every layer)

| Code | Meaning | Supervisor reaction |
|---|---|---|
| `0`  | all work complete | stop (exit 0) |
| `2`  | rate-limit wall | sleep `LONGRUN_WALL_SLEEP` (default 1h), relaunch |
| `10` | this chunk done, more remains | sleep `LONGRUN_SLEEP_BETWEEN` (default 20m), relaunch |
| other| crash | sleep `LONGRUN_CRASH_SLEEP`, retry up to `LONGRUN_MAX_CRASHES`, else give up (exit 1) |

This is already what `longrun.sh` enforces. Any worker that obeys it is automatically durable.

## 4. The worker contract (what makes multi-window survival work)

A worker MUST:
1. **Be resumable + idempotent.** Persist progress to disk (claimed/done markers). Relaunching the
   *same argv* continues, never redoes. This is the property that lets a job span many 5-hour windows.
2. **Do one bounded chunk per invocation**, then `exit(10)`. The supervisor owns pacing; a crash loses
   ≤1 chunk; `--resume` picks up the rest.
3. **Claim units atomically** for any shared queue (the chapter-claim lock the project already uses).
   This is the fix for the duplicate-row race below.
4. **Emit one telemetry row per unit** to the ledger (§5).
5. Detect the rate-limit wall and `exit(2)` (vs a real crash) so the supervisor sleeps-until-reset
   instead of burning crash retries.

## 5. Telemetry ledger (JSONL, per-worker — the CSV-race fix)

**The race Matt remembered is real:** `working/extraction-stats/extraction-stats-agot-pass1-v3.csv` has
chapter `acok-davos-02` twice (6s and 247s) — two terminals appended for the same unit into one shared
CSV. **Fix: append-only JSONL keyed by `worker_id`.** Each line is one atomic write, self-identifying, so
concurrent workers can't corrupt or duplicate each other (the Stage-4 `timing.jsonl` already does this).

Proposed row schema (one per unit of work):
```json
{"run_id":"...","track":"pass1-affc","worker_id":"worker-<ts>-<pid>","unit":"affc-cersei-03",
 "started_at":"2026-...Z","elapsed_s":231,"input_tokens":3702,"cache_creation":533157,
 "cache_read":2907759,"output_tokens":106755,"cost_usd":4.86,"exit_reason":"ok|wall|crash",
 "rate_limited":false,"sleep_taken_s":0,"model":"claude-..."}
```
**Backfill the ledger** from existing data so prediction works on day one:
`working/extraction-stats/*.csv` (Pass-1 per-chapter), `working/missions/*/timing.jsonl` (Stage-4
per-batch, already this schema), `working/missions/*/run-summary.json` (has `concurrency`,
`rate_limit_events[]`, `chunk_timings[]`).

## 6. The pacer (`pace.py`) — how past stats predict

Ingest the ledger → per-`(track, model)` baselines:
- **median unit duration**, **tokens/unit**, **$/unit**;
- **observed wall cadence** — time between `rate_limited:true` events (how long you run before hitting the wall).

Outputs (advisory by default — see open questions):
- **recommended `LONGRUN_SLEEP_BETWEEN`** (from wall cadence, not a hard-coded guess);
- **ETA** for N remaining units (sequential vs at concurrency C);
- **headroom estimate** — how many concurrent workers before walls dominate;
- **$ projection** for the remaining queue.

**Sequential-first calibration (Matt's instinct):** for a new/unknown task, run K units sequentially to
seed the baseline, THEN let the pacer recommend whether/how much to fan out. You never guess blind.

## 7. Concurrency model (three scenarios + caveats)

1. **One task, multi-window** — 1 worker + longrun. Survives walls/sessions. *(The "process chapters
   over several 5-hour windows" case.)* ✅
2. **Burst fan-out** — N workers, ONE queue, atomic claim, per-worker JSONL telemetry; pacer recommends
   N from headroom. Use when you have burst quota. ✅
3. **Two independent tasks in parallel** — two `weirwood run` tracks, separate supervisors/pidfiles/logs;
   naturally safe (different queues). ✅

**Caveats (honest):**
- All parallel workers share **one account rate-limit pool** — concurrency only buys wall-clock with real
  headroom; past that they all wall together (and longrun sleeps them all). The pacer is what makes the
  concurrency *informed*.
- **Atomic claiming is mandatory** for a shared queue; without it you get the dup-row race.
- **Telemetry must be per-worker JSONL**, never a shared CSV.

## 8. weirwood CLI surface (how to run + how to pass any Python script)

The "everything aliased going forward" convention:
```
weirwood run start custom -- python3 scripts/<worker>.py --resume   # ANY script, longrun-wrapped
weirwood run start <track>            # a registered track (TRACK_CMD in weirwood-run.sh)
weirwood run list | logs <t> | status <t> | stop <t>
```
- **Long jobs ALWAYS go through `weirwood run`** (gets longrun supervision + log + pidfile for free).
- **One-shot tools** get a `weirwood <tool>` subcommand when run repeatedly (e.g. `weirwood graph
  --neighbors <slug>` for `graph-query.py`), else are invoked directly and **documented in
  `scripts/README.md` with their invocation line**.
- Registering a recurring job = add a `TRACK_NAMES/STATUS/DESC/CMD` entry in `weirwood-run.sh` (then
  `weirwood run start <name>`).

## 9. How an agent builds a NEW task (the recipe this enables)

Given "process chapters X–Y" (or any long job):
1. Agent writes `scripts/<task>.py` implementing the **worker contract** (§4): resumable queue, one
   bounded chunk per run, `exit 0/2/10`, one telemetry row per unit (helper from `pace.py`).
2. Launch: `weirwood run start custom -- python3 scripts/<task>.py --resume`.
3. Walk away. longrun survives walls + windows; pace.py predicts ETA/cost; `weirwood run status` shows progress.

No new wrapper. No new sleep logic. No new rate-limit handling. That all lives once, in longrun.sh + pace.py.

## 10. Migration / cleanup (folds in THIS session's work)

1. **Archive 24 verified-safe one-offs** (early Stage-4 `classify-*` / `temp-*` iteration scripts) →
   `scripts/archive/`. Guard already run (grep vs living files); 2 had real refs:
   `migrate-stats-csv.py` (called by live `extract.sh` — keep or de-reference), `stage4-haiku-smoke-prep.py`
   (only ref is sibling candidate `stage4-haiku-smoke-cleanup.py` — moves together, false block).
2. **Legacy wrappers** — extract their good ideas (rate-limit detection incl. the `next-eligible` sidecar,
   sleep defaults) into `pace.py` / the worker contract; archive ONLY the wrappers whose tracks are
   shelved/shipped. **Do NOT archive `edge-reify-run-forever.sh`** — its track is PLANNED/live in the
   `weirwood-run.sh` registry (§13 S7). `stage4-run-forever.sh` = the **proven** reference (ran reliably
   overnight per `project_stage4_run_forever_wrapper`). Recount against the registry before moving any wrapper.
3. **`scripts/README.md` refresh** — per-script purpose + **session-provenance column** + invocation line.
4. **Build `pace.py` + the ledger**; backfill from existing stats (§5).
5. **Keep the 27 comention scripts** (S73 KEEP — revival-recall lever; do NOT archive).

## 11. Script Organization Standard (the umbrella — ALL scripts, not just orchestration)

Goal: every script — today's and every one created in the future — has an obvious **name, place,
run-path, and doc entry**, so `scripts/` never sprawls back to 150 loose files. Builds on the §1.5
class taxonomy (A=long-run job, B=one-shot mutation, C=standing tool, D=resolver/library).

### 11.1 Naming
`<area>-<verb>.py` — e.g. `historical-anchor-mint`, `edge-reify-backfill`, `build-entity-indexes`. Same
area → same prefix so siblings sort together. Avoid `temp-` / `test-` / `-v2` in committed names — those
signal "should already be archived."

### 11.2 Location
- `scripts/` — live scripts (classes A, C, D, and B while in flight).
- `scripts/archive/` — spent class-B one-offs + superseded scripts. Stays in git history; out of the live dir.
- `scripts/lib/` *(optional, only if it grows)* — importable shared modules / resolvers (class D) that other scripts import.
- The 27 wiki-comention scripts stay put (S73 KEEP — revival-recall lever).

### 11.3 README row for EVERY script — no exceptions
`scripts/README.md` is the **universal index**. Columns: **class (A/B/C/D) · script · purpose ·
session-created · how-to-run**. Even a one-shot that will be archived tomorrow gets one row first, so it is
always findable. This row — not an alias — is the real "organized."

### 11.4 Alias policy (aliases are for repeat-use, not throwaways)
- **Class A** (long jobs) → `weirwood run start <track>` / `custom`.
- **Class C** (standing tools) + **D** (resolvers) → `weirwood <tool>` (e.g. `weirwood graph`,
  `weirwood resolve`, `weirwood refresh`).
- **Class B** (one-shot mutation) → run directly (`python3 scripts/<x>.py`), README row, **archive when
  spent. No alias** — you won't run it twice.

### 11.5 New-script checklist (so future scripts are BORN organized)
When ANY script is created (by Matt or an agent):
1. Name it `<area>-<verb>`.
2. Decide its class (A/B/C/D).
3. Add its README row (class · purpose · session · how-to-run).
4. Wire an alias ONLY if class A (track) or C/D (repeat-use tool).
5. If it's a class-B mutation that **adds or renames nodes**, it must call `weirwood refresh` (or the
   builders directly) as its final step — see §11.6.
Encode this as a short preamble in `scripts/README.md` (or a `scripts/CONTRIBUTING.md`) so it's self-enforcing.

### 11.6 `weirwood refresh` + forget-proofing
`weirwood refresh` runs ALL derived-artifact builders in sequence — entity indexes
(`build-entity-indexes.py`) + alias resolver (`event_alias_resolver.py --build`) + any future class-D
builder — in one command, so you never have to remember the individual steps.
Because it's easy to forget after a manual graph edit, reduce reliance on willpower (these are
reminders + one real check — see §13 S8, they are not fully "mechanical"):
- **Auto-call:** every class-B node-adding/renaming mutation script calls `weirwood refresh` (or the
  builders directly) as its last step. The mutation that creates staleness also fixes it. *(Soft — depends
  on the script author adding the call.)*
- **Real check:** `weirwood refresh --check` compares `graph/nodes/` mtime vs the resolver-artifact mtime
  and WARNS if stale; wire it into a pre-commit hook so a node change without a refresh is flagged.
- **Backstop — memory:** the `project` memory entry `rebuild-derived-artifacts-after-node-mutation` reminds
  agents doing graph work to refresh even when editing by hand.
- Edge-only mutations need no refresh (see §1.5).

## 12. Decisions (resolved 2026-06-15 after fresh review — reviewer concurred with all leans)
- **Ledger location → per-track files** `working/telemetry/<track>.jsonl` (NOT one flat file — avoids
  unbounded growth + concurrent-append contention).
- **Pacer = advisory only.** `pace.py` *prints* a recommended `LONGRUN_SLEEP_BETWEEN` / concurrency; it
  NEVER auto-sets env vars (surprising + hard to debug). User sets the recommended value explicitly.
- **Default posture = sequential-always.** Burst is opt-in via `--workers N`, with a headroom warning. An
  accidental fan-out under tight quota is worse than being slow.
- **pace.py v1 scope = report only:** ingest existing CSV/JSONL → normalize to ledger schema → print
  per-`(track, model, unit_type)` baselines (median duration, tokens, $/unit) + a conservative recommended
  sleep. **No ETA/headroom/concurrency-recommendation in v1** — the wall-cadence data to power them does
  not exist yet (§13 M3). Add once the ledger accumulates live wall events.

## 13. Spec amendments from fresh review (BINDING — fold into the worker contract before building)

> Fresh reviewer read the real `stage4.sh` wall-detection + the actual stats schemas and found 4
> specification gaps that would cause data-loss / missed-wall bugs on the first overnight run. These
> amend §3–§11.

**MUST (write into the worker/supervisor contract now):**
- **M1 — exit(2) requires a POSITIVE wall signal.** A worker emits `exit 2` ONLY when it actually detects
  the rate-limit rejection (e.g. greps the `claude -p` stream for `"status":"rejected"` + `rateLimitType`,
  as `stage4.sh:403` does). If it *can't tell* (claude died with no parseable output) it exits **crash**,
  never 2 — otherwise it silently burns a full `LONGRUN_WALL_SLEEP`. Preserve the proven belt-and-suspenders:
  on a detected wall, write the reset time to a shared `working/telemetry/<track>.next-eligible` file.
- **M2 — atomic state writes.** All worker STATE writes (progress manifest, claim markers) use
  write-to-tmp-then-`rename`. Telemetry JSONL appends are single-line atomic; multi-byte manifests are NOT —
  never in-place mutate. A SIGTERM mid-write (from `weirwood run stop`) must not corrupt progress.
- **M3 — honest backfill.** Existing data gives solid unit-**duration**/token/$ baselines day-one, but
  **wall-cadence is thin** (~4 wall events across 2 missions; Pass-1 CSVs have NO `rate_limited` column; the
  Haiku mission has no `timing.jsonl`). So v1 reports baselines + a conservative default sleep; genuine
  wall-cadence prediction waits for live rows. Do not overclaim "prediction works day-one."
- **M4 — concurrent wall storm.** For any fan-out, ALL supervisors of a track read ONE shared
  `<track>.next-eligible` timestamp (M1) and wake together at the authoritative reset — not at staggered
  per-worker guesses that re-storm the API. **v1 ships single-worker durable + writes the next-eligible
  file; multi-worker burst is gated behind M4 being implemented (effectively v2).**

**SHOULD:**
- **S5 — chunk sizing:** size a chunk to finish comfortably under `LONGRUN_SLEEP_BETWEEN` and lose ≤1 chunk
  on crash (typical units: chapter ~250s, Haiku chunk ~157s). State this in §4.
- **S6 — ledger needs `unit_type`** (chapter|batch|file|edge); pacer groups by `(track, model, unit_type)`
  so it never averages chapters against 5-file chunks.
- **S7 — reconcile the legacy-wrapper list:** the `weirwood-run.sh` registry has 3 LEGACY tracks +
  `edge-reify` as **PLANNED (live, NOT shelved)**. Do NOT archive `edge-reify-run-forever.sh`. Recount
  against the registry before moving any wrapper.
- **S8 — `weirwood refresh` enforcement is SOFT, not "mechanical."** Auto-call + memory are reminders. Add a
  real check: `weirwood refresh --check` (or a pre-commit hook) that compares `graph/nodes/` mtime vs the
  resolver-artifact mtime and WARNS if stale. (§11.6 wording softened accordingly.)
- **S9 — hang defense:** add `LONGRUN_ITER_TIMEOUT` (default 0 = off) wrapping the worker in `timeout` so a
  hung worker can't stall the supervisor forever.

**NICE:**
- **N10 — sequential calibration K=5** as the default seed count.
- **N12 — `custom` pidfile collision:** `weirwood run start custom` always writes `custom.pid`; two
  concurrent ad-hoc jobs clobber tracking. Use named tracks for parallel jobs, or namespace custom pidfiles.

## 14. Scope realism — this is TWO sessions, not one
Fresh review (and the heterogeneous-CSV backfill reality) say the honest split is:
- **Session 1 — orchestration/pacer:** `pace.py` v1 (report-only) + the worker-contract template + the
  ledger + the M1–M4 amendments. ~one session; the **backfill normalizer** (5 different input schemas:
  13-col vs 16-col CSVs, `cache_creation` vs `cache_creation_tokens`, missing `timing.jsonl`, the
  `acok-davos-02` duplicate rows) is the time-sink, not the architecture.
- **Session 2 — script cleanup:** archive the 24 one-offs + resolve the 2 blocked + legacy-wrapper
  disposition + `weirwood` CLI aliasing (`graph`/`resolve`/`refresh`) + README refresh with the class +
  session-provenance columns.
Cramming both risks a rushed, half-tested pacer. Recommend Session 1 first (it's the part with real
correctness stakes), Session 2 as the mechanical follow-up.
