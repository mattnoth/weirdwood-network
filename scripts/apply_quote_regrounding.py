#!/usr/bin/env python3
"""apply_quote_regrounding.py — S195 apply step for quote re-grounding.

Merges the staging proposals (propose_quote_regrounding.py) with reviewer
verdicts (s195-review-batch*.json) and hand-fix overrides
(s195-handfix-overrides.json), RE-VALIDATES every final (text, cite) with the
same logic the verifiers use, then rewrites:

  * node `## Quotes` blocks (quote text -> the verbatim span; cite repointed;
    attribution replaced when a reviewer supplied attribution_fix)
  * edges.jsonl evidence_quote / evidence_ref (backup written first)

Disposition resolution per staging row:
  - override file wins over reviewer verdicts
  - reviewed rows: accept -> proposed_*, adjust -> adjusted_*, park -> skip
  - unreviewed edge a-class rows (deterministic repoints): auto-accept
  - d-no-source rows without an override: park
Any final pair that fails re-validation is parked loudly, never written.

Usage: python3 scripts/apply_quote_regrounding.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from propose_quote_regrounding import node_check, edge_check, CITE_RE  # noqa: E402

STAGING = REPO / "working" / "quote-census" / "s195-regrounding-staging.json"
REVIEWS = sorted((REPO / "working" / "quote-census").glob("s195-review-batch*.json"))
OVERRIDES = REPO / "working" / "quote-census" / "s195-handfix-overrides.json"
EDGES = REPO / "graph" / "edges" / "edges.jsonl"
PARK_REPORT = REPO / "working" / "quote-census" / "s195-parked-rows.md"


# ---------- node `## Quotes` block scanner (mirrors weirwood_query parse_quotes) ----------

def scan_quote_blocks(lines: list[str], qstart: int, qend: int):
    """Yield dicts describing each quote block in lines[qstart:qend]:
    text, cite, text_line_idxs (absolute), attr_line_idx (absolute or None)."""
    i = qstart
    while i < qend:
        if lines[i].lstrip().startswith(">"):
            block_idxs = []
            while i < qend and lines[i].lstrip().startswith(">"):
                block_idxs.append(i)
                i += 1
            stripped = [re.sub(r"^\s*>\s?", "", lines[j]) for j in block_idxs]
            attr_pos = next(
                (k for k in range(len(stripped) - 1, -1, -1)
                 if stripped[k].lstrip().startswith("—")),
                None,
            )
            attr_line_idx = None
            if attr_pos is not None:
                attr_line_idx = block_idxs[attr_pos]
                text_idxs = block_idxs[:attr_pos]
                text_parts = stripped[:attr_pos]
            else:
                text_idxs = block_idxs
                text_parts = stripped
            text = " ".join(s.strip() for s in text_parts if s.strip()).strip()
            j = i
            while j < qend and not lines[j].strip():
                j += 1
            if attr_line_idx is None and j < qend and lines[j].lstrip().startswith("—"):
                attr_line_idx = j
                i = j + 1
            cite = None
            if attr_line_idx is not None:
                # same pattern as weirwood_query.load._CITE_RE
                cm = re.search(r"`?(sources/chapters/[a-z0-9/_-]+?\.md:\d+)`?",
                               lines[attr_line_idx], re.I)
                if cm:
                    cite = cm.group(1)
            yield {
                "text": text,
                "cite": cite,
                "text_line_idxs": text_idxs,
                "attr_line_idx": attr_line_idx,
                "attr_in_block": attr_pos is not None,
            }
        else:
            i += 1


def quotes_section_bounds(lines: list[str]):
    start = next((i for i, ln in enumerate(lines) if re.match(r"^## Quotes[ \t]*$", ln)), None)
    if start is None:
        return None, None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start + 1, end


def apply_node_row(row: dict, final_text: str, final_cite: str,
                   attribution_fix: str | None, dry: bool) -> str | None:
    """Rewrite one node quote block. Returns error string or None on success."""
    path = REPO / row["node_file"]
    lines = path.read_text(encoding="utf-8").splitlines()
    qs, qe = quotes_section_bounds(lines)
    if qs is None:
        return "no ## Quotes section"
    target = None
    for blk in scan_quote_blocks(lines, qs, qe):
        if blk["text"] == row["old_text"] and blk["cite"] == row["old_cite"]:
            target = blk
            break
    if target is None:
        return "quote block not found (old_text+old_cite)"
    if not target["text_line_idxs"]:
        return "quote block has no text lines"
    if target["attr_line_idx"] is None:
        return "quote block has no attribution line to carry the cite"

    # replace text lines with a single quoted line
    first = target["text_line_idxs"][0]
    for idx in sorted(target["text_line_idxs"][1:], reverse=True):
        del lines[idx]
        if target["attr_line_idx"] > idx:
            target["attr_line_idx"] -= 1
    indent = re.match(r"^\s*", lines[first]).group(0)
    lines[first] = f"{indent}> {final_text}"

    ai = target["attr_line_idx"]
    if attribution_fix:
        prefix = "> — " if target["attr_in_block"] else "— "
        new_attr = f"{prefix}{attribution_fix}"
        if "sources/chapters/" not in new_attr:
            new_attr += f" (`{final_cite}`)"
        # preserve a trailing [Lnnn] ledger token if present on the old line
        led = re.search(r"\s(\[L\d+\])\s*$", lines[ai])
        if led and led.group(1) not in new_attr:
            new_attr += f" {led.group(1)}"
        lines[ai] = new_attr
    else:
        if row["old_cite"] not in lines[ai]:
            return "old cite not on attribution line"
        lines[ai] = lines[ai].replace(row["old_cite"], final_cite)

    if not dry:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return None


# ---------- main ----------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    staging = json.loads(STAGING.read_text())["rows"]
    verdicts: dict[int, dict] = {}
    for f in REVIEWS:
        for v in json.loads(f.read_text()):
            verdicts[v["index"]] = v
    if OVERRIDES.exists():
        for v in json.loads(OVERRIDES.read_text()):
            verdicts[v["index"]] = v

    applied_node = applied_edge = 0
    parked: list[str] = []
    edge_jobs: list[tuple[dict, str, str]] = []

    for i, row in enumerate(staging):
        v = verdicts.get(i)
        tag = row.get("slug") or f"{row.get('source_slug')}--{row.get('edge_type')}-->{row.get('target_slug')}"
        # resolve disposition
        if v and v["verdict"] == "park":
            parked.append(f"[{i}] {row['scope']} {tag} — reviewer park: {v.get('reason','')}")
            continue
        if v and v["verdict"] == "adjust":
            final_text, final_cite = v["adjusted_text"], v["adjusted_cite"]
        elif v and v["verdict"] == "accept":
            final_text, final_cite = row["proposed_text"], row["proposed_cite"]
        elif row["class"] == "d-no-source":
            why = row.get("note", "no plausible source")
            if row["scope"] == "edge" and row.get("verdict") == "ok_widened":
                why = "LEFT AS-IS: passes verifier default gate (ok_widened; fragments span >±2 lines)"
            parked.append(f"[{i}] {row['scope']} {tag} — {why}")
            continue
        elif row["scope"] == "edge" and row["class"] == "a-exact-elsewhere":
            final_text, final_cite = row["proposed_text"], row["proposed_cite"]
        else:
            parked.append(f"[{i}] {row['scope']} {tag} — UNREVIEWED non-deterministic row, not applied")
            continue

        # re-validate before writing
        if row["scope"] == "node":
            ok = node_check(final_cite, final_text)
        else:
            ok = edge_check({"evidence_ref": final_cite, "evidence_quote": final_text})[0] == "ok"
        if not ok:
            parked.append(f"[{i}] {row['scope']} {tag} — FINAL PAIR FAILED RE-VALIDATION, not applied")
            continue

        if row["scope"] == "node":
            err = apply_node_row(row, final_text, final_cite,
                                 (v or {}).get("attribution_fix"), args.dry_run)
            if err:
                parked.append(f"[{i}] node {tag} — apply error: {err}")
            else:
                applied_node += 1
        else:
            edge_jobs.append((row, final_text, final_cite))

    # edges: single pass over edges.jsonl
    if edge_jobs:
        lines = EDGES.read_text(encoding="utf-8").splitlines()
        pending = {}
        for row, ft, fc in edge_jobs:
            key = (row["source_slug"], row["edge_type"], row["target_slug"],
                   row["old_cite"], row["old_text"])
            pending.setdefault(key, []).append((row, ft, fc))
        for n, ln in enumerate(lines):
            if not ln.strip():
                continue
            r = json.loads(ln)
            key = (r.get("source_slug"), r.get("edge_type"), r.get("target_slug"),
                   r.get("evidence_ref"), r.get("evidence_quote"))
            jobs = pending.get(key)
            if jobs:
                row, ft, fc = jobs.pop(0)
                if not jobs:
                    del pending[key]
                r["evidence_quote"], r["evidence_ref"] = ft, fc
                lines[n] = json.dumps(r, ensure_ascii=False)
                applied_edge += 1
        for key, jobs in pending.items():
            for row, ft, fc in jobs:
                parked.append(f"[?] edge {key[0]}--{key[1]}-->{key[2]} — edge row not found in edges.jsonl")
        if not args.dry_run and applied_edge:
            stamp = dt.date.today().isoformat()
            backup = REPO / "graph" / "edges" / "_regrounding" / f"edges-pre-quote-regrounding-{stamp}.jsonl"
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_text(EDGES.read_text(encoding="utf-8"), encoding="utf-8")
            EDGES.write_text("\n".join(lines) + "\n", encoding="utf-8")

    PARK_REPORT.write_text(
        "# S195 quote re-grounding — parked rows\n\n"
        f"> {'DRY RUN — nothing written. ' if args.dry_run else ''}"
        f"applied: {applied_node} node quotes, {applied_edge} edge rows; "
        f"{len(parked)} parked (listed below, per the no-silent-drop gate).\n\n"
        + "\n".join(f"- {p}" for p in parked) + "\n",
        encoding="utf-8")
    print(f"{'DRY RUN: ' if args.dry_run else ''}applied {applied_node} node quotes, "
          f"{applied_edge} edge rows; parked {len(parked)} "
          f"(see {PARK_REPORT.relative_to(REPO)})")


if __name__ == "__main__":
    main()
