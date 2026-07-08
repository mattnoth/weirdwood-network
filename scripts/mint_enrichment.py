#!/usr/bin/env python3
"""Parameterized enrichment minter — the ONE script every enrichment dip uses (S158).

Replaces the ~33 disposable per-dip `mint_<unit>_enrichment_sNNN.py` scripts. Those were ~95%
identical boilerplate (slug pre-check, re-run guard, quote re-grep/fail-fast, backup, append edges,
create nodes); the only genuinely per-dip content is DATA — the edge list, the new-node bodies, the
run_id / typed_by. This tool reads all of that from a dip's `candidates.json` (+ optional `.node.md`
files) and does the shared steps. The historical per-dip scripts are frozen in
`scripts/enrichment/archive/` (kept, never deleted).

Faithful reproduction: the edge-row construction here is byte-identical to the per-dip scripts
(same key order, same `common()` block, same `norm()` + line-grep). Validated S158 against the S157
euron dip — the rows this produces match `graph/edges/edges.jsonl` for run_id euron-enrichment-s157
byte-for-byte. See `scripts/enrichment/README.md`.

DATA SCHEMA (candidates.json — the schema every dip already writes):
    {
      "_meta": {
        "unit": "A1.6 Kingsmoot / Euron",
        "session": "S157",
        "run_id": "euron-enrichment-s157",      # REQUIRED — drives run_id + (default) typed_by + backup name
        "new_node_slugs": ["..."],              # slugs the slug-pre-check should skip (created this dip)
        "note": "...",                          # free prose, ignored by the tool
        "typed_by": "curator-euron-enrichment", # OPTIONAL — default: curator-<unit>-enrichment from run_id
        "produced_at": "2026-06-27T00:00:00+00:00"  # OPTIONAL — default: --produced-at or today 00:00 UTC
      },
      "edges": [
        {"id":"E1","type":"AGENT_IN","source":"...","target":"...","book":"affc",
         "chapter":"affc-the-reaver-01","quote":"...","tier":"tier-1","note":"...",
         "qualifier":"via_bribe",   # OPTIONAL
         "verify": true}            # OPTIONAL — flags interpretive edges; sets verified_by="pending"
      ]
    }

NEW NODES (data, not embedded Python): drop `<slug>.node.md` files into a `nodes/` dir beside
candidates.json (override with --nodes-dir). Each file's `type:` frontmatter routes it to the right
graph/nodes/<dir>/ (character.* -> characters/, object.artifact -> artifacts/, place.* -> locations/,
event.* -> events/, etc.). The slug set must match _meta.new_node_slugs.

USAGE
  # real mint:
  python scripts/mint_enrichment.py --candidates working/enrichment/<unit>/candidates.json
  # validation (write nowhere near the live graph):
  python scripts/mint_enrichment.py --candidates .../candidates.json \\
      --edges /tmp/edges-copy.jsonl --backup /tmp/backup.jsonl --produced-at 2026-06-27T00:00:00+00:00
"""
import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_arc_lib import precheck_slugs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
EDGES_DEFAULT = REPO / "graph" / "edges" / "edges.jsonl"
NODES_ROOT = REPO / "graph" / "nodes"

# Constants shared by every enrichment dip (overridable via _meta if a future dip needs it).
DEFAULTS = {
    "decision": "emit_edge",
    "candidate_kind": "enrichment-curator-arc",
    "evidence_kind": "book-pass1",
    "schema_version": "pass1-derived-v1",
}

# node `type:` prefix -> graph/nodes/ subdir (the convention the per-dip scripts encoded by hand).
TYPE_DIR_MAP = {
    "character": "characters",
    "place": "locations",
    "object.artifact": "artifacts",
    "object.text": "texts",
    "object.food": "foods",
    "object.material": "materials",
    "event": "events",
    "faction": "factions",
    "house": "houses",
    "prophecy": "prophecies",
    "theory": "theories",
    "concept": "concepts",
    "custom": "customs",
    "language": "languages",
    "religion": "religions",
    "species": "species",
    "title": "titles",
    "medical": "medical",
    "meta.chapter": "chapters",
}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("''", "'")  # OCR artifact in fab source (e.g. `Mushroom’'s`) — collapse after curly conversion
    s = s.replace("—", "-").replace("–", "-").replace("…", "...")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def authoritative_line(book, chapter, quote):
    f = REPO / "sources" / "chapters" / book / f"{chapter}.md"
    if not f.exists():
        sys.exit(f"ABORT: chapter file missing: {f}")
    lines = f.read_text(encoding="utf-8").splitlines()
    # Wrap-aware locator — MUST stay byte-identical to
    # fab-reconcile-candidates.locate_quote's matching loop (S199 fix 3): single-line
    # first, then a growing join of up to `window` consecutive lines so a quote that
    # straddles a mid-paragraph break or a blank-line paragraph gap still locates. If
    # the reconciler located a quote via the join, mint must locate it the same way or
    # it aborts on a quote the reconciler already passed. Widening the window can only
    # find MORE quotes (single-line + short joins still match first, at the same line);
    # it never changes a previously-located line, so it is safe for prior enrichment runs.
    window = 4
    q = norm(quote)
    for i, ln in enumerate(lines, 1):
        if q in norm(ln):
            return i
    n = len(lines)
    for i in range(n):
        # blank-start windows skipped — MUST stay byte-identical to the reconciler's
        # locate_quote (a blank-start match always re-matches from the next non-blank
        # line with more window headroom, so located-vs-not never changes; only the
        # returned line becomes the first ACTUAL text line).
        if not lines[i].strip():
            continue
        joined = lines[i]
        for w in range(1, window):
            if i + w >= n:
                break
            joined = joined + " " + lines[i + w]
            if q in norm(joined):
                return i + 1
    sys.exit(f"ABORT: quote not found in {chapter}.md -> {quote!r}")


def derive_typed_by(run_id):
    """euron-enrichment-s157 -> curator-euron-enrichment (matches the per-dip scripts)."""
    unit = run_id.rsplit("-enrichment-", 1)[0] if "-enrichment-" in run_id else run_id
    return f"curator-{unit}-enrichment"


def derive_unit_slug(run_id):
    """euron-enrichment-s157 -> euron (for the default backup filename)."""
    return run_id.rsplit("-enrichment-", 1)[0] if "-enrichment-" in run_id else run_id


def common(meta, run_id, typed_by, produced_at):
    return {
        "decision": meta.get("decision", DEFAULTS["decision"]),
        "candidate_kind": meta.get("candidate_kind", DEFAULTS["candidate_kind"]),
        "evidence_kind": meta.get("evidence_kind", DEFAULTS["evidence_kind"]),
        "typed_by": typed_by,
        "schema_version": meta.get("schema_version", DEFAULTS["schema_version"]),
        "produced_at": produced_at,
        "run_id": run_id,
    }


def make_edge_row(e, common_block):
    book, chapter = e["book"], e["chapter"]
    line = authoritative_line(book, chapter, e["quote"])
    row = {
        "edge_type": e["type"],
        "source_slug": e["source"],
        "target_slug": e["target"],
        **common_block,
        "evidence_book": book,
        "evidence_chapter": chapter,
        "evidence_ref": f"sources/chapters/{book}/{chapter}.md:{line}",
        "evidence_quote": e["quote"],
        "confidence_tier": e["tier"],
        "asserted_relation": e["note"],
        "candidate_id": e["id"],
    }
    if e.get("qualifier"):
        row["qualifier"] = e["qualifier"]
    if e.get("verify"):
        row["verified_by"] = "pending"
    return row


def _frontmatter_field(body, field):
    m = re.search(rf"^{field}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else None


def route_node_dir(node_type):
    if node_type in TYPE_DIR_MAP:
        return TYPE_DIR_MAP[node_type]
    prefix = node_type.split(".", 1)[0]
    return TYPE_DIR_MAP.get(prefix)


def load_node_specs(nodes_dir, declared_slugs, nodes_root):
    """Read <slug>.node.md files; route each by its `type:` frontmatter. Returns
    [(slug, dest_dir, body)]. Verifies the file set matches _meta.new_node_slugs."""
    specs = []
    found = set()
    if nodes_dir.exists():
        for p in sorted(nodes_dir.glob("*.node.md")):
            body = p.read_text(encoding="utf-8")
            slug = _frontmatter_field(body, "slug") or p.name[: -len(".node.md")]
            ntype = _frontmatter_field(body, "type")
            if not ntype:
                sys.exit(f"ABORT: node file has no `type:` frontmatter: {p}")
            subdir = route_node_dir(ntype)
            if subdir is None:
                sys.exit(f"ABORT: no graph/nodes dir for type {ntype!r} ({p.name})")
            specs.append((slug, nodes_root / subdir, body))
            found.add(slug)
    declared = set(declared_slugs)
    if found != declared:
        missing_files = declared - found
        extra_files = found - declared
        msg = []
        if missing_files:
            msg.append(f"declared in _meta.new_node_slugs but no .node.md file: {sorted(missing_files)}")
        if extra_files:
            msg.append(f".node.md file present but not declared in _meta.new_node_slugs: {sorted(extra_files)}")
        sys.exit("ABORT: node manifest mismatch — " + "; ".join(msg)
                 + f"\n  (looked in {nodes_dir})")
    return specs


def main():
    ap = argparse.ArgumentParser(description="Parameterized enrichment minter (S158).")
    ap.add_argument("--candidates", required=True, type=Path, help="path to a dip's candidates.json")
    ap.add_argument("--edges", type=Path, default=EDGES_DEFAULT, help="edges.jsonl to append to (override for validation)")
    ap.add_argument("--backup", type=Path, default=None, help="backup path (default: graph/edges/_regrounding/edges-pre-<unit>-enrichment-<date>.jsonl)")
    ap.add_argument("--nodes-dir", type=Path, default=None, help="dir of <slug>.node.md files (default: <candidates_dir>/nodes/)")
    ap.add_argument("--nodes-root", type=Path, default=NODES_ROOT, help="graph/nodes root to write into (override for validation)")
    ap.add_argument("--produced-at", default=None, help="ISO produced_at (default: _meta.produced_at or today 00:00 UTC)")
    args = ap.parse_args()

    data = json.loads(args.candidates.read_text(encoding="utf-8"))
    meta = data.get("_meta", {})
    edges = data["edges"]

    run_id = meta.get("run_id")
    if not run_id:
        sys.exit("ABORT: _meta.run_id is required.")
    typed_by = meta.get("typed_by") or derive_typed_by(run_id)
    produced_at = (args.produced_at or meta.get("produced_at")
                   or f"{date.today().isoformat()}T00:00:00+00:00")
    new_node_slugs = set(meta.get("new_node_slugs", []))

    nodes_dir = args.nodes_dir or (args.candidates.parent / "nodes")
    node_specs = load_node_specs(nodes_dir, new_node_slugs, args.nodes_root)

    # 1. slug pre-check (existing targets only — new nodes are created below)
    all_slugs = set()
    for e in edges:
        all_slugs.add(e["source"]); all_slugs.add(e["target"])
    resolved, missing = precheck_slugs(all_slugs - new_node_slugs)
    if missing:
        sys.exit(f"ABORT: slug pre-check failed — non-existent: {sorted(missing)}")
    print(f"Slug pre-check OK: {len(resolved)} existing slugs resolved "
          f"(+{len(new_node_slugs)} new this dip).")

    # 2. re-run guard
    raw = args.edges.read_text(encoding="utf-8").splitlines()
    existing = [ln for ln in raw if ln.strip()]
    if any(run_id in ln for ln in existing):
        sys.exit(f"ABORT: run_id '{run_id}' already present — already minted.")
    print(f"Re-run guard OK: run_id '{run_id}' not present.")

    # 3. build rows — FAIL-fast on any unfound quote
    cb = common(meta, run_id, typed_by, produced_at)
    new_rows = [make_edge_row(e, cb) for e in edges]
    print(f"Line-check OK: all {len(new_rows)} quotes located in source.")

    # 4. backup
    backup = args.backup or (REPO / "graph" / "edges" / "_regrounding"
                             / f"edges-pre-{derive_unit_slug(run_id)}-enrichment-{date.today().isoformat()}.jsonl")
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.edges, backup)
    print(f"Backup written -> {backup}")

    # 5. create new nodes (skip-if-exists, like the per-dip scripts)
    created = []
    for slug, dest_dir, body in node_specs:
        p = dest_dir / f"{slug}.node.md"
        if p.exists():
            print(f"  SKIP node (exists): {p.name}")
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
            created.append(slug)
            try:
                shown = p.relative_to(REPO)
            except ValueError:
                shown = p
            print(f"  Created node: {shown}")

    # 6. append edges
    out = existing + [json.dumps(r, ensure_ascii=False) for r in new_rows]
    args.edges.write_text("\n".join(out) + "\n", encoding="utf-8")

    tc = {}
    for e in edges:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    print("\n── SUMMARY ──")
    print(f"Nodes created ({len(created)}): {', '.join(created) or '(none — edge-only dip)'}")
    print(f"Edges appended ({len(new_rows)}):")
    for t, c in sorted(tc.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
