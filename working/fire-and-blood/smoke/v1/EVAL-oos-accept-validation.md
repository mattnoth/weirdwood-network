# EVAL — Out-of-sample accept validation (fresh units: heirs-15-p02, sons-05-p01)

**VERDICT: 0 wrong accepts.** All 8 discriminator would-accepts and all 58 exact-1.0 would-accepts resolve to the contextually correct node. Every case where an accept would have corrupted the graph (Lord Bracken, Lord Blackwood, Manfred Hightower, Ronnel Arryn, Vulture King) was correctly routed to review by the rules. **Gate: PASS.**

- Verifier: read-only adversarial pass, 2026-07-07. Method: chapter text → contextual referent → node frontmatter/Identity ground truth (`graph/nodes/**`), wiki cache not needed beyond node files.
- Discriminator rows: all 16 verified individually (8 would-accept under the rule, 8 route-to-review). Note: parent estimate said "~9 discriminator accepts"; strict application of the rule (top has ≥2 hits, strictly outscores runner-up, runner-up brings no unique evidence) yields **8** — Corlys Velaryon, Jason Lannister, and Balerion each carry only 1 hit (`pack-expected`) so they fall to review, though all three tops are in fact the correct entity (conservative misses, not errors).
- Exact rows: all 58 verified against node identity; generic/era-sensitive names (greens, blacks, High Tide, narrow sea, the Trident, Citadel, Leng, Gods Eye, Maegor's Holdfast, Aegonfort, Stonehelm, Nightsong, Runestone) individually confirmed; unambiguous seats/cities batch-confirmed against node files.

## Unit: fab-heirs-of-the-dragon-15-p02

### Discriminator rows (rule applied to scored_candidates)

| Name | Top slug | Would-accept? | Verdict | Evidence |
|---|---|---|---|---|
| Rhaenys Targaryen | rhaenys-targaryen-daughter-of-aemon | YES (2 disamb hits + pack, 2>0) | CORRECT | Node: 74–129 AC, child of Aemon (son of Jaehaerys I), m. Corlys — the Queen Who Never Was; chapter: passed over for Baelon 92 AC, mother of Laena/Laenor |
| Laena Velaryon | laena-velaryon | YES (2 disamb hits + pack, 2>0) | CORRECT | Node: 92–120 AC, child of Corlys & Rhaenys (d.o. Aemon), m. Daemon; chapter: turned twelve ~105 AC (b. 92 ✓), claimed Vhagar. Runner-up (daughter of Alyn, b. 134) wrong era |
| Corlys Velaryon | corlys-velaryon | no (1 hit) → review | (top is correct anyway) | Node: 53–132 AC, m. Rhaenys (d.o. Aemon) = the Sea Snake; conservative miss, no gate risk |
| Jason Lannister | jason-lannister | no (1 hit) → review | (top is correct anyway) | Node: d. 130 AC, m. Johanna — the Dance-era twin of Tyland; chapter era 112 AC ✓ |
| Lord Bracken | (all score 0) → review | no | REVIEW CORRECT — accept would be WRONG | Candidates are Aerys II-era, father-of-Otho (~209 AC), Hand d. 178 AC; none is the 112 AC lord whose son dueled at the Trident |
| Lord Blackwood | (all score 0) → review | no | REVIEW CORRECT — accept would be WRONG | Candidates are Conquest-era and Aerys II-era; neither is the 112 AC lord |

### Exact-1.0 rows (33) — all CORRECT

| Name | Slug | Verdict | Evidence |
|---|---|---|---|
| Dark Sister | dark-sister | CORRECT | Targaryen Valyrian sword; Daemon's blade in context |
| House Hightower | house-hightower | CORRECT | Oldtown house, Otto/Alicent's |
| House Velaryon | house-velaryon | CORRECT | Driftmark seahorse house |
| House Frey | house-frey | CORRECT | Fool Frey's house; only one House Frey |
| greens | greens | CORRECT | Node: Alicent/Aegon II Dance faction, named for Alicent's green gown — exactly the party coined at the 111 AC tourney in this unit |
| blacks | blacks | CORRECT | Node: Rhaenyra's Dance faction — the "party of the princess" |
| Maidenpool | maidenpool | CORRECT | Riverlands town; accession melee site |
| Maegor's Holdfast | maegors-holdfast | CORRECT | Red Keep inner holdfast; exists by 105 AC (built under Maegor) |
| Street of Silk | street-of-silk | CORRECT | KL brothel street |
| Dragonstone | dragonstone | CORRECT | Targaryen island seat |
| Runestone | runestone | CORRECT | Royce seat in the Vale — Daemon's "bronze bitch" wife's seat |
| Vale of Arryn | vale-of-arryn | CORRECT | Region |
| Lys / Myr / Tyrosh | lys / myr / tyrosh | CORRECT | The three Free Cities of the Triarchy |
| High Tide | high-tide | CORRECT | Node: "seat of the Sea Snake, Lord Corlys Velaryon" on Driftmark — the war-council site |
| Driftmark | driftmark | CORRECT | Velaryon island |
| Blackwater Bay | blackwater-bay | CORRECT | Bay off KL |
| Stepstones | stepstones | CORRECT | Islands between Dorne and Disputed Lands — Daemon's war theater |
| Disputed Lands | disputed-lands | CORRECT | Essosi contested region |
| Dorne | dorne | CORRECT | Region; joined the Triarchy |
| narrow sea | narrow-sea | CORRECT | Node: sea between Westeros/Essos — Mysaria's storm |
| King's Landing | kings-landing | CORRECT | Capital |
| Casterly Rock | casterly-rock | CORRECT | Lannister seat; feast site |
| the Trident | trident | CORRECT | Node is the river (Tristifer Mudd / river kings) — "visited the Trident in 112" = the river region, not a battle |
| White Sword Tower | white-sword-tower | CORRECT | Kingsguard tower in Red Keep (Mushroom's Criston tale) |
| Red Keep | red-keep | CORRECT | Royal castle |
| Citadel | citadel | CORRECT | Oldtown maesters' institution — Lyonel's six links; maester's letter |
| Leng | leng | CORRECT | Node: isolated far-east island (Lengii) — Empress of Leng's jade tiara |
| Oldtown | oldtown | CORRECT | Hightower city |
| Blackhaven | blackhaven | CORRECT | Dondarrion seat (Criston Cole's origin) |
| Pentos / Braavos | pentos / braavos | CORRECT | Free Cities; envoys' letters |

## Unit: fab-sons-of-the-dragon-05-p01

### Discriminator rows (rule applied to scored_candidates)

| Name | Top slug | Would-accept? | Verdict | Evidence |
|---|---|---|---|---|
| Rhaenys Targaryen | rhaenys-targaryen | YES (spouse:aegon + pack, 2>0) | CORRECT | Node: d. 10 AC, m. Aegon I — the conquest queen; chapter: slain in Dorne with Meraxes when Aenys (b. 7) was three ✓ |
| Visenya Targaryen | visenya-targaryen | YES (spouse:aegon + pack, 2>0) | CORRECT | Node: 29 BC–44 AC, m. Aegon I; runner-up (daughter of Daemon, 129 AC infant) has no evidence |
| Maegor Targaryen | maegor-i-targaryen | YES (score 4 vs 1) | CORRECT | Node: 12–48 AC, child of Aegon I & Visenya. Runner-up (son of Aerion, b. 232) hits only `disambiguator~prince`, which the top also has — no unique evidence, rule satisfied |
| Rhaena Targaryen | rhaena-targaryen-daughter-of-aenys-i | YES (score 3 vs 0) | CORRECT | Node: 23–73 AC, child of Aenys I & Alyssa — Dreamfyre's rider; other Rhaenas (d.o. Aegon III b. 147, d.o. Daemon b. 116) wrong |
| Vaella Targaryen | vaella-targaryen-daughter-of-aenys-i | YES (score 2 vs 0) | CORRECT | Node: 39–39 AC, child of Aenys I & Alyssa, died in cradle — exact match; other Vaella b. 222 |
| Samwell Tarly | samwell-tarly-lord | YES (lord-of-horn-hill + pack, 2>0) | CORRECT | Node: alias "Savage Sam", Lord of Horn Hill, Heartsbane, Vulture Hunt 37 AC — the historical lord, NOT ASOIAF Sam (b. 283, Novice, never lord). Era-sensitive case handled right |
| Manfred Hightower | (both score 0) → review | no | REVIEW CORRECT — pack contains a trap | Correct entity is manfred-hightower-son-of-addam (d. 41 AC — Ceryse's father); manfred-hightower-aegons-conquest is the grandsire the text explicitly warns against confusing |
| Ronnel Arryn | (score 0) → review | no | REVIEW CORRECT — accept would be WRONG | Only candidate ronnel-arryn-son-of-jasper = Jon Arryn's era Keeper of the Gates of the Moon; the 37 AC King-Who-Flew (thrown from the Moon Door by Jonos) appears to have NO node in the graph — accept impossible to be right |
| Vulture King | (tie 1-1-1) → review | no | REVIEW CORRECT — see reverse check below | No strict outscore; correct entity vulture-king-aenys-i sat in a 3-way tie |
| Balerion | balerion | no (1 hit) → review | (top is correct anyway) | Node: the dragon, the Black Dread, Aegon I's mount; balerion-cat obviously wrong. Conservative miss |

### Exact-1.0 rows (25) — all CORRECT

| Name | Slug | Verdict | Evidence |
|---|---|---|---|
| Aenys Targaryen (Aenys I) | aenys-i-targaryen | CORRECT | Node: 7–42 AC, child of Aegon I & Rhaenys |
| Viserys Targaryen (son of Aenys) | viserys-targaryen-son-of-aenys-i | CORRECT | Node: 29–44 AC, child of Aenys I & Alyssa — the second son b. 29 AC |
| Blackfyre | blackfyre | CORRECT | Aegon the Conqueror's Valyrian sword |
| Dark Sister | dark-sister | CORRECT | Visenya's blade given to Maegor at 13 |
| Heartsbane | heartsbane | CORRECT | House Tarly heirloom — Savage Sam's blade |
| Dragonstone | dragonstone | CORRECT | Targaryen seat, dragon pits |
| King's Landing | kings-landing | CORRECT | The capital |
| Aegonfort | aegonfort | CORRECT | Node: motte-and-bailey on Aegon's High Hill, torn down 35 AC |
| Red Keep | red-keep | CORRECT | Stone castle ordered on the Aegonfort site |
| Harrenhal | harrenhal | CORRECT | Qoherys grant; Harren the Red |
| Oldtown | oldtown | CORRECT | Hightower/Starry Sept city |
| Starry Sept | starry-sept | CORRECT | Oldtown sept — Maegor/Ceryse wedding, Aenys anointing |
| Riverrun | riverrun | CORRECT | Tully seat, 28 AC tourney |
| Highgarden | highgarden | CORRECT | Tyrell seat; Aenys on progress |
| Storm's End | storms-end | CORRECT | Baratheon seat |
| the Eyrie | eyrie | CORRECT | Arryn seat, Moon Door |
| Stonehelm | stonehelm | CORRECT | Swann seat in the stormlands, besieged by Walter Wyl |
| Nightsong | nightsong | CORRECT | Caron seat (node RULES Bryce Caron) — failed siege |
| Horn Hill | horn-hill | CORRECT | Tarly seat |
| Blackhaven | blackhaven | CORRECT | Dondarrion seat — node's own Origins cite the first Vulture King burning it |
| Gods Eye | gods-eye | CORRECT | The lake — Harren the Red cornered west of it |
| Sunspear | sunspear | CORRECT | Martell seat — Deria's "feast of friendship" |
| Pentos | pentos | CORRECT | Maegor's exile city |
| Stepstones | stepstones | CORRECT | Sargoso Saan pirate campaign 29–30 AC |
| Driftmark | driftmark | CORRECT | Velaryon seat — Larissa recalled there |

## Reverse check — Vulture King review-hold (sons unit)

Confirmed: the pack candidate `vulture-king-aegon-ii` is the **wrong** Vulture King for the 37 AC rebellion — its node identifies "the third Vulture King, a Dornish rebel active during the Dance of the Dragons" (129–131 AC, Borros Baratheon campaign). The correct entity is `vulture-king-aenys-i` (d. 37 AC, rose against Aenys I in the Second Dornish War, matching the chapter's thirst-and-exposure death). The scores tied 1-1-1 (pack-expected on three of four candidates), so the discriminator rule's strict-outscore condition correctly forced review. **An accept here would have corrupted the graph; review was the right routing.**

## Asides (not gate failures)

1. **Data bug found in passing:** `graph/nodes/characters/manfred-hightower-aegons-conquest.node.md` has frontmatter `type: event.war` on a character node (name "Manfred Hightower (Aegon's Conquest)", sworn to House Hightower). Pre-existing Pass 2 artifact, unrelated to the reconciler; would also incidentally break the exact rule's category-equality check for this node.
2. **Graph gap:** no node appears to exist for the historical Ronnel Arryn (the boy King of Mountain and Vale who flew about the Giant's Lance, murdered via the Moon Door ~37 AC). The reconciler correctly held rather than force-matching the modern namesake.
3. **Count note:** strict application of the discriminator rule yields 8 would-accepts (not the ~9 estimated): Corlys Velaryon, Jason Lannister, and Balerion carry only a single `pack-expected` hit and fall to review — all three tops are nonetheless the correct entity, i.e. the rule erred only on the conservative side.
