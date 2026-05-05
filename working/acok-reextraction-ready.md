# ACOK Re-extraction — Ready to Launch

**Date:** 2026-05-04  
**Status:** Pre-flight complete, cleanup done, ready to run

## Current State
- ✅ 20 ACOK chapters FINAL v3 in `extractions/mechanical/acok/` (locked)
- ✅ 50 ACOK chapters archived in `extractions/archives/acok-v2-original-2026-05-04/` (ready for re-extraction)
- ✅ Failed attempt files deleted (acok-arya-01, acok-arya-06)
- ✅ mechanical-extractor agent confirmed v3 prompt

## Exact Command to Run

Open iTerm and paste:

```
weirwood acok 2 1 claude-opus-4-6 --delay 2h --chain
```

### What This Does
- **2 terminals** × 1 wave each = 10 chapters per batch
- **Opus model** (required for AGOT v3 consistency)
- **--delay 2h** auto-advance: waits 2h, launches next batch
- **--chain** continues until all 50 chapters complete
- **Total:** ~10 hours wall-clock, 50 chapters, all v3 schema

## Notes
- No preflight checks needed
- Archive reads auto from weirwood context
- All outputs go to `extractions/mechanical/acok/` with v3 schema
