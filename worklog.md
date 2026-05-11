# The Weirwood Network — Project Worklog

> **Purpose:** This is the living history of the project. Every Claude Code session should read this file to understand what has been done, what decisions have been made, what's in progress, and what's queued. Update this file at the end of every work session.
>
> **Convention:** Newest entries at the top. Each entry is dated and tagged with what was done.

---

## How To Use This File

### For Claude Code Agents
Load this file alongside `reference/architecture.md` at the start of every session. Before doing any work:
1. Read the **Current State** section to understand what exists
2. Read the **Active Decisions** section for unresolved design questions
3. Read the **Ideas & Backlog** section for queued work
4. Check the **Session Log** for what happened recently

After completing work, update:
- **Current State** to reflect what now exists
- **Session Log** with a new entry describing what was done
- **Active Decisions** if new questions arose
- **Ideas & Backlog** if new ideas or tasks surfaced

### For Matt
This is your project memory. When you come back after a break, read Current State and the last few Session Log entries to get back up to speed. Add ideas to the backlog whenever they occur to you, even outside of Claude Code sessions.

---

## Current State

### Infrastructure
- [x] Repository initialized
- [x] project-context.md in place (master architecture spec)
- [x] CLAUDE.md in place (orchestration guide)
- [x] Directory structure created (sources/, extractions/, graph/, index/, curation/, reference/, scripts/)
- [x] Source .txt files moved to sources/raw/
- [x] Subagent definitions in .claude/agents/ (2 full: mechanical-extractor, script-builder; 5 stubs: wiki-ingester, voice-analyzer, foreshadowing-scanner, theory-extractor, discovery-agent)
- [x] Custom slash commands (.claude/commands/endsession.md, continue.md)
- [x] Working directory with progress.md + todos.md
- [x] Reference files organized (reference/architecture.md, foreshadowing-events.md, pov-characters.md)
- [x] Chapter splitter script written (`scripts/chapter-splitter.py`)
- [x] Chapter splitter tested on one book (AGOT: 73/73)
- [x] All five books split into chapter files (344 total: AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73)
- [x] Wiki scraper script written (`scripts/wiki-scraper.py`) — migrated from urllib to Playwright for Cloudflare bypass
- [x] Wiki scraper extended with `--mode all` + `--limit N` for full unattended crawl
- [x] Wiki directory structure created (`sources/wiki/`) — now fully gitignored
- [x] Full-crawl runbook drafted and updated for Playwright (`working/runbooks/wiki-full-crawl.md`)
- [x] Full wiki crawl executed (17,945/17,952 pages succeeded, 377 MB on disk)
- [x] Taxonomy candidates template created (`working/taxonomy-candidates.md`)
- [x] POV reference table corrected (6 missing chapter headings added)
- [x] D&E novellas split into chapter files (3 total: THK 1, TSS 1, TMK 1 — each novella is one continuous chapter)
- [x] TWOIAF OCR'd and extracted to plaintext (179K words, 164MB OCR'd PDF)
- [x] ocrmypdf + poppler installed (Tesseract, Ghostscript, pdftotext)

### Extraction Pipeline
- [x] Pass 1 agent prompt v1 (draft complete — `agents/pass-1-mechanical.md`)
- [x] Pass 1 v1 run on AGOT (73/73 chapters, archived to `extractions/archives/agot-v1/`)
- [x] Pass 1 agent prompt v2 — added: Physical Environment, Character Appearances, Food & Drink, Hospitality & Guest Right, Location Descriptions, Spatial Layout & Movement, time_markers, direwolves/dragons-as-characters rule
- [x] Pass 1 v2 run on AGOT (73/73, archived to `extractions/archives/agot-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v2 run on ACOK (50/70, archived to `extractions/archives/acok-v2/` — 4-category Raw Entity List)
- [x] Pass 1 v3 prompt update: expanded Raw Entity List to 12 categories (10 + Other catch-all), added strict formatting rules (all headers required, no merging/renaming, "None" for empty categories)
- [x] Pass 1 v3 run on AGOT (73/73 — complete)
- [x] Pass 1 v3 run on ACOK (70/70 — complete)
- [x] Pass 1 v3 run on ASOS (82/82 — complete; Okey ran in parallel on shared Max account, branch `pass1-asos-extraction`)
- [x] Pass 1 v3 run on AFFC (46/46 — complete)
- [x] Pass 1 v3 run on ADWD (73/73 — complete)
- [ ] Pass 1 on Tales of Dunk and Egg (THK, TSS, TMK) — **deferred (enrichment pass for main-arc nodes)**. D&E content will eventually enrich existing main-arc Targaryen-prehistory nodes (Bloodraven, Egg/Aegon V, etc.) but is not on the active critical path. Not dropped, not urgent. Decision 2026-05-06 (Session 37 Q11=b).
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki/data/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [x] AGOT/ACOK supplementary entity index — OBSOLETED 2026-04-25. v3 prompt captures all 12 categories directly; backfill index no longer needed. See `working/todos.md` line ~245.
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 3c — audit cleanup (Session 27; 4 audits run, 6 parser bugs fixed, 484 nodes re-emitted across multiple targeted runs. Tier 3 promotion campaign Passes A-D + E Phase 1 added 769 new nodes. Cat 1 orphan edges 7,784→2,955 (62% drop). Stale religion-bleed 0. Edge vocabulary lock holds.)
- [x] Wiki Pass 2 Path B — categorizer extension + promotion campaign (Session 28; bounded MediaWiki categories backfill + parser CATEGORY_TYPE_MAP. `unknown` 12,434 (70.4%) → 2,118 (12.0%). +2,240 graph nodes (5,008 → 7,248). Cat 1 orphan edges 2,955 → 1,973. 5 new dirs bootstrapped: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`. New entity type `object.food`.)
- [x] Wiki Pass 2 Path B promotion completion + schema-drift audit (Session 29; 4 new entity types added: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. 4 new dirs: `materials/`, `languages/`, `medical/`, `customs/`. `unknown` 2,098 → 1,257. Net +315 graph nodes (7,248 → 7,563). 130 stale-dir mismatches cleaned. Full schema-drift audit on opus: 0 HIGH / 4 MED / 4 LOW. Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary lock holds. Chronology data extracted from 74 year pages: 2,245 events in `working/wiki/data/chronology-events.jsonl` (awaits v2 temporal-edges schema; not graph edges yet).)
- [x] Wiki Pass 2 Stage 0 foundation — alias-resolver built + run (Session 26). 707 broken refs reclaimed via slug-mismatch fix. Empirical signal validates that most remaining "broken" refs are genuinely missing concept entities (concept-pages decision: defer).
- [ ] Wiki Pass 2 Stage 4 — prose-derived edge discovery (Stage 0 prep complete + cross-references index built; Stage 4 hybrid plan documented in `working/agent-fleet-specs/fleet-orchestration-plan.md`. Pass 1 dependency now met (344/344 across 5 books). Need to build: edge-candidate-generator script, then prose-edge-classifier agent runs (full prompt ready in `.claude/agents/prose-edge-classifier.md`), then peer review, then promote. Continue prompt: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`)
- [ ] Pass 3 voice/perception agent prompt written
- [ ] Pass 4 foreshadowing agent prompt written
- [ ] Pass 5 theory-informed agent prompt written
- [ ] Pass 6 discovery agent prompt written

### Index & Graph
- [ ] Trigger table v1
- [ ] Entity index
- [ ] Chapter index
- [ ] Graph edges formalized
- [ ] Convergence maps

### Reference Materials
- [x] Foreshadowing events list (`reference/foreshadowing-events.md`)
- [ ] Theory seeds file
- [ ] Taxonomy reference doc
- [x] Architecture spec (original outline exists, needs refinement)

---

## Active Decisions

> Design questions that need resolution. Tag with status: OPEN, DECIDED, DEFERRED.

### OPEN: Storage Format — Pure Markdown vs. Graph DB
- **Question:** Does the graph live as pure markdown files with edges represented as YAML/frontmatter references, or do we use a lightweight graph DB (Neo4j, SQLite with graph extensions)?
- **Leaning:** Start with pure markdown. The context base pattern works well for agentic access. Graph DB can come later if query complexity demands it.
- **Trade-off:** Markdown is portable, version-controlled, and readable by Claude Code natively. Graph DB gives real traversal queries but adds infrastructure.

### DECIDED: Wiki Ingestion Scope — Full Crawl, Then Triage
- **Decision (2026-04-13):** Scrape the entire AWOIAF wiki once (~17,952 pages, ~5–6 hrs, ~1–2 GB), store as a *reference layer* in `sources/wiki/` (gitignored). Pass 2 (wiki-ingester) decides what gets promoted into `graph/nodes/` with proper `first_available` spoiler tags.
- **Rationale:** Targeted scraping required us to predict relevance up front. Full crawl is a one-time cost (~5 hrs, ~1.5 GB) and lets us refine classification rules against a static cache for free. Cache + resume means the crawl is interruption-tolerant. The graph is still curated — only the *source layer* is exhaustive.
- **Open downstream question:** How does Pass 2 decide what to promote? Likely a combination of (a) categories the page belongs to, (b) whether the page subject appears in any chapter extraction, (c) page length / infobox richness as a quality signal. To be designed when Pass 2 prompt is written.

### OPEN: Descriptive Chapter Title Mapping
- **Question:** AFFC and ADWD use descriptive chapter titles (THE PROPHET, REEK, THE UGLY LITTLE GIRL) that map to known characters. Should the extraction system normalize these to the character's real name or preserve the title?
- **Leaning:** Preserve the title in the filename and frontmatter, but add a `real_identity` field in frontmatter. "THE UGLY LITTLE GIRL" → `real_identity: Arya Stark`. This preserves GRRM's thematic intention (Theon losing his identity as "Reek") while keeping the graph navigable.
- **Note:** This matters for the voice analysis pass — "Reek" chapters have a fundamentally different internal voice than "Theon" chapters even though it's the same character.

### DECIDED: Chapter Splitter — Source Format
- **Decision:** Source files are plain .txt (converted from EPUB). Splitter targets .txt input.
- **Location:** `sources/raw/` contains GoT.txt, ACOK.txt, ASOS.txt, AFFC.txt, ADWD.txt

### DEFERRED: Spoiler Gating to Post-First-Release (2026-04-27)
- **Decision (2026-04-27):** `first_available` field is **deferred**. Optional in v1 nodes; existing values may be wrong/missing/inconsistent. Do not invest context reasoning out individual values. Backfill via deterministic script after first release.
- **Supersedes prior DECIDED rule** ("required on every node from the start; not retrofittable") which was overturned mid-Stage-2 review when schema-correctness remediation was projected to consume too much context for too little payoff. The wiki cite_ref data is rich enough that a deterministic backfill is cheap once we stop trying to enforce per-node consistency during extraction.
- **What this changes:** wiki-ingester drops the "agent self-corrects to `always available`" rule. Validator does not enforce `first_available`. CLAUDE.md and architecture.md updated. Tyrion/Varys (Stage-2 sample bugs) nulled rather than manually patched.
- **What this preserves:** the wiki data sources (infobox Books field + cite_ref anchors) remain documented in architecture.md so the backfill script can still use them.

### DECIDED: Track B (Wiki Parser) Before v3 Schema Review
- **Decision (2026-04-25):** Build the wiki infobox parser (Track B) before doing a schema review of the v3 Pass 1 output and before scaling v3 to ACOK/ASOS/AFFC/ADWD.
- **Rationale:** Track B surfaces schema signals that an isolated v3 review cannot:
  - **Entity type boundaries** — wiki categories are an external taxonomy. Mismatch with the 12 Pass 1 categories is a schema signal.
  - **Relationship/edge shape** — infobox fields (`spouse`, `father`, `liege`, `culture`, `religion`) define the graph's relationship vocabulary. Gaps in Pass 1's relationship extraction surface here.
  - **`first_available` mechanics** — `cite_ref` chapter anchors are the spoiler-gating primitive. The parser proves whether the encoding is reliable.
  - **Schema redundancy** — if the wiki provides house words / sigils / seats reliably, Pass 1 doesn't need to extract them. Track B can *shrink* the Pass 1 schema.
- **Cost asymmetry:** Doing schema review first risks discovering Track B reshapes it → 272 chapters (ACOK + ASOS + AFFC + ADWD) re-run. Doing Track B first costs a few days of already-queued work.
- **Continue prompt:** `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` (now includes this rationale at the top).

### DECIDED: Extraction Pass Order
- **Decision:** Six passes in sequence: Mechanical → Wiki → Voice/Perception → Foreshadowing → Theory-Informed → Discovery
- **Rationale:** Each pass builds on the structured outputs of prior passes. Cross-chapter analysis (Passes 3+) requires the chapter-level extractions from Pass 1 as input.

---

## Ideas & Backlog

> Capture every idea here, even half-formed ones. Tag with priority: HIGH, MEDIUM, LOW, SOMEDAY.

### HIGH
- [ ] Write the chapter splitter script (agent prompt ready)
- [ ] Run Pass 1 on AGOT as proof of concept
- [ ] Write Pass 2 wiki ingestion agent prompt
- [ ] Create theory seeds file (top 20-30 theories with confidence tiers)

### MEDIUM
- [ ] Design the trigger table schema (what columns, what routing logic)
- [ ] Write Pass 3 voice analysis prompt — include the cross-POV perception dimension (how Character X is perceived by Character Y's POV vs. their own self-perception)
- [ ] Write Pass 4 foreshadowing prompt — agent receives the foreshadowing events list and scans chapter extractions for matches
- [ ] Design the node file schema (what does a single entity file look like in `graph/nodes/`)
- [ ] Build convergence map for Oldtown as proof of concept

### LOW
- [ ] Explore fan fiction generation as a downstream use case — voice profiles + relationship graph + location descriptions = grounded creative generation
- [ ] Portfolio README and demo design
- [ ] Consider MCP server for programmatic graph access
- [ ] Explore cybersecurity knowledge graph as a parallel project using the same architecture

### SOMEDAY
- [ ] Graph DB migration if markdown doesn't scale
- [ ] UI for graph exploration (React app?)
- [ ] Automated theory confidence scoring based on evidence density
- [ ] Ingest theory content from YouTube transcripts (Alt Shift X, Glidus, etc.)
- [ ] Community contribution pipeline — let other ASOIAF nerds submit nodes/edges through PRs

---

## Session Log

> Newest first. One entry per work session. **Strict 5-entry max** (CLAUDE.md rule #8): when a 6th lands, the oldest archives to `history/worklog-archives/archiveNNN.md`.

### Session 41 — Per-character index roll-up + POV canonical resolution (2026-05-11)

**Changes made:**
- `scripts/build-character-indexes.py` — NEW. Pure-Python (no LLM, no HTTP) script that walks 3,910 `character.*` graph nodes, parses each frontmatter for slug/name/type, joins against the per-chapter mention index (inverse maps for POV + mentioned-in), reads node-body `## Edges` section for out_edge_count, looks up `working/wiki/data/backlink-counts.json` for in_edge_count, and emits one `graph/index/characters/<slug>.index.json` per character + a `_summary.json` rollup. CLI: `--character <slug>` (test mode), `--all` (default), `--dry-run`. Idempotent. Runs in ~1.0s.
- `graph/index/characters/` — NEW directory. 3,910 character-index JSON files + `_summary.json`. Stats per file: `appearances_total`, `chapters_pov`, `chapters_mentioned_in`, `out_edge_count`, `in_edge_count`. Lists: `chapters.pov` and `chapters.mentioned_in` (each mention record carries chapter_id, book, pov_character_slug, mention_count, sections, resolved_via). POV chapters excluded from mentioned_in to avoid double-counting.
- **POV canonical resolution (Matt-requested expansion):** instead of guessing POV from the filename stem (which left Alayne/Reek/descriptive-title chapters with the wrong POV), the script now parses each Pass 1 extraction's `pov_character:` frontmatter field. Pass 1 already encodes truename canonicalization there: `Alayne (Sansa Stark)`, `Reek (Theon Greyjoy)`, `Theon Greyjoy (as "The Turncloak" / "Reek")`. A small parser handles both `(truename)` and `(as "alias")` idioms + disguise wording (`Arya Stark (disguised as "Arry")`). Slug resolution chain: kebab → direct → alias-resolver → honorific-strip (`Maester Cressen` → `cressen`) → unique-prefix-match → mention-disambiguated prefix-match (`Catelyn` → catelyn-stark beats catelyn-bracken because catelyn-stark appears in chapter's Characters Present). All but 1 of 344 chapter POVs now resolve (the remaining 1: AFFC prologue's Pate the Novice — wiki page exists at `Pate_(Novice).json` but was never promoted to graph, real missing-node case).
- `working/todos.md` — marked Per-character Index Roll-up DONE; added new Year-page Type Bug todo (10 wiki year-pages slipped through as `character.human`; faithfully emitted but flagged in `_summary.json.year_pages_emitted_as_characters`).

**Decisions:** Followed the continue-prompt's 4 leans verbatim: (a) include all `character.*` types — 3876 human + 28 dragon + 6 direwolf; (b) `in_edge_count` from `backlink-counts.json` (the existing prose cross-ref count); (c) POV chapters in separate list from mentioned_in (no double-counting); (d) alias resolution inherits from mention-index — no extra work. **Year-page handling: emit faithfully + log** (option a from the 3 choices), with a todo entry capturing the underlying type-classification bug for separate fix. **POV canonicalization done at the index layer, not the graph layer.** Alayne and Reek remain distinct graph nodes (POV=0 each, mentioned_in retained). The character INDEX treats them as Sansa/Theon for retrieval (correct narrative model). The graph-level SAME_AS merge is Stage 4 work — but the index doesn't need to wait for it. **POV roster grew 18 → 30** after this work: gained Quentyn (4), Barristan (4), Victarion (4), Asha (4), Aeron (2), Areo (2), Jon Connington (2), Arianne (2), Cressen, Will, Chett, Varamyr, Arys Oakheart, Melisandre, Kevan, Merrett Frey. Top-9 POV counts match canon: Tyrion 47 ✓, Jon 42 ✓, Arya 33 ✓ (was 31 — pre-fix missed Cat of the Canals + Blind Girl + Ugly Little Girl), Daenerys 31 ✓, Catelyn 25 ✓ (was 24 — pre-fix missed agot-catelyn-06 where pov_character was just "Catelyn" with no surname), Sansa 24 ✓ (was 21 — +Alayne ×2 + Sansa I), Bran 21 ✓, Jaime 17 ✓, Eddard 15 ✓, Theon 13 (was 7 — +Reek ×3 + 3 descriptive titles). Continue-prompt's smoke-test estimate of "30-50 chapters mentioned in" for Eddard was wrong — actual is 185 (referenced post-death throughout AFFC/ADWD).

**Session 41 addendum (post-commit `e737ba4e`):**
- `graph/nodes/characters/pate-novice.node.md` — NEW. Hand-crafted from Pass 1 (`affc-prologue.extraction.md`) content because the wiki crawl had only the redirect HTML for this page (case-collision bug, see below). Includes the impersonation edges (`KILLED_BY: alchemist` + `KILLED_BY: jaqen-hghar`) per memory rule `project_impersonation_edges_redirect.md`. Theory-relevant: Pate is murdered by Jaqen H'ghar disguised as the alchemist, and Jaqen takes Pate's face/identity at the Citadel — major Faceless Men plotline.
- `scripts/build-character-indexes.py` enhanced with a raw-name reverse-map tiebreaker: when prefix-match returns multiple candidates (e.g., POV "Pate" → 12 `pate-*` slugs), intersect with nodes that explicitly claim that raw name in their frontmatter aliases. Solves the "alias-resolver rightly refuses to pin a single-word bare-disambiguation alias" case without modifying the alias-resolver. Pate now resolves; all 344 chapter POVs resolve; **POV roster = 31** (up from 30).
- `scripts/audit-missing-nodes.py` — NEW. Audits the gap between cached wiki pages and graph nodes. Output: `working/audits/missing-nodes-2026-05-11/execution/missing-nodes.{md,json}`. Findings:
  - **1,170 unpromoted wiki pages** (excluding pages flagged for `skip`)
  - **138 Bucket A** — Pass 1 references them, no graph node. Top: `godswood`/36, `flea-bottom`/31, `old-gods`/22, `seastone-chair`/14, `chatayas-brothel`/12, `unsullied`/9, `valyrian-steel-dagger`/8.
  - **83 Bucket B** — heavily wiki-backlinked but Pass 1 silent (mostly D&E/historical).
  - **949 Bucket C** — tail (defer).
  - **125 case-collision redirect crawl bugs** — pages whose canonical-content variant got overwritten on case-insensitive macOS HFS+. Major losses: `Children of the Forest`, `Free Folk`, `Red Priest`, `Valar Morghulis`, `House Words`, `Known World`. Per CLAUDE.md narrow-exception rule, fetching these requires explicit per-use approval and CANNOT write to `sources/` directly — fix is a dedicated session.
- `working/todos.md` — added 3 new HIGH-priority todos: case-collision crawl bug (125 pages), missing-node backfill (138 Bucket A pages), wiki prose extraction never completed (5,975 stub-only nodes).

**What's next:**
- **Stage 4 component (b) — chapter-evidence backfill** is now unblocked. The character index per slug provides the prerequisite "for character X, here are the chapters that reference them" lookup. Continue prompt for the larger Stage 4 work: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.
- **Year-page type fix** queued in todos.md (10 nodes; bundles naturally with Stage 4 temporal-edges work, since year pages are the natural `OCCURRED_IN_YEAR` anchors).
- **Case-collision crawl bug** queued in todos.md — major finding, 125 pages affected, requires dedicated session + per-use exception approval.
- **138 missing-node backfill** queued in todos.md — cheap Python work, $0, would close the highest-signal gap.
- **Wiki prose extraction** queued in todos.md — re-run `wiki-pass2-extract-prose.py` against the 5,975 stub-only nodes.
- **Per-LOCATION + per-ARTIFACT index roll-ups** are the natural next iteration of this work (continue prompt scoped to characters only). Pattern is reusable — same script structure with different node-type filter. Not yet a todo; flag if/when Stage 4 needs them.
- **Per Matt's standing rule, /endsession is NOT auto-run.**

### Session 40 — Catch-up synthesis, surgical merges, alias backfill (2026-05-11)
**Detail:** `history/session-details/session-040.md`

**Changes made:**
- `reference/architecture.md` — added `event.tournament` row to Type Reference Table + hierarchy diagram (was missing from spec despite 35 nodes using it); removed dead reference to `working/taxonomy-candidates.md` (file lost in Session 39 reorg).
- `working/todos.md` — marked religion type-drift todo OBSOLETE (architecture.md updated since the original Session 26 entry; current spec matches all 63 religion nodes); marked alias-backfill todo DONE; added Stage 4 richest-form 3-component expansion under existing Stage 4 entry; added Per-character Index Roll-up as READY-TO-DO with new continue-prompt link; added 3 tiny follow-up todos surfaced this session.
- `graph/nodes/events/battle-of-the-blackwater.node.md` — surgical merge: kept Python-extracted Origins/Aftermath/Quotes (110-line wiki body), replaced stub Identity with agent's rich version, inserted Allegiances + Narrative Arc sections from `_conflicts/`. Deleted `_conflicts/battle-of-the-blackwater-battles-b-2026-05-01T20-34-52.node.md`.
- `graph/nodes/texts/battle-of-the-blackwater-song.node.md` — replaced Python stub with agent-rich version via `git mv` from `artifacts/`. Preserves `WRITTEN_BY: Galyeon of Cuy` edge that Python had no way to infer (no infobox on songs). Deleted `artifacts/battle-of-the-blackwater-song.node.md`.
- `graph/nodes/factions/caltrops.node.md` — agent's `organization.faction` type was correct (the wiki entry is a 13-noble conspiracy from the Dance of the Dragons, not a battle); replaced 1-paragraph Narrative Arc with Python's richer 4-paragraph wiki extraction, added Quotes section. Deleted `graph/nodes/events/caltrops.node.md`.
- 6 character/location nodes — added missing aliases: `eddard-stark` ← "Ned Stark", `tormund` ← "Tormund Giantsbane", `eastwatch-by-the-sea` ← "Eastwatch", `blackwater-rush` ← "The Blackwater" (river), `brienne-tarth` ← "Brienne", `thoros` ← "Thoros of Myr". Durable path (frontmatter, not just JSON).
- `working/wiki/data/alias-resolver.json` — regenerated via `scripts/wiki-pass2-build-alias-resolver.py --apply`. 1,199 → 1,205 alias_to_canonical entries.
- `graph/index/chapters/{book}/*.mentions.json` — all 344 files regenerated via `scripts/build-mention-index.py --all`. Resolution rate **70.0% → 70.6%** (+209 newly resolved).
- `scratch` — triaged + emptied. Both items addressed by this session's discussion (Item 1 = Stage 4 component-b; Item 2 = superseded by existing Stage 4 continue prompt).
- Memory: added `project_team_is_solo.md` (team = Matt only; Okey was one-off), `project_stage4_richest_form.md` (3-component expansion of Stage 4 scope). MEMORY.md index updated.

**Decisions:** **Stage 4 reframed to 3 components, not 1.** Original scope was prose-edge-classifier alone (cross-references.jsonl → typed edges). Catch-up synthesis surfaced that accumulated raw material (Pass 1 across 5 books, mention-index at 70.6%, cross-refs.jsonl, Python prose on 6,968 nodes) makes a richer scope economical: (a) prose-inferred edges, (b) chapter-evidence backfill, (c) rich Identity rewrites for top-N high-traffic nodes. Each independently shippable. **Stage 1 was paused mid-stride** for cost reasons (Session 24 pivot from agent to Python-deterministic for secondary buckets; saved ~$1,200). The 855 agent-rich Stage-1 nodes are the only ones with synthesized rich Identity + prose-inferred edges. **The 247 remaining `_conflicts/` files are NOT being regenerated** (idempotent script, all dated Apr 26-May 1); deferred to bundled Stage 4 work per existing line 101. **The agent was correct on caltrops type-classification disagreement** (Python trusted bucket assignment as `event.battle`; agent read prose and correctly typed as `organization.faction` with explicit Notes explaining override).

**What's next:**
- **READY TO DO — Per-character index roll-up** — pure Python, $0, ~30-60 min. Continue prompt: `progress/continue-prompts/2026-05-11-per-character-index-rollup.md`. Unblocks Stage 4 component (b).
- **Stage 4 launch** — still queued at `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. Alias-backfill prerequisite NOW MET as of this session.
- **3 tiny follow-ups** in `working/todos.md` under "Tiny Follow-ups (Session 40 surface)": architecture.md typo fix, second round of alias-backfill, conflicts cleanup (covered).
- **Per Matt's standing rule, /endsession was invoked explicitly** — handoff prompt below.

### Session 39 — Status check + working/wiki/ subtree reorg (2026-05-07)
**Detail:** `history/session-details/session-039.md`

**Changes made:**
- **Reorg:** `working/wiki-parsed/` split into `working/wiki/data/` (9 permanent reference files: alias-resolver, infobox-data, page-index, page-categories, cross-references, chronology-events, backlink-counts, parse-stats.md, cross-refs-summary.md) and `working/wiki/pass2-staging/` (7 run-specific staging files: triage-bucket-assignments, triage-manifest, draft-buckets, priority-summary, stage3-promote-summary, stage3a-emission-summary, stage3b-extraction-summary). `working/wiki-pass2/` → `working/wiki/pass2-buckets/` (all 536 buckets, 14,141 files via `git mv`). `working/wiki-parsed/` directory removed.
- `working/wiki/README.md` — NEW. Explains data/staging/buckets split. Notes that historical session details, archived continue prompts, and audit execution logs reference old paths and were intentionally not rewritten.
- 65 live files updated via three-step targeted sed (~32 scripts/, 14 .claude/agents/*.md, 4 reference/*.md, 3 working/runbooks/, 3 working/agent-fleet-specs/, 2 .claude/commands/, 2 active continue prompts, CLAUDE.md, worklog.md, working/todos.md, working/tier3-promotion-plan.md). Sed key trick: only match the **quoted** `"wiki-parsed"` and `"wiki-pass2"` to avoid breaking script filenames like `wiki-pass2-triage.py`.
- `CLAUDE.md` Directory Structure diagram updated (lines 119-120 now show `wiki/` parent with `data/`, `pass2-buckets/`, `pass2-staging/` children).
- `worklog.md` Session 35 corrected: ASOS Okey branch IS merged (commit `2eaf5c71`, verified via `git log`). Prior entry's "Branch not yet merged" was correct at Session 35 but stale by Session 39.
- Smoke verification: `python3 scripts/build-mention-index.py --book agot --dry-run` runs cleanly against new paths; final grep confirms only remaining `wiki-pass2` refs in live files are correct script filenames.

**Decisions:** **Naming reorg adopted as Option D** (Matt's instinct, beating my original A/B/C menu). `working/wiki/` as parent domain; pass-numbers as children of the domain rather than top-level siblings. Future passes (Stage 4 prose-edge, etc.) get a natural home. Frozen records (`history/**`, `working/audits/**`, `progress/continue-prompts/archive/**`, `working/runbooks/archive/**`, `scripts/archive/**`) **left untouched** — they describe what was true at the time. **`graph/index/chapters/` not renamed** — the path already says "chapters"; "mention" is fine as a concept once explained. README todo added. **Food/dialogue cost design discussion** (no execution): Python pre-pass makes the LLM pass substantially cheaper — targeting + tighter scopes + scene-level chunking + sampling-oracle pattern → ~$10-25/book on Sonnet vs ~$50/book for blind Pass 1. Reasoning still required for scene-level structure.

**What didn't get done:**
- **No commit.** Reorg sits in working tree as 14,141 renames + 65 modifications + 1 new README. Awaits explicit authorization.
- `graph/index/chapters/README.md` agreed but not written (added to todos).

**What's next:**
- **Commit the reorg** (single commit, suggested: `Reorg: working/wiki-{parsed,pass2}/ → working/wiki/{data,pass2-buckets,pass2-staging}/`).
- **Smallest unit-of-work next:** alias-backfill from Session 38 mention-index top-20 unresolved patterns; cheap edit to `working/wiki/data/alias-resolver.json` + re-run mention-index → expected resolution >75%.
- Other live tracks unchanged: Stage 4 prose-edge-classifier (`progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`); dialogue/meals/mention-index design (`progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md`); model-fit recommendations awaiting Matt's review; two PreToolUse hooks queued.
- **Per Matt's standing rule, no `/endsession` auto-run.**

### Session 38 — Mention-index built (graph-traversal infrastructure) (2026-05-06)

**Changes made:**
- `scripts/build-mention-index.py` — NEW. Pure-Python script that walks all 344 Pass 1 v3 extractions, parses structured `## Section` blocks (Characters Present, Characters Referenced, Locations, Artifacts, Food & Drink, Raw Entity List 12 categories), slugifies via `to_kebab` (reused from `wiki-pass2-build-alias-resolver.py`), resolves through `alias-resolver.json` plus an honorific-prefix-stripping pass (Ser-, Maester-, Khal-, Lord-, etc.), tags each row with section/line/node-type/node-path. CLI: `--book <slug>`, `--all`, `--dry-run`. Idempotent — overwrites in place.
- `graph/index/chapters/` — NEW directory tree. 344 mention files written (agot 73, acok 70, asos 82, affc 46, adwd 73). 37,222 total mentions. **70.0% resolve to graph nodes** (66.6% direct + 3.4% alias). 30.0% unresolved are diagnosable patterns, not parser bugs. Plus `_summary.json` rollup.
- `working/todos.md` — alias-backfill todo added under § Wiki / Pass 2 Prep, sourced from the top-20 unresolved list.

**Decisions:** Re-framed `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` under graph-for-agents lens. Matt confirmed dialogue + meals were agent-invented scope (Matt never asked for them in prior sessions). **Mention-index is the only piece that survives the reframe** — it's graph-traversal infrastructure that closes "from a node fact, find the scene." Dialogue + meals + voice scope deferred entirely; built only the free Python piece. **One spec divergence:** added honorific-prefix stripping beyond original spec (`Ser-`, `Maester-`, `Grand-Maester-`, `Khal-`, `Lord-`, `The-`) — Pass 1 captures titled forms ("Ser Rodrik Cassel", "Khal Drogo") that wiki nodes don't. This single addition lifted AGOT resolution 57% → 72%.

**Top-20 unresolved patterns (signal):**
- **Missing alias entries** (clean backfill candidates): `ned-stark`/42 → eddard-stark, `tormund-giantsbane`/21 → tormund, `eastwatch`/23 → eastwatch-by-the-sea, `the-blackwater`/23 → blackwater-rush, `brienne`/27 → brienne-tarth, `thoros-of-myr`/28 → thoros.
- **Ambiguous short names**: `joffrey`/47, `aegon`/27, `maester-aemon`/57.
- **Genuinely missing nodes**: `godswood`/36, `flea-bottom`/31, `the-narrow-sea`/40, `great-pyramid-of-meereen`/24, `little-walder-frey`/22, `old-gods`/22.

**What's next:**
- **Apply alias-backfill** from top-20 unresolved (todos.md alias-backfill todo). Cheap edit to `alias-resolver.json` + re-run mention-index → expect resolution to climb past 75%.
- **Per-character index roll-up** (`graph/index/characters/<slug>.index.json`) is the natural next step — combines mention-index + Pass 1 POV chapter data + node prose into a single agent-retrieval entry point. Pure Python.
- **Dialogue + meals + voice remain deferred** until Matt asks for them.
- **Stage 4 prose-edge-classifier** queued continue prompt (`2026-05-02-stage4-v1-prose-edge-classifier.md`) is the other live track.
- **Per Matt's standing rule, no `/endsession` auto-run.**

### Session 37 — Cleanup scrubs + model-fit audit (2026-05-06)

**Changes made:**
- **Scrub A (D&D framing retired):** moved `working/chat-ui-architecture.md` and `working/diagrams.md` → `history/archive/sketches/` with stale-sketch preambles. Deleted 2 chat-UI/D&D-framed bullets in `working/todos.md` (Q5(a) two-repo split + Q6 unrelated chat-UI-scope bullet). Q6 spoiler-gate bullet kept (defer; rides on existing first_available deferral).
- **Scrub B (copyright rule deleted entirely):** removed the textual rule from CLAUDE.md, README.md (line 220 surgical), worklog.md Current State, .claude/commands/endsession.md (step 7 deleted, renumbered), dialogue-meals continue prompt, runbooks/book-integration-done.md, scratch-design-review-stage3b.md, memory MEMORY.md + memory feedback_never_commit_books.md (deleted), memory project_real_goal_graph_for_agents.md (two-repo line deleted per Q5=a). `STATUS.md` retired entirely (Q3=b). Mechanical protection (.gitignore + .claude/settings.json permission denials) is now the only line of defense.
- **Citation-validator full-corpus re-run** at `working/audits/citation-corpus-rerun-2026-05-06/execution/citation-issues.md`: PENDING-PASS-1 bucket from 2026-04-30 audit fully closed, zero broken chapter-file references, zero new HIGH findings. Several Stage-1 cite-format issues from prior audit have been re-emitted away in interim node-rebuild work.
- **Model-fit audit** at `working/audits/agent-model-fit-2026-05-06/execution/agent-model-fit-report.md`: 27 agents audited. 6 Opus → Sonnet (mechanical-extractor, wiki-ingester, citation-validator, orphan-edge-finder, prose-edge-classifier [smoke-test gated], schema-drift-auditor). 2 → Haiku (status-reporter, duplicate-detector). 2 keep Opus (cross-identity-detector + reviewer — high-stakes, low-volume SAME_AS decisions). 13 STUBs deferred. Fleet-plan near-term spend (Stages 1-3) drops from $100-200 to $25-65 if classifier smoke passes — 60-75% reduction.
- **D&E Pass 1 reframed in Current State:** "deferred (enrichment pass for main-arc nodes)" per Q11=(b). Not dropped, not urgent, not on active critical path.
- **Audit folder layout adopted (Q10):** new audits land at `working/audits/<slug>-YYYY-MM-DD/{prompt-planning,prompt,execution,validation}/`. Existing flat-path audits not migrated; new layout for new audits only.

**Decisions:** **Two cleanup scrubs landed.** D&D-group / shared-password / friend-group-only chat-UI framing retired across docs, todos, and one memory file; the *concept* of a chat UI is preserved as "ask-questions interface on top of the graph" (per the handoff's reframe), but as a NEW future todo, not a salvage of the retired bullets. **Copyright textual rule deleted entirely** — Matt's call: gitignore + permission denials suffice, the textual reminder created drift not safety. **Per-audit folder layout adopted (Q10)** to make audit + validation pairs first-class. **Model-fit recommendations queued for Matt's review** before any agent prompt frontmatter changes; smoke-test gates explicit. **Hooks follow-up captured** — two PreToolUse hooks (block edits to historical archives + block edits under sources/) added to todos.md as separate items, not freelanced this session.

**Unexpected surface:** `validate-2026-05-06-handoff-cleanup-and-direction.md` at repo root (untracked) — sibling validation prompt for this scrub work. Contains 11 "copyright" + ~7 "chat-ui/D&D" anchor strings as part of describing what to check. Not in scope per § 3 of the handoff. Flagged for Matt to triage at /endsession (move to `working/audits/<slug>/validation/` per Q10, archive next to the handoff, or run it).

**What's next:**
- **Strategic question deferred (Q12=b):** Stage-4-vs-mention-index choice — re-read both queued continue prompts under graph-for-agents lens — left for a separate fresh session.
- **Two new READY-TO-DO follow-ups in `working/todos.md`:** (a) review fleet plan against model-fit recommendations, (b) two PreToolUse hooks (block edits to historical archives, block writes under sources/).
- **Continue prompts active (3):** `2026-05-02-stage4-v1-prose-edge-classifier.md`, `2026-05-05-dialogue-meals-mention-index-design.md`, plus this handoff (will be archived at /endsession).
- **Per Matt's standing rule, /endsession is NOT auto-run** — handoff prompt awaits Matt's invocation.

> Sessions 34, 35, 36 archived to `history/worklog-archives/archive008.md` (archive008.md has 3 entries; will fill over future cycles)
> Sessions 30–33 in `history/worklog-archives/archive007.md` (full at 5 entries)
> Sessions 25–29 archived to `history/worklog-archives/archive006.md`
> Sessions 22–24 archived to `history/worklog-archives/archive005.md`
> Sessions 16-21 archived to `history/worklog-archives/archive004.md`

> Sessions 8–15 archived to `history/worklog-archives/archive003.md`
> Sessions 5–7 archived to `history/worklog-archives/archive002.md`
> Sessions 0–4 archived to `history/worklog-archives/archive001.md`

---

## Principles

> Guiding principles for the project. Reference these when making design decisions.

1. **The chapter text is immutable.** Source files in `sources/chapters/` never change. Everything else layers on top.
2. **Facts before interpretations.** Mechanical extraction before analytical. Tier 1 before Tier 4.
3. **Agents propose, humans decide.** Analytical findings go to the curation queue. Matt assigns confidence.
4. **Spoiler gating is architectural.** Every node has `first_available`. This is not a feature to add later.
5. **The index and the graph are complementary.** The index routes. The graph traverses. Both are needed.
6. **Each token should be productive.** Structure exists to reduce waste — agents should read relevant, trustworthy content, not re-derive known relationships.
7. **Start with the foundation, not the flashiest feature.** Chapter files → mechanical extraction → wiki → index → graph → analytical passes. In that order.
