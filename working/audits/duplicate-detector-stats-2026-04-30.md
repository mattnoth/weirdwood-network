# Duplicate Detector Stats - 2026-04-30

Read-only audit of `graph/nodes/**/*.node.md` (excluding `_conflicts/`, `_unclassified/`).
Output JSONL: `working/wiki-pass2/duplicate-candidates.jsonl`.

## Scan summary

- Node files discovered: 4236
- Nodes successfully indexed: 4236
- Malformed nodes (logged to `questions-for-matt.jsonl`): 0
- Distinct `wiki_source` URLs: 4236
- Distinct normalized aliases / names: 4524

## Candidates by category

| Category | Count | Confidence |
|---|---|---|
| shared-wiki-source | 0 | high |
| alias-bridge | 16 | medium |
| slug-similarity | 2868 | low |
| **total** | **2884** | |

## Top 10 candidates by confidence

1. **medium** - `aegon-targaryen-son-of-rhaegar` <-> `rhaegar-targaryen` [alias-bridge] - alias-key: `the-prince-that-was-promised`
2. **medium** - `arya-stark` <-> `lyanna-stark` [alias-bridge] - alias-key: `wolf-girl`
3. **medium** - `arya-stark` <-> `nymeria` [alias-bridge] - alias-key: `nymeria`
4. **medium** - `arya-stark` <-> `nymeria-direwolf` [alias-bridge] - alias-key: `nymeria`
5. **medium** - `arya-stark` <-> `sansa-stark` [alias-bridge] - alias-key: `wolf-girl`
6. **medium** - `arya-stark` <-> `weasel` [alias-bridge] - alias-key: `weasel`
7. **medium** - `asha-greyjoy` <-> `esgred` [alias-bridge] - alias-key: `esgred`
8. **medium** - `bronn` <-> `lord-stokeworth` [alias-bridge] - alias-key: `lord-stokeworth`
9. **medium** - `jonnel-stark` <-> `one-eye` [alias-bridge] - alias-key: `one-eye`
10. **medium** - `jonquil` <-> `sansa-stark` [alias-bridge] - alias-key: `jonquil`

## Cross-identity spot-check

Confirmed present as separate nodes (handled by future `cross-identity-detector` agent):

- `theon-greyjoy` and `reek`

Candidate rows touching cross-identity slugs: 28

## Estimated false-positive rate per category

| Category | Heuristic FP rate | Rationale |
|---|---|---|
| shared-wiki-source | <5% | Same source URL is near-deterministic evidence both nodes parse the same wiki page; only false-positive class is intentional duplicate-from-different-bucket retention. |
| alias-bridge | 30-50% | Cross-identity disguises (Theon/Reek, Sansa/Alayne) and canonical alias splits live here; the cross-identity-detector decides per pair. |
| slug-similarity | 70-90% | Mostly namesakes (cousins/dynasties), houses with similar surnames, and ordinal numerals; cross-identity-detector rejects the bulk. |

## Notes / patterns

- Type mismatches (e.g., `character.*` vs `place.*`) are dropped before emission.
- Pairs differing only in a Roman/Arabic ordinal token (e.g., `aegon-i-targaryen` vs `aegon-ii-targaryen`) are dropped - distinct dynasts, never duplicates.
- Pairs disambiguated by `son-of-X` / `daughter-of-Y` / `wife-of-X` suffixes with the same prefix are dropped - explicitly-named namesakes.
- `_conflicts/` and `_unclassified/` directories were excluded from the scan per the contract.
