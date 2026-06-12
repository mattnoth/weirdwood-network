# Weirwood Network Graph Deep Dive — Findings & Verdict (2026-06-11)

> Produced 2026-06-11 by a read-only Fable subagent. All counting done with throwaway Python in /tmp
> (`an1_edges.py` … `an7_proj.py`) against the repo. Nothing modified.

## 1. Canonical edge layer (`graph/edges/edges.jsonl`, 4,760 rows)

- **evidence_kind:** book-pass1 3,809 | book-pass1-reified 897 | plate4-wiki-cluster 51 | book-curator 3
- **typed_by:** python-map 1,962 | sonnet 1,401 (tail-llm) | hospitality-table 396 + violation 50 | curator-s91 3 | missing 948 (= the 897 reified + 51 plate4 rows)
- **confidence_tier:** 1: 4,553 | 2: 194 | 3: 13
- **edge types:** 111 distinct. Top: GUEST_OF 404, AGENT_IN 335, VICTIM_IN 316, OPPOSES 265, SERVES 255, DISTRUSTS 204, HATES 173, COMMANDS 171… Heavily affect/interaction-typed; **family types are thin: SIBLING_OF 51, PARENT_OF 41, SPOUSE_OF 40, UNCLE_OF 25, COUSIN_OF 21.**
- **Evidence quality is excellent:** 4,728/4,760 carry evidence_quote; 3,782 have `file:line` evidence_ref with locate_status=verbatim (the 948 reified/plate rows cite chapter labels like "ASOS Jon VIII" instead — no file:line, no typed_by).
- **1,330 distinct endpoint slugs**, of which **115 have no node file** — mostly alias-slug mismatches (`brienne-of-tarth` vs node `brienne-tarth`, `aeron-damphair` vs `aeron-greyjoy`, `bittersteel`, `big-walder-frey`). Small but real referential-integrity gap.

## 2. Node-layer connectivity — the isolation problem, quantified

**8,261 node files (excl. _conflicts/_unclassified); only 1,216 (14.7%) touch any edge.**

| Type | Nodes | Connected |
|---|---|---|
| characters | 3,925 | 784 (20.0%) |
| locations | 1,097 | 57 (5.2%) |
| events | 583 | 249 (42.7%) |
| houses | 556 | 25 (4.5%) |
| titles | 542 | 14 (2.6%) |
| artifacts | 282 | 18 (6.4%) |
| factions | 191 | 35 (18.3%) |
| everything else | ~1,085 | ~34 (<5%) |

Degree of connected nodes: median 3, mean 7.7, p90 13. Hubs: jon-snow 336, tyrion-lannister 334, daenerys-targaryen 261, cersei-lannister 256, arya/jaime 207 — the spine is dense and healthy; everything off-POV-screen is dark.

## 3. The three latent wiki layers

**(a) Node-file `## Edges` display bullets:** 4,684 of 8,263 files have them; **21,129 bullets**, 56 relation types (SWORN_TO 4,143, HOLDS_TITLE 3,919, CULTURE_OF 3,447, PARENT_OF 1,765, DIED_AT 924, BORN_AT 881, SPOUSE_OF 663…). ~72% of targets resolve to existing node slugs after stripping cite suffixes; misses are mostly culture strings ("Stormlander", "Andal"), "Unknown", and date-qualified death-places. **These bullets are a rendering of the same infobox data as (b)** — `(track_b: …)` provenance throughout — so (a) and (b) are one layer, not two.

**(b) Infobox-structural (`working/wiki/data/infobox-data.jsonl`):** 4,786 pages, 4,663 with ≥1 relationship, **20,614 relationship rows already typed to 23 edge types** (SWORN_TO 4,142, HOLDS_TITLE 3,976, CULTURE_OF 3,329, PARENT_OF 3,143, DIED_AT 939, BORN_AT 896, SPOUSE_OF 668, RULES 559, DEFEATS 316, HEIR_TO 201…). Source pages resolve 4,660/4,663; **targets resolve 92.2%** with naive slugify (the alias-resolver would push higher). Known noise to filter: "Unknown"/"None"/"Extinct"/bare "Son(s)" targets (~500 rows), culture-string targets, speculative fields (Jon Snow's infobox lists *two* "Mothers" — Wylla and Ashara Dayne — naive promotion would mint false PARENT_OF edges), and multi-value parse splits (Doran gets `SPOUSE_OF → Norvos` from "Mellario of Norvos", `HOLDS_TITLE → Sunspear` from "Castellan of Sunspear").

**(c) Prose-comention/entity emits (pass2-buckets):** 207 buckets with Sonnet `prose-edges/` (**4,132 emit_edge** out of 14,502 decisions), 37 buckets `prose-edges-haiku/` (2,050 emits / 16,864 rows, of which 295 comention emits are already stamped `status=superseded, do_not_promote=true`), plus `_events-haiku-bulk` (16,583 rows, 14,884 rejected, ~1,617 typed — the NO-GO'd run). Sampled 18 emits: facts mostly accurate, but **evidence is wiki-prose snippets, not book quotes — no file:line, no verbatim locate** — and the schema is inconsistent across batches (`source` vs `source_slug`, `confidence: "tier-1"` strings vs `confidence_tier: 1` ints, ~800 rows missing slug fields, 1,162 missing evidence_kind). Several type-stretches (Mance OPPOSES Stannis evidenced by "Melisandre is preparing to burn Mance"; RESPECTS from a quote section). This layer fails the canonical evidence standard as-is and would need per-row revalidation.

## 4. Overlap & complementarity (30 major characters)

The wiki layer is **98.4% additive at the pair level**: of 20,614 infobox pairs, only 340 connect a pair edges.jsonl already connects; only 159 match on (pair, type). For family edges specifically, 94% of 4,205 infobox family rows connect pairs canon doesn't.

Pattern: book layer wins on lived relationships (Jon has 336 edges: LOVES/PROTECTS/OPPOSES with quotes); wiki wins on **genealogy, titles, allegiance, vital records**. Walder Frey: book = 2 family edges (two HEIR_TO); wiki = 8 spouses + 29 children. Jon Snow's book family edges cover only Ned + 4 siblings + Benjen; no Lyanna/Rhaegar anywhere (and the wiki's "Mothers" field is the rumor pair). Varys, Melisandre, Ygritte, Barristan have **zero** family/structural edges in canon. Even Davos (69 canon edges) has 2 family edges vs 8 in the wiki (wife + 7 sons). Redundancy is essentially limited to core-POV sibling/parent pairs.

## 5. Quality spot-check of canonical edges

20 random rows read, 5 evidence_refs verified against `sources/chapters/`: **5/5 verbatim matches at the cited line.** No direction errors, no superseded rows. Minor: ~4/20 affect edges over-type their quote (e.g., `roose-bolton DISTRUSTS ramsay-snow` from a quote showing neither; `tywin COMMANDS tyrion` from the Sansa-wedding scene; `theon DISTRUSTS aeron` from "dismissive") — hint-mapped tier-1 affect edges run a bit hot but `asserted_relation` preserves the original nuance. Reified event edges (948) are structurally fine but lack file:line refs and typed_by. Curator pilot (3 rows) matches schema.

## 6. Verdict

**(a) Salvageable?** Yes — but only one of the three layers, and it isn't really "salvage," it's a never-shipped deterministic product:

- **Infobox-structural: MERGE.** Already parsed, already typed to a 23-type vocabulary architecture.md documents as the wiki-infobox subset of the master vocab (`FIELD_EDGE_MAP` in `scripts/wiki-infobox-parser.py`), 92% target-resolvable, 98.4% additive. Effort: one Python script — slugify via the existing alias-resolver, filter noise targets (~2.5%), quarantine speculative fields (multi-Mother/Father → tier 3 or skip), tag `evidence_kind: wiki-infobox`, `typed_by: python-infobox-map`, cite `wiki:<Page>` + cite_refs where present, confidence tier 2 (tier 1 is earned by verbatim book quotes). Expected yield: **~18-19k edges after filtering.** Days, not weeks; zero LLM spend.
- **Node-file `## Edges` bullets: do nothing.** Same data as infobox-data.jsonl; merging (b) supersedes them. Optionally regenerate display bullets from edges.jsonl later.
- **Prose-comention/entity emits (Sonnet 4,132 + Haiku 2,050 + events-haiku 1,617): leave deprecated.** Real signal exists, but inconsistent schemas, wiki-prose-only evidence, no file:line, comention subset already stamped do-not-promote. Re-validating ~6k rows costs more than the curator/Stage-4 path already producing better edges from book text. Keep as a candidate pool for future curator passes at most.

**(b) Necessary for the agent-query goal? Yes.** Today an agent walks a dense affect/interaction graph over ~1,200 entities and hits a wall at 85% of nodes. Concrete walls: "Who are Walder Frey's children?" (canon: 2 HEIR_TO rows vs 29 children in infobox); "Who is Jon's mother per the wiki?" (nothing); "Which houses are sworn to House Tyrell?" (houses 4.5% connected); any title/succession/culture/geography question (titles 2.6%, locations 5.2%). These are exactly the lookup-shaped questions users ask first. The infobox merge moves overall connectivity **14.7% → 72.2%** (characters 20% → 97%, houses 4.5% → 94%, titles 2.6% → 87%, factions 18% → 70%) — measured by simulation.

**(c) Enrich-now vs dialog-now: do the infobox merge, then go to dialog.** It's the last cheap, deterministic, high-leverage step: one script, ~18-19k edges, +57 points of connectivity, no model risk, consistent with the architecture's existing wiki-infobox edge-type subset. Two small hygiene items to fold in: resolve the 115 orphan endpoint slugs through the alias-resolver, and backfill typed_by/evidence_ref format on the 948 reified rows — both scriptable. After that, the graph is genuinely ready for the agent-traversal phase, and dialog-phase usage will tell you better than another enrichment pass which gaps actually matter.
