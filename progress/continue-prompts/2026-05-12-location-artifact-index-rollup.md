# Continue: Per-LOCATION + per-ARTIFACT index roll-ups

**Created:** 2026-05-12 (end of Session 42)
**Track:** Track 3 of three parallel-runnable tracks (Track 1 done Session 42; Track 2 has its own continue prompt)
**Status:** Ready
**Estimated effort:** One session, pure Python, $0
**Recommended model:** **Sonnet 4.6** (`claude-sonnet-4-6`) or **Haiku 4.5** (`claude-haiku-4-5-20251001`). Pure Python — the LLM parameterizes one reference script, runs it, smoke-tests outputs. No agent reasoning. Per `feedback_model_selection_at_session_start.md`, default to cheapest viable; Opus is wasteful here. Sonnet preferred for the design-decision moments (one-script-vs-many, section-aware-vs-flat); Haiku fine if those decisions are pre-made.
**Memory rules in play:** `feedback_python_before_agent.md`, `feedback_check_existing_knowledge_first.md`, `feedback_model_selection_at_session_start.md`

---

## What this work is

Extend the per-character-index pattern from Session 41 to locations and artifacts (and possibly houses). Same script structure, different node-type filter. Closes "what does the graph know about Winterfell / about the Iron Throne?" in O(1) lookup.

This is **Stage 4 component (b) — chapter-evidence backfill** prerequisite for non-character node types. Characters already have it (`graph/index/characters/` from Session 41).

## Read first

- `scripts/build-character-indexes.py` — the reference implementation. Read it end-to-end before starting; understand:
  - How it walks `graph/nodes/characters/*.node.md` and parses frontmatter
  - How it joins against `graph/index/chapters/{book}/*.mentions.json` to build inverse maps
  - How it reads each node's `## Edges` section for `out_edge_count`
  - How it looks up `working/wiki/data/backlink-counts.json` for `in_edge_count`
  - How it handles POV resolution (this is character-specific and likely not needed for locations/artifacts)
- `graph/index/characters/_summary.json` — confirm the output schema you're matching.
- `worklog.md` Session 41 entry — design rationale + the prefix-disambiguation tiebreaker (probably not needed for locations/artifacts since they don't have name-collision problems like Pate vs pate-tully).

## Decisions to make before acting

### 1. One script or several?

- **Option A (LEAN)** — Parameterize `build-character-indexes.py` into `scripts/build-entity-indexes.py --type <type-prefix>` that handles characters, locations, artifacts, houses, etc. POV resolution is `--type character.*`-gated inside the script.
- **Option B** — Write `build-location-indexes.py`, `build-artifact-indexes.py`, etc. as type-specific clones.

Lean Option A if the locations/artifacts logic is ≥80% same as characters. The schema is roughly: `appearances_total`, `chapters_referenced_in`, `out_edge_count`, `in_edge_count`. Type-specific extras (POV for characters; "wielded by" for artifacts) can be optional fields.

### 2. Which node types?

Tier 1 (do):
- `place.*` → `graph/index/locations/`
- `object.artifact` (and `artifact.weapon`, `artifact.armor`) → `graph/index/artifacts/`

Tier 2 (probably yes):
- `organization.house` → `graph/index/houses/` (high-traffic; "show me everything about House Frey")

Tier 3 (probably defer):
- `organization.faction`, `organization.religion`, `event.*`, `title`, `species`, `concept.*` — lower traffic; can add later.

Lean: do tier 1 + tier 2, defer tier 3.

### 3. Semantic model for non-character nodes

Characters have:
- `chapters.pov` (where they narrate)
- `chapters.mentioned_in` (where they're referenced)

Locations have:
- Appearance in chapter `## Locations` section
- Appearance in chapter `## Raw Entity List` 12 categories

Two options:
- **(a) Single field** `chapters.referenced_in` — flat list of all chapter mentions.
- **(b) Two fields** `chapters.in_locations_section` (Pass-1 Locations) + `chapters.in_raw_list` (Raw Entity List hits) — preserves the section distinction; useful for "is this a primary or incidental setting?"

Lean: **(b)**, but the field naming should reflect node-type. For artifacts: `chapters.in_artifacts_section` + `chapters.in_raw_list`. For houses: `chapters.in_raw_list` only (Pass 1 doesn't have a houses-specific section).

### 4. `out_edge_count` for non-character nodes

Same logic — count `- EDGE_TYPE: target` lines in the `## Edges` block. Edge counts will be different shapes (locations have RULED_BY, HOUSE_OF, NEAR; artifacts have WIELDED_BY, FORGED_BY) but the counting is identical.

## Pieces to reuse

| Resource | Path | Notes |
|---|---|---|
| Reference implementation | `scripts/build-character-indexes.py` | Copy and parameterize. |
| Mention index | `graph/index/chapters/{book}/*.mentions.json` | Per-chapter mentions tagged with section + node-type — already includes locations + artifacts. |
| Backlink counts | `working/wiki/data/backlink-counts.json` | Per-slug wiki backlink count for `in_edge_count` baseline. Works for all node types. |
| Pass-1 extractions | `extractions/mechanical/{book}/{book}-{slug}-NN.extraction.md` | Source for chapter→entity mentions. The mention-index already digests these. |

## Smoke-test slugs (verify after build)

Locations:
- `winterfell` — should appear in 100+ chapter records; primary setting for AGOT Bran/Catelyn/Sansa/Arya.
- `kings-landing` — densest location in the graph (every book has chapters here).
- `the-wall` — Jon's primary setting; should show high mention count.
- `meereen` — should show heavy ADWD Daenerys/Barristan/Quentyn presence.
- `oldtown` — AFFC prologue + Sam's later chapters.

Artifacts:
- `iron-throne` — should appear in dozens of Eddard/Tyrion/Cersei chapters.
- `heartsbane` — should appear in Sam chapters (AFFC prologue, ADWD).
- `lightbringer` — Stannis/Melisandre chapters.
- `longclaw` — Jon chapters.
- `oathkeeper` — Brienne/Jaime chapters.

Houses:
- `house-stark`, `house-lannister`, `house-targaryen` — should each have hundreds of mentions.
- `house-frey` — high count, all books.
- `house-mormont` — moderate.

**Smoke-test post-action:** Spot-check 5 location indexes and 5 artifact indexes. Confirm chapter counts make sense (high-traffic = 100s of mentions; obscure = a handful).

## Expected delta

- ~7,000 new index files across `graph/index/{locations,artifacts,houses}/`.
- Each file ~1-3 KB depending on mention density.
- Stage 4 component (b) — chapter-evidence backfill — is unblocked for these node types.

## What this unblocks downstream

- **Stage 4 prose-edge-classifier** can now ground its edge classifications in per-entity chapter context for all primary node types, not just characters.
- **Agent retrieval queries** like "what does the graph know about Riverrun?" or "show me all artifacts that appear in ADWD" can be answered O(1) via the index instead of scanning all 7,583 nodes.
- **Convergence maps** (graph/convergence-maps/) — when those get built, the per-location index is the natural data source for "all characters who pass through Oldtown."

## DO NOT

- Touch existing `graph/index/characters/` — already correct (Session 41).
- Touch Pass 1 extractions in `extractions/mechanical/`.
- Try to canonicalize aliases at this layer — that's mention-index's job (already done).
- Add type-specific logic that doesn't generalize cleanly (e.g., don't parse `## Aftermath` looking for casualty counts in event indexes — that's a separate enrichment pass).
- Auto-run `/endsession`.

## After this lands

- Mark new todo in `working/todos.md` as `[x] DONE` (todo doesn't exist yet — file it when work begins).
- Stage 4 component (b) prerequisite is fully met for primary node types.
- Add Session entry to worklog.
- Consider: do the tier-3 node types (factions, religions, events, titles, species, concepts) merit their own index roll-ups? File as a follow-up todo only if Stage 4 hits a wall without them.
