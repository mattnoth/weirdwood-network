# Continue Prompt: Track B — Wiki Infobox Parser Script

> Created: 2026-04-24 | Source: working/todos.md "Wiki / Pass 2 Prep" + worklog.md Session 8

## Context

We have 17,657 cached wiki pages as JSON files in `sources/wiki/_raw/`. Each file has `{page, html, fetched}` keys. 5,279 pages have infoboxes (HTML `class="infobox"`). These infoboxes contain structured relationship data and book appearance data that feeds into Pass 2 (wiki ingestion) and graph building.

This script is **independent of Track A** (extraction). It can be built and run regardless of extraction progress.

## What to Build

A Python script at `scripts/wiki-infobox-parser.py` that processes the cached wiki JSON and outputs structured data.

### Data to Extract

**1. Entity `first_available` from citation anchors (chapter-level)**

Wiki footnotes encode book and chapter in `cite_ref` and `cite_note` HTML anchor IDs:
```
cite_ref-Ragot2...   → AGOT chapter 2
cite_ref-Rasos24...  → ASOS chapter 24
cite_ref-Radwd62...  → ADWD chapter 62
cite_note-Rawoiaf... → TWOIAF reference (not a chapter)
```

Regex: `cite_(?:ref|note)-R(agot|acok|asos|affc|adwd)(\d+)` — captures book abbreviation and chapter number. Ignore non-book prefixes (like `Rawoiaf`, `Citadel`, `IMDB`, `Calculation`).

The lowest chapter number per book gives the entity's first appearance in that book. The overall lowest across all books → `first_available`.

To convert chapter number to POV format (`AGOT Bran I`), cross-reference with `reference/pov-characters.md` which has the chapter-to-POV mapping.

**2. Entity `first_available` from infobox "Books" field (book-level fallback)**

```html
<th scope="row">Books</th><td>
<div class="plainlist"><ul>
  <li><a href="...">A Game of Thrones</a> <small>(POV)</small></li>
  <li><a href="...">A Clash of Kings</a> <small>(mentioned)</small></li>
</ul></div>
```

Appearance types: `POV`, `appears`, `mentioned`. The first book where appearance is NOT just "mentioned" → book-level `first_available`. Use this as fallback when cite_ref data is absent or ambiguous.

**3. Relationship fields from infoboxes**

Parse these `<th>` → `<td>` pairs from infoboxes:

| Infobox Field | Edge Type | Notes |
|---|---|---|
| Father | `PARENT_OF` (reverse) | Parse character name from `<a>` tag |
| Mother | `PARENT_OF` (reverse) | Parse character name from `<a>` tag |
| Spouse, Spouses | `SPOUSE_OF` | May be multiple |
| Lover, Lovers | `LOVER_OF` | May be multiple |
| Issue | `PARENT_OF` (forward) | May be multiple |
| Allegiance, Allegiances | `SWORN_TO` | May be multiple |
| Overlord, Overlords | `OVERLORD_OF` (reverse) | |
| Culture | `CULTURE_OF` | |
| Religion | `WORSHIPS` | For characters; context-dependent for locations |
| Seat, Seats | `SEAT_OF` | |
| Head | `RULES` | |
| Heir, Heirs | `HEIR_TO` | |
| Founder | `FOUNDED` | |
| Successor | `SUCCEEDS` | |
| Predecessor | `SUCCEEDS` (reverse) | |
| Ancestral weapon | `ANCESTRAL_WEAPON_OF` | |
| Cadet branches | `CADET_BRANCH_OF` | |
| Owner, Owners | `OWNS` | |
| Monarch | `SWORN_TO` or `SERVES` | Context-dependent |
| Born | `BORN_AT` | Extract location if present |
| Died | `DIED_AT` | Extract location if present |
| Buried | `BURIED_AT` | |
| Alias, Aliases | `ALIAS_OF` | |
| Ruler | `RULES` | |
| Region, Regions | `REGION_OF` | |
| Species | Node type metadata | Not an edge — informs entity type classification |

The full mapping table is in `reference/architecture.md` under "Wiki Infobox Fields → Edge Type Mapping".

**4. Entity type classification from infobox structure**

Different entity types have different infobox structures:
- Characters: have Father/Mother/Spouse/Born/Died/Culture/Allegiance
- Houses: have Coat of arms/Seat/Head/Overlord/Cadet branches/Ancestral weapon/Founder
- Locations: have Location/Government/Ruler/Religion/Founded/Notable places
- Battles: have Conflict/Date/Place/Result/Strength/Casualties
- Titles/Offices: have Office/Current Holder/First Holder/Creator

Use the presence of these field combinations to classify entity type according to the hierarchy in `reference/architecture.md`.

### Output Format

Produce a JSON Lines file (one JSON object per wiki page) at `working/wiki-parsed/infobox-data.jsonl`:

```json
{
  "page": "Eddard_Stark",
  "entity_type": "character.human",
  "first_available": {"book": "AGOT", "chapter": 2, "pov": "Catelyn I", "source": "cite_ref"},
  "books": [
    {"book": "AGOT", "appearance": "POV"},
    {"book": "ACOK", "appearance": "mentioned"}
  ],
  "relationships": [
    {"field": "Father", "target": "Rickard Stark", "edge_type": "PARENT_OF", "direction": "reverse"},
    {"field": "Spouse", "target": "Catelyn Tully", "edge_type": "SPOUSE_OF", "direction": "symmetric"},
    {"field": "Allegiance", "target": "House Stark", "edge_type": "SWORN_TO", "direction": "forward"}
  ],
  "aliases": ["Ned", "The Quiet Wolf"],
  "cite_refs": {"agot": [1,2,4,5,6,10,12,...], "acok": [3,4,11,...], ...}
}
```

Also produce a summary stats file at `working/wiki-parsed/parse-stats.md` with counts: how many pages parsed, how many had infoboxes, how many had cite_refs, distribution by entity type, most common relationship fields, pages that failed parsing.

### Implementation Notes

- Use only Python stdlib (no external dependencies) — consistent with existing scripts
- Process all 17,657 JSON files in `sources/wiki/_raw/`
- Handle HTML parsing with `html.parser` or regex — the infobox structure is consistent enough for regex
- The `<a>` tags inside infobox `<td>` cells contain the entity names; strip HTML to get clean names
- Some fields have multiple values (e.g., multiple spouses, multiple allegiances) — parse as lists
- Some fields have qualifiers in parentheses (e.g., "Catelyn Tully (m. 283 AC)") — preserve qualifiers in metadata
- Expect ~5,279 pages with infoboxes, ~17,000+ with cite_refs
- TV-show-only fields (Played by, TV series, episode data) should be skipped
- Book metadata fields (Author, Publisher, ISBN, Pages, Language) should be skipped

## What NOT to Do

- Do NOT modify any wiki cache files — they are a static reference layer
- Do NOT start building graph nodes yet — this script produces intermediate parsed data that Pass 2 consumes
- Do NOT try to resolve entity names to node filenames — that's a Pass 2 problem
- Do NOT assign confidence tiers — that requires wiki-category → tier mapping rules (a Pass 2 design task)

## Files to Read First

1. `reference/architecture.md` — entity type hierarchy, edge type taxonomy, wiki infobox → edge mapping table, spoiler gating section (wiki data sources)
2. `sources/wiki/_raw/Eddard_Stark.json` — example character page (78 cite_refs, full infobox)
3. `sources/wiki/_raw/House_Stark.json` — example house page
4. `sources/wiki/_raw/Winterfell.json` — example location page
5. `sources/wiki/_raw/Battle_of_the_Blackwater.json` — example battle page
6. `scripts/wiki-scraper.py` — existing script for style/convention reference
7. `reference/pov-characters.md` — chapter number to POV mapping (needed to convert cite_ref chapter numbers to `first_available` POV format)

## After This Script

The parsed output feeds into Pass 2 design:
- Entity `first_available` data → spoiler gates on graph nodes
- Relationship data → pre-populated edges (Tier 1, wiki-sourced)
- Entity type classifications → node routing (which `graph/nodes/` subdirectory)
- The wiki-ingester agent prompt can be written once we understand the shape of this data
