#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier for the Weirwood Network.
Uses enriched evidence to classify relationship edges.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import re

TIER1_EDGES = {
    "SIBLING_OF": ["full", "half", "step", "milk", "unknown"],
    "SPOUSE_OF": ["current", "former", "annulled", "widowed", "salt_wife", "unknown"],
    "PARENT_OF": ["biological", "adopted", "claimed", "rumored", "disputed", "unknown"],
    "WARD_OF": ["formal", "informal", "hostage", "unknown"],
    "HOLDS_TITLE": ["current", "former", "claimed", "contested", "historical", "unknown"],
    "VOWS_TO": ["active", "kept", "broken", "fulfilled", "unknown"],
    "MANIPULATES": ["via_bribe", "via_flattery", "via_false_information", "via_threat", "via_seduction", "unknown"],
    "SWORN_TO": ["current", "former", "deserted", "by_marriage", "claimed", "unknown"],
}

def extract_evidence_snippet(paragraph: str, anchor_text: str, max_len: int = 200) -> str:
    """Extract a meaningful snippet containing the anchor text."""
    # Remove anchors for readability
    para_clean = paragraph.replace("«", "").replace("»", "")

    # Find sentences containing the anchor
    sentences = re.split(r'(?<=[.!?])\s+', para_clean)
    relevant = []

    for sent in sentences:
        if anchor_text.lower() in sent.lower() or any(word.lower() in sent.lower() for word in anchor_text.split()):
            relevant.append(sent.strip())
            if len(" ".join(relevant)) > 150:
                break

    if relevant:
        snippet = " ".join(relevant)
        return snippet[:max_len] if len(snippet) > max_len else snippet

    return para_clean[:max_len]

def classify_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify a single source_target candidate.
    """
    source_slug = candidate["source_slug"]
    target_slug = candidate["target_slug"]
    target_type = candidate.get("target_type", "unknown")
    valid_edge_types = candidate.get("valid_edge_types", [])
    evidence_paragraph = candidate.get("evidence_paragraph", "")
    anchor_text = candidate.get("anchor_text", "")
    source_section = candidate.get("source_section", "")

    if not evidence_paragraph:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "no-evidence-paragraph"
        }

    evidence_lower = evidence_paragraph.lower()
    anchor_lower = anchor_text.lower()

    # === Heuristic 1: TUTORS ===
    if re.search(r'\btaught?\b', evidence_lower):
        if "TUTORS" in valid_edge_types and "character" in target_type:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "TUTORS",
                "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                "evidence_section": source_section,
                "evidence_paragraph_index": 0,
                "confidence_tier": 2
            }

    # === Heuristic 2: FIGHTS_IN (for events) ===
    if re.search(r'\b(fought|fight)\b', evidence_lower) and "event" in target_type:
        if "FIGHTS_IN" in valid_edge_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "FIGHTS_IN",
                "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                "evidence_section": source_section,
                "evidence_paragraph_index": 0,
                "confidence_tier": 2
            }

    # === Heuristic 3: MEMBER_OF (for organizations) ===
    if re.search(r'\b(member|part of|order of|sworn to)\b', evidence_lower) and "organization" in target_type:
        if "MEMBER_OF" in valid_edge_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "MEMBER_OF",
                "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                "evidence_section": source_section,
                "evidence_paragraph_index": 0,
                "confidence_tier": 2
            }

    # === Heuristic 4: LOCATED_AT or BORN_AT ===
    if "place" in target_type:
        if re.search(r'\bborn\b', evidence_lower) and "BORN_AT" in valid_edge_types:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "BORN_AT",
                "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                "evidence_section": source_section,
                "evidence_paragraph_index": 0,
                "confidence_tier": 2
            }

    # === Heuristic 5: WIELDS (for artifacts) ===
    if "artifact" in target_type:
        if re.search(r'\b(wield|bear|carry|uses?)\b.*\b(sword|axe|weapon|blade|mace|staff|spear)\b', evidence_lower):
            if "WIELDS" in valid_edge_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "WIELDS",
                    "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                    "evidence_section": source_section,
                    "evidence_paragraph_index": 0,
                    "confidence_tier": 2
                }

        # OWNS (broader)
        if re.search(r'\b(own|possess|has)\b', evidence_lower):
            if "OWNS" in valid_edge_types:
                return {
                    "decision": "emit_edge",
                    "candidate_kind": "source_target",
                    "evidence_kind": "wiki-entity",
                    "source_slug": source_slug,
                    "target_slug": target_slug,
                    "edge_type": "OWNS",
                    "evidence_snippet": extract_evidence_snippet(evidence_paragraph, anchor_text),
                    "evidence_section": source_section,
                    "evidence_paragraph_index": 0,
                    "confidence_tier": 2
                }

    # === Default: just a mention ===
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": "no-fitting-relationship-detected"
    }

def process_candidates_file(input_path: Path, output_path: Path) -> tuple[int, int]:
    """
    Read candidates from input_path, classify them, write to output_path.
    Returns (total, emit_count).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    emit_count = 0
    total = 0
    decisions = []

    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            candidate = json.loads(line)
            decision = classify_candidate(candidate)
            decisions.append(decision)
            total += 1

            if decision["decision"] == "emit_edge":
                emit_count += 1

    # Write output file
    if decisions:
        with open(output_path, 'w') as f:
            for decision in decisions:
                f.write(json.dumps(decision) + "\n")

    return total, emit_count

def main():
    bucket_root = Path("/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-tarth")
    candidates_dir = bucket_root / "prose-edge-candidates-enriched"
    edges_dir = bucket_root / "prose-edges-haiku"

    pairs = [
        ("brienne-tarth.candidates.jsonl", "brienne-tarth.edges.jsonl"),
        ("bryndemere-tarth.candidates.jsonl", "bryndemere-tarth.edges.jsonl"),
        ("cameron-tarth.candidates.jsonl", "cameron-tarth.edges.jsonl"),
        ("endrew-tarth.candidates.jsonl", "endrew-tarth.edges.jsonl"),
        ("goodwin.candidates.jsonl", "goodwin.edges.jsonl"),
    ]

    total_all = 0
    total_emit_all = 0

    for input_name, output_name in pairs:
        input_path = candidates_dir / input_name
        output_path = edges_dir / output_name

        if input_path.exists():
            total, emit = process_candidates_file(input_path, output_path)
            total_all += total
            total_emit_all += emit

            print(f"[done] {input_name} → {emit} emit_edge, {total - emit} reject_just_mention — wrote {output_path}")

    print(f"\nTOTALS: {total_all} candidates | {total_emit_all} emitted")

if __name__ == "__main__":
    main()
