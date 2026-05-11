# Worklog Archive 008

> Sessions 34 onward. Each archive file holds exactly 5 entries (CLAUDE.md rule #8).

---

### Session 34 — ADWD complete + bug-fix landing + cleanup (2026-05-05)

**Changes made:**
- `extractions/mechanical/adwd/` — 73/73 v3 chapters complete (15 waves, 2026-05-05). Some duplicate wave entries from Bug A residue before fix landed; last-writer-wins, all valid v3. Was untracked — committed this session.
- `working/extraction-stats/extraction-stats-ADWD-pass1-v3.csv` — NEW. Was untracked — committed.
- `scripts/extract.sh` + `scripts/weirwood.zsh` — chain/race fix landed across commits `5f9b808f`, `f3cd92ba`, `dea679af` (Bug A `--chain` explosion + Bug B parallel-extraction race + UX cleanup with phase banners and streamed Claude assistant output). Two small follow-ups committed this session: `${_HEARTBEAT_PID:-}` guard (cmd_run trap) and arithmetic expansion fix in cmd_check.
- `progress/continue-prompts/archive/` — moved `2026-05-04-urgent-fix-chain-and-race-bug.md` + `2026-05-04-acok-waves1-10-rerun.md` (work complete).
- `working/todos.md` — URGENT BLOCKER block removed.
- `worklog.md` — Current State updated: ADWD 73/73, ACOK 70/70, ASOS line clarified (Okey running Opus on shared Max). This entry.
- `working/progress.md` — 22 ADWD wave rows appended (some duplicates from Bug A residue).

**State:** Pass 1 v3 4/5 books complete (AGOT 73 + ACOK 70 + AFFC 46 + ADWD 73 = 262/344). ASOS 0/82 pending Okey's push.

**Decisions:** None this session — execution + cleanup only. Design discussion on next-pass direction (dialogue extraction → Pass 3 voice-analyzer anchor) deferred to next session for prompt drafting + smoke test.

**What's next:**
- **PRIMARY HANDOFF:** `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — three new passes designed (dialogue, meals & feasts, per-chapter mention index) + Opus-as-sampling-oracle validation strategy + file organization proposal. Self-contained design doc; next session reads it end-to-end, resolves 7 Open Questions with Matt, then builds the mention index first as the free Python unblocker, then smokes dialogue on Ned (POV-rich) followed by Robert Baratheon (POV-less stress test for non-POV quote attribution + cross-POV perception capture).
- Wait on Okey's ASOS push to land (no Claude work needed until then; design + smoke can proceed on AGOT regardless).
- Stage 4 v1 prose-edge-classifier remains queued for once 5/5 Pass 1 books land (`2026-05-02-stage4-v1-prose-edge-classifier.md`).
