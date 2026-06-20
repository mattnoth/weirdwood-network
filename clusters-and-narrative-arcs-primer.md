# Clusters, Reification, and Narrative Arcs — A Primer
**For:** Matt's own learning, not a project deliverable.
**Date:** 2026-06-13
**Why this file exists:** The conversation surfaced terms ("cluster," "reification," "narrative arc") that show up across graph theory, knowledge graphs, and computational narratology. This doc unpacks each one, says what we actually did vs the formal version, and points at reading.

---

## 1. The terms in one table

| Term | Field where it lives | What it means | Did we use it? |
|---|---|---|---|
| **Cluster / community** | Graph theory | A densely-connected subgroup *discovered* in an existing graph by an algorithm | No — we don't run community-detection |
| **Reification** | Knowledge graphs / philosophy of language | Turning a verb/event/relationship into a node so you can attach properties to it | **YES** — every event hub in our `graph/nodes/events/` is reified |
| **N-ary relation** | Knowledge graphs | A relationship that connects more than 2 entities ("X killed Y at Z under W's orders") | Yes, modeled as reified event hubs + role edges (AGENT_IN, VICTIM_IN, etc.) |
| **Hypergraph** | Graph theory | A graph where edges can connect any number of nodes at once | No — we deliberately model n-ary via reification instead |
| **Frame / frameset** | Computational linguistics (FrameNet) | A structured representation of a situation (e.g., "Killing" frame: KILLER, VICTIM, INSTRUMENT, PLACE) | Conceptually similar to our reified event hubs |
| **Plot unit** | Computational narratology (Lehnert) | A small recurring affective pattern in stories (e.g., "promised reward," "betrayal") | No — but the project's foreshadowing/theory passes are headed this direction |
| **Script** | AI / Schank | A stereotyped sequence of events (e.g., "wedding script": invite → ceremony → feast → bedding) | We model individual weddings; we don't have a generic "wedding script" abstraction |
| **Narrative arc / causal chain** | Literary digital humanities | A reader-recognized chain of cause-and-consequence spanning multiple events | **YES — new track surfaced 2026-06-13** (`incident-at-the-trident` is the first one) |

---

## 2. Clusters in graph theory (what they *actually* are)

In formal graph theory, **clustering** is an *algorithmic discovery* task, not a modeling choice. You have a graph; you run an algorithm that finds densely-connected subgroups; those subgroups are called clusters or **communities**.

Canonical algorithms:
- **Louvain method** (2008) — greedy modularity optimization; ~O(n log n)
- **Girvan-Newman** (2002) — iteratively removes high-betweenness edges
- **Label propagation** — fast, near-linear
- **Spectral clustering** — uses eigenvectors of the graph Laplacian

What they'd do on OUR graph: identify house-clusters (`house-stark` + its 50-odd PARENT_OF/SPOUSE_OF/SWORN_TO neighbors), region-clusters (`the-north` + its locations), event-clusters (Red Wedding's 8 SUB_BEAT_OF children). The clusters would be *emergent* from the existing structure — we don't mint a "cluster node."

**Why we don't use this:** community detection is useful for graphs where structure is unknown and you're hunting for it. Our structure is known (we built it). Running Louvain on our graph would mostly rediscover the houses and regions we already named.

**Where it MIGHT become useful:** as a validation tool. After the narrative-arc track produces ~20 arc-parent hubs, running community detection on the result would tell us whether the arcs we curated match the dense subgroups the graph reveals on its own. Mismatch = signal that we missed an arc or over-grouped beats.

**Reading:** Newman, *Networks: An Introduction* (2nd ed., 2018) — chapters 11-14. The standard textbook.

---

## 3. Reification (this IS what we do)

**Reification** = turning an abstract thing (an event, a statement, a relationship) into a concrete node so you can attach properties, qualifiers, and other relationships to it.

Without reification, our graph would have only direct edges:
- `sandor-clegane KILLS mycah`

That edge can carry a few properties (Tier 1, evidence_quote, etc.) but you can't easily attach: "this killing happened on the kingsroad / was ordered by Cersei / had Joffrey as the trigger / Sansa-Arya rift was a downstream effect."

With reification, the killing becomes a node `death-of-mycah`, and you can spray edges off it:
- `sandor-clegane AGENT_IN death-of-mycah`
- `mycah VICTIM_IN death-of-mycah`
- `kingsroad LOCATED_AT death-of-mycah`
- `cersei-maneuvers TRIGGERS death-of-mycah`
- `incident-at-the-trident` contains it via SUB_BEAT_OF

Now the event is a first-class graph object that can be queried, contextualized, and grouped.

**Other knowledge graphs that reify:**
- **Wikidata** uses "statements" with qualifiers — essentially reified property-assertions
- **schema.org** Action types (e.g., `MarryAction`) reify events
- **CIDOC-CRM** (museum metadata) reifies everything as `E5_Event`
- **RDF reification** is the W3C-blessed pattern for turning triples into quads

**Cost:** node count explodes. Our graph went from ~8,500 nodes pre-reification to 8,518 (events alone: 371 → 585 across S87/S93/S95). For a fully-reified graph the events directory might hit 1,500-2,000.

**Benefit:** the queries you want to run become 1-2 hop traversals instead of LLM reasoning.

**Reading:** Hogan et al., *Knowledge Graphs* (2021, free PDF) — chapter 3.4 covers reification patterns in depth. This is the modern canonical reference.

---

## 4. Hypergraphs (the road we didn't take)

A **hypergraph** generalizes graphs by letting a single edge connect any number of nodes. In ASOIAF terms: the Red Wedding could be a single hyperedge connecting Walder Frey, Roose Bolton, Robb Stark, Catelyn Stark, Talisa Stark, Grey Wind, the Twins, and every Frey present — all at once, no reification needed.

We chose reification (event hubs + binary edges) instead. Why:
1. Hypergraphs lose direction. We need to say "Walder Frey AGENT vs Robb VICTIM," not just "they were all in this event together."
2. Tooling. Almost every graph database, query language (SPARQL, Cypher), and visualization assumes binary edges. Hypergraphs are research-grade; reified binary edges are production-grade.
3. Reification gives us a *named hub* (the event slug `red-wedding`) that itself becomes queryable, citable, and rememberable. A hyperedge has no identity of its own.

**When hypergraphs win:** dense multi-party relations where role distinctions don't matter (e.g., social co-authorship networks where "these 5 people wrote this paper together" is the only fact).

**Reading:** Battiston et al., "The physics of higher-order interactions in complex systems" (Nature Physics, 2021) — survey paper on hypergraphs and simplicial complexes in network science.

---

## 5. Frames (computational linguistics' version)

**FrameNet** (Berkeley, ongoing since 1997) defines ~1,200 *frames* — structured representations of situations. The Killing frame has slots: KILLER, VICTIM, INSTRUMENT, CAUSE, PLACE, TIME, MANNER. Filling those slots from a sentence ("Sandor cut Mycah down on the kingsroad with his greatsword") produces a structured representation.

Our reified event hubs are essentially frame instances:
- `death-of-mycah` is an instance of the *Killing* frame
- Role edges (AGENT_IN, VICTIM_IN, LOCATED_AT) fill its slots
- Each event hub TYPE in our schema (`event.death`, `event.battle`, `event.ceremony`, `event.deception`) corresponds roughly to a frame

**Where this matters for us:** FrameNet's frame inventory is a *vocabulary check.* If FrameNet has 1,200 frames and we have ~20 event types, we're either under-modeling or our domain (ASOIAF) genuinely needs fewer.

**Reading:** Fillmore & Baker, "A Frames Approach to Semantic Analysis" (2010) — short, readable intro. Or just browse framenet.icsi.berkeley.edu (if you ever go online).

---

## 6. Computational narratology — where narrative arcs live

This is the field that names what we're now starting to do.

**Plot units (Lehnert, 1981)** — small affective patterns of mental states (problems, positive/negative events). E.g., "promised reward" = P+ that leads to M+ (mental positive). "Betrayal" = expected M+ that flips to M-. Story arcs are sequences of plot units.

**Scripts (Schank & Abelson, 1977)** — stereotyped event sequences ("restaurant script": enter, sit, order, eat, pay, leave). A wedding has a script; a battle has a script. Our individual reified weddings are *instances* of an unrepresented wedding script.

**Story grammars (Mandler & Johnson, 1977)** — recursive grammars that generate well-formed stories. Setting + Episode+ where Episode = Beginning + Development + Ending.

**Modern narrative-event-extraction** — ACE-2005, ECB+, NewsReader, Story Cloze. These are the corpora and tasks where research-grade systems try to do what we're doing manually with curation.

**What we're doing that's actually novel:**
1. **Grounding.** Every edge cites a verbatim book quote. Most narrative-event datasets either drop grounding entirely or use sentence-level alignment. We use line-level.
2. **Identity-aware reification.** Our impersonation rule ([[project_impersonation_edges_redirect]]) + skinchanger-attribution rule (S95 Q1) handles in-universe identity manipulation in a way generic NLP can't.
3. **Hospitality and food as first-class** ([[user_asoiaf_design_values]]) — most narrative graphs throw this out as fluff; we treat it as load-bearing.

**Reading:**
- Mani, *Computational Modeling of Narrative* (2013) — short Morgan & Claypool monograph. The field's textbook.
- Riedl & Young, "Narrative Planning" (2010) — readable paper introducing the planning angle.

---

## 7. Narrative arc reification (where we just landed)

This is the term for the track we just opened. It's NOT a standard textbook term — it's an applied use of reification (Section 3) to causal chains (computational narratology, Section 6) that span multiple already-reified events.

**Pattern:**
- Parent event hub (event.incident, event.arc, or similar type)
- SUB_BEAT_OF children attach existing/new event hubs to the parent
- TRIGGERS / PRECEDES edges within the children encode causal direction
- Role edges live at the BEAT level, not at the parent (avoids duplication)

**First instance:** `incident-at-the-trident` (S95 Q5). Parent + 4 children (cersei-maneuvers-for-lady-s-death, ned-claims-the-execution, ned-kills-lady, death-of-mycah). The first three already existed as standalone hubs; they got retroactively linked.

**Open questions:**
1. Should arcs use a distinct type (`event.arc`) or just `event.incident`?
2. Should TRIGGERS density be high (every adjacent sub-beat) or low (only load-bearing causal junctures)?
3. Cross-arc edges — when does Sack-of-KL TRIGGER the Mountain's later Harrenhal acts? (gateway to cross-arc reification)
4. Are theories and arcs the same shape with different uses? (theories are about interpretation; arcs are about causation)

These will resolve as more arcs land. The Mode 3 dip is the priority signal.

---

## 8. Where to start reading (one-paragraph picks)

If you want ONE book on knowledge graphs: **Hogan et al., *Knowledge Graphs* (2021).** Free PDF. Comprehensive, modern, covers reification + querying + reasoning + applications. ~300 pages.

If you want ONE book on graph theory itself: **Newman, *Networks* (2nd ed., 2018).** Standard textbook. The community-detection chapters are the relevant ones for "clusters."

If you want ONE on computational narratology: **Mani, *Computational Modeling of Narrative* (2013).** ~150 pages. Synthesizes the field.

If you want ONE on linguistic frames: **Fillmore & Baker, "A Frames Approach to Semantic Analysis" (2010).** Free PDF. ~40 pages.

For graph databases practically: **O'Reilly's *Graph Databases* (Robinson, Webber, Eifrem, 2nd ed., 2015).** Free PDF from Neo4j. Practical.

---

## 9. The 10-second version

We don't use "clusters" in the algorithm-discovery sense. We use **reification** — turning events into nodes — at the per-event level (Plate 5, S87) and now we're starting to use it one level up at the **narrative-arc** level (S95). The pattern is the same; the scale is different. Other fields have called this "frame instances" (linguistics), "n-ary event reification" (knowledge graphs), or "causal chain modeling" (narratology). What's novel about our version is the grounding (verbatim book-quote citations on every edge), the identity-awareness (impersonation + skinchanger rules), and the elevation of hospitality/food as first-class graph objects.
