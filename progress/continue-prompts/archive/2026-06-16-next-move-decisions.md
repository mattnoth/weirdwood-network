# Continue — Next-Move Decisions (OPEN BY ASKING MATT)

> **Recommended model:** Sonnet 4.6 (the work behind each decision is deterministic/curatorial; no heavy reasoning
> until a track is picked). Opus only if Matt picks the causal-`TRIGGERS` track and wants insurance.
>
> **Status (S103, 2026-06-16):** **Track 3 (dating leftovers) DONE S102; Fable nomenclature DONE S103.**
> S103 decided the canonical vocabulary (3 terms — Pass/Track/Tier + lowercase `step`; `reference/glossary.md`)
> and declined the full doc-sweep as churn. **2 decisions remain, both Matt's** (board order #1 → #2). This
> session's FIRST action: present the 2 and ask Matt what he wants to answer on each, then execute his pick.

## STEP 1 — open by asking Matt (do this before any work)
Read `working/next-move-decisions-2026-06-16.md` (the full talking points; #3 dating + Fable-nomenclature struck/done).
Put the 2 remaining decisions to Matt, asking what he needs to resolve on each. Summarize each in 1–2 lines;
do not start executing until he answers.

1. **`PRECEDES`/`FOLLOWS` ordering edges** — GATED on two of Matt's calls: (a) approve adding `PRECEDES`/`FOLLOWS`
   (and maybe `OCCURRED_IN_YEAR`) to the locked edge vocab in `reference/architecture.md` — **these are currently
   ABSENT from the vocab** (verified S102); the vocab-count test is now at **166** (reconciled S102), so a vocab
   add must bump that assertion too; (b) pick the grouping basis — the 118 dated events are NOT `PART_OF`-clustered,
   so ordering needs a basis (shared war? globally within an `era`? cross-year-only with same-year broken by
   `narrative_first`?). $0 deterministic once decided. (Note: edge-vocab add, unrelated to the now-pinned confidence Tiers.)
2. **Causal `TRIGGERS` / consequence edges** — the dip's MEASURED gap (highest query-value). **`TRIGGERS` is
   ALREADY in the locked vocab (architecture.md:410) — NO vocab add needed** (verified S102). Interpretive →
   pollution-sensitive → needs Matt's sign-off. Recommended pilot: the Robert's Rebellion chain (Harrenhal 281 →
   Trident 283 → Sack 283 → Tower of Joy), which now has participants + dates. Curator-guided, small, review-first.

**Also still open (lower priority, not on the board #1→#2 path):** Fable cleanup's *repo-reorg* half
(`working/repo-reorg-plan-2026-06-12.md` — mostly overtaken by S99/S101 hygiene; small leftovers + a deferred
MATT register remain) + the 2 narrow nomenclature follow-ups in `working/todos.md` (rename live non-confidence
"Tier"→class/level; pull-channel pointer in ~8 live agents).

## STEP 2 — execute whichever Matt picks
Follow the relevant plan/doc. Honor: deterministic-Python-before-LLM; backup `edges.jsonl` before any edge write;
frontmatter-only idempotent node patches; rebuild indexes/alias-resolver only on node ADD/RENAME (and prefer
targeted index-file ops over a full `weirwood refresh`, which re-stamps 7.9k timestamps — S102 lesson);
agents-propose-Matt-decides for anything interpretive (TRIGGERS, ATTENDS).

## Context / source-of-truth
- `working/next-move-decisions-2026-06-16.md` — the talking points in full (#3 struck/done S102).
- `history/session-details/session-102.md` — the advisory-board run + Track 3 results + the index-churn lesson.
- `working/session-results/2026-06-15-mode3-dip-rerun.md` — the measured gaps (causal + ATTENDS).
- `working/design-opinions/2026-06-16-era-field-analysis.md` — the `occurred:` schema + 9-invariant validator.

## Hard rules
- Do NOT `/endsession` without Matt's permission. Do NOT refetch the wiki. Backup before any `edges.jsonl` write.
- Do NOT add edge types to the vocab without Matt's explicit OK (decision #1).
