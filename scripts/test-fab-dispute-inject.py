#!/usr/bin/env python3
"""Build-time unit tests for scripts/fab-dispute-inject.py.

Deterministic, no LLM, no network. Builds a small fixture unit dir (matched.jsonl,
dispute-preclass.jsonl, candidates.json, merge-plan.json) under a tempdir and exercises
process_unit() end-to-end, then re-runs it to prove idempotency. The one deliberately
"real-data" case (an AUTO_CLEAR edge whose source name is NOT in the fixture matched.jsonl)
exercises the resolver-fallback path against the real graph/query alias tables — it uses
"Jaehaerys I Targaryen", a real character-node name stable across the corpus.

Run:  python3 scripts/test-fab-dispute-inject.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fab_dispute_inject", REPO / "scripts" / "fab-dispute-inject.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load_module()

PASS, FAIL = 0, 0


def check(label, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {label}")
    else:
        FAIL += 1
        print(f"  FAIL {label}  {detail}")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


UNIT = "fab-test-01"


def build_fixture(root: Path) -> Path:
    unit_dir = root / UNIT
    unit_dir.mkdir(parents=True)

    matched = [
        {"unit": UNIT, "name": "Alric Testman", "slug": "alric-testman", "route_reason": "hit-character"},
        {"unit": UNIT, "name": "Betha Testwoman", "slug": "betha-testwoman", "route_reason": "hit-character"},
        {"unit": UNIT, "name": "Cregar Disputeson", "slug": "cregar-disputeson", "route_reason": "hit-character"},
        {"unit": UNIT, "name": "Dara Disputedaughter", "slug": "dara-disputedaughter", "route_reason": "hit-character"},
        {"unit": UNIT, "name": "Elyn Proseworthy", "slug": "elyn-proseworthy", "route_reason": "hit-character"},
    ]
    write_jsonl(unit_dir / "matched.jsonl", matched)

    preclass_rows = [
        # 1. AUTO_CLEAR edge -> should inject as tier-1, no disputed flag.
        {"unit": UNIT, "kind": "edge", "edge_type": "PARENT_OF",
         "source": "Alric Testman", "target": "Betha Testwoman",
         "quote": "Alric Testman was the father of Betha Testwoman", "line": 10,
         "hedge_term": "mushroom", "hedge_distance": 1,
         "preclass_bucket": "AUTO_CLEAR", "preclass_tier": 1,
         "preclass_in_universe_source": None,
         "preclass_reason": "genealogical/definitional edge_type=PARENT_OF; no hedge verb in quote"},
        # 2. AUTO_DISPUTED edge -> should inject as tier-2 + disputed + in_universe_source.
        {"unit": UNIT, "kind": "edge", "edge_type": "LOVER_OF",
         "source": "Cregar Disputeson", "target": "Dara Disputedaughter",
         "quote": "it is said Cregar took Dara as his paramour", "line": 20,
         "hedge_term": "romance-class-untagged", "hedge_distance": 0,
         "preclass_bucket": "AUTO_DISPUTED", "preclass_tier": 2,
         "preclass_in_universe_source": "mushroom",
         "preclass_reason": "romance-class hedge/euphemism cue in quote: 'it is said'"},
        # 3. AUTO_CLEAR prose -> should append a bullet to merge-plan.json.
        {"unit": UNIT, "kind": "prose", "entity": "Elyn Proseworthy", "slug": "elyn-proseworthy",
         "text": "A minor lord of no particular note", "line": 30,
         "hedge_term": "eustace", "hedge_distance": 1,
         "preclass_bucket": "AUTO_CLEAR", "preclass_tier": 1,
         "preclass_in_universe_source": None,
         "preclass_reason": "prose kind: flat node-description text, no hedge/attribution cue"},
        # 4. AUTO_CLEAR edge with an UNRESOLVABLE source name -> leftover.
        {"unit": UNIT, "kind": "edge", "edge_type": "ALLIES_WITH",
         "source": "Qwyxzflarn Nobodyson", "target": "Betha Testwoman",
         "quote": "Qwyxzflarn allied with Betha", "line": 40,
         "hedge_term": "mushroom", "hedge_distance": 1,
         "preclass_bucket": "AUTO_CLEAR", "preclass_tier": 1,
         "preclass_in_universe_source": None,
         "preclass_reason": "genealogical/definitional edge_type=ALLIES_WITH; no hedge verb in quote"},
        # 5. event kind -> ALWAYS deferred, regardless of bucket.
        {"unit": UNIT, "kind": "event", "name": "Test Battle of Nowhere",
         "quote": "a battle happened near the fixture", "line": 50,
         "hedge_term": "avers", "hedge_distance": 1,
         "preclass_bucket": "AUTO_CLEAR", "preclass_tier": 1,
         "preclass_in_universe_source": None,
         "preclass_reason": "event kind: flat name+quote, no secret/alleged/rumored/hedge cue"},
        # 6. AUTO_CLEAR edge whose source is NOT in matched.jsonl -> resolver-fallback path.
        {"unit": UNIT, "kind": "edge", "edge_type": "ALLIES_WITH",
         "source": "Jaehaerys I Targaryen", "target": "Betha Testwoman",
         "quote": "Jaehaerys I Targaryen allied with Betha Testwoman", "line": 60,
         "hedge_term": "mushroom", "hedge_distance": 1,
         "preclass_bucket": "AUTO_CLEAR", "preclass_tier": 1,
         "preclass_in_universe_source": None,
         "preclass_reason": "genealogical/definitional edge_type=ALLIES_WITH; no hedge verb in quote"},
        # 7. NEEDS_READ edge, no verdict -> should be SKIPPED entirely (not injected,
        #    not leftover, not deferred).
        {"unit": UNIT, "kind": "edge", "edge_type": "IMPRISONS",
         "source": "Alric Testman", "target": "Cregar Disputeson",
         "quote": "amongst others taken captive that day", "line": 70,
         "hedge_term": "eustace", "hedge_distance": 1,
         "preclass_bucket": "NEEDS_READ", "preclass_tier": None,
         "preclass_in_universe_source": None,
         "preclass_reason": "not genealogical/romance and quote has no explicit hedge verb"},
    ]
    write_jsonl(unit_dir / "dispute-preclass.jsonl", preclass_rows)

    candidates = {
        "_meta": {"unit": UNIT, "session": "fab-reconcile", "run_id": f"{UNIT}-2026-07-09",
                  "evidence_kind": "book-fab", "new_node_slugs": [],
                  "note": "fixture", "produced_at": "2026-07-09T00:00:00+00:00"},
        "edges": [
            {"id": "E1", "type": "SPOUSE_OF", "source": "alric-testman", "target": "betha-testwoman",
             "book": "fab", "chapter": UNIT, "quote": "a pre-existing organic edge",
             "tier": "tier-1", "note": "Fire & Blood: Alric Testman SPOUSE_OF Betha Testwoman"},
        ],
    }
    (unit_dir / "candidates.json").write_text(json.dumps(candidates, indent=2) + "\n", encoding="utf-8")
    (unit_dir / "merge-plan.json").write_text("[]\n", encoding="utf-8")

    return unit_dir


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        apply_dir = root / "apply"
        nodes_root = root / "nodes"
        nodes_root.mkdir(parents=True)
        unit_dir = build_fixture(apply_dir)

        # ---------------------------------------------------------------
        # Run 1 — the real injection.
        # ---------------------------------------------------------------
        report1 = D.process_unit(UNIT, apply_dir, nodes_root, verdict_index={}, dry_run=False)
        s1 = report1["stats"]

        check("run1: 3 edges injected (AUTO_CLEAR PARENT_OF, AUTO_DISPUTED LOVER_OF, "
              "AUTO_CLEAR resolver-fallback ALLIES_WITH)", s1.get("edges_injected") == 3, s1)
        check("run1: 1 bullet injected", s1.get("bullets_injected") == 1, s1)
        check("run1: 1 leftover edge (unresolvable source name)", report1["leftover_count"] == 1, report1)
        check("run1: 1 event deferred", report1["deferred_count"] == 1, report1)
        check("run1: 1 NEEDS_READ row skipped (awaiting adjudication, no verdict)",
              report1["skipped_awaiting_count"] == 1, report1)
        check("run1: 0 dropped", report1["dropped_count"] == 0, report1)

        candidates_out = json.loads((unit_dir / "candidates.json").read_text(encoding="utf-8"))
        edges_out = candidates_out["edges"]
        check("candidates.json: original E1 edge still present untouched",
              any(e["id"] == "E1" for e in edges_out), edges_out)
        check("candidates.json: 4 total edges after injection (1 original + 3 injected)",
              len(edges_out) == 4, edges_out)

        injected_ids = [e["id"] for e in edges_out if e["id"] != "E1"]
        check("injected edge ids use the DISP<n> scheme, distinct from E1",
              all(i.startswith("DISP") for i in injected_ids), injected_ids)
        check("injected edge ids are unique (no collision)",
              len(set(injected_ids)) == len(injected_ids), injected_ids)

        clear_edge = next(e for e in edges_out if e["type"] == "PARENT_OF")
        check("AUTO_CLEAR edge injected as tier-1", clear_edge["tier"] == "tier-1", clear_edge)
        check("AUTO_CLEAR edge has no disputed flag", not clear_edge.get("disputed"), clear_edge)
        check("AUTO_CLEAR edge source/target resolved via matched.jsonl",
              clear_edge["source"] == "alric-testman" and clear_edge["target"] == "betha-testwoman", clear_edge)
        check("AUTO_CLEAR edge is marked via=dispute-inject", clear_edge.get("via") == "dispute-inject", clear_edge)

        disputed_edge = next(e for e in edges_out if e["type"] == "LOVER_OF")
        check("AUTO_DISPUTED edge injected as tier-2", disputed_edge["tier"] == "tier-2", disputed_edge)
        check("AUTO_DISPUTED edge carries disputed:true", disputed_edge.get("disputed") is True, disputed_edge)
        check("AUTO_DISPUTED edge carries in_universe_source from preclass_in_universe_source",
              disputed_edge.get("in_universe_source") == "mushroom", disputed_edge)

        fallback_edge = next(e for e in edges_out if e["source"] == "jaehaerys-i-targaryen")
        check("resolver-fallback edge resolved 'Jaehaerys I Targaryen' (not in matched.jsonl) "
              "via weirwood_query.resolve", fallback_edge["source"] == "jaehaerys-i-targaryen", fallback_edge)
        check("resolver-fallback edge target still resolved via matched.jsonl",
              fallback_edge["target"] == "betha-testwoman", fallback_edge)

        merge_plan_out = json.loads((unit_dir / "merge-plan.json").read_text(encoding="utf-8"))
        check("merge-plan.json: 1 entry for elyn-proseworthy", len(merge_plan_out) == 1, merge_plan_out)
        entry = merge_plan_out[0] if merge_plan_out else {}
        check("merge-plan.json entry targets the right slug", entry.get("slug") == "elyn-proseworthy", entry)
        expected_bullet = f"- A minor lord of no particular note ({UNIT}:30)"
        check("AUTO_CLEAR prose bullet formatted '- <text> (<unit>:<line>)'",
              entry.get("fab_section_md") == expected_bullet, entry)

        leftover_out = [json.loads(ln) for ln in
                        (unit_dir / "dispute-inject-leftover.jsonl").read_text(encoding="utf-8").splitlines() if ln]
        check("dispute-inject-leftover.jsonl has exactly the unresolvable-name row",
              len(leftover_out) == 1 and leftover_out[0]["source"] == "Qwyxzflarn Nobodyson", leftover_out)

        deferred_out = [json.loads(ln) for ln in
                        (unit_dir / "dispute-events-deferred.jsonl").read_text(encoding="utf-8").splitlines() if ln]
        check("dispute-events-deferred.jsonl has exactly the event row (with its preclass fields intact)",
              len(deferred_out) == 1 and deferred_out[0]["name"] == "Test Battle of Nowhere"
              and deferred_out[0]["preclass_bucket"] == "AUTO_CLEAR", deferred_out)

        # ---------------------------------------------------------------
        # Run 2 — idempotency: nothing new should be injected.
        # ---------------------------------------------------------------
        report2 = D.process_unit(UNIT, apply_dir, nodes_root, verdict_index={}, dry_run=False)
        s2 = report2["stats"]
        check("run2 (idempotent re-run): 0 NEW edges injected", s2.get("edges_injected", 0) == 0, s2)
        check("run2 (idempotent re-run): 0 NEW bullets injected", s2.get("bullets_injected", 0) == 0, s2)
        check("run2: edges_already_present == 3 (all 3 from run1 detected as dupes)",
              s2.get("edges_already_present") == 3, s2)
        check("run2: bullets_already_present == 1", s2.get("bullets_already_present") == 1, s2)

        candidates_out2 = json.loads((unit_dir / "candidates.json").read_text(encoding="utf-8"))
        check("run2: candidates.json edge count unchanged (still 4, no duplicate DISP rows)",
              len(candidates_out2["edges"]) == 4, candidates_out2["edges"])

        merge_plan_out2 = json.loads((unit_dir / "merge-plan.json").read_text(encoding="utf-8"))
        check("run2: merge-plan.json bullet text unchanged (no duplicate bullet line)",
              merge_plan_out2[0]["fab_section_md"] == expected_bullet, merge_plan_out2)

    # -------------------------------------------------------------------
    # Small pure-function checks (no filesystem needed).
    # -------------------------------------------------------------------
    check("determine_treatment: AUTO_CLEAR bucket, no verdict -> inject tier-1",
          D.determine_treatment({"preclass_bucket": "AUTO_CLEAR"}, None)
          == {"action": "inject", "tier": "tier-1", "disputed": False,
              "in_universe_source": None, "basis": "auto"})

    t = D.determine_treatment({"preclass_bucket": "NEEDS_READ"}, None)
    check("determine_treatment: NEEDS_READ, no verdict -> skip", t["action"] == "skip", t)

    t = D.determine_treatment({"preclass_bucket": "NEEDS_READ", "preclass_in_universe_source": None},
                              {"verdict": "disputed", "in_universe_source": "eustace"})
    check("determine_treatment: NEEDS_READ + a 'disputed' verdict -> inject tier-2 with the verdict's "
          "own in_universe_source", t["action"] == "inject" and t["tier"] == "tier-2"
          and t["in_universe_source"] == "eustace", t)

    t = D.determine_treatment({"preclass_bucket": "ROMANCE_CLASS"}, {"verdict": "drop"})
    check("determine_treatment: a 'drop' verdict -> action drop", t["action"] == "drop", t)

    row = {"kind": "edge", "line": 5, "edge_type": "PARENT_OF", "source": "A", "target": "B"}
    idx = D.index_verdicts([{"unit": "u1", "kind": "edge", "source": "A", "target": "B",
                             "edge_type": "PARENT_OF", "verdict": "clear"}])
    v = D.find_verdict("u1", row, idx)
    check("find_verdict matches the edge-shaped fallback tuple (kind/source/target/edge_type)",
          v is not None and v["verdict"] == "clear", v)

    row_ref = D.compute_row_ref("u1", row)
    idx2 = D.index_verdicts([{"unit": "u1", "row_ref": row_ref, "verdict": "disputed",
                              "in_universe_source": "munkun"}])
    v2 = D.find_verdict("u1", row, idx2)
    check("find_verdict matches an explicit row_ref", v2 is not None and v2["in_universe_source"] == "munkun", v2)

    prose_row = {"kind": "prose", "line": 9, "entity": "Someone", "slug": "someone"}
    idx3 = D.index_verdicts([{"unit": "u1", "kind": "prose", "entity": "Someone", "slug": "someone",
                              "verdict": "clear"}])
    v3 = D.find_verdict("u1", prose_row, idx3)
    check("find_verdict matches the prose-shaped fallback tuple (extension)",
          v3 is not None and v3["verdict"] == "clear", v3)

    # assert_disputed_invariant backstop
    try:
        D.assert_disputed_invariant([{"id": "DISP9", "type": "KILLS", "source": "a", "target": "b",
                                      "tier": "tier-1", "disputed": True}])
        check("assert_disputed_invariant fails loudly on a disputed edge with no in_universe_source",
              False, "did not raise")
    except SystemExit as e:
        check("assert_disputed_invariant fails loudly on a disputed edge with no in_universe_source",
              "DISP9" in str(e), str(e))

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
