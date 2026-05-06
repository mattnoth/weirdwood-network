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
**Detail:** `working/session-details/session-030.md`

**Changes made:**
- `extractions/mechanical/acok/` — promoted 50 files from `extractions/archives/acok-v2/`; ran waves 11-14 (20 new v3 chapters: theon-02 through tyrion-15); re-ran tyrion-10 (silent drop during wave 13). Now 70/70.
- `worklog.md` — ACOK pipeline line updated to reflect 70/70 complete with schema-mix note.
- `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` — state check updated: ACOK now 70/70, v2/v3 schema split documented, re-run instruction added.
- `working/session-details/session-030.md` — NEW.

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

> Archived from worklog.md at end of Session 36 (2026-05-06). First archive file under the new strict 5-entry rule (CLAUDE.md orchestration rule #8). Currently holds 3 entries; will fill to 5 over future archive cycles.
