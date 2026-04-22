# The Harness — Architecture Evolution Notes: 2026-04-13

**Source:** Conversation between Matt and Claude exploring whether the Harness pattern is limited compared to knowledge graph architectures, how trust/provenance applies, how hot/warm/cold memory scales, and where multi-agent orchestration fits.

---

## The Core Question

Is the Harness — markdown files, trigger tables, hot/cold memory, trust ranking — just a simpler, less powerful version of a knowledge graph? Does the Weirwood Network's need for graph traversal and a potential graph DB mean the Harness's approach is fundamentally limited?

**Answer: No. They solve different problems.**

---

## Harness vs. Knowledge Graph — Different Tools for Different Access Patterns

### The Harness (Allvue context)

**Problem it solves:** "What context does the agent need right now to do this task?"

This is a **routing and assembly** problem. The agent is working on a mapper bug → load the mapper doc, the YAML config reference, the relevant pipeline architecture section. The trigger table routes, hot/cold memory prioritizes. Markdown files are the perfect storage format because the consumer is an LLM reading text.

**Access pattern:** Deep but narrow. You're always working on one mapper, one entity, one bug. The context is scoped to a single topic. One hop from the trigger table to the relevant documents.

**Why markdown works:** The agent doesn't need to traverse relationships across 500 entities. It needs the right 3-4 documents loaded. Markdown is portable, version-controlled, readable by Claude Code natively, and the LLM consumes text — not query results.

### The Knowledge Graph (Weirwood Network context)

**Problem it solves:** "How do these entities connect to each other across a web of relationships?"

This is a **traversal** problem. The query isn't "give me the right document" — it's "follow edges across nodes and tell me what you find." "Which characters have been to both Oldtown and the Wall?" requires checking every character node for location edges to both places and returning the intersection.

**Access pattern:** Wide and interconnected. The whole point is cross-entity connections — the value is in multi-hop reasoning.

**Why markdown hits its ceiling:** With 18k nodes and hundreds of edges each, a query like "trace the path from Littlefinger's dagger lie to the War of the Five Kings" means manually chaining file lookups. A graph DB does that traversal in milliseconds.

### The Key Distinction

The Harness is a **table of contents.** It tells you where to look.

A knowledge graph is a **web.** It tells you how things connect.

You don't use a web when you need a table of contents. You don't use a table of contents when you need a web. They're complementary, not competing.

### Where They Converge

The Harness could evolve to include a graph layer underneath for use cases that need traversal. The routing stays the same — trigger table, hot/warm/cold memory. You'd add a traversal capability for the queries that require it. The Harness doesn't become the graph — it sits on top of one.

---

## Hot / Warm / Cold Memory — Scaled for Large Graphs

At Allvue, hot/cold memory is binary: always loaded vs. loaded on demand. With the ASOIAF corpus (18k+ nodes, hundreds of thousands of edges), a third tier is needed because the graph is too big to ever load entirely. Hot/cold isn't just about relevance anymore — it's about **size management**.

### Hot Memory (always loaded)
- The trigger table itself (routing infrastructure)
- Hub ranking from the adjacency list (top 50-100 most connected nodes)
- Entity type index (what types exist, how many of each)
- Alias table (name → canonical entity mapping)
- Template/navbox index (what collections exist)

**Footprint:** Small. Navigational infrastructure. Answers "where do I start?"

### Warm Memory (loaded per query context)
- The target node plus its immediate (first-degree) edges
- For a character query: family edges, location edges, event participation, key perception edges
- For a location query: who's there, what events happened, what strategic significance
- Edge subset filtered by type and relevance to the query

**Footprint:** Moderate. One hop out from the query target. Even heavily-connected hub nodes (Tyrion with 500+ edges) are manageable if you filter by edge type.

**Key design question:** Does the agent pre-load edge summaries, or traverse on demand? For now, pre-load the first-degree connections. If traversal queries become common, that's when the graph DB earns its keep.

### Cold Memory (loaded on demand)
- Second-degree connections (two hops out)
- Full chapter extractions (raw text)
- Theory evidence chains
- Foreshadowing mappings
- Voice profiles

**Footprint:** Large. Only pulled when the query requires deep traversal or detailed evidence.

### How This Applies Back to Allvue

The three-tier model could improve the Harness at Allvue too:

- **Hot:** Architecture overview, pipeline topology, active JIRA context, coding conventions
- **Warm:** The specific entity/mapper/service being worked on, plus its immediate dependencies
- **Cold:** Historical investigation notes, related bugs, full SQL/YAML reference for adjacent entities

The current Allvue Harness already does something like this implicitly (the trigger table routes to specific docs, which is effectively warm memory loading). Making it explicit with three tiers would formalize what's already happening.

---

## Trust & Provenance — How It Applies to the Harness

### What the industry does

Knowledge graphs handle trust through:

1. **Provenance tracking** — every fact carries metadata about its source (W3C PROV-O standard)
2. **Confidence scoring** — facts get numerical confidence, sources earn/lose trust based on accuracy
3. **Reification** — storing "statements about statements" so you can say "Source A claims X with confidence 0.8" rather than just "X is true"
4. **Freshness decay** — reliability degrades over time (KOS Protocol, April 2026)
5. **Calibration** — ensuring AI confidence matches actual accuracy (Ca2KG framework, January 2026)

### What the Harness already does

The Harness's trust ranking on context documents is a simple version of provenance + confidence:
- Documents are ranked by trust level (canonical architecture docs > investigation notes > speculative ideas)
- The trigger table routes to the most relevant documents, implicitly prioritizing higher-trust sources
- The domain taxonomy controls scope — the agent only sees context relevant to the current topic

### What the Harness could add

**For Allvue (compliance/financial):**
- **Freshness decay** matters. A compliance rule set from six months ago might be outdated. Data about an issuer's credit rating has a shelf life. The Harness could timestamp context documents and flag staleness.
- **Dynamic confidence** matters. If a data source consistently produces accurate results, increase its trust weight. If a source's data leads to reconciliation errors, decrease it.
- **Conflict surfacing** matters. When two sources disagree about an entity's value, the Harness should present both with provenance rather than silently picking one.

**For ASOIAF (static corpus):**
- **Static provenance** is sufficient. The books don't change. Tag every fact with source, chapter, narrator, tier at extraction time and leave it.
- **Reification** for contested claims. Cersei's beliefs, Mushroom's testimony, Yandel's biases — store these as claims with metadata, not flat facts.
- **Confidence is source-dependent.** Tier 1 text > Tier 2 wiki synthesis > Tier 3 community interpretation. This doesn't need to be dynamic.

---

## Multi-Agent Orchestration — The Execution Layer

### The relationship between the Harness and multi-agent orchestration

The Harness is the **context management layer** — it tells each agent what to know.

Multi-agent orchestration is the **execution layer** — it tells agents how to collaborate.

They're complementary. Multi-agent orchestration is how you operationalize the Harness at scale. When a single agent can't hold everything it needs in one context window, you decompose into specialist agents, each with its own Harness-managed context (its own hot/warm/cold memory profile), and an orchestrator that assembles their outputs.

### Application 1: Building a Knowledge Graph (Weirwood Network)

**Parallelization by pass:**
- Pass 1 (Mechanical Extraction): parallel by chapter — each chapter is independent. 10 agents, 10 chapters simultaneously.
- Wiki parsing: parallel by page type — entity pages, year pages, community pages assigned to different worker pools.
- Pass 3 (Voice/Perception): parallel by character — one agent per POV character, each processing all that character's chapters.

**Orchestrator responsibilities:**
- Dependency graph management — which passes depend on which prior passes
- Work partitioning — how to split work within each pass (by chapter? by character? by page type?)
- Schema validation — ensure all worker outputs conform to the expected structure
- Failure handling — retry failed extractions, flag inconsistencies

This is the same problem as a build system (Make/Gradle) with LLM agents as workers.

### Application 2: Querying a Knowledge Graph (Chat Experience)

**Query decomposition into specialist agents:**

| Agent | Role | Hot Memory |
|-------|------|------------|
| Router | Reads query, dispatches to specialists | Trigger table, entity type index |
| Graph Traversal | Finds nodes, follows edges, identifies clusters | Adjacency list, hub ranking |
| Citation | Pulls specific chapter passages as evidence | Chapter index, reference mappings |
| Theory | Checks theory connections to queried nodes | Theory index, evidence chains |
| Synthesis | Composes final answer from specialist outputs | None — input is other agents' outputs |

Each specialist has a focused context window. The router doesn't need theory content. The citation agent doesn't need the full graph topology. No single agent carries everything — each carries only what the Harness says it needs.

### Application 3: Allvue Compliance (Trade Approval)

**Trade comes in → orchestrator spawns specialists:**

| Agent | Role | Context Loaded |
|-------|------|----------------|
| Rules | Checks trade against fund compliance rules | Fund rule set, current portfolio state, restricted lists |
| Context | Pulls relevant background on entities involved | Issuer news, counterparty history, related pending trades |
| Risk | Assesses portfolio-level impact | Portfolio analytics, sector/duration/credit distribution |
| Synthesis | Assembles approval package | All three specialist outputs |

**Output to human:** "This trade passes all automated checks. Risk impact: sector concentration increases from 22% to 24%. Two notes: (1) this issuer was downgraded last week, (2) there's a related trade pending for the same fund."

Human says "approve" or "hold."

### The Common Thread

All three applications solve the same problem: **no single agent can hold everything it needs.** You decompose by specialty, give each agent only its relevant context (via the Harness), and have an orchestrator that knows how to assemble results. The scale is different — 10 parallel chapter extractors vs. 4 specialist query agents vs. 3 compliance checkers — but the pattern is identical.

---

## What This Means for the Harness Brief

The brief for Dan shouldn't position the Harness as a markdown file system. It should position it as an **AI context management architecture** with three components:

1. **Routing layer** (trigger table / taxonomy) — routes queries to the right domain context
2. **Memory management** (hot/warm/cold) — controls what each agent sees and when
3. **Execution layer** (multi-agent orchestration) — decomposes complex tasks across specialist agents

The markdown files, the trust ranking, the domain scoping — those are implementation details of component 1 and 2. They work great for the single-agent, single-topic Allvue use case. But the architecture *pattern* scales to multi-agent, multi-domain, graph-backed systems.

The Weirwood Network is a proof-of-concept for the scaled version. The Allvue compliance use case is the enterprise application. The Harness is the common architecture underneath both.

---

## Portfolio Framing

The Weirwood Network isn't "I built a fun ASOIAF project." It's:

"I built a knowledge graph with typed entity relationships, multi-hop traversal, trust-tiered sourcing, provenance tracking, and a context routing layer — and here's how the same architecture applies to financial data lineage, compliance automation, and natural language analytics."

The ASOIAF domain is the proof environment — complex enough to stress-test the architecture, familiar enough to validate results, publicly discussable in interviews. The Allvue application is the enterprise value proposition. The Harness is the connective tissue.

---

## Open Design Questions

### How does the Harness routing layer interact with a graph DB?
If the knowledge graph lives in Neo4j, the trigger table still routes queries to the right domain. But instead of pointing to markdown files, some routes might point to graph queries — "run this Cypher query and load the results as context." The trigger table becomes a dispatcher that can route to files OR to queries depending on the context type.

### Should the Harness be a library, a framework, or a protocol?
Currently it's a convention — markdown files with a known structure, a trigger table pattern, a set of agent instructions. To make it transferable across Vista portfolio companies, it would need to be more formalized. A specification that any team can implement, not just a set of files in Matt's repo.

### What's the minimum viable demo?
For the Harness at Allvue: a before/after comparison showing the same coding task with and without Harness-managed context. Measurably better output with the Harness.

For the Weirwood Network: a query like "what's converging on Oldtown" that demonstrates multi-hop traversal, citation, and theory integration — producing an answer no vanilla LLM could reliably generate.

For compliance: a mock trade approval workflow showing the multi-agent decomposition and the quality of the synthesized approval package.
