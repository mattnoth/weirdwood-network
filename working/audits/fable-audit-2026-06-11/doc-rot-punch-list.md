# Doc-Rot Punch List — 2026-06-11

> Actionable extraction of history-audit.md §E. Items 1–7 = Step 1 (doc fixes, this session).
> Items 8–10 = Step 1b (todos.md cleanup, this session). Items 11–12 = recorded, NOT this session.
> Rule for all fixes: correct living docs only; history/ archives and session-details are
> records-of-thought-at-the-time and are NEVER edited.

## Step 1 — CLAUDE.md + worklog.md (mechanical truth fixes)

1. **CLAUDE.md pipeline table.** Step 5 "Pass 2: Wiki Ingestion — Not started — Agent prompt not yet written"
   → actually ran Apr 26–May 1 (855 agent nodes Stage 1 + ~7,000 Python promotions Stages 3/3c/Path B; ~8,261 nodes today).
   Step 6 "Build Index — Not started" → built S38–S44, completed to all 21 categories S72.
   Also: the table has a duplicated header row (formatting bug). Fix all three.
2. **worklog.md Principles #4** — "Spoiler gating is architectural. Every node has `first_available`.
   This is not a feature to add later." Directly contradicts the S24 DEFERRED decision recorded in the same
   file, CLAUDE.md, and memory. Rewrite to reflect the deferral (deterministic backfill post-first-release).
3. **worklog.md Current State — Stage-4 fossil.** The long `[~]` Stage-4 entry still ends
   "**`graph/edges/` still EMPTY** — the FORMALIZE/merge is the milestone" — contradicted ~10 lines below
   (edges v1.3 shipped; Plate 5 at 4,757; S91 at 4,760). Entry is an S69 fossil never rewritten after S70.
4. **worklog.md Current State — unchecked-but-done lines.** `[ ] Pass 2 wiki ingestion agent prompt written` /
   `[ ] Pass 2 wiki ingestion complete` sit unchecked immediately above the `[x]` lines describing
   Pass 2's completed stages. Reconcile.
5. **worklog.md Ideas & Backlog → HIGH** still lists "Write the chapter splitter script" (done S2),
   "Run Pass 1 on AGOT as proof of concept" (done April), "Write Pass 2 wiki ingestion agent prompt" (done S19).
   Groom the whole backlog section (MEDIUM/LOW too — keep genuinely-open items only, with current framing).
6. **worklog.md Infrastructure checklist** says "Subagent definitions (2 full … 5 stubs)" — fleet grew to
   27 agents in S26. Correct.
7. **Numeric drift.** Wiki page count: 17,945 (CLAUDE.md, worklog) vs 17,657 (memory, parser outputs) —
   delta = case-collision/redirect losses; add a one-line explanation wherever both numbers can confuse.
   Index rebuild "+1,847" (worklog) vs "+1,861" (todos) — reconcile or annotate.

**THE REAL TARGET of Step 1 (Matt, verbatim intent):** when done, there must be ONE trustworthy
"where am I" surface — worklog.md Current State — answering at a glance: what's shipped, what's in flight,
what's gated on what, what Matt reviews next. If Current State can't carry it alone, propose the minimal
extra surface (e.g., a short STATUS section) — ONE surface, not another scattered file.

## Step 1b — working/todos.md

8. **Stage-4 section header + items** still frame the Haiku-cutover comention prep as the live track
   ("the run phase is an Opus conductor"); "[ ] STAGE 4 RUN — Opus conductor … scale to the ~1017-queue"
   unchecked though the comention bulk was deprecated S65; "[~] STAGE 4 — PIVOT … (ACTIVE)" itself superseded
   (spine shipped, edges formalized, reification canonical).
9. **Mission Protocol section** carries live-looking items (watcher v2, protocol redline, mission git-tracking,
   next.md reconciliation) untouched since S45–47; `next.md` unmentioned since S52.
10. **Model-fit READY-TO-DO items (S37)** reference applying recommendations to a 27-agent fleet and
    reconciling fleet-orchestration budgets — fleet plan never executed; retired in practice but not on paper.

## Recorded, NOT actioned this session

11. **Graph-internal staleness (no graph writes this session):** renamed Plate-3 mints still carry
    `status: minted-plate3` + "Staging only" body notes though Plate 5 merged them (S91 look-at-twice);
    node-file `## Edges` display bullets are pre-Plate-5 across the whole graph (post-Plate-5 followup #1).
12. **Memory entries:** `project_pass1_prompt_v3_canonical` self-flags as unreliable for state;
    `project_stage4_haiku_not_sonnet` reads as a standing rule but was comention-track-specific —
    reconcile in a future `consolidate-memory` run.

## Data-layer gaps (feed Step 3 spec, not doc fixes)

- 115 orphan endpoint slugs in edges.jsonl (alias mismatches; resolve via alias-resolver).
- 948 reified role edges missing `typed_by` + file:line `evidence_ref` (chapter-label cites only).
- 32 SUB_BEAT_OF rows with empty evidence_quote (existing post-Plate-5 followup #2).
