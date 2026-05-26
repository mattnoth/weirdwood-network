# Pass-1-Derived v1.1 Refinement — Applied Report

**Input:** `/Users/mnoth/source/asoiaf-chat/graph/edges/edges.jsonl` (READ-ONLY — not modified)
**Total in:** 3842

---

## Summary

| Operation | Count |
|-----------|-------|
| Input rows | 3842 |
| SURE-DROP (genuinely wrong target) | 4 |
| Type-contract DROP | 33 |
| **Total dropped** | **37** |
| RULES→COMMANDS retype | 3 |
| Contract FLAG/FLIP | 2 |
| ECHOES char↔char KEPT | 1 |
| ECHOES _evidence_weak:true applied | 1 |
| NODE-DEPENDENT flagged | 5 |
| QR soft-flagged | 1930 |
| **Final candidate rows** | **3805** |

---

## SURE-DROP List (4 targeted + any contract drops)

### Targeted drops (genuinely wrong target — not a person):

- `theon-greyjoy UNCLE_OF greyjoy-rebellion`
- `black-walder-frey LOVER_OF fair-isle`
- `missandei SIBLING_OF three-sisters`
- `gilly PARENT_OF her-little-flower`

_All 4 sure-drop targets found and dropped._

---

## RULES→COMMANDS Retype List

Architecture: RULES = Ruler→Location; COMMANDS = Commander→Subordinate.
These edges had a character target — correct type is COMMANDS.

- `daenerys-targaryen RULES→COMMANDS barristan-selmy`
- `daenerys-targaryen RULES→COMMANDS grey-worm`
- `lord-tywin RULES→COMMANDS tommen-baratheon`

---

## ECHOES char↔char — KEPT

Contract was removed per architecture: ECHOES is valid for character↔character.

- `robb-stark ECHOES eddard-stark` [_evidence_weak:true]

---

## NODE-DEPENDENT Flags (endpoints unchanged, awaiting node decision)

Format: `src EDGE tgt` → `_proposed_fix`

- `nestor-royce COUSIN_OF bronze` → `retarget target bronze->yohn-royce (alias)`
- `robb-stark HEIR_TO winterfell` → `retarget target winterfell->lord-of-winterfell (title node)`
- `queen-cersei SEEKS gendry` → `alias queen-cersei->cersei-lannister`
- `queen-cersei GUEST_OF eddard-stark` → `alias queen-cersei->cersei-lannister`
- `queen-cersei GUEST_OF house-stark` → `alias queen-cersei->cersei-lannister`

### WARNING: Expected node-dep edges NOT found in candidate:

- NOT FOUND: `queen-cersei SPOUSE_OF robert-i-baratheon`

---

## QR Soft-Flag Summary

Total QR-flagged rows: **1930**
(Kept in candidate, not dropped — soft annotation only)

| Reason | Count |
|--------|-------|
| unmatched_source | 968 |
| unmatched_target | 647 |
| both | 307 |
| unmatchable | 8 |

---

## Input Integrity Check

`graph/edges/edges.jsonl` is READ-ONLY. Total rows in: 3842.
This script NEVER writes to `graph/edges/`.

Total candidate rows out: 3805
Total dropped rows: 37
Expected: 3842 = 3805 + 37
Check: PASS
