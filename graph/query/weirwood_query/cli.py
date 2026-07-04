#!/usr/bin/env python3
"""cli.py — `weirwood query …` command line interface.

Absorbs scripts/graph-query.py's argparse CLI and print formatting VERBATIM
(same flags, same text-mode output, same JSON shapes) so
`python3 -m weirwood_query.cli <slug>` (or the `scripts/graph-query.py` compat
shim) produces byte-identical output to the pre-consolidation script.

Usage — legacy flag surface (identical to the old script; byte-for-byte
unchanged):
  python3 -m weirwood_query.cli <slug>
  python3 -m weirwood_query.cli <slug> --edges-only|--inbound-only|--json
  python3 -m weirwood_query.cli --neighbors <slug>
  python3 -m weirwood_query.cli --path <slugA> <slugB>
  python3 -m weirwood_query.cli --health
  python3 -m weirwood_query.cli --event-participants <hub-slug>
  python3 -m weirwood_query.cli --causal-chain <slug> [--expand-beats]
  python3 -m weirwood_query.cli --full-chain <slug> [--expand-beats]
  python3 -m weirwood_query.cli --container <name>
  python3 -m weirwood_query.cli --family-tree <slug>
  python3 -m weirwood_query.cli --edges <path>

Usage — subcommand front door (query-layer design contract; additive
translation layer over the same flags, see `_translate_subcommand` below):
  python3 -m weirwood_query.cli read <slug>              == <slug>
  python3 -m weirwood_query.cli neighbors <slug>          == --neighbors <slug>
  python3 -m weirwood_query.cli path <a> <b>              == --path <a> <b>
  python3 -m weirwood_query.cli health                    == --health
  python3 -m weirwood_query.cli participants <hub>        == --event-participants <hub>
  python3 -m weirwood_query.cli chain <slug>               == --causal-chain <slug>
  python3 -m weirwood_query.cli full-chain <slug>          == --full-chain <slug>
  python3 -m weirwood_query.cli container <name>           == --container <name>
  python3 -m weirwood_query.cli family <slug>              == --family-tree <slug>
  python3 -m weirwood_query.cli resolve <phrase>           -- phrase -> slug (event_alias_resolver --lookup format)
Any extra flags (--json, --expand-beats, ...) pass through unchanged after
the subcommand's positional args.

Usage — braid / convergence-map primitives (query-layer Track, step 7; the
S117 charter un-deferred, graph/convergence-maps/README.md. NEW ops, no
legacy-flag equivalent — full-profile only, no chat port):
  python3 -m weirwood_query.cli fork-hubs [--min-out N] [--include-enables] [--json]
  python3 -m weirwood_query.cli join-hubs [--min-in N] [--include-enables] [--json]
  python3 -m weirwood_query.cli braid <slugA> <slugB> [more...] [--include-enables] [--json]

Usage — content search / browse / corpus scan (query-layer Track, step 5;
design.md D-C, the headline capability). NEW ops, no legacy-flag equivalents:
  python3 -m weirwood_query.cli search <query> [--type CATEGORY] [--limit N] [--json]
  python3 -m weirwood_query.cli list --type CATEGORY [--has-quotes] [--container NAME]
                                      [--limit N] [--offset N] [--json]
  python3 -m weirwood_query.cli corpus-search <query> [--book BOOK] [--mode phrase|tokens]
                                                [--limit N] [--json]
    (corpus-search is CLI-only — full-profile, no bundle/chat exposure; see
    weirwood_query/corpus_search.py's module docstring.)

Usage — theme / mentions (query-layer Track, step 8a/8b; design.md D-E/G4/G13).
NEW ops, no legacy-flag equivalents:
  python3 -m weirwood_query.cli theme [name] [--category CATEGORY] [--json]
    (no name -> lists every theme + member_count)
  python3 -m weirwood_query.cli mentions <slug> [--json]
    (reads the LIVE graph/index/ — may be stale, see G13; a `staleness_note`
    is included when the mention-index-preview repair shows a different count)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import braid as braid_mod
from . import corpus_search as corpus_search_mod
from . import list_nodes as list_nodes_mod
from . import mentions as mentions_mod
from . import report as report_mod
from . import resolve as resolve_mod
from . import search as search_mod
from . import themes as themes_mod
from . import traverse
from .load import EDGES_FILE, NODES_DIR, load_edges

# ---------------------------------------------------------------------------
# Subcommand front door — additive translation layer (query-layer design.md's
# `weirwood query <subcommand> <args>` contract). Maps each subcommand to its
# equivalent legacy flag(s); every legacy flag invocation remains untouched.
# `resolve` has no legacy-flag equivalent in this CLI (it lived only in
# scripts/event_alias_resolver.py --lookup) so it is handled as its own case
# in main(), not translated into a flag.
# ---------------------------------------------------------------------------

# subcommand -> number of positional args it consumes, and the flag(s) to
# splice them into. `None` positional count means "one slug, no flag prefix"
# (the legacy positional node-inspection mode).
_SUBCOMMANDS: dict[str, tuple[int, list[str] | None]] = {
    "read": (1, None),  # positional slug, no flag
    "neighbors": (1, ["--neighbors"]),
    "path": (2, ["--path"]),
    "health": (0, ["--health"]),
    "participants": (1, ["--event-participants"]),
    "chain": (1, ["--causal-chain"]),
    "full-chain": (1, ["--full-chain"]),
    "container": (1, ["--container"]),
    "family": (1, ["--family-tree"]),
    # "resolve" intentionally absent — handled directly in main(), not by flag translation.
}


def _translate_subcommand(argv: list[str]) -> list[str]:
    """If argv[0] names a known subcommand, translate it (+ its positional
    args) into the equivalent legacy flag argv and return that. Extra flags
    after the positionals (e.g. --json, --expand-beats) pass through
    unchanged. If argv[0] is not a known subcommand (including the legacy
    flag surface, e.g. "--health" or a bare slug), return argv unchanged."""
    if not argv:
        return argv
    name = argv[0]
    if name not in _SUBCOMMANDS:
        return argv
    nargs, flag = _SUBCOMMANDS[name]
    positionals = argv[1:1 + nargs]
    rest = argv[1 + nargs:]
    if len(positionals) < nargs:
        # Not enough args for this subcommand — let argparse's normal error
        # path handle it (translate as a no-op so argparse reports the
        # missing legacy flag's own usage message).
        return argv
    if flag is None:
        return positionals + rest
    return flag + positionals + rest


# ---------------------------------------------------------------------------
# Human-readable printers — absorbed verbatim from scripts/graph-query.py
# ---------------------------------------------------------------------------

def print_report(report: dict, *, inbound_only: bool = False, edges_only: bool = False) -> None:
    if report["error"]:
        print(f"ERROR: {report['error']}")
        suggestions = report.get("suggestions", [])
        if suggestions:
            print(f"\nDid you mean:")
            for s in suggestions:
                print(f"  {s}")
        else:
            print("  No alias matches found.")
        return

    node = report["node"]

    print("=" * 70)
    print(f"NODE: {node['slug']}")
    if node.get("top_level_alias"):
        print(f"  (resolved from alias → {node['top_level_alias']})")
    print(f"  Name : {node['name']}")
    print(f"  Type : {node['type']}")
    print(f"  File : {node['file_path']}")
    aliases = node.get("aliases", [])
    if aliases:
        alias_strs = aliases if isinstance(aliases, list) else [aliases]
        print(f"  Aliases: {', '.join(str(a) for a in alias_strs)}")
    else:
        print("  Aliases: (none)")

    if not inbound_only:
        edges = report["edges"]
        print()
        print(f"OUTBOUND EDGES ({len(edges)} total)")
        print("-" * 70)
        if not edges:
            print("  (no edges found)")
        for edge in edges:
            status = edge["resolution_status"]
            status_tag = f"[{status}]"
            rev = " (reverse)" if edge["is_reverse"] else ""
            print(f"  {edge['edge_type']}{rev}")
            print(f"    Target title : {edge['target_title']}")
            print(f"    Target slug  : {edge['target_slug']}  {status_tag}")
            print(f"    Raw line     : {edge['raw']}")
            print()

    if not edges_only:
        total = report["inbound_total"]
        refs = report["inbound"]
        print()
        print(f"INBOUND REFERENCES ({total} total, showing {len(refs)})")
        print("-" * 70)
        if not refs:
            print("  (none found)")
        for ref in refs:
            src = ref.get("source_slug", "?")
            anchor = ref.get("anchor_text", "?")
            snippet = ref.get("snippet", ref.get("context_snippet", ""))
            snippet_short = (snippet[:60] + "...") if len(snippet) > 60 else snippet
            print(f"  [{src}]  anchor='{anchor}'")
            print(f"    {snippet_short}")
        print()

    print("=" * 70)
    print(f"SUMMARY: {report['summary']}")


def print_json(report: dict) -> None:
    if report.get("node"):
        report["node"]["file_path"] = str(report["node"]["file_path"])
    print(json.dumps(report, indent=2, default=str))


def print_neighbors(result: dict, *, json_output: bool) -> None:
    if json_output:
        # node_file is a text-mode-only convenience field (the old script's
        # JSON output never included it) — strip before dumping for exact
        # JSON parity.
        json_result = {k: v for k, v in result.items() if k != "node_file"}
        print(json.dumps(json_result, indent=2, default=str))
        return

    slug = result["slug"]
    print("=" * 72)
    print(f"NEIGHBORS: {slug}")
    if result.get("node_file"):
        print(f"  {result['node_header']}")
        print(f"  File: {result['node_file']}")
    else:
        print("  (no node file found for this slug)")
    print()

    outgoing = result["outgoing"]
    print(f"OUTGOING ({result['outgoing_count']} edges — {slug} is source)")
    print("-" * 72)
    if not outgoing:
        print("  (none)")
    else:
        by_type: dict[str, list[dict]] = {}
        for r in outgoing:
            by_type.setdefault(r["edge_type"], []).append(r)
        for etype in sorted(by_type):
            group = by_type[etype]
            print(f"  [{etype}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
            for r in group:
                print(f"    -> {r['other_slug']}")
                if r.get("evidence_ref"):
                    print(f"       ref  : {r['evidence_ref']}")
                quote80 = traverse._short_quote(r.get("evidence_quote") or "", 80)
                if quote80:
                    print(f"       quote: \"{quote80}\"")
    print()

    incoming = result["incoming"]
    print(f"INCOMING ({result['incoming_count']} edges — {slug} is target)")
    print("-" * 72)
    if not incoming:
        print("  (none)")
    else:
        by_type_in: dict[str, list[dict]] = {}
        for r in incoming:
            by_type_in.setdefault(r["edge_type"], []).append(r)
        for etype in sorted(by_type_in):
            group = by_type_in[etype]
            print(f"  [{etype}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
            for r in group:
                print(f"    <- {r['other_slug']}")
                if r.get("evidence_ref"):
                    print(f"       ref  : {r['evidence_ref']}")
                quote80 = traverse._short_quote(r.get("evidence_quote") or "", 80)
                if quote80:
                    print(f"       quote: \"{quote80}\"")

    print()
    print("=" * 72)
    print(
        f"SUMMARY: {slug}  |  {result['outgoing_count']} outgoing, "
        f"{result['incoming_count']} incoming  "
        f"({result['outgoing_count'] + result['incoming_count']} total)"
    )


def _format_arrow(pivot: str, bridge: str, direction: str, types: list[str]) -> str:
    type_str = "|".join(types) if types else "?"
    if direction == "out":
        return f"{pivot} --[{type_str}]--> {bridge}"
    elif direction == "in":
        return f"{bridge} --[{type_str}]--> {pivot}"
    else:
        return f"{pivot} <-[{type_str}]-> {bridge}"


def print_path(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    slug_a, slug_b = result["slug_a"], result["slug_b"]
    print("=" * 72)
    print(f"PATH: {slug_a}  -->  {slug_b}")
    print(f"  A: {traverse.node_header(slug_a)}")
    print(f"  B: {traverse.node_header(slug_b)}")
    print()

    direct = result["direct_edges"]
    print(f"DIRECT EDGES ({len(direct)})")
    print("-" * 72)
    if not direct:
        print("  (no direct edges between these nodes)")
    for e in direct:
        print(f"  {e['source_slug']}  --[{e['edge_type']}]-->  {e['target_slug']}")
        if e.get("evidence_ref"):
            print(f"    ref  : {e['evidence_ref']}")
        quote80 = traverse._short_quote(e.get("evidence_quote") or "", 80)
        if quote80:
            print(f"    quote: \"{quote80}\"")
        print()

    total_bridges = result["total_bridges"]
    bridges = result["bridges"]
    print(
        f"2-HOP BRIDGES ({total_bridges} common neighbors"
        + (f", showing top {result['bridges_shown']}" if total_bridges > result["bridges_shown"] else "")
        + ")"
    )
    print("-" * 72)
    if not bridges:
        print("  (no common neighbors)")
    for b in bridges:
        a_arrow = _format_arrow(slug_a, b["bridge"], b["a_dir"], b["a_types"])
        b_arrow = _format_arrow(slug_b, b["bridge"], b["b_dir"], b["b_types"])
        print(f"  {a_arrow}  --[{b['bridge']}]--  {b_arrow}")

    print()
    print("=" * 72)
    print(
        f"SUMMARY: {slug_a} → {slug_b}  |  "
        f"{len(direct)} direct edges, {total_bridges} 2-hop bridges"
    )


def print_health(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    print("GRAPH HEALTH REPORT")
    print("=" * 72)
    print(f"  Node files (*.node.md)  : {result['node_count']:>7,}")
    print(f"  Edge count              : {result['edge_count']:>7,}")
    print(f"  Unique edge endpoints   : {result['unique_endpoints']:>7,}")
    print(f"  Orphan endpoints        : {result['orphan_endpoint_count']:>7,}  "
          f"(endpoints with no node file)")
    print()

    type_dist = result["edge_type_distribution"]
    print(f"EDGE-TYPE DISTRIBUTION  ({len(type_dist)} types)")
    print("-" * 72)
    for etype, cnt in type_dist:
        bar = "#" * min(cnt // 5, 40)
        print(f"  {etype:<30}  {cnt:>5}  {bar}")
    print()

    orphan_count = result["orphan_endpoint_count"]
    if orphan_count == 0:
        print("ORPHAN ENDPOINTS: none — all edge endpoints have node files")
    else:
        orphan_endpoints = result["orphan_endpoints"]
        print(f"ORPHAN ENDPOINTS ({orphan_count})")
        print("-" * 72)
        for s in orphan_endpoints[:50]:
            print(f"  {s}")
        if orphan_count > 50:
            print(f"  ... and {orphan_count - 50} more")
    print()

    degree_leaders = result["degree_leaders"]
    print(f"DEGREE LEADERS (top {traverse.DEGREE_TOP_N} — total edges touching each entity)")
    print("-" * 72)
    for rank, entry in enumerate(degree_leaders, 1):
        deg = entry["degree"]
        bar = "#" * min(deg // 10, 35)
        print(f"  {rank:>2}. {entry['slug']:<40}  {deg:>5}  {bar}")

    print()
    print("=" * 72)
    print(f"SUMMARY: {result['node_count']:,} nodes, {result['edge_count']:,} edges, "
          f"{orphan_count} orphan endpoints, "
          f"{len(type_dist)} edge types")


def print_event_participants(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2))
        return

    if result.get("error"):
        print(f"ERROR: {result['error']}")
        print("  No node file found for this slug. Check spelling.")
        suggestions = result.get("suggestions", [])
        if suggestions:
            print("  Did you mean:")
            for s in suggestions:
                print(f"    {s}")
        return

    hub_slug = result["hub_slug"]
    hub_label = result["hub_node"]

    if result["beat_count"] == 0:
        print("=" * 72)
        print(f"EVENT PARTICIPANTS: {hub_slug}")
        print(f"  {hub_label}")
        print()
        print(
            "  No beats found — this hub has no reified children "
            "(no SUB_BEAT_OF edges incoming)."
        )
        print(
            "  All role edges must be directly on the hub itself (check "
            "--neighbors) or the event has not been mined yet."
        )
        print()
        print("=" * 72)
        print(f"SUMMARY: 0 beats, 0 participants")
        return

    beat_slugs = result["beats"]
    print("=" * 72)
    print(f"EVENT PARTICIPANTS: {hub_slug}")
    print(f"  {hub_label}")
    print(f"  Beats ({len(beat_slugs)}): {', '.join(beat_slugs)}")
    print()

    participants = result["participants"]
    if not participants:
        print("  (beats found but no participant role edges on any beat)")
        print()
        print("=" * 72)
        print(f"SUMMARY: {len(beat_slugs)} beats, 0 participant edges")
        return

    by_role: dict[str, list[dict]] = {}
    for r in participants:
        by_role.setdefault(r["role_type"], []).append(r)

    print(f"PARTICIPANTS BY ROLE  ({len(participants)} total role edges)")
    print("-" * 72)

    for role_type in sorted(by_role):
        group = by_role[role_type]
        print(f"\n  [{role_type}]  ({len(group)} edge{'s' if len(group) != 1 else ''})")
        for rec in group:
            source = rec["source_slug"]
            beat = rec["beat_slug"]
            chapter = rec.get("evidence_chapter") or rec.get("evidence_book") or ""
            quote = rec.get("evidence_quote", "")
            print(f"    {source}")
            print(f"      via beat : {beat}")
            if chapter:
                print(f"      chapter  : {chapter}")
            if quote:
                print(f"      quote    : \"{quote}\"")

    print()
    print("=" * 72)
    distinct_sources = {r["source_slug"] for r in participants}
    print(
        f"SUMMARY: {hub_slug}  |  "
        f"{len(beat_slugs)} beats, "
        f"{len(participants)} role edges, "
        f"{len(distinct_sources)} distinct participants"
    )


def print_causal_chain(result: dict, *, json_output: bool, expand_beats: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    slug = result["slug"]
    full = result["mode"] == "full-chain"
    edge_types = result["edge_types"]
    type_label = " / ".join(edge_types)

    print("=" * 72)
    print(f"{'FULL CHAIN' if full else 'CAUSAL CHAIN'}: {slug}")
    print(f"  {traverse.node_header(slug)}")
    print(f"  walks {type_label} (transitive, both directions)")
    if full:
        print("  (ENABLES hops shown as preconditions; --causal-chain omits them)")
    print()

    upstream = result["upstream"]
    n_up = len(upstream)
    print(f"UPSTREAM — what led to this  ({n_up} edge{'s' if n_up != 1 else ''})")
    print("-" * 72)
    if not upstream:
        print("  (none — no causal antecedents)")
    else:
        for e in sorted(upstream, key=lambda r: (-r["depth"], r["source_slug"])):
            indent = "  " * (e["depth"] - 1)
            print(f"  {indent}{e['source_slug']} --[{traverse._edge_label(e)}]--> "
                  f"{e['target_slug']}")
    print()

    downstream = result["downstream"]
    n_down = len(downstream)
    print(f"DOWNSTREAM — what this led to  ({n_down} edge{'s' if n_down != 1 else ''})")
    print("-" * 72)
    if not downstream:
        print("  (none — no causal consequences)")
    else:
        for e in sorted(downstream, key=lambda r: (r["depth"], r["target_slug"])):
            indent = "  " * (e["depth"] - 1)
            print(f"  {indent}{e['source_slug']} --[{traverse._edge_label(e)}]--> "
                  f"{e['target_slug']}")
    print()

    if expand_beats:
        beat_map = result.get("beats", {})
        n_beat_nodes = len(beat_map)
        print(f"BEAT EXPANSION — sub-beats & roles within chain nodes  "
              f"({n_beat_nodes} node{'s' if n_beat_nodes != 1 else ''} with beats)")
        print("-" * 72)
        if not beat_map:
            print("  (no SUB_BEAT_OF children on any chain node)")
        else:
            # Edge-discovery order (old script's `chain_nodes`), NOT the sorted
            # upstream_nodes/downstream_nodes JSON fields — those are sorted
            # sets for JSON parity and would reorder the printed beat sections.
            seen_nodes = {slug}
            ordered = [slug]
            for e in upstream + downstream:
                for n in (e["source_slug"], e["target_slug"]):
                    if n not in seen_nodes:
                        seen_nodes.add(n)
                        ordered.append(n)
            for node in ordered:
                if node not in beat_map:
                    continue
                print(f"  {node}")
                for b in beat_map[node]:
                    print(f"    {b['beat']}  [SUB_BEAT_OF]")
                    for role_type, participant in b["roles"]:
                        print(f"      {participant} --[{role_type}]--> {b['beat']}")
        print()

    print("=" * 72)
    total = n_up + n_down
    print(
        f"SUMMARY: {slug}  |  {n_up} upstream + {n_down} downstream "
        f"= {total} {'chain' if full else 'causal'} edge{'s' if total != 1 else ''}"
        + (f"  |  {len(result.get('beats', {}))} node(s) with beats" if expand_beats else "")
    )


def print_container(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    name = result["container"]
    matches = result["nodes"]
    print("=" * 72)
    print(f"CONTAINER: {name}   (bag-retrieval — unordered; for the arc use --causal-chain)")
    print("-" * 72)
    if not matches:
        print(f"  (no nodes carry containers: [... {name} ...])")
    else:
        target = name.strip().lower()
        for m in matches:
            extra = [c for c in m["containers"] if c.lower() != target]
            seam = f"  (+{', '.join(extra)})" if extra else ""
            print(f"  {m['slug']}  —  {m['type']}{seam}")
    print("=" * 72)
    print(f"SUMMARY: container '{name}' = {len(matches)} node"
          f"{'s' if len(matches) != 1 else ''}")


def print_fork_hubs(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    mode = "CAUSAL+ENABLES" if result["include_enables"] else "CAUSAL"
    print(f"FORK HUBS ({mode})  —  divergence points, direct out-degree >= {result['min_out']}")
    print("-" * 72)
    hubs = result["hubs"]
    if not hubs:
        print(f"  (no nodes with direct out-degree >= {result['min_out']})")
    else:
        for rank, h in enumerate(hubs, 1):
            print(
                f"  {rank:>2}. {h['slug']:<45}  out={h['out_degree']:<3}  "
                f"downstream_reach={h['downstream_reach']:<4}  {h['node_header']}"
            )
    print("=" * 72)
    print(f"SUMMARY: {result['count']} fork hub(s) at min_out={result['min_out']} ({mode})")


def print_join_hubs(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    mode = "CAUSAL+ENABLES" if result["include_enables"] else "CAUSAL"
    print(f"JOIN HUBS ({mode})  —  convergence points, direct in-degree >= {result['min_in']}")
    print("-" * 72)
    hubs = result["hubs"]
    if not hubs:
        print(f"  (no nodes with direct in-degree >= {result['min_in']})")
    else:
        for rank, h in enumerate(hubs, 1):
            print(
                f"  {rank:>2}. {h['slug']:<45}  in={h['in_degree']:<3}  "
                f"upstream_reach={h['upstream_reach']:<4}  {h['node_header']}"
            )
    print("=" * 72)
    print(f"SUMMARY: {result['count']} join hub(s) at min_in={result['min_in']} ({mode})")


def print_braid(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    if result.get("error"):
        print(f"ERROR: {result['error']}")
        return

    slugs = result["slugs"]
    mode = "CAUSAL+ENABLES" if result["include_enables"] else "CAUSAL"
    print("=" * 72)
    print(f"BRAID ({mode}):  " + "  <->  ".join(slugs))
    print("=" * 72)

    shared_anc = result["shared_ancestors"]
    print(f"\nSHARED ANCESTORS — divergence point(s) upstream of EVERY strand ({len(shared_anc)})")
    print("-" * 72)
    if not shared_anc:
        print("  (none — no single node is upstream of all strands)")
    for a in shared_anc:
        print(f"  {a['slug']}  —  {a['node_header']}")

    shared_desc = result["shared_descendants"]
    print(f"\nSHARED DESCENDANTS — convergence point(s) downstream of EVERY strand ({len(shared_desc)})")
    print("-" * 72)
    if not shared_desc:
        print("  (none — no single node is downstream of all strands)")
    for d in shared_desc:
        print(f"  {d['slug']}  —  {d['node_header']}")

    print(f"\nPAIRWISE OVERLAP ({len(result['pairwise'])} pair(s))")
    print("-" * 72)
    for p in result["pairwise"]:
        print(f"  {p['a']}  <->  {p['b']}")
        print(f"    shared ancestors   ({len(p['shared_ancestors'])}): {', '.join(p['shared_ancestors']) or '(none)'}")
        print(f"    shared descendants ({len(p['shared_descendants'])}): {', '.join(p['shared_descendants']) or '(none)'}")
        print(f"    offset/shared-middle ({len(p['offset_shared_middle'])}): {', '.join(p['offset_shared_middle']) or '(none)'}")

    print(f"\nPER-STRAND CHAINS")
    print("-" * 72)
    for slug in slugs:
        strand = result["per_strand"][slug]
        print(
            f"  {slug}: {strand['upstream_count']} upstream + "
            f"{strand['downstream_count']} downstream {strand['mode']} edges"
        )

    print()
    print("=" * 72)
    print(
        f"SUMMARY: {len(slugs)} strands  |  "
        f"{len(shared_anc)} shared ancestor(s), {len(shared_desc)} shared descendant(s)"
    )


def print_search(query: str, results: list[dict], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"query": query, "results": results}, indent=2, default=str))
        return

    print("=" * 72)
    print(f"SEARCH: {query!r}")
    print("-" * 72)
    if not results:
        print("  (no matching quotes/identity blurbs)")
    for i, r in enumerate(results, 1):
        text80 = traverse._short_quote(r.get("text") or "", 100)
        print(f"  {i:>2}. [{r['score']:.3f}]  {r['slug']}  ({r['type']})")
        if r.get("cite"):
            print(f"      cite : {r['cite']}")
        print(f"      text : \"{text80}\"")
    print("=" * 72)
    print(f"SUMMARY: {len(results)} result(s) for {query!r}")


def print_list(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    print(f"LIST: category={result['category']}")
    print(
        f"  total={result['total']}  offset={result['offset']}  "
        f"limit={result['limit']}  showing={len(result['items'])}"
    )
    print("-" * 72)
    if not result["items"]:
        print("  (no matching nodes)")
    for it in result["items"]:
        print(f"  {it['slug']:<40}  {it['name']:<30}  quotes={it['quote_count']}")
    print("=" * 72)
    print(f"SUMMARY: {result['total']} node(s) in category '{result['category']}'")


def print_corpus_search(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    scope = f" (book={result['book']})" if result.get("book") else ""
    print(f"CORPUS SEARCH: {result['query']!r}{scope}  mode={result['mode']}")
    print("-" * 72)
    matches = result["matches"]
    if not matches:
        print("  (no matching lines)")
    for m in matches:
        print(f"  {m['cite']}")
        print(f"    {m['text'][:140]}")
    print("=" * 72)
    shown_note = f", showing {len(matches)}" if result["total"] > len(matches) else ""
    print(f"SUMMARY: {result['total']} matching line(s){shown_note}")


def print_theme(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    if result.get("error"):
        print(f"THEME: {result['theme']!r} — ERROR: {result['error']}")
        known = result.get("known_themes", [])
        if known:
            print("  Known themes:")
            for t in known:
                print(f"    {t}")
        print("=" * 72)
        return

    print(f"THEME: {result['theme']}")
    print(f"  member_count={result['member_count']}")
    print("-" * 72)
    for m in result["members"]:
        print(f"  {m['slug']:<40}  {m['category']:<14}  {m['name']}")
    print("=" * 72)
    print(f"SUMMARY: theme '{result['theme']}' = {result['member_count']} member(s)")


def print_theme_list(themes_list: list[dict], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"themes": themes_list}, indent=2, default=str))
        return

    print("=" * 72)
    print("THEMES")
    print("-" * 72)
    if not themes_list:
        print("  (theme index not built — run graph/query/build/build_theme_index.py)")
    for t in themes_list:
        print(f"  {t['name']:<24}  {t['member_count']:>4} members")
    print("=" * 72)
    print(f"SUMMARY: {len(themes_list)} theme(s)")


def print_mentions(result: dict, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result, indent=2, default=str))
        return

    print("=" * 72)
    print(f"MENTIONS: {result['slug']}")
    print(f"  source: {result['source']}")
    if result.get("staleness_note"):
        print(f"  ** {result['staleness_note']} **")
    print(f"  chapter_count={result['chapter_count']}  appearances_total={result['appearances_total']}")
    print("-" * 72)
    if not result["chapters"]:
        print("  (no chapters found)")
    for c in result["chapters"]:
        print(f"  {c['chapter_id']:<28}  book={c['book']:<6}  pov={c.get('pov_character','?'):<14}  "
              f"mentions={c['mention_count']}  via={','.join(c['resolved_via'])}")
    print("=" * 72)
    print(f"SUMMARY: {result['chapter_count']} chapter(s), {result['appearances_total']} appearance(s)")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

def print_resolve(phrase: str, slug: str | None, status: str, candidates: list[dict]) -> None:
    """Print a phrase->slug resolution in the same format as
    scripts/event_alias_resolver.py --lookup (minus its deprecation-shim
    stderr banner, which is specific to that compat shim, not this CLI)."""
    from .normalize import normalize

    norm = normalize(phrase)
    print(f"Input:      {phrase!r}")
    print(f"Normalized: {norm!r}")
    if status == "hit":
        print(f"Result:     {slug}")
        print(f"Status:     HIT")
    elif status == "hit-character":
        print(f"Result:     {slug}")
        print(f"Status:     HIT-CHARACTER (character node; use --neighbors {slug} to find edges)")
        if len(candidates) > 1:
            print(f"Alternates: {', '.join(c['slug'] for c in candidates[1:])}")
    elif status == "ambiguous":
        print(f"Result:     (ambiguous — multiple slugs match this phrase)")
        print(f"Status:     AMBIGUOUS")
    elif status == "candidates":
        if slug:
            print(f"Result:     {slug}  [top candidate, score={candidates[0]['score']:.2f}]")
            print(f"Status:     CANDIDATES (fuzzy match; verify before use)")
        else:
            print(f"Result:     (no confident single match)")
            print(f"Status:     CANDIDATES (fuzzy; multiple close matches)")
        if candidates:
            print(f"Ranked candidates:")
            for i, c in enumerate(candidates, 1):
                cat = c.get("node_category", "")
                typ = c.get("node_type", "")
                label = f"{cat}/{typ}" if typ else cat
                print(f"  {i}. {c['slug']}  score={c['score']:.2f}  [{label}]  match={c['match_type']}")
    else:
        print(f"Result:     (no match)")
        print(f"Status:     MISS")


def main() -> None:
    argv = sys.argv[1:]

    # `resolve` has no legacy-flag equivalent — handle it before any argparse
    # translation/parsing (it takes a free-text PHRASE, not a slug).
    if argv and argv[0] == "resolve":
        if len(argv) < 2:
            print("usage: weirwood query resolve <phrase>", file=sys.stderr)
            sys.exit(2)
        phrase = argv[1]
        json_output = "--json" in argv[2:]
        slug, status, candidates = resolve_mod.resolve(phrase)
        if json_output:
            print(json.dumps(
                {"phrase": phrase, "slug": slug, "status": status, "candidates": candidates},
                indent=2, default=str,
            ))
        else:
            print_resolve(phrase, slug, status, candidates)
        sys.exit(0)

    # `fork-hubs` / `join-hubs` / `braid` (query-layer Track, step 7 — the
    # S117 convergence-map charter). No legacy-flag equivalents (these are
    # NEW ops, additive-only); handled directly, same pattern as `resolve`
    # above, before the subcommand-translation layer ever sees them.
    if argv and argv[0] == "fork-hubs":
        rest = argv[1:]
        json_output = "--json" in rest
        include_enables = "--include-enables" in rest
        min_out = braid_mod.DEFAULT_MIN_OUT
        if "--min-out" in rest:
            idx = rest.index("--min-out")
            min_out = int(rest[idx + 1])
        edges = load_edges()
        result = braid_mod.fork_hubs(edges, min_out=min_out, include_enables=include_enables)
        print_fork_hubs(result, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "join-hubs":
        rest = argv[1:]
        json_output = "--json" in rest
        include_enables = "--include-enables" in rest
        min_in = braid_mod.DEFAULT_MIN_IN
        if "--min-in" in rest:
            idx = rest.index("--min-in")
            min_in = int(rest[idx + 1])
        edges = load_edges()
        result = braid_mod.join_hubs(edges, min_in=min_in, include_enables=include_enables)
        print_join_hubs(result, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "braid":
        rest = argv[1:]
        json_output = "--json" in rest
        include_enables = "--include-enables" in rest
        slugs = [a for a in rest if not a.startswith("--")]
        if len(slugs) < 2:
            print("usage: weirwood query braid <slugA> <slugB> [more...] [--json] [--include-enables]", file=sys.stderr)
            sys.exit(2)
        edges = load_edges()
        result = braid_mod.braid(slugs, edges, include_enables=include_enables)
        print_braid(result, json_output=json_output)
        sys.exit(0)

    # `search` / `list` / `corpus-search` (query-layer Track, step 5; design.md
    # D-C). No legacy-flag equivalents (new ops); handled directly, same
    # pattern as resolve/braid above, before the subcommand-translation layer.
    if argv and argv[0] == "search":
        rest = argv[1:]
        json_output = "--json" in rest
        node_type = None
        if "--type" in rest:
            idx = rest.index("--type")
            node_type = rest[idx + 1]
        limit = search_mod.DEFAULT_LIMIT
        if "--limit" in rest:
            idx = rest.index("--limit")
            limit = int(rest[idx + 1])
        positionals = [a for a in rest if not a.startswith("--")]
        # Strip values already consumed by --type/--limit from the positional
        # scan (e.g. "search cakes --type foods" must not treat "foods" as
        # part of the query).
        consumed = set()
        if "--type" in rest:
            consumed.add(rest[rest.index("--type") + 1])
        if "--limit" in rest:
            consumed.add(rest[rest.index("--limit") + 1])
        query_parts = [a for a in positionals if a not in consumed]
        if not query_parts:
            print("usage: weirwood query search <query> [--type CATEGORY] [--limit N] [--json]", file=sys.stderr)
            sys.exit(2)
        query = " ".join(query_parts)
        results = search_mod.search(query, node_type=node_type, limit=limit)
        print_search(query, results, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "list":
        rest = argv[1:]
        json_output = "--json" in rest
        has_quotes = "--has-quotes" in rest
        category = None
        if "--type" in rest:
            category = rest[rest.index("--type") + 1]
        container_name = None
        if "--container" in rest:
            container_name = rest[rest.index("--container") + 1]
        limit = list_nodes_mod.DEFAULT_LIMIT
        if "--limit" in rest:
            limit = int(rest[rest.index("--limit") + 1])
        offset = 0
        if "--offset" in rest:
            offset = int(rest[rest.index("--offset") + 1])
        if not category:
            print("usage: weirwood query list --type CATEGORY [--has-quotes] [--container NAME] "
                  "[--limit N] [--offset N] [--json]", file=sys.stderr)
            sys.exit(2)
        result = list_nodes_mod.list_nodes(
            category, has_quotes=has_quotes, container=container_name, limit=limit, offset=offset,
        )
        print_list(result, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "corpus-search":
        rest = argv[1:]
        json_output = "--json" in rest
        book = None
        if "--book" in rest:
            book = rest[rest.index("--book") + 1]
        mode = "phrase"
        if "--mode" in rest:
            mode = rest[rest.index("--mode") + 1]
        limit = corpus_search_mod.DEFAULT_LIMIT
        if "--limit" in rest:
            limit = int(rest[rest.index("--limit") + 1])
        consumed = set()
        if "--book" in rest:
            consumed.add(rest[rest.index("--book") + 1])
        if "--mode" in rest:
            consumed.add(rest[rest.index("--mode") + 1])
        if "--limit" in rest:
            consumed.add(rest[rest.index("--limit") + 1])
        query_parts = [a for a in rest if not a.startswith("--") and a not in consumed]
        if not query_parts:
            print("usage: weirwood query corpus-search <query> [--book BOOK] [--mode phrase|tokens] "
                  "[--limit N] [--json]", file=sys.stderr)
            sys.exit(2)
        query = " ".join(query_parts)
        result = corpus_search_mod.corpus_search(query, book=book, mode=mode, limit=limit)
        print_corpus_search(result, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "theme":
        rest = argv[1:]
        json_output = "--json" in rest
        category = None
        if "--category" in rest:
            category = rest[rest.index("--category") + 1]
        consumed = set()
        if "--category" in rest:
            consumed.add(rest[rest.index("--category") + 1])
        name_parts = [a for a in rest if not a.startswith("--") and a not in consumed]
        if not name_parts:
            themes_list = themes_mod.list_themes()
            print_theme_list(themes_list, json_output=json_output)
            sys.exit(0)
        name = " ".join(name_parts)
        result = themes_mod.theme(name, category=category)
        print_theme(result, json_output=json_output)
        sys.exit(0)

    if argv and argv[0] == "mentions":
        rest = argv[1:]
        json_output = "--json" in rest
        positionals = [a for a in rest if not a.startswith("--")]
        if not positionals:
            print("usage: weirwood query mentions <slug> [--json]", file=sys.stderr)
            sys.exit(2)
        slug = positionals[0]
        result = mentions_mod.mentions(slug)
        print_mentions(result, json_output=json_output)
        sys.exit(0)

    # Subcommand front door (query-layer design contract): translate a known
    # subcommand + its positional args into the equivalent legacy flag argv.
    # No-op for the legacy flag surface itself (unrecognized subcommand names,
    # including "--health"/a bare slug, pass through unchanged) — legacy
    # invocations are byte-identical, this is purely additive.
    sys.argv = [sys.argv[0]] + _translate_subcommand(argv)

    parser = argparse.ArgumentParser(
        description=(
            "Inspect Weirwood Network graph nodes and edges.\n\n"
            "NODE INSPECTION (original):\n"
            "  weirwood query <slug> [--edges-only] [--inbound-only] [--json]\n\n"
            "CANONICAL EDGE LAYER:\n"
            "  weirwood query --neighbors <slug>\n"
            "  weirwood query --path <slugA> <slugB>\n"
            "  weirwood query --health\n"
            "  weirwood query --event-participants <hub-slug>\n"
            "  weirwood query --causal-chain <slug>\n"
            "  weirwood query --full-chain <slug>\n"
            "  weirwood query --container <name>\n"
            "  weirwood query --family-tree <slug>\n"
            "  weirwood query --edges <path>   (override edges.jsonl location)\n\n"
            "SUBCOMMAND FRONT DOOR (additive; translates to the flags above —\n"
            "extra flags like --json/--expand-beats pass through unchanged):\n"
            "  weirwood query read <slug>\n"
            "  weirwood query neighbors <slug>\n"
            "  weirwood query path <slugA> <slugB>\n"
            "  weirwood query health\n"
            "  weirwood query participants <hub-slug>\n"
            "  weirwood query chain <slug>\n"
            "  weirwood query full-chain <slug>\n"
            "  weirwood query container <name>\n"
            "  weirwood query family <slug>\n"
            "  weirwood query resolve <phrase>   (phrase -> slug; no legacy-flag form)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "slug", nargs="?", default=None,
        help="Node slug for node inspection (e.g. house-stark, eddard-stark)",
    )
    parser.add_argument("--edges-only", action="store_true",
                         help="(node inspection) Print only outbound edges, skip inbound references.")
    parser.add_argument("--inbound-only", action="store_true",
                         help="(node inspection) Print only inbound references (top 50).")
    parser.add_argument("--json", action="store_true", dest="json_output",
                         help="Output machine-readable JSON instead of formatted text.")

    parser.add_argument("--neighbors", metavar="SLUG", default=None,
                         help="Show all edges touching SLUG, split OUTGOING/INCOMING, grouped by edge_type.")
    parser.add_argument("--path", nargs=2, metavar=("SLUG_A", "SLUG_B"), default=None,
                         help="Show direct edges between SLUG_A and SLUG_B, plus 2-hop bridges.")
    parser.add_argument("--health", action="store_true",
                         help="Print graph-wide stats.")
    parser.add_argument("--event-participants", metavar="HUB_SLUG", default=None, dest="event_participants",
                         help="Union participant role edges across SUB_BEAT_OF children of HUB_SLUG.")
    parser.add_argument("--causal-chain", metavar="SLUG", default=None, dest="causal_chain",
                         help="Walk CAUSES/TRIGGERS/MOTIVATES edges transitively, both directions.")
    parser.add_argument("--full-chain", "--include-enables", metavar="SLUG", default=None, dest="full_chain",
                         help="Like --causal-chain but also follows ENABLES preconditions.")
    parser.add_argument("--expand-beats", action="store_true", dest="expand_beats",
                         help="Modifier for --causal-chain/--full-chain: surface SUB_BEAT_OF children + role edges.")
    parser.add_argument("--container", metavar="NAME", default=None,
                         help="Bag-retrieval: list every node whose containers: array contains NAME.")
    parser.add_argument("--family-tree", metavar="SLUG", default=None, dest="family_tree",
                         help="Walk the lineage around SLUG (PARENT_OF/SPOUSE_OF), ported from web/src/lib/graph.ts.")
    parser.add_argument("--edges", metavar="PATH", default=None,
                         help=f"Override path to edges.jsonl (default: {EDGES_FILE})")

    args = parser.parse_args()

    new_mode = (
        args.neighbors or args.path or args.health or args.event_participants
        or args.causal_chain or args.full_chain or args.container or args.family_tree
    )
    old_mode = args.slug is not None

    if new_mode and old_mode:
        parser.error(
            "Cannot combine a positional slug with "
            "--neighbors / --path / --health / --event-participants / "
            "--causal-chain / --full-chain / --container / --family-tree. Use one mode at a time."
        )

    if args.expand_beats and not (args.causal_chain or args.full_chain):
        parser.error("--expand-beats must be combined with --causal-chain or --full-chain.")

    if not new_mode and not old_mode:
        parser.print_help()
        sys.exit(0)

    if new_mode:
        if args.container:
            result = traverse.container(args.container)
            print_container(result, json_output=args.json_output)
            sys.exit(0)

        if args.family_tree:
            edges = load_edges(Path(args.edges) if args.edges else EDGES_FILE)
            nodes = traverse.build_family_nodes_map(NODES_DIR)
            result = traverse.family_tree(args.family_tree, edges, nodes)
            print(json.dumps(result, indent=2, default=str))
            sys.exit(0)

        edges_path = Path(args.edges) if args.edges else EDGES_FILE
        try:
            edges = load_edges(edges_path)
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.neighbors:
            result = traverse.neighbors(args.neighbors, edges)
            print_neighbors(result, json_output=args.json_output)

        elif args.path:
            result = traverse.path(args.path[0], args.path[1], edges)
            print_path(result, json_output=args.json_output)

        elif args.health:
            result = traverse.health(edges, NODES_DIR)
            print_health(result, json_output=args.json_output)

        elif args.event_participants:
            result = traverse.event_participants(args.event_participants, edges, NODES_DIR)
            print_event_participants(result, json_output=args.json_output)

        elif args.causal_chain:
            result = traverse.causal_chain(
                args.causal_chain, edges, expand_beats=args.expand_beats,
            )
            print_causal_chain(result, json_output=args.json_output, expand_beats=args.expand_beats)

        elif args.full_chain:
            result = traverse.causal_chain(
                args.full_chain, edges,
                edge_types=traverse.FULL_CHAIN_EDGE_TYPES, expand_beats=args.expand_beats,
            )
            print_causal_chain(result, json_output=args.json_output, expand_beats=args.expand_beats)

        sys.exit(0)

    if args.edges_only and args.inbound_only:
        parser.error("--edges-only and --inbound-only are mutually exclusive.")

    inbound_limit = 50 if args.inbound_only else 20

    report = report_mod.build_report(
        args.slug,
        edges_only=args.edges_only,
        inbound_only=args.inbound_only,
        inbound_limit=inbound_limit,
    )

    if args.json_output:
        print_json(report)
    else:
        print_report(report, inbound_only=args.inbound_only, edges_only=args.edges_only)

    if report["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
