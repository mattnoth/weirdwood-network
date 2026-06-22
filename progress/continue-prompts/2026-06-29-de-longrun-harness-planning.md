# SESSION 132 — D&E Pass-1 via longrun.sh: harness planning (design only, NO extraction launch)

> **Session number:** this track is **parallel-safe** with the low-value-remainders track
> (`2026-06-29-low-value-remainders.md`). They touch different files and can run in different windows.
> Stamp your worklog entry with the **next free `### Session N`** per `worklog.md` at endsession (132 if the
> remainders track ran first as 131; 131 if you run/endsession first). Don't hardcode — check the worklog.

> **Recommended model:** Opus 4.8 (architecture/design session — wiring the unattended harness; no bulk LLM run here).

## Goal
**Plan how to run the Dunk & Egg full-Opus Pass-1 batch UNATTENDED** via `longrun.sh` + the unified worker
harness (`scripts/worker-template.py`), passing in a **D&E-specific orchestrator/fleet sub-script**. Two wins
(Matt S130): (1) get D&E (THK/TSS/TMK) extracted off the critical path — it can run concurrently / in the
background while interactive enrichment happens; (2) **exercise + validate the unified-script architecture**
from the S98/S99 post-Fable-audit consolidation, which hasn't been run unattended in a while. D&E is the ideal
test payload: 3 small self-contained novellas, mechanical Pass 1.

**This is a DESIGN session. It LAUNCHES NOTHING.** Output is a concrete run-plan + the D&E sub-script scaffold.
Per `feedback_no_extraction_without_asking` (memory), the actual extraction is launched only after Matt's
explicit go-ahead — and only after the prompt-improvement prereq (below) lands.

## Read first
- `scripts/README.md` — the universal script index (Class A/B/C/D), to locate the harness pieces.
- `scripts/worker-template.py` (unified worker, M1/M2/M4 modes) + `longrun.sh` (supervisor, S97) +
  `scripts/stage4-run-forever.sh` (the rate-limit-wall auto-resume wrapper; memory
  `project_stage4_run_forever_wrapper`, sleep config `project_stage4_sleep_defaults`).
- `working/agent-fleet-specs/` (fleet-orchestration / runtime-architecture plans) + the mission protocol
  draft (`working/agent-fleet-specs/mission-protocol.md`, memory `project_mission_protocol_v0`).
- How LLM passes run: memory `reference_llm_pass_via_claude_p` (`claude -p` subprocesses, cwd=/tmp ~49%
  cheaper; load vocab via canonical extraction, not naive scrape).
- The D&E source: `sources/chapters/thk/thk-dunk-01.md`, `tss/tss-dunk-01.md`, `tmk/tmk-dunk-01.md`
  (single-file novellas — NOTE: not yet chapter-split the way the 5 books are; the plan must decide whether
  to split them first or run whole-novella).
- The current Pass-1 contract: the `mechanical-extractor` agent + the v3 12-category prompt (memory
  `project_pass1_prompt_v3_canonical`); all Pass 1 ran on Opus (`project_pass1_all_opus`).

## Plan to produce (the deliverable)
1. **Harness review:** how does a pass get "passed into" `worker-template.py` + `longrun.sh` today? Document
   the actual contract (config/env/args). Note any gaps that block an unattended D&E run.
2. **D&E sub-script / orchestrator config:** design (scaffold, don't run) the D&E-specific worker config —
   the 3 novellas as work items, output → `extractions/mechanical/{thk,tss,tmk}/` (NEW dirs; **never** an
   archive folder — `feedback_extraction_archive_rules`), Opus, `claude -p` per `reference_llm_pass_via_claude_p`.
3. **Prompt-improvement prereq (separate sub-task, flag it):** the v3 Pass-1 prompt predates everything since
   the first book passes — Matt wants it improved before the run ("we can def make those prompts better").
   Scope what to improve; this is a prereq gate, likely its own small step.
4. **Chapter-split decision:** do the D&E novellas need `scripts/chapter-splitter.py` treatment first, or run
   whole-novella? Decide + note.
5. **Run/monitor/resume plan:** exact launch command, where logs/telemetry land, how longrun survives
   rate-limit walls + resumes, how to verify output (counts, schema validator / drift-detection per
   `feedback_drift_detection_mandatory`).
6. **STOP — do not launch.** End with a "ready to fire?" checklist for Matt. Confirm before any extraction.

## Vocabulary (PASTE into any naming/sequencing subagent — they don't load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · lowercase step = ordered piece · Tier = confidence 1–5 ONLY. No new capitalized terms.

## DO NOT
Launch ANY extraction without Matt's explicit confirm (`feedback_no_extraction_without_asking`) · write
extractions to archive folders (canonical `extractions/mechanical/{book}/` only) · refetch wiki · skip the
prompt-improvement prereq · `/endsession` without explicit permission.
