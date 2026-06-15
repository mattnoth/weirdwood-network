# Continue-Prompts Triage Manifest

**Generated:** 2026-06-11 (after S91)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene (S97 2026-06-15):** the live dir now holds ONLY actionable tracks (LIVE + HALTED-gated). All DONE/STALE prompts were `git mv`'d to `archive/` (kept, organized — per Matt's "archive, don't delete"). Per `/endsession` step 3, this is the standing discipline going forward.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-15-script-consolidation.md` | 2026-06-15 | Orchestration/pacer + script cleanup | **LIVE — TOP OF QUEUE (S97)** | Sonnet 4.6 | TWO sessions: S1 pacer build, S2 cleanup. Spec = `working/orchestration-pacer-design-2026-06-15.md` (§13 must-fixes binding) |
| `2026-06-15-historical-anchor-wave2.md` | 2026-06-15 | Historical-anchor #9 wave 2 | **LIVE** | Sonnet 4.6 | Wave 1 shipped S97 (+121 edges, 8 hubs); wave 2 = remaining main-saga-recalled historical hubs; tooling `scripts/historical-anchor-*.py` |
| `2026-06-15-arc-wave1-mint.md` | 2026-06-14 | Narrative-arc wave 1 mint (Red Wedding + Joffrey) | **HALTED-gated-on-Matt's-3-decisions** | Sonnet 4.6 | Drafts+review done; gated on RW-4 role edges / arc boundaries / RECIPIENT_IN vocab. De-prioritized by S96 dip |
| `2026-06-05-edge-modeling-plate-4-haiku-disposition.md` | 2026-06-05 | Post-Plate-5 backfill Track B (1,617 Haiku bulk re-bucketing) | **LIVE** | Opus (review) / Sonnet (filter) | Explicitly KEPT in S88 + re-linked in todos.md; queued under post-Plate-5 backfill Track B |

---

## Archive (`archive/` subfolder — 26 files)

All archive files are **DONE** or **STALE-superseded**. Summary:

| Group | Files | Status |
|-------|-------|--------|
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

1. **`2026-06-11-phase2-mode3-dip.md`** (Opus 4.7) — top of queue. Gate cleared S94 (2026-06-13) when infobox merge shipped. Light Mode 3 grounded-agent dip on the 21,770-edge merged graph; failure modes drive backfill Track B priorities.
2. **`2026-06-12-graph-cleanup.md`** (Sonnet 4.6) — **PARTIALLY GATED**: infobox merge ✓ shipped; still waits on Matt approving the two curation files. Parallel-safe with #1.
3. **`2026-06-05-edge-modeling-plate-4-haiku-disposition.md`** (Opus) — Haiku bulk re-bucketing under reify lens; post-Plate-5 backfill Track B. Lower priority; can run any time after Mode 3.
4. ~~`2026-06-12-infobox-merge-ship.md`~~ — DONE S94 (2026-06-13); file deleted.
5. ~~`2026-06-12-deferred-structural-restructures.md`~~ — DONE S93 (2026-06-12); file kept pending writeup-confirm.
6. ~~`2026-06-07-repo-audit-strategy-reconciliation.md`~~ — DONE S92 (reorg plan at `working/repo-reorg-plan-2026-06-12.md`); only the optional memory-consolidation skill run remains.
