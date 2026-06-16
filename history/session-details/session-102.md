---
session: 102
date: 2026-06-16
model: Opus 4.8 (1M context) orchestrator + 4 Sonnet 4.6 general-purpose advisors
title: "Advisory board → Track 3 dating-leftovers cleanup"
commit: (this endsession commit)
---

# Session 102 — Advisory board picks Track 3; dating leftovers finished

## Purpose

S101 left **4 next-move decisions** for Matt (`working/next-move-decisions-2026-06-16.md`):
(1) PRECEDES/FOLLOWS ordering edges, (2) causal TRIGGERS, (3) dating-pass leftovers,
(4) Fable cleanup. The session opened (via `/continue next-move-decisions`) by putting the 4
to Matt. Rather than pick directly, Matt chose: **"fan out an advisory board re: immediate
direction, compare recs, top rec wins."**

## The advisory board (novel orchestration pattern)

Four independent advisors (parallel `general-purpose` subagents), each grounded in the same
project state but reasoning through a **distinct lens** so the comparison was real:

| Advisor lens | Winner | Key note |
|---|---|---|
| Query-value (the real goal) | **#2 Causal TRIGGERS** | …but "do the cheap #3 year-node fix first" |
| Cost/risk/ROI | **#3 Dating leftovers** | dominant ROI; de-risks #1 |
| Schema integrity | **#3 Dating leftovers** | retires live schema debt; TRIGGERS needs NO vocab add |
| Curatorial debt | **#3 Dating leftovers** | the canonical finisher |

**Top rec → Track 3** (3 of 4; the dissenter still wanted #3's year-node fix done first).
The board also produced a **sequencing roadmap** all four broadly endorsed:
**#3 now → #1 ordering → #2 causal pilot → #4 Fable.**

Two cross-cutting findings the board surfaced and I acted on:
- **`TRIGGERS` is already in the locked vocab** (architecture.md:410) — track #2, when it comes,
  needs no vocab add; it's curatorial-only. (`PRECEDES`/`FOLLOWS` are absent → #1 *does* need a vocab add.)
- **The vocab-count test was stale**: `assertEqual(len(vocab), 163)` but the real documented count
  is **166** (the +3 are reification edges AGENT_IN/VICTIM_IN/SUB_BEAT_OF, S82–S87). This was 2 of the
  3 "documented pytest fails" — a drift-detector red-by-default, masking real state.

## Track 3 — what shipped (deterministic, $0, additive/reversible)

All four sub-items resolved against data, not guesswork:

1. **`conquest-of-dorne` — verified, no change.** The dated `event.battle` node carries `ac_year: 161`;
   the in-world book is a separate `texts/the-conquest-of-dorne` node. Date is on the event. ✓
2. **5 multi-year spans — dated as ranges** using the existing `ac_year_end` field (validator already
   supported it; architecture.md:468 had them staged as "5 multi-year hubs for review"):
   `dance-of-the-dragons` 129→132, `war-of-the-five-kings` 298→300, `greyjoy-rebellion` 289→290,
   `regency-of-aegon-iii` 131→136. `first-blackfyre-rebellion` resolved to single-year **196**
   (the chronology data's **212** was dropped as a wiki cross-link error — Redgrass Field was 196 AC).
3. **`long-night`** — `ac_year: null` / `precision: relative-only` (matching architecture.md:476's own
   Long Night example, NOT the next-move doc's looser `era`). The wiki mention-index's spurious **297 AC**
   link recorded in a `note:` field and excluded.
4. **10 mistyped year-page nodes deleted** (Matt's call). All were `character.human`, 0 edges, boilerplate
   "X is a character from the AWOIAF wiki" — auto-mis-promoted wiki year-pages. Aligns with the
   `chronology-extractor` design note ("year pages may not become graph nodes themselves"). In-world
   year-lookup is now served by `occurred.ac_year` on event nodes. Source JSON in `sources/wiki/_raw/`
   untouched. `characters/_summary.json` metric `year_pages_emitted_as_characters: 10 → 0`.

**Vocab-count test reconciled 163 → 166** (both `tests/test_stage4_tail_classifier.py` and
`tests/test_validate_edge_jsonl.py`), with the baseline history in the comments. Restores the
drift-detector as a live tripwire.

## Operational lesson — `weirwood refresh` timestamp churn

After deleting 10 nodes I ran `scripts/weirwood-refresh.sh` (per the rebuild-derived-artifacts rule).
It re-stamped `generated_at` on **every** index file → **7,922 timestamp-only diffs** that would have
buried the 16 real changes. Investigation showed only `characters/_summary.json` (and
`all-node-alias-lookup.json`, which correctly dropped the 10 year slugs) had real content changes.

**Fix applied:** reverted the 7,921 timestamp-only per-node index files + the other summaries; kept
`characters/_summary.json` (real resync) + `all-node-alias-lookup.json` (real) + 2 new index files for
prior-session nodes the refresh newly surfaced. Final staged diff: **22 files, +25/−439.**

**Lesson for next time:** the 10 deleted year nodes had **0 edges**, so a full refresh was overkill —
only their own 10 index files needed removing. Prefer targeted index-file deletion over a full
`weirwood refresh` when the mutated nodes are edgeless. If a full refresh is run, expect to revert
timestamp-only churn before committing. (Candidate fix logged in todos: make `weirwood refresh` skip
re-stamping `generated_at` when content is byte-identical.)

## Verification

- `283-ac` (and all 10) no longer resolve as nodes or aliases.
- Event nodes with `occurred:` blocks: **112 → 118**.
- `--health`: **8,518 nodes / 21,993 edges / 62 orphans** (−10 nodes, edges untouched).
- pytest: **1297 passed, 1 failed** — the lone fail is the environmental `cwd-is-tmp` test
  (pre-existing, requires cwd=/tmp). The two vocab fails are now green. Net: 3 documented fails → 1.

## What's next

Track 3 is complete. Per the board roadmap, the remaining decisions are **#1 PRECEDES/FOLLOWS**
(needs Matt's vocab-add OK + grouping basis — note 0 dated events share a `PART_OF` parent),
**#2 causal TRIGGERS pilot** (no vocab add; needs sign-off on the Robert's Rebellion pilot), and
**#4 Fable cleanup** (scheme pick + repo-reorg). Live continue prompt updated to carry the remaining 3.
