# Agent Inventory

All agent definitions live in `.claude/agents/`. The orchestrator (main Claude Code session) delegates to these — they execute, they don't coordinate. The fleet design philosophy is in `reference/design-philosophy.md`; the strategic plan + dependency-driven ordering is in `working/agent-fleet-specs/agent-pipeline-plan.md`.

**Hard rules every agent in this fleet honors** (see `reference/design-philosophy.md` for rationale):
- One reasoning task per agent.
- Single-writer-per-file invariant.
- Text streams (markdown / JSONL) as universal interface.
- No subagent calls another subagent — composition belongs to the orchestrator.
- No HTTP. No fetching the wiki (it's local).
- No inventing edge types. The locked vocabulary is in `reference/architecture.md`.
- No emitting `first_available` (spoiler gating deferred).
- **Package + global-install policy.** Code-writing agents (script-builder, frontend-developer, backend-developer, deployment-engineer, embedding-refresh-runner, etc.) MUST: never run global installs without explicit user approval; never use suspicious / typosquat / unmaintained packages; always justify dependencies with name + version + alternatives considered; show diffs before applying settings.json changes. Full rules + canonical package choices in `reference/package-install-policy.md`.

---

## Active Agents (in current use)

| Agent | File | Status | Pass | Purpose |
|-------|------|--------|------|---------|
| `mechanical-extractor` | `mechanical-extractor.md` | Full prompt (v3) | Pass 1 | Reads ONE chapter file → produces structured extraction (12 categories: characters, locations, artifacts, events, relationships, food, hospitality, descriptions, spatial layout, etc.). One extraction per chapter. AGOT complete; ACOK/ASOS/AFFC/ADWD pending. |
| `script-builder` | `script-builder.md` | Full prompt | Utility | Writes Python scripts. Used heavily for pipeline scripts. |
| `status-reporter` | `status-reporter.md` | Full prompt | Utility | Surveys repo, counts artifacts, produces detailed progress report. Read-only. |

## Archived Agents (preserved for re-runs only)

| Agent | File | Status | Notes |
|-------|------|--------|-------|
| `wiki-ingester` | `wiki-ingester.md` | Archived (Stage 1 prompt) | Stage 1 used this for full-node authoring of 855 core-tier wiki nodes. Stage 3 replaced the role with `wiki-pass2-emit-deterministic.py` + `wiki-pass2-extract-prose.py` (Python-only). Prompt kept for re-running any of the 37 Stage-1 buckets. |

## Stage 4 Agents (Wiki Pass 2 prose-derived edge discovery)

The next pipeline step. Hybrid pattern: deterministic Python preprocessing → narrow-scope agent classification → deterministic Python promotion.

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `prose-edge-classifier` | `prose-edge-classifier.md` | **Full prompt (priority)** | Classifies candidate edges from prose narrative. Reads candidate JSONL + source/target node prose. Decides edge_type from locked vocabulary OR rejects as just-mention OR escalates. Emits `prose-edges/<slug>.edges.jsonl`. |
| `cross-identity-detector` | `cross-identity-detector.md` | **Full prompt (priority)** | Detects when two graph nodes represent the same entity (Reek=Theon). Reads explicit-redirect + alias-overlap + prose-escalation candidates. Emits `SAME_AS` decisions to `cross-identity-decisions.jsonl`. |
| `disambiguation-resolver` | `disambiguation-resolver.md` | Stub | When prose says "King Aegon" without a wiki link, picks which Aegon (I-V or unnumbered). Reads surrounding context + chronology hints. Stub until Stage 4 candidates accumulate. |
| `contradiction-surfacer` | `contradiction-surfacer.md` | Stub | Compares wiki claims to Pass 1 chapter extractions; surfaces disagreements. Read-only. Stub until Pass 1 completes for ≥2 books. |
| `multi-type-entity-resolver` | `multi-type-entity-resolver.md` | Stub | Reviews multi-type entity cases (Citadel = org+place, Faith of the Seven = religion+org). Decides keep-single-node-v1 / propose-schema-split / emit-cross-type-edges. Stub until Stage 4 prose-edges reveal traversal patterns. |

## Quality / Cleanup Agents (run periodically; high-value immediately)

These don't gate any pipeline step. Run them periodically to catch drift and surface bugs in the existing graph.

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `schema-drift-auditor` | `schema-drift-auditor.md` | **Full prompt (priority)** | Walks graph nodes; finds frontmatter type strings not in TYPE_DIR_MAP, edge labels not in locked vocabulary, frontmatter schema violations, slug-format violations. Read-only. Produces `working/audits/schema-drift-<date>/execution/schema-drift.md`. |
| `citation-validator` | `citation-validator.md` | **Full prompt (priority)** | Walks graph nodes; verifies every claim has a valid citation and every citation resolves. Distinguishes Pass-1-pending from genuinely broken. Produces `working/audits/citation-issues-<date>/execution/citation-issues.md`. |
| `duplicate-detector` | `duplicate-detector.md` | **Full prompt (priority)** | Finds nodes that may be duplicates via slug-similarity, alias-overlap, or shared `wiki_source`. Outputs candidates for `cross-identity-detector` to review. |
| `orphan-edge-finder` | `orphan-edge-finder.md` | **Full prompt (priority)** | Walks graph edges; identifies edges whose targets resolve to no node (after exhausting alias-resolution). Distinguishes genuinely-missing-target from slug-mismatch noise. |
| `extraction-quality-auditor` | `extraction-quality-auditor.md` | Stub | Reviews a batch of Pass 1 extractions for cross-chapter consistency. Stub — fill out per book as Pass 1 completes for each. |
| `cross-book-entity-reconciler` | `cross-book-entity-reconciler.md` | Stub | After multi-book Pass 1, suggests aliases to add to existing graph nodes (Theon↔Reek, etc.). Stub — depends on ≥2 books complete. |

## Pass 3 Agents (Voice & Perception)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `voice-analyzer` | `voice-analyzer.md` | Stub | Per-POV character voice profile (vocabulary, sentence rhythm, characteristic blind spots). One profile per POV. |
| `perception-mapper` | `perception-mapper.md` | Stub | Cross-POV perception edges: how does each POV see each other character? Emits `PERCEIVED_AS`, `RESENTS`, `FEARS`, etc. (vocabulary expansion required). |

## Pass 4 Agents (Foreshadowing)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `foreshadowing-scanner` | `foreshadowing-scanner.md` | Stub | Maps foreshadowing patterns from `reference/foreshadowing-events.md` to chapter occurrences. |
| `chekhovs-gun-tracker` | `chekhovs-gun-tracker.md` | Stub | Tracks planted-but-unresolved details from the Chekhov's gun list. Different reasoning shape from foreshadowing-scanner: looks for absences. |

## Pass 5 Agents (Theory-Informed)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `theory-extractor` | `theory-extractor.md` | Stub | Extracts textual evidence for/against known theories. One pass per theory in `reference/theory-seeds.md` (file not yet created). |
| `theory-evidence-scorer` | `theory-evidence-scorer.md` | Stub | Reviews accumulated evidence for one theory; assigns confidence; identifies strongest support + counter-evidence + load-bearing assumption. |

## Pass 6 Agent (Open-Ended Discovery)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `discovery-agent` | `discovery-agent.md` | Stub | Open-ended pattern discovery across the full extraction corpus. Runs LAST — sees everything. Output goes to curation queue for Matt review. |

## Tier 3 Deferred (Chronology)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `chronology-extractor` | `chronology-extractor.md` | Stub (Tier 3 deferred) | Ingests year pages (130-ac, etc.); emits `OCCURRED_IN_YEAR` and `PRECEDES`/`FOLLOWS` edges. Year pages don't become graph nodes themselves. Vocabulary expansion required. |
| `event-orderer` | `event-orderer.md` | Stub (Tier 3 deferred) | Orders events finer-grained-than-year using cite_refs + causal-language hints. Runs after chronology-extractor. |

## Reviewer Agents (orchestrator-invoked, sample-based peer review)

These agents are NOT recursive subagent calls — the orchestrator invokes both the classifier and the reviewer separately, with composition via on-disk JSONL. See `working/agent-fleet-specs/fleet-orchestration-plan.md` § "Self-review pattern".

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| `prose-edge-reviewer` | `prose-edge-reviewer.md` | Stub | Reads stratified 5-10% sample of `prose-edge-classifier` output per bucket; surfaces systematic biases, structural malformation, edge_type-vs-snippet mismatches. Emits CLEAN/CONCERNS/SYSTEMATIC verdict per bucket. |
| `cross-identity-reviewer` | `cross-identity-reviewer.md` | Stub | Reads 100% of `cross-identity-detector`'s `SAME_AS` proposals (low volume, high stakes); per-proposal verdict (confirm / reject / escalate). |
| `fleet-stats-reviewer` | `fleet-stats-reviewer.md` | Stub | After each major stage, synthesizes the stage's stats CSV + audit reports + reviewer reports into a one-page TL;DR with a recommended next action (PROMOTE / REVIEW / RETRY / ESCALATE / ASK MATT). |

---

## Agent Status Key

- **Full prompt** — Complete, tested, ready to run
- **Full prompt (priority)** — Complete and runnable; written in Session 26 as a high-priority addition
- **Stub** — File exists with role description and key constraints; full prompt body deferred until prerequisites are met (Pass 1 progress, vocabulary expansion, candidate accumulation, etc.)
- **Archived** — Prompt preserved but no longer the active path; replaced by deterministic Python or by a different agent role

---

## How Agents Run

Pipeline agents (Pass 1-6) are invoked by shell scripts in `scripts/` or directly by the orchestrator via the Agent tool. Each invocation is a fresh Claude session with no shared context — the agent reads the project files it needs from disk.

Stage 4 agents (Wiki Pass 2 prose-derived edge discovery) are invoked by `wiki-pass2.sh` or directly by the orchestrator, one bucket at a time. They write to per-bucket `working/wiki/pass2-buckets/<bucket>/<artifact-dir>/` paths and never touch `graph/nodes/` directly — Python promoters handle that.

Quality/Cleanup agents are invoked ad-hoc by the orchestrator. Their output is markdown audit reports in `working/audits/`. Read-only on the graph.

The orchestrator never lets a subagent invoke another subagent. Composition belongs to the orchestrator (Unix-shell pattern).

## Where to learn more

- `reference/design-philosophy.md` — Why the fleet looks the way it does (Unix philosophy + worse-is-better + the corollaries)
- `reference/package-install-policy.md` — Operational rules for code-writing agents adding dependencies or changing settings
- `working/agent-fleet-specs/agent-pipeline-plan.md` — Strategic plan: dependency ordering, cost estimates, what's NOT in the fleet (deliberately)
- `reference/architecture.md` — Schema (entity types, locked edge vocabulary, frontmatter requirements, artifact format taxonomy)
- `working/runbooks/wiki-pass2-pipeline.md` — Concrete pipeline example (Stage 3 — the redesign that taught us the fleet philosophy)
