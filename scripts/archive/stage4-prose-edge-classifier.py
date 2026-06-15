#!/usr/bin/env python3
"""
Stage 4 Prose-Edge Classifier — deterministic rule-based pass.

Reads enriched prose-edge-candidate JSONL files and emits one decision row
per candidate to corresponding output JSONL files.

Decision outcomes per candidate:
  - emit_edge          — concrete typed edge with evidence snippet
  - reject_just_mention — entity mentioned but no classifiable edge
  - escalate_cross_identity — source/target slugs resolve to same person
  - escalate_disambiguation — target slug is ambiguous

Key design choice:
  Classification uses the `snippet` field (200-char window centered on the
  «target» anchor) as the primary signal, NOT the full evidence_paragraph.
  The evidence_paragraph contains the broader passage shared across many
  candidates; scanning it would match text about OTHER entities in the same
  paragraph, producing false positives. The snippet faithfully reflects which
  relationship words appear directly adjacent to the target anchor.

  The evidence_paragraph is used only for: (a) building the output
  evidence_snippet, and (b) a secondary fallback for event-type targets where
  the snippet window may cut off the verb.

Vocabulary rules (Session 63/64 locked):
  - KNOWS is deprecated; never emitted.
  - ENCOUNTERS requires a staging verb (staging_verbs_present must be non-empty).
  - CONTEMPORARY_WITH is NOT used as a fallback; reject_just_mention instead.
  - ATTENDS / FIGHTS_IN / PARTICIPATES_IN must target event.* nodes.
  - Qualifier rules follow reference/edge-qualifier-vocab.md:
      Tier 1 (required): SIBLING_OF, SPOUSE_OF, PARENT_OF, WARD_OF,
                         HOLDS_TITLE, VOWS_TO, MANIPULATES, SWORN_TO
      Tier 2 (optional): BETROTHED_TO, LOVER_OF, KILLS, CONTRACTED_WITH,
                         DECEIVES, REVEALS_TO, ATTACKS, GUEST_OF, IN_LAW_OF
      Tier 3 (no qualifier field): all others — MUST NOT have qualifier

Usage:
    python3 scripts/stage4-prose-edge-classifier.py
    python3 scripts/stage4-prose-edge-classifier.py --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — input/output file pairs
# ---------------------------------------------------------------------------

BASE = Path("/Users/mnoth/source/asoiaf-chat")

FILE_PAIRS = [
    (
        BASE / "working/wiki/pass2-buckets/characters-house-payne"
              / "prose-edge-candidates-enriched/podrick-payne.candidates.jsonl",
        BASE / "working/wiki/pass2-buckets/characters-house-payne"
              / "prose-edges-haiku/podrick-payne.edges.jsonl",
    ),
    (
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edge-candidates-enriched/amaury-peake.candidates.jsonl",
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edges-haiku/amaury-peake.edges.jsonl",
    ),
    (
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edge-candidates-enriched/armen-peake.candidates.jsonl",
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edges-haiku/armen-peake.edges.jsonl",
    ),
    (
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edge-candidates-enriched/bernard.candidates.jsonl",
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edges-haiku/bernard.edges.jsonl",
    ),
    (
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edge-candidates-enriched/gedmund-peake.candidates.jsonl",
        BASE / "working/wiki/pass2-buckets/characters-house-peake"
              / "prose-edges-haiku/gedmund-peake.edges.jsonl",
    ),
]

# ---------------------------------------------------------------------------
# Qualifier vocabulary (reference/edge-qualifier-vocab.md)
# ---------------------------------------------------------------------------

# Tier 1: qualifier REQUIRED
TIER1_QUALIFIERS = {
    "SIBLING_OF":  {"full", "half", "step", "milk", "unknown"},
    "SPOUSE_OF":   {"current", "former", "annulled", "widowed", "salt_wife", "unknown"},
    "PARENT_OF":   {"biological", "adopted", "claimed", "rumored", "disputed", "unknown"},
    "WARD_OF":     {"formal", "informal", "hostage", "unknown"},
    "HOLDS_TITLE": {"current", "former", "claimed", "contested", "historical", "unknown"},
    "VOWS_TO":     {"active", "kept", "broken", "fulfilled", "unknown"},
    "MANIPULATES": {"via_bribe", "via_flattery", "via_false_information",
                    "via_threat", "via_seduction", "unknown"},
    "SWORN_TO":    {"current", "former", "deserted", "by_marriage", "claimed", "unknown"},
}

# Tier 2: qualifier OPTIONAL
TIER2_QUALIFIERS = {
    "BETROTHED_TO":    {"current", "broken", "fulfilled", "secret", "unknown"},
    "LOVER_OF":        {"current", "former", "secret", "paramour", "rumored", "unknown"},
    "KILLS":           {"in_combat", "in_duel", "by_arrow", "by_blade", "by_ambush",
                        "by_proxy", "by_creature", "unknown"},
    "CONTRACTED_WITH": {"assassination", "mercenary_service", "ransom", "safe_passage",
                        "construction", "marriage_brokerage", "espionage", "unknown"},
    "DECEIVES":        {"by_lie", "by_disguise", "by_omission", "by_false_witness",
                        "by_silence", "unknown"},
    "REVEALS_TO":      {"voluntary", "coerced", "accidental", "under_torture", "unknown"},
    "ATTACKS":         {"in_anger", "unprovoked", "in_self_defense", "on_command",
                        "by_creature", "unknown"},
    "GUEST_OF":        {"shelter", "feast", "bread_and_salt", "safe_conduct",
                        "gift_exchange", "refused", "unknown"},
    "IN_LAW_OF":       {"by_marriage_of_self", "by_marriage_of_child",
                        "by_marriage_of_sibling", "by_marriage_of_parent", "unknown"},
}

# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

_WIKI_LINK_RE = re.compile(r'\[([^\]]+)\]\(wiki:[^)]+\)')
# Match complete (wiki:...) citations AND truncated ones ending with '...' or end-of-string.
# Snippets are 200-char windows and may be cut mid-citation, leaving "(wiki:Foo.cite..." with
# no closing ')'. The second alternative strips these partial refs so they don't leak entity
# names (e.g. "podrick" in "(wiki:Podrick_Payne.cite_ref...") into the cleaned text.
_CITE_REF_RE = re.compile(r'\(wiki:[^)]*\)|\(wiki:[^)]*$|\(wiki:[^)]*\.\.\.')
_ANGLE_QUOTE_RE = re.compile(r'[«»]')


def _clean(text: str) -> str:
    """
    Strip wiki markup from snippet/paragraph text and return lowercased plain text.
    Removes: «»  [[Link|text]] style refs  (wiki:...) citation anchors
    Also strips partial/truncated (wiki:... citations that lack a closing paren.
    """
    text = _WIKI_LINK_RE.sub(r'\1', text)
    text = _CITE_REF_RE.sub('', text)
    text = _ANGLE_QUOTE_RE.sub('', text)
    return text.lower()


def _t(type_str: str) -> str:
    """Return top-level type prefix, e.g. 'character' from 'character.human'."""
    return type_str.split(".")[0] if type_str else ""


def _source_name_parts(source_slug: str) -> list:
    """
    Return lowercased name fragments from a slug for snippet presence checks.
    E.g. 'podrick-payne' → ['podrick', 'payne']
         'amaury-peake' → ['amaury', 'peake']
    Filters out very short tokens (len < 4) to avoid false matches.
    """
    return [p for p in source_slug.split("-") if len(p) >= 4]


def _source_in_snippet(source_slug: str, snippet_clean: str) -> bool:
    """
    Return True if the source entity's FIRST NAME (first slug token with len>=4)
    appears in the cleaned snippet.

    We intentionally use the FIRST name part only (not last/family name) because
    family names (e.g. 'peake') appear in the snippet for OTHER members of the
    same family, causing false positives. First names are generally unique enough
    within a paragraph window to serve as reliable presence indicators.

    If the first significant token is absent but the whole slug is very short,
    fall back to any-match.
    """
    parts = _source_name_parts(source_slug)
    if not parts:
        return True  # slug too short — be permissive
    # Use only the FIRST significant name part as the discriminating token
    # (first name of the person), not the family name
    first_name = parts[0]
    return first_name in snippet_clean


def _split_snippet_at_target(raw_snippet: str) -> tuple:
    """
    Split the raw snippet into (before_target, target_text, after_target)
    using the «...» anchor markers. Returns cleaned (lowercased, markup-stripped)
    versions of each part.

    If no «» markers found, returns (full_clean, '', '').
    """
    if "«" not in raw_snippet:
        return (_clean(raw_snippet), "", "")

    # Find the first «...» span
    start = raw_snippet.find("«")
    end = raw_snippet.find("»", start)
    if end == -1:
        return (_clean(raw_snippet), "", "")

    before = raw_snippet[:start]
    target = raw_snippet[start+1:end]
    after = raw_snippet[end+1:]
    return (_clean(before), _clean(target), _clean(after))


# ---------------------------------------------------------------------------
# Main classifier dispatch
# ---------------------------------------------------------------------------

def classify_candidate(row: dict) -> dict:
    """
    Apply deterministic classification rules to one candidate row.

    Returns a decision dict with 'decision' key set to one of:
      emit_edge, reject_just_mention, escalate_cross_identity, escalate_disambiguation

    Primary classification signal: `snippet` (200-char window around «target»).
    The snippet is far more reliable than scanning the full evidence_paragraph,
    which contains text about many other entities.
    """
    source_slug = row["source_slug"]
    target_slug = row["target_slug"]
    target_type = row.get("target_type", "")
    evidence_paragraph = row.get("evidence_paragraph", "")
    snippet = row.get("snippet", "")
    valid_types = set(row.get("valid_edge_types", []))
    staging_verbs = row.get("staging_verbs_present", [])
    candidate_kind = row.get("candidate_kind", "source_target")
    source_section = row.get("source_section", "")

    ttop = _t(target_type)

    # Hard guard: KNOWS is deprecated — never emit
    valid_types.discard("KNOWS")

    # Build clean versions of both signals
    cs = _clean(snippet)         # cleaned snippet — primary signal
    cp = _clean(evidence_paragraph)  # cleaned paragraph — secondary/fallback

    # Same-slug guard
    if source_slug == target_slug:
        return _reject(candidate_kind, source_slug, target_slug,
                       "same-slug-source-equals-target")

    # Year-slug guard: slugs matching \d+-ac or \d+-bc (e.g. "134-ac") are
    # calendar years misclassified as character nodes upstream. Kinship edges
    # to year nodes are nonsensical — reject immediately.
    _YEAR_SLUG_RE = re.compile(r'^\d+-a[bc]$|^\d+-bc$')
    if _YEAR_SLUG_RE.match(target_slug):
        return _reject(candidate_kind, source_slug, target_slug,
                       "target-is-year-not-entity")

    # Source-in-snippet guard: check whether source name appears in snippet.
    # Used by relationship types that describe a direct source↔target bond
    # (kinship, service, emotional) where false positives come from the snippet
    # describing OTHER entities' relationships.
    source_in_snip = _source_in_snippet(source_slug, cs)

    # Split snippet around the «target» anchor for directionality checks.
    # `snip_before` = text before the target anchor (source's actions toward target)
    # `snip_after`  = text after the target anchor (target's attributes/actions)
    snip_before, snip_target, snip_after = _split_snippet_at_target(snippet)

    # Dispatch by target type
    if ttop == "character":
        return _classify_character(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, staging_verbs, candidate_kind, source_section,
            source_in_snip, snip_before, snip_after
        )
    if ttop == "place":
        return _classify_place(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip
        )
    if ttop == "organization":
        return _classify_org(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip
        )
    if ttop == "event":
        return _classify_event(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip
        )
    if target_type == "title":
        return _classify_title(
            cs, cp, source_slug, target_slug, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip,
            snip_before
        )
    if ttop == "concept":
        return _classify_concept(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip
        )
    if ttop == "object":
        return _classify_object(
            cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
            valid_types, candidate_kind, source_section, source_in_snip
        )
    if target_type == "species":
        if "CULTURE_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CULTURE_OF",
                         evidence_paragraph, source_section, tier=2)
        return _reject(candidate_kind, source_slug, target_slug,
                       "no-fitting-type-vocab-locked")

    return _reject(candidate_kind, source_slug, target_slug,
                   f"unknown-target-type:{target_type}")


# ---------------------------------------------------------------------------
# Per-target-type classifiers — all operate on `cs` (cleaned snippet) primary
# ---------------------------------------------------------------------------

def _classify_character(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, staging_verbs, candidate_kind, source_section,
    source_in_snip=True, snip_before="", snip_after=""
):
    """
    Classify edges toward character.* targets using snippet as primary signal.

    source_in_snip: True if the source entity's first name appears in the snippet.
    snip_before: cleaned text appearing BEFORE the «target» anchor — used for
                 directionality checks (subject-verb-object ordering).
    snip_after:  cleaned text appearing AFTER the «target» anchor.

    Kinship and direct-relationship types guard on source_in_snip to avoid
    matching relationship words that describe OTHER entities' relationships
    within the same paragraph window.

    Directional types (KILLS, COMMANDS, PARENT_OF) additionally require the
    action verb to appear in snip_before (before the target anchor), ensuring
    the source is the AGENT of the action, not the patient or bystander.
    """

    # ENCOUNTERS: only with staging verb pre-detected by enricher
    if staging_verbs and "ENCOUNTERS" in valid_types:
        return _emit(candidate_kind, source_slug, target_slug, "ENCOUNTERS",
                     evidence_paragraph, source_section, tier=3)

    # For kinship and direct personal-relationship types, only classify when
    # the source entity appears in the snippet. If the source isn't in the
    # snippet, the relationship words describe OTHER characters' relationships
    # within the shared paragraph context.
    kin_guard = source_in_snip

    # Kinship — look in snippet for possessive pronouns or direct relationship words
    # near the target anchor. Patterns like "his brother X", "X, nephew of Y", etc.

    # Spouse: guard with source presence AND require the spouse language to appear
    # in snip_before (before the target anchor), where the source's context is set.
    # "the wife of prince «Viserys»" has "wife of" in snip_before but the subject
    # (Larra Rogare) is not the source — we need source in snip_before too.
    source_first_name = _source_name_parts(source_slug)[0] if _source_name_parts(source_slug) else ""
    spouse_in_before = _any(snip_before, "wife", "husband", "married to", "spouse of",
                             "wed to", "widow of", "wedded")
    source_in_before = (source_first_name and source_first_name in snip_before)
    if kin_guard and spouse_in_before and source_in_before:
        if "SPOUSE_OF" in valid_types:
            qual = "widowed" if "widow" in cs else "current"
            return _emit(candidate_kind, source_slug, target_slug, "SPOUSE_OF",
                         evidence_paragraph, source_section, tier=1, qualifier=qual)
        if "BETROTHED_TO" in valid_types and _any(cs, "betrothed", "promised in"):
            return _emit(candidate_kind, source_slug, target_slug, "BETROTHED_TO",
                         evidence_paragraph, source_section, tier=2, qualifier="current")

    # Parent / child — source→child: action words appear BEFORE target anchor.
    # Also require the source's first name in snip_before to confirm the source
    # is the grammatical subject of the parenting action. Without this, "Larra
    # Rogare gave birth to prince «Aegon»" would fire for Septon Bernard who is
    # also in the snippet (but merely as the anointer, not the parent).
    if kin_guard and source_in_before and _any(snip_before, "his son", "her son",
                          "his daughter", "her daughter", "his child", "her child",
                          "father of", "mother of", "fathered", "bore him", "bore her",
                          "gave birth", "sired", "bastard son", "bastard daughter"):
        if "PARENT_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PARENT_OF",
                         evidence_paragraph, source_section, tier=1,
                         qualifier="biological")

    # Parent appearing as attribute of target (target's parent is source):
    # "his father [target]" / "her mother [target]" — relationship word before anchor
    if kin_guard and _any(snip_before, "his father", "her father", "his mother",
                          "her mother", "his parent", "her parent"):
        if "PARENT_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PARENT_OF",
                         evidence_paragraph, source_section, tier=1,
                         qualifier="biological")

    # Sibling — explicit half/full forms; do NOT include "sworn brother" here
    # (sworn brother = Night's Watch / Kingsguard brotherhood, not blood kin)
    if _any(cs, "half-brother", "half brother"):
        if "SIBLING_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SIBLING_OF",
                         evidence_paragraph, source_section, tier=1, qualifier="half")
    if _any(cs, "half-sister", "half sister"):
        if "SIBLING_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SIBLING_OF",
                         evidence_paragraph, source_section, tier=1, qualifier="half")
    if kin_guard and _any(cs, " his brother", " her brother", "brother of",
                          "twin brother", "elder brother", "younger brother"):
        if "SIBLING_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SIBLING_OF",
                         evidence_paragraph, source_section, tier=1, qualifier="full")
    if kin_guard and _any(cs, " his sister", " her sister", "sister of",
                          "elder sister", "younger sister", "twin sister"):
        if "SIBLING_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SIBLING_OF",
                         evidence_paragraph, source_section, tier=1, qualifier="full")

    # Uncle / nephew / aunt / niece — require kinship language in snip_before
    # (before the target anchor) so the relationship connects source TO target.
    if kin_guard and _any(snip_before, "his uncle", "her uncle", "uncle of",
                          "his aunt", "her aunt", "aunt of"):
        if "UNCLE_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "UNCLE_OF",
                         evidence_paragraph, source_section, tier=2)
    if kin_guard and _any(snip_before, "his nephew", "her nephew", "nephew of",
                          "his niece", "her niece", "niece of"):
        if "NEPHEW_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "NEPHEW_OF",
                         evidence_paragraph, source_section, tier=2)

    # Cousin — require cousin language in snip_before to confirm the target IS
    # the cousin (not a third party mentioned after the anchor who is someone
    # else's cousin). E.g. "his cousin Bernard" appearing in snip_after means
    # the source/target relationship is mediated by a third party.
    if kin_guard and _any(snip_before, "his cousin", "her cousin", "cousin of", "their cousin"):
        if "COUSIN_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "COUSIN_OF",
                         evidence_paragraph, source_section, tier=2)

    # Betrothal — guard on source presence
    if kin_guard and _any(cs, "betrothed", "betroth", "promised in marriage",
                          "his bride", "her groom"):
        if "BETROTHED_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BETROTHED_TO",
                         evidence_paragraph, source_section, tier=2, qualifier="current")

    # Lover / paramour — guard on source presence
    if kin_guard and _any(cs, "his lover", "her lover", "his paramour", "her paramour",
                          "his mistress", "her mistress", "paramour"):
        if "LOVER_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "LOVER_OF",
                         evidence_paragraph, source_section, tier=2, qualifier="current")

    # Ward / fostered — guard on source presence
    if kin_guard and _any(cs, "his ward", "her ward", "ward of", "fostered by",
                          "raised by", "taken as ward", "taken in as ward"):
        if "WARD_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "WARD_OF",
                         evidence_paragraph, source_section, tier=1, qualifier="formal")

    # Ancestor / heir
    if kin_guard and _any(cs, "ancestor", "descended from", "descendant of"):
        if "ANCESTOR_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ANCESTOR_OF",
                         evidence_paragraph, source_section, tier=2)
    if kin_guard and _any(cs, "heir to", "his heir", "her heir", "named heir",
                          "designated heir"):
        if "HEIR_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "HEIR_TO",
                         evidence_paragraph, source_section, tier=1)

    # In-law — guard on source presence
    if kin_guard and _any(cs, "good-mother", "good-father", "good-brother",
                          "good-sister", "mother-in-law", "father-in-law",
                          "sister-in-law", "brother-in-law",
                          "son-in-law", "daughter-in-law", "good mother", "good father"):
        if "IN_LAW_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "IN_LAW_OF",
                         evidence_paragraph, source_section, tier=2, qualifier="unknown")

    # Squire / service — guard on source presence to avoid "assigned as squire to X"
    # matching when the subject is a different character.
    # Require squire language in snip_before (before the target anchor) AND
    # that the snippet does not contain dialogue denial context (e.g. "No. Not
    # that Hand.") which indicates the squire language refers to a DIFFERENT
    # target than the one anchored in the snippet.
    has_squire_before = _any(snip_before, "his squire", "her squire", "squire to",
                              "squired for", "squired to", "serves as squire",
                              "assigned as squire", "as his squire", "as her squire",
                              "i'm your squire", "i am your squire")
    denial_context = _any(cs, "no. not that", "not that hand", "no. not him",
                          "no. not her", "not that lord")
    if source_in_snip and has_squire_before and not denial_context:
        if "SERVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SERVES",
                         evidence_paragraph, source_section, tier=1)

    # All remaining character→character relationship types require source_in_snip.
    # The snippet window is centered on the TARGET; if the source entity's first name
    # isn't in that window, the relationship word describes OTHER characters'
    # relationships and we cannot safely attribute it to source→target.
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    # --- below here source_in_snip is guaranteed True ---

    # Knighthood
    if _any(cs, "knighted by", "dubbed by", "dubbing", "made a knight by",
            "received knighthood from"):
        if "KNIGHTED_BY" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "KNIGHTED_BY",
                         evidence_paragraph, source_section, tier=1)
        if "BESTOWS_KNIGHTHOOD_ON" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug,
                         "BESTOWS_KNIGHTHOOD_ON",
                         evidence_paragraph, source_section, tier=1)

    # Killing / death — kill verbs must appear BEFORE the target anchor AND
    # the source's first name must also appear in snip_before (to confirm that
    # the source is the grammatical subject of the kill, not a bystander).
    source_first = _source_name_parts(source_slug)[0] if _source_name_parts(source_slug) else ""
    source_is_killer = (source_first and source_first in snip_before)

    if source_is_killer and _any(snip_before, " killed ", " kills ", " slew ",
                                  " slain ", " slays ", "cut down", "struck down",
                                  "beheads", "beheaded", "murdered", "murders",
                                  "put to death"):
        if _any(cs, "poison", "poisons", "poisoned", "strangles") and "POISONS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "POISONS",
                         evidence_paragraph, source_section, tier=1)
        if "KILLS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "KILLS",
                         evidence_paragraph, source_section, tier=1,
                         qualifier="in_combat")
        if "EXECUTES" in valid_types and _any(snip_before, "executed", "executes"):
            return _emit(candidate_kind, source_slug, target_slug, "EXECUTES",
                         evidence_paragraph, source_section, tier=1)

    # KILLED_BY: the target killed the source (target's kill verb in snip_after)
    if _any(snip_after, " killed ", " kills ", " slew ", " slays ", "executed",
            "put to death", "murdered"):
        if "KILLED_BY" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "KILLED_BY",
                         evidence_paragraph, source_section, tier=1)

    # Executes (formal, source in snip_before as agent)
    if source_is_killer and _any(snip_before, "executed", "executes",
                                  "put to death", "beheaded"):
        if "EXECUTES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "EXECUTES",
                         evidence_paragraph, source_section, tier=1)

    # Commands — source name + command verb must both appear in snip_before
    if source_is_killer and _any(snip_before, " commands ", "commanded",
                                  "lord commander of"):
        if "COMMANDS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "COMMANDS",
                         evidence_paragraph, source_section, tier=2)

    # Advises
    if _any(cs, "advises", "adviser", "advisor", "counsel", "counseled",
            "counselor", "advised by"):
        if "ADVISES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ADVISES",
                         evidence_paragraph, source_section, tier=2)

    # Appointed
    if _any(cs, "appointed by", "appointed him", "appointed her", "named by",
            "elevated by", "elevated to"):
        if "APPOINTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "APPOINTS",
                         evidence_paragraph, source_section, tier=1)

    # Sworn to / fealty
    if _any(cs, "sworn to", "swore fealty", "pledged fealty", "allegiance to"):
        if "SWORN_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SWORN_TO",
                         evidence_paragraph, source_section, tier=1,
                         qualifier="current")

    # Serves (generic — after squire-specific check above).
    # Do NOT trigger on "hand's" (possessive) — that means the source is squire
    # to the Hand, not that the source holds the Hand role.
    if _any(cs, "in service", " serves ", " served ", "serving", "in the service of",
            "into the service of", "passes into the service",
            "maester of", "septa of", "captain of the guard"):
        if "SERVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SERVES",
                         evidence_paragraph, source_section, tier=1)
    # "hand of the king" as a SERVES trigger: only when "hand of" is not possessive.
    # "the hand's squire" → do not emit SERVES toward the Hand.
    if "hand of" in cs and "hand's" not in cs and "hand of the" in cs:
        if "SERVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SERVES",
                         evidence_paragraph, source_section, tier=1)

    # Protection / rescue / guarding — rescue verb must be in snip_before
    # AND source must be in snip_before (source is the grammatical agent)
    source_agent = (source_first and source_first in snip_before)
    if source_agent and _any(snip_before, "protects", "protected", "defends",
                             "defended"):
        if "PROTECTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PROTECTS",
                         evidence_paragraph, source_section, tier=2)
    if source_agent and _any(snip_before, "rescues", "rescued", "saves",
                             "saved from"):
        if "RESCUES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "RESCUES",
                         evidence_paragraph, source_section, tier=2)
    if source_agent and _any(snip_before, " guards ", "guarded", "guarding"):
        if "GUARDS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "GUARDS",
                         evidence_paragraph, source_section, tier=3)

    # Capture / prisoner
    if _any(cs, "captured", "takes prisoner", "taken prisoner",
            "taken captive", "as prisoner"):
        if "CAPTURES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CAPTURES",
                         evidence_paragraph, source_section, tier=1)
        if "PRISONER_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PRISONER_OF",
                         evidence_paragraph, source_section, tier=1)

    # Emotional / perceptual
    if _any(cs, " trusts ", "trusted by", "has faith in"):
        if "TRUSTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TRUSTS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "distrusts", "suspicious of", "does not trust", "distrust"):
        if "DISTRUSTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "DISTRUSTS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, " fears ", " feared ", "afraid of", "terrified of"):
        if "FEARS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "FEARS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, " loves ", " loved ", "his love", "her love", "deeply cares"):
        if "LOVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "LOVES",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, " hates ", " hated ", "loathes", "despises", "enmity"):
        if "HATES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "HATES",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "mourns", "mourned", "grieves for"):
        if "MOURNS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "MOURNS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "respects", "respected", "holds in high regard"):
        if "RESPECTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "RESPECTS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "resents", "resentment toward", "bitterness toward"):
        if "RESENTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "RESENTS",
                         evidence_paragraph, source_section, tier=2)

    # Alliance / opposition
    if _any(cs, "allies with", "allied with", "formed alliance"):
        if "ALLIES_WITH" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ALLIES_WITH",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, " opposes ", " opposed ", "at odds with", "enemy of", "enemies of"):
        if "OPPOSES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "OPPOSES",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "betrays", "betrayed", "broke faith with"):
        if "BETRAYS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BETRAYS",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "conspires with", "conspired with", "secret plot", "plotted together",
            "in league with"):
        if "CONSPIRES_WITH" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CONSPIRES_WITH",
                         evidence_paragraph, source_section, tier=3)

    # Companion / travel
    if _any(cs, "close companion", "good friend", "sworn friend", "companion of"):
        if "COMPANION_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "COMPANION_OF",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "traveled with", "travels with", "journeyed with", "accompanied",
            "in company of", "in his party", "in her party", "retinue"):
        if "TRAVELS_WITH" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TRAVELS_WITH",
                         evidence_paragraph, source_section, tier=3)

    # Teaching
    if _any(cs, "tutored by", "trained by", "tutors", "training under",
            "studied under", "mentored by"):
        if "TUTORS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TUTORS",
                         evidence_paragraph, source_section, tier=2)
        if "TEACHES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TEACHES",
                         evidence_paragraph, source_section, tier=2)

    # Duel / attack
    if _any(cs, " duels ", "dueled", "duel with", "single combat"):
        if "DUELS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "DUELS",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, " attacks ", " attacked ", "assaults", "assaulted", "charges"):
        if "ATTACKS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ATTACKS",
                         evidence_paragraph, source_section, tier=1, qualifier="unknown")

    # Deception / manipulation
    if _any(cs, "deceives", "deceived", "lied to", "misled"):
        if "DECEIVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "DECEIVES",
                         evidence_paragraph, source_section, tier=2, qualifier="by_lie")
    if _any(cs, "manipulates", "manipulated"):
        if "MANIPULATES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "MANIPULATES",
                         evidence_paragraph, source_section, tier=2, qualifier="unknown")

    # Vows / oaths
    if _any(cs, "vowed to", "swore an oath", "swore to", "made a vow"):
        if "VOWS_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "VOWS_TO",
                         evidence_paragraph, source_section, tier=1, qualifier="active")

    # Banish / exile
    if _any(cs, "banished", "banishes", "exiled", "exiles", "cast out"):
        if "BANISHES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BANISHES",
                         evidence_paragraph, source_section, tier=1)

    # Torture / imprison
    if _any(cs, "tortures", "tortured", "flayed", "flaying", "racked"):
        if "TORTURES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TORTURES",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "imprisoned", "imprisons", "locked away", "thrown in cells"):
        if "IMPRISONS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "IMPRISONS",
                         evidence_paragraph, source_section, tier=1)

    # Information / reveals — source reveals TO target.
    # Require the reveal verb in snip_before (the source acts toward the target)
    # OR in the full snippet for passive forms. Do NOT emit on "tells him/her"
    # in snip_after — that means the TARGET is telling the SOURCE (wrong direction).
    _reveals_in_before = _any(snip_before, "reveals", "revealed", "disclosed",
                               "tells", "informed", "confesses", "confessed")
    _reveals_in_after = _any(snip_after, "tells him", "tells her", "told him",
                              "told her", "informed him", "informed her",
                              "tells podrick", "told podrick")
    if _reveals_in_before and not _reveals_in_after:
        if "REVEALS_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "REVEALS_TO",
                         evidence_paragraph, source_section, tier=2, qualifier="voluntary")

    # Seeks
    if _any(cs, " seeks ", " seeking ", "hunts for", "in search of", "searched for"):
        if "SEEKS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SEEKS",
                         evidence_paragraph, source_section, tier=2)

    # Negotiates
    if _any(cs, "negotiated with", "negotiates with", "parleyed"):
        if "NEGOTIATES_WITH" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "NEGOTIATES_WITH",
                         evidence_paragraph, source_section, tier=2)

    # Spies
    if _any(cs, "spies on", "spied on", "surveils"):
        if "SPIES_ON" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SPIES_ON",
                         evidence_paragraph, source_section, tier=3)

    # Heals
    if _any(cs, "healed", " heals ", "treated", "tended", "nursed back"):
        if "HEALS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "HEALS",
                         evidence_paragraph, source_section, tier=2)

    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


def _classify_place(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True
):
    """
    Classify edges toward place.* targets.
    Source-presence guard on all types except LOCATED_AT broad fallback,
    which is intentionally permissive (presence in context implies location).
    However, even LOCATED_AT requires source_in_snip to avoid attributing
    location to a character merely mentioned in passing.
    """
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    if _any(cs, "born in", "born at", "birthplace", "was born"):
        if "BORN_AT" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BORN_AT",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "died at", "died in", "death at", "killed at",
            "killed in", "fell at", "died near"):
        if "DIED_AT" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "DIED_AT",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "buried at", "buried in", "interred at", "tomb at",
            "tomb in", "crypt at", "crypt of"):
        if "BURIED_AT" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BURIED_AT",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "imprisoned at", "imprisoned in", "held at", "held in",
            "locked in", "locked away in", "confined to", "confined in"):
        if "IMPRISONED_AT" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "IMPRISONED_AT",
                         evidence_paragraph, source_section, tier=3)
    if _any(cs, "traveled to", "travels to", "journeyed to", "rode to",
            "sailed to", "went to", "fled to", "marched to", "proceeded to",
            "arrived at", "arrived in", "returned to", "departed for"):
        if "TRAVELS_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "TRAVELS_TO",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, " rules ", " ruled ", "lord of", "lady of", "king of", "queen of",
            "holds dominion", "seat of rule"):
        if "RULES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "RULES",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "besieges", "besieged", "laid siege to"):
        if "BESIEGES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BESIEGES",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, " built ", "constructed", "oversaw construction", "had built"):
        if "BUILT" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "BUILT",
                         evidence_paragraph, source_section, tier=1)
    # Generic location presence — broad fallback for place targets
    if "LOCATED_AT" in valid_types:
        return _emit(candidate_kind, source_slug, target_slug, "LOCATED_AT",
                     evidence_paragraph, source_section, tier=3)
    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


def _classify_org(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True
):
    """
    Classify edges toward organization.* targets.
    No broad fallback — requires explicit membership/service language.
    """
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    if _any(cs, "member of", "joined", "joins", "belongs to",
            "sworn member"):
        if "MEMBER_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "MEMBER_OF",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "founded", "established", "created", "formed"):
        if "FOUNDED" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "FOUNDED",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, " commands ", "commanded", " led ", " leads ", "lord commander",
            "general of"):
        if "COMMANDS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "COMMANDS",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, " rules ", " ruled ", "lord of", "lady of", "king of", "queen of",
            "head of"):
        if "RULES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "RULES",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "advises", "adviser", "advisor", "counsel", "counselor"):
        if "ADVISES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ADVISES",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "sworn to", "fealty to", "allegiance to", "vassal of"):
        if "SWORN_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SWORN_TO",
                         evidence_paragraph, source_section, tier=1,
                         qualifier="current")
    if _any(cs, "overlord of", "overlord over"):
        if "OVERLORD_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "OVERLORD_OF",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, " opposes ", " opposed ", "enemy of", "against"):
        if "OPPOSES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "OPPOSES",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "allies with", "allied with", "alliance with"):
        if "ALLIES_WITH" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ALLIES_WITH",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "worships", "worshipped", "follower of", "devout", "prays to"):
        if "WORSHIPS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "WORSHIPS",
                         evidence_paragraph, source_section, tier=2)
    if _any(cs, "clergy of", "septon of", "septa of", "high priest", "red priest"):
        if "CLERGY_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CLERGY_OF",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "cadet branch", "junior branch"):
        if "CADET_BRANCH_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CADET_BRANCH_OF",
                         evidence_paragraph, source_section, tier=1)
    if _any(cs, "appointed to", "named to", "elevated to"):
        if "APPOINTS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "APPOINTS",
                         evidence_paragraph, source_section, tier=1)
    # Serves — generic pattern for org targets (no broad fallback)
    if _any(cs, " serves ", " served ", "in service", "serving", "hand of",
            "maester of", "septa of"):
        if "SERVES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SERVES",
                         evidence_paragraph, source_section, tier=2)
    # NOTE: No MEMBER_OF fallback here. A generic org mention in context is not
    # sufficient evidence of membership. Require explicit membership language.
    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


def _classify_event(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True
):
    """
    Classify edges toward event.* targets. Uses both snippet and paragraph.

    For events, the snippet window often cuts off the action verb, so we also
    check the full paragraph (cp) as secondary signal. However, ALL checks
    require source_in_snip — if the source entity's name does not appear in the
    snippet window, the event is merely mentioned in surrounding context and we
    cannot reliably attribute participation to the source.

    Example false positive without this guard: "While preparing for the
    «second siege of Meereen», Tyrion Lannister recalls that Podrick had been
    sleeping before the battle on the Green Fork." — Podrick is named in the
    sentence but wasn't at Meereen. source_in_snip will be True (snippet
    mentions Podrick), but the participation language is about another character,
    and the sentence explicitly says it is a *recall* — not direct participation.
    The guard plus requiring explicit participation verbs in snippet handles this.
    """
    # All event checks require source in snippet.
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    # Guard: if the event anchor is surrounded by recollection/memory language,
    # the source is not a direct participant.
    # Two patterns handled:
    #   (a) "[3rd party] recalls that «event»..." — recollection verb in snip_before
    #   (b) "...«event», [3rd party] recalls that [source] had..." — recollection
    #       verb in snip_after, source is the object of the recollection
    # For (b): split the raw snippet at the «target» anchor to get snip_after.
    _raw_snip = snippet if 'snippet' in dir() else ""  # fallback
    # Recompute snip_after from cs by splitting on target name
    _ev_target_words = target_slug.replace("-", " ")
    if _ev_target_words in cs:
        _ev_parts = cs.split(_ev_target_words, 1)
        _ev_snip_before_local = _ev_parts[0]
        _ev_snip_after_local = _ev_parts[1] if len(_ev_parts) > 1 else ""
    else:
        _ev_snip_before_local = cs
        _ev_snip_after_local = ""
    if _any(_ev_snip_before_local, "recalls that", "recalled that", "remembers that",
            "recollects that", "dreamed of", "thought about"):
        return _reject(candidate_kind, source_slug, target_slug,
                       "event-in-recollection-not-direct-participation")
    # Pattern (b): "«event», [3rd party] recalls that [source]..."
    source_first_ev = _source_name_parts(source_slug)[0] if _source_name_parts(source_slug) else ""
    if _any(_ev_snip_after_local, "recalls that", "recalled that", "remembers that"):
        # The source appearing AFTER the recollection verb = object of memory, not participant
        if source_first_ev and source_first_ev in _ev_snip_after_local:
            after_recall = _ev_snip_after_local.split("recalls that", 1)[-1] if "recalls that" in _ev_snip_after_local else ""
            if source_first_ev in after_recall:
                return _reject(candidate_kind, source_slug, target_slug,
                               "event-in-recollection-not-direct-participation")

    # Use combined signal but prefer snippet for explicit participation language.
    combined = cs + " " + cp

    # Tier 1: explicit participation verbs in snippet (not just paragraph fallback)
    if _any(cs, "fought in", "fought at", "fighting in", "fought during",
            "took part in battle", "joined the battle", "participated in the battle",
            "insists upon accompanying", "accompanies", "accompanying"):
        if "FIGHTS_IN" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "FIGHTS_IN",
                         evidence_paragraph, source_section, tier=1)

    # Combined check (snippet + paragraph) for explicitly participation verbs
    if _any(combined, "fought in", "fought at", "fighting in",
            "took part in battle", "joined the battle", "participated in the battle",
            "in the battle", "during the battle"):
        if "FIGHTS_IN" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "FIGHTS_IN",
                         evidence_paragraph, source_section, tier=1)

    if _any(combined, " commanded ", " commanded in ", " led the ", " led forces",
            "general at", "commanded forces"):
        if "COMMANDS_IN" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "COMMANDS_IN",
                         evidence_paragraph, source_section, tier=1)

    if _any(combined, "attended", " attends ", "present at", "witnessed",
            "guest at", "spectator", "observed the"):
        if "ATTENDS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "ATTENDS",
                         evidence_paragraph, source_section, tier=2)

    if _any(combined, "officiated", "officiates", "performed the ceremony",
            "conducted the", "presided over"):
        if "OFFICIATES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "OFFICIATES",
                         evidence_paragraph, source_section, tier=1)

    if _any(combined, "participated in", "participates in", "took part in",
            "played a role in"):
        if "PARTICIPATES_IN" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PARTICIPATES_IN",
                         evidence_paragraph, source_section, tier=2)

    if _any(combined, "part of", "component of", "campaign of", "phase of"):
        if "PART_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PART_OF",
                         evidence_paragraph, source_section, tier=1)

    # Tournament-specific
    if target_type == "event.tournament":
        if _any(combined, "jousted", "competed", "rode in the", "entered"):
            if "FIGHTS_IN" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "FIGHTS_IN",
                             evidence_paragraph, source_section, tier=2)

    # Broad fallback: source_in_snip already guaranteed above.
    # Guard: if a family-member possessive ("podrick's father", "podrick's mother",
    # etc.) appears BEFORE the event anchor in the snippet, the event participation
    # belongs to the family member, not the source. Reject.
    _ev_target_words2 = target_slug.replace("-", " ")
    if _ev_target_words2 in cs:
        _ev_before2 = cs.split(_ev_target_words2, 1)[0]
    else:
        _ev_before2 = cs
    source_first2 = _source_name_parts(source_slug)[0] if _source_name_parts(source_slug) else ""
    source_possessive = source_first2 + "'s" if source_first2 else ""
    if source_possessive and _any(_ev_before2,
                                   source_possessive + " father",
                                   source_possessive + " mother",
                                   source_possessive + " brother",
                                   source_possessive + " sister",
                                   source_possessive + " uncle",
                                   source_possessive + " son",
                                   source_possessive + " daughter"):
        return _reject(candidate_kind, source_slug, target_slug,
                       "event-participation-via-family-member-not-source")

    if "FIGHTS_IN" in valid_types and _any(cp, "battle", "war", "siege",
                                           "rebellion", "conflict"):
        return _emit(candidate_kind, source_slug, target_slug, "FIGHTS_IN",
                     evidence_paragraph, source_section, tier=3)
    if "PARTICIPATES_IN" in valid_types:
        return _emit(candidate_kind, source_slug, target_slug, "PARTICIPATES_IN",
                     evidence_paragraph, source_section, tier=3)
    if "ATTENDS" in valid_types:
        return _emit(candidate_kind, source_slug, target_slug, "ATTENDS",
                     evidence_paragraph, source_section, tier=3)

    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


def _classify_title(
    cs, cp, source_slug, target_slug, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True,
    snip_before=""
):
    """
    Classify edges toward title targets.

    HOLDS_TITLE is only emitted when the source entity appears in the snippet,
    because title-type nodes appear frequently in shared paragraph context
    without the source entity holding that title.
    """
    if "HOLDS_TITLE" in valid_types and source_in_snip:
        # Guard: title appears in possessive form (e.g. "the Hand's squire") means
        # the source serves the title-holder, not that the source holds the title.
        target_base = target_slug.split("-")[0]  # e.g. "hand" from "hand-of-the-king"
        if (target_base + "'s") in cs or (target_base + "’s") in cs:
            return _reject(candidate_kind, source_slug, target_slug,
                           "title-possessive-not-held")

        # Guard: third-party subject before the title anchor means the title
        # belongs to someone else (e.g. "his father was a «squire»").
        source_first = _source_name_parts(source_slug)[0] if _source_name_parts(source_slug) else ""
        third_party_title = _any(snip_before, "his father", "her father", "his mother",
                                  "her mother", "her husband", "his wife", "his brother",
                                  "his uncle", "her uncle", "his son", "her son",
                                  "had allied with the", "allied with the",
                                  "the wife of", "the husband of")
        if third_party_title:
            return _reject(candidate_kind, source_slug, target_slug,
                           "title-belongs-to-third-party")

        # Guard: source must be in snip_before OR the snippet contains explicit
        # title-holding language. Without one of these, the title is merely
        # mentioned near the source (e.g. "Gedmund remained ... the Archon of
        # Tyrosh [who allied with Racallio]") and the source doesn't hold it.
        source_in_snip_before = source_first and source_first in snip_before
        explicit_holding = _any(cs, " is the ", " was the ", " as the ", " named the ",
                                 " appointed the ", " served as ", " became the ",
                                 "lord commander", "i'm your", "i am your",
                                 "i'm his", "i am his", "not for a ")
        if not source_in_snip_before and not explicit_holding:
            return _reject(candidate_kind, source_slug, target_slug,
                           "title-source-not-linked-to-title")

        # Determine qualifier from snippet
        if _any(cs, "former", "formerly", "stripped of", "lost the title"):
            qual = "former"
        elif _any(cs, "claimed", "pretender", "claimant", "self-styled"):
            qual = "claimed"
        elif _any(cs, "historical", "once", "ancient"):
            qual = "historical"
        else:
            qual = "current"
        return _emit(candidate_kind, source_slug, target_slug, "HOLDS_TITLE",
                     evidence_paragraph, source_section, tier=1, qualifier=qual)
    if source_in_snip and _any(cs, "heir", "successor to", "inherits"):
        if "HEIR_TO" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "HEIR_TO",
                         evidence_paragraph, source_section, tier=2)
    if source_in_snip and _any(cs, "succeeded", "succeeds", "replaced"):
        if "SUCCEEDS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "SUCCEEDS",
                         evidence_paragraph, source_section, tier=2)
    # Title mentioned only as context (source not in snippet, or no fitting pattern)
    return _reject(candidate_kind, source_slug, target_slug,
                   "title-context-only")


def _classify_concept(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True
):
    """
    Classify edges toward concept.* targets.
    Requires source_in_snip for medical/magic/prophecy to avoid attributing
    conditions/practices to the source when the snippet describes someone else.
    """
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    if target_type == "concept.culture":
        if "CULTURE_OF" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "CULTURE_OF",
                         evidence_paragraph, source_section, tier=1)
    if target_type == "concept.magic":
        if "PRACTICES" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "PRACTICES",
                         evidence_paragraph, source_section, tier=2)
    if target_type == "concept.medical":
        combined = cs + " " + cp
        if _any(combined, "died of", "death from", "killed by disease",
                "succumbed", "died from"):
            if "DIED_OF" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "DIED_OF",
                             evidence_paragraph, source_section, tier=1)
        if "AFFLICTED_BY" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "AFFLICTED_BY",
                         evidence_paragraph, source_section, tier=1)
    if target_type == "concept.prophecy":
        if "SUBJECT_OF_PROPHECY" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug,
                         "SUBJECT_OF_PROPHECY",
                         evidence_paragraph, source_section, tier=2)
        if "APPEARS_TO_FULFILL" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug,
                         "APPEARS_TO_FULFILL",
                         evidence_paragraph, source_section, tier=3)
    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


def _classify_object(
    cs, cp, source_slug, target_slug, target_type, evidence_paragraph,
    valid_types, candidate_kind, source_section, source_in_snip=True
):
    """Classify edges toward object.* targets."""
    if not source_in_snip:
        return _reject(candidate_kind, source_slug, target_slug,
                       "source-not-in-snippet-reject")

    if target_type == "object.artifact":
        if _any(cs, "wields", "wielded", "bears", "bore", "carries", "carried",
                "brandishes"):
            if "WIELDS" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "WIELDS",
                             evidence_paragraph, source_section, tier=1)
        if _any(cs, "gifted", "given as gift", "presented with"):
            if "GIFTED_TO" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "GIFTED_TO",
                             evidence_paragraph, source_section, tier=2)
        if _any(cs, "inherited", "inherits", "passed down"):
            if "INHERITED_BY" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "INHERITED_BY",
                             evidence_paragraph, source_section, tier=2)
        if _any(cs, "captain of", "captained", "commands the ship"):
            if "CAPTAIN_OF" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "CAPTAIN_OF",
                             evidence_paragraph, source_section, tier=1)
        if "OWNS" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "OWNS",
                         evidence_paragraph, source_section, tier=3)
    if target_type == "object.text":
        if _any(cs, "wrote", "written by", "authored", "composed"):
            if "WRITTEN_BY" in valid_types:
                return _emit(candidate_kind, source_slug, target_slug, "WRITTEN_BY",
                             evidence_paragraph, source_section, tier=1)
        if "DEPICTED_IN" in valid_types:
            return _emit(candidate_kind, source_slug, target_slug, "DEPICTED_IN",
                         evidence_paragraph, source_section, tier=2)
    # food / material — no person→food/material edge in schema
    return _reject(candidate_kind, source_slug, target_slug,
                   "no-fitting-type-vocab-locked")


# ---------------------------------------------------------------------------
# Helper: contains-any substring check
# ---------------------------------------------------------------------------

def _any(text: str, *phrases: str) -> bool:
    """Return True if any of the phrases appears in text (case-already-lowered)."""
    return any(p in text for p in phrases)


# ---------------------------------------------------------------------------
# Output row builders
# ---------------------------------------------------------------------------

def _snippet(evidence_paragraph: str, min_len: int = 10, max_len: int = 200) -> str:
    """
    Extract a verbatim snippet from evidence_paragraph, 10-200 chars.
    Strips «» wiki anchor markers but preserves all other text verbatim.
    """
    text = evidence_paragraph.strip()
    text = text.replace("«", "").replace("»", "")
    if len(text) <= max_len:
        return text
    # Truncate at word boundary near max_len
    truncated = text[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > min_len:
        truncated = truncated[:last_space]
    return truncated


def _emit(candidate_kind: str, source_slug: str, target_slug: str,
          edge_type: str, evidence_paragraph: str, evidence_section: str,
          tier: int, qualifier=None) -> dict:
    """Build an emit_edge decision row with correct qualifier tier handling."""
    row: dict = {
        "decision": "emit_edge",
        "candidate_kind": candidate_kind,
        "evidence_kind": "wiki-entity",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "edge_type": edge_type,
        "evidence_snippet": _snippet(evidence_paragraph),
        "evidence_section": evidence_section,
        "confidence_tier": tier,
    }

    # Qualifier enforcement
    if edge_type in TIER1_QUALIFIERS:
        # Required: use provided or fall back to "unknown"
        if qualifier is not None and qualifier in TIER1_QUALIFIERS[edge_type]:
            row["qualifier"] = qualifier
        else:
            row["qualifier"] = "unknown"
    elif edge_type in TIER2_QUALIFIERS:
        # Optional: include only if valid
        if qualifier is not None and qualifier in TIER2_QUALIFIERS[edge_type]:
            row["qualifier"] = qualifier
        # else: omit — Tier 2 permits missing qualifier
    # Tier 3: no qualifier field — never add one

    return row


def _reject(candidate_kind: str, source_slug: str, target_slug: str,
            reason: str) -> dict:
    """Build a reject_just_mention decision row."""
    return {
        "decision": "reject_just_mention",
        "candidate_kind": candidate_kind,
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(input_path: Path, output_path: Path, dry_run: bool) -> dict:
    """Read input JSONL, classify each candidate, write output JSONL."""
    if not input_path.exists():
        print(f"  [WARN] Input not found: {input_path}", file=sys.stderr)
        return {"input": str(input_path), "error": "file-not-found"}

    candidates = []
    with open(input_path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"  [WARN] JSON parse error at line {lineno} of "
                      f"{input_path.name}: {exc}", file=sys.stderr)

    decisions = [classify_candidate(row) for row in candidates]

    counts: dict = {}
    for d in decisions:
        key = d["decision"]
        counts[key] = counts.get(key, 0) + 1

    if not dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            for d in decisions:
                fh.write(json.dumps(d, ensure_ascii=False) + "\n")

    return {
        "input": input_path.name,
        "output": output_path.name,
        "total": len(decisions),
        "counts": counts,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Stage 4 prose-edge classifier — deterministic rule-based pass."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Classify but do not write output files."
    )
    args = parser.parse_args()

    if args.dry_run:
        print("[dry-run] Classifying without writing output files.\n")

    all_stats = []
    for input_path, output_path in FILE_PAIRS:
        stats = process_file(input_path, output_path, dry_run=args.dry_run)
        all_stats.append(stats)

    print()
    print("=" * 70)
    print("Stage 4 Prose-Edge Classifier — Summary")
    print("=" * 70)

    total_candidates = 0
    total_emitted = 0
    total_rejected = 0
    total_escalated = 0

    for s in all_stats:
        if "error" in s:
            print(f"  [ERROR] {s['input']}: {s['error']}")
            continue

        counts = s["counts"]
        emitted = counts.get("emit_edge", 0)
        rejected = counts.get("reject_just_mention", 0)
        escalated = (counts.get("escalate_cross_identity", 0)
                     + counts.get("escalate_disambiguation", 0))

        total_candidates += s["total"]
        total_emitted += emitted
        total_rejected += rejected
        total_escalated += escalated

        parts = []
        if emitted:
            parts.append(f"{emitted} emit_edge")
        if rejected:
            parts.append(f"{rejected} reject_just_mention")
        if escalated:
            parts.append(f"{escalated} escalate")

        suffix = f" → {s['output']}" if not args.dry_run else ""
        print(f"  [done] {s['input']!s} → {', '.join(parts)}{suffix}")

    print()
    print(f"  Total candidates : {total_candidates}")
    print(f"  Emitted edges    : {total_emitted}")
    print(f"  Rejected         : {total_rejected}")
    print(f"  Escalated        : {total_escalated}")
    print("=" * 70)


if __name__ == "__main__":
    main()
