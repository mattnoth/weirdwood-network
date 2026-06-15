# Continue-Prompts Triage Manifest

**Generated:** 2026-06-15 (refreshed after S99)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene (S97 2026-06-15):** the live dir now holds ONLY actionable tracks (LIVE + HALTED-gated). All DONE/STALE prompts were `git mv`'d to `archive/` (kept, organized — per Matt's "archive, don't delete"). Per `/endsession` step 3, this is the standing discipline going forward.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-15-historical-anchor-wave2.md` | 2026-06-15 | Historical-anchor #9 wave 2 | **LIVE — TOP OF QUEUE** | Sonnet 4.6 | Wave 1 shipped S97 (+121 edges, 8 hubs); wave 2 = remaining main-saga-recalled historical hubs; tooling `scripts/historical-anchor-*.py` |
| `2026-06-15-arc-wave1-mint.md` | 2026-06-14 | Narrative-arc wave 1 mint (Red Wedding + Joffrey) | **HALTED-gated-on-Matt's-3-decisions** | Sonnet 4.6 | Drafts+review done; gated on RW-4 role edges / arc boundaries / RECIPIENT_IN vocab. De-prioritized by S96 dip |
| `2026-06-05-edge-modeling-plate-4-haiku-disposition.md` | 2026-06-05 | Post-Plate-5 backfill Track B (1,617 Haiku bulk re-bucketing) | **LIVE** | Opus (review) / Sonnet (filter) | Explicitly KEPT in S88 + re-linked in todos.md; queued under post-Plate-5 backfill Track B |

---

## Archive (`archive/` subfolder — 27 files)

All archive files are **DONE** or **STALE-superseded**. Summary:

| Group | Files | Status |
|-------|-------|--------|
| `2026-06-15-script-consolidation.md` | 1 file | **DONE S99** — Session 1 (pacer/orchestration) S98 + Session 2 (archive 30 one-offs/wrappers, `weirwood graph/resolve/refresh` aliasing, README universal-index refresh, design §0 fully BUILT) S99. |
| Stage-4 comention + events + design prompts (2026-05-02 → 2026-06-08) | 10 files | Archived S97 — DONE/STALE (comention deprecated S65; events absorbed into Track B; repo-audit done S92; alias-and-display was a chat export). Incl. the `2026-05-31-events-v2-promotion-chain/` folder. |
| Wiki Pass 2 Stage 1-3 prompts (2026-04-26 to 2026-04-27) | 6 files | DONE — wiki Pass 2 Stages 1-3 shipped (Sessions 20-27; 7,563+ nodes) |
| Tier 3 Pass E Phase 2 (2026-05-01) | 1 file | DONE — Path B promotion campaign complete (S28) |
| Pass 1 remaining books (2026-05-02 to 2026-05-04) | 4 files | DONE — all 5 books 344/344 (S30-S36) |
| Bug fix: chain/race bug (2026-05-04) | 1 file | DONE — extraction pipeline bugs fixed (S33) |
| Post-Pass-1 cleanup + direction (2026-05-06) | 1 file | DONE — cleanup executed; Stage 4 direction set |
| Missing-node backfill / wiki prose backfill (2026-05-12) | 2 files | DONE — node layer confirmed whole (S72 false-alarm resolution) |
| Events Haiku bulk monitor (2026-05-27) | 1 file | DONE — bulk run complete (S80); monitor no longer needed |

---

## Open threads right now (LIVE, recommended execution order)

1. **`2026-06-15-historical-anchor-wave2.md`** (Sonnet 4.6) — **TOP OF QUEUE.** historical-anchor #9 wave 2 (remaining main-saga-recalled hubs); wave 1 shipped S97 (+121 edges).
2. **`2026-06-15-arc-wave1-mint.md`** (Sonnet 4.6) — **HALTED**, gated on Matt's 3 decisions (RW-4 role edges / arc boundaries / RECIPIENT_IN vocab). De-prioritized by S96 dip.
3. **`2026-06-05-edge-modeling-plate-4-haiku-disposition.md`** (Opus review / Sonnet filter) — Haiku bulk re-bucketing; post-Plate-5 backfill Track B. Lower priority.

*Done & archived (no longer live): script-consolidation S1+S2 (S98/S99), Mode 3 dip + graph-cleanup (S96), infobox-merge-ship (S94), deferred-structural-restructures (S93), repo-audit-reconciliation (S92).*
