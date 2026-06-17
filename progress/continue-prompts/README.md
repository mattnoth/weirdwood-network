# Continue-Prompts Triage Manifest

**Generated:** 2026-06-17 (refreshed after S104)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene policy (FIRM — Matt, recurring: "two continue prompts is confusing"):** the live dir holds the **ONE actionable next track** — not a menu. DONE/STALE prompts AND parked tracks (gated-on-Matt or lower-priority backlog) all `git mv` to `archive/` (kept, organized, recoverable). A parked track's context lives in `worklog.md` / `working/todos.md`; restore its prompt from `archive/` when it becomes the next thing. Never present multiple co-equal "next" prompts at session close.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-17-causal-edges-and-spark-nodes.md` | 2026-06-17 | Causal edges + Rebellion spark-node minting | **LIVE** | Sonnet 4.6 + subagent verify | Continuation of next-move #2 (decisions #1 PRECEDES + #2 causal pilot both DONE S104). Phase 1: mint 3 missing Robert's Rebellion spark-beat nodes (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) from local sources → index/alias rebuild. Phase 2: wire the full chain as `TRIGGERS`. **Verification gate: fresh subagents vs LOCAL cache, Matt gates at policy level** (Matt S104). |

---

## Archive (`archive/` subfolder — 31 files)

Archive files are **DONE**, **STALE-superseded**, or **PARKED** (gated/backlog — recoverable; restore when next). Summary:

| Group | Files | Status |
|-------|-------|--------|
| `2026-06-16-next-move-decisions.md` | 1 file | **DONE S104** — both remaining decisions resolved: #1 `PRECEDES` ordering edges SHIPPED (174); #2 causal pilot SHIPPED (2 `CAUSES` edges). Superseded by the causal-edges+spark-nodes live track. |
| `2026-06-15-arc-wave1-mint.md` | 1 file | **PARKED S99** — gated on Matt's 3 decisions (RW-4 role edges / arc boundaries / RECIPIENT_IN vocab). Drafts+review done. Restore when Matt decides. Context: worklog S95/S97 + `curation/narrative-arc-wave1-*-draft-2026-06-14.md`. |
| `2026-06-05-edge-modeling-plate-4-haiku-disposition.md` | 1 file | **PARKED S99** — post-Plate-5 backfill Track B (1,617 Haiku bulk re-bucketing); lower-priority backlog, de-prioritized by S96 dip. Context: `working/todos.md` Track B. |
| `2026-06-15-historical-anchor-wave2.md` | 1 file | **DONE S100** — wave 2 shipped: 4 WO5K hubs attached (siege-of-riverrun/battle-of-the-camps/battle-of-oxcross/melee-at-bitterbridge), +43 edges (21,950→21,993), validated + minted. `siege-of-storms-end` deferred (dup cluster). Wave 3 (deep-lore wiki-only) optional/low. |
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

## Open thread right now (ONE live track)

**LIVE: `2026-06-17-causal-edges-and-spark-nodes.md`** — continuation of next-move decision #2 (both #1
`PRECEDES` and #2 causal pilot shipped S104). **Phase 1:** mint the 3 missing Robert's Rebellion spark-beat
nodes (`abduction-of-lyanna`, `execution-of-brandon-and-rickard-stark`, `aerys-demands-ned-and-robert`) from
LOCAL-source evidence → rebuild indexes/alias-resolver (node ADD). **Phase 2:** wire the full causal chain as
`TRIGGERS` at beat granularity, then scale to other historical hubs (dip-driven). **Verification gate (Matt
S104, FIRM):** fresh subagents confirm/refute edges + nodes against the LOCAL wiki/book cache; Matt gates at
policy level, gets summaries, not per-edge review. This is narrative-arc reification on a historical arc.

*Parked in `archive/` (restore when next, not deleted): arc-wave1-mint (gated on Matt's 3 decisions), edge-modeling-plate-4 Track B (backlog).*
*Done & archived (no longer live): next-move-decisions (S104), Track 3 dating leftovers (S102), historical-anchor #9 wave 2 (S100), script-consolidation S1+S2 (S98/S99), Mode 3 dip + graph-cleanup (S96), infobox-merge-ship (S94).*
