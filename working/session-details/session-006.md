# Session 6 — Book Integration: Dunk & Egg + TWOIAF

**Date:** 2026-04-16

---

## What Triggered This Session

The main-series pipeline was established: 5 books split into 344 chapters, wiki cache complete, Pass 1 extraction ready to begin on AGOT. But the project scope includes more than the five novels. Two additional sources needed integration: *The Tales of Dunk and Egg* (three prequel novellas) and *The World of Ice and Fire* (a companion encyclopedia). Both were available as files but not yet processed into the pipeline's expected format.

## What Happened

### Dunk & Egg

The plan was straightforward: convert the epub to plaintext, then run it through the chapter splitter. Reality was messier.

Calibre's `ebook-convert` produced the plaintext file (`sources/raw/TDAE.txt`), but the output structure didn't match what the chapter splitter expected. The main-series books use ALL CAPS chapter headings ("BRAN" / "TYRION") that the splitter's regex can detect. Calibre's epub conversion produced mixed-case section headers, and more significantly, the three novellas have no internal chapter divisions at all. Each novella — *The Hedge Knight*, *The Sworn Sword*, *The Mystery Knight* — is one continuous block of prose. There's nothing to split on within each story.

This meant the existing `chapter-splitter.py` couldn't handle it. A new script was needed: `scripts/dunk-egg-splitter.py`. The `script-builder` subagent wrote it. Rather than duplicating the text normalization logic, it imports the `normalize()` function from `chapter-splitter.py` via `importlib` — necessary because the hyphenated filename isn't a valid Python module name, so a standard `import` statement won't work.

The splitter produced three files, one per novella:
- `thk-dunk-01.md` — *The Hedge Knight* (~31,600 words)
- `tss-dunk-01.md` — *The Sworn Sword* (~36,600 words)
- `tmk-dunk-01.md` — *The Mystery Knight* (~36,800 words)

Each file has YAML frontmatter with `collection: tales-of-dunk-and-egg`, `first_available: pre-agot`, and `real_identity: Duncan the Tall`. The `pre-agot` value for `first_available` was a new convention — these stories take place roughly 90 years before the main series. The architecture doc was updated to document this value, with a note that it can be renamed later if a more granular pre-series timeline scheme is needed.

The files are large for single "chapters" (31-37K words each, compared to typical main-series chapters at 4-8K words). If future analysis needs finer granularity, a subdivider could split on scene breaks (blank-line gaps in the prose), but that's an optimization to defer until there's a demonstrated need.

### TWOIAF (The World of Ice and Fire)

TWOIAF posed a different kind of challenge. The source was a scanned PDF — 344 pages of a lavishly illustrated companion book. No selectable text, no epub available. This meant OCR.

Installed the OCR toolchain via Homebrew: `ocrmypdf` (the orchestrator), `tesseract` (the OCR engine), `ghostscript` (PDF rendering), `poppler` (for `pdftotext` extraction). Then ran OCR:

```
ocrmypdf --output-type pdf --optimize 1 --jobs 8 sources/raw/TWOIAF.pdf sources/raw/TWOIAF.ocr.pdf
```

The OCR'd PDF came out at 164 MB (5.7% smaller than the input, thanks to the `--optimize 1` flag). Tesseract threw warnings on about 15 pages — "lots of diacritics" — but these were all decorative pages (ornamental fonts, maps, illustrated title pages) where garbled OCR is expected and irrelevant. No fatal errors.

Text extraction via `pdftotext -layout` produced `sources/raw/TWOIAF.txt` at 179,397 words. Quality spot-checks passed: "valyrian" appeared 129 times, "targaryen" 309 times, "long night" 14 times — all plausible frequencies for an encyclopedia covering Westerosi history.

The OCR quality followed a predictable pattern: decorative cover pages, table-of-contents dot-leader lines, and ornamental section headers were garbled, but the actual prose content — the part that matters for the reference layer — was clean and readable.

### Bookkeeping

Updated `.gitignore` to exclude `sources/reference/` (TWOIAF lives here as a non-narrative source, distinct from the chapter files in `sources/chapters/`). Updated `reference/architecture.md` with D&E book codes (THK, TSS, TMK), the `collection:` frontmatter field, the `pre-agot` first_available convention, and the `sources/reference/` directory as a new layer. Updated `reference/pov-characters.md` with Duncan the Tall's entry and per-novella chapter counts.

## Key Decisions and Why

**One file per novella, not subdivided.** The D&E stories don't have chapter breaks, and artificially splitting them on scene breaks would create arbitrary boundaries that don't correspond to any authorial structure. Better to keep them as the units GRRM wrote and handle the size at the extraction level (the mechanical extractor can process long documents, it just takes more context).

**`pre-agot` as a first_available value.** The spoiler gating system needs a way to say "this information exists before the main series begins." Rather than inventing a complex pre-series timeline (which would need to distinguish between events 90 years before AGOT and events 300 years before), a single `pre-agot` bucket is sufficient for now. It can be refined later if the project ever needs to gate *within* the pre-series timeline.

**TWOIAF structural splitting deferred.** The encyclopedia has a complex internal structure — sections by region, by historical era, by topic. Deciding how to segment it requires a planning session: by chapter heading? by region? by era? Each choice affects how the reference material gets cited in the graph. The OCR and text extraction were the time-sensitive steps; segmentation strategy can wait.

**OCR over manual transcription.** Obvious, but worth noting the trade-off: OCR is fast and automated but produces artifacts on decorative pages. For a reference encyclopedia where the prose content is what matters, this trade-off is overwhelmingly favorable.

## What Was Left Open

- **TWOIAF structural splitter.** The plaintext exists but hasn't been segmented into usable units. Needs a planning session to decide the segmentation strategy.
- **D&E extraction timing.** The novellas are ready for Pass 1 extraction whenever the pipeline is proven on the main series. No rush — AGOT is the priority.
- **`pre-agot` granularity.** If the project eventually needs to distinguish between Aegon's Conquest-era events and Blackfyre Rebellion-era events, the `pre-agot` value will need to be replaced with something more specific. Not a current concern.
- **OCR quality on maps and illustrations.** The text around maps and illustrated pages may contain garbled content that could confuse downstream processing. A cleanup pass (or just filtering rules in the ingestion step) might be needed when TWOIAF actually enters the pipeline.
