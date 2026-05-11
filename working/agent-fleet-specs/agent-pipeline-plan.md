# Agent Fleet Plan — Weirwood Network

**Last updated:** 2026-04-28 (Session 26)

**Purpose:** A focused-agent fleet plan. Each agent does ONE discrete reasoning task well. Replaces the "few mega-agents" model with the Unix-philosophy approach: small, composable, each with a clean contract.

**Work queue:** This is an operating manual. The live queue of WHAT to work on is `working/todos.md`. The fleet was designed to tackle that queue automatically.

**Why this matters:** Session 26 redesigned Stage 3 of Wiki Pass 2 from "wiki-ingester agent does everything" to "Python emits skeletons + Python extracts prose + Python promotes" because the mega-agent design conflated concerns and introduced agent-paraphrase failure modes. The same lesson applies fleet-wide: an agent's prompt should describe ONE reasoning task, with everything else delegated to Python pre/post-steps or to other focused agents.

**Hard rules that bind every agent in this fleet** (no exceptions):
- **Python before Agent.** If a deterministic Python step can produce part of the output, it runs first. Agents only do what genuinely requires reasoning.
- **No HTTP calls.** The wiki cache is local at `sources/wiki/_raw/`. No `WebFetch`, `curl`, or remote anything.
- **Don't invent edge types.** The vocabulary is locked at `scripts/wiki-infobox-parser.py::FIELD_EDGE_MAP`. New edge types flow through `reference/architecture.md` § "Wiki Infobox Fields → Edge Type Mapping" FIRST, then the parser.
- **Don't emit `first_available`.** Spoiler gating is owned by a post-release backfill script.
- **Don't modify outputs from prior pipeline stages.** Each agent has a single write path; existing artifacts are read-only inputs.
- **Single-writer-per-file invariant.** Agents write to their own dedicated path under `working/wiki/pass2-buckets/<bucket>/<agent-output-dir>/` (Stage 4 work) or `working/<purpose>/<filename>` (cleanup work). They never write to `graph/nodes/`.
- **Structured output channels for surfacing issues.** Append-only JSONL: `questions-for-matt.jsonl` (when human needed), `conflicts.jsonl` (cross-source disagreements), `pass1-contradictions.jsonl` (wiki vs chapter). Never overwrite; always append.
- **Disambiguation pages never become graph nodes.** Each named individual already has a unique-slugged node. The "which Aegon does this prose mean?" problem is a `disambiguation-resolver` concern at edge-discovery time, not a node-creation concern.

---

## Multi-type entity policy (PROMINENT — established Session 26)

Some wiki pages encode multiple entity types simultaneously: **Citadel** (organization + place), **Faith of the Seven** (religion + organization), **Night's Watch** (organization + sworn brotherhood — handled via `organization.faction` v1 placeholder).

**v1 policy:** emit each as ONE node with the dominant type from the wiki infobox. Don't split into two nodes. Don't add a `secondary_types` field. The "X is also a place" relationship goes in `## Edges` (e.g., `HEADQUARTERED_AT: Oldtown` for Citadel), not in a second node.

**Why:** node duplication breaks slug-based traversal. The graph layer wants one canonical slug per entity.

**Where this gets resolved:** the `multi-type-entity-resolver` agent (Stage 4 sub-task) reviews multi-type cases and decides whether to (a) accept the v1 single-node decision, (b) propose splitting via a schema review, or (c) emit cross-type edges.

---

## The Fleet (24 agents, organized by category)

### Category A — Pass 1: Mechanical Extraction (existing, in active use)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 1 | `mechanical-extractor` | `.claude/agents/mechanical-extractor.md` | Full prompt v3 | Reads ONE chapter file, produces structured extraction (characters, locations, artifacts, events, relationships, food, hospitality, descriptions, spatial layout). One extraction per chapter. AGOT complete; ACOK/ASOS/AFFC/ADWD pending. |

### Category B — Pass 2: Wiki Ingestion (Stage 1 retired, Stage 3 is fully Python — no agents currently active here)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 2 | `wiki-ingester` | `.claude/agents/wiki-ingester.md` | Archived (Stage 1 prompt preserved for re-runs only) | Stage 1 used this for full-node authoring. Stage 3 replaced with `wiki-pass2-emit-deterministic.py` + `wiki-pass2-extract-prose.py`. Prompt kept for re-running any of the 37 Stage-1 buckets. |

### Category C — Stage 4: Prose-Derived Edge Discovery (next pipeline step; 5 specialized agents)

This is the work-in-progress focus. Stage 3 produced 4,239 nodes with infobox-derived edges; Stage 4 finds edges encoded in prose narrative, cross-page references, and Pass 1 chapter extractions. Hybrid pattern: Python preprocessing → narrow-scope agent classification.

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 3 | `prose-edge-classifier` | `.claude/agents/prose-edge-classifier.md` | **WRITE NOW (priority)** | Reads candidate-edge JSONL rows + source prose snippet + target node frontmatter; decides edge_type from locked vocabulary OR rejects as just-a-mention OR escalates to other agents OR files to questions. Emits `prose-edges/<slug>.edges.jsonl`. |
| 4 | `cross-identity-detector` | `.claude/agents/cross-identity-detector.md` | **WRITE NOW (priority)** | Detects explicit-redirect + alias-overlap cross-identity cases (Reek=Theon, Alayne=Sansa). Inputs: wiki redirect graph + alias-overlap candidates. Output: `cross-identity-decisions.jsonl` with proposed `SAME_AS` edges. |
| 5 | `disambiguation-resolver` | `.claude/agents/disambiguation-resolver.md` | Stub | When prose says "King Aegon" without a wiki link, decide which Aegon (I-V, or one of the unnumbered). Reads surrounding context + chronology hints. Output: per-mention disambiguation decisions. |
| 6 | `contradiction-surfacer` | `.claude/agents/contradiction-surfacer.md` | Stub | Compares wiki claims to Pass 1 chapter extractions; surfaces cases where they disagree. Doesn't decide who's right — just surfaces for human review. Output: `pass1-contradictions.jsonl` rows. Hard dependency on Pass 1 completion (only AGOT done as of Session 26). |
| 7 | `multi-type-entity-resolver` | `.claude/agents/multi-type-entity-resolver.md` | Stub | Reviews multi-type entity cases (Citadel, Faith of the Seven). Decides: keep single-node v1 with current type / propose schema split / emit cross-type edges. Output: `multi-type-decisions.jsonl`. |

### Category D — Pass 3: Voice & Perception (multi-agent)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 8 | `voice-analyzer` | `.claude/agents/voice-analyzer.md` | Stub | Per-POV voice profile (vocabulary, sentence rhythm, recurring imagery, characteristic blind spots). One profile per POV character. Hard dependency on Pass 1 completion. |
| 9 | `perception-mapper` | `.claude/agents/perception-mapper.md` | Stub (NEW — split from voice-analyzer) | Cross-POV perception edges: how does each POV see each other character? Emits `PERCEIVED_AS`, `RESENTS`, `FEARS`, `MOURNS` edges. One pass per (POV, target) pair. |

### Category E — Pass 4: Foreshadowing (multi-agent)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 10 | `foreshadowing-scanner` | `.claude/agents/foreshadowing-scanner.md` | Stub | Maps known foreshadowing patterns from `reference/foreshadowing-events.md` to chapter occurrences. Emits foreshadowing→event linkage edges. |
| 11 | `chekhovs-gun-tracker` | `.claude/agents/chekhovs-gun-tracker.md` | Stub (NEW — split from foreshadowing) | Tracks planted-but-unresolved details from `reference/foreshadowing-events.md` Chekhov's gun list. Different reasoning shape from foreshadowing-scanner: looks for absences (still-unresolved) rather than confirmations. |

### Category F — Pass 5: Theory-Informed Extraction (multi-agent)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 12 | `theory-extractor` | `.claude/agents/theory-extractor.md` | Stub | Extracts textual evidence for/against known theories. One pass per theory in `reference/theory-seeds.md` (file not yet created). |
| 13 | `theory-evidence-scorer` | `.claude/agents/theory-evidence-scorer.md` | Stub (NEW — split from theory-extractor) | Reviews accumulated evidence for one theory; assigns a confidence score and identifies the strongest single piece of evidence + the strongest counter-evidence. |

### Category G — Pass 6: Open-Ended Discovery

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 14 | `discovery-agent` | `.claude/agents/discovery-agent.md` | Stub | Open-ended pattern discovery across the full extraction corpus. Runs LAST — sees everything. Surfaces patterns not covered by Pass 4-5 (which are theory-driven). Output: `working/curation/candidates.md` for Matt review. |

### Category H — Quality / Cleanup (utility agents — high value immediately)

These don't gate any pipeline step but should run periodically to catch drift and surface bugs.

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 15 | `schema-drift-auditor` | `.claude/agents/schema-drift-auditor.md` | **WRITE NOW (priority)** | Walks `graph/nodes/**/*.node.md`; finds frontmatter `type:` strings not in `architecture.md`'s TYPE_DIR_MAP; finds edge labels not in the locked vocabulary; finds `first_available` values that don't parse cleanly. Output: `working/audits/schema-drift-<date>/execution/schema-drift.md` report. Read-only. |
| 16 | `citation-validator` | `.claude/agents/citation-validator.md` | **WRITE NOW (priority)** | Walks every node; for each claim that should be cited, verifies the cite_ref or chapter reference resolves to a real file. Flags claims missing citations and citations missing targets. Output: `working/audits/citation-issues-<date>/execution/citation-issues.md`. Read-only. |
| 17 | `duplicate-detector` | `.claude/agents/duplicate-detector.md` | **WRITE NOW (priority)** | Finds nodes that may be duplicates of each other via slug-similarity, alias-overlap, or shared `wiki_source`. Output: candidate merges to `cross-identity-decisions.jsonl` for the `cross-identity-detector` agent to review. Read-only. |
| 18 | `orphan-edge-finder` | `.claude/agents/orphan-edge-finder.md` | **WRITE NOW (priority)** | After alias-resolver runs, finds edges whose targets resolve to no node (after considering aliases). Surfaces real graph gaps (vs. mere slug mismatches). Output: `working/audits/orphan-edges-<date>/execution/orphan-edges.md`. Read-only. |
| 19 | `extraction-quality-auditor` | `.claude/agents/extraction-quality-auditor.md` | Stub | Reviews a batch of Pass 1 extractions for consistency: did all chapters cover the 12 categories? are POV characters tagged consistently? did "Other" buckets get used for things that should have been in named categories? Output: `working/audits/extraction-quality-<batch>.md`. |
| 20 | `cross-book-entity-reconciler` | `.claude/agents/cross-book-entity-reconciler.md` | Stub | After multiple books' Pass 1 complete, reconciles entity references across books: same character with different aliases per book, same location with different naming conventions. Suggests aliases to add to existing nodes. |

### Category I — Tier 3 / Future (deferred work, design now)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 21 | `chronology-extractor` | `.claude/agents/chronology-extractor.md` | Stub (Tier 3 deferred) | Ingests year pages (130-ac, 133-ac, etc.); emits `OCCURRED_IN_YEAR(<event>, <year>)` and `PRECEDES`/`FOLLOWS` edges. Hybrid pattern: Python prep enumerates year pages, agent extracts. Year pages may not become graph nodes; they're sources of temporal edges between existing event nodes. |
| 22 | `event-orderer` | `.claude/agents/event-orderer.md` | Stub | Given a set of events, places them in chronological order using cite_refs + chronology extractor output + prose hints. Emits `PRECEDES`/`FOLLOWS` edges between events. |

### Category J — Meta / Orchestration (utility agents for the orchestrator)

| # | Agent | File | Status | Role |
|---|-------|------|--------|------|
| 23 | `script-builder` | `.claude/agents/script-builder.md` | Full prompt (in active use) | Writes Python scripts. Used heavily for pipeline scripts. |
| 24 | `status-reporter` | `.claude/agents/status-reporter.md` | Full prompt | Surveys repo, counts artifacts, produces detailed progress report. Read-only. |

---

## Suggested ordering (dependency-driven)

```
NOW (next session, deterministic Python first)
 │
 ├── Group A1: alias-resolver script + re-cross-refs (15 minutes)
 │     └── Cuts broken-link rate by ~50% via slug-mismatch fix
 │
 ├── Group A2: edge-candidate generator script (30 minutes)
 │
 ├── Run quality/cleanup agents (#15-#18 — schema-drift-auditor, citation-validator, duplicate-detector, orphan-edge-finder)
 │     └── Establishes baseline; finds real bugs in current 4,239-node graph
 │
 ├── Stage 4 agent runs (#3-#5 — prose-edge-classifier, cross-identity-detector, disambiguation-resolver)
 │     └── 3-5 hours wall-clock, $50-100
 │
PARALLEL (independent of Stage 4)
 │
 ├── Pass 1 ACOK + ASOS via mechanical-extractor (#1)
 │     └── Background-able in separate orchestration tabs
 │     └── Pass 4 / 5 / 6 depend on this
 │     └── #6 contradiction-surfacer also depends on this for full coverage
 │
AFTER PASS 1 COMPLETE (all 5 books)
 │
 ├── #6 contradiction-surfacer (full corpus pass)
 ├── #19 extraction-quality-auditor (batch review across books)
 ├── #20 cross-book-entity-reconciler
 ├── #8-9 voice-analyzer + perception-mapper (Pass 3)
 ├── #10-11 foreshadowing-scanner + chekhovs-gun-tracker (Pass 4)
 ├── #12-13 theory-extractor + theory-evidence-scorer (Pass 5; needs theory-seeds.md)
 └── #14 discovery-agent (Pass 6 — runs LAST)
 │
DEFERRED (post-release)
 │
 ├── #21 chronology-extractor (Tier 3)
 ├── #22 event-orderer
 └── Spoiler-gating `first_available` backfill (deterministic Python; no agent)
```

---

## Cost / time estimates (rough)

| Phase | Agents involved | Cost | Wall-clock |
|-------|-----------------|------|------------|
| Quality/cleanup audits | #15-#18 | $5-15 each | <1 hour each |
| Stage 4 hybrid | #3-#5 | $50-100 total | 3-5 hours total |
| Stage 4 contradictions (post Pass 1) | #6 | $20-40 | 2-4 hours |
| Pass 1 remaining 4 books | #1 | ~$95/book × 4 = ~$380 | 4-8 hours per book |
| Pass 3 voice + perception | #8-9 | $100-200 | Multi-session |
| Pass 4 foreshadowing | #10-11 | $50-100 | Multi-session |
| Pass 5 theory | #12-13 | $100-200 | Multi-session |
| Pass 6 discovery | #14 | $200-500 | Multi-session |

Total remaining-work budget: ~$1,500-2,500 across all 6 passes + 4 Pass-1 books + Stage 4 + cleanup + chronology.

---

## What's NOT in this fleet (deliberately)

- **Multiple agents reviewing each other's output.** The `theory-evidence-scorer` reviews evidence; it doesn't review `theory-extractor`'s reasoning. Cross-review introduces convergence-bias risk and isn't worth the cost. Quality is enforced via deterministic validators (Python) and the audit agents (#15-18), not via agent peer review.
- **Agent-orchestrating-other-agents** (recursive subagents). The orchestrator (this main session) coordinates; agents execute. No agent in this fleet calls another agent.
- **Generative agents.** No agent invents new theories, characters, or plot points. All agents are evidence-grounded — they extract, classify, score, or surface. The `discovery-agent` (#14) is the closest to generative but its output goes to the curation queue for Matt's review, never directly into the graph.
- **Long-context "summary" agents.** No agent reads the full corpus and writes a narrative summary. Such agents drift fast and add little value the graph doesn't already encode.

---

## Files this plan ties into

- `working/todos.md` — granular TODO list; this plan is the higher-level grouping
- `working/runbooks/wiki-pass2-pipeline.md` — Stage 3 canonical pipeline (done)
- `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md` — Stage 4 hybrid plan (drafted)
- `reference/architecture.md` — schema (entity types, edge vocabulary, artifact formats)
- `reference/agents.md` — agent roster (sync with this plan)
- `.claude/agents/<name>.md` — per-agent prompts (priority 5 written this session; rest are stubs)
