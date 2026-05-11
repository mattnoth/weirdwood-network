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

---

### Session 35 — ASOS Pass 1 complete via Okey's parallel run (2026-05-06)

**Changes made:**
- `extractions/mechanical/asos/` — 82/82 v3 chapters pushed by Okey on branch `origin/pass1-asos-extraction` (parallel Opus pass on shared Max account, ran 2026-05-01 → 2026-05-06, ~$54.85). All 12 POVs covered (13 Arya / 4 Bran / 7 Catelyn / 6 Daenerys / 6 Davos / 9 Jaime / 12 Jon / 5 Samwell / 7 Sansa / 11 Tyrion + Prologue + Epilogue). Spot-checked early/mid/late waves — full v3 schema, healthy. **Merged to main in commit `2eaf5c71` ("Merge ASOS Pass 1 v3 from Okey's parallel run") — verified 2026-05-07.**
- `worklog.md` — Current State updated: ASOS now 82/82 ✓ (Pass 1 5/5 books complete, 344/344). This entry.
- `working/progress.md` — single pointer line appended; per-wave detail lives in `working/extraction-stats/extraction-stats-asos-pass1-v3.csv` on Okey's branch.

**State:** Pass 1 v3 ALL 5 books complete (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73 = 344/344). Stage 4 prose-edge-classifier and the dialogue/meals/mention-index design are the unblocked next moves.

**Decisions:** None — verification + worklog hygiene only. Okey's branch left unmerged for now (merge when ready; minor `worklog.md` + `working/progress.md` conflicts expected, no extraction-file collisions).

**What's next:**
- Merge `origin/pass1-asos-extraction` into main when ready (resolve worklog/progress conflicts in favor of main's clean entry).
- Resume primary handoff: `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — 7 Open Questions to resolve, then build mention index, then smoke dialogue on Ned + Robert.
- Stage 4 v1 prose-edge-classifier now unblocked: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

### Session 36 — Hygiene pass + soft-convention hardening (2026-05-06)
**Detail:** `history/session-details/session-036.md`

**Changes made:**
- 3 stale Pass 1 continue prompts → `progress/continue-prompts/archive/`. `progress/SESSION-32-HANDOFF.md` → `history/worklog-archives/session-32-handoff.md`.
- `progress/scratch-notes.md` deleted; three referenced long-form entries folded into `working/todos.md` lines that referenced them. Rest dropped (stale or redundant).
- Cleaned scratch-notes/handoffs.md refs in `CLAUDE.md`, `README.md`, `STATUS.md`, `.claude/agents/status-reporter.md`, `.claude/commands/endsession.md`.
- `CLAUDE.md` orchestration rules #7 and #8 rewritten: session-details now explicitly as-needed (not every-session); worklog Session Log strict 5-entry max with archives holding exactly 5 entries each.
- `CLAUDE.md` new section "Top-Level `scratch` File — Ignore It" before Orchestration Rules. Tells agents to ignore scratch outside `/endsession` step 4(a). `.gitignore` updated; root `scratch` file untracked.
- `.claude/commands/endsession.md` step 4 expanded with scratch-triage subroutine; step 6 rewritten to strict 5-entry rule.
- `working/todos.md` staleness sweep: Pass 1 model-fit smoke test obsoleted, Stage 4 prereq-met, agent-stub vs full-prompt status corrected, citation-validator queued for verify, spoiler-gating prereq-met, model-fit policy phrasing updated. New "Project Story / Auxiliary" category with session-details audit todo. `READY TO DO` flag added on model-fit-audit todo.
- `worklog.md` two staleness fixes (entity-index todo obsoleted; Stage 4 skeleton ref refreshed).
- Archive operation under new rule: Sessions 27, 28, 29 appended to `archive006.md` (now 5 entries); Sessions 30 (×2 numbered entries) and 31 created `archive007.md` (3 entries, will fill over future cycles).
- Single commit `240fe565` "Hygiene pass: archive stale prompts, retire scratch-notes, harden conventions" — 15 files, +407/−214. Pushed to `origin/main`.

**Decisions:** **Five rule changes locked.** (1) Worklog Session Log strict 5-entry max, archive in 5-entry blocks; ambiguous "~150 lines" replaced with concrete count. (2) Session-details files are as-needed, not every-session — write only for design/incident/novel-decision sessions; pure-execution skips. (3) Top-level `scratch` is Matt's private space (gitignored, agents don't read outside /endsession). (4) `/endsession` step 4(a) triages scratch contents at end of every session. (5) `progress/scratch-notes.md` retired; replaced by the gitignored top-level scratch + designated triage moment. **Soft-conventions framing surfaced as a project pattern:** rules in prose without enforcement drift over time; rules in /endsession do better but conditional steps still slip; hooks add real enforcement when the action must not be skipped (none built this session — all current cases are well-served by strict /endsession steps). **Hooks vs rules clarified:** rule = read; hook = executed; both together is "double cost" only when redundant; rules in /endsession alone are sufficient when /endsession is reliably invoked. **`working/todos.md` reorganization deferred** — proposed structure exists in conversation but not executed; Matt paused before approving.

**What's next:**
- **PRIMARY HANDOFF unchanged:** `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — design pass for dialogue/meals/mention-index passes, awaiting Matt's review of 7 Open Questions.
- **`working/todos.md` reorganization** — proposed 12-section structure + parallel `working/todos-archive.md`; restart this in next session.
- **`READY TO DO` next** (per todos.md): model-fit audit across `.claude/agents/*.md` (resource-conservation pass). And: re-run `citation-validator` on full 5-book corpus now that Pass 1 is 344/344.
- Stage 4 v1 still queued: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

### Session 37 — Cleanup scrubs + model-fit audit (2026-05-06)

**Changes made:**
- **Scrub A (D&D framing retired):** moved `working/chat-ui-architecture.md` and `working/diagrams.md` → `history/archive/sketches/` with stale-sketch preambles. Deleted 2 chat-UI/D&D-framed bullets in `working/todos.md` (Q5(a) two-repo split + Q6 unrelated chat-UI-scope bullet). Q6 spoiler-gate bullet kept (defer; rides on existing first_available deferral).
- **Scrub B (copyright rule deleted entirely):** removed the textual rule from CLAUDE.md, README.md (line 220 surgical), worklog.md Current State, .claude/commands/endsession.md (step 7 deleted, renumbered), dialogue-meals continue prompt, runbooks/book-integration-done.md, scratch-design-review-stage3b.md, memory MEMORY.md + memory feedback_never_commit_books.md (deleted), memory project_real_goal_graph_for_agents.md (two-repo line deleted per Q5=a). `STATUS.md` retired entirely (Q3=b). Mechanical protection (.gitignore + .claude/settings.json permission denials) is now the only line of defense.
- **Citation-validator full-corpus re-run** at `working/audits/citation-corpus-rerun-2026-05-06/execution/citation-issues.md`: PENDING-PASS-1 bucket from 2026-04-30 audit fully closed, zero broken chapter-file references, zero new HIGH findings. Several Stage-1 cite-format issues from prior audit have been re-emitted away in interim node-rebuild work.
- **Model-fit audit** at `working/audits/agent-model-fit-2026-05-06/execution/agent-model-fit-report.md`: 27 agents audited. 6 Opus → Sonnet (mechanical-extractor, wiki-ingester, citation-validator, orphan-edge-finder, prose-edge-classifier [smoke-test gated], schema-drift-auditor). 2 → Haiku (status-reporter, duplicate-detector). 2 keep Opus (cross-identity-detector + reviewer — high-stakes, low-volume SAME_AS decisions). 13 STUBs deferred. Fleet-plan near-term spend (Stages 1-3) drops from $100-200 to $25-65 if classifier smoke passes — 60-75% reduction.
- **D&E Pass 1 reframed in Current State:** "deferred (enrichment pass for main-arc nodes)" per Q11=(b). Not dropped, not urgent, not on active critical path.
- **Audit folder layout adopted (Q10):** new audits land at `working/audits/<slug>-YYYY-MM-DD/{prompt-planning,prompt,execution,validation}/`. Existing flat-path audits not migrated; new layout for new audits only.

**Decisions:** **Two cleanup scrubs landed.** D&D-group / shared-password / friend-group-only chat-UI framing retired across docs, todos, and one memory file; the *concept* of a chat UI is preserved as "ask-questions interface on top of the graph" (per the handoff's reframe), but as a NEW future todo, not a salvage of the retired bullets. **Copyright textual rule deleted entirely** — Matt's call: gitignore + permission denials suffice, the textual reminder created drift not safety. **Per-audit folder layout adopted (Q10)** to make audit + validation pairs first-class. **Model-fit recommendations queued for Matt's review** before any agent prompt frontmatter changes; smoke-test gates explicit. **Hooks follow-up captured** — two PreToolUse hooks (block edits to historical archives + block edits under sources/) added to todos.md as separate items, not freelanced this session.

**Unexpected surface:** `validate-2026-05-06-handoff-cleanup-and-direction.md` at repo root (untracked) — sibling validation prompt for this scrub work. Contains 11 "copyright" + ~7 "chat-ui/D&D" anchor strings as part of describing what to check. Not in scope per § 3 of the handoff. Flagged for Matt to triage at /endsession (move to `working/audits/<slug>/validation/` per Q10, archive next to the handoff, or run it).

**What's next:**
- **Strategic question deferred (Q12=b):** Stage-4-vs-mention-index choice — re-read both queued continue prompts under graph-for-agents lens — left for a separate fresh session.
- **Two new READY-TO-DO follow-ups in `working/todos.md`:** (a) review fleet plan against model-fit recommendations, (b) two PreToolUse hooks (block edits to historical archives, block writes under sources/).
- **Continue prompts active (3):** `2026-05-02-stage4-v1-prose-edge-classifier.md`, `2026-05-05-dialogue-meals-mention-index-design.md`, plus this handoff (will be archived at /endsession).
- **Per Matt's standing rule, /endsession is NOT auto-run** — handoff prompt awaits Matt's invocation.
