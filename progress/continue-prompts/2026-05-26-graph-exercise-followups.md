# Graph-exercise follow-ups — conflict-pair audit + reusable query tool

> **Recommended model:** **Sonnet 4.6** for both $0 deterministic builds (delegate to script-builder).
> **Opus 4.7** only to review the conflict-pair audit output / decide cleanup policy. Never per-row.
>
> **Trust `worklog.md` over this prompt if they disagree** (CLAUDE.md #9). Authoritative state:
> worklog Session 74 + the "Graph edges formalized" Current-State line + the Session-74 Active Decision.

## State (end of Session 74, 2026-05-26)

- **The deterministic core is SHIPPED:** `graph/edges/edges.jsonl` = **3,811** cited edges (v1.3), committed `63b8b461a`. Citations re-grounded this session (`scripts/stage4-reground-core-citations.py`) — `evidence_ref` line numbers now correct; quote text + edge set untouched.
- **Enrichment is SHELVED (NO-GO).** Do NOT run the ~$75 Events+Dialogue Haiku enrichment. Post-locator-fix out-of-sample smokes were 74.5% / 62.5% strict (unstable, <75% gate). The v5 precision rules (`prompt_version=v5-precision-rules` in `scripts/stage4-tail-classifier.py`) are kept for any future revisit but are not being run. See the Session-74 Active Decision in worklog.
- **The graph composes:** 8,297 nodes / 3,811 edges; **100% of 898 edge endpoints resolve to a node, 0 orphans, fully traversable** (exact-slug).

## Why these follow-ups (from exercising the graph in S74)

Walking a Cersei↔Tyrion query surfaced two things:
1. **Mis-typed edges cluster on conflicting-type pairs.** The same pair carries contradictory types (e.g. `cersei LOVES tyrion` + `cersei HATES tyrion`; `cersei ALLIES_WITH tyrion` is really grudging submission). With the citations now navigable, these are individually adjudicable — but there's no tool to *find* them in bulk.
2. **There is no query interface.** The traversal was an ad-hoc inline Python script.

## Task 1 — Conflict-pair audit ($0, NO LLM) — HIGHEST VALUE

Build `scripts/graph-conflict-pairs.py` (read-only over `graph/edges/edges.jsonl`):
- For every unordered entity pair, collect all edge types in both directions.
- Flag pairs carrying **semantically incompatible** types. Start with a small, defensible incompatibility set (extend cautiously — ASOIAF relationships are genuinely complex, so do NOT over-flag): `LOVES`×`HATES`, `ALLIES_WITH`×`OPPOSES`, `TRUSTS`×`DISTRUSTS`, `PROTECTS`×`ATTACKS`/`ASSAULTS`. (Sentiment can legitimately coexist across 5 books — so this is a *review queue*, not an auto-delete. The point is to concentrate the ~22% mis-types into a human/Opus-reviewable list with the `evidence_ref` for each conflicting edge.)
- Output `working/wiki/data/graph-conflict-pairs.md` (or `.jsonl`): each flagged pair + the conflicting edges + their `evidence_ref` + `evidence_quote` so a reviewer can click straight to the line.
- Tests in `tests/` (load via `tests/_helpers.py:load_script`). Report flagged-pair count + a sample.
- This is the precision-cleanup lever for the shipped core. Do NOT modify `edges.jsonl` — produce the queue only; Matt/Opus decides corrections.

## Task 2 — Reusable graph query tool ($0, NO LLM)

Formalize the S74 ad-hoc traversal into `scripts/graph-query.py` (read-only):
- Resolve an entity name/slug → node (check `graph/nodes/**/*.node.md`).
- `--neighbors <slug>`: incoming + outgoing edges grouped by type.
- `--path <slugA> <slugB>`: direct edges + 2-hop bridges (common neighbors) with the edge type on each leg.
- `--health`: node/edge counts, edge-type distribution, orphan-endpoint audit (the 0-orphan check), degree leaders.
- Tests + a couple of worked examples in the report. This is the graph's first query interface (was a MEDIUM backlog item).

## Deferred (NOT this session unless Matt asks)
- **Edge temporal scoping** — edges have no chapter/timeline ordering, so contradictory-but-individually-valid edges coexist. A real fix (per-edge chapter anchor → relationship-phase queries) is a larger design item.
- **SIBLING_OF-class weak evidence** — structural facts (SIBLING_OF/PARENT_OF) sometimes have generic name-match quotes because the relationship isn't stated in one sentence. Acceptable for now.
- **S67 resolver levers** (full-surname rung, index-pollution filter) — `progress/continue-prompts/2026-05-23-stage4-pass1-finishing.md`. Lower priority now that core is shipped.

## DO NOT
- Run the ~$75 Events+Dialogue enrichment (SHELVED — see Active Decision).
- Modify `graph/edges/edges.jsonl` from the conflict-pair audit (produce the review queue only; show Matt before/after for any correction).
- Delete anything. Run `/endsession` without explicit permission.

## Final step
Write `working/session-results/<date>-graph-followups.md` (status + headline numbers + what's next) and update worklog + todos.
