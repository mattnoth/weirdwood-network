#!/usr/bin/env python3
"""
Stage 4 prose-edge classifier v2 - proper classification matching anchor_text.
"""

import json
from pathlib import Path

def classify_candidate(candidate):
    """Classify using anchor_text context."""

    source_slug = candidate['source_slug']
    target_slug = candidate['target_slug']
    target_type = candidate['target_type']
    anchor_text = candidate.get('anchor_text', '').lower()
    evidence_paragraph = candidate.get('evidence_paragraph', '')
    valid_edge_types = set(candidate.get('valid_edge_types', []))
    source_section = candidate.get('source_section', '')

    evidence_lower = evidence_paragraph.lower()
    snippet = evidence_paragraph[:200] if len(evidence_paragraph) > 200 else evidence_paragraph

    # Key insight: use anchor_text to find what's actually being referred to in context
    # Find the anchor in the evidence and look at surrounding text

    if not anchor_text:
        # If no anchor, default reject
        return {
            'decision': 'reject_just_mention',
            'candidate_kind': 'source_target',
            'source_slug': source_slug,
            'target_slug': target_slug,
            'reason': 'no-anchor-text',
        }

    # Find location of anchor in evidence (normalize « » guillemets)
    evidence_for_match = evidence_paragraph.replace('«', '').replace('»', '')
    anchor_for_match = anchor_text.replace('«', '').replace('»', '')

    anchor_pos = -1
    for i in range(len(evidence_for_match) - len(anchor_for_match) + 1):
        if evidence_for_match[i:i+len(anchor_for_match)].lower() == anchor_for_match:
            anchor_pos = i
            break

    # Get context around anchor (50 chars before and after)
    context_start = max(0, anchor_pos - 50) if anchor_pos >= 0 else 0
    context_end = min(len(evidence_for_match), anchor_pos + len(anchor_for_match) + 50) if anchor_pos >= 0 else len(evidence_for_match)
    context = evidence_for_match[context_start:context_end].lower()

    # ===== KINSHIP RELATIONSHIPS =====

    # Full sibling - "his brother", "her sister", etc.
    if 'brother' in anchor_text or 'sister' in anchor_text:
        if 'SIBLING_OF' in valid_edge_types and 'half-brother' not in context and 'half-sister' not in context:
            return {
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
            }

    # Half-sibling
    if 'half' in anchor_text or 'half-brother' in context or 'half-sister' in context:
        if 'SIBLING_OF' in valid_edge_types:
            return {
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
            }

    # Nephew relationship
    if 'nephew' in anchor_text or 'niece' in anchor_text:
        if 'UNCLE_OF' in valid_edge_types:
            return {
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
            }

    # In-law relationship
    if 'goodbrother' in anchor_text or 'goodsister' in anchor_text or 'mother-in-law' in anchor_text:
        if 'IN_LAW_OF' in valid_edge_types:
            return {
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
            }

    # ===== SPATIAL RELATIONSHIPS =====

    if target_type in ['place.location', 'place.region']:
        # Location mentioned in evidence with source
        if 'LOCATED_AT' in valid_edge_types:
            return {
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
            }

    # ===== EVENT RELATIONSHIPS =====

    if target_type == 'event.battle':
        # Check context for event relationship type
        if 'attends' in context or 'wedding feast' in context or 'nearby' in context:
            if 'ATTENDS' in valid_edge_types:
                return {
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
                }

        # Participates in battle/event
        if 'PARTICIPATES_IN' in valid_edge_types:
            return {
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
            }

    # ===== DEFAULT REJECT =====

    return {
        'decision': 'reject_just_mention',
        'candidate_kind': 'source_target',
        'source_slug': source_slug,
        'target_slug': target_slug,
        'reason': 'temporal-cooccurrence-not-relational',
    }


def process_file(input_path, output_path):
    """Process a candidate file."""

    with open(input_path) as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
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

    for filename in files:
        input_path = candidates_dir / filename
        output_filename = filename.replace('.candidates.jsonl', '.edges.jsonl')
        output_path = output_dir / output_filename

        if input_path.exists():
            process_file(input_path, output_path)


if __name__ == '__main__':
    main()
