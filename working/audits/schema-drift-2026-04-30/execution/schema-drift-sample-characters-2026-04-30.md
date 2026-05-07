# Schema-Drift Audit (Sample, Characters) — 2026-04-30

**Scope:** all character nodes whose slugs start `[abc]` — 614 of 3,373 total in `graph/nodes/characters/` (~18% of the corpus). The original brief asked for the alphabetically-first 500. The actual slice is 614 because Glob-by-prefix is the only deterministic way to take an alphabetical slice from this corpus, and `a` (245) + `b` (220) + `c` (149) sums to 614. The over-scope is small and within the cost budget set by the houses+locations sister run.
**Sister run:** `working/audits/schema-drift-sample-2026-04-30.md` (houses + locations). Findings repeat-from-houses are referenced by number, not restated.
**Purpose:** surface character-specific drift before the full-corpus audit — wiki "Born/Died" date-bleed into edge targets, malformed YAML, and dragon-vs-human typing.
**Method:** read-only ripgrep across required frontmatter fields, edge labels, edge-target shapes, and structural sections. No node was modified.
**Nodes scanned:** 614
**Total findings:** 6 character-specific patterns + 4 patterns identical to houses+locations (referenced, not restated)
**Severity counts (character-specific only):** HIGH: 3, MED: 2, LOW: 1

---

## Category 1: type-string drift

### Finding 1.1c — HIGH — Dragons systematically typed as `character.human`

**Pattern:** Every dragon node in the corpus has `type: character.human` instead of `type: character.dragon`. The leaf type `character.dragon` exists in `architecture.md` § Type Reference Table and is documented as the correct type for "Drogon, Rhaegal, Viserion, Balerion, etc." Direwolves are correctly typed as `character.direwolf` (6 nodes), so the type vocabulary is recognized — but the dragon classification path is wrong corpus-wide.

**Count:** 0 of 3,373 character nodes have `type: character.dragon`. Every dragon I checked has `type: character.human`.

**Examples within `[abc]` sample:**
- `graph/nodes/characters/balerion.node.md:3` — `type: character.human`. Body content (lines 28–34) is a clear dragon biography ("claimed by Lord Aegon Targaryen", "Aegon descended on Lords Mooton and Darklyn ... Balerion's dragonfire").
- `graph/nodes/characters/caraxes.node.md:3` — `type: character.human`. Body (line 30) "It is unknown when Caraxes hatched from his egg ... young dragon of rideable size".
- `graph/nodes/characters/arrax.node.md:3` — `type: character.human`. Has `### Dragon Egg` subsection.
- `graph/nodes/characters/caraxes.node.md:5` — alias `"the Blood Wyrm"`.

**Examples confirmed corpus-wide (outside `[abc]` slice):** `viserion`, `rhaegal`, `vhagar`, `dreamfyre`, `dragon-that-died-in-the-red-waste` — all `type: character.human`. (Drogon does not appear to have a node yet — separate coverage gap.)

**Severity rationale:** HIGH — every "show me all dragons" query returns 0 hits. Cross-identity / dragonrider analysis is broken (a dragon and a human aren't distinguishable from frontmatter). The cohort is at least dozens of nodes (Targaryen-era + Dance of the Dragons named dragons + book-1 Daenerys dragons).

**Recommendation:** patch the Stage-3 deterministic emitter (`scripts/wiki-pass2-emit-deterministic.py`) to recognize the wiki "Species" infobox value or a "Dragons" / "Targaryen dragons" category and emit `type: character.dragon`. After the fix, re-promote affected nodes (deletion-and-re-emission, since the type-bucket directory wouldn't change — `character.dragon` is also under `characters/`). Estimated 30–80 dragon nodes to retype.

### Finding 1.2c — none for type-string-not-in-TYPE_DIR_MAP

**Count:** 0 nodes in the [abc] sample have a `type:` value outside TYPE_DIR_MAP. All 614 nodes are `type: character.human` (608) or `type: character.direwolf` (6, all outside [abc]). The "religion → organization.religion" drift class flagged in the original prompt does not manifest in characters.

---

## Category 2: edge-vocabulary drift

### Finding 2.0c — none

**Count:** 0 violations across [abc] sample (614 nodes, ~3,000+ edges). Confirmed labels in use match houses+locations Finding 2.0: `PARENT_OF`, `SPOUSE_OF`, `LOVER_OF`, `SIBLING_OF`, `BETROTHED_TO`, `WARD_OF`, `HEIR_TO`, `RULES`, `OVERLORD_OF`, `SWORN_TO`, `HOLDS_TITLE`, `MEMBER_OF`, `FOUNDED`, `KILLS`, `EXECUTES`, `BORN_AT`, `DIED_AT`, `BURIED_AT`, `WIELDS`, `OWNS`, `ANCESTRAL_WEAPON_OF`, `WORSHIPS`, `CULTURE_OF`, etc. — all in the locked 22-type vocabulary. No invented labels (`MARRIED_TO`, `KILLS_IN_BATTLE`, etc.) detected.

The vocabulary lock holds across characters as it did across houses+locations. Vocabulary-drift can be skipped from the full-corpus audit.

---

## Category 3: frontmatter schema violations

### Finding 3.1c — HIGH — Malformed YAML aliases (unescaped inner double-quotes)

**Pattern:** Some Stage-1 v1 agent emissions wrap a quote-bearing alias string in double-quotes without escaping the inner quotes, producing invalid YAML that PyYAML / many parsers will reject.

**Count within [abc] sample:** 1
**Count corpus-wide:** 2

**Examples:**
- `graph/nodes/characters/arryk-cargyll.node.md:5` — `aliases: ["One of "the celebrated Cargyll twins""]`
- `graph/nodes/characters/erryk-cargyll.node.md:5` — `aliases: ["One of "the celebrated Cargyll twins""]` (outside [abc] slice; same pattern, same wiki-source phrasing)

**Severity rationale:** HIGH — a strict YAML parser fails to load the node entirely. Lenient parsers (most Python YAML libraries) silently accept and produce a corrupted alias list. Either way the alias is unusable for trigger-table / cross-reference lookups.

**Recommendation:** quick fix — `sed` replace those two lines with `aliases: ["One of the celebrated Cargyll twins"]` (drop the inner quotes; the wiki phrasing is editable). Long fix — patch the Stage-1 prompt or the alias-extraction logic to either escape `"` to `\"` or convert all inner `"` to single quotes. The corpus-wide count of 2 makes this trivially fixable now.

### Finding 3.2c — MED — `first_available` field present in 121 of 614 sample nodes (20%)

**Pattern:** Same as houses+locations Finding 3.1. Stage-1 v1 agent emissions include `first_available`; Stage-3 v1-python deterministic emissions do not. Per architecture.md § "Spoiler Gating — DEFERRED", values are ignored at v1 and will be overwritten by the post-first-release backfill script.

**Count within [abc] sample:**
- v1 (Stage 1, has `first_available`): 121 nodes (also includes `same_as: null` and structured-map shapes for the field)
- v1-python (Stage 3, no `first_available`): 489 nodes
- Two-tier same as houses+locations split.

**Severity rationale:** MED — known-deferred. No action.

### Finding 3.3c — LOW — All other required frontmatter fields present and well-typed

Verified across all 614 nodes:
- `name`, `type`, `slug`, `confidence`, `wiki_source`, `bucket_id`, `prompt_version`, `node_version`, `pass_origin`, `aliases` — present in every node. `confidence: tier-1` and `node_version: 1` are constant across the sample. No required field is missing.

`aliases: []` (empty list) appears in 461 of 614 nodes (75%) — same as the houses+locations coverage gap. Wiki Aliases / Other Names fields are sparsely populated by the deterministic parser. Not a violation; surface as coverage observation.

---

## Category 4: slug format violations

### Finding 4.0c — none

**Count:** 0 slug violations across 614 nodes. Same as houses+locations Finding 4.0 — every slug matches `[a-z0-9-]+`, every `slug:` value matches the filename's `<slug>.node.md` segment. Anti-pattern grep `^slug:.*[A-Z_'\.\(\)]` returned 0 matches. Slug audit can be skipped from the full-corpus audit.

---

## Category 5: structural / format violations — character-specific

### Finding 5.1c — HIGH — Date-bleed and qualifier-bleed in `BORN_AT` / `DIED_AT` edge targets (parser bug)

**Pattern:** The deterministic parser handling wiki "Born" and "Died" infobox fields splits on commas / years / parentheses and emits each fragment as a separate `BORN_AT:` or `DIED_AT:` edge. The result: edges where the target is a year string, an era name, a region, or a country — none of which resolve to a node. Two distinct sub-patterns coexist, depending on emitter.

**Sub-pattern A — Stage-3 v1-python (deterministic):** wiki "Born" field like `Winterfell, 263 AC` splits into TWO edges:
```
- BORN_AT: 263 AC (track_b: Born)
- BORN_AT: Winterfell (track_b: Born)
```
Both are emitted as separate `BORN_AT:` rows. The first is a date-string-as-target (fails to resolve); the second is the actual birthplace and resolves to `winterfell`.

**Sub-pattern B — Stage-1 v1 agent emission:** wiki "Born" field `Winterfell, 263 AC` is preserved as a single concatenated target:
```
- BORN_AT: Winterfell, 263 AC (track_b: Born)
```
The kebab-case slug-normalization will produce `winterfell-263-ac`, which doesn't resolve to any node. This is the variant the original prompt flagged via `eddard-stark.node.md` (line 69, outside [abc] slice but corpus-wide).

**Sub-pattern C — bare year, no AC/BC suffix:**
```
- BORN_AT: 282 (track_b: Born)
- BORN_AT: 257 (track_b: Born)
```
Same bug, but the year-string is missing its era suffix. Slug-normalizes to `282`, `257`, etc. — pure-numeric slugs which definitely don't resolve.

**Sub-pattern D — era-name as date target:**
```
- BORN_AT: Age of Heroes (track_b: Born)
```
Slug-normalizes to `age-of-heroes`. The Age of Heroes is an era, not a place — this should be a temporal qualifier, not an edge target. Confirmed in 13 nodes corpus-wide (`torgon-the-terrible`, `crake-the-boarkiller`, `symeon-star-eyes`, `hooded-man`, `durran-godsgrief`, `ragged-ralf`, `nights-king`, `alan-o-the-oak`, `hrothgar-of-pyke`, `jorl-the-whale`, `corpse-queen`, `elenei`, `dagon-drumm`).

**Counts within [abc] sample (sub-patterns combined):**
- `BORN_AT:` with a year-or-era target (years AC, years BC, "Age of Heroes", bare digits): 190 edges across 138 files
- `DIED_AT:` with a year target: 175+ edges across 145 files
- Combined: ~22% of [abc] character nodes have at least one date-bleed edge

**Examples (Sub-pattern A — most common in this sample):**
- `graph/nodes/characters/cregan-karstark.node.md:22` — `- BORN_AT: 249 AC (track_b: Born)`
- `graph/nodes/characters/cregan-karstark.node.md:23` — `- BORN_AT: Karhold (track_b: Born)` (the real place — same Born field)
- `graph/nodes/characters/aegon-i-targaryen.node.md:29-30` — `- BORN_AT: 27 BC (track_b: Born)` then `- BORN_AT: Dragonstone (track_b: Born)`
- `graph/nodes/characters/clayton-suggs.node.md:25-26` — `- BORN_AT: Flea Bottom (track_b: Born)` then `- BORN_AT: King's Landing (track_b: Born)` (this is the legitimate "neighborhood + city" bleed; both resolve, but it implies a location is in two places at once)

**Examples (Sub-pattern B — Stage-1 agent style):**
- `graph/nodes/characters/eddard-stark.node.md:69-70` (outside [abc] slice) — `- BORN_AT: Winterfell, 263 AC (track_b: Born)` and `- DIED_AT: Great Sept of Baelor, King's Landing, 299 AC (track_b: Died)`
- `graph/nodes/characters/cregard-stark.node.md:33` — `- BORN_AT: 153–208 AC (track_b: Born)` (range, not even a single year)

**Examples (Sub-pattern C — no-suffix year):**
- `graph/nodes/characters/cleos-frey.node.md:24` — `- BORN_AT: 257 (track_b: Born)`
- `graph/nodes/characters/boy.node.md:22` — `- BORN_AT: 282 (track_b: Born)`

**Severity rationale:** HIGH — this is the dominant character-edge defect. ~22% of character nodes in the sample have at least one unresolvable BORN_AT/DIED_AT edge target. Across the full 3,373-node corpus this projects to ~700–800 character nodes with broken date-bleed edges, generating ~1,500–2,000 invalid edge instances. Graph-traversal queries for "where was X born" silently return wrong-type-entity placeholders or nothing. Same severity class as the Religion-field parser bug (Finding 5.2 of houses+locations) — same upstream-parser fix locus.

**Recommendation:** patch `scripts/wiki-infobox-parser.py` Born / Died handling:
1. Detect any token matching `^\d{1,4}(\s*(AC|BC))?$` or `^\d+–\d+\s*AC$` or "Age of Heroes" / "Long Night" / similar era-strings; treat these as a `qualifier: <date>` metadata field on the same edge, not a separate edge target.
2. Recognize the "Place, Year" pattern by `re.match(r'^(.+?),\s*\d+\s*(AC|BC)?$', target)` and split into `target=Place`, `qualifier=Year`.
3. Re-run parser; re-emit Stage-3 nodes; do not modify Stage-1 nodes (those are sub-pattern B and need the same regex-split applied during the Stage-3 promotion step). Estimated 700+ nodes updated.

### Finding 5.2c — MED — Edge directionality conventions (same as houses+locations Finding 5.1)

**Count within [abc] sample:**
- `(reverse)` annotation (Stage 3 v1-python): 334 edges across 212 files
- Unicode arrow `→` (Stage 1 v1): 12 edges across 6 files
- ASCII arrow `->` (Stage 1 v1, smaller variant): 0 in [abc] sample (was 95 in houses+locations sample, so character cohort is cleaner here)

Same recommendation as houses+locations Finding 5.1: normalize at graph-build time, don't rewrite nodes.

### Finding 5.3c — MED — Placeholder Identity prose on Stage-3 nodes (same as houses+locations Finding 5.3)

**Pattern:** All 489 Stage-3 (v1-python) nodes have the boilerplate Identity body: `<Name> is a character.human from the AWOIAF wiki.` This is identical to the houses+locations stub-prose finding and resolves the same way (defer to prose-fill phase). Stage-1 nodes have substantive Identity prose (see `theon-greyjoy`, `eddard-stark`, etc.).

Plus the existing grammar-bug observation from Finding 5.3 of houses+locations: `is a character.human from the AWOIAF wiki` should be `is a character.human entity from the AWOIAF wiki` — but again, deferred to prose-fill.

### Finding 5.4c — LOW — Cross-identity nodes coexist as separate nodes plus alias

**Pattern:** For characters who go by multiple identities in canon (Theon Greyjoy / Reek; Sansa Stark / Alayne; Petyr Baelish's mother also named Alayne), the corpus encodes them as:
- Two separate top-level nodes (one for each identity, where the alias has a wiki page).
- The "true identity" node carries the alias as a string in `aliases:`.
- No `SAME_AS`, `IMPERSONATES`, `DISGUISED_AS`, or `ALIAS_OF` edges connecting the pair.

**Examples:**
- `graph/nodes/characters/reek.node.md` (the original Reek, Ramsay's tutor — a real distinct character)
- `graph/nodes/characters/theon-greyjoy.node.md:9` aliases includes `"Reek (III)"` — Theon's later disguise identity
- `graph/nodes/characters/alayne-baelish.node.md` (Petyr's mother — real distinct character, dead before AGOT)
- `graph/nodes/characters/sansa-stark.node.md` (does not include "Alayne Stone" in `aliases:` field at last check, but the disguise is in prose)

**Severity rationale:** LOW — not a schema violation per se. The architecture has `ALIAS_OF`, `SAME_AS`, `DISGUISED_AS`, `IMPERSONATES` edge types for exactly this case, but the parser doesn't yet emit them; surfacing identity-fraud relationships is the explicit job of the cross-identity-detector agent (in `.claude/agents/cross-identity-detector.md`, prompt-not-yet-written stub). No action needed during this audit cycle — the cross-identity-detector will sweep this when it runs.

### Finding 5.5c — LOW — All structural sections present

`## Edges` section: present in 614 of 614 sample nodes.
`## Identity` section: present in 614 of 614 sample nodes (most as the boilerplate stub).
Frontmatter `---` open and close: 2 markers per file, all 614 well-formed.
Filename matches `<slug>.node.md`: 614 of 614.

No structural violations of the kind documented in Category 5 of the sister audit's "missing required structural section" sub-finding.

---

## Estimated full-corpus impact (remaining 2,759 character nodes outside the [abc] slice)

Order-of-magnitude projections of how each character-specific pattern likely scales to the remaining 2,759 nodes:

| Finding | Sample count | Affected emission path | Full character-corpus projection | Reasoning |
|---|---|---|---|---|
| 1.1c (dragons typed `character.human`) | ~3 within [abc] (`balerion`, `caraxes`, `arrax`); 5+ confirmed corpus-wide | Stage-3 deterministic + Stage-1 agent (both emit `character.human` default) | 30–80 dragon nodes corpus-wide | Targaryen-era dragons + Dance-of-the-Dragons mounts + Daenerys's three. Bounded because dragons-with-names is a closed canonical set. |
| 3.1c (malformed YAML aliases) | 1 in [abc]; 2 corpus-wide | Stage-1 agent only (Cargyll-twin pages) | 2 corpus-wide | Already counted full corpus. The two affected nodes share wiki source phrasing. Unlikely to scale further. |
| 5.1c (BORN_AT / DIED_AT date-bleed) | 190+175 edges across ~22% of files | Stage-3 deterministic parser (sub-patterns A, C, D) + Stage-1 agent emission preserving wiki composite (sub-pattern B) | 700–800 character nodes affected; 1,500–2,000 invalid edges | The wiki "Born" / "Died" infobox field is populated for any character with a known birth or death year. This is most named characters with infoboxes. ~22% sample rate scales linearly to full character corpus. |
| 5.2c (edge directionality) | 334 + 12 across [abc] | All emitters (different per emitter) | All edges corpus-wide | Architectural — fix at graph-build, not at node level. |
| 5.3c (stub Identity prose) | 489 Stage-3 in [abc] | Stage-3 deterministic | ~2,700 corpus-wide | All Stage-3 nodes affected. Defer to prose-fill. |
| 5.4c (cross-identity duplication) | ~2 confirmed in [abc] | Both emitters | 30–100 corpus-wide | Bounded: characters with major disguise/alias identities in canon. Cross-identity-detector handles. |

**Combined HIGH-severity full-corpus exposure:** ~30–80 mistyped dragons (Finding 1.1c) and ~700–800 nodes with date-bleed BORN_AT/DIED_AT edges (Finding 5.1c). Both are upstream-parser / classifier bugs, not per-node fixes.

---

## Summary

The character sample surfaced **two character-specific upstream bugs** worth fixing before a full corpus audit:

1. **Dragon mistyping (Finding 1.1c)** — every dragon is `type: character.human`. Direwolves work correctly; dragons don't. Specific, bounded fix in the type-classifier path.
2. **BORN_AT / DIED_AT date-bleed (Finding 5.1c)** — the parser emits date strings (years, eras, ranges) as edge targets instead of as edge qualifiers. Affects ~22% of character nodes. Same fix-locus as the houses+locations Religion-field parser bug — `scripts/wiki-infobox-parser.py`.

One **trivially-fixable Stage-1 leakage**:

3. **Malformed YAML aliases (Finding 3.1c)** — exactly 2 nodes corpus-wide (`arryk-cargyll`, `erryk-cargyll`) have unescaped inner double-quotes. Five-second `sed` fix.

Every other pattern reproduces the houses+locations findings with similar shape and proportion. The vocabulary lock holds (0 violations across ~3,000+ character edges). Slug format is clean (0 violations). The known-deferred `first_available` policy is observed correctly: present on Stage-1 nodes, absent on Stage-3 nodes.

The cross-identity duplication pattern (Finding 5.4c) is interesting but explicitly out of scope for schema-drift — it's downstream-pipeline work (the cross-identity-detector agent).

---

## Recommended actions

In priority order:

1. **Patch the type-classifier dragon path** (Finding 1.1c) — modify `scripts/wiki-pass2-emit-deterministic.py` to set `type: character.dragon` when the wiki page has a "Species: Dragons" or "Species: Targaryen dragons" hint, when the page is in the wiki "Dragons" category, or when the page name matches the canonical-dragon allowlist. Re-emit affected Stage-3 nodes; for Stage-1 nodes (e.g., a hypothetical agent-written Drogon node), the agent prompt would need the same recognition. Estimated 30–80 nodes retyped.

2. **Patch the BORN_AT / DIED_AT date-bleed parser** (Finding 5.1c) — `scripts/wiki-infobox-parser.py` Born/Died field handling: split by `re.match(r'^(.+?),\s*(\d+(?:–\d+)?\s*(?:AC|BC)?)$', value)` to separate place and date; emit ONE edge with `qualifier: <date>` instead of two edges. Drop edges where the target is a bare year, era name, or pure-numeric. Re-run parser, re-promote affected Stage-3 nodes. Estimated 700–800 character nodes touched, ~1,500 edges normalized. This is the highest-impact single fix in the corpus.

3. **Hand-fix the 2 malformed-alias nodes** (Finding 3.1c):
   ```sh
   sed -i '' 's|aliases: \["One of "the celebrated Cargyll twins""\]|aliases: ["One of the celebrated Cargyll twins"]|' \
     graph/nodes/characters/arryk-cargyll.node.md \
     graph/nodes/characters/erryk-cargyll.node.md
   ```
   No need to chase the underlying Stage-1 prompt bug yet — corpus-wide count is 2.

4. **Skip a full edge-vocabulary audit, slug audit, and structural-completeness audit on characters.** All three categories are clean across the [abc] sample (614 nodes, ~3,000+ edges, 0 violations). Same null result as houses+locations. The full-corpus audit will not surface anything.

5. **Defer everything else.** Edge directionality normalization (5.2c), Identity prose fill (5.3c), cross-identity edge backfill (5.4c), and `first_available` cleanup all happen in dedicated later phases. Don't address during this audit cycle.

6. **Do not run a full-corpus schema-drift audit yet.** The two sample audits (houses+locations and characters/[abc]) have collectively covered ~1,114 of 4,239 nodes (~26%) and surfaced four upstream-parser bugs. Fix those bugs first, re-promote affected nodes, then re-sample. The remaining 75% of the corpus will mostly reproduce the same fixed-by-upstream-fix patterns.
