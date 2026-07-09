#!/usr/bin/env python3
"""fab-semantic-gate.py — deterministic per-batch semantic gate for the Fire & Blood
apply pipeline.

Runs AFTER each F&B apply batch's `weirwood refresh`. The routing tests (`weirwood
test`, `test-fab-reconcile.py`, etc.) prove the *machinery* ran without crashing;
this script proves the *graph* it produced is still semantically clean — the
advisory-board bar of "green means clean, not just tests-ran".

No LLM, no network, read-only on `graph/`. Four checks:

  1. VICTIM_IN harm-gate      — a VICTIM_IN edge onto a non-harm event subtype is a
                                 semantic error (you cannot be "the victim" of a
                                 birth or a coronation). Reuses the reconciler's own
                                 `HARM_EVENT_SUBTYPES` / `classify_patient_edge_type`
                                 (imported read-only from fab-reconcile-candidates.py
                                 — never a second copy of the harm list). Gated FAIL
                                 scope: `is_fab_provenance_edge()` — strictly
                                 `evidence_kind == "book-fab"` (or a `run_id` starting
                                 "fab-", belt-and-suspenders; the two never diverge on
                                 the live graph). Pre-existing `book-pass1` /
                                 `book-pass1-reified` / wiki-sourced VICTIM_IN edges
                                 (e.g. the AGOT narrative-arc reification pass's
                                 `bran-stark VICTIM_IN six-wildling-deserters-ambush-
                                 bran`, run_id None) are NEVER in the FAIL scope, no
                                 matter their target subtype — always informational
                                 (the pre-existing baseline this gate doesn't own).
  2. Junk character.human      — reuses the reconciler's `junk_character_screen`
     nodes                      (imported read-only). See "Design note: check 2
                                 scoping" below for why the FAIL scope is narrower
                                 than a literal whole-corpus read of the spec.
  3. Orphan edges               — every edge's source_slug/target_slug must resolve
                                 to a live node, directly or via
                                 working/wiki/data/alias-resolver.json. Informational
                                 by default; FAIL only if --baseline-orphans N is
                                 given and the live count exceeds N (some orphans
                                 pre-date F&B and are not this gate's job to fix).
  4. Duplicate edges            — groups edges by the mint guard's own dedup key
                                 (edge_type, source_slug, target_slug,
                                 normalized_quote), imported read-only from
                                 mint_enrichment.py (`edge_dedup_key`). Any group of
                                 2+ is reported informational (should be ~0 given the
                                 mint dedup guard); FAIL only if a group contains an
                                 `is_fab_provenance_edge()` member (a guard miss on
                                 an F&B edge) — pre-existing book-pass1 dup groups
                                 stay informational.

Design note: check 2 scoping.
  The spec text for check 2 reads "For every node with type: character.human ...
  FAIL if any live character.human node would be rejected by the screen" with no
  explicit F&B scope (unlike checks 1/3/4, which are explicitly F&B-scoped).
  Applying `junk_character_screen` to the RAW `name:` frontmatter field of every one
  of the ~3,878 existing character.human nodes produces ~116 hits — almost entirely
  the graph's own long-standing "Firstname Lastname (son of X)" / "(daughter of X)"
  disambiguator-suffix convention (e.g. "Aerion Targaryen (son of Daemion)") and
  canonical in-world epithet names ("The Liddle", "Ben Bones"). The screen is
  calibrated (see fab-reconcile-candidates.py's own call site, ~line 1504) against a
  BARE roster name with any disambiguator tracked in a SEPARATE column — never a
  full disambiguated node display name. Feeding it the full display name is not
  "the screen catching junk that slipped through"; it's a mismatched calling
  convention that would make this gate FAIL on ~3% of the pre-existing corpus on
  every single run, forever, regardless of what any given F&B batch did — the
  opposite of a usable green light.
  This script therefore (a) strips a trailing " (...)" disambiguator clause before
  calling the screen — the same bare-name convention the reconciler itself uses —
  and (b) gates the FAIL on F&B-PROVENANCE nodes only (a node is F&B-provenance if
  its body carries a `<!-- fab-enriched: ... -->` merge marker, OR its
  `pass_origin` frontmatter contains "fab" — i.e. it was CREATEd or UPDATEd by the
  F&B pipeline). Both the raw-name and stripped-name whole-corpus hit counts are
  still reported, informational, in every run — nothing is hidden, the design
  decision is fully auditable from the output.

USAGE
  python3 scripts/fab-semantic-gate.py
  python3 scripts/fab-semantic-gate.py --baseline-orphans 67
  python3 scripts/fab-semantic-gate.py --json

Exit code: 0 if every check is PASS; 1 if any check is FAIL.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NODES_ROOT = REPO / "graph" / "nodes"
EDGES_FILE = REPO / "graph" / "edges" / "edges.jsonl"
ALIAS_RESOLVER_FILE = REPO / "working" / "wiki" / "data" / "alias-resolver.json"
SKIP_DIRS = {"_conflicts", "_unclassified"}

FAB_EVIDENCE_KIND = "book-fab"
EXAMPLE_CAP = 10  # up to ~10 example offenders per check in human-readable output


# ---------------------------------------------------------------------------
# Read-only imports of the canonical definitions this gate audits AGAINST.
# Hyphenated filenames -> importlib.util (same pattern as test-fab-reconcile.py).
# Neither module executes anything at import time beyond def/class statements
# (both are guarded by `if __name__ == "__main__":`).
# ---------------------------------------------------------------------------
def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_reconciler():
    return _load_module("fab_semantic_gate_reconciler_import", "scripts/fab-reconcile-candidates.py")


def load_mint():
    return _load_module("fab_semantic_gate_mint_import", "scripts/mint_enrichment.py")


# ---------------------------------------------------------------------------
# Node index — one scan of graph/nodes/**/*.node.md (excluding _conflicts/
# _unclassified, matching the convention in scripts/orphan-edges-audit.py).
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FRONTMATTER_LINE_RE = re.compile(r"^([a-zA-Z_]+):\s*(.*)$")


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        km = FRONTMATTER_LINE_RE.match(line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return fm


def is_fab_provenance_edge(e: dict) -> bool:
    """Strict F&B-provenance test for EDGE checks (1 and 4): `evidence_kind ==
    "book-fab"` is authoritative; a `run_id` starting with "fab-" is accepted as a
    belt-and-suspenders fallback (on the live graph the two conditions are
    perfectly co-occurring — every book-fab edge carries a fab-*-run_id and vice
    versa — so this never changes the result, it only guards against a future edge
    that sets one field but not the other).

    Deliberately narrow: pre-existing AGOT-era `book-pass1` / `book-pass1-reified`
    edges (e.g. the narrative-arc reification pass's `bran-stark VICTIM_IN
    six-wildling-deserters-ambush-bran`, run_id None) are NEVER F&B-provenance under
    this test, no matter what their target event's subtype is — they are always
    routed to the informational bucket in checks 1 and 4, never the hard FAIL."""
    if e.get("evidence_kind") == FAB_EVIDENCE_KIND:
        return True
    run_id = e.get("run_id") or ""
    return run_id.startswith("fab-")


def is_fab_provenance(text: str, pass_origin: str | None) -> bool:
    """A node was CREATEd or UPDATEd by the F&B pipeline: its body carries a
    `<!-- fab-enriched: ... -->` merge marker (fab_merge_node.py), OR its
    pass_origin names the F&B enrichment pass (`pass-fab-enrichment`, the CREATE
    stamp). Either is sufficient; neither is required for a node to be legitimate —
    this only marks nodes this gate should hold F&B accountable for."""
    if "fab-enriched" in text:
        return True
    return bool(pass_origin) and "fab" in pass_origin.lower()


def build_node_index(nodes_root: Path = NODES_ROOT) -> dict[str, dict]:
    """slug -> {type, name, dir, path, fab_provenance}."""
    index: dict[str, dict] = {}
    if not nodes_root.exists():
        return index
    for type_dir in sorted(nodes_root.iterdir()):
        if not type_dir.is_dir() or type_dir.name in SKIP_DIRS:
            continue
        for p in sorted(type_dir.glob("*.node.md")):
            slug = p.name[: -len(".node.md")]
            text = p.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            index[slug] = {
                "type": fm.get("type"),
                "name": fm.get("name", slug),
                "dir": type_dir.name,
                "path": p,
                "fab_provenance": is_fab_provenance(text, fm.get("pass_origin")),
            }
    return index


def load_alias_index(path: Path = ALIAS_RESOLVER_FILE) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("alias_to_canonical", {})


def load_edges(path: Path = EDGES_FILE) -> list[dict]:
    edges = []
    if not path.exists():
        return edges
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            print(f"WARNING: skipping malformed edges.jsonl line {i}: {line[:80]!r}", file=sys.stderr)
            continue
        row["_line"] = i
        edges.append(row)
    return edges


# ---------------------------------------------------------------------------
# Check 1 — VICTIM_IN harm-gate
# ---------------------------------------------------------------------------
def check_victim_in_harm_gate(edges: list[dict], node_index: dict[str, dict],
                              classify_patient_edge_type) -> dict:
    fab_offenders = []
    nonfab_offenders = []
    non_event_targets = []  # additional finding, out of strict spec scope — see report
    checked = 0
    for e in edges:
        if e.get("edge_type") != "VICTIM_IN":
            continue
        target_slug = e.get("target_slug")
        node = node_index.get(target_slug)
        if node is None:
            continue  # orphan target — check 3's job, not this check's
        node_type = node.get("type") or ""
        if not node_type.startswith("event."):
            non_event_targets.append({
                "source": e.get("source_slug"), "target": target_slug,
                "target_type": node_type or "(untyped)",
                "evidence_kind": e.get("evidence_kind"), "line": e.get("_line"),
            })
            continue
        checked += 1
        subtype = node_type.split(".", 1)[1]
        expected = classify_patient_edge_type(subtype)
        if expected == "VICTIM_IN":
            continue  # correctly typed, harm event
        offender = {
            "source": e.get("source_slug"), "target": target_slug,
            "target_subtype": subtype, "expected_edge_type": expected,
            "evidence_kind": e.get("evidence_kind"), "run_id": e.get("run_id"),
            "evidence_quote": e.get("evidence_quote"), "line": e.get("_line"),
        }
        if is_fab_provenance_edge(e):
            fab_offenders.append(offender)
        else:
            nonfab_offenders.append(offender)

    status = "FAIL" if fab_offenders else "PASS"
    return {
        "name": "victim_in_harm_gate",
        "status": status,
        "checked_event_targeted": checked,
        "fail_count": len(fab_offenders),
        "informational_nonfab_count": len(nonfab_offenders),
        "offenders": fab_offenders,
        "informational_offenders": nonfab_offenders,
        "non_event_target_count": len(non_event_targets),
        "non_event_targets": non_event_targets,
        "summary": (
            f"{len(fab_offenders)} F&B-provenance VICTIM_IN edge(s) point at a non-harm "
            f"event subtype (checked {checked} VICTIM_IN->event edges total; "
            f"{len(nonfab_offenders)} additional non-F&B offenders in the pre-existing "
            f"baseline, informational only). {len(non_event_targets)} VICTIM_IN edge(s) "
            f"target a node that isn't an event at all (out of this check's strict scope, "
            f"reported informationally)."
        ),
    }


# ---------------------------------------------------------------------------
# Check 2 — junk character.human nodes
# ---------------------------------------------------------------------------
TRAILING_PAREN_RE = re.compile(r"\s*\([^()]*\)\s*$")


def strip_trailing_disambiguator(name: str) -> str:
    """Strip trailing ' (...)' clause(s) — e.g. 'Aerion Targaryen (son of Daemion)'
    -> 'Aerion Targaryen'. Mirrors the reconciler's own name/disambiguator split (the
    CREATE-guard call site screens the bare roster name; the disambiguator is tracked
    in a separate table column, never appended to the name it screens). See module
    docstring "Design note: check 2 scoping"."""
    prev = None
    s = name.strip()
    while prev != s:
        prev = s
        s = TRAILING_PAREN_RE.sub("", s).strip()
    return s or name.strip()


def check_junk_characters(node_index: dict[str, dict], junk_character_screen) -> dict:
    fab_offenders = []
    informational_stripped = []  # non-fab nodes the (stripped-name) screen still flags
    raw_hit_count = 0            # whole-corpus raw-name hit count, informational tally only

    for slug, node in node_index.items():
        if node.get("type") != "character.human":
            continue
        name = node.get("name") or slug
        if junk_character_screen(name):
            raw_hit_count += 1
        stripped = strip_trailing_disambiguator(name)
        reason = junk_character_screen(stripped)
        if not reason:
            continue
        row = {
            "slug": slug, "name": name, "screened_name": stripped, "reason": reason,
            "fab_provenance": node.get("fab_provenance", False),
        }
        if node.get("fab_provenance"):
            fab_offenders.append(row)
        else:
            informational_stripped.append(row)

    status = "FAIL" if fab_offenders else "PASS"
    return {
        "name": "junk_character_nodes",
        "status": status,
        "fail_count": len(fab_offenders),
        "offenders": fab_offenders,
        "informational_stripped_count": len(informational_stripped),
        "informational_stripped_offenders": informational_stripped,
        "informational_raw_hit_count": raw_hit_count,
        "summary": (
            f"{len(fab_offenders)} F&B-provenance character.human node(s) would be "
            f"rejected by junk_character_screen after disambiguator-stripping. "
            f"Informational: {len(informational_stripped)} pre-existing (non-F&B) node(s) "
            f"also flag under the same stripped screen (long-standing epithet-named "
            f"characters this gate doesn't own); {raw_hit_count} node(s) flag under the "
            f"RAW (un-stripped) name across the whole corpus — most of that gap is the "
            f"graph's own '(son of X)'/'(daughter of X)' disambiguator-suffix convention, "
            f"a known screen/calling-convention mismatch, not new junk. See module "
            f"docstring."
        ),
    }


# ---------------------------------------------------------------------------
# Check 3 — orphan edges (source_slug / target_slug must resolve, after aliases)
# ---------------------------------------------------------------------------
def resolve_slug(slug: str | None, node_index: dict, alias_index: dict) -> str:
    """'direct' | 'alias' | 'missing'."""
    if not slug:
        return "missing"
    if slug in node_index:
        return "direct"
    canonical = alias_index.get(slug)
    if canonical and canonical in node_index:
        return "alias"
    return "missing"


def check_orphan_edges(edges: list[dict], node_index: dict, alias_index: dict,
                       baseline_orphans: int | None = None) -> dict:
    missing_examples = []
    alias_examples = []
    missing_count = 0
    alias_count = 0
    for e in edges:
        for endpoint in ("source_slug", "target_slug"):
            slug = e.get(endpoint)
            status = resolve_slug(slug, node_index, alias_index)
            if status == "missing":
                missing_count += 1
                if len(missing_examples) < EXAMPLE_CAP:
                    missing_examples.append({
                        "edge_type": e.get("edge_type"), "endpoint": endpoint,
                        "slug": slug, "evidence_kind": e.get("evidence_kind"),
                        "line": e.get("_line"),
                    })
            elif status == "alias":
                alias_count += 1
                if len(alias_examples) < EXAMPLE_CAP:
                    alias_examples.append({
                        "edge_type": e.get("edge_type"), "endpoint": endpoint,
                        "slug": slug, "resolves_to": alias_index.get(slug),
                        "line": e.get("_line"),
                    })

    if baseline_orphans is None:
        status = "PASS"
        gate_note = "informational only — no --baseline-orphans given"
    else:
        status = "FAIL" if missing_count > baseline_orphans else "PASS"
        gate_note = f"gated against --baseline-orphans {baseline_orphans}"

    return {
        "name": "orphan_edges",
        "status": status,
        "missing_count": missing_count,
        "alias_resolvable_count": alias_count,
        "offenders": missing_examples,
        "informational_alias_offenders": alias_examples,
        "baseline_orphans": baseline_orphans,
        "summary": (
            f"{missing_count} edge-endpoint(s) resolve to no node, even after aliases "
            f"({gate_note}). {alias_count} additional endpoint(s) only resolve via "
            f"alias-resolver (slug-format drift, not a graph gap)."
        ),
    }


# ---------------------------------------------------------------------------
# Check 4 — duplicate edges
# ---------------------------------------------------------------------------
def check_duplicate_edges(edges: list[dict], edge_dedup_key) -> dict:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for e in edges:
        quote = e.get("evidence_quote")
        et, src, tgt = e.get("edge_type"), e.get("source_slug"), e.get("target_slug")
        if not (quote and et and src and tgt):
            continue
        key = edge_dedup_key(et, src, tgt, quote)
        groups[key].append(e)

    dup_groups = {k: v for k, v in groups.items() if len(v) >= 2}
    fab_dup_groups = {k: v for k, v in dup_groups.items()
                      if any(is_fab_provenance_edge(m) for m in v)}

    def _group_row(key, members):
        return {
            "edge_type": key[0], "source": key[1], "target": key[2],
            "normalized_quote": key[3], "count": len(members),
            "members": [{"evidence_kind": m.get("evidence_kind"), "run_id": m.get("run_id"),
                        "line": m.get("_line")} for m in members],
        }

    fab_offenders = [_group_row(k, v) for k, v in fab_dup_groups.items()]
    informational_offenders = [_group_row(k, v) for k, v in dup_groups.items() if k not in fab_dup_groups]

    status = "FAIL" if fab_offenders else "PASS"
    total_redundant = sum(v["count"] - 1 for v in fab_offenders + informational_offenders)
    return {
        "name": "duplicate_edges",
        "status": status,
        "fail_count": len(fab_offenders),
        "offenders": fab_offenders[:EXAMPLE_CAP],
        "informational_count": len(informational_offenders),
        "informational_offenders": informational_offenders[:EXAMPLE_CAP],
        "total_duplicate_groups": len(dup_groups),
        "total_redundant_edges": total_redundant,
        "summary": (
            f"{len(fab_offenders)} F&B-provenance duplicate-edge group(s) found "
            f"(identical edge_type/source/target/normalized-quote) — a mint dedup-guard "
            f"miss. {len(informational_offenders)} additional pre-existing duplicate "
            f"group(s) (informational; predate the S200 mint dedup guard)."
        ),
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def run_checks(edges: list[dict], node_index: dict, alias_index: dict,
               classify_patient_edge_type, junk_character_screen, edge_dedup_key,
               baseline_orphans: int | None = None) -> list[dict]:
    return [
        check_victim_in_harm_gate(edges, node_index, classify_patient_edge_type),
        check_junk_characters(node_index, junk_character_screen),
        check_orphan_edges(edges, node_index, alias_index, baseline_orphans),
        check_duplicate_edges(edges, edge_dedup_key),
    ]


def print_human(results: list[dict]) -> None:
    overall = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    print("=" * 72)
    print(f"fab-semantic-gate — OVERALL: {overall}")
    print("=" * 72)
    for r in results:
        print(f"\n[{r['status']}] {r['name']}")
        print(f"  {r['summary']}")
        offenders = r.get("offenders") or []
        if offenders:
            print(f"  Offenders (up to {EXAMPLE_CAP} of {r.get('fail_count', r.get('missing_count', len(offenders)))}):")
            for o in offenders[:EXAMPLE_CAP]:
                print(f"    - {o}")
        info_keys = [k for k in r if k.startswith("informational_") and k.endswith("offenders")]
        for k in info_keys:
            rows = r.get(k) or []
            if rows:
                label = k.replace("informational_", "").replace("_offenders", "")
                print(f"  Informational ({label}, up to {EXAMPLE_CAP} shown):")
                for o in rows[:EXAMPLE_CAP]:
                    print(f"    - {o}")
        non_event = r.get("non_event_targets") or []
        if non_event:
            print(f"  Informational (VICTIM_IN target not an event node, up to {EXAMPLE_CAP} shown):")
            for o in non_event[:EXAMPLE_CAP]:
                print(f"    - {o}")
    print()


def to_json(results: list[dict]) -> dict:
    overall = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    return {"overall": overall, "checks": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline-orphans", type=int, default=None,
                       help="Gate check 3 (orphan edges): FAIL if the live missing-endpoint "
                            "count exceeds this. Default: informational only.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON verdict instead of the human summary.")
    parser.add_argument("--nodes-root", type=Path, default=NODES_ROOT, help="Override graph/nodes/ root (testing).")
    parser.add_argument("--edges-file", type=Path, default=EDGES_FILE, help="Override edges.jsonl path (testing).")
    parser.add_argument("--alias-resolver", type=Path, default=ALIAS_RESOLVER_FILE, help="Override alias-resolver.json path (testing).")
    args = parser.parse_args()

    reconciler = load_reconciler()
    mint = load_mint()

    node_index = build_node_index(args.nodes_root)
    alias_index = load_alias_index(args.alias_resolver)
    edges = load_edges(args.edges_file)

    results = run_checks(
        edges, node_index, alias_index,
        reconciler.classify_patient_edge_type,
        reconciler.junk_character_screen,
        mint.edge_dedup_key,
        baseline_orphans=args.baseline_orphans,
    )

    if args.json:
        print(json.dumps(to_json(results), indent=2, default=str))
    else:
        print_human(results)

    return 0 if all(r["status"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
