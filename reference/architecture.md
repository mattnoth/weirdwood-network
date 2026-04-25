# The Weirwood Network — Schema Reference

> **This file is the schema reference for all agents working on this project.** It defines entity types, edge types, confidence tiers, file naming conventions, and spoiler gating. Every agent should load this file to understand the data model.
>
> For project overview, directory structure, and pipeline sequence, see `CLAUDE.md`.
> For current project state and progress, see `worklog.md`.

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

## Entity Type Hierarchy

Every node in the graph belongs to a type in this hierarchy. Child types inherit from their parent — a query for "organizations" returns houses, factions, and religions. A query for "events" returns both wars and individual battles.

This hierarchy is **extensible**. New leaf types can be added without restructuring; new intermediate types should be rare and require design review. See `working/taxonomy-candidates.md` for proposed additions under evaluation.

```
Entity
├── Character
│   ├── Human
│   ├── Direwolf          (Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog)
│   └── Dragon            (Drogon, Rhaegal, Viserion; also historical: Balerion, Vhagar)
├── Place
│   ├── Location          (specific: Winterfell, Tower of Joy, The Citadel)
│   └── Region            (geographic: The North, Dorne, The Reach, Beyond the Wall)
├── Organization
│   ├── House             (sigil, words, seat, bloodline: House Stark, House Frey)
│   ├── Faction           (Night's Watch, Faceless Men, Golden Company, Brotherhood Without Banners)
│   └── Religion          (deities, clergy, rituals, sacred sites: Faith of the Seven, R'hllor, Old Gods)
├── Concept
│   ├── Culture           (customs, language, appearance norms: Dothraki, Ironborn, Free Folk)
│   ├── Magic             (rules, practitioners, costs: warging, greensight, shadowbinding, wildfire)
│   ├── Prophecy          (Azor Ahai, Maggy the Frog, House of the Undying visions)
│   └── Theory            (R+L=J, Grand Northern Conspiracy, Eldritch Apocalypse)
├── Object
│   ├── Artifact          (Valyrian steel swords, horns, crowns: Ice, Dragonbinder, Dawn)
│   └── Text              (in-world books, letters, songs: The Jade Compendium, The Rains of Castamere)
├── Event
│   ├── Battle            (single engagement: Red Wedding, Battle of the Blackwater)
│   └── War               (multi-battle conflict: Robert's Rebellion, War of the Five Kings)
├── Species               (biological type, NOT individual: dragons-as-species, Others, Children of the Forest)
└── Title                 (formal office: Hand of the King, Lord Commander, High Septon)
```

### Type Reference Table

| Type | Parent | Description | Distinguishing Fields | Examples |
|------|--------|-------------|----------------------|----------|
| `character.human` | Character | Named human individual | name, aliases, culture, allegiance, born, died | Jon Snow, Jaqen H'ghar, Cersei Lannister |
| `character.direwolf` | Character | Named Stark direwolf | name, bonded_to, status | Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog |
| `character.dragon` | Character | Named dragon with narrative agency | name, rider, status | Drogon, Rhaegal, Viserion, Balerion |
| `place.location` | Place | Specific named place | defensive_features, architecture, ruler, region | Winterfell, Tower of Joy, The Citadel |
| `place.region` | Place | Geographic area containing locations | climate, cultures, ruling_house | The North, Dorne, The Reach, Essos |
| `organization.house` | Organization | Noble house or dynasty | sigil, words, seat, head, overlord, cadet_branches, ancestral_weapon | House Stark, House Targaryen, House Frey |
| `organization.faction` | Organization | Non-dynastic organization, order, or alliance | purpose, leadership, headquarters | Night's Watch, Faceless Men, Golden Company |
| `organization.religion` | Organization | Belief system and its institutions | deities, clergy_hierarchy, rituals, sacred_sites, moral_codes | Faith of the Seven, R'hllor, Drowned God, Old Gods |
| `concept.culture` | Concept | Ethnic or regional cultural group | customs, language, appearance_norms, marriage_practices, warfare_style | Dothraki, Ironborn, Free Folk, Braavosi |
| `concept.magic` | Concept | Magical system, ability, or phenomenon | rules, practitioners, costs, limitations | Warging, greensight, shadowbinding, glass candles |
| `concept.prophecy` | Concept | Prophetic statement or vision | prophet, text, candidates, status | Azor Ahai, Maggy the Frog, House of the Undying |
| `concept.theory` | Concept | Interpretive framework (community or textual) | evidence_for, evidence_against, confidence_tier | R+L=J, Grand Northern Conspiracy |
| `object.artifact` | Object | Object of narrative significance | material, current_holder, history | Ice, Dragonbinder, Dawn, glass candles |
| `object.text` | Object | In-world book, document, or song | author, subject, location | The Jade Compendium, The Rains of Castamere |
| `event.battle` | Event | Single engagement or plot event | location, date, participants, outcome | Red Wedding, Battle of the Blackwater |
| `event.war` | Event | Multi-battle named conflict | belligerents, causes, phases, battles, outcome | Robert's Rebellion, War of the Five Kings |
| `species` | Entity | Non-human biological type (NOT named individuals — those are characters) | habitat, abilities, known_specimens | Dragons (species), Others, Children of the Forest, Giants |
| `title` | Entity | Formal office or hereditary title | holders, succession, powers, created_by | Hand of the King, Lord Commander, High Septon |

### Hierarchy Query Rules

- **Querying a parent returns all children.** "Show me all Organizations" → houses + factions + religions.
- **Querying a leaf returns only that type.** "Show me all Houses" → only houses, not factions.
- **An entity has exactly one type.** The Night's Watch is `organization.faction`, not both faction and religion. If an entity genuinely straddles types, pick the primary and note the secondary in metadata.
- **Characters are individuals, species are categories.** Drogon is `character.dragon`. "Dragons" as a biological category is `species`. Ghost is `character.direwolf`. "Direwolves" as a species is `species`.

---

## Edge Types (Relationship Categories)

Edges connect nodes in the graph. Every edge must have:
- `type` — from the taxonomy below
- `source` / `target` — the two nodes
- `first_available` — spoiler gate
- `evidence` — chapter citation or wiki source
- `confidence` — tier 1-5

### Design Principles

The v1 AGOT extractions organically produced ~127 ad-hoc relationship labels. The wiki infobox fields surface another ~40 structured relationship types. This taxonomy normalizes both into a controlled vocabulary that is **specific enough to be queryable** but **general enough to avoid synonyms** (e.g., one `SERVES` rather than SERVES / SERVED_BY / CLAIMS_TO_SERVE / SWORN_TO all meaning slightly different things).

When an extraction or wiki field doesn't fit an existing edge type, add a new one to this taxonomy rather than forcing a bad fit. Edge types are cheaper than lost information.

**When this taxonomy is used:** This controlled vocabulary is for the **graph layer** (building nodes and edges in `graph/`), the **wiki ingestion pass** (Pass 2), and any **downstream analytical passes**. Pass 1 (mechanical extraction) records relationships in free-text natural language in its Relationships Observed table — it does NOT need to use these labels. The normalization from free-text → controlled vocabulary happens when graph edges are built from extraction outputs.

### Kinship & Family

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `PARENT_OF` | Biological or adoptive parent | Parent → Child | Father, Mother |
| `SIBLING_OF` | Brother/sister (full, half, or step — note which in metadata) | Symmetric | — |
| `SPOUSE_OF` | Married to (note if current, former, or annulled) | Symmetric | Spouse, Spouses |
| `BETROTHED_TO` | Engaged/promised in marriage | Symmetric | — |
| `LOVER_OF` | Romantic/sexual relationship outside marriage | Symmetric | Lover, Lovers |
| `WARD_OF` | Fostered by / raised by (not biological parent) | Ward → Guardian | — |
| `ANCESTOR_OF` | Distant lineage (more than one generation) | Ancestor → Descendant | Dynasty |
| `HEIR_TO` | Designated or expected successor (person → person or person → title) | Heir → Holder | Heir, Heirs |
| `CADET_BRANCH_OF` | Junior house derived from senior house | Cadet → Parent House | Cadet branches |

### Political & Authority

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `RULES` | Holds authority over a location or domain | Ruler → Location | Ruler, Head |
| `OVERLORD_OF` | Feudal superior of a house or lord | Overlord → Vassal | Overlord, Overlords |
| `SWORN_TO` | Feudal allegiance (house-to-house or person-to-house) | Vassal → Lord | Allegiance, Allegiances |
| `COMMANDS` | Military or organizational command | Commander → Subordinate | — |
| `SERVES` | Service relationship (broader than feudal — includes maesters, squires, servants) | Server → Served | — |
| `ADVISES` | Counsel relationship (Hand, maester, septa) | Advisor → Advised | — |
| `HOLDS_TITLE` | Person holds a named office or title | Person → Title | Titles, Title, Office |
| `SUCCEEDS` | Succeeded someone in a role or position | Successor → Predecessor | Successor, Predecessor |
| `CLAIMS` | Asserts right to a title, throne, or domain (may be contested) | Claimant → Claimed | — |
| `APPOINTS` | Grants a position or authority to someone | Appointer → Appointed | — |
| `DEPOSES` | Removes someone from power | Deposer → Deposed | — |

### Factional & Diplomatic

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `MEMBER_OF` | Belongs to a faction, order, or organization | Person → Faction | — |
| `FOUNDED` | Created or established an organization, house, or institution | Founder → Founded | Founder, Founded |
| `ALLIES_WITH` | Alliance (note if temporary, forced, or strategic) | Symmetric | — |
| `OPPOSES` | Active opposition or enmity | Symmetric | — |
| `MANIPULATES` | One party unknowingly used by another | Manipulator → Target | — |
| `BETRAYS` | Broke faith, oath, or alliance | Betrayer → Betrayed | — |
| `NEGOTIATES_WITH` | Diplomatic engagement (may not result in alliance) | Symmetric | — |

### Military & Conflict

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FIGHTS_IN` | Participates in a battle or war | Person → Event/War | — |
| `COMMANDS_IN` | Holds command role in a battle or war (note which side) | Person → Event/War | — |
| `KILLS` | Directly causes death | Killer → Killed | — |
| `EXECUTES` | Formal/judicial killing | Executor → Executed | — |
| `CAPTURES` | Takes prisoner | Captor → Captive | — |
| `PRISONER_OF` | Held captive by | Prisoner → Captor | — |
| `BESIEGES` | Conducts siege of a location | Besieger → Location | — |
| `DEFEATS` | Wins against in battle or conflict | Victor → Defeated | Result |
| `DUELS` | Single combat | Symmetric | — |

### Knowledge & Information

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `KNOWS` | Possesses specific information | Knower → Information/Secret | — |
| `IGNORANT_OF` | Critically lacks information that the reader or other characters have | Person → Information | — |
| `SEEKS` | Pursuing knowledge, artifact, or person | Seeker → Sought | — |
| `REVEALS_TO` | Discloses information to another | Revealer → Recipient (note what was revealed) | — |
| `DECEIVES` | Deliberately misleads | Deceiver → Deceived (note the deception) | — |
| `HOARDS` | Institution or person suppresses knowledge | Hoarder → Knowledge | — |
| `INVESTIGATES` | Actively trying to learn or prove something | Investigator → Subject | — |
| `TEACHES` | Transmits knowledge or skill | Teacher → Student | — |

### Emotional & Perceptual

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `PERCEIVED_AS` | How POV Character X sees Character Y (with characterization notes) | Perceiver → Perceived | — |
| `TRUSTS` | Places confidence in | Truster → Trusted | — |
| `DISTRUSTS` | Lacks confidence in, suspects | Distruster → Distrusted | — |
| `RESPECTS` | Holds in high regard | Respecter → Respected | — |
| `FEARS` | Afraid of (person, faction, or thing) | Fearer → Feared | — |
| `LOVES` | Deep emotional attachment (familial, romantic, or platonic) | Lover → Loved | — |
| `HATES` | Deep enmity or loathing | Hater → Hated | — |
| `MOURNS` | Grieves for (dead person, lost thing) | Mourner → Mourned | — |
| `PROTECTS` | Acts as guardian or defender | Protector → Protected | — |
| `RESENTS` | Harbors bitterness toward | Resenter → Resented | — |

### Spatial & Temporal

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `LOCATED_AT` | Entity at location (with book/chapter timestamp) | Entity → Location | Location, Seat |
| `SEAT_OF` | Primary location of a house or faction | Location → House/Faction | Seat, Seats |
| `TRAVELS_TO` | Movement from one location to another | Traveler → Destination (note origin) | — |
| `BORN_AT` | Birthplace | Person → Location | Born |
| `DIED_AT` | Place of death | Person → Location | Died |
| `BURIED_AT` | Place of burial or interment | Person → Location | Buried |
| `CONTEMPORARY_WITH` | Events happen simultaneously or overlap in time | Symmetric | — |
| `REGION_OF` | Location belongs to a larger geographic region | Location → Region | Region, Regions |

### Possession & Ownership

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `WIELDS` | Currently bears or uses a weapon/artifact | Person → Artifact | — |
| `OWNS` | Possesses (broader than wields — castles, ships, animals) | Owner → Owned | Owner, Owners |
| `ANCESTRAL_WEAPON_OF` | Valyrian steel sword or other hereditary weapon of a house | Weapon → House | Ancestral weapon |
| `FORGED_BY` | Creator of an artifact | Creator → Artifact | — |

### Identity & Disguise

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `ALIAS_OF` | Known by another name | Alias → True Identity | Alias, Aliases |
| `DISGUISED_AS` | Actively pretending to be someone/something else | Person → Disguise Identity | — |
| `SAME_AS` | Two references that resolve to the same entity (for cross-identity matching) | Symmetric | — |
| `IMPERSONATES` | Pretending to be a specific other person | Impersonator → Impersonated | — |

### Cultural & Religious

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CULTURE_OF` | Person belongs to a cultural group | Person → Culture | Culture, Race |
| `WORSHIPS` | Follows or serves a deity/religion | Person → Religion | Religion |
| `SACRED_TO` | Location or artifact is holy to a religion | Entity → Religion | — |
| `CLERGY_OF` | Serves as religious official | Person → Religion | — |

### Narrative & Literary

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FORESHADOWS` | Detail A is a Chekhov's gun for Event B | Detail → Event | — |
| `PARALLELS` | Event/character A mirrors Event/character B thematically | Symmetric | — |
| `SUBVERTS` | Event A inverts the expectation set by B | Subverter → Subverted | — |
| `ECHOES` | Weaker than PARALLELS — structural or verbal similarity without full thematic mirroring | Echo → Source | — |
| `CONTRASTS` | Deliberate opposition in characterization, situation, or outcome | Symmetric | — |

### Prophecy

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FULFILLS` | Event fulfills prophecy (confirmed) | Event → Prophecy | — |
| `APPEARS_TO_FULFILL` | Possible fulfillment, may be red herring | Event → Prophecy | — |
| `SUBVERTS_PROPHECY` | Contradicts expected fulfillment | Event → Prophecy | — |
| `PROPHESIED_BY` | Who made the prophecy | Prophecy → Prophet | — |
| `SUBJECT_OF_PROPHECY` | Person/event the prophecy is about | Person → Prophecy | — |

### Evidentiary (Theory Support)

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `SUPPORTS` | Textual passage supports a theory | Evidence → Theory | — |
| `CONTRADICTS` | Textual passage undermines a theory | Evidence → Theory | — |
| `CITED_BY` | Theory attributed to source theorist or community | Theory → Source | — |

### Causal & Plot

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CAUSES` | Event A leads to Event B | Cause → Effect | — |
| `PREVENTS` | Action A blocks Event B | Preventer → Prevented | — |
| `ENABLES` | Condition A makes Event B possible | Enabler → Enabled | — |
| `MOTIVATES` | Event or condition drives a character's actions | Motivation → Actor | — |
| `TRIGGERS` | Immediate cause (narrower than CAUSES — the specific spark) | Trigger → Result | — |

### Hospitality & Custom

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `GUEST_OF` | Under someone's roof / protection by custom | Guest → Host | — |
| `VIOLATES_GUEST_RIGHT` | Broke the sacred hospitality compact | Violator → Victim | — |
| `GRANTS_SAFE_CONDUCT` | Promised safe passage | Grantor → Recipient | — |

---

## Edge Metadata

Every edge instance should carry these fields where applicable:

| Field | Purpose | Example |
|-------|---------|---------|
| `type` | Edge type from taxonomy above | `KILLS` |
| `source` | Source node | `jaime-lannister` |
| `target` | Target node | `aerys-ii-targaryen` |
| `first_available` | Spoiler gate — earliest book/chapter where this is known | `AGOT Jaime I` |
| `confidence` | Tier 1-5 | `1` |
| `evidence` | Chapter citation or wiki URL | `AGOT Eddard XV` |
| `notes` | Qualifiers, context, temporal bounds | `"while serving as Kingsguard"` |
| `temporal` | When this edge is active (if not permanent) | `"until ASOS"`, `"during Robert's Rebellion"` |
| `symmetric` | Whether the edge is bidirectional | `true` / `false` |

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
- `first_available: pre-agot` (D&E novellas and pre-series information)

The system can filter all content to a user-declared spoiler ceiling. Any node with `first_available` above the ceiling is excluded from retrieval.

**Retroactive significance:** Some information has retroactive importance. A fact available in AGOT may only become meaningful in ADWD. Use `significance_unlocked` as a secondary field:
- `first_available: AGOT Eddard I` / `significance_unlocked: ADWD` (Ned's internal guilt about Jon)

### Wiki Data Source for Spoiler Gates

The AWOIAF wiki provides two structured sources for auto-populating `first_available`:

**1. Infobox "Books" field** (book-level granularity):
```html
<li><a href="...">A Game of Thrones</a> <small>(POV)</small></li>
<li><a href="...">A Clash of Kings</a> <small>(mentioned)</small></li>
```
Appearance types: `POV` (has point-of-view chapters), `appears` (present in narrative), `mentioned` (referenced only). The first book where the entity is NOT just "mentioned" is the book-level `first_available`.

**2. Citation anchor IDs** (chapter-level granularity):
Wiki footnotes encode book and chapter number directly in their `cite_ref` / `cite_note` HTML anchor IDs:
```
cite_ref-Ragot2...   → AGOT chapter 2
cite_ref-Rasos24...  → ASOS chapter 24
cite_ref-Radwd62...  → ADWD chapter 62
```
Format: `R{book_abbrev}{chapter_number}`. The **lowest-numbered citation** for a given entity gives us chapter-level `first_available`. Example: Eddard Stark's wiki page has 78 unique chapter citations across all 5 books — the first is `agot1` (AGOT chapter 1), giving `first_available: AGOT Bran I`.

5,279 of 17,657 cached wiki pages have infoboxes. Citation anchors appear across an even wider set of pages. A parser script should extract both and cross-reference to produce the most precise `first_available` possible.

---

## Pass 1 Extraction Schema (v2)

Each mechanical extraction produces a `.extraction.md` file with these sections:

| Section | Purpose |
|---------|---------|
| Chapter Metadata | Book, chapter number, POV, spoiler gate, locations, timeline, `time_markers` |
| Physical Environment | Weather, season, time of day, lighting, sounds, smells, sensory details |
| Characters Present | Who appears in the chapter with role and notes |
| Character Appearances | Physical descriptions as given in this chapter: hair, eyes, build, scars, clothing, weapons, age |
| Characters Referenced | Who is mentioned but not present |
| Locations | Location routing table (name, role, first appearance) |
| Location Descriptions | Defensive features, architecture, interiors, scale, condition, terrain, sensory details |
| Artifacts & Objects | Objects of narrative significance |
| Food & Drink | All meals/food described: dishes, ingredients, who eats with whom, preparation |
| Hospitality & Guest Right | Guest right invocations, bread and salt, shelter, violations |
| Events & Actions | Numbered sequence of chapter events |
| Spatial Layout & Movement | Phase-based positioning table (Opening, Advance, Ambush, Assembly, etc.) |
| Information Revealed | What the reader/characters learn, with knowledge asymmetry tracking |
| Dialogue of Note | Key quotes with speaker, listener, context |
| POV Internal State | Emotional state, preoccupations, decisions, self-deception |
| Relationships Observed | Character-to-character relationships with evidence |
| Unanswered Questions | Open questions raised by the chapter |
| Raw Entity List | Flat index across 10 categories: Characters, Locations, Houses, Factions & Organizations, Religions & Faiths, Cultures & Peoples, Artifacts & Objects, In-world Texts & Songs, Magic & Phenomena, Wars & Conflicts, Titles & Offices |

Full schema definition and extraction rules: `.claude/agents/mechanical-extractor.md`

---

## Agent Conventions

All agents working in this project should:

1. **Load this file first** — understand the data model before doing anything
2. **Follow the file naming conventions** — consistency is critical
3. **Tag every output with confidence tiers** — nothing goes untiered
4. **Include `first_available` on every node and edge** — spoiler gating is architectural, not optional
5. **Output structured markdown** — follow the schemas defined in each agent prompt file
6. **Propose, don't decide** — analytical findings go to the curation queue as candidates, not as accepted facts
7. **Cite chapter sources** — every claim traces back to a specific chapter or wiki page
8. **Direwolves and dragons are characters** — Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, Viserion are characters with agency and narrative arcs, not creatures or fauna
9. **Edge taxonomy is for the graph layer, not Pass 1** — Pass 1 (mechanical extraction) records relationships in free-text natural language. Pass 2+, wiki ingestion, and graph-building use the controlled edge vocabulary from this file. If you're building graph edges and no type fits, flag it for taxonomy expansion rather than inventing ad-hoc labels

---

## Wiki Infobox Fields → Edge Type Mapping

When Pass 2 (wiki ingestion) processes wiki pages, these infobox fields map to edge types:

| Wiki Infobox Field | Edge Type | Notes |
|-------------------|-----------|-------|
| Father, Mother | `PARENT_OF` | Reverse direction (wiki lists parent on child's page) |
| Spouse, Spouses | `SPOUSE_OF` | |
| Lover, Lovers | `LOVER_OF` | |
| Issue | `PARENT_OF` | Forward direction (wiki lists children on parent's page) |
| Allegiance, Allegiances | `SWORN_TO` | |
| Overlord, Overlords | `OVERLORD_OF` | Reverse direction |
| Culture | `CULTURE_OF` | |
| Religion | `WORSHIPS` | For characters; `RELIGION_OF` for locations |
| Seat, Seats | `SEAT_OF` | |
| Head | `RULES` | House head rules the house |
| Heir, Heirs | `HEIR_TO` | |
| Founder | `FOUNDED` | |
| Successor | `SUCCEEDS` | |
| Predecessor | `SUCCEEDS` | Reverse direction |
| Ancestral weapon | `ANCESTRAL_WEAPON_OF` | |
| Cadet branches | `CADET_BRANCH_OF` | |
| Owner, Owners | `OWNS` | For animals, ships, etc. |
| Monarch | `SWORN_TO` or `SERVES` | Context-dependent |
| Born | `BORN_AT` | If location extractable |
| Died | `DIED_AT` | If location extractable |
| Buried | `BURIED_AT` | |
| Alias, Aliases | `ALIAS_OF` | |
| Ruler | `RULES` | |
| Region, Regions | `REGION_OF` | |
| Species | Node type metadata | Not an edge — informs entity type |
| Conflict | `FIGHTS_IN` | For battle pages |
| Result | `DEFEATS` | Extract victor/defeated from result text |
