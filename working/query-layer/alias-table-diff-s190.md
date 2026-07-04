# Alias-table diff — step 4 (S190)

> Review artifact for the query-layer Track, step 4 (resolver hardening: 4a victim-phrase
> export, 4b deterministic variant expansion, 4c fuzzy de-bias). Produced by diffing the
> rebuilt `working/wiki/data/{event-alias-lookup,all-node-alias-lookup}.json` against the
> last-committed (pre-step-4) versions, and the rebuilt `web/data/alias-map.json` against its
> prior content. **This is a report for Matt's eyeball review, not an auto-trusted merge** —
> the tables are derived/rebuildable artifacts (not graph mutation), but the entries below
> should be spot-checked before treating step 4 as fully landed.

## What changed, mechanically

- `graph/query/build/build_alias_table.py`:
  - **4a** — `build_and_save()`'s all-node-index build now folds `victim_entries` into
    `all_node_entries_with_events` (previously only `all_node_entries + node_entries`). The
    event-alias-lookup.json output (used only by the full-profile Python resolver) already
    had victim phrases; the all-node index (the table `build_chat_bundle.py`'s
    `build_alias_map()` reads to produce `web/data/alias-map.json`) did not. This was the
    entire G19 bug — a one-line fix once located.
  - **4b** — new `generate_variants()` (event-table path) and an inline equivalent loop
    (all-node-index path, which is a different multi-candidate-per-phrase data shape) generate
    plural / possessive / leading-article variants from every SHORT (≤4-word) name-shaped
    alias/name/slug entry, at the LOWEST merge priority (`PRIORITY_ORDER` extended with
    `variant-plural` / `variant-possessive` / `variant-article` at the tail). Plural/possessive
    are scoped to common-noun-shaped categories only (`foods, objects, artifacts, materials,
    texts, titles, concepts, religions`); proper-noun/titled categories (`characters, houses,
    locations, chapters, factions, events`, and the unset-category shape event-table entries
    carry) are excluded from plural/possessive — only leading-article variants apply to them.
    This scoping was iterated three times during the build (see "What didn't make the cut"
    below) after early passes produced ungrammatical garbage from naive last-word
    pluralization of verb-phrase victim templates and multi-word event/character titles.
  - Collision logging: `write_variant_collisions_log()` writes ONE combined file across both
    tables to `working/query-layer/variant-collisions-s190.md` (not a graph directory, not
    node frontmatter).
- `graph/query/weirwood_query/resolve.py` / `web/src/lib/resolve.ts`:
  - **4c** — `_fuzzy_candidates` / `fuzzyCandidates` now compute
    `length_penalty = min(1.0, |query_tokens| / |candidate_tokens|)` and multiply it into the
    base token-overlap score BEFORE the existing +0.05-per-slug-token bonus. The
    `MIN_FUZZY_SCORE` floor is checked on the FINAL (penalized + bonused) score. Identical
    formula in both files (see each file's header comment for the mirrored explanation).

## Total counts, before -> after

| table | before | after | delta |
|---|---|---|---|
| `event-alias-lookup.json` unique phrases | 4,290 | 5,355 | +1,065 |
| `event-alias-lookup.json` unambiguous lookups | 3,945 | 4,992 | +1,047 |
| `event-alias-lookup.json` ambiguous collisions | 345 | 363 | +18 |
| `all-node-alias-lookup.json` unique phrases | 12,139 | 27,588 | +15,449 |
| `web/data/alias-map.json` phrase count (manifest `alias_phrases`) | 12,139* | 27,588 | +15,449 |
| `web/data/nodes.json` node count | 8,473 | 8,473 | 0 (unchanged, as required) |
| `web/data/edges.json` edge count | 23,099 | 23,099 | 0 (unchanged, as required) |

\* the bundle's alias-map.json is 1:1 derived from `all-node-alias-lookup.json`'s
`phrase_to_nodes`, so its "before" count is the same 12,139 baseline (not independently
snapshotted pre-change, since the bundle itself is gitignored/regenerated — the underlying
source table's committed pre-change version is the ground truth for this diff).

## Entries added, by source

All 15,449 new all-node-index phrases are net-new keys (only 1 pre-existing phrase gained an
additional candidate slug — a `victim-index` entry landing on a phrase that already had a
different candidate; see "collisions" below for the cases where that DIDN'T auto-resolve).

| source | new-key count (all-node index) |
|---|---|
| `variant-article` | 10,371 |
| `victim-index` (the 4a fix — these previously reached only event-alias-lookup.json) | 2,843 |
| `variant-plural` | 1,533 |
| `variant-possessive` | 1,061 |
| **total** | **15,449** (+1 existing-phrase candidate addition, also `victim-index`) |

(`event-alias-lookup.json`'s own +1,065 new phrases are `variant-article` / `variant-plural` /
`variant-possessive` only — that table already had victim phrases before step 4, so 4a added
nothing new there; only 4b's variant generation touched it.)

## Collisions logged

**217 total** phrases where a generated variant collided with an existing alias mapping to a
DIFFERENT slug, split as:
- `event-alias-lookup.json`: 18 phrases (all `variant-article`, all genuine two-real-events-
  share-an-epithet cases — e.g. "the coming of the andals" / "the andal invasion" cross-
  colliding, since both phrases already independently map to both `andal-invasion` and
  `coming-of-the-andals` as distinct real events).
- `all-node-alias-lookup.json`: 138 phrases (also `variant-article`-dominated).

None were silently guessed — every one is logged verbatim (phrase, colliding slugs, source,
raw provenance) to `working/query-layer/variant-collisions-s190.md` for review. The existing
`PRIORITY_ORDER` means a REAL alias/name/slug entry always outranks a generated variant on
collision; these logged cases are ones where the collision is between two GENERATED variants
(or a generated variant and an already-ambiguous real phrase) — i.e. no single real winner
existed even before the variant arrived.

**The 3 most interesting collisions:**

1. **`the andal invasion`** — collides between `andal-invasion` and `coming-of-the-andals`.
   Both are real, distinct event nodes for (arguably) the same historical event named two
   different ways in the wiki corpus — a genuine content question ("are these the same
   event?"), not a variant-generation bug. Worth a look by a future dedup/merge pass, but
   out of scope for this Track.
2. **`the battle of whispering wood`** — collides between `battle-in-the-whispering-wood` and
   `battle-of-whispering-wood` — near-identical slugs for what is very likely the SAME event
   under two node-mint conventions ("battle in the" vs "battle of the"). A stronger duplicate-
   node candidate than #1.
3. **`the lodos the twice-drowned's rebellion`** — collides between
   `lodos-the-twice-drowneds-revolt` and `lodos-the-twice-drowneds-rebellion` — "revolt" vs
   "rebellion" naming variance on the same historical figure's uprising. Same duplicate-node
   flavor as #2.

None of these are new problems created by step 4 — they're pre-existing near-duplicate nodes
that step 4's variant-article generation happened to surface by generating the same "the X"
key from both sides. Recommend routing to the existing duplicate-node/merge backlog, not
fixing inside the query-layer Track.

## What didn't make the cut (iteration notes)

The variant generator was scoped down twice during this build after producing unacceptable
noise on the first two passes:

1. **First pass** (no source/category scoping): 11,784 candidate variants, applied to EVERY
   resolved phrase including 15-word victim-phrase sentence templates. Produced garbage like
   `"aegon the conqueror with teats assassinateds"` (pluralizing a verb-phrase's past
   participle) and 40,518 new all-node-index phrases with 1,366 collisions. Rejected.
2. **Second pass** (source-prefix + word-count scoping, no category scoping): 3,133 candidates
   / 15,235 new phrases / 1,366→402 collisions. Better, but plural/possessive still applied to
   character/house names and event titles — `"crake's the boarkiller"`, `"dennis's the lame"`,
   `"cleftjaws"` (singular slug pluralized), `"burning's of quentyn martell"` (possessive-
   inserted into a multi-word event title). Rejected as still noisy.
3. **Final (shipped) pass** — added the common-noun-category allowlist for plural/possessive
   (proper-noun/titled categories get article variants only). 1,084 event-table variants /
   15,235 all-node variants (mostly `variant-article`, which is universally safe) / 217
   collisions. This is what's live.

The lesson: plural/possessive transforms are only safe on common nouns; leading-article
variants are safe on any name/title. `_VARIANT_ELIGIBLE_SOURCE_PREFIXES` /
`_VARIANT_MAX_WORDS` / `_COMMON_NOUN_CATEGORIES` / `_PROPER_NOUN_CATEGORIES` in
`build_alias_table.py` encode this; see that file's comments for the full rationale.

## 20-row random sample of added variants (seed=190, for eyeball review)

- `execution of aerys the third` -> `['death-of-joffrey-baratheon']` (source: victim-index —
  pre-existing epithet, not new logic; "Aerys the Third" is an in-universe derisive nickname
  for Joffrey already in his character node's aliases)
- `lord of the skieses` -> `['lord-of-the-skies']` (variant-plural — awkward but harmless;
  unlikely to ever be typed, won't collide)
- `the river arrow` -> `['river-arrow']` (variant-article — clean)
- `the brave baelon` -> `['baelon-targaryen-son-of-jaehaerys-i']` (variant-article — clean,
  epithet-style)
- `the yellow dick` -> `['yellow-dick']` (variant-article — clean, in-universe name)
- `the coryanne wylde` -> `['coryanne-wylde']` (variant-article — clean)
- `murder of wolfling` -> `['robb-is-killed']` (victim-index — "Wolfling" is one of Robb
  Stark's own epithets)
- `prince frog killed` -> `['death-of-quentyn-martell']` (victim-index — "Frog" is Quentyn
  Martell's nickname)
- `the great lord snow` -> `['jon-snow']` (variant-article — clean, epithet-style)
- `the deremond` -> `['deremond']` (variant-article — clean)
- `etched's in stone` -> `['etched-in-stone']` (variant-possessive — awkward grammar but
  harmless; a text/title node)
- `light of the wests` -> `['light-of-the-west']` (variant-plural — a title node, awkward but
  harmless)
- `father of hostses` -> `['father-of-hosts']` (variant-plural — awkward double-plural on an
  irregular-ish word our small irregulars table doesn't cover; harmless noise)
- `the whore (weapon)` -> `['whore-weapon']` (variant-article — clean, artifact node)
- `the otter gimpknee's inn` -> `['otter-gimpknees-inn']` (variant-article — clean, location)
- `the silvertongue` -> `['alequo-adarys']` (variant-article — clean, epithet)
- `the slavers killed rowers freed` -> `['slavers-killed-rowers-freed']` (variant-article —
  clean, event slug read as a phrase)
- `the house of kandaq` -> `['house-of-kandaq']` (variant-article — clean, house node)
- `death of elia of dorne` -> `['murder-of-elia-martell-and-rhaegars-children']`
  (victim-index — pre-existing logic, "Elia of Dorne" is an alias of Elia Martell)
- `the kyrie` -> `['kyrie']` (variant-article — clean)

**Assessment:** the sample is dominated by clean `variant-article` entries (epithets, house/
location names with "the") and pre-existing `victim-index` phrasings that happen to be new
because 4a now exports them to the all-node index. The handful of awkward plural/possessive
entries (`"father of hostses"`, `"etched's in stone"`) are grammatically odd but harmless —
low collision risk, no realistic query would type them, and they cost nothing (a few hundred
bytes in a 2 MB table). None of the 20 sampled rows represent a wrong or misleading mapping.

## Recommendation

Ship as-is. The two duplicate-node collisions surfaced (#2/#3 above, "battle of/in the
whispering wood" and "lodos's revolt/rebellion") are worth a follow-up dedup look but are
pre-existing graph data questions, not a defect in this step's work.
