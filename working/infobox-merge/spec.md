# Infobox-Merge Specification — Promoting the Wiki Infobox Layer into `graph/edges/edges.jsonl`

> **Status:** SPEC v2 — written 2026-06-11, revised 2026-06-12 after adversarial fresh-eyes review
> (verdict: ACCEPT-WITH-FIXES; all required fixes applied — see `## Changelog`). Greenlit by Matt per
> `working/audits/fable-audit-2026-06-11/synthesis.md`. Implementation target: `scripts/infobox-merge.py`,
> dry-run only tonight. **No writes to `graph/` until Matt reviews the dry-run report.**
>
> Every count in this spec was computed by running the rules below as throwaway Python in
> `/tmp/infobox-merge-analysis/` against the live repo (v1 rules 2026-06-11; v2 rules recomputed
> 2026-06-12, with the v1 numbers reproduced exactly first as a regression check). The pipeline is
> fully deterministic — the implementation's dry-run counts must match these numbers EXACTLY (same
> inputs, same rules). Any deviation means the implementation diverged from this spec; explain or fix
> before Matt review.
>
> Recommended model for implementation: **Sonnet** (pure Python translation of a fully-specified
> rule set; no open reasoning).

---

## 1. What this is, in plain language

### Where the data came from

In April we crawled the entire AWOIAF wiki once (17,945 pages) into `sources/wiki/_raw/`. The script
`scripts/wiki-infobox-parser.py` then read every cached page and pulled apart its **infobox** — the
structured fact-table in the top-right corner of every wiki article (Title / Allegiance / Father /
Mother / Spouse / Born / Died / Seat / Overlord / ...). For each infobox field it recognized, the
parser's `FIELD_EDGE_MAP` dict translated the field name into one of the project's locked edge types
(`Allegiance` → `SWORN_TO`, `Father` → `PARENT_OF`, `Seat` → `SEAT_OF`, ...) and recorded the field's
link targets. The output is `working/wiki/data/infobox-data.jsonl`: **4,786 pages, 20,614 relationship
rows, already typed to 23 edge types** from the master vocabulary. It has been sitting there, finished,
since April. It was rendered into the node files' `## Edges` display bullets, but **never promoted into
the canonical edge file** `graph/edges/edges.jsonl` — which is why 85% of graph nodes have no edges
while the data that would connect them is already parsed on disk.

### What a raw row looks like

Two real rows from `infobox-data.jsonl` (each page is one JSON line; `relationships` is the row list):

```json
{"page": "Abelar Hightower", "entity_type": "character.human", "relationships": [
  {"field": "Title", "target": "Ser", "edge_type": "HOLDS_TITLE", "direction": "forward"},
  {"field": "Allegiance", "target": "House Hightower", "edge_type": "SWORN_TO", "direction": "forward"},
  {"field": "Culture", "target": "Reach", "edge_type": "CULTURE_OF", "direction": "forward"},
  {"field": "Born", "target": "Hightower", "edge_type": "BORN_AT", "direction": "forward"},
  {"field": "Born", "target": "Oldtown", "edge_type": "BORN_AT", "direction": "forward"}], "cite_refs": {}}
```

```json
{"page": "Jon Snow", "entity_type": "character.human", "relationships": [
  {"field": "Title", "target": "Lord Commander of the Night's Watch", "edge_type": "HOLDS_TITLE", "direction": "forward"},
  {"field": "Allegiances", "target": "House Stark", "edge_type": "SWORN_TO", "direction": "forward"},
  {"field": "Allegiances", "target": "Night's Watch", "edge_type": "SWORN_TO", "direction": "forward"},
  {"field": "Culture", "target": "Northmen", "edge_type": "CULTURE_OF", "direction": "forward"},
  {"field": "Father", "target": "Eddard Stark", "edge_type": "PARENT_OF", "direction": "reverse"},
  {"field": "Mothers", "target": "Wylla", "edge_type": "PARENT_OF", "direction": "reverse", "qualifier": "supposedly"},
  {"field": "Mothers", "target": "Ashara Dayne", "edge_type": "PARENT_OF", "direction": "reverse", "qualifier": "rumored"},
  {"field": "Lover", "target": "Ygritte", "edge_type": "LOVER_OF", "direction": "symmetric"}],
 "cite_refs": {"agot": [1, 2, 3, 5, "..."], "adwd": [0, 3, 7, "..."]}}
```

Note three things that drive the whole rule set:

- **Targets are display strings, not slugs.** "House Hightower" must be resolved to the node slug
  `house-hightower` before an edge can exist. That's the resolution ladder (Rule 2/4).
- **`direction` says which side of the edge the page is on.** Jon's page lists his *Father*; the edge
  runs the other way (`eddard-stark PARENT_OF jon-snow`), hence `"reverse"`.
- **The wiki encodes rumor.** Jon's infobox lists TWO "Mothers" — Wylla *(supposedly)* and Ashara Dayne
  *(rumored)*. Naive promotion would mint two false `PARENT_OF` edges and graph-canonize R+L=J's
  biggest red herrings. These rows get **quarantined**, not merged and not deleted (Rule 3).

### What "promotion" means, concretely

Each surviving row becomes one JSONL line appended to `graph/edges/edges.jsonl`, in the canonical edge
schema (section 4). Four real before/after examples from the computed run:

| # | Raw infobox row | Merged edge |
|---|---|---|
| 1 | `Abelar Hightower` · field `Allegiance` · target `House Hightower` · SWORN_TO · forward | `abelar-hightower --SWORN_TO--> house-hightower` |
| 2 | `Walder Frey` · field `Issue` · target `Roslin Frey` · PARENT_OF · forward | `walder-frey --PARENT_OF--> roslin-frey` (one of 29 children listed; 23 merge — the other 6 quarantine as mirrors of the wiki's Black-Walder-fathered-them rumor, Rule 3e) |
| 3 | `Acorn Hall` · field `Ruler` · target `Theomar Smallwood` · RULES · forward | `theomar-smallwood --RULES--> acorn-hall` (**direction-corrected** — see Rule 7; the map's `forward` would have emitted the castle ruling the man) |
| 4 | `House Stark` · field `Seat` · target `Winterfell` · SEAT_OF · reverse | `winterfell --SEAT_OF--> house-stark` (map's `reverse` honored as-is; matches architecture's Location → House) |

Every merged edge is **Tier 2, never Tier 1** — Tier 1 is earned by verbatim book quotes, and an
infobox row has no quote. Every merged edge carries `evidence_kind: wiki-infobox`,
`typed_by: python-infobox-map`, and cites `wiki:<Page_Name>`.

**On cite_ref chapter anchors:** the requirement was to carry per-row chapter anchors where the infobox
row has them. Computed fact: **rows do not carry them** — the parser strips `<sup>` citation markers
when extracting field values, so chapter anchors survive only at *page* level (the `cite_refs` dict,
e.g. Jon's `{"agot": [1,2,3,...]}`). Page-level anchors are not row evidence (Eddard's page cites 70+
chapters; attaching all of them to `eddard-stark SPOUSE_OF catelyn-tully` would be noise dressed as
precision). So v1 merged edges cite `wiki:<Page>` only. If per-row anchors are ever wanted, the path is
a targeted re-parse of the infobox `<td>` HTML keeping `<sup>` ids — logged as a possible follow-up,
not part of this merge.

---

## 2. The promotion rule set

The script processes all 20,614 rows through these rules **in this order**. Every row ends in exactly
one bucket: **MERGED**, **FILTERED** (mechanical noise — logged, never promotable as-is), or
**QUARANTINED** (real signal the graph must not assert — logged for later curation). Nothing is
silently dropped; the dry-run report accounts for all 20,614.

### Rule 0 — Row universe

Input: every object in every page's `relationships` array in `working/wiki/data/infobox-data.jsonl`.
Count: **20,614 rows across 4,786 pages** (4,663 pages have ≥1 row).

### Rule 1 — Source resolution (the page itself must be a node)

Resolve the wiki page name through the **resolution ladder** (defined once, used for both endpoints):

1. **exact, parens kept** — slugify keeping parenthetical disambiguators:
   `Aegon Frey (son of Stevron)` → `aegon-frey-son-of-stevron`. Tried FIRST because node slugs were
   minted from page names with disambiguators kept; there are **215 pages** where the parens-stripped
   form is *also* a node (a different person — `aegon-frey` exists too). Stripping first would
   silently attach a minor Frey's children to the wrong Aegon.
2. **exact, parens stripped** — standard `kebab()` (the `orphan-edges-audit.py` implementation:
   lowercase, strip `[...]`/`(...)`, apostrophes removed, non-alphanumeric → `-`).
3. **alias-resolver** — look up either slug form in
   `working/wiki/data/alias-resolver.json :: alias_to_canonical` (1,433 entries); accept only if the
   canonical slug is an existing node.
4. **leading-article strip** — if the slug starts with `the-`, try the remainder as an exact node
   match (`The Citadel` → `citadel`). Exact-match-only after the strip; no fuzzy. *Note:* this
   deliberately supersedes the alias-resolver's `alias_collisions` conservatism for pure
   `the-`-variants (`the-wall` is marked "ambiguous-do-not-resolve" there despite having exactly one
   candidate) — flagged as open question 6.
5. **unresolved** → the row is FILTERED as `source-unresolved` and logged.

Slugify must be byte-identical to `kebab()` in `scripts/orphan-edges-audit.py` (which matches the
pass2 emit convention). Node universe = `graph/nodes/**/*.node.md` filename stems, excluding
`_conflicts/` and `_unclassified/`.

- **ACCEPTED:** page `Abelar Hightower` → `abelar-hightower` (rung 1/2, exact). All 5 rows proceed.
- **FILTERED:** page `A Song of Ice and Fire` (the real-world novel — never promoted to a node, so no
  slug exists) → its `WRITTEN_BY → George R. R. Martin` row is filtered. This is the *intended* fate
  of out-of-world pages: node non-existence is the gate. Only **3 rows** in the whole dataset fail
  here (all real-world ASOIAF publications), because rung 1 resolves the 345 disambiguated-character
  rows that a naive slugify misses (counted over rows passing Rule 4: page has parens, parens-kept
  slug is a node, parens-stripped slug is not — v1 said 351, measured under a superseded rung
  ordering; corrected, see changelog).
- **QUARANTINED:** n/a — source resolution filters or passes; it never quarantines.

### Rule 2 — Noise-target filter

Before resolving the target, discard targets that are placeholders, not entities. Three sub-filters
(case-insensitive, on the whole target string, NBSP-normalized):

- **2a placeholder words:** `Unknown`, `None`, `Extinct`, `Unborn`, `N/A`, `Various`, `Several`,
  `Many`, `Disputed`, `Vacant`, `Defunct`, `Dead`, `Deceased`, `Abandoned`, `Uninhabited`, `Mixed`,
  `Uncertain`, `Unnamed`, `Issue` — **412 rows**.
- **2b bare kinship words:** regex over optional count/state prefix + kinship noun —
  `(a|an|two|three|...)? (unborn|deceased|stillborn|bastard)? (son(s)|daughter(s)|child(ren)|brother(s)|sister(s)|mother(s)|father(s)|wife|wives|husband(s)|nephew(s)|niece(s)|cousin(s)|grandson(s)|granddaughter(s)|uncle(s)|aunt(s))` —
  catches `Son`, `Two sons`, `A daughter` — **204 rows**.
- **2c pure numerals/dates:** `^\d[\d\s,–—-]*(AC|BC)?$` — **0 rows** today (the parser's date-bleed
  fix already strips these from Born/Died); kept as a defensive guard.

Total filtered here: **616 rows = 3.0% of input** (the audit's "~2.5%" estimate, measured precisely).

- **ACCEPTED:** `Walder Frey` · `Issue` · `Roslin Frey` — a real named child, passes untouched.
- **FILTERED:** `Aerys I Targaryen` · `Issue` · `None` (2a — the wiki recording childlessness, not a
  child named None); `Alyn Tarbeck` · `Issue` · `Son` (2b — an unnamed son with no page; nothing to
  link to).
- **QUARANTINED:** n/a — placeholders carry no salvageable claim; this rule only filters.

### Rule 3 — Speculative-kinship quarantine (the Jon Snow rule) — **quarantines by FACT KEY, not row**

Kinship is where the wiki encodes *rumor with a straight face*, and where a false edge does the most
damage. Kinship fields = `{father, fathers, mother, mothers, spouse, spouses, lover, lovers, issue,
heir, heirs}`.

**The v2 core principle (critic finding 1, CRITICAL):** the wiki encodes kinship *bidirectionally* —
Joffrey's page says `Fathers: Robert (legally) / Jaime (biologically)` while Robert's page says
`Issue: Joffrey (legally)` and Jaime's says `Issue: Joffrey` (unqualified). Per-row quarantine (v1)
caught Joffrey's side and let the mirror rows merge — and since `legally` was not in the PARENT_OF
qualifier map, the default would have graph-canonized `robert-i-baratheon PARENT_OF
joffrey-baratheon` as **`biological`** at Tier 2. So in v2 the unit of quarantine is the **fact key**:

> **Fact key** = `(semantic relation class, unordered endpoint pair)` of the *resolved* slugs.
> Relation classes: `PARENT` (asserted by `Father`/`Fathers`/`Mother`/`Mothers`/`Issue` rows — all
> five fields assert the same parentage fact, regardless of which page carries the row or which
> direction it materializes; there is no CHILD_OF), `SPOUSE` (`Spouse`/`Spouses` in either
> direction assert the same marriage), `LOVER` (`Lover`/`Lovers`), `HEIR` (`Heir`/`Heirs`).
> **If any row asserting fact key K trips 3a–3d, ALL rows asserting K are quarantined** (rule 3e).

Triggers (any one quarantines the row, and via 3e its whole fact):

- **3a — plural parent field:** field name is `Mothers` or `Fathers`. The wiki only pluralizes
  parentage when it is presenting *competing claims*. All rows in the field quarantine. **46 rows.**
- **3b — multi-value singular parent field:** a single page has >1 distinct (non-noise) target under
  singular `Father` or `Mother`. Uniqueness-expected field with two values = the wiki hedging. All
  rows in that (page, field) quarantine. **8 rows.**
- **3c — speculative/hedge qualifier on a kinship field:** qualifier matches (v2-widened — the seven
  additions are all verified present in the data and escaped the v1 regex; critic finding 2):
  `\b(rumored|rumoured|supposedly|supposed|alleged(ly)?|possibly|reportedly|officially|legally|`
  `unconfirmed|presumably|debated|dubious canonicity|in some tales)\b` (NBSP-normalized before
  matching). **102 rows** (86 v1 + 16 newly caught, e.g. `Robert I Baratheon` · `Issue` · Joffrey/
  Myrcella/Tommen *(legally)*, Dreamfyre's *(unconfirmed)* clutch, Nettles/Daemon *(debated)*).
  Note: `officially`/`legally` are hedges *here* because an infobox only reaches for them when the
  bare claim is contested; `biologically` is deliberately NOT in the set (it asserts the non-hedged
  side of a competing claim — those rows quarantine via 3a/3b/3e instead).
- **3d — `disputed` on a kinship field whose edge type is not PARENT_OF (policy, critic finding 2):**
  PARENT_OF's locked qualifier enum contains `disputed`, so a disputed parentage row can merge
  *visibly flagged* (e.g. `jonos-bracken PARENT_OF harry-rivers`, qualifier `disputed`). The other
  kinship types cannot carry the flag — HEIR_TO's enum FORBIDS qualifiers, SPOUSE_OF/LOVER_OF's enums
  lack `disputed` — so a disputed row would merge *bare*, i.e. unflagged. Policy: those rows
  quarantine. **5 rows** (Balon Greyjoy's two disputed heirs, `Lord of Storm's End` · heir ·
  Myrcella *(disputed)*, Shireen *(disputed by Shireen Baratheon)*, Marilda of Hull · lovers ·
  Laenor *(disputed)*).
- **3e — mirror of a quarantined fact (the fact-key closure; critic finding 1):** the row itself is
  clean, but another row asserting the same fact key tripped 3a–3d. **24 rows.** Evaluated after
  Rule 4 (it needs both endpoints resolved); the implementation builds the quarantined-fact-key set
  in a pre-pass over all rows tripping 3a–3d (resolving their endpoints; rows whose endpoints don't
  both resolve contribute no key). The full verified list: Robert's and Jaime's `Issue` mirrors of
  the three Lannister-incest children quarantine via 3c/3e (Cersei's rows, with no competing claim, pass Rule 3 untouched — they end as
  Rule-10 corroborations of her existing Tier-1 book edges); `Ramsay Snow` · `Spouses` · `Arya Stark` (unqualified — mirror of Arya's
  *(allegedly)* row; per the project's impersonation-edges rule that marriage belongs on
  jeyne-poole, whose unqualified rows DO merge); Laenor Velaryon's 5 `Issue (disputed)` rows
  (mirrors of his legal children's 3a `Fathers` rows); Walder Frey's 6 `Issue` rows for Annara
  Farring's children (mirrors of their 3a `Fathers: Walder (officially) / Black Walder (rumored)`);
  Aegon IV's `Issue` mirrors of Daeron II / Viserys Plumm / Jeyne Lothston; plus Ossifer Plumm,
  Quentyn Ball, Alys Rivers, Raymont Baratheon, Petyr Frey, Lyman/Loren Lannister-class mirrors.

**Ordering note:** 3a–3d fire before target resolution (Rule 4); 3e fires immediately after it.
Because all of Rule 3 precedes Rule 10, **5 rows that v1 logged as corroborations of existing
book edges now quarantine instead** (e.g. `Jaime Lannister` · `Issue` · `Joffrey Baratheon`,
`Ramsay Snow` · `Spouses` · `Arya Stark`) — correct: a leak of a quarantined fact must not be
blessed as "corroboration" either.

**The canonical example — Jon Snow's two mothers.** His infobox `Mothers` field lists Wylla
*(supposedly)* and Ashara Dayne *(rumored)*. Both rows trip 3a AND 3c, and their fact keys
quarantine any mirror rows elsewhere. If merged, the graph would assert `wylla PARENT_OF jon-snow`
and `ashara-dayne PARENT_OF jon-snow` as Tier-2 facts — two false edges, both famous in-world
misdirections. Quarantined instead: preserved in `working/infobox-merge/quarantined.jsonl` with full
context, available to a future curator pass that could promote them as Tier 4 `PARENT_OF` with
qualifier `rumored` *as explicitly-flagged rumor* — that's an agent-reasoning decision, not a
bulk-script decision.

- **ACCEPTED:** `Eddard Stark` · `Father` · `Rickard Stark` (single value, no speculative qualifier,
  fact key untainted) → `rickard-stark PARENT_OF eddard-stark`. Also `Cersei Lannister` · `Issue` ·
  `Joffrey Baratheon` passes Rule 3 (her motherhood is uncontested — only the fathers' fact keys are
  tainted), though it ultimately lands in Rule 10's corroboration log, not the merge.
- **FILTERED:** n/a — this rule only quarantines.
- **QUARANTINED:** Jon's two Mothers rows (above); `Addam Velaryon` · `Fathers` · Laenor *(officially)*
  / Corlys *(rumored)* (3a); `Benedict I Justman` · `father` · `Blackwood` AND `Bracken` (3b — the
  legend says one of the two feuding houses); `Aegon IV Targaryen` · `lovers` · `Elaena Targaryen`
  *(rumored)* (3c); `Balon Greyjoy` · `heir` · `Theon Greyjoy` *(disputed)* (3d); `Jaime Lannister` ·
  `Issue` · `Joffrey Baratheon` (3e — clean row, tainted fact).

Deliberately NOT quarantined: plural `Spouses` with multiple values (Walder Frey's 8 wives are
sequential marriages, fact not rumor); political qualifiers like `claimant`/`disputed` on titles
(legitimate contested-claim data, kept as qualifier — see Rule 11); and `disputed` on PARENT_OF
*when no competing claim taints the fact key* (merges with enum qualifier `disputed` — e.g.
Aegon IV's disputed Otherys bastards, where the wiki offers no rival father).

### Rule 4 — Target resolution ladder

Same ladder as Rule 1, applied to the target string. Unresolved targets are FILTERED as
`target-unresolved` and logged (skip-and-log — never guess). **507 rows filtered.**

- **ACCEPTED (each rung):** exact: `House Hightower` → `house-hightower`; alias:
  `Stormlander` → alias-resolver → `stormlanders` (this answers the culture-string question — the
  alias layer already canonicalizes most demonym variants); the-strip: `The Citadel` → `citadel`
  (77 maester `SWORN_TO` rows recovered by one rung).
- **FILTERED:** `Aelyx Targaryen` · `Father` · `Aerys Targaryen` — bare "Aerys Targaryen" is not a
  node (only `aerys-i-targaryen` / `aerys-ii-targaryen` exist) and not a registered alias —
  resolving it would require choosing a king, so: skip and log. Also `Queen consort`,
  `Prince Regent` (title strings with no title node).
- **QUARANTINED:** n/a — unresolvable means unmergeable; nothing to quarantine.

**Culture-string decision (locked):** `CULTURE_OF` targets resolve through the same ladder, no special
casing. Where the culture exists as a node (`northmen`, `rivermen`, `stormlanders` via alias,
`valyrian`, `andals` via alias) the edge merges. Where the wiki used a *region name* as the culture
(`Reach`, `Crownlands` — 927 rows resolve to location nodes), the edge merges with the location as
target: type-impure but information-preserving, and exactly what "which characters are from the
Reach?" needs. Where nothing resolves (`Dornish` ×14, `Sarnori`, `Myrhish` typo) → filtered by this
rule. Demonym normalization (minting `reachmen`/`crownlanders` culture nodes and retargeting) is
flagged as optional follow-up, open question 4.

### Rule 5 — Deterministic retypes (sanctioned by architecture.md)

Two field→type mappings in the parser are context-blind; architecture.md already documents the
correct context-split. The script applies them deterministically from the resolved **source node's
category** (its `graph/nodes/<dir>/`):

- **5a `FIGHTS_IN` → `PART_OF`** when the source is an `events/` node. The `Conflict` field on a
  *battle* page names its containing *war*; architecture: "Conflict (on a war page's battle list) →
  PART_OF — battle → war containment." **184 rows retyped** (e.g. battle pages of the Dance →
  `PART_OF` `dance-of-the-dragons`). Characters' `Conflict`/`Battles` rows stay `FIGHTS_IN` (person →
  battle). Only 4 `FIGHTS_IN` rows survive with non-character sources (3 texts, 1 faction) — review
  at dry-run, see Known residuals.
- **5b `WORSHIPS` → `RELIGION_OF`** when the source is a `locations/` node. Architecture's infobox
  table: "Religion → WORSHIPS for characters; RELIGION_OF for locations." **93 rows retyped**
  (e.g. `acorn-hall RELIGION_OF faith-of-the-seven`).

No other retyping. No edge type is invented; both targets are in the master vocabulary.

### Rule 6 — Endpoint type contracts (mirrors `scripts/stage4-type-contract-validator.py`)

Contracts catch rows where resolution *succeeded* but onto the wrong kind of node — almost always a
parser value-split or a slug collision. Violations QUARANTINE (logged with both endpoint categories);
they are true relationships with broken encoding, recoverable by a later curator, never silently
mergeable.

- **6a kinship char↔char:** `PARENT_OF`, `SPOUSE_OF`, `LOVER_OF` require both endpoints in
  `characters/`. **73 rows quarantined.** Canonical catch: `Doran Martell` · `Spouse` · `Norvos` —
  the parser split "Mellario of Norvos" into two targets; `Mellario` merges, `Norvos` (a location)
  would have become `doran-martell SPOUSE_OF norvos`. Also `Alannys Harlaw` · `father` · `Harlaw`
  (location), `Alys Karstark` · `spouse` · `Thenns` (faction).
- **6b HOLDS_TITLE target must be `titles/`:** **464 rows quarantined.** Catches three failure
  classes in one move: title-fragment splits (`Doran Martell HOLDS_TITLE Sunspear` from "Castellan of
  Sunspear"; `Aemon ... HOLDS_TITLE Castle Black` from "Maester at Castle Black"), slug collisions
  (`Aelinor Penrose HOLDS_TITLE Lady` — `lady` is Sansa's *direwolf*), and ship-captaincy encoded as
  Title (`Aeron Greyjoy HOLDS_TITLE Golden Storm`, an artifact — possible future `CAPTAIN_OF`
  retype, open question 3). Also catches HOLDS_TITLE self-references before Rule 8 sees them
  (`Amethyst Empress HOLDS_TITLE Amethyst Empress` — target resolves to the character herself).
- **6c Result-field DEFEATS — quarantined wholesale:** **315 rows.** Architecture maps `Result` →
  `DEFEATS` with the note "Extract victor/defeated from result text" — that extraction was never
  implemented. The rows as parsed are `<battle-page> DEFEATS <whoever was linked in the result
  cell>`, where the link is usually the *victor* (`Aegon's first test` · result · `Targaryen`) —
  wrong direction AND wrong endpoints (DEFEATS is Victor → Defeated, both combatants, never the
  battle itself). Unsalvageable deterministically; quarantined as a class for a future
  victor-extraction pass.

- **ACCEPTED:** `Walder Frey` PARENT_OF `Roslin Frey` (char↔char ✓); `Eddard Stark` HOLDS_TITLE
  `Hand of the King` (target in `titles/` ✓).
- **FILTERED:** n/a — contracts quarantine, never filter.

### Rule 7 — Direction conventions (and the FIELD_EDGE_MAP correction table)

The row's `direction` field means: `forward` = page → target; `reverse` = target → page;
`symmetric` = undirected (emit once, `symmetric: true`).

**Finding (computed against architecture.md's directionality column):** `FIELD_EDGE_MAP`'s direction
value is **inverted for 10 fields**. The error was invisible until now because the only consumer was
the display-bullet renderer, which prints rows page-relatively without materializing endpoints. This
merge is the first materialization, so the script carries a correction table — `DIRECTION_FLIP_FIELDS
= {heir, heirs, cadet branches, head, ruler, successor, predecessor, founder, owner, owners}` — and
swaps endpoints after applying the map direction for those fields. Verification of each against
architecture.md:

| Edge type | architecture.md direction | Field (on page X, listing T) | Map says | Correct materialization | Flip? |
|---|---|---|---|---|---|
| `PARENT_OF` | Parent → Child | `Father`/`Mother` on child's page | reverse | T → X ✓ | no |
| `PARENT_OF` | Parent → Child | `Issue` on parent's page | forward | X → T ✓ | no |
| `SPOUSE_OF` / `LOVER_OF` | Symmetric | `Spouse(s)` / `Lover(s)` | symmetric | undirected ✓ | no |
| `SWORN_TO` | Vassal → Lord | `Allegiance(s)`, `Monarch` | forward | X → T ✓ | no |
| `OVERLORD_OF` | Overlord → Vassal | `Overlord(s)` on vassal's page | reverse | T → X ✓ | no |
| `RULES` | Ruler → Location/domain | `Ruler` on location page, `Head` on house page | forward (X → T) | **T → X** | **YES** |
| `HEIR_TO` | Heir → Holder | `Heir(s)` on holder's page | forward (X → T) | **T → X** | **YES** |
| `SUCCEEDS` | Successor → Predecessor | `Successor` on predecessor's page | forward (X → T) | **T → X** | **YES** |
| `SUCCEEDS` | Successor → Predecessor | `Predecessor` on successor's page | reverse (T → X) | **X → T** | **YES** |
| `FOUNDED` | Founder → Founded | `Founder` on the founded page | forward (X → T) | **T → X** | **YES** |
| `OWNS` | Owner → Owned | `Owner(s)` on the owned thing's page | forward (X → T) | **T → X** | **YES** |
| `CADET_BRANCH_OF` | Cadet → Parent house | `Cadet branches` on senior house's page | forward (X → T) | **T → X** | **YES** |
| `SEAT_OF` | Location → House | `Seat(s)` on house page | reverse | T → X ✓ | no |
| `ANCESTRAL_WEAPON_OF` | Weapon → House | `Ancestral weapon` on house page | reverse | T → X ✓ | no |
| `REGION_OF` | Location → Region | `Region(s)` | forward | X → T ✓ | no |
| `BORN_AT`/`DIED_AT`/`BURIED_AT` | Person → Location | `Born`/`Died`/`Buried` | forward | X → T ✓ | no |
| `CULTURE_OF` | Person → Culture | `Culture`, `Race` | forward | X → T ✓ | no |
| `WORSHIPS` / `RELIGION_OF` | Person/Place → Religion | `Religion` | forward | X → T ✓ | no |
| `HOLDS_TITLE` | Person → Title | `Title(s)` | forward | X → T ✓ | no |
| `FIGHTS_IN` / `PART_OF` | Person → Event / Battle → War | `Conflict`, `Battles` | forward | X → T ✓ | no |
| `WRITTEN_BY` | Text → Author | `Author`, `Written by` | forward | X → T ✓ | no |

(There is no `CHILD_OF` type — child-page `Father`/`Mother` rows materialize as the parent-sourced
`PARENT_OF`, per the reverse-emission policy in architecture.md's vocabulary-lock note.)

Worked example: `Acorn Hall` · `Ruler` · `Theomar Smallwood` · map `forward` → flip →
`theomar-smallwood RULES acorn-hall`. Without the flip, the graph would say a castle rules its lord —
×264 RULES rows, ×179 HEIR_TO, ×93 SUCCEEDS, ×71 FOUNDED, ×84 OWNS, ×26 CADET_BRANCH_OF.
Sanity confirmation from the computed run: post-flip RULES is 183 char→house + 75 char→location;
OVERLORD_OF is 545 house→house. **Open question 1:** the same inversion should be fixed at the source
(`FIELD_EDGE_MAP` + architecture.md's infobox-subset table rows for Successor/Predecessor) — doc/parser
sync, no re-parse needed for this merge since the script corrects at materialization.

### Rule 8 — Self-loop suppression

After resolution and direction, drop rows where source == target. **2 rows filtered** (`Brandon
Norrey` · `Issue` · `Brandon Norrey` — the wiki's "his son, also named Brandon Norrey" linking back
to the same page; `Timett` · `father` · `Timett` — Timett son of Timett, same page). Logged; if
son-pages ever get minted these can return.

### Rule 9 — In-run dedupe (qualifier-aware)

Key = `(edge_type, source, target)`; for symmetric types (`SPOUSE_OF`, `LOVER_OF`) the endpoint pair
is unordered. **1,356 rows deduped.** This is mostly the wiki's own bidirectional encoding collapsing
correctly: Eddard's page lists `Spouse: Catelyn Tully` and Catelyn's lists `Spouse: Eddard Stark` →
one edge. Same for `Father`+`Issue` pairs (child's page and parent's page assert the same
`PARENT_OF`).

**v2 — dedupe is qualifier-aware, not first-wins (critic finding 3).** v1's first-occurrence-wins
silently dropped qualifiers when the qualified row arrived second — verified casualties: Tyrion/Tysha
(`annulled` vs none), Dalton/Tess and Dalton/Lysa Farman (`salt wife` vs none), Asha/Erik Ironmaker
(`forced marriage` vs none). v2 policy, comparing NBSP/whitespace/case-normalized raw qualifiers:

- later row's qualifier equals the kept row's, or later row is unqualified → plain dedupe;
- kept row unqualified, later row qualified → **the qualified row replaces the kept row** (same
  endpoints by key construction; counted as a dedupe, plus an informational
  `qualified_row_preferred` sub-count: **3 swaps** in the current data — the other verified cases
  happen to arrive qualified-first and need no swap);
- two *different* non-empty qualifiers → **quarantine the fact for review** (both rows move to
  `quarantined.jsonl` tagged `R9q`, the kept row is retracted from the merge, and any further rows
  on that key also quarantine). **0 rows today** — every current collision is qualified-vs-blank —
  but the bucket exists and the dry-run report must print it (expected 0).
- dups of a key that Rule 10 already routed to the corroboration log are plain dedupes (nothing is
  being emitted for that key, so there is no qualifier to lose).

### Rule 10 — Dedupe against existing edges.jsonl (corroboration log)

Same key against the 4,760 existing canonical rows (run AFTER hygiene fix A remaps, so corrected
endpoints are compared). **Symmetric types (`SPOUSE_OF`, `LOVER_OF`) key on the unordered endpoint
pair here too, exactly as in Rule 9** — an existing `a SPOUSE_OF b` matches an incoming
`b SPOUSE_OF a` (critic finding 5). Matches are **skipped and logged as corroboration candidates** —
the book edge already owns the fact at Tier 1 with a quote; the wiki agreeing is confirmation
metadata, not a second edge. **87 rows logged** (e.g. `Arianne Martell` · `father` · `Doran Martell`
— already in canon as a Pass-1 edge; Jon Snow `SWORN_TO Night's Watch` and `LOVER_OF Ygritte` — both
already earned by book quotes; down from 92 in v1 because 5 rows now quarantine under Rule 3
before reaching this rule). The merge logs them to `corroborations.jsonl`; stamping
`corroborated_by: wiki-infobox` onto the existing rows is open question 8.

**Idempotency (critic finding 6):** this rule also makes `--apply` idempotent. A second `--apply`
against an already-merged `edges.jsonl` finds every previously appended row in `existing_keys`,
routes all of them to the corroboration log, and appends **0 rows** — an all-corroboration no-op.
Source-collision risk (two distinct input rows surviving to emit the same key in one run) is handled
by Rule 9 upstream; verified clean on the current data.

### Rule 11 — Stamping: tier, provenance, qualifiers

Every merged edge gets:

- `confidence_tier: 2` — **hard ceiling, no exceptions.** Tier 1 is earned by verbatim book quotes
  (locked requirement). Nothing in this run can be Tier 1, including facts that are *obviously* true.
- `evidence_kind: "wiki-infobox"`, `typed_by: "python-infobox-map"`, `evidence_ref: "wiki:<Page>"`
  (URL-style page name with underscores, e.g. `wiki:Walder_Frey`, matching node files' `wiki_source`
  convention).
- **Qualifier normalization.** `reference/edge-qualifier-vocab.md` makes `qualifier` a validated enum:
  REQUIRED for SPOUSE_OF/PARENT_OF/HOLDS_TITLE/SWORN_TO (among the merged types), OPTIONAL-enum for
  LOVER_OF, FORBIDDEN for everything else (Tier-3 types reject any qualifier — and dates like
  `208 AC` on BORN_AT are not enum values). So: the raw infobox qualifier string is preserved
  verbatim in a separate `wiki_qualifier` field on every row that has one; the enum `qualifier`
  field is set only on enum-bearing types via this deterministic map (built from the vocab file's
  own wiki-derived rationale data):
  - HOLDS_TITLE: `formerly`→`former`, `claimant`/`self-styled`/`pretender`→`claimed`,
    `historical`→`historical`, `stripped`→`former`, `disputed`*→`contested`; default `unknown`.
  - SWORN_TO: `formerly`→`former`, `deserted`→`deserted`, `by marriage`→`by_marriage`,
    `claimed`→`claimed`; default `unknown`.
  - SPOUSE_OF: `salt wife`→`salt_wife`, `annulled`/`dissolved`→`annulled`, `formerly`→`former`;
    default `unknown`.
  - PARENT_OF: `adopted`/`adoptive mother`/`adoptive father`→`adopted`, `disputed`*→`disputed`,
    `claimed`→`claimed`; default `biological` (rumor-class values never reach here — Rule 3 took them).
  - LOVER_OF (optional): `paramour`→`paramour`, `formerly`→`former`; omit otherwise.
  - (* `disputed`-prefixed long strings like "disputed by Tristifer Botley" map on the prefix; full
    string stays in `wiki_qualifier`.)
  - Defaults are open question 2 (`unknown` vs `current`/`biological`-style assumptions).

**Parser-artifact qualifiers — log-line requirement (critic finding 7).** A handful of raw
qualifiers are parser value-split debris, not information: `ren` ×4 and `s` ×2 (the tails of
`Child(ren)`/`Son(s)` — those six rows' targets are bare-kinship words, so Rule 2b/Rule 4 disposes
of the rows themselves), plus date-range strings (`286–298 AC`, `209 AC-215 AC`, ...) on `Heirs`
rows, which DO merge with the range preserved in `wiki_qualifier`. The dry-run report MUST include a
dedicated log section listing every row whose raw qualifier matches the artifact patterns
(`^(ren|s)$` or the date-range shape), with its disposition — so the debris is eyeballed, not
silently carried.

---

## 3. Expected counts (v2 — recomputed 2026-06-12; the dry-run report MUST be checked against these)

The implementation is deterministic over `infobox-data.jsonl` + `alias-resolver.json` + the node-file
tree + `edges.jsonl`. Run against the same repo state, the dry run must reproduce these numbers
exactly; if nodes/edges changed in between, small drift is explainable but must be itemized.
(v1 originals shown where they changed; the v1 pipeline was re-run 2026-06-12 and reproduced its
spec numbers exactly before the v2 rules were applied, so every delta below is attributable to the
critic fixes, not repo drift.)

**Disposition of all 20,614 rows:**

| Bucket | Rule | Count | (v1) |
|---|---|---|---|
| **MERGED** | — | **17,006** | 17,040 |
| Filtered: source unresolved | R1 | 3 | — |
| Filtered: noise placeholder | R2a | 412 | — |
| Filtered: noise bare-kinship | R2b | 204 | — |
| Filtered: noise numeral/date | R2c | 0 | — |
| Filtered: target unresolved | R4 | 507 | — |
| Filtered: self-loop | R8 | 2 | — |
| **Filtered total** | | **1,128** | 1,128 |
| Quarantined: plural Mothers/Fathers field | R3a | 46 | — |
| Quarantined: multi-value singular father/mother | R3b | 8 | — |
| Quarantined: speculative/hedge qualifier (kinship, widened) | R3c | 102 | 86 |
| Quarantined: `disputed` on non-PARENT_OF kinship | R3d | 5 | n/a |
| Quarantined: mirror of quarantined fact (fact-key closure) | R3e | 24 | n/a |
| Quarantined: kinship endpoint contract | R6a | 73 | — |
| Quarantined: HOLDS_TITLE target contract | R6b | 464 | — |
| Quarantined: Result-field DEFEATS class | R6c | 315 | — |
| **Quarantined total** | | **1,037** | 992 |
| Quarantined: dedupe qualifier conflict | R9q | 0 | n/a |
| Deduped within run (incl. 3 qualified-row-preferred swaps) | R9 | 1,356 | 1,362 |
| Skipped, corroborates existing edge | R10 | 87 | 92 |
| **Sum** | | **20,614** ✓ | 20,614 ✓ |

Delta vs v1: 45 rows moved into quarantine (16 widened-regex + 5 disputed-non-PARENT_OF + 24
mirrors), drawn 34 from MERGED, 6 from dedupe, 5 from corroborations. Filtered buckets unchanged.

Retypes inside the merged set: `FIGHTS_IN`→`PART_OF` 184, `WORSHIPS`→`RELIGION_OF` 93 (unchanged).
Resolution-ladder usage (counted over rows passing Rule 4, identical under v1 and v2 rules):
target via alias 299, target via the-strip 89, source rescued by parens-kept rung 345 (rows whose
parens-stripped page slug is not a node). *Erratum: v1 stated 305/89/351 — the alias and parens
numbers were measured under a superseded rung ordering from an earlier analysis script; corrected
here, see changelog.*

**Merged edges by type (all 22; v1 deltas noted):**

| Type | Count | | Type | Count |
|---|---|---|---|---|
| SWORN_TO | 4,064 | | RULES | 264 |
| HOLDS_TITLE | 3,401 | | PART_OF | 184 |
| CULTURE_OF | 3,252 | | HEIR_TO | 179 (v1: 181) |
| PARENT_OF | 1,645 (v1: 1,675) | | RELIGION_OF | 93 |
| DIED_AT | 915 | | SUCCEEDS | 93 |
| BORN_AT | 833 | | OWNS | 84 |
| REGION_OF | 573 | | LOVER_OF | 71 (v1: 73) |
| OVERLORD_OF | 551 | | FOUNDED | 71 |
| SEAT_OF | 329 | | BURIED_AT | 48 |
| SPOUSE_OF | 313 | | CADET_BRANCH_OF | 26 |
| | | | ANCESTRAL_WEAPON_OF | 13 |
| | | | FIGHTS_IN | 4 |

**Aggregate effect:** `edges.jsonl` 4,760 → **21,766 rows** (v1: 21,800). Node connectivity (nodes
touching ≥1 edge, excl. `_conflicts`/`_unclassified`): 1,215/8,261 (**14.7%**) → 5,868/8,261
(**71.0%**) — identical to v1; all 34 newly suppressed rows connect nodes that other edges already
touch.

**Known residuals (≤5 rows, accepted for dry-run review):** 4 surviving FIGHTS_IN rows have
non-character sources (3 `texts/`, 1 `factions/`), and 1 PART_OF row has a location target — listed
in the dry-run sample for Matt's eyeball; not worth a rule of their own.

---

## 4. Edge schema (exact fields per merged row)

Matches the canonical `edges.jsonl` shape (the Pass-1-derived rows are the template; field names
identical where semantics overlap). One complete real example — Walder Frey's daughter Roslin:

```json
{"decision": "emit_edge", "candidate_kind": "wiki-infobox", "edge_type": "PARENT_OF",
 "source_slug": "walder-frey", "source_resolution_status": "resolved-exact",
 "target_slug": "roslin-frey", "target_resolution_status": "resolved-exact",
 "evidence_kind": "wiki-infobox", "evidence_ref": "wiki:Walder_Frey",
 "evidence_field": "Issue", "evidence_quote": null,
 "evidence_book": null, "evidence_chapter": null,
 "qualifier": "biological", "wiki_qualifier": null,
 "confidence_tier": 2, "typed_by": "python-infobox-map",
 "symmetric": false, "direction_corrected": false,
 "run_id": "infobox-merge-20260612", "schema_version": "infobox-merge-v2",
 "produced_at": "<ISO-8601 UTC>"}
```

Field notes:
- `source_resolution_status` / `target_resolution_status`: `resolved-exact` | `resolved-exact-parens`
  | `resolved-alias` | `resolved-the-strip` (mirrors the Stage-4 status vocabulary).
- `evidence_quote` is explicitly `null` — infoboxes have no prose. This plus `evidence_kind` is what
  keeps these rows honest next to the book layer's verbatim quotes.
- `evidence_book` / `evidence_chapter` are **explicitly emitted as `null`** (critic finding 4 —
  these fields are present on all 4,760 existing canon rows, so downstream consumers expect the
  keys). Rationale for null rather than derived: the parser strips per-row `<sup>` citation markers,
  so chapter anchors survive only at *page* level (`cite_refs`), and attaching page-level anchors to
  a single row is false precision (see the cite_refs note in section 1 — Eddard's page cites 70+
  chapters). Consumers must treat `evidence_kind: "wiki-infobox"` + null book/chapter as the defined
  shape for this layer. If per-row anchors are ever recovered (targeted `<td>` re-parse keeping
  `<sup>` ids), backfill is additive. Decided-by-default; flagged as open question 11.
- `qualifier` present only on enum-bearing types (Rule 11); `wiki_qualifier` carries the raw string
  (`"208 AC"`, `"formerly"`, `"de jure"`) whenever the infobox had one, on any type.
- `symmetric: true` on SPOUSE_OF / LOVER_OF rows.
- `direction_corrected: true` on rows whose field is in `DIRECTION_FLIP_FIELDS` (audit trail for the
  Rule-7 fix).
- No `notes` field (deleted from schema 2026-05-18; validator rejects it). No `first_available`
  (deferred project-wide).

---

## 5. Hygiene fixes (same script pass, separate report sections)

### Fix A — orphan endpoint slugs already in edges.jsonl

Recomputed exactly (2026-06-11): **115 distinct endpoint slugs across 140 rows of edges.jsonl have no
node file.** Resolution through the ladder plus one extra rung:

| Resolution | Slugs | Rows | Action |
|---|---|---|---|
| alias-resolver remap | 23 | 35 | rewrite slug in place, keep every other field |
| leading-`the-` strip | 3 | 4 | same (`the-antler-men`→`antler-men`, `the-great-walrus`→`great-walrus`, `the-windblown`→`windblown`) |
| honorific-prefix strip | 26 | 33 | same, **guarded** (below) |
| unresolvable | 63 | 68 | leave as-is, log (most are Pass-1 minor entities that never got nodes — `unnamed-soldier`, `vision-bearded-man`, `rooftop-sentinel`; node-minting is a separate backlog item, not this script's job) |

The 23 alias remaps, verbatim (slug → canonical, row count):

```
abel→mance-rayder(1)  aeron-damphair→aeron-greyjoy(1)  bittersteel→aegor-rivers(1)
brienne-of-tarth→brienne-tarth(2)  caggo-corpsekiller→caggo(2)  deaf-dick-follard→dick-follard(1)
greatjon-umber→jon-umber(4)  iron-emmett→emmett(1)  lady-stoneheart→catelyn-stark(1)
lark-the-sisterman→lark(1)  lem-lemoncloak→lem(1)  ned-stark→eddard-stark(1)
petyr-pimple→petyr-frey(1)  pyp→pypar(2)  raff-the-sweetling→rafford(2)
ramsay-bolton→ramsay-snow(2)  the-high-sparrow→high-sparrow(1)  the-tickler→tickler(2)
thoros-of-myr→thoros(2)  tormund-giantsbane→tormund(3)  varamyr-sixskins→varamyr(1)
wine-merchant→wineseller(1)  young-griff→aegon-targaryen-young-griff(1)
```

**Two of these are SEMANTIC, not cosmetic, and the dry-run report must flag them for Matt's eyeball
(critic finding 8):** `lady-stoneheart→catelyn-stark` and `abel→mance-rayder` collapse an in-story
*persona* onto the underlying person. Both follow established project conventions (the
alias-resolver already canonicalizes them, and the impersonation-edges rule attaches identity-fraud
edges to the actual actor), but persona-collapse is a judgment call, not a spelling fix — the
report renders these two remaps in their own labeled subsection, with the affected rows, so the
default can be overridden before `--apply`.

**Honorific-strip rung:** strip a leading `ser-|lord-|lady-|maester-|septa-|septon-|khal-|king-|queen-|prince-|princess-`
token and accept only if the remainder is an existing node (or alias) **in `characters/`**. The
category guard is load-bearing: it admits the 26 legitimate fixes (`ser-rodrik-cassel`→`rodrik-cassel`,
`khal-drogo`→`drogo`, `maester-luwin`→`luwin`, ...) and rejects the one false positive the unguarded
rung produces — `maester-griffins-roost` would strip to `griffins-roost`, a *location*, but the edge
is about a person (the maester AT Griffin's Roost). That slug stays in the unresolvable list. This
rung goes beyond the literal "alias layer" — it mirrors `stage4_name_resolver.py`'s TITLE_PREFIXES
precedent — flagged as open question 7.

Mechanics: remap runs FIRST (before the merge dedupe, so Rule 10 compares corrected endpoints). Each
remapped row keeps all other fields, gains `endpoint_remapped: {"<old>": "<new>"}`. After remapping,
re-key against the rest of edges.jsonl: if a remap creates an exact (type, source, target) duplicate
of another existing row, log it as a merge-candidate pair for Matt — do NOT auto-delete (expected
rare; report will give the exact count).

### Fix B — the 948 rows missing `typed_by` (+ chapter-label-only citations)

Recomputed: exactly **948 rows lack `typed_by`** — 897 `evidence_kind: book-pass1-reified` (Plate-3
event-reification role edges) + 51 `plate4-wiki-cluster` (Plate-4 chapter-beat/SUB_BEAT_OF rows).
Backfill:

- 897 reified rows → `typed_by: "plate3-reifier"` (consistent with their `plate: plate3-*` /
  `schema_version: plate3-v1` provenance; the typing was done by the Plate-3 reification pipeline).
- 51 plate4 rows → `typed_by: "plate4-cluster-classifier"` (the row already carries the exact
  `classifier_model` + `reconciled_model` fields; typed_by names the pipeline, matching how
  `python-map`/`hospitality-table` name pipelines, not models).

**Citations:** these rows cite chapter labels (`evidence_chapter: "ASOS Arya VII"`), no `file:line`.
Computed: a deterministic label→file converter (book + POV name + roman numeral → chapter-file stem,
validated against `sources/chapters/`) maps **891/948** directly to an existing chapter file. The 57
misses are named non-POV-pattern chapters (`ADWD The Griffin Reborn` ×18, `AFFC The Queenmaker` ×14,
`ADWD The King's Prize I` ×8, ...) — closable with a small static label→file table built from
`reference/pov-characters.md` — plus 2 rows with an empty label (log, leave). Backfill writes
`evidence_ref: "sources/chapters/<book>/<file>.md"` (file-level, no line) and
`locate_status: "chapter-file"` — honest about precision. **Line-level ref backfill remains the
separate follow-up #11**; this fix only normalizes the field shape so consumers stop special-casing
948 rows.

Optional same-pass cleanup (flag in report, default ON): the 51 plate4 rows still carry the stale
field `"stage": "STAGED — DO NOT promote to graph/edges/edges.jsonl until Plate 5 gated merge"` —
they WERE promoted (all have `plate5_merged_at`). Drop the `stage` field.

---

## 6. Out of scope — explicitly NOT promoted

- **Node-file `## Edges` display bullets** (21,129 bullets across 4,684 node files): same underlying
  data as infobox-data.jsonl (`track_b` provenance throughout) rendered for humans. This merge
  supersedes them as a data source. They are NOT touched, NOT parsed, NOT deleted by this script.
  Regenerating display bullets *from* edges.jsonl is a possible later cosmetic pass.
- **Prose-comention / entity emits** (pass2-buckets Sonnet ~4,132 + Haiku ~2,050 + events-haiku
  ~1,617): deprecated, stays deprecated (S84 verdict, reaffirmed in the 2026-06-11 audit). Wiki-prose
  evidence, no file:line, inconsistent schemas. Not part of this merge in any form.
- **Theories and prophecies: zero coverage — stated so you're not surprised.** Theory/prophecy wiki
  pages have no infoboxes, so this merge contributes nothing to `theories/` (45 nodes, ~0 connected)
  or `prophecies/` (2 nodes, 0 connected). Those layers stay dark after the merge; connecting them is
  the Pass 4/5 analytical surface plus wiki-prose-link ABOUT/MENTIONS edges (synthesis.md sketches
  the options).
- **WRITTEN_BY:** 3 rows in, 0 merged — all three are real-world ASOIAF publications whose pages were
  never promoted to nodes (Rule 1 filters them). In-world texts with Author infobox rows would merge;
  none exist in the current parse.
- **`first_available` / spoiler gating:** deferred project-wide; the field is not set on merged edges.
- **Edge polish / variant merging** (e.g. unifying SUCCEEDS chains): explicitly a future
  agent-reasoning phase per architecture.md; this script never merges semantically-near edges.

---

## 7. Execution plan

**Script:** `scripts/infobox-merge.py` — single file, stdlib-only, no LLM, no network.

**Inputs (read-only):** `working/wiki/data/infobox-data.jsonl`,
`working/wiki/data/alias-resolver.json`, `graph/nodes/**` (slug+category walk),
`graph/edges/edges.jsonl`, `sources/chapters/**` (filename stems only, for Fix B label→file).

**Modes:**
- `--dry-run` (DEFAULT): writes nothing under `graph/`. Emits to `working/infobox-merge/`:
  - `dry-run-report.md` — every count in section 3 side-by-side with this spec's expected values,
    PASS/FAIL per line; Fix A table (remaps + unresolvables, **with the two semantic remaps
    `lady-stoneheart→catelyn-stark` / `abel→mance-rayder` in their own flagged subsection**); Fix B
    counts; ladder usage; per-type endpoint-category crosstab; the R9q dedupe-conflict section
    (expected 0); the parser-artifact-qualifier log section (Rule 11); **20-edge random sample**
    (seeded RNG, seed in report) rendered human-readably for spot-checking.
  - `merged-candidate.jsonl` (the 17,006 rows, exactly as they would be appended),
  - `filtered.jsonl`, `quarantined.jsonl`, `corroborations.jsonl` (full logs, every row tagged with
    its rule id),
  - `hygiene-a-remaps.jsonl`, `hygiene-b-stamps.jsonl` (per-row before/after for both fixes).
- `--apply`: requires `--dry-run` outputs to exist and match; then:
  1. Backup `graph/edges/edges.jsonl` → `graph/edges/_regrounding/edges-pre-infobox-merge-2026-MM-DD.jsonl`
     (the established `_regrounding/` convention — `edges-pre-reification-2026-06-09.jsonl` is the precedent).
  2. Apply Fix A remaps in place, then Fix B stamps in place.
  3. Append the merged rows.
  4. Re-run validators: `scripts/stage4-type-contract-validator.py` (0 new DROP-class violations
     expected on the appended set), the qualifier-enum rules from
     `reference/edge-qualifier-vocab.md` (0 violations — Rule 11 guarantees enum compliance), and
     `scripts/orphan-edges-audit.py` / a slug-intersection check (**new orphan endpoints introduced
     by this merge: must be exactly 0** — every merged endpoint resolved to an existing node by
     construction; pre-existing 63 unresolvables remain and are reported, not worsened).

**Test expectations (assert in-script before writing anything in --apply):** total disposition sums
to rows-in; merged-by-type matches dry-run; post-append line count = 4,760 + 17,006 = 21,766
(adjusted if edges.jsonl changed since this spec — recompute, don't hardcode 4,760); JSON-parse
round-trip of every emitted line. A second `--apply` must be a no-op (Rule 10 idempotency — all
candidates route to the corroboration log, 0 appends).

**The gate:** tonight's session runs `--dry-run` ONLY → Matt reviews `dry-run-report.md` (counts vs
this spec, the 20-edge sample, the quarantine logs, the open questions below) → `--apply` ships in a
later session. **This session and the implementation session do not write to `graph/`.**

---

## 8. Open questions flagged for Matt (none block the dry run)

1. **FIELD_EDGE_MAP direction inversions (Rule 7, 10 fields).** Merge script corrects at
   materialization. Should the same session that ships `--apply` also fix `FIELD_EDGE_MAP` +
   architecture.md's infobox-subset table (Successor/Predecessor rows et al.)? No re-parse needed;
   doc/parser sync only. (Recommended: yes, per CLAUDE.md rule 6 — schema and architecture.md must
   not stay contradictory.)
2. **Tier-1 qualifier defaults** (Rule 11): rows with no wiki qualifier get `unknown` for
   HOLDS_TITLE/SWORN_TO/SPOUSE_OF and `biological` for PARENT_OF. Alternative: `current` for the
   first three (claims more than the wiki states for historical figures). Spec'd as `unknown`; cheap
   to change before apply.
3. **Quarantined ship-captaincy rows** (Rule 6b, 43 of the 464): `HOLDS_TITLE → artifact` rows like
   Aeron/`Golden Storm` are real captaincies; retype to `CAPTAIN_OF` in a small follow-up pass?
4. **CULTURE_OF region-name targets** (927 rows, Rule 4): merged as-is (person → location standing in
   for the culture). OK, or mint `reachmen`/`crownlanders` culture nodes and retarget later?
5. **Result-field DEFEATS class** (315 rows, Rule 6c): quarantined wholesale. Accept kill, or queue a
   victor-extraction curator pass?
6. **`the-` strip rung** overrides `alias_collisions`' "ambiguous-do-not-resolve" for single-candidate
   leading-article variants (`the-wall`→`wall` class). Exact-match-only; 89 target rows + 4 orphan
   rows depend on it.
7. **Honorific-strip rung in Fix A** (26 slugs / 33 rows): deterministic + character-guarded, but
   beyond the literal alias layer. Approve, or restrict Fix A to pure alias remaps (then 23/35)?
8. **Corroboration handling** (87 rows): log-only in v1/v2. Worth stamping
   `corroborated_by: wiki-infobox` on the matching existing Tier-1 edges at apply time?
9. **Fact-key mirror quarantine (Rule 3e) — decided by default, override available.** v2 quarantines
   by fact key, so 24 individually-clean rows (Jaime's `Issue` rows for the incest children,
   Ramsay·`Spouses`·Arya, Laenor's disputed issue, Walder's six Annara-children rows, ...) are
   suppressed because their mirrors are tainted. The conservative direction (quarantine ≠ delete;
   a curator can promote per-fact) — but it IS a default Matt can override per-fact from
   `quarantined.jsonl`. Companion policy: `disputed` on non-PARENT_OF kinship quarantines (Rule 3d)
   because those types can't carry the flag; `disputed` PARENT_OF with an untainted fact key still
   merges, enum-flagged.
10. **Dedupe-conflict policy (Rule 9) — decided by default, override available.** Qualified row
    beats unqualified (3 swaps); two different qualifiers quarantine the fact (R9q — currently 0
    rows, policy exists for future data). Alternative Matt could prefer: union both qualifiers into
    `wiki_qualifier` and merge anyway.
11. **`evidence_book`/`evidence_chapter` emitted as explicit nulls — decided by default, override
    available.** Present on 4,760/4,760 canon rows, so the keys are emitted with `null` rather than
    omitted (section 4 rationale: page-level cite_refs would be false precision at row level).
    Alternative: derive from `cite_refs` where a page cites exactly one chapter — rejected for v2 as
    a special case that changes meaning per-row; revisit only with the targeted `<sup>` re-parse.

---

## Changelog

- **v1 — 2026-06-11.** Original spec (Fable subagent, read-only session). All counts computed from
  throwaway Python in `/tmp/infobox-merge-analysis/` (an1–an9): 17,040 merged / 1,128 filtered /
  992 quarantined / 1,362 deduped / 92 corroborations.
- **v2 — 2026-06-12.** Revision after adversarial fresh-eyes review (verdict: ACCEPT-WITH-FIXES).
  The critic **independently confirmed the Rule 7 direction-inversion table — all 10 flip fields —
  and reproduced the headline counts, including SWORN_TO 4,064 exactly.** Before applying fixes,
  the v1 pipeline was re-run and reproduced every v1 spec number exactly (no repo drift). Findings
  applied — **none rejected**:
  1. *(CRITICAL)* Rule 3 quarantine leaked through the wiki's bidirectional kinship encoding
     (verified: Robert/Jaime `Issue` mirrors of the incest children, Ramsay·`Spouses`·Arya, Laenor's
     disputed issue). Fixed by quarantining by **fact key** (new Rule 3e, 24 rows; fact-key
     normalization defined in Rule 3).
  2. *(MAJOR)* Rule 3c regex widened with seven verified-in-data hedge terms (`officially`,
     `legally`, `unconfirmed`, `presumably`, `debated`, `dubious canonicity`, `in some tales`):
     86 → 102 rows. Policy decided for `disputed` on non-PARENT_OF kinship: quarantine (new
     Rule 3d, 5 rows), since HEIR_TO forbids qualifiers and SPOUSE_OF/LOVER_OF enums lack
     `disputed` — merging bare would unflag a contested claim.
  3. *(MAJOR)* Rule 9 dedupe made qualifier-aware (verified casualties Tyrion/Tysha `annulled`,
     Dalton `salt wife` ×2, Asha/Erik `forced marriage`): qualified row preferred (3 swaps);
     conflicting qualifiers quarantine the fact (R9q, currently 0).
  4. *(MAJOR)* Schema decision documented for `evidence_book`/`evidence_chapter` (present on all
     4,760 canon rows): emitted as explicit nulls with rationale (section 4, open question 11).
  5. *(MINOR)* Rule 10 now states symmetric types key on the unordered pair (matching Rule 9).
  6. *(MINOR)* Idempotency stated explicitly: second `--apply` = all-corroboration no-op (Rule 10 +
     section 7 test expectation).
  7. *(MINOR)* Parser-artifact qualifiers (`ren` ×4, `s` ×2, date-ranges): dedicated dry-run log
     section required (Rule 11).
  8. The two semantic orphan remaps (`lady-stoneheart→catelyn-stark`, `abel→mance-rayder`) must be
     flagged in their own dry-run report subsection for Matt's eyeball (Fix A).
  9. Findings 1/3/4 added to open questions (9/10/11) as decided-by-default-pending-override.

  Count changes: merged 17,040 → **17,006**, quarantined 992 → **1,037** (+45: 16 widened-regex +
  5 disputed-non-PARENT_OF + 24 mirrors), deduped 1,362 → **1,356**, corroborations 92 → **87**;
  filtered unchanged at 1,128; sum still 20,614. By type: PARENT_OF −30, HEIR_TO −2, LOVER_OF −2.
  Post-merge edges.jsonl 21,800 → **21,766**; connectivity unchanged at 5,868/8,261 (71.0%).
  Erratum found during recompute (not a critic finding): v1's resolution-ladder usage stats
  (target-alias 305 / source-parens 351) were carried from a superseded rung ordering; corrected to
  299 / 345 with the counting point now defined (rows passing Rule 4). Schema version bumped to
  `infobox-merge-v2`.

---

*Computation artifacts for this spec live in `/tmp/infobox-merge-analysis/` (an1–an9 = v1, an10_v2.py
= v2 recompute incl. v1 regression check; merged/filtered/quarantined-v4.json are the v2 dumps).
They are throwaway; the spec is self-contained without them.*
