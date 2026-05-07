# Session 28 — Path B Promotion Campaign + Parser Iteration (2026-04-30 → 2026-05-01)

> **Detail file** for Session 28. Full narrative including the Session 28 prelude (categorizer extension + categories backfill) which had been committed but not yet worklog-entered when this session began.
>
> **Session 28 in two acts:**
> - **Act 1 (committed at session start):** the categorizer/parser/category-backfill work that created the Path B framework.
> - **Act 2 (this conversation):** the Path B promotion campaign — 7 sub-tasks, 14 commits, +2,240 graph nodes, three parser-iteration cycles.

---

## Final tally

`unknown` 12,434 (Session 28 start, 70.4%) → **2,118 (12.0%)**.

| Type dir | Pre-session | Post-session | Δ |
|---|---|---|---|
| characters | 3,557 | 3,938 | +381 |
| locations | 168 | 1,010 | +842 |
| events | 249 | 352 | +103 |
| titles | 546 | 601 | +55 |
| houses | 313 | 556 | +243 |
| artifacts | 1 | 230 | +229 |
| factions | 97 | 163 | +66 |
| texts | 0 | 150 | +150 (new dir) |
| theories | 0 | 45 | +45 (new dir) |
| religions | 20 | 60 | +40 |
| concepts | 0 | 31 | +31 (new dir) |
| species | 0 | 38 | +38 (new dir) |
| foods | 0 | 69 | +69 (new dir, new entity type `object.food`) |
| **TOTAL** | **5,008** | **7,248** | **+2,240** |

**Cat 1 orphan edges:** 2,955 → 1,973 (−982, −33%).

5 new dirs bootstrapped. 1 new entity type added to architecture.md schema (`object.food`).

---

## Act 1 prelude — what was already done before this session

The continue prompt at session start (`progress/continue-prompts/2026-05-01-pathb-promotion.md`) inherited a structural finding from the prior session:

**The wiki cache had a fossil categorizer.** The original Playwright crawl (archived) included an entity-type categorizer that mapped MediaWiki **categories** (`Swords`, `Books and scrolls`, `Castles`, `Battles`) to project entity types via `CATEGORY_TYPE_MAP`. Only the name-based fast path (`if page.startswith("House ")`) ran, populating `sources/wiki/houses/` — the other directories (`characters/`, `locations/`, `events/`, `artifacts/`) are empty because the categorizer needed category data and the original `action=parse` API stripped catlinks footers.

**Path B was the structural fix:** a one-time bounded fetch via `cloudscraper` (NOT Playwright — `urllib` is 403'd by Cloudflare; `cloudscraper` returns 200) backfilled MediaWiki categories for all 17,657 pages into `working/wiki-parsed/page-categories.jsonl`. `scripts/wiki-infobox-parser.py` was extended with `CATEGORY_TYPE_MAP`. CLAUDE.md gained a narrow re-fetch-exception clause.

**Result of Act 1 alone:** unknown 12,434 (70.4%) → 2,487 (14.1%). All this was committed in earlier sessions BUT the worklog never received an entry. Initial blocker this session: discovered git status showed Session 28's residue uncommitted, including the new `scripts/wiki-fetch-categories.py`, modified parser, parse outputs, and the continue prompt itself.

**First action this session:** Committed the Session 28 categorizer work as commits `de9cf6f` (parser/backfill) + `bb49b29` (continue-prompt rotation) before doing anything else.

---

## Act 2 — Path B Promotion Campaign

The continue prompt's plan: 7 sub-tasks, batch by entity type, commit each batch separately, pause for review after the small/safe batches before the bigger ones.

### Sub-task 1a: object.text (150 nodes)

**First action: a parser fix.** Dry-run output exposed that 31 of 185 `object.text` pages were real-world publications: A Game of Thrones (the novel), A Clash of Kings, A Storm of Swords, A Knight of the Seven Kingdoms, Fire & Blood, The World of Ice & Fire, A Game of Groans (parody), A Feast of Ice and Fire (cookbook), comics, art books. They classify under MediaWiki's `Books` category but lack the in-world-only `Books and scrolls` companion category.

Clean signal: **all 31 `Books`-only pages are real-world publications** with zero false negatives. Fixed in the parser via a `Books`-without-`Books and scrolls` SKIP rule (commit `1fe5920`). `object.text` 185 → 154.

**Second issue: filename encoding bug.** The wiki cache encodes colons in titles as underscores (`": "` → `"__"`). My filename derivation didn't handle colons, so 7 of 150 pages reported "Raw file missing": `Hardhome: An Account of Three Years Spent...`, `Dragons, Wyrms, and Wyverns: Their Unnatural History`, `When Women Ruled: Ladies of the Aftermath`, etc. Fixed: added `.replace(":", "_")` to the filename derivation.

**Apply:** 150 promoted (4 already in graph). 80 with prose / 70 stub-only. Commit `300f79c`.

### Sub-task 1b: object.artifact (190 nodes)

**Pre-promotion audit found 7 weapon-type glossary entries:** Arakh, Bastard sword, Falchion, Greatsword, Longsword, Shortsword, Armament. Tagged with `Terms` + `Swords` or `Science and technology` + `Weapons`. They're glossary, not artifacts.

Considered a parser-level `Terms` skip but rejected — `Terms` is also legitimately used for titles (Khal, Magnar), events (Coming of the Andals, War of the Wombs), magic concepts (Water magic). Wrong scope. In-script `GLOSSARY_SKIP_PAGES` instead.

**Surprise finding:** 190/190 artifacts have NO infobox. Verified: Longclaw's HTML has no `class="infobox"` table — just an image and prose. The wiki simply doesn't have infobox templates for named artifacts. Skeleton + prose only. WIELDS / FORGED_BY / HOLDS edges deferred to Stage 4.

**Notable artifacts now in graph:** Longclaw, Needle, Dark Sister, Blackfyre, Brightroar, Heartsbane, Lady Forlorn, Nightfall, Red Rain, Lamentation, Vigilance, Truth, Widow's Wail, Oathkeeper, Ice (re-forged), Dawn, Dragonbinder, ~80 ironborn longships. Commit `006305d`.

### Sub-task 2: place.location + place.region (769 nodes)

Largest single batch. `place.region` (7 pages — Sothoryos, White Waste, Grey Waste, Cannibal Sands, Further East, Land of the Shrykes, Plains of the Jogos Nhai) folded into `locations/` per existing TYPE_DIR_MAP convention.

769 NEW (208 already in graph). 559 prose / 210 stub. Same caveat: 769/769 have no parser-recognized infobox. Most location pages are short articles. Cat 1 orphan edges drop **2,941 → 2,539** (−402 edges) — locations are heavy reverse-edge targets (HOUSED_AT, BORN_AT, DIED_AT, LOCATED_IN). Commit `39d14a94`.

### Sub-task 3 (events): the chapter-page disaster

**First events run: 382 nodes promoted, 338 of them garbage.** The committed nodes had names like `a-clash-of-kings-chapter-1.node.md`. Wiki chapter-summary pages misclassified as `event.battle`.

Diagnosed: chapter summary pages have infoboxes containing fields `POV / Place / Page / Chapter chronology`. The `Place` field is a strong field for `event.battle` in `ENTITY_TYPE_SIGNATURES`, scoring weight 2 (highest among types). Whole-corpus false positive. Reverted commit (`fbbf764c`).

Fix: parser SKIP rule for the `A Song of Ice And Fire chapters` MediaWiki category. Re-ran: `event.battle` 528 → 174 (354 chapter pages now skip).

**Second-pass false positives** from the parser's pre-existing `\bwar\b` / `\bconquest\b` / `\binvasion\b` page-name patterns: `Lance (war galley)` (ship), `Conquest of Dorne (book)`, `Account of the War of the Ninepenny Kings` (book), `Years after Aegon's Conquest*` timeline meta-pages, `Engines of War` / `Brothel Queens` / `Lads` / `Blacks` / `Greens` / `Two Alans` / `Two Betrayers` / `Seven Who Rode` / `Winter Wolves` / `Widow Fairs` / `Gutter knights` / `Sowing` (factions/groups), `Coronation of Aegon II` / `Wedding of Aegon III...` (ceremonies).

Tightening the regex would require list-of-exclusions logic anyway. In-script `GLOSSARY_SKIP_PAGES` (26 pages) instead. Plus Matt's `Dragon egg` ENTITY_TYPE_OVERRIDES catch (categorized as `Objects` / `Dragons`, neither in CATEGORY_TYPE_MAP at the time).

**Apply (clean):** 26 events (8 battles + 18 wars). `graph/nodes/events/` 249 → 275. Commit `39eabd9a` (combined parser-fix + events + Dragon egg).

**Lesson logged:** dry-run sample-checking surfaces false-positives. Spot-check the actual page names in `--plan` mode before `--apply` for every batch.

### Sub-task 4: organizations (289 nodes)

Per-type routing via `TYPE_TO_DIR` map (this script departs from prior single-DEST_DIR pattern):
- `organization.house` → `houses/` (313 → 556, +243)
- `organization.religion` → `religions/` (20 → 45, +25)
- `organization.faction` → `factions/` (97 → 118, +21)

927 infobox-derived edges. Houses have rich infobox templates: seat, overlord, words, sigil, founder, head, predecessor. 221 prose / 68 stub. Commit `55a956e1`.

### Sub-task 5: characters (381 nodes)

`character.human: 373` + `character.dragon: 8`. 1,029 infobox edges (rich character infoboxes: father, mother, spouse, siblings, allegiance, culture, religion). 336 prose / 45 stub. Mostly minor characters: knights, septons, historical figures, named animals (Balerion the cat), servants. Cross-identity checks (Reek=Theon, Alayne=Sansa) deferred to Stage 4 cross-identity-detector. Commit `8d161c8d`.

### Sub-task 6: long-tail (119 nodes)

55 titles + 31 magic + 18 species + 15 cultures (Pass B precedent: cultures route to `factions/`).

`graph/nodes/concepts/` bootstrapped (0 → 31): Aeromancer, Bloodmage, Bloodmagic, Glass candle, Greenseer, Greensight, Necromancy, Pyromancer, Shadowbinder, Shapechanger, Skinchanger, Wights, Magic.

`graph/nodes/species/` bootstrapped (0 → 18): Centaurs, Deep Ones, Demons, Grumkin, Harpies, Ice giants, Jhogwin, Merlings, Others, Rock goblins, Selkies, Shrykes, Snarks, Sphinx, Squishers, Tiger-men, Walrus-men, Ifequevron.

1 skip: `Dragon` — categorized as Magic but is the species page; deferred. Commit `4c5eb9e3`.

### Iteration 2: parser expansion (283 nodes)

Matt's pushback on "diminishing returns" framing surfaced load-bearing entities still in `unknown`: Ashford Tourney, Knight of the Laughing Tree (Lyanna's secret identity at Harrenhal — R+L=J pillar), Red Wedding, Theory pages.

**Audit of unknowns by category** (top buckets in 2,484 unknown pages):
- Tourneys (25), Theories (45), Weddings (23), Events (25), Mountain clans (11), Deities (20), Streets/Gates/Halls (64), Objects/Merchant ships (39)
- Plus Animals (95), Plants (34), Food (58), Drinks (16), Trees (20) — schema decision territory
- Plus 836 pages with NO categories at all (stubs + edge cases)
- Plus wiki cruft: Feature quotes (278), Did you know (148), Feature articles (61) — defer

**Parser additions:**
- CATEGORY_TYPE_MAP: Tourneys/Tournaments → `event.tournament` (NEW type), Weddings/Assassinations/Massacres/Coronations → `event.battle`, Events → `event.battle`, Theories/Theory → `concept.theory`, Streets in / Halls / Gates / Squares / Plazas / Markets / Bridges / Wells / Gardens → `place.location`, Mountain clans of → `organization.faction`, Organizations → `organization.faction`, Deities/Gods/Goddesses → `organization.religion`, Objects/Merchant ships → `object.artifact`
- PAGE_NAME_TYPE_PATTERNS: `\btourney\b` → `event.tournament` (catches Ashford Tourney with empty categories)
- ENTITY_TYPE_OVERRIDES: Knight of the Laughing Tree → `character.human`

Promotion script updates:
- events: TARGET_TYPES adds `event.tournament`
- longtail: TYPE_TO_DIR adds `concept.theory` → `theories/`

**Apply across all 6 scripts:** +283 NEW nodes (artifacts +38, locations +73, events +77, orgs +50, characters 0 (Knight already had a slug match), longtail +45 theories). Cat 1: 2,021 → 1,973. Commit `58718ff2`.

**Verified key narrative pages now in graph:** Knight of the Laughing Tree (character), Ashford Tourney, Tourney at Harrenhal, Red Wedding, Doom of Valyria, Defiance of Duskendale, Azor Ahai/Theories, R+L=J theory cluster.

### Iteration 3: foods + trees (89 nodes, schema change)

Matt's design-values memory: food/hospitality is first-class. Schema decision:
- **Foods (food + drinks combined)** → new `foods/` dir, type `object.food`. ~74 nodes.
- **Trees** → existing `species/` (broadens dir scope to "in-world flora/fauna kinds"; weirwood/heart tree/ironwood/sentinel as first-class species).
- **Animals/Birds/Fish/Plants** deferred ("don't have to get into species right now").

**Trees vs Food precedence:** 4 pages dual-tagged (Apple, Lemon, Orange, Chestnut tree). Trees pattern placed BEFORE Food in CATEGORY_TYPE_MAP — tree is canonical, fruit is derivative.

Schema additions:
- `reference/architecture.md`: `object.food` row added; `species` row description broadened
- `scripts/wiki-pass2-promote.py` TYPE_DIR_MAP: `object.food → foods`
- `scripts/wiki-pass2-tier3-pathb-longtail.py` TYPE_TO_DIR: `object.food → foods/` + identity-line branch

**Apply:** 69 foods + 20 trees = 89 NEW. Bootstraps `graph/nodes/foods/` and broadens `species/`. Notable: Bowl of brown, mead, dreamwine, hippocras, lemon cakes, Arbor wine, milk of the poppy, moon tea, weirwood paste; Weirwood, Heart tree, Ironwood, Sentinel, Soldier pine, Goldenheart, Talking Trees. Commit `1e258b71`.

---

## Decisions made (compressed)

1. **Real-world publications skip via `Books`-without-`Books and scrolls` rule** — clean signal, zero false negatives across 31 pages. Parser-level fix.
2. **Weapon-type glossary skip via in-script set, not parser** — `Terms` category is too broad to use as global skip (catches legitimate titles, events, magic).
3. **Chapter-summary pages skip via `A Song of Ice And Fire chapters` category** — caught a 338-node false-positive disaster in events; reverted + parser fix.
4. **`event.tournament` as new entity type** — tournaments aren't battles structurally; routes to `events/` via TYPE_DIR_MAP.
5. **`object.food` as new entity type + new `foods/` dir** — schema change, food/hospitality is first-class per Matt's design values. Drinks bundle in.
6. **Trees route to `species/`** — broadens species dir to flora/fauna; weirwood is first-class.
7. **Trees-before-Food in CATEGORY_TYPE_MAP** — for dual-tagged pages (Apple, Lemon, Orange, Chestnut tree), tree is canonical.
8. **Cultures route to `factions/`** — Pass B precedent (existing 6 culture nodes there). Migration to `cultures/` deferred.
9. **Knight of the Laughing Tree promoted as separate node from Lyanna Stark** — cross-identity SAME_AS edge is Stage 4 cross-identity-detector's job.
10. **Theory sub-pages (`X/Theories`) keep `-theories` slug suffix** — awkward but deterministic; promoted to `theories/`.
11. **Animals/Birds/Fish/Plants deferred** — Matt's "don't have to get into species right now."
12. **`Years` (74 pages) and wiki-cruft categories (`Feature quotes`/`Did you know`) remain in unknown** — Tier 3 chronology-extractor and concept-page-defer territory.

---

## What surprised

1. **The Books category is weirdly mixed.** "Books and scrolls" is the in-world signal; plain "Books" is the real-world signal. Without that distinction we'd have promoted A Game of Thrones (the novel) into the in-world graph.
2. **Wiki chapter pages have infoboxes with `Place` fields.** Field-signature classifier has no defense against this — hence the 338-node disaster. Category-based skip is the only fix.
3. **Named artifacts have NO infoboxes.** Verified: Longclaw HTML has no `class="infobox"`. The wiki simply uses prose for these. Empty `## Edges` until Stage 4.
4. **Locations almost universally lack infoboxes too.** 769/769 in the locations batch. Same prose-only pattern.
5. **The `\bwar\b` page-name pattern catches more than wars.** "Lance (war galley)", "Engines of War", "Brothel Queens" — false positives that need per-batch skip lists.
6. **Apple/Lemon/Orange/Chestnut tree are dual-tagged Trees+Food.** Solved by category-precedence ordering.
7. **Weirwood is in `Trees` category.** Schema decision validated: trees-as-species is right because the wiki agrees they're flora.

---

## What was NOT done (deferred, by intent or by Matt's call)

- **Animals/Birds/Fish/Plants (~219 unknown pages)** — schema decision punted.
- **Years/era pages (74)** — Tier 3 chronology-extractor's job.
- **Wiki-meta categories** (Feature quotes 278, Did you know 148, Feature articles 61) — defer.
- **836 pages with NO categories at all** — many are stubs; need investigation later.
- **Stage 4 prose-edge-classifier** — separate continue prompt at `2026-04-27-wiki-pass2-stage4-edge-discovery.md`.
- **`Dragon` page** — categorized as Magic but is the species page; needs ENTITY_TYPE_OVERRIDES decision (currently in-script skip from longtail batch).
- **Schema-drift audit on opus (~$50, prior approval)** — held until promotion phase stabilizes. Continue prompt drafted: `2026-05-02-promotion-completion-then-schema-drift.md`.

---

## Process notes for future iterations

1. **Always sample `--plan` output before `--apply`.** The chapter-page disaster would have been caught in 30 seconds of looking at sample slugs. Don't trust dry-run summary numbers alone.
2. **In-script GLOSSARY_SKIP_PAGES is the right tool for narrow false-positive sets.** Parser-level fixes are right when the rule generalizes.
3. **Bulk-rewrite via `python3 -c` over copied template scripts is fast.** The events/orgs/characters/longtail scripts are minor variations of locations.py — text replacement was sufficient.
4. **Per-type routing via TYPE_TO_DIR is cleanly extensible.** Adding `object.food → foods/` to longtail was a one-line change.
5. **Parser changes require regenerating page-index.jsonl.** Big diffs but acceptable. Always commit immediately to keep diff size manageable.
6. **Existing-graph slug-conflict filter prevents collisions** but means rerunning a script after a parser change picks up only NEW classifications, never re-emits existing nodes. That's correct.

---

## Commits this session (14 total)

```
1e258b71 Path B iteration 3: foods + trees (89 nodes, 1 new entity type)
58718ff2 Path B iteration 2: parser expansion + 283 newly-classified nodes
4c5eb9e3 Path B Sub-task 6: promote 119 long-tail nodes
8d161c8d Path B Sub-task 5: promote 381 character nodes
55a956e1 Path B Sub-task 4: promote 289 organization nodes
39eabd9a Path B: parser fix (chapter-page skip) + 26 events + Dragon egg
fbbf764c Revert "Path B Sub-task 3: promote 382 event nodes (battles + wars)"
e72aa039 Path B Sub-task 3: promote 382 event nodes (battles + wars)   [reverted]
39d14a94 Path B Sub-task 2: promote 769 location/region nodes
006305dc Path B Sub-task 1b: promote 190 artifact nodes (named weapons + ships)
300f79c8 Path B Sub-task 1a: promote 150 in-world text nodes
1fe59200 Path B parser fix: skip real-world publications
bb49b291 Rotate continue prompts: archive Phase 2, add Path B promotion
de9cf6f7 Path B: parser categorizer extension + MediaWiki categories backfill
```
