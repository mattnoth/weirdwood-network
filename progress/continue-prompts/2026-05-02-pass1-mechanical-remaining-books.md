# Pass 1 Mechanical Extraction — ACOK / ASOS / AFFC / ADWD

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-05-01 (Session 30 start). Decision made this session: complete Pass 1 across all remaining books **before** launching Stage 4 v1 prose-edge classification. Reasoning: Stage 4's contradiction-sweep component compares wiki node prose to chapter Pass-1 extractions; AGOT-only contradiction sweep would have to re-run for each later book. Get the corpus complete first, then Stage 4 ships clean against all 5 books in one pass.

---

## Why this work, why now

Pass 1 mechanical extraction is **Step 4 of the pipeline** (per `CLAUDE.md` table) and the longest-standing piece of unfinished foundation work. AGOT v3 is complete (73/73). The remaining 4 books gate:

- **Stage 4 v1 contradiction sweep** — compares wiki claims to Pass-1 mentions; needs corpus coverage to be useful as a single pass
- **Pass 3 voice/perception analysis** — cross-POV perception edges require all chapters where each POV character appears
- **Pass 4 foreshadowing scanning** — needs the full timeline of mentions to map plant→payoff
- **Pass 5 theory-informed extraction** — needs the full corpus
- **Trigger table / index build** — emits from Pass 1 outputs

Stage 4 v1 prose-edge discovery (the wiki→wiki edge work) does NOT block on this and is a separate parallel track once usage-limit headroom exists. But sequencing-wise, Matt chose Pass 1 first this session.

---

## Hard constraints (carry-forward, non-negotiable)

- **NEVER auto-launch agent runs without confirming each batch with Matt.** Each book launch confirmed separately. Each batch within a book confirmed separately.
- **NEVER run `/endsession` without explicit permission.** Hard rule — historically violated multiple times.
- **NEVER commit copyrighted source content.** `sources/raw/` and `sources/chapters/` are gitignored and stay that way. Extractions in `extractions/mechanical/` are derivative outputs and ARE committed.
- **Extraction goes through the `weirwood` pipeline in iTerm, not background subagents.** This is a hard memory rule. Do NOT spawn `mechanical-extractor` agents from the orchestrator's tool calls. The user launches via `weirwood <book> <terminals> <waves>` in their terminal.
- **Usage-limit graceful-fail is built in** — the soft-stop file (`/tmp/extraction-stop`) plus wave-boundary checkpointing plus resume-aware re-launch. Do not "improve" it by adding mid-wave interruption.
- **`first_available` deferred** — agent prompts already updated; do not re-introduce the rule.

---

## State at session start (verify before doing anything)

```bash
# Verify HEAD
git log --oneline -3

# Check Pass 1 progress per book
for d in extractions/mechanical/*/; do
  b=$(basename "$d")
  done=$(ls "$d"/*.extraction.md 2>/dev/null | wc -l | tr -d ' ')
  total=$(ls sources/chapters/"$b"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "  $b: $done/$total"
done
# Expected at start of this work:
#   agot:  73/73   (done)
#   acok:  70/70   (done BUT 50 chapters are v2 schema — need re-run of waves 1-10)
#   asos:   0/82
#   affc:  46/46   (done)
#   adwd:   0/73

# Verify weirwood is sourced + sees the books
weirwood
# Should print all-books overview with chapter counts

# Verify chapter files exist (gitignored, but on disk)
ls sources/chapters/affc | head -3
# Should show affc-aeron-01.md, affc-arianne-01.md, etc.

# Confirm no stale stop file
ls -la /tmp/extraction-stop 2>/dev/null && echo "STOP FILE EXISTS — clear before launching"
```

**ACOK state (updated Session 30):** `extractions/mechanical/acok/` has 70 files but chapters 1-50 (arya/bran/catelyn/daenerys/davos/jon/prologue/sansa/theon-01) are v2 schema (4-category Raw Entity List). Chapters 51-70 (theon-02 through tyrion-15) are v3. Re-run waves 1-10 first: `weirwood-mechanical --chain acok 4 1` then stop after wave 10. Confirm with Matt before launching.

---

## Pipeline shape

### Book order (confirmed Session 30)
1. **AFFC** — 46 chapters / 10 waves / ~2 hrs at 4 terminals. **Canary book.** Smallest remaining book; runs first to verify v3 prompt holds up on a non-AGOT book before committing the larger books.
2. **ACOK** — 70 chapters / 14 waves / ~3 hrs
3. **ASOS** — 82 chapters / 17 waves / ~3.5 hrs
4. **ADWD** — 73 chapters / 15 waves / ~3 hrs

**Total: 271 chapters / 56 waves / ~11.5 hrs wall-clock at 4 terminals.** That's at least 2-3 usage-limit windows. Plan to checkpoint at book boundaries.

### Launch sizing (UNDECIDED — confirm with Matt first)

Two options, both honor the usage-limit concern:

**Option A — Manual batched (preferred for canary book):**
```bash
weirwood affc 2 3      # 2 terminals, 3 waves each = 6 waves of 5 chapters = 30 chapters
# wait ~30 min, check sample extraction quality, relaunch
weirwood affc 2 3      # picks up from next incomplete wave automatically
```
Smaller blast radius. Matt can sample-review extractions between batches and catch any v3-prompt drift on a new book before it scales.

**Option B — Chained with soft-stop (faster, less hands-on):**
```bash
weirwood affc --chain 4   # 4 terminals cycle through all remaining waves
# When usage window is about to close:
weirwood stop             # soft-stop, halts at next wave boundary
```
Fire-and-forget within a single usage window. Stops cleanly. Resume next window with another `--chain`.

**Recommendation:** Option A for AFFC (canary). After AFFC completes cleanly, switch to Option B for ACOK/ASOS/ADWD (proven prompt, no further mid-book sample-review needed).

### Per-book acceptance criteria

For each book:
- Every chapter in `sources/chapters/<book>/` has a corresponding `.extraction.md` in `extractions/mechanical/<book>/`
- Spot-check: open 2-3 random extractions and verify all 12 Raw Entity List categories present (per v3 prompt — strict formatting rules)
- No `_FAILED` markers / no zero-byte extraction files / no truncated outputs
- `working/extraction-stats/extraction-stats-<book>-pass1-v3.csv` populated

### Cross-book canary check (after AFFC completes)

Before launching ACOK, sample 5 random AFFC extractions and verify:
- All 12 Raw Entity List categories present (with "None" for empty categories — never elided)
- Character Appearances section populated (v2/v3 addition)
- Food & Drink section populated where applicable
- Hospitality & Guest Right correctly flagged at any feast scenes
- POV Character's Internal State present
- No regressions vs AGOT v3 quality

If quality is good → proceed to ACOK. If drift detected → surface to Matt before scaling.

---

## Recommended execution order

1. **Pre-flight** — verify state per checks above. Confirm with Matt:
   - Launch sizing: Option A (manual batched) for AFFC, Option B (chained) for the rest? Or all manual?
   - Who launches: Matt in iTerm, or orchestrator via `! weirwood ...` from this session?
2. **AFFC canary** — first batch (Option A). ~30 min wall-clock. Stop. Sample-review.
3. **AFFC continuation** — finish AFFC. ~1.5 hr more wall-clock.
4. **AFFC quality check** — 5-extraction sample review. Confirm prompt holds up.
5. **ACOK** — full run (Option B chained, or continue Option A). ~3 hrs.
6. **ASOS** — full run. ~3.5 hrs.
7. **ADWD** — full run. ~3 hrs.
8. **Final verification** — `extractions/mechanical/{acok,asos,affc,adwd}/` all complete. 344/344 across all 5 books.
9. **Update worklog.md** — Session N entry with totals + cost + duration.
10. **Hand off to Stage 4 v1** — continue prompt at `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` (drop AGOT-only carve-out — Stage 4 contradiction sweep now spans all 5 books).

---

## Files / commands reference

**Launcher:**
- `scripts/weirwood.zsh` — sourced shell function (entry point: `weirwood <book> <terminals> <waves>`)
- `scripts/launch-extraction.sh` — underlying iTerm tab launcher
- `scripts/run-extraction-wave.sh` — per-wave executor (calls `claude` CLI per chapter)
- `scripts/extract.sh` — status / launch dispatcher

**Agent prompt (do NOT modify mid-run):**
- `.claude/agents/mechanical-extractor.md` — Pass 1 v3 prompt (12-category Raw Entity List)

**Outputs:**
- `extractions/mechanical/{book}/` — per-chapter `.extraction.md` files
- `working/extraction-stats/extraction-stats-{book}-pass1-v3.csv` — token + timing stats per chapter

**Reference:**
- `working/runbooks/mechanical-extraction-howto.md` — operational details
- `progress/pass1-agot.md` — AGOT v3 wave log (use as template for ACOK/ASOS/AFFC/ADWD progress files if needed)
- `reference/architecture.md` — entity types + relationship taxonomy v3 honors

**Soft-stop:**
- `/tmp/extraction-stop` — touch this file (or run `weirwood stop`) to halt at next wave boundary
- Auto-cleared on next launch

---

## Don'ts (process)

- **Don't run `/endsession` without explicit permission.** Historically violated.
- **Don't auto-launch extractions** — Matt confirms each book + each batch.
- **Don't spawn `mechanical-extractor` subagents** from the orchestrator's tool calls. Extraction goes through `weirwood` in iTerm. Hard memory rule.
- **Don't modify the v3 prompt mid-run.** If a quality issue surfaces, stop, fix the prompt, archive partial outputs to `extractions/archives/<book>-v3-partial/`, restart cleanly. Never run two prompt versions on the same book.
- **Don't commit chapter files or extraction files containing copyrighted prose.** Extractions are structured derivative outputs and DO commit; the underlying chapter files DO NOT. Verify `.gitignore` is intact before any commit.
- **Don't promote prose-edges or run Stage 4** before all 271 chapters complete.

---

## Open questions for Matt (session start)

1. **Launch sizing:** Option A manual batched for everything, or A for AFFC + B for the rest, or B for everything?
2. **Terminal count:** 4 terminals matches AGOT v1 baseline (no usage-limit issues). Drop to 2 if you want extra headroom?
3. **Who launches:** you in iTerm, or me via `! weirwood ...` from this session?
4. **Per-book commit cadence:** commit extractions per-book, or one big commit at end of all 271?

---

## Reference

- AGOT v3 baseline: `extractions/mechanical/agot/` (73 files, archived progress at `progress/pass1-agot.md`)
- Earlier ACOK v2 partial run: `extractions/archives/acok-v2/` (50/70, schema differs — reference only, do not resume)
- v3 prompt change history: `working/session-details/session-014.md` and onward (search for "v3")
- Memory rules in effect: `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_no_extraction_without_asking.md`, `feedback_endsession_requires_permission.md`
