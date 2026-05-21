# Stage 4 Candidate Enrichment — Design (Session 63, 2026-05-21)

> **Principle:** Make it as easy as possible for Haiku to find ONLY the things relevant to this candidate.
>
> Every candidate row should be a complete, self-contained decision unit. Haiku reads the row, looks at the evidence in the row, picks an `edge_type` or rejects. NO file reads. NO scanning. NO recovering context Python could have pre-computed.

## Why this matters

Per-call Haiku work today (per the classify prompt's Step 2):
1. Read the candidate file (small)
2. Read the source node's **full markdown** (~500-2000 lines of prose)
3. For each candidate row, read the **target's frontmatter** (~20 lines × N candidates ≈ 30 file reads per chunk)
4. Reason about each candidate

Steps 2-3 are file I/O and context-loading the model is paying for. The reasoning itself is fast. We're using Haiku as a file-system reader-and-reasoner when it should be a *constrained chooser* picking from a pre-filtered menu.

## The candidate row, post-enrichment

Each row contains everything Haiku needs to decide:

| Field | Source | Purpose |
|---|---|---|
| `source_slug`, `target_slug`, `anchor_text`, `source_section` | Original candidate builder | Identity (kept) |
| `target_type` | `build_node_type_index(graph/nodes/)` | Type-contract check inline (no frontmatter read) |
| `evidence_paragraph` | Source node's `.node.md`, paragraph containing the anchor, cleaned of cite_ref noise | Full relevant prose context (no source-node read) |
| `valid_edge_types` | TYPE_CONTRACTS table pre-filtered by `target_type` | Haiku picks from a ~10-30 menu, not the 163-type vocab |
| `staging_verbs_present` | Regex-scan of `evidence_paragraph` for ENCOUNTERS verb whitelist | Pre-computed verb-gate hint (Haiku confirms, doesn't search) |

## What Haiku is asked to do, post-enrichment

For each row:

1. Read the `evidence_paragraph`.
2. If the prose establishes a relationship between source and target → emit_edge with an `edge_type` from `valid_edge_types`.
3. Otherwise → `reject_just_mention` with a reason.
4. If the source/target identity is unclear → `escalate_*`.

That's it. No file reads. No type-contract validation against a 22-row table. No mental filter of 163 vocab types. No verb-gate hunt across 13 whitelisted phrases.

## What gets removed from the classify prompt

After enrichment, these prompt sections become unnecessary or dramatically smaller:

- **TYPE CONTRACTS table (22 rows)** → not needed; each row's `valid_edge_types` is the per-row contract
- **LOCKED EDGE VOCABULARY (163 entries with full descriptions)** → keep slimmed (name + 1-line summary); full descriptions move to a reference Haiku only opens if it can't decide
- **Rule 6 ENCOUNTERS verb-gate whitelist** → row's `staging_verbs_present` is the hint; rule shrinks to "if list is empty, reject"
- **Step 2 instructions to "read source node prose" and "read target frontmatter"** → deleted

Estimated prompt reduction: ~700 lines → ~150 lines.

## What this is NOT

- **NOT pre-classification of edge types in Python (F4 deferred).** Python flags possibilities and hints; the semantic decision stays with Haiku. We don't compete with the model on the task we want it to do.
- **NOT pre-rejection of soft candidates (F6 deferred).** Python doesn't decide "this is a dream-context reject." It can flag "evidence_paragraph contains the word 'nightmare'" — Haiku decides what that means. Avoid laundering semantic errors through Python.

## Implementation plan

1. **`scripts/wiki-pass2-enrich-candidates.py`** — one script does F1+F2+F3+F5+F7 in one pass over `working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/*.candidates.jsonl`. Writes to `prose-edge-candidates-enriched/` (preserves originals). Idempotent.
2. **Update `.claude/commands/stage4-haiku-classify.md`** — drop file-read instructions; reference enriched fields; collapse type-contracts + vocab sections.
3. **Update `scripts/stage4-haiku-run.py`** — read from `prose-edge-candidates-enriched/` when present.
4. **Smoke test on `batch-0019`** — compare validator violation rate + per-chunk wall-clock to overnight chunk=3 baseline.
5. **If smoke clean → relaunch** with enriched candidates + LEVER 1 (`SLEEP_BETWEEN=10`) + chunk_size=5 (worth re-testing now that per-call work is smaller).

## Open questions for Matt

- **F5 (prompt shrink) full or partial?** Slim vocab to name+1-line summaries inline (full descriptions in a referenced file) — or just delete the descriptions entirely and rely on Haiku's training? Risk: descriptions disambiguate edge-type intent for borderline cases. Lean: keep 1-line summaries; the per-row `valid_edge_types` filters most ambiguity.
- **Comention candidates** — these have a different schema (`pair_a` / `pair_b`, evidence_paragraphs list). Enrich them same-day or defer until source_target proves the pattern?
- **Pass1_relationship candidates** — already self-contained (carry `evidence_quote` + `asserted_relation`). May not need enrichment. Verify.
