### Session 31 — Pass 1 launch prep: auto-advance feature + schema cleanup (2026-05-04)

**Changes made:**
- Memory system updated: `project_pass1_schema_versions.md` — NEW. Documents v3 as canonical, v1/v2 archived for reference. Clarifies that ACOK v2 chapters in archive ≠ incomplete work. Added to `MEMORY.md` index.
- `extractions/archives/acok-v2-original-2026-05-04/` — NEW archive folder. All 50 v2 ACOK chapters (prologue through theon-01) moved here for preservation. v3 chapters (theon-02 through tyrion-15) restored to canonical `extractions/mechanical/acok/` (20 files).
- `scripts/extract.sh` — UPDATED. Added `--delay <duration>` and `--chain` parameters to cmd_launch. New helper: `parse_duration_to_seconds()`. Auto-advance logic: after launching initial batch, waits for specified delay, then re-launches next batch of incomplete waves. Enables hands-off multi-batch runs (e.g., `2h` waits between batches to spread token usage across session windows).
- `scripts/weirwood.zsh` — UPDATED. Passes `--delay` and `--chain` flags through to launch command. Help text updated with new examples: `weirwood acok 2 1 --delay 2h --chain`.
- Schema version clarity locked in: v3 is main prompt; previous versions archived; no future confusion.

**Decisions:** 2-hour delays between ACOK batches to spread token usage across API windows. Auto-advance feature (`--chain`) handles re-launching without manual intervention. Quality consistency enforced — all books extracted with v3 schema (Opus). Archive structure prevents confusion. Next session: smoke-test 1-2 waves to verify v3 schema before committing to full re-run.

**What's next:** Session 32 — ACOK re-run with smoke test. Command: `weirwood acok 2 1 --delay 2h --chain`. Verify waves 1-2 quality before auto-advancing. Full run: 10 waves / 50 chapters / ~10 hrs wall-clock with 2h delays. Continue prompt: `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md`.

### Session 30 — ACOK Pass 1 completion + schema-mix discovery (2026-05-02)
**Detail:** `history/session-details/session-030.md`

**Changes made:**
- `extractions/mechanical/acok/` — promoted 50 files from `extractions/archives/acok-v2/`; ran waves 11-14 (20 new v3 chapters: theon-02 through tyrion-15); re-ran tyrion-10 (silent drop during wave 13). Now 70/70.
- `worklog.md` — ACOK pipeline line updated to reflect 70/70 complete with schema-mix note.
- `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` — state check updated: ACOK now 70/70, v2/v3 schema split documented, re-run instruction added.
- `history/session-details/session-030.md` — NEW.

**Decisions:** ACOK 70/70 complete at `extractions/mechanical/acok/` but is a schema mix: chapters 1-50 (archived v2 run from the night before Session 30, before v3 existed) have 4-category Raw Entity List; chapters 51-70 have v3 12-category. Re-run waves 1-10 when usage budget allows (`weirwood-mechanical --chain acok 4 1`, stop after wave 10). Future books (ASOS, ADWD) will be single-pass v3. Friend running ASOS confirmed: no prompt update needed, v3 is current.

**What's next:**
- Re-run ACOK waves 1-10 to fix v2/v3 schema mix (50 chapters)
- Then ASOS (0/82) and ADWD (0/73) — single-pass v3 each
- Continue prompt: `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`

### Session 30 — Pass-1-first sequencing decision + Stage 4 v1 prompt amended (2026-05-01)

> **Note on numbering:** Two sessions in this archive share the number 30. Both are preserved as-is rather than renumbering history. The first (above, dated 2026-05-02) covered ACOK Pass 1 completion. This second one (below, dated 2026-05-01) covered the sequencing decision that preceded it. The dates make the actual order unambiguous.

**Changes made:**
- `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` — NEW. Self-contained continue prompt for Pass 1 mechanical extraction across ACOK/ASOS/AFFC/ADWD. Order: AFFC (canary, 46ch) → ACOK (70) → ASOS (82) → ADWD (73). 271 chapters / 56 waves / ~11.5 hrs at 4 terminals. Existing `weirwood` infra reused (soft-stop + wave checkpointing = graceful-fail). Hard pre-flight checks; per-book acceptance criteria; canary-quality-check after AFFC; both manual-batched and `--chain` launch options documented.
- `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` — UPDATED. Pass-1 dependency now resolved up-front (no longer "AGOT-only v1 + back-fill v2"). Contradiction sweep now spans all 5 books in a single pass. Open question 3 marked RESOLVED. Pre-flight check for 344/344 chapter parity added.
- `worklog.md` — Session 29 "What's next" reordered: Pass 1 first, Stage 4 v1 second. New Session 30 entry (this).

**Decisions:** Sequence Pass 1 corpus completion BEFORE Stage 4 v1 (Matt-decision Session 30, "I need to get the books in then"). Reasoning: Stage 4's contradiction-sweep component compares wiki node prose to Pass-1 mentions; AGOT-only sweep would have to re-run for each later book as Pass 1 lands. Bundling the corpus-complete prep with Stage 4 v1 launch means a single clean deliverable instead of N back-fills. Pass 1 also unblocks Pass 3/4/5/6 + trigger-table + index work that Stage 4 doesn't touch. Stage 4 v1 (when it eventually launches) will include Tier-B nodes (Matt-decision Session 30: thin-infobox ≠ thin-prose; Tier-B is where prose-edge yield is proportionally MOST valuable since Python had less to extract there). Cross-identity escalation runs INLINE in Step 3 (single load of source prose) with flags batched to `cross-identity-queue.jsonl` for end-of-pass review (avoids double-load while preserving review batching). Usage-limit graceful-fail = the existing `weirwood` soft-stop (`/tmp/extraction-stop`) + wave-boundary checkpoint pattern — no new scripts needed for Pass 1; Stage 4 launcher will mirror this pattern when it ships.

**No code changes; no agent runs; no commits this session.** Planning + prompt-amendment only.

**What's next:** Launch Pass 1 per the new continue prompt. Open questions deferred to launch-time (in iTerm session): manual-batched vs `--chain`, 4 terminals vs 2, who launches, per-book vs end-commit cadence. Stage 4 v1 follows once 344/344 extractions exist.

### Session 32 — ACOK v3 confirmation + ready for auto-advance launch (2026-05-04)

**Context:** Session 31 built auto-advance feature. Smoke test attempted to verify v3 quality on ACOK waves 1-2, but Opus model running slower than expected. Session 32 verified prompt status and prepared handoff.

**Changes made:**
- `mechanical-extractor` agent prompt (`.claude/agents/mechanical-extractor.md`) — CONFIRMED using v3 canonical schema: 12-category Raw Entity List (Characters, Locations, Houses, Factions & Organizations, Religions & Faiths, Cultures & Peoples, Artifacts & Objects, In-world Texts & Songs, Magic & Phenomena, Wars & Conflicts, Titles & Offices, Other). Plus all v3 sections: Physical Environment, Character Appearances, Food & Drink, Hospitality & Guest Right, POV Character's Internal State, etc. Model set to Opus.
- `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md` — UPDATED: clarified state (20 ACOK chapters FINAL with v3, 50 in archive `acok-v2-original-2026-05-04/`), removed smoke-test section (v3 already proven on AGOT + confirmed on 20 ACOK chapters), added "Launch Full Auto-Advance Run (Session 33+)" with single command ready to execute.

**Decisions:** No smoke test needed — v3 is canonical and proven. Opus model confirmed; do not substitute Sonnet/Haiku for consistency with AGOT v3. Handoff complete. Next session: fresh iTerm session, run `weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain` immediately. No pre-flight checks — state already verified.

**What's next:**
- **Session 33+:** Fresh session → `weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain` (50 chapters, 10 waves, ~10 hrs wall-clock with 2h delays)
- After ACOK 70/70 complete: ASOS (82 chapters, single-pass v3) and ADWD (73 chapters, single-pass v3) per continue prompt `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`
- Once 344/344 complete: Stage 4 v1 prose-edge-classifier per continue prompt `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`

### Session 33 — ACOK chain-launch terminal explosion + race-condition bug discovery (2026-05-04)
**Detail:** `history/session-details/session-033.md`

**Changes made:**
- `extractions/mechanical/acok/` — waves 1-4 re-extracted to v3 (acok-arya-01..10, acok-bran-01..07, acok-catelyn-01..03). Some chapters were extracted twice in parallel due to bug below; second-finishing version won. All landed valid v3.
- `progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md` — NEW (BLOCKER continue prompt).
- `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md` — UPDATED: marked BLOCKED on the urgent fix, status reflects 40/70 v3 with waves 5-10 still v2.
- `history/session-details/session-033.md` — NEW.
- `working/todos.md` — added BLOCKER row for chain/race fix; added model-fit smoke-test todo for Pass 1 (Sonnet vs Opus); flagged model-fit-rule as standing principle.
- `worklog.md` — ACOK pipeline line updated to 40/70 + BLOCKED. This entry.

**Decisions:** Two distinct bugs in `scripts/extract.sh` discovered. **Bug A (extract.sh:689-695):** `--chain` causes terminal explosion — every spawned terminal independently re-launches `extract.sh launch -t N --chain`, doubling the tab count each cycle (2→4→8). **Bug B (extract.sh:117-127 + cmd_run loop):** `is_complete()` only detects finished files, not in-progress claims. Two parallel terminals can both decide "missing" and both extract the same chapter, last-writer-wins. Bug B fires whenever Bug A spawns overlapping waves, OR on any accidental double-launch. My `pkill` cleanup made things WORSE because the terminal command lines use `;` chaining, so killing each step advanced the chain to the next step (which spawned MORE tabs). Correct stop is `weirwood stop` or closing iTerm tabs. **Fix decided + iterated to a six-item patch:** (1) drop `--chain`/`--delay` entirely; (2) per-chapter status enum in the stats CSV (`not_started`/`started`/`working`/`done`/`failed-rate`/`failed-error`/`failed-stale`/`skipped-*`) + new columns (`last_heartbeat`, `terminal_id`, `retry_at`) + atomic claim via `flock`; (3) startup stale-sweep (heartbeat >90s primary + row age >30min fallback → `failed-stale`); (4) `weirwood <book>` live status table only when started/working rows exist (otherwise existing static summary); (5) terminal log cleanup — drop all dollar amounts, delete broken `0\n0 events | 0\n0 relationships` counters, restructure into `[1/3] Preparing / [2/3] Extracting / [3/3] Complete` phases with `═` wave banners; (6) stream `claude -p`'s assistant output to terminal via tee → `scripts/stream-claude-output.py` → stderr with `│ ` prefix (full text + tool_use, no flag — terminal output doesn't enter context). Plus one-time auto-migration of existing CSVs with `.bak` backup. Sonnet-class work, do not use Opus. **Model-fit policy** added per Matt's request: default to cheapest model that can do the job; Opus only when reasoning depth genuinely requires it. **Sonnet smoke-test for Pass 1 explicitly OUT of urgent-fix scope** — Matt wants at least one full Opus pass on every book first (friend is running ASOS on Opus from shared Max); revisit once one book remains. ~$19 wasted on duplicate extractions; in-flight Claude calls also wasted to pkill.

**What's next:**
- **URGENT first:** `progress/continue-prompts/2026-05-04-urgent-fix-chain-and-race-bug.md` — fix both bugs in extract.sh, smoke-test, commit.
- **Then:** `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md` — re-run 30 remaining v2 chapters (waves 5-10) with the fixed launcher. NO `--chain` even after fix.
- ASOS / ADWD via `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`. Open: Sonnet vs Opus smoke-test before committing Opus to 155 more chapters.
- Stage 4 v1 — `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` — gated on 344/344 Pass 1 complete.

> Archived from worklog.md at end of Session 36 (2026-05-06), Session 37 (2026-05-06), and Session 38 (2026-05-06). Now full at 5 entries per CLAUDE.md orchestration rule #8 — next archive cycle creates `archive008.md`.
