"""Tests for the S121 mint helpers: scripts/mint_arc_lib.py + scripts/stamp_containers.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import load_script

mal = load_script("mint_arc_lib.py")
sc = load_script("stamp_containers.py")


# --- mint_arc_lib.precheck_slugs / resolve_slug -----------------------------

def test_resolve_real_node():
    ok, canon = mal.resolve_slug("death-of-khal-drogo")
    assert ok is True
    assert canon == "death-of-khal-drogo"


def test_resolve_fake_slug():
    ok, canon = mal.resolve_slug("definitely-not-a-real-slug-xyz-123")
    assert ok is False
    assert canon is None


def test_precheck_partitions():
    resolved, missing = mal.precheck_slugs(
        ["death-of-khal-drogo", "definitely-not-a-real-slug-xyz-123"]
    )
    assert "death-of-khal-drogo" in resolved
    assert "definitely-not-a-real-slug-xyz-123" in missing


def test_normalize_keeps_hyphens_lowercases():
    assert mal._normalize("  Death  of  Khal Drogo ") == "death of khal drogo"
    assert mal._normalize("Daznak-s-Pit") == "daznak-s-pit"


# --- stamp_containers.parse_containers --------------------------------------

def test_parse_containers_inline():
    assert sc.parse_containers("containers: [essos, wo5k]") == ["essos", "wo5k"]


def test_parse_containers_single():
    assert sc.parse_containers("containers: [essos]") == ["essos"]


def test_parse_containers_null_and_empty():
    assert sc.parse_containers("containers: null") == []
    assert sc.parse_containers("containers: []") == []


# --- stamp_containers.stamp (idempotent, on a tmp node file) ----------------

FRONTMATTER = """---
name: "Test Node"
type: event.incident
slug: test-node
confidence: tier-1
---

## Identity
body
"""


def test_stamp_inserts_then_merges_then_noops(tmp_path):
    node = tmp_path / "test-node.node.md"
    node.write_text(FRONTMATTER, encoding="utf-8")

    status, vals = sc.stamp(node, "essos")
    assert status == "inserted"
    assert vals == ["essos"]
    assert "containers: [essos]" in node.read_text()

    status, vals = sc.stamp(node, "wo5k")
    assert status == "merged"
    assert vals == ["essos", "wo5k"]
    assert "containers: [essos, wo5k]" in node.read_text()

    status, vals = sc.stamp(node, "essos")
    assert status == "already"
    # never duplicates
    assert node.read_text().count("essos") == 1
