# scripts/ — Weirwood Network Script Inventory

**Generated:** 2026-06-12  
**Rule:** This file is a MAP, not a cleanup list. Nothing is moved or deleted here.  
Archiving/deletion moves happen in a separate session, off this inventory.

---

## Legend

| Status | Meaning |
|--------|---------|
| `LIVE` | Actively used; do not archive |
| `LEGACY-migrate-to-longrun` | Run-forever wrapper superseded by `longrun.sh`; migrate when its track finishes — do NOT touch while a live run is in progress |
| `SUPERSEDED-by-pass1-derived` | Wiki-comention scripts (27 total); KEPT as revival-recall lever (S73 decision) — do NOT propose archiving |
| `SUPERSEDED-by-X` | Replaced by a named successor |
| `ARCHIVE-CANDIDATE` | Single-purpose throwaway confirmed as such in project docs |
| `LIVE?` | Purpose unclear; needs verification |

**Summary (146 scripts + 2 archive files):**  
LIVE: 98 · LEGACY-migrate-to-longrun: 6 · SUPERSEDED-by-pass1-derived: 27 · SUPERSEDED-by-X: 7 · ARCHIVE-CANDIDATE: 5 · LIVE?: 3

---

## Chapter / Source Processing

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `chapter-splitter.py` | Splits ASOIAF .txt source files into per-chapter markdown with YAML frontmatter | Chapter split | LIVE |
| `dunk-egg-splitter.py` | Splits Dunk & Egg Calibre plaintext into 3 novella markdown files | Chapter split | LIVE |

---

## Extraction Pipeline (Pass 1)

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `extract.sh` | Unified extraction entry point: run/status/launch subcommands; wraps `weirwood` shell function | Pass 1 extraction | LIVE |
| `run-extraction-wave.sh` | Runs Pass 1 extraction on one wave of chapters (5 chapters per wave) in a single terminal | Pass 1 extraction | LIVE |
| `run-extraction-all.sh` | Runs Pass 1 extraction across an entire book with N parallel workers and skip-existing resume | Pass 1 extraction | LIVE |
| `launch-extraction.sh` | Opens iTerm2 tabs and runs extraction waves in parallel; supports --chain for chained wave cycling | Pass 1 extraction | LIVE |
| `claim-chapter.py` | Atomically claims a chapter for extraction against the stats CSV (race-safe via lockdir) | Pass 1 extraction | LIVE |
| `extract-status-sweep.py` | Sweeps stale started/working CSV rows and rewrites them as failed-stale | Pass 1 extraction | LIVE |
| `extraction-status.sh` | Shows per-book extraction progress and next steps | Pass 1 extraction | LIVE |
| `stream-claude-output.py` | Streams Claude assistant output to stderr with │ prefix during extraction | Pass 1 extraction | LIVE |
| `migrate-stats-csv.py` | Migrates extraction-stats CSV from old 13-col schema to new 16-col schema | Pass 1 extraction | SUPERSEDED-by-new-schema (one-time migration; run is complete) |
| `weirwood.zsh` | Shell function loader — `weirwood` CLI entry point for extraction and stage4 | Pass 1 extraction | LIVE |

---

## Wiki Pipeline — Crawl Era / Parser / Infobox

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `wiki-infobox-parser.py` | Parses all 17,657 cached wiki JSON files; emits `infobox-data.jsonl` + `page-index.jsonl` + `parse-stats.md` | Wiki Pass 2 | LIVE |
| `wiki-fetch-categories.py` | Bounded MediaWiki categories backfill (approved exception fetch 2026-04-30); writes `page-categories.jsonl` | Wiki Pass 2 | LIVE (run complete; kept for rerun if needed) |
| `wiki-pass2-triage.py` | Triages 17,657 wiki pages into per-bucket manifests (Stage 1 + Stage 2 grouping) | Wiki Pass 2 | LIVE |
| `wiki-pass2-prioritize.py` | Computes `priority_tier` A/B/C for every page in secondary-tier manifests | Wiki Pass 2 | LIVE |
| `wiki-pass2.sh` | Wiki Pass 2 launcher: triage/run/launch/status/check/reset/unstick/questions/stop subcommands | Wiki Pass 2 | LIVE |

---

## Wiki Pipeline — Pass 2 Promotion Stages

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `wiki-pass2-emit-deterministic.py` | Stage 3a: emits deterministic skeleton node files from manifest + infobox data | Wiki Pass 2 | LIVE |
| `wiki-pass2-extract-prose.py` | Stage 3b: extracts prose body from cached wiki HTML into per-page prose files | Wiki Pass 2 | LIVE |
| `wiki-pass2-promote.py` | Stage 3 promotion: concatenates skeleton + prose artifacts → atomic rename into `graph/nodes/` | Wiki Pass 2 | LIVE |
| `wiki-pass2-validator.py` | Gate validator: validates `tmp/` node files before launcher promotes to `graph/nodes/` | Wiki Pass 2 | LIVE |
| `wiki-pass2-coherence.py` | Cross-bucket coherence check: edge targets exist, allegiance resolves, no duplicate names | Wiki Pass 2 | LIVE |
| `wiki-pass2-attach-prose.py` | Attaches prose body to stub-only `pass2-wiki-deterministic` nodes that lack prose sections | Wiki Pass 2 | LIVE |
| `wiki-pass2-repromote-targeted.py` | Targeted re-promotion for 14 parser-bug-affected nodes (mistyped + religion-bleed) | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-repromote-targeted-2.py` | Targeted re-promotion for 178 BORN_AT/DIED_AT date-bleed + dragon mistype + guards mistype bugs | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-fix-date-bleed-remaining.py` | Fixes 178 remaining date-bleed character nodes after Session 27 repromote wave | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-stage3-house-location-reemit.py` | Surgical edge replacement for 259 Stage-1 house nodes (upgrades old `cite: track_b_row` edge format) | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-stale-dir-cleanup.py` | Migrates nodes whose entity_type_guess no longer matches their directory | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-option-c-prose-merge.py` | Option C: re-emits Stage-1 character nodes with Stage-3 prose while preserving agent-written ## Edges | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-bucket-a-backfill.py` | Promotes 138 Bucket A (Pass 1 referenced, never promoted) wiki pages | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-chapter-promotion-migration.py` | Migrates 344 chapter-summary wiki pages to `meta.chapter` nodes in `graph/nodes/chapters/` | Wiki Pass 2 | LIVE (run complete; kept for rerun) |
| `wiki-pass2-repartition-manifest.py` | Re-partitions Stage 4 batch manifest from 30-file batches to smaller N-file batches | Wiki Pass 2 | LIVE? (one-time utility; may be spent) |
| `wiki-pass2-stale-dir-cleanup.py` | (listed above) | — | — |
| `wiki-pass2-pass-e-phase1.py` | Pass E Phase 1: fixes 19 misclassified title nodes, merges culture duplicates, re-emits religion-bleed locations | Wiki Pass 2 | LIVE (run complete; kept for rerun) |

---

## Wiki Pipeline — Tier 3 Backfill Passes

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `wiki-pass2-tier3-pass-a-titles.py` | Tier 3 Pass A: promotes missing `title` nodes from HOLDS_TITLE orphan slugs | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pass-b-cultures.py` | Tier 3 Pass B: promotes missing culture nodes from CULTURE_OF orphan slugs | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pass-c-religions.py` | Tier 3 Pass C: promotes religion/god nodes from WORSHIPS orphan slugs | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pass-d-characters.py` | Tier 3 Pass D: character backfill for family-tree/kill-edge orphan slugs | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-texts.py` | Path B Sub-task 1a: promotes `object.text` (in-world books/songs) nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-artifacts.py` | Path B Sub-task 1b: promotes `object.artifact` (named weapons, ships) nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-events.py` | Path B Sub-task 3: promotes `event.battle` + `event.war` nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-locations.py` | Path B Sub-task 2: promotes `place.location` + `place.region` nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-orgs.py` | Path B Sub-task 4: promotes `organization.house/religion/faction` nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-characters.py` | Path B Sub-task 5: promotes `character.human/dragon/direwolf` nodes | Wiki Pass 2 | LIVE (run complete) |
| `wiki-pass2-tier3-pathb-longtail.py` | Path B Sub-task 6: promotes titles + magic + cultures + species long-tail nodes | Wiki Pass 2 | LIVE (run complete) |

---

## Index Builders

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `build-mention-index.py` | Pass 1.7: per-chapter mention index → `graph/index/chapters/` (resolves entity names to slugs) | Index | LIVE |
| `build-character-indexes.py` | Per-character index roll-up → `graph/index/characters/` (POV chapters, mentions, edge counts) | Index | LIVE |
| `build-entity-indexes.py` | Per-entity index roll-up for locations/artifacts/houses → `graph/index/` (non-character node types) | Index | LIVE |
| `wiki-pass2-build-alias-resolver.py` | Builds `alias-resolver.json` from all node frontmatter (slug, name, aliases) | Index | LIVE |
| `wiki-pass2-build-cross-refs.py` | Builds `cross-references.jsonl` + `backlink-counts.json` from all prose wiki-link anchors | Index | LIVE |
| `wiki-pass2-extract-chronology.py` | Extracts year-page internal-link references → `chronology-events.jsonl` (for future temporal-edge backfill) | Index | LIVE |
| `wiki-pass2-duplicate-detector.py` | Surfaces candidate duplicates (shared-wiki-source, alias-bridge, slug-similarity) for Opus review | Index | LIVE |

---

## Edge Pipeline — Stage 4 Spine / Candidates / Locator / Resolver

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `stage4-pass1-edge-candidates.py` | Script 1: walks 344 Pass 1 extractions, parses Relationships tables, resolves slugs, types hints → per-chapter candidate JSONL | Stage 4 spine | LIVE |
| `stage4-pass1-evidence-locator.py` | Script 2: locates verbatim supporting passages in chapter prose for each spine candidate | Stage 4 spine | LIVE |
| `stage4-pass1-extra-tables.py` | Extra tables miner: hospitality, dialogue, food/drink, events, information-revealed candidate pools | Stage 4 spine | LIVE |
| `stage4-pass1-hint-inventory.py` | Inventories free-text hint phrases across all 344 Pass 1 Relationships tables; builds deterministic HINT_TO_EDGE map | Stage 4 spine | LIVE |
| `stage4_name_resolver.py` | Importable module: 5-rung collision-aware name resolver (exact/alias/firstname-unique/context-present/context-prior) | Stage 4 spine | LIVE |
| `stage4-formalize-edges.py` | Merges, deduplicates, and endpoint-gates all Stage 4 edges from spine + tail + hospitality → staging dir | Stage 4 spine | LIVE |
| `stage4-formalize-edges-test.py` | Unit tests for `stage4-formalize-edges.py` | Stage 4 spine | LIVE |
| `stage4-produce-v1-1-candidate.py` | Produces deterministic v1.1 refinement candidate (drops, retypes, evidence annotations) | Stage 4 spine | LIVE |
| `stage4-refine-v1-edges.py` | Read-only v1.1 refinement candidate producer (type-contract hard drop + quote-relevance soft flag) | Stage 4 spine | LIVE |
| `stage4-reground-core-citations.py` | Re-grounds evidence_ref line numbers for shipped core edge layer (fixes ':11' line-number bug) | Stage 4 spine | LIVE (run complete) |
| `stage4-resolve-link-placeholders.py` | Burns `[LINK]` → `«anchor_text»` substitution into candidate snippets before classification | Stage 4 spine | LIVE |
| `stage4-quote-relevance-filter.py` | Name-aware quote-relevance filter: edge passes only if evidence_quote contains tokens for both endpoints | Stage 4 spine | LIVE |
| `stage4-type-contract-validator.py` | Deterministic endpoint-type contract validator (DROP/FLIP/FLAG/RETYPE/KEEP dispositions) | Stage 4 spine | LIVE |
| `stage4-fresh-relocate-sample.py` | Draws fresh stratified sample from untyped _extra-tables pool, re-locates with v2 locator | Stage 4 spine | LIVE |
| `stage4-relocate-smoke.py` | Re-locates evidence quotes for smoke3 rows using improved locator v2; produces measurement report | Stage 4 spine | LIVE |

---

## Edge Pipeline — Stage 4 Tail Classifier (LLM Typing)

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `stage4-tail-classifier.py` | LLM tail classifier: batches untyped `needs_type` rows → Haiku/Sonnet for locked-vocab edge type assignment | Stage 4 tail | LIVE |
| `stage4-close-vocab-gaps.py` | Closes vocab-gap rows in `questions-for-matt.jsonl` with Session 54/55 resolution decisions | Stage 4 tail | LIVE (run complete) |
| `stage4-vocab-gap-analysis.py` | Normalizes and rolls up `questions-for-matt.jsonl` across 16 distinct schemas | Stage 4 tail | LIVE? (may be spent) |
| `stage4-model-run-diff.py` | Diffs two Stage 4 tail-classifier runs over the same candidate rows (verdict comparison) | Stage 4 tail | LIVE |
| `stage4-edge-temporal-scope.py` | Annotates `edges.jsonl` with temporal order (book_order × chapter_number); audits time-conflict pairs | Stage 4 tail | LIVE |

---

## Edge Pipeline — Stage 4 Haiku Bulk Run

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `stage4-haiku-run.py` | Haiku orchestrator: bookkeeping + batch chunking + `claude -p` subprocess dispatch for Haiku classify runs | Stage 4 Haiku | LIVE |
| `stage4-haiku-normalize-edge-types.py` | Deterministic edge-type-name normalizer: fixes case/whitespace/morphology drift in Haiku output | Stage 4 Haiku | LIVE |
| `stage4-haiku-residual-resolve.py` | Residual-resolution pass: gets second Haiku pass on `normalizer-residual` rows; applies map/reject/escalate | Stage 4 Haiku | LIVE |
| `stage4-haiku-smoke-prep.py` | Archives batch-0020 Sonnet output + registers re-run under new batch ID for cross-model smoke | Stage 4 Haiku | SUPERSEDED-by-smoke-complete (one-time smoke setup; smoke is done) |
| `stage4-haiku-smoke-cleanup.py` | Reverses `stage4-haiku-smoke-prep.py`; restores Sonnet mission to pre-smoke state | Stage 4 Haiku | SUPERSEDED-by-smoke-complete (one-time cleanup; smoke is done) |
| `build-edge-type-counts.py` | Scans all node files, tallies edge-type instances, compares against locked vocab; emits counts + drift report | Stage 4 Haiku | LIVE |
| `build-vocab-gap-log.py` | Aggregates `questions-for-matt.jsonl` vocab-gap rows across all buckets → human-readable log + structured JSON | Stage 4 Haiku | LIVE |
| `stage4-deprecate-comention-stamp.py` | Stamps deprecated comention output files IN-DATA (`status: superseded`) — provenance over file moves | Stage 4 Haiku | LIVE (run complete; kept for record) |
| `mission-stage4-init.py` | Initializes Stage 4 bulk prose-edge classification mission: scans inputs, groups into priority-tier batches, writes batch-manifest | Stage 4 Haiku | LIVE |
| `stage4.sh` | Stage 4 worker controller: status/run/launch/unstick subcommands (wraps `weirwood stage4`) | Stage 4 Haiku | LIVE |

---

## Edge Pipeline — Stage 4 Haiku Classify Variants (early iteration scripts)

> These are earlier classifier iterations, pre-`stage4-haiku-run.py` and pre-`stage4-tail-classifier.py`. The canonical path is the tail-classifier + haiku-run combo. These are kept as reference/recall.

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `stage4-classify-prose-edges-haiku.py` | Early per-file Haiku classifier (careful validation + REJECT patterns) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-classify-prose-edges.py` | Deterministic classifier for 5 Lannister-character candidate files | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify.py` | Early Haiku prose-edge classifier (3 candidate files, CRITICAL_RULES dict) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-v2.py` | Haiku classifier v2 (uses anchor_text context) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-test.py` | Earlier Haiku classifier (TIER_1_QUALIFIERS dict) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-prose-edges.py` | Earlier Haiku prose-edge classifier (TIER1_EDGES dict, re_module) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-batch.py` | Batch processor variant for Haiku with relationship_signals extraction | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-comention.py` | Comention-specific candidate formatter/loader for Haiku | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-classify-karstark.py` | Per-character Haiku classifier for Karstark family | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-haiku-proper-classify.py` | Haiku classifier "proper" (uses staging_verbs_present, source_section) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-prose-edge-classifier.py` | Deterministic rule-based classifier using snippet (200-char window) as primary signal | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-real-classifier.py` | Hardcoded ACOK-chapter relationship table classifier | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-complete-classifier.py` | Chapter-relationship table classifier (5 ACOK chapters, full set) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-comention-classifier.py` | Comention classifier with hardcoded KINSHIP_FACTS table | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `classify-prose-edges-haiku.py` | Standalone REJECT-pattern classifier (MATERIAL/TITLE/CONCEPT block) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `classify-prose-edges-house-mormont.py` | Deterministic rule-based classifier for House Mormont characters | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `classify-prose-edges-randyll-tarly.py` | Deterministic rule-based classifier for randyll-tarly | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `classify-ramsay-snow.py` | Intelligent edge classifier for ramsay-snow candidates | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `classify-wyman-manderly.py` | Deterministic rule-based classifier for wyman-manderly (Sessions 61/63 rules) | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `stage4-classify-manderly.py` | Classifier for 5 Manderly-character enriched candidate files | Stage 4 Haiku iter | SUPERSEDED-by-stage4-tail-classifier |
| `temp-classify-glovers.py` | Temporary classifier for Glover family candidates | Stage 4 Haiku iter | ARCHIVE-CANDIDATE |

---

## Edge Pipeline — Wiki Comention (DEPRECATED — KEPT as revival-recall lever)

> Per S73 decision: these 27 scripts are deliberately kept. Wiki-comention is DEPRECATED (replaced by Pass-1-derived pipeline). Do NOT re-run them and do NOT propose archiving. They remain as a recall lever if comention-based edges are ever re-evaluated.

| Script | What it does | Status |
|--------|--------------|--------|
| `wiki-pass2-build-comention-candidates.py` | Builds entity-pair co-mention candidates from meta.chapter prose paragraphs | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-build-edge-candidates.py` | Filters `cross-references.jsonl` → per-source candidate edge JSONL files | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-build-pass1-relationship-candidates.py` | Walks Pass 1 Relationships tables → structured candidate edge JSONL (per-chapter) | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-enrich-candidates.py` | Enriches candidates with `target_type`, `evidence_paragraph`, `valid_edge_types`, `staging_verbs_present` | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention.py` | Stage 4 comention classifier (reference; actual classification requires human judgment) | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention-batch.py` | Batch comention classifier with relationship_signals extraction | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention-review.py` | Formats co-mention candidates as readable text review for systematic classification | SUPERSEDED-by-pass1-derived |
| `classify-comention-candidates.py` | Comention classifier with SIBLING_OF/TRAVELS_WITH/LOVER_OF/MANIPULATES/SERVES heuristics | SUPERSEDED-by-pass1-derived |
| `classify-comention-batch.py` | Conservative comention batch classifier (defaults to `reject_just_mention`) | SUPERSEDED-by-pass1-derived |
| `classify-comention-adwd-41-45.py` | Deterministic classifier for ADWD chapters 41-45 comention candidates | SUPERSEDED-by-pass1-derived |
| `stage4-classify-comention-review.py` | (listed above) | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-batch-comention-reject.py` | Batch-classifies ACOK co-mention candidates as `reject_just_mention` (default rule) | SUPERSEDED-by-pass1-derived |
| `stage4-haiku-smoke-finish.sh` | Drives Haiku worker until batch-0020-haiku-smoke is fully classified | SUPERSEDED-by-pass1-derived |
| `stage4-flag-suspicious-edges.py` _(see wiki-pass2-flag-suspicious-edges.py)_ | — | — |
| `wiki-pass2-flag-suspicious-edges.py` | Tags `emit_edge` rows matching soft-fallback / semantic-suspicious patterns for Opus audit | SUPERSEDED-by-pass1-derived |
| `stage4-vocab-gap-analysis.py` | (also listed in tail section above) | SUPERSEDED-by-pass1-derived |
| `stage4-close-vocab-gaps.py` | (also listed in tail section above — run complete) | SUPERSEDED-by-pass1-derived |
| `stage4-haiku-classify-comention.py` | (listed in haiku-iter section above) | SUPERSEDED-by-pass1-derived |
| `wiki-pass2-attach-prose.py` | (listed in promotion section above — also used by comention prep) | LIVE (dual use) |

---

## Events / Enrichment Era

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `wiki-event-alias-harvester.py` | Harvests event-name aliases from local MediaWiki cache (redirect pages + infobox titles) → `event-node-aliases.json` | Events | LIVE |
| `event_alias_resolver.py` | Builds flat `{alias_phrase → canonical_slug}` lookup from 3 sources; CLI lookup mode | Events | LIVE |
| `event-node-inventory.py` | Inventories existing `graph/nodes/events/` nodes; produces human catalog + reuse-lookup JSON | Events | LIVE |
| `rename-event-node.py` | Renames an event node slug across graph: node file + edges.jsonl + alias files + cross-refs + other node bodies | Events | LIVE |
| `stage4-haiku-run-forever.sh` | Resilient outer wrapper for `stage4-haiku-loop.sh`; re-launches on crash/stop | Stage 4 Haiku | LEGACY-migrate-to-longrun |
| `stage4-haiku-loop.sh` | Sequential Haiku batch runner with stop-file support; sleeps between batches | Stage 4 Haiku | LEGACY-migrate-to-longrun |
| `events-drift-audit.py` | THROWAWAY: Stratified 50-row cross-model drift audit of Events Haiku bulk emits (Sonnet vs Haiku; seed=531) | Events | ARCHIVE-CANDIDATE |

---

## Edge Modeling / Reification (Plates 0-5)

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `aerys-slug-merge.py` | Plate 0b: generates Aerys slug merge candidates (phantom `aerys-targaryen` → canonical `aerys-ii-targaryen`) | Edge modeling | LIVE (Plate 0 shipped) |
| `edge-direction-normalizer.py` | Plate 0: deterministic head-direction normalizer for `edges.jsonl` (fixes inverted source/target from Pass-1 typer) | Edge modeling | LIVE (Plate 0 shipped) |
| `stage-drift-reclassify.py` | Plate 2.5: staging candidates for 12 event-node category-drift cases (POV chapters mistyped as event.battle) | Edge modeling | LIVE (Plate 2.5 shipped) |
| `stage-event-collision-merge.py` | Plate 2.5: produces merge candidates for reuse-lookup collision groups (multiple slugs per normalized key) | Edge modeling | LIVE (Plate 2.5 shipped) |
| `edge-reify-backfill.py` | Plate 3: mines Pass-1 for n-ary events, resolves event hubs, emits role edges (AGENT_IN/VICTIM_IN/COMMANDS_IN/LOCATED_AT) | Edge modeling | LIVE |
| `plate2-event-coverage.py` | Plate 2: measures Pass-1 event coverage by existing event nodes (chapter-overlap + title fuzzy match) | Edge modeling | LIVE |
| `plate3-alias-retro-match.py` | Plate 3: checks whether 219 minted event-node slugs appear in `event-node-aliases.json` | Edge modeling | LIVE (Plate 3 shipped) |
| `plate4-wiki-cluster.py` | Plate 4: classifies Plate-3 mints against wiki event-nodes via LLM (sub-beat-of/duplicate-of/distinct) | Edge modeling | LIVE (Plate 4 shipped) |
| `plate4-emit-cluster-edges.py` | Plate 4: emits SUB_BEAT_OF / DUPLICATE_OF edges from Pass-A/B/C cascade → staging JSONL | Edge modeling | LIVE (Plate 4 shipped) |
| `plate5-merge.py` | Plate 5: gated merge of all staged edge-modeling work into canonical `graph/edges/edges.jsonl` | Edge modeling | LIVE (Plate 5 shipped) |
| `stage3-preview-emit.py` | Stage 3 preview: emits sample node files for 3 targets to `_stage3-preview/` (no modifications) | Edge modeling | LIVE? (preview; may be spent) |

---

## Graph Query & Audit Tools

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `graph-query.py` | Read-only graph inspection: node header, outbound edges, inbound refs, `--neighbors`, `--path`, `--health`, `--event-participants` | Graph query | LIVE |
| `graph-conflict-pairs.py` | Read-only semantic-conflict audit: flags entity pairs with incompatible edge types (e.g. LOVES + HATES) | Graph audit | LIVE |
| `orphan-edges-audit.py` | Full-corpus orphan-edge auditor: classifies unresolved edge targets into Cat 1/2/stale-legacy/format issues | Graph audit | LIVE |
| `audit-missing-nodes.py` | Audits gap between wiki cache and graph: wiki pages with no graph node, sorted by Pass 1 mention frequency | Graph audit | LIVE |
| `audit-prose-coverage.py` | Per-node prose coverage audit: stub vs. prose-attached, has wiki cache, redirect-only, etc. | Graph audit | LIVE |
| `wiki-pass2-validate-edge-jsonl.py` | Validates Stage 4 batch output: required-fields contract + type contracts + qualifier enums | Graph audit | LIVE |
| `stage4-type-contract-validator.py` | (also in spine section — importable module used by audit) | Stage 4 spine | LIVE |
| `stage4-edge-temporal-scope.py` | (also in tail section — temporal annotation + conflict audit) | Stage 4 tail | LIVE |
| `filter-case-collision-tail.py` | Filters 65 case-collision tail slugs into DROP/ALREADY_EXISTS/CANONICAL/UNCERTAIN | Graph audit | LIVE? (case-collision mission; may be spent) |
| `promote-case-collision.py` | Promotes 60 case-collision worker outputs into `graph/nodes/` (--dry-run / --apply) | Graph audit | LIVE (run complete; kept for rerun) |

---

## Validators & Flaggers

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `stage4-type-contract-validator.py` | (listed above in spine + audit sections) | — | LIVE |
| `stage4-quote-relevance-filter.py` | (listed above in spine section) | — | LIVE |
| `wiki-pass2-coherence.py` | (listed above in promotion section) | — | LIVE |
| `wiki-pass2-duplicate-detector.py` | (listed above in index section) | — | LIVE |
| `wiki-pass2-validate-edge-jsonl.py` | (listed above in audit section) | — | LIVE |
| `stage4-haiku-normalize-edge-types.py` | (listed above in haiku section) | — | LIVE |

---

## Run Wrappers / Supervisors

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `longrun.sh` | **Generic long-run supervisor.** Relaunches any command on rate-limit walls (exit 2) and crashes; exits cleanly on success (exit 0); iteration loop on exit 10. Standardized env vars + logging. Exit contract: 0=done / 2=wall-sleep-relaunch / 10=more-work-sleep-relaunch / other=crash-retry. | Infrastructure | LIVE |
| `stage4-run-forever.sh` | Wraps `stage4.sh run`; inspects next-eligible.txt + manifest; sleeps until reset if needed | Stage 4 | LEGACY-migrate-to-longrun |
| `stage4-events-bulk-run.sh` | Paced multi-day wrapper for Stage 4 pass1_events Haiku bulk typing run (inter-batch `--sleep-between` pacing) | Stage 4 Events | LEGACY-migrate-to-longrun |
| `stage4-tail-bulk-forever.sh` | Burst-model overnight loop for tail-classifier bulk run (runs flat-out until rate-limit wall, then sleeps) | Stage 4 tail | LEGACY-migrate-to-longrun |
| `edge-reify-run-forever.sh` | 5-hour-wall-safe wrapper for Plate 3 reification full sweep (`edge-reify-backfill.py --all --resume`) | Edge modeling | LEGACY-migrate-to-longrun |
| `stage4-haiku-run-forever.sh` | Resilient outer wrapper for `stage4-haiku-loop.sh`; re-launches on crash/stop-file | Stage 4 Haiku | LEGACY-migrate-to-longrun |
| `stage4-haiku-loop.sh` | Sequential Haiku batch runner; sleeps `STAGE4_HAIKU_SLEEP_BETWEEN` between batches | Stage 4 Haiku | LEGACY-migrate-to-longrun |

---

## One-Off / Throwaway

| Script | What it does | Track | Status |
|--------|--------------|-------|--------|
| `events-drift-audit.py` | Stratified ~50-row cross-model drift audit of Events Haiku bulk emits (docstring: "THROWAWAY") | Events | ARCHIVE-CANDIDATE |
| `temp-classify-glovers.py` | Temporary classifier for Glover family candidates (filename: `temp-*`) | Stage 4 Haiku iter | ARCHIVE-CANDIDATE |
| `stage4-haiku-smoke-prep.py` | One-time smoke setup: archives Sonnet output + registers re-run under new batch ID | Smoke | ARCHIVE-CANDIDATE |
| `stage4-haiku-smoke-cleanup.py` | One-time smoke cleanup: reverses smoke-prep (both smoke-prep and smoke-cleanup are spent) | Smoke | ARCHIVE-CANDIDATE |
| `stage4-haiku-smoke-finish.sh` | Drove Haiku worker until smoke batch was fully classified (smoke is done) | Smoke | ARCHIVE-CANDIDATE |
| `migrate-stats-csv.py` | One-time CSV schema migration (13-col → 16-col); migration is complete | Infra | SUPERSEDED-by-new-schema |

---

## archive/ (retired — do not restore)

`scripts/archive/` contains 2 files:

- `wiki-scraper.py.archive` — original Playwright-based AWOIAF wiki scraper. Archived per CLAUDE.md; superseded by the local cache at `sources/wiki/_raw/`. Do NOT restore.
- `wiki-fetch-categories.py.archive` — earlier version of the categories backfill script. Superseded by the live `wiki-fetch-categories.py`.
