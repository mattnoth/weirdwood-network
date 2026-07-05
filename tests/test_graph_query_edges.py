"""Tests for the canonical edge-layer modes added to graph-query.py.

Covers:
  - --neighbors: outgoing vs incoming split, grouped by edge_type
  - --path: direct edges + 2-hop bridge detection
  - --health: node count, edge count, type distribution, orphan detection,
              degree leaders

Uses small in-memory / tmp-file fixtures only — does NOT depend on the
real 3,811-edge edges.jsonl.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# S191 (shim retirement Tier B): imports the weirwood_query package directly —
# previously loaded the scripts/graph-query.py compat shim via _helpers. The
# shim's cmd_* wrappers were compute(traverse) + print(cli) glue; the flat
# namespace below re-composes those two calls, so both halves stay covered
# and the test bodies are unchanged.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "graph" / "query"))
from weirwood_query import cli as wq_cli  # noqa: E402
from weirwood_query import load as wq_load  # noqa: E402
from weirwood_query import traverse as wq_traverse  # noqa: E402


class _GQ:
    """Flat namespace matching the old shim surface these tests were written
    against (load_edges + cmd_*), now backed by package calls."""

    load_edges = staticmethod(wq_load.load_edges)

    @staticmethod
    def cmd_neighbors(slug, edges, *, json_output=False):
        wq_cli.print_neighbors(wq_traverse.neighbors(slug, edges), json_output=json_output)

    @staticmethod
    def cmd_path(slug_a, slug_b, edges, *, json_output=False):
        wq_cli.print_path(wq_traverse.path(slug_a, slug_b, edges), json_output=json_output)

    @staticmethod
    def cmd_health(edges, nodes_dir, *, json_output=False):
        wq_cli.print_health(wq_traverse.health(edges, nodes_dir), json_output=json_output)

    @staticmethod
    def cmd_causal_chain(slug, edges, *, json_output=False, expand_beats=False):
        result = wq_traverse.causal_chain(slug, edges, expand_beats=expand_beats)
        wq_cli.print_causal_chain(result, json_output=json_output, expand_beats=expand_beats)


gq = _GQ()

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# Minimal edge set shared across most tests:
#
#  arya-stark  --[LOVES]-->     jon-snow
#  arya-stark  --[FEARS]-->     cersei-lannister
#  jon-snow    --[SERVES]-->    ned-stark
#  cersei-lannister --[HATES]--> ned-stark
#
# Bridges between arya-stark and ned-stark:
#   arya–[LOVES]→jon–[SERVES]→ned   (jon-snow is a bridge)
#   arya–[FEARS]→cersei–[HATES]→ned  (cersei-lannister is a bridge)

EDGES_FIXTURE = [
    {
        "edge_type": "LOVES",
        "source_slug": "arya-stark",
        "target_slug": "jon-snow",
        "evidence_ref": "sources/chapters/agot/agot-arya-01.md:10",
        "evidence_quote": "Jon was her brother and best friend.",
        "confidence_tier": 1,
        "dup_count": 1,
    },
    {
        "edge_type": "FEARS",
        "source_slug": "arya-stark",
        "target_slug": "cersei-lannister",
        "evidence_ref": "sources/chapters/agot/agot-arya-02.md:20",
        "evidence_quote": "Arya hated the queen.",
        "confidence_tier": 1,
        "dup_count": 1,
    },
    {
        "edge_type": "SERVES",
        "source_slug": "jon-snow",
        "target_slug": "ned-stark",
        "evidence_ref": "sources/chapters/agot/agot-jon-01.md:5",
        "evidence_quote": "Jon respected his lord father.",
        "confidence_tier": 1,
        "dup_count": 1,
    },
    {
        "edge_type": "HATES",
        "source_slug": "cersei-lannister",
        "target_slug": "ned-stark",
        "evidence_ref": "sources/chapters/agot/agot-eddard-01.md:100",
        "evidence_quote": "Cersei despised Stark.",
        "confidence_tier": 1,
        "dup_count": 1,
    },
]


def _write_edges(tmp_path: Path, rows: list[dict]) -> Path:
    """Write a list of edge dicts to a JSONL file and return the path."""
    p = tmp_path / "edges.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# --neighbors tests
# ---------------------------------------------------------------------------

class TestNeighbors:
    """Tests for cmd_neighbors via JSON output (avoids stdout parsing)."""

    def _run(self, slug: str, edges: list[dict], tmp_path: Path) -> dict:
        """Run cmd_neighbors with --json and capture the printed JSON."""
        import io
        from contextlib import redirect_stdout

        edges_file = _write_edges(tmp_path, edges)
        loaded = gq.load_edges(edges_file)
        buf = io.StringIO()
        with redirect_stdout(buf):
            gq.cmd_neighbors(slug, loaded, json_output=True)
        return json.loads(buf.getvalue())

    def test_outgoing_and_incoming_counts(self, tmp_path):
        result = self._run("arya-stark", EDGES_FIXTURE, tmp_path)
        # arya is source in 2 edges, target in 0
        assert result["outgoing_count"] == 2
        assert result["incoming_count"] == 0

    def test_incoming_only(self, tmp_path):
        result = self._run("ned-stark", EDGES_FIXTURE, tmp_path)
        # ned is target in 2 edges (jon SERVES ned, cersei HATES ned)
        assert result["incoming_count"] == 2
        assert result["outgoing_count"] == 0

    def test_bidirectional_node(self, tmp_path):
        result = self._run("jon-snow", EDGES_FIXTURE, tmp_path)
        # jon is target of arya's LOVES, source of SERVES ned
        assert result["outgoing_count"] == 1
        assert result["incoming_count"] == 1

    def test_outgoing_edge_types_present(self, tmp_path):
        result = self._run("arya-stark", EDGES_FIXTURE, tmp_path)
        types = {r["edge_type"] for r in result["outgoing"]}
        assert "LOVES" in types
        assert "FEARS" in types

    def test_outgoing_other_slugs(self, tmp_path):
        result = self._run("arya-stark", EDGES_FIXTURE, tmp_path)
        others = {r["other_slug"] for r in result["outgoing"]}
        assert "jon-snow" in others
        assert "cersei-lannister" in others

    def test_incoming_other_slug(self, tmp_path):
        result = self._run("ned-stark", EDGES_FIXTURE, tmp_path)
        others = {r["other_slug"] for r in result["incoming"]}
        assert "jon-snow" in others
        assert "cersei-lannister" in others

    def test_no_edges_node(self, tmp_path):
        result = self._run("ghost", EDGES_FIXTURE, tmp_path)
        assert result["outgoing_count"] == 0
        assert result["incoming_count"] == 0

    def test_slug_field_correct(self, tmp_path):
        result = self._run("arya-stark", EDGES_FIXTURE, tmp_path)
        assert result["slug"] == "arya-stark"


# ---------------------------------------------------------------------------
# --path tests
# ---------------------------------------------------------------------------

class TestPath:
    """Tests for cmd_path via JSON output."""

    def _run(self, slug_a: str, slug_b: str, edges: list[dict], tmp_path: Path) -> dict:
        import io
        from contextlib import redirect_stdout

        edges_file = _write_edges(tmp_path, edges)
        loaded = gq.load_edges(edges_file)
        buf = io.StringIO()
        with redirect_stdout(buf):
            gq.cmd_path(slug_a, slug_b, loaded, json_output=True)
        return json.loads(buf.getvalue())

    def test_direct_edge_count(self, tmp_path):
        # arya LOVES jon directly
        result = self._run("arya-stark", "jon-snow", EDGES_FIXTURE, tmp_path)
        assert len(result["direct_edges"]) == 1
        assert result["direct_edges"][0]["edge_type"] == "LOVES"

    def test_direct_edge_direction_reversed(self, tmp_path):
        # Same query reversed — should still find it
        result = self._run("jon-snow", "arya-stark", EDGES_FIXTURE, tmp_path)
        assert len(result["direct_edges"]) == 1

    def test_no_direct_edge(self, tmp_path):
        # arya <-> ned-stark: no direct edge in fixture
        result = self._run("arya-stark", "ned-stark", EDGES_FIXTURE, tmp_path)
        assert len(result["direct_edges"]) == 0

    def test_two_hop_bridges_detected(self, tmp_path):
        # arya→[LOVES]→jon→[SERVES]→ned  (bridge: jon-snow)
        # arya→[FEARS]→cersei→[HATES]→ned  (bridge: cersei-lannister)
        result = self._run("arya-stark", "ned-stark", EDGES_FIXTURE, tmp_path)
        assert result["total_bridges"] == 2
        bridge_names = {b["bridge"] for b in result["bridges"]}
        assert "jon-snow" in bridge_names
        assert "cersei-lannister" in bridge_names

    def test_bridge_edge_types_populated(self, tmp_path):
        result = self._run("arya-stark", "ned-stark", EDGES_FIXTURE, tmp_path)
        # Find the jon-snow bridge
        jon_bridge = next(b for b in result["bridges"] if b["bridge"] == "jon-snow")
        # arya–[LOVES]→jon side
        assert "LOVES" in jon_bridge["a_types"]
        # jon–[SERVES]→ned side
        assert "SERVES" in jon_bridge["b_types"]

    def test_no_bridges(self, tmp_path):
        # Two disconnected nodes
        result = self._run("ghost", "robb-stark", EDGES_FIXTURE, tmp_path)
        assert result["total_bridges"] == 0
        assert len(result["direct_edges"]) == 0

    def test_slug_fields_correct(self, tmp_path):
        result = self._run("arya-stark", "ned-stark", EDGES_FIXTURE, tmp_path)
        assert result["slug_a"] == "arya-stark"
        assert result["slug_b"] == "ned-stark"

    def test_direct_edge_evidence_ref_present(self, tmp_path):
        result = self._run("arya-stark", "jon-snow", EDGES_FIXTURE, tmp_path)
        ref = result["direct_edges"][0]["evidence_ref"]
        assert "agot-arya-01" in ref


# ---------------------------------------------------------------------------
# --health tests
# ---------------------------------------------------------------------------

class TestHealth:
    """Tests for cmd_health via JSON output."""

    def _run(
        self,
        edges: list[dict],
        tmp_path: Path,
        extra_nodes: list[str] | None = None,
    ) -> dict:
        """Write edges + optionally create node files, then call cmd_health."""
        import io
        from contextlib import redirect_stdout

        edges_file = _write_edges(tmp_path, edges)
        loaded = gq.load_edges(edges_file)

        # Create a fake nodes directory
        nodes_dir = tmp_path / "nodes" / "characters"
        nodes_dir.mkdir(parents=True, exist_ok=True)

        # Default: create node files for all slugs in EDGES_FIXTURE
        node_slugs = extra_nodes if extra_nodes is not None else [
            "arya-stark", "jon-snow", "cersei-lannister", "ned-stark"
        ]
        for slug in node_slugs:
            (nodes_dir / f"{slug}.node.md").write_text(
                f"---\nname: {slug}\ntype: character\nslug: {slug}\n---\n",
                encoding="utf-8",
            )

        buf = io.StringIO()
        with redirect_stdout(buf):
            gq.cmd_health(loaded, tmp_path / "nodes", json_output=True)
        return json.loads(buf.getvalue())

    def test_edge_count(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        assert result["edge_count"] == 4

    def test_node_count(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        assert result["node_count"] == 4

    def test_edge_type_distribution_keys(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        type_map = dict(result["edge_type_distribution"])
        assert type_map["LOVES"] == 1
        assert type_map["FEARS"] == 1
        assert type_map["SERVES"] == 1
        assert type_map["HATES"] == 1

    def test_unique_endpoints(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        # arya-stark, jon-snow, cersei-lannister, ned-stark
        assert result["unique_endpoints"] == 4

    def test_zero_orphans_when_all_nodes_exist(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        assert result["orphan_endpoint_count"] == 0
        assert result["orphan_endpoints"] == []

    def test_orphan_detected_when_node_missing(self, tmp_path):
        # Create node files for only 3 of 4 slugs — ned-stark has no node file
        result = self._run(
            EDGES_FIXTURE,
            tmp_path,
            extra_nodes=["arya-stark", "jon-snow", "cersei-lannister"],
        )
        assert result["orphan_endpoint_count"] == 1
        assert "ned-stark" in result["orphan_endpoints"]

    def test_multiple_orphans(self, tmp_path):
        result = self._run(
            EDGES_FIXTURE,
            tmp_path,
            extra_nodes=["arya-stark"],  # only arya has a node file
        )
        assert result["orphan_endpoint_count"] == 3
        orphan_set = set(result["orphan_endpoints"])
        assert "jon-snow" in orphan_set
        assert "cersei-lannister" in orphan_set
        assert "ned-stark" in orphan_set

    def test_degree_leaders_present(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        # ned-stark appears as target twice (jon SERVES ned, cersei HATES ned)
        # arya-stark appears as source twice
        leaders = {entry["slug"]: entry["degree"] for entry in result["degree_leaders"]}
        assert leaders["ned-stark"] == 2
        assert leaders["arya-stark"] == 2

    def test_degree_leader_ordering(self, tmp_path):
        result = self._run(EDGES_FIXTURE, tmp_path)
        # Highest degree should come first
        degrees = [entry["degree"] for entry in result["degree_leaders"]]
        assert degrees == sorted(degrees, reverse=True)

    def test_empty_edges(self, tmp_path):
        result = self._run([], tmp_path, extra_nodes=["arya-stark"])
        assert result["edge_count"] == 0
        assert result["unique_endpoints"] == 0
        assert result["orphan_endpoint_count"] == 0


# ---------------------------------------------------------------------------
# --causal-chain tests
# ---------------------------------------------------------------------------

# A linear causal chain with one downstream branch at the focal node `d`, plus
# a non-causal edge (PRECEDES) that must be ignored:
#
#   a --[TRIGGERS]--> b --[CAUSES]--> c --[CAUSES]--> d --[CAUSES]--> e
#                                                     d --[MOTIVATES]--> x
#   a --[PRECEDES]--> e    (chronology only — must NOT appear)
CAUSAL_FIXTURE = [
    {"edge_type": "TRIGGERS", "source_slug": "a", "target_slug": "b",
     "confidence_tier": 2, "evidence_ref": "x.md:1", "evidence_quote": "spark"},
    {"edge_type": "CAUSES", "source_slug": "b", "target_slug": "c",
     "confidence_tier": 2, "evidence_ref": "x.md:2", "evidence_quote": ""},
    {"edge_type": "CAUSES", "source_slug": "c", "target_slug": "d",
     "confidence_tier": 2, "evidence_ref": "x.md:3", "evidence_quote": ""},
    {"edge_type": "CAUSES", "source_slug": "d", "target_slug": "e",
     "confidence_tier": 2, "evidence_ref": "x.md:4", "evidence_quote": ""},
    {"edge_type": "MOTIVATES", "source_slug": "d", "target_slug": "x",
     "confidence_tier": 2, "evidence_ref": "x.md:5", "evidence_quote": ""},
    {"edge_type": "PRECEDES", "source_slug": "a", "target_slug": "e",
     "confidence_tier": 3, "evidence_ref": "x.md:6", "evidence_quote": ""},
]


class TestCausalChain:
    """Tests for cmd_causal_chain via JSON output."""

    def _run(self, slug: str, edges: list[dict], tmp_path: Path) -> dict:
        import io
        from contextlib import redirect_stdout

        edges_file = _write_edges(tmp_path, edges)
        loaded = gq.load_edges(edges_file)
        buf = io.StringIO()
        with redirect_stdout(buf):
            gq.cmd_causal_chain(slug, loaded, json_output=True)
        return json.loads(buf.getvalue())

    def test_full_chain_from_middle(self, tmp_path):
        # From focal node `d`: 3 upstream (a→b, b→c, c→d) + 2 downstream (d→e, d→x)
        result = self._run("d", CAUSAL_FIXTURE, tmp_path)
        assert result["upstream_count"] == 3
        assert result["downstream_count"] == 2

    def test_all_downstream_from_root(self, tmp_path):
        # From the root `a`: 0 upstream, 5 downstream (whole arc minus PRECEDES)
        result = self._run("a", CAUSAL_FIXTURE, tmp_path)
        assert result["upstream_count"] == 0
        assert result["downstream_count"] == 5

    def test_all_upstream_from_leaf(self, tmp_path):
        # From leaf `e`: 4 upstream (a→b, b→c, c→d, d→e), 0 downstream
        result = self._run("e", CAUSAL_FIXTURE, tmp_path)
        assert result["upstream_count"] == 4
        assert result["downstream_count"] == 0

    def test_precedes_excluded(self, tmp_path):
        # PRECEDES (a→e) is chronology, not causation — must not appear anywhere.
        result = self._run("a", CAUSAL_FIXTURE, tmp_path)
        types = {edge["edge_type"] for edge in result["downstream"]}
        assert "PRECEDES" not in types
        # e is reached only via the CAUSES chain, not the direct PRECEDES edge
        assert all(edge["edge_type"] in {"CAUSES", "TRIGGERS", "MOTIVATES"}
                   for edge in result["downstream"])

    def test_motivates_branch_captured(self, tmp_path):
        result = self._run("d", CAUSAL_FIXTURE, tmp_path)
        down = {(e["source_slug"], e["edge_type"], e["target_slug"])
                for e in result["downstream"]}
        assert ("d", "CAUSES", "e") in down
        assert ("d", "MOTIVATES", "x") in down

    def test_depth_assigned(self, tmp_path):
        # Downstream depths from root: b=1, c=2, d=3, e=4, x=4
        result = self._run("a", CAUSAL_FIXTURE, tmp_path)
        depth_by_target = {e["target_slug"]: e["depth"] for e in result["downstream"]}
        assert depth_by_target["b"] == 1
        assert depth_by_target["e"] == 4
        assert depth_by_target["x"] == 4

    def test_isolated_node(self, tmp_path):
        result = self._run("ghost", CAUSAL_FIXTURE, tmp_path)
        assert result["upstream_count"] == 0
        assert result["downstream_count"] == 0

    def test_cycle_safe(self, tmp_path):
        # A→B→A cycle must terminate and emit each edge once.
        cyclic = [
            {"edge_type": "CAUSES", "source_slug": "p", "target_slug": "q",
             "confidence_tier": 2, "evidence_ref": "x.md:1", "evidence_quote": ""},
            {"edge_type": "CAUSES", "source_slug": "q", "target_slug": "p",
             "confidence_tier": 2, "evidence_ref": "x.md:2", "evidence_quote": ""},
        ]
        result = self._run("p", cyclic, tmp_path)
        assert result["downstream_count"] == 2

    def test_node_lists(self, tmp_path):
        result = self._run("d", CAUSAL_FIXTURE, tmp_path)
        assert set(result["upstream_nodes"]) == {"a", "b", "c"}
        assert set(result["downstream_nodes"]) == {"e", "x"}

    def test_text_mode_renders(self, tmp_path):
        # Text mode calls _node_header (node-file lookup); should not crash even
        # when the node file is absent.
        import io
        from contextlib import redirect_stdout

        edges_file = _write_edges(tmp_path, CAUSAL_FIXTURE)
        loaded = gq.load_edges(edges_file)
        buf = io.StringIO()
        with redirect_stdout(buf):
            gq.cmd_causal_chain("d", loaded, json_output=False)
        out = buf.getvalue()
        assert "CAUSAL CHAIN: d" in out
        assert "UPSTREAM" in out
        assert "DOWNSTREAM" in out


# ---------------------------------------------------------------------------
# load_edges error handling
# ---------------------------------------------------------------------------

class TestLoadEdges:
    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="edges.jsonl not found"):
            gq.load_edges(tmp_path / "nonexistent.jsonl")

    def test_loads_valid_jsonl(self, tmp_path):
        edges_file = _write_edges(tmp_path, EDGES_FIXTURE)
        loaded = gq.load_edges(edges_file)
        assert len(loaded) == 4

    def test_skips_blank_lines(self, tmp_path):
        p = tmp_path / "edges.jsonl"
        p.write_text(
            json.dumps(EDGES_FIXTURE[0]) + "\n\n" + json.dumps(EDGES_FIXTURE[1]) + "\n",
            encoding="utf-8",
        )
        loaded = gq.load_edges(p)
        assert len(loaded) == 2
