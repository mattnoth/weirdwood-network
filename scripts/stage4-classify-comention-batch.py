#!/usr/bin/env python3
"""
Stage 4 Comention Classifier - Batch processor
Processes comention candidates JSONL files and outputs classification decisions.
Requires manual reasoning for each edge_type decision.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime


def extract_relationship_signals(snippets):
    """Extract relationship signals from snippets."""
    combined = " ".join([s.get('snippet', '') for s in snippets])
    combined_lower = combined.lower()

    signals = {
        'verbs_present': [],
        'has_quotes': '"' in combined or '«' in combined,
        'length': len(combined),
    }

    # Look for common relationship verbs
    verb_patterns = {
        'encounter': r'\b(met|meets|meeting|encounter|faced|confront|see|saw)\b',
        'travel': r'\b(travel|journey|ride|ride together|rode|accompany|accompan)\b',
        'command': r'\b(command|led|leads|fight|fought|fighting|battle)\b',
        'serve': r'\b(serve|serves|served|follow|loyal|sworn)\b',
        'family': r'\b(brother|sister|father|mother|parent|child|son|daughter|uncle|aunt|cousin)\b',
        'authority': r'\b(rule|ruled|govern|king|queen|lord|master|lord|command)\b',
        'death': r'\b(kill|killed|murder|slain|died|dead|poison|execute)\b',
        'knowledge': r'\b(know|knows|knew|tell|told|inform|aware|learned|heard|secret)\b',
    }

    for verb_type, pattern in verb_patterns.items():
        if re.search(pattern, combined_lower):
            signals['verbs_present'].append(verb_type)

    return signals


def decide_comention_edge(pair_a, pair_b, snippets, valid_edge_types, target_type):
    """
    Decide on a comention edge classification.
    Returns (decision, data_dict) tuple.

    This function applies heuristics but requires manual verification for actual edge types.
    """

    # No valid edge types = must reject
    if not valid_edge_types:
        return ('reject_just_mention', {
            'reason': 'no-fitting-type-vocab-locked'
        })

    signals = extract_relationship_signals(snippets)

    # Very weak signal: no verbs, short snippet
    if not signals['verbs_present'] and signals['length'] < 100:
        return ('reject_just_mention', {
            'reason': 'temporal-cooccurrence-not-relational'
        })

    # If any mention-style signals appear, it's likely just a mention
    snippet_text = " ".join([s.get('snippet', '') for s in snippets]).lower()

    # Check for patterns that suggest NOT a real relationship
    if any(phrase in snippet_text for phrase in [
        'was mentioned',
        'was referred to',
        'was named',
        'is mentioned',
        'is named',
        '\'s thoughts',
        'remembered',
        'thought of',
    ]):
        return ('reject_just_mention', {
            'reason': 'just-mention-reference'
        })

    # Check for "and" co-mentions (often just lists)
    if re.search(r'\b\w+\s+and\s+\w+\b', snippet_text) and len(signals['verbs_present']) < 2:
        return ('reject_just_mention', {
            'reason': 'conjunctive-cooccurrence'
        })

    # If we reach here, there might be a real edge, but we need manual classification
    # Return a flag for manual review
    return ('manual_review', {
        'signals': signals,
        'note': f'Valid types available: {valid_edge_types}'
    })


def process_candidates_file(input_path, output_path):
    """Process a single comention candidates file."""

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        return False

    candidates = []
    with open(input_path) as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    if not candidates:
        print(f"No candidates in {input_path.name}", file=sys.stderr)
        return True

    print(f"\nProcessing {input_path.name}: {len(candidates)} candidates", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    emit_count = 0
    reject_count = 0
    manual_count = 0

    with open(output_path, 'w') as out_f:
        for idx, candidate in enumerate(candidates):
            pair_a = candidate.get('pair_a')
            pair_b = candidate.get('pair_b')
            evidence_chapter = candidate.get('evidence_chapter')
            evidence_paragraphs = candidate.get('evidence_paragraphs', [])
            valid_edge_types = candidate.get('valid_edge_types', [])
            target_type = candidate.get('target_type')

            # Apply decision logic
            decision, data = decide_comention_edge(
                pair_a, pair_b, evidence_paragraphs, valid_edge_types, target_type
            )

            if decision == 'reject_just_mention':
                # Output rejection
                output_row = {
                    'decision': 'reject_just_mention',
                    'candidate_kind': 'comention',
                    'pair_a': pair_a,
                    'pair_b': pair_b,
                    'evidence_chapter': evidence_chapter,
                    'reason': data['reason']
                }
                out_f.write(json.dumps(output_row) + '\n')
                reject_count += 1

            elif decision == 'manual_review':
                # For manual cases, output a debug note to stderr
                manual_count += 1
                if manual_count <= 5:  # Only print first few
                    print(f"  Manual: {pair_a} ↔ {pair_b} - {data.get('note')}", file=sys.stderr)

    print(f"  Completed: {reject_count} rejected, {manual_count} manual review needed", file=sys.stderr)
    return True


def main():
    # Input files (hardcoded for ACOK 32-36)
    input_dir = Path('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/meta-chapters-acok/comention-candidates')
    output_dir = Path('/Users/mnoth/source/asoiaf-chat/working/wiki/pass2-buckets/meta-chapters-acok/prose-edges-haiku')

    chapters = [32, 33, 34, 35, 36]

    for chapter_num in chapters:
        input_file = input_dir / f'a-clash-of-kings-chapter-{chapter_num}.candidates.jsonl'
        output_file = output_dir / f'a-clash-of-kings-chapter-{chapter_num}.comention-edges.jsonl'

        if input_file.exists():
            process_candidates_file(input_file, output_file)
        else:
            print(f"Warning: {input_file} not found", file=sys.stderr)

    print("\nBatch processing complete", file=sys.stderr)


if __name__ == '__main__':
    main()
