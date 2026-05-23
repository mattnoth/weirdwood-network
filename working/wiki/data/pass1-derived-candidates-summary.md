# Pass-1-Derived Edge Candidates Summary

> Generated: 2026-05-23T04:26:34+00:00  
> run_id: pass1-derived-20260523  
> schema_version: pass1-derived-v1  

## Counts

| Stage | Count |
|-------|-------|
| Extraction files walked | 344 |
| Total Relationships rows seen | 7,398 |
| Drop: source unresolved | 148 |
| Drop: target unresolved | 390 |
| Drop: source generic-term | 5 |
| Drop: target generic-term | 13 |
| Drop: source ambiguous-queued | 306 |
| Drop: target ambiguous-queued | 345 |
| Ambiguous-queued rows | 633 |
| Drop: self-edge | 10 |
| Resolved pairs (total) | 6,199 |
| → Routed to needs-qualifier tail | 352 |
| → Main candidates | 5,847 |
|    of which typed | 2,818 |
|    of which untyped | 3,029 |
| Corroborating (wiki-known) | 1,966 |
| New (not in existing edges) | 4,233 |
| Conform drift issues | 0 |
| Total distinct unresolved names | 453 |

## Resolution-Status Histogram

Counts are per-endpoint (each edge has two endpoints).

| Status | Endpoint Count |
|--------|---------------|
| resolved-exact | 6,613 |
| resolved-alias | 780 |
| resolved-firstname-unique | 1,175 |
| resolved-context-present | 3,039 |
| resolved-context-prior | 791 |
| unresolved-generic (dropped) | 18 |

## Per-Book Breakdown

| Book | Resolved | Typed | Untyped | Corroborating | New |
|------|----------|-------|---------|--------------|-----|
| AGOT | 1,212 | 703 | 609 | 460 | 752 |
| ACOK | 1,161 | 635 | 575 | 334 | 827 |
| ASOS | 1,464 | 764 | 766 | 452 | 1,012 |
| AFFC | 774 | 401 | 451 | 225 | 549 |
| ADWD | 1,236 | 667 | 628 | 276 | 960 |

## Edge Type Distribution

| Edge Type | Count |
|-----------|-------|
| SERVES | 273 |
| MOURNS | 253 |
| OPPOSES | 237 |
| COMMANDS | 204 |
| HATES | 195 |
| DISTRUSTS | 169 |
| PROTECTS | 158 |
| RESPECTS | 136 |
| LOVES | 134 |
| SIBLING_OF | 133 |
| PARENT_OF | 133 |
| COMPANION_OF | 118 |
| FEARS | 103 |
| KILLS | 100 |
| RESENTS | 90 |
| ALLIES_WITH | 77 |
| ADVISES | 70 |
| TRUSTS | 55 |
| BONDED_TO | 50 |
| LOVER_OF | 46 |
| BETROTHED_TO | 42 |
| TUTORS | 39 |
| SPOUSE_OF | 33 |
| SEEKS | 32 |
| UNCLE_OF | 30 |
| MANIPULATES | 30 |
| COUSIN_OF | 26 |
| CAPTURES | 21 |
| WARGS_INTO | 19 |
| NEPHEW_OF | 18 |
| PRISONER_OF | 15 |
| CONSPIRES_WITH | 14 |
| SWORN_TO | 13 |
| BETRAYS | 11 |
| GUARDS | 10 |
| WARD_OF | 10 |
| RESCUES | 9 |
| IN_LAW_OF | 6 |
| GIFTED_TO | 6 |
| TEACHES | 6 |
| EXECUTES | 4 |
| NEGOTIATES_WITH | 4 |
| MEMBER_OF | 4 |
| CONTRACTED_WITH | 3 |
| ATTACKS | 3 |
| HEALS | 3 |
| HEIR_TO | 3 |
| DISGUISED_AS | 3 |
| IMPRISONS | 3 |
| RULES | 3 |
| DEFEATS | 2 |
| TRAVELS_WITH | 2 |
| OWNS | 2 |
| SPIES_ON | 2 |
| WORSHIPS | 2 |
| DREAMS_OF | 1 |
| DECEIVES | 1 |
| GUEST_OF | 1 |

## Top 50 Unresolved Entity Names

| Entity Name (raw) | Count | Example Chapter |
|-------------------|-------|----------------|
| Lady Dustin | 12 | adwd-a-ghost-in-winterfell-01 |
| Cat/Arya | 11 | affc-cat-of-the-canals-01 |
| Drogon, Rhaegal, Viserion | 5 | agot-daenerys-10 |
| Bolton | 5 | acok-arya-10 |
| Lord Manderly | 5 | acok-bran-02 |
| Hotah | 5 | affc-the-captain-of-guards-01 |
| Everyone | 4 | agot-bran-02 |
| Himself | 4 | agot-eddard-13 |
| (general) | 4 | acok-bran-03 |
| Dragons | 4 | acok-daenerys-01 |
| Tris Botley | 4 | affc-the-iron-captain-01 |
| (self) | 3 | agot-bran-07 |
| Bran, Rickon | 3 | agot-bran-07 |
| Wildling host | 3 | acok-jon-05 |
| — | 3 | asos-arya-01 |
| Lame Lothar Frey | 3 | asos-catelyn-05 |
| Translator (slave girl) | 3 | asos-daenerys-02 |
| Arstan/Barristan | 3 | asos-daenerys-05 |
| Slynt | 3 | asos-jon-09 |
| Ser Gregor, Dunsen, Raff the Sweetling, Ser Ilyn, Ser Meryn, Queen Cersei | 3 | affc-arya-01 |
| Shagwell, Timeon, Pyg | 3 | affc-brienne-04 |
| Lord Peasebury | 3 | adwd-the-kings-prize-01 |
| Blond bedwarmer | 3 | adwd-tyrion-01 |
| Stout man (torchbearer) | 2 | agot-arya-03 |
| Bran's direwolf (unnamed) | 2 | agot-bran-02 |
| Bran's direwolf | 2 | agot-catelyn-03 |
| Irri, Jhiqui, Doreah | 2 | agot-daenerys-02 |
| Jon's friend group | 2 | agot-jon-09 |
| Rorge, Biter | 2 | acok-arya-02 |
| Sansa, Arya | 2 | acok-catelyn-03 |
| Lord Meadows | 2 | acok-davos-02 |
| Gendry, Hot Pie | 2 | asos-arya-01 |
| Caged northmen | 2 | asos-arya-05 |
| Village elder's daughter | 2 | asos-arya-12 |
| Unnamed squire | 2 | asos-arya-13 |
| Jhogo, Aggo, Rakharo | 2 | asos-daenerys-04 |
| Aggo, Jhogo, Rakharo | 2 | asos-daenerys-05 |
| Kingslanders | 2 | asos-tyrion-01 |
| Lord Rykker | 2 | affc-brienne-02 |
| Lord Mooton | 2 | affc-brienne-03 |
| Cersei, Jaime | 2 | affc-cersei-01 |
| Drey / Ser Andrey Dalt | 2 | affc-the-princess-in-the-tower-01 |
| Darkstar / Ser Gerold Dayne | 2 | affc-the-princess-in-the-tower-01 |
| Tytos's mistress | 2 | adwd-cersei-02 |
| Qezza, Grazhar | 2 | adwd-daenerys-04 |
| Manderly | 2 | adwd-davos-04 |
| Ramsay's mother | 2 | adwd-reek-03 |
| Yunkai'i | 2 | adwd-the-kingbreaker-01 |
| Strickland | 2 | adwd-the-lost-lord-01 |
| Ship's crew | 2 | adwd-tyrion-08 |
