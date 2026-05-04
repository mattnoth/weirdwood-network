---
title: ACOK Waves 1-10 Re-Run with Auto-Advance + Smoke Test
date: 2026-05-04
model: haiku
focus: execution
---

# ACOK Re-Run: 50 V2 Chapters → V3 Schema

> **Context:** Session 31 built the auto-advance feature. 50 ACOK chapters (v2 schema) are archived at `extractions/archives/acok-v2-original-2026-05-04/`. Ready to re-extract with v3 schema using automatic 2-hour delays between batches.

---

## What You're Doing

**Converting 50 ACOK chapters from v2 schema (4 categories) to v3 schema (12 categories).**

- Chapters 1-50 currently have v2 4-category Raw Entity List (old schema)
- Chapters 51-70 already have v3 12-category Raw Entity List (new schema)
- Goal: standardize all 70 to v3 for downstream consistency

**Why the smoke test?**
The v3 prompt hasn't been tested on a full fresh ACOK extraction (AGOT v3 proved the prompt, but ACOK has different POV character distribution). A 1-2 wave sample verifies quality before committing to the full 10-wave run.

---

## Current State — Verify Before Proceeding

```bash
# Check ACOK extraction status
weirwood acok

# Expected output:
#   ACOK: 20/70 chapters extracted
#   Completed waves: (none, or maybe a few if old v3 runs landed)
#   Missing waves: 1, 2, 3, ... 10 (50 chapters total)
#
# If you see 70/70, the v2 chapters are still in canonical location — 
# something went wrong in Session 31. Contact Matt before proceeding.

# Verify the archive exists
ls extractions/archives/acok-v2-original-2026-05-04/ | wc -l
# Should show 50
```

---

## Smoke Test: Waves 1-2 (10 chapters)

**Goal:** Extract first 10 chapters with v3 prompt, verify schema quality, then proceed.

```bash
# Launch JUST waves 1-2 (no delay, no chain — single batch)
weirwood acok 2 1
```

This opens 2 iTerm tabs. Terminal 1 runs wave 1, Terminal 2 runs wave 2, in parallel (~30 min total).

### After waves 1-2 complete:

1. **Check completion:**
   ```bash
   weirwood acok
   # Should now show: 20/70 → 30/70 (20 existing v3 + 10 new from waves 1-2)
   ```

2. **Spot-check 2-3 random extractions:**
   ```bash
   # Pick random chapters from waves 1-2 output, e.g., acok-arya-01, acok-bran-03, acok-catelyn-02
   cat extractions/mechanical/acok/acok-arya-01.extraction.md | head -100
   
   # Verify:
   #  - All 12 Raw Entity List headers present (Characters, Locations, Houses, etc.)
   #  - "None" for empty categories (not omitted)
   #  - Physical descriptions captured in "## Character Appearances"
   #  - Food & Drink section populated (ACOK has feast scenes)
   #  - POV Character's Internal State filled
   #  - No schema drift vs. AGOT v3 extractions
   ```

3. **Check stats:**
   ```bash
   cat working/extraction-stats/extraction-stats-acok-pass1-v3.csv | tail -15
   # Should show ~5 chapters per wave, cost tracking, no failures
   ```

---

## Smoke Test Decision

### If quality looks good ✅
Proceed to full auto-advance run.

### If issues found ❌
- Flag which category/section has problems
- Do NOT proceed to full run — investigate with Matt first
- The v3 prompt may need tweaking before scaling to all 50 chapters

---

## Full Auto-Advance Run (after smoke test approval)

**Command:**
```bash
weirwood acok 2 1 --delay 2h --chain
```

**What this does:**
- Waves 1-2 run in parallel (2 terminals)
- When done, waits 2 hours
- Auto-launches waves 3-4
- Waits 2 hours, then 5-6
- Continues: 7-8, wait 2h, 9-10
- **Total:** ~10 hours wall-clock across ~5 batches, 50 chapters, v3 schema

**Soft stop anytime:**
```bash
weirwood stop
# Terminates after the current wave finishes (graceful, no data loss)
```

**Monitor progress:**
- Check in every 2-3 hours to spot-check 1-2 random extractions
- Watch for rate-limit messages (script handles them, but worth knowing)
- After each 2h wait completes, next batch auto-launches

---

## Acceptance Criteria — Full Run

All 50 chapters extracted with v3 schema:
- ✅ `weirwood acok` shows 70/70 (20 existing v3 + 50 newly re-extracted)
- ✅ Sample 5 random chapters → all have 12 Raw Entity List headers
- ✅ No `_FAILED` markers / no truncated files / no zero-byte outputs
- ✅ `working/extraction-stats/extraction-stats-acok-pass1-v3.csv` has 70 rows (including the pre-existing 20)
- ✅ Worklog updated with cost, duration, chapter count

---

## If Something Goes Wrong

**Rate limit hit during run:**
- Script detects and pauses the wave
- Next auto-advance will retry
- Check `/tmp/extraction-stop` — if it exists, the script halted gracefully

**Wave takes longer than 2 hours:**
- Auto-advance may launch before previous batch finishes (intentional — allows some overlap)
- If terminals fill up, oldest terminal will finish, next batch picks up

**Need to abort mid-run:**
```bash
weirwood stop
# Stops after current wave, script exits cleanly
```

---

## Next Steps After ACOK 70/70 Complete

1. **Quick verification:** `weirwood acok` shows all 70
2. **Update worklog:** Cost, duration, quality notes
3. **Hand off:** ASOS and ADWD follow per `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` (ASOS 82 chapters, ADWD 73 chapters, both single-pass v3)
4. **Then Stage 4:** Once all 344 chapters done, stage-4 prose-edge classifier runs (new continue prompt)

---

## Quick Reference — New Feature

The `--delay` and `--chain` flags were added in Session 31:

```bash
# Manual batch-by-batch (old way)
weirwood acok 2 1
# wait 2h manually
weirwood acok 2 1
# repeat...

# Auto-advance (new way)
weirwood acok 2 1 --delay 2h --chain
# runs all batches automatically with 2h waits
```

Spreads token usage across 5 API windows instead of hammering one session.
