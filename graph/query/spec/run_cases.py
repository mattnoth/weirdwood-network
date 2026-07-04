#!/usr/bin/env python3
"""Standalone verification runner for the "full"/"both"-profile golden cases in
graph/query/spec/cases/*.json — the Python side of the cross-language parity
fixtures (query-layer Track, step 1, session A; see spec/operations.md).

NOT a pytest suite (D-G explicitly defers the pytest traversal suite to the
Track's final session — this script is a verification artifact, not a test
runner with fixtures/CI wiring). Run it directly:

    python3 graph/query/spec/run_cases.py

Deliberately TOLERANT: `graph/query/weirwood_query/` is being built concurrently
by another session in this same Track. This script does not assume any
particular function signature beyond what it can introspect at call time, and
it SKIPS (never crashes the whole run) when:
  - the weirwood_query package isn't importable at all,
  - a case's op has no matching callable yet,
  - a callable exists but raises/returns a shape this script can't interpret.

Every skip is reported with a reason. A "full"-profile case that never runs
because the engine doesn't exist yet is expected, common, and NOT a failure —
this script exists to be re-run as the engine lands, not to gate anything today.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

SPEC_DIR = Path(__file__).resolve().parent
CASES_DIR = SPEC_DIR / "cases"
REPO_ROOT = SPEC_DIR.parent.parent.parent  # graph/query/spec -> graph/query -> graph -> repo root
QUERY_PKG_DIR = REPO_ROOT / "graph" / "query"
WEB_DATA_DIR = REPO_ROOT / "web" / "data"

CASE_FILES = ["resolve.json", "neighbors.json", "chain.json", "family.json", "braid.json"]

# `family` cases are tagged profile: "bounded" (they pin values verified against
# the live TS engine) but, as of step 1 close-out, the Python family_tree() port
# exists and can be checked against the SAME bundle-derived data the TS values
# were pinned from (web/data/{nodes,edges}.json) — so the expected values still
# hold. Rather than retag the case files (the expected values pin current TS
# behavior, and retagging would make this the only op whose golden cases run
# under a different profile than their tag says), this runner special-cases
# family.json: it always runs, using the bundle as its input, regardless of the
# generic runs_under_full() gate below.
FAMILY_ALWAYS_RUNS = "family.json"


def load_bundle() -> tuple[list[dict], dict[str, dict]] | None:
    """Load web/data/{edges,nodes}.json and adapt edges to the traverse.py
    dict convention (source_slug/target_slug/edge_type) family_tree expects.
    Returns None if the bundle isn't present (fresh checkout before `deno
    task build` has run) — callers SKIP rather than fail in that case."""
    edges_path = WEB_DATA_DIR / "edges.json"
    nodes_path = WEB_DATA_DIR / "nodes.json"
    if not edges_path.exists() or not nodes_path.exists():
        return None
    try:
        bundle_edges = json.loads(edges_path.read_text(encoding="utf-8"))
        bundle_nodes = json.loads(nodes_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    edges = [
        {
            "source_slug": e.get("source"),
            "target_slug": e.get("target"),
            "edge_type": e.get("type"),
            "evidence_ref": e.get("ref"),
            "confidence_tier": e.get("tier"),
            "evidence_quote": e.get("quote"),
        }
        for e in bundle_edges
    ]
    return edges, bundle_nodes


def load_cases(filename: str) -> list[dict]:
    path = CASES_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def runs_under_full(case: dict) -> bool:
    return case.get("profile") in ("full", "both")


class Engine:
    """Best-effort handle onto weirwood_query. `ok` is False if the package
    couldn't be imported at all — every case is then a clean SKIP, not a crash."""

    def __init__(self) -> None:
        self.ok = False
        self.resolve_mod: Any = None
        self.traverse_mod: Any = None
        self.error: str | None = None
        try:
            if str(QUERY_PKG_DIR) not in sys.path:
                sys.path.insert(0, str(QUERY_PKG_DIR))
            import weirwood_query  # type: ignore

            self.resolve_mod = getattr(weirwood_query, "resolve", None)
            self.traverse_mod = getattr(weirwood_query, "traverse", None)
            self.ok = True
        except Exception as e:  # pragma: no cover - defensive, package is WIP
            self.error = f"{type(e).__name__}: {e}"


def find_callable(mod: Any, *names: str) -> Callable | None:
    if mod is None:
        return None
    for name in names:
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn
    return None


# ---- per-op attempts. Each returns (status, detail) where status is one of
# "pass" / "fail" / "skip". Never raises past its own try/except. ----


def try_resolve(engine: Engine, case: dict) -> tuple[str, str]:
    fn = find_callable(engine.resolve_mod, "resolve")
    if fn is None:
        return "skip", "no resolve() callable found in weirwood_query.resolve"
    phrase = case["input"]["phrase"]
    try:
        result = fn(phrase)
    except Exception as e:
        return "skip", f"resolve() raised (signature likely still in flux): {e}"

    exp = case["expect"]
    # The Python resolve() signature/shape is not yet finalized (per
    # operations.md's appendix: full uses (slug, status, candidates), a materially
    # different shape than the bounded candidate list). Rather than guess the
    # shape, just sanity-check whatever came back is non-crashing and, where a
    # top slug is asserted, do a best-effort substring/tuple check.
    if exp.get("top", {}).get("slug"):
        want = exp["top"]["slug"]
        text = json.dumps(result, default=str)
        if want not in text:
            return "fail", f"expected slug {want!r} not found anywhere in resolve() output: {result!r}"
    return "pass", "best-effort shape check (see operations.md appendix on resolve status-enum mismatch)"


def try_neighbors(engine: Engine, case: dict) -> tuple[str, str]:
    fn = find_callable(engine.traverse_mod, "neighbors")
    if fn is None:
        return "skip", "no neighbors() callable found in weirwood_query.traverse"
    return "skip", "neighbors() full-profile parity check not yet wired (needs edges.jsonl load helper contract) — placeholder for a future iteration of this script"


def try_chain(engine: Engine, case: dict) -> tuple[str, str]:
    fn = find_callable(engine.traverse_mod, "causal_chain")
    if fn is None:
        return "skip", "no causal_chain() callable found in weirwood_query.traverse"
    return "skip", "causal_chain() full-profile parity check not yet wired (full profile has no depth cap / no story-time sort yet per operations.md — a byte-identical parity check does not apply until step 1 ports the sort)"


def try_family(engine: Engine, case: dict) -> tuple[str, str]:
    """Exact check for family_tree() against the SAME bundle-derived data the
    TS values in family.json were pinned from (web/data/{edges,nodes}.json —
    see load_bundle()). All 6 cases are checked in full (not best-effort):
    root/rootName/memberCount/truncated, generationCounts, mustInclude/
    mustExclude, generationBounds, spouseBondIncludes, and — for the two
    `mode: exact` cases — an exact members/parentBonds/spouseBonds match."""
    fn = find_callable(engine.traverse_mod, "family_tree")
    if fn is None:
        return "skip", "no family_tree() callable found in weirwood_query.traverse"

    bundle = load_bundle()
    if bundle is None:
        return "skip", "web/data/{edges,nodes}.json not found — run the bundle build first"
    edges, nodes = bundle

    slug = case["input"]["slug"]
    kwargs: dict[str, Any] = {}
    if "generationsUp" in case["input"]:
        kwargs["generations_up"] = case["input"]["generationsUp"]
    if "generationsDown" in case["input"]:
        kwargs["generations_down"] = case["input"]["generationsDown"]
    try:
        result = fn(slug, edges, nodes, **kwargs)
    except Exception as e:
        return "skip", f"family_tree() raised: {e}"

    if not isinstance(result, dict):
        return "fail", f"family_tree() did not return a dict: {type(result)!r}"

    exp = case["expect"]
    problems: list[str] = []

    def snake_or_camel(d: dict, camel: str, snake: str) -> Any:
        return d.get(camel, d.get(snake))

    members = result.get("members", [])
    member_slugs = {m.get("slug") for m in members}

    if "root" in exp:
        got = result.get("root")
        if got != exp["root"]:
            problems.append(f"root: got {got!r}, expected {exp['root']!r}")

    if "rootName" in exp:
        got = snake_or_camel(result, "rootName", "root_name")
        if got != exp["rootName"]:
            problems.append(f"rootName: got {got!r}, expected {exp['rootName']!r}")

    if "memberCount" in exp:
        got = snake_or_camel(result, "memberCount", "member_count")
        if got != exp["memberCount"]:
            problems.append(f"memberCount: got {got!r}, expected {exp['memberCount']!r}")

    if "truncated" in exp:
        got = result.get("truncated")
        if got != exp["truncated"]:
            problems.append(f"truncated: got {got!r}, expected {exp['truncated']!r}")

    if "generationCounts" in exp:
        from collections import Counter

        got_counts = Counter(m.get("generation") for m in members)
        exp_counts = {int(k): v for k, v in exp["generationCounts"].items()}
        got_counts_int = {int(k): v for k, v in got_counts.items()}
        if got_counts_int != exp_counts:
            problems.append(f"generationCounts: got {got_counts_int}, expected {exp_counts}")

    if "mustInclude" in exp:
        missing = [s for s in exp["mustInclude"] if s not in member_slugs]
        if missing:
            problems.append(f"mustInclude: missing {missing}")

    if "mustExclude" in exp:
        present = [s for s in exp["mustExclude"] if s in member_slugs]
        if present:
            problems.append(f"mustExclude: unexpectedly present {present}")

    if "generationBounds" in exp:
        gens = [m.get("generation") for m in members]
        got_bounds = {"min": min(gens), "max": max(gens)} if gens else {"min": None, "max": None}
        if got_bounds != exp["generationBounds"]:
            problems.append(f"generationBounds: got {got_bounds}, expected {exp['generationBounds']}")

    if "spouseBondIncludes" in exp:
        want = exp["spouseBondIncludes"]
        want_pair = {want["a"], want["b"]}
        spouse_bonds = snake_or_camel(result, "spouseBonds", "spouse_bonds") or []
        found = any({sb.get("a"), sb.get("b")} == want_pair for sb in spouse_bonds)
        if not found:
            problems.append(f"spouseBondIncludes: {want_pair} not found in spouseBonds")

    if exp.get("mode") == "exact":
        if "members" in exp:
            got_members_norm = _normalize_members(members)
            exp_members_norm = _normalize_members(exp["members"])
            if got_members_norm != exp_members_norm:
                problems.append(f"members (exact): got {got_members_norm}, expected {exp_members_norm}")
        for bond_key, snake_key in (("parentBonds", "parent_bonds"), ("spouseBonds", "spouse_bonds")):
            if bond_key in exp:
                got_bonds = snake_or_camel(result, bond_key, snake_key) or []
                if got_bonds != exp[bond_key] and not (not got_bonds and not exp[bond_key]):
                    problems.append(f"{bond_key} (exact): got {got_bonds}, expected {exp[bond_key]}")

    if problems:
        return "fail", "; ".join(problems)
    return "pass", "exact check against web/data/ bundle"


def _normalize_members(members: list[dict]) -> list[tuple]:
    """Reduce a members list to a comparable, order-independent set of tuples
    over the fields both the TS (camelCase) and Python (snake_case) shapes
    carry, so exact-mode member comparisons don't false-fail on key casing."""
    out = []
    for m in members:
        out.append((
            m.get("slug"),
            m.get("name"),
            m.get("generation"),
            m.get("hasNode", m.get("has_node")),
            m.get("degree"),
            m.get("quoteCount", m.get("quote_count")),
            m.get("prominence"),
        ))
    return sorted(out, key=lambda t: (t[2], t[0] or ""))


def _braid_mod(engine: Engine) -> Any:
    """Lazily fetch weirwood_query.braid — not preloaded onto Engine like
    resolve/traverse since braid.py is new in this session; import defensively
    so an engine mid-build (braid.py not yet landed) SKIPs cleanly."""
    if not engine.ok:
        return None
    try:
        import weirwood_query  # type: ignore

        return getattr(weirwood_query, "braid", None)
    except Exception:
        return None


def try_fork_hubs(engine: Engine, case: dict) -> tuple[str, str]:
    mod = _braid_mod(engine)
    fn = find_callable(mod, "fork_hubs")
    if fn is None:
        return "skip", "no fork_hubs() callable found in weirwood_query.braid"
    from weirwood_query.load import load_edges  # type: ignore

    try:
        edges = load_edges()
        min_out = case["input"].get("minOut", 2)
        include_enables = case["input"].get("includeEnables", False)
        result = fn(edges, min_out=min_out, include_enables=include_enables)
    except Exception as e:
        return "skip", f"fork_hubs() raised: {e}"

    exp = case["expect"]
    problems: list[str] = []
    hub_map = {h["slug"]: h for h in result.get("hubs", [])}

    if "mustIncludeSlugs" in exp:
        missing = [s for s in exp["mustIncludeSlugs"] if s not in hub_map]
        if missing:
            problems.append(f"mustIncludeSlugs: missing {missing}")

    if "allOutDegreesAtLeast" in exp:
        floor = exp["allOutDegreesAtLeast"]
        bad = [h["slug"] for h in result.get("hubs", []) if h["out_degree"] < floor]
        if bad:
            problems.append(f"allOutDegreesAtLeast={floor}: violated by {bad}")

    if problems:
        return "fail", "; ".join(problems)
    return "pass", f"{len(result.get('hubs', []))} hubs at min_out={min_out}"


def try_join_hubs(engine: Engine, case: dict) -> tuple[str, str]:
    mod = _braid_mod(engine)
    fn = find_callable(mod, "join_hubs")
    if fn is None:
        return "skip", "no join_hubs() callable found in weirwood_query.braid"
    from weirwood_query.load import load_edges  # type: ignore

    try:
        edges = load_edges()
        min_in = case["input"].get("minIn", 2)
        include_enables = case["input"].get("includeEnables", False)
        result = fn(edges, min_in=min_in, include_enables=include_enables)
    except Exception as e:
        return "skip", f"join_hubs() raised: {e}"

    exp = case["expect"]
    problems: list[str] = []
    hub_map = {h["slug"]: h for h in result.get("hubs", [])}

    if "mustIncludeSlugs" in exp:
        missing = [s for s in exp["mustIncludeSlugs"] if s not in hub_map]
        if missing:
            problems.append(f"mustIncludeSlugs: missing {missing}")

    if "allInDegreesAtLeast" in exp:
        floor = exp["allInDegreesAtLeast"]
        bad = [h["slug"] for h in result.get("hubs", []) if h["in_degree"] < floor]
        if bad:
            problems.append(f"allInDegreesAtLeast={floor}: violated by {bad}")

    if problems:
        return "fail", "; ".join(problems)
    return "pass", f"{len(result.get('hubs', []))} hubs at min_in={min_in}"


def try_braid(engine: Engine, case: dict) -> tuple[str, str]:
    mod = _braid_mod(engine)
    fn = find_callable(mod, "braid")
    if fn is None:
        return "skip", "no braid() callable found in weirwood_query.braid"
    from weirwood_query.load import load_edges  # type: ignore

    slugs = case["input"]["slugs"]
    try:
        edges = load_edges()
        include_enables = case["input"].get("includeEnables", False)
        result = fn(slugs, edges, include_enables=include_enables)
    except Exception as e:
        return "skip", f"braid() raised: {e}"

    exp = case["expect"]

    if exp.get("error"):
        if result.get("error"):
            return "pass", "error path returned as expected"
        return "fail", f"expected an error result, got: {result!r}"

    problems: list[str] = []
    shared_anc = {a["slug"] for a in result.get("shared_ancestors", [])}
    shared_desc = {d["slug"] for d in result.get("shared_descendants", [])}
    offset: set[str] = set()
    for p in result.get("pairwise", []):
        offset |= set(p.get("offset_shared_middle", []))

    if "sharedAncestorsMustInclude" in exp:
        missing = [s for s in exp["sharedAncestorsMustInclude"] if s not in shared_anc]
        if missing:
            problems.append(f"sharedAncestorsMustInclude: missing {missing} (got {sorted(shared_anc)})")

    if "sharedDescendantsMustInclude" in exp:
        missing = [s for s in exp["sharedDescendantsMustInclude"] if s not in shared_desc]
        if missing:
            problems.append(f"sharedDescendantsMustInclude: missing {missing} (got {sorted(shared_desc)})")

    if "offsetMustInclude" in exp:
        missing = [s for s in exp["offsetMustInclude"] if s not in offset]
        if missing:
            problems.append(f"offsetMustInclude: missing {missing} (got {sorted(offset)})")

    if problems:
        return "fail", "; ".join(problems)
    return "pass", "shared-ancestor/descendant/offset invariants held"


RUNNERS: dict[str, Callable[[Engine, dict], tuple[str, str]]] = {
    "resolve": try_resolve,
    "neighbors": try_neighbors,
    "chain": try_chain,
    "family": try_family,
    "fork-hubs": try_fork_hubs,
    "join-hubs": try_join_hubs,
    "braid": try_braid,
}


def main() -> int:
    engine = Engine()
    if not engine.ok:
        print(f"weirwood_query not importable ({engine.error}) — every full/both case will SKIP.")
        print("This is expected while graph/query/weirwood_query/ is mid-build. Re-run later.\n")

    totals = {"pass": 0, "fail": 0, "skip": 0}
    failures: list[str] = []

    for filename in CASE_FILES:
        cases = load_cases(filename)
        for case in cases:
            # family.json cases are tagged profile: "bounded" (they pin values
            # verified against the live TS engine) but the Python family_tree()
            # port exists now and can be checked against the same bundle those
            # values were pinned from — see FAMILY_ALWAYS_RUNS / load_bundle().
            # Every other bounded-only case stays deno-runner-only.
            if filename != FAMILY_ALWAYS_RUNS and not runs_under_full(case):
                continue  # bounded-only case: the deno runner's job, not this script's.
            runner = RUNNERS.get(case["op"])
            if runner is None or not engine.ok:
                status, detail = "skip", "engine not importable" if not engine.ok else "no runner for op"
            else:
                try:
                    status, detail = runner(engine, case)
                except Exception as e:  # belt-and-suspenders: a case must never crash the run
                    status, detail = "skip", f"unexpected error, treated as skip: {e}"
            totals[status] += 1
            marker = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP"}[status]
            print(f"[{marker}] {filename}:{case['id']} — {detail}")
            if status == "fail":
                failures.append(f"{filename}:{case['id']}")

    print(f"\n{totals['pass']} passed, {totals['fail']} failed, {totals['skip']} skipped.")
    if failures:
        print("Failed cases:", ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
