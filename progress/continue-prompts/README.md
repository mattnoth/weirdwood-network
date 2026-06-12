# Continue-Prompts Triage Manifest

**Generated:** 2026-06-11 (after S91)  
**Rule:** `worklog.md` is the authoritative state file. When a prompt's claims contradict it, the prompt is marked STALE or DONE — the prompt's *content* is left unchanged per the hard rule above.  
**Status vocabulary:** LIVE | DONE | STALE-superseded-by-\<what\> | MERGED-into-worklog | HALTED-gated-on-\<what\>

---

## Active Prompts (sorted: LIVE → HALTED → STALE → DONE)

| Filename | Date | Track | Status | Recommended Model | Note |
|----------|------|-------|--------|-------------------|------|
| `2026-06-12-graph-cleanup.md` | 2026-06-12 | Graph cleanup — hub-triage FIX-22 + Plate-5 followups | **GATED** | Sonnet 4.6 | Runs after infobox merge ships (edges.jsonl ≈ 21,766 + wiki-infobox rows) AND after Matt approves curation files; 9-step work plan, ~30–45 rows touched |
| `2026-06-12-infobox-merge-ship.md` | 2026-06-12 | Infobox merge — apply to graph/ | **LIVE** | Sonnet 4.6 | Spec/script/dry-run all done (S92); Step 0 = Matt reviews dry-run report + 11 YOUR-DECISIONS items before launch |
| `2026-06-12-deferred-structural-restructures.md` | 2026-06-12 | Rename / restructure (Wyman + Jaime arcs) | **LIVE** | Opus 4.7 | Next queued session per S91; subagent decision packets reproduced in-prompt |
| `2026-06-11-phase2-mode3-dip.md` | 2026-06-11 | Graph validation Mode 3 | **LIVE — RE-SEQUENCED** | Opus 4.7 | Unblocked but Matt decided today it runs *after* infobox-merge track lands; see `working/reply-to-audit-session-2026-06-11.md` |
| `2026-06-07-repo-audit-strategy-reconciliation.md` | 2026-06-07 | Repo hygiene + memory consolidation | **DONE (S92)** — file kept per Matt's keep-everything rule | Opus 4.7 | Fable audit session executed the doc/strategy items; reorg plan delivered at `working/repo-reorg-plan-2026-06-12.md`; only the optional `consolidate-memory` skill run remains (fold into a future session) |
| `2026-06-05-edge-modeling-plate-4-haiku-disposition.md` | 2026-06-05 | Post-Plate-5 backfill Track B (1,617 Haiku bulk re-bucketing) | **LIVE** | Opus (review) / Sonnet (filter pass) | Explicitly KEPT in S88 + re-linked in todos.md; queued under post-Plate-5 backfill Track B |
| `2026-05-31-events-v2-promotion-chain/` (folder) | 2026-05-31 | Events v2 promotion (7-step chain) | **HALTED-gated-on-Matt's-escalation-pick** | See per-step files | Chain halted at step 1 (S81 NO-GO); step-01-status.md documents the verdict; absorbed into backfill Track B under edge-modeling reification lens |
| `2026-06-01-events-bulk-escalation-pick.md` | 2026-06-01 | Events Haiku bulk escalation decision | **STALE-superseded-by-backfill-Track-B** | Opus 4.7 / Sonnet 4.6 | Reframed per todos.md — no longer a free-choice menu; the 5 path descriptions remain reference-only |
| `2026-06-08-alias-and-display-design.md` | 2026-06-08 | Post-Plate-5 backfill design (Track A/B/C vocab-drift + reification) | **STALE — not a continue prompt** | n/a | File is a raw agent chat export (no YAML frontmatter, no task structure); the design it captured was formalized in `working/edge-modeling/post-plate5-backfill-design.md`. Should be deleted or renamed to a `working/` doc. |
| `2026-05-26-stage4-events-enrichment.md` | 2026-05-26 | Events enrichment (precision-gated) | **STALE-superseded-by-plate4-haiku-disposition** | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 | Status block at top of file already flags S76 in-progress state; worklog confirms Events bulk ran (S79-S80), drifted (S81 NO-GO), and is now framed as backfill Track B — this prompt predates that pivot |
| `2026-05-23-stage4-pass1-finishing.md` | 2026-05-23 | Stage 4 tail cleanup + resolver levers + merge | **STALE-superseded-by-edges-v1.3** | Sonnet 4.6 / Opus 4.7 | Describes edges "un-merged"; worklog confirms edges v1.3 shipped (S72-S74, 3,811 edges). Resolver levers absorbed into the v1.3 commit. |
| `2026-05-16-stage4-bulk-resume.md` | 2026-05-16 | Stage 4 v1 bulk run (wiki-comention) | **STALE-superseded-by-pass1-derived-pivot** | Sonnet 4.6 | Wiki-comention DEPRECATED (S65); this prompt targets the old comention approach |
| `2026-05-17-stage4-bulk-watcher.md` | 2026-05-17 | Stage 4 v1 bulk watcher | **STALE-superseded-by-pass1-derived-pivot** | Sonnet 4.6 | Same track as above; comention apparatus superseded |
| `2026-05-02-stage4-v1-prose-edge-classifier.md` | 2026-05-02 | Stage 4 v1 prose-edge classifier (comention) | **STALE-superseded-by-pass1-derived-pivot** | Sonnet 4.6 / Haiku 4.5 | Original comention approach; pivoted S65 |
| `2026-05-05-dialogue-meals-mention-index-design.md` | 2026-05-05 | Dialogue + meals + mention-index pass design | **STALE** | Sonnet | Design framing predates Stage 4 pivot + edge-modeling reification; Dialogue is deferred to v2.1 and now must fold in Plate 1 head rule + reification lessons per todos.md |

---

## Archive (`archive/` subfolder — 16 files)

All archive files are **DONE** or **STALE-superseded**. Summary:

| Group | Files | Status |
|-------|-------|--------|
| Wiki Pass 2 Stage 1-3 prompts (2026-04-26 to 2026-04-27) | 6 files | DONE — wiki Pass 2 Stages 1-3 shipped (Sessions 20-27; 7,563+ nodes) |
| Tier 3 Pass E Phase 2 (2026-05-01) | 1 file | DONE — Path B promotion campaign complete (S28) |
| Pass 1 remaining books (2026-05-02 to 2026-05-04) | 4 files | DONE — all 5 books 344/344 (S30-S36) |
| Bug fix: chain/race bug (2026-05-04) | 1 file | DONE — extraction pipeline bugs fixed (S33) |
| Post-Pass-1 cleanup + direction (2026-05-06) | 1 file | DONE — cleanup executed; Stage 4 direction set |
| Missing-node backfill / wiki prose backfill (2026-05-12) | 2 files | DONE — node layer confirmed whole (S72 false-alarm resolution) |
| Events Haiku bulk monitor (2026-05-27) | 1 file | DONE — bulk run complete (S80); monitor no longer needed |

---

## Open threads right now (LIVE, recommended execution order)

1. **`2026-06-12-infobox-merge-ship.md`** (Sonnet 4.6) — FIRST: Matt reviews `working/infobox-merge/dry-run-report-2026-06-12.md` + records decisions; then launch apply. Short + deterministic. Unblocks Mode 3.
1a. **`2026-06-12-graph-cleanup.md`** (Sonnet 4.6) — **GATED**: runs only after infobox merge ships + Matt approves curation files. FIX-22 hub-triage + Plate-5 small followups. ~30–45 rows. 9 steps.
2. **`2026-06-12-deferred-structural-restructures.md`** (Opus 4.7) — apply Wyman-execution arc + Jaime-sheathes arc restructures from S91 subagent decision packets. Parallel-safe with #1.
3. **`2026-06-11-phase2-mode3-dip.md`** (Opus 4.7) — light Mode 3 grounded-agent dip. Runs *after* infobox-merge track lands.
4. **`2026-06-05-edge-modeling-plate-4-haiku-disposition.md`** (Opus) — Haiku bulk re-bucketing under reify lens; post-Plate-5 backfill Track B. Lower priority; can run any time after Mode 3.
5. ~~`2026-06-07-repo-audit-strategy-reconciliation.md`~~ — DONE S92 (reorg plan at `working/repo-reorg-plan-2026-06-12.md`); only the optional memory-consolidation skill run remains.
