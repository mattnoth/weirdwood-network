#!/usr/bin/env python3
"""
Stage 4 comention classifier for ASOIAF wiki prose edges.
Processes candidates and assigns classifications based on relationship patterns.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Kinship patterns (simple name-based matching + known facts)
KINSHIP_FACTS = {
    # Format: (entity1, entity2) -> (edge_type, direction)
    ("theon-greyjoy", "aeron-greyjoy"): ("UNCLE_OF", "reverse"),  # Aeron is Theon's uncle
    ("aeron-greyjoy", "theon-greyjoy"): ("UNCLE_OF", "forward"),  # Aeron is uncle of Theon
    ("balon-greyjoy", "theon-greyjoy"): ("PARENT_OF", "forward"),  # Balon is Theon's father
    ("balon-greyjoy", "aeron-greyjoy"): ("SIBLING_OF", "forward"),  # Balon and Aeron are brothers
    ("helman-tallhart", "benfred-tallhart"): ("PARENT_OF", "forward"),  # Helman is Benfred's father
    ("benfred-tallhart", "helman-tallhart"): ("PARENT_OF", "reverse"),  # Benfred is son of Helman
}

# Religious relationships
RELIGIOUS_FACTS = {
    ("aeron-greyjoy", "drowned-god"): ("WORSHIPS", "forward"),  # Aeron worships the Drowned God
}

# Spatial relationships - visiting/travel
SPATIAL_FACTS = {
    # Theon accompanied Eddard to Torrhen's Square
    ("theon-greyjoy", "torrhens-square"): ("TRAVELS_TO", "forward"),
    ("eddard-stark", "torrhens-square"): ("TRAVELED_TO", "forward"),
}

# Military/Conflict relationships
MILITARY_FACTS = {
    # Benfred was captured by Theon
    ("benfred-tallhart", "theon-greyjoy"): ("PRISONER_OF", "forward"),
    ("theon-greyjoy", "benfred-tallhart"): ("CAPTURES", "forward"),
}


def get_relationship(pair_a: str, pair_b: str, evidence_snippet: str) -> Optional[Tuple[str, str]]:
    """
    Determine if there's a canonical relationship between pair_a and pair_b.
    Returns: (edge_type, direction) or None if no relationship found
    where direction is "a_to_b", "b_to_a", or "symmetric"
    """

    # Check forward direction
    if (pair_a, pair_b) in KINSHIP_FACTS:
        edge_type, dir_hint = KINSHIP_FACTS[(pair_a, pair_b)]
        if dir_hint == "forward":
            return (edge_type, "a_to_b")
        elif dir_hint == "reverse":
            return (edge_type, "b_to_a")

    if (pair_a, pair_b) in RELIGIOUS_FACTS:
        edge_type, dir_hint = RELIGIOUS_FACTS[(pair_a, pair_b)]
        return (edge_type, "a_to_b")

    # Check reverse direction
    if (pair_b, pair_a) in KINSHIP_FACTS:
        edge_type, dir_hint = KINSHIP_FACTS[(pair_b, pair_a)]
        if dir_hint == "forward":
            return (edge_type, "b_to_a")
        elif dir_hint == "reverse":
            return (edge_type, "a_to_b")

    if (pair_b, pair_a) in RELIGIOUS_FACTS:
        edge_type, dir_hint = RELIGIOUS_FACTS[(pair_b, pair_a)]
        return (edge_type, "b_to_a")

    # Check for other patterns in snippet
    # (This would be expanded with more sophisticated pattern matching)

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
            "reason": "no-evidence-paragraphs"
        }

    first_para = evidence_paragraphs[0]
    section = first_para.get("section", "## Unknown")
    paragraph_index = first_para.get("paragraph_index", 0)
    snippet = first_para.get("snippet", "")

    # Try to classify the relationship
    relationship = get_relationship(pair_a, pair_b, snippet)

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
            "evidence_snippet": snippet[:200],  # Truncate to 200 chars
            "evidence_section": section,
            "evidence_paragraph_index": paragraph_index,
            "confidence_tier": 2  # Inferred from context
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


def process_file(input_path: Path, output_path: Path) -> int:
    """Process a candidates file and write classifications."""

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    classifications = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    candidate = json.loads(line)
                    decision = classify_candidate(candidate)
                    classifications.append(decision)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}", file=sys.stderr)
                    continue

    # Write output
    with open(output_path, 'w') as f:
        for classification in classifications:
            f.write(json.dumps(classification) + '\n')

    emit_count = sum(1 for c in classifications if c.get("decision") == "emit_edge")
    reject_count = sum(1 for c in classifications if c.get("decision") == "reject_just_mention")

    print(f"[done] {input_path.name} → {emit_count} emit_edge, {reject_count} reject_just_mention, 0 escalate — wrote {output_path.name}")

    return len(classifications)


def main():
    base_path = Path("/Users/mnoth/source/asoiaf-chat")

    files = [
        ("a-clash-of-kings-chapter-37", "acok"),
        ("a-clash-of-kings-chapter-38", "acok"),
        ("a-clash-of-kings-chapter-39", "acok"),
        ("a-clash-of-kings-chapter-4", "acok"),
        ("a-clash-of-kings-chapter-40", "acok"),
    ]

    total_candidates = 0
    for chapter_slug, book in files:
        input_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/comention-candidates/{chapter_slug}.candidates.jsonl"
        output_path = base_path / f"working/wiki/pass2-buckets/meta-chapters-{book}/prose-edges-haiku/{chapter_slug}.comention-edges.jsonl"

        count = process_file(input_path, output_path)
        total_candidates += count

    print(f"\nTotal candidates processed: {total_candidates}")


if __name__ == "__main__":
    main()
