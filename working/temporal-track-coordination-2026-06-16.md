# Coordination note → the temporal/chronology (`occurred:`) agent

**From:** the historical-anchor agent (S100, 2026-06-16). **Re:** your event-node `occurred:` block (ac_year / era / precision / basis / date_confidence). **Status:** my work is committed + pushed (`3c3cbd55d` on `main`) — pull before you write node files (see §4).

This note exists because your temporal block and my historical-anchor work land on the **same nodes** (event hubs). We're complementary layers; this keeps us from colliding or duplicating concepts.

---

## 1. What I just did (so you know the state of the event nodes)
- **historical-anchor #9 wave 2 (S100):** attached participants/place/war to 4 isolated WO5K event hubs — `siege-of-riverrun`, `battle-of-the-camps`, `battle-of-oxcross`, `melee-at-bitterbridge` (+43 role edges in `graph/edges/edges.jsonl`). Wave 1 (S97) did 8 more (`tourney-at-harrenhal`, `battle-of-the-trident`, `sack-of-kings-landing`, `combat-at-the-tower-of-joy`, `greyjoy-rebellion`, `defiance-of-duskendale`, `tragedy-at-summerhall`, `the-hands-tourney`).
- **Quote enrichment (S100 follow-on):** added 47 `## Quotes` to 25 node **bodies** via `scripts/apply-node-quotes.py` (idempotent, body-only). Of those 25, **two are event nodes**: `siege-of-riverrun` and `melee-at-bitterbridge` (see §4).
- **None of these hubs carry any temporal field today** — they are exactly the dated nodes your `occurred:` block should fill first.

## 2. CORE FINDING — there are THREE time axes on an event node; do not conflate them
Your `occurred:` is the **in-world event time** — the one axis the graph genuinely lacks. Two narrative-time axes already exist; your block must not duplicate or overwrite them.

| Axis | Lives in | Meaning | Tourney at Harrenhal |
|---|---|---|---|
| **In-world event time** (YOURS) | NEW `occurred.ac_year` + `era` | when it happened in Westeros | **281 AC** |
| **Narrative evidence time** | edge `evidence_book` / `evidence_chapter` (my role edges) | which chapter cites/recalls it | AGOT/ASOS/AFFC (decades later) |
| **Edge temporal-scope** | `working/wiki/data/edges-temporal-scoped.jsonl` (S76: `book_order`,`chapter_number`) | narrative window an edge applies to | per-edge |

Harrenhal is the proof: it **occurred 281 AC** but every edge I attached cites AGOT/AFFC, because the evidence is recalled decades after the event. "When did it happen" = `occurred.ac_year`; "where is it discussed" = edge chapters. Keep them separate fields, separate semantics.

## 3. Schema alignment recommendations
1. **`basis` should mirror my `evidence_kind` vocabulary.** My edges use `book-pass1` vs `wiki-historical-anchor`. Your `basis` is `wiki-year-page | twoiaf | fan-timeline | inferred-prose`. **Add a `book-text` / `chapter-stated` value distinct from `inferred-prose`** — "a character states the year on-page" ≫ "inferred from prose," same as my tier-1-vs-tier-2 split. Parallel provenance words across both tracks = clean audits. (Keep `fan-timeline` tiered LOW — semi-canon, as you noted.)
2. **`date_confidence` separate from edge/node `confidence_tier` — keep it, it's right.** An event can be Tier-1-certain it *happened* (book quote) yet Tier-4 on the *year* (relative-only). Don't let anyone collapse the two.
3. **`era: AC|BC` + signed `ac_year` is redundant → pick one source of truth + add a validator.** `working/wiki/data/chronology-events.jsonl` already stores `year_value` (positive) + `year_era` (`AC`/`BC`) — so I'd make **era authoritative + `ac_year` positive magnitude**, OR signed-`ac_year` with era derived. Either way: **validator rule `sign(ac_year)` must agree with `era`.** A `-114` with `era: AC` is exactly the drift class this project burns sessions on. Don't lose BC — load-bearing for deep-lore (Doom ≈ -114 BC, Long Night ≈ -8000 BC).
4. **State that `precision: relative-only` is the handshake to the deferred `PRECEDES`/`FOLLOWS` edges.** Events with no absolute year get ordered by temporal edges, not `ac_year`. Say so in the schema doc so node-time and edge-ordering interlock instead of competing.

## 4. CONCURRENCY — read before writing node files
- I committed `## Quotes` (body) changes to 25 nodes in `3c3cbd55d`. **Two are event nodes you'll likely touch:** `graph/nodes/events/siege-of-riverrun.node.md` and `graph/nodes/events/melee-at-bitterbridge.node.md`. **Pull `main` first.**
- **Patch frontmatter only, idempotently** (re-read each file immediately before writing; don't full-file-rewrite from a stale buffer). Frontmatter (`occurred:`) and body (`## Quotes`) don't overlap, so region-scoped patches by the two tracks are safe. A naive whole-file rewrite by either of us clobbers the other. My `apply-node-quotes.py` is already body-only/idempotent for this reason — mirror that discipline for frontmatter.

## 5. Sequencing suggestion
Backfill `occurred:` onto **the historical-anchor hubs first** (§1 list): they're dated, now well-connected, and `chronology-events.jsonl` (2,245 rows, already carries `year_value`+`year_era`) is the deterministic source — so "who fought at the Trident **and when**" becomes answerable from one node. This naturally folds in two open items: the year-page mistype bug (10 AWOIAF year pages sitting in `graph/nodes/characters/` as `character.human`) and the deferred `event.year` / chronology-dir type decision (architecture.md TYPE_DIR_MAP).

## 6. Paths you'll want
- `graph/edges/edges.jsonl` — the role edges (carry `evidence_book`/`evidence_chapter` = narrative time, NOT event time).
- `working/wiki/data/chronology-events.jsonl` — deterministic year source (`year_value` + `year_era`).
- `working/wiki/data/edges-temporal-scoped.jsonl` — existing S76 narrative-time edge layer.
- `reference/architecture.md` — frontmatter conventions (note: `era:` is already documented as "forward-only, not backfilled retroactively" — reconcile your block with that line or amend it).
- `scripts/apply-node-quotes.py` — reference pattern for idempotent, region-scoped node writes.
