#!/usr/bin/env python3
"""
classify-prose-edges-randyll-tarly.py

Deterministic rule-based edge classifier for randyll-tarly.candidates.jsonl.

Reads the enriched prose-edge-candidates file for Randyll Tarly and classifies
each candidate into one of:
  - emit_edge         (a typed edge with evidence)
  - reject_just_mention  (co-mention only, no typed relationship)
  - escalate_cross_identity  (candidate requires identity resolution)
  - escalate_disambiguation  (target is ambiguous)

Output: one JSON row per candidate to prose-edges-haiku/randyll-tarly.edges.jsonl,
in input order.

Usage:
    python3 scripts/classify-prose-edges-randyll-tarly.py
    python3 scripts/classify-prose-edges-randyll-tarly.py --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

INPUT_PATH = Path(
    "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets"
    "/characters-house-tarly/prose-edge-candidates-enriched"
    "/randyll-tarly.candidates.jsonl"
)
OUTPUT_PATH = Path(
    "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets"
    "/characters-house-tarly/prose-edges-haiku"
    "/randyll-tarly.edges.jsonl"
)

SOURCE_SLUG = "randyll-tarly"


def emit_edge(target_slug, edge_type, snippet, section, paragraph_index=0,
              qualifier=None, confidence_tier=1):
    row = {
        "decision": "emit_edge",
        "candidate_kind": "source_target",
        "evidence_kind": "wiki-entity",
        "source_slug": SOURCE_SLUG,
        "target_slug": target_slug,
        "edge_type": edge_type,
    }
    if qualifier is not None:
        row["qualifier"] = qualifier
    row["evidence_snippet"] = snippet
    row["evidence_section"] = section
    row["evidence_paragraph_index"] = paragraph_index
    row["confidence_tier"] = confidence_tier
    return row


def reject(target_slug, reason):
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": SOURCE_SLUG,
        "target_slug": target_slug,
        "reason": reason,
    }


def escalate_cross_identity(target_slug, reason):
    return {
        "decision": "escalate_cross_identity",
        "candidate_kind": "source_target",
        "source_slug": SOURCE_SLUG,
        "target_slug": target_slug,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Classification table
# Keys are (target_slug, section_key) where section_key is a substring match
# against source_section. When multiple candidates share the same target_slug,
# the section discriminates which paragraph applies.
# A section_key of None means "match any section" — used for targets that
# appear in only one paragraph or where the relationship is the same across
# all paragraphs for that target.
#
# Format per entry: callable that returns a decision row, OR a string reason
# for a reject.
# ---------------------------------------------------------------------------

# We build the lookup as a list of (target_slug, section_fragment, decider)
# processed in order; first match wins.
# decider is either:
#   - a function(c) -> row
#   - the string "reject:<reason>"
#   - the string "emit:<edge_type>:<snippet>:<confidence>"
#   - the string "emit_q:<edge_type>:<qualifier>:<snippet>:<confidence>"

def classify(c):
    """Classify a single candidate dict. Returns a decision row dict."""
    slug = c["target_slug"]
    section = c.get("source_section", "")
    para = c.get("evidence_paragraph", "")
    sec = section  # shorthand

    # ------------------------------------------------------------------
    # Quotes sections: these are quote co-mentions — targets appear in
    # the body of a quote or as the quoted speaker/subject. Relationship
    # is between the quoted parties, NOT between Randyll and the target
    # directly unless a distinct typed relationship is expressed.
    # We handle quote-section candidates explicitly below where they
    # warrant edges, and reject the rest.
    # ------------------------------------------------------------------

    # =================================================================
    # Appearances & Description section
    # =================================================================
    if "Appearances & Description" in sec:
        if slug == "faith-of-the-seven":
            return emit_edge(slug, "WORSHIPS",
                             "Randyll follows the Faith of the Seven.",
                             sec)
        if slug == "heartsbane":
            return emit_edge(slug, "WIELDS",
                             "He carries the ancestral Valyrian steel sword Heartsbane across his back.",
                             sec)
        if slug == "valyrian-steel":
            # Heartsbane is the artifact; valyrian-steel is the material.
            # The edge goes to heartsbane, not to valyrian-steel as a material.
            return reject(slug, "valyrian-steel is the material of Heartsbane — "
                                "WIELDS edge targets the artifact (heartsbane), not the material")
        if slug == "steel":
            return reject(slug, "generic material mention — no-fitting-type-vocab-locked")
        if slug == "jewelry":
            return reject(slug, "jeweled scabbard — incidental material detail, no typed edge")
        if slug == "household-knight":
            return reject(slug, "title mention for Hyle Hunt — not a Randyll→title edge; "
                                "reject as no-fitting-type-vocab-locked")
        if slug == "hyle-hunt":
            return emit_edge(slug, "COMMANDS",
                             "Ser Hyle Hunt is one of his household knights and captains.",
                             sec)
        if slug == "mace-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "A careful tactician always in the van of his liege, Lord Mace Tyrell.",
                             sec, qualifier="bannerman")
        if slug == "stannis-baratheon":
            return reject(slug, "Stannis mentioned as having assessed Randyll's generalship — "
                                "temporal-cooccurrence-not-relational; no direct edge here")
        if slug == "kevan-lannister":
            return reject(slug, "Kevan mentioned as praising Randyll — "
                                "temporal-cooccurrence-not-relational")
        if slug == "seven-kingdoms":
            return reject(slug, "Seven Kingdoms appears as geographic context — just-mention")
        if slug == "oldtown":
            return reject(slug, "Oldtown as setting context — just-mention")
        # Fallback for description section
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # Origins section
    # =================================================================
    if sec == "## Origins":
        if slug == "alester-florent":
            return emit_edge(slug, "IN_LAW_OF",
                             "Randyll married Lady Melessa Florent, the eldest daughter of Alester Florent.",
                             sec, qualifier="father_in_law", confidence_tier=1)
        if slug == "283-ac":
            return reject(slug, "283 AC is a year-date node — no typed edge from Randyll; "
                                "temporal context for Sam's birth")
        if slug == "lord-of-brightwater-keep":
            return reject(slug, "title held by Alester Florent — not a Randyll→title edge; "
                                "no-fitting-type-vocab-locked")
        if slug == "battle-of-ashford":
            return emit_edge(slug, "FIGHTS_IN",
                             "He defeated Lord Robert Baratheon's forces at the Battle of Ashford, "
                             "cutting down Lord Cafferen with Heartsbane during the battle.",
                             sec, confidence_tier=1)
        if slug == "roberts-rebellion":
            return emit_edge(slug, "FIGHTS_IN",
                             "As one of Lord Mace Tyrell's bannermen, Randyll fought in Robert's Rebellion "
                             "on the side of House Targaryen.",
                             sec, confidence_tier=1)
        if slug == "heartsbane":
            return emit_edge(slug, "WIELDS",
                             "cutting down Lord Cafferen with Heartsbane during the battle.",
                             sec, confidence_tier=1)
        if slug == "house-targaryen":
            return emit_edge(slug, "ALLIES_WITH",
                             "Randyll fought in Robert's Rebellion on the side of House Targaryen.",
                             sec, confidence_tier=1)
        if slug == "lord-cafferen":
            return emit_edge(slug, "KILLS",
                             "cutting down Lord Cafferen with Heartsbane during the battle.",
                             sec, confidence_tier=1)
        if slug == "mace-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "As one of Lord Mace Tyrell's bannermen, Randyll fought in Robert's Rebellion.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "robert-i-baratheon":
            return emit_edge(slug, "DEFEATS",
                             "He defeated Lord Robert Baratheon's forces at the Battle of Ashford.",
                             sec, confidence_tier=1)
        if slug == "nights-watch":
            # Randyll forced Sam into the Night's Watch — this is Sam's membership,
            # not Randyll's. The source slug is Randyll; there is no typed
            # Randyll→Night's Watch edge here.
            return reject(slug, "Night's Watch as institution Sam was forced to join — "
                                "edge belongs to Sam (MEMBER_OF), not Randyll; "
                                "temporal-cooccurrence-not-relational")
        if slug == "arbor":
            return reject(slug, "Randyll brought Sam to the Arbor for a visit — "
                                "temporal location context, no permanent residence edge; "
                                "no-fitting-type-vocab-locked")
        if slug == "highgarden":
            return reject(slug, "Randyll brought Sam to Highgarden for a visit — "
                                "travel context, no permanent residence; no-fitting-type-vocab-locked")
        if slug == "citadel":
            return reject(slug, "Randyll sent Sam to Oldtown/Citadel instead of leaving him at the Arbor — "
                                "destination for Sam, not a Randyll relationship; temporal-cooccurrence-not-relational")
        if slug == "maester":
            return reject(slug, "maester title mentioned as path not taken for Sam — "
                                "no-fitting-type-vocab-locked")
        if slug == "paxter-redwyne":
            return reject(slug, "Paxter Redwyne mentioned as potential host for Sam — "
                                "prospective relationship, no edge realized; no-fitting-type-vocab-locked")
        if slug == "horas-redwyne":
            return reject(slug, "Horas mentioned as mocking Sam — third-party co-mention; "
                                "no direct Randyll→Horas edge; temporal-cooccurrence-not-relational")
        if slug == "hobber-redwyne":
            return reject(slug, "Hobber mentioned as mocking Sam — third-party co-mention; "
                                "no direct Randyll→Hobber edge; temporal-cooccurrence-not-relational")
        if slug == "house-redwyne":
            return reject(slug, "House Redwyne mentioned as host-candidate for Sam — "
                                "indirect context; no-fitting-type-vocab-locked")
        if slug == "oldtown":
            return reject(slug, "Oldtown as destination for Sam's Citadel training — "
                                "Sam's location, not Randyll's; temporal-cooccurrence-not-relational")
        if slug == "the-song-of-the-seven":
            return reject(slug, "Randyll forbade Sam from singing the song — "
                                "no typed edge between Randyll and the text; no-fitting-type-vocab-locked")
        if slug == "hyle-hunt":
            return reject(slug, "Hyle Hunt mentioned in same section — co-mention only; "
                                "the COMMANDS edge is already established from Appearances section")
        if slug == "aurochs":
            return reject(slug, "aurochs mentioned as physical comparison for Dickon — "
                                "no Randyll→aurochs typed edge; no-fitting-type-vocab-locked")
        if slug == "warlocks":
            return reject(slug, "warlocks of Qarth mentioned as threats Randyll warned about — "
                                "narrative aside, no direct edge; temporal-cooccurrence-not-relational")
        if slug == "qarth":
            return reject(slug, "Qarth mentioned as distant threat context — just-mention")
        if slug == "wall":
            return reject(slug, "The Wall as Sam's destination after NW induction — "
                                "Sam's travel, not Randyll's; temporal-cooccurrence-not-relational")
        # Fallback
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # A Game of Thrones narrative section
    # =================================================================
    if "A Game of Thrones" in sec:
        if slug == "castle-black":
            return reject(slug, "Castle Black as Sam's destination — Sam's location; "
                                "temporal-cooccurrence-not-relational")
        if slug == "wall":
            return reject(slug, "The Wall as Sam's destination — Sam's location; "
                                "temporal-cooccurrence-not-relational")
        if slug == "nights-watch":
            # Randyll forced Sam to join the NW — this is the relationship
            # but the edge is Sam→NW (MEMBER_OF), not Randyll→NW.
            # There's no good Randyll→NW edge here; the action is coercion of Sam.
            return reject(slug, "Night's Watch as institution Sam was forced to join — "
                                "edge belongs to Sam (MEMBER_OF), not Randyll; "
                                "temporal-cooccurrence-not-relational")
        if slug == "jon-snow":
            return reject(slug, "Jon Snow mentioned as Sam's friend at Castle Black — "
                                "no direct Randyll→Jon edge; temporal-cooccurrence-not-relational")
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # A Clash of Kings narrative section
    # =================================================================
    if "A Clash of Kings" in sec:
        if slug == "renly-baratheon":
            return emit_edge(slug, "ALLIES_WITH",
                             "When Renly Baratheon calls his banners, Randyll joins with House Tyrell "
                             "in supporting Renly.",
                             sec, confidence_tier=1)
        if slug == "house-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "Randyll joins with House Tyrell in supporting Renly.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "brienne-tarth":
            return emit_edge(slug, "ENCOUNTERS",
                             "Randyll summons Brienne and tells her that some of the men laid wagers "
                             "on the first to claim her maidenhead, tersely advising her to go home.",
                             sec, confidence_tier=1)
        if slug == "catelyn-stark":
            return emit_edge(slug, "ENCOUNTERS",
                             "Randyll accompanies Renly's army to Bitterbridge, and he meets Catelyn Stark "
                             "when she arrives during the melee at Bitterbridge.",
                             sec, confidence_tier=1)
        if slug == "house-florent":
            return emit_edge(slug, "IN_LAW_OF",
                             "He puts a great many men to death, mainly those sworn to House Florent, "
                             "his wife's family.",
                             sec, qualifier="wifes_house", confidence_tier=1)
        if slug == "mace-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "As one of Lord Mace Tyrell's bannermen, Randyll fought on the side of "
                             "House Targaryen.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "tywin-lannister":
            return reject(slug, "Tywin mentioned as the lord Randyll was sent to find — "
                                "coordinating movement, no direct command/service relationship established here; "
                                "temporal-cooccurrence-not-relational")
        if slug == "mathis-rowan":
            return emit_edge(slug, "ALLIES_WITH",
                             "Randyll and Lord Mathis Rowan discuss tactics for the upcoming battle.",
                             sec, confidence_tier=2)
        if slug == "battle-of-the-blackwater":
            return emit_edge(slug, "COMMANDS_IN",
                             "Lord Tarly joins with the Lannisters and fights against Stannis, "
                             "commanding the center at the Battle of the Blackwater.",
                             sec, confidence_tier=1)
        if slug == "fighting-at-bitterbridge":
            return emit_edge(slug, "FIGHTS_IN",
                             "He captures Renly's stores and puts a great many men to death in "
                             "fighting at Bitterbridge.",
                             sec, confidence_tier=1)
        if slug == "melee-at-bitterbridge":
            return reject(slug, "melee-at-bitterbridge is a tournament; Randyll accompanies Renly's "
                                "army there but does not participate in the melee itself — "
                                "temporal-cooccurrence-not-relational")
        if slug == "stannis-baratheon":
            return emit_edge(slug, "OPPOSES",
                             "Randyll continues to follow the Tyrells in forsaking Stannis's cause, "
                             "commanding the center against Stannis at the Battle of the Blackwater.",
                             sec, confidence_tier=1)
        if slug == "siege-of-storms-end-299":
            # Randyll counseled attacking, but Renly was assassinated before the battle took place.
            # Randyll never fought in this siege — it was never joined.
            return reject(slug, "siege-of-storms-end never took place — Renly was assassinated before "
                                "battle was joined; temporal-cooccurrence-not-relational")
        if slug == "house-lannister":
            return emit_edge(slug, "ALLIES_WITH",
                             "Lord Tarly joins with the Lannisters and fights against Stannis.",
                             sec, confidence_tier=1)
        if slug == "bastard":
            return reject(slug, "bastard title mentioned in Stannis's letter — political context; "
                                "no-fitting-type-vocab-locked")
        if slug == "bitterbridge":
            return reject(slug, "Bitterbridge as location of military actions — "
                                "LOCATED_AT could apply but is repetitive with the battle edges; "
                                "no-fitting-type-vocab-locked")
        if slug == "highgarden":
            return reject(slug, "Highgarden as location where Randyll was encamped — "
                                "passing location context, no permanent residence; "
                                "no-fitting-type-vocab-locked")
        if slug == "great-hall-red-keep":
            return reject(slug, "Randyll honored in the throne room after the Blackwater — "
                                "setting for ceremony; no-fitting-type-vocab-locked")
        if slug == "tumblers-falls":
            return reject(slug, "Tumbler's Falls as assembly point — location context; "
                                "no-fitting-type-vocab-locked")
        if slug == "robert-i-baratheon":
            return reject(slug, "Robert mentioned as historical defeated foe — prior-events context "
                                "already captured by DEFEATS edge in Origins section; "
                                "temporal-cooccurrence-not-relational")
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # A Storm of Swords narrative section
    # =================================================================
    if "A Storm of Swords" in sec:
        if slug == "battle-at-duskendale":
            return emit_edge(slug, "COMMANDS_IN",
                             "Randyll destroys a northern force attacking the town of Duskendale.",
                             sec, confidence_tier=1)
        if slug == "harrion-karstark":
            return emit_edge(slug, "CAPTURES",
                             "resulting in the capture of Harrion Karstark.",
                             sec, confidence_tier=1)
        if slug == "robett-glover":
            return emit_edge(slug, "CAPTURES",
                             "resulting in the capture of Robett Glover.",
                             sec, confidence_tier=1)
        if slug == "helman-tallhart":
            return emit_edge(slug, "KILLS",
                             "resulting in the death of Helman Tallhart.",
                             sec, confidence_tier=2)
        if slug == "william-mooton":
            return emit_edge(slug, "IMPRISONS",
                             "locks Lord William Mooton of Maidenpool in a tower.",
                             sec, confidence_tier=1)
        if slug == "renfred-rykker":
            return emit_edge(slug, "ALLIES_WITH",
                             "he takes the town of Maidenpool with Lord Renfred Rykker.",
                             sec, confidence_tier=1)
        if slug == "maidenpool":
            return emit_edge(slug, "RULES",
                             "he takes the town of Maidenpool and secures it.",
                             sec, confidence_tier=1)
        if slug == "duskendale":
            return reject(slug, "Duskendale as battle location — already captured by battle edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "kingsroad":
            return reject(slug, "kingsroad secured — strategic objective, no typed edge to road entity; "
                                "no-fitting-type-vocab-locked")
        if slug == "north":
            return reject(slug, "northern force as opponent — general faction context, "
                                "no direct Randyll→North edge warranted here; "
                                "temporal-cooccurrence-not-relational")
        if slug == "arwyn-oakheart":
            return reject(slug, "Arwyn Oakheart mentioned as co-recipient of land grants — "
                                "co-mention in ceremony; no direct Randyll→Arwyn edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "leyton-hightower":
            return reject(slug, "Leyton Hightower mentioned as co-recipient of land grants — "
                                "co-mention; no direct Randyll→Leyton edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "bastard":
            return reject(slug, "bastard mentioned in Stannis letter context — "
                                "no-fitting-type-vocab-locked")
        if slug == "gilly":
            return reject(slug, "Gilly mentioned as prospective ward at Horn Hill — "
                                "Sam's plan for Gilly, not a realized Randyll→Gilly relationship; "
                                "temporal-cooccurrence-not-relational")
        if slug == "monster":
            return reject(slug, "Gilly's son mentioned as prospective ward — "
                                "Sam's plan, not realized; temporal-cooccurrence-not-relational")
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # A Feast for Crows narrative section
    # =================================================================
    if "A Feast for Crows" in sec:
        if slug == "heartsbane":
            return emit_edge(slug, "WIELDS",
                             "He beheads outlaws with Heartsbane; and defeated Lord Cafferen "
                             "with Heartsbane at Ashford.",
                             sec, confidence_tier=1)
        if slug == "hyle-hunt":
            return emit_edge(slug, "COMMANDS",
                             "Randyll sends Ser Hyle Hunt, one of his captains, to follow Brienne.",
                             sec, confidence_tier=1)
        if slug == "brienne-tarth":
            return emit_edge(slug, "ENCOUNTERS",
                             "Brienne encounters Lord Tarly while he is dispensing harsh justice "
                             "in the fishmarket of Maidenpool.",
                             sec, confidence_tier=1)
        if slug == "sansa-stark":
            return reject(slug, "Sansa mentioned as target of Brienne's search — "
                                "indirect context; no direct Randyll→Sansa relationship here; "
                                "temporal-cooccurrence-not-relational")
        if slug == "brotherhood-without-banners":
            return emit_edge(slug, "OPPOSES",
                             "Lord Tarly is hunting outlaws from Maidenpool; "
                             "Jack-Be-Lucky says Lord Tarly has hanged a score of his comrades.",
                             sec, confidence_tier=1)
        if slug == "brave-companions":
            return reject(slug, "Brave Companions mentioned as former affiliation of outlaws Brienne killed — "
                                "no direct Randyll→Brave Companions edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "pyg":
            return reject(slug, "Pyg killed by Brienne, not by Randyll — "
                                "no direct Randyll→Pyg relationship; "
                                "temporal-cooccurrence-not-relational")
        if slug == "timeon":
            return reject(slug, "Timeon killed by Brienne, not by Randyll — "
                                "no direct Randyll→Timeon relationship; "
                                "temporal-cooccurrence-not-relational")
        if slug == "shagwell":
            return reject(slug, "Shagwell killed by Brienne, not by Randyll — "
                                "no direct Randyll→Shagwell relationship; "
                                "temporal-cooccurrence-not-relational")
        if slug == "dick-crabb":
            return reject(slug, "Dick Crabb mentioned as person Hyle helped bury — "
                                "no direct Randyll→Dick Crabb edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "jack-be-lucky":
            return reject(slug, "Jack-Be-Lucky is a Brotherhood member who mentions Randyll — "
                                "no direct Randyll→Jack-Be-Lucky edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "elder-brother-quiet-isle":
            return reject(slug, "Elder Brother mentions Randyll's activities — "
                                "informant in Brienne's quest, no direct Randyll relationship; "
                                "temporal-cooccurrence-not-relational")
        if slug == "quiet-isle":
            return reject(slug, "Quiet Isle as setting for Brienne's journey — "
                                "just-mention location")
        if slug == "margaery-tyrell":
            return emit_edge(slug, "GUARDS",
                             "The Faith releases Margaery and her cousins into his custody after "
                             "Lord Tarly swears a holy oath to return them for trial.",
                             sec, confidence_tier=1)
        if slug == "kings-landing":
            return reject(slug, "King's Landing as destination/capital context — "
                                "no-fitting-type-vocab-locked")
        if slug == "tommen-baratheon":
            return emit_edge(slug, "SERVES",
                             "Randyll dispenses justice in Maidenpool as lord of the region "
                             "under King Tommen's authority, representing the crown's law.",
                             sec, confidence_tier=2)
        if slug == "hand-of-the-king":
            return emit_edge(slug, "CLAIMS",
                             "Randyll and Lord Mathis Rowan are suggested as candidates to replace "
                             "Tywin Lannister as Hand of the King; Cersei refuses.",
                             sec, confidence_tier=2)
        if slug == "cersei-lannister":
            return reject(slug, "Cersei mentioned as refusing to appoint Randyll Hand — "
                                "political context, no direct Randyll→Cersei typed edge here; "
                                "temporal-cooccurrence-not-relational")
        if slug == "kevan-lannister":
            return reject(slug, "Kevan mentioned as suggesting Randyll for Hand — "
                                "Kevan as actor, not a Randyll→Kevan edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "tywin-lannister":
            return reject(slug, "Tywin mentioned as the late Hand Randyll could replace — "
                                "reference context; temporal-cooccurrence-not-relational")
        if slug == "mathis-rowan":
            return emit_edge(slug, "ALLIES_WITH",
                             "Randyll and Lord Mathis Rowan are suggested as co-candidates for Hand.",
                             sec, confidence_tier=2)
        if slug == "house-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "As one of Lord Mace Tyrell's bannermen, Randyll fought on the side of "
                             "House Targaryen.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "mace-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "Randyll's army reaches King's Landing before his liege lord, Mace Tyrell.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "faith-of-the-seven":
            return emit_edge(slug, "WORSHIPS",
                             "Lord Tarly swears a holy oath to return Margaery for trial.",
                             sec, confidence_tier=1)
        if slug == "eleanor-mooton":
            return emit_edge(slug, "MARRIES_OFF",
                             "His son Dickon is to marry Eleanor Mooton, the daughter of the "
                             "pardoned Lord William.",
                             sec, confidence_tier=1)
        if slug == "house-mooton":
            return emit_edge(slug, "NEGOTIATES_WITH",
                             "Randyll pardons Lord William Mooton and arranges the marriage of "
                             "Dickon to Eleanor Mooton.",
                             sec, confidence_tier=1)
        if slug == "oathkeeper":
            return reject(slug, "Oathkeeper mentioned as Brienne's sword that Randyll comments on — "
                                "no Randyll→Oathkeeper ownership/wields edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "valyrian-steel":
            return reject(slug, "Valyrian steel as material of Heartsbane — "
                                "material detail; WIELDS edge targets the artifact")
        if slug == "gilly":
            return reject(slug, "Gilly mentioned as Sam's plan — "
                                "prospective ward not realized in this context; "
                                "temporal-cooccurrence-not-relational")
        if slug == "wall":
            return reject(slug, "Wall mentioned as Sam's assignment — "
                                "Sam's location; temporal-cooccurrence-not-relational")
        if slug == "oldtown":
            return reject(slug, "Oldtown as Citadel destination for Sam — "
                                "Sam's location; temporal-cooccurrence-not-relational")
        if slug == "citadel":
            return reject(slug, "Citadel as Sam's destination — "
                                "Sam's institution; temporal-cooccurrence-not-relational")
        if slug == "arbor":
            return reject(slug, "Arbor as location from Sam's childhood — "
                                "historical location context; temporal-cooccurrence-not-relational")
        if slug == "paxter-redwyne":
            return reject(slug, "Paxter Redwyne mentioned as former potential host for Sam — "
                                "historical context; temporal-cooccurrence-not-relational")
        if slug == "horas-redwyne":
            return reject(slug, "Horas Redwyne mentioned as Sam's childhood tormentor — "
                                "no direct Randyll→Horas edge; temporal-cooccurrence-not-relational")
        if slug == "hobber-redwyne":
            return reject(slug, "Hobber Redwyne mentioned as Sam's childhood tormentor — "
                                "no direct Randyll→Hobber edge; temporal-cooccurrence-not-relational")
        if slug == "house-redwyne":
            return reject(slug, "House Redwyne mentioned as host of Sam's failed fosterage — "
                                "historical context; no-fitting-type-vocab-locked")
        if slug == "highgarden":
            return reject(slug, "Highgarden as location of Mace visit — "
                                "historical visit; no-fitting-type-vocab-locked")
        if slug == "renly-baratheon":
            return emit_edge(slug, "ALLIES_WITH",
                             "Randyll joins with House Tyrell in supporting Renly.",
                             sec, confidence_tier=1)
        if slug == "currency":
            return reject(slug, "currency/stags mentioned as fine amount — "
                                "incidental economic detail; no-fitting-type-vocab-locked")
        if slug == "sept":
            return reject(slug, "sept mentioned as location from which a thief stole — "
                                "just-mention location")
        if slug == "whispers":
            return reject(slug, "Whispers as location of Brienne's fight — "
                                "Brienne's location; temporal-cooccurrence-not-relational")
        if slug == "helman-tallhart":
            return reject(slug, "Helman Tallhart already covered in A Storm of Swords section; "
                                "this is same paragraph repeated — duplicate; "
                                "temporal-cooccurrence-not-relational")
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # A Dance with Dragons narrative section
    # =================================================================
    if "A Dance with Dragons" in sec:
        if slug == "mace-tyrell":
            return emit_edge(slug, "SWORN_TO",
                             "Randyll's army reaches King's Landing before his liege lord, Mace Tyrell.",
                             sec, qualifier="bannerman", confidence_tier=1)
        if slug == "margaery-tyrell":
            return emit_edge(slug, "GUARDS",
                             "The Faith releases Margaery and her cousins into his custody after "
                             "Lord Tarly swears a holy oath to return them for trial.",
                             sec, confidence_tier=1)
        if slug == "faith-of-the-seven":
            return emit_edge(slug, "WORSHIPS",
                             "Lord Tarly swears a holy oath before the Faith.",
                             sec, confidence_tier=1)
        if slug == "kevan-lannister":
            return reject(slug, "Kevan mentioned as suggesting Randyll for Hand — "
                                "Kevan as actor; temporal-cooccurrence-not-relational")
        if slug == "cersei-lannister":
            return reject(slug, "Cersei refuses to name Randyll Hand — "
                                "political context, no direct typed edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "hand-of-the-king":
            return emit_edge(slug, "CLAIMS",
                             "Randyll and Lord Mathis Rowan are suggested as candidates to replace "
                             "Tywin Lannister as Hand of the King.",
                             sec, confidence_tier=2)
        if slug == "mathis-rowan":
            return emit_edge(slug, "ALLIES_WITH",
                             "Randyll and Lord Mathis Rowan are suggested as co-candidates for Hand.",
                             sec, confidence_tier=2)
        if slug == "small-council":
            return reject(slug, "small council mentioned as awarding land grants — "
                                "institutional body issuing rewards; no-fitting-type-vocab-locked")
        if slug == "house-targaryen":
            return reject(slug, "House Targaryen mentioned as the pretender's claimed lineage — "
                                "historical context; temporal-cooccurrence-not-relational")
        if slug == "aegon-targaryen-young-griff":
            return reject(slug, "Randyll expresses doubts about Aegon's identity — "
                                "DISTRUSTS possible but Randyll has no direct relationship to Young Griff; "
                                "political assessment context only; temporal-cooccurrence-not-relational")
        if slug == "jon-connington":
            return reject(slug, "Randyll expresses doubts about Jon Connington's identity — "
                                "political assessment; no direct Randyll→JonCon edge warranted; "
                                "temporal-cooccurrence-not-relational")
        if slug == "ronnet-connington":
            return reject(slug, "Randyll suggests sending Ronnet to the Wall — "
                                "political suggestion, no direct Randyll→Ronnet edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "taking-of-griffins-roost":
            return reject(slug, "taking of Griffin's Roost as news context — "
                                "Randyll not a participant; temporal-cooccurrence-not-relational")
        if slug == "landing-of-the-golden-company":
            return reject(slug, "landing of Golden Company as news context — "
                                "Randyll not a participant; temporal-cooccurrence-not-relational")
        if slug == "kingsguard":
            return reject(slug, "Kingsguard mentioned in context of Cersei/Tyrell alliance — "
                                "institutional reference; no-fitting-type-vocab-locked")
        if slug == "arys-oakheart":
            return reject(slug, "Arys Oakheart mentioned as a Kingsguard member in alliance context — "
                                "no direct Randyll→Arys edge; temporal-cooccurrence-not-relational")
        if slug == "robert-strong":
            return reject(slug, "Robert Strong (reanimated Mountain) mentioned in Cersei's trial context — "
                                "no direct Randyll→Robert Strong edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "sparrows":
            return reject(slug, "Sparrows/Faith Militant mentioned as political context — "
                                "institutional context; no-fitting-type-vocab-locked")
        if slug == "tommen-baratheon":
            return emit_edge(slug, "SERVES",
                             "Randyll commands forces in King's Landing and dispenses justice "
                             "under King Tommen's authority.",
                             sec, confidence_tier=2)
        if slug == "wall":
            return reject(slug, "Wall mentioned as proposed destination for Ronnet — "
                                "Randyll's suggestion for others; temporal-cooccurrence-not-relational")
        if slug == "hyle-hunt":
            return reject(slug, "Hyle Hunt already established as commander target — "
                                "duplicate context; temporal-cooccurrence-not-relational")
        return reject(slug, "no-fitting-type-vocab-locked")

    # =================================================================
    # Quotes sections
    # Quotes are dialogue — they contain co-mentions but typically do not
    # establish direct Randyll↔target edges unless the quote itself is
    # from/to the target or describes a direct relationship.
    # =================================================================
    if "Quotes" in sec:
        # Specific quotes that do establish edges
        if slug == "brienne-tarth" and "Quotes by Randyll" in sec:
            # Direct conversation: Randyll to Brienne
            return emit_edge(slug, "ENCOUNTERS",
                             "Randyll to Brienne: The gods made men to fight, and women to bear children.",
                             sec, confidence_tier=1)
        if slug == "guyard-morrigen" and "Quotes by Randyll" in sec:
            # Direct conversation: Randyll to Guyard
            return emit_edge(slug, "ENCOUNTERS",
                             "Randyll to Guyard: I was leading Mace Tyrell's van when you were still "
                             "sucking on your mother's teat.",
                             sec, confidence_tier=1)
        if slug == "aerys-ii-targaryen" and "Quotes about Randyll" in sec:
            # Stannis mentions Randyll sent Cafferen's head to Aerys
            return emit_edge(slug, "SERVES",
                             "Randyll slew Lord Cafferen and sent his head to Aerys (King at the time).",
                             sec, confidence_tier=1)
        if slug == "dunstan-drumm" and "Quotes about Randyll" in sec:
            return reject(slug, "Dunstan Drumm speaks about Randyll — no direct Randyll→Dunstan edge; "
                                "temporal-cooccurrence-not-relational")
        if slug == "victarion-greyjoy" and "Quotes about Randyll" in sec:
            # Victarion boasts about possibly taking Randyll's sword in a future battle.
            # This is a prospective threat from Victarion's POV, not an established
            # Randyll↔Victarion opposition edge. They have not opposed each other in-text.
            return reject(slug, "Victarion's boast about fighting Randyll is prospective — "
                                "no realized opposition; temporal-cooccurrence-not-relational")
        if slug == "war-of-the-five-kings" and "Quotes about Randyll" in sec:
            return reject(slug, "War of the Five Kings mentioned in Kevan's quote praising Randyll — "
                                "context mention; no-fitting-type-vocab-locked")
        if slug == "rainbow-guard" and "Quotes by Randyll" in sec:
            return reject(slug, "rainbow cloak mentioned in taunt to Guyard (Rainbow Guard context) — "
                                "no Randyll→Rainbow Guard typed edge; no-fitting-type-vocab-locked")
        if slug == "king-in-the-north" and "Quotes by Randyll" in sec:
            return reject(slug, "king-in-the-north title mentioned in context of quote — "
                                "no direct Randyll→title edge; no-fitting-type-vocab-locked")
        if slug == "red-rain" and "Quotes about Randyll" in sec:
            return reject(slug, "Red Rain (Drumm sword) mentioned in quote comparing Valyrian steel swords — "
                                "no Randyll→Red Rain edge; temporal-cooccurrence-not-relational")
        if slug == "reach" and "Quotes about Randyll" in sec:
            return reject(slug, "reach mentioned as Randyll's territory context — just-mention region")
        # All remaining quote co-mentions: the context is narrative paragraphs
        # attached to quote sections that repeat the same evidence paragraphs
        # already handled above. These are duplicates with different section labels.
        # The underlying evidence paragraphs are the same — already handled.
        # Reject all as duplicate context.
        return reject(slug, "quote-section co-mention or repeated narrative paragraph — "
                            "relationship already captured from primary narrative section or "
                            "no direct Randyll edge; temporal-cooccurrence-not-relational")

    # =================================================================
    # Fallback for any unhandled section
    # =================================================================
    return reject(slug, "no-fitting-type-vocab-locked")


def main():
    parser = argparse.ArgumentParser(
        description="Classify prose edge candidates for randyll-tarly into typed graph edges."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results to stdout instead of writing to output file.",
    )
    args = parser.parse_args()

    if not INPUT_PATH.exists():
        print(f"ERROR: Input file not found: {INPUT_PATH}", file=sys.stderr)
        sys.exit(1)

    candidates = []
    with INPUT_PATH.open() as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARNING: Skipping malformed line {line_num}: {e}", file=sys.stderr)

    print(f"Read {len(candidates)} candidates from {INPUT_PATH.name}")

    decisions = []
    for c in candidates:
        row = classify(c)
        decisions.append(row)

    # Stats
    emit_count = sum(1 for d in decisions if d["decision"] == "emit_edge")
    reject_count = sum(1 for d in decisions if d["decision"] == "reject_just_mention")
    escalate_ci = sum(1 for d in decisions if d["decision"] == "escalate_cross_identity")
    escalate_d = sum(1 for d in decisions if d["decision"] == "escalate_disambiguation")

    if args.dry_run:
        for row in decisions:
            print(json.dumps(row))
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT_PATH.open("w") as f:
            for row in decisions:
                f.write(json.dumps(row) + "\n")
        print(f"Wrote {len(decisions)} rows to {OUTPUT_PATH}")

    print()
    print("=== Summary ===")
    print(f"  emit_edge:               {emit_count}")
    print(f"  reject_just_mention:     {reject_count}")
    print(f"  escalate_cross_identity: {escalate_ci}")
    print(f"  escalate_disambiguation: {escalate_d}")
    print(f"  Total:                   {len(decisions)}")

    # Edge type breakdown
    edge_types: dict[str, int] = {}
    for d in decisions:
        if d["decision"] == "emit_edge":
            et = d.get("edge_type", "unknown")
            edge_types[et] = edge_types.get(et, 0) + 1
    if edge_types:
        print()
        print("Edge types emitted:")
        for et, count in sorted(edge_types.items()):
            print(f"  {et}: {count}")


if __name__ == "__main__":
    main()
