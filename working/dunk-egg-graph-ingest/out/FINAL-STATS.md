# D&E Graph-Ingest — FINAL-STATS (--assemble-final)

> Generated: 2026-07-19T21:11:21+00:00  
> run_id: dunk-egg-pass1-derived-s222  
> source: /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/out/emit.jsonl  
> verdicts: /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/repass-verdicts-s222.jsonl  
> alias source: /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/out/alias-adds.jsonl  

## Edge verdict counts

| Stage | Count |
|-------|-------|
| emit.jsonl rows (input) | 253 |
| repass-verdicts.jsonl rows (input) | 101 |
| Kept — no verdict (untouched by repass) | 152 |
| Kept — CONFIRM | 76 |
| Kept — unknown verdict string (defensive passthrough) | 0 |
| Fixed — FIX applied | 21 |
| Dropped — self-edge created by FIX (defensive) | 0 |
| Rejected — REJECT | 4 |
| Dedup-merged after fixes (triple collisions) | 2 |
| Moved to final-overlay.jsonl (now matches live edges.jsonl) | 6 |
| **final-edges.jsonl (emitted)** | **241** |
| Verdict rows with duplicate triples in verdicts file (last-wins) | 0 |
| Verdict rows that did NOT match any emit.jsonl triple | 0 |

## Alias counts

| Stage | Count |
|-------|-------|
| alias-adds.jsonl rows (input) | 65 |
| Kept -> final-aliases.jsonl | 58 |
| Dropped (total) | 7 |
|   -> reject-list-pair | 6 |
|   -> collision-graph-wide | 1 |

## Every FIX applied

| Edge Type | Old Source | Old Target | New Source | New Target | Reason |
|-----------|------------|------------|------------|------------|--------|
| PARENT_OF | eustace-osgrey | alysanne | eustace-osgrey | alysanne-osgrey | Target resolved to 'alysanne' disambiguation-hub stub (wrong candidate listed: daughter of Aegon IV) instead of the specific Osgrey daughter named in the quote. |
| KILLS | daemon-i-blackfyre | wild-hares | daemon-i-blackfyre | wyl-waynwood | Target resolved to 'wild-hares' (organization.faction) via stray 'Wild' match; quote names 'Wild Wyl Waynwood', an existing person node with alias 'Wild Wyl'. |
| PARENT_OF | daemon-i-blackfyre | aemon-targaryen-son-of-maekar-i | daemon-i-blackfyre | aemon-blackfyre | Target resolved to Aemon Targaryen (son of Maekar I, i.e. Maester Aemon) instead of Aemon Blackfyre, Daemon I's twin son who died at Redgrass Field carrying his father's sword. |
| KILLS | brynden-rivers | aemon-targaryen-son-of-maekar-i | brynden-rivers | aemon-blackfyre | Same misresolution as row 22: 'Young Aemon' at Redgrass Field is Aemon Blackfyre, not Aemon Targaryen son of Maekar I. |
| PARENT_OF | aegon-v-targaryen | brynden-rivers | aegon-iv-targaryen | brynden-rivers | Source resolved to Aegon V Targaryen (Egg) instead of Aegon IV Targaryen (the Unworthy); quote is about Bloodraven's 'royal father' legitimizing his bastards on his deathbed — that's Aegon IV. |
| SIBLING_OF | sefton-staunton | simon-leygood | sefton-staunton | simon-staunton | Target resolved to Simon Leygood (a living suitor of Rohanne) instead of Simon Staunton (Sefton's late brother, a previous septon); collision on shared first name 'Simon'. |
| SPOUSE_OF | simon-leygood | rohanne-webber | simon-staunton | rohanne-webber | Same Simon/Simon collision as row 29: the quote's 'Ser Simon Staunton' (Rohanne's deceased 3rd husband) was resolved to Simon Leygood instead. |
| SPOUSE_OF | rolland-storm | rohanne-webber | rolland-storm | rolland-uffering | Target resolved to Rolland Storm (Bastard of Nightsong, unrelated character) instead of Rolland Uffering, who the quote names explicitly as Rohanne's 4th husband. |
| SIBLING_OF | helicent-uffering | rolland-storm | helicent-uffering | rolland-uffering | Same Rolland/Rolland collision as row 31. |
| HEIR_TO | otho-bracken | bracken | otho-bracken | lord-bracken-father-of-otho | Target resolved to generic 'Bracken' stub instead of the specific 'Lord Bracken (father of Otho)' node that exists and matches the quote (Otho's dying father on the Trident). |
| PARENT_OF | aegon-v-targaryen | aegor-rivers | aegon-iv-targaryen | aegor-rivers | Same Aegon IV/Aegon V collision as row 28: 'He had legitimized the lot upon his deathbed' refers to Aegon IV (the Unworthy), not Aegon V. |
| PARENT_OF | aegon-v-targaryen | daemon-i-blackfyre | aegon-iv-targaryen | daemon-i-blackfyre | Same Aegon IV/Aegon V collision as rows 28 and 47. |
| OPPOSES | alyn-velaryon | duncan-the-tall | alyn-cockshaw | duncan-the-tall | Resolved to Alyn Velaryon (Oakenfist, Dance-of-Dragons-era admiral) instead of Alyn Cockshaw, the TMK antagonist who is the only 'Alyn'/'Lord Alyn' referenced anywhere in this chapter. |
| DEFEATS | glendon-flowers | alyn-velaryon | glendon-flowers | alyn-cockshaw | Same Velaryon/Cockshaw collision as row 60. |
| ATTACKS | alyn-velaryon | duncan-the-tall | alyn-cockshaw | duncan-the-tall | Same Velaryon/Cockshaw collision as row 60. |
| CONSPIRES_WITH | alyn-velaryon | daemon-ii-blackfyre | alyn-cockshaw | daemon-ii-blackfyre | Same Velaryon/Cockshaw collision as row 60. |
| SIBLING_OF | daemon-ii-blackfyre | aegon-v-targaryen | daemon-ii-blackfyre | aegon-blackfyre | Target resolved to Aegon V Targaryen (Egg) instead of Aegon Blackfyre, Daemon I's twin son; quote is Cockshaw recalling being bullied as a child by 'Aegon and Aemon' — the Blackfyre twins who died at Redgrass Field, not Egg. |
| LOVER_OF | alyn-velaryon | daemon-ii-blackfyre | alyn-cockshaw | daemon-ii-blackfyre | Same Velaryon/Cockshaw collision as row 60. |
| CONTRACTED_WITH | alyn-velaryon | uthor-underleaf | alyn-cockshaw | uthor-underleaf | Same Velaryon/Cockshaw collision as row 60. |
| SIBLING_OF | brynden-rivers | aerys-ii-targaryen | brynden-rivers | aegor-rivers | Target resolved to Aerys II Targaryen (the Mad King, main-series era) instead of the correct referent; the quote's 'my half brother' is Bittersteel (Aegor Rivers), not any Aerys at all — both a wrong-era and wrong-person error stacked together. |
| ADVISES | brynden-rivers | aerys-ii-targaryen | brynden-rivers | aerys-i-targaryen | Target resolved to Aerys II Targaryen (Mad King, ~262-283 AC) instead of Aerys I Targaryen, the reigning king in TMK's setting (~211 AC) whom Bloodraven serves as Hand. |

## Every REJECT applied

| Edge Type | Source | Target | Reason |
|-----------|--------|--------|--------|
| KILLS | rohanne-webber | her-little-flower | Target 'her-little-flower' is a song (type object.text), unrelated to the quote; the quote's actual victims ('three of her husbands') are unnamed and not resolvable to a specific node. |
| SPOUSE_OF | rowans-forced-confession | wendell-webber | Source 'rowans-forced-confession' is an unrelated Fire & Blood-era event.trial node (false confession unravelled by Viserys); the actual subject ('Lord Rowan's sister') is an unnamed person with no matching node. |
| SERVES | sefton-staunton | high-septon | Target 'high-septon' is the generic title node (type: title), not a person; the text never names a specific contemporary High Septon, so no person-node fix is available. |
| SWORN_TO | kyle-the-cat | joffrey-caswell | Quote explicitly says Kyle's sword 'was sworn to his father' (Joffrey Caswell's unnamed father), not to Joffrey Caswell himself; no node exists for the unnamed father. |

## Every dropped alias

| Slug | Alias | Drop Reason | Colliding Slugs |
|------|-------|--------------|------------------|
| arlan-of-pennytree | The old man | reject-list-pair |  |
| arlan-of-pennytree | old man | reject-list-pair |  |
| aegon-v-targaryen | Aegon | reject-list-pair |  |
| wet-wat | The younger Wat brother | reject-list-pair |  |
| wet-wat | younger Wat brother | reject-list-pair |  |
| aegon-v-targaryen | Aegon Targaryen | reject-list-pair |  |
| uthor-underleaf | Snail | collision-graph-wide | snail |

## Commands run

```
python3 scripts/dunk-egg-graph-ingest.py --assemble-final --out-dir /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/out --verdicts /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/repass-verdicts-s222.jsonl
```

