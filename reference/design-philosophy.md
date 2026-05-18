# Design Philosophy — Weirwood Network

**Established:** Session 26 (2026-04-28), retroactively articulating principles that emerged from the Stage 3 redesign and the fleet planning effort.

**Purpose:** A reference for *why* the project's architecture looks the way it does. `architecture.md` says *what* the schema is. This doc says *what design tradition* the schema is in and *which alternatives we rejected*.

For the operational rules code-writing agents must follow when adding dependencies or changing settings, see `reference/package-install-policy.md` (split out of this doc on 2026-05-07 because it's load-bearing operational policy, not just framing).

---

## Core principle: The Unix Philosophy

Doug McIlroy, 1978:
> "Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."

How this maps to the Weirwood Network:

### 1. "One thing well."

Each pipeline component (script or agent) has a single, focused responsibility. It doesn't try to be flexible enough to do related-but-different jobs.

- `wiki-pass2-emit-deterministic.py` emits skeletons. It doesn't ALSO extract prose.
- `wiki-pass2-extract-prose.py` extracts prose. It doesn't ALSO emit skeletons or promote.
- `prose-edge-classifier` (Stage 4 agent) classifies candidate edges. It doesn't ALSO detect cross-identity (`cross-identity-detector`'s job) or surface contradictions (`contradiction-surfacer`'s job).
- The original Stage-1 `wiki-ingester` was a mega-agent doing 5 things at once: parse infobox → emit frontmatter → write Identity prose → write Narrative Arc prose → emit Edges. It had agent-paraphrase failures that took a full session to diagnose. The Stage 3 redesign split it into 4 focused tools (Python emitters + Python promoter), each replaceable independently.

### 2. "Work together."

Each component emits structured output (JSONL or markdown) that becomes input to another component — usually a Python composer that the orchestrator coordinates.

- `wiki-pass2-emit-deterministic.py` writes `skeleton/<slug>.node.md`
- `wiki-pass2-extract-prose.py` writes `prose/<slug>.prose.md`
- `wiki-pass2-promote.py` reads both, concats, writes `graph/nodes/<type>/<slug>.node.md`
- `wiki-pass2-build-cross-refs.py` reads the promoted nodes, writes `cross-references.jsonl`
- (Future) `prose-edge-classifier` reads `cross-references.jsonl` + node prose, writes `prose-edges/<slug>.edges.jsonl`
- (Future) `wiki-pass2-promote-prose-edges.py` reads that JSONL, appends to nodes

No tight coupling. No agent invokes another agent. No script reaches into another script's internal state. Every connection is via on-disk artifacts with documented schemas.

### 3. "Text streams as universal interface."

Everything is markdown or JSONL. Both are line-oriented plain text — you can `grep`, `jq`, `cat`, `wc`, `head`, `tail`, `awk`, `diff` any artifact in the pipeline without writing a parser. **No proprietary formats. No binary blobs. No agent-internal state leaking between stages.**

The single-writer-per-file invariant we established Session 26 is exactly the Unix file-as-pipe pattern: one writer per file, anyone can read. If you can `cat` it, you can debug it.

---

## What is "text streaming"?

**Text streaming = data flow via plain-text files (or stdin/stdout pipes), where each consumer can read the producer's output without a schema, library, or binding.**

Concretely in this project:
- **Markdown** is text-streamed (human readable, line-oriented, structured by `##` headings and `- ` bullets, grep-able).
- **JSONL** is text-streamed (one JSON object per line, `jq`-able, line-oriented; you don't need to load the whole file to process it).
- **Concatenation IS the pipe.** `wiki-pass2-promote.py` produces final nodes by literally `cat skeleton + "\n" + prose`. That's text streaming as composition.

The opposite of text streaming:
- **Database wire protocols** — require a client library
- **Java RMI / SOAP / gRPC / Protobuf** — require generated bindings on both sides; schema versioning becomes a thing
- **Memory-mapped binary state** — requires shared address space and tight version coupling
- **Pickle / Serialized objects** — language-specific; can't be inspected without the producing language's runtime

The Unix insight is that **text is the universal interface** because every language, every shell, every editor, every human can read it. There's no SDK to write a JSONL reader: `for line in file: json.loads(line)` works in any language. There's no SDK to read markdown: it's just text with conventions. The cost of going through plain text (parsing overhead, schema-by-convention rather than schema-enforced) is dwarfed by the freedom-to-debug-everything-with-grep that you get back.

This is why the fleet plan rejects "agent-internal state leaking between stages" — if Agent A's internal reasoning state has to be passed to Agent B, that's hidden coupling, not text streaming. Make A write its reasoning to a JSONL file, B read that file. Now any third tool — including `cat`, including a future agent we haven't designed yet, including a script for debugging — can also read it.

---

## Anti-patterns we explicitly reject

**Featuritis.** Adding "just one more thing" to an existing component rather than building a new focused one. The wiki-ingester agent was a featuritis casualty — every time something was missing it got another instruction stuffed into the prompt. Eventually nobody could keep its constraints straight, and it failed in subtle ways. Fix: split.

**Hidden coupling.** A component depending on another component's internal state, side effects, or undocumented behavior. Two agents both writing to the same file is hidden coupling — the second agent's output depends on what the first agent left there. We forbid this via the single-writer-per-file invariant.

**Recursive complexity.** Subagents calling subagents. Allowed in Claude Code's mechanics; disallowed in our fleet because (a) context-isolation breaks debugging — failures bury inside nested levels, (b) token cost compounds — every level pays the project-context tax anew, (c) progress reporting fails — the orchestrator can't see what's happening 2 levels down. Composition belongs to the orchestrator (Unix shell), not to the leaf workers (Unix programs).

**Important distinction — peer review IS allowed if the orchestrator drives it.** What's disallowed is `agent A invokes agent B to review A's output` (recursion). What's allowed and useful is `orchestrator invokes A; orchestrator invokes B reading A's text-stream output`. The reviewer agent is at the same level as the classifier — both leaf workers, both invoked by the orchestrator, composing via on-disk JSONL. See `working/agent-fleet-specs/fleet-orchestration-plan.md` § "Self-review pattern (clarification)" for how the prose-edge-reviewer / cross-identity-reviewer / fleet-stats-reviewer agents fit this pattern. The first version of this doc rejected peer review broadly; that was an over-correction. Sample-based, orchestrator-driven, separately-framed peer review is consistent with the philosophy.

**Composition through inheritance.** Building a "more capable" agent by extending a base agent. We compose through pipes — Python composers between agent stages — which keeps each agent simple and lets us replace any one of them without touching the others.

---

## The corollary: "Worse is better" (Richard Gabriel, 1991)

> "It is better to have a simple system that does 70% of what you want than a complex system that does 99%."

Ship the 70% solution in 100 lines rather than the 99% solution in 5,000. Then iterate on the parts that turned out to matter.

Examples in this project:
- **Stage 3b prose extractor** is ~770 lines of HTML-walking + a static header-mapping table. Could be smarter (NLP-based section detection, fuzzy matching against schema headings, learned classifiers). Doesn't need to be — the static table hits 90% of pages cleanly, and the misses are concentrated in known categories we map case-by-case.
- **Edge vocabulary lock.** ~96 edge types, manually curated — ~26 derived from wiki infobox-field frequencies, the rest pre-declared for narrative/perception/prophecy passes. Could automate ontology induction with embeddings or graph statistics. Doesn't need to be — manual curation gets us a coherent vocabulary in a weekend; automated induction would take months and produce a wider but less queryable vocabulary.
- **Bucket fingerprints** (cold review's C1 finding — track_b_row hashes missing from fingerprint). The fingerprint catches 95% of "needs re-queue" cases. The wiki-re-crawl-touches-only-infobox case is rare and was deferred. Worse-is-better in action.
- **Agent prompts** — short, focused, no kitchen-sink instructions. A 100-line agent prompt that does one job well beats a 500-line "comprehensive" prompt that does five jobs poorly.

The discipline to apply "worse is better" requires admitting what you don't know yet. We don't know which prose-derived edges are most valuable until Stage 4 runs once. We don't know which cross-identity cases are high-value until cross-references-resolution runs once. So we ship 70% solutions, observe what fails, fix the failures we actually see — not the failures we imagine.

---

## The contrast worth naming

The alternative to the Unix philosophy is the "Lisp Machine" / "Smalltalk" / "Emacs" philosophy: one big intelligent system that does everything within a unified worldview. Powerful when the system is a runtime you live inside (text editor, IDE, mathematical workspace). Poor fit for **batch data pipelines** because:

1. **Debugging failure modes of a giant agent is intractable.** When a 5,000-token mega-prompt fails, you can't pinpoint which constraint it violated. When a 200-token focused prompt fails, the failure maps 1:1 to a single decision.
2. **Composition through extension doesn't compose.** Adding new capabilities to a giant system requires understanding the whole system. Adding a new focused agent requires understanding only the input/output contract.
3. **The unified worldview is a liability for evolution.** When schema changes — and it does, every cold review surfaces something — a unified system has to be updated coherently across all its parts. A pipeline of focused tools changes one tool at a time.

Stage 1's wiki-ingester was a mini Lisp Machine: hold the whole bundle, think about everything, write everything. It produced 855 nodes and was retired because the failure modes (silent paraphrase, edge invention, frontmatter drift) were too tangled to debug at scale. Stage 3's pipeline of small tools produced 3,314 nodes in 30 seconds with zero similar failures, because each tool had one job and emitted plain text we could inspect.

---

## Where this philosophy applies (and where it doesn't)

**Applies to:**
- Pipeline components (scripts and agents)
- Artifact formats (markdown / JSONL only)
- Inter-stage contracts (file paths, schema columns)
- Agent prompt design (single reasoning task per prompt)
- The orchestrator's role (coordinate; don't reach into workers)

**Does NOT apply to:**
- Reference materials (`reference/architecture.md`, `reference/foreshadowing-events.md`) — these are knowledge artifacts. They're meant to be unified worldviews, not pipeline tools.
- The graph itself — `graph/nodes/` is the unified data structure all the pipelines feed. It's the *output*, not a stage.
- The orchestrator session (this Claude Code chat) — by design, the orchestrator IS the integrator. It's allowed to hold context across many tools.

---

## Files this philosophy ties into

- `reference/architecture.md` — the schema (what)
- `reference/package-install-policy.md` — operational rules for code-writing agents (split out of this doc 2026-05-07)
- `working/agent-fleet-specs/agent-pipeline-plan.md` — the fleet (which agents apply this philosophy)
- `working/runbooks/wiki-pass2-pipeline.md` — Stage 3 canonical pipeline (concrete example of the philosophy)
- `working/scratch-design-review-stage3b.md` — the Session 26 design review where this philosophy was first articulated explicitly (in the form of the Stage 3b agent → Python redesign)
