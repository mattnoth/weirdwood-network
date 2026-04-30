# Chat UI Architecture — Weirwood Network Retrieval Layer

**Created:** Session 26 (2026-04-28)
**Purpose:** How the eventual ASOIAF chat UI retrieves answers from the graph + wiki prose + book chapters. Same Unix-philosophy approach as the construction layer (`working/fleet-runtime-architecture.md`), but for queries instead of pipeline.

**Companion docs:**
- `working/fleet-runtime-architecture.md` — the construction-side architecture (how the graph gets built)
- `working/design-philosophy.md` — Unix philosophy applied to the project
- `reference/architecture.md` — schema (entity types, edges, artifact formats)

---

## Goals

1. **Deployable preview for D&D group.** Not personal-local. Shareable-from-day-1 to a small invited friend group via a hosted web UI behind minimal auth. Books-included retrieval is the value prop — the wiki alone isn't enough to be interesting.
2. **Cited answers.** Every fact the chat UI surfaces traces back to a wiki page, a chapter, or a derived extraction.
3. **Three-corpus retrieval.** Graph (structured), wiki prose (narrative summary), book chapters (canonical narrative). The chat reaches into all three and joins on slugs.
4. **Spoiler gate fully OPEN for v1.** No `first_available` filtering. Add later as an additive layer.
5. **Stage-by-stage shippable.** A degraded chat UI on graph-only (no prose) is shippable as a proof of concept; the friend-group preview must include book chunks to be interesting.
6. **No tight coupling between corpus and retrieval.** A new corpus (TWOIAF, F&B, etc.) gets ingested via the same chunking → mention-tagging → embedding pipeline; query layer doesn't change.

---

## Three corpora, one join

The slug is the universal join key. Every chunk and every node carries the slugs it relates to. Retrieval queries combine across corpora by slug intersection.

| Corpus | Source | What's in it | Per-chunk metadata |
|--------|--------|--------------|--------------------|
| **Graph nodes** | `graph/nodes/<type>/<slug>.node.md` | Structured facts: frontmatter (name, type, aliases, etc.) + `## Edges` (typed relationships) + `## Identity` (canonical short-form) + prose body sections | `slug`, `type`, `aliases`, `book_appearances` (from cite_refs) |
| **Wiki prose chunks** | derived from `working/wiki-pass2/<bucket>/prose/<slug>.prose.md` (or post-promotion `graph/nodes/<type>/<slug>.node.md` body sections) | Narrative summaries from the wiki: Origins, Allegiances, Appearances & Description, Narrative Arc, Quotes, Notes | `chunk_id`, `node_slug`, `section` (e.g., `## Narrative Arc`), `subsection` (e.g., `### A Storm of Swords`), `mentioned_slugs` (extracted from `[text](wiki:Page)` markdown links), `cite` |
| **Book chunks** | derived from `sources/chapters/<book>/<chapter>.md` | The actual GRRM prose. POV-locked, scene-anchored, full narrative texture. | `chunk_id`, `chapter` (e.g., `agot-eddard-12`), `book`, `pov`, `position_in_chapter`, `mentioned_slugs` (from Pass 1's per-chapter mention list, resolved via alias-resolver), `cite` |

**Why this works as a join:** when a query needs context about an entity, retrieval pulls (a) its node + edges, (b) wiki prose chunks where `node_slug == entity` or `entity in mentioned_slugs`, (c) book chunks where `entity in mentioned_slugs` (and optionally where `pov == entity`). The LLM gets all three layers as input context; it synthesizes citing each.

---

## Architecture

```
                      ASOIAF CHAT UI QUESTION
                              │
                              ▼
                  ┌───────────────────────────┐
                  │    QUERY ROUTER           │
                  │  (decides corpus mix)     │
                  └───────────┬───────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────────┐  ┌──────────────────┐
   │ GRAPH       │   │ WIKI PROSE      │  │ BOOK CHUNK       │
   │ TRAVERSAL   │   │ SEMANTIC SEARCH │  │ SEMANTIC SEARCH  │
   │             │   │                 │  │                  │
   │ - Slug match│   │ - Vector embed  │  │ - Vector embed   │
   │ - Edge walk │   │   query         │  │   query          │
   │ - Cross-ref │   │ - Top-K nearest │  │ - Top-K nearest  │
   │   lookup    │   │ - Filter on     │  │ - Filter on      │
   │ - Per-entity│   │   mentioned_    │  │   pov, book,     │
   │   index     │   │   slugs intersect  │   mentioned_     │
   │             │   │   with graph    │  │   slugs intersect│
   └──────┬──────┘   └────────┬────────┘  └─────────┬────────┘
          │                   │                     │
          └───────────────────┼─────────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ SLUG INTERSECTION JOIN  │
                  │ (chunks ↔ graph nodes)  │
                  └───────────┬─────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ SPOILER GATE             │  ← fully OPEN for v1
                  │ (additive filter, v2+)   │
                  └───────────┬─────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ CITATION ASSEMBLER       │
                  │ - Every chunk has a cite│
                  │ - Every edge has a cite │
                  │ - Bundle into context   │
                  └───────────┬─────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ LLM SYNTHESIS            │
                  │ (Claude API w/ caching) │
                  └───────────┬─────────────┘
                              │
                              ▼
                          ANSWER
                  (with inline citations,
                   click to expand source)
```

---

## Query router (the dispatch decision)

The router decides what mix of retrieval to apply. Three rough question categories:

**Structured questions** (graph-heavy):
- "Who is Tyrion's father?" → graph traversal
- "Who has the title Hand of the King?" → graph traversal across HOLDS_TITLE edges
- "Which houses are sworn to House Stark?" → SWORN_TO inverse traversal

For these, prose retrieval is optional (could provide flavor text, but the structured answer is sufficient).

**Narrative questions** (prose-heavy):
- "Describe the Red Wedding"
- "What's a scene that shows Tywin's cruelty?"
- "Find passages where Sansa thinks about Joffrey"

For these, vector search over wiki prose + book chunks is the primary; graph traversal is secondary (provides context after the chunks are surfaced).

**Hybrid questions** (need both):
- "Tell me about Tywin's relationship with Tyrion" → graph for the structural relationship, prose for the texture
- "What's known about Jon Snow's parentage?" → graph for the relevant nodes (Lyanna, Rhaegar) + their edges (LOVER_OF, etc.) + prose for the narrative arc + Pass 5 theory evidence (when Pass 5 ships)

Most chat UI questions are hybrid. Default behavior: hit all three corpora, intersect on slugs, surface ranked combined results to the LLM.

**Router implementation v1: simple heuristic.** Keywords like "describe", "scene", "find a passage" trigger prose-heavy. Keywords like "who", "what house", "what title" trigger graph-heavy. Plain entity-mention queries trigger hybrid. Don't overengineer — most queries can hit all three corpora and let the LLM decide what's relevant.

**Router implementation v2 (later):** an LLM-based query classifier that picks the corpus mix. Maybe a small fast model. Probably unnecessary if v1 heuristic is good enough.

---

## Chunking strategy

### Wiki prose chunks

The Stage 3b prose files (`prose/<slug>.prose.md`) are already structured by `## Section` headings. Chunk by section + paragraph-bounded:

- One chunk per `## Section` if the section is < ~800 words
- Larger sections split paragraph-bounded into ~500-800 word chunks
- Preserve `### Subsection` boundaries (e.g., `### A Game of Thrones` inside `## Narrative Arc`) — these are book-bounded chunks, useful for spoiler gating later
- Each chunk includes its parent `node_slug` + section + subsection in metadata
- Mention extraction: walk markdown links `[anchor](wiki:Page)` in the chunk → kebab-case → resolve via alias-resolver → emit `mentioned_slugs` list

Chunker output (one row per chunk in JSONL):
```json
{
  "chunk_id": "wiki-prose-tyrion-lannister-narrative-arc-002",
  "source_type": "wiki-prose",
  "node_slug": "tyrion-lannister",
  "section": "## Narrative Arc",
  "subsection": "### A Storm of Swords",
  "text": "<500-800 words of prose>",
  "mentioned_slugs": ["tywin-lannister", "shae", "jaime-lannister", "casterly-rock"],
  "cite": "wiki:Tyrion_Lannister.cite_ref-...",
  "char_count": 4823,
  "word_count": 712
}
```

### Book chapter chunks

Chapter files at `sources/chapters/<book>/<chapter>.md` have YAML frontmatter (book, POV, chapter number, sequence) + chapter prose. Chunk paragraph-bounded into ~500-1000 word chunks:

- Respect paragraph boundaries — never split mid-paragraph
- Respect scene breaks (often denoted by blank lines or `* * *` markers in the source) — never split across scenes
- Include 1 paragraph of overlap between adjacent chunks for boundary-spanning queries
- Each chunk's `mentioned_slugs` comes from Pass 1's per-chapter character/location mention lists, RESOLVED THROUGH ALIAS-RESOLVER. Example: Pass 1 chapter extraction lists "Theon" → alias-resolver maps to `theon-greyjoy` → goes into `mentioned_slugs`

Chunker output:
```json
{
  "chunk_id": "agot-eddard-12-chunk-007",
  "source_type": "book-chapter",
  "book": "agot",
  "chapter": "agot-eddard-12",
  "pov": "eddard-stark",
  "position_in_chapter": 7,
  "text": "<500-1000 words of GRRM prose>",
  "mentioned_slugs": ["catelyn-stark", "robert-i-baratheon", "ice"],
  "cite": "agot-eddard-12:para-7-13"
}
```

### Why mention-tagging matters

The mention list is what makes graph + prose retrievable together. Without `mentioned_slugs`, you can semantic-search prose, but you can't cleanly say "show me chunks ABOUT Tywin that ALSO mention Tyrion." The mention metadata makes that intersect query a structured filter.

For wiki prose: trivial (markdown links).
For book chapters: derived from Pass 1's per-chapter extractions + alias-resolver. AGOT chapters are ready to chunk this way today; ACOK/ASOS/AFFC/ADWD become ready as Pass 1 completes for each.

---

## Embedding pipeline

### Model choice (decide later)

Three viable options:
- **Voyage AI** (currently best for text retrieval; paid API; ~$0.10 per million tokens)
- **OpenAI text-embedding-3-large** (good, cheaper than Voyage; paid API)
- **Local nomic-embed-text** (free, runs on Mac; lower quality but adequate for narrative-rich content like this)

For a personal chat UI, local embeddings are fine. For a shared product (later), Voyage or OpenAI for quality.

**Decision: defer until chat UI build.** Embeddings are a one-time cost per chunk; switching models means re-embedding the corpus. Pick once, after a small bake-off.

### Vector store (decide later)

Three viable options:
- **SQLite + FTS5 + sqlite-vec extension** — file-based, no server, perfect for personal local use
- **LanceDB** — file-based, vector-native, good for embeddings
- **Chroma** — most batteries-included, slightly heavier

**Decision: SQLite + sqlite-vec for v1.** It's a single file, no server, dead simple to back up, supports both vector and full-text search in one query. Migration to LanceDB or Chroma later is straightforward (export/import JSONL).

### Pipeline shape

```
chunked-corpus.jsonl  (from chunker)
        │
        ▼
embed-corpus.py       — walks chunks, calls embedding model, writes vectors
        │
        ▼
working/embeddings/<model>/<corpus>.sqlite
        │             — chunks table: chunk_id, text, metadata
        │             — vectors table: chunk_id, vector
        │             — fts table: chunk_id, text (full-text fallback)
        ▼
query-corpus.py       — given a query, returns top-K chunks + their metadata
                        (used by the chat UI's retrieval layer)
```

**Idempotent:** re-embedding the same chunk produces the same vector (assuming same model). Adding new chunks doesn't re-embed existing ones. Chunk IDs are stable across runs.

---

## Spoiler gating (default OPEN for v1)

`first_available` is deferred per project policy. v1 chat UI ships with no spoiler filter:

- Every chunk is retrievable regardless of which book it's from
- Every edge is traversable regardless of when it was established
- No "where are you in the books?" UI
- No per-query gate stage

**v2+ when `first_available` ships:**
- Each chunk gains `first_available` metadata (book + chapter)
- Each edge inherits `first_available` from its source (and the underlying claim's cite_ref)
- Query layer adds an optional filter: "first_available <= user-read-progress"
- UI adds a "set my read-progress" interaction
- The filter is ADDITIVE — doesn't change the corpus shape, just hides what shouldn't show

The retrieval layer is designed to make this an opt-in filter, not a structural change. v1 doesn't pay any complexity tax for v2's eventual feature.

---

## Citation chain

Every retrieved chunk and every traversed edge carries its citation. The LLM synthesis step produces an answer with inline citations; the chat UI renders the citations as expandable inline references.

**Source-of-truth for each citation type:**

| Citation form | Resolves to | UI rendering |
|---------------|-------------|--------------|
| `(agot-bran-01)` | `extractions/mechanical/agot/agot-bran-01.md` (Pass 1 extraction) AND/OR `sources/chapters/agot/agot-bran-01.md` (chapter source) | "AGOT, Bran I" with click-to-show-quote |
| `(wiki:Page.cite_ref-X)` | wiki cache page (HTML) | "Wiki: <Page Name>" with click-to-open-wiki |
| `(track_b: Father)` | parser-level infobox field | "From Wiki Infobox" |
| `(wiki:Page)` | generic wiki page reference | "Wiki: <Page Name>" |
| `(node:<slug>)` | graph node | "From <Entity Name>" with click-to-show-node |

**Citation hygiene comes from the citation-validator agent** (already designed) — it ensures every claim has a resolvable cite before the chat UI ships. If citation-validator surfaces broken cites, the chat UI doesn't ship until they're fixed.

---

## LLM synthesis

The synthesis step takes:
- Top-K retrieved chunks (with metadata)
- Relevant graph traversal results (nodes + edges)
- The user's question

Produces:
- A grounded answer with inline citations
- Suggested follow-up queries ("Want to know more about Tyrion's trial?")

**Implementation choice:** Claude API directly with prompt caching for the long-lived parts of the prompt (system prompt + retrieval-format-spec + recent corpus context).

**Model choice:** Claude Sonnet for cost-conscious synthesis, Claude Opus for hardest questions. Adaptive routing — easy questions use Sonnet, complex multi-hop questions use Opus.

**Prompt structure:**
- System prompt: "You are an ASOIAF expert grounded in the Weirwood Network. Cite every claim. If the retrieved context doesn't answer the question, say so. Never invent facts."
- Retrieved context: top-K chunks + graph traversal results, formatted as a structured block
- User question: as-is

Prompt caching: the system prompt is stable. The corpus context might be partially stable across questions if user is exploring related topics. Both are cache-cacheable.

---

## Build order

```
PHASE 1 — Today's foundation (already mostly done)
 ✓ Graph: 4,239 nodes with edges, citations, prose sections
 ✓ Wiki prose files: 2,988 prose files at working/wiki-pass2/<bucket>/prose/
 ✓ Cross-references index: 81,090 references mapped
 ✓ Alias resolver: working/wiki-parsed/alias-resolver.json

PHASE 2 — Pre-chat-UI prep (build before any chat UI ships)
 ☐ Stage 4: prose-derived edges (current pipeline plan)
 ☐ Pass 1 catch-up: ACOK + ASOS at minimum (book chunks need mention-tagging)
 ☐ Per-entity index tables: graph/index/<type>/<slug>.index.json
 ☐ Wiki prose chunker: scripts/chunk-wiki-prose.py
 ☐ Book chapter chunker: scripts/chunk-book-chapters.py
 ☐ Mention-tagging in chunks: link-extraction (wiki) + Pass-1-derived (chapters)

PHASE 3 — Embedding + vector store
 ☐ Pick embedding model (bake-off)
 ☐ scripts/embed-corpus.py
 ☐ SQLite + sqlite-vec setup
 ☐ Index both corpora (wiki prose chunks + book chapter chunks)

PHASE 4 — Retrieval layer
 ☐ scripts/query-corpus.py — semantic search interface
 ☐ Graph traversal helper (already implicitly available via grep + JSON)
 ☐ Slug intersection logic
 ☐ Spoiler gate stub (returns "no filter" for v1)

PHASE 5 — Chat UI itself
 ☐ Pick frontend (CLI? Streamlit? Custom React? Open-source library?)
 ☐ Wire the retrieval layer to LLM synthesis
 ☐ Citation rendering with click-to-expand
 ☐ Follow-up query suggestions
 ☐ Conversation memory (across multiple turns in one session)

PHASE 6 — Quality + iteration
 ☐ Smoke test against ASOIAF question categories (factual, narrative, hybrid)
 ☐ Identify systematic failure modes (e.g., questions that need Pass 3 voice analysis but it's not built yet)
 ☐ Add Pass 3-6 corpora as they ship
 ☐ Spoiler gate v2 when first_available backfill ships
```

**Phase 2 is the bottleneck — book chunking can't fully start until Pass 1 has multi-book coverage.** This means: get Pass 1 finished for all 5 books BEFORE building the chat UI. AGOT-only chat UI is a proof of concept; AGOT+ACOK is meaningful; all 5 books is shippable.

---

## Deployment for the D&D-group preview

This section was added when scope shifted from personal-local to friend-group-shareable.

### Architecture for shared deployment

The chat UI deploys as a page on Matt's existing `mattnoth.com` site (`mattnoth.com/projects/<slug>`), with this repo (`asoiaf-chat`) included as a **git submodule** of `mattnoth-dev`. The chat UI component is **pure TypeScript + CSS** — no framework lock-in — so it embeds cleanly into whatever stack `mattnoth-dev` runs.

```
┌────────────────────────────────────────────────────────────────┐
│  mattnoth.com (Vercel/Netlify, deployed from mattnoth-dev repo) │
│                                                                 │
│  /projects/<slug>  page  ──┐                                   │
│                            │ imports ChatComponent from        │
│                            ▼                                    │
│  ┌──────────────────────────────────────┐                      │
│  │ asoiaf-chat (git submodule)          │                      │
│  │                                      │                      │
│  │ ui/component/chat.ts                 │                      │
│  │ ui/component/chat.css                │                      │
│  │ ui/component/types.ts                │                      │
│  │                                      │                      │
│  │ Pure TS + CSS, no React / Vue / etc. │                      │
│  │ Works as Web Component OR plain      │                      │
│  │ DOM with explicit hooks              │                      │
│  └──────────────────────────────────────┘                      │
│                                                                 │
│  Page-level auth (mattnoth-dev gates URL) OR                   │
│  Component-level auth (chat prompts for shared password)       │
└─────────────────────────────────┬───────────────────────────────┘
                                  │ fetch /api/query
                                  │ (POST, JSON, with auth header)
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  Backend service (separately deployed; Render / Fly.io)        │
│                                                                 │
│  Python FastAPI server                                          │
│  - Holds Anthropic API key (server-side env var)               │
│  - Holds vector store (SQLite + sqlite-vec, bundled)           │
│  - Holds graph nodes (read from this repo's graph/nodes/)      │
│  - Implements query router + retrieval + LLM synthesis         │
│  - Returns cited answer                                         │
│                                                                 │
│  Deploys independently from mattnoth.com — chat-UI updates and │
│  backend updates are decoupled.                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why submodule + pure TS+CSS works here

mattnoth-dev's stack (confirmed by reading `/Users/mnoth/source/mattnoth-dev/CLAUDE.md` and `package.json`):

| Layer | mattnoth-dev's choice |
|-------|----------------------|
| Language | TypeScript 5.8+, ES2024 target |
| Styling | Native CSS (no Sass, no PostCSS, no CSS-in-JS, no Tailwind) |
| Bundler | esbuild |
| Content | Markdown + frontmatter (gray-matter, marked) |
| Type check | `tsc --noEmit` |
| Hosting | Netlify free tier |
| Framework runtime | **NONE** — explicit hard rule |

The chat component slots into this stack natively:

- **Source travels with this project.** Chat component evolution lands in `asoiaf-chat` repo. `mattnoth-dev` pulls the latest via `git submodule update` and rebuilds.
- **Stack-aligned.** Pure TS + native modern CSS matches mattnoth-dev's hard rules exactly. No frameworks, no Sass, no CSS-in-JS — same constraints.
- **esbuild handles bundling.** mattnoth-dev's existing `tsx build/build.ts` build pipeline can compile the chat component alongside everything else. No new bundler needed.
- **CSS cascade-layers integrate.** mattnoth-dev uses `@layer reset, tokens, typography, layout, components, animations, utilities;` — the chat component's styles live in the `components` layer. No specificity wars.
- **Backend deploys independently.** Backend service updates don't redeploy mattnoth.com.
- **Versioned together with the corpus.** Submodule pin = precise version of the chat UI. When corpus updates and component changes to consume new edge types, mattnoth-dev's submodule pin advances atomically.

### Specific TS + CSS conventions to follow (inherited from mattnoth-dev)

These are not preferences — they're hard constraints of the host site:

**TypeScript (browser code in chat component):**
- Target: ES2024
- `module: ESNext` + `moduleResolution: bundler`
- `verbatimModuleSyntax: true` — use `import type` / `export type` for type-only
- `erasableSyntaxOnly: true` — no enums, no namespaces, no parameter properties; use `as const` objects
- `noUncheckedIndexedAccess: true` — handle index access defensively
- Never `any`. Use `unknown` + narrowing.
- Use `satisfies` for config validation
- Use modern stdlib: `Object.groupBy`, `Map.groupBy`, `Set.union`/`intersection`, `Promise.withResolvers`
- Template literal types for route paths / CSS class names where it adds safety

**Native CSS:**
- Cascade layers: chat component styles live in `@layer components`
- Native CSS nesting: `.weirwood-chat { & .message { … } &:hover { … } }`
- Colors: `oklch()` and `color-mix(in oklch, …)` only — NO hex, NO `rgb()`, NO named colors in new code
- Design tokens as CSS custom properties on `:root` — chat component reads `--chat-bg`, `--chat-fg`, `--chat-accent`, `--chat-font-family` etc., falls back to defaults
- Container queries (`container-type: inline-size` + `@container`) for component-scoped responsive — NOT media queries
- Logical properties: `margin-inline`, `padding-block`, `inline-size`, `block-size`
- `dvh` / `svh` / `lvh` for viewport sizing
- `:has()` where it replaces JS for parent-aware styling
- `@media (prefers-reduced-motion: reduce)` always present
- Mobile-first base styles, enhance with container queries

### Directory layout (revised to fit mattnoth-dev's specialist-subagent ownership)

mattnoth-dev has strict directory ownership (one specialist subagent per directory). The chat UI submodule respects this:

```
asoiaf-chat/  (this repo, included as a submodule in mattnoth-dev)
├── ui/
│   ├── ts/                           ← TS specialist territory
│   │   ├── chat.ts                   ← entry point
│   │   ├── api-client.ts             ← fetch wrapper
│   │   ├── citation-renderer.ts      ← citation expansion
│   │   ├── types.ts                  ← shared types
│   │   └── index.ts                  ← public exports
│   ├── styles/                       ← CSS specialist territory
│   │   ├── chat.css                  ← @layer components scoped
│   │   └── tokens.css                ← optional default token values
│   ├── README.md                     ← embedding instructions for mattnoth-dev
│   └── tsconfig.json                 ← matches mattnoth-dev's TS rules
├── backend/
│   ├── main.py                       ← FastAPI app
│   ├── retrieval.py
│   └── ...
└── (existing graph/, scripts/, etc.)
```

When integrated into mattnoth-dev:
- `mattnoth-dev/src/ts/projects/asoiaf-chat/` symlinks or imports from `../../asoiaf-chat/ui/ts/`
- `mattnoth-dev/src/styles/components/asoiaf-chat.css` imports `../../asoiaf-chat/ui/styles/chat.css`
- `mattnoth-dev/src/content/projects/asoiaf-chat.md` is the markdown content + frontmatter for `mattnoth.com/projects/asoiaf-chat`
- Page template embeds the component via the standard mattnoth-dev pattern (TS-loaded interactive island in a static page)

### Specialist-subagent integration with mattnoth-dev

mattnoth-dev's existing specialist subagents (build-specialist, css-specialist, ts-specialist, content-specialist, reviewer) own that side of the integration. The asoiaf-chat repo's UI-build fleet (frontend-developer, etc.) owns the chat component itself.

**Boundary:**
- Chat component code (TS + CSS) → asoiaf-chat repo's UI-build fleet
- Page template + content + integration glue → mattnoth-dev's specialists
- The two coordinate via the submodule interface — clean handoff at the directory boundary

When the chat component needs page-level integration help (responsive layout in mattnoth-dev's grid, theme-token wiring, etc.), the orchestrator dispatches to mattnoth-dev's specialists in a separate session. Bidirectional but isolated.

### Integration constraints (deeper than a typical embed)

Matt noted this UI is "more integration" than past submodule projects. Two specific design accommodations:

1. **Style integration.** The component reads CSS variables (custom properties) for theming — `--chat-bg`, `--chat-fg`, `--chat-accent`, `--chat-font-family`, etc. — with sensible defaults. `mattnoth-dev` can override these to match the site's design system, or the component falls back to its own polished defaults. This avoids the "embedded widget looks foreign" problem.

2. **Layout integration.** The component renders into a parent-defined container. It doesn't take over the page; it fits whatever box `mattnoth-dev`'s page layout gives it. Responsive: works in a sidebar, a centered article column, or full-width. Component reads its container's dimensions, doesn't impose absolute positioning.

3. **Asset isolation.** All the chat component's CSS is scoped (CSS Modules, or scoped class names like `.weirwood-chat__message`). No global selectors that could fight `mattnoth-dev`'s existing styles.

4. **Optional Web Component wrapper.** For maximum embedding-isolation, the component can be wrapped as a Web Component (`<weirwood-chat>` custom element with shadow DOM). Matt's call whether to ship that wrapper or the bare TS/CSS — depends on `mattnoth-dev`'s framework comfort.

### File layout in this repo

```
asoiaf-chat/                          (this repo)
├── ui/
│   ├── component/
│   │   ├── chat.ts                   ← entry point: ChatComponent class
│   │   ├── chat.css                  ← scoped styles
│   │   ├── types.ts                  ← TypeScript types for messages/citations
│   │   ├── api-client.ts             ← fetch wrapper for backend calls
│   │   ├── citation-renderer.ts      ← inline-citation expansion logic
│   │   └── index.ts                  ← public exports
│   ├── README.md                     ← embedding instructions for mattnoth-dev
│   └── tsconfig.json                 ← compile to ES modules + .d.ts
├── backend/
│   ├── main.py                       ← FastAPI app
│   ├── retrieval.py                  ← query router + vector search
│   ├── synthesis.py                  ← Anthropic API + prompt caching
│   └── ...
└── (existing graph/, scripts/, etc.)
```

### Storage (backend side, unchanged from prior design)

- **SQLite + sqlite-vec file:** wiki prose chunks + book chunks + embeddings. ~500MB-2GB. Bundled with backend deployment as a static asset.
- **Graph nodes:** read directly from this repo's `graph/nodes/<type>/<slug>.node.md`. Bundled with backend deployment.
- **Vector store rebuild:** when corpus changes, re-embed → produce new SQLite file → backend redeploy. Probably monthly cadence.

### Deploy boundaries vs .gitignore (the legal-safety architecture)

The `weirdwood-network` GitHub repo is PRIVATE. Books and chapters are gitignored (`sources/raw/`, `sources/chapters/`). This creates an intentional separation between what Netlify can deploy and what the backend host can deploy:

```
           NETLIFY (Frontend, mattnoth.com)              SEPARATE BACKEND HOST (Render/Fly)
           Auto-publishes from main branch               Deploys via private container registry
           ╔════════════════════════════════╗            ╔═══════════════════════════════════╗
           ║  CAN access:                   ║            ║  CAN access:                      ║
           ║  ✓ Chat UI component (TS+CSS)  ║            ║  ✓ Backend code (FastAPI server)  ║
           ║  ✓ Graph node files            ║   fetch    ║  ✓ Wiki prose chunks + embeddings ║
           ║  ✓ Wiki-derived prose          ║◄──────────►║  ✓ BOOK CHUNKS + EMBEDDINGS       ║
           ║  ✓ Page templates              ║   HTTPS    ║  ✓ Anthropic API key (env var)    ║
           ║                                ║            ║                                   ║
           ║  CANNOT access:                ║            ║  How books arrive:                ║
           ║  ✗ Books (gitignored)          ║            ║  → Local build, books baked into  ║
           ║  ✗ Book chunks (derived from   ║            ║    container, push to private     ║
           ║    gitignored content)         ║            ║    registry (GitHub Container     ║
           ║  ✗ Anthropic API key           ║            ║    Registry, free tier)           ║
           ╚════════════════════════════════╝            ╚═══════════════════════════════════╝
```

**Properties:**
- The .gitignore rule (`sources/raw/`, `sources/chapters/`) is what makes Netlify auto-publish-from-main SAFE. Copyrighted content can never reach the public-facing host because it can never reach the repo.
- The frontend is publicly deployed; backed by a backend that holds the copyrighted material. The backend is friend-group-only (auth gate) but technically holds the books.
- Frontend and backend are deployed via DIFFERENT mechanisms — Netlify for frontend (Git-driven), private container registry for backend (manual-build-and-push). This is the intentional asymmetry.

**Three options for getting books to the backend** (pick when building the backend deploy):

| Option | Mechanism | Tradeoff |
|--------|-----------|----------|
| **A. Local build + private container registry** | Build Docker container locally (your machine has books), push to GitHub Container Registry, Render/Fly pulls | Most polished. Monthly rebuild matches corpus update cadence. Books baked into private container image. **Recommended.** |
| **B. Cloud storage at runtime** | Books in private S3/R2 bucket, backend pulls at startup with stored creds | Most legally hygienic — books fetched at runtime, not in deploy artifact. Backend startup slower. |
| **C. Rsync to persistent disk** | Render/Fly persistent volume; rsync books once per corpus update | Simplest deploy. Books live on the server continuously. |

**Netlify access to private submodule:**
For mattnoth-dev (deployed on Netlify) to include asoiaf-chat as a private submodule, authorize Netlify's GitHub app on the `weirdwood-network` repo (one-time OAuth flow in Netlify repo connection settings). Netlify will then have read access to fetch the submodule during build.

### Auth: minimum viable for friend group

Pick the simplest thing that works:
- **Shared password** in an env var; chat UI prompts for it on first visit, sets a long-lived cookie. Trivial to implement, fine for a small known group.
- **Magic-link email auth** (no passwords, ~30 lines of code with most modern auth libraries). One step better.
- **Discord OAuth** if the D&D group already lives in Discord. Nice UX, slightly more setup.

**Lean: shared password for v1, swap for magic-link if the group grows past ~10 people.** Don't build user accounts, profiles, conversation history, etc. — you can add later if real demand surfaces.

### Cost envelope (rough estimate for D&D-group scale)

For a group of 5-10 people running maybe 5-20 queries each per D&D session:
- **Hosting:** $0-20/month (Vercel free tier for frontend; Render/Fly.io free or $5-15/mo tier for backend)
- **Anthropic API:** depends on per-query token spend. Rough math: ~3K input tokens (retrieved context) + ~500 output tokens per query = ~$0.05/query at Sonnet rates. 100 queries/month = $5. 1,000 queries/month = $50.
- **Vector store:** $0 (file-based, ships with deployment)
- **Embeddings refresh:** one-time per corpus change, ~$5-20 each (Voyage/OpenAI rates for the full corpus)

**Total realistic monthly cost for a D&D-group preview: $10-50/month.** Low enough that you can self-fund or split among the group.

### Book content + copyright posture

This is the most sensitive part. The honest landscape:

**Copyright reality:** GRRM's books are copyrighted. Storing the full text on a server and surfacing chunks to users is in fair-use gray area — closer to "research and criticism" than to "republishing," but not 100% defensible if challenged. The risk is exceedingly low for a small private friend group; it scales with audience size and visibility.

**Posture for the D&D-group preview** (proceed-with-caution-and-some-defensible-choices):

1. **Friend-group only, behind auth.** No public access. No SEO. Don't broadcast. The legal exposure of a 5-10 person Discord-private chat tool is minimal in practice — equivalent to a book club discussing passages.

2. **Synthesis-not-quotation default.** Instruct the LLM to synthesize answers from retrieved chunks rather than quoting GRRM verbatim. Short quoted phrases (under ~20 words) are fair-use-defensible; long quoted passages are not. Build this into the system prompt: "When citing the books, paraphrase or use brief quoted phrases under 20 words. Do not output passages longer than that even if asked."

3. **Snippet-limit on retrieval display.** When the chat UI shows "source" expansion for a book chunk, render only ~50 words of context, not the full chunk. The full chunk is in the LLM's context for synthesis but doesn't get exposed to the user verbatim.

4. **No download / no copy-friendly layout.** Don't make the chat UI a way to extract the book text. Disable text selection on book-source expansions if needed.

5. **Be ready to remove if asked.** If GRRM's people or Penguin/Bantam ever notice and ask, take it down promptly. Document this commitment somewhere visible (a README or footer note: "personal research project; will respect any takedown request").

6. **Public-facing version, if ever:** would need to either (a) replace book chunks with derived summaries, (b) require users to upload their own legitimately-purchased ebook for processing locally, or (c) license the text. None of these are tonight's problem.

**v1 implementation — what to build:**
- Embed the full book chunks (you have them locally; this is one-time work)
- Bundle with backend deployment behind auth
- LLM system prompt enforces synthesis-not-quotation
- UI renders short snippets only on source expansion

This is defensible-enough for a small private friend group. If the project scales beyond that, revisit.

### Update to build order (deployment-aware)

```
PHASE 1 — Foundation (in progress)
 ✓ Graph nodes, wiki prose, cross-references, alias-resolver

PHASE 2 — Pre-deployment prep
 ☐ Stage 4 prose-derived edges
 ☐ Pass 1 catch-up (ACOK + ASOS minimum; ideally all 4)
 ☐ Per-entity index tables
 ☐ Wiki prose chunker
 ☐ Book chapter chunker
 ☐ Mention-tagging

PHASE 3 — Embedding + retrieval
 ☐ Pick embedding model (recommend Voyage for production-quality)
 ☐ Embed all three corpora
 ☐ SQLite + sqlite-vec setup
 ☐ Query router + retrieval helpers

PHASE 4 — Backend service
 ☐ FastAPI server with /query endpoint
 ☐ Auth middleware (shared password for v1)
 ☐ Anthropic API integration with prompt caching
 ☐ System prompt enforcing synthesis-not-quotation

PHASE 5 — Frontend
 ☐ Pick frontend stack (Next.js + Vercel AI SDK, or Streamlit)
 ☐ Chat UI with citation expansion
 ☐ Auth gate
 ☐ Conversation memory within session

PHASE 6 — Deploy and iterate
 ☐ Deploy backend (Render/Fly/Railway)
 ☐ Deploy frontend (Vercel/Netlify)
 ☐ Share invite link with D&D group
 ☐ Iterate based on real questions
```

**Honest milestone to watch:** Phase 5 is "the chat UI exists and is shareable." Phases 2-3 are "the corpus is ingested and queryable." If Phases 2-3 are done well, Phases 4-5 are 1-2 weeks of focused work.

---

## UI Build Fleet — separate from the construction fleet

The chat UI build is its own orchestration concern, parallel to the construction-side fleet (`working/agent-pipeline-plan.md`). Different work shape: construction is bounded ("ingest the corpus, ship structured output"); UI is continuous ("iterate on a product based on user feedback, ship updates indefinitely"). Different agents, different cadence, different success criteria.

The runtime architecture already supports this — `working/fleet-runtime-architecture.md` § "Multi-orchestrator support" describes how the `check-fleet` skill can iterate over multiple orchestrators by name. The construction fleet runs as `fleet-construction` tmux session; the UI build fleet runs as `fleet-ui-build` tmux session. Same skill, two state-file paths.

### UI-build fleet roster (initial, all stubs until needed)

| Agent | File | Status | Role |
|-------|------|--------|------|
| `frontend-developer` | `.claude/agents/frontend-developer.md` | Stub (future) | Implements/modifies Next.js or Streamlit chat UI components from a spec. Focused on UI code, not on retrieval logic. |
| `backend-developer` | `.claude/agents/backend-developer.md` | Stub (future) | Implements/modifies FastAPI endpoints, retrieval helpers, and the query layer. Doesn't touch frontend. |
| `prompt-engineer` | `.claude/agents/prompt-engineer.md` | Stub (future) | Iterates on the LLM synthesis system prompt — the prompt the chat UI sends to Anthropic for each query. Tests against a regression suite of ASOIAF questions. |
| `deployment-engineer` | `.claude/agents/deployment-engineer.md` | Stub (future) | Handles Vercel/Render config, env vars, deploy scripts, GitHub Actions. Production-config concerns only. |
| `chat-ui-tester` | `.claude/agents/chat-ui-tester.md` | Stub (future) | Runs the chat UI through a regression suite of ASOIAF questions; evaluates answer quality (correctness, citation hygiene, defensibility-against-quotation-rules). |
| `ux-feedback-analyzer` | `.claude/agents/ux-feedback-analyzer.md` | Stub (future, post-launch) | Reads user query logs (post-deployment), identifies common-question patterns the chat handles poorly, proposes UI improvements. |
| `embedding-refresh-runner` | `.claude/agents/embedding-refresh-runner.md` | Stub (future) | Triggered when underlying corpus changes (graph nodes promoted, prose updated). Re-embeds affected chunks, validates the vector store post-refresh. Mostly Python with agent-quality-check supervision. |

### UI-build orchestration cadence

The construction fleet runs as one big multi-day batch. The UI-build fleet runs as small task-specific bursts:

- **Build a feature:** orchestrator dispatches `frontend-developer` + `backend-developer` in parallel for a defined ticket; reviews their output via `prompt-engineer` reviewing prompt changes + `chat-ui-tester` regression check; deploys via `deployment-engineer` if green.
- **Iterate on retrieval quality:** dispatches `prompt-engineer` against the regression suite; if scores improve, ships.
- **Refresh corpus:** dispatches `embedding-refresh-runner` when `graph/nodes/` or `working/wiki-pass2/` mtime advances.
- **Post-launch quality:** weekly `ux-feedback-analyzer` run on logs.

These are **bursts** — minutes-to-hours, not days. Each is initiated either manually (Matt has a feature in mind) or by a trigger (corpus mtime change, weekly cron).

### Why separate from the construction fleet

- **Different success criteria:** construction succeeds when 4,239 nodes become 5,000+ with prose-derived edges. UI build succeeds when D&D-group questions get good answers and the friends use it.
- **Different review patterns:** construction reviewers (`prose-edge-reviewer`, `cross-identity-reviewer`) check structural correctness against a fixed schema. UI reviewers (`chat-ui-tester`) check subjective answer quality against an evolving regression suite.
- **Different deployment loop:** construction promotes to disk (graph/nodes/). UI build promotes to a hosted service (Vercel/Render). Different post-promotion checks.
- **Different blast radius:** a bad construction-fleet run produces bad data (recoverable, audit-driven). A bad UI-build run breaks the live service users see (immediate-impact, needs rollback).
- **Different test surface:** construction tests with the validators + audit agents we already have. UI build tests with a ASOIAF-question regression suite that doesn't exist yet — that's a new artifact (`working/ui-tests/regression-questions.jsonl`) the chat-ui-tester consumes.

### What goes in the UI-build TODO list (separately tracked)

A new file `working/ui-build-todos.md` (created when chat UI work begins) tracks UI-side tasks distinctly from construction-side tasks. Avoids the construction TODO list bloating with "fix the chat UI's mobile layout" items.

---

## What this architecture deliberately doesn't do (v1)

- **Conversation memory across sessions.** Each chat session is independent. Future feature: per-user history.
- **Multi-modal retrieval.** No images, maps, family trees in v1. Add when needed.
- **Real-time corpus updates.** Books don't change; wiki updates rarely. Re-embed on cadence (monthly?), not in real-time.
- **Full user accounts.** Shared password for v1. Real auth + per-user state if/when D&D group grows or audience expands.
- **Dialogue with the chat UI suggesting graph improvements.** ("This question requires Pass 3 to answer well — should I run it?") Cool but premature.
- **Public API.** Behind auth, friends-only, not exposed to the internet at large.

---

## What this architecture explicitly enables (with no extra work)

- **Cross-corpus citations.** A question can be answered by combining a graph edge + a wiki summary chunk + a book passage. The citation list can mix all three.
- **Comparison queries.** "How does Eddard differ from Tywin in their parenting?" → retrieve chunks for both, graph compares their edges (PARENT_OF, etc.), prose comparison surfaces in synthesis.
- **Long-tail entity questions.** "Who is Brienne's squire?" — a Tier-2 character (Podrick) might not be heavily in the graph yet, but his book chapters are; semantic search retrieves them.
- **Theory probing.** "Show me evidence for R+L=J." Retrieves passages from AGOT (Eddard's reflections), from ASOS (Howland Reed's hints), from ADWD (visions) — pre-Pass-5, but raw retrieval still works.
- **Citation chains.** "Why do you say X?" → "Because chunk Y from chapter Z says..." → "Show me chunk Y" → user can verify directly.

---

## Honesty about what THIS doesn't fix

**The chat UI inherits the construction layer's gaps:**

- If the graph doesn't have a node, the chat can't reach it (e.g., concept pages we deferred — `dragon`, `weirwood` — are still gaps)
- If Pass 1 hasn't run on a book, that book's chunks lack mention-tagging — semantic retrieval still works but slug-intersection is degraded
- If a wiki claim is wrong, the chat will repeat it (until contradiction-surfacer flags it and Matt fixes the source)
- If two characters share a name and disambiguation hasn't run, the chat may conflate them

**The chat UI is an honest mirror of the construction layer.** Improving the chat means improving the construction. There's no "fix the chat without fixing the data" path.

---

## Files this plan ties into

- `reference/architecture.md` — schema (entity types, edges, artifact formats); citation form definitions
- `working/fleet-runtime-architecture.md` — construction-side architecture (this doc is the retrieval-side counterpart)
- `working/agent-pipeline-plan.md` — agent fleet (this doc consumes the fleet's output)
- `working/design-philosophy.md` — Unix philosophy (applies to both construction and retrieval)
- (future) `working/runbooks/chat-ui-runbook.md` — operational procedures for embedding refresh, vector store rebuild, etc.
