#!/usr/bin/env python3
"""Proper prose-edge classification based on evidence."""

import json
import os
import re

def classify(candidate):
    """Classify one candidate based on evidence."""
    source = candidate.get('source_slug')
    target = candidate.get('target_slug')
    target_type = candidate.get('target_type', '')
    evidence = candidate.get('evidence_paragraph', '')
    section = candidate.get('source_section', '')
    valid_types = set(candidate.get('valid_edge_types', []))
    anchor = candidate.get('anchor_text', '')

    # Reject concepts and materials immediately
    if target_type in ['concept.custom', 'concept.culture', 'concept.magic', 'concept.medical', 'object.material']:
        return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
                'source_slug': source, 'target_slug': target, 'reason': 'target-not-entity'}

    # SPOUSE/MARRIED relationships
    if target_type == 'character.human':
        evidence_lower = evidence.lower()

        # Explicit marriage language
        if re.search(r'\bwed[s]?\b|\bmarried\b|\bweds?\b', evidence_lower):
            if 'SPOUSE_OF' in valid_types:
                qual = 'unknown'
                if 'widowed' in evidence_lower or 'widow' in evidence_lower:
                    qual = 'widowed'
                elif 'former' in evidence_lower or 'divorced' in evidence_lower:
                    qual = 'former'
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source,
                    'target_slug': target,
                    'edge_type': 'SPOUSE_OF',
                    'evidence_snippet': evidence[:200] if len(evidence) > 200 else evidence,
                    'evidence_section': section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 1,
                    'qualifier': qual
                }

        # Cousin relationship
        elif 'cousin' in evidence_lower:
            if 'COUSIN_OF' in valid_types:
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source,
                    'target_slug': target,
                    'edge_type': 'COUSIN_OF',
                    'evidence_snippet': evidence[:200] if len(evidence) > 200 else evidence,
                    'evidence_section': section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 1
                }

        # Slept with / lover
        elif 'slept with' in evidence_lower:
            if 'LOVER_OF' in valid_types:
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source,
                    'target_slug': target,
                    'edge_type': 'LOVER_OF',
                    'evidence_snippet': evidence[:200] if len(evidence) > 200 else evidence,
                    'evidence_section': section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 1
                }

        # Generic character co-mention
        return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
                'source_slug': source, 'target_slug': target, 'reason': 'character-temporal-cooccurrence'}

    # Location relationships
    elif target_type == 'place.location':
        evidence_lower = evidence.lower()

        # Page/squire/servant AT location
        if any(role in evidence_lower for role in [' page ', ' squire ', ' servant ', ' lord of ', ' lady of ', ' at the ', ' at ']):
            if 'LOCATED_AT' in valid_types:
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source,
                    'target_slug': target,
                    'edge_type': 'LOCATED_AT',
                    'evidence_snippet': evidence[:200] if len(evidence) > 200 else evidence,
                    'evidence_section': section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 2
                }

        # Just mention of location
        return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
                'source_slug': source, 'target_slug': target, 'reason': 'location-mention-not-relational'}

    # Region relationships
    elif target_type == 'place.region':
        # Just mentions in context
        return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
                'source_slug': source, 'target_slug': target, 'reason': 'region-mention-not-relational'}

    # Event relationships
    elif target_type in ['event.battle', 'event.ceremony', 'event.tournament']:
        evidence_lower = evidence.lower()

        # Attending event
        if 'ATTENDS' in valid_types:
            if any(word in evidence_lower for word in ['attended', 'present at', 'at the wedding', 'seated at', 'feast']):
                return {
                    'decision': 'emit_edge',
                    'candidate_kind': 'source_target',
                    'evidence_kind': 'wiki-entity',
                    'source_slug': source,
                    'target_slug': target,
                    'edge_type': 'ATTENDS',
                    'evidence_snippet': evidence[:200] if len(evidence) > 200 else evidence,
                    'evidence_section': section,
                    'evidence_paragraph_index': 0,
                    'confidence_tier': 2
                }

        return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
                'source_slug': source, 'target_slug': target, 'reason': 'event-mention-no-evidence'}

    # Default rejection
    return {'decision': 'reject_just_mention', 'candidate_kind': 'source_target',
            'source_slug': source, 'target_slug': target, 'reason': 'no-relationship-found'}

def process_file(input_path, output_path):
    """Process one candidates file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    decisions = []
    with open(input_path, 'r') as f:
        for line in f:
            if line.strip():
                cand = json.loads(line.strip())
                dec = classify(cand)
                decisions.append(dec)

    with open(output_path, 'w') as f:
        for dec in decisions:
            f.write(json.dumps(dec) + '\n')

    return len(decisions), sum(1 for d in decisions if d['decision'] == 'emit_edge')

# Process all files
files = {
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-merrett.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-merrett.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-rhaegar.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-rhaegar.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-frey-daughter-of-walton.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-frey-daughter-of-walton.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walda-rivers-daughter-of-aemon.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walda-rivers-daughter-of-aemon.edges.jsonl',
    'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edge-candidates-enriched/walder-frey-son-of-emmon.candidates.jsonl':
        'working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walder-frey-son-of-emmon.edges.jsonl'
}

for inp, out in files.items():
    total, emitted = process_file(inp, out)
    fname = os.path.basename(inp).replace('.candidates.jsonl', '')
    rejected = total - emitted
    print(f'[done] {fname} → {emitted} emit_edge, {rejected} reject_just_mention — wrote {out}')
