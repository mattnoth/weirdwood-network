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
