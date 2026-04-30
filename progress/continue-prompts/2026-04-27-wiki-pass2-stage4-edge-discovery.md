# Continue Prompt — Wiki Pass 2 Stage 4: Prose-Derived Edge Discovery

**Created:** 2026-04-27 end-of-Session-24 (skeleton; flesh out when Stage 3 finishes)
**Goal:** Discover prose-derived and cross-page edges that infobox-only emission missed. Layer them on top of the existing Python-emitted edges in the node corpus.
**Sequencing:** AFTER Stage 3 (Tier A agent prose-fill complete + Tier B Python skeletons emitted). **Sequential, never parallel** — too much usage to run with Stage 3.
**Status:** Skeleton only. Flesh out the script/agent design when Stage 3 finishes.

## Why this is its own pass (Matt's reasoning, kept verbatim)

> Edge discovery — separate pass, not in priority-bucket script. Reasons:
>
> - Different work shape: priority-bucket is read-only labeling on metadata. Edge discovery reads prose, applies the edge taxonomy, adjudicates conflicts across sources.
> - Different inputs: priority script reads page-index.jsonl + infobox-data.jsonl. Edge discovery reads chapter prose + the 855 existing node bodies + Pass 1 raw entity lists.
> - Different agent: priority script is mechanical Python. Edge discovery wants an LLM pass.
> - The 37 core nodes already have infobox-derived edges in their ## Edges sections (5.83 edges/node mean). What they lack is prose-derived and cross-page edges. That's a real second pass against the same bundles.

So edge discovery is its own workstream that runs sequential to Stage 3.

## Inputs

- The full node corpus in `graph/nodes/{characters,houses,factions,...}/` — all Stage 1 + Stage 3 emitted nodes
- The bucket bundles preserved at `working/wiki-pass2/<bucket_id>/{bucket_input.json, tmp/, validator-report.json}`
- Chapter extractions in `extractions/mechanical/<book>/` — Pass 1 raw entity lists + Relationships Observed sections + Dialogue of Note sections
- Source chapter text in `sources/chapters/<book>/` (read-only; reference only)
- `reference/architecture.md` § "Edge Types" — the controlled vocabulary

## What to find

Edges that the Python infobox extraction couldn't see. Three categories:

1. **Prose-derived edges from a single wiki page** — edges encoded in narrative text rather than infobox. Examples: "Tyrion fought beside Bronn at the Eyrie" (`ALLIES_WITH`), "Varys served Aerys II as spymaster" (`SERVES`), "the Boltons ruled the Dreadfort for thousands of years" (`RULES`). The wiki-ingester captured some of these in the 37 core nodes' prose Allegiances and Narrative Arc sections; this pass formalizes them as edges.

2. **Cross-page edges** — edges that require seeing two pages at once. Stage 3 was bucket-isolated; the agent never saw both endpoints simultaneously. Example: page A says "X was killed by Y"; page B (Y's page) doesn't mention X. The edge `Y KILLS X` is canon but only resolvable cross-page.

3. **Pass-1-derived edges** — edges from chapter extractions that don't appear in any wiki infobox. Examples: perception edges (`PERCEIVED_AS`), emotional edges (`FEARS`, `RESENTS`, `MOURNS`), POV-internal edges (`IGNORANT_OF`, `KNOWS`). These are mostly absent from wiki infoboxes by design — they live in chapter prose.

## Pipeline shape (TBD — flesh out when Stage 3 finishes)

Likely something like:

```
Python: build cross-page edge candidates from track_b_row entity references
   (e.g., page A's Spouse field names page B; emit candidate SPOUSE_OF edge from B's perspective)
   ▼
Python: scan node prose bodies for controlled-vocabulary edge phrases
   (e.g., "served as Hand of the King" → HOLDS_TITLE candidate)
   ▼
Python: scan Pass 1 Relationships Observed tables for edge candidates
   ▼
Agent: for each candidate, read source prose and decide: emit / reject / flag for Matt
   ▼
Patch: append accepted edges to existing nodes' ## Edges sections under "## Edges (prose-derived)" subheading
   ▼
Validator: check no infobox edges were modified (Python-emitted edges are immutable)
```

## Hard rules (carried forward)

- **Python before Agent.** Pre-extract candidates deterministically; agent only reasons over the candidate list.
- **Never modify Python-emitted edges.** They are stable. Prose-derived edges go under a separate subheading or section.
- **Never drop anything from sources.** All bucket bundles, all node files, all chapter files preserved.
- **Sequential, not parallel with Stage 3.** Too much usage.
- **`first_available` not emitted on edges either** — same deferral rule as nodes.

## Out of scope

- Re-extracting infobox edges (Stage 3a owns those, immutable here)
- Modifying any Python-emitted frontmatter
- Pass 3 (voice/perception) — separate workstream, even though it overlaps thematically with PERCEIVED_AS edges
- Pass 4 (foreshadowing) — separate workstream

## To flesh out when Stage 3 finishes

- Concrete script names + script designs
- Candidate generation heuristics (which prose phrases trigger which edge types)
- Agent prompt for the candidate-review pass
- Validator updates for the prose-derived-edge subheading format
- Cost projection and tier prioritization (probably mirror Stage 3's Tier A/B split — only run prose-edge agent on the prose-rich Tier A nodes; Tier B nodes have no prose for the agent to read)

---

## Hybrid plan (drafted Session 26 — Stage 3 now complete; this is the working plan)

Three options were considered:

**A. Pure agent** — read every Tier-A node's prose, extract prose-derived edges, detect cross-identity, surface contradictions. ~1,479 Tier-A nodes × ~$0.05/node = ~$75-100. Wall-clock with 3-5 parallel tabs: 6-10 hours. Carries the same agent failure modes Stage 3b avoided (paraphrase, rate limits, parallel question-ID collisions).

**B. Hybrid (recommended)** — Python preprocessing + agent classification on the survivor set. **This is the chosen design.**

**C. Pure deterministic (no LLM)** — extract markdown links + apply the locked edge vocabulary heuristically. $0, ~5 minutes, but loses cross-identity (Reek=Theon) and prose-implicit edges entirely. Could be a Stage 4.0 sub-step before Stage 4.1 hybrid runs.

### Hybrid design (B)

**Step 1 — Cross-references index (deterministic Python prep, ~30 seconds, $0):**
- Walk every prose file, extract `[text](wiki:Page)` markdown links → `working/wiki-parsed/cross-references.jsonl` rows of `{"source_slug", "target_slug", "anchor_text", "section", "snippet"}`. ~50-150K rows.
- Build inverted index → `working/wiki-parsed/backlink-counts.json`: `{"<target_slug>": {"in_count": N, "out_count": M, "ratio": N/M, "sample_sources": [...]}, ...}`.
- Use cases: pagerank-lite importance signal, asymmetric reference detection, disambiguation by frequency, candidate-edge scoring, query-time relevance ranking.
- Status: **BUILT in Session 26** — see `scripts/wiki-pass2-build-cross-refs.py`.

**Step 2 — Candidate edge generation (deterministic Python, ~30 seconds, $0):**
- For every cross-reference row, check if an edge of any type already exists between source_slug and target_slug in their respective `## Edges` sections.
- If yes → drop (already-known edge).
- If no → emit `working/wiki-pass2/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl` row of `{"source", "target", "anchor_text", "section", "snippet", "backlink_count": <target's in_count>}`.
- Filter targets not in graph (broken wiki links → drop, log to summary).
- Filter low-confidence candidates: `target.in_count < 2` AND `source.section in {Quotes, Notes}` → drop (probably trivia mention, not a real edge).
- Survivor set estimate: 5K-15K candidates after filtering vs. ~30K naïve pass.

**Step 3 — Agent classification (LLM, ~2-4 hours wall-clock with 3 parallel tabs, ~$50-100):**
- Bucket-by-bucket: agent reads `<slug>.candidates.jsonl` + the source slug's prose file + (for cross-identity) target candidates' frontmatter (aliases, type).
- For each candidate, decide: (a) emit edge with `edge_type` from the locked vocabulary, (b) reject as not-an-edge (just-a-mention), (c) flag as cross-identity (`SAME_AS` candidate), (d) escalate to questions-for-matt.
- Emit `working/wiki-pass2/<bucket>/prose-edges/<slug>.edges.jsonl` (matches the artifact-format-by-consumer pattern in architecture.md). Single-writer-per-file: agent never touches existing nodes.

**Step 4 — Promote prose-edges to nodes (deterministic Python, $0):**
- Append accepted edges to nodes under a `## Edges (prose-derived)` subheading (separator from Python-emitted infobox edges, which remain immutable).
- Atomic-rename pattern same as Stage 3-promote.

**Cost projection:** ~$50-100 total, 3-5 hours wall-clock. ~10× cheaper and ~2× faster than pure-agent design.

### Hard dependency on Pass 1

Stage 4's contradiction-surfacing component wants Pass-1-derived chapter mentions to cross-check against wiki claims. **Pass 1 is only complete for AGOT** as of Session 26. Two paths:

- **Stage 4 v1 (recommended):** AGOT-only contradiction sweep + full-corpus prose-edge discovery + full-corpus cross-identity detection. Ships in 3-5 hours, ~$75.
- **Stage 4 v2 (later):** Re-run contradiction sweep against ACOK/ASOS/AFFC/ADWD as Pass 1 completes those books. Each book back-fill: ~$10-20.

### Recommendation when starting Stage 4

1. Run cross-references index first (already built — re-run if prose has changed).
2. Inspect backlink-count distribution before designing the candidate filter (centrality of the corpus is empirical — let the data drive the threshold).
3. Build candidate generation script (Step 2) and test on one bucket.
4. Brief the wiki-ingester-style agent for prose-edge classification — DIFFERENT role from Stage 1's wiki-ingester (no node authoring, just edge classification).
5. Run on Tier-A nodes only for v1; defer Tier-B prose-edge discovery (those nodes have less prose anyway, lower yield per token).
6. Promote in a separate Python step. Validator update: enforce that infobox edges are unchanged before/after prose-edge promotion.

Same Python-before-Agent discipline as Stage 3.
