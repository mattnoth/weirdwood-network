# Era Field Research Dossier
**Produced:** 2026-06-16  
**Purpose:** Factual evidence only — no recommendations. Determines whether `era:` and related time/date fields already exist before adding an `occurred:` frontmatter block with AC/BC year reckoning.

---

## 1. `era` in architecture.md (case-insensitive grep)

**File:** `reference/architecture.md`

All hits with line numbers:

- **Line 38:** (table header context — contains "extensible" / "Event entities" prose — `era` appears inside the word "literature" — NOT a relevant hit)
- **Line 83:** prose mention of "Event entities" — `era` appears as substring in `iterate`, `rework` etc. — irrelevant substring hits
- **Line 426:** (section header status note)
  > `> **Status (Session 86, 2026-06-08):** documented. \`era:\` is forward-only — NOT backfilled retroactively. Existing 7,000+ nodes do not need an \`era\` field; new mints stamp it at creation.`
- **Line 438:** (field table row)
  > `| \`era\` | Optional, forward-only. The narrative epoch this entity belongs to. Set on new mints; NOT backfilled. The narrowing function in \`scripts/plate4-wiki-cluster.py\` weights \`era=current-narrative\` higher when classifying current-narrative mints, suppressing false-positive matches against pre-series events. | \`current-narrative\` |`
- **Line 441:** `### \`era:\` enum values`
- **Lines 444–456:** full enum block (see §6 below for complete text)
- **Line 545:** (spoiler-gating section) — `era` appears as substring in "ADWD-era references" — not a field reference
- **Line 623:** (vocab changelog) — `era` appears as substring in "Sonnet-era" in a parenthetical — not a field reference

**Is there an `era:` frontmatter FIELD defined?** YES — explicitly defined at `reference/architecture.md:438` in the Node Frontmatter Conventions table.

**What does it mean?** Narrative epoch (historical period) — one of seven enum values from `pre-conquest` to `current-narrative`. It classifies WHEN an entity belongs in in-world history.

**"Forward-only / not backfilled retroactively" phrasing — what field does it attach to?**

The exact "forward-only" language attaches to `era:`, NOT to `first_available`. Two locations:

- `reference/architecture.md:426`: `"era:" is forward-only — NOT backfilled retroactively.`
- `reference/architecture.md:438`: `"Optional, forward-only. The narrative epoch this entity belongs to. Set on new mints; NOT backfilled."`

`first_available` has its own separate deferral language at lines 439 and 513–515: *"DEFERRED to post-first-release backfill"* — a different rationale (release timing), not the forward-only language.

---

## 2. `era:` as frontmatter in node files

**Command run:** `grep -rn "^era:" graph/nodes/` and full frontmatter-block scan via Python.

**Result: 0 nodes carry `era:` in their YAML frontmatter block.**

The Python scan confirmed: of all `.node.md` files under `graph/nodes/`, none have `^era:` in the block between the opening and closing `---` delimiters.

The 4 files returned by `grep -rl "era:" graph/nodes/` all contain `era` in body text (prose quotes, not frontmatter):
- `graph/nodes/customs/walk-of-atonement.node.md:38` — contains "era" as substring in prose quote
- `graph/nodes/locations/northern-mountains.node.md:46` — "era" substring in Meera's name in dialogue
- `graph/nodes/events/tourney-at-harrenhal.node.md:114` — "era" substring in prose quote
- `graph/nodes/characters/alys-turnberry.node.md:53` — "era" substring in dialogue attribution

**Summary: `era:` is documented in architecture.md but has ZERO actual instances in the node corpus. The field was introduced at Session 86 (2026-06-08) as forward-only; no mints since then have stamped it.**

---

## 3. Spoiler-gating / `first_available`

**`first_available` documentation locations:**

- `reference/architecture.md:24` (chapter-file section): `"D&E novellas use \`collection: tales-of-dunk-and-egg\` in frontmatter and \`first_available: pre-agot\` for spoiler gating"`
- `reference/architecture.md:151`: `"- \`first_available\` — spoiler gate"`
- `reference/architecture.md:439` (frontmatter table): `"| \`first_available\` | Optional. Spoiler gating field — DEFERRED to post-first-release backfill (see Spoiler Gating section below). | \`"AGOT Bran II"\` |"`
- `reference/architecture.md:488` (edge metadata table): `"| \`first_available\` | Spoiler gate — earliest book/chapter where this is known | \`AGOT Jaime I\` |"`
- `reference/architecture.md:513–515` (Spoiler Gating section): `"Spoiler gating via \`first_available\` is **deferred** to a post-first-release backfill pass. The field is **optional** in v1 nodes."`

**Does `first_available` use the word "era" anywhere in its definition or values?** NO.

`first_available` values are formatted as `AGOT Bran II`, `ASOS Epilogue`, `pre-agot` — book/chapter identifiers, not era names. The word "era" does not appear in any `first_available` definition, value example, or surrounding prose (verified by grep). The two fields are semantically and textually distinct.

---

## 4. Code that reads/writes/validates `era`

**Scripts grep (`grep -rn -i "\bera\b" scripts/`):**

Relevant hits only (substring false positives filtered):

- `scripts/stage4-haiku-run.py:196,226,271,273,279,281,284,287` — uses "Sonnet-era" as a human-readable label for the pre-Haiku batch of prompts; `era` here is an English word in comments/strings, NOT a field read/write.
- `scripts/wiki-infobox-parser.py:1018`: comment `# title= attribute forms: year-anchor pages and era names` — refers to in-wiki era name strings (e.g., "Age of Heroes") being detected as date anchors. Not reading an `era:` frontmatter field.
- `scripts/wiki-infobox-parser.py:1031`: comment `# Pattern A: basic year/era with optional AC/BC (e.g. "263 AC", "37", "Dawn Age")` — same: pattern matching wiki anchor text.
- `scripts/wiki-infobox-parser.py:1256`: comment `# Match "Place, <date>" where date is year/era at end of string` — same context.
- `scripts/wiki-pass2-repromote-targeted-2.py:89`: comment `# Date-only targets: year strings, era names` — same: identifying date-bleed patterns in edges, not reading `era:` frontmatter.
- `scripts/classify-comention-candidates.py:107`: comment `# obscure Harrenhal-era reference` — natural English usage.

**No script reads or writes `era:` as a frontmatter key-value pair.** The `scripts/plate4-wiki-cluster.py` file is named in architecture.md:438 as the consumer of `era=current-narrative`, but inspection of that file shows zero references to `era` as a dictionary key — the only `era`-containing line is `enumerate` in a loop. The stated narrowing function consuming `era:` either has not been implemented yet or the script's era logic is implicit elsewhere.

**Tests grep (`grep -rn -i "\bera\b" tests/`):** Zero hits — no test file references `era` as a field.

---

## 5. Existing AC/BC reckoning storage

**`working/wiki/data/chronology-events.jsonl`:**

Fields confirmed from inspection:
```
year_page    — string: "1 AC", "4 AC", etc.
year_value   — integer: 1, 4, 9, etc.
year_era     — string: the era suffix
target_page  — string: wiki page name
target_slug  — string: kebab slug
target_type  — string: entity type
anchor_text  — string
snippet      — string: raw HTML snippet
```

`year_era` vocabulary (exhaustive): **`{"AC"}`** — only `AC` values appear in all 2,245 records. No `BC` values present in this file (the file covers post-Conquest years; BC events may simply not have chronology wiki pages, or they were not scraped).

**`working/wiki/data/infobox-data.jsonl`:** Fields are `page`, `entity_type`, `first_available`, `books`, `relationships`, `aliases`, `cite_refs`. No year, era, AC, BC, date, or born/died fields at the record level (those are embedded inside the `relationships` sub-structure if present). Confirmed: 4,786 records, no top-level time-related key.

**Year-page node (`graph/nodes/characters/283-ac.node.md`):**  
The node was created by the Python promotion pass as `type: character.human` (a misclassification — year pages fell into the character bucket). Its frontmatter:
```yaml
name: "283 AC"
type: character.human
slug: 283-ac
aliases: []
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/283_AC"
bucket_id: tier3-characters
prompt_version: v1-python
node_version: 1
pass_origin: pass2-wiki-deterministic
```
No `era:`, `year:`, `year_value:`, `year_era:`, `occurred:`, or any date field. The AC/BC reckoning is embedded only in the `name` string itself.

**Other AC/BC storage locations found:**
- `working/wiki/data/chronology-events.jsonl` — the canonical machine-readable year data; uses `year_value` (int) + `year_era` (string `"AC"`) as separate fields.
- `scripts/wiki-infobox-parser.py` — regex patterns parse `"263 AC"`, `"37 BC"` strings from wiki infobox HTML but do NOT emit them into edge or node files as structured fields. They are used only to filter out date-bleed (edges that accidentally pointed to a year string instead of a named entity).

---

## 6. Other time/date fields already in the schema

**`reference/architecture.md` — documented frontmatter fields table (lines 430–439):**

| Field | Status | Meaning |
|-------|--------|---------|
| `era` | Optional, forward-only | Narrative epoch enum: `pre-conquest`, `age-of-heroes`, `targaryen-conquest`, `targaryen-rule`, `dance-of-dragons`, `roberts-rebellion`, `current-narrative` |
| `first_available` | Optional, DEFERRED | Spoiler gate — earliest book/chapter (format: `AGOT Bran II`) |

**`reference/architecture.md` — edge metadata fields (lines 483–493):**

| Field | Meaning |
|-------|---------|
| `temporal` | When the edge is active: `"until ASOS"`, `"during Robert's Rebellion"` |
| `first_available` | Spoiler gate on edges |

**Entity type table — `date` as an attribute (not a frontmatter field) (lines 108–119):**  
Multiple event subtypes list `date` as a conceptual attribute in the type-reference table column "Attributes": `event.battle`, `event.tournament`, `event.wedding`, `event.feast`, `event.coronation`, `event.trial`, `event.assassination`, `event.execution`, `event.deception`, `event.incident`. This is documentation of the semantic concept, NOT a standardized frontmatter key — actual node files do not carry a `date:` frontmatter field.

**Node frontmatter grep across `graph/nodes/` for date/year/time keys:**  
Grep for `^date:`, `^year:`, `^ac_year:`, `^reckoning:`, `^chronology:`, `^occurred:`, `^when:`, `^timeline:` → **zero hits** across all node files. None of these are live frontmatter fields in any current node.

**`era:` enum values (architecture.md:444–456):**
```
era: pre-conquest | age-of-heroes | targaryen-conquest | targaryen-rule
    | dance-of-dragons | roberts-rebellion | current-narrative
```
These are coarse narrative-epoch classifiers, NOT AC/BC calendar years.

---

## 7. architecture.md frontmatter conventions section — where to amend

**Section header:** `## Node Frontmatter Conventions` at `reference/architecture.md:424`

**Status note at line 426** (must be updated when adding fields):
> `> **Status (Session 86, 2026-06-08):** documented. \`era:\` is forward-only — NOT backfilled retroactively. Existing 7,000+ nodes do not need an \`era\` field; new mints stamp it at creation.`

**The field table (lines 430–439) is the amendment target.** A new `occurred:` field would be inserted here as a new row. The table currently has 8 fields: `name`, `slug`, `type`, `aliases`, `confidence`, `wiki_source`, `era`, `first_available`.

**Stated rules about adding new frontmatter fields:** The `## Node Frontmatter Conventions` section itself contains no explicit amendment protocol. The parallel rule exists for edge types (architecture.md:630): *"Adding a new edge type: append a row to the appropriate `## Edge Types` subsection FIRST."* No equivalent "Adding a new frontmatter field" rule is written. The closest statement is the section status note (line 426), which logs the session that established the convention.

**`era:` enum values subsection (lines 441–456):** The `occurred:` field (if it carries AC/BC integers or strings) would require a parallel `### occurred: format` subsection documenting value format — the `era:` enum block provides the precedent pattern.

---

## Raw facts summary

- **`era:` IS a documented frontmatter field** — defined at `reference/architecture.md:438` in the Node Frontmatter Conventions table. It means narrative epoch (historical period), NOT AC/BC calendar year. Enum: `pre-conquest | age-of-heroes | targaryen-conquest | targaryen-rule | dance-of-dragons | roberts-rebellion | current-narrative`.

- **The "forward-only / not backfilled retroactively" phrasing attaches to `era:` at architecture.md:426 and :438** — NOT to `first_available`. `first_available` has its own separate deferral language ("DEFERRED to post-first-release backfill") at architecture.md:513.

- **`era:` appears as a frontmatter field on ZERO live nodes** — 0 instances in `graph/nodes/` (confirmed by Python scan). Documented at Session 86 (2026-06-08); no mints since have stamped it.

- **No script reads or writes `era:` as a structured field** — `plate4-wiki-cluster.py` is named as the consumer but has no `era`-as-key code present. All other script hits are natural-English uses or regex comments.

- **`chronology-events.jsonl` stores `year_era ∈ {"AC"}` (only AC present in all 2,245 records)** alongside `year_value` (int) as separate fields. BC values are absent from this dataset.

- **No `occurred:`, `date:`, `year:`, `ac_year:`, `reckoning:`, `chronology:`, `when:`, or `timeline:` field exists** anywhere in node frontmatter or architecture.md's frontmatter table. The concept of `date` appears in the entity-type attribute column as documentation only.

- **The `era:` enum vocabulary is a naming collision risk** for a proposed field intended to carry `AC | BC` — the word `era` is taken, with a completely different semantic (epoch label, not calendar reckoning). `year_era` is already used in `chronology-events.jsonl` with exactly the AC/BC meaning.

- **Section to amend for `occurred:`:** `reference/architecture.md:424–439` (the Node Frontmatter Conventions table). No written amendment protocol exists for frontmatter fields (only for edge types at architecture.md:630). The status note at line 426 logs the owning session.
