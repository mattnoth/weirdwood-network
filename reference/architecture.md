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

This hierarchy is **extensible**. New leaf types can be added without restructuring; new intermediate types should be rare and require design review.

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
│   ├── War               (multi-battle conflict: Robert's Rebellion, War of the Five Kings)
│   └── Tournament        (formal tourney: Tourney at Harrenhal, Hand's Tourney, Ashford Tourney)
├── Species               (biological type, NOT individual: dragons-as-species, Others, Children of the Forest)
├── Title                 (formal office: Hand of the King, Lord Commander, High Septon)
└── Meta                  (out-of-universe constructs — chapters, novels, publication metadata)
    ├── Chapter           (a chapter of a published novel: AGOT Chapter 1, ASOS Chapter 71)
    └── (future)          (Book, PovArc — added when needed)
```

**Meta vs in-world** — Meta entities are out-of-universe (they describe the books *about* the world, not things *in* the world). They are categorically distinct from Event entities (Red Wedding, Battle of the Blackwater), which are in-world happenings. A `meta.chapter` node represents the literary container; the in-world events that happen *within* a chapter remain their own `event.battle/war/tournament` nodes. Edges from in-world entities to `meta.chapter` nodes are *citation/provenance* edges (this entity is featured in / discussed in this chapter), not in-world relationships.

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
| `concept.language` | Concept | Spoken or written in-world language | speakers, regions, script, status | Common Tongue, High Valyrian, Old Tongue, Dothraki, Skroth |
| `concept.medical` | Concept | Disease, poison, treatment, or medical condition | effects, regions, treatment, mortality | Greyscale, the bloody flux, the strangler, milk of the poppy |
| `concept.custom` | Concept | Cultural practice, tradition, or ceremony (NOT ethnic group — that's concept.culture) | regions, cultures, status_in_law | Bedding, Guest right, Fosterage, Heraldry, Dowry, Kingsmoot |
| `object.artifact` | Object | Object of narrative significance | material, current_holder, history | Ice, Dragonbinder, Dawn, glass candles |
| `object.text` | Object | In-world book, document, or song | author, subject, location | The Jade Compendium, The Rains of Castamere |
| `object.food` | Object | In-world food or drink (hospitality/feast/guest-right artifacts) | regions, ingredients, culture | Bowl of brown, lemon cakes, Arbor gold, dreamwine |
| `object.material` | Object | Raw material, mineral, or substance (NOT a named artifact — that's object.artifact) | composition, regions, uses, rarity | Dragonglass, dragonbone, Valyrian steel (as substance), gold, salt |
| `event.battle` | Event | Single engagement or plot event | location, date, participants, outcome | Red Wedding, Battle of the Blackwater |
| `event.war` | Event | Multi-battle named conflict | belligerents, causes, phases, battles, outcome | Robert's Rebellion, War of the Five Kings |
| `event.tournament` | Event | Formal tourney or melee with named participants | location, date, host, champions, participants | Tourney at Harrenhal, Hand's Tourney, Ashford Tourney |
| `species` | Entity | Non-human biological type — sentient species, magical creatures, in-world flora kinds, AND in-world fauna kinds (NOT named individuals — those are characters) | habitat, abilities, known_specimens | Dragons (species), Others, Children of the Forest, Giants, weirwood, ironwood, direwolves, aurochs |
| `title` | Entity | Formal office or hereditary title | holders, succession, powers, created_by | Hand of the King, Lord Commander, High Septon |
| `meta.chapter` | Meta | A chapter of a published ASOIAF novel — out-of-universe literary container (NOT an in-world event; the in-world events that occur within the chapter remain their own `event.*` nodes) | book, chapter_number, pov_character, wiki_source | A Game of Thrones-Chapter 1, A Storm of Swords-Chapter 71 |

### Hierarchy Query Rules

- **Querying a parent returns all children.** "Show me all Organizations" → houses + factions + religions.
- **Querying a leaf returns only that type.** "Show me all Houses" → only houses, not factions.
- **An entity has exactly one type.** The Night's Watch is `organization.faction`, not both faction and religion. If an entity genuinely straddles types, pick the primary and note the secondary in metadata.
- **Characters are individuals, species are categories.** Drogon is `character.dragon`. "Dragons" as a biological category is `species`. Ghost is `character.direwolf`. "Direwolves" as a species is `species`.

### Multi-type entities

Some real-world entities span multiple of the type categories above. Free Folk are simultaneously a culture (`concept.culture`) and a polity/faction (`organization.faction`). Children of the Forest are simultaneously a species (`species`) and an ancient sentient faction. Wardens are titles, but the *role* of being a warden is also a behavior set.

**Policy: one node per real-world entity. The `type` field captures its primary identity. Other facets emerge through edges, not through a second node.**

- Free Folk → `concept.culture`. Polity-ness emerges via MEMBER_OF (character → free-folk), FIGHTS_IN (war/battle → free-folk), HOLDS_TITLE (king-beyond-the-wall), LOCATED_AT (beyond-the-wall → free-folk).
- Children of the Forest → `species`. Faction-ness emerges via FIGHTS_IN (war-of-first-men), LOCATED_AT (isle-of-faces), and magic-use edges.

This avoids SAME_AS bookkeeping and ambiguous "which node?" queries. Retrieval naturally unions identity + behaviors via edge traversal.

**The `multi-type-entity-resolver` agent's job** under this policy: pick the right primary type + ensure edges capture the other facets. NOT split into multiple nodes.

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
| `WARD_OF` | Fostered by / raised by (not biological parent). Reverse-direction `FOSTERED_BY` (Guardian → Ward) is permitted and semantically equivalent — same pattern as HELD_BY for HOLDS_TITLE. | Ward → Guardian | — |
| `ANCESTOR_OF` | Distant lineage (more than one generation) | Ancestor → Descendant | Dynasty |
| `HEIR_TO` | Designated or expected successor (person → person or person → title) | Heir → Holder | Heir, Heirs |
| `CADET_BRANCH_OF` | Junior house derived from senior house | Cadet → Parent House | Cadet branches |
| `MARRIES_OFF` | Parent / overlord / king arranges a marriage for another person — distinct from `SPOUSE_OF` (the marriage itself); captures the arranger's agency as a political instrument | Arranger → Married-off person | — |
| `UNCLE_OF` | One-generation kinship shortcut: parent's sibling. Captures uncle/aunt without forcing two-hop traversal through the missing/inferred parent. Use when prose explicitly says "his uncle X" / "her aunt Y". | Uncle/Aunt → Nephew/Niece | — |
| `NEPHEW_OF` | Reverse of `UNCLE_OF` — emitted on the nephew/niece node pointing to the uncle/aunt. Same one-hop kinship shortcut. | Nephew/Niece → Uncle/Aunt | — |
| `COUSIN_OF` | Symmetric kinship shortcut for cousins (children of siblings). Captures first/second/etc. cousins without traversing two PARENT_OF + one SIBLING_OF. Use when prose explicitly says "his cousin X" / "her cousin Y". Especially common in Frey, Lannister, Tully, Tyrell, Targaryen families. | Symmetric | — |
| `MILK_BROTHER_OF` | Symmetric kinship: characters who shared a wet-nurse. Real Westerosi cultural category (Edric Dayne and Jon Snow, Robert Baratheon and Ned Stark per fostering customs). Distinct from SIBLING_OF (no blood) and FOSTERED_BY (institutional). | Symmetric | — |
| `NURSED_BY` | Child was wet-nursed by this person. Reverse is `WET_NURSE_OF`. Distinct from PARENT_OF; captures the lifelong attachment ASOIAF treats as significant (Wylla nursing Edric, Catelyn re Jon's nurse, etc.). | Child → Nurse | — |
| `WET_NURSE_OF` | Reverse of NURSED_BY — emitted on the nurse's node pointing to the child she nursed. | Nurse → Child | — |

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
| `HELD_BY` | Reverse of `HOLDS_TITLE` — emitted on title nodes pointing to the people/houses who have held the title | Title → Person/House | — |
| `SUCCEEDS` | Succeeded someone in a role or position | Successor → Predecessor | Successor, Predecessor |
| `CLAIMS` | Asserts right to a title, throne, or domain (may be contested) | Claimant → Claimed | — |
| `APPOINTS` | Grants a position or authority to someone | Appointer → Appointed | — |
| `DEPOSES` | Removes someone from power | Deposer → Deposed | — |
| `VOWS_TO` | Personal named oath made to another (distinct from `SWORN_TO`, which is structural feudal allegiance) — e.g., Brienne's vow to Catelyn, Jaime's vow to Catelyn, Arya's prayer list | Vow-maker → Recipient | — |
| `BREAKS_VOW` | Breaking of a personal vow or sworn oath — paired with `VOWS_TO` / `SWORN_TO` to track oath-keeping arcs (Jaime breaking Kingsguard oath by killing Aerys; Theon breaking foster-bond to Robb; etc.) | Vow-breaker → Vow-recipient | — |

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
| `PART_OF` | Battle or sub-event is a component of a larger war | Battle → War | Conflict, Battles |
| `KILLS` | Directly causes death | Killer → Killed | — |
| `KILLED_BY` | Reverse of `KILLS` — emitted on victim nodes pointing to killer | Killed → Killer | — |
| `EXECUTES` | Formal/judicial killing | Executor → Executed | — |
| `CAPTURES` | Takes prisoner | Captor → Captive | — |
| `PRISONER_OF` | Held captive by | Prisoner → Captor | — |
| `BESIEGES` | Conducts siege of a location | Besieger → Location | — |
| `DEFEATS` | Wins against in battle or conflict | Victor → Defeated | Result |
| `DUELS` | Single combat | Symmetric | — |
| `POISONS` | Killing or attempted-killing via poison — narrower than `KILLS` because method matters narratively (whodunnit plots, named poisons like the strangler, tears of Lys) | Poisoner → Poisoned | — |
| `RANSOMS` | Pays or negotiates for a captive's release — distinct from `CAPTURES` (the taking) and `PRISONER_OF` (the state) | Ransomer → Captive | — |
| `IMPRISONS` | Holds a captive in named confinement (cell, dungeon, tower) — distinct from `CAPTURES` (battlefield event) and `PRISONER_OF` (the captive's state); captures the institutional/judicial act of confinement, e.g., Cersei imprisoning Tyrion in the Red Keep after Joffrey's death (he was already at court, not captured) | Imprisoner → Imprisoned | — |
| `KILLED_WITH` | Combat death attributed to a specific named artifact — mirror of `EXECUTED_WITH` for non-judicial battlefield deaths. Use when prose names the weapon as agent of death ("slain by Orphan-Maker", "took an arrow from Ice"). Coexists with `KILLED_BY person` — the person did the killing, the artifact was the instrument. | Victim → Artifact | — |
| `KNIGHTED_BY` | Granted knighthood by another knight or lord. Distinct from `TUTORS` (skill transfer over time) and `APPOINTS` (political office). Use when prose explicitly describes the dubbing/knighting. | Knight → Dubber | — |
| `BESTOWS_KNIGHTHOOD_ON` | Reverse of `KNIGHTED_BY` — emitted on the dubber's node. | Dubber → Knight | — |

### Knowledge & Information

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `KNOWS` | Possesses specific information | Knower → Information/Secret | — |
| `IGNORANT_OF` | Critically lacks information that the reader or other characters have | Person → Information | — |
| `SEEKS` | Pursuing knowledge, artifact, or person | Seeker → Sought | — |
| `REVEALS_TO` | Discloses information to another | Revealer → Recipient (note what was revealed) | — |
| `DECEIVES` | Deliberately misleads | Deceiver → Deceived (note the deception) | — |
| `DECEIVED_BY` | Reverse of `DECEIVES` — emitted on target nodes pointing to deceiver | Deceived → Deceiver | — |
| `HOARDS` | Institution or person suppresses knowledge | Hoarder → Knowledge | — |
| `INVESTIGATES` | Actively trying to learn or prove something | Investigator → Subject | — |
| `TEACHES` | Transmits knowledge or skill (general/casual instruction) | Teacher → Student | — |
| `TUTORS` | Sustained formal one-on-one mentorship — narrower than `TEACHES` (Syrio→Arya water-dancing, Cressen→Stannis childhood, Aemon→Sam ravenry, Septa Mordane→Sansa) | Tutor → Student | — |
| `HEALS` | Medical or maester treatment — restoration of body, not resurrection of the dead (which is `RESURRECTS`). Maester Luwin healing Bran after the fall; Aemon healing Sam; the unnamed septon healing Sandor. **Excludes:** Red Priests reviving the dead (use `RESURRECTS`); Qyburn's reanimation of the Mountain (use `RESURRECTS`) | Healer → Healed | — |

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
| `LOCATED_AT` | Entity at location (with book/chapter timestamp). Covers both event-at-place (battle location) and person-at-place (witness location). Deprecated synonym `LOCATED_IN` was emitted by an early parser variant; normalize on read. | Entity → Location | Location, Seat |
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
| `WIELDS` | Currently bears or uses a weapon/artifact. **Target MUST be `object.artifact`** — animals (mounts, ravens, dragons) use `OWNS` or `BONDED_TO`, never `WIELDS`. | Person → Artifact | — |
| `OWNS` | Possesses (broader than wields — castles, ships, animals) | Owner → Owned | Owner, Owners |
| `ANCESTRAL_WEAPON_OF` | Valyrian steel sword or other hereditary weapon of a house | Weapon → House | Ancestral weapon |
| `FORGED_BY` | Creator/smith of an artifact (the person/group who made it). **NOT for material composition** — use `MADE_OF` for substance/material relationships. | Creator → Artifact | — |
| `MADE_OF` | Artifact is composed of a material (Valyrian steel, dragonglass, dragonbone, weirwood, etc.). Distinct from `FORGED_BY` (smith). | Artifact → Material (`object.material`) | — |
| `LOOTED_BY` | Artifact taken by force or conquest from prior holder. Distinct from `OWNS` (steady state). Captures the transactional moment. | Artifact → New holder | — |
| `REFORGED_INTO` | Original artifact materially transformed into a new artifact (or multiple). The original ceases to exist; the new artifact(s) inherit material and lineage. | Original artifact → Resulting artifact | — |
| `GIFTED_TO` | Deliberate voluntary transfer of an artifact from one person to another as gift or honor. Distinct from `OWNS` (state) and `INHERITED_BY` (death-succession). Note giver in qualifier. | Artifact → Recipient | — |
| `INHERITED_BY` | Artifact passed via inheritance from deceased holder to heir. | Artifact → Heir | — |
| `WIELDED_IN` | Artifact was used in a named event (battle, execution, ritual). Distinct from `WIELDS` (person → artifact possession state). Enables artifact-history queries. | Artifact → Event | — |
| `EXECUTED_WITH` | A specific person was executed with a specific weapon (poetic-detail edges: Eddard executed with Ice, etc.). May overlap with `WIELDED_IN` + `EXECUTES`; kept distinct for narrative-precision queries. | Victim → Weapon | — |

### Identity & Disguise

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `ALIAS_OF` | Known by another name | Alias → True Identity | Alias, Aliases |
| `DISGUISED_AS` | Actively pretending to be someone/something else | Person → Disguise Identity | — |
| `SAME_AS` | Two references that resolve to the same entity (for cross-identity matching) | Symmetric | — |
| `IMPERSONATES` | Pretending to be a specific other person | Impersonator → Impersonated | — |

### Magic & Supernatural

> These edges capture relationships that involve magical, ritual, or supernatural agency — distinct from in-world physical relations. ASOIAF has rich magical systems (warging, R'hllor blood magic, Faceless-Men identity-transfer, weirwood-bonding, dragon-bonding, resurrection, curse-laying) that infobox extraction cannot reach. These types are *prose-derived only* — the wiki-infobox parser does not emit them.

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `WARGS_INTO` | A warg / skinchanger actively occupies the consciousness of an animal or person — e.g., Bran into Summer / Hodor / the heart tree; Arya into Nymeria (dream-skinchange); Varamyr into his wolf / eagle / shadowcat; Orell into his eagle; Jon (low-key) into Ghost | Warg → Vessel | — |
| `BONDED_TO` | Static magical bond between two beings — broader and more permanent than `WARGS_INTO` (which is the active occupation moment). Covers dragon-rider bonds (Daenerys ↔ Drogon, etc.), warg-animal lifelong pairing (Bran ↔ Summer when not actively warging), weirwood-bond (Bran ↔ his three-eyed-crow / weirwood network) | Symmetric | — |
| `SACRIFICES` | Deliberate ritual or magical killing with supernatural/symbolic purpose — distinct from `KILLS` (combat) and `EXECUTES` (judicial). Mirri Maz Duur sacrificing Drogo's life-essence; Daenerys sacrificing her unborn child to magic the dragon eggs; Stannis (via Melisandre) sacrificing Edric Storm's leech-blood / Mance / Penny's brother / (theory-tier) Shireen; Craster sacrificing his sons to the Others | Sacrificer → Victim | — |
| `RESURRECTS` | Returns the dead to life via supernatural means — distinct from `HEALS` (medical), distinct from `KILLED_BY` (semantic reverse). Thoros of Myr resurrects Beric Dondarrion (multiple times); Beric resurrects Catelyn → Lady Stoneheart (ASOS Epilogue); Coldhands resurrected by unknown force (Children?); Patchface drowned-and-returned; Qyburn reanimates the Mountain; Red Priests broadly perform this (Thoros, Moqorro) — `HEALS` is for body-restoration, `RESURRECTS` is for death-reversal | Resurrector → Resurrected | — |
| `CURSES` | A character or magical force lays a curse — Mirri Maz Duur's "when the sun rises in the west" curse on Daenerys; Maggy the Frog's Valonqar prophecy-curse on Cersei; the Curse of Harrenhal (collective); Night's King lore | Curser → Cursed | — |

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
| `DEPICTED_IN` | Character is the subject of an in-world text/song/ballad/tale (Danny Flint → "Brave Danny Flint" song, Florian → Florian-and-Jonquil tales). Distinct from `WRITTEN_BY` (author → work). Captures the in-universe legacy/folklore layer. | Character → Text | — |

*continued:*

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FORESHADOWS` | Detail A is a Chekhov's gun for Event B | Detail → Event | — |
| `PARALLELS` | Event/character A mirrors Event/character B thematically | Symmetric | — |
| `SUBVERTS` | Event A inverts the expectation set by B | Subverter → Subverted | — |
| `ECHOES` | Weaker than PARALLELS — structural or verbal similarity without full thematic mirroring | Echo → Source | — |
| `CONTRASTS` | Deliberate opposition in characterization, situation, or outcome | Symmetric | — |
| `WRITTEN_BY` | Authorship of an in-world text (book, song, decree, letter) | Text → Author | Written by |

### Prophecy

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FULFILLS` | Event fulfills prophecy (confirmed) | Event → Prophecy | — |
| `APPEARS_TO_FULFILL` | Possible fulfillment, may be red herring | Event → Prophecy | — |
| `SUBVERTS_PROPHECY` | Contradicts expected fulfillment | Event → Prophecy | — |
| `PROPHESIED_BY` | Who made the prophecy | Prophecy → Prophet | — |
| `SUBJECT_OF_PROPHECY` | Person/event the prophecy is about | Person → Prophecy | — |
| `DREAMS_OF` | In-world prophetic or significant dream/vision about a person, place, event, or symbol. Distinct from `FORESHADOWS` (which is a reader-facing narrative-craft edge); `DREAMS_OF` is character-facing. Heavily concentrated in Bran (greendreams, three-eyed-crow), Daenerys (HotU visions), Jojen, and the Targaryen line (canonical prophetic-dreaming lineage) | Dreamer → Subject | — |

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
| `ATTENDS` | Person present at a named event as guest, witness, or audience — not as combatant (`FIGHTS_IN`), commander (`COMMANDS_IN`), or organizer. Use for tourney spectators, wedding guests, feast attendees, court hearings. | Person → Event | — |

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

## Spoiler Gating — DEFERRED to Post-First-Release

> **Status (2026-04-27):** Spoiler gating via `first_available` is **deferred** to a post-first-release backfill pass. The field is **optional** in v1 nodes. Existing values may be missing, in inconsistent shapes, or wrong (the wiki-infobox-parser produces systematically wrong values for some page classes — e.g., Tyrion and Varys both got `ADWD` despite appearing from AGOT). **Do not invest context reasoning out individual values during extraction or curation work.** Backfill will happen via a deterministic script after the first release, when the data model is stable enough to enforce consistently.
>
> When backfill runs, it will use the wiki data sources documented below to derive `first_available` mechanically across the entire node corpus in one pass, rather than relying on per-node agent judgment.

### Format (when re-introduced)

`{BOOK} {POV} {CHAPTER_NUMBER}` or `{BOOK} Prologue/Epilogue`

Examples:
- `first_available: AGOT Bran II` (Bran's fall — available from this chapter onward)
- `first_available: ASOS Epilogue` (Lady Stoneheart reveal)
- `first_available: pre-agot` (D&E novellas and pre-series information)

The system will filter content to a user-declared spoiler ceiling. Any node with `first_available` above the ceiling is excluded from retrieval. **This filtering is not active in v1.**

**Retroactive significance:** Some information has retroactive importance. A fact available in AGOT may only become meaningful in ADWD. Use `significance_unlocked` as a secondary field:
- `first_available: AGOT Eddard I` / `significance_unlocked: ADWD` (Ned's internal guilt about Jon)

### Wiki Data Source for Future Backfill

The AWOIAF wiki provides two structured sources for the eventual backfill script:

**1. Infobox "Books" field** (book-level granularity):
```html
<li><a href="...">A Game of Thrones</a> <small>(POV)</small></li>
<li><a href="...">A Clash of Kings</a> <small>(mentioned)</small></li>
```
Appearance types: `POV`, `appears`, `mentioned`. First non-"mentioned" book → book-level `first_available`.

**2. Citation anchor IDs** (chapter-level granularity):
Format: `R{book_abbrev}{chapter_number}` in cite_ref HTML anchors. Example: `cite_ref-Ragot2` → AGOT chapter 2. Lowest-numbered citation per page → chapter-level `first_available`.

**Known parser-bug class:** the lowest-cite_ref heuristic produces wrong values for some pages (cite_refs are reordered when wiki footnotes are edited; ADWD-era references can sort first). The backfill script must cross-reference cite_refs against `pass1_mentions` to detect and correct these silent failures, OR simply use `Books` field as the primary signal and treat cite_refs as refinement only.

**Coverage at v1:** 5,279 of 17,657 cached wiki pages have infoboxes. The Track B parser populated `first_available` for 2,888 of those (54.7%) — values not yet validated.

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

## Artifact Formats by Consumer

> **Principle:** Markdown for things that become node content. Structured (JSONL/JSON) for things consumed by code. Don't force one format across all artifact types.
>
> Wiki Pass 2 produces a per-page family of intermediate artifacts at `working/wiki/pass2-buckets/<bucket_id>/<artifact-dir>/<slug>.<ext>`. Each artifact has exactly one writer (single-writer-per-file invariant). The launcher's promotion step is the only process that combines them into the final node.

| Artifact | Format | Producer | Format choice why |
|----------|--------|----------|-------------------|
| `skeleton/<slug>.node.md` | markdown | Python emitter (`scripts/wiki-pass2-emit-deterministic.py`) | becomes the head of the final node — frontmatter + thin Identity + full Edges from infobox |
| `prose/<slug>.prose.md` | markdown | Python extractor (`scripts/wiki-pass2-extract-prose.py`) | concatenated onto skeleton at promotion — narrative body sections from wiki HTML |
| `prose-edges/<slug>.edges.jsonl` | JSONL | Stage 4 agent (future) | structured rows `{source, edge_type, target, qualifier, citation}` consumed by graph build, not by readers |
| `entity-index/<slug>.index.json` | JSON | post-promotion script (future) | trigger-table input — alias/title/name → slug lookup for Pass 3+ extractions |

**Promotion rule:** the launcher concatenates `skeleton/<slug>.node.md + "\n" + prose/<slug>.prose.md` (when prose exists) and atomic-renames into `graph/nodes/<type>/<slug>.node.md`. Tier-B pages with no prose file get the skeleton verbatim. Stage 4 + entity-index artifacts attach later via separate promotion steps.

**Investigation tooling:** `scripts/graph-query.py <slug>` — read-only CLI that prints a node's frontmatter, outbound edges (with target-resolution status: OK / ALIAS→ / ORPHAN), and top inbound references from `working/wiki/data/cross-references.jsonl`. Use this before grepping raw markdown when investigating any single node. Modes: default full, `--edges-only`, `--inbound-only`, `--json`.

**Why single-writer-per-file matters:** if two processes (e.g., Python skeleton emitter + LLM prose-fill agent) both wrote to the same file, the LLM's tendency to paraphrase or normalize would corrupt the deterministic prefix. Separating artifacts by writer makes that class of failure structurally impossible. A validator never has to enforce byte-equality; the concatenation is the only path that produces the final node.

---

## Wiki Infobox Fields → Edge Type Mapping

> **Vocabulary lock — read this before adding or renaming any edge type.**
>
> **There are two related vocabularies in this document, and it matters which one you mean.**
>
> 1. **Master edge vocabulary** — the union of all subsections under `## Edge Types (Relationship Categories)` above. Currently **~132 distinct edge types** across 15 categories (kinship, political, factional, military, knowledge, emotional/perceptual, spatial, possession, identity, cultural, narrative, prophecy, evidentiary, causal, hospitality, magic-and-supernatural). For an authoritative live count, run `scripts/build-edge-type-counts.py` — its `canonical_type_count` is derived from this file. Session 54 (2026-05-15) added `UNCLE_OF`, `NEPHEW_OF`, `KILLED_WITH`, `ATTENDS` after Stage 4 batch-0012 vocab-gap audit. Session 55 (2026-05-16) added `COUSIN_OF`, `MILK_BROTHER_OF`, `NURSED_BY`, `WET_NURSE_OF`, `KNIGHTED_BY`, `BESTOWS_KNIGHTHOOD_ON`, `DEPICTED_IN` after Stage 4 batches 0012-0018 surfaced these recurring patterns. Some types (`FEARS`, `MOURNS`, `IMPERSONATES`, `FORESHADOWS`, `DREAMS_OF`, `WARGS_INTO`, `RESURRECTS`, `MADE_OF`, `LOOTED_BY`, `GIFTED_TO`, etc.) are pre-declared for prose-derived passes and currently have zero instances in the graph — that's expected; they're reserved for Stage 4 classification. This vocabulary is the **single source of truth for every emitter** — Python parsers, Pass-1 mechanical extractor, prose-edge-classifier, voice-analyzer, foreshadowing-scanner, every script, every agent.
> 2. **Wiki infobox subset** — the table below, mapping wiki infobox FIELD names to edge types. Currently **26 distinct edge types**, all of which are also in the master vocabulary. The parser at `scripts/wiki-infobox-parser.py` (`FIELD_EDGE_MAP` dict) implements only this subset, because infobox fields are the only signal it sees. Prose-derived edges are NOT restricted to this subset — they may emit any of the master vocabulary types (including the new Magic & Supernatural subsection added Session 53).
>
> **Why locked:** the graph's value comes from being able to traverse `SPOUSE_OF` everywhere consistently. If one source emits `SPOUSE_OF` and another emits `MARRIED_TO`, traversal breaks. The master edge types were chosen deliberately (curated from infobox-field frequencies + narrative/perception/prophecy needs for later passes, with Magic & Supernatural added Session 53 ahead of Stage 4); expanding the set requires the same deliberation — propose via `curation/edge-vocabulary-candidates.md`, get approval, then update this file + parser + classifier prompt.
>
> **No emitter invents edge types.** Scripts and agents emit ONLY from the master vocabulary. If a prose passage describes a relationship that doesn't fit any of the ~125, the agent files a `vocabulary-gap` question to `working/wiki/pass2-buckets/questions-for-matt.jsonl` with ≥3 example sentences — it does not invent. Matt + orchestrator decide whether to expand.
>
> **Adding a new edge type:** append a row to the appropriate `## Edge Types` subsection FIRST. If the new type comes from a wiki infobox field, also add the field → edge_type mapping to `FIELD_EDGE_MAP` in `scripts/wiki-infobox-parser.py` and add a row to the wiki-infobox subset table below. Then re-run the affected emitter. Don't shortcut the order.
>
> **Reverse-direction emissions** (e.g., `HELD_BY` on a title node pointing back to people who held it, `KILLED_BY` on a victim pointing to killer, `DECEIVED_BY` on a target pointing to deceiver) are permitted and equivalent to the forward edge with directionality swapped. They are not separate types — query layers should treat `HELD_BY(a→b)` as identical to `HOLDS_TITLE(b→a)`. Reverse pairs are documented in their respective subsection notes.
>
> **Currently unmapped infobox fields** (deliberately deferred — see `working/todos.md` "Edge taxonomy gaps"): `dynasty` (222 pages), `written by` (168), `hatched` (8), `fathers` plural (21), `vassal` (8), `cadet branch` singular (11). These need taxonomy decisions before mapping.
>
> **Edge polish phase (future):** semantically-equivalent variants that crept in via different infobox fields (e.g., `Predecessor`/`Successor` both producing `SUCCEEDS` in different directions, or any future near-duplicates) get reviewed and merged by an agent reasoning step. That review happens AFTER all wiki ingestion completes — not during. Stage 3a / Stage 3b never merge edges.

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
| Conflict, Battles | `FIGHTS_IN` | For battle pages and characters' battle lists |
| Conflict (on a war page's battle list) | `PART_OF` | Reverse direction — battle → war containment; emit when parsing a war page's list of constituent battles |
| Result | `DEFEATS` | Extract victor/defeated from result text |
| Written by | `WRITTEN_BY` | For in-world texts (books, songs, decrees); subject = text, target = author |
