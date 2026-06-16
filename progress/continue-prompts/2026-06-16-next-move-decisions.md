# Continue — Next-Move Decisions (OPEN BY ASKING MATT)

> **Recommended model:** Sonnet 4.6 (the work behind each decision is deterministic/curatorial; no heavy reasoning
> until a track is picked). Opus only if Matt picks the causal-`TRIGGERS` track and wants insurance.
>
> **Status (S101, 2026-06-16):** event in-world dating + `narrative_first` SHIPPED and committed. The next move is
> NOT pre-decided — there are **4 open decisions, all Matt's.** This session's FIRST action is to present them and
> **ask Matt what he wants to answer on each**, then execute whichever he picks.

## STEP 1 — open by asking Matt (do this before any work)
Read `working/next-move-decisions-2026-06-16.md` (the full talking points) and put the 4 decisions to Matt,
asking what he needs to resolve on each. Summarize each in 1–2 lines; do not start executing until he answers.

1. **`PRECEDES`/`FOLLOWS` ordering edges** — GATED on two of Matt's calls: (a) approve adding `PRECEDES`/`FOLLOWS`
   (and maybe `OCCURRED_IN_YEAR`) to the locked edge vocab in `reference/architecture.md` — NOTE this shifts the
   vocab-count test baseline (3 documented fails reference a 163 count); (b) pick the grouping basis — the 112
   dated events are NOT `PART_OF`-clustered, so ordering needs a basis (shared war? globally within an `era`?
   cross-year-only with same-year broken by `narrative_first`?). $0 deterministic once decided.
2. **Causal `TRIGGERS` / consequence edges** — the dip's MEASURED gap (highest query-value). Interpretive →
   pollution-sensitive → needs Matt's sign-off. Recommended pilot: the Robert's Rebellion chain (Harrenhal 281 →
   Trident 283 → Sack 283 → Tower of Joy), which now has participants + dates. Curator-guided, small, review-first.
3. **Dating leftovers** (mostly deterministic): 5 multi-year spans need `ac_year_end`/split decisions
   (`dance-of-the-dragons`, `war-of-the-five-kings`, `greyjoy-rebellion`, `regency-of-aegon-iii`,
   `first-blackfyre-rebellion` [196,212 — the 212 looks like a wiki error]); `long-night` → `ac_year:null` +
   `precision:era`; confirm `conquest-of-dorne` (dated node = the event, not the in-world book `object.text`);
   the 10 mistyped `*-ac` year-page nodes in `graph/nodes/characters/` (type/dir decision — `event.year`/chronology).
4. **Fable cleanup** (the original S101 loose end): nomenclature scheme pick (`working/nomenclature-reform-proposal.md`)
   + repo/working-dir reorg (`working/repo-reorg-plan-2026-06-12.md`, "plan only" — never executed).

## STEP 2 — execute whichever Matt picks
Follow the relevant plan/doc. Honor: deterministic-Python-before-LLM; backup `edges.jsonl` before any edge write;
frontmatter-only idempotent node patches; rebuild indexes/alias-resolver only on node ADD/RENAME; agents-propose-
Matt-decides for anything interpretive (TRIGGERS, ATTENDS).

## Context / source-of-truth
- `working/next-move-decisions-2026-06-16.md` — the 4 talking points in full (the authoritative menu).
- `working/session-results/2026-06-16-event-dating-APPLIED.md` — what shipped this session + staged leftovers.
- `working/session-results/2026-06-15-mode3-dip-rerun.md` — the measured gaps (causal + ATTENDS).
- `working/design-opinions/2026-06-16-era-field-analysis.md` — the `occurred:` schema + 9-invariant validator.

## Hard rules
- Do NOT `/endsession` without Matt's permission. Do NOT refetch the wiki. Backup before any `edges.jsonl` write.
- Do NOT add edge types to the vocab without Matt's explicit OK (decision #1).
