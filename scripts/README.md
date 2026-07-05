# scripts/ — Weirwood Network Script Inventory

**Refreshed:** 2026-06-15 (Session 2 — script consolidation)
**Rule:** This file is the **universal index** for every script — the existence-truth.
A script is "organized" when it has a row here (class · purpose · provenance · how-to-run),
not when it has an alias. Every script gets a row, even a one-shot that will be archived tomorrow.

---

## Class taxonomy (design §1.5 — `working/orchestration-pacer-design-2026-06-15.md`)

| Class | Kind | How it runs | Aliased as | Lifecycle |
|-------|------|-------------|------------|-----------|
| **A** | Long-run job (rate-limited, multi-window, LLM-driven) **or** the orchestration infra itself (supervisor / pacer / worker template / front door) | `weirwood run` → `longrun.sh` → worker → `pace.py` | `weirwood run start <track>` / `custom` | the orchestration in design §3–§9 |
| **B** | One-shot mutation (deterministic; mutates graph/data once) | direct — never longrun-wrapped | usually direct; documented here | backup → dry-run → apply → validate; **archive to `scripts/archive/` when spent** |
| **C** | Standing tool (on-demand; read-only or build-an-artifact) | on demand | `weirwood <tool>` (e.g. `weirwood graph`) | LIVE forever; never archived |
| **D** | Resolver / library (builds a derived artifact + queried/imported) | `--build` regenerates; `--lookup`/import queries | `weirwood refresh` (rebuild all derived artifacts) | LIVE forever; **rebuild after any node-adding/renaming mutation**; never archived |

**Provenance (`Added`)** = the git add-date. Map to a session via the worklog archive map
(`worklog.md` → Archive map: e.g. 2026-04-22 ≈ S0–4, 2026-04-30 ≈ S22–29, 2026-05-18–27 ≈ S49–77,
2026-06-05–08 ≈ S82–87, 2026-06-10–14 ≈ S89–96, 2026-06-15 = S97–99).

### New-script checklist (so future scripts are BORN organized — design §11.5)
When ANY script is created (by Matt or an agent):
1. Name it `<area>-<verb>` (avoid `temp-` / `test-` / `-v2` in committed names — those signal "should already be archived").
2. Decide its class (A/B/C/D).
3. Add its row here (class · purpose · provenance · how-to-run).
4. Wire an alias ONLY if class A (track) or C/D (repeat-use tool).
5. If it is a class-B mutation that **adds or renames nodes**, call `weirwood refresh` (or the builders directly) as its final step.

---

## Legend (status)

| Status | Meaning |
|--------|---------|
| `LIVE` | Actively used; do not archive |
| `LIVE (run complete; kept)` | One-shot already run; kept for rerun/recall by project decision |
| `LEGACY-migrate-to-longrun` | Run-forever wrapper superseded by `longrun.sh`; migrate when its track reopens — do NOT touch while a live run is in progress |
| `SUPERSEDED-by-pass1-derived` | Wiki-comention scripts (27); KEPT as revival-recall lever (S73 decision) — do NOT archive |
| `SUPERSEDED-by-X` | Replaced by a named successor |
| `ARCHIVED 2026-06-15` | Moved to `scripts/archive/` in the Session-2 consolidation (history preserved via `git mv`) |

**Summary (live `scripts/` + `scripts/archive/`):**
124 live scripts · 32 archived (2 original + 30 moved 2026-06-15). The wiki-comention scripts stay LIVE-in-place (KEPT, S73).

> **Session-2 archival (2026-06-15):** 24 early Stage-4 `classify-*`/`temp-*` iteration scripts + 2 smoke scripts
> (`stage4-haiku-smoke-prep.py`, `stage4-haiku-smoke-cleanup.py`) + `migrate-stats-csv.py` (de-referenced from
> `extract.sh` first) + 4 shelved run-forever wrappers (`stage4-haiku-run-forever.sh`, `stage4-tail-bulk-forever.sh`,
> `stage4-events-bulk-run.sh`, `stage4-haiku-loop.sh`) → `scripts/archive/`. Frozen Pass-1/Pass-2 stats CSVs →
> `working/extraction-stats/_archive/` (readers fall back there). **KEPT in place:** `stage4-run-forever.sh`
> (proven reference) + `edge-reify-run-forever.sh` (registry PLANNED/live) + the 27 comention scripts.

---

## Orchestration / Pacer (the supervisor / worker / pacer / front-door — design §2–§9)

| Class | Script | What it does | Added | How to run |
|-------|--------|--------------|-------|------------|
| A | `longrun.sh` | **Generic long-run supervisor.** Relaunches any worker on rate-limit walls (exit 2) and crashes; exits on success (0); iterates on exit 10. Standardized env vars + logging. | 2026-06-12 | via `weirwood run` (not usually called directly) |
| A | `weirwood-run.sh` | Declarative long-run track **registry** wrapping `longrun.sh`; per-track log + latest-symlink + pidfile. `list`/`start`/`logs`/`status`/`stop`. | 2026-06-12 | `weirwood run <subcommand>` |
| A | `weirwood.zsh` | **Front-door CLI** — `weirwood` shell function. Dispatches extraction, `wiki`, `stage4`, `run`, `graph`, `resolve`, `refresh`. | 2026-04-25 | source in `.zshrc`; `weirwood --help` |
| A | `pace.py` | **Pacer** (v1 report-only). `backfill` normalizes 6 heterogeneous stat schemas → per-track `working/telemetry/<track>.jsonl`; `report` prints per-`(track,model,unit_type)` baselines + a conservative `LONGRUN_SLEEP_BETWEEN`. `emit_telemetry_row()` is the importable worker helper. No ETA/headroom in v1 (wall data thin — design §13 M3). | 2026-06-15 | `python3 scripts/pace.py backfill` · `... report` |
| A | `worker-template.py` | **Copy-me reference worker** implementing the §4 contract + §13 M1/M2/M4: positive-wall `exit(2)` only + `next-eligible`, atomic `os.replace` + `O_EXCL` claim, one telemetry row/unit, single-worker-durable. | 2026-06-15 | copy → `weirwood run start custom -- python3 scripts/<task>.py --resume` |

---

## QUERY — the query surface lives at `graph/query/` (query-layer Track, step 1)

The consolidated Python query engine is the package **`graph/query/weirwood_query/`**
(modules: model / load / normalize / resolve / traverse / report / cli) plus the
alias-table builder **`graph/query/build/build_alias_table.py`**. Front door:
**`weirwood query <args>`** (= `PYTHONPATH=graph/query python3 -m weirwood_query.cli`).
Contract + parity cases: `graph/query/spec/`.

The compat shims are RETIRED (S191, shim-retirement Tier B): `scripts/graph-query.py`,
`scripts/event_alias_resolver.py`, and `scripts/build-chat-export.py` are deleted. Every
consumer now imports/invokes `graph/query/` directly — tests import the package, the
netlify.toml build command runs the `graph/query/build/` builders, and the `weirwood
graph` / `weirwood resolve` shell aliases forward to the engine (permanent short
aliases). `scripts/weirwood-refresh.sh` step 3 calls
`graph/query/build/build_alias_table.py --build` directly.

---

## Standing Tools — `weirwood` CLI aliases (class C/D)

| Class | Script | What it does | Added | How to run |
|-------|--------|--------------|-------|------------|
| C | *(retired S191: `graph-query.py`)* | Read-only graph inspection now lives in `graph/query/weirwood_query/` (see QUERY section): node header, edges, neighbors, path, health, participants, chain/full-chain, expand-beats, container. | 2026-04-30 | `weirwood query <args>` · `weirwood graph <args>` (legacy alias, same engine) |
| D | `mint_arc_lib.py` | Importable mint-script helper: `precheck_slugs(slugs)` validates edge endpoints resolve (node-file existence OR alias-resolver) BEFORE edges land — the `daznak-s-pit` vs `daznaks-pit` floor-check. CLI: `python mint_arc_lib.py <slug>…`. | 2026-06-21 | imported by mint scripts |
| C | `stamp_containers.py` | Idempotent `containers:` frontmatter stamper: `python stamp_containers.py [--dry-run] <name> <slug>…` adds a container tag (merge-safe, never `[]`). For the container-membership rollout. | 2026-06-21 | `python scripts/stamp_containers.py …` |
| D | *(retired S191: `event_alias_resolver.py`)* | Alias resolution now lives in `graph/query/` — lookups via `weirwood_query.resolve`, table builds via `graph/query/build/build_alias_table.py` (`working/wiki/data/event-alias-lookup.json`). **LIVE infrastructure — never archive the builder.** | 2026-06-10 | `weirwood query resolve "<phrase>"` · `weirwood resolve <args>` (legacy alias; rebuilt by `weirwood refresh`) |
| D | `stage4_name_resolver.py` | Importable 5-rung collision-aware name resolver (exact/alias/firstname-unique/context-present/context-prior). **LIVE library — never archive.** | 2026-05-23 | imported by Stage 4 scripts |
| C/D | `weirwood-refresh.sh` | Rebuilds ALL derived artifacts in one command (17 entity-index types + character indexes + alias resolver) — the standard post-node-mutation step. `--check` WARNs if artifacts are stale vs `graph/nodes/`. | 2026-06-15 | `weirwood refresh` · `weirwood refresh --check` |

---

## Chapter / Source Processing

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| C | `chapter-splitter.py` | Splits ASOIAF .txt source files into per-chapter markdown with YAML frontmatter | 2026-04-22 | LIVE |
| C | `dunk-egg-splitter.py` | Splits Dunk & Egg Calibre plaintext into 3 novella markdown files | 2026-04-22 | LIVE |

---

## Extraction Pipeline (Pass 1) — class A machinery + status tools

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| A | `extract.sh` | Unified Pass-1 entry point: run/status/launch; wrapped by the `weirwood` function | 2026-04-25 | LIVE |
| A | `run-extraction-wave.sh` | Runs Pass 1 on one wave of 5 chapters in a single terminal | 2026-04-23 | LIVE |
| A | `run-extraction-all.sh` | Runs Pass 1 across a book with N parallel workers + skip-existing resume | 2026-04-23 | LIVE |
| A | `launch-extraction.sh` | Opens iTerm2 tabs and runs extraction waves in parallel | 2026-04-23 | LIVE |
| A | `claim-chapter.py` | Atomically claims a chapter for extraction against the stats CSV (race-safe via lockdir) | 2026-05-04 | LIVE |
| A | `extract-status-sweep.py` | Sweeps stale started/working CSV rows and rewrites them as failed-stale | 2026-05-04 | LIVE |
| A | `stream-claude-output.py` | Streams Claude assistant output to stderr with │ prefix during extraction | 2026-05-04 | LIVE |
| C | `extraction-status.sh` | Shows per-book extraction progress and next steps (read-only) | 2026-04-23 | LIVE |

> `migrate-stats-csv.py` (one-time 13→16-col CSV migration) was **de-referenced from `extract.sh` and ARCHIVED 2026-06-15** — see archive section. Pass 1 is frozen 344/344; fresh CSVs are written with the 16-col header directly.

---

## Wiki Pipeline — Parser / Infobox / Crawl-era

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| C | `wiki-infobox-parser.py` | Parses all 17,657 cached wiki JSON → `infobox-data.jsonl` + `page-index.jsonl` + `parse-stats.md` | 2026-04-30 | LIVE |
| C | `wiki-fetch-categories.py` | Bounded MediaWiki categories backfill (approved exception fetch 2026-04-30) → `page-categories.jsonl` | 2026-04-30 | LIVE (run complete; kept) |
| A | `wiki-pass2.sh` | Wiki Pass 2 launcher: triage/run/launch/status/check/reset/unstick/questions/stop | 2026-04-30 | LIVE |
| C | `wiki-pass2-triage.py` | Triages 17,657 wiki pages into per-bucket manifests (Stage 1 + Stage 2 grouping) | 2026-04-30 | LIVE |
| C | `wiki-pass2-prioritize.py` | Computes `priority_tier` A/B/C for every page in secondary-tier manifests | 2026-04-30 | LIVE |

---

## Wiki Pipeline — Pass 2 Promotion Stages (class B one-shot mutations; kept for rerun)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| B | `wiki-pass2-emit-deterministic.py` | Stage 3a: emits deterministic skeleton node files from manifest + infobox data | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-extract-prose.py` | Stage 3b: extracts prose body from cached wiki HTML into per-page prose files | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-promote.py` | Stage 3 promotion: concatenates skeleton + prose → atomic rename into `graph/nodes/` | 2026-04-30 | LIVE (run complete; kept) |
| C | `wiki-pass2-validator.py` | Gate validator: validates `tmp/` node files before promotion | 2026-04-30 | LIVE |
| C | `wiki-pass2-coherence.py` | Cross-bucket coherence check: edge targets exist, allegiance resolves, no dup names | 2026-04-30 | LIVE |
| B | `wiki-pass2-attach-prose.py` | Attaches prose to stub-only deterministic nodes lacking prose sections | 2026-05-11 | LIVE (dual use) |
| B | `wiki-pass2-repromote-targeted.py` | Targeted re-promotion for 14 parser-bug nodes (mistyped + religion-bleed) | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-repromote-targeted-2.py` | Targeted re-promotion for 178 BORN_AT/DIED_AT date-bleed + dragon/guards mistypes | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-fix-date-bleed-remaining.py` | Fixes 178 remaining date-bleed character nodes | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-stage3-house-location-reemit.py` | Surgical edge replacement for 259 Stage-1 house nodes (old cite format) | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-stale-dir-cleanup.py` | Migrates nodes whose entity_type_guess no longer matches their directory | 2026-05-01 | LIVE (run complete; kept) |
| B | `wiki-pass2-option-c-prose-merge.py` | Re-emits Stage-1 character nodes with Stage-3 prose, preserving agent-written ## Edges | 2026-04-30 | LIVE (run complete; kept) |
| B | `wiki-pass2-bucket-a-backfill.py` | Promotes 138 Bucket A (Pass 1 referenced, never promoted) wiki pages | 2026-05-12 | LIVE (run complete; kept) |
| B | `wiki-pass2-chapter-promotion-migration.py` | Migrates 344 chapter-summary wiki pages to `meta.chapter` nodes | 2026-05-18 | LIVE (run complete; kept) |
| B | `wiki-pass2-repartition-manifest.py` | Re-partitions Stage 4 batch manifest to smaller N-file batches | 2026-05-18 | LIVE? (one-time utility; may be spent) |
| B | `wiki-pass2-pass-e-phase1.py` | Pass E Phase 1: fixes 19 misclassified title nodes, merges culture dups, re-emits religion-bleed | 2026-04-30 | LIVE (run complete; kept) |

### Tier 3 backfill passes (class B; run complete)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| B | `wiki-pass2-tier3-pass-a-titles.py` | Promotes missing `title` nodes from HOLDS_TITLE orphan slugs | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pass-b-cultures.py` | Promotes missing culture nodes from CULTURE_OF orphan slugs | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pass-c-religions.py` | Promotes religion/god nodes from WORSHIPS orphan slugs | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pass-d-characters.py` | Character backfill for family-tree/kill-edge orphan slugs | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-texts.py` | Path B 1a: promotes `object.text` (in-world books/songs) nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-artifacts.py` | Path B 1b: promotes `object.artifact` (named weapons, ships) nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-events.py` | Path B 3: promotes `event.battle` + `event.war` nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-locations.py` | Path B 2: promotes `place.location` + `place.region` nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-orgs.py` | Path B 4: promotes `organization.house/religion/faction` nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-characters.py` | Path B 5: promotes `character.human/dragon/direwolf` nodes | 2026-04-30 | LIVE (run complete) |
| B | `wiki-pass2-tier3-pathb-longtail.py` | Path B 6: promotes titles + magic + cultures + species long-tail nodes | 2026-04-30 | LIVE (run complete) |

---

## Index Builders & Derived Artifacts (class C/D — rebuilt by `weirwood refresh`)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| D | `build-entity-indexes.py` | Per-entity index roll-up for 17 non-character types → `graph/index/` | 2026-05-12 | LIVE (`weirwood refresh`) |
| D | `build-character-indexes.py` | Per-character index roll-up → `graph/index/characters/` (POV chapters, mentions, edge counts) | 2026-05-11 | LIVE (`weirwood refresh`) |
| D | `build-mention-index.py` | Per-chapter mention index → `graph/index/chapters/` (entity names → slugs) | 2026-05-07 | LIVE |
| D | `wiki-pass2-build-alias-resolver.py` | Builds `alias-resolver.json` from all node frontmatter (slug, name, aliases) | 2026-04-30 | LIVE |
| D | `wiki-pass2-build-cross-refs.py` | Builds `cross-references.jsonl` + `backlink-counts.json` from prose wiki-link anchors | 2026-04-30 | LIVE |
| D | `wiki-pass2-extract-chronology.py` | Extracts year-page link refs → `chronology-events.jsonl` (future temporal-edge backfill) | 2026-05-01 | LIVE |
| C | `wiki-pass2-duplicate-detector.py` | Surfaces candidate duplicates (shared-wiki-source, alias-bridge, slug-similarity) | 2026-04-30 | LIVE |
| D | `wiki-event-alias-harvester.py` | Harvests event-name aliases from MediaWiki cache → `event-node-aliases.json` | 2026-06-08 | LIVE |
| C | `event-node-inventory.py` | Inventories `graph/nodes/events/`; produces catalog + reuse-lookup JSON | 2026-06-07 | LIVE |

---

## Edge Pipeline — Stage 4 Spine / Candidates / Locator (class A/C)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| C | `stage4-pass1-edge-candidates.py` | Walks 344 Pass-1 extractions, parses Relationships tables, resolves slugs, types hints → candidate JSONL | 2026-05-23 | LIVE |
| C | `stage4-pass1-evidence-locator.py` | Locates verbatim supporting passages in chapter prose for each spine candidate | 2026-05-23 | LIVE |
| C | `stage4-pass1-extra-tables.py` | Extra-tables miner: hospitality, dialogue, food/drink, events, info-revealed candidate pools | 2026-05-24 | LIVE |
| C | `stage4-pass1-hint-inventory.py` | Inventories free-text hint phrases across 344 Relationships tables → HINT_TO_EDGE map | 2026-05-22 | LIVE |
| B | `stage4-formalize-edges.py` | Merges/dedups/endpoint-gates all Stage 4 edges → staging dir | 2026-05-25 | LIVE |
| C | `stage4-formalize-edges-test.py` | Unit tests for `stage4-formalize-edges.py` | 2026-05-25 | LIVE |
| B | `stage4-produce-v1-1-candidate.py` | Produces deterministic v1.1 refinement candidate (drops, retypes, annotations) | 2026-05-25 | LIVE |
| B | `stage4-refine-v1-edges.py` | Read-only v1.1 refinement candidate producer (type-contract drop + quote-relevance flag) | 2026-05-25 | LIVE |
| B | `stage4-reground-core-citations.py` | Re-grounds evidence_ref line numbers for shipped core (fixes ':11' bug) | 2026-05-26 | LIVE (run complete) |
| C | `stage4-resolve-link-placeholders.py` | Burns `[LINK]` → `«anchor_text»` into candidate snippets before classification | 2026-05-20 | LIVE |
| C | `stage4-quote-relevance-filter.py` | Name-aware quote-relevance filter (both endpoints must appear) | 2026-05-25 | LIVE |
| C | `stage4-type-contract-validator.py` | Deterministic endpoint-type contract validator (DROP/FLIP/FLAG/RETYPE/KEEP) | 2026-05-25 | LIVE |
| C | `stage4-fresh-relocate-sample.py` | Draws fresh stratified sample from untyped _extra-tables pool, re-locates with v2 locator | 2026-05-25 | LIVE |
| C | `stage4-relocate-smoke.py` | Re-locates evidence quotes for smoke rows with locator v2; measurement report | 2026-05-25 | LIVE |

---

## Edge Pipeline — Stage 4 Tail Classifier + Haiku (LLM typing; class A/C)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| A | `stage4.sh` | Stage 4 worker controller: status/run/launch/unstick (wraps `weirwood stage4`) | 2026-05-18 | LIVE |
| A | `stage4-tail-classifier.py` | LLM tail classifier: batches untyped rows → Haiku/Sonnet for locked-vocab typing | 2026-05-23 | LIVE |
| A | `stage4-haiku-run.py` | Haiku orchestrator: bookkeeping + batch chunking + `claude -p` subprocess dispatch | 2026-05-20 | LIVE |
| C | `stage4-haiku-normalize-edge-types.py` | Deterministic edge-type-name normalizer (case/whitespace/morphology drift) | 2026-05-20 | LIVE |
| C | `stage4-haiku-residual-resolve.py` | Residual-resolution pass: second Haiku pass on `normalizer-residual` rows | 2026-05-20 | LIVE |
| B | `stage4-close-vocab-gaps.py` | Closes vocab-gap rows with Session 54/55 resolution decisions | 2026-05-18 | LIVE (run complete) |
| C | `stage4-vocab-gap-analysis.py` | Normalizes/rolls up `questions-for-matt.jsonl` across 16 schemas | 2026-05-18 | LIVE? (may be spent) |
| C | `stage4-model-run-diff.py` | Diffs two tail-classifier runs over the same rows (verdict comparison) | 2026-05-27 | LIVE |
| C | `stage4-edge-temporal-scope.py` | Annotates `edges.jsonl` with temporal order (book_order × chapter_number); audits conflict pairs | 2026-05-27 | LIVE |
| C | `build-edge-type-counts.py` | Tallies edge-type instances vs locked vocab; emits counts + drift report (canonical vocab extraction) | 2026-05-18 | LIVE |
| C | `build-vocab-gap-log.py` | Aggregates vocab-gap rows across buckets → human log + structured JSON | 2026-05-18 | LIVE |
| B | `stage4-deprecate-comention-stamp.py` | Stamps deprecated comention output IN-DATA (`status: superseded`) | 2026-05-23 | LIVE (run complete; kept for record) |
| A | `mission-stage4-init.py` | Initializes Stage 4 bulk mission: scans inputs, groups into priority-tier batches, writes manifest | 2026-05-18 | LIVE |

---

## Edge Modeling / Reification (Plates 0–5 — class B one-shot mutations; kept)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| B | `aerys-slug-merge.py` | Plate 0b: Aerys slug merge candidates (`aerys-targaryen` → `aerys-ii-targaryen`) | 2026-06-05 | LIVE (shipped) |
| B | `edge-direction-normalizer.py` | Plate 0: head-direction normalizer for `edges.jsonl` (fixes inverted source/target) | 2026-06-05 | LIVE (shipped) |
| B | `stage-drift-reclassify.py` | Plate 2.5: staging for 12 event-node category-drift cases | 2026-06-07 | LIVE (shipped) |
| B | `stage-event-collision-merge.py` | Plate 2.5: merge candidates for reuse-lookup collision groups | 2026-06-07 | LIVE (shipped) |
| B | `edge-reify-backfill.py` | Plate 3: mines Pass-1 for n-ary events, resolves hubs, emits role edges (AGENT_IN/VICTIM_IN/…) | 2026-06-07 | LIVE |
| C | `plate2-event-coverage.py` | Plate 2: measures Pass-1 event coverage by existing event nodes | 2026-06-05 | LIVE |
| C | `plate3-alias-retro-match.py` | Plate 3: checks whether minted slugs appear in `event-node-aliases.json` | 2026-06-08 | LIVE (shipped) |
| B | `plate4-wiki-cluster.py` | Plate 4: classifies Plate-3 mints against wiki event-nodes via LLM (sub-beat/dup/distinct) | 2026-06-08 | LIVE (shipped) |
| B | `plate4-emit-cluster-edges.py` | Plate 4: emits SUB_BEAT_OF / DUPLICATE_OF edges → staging JSONL | 2026-06-08 | LIVE (shipped) |
| B | `plate5-merge.py` | Plate 5: gated merge of all staged edge-modeling work → canonical `edges.jsonl` | 2026-06-08 | LIVE (shipped) |
| C | `stage3-preview-emit.py` | Stage 3 preview: emits sample node files to `_stage3-preview/` (no modifications) | 2026-04-30 | LIVE? (preview; may be spent) |
| B | `rename-event-node.py` | Renames an event node slug across graph: node file + edges.jsonl + alias files + cross-refs | 2026-06-10 | LIVE |
| B | `infobox-merge.py` | S94: merges 20,614 wiki infobox rows → ~17,006 Tier-2 `wiki-infobox` edges (dry-run/apply gated) | 2026-06-12 | LIVE (shipped S94) |
| B | `graph-cleanup-2026-06-14.py` | S96: FIX-22 + plate5 small-followups + 27 S95 edges merge into `edges.jsonl` | 2026-06-14 | LIVE (run complete; kept) |
| C | `edge-reify-run-forever.sh` | 5-hour-wall-safe wrapper for Plate-3 reification full sweep (`edge-reify-backfill.py --all --resume`) | 2026-06-08 | LEGACY-migrate-to-longrun (registry track `edge-reify` = PLANNED — **kept**) |

---

## Historical-Anchor attachment (followup #9 — class B/C)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| C | `historical-anchor-candidates.py` | Surfaces isolated historical-event hubs + candidate existing dyads to attach (read-only) | 2026-06-15 | LIVE |
| C | `historical-anchor-validate.py` | 2-stage verbatim validation of proposed historical-anchor attach edges | 2026-06-15 | LIVE |
| B | `historical-anchor-mint.py` | Mints validated historical-anchor attach edges into `edges.jsonl` (`wiki-historical-anchor` Tier-2) | 2026-06-15 | LIVE (wave 1 shipped S97; wave 2 queued) |

---

## Graph Query & Audit Tools (class C — read-only)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| C | `graph-conflict-pairs.py` | Read-only semantic-conflict audit: flags entity pairs with incompatible edge types | 2026-05-26 | LIVE |
| C | `orphan-edges-audit.py` | Full-corpus orphan-edge auditor: classifies unresolved edge targets | 2026-04-30 | LIVE |
| C | `audit-missing-nodes.py` | Audits wiki↔graph gap: wiki pages with no node, sorted by Pass-1 mention frequency | 2026-05-11 | LIVE |
| C | `audit-prose-coverage.py` | Per-node prose coverage audit (stub vs prose-attached, wiki cache, redirect-only) | 2026-05-11 | LIVE |
| C | `wiki-pass2-validate-edge-jsonl.py` | Validates Stage 4 batch output: required-fields + type contracts + qualifier enums | 2026-05-18 | LIVE |
| C | `wiki-pass2-flag-suspicious-edges.py` | Tags `emit_edge` rows matching soft-fallback / semantic-suspicious patterns | 2026-05-18 | LIVE |
| C | `filter-case-collision-tail.py` | Filters 65 case-collision tail slugs into DROP/ALREADY_EXISTS/CANONICAL/UNCERTAIN | 2026-05-12 | LIVE? (mission; may be spent) |
| B | `promote-case-collision.py` | Promotes 60 case-collision worker outputs into `graph/nodes/` (--dry-run/--apply) | 2026-05-12 | LIVE (run complete; kept) |

---

## Edge Pipeline — Wiki Comention (DEPRECATED — 27 scripts KEPT as revival-recall lever)

> Per S73 decision: these scripts are deliberately kept. Wiki-comention is DEPRECATED (replaced by the Pass-1-derived pipeline). Do NOT re-run them and do NOT archive them. Class — these are spent class-B/C iteration scripts retained for recall.

| Script | What it does | Added | Status |
|--------|--------------|-------|--------|
| `wiki-pass2-build-comention-candidates.py` | Builds entity-pair co-mention candidates from meta.chapter prose | 2026-05-18 | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-build-edge-candidates.py` | Filters `cross-references.jsonl` → per-source candidate edge JSONL | 2026-05-18 | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-build-pass1-relationship-candidates.py` | Walks Pass 1 Relationships tables → candidate edge JSONL | 2026-05-18 | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-enrich-candidates.py` | Enriches candidates with target_type, evidence_paragraph, valid_edge_types | 2026-05-21 | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-batch-comention-reject.py` | Batch-classifies ACOK co-mention candidates as `reject_just_mention` | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention.py` | Stage 4 comention classifier (reference) | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention-batch.py` | Batch comention classifier with relationship_signals | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention-review.py` | Formats co-mention candidates as readable review | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `classify-comention-candidates.py` | Comention classifier (SIBLING_OF/TRAVELS_WITH/LOVER_OF/MANIPULATES/SERVES) | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `classify-comention-batch.py` | Conservative comention batch classifier (defaults to reject) | 2026-05-23 | SUPERSEDED-by-pass1-derived |
| `classify-comention-adwd-41-45.py` | Deterministic classifier for ADWD ch 41-45 comention candidates | 2026-05-23 | SUPERSEDED-by-pass1-derived |

> The remaining comention scripts overlap the Stage-4 Haiku/iteration sections (they were dual-purpose). The 27-script KEEP set spans the `*-comention-*` scripts above plus the `classify-*`/`stage4-*classify*` iteration scripts that were ARCHIVED 2026-06-15 (those moved to `scripts/archive/` but remain in git history — the S73 "do not delete" intent is preserved by archival, not deletion).

---

## Run Wrappers / Supervisors (legacy; superseded by `longrun.sh`)

| Class | Script | What it does | Added | Status |
|-------|--------|--------------|-------|--------|
| A | `stage4-run-forever.sh` | Wraps `stage4.sh run`; inspects next-eligible.txt + manifest; sleeps until reset. **Proven reference** (`project_stage4_run_forever_wrapper`) — **kept**. | 2026-05-18 | LEGACY-migrate-to-longrun (kept as reference) |

> The other 4 run-forever wrappers (`stage4-haiku-run-forever.sh`, `stage4-haiku-loop.sh`, `stage4-tail-bulk-forever.sh`, `stage4-events-bulk-run.sh`) were **ARCHIVED 2026-06-15** (their tracks are shelved/NO-GO'd). Their good ideas (rate-limit detect, sleep defaults) are folded into `pace.py` + `worker-template.py`. `edge-reify-run-forever.sh` is **kept** (registry `edge-reify` track = PLANNED/live). See the archive section.

---

## archive/ (retired — do not restore unless a track reopens)

**Original archive (2):**
- `wiki-scraper.py.archive` — original Playwright AWOIAF scraper. Superseded by the local cache at `sources/wiki/_raw/`. **Do NOT restore** (CLAUDE.md hard rule).
- `wiki-fetch-categories.py.archive` — earlier version of the categories backfill. Superseded by live `wiki-fetch-categories.py`.

**Archived 2026-06-15 (Session 2 consolidation — 30 files, `git mv`, history preserved):**

*Early Stage-4 classify-* / temp-* iteration scripts (superseded by `stage4-tail-classifier.py`):*
`classify-prose-edges-haiku.py`, `classify-prose-edges-house-mormont.py`, `classify-prose-edges-randyll-tarly.py`,
`classify-ramsay-snow.py`, `classify-wyman-manderly.py`, `stage4-classify-manderly.py`,
`stage4-classify-prose-edges-haiku.py`, `stage4-classify-prose-edges.py`, `stage4-comention-classifier.py`,
`stage4-complete-classifier.py`, `stage4-haiku-classify-batch.py`, `stage4-haiku-classify-comention.py`,
`stage4-haiku-classify-karstark.py`, `stage4-haiku-classify-prose-edges.py`, `stage4-haiku-classify-test.py`,
`stage4-haiku-classify-v2.py`, `stage4-haiku-classify.py`, `stage4-haiku-proper-classify.py`,
`stage4-prose-edge-classifier.py`, `stage4-real-classifier.py`, `temp-classify-glovers.py`.

*Spent one-shots / smoke:* `events-drift-audit.py` (THROWAWAY drift audit), `stage4-haiku-smoke-prep.py`,
`stage4-haiku-smoke-cleanup.py`, `stage4-haiku-smoke-finish.sh`, `migrate-stats-csv.py` (de-referenced from `extract.sh` first).

*Shelved run-forever wrappers (tracks shelved/NO-GO'd):* `stage4-haiku-run-forever.sh`, `stage4-haiku-loop.sh`,
`stage4-tail-bulk-forever.sh`, `stage4-events-bulk-run.sh`.

> **Frozen stats CSVs** (not scripts) were moved to `working/extraction-stats/_archive/` the same session
> (Pass 1 = 344/344, Pass 2 complete; nothing appends anymore). `pace.py backfill`, `extract.sh status`, and
> `weirwood wiki status` all fall back to `_archive/` so nothing silently degrades.
