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

### Session 55 — Stage 4 Vocab Lock Decisions + Pass 1 Staleness Incident (2026-05-18)

**Detail:** `history/session-details/session-055.md`

**Changes made:**
- `scripts/stage4-vocab-gap-analysis.py` — NEW. Normalizer for the 16-distinct-schema `questions-for-matt.jsonl` (68 rows). Outputs `working/agent-fleet-specs/stage4-vocab-gaps-{normalized.jsonl,rollup.md}` — 10 stale-resolved, 37 truly open, 7 untyped.
- `working/agent-fleet-specs/stage4-vocab-lock-2026-05-18.md` — NEW. Decision doc bucketed A (12 stale rows close) / B (5 accepts) / C (9 rejects: reverse-direction + too-generic) / D (22 borderline → Matt's call). Updated through D verdicts with second-opinion-agent overrides.
- `working/todos.md` — added "Stage 4 — Haiku Cutover Prep" section with 5 numbered steps (vocab lock / `[LINK]` substitution / validator extension / suspicious-edges worklist / Haiku smoke).
- 4 staleness fixes applied via dispatched agent: `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/{project_pass1_prompt_v3_canonical.md,MEMORY.md,memory_staleness_policy.md (NEW)}` + `CLAUDE.md` (pipeline table row 4 → "✅ Done"; Orchestration Rule 9 added — worklog wins over continue-prompts when they conflict) + `progress/continue-prompts/2026-05-18-stage4-haiku-cutover.md` ("Status from memory" passage corrected).
- `history/session-details/session-055.md` — NEW (full narrative).
- `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` — NEW (Shape B handoff for apply phase).

**Decisions:** 17 new edge types approved (vocab 132 → 149): `AFFLICTED_BY`, `DIED_OF`, `COMPANION_OF`, `PARTICIPATES_IN`, `OFFICIATES`, `ATTACKS`, `ASSAULTS`, `COURTS`, `CONTRACTED_WITH`, `PROPOSED_AS_BRIDE`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`, `PRACTICES`, `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`, `REPUTED_AS`. Plus 2 description mods: `FIGHTS_IN` (add "or tournament"), `MANIPULATES` (qualifier-mechanism note). Rejected: 9 reverse-direction violations (Bucket C), 5 generic/derivable (NAMED_AFTER, extended kinship, BRIBES standalone, USES_AS_SIGIL). **ATTACKS scoped as generic person→person OR creature→person physical violence; ASSAULTS specifically for sexual violence** (Matt's call). **CREW_OF locked at end of session as sibling to CAPTAIN_OF (Path B); both target `object.artifact` vessel.** Subsection placement locked: AFFLICTED_BY/DIED_OF → Knowledge & Information (next to HEALS); CAPTAIN_OF → Possession & Ownership. **Decisions are NOT yet applied** to architecture.md or the classifier prompt — apply work is the next session.

**Incident — stale Pass 1 belief:** Mid-session, orchestrator believed "ACOK/ASOS/ADWD Pass 1 incomplete" based on a 13-day-old memory file + the session's launching continue prompt's "Status from memory" passage. Ground truth: all 5 books complete (344/344) since 2026-05-06. Matt halted, dispatched root-cause investigator. Three stale sources fixed + one new memory rule (`memory_staleness_policy.md`) + CLAUDE.md Rule 9 added: trust worklog over continue prompts when they conflict on state.

**What's next:**
- **Apply the vocab lock + prepare Haiku smoke-test spec for already-done batches.** → continue: `progress/continue-prompts/2026-05-18-stage4-vocab-lock-apply.md` (**Opus 4.7** — mechanical apply work + smoke-test architecture). Smoke-test candidate batches identified: 0066 (wyman-manderly, 168 cands), 0068 (bowen-marsh), 0072 (taena/hallis multi-page), 0001 (early-batch mix).
- Then HAIKU-CUTOVER STEPS 2/3/4 ([LINK] sub / validator type contracts / suspicious-edges flagger) — Matt's call whether they happen before the smoke fires or alongside.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 54 — Stage 4 Schema Lockdown + 21-Batch Bulk Run (2026-05-15 → 2026-05-16)

**Detail:** `history/session-details/session-054.md`

**Changes made:**
- `.claude/agents/prose-edge-classifier.md` — major patches: added `## Output Contract → Required fields per decision` table (mechanically validated), `evidence_kind` discriminator field on every emit_edge (`wiki-entity` / `wiki-chapter-summary` / `book-pass1`), `pass1_relationship` candidate-shape documentation (was wired in candidate generator but undocumented in prompt), `## Common failure patterns` top-level section with 3 concrete from-the-data examples (CONTEMPORARY_WITH-fallback / FIGHTS_IN-with-person / ATTENDS-with-person), `Reverse-direction edges` rule (PARENT_OF/GUEST_OF/RESURRECTS/TUTORS/WIELDS/OWNS/FORGED_BY are one-sided; KILLS/UNCLO_OF/WARD_OF are both-sided).
- `working/agent-fleet-specs/worker-snippets/stage4-classifier-template.md` — validator-runs-before-marking-done step + `Two failure modes to avoid` section.
- `reference/architecture.md` — 11 new edge types across two passes: Session-54 added UNCLE_OF, NEPHEW_OF, KILLED_WITH, ATTENDS; Session-55 added COUSIN_OF, MILK_BROTHER_OF, NURSED_BY, WET_NURSE_OF, KNIGHTED_BY, BESTOWS_KNIGHTHOOD_ON, DEPICTED_IN. Vocab now ~132 types across 15 subsections.
- `scripts/wiki-pass2-validate-edge-jsonl.py` — NEW. Mechanical validator. Loads architecture.md vocab via regex (127 types found), checks per-decision required fields, checks shape rules (`confidence_tier` int 1-3, `evidence_snippet` verbatim ≥10 chars not section-header, `evidence_kind` matches `candidate_kind`, edge_type in canonical vocab). Self-tested against archived broken batch-0012 (caught 14/14 violations).
- `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/feedback_drift_detection_mandatory.md` — NEW memory rule. Every bulk LLM run includes mechanical validator + cross-model audit + verdict-gates-resumption, regardless of model.
- 6 session-results docs written: `2026-05-15-stage4-batch-0012-quality-check.md`, `2026-05-15-stage4-edge-provenance-explained.md`, `2026-05-15-stage4-haiku-smoke-verdict.md`, `2026-05-16-stage4-bulk-run-checkpoint.md`, `2026-05-16-stage4-current-status-and-open-questions.md`, `history/session-details/session-054.md`.
- 21 Sonnet batches completed (batch-0012 canonical re-run through batch-0021). Manifest: 12 → 21 done. ~600+ prose-edges JSONL files written under `working/wiki/pass2-buckets/<bucket>/prose-edges/`.
- 2 failed batch-0012 attempts archived for the comparison record: `_archive/batch-0012-sonnet-pre-schema-fix-2026-05-15/` (schema-broken Sonnet) and `_archive/batch-0012-haiku-failed-2026-05-15/` (Haiku semantic failure).

**Decisions:** Haiku 4.5 rejected for prose-edge classification (smoke test: validator-clean but ~80% semantic failure — SERVES-on-everything, KILLED_BY reversal, type-contract violations wholesale). Sonnet stays the bulk worker. Schema drift is a property of LLM-structured-output, not of any model — defense is mechanical validator + cross-model audit, not stronger prompts alone. **The durable answer to "schema lockdown" is to lock the audit, not the prompt** — build a suspicious-edges worklist (KNOWS without explicit "knew" language, ATTENDS-non-event, FIGHTS_IN-non-event, KILLED_BY-non-person, tier-3, CONTEMPORARY_WITH-on-character-pair) for later Opus review. Soft-fallback whack-a-mole pattern: patched CONTEMPORARY_WITH (Session 55 mid-stream), KNOWS-as-fallback emerged in batch-0020 (~37% of emits). Accept the 5-7% baseline; post-clean via the worklist. Sequential single-terminal bulk firing is safer than parallel (rate-limit failures cleaner, no stale-lock cascades).

**Mission state at session end:** 21/201 batches done, ~$37 cumulative spend, 180 queued. Stop file removed; locks dir empty. Worker not running.

**What's next:**
- **Resume Stage 4 bulk in one terminal** → continue: `progress/continue-prompts/2026-05-16-stage4-bulk-resume.md` (**Sonnet 4.6** workers via `/loop 20m /worker-stage4`). 180 batches × ~$3.42 ≈ $615 remaining.
- **BEFORE resuming if possible**: extend `scripts/wiki-pass2-validate-edge-jsonl.py` with the suspicious-edges flagging logic (Matt's idea) — flag schema-clean-but-semantically-suspicious patterns to `working/wiki/data/stage4-suspicious-edges.jsonl` for later Opus review. See continue prompt Step 4.
- **Vocab gaps pending review:** CROWNS_QUEEN_OF_LOVE_AND_BEAUTY (recommend reject); OFFERED_AS_BRIDE / CONSPIRES_WITH / HOSTAGE_OF may surface again at scale.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 53 — Stage 4 1-Tab Smoke + Throttle Calibration (2026-05-15)

**Detail:** `history/session-details/session-053.md`

**Changes made:**
- `scripts/stage4.sh` — three edits: (1) added `STAGE4_SLEEP_BETWEEN` env var (default 5400s/90 min) replacing prior 30s inter-batch sleep; (2) fixed `set -e` + `pipefail` bug that was silently terminating the worker on non-zero claude exits (the explicit error-handling block was dead code) — pipeline now wrapped in `set +e` / `set -e`; (3) ported rate-limit detection from `extract.sh` — checks tmp_json for `"status":"rejected"` + `"rateLimitType"`, writes `rate-limit-events.jsonl` + `next-eligible.txt`, breaks cleanly. Status command updated to surface rate-limit events + next-eligible countdown. Help text documents the new env var.
- 6 stale lock files cleaned across two waves (initial 4 + post-2-tab smoke 2).

**Decisions:** Multi-tab parallelism dropped — Max 5h cap saturates faster than wall-clock benefit (2 tabs hit wall ~60 min; 6 tabs ~30 min). 1-tab + 90-min throttle is the working config. Detection blind spot uncovered: Max-plan session walls appear as plain-text `"You've hit your org's monthly usage limit"`, not as stream-json `rate_limit_event` — current grep doesn't catch them. Filed as future polish (extend grep patterns). Empirical surprise: batch-0012 ran at $3.42 / 23.8 min / 1.3M cache_read — **16x lower cache_read** than multi-tab batches, projected 5-7 batches per 5h window with ~50% headroom for Matt's other Claude use. Hypothesis: 1-tab serial keeps Anthropic's prompt cache warm; multi-tab fragments it.

**Mission state at session end:** 12/201 batches done, $50.09 cumulative, 0 stuck, 189 queued. Final worker is in 90-min sleep with `/tmp/stage4-stop` set — will exit cleanly on wake.

**What's next:**
- **Spot-check batch-0012 quality + Haiku comparison** (NEXT). → continue: `progress/continue-prompts/2026-05-15-stage4-batch-quality-check.md` (**Opus 4.7** — cross-model audit; auditing Sonnet output with Sonnet misses Sonnet-systematic biases; verdict gates ~$700 of bulk-run downstream). Verdict gates bulk resumption.
- **Resume bulk run** after quality check passes — `weirwood stage4 1` (90-min throttle); stop file auto-clears on launch.
- **Per Matt's standing rule, /endsession was explicitly authorized this session — not auto-triggered.**

---

### Session 52 — Edge Vocabulary Drift Cleanup (2026-05-13)

**Detail:** `history/session-details/session-052.md`

**Changes made:**
- `reference/architecture.md` — rewrote vocabulary-lock callout (line 454-465) to distinguish master vocabulary (~96 types across 14 subsections) from wiki-infobox subset (~26 types). Added `WRITTEN_BY` to Narrative & Literary subsection. Added reverse-direction rows: `HELD_BY` (after HOLDS_TITLE), `KILLED_BY` (after KILLS), `DECEIVED_BY` (after DECEIVES). Added deprecation note on `LOCATED_AT` description noting `LOCATED_IN` as deprecated synonym.
- 21 graph files in `graph/nodes/_conflicts/` — normalized `LOCATED_IN` → `LOCATED_AT`. Final state: 0 LOCATED_IN, 59 LOCATED_AT.
- `reference/design-philosophy.md` (line 91) — "22 edge types" → "~96 edge types".
- `.claude/agents/schema-drift-auditor.md` (line 16) — updated to reference both master and subset tables.
- `.claude/agents/prose-edge-classifier.md` — 3 spots: First Steps (line 14) repointed at master section with explicit perception/narrative/prophecy verb expansion; Vocabulary Lock (line ~74) replaced 22-type hardcoded list with full 14-category expansion (~96 types) referencing architecture.md as source of truth; Definition of Done (line ~131) "22 edge types" → "master vocabulary (~96 edge types)".
- `next.md` — added top-of-file `★ NEXT RECOMMENDATION` callout for Stage 4 wiki-prose edge classifier. Updated "Where we are today" (date, current node/edge counts, vocab cleanup summary). Expanded Track 5 with "tier-difference not polish" framing + "no book passes required" clarification + Open Question on run shape (single-session vs watcher+workers).
- `history/session-details/session-052.md` — NEW. Long-form record of discovery + decisions.

**Decisions:** Edge vocabulary is the master `## Edge Types` section in architecture.md (~96 types). Wiki-infobox table is a parser-only subset (~26 types). Prose-edge-classifier emits from the master (it had been incorrectly restricted to the subset — a real bug, not just stale doc). Reverse-direction edges (HELD_BY/KILLED_BY/DECEIVED_BY) are documented as semantic equivalents — query layer treats `HELD_BY(a→b)` as identical to `HOLDS_TITLE(b→a)`. LOCATED_IN normalized to LOCATED_AT (was 21 instances all in _conflicts/). Stage 4 reframed: not "edges incrementally improve graph"; rather, 37 of the 96 master types are entirely unpopulated (perception/identity/prophecy/narrative/causal verbs) and Stage 4 turns "structured feudal wiki" into "graph that knows the story." Tier-difference. Run-shape question (single-session vs watcher+workers) deferred until candidate volume is known.

**What's next:**
- **Stage 4 wiki-prose edge classifier** (NEXT). Pre-flight: re-run cross-references + edge-candidates scripts (deterministic, free). Then 3-bucket smoke test. → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- Per Matt's standing rule, /endsession was explicitly approved this session — not auto-triggered.

---

### Session 51 — Watcher-Day Orchestration + Session-Results Convention (2026-05-12)

**Detail:** `history/session-details/session-051.md`

**Changes made:**
- Spot-check of 10 Track B nodes; 2 in-place edge fixes: `damon-dance-for-me.node.md` + `henly-maester.node.md` (SERVES: ramsay-bolton → ramsay-snow).
- `scripts/orphan-edges-audit.py` rerun → `working/audits/orphan-edges-2026-05-12.md` + cat1-full.tsv (baseline before Session 50).
- `progress/continue-prompts/2026-05-12-orphan-batch-top-nodes.md` — drafted; used by Session 50; deleted at end-of-session.
- `working/session-results/README.md` — NEW. Convention doc for watcher-handoff result files.
- `working/session-results/2026-05-12-watcher-day-orchestration.md` — NEW. This session's result file (demo + handoff).
- `working/runbooks/general-watcher.md` — updated. First-steps checks `working/session-results/`; signal table + commands include it; "check first" guidance added.
- `working/todos.md` — three new entries: MED Track A spot-check; NEW bake-session-results-into-future-prompts; FUTURE session-state.jsonl upgrade.
- Three commits: `bc19163e4` (Sessions 43-49b, 2587 files), `c54719d40` (Session 50 + convention, 372 files), `4349a62e6` (worklog rotation, 2 files).

**Decisions:** Session-results convention chosen as minimal unlock for watcher friction (per-session file vs shared log vs worklog). Worklog rejected — written too late and conflict-prone for parallel sessions. Per-file is append-by-different-actors, zero merge surface. Session 47 archived to `history/worklog-archives/archive010.md`.

**What's next:**
- **Stage 4 prose-edge-classifier** — next major track (sequential per Matt). → continue: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`. Pre-flight TODO: bake session-results write step into that prompt before firing.
- **MED — Track A 60-node spot-check** — partially absorbed by Session 50 audit improvement; residual remains. See `working/todos.md`.

---

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
