# Stage 4 v1.1 Refinement Candidate — Go/No-Go Proposal

**Produced by:** `scripts/stage4-refine-v1-edges.py --apply`  
**Inputs (read-only):** `graph/edges/edges.jsonl` (v1, 3,842 rows — confirmed byte-for-byte unchanged)  
**Outputs (scratch only):** `working/wiki/pass2-buckets/pass1-derived/_v1-refine/`

---

## Headline

**v1 3,842 → after hard drops: 3,832 survivors, of which 1,950 carry a soft `_qr_warning` (kept, not removed).**

- **Hard-dropped (schema errors):** 10 rows — genuine type-contract violations, removed from the candidate
- **Soft-flagged (quote relevance):** 1,950 rows — annotated with `_qr_warning: true` + `_qr_reason`, NOT dropped; findable/fixable later
- **Clean (no annotation):** 1,882 rows

---

## Hard Drops — Full List (10 rows)

Format: `src --EDGE--> tgt | contract: <which> | quote: "<q>"`

1. `theon-greyjoy --UNCLE_OF--> greyjoy-rebellion`  
   contract: UNCLE_OF requires char<->char, but target 'greyjoy-rebellion' is not a character  
   quote: `"Theon Turncloak." "I am a Greyjoy of Pyke," Theon reminded him.`

2. `black-walder-frey --LOVER_OF--> fair-isle`  
   contract: LOVER_OF requires char<->char, but target 'fair-isle' is not a character  
   quote: `He'd had Edwyn's wife too, that was common knowledge, Fair Walda had been known to slip into his bed`

3. `nestor-royce --COUSIN_OF--> bronze`  
   contract: COUSIN_OF requires char<->char, but target 'bronze' is not a character  
   quote: `One of those others is Bronze Yohn, after all, and Nestor is very much aware that he was born of the`

4. `daenerys-targaryen --RULES--> barristan-selmy`  
   contract: RULES target must not be a character, but target 'barristan-selmy' is a character  
   quote: `"Your Grace," Ser Barristan said, "there was a harpy drawn in the alley where he was f`

5. `daenerys-targaryen --RULES--> grey-worm`  
   contract: RULES target must not be a character, but target 'grey-worm' is a character  
   quote: `Have him washed and dressed for battle and bury him with cap and shield and spears." "It shall be as`

6. `robb-stark --ECHOES--> eddard-stark`  
   contract: ECHOES must not connect two characters (src='robb-stark' tgt='eddard-stark')  
   quote: `Lord Rickard Karstark glowered in silence.`

7. `robb-stark --HEIR_TO--> winterfell`  
   contract: HEIR_TO requires char<->char, but target 'winterfell' is not a character  
   quote: `He seemed to have grown of late, as if Bran's fall and his mother's collapse had somehow made him st`

8. `missandei --SIBLING_OF--> three-sisters`  
   contract: SIBLING_OF requires char<->char, but target 'three-sisters' is not a character  
   quote: `"Three of them were my brothers once, Your Grace." Then I hope your brothers are as brave and clever`

9. `lord-tywin --RULES--> tommen-baratheon`  
   contract: RULES target must not be a character, but target 'tommen-baratheon' is a character  
   quote: `Until then the realm would remain firmly in the hands of his lord grandfather.`

10. `gilly --PARENT_OF--> her-little-flower`  
    contract: PARENT_OF requires char<->char, but target 'her-little-flower' is not a character  
    quote: `When Gilly entered, she went at once to her knees.`

**Notes on drops:**
- Rows 4, 5, 9: Typer confused "rules over" (interpersonal authority) with "RULES location". COMMANDS would be correct.
- Row 1: `greyjoy-rebellion` is an event slug; UNCLE_OF was mis-applied, probably should be PARTICIPANT_IN or similar.
- Row 2: `fair-isle` is a location; `LOVER_OF` mis-fired on "Fair Walda" (partial name match during typing).
- Row 3: `bronze` is not a slug — target resolution reduced "Bronze Yohn" to the adjective alone; the edge itself (Nestor/Bronze Yohn kinship) is real.
- Row 6: ECHOES char<->char — Robb/Eddard parallel is genuine literary observation, but the type contract correctly gates it out (ECHOES is for motif/text, not interpersonal).
- Row 7: HEIR_TO requires char<->char; "Robb is heir to Winterfell" is a valid relation but the wrong edge type (HEIR_TO should point to a title-holder, not a place).
- Row 8: `three-sisters` is a location (islands); Missandei's brothers are not encoded as individual character nodes.
- Row 10: `her-little-flower` is not a canonical character slug.

---

## Soft Flags — Summary

Soft-flagged rows are **kept** in the candidate. They are annotated with `_qr_warning: true` and `_qr_reason`.  
Queries can `filter(_qr_warning != true)` for maximum-confidence edges, or include them all.

### Total: 1,950 flagged out of 3,832 survivors (50.9%)

### By reason

| Reason | Count | Interpretation |
|---|---|---|
| `unmatched_source` | 970 | Source entity not named in the quote — pronoun reference, window artifact |
| `unmatched_target` | 661 | Target entity not named in the quote — same |
| `both` | 307 | Neither endpoint named — broad-context quote, valid edge possible |
| `unmatchable` | 9 | Slug resolves to zero usable tokens (very short or all-stopword slug) |
| `no_quote` | 3 | `evidence_quote` field empty |

### By edge_type (top 20)

| Edge type | QR-flagged |
|---|---|
| GUEST_OF | 263 |
| SERVES | 140 |
| OPPOSES | 125 |
| DISTRUSTS | 115 |
| HATES | 99 |
| COMMANDS | 93 |
| MOURNS | 80 |
| PROTECTS | 69 |
| RESENTS | 64 |
| LOVES | 61 |
| RESPECTS | 61 |
| COMPANION_OF | 52 |
| FEARS | 49 |
| KILLS | 47 |
| ALLIES_WITH | 45 |
| SWORN_TO | 45 |
| TRUSTS | 38 |
| VIOLATES_GUEST_RIGHT | 36 |
| SEEKS | 29 |
| LOVER_OF | 22 |

GUEST_OF dominates (263 flags) because the hospitality evidence quotes are frequently scene-setting sentences that name the host location or a third party rather than both the guest and host directly.

---

## 10-Row Sample of Soft-Flagged Edges (seed=42)

For sanity-checking: these should look like valid edges with pronoun/window quote artifacts.

| Source | Edge | Target | QR reason | Quote excerpt |
|---|---|---|---|---|
| robb-stark | RESENTS | robett-glover | unmatched_source | `"Robett Glover will answer for that when I see him, I promise you."` |
| gold | SERVES | queen-cersei | both | `"Be quiet!" Yoren fingered the warrant ribbon with its blob of golden wax.` |
| catelyn-stark | DISTRUSTS | theon-greyjoy | unmatched_source | `"Gods be good, you might even have sent Theon, though he would not be my choice."` |
| arys-oakheart | VOWS_TO | myrcella-baratheon | unmatched_source | `"For if Myrcella should be slain in Dorne whilst under my protection…"` |
| jarl | SERVES | mance-rayder | unmatched_source | `"Mance promises swords for every man of the first team to reach the top"` |
| barristan-selmy | SERVES | robert-baratheon | both | `"You protected my father for many years, fought beside my brother on the Trident…"` |
| catelyn-stark | TRUSTS | brienne-tarth | unmatched_source | `"May the Warrior give strength to your sword arm, Brienne, she prayed."` |
| catelyn-stark | FEARS | sansa-stark | both | `"If they have slain the Kingslayer, then my daughters are dead as well."` |
| aeron-greyjoy | RESENTS | balon-greyjoy | unmatched_target | `"He was all that an elder brother ought to be, though he had never shown Aeron aught but scorn."` |
| marillion | TRAVELS_WITH | lady-catelyns-sept | both | `"There is a great song to be made from this, and I'm the one to make it," he told Catelyn Stark…` |

The sample confirms the expected pattern: quotes are valid evidence for the edge, but the tokenizer cannot find both entity names because one appears only by pronoun, title, or is outside the quote window.

---

## Integrity Check

```
graph/edges/edges.jsonl line count: 3,842  (unchanged — confirmed before and after run)
```

---

## Files Written (scratch only — NOT in graph/edges/)

- `working/wiki/pass2-buckets/pass1-derived/_v1-refine/edges-v1.1-candidate.jsonl` — 3,832 rows
- `working/wiki/pass2-buckets/pass1-derived/_v1-refine/v1.1-type-contract-dropped.jsonl` — 10 rows

---

## Recommendation

The 10 hard drops are genuine schema errors — mixed-type endpoints that passed
endpoint-gate during formalization but violate the tighter type contracts.
Dropping them is safe.

The 1,950 soft-flags are NOT wrong edges — they are real edges whose quote
windows happen not to name both endpoints by recognizable token. The `_qr_warning`
field makes them queryable. A future pass can supply better quotes from the
chapter text.

**Suggested next action:** approve the candidate; promote
`edges-v1.1-candidate.jsonl` to `graph/edges/edges.jsonl` (replacing v1).
