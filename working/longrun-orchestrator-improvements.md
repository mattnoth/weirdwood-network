# Longrun Orchestrator Improvements — Handoff

**Status:** Design + prototype done (S132). Deferred implementation to avoid blocking D&E smoke-test. **High priority for reuse across projects.**

---

## What works now

The `longrun.sh` + `weirwood run` harness is solid for **individual Claude Code sessions**:
- Exit codes: `0`=done, `2`=wall, `10`=more-remains, other=crash
- Crash retry: 5 attempts × 300s (5 min) sleeps
- Wall sleep: 3600s (1 hour default) — `project_stage4_sleep_defaults`
- Resume via manifest (`done[]` + lock files)
- Logging: supervisor + per-unit streams

Proven on: Stage 4 edge-classify bulk work (unattended overnight), now scaffolded for D&E Pass 1.

---

## What breaks: The 5-hour session timeout

**Problem:** Claude Code sessions die after 5 hours. If a worker is deep in a long run and hits a rate limit wall near hour 4:00–4:30, the supervisor sleeps for 1 hour and tries to relaunch at hour 5:00+. Session is dead; process never recovers gracefully.

**Symptom:** A successful, resumable crash happens at 4:55 elapsed. Supervisor exits(2), sleeps 3600s, *tries* to relaunch at 5:55. Session timeout fires before the relaunch. The manifest says "incomplete" but there's no recovery path within the same session.

**Example timeline:**
```
4:00  — unit 3 starts (20-35 min expected)
4:35  — unit 3 hits rate limit wall → exit(2)
4:35  — supervisor sleeps 3600s
5:35  — supervisor tries relaunch
5:00  — SESSION TIMEOUT (process dead)
       manifest is clean + resumable, but the session is gone
```

---

## The fix: Session chaining

**Approach:** The orchestrator (not `longrun.sh`) detects when a session is approaching timeout and **spawns a fresh Claude Code session** to continue the work.

**What it looks like:**

1. **Supervisor detects time pressure:** When elapsed > 4:30 (leaving 30-min safety margin), set a flag `APPROACHING_TIMEOUT`.
2. **On next relaunch after crash/wall:** Instead of relaunching in the same session, spawn a fresh `claude -p` subprocess that:
   - Reads the manifest (`done[]` + lock files)
   - Resumes the queue from where it left off
   - Runs with the same `--prompt-version` and config
3. **Watcher prompt:** A separate Claude Code session watches `working/logs/longrun/<track>-latest.log` and alerts if:
   - Process dies without graceful exit
   - >5 consecutive crashes (worker likely broken)
   - Manifest corrupted (recovery impossible)

**Scope:** This is infrastructure work, not D&E-specific. The payoff is **reuse across projects** (any long batch job can use the chain).

---

## Where to implement

- **`scripts/longrun.sh`:** Add `APPROACHING_TIMEOUT` logic (detect elapsed time via manifest + timestamps). On the relaunch boundary, decide: same-session retry vs spawn-fresh-session.
- **`scripts/weirwood-run.sh`:** Track elapsed time per invocation. Log it clearly.
- **New: `scripts/longrun-watcher.py` or a watcher prompt:** Monitor the log for breakage; alert if unrecoverable.
- **Design doc:** `working/longrun-session-chaining-design.md` — spell out the state machine (what survives a session boundary, what doesn't, manifest versioning, etc.).

---

## Why defer to the next session

- D&E is **only 3 units** (or 18–27 if split). Even with a wall hit, the whole run takes <2 hours. Session timeout is a non-issue in practice.
- The smoke-test + prompt-tuning is the immediate blocker; orchestrator improvements don't change that path.
- The work is **upstream** (affects how we run ANY long batch job), so it deserves a focused session with no time pressure.

---

## Next steps

**Session N+1:**
1. Write `working/longrun-session-chaining-design.md` — the state machine (1–2 hour design + prototype)
2. Update `longrun.sh` with time-pressure detection + fresh-session spawn logic (1–2 hour implementation)
3. Prototype on a **test track** (e.g., a cheap Haiku bulk that's guaranteed to hit walls) — verify the chain works
4. Document in `scripts/README.md` (Class A worker harness)

**Once proven:**
- Use it for D&E and all future batch work
- Reuse in other projects without modification

---

## Related memories / docs

- `project_stage4_sleep_defaults` — current sleep values (wall 3600s, between 1200s)
- `working/agent-fleet-specs/mission-protocol.md` — the daemon/mission distinction (related but separate)
- `scripts/longrun.sh` — current implementation (no time-pressure logic yet)
- `scripts/weirwood-run.sh` — registry + tracking (will need elapsed-time updates)
