# Fire & Blood OCR-noise scan

Deterministic per-file noise score (pipe-glyph artifacts + che/cbe tokens + mid-word case flips + standalone numeric lines), sorted noisiest-first. This does NOT repair anything — it flags hot files for extraction ordering and the verify arm to attend to.

| File | Unit | Part | Noise Score | pipe | che/cbe | midword_case | numeric_lines |
|------|------|------|-------------|------|---------|--------------|---------------|
| fab-lineages-and-family-tree-25.md | 025 | 1/1 | 275 | 273 | 0 | 2 | 0 |
| fab-jaehaerys-and-alysanne-triumphs-12-p02.md | 012 | 2/2 | 65 | 65 | 0 | 0 | 0 |
| fab-time-of-testing-09.md | 009 | 1/1 | 61 | 59 | 0 | 2 | 0 |
| fab-jaehaerys-and-alysanne-triumphs-12-p01.md | 012 | 1/2 | 46 | 45 | 0 | 1 | 0 |
| fab-jaehaerys-and-alysanne-dragonstone-11.md | 011 | 1/1 | 44 | 44 | 0 | 0 | 0 |
| fab-the-long-reign-cont-14-p01.md | 014 | 1/4 | 32 | 32 | 0 | 0 | 0 |
| fab-the-long-reign-cont-14-p03.md | 014 | 3/4 | 30 | 30 | 0 | 0 | 0 |
| fab-the-hooded-hand-21.md | 021 | 1/1 | 29 | 29 | 0 | 0 | 0 |
| fab-the-blacks-and-the-greens-16-p02.md | 016 | 2/2 | 25 | 24 | 1 | 0 | 0 |
| fab-the-long-reign-cont-14-p04.md | 014 | 4/4 | 24 | 24 | 0 | 0 | 0 |
| fab-the-long-reign-cont-14-p02.md | 014 | 2/4 | 22 | 22 | 0 | 0 | 0 |
| fab-the-red-dragon-and-the-gold-17-p04.md | 017 | 4/4 | 20 | 20 | 0 | 0 | 0 |
| fab-hour-of-the-wolf-20.md | 020 | 1/1 | 20 | 20 | 0 | 0 | 0 |
| fab-the-blacks-and-the-greens-16-p01.md | 016 | 1/2 | 15 | 15 | 0 | 0 | 0 |
| fab-the-long-reign-13.md | 013 | 1/1 | 14 | 13 | 0 | 1 | 0 |
| fab-the-lysene-spring-24-p02.md | 024 | 2/2 | 14 | 14 | 0 | 0 | 0 |
| fab-the-lysene-spring-24-p01.md | 024 | 1/2 | 12 | 11 | 1 | 0 | 0 |
| fab-war-and-peace-and-cattle-shows-22-p01.md | 022 | 1/2 | 11 | 11 | 0 | 0 | 0 |
| fab-aegons-conquest-03.md | 003 | 1/1 | 10 | 10 | 0 | 0 | 0 |
| fab-year-of-the-three-brides-07.md | 007 | 1/1 | 9 | 9 | 0 | 0 | 0 |
| fab-surfeit-of-rulers-08-p02.md | 008 | 2/2 | 9 | 9 | 0 | 0 | 0 |
| fab-sons-of-the-dragon-05-p02.md | 005 | 2/3 | 8 | 8 | 0 | 0 | 0 |
| fab-heirs-of-the-dragon-15-p01.md | 015 | 1/3 | 8 | 6 | 1 | 1 | 0 |
| fab-rhaenyra-overthrown-18-p01.md | 018 | 1/2 | 8 | 8 | 0 | 0 | 0 |
| fab-reign-of-the-dragon-04.md | 004 | 1/1 | 7 | 6 | 1 | 0 | 0 |
| fab-prince-into-king-06.md | 006 | 1/1 | 7 | 7 | 0 | 0 | 0 |
| fab-birth-death-and-betrayal-10.md | 010 | 1/1 | 7 | 7 | 0 | 0 | 0 |
| fab-the-red-dragon-and-the-gold-17-p03.md | 017 | 3/4 | 7 | 7 | 0 | 0 | 0 |
| fab-rhaenyra-overthrown-18-p02.md | 018 | 2/2 | 7 | 7 | 0 | 0 | 0 |
| fab-surfeit-of-rulers-08-p01.md | 008 | 1/2 | 6 | 6 | 0 | 0 | 0 |
| fab-short-sad-reign-of-aegon-ii-19.md | 019 | 1/1 | 5 | 4 | 1 | 0 | 0 |
| fab-war-and-peace-and-cattle-shows-22-p02.md | 022 | 2/2 | 5 | 5 | 0 | 0 | 0 |
| fab-heirs-of-the-dragon-15-p02.md | 015 | 2/3 | 4 | 4 | 0 | 0 | 0 |
| fab-heirs-of-the-dragon-15-p03.md | 015 | 3/3 | 4 | 4 | 0 | 0 | 0 |
| fab-the-red-dragon-and-the-gold-17-p01.md | 017 | 1/4 | 4 | 4 | 0 | 0 | 0 |
| fab-voyage-of-alyn-oakenfist-23.md | 023 | 1/1 | 3 | 3 | 0 | 0 | 0 |
| fab-sons-of-the-dragon-05-p01.md | 005 | 1/3 | 2 | 2 | 0 | 0 | 0 |
| fab-sons-of-the-dragon-05-p03.md | 005 | 3/3 | 2 | 2 | 0 | 0 | 0 |
| fab-the-red-dragon-and-the-gold-17-p02.md | 017 | 2/4 | 1 | 1 | 0 | 0 | 0 |
