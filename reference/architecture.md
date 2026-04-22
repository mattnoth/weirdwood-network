# The Weirwood Network — Project Context

> **This file is the master context for all Claude Code agents working on this project. Every agent session should load this file first to understand the system architecture, conventions, and current state.**

---

## What This Project Is

The Weirwood Network is a structured knowledge graph for A Song of Ice and Fire (ASOIAF) by George R.R. Martin. It catalogs every character, location, faction, artifact, prophecy, theory, and dangling plot thread in the series — with typed relationships between them — so that queries can traverse connections and surface insights that no single document contains.

It is also a portfolio-grade demonstration of knowledge engineering, taxonomy design, entity-relationship modeling, and agentic extraction architecture.

---

## Architecture Overview

The system has two complementary navigation layers:

### The Index (Trigger Table / Topic Table)
A lookup table that routes queries to the right content. Given a query keyword or topic, the index points to the relevant node(s) in the graph. This is the "table of contents" — it answers "where do I look?"

### The Knowledge Graph
A network of typed nodes (entities) connected by typed edges (relationships). Given a starting node, the graph reveals what connects to it and how. This is the "cross-references and footnotes" — it answers "what else is connected to this?"

**Both layers work together.** The index routes you to the right neighborhood. The graph lets you traverse once you're there.

---

## Directory Structure

```
weirwood-network/
├── CONTEXT.md                    # THIS FILE — master project context
├── README.md                     # Portfolio-facing project description
├── scripts/
│   ├── chapter-splitter.py       # Splits ebook files into per-chapter markdown
│   └── wiki-ingester.py          # Scrapes and structures AWOIAF wiki content
├── sources/
│   ├── chapters/                 # Raw chapter text (one file per chapter)
│   │   ├── agot/
│   │   │   ├── agot-prologue.md
│   │   │   ├── agot-bran-01.md
│   │   │   ├── agot-catelyn-01.md
│   │   │   └── ...
│   │   ├── acok/
│   │   ├── asos/
│   │   ├── affc/
│   │   └── adwd/
│   ├── reference/                 # Non-narrative sources (TWOIAF OCR text, etc.) — gitignored
│   └── wiki/                     # Structured wiki extractions
│       ├── characters/
│       ├── locations/
│       ├── houses/
│       └── events/
├── extractions/                  # Structured outputs from extraction agents
│   ├── mechanical/               # Pass 1: mechanical chapter extractions
│   │   ├── agot/
│   │   │   ├── agot-prologue.extraction.md
│   │   │   └── ...
│   │   └── ...
│   ├── voice/                    # Pass 3: character voice analysis
│   ├── foreshadowing/            # Pass 4: foreshadowing mappings
│   └── patterns/                 # Pass 5+: theory-informed pattern extraction
├── graph/
│   ├── nodes/                    # Entity files (one per entity)
│   │   ├── characters/
│   │   ├── locations/
│   │   ├── factions/
│   │   ├── artifacts/
│   │   ├── prophecies/
│   │   └── theories/
│   ├── edges/                    # Relationship files or edge lists
│   └── convergence-maps/         # High-density intersection documents
│       ├── oldtown.md
│       ├── the-wall.md
│       ├── meereen.md
│       └── kings-landing.md
├── index/
│   ├── trigger-table.md          # Master routing table: keyword → node(s)
│   ├── entity-index.md           # Alphabetical entity lookup
│   └── chapter-index.md          # Chapter-level metadata index
├── agents/
│   ├── pass-1-mechanical.md      # Mechanical extraction agent prompt
│   ├── pass-2-wiki.md            # Wiki ingestion agent prompt
│   ├── pass-3-voice.md           # Character voice analysis agent prompt
│   ├── pass-4-foreshadowing.md   # Known-event foreshadowing agent prompt
│   ├── pass-5-theory.md          # Theory-informed pattern extraction prompt
│   └── pass-6-discovery.md       # Open-ended pattern discovery prompt
├── curation/
│   ├── candidates.md             # Agent-proposed findings awaiting human review
│   └── decisions.md              # Human curation decisions log
└── reference/
    ├── foreshadowing-events.md   # Comprehensive list of major events to scan for
    ├── theory-seeds.md           # Core theories that inform analytical extraction
    ├── taxonomy.md               # Entity types, edge types, confidence tiers
    └── architecture-spec.md      # Full system architecture document
```

---

## File Naming Conventions

### Chapter Source Files
`{book-abbrev}-{pov-character}-{chapter-number}.md`

Book abbreviations: `agot`, `acok`, `asos`, `affc`, `adwd`

Novella codes (Tales of Dunk and Egg): `thk` (The Hedge Knight), `tss` (The Sworn Sword), `tmk` (The Mystery Knight)

Examples:
- `agot-bran-01.md` (Bran's first chapter in AGOT)
- `asos-catelyn-07.md` (Catelyn's seventh chapter in ASOS — the Red Wedding)
- `affc-prologue.md` (prologues/epilogues use that as the name)

D&E novellas use `collection: tales-of-dunk-and-egg` in frontmatter and `first_available: pre-agot` for spoiler gating (set pre-AGOT, ~90 years before the main series).

### Extraction Files
Same name as source chapter with `.extraction.md` suffix:
- `agot-bran-01.extraction.md`

### Node Files
`{entity-name-kebab-case}.node.md`
- `jaqen-hghar.node.md`
- `horn-of-joramun.node.md`
- `the-citadel.node.md`

---

## Entity Types (Node Categories)

Every node in the graph is one of these types:

| Type | Description | Examples |
|------|-------------|---------|
| `character` | Named individual | Jon Snow, Jaqen H'ghar, Patchface |
| `location` | Named place | The Citadel, Winterfell, Tower of Joy |
| `faction` | Organization or alliance | Faceless Men, Night's Watch, Golden Company |
| `artifact` | Object of narrative significance | Dragonbinder, Dawn, glass candles |
| `prophecy` | Prophetic statement or vision | Azor Ahai, Maggy the Frog, House of the Undying |
| `theory` | Interpretive framework | R+L=J, Grand Northern Conspiracy, Eldritch Apocalypse |
| `event` | Confirmed plot event | Red Wedding, Battle of the Blackwater |

---

## Edge Types (Relationship Categories)

Every relationship between nodes is one of these types:

### Causal/Plot
- `CAUSES` — Event A leads to Event B
- `PREVENTS` — Action A blocks Event B  
- `ENABLES` — Condition A makes Event B possible

### Narrative/Literary
- `FORESHADOWS` — Detail A is a Chekhov's gun for Event B
- `PARALLELS` — Event A mirrors Event B thematically
- `SUBVERTS` — Event A inverts the expectation set by B

### Factional/Political
- `MEMBER_OF` — Character belongs to Faction
- `OPPOSES` — Faction/character opposes another
- `ALLIES_WITH` — Alliance (possibly temporary)
- `MANIPULATES` — One party unknowingly used by another

### Knowledge/Information
- `SEEKS` — Character/faction pursuing artifact or knowledge
- `KNOWS` — Character possesses specific information
- `IGNORANT_OF` — Character critically lacks information
- `HOARDS` — Institution suppresses knowledge

### Prophecy
- `FULFILLS` — Event fulfills prophecy (confirmed)
- `APPEARS_TO_FULFILL` — Possible fulfillment, may be red herring
- `SUBVERTS_PROPHECY` — Contradicts expected fulfillment

### Evidentiary
- `SUPPORTS` — Textual passage supports theory
- `CONTRADICTS` — Textual passage undermines theory
- `CITED_BY` — Theory attributed to source theorist

### Spatial/Temporal
- `LOCATED_AT` — Entity at location (with book/chapter timestamp)
- `TRAVELS_TO` — Movement from location A to B
- `CONTEMPORARY_WITH` — Events happen simultaneously

### Perceptual (Cross-POV)
- `PERCEIVED_AS` — How POV Character X perceives Character Y (with chapter citation and characterization notes)

---

## Confidence Tiers

Every claim in the system has a confidence tier:

| Tier | Label | Description | Treatment |
|------|-------|-------------|-----------|
| 1 | Verified Canon | Explicitly stated in text, no ambiguity | Ground truth |
| 2 | Strong Inference | Not stated directly, but inferable with high confidence | Near-fact, note the inferential step |
| 3 | Community Consensus | Widely accepted theory with strong textual support | Leading theory, flag as unconfirmed |
| 4 | Plausible Speculation | Reasonable theory with some support, significant uncertainty | Possibility, note competing interpretations |
| 5 | Crackpot | Entertaining, minimal evidence | Include, clearly label |

---

## Spoiler Gating

Every node and extraction carries a `first_available` field: the earliest book and chapter where this information becomes available to the reader.

Format: `{BOOK} {POV} {CHAPTER_NUMBER}` or `{BOOK} Prologue/Epilogue`

Examples:
- `first_available: AGOT Bran II` (Bran's fall — available from this chapter onward)
- `first_available: ASOS Epilogue` (Lady Stoneheart reveal)

The system can filter all content to a user-declared spoiler ceiling. Any node with `first_available` above the ceiling is excluded from retrieval.

**Important:** Some information has *retroactive significance*. A fact available in AGOT may only become meaningful in ADWD. Use `significance_unlocked` as a secondary field for these cases:
- `first_available: AGOT Eddard I` / `significance_unlocked: ADWD` (Ned's internal guilt about Jon)

---

## Extraction Pass Sequence

Agents execute in this order. Each pass builds on prior outputs.

| Pass | Agent | Input | Output | Depends On |
|------|-------|-------|--------|------------|
| 1 | Mechanical | Raw chapter text | Structured chapter extraction (entities, locations, events, metadata) | Nothing — runs first |
| 2 | Wiki | AWOIAF wiki pages | Structured entity nodes with comprehensive data | Pass 1 (for cross-reference) |
| 3 | Voice & Perception | Full POV character arc (all chapters) + wiki nodes | Voice profile + cross-POV perception mappings | Pass 1, Pass 2 |
| 4 | Foreshadowing | Chapter extractions + confirmed event list | Foreshadowing edge mappings | Pass 1, event list |
| 5 | Theory-Informed | Chapter extractions + theory seed list | Theory evidence mappings, pattern flags | Pass 1, Pass 2, theory seeds |
| 6 | Discovery | Full extraction corpus | New candidate theories, unrecognized patterns | All prior passes |

---

## Agent Conventions

All agents working in this project should:

1. **Load this file first** — understand the system before doing anything
2. **Follow the file naming conventions** — consistency is critical
3. **Tag every output with confidence tiers** — nothing goes untiered
4. **Include `first_available` on every node and edge** — spoiler gating is architectural, not optional
5. **Output structured markdown** — follow the schemas defined in each agent prompt file
6. **Propose, don't decide** — analytical findings go to the curation queue as candidates, not as accepted facts
7. **Cite chapter sources** — every claim traces back to a specific chapter or wiki page

---

## Current State

> **Update this section as the project progresses.**

- [x] Chapter splitter script built
- [x] Source chapters extracted (AGOT — 73)
- [x] Source chapters extracted (ACOK — 70)
- [x] Source chapters extracted (ASOS — 82)
- [x] Source chapters extracted (AFFC — 46)
- [x] Source chapters extracted (ADWD — 73)
- [ ] Pass 1 mechanical extraction (AGOT)
- [ ] Pass 1 mechanical extraction (all books)
- [ ] Pass 2 wiki ingestion
- [ ] Index / trigger table v1
- [ ] Pass 3 voice analysis
- [ ] Pass 4 foreshadowing scan
- [ ] Pass 5 theory-informed extraction
- [ ] Graph edges formalized
- [ ] Convergence maps built
