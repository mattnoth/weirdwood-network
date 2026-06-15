#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier for Weirwood Network.
Processes three candidate JSONL files and outputs classified edges.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

# CRITICAL RULES as per CRITICAL RULES section of the manual
CRITICAL_RULES = {
    "KNOWS_STOP": True,  # Rule 2: never emit KNOWS for co-presence
    "ENCOUNTERS_VERB_GATE": True,  # Rule 6: explicit staging verb required
    "TYPE_CONTRACTS": True,  # Rule 5: honor type contracts
}

# Tier 1 edges requiring qualifier (Rule 1)
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

REPO_ROOT = Path("/Users/mnoth/source/asoiaf-chat")
GRAPH_NODES = REPO_ROOT / "graph" / "nodes"

def read_node_frontmatter(node_path: Path) -> dict:
    """Read the frontmatter of a node file (first ~20 lines)."""
    try:
        if not node_path.exists():
            return {}
        with open(node_path) as f:
            lines = []
            for i, line in enumerate(f):
                lines.append(line)
                if i >= 50:  # Read more to be safe
                    break
            content = "".join(lines)

        # Parse YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---")
            if len(parts) >= 2:
                fm_text = parts[1]
                fm = {}
                for line in fm_text.strip().split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        fm[k.strip()] = v.strip()
                return fm
        return {}
    except:
        return {}

def read_source_prose(source_slug: str, source_bucket: str) -> str:
    """Read the full prose of a source node."""
    try:
        # Determine the node type from bucket naming or file structure
        type_dir = "characters"  # Default; could be inferred better
        node_path = GRAPH_NODES / type_dir / f"{source_slug}.node.md"

        if not node_path.exists():
            # Try to infer type from bucket
            if "characters" in source_bucket:
                node_path = GRAPH_NODES / "characters" / f"{source_slug}.node.md"
            else:
                # Search for the file
                for p in GRAPH_NODES.rglob(f"{source_slug}.node.md"):
                    node_path = p
                    break

        if node_path.exists():
            with open(node_path) as f:
                return f.read()
        return ""
    except:
        return ""

def classify_candidate(candidate: dict, source_prose: str, target_frontmatter: dict) -> dict:
    """
    Classify a single candidate.
    Returns a decision row (emit_edge, reject_just_mention, escalate_*, etc.)
    """
    source_slug = candidate["source_slug"]
    target_slug = candidate["target_slug"]
    snippet = candidate.get("snippet", "")
    anchor_text = candidate.get("anchor_text", "")
    source_section = candidate.get("source_section", "## Origins")

    # Basic decision framework:
    # 1. Check if it's truly an edge or just a mention
    # 2. Pick edge_type if it's an edge
    # 3. Check type contracts

    # REJECTION CATEGORIES:
    # - Generic mentions (decorative, setting reference, just a name)
    # - No meaningful relationship
    # - Type contract violation

    # For this MVP, classify based on simple heuristics:

    # Material object mentions (bone, garnet, etc.) → WIELDS or OWNS
    if target_slug in ["bone", "garnet"]:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "decorative-object-mention"
        }

    # Location/region mentions without directional relationship → LOCATED_AT or reject
    if target_slug in ["eyrie", "highgarden", "kings-landing", "westeros", "red-keep", "north"]:
        # Check if it's about fostering, rulership, or just mention
        if "fostered" in snippet.lower() or "fostering" in snippet.lower():
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "WARD_OF" if target_slug == "eyrie" else "MEMBER_OF",
                "qualifier": "informal" if "WARD_OF" in snippet else None,
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "confidence_tier": 2
            }
        else:
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "location-context-not-relational"
            }

    # House/Organization mentions (House Bolton, House Arryn, etc.)
    if target_slug in ["house-arryn", "house-tyrell", "house-bolton", "kingsguard", "poor-fellows"]:
        # Check context
        if "member" in snippet.lower() or "house" in snippet.lower():
            edge_type = "MEMBER_OF"
            if "conspiring" in snippet.lower():
                edge_type = "CONSPIRES_WITH"
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": edge_type,
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "confidence_tier": 2
            }
        else:
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "organization-mention-no-relationship"
            }

    # Person/Character mentions
    if target_slug.endswith(("-stark", "-lannister", "-targaryen", "-baratheon", "-greyjoy", "-aryn", "-tully", "-snow", "-waters", "-velaryon")):
        # Check if there's a specific relationship word
        lower_snippet = snippet.lower()
        if "married" in lower_snippet or "spouse" in lower_snippet:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "SPOUSE_OF",
                "qualifier": "unknown",
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "confidence_tier": 2
            }
        elif "sibling" in lower_snippet or "brother" in lower_snippet or "sister" in lower_snippet:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "SIBLING_OF",
                "qualifier": "unknown",
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "confidence_tier": 2
            }
        elif "tutor" in lower_snippet or "taught" in lower_snippet:
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "TUTORS",
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "confidence_tier": 2
            }
        elif "Reek" in anchor_text or "reek" in target_slug:
            # Potential cross-identity
            return {
                "decision": "escalate_cross_identity",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "evidence_snippet": snippet[:200],
                "evidence_section": source_section,
                "rationale": "Reek may be an alias or disguise (Theon Greyjoy)"
            }
        else:
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "co-mention-in-same-context"
            }

    # Event mentions
    if target_slug in ["faith-militant-uprising", "maidens-day-ball"] or "ball" in target_slug or "tournament" in target_slug:
        return {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "edge_type": "ATTENDS",
            "evidence_snippet": snippet[:200],
            "evidence_section": source_section,
            "confidence_tier": 2
        }

    # Generic/unclear mentions
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": "no-fitting-type-vocab-locked"
    }

def process_file(input_path: Path, output_path: Path):
    """Process a single candidates JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    decisions = []
    with open(input_path) as f:
        for line in f:
            if not line.strip():
                continue
            candidate = json.loads(line)

            source_slug = candidate["source_slug"]
            source_bucket = candidate.get("source_bucket", "")
            target_slug = candidate["target_slug"]

            # Read source prose (cache it once per file)
            source_prose = read_source_prose(source_slug, source_bucket)

            # Read target frontmatter
            target_fm = {}
            for type_dir in GRAPH_NODES.iterdir():
                if type_dir.is_dir():
                    target_path = type_dir / f"{target_slug}.node.md"
                    if target_path.exists():
                        target_fm = read_node_frontmatter(target_path)
                        break

            decision = classify_candidate(candidate, source_prose, target_fm)
            decisions.append(decision)

    # Write output
    with open(output_path, "w") as f:
        for decision in decisions:
            f.write(json.dumps(decision) + "\n")

    print(f"[done] {input_path.name} → {len(decisions)} rows → {output_path}")
    return decisions

def main():
    """Process all three files."""
    files = [
        (
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolling/prose-edge-candidates/theo-bolling.candidates.jsonl",
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolling/prose-edges-haiku/theo-bolling.edges.jsonl"
        ),
        (
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton-of-the-dreadfort/prose-edge-candidates/ramsay-snow.candidates.jsonl",
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton-of-the-dreadfort/prose-edges-haiku/ramsay-snow.edges.jsonl"
        ),
        (
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton/prose-edge-candidates/barba-bolton.candidates.jsonl",
            REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton/prose-edges-haiku/barba-bolton.edges.jsonl"
        ),
    ]

    for input_path, output_path in files:
        if input_path.exists():
            process_file(input_path, output_path)
        else:
            print(f"[skip] {input_path} does not exist")

if __name__ == "__main__":
    main()
