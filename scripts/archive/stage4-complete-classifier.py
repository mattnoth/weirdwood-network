#!/usr/bin/env python3
"""
Stage 4 comention classifier with relationships extracted from all 5 ACOK chapters.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

# Extracted relationships from each chapter
CHAPTER_RELATIONSHIPS = {
    "a-clash-of-kings-chapter-37": {
        # Kinship/Family
        ("aeron-greyjoy", "theon-greyjoy"): ("UNCLE_OF", "a_to_b"),
        ("balon-greyjoy", "theon-greyjoy"): ("PARENT_OF", "a_to_b"),
        ("balon-greyjoy", "aeron-greyjoy"): ("SIBLING_OF", "symmetric"),
        ("helman-tallhart", "benfred-tallhart"): ("PARENT_OF", "a_to_b"),
        ("theon-greyjoy", "asha-greyjoy"): ("SIBLING_OF", "symmetric"),
        # Religious
        ("aeron-greyjoy", "drowned-god"): ("WORSHIPS", "a_to_b"),
        # Military/Combat
        ("theon-greyjoy", "benfred-tallhart"): ("CAPTURES", "a_to_b"),
        ("benfred-tallhart", "wild-hares"): ("COMMANDS", "a_to_b"),
        ("jaime-lannister", "theon-greyjoy"): ("DUELS", "symmetric"),
        ("daryn-hornwood", "theon-greyjoy"): ("PROTECTS", "a_to_b"),
        # Service/Relationship
        ("theon-greyjoy", "brynden-tully"): ("SERVES", "a_to_b"),
        ("theon-greyjoy", "eddard-stark"): ("WARD_OF", "a_to_b"),
        ("wex-pyke", "theon-greyjoy"): ("SERVES", "a_to_b"),
        ("dagmer", "theon-greyjoy"): ("TUTORS", "a_to_b"),
        ("maron-botley", "theon-greyjoy"): ("SERVES", "a_to_b"),
        # Social/Friendship
        ("theon-greyjoy", "robb-stark"): ("COMPANION_OF", "symmetric"),
        # Travel
        ("theon-greyjoy", "helman-tallhart"): ("TRAVELS_WITH", "symmetric"),
        ("eddard-stark", "helman-tallhart"): ("GUEST_OF", "b_to_a"),
        # Fear/Threat
        ("benfred-tallhart", "robb-stark"): ("FEARS", "a_to_b"),
    },
    "a-clash-of-kings-chapter-38": {
        # Kinship
        ("arya-stark", "robb-stark"): ("SIBLING_OF", "symmetric"),
        # Custody/Control
        ("weese", "arya-stark"): ("GUARDS", "a_to_b"),
        # Murder
        ("jaqen-h-ghar", "weese"): ("KILLS", "a_to_b"),
        # Faction
        ("jaqen-h-ghar", "brave-companions"): ("MEMBER_OF", "a_to_b"),
        ("amory-lorch", "harrenhal"): ("RULES", "a_to_b"),
        # Authority
        ("tywin-lannister", "addam-marbrand"): ("COMMANDS", "a_to_b"),
        # Conflict
        ("addam-marbrand", "robb-stark"): ("OPPOSES", "a_to_b"),
        # Fear
        ("arya-stark", "gregor-clegane"): ("FEARS", "a_to_b"),
    },
    "a-clash-of-kings-chapter-39": {
        # Kinship
        ("catelyn-tully", "edmure-tully"): ("SIBLING_OF", "symmetric"),
        ("catelyn-tully", "hoster-tully"): ("PARENT_OF", "b_to_a"),
        ("catelyn-tully", "lysa-arryn"): ("SIBLING_OF", "symmetric"),
        ("catelyn-tully", "eddard-stark"): ("SPOUSE_OF", "symmetric"),
        ("robb-stark", "edmure-tully"): ("UNCLE_OF", "b_to_a"),
        ("roose-bolton", "walda-frey"): ("SPOUSE_OF", "symmetric"),
        # Service/Loyalty
        ("brienne-of-tarth", "catelyn-tully"): ("SERVES", "a_to_b"),
        # Military
        ("robb-stark", "grey-wind"): ("BONDED_TO", "symmetric"),
        ("robb-stark", "greatjon"): ("COMMANDS", "a_to_b"),
        ("roose-bolton", "harrenhal"): ("CAPTURES", "a_to_b"),
        # Conflict
        ("tywin-lannister", "edmure-tully"): ("OPPOSES", "a_to_b"),
    },
    "a-clash-of-kings-chapter-4": {
        # Kinship
        ("bran-stark", "catelyn-stark"): ("PARENT_OF", "b_to_a"),
        ("bran-stark", "eddard-stark"): ("PARENT_OF", "b_to_a"),
        ("bran-stark", "robb-stark"): ("SIBLING_OF", "symmetric"),
        ("bran-stark", "sansa-stark"): ("SIBLING_OF", "symmetric"),
        ("bran-stark", "arya-stark"): ("SIBLING_OF", "symmetric"),
        ("bran-stark", "rickon-stark"): ("SIBLING_OF", "symmetric"),
        ("bran-stark", "jon-snow"): ("SIBLING_OF", "symmetric"),
        ("big-walder-frey", "little-walder-frey"): ("SIBLING_OF", "symmetric"),
        # Magic/Bonding
        ("bran-stark", "summer"): ("BONDED_TO", "symmetric"),
        ("bran-stark", "shaggydog"): ("BONDED_TO", "symmetric"),
        ("rickon-stark", "shaggydog"): ("BONDED_TO", "symmetric"),
        # Guardianship
        ("osha", "bran-stark"): ("GUARDS", "a_to_b"),
        # Mentorship
        ("maester-luwin", "bran-stark"): ("ADVISES", "a_to_b"),
        # Combat/Attack
        ("shaggydog", "little-walder-frey"): ("ATTACKS", "a_to_b"),
    },
    "a-clash-of-kings-chapter-40": {
        # Diplomacy/Negotiation
        ("daenerys-targaryen", "xaro-xhoan-daxos"): ("NEGOTIATES_WITH", "symmetric"),
        # Mentorship/Advice
        ("jorah-mormont", "daenerys-targaryen"): ("ADVISES", "a_to_b"),
        ("quaithe", "daenerys-targaryen"): ("ADVISES", "a_to_b"),
        # Conflict (historical)
        ("robert-baratheon", "daenerys-targaryen"): ("OPPOSES", "a_to_b"),
    },
}


def get_relationship(chapter: str, pair_a: str, pair_b: str) -> Optional[Tuple[str, str]]:
    """Look up the relationship between two entities in a chapter."""
    relationships = CHAPTER_RELATIONSHIPS.get(chapter, {})

    # Check forward direction
    if (pair_a, pair_b) in relationships:
        return relationships[(pair_a, pair_b)]

    # Check reverse direction
    if (pair_b, pair_a) in relationships:
        edge_type, direction = relationships[(pair_b, pair_a)]
        if direction == "a_to_b":
            return (edge_type, "b_to_a")
        elif direction == "b_to_a":
            return (edge_type, "a_to_b")
        else:  # symmetric
            return (edge_type, direction)

    return None


def classify_candidate(candidate: Dict) -> Dict:
    """Classify a single comention candidate."""

    pair_a = candidate.get("pair_a", "")
    pair_b = candidate.get("pair_b", "")
    evidence_chapter = candidate.get("evidence_chapter", "")
    evidence_paragraphs = candidate.get("evidence_paragraphs", [])

    if not evidence_paragraphs:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "comention",
            "pair_a": pair_a,
            "pair_b": pair_b,
            "evidence_chapter": evidence_chapter,
            "reason": "no-evidence"
        }

    first_para = evidence_paragraphs[0]
    section = first_para.get("section", "## Unknown")
    paragraph_index = first_para.get("paragraph_index", 0)
    snippet = first_para.get("snippet", "")

    # Try to get relationship
    relationship = get_relationship(evidence_chapter, pair_a, pair_b)

    if relationship:
        edge_type, direction = relationship

        # Determine source and target based on direction
        if direction == "a_to_b":
            source_slug = pair_a
            target_slug = pair_b
        elif direction == "b_to_a":
            source_slug = pair_b
            target_slug = pair_a
        else:  # symmetric
            source_slug = pair_a
            target_slug = pair_b

        return {
            "decision": "emit_edge",
            "candidate_kind": "comention",
            "evidence_kind": "wiki-chapter-summary",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "direction": direction,
            "edge_type": edge_type,
            "evidence_chapter": evidence_chapter,
            "evidence_snippet": snippet[:200],
            "evidence_section": section,
            "evidence_paragraph_index": paragraph_index,
            "confidence_tier": 1
        }

    # No relationship found - reject as temporal co-occurrence
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "comention",
        "pair_a": pair_a,
        "pair_b": pair_b,
        "evidence_chapter": evidence_chapter,
        "reason": "temporal-cooccurrence-not-relational"
    }


def process_file(input_path: Path, output_path: Path) -> None:
    """Process a single candidates file."""

    if not input_path.exists():
        print(f"Input not found: {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    classifications = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    candidate = json.loads(line)
                    decision = classify_candidate(candidate)
                    classifications.append(decision)
                except Exception as e:
                    print(f"Error: {e}")
                    continue

    # Write output
    with open(output_path, 'w') as f:
        for classification in classifications:
            f.write(json.dumps(classification) + '\n')

    # Count results
    emit_count = sum(1 for c in classifications if c.get("decision") == "emit_edge")
    reject_count = len(classifications) - emit_count

    print(f"[done] {input_path.name} → {emit_count} emit_edge, {reject_count} reject_just_mention, 0 escalate — wrote {output_path.name}")


def main():
    base_path = Path("/Users/mnoth/source/asoiaf-chat")

    files = [
        ("a-clash-of-kings-chapter-37", "acok"),
        ("a-clash-of-kings-chapter-38", "acok"),
        ("a-clash-of-kings-chapter-39", "acok"),
        ("a-clash-of-kings-chapter-4", "acok"),
        ("a-clash-of-kings-chapter-40", "acok"),
    ]

    for chapter_slug, book in files:
        input_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/comention-candidates/{chapter_slug}.candidates.jsonl"
        output_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/prose-edges-haiku/{chapter_slug}.comention-edges.jsonl"
        process_file(input_path, output_path)


if __name__ == "__main__":
    main()
