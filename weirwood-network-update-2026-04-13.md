# Weirwood Network — Project Update: 2026-04-13

**Source:** Conversation between Matt and Claude, capturing scope changes, architectural decisions, new ideas, and a comprehensive datapoint taxonomy for fictional universe analysis.

---

## Session Summary

This session addressed the wiki scraping pivot (Cloudflare → Playwright), the scope expansion from targeted scrape to full corpus acquisition (~18k pages), trust tier revisions, timeline/spoiler field design, and produced an exhaustive taxonomy of datapoints for analysis. The conversation was exploratory and generative — Matt was thinking out loud about what the system could become while staying grounded in what Phase 1 actually requires.

---

## Major Decision Changes

### CHANGED: Wiki Ingestion Scope — Full Scrape, Not Targeted

- **Previous:** Targeted scrape of known entities (characters, locations, houses, events, artifacts from the main five novels). Expand later.
- **New:** Full scrape of entire AWOIAF wiki. ~18,000 pages. No classification at scrape time.
- **Reason:** Cloudflare restrictions on AWOIAF blocked the original Python requests-based scraper. The workaround required Playwright (headless browser) which bypasses Cloudflare but makes selective page targeting impractical at scale. Rather than curate a target list, scrape everything.
- **Status:** Scrape is running on Matt's machine. Estimated 6-8 hours for full acquisition.
- **Output format:** JSON files containing raw HTML per page. Not pretty, but automated and complete.
- **Why this is better:** A targeted scrape would have baked in our assumptions about what's important before we had data to validate those assumptions. The full dump lets the data itself tell us what matters.

### CHANGED: Supplementary Texts Are Tier 1

- **Previous:** Fire & Blood, TWOIAF, Dunk & Egg were implicitly secondary/supplementary.
- **New:** All published GRRM texts — the main five novels, Fire & Blood, The World of Ice and Fire, Dunk & Egg novellas, published sample chapters — are **Tier 1** source material.
- **Reason:** These texts contain essential world-building, history, and character information that the main series references but doesn't fully explain. Many entities that seem like "minor lore" (Targaryen kings, Blackfyre pretenders, historical battles) are actually critical nodes in the knowledge graph.
- **Implication:** Matt owns all of these as ebooks. They need to be split and ingested into the source corpus **before** extraction passes begin, not retrofitted later.

### CHANGED: Trust Tier Model (Revised)

| Tier | Source | Description |
|------|--------|-------------|
| **Tier 1** | Main five novels, Fire & Blood, TWOIAF, Dunk & Egg, published sample chapters | Primary canonical text. The source material itself. |
| **Tier 2** | AWOIAF wiki synthesis | Wiki content that connects dots across multiple Tier 1 sources, or organizes information in ways the source texts don't explicitly state but clearly support. Bulk of the wiki's value lives here. |
| **Tier 3** | Community interpretation, theory content, SSMs (So Spake Martin), convention Q&As | Broadly accepted but not in published text. |

**Important nuance — narrator bias within Tier 1:** TWOIAF is written in-world by Maester Yandel, dedicated to King Robert Baratheon. It has intentional pro-Baratheon, anti-Targaryen bias. Fire & Blood is framed as Archmaester Gyldayn's history, working from conflicting sources (Mushroom vs. Septon Eustace vs. Grand Maester Munkun). Nodes extracted from these texts should carry a `narrator_bias` tag (e.g., `narrator_bias: yandel_pro_baratheon`) to flag that the information is canonical but filtered through an unreliable narrator.

### DECIDED: Spoiler Gate — Deferred, Schema Preserved

- **Decision:** Do not build the spoiler gate system now. Do preserve the schema fields that would enable it later.
- **Reason:** The spoiler gate is a feature, not the foundation. Building it now would be a massive scope expansion (publication order is non-linear across supplementary texts; users may read in different orders; the gate becomes a checklist rather than a slider). The interesting work — the knowledge graph, theory connections, character analysis — doesn't depend on it.
- **Schema requirement:** Every node and edge must still carry `first_available` (which book/chapter introduces this information — publication order) and `timeline_position` (where this sits in in-world chronology). These are cheap to populate during extraction and enable a future spoiler gate without refactoring.
- **Key insight from this session:** `first_available` must track **publication order** (when the reader encounters something), not in-world chronology. Aegon the Conqueror is mentioned in AGOT (1996) but his full story isn't told until Fire & Blood (2018). The spoiler gate cares about the reader's experience, not the fictional calendar.

---

## New Ideas & Insights

### Link Topology from HTML `<a>` Tags

**Origin:** During discussion of what to do with the raw JSON+HTML output from the wiki scrape.

**Insight:** Every internal wiki link (`<a href>` pointing to another AWOIAF page) is a pre-computed edge in the knowledge graph. Before doing any content analysis, we can parse every page's HTML, extract all internal links, and build an adjacency list. This gives us the graph's **topology** — the shape of connections between entities — for free.

**Why this matters:**
- **Hub detection:** Pages with hundreds of inbound links are major entities (Tyrion, King's Landing, Robert's Rebellion). Pages with few inbound links are stubs or minor entries. This is a natural priority ranking for extraction — process the high-connectivity nodes first.
- **Cluster identification:** Groups of pages that heavily cross-link form natural clusters. A cluster of pages all linking to each other around Oldtown reveals a convergence zone without any manual analysis.
- **Classification assistance:** The link graph helps classify unknown pages. A page that links heavily to house pages is probably a character in those houses. A page linked from battle pages is probably a location or combatant.
- **Edge discovery:** The anchor text of links often hints at relationship type. A link to "Cersei Lannister" from Jaime's page with anchor text "his sister" encodes a family relationship.

**Phase:** This should happen in Phase 1 (raw parse), immediately after extracting text content from the HTML. The adjacency list is a foundational artifact that informs all subsequent phases.

### Stub Detection via Link Density

Pages with very few inbound links and minimal content (< 50 words of body text) are stubs. These don't need full extraction passes — they just need to exist as nodes with a name and whatever edges the link graph provides. This keeps the graph complete without wasting extraction compute on one-line entries. The link graph naturally surfaces this: sort pages by inbound link count, and the bottom of the list is your stub tier.

### Narrator Bias as Extractable Metadata

TWOIAF and Fire & Blood have in-world narrators with documented biases. This is a unique metadata dimension that no existing ASOIAF tool tracks. During extraction, nodes sourced from these texts should carry:
- `narrator`: which in-world author wrote this account
- `narrator_bias`: known bias direction (e.g., `pro_baratheon`, `anti_targaryen`, `salacious` for Mushroom)
- `conflicting_accounts`: flag for passages where multiple in-world sources disagree

This enables a future analysis mode: "What does Maester Yandel say about this event vs. what Mushroom claims?" — which is one of the most fun aspects of ASOIAF scholarship.

### Character Voice Profiles for Conversational Mode

The Pass 3 voice/perception extraction (already in the pipeline spec) produces character voice profiles from POV chapter internal monologue. These profiles could power a conversational mode: "Talk to me like you are Jaime Lannister." The corpus for this is every word of Jaime's POV chapters — his dark humor, his obsession with his sword hand, how his thinking about Cersei evolves. This is a compelling demo feature and closer to implementable than it seems — it requires Pass 1 (chapter extractions) and Pass 3 (voice analysis), not the full pipeline.

### Wiki HTML Structural Analysis — Findings from Raw Output Inspection

**Source:** Matt shared sample JSON files from the running Playwright scrape. Analysis of actual output revealed far more exploitable structure than anticipated.

**Output format confirmed:** One JSON file per wiki page. Each file contains three fields:
- `page`: the page title (string)
- `html`: raw HTML content (string)
- `fetched`: scrape date (string, "2026-04-13")

All individual files. This is the simplest possible structure for downstream processing.

**Three page types identified:**

**1. Redirect pages.** Example: "Aegon the Unlikely" → redirects to "Aegon V Targaryen". Detectable by the presence of a `div.redirectMsg` element containing a link to the canonical page. These are NOT junk — they are a free alias table. Every redirect maps an alias to a canonical entity name (`aliases` field in the schema). Estimated 2,000-4,000 of the 18k pages may be redirects. First parse step: split all pages into redirects vs. content pages. Redirects become the alias lookup table.

**2. Stub pages.** Marked by a notice box containing the text "This article or section is a stub." Detectable by content matching or by the stub notice template structure. These pages have minimal body content but may still have infoboxes and navboxes with useful structured data. Example: the Pycelle/Kevan assassination page is flagged as a stub but still has a full infobox and navbox.

**3. Content pages.** Full articles with body text, infoboxes, navboxes, references, and internal links.

**Four exploitable HTML structures per content page:**

**Structure 1: Infoboxes (`table.infobox`)**

Pre-structured entity metadata in consistent key-value format. The wiki uses *multiple infobox templates* that map to different entity subtypes:

| Template | Used For | Key Fields |
|----------|----------|------------|
| `Battlebox` | Military engagements | Conflict, Date, Place, Result, Combatants, Commanders, Strength, Casualties |
| `Attackbox` | Assassinations, raids, plots | Conflict, Date, Place, Result, Orchestrator, Perpetrator, Target, Victims |
| `Character infobox` (TBD) | Characters | House, Titles, Born, Died, Allegiance, etc. |
| `Location infobox` (TBD) | Locations | Region, Type, Ruler, etc. |
| `House infobox` (TBD) | Houses | Seat, Sigil, Words, Lord, etc. |

The template name is identifiable from the parser comments at the bottom of each page's HTML (e.g., `Template:Battlebox`, `Template:Attackbox`). This means the wiki itself tells you what subtype each entity is — you don't have to classify it, the template choice already did it.

**This is free entity subtype classification.** A page using `Battlebox` is a battle. A page using `Attackbox` is an assassination/plot. The infobox template name IS the `entity_subtype` value.

One parser per infobox template can extract structured data from a huge percentage of the wiki without touching body text.

**Structure 2: Navboxes (`table.navbox`)**

Navigation template tables at the bottom of pages. These are curated, hierarchical groupings created by wiki editors that represent pre-built graph clusters. Example: the "Theaters and Campaigns of the War of the Five Kings" navbox organizes every battle by theater (Stark-Lannister, King's Landing, Northern civil war, Ironborn, Stannis, Aegon) in roughly chronological order within each theater.

Navboxes are shared across pages — every War of the Five Kings battle page includes the same navbox. This means:
- The navbox title identifies a named collection/cluster (e.g., "War of the Five Kings")
- The navbox groups identify sub-clusters (e.g., "Ironborn campaigns")
- The links within each group are the member entities of that sub-cluster
- The ordering within groups reflects the wiki editors' understanding of chronological sequence

**These are pre-built convergence maps.** Extract the navbox title + group names + member links, and you have a curated subgraph for free.

Different page types will have different navboxes — character pages might have house navboxes, location pages might have regional navboxes. Each navbox type represents a different organizational axis for the graph.

**Structure 3: Body text `<a>` tags (excluding infoboxes and navboxes)**

Internal links in the article prose. These represent organic relationship edges — the connections the wiki editors made while describing events, characters, and locations. The anchor text often encodes relationship context (e.g., a link to "Cersei Lannister" with anchor text "the queen" on Varys's page).

Parse these separately from infobox and navbox links. Body links represent narrative connections; infobox links represent structured metadata; navbox links represent editorial groupings. All three are valuable but they encode different things.

**Structure 4: References (`ol.references`)**

Citation lists at the bottom of pages that map wiki claims back to specific book chapters. Example from the Torrhen's Square page: references cite ACOK Chapter 46 (Bran VI), ACOK Chapter 56 (Theon V), ASOS Chapter 76 (Jon XI), ADWD Appendix.

This is the bridge between the wiki corpus and the chapter corpus. Each reference provides:
- Book title (A Clash of Kings, A Storm of Swords, etc.)
- Chapter number and POV character
- Optionally, the AWOIAF app/companion reference

These can be parsed to automatically populate `first_available` for wiki-sourced nodes, and to create cross-reference edges between wiki pages and chapter files.

**Additional signals found:**
- `a.new` class (with `redlink=1` in href) indicates pages that are linked but don't exist yet on the wiki. These are "missing nodes" — entities the wiki editors considered important enough to link but that no one has written a page for. Could be useful for identifying gaps.
- `a.mw-selflink` class indicates the current page's own entry in a navbox, confirming which collection the page belongs to.
- Parser cache comments at the bottom of each page include template expansion data that reveals which templates were used (Battlebox, Attackbox, Infobox, etc.) and their processing costs. This is machine-readable metadata about the page's structure.

**Impact on Phase 1 parsing strategy:**

The rich HTML parse step (Phase 1, Step 5) should extract different artifacts per page depending on its type (as classified by the discovery pass). For content/entity pages, extract five artifacts:
1. Page metadata: title, slug, fetched date, page type
2. Infobox data: template type + key-value pairs
3. Navbox data: navbox title + group names + member links
4. Body links: all internal `<a>` tags from body text (excluding infobox/navbox), with anchor text
5. References: parsed citations mapping to book + chapter (with reference ID prefix for trust tier classification)

For redirect pages: extract alias name → canonical page target (these build the alias lookup table).

For year/timeline pages: extract Events/Births/Deaths section content with citations.

For meta/community pages: extract curated content appropriate to the page (e.g., the "Did you know" fact table with its cross-chapter citations).

For stubs: extract whatever structured data exists (infobox and/or navbox if present, body links, references).

Every page type gets parsed — just with a different strategy.

**Structure 5: Section headings as semantic structure (Year pages and similar)**

Year pages (e.g., "39 AC") use a completely different structure from entity pages. No infobox — instead, the body is organized with `Events`, `Births`, `Deaths` headings, each containing lists of what happened that year with citations. The navbox is a `Template:Years` timeline index organized by century, linking every year that has a page.

This is a distinct page type that directly populates `timeline_position` data. Each year page is a pre-built timeline slice: events with dates, character births and deaths with citations back to Fire & Blood, TWOIAF, etc. The years navbox also reveals which years the sources cover in detail — gaps in the navbox (e.g., 13 AC to 37 AC) indicate periods with sparse documentation.

Year pages should be parsed differently from entity pages — extract the section-based Events/Births/Deaths structure rather than looking for infoboxes.

---

## Wiki Discovery Pass — Classify Everything, Delete Nothing

**The discovery pass doesn't filter anything out. It classifies everything and reports what's there.** Every page gets a type label. No page gets deleted or excluded. The point is to understand the shape of the corpus so you know what parsers to build — not to decide what matters.

The discovery pass answers one question: **"What do I have?"**

It scans all 18k JSON files and produces a single report that says: here are the page types I found (redirects, stubs, entity pages with infoboxes, year pages, meta/community pages, consolidated timeline pages, etc.), here's how many of each, here are the templates in use and how many pages use each one, here are the navbox types, here are the reference ID prefix patterns and what sources they map to, here are the section heading patterns, here are the word count distributions, here are the redlinks.

That's it. One pass, one report, no decisions. Every subsequent step reads that report and decides what to do with each page type. The entity parser knows to look for infoboxes. The timeline parser knows to look for Events/Births/Deaths sections. A community page parser could extract those curated cross-chapter connections from the "Did you know" table. The redirect processor builds the alias table. Each parser is purpose-built for the page types the discovery pass identified.

**The discovery pass is the table of contents for the corpus. Each extraction pass is a chapter that reads specific pages using specific strategies. Nothing gets thrown away — it just gets routed to the right parser.**

### What the discovery pass collects:

### 1. Page Type Distribution
- Classify every page into a type: redirect, stub, entity (with infobox), year/timeline, meta/community, consolidated reference, etc.
- Count how many pages fall into each type
- Every page gets a label — no "other" bucket, no exclusions

### 2. Template Census
- Extract every template name from the parser cache comments at the bottom of each page (the `Transclusion expansion time report` block)
- Count how many pages use each template
- This tells you every infobox variant in use (Battlebox, Attackbox, Character, Location, House, etc.) and how many pages use each one — i.e., the entity subtype distribution across the entire wiki

### 3. Navbox Census
- Extract every unique navbox title across all pages
- Count how many pages include each navbox
- This reveals every curated collection the wiki editors have built — wars, house lineages, regions, book chapter lists, year timelines, etc.

### 4. Reference ID Prefix Patterns
- Extract reference IDs from citations across all pages (e.g., `Ragot55`, `Rfab`, `Rssm1467`, `Rhbogots02e05`)
- Map prefixes to source texts: `Ragot` = A Game of Thrones, `Racok` = A Clash of Kings, `Rasos` = A Storm of Swords, `Raffc` = A Feast for Crows, `Radwd` = A Dance with Dragons, `Rfab` = Fire & Blood, `Rtwoiaf` = The World of Ice & Fire, `Rthk` = The Hedge Knight, `Rtmk` = The Mystery Knight, `Rssm` = So Spake Martin, `Rhbogot` = HBO Game of Thrones, `Rawoiaf` = AWOIAF app
- This is a parseable source classification system baked into the citation IDs — every citation on the wiki can be programmatically classified by trust tier from its reference ID prefix alone

### 5. Section Heading Patterns
- For all pages (not just non-infobox pages), what `<h2>` and `<h3>` headings appear?
- Common patterns (Events/Births/Deaths for year pages; Appearance/Personality for character pages; History/Layout for location pages) reveal parseable structure
- Meta/community pages will have unique heading patterns (List of facts, Adding new facts, etc.) that identify them

### 6. Body Content Metrics
- Word count per page (strip HTML, count words)
- This, combined with inbound link count from the adjacency list, gives you the hub/stub ranking

### 7. Redlink Inventory
- Collect all `a.new` (redlink) targets across all pages
- These are entities the wiki considers important enough to reference but that don't have pages — potential nodes that need to exist in the graph as stubs

**Why this matters:** You can't build good parsers for page types you haven't seen yet. The template census alone might reveal 15-20 infobox variants you don't know about. Meta/community pages like "Did you know" contain curated cross-chapter connections that would be lost if you assumed all non-entity pages were junk. Running the discovery pass first means you build parsers for the *actual* data, not for what you assumed was there. It's the same principle as your Snowflake metadata discovery work at Allvue — understand the shape of the data before you try to transform it.

**Output:** A single report file (JSON or markdown) with counts, distributions, and sample page titles for each category. This becomes the reference document for building the parser pipeline. Every page in the corpus appears in this report with its type classification.

---

## Revised Phase 1 Scope

Phase 1 is corpus acquisition and raw processing. No classification, no extraction prompts, no graph construction. Just get the material organized and understood.

### Phase 1 Steps (in order):

1. **Wiki scrape completes** — running now, 6-8 hours, Playwright script on Matt's machine. Output: one JSON file per page (`{page, html, fetched}`).
2. **Wiki discovery pass** — lightweight scan of all 18k pages. Classifies every page by type, runs template census, navbox census, reference ID prefix mapping, section heading patterns, word counts, redlink inventory. Output: a single report file. No pages excluded — every page gets a type label. See "Wiki Discovery Pass" section above.
3. **Chapter splitter: main five novels** — split AGOT, ACOK, ASOS, AFFC, ADWD into per-chapter markdown files with YAML frontmatter (POV character, chapter number, book). Script spec exists in foundation-builder agent prompt.
4. **Chapter splitter: supplementary texts** — split Fire & Blood (by chapter), TWOIAF (by section/region), Dunk & Egg (by novella). Simpler than main novels — no POV tracking, no descriptive title normalization. Matt has these as ebooks.
5. **Rich HTML parse** — process ALL pages according to their type (from the discovery report). Redirects: extract alias → canonical mapping. Entity pages: extract infobox data, navbox data, body links, references. Year pages: extract Events/Births/Deaths structure. Meta/community pages: extract curated content (e.g., "Did you know" cross-chapter connections). Stubs: extract whatever structured data exists (infobox/navbox if present). Each page type gets its own parser strategy. Output: structured data per page.
6. **Link adjacency list** — from the body links + infobox links + navbox links extracted in step 5, build a complete adjacency list. Output: a data structure mapping every page to every page it links to, and vice versa (inbound links). Calculate inbound link counts per page. Keep link source type (body/infobox/navbox) as metadata on each edge.
7. **Hub analysis** — sort pages by inbound link count. Cross-reference with page types and infobox template types from the discovery report. Output: a ranked page list with connectivity metrics, page type, and template classification.

**Phase 1 does NOT include:** entity classification, extraction prompt runs, graph node creation, trigger table construction, theory ingestion, voice analysis, or spoiler gate implementation.

---

## Comprehensive Datapoint Taxonomy

This is the exhaustive list of datapoint types that the Weirwood Network schema should be able to accommodate. Not all of these will be populated in early phases — this is the ceiling of what the system could track, organized to keep work manageable by phase.

### Category 1: Entity Identity & Classification

These are the "what is this thing" fields. Every node in the graph needs these.

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `entity_name` | Canonical name | Jaime Lannister |
| `aliases` | All known names, titles, nicknames | The Kingslayer, Goldenhand, Ser Jaime |
| `entity_type` | Primary classification | Character, Location, House, Event, Artifact, Prophecy |
| `entity_subtype` | Secondary classification | Character → POV / Non-POV / Historical; Location → Castle / City / Region / Body of Water |
| `status` | Current state in the narrative | Alive, Dead, Unknown, Destroyed, Dissolved |
| `first_available` | Publication-order first appearance | AGOT, Bran II |
| `timeline_position` | In-world chronological position | ~281 AC (birth), active 298-300 AC |
| `tier` | Source trust level | Tier 1 (book text), Tier 2 (wiki synthesis), Tier 3 (community) |
| `narrator` | In-world author if applicable | Maester Yandel, Archmaester Gyldayn |
| `narrator_bias` | Known bias of in-world narrator | pro_baratheon, salacious (Mushroom) |
| `wiki_inbound_links` | Count of pages linking to this entity | 347 |
| `wiki_outbound_links` | Count of pages this entity links to | 89 |
| `stub_flag` | Whether this is a minimal-content node | true/false |

### Category 2: Character-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `house_allegiance` | Current and historical house affiliations | Lannister (birth), Kingsguard (sworn) |
| `family_relationships` | Typed family edges | father: Tywin, sister: Cersei, brother: Tyrion |
| `titles_held` | Formal titles with timeframes | Lord Commander of the Kingsguard (298-300 AC) |
| `locations_visited` | Places the character has been, with chapter citations | King's Landing (AGOT-ASOS), Riverlands (ASOS-AFFC) |
| `allegiance_changes` | Shifts in loyalty or faction | Aerys → Robert (281 AC, during rebellion) |
| `kills` | Characters this person has killed | Aerys II Targaryen, Jory Cassel |
| `killed_by` | If dead, who killed them and how | — |
| `pov_chapters` | List of chapters from this character's perspective | ASOS Jaime I–IX, AFFC Jaime I–IV |
| `pov_chapter_count` | Number of POV chapters | 17 |
| `internal_knowledge` | What this character knows at a given point in the narrative | Knows Cersei's children are illegitimate (AGOT) |
| `reader_knows_they_dont` | Dramatic irony — things the reader knows that this character doesn't | Jon's parentage (reader suspects, Jaime doesn't know) |
| `character_arc_phase` | Narrative arc stage per book | AGOT: antagonist; ASOS: protagonist shift; AFFC: redemption |
| `physical_description` | Canonical appearance details | Golden hair, green eyes, lost right hand (ASOS) |
| `weapons` | Named or notable weapons carried | Oathkeeper (Valyrian steel, given by Brienne — originally his) |
| `skills_abilities` | Known competencies | Master swordsman (pre-hand loss), tactical commander |
| `psychological_profile` | Internal drives, fears, obsessions | Obsession with honor/legacy, Cersei dependency, sword hand identity |
| `voice_markers` | Distinctive speech patterns, vocabulary, humor style | Dark ironic humor, self-deprecation post-hand, contempt for hypocrisy |
| `perception_by_others` | How other POV characters see this character | Catelyn: monster; Brienne: honorable; Cersei: extension of herself |

### Category 3: Location-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `region` | Parent geographic region | Westerlands, Crownlands, Beyond the Wall |
| `location_type` | Castle, city, ruin, body of water, road, etc. | Castle |
| `current_holder` | Who controls this location at narrative present | Cersei Lannister (Casterly Rock, disputed) |
| `historical_holders` | Sequence of rulers/owners | Casterlys → Lannisters (Age of Heroes) |
| `notable_events_here` | Events that occurred at this location | Tower of Joy: fight between Ned and Kingsguard (283 AC) |
| `characters_present` | Who is at this location at different points in the narrative | Oldtown: Sam, Jaqen-as-Pate, Marwyn, Leo Tyrell (AFFC-ADWD) |
| `convergence_flag` | Whether multiple unrelated plot threads intersect here | true (Oldtown: Sam + Faceless Men + glass candles + Euron's fleet) |
| `strategic_significance` | Military, political, economic, or magical importance | Controls Sunset Sea trade routes |
| `magical_properties` | Weirwood presence, magical wards, ancient construction | Weirwood heart tree in godswood |
| `physical_description` | Canonical description of the place | — |

### Category 4: House / Faction-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `seat` | Primary castle/holdfast | Casterly Rock |
| `sigil` | Heraldic device | Golden lion on crimson |
| `words` | House words | "Hear Me Roar!" (official), "A Lannister always pays his debts" (unofficial) |
| `current_lord` | Head of house at narrative present | Cersei Lannister (disputed) |
| `lord_succession` | Historical sequence of lords | Tytos → Tywin → Cersei |
| `vassal_houses` | Sworn houses | Clegane, Crakehall, Marbrand, Lefford, etc. |
| `liege_lord` | Who this house is sworn to | The Iron Throne (directly) |
| `alliances` | Political alliances with timeframes | Lannister-Tyrell alliance (ASOS-AFFC) |
| `feuds` | Historical or active conflicts | Lannister-Stark (AGOT-present), Lannister-Reyne (historical) |
| `cadet_branches` | Offshoot houses | Lannister of Lannisport |
| `extinction_risk` | Whether the house's main line is endangered | — |

### Category 5: Event-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `event_type` | Battle, wedding, trial, assassination, coronation, etc. | Battle |
| `timeline_position` | When it happened in-world | 283 AC |
| `location` | Where it happened | The Trident |
| `participants` | Who was involved, with roles | Robert Baratheon (victor), Rhaegar Targaryen (killed) |
| `outcome` | What resulted | Targaryen defeat, Rhaegar killed, royalist army broken |
| `causes` | What led to this event | Lyanna's disappearance, Brandon and Rickard's execution, Aerys's demand for Ned and Robert's heads |
| `consequences` | What this event caused downstream | Fall of King's Landing, end of Targaryen dynasty, Robert's coronation |
| `chapters_covering` | Which chapters describe or reference this event | AGOT Eddard (multiple), ASOS Jaime V (Jaime's account) |
| `conflicting_accounts` | Whether sources disagree on what happened | Tower of Joy: Ned's memory vs. Dayne legend |
| `foreshadowed_by` | Earlier textual hints pointing to this event | — |
| `foreshadows` | Future events this hints at | — |

### Category 6: Artifact / Object-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `artifact_type` | Weapon, book, horn, crown, poison, letter, etc. | Valyrian steel sword |
| `current_holder` | Who has it now | Brienne of Tarth |
| `holder_history` | Sequence of owners | Ice (Stark) → melted → Oathkeeper (Tywin → Jaime → Brienne) |
| `location` | Where it currently is | With Brienne, Riverlands |
| `magical_properties` | Known or suspected magical attributes | Valyrian steel: kills Others, lighter than normal steel |
| `origin` | Where it came from | Reforged from Ned Stark's Ice by Tobho Mott |
| `significance` | Why it matters to the plot | — |
| `prophecy_connection` | Whether connected to any prophecy | Lightbringer candidate? |

### Category 7: Prophecy / Vision-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `source` | Who delivered the prophecy | Maggy the Frog |
| `recipient` | Who received it | Cersei Lannister |
| `text` | Exact wording from the books | (cite chapter, quote key phrases) |
| `interpretation_canonical` | What the text clearly means | Three children, all gold-shrouded |
| `interpretation_speculative` | Community theories about meaning | "Younger and more beautiful" = Daenerys? Sansa? Jaime? Brienne? |
| `fulfillment_status` | How much has come true | Partially fulfilled (children's deaths in progress) |
| `evidence_for` | Textual evidence supporting interpretations | — |
| `evidence_against` | Textual evidence contradicting interpretations | — |
| `connected_prophecies` | Other prophecies that may relate | Azor Ahai, Prince That Was Promised, Stallion Who Mounts the World |

### Category 8: Theory-Specific

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `theory_name` | Common name | R+L=J |
| `confidence_level` | confirmed / near-confirmed / strong / speculative / crackpot | near-confirmed |
| `thesis` | One-sentence summary | Jon Snow is the son of Rhaegar Targaryen and Lyanna Stark |
| `evidence_for` | List of textual evidence with chapter citations | Ned's fever dream (AGOT Eddard X), "Promise me, Ned" |
| `evidence_against` | Counter-evidence | Ned's internal monologue never explicitly states it |
| `first_proposed` | When/where the theory originated | Early internet fandom, pre-ACOK |
| `key_sources` | Notable community analyses | Alt Shift X, Tower of the Hand |
| `implications` | What this means if true | Jon has a claim to the Iron Throne, dragon rider potential |
| `connected_theories` | Theories that depend on or interact with this one | Three heads of the dragon, Jon's resurrection purpose |
| `status` | Active / debunked / confirmed by show / confirmed by text | Confirmed by show, strongly supported by text |

### Category 9: Relationship / Edge-Specific

These are the typed connections between nodes. Every edge in the graph needs these.

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `source_node` | Starting entity | Jaime Lannister |
| `target_node` | Ending entity | Cersei Lannister |
| `relationship_type` | Category of connection | Family, Political, Military, Romantic, Antagonistic, Mentor, Geographic |
| `relationship_subtype` | Specific connection | twin_sibling, lover, co-conspirator |
| `directionality` | Whether the edge is directional | Bidirectional (siblings), Directional (Jaime → Cersei: romantic obsession; Cersei → Jaime: tool/extension) |
| `strength` | How significant the connection is | Primary (defines both characters) |
| `evolution` | How the relationship changes over time | AGOT: codependent; AFFC: Jaime distancing; ADWD: estranged |
| `first_available` | When the reader learns about this connection | AGOT Bran II (Bran witnesses them) |
| `timeline_active` | When this relationship is active in-world | ~276 AC (childhood) – 300 AC (estrangement) |
| `evidence_chapters` | Chapters that develop or reveal this relationship | AGOT Bran II, ASOS Jaime II, AFFC Cersei IV, AFFC Jaime VII |

### Category 10: Thematic / Literary Analysis

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `foreshadowing_source` | Textual moment that hints at a future event | "The things I do for love" (AGOT Bran II) |
| `foreshadowing_target` | The event being foreshadowed | Jaime's eventual break from Cersei |
| `foreshadowing_confidence` | How clearly this is foreshadowing vs. coincidence | Strong — thematic echo |
| `dramatic_irony` | Moments where reader knows more than the character | Reader suspects Jon's parentage; Ned refuses to think about it directly |
| `parallel_characters` | Characters who mirror each other thematically | Jaime / Theon (identity destruction and reconstruction) |
| `parallel_events` | Events that echo or invert each other | Red Wedding / Purple Wedding (subversion of guest right) |
| `motif` | Recurring symbolic element | Hands (Jaime's hand, Hand of the King, Qhorin Halfhand) |
| `thematic_thread` | Big-picture theme this element connects to | Identity, oath vs. honor, power and corruption |
| `chapter_structure_note` | Narrative structure observations | ASOS Jaime chapters alternate with Brienne — their arcs are woven |
| `unreliable_narration_flag` | Whether the POV character's account should be questioned | Cersei's POV chapters: she is consistently wrong about her own competence |
| `subtext` | What a passage implies beyond its surface meaning | — |

### Category 11: Magic & Supernatural Systems

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `magic_system` | Which magical tradition | Warging, R'hllor fire magic, Faceless Men, Glass candles |
| `practitioners` | Who uses this magic | Bran, Bloodraven, Varamyr (warging) |
| `rules_known` | Established rules/limitations | Skinchanging into humans is abomination; second life in an animal at death |
| `rules_speculated` | Community theories about how it works | Weirwood network enables time influence? |
| `artifacts_connected` | Objects tied to this magic system | Weirwood trees, shade of the evening, obsidian candles |
| `geographic_association` | Where this magic is strongest | North of the Wall (warging), Asshai (shadow magic) |
| `cost` | What using this magic costs | Warging: loss of human identity over time; R'hllor: life force (Beric) |

### Category 12: Religion & Culture

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `religion` | Faith system | Faith of the Seven, Old Gods, R'hllor, Drowned God, Many-Faced God |
| `geographic_prevalence` | Where this religion is dominant | Old Gods: the North; Faith of the Seven: south of the Neck |
| `key_figures` | Religious leaders, prophets | High Sparrow, Melisandre, Moqorro, Aeron Greyjoy |
| `institutions` | Organized structures | The Most Devout, the Faith Militant, the Faceless Men |
| `doctrinal_claims` | What the religion teaches | R'hllor: Azor Ahai will be reborn to fight the Great Other |
| `evidence_of_real_power` | Whether this religion's magic demonstrably works | R'hllor: shadow babies, resurrection (yes); Faith of the Seven: (no demonstrated magic) |
| `cultural_practices` | Rituals, customs, taboos | Guest right, trial by combat, the iron price |

### Category 13: Creatures & Species

| Datapoint | Description | Example |
|-----------|-------------|---------|
| `species` | Type of creature | Dragon, Direwolf, Others/White Walkers, Children of the Forest |
| `known_individuals` | Named members | Drogon, Rhaegal, Viserion; Grey Wind, Ghost, Nymeria, Lady, Summer, Shaggydog |
| `bonded_to` | Character bond if applicable | Ghost → Jon Snow |
| `abilities` | Known capabilities | Dragons: fire, flight, war weapon; Others: raise the dead, cold aura, shatter normal steel |
| `vulnerabilities` | Known weaknesses | Others: dragonglass, Valyrian steel; Dragons: scorpion bolts (eyes), dragonbinder horn? |
| `historical_significance` | Role in world history | Dragons enabled Targaryen conquest and maintained dynasty for 150 years |
| `current_status` | Where they are in the narrative | Drogon: ridden by Daenerys, Meereen → ? |
| `extinction_status` | Whether the species is dying out | Dragons: recently returned; Children: nearly extinct; Giants: nearly extinct |

---

## Keeping the Work Manageable: Phased Datapoint Population

The taxonomy above is the **ceiling** — what the system could eventually hold. Not every field gets populated at once. The rule: each extraction pass populates only its own fields. No pass tries to do everything.

### Phase 1 — Corpus Acquisition (Current)
**Populates:** Nothing in the taxonomy. Phase 1 produces raw source material and the link adjacency list. No nodes, no edges, no extraction.

### Phase 2 — Mechanical Extraction (Pass 1)
**Populates from chapters:** `entity_name`, `aliases`, `entity_type`, `entity_subtype`, `status`, `first_available`, `family_relationships` (stated), `locations_visited`, `kills`, `physical_description`, `weapons`, event nodes with `participants`, `outcome`, `location`. Basically everything that's directly stated in the text without interpretation.

### Phase 3 — Wiki Enrichment (Pass 2)
**Populates from wiki:** `timeline_position`, `wiki_inbound_links`, `wiki_outbound_links`, `stub_flag`, `historical_holders`, `vassal_houses`, `sigil`, `words`, `lord_succession`, `holder_history` for artifacts. Cross-references against Pass 1 output. Adds the `tier` and `narrator`/`narrator_bias` fields for wiki-sourced content.

### Phase 4 — Voice & Perception (Pass 3)
**Populates:** `voice_markers`, `psychological_profile`, `perception_by_others`, `character_arc_phase`, `unreliable_narration_flag`. Requires full POV character arcs from Pass 1 as input.

### Phase 5 — Foreshadowing & Literary (Pass 4)
**Populates:** `foreshadowing_source`, `foreshadowing_target`, `foreshadowing_confidence`, `dramatic_irony`, `parallel_characters`, `parallel_events`, `motif`, `thematic_thread`. Requires Passes 1-3 as input.

### Phase 6 — Theory Integration (Pass 5)
**Populates:** All Category 8 fields (theory nodes). `evidence_for`, `evidence_against`, `connected_theories`, `implications`. Requires community source ingestion (Alt Shift X, Poor Quentyn, etc.) plus all prior passes.

### Phase 7+ — Discovery & Expansion
**Populates:** `subtext`, new relationship types, new entity types surfaced by analysis, `convergence_flag` refinements. This is where the system starts finding things we didn't know to look for.

---

## Edge Accumulation Model

Edges are the most important part of the knowledge graph — nodes without edges are just a database of facts. The connections are what make it a *knowledge graph*. Edges accumulate across every pass in the pipeline, with each pass adding a different type of connection.

### Edge Sources by Phase

**Phase 1 — From Wiki HTML (no LLM needed):**
- **Untyped link edges:** Every internal `<a>` tag is an edge from page A to page B. No relationship type — just "this page references that page." These form the raw adjacency list.
- **Typed infobox edges:** Infobox fields encode specific relationship types. Battlebox: Combatants, Commanders, Casualties. Attackbox: Orchestrator, Perpetrator, Target, Victims. Character infobox: House, Allegiance, Spouse. These are pre-classified relationships.
- **Grouping edges:** Navbox membership. "These entities all belong to the War of the Five Kings → Ironborn campaigns." Shared navbox membership implies thematic or categorical connection.
- **Source edges:** Reference citations map wiki claims to specific book chapters. This bridges the wiki corpus to the chapter corpus.

**Phase 2 — From Mechanical Extraction (Pass 1, LLM-assisted):**
- **Co-occurrence edges:** Characters present in the same chapter.
- **Family edges:** Relationships stated in text (father, sister, wife).
- **Geographic edges:** Character → Location (visited, lives at, traveled to).
- **Possession edges:** Character → Artifact (carries, owns, received).
- **Event participation edges:** Character → Event (fought in, witnessed, caused).
- **Information edges:** Character learns X in this chapter (feeds spoiler gate).

**Phase 3 — From Voice & Perception (Pass 3):**
- **Perception edges (directional):** How one POV character sees another. Catelyn → Jaime: sees him as a monster. Brienne → Jaime: sees him as honorable. These are one-directional — Catelyn's perception of Jaime is not Jaime's perception of Catelyn.

**Phase 4 — From Foreshadowing (Pass 4):**
- **Foreshadowing edges (temporal):** Textual moment A hints at future event B. "The things I do for love" → Jaime's eventual break from Cersei.

**Phase 5 — From Theory Integration (Pass 5):**
- **Evidence edges:** Textual passage → Theory it supports.
- **Counter-evidence edges:** Textual passage → Theory it contradicts.
- **Theory dependency edges:** Theory A depends on Theory B being true.

**Phase 6+ — From Discovery:**
- **Parallel edges:** Character A mirrors Character B thematically.
- **Subtext edges:** Surface meaning → Implied meaning.
- **New relationship types** surfaced by pattern analysis.

### Edge Schema

Every edge in the graph carries:

| Field | Description | Example |
|-------|-------------|---------|
| `source_node` | Starting entity | Jaime Lannister |
| `target_node` | Ending entity | Cersei Lannister |
| `relationship_type` | Category | Family, Perception, Foreshadowing, Evidence |
| `relationship_subtype` | Specific connection | twin_sibling, lover, co-conspirator |
| `directionality` | One-way or bidirectional | Perception edges are directional; family edges are bidirectional |
| `source_pass` | Which extraction pass created this edge | wiki_html, pass_1_mechanical, pass_3_voice |
| `evidence_chapter` | Chapter citation supporting this edge | AGOT Bran II |
| `trust_tier` | Provenance tier of the source | Tier 1, Tier 2, Tier 3 |
| `first_available` | When the reader learns about this connection | AGOT Bran II |
| `confidence` | How certain we are this edge is correct | high / medium / low |

### Key Principle: Edges Accumulate, They Don't Replace

A later pass never overwrites an earlier pass's edges. Pass 1 records "Jaime is present in King's Landing." Pass 3 adds "Jaime perceives Cersei as an extension of himself." Pass 4 adds "Jaime's internal monologue here foreshadows his later rejection of her." These are three different edges between the same two nodes, each from a different pass, each encoding a different kind of connection. The graph gets richer with every pass without any pass trying to capture everything.

---

## Trust & Provenance — Industry Context

Research into how knowledge graphs handle trust in 2025-2026 reveals several patterns that validate and inform the Weirwood Network's approach:

### Provenance Tracking (W3C PROV-O)
The standard approach: every fact carries metadata about where it came from, when it was extracted, and how it was verified. The W3C PROV-O ontology formalizes this. The Weirwood Network's `tier`, `narrator`, `first_available`, and `evidence_chapter` fields are provenance tracking — we just didn't use the formal vocabulary.

### Confidence Scoring
Industry practice: facts get confidence scores, and when conflicting information appears, the system adjusts trust in the sources. Sources that consistently provide correct information gain trust; sources that provide erroneous information lose it. This is a dynamic trust model — relevant for the Allvue compliance use case (where data freshness matters) but probably overkill for ASOIAF (where the source texts don't change).

### Reification — Statements About Statements
This is the concept that solves the Cersei problem. Instead of storing "Cersei is brilliant" as a flat fact, you store the *claim* that Cersei believes she's brilliant, with metadata about who asserted it, when, what the confidence is, and what source it came from. RDF 1.2 (published 2024) introduced quoted triple syntax that lets you annotate an annotation — creating arbitrarily deep metadata about any fact's reliability.

For the Weirwood Network, reification means the schema can represent:
- "Cersei believes she is Tywin's true heir" (claim, source: AFFC Cersei III, claim_type: character_belief)
- "This belief is contradicted by outcomes" (meta-claim, source: cross-POV analysis, added in later pass)
- "Mushroom claims X happened" (claim, source: Fire & Blood, narrator_bias: salacious)
- "Septon Eustace contradicts Mushroom's account" (conflicting claim, same event, different narrator)

All of these coexist in the graph. No fact gets deleted — they get annotated with context about reliability.

### KOS Protocol (April 2026)
A brand-new open standard for publishing machine-readable, provenance-tracked knowledge. Notable for its freshness decay formula: reliability degrades over time using exponential decay. A concept barely decays but an event expires in days. Not directly applicable to ASOIAF (the books don't change) but highly relevant to the Allvue compliance use case where data freshness is critical.

### KG-RAG Calibration (Ca2KG, January 2026)
Research showing that AI models using knowledge graph retrieval-augmented generation are often severely overconfident — producing high-confidence predictions even when retrieved subgraphs are incomplete or unreliable. The Ca2KG framework uses counterfactual prompting to expose uncertainties. This is directly relevant to the Weirwood Network's chat experience: the system should be able to say "I'm confident about this connection but uncertain about that one" based on the provenance and confidence metadata in the graph.

### Implications for the Weirwood Network

The trust model should be:
1. **Static provenance at extraction time** — every fact tagged with source, chapter, narrator, tier. This is non-negotiable and already in the schema.
2. **Confidence scoring at extraction time** — high/medium/low based on source type and corroboration. Simple to implement.
3. **Reification for contested/belief claims** — store claims as first-class objects with metadata, not as flat facts. This is the open design question from the reliability framework section.
4. **Dynamic trust adjustment deferred** — relevant for Allvue, not needed for ASOIAF in early phases. The schema should support it (confidence scores can be updated) but the mechanism for updating them is a later problem.

---

## Multi-Agent Orchestration

Multi-agent orchestration applies at three layers of the Weirwood Network and extends to the Allvue compliance use case.

### Layer 1: Building the Knowledge Graph (Extraction Pipeline)

The extraction pipeline is designed as sequential passes, but within each pass, work can be parallelized:

**Pass 1 (Mechanical Extraction):** Embarrassingly parallel by chapter. Each of the 300+ chapters is independent. An orchestrator agent manages the queue: assigns chapters to worker agents, monitors for schema compliance failures, aggregates results. 10 agents can process 10 chapters simultaneously.

**Wiki parsing:** Parallel by page type. The discovery report tells the orchestrator the distribution — assign entity pages to one worker pool, year pages to another, community pages to another. Each pool uses type-specific parsers.

**Pass 3 (Voice/Perception):** Parallelizes by *character*, not by chapter. One agent gets all Jaime chapters, another gets all Cersei chapters, another gets all Tyrion chapters. Different parallelization axis than Pass 1. The orchestrator must know the dependency: Pass 3 requires Pass 1 output as input.

**The orchestrator's job:** Know which passes can run in parallel, which have dependencies, and how to partition work within each pass. This is the same problem as a build system (Make/Gradle) — dependency graph management with LLM agents as workers instead of compilers.

### Layer 2: Querying the Knowledge Graph (Chat Experience)

A single agent answering "what's converging on Oldtown and why does it matter" has to traverse the graph, pull chapter evidence, assess theories, and compose a response. That's a lot of reasoning for one context window.

Multi-agent decomposition:

- **Router agent:** Reads the query, decides what's needed, dispatches to specialists. Hot memory: trigger table, entity type index.
- **Graph traversal agent:** Finds relevant nodes and edges. Follows connections, identifies clusters. Hot memory: adjacency list, hub ranking.
- **Citation agent:** Pulls specific chapter passages supporting each connection. Hot memory: chapter index, reference mappings.
- **Theory agent:** Checks whether established theories touch these nodes. Hot memory: theory index, evidence chains.
- **Synthesis agent:** Takes all specialist outputs, composes the final answer. Applies spoiler gate if active. No domain-specific hot memory — its input is the other agents' outputs.

Each specialist agent has a focused context window with only the memory it needs. The Harness pattern defines what each agent loads — trigger table routes the query, hot/warm/cold tiers determine what each specialist sees.

**This is how you operationalize the Harness at scale.** Multi-agent orchestration isn't a separate concept from the Harness — it's the execution layer. The Harness tells each agent what to know. The orchestration framework tells them how to collaborate.

### Layer 3: Allvue Compliance (Approval Workflow)

A trade comes in. The orchestrator spawns specialist agents:

- **Rules agent:** Checks the trade against the fund's compliance rules (concentration limits, restricted lists, investment guidelines). Context: fund rule set + current portfolio state. Output: pass/fail/warning per rule.
- **Context agent:** Pulls relevant background (issuer news, counterparty credit rating changes, related pending trades). Context: external data sources + internal history. Output: "things the approver should know."
- **Risk agent:** Assesses portfolio-level impact (sector concentration change, duration impact, credit quality distribution). Context: portfolio analytics. Output: risk metrics.
- **Synthesis agent:** Assembles the approval package from all three specialist outputs. Output: "This trade passes all automated checks. Here's the risk impact. Here are two things worth noting before you approve."

The human sees one clean output and says "approve" or "hold."

### The Common Thread

Across all three layers, multi-agent orchestration solves the same problem: **no single agent can hold everything it needs in one context window.** You decompose by specialty, give each agent only the context it needs (via the Harness's hot/warm/cold memory), and have an orchestrator that knows how to assemble their outputs. The Harness is the context management layer. Multi-agent orchestration is the execution layer. They're complementary.

---

## Open Questions (New or Updated)

### NEW: Output Structure of Playwright Scraper
- **Status:** RESOLVED — confirmed from live samples. One JSON file per page with `{page, html, fetched}` structure.

### NEW: Reliability & Epistemology Framework — Needs Thinking

**This is a hard problem that needs more thought before committing to a schema.**

The trust tier model (Tier 1/2/3) handles *where* information comes from. But it doesn't handle *how reliable the information is within its own source*. ASOIAF is built on unreliable narration, contested history, character self-deception, and deliberate lies. The knowledge graph needs to represent this, but the approach is not obvious.

**The core tension:** A character's belief is a textual fact even when the belief is wrong. Cersei genuinely believes she's Tywin's true heir and the smartest person in the room. That belief is a Tier 1 fact — it's right there in her POV chapters. But the *content* of the belief is wrong, which the reader can infer from the gap between what Cersei thinks will happen and what actually happens. The graph needs to record "Cersei believes X" without the extraction pass making a judgment call about whether X is true — because that judgment requires cross-referencing multiple POVs and events, which is interpretive work for a later pass.

**Dimensions that need to be captured (eventually):**

- **Source reliability:** How trustworthy is the narrator/speaker? Ned: high. Cersei's self-assessment: low. Mushroom: entertaining but unreliable. Yandel: biased but factually careful within his bias. *But — "low reliability" on Cersei's self-assessment is a reader-level conclusion, not something the text states. Who decides this, and when?*

- **Claim type:** Is this a directly observed event, a reported secondhand account, a character's opinion/belief, a stated claim by another character, or a known lie? Bran falling is observed. Robert's Rebellion backstory is reported. Cersei thinking she's brilliant is a belief. Littlefinger telling Ned the dagger belonged to Tyrion is a confirmed lie (confirmed later by Littlefinger himself).

- **Corroboration:** Is this fact confirmed by multiple independent sources? What happened at the Tower of Joy rests almost entirely on Ned's fever dream. Jon Arryn's death is confirmed across multiple POVs.

- **Contested flag:** Do sources actively disagree? Rhaegar and Lyanna — abduction or elopement? Different characters state different versions as fact. The wiki presents both versions. The books never fully resolve it (in published text).

- **Character perspective vs. reader perspective:** Cersei *believes* she's brilliant. The reader can see she's not. Both are "true" at different levels. The extraction needs to preserve the character's perspective without endorsing or correcting it — that analysis is for later passes.

**What the mechanical extraction (Pass 1) should do:**
- Record what is stated and by whom: "Cersei believes X. Source: AFFC Cersei III."
- Record what is observed: "Bran falls from tower. Source: AGOT Bran I."
- Record what characters claim: "Littlefinger claims dagger is Tyrion's. Source: AGOT Catelyn IV."
- Do NOT assess whether beliefs are correct, claims are truthful, or narrators are reliable. That's interpretive.

**What later passes should do:**
- Cross-reference claims against outcomes (Cersei's plans vs. what actually happens)
- Identify confirmed lies (claims later revealed to be false by the same or another source)
- Flag contested events where sources disagree
- Build character reliability profiles from the pattern of correct/incorrect beliefs and claims

**Open design questions:**
- Where does reliability assessment happen in the pass sequence? It requires cross-POV comparison, which means at minimum Pass 3 (voice/perception) input. Possibly its own dedicated pass.
- How do you represent "Cersei believes X" in the schema without implying X is true? Is it an edge from Cersei to the claim with `claim_type: belief`? Or a property on the claim node itself?
- Can reliability scoring be partially automated (compare stated predictions against known outcomes), or does it require human/LLM judgment?
- How does this interact with the theory layer? A theory is essentially a reader-level reliability assessment: "I think Littlefinger is lying about X because of evidence Y and Z."

**Decision:** Defer the schema design for reliability. Capture the *raw material* (who said what, who believes what) during mechanical extraction. Build the reliability/epistemology framework as a later pass once there's enough cross-referenced data to work with. But keep this document as the reference for what the framework needs to eventually handle.

### NEW: Pre-Conquest Timeline Structure
- **Observation:** Pre-Conquest dates (e.g., "12000 BC") redirect to section anchors within a consolidated "Years before Aegon's Conquest" page, rather than having individual year pages like post-Conquest dates do.
- **Implication:** Different parsing strategy needed for pre-Conquest vs. post-Conquest timeline data. The discovery pass should catalog both patterns.

### NEW: Supplementary Text Splitting Strategy
- **Question:** What's the natural unit for splitting Fire & Blood, TWOIAF, and Dunk & Egg?
- **Leaning:** Fire & Blood by chapter, TWOIAF by section/region (it's organized topically), Dunk & Egg by individual novella.
- **Note:** These are simpler than the main novels — no POV character tracking, no descriptive title normalization.

### NEW: Ebook Formats for Supplementary Texts
- **Question:** What format are Matt's Fire & Blood, TWOIAF, and Dunk & Egg files?
- **Action:** Matt to confirm (epub, pdf, txt) before splitter scripts are written.

### UPDATED: Storage Format — Pure Markdown vs. Graph DB
- **Previous leaning:** Pure markdown.
- **New consideration:** With 18k wiki pages plus chapter extractions, the link adjacency list alone could be massive. Markdown-as-graph may hit practical limits for traversal queries. The link topology analysis (hub detection, cluster identification, path finding) might justify a lightweight graph DB sooner than expected.
- **Suggestion:** Start with markdown + a JSON adjacency list. If traversal queries become painful, migrate to Neo4j or SQLite with recursive CTEs.

### UPDATED: TV Show Content
- **Decision:** The TV show is explicitly NOT Tier 1 knowledge. Especially from season 5 onward where it diverges from source material. Show-confirmed theories (like R+L=J) can be noted in the theory node's `status` field as "confirmed by show" but this does not make them confirmed-by-text.

---

## Worklog Entry

### 2026-04-13 — Scope Expansion & Datapoint Taxonomy Session

**What happened:**
- Wiki scrape pivot documented: Python requests blocked by Cloudflare → Playwright headless browser workaround. Full scrape running (~18k pages, 6-8 hours). CLI required `--skip-all-permissions` flag.
- Output format confirmed from live samples: one JSON file per page with `{page, html, fetched}` structure.
- Three page types identified: redirects (free alias table), stubs (minimal content but may have infoboxes), content pages (full articles).
- HTML structural analysis of sample pages revealed four exploitable structures: infoboxes (typed by template — Battlebox, Attackbox, etc., providing free entity subtype classification), navboxes (curated hierarchical groupings = pre-built subgraphs), body links (organic relationship edges with anchor text context), and references (chapter citations bridging wiki to book corpus).
- Key discovery: wiki infobox template types (visible in parser comments) ARE entity subtype classifiers. A page using `Battlebox` is a battle; `Attackbox` is an assassination/plot. The wiki editors did the classification work for us.
- Scope expanded from targeted wiki scrape to full corpus acquisition.
- Supplementary texts (Fire & Blood, TWOIAF, Dunk & Egg) elevated to Tier 1. Must be ingested before extraction passes.
- Trust tier model revised (3 tiers + narrator bias metadata).
- Spoiler gate deferred as a feature; schema fields (`first_available`, `timeline_position`) preserved for future implementation. Key insight: `first_available` must track publication order, not in-world chronology.
- Link topology insight: `<a>` tags in wiki HTML are pre-computed graph edges. Adjacency list extraction added to Phase 1.
- Comprehensive datapoint taxonomy produced (13 categories, 100+ field definitions) covering entity identity, characters, locations, houses, events, artifacts, prophecies, theories, relationships, literary analysis, magic systems, religion/culture, and creatures/species.
- Phased population plan: each extraction pass only populates its own fields, preventing scope creep within individual passes.
- Character voice/conversational mode confirmed as downstream feature (requires Pass 1 + Pass 3, not full pipeline).
- Phase 1 steps revised from 6 to 8, adding redirect/stub triage, wiki discovery pass (template census, navbox census, section heading patterns, redlink inventory), and expanding raw parse to extract five artifacts per page.
- Year pages identified as a distinct page type — structured with Events/Births/Deaths sections and a Template:Years timeline navbox organized by century. Direct source for `timeline_position` data.
- Discovery pass concept formalized: before building parsers, run a lightweight catalog scan of all 18k pages to understand what templates, navboxes, section patterns, and page types actually exist. Same principle as Snowflake metadata discovery — understand the shape of the data before transforming it.
- Reliability/epistemology framework identified as a hard open problem. Trust tiers handle where information comes from, but ASOIAF's unreliable narration, character self-deception, contested history, and deliberate lies require a separate reliability dimension. Key insight: a character's belief is a textual fact even when the belief is wrong — Cersei believing she's brilliant is Tier 1 data, but the content of that belief is incorrect. Mechanical extraction should record "who said/believes what" without judging reliability; reliability assessment is a later-pass problem requiring cross-POV comparison. Deferred for schema design, but raw material capture preserved.
- Pre-Conquest timeline structure identified: dates like "12000 BC" redirect to section anchors within a consolidated page, unlike post-Conquest individual year pages. Different parsing strategy needed.
- Meta/community pages identified as a distinct page type with unique value: the "Did you know" page contains 147 hand-curated cross-chapter connections with full citations — exactly the kind of data the knowledge graph needs. These pages are NOT junk to be filtered out.
- Reference ID prefix pattern discovered: wiki citation IDs use consistent prefixes that map to source texts (`Ragot` = AGOT, `Rfab` = Fire & Blood, `Rssm` = So Spake Martin, `Rhbogot` = HBO show, etc.). This enables programmatic trust tier classification of every citation on the wiki from the reference ID alone. Added to discovery pass checklist.
- Critical correction: discovery pass language changed from "filter" and "triage" to "classify and route." The discovery pass classifies every page and reports what's there. No pages are deleted or excluded. Each page type gets routed to the appropriate parser strategy. The principle: the discovery pass is the table of contents for the corpus, each extraction pass is a chapter.
- Phase 1 steps revised: removed "redirect/stub triage" as a separate step, merged discovery pass to step 2 (immediately after scrape), rich HTML parse (step 5) now processes ALL page types with type-appropriate strategies.

**What's next:**
- Wait for wiki scrape to complete
- Inspect output format (one JSON per page vs. batched)
- Confirm ebook formats for supplementary texts
- Build chapter splitter for main five novels
- Build chapter splitter for supplementary texts
- Build raw HTML parser + link adjacency list extractor
