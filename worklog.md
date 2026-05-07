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
- [x] Wiki infobox parser script (Track B) — `scripts/wiki-infobox-parser.py` produces `working/wiki-parsed/{infobox-data.jsonl (5,279), page-index.jsonl (17,657), parse-stats.md}`. `first_available` populated 2,888/5,279 (54.7%). **Three open issues:** (1) `categories[]` empty across all pages (parse API strips catlinks footer) — blocker for runbook §1.2.1 unless deferred to `entity_type_guess`, (2) `books` field parsed only 37 times vs 1,953 raw occurrences (parser bug), (3) unmapped infobox fields worth edge-taxonomy review (`dynasty`, `written by`, `hatched`, `fathers`, `vassal`, `cadet branch`).
- [x] AGOT/ACOK supplementary entity index — OBSOLETED 2026-04-25. v3 prompt captures all 12 categories directly; backfill index no longer needed. See `working/todos.md` line ~245.
- [ ] Pass 2 wiki ingestion agent prompt written
- [ ] Pass 2 wiki ingestion complete
- [x] Wiki Pass 2 v1 — core (37/37 buckets complete; 855 nodes; cost $95.33; per-node $0.111 healthy per Stage-2 cold review)
- [x] Wiki Pass 2 Stage 2 cold review (Session 24; decision was `remediate`, but overturned same session — see Active Decisions)
- [x] Wiki Pass 2 Stage 3 — secondary (Session 26; FULL pipeline rebuilt as Python-only after design review showed the Stage 3b agent was inertia-driven. 472 buckets / 3,315 candidate pages → 3,314 nodes promoted. Cumulative graph: 855→4,169 then →4,239 after Tier-1+Tier-2 recovery. Cost $0. Wall-clock ~30 sec total. 0 conflicts.) Canonical pipeline: `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3).
- [x] Wiki Pass 2 Stage 3c — audit cleanup (Session 27; 4 audits run, 6 parser bugs fixed, 484 nodes re-emitted across multiple targeted runs. Tier 3 promotion campaign Passes A-D + E Phase 1 added 769 new nodes. Cat 1 orphan edges 7,784→2,955 (62% drop). Stale religion-bleed 0. Edge vocabulary lock holds.)
- [x] Wiki Pass 2 Path B — categorizer extension + promotion campaign (Session 28; bounded MediaWiki categories backfill + parser CATEGORY_TYPE_MAP. `unknown` 12,434 (70.4%) → 2,118 (12.0%). +2,240 graph nodes (5,008 → 7,248). Cat 1 orphan edges 2,955 → 1,973. 5 new dirs bootstrapped: `texts/`, `theories/`, `concepts/`, `species/`, `foods/`. New entity type `object.food`.)
- [x] Wiki Pass 2 Path B promotion completion + schema-drift audit (Session 29; 4 new entity types added: `object.material`, `concept.language`, `concept.medical`, `concept.custom`. 4 new dirs: `materials/`, `languages/`, `medical/`, `customs/`. `unknown` 2,098 → 1,257. Net +315 graph nodes (7,248 → 7,563). 130 stale-dir mismatches cleaned. Full schema-drift audit on opus: 0 HIGH / 4 MED / 4 LOW. Cat 1 orphan edges 1,973 → 1,963. Edge vocabulary lock holds. Chronology data extracted from 74 year pages: 2,245 events in `working/wiki-parsed/chronology-events.jsonl` (awaits v2 temporal-edges schema; not graph edges yet).)
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

### Session 36 — Hygiene pass + soft-convention hardening (2026-05-06)
**Detail:** `history/session-details/session-036.md`

**Changes made:**
- 3 stale Pass 1 continue prompts → `progress/continue-prompts/archive/`. `progress/SESSION-32-HANDOFF.md` → `history/worklog-archives/session-32-handoff.md`.
- `progress/scratch-notes.md` deleted; three referenced long-form entries folded into `working/todos.md` lines that referenced them. Rest dropped (stale or redundant).
- Cleaned scratch-notes/handoffs.md refs in `CLAUDE.md`, `README.md`, `STATUS.md`, `.claude/agents/status-reporter.md`, `.claude/commands/endsession.md`.
- `CLAUDE.md` orchestration rules #7 and #8 rewritten: session-details now explicitly as-needed (not every-session); worklog Session Log strict 5-entry max with archives holding exactly 5 entries each.
- `CLAUDE.md` new section "Top-Level `scratch` File — Ignore It" before Orchestration Rules. Tells agents to ignore scratch outside `/endsession` step 4(a). `.gitignore` updated; root `scratch` file untracked.
- `.claude/commands/endsession.md` step 4 expanded with scratch-triage subroutine; step 6 rewritten to strict 5-entry rule.
- `working/todos.md` staleness sweep: Pass 1 model-fit smoke test obsoleted, Stage 4 prereq-met, agent-stub vs full-prompt status corrected, citation-validator queued for verify, spoiler-gating prereq-met, model-fit policy phrasing updated. New "Project Story / Auxiliary" category with session-details audit todo. `READY TO DO` flag added on model-fit-audit todo.
- `worklog.md` two staleness fixes (entity-index todo obsoleted; Stage 4 skeleton ref refreshed).
- Archive operation under new rule: Sessions 27, 28, 29 appended to `archive006.md` (now 5 entries); Sessions 30 (×2 numbered entries) and 31 created `archive007.md` (3 entries, will fill over future cycles).
- Single commit `240fe565` "Hygiene pass: archive stale prompts, retire scratch-notes, harden conventions" — 15 files, +407/−214. Pushed to `origin/main`.

**Decisions:** **Five rule changes locked.** (1) Worklog Session Log strict 5-entry max, archive in 5-entry blocks; ambiguous "~150 lines" replaced with concrete count. (2) Session-details files are as-needed, not every-session — write only for design/incident/novel-decision sessions; pure-execution skips. (3) Top-level `scratch` is Matt's private space (gitignored, agents don't read outside /endsession). (4) `/endsession` step 4(a) triages scratch contents at end of every session. (5) `progress/scratch-notes.md` retired; replaced by the gitignored top-level scratch + designated triage moment. **Soft-conventions framing surfaced as a project pattern:** rules in prose without enforcement drift over time; rules in /endsession do better but conditional steps still slip; hooks add real enforcement when the action must not be skipped (none built this session — all current cases are well-served by strict /endsession steps). **Hooks vs rules clarified:** rule = read; hook = executed; both together is "double cost" only when redundant; rules in /endsession alone are sufficient when /endsession is reliably invoked. **`working/todos.md` reorganization deferred** — proposed structure exists in conversation but not executed; Matt paused before approving.

**What's next:**
- **PRIMARY HANDOFF unchanged:** `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — design pass for dialogue/meals/mention-index passes, awaiting Matt's review of 7 Open Questions.
- **`working/todos.md` reorganization** — proposed 12-section structure + parallel `working/todos-archive.md`; restart this in next session.
- **`READY TO DO` next** (per todos.md): model-fit audit across `.claude/agents/*.md` (resource-conservation pass). And: re-run `citation-validator` on full 5-book corpus now that Pass 1 is 344/344.
- Stage 4 v1 still queued: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

### Session 35 — ASOS Pass 1 complete via Okey's parallel run (2026-05-06)

**Changes made:**
- `extractions/mechanical/asos/` — 82/82 v3 chapters pushed by Okey on branch `origin/pass1-asos-extraction` (parallel Opus pass on shared Max account, ran 2026-05-01 → 2026-05-06, ~$54.85). All 12 POVs covered (13 Arya / 4 Bran / 7 Catelyn / 6 Daenerys / 6 Davos / 9 Jaime / 12 Jon / 5 Samwell / 7 Sansa / 11 Tyrion + Prologue + Epilogue). Spot-checked early/mid/late waves — full v3 schema, healthy. Branch not yet merged to main.
- `worklog.md` — Current State updated: ASOS now 82/82 ✓ (Pass 1 5/5 books complete, 344/344). This entry.
- `working/progress.md` — single pointer line appended; per-wave detail lives in `working/extraction-stats/extraction-stats-asos-pass1-v3.csv` on Okey's branch.

**State:** Pass 1 v3 ALL 5 books complete (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73 = 344/344). Stage 4 prose-edge-classifier and the dialogue/meals/mention-index design are the unblocked next moves.

**Decisions:** None — verification + worklog hygiene only. Okey's branch left unmerged for now (merge when ready; minor `worklog.md` + `working/progress.md` conflicts expected, no extraction-file collisions).

**What's next:**
- Merge `origin/pass1-asos-extraction` into main when ready (resolve worklog/progress conflicts in favor of main's clean entry).
- Resume primary handoff: `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — 7 Open Questions to resolve, then build mention index, then smoke dialogue on Ned + Robert.
- Stage 4 v1 prose-edge-classifier now unblocked: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`.

### Session 34 — ADWD complete + bug-fix landing + cleanup (2026-05-05)

**Changes made:**
- `extractions/mechanical/adwd/` — 73/73 v3 chapters complete (15 waves, 2026-05-05). Some duplicate wave entries from Bug A residue before fix landed; last-writer-wins, all valid v3. Was untracked — committed this session.
- `working/extraction-stats/extraction-stats-ADWD-pass1-v3.csv` — NEW. Was untracked — committed.
- `scripts/extract.sh` + `scripts/weirwood.zsh` — chain/race fix landed across commits `5f9b808f`, `f3cd92ba`, `dea679af` (Bug A `--chain` explosion + Bug B parallel-extraction race + UX cleanup with phase banners and streamed Claude assistant output). Two small follow-ups committed this session: `${_HEARTBEAT_PID:-}` guard (cmd_run trap) and arithmetic expansion fix in cmd_check.
- `progress/continue-prompts/archive/` — moved `2026-05-04-urgent-fix-chain-and-race-bug.md` + `2026-05-04-acok-waves1-10-rerun.md` (work complete).
- `working/todos.md` — URGENT BLOCKER block removed.
- `worklog.md` — Current State updated: ADWD 73/73, ACOK 70/70, ASOS line clarified (Okey running Opus on shared Max). This entry.
- `working/progress.md` — 22 ADWD wave rows appended (some duplicates from Bug A residue).

**State:** Pass 1 v3 4/5 books complete (AGOT 73 + ACOK 70 + AFFC 46 + ADWD 73 = 262/344). ASOS 0/82 pending Okey's push.

**Decisions:** None this session — execution + cleanup only. Design discussion on next-pass direction (dialogue extraction → Pass 3 voice-analyzer anchor) deferred to next session for prompt drafting + smoke test.

**What's next:**
- **PRIMARY HANDOFF:** `progress/continue-prompts/2026-05-05-dialogue-meals-mention-index-design.md` — three new passes designed (dialogue, meals & feasts, per-chapter mention index) + Opus-as-sampling-oracle validation strategy + file organization proposal. Self-contained design doc; next session reads it end-to-end, resolves 7 Open Questions with Matt, then builds the mention index first as the free Python unblocker, then smokes dialogue on Ned (POV-rich) followed by Robert Baratheon (POV-less stress test for non-POV quote attribution + cross-POV perception capture).
- Wait on Okey's ASOS push to land (no Claude work needed until then; design + smoke can proceed on AGOT regardless).
- Stage 4 v1 prose-edge-classifier remains queued for once 5/5 Pass 1 books land (`2026-05-02-stage4-v1-prose-edge-classifier.md`).

> Session 33 archived to `history/worklog-archives/archive007.md` at end of Session 38 (archive007.md now full at 5 entries; next archive cycle creates `archive008.md`)
> Sessions 30–32 also in `history/worklog-archives/archive007.md`
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
