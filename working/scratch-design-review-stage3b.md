# Design Review Request — Replace Stage 3b Agent with Python Prose Extractor

**Created:** 2026-04-27 (Session 26 mid-design)
**For:** A fresh Claude instance with no conversation context
**Goal:** Second opinion on a proposed design shift. Tell me what I'm missing.

---

## TL;DR

We're mid-design for **Stage 3b** of the Weirwood Network's wiki ingestion pipeline. The original plan was an LLM agent that reads cached wiki HTML and synthesizes prose body sections (`## Origins`, `## Allegiances`, etc.) onto skeleton node files. I'm now proposing to replace that agent with a deterministic Python script that extracts wiki section prose by HTML header mapping.

**The question I want your second opinion on:** Am I throwing away something important? Where does agent reasoning genuinely belong in this pipeline that I might be misallocating to a script?

I'm aware of confirmation bias — I've been arguing for this shift for an hour and want a check from someone who hasn't been in the conversation.

---

## Project Context (necessary background, terse)

**What we're building:** A queryable knowledge graph for *A Song of Ice and Fire*. Source material: the AWOIAF fan wiki (17,945 pages cached locally at `sources/wiki/_raw/`) and the books themselves. Output: typed nodes (characters, houses, locations, etc.) connected by typed edges (`SPOUSE_OF`, `SWORN_TO`, `BORN_AT`, etc.) suitable for spoiler-gated traversal queries.

**Pipeline (relevant slice):**
- Pass 1 — mechanical extraction from book chapters (separate track, in progress)
- **Pass 2 — wiki ingestion (the focus here)**
  - **Stage 1 — "core" tier:** 37 buckets, 855 nodes, agent-driven, **complete and promoted to `graph/nodes/`**. Done in Sessions 19-23.
  - **Stage 2 — cold review of Stage 1 output:** decision was "remediate" (spoiler-gating schema drift), but Matt overturned same-session — spoiler gating deferred to post-release backfill. Done Session 24.
  - **Stage 3 — "secondary" tier:** 472 buckets, ~3,315 pages. The current design effort. Split into:
    - **Stage 3a — skeleton emission (Python):** Frontmatter + thin `## Identity` + full `## Edges` derived from wiki infoboxes via the deterministic parser at `scripts/wiki-infobox-parser.py`. **Just completed this session.** 3,315 skeletons in `working/wiki-pass2/<bucket>/skeleton/<slug>.node.md`. $0 cost, 60 seconds wall-clock.
    - **Stage 3b — prose fill (THE DESIGN QUESTION):** Add `## Origins`, `## Allegiances` (narrative), `## Appearances & Description`, `## Narrative Arc`, `## Quotes`, `## Notes` sections to each skeleton.
    - **Stage 3-promote — concat skeleton + prose → `graph/nodes/<type>/<slug>.node.md`:** Atomic-rename from staging, deterministic Python.
- Stage 4 — prose-derived edge discovery (separate, future, agent-required — see below)

**Hard rules** (these are inviolable):
- The wiki cache is local at `sources/wiki/_raw/`. **No HTTP calls, ever.** No `WebFetch`, no `curl`, no `requests`. The Playwright scraper has been archived.
- The edge vocabulary is **locked** at `scripts/wiki-infobox-parser.py::FIELD_EDGE_MAP`. Any new edge type goes through `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" first, then the parser. No script and no agent invents edge types ad-hoc.
- `first_available` (spoiler gating) is **deferred** to a post-release backfill script. Agents and scripts do not emit, derive, or reason about this field.
- Don't modify `graph/nodes/**/*.node.md` — those are Stage 1 promoted nodes, immutable from Stage 3's perspective.

---

## The Original Stage 3b Plan (the one we're considering replacing)

A new prose-only LLM agent (`.claude/agents/wiki-ingester.md` v2) that:
- Reads each skeleton in `working/wiki-pass2/<bucket>/skeleton/<slug>.node.md`
- Reads the cached wiki HTML at `sources/wiki/_raw/<Page>.json`
- Writes `working/wiki-pass2/<bucket>/prose/<slug>.prose.md` containing the appended prose sections
- Forbidden from emitting `## Edges`, modifying frontmatter, or modifying `## Identity` (which the validator would enforce)
- Runs only on Tier-A pages (~624 pages — Tier-B skeleton-only). Tier promotion via `scripts/wiki-pass2-prioritize.py` (already built and applied).

**Cost:** ~$70 agent cost, ~6 hours wall-clock with 3 parallel orchestration tabs. Subject to rate limits. Subject to the "agent paraphrases or invents content" failure mode.

**Why this was the plan:** Stage 1 used an agent. Defaulting to "another agent for Stage 3b" was inertia, not analysis.

---

## The Proposed Replacement

A new Python script `scripts/wiki-pass2-extract-prose.py` that:
- For every page in Stage 3a's output (Tier-A AND Tier-B — the script is cheap, no reason to artificially restrict to Tier A):
  - Reads `sources/wiki/_raw/<Page>.json` (BeautifulSoup-parseable HTML wrapped in JSON)
  - Walks `<h2>` / `<h3>` headings
  - Applies a deterministic mapping table:
    - Wiki section `Background` → our `## Origins`
    - Wiki section `Appearance and Character` → our `## Appearances & Description`
    - Wiki section `Recent Events` → our `## Narrative Arc`
    - Wiki section `Quotes` → our `## Quotes`
    - Wiki section `Behind the Scenes` → SKIP (publication meta)
    - Unknown section → SKIP or land in `## Notes` (TBD)
  - Translates `<sup id="cite_ref-...">` tags → our `(wiki:Page.cite_ref-X)` citation format
  - Strips publication-meta paragraphs and TV-only content (skip-list already exists in the infobox parser)
  - Writes `prose/<slug>.prose.md` starting with `## ` and a whitelisted heading
- Tier-B pages get prose extraction same as Tier-A (NOT artificially deferred — script is free)
- Promotion concatenates `skeleton + "\n" + prose` (or just `skeleton` if prose missing) → `graph/nodes/<type>/<slug>.node.md`

**Cost:** $0. ~2-5 minutes wall-clock for all 3,315 pages. No rate limits. No agent failure modes.

---

## Where Agent Reasoning Genuinely Belongs (and Why It's NOT Stage 3b)

We've identified that **Stage 4** is where reasoning is required:
- **Cross-identity detection** (Reek IS Theon, Alayne IS Sansa, Mance Rayder's son IS Aemon Steelsong) — requires reading prose, understanding the disguise/swap, emitting `SAME_AS` edges
- **Cross-page edge discovery** — relationships in prose that the source page's infobox didn't capture but a related page's prose mentions
- **Contradiction surfacing** — when the wiki contradicts a Pass 1 chapter extraction
- **Disambiguation reasoning** — three Aegons, which is which on a page that mentions "King Aegon"

Stage 4 stays an agent because these tasks require *reasoning*, not extraction. Stage 3b doesn't have any of those tasks — Stage 3b is "copy this section of the HTML to this section of the markdown, with citation translation." That's mechanical.

---

## Things the Agent Was Supposed To Do That the Script Can't

I want to honestly enumerate these so you can tell me which ones are real concerns:

1. **Compress verbose wiki prose to 200-400 words.** Wiki "Recent Events" sections can be 1,500-3,000 words for major characters. Original plan: agent compresses. Proposed: don't compress. Accept verbose prose. Truncation is a query-time concern (preview = first paragraph; full = on-click). **Counter-counter:** maybe verbosity hurts graph readability or downstream LLM-context budget when a future query agent needs to read 100 nodes. **My response:** truncate at query-time, not ingest-time. Cheaper to keep full content and trim than to lose content and never recover it.

2. **Editorial framing — "the narrative arc" vs background trivia.** Wiki sections include filler. Original plan: agent decides what's signal. Proposed: take it all, let downstream filtering handle. **Counter-counter:** noise pollutes traversal results. **My response:** the noise is in `## Narrative Arc` prose, not in `## Edges`. Edges are the traversal substrate. Prose is the human-readable annotation. Verbose prose annotation is fine.

3. **Phrase prose so it doesn't restate `## Edges` as bullets.** Wiki prose often restates relationships in sentence form ("Eddard's wife Catelyn..."). The original plan was agent-rewrites-to-avoid-redundancy. **Proposed:** allow restatement. The reader sees `## Edges` and prose in different rendering contexts; restatement is fine. **Counter-counter:** noise. **My response:** see above.

4. **Skip "Behind the Scenes" / publication-meta sections.** Script can do this — it's a static skip-list of section names. Already partially solved in the existing infobox parser.

5. **Cite_ref translation.** Mechanical. Script can do this. The HTML structure is regular: `<sup id="cite_ref-NAME-N">[N]</sup>`. Translate to `(wiki:Page.cite_ref-NAME-N)`.

6. **Cross-identity detection (Reek=Theon).** Originally Stage 3b's job. Now Stage 4's job. **Counter-counter:** if Stage 3b was going to flag these, deferring to Stage 4 means Stage 3b nodes don't have `same_as` set. **My response:** correct, that's deferred. v1 won't have cross-identity links until Stage 4 runs. We're not closing the door — Stage 4 can edit promoted nodes' frontmatter to add `same_as` later.

---

## What We Lose

1. **Style consistency with Stage 1's 855 already-promoted nodes.** Stage 1 nodes have agent-synthesized terse prose; Stage 3 nodes will have deterministic-extracted verbose prose. Visible mismatch. **Mitigation:** post-Pass-2 retroactive re-extraction of Stage 1 prose using the same Python extractor. Defer.

2. **Cross-identity / disambiguation handled at Stage 3 time.** Now Stage 4. **Mitigation:** explicit Stage 4 design.

3. **Per-page editorial judgment about what's "important."** Now we capture everything (or nothing if section doesn't match the table) and rely on query-time filtering.

---

## What We Gain

- **$0 cost, minutes vs hours.** Order-of-magnitude.
- **Determinism.** Re-running produces byte-identical output. Fully reproducible.
- **No agent failure modes:** no paraphrase risk, no rate limits, no question-ID collisions, no validator-byte-equality logic, no agent prompt maintenance, no parallel-orchestration coordination.
- **Tier B included free.** Original plan deferred Tier B; new plan covers all 3,315 pages.
- **Single-writer-per-file invariant.** Skeleton owned by Python (Stage 3a). Prose owned by Python (Stage 3b). Final node owned by launcher (concat at promotion). No file has two writers competing.

---

## Open Design Questions Where I Want Your Opinion

1. **Wiki-section-to-schema mapping** — will a static header table cover ~enough of the wiki's section variability, or will fallback logic be needed? Spot-check a few pages of varying entity types if you can. Pages: `Eddard_Stark.json`, `House_Stark.json`, `Winterfell.json`, `Battle_of_the_Bastards.json`, some random secondary character. Look at their `<h2>` structure. Does our six-section schema map cleanly?

2. **Verbose-but-cited prose vs. terse-and-summarized.** Am I making the right tradeoff for v1? The use cases I imagine: (a) traversal queries that surface 5-10 connected nodes — short previews fine, full prose on-click. (b) future agent that reads 50 nodes to answer a question — could care about length. Anything else I'm missing?

3. **Style mismatch with Stage 1 nodes.** Real concern or cosmetic?

4. **Cross-identity deferral to Stage 4.** Is Stage 4 the right home for `SAME_AS` discovery, or should Stage 3b retain that even if everything else moves to Python?

5. **Is there ANYTHING in Stage 3b's original responsibility set that you think genuinely requires reasoning that a script can't do?** I want a check on whether I'm over-correcting toward Python.

6. **Anything else I'm missing.** Failure modes I haven't considered. Future-pipeline considerations. Architectural concerns.

---

## Where to Read for Context

If you have time and want to validate the design against the actual repo state:

- `CLAUDE.md` — project orchestrator instructions, pipeline overview
- `reference/architecture.md` — data model: entity types, edge types, confidence tiers, naming conventions, **plus the new "Wiki Infobox Fields → Edge Type Mapping" lock callout block**
- `reference/architecture.md` § "Artifact Formats by Consumer" — TODO this session, will land before you're called
- `working/runbooks/wiki-pass2-pipeline.md` — canonical Stage 3 pipeline doc
- `scripts/wiki-infobox-parser.py` — the deterministic infobox parser; produces `working/wiki-parsed/infobox-data.jsonl`. Note its `FIELD_EDGE_MAP` (the locked vocabulary) and `ENTITY_TYPE_OVERRIDES` (added this session for misclassified "houses" like Night's Watch).
- `scripts/wiki-pass2-emit-deterministic.py` — Stage 3a; emits skeleton files. Produced 3,315 nodes already.
- `scripts/wiki-pass2-prioritize.py` — applies Tier-A/B/C labels per page.
- `working/wiki-pass2/houses-other-h-w/skeleton/*.node.md` — sample Stage 3a output (14 nodes).
- `graph/nodes/characters/eddard-stark.node.md` — sample Stage 1 promoted node (agent-authored, for the prose-style comparison).
- `working/todos.md` § "Edge taxonomy gaps surfaced by Track B" — the unmapped infobox fields list (informational, not blocking this design).

**Do NOT read:** `sources/raw/`, `sources/chapters/` (gitignored copyrighted content). `graph/nodes/_conflicts/` (Stage 1 cleanup, irrelevant).

**Do NOT do:** Re-fetch the wiki (it's local, see CLAUDE.md hard rule). Modify any existing graph/nodes/ file. Modify any manifest's `priority` field. Run any extraction.

---

## What I'd Like Back From You

A short verdict (≤300 words) covering:
1. Sound or unsound? Why.
2. Most important consideration I missed (if any).
3. Specific concrete recommendation if you'd change the design.

Don't research the entire codebase — read 3-5 of the listed files and form a judgment from there. I value crisp opinion over thoroughness.
