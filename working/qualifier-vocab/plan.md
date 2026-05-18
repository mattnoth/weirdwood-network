# Qualifier Vocabulary Lock-Down — Plan

> **Status:** PLAN. Decisions not yet made.
> **Surfaced:** Session 56 (2026-05-18) during Stage 4 vocab-lock apply.
> **Continue prompt for next session:** `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md`

## Why

The Stage 4 classifier currently emits a freeform `notes` string on edges. That's a second drift surface — unbounded English next to a locked enum vocabulary. Haiku is more drift-prone than Sonnet; the way to make Haiku viable is to close every freestyle surface the classifier has. **Lock the qualifier vocab before the Haiku smoke runs.**

## Three-tier framing (locked Session 56)

| Tier | Behavior | Validator |
|---|---|---|
| **1 — REQUIRED enum** | Edge MUST emit a `qualifier` field from a small closed set | Validator rejects edges missing or out-of-enum |
| **2 — OPTIONAL enum** | `qualifier` may be null; if emitted, must match the enum | Validator rejects out-of-enum |
| **3 — no enum** | No `qualifier` field. `notes` is freeform, explicitly non-queryable, only for narrative-only context | None |

## Data sources next session draws from (USE ALL of these)

1. **Pass 1 corpus** — `extractions/mechanical/{agot,acok,asos,affc,adwd}/*.extraction.md` (344 files; all 5 books). The `## Relationships Observed` table captures relationship in free-text — that text is the raw distribution of how the books actually describe relationship qualifiers.
2. **Wiki infobox data** — `working/wiki/data/infobox-data.jsonl` (5,279 entities). Some infobox fields ARE qualifier surfaces: `Spouse` rows often carry `(Current)` / `(Former)` / `(Annulled)` / `(Deceased)` notes; `Allegiance` carries `(Former)`; etc.
3. **21 completed Sonnet batches** — `working/wiki/pass2-buckets/<bucket>/prose-edges/*.edges.jsonl`. The `notes` field on each emitted edge is real-world data on what the classifier ACTUALLY produced — gives empirical distribution per edge type. Patterns repeat = enum candidates.
4. **ASOIAF series knowledge** — for types where the corpus is sparse, default to canonical-fan-consensus enums (e.g., SIBLING_OF half/full/step is universal; SPOUSE_OF current/former/annulled/widowed maps the four documented states).
5. **AWOIAF wiki structured data** — the wiki encodes specific qualifier-like flags in some infobox columns. Use them when present.

## Output of the next session

**Single decision artifact:** `working/qualifier-vocab/decisions.md` — tabular, verdict-per-edge-type.

Proposed table format:

| Edge Type | Tier | Enum (if Tier 1/2) | Rationale | Data source |
|---|---|---|---|---|
| `SIBLING_OF` | 1 | `{full, half, step, milk, unknown}` | Universal Westerosi kinship category; high query value | corpus + series knowledge |
| `SPOUSE_OF` | 1 | `{current, former, annulled, widowed, unknown}` | Four canonical marital states; wiki infobox tags them | wiki infobox |
| `MANIPULATES` | 1 | `{via_bribe, via_flattery, via_false_information, via_threat, via_seduction, unknown}` | Locked Session 55 | Session 55 verdict |
| `LOVES` | 3 | — | Inherently fuzzy; no clean enum surface | — |
| `KILLS` | 2 | `{in_combat, in_duel, by_arrow, by_ambush, via_dragon, via_proxy, by_poison_separately_use_POISONS, unknown}` | Useful when known; null acceptable | corpus distribution |
| ... | ... | ... | ... | ... |

## Per-edge-type expected coverage (next session does these decisions)

All ~149 master vocab types get classified into Tier 1 / 2 / 3. **Default is Tier 3** unless the type earns Tier 1 or Tier 2.

Candidate Tier 1 / Tier 2 list (next session validates against data; this is the orchestrator's pre-read):

- **Tier 1 candidates:** SIBLING_OF, SPOUSE_OF, BETROTHED_TO (current/broken/fulfilled), MANIPULATES (already locked), PARENT_OF (biological/adoptive/step/claimed), WARD_OF (formal/informal/hostage), HOLDS_TITLE (current/former/contested/claimed), VOWS_TO (active/kept/broken/fulfilled)
- **Tier 2 candidates:** KILLS (method), CONTRACTED_WITH (service-type), DECEIVES (method), REVEALS_TO (voluntary/coerced/torture), ATTACKS (in_anger/unprovoked/in_self_defense), KNOWS (confirmed/suspected/told_by/witnessed)
- **Tier 3 (most types):** all emotional/perceptual (LOVES, FEARS, RESPECTS, HATES, MOURNS, PERCEIVED_AS), spatial (LOCATED_AT, TRAVELS_TO, BORN_AT, DIED_AT, BURIED_AT), narrative (FORESHADOWS, PARALLELS, ECHOES, CONTRASTS), most factional, most prophecy/evidentiary

## Encoding strategy (decide next session)

Three options; pick during decision-making, not before:
- **Option A:** New column in each `## Edge Types` subsection table in architecture.md — `Qualifier Enum` column added to every table row.
- **Option B:** Separate qualifier table per subsection, appended to each subsection (only lists types with Tier 1/2 enums).
- **Option C:** Separate file at `reference/edge-qualifier-vocab.md`; cross-reference from architecture.md.

Tradeoff: A is most discoverable but adds visual noise to Tier-3 rows. B is cleanest but spreads the data. C is most modular but adds cross-file lookup.

## Validator extension (separate implementation session)

After decisions land:
1. Extend `scripts/wiki-pass2-validate-edge-jsonl.py` to load qualifier-enum-per-edge-type from architecture.md (or the new file if Option C).
2. Enforce Tier-1 required-and-enum-match (rejects edge).
3. Enforce Tier-2 enum-match-if-present (rejects edge).
4. Pass-through Tier-3 (no check).
5. Self-test against 1-2 known-good batches.

Validator extension is a follow-up session AFTER decisions land. Same session as HAIKU-CUTOVER STEP 3 (type-contract extension) — folded together since both extend the same script.

## Open questions for next session

1. **Backfill for the 21 already-emitted batches?** Their `notes` fields are freeform. Three options: (a) leave them, document as freeform-legacy; (b) write a post-hoc normalizer (Python + LLM combo) that maps freeform `notes` to qualifier enum; (c) re-classify them on Haiku once vocab is locked. Lean (a) for v1, (b) as a polish pass.
2. **Tier 3 `notes` discipline.** Should Tier 3's `notes` be capped (max-N-words) or fully freeform? Lean: capped at 100 chars, explicit "non-queryable" documentation, never required.
3. **Symmetric-edge qualifier semantics.** When SIBLING_OF is symmetric and one endpoint says "half-brother on father's side," does both endpoints' edge carry the same qualifier? Yes — symmetric edges share qualifier. Document.
4. **Type-contract column?** While we're adding a Qualifier column to architecture.md (if Option A), should we ALSO add the target-type contract that HAIKU-CUTOVER STEP 3 needs? Probably yes — one column-addition session, two purposes.

## DO NOTs

- Do NOT propose enums without checking the data first (Pass 1 corpus + 21 batches + wiki infobox).
- Do NOT skip the empirical distribution step for Tier 1/2 candidates — the corpus has the answer.
- Do NOT make this a 149-row death-march. Tier 3 is the default. Most types stay Tier 3 with one sentence rationale.
- Do NOT touch `notes` discipline retroactively on already-emitted edges this session.
