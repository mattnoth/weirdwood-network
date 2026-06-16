# Era/Reckoning Field — Schema Decision
**Date:** 2026-06-16  
**Status:** DECIDED — ready for architecture.md amendment  
**Input:** `2026-06-16-era-field-research.md` + `2026-06-15-events-time-SYNTHESIS.md`

---

## 1. Is the `era: AC|BC` collision real and disqualifying?

**Yes. `era: AC|BC` is off the table — permanently.**

The collision is exact: `era:` is a **documented frontmatter field** (`reference/architecture.md:438`) with a completely different semantic — it is a **narrative epoch** classifier (enum: `pre-conquest | age-of-heroes | targaryen-conquest | targaryen-rule | dance-of-dragons | roberts-rebellion | current-narrative`). Using `era:` to carry `AC | BC` calendar reckoning would produce two irreconcilable meanings for the same key inside the same frontmatter block:

```yaml
era: current-narrative    # existing meaning: epoch classifier
era: AC                   # proposed meaning: calendar reckoning
# ↑ these cannot coexist; the second would shadow or corrupt the first
```

The fact that `era:` currently has zero live instances does **not** soften the collision — it is documented in architecture.md and forward-only for new mints, meaning every event node stamped from here on is expected to carry the epoch sense. Introducing a second sense now guarantees silent corruption the moment any node receives both. The collision is disqualifying.

**Also disqualified:** `year_era: AC|BC` as a top-level frontmatter field (Option C). Mirroring the `chronology-events.jsonl` field name would be consistent with the data layer, but `year_era` paired with `year_value` at top-level creates two peer scalar fields that don't signal they belong together — and they would sit at node scope, not inside an `occurred:` block, making the schema flat and harder to validate. The nesting of `occurred:` is the right level of abstraction.

---

## 2. Decision: Field name + storage model

**CHOSEN: Option A — signed `ac_year` integer, negative = BC. No separate reckoning field.**

### Justification

**Why Option A over Option B (positive magnitude + separate `reckoning: AC|BC`):**

Option B mirrors `chronology-events.jsonl`'s `year_value` + `year_era` split. That split exists because JSONL is flat and can't nest — a separating field is the only option when you can't encode sign. Inside YAML frontmatter, nesting is free. A signed integer encodes the reckoning *in the value itself*, which is:

- **Unambiguous:** `ac_year: -114` cannot mean AC; `ac_year: 283` cannot mean BC. A two-field form (`reckoning: AC`, `ac_year: 114`) can be contradicted (`reckoning: BC`, `ac_year: -114` → double-negative). The signed form has one truth surface, not two.
- **Sort-correct without preprocessing:** `ORDER BY ac_year ASC` on signed integers produces a correct chronological sequence directly. A two-field model requires either a join/transform or trusting that `reckoning: BC` was flipped — i.e., you must validate before sorting. `PRECEDES`/`FOLLOWS` derivation in Python is a one-liner on signed ints.
- **Drift-resistant:** the sign is mechanically enforced by integer type. A `reckoning` string is a freetext surface that can silently drift to `"BC"`, `"bc"`, `"B.C."`, `null` — and then the magnitude is ambiguous. There is no analogous ambiguity for a signed int.
- **Aligned with the synthesis schema:** `2026-06-15-events-time-SYNTHESIS.md` (the merged panel recommendation at line 69) already uses `ac_year: 283` (positive) and implies negatives for BC via the comment `# signed int; negative = BC`. This decision ratifies that choice explicitly.

**Why the field is named `ac_year` (not `year`, `calendar_year`, or `abs_year`):**

- `year` is too generic; the schema already distinguishes AC from BC and from narrative position (`narrative_first`). Readers should know immediately what the integer means.
- `ac_year` is already the field name used in the synthesis schema (the document this analysis feeds into). Consistent with the panel; no rename cost.
- `ac_year` signals the reference point (Aegon's Conquest = year 0) without needing to read adjacent fields. A reader seeing `ac_year: -8000` and `ac_year: 283` immediately knows the scale and zero-point.

**Convention for BC (negative values):**

| In-world event | `ac_year` value |
|---|---|
| Battle of the Trident (283 AC) | `283` |
| Harrenhal Tourney (281 AC) | `281` |
| Doom of Valyria (~114 BC) | `-114` |
| Long Night (~8000 BC, mythological) | _null_ (see §5) |

The `ac_year` field name reads slightly odd for BC events ("AC year is negative") but this is the universal convention for signed-integer calendar systems (BCE years are negative in ISO 8601, Unix calendars, etc.). The alternative — a separate field for each sense — introduces the drift surface the project cannot afford.

---

## 3. Validator rules

```python
def validate_occurred_block(node_slug, occurred):
    """Invariants every occurred: block must satisfy. Raise on violation."""

    ac_year = occurred.get("ac_year")
    ac_year_end = occurred.get("ac_year_end")
    precision = occurred.get("precision")
    basis_source = occurred.get("basis_source")
    date_confidence = occurred.get("date_confidence")
    uncertainty_radius = occurred.get("uncertainty_radius")
    basis_reliability = occurred.get("basis_reliability")

    # I1 — type contract: ac_year must be int or null, never string
    if ac_year is not None:
        assert isinstance(ac_year, int), \
            f"{node_slug}: ac_year must be int, got {type(ac_year).__name__}"

    # I2 — sign coherence: negative values are BC, no separate era/reckoning field needed;
    #       but if a reckoning: field somehow appears, it must agree with sign
    reckoning = occurred.get("reckoning")  # should not exist, but guard against it
    if reckoning is not None:
        raise ValueError(f"{node_slug}: reckoning: field must not appear; use signed ac_year")

    # I3 — span coherence: ac_year_end implies ac_year; end > start (in signed int order)
    if ac_year_end is not None:
        assert ac_year is not None, \
            f"{node_slug}: ac_year_end set but ac_year is null (need a start)"
        assert isinstance(ac_year_end, int), \
            f"{node_slug}: ac_year_end must be int, got {type(ac_year_end).__name__}"
        assert ac_year_end > ac_year, \
            f"{node_slug}: ac_year_end ({ac_year_end}) must be > ac_year ({ac_year})"

    # I4 — uncertainty_radius is for fuzzy point estimates, NOT spans; can't use both
    if uncertainty_radius is not None and ac_year_end is not None:
        raise ValueError(
            f"{node_slug}: uncertainty_radius and ac_year_end are mutually exclusive "
            f"(use ac_year_end for spans, uncertainty_radius for fuzzy single points)"
        )

    # I5 — basis required when ac_year is set (no naked dates)
    if ac_year is not None:
        assert basis_source is not None, \
            f"{node_slug}: ac_year set but basis_source is null (cite your source)"

    # I6 — mythological / age-inferred events must NOT carry ac_year (leave null)
    #       proxy: era field = age-of-heroes or pre-conquest AND ac_year set → flag for review
    node_era = occurred.get("era")  # see §4 for why era may appear inside occurred:
    if node_era in ("age-of-heroes",) and ac_year is not None:
        raise ValueError(
            f"{node_slug}: age-of-heroes events must not carry ac_year "
            f"(mythological dates are fan-extrapolated; use precision: era + leave ac_year null)"
        )

    # I7 — confidence cap: tertiary-fan source auto-caps at tier-3
    if basis_reliability == "tertiary-fan" and date_confidence is not None:
        tier = int(date_confidence.replace("tier-", ""))
        assert tier >= 3, \
            f"{node_slug}: tertiary-fan basis cannot yield date_confidence above tier-3 (got {date_confidence})"

    # I8 — precision must be a known enum value
    PRECISION_VALUES = {"exact", "year", "decade", "century", "era", "relative-only"}
    if precision is not None:
        assert precision in PRECISION_VALUES, \
            f"{node_slug}: precision '{precision}' not in allowed enum {PRECISION_VALUES}"

    # I9 — era: field inside occurred: must be the epoch enum, not AC/BC
    ERA_EPOCH_VALUES = {
        "pre-conquest", "age-of-heroes", "targaryen-conquest", "targaryen-rule",
        "dance-of-dragons", "roberts-rebellion", "current-narrative"
    }
    if node_era is not None:
        assert node_era in ERA_EPOCH_VALUES, \
            f"{node_slug}: occurred.era must be epoch enum (not 'AC'/'BC'), got '{node_era}'"
```

**Critical invariant summary (prose):**

- I1: `ac_year` is always int-or-null, never a string like `"283 AC"` or `"~283"`.
- I2: no `reckoning:` field — its presence is an error.
- I3: spans require both endpoints; end > start (signed).
- I4: `uncertainty_radius` and `ac_year_end` are mutually exclusive.
- I5: no naked dates — `basis_source` required whenever `ac_year` is non-null.
- I6: `age-of-heroes` nodes must leave `ac_year: null`.
- I7: `tertiary-fan` basis caps confidence at tier-3.
- I8: `precision` must be one of the six enum values.
- I9: if `era:` appears inside `occurred:`, it must be an epoch label, not `"AC"` or `"BC"`.

---

## 4. Should epoch `era:` coexist inside `occurred:`?

**Recommendation: YES — carry `era:` inside `occurred:` for event nodes that have an AC date, and leave it as a SEPARATE top-level field for non-event nodes.**

### Reasoning

The epoch `era:` field and the AC year are **complementary, not competing**:

- `era:` answers "which broad period?" — a coarse classifier useful for filtering and display.
- `ac_year:` answers "exactly when?" — precise, sortable, derivation-ready.

For event nodes they are tightly coupled: if you know `ac_year: 283`, the epoch is mechanically derivable (`roberts-rebellion`). Placing `era:` inside `occurred:` for events makes this derivable relationship explicit and keeps the two pieces of temporal evidence together in one block, which helps validators cross-check them (a `roberts-rebellion` event with `ac_year: 5` is a red flag).

**Is event-dating the right place to first populate `era:`?**

Yes — arguably the best place. The epoch `era:` was designed for event nodes in the first place (the SYNTHESIS schema already anticipates it); it just happened to be documented in a general frontmatter section. Event nodes that receive `occurred.ac_year` from deterministic Python extraction are also the nodes where the epoch is *most deterministic* (if `ac_year` is in range 282–283, epoch is `roberts-rebellion`, no reasoning needed). The first real population of `era:` can be a free byproduct of the dating pass.

**Implementation rule:** when the Python dating script writes `occurred.ac_year`, it also writes `occurred.era` (computed from the year range), AND writes `era:` at the top-level frontmatter as specified in architecture.md:438. The two values must agree; the validator (I9 above) catches any mismatch. For non-event nodes, `era:` stays at top level only (no `occurred:` block).

---

## 5. BC coverage gap — sourcing and deferral

**Given:** `chronology-events.jsonl` contains only `year_era = "AC"` across all 2,245 records. No BC values exist in that dataset. BC dates for deep-lore events (Doom of Valyria ≈114 BC, Long Night ≈8000 BC) must come from other sources.

### Sources for BC dates

| Source | What it covers | Reliability |
|---|---|---|
| Wiki infobox `Date:` cell (raw HTML in `sources/wiki/_raw/`) | Named events with a stated BC year (e.g., Doom page) | `wiki-year-page` → `tertiary-fan` |
| TWOIAF text (if in `sources/reference/`) | Historical/mythological events with year ranges | `secondary-source` |
| Year-page nodes (e.g., `114 BC`) | Events listed under a year page | `tertiary-fan` |
| Fan extrapolation / character-age inference | Long Night, Age of Heroes dates | **DO NOT MINT** — leave `ac_year: null` |

### Tiering rule for BC dates

Any BC date sourced from a wiki year-page or infobox is **at most tier-3** (`basis_reliability: tertiary-fan`). Any BC date that is mythological, age-inferred, or "commonly cited in fandom" (Long Night ~8,000 BC, Age of Heroes ~6,000 BC, etc.) **must not receive an `ac_year` value** — these are fan extrapolations from vague textual ranges and do not constitute cited fact. Set `precision: era` or `precision: relative-only` and leave `ac_year: null`.

### Should BC support ship in v1?

**YES — include the field and validator in v1, but populate it conservatively.**

The *schema* must support negative `ac_year` values from day one. Excluding negative integers from v1 would mean retrofitting the schema when the first BC event (Doom of Valyria) is dated — unnecessary churn. The validator rules above already handle negatives correctly.

**However:** the *population* of BC dates should be extremely conservative in v1. The Doom (≈114 BC) is the primary candidate — it has a stated wiki year, a dedicated year-page, and is not mythological. The Long Night and Age of Heroes events should be left `null` until there is an explicit, citable canon source (TWOIAF chapter, appendix, etc.) — not fandom consensus.

**Migration note:** no existing nodes need migration for the `ac_year` field (zero nodes carry any date field today). The schema is purely additive. The validator can be run immediately against the (empty) current corpus as a baseline.

**Sourcing note for BC first pass:** run `grep -r "BC" sources/wiki/_raw/` scoped to event-type pages to find explicitly stated BC years in wiki infoboxes. Do NOT use `chronology-events.jsonl` for BC lookup — it has no BC data and its mention-index model means absence ≠ undatable.

---

## Copy-paste fragment: reckoning block inside `occurred:`

This is the reckoning portion of the `occurred:` block, reflecting the signed-integer decision. Slot into the full `occurred:` schema from `2026-06-15-events-time-SYNTHESIS.md`:

```yaml
occurred:
  # ── IN-WORLD DATE AXIS ─────────────────────────────────────────────────────
  # ac_year: signed integer. Positive = AC (After Conquest). Negative = BC.
  # null is the correct value when the date is unknown or mythological.
  # NO separate reckoning/era field for AC vs. BC — the sign carries it.
  ac_year: 283              # e.g. Battle of the Trident: 283 AC → 283
  # ac_year: -114           # e.g. Doom of Valyria: 114 BC → -114
  # ac_year: null           # e.g. Long Night: DO NOT MINT a year — use precision: era

  ac_year_end: null         # SPAN endpoint only (wars, reigns). NOT for uncertainty.
                            # Must be > ac_year (signed). null for point events.

  uncertainty_radius: null  # ± years for a fuzzy single-point estimate.
                            # MUTUALLY EXCLUSIVE with ac_year_end.

  precision: year           # exact | year | decade | century | era | relative-only

  basis_source: wiki-year-page
                            # narrative-prose | appendix | twoiaf |
                            # wiki-year-page | inferred
  basis_reliability: tertiary-fan
                            # primary-source | secondary-source |
                            # tertiary-fan | inferred-only
  date_confidence: tier-3   # tertiary-fan auto-caps at tier-3

  era: roberts-rebellion    # Epoch label (epoch enum, NOT "AC"/"BC").
                            # Derivable from ac_year range; validator cross-checks.

  dispute: null             # Populated ONLY when ≥2 competing canon dates exist.
  # dispute:
  #   ac_year: 281
  #   basis_reliability: inferred-only
  #   notes: "GRRM-acknowledged inconsistency"

  # ── NARRATIVE AXIS ─────────────────────────────────────────────────────────
  narrative_first: "agot-3" # {book}-{chapter_number}: earliest reader encounter
                            # (min across the event's edges). Tier-1; nearly free.
```

---

## Bottom line

`era: AC|BC` is disqualifying because `era:` is an existing documented field with the meaning "narrative epoch" — adding a second meaning would silently corrupt every future event mint. The correct field is **`ac_year` (signed integer, negative = BC)** inside the `occurred:` block: no separate reckoning field, no mirroring of the data layer's flat `year_value`/`year_era` split, because a signed integer is unambiguous, sort-correct, and eliminates the drift surface that a two-field string reckoning creates. BC dates should be included in the v1 schema (negative integers are immediately supportable) but populated conservatively — only explicitly wiki-stated values, never fan-extrapolated mythological timescales; the `age-of-heroes` validator guard enforces this mechanically.
