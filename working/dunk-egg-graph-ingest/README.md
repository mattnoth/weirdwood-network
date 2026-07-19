# D&E graph-ingest track

Deterministic ingest pipeline for the 24 Dunk & Egg Pass-1 extraction files
(`thk-dunk-01-p01..07`, `tss-dunk-01-p01..08`, `tmk-dunk-01-p01..09`) into
graph edge candidates.

## Script contract

`scripts/dunk-egg-graph-ingest.py`

- **Input:** `extractions/mechanical/{thk,tss,tmk}/*.extraction.md` — parses
  only the `## Relationships Observed` table in each part file.
- **Grounds** evidence quotes against the whole-novella source files
  (`sources/chapters/{book}/{book}-dunk-01.md`), never the `-pNN` part files.
- **Resolves** character names to existing `graph/nodes/**/*.node.md` slugs
  via `scripts/stage4_name_resolver.py`'s five-rung ladder, seeded by
  `curated-map.csv` (exact-name anchors, checked before the resolver ladder)
  and a fallback honorific-stripped retry (`Ser `/`Lord `/`Lady `/`King `/
  `Prince `/`Maester `).
- **Never writes to `graph/`.** All outputs land in `out/`. This is a
  dry-run candidate builder — an orchestrator (human or agent) reviews
  `out/STATS.md` + the JSONL files before anything is minted into the graph.

## Files in this directory

- `curated-map.csv` — hand-seeded name -> slug anchors (columns: `name,slug`;
  `slug=SKIP` drops a name from resolution entirely). Edit this file to add
  more anchors; it is read fresh on every run via `--map`.
- `out/emit.jsonl` — ready candidate edges (schema matches the live
  `pass1_relationship` rows in `graph/edges/edges.jsonl`).
- `out/alias-adds.jsonl` — `{slug, alias, source_row}` — surface forms found
  via `SAME_AS`/`ALIAS_OF` rows that resolve to an existing node but are
  missing from that node's `aliases:` frontmatter list.
- `out/identity-flags.jsonl` — `SAME_AS`/`ALIAS_OF` rows where the two sides
  resolved to different slugs, or one/both sides didn't resolve. Needs a
  human/orchestrator adjudication pass. **`SAME_AS` edges are never minted.**
- `out/overlay-candidates.jsonl` — rows that ground and resolve cleanly but
  whose `(source_slug, edge_type, target_slug)` triple already exists in
  live `graph/edges/edges.jsonl` — book-evidence overlay opportunities on
  wiki-sourced edges (a later step, not part of this run).
- `out/quarantine.jsonl` — rows dropped with a `reason` (ungrounded,
  unresolved, self-edge, malformed cell, missing required qualifier, etc).
- `out/needs-map.csv` — census of names that failed to resolve even after
  the curated map + resolver + honorific fallback, for curated-map growth.
- `out/STATS.md` — full run stats, per-book breakdown, quarantine-reason
  histogram, and the exact commands run.

## Re-running

```
python3 scripts/dunk-egg-graph-ingest.py --map working/dunk-egg-graph-ingest/curated-map.csv --out-dir working/dunk-egg-graph-ingest/out
```

Idempotent — overwrites `out/` cleanly. Stdlib-only, no network, no LLM calls.

## Follow-up subcommands (added S222, after the repass verdicts)

- `repass-verdicts-s222.jsonl` — one object per verified risky row from an
  exhaustive verifier pass: `{source_slug, edge_type, target_slug, verdict:
  CONFIRM|REJECT|FIX, reason, fix_source_slug?, fix_target_slug?}`. Verdicts
  match `out/emit.jsonl` rows by their **original** `(source_slug, edge_type,
  target_slug)` triple.

- `--assemble-final` — reads `out/emit.jsonl` + `repass-verdicts-s222.jsonl`
  + `out/alias-adds.jsonl`, applies REJECT (drop) / FIX (rewrite endpoint(s),
  tag `*_resolution_status: "repass-fixed"`), re-dedups any triples FIX makes
  collide (keeps first row, bumps `dup_count`), and splits out anything that
  now matches live `graph/edges/edges.jsonl` into `out/final-overlay.jsonl`
  instead of emitting it. Alias adds go through an explicit reject-list +
  already-on-node + graph-wide name/alias collision guard. Writes
  `out/final-edges.jsonl`, `out/final-overlay.jsonl`, `out/final-aliases.jsonl`,
  `out/FINAL-STATS.md`. Still dry-run — writes only under `working/`.

  ```
  python3 scripts/dunk-egg-graph-ingest.py --assemble-final
  ```

- `--apply` — **mutates `graph/`.** Backs up `graph/edges/edges.jsonl` to
  `graph/edges/edges.jsonl.bak-s222-dunk-egg`, appends `out/final-edges.jsonl`,
  and inserts each `out/final-aliases.jsonl` entry into its node's `aliases:`
  frontmatter (idempotent, preserves the double-quoted JSON-array style).
  Refuses to run twice (aborts if `run_id: "dunk-egg-pass1-derived-s222"` is
  already present in `edges.jsonl`). **Orchestrator-gated — run only on
  explicit go-ahead**, per project policy (no graph mutation without an
  explicit approved dry-run review first).

  ```
  python3 scripts/dunk-egg-graph-ingest.py --apply
  ```
