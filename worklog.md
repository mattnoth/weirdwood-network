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

### Session 60 — Stage 4 Haiku: Normalizer + No-Silent-Drop Pipeline (2026-05-19)

**Detail:** `history/session-details/session-060.md`

**Changes made:**
- `scripts/stage4-haiku-normalize-edge-types.py` — NEW. Deterministic edge-type-name normalizer: morphological alias table (6 entries — `TRAVELED_TO`→`TRAVELS_TO`, `DIES_AT`→`DIED_AT`, `ALLIED_WITH`→`ALLIES_WITH`, `ATTENDED`→`ATTENDS`, `LOCATEDOCATED_AT`→`LOCATED_AT`, `LOCATED_IN`→`LOCATED_AT`) + difflib fallback @0.80 + `--dry-run`/`--dump-vocab` modes. Applied 19 morphological rewrites to existing Haiku output (batch-0020 + 8-wave).
- `scripts/wiki-pass2-validate-edge-jsonl.py` — `load_canonical_vocab()` fixed: was over-counting 161 (scraped `FOSTERED_BY` + `LOCATED_IN` from description prose); now table-row-key regex → correct **159**.
- `working/missions/2026-05-19-stage4-haiku/unresolved-edges-log.jsonl` — NEW. Persistent multi-stage append log (22 rows; `stage` field lets normalizer/residual-pass/validator all write; dedup-keyed; idempotent).
- `working/missions/2026-05-19-stage4-haiku/locked-edge-vocab-159.md` — NEW. Printed self-contained 159-vocab reference (name + description + type-contract).
- `working/missions/2026-05-19-stage4-haiku/normalizer-report-2026-05-19.md` — NEW.
- Reverted Session-59 Sonnet-mission debris: `working/missions/2026-05-14-stage4-v1-bulk-sonnet/{state.jsonl, locks/batch-0057.lock, locks/batch-0067.lock}` restored via `git checkout`.
- `progress/continue-prompts/2026-05-19-stage4-haiku-normalize-and-residual.md` — NEW. `2026-05-19-stage4-haiku-run-batches.md` — DELETED (superseded).
- `history/session-details/session-060.md` — NEW.

**Decisions:** The deterministic normalizer fixes ONLY morphological variants (same word, wrong tense / literal typo) — cross-lemma semantic remaps must NOT be auto-applied (a first build over-reached with a synonym table — `ATTACKED_BY`→`KILLED_BY` etc. — caught and removed; silently laundering semantic errors would destroy the Haiku-vs-Sonnet drift signal we are about to measure). Vocab is **159**, confirmed — the validator parser bug reporting 161 is fixed. **No-silent-drop pipeline locked** (6 stages: prevention → classify → normalizer → 2nd-Haiku residual pass → validator → targeted Opus review); every unresolved edge accumulates in `unresolved-edges-log.jsonl` with a `stage` tag, never dropped. The final Opus review is **self-contained** — reads only the log + the printed 159-vocab, never architecture.md. Sequencing: **prevention first** (inline vocab into the classify prompt) — shrinks the residual across the whole ~1017-batch bulk. The Session-59 Sonnet-mission touch was an abandoned Haiku-as-Sonnet-worker attempt; **no Sonnet output was overwritten**; the current Python orchestrator never touches the Sonnet mission. "harness" retired as project vocabulary.

**What's next:**
- **STEP 1 prevention → STEP 2 residual pass → STEP 3 targeted Opus review → STEP 4 validator-to-log → then run/compare/harden/scale** → continue: `progress/continue-prompts/2026-05-19-stage4-haiku-normalize-and-residual.md` (**Opus 4.7** conductor).
- Known flags: `FOSTERED_BY`/`FOSTERED_BY_INVERSE` need direction-aware handling (in the log, not auto-fixed); chunk-size never validly tested (8-wave batches were all 5 files = single chunk); Opus conductor/watcher sessions are the cost driver, not the Haiku batches (~$8.50 Haiku API to date).
- **/endsession was explicitly authorized this session.**

---

### Session 59 — Stage 4 Haiku Worker Built + Smoke (2026-05-19)

**Detail:** `history/session-details/session-059.md`

**Changes made:**
- `scripts/stage4-haiku-run.py` — NEW. Haiku Stage 4 orchestrator: batch selection (`--batches`/`--all-done`), `--chunk-size`, `--concurrency` (parallel chunks), rate-limit detection, provenance snapshot, results + `run-summary.json`. Output → `prose-edges-haiku/` (separate from Sonnet's `prose-edges/`).
- `.claude/commands/stage4-haiku-classify.md` — NEW. Thin classify-only Haiku prompt; hardened with a `## CRITICAL RULES` section (Tier-1 qualifier-enum table, KNOWS STOP, qualifier≠direction, no-invented-types, type contracts).
- `.claude/agents/prose-edge-classifier.md` — R1/R2/R3 applied (Pattern 5 KNOWS STOP rule + KNOWS type-contract row; co-presence centralized rule; qualifier self-check).
- `scripts/stage4-haiku-smoke-prep.py` / `-cleanup.py` / `-finish.sh` — NEW (smoke scaffolding).
- `working/session-results/2026-05-19-batch-0020-opus-audit.md` — NEW (audit re-run; verdict "needs prompt change first" → R1).
- New Haiku mission dir `working/missions/2026-05-19-stage4-haiku/`; batch-0020 Sonnet control + Haiku-v1 output archived under `working/wiki/pass2-buckets/_archive/`.
- Memory `project_stage4_haiku_not_sonnet.md` — NEW.
- Continue prompt `2026-05-19-stage4-haiku-run-batches.md` — NEW. `2026-05-19-stage4-haiku-smoke-fire.md` + `2026-05-19-batch-0020-opus-audit.md` — DELETED (completed).

**Decisions:** Haiku is the Stage 4 bulk worker; **Sonnet is off the table** (cost — ~1017 batches; memory `project_stage4_haiku_not_sonnet`). The Haiku worker is built SEPARATE from the Sonnet worker (own scripts, output dir, mission dir) — never co-mingle. Haiku cannot drive the Sonnet worker harness's batch-bookkeeping (claimed wrong batch, early-exited, asked human mid-task) → a Python orchestrator does all bookkeeping; Haiku only classifies. Prompt hardening works when rules are inlined WITH their data (qualifier-missing 38→0, KNOWS 60→16) — proven twice. Speed-first; imperfect output acceptable (Opus watcher + later mechanical-extraction enrichment backstop). batch-0020 Haiku chunk-10 parallel = $1.86/5.7min vs chunk-3 = $2.99/28.5min — under Sonnet's $3.42. Remaining ~17.5% drift = invented type-name variants + type-contract → next: Python normalizer + inline-vocab + pre-loading re-architecture.

**What's next:**
- **Opus conductor — optimize Haiku pass speed, run batches, compare vs Sonnet, harden, iterate, scale** → continue: `progress/continue-prompts/2026-05-19-stage4-haiku-run-batches.md` (**Opus 4.7** conductor).
- 8-batch Haiku wave (queued batches, chunk-15, concurrency-8) completed at session close — next session reads its `run-summary.json` as STEP 0.
- **/endsession was explicitly authorized this session.**

---

### Session 58 — Stage 4 Lockdown Completion + Vocab Round 2 (2026-05-18 → 2026-05-19)

**Detail:** `history/session-details/session-058.md`

**Changes made:**
- `reference/edge-qualifier-vocab.md` — NEW. 18 enum-bearing types (8 Tier-1 + 10 Tier-2). IN_LAW_OF added Round 2 with `{by_marriage_of_*}` enum.
- `reference/architecture.md` — `## Edge Types` intro cross-ref to qualifier-vocab; 10 new edge type rows across 6 subsections (Kinship/Political/Factional/Military/Knowledge/Cultural); vocab callout 149 → 159; Session-58 audit history line added.
- `.claude/agents/prose-edge-classifier.md` — `notes` field DELETED from emit_edge schema; `qualifier` field added with tier-dependent behavior; qualifier-lookup workflow step (step 4); Pattern 4 prohibition; 5 vocab-count refs bumped 149 → 159; reverse-direction lists extended (STEP_PARENT_OF/STEP_CHILD_OF one-sided pair; IN_LAW_OF/CONSPIRES_WITH symmetric).
- `scripts/stage4-resolve-link-placeholders.py` — NEW. 4,744 queued candidate files rewritten (121,310 `[LINK]` → `«anchor»` substitutions). Inline patch in `scripts/wiki-pass2-build-edge-candidates.py` for future generations.
- `scripts/wiki-pass2-validate-edge-jsonl.py` — extended with 3 new check classes (type contracts / qualifier enums / notes-rejection). Self-test on 21 Sonnet control-arm batches surfaces 2,528 new violations (1,757 tier-3 qualifier emission dominant; 380 not-in-enum; 193 notes; 149 missing required; 49 type-contract).
- `scripts/wiki-pass2-flag-suspicious-edges.py` — extended with 6 pattern classes. Full run across 72 done batches / 4,075 emits: 288 flagged (7.1%). KNOWS-as-fallback dominates at 82.3% of KNOWS emits; batch-0020 alone has 140 of 163.
- `working/qualifier-vocab/audit-completeness-2026-05-19.md` — NEW. 229-line audit deliverable; 8 STRONG ADOPT edges + 0 sub-qualifiers + 8 MEDIUM DEFER + 11 REJECT + 3 borderlines.
- `working/qualifier-vocab/decisions.md` — `## Round 2` section appended (Round 1 untouched).
- `progress/continue-prompts/2026-05-19-batch-0020-opus-audit.md` — NEW (Opus audit running in iTerm2 at session close).
- `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` — DELETED (STEP 1.6 completed).
- `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` — DELETED (superseded by smoke-fire prompt).
- `working/todos.md` — HAIKU-CUTOVER STEPS 1.6/1.7/2/3/4 marked [x]; entity-linking-Pass-1-to-nodes item added under Ideas & Backlog (Matt's session-58 follow-up).
- `history/session-details/session-058.md` — NEW.
- `history/worklog-archives/archive012.md` — NEW. Session 53 archived (archive012 holds 1/5 entries).

**Decisions:** **Vocab FINAL at 159 types / 18 enumerable** (8 Tier-1 + 10 Tier-2 + ~141 Tier-3). **Sub-qualifier dimension NOT adopted** — audit confirmed enum value IS the leaf. 10 new edge types adopted from vocab-completeness audit: SPIES_ON, INFORMS, NAMED_AFTER, STEP_PARENT_OF, STEP_CHILD_OF, IN_LAW_OF (Tier-2), RESCUES, BANISHES, TORTURES, CONSPIRES_WITH. **Pass-1 deterministic harvester deferred** — architecture settled (markdown-parse + Haiku closed-vocab + Opus stratified audit), not built; revisit after Haiku smoke. **batch-0020 chosen as canonical Haiku smoke target** (hot zone: 153/437 flagged, KNOWS-fallback concentration). **Haiku smoke fires via watcher pattern** (Matt's call) — watcher Opus 4.7, worker Haiku 4.5, verdict-gating mandatory per drift-detection rule. **Entity-linking via extractions surfaced as follow-up** (Matt's session-close add) — Pass 1 mentions ("Jon Snow", "the bastard of Winterfell") need to resolve to canonical node slugs so extractions can enrich graph-node edges. Deferred to post-smoke. **Mid-session reframe:** Matt's three probing questions — "could you have recorded relationships on that same pass?" → "python might miss what the word means... does that lock in our edges?" → "did we miss anything?" — reshaped the harvester architecture (candidate + verify, not deterministic emit) and triggered the completeness audit that produced Round 2.

**What's next:**
- **Verify batch-0020 Opus audit completion** (running in fresh iTerm2 separate process at session close; verify `working/session-results/2026-05-19-batch-0020-opus-audit.md` exists before firing smoke).
- **STEP 5 Haiku smoke fire** → continue: `progress/continue-prompts/2026-05-19-stage4-haiku-smoke-fire.md` (**Opus 4.7 watcher + Haiku 4.5 worker** per mission-protocol). Gated on audit verdict.
- After smoke: revisit Pass-1 deterministic harvester; decide Stage 4 bulk Haiku resume; begin Pass-1-mention → graph-node entity-linking work (Matt's session-58 add).
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 57 — Stage 4 Qualifier Vocab Lock-Down (2026-05-18)

**Detail:** `history/session-details/session-057.md`

**Changes made:**
- `working/qualifier-vocab/decisions.md` — NEW. Full verdict matrix: 17 enumerable types (8 Tier-1 REQUIRED + 9 Tier-2 OPTIONAL) + 132 Tier-3 (no qualifier, no notes). Open questions Q1–Q5 answered. Schema implications for STEP 1.6 + STEP 3 documented.
- `working/session-results/2026-05-18-stage4-qualifier-vocab-locked.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` — NEW. Self-contained STEP 1.6 handoff with all 17 enums verbatim.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` — DELETED (this session's launching continue prompt, completed).
- `working/todos.md` — HAIKU-CUTOVER STEP 1.5 marked [x] (17 enums verdicted; notes field deletion decided); new STEP 1.6 (encode) inserted; STEP 3 updated to reference the new vocab file and `notes`-rejection.
- `history/session-details/session-057.md` — NEW.
- `history/worklog-archives/archive011.md` — Session 52 archived; archive011 now full at 5 entries.

**Decisions:** **Tier-1 (8):** SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO — REQUIRED enum from closed set. **Tier-2 (9):** BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, KNOWS, GUEST_OF — OPTIONAL enum. **Tier-3 (132):** all others — NO qualifier, NO notes. **`notes` field DELETED ENTIRELY from edge schema across all tiers** (Matt's "zero freeform" call — notes was the open drift surface qualifier-vocab is meant to close). **Encoding strategy: Option C** (new file `reference/edge-qualifier-vocab.md`; architecture.md tables untouched) — decided by fresh-context agent to avoid orchestrator bias. **21 already-emitted Sonnet batches preserved as freeform control arm** for the eventual Haiku enum-locked comparison; no normalizer. Mid-session correction: Matt prompted "is `Relationships Observed` the only Pass 1 table worth noting? there is spatial movement as well" — audit of remaining 16 Pass 1 sections surfaced GUEST_OF as missed Tier-2 candidate via Pass 1's own `## Hospitality & Guest Right` `Type` column (680 rows, top-10 = 88%). 16 enums → 17 enums. Matt's session-close caveat preserved: "I feel like there may be more qualifiers that come up as we are locking this stuff down" — STEP 1.6 should treat the 17 as v1, append rather than re-audit if new ones surface.

**What's next:**
- **STEP 1.6 — Encode qualifier vocab + delete notes field** → continue: `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-encode.md` (**Sonnet 4.6** — mechanical translation of decisions.md into runnable artifacts). Writes new `reference/edge-qualifier-vocab.md`, adds one architecture.md cross-ref line, updates prose-edge-classifier prompt schema (delete `notes`, add `qualifier` field + lookup step).
- STEP 2 ([LINK] sub), STEP 3 (validator — type contracts + qualifier enums + notes-rejection folded), STEP 4 (suspicious-edges flagger) — can run independently / parallel after 1.6. STEP 5 (Haiku smoke) gated on all four.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 56 — Stage 4 Vocab Applied + Qualifier Vocab Lock-Down Planned (2026-05-18)

**Detail:** `history/session-details/session-056.md`

**Changes made:**
- `reference/architecture.md` — 17 new edge-type rows applied across 8 subsections (AFFLICTED_BY, DIED_OF, COMPANION_OF, PARTICIPATES_IN, OFFICIATES, ATTACKS, ASSAULTS, COURTS, CONTRACTED_WITH, PROPOSED_AS_BRIDE, CROWNS_QUEEN_OF_LOVE_AND_BEAUTY, PRACTICES, PURCHASED_FROM, BUILT, CAPTAIN_OF, CREW_OF, REPUTED_AS); 2 description mods (FIGHTS_IN "battle, war, or tournament as a combatant"; MANIPULATES mechanism note); vocab callout 132 → 149; Session-55-second-wave historical note added; gap-filing default rewritten from "file vocabulary-gap question" to "vocab FINAL — reject as `no-fitting-type-vocab-locked`."
- `.claude/agents/prose-edge-classifier.md` — vocab FINAL flip; 5 `~149` references (lines 20, 210, 241, 378, 417); 17 new types appended to in-prompt category-expansion list; reverse-direction section extended (both-sided list adds KNIGHTED_BY/BESTOWS_KNIGHTHOOD_ON + NURSED_BY/WET_NURSE_OF; one-sided list adds CHILD_OF/HOST_OF/RESURRECTED_BY/SERVED_BY/DEFEATED_BY/GUARDIAN_OF); CONTEMPORARY_WITH STOP-block contradiction fixed (now points at `no-fitting-type-vocab-locked` + PROPOSED_AS_BRIDE example).
- `scripts/stage4-close-vocab-gaps.py` — NEW. Decision-map for all 68 rows in `working/wiki/pass2-buckets/questions-for-matt.jsonl`. Idempotent atomic rewrite. **63 rows newly closed**, 5 pre-resolved skipped, 0 unresolved. JSONL integrity verified.
- `working/qualifier-vocab/plan.md` — NEW. 1-screen scannable plan for HAIKU-CUTOVER STEP 1.5. Three-tier framing locked: Tier 1 REQUIRED enum / Tier 2 OPTIONAL enum / Tier 3 freeform notes.
- `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` — NEW.
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — DELETED (this session's continue prompt, completed).
- `working/todos.md` — HAIKU-CUTOVER STEP 1 marked [x]; new STEP 1.5 inserted; STEP 5 (Haiku smoke) flagged BLOCKED on STEP 1.5; STEP 3 (validator) notes folded qualifier-enum enforcement.
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_lockdown_before_long_passes.md` — NEW. Companion to drift-detection-mandatory. MEMORY.md index updated.
- `working/session-results/2026-05-18-stage4-vocab-applied-and-smoke-prepped.md` — NEW.

**Decisions:** **Three-tier qualifier framing locked** (Tier 1 REQUIRED / Tier 2 OPTIONAL / Tier 3 no-enum). **Haiku smoke (STEP 5) BLOCKED on qualifier vocab lock-down** (STEP 1.5) — Haiku is more drift-prone than Sonnet; closing every freestyle surface is the actual lever for making Haiku viable, not stronger prompts. **Lockdown-before-long-passes is now a project memory rule.** Three additional uncovered types resolved during apply without inventing new vocab: COMPETES_IN (rejected, duplicate of post-Session-55 FIGHTS_IN), SOLD_TO (rejected, reverse-of-PURCHASED_FROM), TRANSACTS_WITH (rejected, too-generic); SLAIN_BY_WEAPON/KILLED_WIELDING resolved-pre-adopted under Session-54 KILLED_WITH. Mid-session drift catch: orchestrator was extrapolating "note X in `notes`" from the Session-55 MANIPULATES decision into three other new-type rows; Matt halted and reverted — exact failure pattern that motivated the qualifier-vocab lock-down track.

**What's next:**
- **Qualifier vocab lock-down** (next major track) → continue: `progress/continue-prompts/2026-05-18-stage4-qualifier-vocab-lock.md` (**Opus 4.7** — corpus-knowledge synthesis at scale: Pass 1 + wiki + 21 batches + series knowledge to verdict ~149 edge types). Produces `working/qualifier-vocab/decisions.md`.
- After: STEP 1.6 (encode into architecture.md + classifier prompt), STEP 2 ([LINK] sub), STEP 3 (validator — type contracts + qualifier enums folded), STEP 4 (suspicious-edges flagger), THEN STEP 5 (Haiku smoke).
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

> Session 55 archived to `history/worklog-archives/archive012.md` (3/5 entries)
> Session 54 archived to `history/worklog-archives/archive012.md` (2/5 entries)
> Session 53 archived to `history/worklog-archives/archive012.md` (1/5 entries)
> Session 52 archived to `history/worklog-archives/archive011.md` (archive011 now full)
> Session 51 archived to `history/worklog-archives/archive011.md`
> Session 50 archived to `history/worklog-archives/archive011.md`
> Session 49b archived to `history/worklog-archives/archive011.md`
> Session 49 archived to `history/worklog-archives/archive011.md`
> Sessions 44-48 archived to `history/worklog-archives/archive010.md` (full at 5 entries)
> Sessions 39–43 archived to `history/worklog-archives/archive009.md` (full at 5 entries)
> Sessions 34–38 archived to `history/worklog-archives/archive008.md` (full at 5 entries)
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
