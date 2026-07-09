#!/usr/bin/env python3
"""Build-time unit tests for scripts/fab-semantic-gate.py.

Deterministic, no LLM, no network, no dependency on live graph state — every check
function is exercised against small synthetic fixtures (node_index / edges dicts
built by hand), per the fixture list in the build task:
  - VICTIM_IN -> event.coronation FAILs check 1 (book-fab provenance)
  - VICTIM_IN -> event.death PASSes check 1
  - a character.human named "the mob" (F&B-provenance) FAILs check 2
  - a normal character.human name PASSes check 2
  - an edge to a nonexistent slug is counted / FAILs check 3
Plus one bonus fixture for check 4 (duplicate edges), for full 4-check coverage.

Run:  python3 scripts/test-fab-semantic-gate.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("fab_semantic_gate_test_import", "scripts/fab-semantic-gate.py")
RECONCILER = G.load_reconciler()
MINT = G.load_mint()

PASS, FAIL = 0, 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {label}")
    else:
        FAIL += 1
        print(f"  FAIL {label}  {detail}")


def make_event_node(slug: str, subtype: str) -> dict:
    return {"type": f"event.{subtype}", "name": slug, "dir": "events",
            "path": None, "fab_provenance": False}


def make_character_node(name: str, fab_provenance: bool = False) -> dict:
    return {"type": "character.human", "name": name, "dir": "characters",
            "path": None, "fab_provenance": fab_provenance}


def make_edge(edge_type: str, source: str, target: str, evidence_kind: str = "book-fab",
             quote: str = "some quote", line: int = 1, run_id: str | None = None) -> dict:
    return {"edge_type": edge_type, "source_slug": source, "target_slug": target,
            "evidence_kind": evidence_kind, "evidence_quote": quote, "_line": line,
            "run_id": run_id}


def test_check1_victim_in_harm_gate():
    print("\n-- check 1: VICTIM_IN harm-gate --")
    node_index = {
        "some-coronation": make_event_node("some-coronation", "coronation"),
        "some-death": make_event_node("some-death", "death"),
    }
    edges = [
        make_edge("VICTIM_IN", "aegon-i-targaryen", "some-coronation", evidence_kind="book-fab", line=1),
        make_edge("VICTIM_IN", "some-victim", "some-death", evidence_kind="book-fab", line=2),
    ]
    result = G.check_victim_in_harm_gate(edges, node_index, RECONCILER.classify_patient_edge_type)
    check("VICTIM_IN -> event.coronation (book-fab) FAILs check 1",
          result["status"] == "FAIL" and result["fail_count"] == 1, result)
    offending_targets = {o["target"] for o in result["offenders"]}
    check("the coronation edge is the one flagged, not the death edge",
          offending_targets == {"some-coronation"}, offending_targets)


def test_check1_death_passes():
    print("\n-- check 1: VICTIM_IN -> event.death passes clean --")
    node_index = {"some-death": make_event_node("some-death", "death")}
    edges = [make_edge("VICTIM_IN", "some-victim", "some-death", evidence_kind="book-fab", line=1)]
    result = G.check_victim_in_harm_gate(edges, node_index, RECONCILER.classify_patient_edge_type)
    check("VICTIM_IN -> event.death PASSes check 1",
          result["status"] == "PASS" and result["fail_count"] == 0, result)


def test_check1_nonfab_offender_is_informational_only():
    print("\n-- check 1: non-F&B offender stays informational, does not FAIL the gate --")
    node_index = {"some-coronation": make_event_node("some-coronation", "coronation")}
    edges = [make_edge("VICTIM_IN", "someone", "some-coronation", evidence_kind="book-pass1", line=1)]
    result = G.check_victim_in_harm_gate(edges, node_index, RECONCILER.classify_patient_edge_type)
    check("non-F&B VICTIM_IN-on-non-harm does NOT fail the gate",
          result["status"] == "PASS" and result["fail_count"] == 0, result)
    check("...but IS counted informationally",
          result["informational_nonfab_count"] == 1, result)


def test_check1_pass1_reified_offender_is_informational_not_fail():
    print("\n-- check 1: book-pass1-reified VICTIM_IN-on-non-harm is informational, NEVER a FAIL --")
    # The real AGOT narrative-arc reification example the coordinator flagged: a
    # pre-existing, non-F&B VICTIM_IN edge onto a non-harm event subtype (an
    # `event.incident`, run_id None). This must never contribute to fail_count,
    # regardless of how many such pre-existing edges exist.
    node_index = {"six-wildling-deserters-ambush-bran": make_event_node(
        "six-wildling-deserters-ambush-bran", "incident")}
    edges = [make_edge("VICTIM_IN", "bran-stark", "six-wildling-deserters-ambush-bran",
                       evidence_kind="book-pass1-reified", run_id=None, line=1)]
    result = G.check_victim_in_harm_gate(edges, node_index, RECONCILER.classify_patient_edge_type)
    check("book-pass1-reified VICTIM_IN-on-non-harm does NOT fail check 1",
          result["status"] == "PASS" and result["fail_count"] == 0, result)
    check("...and is counted informationally instead",
          result["informational_nonfab_count"] == 1, result)
    check("is_fab_provenance_edge() is False for evidence_kind=book-pass1-reified, run_id=None",
          not G.is_fab_provenance_edge(edges[0]), edges[0])


def test_is_fab_provenance_edge_run_id_fallback():
    print("\n-- is_fab_provenance_edge(): evidence_kind and run_id-prefix fallback --")
    check("evidence_kind=book-fab is fab-provenance",
          G.is_fab_provenance_edge({"evidence_kind": "book-fab", "run_id": None}))
    check("run_id starting 'fab-' is fab-provenance even with a different evidence_kind",
          G.is_fab_provenance_edge({"evidence_kind": "book-pass1", "run_id": "fab-some-unit-2026-07-09"}))
    check("book-pass1-reified with run_id=None is NOT fab-provenance",
          not G.is_fab_provenance_edge({"evidence_kind": "book-pass1-reified", "run_id": None}))
    check("book-pass1 with a non-fab run_id is NOT fab-provenance",
          not G.is_fab_provenance_edge({"evidence_kind": "book-pass1", "run_id": "pass1-derived-20260523"}))


def test_check2_junk_character_fails():
    print("\n-- check 2: junk character.human --")
    node_index = {"the-mob": make_character_node("the mob", fab_provenance=True)}
    result = G.check_junk_characters(node_index, RECONCILER.junk_character_screen)
    check('character.human named "the mob" (F&B-provenance) FAILs check 2',
          result["status"] == "FAIL" and result["fail_count"] == 1, result)
    check("the offender is the-mob", result["offenders"][0]["slug"] == "the-mob", result)


def test_check2_normal_person_passes():
    print("\n-- check 2: a normal person passes --")
    node_index = {"jon-snow": make_character_node("Jon Snow", fab_provenance=True)}
    result = G.check_junk_characters(node_index, RECONCILER.junk_character_screen)
    check("a normal character.human name PASSes check 2",
          result["status"] == "PASS" and result["fail_count"] == 0, result)


def test_check2_nonfab_junk_is_informational_only():
    print("\n-- check 2: pre-existing (non-F&B) junk-flagged node does not fail the gate --")
    node_index = {"the-mob": make_character_node("the mob", fab_provenance=False)}
    result = G.check_junk_characters(node_index, RECONCILER.junk_character_screen)
    check("non-F&B junk-screen hit does NOT fail the gate",
          result["status"] == "PASS" and result["fail_count"] == 0, result)
    check("...but IS counted informationally",
          result["informational_stripped_count"] == 1, result)


def test_check2_disambiguator_suffix_is_not_junk():
    print("\n-- check 2: '(son of X)' disambiguator suffix is not treated as junk --")
    node_index = {
        "aerion-targaryen-son-of-daemion": make_character_node(
            "Aerion Targaryen (son of Daemion)", fab_provenance=True),
    }
    result = G.check_junk_characters(node_index, RECONCILER.junk_character_screen)
    check("a real disambiguated person name PASSes (disambiguator-suffix stripped before screening)",
          result["status"] == "PASS" and result["fail_count"] == 0, result)


def test_check3_orphan_edge_counted():
    print("\n-- check 3: orphan edges --")
    node_index = {"jon-snow": make_character_node("Jon Snow")}
    alias_index: dict[str, str] = {}
    edges = [make_edge("KILLS", "jon-snow", "nonexistent-slug-xyz", line=1)]
    result = G.check_orphan_edges(edges, node_index, alias_index, baseline_orphans=None)
    check("edge to a nonexistent slug is counted in check 3",
          result["missing_count"] == 1, result)
    check("default (no --baseline-orphans) is informational-only, PASS",
          result["status"] == "PASS", result)

    result_gated = G.check_orphan_edges(edges, node_index, alias_index, baseline_orphans=0)
    check("with --baseline-orphans 0, the same missing edge FAILs the gate",
          result_gated["status"] == "FAIL", result_gated)


def test_check3_alias_resolves_is_not_orphan():
    print("\n-- check 3: alias-resolvable endpoint is not an orphan --")
    node_index = {"brienne-tarth": make_character_node("Brienne of Tarth")}
    alias_index = {"brienne-of-tarth": "brienne-tarth"}
    edges = [make_edge("KILLS", "brienne-of-tarth", "brienne-tarth", line=1)]
    result = G.check_orphan_edges(edges, node_index, alias_index, baseline_orphans=None)
    check("alias-resolvable source does not count as missing",
          result["missing_count"] == 0, result)
    check("...but is tracked as alias-resolvable",
          result["alias_resolvable_count"] == 1, result)


def test_check3_baseline_not_exceeded_passes():
    print("\n-- check 3: baseline gating only fails when count EXCEEDS baseline --")
    node_index: dict = {}
    alias_index: dict = {}
    edges = [make_edge("KILLS", "a", "b", line=1)]  # both endpoints missing = 2
    result = G.check_orphan_edges(edges, node_index, alias_index, baseline_orphans=2)
    check("count == baseline PASSes (not an increase)", result["status"] == "PASS", result)
    result2 = G.check_orphan_edges(edges, node_index, alias_index, baseline_orphans=1)
    check("count > baseline FAILs", result2["status"] == "FAIL", result2)


def test_check4_duplicate_fab_edge_fails():
    print("\n-- check 4: duplicate edges (bonus coverage) --")
    edges = [
        make_edge("KILLS", "a", "b", evidence_kind="book-fab", quote="he slew him", line=1,
                  run_id="fab-unit-1"),
        make_edge("KILLS", "a", "b", evidence_kind="book-fab", quote="he slew him", line=2,
                  run_id="fab-unit-1"),
    ]
    result = G.check_duplicate_edges(edges, MINT.edge_dedup_key)
    check("two identical (type, src, dst, quote) book-fab edges FAIL check 4",
          result["status"] == "FAIL" and result["fail_count"] == 1, result)


def test_check4_pass1_duplicate_is_informational_not_fail():
    print("\n-- check 4: a pre-existing book-pass1 duplicate group stays informational --")
    edges = [
        make_edge("KILLS", "janos-slynt", "varly", evidence_kind="book-pass1",
                  quote="janos slynt himself slashed open varly's throat", line=1,
                  run_id="pass1-derived-20260523"),
        make_edge("KILLS", "janos-slynt", "varly", evidence_kind="book-pass1",
                  quote="janos slynt himself slashed open varly's throat", line=2,
                  run_id="neds-downfall-enrichment-s137"),
    ]
    result = G.check_duplicate_edges(edges, MINT.edge_dedup_key)
    check("a book-pass1 duplicate group does NOT fail check 4",
          result["status"] == "PASS" and result["fail_count"] == 0, result)
    check("...but is counted informationally",
          result["informational_count"] == 1, result)


def test_check4_distinct_quotes_not_duplicate():
    print("\n-- check 4: same triple, different quote is multi-provenance, not a dup --")
    edges = [
        make_edge("KILLS", "a", "b", evidence_kind="book-fab", quote="he slew him", line=1),
        make_edge("KILLS", "a", "b", evidence_kind="book-fab", quote="a different sentence entirely", line=2),
    ]
    result = G.check_duplicate_edges(edges, MINT.edge_dedup_key)
    check("distinct quotes on the same triple do not FAIL check 4",
          result["status"] == "PASS" and result["fail_count"] == 0, result)


def test_run_checks_end_to_end():
    print("\n-- run_checks(): all four checks wired together --")
    node_index = {
        "some-coronation": make_event_node("some-coronation", "coronation"),
        "the-mob": make_character_node("the mob", fab_provenance=True),
    }
    alias_index: dict = {}
    edges = [
        make_edge("VICTIM_IN", "aegon-i-targaryen", "some-coronation", evidence_kind="book-fab", line=1),
        make_edge("KILLS", "someone", "nonexistent-slug", evidence_kind="book-fab", line=2),
    ]
    results = G.run_checks(edges, node_index, alias_index,
                           RECONCILER.classify_patient_edge_type,
                           RECONCILER.junk_character_screen,
                           MINT.edge_dedup_key,
                           baseline_orphans=None)
    check("run_checks returns exactly 4 check results", len(results) == 4, results)
    by_name = {r["name"]: r for r in results}
    check("victim_in_harm_gate FAILs", by_name["victim_in_harm_gate"]["status"] == "FAIL")
    check("junk_character_nodes FAILs", by_name["junk_character_nodes"]["status"] == "FAIL")
    overall = G.to_json(results)["overall"]
    check("overall verdict is FAIL when any check fails", overall == "FAIL", overall)


def main() -> int:
    test_check1_victim_in_harm_gate()
    test_check1_death_passes()
    test_check1_nonfab_offender_is_informational_only()
    test_check1_pass1_reified_offender_is_informational_not_fail()
    test_is_fab_provenance_edge_run_id_fallback()
    test_check2_junk_character_fails()
    test_check2_normal_person_passes()
    test_check2_nonfab_junk_is_informational_only()
    test_check2_disambiguator_suffix_is_not_junk()
    test_check3_orphan_edge_counted()
    test_check3_alias_resolves_is_not_orphan()
    test_check3_baseline_not_exceeded_passes()
    test_check4_duplicate_fab_edge_fails()
    test_check4_pass1_duplicate_is_informational_not_fail()
    test_check4_distinct_quotes_not_duplicate()
    test_run_checks_end_to_end()

    print(f"\n{PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
