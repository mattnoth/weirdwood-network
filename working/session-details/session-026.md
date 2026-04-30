# Session 26 — Stage 3 Completion + Tier-Recovery + Fleet Architecture + Chat UI Design

**Date:** 2026-04-27 → 2026-04-28 (multi-day session)
**Continue prompt entering session:** `progress/continue-prompts/2026-04-27-wiki-pass2-stage3-finish.md`
**Continue prompt leaving session:** none (every concrete work track has a documented next step in `working/agent-pipeline-plan.md` + `working/fleet-orchestration-plan.md`)

## What this session was

This was an **enormous multi-arc design session** that started as "finish Stage 3 of wiki Pass 2" and ended as "design the entire downstream architecture of the project from end of Pass 2 through chat UI deployment to Matt's D&D group." Probably 7-8 hours of work across multiple sittings. Matt was leaving town and explicitly authorized "do as much as you can without my input"; I took that as license to follow the design rabbit holes wherever they led.

The session has two distinct phases:

**Phase 1 (execution-heavy):** Finish Stage 3 of Wiki Pass 2 — the secondary-tier ingestion. This phase did real concrete work: wrote scripts, ran them, promoted nodes to the graph, ran recovery passes for missing entities. Quantitative outcomes here.

**Phase 2 (design-heavy):** Once Stage 3 was done and broken-link analysis surfaced what's actually missing, the session pivoted to designing the rest of the project: agent fleet plan, runtime architecture for multi-day autonomous orchestration, monitoring skill, chat UI architecture, deployment posture, etc. Almost no code in Phase 2 — pure architectural design and documentation.

The two phases are linked: Phase 1's empirical findings (broken-link distribution, slug-mismatch patterns, missing-entity audit) informed Phase 2's design. Without running Stage 3 first, the architecture design would have been speculative.

---

## Phase 1: Stage 3 completion (execution-heavy)

### Stage 3b agent → Python redesign (the big mid-course correction)

Entering this session, the plan from Session 25 was: Stage 3a (Python skeletons, done) + mid-stage agent review + Stage 3b (LLM agent prose-fill on Tier A only) + validator byte-equality enforcement.

About 30 minutes in, while drafting the Stage 3b agent prompt, Matt asked the obvious-in-hindsight question: "We need to rewrite the prose? I don't understand that — don't we already have the prose wrapped in HTML tags?"

This led to a fundamental redesign. The wiki HTML already contains the prose. A Python extractor with a deterministic h2→schema-heading mapping table can produce the prose body sections without an agent. Original budget: $70 / 6 hours / agent paraphrase risk. New budget: $0 / ~14 seconds / fully deterministic.

Before committing, I spawned a **fresh general-purpose agent** to second-opinion the redesign (briefing in `working/scratch-design-review-stage3b.md`). Verdict: SOUND, three small adjustments — preserve `<h3>` book boundaries inside `## Narrative Arc` for future spoiler-gating, skip-don't-dump for unmapped sections, both `Quotes by X` and `Quotes about X` map to `## Quotes` with subheading preservation. All three accepted.

The Stage 3b agent prompt I had written got rolled back; the Stage 1 wiki-ingester prompt was restored with a header note explaining the Stage 3 redesign. Wasted work, but cheap (one Write call). Sunk cost.

### Stage 3b Python implementation + run

Built `scripts/wiki-pass2-extract-prose.py` (~770 lines). Ran on test bucket `houses-other-h-w` (14 pages); validated. Ran full --apply across 472 buckets in ~14 seconds → **2,988 prose files emitted from 3,315 candidate pages (90.1% hit rate)**.

After the first run, top unmapped sections were heavily concentrated in battle pages (`Aftermath` 151, `Prelude` 134, `Battle` 84, `Synopsis` 24) and location pages (`Layout` 66, `City` 16). One more script-builder pass added these mappings + `## Aftermath` as a new schema heading + `Background`/`Legend`/`Character and Appearance` mappings. After the second run: 2,988 → 2,988 (1 dropped because empty-files-suppressed), but mean word count climbed 262→294, broken-link rate dropped further.

Schema-decision side effects:
- New `## Culture` and `## Organization` schema headings added (Night's Watch's wiki page has substantial Organization content with 5 h3 subsections; Velaryon and Windblown have Culture sections)
- `## Aftermath` added for battle pages
- All decisions documented in `working/runbooks/wiki-pass2-pipeline.md` (rewritten as v3)

### Stage 3-promote (concatenation + atomic-rename)

Built `scripts/wiki-pass2-promote.py` (~585 lines). Single-bucket test passed. Concat verified byte-exact (skeleton + "\n" + prose = final node, byte-identical math). Conflict path tested by manually mutating a destination file and watching it route to `_conflicts/`.

Full --apply across 472 buckets: **0.84 seconds**. **3,314 new nodes promoted** to `graph/nodes/`. 0 conflicts. 1 unclassified (`battle-of-the-blackwater-song` — type=unknown, parser edge case routed to `_unclassified/`). Tested idempotency; re-run reports all-byte-equal, zero new writes.

**Graph state after Stage 3:** 4,169 nodes (855 Stage 1 + 3,314 Stage 3) across `characters/` (3,361), `houses/` (315), `events/` (242), `locations/` (151), `titles/` (79), `factions/` (21).

### Cross-references index (Stage 4 prep — unblocked)

Built `scripts/wiki-pass2-build-cross-refs.py` (Step 1 of the Stage 4 hybrid plan from `progress/continue-prompts/2026-04-27-wiki-pass2-stage4-edge-discovery.md`). Walks all 2,988 prose files extracting `[anchor](wiki:Page)` markdown links → 81,090 reference rows in `cross-references.jsonl`. Inverted index in `backlink-counts.json`. Top-50 leaderboard rendered to `cross-refs-summary.md`.

Sanity-check passed: all 6 expected major-character slugs appear in top-20 (Jaime, Tyrion, Jon, Stannis, Cersei, Daenerys). Top-1 is `kings-landing` at 833 references.

But: **34,782 broken links (42.9% of total)** — meaning slugs referenced in prose that don't exist as graph nodes. Two kinds of broken links discovered through investigation:

1. **Slug-mismatch noise** — Brienne's node is `brienne-tarth.node.md` (Stage 1 agent dropped the "of") but the wiki page is `Brienne_of_Tarth` → kebab `brienne-of-tarth` → no slug match. Resolvable via alias-resolver.
2. **Genuinely missing entities** — `house-lannister`, `house-frey`, `house-bolton`, etc. — major narrative spine NOT in the graph.

### Tier 1 + Tier 2 entity recovery (the unexpected finding)

A quick audit (using `working/wiki-parsed/backlink-counts.json` against existing graph slugs) revealed 100 most-referenced entities NOT in the graph, accounting for 12,838 broken refs (37% of the 34,782 total).

Categorized into three tiers:
- **Tier 1** (definitely recover, narrative spine): 5 missing major houses (Lannister, Frey, Bolton, Greyjoy, Baratheon parent), 14 regions (Westeros, North, Reach, etc.), 16 locations (Iron Throne, Wall, Red Keep, Castle Black, etc.), 10 pre-narrative Targaryens (Aegon I-V, Aerys II, Aenys I, Viserys I, Daemon, Corlys), 2 characters (Gendry, Gilly).
- **Tier 2** (important but schema-question): 4 religions, 12 titles, 6 cultures, 2 organizations.
- **Tier 3** (defer): year/calendar pages, generic concept pages.

Built **two recovery buckets** (`houses-major-recovery` + `tier2-recovery`) by directly creating the manifest.json structure + skipping triage, then ran the full Stage 3 pipeline (emit-deterministic → extract-prose → patch types where parser left them as `unknown` → promote). Ran each in ~5-10 minutes total.

**Recovery result:** 46 + 24 = **70 new nodes promoted**. Cumulative graph went 4,169 → 4,239.
**Broken-link rate:** 34,782 → 31,933 (Tier 1, -2,849) → 29,291 (Tier 2, -2,642). Total: -5,491 broken links eliminated.

Surprise findings during recovery:
- House Tully, House Tyrell, House Martell, House Arryn ARE in graph — earlier assumption that "all major houses missing except Stark and Targaryen" was wrong
- Lannister/Frey/Bolton/Greyjoy/Baratheon (parent) genuinely missing — these were never in any Stage 1 OR Stage 3 bucket
- 1 likely wiki typo: `bellenora-otherys` vs `bellonara-otherys` — same person, different spelling, two separate nodes

### Alias-resolver (smoke-tested as Stage 0 of fleet plan)

After Phase 2's design discussion, came back and built `scripts/wiki-pass2-build-alias-resolver.py` to validate the architecture's foundation layer was buildable. Walks every node's frontmatter `aliases` field, builds `wiki_form_kebab → canonical_slug` map. Idempotent in content (timestamp moves, structured data stable).

Result: 1,373 alias strings → 1,175 resolver entries → **707 broken refs reclaimed** (2.4% of remaining 29,291). LOWER than my 5K-15K estimate — but informative. Most "broken" refs are genuinely missing concept entities (`dragon`, `weirwood`, `smallfolk`, `years-after-aegons-conquest`), NOT slug-mismatches. The deferred concept-pages decision is validated by this empirical signal.

Top 10 alias collisions captured genuine in-universe ambiguity:
- `the-prince-that-was-promised` → 4 candidates (Aegon-son-of-Rhaegar, Daenerys, Rhaegar, Stannis) — exactly the kind of contested identifier we shouldn't auto-resolve
- `wolf-girl` → Arya/Lyanna/Sansa
- `ned` → Eddard Stark / Edric Dayne

### Edge schema discussions (temporal + multi-type)

Two important schema conversations surfaced:

**Multi-type entities** (Citadel = org+place, Faith of the Seven = religion+org): v1 policy = ONE node per entity with dominant infobox-type. Future Stage-4 `multi-type-entity-resolver` agent reviews; agent decides keep-single-node-v1 / propose-schema-split / emit-cross-type-edges. Documented PROMINENTLY in `working/agent-pipeline-plan.md` and todos.md.

**Temporal edges** (RULES: Winterfell — but rulers change over time): current schema handles via bracketed qualifiers (`SPOUSE_OF: Lysa Tully [third wife]`). For temporal range queries we'd need v2: keep bracket for human readability AND add OPTIONAL structured `start_year` / `end_year` / `precision` / `scope` / `start_event` / `relation` fields. Defer until query-pattern signal demonstrates it's needed; v1 is fine without.

**Per-entity index tables**: `graph/index/<type>/<slug>.index.json` — derived view aggregating outbound + inbound edges + chapter appearances + node mentions + timeline. Already in architecture.md's Artifact-Format-by-Consumer table; build a Python script post-Stage-4.

---

## Phase 2: Architecture design (design-heavy)

Once Stage 3 was done and broken-link analysis revealed the project's real shape, the conversation pivoted to "okay, what does the rest of the project look like?" Each design decision led to the next; here's the chain:

### Design philosophy crystallization

The Stage 3b agent → Python redesign forced an explicit articulation of the project's design philosophy. Wrote `working/design-philosophy.md` covering:
- Unix philosophy (one thing well, work together, text streams as universal interface)
- Worse-is-better corollary
- Anti-patterns explicitly rejected (featuritis, hidden coupling, recursive complexity, composition through inheritance)
- Single-writer-per-file invariant
- The contrast with the Lisp-Machine / Smalltalk philosophy and why pipelines aren't IDEs

This became the canonical reference for "why does the architecture look the way it does." Later additions: peer review IS allowed (orchestrator-driven sample-based, not recursive), and a Package + Global-Install Policy section.

Matt asked "what makes this Unix philosophy?" → wrote a focused explanation that he liked enough to ask me to record (which I did, as `working/design-philosophy.md`). Also asked "what is text streaming?" → covered in same doc.

### Agent fleet expansion (4 → 27 agents)

Initial Stage 4 design had 4 agent roles (prose-edge-classifier + cross-identity-detector + disambiguation-resolver + chronology-extractor). Matt pushed back: "only four for all the todos?"

Walked through ALL the project's pending work and the existing agent definitions. Built `working/agent-pipeline-plan.md` with 24 categorized agents. Then added 3 more for orchestrator-invoked sample-based peer review (`prose-edge-reviewer`, `cross-identity-reviewer`, `fleet-stats-reviewer`) → 27 total.

Wrote 6 detailed prompts (`prose-edge-classifier`, `cross-identity-detector`, `schema-drift-auditor`, `citation-validator`, `duplicate-detector`, `orphan-edge-finder`) and 13 stubs. The 6 detailed ones are runnable today; the 13 stubs have role descriptions + key constraints + "build out when prerequisites met" notes.

Key design distinction surfaced: **subagent-calling-subagent is disallowed (recursion)**, but **orchestrator-invoking-multiple-subagents-where-one-reads-another's-text-output is allowed (composition)**. Earlier "no peer review" position was an over-correction; updated `design-philosophy.md` with the soft correction.

### Multi-day orchestration architecture

Matt asked about long-running unattended orchestration: "I want it to run for multiple days without my interference, but I want to monitor it." This led to `working/fleet-orchestration-plan.md` covering:
- Stage DAG (all 12 stages with dependencies)
- Stats schema (per-agent CSV adapted from mechanical-extraction's pattern)
- Wave-based parallelism with concurrency caps
- Rate-limit detection + 3-tier graceful backoff (per-agent skip → whole-wave pause → whole-stage pause)
- Sample-based peer review (5% per bucket for prose-edge, 100% for cross-identity)
- Idempotent re-runs (manifest-driven)
- Self-generating prompts for vocabulary-gap responses (orchestrator-driven, not recursive)

Then `working/fleet-runtime-architecture.md` for the operational side:
- The orchestrator daemon is **NOT a Claude Code session** — it's a Python process that subprocess.run's `claude --print --agent <name>` for each invocation. Sidesteps session limits entirely. Same pattern as wiki-pass2.sh.
- tmux for persistence (survives terminal close)
- State files on disk continuously (orchestrator-state.json, log, stats CSVs, checkpoint)
- Layer 4: per-stage scripts as the no-daemon escape hatch — every stage liftable, runnable manually
- Resilience: 4 scales of failure isolation (agent-level, wave-level, stage-level, orchestrator-level)
- Coordinator pattern for auto-respawn of dead stages

Matt's insight that pulled this together: "if we use the Unix ideology, each stage will be its own little orchestration that we could take out of the chain if I want more direct control." Made that explicit in the architecture doc.

### Monitoring skill

Built `.claude/commands/check-fleet.md` — a slash command Matt runs in a fresh Claude Code session to check fleet status without leaving Claude open. Verb-rich: `status` / `questions` / `answer Q-ID` / `pause` / `resume` / `stop` / `cost` / `diff` / `dag` / `tail-log` / `health` / `spot` / `dry-run-next-stage` / `anomalies` / `continue-prompt` / `divert`.

Degrades gracefully today (orchestrator daemon doesn't exist yet) — reports on EXISTING orchestration state (mechanical-extraction stats, wiki-pass2 manifests, questions-for-matt.jsonl). Same skill works tomorrow against the daemon's state files. No code change needed when daemon ships.

### Chat UI architecture

This was the biggest design pivot. Started as "personal local chat UI" → ended as "deployable preview for Matt's D&D group with full prose retrieval including books, hosted at `mattnoth.com/projects/<slug>`."

Key decisions in `working/chat-ui-architecture.md`:
- **Three corpora, one join key**: graph nodes + wiki prose chunks + book chapter chunks, all joined on slug. Mention-tagging in chunk metadata makes graph + prose retrievable together.
- **Slug as universal foreign key**. Wiki prose has markdown links → trivial slug extraction. Book chapters have no links → use Pass 1's per-chapter mention list resolved via alias-resolver.
- **Spoiler gate fully OPEN for v1** — no `first_available` filtering. Saves complexity in chunker + embedding pipeline + query layer. v2 spoiler-gating is additive.
- **Book copyright posture**: friend-group-only behind auth, synthesis-not-quotation enforced in LLM system prompt, snippet-limited source rendering, ready-to-remove-if-asked. Defensible-enough for D&D group scale.
- **Stack**: pure TS + native modern CSS (matches mattnoth-dev's existing rules — no React, no Tailwind, no CSS-in-JS, no Sass). esbuild bundler. Discovered after reading mattnoth-dev's `CLAUDE.md` and `package.json` that the stack alignment was already perfect.
- **Submodule pattern**: asoiaf-chat repo included as a git submodule of mattnoth-dev. Component lives in `ui/ts/` and `ui/styles/` here; mattnoth-dev imports via path.
- **Specialist-subagent boundary**: chat component code → asoiaf-chat repo's UI-build fleet (frontend-developer, etc.). Page template + integration glue → mattnoth-dev's specialists (build-specialist, css-specialist, ts-specialist, content-specialist, reviewer).
- **Backend stays separate**: Python FastAPI on Render/Fly.io. Vector store = SQLite + sqlite-vec, bundled with backend. Anthropic API key server-side.

### UI build fleet (separate from construction fleet)

Matt: "This UI build should have its own agent process." Right — construction fleet ("ingest a corpus, ship structured output", bounded) and UI build fleet ("iterate on a product based on user feedback", continuous) have different work shapes. Added 7 UI-build agents as stubs (`frontend-developer`, `backend-developer`, `prompt-engineer`, `deployment-engineer`, `chat-ui-tester`, `ux-feedback-analyzer`, `embedding-refresh-runner`) with their own tmux session and own state files. The `/check-fleet` skill is multi-orchestrator-aware so monitoring stays unified.

### Diagrams doc

Matt: "readable / smaller focused diagrams for human accompaniment would be good." Wrote `working/diagrams.md` — 14 small focused diagrams as scan-in-30-seconds reference. Each links to its deep doc.

### Package + global-install safety policy

Matt: "add a prompt to install anything global or any suspicious packages." Added comprehensive policy section to `working/design-philosophy.md`:
- No global installs without explicit user approval (npm install -g, pip install --user, brew, etc.)
- Project-local installs only, in venvs, pinned in lockfiles
- Reliable packages only (>100k weekly downloads, recent maintenance, recognizable maintainer, no typosquats)
- Canonical package choices spelled out per category (LLM SDK = anthropic only; vector DB = chromadb/lancedb/sqlite-vec; HTTP = requests/httpx; markdown = marked/markdown-it)
- Settings.json updates require user-visible diffs
- Codify at .claude/settings.json deny-rule level (belt-and-suspenders)

---

## Numbers

**Graph state at end of session:**
- Nodes: 855 (Stage 1) → 4,239 (after Stage 3 + Tier 1 + Tier 2 recovery)
- Distribution: 3,361 characters / 322 houses / 242 events / 178 locations / 91 titles / 29 factions / 4 religions / 1 unclassified
- Broken cross-refs: 34,782 → 29,291 (Stage 1+2 recovery, -5,491) → 28,584 (alias-resolver-resolvable, -707 more)
- Total deliverables: 27-agent fleet, 12-stage DAG, 6 deep architecture docs, 14 quick-reference diagrams, 1 monitoring slash command

**Cost this session:** ~$0 (alias-resolver and recovery pipelines are pure Python; only cost was the second-opinion review agent at maybe $1).

**Time invested:** large multi-sitting session; probably 7-8 hours of conversation + execution.

---

## Where we are now

Concrete pipeline state:
- ✅ Stage 0 foundation (alias-resolver) — built and run
- ✅ Stage 1 quality audits — agents written (full prompts), runnable
- 🔄 Stage 2 prose-edge classification — agent prompt full, candidate generation script not yet built
- 🔄 Stage 3 peer review — agent prompts stub, runnable post-classification
- 🔄 Stage 4 promote — script not yet built
- ⏸ Stage 5+ — Pass 1 catch-up across 4 books, depends on mechanical-extractor runs
- ⏸ Stage 6+ — Pass 1 quality (extraction-quality-auditor stub, depends on Pass 1 done)
- ⏸ Stage 7-10 — Pass 3-6, all stubs, depends on Pass 1 done
- ⏸ Stage 11 — Tier 3 (chronology-extractor, event-orderer stubs)
- ⏸ Stage 12 — `first_available` backfill (post-release)

Not yet built:
- Fleet orchestrator daemon (`scripts/fleet-orchestrator.py`)
- Per-stage scripts (`weirwood fleet stage <N>` interface)
- Stats helper (`scripts/fleet_stats.py`)
- `weirwood fleet start/status/stop/attach/resume` shell commands
- Edge-candidate generator script (Stage 2 prep)
- Stage 4 promoter script
- 21 agent stubs need their full prompts when their stages approach
- Vector embedding pipeline + chunkers + retrieval layer (chat UI side)
- Backend FastAPI service
- Frontend chat component (TS + CSS)
- mattnoth-dev integration (page template, content markdown)

The bottleneck is **Pass 1 catch-up across 4 books** (ACOK, ASOS, AFFC, ADWD). Stage 4 contradiction-surfacer, Pass 3-6 agents, book chunking, mention-tagging — all want Pass 1 multi-book coverage. Mechanical-extractor agent already exists and is in active use; just needs to be run.

---

## What surprised me

1. **Stage 3b agent → Python redesign saved $70 + 6 hours**. Inertia of "Stage 1 used an agent so Stage 3b should too" almost cost real money. Matt's instinct to question it was the right call. I cited this in `design-philosophy.md` as the canonical example of when to redesign.

2. **42.9% broken-link rate was lower than slug-mismatch noise alone — most of it is genuinely missing concept entities**. The corpus references many things (dragon, weirwood, smallfolk, year pages) that we deliberately didn't promote. The numbers validated the deferred concept-pages decision instead of contradicting it.

3. **House Lannister, House Frey, House Bolton, House Greyjoy, House Baratheon-parent were missing from the graph despite Stage 1 having processed Lannister-related buckets**. Stage 1 processed CHARACTERS belonging to House Lannister, not the house entity itself. Triage gap.

4. **mattnoth-dev's existing stack (vanilla TS + native CSS + esbuild) was a perfect fit for the chat UI design I'd already drafted**. I was guessing "Next.js? Astro? plain HTML?" — actually plain TS with esbuild, which is what I'd designed for. Lucky.

5. **The Unix philosophy framing keeps paying dividends**. Started as Stage 3b redesign justification. Became the canonical project rationale. Each new design decision (orchestrator daemon, monitoring skill, peer review pattern, multi-orchestrator support, per-stage liftability, single-writer-per-file invariant) maps cleanly onto Unix conventions Matt already understands.

6. **The fleet plan grew from 4 agents to 27** when I actually walked through all the project's pending work. The original 4 was because I'd anchored on "Stage 4 has 4 sub-tasks." Actually the project has many more discrete reasoning tasks — they just hadn't been enumerated.

---

## Decisions made this session (compressed list)

1. **Stage 3b is fully Python** — `wiki-pass2-extract-prose.py` instead of an LLM agent. Single-writer-per-file invariant. Stage 1 wiki-ingester prompt archived for re-runs only.
2. **Concept pages defer (option iii)** — generic glossary pages (Tourney, Marriage, Sept, etc.) not promoted in v1. Empirical broken-link analysis validates this — most aren't real gaps.
3. **Multi-type entities = single node v1** with dominant infobox-type. Future Stage-4 `multi-type-entity-resolver` agent reviews. Documented PROMINENTLY.
4. **Spoiler gate defaults FULLY OPEN for v1**. No `first_available` filtering at chat-UI query time. Saves complexity in chunker + embedding + query. v2 is additive when backfill ships.
5. **Chat UI scope shifted** — personal-local → friend-group-shareable preview at `mattnoth.com/projects/<slug>`. Includes book chunks. Behind shared-password auth. Synthesis-not-quotation prompt rule. Ready-to-remove-if-asked.
6. **Stack confirmed**: pure TS + native modern CSS + esbuild + Netlify (matches mattnoth-dev). Submodule pattern. esbuild compiles the chat component alongside mattnoth-dev's existing build.
7. **Construction fleet ≠ UI build fleet**. Separate orchestrators, separate tmux sessions, separate stat files. `/check-fleet` skill is multi-orchestrator-aware.
8. **Orchestrator daemon is Python (not Claude Code session)**. subprocess.run on `claude --print` per agent invocation. Sidesteps session limits entirely.
9. **Per-stage scripts as the no-daemon escape hatch**. Daemon is convenience; per-stage manual run is the floor.
10. **Peer review IS allowed** (orchestrator-driven, sample-based, not recursive). Earlier "no peer review" stance was over-correction.
11. **Package + global-install policy**. Code-writing agents must justify deps and never global-install without explicit approval. Codified in design-philosophy.md and reference/agents.md.
12. **Per-entity index tables planned** for post-Stage-4 cleanup (`entity-index/<slug>.index.json` per architecture.md's artifact pattern).
13. **Temporal edges defer to v2** with structured fields when needed. v1 uses bracket qualifiers. Don't over-engineer.

---

## What's next

Two parallel tracks:

**Track A — Pipeline construction (ongoing):**
- Stage 4 build: edge-candidate-generator script → prose-edge-classifier (already runnable) → reviewer → promote-prose-edges
- Pass 1 catch-up: ACOK + ASOS via mechanical-extractor (background-able, multi-session)
- Then Pass 1 quality, then Stage 4 contradictions (after Pass 1 done)
- Then Pass 3-6 (multi-session each)

**Track B — Chat UI (parallel, eventual):**
- Wiki prose + book chapter chunkers
- Embedding pipeline (model + vector store choices)
- Backend FastAPI service
- Chat component (TS + CSS)
- mattnoth-dev integration
- Auth + deployment

Neither track requires a continue prompt — `working/agent-pipeline-plan.md` and `working/chat-ui-architecture.md` have the next-action ladders documented.

The natural next session is whatever Matt picks: kick off Pass 1 ACOK in background tabs, or start building the orchestrator daemon, or focus on the chat UI side. All are unblocked.

---

## Late-session addition: Two-repo split for copyright separation

End-of-session question from Matt: "could do forked repos, one for copyright one private."

Proposed architecture: split the project into two repos along the copyright boundary:
- **`weirdwood-network`** (current, could become PUBLIC eventually): scripts, docs, schema, graph nodes, wiki cache, design docs, chat UI component code. All wiki-derived or original.
- **`weirwood-corpus`** (NEW, permanently PRIVATE): `sources/raw/`, `sources/chapters/`, `extractions/mechanical/`, future `working/book-chunks/`. All book-derived.

Why this is cleaner than the current single-repo + .gitignore pattern:
- `.gitignore` today is doing copyright-protection duty. Brittle — one `git add -f` could leak.
- Two-repo split makes protection STRUCTURAL: copyrighted content physically lives elsewhere.
- Frontend deploy (Netlify) imports `weirdwood-network` (zero copyright risk).
- Backend deploy bundles both repos at build time OR mounts the corpus separately at runtime.
- `weirdwood-network` could go PUBLIC if Matt wants to open-source the methodology.

Mechanics for the split (when ready):
- Create `weirwood-corpus`, init from current gitignored content (which is on Matt's local disk but not in either repo's history).
- For local dev: clone both as siblings; scripts reference via relative paths.
- For backend deploy: include corpus as private submodule of a deploy-only repo, OR build container locally and push to private registry.

Decision recorded as TODO in `working/todos.md` for execution before chat-UI deployment phase. Not blocking until then.
