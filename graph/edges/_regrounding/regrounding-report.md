# Core Edge Citation Re-grounding Report

## Summary

| Metric | Count |
|--------|-------|
| Total edges in | 3,811 |
| Total edges out | 3,811 |
| Regrounded (line suffix updated) | 3,676 |
| Skipped (no searchable quote / paraphrase) | 27 |
| Already correct (line unchanged) | 99 |
| Unresolved (quote not found in chapter) | 9 |

## New Line-Suffix Distribution (top 20)

| Line | Count |
|------|-------|
| 11 | 108 |
| 23 | 93 |
| 13 | 83 |
| 15 | 67 |
| 17 | 66 |
| 19 | 64 |
| 25 | 63 |
| 21 | 62 |
| 29 | 62 |
| 35 | 59 |
| 37 | 55 |
| 57 | 53 |
| 45 | 52 |
| 33 | 51 |
| 69 | 51 |
| 47 | 50 |
| 53 | 50 |
| 31 | 50 |
| 73 | 49 |
| 43 | 49 |

## Before/After Sample (first 10 regrounded edges)

| source→target | edge_type | OLD ref | NEW ref | Line content at NEW ref |
|---------------|-----------|---------|---------|-------------------------|
| arya-stark→jon-snow | LOVES | ...:11 | ...:35 | Sansa had the grace to blush. She blushed prettily. She did everything prettily, |
| arya-stark→jon-snow | PROTECTS | ...:11 | ...:35 | Sansa had the grace to blush. She blushed prettily. She did everything prettily, |
| arya-stark→nymeria | BONDED_TO | ...:11 | ...:65 | Nymeria was waiting for her in the guardroom at the base of the stairs. She boun |
| beth-cassel→sansa-stark | RESPECTS | ...:11 | ...:17 | She studied her own work again, looking for some way to salvage it, then sighed  |
| joffrey-baratheon→robb-stark | HATES | ...:11 | ...:129 | “Robb may be a child,” Joffrey said. “I am a prince. And I grow tired of swattin |
| jon-snow→ghost | BONDED_TO | ...:11 | ...:175 | “Nothing is fair,” Jon said. He messed up her hair again and walked away from he |
| jon-snow→joffrey-baratheon | HATES | ...:11 | ...:135 | Jon looked down on the scene with a frown. “Joffrey is truly a little shit,” he  |
| sandor-clegane→joffrey-baratheon | PROTECTS | ...:11 | ...:143 | The master-at-arms put a hand on Robb’s shoulder to quiet him. “Live steel is to |
| sansa-stark→jon-snow | DISTRUSTS | ...:11 | ...:39 | Sansa sighed as she stitched. “Poor Jon,” she said. “He gets jealous because he’ |
| arya-stark→cersei-lannister | HATES | ...:11 | ...:131 | Suddenly her father’s arms were around her. He held her gently as she turned to  |

## Unresolved Edges (quote not found in chapter) — 9 total

| source→target | edge_type | chapter | quote head |
|---------------|-----------|---------|------------|
| robb-stark→jaime-lannister | RESPECTS | agot-catelyn-10.md | He had been so small … And now it was for Robb that she wait |
| tyrion-lannister→tommen-baratheon | PROTECTS | acok-tyrion-04.md | You cheat.” “Prince Tommen is a good boy.” “If I pry him awa |
| jack-be-lucky→brotherhood-without-banners | MEMBER_OF | asos-epilogue.md | “You’ll get it when I see that Petyr—” A squat one-eyed outl |
| brienne-tarth→catelyn-stark | MOURNS | asos-jaime-07.md | .” She never met Robb Stark, yet her grief for him runs deep |
| jaime-lannister→robb-stark | PRISONER_OF | agot-catelyn-10.md | He had been so small … And now it was for Robb that she wait |
| biter→arya-stark | ASSAULTS | acok-arya-02.md | .” Arya sat up straight, straining to hear. |
| jorah-mormont→daenerys-targaryen | COURTS | asos-daenerys-01.md | Daenerys—” “Your Grace!” “Your Grace,” he conceded, “the dra |
| davos-seaworth→alester-florent | COMPANION_OF | asos-davos-03.md | ?” “Ser Davos Seaworth.” Lord Alester blinked. |
| jaime-lannister→osmund-kettleblack | DISTRUSTS | affc-jaime-01.md | .” Jaime had seen Kettleblack naked in the bathhouse, had se |

## Safety Assertion

PASSED — only `evidence_ref` changed; all other fields byte-identical; 3,811 → 3,811 rows.

