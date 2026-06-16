# Events Time-Axis: Data Availability & Cost Opinion
**Date:** 2026-06-15
**Lens:** Data availability and cost — deterministic Python vs LLM spend
**Scope:** 590 event nodes in `graph/nodes/events/`

---

## What I Inspected

| Asset | Finding |
|---|---|
| `working/wiki/data/chronology-events.jsonl` | 2,245 rows total; **158 rows** have `target_type` starting with "event"; **122 distinct event slugs**. This is a sparse mention index, NOT a complete event-date table. |
| `sources/wiki/_raw/*.json` year-pages | 258 year-pages (1–300 AC plus 34 BC pages). Each has a structured HTML event list with `<ul><li>` entries that link to wiki entity pages (verified on `283_AC.json`). |
| `graph/nodes/events/` | **590 event nodes**. Zero carry any `occurred`, `ac_year`, `year`, or `date` frontmatter field today. |
| `working/wiki/data/infobox-data.jsonl` | 232 rows typed as `event.*` — but **zero date-like fields** (no `date`, `year`, `when`, `occurred`). The infobox pipeline did not capture the Date table-cell. |
| `working/wiki/data/edges-temporal-scoped.jsonl` | 3,811 edges, **all 3,811 carry `temporal_key` + `book_order` + `chapter_number`**. The narrative reading-position axis for edges is completely done. |
| Event node frontmatter | 359/590 have `wiki_source` URLs. 219 no-wiki-source nodes (Plate 3 minted) carry `evidence_chapters: [BOOK POV_LABEL]` — the narrative axis anchor for micro-events. |

---

## Question 1 — In-World Date Coverage: Deterministic vs LLM

Three deterministic Python routes exist, with no overlap:

**Route 1 — Year-page HTML link extraction**
The 258 year-page JSON files each contain a structured `<ul><li>` events list that links to wiki entity pages. Cross-referencing those links against event node slugs yields **122 events** (20.7%) datable to a specific AC/BC year. The extraction is pure regex/HTML parsing — already partially done via `chronology-events.jsonl` but that file is a shallow index. A full pass over all 258 year-page HTMLs extracting `href="/index.php/<Title>"` within `<li>` elements can assign years deterministically. Cost: $0 Python.

**Route 2 — Event wiki infobox `Date` field**
The wiki pages for events (cached at `sources/wiki/_raw/<Title>.json`) frequently contain an infobox table cell structured as `Date</th><td><a href="/index.php/NNN_AC"`. Verified on `Battle_of_the_Trident.json` ("Date 283 AC"), `aegon-the-uncrowneds-rebellion` ("43 AC"), `aemonds-march-on-harrenhal` ("130 AC"). This pattern catches an additional **99 events** (16.8%) not covered by Route 1. Cost: $0 Python (regex on cached HTML).

**Route 3 — Prose year mention in wiki body text**
Some event pages lack a structured `Date` infobox cell but mention a year in their opening paragraph (e.g., `Anniversary_Tourney.json`: "in 272 AC"; `defiance-of-duskendale`: "277 AC"). Pattern `\d+\s*&#160;\s*(AC|BC)` in first 2,000 chars of stripped text yields **39 more events** (6.6%). Reliability is lower — requires validating that the year belongs to THIS event, not a mentioned predecessor. Still deterministic, but merits a human spot-check pass. Cost: $0 Python + ~1 hour manual QA.

**Total deterministic coverage: ~260 events (44.1%)**

The remaining 330 events (55.9%) break down as:
- **219 micro-events (Plate 3, no wiki_source)**: carry `evidence_chapters` (e.g., `ACOK Arya V`) — these are chapter-level scene events. They have no in-world AC/BC date and don't need one; their temporal anchor IS the narrative position.
- **~50 War-of-Five-Kings battles** (e.g., `battle-of-the-golden-tooth`, `battle-of-the-stony-shore`): wiki pages exist but no year-link or Date field. Implicitly 298–300 AC from book context — a Python script could assign a range, not a point, by reading which book's wiki pages link to them.
- **~10 TWOW chapter events** (e.g., `alayne-i-the-winds-of-winter`, `arianne-i-the-winds-of-winter`): wiki chapter pages, genuinely dateless in-world.
- **~20 mythic/legendary events** (`battle-for-the-dawn`, `war-of-the-first-men-and-the-children`): inherently undatable.
- **~31 wiki events with no extractable year signal**: e.g., `aegons-landing`, `the-hands-tourney`. These are the LLM/manual tail.

**LLM spend for in-world dating: small, not large.** The genuinely ambiguous tail is ~31 wiki events + ~50 era-range assignments. A Haiku pass over those 80 events with targeted wiki text would cost under $1 and could be validated mechanically (does the output year match a cross-referenced year-page?).

---

## Question 2 — Which Axis Is Nearly Free?

**Narrative reading-position (Book N, Chapter M) is essentially already done.**

- Edges: 3,811 edges carry `temporal_key: "b1-c008"` etc. The `stage4-edge-temporal-scope.py` script completed this. No additional work needed.
- Event nodes (Plate 3 micro-events): 219/233 already carry `evidence_chapters: [BOOK POV_LABEL]`. A lookup table from `sources/chapters/<book>/*.md` frontmatter maps `BOOK POV_LABEL` → `chapter_number` (347 entries available). The mismatch on 28 refs is a trivial normalization (strip trailing roman numerals like `I`, `II`). Cost: $0 Python, ~20 lines of code.
- Wiki-sourced event nodes: `cite_refs` in `edges-temporal-scoped.jsonl` gives book→chapter lists. An event like Aegon's Conquest cited in `agot` ch 60 and `affc` ch 11 gets `min(cite_refs)` as its first-mentioned reading position.

**In-world date (AC/BC year) requires more work** but ~44% is deterministic and the remaining genuine tail is small.

---

## Question 3 — Recommended Build Order

### Phase 1 — $0, Pure Python (do first)

1. **Year-page extraction script**: Parse all 258 year-page HTMLs, extract `<li>` event links → emit `event_slug → year_value/year_era`. Covers ~122 events. (~50 lines Python)
2. **Infobox Date field extractor**: For all 359 nodes with `wiki_source`, fetch their `_raw/*.json`, parse `Date</th><td>` pattern → emit year. Covers ~99 more. (~30 lines Python)
3. **Evidence-chapters → temporal_key resolver**: For 219 Plate 3 micro-events, join `evidence_chapters` label to chapter frontmatter `chapter_number` via pov_label lookup (strip roman numeral suffix for single-chapter POVs). Covers narrative-position axis fully. (~40 lines Python)
4. **Write `ac_year` + `narrative_min_chapter` into event node frontmatter.** Total Python coverage: ~260 events get AC/BC year; ~250 events get narrative-position key.

### Phase 2 — $0 Python, Human QA (an hour)

5. **Prose-year regex pass**: Route 3 above, 39 events. Generate a diff for human spot-check — the main failure mode is attributing a mentioned predecessor's year to this event.
6. **Era-range assignment for WoFK battles**: For the ~50 War-of-5-Kings battles with no exact year, assign `ac_year_min: 298, ac_year_max: 300, ac_year_confidence: era-range`. Python: check which year-pages link to the event page's wiki title.

### Phase 3 — Small LLM job (Haiku, ~$1)

7. **Targeted LLM pass on the ~31 remaining wiki-source events** with no extractable year. Feed the stripped wiki page text + the question "what AC or BC year did this event occur? Output only: `NNN AC` or `NNN BC` or `unknown`." Validate outputs by checking if the stated year appears in a year-page that links back to this event (mechanical cross-check). This is a small, bounded Haiku job with a mechanical validator.

### 80/20 Line

Phase 1 alone covers 44% of the in-world date axis and 100% of the narrative axis — both for $0. Phase 1 + Phase 2 covers ~53% of in-world dating. The expensive "mythic events" and "TWOW chapter events" (~30 nodes) are genuinely undatable and should not get LLM spend; they get `ac_year: null, ac_year_note: undatable-mythic` in frontmatter.

---

## Summary Recommendation

Start with a $0 Python script that (a) parses all 258 year-page HTMLs for event-slug→year links, (b) scrapes the `Date</th><td>` infobox cell from each event's cached wiki JSON, and (c) resolves `evidence_chapters` labels to `chapter_number` keys for Plate 3 micro-events — this covers roughly **44% of in-world dating** and **~95% of the narrative reading-position axis** at zero LLM cost. The ~50 War-of-Five-Kings battles need only an era-range assignment (298–300 AC), derivable from which year-pages link back to them. Only the ~31 genuinely ambiguous wiki events warrant a small Haiku pass (estimated under $1), and ~30 mythic/TWOW-chapter events should be stamped `undatable` without spending anything on them.

**Coverage estimate:** 44% get a precise AC/BC year deterministically; another ~9% get an era-range (298–300 AC) deterministically; ~5% need a small Haiku pass; ~40% (mythic, TWOW, micro-events) are correctly served by narrative-position only and don't need an in-world year at all.

**Cost tier:** Phase 1 is a $0 Python job (1–2 hours of scripting). Phase 3 is a small LLM job (~$1, Haiku, 1 hour). The overall dating track is not a big LLM job.
