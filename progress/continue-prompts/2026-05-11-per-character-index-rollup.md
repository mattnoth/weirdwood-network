# Continue: Per-character index roll-up (Stage 4 component b prep)

**Created:** 2026-05-11 (end of Session 40)
**Track:** Graph retrieval infrastructure (cheap-Python, $0)
**Status:** Ready to start — no prerequisites unresolved
**Estimated effort:** 30-60 minutes, pure Python

---

## What this work is

Build per-character index files at `graph/index/characters/<slug>.index.json` — one file per character node. Each file is the **reverse** of the existing per-chapter mention-index. It answers "what does the graph know about character X?" without requiring an agent to scan 344 chapter-mention files or all the wiki nodes.

This is the cheap-Python foundation under Stage 4 component (b) — chapter-evidence backfill (see `working/todos.md` Stage 4 richest-form entry + memory `project_stage4_richest_form.md`).

## Why it's the right next step

- **No LLM, no cost.** Pure Python file walking + JSON emission.
- **Unblocks Stage 4 component (b)** — when the chapter-evidence backfill ever runs, the agent has a pre-computed per-character file pointing at the relevant chapters instead of having to derive them.
- **Improves agent retrieval today.** Any agent reading the graph can answer "what does the graph say about Eddard?" by reading one file (per-character index) plus one file (the node) instead of node + 344 chapter scans.
- **Was specced in Session 38's continue prompt** — Matt validated the design then but deferred execution.

## Existing material to consume

| Source | Path | What it provides |
|---|---|---|
| Per-chapter mention-index | `graph/index/chapters/{book}/{chapter}.mentions.json` (344 files) | "Chapter → entities mentioned in it." Inverse of what we're building. |
| Pass 1 extractions | `extractions/mechanical/{book}/{book}-{pov}-NN.extraction.md` (344 files) | `pov_character` field in frontmatter — drives "is X the POV of this chapter?" |
| Graph nodes | `graph/nodes/characters/<slug>.node.md` (4,084 character nodes) | Source of truth for the character itself; emit one index per node |
| Cross-references | `working/wiki/data/cross-references.jsonl` | Wiki-page → wiki-page link counts. Optional: derive in/out edge counts. |
| Backlink counts | `working/wiki/data/backlink-counts.json` | Pre-computed in-degree per slug. Drop-in. |

## Output schema (proposed)

```json
{
  "slug": "eddard-stark",
  "name": "Eddard Stark",
  "type": "character.human",
  "node_path": "graph/nodes/characters/eddard-stark.node.md",
  "generated_at": "2026-05-11T...",
  "stats": {
    "appearances_total": 87,
    "chapters_present": 47,
    "chapters_pov": 15,
    "in_edge_count": 312,
    "out_edge_count": 28
  },
  "chapters": {
    "pov": [
      {"chapter_id": "agot-eddard-01", "book": "agot"},
      {"chapter_id": "agot-eddard-02", "book": "agot"},
      ...
    ],
    "mentioned_in": [
      {
        "chapter_id": "agot-bran-01",
        "book": "agot",
        "pov": "bran",
        "mention_count": 3,
        "resolved_via": "direct"
      },
      ...
    ]
  }
}
```

Output location: `graph/index/characters/<slug>.index.json` (one file per character node).

Also emit a `graph/index/characters/_summary.json` rollup with total counts (paralleling `_summary.json` in `graph/index/chapters/`).

## Implementation sketch

Script: `scripts/build-character-indexes.py` (new). Pattern after `scripts/build-mention-index.py` (already written, good reference for slug handling + frontmatter parsing).

1. Walk all character nodes in `graph/nodes/characters/` and `graph/nodes/_unclassified/` (filter by `type:` prefix `character.`).
2. For each character:
   a. Read frontmatter (name, type, slug, aliases).
   b. Inverse-lookup mention-index: walk all 344 `*.mentions.json` files, find entries where `slug` matches.
   c. Inverse-lookup Pass 1 POV: walk all 344 `*.extraction.md` files, check the `pov_character` field.
   d. Read node's `## Edges` section for out-edge count. Use `backlink-counts.json` for in-edge count.
   e. Emit `<slug>.index.json`.
3. Emit `_summary.json` rollup.

CLI: `--character <slug>` for single-char testing; `--all` for full corpus; `--dry-run` for verification.

Idempotent (overwrite in place). Should take seconds, not minutes — same scale as the mention-index build (which did 344 files in ~6s).

## Things to decide before starting

1. **Scope to character.human only, or include dragons + direwolves?** Lean: include all `character.*` types since they're all narrative agents per `reference/architecture.md`.
2. **Where does the in_edge_count come from?** Two paths: (a) re-derive from `cross-references.jsonl` (Wiki-link backlinks), (b) use the existing `backlink-counts.json`. Lean: (b). It's already computed.
3. **Should mention `chapters_mentioned_in` include chapters where the character is the POV?** Lean: separate "pov" list from "mentioned_in" list (don't double-count). Pass 1 POVs only count under "pov".
4. **Alias-aware resolution?** Pass 1's raw "Ned Stark" already resolves to `eddard-stark` via the mention-index's alias step (verified post-Session-40 backfill). The character index inherits that — no extra alias work needed.

## What NOT to do

- Don't bundle dialogue/voice extraction — that was deferred entirely (memory: `project_real_goal_graph_for_agents.md` and the dialogue-meals continue prompt is archived).
- Don't try to compute `first_available` — deferred (`project_first_available_deferred.md`).
- Don't generate per-LOCATION or per-ARTIFACT index files yet — characters first. Other types are a follow-on if this proves useful.
- Don't write LLM code paths. This is pure Python. If it grows tendrils into "agent decides," that's Stage 4 component (b), not this work.

## Smoke test

After build:
```bash
cat graph/index/characters/eddard-stark.index.json | python3 -m json.tool | head -50
```

Expect to see: ~15 POV chapters, ~30-50 chapters mentioned in (back-of-envelope from his appearance pattern), in_edge_count in the few-hundreds range, out_edge_count in the dozens.

Spot-check 3 characters of different prominence: `eddard-stark` (high-traffic POV), `tormund` (supporting character, no POV), `gilly` (minor named character). Numbers should look plausible.

## Connection to alias-backfill (Session 40 commit `ace00ee0`)

The mention-index this work consumes was last regenerated in Session 40 with the 6-alias backfill. Resolution is currently 70.6%. The 30% unresolved are not parser bugs — they're either ambiguous slugs (multiple "Aegon"s, multiple "joffrey"s) or genuine missing graph nodes (most regions like `the-narrow-sea`, `flea-bottom`). The character index inherits these limitations — if a character is sometimes referred to ambiguously in Pass 1 (e.g. "Aegon" without distinguishing which one), their per-character index will under-count those chapters. That's a real Stage 4 problem (`disambiguation-resolver`), not a per-character-index problem.

## DO NOT

- DO NOT auto-run `/endsession` after completing this work (memory: `feedback_endsession_requires_permission.md`).
- DO NOT modify `graph/nodes/` files — this work only emits indexes, never touches source-of-truth nodes.
- DO NOT delete the mention-index files — the per-character index is additive, not a replacement.
- DO NOT generate per-character indexes for non-character entity types in this run.
