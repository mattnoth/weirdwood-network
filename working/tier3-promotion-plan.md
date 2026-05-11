# Tier 3 Promotion Plan

> **Purpose:** Bring the 2,221 unique missing-target slugs (Cat 1 of orphan-edges audit) into the graph through targeted promotion campaigns.
>
> **Status:** Plan-only. Drafted 2026-04-30 (Session 27) after orphan-edges full sweep landed.

## Source signal

- `working/audits/orphan-edges-2026-04-30/execution/orphan-edges-2026-04-30.md` — full sweep summary
- `working/audits/orphan-edges-2026-04-30-cat1-full.tsv` — every (source_node, edge_type, target_text, target_slug) row
- 7,219 dangling edges across 2,221 unique target slugs

## Pass strategy

Each pass is one-shot, deterministic, ~$0 via the Stage 3 pipeline (`emit-deterministic.py` + `extract-prose.py` + `promote.py`). No LLM agent. Each pass:
1. Filters cat1-full.tsv for the pass's target subset.
2. Looks up each target slug in `working/wiki/data/page-index.jsonl` to confirm a wiki page exists.
3. Builds a one-off bucket (`working/wiki/pass2-buckets/tier3-<pass-name>/manifest.json`).
4. Runs the standard pipeline: emit → extract-prose → promote.

## Pass A — Title nodes (HIGHEST IMPACT)

**Target:** 256 unique title slugs covering 1,154 edges. Single biggest orphan cluster.

**Examples (ranked by orphan-count):**
- `ser` (~693 edges via the bad `ser` alias-resolver entry; remove that entry first then promote `ser` as title)
- `lord`, `lady`, `prince`, `princess`, `king`, `queen`
- `khal`, `khaleesi`, `castellan`, `septon`, `septa`, `maester`
- `bastard`, `sellsword`, `hedge-knight`

**Existing baseline:** 91 title nodes already in `graph/nodes/titles/`.
**Projected after pass:** ~350 title nodes.
**Wiki source check needed:** not every title has a standalone wiki page (e.g., "Ser" → does `Ser_(title)` exist? Probably not). Pass should only promote slugs that have a wiki page; the rest stay orphan and get dropped to a known-acceptable backlog.

**Estimated cost / time:** $0 / ~5 minutes pipeline run.

## Pass B — Cultures (MED IMPACT)

**Target:** Currently undetermined exact count; orphan-edges audit attributed ~2,700 CULTURE_OF dangling but spot-checks show several already exist as factions. Need to filter cat1-full.tsv for `CULTURE_OF` edges that genuinely don't resolve.

**Likely missing:** Crannogmen, Mountain clans of the Vale, Hill tribes, Skagosi, Stoneborn, Cave dwellers, Andals (canonical placement?).

**Type decision:** Use `organization.faction` (matches Tier 2 recovery convention) OR add a new top-level `culture` type. Lean toward `culture` as a new type for cleaner queries — but requires `architecture.md` TYPE_DIR_MAP update first.

**Estimated cost / time:** $0 / ~3 minutes once scoped.

## Pass C — Religions / Gods (MED IMPACT)

**Target:** Currently 4 religion nodes (`faith-of-the-seven`, `drowned-god`, `old-gods-of-the-forest`, `rhllor`). Many `WORSHIPS:` and god-name references dangle.

**Likely missing:** Many-Faced God, Black Goat of Qohor, Lion of Night, Maiden-Made-of-Light, Stranger, Father, Mother, etc. (the individual Seven aspects), Storm God, Lady of Waves, Crab King, Pat the Pig (joke entry), Trios.

**Type:** `religion` (existing top-level type). Patch the 4 religion-bleed nodes' WORSHIPS edges to target the new nodes after promotion.

**Estimated cost / time:** $0 / ~3 minutes.

## Pass D — Character backfill (LARGEST RESIDUAL)

**Target:** The remaining ~1,500 of the 2,221 slugs after Passes A/B/C are minor characters mentioned in family trees, sworn-shield rolls, etc., who weren't in the original Stage 1 / Stage 3 buckets because their wiki pages are stubs or sub-pages.

**Filter approach:**
1. From cat1-full.tsv, keep only `PARENT_OF`, `SPOUSE_OF`, `SIBLING_OF`, `LOVER_OF`, `HEIR_TO`, `KILLS` edges (these target characters).
2. Drop targets that resolve via alias-resolver (Cat 2 already).
3. Cross-check each remaining target against `page-index.jsonl` — drop any that don't have a wiki page.
4. Build a one-off bucket per house surname (or alphabetical chunks) and run pipeline.

**Estimated cost / time:** $0 / ~10 minutes for the full chunk.

## Pass E — Long tail (cleanup)

After A-D, audit again. Whatever remains is probably:
- True graph gaps (entities mentioned in prose but no wiki page)
- Edge-target-text encoding errors that no clean fix exists for
- Concept pages we deliberately didn't promote

Acceptable residual: target <100 unresolved orphans corpus-wide.

## Sequencing

1. **Patch alias-resolver** to remove `ser → gregor-clegane` and `aegon-targaryen → pisswater-prince`. Re-run the resolver builder. Verify Cat 2 count drops to a sane number.
2. **Pass A — Titles** (highest impact, smallest scope).
3. **Pass C — Religions / Gods** (small scope, high quality signal).
4. **Pass B — Cultures** (after type-decision call).
5. **Pass D — Character backfill** (largest scope; most mechanical).
6. **Pass E — Audit residual.**

## Open questions

- New `culture` top-level type, or stay with `organization.faction` for cultures?
- Should Pass A also retro-fit the existing 91 title nodes' format? (They were promoted via Tier 2 recovery; some may be duplicated by this pass.)
- For Pass D, do we need a Pass-1-extraction cross-check before promoting minor characters? Some referenced names may be aliases / nicknames the wiki doesn't have a page for.

## Acceptance criteria

After all passes:
- Cat 1 (genuinely missing) drops from 7,219 edges / 2,221 slugs to <500 edges / <100 slugs.
- Cat 2 (alias-mismatch) cleaned of the two bad mappings (`ser`, `aegon-targaryen`).
- Schema consistency: no edge type drift, no slug-format violations introduced.
- Re-running orphan-edges-audit + duplicate-detector + schema-drift-auditor produces clean reports.
