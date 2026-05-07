# Session 0 — Project Genesis

**Date:** approximately 2026-04-13 (or possibly earlier)

---

## What Triggered This Session

Matt wanted to build something that didn't exist: a structured, queryable knowledge graph for A Song of Ice and Fire that could answer questions like "What does Catelyn think of Jon Snow?" or "When does the reader first learn about Lyanna's blue roses?" — questions that require traversing relationships across chapters and books, with awareness of what a reader knows at any given point in the story.

The existing resources — wiki pages, fan databases, Reddit threads — are flat and unspoilered. Matt wanted a system where you could ask a question and get an answer scoped to exactly how far you've read.

## What Happened

This was the foundational design session. Matt and Claude worked through the entire system architecture from a blank slate, making a series of interlocking design decisions that would shape everything that followed.

### The Two-Layer Architecture

The first major design decision was splitting the system into two layers: a **trigger table** for routing and a **knowledge graph** for traversal.

The trigger table is the index layer — it maps search terms (character names, location names, aliases, nicknames) to entity nodes. Its job is answering "what are you asking about?" before the graph ever gets involved. This matters because ASOIAF is full of aliases and ambiguity: "the Imp" and "Tyrion Lannister" and "Hugor Hill" all need to route to the same node, but a reader in ASOS doesn't know about "Hugor Hill" yet.

The knowledge graph is the relationship layer — typed nodes connected by typed edges. Characters linked to locations by TRAVELS_TO edges, to other characters by KILLS or SPOUSE_OF or PERCEIVED_AS edges, to houses by MEMBER_OF edges. The graph answers "what do we know about this entity and how does it connect to everything else?"

The separation means queries hit the trigger table first (fast, flat lookup), then traverse the graph (rich, typed relationships). It also means the two layers can be built and maintained independently.

### Spoiler Gating as Architecture

The single most consequential decision was making spoiler gating architectural rather than cosmetic. Every node and every edge in the graph carries a `first_available` field — the earliest book/chapter where that piece of information is revealed to the reader.

This wasn't retrofitted. It was designed in from the first conversation. The reasoning: if you add spoiler gating later, you have to go back through every piece of data and tag it. If you require it from the start, every extraction pass and every data pipeline inherently produces spoiler-aware output.

A query scoped to "AGOT Chapter 40" filters out everything with a `first_available` after that point. The reader's knowledge boundary becomes a first-class query parameter.

### The PERCEIVED_AS Edge Type

One of the more novel design decisions was the `PERCEIVED_AS` edge type, which tracks how POV characters perceive other characters. In ASOIAF, perception IS the text — we only see other characters through POV lenses. Catelyn sees Tyrion as a scheming monster; Jaime sees him as his clever little brother. These aren't just opinions; they're the fabric of the narrative.

PERCEIVED_AS edges carry the POV character, the perceived character, the perception (free text), and the chapter where it occurs. Over time, you can trace how a POV character's perception of someone evolves — or query all perceptions of a single character across all POVs to see how differently they're viewed.

### The real_identity Mapping

AFFC and ADWD use descriptive chapter titles instead of character names — "The Prophet" (Aeron Greyjoy), "The Soiled Knight" (Arys Oakheart), "The Queensmaker" (Arianne Martell). These are literary choices by GRRM, not accidents, and the system needed to handle them.

The solution was a `real_identity` mapping in the chapter splitter: the file gets named with the descriptive title (preserving GRRM's intent), but metadata links it to the actual POV character. This means you can query by either — "show me all Arya chapters" includes "Cat of the Canals" and "Mercy," while "show me what AFFC calls its chapters" preserves the descriptive titles.

### The Six-Pass Extraction Pipeline

Rather than trying to extract everything in one pass, the pipeline was designed as six sequential passes, each building on prior results:

1. **Mechanical** — Pure text extraction: who appears, what happens, what's mentioned. No interpretation.
2. **Wiki Ingestion** — Scrape the AWOIAF wiki as a reference layer. Cross-reference with extraction outputs.
3. **Voice Analysis** — Character voice profiles, speech patterns, cross-POV perception mapping.
4. **Foreshadowing** — Map textual foreshadowing to known future events (using a curated event list).
5. **Theory-Informed** — Use known fan theories (R+L=J, Grand Northern Conspiracy) as extraction lenses.
6. **Discovery** — Open-ended pattern finding: what did the earlier passes miss?

The ordering is deliberate. Mechanical extraction is objective and repeatable — it builds the foundation. Each subsequent pass adds interpretation layers, with increasing subjectivity. The confidence tier system (Tier 1 through Tier 5, from verified canon to crackpot theory) maps onto this progression: early passes produce high-confidence data, later passes produce lower-confidence but potentially more interesting findings.

### The Confidence Tier System

Five tiers were defined to handle the full spectrum from explicit text to fan speculation:

1. **Verified Canon** — Explicitly stated in text
2. **Strong Inference** — Heavily implied, widely agreed
3. **Reasonable Inference** — Supported by evidence, debatable
4. **Speculative** — Plausible but thin evidence
5. **Crackpot** — Creative interpretation, minimal textual support

This system lets the graph contain R+L=J (Tier 2-3 depending on how you weigh the evidence) alongside "Tyrion is a secret Targaryen" (Tier 4-5) without treating them as equivalent claims. Queries can filter by confidence tier.

### Theories as Input AND Output

An insight that shaped the later-pass design: fan theories aren't just things the system produces — they're lenses for extraction. R+L=J isn't just a conclusion; it's a filter that makes you notice Ned's fever dream about the Tower of Joy, Lyanna's "promise me, Ned," and a dozen other textual signals. The theory-informed extraction pass (Pass 5) would use curated theories as input prompts, asking the extractor to specifically look for evidence that supports, contradicts, or complicates each theory.

This creates a feedback loop: early passes produce data, analysis of that data generates theories, theories become input lenses for later extraction passes.

## Key Decisions and Why

| Decision | Reasoning |
|----------|-----------|
| Two-layer architecture (trigger table + graph) | Separates the "what are you asking about?" problem from the "what do we know about it?" problem |
| `first_available` on all nodes/edges from day one | Spoiler gating is architectural; retrofitting it would require re-processing everything |
| PERCEIVED_AS as a first-class edge type | ASOIAF's POV structure means perception IS data, not commentary |
| `real_identity` mapping for descriptive chapter titles | Preserves GRRM's literary choices while maintaining queryability |
| Six sequential extraction passes | Each pass builds on prior results; interpretation increases gradually |
| Five confidence tiers | The graph needs to contain both canon facts and speculative theories without conflating them |
| Markdown-based, not a database | The entire system is readable files in a git repo — no infrastructure dependencies |

## What Was Left Open

- The exact schema for extraction output (what fields, what structure) was directional but not finalized — that would come when actually writing the mechanical extractor prompt
- Wiki scraping strategy was identified as necessary but not designed yet
- How to handle the Dunk and Egg novellas and The World of Ice and Fire (non-novel sources) was noted but deferred
- Fan fiction generation was mentioned as a potential downstream use case but explicitly shelved as out of scope for the build phase
- Whether the architecture could generalize beyond ASOIAF to other literary universes was noted as interesting but not pursued
