---
title: Session 32 Handoff — ACOK Ready to Launch
date: 2026-05-04
model: haiku
focus: verification + handoff
---

# Session 32 Handoff

## What Was Done

**Session 31** built the auto-advance feature (`--delay` + `--chain` flags). **Session 32** verified the v3 prompt status and confirmed ACOK is ready for re-extraction.

## Status — CONFIRMED ✅

- **20 ACOK chapters (waves 11-14):** FINAL with v3 schema — locked, do not re-extract
- **50 ACOK chapters (waves 1-10):** Archived in `extractions/archives/acok-v2-original-2026-05-04/` — ready for v3 re-extraction
- **Mechanical-extractor agent:** Confirmed using v3 canonical prompt (12-category Raw Entity List + all v3 sections)
- **Model:** Opus (required for consistency with AGOT v3)

## Next Step — Session 33+ (Fresh Session)

Open a new iTerm session and run this single command:

```bash
weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain
```

**What this does:**
- Launches 2 terminals, 1 wave each (10 chapters total = 5 per terminal)
- Opus model extracts with v3 schema
- After completing, waits 2 hours, then auto-launches next batch
- Repeats: waves 1-2, wait, 3-4, wait, 5-6, wait, 7-8, wait, 9-10
- Total: ~10 hours wall-clock across ~5 batches, 50 chapters, all v3 schema

**No preflight checks needed.** State already verified.

## Important Rules

- ✅ Use **Opus model only** (not Sonnet/Haiku) — consistency with AGOT v3
- ✅ Use **12-category v3 schema** (confirmed in agent definition)
- ✅ **Do not delete archives** — `acok-v2/` and `acok-v2-original-2026-05-04/` stay forever
- ✅ New extractions land in **`extractions/mechanical/acok/`** (canonical location), never in archive folders
- ❌ **Never run /endsession without explicit permission** (this rule has been violated)

## After ACOK 70/70 Complete

1. Verify: `weirwood acok` shows 70/70
2. Update worklog with cost/duration
3. Move to ASOS (82 chapters) and ADWD (73 chapters) — both single-pass v3
4. Continue prompt: `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`
5. Once 344/344 all-books complete: Stage 4 v1 prose-edge-classifier

## Files Updated This Session

- `progress/continue-prompts/2026-05-04-acok-waves1-10-rerun.md` — state clarified, ready-to-launch version
- `worklog.md` — Session 32 entry + Current State updated
- This file: `progress/SESSION-32-HANDOFF.md`

---

**Ready.** Fresh session, single command. Go.
