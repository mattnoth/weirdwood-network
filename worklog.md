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
- [x] .gitignore protecting copyrighted content (sources/raw/, sources/chapters/, full-txt-files/, epubs/)
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
- [ ] Pass 1 v3 run on ACOK (0/70)
- [ ] Pass 1 v3 run on remaining books (ASOS 0/82, AFFC 0/46, ADWD 0/73)
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki-parsed/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [ ] AGOT/ACOK supplementary entity index: script to scan existing extractions and categorize candidate entity types from narrative sections
- [ ] Pass 1 run on remaining books (ASOS, AFFC, ADWD) — blocked on prompt update + wiki parser groundwork
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 0 foundation — alias-resolver built + run (Session 26). 707 broken refs reclaimed via slug-mismatch fix. Empirical signal validates that most remaining "broken" refs are genuinely missing concept entities (concept-pages decision: defer).
- [ ] Wiki Pass 2 Stage 4 — prose-derived edge discovery (Stage 0 prep complete + cross-references index built; Stage 4 hybrid plan documented in `working/fleet-orchestration-plan.md`. Need to build: edge-candidate-generator script, then prose-edge-classifier agent runs (full prompt ready), then peer review, then promote. Skeleton: `2026-04-27-wiki-pass2-stage4-edge-discovery.md`)
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

> Newest first. One entry per work session.

### Session 26 — Stage 3 Completion + Tier-Recovery + Fleet Architecture + Chat UI Design (2026-04-27 → 2026-04-28)
**Detail:** `working/session-details/session-026.md`

**Changes made:**
- `scripts/wiki-pass2-extract-prose.py` — NEW. Stage 3b deterministic prose extractor (replaces planned LLM agent). H2→schema-heading mapping, h3 book-boundary preservation, cite_ref translation. ~770 lines.
- `scripts/wiki-pass2-promote.py` — NEW. Stage 3 promoter. Concat skeleton + "\n" + prose → `graph/nodes/<type>/<slug>.node.md`. Atomic-rename + conflict-detect. ~585 lines.
- `scripts/wiki-pass2-build-cross-refs.py` — NEW. Stage 4 prep step. Walks prose files extracting `[anchor](wiki:Page)` links → `cross-references.jsonl` (81,090 rows) + `backlink-counts.json` + `cross-refs-summary.md`.
- `scripts/wiki-pass2-build-alias-resolver.py` — NEW. Stage 0 foundation. Walks node aliases, builds wiki-form-kebab→canonical-slug map. 707 broken refs reclaimed.
- `scripts/wiki-pass2-emit-deterministic.py` — UPDATED. Emits to `skeleton/` (was `tmp/`) for single-writer-per-file. Added `## Culture`, `## Organization`, `## Aftermath` schema headings. Added `Background`/`Prelude`/`Battle`/`Aftermath`/`Layout`/`City`/`Legend`/`Character and Appearance` mappings. Skip-empty-prose-files behavior.
- `scripts/wiki-infobox-parser.py` — UPDATED. Plural mappings (fathers/cultures/battles) and `written by`→`WRITTEN_BY`. ENTITY_TYPE_OVERRIDES dict (21 entries).
- `.claude/agents/` — 6 detailed agent prompts NEW (`prose-edge-classifier`, `cross-identity-detector`, `schema-drift-auditor`, `citation-validator`, `duplicate-detector`, `orphan-edge-finder`). 13 stub agents NEW (`disambiguation-resolver`, `contradiction-surfacer`, `multi-type-entity-resolver`, `perception-mapper`, `chekhovs-gun-tracker`, `theory-evidence-scorer`, `extraction-quality-auditor`, `cross-book-entity-reconciler`, `chronology-extractor`, `event-orderer`, `prose-edge-reviewer`, `cross-identity-reviewer`, `fleet-stats-reviewer`). Total fleet now 27 agents (was 8).
- `.claude/agents/wiki-ingester.md` — header note explaining Stage 1 archive; full v1 prompt restored beneath.
- `.claude/commands/check-fleet.md` — NEW slash command for fleet monitoring (verb-rich: status/questions/answer/cost/dag/spot/dry-run-next-stage/divert/etc.; degrades gracefully against existing-state when daemon doesn't exist yet).
- `working/agent-pipeline-plan.md` — NEW canonical fleet roster (27 agents, dependency-driven ordering, total budget ~$1,250-2,310).
- `working/fleet-orchestration-plan.md` — NEW. Stage DAG, stats schema, rate-limit handling, sample-based peer-review pattern.
- `working/fleet-runtime-architecture.md` — NEW. Multi-day Python daemon (NOT a Claude Code session — sidesteps session limits via subprocess.run on `claude --print`). tmux for persistence. State files. Resilience: 4 scales of failure isolation. Coordinator pattern for auto-respawn. Per-stage scripts as no-daemon escape hatch.
- `working/chat-ui-architecture.md` — NEW. Three-corpus retrieval (graph + wiki prose + book chunks, joined on slug). Friend-group D&D-preview deployment via mattnoth.com submodule. Pure TS + native CSS matching mattnoth-dev's stack. Spoiler gate fully OPEN for v1. Synthesis-not-quotation prompt rule for book copyright posture. UI build fleet separate from construction fleet. .gitignore + Netlify deployment-boundary architecture.
- `working/design-philosophy.md` — NEW. Unix philosophy + worse-is-better corollary + anti-patterns (featuritis/hidden-coupling/recursive-complexity/composition-through-inheritance). Soft-corrected on peer review (orchestrator-driven sample-based is fine; recursive subagent calls are not). Package + global-install policy.
- `working/diagrams.md` — NEW. 14 small focused architecture diagrams as scan-in-30-seconds reference.
- `working/scratch-design-review-stage3b.md` — NEW. Briefing for second-opinion agent that validated the Stage 3b agent→Python redesign.
- `working/runbooks/wiki-pass2-pipeline.md` — REWRITTEN as v3. Stage 3 fully Python; mid-stage review marked as ran-once-clean; new `## Aftermath`/`## Culture`/`## Organization` schema headings documented.
- `reference/architecture.md` — Artifact-Format-by-Consumer section + entity-type override doc + edge-vocabulary-lock callout (from Session 25 carried into Session 26 work).
- `reference/agents.md` — REWRITTEN. 27-agent canonical roster organized by category (Active / Archived / Stage 4 / Quality / Pass 3 / Pass 4 / Pass 5 / Pass 6 / Tier 3 / Reviewers / Meta). Hard-rules block at top includes package-policy reference.
- `working/wiki-pass2/houses-major-recovery/` — NEW one-off recovery bucket for Tier-1 entities (46 nodes: 7 missing major houses, 27 regions/locations, 10 pre-narrative Targs, 2 chars).
- `working/wiki-pass2/tier2-recovery/` — NEW one-off recovery bucket for Tier-2 entities (24 nodes: 4 religions, 12 titles, 6 cultures, 2 organizations).
- `graph/nodes/` — 3,384 new nodes added (3,314 Stage 3 + 46 Tier 1 + 24 Tier 2). Cumulative: 855→4,239.
- `working/wiki-parsed/` — `cross-references.jsonl` (81,090), `backlink-counts.json` (6,526 entries), `alias-resolver.json`, `cross-refs-summary.md`, `stage3a-emission-summary.json`, `stage3b-extraction-summary.json`, `stage3-promote-summary.json`.
- `working/todos.md` — major updates: Stage 3 marked complete with stats; Tier 1+2 recoveries logged; obsoleted entries (`Wiki-ingester prompt v2`, `Validator edge byte-equality`); new entries (alias-resolver, multi-type-entity policy PROMINENT, temporal edges v2, per-entity index tables, spoiler-gate-fully-open PROMINENT, chat-UI-deployable-D&D-preview PROMINENT, religion type drift, type=unknown song page, 4 new agent prompts to write, agent pipeline plan reference, chat UI scope shift).
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-finish.md` — completed this session (work absorbed into pipeline-plan + orchestration plan; not deleted because the file documented the redesign decisions).
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — UPDATED with hybrid plan (Python preprocessing + agent classification). Step 1 (cross-references index) marked complete in this session.

**Decisions (compressed):** Stage 3b became fully Python (no LLM agent) after design review showed wiki HTML already contains the prose; extractor is deterministic, cheap, ~14 sec for 3,315 pages. Concept pages defer (option iii) — empirical broken-link analysis validates this. Multi-type entities are single-node v1 with dominant infobox-type. Spoiler gate fully OPEN for v1. Chat UI scope shifted from personal-local to friend-group-shareable preview at mattnoth.com/projects/<slug> with full prose retrieval (book copyright posture: friend-group only, synthesis-not-quotation, snippet-limited). Stack confirmed pure-TS + native-CSS + esbuild matching mattnoth-dev. Construction fleet ≠ UI build fleet (separate orchestrators, separate tmux sessions; `/check-fleet` skill is multi-orchestrator-aware). Orchestrator daemon is Python-not-Claude-Code-session (subprocess.run on `claude --print` per agent invocation; sidesteps session limits). Per-stage scripts as no-daemon escape hatch. Peer review IS allowed (orchestrator-driven sample-based, not recursive subagent calls). Package + global-install policy codified for code-writing agents. Unix-philosophy framing established as canonical project rationale. Repo confirmed PRIVATE on GitHub (`mattnoth/weirdwood-network`); .gitignore + Netlify-auto-publish-from-main is the intentional safety property keeping copyrighted content off Netlify; books reach the backend via separate path (private container registry, recommended).

**What's next:** Two parallel tracks, both unblocked. Track A (pipeline construction): Stage 4 build (edge-candidate-generator → prose-edge-classifier runs → reviewer → promote-prose-edges) and Pass 1 catch-up (ACOK + ASOS via mechanical-extractor). Track B (chat UI, eventual): wiki prose chunker + book chapter chunker + embedding pipeline + backend FastAPI + chat component + mattnoth-dev integration. Neither needs a continue prompt — `working/agent-pipeline-plan.md` and `working/chat-ui-architecture.md` document the next-action ladders. Open question: whether to build the orchestrator daemon next OR run Pass 1 catch-up in background tabs OR start the chat UI side. Matt's call.

### Session 25 — Stage 3 Prep: Priority Script + Stage 3a + Edge Vocabulary Lockdown (2026-04-27)
**Detail:** `working/session-details/session-025.md`
**Changes made:**
- `scripts/wiki-pass2-prioritize.py` — NEW. 472 secondary manifests labeled with `priority_tier` (A/B/C) + `page_kind` (Tier C only). Tier-C-`entity` → Tier-B promotion patched in. Idempotent.
- `scripts/wiki-pass2-emit-deterministic.py` — NEW. Stage 3a deterministic skeleton emitter. Reads infobox-data.jsonl + per-bucket priority labels; emits `working/wiki-pass2/<bucket>/tmp/<slug>.node.md` (frontmatter + thin Identity + full `## Edges`). Tested on 1 bucket (`houses-other-h-w`, 14 nodes). Full --apply NOT YET RUN.
- `scripts/wiki-infobox-parser.py` — NEW `ENTITY_TYPE_OVERRIDES` dict (21 mistyped "houses" → `organization.faction`: Night's Watch, Kingsguard, Faceless Men, Maesters, Golden Company, etc.). FIELD_EDGE_MAP additions: `fathers`/`cultures`/`battles` (plural variants of existing mappings) + new `written by` → `WRITTEN_BY` edge type. Module docstring expanded with edge-vocabulary-lock callout.
- `scripts/wiki-pass2.sh` (`cmd_run`) — reads `prior_status` before flipping bucket to in-progress; if prior was `fail`/`validation-failed`, `rm -rf` `tmp/` (closes long-standing footgun).
- `reference/architecture.md` — Edge Type Mapping table gained `WRITTEN_BY` row + `Battles` plural note. NEW vocabulary-lock callout block above table (parser is single source of truth, no script invents edges, currently-unmapped fields ranked, edge-polish-is-future, procedure for adding new edge types).
- `working/wiki-parsed/{infobox-data.jsonl, page-index.jsonl, parse-stats.md, priority-summary.json}` — regenerated by parser + prioritize re-runs.
- `working/wiki-pass2/*/manifest.json` × 472 — gained additive `priority` field.
- `working/wiki-pass2/houses-other-h-w/tmp/*.node.md` × 14 — test-bucket skeletons.
- `working/todos.md` — 4 entries added (book-chapter-pages defer-bucket plan, vocabulary-lock note attached to "Edge taxonomy gaps", new "Edge polish phase (FUTURE)" entry, new "Non-ASCII qualifier normalization (graph layer)" entry). "Launcher should auto-wipe stale tmp/" checked off.
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-prep.md` → archived (DoD ~60% complete).
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-finish.md` — NEW handoff for next session (remaining 40%).

**Decisions:** Three mid-course corrections beyond the original prep prompt scope. (1) **Tier-C-entity → Tier-B promotion:** 9 real-content houses/people lacking infoboxes (House Brune, House Shett, etc.) would have been deferred to Stage 4; promoted instead. Empty `## Edges` accepted as the cost. (2) **21 mistyped "houses" surfaced via Stage 3a test-bucket emission and fixed at parser level** (not inline in emit script) so the fix propagates to Stage 4 + future spoiler-gating backfill + any other downstream consumer. v1 uses `organization.faction` for all 21; finer-grained split (order/guild/company) deferred to future edge-polish/entity-polish phase. (3) **Edge vocabulary lock documented in 4 places** after Matt asked whether the taxonomy was being protected from drift — confirmed empirically derived from infobox field frequencies (parse-stats.md is the auto gap-finder), but added explicit hard-rule callouts in architecture.md, parser docstring, emit-deterministic docstring, and todos.md. Captured "edge polish phase" as a future agent-reasoning step, not a Stage 3a/3b concern. Sub-correction: 4 unmapped fields added to FIELD_EDGE_MAP during the lock-down review (`fathers`, `cultures`, `battles` plurals + `written by` → `WRITTEN_BY` new type); mean edges/skeleton ticked 4.57 → 4.60. Tier distribution after promotion: A=624 (18.5%), B=2,691 (79.8%), C=57 (1.7%, all redirects). Stage 3b cost projection: ~$70 for 624 Tier-A pages, well under the $200 guard.

**What's next:**
- `/continue 2026-04-27-wiki-pass2-stage3-finish` — fresh agent runs full Stage 3a `--apply`, mid-stage review, wiki-ingester v2 prose-only rewrite, validator edge byte-equality update. THEN STOPS for Matt's go-ahead before Stage 3b.
- Stage 4 (`2026-04-27-wiki-pass2-stage4-edge-discovery.md`) skeleton remains — flesh out only after Stage 3 finishes.

> Sessions 22–24 archived to `working/worklog-archives/archive005.md`
> Sessions 16-21 archived to `working/worklog-archives/archive004.md`

> Sessions 8–15 archived to `working/worklog-archives/archive003.md`
> Sessions 5–7 archived to `working/worklog-archives/archive002.md`
> Sessions 0–4 archived to `working/worklog-archives/archive001.md`

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
