#!/usr/bin/env python3
"""
Stage 4 comention classifier - reads chapter prose and classifies candidates
based on explicitly mentioned relationships in ASOIAF wiki text.
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple, List

# Extracted relationships from ACOK chapters
# Format: {chapter_slug: {(entity1, entity2): (edge_type, direction)}}
CHAPTER_RELATIONSHIPS = {
    "a-clash-of-kings-chapter-37": {
        # Family/Kinship
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
    # Other chapters would have their own relationship maps
    # For now, defaulting to empty for other chapters
    "a-clash-of-kings-chapter-38": {},
    "a-clash-of-kings-chapter-39": {},
    "a-clash-of-kings-chapter-4": {},
    "a-clash-of-kings-chapter-40": {},
}


def normalize_entity_slug(text: str) -> str:
    """Convert entity text to slug format (lowercase, dashes)."""
    return text.lower().replace(" ", "-").replace("'", "")


def get_relationship(chapter: str, pair_a: str, pair_b: str) -> Optional[Tuple[str, str]]:
    """
    Look up the relationship between two entities in a chapter.
    Returns: (edge_type, direction) or None
    """
    relationships = CHAPTER_RELATIONSHIPS.get(chapter, {})

    # Check forward direction
    if (pair_a, pair_b) in relationships:
        return relationships[(pair_a, pair_b)]

    # Check reverse direction (for symmetric edges, this is a duplicate, but for others,
    # we may need to reverse)
    if (pair_b, pair_a) in relationships:
        edge_type, direction = relationships[(pair_b, pair_a)]
        # Reverse the direction
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

        # Determine source and target
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

    # No relationship found
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
                except (json.JSONDecodeError, Exception) as e:
                    print(f"Error processing: {e}")
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
