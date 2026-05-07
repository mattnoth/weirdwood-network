# Session 2 — Foundation Builder: Chapter Splitter + Wiki Scraper

**Date:** 2026-04-13

---

## What Triggered This Session

The directory skeleton was in place, the safety rails were installed, but the project had no tooling and no processed data. The extraction pipeline couldn't start until source texts were split into per-chapter files. The wiki reference layer couldn't exist until there was a scraper. This session was about building the two foundational scripts that everything else depends on.

## What Happened

### Chapter Splitter

The first script built was `scripts/chapter-splitter.py`, delegated to the script-builder subagent. Its job: take a raw .txt file of an ASOIAF novel and split it into individual chapter files, one per chapter, with YAML frontmatter containing metadata (book, POV character, chapter number, chapter title).

The core engineering challenge was detecting chapter boundaries. GRRM's chapter headings are not uniform:

- Most chapters use ALL-CAPS character names: `EDDARD`, `CATELYN`, `TYRION`
- Prologues and epilogues: `PROLOGUE`, `EPILOGUE`
- AFFC and ADWD use descriptive titles: `THE PROPHET`, `THE SOILED KNIGHT`, `THE QUEENSMAKER`
- Some headings have special characters or unusual spacing

A gap-based approach (looking for blank lines between chunks of text) would be fragile — GRRM's text has plenty of section breaks within chapters. Instead, the splitter uses a **prose-detection heuristic**: it identifies lines that match chapter heading patterns (known POV names, known descriptive titles, PROLOGUE/EPILOGUE) and treats them as split points. The heading itself becomes the chapter title; the POV character is looked up from a reference table.

The `real_identity` mapping from Session 0's architecture was implemented here: descriptive titles like "THE PROPHET" are preserved in the filename and title field, with a `real_identity` field in the frontmatter linking to "Aeron Greyjoy."

### Running the Splitter: 344 Chapters, All Correct

The splitter was run against all five novels. Results:

| Book | Expected | Actual | Status |
|------|----------|--------|--------|
| AGOT | 73 | 73 | Match |
| ACOK | 70 | 70 | Match |
| ASOS | 82 | 82 | Match |
| AFFC | 46 | 46 | Match |
| ADWD | 73 | 73 | Match |
| **Total** | **344** | **344** | **All match** |

Every book split correctly on the first run. This is worth noting because the problem has real complexity — 344 chapters across 5 books, with varied heading formats, and the splitter had to handle all of them without manual intervention. The prose-detection heuristic proved robust across GRRM's full range of chapter naming conventions.

During the run, 6 missing chapter headings were discovered in `reference/pov-characters.md` — the reference table that maps chapter titles to POV characters. These were added: headings that the splitter encountered in the text but couldn't resolve. This kind of discovery — the tool finding gaps in the reference data — is exactly why you run the tool rather than trying to enumerate everything manually.

### Wiki Scraper

The second script was `scripts/wiki-scraper.py`, also delegated to the script-builder subagent. At 1,213 lines, it was a substantially larger piece of work than the chapter splitter.

The scraper targets the AWOIAF (A Wiki of Ice and Fire) MediaWiki instance. It operates in multiple modes:
- **Entity mode** — scrape a specific page by name
- **Category mode** — scrape all pages in a wiki category
- **All mode** — scrape the entire wiki (added in Session 3)

For each page, the scraper:
1. Fetches the page HTML via the MediaWiki API
2. Parses the infobox (structured sidebar data: aliases, titles, allegiance, family, book appearances)
3. Extracts the full article text, cleaned of wiki markup
4. Classifies the page into an entity type (character, location, house, event, artifact)
5. Writes a structured markdown file to the appropriate `sources/wiki/` subdirectory
6. Caches the raw HTML/JSON to `sources/wiki/_raw/` for reprocessing

A key design constraint: **stdlib-only, no pip dependencies**. The scraper uses only Python's standard library (`urllib`, `html.parser`, `json`, `re`). This was deliberate — the project runs on Matt's local machine with Claude Code, and adding dependency management (virtualenvs, requirements.txt, pip) was unnecessary complexity for a single-purpose scraping tool.

### Wiki Directory Structure

The wiki output directory was created with a classification scheme:
- `sources/wiki/characters/`
- `sources/wiki/locations/`
- `sources/wiki/houses/`
- `sources/wiki/events/`
- `sources/wiki/artifacts/`
- `sources/wiki/_uncategorized/` — pages that don't fit the above categories
- `sources/wiki/_raw/` — cached raw API responses

A taxonomy candidates template was also created at `working/taxonomy-candidates.md` — a place to collect wiki categories that might map to entity types not yet in the schema. This would eventually feed into the entity type hierarchy expansion in Session 8.

### The Cloudflare Wall

The session ended on a blocker: the wiki scraper couldn't actually reach AWOIAF. Cloudflare's bot protection was rejecting all requests from `urllib`. The scraper code was correct — it parsed test HTML perfectly — but it couldn't get past the front door.

This was noted as a blocker and deferred. The solution (migrating to Playwright browser automation) would come in Session 4.

## Key Decisions and Why

| Decision | Reasoning |
|----------|-----------|
| Prose-detection heuristic over gap-based splitting | GRRM's text has section breaks within chapters; gaps are unreliable. Pattern-matching against known heading formats is deterministic. |
| stdlib-only wiki scraper | No dependency management overhead. Python's standard library has everything needed for HTTP requests and HTML parsing. If Cloudflare hadn't intervened, this would have been sufficient. |
| Full article text extraction, not just infoboxes | The wiki's prose contains relationship information, historical context, and cross-references that structured infobox fields don't capture. Extracting both gives the wiki ingestion pass (Pass 2) maximum material to work with. |
| Classification at scrape time | Sorting pages into entity-type directories during scraping means the cache is pre-organized for downstream processing. Pages that don't classify cleanly go to `_uncategorized/` for later triage. |

## What Was Left Open

- Wiki scraper was blocked on Cloudflare — functional code but no way to reach the target
- The Dunk and Egg novellas (The Hedge Knight, The Sworn Sword, The Mystery Knight) were also split during this session, though the archive entry doesn't mention the count — they use a different chapter structure than the main novels
- The mechanical extractor prompt hadn't been tested against actual chapter files yet — that would happen in a later session
- The wiki classification scheme was provisional — the five categories (characters, locations, houses, events, artifacts) were a starting point, not a final taxonomy. The `_uncategorized/` directory was explicitly designed as a catch-all for the long tail
