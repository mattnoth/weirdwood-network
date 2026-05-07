# Runbook: Book Integration (Dunk & Egg + TWOIAF)

**Purpose:** Integrate two new source artifacts into the Weirwood Network pipeline:
1. `The Tales of Dunk & Egg.epub` → split into per-chapter markdown
2. `The-World-of-Ice-and-Fire-a-Shinnick-Scan.pdf` → OCR to searchable text

Run from a Claude CLI session launched with `--dangerously-skip-permissions` so
the long `brew install`, `ocrmypdf`, and file-write operations don't need
interactive approval.

**Expected runtime:** 30–70 minutes total (mostly TWOIAF OCR)
**Expected disk:** ~500MB new (OCR'd PDF + text + D&E chapters)

**Plan file:** `/Users/mnoth/.claude/plans/users-mnoth-source-asoiaf-chat-worklog-toasty-crab.md`
(Read it if you want the full design context. This runbook is the executable version.)

---

## Instructions for the Claude CLI agent following this runbook

You are running a mix of shell commands and file edits. Do not run any
extraction passes. Do not promote anything into `graph/nodes/`. Do not commit
anything. Do not modify `.gitignore` except to add the single `sources/reference/`
line specified in Step 5. Your job is to get the two new sources into the
pipeline and then update bookkeeping.

**Working directory:** `/Users/mnoth/source/asoiaf-chat` for all commands below.

You MAY delegate the D&E splitter script to the `script-builder` subagent
(Step 3). Everything else is direct execution.

---

### Step 0 — Pre-flight checks

Verify before starting:

1. **Source files present.** Both must exist in `sources/raw/`:
   ```
   ls -la "sources/raw/The Tales of Dunk & Egg.epub" \
          "sources/raw/The-World-of-Ice-and-Fire-a-Shinnick-Scan.pdf"
   ```
   Expected sizes: ~438KB for the epub, ~182MB for the PDF.

2. **ebook-convert available** (Calibre):
   ```
   which ebook-convert
   ```
   Should print `/opt/homebrew/bin/ebook-convert`. If missing:
   `brew install --cask calibre`.

3. **Disk space.** `df -h .` — need at least 2GB free (OCR'd PDF will be
   somewhat smaller than the 182MB original after `--optimize 1`, but working
   space matters).

If any check fails, stop and report. Do not improvise.

---

### Step 1 — Install OCR tooling

```
brew install ocrmypdf poppler
```

Pulls in Tesseract, Poppler (`pdftotext`), Ghostscript, and dependencies.
Expect ~400MB of installs, 2–5 minutes. Run to completion.

After it finishes, verify:
```
which ocrmypdf tesseract pdftotext
```
All three should resolve. If any are missing, report and stop.

---

### Step 2 — Convert D&E epub to plain text

```
ebook-convert "sources/raw/The Tales of Dunk & Egg.epub" "sources/raw/TDAE.txt"
```

Expected: a clean ~1–2MB `.txt` file under `sources/raw/`. Calibre will print
conversion details.

**Inspect the structure** before writing the splitter:
```
grep -n "^THE HEDGE KNIGHT\|^THE SWORN SWORD\|^THE MYSTERY KNIGHT" sources/raw/TDAE.txt
grep -cE "^[IVX]+$" sources/raw/TDAE.txt
```

Report back:
- Line numbers where each novella starts (expected 3 hits)
- Total count of Roman-numeral-only lines (these are internal chapter markers)
- If the patterns don't match expectations (e.g. Calibre emitted `The Hedge
  Knight` mixed case, or used `Chapter 1` instead of Roman numerals), **stop
  and report** before writing the splitter. Do not try to retrofit.

Typical expected counts from the novellas:
- *The Hedge Knight*: ~4 internal sections (I–IV)
- *The Sworn Sword*: ~6 internal sections (I–VI)
- *The Mystery Knight*: ~5 internal sections (I–V)

---

### Step 3 — Write the D&E splitter

Delegate to the `script-builder` subagent with this prompt (fill in the
`[STRUCTURE_SUMMARY]` with what you saw in Step 2):

> Write `scripts/dunk-egg-splitter.py` — a sibling to the existing
> `scripts/chapter-splitter.py`. Input: `sources/raw/TDAE.txt`. Output:
> per-chapter markdown files in `sources/chapters/thk/`, `sources/chapters/tss/`,
> `sources/chapters/tmk/`.
>
> **Structure summary from the input file:** [STRUCTURE_SUMMARY]
>
> **Requirements:**
> - Reuse helpers from `scripts/chapter-splitter.py`: `normalize()` (smart
>   quotes), `to_roman()`, `heading_to_title()`. Import them via
>   `from chapter_splitter import ...` (same directory, so this works when
>   run from repo root).
> - Three novella codes: `thk` (The Hedge Knight), `tss` (The Sworn Sword),
>   `tmk` (The Mystery Knight).
> - Filename convention: `{novella}-dunk-{nn}.md` (e.g. `thk-dunk-01.md`).
> - YAML frontmatter per file, mirroring the shape used in
>   `sources/chapters/agot/*.md` (read one to see the exact fields), plus:
>   - `pov: dunk`
>   - `real_identity: Duncan the Tall`
>   - `collection: tales-of-dunk-and-egg`
>   - `first_available` set to match the project's pre-AGOT convention (if
>     `reference/architecture.md` doesn't specify one, use `pre-agot` as the
>     value and flag it in your summary so we can rename later).
> - Skip the "Introduction" section if the Calibre output includes one —
>   that's frontmatter from George R.R. Martin, not narrative.
> - Print a summary at the end: per-novella chapter count produced.
>
> Also add a `--verbose` flag that prints which heading triggered each file
> write, matching the style of the existing `chapter-splitter.py`.
>
> Do NOT modify `chapter-splitter.py`. If refactoring shared helpers into a
> new module feels cleaner, note that as a follow-up but keep the direct
> import for now.

When the subagent returns, verify the script exists at
`scripts/dunk-egg-splitter.py` and read it once to sanity-check before running.

---

### Step 4 — Run the D&E splitter

```
python3 scripts/dunk-egg-splitter.py sources/raw/TDAE.txt --verbose
```

Verify the output:
```
ls sources/chapters/thk/ sources/chapters/tss/ sources/chapters/tmk/ | wc -l
ls sources/chapters/thk/ sources/chapters/tss/ sources/chapters/tmk/
```

Pick one file at random (e.g. `sources/chapters/thk/thk-dunk-01.md`) and
confirm:
- Valid YAML frontmatter
- Body is coherent narrative prose (not blank, not garbled)
- Word count is reasonable for a novella section (typically 3k–10k words)

If anything looks off, stop and report. Do not attempt to fix the splitter
inline — that's a separate planning cycle.

---

### Step 5 — Gitignore update for reference layer

Add a single new rule to `.gitignore`:

```
sources/reference/
```

Add it in the same block as the other `sources/` rules. Then verify with
`git status` — nothing new under `sources/` should appear as untracked.

---

### Step 6 — OCR TWOIAF

This is the longest step (20–45 minutes on an M4 Max). Run in the foreground
and let it finish:

```
ocrmypdf \
  --output-type pdf \
  --optimize 1 \
  --jobs 8 \
  "sources/raw/The-World-of-Ice-and-Fire-a-Shinnick-Scan.pdf" \
  "sources/raw/TWOIAF.ocr.pdf"
```

Notes:
- Do NOT add `--force-ocr`. The original has no text layer, so default behavior
  OCRs every page.
- If ocrmypdf complains about encrypted/protected PDF, try adding
  `--force-ocr` as a fallback. Report the error either way.
- Progress is printed per page. If it stalls on one page for >5 minutes,
  abort (Ctrl-C), add `--skip-big 50` to skip very large pages, and retry.

When it finishes, verify:
```
ls -lh sources/raw/TWOIAF.ocr.pdf
```
Expected size: 150–250MB.

---

### Step 7 — Extract TWOIAF text

```
pdftotext -layout "sources/raw/TWOIAF.ocr.pdf" "sources/raw/TWOIAF.txt"
```

Quality check:
```
wc -w sources/raw/TWOIAF.txt
grep -c -i "valyrian" sources/raw/TWOIAF.txt
grep -c -i "targaryen" sources/raw/TWOIAF.txt
grep -c -i "long night" sources/raw/TWOIAF.txt
head -200 sources/raw/TWOIAF.txt
```

Expected:
- Word count: 150,000–200,000
- "valyrian" / "targaryen" / "long night" should all return double-digit+ counts
- First 200 lines should contain recognizable text (title page, TOC, prose)

Report any concerns:
- Word count below 100k → OCR likely failed on a large chunk; flag it
- One of the grep counts is 0 → the keyword terms are present in TWOIAF, so a
  zero means that part of the text was garbled
- First 200 lines are unreadable gibberish → OCR failed; stop and report

Do NOT write the TWOIAF structural splitter yet (that was explicitly deferred
in the plan — it's a follow-up once we see OCR quality).

---

### Step 8 — Update reference docs

Two small edits:

**`reference/architecture.md`** — add a section documenting:
- The `sources/reference/` layer (TWOIAF, future non-narrative sources; not
  subject to Pass 1 chapter extraction)
- The three D&E novella book codes: `thk`, `tss`, `tmk`
- The `collection:` frontmatter field used for novella grouping
- The `pre-agot` value convention for `first_available` on D&E chapters

Find the right section (likely near the chapter-file naming / directory
structure discussion) and add concisely. If the file structure makes placement
ambiguous, pick the best-fit spot and note the placement choice in your final
report.

**`reference/pov-characters.md`** — add an entry for Duncan the Tall as the
sole POV of the D&E novellas. Include expected chapter counts per novella
(from your Step 4 run).

---

### Step 9 — Git sanity check

```
git status --porcelain
```

Expected untracked/modified:
- `.gitignore` (modified — sources/reference/ added)
- `scripts/dunk-egg-splitter.py` (new)
- `reference/architecture.md` (modified)
- `reference/pov-characters.md` (modified)
- `worklog.md` (modified — Step 10)
- `working/runbooks/book-integration.md` (this file, already committed or
  untracked depending on your session)

NO files under `sources/raw/`, `sources/chapters/`, or `sources/reference/`
should appear. If any do, stop and report — the gitignore is wrong.

Do NOT commit anything. That's Matt's call.

---

### Step 10 — Worklog update

Append a Session 6 entry to `worklog.md` following the Session 5 format. Put
it directly below the `## Session Log` header (newest first). Cover:

- Date: today (check `date` if unsure, should be around 2026-04-16)
- D&E: total chapters produced, per-novella breakdown, any heading
  oddities encountered
- TWOIAF: OCR runtime, output file size, word count, keyword spot-check
  results
- Any anomalies or follow-ups for the next session (especially if OCR
  quality suggests a rerun with different settings, or if the D&E splitter
  needs a tweak)
- "What's next" section noting that Pass 1 on AGOT is still the primary
  unblocked work, and that the TWOIAF structural splitter is deferred

Also update the **Current State → Infrastructure** checklist at the top of
`worklog.md`:
- Add checked item: "D&E novellas split into chapter files (counts from Step 4)"
- Add checked item: "TWOIAF OCR'd and extracted to plaintext"
- Add checked item: "ocrmypdf + poppler installed"

---

### Step 11 — Final report to the user

Print a concise summary:
- D&E chapter counts (3 novellas, N total chapters)
- TWOIAF OCR outcome (word count, disk footprint, quality verdict)
- Any follow-ups flagged for Matt

That's it. Stop. Do not start Pass 1. Do not commit.

---

## Notes for the human iterating this runbook

- **If the D&E heading pattern differs from expectations:** the agent will stop
  at Step 2 and report. Update the splitter prompt in Step 3 with the actual
  pattern, then restart from Step 3.
- **If OCR quality is poor:** retry Step 6 with `--deskew --clean` added (fixes
  skew from scan imperfections). If still poor, escalate to a planning session
  — may need a different OCR approach or preprocessing.
- **Resuming after interruption:** every step is idempotent except Step 3
  (splitter write). If the splitter already exists, skip to Step 4.
  `ocrmypdf` won't re-OCR if the output file exists — delete it to force
  rerun.
- **The plan file** (`~/.claude/plans/users-mnoth-source-asoiaf-chat-worklog-toasty-crab.md`)
  has the design rationale. Consult it if any step's *why* is unclear.
