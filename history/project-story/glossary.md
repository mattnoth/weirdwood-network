# Glossary — The Weirwood Network's Internal Vocabulary

> Part of the [project-story series](00-overview.md). The project's working documents are dense
> with internal shorthand — Passes, Stages, Plates, Tracks, three different things called "Tier,"
> and two different things called "Stage 4." This file decodes all of it for a reader with no
> project context, organized by category.

## The books and sources

**AGOT / ACOK / ASOS / AFFC / ADWD** — The five published *A Song of Ice and Fire* novels: *A Game of Thrones*, *A Clash of Kings*, *A Storm of Swords*, *A Feast for Crows*, *A Dance with Dragons*. Split into 344 chapter files total (73 / 70 / 82 / 46 / 73).

**D&E** — The three *Dunk & Egg* novellas (prequel stories), split alongside the novels as additional source text.

**TWOIAF** — *The World of Ice and Fire*, the in-universe history book. Ingested as a non-narrative reference source.

**AWOIAF** — *A Wiki of Ice and Fire* (awoiaf.westeros.org), the fan-maintained encyclopedia. The project crawled all 17,945 of its pages once, in April 2026, into a local cache at `sources/wiki/_raw/` — and has a hard rule never to fetch from it again.

**Chapter files** — The unit of book text: one markdown file per chapter with YAML frontmatter, named `{book}-{pov}-{number}.md` (e.g., `agot-bran-01.md`). Every book citation in the graph ultimately points into one of these files.

## The pipeline: the six Passes

The original architecture defined six extraction passes over the source text. Only the first two exist; 3–6 are stubs.

**Pass 1 — Mechanical extraction (DONE).** An agent reads each chapter and fills out structured tables: who appears, who relates to whom, food and hospitality, physical descriptions, events. Ran on Opus across all 344 chapters (~$234). Its tables later became the primary source for the edge layer — the project's highest-ROI purchase.

**Pass 2 — Wiki ingestion (DONE).** Promoting the crawled wiki cache into graph nodes. Started as an expensive agent pipeline, finished as a mostly-Python one. Produced ~7,500 of the graph's ~8,263 active nodes (excl. `_conflicts/` staging).

**Pass 3 — Voice analysis (stub).** Planned character voice profiles and cross-POV perception. Never built.

**Pass 4 — Foreshadowing scan (stub).** Planned mapping of foreshadowing to a curated event list. Never built.

**Pass 5 — Theory extraction (stub).** Planned theory-informed pattern extraction. Never built. (Passes 4–5 are why the theory/prophecy corner of the graph is still dark.)

**Pass 6 — Discovery (stub).** Planned open-ended pattern hunting. Never built.

## "Stage" — warning, the word collides

Two completely different things were called "Stage" in different eras. This trips up every reader of the history.

**Pass 2's internal Stages 0–4 (April–May).** The wiki-promotion pipeline's steps: Stage 0/1 triaged wiki pages into buckets and ran agents over the core ones (855 agent-written nodes, the cost blowout); Stage 2 was the cold review that returned "remediate" and triggered the Python-first pivot; Stage 3 was the deterministic Python promotion (3,314 nodes in ~30 seconds for $0); Stage 4 — *in this numbering* — meant "edge enrichment," the step after node promotion.

**"Stage 4" the era (May 13 onward).** The name detached from Pass 2 and became shorthand for the whole prose-edge-classification effort: LLMs reading evidence and typing edges (first from wiki comentions — deprecated — then from Pass 1 tables, then Events). Scripts, skills, and memory entries named `stage4-*` belong to this era, not to Pass 2's step list.

## Plates 0–5 (the reification merge sequence)

The June edge-modeling era staged its changes as numbered "plates," applied in a fixed order, with everything held out of the canonical graph until the final one:

- **Plate 0** — direction normalizer: flip edges whose subject/object were backwards (grammatical-subject leakage), plus node repoints.
- **Plates 1–2.5** — head-rule and schema fixes: retype miscategorized events, merge high-confidence duplicate nodes, apply drift retypes.
- **Plate 3** — the big mint: 217 new event hub nodes plus 897 role edges connecting participants to them.
- **Plate 4** — cluster layer: SUB_BEAT_OF edges linking beats to parent events, built using the NO-GO'd Events-Haiku output as input (~$35).
- **Plate 5** — the single gated merge that wrote all staged work into `edges.jsonl` (shipped June 9: edges 3,811 → 4,757, event nodes 371 → 583).

## Tracks (three unrelated uses)

**Wiki-era Track A / Track B (late April).** Two parallel work streams: Track A = update the Pass 1 extractor prompt and keep extracting books; Track B = build the wiki infobox parser. The April 25 decision to do Track B first is why the infobox data exists.

**Backfill Tracks A/B/C (June, post-Plate-5).** Three scoped cleanup tracks gated on what Mode 3 reveals: Track A = vocab-drift retyping (deterministic dictionary first, Haiku fallback); Track B = reifying more existing edges into event hubs (absorbs the shelved Events-Haiku rows); Track C = retroactive direction-flip cleanup beyond Plate 0's ten flips. Budgeted ~$25–75 total.

**Track W.** A candidate task to extend the infobox-field→edge-type map to fields the parser doesn't yet map (`dynasty`, `vassal`, `cadet branch`…). Pure Python, folded into infobox-merge territory.

## "Tier" — three different tier systems

**Confidence tiers 1–5 (on facts/edges).** How much to trust a claim: Tier 1 = verified canon, earned only by a verbatim book quote; Tier 2 = strongly supported (wiki-infobox edges land here); Tier 3 = plausible inference; Tier 4 = speculation; Tier 5 = crackpot. Every node and edge carries one.

**Wiki page tiers (for promotion).** A triage ranking of the 17,945 wiki pages by importance: tier-core (the 37 buckets that got full agent treatment), tier-secondary, and tier-3 (the long tail, promoted by Python). About *which pages get how much attention*, not about truth.

**Qualifier-vocab Tiers 1–3 (on edge types).** A validation strictness level assigned to each edge type's qualifier field: Tier 1 = qualifier required and must match a closed enum (e.g., PARENT_OF must say biological/adoptive/step/claimed); Tier 2 = optional, but must match the enum if present; Tier 3 = free text, no check (most emotional/spatial types). Part of the vocab lockdown.

## Modes 1–4 (the validation track)

How the finished graph gets tested, scoped in Session 88: **Mode 1** = capability validation (do probe queries against the new structure work?); **Mode 2** = canonical accuracy (fact-check edges against the books); **Mode 3** = agent grounding — the real goal: give an agent the graph as a query tool and have it answer genuine ASOIAF questions / ground dialog; **Mode 4** = surprise/discovery (aggregate queries that were impossible before reification). Mode 1 ran in Sessions 89–91; Mode 3 is next, after the infobox merge.

## Work units and cadence

**Session** — One Claude Code conversation. The project ran 91 of them (S0–S91), each starting amnesiac and rebuilding context from the worklog.

**Worklog** (`worklog.md`) — The authoritative living state file: current status, active decisions, and the 5 most recent session entries (older ones archive out in blocks of 5). When any other document disagrees with the worklog, the worklog wins — a rule written in blood after several stale-state incidents.

**Continue prompt** — A self-contained resumption document for a specific work track, written so a fresh agent can pick up the work cold. Lives in `progress/continue-prompts/`.

**/endsession** — The end-of-session checklist skill: update the worklog, archive old entries, write continue prompts, commit. Has its own hard rule: never run it without Matt's explicit permission.

**Bucket** — Pass 2's work unit: a cluster of related wiki pages (e.g., "Direwolves") processed together by one agent run. 536 bucket workspaces exist; 37 "core" buckets got the full agent treatment.

**Wave** — Pass 1's work unit: a batch of chapters launched together, tracked wave-by-wave in the progress logs.

**Mission / watcher / worker** — A protocol for longer multi-agent jobs: a *mission* defines the goal, *workers* execute pieces, a *watcher* (Opus-locked) monitors and intervenes. Used about three times (notably the case-collision page reconstruction), dormant since mid-May.

## Safety and discipline vocabulary

**Python before Agent** — The project's defining rule (instituted Session 24): if a deterministic script can produce part of an output, it runs first; LLMs only do what genuinely requires reasoning. Saved ~$1,200 the day it was born and several thousand since.

**Smoke before spend** — No bulk LLM run launches without a small sample run ("smoke") measured against a precision gate first. Held at least five times; the smokes themselves cost ~$11 and blocked ~$600 of bad bulk spend.

**NO-GO gate** — A pre-committed precision threshold a smoke or audit must clear before bulk spend or promotion. A failed gate means the output is parked, not merged — even when the run itself was flawless (see Events-Haiku).

**Vocab lockdown** — Closing every surface where an LLM could freestyle: a locked list of edge types (163 at the end of the comention era; 166 today after reification added `AGENT_IN`, `VICTIM_IN`, `SUB_BEAT_OF`), qualifier enums, no free-text notes field, fixed schemas. Built painfully after Haiku's pre-lockdown smoke failed at ~80%; afterward Haiku ran at ~3–4% violations.

**Head rule** — The Pass-1/Plate-1 convention for which entity is an edge's source ("head") vs. target: the head is always the **semantic agent** (the entity doing or initiating the action), never the grammatical subject of the sentence and never the POV character. Added to the Pass 1 extractor prompt at Plate 1 to prevent the grammatical-subject leakage that produced backwards edges like `cressen KILLS melisandre`. See [06 — Reification, Explained](06-reification-explained.md).

**Drift detection** — Mechanical validators plus cross-model audits that catch an LLM's output schema or semantics shifting mid-run (which happens even with identical prompts). Mandatory on every bulk run; failures halt the run via exit codes.

**Cross-model / fresh-eyes audit** — Having a different model, or a subagent with no conversation context, re-check conclusions. Corrected the orchestrator's own errors at least seven times in 91 sessions.

## Graph anatomy

**Node** — One entity, one markdown file (`{name}.node.md`) under `graph/nodes/{type}/`. 8,263 of them (excl. `_conflicts/` staging) across characters, locations, houses, events, artifacts, titles, factions, theories, prophecies, and more.

**edges.jsonl** (`graph/edges/edges.jsonl`) — The canonical edge layer: one JSON row per typed relationship (4,760 rows), each carrying source, target, edge type, confidence tier, and evidence. The project's central deliverable.

**evidence_kind** — A field stamping where an edge's evidence comes from. Current values: `book-pass1` (3,809 — from Pass 1 tables), `book-pass1-reified` (897 — role edges from reification), `plate4-wiki-cluster` (51), `book-curator` (3 — hand-curated pilot). The infobox merge adds `wiki-infobox`.

**Spine vs tail** — The two halves of the original edge build: the *spine* is the 2,834 edges whose types could be derived deterministically from Pass 1 tables ($0); the *tail* is the 2,385 ambiguous rows an LLM typed afterward ($20.88).

**Pass 1 "Relationships Observed" tables** — The section of each Pass 1 chapter extraction listing observed relationships with supporting quotes. 7,348 first-party rows; the raw material the entire edge layer was mined from.

**Comention** — Two entities appearing near each other in wiki text, used as an edge *candidate* signal. The basis of the deprecated Stage-4 wiki track: 29,259 candidate pairs that proved structurally too noisy versus Pass 1's first-party observations.

**Trigger table** — The original architecture's index layer: a lookup table mapping mentions/triggers in text to entities, sitting alongside the graph (the "two-layer" design). Realized in practice as the mention and entity indexes under `index/`.

**Alias resolver** — The deterministic mapping from name variants ("the Imp," "Dany") to canonical node slugs. Built from wiki redirects and infobox data; load-bearing for everything that resolves names.

**Slug** — An entity's kebab-case identifier (`jon-snow`, `brienne-tarth`), used as the join key between nodes, edges, and indexes.

**Reification / event hub / role edge / SUB_BEAT_OF** — The June restructuring: instead of flat character→character edges trying to encode events ("X kills Y at Z"), events become their own *hub* nodes, and *role edges* (AGENT_IN, VICTIM_IN, GUEST_OF…) connect participants to the hub; SUB_BEAT_OF links a small beat to its parent event (the Red Wedding has 8). Full explainer with the Red Wedding worked example: [chapter 06](06-reification-explained.md).

**`first_available` (spoiler gating)** — A planned per-node/per-edge field marking the earliest book where a fact is known, so queries could avoid spoiling later books. Declared "architectural, not optional" on day one; reversed to "deferred, backfill later by script" in Session 24. Still deferred.
