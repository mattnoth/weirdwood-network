---
session: 33
date: 2026-05-04
title: ACOK chain-launch terminal explosion + race-condition bug discovery
model: claude-sonnet-4-6 (orchestrator) / claude-opus-4-6 (extractions, killed)
type: incident / bug discovery
---

# Session 33 — ACOK auto-advance chain bug

## Context entering

Session 32 prepared a hands-off ACOK re-extraction plan: `weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain` would run 50 archived v2 chapters under v3 over ~10 wall-clock hours, with 2h delays between batches to spread token usage across API windows. Continue prompt at `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md`.

Matt launched the run from iTerm before this session started.

## What actually happened

**~16:32 UTC** — User launched the chain. 2 iTerm tabs opened: Terminal 1 ran wave 1 (acok-arya-01..05), Terminal 2 ran wave 2 (acok-arya-06..10). Both completed cleanly by ~16:55. Both then entered `sleep 7200` waiting for 2h before launching the next batch.

**~18:55** — Sleep timers fired in both tabs. Each terminal ran `./scripts/extract.sh launch acok -t 2 -w 1 -m claude-opus-4-6 --delay '2h' --chain` to start the next batch. Both terminals each opened **2 new iTerm tabs**, for a total of **4 tabs** active. Each of those 4 tabs read the incomplete-waves list independently — and because they all ran `extract.sh launch` at nearly the same moment, two of the tabs picked wave 3 and the other two picked wave 4.

**Result:** Wave 3 was extracted twice in parallel (19:00–19:16 vs 19:02–19:16); wave 4 was extracted twice in parallel (19:00–19:18 vs 18:56–19:25). When two parallel extractions write to the same `acok-bran-02.extraction.md`, the later-finishing one overwrites the earlier. The early one's tokens, time, and money are gone — no backup file exists.

**Matt's session reset before the runaway was understood**, so when this session started, my context was empty. Matt told me terminals were sleeping and asked if we could wake them. I incorrectly suggested `pkill -f "sleep 7200"` to advance them.

## Why my pkill made it worse

Each tab's command line looked like:

```
./scripts/extract.sh run acok --wave N ; sleep 7200 ; ./scripts/extract.sh launch ...
```

`;` is "run next regardless of exit." When `pkill` killed an in-flight `extract.sh run` or a `sleep 7200`, the shell didn't stop — it advanced to the next `;` step. So each kill:

- Killing `sleep 7200` → triggered the `extract.sh launch` step, opening **more** new tabs.
- Killing `extract.sh run` → triggered the `echo`s + `sleep 7200` next, then a new `launch`.

Every kill advanced the runaway. By the time Matt manually closed iTerm, we had 5 simultaneous extractions running in parallel against waves 5 and 6 (2 tabs racing on wave 5, 3 tabs racing on wave 6). Burned multiple in-flight Claude calls.

## Root causes (two distinct bugs in `scripts/extract.sh`)

### Bug A — Terminal explosion via `--chain`

`scripts/extract.sh:695`. The chain clause appended to *every* spawned terminal is:

```bash
sleep $(parse_duration_to_seconds "$delay")
./scripts/extract.sh launch ${book} -t ${terminals} -w ${waves_per} -m ${model} --delay '${delay}' --chain
```

Every terminal independently re-launches `-t 2`. With 2 starting terminals, after each delay you get `T_n+1 = T_n × 2`. Round 1: 2. Round 2: 4. Round 3: 8.

### Bug B — Race condition on `is_complete()` check

`scripts/extract.sh:117-127`. `is_complete()` checks file-existence + line-count + section-headers. Two parallel terminals can both run the check before *either* has written output, both decide "missing," and both start extracting the same chapter. Last-finishing terminal overwrites the first. No lock, no claim file, no atomic test-and-set.

Even without Bug A, Bug B can fire any time two `extract.sh` runs are pointed at overlapping wave lists.

## Files actually overwritten this session

From mtime + log-timestamp cross-check:

| Chapter | First-run finish | Mtime | Verdict |
|---|---|---|---|
| acok-bran-02 | ~19:05 | 19:10 | overwritten by 2nd terminal |
| acok-bran-04 | ~19:13 | 19:16 | overwritten |
| acok-bran-06 | ~19:00 | 19:05 | overwritten |
| acok-catelyn-01 | ~19:14 | 19:14 | likely overwritten (border) |
| acok-catelyn-03 | ~19:18 | 19:25 | overwritten |

All overwrites are valid v3 extractions (both versions were); we just paid twice. Estimated token waste ~$19 across the duplicated waves visible in `working/progress.md` (lines 36–39):

- Wave 3 at 19:16: $4.99 + $5.79
- Wave 4 at 19:18 / 19:25: $5.45 + $6.69
- Wave 1 at 16:55 ($6.96 — abnormally high; possibly the chain-start collision)

Plus uncounted in-flight calls killed by pkill.

## Where ACOK Pass 1 stands

Looking at canonical `extractions/mechanical/acok/`:

- Waves 1–4 v3 files exist and are complete (re-extracted this session, even if some twice).
- Waves 5–10 NOT re-extracted (still v2 in archive).
- Waves 11–14 (theon-02 through tyrion-15) were already v3 from Session 30.

Net: ACOK has 40 v3 chapters and 30 v2 chapters as of session end. Re-run still needed for the 30 v2 chapters in `extractions/archives/acok-v2-original-2026-05-04/`.

**DO NOT re-launch with the current `--chain` implementation.** It will repeat exactly this incident.

## Decision: model-fit guidance going forward

Matt called this out explicitly: he was naive starting the project assuming Opus everywhere was fine, and he wants to be smart about model choice now. The standing rule going forward (added to feedback memory):

**Default to the cheapest model that can do the job. Opus only when reasoning depth genuinely requires it.**

Concrete applications:
- **Mechanical extraction (Pass 1):** Opus has been the default for AGOT/AFFC for v3-consistency reasons. Open question: would Sonnet 4.6 produce equivalent v3 schema output? Worth a smoke-test before committing Opus to ASOS (82 ch) and ADWD (73 ch). Filed as TODO.
- **Bash/Python script edits:** Sonnet or Haiku. Almost never Opus.
- **Schema audits and full-corpus reviews:** Opus is justified (see Session 29's $50 audit).
- **Orchestration / coordination:** Sonnet is plenty.
- **Wiki Pass 2 stages:** Mostly Python now (no agent), so model choice only applies to occasional review prompts. Sonnet default.

## Continue prompt(s) created

One urgent prompt: `progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md`. Single track because the two bugs share a fix surface (`scripts/extract.sh`) and must both be addressed before any re-launch. Model: Sonnet 4.6 (script editing).

The prior continue prompt `2026-05-04-acok-waves1-10-rerun.md` is now stale — the launch command in it is dangerous. Updated it to point at the urgent prompt as a prerequisite.

## What did NOT happen

- No commits this session.
- No new schema decisions.
- No agent improvements.
- No graph changes.
- ACOK extraction NOT advanced beyond what waves 1–4 happened to land before the chaos.

## Lessons captured

1. **Don't use `;`-chained shell commands for unattended orchestration.** Anything that spawns child processes via `;` is one error away from cascading. A wrapper script with traps + explicit exit codes is safer.
2. **`pkill` is the wrong tool for stopping `;`-chained sequences.** Killing a process in a sequence advances the chain. The correct kill target is the parent shell (the iTerm tab's `-zsh`).
3. **Per-chapter atomic claim file is non-negotiable for parallel extraction.** Even without Bug A, ANY parallel-terminal pattern is a race waiting to fire.
4. **One-tab-spawns-many is a footgun pattern.** If chain-on-finish is desired, only ONE coordinator should re-launch — never every terminal.

## Handoff

URGENT continue prompt: `progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md`. Fix both bugs before any re-launch. Sonnet 4.6 is sufficient.

---

## Post-endsession redesign (2026-05-04, same session)

After the initial endsession run, Matt and I iterated on the urgent prompt to widen its scope and lock in design decisions. The continue prompt now covers six work items, not two:

1. **Drop `--chain`/`--delay` entirely** — no per-terminal re-launch, no auto-advance. Manual re-launch only. Single-coordinator design left for a hypothetical v2.
2. **Per-chapter status enum in the stats CSV** — replaces the simple `mkdir`-lock approach with a stronger primitive. Statuses: `not_started`, `started`, `working`, `done`, `failed-rate`, `failed-error`, `failed-stale`, `skipped-done`, `skipped-claimed`. Adds `last_heartbeat`, `terminal_id`, `retry_at` columns. Atomic claim via `flock` on the CSV. Heartbeat updater (~30s interval) spawned in background during `claude -p`.
3. **Stale-claim sweep** — at start of every `cmd_run`. Primary signal: heartbeat older than 90s (= three missed beats). Fallback signal: row written >30 min ago with no heartbeat (catches pre-heartbeat deaths). Stale rows promoted to `failed-stale`, become re-claimable.
4. **Live status table** — `weirwood <book>` shows per-chapter live dashboard ONLY when at least one row has status `started` or `working`. Otherwise prints existing static wave summary. Live rows show terminal_id + heartbeat age + (for `failed-rate`) retry-after timestamp.
5. **Terminal log cleanup** — drop dollar amounts entirely from per-chapter line, wave summary, status command, progress.md log line (CSV column kept for future). Delete the broken `0\n0 events | 0\n0 relationships` block (extract.sh:497-506) — replace with single `📋 N lines`. Restructure each chapter's output into `[1/3] Preparing` / `[2/3] Extracting` / `[3/3] Complete` phases with `═` banners for waves.
6. **Stream Claude's output during extraction** — pipe `claude -p`'s `stream-json` through a small `scripts/stream-claude-output.py` (via `tee`, to stderr, with `│ ` prefix). Full text + tool_use, no quiet mode. Doesn't enter orchestrator context — purely visual.

Plus a one-time auto-migration of existing `extraction-stats-{book}-pass1-v3.csv` files (AGOT, AFFC, ACOK partial) to the new schema, with `.bak` backup.

**Open questions resolved during the iteration:**

- Sweep age — heartbeat-driven (90s) primary + wall-clock (30 min) fallback.
- Live status table trigger — only when started/working rows exist.
- Sonnet smoke-test for Pass 1 — explicitly EXCLUDED from this scope. Matt wants at least one full Opus pass on every book before considering Sonnet for Pass 1; his friend is currently running ASOS on Opus from a shared Max account. Revisit once one book remains.
- Streaming verbosity — full text, no flag.
- Schema migration — auto, with `.bak`, on first launch after patch.
- `failed-rate` retry timing — store `resetsAt` in CSV row, render in status table.

The prompt is now self-contained at the level a Sonnet 4.6 agent should be able to execute end-to-end without bouncing back for clarifications.
