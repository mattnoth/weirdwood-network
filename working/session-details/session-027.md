# Session 27 — Stage 3c audit cleanup + Tier 3 promotion campaign + Option C

> **Date:** 2026-04-30
> **Type:** Heavy execution + design — audit-driven cleanup, multi-pass promotion campaign, ending with one big architectural insight (parser is the bottleneck, not the scraper).
> **Outcome:** Graph 4,239 → 5,008 nodes (+769). Cat 1 orphan edges 7,784 → 2,955 (62% reduction). 8 commits. Session 27 was originally scoped as "run audits, fix what they surface" and grew into the full Tier 3 promotion campaign.

---

## How the session unfolded

### Setup — orienting after a multi-day gap

Session opened with a long handoff from Session 26 listing two parallel tracks (Track A pipeline construction, Track B chat UI). Matt asked "what's next?" and corrected my Track-A/B framing — Track B was the wiki infobox parser (already done in Session 26), not the chat UI which is downstream of both. I conflated them from the handoff. Real Track A = Pass 1 chapter mechanical extraction; real Track B = wiki infobox parser; chat UI = the eventual consumer.

Recommendation that emerged: warm up with the four read-only audit agents before picking either track. They already had full prompts written and would take audit reports to file, no graph mutations.

### Built scripts/graph-query.py first

Before launching audits, Matt asked whether I had a way to traverse the graph. I didn't. Took 5 minutes to delegate a read-only CLI primitive to script-builder:
- Outbound edges with target-resolution status (`[OK]` / `[ALIAS→]` / `[ORPHAN]`)
- Inbound references from cross-references.jsonl
- Slug-not-found suggestion path
- JSON output mode

Used it dozens of times for spot-checks throughout the session. Pure investigation primitive — no mutations.

Note added to `reference/architecture.md` § Artifact Formats by Consumer so future agents discover it. Decided NOT to memorize the script path in auto-memory (rule: file paths are derivable from project state).

### Sample schema-drift audits — found 5 parser bugs

Cost-conscious approach: ran schema-drift-auditor on **houses + locations sample (500 nodes)** instead of full corpus. Cost ~$5 vs ~$50 for full opus. Surfaced 9 findings; 3 HIGH severity were actionable parser bugs:

1. **Type-classifier `place.location` fallback** — wars (Spice War, Salt War, etc.), factions (Second Sons, Triarchy), Iron Throne all wrong-bucketed in `locations/`. Parser had no handling for `*_war*` patterns or for free-company / political-alliance pages.
2. **Religion-field parenthesized-region bleed** — `Faith of the Seven; Old gods (North); Drowned God (Iron Islands)` parsed as 5 separate WORSHIPS targets including bare "religions", "North", "Iron Islands". Parser was splitting on `(` instead of `;`.
3. **Various deferred items** — first_available on v1 nodes (deferred-policy), edge directionality variants (deferred to graph-build), stub Identity prose (deferred to prose-fill phase).

Then sample audit on **characters (614 of 3,373 nodes)** surfaced 3 more:
4. **BORN_AT/DIED_AT date-bleed** — "Winterfell, 263 AC" kept as single edge target; year strings, era names, comma-suffixed locations not separated. ~22% of characters affected, ~700-800 nodes corpus-wide.
5. **Dragon mistyping** — all dragons typed `character.human` instead of `character.dragon`. Parser's classifier didn't read the Species field.
6. **2 cargyll YAML alias nodes** — `aliases: ["One of "the celebrated Cargyll twins""]` (unescaped inner quotes; broke YAML).

Plus Matt's explicit decision when I flagged `*-guards` sub-page nodes:
7. **`*-guards` retyping** — "house guards aren't houses; retype as factions." 6 nodes affected.

### Parser fixes + targeted re-promotions (5 rounds)

Patched all 6 bugs in `scripts/wiki-infobox-parser.py`:
- Added `PAGE_NAME_TYPE_PATTERNS` regex list (`\bwar\b`, `\brebellion\b`, `\bconquest\b`, `\binvasion\b`, `\bguards$` → faction).
- Extended `ENTITY_TYPE_OVERRIDES` (Iron Throne → artifact; Triarchy + 4 sellsword companies → faction).
- Added `<small>`-tag-aware qualifier handling in `InlineTextExtractorHTML` for the religion-bleed fix.
- Added `_DATE_TEXT_RE` patterns for year ranges, year disjunctions, "or before/after", `<year> AC, <Place>` concatenations.
- Added `classify_by_species()` reading the Species infobox field for dragon detection.

Cargyll YAML aliases: edited directly twice (once before agent re-emit, once after the agent re-emission reverted my fix). Upstream parser bug noted as TODO — when alias contains inner double-quotes, emitter doesn't escape them.

Targeted re-promotions via `wiki-pass2-repromote-targeted.py` and `-targeted-2.py`:
- Round 1: 14 nodes (10 wars/factions/Iron Throne moved to correct dirs; 4 location nodes overwrote with clean WORSHIPS edges)
- Round 2 (the agent's own bundled run): 1,206 nodes total (1,137 Stage-3 full re-emit for date-bleed + 44 Stage-1 surgical edits + 19 dragons + 6 guards)

### Slug regression introduced + fixed in same session

`wiki-pass2-repromote-targeted-2.py` had two `slug = node_path.stem` lines. `Path.stem` on `arryk-cargyll.node.md` returns `arryk-cargyll.node` (only strips last `.md`). 1,120 re-emitted nodes ended up with `slug: <slug>.node` (the `.node` suffix bled into the slug field).

Caught immediately via Matt's spot-eye on a system-reminder showing the cargyll node frontmatter. Fixed both script lines (`stem.removesuffix(".node")`) and patched all 1,120 affected files via in-place sed. Verified 0 bad slugs remaining.

Lesson logged in todos: when writing future targeted-re-promote scripts, audit `Path.stem` usage on `*.node.md` paths.

### Stage 3a/3b/3c framing

After Matt observed "I still think these audits and fixes are in stage 3, or stage 4 needs to be split up into 4 and 5", added the Stage 3a/3b/3c naming to `working/runbooks/wiki-pass2-pipeline.md`:

- **Stage 3a** = deterministic skeleton emit (done Session 26)
- **Stage 3b** = deterministic prose extract (done Session 26)
- **Stage 3c** = post-emission audit cleanup (corrective — fixes existing emissions; this session)
- **Stage 4** = additive (discovers NEW edges from prose; not yet started)

Boundary: corrective vs additive. Stage 3c never modifies the deterministic skeleton bytes; it patches the parser then re-emits. Stage 4 emits to `prose-edges/<slug>.edges.jsonl` siblings, never touches existing nodes.

### Three full-corpus audits in parallel

After Stage 3c parser-fix work landed, ran the three remaining read-only audits in parallel as background subagents:
- `orphan-edge-finder` — 18,681 edges checked, 7,784 Cat 1 / 784 Cat 2 / 24 stale-religion-bleed / 199 date-bleed
- `duplicate-detector` — 2,884 candidates total but 0 shared-wiki-source duplicates (Stage 3c de-conflict worked)
- `citation-validator` — 5 malformed cite_ref classes, 11 bare `(wiki:Raffc9)` Stage-1 emission bugs, ~3,400 URL-encoded cite_ref strings validated as wiki-literal not noise

All three agents flagged that they couldn't do full sweeps (read-only via Read/Write/Glob/Grep, no Bash for O(n²) operations). They prepared Python scripts for the orchestrator to run. I ran the prepared scripts to get full-corpus numbers.

### Aha moment on alias-resolver investigation

Matt asked me to investigate the 31 Cat-2 alias-mismatch entries. I checked the resolver and found 1,175 entries already populated (the audit was correctly using existing entries; 784 edges weren't broken — they resolve via the resolver, just labeled MED-severity to flag that the future graph-build layer needs to consult the resolver after a direct-slug miss).

Two BAD entries surfaced:
- `ser → gregor-clegane` — title bridging to one specific character (Gregor's "Ser Gregor" alias kebab-cased and registered as `ser`). 693 edges flowing through this bad mapping.
- `aegon-targaryen → pisswater-prince` — bare-name disambiguation pinned to the babe-swap victim. 25 edges.

Built a patch into `wiki-pass2-build-alias-resolver.py`: `TITLE_WORD_SLUGS` filter + `BARE_DISAMBIGUATION_THRESHOLD=3` filter. Removed both bad entries on next rebuild.

When I ran the rebuild after the wildlings/free-folk merge later, found a new bug: `Wildlings` and `wildlings` both kebab to `wildlings`, producing duplicated single-candidate list which the dedup-after-length-check logic incorrectly classified as "ambiguous". Bug noted; manual workaround was to put one alias not two.

### Tier 3 promotion campaign

`working/tier3-promotion-plan.md` drafted before Pass A as a coherent multi-pass plan. Five passes scoped:
- A — Titles (highest impact, 256 unique slugs / 1,154 edges)
- B — Cultures (small)
- C — Religions/Gods (small)
- D — Character backfill (largest residual)
- E — Audit residual (cleanup)

#### Pass A — 470 title nodes promoted

Filtered Cat 1 TSV for HOLDS_TITLE targets, cross-referenced page-index.jsonl. 528 candidate slugs; 470 had wiki pages, 58 backlogged (no wiki page — entities mentioned in prose without standalone pages: `captain`, `commander`, `brother`, etc.).

91 → 561 title nodes. Cat 1 orphan edges: 7,784 → 5,274 (-2,510, 32% drop). HOLDS_TITLE orphan slugs: 528 → 58 (89% reduction).

Caveat caught: 19 of 470 were unreferenced after promotion — likely faction misclassifications (`city-watch-braavos`, `sons-of-the-harpy`, `poor-fellows`, `sparrows`, `antler-men`, etc.). Logged for Pass E cleanup; non-blocking.

Side fix: 201 nodes had space-form cite_refs (`wiki:Prince of Dragonstone.cite_ref-X`) which the agent inline-patched to underscored form. Script also patched.

#### Pass B + C parallel — 52 cultures + 16 religions/gods

Ran both in parallel since they don't overlap on slugs.

Pass B (Cultures): 52 nodes promoted via `organization.faction` type to `factions/` (per Tier 2 convention; `concept.culture` in TYPE_DIR_MAP routes to `concepts/` not `cultures/`, so fell back). Cat 1: 5,274 → 3,419 (-1,855). CULTURE_OF residual: 2 (mixed, myrhish — no wiki page).

Variant duplicates promoted as separate nodes — `andal/andals`, `dornish/dornishmen/dornishman`, `lhazareen/lhazarene`, `lysene/lyseni`, `stormlander/stormlanders`. Same culture, separate wiki pages. Logged for Pass E merge.

Pass C (Religions/Gods): 16 promoted including the 7 Seven aspects (Mother, Maid, Smith, Warrior, Crone, Stranger, Father Above) plus Black Goat, Lion of Night, Many-Faced God, Storm God, Trios, Crab King, Boash. religions/ count: 4 → 20.

6 alias additions to alias-resolver.json: `old-gods → old-gods-of-the-forest` (covers the 10 stale-religion-bleed edges), `crone → crone-the-seven`, `warrior → warrior-the-seven`, `father → father-above`, `maiden → maid`, `stranger-the-seven → stranger`. WORSHIPS Cat 1 orphans: 3 → 0.

Combined Cat 1 after B+C: 3,413 (down 1,861 edges).

#### Pass D — 184 character backfill nodes

Smaller result than expected — 184 of 564 candidate slugs had wiki pages; 380 backlogged. The wiki simply doesn't have pages for many minor mentioned characters in family trees. Promoted 184 (1 dragon: Drogon).

184 backlog entries include 28 date-like HEIR_TO artifacts (`209-ac`, `130-ac`) — real parser bug surfaced for Pass E to fix.

characters/ count: 3,373 → 3,557. Cat 1: 3,413 → 2,968.

#### Pass E Phase 1 — debt cleanup

4 sub-tasks bundled into one delegation:

- **Task 1 — 19 misclassified titles:** 15 migrated to `factions/` (city-watch-*, sons-of-the-harpy, sparrows, etc.); 4 kept as title (bastard, hedge-knight, sellsword, lord-of-widows-watch).
- **Task 2 — Culture variant merges:** 5 canonical updates, 6 variants deleted with aliases preserved on canonicals (andals, dornishmen, lhazareen, lyseni, stormlanders).
- **Task 3 — 14 religion-bleed locations re-emitted:** stale `WORSHIPS: Old gods` etc. now resolve via the new old-gods alias. Stale religion-bleed: 14 → 0.
- **Task 4 — HEIR_TO date-bleed parser fix:** extended `is_born_died_field` filter to Heir/Heirs fields. 425 nodes had bare-number HEIR_TO edges removed (`131` from `131-134 AC` format).

#### Option C — Stage-1 character prose-only re-emission

Matt overrode the original deferral. Hybrid approach: replace prose body with Stage-3 deterministic wiki-extracted prose, preserve `## Edges` section verbatim.

544 of 591 Stage-1 character nodes processed (47 stub-wiki skipped). Edge count invariant HELD: 3,495 = 3,495 (zero edge loss). Prose mean: 1,067 → 6,072 chars (×5.7). Eddard Stark: 3,319 → 47,693 chars (×14.4).

Importantly, the spot-check finding from earlier was misleading: jon-snow's "lost edges" (SIBLING_OF, WIELDS) weren't actually formal `## Edges` bullets — they were prose-embedded narrative mentions. Option C preserved the 8 formal edges; the prose-mentioned ones were never structured edges.

### The big architectural finding — parser is the bottleneck

End of session, after Option C committed, Matt asked about WIELDS and named valyrian steel swords. Investigation revealed:

- **15+ named swords (Longclaw, Blackfyre, Ice, Dawn, etc.) are MISSING from the graph.**
- **Only 3 WIELDS edges total** — all Stage-1 prose-mentions, not parser-emitted.
- **WIELDS is NOT in the parser's FIELD_EDGE_MAP.**
- **`graph/nodes/artifacts/` has exactly 1 node** (Iron Throne).

When Matt asked "do these exist in our sources/wiki or did playwright miss them?" I checked directly. **All sword pages and book pages ARE in the wiki cache.** Playwright didn't miss anything. The failure is the parser:
- 70.4% of pages (12,434 of 17,657) classify as `entity_type_guess: 'unknown'`.
- Longclaw's HTML has NO `class="infobox"` div, no template hint, no infobox table — pages are PROSE-ONLY.
- Same failure mode for books (Fire and Blood, The Seven-Pointed Star, etc.).

So the fix isn't "extend the infobox detector" (no infoboxes to detect) — it's `ENTITY_TYPE_OVERRIDES` for confirmed-real entity names, mirroring the Session 27 Iron Throne fix. The wiki cache + page-index already has these pages; they just need name-pattern triage rules to escape the `unknown` bucket.

This becomes the critical first step for Phase 2.

---

## Counts

| Metric | Start | End |
|---|---|---|
| Total nodes | 4,239 | 5,008 (+769) |
| Cat 1 orphan edges | 7,784 | 2,955 (62% drop) |
| Cat 2 alias-mismatch | 784 | 268 (mostly absorbed by alias-resolver patches) |
| Stale religion-bleed | 24 | 0 |
| Date-bleed orphans | 199 | 41 (parser-floor) |
| Edge vocabulary violations | 0 | 0 (lock holds) |
| Slug-format violations | 0 | 0 |
| Title nodes | 91 | 546 |
| Faction nodes | 37 | 97 |
| Religion nodes | 4 | 20 |
| Character nodes | 3,373 | 3,557 |
| Artifact nodes | 0 | 1 (Iron Throne — gap remains) |

**8 commits total this session** (including the small follow-on for the audit + summary).

## Key decisions made

1. Deferred full-corpus schema-drift audit; sample audits caught all categories at ~$10 vs ~$50.
2. Stage 3a/3b/3c naming added to canonical pipeline runbook.
3. Stage 1 character carve-out — never re-emit edges via Stage 3 to preserve agent-derived signal until Stage 4.
4. Option C overrode the deferral for prose enrichment only (preserves edges).
5. Variant culture duplicates accepted in Pass B, then merged in Phase 1 with aliases on canonicals.
6. The 19 unreferenced "title" promotions were faction misclassifications — migrated in Phase 1 rather than left as noise.
7. `*-telltale` and `*-theories` sub-pages deleted (not first-class entities).
8. Bare ambiguous aliases (`ser`, `aegon-targaryen`) filtered from resolver via title-word and bare-disambiguation patterns.

## Things rejected / not done

- **Full schema-drift audit on the 5,000-node corpus** — sample work covered all categories cheaply.
- **Stage 1 character full re-emission** — would lose narrative-prose edges; deferred to Stage 4.
- **`concept` type promotion for governance terms** — deferred per existing recommendation.
- **`culture` type with own directory** — kept `organization.faction` per Tier 2 convention; future taxonomy split is separate.
- **iTerm-tab launcher for audit agents** — built nothing; used background subagents with `tail -f` instructions instead. Daemon is planned but not yet built.

## What surprised

- **Stage 1 character "lost edges" framing was overstated.** Jon Snow's WIELDS and SIBLING_OF were prose-embedded narrative, not formal Edges bullets. Option C revealed this: the carve-out was based on a wrong assumption about edge format.
- **70.4% of wiki pages classify as `unknown`.** Most are appropriately so (list pages, appendices), but the figure surprised me. The Tier 3 promotion campaign promotes from this unknown bucket via name-pattern overrides; it's the only path until/unless the parser learns more infobox templates.
- **The Playwright scraper was thorough.** Every page Matt thought might be missing was actually in the cache. Bottleneck has been the parser/classifier from the start.
- **Pass D was smaller than expected** (184 vs ~600-1,200 estimate) because the wiki simply lacks pages for many family-tree-mentioned minor characters.
- **`HEIR_TO: 209 AC`-style date-bleed** affected 425 nodes — same parser-bug class as BORN_AT/DIED_AT but in a different field.

## Continue prompts touched

- Created: `progress/continue-prompts/2026-05-01-tier3-pass-e-phase-2.md` for Phase 2 (books + named weapons + locations completeness + final audits).
- Updated this prompt at end of session with the books/weapons/parser-bottleneck framing as critical first step + 70% unknown-rate context + verified state + completed-pass commit history.
