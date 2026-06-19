# Continue-Prompts Triage Manifest

**Generated:** 2026-06-19 (refreshed after S107)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

> **Hygiene policy (FIRM — Matt, recurring: "two continue prompts is confusing"):** the live dir holds the **ONE actionable next track** — not a menu. DONE/STALE prompts AND parked tracks (gated-on-Matt or lower-priority backlog) all `git mv` to `archive/` (kept, organized, recoverable). A parked track's context lives in `worklog.md` / `working/todos.md`; restore its prompt from `archive/` when it becomes the next thing. Never present multiple co-equal "next" prompts at session close.

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-18-causal-arc-execution.md` | 2026-06-18 (rewritten S107) | Causal-arc execution: B3 (Ned's downfall), then re-dip | **LIVE** | Sonnet 4.6 | S107: dip ran (5/10; all prior arcs validated) → minted B1 (Red-Wedding-upstream) + B2 (Greyjoy→Theon-ward), both fresh-subagent verified; post-build re-dip 6/10, Q7 confirmed fixed. **Next action = build B3 (Ned's-downfall arc, the Q10 gap: discovery→Littlefinger betrayal→arrest→execution), then re-dip.** Spec: `working/causal-arc-strategy-2026-06-18.md`; dips: `working/session-results/2026-06-19-arc-weighted-{dip,redip}.md`; terms: `reference/narrative-arc-glossary.md`. |

---

## Archive (`archive/` subfolder — 32 files)

Archive files are **DONE**, **STALE-superseded**, or **PARKED** (gated/backlog — recoverable; restore when next). Summary:

| Group | Files | Status |
|-------|-------|--------|
| `2026-06-17-causal-edges-and-spark-nodes.md` | 1 file | **DONE S105** — pure-analysis strategy delivered (`working/causal-arc-strategy-2026-06-18.md`) + second smoke-test arc (Bran's fall) built + 4-lens advisory board run. Superseded by the causal-arc-execution live track. |
| `2026-06-16-next-move-decisions.md` | 1 file | **DONE S104** — both remaining decisions resolved: #1 `PRECEDES` ordering edges SHIPPED (174); #2 causal pilot SHIPPED (2 `CAUSES` edges). Superseded by the causal-edges+spark-nodes live track. |
| `2026-06-15-arc-wave1-mint.md` | 1 file | **STALE-superseded-by-chain-as-arc (S106)** — its `event.conspiracy` umbrella-parent model is reversed by the S105/S106 chain-as-arc decision (arcs = causal chains queried via `--causal-chain`, NO parent hubs). Kept for historical reference only; do NOT restore as-is. The Red-Wedding/Joffrey arcs it drafted are now candidates for the chain-as-arc machine. (Prompt body unchanged per the manifest hard rule; staleness tracked here.) See memory `project_narrative_arc_reification`. |
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

**LIVE: `2026-06-18-causal-arc-execution.md`** — chain-as-arc ratified (S106); the `--causal-chain` primitive +
the two Tier-A arcs (Sack of KL, Purple Wedding) are SHIPPED and fresh-subagent-verified. **Next action = run an
arc-weighted Mode-3 dip BEFORE any Tier-B minting** (Catelyn-frees-Jaime→Red-Wedding-feed; Greyjoy→Theon-hostage→
Northern-invasion). Dip-driven, not mass-mint: the dip's fumbles re-rank Tier B. Reuse the proven mint machine
(research subagent → trim+mint script → index/alias rebuild → fresh-subagent verify → `--causal-chain` smoke).
Spec: `working/causal-arc-strategy-2026-06-18.md`; terms: `reference/narrative-arc-glossary.md`.

*Parked/stale in `archive/` (recoverable, not deleted): arc-wave1-mint (**STALE — parent-hub model superseded by chain-as-arc**; its drafted Red-Wedding/Joffrey arcs are candidates for the chain machine), edge-modeling-plate-4 Track B (backlog).*
*Done & archived (no longer live): causal-edges-and-spark-nodes strategy (S105), next-move-decisions (S104), Track 3 dating leftovers (S102), historical-anchor #9 wave 2 (S100), script-consolidation S1+S2 (S98/S99), Mode 3 dip + graph-cleanup (S96), infobox-merge-ship (S94).*
