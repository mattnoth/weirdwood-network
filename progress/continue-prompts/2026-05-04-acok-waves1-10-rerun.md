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

## Current State — Status Confirmed ✅

**ACOK Extraction Status (confirmed in Session 32):**
- **20/70 chapters FINAL:** Waves 11-14 (chapters 51-70) already extracted with v3 schema — locked, do not re-extract
- **50/70 chapters archived:** Waves 1-10 (chapters 1-50) in `extractions/archives/acok-v2-original-2026-05-04/` — need re-extraction with v3 schema
- **Mechanical-extractor agent confirmed using v3 (12-category) prompt** — no schema drift, canonical format

No pre-flight checks needed. Ready to launch.

---

## No Smoke Test — Ready for Full Run ✅

**Why skip the smoke test?**
- v3 prompt is confirmed canonical and working (AGOT proved it, 20 ACOK chapters confirmed it)
- Schema verified: 12 categories, all required sections (Food & Drink, Hospitality, Physical Environment, etc.)
- Matt confirmed: "as long as we are using the 12 cat, we are good to just start it"
- Session 32 attempted smoke test but Opus model is slow (one wave taking 20+ min) — better to use auto-advance for full run

---

## Launch Full Auto-Advance Run (Session 33+)

**Single command to run (fresh session):**
```bash
weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain
```

**Opus is required.** AGOT v3 used Opus for consistency and quality. ACOK must match. Do not substitute Sonnet or Haiku.

**What this does:**
- Waves 1-2 run in parallel (2 terminals, Opus model)
- When done, waits 2 hours
- Auto-launches waves 3-4
- Waits 2 hours, then 5-6
- Continues: 7-8, wait 2h, 9-10
- **Total:** ~10 hours wall-clock across ~5 batches, 50 chapters, v3 schema, Opus quality

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
