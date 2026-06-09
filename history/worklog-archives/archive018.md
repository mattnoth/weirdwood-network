# Worklog Archive 018

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 83-tmp-paths (1/5).

---

### Session 83 — Move `/tmp` paths into `~/source/claude-cwd/` hierarchy (2026-06-05)

**Model:** Opus 4.7 (orchestrator + execution; no agents delegated). **Detail:** none (pure path-rename hygiene). **Commit:** this endsession commit.

**Changes made (path refactor; no behavior change):**
- NEW dirs: `~/source/claude-cwd/` (empty `cwd=` for `claude -p` subprocesses; sibling of repo, no parent `CLAUDE.md` to defeat the cost trick) + `~/source/claude-cwd/tmp/` (for stop-files + per-run logs).
- `scripts/stage4-tail-classifier.py`: `cwd="/tmp"` → `cwd=CLAUDE_P_CWD` constant; `STOP_FILE` uses `os.path.expanduser` over the new path. `scripts/events-drift-audit.py`: cosmetic — comments / `judge_cwd` metadata / APPLY log line (inherits the cwd from `TC.invoke_claude`).
- 13 active shell scripts (`extract.sh`, `weirwood.zsh`, `launch-extraction.sh`, `run-extraction-wave.sh`, `run-extraction-all.sh`, `stage4.sh`, `stage4-run-forever.sh`, `stage4-events-bulk-run.sh`, `stage4-haiku-loop.sh`, `stage4-haiku-run-forever.sh`, `stage4-haiku-smoke-finish.sh`, `stage4-tail-bulk-forever.sh`, `wiki-pass2.sh`): every `/tmp/{extraction,stage4,wiki-pass2,haiku-smoke}-*` replaced with `$HOME/source/claude-cwd/tmp/...`.
- `tests/test_stage4_bulk_run_apparatus.py`: assertion + comments; 42/42 pass.
- `reference/extraction-commands.md`, `working/runbooks/{stage4-events-haiku-bulk, mechanical-extraction-howto, wiki-pass2-orchestration, pass1-auto-advance-mode}.md`, `progress/continue-prompts/{2026-05-17-stage4-bulk-watcher, 2026-05-16-stage4-bulk-resume}.md`, `BEFORE-LEAVE-RESUME-2026-05-28.md`, worklog S79 line, memory `reference_llm_pass_via_claude_p.md`.

**Skipped (per "except archived files" rule):** `scripts/archive/`, `working/runbooks/archive/`, `progress/continue-prompts/archive/`, `working/session-results/` (frozen historical), `EDGE_INVENTORY_REPORT.md` (one-time report). Unrelated `/tmp` references untouched: `bucket_dir/tmp` (Pass-2 bucket-internal subdir, not `/tmp`); `/tmp/test/`, `/tmp/edge-inventory/`, `/tmp/parse_rels.py` example/throwaway paths.

**Decisions:** (1) Two `/tmp` use cases share the new root: `~/source/claude-cwd/` for the `claude -p` cwd cost trick (~49% cheaper by skipping the repo CLAUDE.md cold-load); `~/source/claude-cwd/tmp/` for stop-files + per-run logs. (2) Verified nothing was in flight in `/tmp` at time of change (no processes, no stop-files, no log files) — pure code rename, nothing on disk moved. (3) Shell uses `$HOME/source/claude-cwd/tmp/...` (POSIX-portable inside quoted strings); Python uses `os.path.expanduser("~/source/claude-cwd/tmp/...")`. Test assertion now uses `os.path.expanduser` so it doesn't hard-code Matt's homedir.

**What's next:** No new track from this session — the path refactor is self-contained and complete. Queued prior-session work is unaffected: → `progress/continue-prompts/2026-06-04-edge-modeling-cleanroom-execution.md` (S82, **Opus 4.7**) is the most recent live track; `progress/continue-prompts/2026-06-01-events-bulk-escalation-pick.md` (S81) partially superseded by S82's cleanroom reframe; 3 core-cleanups still gated on Matt since S77.
