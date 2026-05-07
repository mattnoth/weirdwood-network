# Worklog Archive — Sessions 5–7

> Archived 2026-04-24. These sessions cover wiki crawl execution, D&E/TWOIAF integration, and mechanical extraction schema v2.

---

### Session 7 — Mechanical Extraction Schema v2 + Tooling (2026-04-22)
**What happened:**
- Reviewed all 73 AGOT v1 extractions for quality and coverage gaps
- Identified physical vector gaps: character appearances, food/drink, hospitality, location descriptions, spatial layout, weather/environment, time markers
- Updated mechanical-extractor agent prompt (`.claude/agents/mechanical-extractor.md`) with 6 new schema sections:
  - **Physical Environment** — weather, season, time of day, lighting, sounds, smells
  - **Character Appearances** — hair, eyes, build, scars, clothing, weapons, age (per-chapter, not assumed)
  - **Food & Drink** — dishes, ingredients, who eats with whom, preparation details
  - **Hospitality & Guest Right** — bread and salt, guest right, violations, shelter offered/denied
  - **Location Descriptions** — defensive features, architecture, interiors, scale, condition, terrain
  - **Spatial Layout & Movement** — phase-based scene graph with controlled vocabulary (Advance, Ambush, Assembly, etc.)
- Added `time_markers` field to Chapter Metadata
- Added direwolves and dragons as characters rule (Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, Viserion)
- Changed extraction philosophy from "leave empty if N/A" to "be expansive, never invent" — variance between runs is a feature
- Archived AGOT v1 extractions to `extractions/archives/agot-v1/` for comparison
- Updated `scripts/run-extraction-wave.sh` to take book as first argument, auto-discover chapters from directory
- Created `scripts/launch-extraction.sh` — opens N iTerm2 tabs and distributes waves automatically
- Created `weirwood-mechanical` shell function in `terminal-collection/functions/` for easy launching
- Created extraction runbook at `working/runbooks/extraction-pass1.md`
- Added orchestration rules to CLAUDE.md: agent prompt ↔ architecture.md sync rule, worklog archival rule
- Archived Sessions 0–4 to `history/worklog-archives/archive001.md` to reduce context load
- Updated `working/todos.md` with timeline reconstruction and direwolves/dragons items

**Key decisions made:**
- Food and Hospitality are separate concerns: food is GRRM's detailed descriptions (queryable data), hospitality is the moral/narrative framework (guest right, violations)
- Physical character descriptions need to be granular enough for cross-identity matching (Jaqen/Alchemist use case)
- Spatial Layout phases are directed-graph edges (Advance, Ambush, etc.) — mini scene graphs per chapter
- Extraction runs use Opus for quality; 4 iTerm2 terminals with 5-chapter waves
- v1 extractions preserved in archives for schema progression comparison

**What's next:**
- AGOT v2 extraction run in progress (launched via `weirwood-mechanical agot 4`)
- Compare v1 vs v2 output quality on key chapters
- Update `reference/architecture.md` to reflect new extraction schema sections (sync rule)
- Begin ACOK extraction once AGOT v2 is validated

---

### Session 6 — Book Integration: Dunk & Egg + TWOIAF (2026-04-16)
**What happened:**
- Followed runbook at `working/runbooks/book-integration.md` to integrate two new source artifacts.
- **Dunk & Egg (D&E):**
  - Converted `The Tales of Dunk & Egg.epub` to plaintext via Calibre `ebook-convert` → `sources/raw/TDAE.txt`
  - Structure deviated from runbook expectations: Calibre output used mixed-case titles (not ALL CAPS) and had **no internal chapter/section divisions** (no Roman numerals). Each novella is one continuous block of prose.
  - Wrote `scripts/dunk-egg-splitter.py` via script-builder subagent. Imports `normalize()` from `chapter-splitter.py` via importlib (hyphenated filename workaround).
  - Produced 3 files total (one per novella):
    - `thk-dunk-01.md` — The Hedge Knight (~31,600 words)
    - `tss-dunk-01.md` — The Sworn Sword (~36,600 words)
    - `tmk-dunk-01.md` — The Mystery Knight (~36,800 words)
  - All files have valid YAML frontmatter with `collection: tales-of-dunk-and-egg`, `first_available: pre-agot`, `real_identity: Duncan the Tall`
- **TWOIAF (The World of Ice and Fire):**
  - Installed `ocrmypdf` + `poppler` via Homebrew (Tesseract, Ghostscript, pdftotext, dependencies)
  - OCR'd 344-page scanned PDF: `ocrmypdf --output-type pdf --optimize 1 --jobs 8` → `sources/raw/TWOIAF.ocr.pdf` (164MB, 5.7% smaller than input)
  - Tesseract warnings on ~15 pages ("lots of diacritics" — decorative pages, maps) but no fatal errors
  - Extracted text: `pdftotext -layout` → `sources/raw/TWOIAF.txt` (179,397 words)
  - Quality spot-check: "valyrian" 129 hits, "targaryen" 309 hits, "long night" 14 hits — all pass
  - OCR quality: title/TOC pages have garbled decorative text (expected for scanned ornamental fonts), but prose content is clean and readable
- Updated `.gitignore` with `sources/reference/` exclusion
- Updated `reference/architecture.md` with D&E book codes, `collection:` field, `first_available: pre-agot` convention, and `sources/reference/` layer
- Updated `reference/pov-characters.md` with Duncan the Tall entry and per-novella chapter counts

**Anomalies / follow-ups:**
- D&E novellas have no internal chapter divisions — if future analysis needs finer granularity, a subdivider script could split on scene breaks (blank-line gaps in prose), but not needed now
- TWOIAF OCR: decorative cover pages and TOC dotted-leader lines are garbled, but this is cosmetic — the prose content that matters for the reference layer is clean
- TWOIAF structural splitter was explicitly deferred per plan — needs a planning session once we decide how to segment the reference material (by region? by era? by topic heading?)
- The `pre-agot` value for `first_available` is a new convention not previously in the architecture — flagged in architecture.md, can be renamed later if a more specific scheme is needed

**What's next:**
- Pass 1 mechanical extraction on AGOT remains the primary unblocked work
- TWOIAF structural splitter is deferred until OCR quality reviewed and segmentation strategy decided
- D&E chapters are available for Pass 1 extraction whenever the main-series pipeline is proven

---

### Session 5 — Full Wiki Crawl Executed (2026-04-14)
**What happened:**
- Ran `python3 scripts/wiki-scraper.py --mode all -v` per runbook (`working/runbooks/wiki-full-crawl.md`). Crawl completed fully unattended — no Cloudflare challenges triggered. All 17,952 pages processed: 17,945 succeeded, 7 failed (all HTTP 403 — 6 "Mander"-related pages + "The Mance", likely redirect/special-character edge cases). Final disk footprint: 377 MB total (293 MB raw cache, 81 MB uncategorized markdown, 3.8 MB houses). Only 640 pages classified as `houses/`; 17,305 landed in `_uncategorized/` due to conservative classifier rules. No anomalies beyond the classification skew. Crawl took approximately 36 hours wall clock (slower than the 6–8 hour estimate due to sustained ~280 pages/hour rate on larger character/location pages).

**What's next:**
- Refine `classify_entity()` rules against the static cache to reduce `_uncategorized/` count before designing Pass 2
- Design Pass 2 (wiki-ingester) prompt — what gets promoted from `sources/wiki/` into `graph/nodes/` and how `first_available` gets assigned
- Begin Pass 1 mechanical extraction testing on AGOT chapters (unblocked)
