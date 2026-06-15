#!/usr/bin/env python3
"""Merge + mint historical-anchor candidate edges into graph/edges/edges.jsonl.

Reads working/historical-anchor/*.candidates.jsonl, applies a curator DROP list and
quote-FIX list (from the validation pass), dedupes against existing edges, writes a
merged file, and with --apply backs up + appends to edges.jsonl.

Default (no --apply) = dry run: writes _merged.candidates.jsonl + prints counts.
"""
import json, glob, os, sys, datetime
from pathlib import Path

ROOT = Path('.')
EDGES = ROOT / 'graph/edges/edges.jsonl'
MERGED = ROOT / 'working/historical-anchor/_merged.candidates.jsonl'

# (hub, source_slug, edge_type, target_slug) -> drop
DROP = {
    ('greyjoy-rebellion', 'theon-greyjoy', 'FIGHTS_IN', 'greyjoy-rebellion'),  # hostage, not combatant
    ('tourney-at-harrenhal', 'lewyn-martell', 'ATTENDS', 'tourney-at-harrenhal'),   # meta-desc quote, minor
    ('tourney-at-harrenhal', 'jonothor-darry', 'ATTENDS', 'tourney-at-harrenhal'),  # meta-desc quote, minor
    ('battle-of-the-trident', 'jon-arryn', 'COMMANDS_IN', 'battle-of-the-trident'),  # wedding quote, no command support
    ('tragedy-at-summerhall', 'rhaegar-targaryen', 'ATTENDS', 'tragedy-at-summerhall'),  # born, not attendee
    ('tragedy-at-summerhall', 'jaehaerys-ii-targaryen', 'ATTENDS', 'tragedy-at-summerhall'),  # speculative
}

# (hub, source_slug, edge_type, target_slug) -> field overrides (verbatim-grounded fixes)
FIX = {
    ('the-hands-tourney', 'hugh-of-the-vale', 'FIGHTS_IN', 'the-hands-tourney'): {
        'evidence_quote': "the silent sisters had dressed him in his best velvet tunic, with a high collar to cover the ruin the lance had made of his throat",
        'evidence_ref': 'sources/chapters/agot/agot-eddard-07.md:13',
        'evidence_chapter': 'agot-eddard-07', 'evidence_book': 'agot',
    },
    ('tourney-at-harrenhal', 'tourney-at-harrenhal', 'LOCATED_AT', 'harrenhal'): {
        'evidence_quote': "the tourney staged by Lord Whent at Harrenhal beside the Gods Eye",
        'evidence_ref': 'wiki:Tourney_at_Harrenhal',
    },
    ('tourney-at-harrenhal', 'walter-whent', 'ATTENDS', 'tourney-at-harrenhal'): {
        'evidence_quote': "The tourney was announced in 280 AC by Lord Walter Whent",
        'evidence_ref': 'wiki:Tourney_at_Harrenhal',
    },
    ('tragedy-at-summerhall', 'tragedy-at-summerhall', 'LOCATED_AT', 'summerhall'): {
        'evidence_quote': "a fire at Summerhall, a pleasure castle of House Targaryen in the Dornish Marches",
        'evidence_ref': 'wiki:Tragedy_at_Summerhall',
    },
}

RUN_ID = 'historical-anchor-w1-20260615'


def key(hub, e):
    return (hub, e.get('source_slug'), e.get('edge_type'), e.get('target_slug'))


def main():
    apply = '--apply' in sys.argv

    existing = set()
    with open(EDGES, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            existing.add((e.get('source_slug'), e.get('edge_type'), e.get('target_slug')))

    merged = []
    dropped = 0
    deduped = 0
    fixed = 0
    for fp in sorted(glob.glob('working/historical-anchor/*.candidates.jsonl')):
        if fp.endswith('_merged.candidates.jsonl'):
            continue
        hub = os.path.basename(fp).replace('.candidates.jsonl', '')
        for line in open(fp, encoding='utf-8'):
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            k = key(hub, e)
            if k in DROP:
                dropped += 1
                continue
            if k in FIX:
                e.update(FIX[k])
                fixed += 1
            de = (e.get('source_slug'), e.get('edge_type'), e.get('target_slug'))
            if de in existing:
                deduped += 1
                continue
            e['run_id'] = RUN_ID
            merged.append(e)
            existing.add(de)  # guard against intra-batch dups

    MERGED.write_text('\n'.join(json.dumps(e, ensure_ascii=False) for e in merged) + '\n', encoding='utf-8')

    from collections import Counter
    print(f"merged: {len(merged)}   dropped: {dropped}   deduped(existing): {deduped}   fixed: {fixed}")
    print('edge types:', dict(Counter(e['edge_type'] for e in merged)))
    print('provenance:', dict(Counter(e['evidence_kind'] for e in merged)))
    print('tiers:', dict(Counter(e.get('confidence_tier') for e in merged)))
    print('per-hub:', dict(Counter(e['target_slug'] if e['edge_type'] in ('FIGHTS_IN','ATTENDS','AGENT_IN','VICTIM_IN','COMMANDS_IN') else e['source_slug'] for e in merged)))
    print(f"\nwrote {MERGED}")

    if apply:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%S')
        bak = ROOT / f'graph/edges/_regrounding/edges-pre-historical-anchor-{ts}.jsonl'
        bak.parent.mkdir(parents=True, exist_ok=True)
        bak.write_bytes(EDGES.read_bytes())
        before = sum(1 for _ in open(EDGES, encoding='utf-8'))
        with open(EDGES, 'a', encoding='utf-8') as f:
            for e in merged:
                f.write(json.dumps(e, ensure_ascii=False) + '\n')
        after = sum(1 for _ in open(EDGES, encoding='utf-8'))
        print(f"\nAPPLIED: edges.jsonl {before} -> {after} (+{after-before})")
        print(f"backup: {bak}")
    else:
        print("\n(dry run — pass --apply to append to edges.jsonl)")


if __name__ == '__main__':
    main()
