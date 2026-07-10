#!/usr/bin/env python3
"""build-headmap-proposals.py — S208 step: auto-propose name→slug for the
unresolved-status head (names appearing >=2x) + small classes.

For each name: fresh resolve() (the graph has grown since the apply), slugify-exact
check, row candidates, disambiguator samples. Emits headmap-proposals.tsv with a
PROPOSAL column (AUTO where slugify(name) is itself an existing node slug or the fresh
resolver's sole/top exact candidate; else REVIEW). Curator edits the tsv / writes
curation-decisions.json.
"""
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "graph" / "query"))
from weirwood_query.resolve import resolve  # noqa: E402

rows_by_unit = json.loads((HERE / "quarantined-rows.json").read_text(encoding="utf-8"))

# existing slug set
existing = set()
for p in (REPO / "graph" / "nodes").glob("**/*.node.md"):
    existing.add(p.name[: -len(".node.md")])


def slugify(name: str) -> str:
    s = name.lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# gather per-name info for unresolved-status names
per_name = defaultdict(lambda: {"units": [], "reasons": set(), "disamb": [],
                                "cands": Counter(), "rel": 0, "ev": 0, "role": 0})
for unit, names in rows_by_unit.items():
    for name, entry in names.items():
        reasons = set(entry["reasons"])
        if not any(r.startswith("unresolved-status") for r in reasons):
            continue
        s = per_name[name]
        s["units"].append(unit)
        s["reasons"] |= reasons
        s["rel"] += len(entry["rel_rows"])
        s["ev"] += len(entry["event_rows"])
        s["role"] += len(entry["role_refs"])

# pull candidates + disambiguators from the original review rows
for f in sorted((REPO / "working" / "fire-and-blood" / "apply").glob("*/reconcile-review.jsonl")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        name = r.get("name")
        if name in per_name and (r.get("reason") or "").startswith("unresolved-status"):
            if r.get("disambiguator"):
                per_name[name]["disamb"].append(r["disambiguator"])
            for c in r.get("candidates") or []:
                if isinstance(c, dict) and c.get("slug"):
                    per_name[name]["cands"][c["slug"]] += 1

head = {n: s for n, s in per_name.items() if len(s["units"]) >= 2}
tail = {n: s for n, s in per_name.items() if len(s["units"]) < 2}

lines = ["name\tn_units\trows(rel/ev/role)\tPROPOSAL\tbasis\tfresh_resolve\ttop_row_cands\tdisambiguator_sample"]
auto = 0
for name, s in sorted(head.items(), key=lambda kv: -len(kv[1]["units"])):
    slug_guess = slugify(name)
    fslug, fstatus, fcands = resolve(name)
    fcand_slugs = [c.get("slug") if isinstance(c, dict) else c for c in (fcands or [])][:4]
    proposal, basis = "REVIEW", ""
    if slug_guess in existing:
        proposal, basis = slug_guess, "slugify-exact"
    elif fslug and fslug in existing:
        proposal, basis = fslug, f"fresh-resolve[{fstatus}]"
    elif fcand_slugs and fcand_slugs[0] in existing and slugify(fcand_slugs[0]) == slug_guess:
        proposal, basis = fcand_slugs[0], "first-cand-slug-match"
    if proposal != "REVIEW":
        auto += 1
    top_cands = ";".join(f"{sl}x{c}" for sl, c in s["cands"].most_common(3))
    dis = (s["disamb"][0] if s["disamb"] else "")[:90]
    lines.append(f"{name}\t{len(s['units'])}\t{s['rel']}/{s['ev']}/{s['role']}"
                 f"\t{proposal}\t{basis}\t{fslug}[{fstatus}]\t{top_cands}\t{dis}")

(HERE / "headmap-proposals.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")

# tail drop log
tail_rows = sum(s["rel"] + s["ev"] + s["role"] for s in tail.values())
(HERE / "tail-drop-log.json").write_text(json.dumps({
    "dropped_names": len(tail),
    "dropped_proposal_rows": tail_rows,
    "names": sorted(tail)}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"head names: {len(head)} ({auto} AUTO / {len(head)-auto} REVIEW) -> headmap-proposals.tsv")
print(f"tail names: {len(tail)} carrying {tail_rows} proposal rows -> tail-drop-log.json (DROP)")
