#!/usr/bin/env python3
"""Split the Fire & Blood epub into per-section, line-numbered markdown files.

Fire & Blood analogue of dunk-egg-splitter.py, with one new capability: the
source is an epub (a zip of XHTML files), not a plain .txt.  This script reads
the epub's content HTML directly via stdlib `zipfile` + `re`/`html` — no new
pip dependencies.

The authoritative cutting map is `working/fire-and-blood/unit-map.json`
(built by hand against the unzipped epub, S198).  The epub's own `toc.ncx` is
UNRELIABLE — several navPoints resolve to anchors that don't exist, and files
011/014 have no navPoint at all — so this script never consults the NCX for
boundaries; it trusts unit-map.json exclusively.

Each base unit == one content HTML file (index_split_0NN.html, NN 003-025).
Oversized units are sub-split on paragraph boundaries into `-pMM` parts per
the token thresholds recorded in unit-map.json's `_meta` block.

CRITICAL cleaning rule: this script does NOT "fix" OCR noise (letter
substitutions like "che" for "the", "|" for "I", stray case flips).  Those are
left verbatim on purpose — downstream quote-locators grep the noisy text, and
a "corrected" quote becomes unfindable.  See the QA gate's OCR-frequency scan,
which reports noise instead of repairing it.

Usage:
    python scripts/fire-and-blood-splitter.py
    python scripts/fire-and-blood-splitter.py --verbose
    python scripts/fire-and-blood-splitter.py --dry-run
    python scripts/fire-and-blood-splitter.py --epub /path/to/fire-and-blood.epub \\
        --map /path/to/unit-map.json --output /tmp/fab-out/
"""

import argparse
import html
import json
import math
import re
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# HTML -> paragraph parsing
# ---------------------------------------------------------------------------

# One paragraph-level element: <p ...>...</p> or <h2 ...>...</h2>, captured
# with its opening-tag attributes (to recover id="page_N" / class="...") and
# its raw inner HTML (which may itself contain inline tags like <span>/<i>).
_BLOCK_RE = re.compile(
    r"<(?P<tag>p|h2)(?P<attrs>[^>]*)>(?P<inner>.*?)</(?P=tag)>",
    re.DOTALL | re.IGNORECASE,
)
_ATTR_ID_RE = re.compile(r'\bid="([^"]*)"')
_ATTR_CLASS_RE = re.compile(r'\bclass="([^"]*)"')
_CALIBRE3_SPAN_RE = re.compile(
    r'<span class="calibre3">(.*?)</span>', re.DOTALL | re.IGNORECASE
)
_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"[ \t ]+")


class Paragraph:
    """One parsed <p>/<h2> block from the epub body."""

    __slots__ = ("tag", "elem_id", "css_class", "raw_inner", "text", "has_calibre3_span")

    def __init__(self, tag, elem_id, css_class, raw_inner):
        self.tag = tag.lower()
        self.elem_id = elem_id
        self.css_class = css_class or ""
        self.raw_inner = raw_inner
        self.has_calibre3_span = bool(_CALIBRE3_SPAN_RE.search(raw_inner))
        self.text = clean_inline_html(raw_inner)

    def __repr__(self):
        return f"Paragraph(tag={self.tag!r}, id={self.elem_id!r}, class={self.css_class!r}, text={self.text[:40]!r})"


def clean_inline_html(raw_inner):
    """Strip inline tags (span/i/etc.) and unescape entities; collapse whitespace.

    Deliberately does NOT touch letter-level OCR noise, curly quotes, or
    em-dashes — those are left verbatim per the FAB cleaning spec.
    """
    text = _TAG_RE.sub("", raw_inner)
    text = html.unescape(text)
    text = _WHITESPACE_RE.sub(" ", text)
    # Normalize newlines-within-a-paragraph (shouldn't occur given DOTALL match,
    # but be defensive) to single spaces, then strip.
    text = text.replace("\n", " ").replace("\r", " ")
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def parse_body_paragraphs(html_bytes):
    """Extract the <body>...</body> region and parse it into Paragraph objects.

    Explicitly drops everything in <head> (including the leaked PDF build path
    in <title>) by only ever looking inside <body>.
    """
    content = html_bytes.decode("utf-8")
    body_match = re.search(r"<body[^>]*>(.*)</body>", content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        raise ValueError("No <body> tag found in HTML content")
    body_html = body_match.group(1)

    paragraphs = []
    for m in _BLOCK_RE.finditer(body_html):
        tag = m.group("tag")
        attrs = m.group("attrs") or ""
        inner = m.group("inner")
        id_match = _ATTR_ID_RE.search(attrs)
        class_match = _ATTR_CLASS_RE.search(attrs)
        elem_id = id_match.group(1) if id_match else None
        css_class = class_match.group(1) if class_match else None
        paragraphs.append(Paragraph(tag, elem_id, css_class, inner))
    return paragraphs


# ---------------------------------------------------------------------------
# Title-anchor detection (per unit's title_marker.kind)
# ---------------------------------------------------------------------------

def find_title_span_indices(paragraphs, start_idx=0):
    """Return the index of the first paragraph (at/after start_idx) that
    contains a <span class="calibre3"> — the title-text marker used by both
    'h2' and 'calibre3_span' kinds. Returns None if not found."""
    for i in range(start_idx, len(paragraphs)):
        if paragraphs[i].has_calibre3_span:
            return i
    return None


def is_blank_paragraph(p):
    return p.text == "" or p.css_class == "whitespace"


def locate_title_block(paragraphs, marker):
    """Locate the title paragraph(s) for a unit given its title_marker.

    Returns (title_text, set_of_dropped_indices) where dropped_indices are the
    paragraph indices that belong to the title itself (to be excluded from
    body prose) — this includes a second wrapped title-fragment paragraph
    when the title text wraps across two consecutive calibre3-span
    paragraphs (a real pattern in this epub: e.g. file 012's "...Triumphs
    and " + "Tragedies").

    Content BEFORE the located title index is preamble and is dropped by the
    caller (return value only covers the title paragraph indices themselves).
    """
    kind = marker.get("kind")

    if kind == "h2":
        for i, p in enumerate(paragraphs):
            if p.tag == "h2":
                return p.text, {i}, i
        raise ValueError("title_marker kind=h2 but no <h2> found")

    if kind == "calibre3_span":
        anchor = marker.get("anchor")
        # Find the paragraph whose id == anchor AND which carries the
        # calibre3 span (title text may live in a <p> whose *class* varies —
        # calibre1 in most files, but calibre9 in file 022 — so key off id +
        # the span, not the class).
        title_idx = None
        for i, p in enumerate(paragraphs):
            if p.elem_id == anchor and p.has_calibre3_span:
                title_idx = i
                break
        if title_idx is None:
            raise ValueError(f"title_marker anchor {anchor!r} not found (calibre3_span)")

        dropped = {title_idx}
        title_text = paragraphs[title_idx].text

        # Wrapped-title continuation: scan forward past blank/whitespace-only
        # paragraphs for one more calibre3-span paragraph with NO id of its
        # own (a second title fragment, e.g. "Tragedies" continuing "...
        # Triumphs and "). Stop looking once we hit real body prose.
        j = title_idx + 1
        while j < len(paragraphs) and is_blank_paragraph(paragraphs[j]):
            j += 1
        if (
            j < len(paragraphs)
            and paragraphs[j].has_calibre3_span
            and paragraphs[j].elem_id is None
        ):
            dropped.add(j)
            # Join without forcing a space if the first half already ends in
            # a space (it usually does, from the source line wrap).
            sep = "" if title_text.endswith(" ") or not title_text else " "
            title_text = f"{title_text}{sep}{paragraphs[j].text}".strip()
            title_idx = j

        return title_text, dropped, title_idx

    if kind == "none_continuation":
        return None, set(), -1

    raise ValueError(f"Unknown title_marker kind: {kind!r}")


def strip_duplicate_running_header(paragraphs, keep_mask, ncx_title):
    """Drop standalone body paragraphs that exactly duplicate the section
    title (a duplicated running-header artifact of the PDF->epub conversion).

    Only fires when a paragraph's ENTIRE text equals the title (normalized on
    whitespace/case-insensitive-ish via exact string compare after strip) —
    never when the title is glued to real prose in the same paragraph (e.g.
    "...End of Regency eace reigned over King's Landing" must survive intact
    because dropping it would eat real prose).
    """
    if not ncx_title:
        return 0
    target = ncx_title.strip()
    dropped_count = 0
    for i, p in enumerate(paragraphs):
        if not keep_mask[i]:
            continue
        if p.text.strip() == target:
            keep_mask[i] = False
            dropped_count += 1
    return dropped_count


# ---------------------------------------------------------------------------
# Unit extraction
# ---------------------------------------------------------------------------

class UnitResult:
    def __init__(self, unit, title_text, body_paragraphs, warnings):
        self.unit = unit
        self.title_text = title_text
        self.body_paragraphs = body_paragraphs  # list[str], cleaned text, in order
        self.warnings = warnings


def extract_unit(unit, html_bytes, verbose=False):
    """Parse one epub content file into (title, ordered body paragraph texts)."""
    warnings = []
    paragraphs = parse_body_paragraphs(html_bytes)
    marker = unit["title_marker"]
    ncx_title = unit["ncx_title"]

    title_text, title_indices, title_last_idx = locate_title_block(paragraphs, marker)

    keep_mask = [True] * len(paragraphs)

    if marker["kind"] == "none_continuation":
        # No preamble to drop, no title paragraph to exclude — keep everything.
        content_start = 0
        title_text = ncx_title  # displayed title comes from the map, not the body
    else:
        content_start = title_last_idx + 1
        for i in title_indices:
            keep_mask[i] = False
        # Drop everything strictly before the title anchor (preamble junk —
        # e.g. file 003's garbled OCR "Dedication" block).
        for i in range(0, title_last_idx):
            keep_mask[i] = False

    # Drop blank/whitespace-only paragraphs everywhere.
    for i, p in enumerate(paragraphs):
        if keep_mask[i] and is_blank_paragraph(p):
            keep_mask[i] = False

    # Drop standalone duplicated running-header paragraphs (dedup-header leak).
    dup_dropped = strip_duplicate_running_header(paragraphs, keep_mask, ncx_title)
    if dup_dropped and verbose:
        print(f"    Dropped {dup_dropped} duplicate running-header paragraph(s)")

    body_paragraphs = [paragraphs[i].text for i in range(len(paragraphs)) if keep_mask[i]]

    if not body_paragraphs:
        warnings.append(f"Unit {unit['nn']} ({unit['slug']}): no body paragraphs survived cleaning")

    if title_text is None:
        title_text = ncx_title

    return UnitResult(unit, title_text, body_paragraphs, warnings)


# ---------------------------------------------------------------------------
# Sub-splitting on paragraph boundaries
# ---------------------------------------------------------------------------

def plan_parts(paragraphs, source_words, meta, dance_core, verbose=False):
    """Decide how many parts a unit needs and how to distribute paragraphs.

    Uses source_words * token_per_word as the token estimate (matches the
    spec, rather than re-tokenizing the cleaned text, so the trigger lines up
    with the authoritative word counts in unit-map.json).

    Returns a list of paragraph-index-range tuples (start, end) [end exclusive],
    one per part, in order. A single-part unit returns [(0, len(paragraphs))].
    """
    token_per_word = meta["token_per_word"]
    split_trigger = meta["split_trigger_tokens"]
    cap = meta["dance_core_cap_tokens"] if dance_core else meta["default_cap_tokens"]

    total_tokens = source_words * token_per_word

    if total_tokens <= split_trigger:
        return [(0, len(paragraphs))], total_tokens

    n_parts = max(2, math.ceil(total_tokens / cap))

    # Distribute paragraphs across n_parts as evenly as possible by an
    # approximate per-paragraph token weight (proportional to character
    # length, a reasonable proxy since we don't want to re-tokenize).
    para_lengths = [max(1, len(p)) for p in paragraphs]
    total_len = sum(para_lengths)
    target_len = total_len / n_parts

    boundaries = []
    running = 0
    part_start = 0
    for i, length in enumerate(para_lengths):
        running += length
        if running >= target_len * (len(boundaries) + 1) and i + 1 < len(paragraphs):
            boundaries.append(i + 1)
    # Ensure exactly n_parts - 1 boundaries; trim or pad defensively.
    boundaries = sorted(set(b for b in boundaries if 0 < b < len(paragraphs)))
    while len(boundaries) > n_parts - 1:
        boundaries.pop()
    while len(boundaries) < n_parts - 1:
        # Pad by splitting the largest remaining segment in half.
        segs = [0] + boundaries + [len(paragraphs)]
        seg_sizes = [(segs[i + 1] - segs[i], i) for i in range(len(segs) - 1)]
        seg_sizes.sort(reverse=True)
        _, seg_i = seg_sizes[0]
        new_b = (segs[seg_i] + segs[seg_i + 1]) // 2
        if new_b <= segs[seg_i]:
            new_b = segs[seg_i] + 1
        boundaries.append(new_b)
        boundaries = sorted(set(boundaries))

    ranges = []
    prev = 0
    for b in boundaries:
        ranges.append((prev, b))
        prev = b
    ranges.append((prev, len(paragraphs)))

    if verbose:
        print(f"    Split into {len(ranges)} parts (~{total_tokens:,.0f} tokens, cap {cap:,})")

    return ranges, total_tokens


# ---------------------------------------------------------------------------
# Frontmatter + file writing
# ---------------------------------------------------------------------------

def build_frontmatter(unit, part, part_total, file_name):
    return (
        f"---\n"
        f"book: FAB\n"
        f"collection: fire-and-blood\n"
        f"section_number: {int(unit['nn'])}\n"
        f'section_title: "{unit["ncx_title"]}"\n'
        f"part: {part}\n"
        f"part_total: {part_total}\n"
        f"era: {unit['era']}\n"
        f"first_available: pre-agot\n"
        f"file_name: {file_name}\n"
        f"---\n\n"
    )


def file_name_for(slug, nn, part, part_total):
    """Build the output file name.

    NN in the filename is the unit's NCX section order, 2-digit zero-padded
    (e.g. nn="003" -> "03", nn="015" -> "15", nn="025" -> "25") — NOT the raw
    3-digit epub file number. Confirmed against the design doc's own worked
    examples (fab-aegons-conquest-03, fab-heirs-of-the-dragon-15).
    """
    nn_2digit = f"{int(nn):02d}"
    if part_total == 1:
        return f"fab-{slug}-{nn_2digit}.md"
    return f"fab-{slug}-{nn_2digit}-p{part:02d}.md"


def write_unit_files(unit_result, meta, output_dir, verbose=False):
    """Write one or more markdown files for a single unit; return metadata
    for the QA/summary pass."""
    unit = unit_result.unit
    nn = unit["nn"]
    slug = unit["slug"]
    dance_core = unit["dance_core"]
    title_text = unit_result.title_text
    paragraphs = unit_result.body_paragraphs

    ranges, est_tokens = plan_parts(paragraphs, unit["source_words"], meta, dance_core, verbose=verbose)
    part_total = len(ranges)

    written_files = []
    for part_idx, (start, end) in enumerate(ranges, start=1):
        part_paragraphs = paragraphs[start:end]
        file_name = file_name_for(slug, nn, part_idx, part_total)
        out_path = Path(output_dir) / file_name

        body_text = "\n\n".join(part_paragraphs)
        frontmatter = build_frontmatter(unit, part_idx, part_total, file_name)

        full_text = frontmatter + f"# {title_text}\n\n" + body_text + "\n"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        word_count = sum(len(p.split()) for p in part_paragraphs)
        line_count = full_text.count("\n") + 1

        written_files.append({
            "unit_nn": nn,
            "slug": slug,
            "part": part_idx,
            "part_total": part_total,
            "file_name": file_name,
            "path": out_path,
            "word_count": word_count,
            "line_count": line_count,
            "est_tokens": est_tokens / part_total if part_total else est_tokens,
        })

        if verbose:
            print(f"    Wrote {out_path}  ({line_count} lines, {word_count:,} words)")

    return written_files


# ---------------------------------------------------------------------------
# QA gate
# ---------------------------------------------------------------------------

PDF_PATH_NEEDLE = "B07C6TBTV3"

# OCR-noise regex components (see QA gate spec item 4).
# The dominant pipe artifact in this epub is a STANDALONE "|" token (OCR
# misread of the word "I") — e.g. "Jaehaerys | Targaryen", "|t purports".
# Also match pipe glued directly onto a letter (both orders), the rarer case.
_OCR_PIPE_RE = re.compile(r"(?<![A-Za-z])\|(?![A-Za-z])|[A-Za-z]\||\|[A-Za-z]")
_OCR_CHE_CBE_RE = re.compile(r"\b(che|cbe)\b")
_OCR_MIDWORD_CASE_RE = re.compile(r"\b[a-z]+[A-Z][a-z]*\b")
_OCR_NUMERIC_LINE_RE = re.compile(r"^\s*\d+\s*$")


def score_ocr_noise(file_text):
    """Return (score, breakdown dict) for one output file's OCR-noise scan."""
    pipe_hits = len(_OCR_PIPE_RE.findall(file_text))
    che_hits = len(_OCR_CHE_CBE_RE.findall(file_text))
    midword_hits = len(_OCR_MIDWORD_CASE_RE.findall(file_text))
    numeric_lines = sum(1 for line in file_text.splitlines() if _OCR_NUMERIC_LINE_RE.match(line))

    score = pipe_hits + che_hits + midword_hits + numeric_lines
    return score, {
        "pipe": pipe_hits,
        "che_cbe": che_hits,
        "midword_case": midword_hits,
        "numeric_lines": numeric_lines,
    }


def run_qa_gate(written_files, unit_map_by_nn, output_dir, verbose=False):
    """Run the deterministic QA checks and write working/fire-and-blood/ocr-scan.md.

    Returns (warnings list, qa_summary dict) for the caller to print.
    """
    warnings = []

    # --- Check 1: PDF-path header leak ---
    pdf_path_hits = 0
    pdf_path_files = []
    for wf in written_files:
        text = wf["path"].read_text(encoding="utf-8")
        if PDF_PATH_NEEDLE in text:
            pdf_path_hits += text.count(PDF_PATH_NEEDLE)
            pdf_path_files.append(wf["file_name"])
    if pdf_path_hits:
        warnings.append(
            f"PDF-path header leak: {PDF_PATH_NEEDLE!r} found {pdf_path_hits}x in {pdf_path_files}"
        )

    # --- Check 2: per-unit word count vs source_words (sum across parts) ---
    words_by_unit = {}
    for wf in written_files:
        words_by_unit.setdefault(wf["unit_nn"], 0)
        words_by_unit[wf["unit_nn"]] += wf["word_count"]

    word_count_flags = []
    for nn, total_words in words_by_unit.items():
        expected = unit_map_by_nn[nn]["source_words"]
        if expected == 0:
            continue
        pct_diff = abs(total_words - expected) / expected
        if pct_diff > 0.10:
            word_count_flags.append((nn, unit_map_by_nn[nn]["slug"], expected, total_words, pct_diff))
            warnings.append(
                f"Unit {nn} ({unit_map_by_nn[nn]['slug']}): word count {total_words:,} vs "
                f"expected {expected:,} ({pct_diff:.1%} off)"
            )

    # --- Check 3: boundary integrity — whole paragraph duplicated across adjacent files ---
    # Group files by unit, in part order; also check across unit boundaries
    # (adjacent units in nn order) since a dedup-header leak could duplicate
    # a paragraph across a unit seam too.
    files_in_order = sorted(written_files, key=lambda wf: (wf["unit_nn"], wf["part"]))
    dup_paragraph_count = 0
    dup_examples = []
    for i in range(len(files_in_order) - 1):
        cur = files_in_order[i]
        nxt = files_in_order[i + 1]
        cur_paras = [p for p in cur["path"].read_text(encoding="utf-8").split("\n\n") if p.strip()]
        nxt_paras = [p for p in nxt["path"].read_text(encoding="utf-8").split("\n\n") if p.strip()]
        if not cur_paras or not nxt_paras:
            continue
        cur_last = cur_paras[-1].strip()
        nxt_first_candidates = nxt_paras[:2]  # skip past frontmatter/H1 remnants defensively
        for cand in nxt_first_candidates:
            if cur_last and cur_last == cand.strip():
                dup_paragraph_count += 1
                dup_examples.append((cur["file_name"], nxt["file_name"]))
                break

    if dup_paragraph_count:
        warnings.append(
            f"Boundary integrity: {dup_paragraph_count} duplicated paragraph(s) across adjacent files: {dup_examples}"
        )

    # --- Check 4: OCR-frequency scan per file ---
    ocr_rows = []
    for wf in written_files:
        text = wf["path"].read_text(encoding="utf-8")
        score, breakdown = score_ocr_noise(text)
        ocr_rows.append({**wf, "noise_score": score, "noise_breakdown": breakdown})

    ocr_rows.sort(key=lambda r: r["noise_score"], reverse=True)

    # Write working/fire-and-blood/ocr-scan.md
    scan_path = Path("working/fire-and-blood/ocr-scan.md")
    scan_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Fire & Blood OCR-noise scan",
        "",
        "Deterministic per-file noise score (pipe-glyph artifacts + che/cbe "
        "tokens + mid-word case flips + standalone numeric lines), sorted "
        "noisiest-first. This does NOT repair anything — it flags hot files "
        "for extraction ordering and the verify arm to attend to.",
        "",
        "| File | Unit | Part | Noise Score | pipe | che/cbe | midword_case | numeric_lines |",
        "|------|------|------|-------------|------|---------|--------------|---------------|",
    ]
    for r in ocr_rows:
        b = r["noise_breakdown"]
        lines.append(
            f"| {r['file_name']} | {r['unit_nn']} | {r['part']}/{r['part_total']} | "
            f"{r['noise_score']} | {b['pipe']} | {b['che_cbe']} | {b['midword_case']} | {b['numeric_lines']} |"
        )
    scan_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    qa_summary = {
        "pdf_path_hits": pdf_path_hits,
        "pdf_path_files": pdf_path_files,
        "word_count_flags": word_count_flags,
        "dup_paragraph_count": dup_paragraph_count,
        "dup_examples": dup_examples,
        "ocr_rows": ocr_rows,
        "scan_path": scan_path,
    }

    return warnings, qa_summary


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def load_unit_map(map_path):
    with open(map_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["_meta"], data["units"]


def split_fire_and_blood(epub_path, map_path, output_dir, verbose=False, dry_run=False):
    meta, units = load_unit_map(map_path)

    zf = zipfile.ZipFile(epub_path)

    all_written = []
    all_warnings = []
    unit_map_by_nn = {u["nn"]: u for u in units}

    for unit in units:
        nn = unit["nn"]
        slug = unit["slug"]
        html_file = unit["html_file"]

        if verbose:
            print(f"Unit {nn} ({slug}) <- {html_file}")

        try:
            html_bytes = zf.read(html_file)
        except KeyError:
            all_warnings.append(f"Unit {nn} ({slug}): epub member {html_file!r} not found")
            continue

        try:
            unit_result = extract_unit(unit, html_bytes, verbose=verbose)
        except ValueError as e:
            all_warnings.append(f"Unit {nn} ({slug}): {e}")
            continue

        all_warnings.extend(unit_result.warnings)

        if dry_run:
            ranges, est_tokens = plan_parts(
                unit_result.body_paragraphs, unit["source_words"], meta, unit["dance_core"], verbose=verbose
            )
            for part_idx, (start, end) in enumerate(ranges, start=1):
                part_paragraphs = unit_result.body_paragraphs[start:end]
                word_count = sum(len(p.split()) for p in part_paragraphs)
                all_written.append({
                    "unit_nn": nn,
                    "slug": slug,
                    "part": part_idx,
                    "part_total": len(ranges),
                    "file_name": file_name_for(slug, nn, part_idx, len(ranges)),
                    "path": None,
                    "word_count": word_count,
                    "line_count": None,
                    "est_tokens": est_tokens / len(ranges) if ranges else est_tokens,
                })
            continue

        written_files = write_unit_files(unit_result, meta, output_dir, verbose=verbose)
        all_written.extend(written_files)

    if dry_run:
        print(f"\n{'=' * 70}")
        print("Fire & Blood splitter — DRY RUN (nothing written)")
        print(f"Epub:  {epub_path}")
        print(f"Map:   {map_path}")
        print(f"Units planned: {len(units)}  |  Output files planned: {len(all_written)}")
        print()
        print(f"{'File':<40} {'Words':>8}  {'~Tokens':>8}")
        print(f"{'-' * 40} {'-' * 8}  {'-' * 8}")
        for wf in sorted(all_written, key=lambda w: (w['unit_nn'], w['part'])):
            print(f"{wf['file_name']:<40} {wf['word_count']:>8,}  {wf['est_tokens']:>8,.0f}")
        if all_warnings:
            print(f"\nWarnings ({len(all_warnings)}):")
            for w in all_warnings:
                print(f"  WARNING: {w}")
        return all_written, all_warnings, None

    qa_warnings, qa_summary = run_qa_gate(all_written, unit_map_by_nn, output_dir, verbose=verbose)
    all_warnings.extend(qa_warnings)

    print_summary(epub_path, map_path, output_dir, all_written, all_warnings, qa_summary, unit_map_by_nn)

    return all_written, all_warnings, qa_summary


def print_summary(epub_path, map_path, output_dir, written_files, warnings, qa_summary, unit_map_by_nn):
    print(f"\n{'=' * 78}")
    print("Fire & Blood splitter")
    print(f"Epub:   {epub_path}")
    print(f"Map:    {map_path}")
    print(f"Output: {output_dir}")

    units_seen = sorted(set(wf["unit_nn"] for wf in written_files))
    print(f"Units processed: {len(units_seen)} / {len(unit_map_by_nn)}")
    print(f"Files written:   {len(written_files)}")
    print()

    # Per-unit summary table (unit, parts, words, tokens, noise score)
    noise_by_file = {}
    if qa_summary:
        for r in qa_summary["ocr_rows"]:
            noise_by_file[r["file_name"]] = r["noise_score"]

    print(f"{'Unit':<6} {'Section':<40} {'Parts':>5} {'Words':>8} {'~Tokens':>8} {'Noise':>6}")
    print(f"{'-' * 6} {'-' * 40} {'-' * 5} {'-' * 8} {'-' * 8} {'-' * 6}")
    by_unit = {}
    for wf in written_files:
        by_unit.setdefault(wf["unit_nn"], []).append(wf)
    for nn in sorted(by_unit.keys()):
        files = sorted(by_unit[nn], key=lambda w: w["part"])
        total_words = sum(f["word_count"] for f in files)
        total_tokens = sum(f["est_tokens"] for f in files)
        total_noise = sum(noise_by_file.get(f["file_name"], 0) for f in files)
        section_title = unit_map_by_nn[nn]["ncx_title"]
        print(
            f"{nn:<6} {section_title[:40]:<40} {len(files):>5} {total_words:>8,} "
            f"{total_tokens:>8,.0f} {total_noise:>6}"
        )

    if qa_summary:
        print()
        print("QA gate:")
        print(f"  PDF-path header leaks: {qa_summary['pdf_path_hits']}"
              + (f"  files={qa_summary['pdf_path_files']}" if qa_summary['pdf_path_hits'] else ""))
        print(f"  Word-count mismatches (>10%): {len(qa_summary['word_count_flags'])}")
        print(f"  Duplicated boundary paragraphs: {qa_summary['dup_paragraph_count']}")
        print(f"  OCR-scan report: {qa_summary['scan_path']}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARNING: {w}")
    else:
        print("\nNo warnings.")


def main():
    parser = argparse.ArgumentParser(
        description="Split the Fire & Blood epub into per-section line-numbered markdown "
                    "with YAML frontmatter, per working/fire-and-blood/unit-map.json."
    )
    parser.add_argument(
        "--epub",
        default=None,
        help="Path to fire-and-blood.epub (default: sources/raw/fire-and-blood.epub)",
    )
    parser.add_argument(
        "--map",
        default=None,
        help="Path to unit-map.json (default: working/fire-and-blood/unit-map.json)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output directory (default: sources/chapters/fab/)",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Compute + report the plan without writing any files (no QA gate run either).",
    )

    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent.parent

    epub_path = args.epub or str(project_dir / "sources" / "raw" / "fire-and-blood.epub")
    map_path = args.map or str(project_dir / "working" / "fire-and-blood" / "unit-map.json")
    output_dir = args.output or str(project_dir / "sources" / "chapters" / "fab")

    if not Path(epub_path).exists():
        print(f"ERROR: Epub not found: {epub_path}", file=sys.stderr)
        sys.exit(1)
    if not Path(map_path).exists():
        print(f"ERROR: unit-map.json not found: {map_path}", file=sys.stderr)
        sys.exit(1)

    split_fire_and_blood(epub_path, map_path, output_dir, verbose=args.verbose, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
