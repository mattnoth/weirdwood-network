# Tier 3 Pass E Phase 2 — Completeness on remaining residuals

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-04-30 end of Session 27. Phase 1 cleanup committed (`7b723f8`). Option C (Stage-1 prose-only re-emission) was running at session end — verify its commit landed before starting Phase 2.

## Where we are

The graph is at ~5,000 nodes after Tier 3 Passes A-D + Pass E Phase 1. Cat 1 orphan edges are at 2,955 (down from 7,784 pre-Tier-3, 62% reduction). The remaining 1,174 unique missing-target slugs are mostly:

- **Locations** not yet promoted (specific castles, towns, geographical features)
- **Factions** not yet promoted (smaller military orders, mercenary companies, criminal organizations)
- **Events** beyond what Tier 1 caught (battles, plots, councils)
- **In-world books and texts** (`Fire and Blood`, `The Seven-Pointed Star`, `A World of Ice and Fire`, etc.) — these classify as `entity_type_guess: unknown` because the parser doesn't recognize the book-infobox signature; they got dropped during triage. **WRITTEN_BY edge type is in the locked vocabulary but ZERO WRITTEN_BY edges currently exist** because no books are nodes.
- **"Concepts"** — Dance-of-the-Dragons faction names (`blacks`, `greens`), governance terms (`small-council`, `great-council`)

## What to read first

1. `working/audits/orphan-edges-2026-05-01.md` — most recent audit, residual breakdown (or re-run `python3 scripts/orphan-edges-audit.py 2026-05-XX` if dated for current run)
2. `working/audits/orphan-edges-2026-05-01-cat1-full.tsv` — every dangling edge as a row
3. `working/tier3-promotion-plan.md` — original Tier 3 plan (Phase 2 == "Pass E completeness" within it)
4. `worklog.md` — current state checklist
5. `scripts/wiki-pass2-tier3-pass-{a-titles,b-cultures,c-religions,d-characters}.py` — completed pass scripts; pattern to mirror

## Phase 2 has 4 sub-tasks

### Sub-task 1 — Books / in-world texts pass (NEW, surfaced this session)

Add `object.text` overrides for known books in `scripts/wiki-infobox-parser.py`'s `ENTITY_TYPE_OVERRIDES` dict. Confirmed candidates from the wiki cache:
- `Fire and Blood`, `The Seven-Pointed Star`, `A World of Ice and Fire`
- `The Princess and the Queen`, `The Rogue Prince`, `The Dance of the Dragons`
- `The Lineages and Histories of the Great Houses of the Seven Kingdoms`
- Plus the existing `battle-of-the-blackwater-song` in `_unclassified/`

Then expand: grep `working/wiki-parsed/page-index.jsonl` for entries with `cite_ref_books` populated but `entity_type_guess: unknown` — many are likely in-world texts.

After overrides, run a one-off Stage 3 pipeline (mirror `wiki-pass2-tier3-pass-a-titles.py`) → emit + extract-prose + promote → `graph/nodes/artifacts/<slug>.node.md` (or rename TYPE_DIR_MAP to route `object.text` somewhere distinct like `texts/`).

**Expected outcome:** ~30-50 book nodes added; previously-orphan WRITTEN_BY edges from Maester/Septon characters resolve; first-time WRITTEN_BY signal in the graph.

### Sub-task 2 — Locations / events / factions completeness

Filter `orphan-edges-2026-05-01-cat1-full.tsv` for non-character / non-title / non-religion edge types and target slugs that have wiki pages. Mirror Pass A pattern. Expected scope: ~400-600 nodes. Edge types to focus on: `REGION_OF`, `OVERLORD_OF`, `RULES`, `SEAT_OF`, etc. with non-existing target slugs.

### Sub-task 3 — Concept page decision

`small-council`, `great-council`, `kingsmoot`, `tourney`, etc. — glossary-style concept pages. Per `working/todos.md` Tier 3 todo, the recommendation was **option (iii) defer**. With Phase 2 closing out Pass E, decide: defer permanently, or promote with a `concept` type? If promote, ~20-30 nodes.

Recommend deferring unless Stage 4 surfaces specific need.

### Sub-task 4 — Final verification

After 1-3 land:
- Re-run `orphan-edges-audit.py`
- Re-run `duplicate-detector` for any new variant duplicates introduced
- Re-run `schema-drift-auditor` against full corpus (we never ran it on the FULL graph — only samples)
- Spot-check via `graph-query.py`

**Acceptance criteria from tier3-promotion-plan.md:** Cat 1 drops to <500 edges / <100 slugs corpus-wide.

## Things deferred (explicitly NOT in Phase 2)

- **Stage-1 character cite-format divergence** (978 verbose-cite occurrences) — handled by Stage 4 prose-edge-classifier when it lands. Option C may have addressed prose enrichment but not edge format.
- **42 BORN_AT/DIED_AT date-bleed remaining** — parser-floor cases (wiki has only dates, no location). Resolves when year-period nodes exist or via parser suppression.
- **The 19+1 misclassified-as-title cases now living in `factions/` as cultures** — directory mixing `organization.faction` literal factions with cultures. Future taxonomy split (proper `culture` type with own dir) is a separate decision.

## Hard constraints

- **NEVER touch Stage-1 character nodes** (`prompt_version: v1` in characters/) unless Option C completed and the carve-out is documented as resolved. Verify via worklog.
- **NEVER modify the locked edge vocabulary** in `reference/architecture.md`.
- **NEVER introduce new entity types** without first updating `reference/architecture.md`'s TYPE_DIR_MAP.
- **Atomic-rename invariant** for all writes to `graph/nodes/`.
- **Slug-correctness check** after every sub-task — `grep '^slug: .*\.node$'` should be 0.
- **The wiki cache is read-only** — never re-fetch (`sources/wiki/_raw/` only).
- **NO SOURCE TEXTS COMMITTED** — `sources/raw/` and `sources/chapters/` are gitignored; never override.

## Don't

- Don't run `/endsession` without explicit permission.
- Don't auto-launch agents without confirming with Matt.
- Don't try to rebuild `alias-resolver.json` without running with `--apply` flag.
- Don't introduce parser changes without re-running `wiki-infobox-parser.py` end-to-end + verifying `infobox-data.jsonl` regenerated.

## Recommended order

1. Verify Option C committed (was running at end of Session 27).
2. Sub-task 1: books pass (highest novelty, unlocks WRITTEN_BY).
3. Sub-task 2: locations/events/factions completeness (largest scope).
4. Sub-task 3: defer unless surfaced — light triage.
5. Sub-task 4: full audits + commit.

Each sub-task gets its own commit. Total expected: 3-4 commits, ~500-700 new nodes, Cat 1 drop to <500 edges.
