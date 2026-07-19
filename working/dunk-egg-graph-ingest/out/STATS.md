# D&E Graph-Ingest — STATS

> Generated: 2026-07-19T20:55:13+00:00  
> run_id: dunk-egg-pass1-derived-s222  
> schema_version: pass1-derived-v1  
> curated_map: working/dunk-egg-graph-ingest/curated-map.csv (133 rows)  

## Pipeline counts

| Stage | Count |
|-------|-------|
| Extraction files walked | 24 |
| Relationships-table rows parsed | 666 |
| Malformed relationship cells | 0 |
| Identity rows (SAME_AS/ALIAS_OF) | 80 |
|  -> resolved to same slug (alias-check) | 74 |
|  -> alias-add candidates emitted | 65 |
|  -> flagged for adjudication | 6 |
| Non-identity rows resolved (both endpoints) | 509 |
| Grounded at confidence_tier=1 | 427 |
| Unique (source,type,target) triples after in-run dedup | 282 |
| Duplicate rows collapsed within-run | 145 |
| Deduped vs live edges.jsonl (-> overlay-candidates) | 29 |
| Emitted (emit.jsonl) | 253 |
| Quarantined (total) | 159 |
| Tier-3 qualifiers dropped (anomaly, not quarantined) | 2 |
| Distinct unresolved names (needs-map.csv) | 15 |

## Quarantine reasons

| Reason | Count |
|--------|-------|
| curated-map-skip | 59 |
| no-quoted-fragment-ungroundable | 47 |
| quoted-fragment-not-grounded | 32 |
| ambiguous-target | 7 |
| unresolved-target | 6 |
| ambiguous-source | 3 |
| self-edge-after-resolution | 3 |
| unresolved-source | 2 |

## Per-book breakdown

| Book | Rows Parsed | Identity Rows | Resolved (non-identity) | Grounded Tier-1 |
|------|-------------|----------------|--------------------------|------------------|
| THK | 178 | 22 | 148 | 117 |
| TSS | 239 | 23 | 185 | 161 |
| TMK | 249 | 35 | 176 | 149 |

## identity-flags.jsonl: different-slugs rows

3 row(s) where both sides resolved but to DIFFERENT slugs (orchestrator adjudication required):

| Book | Char A (raw) | -> slug | Char B (raw) | -> slug | Relationship | Extraction file |
|------|--------------|---------|--------------|---------|--------------|------------------|
| thk | Dragonbane | aegon-iii-targaryen | King Aegon (the third) | aegon-v-targaryen | ALIAS_OF | extractions/mechanical/thk/thk-dunk-01-p01.extraction.md |
| tss | Treb | treb | Will (the rock-chucker) | will | ALIAS_OF | extractions/mechanical/tss/tss-dunk-01-p02.extraction.md |
| tmk | "the Brown Dragon" | daemon-ii-blackfyre | Ser Glendon Ball | glendon-flowers | ALIAS_OF | extractions/mechanical/tmk/tmk-dunk-01-p09.extraction.md |

## Top 30 unresolved names (needs-map.csv)

| Name | Count | Sample evidence | Sample file |
|------|-------|------------------|-------------|
| Aegon (son of Daemon Blackfyre) | 3 | "He slew Aegon first, the elder of the twins"; "Daemon and his sons" | extractions/mechanical/tss/tss-dunk-01-p04.extraction.md |
| Raymun's cousin (Fossoway) | 2 | "I think I cracked a few of my cousin's ribs" | extractions/mechanical/thk/thk-dunk-01-p07.extraction.md |
| The bride (Lady Butterwell) | 2 | "that little brother of hers crept down after her" | extractions/mechanical/tmk/tmk-dunk-01-p04.extraction.md |
| Ring-stealing outlaw | 1 | "one outlaw Ser Arlan had helped hang" | extractions/mechanical/tss/tss-dunk-01-p01.extraction.md |
| Eustace's cousin (unnamed) | 1 | "A cousin, she was, my uncle's youngest daughter, of the Osgreys of Leafy Lake" | extractions/mechanical/tss/tss-dunk-01-p02.extraction.md |
| Daeron's Dornish wife | 1 | "he had taken a Dornishwoman into his bed … his Dornish wife" | extractions/mechanical/tss/tss-dunk-01-p06.extraction.md |
| a Frey (bride) | 1 | "This will be a marriage of cattle thieves and toll collectors"; "Unless this ne | extractions/mechanical/tmk/tmk-dunk-01-p02.extraction.md |
| Ser Willam Wylde | 1 | "King Daeron named Ser Willam Wylde instead" (to the Kingsguard) | extractions/mechanical/tmk/tmk-dunk-01-p03.extraction.md |
| An archer (a common man) | 1 | "An archer put an arrow through his throat as he dismounted by a stream to have  | extractions/mechanical/tmk/tmk-dunk-01-p03.extraction.md |
| the old Lord of Casterly Rock (the Grey Lion) | 1 | "once unhorsed the Lord of Casterly Rock . . . the old Grey Lion" | extractions/mechanical/tmk/tmk-dunk-01-p03.extraction.md |
| forty men (at the Redgrass Field, by repute) | 1 | "The Old Ox slew forty men upon the Redgrass Field" | extractions/mechanical/tmk/tmk-dunk-01-p03.extraction.md |
| "the prince" (the conspirators' claimant) | 1 | (inferred) conspirators: "the prince... dreamed his brothers dead"; Fiddler: "I  | extractions/mechanical/tmk/tmk-dunk-01-p04.extraction.md |
| The scullion (at the Twins) | 1 | "His bride was deflowered by a scullion at the Twins... She would creep down to  | extractions/mechanical/tmk/tmk-dunk-01-p04.extraction.md |
| An old squire (near the Pussywillows) | 1 | "An old squire who lived nearby gave the boy his training ... in trade for ale a | extractions/mechanical/tmk/tmk-dunk-01-p06.extraction.md |
| the white cloak (Kingsguard) | 1 | "I mean to claim the white cloak that he never got to wear" | extractions/mechanical/tmk/tmk-dunk-01-p07.extraction.md |

## Parsing anomalies

- extractions/mechanical/tmk/tmk-dunk-01-p05.extraction.md: Tier-3 edge type 'SERVES' carried a qualifier 'former' (dropped) — row Ser Kyle / Lord Joffrey Caswell
- extractions/mechanical/tmk/tmk-dunk-01-p09.extraction.md: Tier-3 edge type 'SERVES' carried a qualifier 'former' (dropped) — row Dunk / Ser Arlan

## Commands run

```
python3 scripts/dunk-egg-graph-ingest.py --map working/dunk-egg-graph-ingest/curated-map.csv --out-dir /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/out
```

