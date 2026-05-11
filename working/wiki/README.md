# `working/wiki/` — Wiki Pipeline Workspace

This directory holds everything the wiki pipeline produces from `sources/wiki/_raw/` (the local cache of the AWOIAF wiki). It is split into three subdirectories by **lifetime**, not by pipeline stage.

## Subdirectories

### `data/` — permanent reference products

Derived data products that downstream code reads. These are stable; they get rebuilt when source data changes, but they are not tied to any specific run.

| File | What | Built by |
|---|---|---|
| `alias-resolver.json` | Canonical-slug → variant-slug map (e.g., `eddard-stark` ← `ned`). 53 KB. | `scripts/wiki-pass2-build-alias-resolver.py` |
| `page-index.jsonl` | Metadata for all 17,657 wiki pages (slug, title, length, redirect target, etc.). 5 MB. | `scripts/wiki-infobox-parser.py` |
| `infobox-data.jsonl` | Structured infobox fields for 5,279 pages with infoboxes. 3 MB. | `scripts/wiki-infobox-parser.py` |
| `page-categories.jsonl` | MediaWiki categories for each page (backfilled 2026-04-30). 2.8 MB. | `scripts/wiki-fetch-categories.py` |
| `cross-references.jsonl` | Every `[anchor](wiki:Page)` link found in node prose. 34 MB. | `scripts/wiki-pass2-build-cross-refs.py` |
| `chronology-events.jsonl` | 2,245 dated events extracted from year pages. 840 KB. Awaits temporal-edges schema. | `scripts/wiki-pass2-extract-chronology.py` |
| `backlink-counts.json` | Per-page incoming-link counts. 1.8 MB. | (script) |
| `parse-stats.md` | Human-readable summary of infobox parser run. | `scripts/wiki-infobox-parser.py` |
| `cross-refs-summary.md` | Human-readable summary of cross-reference build. | `scripts/wiki-pass2-build-cross-refs.py` |

If you're an agent looking for something derived from the wiki, **start here.**

### `pass2-buckets/` — Pass 2 promotion run workspace

536 per-bucket folders from the Wiki Pass 2 promotion pipeline. Each bucket folder contains:

```
<bucket-name>/
  ├── bucket_input.json     # Pages assigned to this bucket
  ├── manifest.json         # Per-bucket run state, tier, mode
  ├── tmp/                  # Scratch from the run
  └── validator-report.json # Schema validation output
```

These were the *inputs and outputs of a specific run* — Stage 1 (855 nodes from 37 buckets) and Stage 3 (3,314 nodes from 472 buckets). The actual graph nodes that resulted live in `graph/nodes/`, not here. This directory is preserved so future Pass 2 stages (e.g., Stage 4 prose-edge-classifier) can target specific buckets.

### `pass2-staging/` — Pass 2 staging artifacts

Run-specific staging files that informed the Pass 2 promotion but aren't permanent reference data. Kept separate from `data/` because they describe *one specific run*, not the wiki itself.

- `triage-bucket-assignments.jsonl` — page-to-bucket assignments
- `triage-manifest.jsonl` — bucket membership canonical
- `draft-buckets.jsonl` — pre-triage bucket drafts
- `priority-summary.json` — bucket priority scoring
- `stage3-promote-summary.json` — Stage 3 promotion summary
- `stage3a-emission-summary.json` — Stage 3a (skeleton) emission
- `stage3b-extraction-summary.json` — Stage 3b (prose) extraction

## History note

This directory was created on 2026-05-07 by a reorg. Previously the contents lived flat under `working/wiki-parsed/` and `working/wiki-pass2/`. **Historical session details, archived continue prompts, and audit execution logs reference the old paths and were intentionally not rewritten** — those records describe what was true at the time they were written.

## What is *not* here

- `sources/wiki/_raw/` — the local wiki cache (read-only source data)
- `graph/nodes/` — the actual promoted graph
- `graph/index/chapters/` — the per-chapter mention-index (a different pipeline)
