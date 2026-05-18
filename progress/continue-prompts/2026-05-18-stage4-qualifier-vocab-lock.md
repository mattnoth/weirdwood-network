# Stage 4 Qualifier Vocab Lock-Down

> **Recommended model:** Opus 4.7 — corpus-knowledge synthesis at scale (Pass 1 distribution analysis + 21-batch empirical analysis + ~149 edge-type verdicts). Reasoning-depth genuinely required; Sonnet would burn too many tool calls re-deriving context.
>
> **Parent context:** HAIKU-CUTOVER STEP 1.5 in `working/todos.md`. Plan at `working/qualifier-vocab/plan.md`. **Read plan.md first** — it's a 1-screen scannable doc with the three-tier framing, data sources, encoding-strategy options, and open questions already laid out.
>
> **What this session does:** lock the qualifier vocabulary (closed enum per edge type) so the prose-edge-classifier cannot freestyle on `notes`. Three-tier framing locked Session 56: Tier 1 (REQUIRED enum), Tier 2 (OPTIONAL enum), Tier 3 (no enum / freeform notes only).
>
> **What this session does NOT do:** implement the architecture.md encoding (separate session), implement the validator extension (folded with HAIKU-CUTOVER STEP 3), retrofit already-emitted batches (deferred).

---

## Goal

Produce **`working/qualifier-vocab/decisions.md`** — tabular verdict-per-edge-type, with enum proposals for Tier 1 and Tier 2 types, drawn from the actual corpus + batches + wiki, not invented.

---

## Inputs (READ THESE)

1. `working/qualifier-vocab/plan.md` — the plan.
2. `reference/architecture.md` § "Edge Types (Relationship Categories)" — the ~149 master vocab.
3. `extractions/mechanical/{agot,acok,asos,affc,adwd}/*.extraction.md` (344 files). The `## Relationships Observed` table per chapter is the raw distribution of how the books describe relationship qualifiers in narrative voice. **Sampling strategy:** grep across all 344 for relationship terms keyed to each edge-type candidate (e.g., for SIBLING_OF: grep "half-brother|half-sister|step-brother|step-sister|milk brother|sibling"). Tally observed qualifier-language counts per edge type.
4. `working/wiki/data/infobox-data.jsonl` (5,279 entities). Some infobox fields encode qualifier-like flags: `(Current)`, `(Former)`, `(Annulled)`, `(Deceased)`. Run a Python pass to extract those.
5. **21 completed Sonnet batches** at `working/wiki/pass2-buckets/<bucket>/prose-edges/*.edges.jsonl` (75 batches total per manifest as of 2026-05-17, ~21+ rerun-fresh after vocab fix). Sample the `notes` field distribution per edge type. Patterns repeat = enum candidates. Patterns vary = either subset to enum or stay Tier 3.

---

## Process (suggested)

### Phase 1 — Tier-1 candidates (most reasoning-heavy)

For each candidate below, query the corpus + batches, propose an enum, verify it covers ≥90% of observed cases:

- `SIBLING_OF` — propose `{full, half, step, milk, unknown}`. Verify with grep on Pass 1 corpus.
- `SPOUSE_OF` — propose `{current, former, annulled, widowed, unknown}`. Verify with infobox `(Current)/(Former)/(Annulled)/(Deceased)` count.
- `BETROTHED_TO` — propose `{current, broken, fulfilled, contested}`. Verify in corpus.
- `PARENT_OF` — propose `{biological, adoptive, step, claimed, fostered, unknown}`. Note: WARD_OF/FOSTERED_BY exist; PARENT_OF.fostered may be redundant — decide.
- `WARD_OF` — propose `{formal, informal, hostage, unknown}`.
- `HOLDS_TITLE` — propose `{current, former, contested, claimed, hereditary}`.
- `VOWS_TO` — propose `{active, kept, broken, fulfilled}`.
- `MANIPULATES` — **ALREADY LOCKED** Session 55: `{via_bribe, via_flattery, via_false_information, via_threat, via_seduction, unknown}`. Confirm and document.

### Phase 2 — Tier-2 candidates (medium reasoning)

- `KILLS` — propose `{in_combat, in_duel, by_arrow, by_ambush, by_proxy, via_creature, unknown}`. (Note: POISONS is separate type; don't fold.)
- `CONTRACTED_WITH` — propose `{assassination, mercenary, construction, ransom, safe_passage, marriage_brokerage, unknown}`.
- `DECEIVES` — propose `{by_lie, by_disguise, by_omission, by_false_witness, unknown}`.
- `REVEALS_TO` — propose `{voluntary, coerced, accidental, under_torture, unknown}`.
- `ATTACKS` — propose `{in_anger, unprovoked, in_self_defense, on_command, by_creature, unknown}`.
- `KNOWS` — propose `{confirmed, suspected, told_by_X, witnessed, unknown}`.
- Others surfaced during analysis — list and verdict.

### Phase 3 — Tier-3 (default; fast)

All other ~130 edge types are Tier 3 unless data shows otherwise. For each, one-line rationale ("emotional/perceptual; inherently fuzzy"). Quick.

### Phase 4 — Encoding-strategy decision

Per `plan.md`, pick Option A (new column in architecture.md tables) / B (separate qualifier table per subsection) / C (separate file). Document choice + rationale in decisions.md.

### Phase 5 — Write decisions.md

Tabular format per `plan.md`. One verdict per type. Group by tier.

### Phase 6 — Update todos.md

Mark HAIKU-CUTOVER STEP 1.5 [x] DONE. Add a new STEP 1.6 — "Encode qualifier vocab into architecture.md + classifier prompt" with the chosen encoding strategy.

### Phase 7 — Session-results file

`working/session-results/<date>-stage4-qualifier-vocab-locked.md` — counts per tier, encoding choice, what next session does.

---

## Open questions to answer in decisions.md

(See `plan.md` § "Open questions for next session" — copy the 4 questions and answer them.)

1. Backfill strategy for the 21 already-emitted batches? Lean (a) — document as freeform-legacy.
2. Tier-3 `notes` discipline — cap at 100 chars? Required documentation as non-queryable.
3. Symmetric-edge qualifier semantics — yes, shared across both endpoints.
4. Combine type-contract column with qualifier column (single architecture.md change)?

---

## Definition of done

- [ ] `working/qualifier-vocab/decisions.md` written — tabular, one verdict per edge type, ~149 rows.
- [ ] All Tier-1 enums verified against corpus distribution (≥90% coverage demonstrated).
- [ ] All Tier-2 enums proposed with rationale + data source.
- [ ] Encoding strategy (A/B/C) chosen with rationale.
- [ ] Open questions answered.
- [ ] `working/todos.md`: HAIKU-CUTOVER STEP 1.5 marked [x]; new STEP 1.6 added.
- [ ] Session-results file written.

After: STEP 1.6 (encode into architecture.md + classifier prompt) is a separate implementation session. STEP 3 (validator extension) folds in the qualifier-enum enforcement alongside the type-contract checks.

---

## DO NOTs

- Do NOT propose enums without checking the data. The corpus has the answer; trust it.
- Do NOT make Tier-3 verdicts a 130-row death-march. One-line rationale per type is enough.
- Do NOT touch architecture.md or the classifier prompt — those changes are in the encoding session (STEP 1.6).
- Do NOT touch already-emitted edges. Backfill is a separate decision (lean defer).
- Do NOT run /endsession without permission.
