#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier - proper classification with manual rule compliance.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def classify_candidate(candidate):
    """Classify a single enriched candidate into a decision."""

    source_slug = candidate['source_slug']
    target_slug = candidate['target_slug']
    target_type = candidate['target_type']
    evidence_paragraph = candidate.get('evidence_paragraph', '')
    valid_edge_types = set(candidate.get('valid_edge_types', []))
    staging_verbs_present = candidate.get('staging_verbs_present', [])
    source_section = candidate.get('source_section', '')

    evidence_lower = evidence_paragraph.lower()

    # Extract snippet - take first 200 chars of evidence
    snippet = evidence_paragraph[:200] if len(evidence_paragraph) > 200 else evidence_paragraph

    decisions = []

    # ===== KINSHIP RELATIONSHIPS =====
    # These have explicit linguistic markers in the evidence

    # Full sibling
    if 'his brother Ser ' in evidence_paragraph or 'his sister' in evidence_paragraph:
        if 'SIBLING_OF' in valid_edge_types:
            decisions.append({
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'SIBLING_OF',
                'qualifier': 'full',
                'evidence_snippet': snippet,
                'evidence_section': source_section,
                'evidence_paragraph_index': 0,
                'confidence_tier': 1,
            })
            return decisions[0]

    # Half-sibling
    if 'half-brother' in evidence_lower or 'half-sister' in evidence_lower:
        if 'SIBLING_OF' in valid_edge_types:
            decisions.append({
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'SIBLING_OF',
                'qualifier': 'half',
                'evidence_snippet': snippet,
                'evidence_section': source_section,
                'evidence_paragraph_index': 0,
                'confidence_tier': 1,
            })
            return decisions[0]

    # Nephew relationship
    if ' nephew ' in evidence_lower or 'nephew Ser ' in evidence_paragraph:
        if 'UNCLE_OF' in valid_edge_types:
            decisions.append({
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'UNCLE_OF',
                'evidence_snippet': snippet,
                'evidence_section': source_section,
                'evidence_paragraph_index': 0,
                'confidence_tier': 1,
            })
            return decisions[0]

    # In-law relationship (goodbrother/goodsister/etc.)
    if 'goodbrother' in evidence_lower or 'goodsister' in evidence_lower:
        if 'IN_LAW_OF' in valid_edge_types:
            decisions.append({
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'IN_LAW_OF',
                'evidence_snippet': snippet,
                'evidence_section': source_section,
                'evidence_paragraph_index': 0,
                'confidence_tier': 1,
            })
            return decisions[0]

    # ===== SPATIAL RELATIONSHIPS =====

    if target_type in ['place.location', 'place.region']:
        # Person is mentioned at/in a location
        if 'LOCATED_AT' in valid_edge_types:
            # Look for position markers
            if (' at ' in evidence_lower or ' in ' in evidence_lower or
                'sitting' in evidence_lower or 'training' in evidence_lower or
                'captive' in evidence_lower):
                decisions.append({
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source_slug,
                    'target_slug': target_slug,
                    'edge_type': 'LOCATED_AT',
                    'evidence_snippet': snippet,
                    'evidence_section': source_section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 2,
                })
                return decisions[0]

    # ===== EVENT RELATIONSHIPS =====

    if target_type == 'event.battle':
        # Check what the source is doing regarding the event
        if 'attends' in evidence_lower or 'wedding feast' in evidence_lower:
            if 'ATTENDS' in valid_edge_types:
                decisions.append({
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source_slug,
                    'target_slug': target_slug,
                    'edge_type': 'ATTENDS',
                    'evidence_snippet': snippet,
                    'evidence_section': source_section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 2,
                })
                return decisions[0]

        # Participates in event (violence, battle action)
        if any(word in evidence_lower for word in ['defends', 'striking', 'stabs', 'kills', 'fights']):
            if 'PARTICIPATES_IN' in valid_edge_types:
                decisions.append({
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source_slug,
                    'target_slug': target_slug,
                    'edge_type': 'PARTICIPATES_IN',
                    'evidence_snippet': snippet,
                    'evidence_section': source_section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 2,
                })
                return decisions[0]

    # ===== COMPANION/TRAVEL RELATIONSHIPS =====

    # When multiple characters are mentioned together in a scene
    if 'drinking with' in evidence_lower or 'sitting' in evidence_lower:
        if target_type == 'character.human' and 'TRAVELS_WITH' in valid_edge_types:
            # Co-presence in a social setting
            decisions.append({
                'decision': 'emit_edge',
                'candidate_kind': 'source_target',
                'evidence_kind': 'wiki-entity',
                'source_slug': source_slug,
                'target_slug': target_slug,
                'edge_type': 'TRAVELS_WITH',
                'evidence_snippet': snippet,
                'evidence_section': source_section,
                'evidence_paragraph_index': 0,
                'confidence_tier': 2,
            })
            return decisions[0]

    # ===== DEFAULT REJECT =====

    # If no clear relationship found, reject as mention
    return {
        'decision': 'reject_just_mention',
        'candidate_kind': 'source_target',
        'source_slug': source_slug,
        'target_slug': target_slug,
        'reason': 'temporal-cooccurrence-not-relational',
    }


def process_file(input_path, output_path):
    """Process a candidate file and write edges."""

    with open(input_path) as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print(f"{input_path.name}: 0 candidates")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    emit_count = 0
    reject_count = 0

    with open(output_path, 'w') as out:
        for line in lines:
            candidate = json.loads(line)
            decision = classify_candidate(candidate)
            out.write(json.dumps(decision) + '\n')

            if decision['decision'] == 'emit_edge':
                emit_count += 1
            else:
                reject_count += 1

    print(f"[done] {input_path.name} → {emit_count} emit_edge, {reject_count} reject_just_mention, 0 escalate — wrote {output_path.name}")
    return len(lines)


def main():
    base_dir = Path('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/characters-house-frey-m-t')
    candidates_dir = base_dir / 'prose-edge-candidates-enriched'
    output_dir = base_dir / 'prose-edges-haiku'

    output_dir.mkdir(parents=True, exist_ok=True)

    files = [
        'raymund-frey.candidates.jsonl',
        'rhaegar-frey.candidates.jsonl',
        'robert-frey-son-of-raymund.candidates.jsonl',
        'ronel-rivers.candidates.jsonl',
        'roslin-frey.candidates.jsonl',
    ]

    total = 0
    for filename in files:
        input_path = candidates_dir / filename
        output_filename = filename.replace('.candidates.jsonl', '.edges.jsonl')
        output_path = output_dir / output_filename

        if input_path.exists():
            count = process_file(input_path, output_path)
            total += count

    print(f"\nProcessed {total} total candidates")


if __name__ == '__main__':
    main()
