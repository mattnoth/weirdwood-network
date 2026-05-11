# Continue: Missing-node backfill — 138 Bucket A unpromoted wiki pages

**Created:** 2026-05-12 (end of Session 42)
**Track:** Track 2 of three parallel-runnable tracks (Track 1 done Session 42; Track 3 has its own continue prompt)
**Status:** Ready, with investigate-first step
**Estimated effort:** One session, pure Python, $0
**Recommended model:** **Sonnet 4.6** (`claude-sonnet-4-6`). This track is pure Python — the LLM only orchestrates script-builder, reads outputs, and writes 138 new node files via deterministic scripts. No agent reasoning, no extraction, no edge classification. Haiku 4.5 also viable if budget is tight; Opus is wasteful here. Per `feedback_model_selection_at_session_start.md` (default to cheapest viable).
**Memory rules in play:** `feedback_python_before_agent.md`, `feedback_no_external_wiki_fetch.md`, `feedback_check_existing_knowledge_first.md`, `feedback_model_selection_at_session_start.md`

---

## What this work is

Promote the 138 wiki pages that Pass 1 actively references but were never given a graph node. Highest-signal slugs (by Pass-1 mention count):

| Slug | Pass-1 hits | Likely type |
|---|---|---|
| `godswood` | 36 | place.location (or new place.feature) |
| `flea-bottom` | 31 | place.location |
| `old-gods` | 22 | organization.religion |
| `seastone-chair` | 14 | object.artifact |
| `chatayas-brothel` | 12 | place.location |
| `black-cells` | 11 | place.location |
| `queens-men` | 9 | organization.faction |
| `unsullied` | 9 | organization.faction |
| `cinnamon-wind` | 8 | object.artifact (ship) |
| `valyrian-steel-dagger` | 8 | object.artifact |

Full Bucket A list: `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.{md,json}`.

## Why they were missed

Path B's categorizer (`scripts/wiki-infobox-parser.py` + the `CATEGORY_TYPE_MAP` constant) routed them to `unknown`. The Stage 3 Python emitter skips `unknown`-typed pages. The result: wiki page exists in `sources/wiki/_raw/`, but no graph node was emitted.

## Investigate-first step (15 minutes)

Before any script work:

1. **Verify wiki cache** — for the top-10 slugs above, check `sources/wiki/_raw/<Capitalized_Page>.json` exists. Most should.
2. **Check page-index entries** — for each one, grep `working/wiki/data/page-index.jsonl` for the page. What does `entity_type_guess` say? If `unknown`, the categorizer rule is the source of the bug.
3. **Check infobox-data** — same grep against `working/wiki/data/infobox-data.jsonl`. Does the page have an infobox at all? If not, the page is text-only and the Track 2 emission path must handle that.
4. **Slug-collision check** — for each top-10 slug, grep `graph/nodes/` for any existing file with that slug or a related slug. `godswood` might collide with `winterfell-godswood`/`kings-landing-godswood` etc.

## Decisions to make before acting

1. **New entity types?** `godswood` is generic. Options:
   - **(a)** Introduce `place.feature` to architecture.md TYPE_DIR_MAP — clean separation between named locations and generic features.
   - **(b)** Force-classify `godswood` as `place.location` with `aliases: ["the godswood"]` — pragmatic, conflates generic-vs-specific.
   - **(c)** Introduce `concept.geography` for generic-feature concepts.
   - **Lean: (b)** — skip type-system invention; let Stage 4 sort it out.
2. **`old-gods` taxonomy** — `organization.religion` (like `the-faith-of-the-seven`) or `concept.theological`? **Lean: `organization.religion`**, consistent with wiki encoding.
3. **Promotion strategy.** All new nodes — no existing-node overwrites. Use a simple write-if-not-exists check; no conflict logic needed. Atomic-write via staging temp file like the other Pass 2 scripts.
4. **Two-script approach?**
   - **(a) Categorizer fix** — fix the `CATEGORY_TYPE_MAP` rule(s), re-run `wiki-infobox-parser.py --apply`, then re-run `wiki-pass2-emit-deterministic.py` scoped to the 138 slugs. Slower but cleaner; catches future similar misses too.
   - **(b) Targeted emitter** — write `scripts/wiki-pass2-bucket-a-backfill.py` that takes the 138-slug list, looks up each one's wiki cache + infobox, decides the type, emits skeleton + prose. Faster, less general.
   - **Lean: (b) for speed, file (a)'s fix as a follow-up.** The categorizer probably has 5-10 other systemic gaps beyond just the 138 Pass-1-referenced ones; that's a separate cleanup pass.

## Existing pieces to reuse

| Resource | Path | Notes |
|---|---|---|
| Skeleton emitter | `scripts/wiki-pass2-emit-deterministic.py` | Produces frontmatter + thin Identity + full Edges from infobox-data + page-index rows. |
| Prose extractor | `scripts/wiki-pass2-extract-prose.py` | Produces prose body sections from cached wiki HTML. |
| Attach-prose tool (NEW Session 42) | `scripts/wiki-pass2-attach-prose.py` | Useful if you emit skeleton-only and want to append prose afterward. |
| Page-index | `working/wiki/data/page-index.jsonl` | One row per wiki page; carries `entity_type_guess` and category list. |
| Infobox-data | `working/wiki/data/infobox-data.jsonl` | One row per page with infobox; carries relationships, aliases, type signature. |
| Cross-references | `working/wiki/data/cross-references.jsonl` | Backlink counts; validates the "Bucket A" sourcing. |
| Audit source | `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.json` | The 138-slug enumeration with mention counts. |

## Implementation sketch (if going with option b)

1. **Load the Bucket A slug list** from `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.json`.
2. **Per-slug type decision tree** (use this order):
   - If `infobox-data.jsonl` has the page: use `entity_type` from that row (apply CATEGORY_TYPE_MAP correction first if needed).
   - Else if wiki cache has only a list/disambiguation: skip (will not be a graph-traversal-useful node).
   - Else default to `place.location` for region-like slugs (flea-bottom, godswood), `object.artifact` for thing-slugs (seastone-chair, cinnamon-wind), `organization.faction` for group-slugs (unsullied, queens-men), etc.
3. **Skeleton render** — reuse `render_skeleton()` logic from `wiki-pass2-emit-deterministic.py`. Frontmatter + Identity stub + Edges from infobox.
4. **Prose extract** — reuse `extract_sections()` from `wiki-pass2-extract-prose.py` against the wiki cache.
5. **Concatenate** — `final_bytes = skeleton + b"\n" + prose` (or skeleton-only if no prose).
6. **Write to `graph/nodes/<type-dir>/<slug>.node.md`** via atomic-rename. If destination already exists: skip (don't overwrite — this script is purely additive).

## Smoke-test slugs (verify after)

- `godswood` → `graph/nodes/locations/godswood.node.md` with body covering weirwood-grove concept across the North.
- `flea-bottom` → `graph/nodes/locations/flea-bottom.node.md` covering the King's Landing slum.
- `seastone-chair` → `graph/nodes/artifacts/seastone-chair.node.md`.
- `old-gods` → `graph/nodes/religions/old-gods.node.md` (or wherever the categorizer places `organization.religion`).
- `unsullied` → `graph/nodes/factions/unsullied.node.md`.

**Smoke-test post-action:** re-run `scripts/audit-missing-nodes.py` and confirm Bucket A drops from 138 → near-zero.

## Expected delta

- ~138 new graph nodes across locations/, factions/, religions/, artifacts/.
- Mention-index resolution rate jumps significantly: `godswood` alone is +36 newly-resolvable mentions; `flea-bottom` +31; `old-gods` +22. Expect mention-index resolution to cross 75% (up from 70.6%).
- Per-character indexes for characters who frequent these new locations (Tyrion ↔ Chataya's brothel, Stannis ↔ Queen's Men, Daenerys ↔ Unsullied) get richer `mentioned_in` lists.

## What this unblocks downstream

- **Stage 4 prose-edge-classifier** — fewer missing-node targets means fewer orphan edges and cleaner same-as candidate detection.
- **Per-LOCATION index roll-up** (Track 3) — adds 100+ new location nodes to the location-index population.
- **Cross-character traversal** — "show me all characters who appear in Flea Bottom" becomes a real query instead of returning a no-such-node error.

## DO NOT

- Refetch any wiki pages. The wiki is local. (`feedback_no_external_wiki_fetch.md` — hard rule.)
- Touch Stage 1 agent-rich nodes (`pass_origin: pass2-wiki`).
- Overwrite existing graph nodes if a slug collision is discovered — log it for review instead.
- Try to fix the 125 case-collision pages here — separate todo (`Track 4` in next.md).
- Auto-run `/endsession` — Matt's standing rule (`feedback_endsession_requires_permission.md`).

## After this lands

- Mark `working/todos.md` HIGH "Missing-node backfill: 138 Bucket A unpromoted wiki pages" as `[x] DONE` with actual delta.
- Re-run `scripts/build-mention-index.py --all` — new resolution rate.
- Re-run `scripts/build-character-indexes.py --all` — richer mentioned_in lists.
- Add Session entry to worklog.
- If categorizer-fix path (a) is deferred: file it as a NEW todo in `working/todos.md`.
