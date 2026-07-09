#!/usr/bin/env python3
"""Build-time unit tests for scripts/fab-reconcile-candidates.py.

Deterministic, no LLM, no network. Loads the real blocklist / redirect map / same-name
clusters / node index and asserts the §5.1 routing rules — especially the R1
confident-wrong-match trap and the S199 CREATE-guard fixes.

Run:  python3 scripts/test-fab-reconcile.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load_reconciler():
    spec = importlib.util.spec_from_file_location(
        "fab_reconcile", REPO / "scripts" / "fab-reconcile-candidates.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load_reconciler()


def make_router(smoke=False):
    D = REPO / "working" / "wiki" / "data"
    blocklist = R.load_json(D / "disambig-node-blocklist.json", {})
    redirect_map = R.load_json(D / "redirect-node-map.json", {})
    clusters = R.load_json(D / "same-name-clusters.json", {})
    existing_slugs, house_slugs, node_categories = R.index_existing_nodes(REPO / "graph" / "nodes")
    return R.Router(blocklist, redirect_map, clusters, pack=None,
                    unit_era="targaryen-conquest", smoke=smoke,
                    existing_slugs=existing_slugs, house_slugs=house_slugs,
                    node_categories=node_categories)


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
    router = make_router(smoke=False)

    # --- R1 trap: "Aegon Targaryen" must NEVER accept the aegon-targaryen disambig node ---
    r = router.route("Aegon Targaryen", "")
    check("Aegon Targaryen never UPDATEs the trap node",
          not (r["decision"] == "update" and r.get("slug") == "aegon-targaryen"), r)
    check("Aegon Targaryen routes to review/discriminate (blocklist+cluster)",
          r["decision"] == "review", r)

    # --- redirect: "Aenys Targaryen" -> aenys-i-targaryen (transparent redirect wins) ---
    r = router.route("Aenys Targaryen", "")
    check("Aenys Targaryen redirects to aenys-i-targaryen",
          r["decision"] == "update" and r.get("slug") == "aenys-i-targaryen", r)

    # --- clean hit: "Criston Cole" -> UPDATE criston-cole ---
    r = router.route("Criston Cole", "")
    check("Criston Cole UPDATE-accepts criston-cole",
          r["decision"] == "update" and r.get("slug") == "criston-cole", r)

    # --- S199 fix 1a: fuzzy `candidates` status must NOT CREATE (daenys, arrec) ---
    for nm in ("daenys", "arrec"):
        r = router.route(nm, "daughter of Aenar, a Targaryen of old Valyria")
        check(f"{nm!r} (fuzzy candidates) routes to review, never CREATE",
              r["decision"] == "review", r)

    # --- S199 fix 1b: bare plural surname whose House node exists -> review, not CREATE ---
    for nm, expect in (("Blackwoods", "house-blackwood"), ("Vances", "house-vance"),
                       ("Mudds", "house-mudd"), ("Strongs", "house-strong")):
        r = router.route(nm, "")
        cand_slugs = [c.get("slug") for c in r.get("candidates", [])]
        check(f"{nm!r} routes to review with {expect} candidate (no dupe mint)",
              r["decision"] == "review" and expect in cand_slugs, r)

    # --- S199 fix 2: composite / collective names never CREATE ---
    r = router.route("Mern IX Gardener; Loren I Lannister", "")
    check("composite '; '-joined cell routes to review", r["decision"] == "review", r)
    r = router.route("the Targaryen fleet", "")
    check("collective 'the Targaryen fleet' routes to review", r["decision"] == "review", r)

    # --- S199 event-type-aware routing: event-vs-event dedup risk -> review;
    #     event whose only fuzzy candidate is a person/place -> CREATE ---
    r = router.route("Submission of Rosby", "", kind="event")
    check("event with an existing-event candidate routes to review (dedup risk)",
          r["decision"] == "review", r)
    # S200: fixture was "Capture of Loren Lannister" until that event node was minted
    # (S200 apply made it a clean hit -> update, which is correct live behavior).
    # sharra-arryn exists as a person node; no such event node exists.
    r = router.route("Capture of Sharra Arryn", "", kind="event")
    check("event whose only candidate is a person CREATEs (genuinely new)",
          r["decision"] == "create", r)

    # --- CREATE guard helpers (unit-level) ---
    check("looks_composite splits '; '", R.looks_composite("A B; C D") is True)
    check("looks_composite false on single name", R.looks_composite("Orys Baratheon") is False)
    check("is_collective true on 'host'", R.is_collective("Aegon's host at the Field of Fire") is True)
    check("is_collective false on person", R.is_collective("Torrhen Stark") is False)
    check("singularize Blackwoods->Blackwood", R.singularize("Blackwoods") == "Blackwood")
    check("singularize keeps 'ss'", R.singularize("Loss") == "Loss")

    # --- S199 fix 3: wrap-aware locate_quote across a blank-line paragraph gap ---
    lines = ["He was named Warden of the South and Lord", "", "Paramount of the Mander by King Aegon."]
    ln = R.locate_quote(lines, "Warden of the South and Lord Paramount of the Mander")
    check("wrap-aware locate_quote finds paragraph-gap quote", ln == 1, f"got {ln}")
    ln2 = R.locate_quote(lines, "no such quote appears here at all")
    check("locate_quote returns None on a genuine miss", ln2 is None, f"got {ln2}")

    # --- S199 Stage-2 §5.1 tuning: base-name parent/spouse discriminator + margin rule ---
    clusters = R.load_json(REPO / "working" / "wiki" / "data" / "same-name-clusters.json", {})
    sc = R.score_candidates("Baelon Targaryen", "son of Jaehaerys I and Alysanne",
                            "", None, clusters["baelon targaryen"])
    check("parent base-name 'jaehaerys' scores despite slug-form parents",
          any(h.startswith("disambiguator~parent:jaehaerys")
              for h in sc["baelon-targaryen-son-of-jaehaerys-i"]["hits"]),
          sc["baelon-targaryen-son-of-jaehaerys-i"])
    sc2 = R.score_candidates("Aemon Targaryen",
                             "son of Jaehaerys I and Alysanne; Prince of Dragonstone; father of Rhaenys",
                             "", None, clusters["aemon targaryen"])
    top_hits = sc2["aemon-targaryen-son-of-jaehaerys-i"]["hits"]
    check("ALL category-(a) hits kept (parent AND shared title), score caps category at 1",
          any("parent:jaehaerys" in h for h in top_hits)
          and any(h == "disambiguator~prince" for h in top_hits)
          and sc2["aemon-targaryen-son-of-jaehaerys-i"]["score"] == 1, sc2)

    # margin rule via a synthetic cluster: top 2 hits, runner-up's single hit SHARED -> accept;
    # tie -> review; runner-up-only evidence -> review.
    syn = {"members": {
        "testy-a": {"parents": ["fatherx-targaryen"], "spouse": [], "key_title": "prince",
                    "era": None, "born": None, "died": 82, "regnal": None},
        "testy-b": {"parents": [], "spouse": [], "key_title": "prince",
                    "era": None, "born": None, "died": None, "regnal": None},
    }, "trap_nodes": [], "redirect_nodes": []}
    rt = R.Router({}, {}, {"testy tester": syn}, pack=None, unit_era="", smoke=False,
                  existing_slugs=set(), house_slugs=set())
    r = rt.route("Testy Tester", "the prince; son of Fatherx; died 82 AC")
    check("auto-accept fires on 2-vs-1 when runner-up hit is shared",
          r["decision"] == "update" and r.get("slug") == "testy-a", r)
    r = rt.route("Testy Tester", "the prince")
    check("tie routes to review", r["decision"] == "review", r)
    syn2 = {"members": {
        "testy-c": {"parents": ["fatherx-targaryen"], "spouse": [], "key_title": None,
                    "era": None, "born": None, "died": 82, "regnal": None},
        "testy-d": {"parents": ["mothery-targaryen"], "spouse": [], "key_title": None,
                    "era": None, "born": None, "died": None, "regnal": None},
    }, "trap_nodes": [], "redirect_nodes": []}
    rt2 = R.Router({}, {}, {"testy tester": syn2}, pack=None, unit_era="", smoke=False,
                   existing_slugs=set(), house_slugs=set())
    r = rt2.route("Testy Tester", "son of Fatherx and Mothery; died 82 AC")
    check("runner-up-only evidence routes to review even at 2-vs-1",
          r["decision"] == "review", r)

    # the Rhaena precision trap: pack-expected alone (score 1) must NEVER auto-accept
    pack = {"expected_slugs": ["rhaena-targaryen-daughter-of-daemon"],
            "per_slug": {"rhaena-targaryen-daughter-of-daemon": {"anchor_count": 3}}}
    rt3 = R.Router({}, {}, clusters, pack=pack, unit_era="dance-of-dragons", smoke=False,
                   existing_slugs=set(), house_slugs=set())
    r = rt3.route("Rhaena Targaryen", "sister of Jaehaerys I; began the dragon-egg-in-cradle tradition")
    check("Rhaena trap: pack-expected-only top stays in review",
          r["decision"] == "review", r)

    # --- S199 Stage-2 BLOCKER fix: type-agreement gate on clean-hit UPDATEs ---
    r = router.route("Lorath", "Shivering Sea destination", type_guess="place")
    check("Lorath (place) never UPDATEs a character node (type gate)",
          not (r["decision"] == "update"
               and R.expected_category("place") != router.node_categories.get(r.get("slug"), "locations")),
          r)
    r2 = router.route("Criston Cole", "", type_guess="character")
    check("type gate passes on agreement (Criston Cole still UPDATEs)",
          r2["decision"] == "update" and r2.get("slug") == "criston-cole", r2)
    r3 = router.route("Criston Cole", "")
    check("empty type guess leaves routing unchanged",
          r3["decision"] == "update" and r3.get("slug") == "criston-cole", r3)

    # --- S199 Stage-2 eval fix 5: exact-1.0 accept with POSITIVE type agreement ---
    r = router.route("Dark Sister", "Valyrian sword given to Daemon", type_guess="sword")
    check("exact-1.0 + type-agree auto-accepts (Dark Sister -> dark-sister)",
          r["decision"] == "update" and r.get("slug") == "dark-sister", r)
    r = router.route("Cod Queen", "fishing boat Corlys first captained", type_guess="ship")
    check("Cod Queen (ship) must NOT exact-accept onto a non-artifact node",
          not (r["decision"] == "update"
               and router.node_categories.get(r.get("slug")) != "artifacts"), r)
    r = router.route("Merling King", "legendary giver of the Driftwood Throne",
                     type_guess="figure (legend)")
    check("Merling King (unmapped guess) never exact-accepts (no positive agreement)",
          r["decision"] != "update" or r.get("route_reason") != "exact-1.0-type-agree", r)
    rs = make_router(smoke=True)
    r = rs.route("Dark Sister", "Valyrian sword given to Daemon", type_guess="sword")
    check("smoke mode holds the exact-1.0 accept in review",
          r["decision"] == "review" and r["reason"] == "smoke-exact-accept-disabled", r)

    # --- S199 Stage-2 eval fix 7: type normalization ---
    check("event.tourney -> event.tournament", R.guess_node_type("event.tourney") == "event.tournament")
    check("bare place -> place.location", R.guess_node_type("place") == "place.location")
    check("bare house -> organization.house", R.guess_node_type("house") == "organization.house")
    check("dragon -> character.dragon", R.guess_node_type("dragon") == "character.dragon")

    # --- S199 dispute-proximity quarantine (§7.2 gate FAIL response) ---
    zone = [
        "Otto Hightower was named Hand of the King.",                       # 1 flat
        "Here is where our sources diverge, however.",                      # 2 opener
        "The king sent his brother into exile, never to return.",          # 3 inside zone
        "Mushroom tells another tale entirely in his Testimony.",          # 4 hedge
        "Of the aftermath, these things are certain: the prince departed.", # 5 certainty
        "The prince returned to the Stepstones and his war.",              # 6 post-zone
    ]
    check("claim inside hedge neighborhood is flagged",
          R.dispute_proximity(zone, 3) is not None)
    check("flat claim next to certainty marker (closer than hedge) is cleared",
          R.dispute_proximity(zone, 6) is None, R.dispute_proximity(zone, 6))
    far = ["flat text"] * 30
    check("no hedge in window -> None", R.dispute_proximity(far, 15) is None)
    check("romance-class set covers LOVER_OF", "LOVER_OF" in R.ROMANCE_EDGE_TYPES)

    # --- S199 identity_line wiring (Matt: 'wire it') ---
    ents = [{"text": "Second wife of Maegor, daughter of Lord Lucas Harroway", "quote": ""}]
    check("identity_line composed as 'Name — text.'",
          R.derive_identity_line("Alys Harroway", ents)
          == "Alys Harroway — Second wife of Maegor, daughter of Lord Lucas Harroway.")
    ents2 = [{"text": "He and Queen Alysanne produced thirteen children", "quote": ""}]
    check("pronoun-opener bullet yields no identity_line (boilerplate stays)",
          R.derive_identity_line("Jaehaerys I Targaryen", ents2) is None)
    ents3 = [{"text": "Alys Harroway was the second wife of Maegor.", "quote": ""}]
    check("name-prefixed bullet passes through un-doubled",
          R.derive_identity_line("Alys Harroway", ents3)
          == "Alys Harroway was the second wife of Maegor.")
    check("empty prose yields None", R.derive_identity_line("X Y", [{"text": "", "quote": ""}]) is None)
    check("overlong bullet yields None",
          R.derive_identity_line("X Y", [{"text": "w " * 200, "quote": ""}]) is None)

    # --- S199 Stage-2: year-aware era refinement for dated CREATE events ---
    check("era_for_year 92 -> targaryen-rule", R.era_for_year(92) == "targaryen-rule")
    check("era_for_year 130 -> dance-of-dragons", R.era_for_year(130) == "dance-of-dragons")
    check("era_for_year 1 -> targaryen-conquest", R.era_for_year(1) == "targaryen-conquest")
    check("era_for_year -50 -> pre-conquest", R.era_for_year(-50) == "pre-conquest")

    # --- S199 Stage-2 fix: trailing-punct quote repair (extractor clips mid-sentence + adds '.') ---
    lines3 = ["His remains were burned in the Dragonpit, his ashes interred on Dragonstone."]
    ln3, canon3, rep3 = R.locate_or_repair(lines3, "His remains were burned in the Dragonpit.")
    check("locate_or_repair strips synthetic trailing period",
          ln3 == 1 and rep3 is True and canon3 == "His remains were burned in the Dragonpit",
          f"got ({ln3}, {canon3!r}, {rep3})")
    ln4, canon4, rep4 = R.locate_or_repair(lines3, "His remains were burned in the Dragonpit!")
    check("repaired canonical is strictly verbatim (mint re-locates it unchanged)",
          rep4 is True and R.locate_quote(lines3, canon4) == 1, f"got ({ln4}, {canon4!r}, {rep4})")
    ln5, canon5, rep5 = R.locate_or_repair(lines3, "He was burned at the Wall.")
    check("locate_or_repair still None on a genuine miss", ln5 is None and rep5 is False)
    ln6, canon6, rep6 = R.locate_or_repair(lines3, "His remains were burned in the Dragonpit, his ashes interred on Dragonstone.")
    check("strict hit is NOT flagged repaired", ln6 == 1 and rep6 is False and canon6.endswith("."))

    # --- S199 out-of-sample fix: enclosing-quote-pair strip (p02 extractor drift) ---
    ln7, canon7, rep7 = R.locate_or_repair(lines3, '"His remains were burned in the Dragonpit,"')
    check("enclosing quote pair stripped (p02 drift class)",
          ln7 == 1 and rep7 is True and canon7 == "His remains were burned in the Dragonpit,",
          f"got ({ln7}, {canon7!r}, {rep7})")
    ln8, canon8, rep8 = R.locate_or_repair(lines3, '"His remains were burned in the Dragonpit."')
    check("enclosing quotes + synthetic trailing punct both stripped",
          ln8 == 1 and rep8 is True and canon8 == "His remains were burned in the Dragonpit",
          f"got ({ln8}, {canon8!r}, {rep8})")
    lines_dlg = ['He called her "my bronze bitch," after the runic armor.']
    ln9, canon9, rep9 = R.locate_or_repair(lines_dlg, '"my bronze bitch,"')
    check("genuine dialogue quote matches strict-first, never stripped",
          ln9 == 1 and rep9 is False and canon9 == '"my bronze bitch,"',
          f"got ({ln9}, {canon9!r}, {rep9})")

    # --- S199 Stage-2 fix: OCR doubled-apostrophe collapse in norm ---
    lines_ocr = ["decreed that every copy of Mushroom’'s chronicle should be burned."]
    check("norm collapses OCR doubled apostrophe",
          R.locate_quote(lines_ocr, "every copy of Mushroom's chronicle should be burned.") == 1)

    # --- lockstep: reconciler.norm must equal mint_enrichment.norm (byte-identical) ---
    spec = importlib.util.spec_from_file_location(
        "mint_enrichment", REPO / "scripts" / "mint_enrichment.py")
    mint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mint)
    for sample in ("  “Warden”—of  the\n South…  ", "Mushroom’'s chronicle", "Aegon’'s host"):
        check(f"reconciler.norm == mint.norm (lockstep) on {sample!r}",
              R.norm(sample) == mint.norm(sample))

    # =========================================================================
    # P1 — VICTIM_IN harm-gate
    # =========================================================================
    for subtype in ("death", "execution", "murder", "assassination", "poisoning",
                    "maiming", "torture", "capture", "imprisonment", "battle", "sack",
                    "destruction", "suicide", "stillbirth", "betrayal", "raid",
                    "attack", "duel", "deception", "mutiny", "massacre", "abduction",
                    "wounding"):
        check(f"classify_patient_edge_type({subtype!r}) -> VICTIM_IN (harm subtype)",
              R.classify_patient_edge_type(subtype) == "VICTIM_IN")
    for subtype in ("birth", "coronation", "appointment", "investiture", "treaty",
                    "betrothal", "wedding", "funeral", "feast", "council",
                    "construction", "decree", "confrontation", "escape", "tournament"):
        check(f"classify_patient_edge_type({subtype!r}) -> PARTICIPATES_IN (non-harm)",
              R.classify_patient_edge_type(subtype) == "PARTICIPATES_IN")
    check("classify_patient_edge_type(None) -> PARTICIPATES_IN (unknown defaults neutral)",
          R.classify_patient_edge_type(None) == "PARTICIPATES_IN")
    check("classify_patient_edge_type('') -> PARTICIPATES_IN (absent defaults neutral)",
          R.classify_patient_edge_type("") == "PARTICIPATES_IN")
    check("classify_patient_edge_type('some-unmapped-subtype') -> PARTICIPATES_IN",
          R.classify_patient_edge_type("some-unmapped-subtype") == "PARTICIPATES_IN")
    check("classify_patient_edge_type is case-insensitive ('DEATH' -> VICTIM_IN)",
          R.classify_patient_edge_type("DEATH") == "VICTIM_IN")
    check("event_node_subtype('event.death') -> 'death'", R.event_node_subtype("event.death") == "death")
    check("event_node_subtype('event.incident') -> 'incident'",
          R.event_node_subtype("event.incident") == "incident")
    check("event_node_subtype(None) -> None", R.event_node_subtype(None) is None)
    check("event_node_subtype(bare 'event') -> None", R.event_node_subtype("event") is None)
    check("HARM_EVENT_SUBTYPES does not include 'birth'", "birth" not in R.HARM_EVENT_SUBTYPES)
    check("HARM_EVENT_SUBTYPES does not include 'coronation'", "coronation" not in R.HARM_EVENT_SUBTYPES)
    check("HARM_EVENT_SUBTYPES includes 'death'", "death" in R.HARM_EVENT_SUBTYPES)

    # --- coordinator follow-up: assassination_attempt (real case: "Attack on Queen
    #     Alysanne at Jonquil's Pool", fab-birth-death-and-betrayal-10) + generic
    #     attempt-marker spelling variants around an already-HARM base word ---
    check("classify_patient_edge_type('assassination_attempt') -> VICTIM_IN"
          " (spelling variant of 'assassination')",
          R.classify_patient_edge_type("assassination_attempt") == "VICTIM_IN")
    check("classify_patient_edge_type('attempted_murder') -> VICTIM_IN (prefix variant)",
          R.classify_patient_edge_type("attempted_murder") == "VICTIM_IN")
    check("classify_patient_edge_type('murder_attempt') -> VICTIM_IN (suffix variant)",
          R.classify_patient_edge_type("murder_attempt") == "VICTIM_IN")
    check("classify_patient_edge_type('attempted_treaty') -> PARTICIPATES_IN"
          " (attempt marker around a NON-harm base word stays neutral)",
          R.classify_patient_edge_type("attempted_treaty") == "PARTICIPATES_IN")
    # borderline political subtypes stay NON-HARM (PARTICIPATES_IN default) — not
    # reclassified by this fix, per explicit instruction.
    for subtype in ("siege", "uprising", "rebellion", "trial"):
        check(f"classify_patient_edge_type({subtype!r}) stays PARTICIPATES_IN"
              " (borderline political, not reclassified)",
              R.classify_patient_edge_type(subtype) == "PARTICIPATES_IN")

    # =========================================================================
    # P2 — junk character.human CREATE screen
    # =========================================================================
    JUNK_EXAMPLES = [
        "A Wanton's Tale", "Sins of the Flesh", "Six Times to Sea",
        "the Gullet, off Dragonstone", "field of ashes west of Rook's Rest",
        "the mob", "Myrish galley crew", "three sons of Elinor",
        "Rosby, Stokeworth, Duskendale", "Prince Joffrey's body", "OrphanMaker",
        # found on the full 39-unit out-of-sample scan (not in the board's original
        # list, but clearly junk of the same families — comma-list-of-places with an
        # article-prefixed member, and a table-parsing artifact bleeding into a cell).
        "Raventree, Riverrun, Stoney Sept, the Twins, Fairmarket",
        "Lord Rogar's four brothers → Borys Baratheon",
        # coordinator follow-up: collective-with-numeric-appositive, article-prefixed
        # (fab-rhaenyra-overthrown-18-p01) — was KEPT before the article-prefix predicate.
        "the Dragonkeepers, four dragons",
    ]
    for name in JUNK_EXAMPLES:
        reason = R.junk_character_screen(name)
        check(f"junk_character_screen rejects {name!r}", reason is not None, reason)
    REAL_PERSON_EXAMPLES = [
        "Criston Cole", "Alys Harroway", "Septon Eustace", "Rogar Baratheon",
        "Aegon the Conqueror", "Jaehaerys I Targaryen", "Mushroom", "Elinor Costayne",
        "Aegon (nephew of Maegor)",
    ]
    for name in REAL_PERSON_EXAMPLES:
        reason = R.junk_character_screen(name)
        check(f"junk_character_screen keeps real person {name!r}", reason is None, reason)

    check("junk_character_screen tags 'the Dragonkeepers, four dragons' article-prefixed",
          R.junk_character_screen("the Dragonkeepers, four dragons") == "junk-character-article-prefix",
          R.junk_character_screen("the Dragonkeepers, four dragons"))
    check("_is_article_prefixed true on 'the Sea Snake' (epithet/alias, not a primary name)",
          R._is_article_prefixed("the Sea Snake") is True)
    check("_is_article_prefixed false on 'Aegon the Conqueror' (article is mid-name)",
          R._is_article_prefixed("Aegon the Conqueror") is False)

    # =========================================================================
    # P3 — disputed => in_universe_source invariant
    # =========================================================================
    lines_p3 = ["Mushroom claims the king gave the order himself.",
                "Others say it was Ser Nobody entirely."]
    check("derive_in_universe_source finds 'Mushroom' in the quote itself",
          R.derive_in_universe_source("Mushroom claims the king gave the order himself.",
                                      lines_p3, 1) == "mushroom")
    lines_p3b = ["Septon Eustace, more plausibly, suspects Prince Daemon.",
                 "the king himself might have given the command"]
    check("derive_in_universe_source finds a chronicler on a nearby line",
          R.derive_in_universe_source("the king himself might have given the command",
                                      lines_p3b, 2) == "eustace")
    check("derive_in_universe_source defaults to gyldayn-synthesis with no chronicler nearby",
          R.derive_in_universe_source("no chronicler named here at all", ["flat text"] * 5, 3)
          == "gyldayn-synthesis")

    good_disputed_edge = {"id": "E1", "type": "KILLS", "source": "a", "target": "b",
                          "tier": "tier-2", "disputed": True, "in_universe_source": "gyldayn-synthesis"}
    try:
        R.assert_disputed_invariant([good_disputed_edge])
        check("assert_disputed_invariant passes a properly-sourced disputed edge", True)
    except SystemExit as e:
        check("assert_disputed_invariant passes a properly-sourced disputed edge", False, str(e))

    bad_disputed_edge = {"id": "E71", "type": "KILLS", "source": "viserys-i-targaryen",
                         "target": "lyonel-strong", "tier": "tier-2", "disputed": True}
    try:
        R.assert_disputed_invariant([bad_disputed_edge])
        check("assert_disputed_invariant fails loudly on a disputed edge with no in_universe_source",
              False, "did not raise")
    except SystemExit as e:
        msg = str(e)
        check("assert_disputed_invariant fails loudly on a disputed edge with no in_universe_source"
              " (names the offending edge id)", "E71" in msg, msg)

    bad_tier_edge = {"id": "E2", "type": "KILLS", "source": "a", "target": "b",
                     "tier": "tier-3", "disputed": True, "in_universe_source": "mushroom"}
    try:
        R.assert_disputed_invariant([bad_tier_edge])
        check("assert_disputed_invariant fails loudly on a disputed edge with tier>2", False, "did not raise")
    except SystemExit as e:
        check("assert_disputed_invariant fails loudly on a disputed edge with tier>2",
              "E2" in str(e), str(e))

    non_disputed_edge = {"id": "E3", "type": "KILLS", "source": "a", "target": "b", "tier": "tier-1"}
    try:
        R.assert_disputed_invariant([non_disputed_edge])
        check("assert_disputed_invariant ignores a non-disputed edge with no in_universe_source", True)
    except SystemExit as e:
        check("assert_disputed_invariant ignores a non-disputed edge with no in_universe_source",
              False, str(e))

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
