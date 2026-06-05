# Worklog Archive 017

> Archived Session Log entries (oldest-first within this file). Each archive holds 5 entries.
> Sessions: 78 (1/5 — start).

---

### Session 78 — Events Haiku bulk: monitor checkpoints (healthy) + continue-prompt refresh (2026-05-28)

**Model:** Opus 4.7 (orchestrator; read + light doc-writes). **Detail:** none (pure monitoring/admin session). **Commit:** this endsession commit.

**Changes made (no code, no graph — doc writes + worklog + hygiene):**
- NEW `working/session-results/2026-05-27-events-haiku-bulk-monitor-log.md` — durable checkpoint log (precision + reject-recall baseline for the completion read).
- REFRESHED `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` — current state baked in; **relaxed the read-only framing per Matt ("it can write if it needs to"; only `edges.jsonl` is gated)**; added a "why ~90% reject is healthy" section + a **REQUIRED reject-recall (false-reject) step** in the completion validation (Matt's call — expect unique-edge recall loss <~15%).
- Worklog Current State Events line → LAUNCHED + MONITORED HEALTHY.
- HYGIENE: `.claude/scheduled_tasks.lock` (stale per-process lock accidentally committed S76, dead pid) untracked + added to `.gitignore`.

**Monitoring (read-only on the in-flight run — never touched it):**
- Run alive (PIDs 65068/65078), 600s pacing. Matt relaunched the temp-1800s start at 600s himself → the worklog "lower sleep before travel" action item is already done.
- First-flush human precision read (58 edges): **~93–96% strict**; 2 clear + 2 borderline errors, all candidate-slug / over-eager-moment class (`bran TEACHES joseth-maester`, `robb FEARS sansa`, `jaime RESCUES bran`, `bran LOCATED_AT winterfell`), NOT vocab drift. Schema clean (`typed_by=haiku`, 0 ASSAULTS).
- Automated validate@25/50/75 all OK (reject_rate ~0.90, unresolved=0; no walls, no drift).
- **Reject-recall check (Matt flagged "most rows getting rejected"):** ~90% reject is by-design (high-recall candidates × precision filter, inflated by the same real pair recurring across event rows). 25 random rejects → **~0 clear missed edges, ~4 borderline** (each already captured from a cleaner row or a group/bad slug) → **unique-edge recall loss <~15%**, acceptable per the Haiku trade.

**Decisions:** (1) **Pacing is NOT a cost lever** — 600s spreads the SAME ~$50 token spend over ~3 days; it's a weekly-usage-rate lever (splits spend across weeks). Total Haiku run ~$50 vs Sonnet's ~$270 for the same rows. (2) Next session **MAY write** (Matt) — only `edges.jsonl` modification stays gated on before/after sign-off. (3) **Reject-recall is now a required validation dimension** (not just emit-precision) — the high reject rate is healthy, but completion must quantify false-rejects, not assume.

**What's next:** Run self-driving (~2.7 days; exit-43 drift halt guards it). → `progress/continue-prompts/2026-05-27-events-haiku-bulk-monitor.md` (**Opus 4.7**): owed = completion read + slug long-tail triage + MERGE into `edges.jsonl` (gated). Still gated on Matt: 3 core-cleanups (drop 2 `cersei↔tyrion` LOVES / ~22 `ASSAULTS`→`ATTACKS` / merge-time `OWNS→BONDED_TO`).
