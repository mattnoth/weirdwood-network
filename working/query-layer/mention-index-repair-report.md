# Mention-Index Repair Report (preview-only, query-layer step 8b)

`graph/index/` is behind the no-graph-mutation gate — this report describes a PREVIEW build at `working/query-layer/mention-index-preview/`, not a live change. Nothing under `graph/` was written by this script.

## Headline

- Live index resolution rate: **73.0%** (27,169 / 37,222)
- Preview index resolution rate: **73.5%** (27,348 / 37,222)
- Chapters whose resolved/unresolved counts would CHANGE: **181** (unchanged: 163, no live file to compare: 0)

## Known-stale spot-checks (before -> after)

Slugs verified this session to have a BULLETED Raw-Entity-List mention (so extraction-parsing is not the confound) that only resolves once the alias source is switched from `alias-resolver.json` (1,433 aliases) to `all-node-alias-lookup.json` (27,588 phrases, the query-layer step-4 hardened table).

| slug | live appearances | preview appearances |
|---|---|---|
| `crow-cage` | 0 | 2 |
| `lemonwater` | 0 | 1 |
| `goat` | 0 | 1 |
| `acorn-paste` | 0 | 0 |

## Known extraction-format gap (OUT OF SCOPE for this repair)

`acorn-paste` does NOT move in this preview (0 -> 0) despite being exactly the case design.md's step-8b card names as the motivating example. Root cause: its one Pass-1 mention (acok-arya-05, 'Raw Entity List > Other') is written as an un-bulleted, comma-separated prose line ("Acorn paste (survival food technique taught by Kurz), water dancer (...)"), not the schema's bulleted list — `build-mention-index.py`'s bullet-only parser (absorbed verbatim here) never extracts it as a mention candidate at all, so no alias-table fix can resolve it. This is a Pass-1 EXTRACTION-format inconsistency, not an alias-table gap — **2464 non-bulleted 'Other'-subsection content lines** exist across the processed corpus (same class of gap). Fixing it would mean either a Pass-1 re-extraction pass or a looser (comma-splitting) parser for this one subsection — both out of scope for the alias-table repair this step delivers. Flagged here, not silently absorbed into the headline number.

## Sample chapter diffs (up to 15)

| chapter | live resolved | preview resolved | live unresolved | preview unresolved |
|---|---|---|---|---|
| agot-arya-03 | 48 | 49 | 33 | 32 |
| agot-arya-04 | 38 | 39 | 32 | 31 |
| agot-bran-06 | 65 | 66 | 32 | 31 |
| agot-catelyn-01 | 89 | 88 | 30 | 31 |
| agot-catelyn-02 | 88 | 85 | 20 | 23 |
| agot-catelyn-03 | 72 | 73 | 31 | 30 |
| agot-catelyn-05 | 49 | 51 | 9 | 7 |
| agot-catelyn-06 | 66 | 67 | 12 | 11 |
| agot-daenerys-01 | 121 | 120 | 69 | 70 |
| agot-daenerys-02 | 59 | 64 | 57 | 52 |
| agot-daenerys-03 | 70 | 74 | 40 | 36 |
| agot-daenerys-05 | 32 | 33 | 14 | 13 |
| agot-daenerys-07 | 30 | 31 | 16 | 15 |
| agot-daenerys-09 | 33 | 34 | 13 | 12 |
| agot-daenerys-10 | 30 | 31 | 22 | 21 |

## Top unresolved slugs remaining in the preview (up to 20)

- `joffrey` — 47
- `aegon` — 27
- `aerys-targaryen` — 25
- `great-pyramid-of-meereen` — 24
- `old-gods` — 22
- `lady-tanda` — 22
- `little-walder-frey` — 22
- `wildlings-free-folk` — 20
- `queen-selyse` — 20
- `big-walder-frey` — 19
- `gold-cloaks` — 18
- `winterfell-godswood` — 18
- `crossbow` — 18
- `the-old-gods` — 17
- `throne-room` — 17
- `the-inn` — 17
- `stables` — 16
- `lord-commander` — 16
- `king-tommen` — 15
- `king-robert` — 14

## Top ambiguous phrases (first-candidate tie-break used, up to 20)

- "pate" — 13 occurrence(s)
- "giant" — 7 occurrence(s)
- "ned" — 3 occurrence(s)
- "merry" — 3 occurrence(s)
- "lord brynden" — 3 occurrence(s)
- "silent sister" — 2 occurrence(s)
- "wull" — 2 occurrence(s)
- "prince that was promised" — 1 occurrence(s)
- "sam the slayer" — 1 occurrence(s)
- "mummer's farce" — 1 occurrence(s)
- "boy king" — 1 occurrence(s)

## Apply command (Matt's go required — NOT run by this script)

```
# Replaces graph/index/chapters/ with the reviewed preview tree.
# This IS a graph/index/ write — needs Matt's explicit go per the no-mutation gate.
rm -rf graph/index/chapters
cp -r working/query-layer/mention-index-preview/chapters graph/index/chapters
# Then re-run the per-entity rollups so graph/index/<type>/ picks up the repair:
bash scripts/weirwood-refresh.sh
```
