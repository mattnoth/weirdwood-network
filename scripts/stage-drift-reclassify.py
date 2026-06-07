#!/usr/bin/env python3
"""
stage-drift-reclassify.py

Produces STAGING CANDIDATES for the 12 event-node category-drift cases identified in
Plate 2.5 (working/edge-modeling/event-node-inventory.md).

These nodes are POV-chapter articles (ASOS Prologue/Epilogue, Winds of Winter preview
chapters) that were misfiled as event.battle by the wiki-ingest pass. The correct type
is meta.chapter (out-of-universe literary container).

READ-ONLY: does NOT modify any file under graph/. All output goes to
working/edge-modeling/.

Outputs:
  working/edge-modeling/drift-reclassify-candidates.jsonl
  working/edge-modeling/drift-reclassify-summary.md

Usage:
  python3 scripts/stage-drift-reclassify.py
  python3 scripts/stage-drift-reclassify.py --repo-root /path/to/asoiaf-chat
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DRIFT_SLUGS = [
    "a-storm-of-swords-epilogue",
    "a-storm-of-swords-prologue",
    "alayne-i-the-winds-of-winter",
    "arianne-i-the-winds-of-winter",
    "arianne-ii-the-winds-of-winter",
    "barristan-i-the-winds-of-winter",
    "barristan-ii-the-winds-of-winter",
    "mercy-the-winds-of-winter",
    "the-forsaken-the-winds-of-winter",
    "theon-i-the-winds-of-winter",
    "tyrion-ii-the-winds-of-winter",
    "victarion-i-the-winds-of-winter",
]

# Patterns that confirm a node is a chapter article (not an in-world event)
# matched against the slug
CHAPTER_PATTERNS = [
    # "name-i-the-winds-of-winter", "name-ii-the-winds-of-winter", etc.
    re.compile(r"^[a-z\-]+-(?:i|ii|iii|iv|v)-the-winds-of-winter$"),
    # "mercy-the-winds-of-winter" (no roman numeral)
    re.compile(r"^[a-z]+-the-winds-of-winter$"),
    # "the-forsaken-the-winds-of-winter"
    re.compile(r"^the-[a-z]+-the-winds-of-winter$"),
    # ASOS prologue / epilogue
    re.compile(r"^a-storm-of-swords-(?:prologue|epilogue)$"),
]

PROPOSED_TYPE = "meta.chapter"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields from a markdown file (simple key: value only)."""
    fm = {}
    in_fm = False
    for i, line in enumerate(text.splitlines()):
        if i == 0 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if line.strip() == "---":
                break
            m = re.match(r'^(\w[\w_]*):\s*(.+)$', line)
            if m:
                key = m.group(1)
                val = m.group(2).strip().strip('"')
                fm[key] = val
    return fm


def is_chapter_slug(slug: str) -> bool:
    """Return True if the slug matches any chapter-article pattern."""
    for pat in CHAPTER_PATTERNS:
        if pat.match(slug):
            return True
    return False


def build_rationale(slug: str, name: str) -> str:
    """Build a human-readable rationale string for the proposed reclassification."""
    if "winds-of-winter" in slug:
        book = "The Winds of Winter"
        # Derive POV name from slug: strip trailing "-the-winds-of-winter"
        pov_part = re.sub(r"-the-winds-of-winter$", "", slug)
        # Preserve roman numerals in uppercase; title() would lowercase "ii" → "Ii"
        tokens = pov_part.replace("-", " ").split()
        roman = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}
        pov_display = " ".join(
            t.upper() if t.lower() in roman else t.capitalize() for t in tokens
        )
        return (
            f'Wiki page "{name}" is a chapter-summary article for '
            f'"{pov_display}" in {book}. '
            f"It describes a POV chapter, not an in-world event. "
            f"Reclassify from event.battle to meta.chapter."
        )
    elif "a-storm-of-swords-prologue" in slug:
        return (
            f'Wiki page "{name}" is the chapter-summary article for the ASOS Prologue. '
            f"It describes a POV chapter, not an in-world event. "
            f"Reclassify from event.battle to meta.chapter."
        )
    elif "a-storm-of-swords-epilogue" in slug:
        return (
            f'Wiki page "{name}" is the chapter-summary article for the ASOS Epilogue. '
            f"It describes a POV chapter (Merrett Frey / Lady Stoneheart reveal), "
            f"not an in-world event. "
            f"Reclassify from event.battle to meta.chapter."
        )
    else:
        return (
            f'Wiki page "{name}" appears to be a chapter-summary article '
            f"misfiled as event.battle. "
            f"Reclassify to meta.chapter pending human review."
        )


def scan_edges(edges_path: Path, slugs: set) -> dict:
    """
    Scan edges.jsonl for any edge referencing the given slugs.

    Returns:
        {slug: [edge_dict, ...]}  — keyed by the matching slug(s) per edge
    """
    affected: dict = {slug: [] for slug in slugs}

    if not edges_path.exists():
        print(f"WARNING: edges.jsonl not found at {edges_path}", file=sys.stderr)
        return affected

    with edges_path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                edge = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"WARNING: JSON parse error on line {lineno}: {exc}", file=sys.stderr)
                continue

            src = edge.get("source_slug", "")
            tgt = edge.get("target_slug", "")
            for slug in slugs:
                if src == slug or tgt == slug:
                    affected[slug].append(edge)

    return affected


def format_edge_row(edge: dict, slug: str) -> str:
    """Format a single edge as a markdown table row for the summary."""
    etype = edge.get("edge_type", edge.get("type", "?"))
    src = edge.get("source_slug", "?")
    tgt = edge.get("target_slug", "?")
    role = "source" if src == slug else "target"
    other = tgt if role == "source" else src
    evidence = edge.get("evidence_chapter", edge.get("evidence", ""))
    return f"| `{slug}` | `{etype}` | {role} | `{other}` | {evidence} |"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Stage reclassification candidates for 12 category-drift event nodes."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("/Users/mnoth/source/asoiaf-chat"),
        help="Path to the repository root (default: /Users/mnoth/source/asoiaf-chat)",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    nodes_dir = repo / "graph" / "nodes" / "events"
    edges_path = repo / "graph" / "edges" / "edges.jsonl"
    out_dir = repo / "working" / "edge-modeling"
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = out_dir / "drift-reclassify-candidates.jsonl"
    summary_path = out_dir / "drift-reclassify-summary.md"

    print(f"Repository root : {repo}")
    print(f"Nodes directory : {nodes_dir}")
    print(f"Edges file      : {edges_path}")
    print(f"Output directory: {out_dir}")
    print()

    # ------------------------------------------------------------------
    # Step 1: Read each node file and collect metadata
    # ------------------------------------------------------------------
    print("Reading node files...")
    records = []  # list of dicts
    needs_human_judgment = []  # slugs flagged for human review

    for slug in DRIFT_SLUGS:
        node_path = nodes_dir / f"{slug}.node.md"
        if not node_path.exists():
            print(f"  WARNING: node file not found: {node_path}", file=sys.stderr)
            continue

        text = node_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        current_type = fm.get("type", "UNKNOWN")
        name = fm.get("name", slug)
        wiki_source = fm.get("wiki_source", "")

        # Step 2: Confirm it matches the chapter-article pattern
        confirmed_chapter = is_chapter_slug(slug)

        if confirmed_chapter:
            proposed = PROPOSED_TYPE
            flag_human = False
            rationale = build_rationale(slug, name)
        else:
            # The slug doesn't match any chapter pattern — flag for human review
            proposed = "NEEDS_HUMAN_JUDGMENT"
            flag_human = True
            rationale = (
                f'Slug "{slug}" does not match any known chapter-article naming '
                f"pattern. The inventory flagged this as category drift, but the "
                f"correct reclassification is uncertain. Human review required."
            )
            needs_human_judgment.append(slug)

        records.append({
            "slug": slug,
            "name": name,
            "current_type": current_type,
            "proposed_type": proposed,
            "rationale": rationale,
            "wiki_source": wiki_source,
            "flag_human": flag_human,
        })

    print(f"  Loaded {len(records)} node records.")

    # ------------------------------------------------------------------
    # Step 3: Scan edges.jsonl for affected edges
    # ------------------------------------------------------------------
    print("Scanning edges.jsonl for affected edges...")
    slug_set = {r["slug"] for r in records}
    affected = scan_edges(edges_path, slug_set)

    # Attach affected_edge_count to each record
    for rec in records:
        rec["affected_edge_count"] = len(affected.get(rec["slug"], []))

    total_affected_edges = sum(len(v) for v in affected.values())
    slugs_with_edges = [slug for slug, edges in affected.items() if edges]
    print(f"  Total affected edges: {total_affected_edges}")
    print(f"  Slugs with edges    : {len(slugs_with_edges)}")

    # ------------------------------------------------------------------
    # Step 4a: Write candidates.jsonl
    # ------------------------------------------------------------------
    print(f"Writing {candidates_path.name}...")
    with candidates_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            row = {
                "slug": rec["slug"],
                "current_type": rec["current_type"],
                "proposed_type": rec["proposed_type"],
                "rationale": rec["rationale"],
                "affected_edge_count": rec["affected_edge_count"],
            }
            fh.write(json.dumps(row) + "\n")
    print(f"  Wrote {len(records)} rows.")

    # ------------------------------------------------------------------
    # Step 4b: Write summary.md
    # ------------------------------------------------------------------
    print(f"Writing {summary_path.name}...")
    lines = []
    lines.append("# Drift Reclassify Candidates — Staging Summary")
    lines.append("")
    lines.append(
        "Generated by `scripts/stage-drift-reclassify.py`. "
        "READ-ONLY — no graph/ files were modified. "
        "Matt must approve before any merge."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Nodes evaluated:** {len(records)}")
    lines.append(f"- **Auto-proposed as `meta.chapter`:** {len(records) - len(needs_human_judgment)}")
    lines.append(f"- **Flagged for human judgment (uncertain):** {len(needs_human_judgment)}")
    lines.append(f"- **Nodes with affected edges:** {len(slugs_with_edges)}")
    lines.append(f"- **Total affected edge count:** {total_affected_edges}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Reclassification Table")
    lines.append("")
    lines.append(
        "| Slug | Name | Current Type | Proposed Type | Affected Edges | Flag |"
    )
    lines.append(
        "|------|------|-------------|---------------|---------------|------|"
    )
    for rec in records:
        flag_str = "HUMAN REVIEW" if rec["flag_human"] else "auto"
        edge_count = rec["affected_edge_count"]
        lines.append(
            f"| `{rec['slug']}` | {rec['name']} | `{rec['current_type']}` "
            f"| `{rec['proposed_type']}` | {edge_count} | {flag_str} |"
        )
    lines.append("")
    lines.append("### Rationale (per node)")
    lines.append("")
    for rec in records:
        lines.append(f"**`{rec['slug']}`**")
        lines.append(f"> {rec['rationale']}")
        lines.append("")

    # ------------------------------------------------------------------
    # Affected edges section
    # ------------------------------------------------------------------
    lines.append("---")
    lines.append("")
    lines.append("## Affected Edges")
    lines.append("")

    if total_affected_edges == 0:
        lines.append(
            "No edges in `graph/edges/edges.jsonl` reference any of the 12 drift "
            "slugs. Reclassification would have zero edge impact."
        )
    else:
        lines.append(
            "These edges reference one of the 12 drift slugs as `source_slug` or "
            "`target_slug`. They would be affected by reclassification and require "
            "human decision: drop, re-point, or reinterpret as citation/provenance edges."
        )
        lines.append("")
        lines.append(
            "| Drift Slug | Edge Type | Role | Other Endpoint | Evidence |"
        )
        lines.append(
            "|-----------|-----------|------|---------------|----------|"
        )
        for slug in DRIFT_SLUGS:
            for edge in affected.get(slug, []):
                lines.append(format_edge_row(edge, slug))

        lines.append("")
        lines.append("### Impact analysis by edge type")
        lines.append("")
        lines.append(
            "When reclassified to `meta.chapter`, edges whose semantics depend on "
            "the target being an in-world event (e.g., `FIGHTS_IN`, `COMMANDS_IN`, "
            "`ATTENDS`, `AGENT_IN`, `VICTIM_IN`) become semantically invalid. "
            "They should be reviewed for either:"
        )
        lines.append("")
        lines.append(
            "- **Drop:** the relationship doesn't survive reclassification "
            "(e.g., you can't fight in a chapter)."
        )
        lines.append(
            "- **Re-point:** redirect the edge to the actual in-world event node "
            "that occurs within that chapter."
        )
        lines.append(
            "- **Convert to citation:** if the edge just means 'this character "
            "appears in this chapter', a `FEATURED_IN` or `APPEARS_IN` provenance "
            "edge to the `meta.chapter` node may be appropriate — but that edge "
            "type would need to be added to the taxonomy first."
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    # ------------------------------------------------------------------
    # Needs human judgment section
    # ------------------------------------------------------------------
    lines.append("## Needs Human Judgment")
    lines.append("")

    if not needs_human_judgment:
        lines.append(
            "All 12 nodes matched a known chapter-article naming pattern. "
            "No cases require human judgment on the proposed type — "
            "all are auto-proposed as `meta.chapter`."
        )
    else:
        lines.append(
            "The following slugs did NOT match any known chapter-article naming "
            "pattern. The inventory flagged them as drift, but the auto-classifier "
            "is not confident in the proposed type. Human review required before "
            "any reclassification is merged."
        )
        lines.append("")
        for slug in needs_human_judgment:
            rec = next(r for r in records if r["slug"] == slug)
            lines.append(f"- **`{slug}`** — {rec['name']}")
            lines.append(f"  - wiki_source: {rec['wiki_source']}")
            lines.append(f"  - {rec['rationale']}")
            lines.append("")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Merge Gate")
    lines.append("")
    lines.append(
        "This file is a STAGING CANDIDATE only. No changes to `graph/` "
        "should be made until Matt has reviewed and signed off. "
        "The actual merge script (when written) should:"
    )
    lines.append("")
    lines.append(
        "1. For each approved slug, update `graph/nodes/events/<slug>.node.md`: "
        "change `type: event.battle` to `type: meta.chapter` and move the file "
        "to `graph/nodes/meta/<slug>.node.md` (or keep in events/ with a clear "
        "type label — directory convention TBD)."
    )
    lines.append(
        "2. Resolve each affected edge per the human decision: drop / re-point / convert."
    )
    lines.append(
        "3. Re-run `build-edge-type-counts.py` and the event-node inventory to "
        "confirm the drift list is cleared."
    )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Written.")

    # ------------------------------------------------------------------
    # Terminal summary
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Nodes processed         : {len(records)}")
    print(f"  Auto-proposed meta.chapter: {len(records) - len(needs_human_judgment)}")
    print(f"  Needs human judgment    : {len(needs_human_judgment)}")
    if needs_human_judgment:
        for s in needs_human_judgment:
            print(f"    - {s}")
    print(f"  Nodes with affected edges: {len(slugs_with_edges)}")
    if slugs_with_edges:
        for s in slugs_with_edges:
            print(f"    - {s} ({len(affected[s])} edges)")
    else:
        print("    (none — zero edge impact)")
    print(f"  Total affected edges    : {total_affected_edges}")
    print()
    print("Output files:")
    print(f"  {candidates_path}")
    print(f"  {summary_path}")


if __name__ == "__main__":
    main()
