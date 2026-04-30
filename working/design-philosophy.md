# Design Philosophy — Weirwood Network

**Established:** Session 26 (2026-04-28), retroactively articulating principles that emerged from the Stage 3 redesign and the fleet planning effort.

**Purpose:** A reference for *why* the project's architecture looks the way it does. Architecture.md says *what* the schema is. This doc says *what design tradition* the schema is in and *which alternatives we rejected*.

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

**Important distinction — peer review IS allowed if the orchestrator drives it.** What's disallowed is `agent A invokes agent B to review A's output` (recursion). What's allowed and useful is `orchestrator invokes A; orchestrator invokes B reading A's text-stream output`. The reviewer agent is at the same level as the classifier — both leaf workers, both invoked by the orchestrator, composing via on-disk JSONL. See `working/fleet-orchestration-plan.md` § "Self-review pattern (clarification)" for how the prose-edge-reviewer / cross-identity-reviewer / fleet-stats-reviewer agents fit this pattern. The first version of this doc rejected peer review broadly; that was an over-correction. Sample-based, orchestrator-driven, separately-framed peer review is consistent with the philosophy.

**Composition through inheritance.** Building a "more capable" agent by extending a base agent. We compose through pipes — Python composers between agent stages — which keeps each agent simple and lets us replace any one of them without touching the others.

---

## The corollary: "Worse is better" (Richard Gabriel, 1991)

> "It is better to have a simple system that does 70% of what you want than a complex system that does 99%."

Ship the 70% solution in 100 lines rather than the 99% solution in 5,000. Then iterate on the parts that turned out to matter.

Examples in this project:
- **Stage 3b prose extractor** is ~770 lines of HTML-walking + a static header-mapping table. Could be smarter (NLP-based section detection, fuzzy matching against schema headings, learned classifiers). Doesn't need to be — the static table hits 90% of pages cleanly, and the misses are concentrated in known categories we map case-by-case.
- **Edge vocabulary lock.** 22 edge types, manually curated from infobox-field frequencies. Could automate ontology induction with embeddings or graph statistics. Doesn't need to be — manual curation gets us a coherent vocabulary in a weekend; automated induction would take months and produce a wider but less queryable vocabulary.
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

## Package selection and global-install policy

Every code-writing agent in the fleet (`script-builder`, `frontend-developer`, `backend-developer`, `deployment-engineer`, `embedding-refresh-runner`, etc.) must respect this policy. It exists because the cost of a malicious or unreliable dependency is high (supply-chain compromise, system pollution, hard-to-undo state changes), and the cost of asking before installing is low.

### Rules

**1. No global installs without explicit user approval.**
Never run any of: `npm install -g`, `yarn global add`, `pip install --user`, `pip install --break-system-packages`, `pipx install` outside a documented project tool, `brew install`, `gem install` system-wide, `cargo install` to system path, or any equivalent that modifies the host's global package state. If a global tool is genuinely needed, file a question to `working/wiki-pass2/questions-for-matt.jsonl` of type `package-global-install-request` with: tool name, why needed, the exact command proposed, what alternatives were considered. User approves explicitly before the command runs.

**2. Project-local installs only.**
- Python: always inside a virtual environment (`python3 -m venv venv`, then `source venv/bin/activate`). Pin in `requirements.txt` or `pyproject.toml`.
- Node: project-local `node_modules`, pinned in `package.json` + `package-lock.json` / `pnpm-lock.yaml` / `bun.lockb`. Never `-g`.
- Rust: project-local `Cargo.toml`. No system-wide cargo install.

**3. Reliable packages only.**
Before adding ANY dependency, the agent confirms ALL of:

- High download volume (npm: >100k weekly downloads; PyPI: comparable established tier)
- Recent maintenance (last commit within ~12 months)
- Recognizable maintainer (named individual, established org, foundation — not "random GitHub account with 0 followers")
- Package name matches its homepage / repo (no typosquat suspicion — `requests` not `requestz`, `numpy` not `nump`, etc.)
- For each package category, prefer the canonical recommended choice rather than a flashy newcomer:
  - **LLM SDK:** `anthropic` (official) — and ONLY `anthropic` for Claude calls
  - **Vector DB:** `chromadb`, `lancedb`, or `sqlite-vec` (these have been vetted by the Anthropic ecosystem)
  - **Embedding:** Voyage AI's official SDK, OpenAI's official SDK, or local `sentence-transformers`/`nomic-embed`
  - **HTTP / API:** `requests` (Python), `httpx` (Python async), `fetch` (Node native — no axios/got/etc. unless specifically justified)
  - **Markdown rendering:** `marked` (Node) or `markdown-it`, `python-markdown` or `mistune` (Python). Mature and audited.
  - **CSS scoping:** scoped class names or CSS Modules. No new CSS-in-JS framework unless `mattnoth-dev` is already using one.

**4. Always state the package + alternatives.**
When proposing a new dependency, the agent's commit message / PR description / output report includes:
- Package name + version + source (npm / PyPI / GitHub releases)
- Homepage URL
- Why this package over the alternatives it considered (one-line each)
- Whether this is a hard requirement or "nice-to-have"

User can override with a different package without penalty.

**5. Settings updates require user-visible diffs.**
When an agent proposes changes to `.claude/settings.json` or `.claude/settings.local.json` (using the `update-config` skill or otherwise):
- Show the proposed diff to the user first
- Don't add `*` permission grants (too broad)
- Don't disable security-sensitive defaults
- Hooks that auto-execute commands need EXTRA scrutiny — describe what the hook does, when it fires, what it can read/write
- Default to least-privilege; ask before broadening

**6. Codify the policy in `.claude/settings.json` deny-rules.**
The project's settings file should explicitly deny global-install bash commands at the harness level. Belt-and-suspenders alongside the prompt-level rule. Suggested deny patterns:
- `npm install -g *`
- `yarn global *`
- `pip install --user *`
- `pip install --break-system-packages *`
- `brew install *`
- `gem install *`
- `cargo install *`

When these are denied by the harness, an agent attempting them gets a permission prompt — Matt approves manually if the install is genuinely needed.

### Why this policy

- **Supply-chain attacks are real.** Typosquats, dependency confusion, and post-install scripts have shipped malware in npm, PyPI, and other registries. An agent moving fast on "build me a chat UI" is exactly the wrong context for casual `npm install random-chat-package`.
- **Global installs are hard to undo.** Project-local installs delete with the project directory. Global installs leave artifacts that survive. If something turns out to be malicious, project-local containment limits the blast radius.
- **Settings drift compounds.** A permissive settings.json over time accumulates broad permissions that the user can't easily audit. Diff-before-apply keeps the project's threat model legible.

### When this policy bites (and that's the point)

If an agent proposes installing `chromadb` (recognized, reliable) the policy passes silently — nothing to ask Matt about, install proceeds in the venv. If an agent proposes installing `chrome-vector-db-fast` (looks like chromadb but isn't) the policy catches it: agent has to justify, alternatives considered, Matt approves explicitly. The friction is the feature.

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
- `working/agent-pipeline-plan.md` — the fleet (which agents apply this philosophy)
- `working/runbooks/wiki-pass2-pipeline.md` — Stage 3 canonical pipeline (concrete example of the philosophy)
- `working/scratch-design-review-stage3b.md` — the Session 26 design review where this philosophy was first articulated explicitly (in the form of the Stage 3b agent → Python redesign)
