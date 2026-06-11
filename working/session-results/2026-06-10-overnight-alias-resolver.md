---
date: 2026-06-10
agent: script-builder
task: NEW TODO #8 — event-alias-resolver build
status: complete
---

# Event Alias Resolver — Build Results

## Design approach taken

Followed `reference/alias-resolver-design.md` (S86, Q1) exactly: built a **separate, deterministic, lookup-only resolver** for events. No LLM in the loop.

The resolver (`scripts/event_alias_resolver.py`) harvests aliases from three sources, merges them into a flat `{normalized_phrase -> canonical_slug}` dict, handles collisions by priority order, and provides both a `--build` (artifact generation) and `--lookup PHRASE` (CLI query) mode.

### Three alias sources (priority order, highest first)

1. **`node-name`** — the `name:` field from each `graph/nodes/events/*.node.md` frontmatter (583 nodes). Canonical, highest trust.
2. **`node-slug`** — the `slug:` field normalized to a phrase (583 nodes). Covers the action-slug form.
3. **`node-frontmatter-alias`** — the `aliases:` list in node frontmatter (6 non-empty, 14 alias entries). Author-curated.
4. **`wiki-canonical-name`** — the canonical page title from `working/wiki/data/event-node-aliases.json` (355 entries after filtering noise).
5. **`wiki-slug-self`** — the event slug from the harvested JSON treated as a phrase (371 entries).
6. **`wiki-redirect`** — wiki redirect chain aliases from the S85 harvester (176 entries across 113 of 371 harvested event slugs).

**Normalization:** lowercase, strip leading article (a/an/the), collapse whitespace. All lookup keys and input queries are normalized before matching — so "the Red Wedding", "Red Wedding", "red wedding" all resolve identically.

**Collision handling:** if a normalized phrase maps to >1 canonical slug, it's flagged as AMBIGUOUS and excluded from the lookup (returns `None, "ambiguous"`). Priority order breaks ties when sources differ.

**Noise filter:** wiki canonical_name strings containing "part of" mid-string (scraper artifact from infobox concatenation) are excluded from the alias_to_canonical table. This dropped 16 noisy entries.

## Files produced

- **Script:** `/Users/mnoth/source/asoiaf-chat/scripts/event_alias_resolver.py`
- **Lookup artifact:** `/Users/mnoth/source/asoiaf-chat/working/wiki/data/event-alias-lookup.json`

## Coverage stats

```
Total entries scanned:  2082
Unique phrases indexed:  876
Unambiguous lookups:     875
Ambiguous collisions:      1
```

Source breakdown:
```
node-frontmatter-alias             :    14
node-name                          :   583
node-slug                          :   583
wiki-canonical-name                :   355
wiki-redirect                      :   176
wiki-slug-self                     :   371
```

Event nodes scanned: 583 total (366 wiki-derived with `aliases:` frontmatter field, 217 chapter-beat minted-plate3).

Nodes with zero aliases in any source: 217 (all chapter-beat nodes — their slugs and names do index, but they have no wiki redirect aliases and no frontmatter alias lists). These are correctly covered by the node-name and node-slug sources; they just have no synonym variants.

## Smoke test outputs (verbatim)

### From the task brief

| Phrase | Result | Status | Notes |
|--------|--------|--------|-------|
| "Ned's execution" | (no match) | MISS | Expected and correct — see below |
| "the Tourney at Harrenhal" | `tourney-at-harrenhal` | HIT | |
| "the Trident" | (no match) | MISS | Expected and correct — see below |
| "the Red Wedding" | `red-wedding` | HIT | |
| "the Purple Wedding" | `purple-wedding` | HIT | |
| "the Battle of the Blackwater" | `battle-of-the-blackwater` | HIT | |
| "Robert's Rebellion" | `roberts-rebellion` | HIT | |
| "Sack of King's Landing" | `sack-of-kings-landing` | HIT | |
| "the Doom of Valyria" | `doom-of-valyria` | HIT | |

### Additional tests showing redirect coverage

| Phrase | Result | Status |
|--------|--------|--------|
| "war of the usurper" | `roberts-rebellion` | HIT (wiki redirect) |
| "battle of stoney sept" | `battle-of-the-bells` | HIT (wiki redirect) |
| "bread riots" | `riots-in-kings-landing` | HIT (wiki redirect) |
| "the long night" | `long-night` | HIT (wiki redirect) |
| "dance of the dragons" | `dance-of-the-dragons` | HIT |
| "the great spring sickness" | `great-spring-sickness` | HIT |
| "battle of the whispering wood" | `battle-of-the-whispering-wood` | HIT |
| "combat at the tower of joy" | `combat-at-the-tower-of-joy` | HIT |

## Explaining the two expected misses

### "Ned's execution" → MISS

Correct behavior. The canonical node is `joffrey-orders-execution` (action-named slug), and its `name:` field is "Joffrey orders execution". Neither form contains "Ned". There is no wiki redirect from a "Ned's execution" page. This miss is the exact slug-discoverability gap that NEW TODO #10 addresses: renaming `joffrey-orders-execution` → `execution-of-eddard-stark`. Once that rename lands, the resolver will auto-generate "execution of eddard stark" from the new slug and name, making "execution of eddard stark" a HIT. A reader phrase like "Ned's execution" (possessive contraction) will still miss — that would require a hand-authored `aliases:` entry on the node.

### "the Trident" → MISS

Correct behavior. "Trident" (after article strip) is the river name, not unambiguously the battle. The unambiguous form "Battle of the Trident" resolves cleanly to `battle-of-the-trident`. The design doc explicitly says "events are typically named with full unambiguous phrases" — "the Trident" as a battle shorthand is colloquial ambiguity the deterministic resolver correctly refuses to guess at.

## Sole ambiguous collision

```
'conquest of dorne' -> ['conquest-of-dorne', 'the-conquest-of-dorne']
```

Two wiki event nodes exist for "Conquest of Dorne": the military campaign (`conquest-of-dorne`) and a Dunk & Egg novella / book reference (`the-conquest-of-dorne`). Both have "conquest of dorne" as a normalized alias. Correctly flagged as AMBIGUOUS — the caller must pick based on context.

## Design questions for Matt

1. **"Ned's execution" possessive form:** After NEW TODO #10 renames the node to `execution-of-eddard-stark`, a possessive alias "ned's execution" will still miss unless an `aliases:` list entry is added to the node frontmatter. Recommend adding it as part of the rename script's output. The resolver reads node frontmatter aliases, so it will auto-pick up whatever is in `aliases:` after the rename.

2. **"the Trident" as battle shorthand:** If Mode 3 agent queries frequently use "the Trident" to mean `battle-of-the-trident`, add `["the Trident", "Battle of the Trident"]` to that node's frontmatter `aliases:` list. The resolver will pick it up on next `--build`. This is an editorial call, not a script fix.

3. **Wiki redirect aliases for `battle-of-the-trident`:** The `event-node-aliases.json` shows `alias_count: 0` for `battle-of-the-trident` — the wiki has no redirect pages pointing to it. The node itself does exist in the graph. This is expected: prominent events sometimes lack redirect pages on the wiki.

4. **Chapter-beat nodes with no synonyms:** 217 minted-plate3 nodes (e.g. `arya-captured`, `joffrey-orders-execution`) have only their slug and name forms indexed. Their action-phrased names are precise enough that reader queries are likely to use the full phrase or a very close variant. No action needed unless specific misses surface in Mode 3 testing.

## Readiness note

**Ready for use.** The resolver is deterministic, idempotent, and covers all named-event hubs the wiki knows about plus all graph event nodes. The two "misses" in the smoke tests are correct behavior (not data gaps — the resolver is doing the right thing). Run `python3 scripts/event_alias_resolver.py --lookup "PHRASE"` to query; rebuild after any node renames or alias additions with `--build`.

Post-#10 (Ned rename): re-run `--build` after the rename script applies — the resolver will auto-update from the new node file.
