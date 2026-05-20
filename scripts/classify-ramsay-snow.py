#!/usr/bin/env python3
"""Classify ramsay-snow candidates with intelligent edge reasoning."""
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path("/Users/mnoth/source/asoiaf-chat")
GRAPH_NODES = REPO_ROOT / "graph" / "nodes"

# Cache for source prose and node frontmatters
_prose_cache = {}
_frontmatter_cache = {}

def get_source_prose(source_slug: str, source_bucket: str) -> str:
    """Read source node prose, cached."""
    if source_slug in _prose_cache:
        return _prose_cache[source_slug]

    try:
        # Try characters first
        for type_dir in ["characters"]:
            path = GRAPH_NODES / type_dir / f"{source_slug}.node.md"
            if path.exists():
                with open(path) as f:
                    prose = f.read()
                    _prose_cache[source_slug] = prose
                    return prose
    except:
        pass

    return ""

def get_node_frontmatter(slug: str) -> dict:
    """Read node frontmatter, cached."""
    if slug in _frontmatter_cache:
        return _frontmatter_cache[slug]

    try:
        for type_dir in GRAPH_NODES.iterdir():
            if not type_dir.is_dir():
                continue
            path = type_dir / f"{slug}.node.md"
            if path.exists():
                with open(path) as f:
                    lines = f.readlines()[:50]
                    fm = {}
                    in_fm = False
                    fm_count = 0
                    for line in lines:
                        if line.strip() == "---":
                            if in_fm:
                                break
                            in_fm = True
                        elif in_fm and ":" in line:
                            k, v = line.split(":", 1)
                            fm[k.strip()] = v.strip()
                    _frontmatter_cache[slug] = fm
                    return fm
    except:
        pass

    return {}

def classify_ramsay_candidate(candidate: dict, source_prose: str) -> dict:
    """Classify a single ramsay-snow candidate."""
    source_slug = candidate["source_slug"]
    target_slug = candidate["target_slug"]
    snippet = candidate.get("snippet", "")[:200]
    anchor_text = candidate.get("anchor_text", "")
    section = candidate.get("source_section", "## Origins")

    target_fm = get_node_frontmatter(target_slug)
    target_type = target_fm.get("type", "unknown")

    # CLASSIFICATION LOGIC

    # Material/Object mentions - usually WIELDS or just decorative
    if target_slug in ["bone", "garnet"]:
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "decorative-object-reference"
        }

    # House mentions with "true Bolton" context
    if target_slug in ["house-bolton"] and ("true" in snippet.lower() or "considers" in snippet.lower()):
        # "Ramsay considers himself a true Bolton" - identity affiliation
        return {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "edge_type": "MEMBER_OF",
            "evidence_snippet": snippet,
            "evidence_section": section,
            "confidence_tier": 1
        }

    # House mentions with "custom of flaying"
    if target_slug in ["house-bolton"] and ("custom" in snippet.lower() or "flaying" in snippet.lower()):
        # "fond of the old Bolton custom of flaying" - cultural/identity reference
        return {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "edge_type": "CULTURE_OF",
            "evidence_snippet": snippet,
            "evidence_section": section,
            "confidence_tier": 2
        }

    # House mentions in quotes/dialogue
    if target_slug in ["house-bolton"] and (">" in snippet or "Roose" in snippet or "decree" in snippet):
        # Quote context
        return {
            "decision": "emit_edge",
            "candidate_kind": "source_target",
            "evidence_kind": "wiki-entity",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "edge_type": "MEMBER_OF",
            "evidence_snippet": snippet,
            "evidence_section": section,
            "confidence_tier": 1
        }

    # Reek identity escalation
    if target_slug == "reek" or "Reek" in anchor_text:
        return {
            "decision": "escalate_cross_identity",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "evidence_snippet": snippet,
            "evidence_section": section,
            "rationale": "Reek is an alias or identity that Ramsay uses or that refers to a character connected to Ramsay (possibly Theon Greyjoy)"
        }

    # Theon mentions - could be TORTURES, PRISONER_OF, MASTER_OF, etc.
    if target_slug == "theon-greyjoy":
        lower = snippet.lower()
        if "reek" in lower or (">" in snippet and "Ramsay" in snippet):
            # Quote from or about Ramsay and Theon/Reek
            return {
                "decision": "emit_edge",
                "candidate_kind": "source_target",
                "evidence_kind": "wiki-entity",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "edge_type": "TORTURES",
                "evidence_snippet": snippet,
                "evidence_section": section,
                "confidence_tier": 2
            }
        else:
            return {
                "decision": "reject_just_mention",
                "candidate_kind": "source_target",
                "source_slug": source_slug,
                "target_slug": target_slug,
                "reason": "co-mention-in-quote"
            }

    # Tommen mentions in quotes
    if target_slug == "tommen-baratheon":
        return {
            "decision": "reject_just_mention",
            "candidate_kind": "source_target",
            "source_slug": source_slug,
            "target_slug": target_slug,
            "reason": "co-mention-in-quote"
        }

    # Generic rejection
    return {
        "decision": "reject_just_mention",
        "candidate_kind": "source_target",
        "source_slug": source_slug,
        "target_slug": target_slug,
        "reason": "no-fitting-type-vocab-locked"
    }

def main():
    """Classify ramsay-snow candidates."""
    input_path = REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton-of-the-dreadfort/prose-edge-candidates/ramsay-snow.candidates.jsonl"
    output_path = REPO_ROOT / "working/wiki/pass2-buckets/characters-house-bolton-of-the-dreadfort/prose-edges-haiku/ramsay-snow.edges.jsonl"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Pre-read source prose once
    source_prose = get_source_prose("ramsay-snow", "characters-house-bolton-of-the-dreadfort")

    decisions = []
    with open(input_path) as f:
        for line in f:
            if not line.strip():
                continue
            candidate = json.loads(line)
            decision = classify_ramsay_candidate(candidate, source_prose)
            decisions.append(decision)

    # Write output
    with open(output_path, "w") as f:
        for decision in decisions:
            f.write(json.dumps(decision) + "\n")

    print(f"[done] ramsay-snow.candidates.jsonl → {len(decisions)} rows → {output_path}")

if __name__ == "__main__":
    main()
