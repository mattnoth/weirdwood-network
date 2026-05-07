# Schema-Drift Audit (Sample) — 2026-04-30

**Scope:** sample-based audit of `graph/nodes/houses/` + `graph/nodes/locations/` (~500 nodes of 4,239 total)
**Purpose:** surface drift categories before committing to full-corpus audit
**Nodes scanned:** 500 (322 houses + 178 locations)
**Total findings:** 9 distinct patterns (HIGH: 3, MED: 4, LOW: 2)
**Method:** read-only grep across required frontmatter fields, type values, edge labels, slugs, and structural sections. No node was modified.

---

## Category 1: type-string drift

### Finding 1.1 — HIGH — Non-place entities promoted into `locations/` with `type: place.location`

**Pattern:** Wars, factions, artifacts, and political alliances were classified as `place.location` and sorted into `graph/nodes/locations/`. The `type:` value is itself in TYPE_DIR_MAP (so it doesn't fail the literal type-string check), but the entity is in the wrong type bucket entirely.

**Count within sample:** at least 8 nodes in `locations/`

**Examples:**
- `graph/nodes/locations/iron-throne.node.md` — `type: place.location`, but it's an artifact (the throne object). Promoted via `bucket_id: houses-major-recovery`.
- `graph/nodes/locations/second-sons.node.md` — `type: place.location`, but it's a sellsword company (faction).
- `graph/nodes/locations/triarchy.node.md` — `type: place.location`, but it's a political alliance / faction (Tyrosh, Lys, Myr).
- `graph/nodes/locations/war-for-the-dawn.node.md` — `type: place.location`, but it's a prophesied/recurring war (event.war or concept.prophecy).
- `graph/nodes/locations/spice-war.node.md`, `salt-war.node.md`, `third-turtle-war.node.md`, `second-turtle-war.node.md`, `war-of-three-princes.node.md`, `war-on-dagger-lake.node.md` — wars all classified `place.location`.

**Severity rationale:** HIGH — these are downstream-traversal-breaking. A query for "all events" misses these wars; "all factions" misses Second Sons and Triarchy; the Iron Throne is not findable as an artifact.

**Recommendation:** the upstream classifier (or its bucket-routing rules) emits `place.location` as a fallback when no other type is determined for a wiki page. Audit the classifier's default-type path and add disambiguation for `_war`, `_war_of_*`, `*_war`, free-company / sellsword company patterns, and the `Iron_Throne` page specifically. Consider migrating these out of `locations/` as a one-time correction once the typing is fixed.

### Finding 1.2 — none for valid type-string violations

No nodes in the sample have a `type:` value outside TYPE_DIR_MAP. All 322 houses are `organization.house`; all 178 locations are `place.location` (151) or `place.region` (27). The "religion → organization.religion" drift class flagged in the prompt does NOT manifest in the houses/locations sample.

---

## Category 2: edge-vocabulary drift

### Finding 2.0 — none

**Count:** 0 violations in 1,562 edges across the sample (1,366 house edges + 196 location edges).

Every edge label in the sample matches the locked 22-type vocabulary in `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping". Confirmed labels in use: `SEAT_OF`, `RULES`, `RULES (reverse)` (legacy formatting variant), `REGION_OF`, `HOLDS_TITLE`, `HEIR_TO`, `OVERLORD_OF`, `OVERLORD_OF (reverse)`, `CADET_BRANCH_OF`, `ANCESTRAL_WEAPON_OF`, `ANCESTRAL_WEAPON_OF (reverse)`, `FOUNDED`, `SWORN_TO`, `WORSHIPS`, `SEAT_OF (reverse)`. Every label is in the 22-type lock.

**Note (reported under Finding 5.2):** the `(reverse)` annotation on edge labels is a stylistic variant produced by the v1-python deterministic emitter that doesn't appear in the v1 agent emissions. It's syntactically a vocabulary-extension if downstream parsers naively split on whitespace, but if the parser recognizes the label-token before the open-paren, it's fine. Surfaced as structural variant under Category 5, not vocabulary drift.

---

## Category 3: frontmatter schema violations

### Finding 3.1 — MED — `first_available` field present in 250 of 322 houses (78%) despite v1-deferred policy

**Pattern:** `architecture.md` § "Spoiler Gating — DEFERRED" states the field is **optional in v1 nodes** and that "existing values may be missing, in inconsistent shapes, or wrong" (parser-bug class). The agent prompts emit the field for v1 (Stage 1) nodes; v1-python (Stage 3) deterministic nodes correctly omit it.

**Count within sample:**
- 250 houses (all `prompt_version: v1`) have `first_available` — typically as a structured map (`book/chapter/source/pov`).
- 0 locations have `first_available` — all locations are `prompt_version: v1-python` deterministic.

**Examples:**
```yaml
# graph/nodes/houses/house-bar-emmon.node.md (lines 12-16)
first_available:
  book: ACOK
  chapter: 10
  source: cite_ref
  pov: Arya III
```
```yaml
# graph/nodes/houses/house-tuttle-telltale.node.md (line 12)
first_available: null
```

**Severity rationale:** MED — values are ignored at v1 but their presence is a known-bad-data class (per architecture.md). The deferred-backfill plan supersedes any current values. 61 of these are `first_available: null` (the parser couldn't derive anything — already known to be wrong).

**Recommendation:** when the deferred-spoiler-gating script runs post-first-release, it overwrites all 250 v1 values. Until then, no action — leave them. Do not invest agent context inferring or fixing these.

### Finding 3.2 — MED — Two distinct `prompt_version` values within same type bucket

**Pattern:** Houses split between `v1` (250 nodes, agent-synthesized Stage 1) and `v1-python` (72 nodes, Stage 3 deterministic + Tier recovery). All locations are `v1-python`.

**Count within sample:**
- Houses `v1`: 250
- Houses `v1-python`: 72
- Locations `v1-python`: 178

**Severity rationale:** MED — not a violation per se (architecture allows both as schema-versioned tags), but the two emitters produce divergent edge-format conventions (see Finding 5.1) and divergent Identity-prose content (see Finding 5.3). Consumers must handle both.

**Recommendation:** acceptable as-is for v1 release, but the prose-fill / edge-polish phase should normalize toward one canonical shape per node before any post-release schema bump.

### Finding 3.3 — LOW — All other required frontmatter fields present and well-typed

Verified across all 500 nodes:
- `name` — present in 500/500
- `type` — present in 500/500
- `slug` — present in 500/500
- `confidence` — present in 500/500 (always `tier-1`)
- `wiki_source` — present in 500/500
- `bucket_id` — present in 500/500
- `prompt_version` — present in 500/500
- `node_version` — present in 500/500 (always `1`)
- `pass_origin` — present in 500/500 (`pass2-wiki` for v1, `pass2-wiki-deterministic` for v1-python)
- `aliases` — present in 500/500 (always `[]` in this sample — likely a coverage gap to surface separately)

No required field is missing from any node in the sample.

---

## Category 4: slug format violations

### Finding 4.0 — none

**Count:** 0 slug violations across 500 nodes.

Every slug matches `[a-z0-9-]+`. No uppercase, no underscores, no apostrophes, no parentheses. Every `slug:` value matches the filename's `<slug>.node.md` segment. Verified by:
- `^slug: .*[A-Z_]` — 0 matches
- `^slug: [^a-z0-9-]*[A-Z_'\.\(\)]` — 0 matches

The kebab-case-from-wiki-page-title transform appears clean for this sample.

---

## Category 5: structural / format violations

### Finding 5.1 — MED — Edge directionality conventions inconsistent between emitters

**Pattern:** Three different conventions for expressing edge direction coexist:

1. **v1-python deterministic** (Stage 3): explicit `(reverse)` annotation on the label, e.g. `SEAT_OF (reverse): Winterfell (track_b: Seat)`. Source-target inferred from forward/reverse marker.
2. **v1 agent emissions** (Stage 1): Unicode arrow notation, e.g. `OVERLORD_OF: House Targaryen → House Bar Emmon (cite: ...)`. Both endpoints stated explicitly.
3. **v1 agent emissions, ASCII-arrow variant** (Stage 1, smaller subset): `OVERLORD_OF: House Lannister -> House Spicer (...)`. Same as variant 2 but with ASCII arrow.

**Count within sample:**
- Variant 1 (`(reverse)` annotation): 107 edges across 43 houses, 0 locations.
- Variant 2 (Unicode arrow `→`): 254 edges across 140 houses.
- Variant 3 (ASCII arrow `->`): 95 edges across 25 houses.

**Examples:**
- v1-python: `graph/nodes/houses/house-stark.node.md:31` — `- OVERLORD_OF (reverse): House Baratheon of King's Landing (track_b: Overlords) [AGOT]`
- v1 unicode arrow: `graph/nodes/houses/house-bar-emmon.node.md:46` — `- OVERLORD_OF: House Durrandon → House Bar Emmon (?–2 BC) (cite: ...)`
- v1 ASCII arrow: `graph/nodes/houses/house-spicer.node.md:37` — `- OVERLORD_OF: House Lannister -> House Spicer (track_b: Overlord)`

**Severity rationale:** MED — graph-build downstream needs to handle all three patterns. If the consumer assumes one shape, ~30% of house edges and 100% of location edges will be parsed incorrectly. None of this is wrong per the locked vocabulary (the labels are valid), but the *target extraction* pipeline must normalize.

**Recommendation:** define a canonical shape for the graph-build step (probably the v1-python `(reverse)` or a structured `source:`/`target:` pair) and write a normalizer that converts both arrow variants to it. Don't rewrite the node files yet — rewrite the consumer.

### Finding 5.2 — HIGH — Region/qualifier-bleed into WORSHIPS edge targets (parser bug)

**Pattern:** When a wiki Religion infobox field contains parenthesized region scoping (e.g. `Faith of the Seven; Old gods (North); Drowned God (Iron Islands)`), the deterministic parser splits on the parenthesis content and emits the region name as a separate `WORSHIPS:` target. The result is an edge that tries to resolve a region as a religion.

**Count within sample:** confirmed in at least 4 location nodes; pattern signature suggests more.

**Examples:**
- `graph/nodes/locations/seven-kingdoms.node.md:23` — `- WORSHIPS: North (track_b: Religion) [North]` (target "North" is a region, not a religion)
- `graph/nodes/locations/seven-kingdoms.node.md:25` — `- WORSHIPS: Iron Islands (track_b: Religion) [Iron Islands]` (target "Iron Islands" is a region)
- `graph/nodes/locations/pentos.node.md:20` — `- WORSHIPS: religions (track_b: Religion)` (the literal English plural noun "religions" became a target)
- `graph/nodes/locations/lys.node.md:20`, `tyrosh.node.md:20` — `- WORSHIPS: religions (track_b: Religion)` (same literal-noun bug)
- `graph/nodes/locations/valyrian-freehold.node.md:21` — `- RULES: Lords freeholder (track_b: Ruler)` (similar role-not-entity bug, RULES variant)

**Severity rationale:** HIGH — produces edges where the target slug literally cannot resolve to a node (`north`, `iron-islands`, `religions`). Downstream graph-build will either fail-loudly or silently create orphan target placeholders. Either way the graph is wrong.

**Recommendation:** patch `scripts/wiki-infobox-parser.py` Religion-field handling to (a) split on `;` not on `(` , (b) treat parenthesized text as a `qualifier` metadata field, not a separate edge, (c) skip non-proper-noun targets like the bare word "religions". This is upstream of the audit — flag for next parser-fix pass.

### Finding 5.3 — MED — All locations have placeholder Identity prose

**Pattern:** Every single location node has Identity content of the form "X is a place.location from the AWOIAF wiki." or "X is a place.region from the AWOIAF wiki." This is the deterministic emitter's stub, not a problem per se because the rich prose lives in subsequent sections (`## Origins`, `## Narrative Arc`, etc). However, if a downstream consumer extracts Identity-only as a node summary, it will get useless boilerplate plus wrong grammar ("a organization.house" — should be "an"; "a place.region" — should be "a", but is fine with the dot).

**Count within sample:** 178 of 178 locations (100%); 61 of 322 houses (19%) — the v1-python subset.

**Examples:**
- `graph/nodes/locations/winterfell.node.md:16` — `Winterfell is a place.location from the AWOIAF wiki.`
- `graph/nodes/houses/house-stark.node.md:16` — `House Stark is a organization.house from the AWOIAF wiki.`
- `graph/nodes/houses/house-cassel-theories.node.md:16` — `House Cassel/Theories is a organization.house from the AWOIAF wiki.` (also a non-canonical entity, see Finding 5.5)

**Severity rationale:** MED — not violating the architecture (Identity is required, not "Identity must be substantive"), but downstream consumers cannot rely on Identity for an entity summary.

**Recommendation:** either (a) the prose-fill agent backfills a real Identity sentence, or (b) downstream consumers learn to skip the deterministic stub and read prose from the next section. Out of scope for this audit; surface for the prose-fill phase.

### Finding 5.4 — MED — Empty `## Edges` section in 62 nodes (12.4% of sample)

**Pattern:** Some nodes have a `## Edges` heading but no edge bullets — typically because the source wiki page had no infobox or a sparse one.

**Count within sample:**
- Houses: 7 (all are `*-guards`-suffixed sub-pages: `house-bolton-guards`, `house-stark-guards`, `house-tully-guards`, `house-tyrell-guards`, `house-arryn-guards`, `house-targaryen-guards`, plus `house-with-the-red-door`).
- Locations: 55 (mostly regions, large geographic features, and the misclassified war/faction nodes from Finding 1.1).

**Examples:**
- `graph/nodes/houses/house-bolton-guards.node.md:18-21` — `## Edges` header followed by blank lines.
- `graph/nodes/locations/war-for-the-dawn.node.md:18-21` — same shape.
- `graph/nodes/locations/iron-throne.node.md:18-21` — same shape.

**Severity rationale:** MED — empty Edges section technically satisfies the structural requirement but conveys no graph information. Many of these (the wars, the guards) are also Finding-1.1 misclassifications; fixing the type bucketing may also fix the empty-Edges symptom.

**Recommendation:** the prose-edge-classifier (Stage 4 future) should backfill edges from the prose for these nodes. For now, note as a coverage gap.

### Finding 5.5 — LOW — Wiki-sub-page artifacts promoted as canonical entities

**Pattern:** Several nodes are derived from wiki **sub-pages** that aren't really standalone canonical entities — e.g. House X's "guards" page (a stub article describing the guardsmen of a house), `_(Telltale)` non-canon sub-pages for the licensed Telltale Games adaptation, and `/Theories` sub-pages collecting fan theories. Per Matt's documented rule "video-game-only entities excluded — Cyanide RPG / non-canon licensed-derivative pages are deleted from the graph, not demoted", at least 2 Telltale-suffix nodes should never have been promoted.

**Count within sample (houses):**
- `*-guards`: 6 nodes (`house-bolton-guards`, `house-stark-guards`, `house-tully-guards`, `house-tyrell-guards`, `house-arryn-guards`, `house-targaryen-guards`)
- `*-telltale`: 2 nodes (`house-tuttle-telltale`, `house-whitehill-telltale`) — should be deleted per video-game policy
- `*-theories`: 1 node (`house-cassel-theories`) — collects fan theories, not a real house

**Examples:**
- `graph/nodes/houses/house-tuttle-telltale.node.md` — `wiki_source: https://awoiaf.westeros.org/index.php/House_Tuttle_(Telltale)`. Identity says "appearing in the Telltale video game adaptation". Per documented policy this should not be in the graph.
- `graph/nodes/houses/house-cassel-theories.node.md` — wiki page is `House_Cassel/Theories`, a sub-section, not an entity.
- `graph/nodes/houses/house-bolton-guards.node.md` — wiki page is `House_Bolton_guards`, a sub-page describing guardsmen rather than a noble house.

**Severity rationale:** LOW — small absolute count, well-isolated by filename suffix, and the policy decision is already documented (just not enforced for these). Easy to surface and decide later.

**Recommendation:** delete the 2 `*-telltale` nodes per documented video-game policy. For the 6 `*-guards` and 1 `*-theories`, file as `audit-uncertain` for Matt — they may be legitimately separable (House guards as a sub-entity of House) or may need merging back into the parent house's node.

---

## Estimated full-corpus impact

Order-of-magnitude projections of how each pattern likely scales to the full 4,239-node corpus, based on which emission path produced the affected nodes:

| Finding | Sample count | Affected emission path | Full-corpus projection | Reasoning |
|---|---|---|---|---|
| 1.1 (mistyped non-place entities in `locations/`) | ≥8 | Stage 3 v1-python + Tier recovery | ~30–80 across whole graph | Stage 3 deterministic emits `place.location` as a default; characters/ and other dirs likely have analogous fallback bugs. Run a directory-vs-type sanity check on every dir. |
| 2.0 (edge-vocabulary drift) | 0 | — | likely 0 corpus-wide | Both the agent prompt and the deterministic parser hard-code the locked 22 labels. No drift detected and unlikely to appear elsewhere. |
| 3.1 (`first_available` present in v1) | 250 | Stage 1 v1 agent | ~855 corpus-wide | Stage 1 produced 855 nodes total per session notes. ~30% are houses; the entire 855-node set likely has this field. The v1-python 3,314-node set will not. |
| 3.2 (mixed `prompt_version` values) | 322/178 split | Stage 1 vs Stage 3 | Same split corpus-wide | Architectural, not a bug. |
| 5.1 (edge directionality formats) | 456 | All emitters (different per emitter) | All edges corpus-wide | Every edge in the graph follows one of the 3 patterns. Normalizer is needed regardless. |
| 5.2 (region/qualifier bleed in WORSHIPS) | ≥4 | Stage 3 v1-python parser | ~30–100 corpus-wide | Same parser writes all v1-python nodes. Look for ALL fields that take parenthesized scoping (Religion, Allegiance with date qualifiers, Heir with conditional notes). May affect 2–5% of all edges. |
| 5.3 (placeholder Identity prose) | 239 | Stage 3 v1-python | ~3,314 corpus-wide | All Stage 3 nodes use the same template. Until prose-fill runs, Identity will be stub for everyone. |
| 5.4 (empty Edges) | 62 | Stage 3 v1-python (sparse-infobox pages) | ~500–1,200 corpus-wide | Stub wiki pages, list articles, and disambiguation pages will all hit this. Worth one count run. |
| 5.5 (sub-page artifacts) | 9 | Stage 3 v1-python promotion | ~50–200 corpus-wide | Telltale/Theories/guards sub-pages, plus likely _(disambiguation)_ pages, _(fictional)_ qualifiers, and similar wiki-namespace artifacts. Run a `wiki_source` regex-grep across the full corpus for `_(Telltale|Theories|Cyanide|video_game)`-style suffixes. |

**Combined HIGH-severity full-corpus exposure:** ~30–100 type-misclassified entities (Finding 1.1) and ~30–100 region-bleed edge targets (Finding 5.2). Both are upstream-classifier / parser bugs, not per-node fixes. Full audit before fixing risks doing the same per-node remediation many times.

---

## Summary

The sample run successfully surfaced **two upstream bugs** worth fixing before a full audit:

1. **Type-classifier fallback bug** — wars, factions, artifacts, and political alliances are getting `place.location` as a default when the classifier can't determine type, then being sorted into `locations/`. Visible immediately in 8+ filenames in the sample.
2. **Religion-field parser bug** — parenthesized region scoping in `Religion:` infobox fields produces malformed edges where region names become religion targets. At least 4 confirmed instances; likely 30–100 corpus-wide.

Two **emitter-divergence patterns** worth normalizing **before** building the graph but **not** before promoting more nodes:

3. **Edge directionality** has 3 formats (`(reverse)`, `→`, `->`). Normalize at graph-build time, not at promotion.
4. **Identity prose** is stub-only for ~80% of nodes (all Stage 3 + a v1 subset). Defer to prose-fill phase.

The known-deferred concern about `first_available` is confirmed as expected — present on 78% of houses, all from Stage 1. The deferred-backfill script will overwrite all of them.

The sample found **no edge-vocabulary drift** and **no slug-format violations** — both are clean across 500 nodes and 1,562 edges. These categories likely don't need a full audit.

---

## Recommended actions

In priority order:

1. **Patch the type-classifier fallback** (Finding 1.1) — add explicit handling for `*_war*`, `Iron_Throne`, free companies, and political alliances before the `place.location` default kicks in. Run on full corpus and re-promote affected nodes. Estimated 30–100 affected.
2. **Patch the Religion-field parser** (Finding 5.2) — change the split logic to use `;` as separator and treat parens as qualifier metadata. Re-run wiki-infobox-parser on full corpus. Estimated 30–100 affected edges.
3. **Decide policy on `*-telltale`, `*-theories`, `*-guards` sub-page nodes** (Finding 5.5) — delete 2 Telltale per documented rule; ask Matt about guards and theories sub-pages. ~9 in sample, ~50–200 corpus-wide.
4. **Defer everything else.** Edge directionality normalization, Identity prose fill, empty Edges backfill, `first_available` cleanup all happen in dedicated later phases (graph-build, prose-fill, deferred-spoiler-backfill). Don't address those during this audit cycle.
5. **Skip a full edge-vocabulary audit and slug audit** — the sample shows zero drift in those two categories and the emission code paths are deterministic. Full-corpus audit there is unlikely to find anything.
6. **Re-run a sample audit on `characters/`** before deciding on full-corpus audit. Characters have the prompted-for edges (BORN_AT/DIED_AT location-with-date strings, the unescaped-quotes alias bug) that didn't manifest in houses/locations. Different patterns may emerge.
