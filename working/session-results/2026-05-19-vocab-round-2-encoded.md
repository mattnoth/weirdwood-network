# Vocab Round 2 Encode — Session Results

**Date:** 2026-05-19 (Session 58 continuation)
**Worker model:** Sonnet 4.6
**Task:** Mechanical encode of 8 STRONG ADOPT verdicts from vocab-completeness audit → 10 new edge types across 6 files.

---

## The 10 new edge types — placements

| # | Edge type | Subsection | Directionality | Tier |
|---|---|---|---|---|
| 1 | `SPIES_ON` | Knowledge & Information | Person → Surveilled-person | Tier-3 |
| 2 | `INFORMS` | Knowledge & Information | Person → Handler/Spymaster | Tier-3 |
| 3 | `NAMED_AFTER` | **Cultural & Religious** | Entity → Namesake-entity (one-sided) | Tier-3 |
| 4 | `STEP_PARENT_OF` | Kinship & Family | Step-parent → Step-child | Tier-3 |
| 5 | `STEP_CHILD_OF` | Kinship & Family | Step-child → Step-parent | Tier-3 |
| 6 | `IN_LAW_OF` | Kinship & Family | Symmetric | **Tier-2 OPTIONAL enum** |
| 7 | `RESCUES` | Military & Conflict | Rescuer → Rescued-person | Tier-3 |
| 8 | `BANISHES` | Political & Authority | Banisher → Banished-person | Tier-3 |
| 9 | `TORTURES` | Military & Conflict | Torturer → Tortured-person | Tier-3 |
| 10 | `CONSPIRES_WITH` | Factional & Diplomatic | Symmetric | Tier-3 |

---

## NAMED_AFTER subsection choice — Cultural & Religious

**Choice: Cultural & Religious** (not Identity & Disguise).

**Rationale:** `NAMED_AFTER` captures dynastic name-recycling — a cultural institution rather than an identity act. Cultural & Religious already holds edges about cultural group membership (`CULTURE_OF`), religious practice (`WORSHIPS`, `CLERGY_OF`), and cultural ceremony (`OFFICIATES`). Dynastic naming is a cultural transmission practice: Rickard Karstark was named after Rickard Stark as a deliberate cultural act of allegiance and honor. This is categorically distinct from `ALIAS_OF` / `DISGUISED_AS` / `IMPERSONATES` (which are about active identity manipulation or alternative names for the same entity). Identity & Disguise is the wrong drawer — nothing about `NAMED_AFTER` involves deception or alternative identity. Cultural & Religious is the correct drawer.

---

## Judgment calls

1. **STEP_PARENT_OF / STEP_CHILD_OF reverse treatment:** These are treated as a one-sided pair (explicit emit on both endpoints, like KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON), not as a symmetric edge (like IN_LAW_OF or CONSPIRES_WITH). This is consistent with PARENT_OF / CHILD_OF design (CHILD_OF is rejected as a vocab gap; PARENT_OF emits on parent only) — but STEP_PARENT_OF gets explicit both-sided emit because the step relationship's distinct character warrants recording on both nodes. Encoded in the reverse-direction section of the classifier prompt.

2. **IN_LAW_OF and CONSPIRES_WITH as symmetric:** Both added to the new "Symmetric edges (emit once)" callout in the reverse-direction section, separate from the existing one-sided-pair list. This is architecturally clean: one-sided pairs emit on both nodes (two output rows), symmetric edges emit once (one output row, query layer infers reverse).

3. **BANISHES placement in Political & Authority:** The audit rationale says "Political & Authority" — correct. Banishment is a political act by a ruler or authority figure. DEPOSES removes from power; BANISHES expels from domain. Both belong in Political & Authority. No ambiguity.

4. **IN_LAW_OF qualifier enum matches the launch manifest exactly:** `{by_marriage_of_self, by_marriage_of_child, by_marriage_of_sibling, by_marriage_of_parent, unknown}` — 5 values. This is more granular than the audit's original "optional with enum" specification and correctly identifies which third-party marriage created the affinity. Added as 10th row in edge-qualifier-vocab.md Tier-2 table.

---

## Vocab count verification — consistent across all three reference files

| File | Count before | Count after | How stated |
|---|---|---|---|
| `reference/architecture.md` | ~149 | **~159** | Updated in vocabulary-lock callout block (two occurrences: main callout + "gap-filing" sentence) |
| `reference/architecture.md` | Tier-2: 9 | **Tier-2: 10** | Updated in qualifier cross-ref line in Edge Types intro |
| `reference/edge-qualifier-vocab.md` | "9 edge types" / total "~149" | **"10 edge types" / total "~159"** | Updated section heading + count-check line |
| `.claude/agents/prose-edge-classifier.md` | ~149 (×5 occurrences) | **~159** | All instances updated: First Steps §1, qualifier lookup step §4, Vocabulary lock heading, "You may not invent" paragraph, Definition of Done |

All three files now consistently state ~159 total, Tier-2 count = 10.

---

## Files modified

1. `reference/architecture.md` — 10 new edge-type rows added across 6 subsections; vocab callout updated 149 → 159 (2 occurrences); Tier-2 cross-ref updated 9 → 10.
2. `reference/edge-qualifier-vocab.md` — IN_LAW_OF added as 10th Tier-2 row; section heading updated "9 → 10"; count-check line updated "Tier 2 (9)" → "Tier 2 (10)" and "~149" → "~159".
3. `.claude/agents/prose-edge-classifier.md` — all ~149 references updated to ~159; Tier-2 "nine" updated to "ten"; category-expansion list extended with 10 new types in their correct subsections; reverse-direction section extended with STEP_PARENT_OF/STEP_CHILD_OF (one-sided pair) and IN_LAW_OF/CONSPIRES_WITH (symmetric callout).
4. `working/qualifier-vocab/decisions.md` — Round 2 section appended (Round 1 content untouched).
5. `working/todos.md` — HAIKU-CUTOVER STEP 1.7 added and marked done.
6. `working/session-results/2026-05-19-vocab-round-2-encoded.md` — this file.

---

## What's next

- HAIKU-CUTOVER STEP 5 (Haiku smoke test) is now unblocked from the vocab side. Remaining blockers per todos.md: STEP 5 itself (select 3-4 diverse batches; run Haiku vs Sonnet control arm; diff metrics).
- The validator (`scripts/wiki-pass2-validate-edge-jsonl.py`) will automatically pick up the 10 new edge types on its next run — it loads architecture.md vocab via regex. No script change needed.
- The suspicious-edges flagger script similarly uses architecture.md as source of truth — no change needed.
- Worklog update: this encode work is part of Session 58; worklog entry will be written when Matt runs /endsession.
