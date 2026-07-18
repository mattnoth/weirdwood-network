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

Fire & Blood: `fab`. **Not POV-structured** (third-person maester-historian narration by Gyldayn) — so F&B chapter files are named by SECTION, not POV: `fab-<section-slug>-NN[-pMM].md` where `NN` = the epub HTML file number (zero-padded 2-digit) and `-pMM` is an optional sub-split part. Split by `scripts/fire-and-blood-splitter.py` per `working/fire-and-blood/unit-map.json` (the epub `toc.ncx` is unreliable). 23 sections → 39 unit files.

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
│   ├── Battle            (single combat engagement: Red Wedding, Battle of the Blackwater)
│   ├── War               (multi-battle conflict: Robert's Rebellion, War of the Five Kings)
│   ├── Tournament        (formal tourney: Tourney at Harrenhal, Hand's Tourney, Ashford Tourney)
│   ├── Wedding           (named wedding event: Purple Wedding, Wedding of Joffrey and Margaery)
│   ├── Feast             (named feast: Feast in honor of King Robert's visit to Winterfell)
│   ├── Coronation        (formal coronation: Coronation of Robert I, Coronation of Tommen I)
│   ├── Trial             (judicial trial event: Sandor Clegane's trial by combat, Tyrion's trial)
│   ├── Assassination     (targeted killing-as-event: Death of Robert I via boar hunt, Assassination of Tywin)
│   ├── Execution         (named formal execution as event: Execution of Eddard Stark)
│   └── Conspiracy        (named secret plot as event: Grand Northern Conspiracy, Faith Militant uprising)
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
| `concept.theory` | Concept | Fan/community theory as an object — never an assertion of truth (S217 mint conventions: tier 3–5 ALWAYS; body prose always attributed "The theory holds that…"; evidence rides SUPPORTS/CONTRADICTS edges only) | claim, status (open \| show-confirmed \| jossed), origin, video_sources, pass_origin, confidence_tier (3–5) | R+L=J, Grand Northern Conspiracy, Jojen Paste |
| `concept.language` | Concept | Spoken or written in-world language | speakers, regions, script, status | Common Tongue, High Valyrian, Old Tongue, Dothraki, Skroth |
| `concept.medical` | Concept | Disease, poison, treatment, or medical condition | effects, regions, treatment, mortality | Greyscale, the bloody flux, the strangler, milk of the poppy |
| `concept.custom` | Concept | Cultural practice, tradition, or ceremony (NOT ethnic group — that's concept.culture) | regions, cultures, status_in_law | Bedding, Guest right, Fosterage, Heraldry, Dowry, Kingsmoot |
| `object.artifact` | Object | Object of narrative significance | material, current_holder, history | Ice, Dragonbinder, Dawn, glass candles |
| `object.text` | Object | In-world book, document, or song | author, subject, location | The Jade Compendium, The Rains of Castamere |
| `object.food` | Object | In-world food or drink (hospitality/feast/guest-right artifacts) | regions, ingredients, culture | Bowl of brown, lemon cakes, Arbor gold, dreamwine |
| `object.material` | Object | Raw material, mineral, or substance (NOT a named artifact — that's object.artifact) | composition, regions, uses, rarity | Dragonglass, dragonbone, Valyrian steel (as substance), gold, salt |
| `event.battle` | Event | Single combat engagement or plot event involving armed conflict | location, date, participants, outcome | Red Wedding, Battle of the Blackwater |
| `event.war` | Event | Multi-battle named conflict | belligerents, causes, phases, battles, outcome | Robert's Rebellion, War of the Five Kings |
| `event.tournament` | Event | Formal tourney or melee with named participants | location, date, host, champions, participants | Tourney at Harrenhal, Hand's Tourney, Ashford Tourney |
| `event.wedding` | Event | Named wedding event — distinct from `event.battle` for weddings that turn violent (Red Wedding remains `event.battle` because the slaughter dominates its narrative weight; routine but named weddings are `event.wedding`) | location, date, spouses, host, officiant, attendees | Purple Wedding, Wedding of Joffrey and Margaery, Wedding of Sigorn and Alys Karstark, Wedding of Ramsay and "Arya Stark" |
| `event.feast` | Event | Named feast or banquet — used for plot-significant hospitality events that are not weddings; often the staging ground for political action | location, date, host, attendees, hospitality_status | Feast in honor of King Robert's visit to Winterfell, Welcoming feast at the Twins |
| `event.coronation` | Event | Formal coronation event | location, date, monarch, officiant, attendees | Coronation of Robert I Baratheon, Coronation of Tommen I, Aegon's coronations |
| `event.trial` | Event | Judicial trial event — formal proceeding with named accused, judges, and resolution. Includes trial by combat | location, date, accused, judges, champion, outcome | Sandor Clegane's trial by combat, Tyrion's trial in King's Landing, Tyrion's trial at the Eyrie |
| `event.assassination` | Event | Named targeted killing event — distinct from `KILLS` (the edge between killer and victim); this is the event-hub for multi-participant killings with planning, conspirators, instrument, victim | location, date, victim, agents, conspirators, instrument | Death of Robert I (boar hunt), Assassination of Tywin Lannister, Murder of Jon Arryn |
| `event.execution` | Event | Named formal execution as event — distinct from the `EXECUTES` edge (executor → victim) for executions whose narrative weight justifies a hub (orderer + executor + witness + place + instrument) | location, date, victim, executor, orderer, instrument, witnesses | Execution of Eddard Stark, Execution of Lord Rickard Karstark |
| `event.conspiracy` | Event | Named secret plot as event-hub — multi-participant covert scheme treated as a discrete event for traversal (who conspired, what was the target, what was the outcome) | participants, target, period, outcome | Grand Northern Conspiracy, Faith Militant uprising, Queenmaker plot |
| `event.deception` | Event | Named discrete act-of-deceiving as event-hub — a single staged moment (or tight sequence) whose purpose is to propagate a false belief to a specific audience. Distinct from `event.conspiracy` (ongoing covert *scheme* over months/years) and from the `DECEIVES` edge (dyadic deceiver→deceived). Use when the deception is itself the event: who staged it, who was the audience, what false belief was planted, what the payoff was. Often nested INSIDE an `event.conspiracy` (e.g., Wyman's staged execution is a beat within the Grand Northern Conspiracy). Added Session 93 (2026-06-12). | location, date, staged_by, audience, false_belief, payoff, instrument | Wyman Manderly's staged execution of Davos, Cersei's false-attack claim re Jaime's street brawl, Theon's burned "Stark boys" charade, Jeyne Poole as "Arya Stark" |
| `event.incident` | Event | Named discrete incident or confrontation — a bounded multi-beat event that is neither a battle nor a formal ceremony but has enough narrative weight and causal consequence to anchor sub-beats and dyads (e.g., a roadside confrontation, a ship attack, a single-location crisis). Distinct from `event.battle` (organized armed combat) and `event.assassination` (targeted killing with planning/conspirators). Use when the event is primarily defined by a cluster of related actions at a specific place and time. Already in use by 5+ live nodes. Added Session 96 (2026-06-14). | location, date, participants, trigger, consequences | Incident at the Trident (Arya/Joffrey/Mycah kingsroad confrontation), Attack on Ned Stark in the Streets of King's Landing |
| `event.appointment` | Event | Named elevation to an office or institution as a discrete event — the moment of naming/investing someone into a role (Kingsguard induction, naming a Hand or Lord Commander). Distinct from the `APPOINTS` edge (appointer → appointee dyad); use the event-hub when the appointment itself carries narrative weight (who was passed over, what it triggered). Added Session 199 (2026-07-07, F&B enrichment). | location, date, office, appointee, appointer | Criston Cole appointed to Kingsguard (105 AC), Criston Cole named Lord Commander (112 AC) |
| `event.exile` | Event | Named banishment/exile as a discrete event — the removal of a person from court or realm, ordered or self-imposed. Distinct from the `BANISHES` edge (banisher → banished dyad). Added Session 199 (2026-07-07, F&B enrichment). | location, date, exiled, orderer, cause, destination | Exile of Maegor (40 AC), Daemon exiled after the Rhaenyra scandal |
| `event.birth` | Event | Named birth as a discrete event — used when a birth is itself plot-load-bearing (succession stakes, prophecy, a death in childbed). **Slug convention: `birth-of-<canonical-character-slug>`** (bare first names collide across the Targaryen dynasty). Added Session 199 (2026-07-07, F&B enrichment). | location, date, child, parents, complications | Birth of Maegor I Targaryen, Birth of Aegon II Targaryen |
| `event.investiture` | Event | Formal grant/assumption of a seat, title, or domain as a discrete event — broader than `event.coronation` (crowns only); covers a claimant taking a castle-seat, a principality granted, an heir installed. Added Session 199 (2026-07-07, F&B enrichment). | location, date, recipient, grantor, seat_or_title | Rhaenyra takes Dragonstone as her seat |
| `event.death` | Event | Named death as a discrete event-hub — a killing or dying that is neither a formally-planned `event.assassination` nor a judicial `event.execution`: combat deaths, natural/illness deaths, murders whose agency is unproven, and the many Fire & Blood `death-of-<person>` hubs. **Already referenced normatively** by the `SUSPECTED_OF` edge (an unproven killing "stays `event.death`, not `event.assassination`") — sanctioning this row makes de-facto usage explicit. Distinct from the `KILLS`/`KILLED_BY` dyad (this is the multi-participant event hub). Sanctioned Session 207 (2026-07-10; 141 live nodes). | location, date, deceased, cause, agent | Death of Aegon II, Death of Khal Drogo, Death of Ygritte, Death of Queen Rhaenyra |
| `event.capture` | Event | Named capture, arrest, or hostage-taking as a discrete event — the event-hub form of the `CAPTURES`/`IMPRISONS` edges, used when the taking itself carries narrative weight (who ordered it, who resisted, what it triggered). Sanctioned Session 207 (2026-07-10; 42+1 live nodes). | location, date, captive, captor, orderer | Arrest of the Sand Snakes, Jaime Lannister is captured, Ned orders Cersei's arrest |
| `event.ceremony` | Event | Named ceremonial event NOT covered by the specific ceremonial leaves (`event.wedding`/`coronation`/`investiture`/`appointment`/`feast`) — kingsmoots, elections, proclamations, oath-swearings, coming-of-age/nameday milestones, ritual observances. Sanctioned Session 207 (2026-07-10; 24+3 live nodes). | location, date, officiant, honoree, rite | Kingsmoot on Old Wyk, Jon elected Lord Commander, Robb proclaimed King in the North |
| `event.decree` | Event | Named royal edict, law, or proclamation as a discrete event — the legislative act itself (distinct from the `event.council` that debates it). Common in Fire & Blood's governance history. Sanctioned Session 207 (2026-07-10; 10+1 live nodes). | date, issuer, subject, provisions | Abolition of the lord's right to the first night, Promulgation of the Widow's Law, Doubling of the Gift |
| `event.council` | Event | Named formal deliberative assembly as a discrete event — great councils, regency-council selections, war councils, lords' gatherings. The OPEN counterpart to the covert `event.conspiracy`. Sanctioned Session 207 (2026-07-10; 9 live nodes). | location, date, convener, attendees, resolution | Great Council of 101 AC, Selection of three regents by lot, Accord of Storm's End |
| `event.betrothal` | Event | Named betrothal as a discrete event — the political act of promising a marriage (distinct from `event.wedding`, the marriage itself; a betrothal is frequently load-bearing on its own: succession stakes, alliance-forging, later broken). Dynastic betrothals are a recurring governance beat in Fire & Blood. The `BETROTHED_TO` edge carries the couple relation; the event node anchors the act, its broker, and its consequences. Sanctioned Session 208 (2026-07-10; Matt's call after the review-bucket vein surfaced 5 more — 3 S207-folded incident nodes retyped up the same session). `event.betrayal` was considered alongside it and REJECTED (the BETRAYS edge carries the relation; betrayal events type by their physical shape — battle/conspiracy/incident). | date, betrothed pair, broker, stakes, outcome | Betrothal of Aegon III and Daenaera Velaryon, Betrothal of Cregan Stark and Alysanne Blackwood, Betrothal of Alysanne to Orryn Baratheon |
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

**When this taxonomy is used:** This controlled vocabulary is the single source of truth for **every emitter** (see the *Vocabulary lock* note under `## Edge Types` below): the **graph layer** (building nodes and edges in `graph/`), the **wiki ingestion pass** (Pass 2), any **downstream analytical passes**, and — as of the Dunk & Egg Pass-1 **v4** prompt (2026-06-23) — **Pass 1 mechanical extraction** itself. Pass 1's `## Relationships Observed` table now emits exactly one controlled UPPER_CASE type per row (from the character-to-character subset), with a `NEEDS_VOCAB:` gap-hatch for genuine non-fits. (The earlier five-book Pass-1 extractions used the v1–v3 prompts, which recorded relationships in free-text natural language; those free-text labels are normalized → controlled vocabulary when graph edges are built. New Pass-1 work emits the vocabulary directly, so it needs no normalization step.)

**Qualifier enums for Tier-1/Tier-2 edge types:** see `reference/edge-qualifier-vocab.md`. Eight types require a `qualifier` field (Tier 1: SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF, HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO); nine types allow an optional qualifier (Tier 2: BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH, DECEIVES, REVEALS_TO, ATTACKS, GUEST_OF, IN_LAW_OF). All other edge types must NOT carry a `qualifier` field.

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
| `COURTS` | Active suitor relationship — pre-betrothal pursuit of marriage. Distinct from `BETROTHED_TO` (formal engagement) and `LOVER_OF` (sexual/romantic). Use when prose describes someone as a "suitor" / "sought her hand" / "courted." Common pattern: Lysa Arryn's suitors after Jon Arryn's death; Rohanne Webber's suitors; Sansa pre-marriage. | Suitor → Object-of-courtship | — |
| `PROPOSED_AS_BRIDE` | A third party proposes a specific woman as a bride for a specific man (or for a Throne-political match). Distinct from `MARRIES_OFF` (the actual arrangement of an executed marriage) and `BETROTHED_TO` (formalized engagement). Captures the diplomatic-offer stage common in Westerosi succession politics. | Proposer → Proposed bride | — |
| `STEP_PARENT_OF` | Step-parent to a step-child — a marital-consequence relation distinct from `PARENT_OF` (biological/adopted) and `WARD_OF` (institutional fostering). Use when prose explicitly says "stepmother", "stepfather", or structurally implies a step-parental relationship via a parent's marriage. Reverse is `STEP_CHILD_OF`. | Step-parent → Step-child | n/a (marital-consequence relation) |
| `STEP_CHILD_OF` | Reverse of `STEP_PARENT_OF` — emitted on the step-child's node pointing to the step-parent. | Step-child → Step-parent | n/a |
| `IN_LAW_OF` | Marriage-affinity relationship between two people connected by the marriage of a third. Symmetric. Covers "good-mother", "good-father", "good-sister", "good-brother", "mother-in-law", "sister-in-law", etc. Distinct from `SPOUSE_OF` (the marriage itself), `SIBLING_OF` (blood/milk/step), `PARENT_OF` (parentage). Use when a two-hop traversal (SPOUSE_OF + PARENT_OF + invert) would lose the named in-law relationship known from prose. Optional qualifier enum: see `reference/edge-qualifier-vocab.md`. | Symmetric | corpus (97 "good-mother/good-father/mother-in-law" mentions) |

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
| `BANISHES` | Political or royal act of exile — casting a person out of a domain, court, or realm. Distinct from `IMPRISONS` (confinement) and `DEPOSES` (removal from power without necessarily expelling). Captures Euron banishing Balon, court banishments, and exile-sentences issued by rulers. Tier-3 (no qualifier; destination is a separate temporal LOCATED_AT). | Banisher → Banished-person | corpus |

### Factional & Diplomatic

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `MEMBER_OF` | Belongs to a faction, order, or organization | Person → Faction | — |
| `FOUNDED` | Created or established an organization, house, or institution | Founder → Founded | Founder, Founded |
| `ALLIES_WITH` | Alliance (note if temporary, forced, or strategic) | Symmetric | — |
| `OPPOSES` | Active opposition or enmity | Symmetric | — |
| `MANIPULATES` | One party unknowingly used by another. Note mechanism in `notes` when known (e.g., `via bribe`, `via flattery`, `via false information`). | Manipulator → Target | — |
| `BETRAYS` | Broke faith, oath, or alliance | Betrayer → Betrayed | — |
| `NEGOTIATES_WITH` | Diplomatic engagement (may not result in alliance) | Symmetric | — |
| `CONTRACTED_WITH` | Formal contractual or commissioned engagement — distinct from `ALLIES_WITH` (political alliance), `SERVES` (employer-employee state), `NEGOTIATES_WITH` (diplomatic, may not conclude). Use when a party hires/commissions another for a specific service: hiring the Faceless Men for an assassination, contracting a sellsword company, commissioning a maester for a specific task. | Contractor → Contracted party | — |
| `CONSPIRES_WITH` | Secret joint plot — two or more parties engaged in a covert scheme together. Distinct from `ALLIES_WITH` (open political alliance) and `NEGOTIATES_WITH` (diplomatic engagement). Covers the Tyrell-Lannister Joffrey-poisoning conspiracy, Arianne's Queenmaker plot, the Grand Northern Conspiracy, and any secret-pact variant where the alliance must be concealed. Symmetric. Tier-3. | Symmetric | corpus |

### Military & Conflict

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `FIGHTS_IN` | Participates in a battle, war, or tournament as a combatant. | Person → Event (battle/war/tournament) | — |
| `COMMANDS_IN` | Holds command role in a battle or war (note which side), OR acts as the orderer/instigator of an event where the commander did NOT personally execute the act (e.g., Tywin ordering the Mountain to attack the Riverlands — Tywin is `COMMANDS_IN` the event, the Mountain is `AGENT_IN`). Covers both the military-command and the instigator/orderer roles to avoid proliferating near-synonym types. | Person → Event/War | — |
| `PART_OF` | Battle or sub-event is a component of a larger war — event-in-war containment. Coarse-grained; the source is itself an event (typically a battle), and the target is the war it belongs to | Battle → War | Conflict, Battles |
| `SUB_BEAT_OF` | A finer-grained event-beat is a moment within a larger named event hub. Distinct from `PART_OF` (event-in-war scope): `SUB_BEAT_OF` is beat-in-event scope, used when a chapter-beat mint (e.g., `lord-walder-calls-for-the-bedding`, `the-bedding-call`, `rains-of-castamere-plays`) names a moment INSIDE a parent event (`red-wedding`) rather than the event itself. Enables temporal-granular queries like "what beats happened before the slaughter started" that would be erased if the beat were collapsed into the parent. Sub-beats inherit the parent's participants, location, and any `VIOLATES_GUEST_RIGHT`-class edges via traversal. Do NOT use for surface-form aliases (use `aliases:` array); do NOT use for event-in-war containment (use `PART_OF`). Tier-3. | Beat → Parent event | — |
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
| `PRISONER_EXCHANGE_FOR` | Symmetric body-for-body prisoner swap (or proposed swap) between two captives held by opposing sides. Distinct from `RANSOMS` (one-direction payer → captive: gold/concession for release) — the anchor difference is two captives exchanged rather than payer + captive. Examples: Robb's proposed Robett ↔ Martyn Lannister; the proposed Theon ↔ Stark-girls swap; Edmure ↔ Cleos Frey-class swaps. Tier-3 (no qualifier). | Symmetric (captive ↔ captive) | — |
| `IMPRISONS` | Holds a captive in named confinement (cell, dungeon, tower) — distinct from `CAPTURES` (battlefield event) and `PRISONER_OF` (the captive's state); captures the institutional/judicial act of confinement, e.g., Cersei imprisoning Tyrion in the Red Keep after Joffrey's death (he was already at court, not captured) | Imprisoner → Imprisoned | — |
| `GUARDS` | Physical custody of a subject by a custodian — encompasses both protective custody (Kingsguard→King; bloodriders→Khal; sworn-shield→ward) AND custodial confinement (gaoler→prisoner; jailer→captive). Distinct from `PROTECTS` (beneficiary axis — acts for the target's benefit) and `IMPRISONS` (judicial/decisional confinement — typically lord-issued; `GUARDS` is the day-to-day executor of custody). When both protection AND confinement apply (Hound holding Arya), emit `GUARDS` alongside `PRISONER_OF` and/or `PROTECTS` as the prose warrants. Tier-3 (no qualifier). | Custodian → Subject-of-custody | — |
| `KILLED_WITH` | Combat death attributed to a specific named artifact — mirror of `EXECUTED_WITH` for non-judicial battlefield deaths. Use when prose names the weapon as agent of death ("slain by Orphan-Maker", "took an arrow from Ice"). Coexists with `KILLED_BY person` — the person did the killing, the artifact was the instrument. | Victim → Artifact | — |
| `KNIGHTED_BY` | Granted knighthood by another knight or lord. Distinct from `TUTORS` (skill transfer over time) and `APPOINTS` (political office). Use when prose explicitly describes the dubbing/knighting. | Knight → Dubber | — |
| `BESTOWS_KNIGHTHOOD_ON` | Reverse of `KNIGHTED_BY` — emitted on the dubber's node. | Dubber → Knight | — |
| `ATTACKS` | Generic physical violence — combat-style attack, creature attack, or person-on-person aggression that does NOT necessarily result in death (use `KILLS`/`POISONS`/`EXECUTES` if death; `DUELS` if formal mutual combat). Covers creature attacks (eagle on warg, direwolf on attacker), unprovoked violence (Darkstar slashing Myrcella, the Mountain striking Loras's horse), assault in the non-sexual sense. Includes both character→character and creature→character. For sexual violence specifically, use `ASSAULTS`. | Attacker → Target | — |
| `ASSAULTS` | Sexual violence — rape, attempted rape, or sexual assault. Distinct from `ATTACKS` (physical violence, non-sexual). Use only when prose makes the sexual nature explicit. Examples: Gregor Clegane & the five Bracken sisters during the Burning of the Riverlands; Owen Inchfield + Raymun Fossoway attempting Brienne; the canonical Gregor wartime pattern. | Assailant → Victim | — |
| `PARTICIPATES_IN` | Active non-combat involvement in a named event — logistical, administrative, organizational, or supportive role. Distinct from `FIGHTS_IN` (combatant), `ATTENDS` (guest/audience at a gathering), `COMMANDS_IN` (command-tier role). Examples: Medrick Manderly transporting men to the Wall during the Hour of the Wolf; quartermasters in named battles; logistical participants in coronations/kingsmoots/sieges who are not officiants. | Person → Event (`event.*`) | — |
| `RESCUES` | Dramatic single-moment extraction from danger — rescuer saves the target from death, capture, or peril. Distinct from `PROTECTS` (steady-state guardianship) and `HEALS` (medical restoration). Covers Beric rescuing BWB members, Davos rescued by Salladhor, Sam & Gilly rescued by the Mysterious Rider, Jon rescuing Ghost from wildlings. Tier-3 (no qualifier). | Rescuer → Rescued-person | corpus |
| `TORTURES` | The act of inflicting deliberate physical pain — flaying, racking, burning, or other sustained bodily torment. Distinct from `ATTACKS` (generic physical violence; not necessarily sustained or systematic), `ASSAULTS` (sexual violence specifically), `EXECUTES` (formal death sentence), and the `REVEALS_TO=under_torture` qualifier (which captures the informational *effect* of torture, not the act itself). Major narrative thread: Bolton flaying tradition, Mountain at Harrenhal, Qyburn's "studies", the Bloody Mummers, Black Cells. Without this edge, "who has Ramsay tortured?" cannot be graph-answered. Tier-3 (no qualifier; method is sub-typology the narrative captures). | Torturer → Tortured-person | corpus |
| `AGENT_IN` | Acts as the agent/executor of an event — the participant who actually performed the act. Source is the executor; target is the event node. Reification role edge: use when attaching a character or house to a multi-party event hub instead of (or in addition to) a dyadic binary edge. See `VICTIM_IN` (patient), `COMMANDS_IN` (orderer who did not personally execute), `WIELDED_IN` (instrument). | Person/House → Event (`event.*`) | — |
| `VICTIM_IN` | Receives the action of an event as the victim or patient — the participant on whom the act was performed. Source is the recipient; target is the event node. Reification role edge: complement to `AGENT_IN` on the same event hub. | Person/House → Event (`event.*`) | — |
| `WITNESS_IN` | The **observer/perceiver** slot on an event hub — a character whose *load-bearing perception* of a charged event (violence, death, a secret, an atrocity) is itself worth a graph edge, distinct from acting (`AGENT_IN`), suffering (`VICTIM_IN`), ordering (`COMMANDS_IN`), or combatting (`FIGHTS_IN`). **Default to an EDGE** onto the existing event node (the Q2 three-lens consensus, S117): reify the witnessing as its own `event.*` NODE *only* when the act of seeing owns an outgoing causal edge — i.e. the seeing `CAUSES`/`TRIGGERS`/`MOTIVATES` a downstream event (e.g. `bran-witnesses-jaime-and-cersei`, whose seeing causes his fall) — or the witnessed thing has no node of its own. Mechanical test: *does the seeing need an outgoing edge? yes → node; no → edge.* Promotion path: start as an edge, promote to a node later only if a causal edge actually gets drawn. **Text-anchor gate:** emit only when the prose shows the character actually SEES it — present-but-shielded does NOT qualify (Yoren forces Arya's eyes shut at Ned's execution → Arya is NOT a witness; Sansa, who "could not turn her head," IS). **Boundary vs `ATTENDS`:** `ATTENDS` = voluntary audience at a *staged social/ceremonial gathering* (feast, wedding, tourney-as-a-whole, court, coronation); `WITNESS_IN` = perception of a charged/violent/secret incident. Same person can `ATTENDS` the Tourney of the Hand AND `WITNESS_IN` the Loras-vs-Gregor bout within it (different targets). Tier-1 when verbatim-cited. Added Session 117 (2026-06-21); first instances `sansa-stark WITNESS_IN execution-of-eddard-stark`, `arianne-martell WITNESS_IN myrcella-is-maimed-by-darkstar`, `hoster-tully WITNESS_IN battle-of-the-camps`. | Person → Event (`event.*`) | — |

> **Reification role vocabulary note:** `WIELDED_IN` (already in the Possession & Artifacts section, artifact→event) serves the **instrument** role for reified events — no `INSTRUMENT_IN` type is needed. `COMMANDS_IN` (below) serves the **orderer/instigator** role. Together with `AGENT_IN` and `VICTIM_IN`, these four cover the standard **action/instrument** participant slots (agent, patient, orderer, instrument) on an event hub. The **perceiver/observer** slot is a fifth role, `WITNESS_IN` (S117) — epistemic, not action (the perceiver acts on nothing and receives nothing); voluntary audience at a *staged* gathering is `ATTENDS`, not `WITNESS_IN`.

### Knowledge & Information

> **Deprecated (Session 63, 2026-05-21):** `KNOWS` was removed from the active vocabulary. Stage 4 wiki-prose classification ran an 82.3% fallback rate on KNOWS emits — the semantic boundary ("knows of" vs "met once" vs "heard rumor of") is too blurry for prose-derived classification to enforce. Character-knowledge relationships will be derived from a future Pass-1-based chapter co-occurrence + Information Revealed pass. Existing KNOWS edges in the graph (363 Haiku-emit + 21 Sonnet-control-arm) are preserved as historical record; downstream consumers filter deprecated types on read.

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
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
| `AFFLICTED_BY` | Character suffers from a named disease, condition, or magical affliction (living state). Target is `concept.medical`. Distinct from `KILLED_BY` (target = person), `DIED_AT` (location), `DIED_OF` (cause-of-death; this is the living state). Examples: Jorah Mormont/greyscale, Shireen Baratheon/greyscale, Stannis/burns. | Character → Medical | — |
| `DIED_OF` | Character's death was caused by a named disease/condition (post-mortem state). Target is `concept.medical`. Distinct from `KILLED_BY` (person-killer), `DIED_AT` (location), `EXECUTED_WITH` (judicial weapon). Mirrors `AFFLICTED_BY` for the post-mortem state. Examples: Hoster Tully/Spring Sickness, Albin Massey/Shivers, Medrick Manderly/Winter Fever, the Old King Jaehaerys/Great Spring Sickness. | Character → Medical | — |
| `SPIES_ON` | A spy or agent actively surveils, monitors, or gathers intelligence about the target. Distinct from `SERVES` (employment state) and `MANIPULATES` (wrong direction — spy works for handler, not against target). Westeros has structurally-distinct spy networks (Varys's little birds, Littlefinger's network, Qarth's whispers). Tier-3. | Person → Surveilled-person | n/a (Pass 1 corpus + Sonnet no-fit) |
| `INFORMS` | A spy, agent, or informant reports intelligence to their handler or spymaster. Complements `SPIES_ON` (target = person being watched vs. target = handler receiving reports). Distinct from `SERVES` (too generic) and `REVEALS_TO` (one-time disclosure; INFORMS is the ongoing reporting relationship). Tier-3. | Person → Handler/Spymaster | n/a (Pass 1 corpus + Sonnet no-fit) |

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
| `COMPANION_OF` | Close personal friendship or camaraderie. Distinct from `ALLIES_WITH` (political alliance), `TRUSTS` (one-direction confidence), `LOVES` (romantic/deep-familial), `RESPECTS` (cold regard). Use when prose explicitly names a friendship ("good friends with", "sworn brothers", "close companion"). Examples: Patrek Mallister & Edmure Tully; Robert & Ned in their youth; Brienne & Pod; Davos & Salladhor Saan. | Symmetric | — |
| `REPUTED_AS` | Collective reputation or general perception attached to a character without a specific perceiver — distinct from `PERCEIVED_AS` which requires a named POV. Target is `concept.*` (e.g., `concept.magic` for "reputed witch", `concept.craft` for "reputed swordsman", `concept.vice` for "reputed drunkard"). Use when prose narrates a public-domain reputation rather than one character's view of another. | Character → Concept | — |
| `ENCOUNTERS` | Plot-significant face-to-face meeting between two characters, anchored by explicit prose staging (verb gate enforced by validator per CRITICAL RULE — see classify prompt Rule 6). Reserved for first meetings, brief road-crossings, set-piece confrontations short of duel/combat where the meeting itself carries narrative weight. Examples: Dunk ↔ Egg at the Ashford inn; Brienne ↔ Randyll Tarly in AFFC; Arya ↔ Sandor on the kingsroad; Jon ↔ Mance at the Frostfangs; Sam ↔ Coldhands beyond the Wall. NOT for co-presence at events (use `LOCATED_AT` / `ATTENDS` / `FIGHTS_IN`), retinue/court presence (`TRAVELS_WITH`), or formal diplomatic engagement (`NEGOTIATES_WITH`). **Coverage scope (Session 63, 2026-05-21):** Stage 4 captures only wiki-prose-staged meetings — biographical-summary register often elides staging verbs even when meetings happened in-text. Comprehensive character-meeting coverage will come from a future book-derived pass; treat wiki ENCOUNTERS as partial-by-design. Tier-3 (no qualifier). | Symmetric (character ↔ character) | — |

### Spatial & Temporal

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `LOCATED_AT` | Entity at location (with book/chapter timestamp). Covers both event-at-place (battle location) and person-at-place (witness location). Deprecated synonym `LOCATED_IN` was emitted by an early parser variant; normalize on read. | Entity → Location | Location, Seat |
| `SEAT_OF` | Primary location of a house or faction | Location → House/Faction | Seat, Seats |
| `TRAVELS_TO` | Movement from one location to another | Traveler → Destination (note origin) | — |
| `TRAVELS_WITH` | Co-presence in someone's company, on the road OR in attendance at court/event. Covers both journeying together (Arya/Gendry/Hot Pie; Sam+Gilly+Aemon to Oldtown; Dunk+Egg) AND retinue/court presence (Robett kneeling among Catelyn's welcomers at Winterfell). Distinct from `COMPANION_OF` (sustained friendship), `ALLIES_WITH` (political), `MEMBER_OF` (faction affiliation), `SERVES` (subordination). Tier-3 (no qualifier). | Symmetric (character ↔ character) | — |
| `BORN_AT` | Birthplace | Person → Location | Born |
| `DIED_AT` | Place of death | Person → Location | Died |
| `BURIED_AT` | Place of burial or interment | Person → Location | Buried |
| `IMPRISONED_AT` | Captive's place of confinement during a specific imprisonment (cell, dungeon, sky cell, black cells, tower used as gaol, prison hulk). Distinct from `LOCATED_AT` (general presence — not captivity-marked), `IMPRISONS` (jailer→captive judicial relationship), and `PRISONER_OF` (captive↔captor symmetric state). Examples: Ned/Black Cells; Tyrion/Eyrie sky cell; Jaime/Robb's camp at Riverrun; Davos/Dragonstone dungeon. Tier-3 (no qualifier). | Captive → Location (`place.location`) | — |
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
| `PURCHASED_FROM` | Transactional acquisition of an artifact (or service) via purchase — distinct from `OWNS` (steady state), `GIFTED_TO` (voluntary transfer), `LOOTED_BY` (taken by force), `INHERITED_BY` (death-succession). Captures the transactional moment + the seller. Examples: Dunk purchasing the dragon-of-Pentos shield from Pate the Old; ship-passage purchases (when concretely named); merchant exchanges that are plot-significant. | Buyer → Seller | — |
| `BUILT` | Character physically built or oversaw the construction of a named structure (castle, tower, sept, wall, monument). Distinct from `FOUNDED` (scoped to organizations/houses/orders) and `OWNS` (steady state). Use when prose explicitly names the builder of a place. Examples: Brandon-the-Builder/The Wall, Brandon-the-Builder/Storm's End (legend), Lord-Triston-Hightower/Starry-Sept. | Builder → Structure (`place.location`) | — |
| `CAPTAIN_OF` | Character is captain (master/commander) of a named vessel. Target MUST be `object.artifact` (the vessel). Distinct from `COMMANDS` (military org) and `OWNS` (ownership state — captains may or may not own the vessel). Examples: Davos Seaworth/Black Betha, Victarion Greyjoy/Iron Victory, Asha Greyjoy/Black Wind, Salladhor Saan/Valyrian. | Captain → Vessel (`object.artifact`) | — |
| `CREW_OF` | Character serves as a crew member (non-captain) of a named vessel — sibling to `CAPTAIN_OF`. Target MUST be `object.artifact` (the vessel). Use when prose explicitly names a non-captain role (oarsman, first mate, ship's cook, sail-master). Captain → use `CAPTAIN_OF`. Generic faction membership → use `MEMBER_OF`. Note specific role in `notes` if known ("first mate"). | Crew member → Vessel (`object.artifact`) | — |

### Identity & Disguise

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `ALIAS_OF` | Known by another name. **Substitution test (canonical rule, S86 2026-06-08):** two strings are aliases iff substituting one for the other in any sentence about the entity does NOT change the truth value. "Wedding at the Twins" ↔ "Red Wedding" passes — same event. "Lord Walder calls for the bedding" ↔ "Red Wedding" FAILS — the bedding-call is a moment WITHIN the Red Wedding, not the whole event. Granularity differences are NOT aliases; emit `SUB_BEAT_OF` instead. The dashes-vs-spaces test catches surface variants only, NOT granularity. | Alias → True Identity | Alias, Aliases |
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
| `PRACTICES` | Character actively practices a named magical or ritual discipline. Target is `concept.magic` (or `concept.craft` for non-magical-but-named-discipline cases). Distinct from `WARGS_INTO` (active occupation moment), `BONDED_TO` (static pairing), `WORSHIPS` (religious devotion, not the magical practice itself), `CLERGY_OF` (religious office). Examples: Melisandre/shadow-binding, Mirri Maz Duur/maegi-blood-magic, Bran/greendreams, faceless-men/identity-transfer, Qyburn/necromancy. | Character → Magic discipline | — |

### Cultural & Religious

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CULTURE_OF` | Person belongs to a cultural group | Person → Culture | Culture, Race |
| `WORSHIPS` | Follows or serves a deity/religion | Person → Religion | Religion |
| `SACRED_TO` | Location or artifact is holy to a religion | Entity → Religion | — |
| `CLERGY_OF` | Serves as religious official | Person → Religion | — |
| `OFFICIATES` | Character performs the ritual / religious / ceremonial role at a named event (weddings, funerals, coronations, kingsmoots, namedays, knighting ceremonies). Distinct from `CLERGY_OF` (general clergy status, target = religion) and `ATTENDS` (guest/audience). Target is `event.*` or specific named ceremony node. Examples: Melisandre/wedding-of-sigorn-and-alys-karstark; the High Septon/coronation-of-tommen-i; Aeron Damphair/kingsmoot-of-299-ac. | Character → Event | — |
| `HONORED_AT` | Character is the **ceremonial honoree** — the recipient of a conferred honor at a named event (queen of love and beauty crowned at a tourney, a nameday honoree, the dubbed knight at a knighting). The reification-role complement on a ceremonial event hub: the **conferrer** uses `AGENT_IN` (e.g. Rhaegar laying the laurel), the **honoree** uses `HONORED_AT`. Distinct from `ATTENDS` (audience), `OFFICIATES` (performs the rite), `WITNESS_IN` (perceiver), `AGENT_IN` (the one who acts/confers). Added Session 134 (2026-06-23) to retire the off-vocab `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` tail-LLM leakage; first instance `lyanna-stark HONORED_AT crowning-of-lyanna-at-harrenhal`. Tier-1 when verbatim-cited; no qualifier. | Character → Event (`event.*`) | — |
| `NAMED_AFTER` | An entity was given its name in honor of, or as a reference to, another entity. Captures Westeros's pervasive dynastic name-recycling culture (Rickard Karstark named for Rickard Stark, the many Brandons and Aegons). Distinct from `ALIAS_OF` (a different name for the same entity), `SAME_AS` (identity-resolution), and `DEPICTED_IN` (in-world legend about a person). One-sided: the named entity points to its namesake. Surfaced in Sonnet `no-fitting-type` rejections. Tier-3 (no qualifier). | Entity → Namesake-entity | wiki (dynastic naming patterns) |

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
| `SUPPORTS` | A real passage the theory community reads as evidence FOR a theory — the edge asserts the reading exists, not that the theory is true. Every edge carries its own byte-verified verbatim quote + chapter:line ref | Evidence node → Theory | — |
| `CONTRADICTS` | A real passage that undermines a theory (or one scoped sub-claim — scope lives in the edge `note`) | Evidence node → Theory | — |
| `CITED_BY` | DEFERRED (S216) — no out-of-world source node type; provenance lives in theory-node frontmatter (`video_sources`, `origin`) | Theory → Source | — |

**Theory-layer conventions (ratified S216–S217, Matt):**

- **Tier floor is absolute:** theory nodes and SUPPORTS/CONTRADICTS edges are **tier 3–5 ALWAYS** — no "event-anchored" or other exceptions. Per-edge tier variance under a node is allowed (a tier-3 node may carry tier-4/5 edges).
- **Layer rule:** facts already owned by tier-1/2 nodes are the theory's *premise* (prose), not theory evidence — don't re-mint them as edges. An existing node CAN source an edge where its confirmed reality bears directly on the claim (the subject-link pattern).
- **Subject-link pattern:** a theory may link to the event/artifact node it is *about* via a scoped evidence edge (GNC G1 precedent: the confirmed event node sources a SUPPORTS into the theory that generalizes it).
- **Parallel-FORESHADOWS (S217):** when a theory-evidence quote foreshadows an event that actually occurs on the page, the factual layer gets a `FORESHADOWS` edge to that event node (canon-visible; tier 2–4 by mapping strength, typically 2–3) alongside the theory-layer SUPPORTS edge. Both edges may carry the same quote — different layers, different claims.
- **Naming:** display names are claim-style ("Roose Bolton is a skin-stealing immortal"); genuinely unresolved multi-candidate whodunits use question-form ("Who is Coldhands?", "Who Wrote the Pink Letter?", "Who is the Hooded Man of Winterfell?").
- **One node per canonical named theory;** umbrella wiki "X/Theories" stubs stay dark unless they ARE the canonical theory.
- **Evidence sources:** any node class whose entity the quote is about may source an evidence edge — including `object.food` (weirwood-paste), legend/`object.text` (rat-cook), and `concept` nodes (wights). From wave 2 onward, theory edges may cite `fab-*` (Fire & Blood) chapters — same quotecheck machinery; chronicler unreliability handled by tier + `in_universe_source`.
- **Ungrounded material** (show-only, TWOW/TWOIAF-fenced, GRRM interviews, community reasoning) is domain-labelled in the node body — never edges.
- **Chat exposure:** theories are invisible to the chat persona (SHARED_RULES guardrail). Plan of record (S217): an off-by-default UI toggle — OFF = runtime tool-layer filter strips theory nodes/edges; ON = labeled-speculation prompt contract. Build is a separate gated session.

### Causal & Plot

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `CAUSES` | Event A leads to Event B | Cause → Effect | — |
| `PREVENTS` | Action A blocks Event B | Preventer → Prevented | — |
| `ENABLES` | Condition A makes Event B possible | Enabler → Enabled | — |
| `MOTIVATES` | Event or condition drives a character's actions | Motivation → Actor | — |
| `TRIGGERS` | Immediate cause (narrower than CAUSES — the specific spark) | Trigger → Result | — |
| `SUSPECTED_OF` | A character is suspected — in-world and/or by the reader — of being the agent or cause of an event, where the published text does NOT prove it. The unproven counterpart to `AGENT_IN`/`KILLS`/`CAUSES`: use when the suspicion is itself load-bearing but the act is unconfirmed in the 5 published books. **Capped at Tier-2 — NEVER Tier-1** (Tier-1 is reserved for proven canon; an asserted-as-fact killing uses `KILLS`/`AGENT_IN`). Cite the in-text basis (accusation, portents, timing) in the rationale; out-of-text corroboration (TWOW-preview, author statements) may be noted but does not raise the tier. Added Session 116 (2026-06-20) — first instance: `euron-greyjoy SUSPECTED_OF death-of-balon-greyjoy` (Asha's accusation "Silence returns within a day of my lord father's death" + the storm-portents; Euron's confession exists only in the *Forsaken* TWOW-preview chapter, not published canon, so the killing stays unproven and the node stays `event.death`, not `event.assassination`). | Suspect → Event (`event.*`) | — |

#### The `ENABLES` vs `CAUSES` vs `TRIGGERS` contract (S121, 2026-06-21)

The three forward-causal edges are NOT interchangeable; they form a strength ladder, and the choice is load-bearing for graph honesty (the "sequence-only trap" — drawing causation where only chronology exists). Pick by this rubric:

- **`TRIGGERS`** — A is the **immediate spark** of B; B is the very next beat, nothing decisional sits between them. *Is B the very next thing, or is there a step in between?* If next → TRIGGERS. (`ned-confesses-to-treason TRIGGERS execution-of-eddard-stark`.)
- **`CAUSES`** — A **produces** B, possibly through intermediate (modeled or unmodeled) steps. Real causation, mediation allowed. (`siege-of-meereen CAUSES sons-of-the-harpy-kill-twenty-nine` — occupation breeds insurgency.)
- **`ENABLES`** — A is a **precondition** that makes B *possible* but does NOT force it; a third party or a character's free decision actually produces B. *Did A force B, or just open the door while someone/something else walked through?* If door-opener → ENABLES. This is the **relief valve for the sequence trap**: a military campaign's city→city transitions (`fall-of-astapor ENABLES battle-near-yunkai`) are ENABLES, never CAUSES — Astapor didn't *cause* Yunkai; Dany running a campaign did, and she *chose* to march. ENABLES also preserves third-party / dragon / human agency (`wedding-of-hizdahr ENABLES drogon-returns-to-daznak-pit` — the wedding only opened the pit; Drogon *chose* to descend).
- **`MOTIVATES`** — drives an **actor's** decision; target is a **character**, never an event. Use it to route a human choice instead of collapsing it into a false `A CAUSES B` (the agency-collapse check).

**`chain` excludes `ENABLES` by design.** The walk tool `weirwood query chain` follows only `{CAUSES, TRIGGERS, MOTIVATES}` — every `ENABLES` edge is a deliberate **segment break** in that walk (a precondition is not a consequence, so "what caused X?" arguably should not cross it). **To traverse a spine end-to-end including its preconditions, use `full-chain` (alias `--include-enables`)**, which renders ENABLES hops labeled `(precondition)`. Correct ENABLES data therefore reads as "missing" in `chain` unless you switch tools — that is expected, not a defect. (S120 board finding: the Essos spine's 4 ENABLES hinges made it read as 3 disconnected segments under `--causal-chain`.)

#### Two verification gate-levels for causal edges (S121, 2026-06-21)

Causal/role-edge minting uses two named gate-levels so the weaker level does not silently creep onto the hardest edges:

- **L1 — verified-at-mint.** The *same* subagent that researches the edge also adjudicates it (reads local cache, pins quotes, picks the edge type). Acceptable for `ENABLES` / role edges (`AGENT_IN`/`VICTIM_IN`/`WITNESS_IN`/`COMMANDS_IN`) / `SUB_BEAT_OF` and for obvious single-chapter calls. The `mint_essos_e3`/`e5` arcs are L1 exemplars.
- **L2 — independent fresh-verify.** A *separate* subagent with no prior context re-checks the edge against the local book/wiki cache. **REQUIRED for cross-book or contested `CAUSES`/`TRIGGERS`** (the Mirri-blood-magic / Rhaegal-not-Viserion class). Until L2 confirms, the edge carries `verified_by: pending`.

Matt gates at the policy level, not per-edge (memory `feedback_subagent_verify_not_matt`); these two levels are the policy.

### Temporal & Sequencing

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `PRECEDES` | Earlier event occurs before a later event in in-world chronology. Purely temporal (NOT causal — for the specific spark use `TRIGGERS`). Derived deterministically from `occurred.ac_year` on `event.*` nodes (S104): cross-year pairs are rock-solid; same-year pairs are ordered only when both carry `narrative_first` (reading-order proxy), and same-year siblings without it are left mutually unordered. Inverse direction is read by traversing the edge backwards — no separate `FOLLOWS` type is stored. Confidence inherits the source dating ceiling (tier-3 from wiki-year-pages). | Earlier event → Later event | — |

### Hospitality & Custom

| Edge Type | Description | Directionality | Wiki Source |
|-----------|-------------|---------------|-------------|
| `GUEST_OF` | Under someone's roof / protection by custom | Guest → Host | — |
| `VIOLATES_GUEST_RIGHT` | Broke the sacred hospitality compact | Violator → Victim | — |
| `GRANTS_SAFE_CONDUCT` | Promised safe passage | Grantor → Recipient | — |
| `ATTENDS` | Person present as guest or audience at a *staged social/ceremonial gathering* — not as combatant (`FIGHTS_IN`), commander (`COMMANDS_IN`), organizer (`OFFICIATES`), or charged-incident observer (`WITNESS_IN`). Use for tourney spectators (the tourney-as-a-whole), wedding guests, feast attendees, court hearings, coronation audiences. For load-bearing *perception of a charged/violent/secret incident* (an execution, a murder, a specific bout, a battle one watched), use `WITNESS_IN` instead (S117 split — `ATTENDS` no longer covers "witness"). | Person → Event | — |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Tournament champion crowns a chosen woman with the laurel wreath of Queen of Love and Beauty. Distinct edge because the act carries outsized narrative weight in ASOIAF (Rhaegar/Lyanna at Harrenhal as a war-trigger; Loras/Margaery; etc.) and chains to political consequences. Source = tournament champion; target = recipient. | Champion → Recipient | — |

---

## Node Frontmatter Conventions

> **Status (Session 86, 2026-06-08):** documented. `era:` is forward-only — NOT backfilled retroactively. Existing 7,000+ nodes do not need an `era` field; new mints stamp it at creation.

Every node carries these frontmatter fields. Required unless marked optional.

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Human-readable surface form. Used by display layers (chat UI, agent system prompts). Every node — wiki-derived AND chapter-beat mint — uses `name:` (NOT `title:`). | `"Red Wedding"` |
| `slug` | Kebab-case join key. Lower-case ASCII, hyphens. The canonical identifier for cross-file references and graph traversal. | `red-wedding` |
| `type` | Entity type from the hierarchy above. | `event.battle` |
| `aliases` | Optional. List of surface-form variants that pass the substitution test (see `ALIAS_OF` row). Used by `weirwood_query`'s alias resolver (`weirwood query resolve "<phrase>"`) and downstream resolvers. NOT for sub-beats — those emit `SUB_BEAT_OF` edges. | `["wedding-at-the-twins", "slaughter-at-the-twins"]` |
| `confidence` | Tier 1-5. | `tier-1` |
| `wiki_source` | Optional. URL to the source wiki page (if wiki-derived). | `"https://awoiaf.westeros.org/index.php/Red_Wedding"` |
| `era` | Optional, forward-only. The narrative epoch this entity belongs to. Set on new mints; NOT backfilled. The narrowing function in `scripts/plate4-wiki-cluster.py` weights `era=current-narrative` higher when classifying current-narrative mints, suppressing false-positive matches against pre-series events. | `current-narrative` |
| `first_available` | Optional. Spoiler gating field — DEFERRED to post-first-release backfill (see Spoiler Gating section below). | `"AGOT Bran II"` |
| `occurred` | Optional, `event.*` only. Block recording in-world event time (when it happened, not when the reader meets it). See `occurred:` block subsection below. | `{ ac_year: 283, … }` |
| `containers` | Optional, primarily `event.*`. **Array** of lowercase-kebab container names this node belongs to. A *tag*, NOT an umbrella parent node (see subsection). Omit the key or set `null` when untagged — **never `[]`**. | `[wo5k, north]` |
| `disambiguation_hub` | Optional, bool. `true` marks a node minted from a wiki **`Disambiguation pages`** page (bare-name index, e.g. `aegon-targaryen`). Its Identity is a composed "may refer to…" hub line listing the same-name cluster members. **Never an enrichment/UPDATE target** — enrichment passes (F&B reconciler etc.) MUST treat these as ambiguous, never write content onto them. Stamped by `scripts/wiki-prose-identity-composer.py` (S197). | `true` |
| `redirect_to` | Optional, slug. Set on a node minted from a wiki **`Redirect`** page (bare-name stub, e.g. `aenys-targaryen`); names the canonical node it resolves to (`aenys-i-targaryen`). Same handling as `disambiguation_hub` — blocklisted, never an enrichment target; consumers route a hit here to the target slug. Stamped by `scripts/wiki-prose-identity-composer.py` (S197). | `aenys-i-targaryen` |

### `era:` enum values

```
era: pre-conquest | age-of-heroes | targaryen-conquest | targaryen-rule
    | dance-of-dragons | roberts-rebellion | current-narrative
```

- `pre-conquest` — Before Aegon I (pre-1 AC).
- `age-of-heroes` — Legendary/mythic era (Brandon the Builder, Long Night).
- `targaryen-conquest` — Aegon's Conquest and Wars of Conquest (1 AC).
- `targaryen-rule` — Targaryen dynasty post-Conquest, pre-Dance.
- `dance-of-dragons` — The Dance and immediate aftermath.
- `roberts-rebellion` — Pre-AGOT Robert's Rebellion era (excluding the rebellion's deep prehistory, which is `targaryen-rule`).
- `current-narrative` — AGOT-onward main series (the events the books actually cover from the inside).

When in doubt between two values, prefer the one closer to `current-narrative` if the event has direct narrative consequence in the main series; otherwise prefer the earlier era.

### `occurred:` block (in-world event time)

> **Status (2026-06-16):** v1 populated. 112 `event.*` nodes dated deterministically from `working/wiki/data/chronology-events.jsonl` (single attested year + exact slug match) via `scripts/date-event-nodes.py`. Schema decision + 9-invariant validator: `working/design-opinions/2026-06-16-era-field-analysis.md`. Full design: `working/design-opinions/2026-06-15-events-time-SYNTHESIS.md`.

Optional block on `event.*` nodes recording WHEN the event happened in-world — distinct from where the reader encounters it (that axis is `narrative_first`, deferred). In-world reckoning is carried by a **signed `ac_year` integer (negative = BC)**. There is deliberately **no `era: AC|BC`** sub-field, because `era:` (above) already means narrative epoch — the sign on `ac_year` carries AC/BC instead.

| Sub-field | Meaning | Example |
|-----------|---------|---------|
| `ac_year` | Signed int. Positive = AC, negative = BC. null when unknown/mythological. | `283` |
| `ac_year_end` | Optional. SPAN endpoint only (wars/reigns); must be > `ac_year`. NOT for uncertainty. | `300` |
| `uncertainty_radius` | Optional. ± years for a fuzzy point estimate. Mutually exclusive with `ac_year_end`. | `5` |
| `precision` | `exact \| year \| decade \| century \| era \| relative-only` | `year` |
| `basis_source` | `narrative-prose \| appendix \| twoiaf \| wiki-year-page \| inferred` | `wiki-year-page` |
| `basis_reliability` | `primary-source \| secondary-source \| tertiary-fan \| inferred-only`. `tertiary-fan` caps `date_confidence` at tier-3. | `tertiary-fan` |
| `date_confidence` | Tier 1-5 — confidence in the DATE specifically (separate from node `confidence`, which is confidence the event *happened*). | `tier-3` |
| `dispute` | Optional sub-map. Populated only when ≥2 competing canon dates exist (e.g. GRRM-acknowledged inconsistencies). | — |

**v1 applied subset:** `ac_year`, `precision`, `basis_source`, `basis_reliability`, `date_confidence` only — all from `wiki-year-page` / `tertiary-fan` / `tier-3`. Deferred: `ac_year_end` spans (5 multi-year hubs staged for review), `uncertainty_radius`, `dispute`, the narrative reading-position axis (`narrative_first`, blocked on edge chapter-ref format normalization), BC dates (the deterministic source has none), and epoch `era` on event nodes. Mythological/legendary events (e.g. the Long Night) get NO `ac_year` — left null / `relative-only`.

### `containers:` field (narrative-container membership tag) — S121, 2026-06-21

A **container** is a big storyline tackled as a build unit (Essos, WO5K, NORTH, AEGON). The `containers:` field is an **array of lowercase-kebab container names** stamped on the event nodes that belong to that storyline:

```yaml
containers: [wo5k, north]
```

**It is a TAG, not a graph object.** There is no `wo5k` umbrella *node* with beats hanging off it — that would be the "bag-not-path" anti-pattern the project deliberately rejected (chain-as-arc / no-umbrella; an umbrella node loses the order and the why). `containers:` is pure node metadata; it adds no new graph object and so does **not** violate that decision.

- **Query:** `weirwood query container <name>` is **bag-retrieval** — it returns the set of nodes carrying that tag, **unordered**. It is explicitly NOT "show me the arc." For the ordered causal walk of a storyline, use `weirwood query chain` / `full-chain`. (A bag answers "what's in this storyline?"; a path answers "in what order, and why?")
- **Dual membership / seams:** a node on the boundary between two storylines carries both, e.g. `robert-orders-daenerys-assassination` is `containers: [wo5k, essos]` (a cross-container bridge). This is the natural representation of a seam — the node is built once and surfaces under both containers.
- **Untagged nodes:** omit the key or set `containers: null`. **Never use `[]`** — an empty-array "uncategorized" class becomes its own maintenance burden.
- **Backfill is incremental:** stamp as you build a container; retro-tagging the older floating standalone arcs (Red Wedding, Purple Wedding, etc.) is a separate decision, not automatic.

---

## Display Names: slug as identifier, name as surface

> **Status (Session 86, 2026-06-08):** policy documented. The graph layer stores both fields; rendering belongs to the consumer. No prompt-time enforcement.

Every node carries `slug:` (kebab-case join key) and `name:` (human-readable surface). Consumers pick whichever serves them:

- **Programmatic queries / edge endpoints / `weirwood_query`** — use `slug` everywhere. Slugs are the join key; never substitute the name.
- **Agent system prompts / agent reasoning in prose** — when the node frontmatter is in context, the agent naturally uses `name` in narrative explanations. No special enforcement; the surface follows the surroundings.
- **Chat UI rendering** — post-process slugs in agent output to human names at render time. The UI does the conversion via the node index; the graph stays slug-only.
- **JSONL / edge files** — slug always.

The previous "enforceable at the prompt layer" framing was overengineered — there is nothing to enforce. The two-field schema makes the right surface available to every consumer; how they pick is their concern.

### Schema requirement

`name:` is REQUIRED on every node (wiki-derived AND chapter-beat mint). The historical mint schema used `title:` for the human-readable surface; **as of Session 86, chapter-beat mints rename `title:` → `name:`**. The 219 Plate-3 staged mints will be rewritten at Plate 5 merge.

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
| `evidence_kind` | Provenance discriminator. Enum: `wiki-entity` \| `wiki-chapter-summary` \| `book-pass1` \| `wiki-infobox` \| `book-fab`. `book-fab` = grounded in *Fire & Blood* book text via the enrichment pass — Tier-1 when Gyldayn narrates it flatly; Tier-2 + `in_universe_source`/`disputed` when hedged/partisan. Distinguishes the maester-historian layer so queries can filter book-vs-wiki provenance. | `book-fab` |
| `in_universe_source` | Optional; F&B (`book-fab`) edges only. The in-world source of a hedged/partisan claim. Enum: `mushroom` \| `eustace` \| `munkun` \| `orwyle` \| `mellos` \| `gyldayn-synthesis` \| `court-record` \| `unattributed`. Set ONLY when the text hedges or names a partisan source; blank on plain Gyldayn narration. `unattributed` = bare "some say / it is said"; `gyldayn-synthesis` = Gyldayn explicitly weighing named sources. | `mushroom` |
| `disputed` | Optional bool; F&B edges only. `true` when the claim is hedged, single-partisan, or two accounts conflict (each conflicting account emitted as its own edge, each tagged). | `true` |

**Validator invariant:** `disputed: true ⇒ confidence_tier ≤ 2` — reject any tier-1 + disputed row. Same tier-cap pattern as `SUSPECTED_OF` and the staged `occurred.dispute` sub-map. Rationale: F&B is in-universe history compiled by Archmaester Gyldayn from partisan, contradictory sources (Munkun's *True Telling*, Orwyle, Septon Eustace, Mushroom's *Testimony*); uncontested narration is the primary canonical source for 1–136 AC (Tier-1, no POV text exists for that era), but anything hedged/disputed is capped Tier-2. Blanket per-source ceilings were rejected (Fable review §3 #9) — Gyldayn synthesizes, and even Mushroom sometimes reports uncontested fact.

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

**Fire & Blood cite anchors** are section-slug-based, not chapter-number-based: `Rfab<section_slug>` (e.g. `cite_ref-Rfabheirs_of_the_dragon_-_a_question_of_succession`). This is the wiki's own F&B citation prefix — the graph's existing 1,634 `Rfab*`-anchored nodes are the Tier-2 provenance layer the F&B enrichment pass upgrades. Book-cited F&B edges use `evidence_ref: sources/chapters/fab/<unit>.md:LINE` (line-anchored, like all other chapters).

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

**Investigation tooling:** `weirwood query <slug>` — read-only CLI that prints a node's frontmatter, outbound edges (with target-resolution status: OK / ALIAS→ / ORPHAN), and top inbound references from `working/wiki/data/cross-references.jsonl`. Use this before grepping raw markdown when investigating any single node. Modes: default full, `--edges-only`, `--inbound-only`, `--json`.

**Why single-writer-per-file matters:** if two processes (e.g., Python skeleton emitter + LLM prose-fill agent) both wrote to the same file, the LLM's tendency to paraphrase or normalize would corrupt the deterministic prefix. Separating artifacts by writer makes that class of failure structurally impossible. A validator never has to enforce byte-equality; the concatenation is the only path that produces the final node.

---

## Wiki Infobox Fields → Edge Type Mapping

> **Vocabulary lock — read this before adding or renaming any edge type.**
>
> **There are two related vocabularies in this document, and it matters which one you mean.**
>
> 1. **Master edge vocabulary** — the union of all subsections under `## Edge Types (Relationship Categories)` above. Currently **~168 distinct edge types** across 16 categories (kinship, political, factional, military, knowledge, emotional/perceptual, spatial, possession, identity, cultural, narrative, prophecy, evidentiary, causal, temporal, hospitality, magic-and-supernatural). **Session 116 (2026-06-20)**: added `SUSPECTED_OF` (Causal & Plot — unproven actor→event suspicion, capped Tier-2, never asserts the act as fact; first instance `euron-greyjoy SUSPECTED_OF death-of-balon-greyjoy`); vocab 167 → 168. **Session 104 (2026-06-17)**: added `PRECEDES` (new "Temporal & Sequencing" subsection — deterministic in-world event ordering from `occurred.ac_year`; `FOLLOWS` deliberately NOT added, the inverse is read by reverse traversal); vocab 166 → 167. **Session 86 (2026-06-08)**: added `SUB_BEAT_OF` (beat-in-event scope, distinct from `PART_OF`'s event-in-war scope; formalizes the Plate 4 wiki-cluster chapter-beat → parent-event relation); vocab 165 → 166. **Session 83 (2026-06-05)**: added `AGENT_IN` + `VICTIM_IN` (reification role edges for event hubs); vocab 163 → 165. For an authoritative live count, run `scripts/build-edge-type-counts.py` — its `canonical_type_count` is derived from this file. Session 54 (2026-05-15) added `UNCLE_OF`, `NEPHEW_OF`, `KILLED_WITH`, `ATTENDS` after Stage 4 batch-0012 vocab-gap audit. Session 55 first wave (2026-05-16) added `COUSIN_OF`, `MILK_BROTHER_OF`, `NURSED_BY`, `WET_NURSE_OF`, `KNIGHTED_BY`, `BESTOWS_KNIGHTHOOD_ON`, `DEPICTED_IN` after Stage 4 batches 0012-0018 surfaced these recurring patterns. **Session 55 second wave (2026-05-18) — vocab FINAL**: added 17 types (`AFFLICTED_BY`, `DIED_OF`, `COMPANION_OF`, `PARTICIPATES_IN`, `OFFICIATES`, `ATTACKS`, `ASSAULTS`, `COURTS`, `CONTRACTED_WITH`, `PROPOSED_AS_BRIDE`, `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`, `PRACTICES`, `PURCHASED_FROM`, `BUILT`, `CAPTAIN_OF`, `CREW_OF`, `REPUTED_AS`) + 2 description mods (`FIGHTS_IN` extended to "battle, war, or tournament as a combatant"; `MANIPULATES` qualifier-mechanism note). After this wave the classifier prompt flips its gap-filing default to FINAL — vocab-gap questions are no longer filed for remaining batches; non-fitting candidates reject as `no-fitting-type-vocab-locked`. **Session 58 — vocab completeness audit (2026-05-19)**: added 10 types (`SPIES_ON`, `INFORMS`, `NAMED_AFTER`, `STEP_PARENT_OF`, `STEP_CHILD_OF`, `IN_LAW_OF`, `RESCUES`, `BANISHES`, `TORTURES`, `CONSPIRES_WITH`) from vocab-completeness audit of 7,398 P1 rows + 4,207 Stage-4 emits + 135 `no-fitting-type` rejections; vocab 149 → 159. **Session 61 — Stage 4 Haiku residual-resolve patterns (2026-05-19)**: added 5 types (`IMPRISONED_AT`, `TRAVELS_WITH`, `PRISONER_EXCHANGE_FOR`, `GUARDS`, `ENCOUNTERS`) from Stage 4 Haiku residual-resolve surfacing recurring patterns that didn't fit existing vocab; vocab 159 → 164. `ENCOUNTERS` introduces the first **validator-enforced verb gate** (classify-prompt Rule 6) — promotes the prompt-text behavioral constraint pattern (precedent: Rule 2 KNOWS-STOP) to schema enforcement. Normalizer alias `ACCOMPANIES` → `TRAVELS_WITH` added the same session. **Session 63 — KNOWS deprecation (2026-05-21)**: removed `KNOWS` from the active vocabulary (vocab 164 → 163) after Stage 4 overnight run showed 82.3% fallback rate; deferred to a future Pass-1-derived chapter co-occurrence pass. Also added partial-coverage scope-note to `ENCOUNTERS` (wiki-prose register captures only staged meetings, not all real ones). Some types (`FEARS`, `MOURNS`, `IMPERSONATES`, `FORESHADOWS`, `DREAMS_OF`, `WARGS_INTO`, `RESURRECTS`, `MADE_OF`, `LOOTED_BY`, `GIFTED_TO`, etc.) are pre-declared for prose-derived passes and currently have zero instances in the graph — that's expected; they're reserved for Stage 4 classification. This vocabulary is the **single source of truth for every emitter** — Python parsers, Pass-1 mechanical extractor, prose-edge-classifier, voice-analyzer, foreshadowing-scanner, every script, every agent.
> 2. **Wiki infobox subset** — the table below, mapping wiki infobox FIELD names to edge types. Currently **26 distinct edge types**, all of which are also in the master vocabulary. The parser at `scripts/wiki-infobox-parser.py` (`FIELD_EDGE_MAP` dict) implements only this subset, because infobox fields are the only signal it sees. Prose-derived edges are NOT restricted to this subset — they may emit any of the master vocabulary types (including the new Magic & Supernatural subsection added Session 53).
>
> **Why locked:** the graph's value comes from being able to traverse `SPOUSE_OF` everywhere consistently. If one source emits `SPOUSE_OF` and another emits `MARRIED_TO`, traversal breaks. The master edge types were chosen deliberately (curated from infobox-field frequencies + narrative/perception/prophecy needs for later passes, with Magic & Supernatural added Session 53 ahead of Stage 4); expanding the set requires the same deliberation — propose via `curation/edge-vocabulary-candidates.md`, get approval, then update this file + parser + classifier prompt.
>
> **No emitter invents edge types.** Scripts and agents emit ONLY from the master vocabulary. As of the Session 55 second wave (2026-05-18) the vocabulary is **FINAL** for the Stage 4 bulk run — agents that encounter a non-fitting relationship reject it as `no-fitting-type-vocab-locked` rather than filing new `vocabulary-gap` questions. The gap-filing channel (`working/wiki/pass2-buckets/questions-for-matt.jsonl`) is closed for Stage 4 v1; reopen only if a subsequent corpus expansion (cross-book Pass 1 retro, Pass 3 voice/perception passes, etc.) surfaces a recurring pattern that genuinely cannot be expressed in any of the ~159 canonical types.
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
