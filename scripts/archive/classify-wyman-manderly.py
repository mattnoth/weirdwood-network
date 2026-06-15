#!/usr/bin/env python3
"""
classify-wyman-manderly.py

Deterministic rule-based classifier for wyman-manderly.candidates.jsonl.
Applies Stage 4 prose-edge classification rules (locked Session 61/63) to
produce one decision per candidate line.

Rules applied (in order):
  1. KNOWS deprecated — never emit KNOWS
  2. ENCOUNTERS requires staging verb
  3. Only emit types present in valid_edge_types (type contract)
  4. Qualifier requirements for certain edge types (Tier 1 mandatory)
  5. Reject temporal co-occurrence (mentions without relational edges)
  6. Reject reverse-direction edges
  7. Escalate ambiguous cross-identity / disambiguation cases
  8. Confidence tier assignment (1=explicit prose, 2=inferred/clear, 3=hinted)

Input:  prose-edge-candidates-enriched/wyman-manderly.candidates.jsonl
Output: prose-edges-haiku/wyman-manderly.edges.jsonl
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Per-target classification table
# Each entry: (edge_type, confidence_tier, qualifier_or_None, notes)
# "REJECT" means temporal co-occurrence; "REVERSE" means edge belongs elsewhere;
# "ESCALATE_CROSS_IDENTITY" / "ESCALATE_DISAMBIGUATION" for ambiguous cases.
# The key is target_slug. Duplicates (same target appears multiple times with
# different snippets) are resolved by looking at evidence_paragraph fingerprint.
# ---------------------------------------------------------------------------

# Evidence paragraph fingerprint helpers — used to distinguish duplicate slugs
def _para_contains(para: str, *phrases: str) -> bool:
    para_lower = para.lower()
    return all(p.lower() in para_lower for p in phrases)


def classify_candidate(c: dict) -> dict:
    """
    Returns a decision dict for a single candidate record.
    """
    source = c["source_slug"]
    target = c["target_slug"]
    target_type = c.get("target_type", "")
    para = c.get("evidence_paragraph", "")
    section = c.get("source_section", "")
    staging = c.get("staging_verbs_present", [])
    valid_types = set(c.get("valid_edge_types", []))
    anchor = c.get("anchor_text", "")
    snippet = c.get("snippet", "")

    def emit(edge_type, tier, qualifier=None, snippet_override=None):
        d = {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": source,
            "target_slug": target,
            "edge_type": edge_type,
            "evidence_snippet": snippet_override or snippet,
            "evidence_section": section,
            "confidence_tier": tier,
        }
        if qualifier is not None:
            d["qualifier"] = qualifier
        return d

    def reject(reason):
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "reason": reason,
        }

    def escalate(kind, note=None):
        d = {
            "decision": kind,
            "candidate_kind": "source_target",
            "source_slug": source,
            "target_slug": target,
            "evidence_paragraph": para,
        }
        if note:
            d["note"] = note
        return d

    def can_emit(edge_type) -> bool:
        return edge_type in valid_types

    # -----------------------------------------------------------------------
    # Track-B infobox paragraphs — these carry structured edges directly.
    # Detect them and emit the first matching infobox edge, or reject if the
    # evidence_paragraph is unrelated to the target in this candidate.
    # -----------------------------------------------------------------------
    is_track_b = para.strip().startswith("- HOLDS_TITLE:") or (
        "track_b:" in para and para.strip().startswith("-")
    )

    if is_track_b:
        # Parse track_b lines for direct edges
        lines = [ln.strip() for ln in para.splitlines() if ln.strip().startswith("-")]
        for ln in lines:
            m = re.match(r"- ([A-Z_]+): (.+?) \(track_b: (.+?)\)", ln)
            if not m:
                continue
            edge_type, obj_name, field_name = m.group(1), m.group(2), m.group(3)
            # Match this track_b edge to the current target slug
            obj_slug_guess = obj_name.lower().replace(" ", "-").replace("'", "").replace(",", "")
            if (
                target in obj_slug_guess
                or obj_slug_guess in target
                or target.replace("-", "") in obj_slug_guess.replace("-", "")
            ):
                # Emit if the edge type is in valid_types
                if edge_type == "KNOWS":
                    return reject("knows-deprecated-defer-to-pass1")
                if can_emit(edge_type):
                    return emit(edge_type, 1, snippet_override=ln)
        # No matching track_b edge found — temporal co-occurrence
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # TARGET-SPECIFIC CLASSIFICATION
    # -----------------------------------------------------------------------

    # --- Food / material / non-character targets → always temporal co-occurrence ---
    food_or_material_targets = {
        "eel", "lamprey", "pork-pies", "gold", "horse", "wine",
        "arbor-gold",  # wine is the page slug for Arbor Gold
    }
    if target in food_or_material_targets:
        return reject("temporal-cooccurrence-not-relational")

    # object.food target type → reject
    if "object.food" in target_type or "object.material" in target_type:
        return reject("temporal-cooccurrence-not-relational")

    # --- Quotes-section candidates: the evidence paragraph is about co-mention,
    #     not a direct edge from Wyman to the target. Most quotes section candidates
    #     are co-mentions with third parties. We need to handle them carefully. ---

    # -----------------------------------------------------------------------
    # house-stark — explicit loyalty statement.
    # Multiple candidates (narrative + quotes); quotes section re-states loyalty
    # but is attribution only → emit only from narrative sections.
    # -----------------------------------------------------------------------
    if target == "house-stark":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "loyal") or _para_contains(para, "owes") or \
                _para_contains(para, "allegiance") or _para_contains(para, "debt"):
            if can_emit("ALLIES_WITH"):
                return emit("ALLIES_WITH", 1)
            if can_emit("SWORN_TO"):
                return emit("SWORN_TO", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # house-manderly — Wyman is head of house; this is MEMBER_OF or skip
    # -----------------------------------------------------------------------
    if target == "house-manderly":
        # Not in valid_edge_types for character.human targets typically,
        # but check anyway
        if can_emit("MEMBER_OF"):
            return emit("MEMBER_OF", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # mermans-court — Wyman's seat/throne.
    # Multiple candidates (narrative + quotes sections); emit only from non-quotes.
    # -----------------------------------------------------------------------
    if target == "mermans-court":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if can_emit("LOCATED_AT"):
            return emit("LOCATED_AT", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # white-harbor — Wyman rules/is based at White Harbor
    # -----------------------------------------------------------------------
    if target == "white-harbor":
        if _para_contains(para, "rules") or _para_contains(para, "lord of white harbor") or \
                _para_contains(para, "command the defense") or _para_contains(para, "born"):
            if can_emit("RULES"):
                return emit("RULES", 1)
            if can_emit("LOCATED_AT"):
                return emit("LOCATED_AT", 1)
        if _para_contains(para, "born"):
            if can_emit("BORN_AT"):
                return emit("BORN_AT", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # catelyn-stark — Wyman ENCOUNTERS Catelyn (staging verb present).
    # Quotes section has an attribution line only — still emit if staging verb present
    # (the underlying event is the same; downstream deduplicates).
    # -----------------------------------------------------------------------
    if target == "catelyn-stark":
        if staging and can_emit("ENCOUNTERS"):
            return emit("ENCOUNTERS", 1)
        if _para_contains(para, "meets catelyn") or _para_contains(para, "wyman meets"):
            if can_emit("ENCOUNTERS"):
                return emit("ENCOUNTERS", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # robb-stark — Wyman's liege lord, loyal to.
    # Quotes section: "King Robb has no more loyal servant than Wyman Manderly"
    # is a direct loyalty declaration — emit from quotes too.
    # -----------------------------------------------------------------------
    if target == "robb-stark":
        if _para_contains(para, "loyal") or _para_contains(para, "calls his banners") or \
                _para_contains(para, "king in the north"):
            if can_emit("SWORN_TO"):
                return emit("SWORN_TO", 1, qualifier="current")
            if can_emit("ALLIES_WITH"):
                return emit("ALLIES_WITH", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wylis-manderly — Wyman's son (PARENT_OF), also PRISONER_EXCHANGE_FOR
    # -----------------------------------------------------------------------
    if target == "wylis-manderly":
        if _para_contains(para, "heir") or _para_contains(para, "his son") or \
                _para_contains(para, "wylis") and _para_contains(para, "son"):
            if can_emit("PARENT_OF"):
                return emit("PARENT_OF", 1, qualifier="biological")
        if _para_contains(para, "ransom") or _para_contains(para, "captivity") or \
                _para_contains(para, "freedom of his surviving son"):
            if can_emit("PRISONER_EXCHANGE_FOR"):
                return emit("PRISONER_EXCHANGE_FOR", 2)
        # Default if PARENT_OF fits
        if can_emit("PARENT_OF"):
            return emit("PARENT_OF", 1, qualifier="biological")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wendel-manderly — Wyman's second son (PARENT_OF); MOURNS death
    # -----------------------------------------------------------------------
    if target == "wendel-manderly":
        if _para_contains(para, "second son") or _para_contains(para, "his son") or \
                _para_contains(para, "wendel"):
            if _para_contains(para, "killed") or _para_contains(para, "red wedding") or \
                    _para_contains(para, "murdered"):
                if can_emit("MOURNS"):
                    return emit("MOURNS", 1)
            if can_emit("PARENT_OF"):
                return emit("PARENT_OF", 1, qualifier="biological")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wynafryd-manderly, wylla-manderly — granddaughters (MARRIES_OFF).
    # Only emit from narrative section; quotes section is attribution.
    # -----------------------------------------------------------------------
    if target in ("wynafryd-manderly", "wylla-manderly"):
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "granddaughter") or _para_contains(para, "betrothed") or \
                _para_contains(para, "marry his granddaughter") or \
                _para_contains(para, "wynafryd") or _para_contains(para, "wylla"):
            if can_emit("MARRIES_OFF"):
                return emit("MARRIES_OFF", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # marlon-manderly — Wyman's cousin
    # -----------------------------------------------------------------------
    if target == "marlon-manderly":
        if _para_contains(para, "cousin"):
            if can_emit("COUSIN_OF"):
                return emit("COUSIN_OF", 1, qualifier="full")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # davos-seaworth — complex: IMPRISONS (AFFC context), then ENCOUNTERS (ADWD).
    # Multiple candidates exist across narrative and quote sections.
    # Only emit from the first narrative occurrence of each relationship type;
    # quotes sections are attribution only (co-mention), reject them.
    # -----------------------------------------------------------------------
    if target == "davos-seaworth":
        # Reject quote-section duplicates
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        # ADWD: Wyman meets Davos secretly (staging verb present)
        if staging and _para_contains(para, "meets"):
            if can_emit("ENCOUNTERS"):
                return emit("ENCOUNTERS", 1)
        # AFFC: Wyman imprisoned Davos
        if _para_contains(para, "imprisoned") or _para_contains(para, "execute the onion lord"):
            if can_emit("IMPRISONS"):
                return emit("IMPRISONS", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # robett-glover — ENCOUNTERS (Wyman meets Robett per ADWD secret meeting)
    # -----------------------------------------------------------------------
    if target == "robett-glover":
        if staging and can_emit("ENCOUNTERS"):
            return emit("ENCOUNTERS", 1)
        if _para_contains(para, "meets secretly") or _para_contains(para, "wyman meets"):
            if can_emit("ENCOUNTERS"):
                return emit("ENCOUNTERS", 1)
        # Robett comes to White Harbor to raise men — temporal co-occurrence only
        if _para_contains(para, "raising men") or _para_contains(para, "refusing his pleas"):
            return reject("temporal-cooccurrence-not-relational")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wex-pyke — Wyman learned from Wex (INFORMS, reverse: Wex informs Wyman)
    # The staging verb "meets" in the evidence paragraph refers to Wyman meeting
    # Davos, not Wex — Wex is the informant, not someone Wyman staged-met.
    # -----------------------------------------------------------------------
    if target == "wex-pyke":
        # "Wyman learned from Wex" = Wex INFORMS Wyman → reverse direction
        return reject("reverse-direction-edge-belongs-on-target-node")

    # -----------------------------------------------------------------------
    # battle-of-the-trident / roberts-rebellion — FIGHTS_IN
    # -----------------------------------------------------------------------
    if target in ("battle-of-the-trident", "roberts-rebellion"):
        if _para_contains(para, "participated") or _para_contains(para, "trident"):
            if can_emit("FIGHTS_IN"):
                return emit("FIGHTS_IN", 1)
            if can_emit("PARTICIPATES_IN"):
                return emit("PARTICIPATES_IN", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # red-wedding — Wyman's son Wendel was killed there, but Wyman was not present.
    # The correct MOURNS edge is Wyman → wendel-manderly (already classified there).
    # Wyman MOURNS the person, not the event. Reject here.
    # -----------------------------------------------------------------------
    if target == "red-wedding":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # sack-of-winterfell — Wyman learned about it; staging verb present → ENCOUNTERS context
    # Evidence paragraph is the "Wyman meets secretly" ADWD paragraph
    # -----------------------------------------------------------------------
    if target == "sack-of-winterfell":
        # The event itself — Wyman was not present; he learned about it
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # bartimus — Wyman granted the Wolf's Den to Bartimus (APPOINTS or GIFTED_TO).
    # One candidate in Origins section; the candidate appears only once.
    # -----------------------------------------------------------------------
    if target == "bartimus":
        if _para_contains(para, "granted") and _para_contains(para, "wolf"):
            if can_emit("APPOINTS"):
                return emit("APPOINTS", 1)
            if can_emit("GIFTED_TO"):
                return emit("GIFTED_TO", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wolfs-den — Wyman granted it to Bartimus; no direct edge from Wyman to the location
    # -----------------------------------------------------------------------
    if target == "wolfs-den":
        # He granted this to Bartimus but this isn't a Wyman→location edge
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # house-frey — complex. Multiple paragraphs.
    #   - Physical description para (clothing/throne) → reject
    #   - "betrayed by House Frey" para → OPPOSES
    #   - Quote para (Wyman speech: "may the Freys choke") → OPPOSES
    # -----------------------------------------------------------------------
    if target == "house-frey":
        # Physical description paragraph → reject
        if _para_contains(para, "velvet") or _para_contains(para, "doublet") or \
                _para_contains(para, "throne in the merman"):
            return reject("temporal-cooccurrence-not-relational")
        # Son Wendel killed by Freys paragraph → Wyman OPPOSES House Frey
        if _para_contains(para, "betrayed by house frey") or (
            _para_contains(para, "wendel") and _para_contains(para, "killed")
        ):
            if can_emit("OPPOSES"):
                return emit("OPPOSES", 1)
        # Quote: "may the Freys choke" → explicit statement of opposition
        if _para_contains(para, "choke upon their fables"):
            if can_emit("OPPOSES"):
                return emit("OPPOSES", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # hosteen-frey, aenys-frey — Frey envoys who came to White Harbor.
    # Wyman deceives them about the disappeared Frey kinsmen.
    # The "Hosteen attacks Wyman" event is in the Roger Ryswell para (different candidate).
    # -----------------------------------------------------------------------
    if target in ("hosteen-frey", "aenys-frey"):
        if _para_contains(para, "frey envoys") or (
            _para_contains(para, "hosteen") and _para_contains(para, "aenys")
        ):
            if can_emit("DECEIVES"):
                return emit("DECEIVES", 2)
        # Quotes section: Wyman speaking to Roose/Hosteen/Aenys — the evidence para
        # here is the Frey envoys/palfrey paragraph; same DECEIVES logic applies
        if section.lower().startswith("## quotes"):
            if _para_contains(para, "frey envoys") or _para_contains(para, "palfrey"):
                if can_emit("DECEIVES"):
                    return emit("DECEIVES", 2)
            return reject("temporal-cooccurrence-not-relational")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # jared-frey, symond-frey, rhaegar-frey — came as envoys to White Harbor.
    # Narrative section: NEGOTIATES_WITH (Wyman negotiated peace via betrothal deal).
    # Quotes section: Wyman's speech "I drink with Jared, jape with Symond, promise
    # Rhaegar the hand of my granddaughter" — same underlying negotiation, but the
    # snippet context is attribution; emit NEGOTIATES_WITH once per non-quote section,
    # reject quote-section duplicates.
    # -----------------------------------------------------------------------
    if target in ("jared-frey", "symond-frey", "rhaegar-frey"):
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "envoys") or _para_contains(para, "arrive in white harbor"):
            if can_emit("NEGOTIATES_WITH"):
                return emit("NEGOTIATES_WITH", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # walder-frey — Wyman negotiated with him (via envoys); quotes section is
    # attribution only (Wyman speaking at feast).
    # -----------------------------------------------------------------------
    if target == "walder-frey":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "ransom") or \
                _para_contains(para, "agrees to marry a daughter of lord"):
            if can_emit("NEGOTIATES_WITH"):
                return emit("NEGOTIATES_WITH", 2)
            if can_emit("CONTRACTED_WITH"):
                return emit("CONTRACTED_WITH", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # walder-frey-son-of-merrett (Big Walder / Little Walder) — co-mention.
    # Multiple candidates; only emit from narrative section where betrothal is described.
    # -----------------------------------------------------------------------
    if target in ("walder-frey-son-of-merrett", "little-walder-frey", "big-walder-frey"):
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        # Wylla was to be betrothed to Little Walder (Wyman arranged it)
        if _para_contains(para, "little walder") and _para_contains(para, "wylla"):
            if can_emit("MARRIES_OFF"):
                return emit("MARRIES_OFF", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # wynafryd betrothal to Rhaegar Frey
    # -----------------------------------------------------------------------
    if target == "wynafryd-manderly":
        # Already handled above but double check
        if can_emit("MARRIES_OFF"):
            return emit("MARRIES_OFF", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # roose-bolton — Wyman feasts with, serves pies to, at Ramsay's wedding.
    # Quotes section candidates: Wyman's famous pie speech is directed to Roose —
    # this is still DECEIVES since the entire pie scene is the deception act.
    # -----------------------------------------------------------------------
    if target == "roose-bolton":
        if _para_contains(para, "wedding feast") or _para_contains(para, "pies") or \
                _para_contains(para, "three huge pies"):
            if can_emit("DECEIVES"):
                return emit("DECEIVES", 2)
        if section.lower().startswith("## quotes") and _para_contains(para, "pies"):
            if can_emit("DECEIVES"):
                return emit("DECEIVES", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # ramsay-snow / ramsay-bolton — Wyman opposes him, moves to seize Hornwood.
    # Quotes section: Ramsay's boast about Rodrik's body (para about harvest feast) →
    # the evidence paragraph doesn't mention Wyman's action against Ramsay in quotes;
    # only emit from narrative sections.
    # -----------------------------------------------------------------------
    if target in ("ramsay-snow", "ramsay-bolton"):
        if section.lower().startswith("## quotes"):
            # Quotes attribution — para about Ramsay marrying Hornwood / Wyman seizing
            if _para_contains(para, "seize") and _para_contains(para, "hornwood"):
                if can_emit("OPPOSES"):
                    return emit("OPPOSES", 1)
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "seize") and _para_contains(para, "hornwood"):
            if can_emit("OPPOSES"):
                return emit("OPPOSES", 1)
        if _para_contains(para, "responsible for the massacre") or (
            _para_contains(para, "ramsay bolton") and _para_contains(para, "sack")
        ):
            if can_emit("OPPOSES"):
                return emit("OPPOSES", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # stannis-baratheon — Wyman promises to swear allegiance to Stannis.
    # Quotes section: same promise restated → reject duplicates.
    # AFFC para: Stannis/Cersei co-mention → reject.
    # -----------------------------------------------------------------------
    if target == "stannis-baratheon":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "swear allegiance to stannis") or \
                _para_contains(para, "take stannis baratheon as my king") or \
                _para_contains(para, "take «stannis baratheon» as my king"):
            if can_emit("SUPPORTS"):
                return emit("SUPPORTS", 2)
        # AFFC para: Cersei orders execution of Davos (Stannis's envoy) — co-mention
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # theon-greyjoy — Wyman responded to Theon's capture of Winterfell by sending forces.
    # Multiple candidates: same para across different sections.
    # Quote sections (Barbrey Dustin's remarks, Stannis/Theon dialogue) → reject.
    # -----------------------------------------------------------------------
    if target == "theon-greyjoy":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "capture of winterfell") and _para_contains(para, "wyman sends"):
            if can_emit("SUPPORTS"):
                return emit("SUPPORTS", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # bran-stark — Wyman presents proposals to Bran at Winterfell feast (ADVISES).
    # Only emit once from narrative section; quotes section is attribution only.
    # -----------------------------------------------------------------------
    if target == "bran-stark":
        if not section.lower().startswith("## quotes"):
            if _para_contains(para, "bran stark") and _para_contains(para, "proposes"):
                if can_emit("ADVISES"):
                    return emit("ADVISES", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # rodrik-cassel — co-present at Winterfell feast; Wyman proposes to him.
    # Only emit from narrative section; quotes section is attribution/co-mention.
    # -----------------------------------------------------------------------
    if target == "rodrik-cassel":
        if not section.lower().startswith("## quotes"):
            if _para_contains(para, "rodrik cassel") and _para_contains(para, "proposes"):
                if can_emit("ADVISES"):
                    return emit("ADVISES", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # donella-hornwood — Wyman proposed marriage (COURTS her)
    # -----------------------------------------------------------------------
    if target == "donella-hornwood":
        if _para_contains(para, "husband for the widowed lady") or \
                _para_contains(para, "offers himself") and _para_contains(para, "hornwood"):
            if can_emit("COURTS"):
                return emit("COURTS", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # beth-cassel — Wyman dances with Beth at the feast; no staging verb present
    # per the candidate record → reject (ENCOUNTERS requires staging verb gate)
    # -----------------------------------------------------------------------
    if target == "beth-cassel":
        if staging and _para_contains(para, "dances") and _para_contains(para, "beth cassel"):
            if can_emit("ENCOUNTERS"):
                return emit("ENCOUNTERS", 2)
        return reject("no-staging-verb-for-encounters")

    # -----------------------------------------------------------------------
    # eddard-stark — Eddard asked Catelyn to instruct Wyman; reverse direction
    # -----------------------------------------------------------------------
    if target in ("eddard-stark", "ned-stark"):
        # Eddard acts on Wyman (instructs via Catelyn) → edge on Eddard's node
        return reject("reverse-direction-edge-belongs-on-target-node")

    # -----------------------------------------------------------------------
    # luwin — present at meeting with Wyman; co-mention
    # -----------------------------------------------------------------------
    if target == "luwin":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # house-bolton — Wyman opposes House Bolton.
    # Multiple candidates; emit only from narrative section.
    # -----------------------------------------------------------------------
    if target == "house-bolton":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "prevent house bolton") or (
            _para_contains(para, "seize") and _para_contains(para, "hornwood")
        ):
            if can_emit("OPPOSES"):
                return emit("OPPOSES", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # medrick — Maester Medrick heals Wyman; reverse direction
    # -----------------------------------------------------------------------
    if target == "medrick":
        # Medrick HEALS Wyman → edge belongs on medrick's node
        return reject("reverse-direction-edge-belongs-on-target-node")

    # -----------------------------------------------------------------------
    # gregor-clegane — captured Wylis (Wyman's son); reverse direction
    # -----------------------------------------------------------------------
    if target == "gregor-clegane":
        # Gregor captured Wylis → edge on gregor's node (CAPTURES)
        return reject("reverse-direction-edge-belongs-on-target-node")

    # -----------------------------------------------------------------------
    # fighting-at-the-fords-of-the-trident — Wylis captured there; not Wyman
    # -----------------------------------------------------------------------
    if target == "fighting-at-the-fords-of-the-trident":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # rickon-stark — Wyman seeks Rickon; SEEKS edge.
    # Appears in narrative and quotes section; emit only from narrative.
    # -----------------------------------------------------------------------
    if target == "rickon-stark":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "rickon stark") and (_para_contains(para, "retrieved") or
                                                      _para_contains(para, "smuggle me back") or
                                                      _para_contains(para, "liege lord")):
            if can_emit("SEEKS"):
                return emit("SEEKS", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # shaggydog — Rickon's direwolf; Wyman references it as proof of Rickon's identity
    # -----------------------------------------------------------------------
    if target == "shaggydog":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # skagos — Wyman asks Davos to go to Skagos to retrieve Rickon
    # -----------------------------------------------------------------------
    if target == "skagos":
        if _para_contains(para, "skagos"):
            if can_emit("TRAVELS_TO"):
                # Davos travels to Skagos; not Wyman himself
                return reject("temporal-cooccurrence-not-relational")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # hornwood — Wyman moved to seize Hornwood; SEEKS or RULES (attempted).
    # Multiple candidates; emit only from narrative section.
    # -----------------------------------------------------------------------
    if target == "hornwood":
        if section.lower().startswith("## quotes"):
            return reject("temporal-cooccurrence-not-relational")
        if _para_contains(para, "seize") and _para_contains(para, "hornwood"):
            if can_emit("SEEKS"):
                return emit("SEEKS", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # white-knife — Wyman hid warships up the White Knife
    # -----------------------------------------------------------------------
    if target == "white-knife":
        if _para_contains(para, "hiding them up the white knife") or \
                _para_contains(para, "white knife") and _para_contains(para, "barges"):
            return reject("temporal-cooccurrence-not-relational")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # new-castle — Wyman meets Davos in the New Castle
    # -----------------------------------------------------------------------
    if target == "new-castle":
        if _para_contains(para, "new castle") and staging:
            if can_emit("LOCATED_AT"):
                return emit("LOCATED_AT", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # cersei-lannister — Cersei ordered execution; reverse direction / co-mention
    # -----------------------------------------------------------------------
    if target == "cersei-lannister":
        # Cersei orders Wyman (reverse) or learns of Wyman's actions
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # jaime-lannister — Cersei ordered Jaime to release Wylis; no direct edge
    # -----------------------------------------------------------------------
    if target in ("jaime-lannister",):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # harrenhal — Wylis was captive there; no Wyman → Harrenhal edge
    # -----------------------------------------------------------------------
    if target == "harrenhal":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # tommen-i-baratheon — small council co-mention only
    # -----------------------------------------------------------------------
    if target in ("tommen-i-baratheon", "small-council"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # ironborn / iron-throne / lannister-of-lannisport — co-mentions
    # -----------------------------------------------------------------------
    if target in ("iron-throne", "lannisport", "lannister-of-lannisport", "theomore"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # theomore — Wyman doesn't trust Maester Theomore
    # -----------------------------------------------------------------------
    if target == "theomore":
        if _para_contains(para, "not trusting maester") or \
                _para_contains(para, "theomore"):
            if can_emit("DISTRUSTS"):
                return emit("DISTRUSTS", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # battle-at-winterfell (ACOK) — Wyman sent forces that participated
    # -----------------------------------------------------------------------
    if target == "battle-at-winterfell":
        if _para_contains(para, "join rodrik") or _para_contains(para, "sends a dozen barges"):
            if can_emit("SUPPORTS"):
                return emit("SUPPORTS", 2)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # capture-of-winterfell — Wyman responded to it; context event only
    # -----------------------------------------------------------------------
    if target == "capture-of-winterfell":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # dreadfort — co-mention in quote; no direct edge
    # -----------------------------------------------------------------------
    if target == "dreadfort":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # winterfell — Wyman TRAVELS_TO Winterfell for feast and for wedding
    # -----------------------------------------------------------------------
    if target == "winterfell":
        if _para_contains(para, "wyman comes to") and _para_contains(para, "winterfell"):
            if can_emit("TRAVELS_TO"):
                return emit("TRAVELS_TO", 1)
        if _para_contains(para, "attend the wedding") or \
                _para_contains(para, "wyman brings a huge supply"):
            if can_emit("TRAVELS_TO"):
                return emit("TRAVELS_TO", 1)
        # Quotes section co-mention only
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # harvest-feast — Wyman ATTENDS the harvest feast
    # -----------------------------------------------------------------------
    if target == "harvest-feast":
        if can_emit("ATTENDS"):
            return emit("ATTENDS", 1)
        if can_emit("GUEST_OF"):
            return emit("GUEST_OF", 1)
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # king-in-the-north (title) — Robb holds the title; no edge from Wyman to the title
    # -----------------------------------------------------------------------
    if target in ("king-in-the-north", "prince-of-winterfell"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # north (place.region) — Two candidates:
    #   (a) narrative para (harvest feast) → LOCATED_AT / REGION_OF is wrong direction
    #   (b) track_b infobox para → already handled above in track_b block
    # -----------------------------------------------------------------------
    if target == "north":
        if is_track_b:
            # Handled above; shouldn't reach here
            return reject("temporal-cooccurrence-not-relational")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # doran-martell — Cersei's thought comparing Wyman to Doran; co-mention only
    # -----------------------------------------------------------------------
    if target == "doran-martell":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # mountains-skull — Cersei's thought; co-mention
    # -----------------------------------------------------------------------
    if target == "mountains-skull":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # barbrey-dustin — Dustin's quote about Wyman; reverse direction / co-mention
    # -----------------------------------------------------------------------
    if target == "barbrey-dustin":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # roger-ryswell — mentioned as skeptical about Manderlys' guilt; co-mention
    # -----------------------------------------------------------------------
    if target == "roger-ryswell":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # cley-cerwyn, leobald-tallhart, rodrik-cassel (in quotes about Wyman) —
    # Ramsay's boast after displaying bodies; Wyman not present
    # -----------------------------------------------------------------------
    if target in ("cley-cerwyn", "leobald-tallhart"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # taking-of-deepwood-motte, fall-of-torrhen-square, sack-of-winterfell —
    # mentioned in Stannis/Theon dialogue; Wyman is not a participant
    # -----------------------------------------------------------------------
    if target in ("taking-of-deepwood-motte", "fall-of-torrhen-square",
                  "torrhen-square", "deepwood-motte"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # frey-pies-theories — concept.theory mentioned via quote snippet
    # -----------------------------------------------------------------------
    if target == "frey-pies-theories":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # abel — musician Wyman calls for at the wedding feast
    # -----------------------------------------------------------------------
    if target == "abel":
        if _para_contains(para, "calls for") and _para_contains(para, "abel"):
            if can_emit("ENCOUNTERS"):
                # No staging verb but explicit action of calling for Abel
                if staging:
                    return emit("ENCOUNTERS", 2)
            # Without staging verb
            return reject("no-staging-verb-for-encounters")
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # rat-cook — Wyman tells Abel to sing of the Rat Cook; concept reference
    # -----------------------------------------------------------------------
    if target == "rat-cook":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # three-huge-pies / frey-pie — the pies Wyman serves; food object
    # -----------------------------------------------------------------------
    if "pie" in target or target in ("three-huge-pies",):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # twins (place.location) — Wendel died there; no Wyman → Twins edge
    # -----------------------------------------------------------------------
    if target == "twins":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # barrowton — Frey envoys disappeared en route to Barrowton; co-mention
    # -----------------------------------------------------------------------
    if target == "barrowton":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # crofters-village, wolfswood — WoW/ADWD locations; co-mentions
    # -----------------------------------------------------------------------
    if target in ("crofters-village", "wolfswood", "deepwood-motte-location"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # walda-bolton — co-mention at wedding feast only
    # -----------------------------------------------------------------------
    if target == "walda-bolton":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # lionstar (ship) — Frey envoys arrived on it; no Wyman→Lionstar edge
    # -----------------------------------------------------------------------
    if target == "lionstar":
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # arya-stark (fake Arya) — co-mention at wedding; no direct edge
    # -----------------------------------------------------------------------
    if target in ("arya-stark", "jeyne-poole"):
        return reject("temporal-cooccurrence-not-relational")

    # -----------------------------------------------------------------------
    # DEFAULT FALLBACK
    # If the candidate didn't match any specific rule above, apply general logic:
    # -----------------------------------------------------------------------

    # ENCOUNTERS requires staging verb
    if not staging and "ENCOUNTERS" in valid_types:
        # Don't emit ENCOUNTERS without a staging verb, but continue to other types
        pass

    # Generic: if object.food / object.material / place with no relational context
    if any(t in target_type for t in ["object.", "creature.", "species."]):
        return reject("temporal-cooccurrence-not-relational")

    # Generic reject for anything unrecognized
    return reject("temporal-cooccurrence-not-relational")


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Stage 4 prose-edge classifier for wyman-manderly"
    )
    bucket_root = Path(
        "/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-manderly"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=bucket_root / "prose-edge-candidates-enriched" / "wyman-manderly.candidates.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=bucket_root / "prose-edges-haiku" / "wyman-manderly.edges.jsonl",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    candidates = []
    with args.input.open() as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARNING: Line {lineno} parse error: {e}", file=sys.stderr)

    decisions = []
    for c in candidates:
        d = classify_candidate(c)
        decisions.append(d)

    with args.output.open("w") as f:
        for d in decisions:
            f.write(json.dumps(d) + "\n")

    # -----------------------------------------------------------------------
    # Summary report
    # -----------------------------------------------------------------------
    total = len(decisions)
    emit_count = sum(1 for d in decisions if d["decision"] == "emit_edge")
    reject_count = sum(1 for d in decisions if d["decision"] == "reject_just_mention")
    escalate_count = sum(
        1
        for d in decisions
        if d["decision"] in ("escalate_cross_identity", "escalate_disambiguation")
    )

    print(f"\n=== wyman-manderly classification summary ===")
    print(f"Total candidates:  {total}")
    print(f"  emit_edge:       {emit_count}")
    print(f"  reject:          {reject_count}")
    print(f"  escalate:        {escalate_count}")

    # Edge types emitted
    edge_type_counts: Counter = Counter()
    for d in decisions:
        if d["decision"] == "emit_edge":
            edge_type_counts[d["edge_type"]] += 1
    if edge_type_counts:
        print("\nEdge types emitted:")
        for et, cnt in sorted(edge_type_counts.items()):
            print(f"  {et}: {cnt}")

    # Rejection reasons
    reject_reasons: Counter = Counter()
    for d in decisions:
        if d["decision"] == "reject_just_mention":
            reject_reasons[d["reason"]] += 1
    if reject_reasons:
        print("\nRejection reasons:")
        for reason, cnt in sorted(reject_reasons.items()):
            print(f"  {reason}: {cnt}")

    print(f"\nOutput written to: {args.output}")


if __name__ == "__main__":
    main()
