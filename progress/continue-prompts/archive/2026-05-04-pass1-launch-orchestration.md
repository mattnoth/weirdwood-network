---
title: Pass 1 Mechanical Extraction Launch — AFFC/ACOK/ASOS/ADWD
date: 2026-05-04
model: haiku
focus: orchestration
---

# Pass 1 Launch — Fresh Session

> **Context:** Session 31 cleaned up ACOK schema mix and locked in v3 as the canonical prompt. Archives reorganized. This is your fresh launch session.

---

## What Just Happened (Session 31)

- **v3 is now canonical.** Memory system locked in so future sessions don't get confused by archive folders.
- **ACOK reorganized:** 50 v2 chapters archived to `extractions/archives/acok-v2-original-2026-05-04/`. 20 v3 chapters (theon-02 through tyrion-15) returned to `extractions/mechanical/acok/`.
- **Ready to launch:** All infrastructure in place. Continue prompt exists. Just needs you to coordinate the launch with Matt.

---

## Your Job

You are the **orchestrator for Pass 1 mechanical extraction.** Your role:

1. **Verify state** — check chapter counts per book
2. **Confirm with Matt** — ask the two launch-sizing questions (see below)
3. **Surface key decisions** — who launches (Matt in iTerm vs. orchestrator via `! weirwood`), launch sizing per book
4. **Hand off to Matt** — provide the exact command(s) to run in iTerm
5. **Monitor completion** — spot-check extractions as they land
6. **Update worklog** — track cost, duration, acceptance

---

## Current State (verify before proceeding)

```bash
# Run these checks in iTerm
git log --oneline -1
for d in extractions/mechanical/*/; do
  b=$(basename "$d")
  done=$(ls "$d"/*.extraction.md 2>/dev/null | wc -l | tr -d ' ')
  total=$(ls sources/chapters/"$b"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "  $b: $done/$total"
done

# Expected:
#   agot:  73/73   ✅ (done with v3)
#   acok:  20/70   ⚠️  (only v3 chapters; 50 v2 in archive waiting for waves 1-10 re-run)
#   asos:   0/82   
#   affc:  46/46   ✅ (already done with v3)
#   adwd:   0/73   
```

If ACOK shows 70/70 instead of 20/70, the restore didn't work. Let me know.

---

## Open Decisions — Ask Matt

### 1. Launch Sizing for AFFC (canary book)

AFFC is smallest (46 chapters). It runs first to verify v3 quality on a fresh book before scaling to larger books.

**Option A — Manual batched (safer, allows mid-run sample review):**
```bash
weirwood affc 2 3      # 2 terminals, 3 waves each = 6 waves = 30 chapters
# wait ~30 min, sample-review, relaunch
weirwood affc 2 3      # picks up next waves automatically
```
Pros: Can spot-check extractions between batches. Cons: More hands-on.

**Option B — Chained (faster, fire-and-forget):**
```bash
weirwood affc --chain 4   # 4 terminals, cycles through all waves
# When ready: weirwood stop (soft-stop at wave boundary)
```
Pros: Faster, less manual overhead. Cons: Can't sample until done.

**Recommendation:** Option A for AFFC canary to prove the prompt holds up, then switch to Option B for ACOK/ASOS/ADWD (proven prompt, no further mid-book review needed).

**Ask Matt:** A or B for AFFC?

### 2. Per-Book Launch Mode (after AFFC)

Once AFFC proves out, do you want:
- **Manual batched per book** (ACOK batch → wait → ASOS batch, etc.) — safer but slower
- **Chained across all remaining books** (`--chain acok 4`, then `--chain asos 4` when done, etc.)

**Recommendation:** Chained mode (faster) — AFFC already proved the prompt.

**Ask Matt:** How to sequence ACOK/ASOS/ADWD launches?

---

## Existing Continue Prompt

The full playbook lives at:
```
progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md
```

This document covers:
- **Book order:** AFFC (canary, 46ch) → ACOK (70) → ASOS (82) → ADWD (73)
- **Wave breakdown:** 56 waves total / ~11.5 hrs at 4 terminals
- **Acceptance criteria per book:** chapter counts, sample extraction quality, no `_FAILED` markers
- **Cross-book canary check:** 5-extraction sample after AFFC
- **Usage-limit graceful-fail:** soft-stop file at `/tmp/extraction-stop`, wave-boundary checkpointing

Read it. Use it as your reference.

---

## What You Do Now

1. **Verify state** — run the checks above
2. **Ask Matt the two questions** — sizing for AFFC, sequencing for ACOK/ASOS/ADWD
3. **Once Matt decides** — provide exact command(s) to run in iTerm
4. **Monitor extractions as they land** — spot-check 2-3 random files
5. **After AFFC completes** — run the 5-extraction sample review per continue prompt (before launching ACOK)
6. **Track metrics** — token count, wall-clock time, any failures
7. **Update worklog** — Session N entry with final tally

---

## Key Rules (Don't Forget)

- **v3 is canonical.** No version confusion.
- **NEVER auto-launch agent runs.** You ask Matt before each batch.
- **Extraction runs in iTerm via `weirwood` pipeline, not as background subagents.**
- **Usage-limit graceful-fail is built in** — the soft-stop file + wave checkpointing. Trust it.
- **NEVER run `/endsession` without explicit permission.**
- **Archives are archives.** The 50 ACOK v2 chapters in `acok-v2-original-2026-05-04/` are reference only. Don't get confused by them.

---

## How to Proceed

1. Ask Matt: Which launch sizing for AFFC? Manual (Option A) or chained (Option B)?
2. Ask Matt: After AFFC, how to sequence remaining books?
3. Once confirmed, provide the exact iTerm commands
4. Monitor + track as specified above
