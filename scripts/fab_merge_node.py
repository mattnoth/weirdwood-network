#!/usr/bin/env python3
"""fab_merge_node.py — Fire & Blood node UPDATE writer (design §5.3, build-spec Script 2).

`scripts/mint_enrichment.py` is skip-if-exists on nodes (verified) — it will NOT update an
existing node file. So UPDATEs to existing nodes (book-grounded Identity swap + a new
`## Fire & Blood` prose section) need a separate writer, or they are silently dropped. This
is that writer. It is the UPDATE half of the F&B pipeline; CREATE nodes + all edges still go
through `mint_enrichment.py`. This script never touches `edges.jsonl`.

VOCABULARY: "Pass" = numbered corpus sweep. "Track" = named workstream. "step" (lowercase) =
ordered piece of a track. "Tier" = confidence 1-5 ONLY. No other capitalized process words.

INPUT — `--merge-plan <path>`: a JSON array of
    {"slug": "...", "identity_line": "..." (optional), "fab_section_md": "...markdown...",
     "run_id": "fab-<slug>-NN-<date>"}

NODE FILE SHAPES (all three handled):
  (a) boilerplate stub    — `## Identity` line matches BOILERPLATE_RE, little/no other prose.
  (b) rich wiki node      — boilerplate Identity line BUT ~90 lines of real wiki-cited prose
                             below it (Origins/Appearances/Narrative Arc/Quotes). The prose
                             + its (wiki:...cite_ref...) anchors are the Tier-2 provenance
                             layer — PRESERVED untouched. Identity STILL gets swapped if its
                             line matches the boilerplate regex (the swap is line-scoped, not
                             node-scoped).
  (c) no-Identity node     — no `## Identity` section at all (body starts at the first other
                             `##` section, e.g. `## Origins`), OR a real (non-boilerplate)
                             Identity line, which is left alone.

ALGORITHM per merge-plan entry — see module docstring sections below (find, idempotency,
identity-by-shape, append-FAB-section, frontmatter-only-node_version-bump, atomic write).

HARD RULE: a merge-plan entry whose slug has no matching node file is a HARD ERROR
(`sys.exit`) — that is the silent-UPDATE-drop failure mode this script exists to prevent
(design R3). Do NOT skip-and-continue on not-found.

CLI
    python scripts/fab_merge_node.py --merge-plan merge-plan.json
    python scripts/fab_merge_node.py --merge-plan merge-plan.json --nodes-root /tmp/nodes-copy
    python scripts/fab_merge_node.py --merge-plan merge-plan.json --dry-run
"""
import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_ROOT_DEFAULT = REPO / "graph" / "nodes"

# Exact regex from the design doc / build spec — matches ONLY the flat wiki-boilerplate
# Identity line ("Eon is a character.human from the AWOIAF wiki."). Must NOT match a real
# prose Identity line (e.g. Rhaenyra's "(97-130 AC) - child of ..." or a book-grounded line).
BOILERPLATE_RE = re.compile(r"^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$")

FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
NODE_VERSION_RE = re.compile(r"^(node_version:\s*)(\d+)(\s*)$", re.MULTILINE)
HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)


def marker_for(run_id: str) -> str:
    return f"<!-- fab-enriched: {run_id} -->"


def find_node_file(slug: str, nodes_root: Path) -> Path | None:
    """Scan graph/nodes/*/<slug>.node.md (direct glob — merge-plan slugs are already
    reconciler-resolved, so this is an existence lookup, not alias resolution)."""
    matches = sorted(nodes_root.glob(f"*/{slug}.node.md"))
    if not matches:
        return None
    return matches[0]


def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Return (frontmatter_inner, body, full_frontmatter_block_with_delims).
    frontmatter_inner is the YAML lines WITHOUT the '---' delimiters (for field bumps).
    body is everything after the closing '---\\n'."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        sys.exit(f"ABORT: node file has no parsable YAML frontmatter block")
    frontmatter_inner = m.group(1)
    body = text[m.end():]
    full_block = m.group(0)
    return frontmatter_inner, body, full_block


def bump_node_version(full_frontmatter_block: str) -> str:
    """Bump node_version by 1 within the frontmatter block. If the field is absent,
    treat as 1 -> insert node_version: 2 (append, right before the closing '---')."""
    if NODE_VERSION_RE.search(full_frontmatter_block):
        def _bump(m):
            return f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}"
        return NODE_VERSION_RE.sub(_bump, full_frontmatter_block, count=1)
    # Absent -> treat as 1 -> set 2. Insert just before the closing '---\n'.
    if not full_frontmatter_block.endswith("---\n"):
        sys.exit("ABORT: frontmatter block does not end with '---\\n' as expected")
    head = full_frontmatter_block[: -len("---\n")]
    if not head.endswith("\n"):
        head += "\n"
    return head + "node_version: 2\n" + "---\n"


def find_section_span(body: str, heading: str) -> tuple[int, int] | None:
    """Find `## <heading>` in body (top-level ## heading only). Returns (start, end)
    character offsets spanning from the heading line to just before the next ## heading
    (or end of body). Returns None if not present."""
    headings = list(HEADING_RE.finditer(body))
    for i, hm in enumerate(headings):
        if hm.group(1).strip() == heading:
            start = hm.start()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
            return start, end
    return None


def first_heading_offset(body: str) -> int:
    """Offset of the first top-level ## heading in body, or len(body) if none."""
    hm = HEADING_RE.search(body)
    return hm.start() if hm else len(body)


def get_identity_line(identity_section: str) -> tuple[str | None, int, int]:
    """Given the full `## Identity ... ` section text, find the single non-blank prose
    line (the Identity line). Returns (line_text_or_None, start_offset, end_offset) of
    that line WITHIN identity_section (end_offset excludes trailing newline)."""
    lines = identity_section.splitlines(keepends=True)
    offset = 0
    for ln in lines:
        stripped = ln.strip()
        if stripped and not stripped.startswith("## "):
            line_no_nl = ln.rstrip("\n")
            return line_no_nl, offset, offset + len(line_no_nl)
        offset += len(ln)
    return None, -1, -1


def build_fab_block(run_id: str, fab_section_md: str) -> str:
    fab_section_md = fab_section_md.strip("\n")
    return f"{marker_for(run_id)}\n\n{fab_section_md}\n"


def process_entry(entry: dict, nodes_root: Path, dry_run: bool) -> dict:
    """Process one merge-plan entry. Returns a result dict:
    {slug, status: merged|skipped_marker, identity_action, fab_action, path}
    Raises SystemExit on not-found (hard error, per design)."""
    slug = entry["slug"]
    run_id = entry["run_id"]
    identity_line = entry.get("identity_line")
    fab_section_md = entry.get("fab_section_md", "")

    path = find_node_file(slug, nodes_root)
    if path is None:
        sys.exit(
            f"ABORT: merge-plan slug not found in {nodes_root}/*/<slug>.node.md: {slug!r}\n"
            f"  This is a HARD ERROR (design R3) — a not-found slug means the UPDATE would be\n"
            f"  silently dropped. Fix the merge-plan (or the reconciler's routing) and re-run."
        )

    text = path.read_text(encoding="utf-8")
    frontmatter_inner, body, full_frontmatter_block = split_frontmatter(text)

    marker = marker_for(run_id)
    if marker in body:
        return {
            "slug": slug, "status": "skipped_marker", "identity_action": "n/a",
            "fab_action": "n/a", "path": str(path),
        }

    # --- Identity handling by shape ---
    identity_span = find_section_span(body, "Identity")
    identity_action = "left_alone_no_section"
    new_body = body

    if identity_span is not None:
        start, end = identity_span
        identity_section = body[start:end]
        line_text, lstart, lend = get_identity_line(identity_section)
        if line_text is not None and BOILERPLATE_RE.match(line_text.strip()):
            if identity_line:
                new_line = identity_line.strip()
                new_identity_section = (
                    identity_section[:lstart] + new_line + identity_section[lend:]
                )
                new_body = body[:start] + new_identity_section + body[end:]
                identity_action = "swapped_boilerplate_line"
            else:
                identity_action = "boilerplate_line_but_no_identity_line_provided_left_alone"
        else:
            identity_action = "left_alone_real_identity"
    else:
        if identity_line:
            insert_at = first_heading_offset(new_body)
            insertion = f"## Identity\n\n{identity_line.strip()}\n\n"
            new_body = new_body[:insert_at] + insertion + new_body[insert_at:]
            identity_action = "inserted_new_section"
        else:
            identity_action = "no_section_no_identity_line_provided_left_alone"

    # --- Fire & Blood section: create or extend ---
    fab_span = find_section_span(new_body, "Fire & Blood")
    fab_block = build_fab_block(run_id, fab_section_md)
    if fab_span is None:
        if not new_body.endswith("\n"):
            new_body += "\n"
        if new_body and not new_body.endswith("\n\n"):
            new_body += "\n"
        new_body = new_body + f"## Fire & Blood\n\n{fab_block}"
        fab_action = "section_created"
    else:
        fstart, fend = fab_span
        existing_section = new_body[fstart:fend]
        if not existing_section.endswith("\n"):
            existing_section += "\n"
        if not existing_section.endswith("\n\n"):
            existing_section += "\n"
        extended_section = existing_section + fab_block
        new_body = new_body[:fstart] + extended_section + new_body[fend:]
        fab_action = "section_extended"

    # --- frontmatter: bump node_version only ---
    new_frontmatter_block = bump_node_version(full_frontmatter_block)
    new_text = new_frontmatter_block + new_body

    if not dry_run:
        atomic_write(path, new_text)

    return {
        "slug": slug, "status": "merged", "identity_action": identity_action,
        "fab_action": fab_action, "path": str(path),
    }


def atomic_write(path: Path, text: str) -> None:
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_name, path)
    except Exception:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
        raise


def main():
    ap = argparse.ArgumentParser(
        description="Fire & Blood node UPDATE writer — merges book-grounded prose into "
                    "existing nodes (Identity swap + ## Fire & Blood section append)."
    )
    ap.add_argument("--merge-plan", required=True, type=Path, help="path to merge-plan.json")
    ap.add_argument("--nodes-root", type=Path, default=NODES_ROOT_DEFAULT,
                    help="graph/nodes root to write into (override for testing)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what WOULD change per node; write nothing")
    args = ap.parse_args()

    plan = json.loads(args.merge_plan.read_text(encoding="utf-8"))
    if not isinstance(plan, list):
        sys.exit("ABORT: merge-plan must be a JSON array")

    merged = []
    skipped = []
    for entry in plan:
        result = process_entry(entry, args.nodes_root, args.dry_run)
        if result["status"] == "merged":
            merged.append(result)
            tag = "[DRY-RUN] would merge" if args.dry_run else "MERGED"
            print(f"  {tag} {result['slug']}: identity={result['identity_action']}, "
                  f"fab={result['fab_action']} ({result['path']})")
        else:
            skipped.append(result)
            print(f"  SKIP (marker present) {result['slug']} ({result['path']})")

    print("\n── SUMMARY ──")
    print(f"merged: {len(merged)}")
    print(f"skipped(marker): {len(skipped)}")
    print(f"not-found(=abort): 0  (any not-found slug aborts the run immediately, see above)")
    if args.dry_run:
        print("(dry-run: no files were written)")


if __name__ == "__main__":
    main()
