# Session 8 — Architecture.md Refactor + Edge Type Expansion + Coverage Analysis

**Date:** 2026-04-24

---

## What Triggered This Session

Matt noticed that `reference/architecture.md` had drifted significantly from the actual project state. Specific concerns:
- The pipeline steps weren't updated to reflect actual progress
- The directory tree was stale (wrong paths, missing directories)
- The file was trying to serve both agents and humans, doing neither well
- The edge types (26) seemed too few compared to what we'd discussed
- The wiki entity types (characters, locations, houses, events) didn't cover everything we'd need

## Architecture.md Refactor

**Problem:** architecture.md was a hybrid of project management (directory tree, current state checklist, project overview) and schema reference (entity types, edge types, confidence tiers). Agents loaded it every session, consuming context on stale directory trees and duplicated progress tracking.

**Solution:** Stripped it to a pure schema reference. Removed:
- Directory tree (now only in CLAUDE.md, where it's maintained)
- Current State checklist (duplicated worklog.md)
- "What This Project Is" overview (in CLAUDE.md)
- The old `agents/` directory references (actual agents are at `.claude/agents/`)

Kept and expanded: entity types, edge types, confidence tiers, file naming conventions, spoiler gating, agent conventions, Pass 1 extraction schema.

## Edge Type Expansion: 26 → ~80

**Discovery:** The v1 AGOT extractions (73 chapters, archived) organically produced ~127 ad-hoc relationship types. The mechanical extractor had no controlled vocabulary, so it independently invented synonyms:
- `SERVES`, `SERVED_BY`, `CLAIMS_TO_SERVE`, `SWORN_TO`, `LOYALTY_TO`, `LOYALTY`, `LOYAL_TO`, `BANNERMAN_OF` — all meaning allegiance/service
- `CONTEMPT_FOR`, `CONTEMPT_TOWARD`, `CONTEMPT`, `CONTEMPTUOUS_OF` — same emotion, four labels
- `GRIEVES`, `GRIEVES_FOR`, `GRIEF`, `GRIEF_FOR` — couldn't agree with itself

**Additionally:** Scanned all 5,279 wiki pages with infoboxes. Found ~40+ relationship-relevant structured fields: Father, Mother, Spouse/Spouses, Lover/Lovers, Issue, Allegiance/Allegiances, Overlord/Overlords, Culture, Religion, Seat/Seats, Head, Heir/Heirs, Founder, Successor, Predecessor, Ancestral weapon, Cadet branches, Owner/Owners, Monarch, Born, Died, Buried, Alias/Aliases, Ruler, Region/Regions, Species, Conflict, Result.

**Result:** Normalized both sources into 80 formal edge types across 14 categories:
- Kinship & Family (9): PARENT_OF, SIBLING_OF, SPOUSE_OF, BETROTHED_TO, LOVER_OF, WARD_OF, ANCESTOR_OF, HEIR_TO, CADET_BRANCH_OF
- Political & Authority (11): RULES, OVERLORD_OF, SWORN_TO, COMMANDS, SERVES, ADVISES, HOLDS_TITLE, SUCCEEDS, CLAIMS, APPOINTS, DEPOSES
- Factional & Diplomatic (7): MEMBER_OF, FOUNDED, ALLIES_WITH, OPPOSES, MANIPULATES, BETRAYS, NEGOTIATES_WITH
- Military & Conflict (9): FIGHTS_IN, COMMANDS_IN, KILLS, EXECUTES, CAPTURES, PRISONER_OF, BESIEGES, DEFEATS, DUELS
- Knowledge & Information (8): KNOWS, IGNORANT_OF, SEEKS, REVEALS_TO, DECEIVES, HOARDS, INVESTIGATES, TEACHES
- Emotional & Perceptual (10): PERCEIVED_AS, TRUSTS, DISTRUSTS, RESPECTS, FEARS, LOVES, HATES, MOURNS, PROTECTS, RESENTS
- Spatial & Temporal (8): LOCATED_AT, SEAT_OF, TRAVELS_TO, BORN_AT, DIED_AT, BURIED_AT, CONTEMPORARY_WITH, REGION_OF
- Possession & Ownership (4): WIELDS, OWNS, ANCESTRAL_WEAPON_OF, FORGED_BY
- Identity & Disguise (4): ALIAS_OF, DISGUISED_AS, SAME_AS, IMPERSONATES
- Cultural & Religious (4): CULTURE_OF, WORSHIPS, SACRED_TO, CLERGY_OF
- Narrative & Literary (5): FORESHADOWS, PARALLELS, SUBVERTS, ECHOES, CONTRASTS
- Prophecy (5): FULFILLS, APPEARS_TO_FULFILL, SUBVERTS_PROPHECY, PROPHESIED_BY, SUBJECT_OF_PROPHECY
- Evidentiary (3): SUPPORTS, CONTRADICTS, CITED_BY
- Causal & Plot (5): CAUSES, PREVENTS, ENABLES, MOTIVATES, TRIGGERS
- Hospitality & Custom (3): GUEST_OF, VIOLATES_GUEST_RIGHT, GRANTS_SAFE_CONDUCT

**Key design decision:** Pass 1 (mechanical extraction) keeps recording relationships in free-text natural language. The controlled vocabulary is for the graph layer — when edges are formalized from extraction outputs. If the extractor sees something genuinely new that doesn't fit the 80 types, that's a signal to expand the taxonomy, not force-fit.

## Entity Type Hierarchy

**Problem:** Flat list of 7 entity types (character, location, faction, artifact, prophecy, theory, event) plus 7 "candidate" types. No structure, no inheritance, and `house` was awkwardly jammed into `faction`.

**Solution:** Replaced with a hierarchical taxonomy inspired by biological classification:

```
Entity
├── Character (Human, Direwolf, Dragon)
├── Place (Location, Region)
├── Organization (House, Faction, Religion)
├── Concept (Culture, Magic, Prophecy, Theory)
├── Object (Artifact, Text)
├── Event (Battle, War)
├── Species
└── Title
```

Inheritance rule: querying a parent returns all children. "Show me Organizations" → houses + factions + religions. "Show me Events" → battles + wars. Each leaf type has a Type Reference Table row with distinguishing structural fields.

## Coverage Analysis: Candidate Entity Types in AGOT Extractions

Scanned both v1 (archived) and v2 (current) AGOT extractions to measure how well the 7 candidate entity types are captured:

| Candidate Type | Coverage | Where Found | Gap |
|---|---|---|---|
| In-world Texts | 100% | Artifacts section | Well-covered, just categorized under Artifacts |
| Titles/Offices | 50% | Character descriptions, dialogue | Embedded in character data, not indexed separately |
| Culture | 40% | Houses/Factions, location context | Dothraki, wildlings, ironborn captured as factions |
| Religion | 32% | Location Descriptions (godswood, sept) | Physical locations captured, beliefs/practices scattered |
| Species/Creatures | 11% | Prologue, Bran visions only | v2 eliminated Creatures category entirely |
| War | 7% | Dialogue, character memories | Historical background only, not indexed |
| Magic | 5% | Artifacts (dragonglass only) | Warging, greensight, blood magic almost absent |

**Key finding:** The data IS in the extractions — it appears in narrative sections (Events, Dialogue, Location Descriptions). But the Raw Entity List only has 4 categories (Characters, Locations, Artifacts, Houses/Factions), so these types aren't indexed for downstream discovery.

**Verdict:** AGOT and ACOK (50/70 done) extractions are NOT invalidated. The fix is: (a) expand Raw Entity List to 10 categories for future extraction runs, (b) build a supplementary index script for already-completed chapters.

## Wiki HTML Structure Discovery

### Infobox "Books" Field (book-level)
```html
<li><a href="...">A Game of Thrones</a> <small>(POV)</small></li>
<li><a href="...">A Clash of Kings</a> <small>(mentioned)</small></li>
<li><a href="...">A Feast for Crows</a> <small>(appears)</small></li>
```
Three appearance types: `POV`, `appears`, `mentioned`. First non-"mentioned" book → book-level `first_available`.

### Citation Anchor IDs (chapter-level)
Matt remembered that wiki pages had chapter-level tags — confirmed. Wiki footnotes encode book and chapter directly in `cite_ref` / `cite_note` HTML anchor IDs:

```
cite_ref-Ragot2...   → AGOT chapter 2
cite_ref-Rasos24...  → ASOS chapter 24
cite_ref-Radwd62...  → ADWD chapter 62
```

Format: `R{book_abbrev}{chapter_number}`. Regex: `cite_ref-R([a-z]+)(\d+)`.

Eddard Stark's page has 78 unique chapter citations across all 5 books. The lowest-numbered citation per entity gives chapter-level `first_available` — far more precise than the book-level infobox data.

5,279 of 17,657 cached wiki pages have infoboxes. Citation anchors appear across an even wider set.

### `first_available` naming
Same field name everywhere (extraction + wiki). They measure the same thing from different angles and will agree. Extractions tag information with when it's revealed; wiki tags entities with when they first appear. Both use `{BOOK} {POV} {CHAPTER}` format. They cross-validate each other.

### Wiki confidence tier concern
Wiki doesn't distinguish canon from fan interpretation. A page about R+L=J presents theory alongside textual evidence as if they're the same kind of information. The wiki's category/tag system helps — pages categorized under "Theories" or "Speculation" can be routed to different confidence tiers. This is a Pass 2 design problem (wiki-category → confidence-tier mapping rules).

## Work Track Structure

Realized extraction and wiki work are independent parallel tracks:

**Track A — Extraction:** Update extractor prompt (expand Raw Entity List 4 → 10 categories) → finish ACOK + start ASOS → supplementary index for AGOT/ACOK-first-50

**Track B — Wiki/Pass 2 prep:** Write wiki infobox parser script → design Pass 2 wiki ingestion (agent prompt, node schema, promotion criteria, confidence-tier mapping)

**Convergence:** Both tracks feed into graph building. Extraction outputs + wiki nodes → typed edges using controlled vocabulary. Cross-book analytical passes (Pass 3+) need all books extracted first, but graph building can happen incrementally per-book.

Originally had ACOK completion as step 1 ("finish with current prompt for consistency"), but Matt correctly questioned this — there's no reason to finish 20 chapters with a known-deficient prompt just for consistency with the other 50. Updated sequence: prompt first, then all remaining extraction uses the improved prompt.

## Session Management Decisions

- Archived Sessions 5-7 to `history/worklog-archives/archive002.md`
- Created `progress/continue-prompts/` directory for self-contained work resumption prompts
- Created continue prompt for Track A: `progress/continue-prompts/2026-04-24-track-a-extraction-prompt-update.md`
- Established two-tier session documentation:
  - `worklog.md` session entries: ~20-30 lines, agent-facing, concise
  - `history/session-details/session-NNN.md`: full narrative, human-facing, process documentation
