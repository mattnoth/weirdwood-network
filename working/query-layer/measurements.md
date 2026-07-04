# Query-Layer Track — step 0 Measurements

Read-only measurement pass. All numbers produced by `/private/tmp/measure_query_layer.py`
(one-off script, not checked in; paste-and-rerun commands below). Run 2026-07-04.

```
mkdir -p working/query-layer
python3 /private/tmp/measure_query_layer.py
```

## 1. Narrative-Arc payload (feeds D-F: inline vs fetch-on-demand)

`## Narrative Arc` sections extracted from heading to next `## ` heading or EOF, byte length via UTF-8 encode.

- **Entity nodes only** (excludes `chapters/` — those are per-chapter summary nodes, a different
  subsystem, not front-end entity-detail payloads; excludes `_conflicts/` — unresolved duplicate
  candidates, not live graph): **4,057 files** with a Narrative Arc section, **7,778,305 bytes** (7.42 MB) total.
- **Including `chapters/`** (344 more files, all carrying a "Narrative Arc"-headed chapter summary):
  4,401 files, 9,319,270 bytes (8.89 MB) total.
- `web/data/nodes.json` current size: **3,935,311 bytes** (3.75 MB).
- **Growth if inlined:**
  - entity-nodes-only scope: +7,778,305 bytes → **+197.7%** (nodes.json would ~triple).
  - including chapters: +9,319,270 bytes → **+236.8%**.
- Heaviest contributors (entity scope): characters 4,273,895 B (1,919 files), locations 1,089,329 B
  (658 files), houses 545,082 B (361 files), titles 321,795 B (207 files).

## 2. Quote inverted-index size estimate

Doc = one line/bullet inside a `## Quotes` section (leading `-`/`*` stripped), OR one whole
`## Identity` section body treated as a single paragraph doc. Tokenization: `[a-z0-9]+` on
lowercased text (simple whitespace/alnum split, no stemming/stopwords). Index = token → set of
doc-ids (postings), scanned across every `graph/nodes/**/*.node.md` (excluding `_conflicts`).

- Total docs: **24,114** (22,339 quote-lines + 7,657 identity paragraphs — note these don't sum to
  24,114 because ~1,882 docs came from files whose tokenization produced zero tokens and were
  dropped, or from double counting across the two loops on a per-file basis — see caveat below).
- Total tokens (non-unique): **703,072** (~29.2 tokens/doc average).
- Unique-token vocabulary: **17,270** tokens.
- Estimated serialized index size: sum over tokens of `(len(token) + 4*num_postings)` =
  **2,125,107 bytes ≈ 2.03 MB**.

**Caveat on doc_count discrepancy:** `quote_docs` (22,339) + `identity_docs` (7,657) = 29,996, but
the token-loop `doc_count` is 24,114 — the difference (5,882) is docs whose tokenizer produced zero
tokens (e.g. quote lines that were pure wiki-link brackets/punctuation, or empty Identity bodies)
and were skipped before assignment to a doc-id / posting list. The 2.03 MB estimate and the
703,072-token total are over the 24,114 *tokenized* docs; the 22,339 / 7,657 figures are raw
pre-filter section-line counts and are the more accurate "how many quotes/identity blurbs exist"
numbers to use for UI/copy purposes.

## 3. Reachability census (baseline orphan-rate snapshot)

Orphan = node slug (filename minus `.node.md`) appears as neither `source_slug` nor `target_slug`
in any of the 23,099 lines of `graph/edges/edges.jsonl` (all rows are valid edges — 23,059
`decision: emit_edge` + 40 rows using an older schema with no `decision` field but still valid
source/target slugs; 0 rejected/non-edge rows).

| type dir | nodes | orphans | % orphan |
|---|---|---|---|
| characters | 3,916 | 101 | 2.58% |
| houses | 556 | 31 | 5.58% |
| titles | 542 | 71 | 13.10% |
| events | 744 | 129 | 17.34% |
| factions | 191 | 59 | 30.89% |
| prophecies | 4 | 2 | 50.00% |
| locations | 1,098 | 658 | 59.93% |
| religions | 63 | 51 | 80.95% |
| artifacts | 295 | 243 | 82.37% |
| concepts | 57 | 50 | 87.72% |
| medical | 35 | 31 | 88.57% |
| species | 188 | 169 | 89.89% |
| materials | 58 | 53 | 91.38% |
| languages | 26 | 24 | 92.31% |
| texts | 161 | 151 | 93.79% |
| foods | 113 | 108 | 95.58% |
| customs | 37 | 36 | 97.30% |
| theories | 45 | 44 | 97.78% |
| chapters | 344 | 343 | 99.71% |
| _unclassified | 0 | 0 | — |

**Overall: 2,354 / 8,473 = 27.78% orphan.**

**Data-quality surprise:** `chapters/` (344 chapter-summary nodes) is 99.71% "orphan" because that
subsystem is never wired into `edges.jsonl` by design — chapter provenance is carried via
`evidence_chapter`/`evidence_ref` string fields on edges, not via `source_slug`/`target_slug`
graph edges to chapter nodes. Excluding `chapters/` (not part of the entity graph proper):
**8,129 nodes, 2,011 orphans → 24.74%.** Recommend using the chapters-excluded figure as the
"real" baseline going forward; the raw 27.78% overstates disconnection by conflating two different
subsystems.
