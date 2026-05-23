#!/usr/bin/env python3
"""
stage4-classify-comention-review.py

Formats co-mention candidates from a JSONL file into a readable text review
for systematic edge classification. One block per candidate, printed to stdout.

Usage:
    python scripts/stage4-classify-comention-review.py <candidates.jsonl>

The input file may be either:
  - An enriched candidates file (has target_type, valid_edge_types,
    evidence_paragraph fields — produced by the enrichment step)
  - A plain candidates file (has source_section, snippet, backlink_count only)

For plain files, the script attempts to locate the source's prose file
(at <bucket_dir>/prose/<source_slug>.prose.md) to display the evidence
paragraph. If the prose file is not found, the snippet field is shown instead.

Output format per candidate:
  === 1/135 ===
  pair_a:  a-clash-of-kings-chapter-46
  pair_b:  bran-stark
  type_b:  character.human  [or: UNKNOWN if not enriched]
  section: ## Narrative Arc
  snippet: ...context excerpt with target highlighted in «guillemets»...
  paragraph:
    Full evidence paragraph text (or snippet if unavailable)
  valid_edge_types:
    KILLS, PARENT_OF, SERVES, ...  (or: [not available] if plain format)
"""

import argparse
import json
import sys
import textwrap
from pathlib import Path


def load_candidates(path: Path) -> list[dict]:
    """Load all candidates from a JSONL file, skipping malformed lines."""
    candidates = []
    line_errors = 0
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"WARNING: skipping malformed JSON on line {lineno}: {exc}",
                    file=sys.stderr,
                )
                line_errors += 1
    if line_errors:
        print(
            f"WARNING: {line_errors} line(s) skipped due to JSON parse errors.",
            file=sys.stderr,
        )
    return candidates


def find_prose_file(candidates_path: Path, source_slug: str) -> Path | None:
    """
    Try to locate the prose file for the source entity relative to the
    candidates file's directory.

    Candidates typically live at:
      <bucket_dir>/prose-edge-candidates/<slug>.candidates.jsonl
      <bucket_dir>/prose-edge-candidates-enriched/<slug>.candidates.jsonl
      <bucket_dir>/comention-candidates/<slug>.candidates.jsonl

    Prose files live at:
      <bucket_dir>/prose/<slug>.prose.md
    """
    # Walk up until we find a sibling 'prose' directory
    parent = candidates_path.parent
    for _ in range(3):  # at most 3 levels up
        prose_candidate = parent / "prose" / f"{source_slug}.prose.md"
        if prose_candidate.exists():
            return prose_candidate
        parent = parent.parent
    return None


def load_prose_paragraphs(prose_path: Path) -> dict[str, list[str]]:
    """
    Parse a prose.md file into a dict mapping section heading (e.g.
    "## Narrative Arc") to a list of paragraph strings.

    Section headings are lines that start with '#'. Blank lines delimit
    paragraphs within a section.
    """
    sections: dict[str, list[str]] = {}
    current_section = "(no section)"
    current_para_lines: list[str] = []

    def flush_para():
        text = " ".join(current_para_lines).strip()
        if text:
            sections.setdefault(current_section, []).append(text)
        current_para_lines.clear()

    with prose_path.open("r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\n")
            if line.startswith("#"):
                flush_para()
                current_section = line.strip()
            elif line.strip() == "":
                flush_para()
            else:
                current_para_lines.append(line.strip())
    flush_para()
    return sections


def get_evidence_paragraph(
    candidate: dict,
    prose_sections: dict[str, list[str]] | None,
) -> str | None:
    """
    Return the evidence paragraph text.

    Priority:
      1. candidate['evidence_paragraph'] (enriched format, pre-computed)
      2a. Look up by section + paragraph_index in prose_sections when
          candidate carries an evidence_paragraphs list of
          {section, paragraph_index} dicts (comention-edges output format)
      2b. Look up by source_section alone in prose_sections when the candidate
          has no paragraph_index hint (plain candidates.jsonl format). Uses the
          first paragraph in the named section.
      3. Fall back to candidate['snippet']
    """
    # 1. Enriched: evidence_paragraph is already the full text
    if "evidence_paragraph" in candidate and candidate["evidence_paragraph"]:
        return candidate["evidence_paragraph"]

    if prose_sections:
        # 2a. Structured hint from comention-edges output
        if "evidence_paragraphs" in candidate:
            hints = candidate["evidence_paragraphs"]
            if hints:
                first = hints[0]
                section = first.get("section", "")
                para_idx = first.get("paragraph_index", 0)
                paras = prose_sections.get(section, [])
                if para_idx < len(paras):
                    return paras[para_idx]

        # 2b. Section-only lookup for plain candidates.jsonl (no paragraph_index)
        section = candidate.get("source_section", "")
        if section:
            paras = prose_sections.get(section, [])
            if paras:
                return paras[0]

    # 3. Snippet fallback
    return candidate.get("snippet")


def wrap_text(text: str, width: int = 100, indent: str = "    ") -> str:
    """Wrap text to width with a consistent indent."""
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)


def format_valid_edge_types(types: list[str] | None) -> str:
    """Format the valid_edge_types list for display."""
    if not types:
        return "    [not available]"
    # Wrap the comma-separated list
    joined = ", ".join(types)
    return wrap_text(joined, width=100, indent="    ")


def format_candidate_block(
    idx: int,
    total: int,
    candidate: dict,
    prose_sections: dict[str, list[str]] | None,
) -> str:
    """Format a single candidate into a human-readable review block."""
    pair_a = candidate.get("source_slug", "(unknown)")
    pair_b = candidate.get("target_slug", "(unknown)")
    target_type = candidate.get("target_type", "UNKNOWN")
    section = candidate.get("source_section", "(no section)")
    snippet = candidate.get("snippet", "")
    valid_edge_types = candidate.get("valid_edge_types")

    # Evidence paragraph
    para = get_evidence_paragraph(candidate, prose_sections)
    if para:
        para_display = wrap_text(para, width=100, indent="    ")
    else:
        para_display = "    [no paragraph available]"

    # valid_edge_types
    vet_display = format_valid_edge_types(valid_edge_types)

    lines = [
        f"=== {idx}/{total} ===",
        f"pair_a:  {pair_a}",
        f"pair_b:  {pair_b}",
        f"type_b:  {target_type}",
        f"section: {section}",
        f"snippet: {snippet}",
        "paragraph:",
        para_display,
        "valid_edge_types:",
        vet_display,
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Format co-mention candidates as a readable review for edge classification."
        )
    )
    parser.add_argument(
        "candidates_file",
        type=Path,
        help="Path to the input candidates JSONL file.",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        metavar="N",
        help="Start at candidate N (1-based). Useful for resuming mid-file. Default: 1.",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        metavar="N",
        help="Stop after candidate N (inclusive, 1-based). Default: all.",
    )
    args = parser.parse_args()

    candidates_path: Path = args.candidates_file.resolve()
    if not candidates_path.exists():
        print(f"ERROR: file not found: {candidates_path}", file=sys.stderr)
        sys.exit(1)

    candidates = load_candidates(candidates_path)
    total = len(candidates)
    if total == 0:
        print("No candidates found in input file.", file=sys.stderr)
        sys.exit(0)

    # Determine whether this is an enriched file by inspecting the first row
    is_enriched = "evidence_paragraph" in candidates[0]

    # For plain files, try to load the prose file so we can show full paragraphs.
    # The source_slug in a per-chapter candidates file is the chapter slug itself.
    prose_sections: dict[str, list[str]] | None = None
    if not is_enriched:
        source_slug = candidates[0].get("source_slug", "")
        prose_path = find_prose_file(candidates_path, source_slug)
        if prose_path:
            prose_sections = load_prose_paragraphs(prose_path)
            print(
                f"INFO: loaded prose from {prose_path} ({sum(len(v) for v in prose_sections.values())} paragraphs)",
                file=sys.stderr,
            )
        else:
            print(
                f"INFO: prose file not found for '{source_slug}'; will use snippet field.",
                file=sys.stderr,
            )

    # Apply start/end window (convert to 0-based slice)
    start_idx = max(1, args.start)
    end_idx = args.end if args.end is not None else total
    end_idx = min(end_idx, total)

    if start_idx > total:
        print(
            f"WARNING: --start {start_idx} exceeds total candidates ({total}). Nothing to display.",
            file=sys.stderr,
        )
        sys.exit(0)

    selected = candidates[start_idx - 1 : end_idx]

    # Print blocks
    separator = "\n" + ("-" * 80) + "\n"
    blocks = []
    for local_i, candidate in enumerate(selected):
        global_i = start_idx + local_i
        block = format_candidate_block(global_i, total, candidate, prose_sections)
        blocks.append(block)

    print(separator.join(blocks))

    # Summary footer to stderr so it doesn't pollute stdout piping
    print(
        f"\n--- Displayed {len(selected)} of {total} candidates "
        f"(range {start_idx}–{end_idx}) ---",
        file=sys.stderr,
    )
    if not is_enriched and prose_sections is None:
        print(
            "NOTE: this is a plain (non-enriched) candidates file without a prose file "
            "found nearby. target_type and valid_edge_types will show UNKNOWN / [not available]. "
            "Consider running the enrichment step first, or pass an enriched file.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
