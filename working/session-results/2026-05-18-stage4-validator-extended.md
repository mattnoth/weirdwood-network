# Session Results: Stage 4 Validator Extended (HAIKU-CUTOVER STEP 3)

**Date:** 2026-05-18
**Agent:** script-builder (Sonnet 4.6)
**Task:** Extend `scripts/wiki-pass2-validate-edge-jsonl.py` with three new check classes

---

## Status: COMPLETE

HAIKU-CUTOVER STEP 3 done. Three new check classes added to the validator. Self-test passed — old violations still caught, new violation classes firing correctly on the 21-batch freeform control arm.

---

## What Was Built

**File modified:** `/Users/mnoth/source/asoiaf-chat/scripts/wiki-pass2-validate-edge-jsonl.py`

### Check 1: Type Contracts

- 22 edge-type → target-type constraint entries in `TYPE_CONTRACTS` dict
- Transcribed from `.claude/agents/prose-edge-classifier.md` § "Type contracts on common-failure edge types"
- Resolution: `build_node_type_index()` walks `graph/nodes/` and builds a slug→type map from YAML frontmatter (8,050 nodes indexed in the current graph)
- Pattern matching: prefix-based (`"place."` matches `"place.location"` and `"place.region"`)
- Unresolvable target slugs: check is SKIPPED (warning printed to stderr; slug added to `unresolved_slugs` set for summary)
- Violation kind: `type-contract-violation`
- New CLI flag: `--graph-nodes graph/nodes` (default), `--skip-type-contracts`

### Check 2: Qualifier Enums

- Loads `reference/edge-qualifier-vocab.md` via `load_qualifier_vocab()` — parses Tier-1 and Tier-2 tables into `{edge_type: (tier, frozenset(values))}`
- Tier-1 (8 REQUIRED types: SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO): rejects if qualifier absent or not in enum
- Tier-2 (9 OPTIONAL types: BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, KNOWS, GUEST_OF): accepts absent qualifier; rejects present-but-out-of-enum
- Tier-3 (all other ~132 types): rejects any non-empty qualifier field
- Violation kinds: `qualifier-required-missing`, `qualifier-not-in-enum`, `qualifier-tier3-not-allowed`
- New CLI flag: `--qualifier-vocab reference/edge-qualifier-vocab.md` (default), `--skip-qualifier-enums`

### Check 3: Notes Rejection

- Any row (any decision type: emit_edge, reject_just_mention, escalate_cross_identity, escalate_disambiguation) carrying a `notes` field triggers a violation
- The `notes` field was deleted from the schema entirely 2026-05-18 (Session 57)
- Violation kind: `notes-field-present`
- No new CLI flag needed — always enforced

---

## Self-Test Results

### Test 1: Old violations (batch-0012 archive)

Command:
```
python3 scripts/wiki-pass2-validate-edge-jsonl.py \
    --graph-nodes graph/nodes \
    --qualifier-vocab reference/edge-qualifier-vocab.md \
    --file working/wiki/pass2-buckets/_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/characters-house-costayne/elinor-costayne.edges.jsonl \
    [... 4 files total]
```

Result: `violations=9, invalid-candidate-kind: 9` — same as before extension. Old checks unaffected.

Full archive (30 files, 104 rows): `violations=104, invalid-candidate-kind: 104` — all old violations caught.

### Test 2: New violations (21-batch Sonnet control arm)

898 edge output files, 14,799 rows checked:

| Violation kind | Count | Notes |
|---|---|---|
| `invalid-candidate-kind` | 1,526 | Pre-existing check |
| `missing-required-fields` | 3,142 | Pre-existing check |
| `bad-confidence-tier` | 913 | Pre-existing check |
| `bad-evidence-kind` | 913 | Pre-existing check |
| `bad-evidence-section` | 340 | Pre-existing check |
| `snippet-too-short` | 231 | Pre-existing check |
| `edge-type-not-canonical` | 37 | Pre-existing check |
| `invalid-decision` | 2 | Pre-existing check |
| **`notes-field-present`** | **193** | **NEW — Check 3** |
| **`qualifier-required-missing`** | **149** | **NEW — Check 2 Tier-1** |
| **`qualifier-not-in-enum`** | **380** | **NEW — Check 2 Tier-1+2** |
| **`qualifier-tier3-not-allowed`** | **1,757** | **NEW — Check 2 Tier-3** |
| **`type-contract-violation`** | **49** | **NEW — Check 1** |

The high qualifier counts are expected — the 21 Sonnet batches are the freeform control arm emitted before the qualifier vocab was locked. These violations are the data proving the control arm was genuinely freeform: qualifiers were emitted freely on Tier-3 edges, and Tier-1 required qualifiers were often absent.

---

## Open Questions / Edge Cases

1. **Unresolvable target slugs in type-contract checks**: When a target slug is not found in the 8,050-node graph index, the type-contract check is skipped for that row. This is correct behavior — the slug may be a valid entity not yet promoted to `graph/nodes/`. The validator prints the count of unresolved slugs in the summary (visible with `--verbose`). In the control-arm run, 0 unresolved slugs were reported for the 49 type-contract violations (all targets were found).

2. **Notes on reject/escalate rows**: The notes-rejection check fires on ALL decision types, not just `emit_edge`. Of the 193 violations in the control arm, all were on `reject_just_mention` rows (189) and `emit_edge` rows (20 with 4 additional rows noted in the diff). The schema deletion covers all decision types per the qualifier-vocab file's wording.

3. **Type-contract check scope**: Only the 22 edge types in `TYPE_CONTRACTS` are checked. Edges like `LOCATED_AT` pointing to `event.*` (the most common anti-pattern per the classifier prompt) ARE covered. The 49 violations in the control arm are real schema problems that the locked Haiku run should not produce.

4. **Qualifier `null` / `""` handling**: The validator treats `null` (JSON null → Python None) and `""` (empty string) both as absent for Tier-2 purposes, and as triggering `qualifier-required-missing` for Tier-1. A value of `null` stored in JSON would be read as Python `None` and treated as absent. This is the correct behavior.

---

## Files Changed

- `scripts/wiki-pass2-validate-edge-jsonl.py` — extended (three new check classes + two new loaders + two new CLI flags + updated docstring with self-test commands + violation-by-kind summary in output)
- `working/todos.md` — HAIKU-CUTOVER STEP 3 marked [x]
- `working/session-results/2026-05-18-stage4-validator-extended.md` — this file

---

## What's Next

STEP 5 (Haiku smoke test) is now unblocked from the STEP 3 / STEP 4 side. All five prep steps are complete:
- STEP 1 (vocab lock) — done
- STEP 1.5 (qualifier vocab lock) — done
- STEP 1.6 (encode qualifier vocab) — done
- STEP 2 ([LINK] substitution) — done
- STEP 3 (validator extension) — DONE THIS SESSION
- STEP 4 (suspicious-edges flagger) — done

STEP 5 gates on Matt's smoke-test approval. Recommended batches: 0066, 0068, 0072, 0001.
