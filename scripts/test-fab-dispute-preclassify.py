#!/usr/bin/env python3
"""Build-time unit tests for scripts/fab-dispute-preclassify.py.

Deterministic, no LLM, no network. Exercises classify_row() against the 5
scenarios named in the build brief plus a few corpus-shaped edge cases (romance
ambiguous, non-edge kinds, off-vocab genealogical types).

S201 UPDATE (documented, not silent — same convention as the script's own
"SPEC DEVIATION" docstring section): extending auto-resolution to
kind=="prose"/"event" (previously edge-only) intentionally flips the expected
outcome of 2 of the original 47 checks, because those two rows are now exactly
the cases the new rule is designed to auto-resolve:
  - "bare-text 'companions' alone is NOT a romance entry trigger" (kind=prose,
    text="gathered unsuitable companions") — was NEEDS_READ under the old
    edge_type-gated bucket-1 (prose rows never carry edge_type, so they always
    fell through to the generic default). Now: prose kind with no hedge/
    attribution cue in its own text -> AUTO_CLEAR (a flat low-stakes
    node-description bullet, per spec). Updated below, same row, new
    expectation, label kept close to the original for traceability.
  - "event-kind row (no edge_type) with no hedge cue" (kind=event, name="Birth
    of Lucerys Velaryon", quote="given birth to a second son late in the year
    115 AC") — was NEEDS_READ for the same "no edge_type" reason. Now: event
    kind with no ambiguity/hedge cue in EITHER name or quote -> AUTO_CLEAR.
    Updated below with the same inputs, new expectation.
All other 45 original checks are unchanged and still pass.

Run:  python3 scripts/test-fab-dispute-preclassify.py
"""
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "fab_dispute_preclassify", REPO / "scripts" / "fab-dispute-preclassify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = _load_module()

PASS, FAIL = 0, 0


def check(label, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {label}")
    else:
        FAIL += 1
        print(f"  FAIL {label}  {detail}")


def main():
    # --- the 5 named scenarios ---
    r = P.classify_row({"kind": "edge", "edge_type": "PARENT_OF",
                        "quote": "Aegon was the father of Aenys"})
    check("PARENT_OF flat quote -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    r = P.classify_row({"kind": "edge", "edge_type": "PARENT_OF",
                        "quote": "it is said that she gave birth to a second son"})
    check("PARENT_OF quote containing 'it is said' -> AUTO_DISPUTED",
          r["preclass_bucket"] == "AUTO_DISPUTED" and r["preclass_tier"] == 2, r)

    r = P.classify_row({"kind": "edge", "edge_type": "LOVER_OF",
                        "quote": "the groom's favorite"})
    check("LOVER_OF \"the groom's favorite\" -> AUTO_DISPUTED",
          r["preclass_bucket"] == "AUTO_DISPUTED" and r["preclass_tier"] == 2, r)

    r = P.classify_row({"kind": "edge", "edge_type": "LOVER_OF",
                        "quote": "his paramour"})
    check("LOVER_OF 'his paramour' -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    r = P.classify_row({"kind": "edge", "edge_type": "KILLS",
                        "quote": "slew him in a duel near the border"})
    check("KILLS proximity-only row -> NEEDS_READ",
          r["preclass_bucket"] == "NEEDS_READ" and r["preclass_tier"] is None, r)

    # --- romance-class ambiguous (no flat/euphemism/hedge cue) -> its own bucket ---
    r = P.classify_row({"kind": "edge", "edge_type": "LOVER_OF",
                        "quote": "helped his woman down from Vhagar's back"})
    check("LOVER_OF with no flat/euphemism cue -> ROMANCE_CLASS (not generic NEEDS_READ)",
          r["preclass_bucket"] == "ROMANCE_CLASS" and r["preclass_tier"] is None, r)

    r = P.classify_row({"kind": "edge", "edge_type": "LOVER_OF", "quote": '"'})
    check("LOVER_OF with garbage/empty quote -> ROMANCE_CLASS, never crashes",
          r["preclass_bucket"] == "ROMANCE_CLASS", r)

    # --- entry-trigger word list is {paramour, lover, mistress, favorite} ONLY —
    #     "companion"/"close to"/"intimate with" are EUPHEMISM sub-decision terms,
    #     not entry triggers, so bare "companions" text (no paramour/lover/mistress/
    #     favorite, no edge_type) must NOT be swept into the romance branch (this is
    #     the real corpus's "gathered unsuitable companions" row — about bad company,
    #     not romance). S201: it's still NOT romance-class, but it's now the
    #     prose-kind flat-text fallback -> AUTO_CLEAR (a flat low-stakes
    #     node-description bullet, no hedge/attribution cue in its own text) —
    #     was NEEDS_READ before S201 extended auto-resolution to prose kind.
    r = P.classify_row({"kind": "prose", "entity": "Someone",
                        "text": "gathered unsuitable companions"})
    check("bare-text 'companions' alone is NOT a romance entry trigger -> AUTO_CLEAR (prose fallback, S201)",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    # --- euphemism sub-decision DOES fire once romance-branch is entered via edge_type ---
    r = P.classify_row({"kind": "edge", "edge_type": "LOVER_OF",
                        "quote": "she was often seen close to him at court"})
    check("LOVER_OF quote with euphemism 'close to' -> AUTO_DISPUTED",
          r["preclass_bucket"] == "AUTO_DISPUTED", r)

    r = P.classify_row({"kind": "prose", "entity": "Someone",
                        "text": "He kept her as his paramour thirteen years"})
    check("bare-text flat entry ('paramour') on a non-edge kind -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR", r)

    # --- BONDED_TO (task-listed as genealogical/definitional despite living under
    #     Magic & Supernatural in architecture.md) flat dragon-bond fact -> AUTO_CLEAR ---
    r = P.classify_row({"kind": "edge", "edge_type": "BONDED_TO",
                        "quote": "who had flown Vermithor and Silverwing into battle"})
    check("BONDED_TO flat dragon-bond quote -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR", r)

    # --- S201: kind=="event" with no ambiguity cue in name OR quote -> AUTO_CLEAR
    #     (was NEEDS_READ pre-S201, back when only kind=="edge" could auto-resolve;
    #     "Birth of Lucerys Velaryon" itself carries no secret/alleged/rumored/hedge
    #     term in either field, so the flat-event fallback now clears it — tier-1,
    #     no in_universe_source). See the 4 new dedicated kind-dispatch tests below
    #     for the NEEDS_READ / AUTO_DISPUTED counterparts.
    r = P.classify_row({"kind": "event", "name": "Birth of Lucerys Velaryon",
                        "quote": "given birth to a second son late in the year 115 AC"})
    check("event-kind row (no edge_type), no ambiguity cue -> AUTO_CLEAR (event fallback, S201)",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    # --- 'according to NAME' regex hedge verb ---
    r = P.classify_row({"kind": "prose", "entity": "Baela Targaryen",
                        "text": "According to Baela's own provocation, she had bedded two of Rowan's sons"})
    check("'according to NAME' regex hedge -> AUTO_DISPUTED",
          r["preclass_bucket"] == "AUTO_DISPUTED", r)

    # --- DESCENDANT_OF / TWIN_OF requested-but-not-canonical types never AUTO_CLEAR ---
    check("DESCENDANT_OF dropped from GENEALOGICAL_TYPES (not in locked vocab)",
          "DESCENDANT_OF" not in P.GENEALOGICAL_TYPES)
    check("TWIN_OF dropped from GENEALOGICAL_TYPES (not in locked vocab)",
          "TWIN_OF" not in P.GENEALOGICAL_TYPES)
    r = P.classify_row({"kind": "edge", "edge_type": "TWIN_OF",
                        "quote": "born on the same night, twins in truth"})
    check("TWIN_OF (off-vocab request) never AUTO_CLEARs -> NEEDS_READ",
          r["preclass_bucket"] == "NEEDS_READ", r)

    # --- real genealogical types confirmed present in the locked vocab ---
    for t in ("PARENT_OF", "SIBLING_OF", "SPOUSE_OF", "ANCESTOR_OF", "UNCLE_OF",
              "NEPHEW_OF", "COUSIN_OF", "IN_LAW_OF", "STEP_PARENT_OF", "STEP_CHILD_OF",
              "MILK_BROTHER_OF", "HEIR_TO", "SUCCEEDS", "NAMED_AFTER", "BONDED_TO",
              "PROPOSED_AS_BRIDE", "COURTS", "MARRIES_OFF"):
        check(f"{t} present in GENEALOGICAL_TYPES", t in P.GENEALOGICAL_TYPES)

    # --- ROMANCE_EDGE_TYPES reused verbatim from the reconciler (no drift) ---
    check("ROMANCE_EDGE_TYPES reused from reconciler covers LOVER_OF",
          "LOVER_OF" in P.ROMANCE_EDGE_TYPES)
    check("ROMANCE_EDGE_TYPES reused from reconciler covers PARAMOUR_OF",
          "PARAMOUR_OF" in P.ROMANCE_EDGE_TYPES)

    # --- lexicon helper unit checks ---
    check("find_hedge_match finds 'purportedly'",
          P.find_hedge_match("he purportedly slew the dragon") == "purportedly")
    check("find_hedge_match returns None on flat text",
          P.find_hedge_match("he slew the dragon") is None)
    check("find_euphemism_match finds 'favorite'",
          P.find_euphemism_match("the new favorite of the court") == "favorite")
    check("find_flat_match finds 'his mistress'",
          P.find_flat_match("she was known as his mistress") == "his mistress")
    check("find_flat_match matches bare 'lover(s)'",
          P.find_flat_match("they were lovers for a decade") is not None)
    check("is_romance_entry True on LOVER_OF edge_type with unrelated quote",
          P.is_romance_entry("LOVER_OF", "some unrelated text") is True)
    check("is_romance_entry False on unrelated edge_type + unrelated quote",
          P.is_romance_entry("KILLS", "slew him in the yard") is False)
    check("source_from_hedge_term maps a real chronicler",
          P.source_from_hedge_term("Mushroom") == "mushroom")
    check("source_from_hedge_term returns None on the romance sentinel",
          P.source_from_hedge_term("romance-class-untagged") is None)

    # =========================================================================
    # S201 — kind=="prose"/"event" auto-resolve extension
    # =========================================================================

    # --- the 4 scenarios named in the S201 build brief, verbatim ---
    r = P.classify_row({"kind": "prose", "entity": "Harwin Strong", "slug": "harwin-strong",
                        "text": "After her wedding he became foremost of the blacks at her side"})
    check("S201: flat prose row -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    r = P.classify_row({"kind": "prose", "entity": "Corlys Velaryon", "slug": "corlys-velaryon",
                        "text": "it is said that he sailed nine voyages upon the Sea Snake"})
    check("S201: prose row with 'it is said' -> AUTO_DISPUTED",
          r["preclass_bucket"] == "AUTO_DISPUTED" and r["preclass_tier"] == 2, r)

    r = P.classify_row({"kind": "event", "name": "Secret marriage of Rhaenyra and Daemon",
                        "quote": "The marriage had been performed on Dragonstone, suddenly and secretly"})
    check("S201: event 'Secret marriage of...' -> NEEDS_READ",
          r["preclass_bucket"] == "NEEDS_READ" and r["preclass_tier"] is None, r)

    r = P.classify_row({"kind": "event", "name": "Cremation of King Aegon II",
                        "quote": "his body was burned upon a pyre before the Red Keep"})
    check("S201: flat event 'Cremation of King Aegon II' -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR" and r["preclass_tier"] == 1, r)

    # --- real-corpus-shaped extras: chronicler-opinion attribution (bare 'claims'/
    #     'tells', not covered by the literal HEDGE_VERB_PHRASES list) ---
    r = P.classify_row({"kind": "prose", "entity": "Alys Rivers",
                        "text": "Mushroom alone claims she was pregnant with Aegon's child"})
    check("S201: prose 'Mushroom alone claims' -> AUTO_DISPUTED via chronicler-opinion attribution",
          r["preclass_bucket"] == "AUTO_DISPUTED" and r["preclass_tier"] == 2
          and r["preclass_in_universe_source"] == "mushroom", r)

    r = P.classify_row({"kind": "prose", "entity": "Ormund Hightower",
                        "text": "Munkun tells it differently: the Tyrells forbade him to go to war"})
    check("S201: prose 'Munkun tells it differently' -> AUTO_DISPUTED via chronicler-opinion attribution",
          r["preclass_bucket"] == "AUTO_DISPUTED" and r["preclass_in_universe_source"] == "munkun", r)

    # --- chronicler-opinion attribution requires an ACTUAL chronicler name, not just
    #     any character's own reported claim (no false-positive sweep) ---
    r = P.classify_row({"kind": "prose", "entity": "Cregan Stark",
                        "text": "Cregan claimed her hand in marriage in return"})
    check("S201: non-chronicler 'Cregan claimed' does NOT trigger chronicler-opinion -> AUTO_CLEAR",
          r["preclass_bucket"] == "AUTO_CLEAR", r)

    # --- event ambiguity gate fires on the higher-stakes term list too (not just a
    #     hedge verb), and NEVER auto-disputes an event (NEEDS_READ only) ---
    r = P.classify_row({"kind": "event", "name": "Rumored poisoning of Lord Rogar",
                        "quote": "he sickened and died within a fortnight of the feast"})
    check("S201: event name containing 'rumored' -> NEEDS_READ (never AUTO_DISPUTED for events)",
          r["preclass_bucket"] == "NEEDS_READ", r)

    r = P.classify_row({"kind": "event", "name": "Wedding of Aegon the Elder and Helaena",
                        "quote": "King Viserys wed his son Aegon the Elder to his daughter Helaena, "
                                 "it is said, to spite Rhaenyra"})
    check("S201: event quote containing a hedge verb -> NEEDS_READ (never AUTO_DISPUTED for events)",
          r["preclass_bucket"] == "NEEDS_READ", r)

    # --- lexicon helper unit checks: chronicler-opinion / composite dispute signal /
    #     event ambiguity gate ---
    check("find_chronicler_opinion_match finds 'Eustace tells us'",
          P.find_chronicler_opinion_match("Eustace tells us the feast lasted seven days") is not None)
    check("find_chronicler_opinion_match returns None with no chronicler name present",
          P.find_chronicler_opinion_match("the fool claims the queen's ladies donned mail") is None)
    check("find_chronicler_opinion_match returns None on a bare chronicler-name mention (no opinion verb)",
          P.find_chronicler_opinion_match("Munkun's True Telling records the confession") is None)
    check("find_dispute_signal is a superset of find_hedge_match (catches 'purportedly')",
          P.find_dispute_signal("he purportedly slew the dragon") == "purportedly")
    check("find_dispute_signal also catches chronicler-opinion attribution find_hedge_match misses",
          P.find_dispute_signal("Mushroom alone claims it") is not None)
    check("find_event_ambiguity_match finds 'secret' in the NAME field",
          P.find_event_ambiguity_match("Secret marriage of Rhaenyra and Daemon", "flat quote") == "secret")
    check("find_event_ambiguity_match finds a hedge verb in the QUOTE field",
          P.find_event_ambiguity_match("Death of Lord X", "it is said he died of a fever") is not None)
    check("find_event_ambiguity_match returns None on flat name+quote",
          P.find_event_ambiguity_match("Cremation of King Aegon II",
                                        "his body was burned upon a pyre") is None)

    # --- per-kind summary breakdown helper (S201) ---
    per_unit_rows_fixture = {
        "unit-a": [
            {"kind": "edge", "preclass_bucket": "AUTO_CLEAR"},
            {"kind": "edge", "preclass_bucket": "NEEDS_READ"},
            {"kind": "prose", "preclass_bucket": "AUTO_CLEAR"},
            {"kind": "event", "preclass_bucket": "NEEDS_READ"},
        ],
        "unit-b": [
            {"kind": "prose", "preclass_bucket": "AUTO_DISPUTED"},
        ],
    }
    kc = P.build_kind_bucket_counts(per_unit_rows_fixture)
    check("build_kind_bucket_counts: edge kind counted correctly",
          kc["edge"]["AUTO_CLEAR"] == 1 and kc["edge"]["NEEDS_READ"] == 1, kc)
    check("build_kind_bucket_counts: prose kind aggregates across units",
          kc["prose"]["AUTO_CLEAR"] == 1 and kc["prose"]["AUTO_DISPUTED"] == 1, kc)
    check("build_kind_bucket_counts: event kind counted correctly",
          kc["event"]["NEEDS_READ"] == 1, kc)

    summary_with_kinds = P.build_summary(
        {"unit-a": Counter({"AUTO_CLEAR": 2, "NEEDS_READ": 2}), "unit-b": Counter({"AUTO_DISPUTED": 1})},
        Counter({"AUTO_CLEAR": 2, "NEEDS_READ": 2, "AUTO_DISPUTED": 1}), 5, [], kc)
    check("build_summary prints a 'Per-kind breakdown' section when kind_counts is supplied",
          "Per-kind breakdown" in summary_with_kinds and "prose" in summary_with_kinds
          and "event" in summary_with_kinds)

    # --- output-row shape: original fields survive, preclass_* fields appended ---
    row_in = {"unit": "fab-test-01", "kind": "edge", "edge_type": "PARENT_OF",
              "source": "A", "target": "B", "quote": "A was the father of B",
              "line": 5, "hedge_term": "eustace", "hedge_distance": 0}
    result = P.classify_row(row_in)
    out_row = dict(row_in)
    out_row.update(result)
    check("classified row preserves every original field",
          all(out_row[k] == v for k, v in row_in.items()), out_row)
    check("classified row adds all 4 preclass_* fields",
          {"preclass_bucket", "preclass_tier", "preclass_in_universe_source", "preclass_reason"}
          <= out_row.keys(), out_row)

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
