# Path B Promotion — Convert 2,320 Newly-Classified Entities Into Graph Nodes

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-04-30 end of Session 28. All Session 28 work committed (categorizer-fix commits — verify with `git log --oneline -10`). Working tree clean except for `scratch` / `wiki-logs-` typo'd debris (leave them).

---

## What happened in Session 28 (the prerequisite)

Phase 2 of Tier 3 was originally scoped as "promote ~30-50 books + ~15-30 weapons via per-page `ENTITY_TYPE_OVERRIDES`". A structural finding pivoted the session:

- **The wiki cache had a fossil categorizer.** The original Playwright crawl (archived) included an entity-type categorizer that mapped MediaWiki **categories** (curated wiki tags like `Swords`, `Books and scrolls`, `Castles`, `Battles`) to project entity types via `CATEGORY_TYPE_MAP`. Only the name-based fast path (`if page.startswith("House ")`) ran, populating `sources/wiki/houses/`. The other directories (`characters/`, `locations/`, `events/`, `artifacts/`) are **empty** — the categorizer needed category data and the original crawl's `action=parse` API stripped catlinks footers.
- **Path B fix:** The hard no-re-fetch rule was given one documented narrow exception. A bounded one-time fetch via `cloudscraper` (NOT Playwright — verified 2026-04-30 plain `urllib` is 403'd by Cloudflare; `cloudscraper` returns 200) backfilled MediaWiki categories for all 17,657 pages into `working/wiki-parsed/page-categories.jsonl`.
- **Parser extended** with `CATEGORY_TYPE_MAP` (`scripts/wiki-infobox-parser.py`). Resolution order: `ENTITY_TYPE_OVERRIDES` > `PAGE_NAME_TYPE_PATTERNS` > **categories (NEW)** > `classify_by_species()` > `classify_entity_type()` > unknown. Skip-categories (Redirect, Disambiguation, TV-only) classify as `skip` to filter promotion.
- **`unknown` dropped from 12,434 (70.4%) to 2,487 (14.1%).** `object.artifact` 1→233. `object.text` 0→185. `place.location` 142→967. `concept.magic` 0→32. `organization.religion` 0→32.

**Verified files:**
- `working/wiki-parsed/page-categories.jsonl` — 17,657 rows, MediaWiki categories
- `working/wiki-parsed/page-index.jsonl` — REGENERATED with new types
- `working/wiki-parsed/infobox-data.jsonl` — REGENERATED
- `working/wiki-parsed/triage-bucket-assignments.jsonl` — renamed from misnamed `page-categories.jsonl`
- `CLAUDE.md` — narrow exception clause + 2026-04-30 audit log entry
- `scripts/wiki-fetch-categories.py` — new exception-fetch tool

**Hard constraints from Session 28 (still apply):**
- `sources/wiki/` is read-only. Outputs go to `working/wiki-parsed/` and `graph/`.
- Re-fetch rule: still default-NO. Session 28's exception was per-occasion. If a new gap surfaces, raise it explicitly with Matt before fetching.

---

## What this session needs to do

Promote 2,320 newly-classified entities into `graph/nodes/` directories that match their types. Quantified pool:

| Type | New entities to promote | Target dir |
|---|---|---|
| `place.location` | 762 | `graph/nodes/locations/` (currently empty — first nodes here) |
| `character.human` | 373 | `graph/nodes/characters/` |
| `event.battle` | 338 | `graph/nodes/events/` (verify TYPE_DIR_MAP) |
| `organization.house` | 243 | `graph/nodes/houses/` |
| `object.artifact` | 197 | `graph/nodes/artifacts/` (currently 1 node) |
| `object.text` | 182 | `graph/nodes/texts/` (currently empty — first nodes here) |
| `title` | 55 | `graph/nodes/titles/` |
| `event.war` | 44 | `graph/nodes/events/` |
| `concept.magic` | 32 | new dir? `graph/nodes/concepts/` or per-type — verify TYPE_DIR_MAP |
| `organization.religion` | 25 | `graph/nodes/religions/` |
| `organization.faction` | 21 | `graph/nodes/factions/` |
| `species` | 18 | new dir? `graph/nodes/species/` |
| `concept.culture` | 15 | `graph/nodes/factions/` (per Tier-2 placeholder) or `graph/nodes/cultures/` |
| `character.dragon` | 8 | `graph/nodes/characters/` (subfile) |
| `place.region` | 7 | `graph/nodes/regions/` (verify) |

**Total: 2,320 new graph nodes.** This roughly doubles the graph (currently 5,008 → ~7,300).

---

## Recommended approach

### Step 1 — Verify TYPE_DIR_MAP coverage

Check `scripts/wiki-pass2-promote.py` for the canonical `TYPE_DIR_MAP`. Confirm directory targets for:
- `concept.magic`, `concept.culture`, `concept.prophecy`, `concept.theory`
- `species`
- `place.region`

If any aren't mapped, decide direction (new dir or fold under existing parent) and update the map. Architecture.md is the source of truth — its hierarchy says concepts belong under `Concept` parent; whether they share a dir or split is open.

### Step 2 — Build a Tier 3 Path B Promotion script

Mirror `scripts/wiki-pass2-tier3-pass-a-titles.py` but driver-agnostic to `entity_type_guess`. Read every record from `page-index.jsonl` where:
- `entity_type_guess` is in the classifiable types (NOT `unknown`/`skip`)
- `slug` not already in any `graph/nodes/<dir>/` directory
- `entity_type_guess` is NOT in a list of "promote-pause" types if you want to gate certain categories.

Per-type bucket: `working/wiki-pass2/pathb-<type>/manifest.json` + `skeleton/` + `prose/`. Build all skeletons via `wiki-pass2-emit-deterministic.py` patterns; extract prose via `wiki-pass2-extract-prose.py`. Promote with atomic-rename to `graph/nodes/<type-dir>/<slug>.node.md`.

### Step 3 — Stage by type, commit per type

Single mega-commit is too large to review. Suggested order, each as own commit:

1. **`object.text` (182 books/songs/scrolls)** — completes original sub-task 1a; smallest blast radius for first promotion.
2. **`object.artifact` (197 swords/ships/etc.)** — completes original sub-task 1b. Resolves orphan WIELDS edges (jon→Longclaw, arya→Needle, visenya→Dark Sister).
3. **`place.location` (762)** — biggest single batch. Carve into 2-3 sub-commits if review ergonomics demand (geographic groupings).
4. **`event.battle` (338) + `event.war` (44)** — events together.
5. **`organization.house` (243) + `organization.religion` (25) + `organization.faction` (21)** — organizations.
6. **`character.human` (373) + `character.dragon` (8)** — characters last; biggest semantic risk because new character pages may collide with existing identity-disambiguation work.
7. **`concept.magic` (32) + `concept.culture` (15) + `species` (18) + `place.region` (7) + `title` (55)** — long-tail.

### Step 4 — Audits

After each batch:
- `scripts/orphan-edges-audit.py` — should drop further (Cat 1 currently 2,955; expect <1,000 after locations land because most missing-target slugs become real nodes)
- `scripts/wiki-pass2-duplicate-detector.py` — check for variant slug duplicates (Pass B precedent: andal/andals/dornish/dornishmen)
- `scripts/graph-query.py <slug>` — spot-check 5-10 nodes per batch
- Slug-correctness regex check (`grep '^slug: .*\.node$' graph/nodes/**/*.node.md` should return 0)

### Step 5 — Final corpus audit

After all 2,320 promoted:
- `schema-drift-auditor` agent on full corpus (~$50 with opus per Matt's Session 27 approval) for sign-off
- `citation-validator` re-run
- Update `worklog.md` Current State checklist
- Decide on residual 2,487 `unknown` pages (extend `CATEGORY_TYPE_MAP` for `Animals`/`Plants`/`Theories`/`Tourneys`/`Halls` etc., or accept and move on)

---

## Things explicitly DEFERRED (NOT in this session's scope)

- **WRITTEN_BY edges from books.** In-world books mostly lack infoboxes; "Written by X" lives in prose body. Stage 4 prose-edge-classifier is the architectural home, not this session.
- **WIELDS edges from artifacts.** Same — prose-derived. The 3 existing orphan WIELDS edges (jon→Longclaw, arya→Needle, visenya→Dark Sister) get auto-resolved when those targets land as nodes during sub-task 1b.
- **88 garbage WRITTEN_BY edges in infobox-data.jsonl** for TV episodes (parser misreads "Followed by" infobox field). All TV pages now `skip` post-Path-B, so these never promote. Don't fix the parser — let the skip-classification short-circuit it.
- **Stage-1 character cite-format divergence** (978 verbose-cite occurrences in 596 v1 character nodes) — handled by Stage 4 prose-edge-classifier.
- **Year/era nodes** (`131 AC` etc., `Years` category, 74 unknowns) — Tier 3 chronology-extractor agent's job. NOT this session.
- **Concept pages** (small-council, kingsmoot, tourney, marriage) — `concept.magic` and `concept.culture` are now classified, but small-council-type glossary pages still classify as `unknown` or `skip`. Defer per Tier 3 plan.
- **Stage 4 prose-edge-classifier build** — separate continue prompt at `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`.

---

## Quick-reference investigation commands

```bash
# Current state
find graph/nodes -name '*.node.md' | wc -l
python3 scripts/orphan-edges-audit.py 2026-05-XX

# Inspect a single node end-to-end
python3 scripts/graph-query.py <slug>

# Re-confirm Path B classification still healthy (no regression)
python3 -c "
import json, collections
d = collections.Counter()
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        d[r.get('entity_type_guess')] += 1
for k, v in d.most_common():
    print(f'  {k:30s} {v:>6}')
"

# List pages that classify as a specific type but aren't yet in graph
python3 -c "
import json, re, pathlib
def s(n):
    n = re.sub(r\"['\\\",]\", '', n.lower())
    n = re.sub(r'[ _]+', '-', n)
    n = re.sub(r'[^a-z0-9-]', '-', n)
    return re.sub(r'-+', '-', n).strip('-')
have = {f.name[:-len('.node.md')] for d in pathlib.Path('graph/nodes').iterdir() if d.is_dir() and not d.name.startswith('_') for f in d.glob('*.node.md')}
TARGET = 'object.text'  # change as needed
with open('working/wiki-parsed/page-index.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if r.get('entity_type_guess') == TARGET and s(r['page']) not in have:
            print(s(r['page']), '->', r['page'])
" | head -30
```

---

## Hard constraints (carry-forward)

- **The wiki cache and `sources/wiki/` are read-only.** No writes. Outputs go to `working/wiki-parsed/` and `graph/`.
- **Re-fetch rule still default-NO.** The 2026-04-30 categories backfill was a per-occasion exception. New gap → ask Matt FIRST.
- **NEVER touch Stage-1 character nodes** (`prompt_version: v1`) without explicit Stage-1 carve-out. Option C did prose-only enrichment; their edge sections are still preserved verbatim. Stage 4 prose-edge-classifier handles their edge format.
- **NEVER modify the locked edge vocabulary** in `reference/architecture.md`. Procedure: architecture.md FIRST → parser FIELD_EDGE_MAP → re-run parser.
- **Atomic-rename invariant** for all writes to `graph/nodes/`. Build in temp/tmp; rename at the end.
- **Slug-correctness check** after every sub-task — `grep '^slug: .*\.node$' graph/nodes/**/*.node.md` should return 0. (Session 27 introduced + fixed a `Path.stem` bug across 1,120 nodes; the fix is `stem.removesuffix(".node")`.)
- **NO SOURCE TEXTS COMMITTED** — `sources/raw/` and `sources/chapters/` are gitignored.

---

## Don'ts (process)

- **Don't run `/endsession` without explicit permission.** Historically violated multiple times.
- **Don't auto-launch promotion runs without confirming with Matt.** Each batch (Step 3 above) gets confirmed separately, especially the 762-location batch.
- **Don't promote variant duplicates as separate nodes.** Pass B precedent: `andal/andals`, `dornish/dornishmen/dornishman`, `lhazareen/lhazarene` were promoted then merged — avoid recurrence by checking aliases AGAINST canonical slug before emitting a new node. The existing `scripts/wiki-pass2-build-alias-resolver.py` should be re-run after each batch.
- **Don't extend `CATEGORY_TYPE_MAP` aggressively this session.** The 2,487 residual `unknown` is principled. Better to extend AFTER the easy 2,320 are promoted, then iterate.
- **Don't try to rebuild `alias-resolver.json` without `--apply`.** Default is dry-run.
- **Don't run the schema-drift audit on full corpus until all Path B batches land.** Sample audits per batch are sufficient until the final sign-off step.

---

## Recommended order (concrete)

1. Verify session-startup state. `git log --oneline -10` should show Session 28's commits. `git status` should be clean except typo'd debris.
2. Re-confirm classification distribution (Quick-reference command #3 above) hasn't regressed.
3. **Sub-task 1a — books/texts pass (182 nodes)** — first commit. Smallest, most novel, completes original Phase 2 1a.
4. **Sub-task 1b — artifacts pass (197 nodes)** — second commit. Completes original Phase 2 1b. Resolves orphan WIELDS edges.
5. PAUSE for Matt review before moving to larger batches (locations, characters).
6. **Sub-task 2 — locations (762)** — third commit (or split into 2-3).
7. **Sub-task 3 — events (382)** — fourth commit.
8. **Sub-task 4 — organizations (289)** — fifth commit.
9. **Sub-task 5 — characters (381)** — sixth commit. Run cross-identity-detector samples.
10. **Sub-task 6 — long-tail (127)** — seventh commit (concepts, species, regions, titles).
11. Final audits (Step 4) → archive Phase 2 continue prompts.

Each batch = own commit. Total expected: 7-9 commits, ~2,320 new nodes, Cat 1 orphan edges drop to <500 (acceptance criteria from `working/tier3-promotion-plan.md`).

---

## Session 28 commit history (reference)

After Session 28 ends, `git log --oneline -10` should show roughly:
- Session 28 worklog entry + session-028.md detail
- Path B: parser extended with category-based classification + categories backfill
- Path B: rule exception documented in CLAUDE.md + memory feedback
- (and the 9 prior commits from Sessions 26-27)

If any of these are missing, the session didn't end cleanly — investigate before proceeding.
