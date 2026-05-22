# Stage 4 — Pass-1 Hint Inventory

> Generated: 2026-05-22 16:45:56  
> Total extraction files: 344 | With table: 344 | Without: 0  
> Total relationship rows: 7,348 | Distinct hints: 4,767  
> Layer 1+2 (exact + prefix): **35.1%** (2,582 rows)  
> Layer 3 (keyword/regex): **+15.4%** (1,128 rows)  
> Combined deterministic: **50.5%** of rows (3,710 rows)  
> LLM tail: 49.5% of rows (3,638 rows, 2,969 distinct phrases)  

---

## Per-Book Row Counts

| Book | Rows |
|------|------|
| AGOT | 1,528 |
| ACOK | 1,406 |
| ASOS | 1,770 |
| AFFC | 1,095 |
| ADWD | 1,549 |

---

## Full Hint Inventory (sorted by frequency, desc)

Format: `rank. [count] original phrase` → `EDGE_TYPE` | example A → B (chapter)  
Unmapped phrases show `(LLM tail)` instead of an edge type.

| Rank | Count | Hint (original casing) | Edge Type | Example A → B | Chapter |
|------|-------|----------------------|-----------|---------------|---------|
| 1 | 100 | commands | `COMMANDS` | Joffrey → Ser Ilyn Payne | agot-arya-05 |
| 2 | 92 | Distrusts | `DISTRUSTS` | Arya Stark → The Kingsguard | agot-arya-04 |
| 3 | 67 | Serves | `SERVES` | Jory Cassel → Eddard Stark | agot-bran-01 |
| 4 | 66 | Hostile toward | `OPPOSES` | Ser Meryn Trant → Syrio Forel | agot-arya-04 |
| 5 | 65 | Protective of | `PROTECTS` | Jon Snow → Bran Stark | agot-bran-01 |
| 6 | 59 | Mourns | `MOURNS` | Sansa → Eddard Stark | agot-sansa-06 |
| 7 | 55 | father of | `PARENT_OF` | Lord Jason Mallister → Patrek Mallister | agot-catelyn-05 |
| 8 | 52 | contempt for | `HATES` | Jon → Joffrey | agot-arya-01 |
| 9 | 43 | fears | `FEARS` | Cersei Lannister → Eddard Stark | agot-bran-02 |
| 10 | 43 | Killed | `KILLS` | Jaime Lannister → Torrhen Karstark | agot-catelyn-10 |
| 11 | 37 | Kills | `KILLS` | Arya Stark → Stableboy | agot-arya-04 |
| 12 | 34 | contempt toward | `HATES` | Eddard Karstark → Bran | agot-bran-06 |
| 13 | 31 | Brother of | `SIBLING_OF` | Bran Stark → Robb Stark | agot-bran-01 |
| 14 | 29 | Son of | `PARENT_OF` | Bran Stark → Eddard Stark | agot-bran-01 |
| 15 | 29 | trusts | `TRUSTS` | Bran → Old Nan | agot-bran-07 |
| 16 | 27 | bonded to | `BONDED_TO` | Jon Snow → Ghost | agot-arya-01 |
| 17 | 26 | Betrothed to | `BETROTHED_TO` | Sansa Stark → Joffrey Baratheon | agot-catelyn-02 |
| 18 | 26 | resents | `RESENTS` | Walder Frey → House Tully | agot-catelyn-09 |
| 19 | 25 | Hates | `HATES` | Cersei Lannister → Robert Baratheon | agot-eddard-12 |
| 20 | 24 | daughter of | `PARENT_OF` | Beth Cassel → Ser Rodrik Cassel | agot-arya-01 |
| 21 | 24 | Protects | `PROTECTS` | Jhogo → Daenerys | agot-daenerys-03 |
| 22 | 23 | hostility toward | `OPPOSES` | Arya → Septa Mordane | agot-arya-02 |
| 23 | 23 | Loyal to | `SERVES` | Hullen → House Stark / Eddard Stark | agot-arya-04 |
| 24 | 22 | mother of | `PARENT_OF` | Lysa Arryn → Robin Arryn | agot-bran-02 |
| 25 | 20 | sister of | `SIBLING_OF` | Catelyn Stark → Lysa Arryn | agot-bran-02 |
| 26 | 20 | married to | `SPOUSE_OF` | Rhaegar Targaryen → Elia Martell | agot-eddard-15 |
| 27 | 20 | grieves for | `MOURNS` | Bran Stark → Eddard Stark | acok-bran-01 |
| 28 | 19 | Manipulates | `MANIPULATES` | Cersei Lannister → Robert Baratheon | agot-eddard-03 |
| 29 | 18 | opposes | `OPPOSES` | Lord Rickard Karstark → Robb's peace terms | acok-catelyn-01 |
| 30 | 17 | remembers fondly | `(LLM tail)` | Arya → Needle | asos-arya-02 |
| 31 | 16 | dismissive of | `DISTRUSTS` | Sansa → Jon Snow | agot-arya-01 |
| 32 | 16 | blames | `OPPOSES` | Ned Stark → The Hound / Cersei | agot-arya-02 |
| 33 | 16 | Contemptuous of | `HATES` | Jeor Mormont → Joffrey / King's Landing court | agot-jon-08 |
| 34 | 13 | hatred toward | `HATES` | Arya → The Hound | agot-arya-02 |
| 35 | 13 | longs for | `MOURNS` | Arya → Jon Snow | agot-arya-05 |
| 36 | 13 | allied with | `ALLIES_WITH` | Gold cloaks → Lannisters | agot-arya-05 |
| 37 | 12 | longing for | `(LLM tail)` | Arya → Jon Snow | agot-arya-02 |
| 38 | 12 | Threatens | `OPPOSES` | Viserys → Ser Jorah | agot-daenerys-02 |
| 39 | 12 | Respects | `RESPECTS` | Ned → Barristan Selmy | agot-eddard-05 |
| 40 | 12 | Grief for | `MOURNS` | Sansa → Lady | agot-sansa-02 |
| 41 | 12 | cousin of | `COUSIN_OF` | Lancel → Tyrion | acok-tyrion-07 |
| 42 | 11 | Antagonistic toward | `OPPOSES` | Theon Greyjoy → Jon Snow | agot-bran-01 |
| 43 | 11 | wife of | `SPOUSE_OF` | Cersei Lannister → Robert Baratheon | agot-bran-02 |
| 44 | 11 | Mocks | `OPPOSES` | Khal Drogo → Viserys | agot-daenerys-04 |
| 45 | 11 | formerly served | `SERVES` | Donal Noye → Stannis Baratheon | agot-jon-03 |
| 46 | 11 | attracted to | `(LLM tail)` | Lady Hornwood → Ser Rodrik | acok-bran-02 |
| 47 | 10 | Defiant toward | `OPPOSES` | Arya Stark → Ser Meryn Trant | agot-arya-04 |
| 48 | 10 | bond with | `(LLM tail)` | Bran → Summer | agot-bran-04 |
| 49 | 10 | Sworn to | `SWORN_TO` | Lord Wyman Manderly → Robb/House Stark | agot-catelyn-08 |
| 50 | 10 | suspicious of | `DISTRUSTS` | Haggo → Mirri Maz Duur | agot-daenerys-07 |
| 51 | 10 | Wary of | `DISTRUSTS` | Eddard Stark → Varys | agot-eddard-11 |
| 52 | 10 | protective toward | `PROTECTS` | Arya → The crying girl | acok-arya-04 |
| 53 | 10 | conflicted about | `(LLM tail)` | Arya → Jaqen H'ghar | acok-arya-07 |
| 54 | 10 | Friendship with | `COMPANION_OF` | Jon Snow → Donal Noye | acok-jon-01 |
| 55 | 9 | authority over | `COMMANDS` | Ser Rodrik → Practice yard combatants | agot-arya-01 |
| 56 | 9 | Misses | `MOURNS` | Arya Stark → Nymeria | agot-arya-03 |
| 57 | 9 | Loves | `LOVES` | Bran Stark → Jon Snow | agot-bran-01 |
| 58 | 9 | Protected by | `PROTECTS` | Catelyn Stark → Ser Rodrik Cassel | agot-catelyn-04 |
| 59 | 9 | fears for | `FEARS` | Catelyn → Hoster Tully | agot-catelyn-09 |
| 60 | 9 | Fear of | `FEARS` | Dany → Qotho | agot-daenerys-04 |
| 61 | 9 | Commander | `COMMANDS` | Khal Drogo → Cohollo (bloodrider) | agot-daenerys-06 |
| 62 | 9 | guilt toward | `(LLM tail)` | Ned → Sansa | agot-eddard-04 |
| 63 | 9 | remembers | `(LLM tail)` | Eddard Stark → Rhaegar Targaryen | agot-eddard-09 |
| 64 | 9 | Betrays | `BETRAYS` | Petyr Baelish → Eddard Stark | agot-eddard-14 |
| 65 | 9 | Accuses | `(LLM tail)` | Varys → Eddard Stark | agot-sansa-04 |
| 66 | 8 | Recalls fondly | `(LLM tail)` | Arya Stark → Robb Stark | agot-arya-04 |
| 67 | 8 | relies on | `(LLM tail)` | Robb → Maester Luwin | agot-bran-04 |
| 68 | 8 | Defies | `OPPOSES` | Ser Barristan Selmy → Joffrey Baratheon | agot-sansa-05 |
| 69 | 8 | lover of | `LOVER_OF` | Jaime → Cersei Lannister | acok-catelyn-07 |
| 70 | 8 | Seeks | `SEEKS` | Pyat Pree → Dragons | acok-daenerys-01 |
| 71 | 8 | Protective concern for | `PROTECTS` | Tyrion → Sansa | acok-sansa-05 |
| 72 | 7 | defends | `PROTECTS` | Arya → Jon Snow | agot-arya-01 |
| 73 | 7 | critical of | `(LLM tail)` | Septa Mordane → Arya | agot-arya-01 |
| 74 | 7 | resembles | `(LLM tail)` | Arya → Ned Stark | agot-arya-01 |
| 75 | 7 | worries about | `(LLM tail)` | Arya → Bran Stark | agot-arya-05 |
| 76 | 7 | niece of | `UNCLE_OF` | Catelyn → Brynden Tully | agot-catelyn-01 |
| 77 | 7 | Squire to | `SERVES` | Olyvar Frey → Robb | agot-catelyn-10 |
| 78 | 7 | Loyalty to | `SERVES` | Ser Jorah → Daenerys | agot-daenerys-04 |
| 79 | 7 | Controls | `COMMANDS` | Varys → Jorah Mormont | agot-eddard-08 |
| 80 | 7 | Loyal service to | `SERVES` | Alyn → Eddard Stark | agot-eddard-10 |
| 81 | 7 | grudging respect for | `RESPECTS` | Tyrion → Catelyn Stark | agot-tyrion-04 |
| 82 | 7 | Supports | `(LLM tail)` | Farlen → Palla | acok-bran-06 |
| 83 | 7 | champion of | `(LLM tail)` | Oznak zo Pahl → Meereen's Great Masters | asos-daenerys-05 |
| 84 | 7 | Pities | `(LLM tail)` | Sansa Stark → Margaery Tyrell | asos-sansa-05 |
| 85 | 7 | Former lover of | `LOVER_OF` | Mya Stone → Mychel Redfort | affc-alayne-02 |
| 86 | 7 | Supporter of | `(LLM tail)` | Rodrik the Reader → Asha Greyjoy | affc-the-drowned-man-01 |
| 87 | 6 | remembers teaching of | `(LLM tail)` | Arya → Syrio Forel | agot-arya-05 |
| 88 | 6 | dislikes | `(LLM tail)` | Robert Baratheon → Stannis Baratheon | agot-bran-02 |
| 89 | 6 | dominates | `(LLM tail)` | Summer → Shaggydog | agot-bran-07 |
| 90 | 6 | loved | `LOVES` | Eddard Stark → Brandon Stark, Lyanna Stark | agot-bran-07 |
| 91 | 6 | concern for | `(LLM tail)` | Catelyn → Lysa Arryn | agot-catelyn-01 |
| 92 | 6 | Contempt | `HATES` | Ned → Jorah Mormont | agot-eddard-02 |
| 93 | 6 | devoted to | `(LLM tail)` | Barra's mother → Robert Baratheon | agot-eddard-09 |
| 94 | 6 | Advises | `ADVISES` | Varys → Eddard Stark | agot-eddard-11 |
| 95 | 6 | Suspects | `(LLM tail)` | Eddard Stark → Tywin Lannister | agot-eddard-11 |
| 96 | 6 | Bitter toward | `RESENTS` | Sandor → Rhaegar Targaryen | agot-sansa-02 |
| 97 | 6 | Resentment toward | `RESENTS` | Sansa Stark → Eddard Stark | agot-sansa-03 |
| 98 | 6 | Complex feelings toward | `(LLM tail)` | Tyrion → Jaime Lannister | agot-tyrion-06 |
| 99 | 6 | recalls | `(LLM tail)` | Arya → Jory Cassel | acok-arya-02 |
| 100 | 6 | commander of | `COMMANDS` | Yoren → The Night's Watch recruits | acok-arya-04 |
| 101 | 6 | Husband of | `SPOUSE_OF` | Davos → Marya | acok-davos-01 |
| 102 | 6 | distrust toward | `DISTRUSTS` | Theon → Maester Luwin | acok-theon-05 |
| 103 | 6 | Favors | `(LLM tail)` | Cersei → Lancel Lannister | acok-tyrion-04 |
| 104 | 6 | Fond of | `LOVES` | Bran → Meera Reed | asos-bran-01 |
| 105 | 6 | despises | `HATES` | Robb Stark → Tyrion Lannister | asos-catelyn-05 |
| 106 | 6 | Betrayed | `(LLM tail)` | Roose Bolton → Robb Stark | asos-jon-11 |
| 107 | 6 | Friend of | `COMPANION_OF` | Grenn → Jon Snow | asos-prologue |
| 108 | 5 | Conspires with | `CONSPIRES_WITH` | Stout man (torchbearer) → Fat man (forked beard) | agot-arya-03 |
| 109 | 5 | Half-brother of | `SIBLING_OF` | Bran Stark → Jon Snow | agot-bran-01 |
| 110 | 5 | Ward of | `WARD_OF` | Theon Greyjoy → Eddard Stark | agot-bran-01 |
| 111 | 5 | dependent on | `(LLM tail)` | Bran → Hodor | agot-bran-06 |
| 112 | 5 | serves/protects | `SERVES` | Maester Luwin → Bran, Rickon | agot-bran-07 |
| 113 | 5 | childhood companion of | `COMPANION_OF` | Catelyn Stark → Petyr Baelish (Littlefinger) | agot-catelyn-05 |
| 114 | 5 | Distrustful of | `DISTRUSTS` | Catelyn → Bronn | agot-catelyn-06 |
| 115 | 5 | distrust | `DISTRUSTS` | Northern lords → Walder Frey | agot-catelyn-09 |
| 116 | 5 | subordinate to | `SERVES` | Mago → Ko Jhaqo | agot-daenerys-07 |
| 117 | 5 | Warns | `ADVISES` | Littlefinger → Ned | agot-eddard-05 |
| 118 | 5 | captor of | `CAPTURES` | Catelyn Stark → Tyrion Lannister | agot-eddard-09 |
| 119 | 5 | defeated in joust | `(LLM tail)` | Rhaegar Targaryen → Brandon Stark | agot-eddard-15 |
| 120 | 5 | Friendship | `COMPANION_OF` | Jon Snow → Pyp | agot-jon-05 |
| 121 | 5 | Close friendship with | `COMPANION_OF` | Jon Snow → Samwell Tarly | agot-jon-07 |
| 122 | 5 | Cruel toward | `(LLM tail)` | Joffrey → Mycah | agot-sansa-01 |
| 123 | 5 | Dismisses | `(LLM tail)` | Joffrey Baratheon → Ser Barristan Selmy | agot-sansa-05 |
| 124 | 5 | mentors | `TUTORS` | Jon Snow → Grenn, Pypar | agot-tyrion-03 |
| 125 | 5 | served by | `(LLM tail)` | Ramsay Snow → Reek | acok-bran-02 |
| 126 | 5 | Cares for | `(LLM tail)` | Maester Vyman → Lord Hoster | acok-catelyn-05 |
| 127 | 5 | Commands/leads | `COMMANDS` | Daenerys → Khalasar | acok-daenerys-01 |
| 128 | 5 | Obeys | `SERVES` | Aggo → Daenerys | acok-daenerys-02 |
| 129 | 5 | desires | `(LLM tail)` | Reek → Palla | acok-theon-05 |
| 130 | 5 | secret lover of | `LOVER_OF` | Tyrion → Shae | acok-tyrion-07 |
| 131 | 5 | feels guilt toward | `(LLM tail)` | Arya → Gendry, Hot Pie | asos-arya-01 |
| 132 | 5 | advocates for | `(LLM tail)` | The wild wolf (in story) → The quiet wolf | asos-bran-02 |
| 133 | 5 | companion of | `COMPANION_OF` | Ellaria Sand → Oberyn Martell (Red Viper) | asos-tyrion-08 |
| 134 | 5 | Queen served by | `(LLM tail)` | Daenerys → Irri | adwd-daenerys-03 |
| 135 | 4 | alienated from | `(LLM tail)` | Arya → Household guard (Jory, Harwin, Alyn, etc.) | agot-arya-02 |
| 136 | 4 | opposition | `(LLM tail)` | Ned Stark → The council | agot-arya-02 |
| 137 | 4 | Student of | `TUTORS` | Arya Stark → Syrio Forel | agot-arya-03 |
| 138 | 4 | Loyal to memory of | `SERVES` | Yoren → Benjen Stark | agot-arya-03 |
| 139 | 4 | admires | `RESPECTS` | Bran Stark → Kingsguard (as institution) | agot-bran-02 |
| 140 | 4 | fears/resents | `FEARS` | Cersei Lannister → Robert Baratheon | agot-bran-02 |
| 141 | 4 | Accuses of murder | `(LLM tail)` | Lysa Arryn → Cersei Lannister / the Lannisters | agot-catelyn-02 |
| 142 | 4 | bannerman to | `(LLM tail)` | Lord Jason Mallister → House Tully | agot-catelyn-05 |
| 143 | 4 | Bonded with | `BONDED_TO` | Robb → Grey Wind | agot-catelyn-08 |
| 144 | 4 | declared king by | `(LLM tail)` | Robb → Jon Umber (Greatjon) | agot-catelyn-11 |
| 145 | 4 | Mistrusts | `DISTRUSTS` | Daenerys → Illyrio | agot-daenerys-01 |
| 146 | 4 | Seeks alliance with | `SEEKS` | Viserys → Khal Drogo | agot-daenerys-01 |
| 147 | 4 | bloodrider of | `(LLM tail)` | Qotho → Khal Drogo | agot-daenerys-05 |
| 148 | 4 | seeks vengeance against | `SEEKS` | Daenerys → Mago | agot-daenerys-09 |
| 149 | 4 | grieving for | `MOURNS` | Arya → Mycah (butcher's boy) | agot-eddard-04 |
| 150 | 4 | serves as Hand to | `SERVES` | Eddard Stark → Robert Baratheon | agot-eddard-07 |
| 151 | 4 | Commands/controls | `COMMANDS` | Cersei Lannister → Joffrey Baratheon | agot-eddard-14 |
| 152 | 4 | brother to | `SIBLING_OF` | Benjen Stark → Eddard Stark | agot-jon-01 |
| 153 | 4 | feels abandoned by | `(LLM tail)` | Jon Snow → Benjen Stark | agot-jon-03 |
| 154 | 4 | Steward to | `(LLM tail)` | Jon Snow → Jeor Mormont | agot-jon-07 |
| 155 | 4 | Pity toward | `(LLM tail)` | Sansa Stark → Jon Snow | agot-sansa-03 |
| 156 | 4 | Attacked | `(LLM tail)` | Sandor Clegane → Jeyne Poole's quarters | agot-sansa-04 |
| 157 | 4 | Previously served | `(LLM tail)` | Ser Barristan Selmy → King Aerys II Targaryen | agot-sansa-05 |
| 158 | 4 | Leads | `COMMANDS` | Gunthor → Stone Crows | agot-tyrion-06 |
| 159 | 4 | Negotiates with | `NEGOTIATES_WITH` | Chella → Tywin | agot-tyrion-07 |
| 160 | 4 | uses | `(LLM tail)` | Roose Bolton → Qyburn | acok-arya-10 |
| 161 | 4 | cousin to | `COUSIN_OF` | Big Walder Frey → Little Walder Frey | acok-bran-01 |
| 162 | 4 | threatened by | `(LLM tail)` | Lady Hornwood → Ramsay Snow | acok-bran-02 |
| 163 | 4 | holds captive | `PRISONER_OF` | Lord Tywin → Ser Wylis Manderly | acok-bran-02 |
| 164 | 4 | served | `(LLM tail)` | Reek → Bastard of Bolton | acok-bran-05 |
| 165 | 4 | Warg bond with | `WARGS_INTO` | Bran → Summer | acok-bran-06 |
| 166 | 4 | Former ward of | `(LLM tail)` | Theon → Eddard Stark | acok-bran-06 |
| 167 | 4 | uncle of | `UNCLE_OF` | Ser Brynden Tully → Catelyn Stark | acok-catelyn-01 |
| 168 | 4 | disrespects | `(LLM tail)` | Lord Randyll Tarly → Robb Stark | acok-catelyn-02 |
| 169 | 4 | Killed by | `KILLS` | Ebben → Wildlings | acok-jon-08 |
| 170 | 4 | Disdains | `HATES` | Sansa → Ser Preston (Greenfield) | acok-sansa-01 |
| 171 | 4 | Affectionate toward | `LOVES` | Tyrion → Tommen | acok-sansa-01 |
| 172 | 4 | resentful toward | `RESENTS` | Arya → Brotherhood | asos-arya-08 |
| 173 | 4 | Condemns | `(LLM tail)` | Robb → Theon Greyjoy | asos-catelyn-06 |
| 174 | 4 | grudging respect toward | `RESPECTS` | Jaime Lannister → Brienne of Tarth | asos-jaime-01 |
| 175 | 4 | haunted by memory of | `(LLM tail)` | Tyrion → Tysha | asos-tyrion-09 |
| 176 | 4 | Enemy of | `OPPOSES` | Cersei → Olenna Tyrell | affc-cersei-02 |
| 177 | 4 | trusts / relies on | `TRUSTS` | Maester Aemon → Sam | affc-samwell-03 |
| 178 | 4 | co-conspirator with | `CONSPIRES_WITH` | Arianne Martell → Garin | affc-the-princess-in-the-tower-01 |
| 179 | 3 | companion | `COMPANION_OF` | Sansa → Jeyne Poole | agot-arya-02 |
| 180 | 3 | Protective father of | `(LLM tail)` | Eddard Stark → Arya Stark | agot-arya-03 |
| 181 | 3 | knew | `(LLM tail)` | Yoren → Eddard Stark | agot-arya-05 |
| 182 | 3 | defers to | `(LLM tail)` | High Septon → Joffrey | agot-arya-05 |
| 183 | 3 | kindness toward | `(LLM tail)` | Tyrion → Bran | agot-bran-04 |
| 184 | 3 | Was betrothed to | `BETROTHED_TO` | Catelyn Stark → Brandon Stark | agot-catelyn-04 |
| 185 | 3 | Surveils | `(LLM tail)` | Varys → Catelyn Stark, Ser Rodrik | agot-catelyn-04 |
| 186 | 3 | Estranged from | `(LLM tail)` | Brynden Tully → Lord Hoster Tully | agot-catelyn-06 |
| 187 | 3 | Serves under | `SERVES` | Roose Bolton → Robb | agot-catelyn-08 |
| 188 | 3 | widow of | `SPOUSE_OF` | Catelyn → Eddard Stark | agot-catelyn-11 |
| 189 | 3 | rescued | `RESCUES` | Brynden → Edmure Tully | agot-catelyn-11 |
| 190 | 3 | feared by | `(LLM tail)` | Grey Wind → Riverrun guards | agot-catelyn-11 |
| 191 | 3 | Counsels | `ADVISES` | Illyrio → Viserys | agot-daenerys-02 |
| 192 | 3 | Fearful of | `FEARS` | Dany → Viserys | agot-daenerys-02 |
| 193 | 3 | Trusts and relies on | `TRUSTS` | Daenerys → Ser Jorah | agot-daenerys-03 |
| 194 | 3 | Abuses | `(LLM tail)` | Viserys → Doreah | agot-daenerys-04 |
| 195 | 3 | Teacher to | `(LLM tail)` | Jhiqui → Daenerys | agot-daenerys-04 |
| 196 | 3 | commands / trusts | `COMMANDS` | Dany → Ser Jorah | agot-daenerys-07 |
| 197 | 3 | claims descent from | `(LLM tail)` | Daenerys → Aegon the Conqueror | agot-daenerys-09 |
| 198 | 3 | mocks/antagonizes | `OPPOSES` | Renly → Janos Slynt | agot-eddard-06 |
| 199 | 3 | contemptuous toward | `HATES` | Jaime Lannister → Littlefinger | agot-eddard-09 |
| 200 | 3 | sister to | `SIBLING_OF` | Lyanna Stark → Eddard Stark | agot-eddard-09 |
| 201 | 3 | Close friend of | `COMPANION_OF` | Ser Marq Piper → Edmure Tully | agot-eddard-11 |
| 202 | 3 | Loathes | `HATES` | Sandor Clegane → Gregor Clegane | agot-eddard-12 |
| 203 | 3 | holds hostage | `PRISONER_OF` | Cersei Lannister → Sansa Stark | agot-eddard-15 |
| 204 | 3 | paired with (formal) | `(LLM tail)` | Robb Stark → Myrcella Baratheon | agot-jon-01 |
| 205 | 3 | taunts | `(LLM tail)` | Toad → Jon Snow | agot-jon-03 |
| 206 | 3 | antagonizes | `OPPOSES` | Tyrion Lannister → Ser Alliser Thorne | agot-jon-03 |
| 207 | 3 | bonds with | `(LLM tail)` | Jon Snow → Ghost | agot-jon-03 |
| 208 | 3 | Service to | `(LLM tail)` | Chett → Maester Aemon | agot-jon-05 |
| 209 | 3 | Antagonism with | `(LLM tail)` | Jon Snow → Ser Alliser Thorne | agot-jon-07 |
| 210 | 3 | Angry at | `(LLM tail)` | Jon Snow → Samwell Tarly | agot-jon-08 |
| 211 | 3 | Friendly with | `COMPANION_OF` | Jon Snow → Pyp, Grenn, Toad, Halder, Matt | agot-jon-08 |
| 212 | 3 | Kind toward | `(LLM tail)` | Ser Barristan Selmy → Sansa | agot-sansa-01 |
| 213 | 3 | Disapproves of | `(LLM tail)` | Septa Mordane → Jory Cassel | agot-sansa-02 |
| 214 | 3 | Protective authority over | `(LLM tail)` | Eddard Stark → Sansa and Arya | agot-sansa-03 |
| 215 | 3 | Infatuation with | `(LLM tail)` | Jeyne Poole → Beric Dondarrion | agot-sansa-03 |
| 216 | 3 | Served alongside | `(LLM tail)` | Ser Barristan Selmy → Ser Gerold Hightower | agot-sansa-05 |
| 217 | 3 | Enforcer for | `(LLM tail)` | Ser Meryn Trant → Joffrey | agot-sansa-06 |
| 218 | 3 | loved (past) | `LOVES` | Petyr Baelish → Catelyn Stark | agot-tyrion-04 |
| 219 | 3 | Assesses as dangerous | `(LLM tail)` | Tywin → Stannis Baratheon | agot-tyrion-09 |
| 220 | 3 | Loyal subordinate to | `SERVES` | Kevan → Tywin | agot-tyrion-09 |
| 221 | 3 | granddaughter of | `PARENT_OF` | Arya → Lord Tully | acok-arya-02 |
| 222 | 3 | sympathetic to | `(LLM tail)` | Innkeeper → Night's Watch | acok-arya-02 |
| 223 | 3 | Knows true identity of | `(LLM tail)` | Yoren → Arya | acok-arya-03 |
| 224 | 3 | Frustrated with | `(LLM tail)` | Arya → Lommy | acok-arya-05 |
| 225 | 3 | Under command of | `COMMANDS` | Jaqen H'ghar → Ser Amory Lorch | acok-arya-08 |
| 226 | 3 | grateful to | `(LLM tail)` | Robett Glover → Arya (as Weasel) | acok-arya-09 |
| 227 | 3 | caretaker of | `(LLM tail)` | Maester Luwin → Bran Stark | acok-bran-01 |
| 228 | 3 | proposes alliance with | `ALLIES_WITH` | Leobald Tallhart → Lady Hornwood | acok-bran-02 |
| 229 | 3 | thinks of | `(LLM tail)` | Bran → Jon Snow | acok-bran-02 |
| 230 | 3 | Affection for | `LOVES` | Bran → Hodor and Old Nan | acok-bran-03 |
| 231 | 3 | advises/serves | `ADVISES` | Ser Rodrik Cassel → Bran | acok-bran-05 |
| 232 | 3 | Swears fealty to | `(LLM tail)` | Reek → Theon / House Greyjoy | acok-bran-06 |
| 233 | 3 | Feels betrayed by | `(LLM tail)` | Bran → Osha | acok-bran-06 |
| 234 | 3 | warns/advises | `ADVISES` | Jojen → Bran | acok-bran-07 |
| 235 | 3 | political tension with | `(LLM tail)` | Robb Stark → Catelyn Stark | acok-catelyn-01 |
| 236 | 3 | Compared to | `(LLM tail)` | Renly → Robert Baratheon | acok-catelyn-03 |
| 237 | 3 | Loyal to / serves | `SERVES` | Rivers → Catelyn/Tullys | acok-catelyn-05 |
| 238 | 3 | memory of | `(LLM tail)` | Catelyn → Lysa Arryn | acok-catelyn-07 |
| 239 | 3 | Named bloodrider | `(LLM tail)` | Daenerys → Rakharo | acok-daenerys-01 |
| 240 | 3 | Handmaid to | `(LLM tail)` | Irri → Daenerys | acok-daenerys-01 |
| 241 | 3 | Former husband of | `(LLM tail)` | Ser Jorah → Lynesse Hightower | acok-daenerys-01 |
| 242 | 3 | Named for / honors | `(LLM tail)` | Drogon → Khal Drogo | acok-daenerys-01 |
| 243 | 3 | Sworn protector (bloodrider) | `(LLM tail)` | Jhogo → Daenerys | acok-daenerys-04 |
| 244 | 3 | sent by | `(LLM tail)` | Arstan Whitebeard → Illyrio Mopatis | acok-daenerys-05 |
| 245 | 3 | Leader of | `(LLM tail)` | Ser Axell Florent → The queen's men | acok-davos-01 |
| 246 | 3 | Fears/distrusts | `FEARS` | Davos → Melisandre | acok-davos-03 |
| 247 | 3 | Brotherhood with | `(LLM tail)` | Jon Snow → Ebben, Squire Dalbridge | acok-jon-06 |
| 248 | 3 | bitter resentment | `RESENTS` | Stannis → Robert | acok-prologue |
| 249 | 3 | devoted follower | `(LLM tail)` | Selyse → Melisandre / R'hllor | acok-prologue |
| 250 | 3 | Sympathetic toward | `(LLM tail)` | Tyrion → Sansa | acok-sansa-01 |
| 251 | 3 | avoids | `(LLM tail)` | Ser Horas Redwyne → Sansa | acok-sansa-03 |
| 252 | 3 | Rivalry with | `(LLM tail)` | Joffrey → Robb Stark | acok-sansa-05 |
| 253 | 3 | Distrust of | `DISTRUSTS` | Cersei → Her own guards (sellswords) | acok-sansa-05 |
| 254 | 3 | Abandons | `(LLM tail)` | Cersei → Sansa | acok-sansa-07 |
| 255 | 3 | Loyal squire to | `(LLM tail)` | Wex → Theon | acok-theon-06 |
| 256 | 3 | Guards | `GUARDS` | Chella → Shae | acok-tyrion-01 |
| 257 | 3 | Employs / commands | `COMMANDS` | Tyrion → Bronn | acok-tyrion-03 |
| 258 | 3 | Manipulates / tests loyalty of | `MANIPULATES` | Tyrion → Pycelle | acok-tyrion-04 |
| 259 | 3 | manipulates/controls | `MANIPULATES` | Tyrion → Lancel | acok-tyrion-07 |
| 260 | 3 | Sibling rivalry with | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-09 |
| 261 | 3 | Terrified of | `FEARS` | Sandor Clegane → Fire/wildfire | acok-tyrion-13 |
| 262 | 3 | considers trusting | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-15 |
| 263 | 3 | kinship with | `(LLM tail)` | Arya → Wolves | asos-arya-01 |
| 264 | 3 | traveling companion | `COMPANION_OF` | Arya → Hot Pie | asos-arya-02 |
| 265 | 3 | partner/comrade | `(LLM tail)` | Tom Sevenstrings → Lem Lemoncloak | asos-arya-02 |
| 266 | 3 | Religious devotion to | `(LLM tail)` | Thoros of Myr → R'hllor | asos-arya-06 |
| 267 | 3 | lost to | `(LLM tail)` | Lord Beric → Ser Burton Crakehall | asos-arya-07 |
| 268 | 3 | concerned for | `(LLM tail)` | Thoros → Lord Beric | asos-arya-08 |
| 269 | 3 | bitter about | `RESENTS` | Gendry → His unknown father | asos-arya-08 |
| 270 | 3 | Master of | `(LLM tail)` | Sandor Clegane → Stranger (horse) | asos-arya-09 |
| 271 | 3 | fears/avoids | `FEARS` | Sandor Clegane → Gregor Clegane | asos-arya-10 |
| 272 | 3 | sibling bond with | `(LLM tail)` | Meera Reed → Jojen Reed | asos-bran-02 |
| 273 | 3 | Grandson of | `PARENT_OF` | Jinglebell → Lord Walder Frey | asos-catelyn-06 |
| 274 | 3 | Remembers/mourns | `MOURNS` | Catelyn → Ned Stark | asos-catelyn-07 |
| 275 | 3 | conflicted feelings toward | `(LLM tail)` | Daenerys → Ser Jorah Mormont | asos-daenerys-02 |
| 276 | 3 | commands/owns | `COMMANDS` | Daenerys → Drogon | asos-daenerys-03 |
| 277 | 3 | warns Dany about | `ADVISES` | Arstan Whitebeard → Mero | asos-daenerys-04 |
| 278 | 3 | captained | `(LLM tail)` | Dale Seaworth → Wraith | asos-davos-01 |
| 279 | 3 | Imprisons | `IMPRISONS` | Ser Axell Florent → Lord Alester Florent | asos-davos-03 |
| 280 | 3 | member of | `MEMBER_OF` | Tom of Sevenstreams → Brotherhood Without Banners | asos-epilogue |
| 281 | 3 | manipulated | `(LLM tail)` | Cersei (memory) → Jaime (memory) | asos-jaime-02 |
| 282 | 3 | prisoner of | `PRISONER_OF` | Brienne → Vargo Hoat | asos-jaime-04 |
| 283 | 3 | Recalls with respect | `RESPECTS` | Jon Snow → Benjen Stark | asos-jon-04 |
| 284 | 3 | murderer of | `KILLS` | Garth of Oldtown → Lord Commander Mormont | asos-jon-06 |
| 285 | 3 | Loyal companion to | `COMPANION_OF` | Pyp → Jon Snow | asos-jon-08 |
| 286 | 3 | Appointed | `(LLM tail)` | Tywin Lannister → Roose Bolton | asos-jon-11 |
| 287 | 3 | opposed by | `(LLM tail)` | Jon Snow → Janos Slynt | asos-jon-12 |
| 288 | 3 | Murdered | `KILLS` | Chett → Bessa | asos-prologue |
| 289 | 3 | rescues | `RESCUES` | The mysterious rider → Sam and Gilly | asos-samwell-03 |
| 290 | 3 | Conspired with | `CONSPIRES_WITH` | Petyr Baelish → Olenna Tyrell | asos-sansa-06 |
| 291 | 3 | Remembers / mourns | `MOURNS` | Sansa Stark → Sandor Clegane | asos-sansa-06 |
| 292 | 3 | Sister of (deceased) | `SIBLING_OF` | Brienne → Galladon | affc-brienne-06 |
| 293 | 3 | Friendly acquaintance | `COMPANION_OF` | Cat/Arya → Tagganaro | affc-cat-of-the-canals-01 |
| 294 | 3 | Romantic/sexual exploitation | `(LLM tail)` | Dareon → Lanna | affc-cat-of-the-canals-01 |
| 295 | 3 | Suspicion | `(LLM tail)` | Cersei → Stannis Baratheon | affc-cersei-01 |
| 296 | 3 | Commander/master | `COMMANDS` | Jaime → Josmyn Peckledon | affc-jaime-05 |
| 297 | 3 | Exiled by | `(LLM tail)` | Euron → Balon | affc-the-iron-captain-01 |
| 298 | 3 | Punished | `(LLM tail)` | Balon Greyjoy → Quellon's third wife (Piper) | affc-the-prophet-01 |
| 299 | 3 | Lord of | `(LLM tail)` | Gorold Goodbrother → Hammerhorn | affc-the-prophet-01 |
| 300 | 3 | gaoler to | `(LLM tail)` | Septa Unella → Cersei | adwd-cersei-01 |
| 301 | 3 | Considers betrayer | `(LLM tail)` | Cersei → Lancel | adwd-cersei-02 |
| 302 | 3 | is served by | `(LLM tail)` | Daenerys → Irri | adwd-daenerys-01 |
| 303 | 3 | Knew / recalled | `(LLM tail)` | Reek → Arya Stark | adwd-reek-01 |
| 304 | 3 | Uneasy alliance | `ALLIES_WITH` | Quentyn Martell → Tattered Prince | adwd-the-dragontamer-01 |
| 305 | 3 | Subordinate of | `SERVES` | Pretty Meris → The Tattered Prince | adwd-the-spurned-suitor-01 |
| 306 | 3 | Property of | `(LLM tail)` | Tyrion → Yezzan zo Qaggaz | adwd-tyrion-10 |
| 307 | 3 | Financial debtor to | `(LLM tail)` | Tyrion → Brown Ben Plumm | adwd-tyrion-12 |
| 308 | 3 | Misses/mourns | `MOURNS` | Tyrion → Jaime | adwd-tyrion-12 |
| 309 | 2 | disdain for | `HATES` | Joffrey → Robb / Starks | agot-arya-01 |
| 310 | 2 | protects / serves | `PROTECTS` | Sandor Clegane → Joffrey | agot-arya-01 |
| 311 | 2 | comparison/memory | `(LLM tail)` | Ned Stark → Lyanna Stark | agot-arya-02 |
| 312 | 2 | Fears judgment from | `FEARS` | Arya Stark → Septa Mordane | agot-arya-03 |
| 313 | 2 | Reports to | `(LLM tail)` | Yoren → Eddard Stark | agot-arya-03 |
| 314 | 2 | Asks about | `(LLM tail)` | Arya Stark → Desmond | agot-arya-03 |
| 315 | 2 | Mourns/grieves | `MOURNS` | Arya Stark → Hullen | agot-arya-04 |
| 316 | 2 | Loves/trusts | `LOVES` | Arya Stark → Eddard Stark | agot-arya-04 |
| 317 | 2 | Former service to | `(LLM tail)` | Syrio Forel → The Sealord of Braavos | agot-arya-04 |
| 318 | 2 | overrules | `(LLM tail)` | Joffrey → Cersei Lannister | agot-arya-05 |
| 319 | 2 | executes | `EXECUTES` | Ser Ilyn Payne → Eddard Stark | agot-arya-05 |
| 320 | 2 | mocked | `(LLM tail)` | Sansa and Jeyne Poole → Ser Horas and Ser Hobber Redwyne | agot-arya-05 |
| 321 | 2 | attempts to intervene | `(LLM tail)` | Varys → Joffrey | agot-arya-05 |
| 322 | 2 | Contrasts with | `(LLM tail)` | Jon Snow → Robb Stark | agot-bran-01 |
| 323 | 2 | longs for / loves | `MOURNS` | Bran → Eddard Stark | agot-bran-04 |
| 324 | 2 | frustration with | `(LLM tail)` | Bran → Old Nan | agot-bran-04 |
| 325 | 2 | dependence on | `(LLM tail)` | Bran → Hodor | agot-bran-04 |
| 326 | 2 | connection to | `(LLM tail)` | Tyrion → Jon Snow | agot-bran-04 |
| 327 | 2 | delivers news to | `(LLM tail)` | Yoren → Robb, Bran | agot-bran-04 |
| 328 | 2 | Protective older brother | `SIBLING_OF` | Robb → Bran | agot-bran-05 |
| 329 | 2 | Relies on counsel of | `ADVISES` | Robb → Maester Luwin | agot-bran-05 |
| 330 | 2 | Aggressive protector | `(LLM tail)` | Summer → Hali | agot-bran-05 |
| 331 | 2 | advisor to | `ADVISES` | Maester Luwin → Robb | agot-bran-06 |
| 332 | 2 | companion to | `COMPANION_OF` | Theon Greyjoy → Robb | agot-bran-06 |
| 333 | 2 | brother-in-law of | `IN_LAW_OF` | Ned Stark → Jon Arryn | agot-catelyn-01 |
| 334 | 2 | Deep resentment toward | `(LLM tail)` | Catelyn Stark → Jon Snow | agot-catelyn-02 |
| 335 | 2 | Lives in the shadow of | `(LLM tail)` | Eddard Stark → Brandon Stark | agot-catelyn-02 |
| 336 | 2 | Caretaker | `(LLM tail)` | Old Nan → Catelyn | agot-catelyn-03 |
| 337 | 2 | Informed | `(LLM tail)` | Varys → Petyr Baelish | agot-catelyn-04 |
| 338 | 2 | rivals with | `(LLM tail)` | House Blackwood → House Bracken | agot-catelyn-05 |
| 339 | 2 | Old friend of | `(LLM tail)` | Howland Reed → Ned Stark | agot-catelyn-08 |
| 340 | 2 | mother, counselor to | `ADVISES` | Catelyn → Robb | agot-catelyn-09 |
| 341 | 2 | emulates | `(LLM tail)` | Robb → Ned Stark | agot-catelyn-09 |
| 342 | 2 | serves as scout commander for | `SERVES` | Ser Brynden Tully → Robb | agot-catelyn-09 |
| 343 | 2 | Former betrothed of | `BETROTHED_TO` | Catelyn → Brandon Stark | agot-catelyn-10 |
| 344 | 2 | Sworn protector of | `(LLM tail)` | Hallis Mollen → Catelyn | agot-catelyn-10 |
| 345 | 2 | Serves as lord bannerman to | `SERVES` | Galbart Glover → Robb | agot-catelyn-10 |
| 346 | 2 | childhood acquaintance of | `(LLM tail)` | Catelyn → Petyr Baelish | agot-catelyn-11 |
| 347 | 2 | Recalls with affection | `LOVES` | Daenerys → Ser Willem Darry | agot-daenerys-01 |
| 348 | 2 | Has had sexual relations with | `(LLM tail)` | Illyrio → Doreah | agot-daenerys-02 |
| 349 | 2 | Physically abuses | `(LLM tail)` | Viserys → Daenerys | agot-daenerys-03 |
| 350 | 2 | Seeks counsel from | `SEEKS` | Daenerys → Ser Jorah | agot-daenerys-04 |
| 351 | 2 | Bitterness toward | `RESENTS` | Ser Jorah → Eddard Stark | agot-daenerys-04 |
| 352 | 2 | Warned | `ADVISES` | Illyrio → Viserys | agot-daenerys-04 |
| 353 | 2 | mother of (unborn) | `PARENT_OF` | Daenerys → Rhaego | agot-daenerys-05 |
| 354 | 2 | proud of | `(LLM tail)` | Khal Drogo → Daenerys | agot-daenerys-05 |
| 355 | 2 | conflicted loyalty toward | `(LLM tail)` | Daenerys → Viserys Targaryen | agot-daenerys-05 |
| 356 | 2 | protects/advises | `PROTECTS` | Ser Jorah Mormont → Daenerys | agot-daenerys-05 |
| 357 | 2 | serves/assists | `SERVES` | Irri → Daenerys | agot-daenerys-05 |
| 358 | 2 | visiting peer of | `(LLM tail)` | Khal Jommo → Khal Drogo | agot-daenerys-05 |
| 359 | 2 | Maternal bond | `(LLM tail)` | Daenerys → Rhaego (unborn) | agot-daenerys-06 |
| 360 | 2 | obeys / serves | `SERVES` | Jhogo → Dany | agot-daenerys-07 |
| 361 | 2 | slaps | `(LLM tail)` | Dany → Eroeh | agot-daenerys-08 |
| 362 | 2 | romantic attachment to | `(LLM tail)` | Ser Jorah → Dany | agot-daenerys-08 |
| 363 | 2 | violent toward | `(LLM tail)` | Haggo → Mirri Maz Duur | agot-daenerys-08 |
| 364 | 2 | antagonist of | `(LLM tail)` | Daenerys → Mirri Maz Duur | agot-daenerys-09 |
| 365 | 2 | former subordinate of | `SERVES` | Ko Pono (Khal Pono) → Khal Drogo | agot-daenerys-09 |
| 366 | 2 | Mourns / loves | `MOURNS` | Daenerys → Khal Drogo | agot-daenerys-10 |
| 367 | 2 | Reluctant loyalty to | `(LLM tail)` | Jhogo → Daenerys | agot-daenerys-10 |
| 368 | 2 | Longing / duty-bound separation | `(LLM tail)` | Ned → Catelyn Stark | agot-eddard-02 |
| 369 | 2 | Kingsguard to | `(LLM tail)` | Ser Boros Blount → Robert | agot-eddard-02 |
| 370 | 2 | Father, protector | `(LLM tail)` | Eddard Stark → Arya Stark | agot-eddard-03 |
| 371 | 2 | Protective mother | `(LLM tail)` | Cersei Lannister → Joffrey Baratheon | agot-eddard-03 |
| 372 | 2 | Loyal service | `SERVES` | Jory Cassel → Eddard Stark | agot-eddard-03 |
| 373 | 2 | remembers with complicated feeling | `(LLM tail)` | Ned → Robert | agot-eddard-04 |
| 374 | 2 | Investigates | `INVESTIGATES` | Ned → Pycelle | agot-eddard-05 |
| 375 | 2 | Overprotective of | `(LLM tail)` | Lysa Arryn → Robert Arryn | agot-eddard-05 |
| 376 | 2 | yearns for | `(LLM tail)` | Ned → Catelyn Stark | agot-eddard-06 |
| 377 | 2 | made armor for | `(LLM tail)` | Tobho Mott → Renly Baratheon | agot-eddard-06 |
| 378 | 2 | infatuated with | `(LLM tail)` | Sansa Stark → Ser Loras Tyrell | agot-eddard-07 |
| 379 | 2 | Depends on | `(LLM tail)` | Ned → Vayon Poole | agot-eddard-08 |
| 380 | 2 | guard to | `(LLM tail)` | Heward → Eddard Stark | agot-eddard-09 |
| 381 | 2 | Hatred for | `HATES` | Robert Baratheon → Rhaegar Targaryen | agot-eddard-10 |
| 382 | 2 | Shows mercy to | `(LLM tail)` | Eddard Stark → Cersei Lannister | agot-eddard-12 |
| 383 | 2 | Longing for family | `(LLM tail)` | Ned → Catelyn, Bran, Robb, Rickon | agot-eddard-13 |
| 384 | 2 | Protective father | `(LLM tail)` | Eddard Stark → Sansa Stark | agot-eddard-14 |
| 385 | 2 | grieves for / fears for | `MOURNS` | Eddard Stark → Sansa Stark | agot-eddard-15 |
| 386 | 2 | claims to serve | `(LLM tail)` | Varys → The realm | agot-eddard-15 |
| 387 | 2 | half-brother | `SIBLING_OF` | Jon Snow → Bran Stark | agot-jon-01 |
| 388 | 2 | half-sister | `SIBLING_OF` | Jon Snow → Arya Stark | agot-jon-01 |
| 389 | 2 | cold toward | `(LLM tail)` | Cersei Lannister → Eddard Stark | agot-jon-01 |
| 390 | 2 | resented by father | `(LLM tail)` | Tyrion Lannister → Tywin Lannister | agot-jon-01 |
| 391 | 2 | mocks and demeans | `OPPOSES` | Ser Alliser Thorne → Jon Snow | agot-jon-03 |
| 392 | 2 | misses deeply | `MOURNS` | Jon Snow → Arya Stark | agot-jon-03 |
| 393 | 2 | Camaraderie | `COMPANION_OF` | Pyp → Grenn | agot-jon-05 |
| 394 | 2 | Love / longing | `LOVES` | Jon Snow → Arya Stark | agot-jon-05 |
| 395 | 2 | Assigned to serve | `(LLM tail)` | Jon Snow → Lord Commander Mormont | agot-jon-06 |
| 396 | 2 | Protector of | `PROTECTS` | Ghost → Jeor Mormont | agot-jon-07 |
| 397 | 2 | Mourns/worries for | `MOURNS` | Jon Snow → Eddard Stark | agot-jon-08 |
| 398 | 2 | Worries for | `(LLM tail)` | Jon Snow → Sansa/Arya (his sisters) | agot-jon-08 |
| 399 | 2 | Bond with direwolf | `(LLM tail)` | Jon Snow → Ghost | agot-jon-09 |
| 400 | 2 | Kill | `(LLM tail)` | The Others → Ser Waymar Royce | agot-prologue |
| 401 | 2 | Idolizes | `(LLM tail)` | Sansa → Joffrey | agot-sansa-01 |
| 402 | 2 | Hostile/contemptuous toward | `(LLM tail)` | Robert → Cersei | agot-sansa-02 |
| 403 | 2 | Close friendship | `COMPANION_OF` | Sansa Stark → Jeyne Poole | agot-sansa-03 |
| 404 | 2 | Disciplinarian over | `COMMANDS` | Septa Mordane → Sansa and Arya | agot-sansa-03 |
| 405 | 2 | Defiance toward | `(LLM tail)` | Arya Stark → Sansa Stark | agot-sansa-03 |
| 406 | 2 | Admiration for | `RESPECTS` | Sansa Stark → Loras Tyrell | agot-sansa-03 |
| 407 | 2 | Disdain toward | `HATES` | Sansa Stark → Yoren/Night's Watch | agot-sansa-03 |
| 408 | 2 | Admired by | `RESPECTS` | Alyn → Sansa Stark | agot-sansa-03 |
| 409 | 2 | Takes custody of | `(LLM tail)` | Petyr Baelish → Jeyne Poole | agot-sansa-04 |
| 410 | 2 | Pleads on behalf of | `(LLM tail)` | Sansa Stark → Eddard Stark | agot-sansa-05 |
| 411 | 2 | Shows sympathy toward | `(LLM tail)` | Varys → Ser Barristan Selmy | agot-sansa-05 |
| 412 | 2 | Indifferent toward | `(LLM tail)` | Ser Meryn Trant → Sansa | agot-sansa-06 |
| 413 | 2 | Master-servant | `(LLM tail)` | Tyrion → Morrec | agot-tyrion-02 |
| 414 | 2 | Resentment / dark fantasy toward | `RESENTS` | Tyrion → Tywin Lannister (father) | agot-tyrion-02 |
| 415 | 2 | sardonic camaraderie with | `COMPANION_OF` | Ser Jaremy Rykker → Tyrion | agot-tyrion-03 |
| 416 | 2 | captive of | `PRISONER_OF` | Tyrion → Catelyn Stark | agot-tyrion-04 |
| 417 | 2 | pragmatic alliance with | `ALLIES_WITH` | Bronn → Tyrion | agot-tyrion-04 |
| 418 | 2 | accompanies | `TRAVELS_WITH` | Marillion → Catelyn's party | agot-tyrion-04 |
| 419 | 2 | commands respect from | `COMMANDS` | Catelyn → Party members | agot-tyrion-04 |
| 420 | 2 | Employer of | `(LLM tail)` | Tyrion → Bronn | agot-tyrion-07 |
| 421 | 2 | Sardonic toward | `(LLM tail)` | Tyrion → Tywin | agot-tyrion-07 |
| 422 | 2 | Complicated feelings toward | `(LLM tail)` | Arya → Sansa | acok-arya-01 |
| 423 | 2 | disguised as | `DISGUISED_AS` | Arya → "Arry" (boy) | acok-arya-02 |
| 424 | 2 | courteous toward | `(LLM tail)` | Jaqen H'ghar → Arya | acok-arya-02 |
| 425 | 2 | Grief for / loss | `MOURNS` | Arya → Ned Stark (Father) | acok-arya-03 |
| 426 | 2 | Scout for | `(LLM tail)` | Koss → Yoren | acok-arya-03 |
| 427 | 2 | combat partnership | `(LLM tail)` | Arya → Gendry | acok-arya-04 |
| 428 | 2 | remembers with longing | `(LLM tail)` | Arya → Her brothers (Jon especially) | acok-arya-04 |
| 429 | 2 | assists | `(LLM tail)` | Chiswyck → The Tickler | acok-arya-06 |
| 430 | 2 | recalls praying with | `(LLM tail)` | Arya → Her mother | acok-arya-06 |
| 431 | 2 | misses/longs for | `MOURNS` | Arya → Robb Stark | acok-arya-07 |
| 432 | 2 | owns/commands | `OWNS` | Weese → His dog (spotted bitch) | acok-arya-07 |
| 433 | 2 | loyal follower of | `(LLM tail)` | Chiswyck → Ser Gregor | acok-arya-07 |
| 434 | 2 | orders death of | `(LLM tail)` | Arya → Chiswyck | acok-arya-07 |
| 435 | 2 | hostile rivalry with | `(LLM tail)` | Ser Amory Lorch → Vargo Hoat | acok-arya-09 |
| 436 | 2 | remembers with grief | `MOURNS` | Arya → Eddard Stark | acok-arya-09 |
| 437 | 2 | remembers/channels | `(LLM tail)` | Arya → Syrio Forel | acok-arya-10 |
| 438 | 2 | bonded to / wargs into | `BONDED_TO` | Bran Stark → Summer | acok-bran-01 |
| 439 | 2 | heir to | `HEIR_TO` | Bran Stark → Robb Stark | acok-bran-01 |
| 440 | 2 | befriends | `(LLM tail)` | Rickon Stark → The Walders | acok-bran-01 |
| 441 | 2 | aggressive toward | `(LLM tail)` | Shaggydog → Little Walder Frey | acok-bran-01 |
| 442 | 2 | seeks marriage with | `SEEKS` | Lord Manderly → Lady Hornwood | acok-bran-02 |
| 443 | 2 | Warging bond with | `WARGS_INTO` | Bran → Summer | acok-bran-03 |
| 444 | 2 | bonded to / warg connection | `BONDED_TO` | Bran → Summer | acok-bran-04 |
| 445 | 2 | trusts/confides in | `TRUSTS` | Bran → Jojen Reed | acok-bran-05 |
| 446 | 2 | callous toward | `(LLM tail)` | Little Walder Frey → Ser Stevron Frey | acok-bran-05 |
| 447 | 2 | agrees with | `(LLM tail)` | Bran → Big Walder | acok-bran-05 |
| 448 | 2 | Claims allegiance to | `(LLM tail)` | Theon → Balon Greyjoy | acok-bran-06 |
| 449 | 2 | commits to accompany | `(LLM tail)` | Jojen → Bran | acok-bran-07 |
| 450 | 2 | king over | `(LLM tail)` | Robb Stark → Greatjon Umber | acok-catelyn-01 |
| 451 | 2 | commands/trusts | `COMMANDS` | Robb → Catelyn | acok-catelyn-02 |
| 452 | 2 | defeated | `(LLM tail)` | Brienne → Ser Loras | acok-catelyn-02 |
| 453 | 2 | Resentment | `RESENTS` | Stannis → Robert (deceased) | acok-catelyn-03 |
| 454 | 2 | Devoted service / love | `LOVES` | Brienne → Renly | acok-catelyn-03 |
| 455 | 2 | Compassion for | `(LLM tail)` | Catelyn → Brienne | acok-catelyn-03 |
| 456 | 2 | Sworn service | `(LLM tail)` | Ser Robar Royce → Renly | acok-catelyn-03 |
| 457 | 2 | Alliance with | `ALLIES_WITH` | Stannis → Red priestess | acok-catelyn-03 |
| 458 | 2 | Devoted to (deceased) | `(LLM tail)` | Brienne → Renly | acok-catelyn-05 |
| 459 | 2 | desires vengeance against | `(LLM tail)` | Catelyn → Theon Greyjoy | acok-catelyn-07 |
| 460 | 2 | Great-niece of | `PARENT_OF` | Lynesse Hightower → The White Bull (Gerold Hightower) | acok-daenerys-01 |
| 461 | 2 | Former ko of | `(LLM tail)` | Khal Pono → Khal Drogo | acok-daenerys-01 |
| 462 | 2 | Competes for Dany's favor with | `(LLM tail)` | Pyat Pree → Xaro Xhoan Daxos | acok-daenerys-02 |
| 463 | 2 | empathizes with | `(LLM tail)` | Daenerys → Viserys | acok-daenerys-03 |
| 464 | 2 | distrusts (partially) | `DISTRUSTS` | Daenerys → Illyrio Mopatis | acok-daenerys-03 |
| 465 | 2 | warns against | `ADVISES` | Xaro → Pyat Pree/warlocks | acok-daenerys-03 |
| 466 | 2 | descends from | `(LLM tail)` | Daenerys → Rhaegar Targaryen | acok-daenerys-05 |
| 467 | 2 | Attempted to kill | `(LLM tail)` | Maester Cressen → Melisandre | acok-davos-01 |
| 468 | 2 | Bitter resentment toward | `RESENTS` | Stannis → Robert Baratheon | acok-davos-02 |
| 469 | 2 | Former sworn protector of | `(LLM tail)` | Bryce Caron → Renly | acok-davos-02 |
| 470 | 2 | Pride in | `(LLM tail)` | Davos → His sons | acok-davos-03 |
| 471 | 2 | Rejects | `(LLM tail)` | Davos → R'hllor / Lord of Light | acok-davos-03 |
| 472 | 2 | Commands/mentors | `COMMANDS` | Lord Commander Mormont → Jon Snow | acok-jon-01 |
| 473 | 2 | Antagonism toward | `(LLM tail)` | Thoren Smallwood → Jon Snow and Sam | acok-jon-01 |
| 474 | 2 | Challenges authority of | `(LLM tail)` | Thoren Smallwood → Lord Commander Mormont | acok-jon-01 |
| 475 | 2 | Remembers/respects | `RESPECTS` | Jon Snow → Ned Stark | acok-jon-02 |
| 476 | 2 | Seeking | `(LLM tail)` | Jon Snow → Benjen Stark | acok-jon-03 |
| 477 | 2 | Commands / mentors | `COMMANDS` | Mormont → Jon Snow | acok-jon-03 |
| 478 | 2 | Friend to | `(LLM tail)` | Jon Snow → Samwell Tarly | acok-jon-05 |
| 479 | 2 | Claims kinship with | `(LLM tail)` | Ygritte → Starks / Jon Snow | acok-jon-06 |
| 480 | 2 | Sacrifices self for | `(LLM tail)` | Squire Dalbridge → The ranging party | acok-jon-07 |
| 481 | 2 | Attacked by | `(LLM tail)` | Ghost → Eagle (skinchanger-controlled) | acok-jon-07 |
| 482 | 2 | Feels loss/separation from | `(LLM tail)` | Jon Snow → Bran, Rickon, Robb | acok-jon-08 |
| 483 | 2 | grudging respect | `RESPECTS` | Stannis → Davos | acok-prologue |
| 484 | 2 | contemptuous | `HATES` | Selyse → Cressen | acok-prologue |
| 485 | 2 | loyalty | `(LLM tail)` | Davos → Stannis | acok-prologue |
| 486 | 2 | political refusal | `(LLM tail)` | Stannis → Robb Stark | acok-prologue |
| 487 | 2 | Uneasy around | `(LLM tail)` | Sansa → Ser Mandon (Moore) | acok-sansa-01 |
| 488 | 2 | indebted to | `(LLM tail)` | Ser Dontos Hollard → Sansa Stark | acok-sansa-02 |
| 489 | 2 | protects (reluctantly) | `PROTECTS` | Sandor Clegane → Sansa | acok-sansa-03 |
| 490 | 2 | serves blindly | `SERVES` | Ser Boros Blount → Joffrey | acok-sansa-03 |
| 491 | 2 | serves loyally | `SERVES` | Bronn → Tyrion | acok-sansa-03 |
| 492 | 2 | Grief/longing for | `MOURNS` | Sansa → Lady (direwolf) | acok-sansa-07 |
| 493 | 2 | Secret alliance with | `ALLIES_WITH` | Sansa → Dontos | acok-sansa-08 |
| 494 | 2 | Envoy of | `(LLM tail)` | Theon Greyjoy → Robb Stark | acok-theon-01 |
| 495 | 2 | Remembered negatively | `(LLM tail)` | Theon Greyjoy → Rodrik Greyjoy | acok-theon-01 |
| 496 | 2 | Overlord / war commander | `COMMANDS` | Balon → Victarion | acok-theon-02 |
| 497 | 2 | Dismissive of uncle | `DISTRUSTS` | Theon → Victarion | acok-theon-02 |
| 498 | 2 | commands/relies on | `COMMANDS` | Theon → Black Lorren | acok-theon-04 |
| 499 | 2 | awaits/fears judgment of | `(LLM tail)` | Theon → Asha Greyjoy | acok-theon-04 |
| 500 | 2 | Bitter enemy of | `RESENTS` | Ser Rodrik → Theon | acok-theon-06 |
| 501 | 2 | employs/commands | `COMMANDS` | Tyrion → Bronn | acok-tyrion-02 |
| 502 | 2 | served/took orders from | `(LLM tail)` | Janos Slynt → Cersei | acok-tyrion-02 |
| 503 | 2 | loyal subordinate of | `SERVES` | Allar Deem → Janos Slynt | acok-tyrion-02 |
| 504 | 2 | Sycophantic toward | `(LLM tail)` | Pycelle → Cersei | acok-tyrion-03 |
| 505 | 2 | Politically opposes | `(LLM tail)` | Stannis → Joffrey / Cersei / Lannisters | acok-tyrion-03 |
| 506 | 2 | Married to (unhappily) | `(LLM tail)` | Stannis → Selyse Florent | acok-tyrion-03 |
| 507 | 2 | Former connection to | `(LLM tail)` | Littlefinger → Catelyn Stark | acok-tyrion-04 |
| 508 | 2 | commands / employs | `COMMANDS` | Tyrion → Bronn | acok-tyrion-05 |
| 509 | 2 | was fond of | `LOVES` | Robert Baratheon (recalled) → Thoros of Myr | acok-tyrion-05 |
| 510 | 2 | obedient to | `(LLM tail)` | Vylarr → Tyrion | acok-tyrion-06 |
| 511 | 2 | patron of | `(LLM tail)` | Cersei → Pycelle | acok-tyrion-07 |
| 512 | 2 | Protective mother of | `(LLM tail)` | Cersei → Joffrey | acok-tyrion-08 |
| 513 | 2 | Verbal sparring, rivalry | `(LLM tail)` | Varys → Littlefinger | acok-tyrion-08 |
| 514 | 2 | Cruelty toward | `(LLM tail)` | Joffrey → Sansa Stark | acok-tyrion-08 |
| 515 | 2 | Abusive toward | `(LLM tail)` | Joffrey → Sansa Stark | acok-tyrion-09 |
| 516 | 2 | Comforts | `(LLM tail)` | Myrcella → Tommen | acok-tyrion-09 |
| 517 | 2 | Serves/advises | `SERVES` | Varys → Tyrion | acok-tyrion-10 |
| 518 | 2 | approves of | `(LLM tail)` | Tyrion → Ser Balon Swann | acok-tyrion-11 |
| 519 | 2 | relies on for intelligence | `(LLM tail)` | Tyrion → Varys | acok-tyrion-11 |
| 520 | 2 | Supports authority of | `(LLM tail)` | Ser Mandon Moore → Tyrion | acok-tyrion-13 |
| 521 | 2 | Distressed about | `(LLM tail)` | Joffrey → His ships | acok-tyrion-13 |
| 522 | 2 | Compares himself to | `(LLM tail)` | Tyrion → Aegon the Conqueror | acok-tyrion-13 |
| 523 | 2 | rivalry / resentment toward | `(LLM tail)` | Tyrion → Jaime | acok-tyrion-15 |
| 524 | 2 | leads / commands | `COMMANDS` | Arya → Gendry | asos-arya-01 |
| 525 | 2 | former student of | `(LLM tail)` | Arya → Syrio Forel | asos-arya-01 |
| 526 | 2 | leads/commands | `COMMANDS` | Arya → Hot Pie | asos-arya-02 |
| 527 | 2 | prays to | `(LLM tail)` | Arya → Old gods / tree gods | asos-arya-02 |
| 528 | 2 | Transactional with | `CONTRACTED_WITH` | Ghost of High Heart → Tom Sevenstrings | asos-arya-04 |
| 529 | 2 | Vengeful toward | `(LLM tail)` | Mad Huntsman → Lannisters/westermen | asos-arya-05 |
| 530 | 2 | Former sworn shield of | `(LLM tail)` | Sandor Clegane → Joffrey Baratheon | asos-arya-06 |
| 531 | 2 | Confesses killing | `(LLM tail)` | Sandor Clegane → Mycah | asos-arya-06 |
| 532 | 2 | Captured | `CAPTURES` | Mad Huntsman → Sandor Clegane | asos-arya-06 |
| 533 | 2 | respects memory of | `RESPECTS` | Lord Beric → Eddard Stark | asos-arya-07 |
| 534 | 2 | wants dead | `(LLM tail)` | Arya → Sandor Clegane, Gregor Clegane, Dunsen, Polliver, Raff, the Tickler, Ser Ilyn, Ser Meryn, Joffrey, Cersei | asos-arya-07 |
| 535 | 2 | attached to | `(LLM tail)` | Ghost of High Heart → "Jenny's song" | asos-arya-08 |
| 536 | 2 | connected to | `(LLM tail)` | Edric Dayne → Jon Snow | asos-arya-08 |
| 537 | 2 | predatory toward | `(LLM tail)` | Sandor Clegane → Arya | asos-arya-08 |
| 538 | 2 | Hopes for rescue from | `(LLM tail)` | Arya Stark → Lord Beric Dondarrion / Brotherhood | asos-arya-09 |
| 539 | 2 | desperately seeks reunion with | `(LLM tail)` | Arya Stark → Robb Stark | asos-arya-10 |
| 540 | 2 | Dominant over | `(LLM tail)` | Summer → Wild wolf pack | asos-bran-01 |
| 541 | 2 | follows guidance of | `(LLM tail)` | Bran Stark → Jojen Reed | asos-bran-02 |
| 542 | 2 | wants to reunite with | `(LLM tail)` | Bran → Jon Snow | asos-bran-03 |
| 543 | 2 | guides | `(LLM tail)` | Jojen Reed → Bran | asos-bran-04 |
| 544 | 2 | married (past) | `(LLM tail)` | Jorah Mormont → Lynesse Hightower | asos-catelyn-05 |
| 545 | 2 | plans to use | `(LLM tail)` | Robb Stark → Howland Reed | asos-catelyn-05 |
| 546 | 2 | valued | `(LLM tail)` | Eddard Stark → Howland Reed | asos-catelyn-05 |
| 547 | 2 | Controlling toward | `(LLM tail)` | Lord Walder Frey → His family | asos-catelyn-06 |
| 548 | 2 | Reports to / serves | `(LLM tail)` | Roose Bolton → Robb | asos-catelyn-06 |
| 549 | 2 | Mother figure to | `(LLM tail)` | Daenerys → Drogon, Rhaegal, Viserion | asos-daenerys-01 |
| 550 | 2 | Knighted and close to | `(LLM tail)` | Rhaegar Targaryen → Myles Mooton | asos-daenerys-01 |
| 551 | 2 | romantic interest in | `(LLM tail)` | Ser Jorah Mormont → Daenerys | asos-daenerys-02 |
| 552 | 2 | serves / loyal to | `SERVES` | Irri → Daenerys | asos-daenerys-02 |
| 553 | 2 | maternal bond with | `(LLM tail)` | Daenerys → Drogon, Viserion | asos-daenerys-02 |
| 554 | 2 | trains | `TEACHES` | Ser Jorah → Grey Worm | asos-daenerys-04 |
| 555 | 2 | protects / is guarded by | `PROTECTS` | Daenerys → Arstan Whitebeard | asos-daenerys-04 |
| 556 | 2 | serve | `(LLM tail)` | Irri, Jhiqui → Daenerys | asos-daenerys-04 |
| 557 | 2 | Grief/loss toward | `MOURNS` | Daenerys → Ser Jorah Mormont | asos-daenerys-06 |
| 558 | 2 | knighted | `(LLM tail)` | Stannis Baratheon → Davos | asos-davos-01 |
| 559 | 2 | Serves/champions | `SERVES` | Melisandre → Stannis | asos-davos-03 |
| 560 | 2 | Uncle to | `UNCLE_OF` | Lord Alester Florent → Queen Selyse | asos-davos-03 |
| 561 | 2 | Tends | `(LLM tail)` | Porridge (gaoler) → Davos | asos-davos-03 |
| 562 | 2 | Heals | `HEALS` | Maester Pylos → Davos | asos-davos-03 |
| 563 | 2 | Burned | `(LLM tail)` | Melisandre → Guncer Sunglass | asos-davos-03 |
| 564 | 2 | Conflicted toward | `(LLM tail)` | Stannis → Edric Storm | asos-davos-05 |
| 565 | 2 | Ambivalent toward | `(LLM tail)` | Stannis → R'hllor worship | asos-davos-06 |
| 566 | 2 | Replaced | `(LLM tail)` | Maester Pylos → Maester Cressen | asos-davos-06 |
| 567 | 2 | family bond | `(LLM tail)` | Jaime → Cersei | asos-jaime-04 |
| 568 | 2 | commands/sends | `COMMANDS` | Roose Bolton → Steelshanks Walton | asos-jaime-06 |
| 569 | 2 | compares | `(LLM tail)` | Jaime → Gregor Clegane / bear | asos-jaime-06 |
| 570 | 2 | Mourning mother | `MOURNS` | Cersei → Joffrey | asos-jaime-07 |
| 571 | 2 | Coordinated with | `(LLM tail)` | Tywin → Roose Bolton | asos-jaime-07 |
| 572 | 2 | commands (Lord Commander) | `COMMANDS` | Jaime → Ser Boros, Ser Meryn, Ser Osmund, Ser Balon, Ser Loras | asos-jaime-08 |
| 573 | 2 | political control over | `(LLM tail)` | Lord Tywin → Tommen | asos-jaime-09 |
| 574 | 2 | Guards (friendly) | `GUARDS` | Ygritte → Jon Snow | asos-jon-01 |
| 575 | 2 | Former brother of | `SIBLING_OF` | Mance Rayder → Night's Watch | asos-jon-01 |
| 576 | 2 | Informant for | `(LLM tail)` | Craster → Night's Watch | asos-jon-01 |
| 577 | 2 | Hostile | `(LLM tail)` | Rattleshirt → Jon Snow | asos-jon-02 |
| 578 | 2 | reported killer of | `(LLM tail)` | Theon Greyjoy → Bran Stark | asos-jon-06 |
| 579 | 2 | Memory / affection | `LOVES` | Jon Snow → Benjen Stark | asos-jon-07 |
| 580 | 2 | Chose | `(LLM tail)` | Qhorin Halfhand → Jon Snow | asos-jon-08 |
| 581 | 2 | Allies with | `ALLIES_WITH` | Slynt → Thorne | asos-jon-09 |
| 582 | 2 | Dismissed by | `(LLM tail)` | Donal Noye → Slynt | asos-jon-09 |
| 583 | 2 | Respects/mourns | `RESPECTS` | Jon Snow → Qhorin Halfhand | asos-jon-10 |
| 584 | 2 | Compares self unfavorably to | `(LLM tail)` | Jon Snow → Robb Stark | asos-jon-10 |
| 585 | 2 | Friendly toward | `COMPANION_OF` | Tormund → Jon Snow | asos-jon-10 |
| 586 | 2 | Respects the memory of | `RESPECTS` | Stannis Baratheon → Eddard Stark | asos-jon-11 |
| 587 | 2 | Friendship/dependency | `COMPANION_OF` | Sam → Grenn | asos-samwell-01 |
| 588 | 2 | resent | `(LLM tail)` | Brothers (multiple) → Craster | asos-samwell-02 |
| 589 | 2 | self-loathing | `(LLM tail)` | Sam → Himself | asos-samwell-02 |
| 590 | 2 | grief/guilt toward | `MOURNS` | Sam → Lord Mormont | asos-samwell-03 |
| 591 | 2 | Grief/loss | `MOURNS` | Jon Snow → Ygritte | asos-samwell-04 |
| 592 | 2 | Enmity | `(LLM tail)` | Craster → Mance Rayder | asos-samwell-04 |
| 593 | 2 | Uncomfortable with | `(LLM tail)` | Stannis → Melisandre | asos-samwell-05 |
| 594 | 2 | Humiliates | `(LLM tail)` | Joffrey Baratheon → Tyrion Lannister | asos-sansa-03 |
| 595 | 2 | Paramour of | `(LLM tail)` | Prince Oberyn → Ellaria Sand | asos-sansa-04 |
| 596 | 2 | Suspects / accuses | `(LLM tail)` | Cersei Lannister → Tyrion Lannister | asos-sansa-05 |
| 597 | 2 | Marries | `(LLM tail)` | Petyr Baelish → Lysa Arryn | asos-sansa-06 |
| 598 | 2 | Assesses contemptuously | `(LLM tail)` | Petyr Baelish → Cersei Lannister | asos-sansa-06 |
| 599 | 2 | Obsessively devoted to | `(LLM tail)` | Lysa Arryn → Petyr Baelish | asos-sansa-06 |
| 600 | 2 | longs for / mourns | `MOURNS` | Sansa Stark → Winterfell / home | asos-sansa-07 |
| 601 | 2 | Grateful toward | `(LLM tail)` | Kingslanders → House Tyrell | asos-tyrion-01 |
| 602 | 2 | Serves as Kingsguard | `SERVES` | Ser Loras Tyrell → The Crown | asos-tyrion-02 |
| 603 | 2 | dominates/controls | `(LLM tail)` | Tywin Lannister → Tyrion Lannister | asos-tyrion-03 |
| 604 | 2 | pressures | `(LLM tail)` | Tywin → Tyrion | asos-tyrion-04 |
| 605 | 2 | Domineering control over | `(LLM tail)` | Tywin → Joffrey | asos-tyrion-06 |
| 606 | 2 | Threatened | `(LLM tail)` | Cersei → Robert Baratheon | asos-tyrion-06 |
| 607 | 2 | Considers marrying Shae to | `(LLM tail)` | Tyrion → Bronn | asos-tyrion-07 |
| 608 | 2 | Desecrated the corpse of | `(LLM tail)` | The Freys → Robb Stark | asos-tyrion-07 |
| 609 | 2 | gave gift to | `GIFTED_TO` | Tywin → The Faith | asos-tyrion-08 |
| 610 | 2 | abandoned by | `(LLM tail)` | Tyrion → Bronn | asos-tyrion-09 |
| 611 | 2 | Brutalized | `(LLM tail)` | Tywin → Tysha | asos-tyrion-11 |
| 612 | 2 | Political manipulation of | `(LLM tail)` | Petyr Baelish → Lady Waynwood | affc-alayne-02 |
| 613 | 2 | believes dead | `(LLM tail)` | Arya → Bran Stark | affc-arya-01 |
| 614 | 2 | tested by | `(LLM tail)` | Arya → The kindly man | affc-arya-01 |
| 615 | 2 | Trained | `(LLM tail)` | Ser Goodwin → Brienne | affc-brienne-02 |
| 616 | 2 | Suspicion of | `(LLM tail)` | Brienne → Ser Shadrich | affc-brienne-02 |
| 617 | 2 | mourns/regrets failing | `MOURNS` | Brienne → Renly Baratheon | affc-brienne-04 |
| 618 | 2 | defeated in mêlée | `(LLM tail)` | Brienne → Ronnet Connington | affc-brienne-04 |
| 619 | 2 | Quest loyalty to | `(LLM tail)` | Brienne → Sansa Stark | affc-brienne-05 |
| 620 | 2 | Old friend / regular visitor | `(LLM tail)` | Septon Meribald → Elder Brother | affc-brienne-06 |
| 621 | 2 | Vow sworn to | `(LLM tail)` | Brienne → Jaime (Lannister) | affc-brienne-06 |
| 622 | 2 | Hunting outlaws from | `(LLM tail)` | Randyll Tarly → Maidenpool | affc-brienne-06 |
| 623 | 2 | Performs marriages | `(LLM tail)` | Ezzelyno → Happy Port whores and customers | affc-cat-of-the-canals-01 |
| 624 | 2 | Mistrust | `DISTRUSTS` | Cersei → Mace Tyrell | affc-cersei-01 |
| 625 | 2 | Contempt toward past | `HATES` | Cersei → Jon Arryn | affc-cersei-01 |
| 626 | 2 | Brother of (grieving) | `SIBLING_OF` | Kevan → Tywin (deceased) | affc-cersei-02 |
| 627 | 2 | political rival / bitter enemy | `RESENTS` | Cersei → Margaery Tyrell | affc-cersei-03 |
| 628 | 2 | grief/resentment toward | `MOURNS` | Cersei → Tywin Lannister | affc-cersei-04 |
| 629 | 2 | Romantically interested in | `(LLM tail)` | Megga Tyrell → Mark Mullendore | affc-cersei-06 |
| 630 | 2 | Serves/devoted to | `SERVES` | Qyburn → Cersei | affc-cersei-07 |
| 631 | 2 | Flatters | `(LLM tail)` | Orton Merryweather → Cersei | affc-cersei-07 |
| 632 | 2 | Evaluates/uses | `(LLM tail)` | Cersei → Osmund Kettleblack | affc-cersei-08 |
| 633 | 2 | compares to Robert | `(LLM tail)` | Cersei → Osney Kettleblack | affc-cersei-09 |
| 634 | 2 | claimed to have killed | `(LLM tail)` | Tyrion → Joffrey | affc-jaime-01 |
| 635 | 2 | Formerly married to | `(LLM tail)` | Lady Mariya → Merrett Frey | affc-jaime-04 |
| 636 | 2 | Former lover | `LOVER_OF` | Lancel → Cersei | affc-jaime-04 |
| 637 | 2 | fondness for | `(LLM tail)` | Jaime → Gerion Lannister | affc-jaime-07 |
| 638 | 2 | suspects/accuses | `(LLM tail)` | Edwyn Frey → Black Walder | affc-jaime-07 |
| 639 | 2 | Failed by / submitted to | `(LLM tail)` | Pate → Archmaester Vaellyn | affc-prologue |
| 640 | 2 | nurses | `(LLM tail)` | Gilly → Dalla's son | affc-samwell-02 |
| 641 | 2 | bullied | `(LLM tail)` | Horas Redwyne → Young Samwell Tarly | affc-samwell-02 |
| 642 | 2 | mourns / remembers | `MOURNS` | Maester Aemon → Egg (Aegon V) | affc-samwell-03 |
| 643 | 2 | saved | `(LLM tail)` | Xhondo → Sam | affc-samwell-04 |
| 644 | 2 | misses / would turn to | `MOURNS` | Sam → Jon Snow | affc-samwell-04 |
| 645 | 2 | Deep distrust of | `(LLM tail)` | Archmaester Marwyn → The Citadel ("grey sheep") | affc-samwell-05 |
| 646 | 2 | Resented | `(LLM tail)` | Ser Marwyn Belmore → Marillion | affc-sansa-01 |
| 647 | 2 | Uncle | `UNCLE_OF` | Victarion → Asha | affc-the-iron-captain-01 |
| 648 | 2 | Hostile to | `OPPOSES` | Aeron → Euron | affc-the-iron-captain-01 |
| 649 | 2 | Rivals | `(LLM tail)` | Victarion → Euron | affc-the-iron-captain-01 |
| 650 | 2 | Has support of | `(LLM tail)` | Asha → House Harlaw (Rodrik the Reader) | affc-the-iron-captain-01 |
| 651 | 2 | childhood companions with | `(LLM tail)` | Arianne Martell → Nymeria Sand (Nym) | affc-the-princess-in-the-tower-01 |
| 652 | 2 | not close to | `(LLM tail)` | Arianne Martell → Quentyn Martell | affc-the-princess-in-the-tower-01 |
| 653 | 2 | Protector | `(LLM tail)` | Arianne Martell → Princess Myrcella | affc-the-queenmaker-01 |
| 654 | 2 | Raped | `(LLM tail)` | Euron → Victarion's wife | affc-the-reaver-01 |
| 655 | 2 | Works with | `(LLM tail)` | Lady Dustin → Roose Bolton | adwd-a-ghost-in-winterfell-01 |
| 656 | 2 | Seeks to use | `SEEKS` | Abel (washerwomen) → Theon | adwd-a-ghost-in-winterfell-01 |
| 657 | 2 | Possessive of | `(LLM tail)` | Ramsay Bolton → Yellow Dick | adwd-a-ghost-in-winterfell-01 |
| 658 | 2 | wargs into / skinchanges | `WARGS_INTO` | Bran → Summer | adwd-bran-01 |
| 659 | 2 | Resents / hates | `RESENTS` | Cersei → Septa Unella | adwd-cersei-02 |
| 660 | 2 | Political rival of | `OPPOSES` | Cersei → Margaery Tyrell | adwd-cersei-02 |
| 661 | 2 | rules/commands | `RULES` | Daenerys → Grey Worm | adwd-daenerys-01 |
| 662 | 2 | is advised by | `(LLM tail)` | Daenerys → Reznak mo Reznak | adwd-daenerys-06 |
| 663 | 2 | Suitor to | `(LLM tail)` | Quentyn Martell → Daenerys | adwd-daenerys-07 |
| 664 | 2 | affected by | `(LLM tail)` | Strong Belwas → Honeyed locusts | adwd-daenerys-09 |
| 665 | 2 | queen to | `(LLM tail)` | Daenerys → Ser Barristan Selmy | adwd-daenerys-10 |
| 666 | 2 | kin to | `(LLM tail)` | Ser Jared Frey → Jinglebell | adwd-davos-03 |
| 667 | 2 | conditional allegiance to | `(LLM tail)` | Manderly → King Stannis | adwd-davos-04 |
| 668 | 2 | Murders | `KILLS` | Varys → Kevan Lannister | adwd-epilogue |
| 669 | 2 | Grieves / believes dead | `MOURNS` | Jon Snow → Bran Stark | adwd-jon-01 |
| 670 | 2 | Warging bond | `WARGS_INTO` | Jon Snow → Ghost | adwd-jon-03 |
| 671 | 2 | Tensions with | `(LLM tail)` | Jon Snow → Bowen Marsh | adwd-jon-03 |
| 672 | 2 | Guest of | `GUEST_OF` | Stannis Baratheon → Night's Watch | adwd-jon-03 |
| 673 | 2 | Religious authority over | `(LLM tail)` | Melisandre → Queen's men | adwd-jon-03 |
| 674 | 2 | Aspires to | `(LLM tail)` | Ser Richard Horpe → Winterfell | adwd-jon-04 |
| 675 | 2 | Subordinate dissatisfied with | `SERVES` | Cotter Pyke → Jon Snow | adwd-jon-06 |
| 676 | 2 | wishes present | `(LLM tail)` | Jon Snow → Sam Tarly | adwd-jon-08 |
| 677 | 2 | secretly allied with | `ALLIES_WITH` | Arnolf Karstark → Roose Bolton | adwd-jon-09 |
| 678 | 2 | Grief/longing | `MOURNS` | Jon Snow → Arya Stark | adwd-jon-11 |
| 679 | 2 | Father | `(LLM tail)` | Tormund → Toregg | adwd-jon-11 |
| 680 | 2 | Disapproval | `(LLM tail)` | Queen Selyse → Jon Snow | adwd-jon-11 |
| 681 | 2 | Swears allegiance to | `(LLM tail)` | Morna White Mask → Jon Snow | adwd-jon-12 |
| 682 | 2 | Antagonized by / distrusted by | `OPPOSES` | Jon Snow → Bowen Marsh | adwd-jon-13 |
| 683 | 2 | Squire serving | `(LLM tail)` | Big Walder Frey → Ramsay Bolton | adwd-reek-01 |
| 684 | 2 | Leads vanguard for | `COMMANDS` | Hosteen Frey → Roose Bolton | adwd-reek-02 |
| 685 | 2 | Student/trainee | `TUTORS` | Arya → The kindly man | adwd-the-blind-girl-01 |
| 686 | 2 | Nostalgic affection | `LOVES` | Arya → Cat of the Canals identity | adwd-the-blind-girl-01 |
| 687 | 2 | Nephew of | `NEPHEW_OF` | Quentyn Martell → Prince Lewyn Martell | adwd-the-discarded-knight-01 |
| 688 | 2 | Longing for / regret | `(LLM tail)` | Quentyn Martell → Gwyneth Yronwood | adwd-the-dragontamer-01 |
| 689 | 2 | sent to capture | `(LLM tail)` | Ser Tristan Rivers → Crow's Nest (House Morrigen) | adwd-the-griffin-reborn-01 |
| 690 | 2 | Hostility from | `(LLM tail)` | Moqorro → Dusky woman | adwd-the-iron-suitor-01 |
| 691 | 2 | Subordinate captain to | `SERVES` | The Vole → Victarion | adwd-the-iron-suitor-01 |
| 692 | 2 | Loyal protector of | `(LLM tail)` | Barristan → Daenerys Targaryen | adwd-the-kingbreaker-01 |
| 693 | 2 | Eager for battle | `(LLM tail)` | Symon Stripeback → Yunkai'i | adwd-the-kingbreaker-01 |
| 694 | 2 | Support | `(LLM tail)` | Laswell Peake → Aegon | adwd-the-lost-lord-01 |
| 695 | 2 | Leader/commander of | `COMMANDS` | Quentyn Martell → Ser Gerris Drinkwater | adwd-the-spurned-suitor-01 |
| 696 | 2 | Student/acolyte of | `TUTORS` | Arya → The kindly man | adwd-the-ugly-little-girl-01 |
| 697 | 2 | Guarded by | `(LLM tail)` | The old man → The tall thin guard | adwd-the-ugly-little-girl-01 |
| 698 | 2 | Brother of (dead) | `SIBLING_OF` | Prince Doran → Oberyn Martell | adwd-the-watcher-01 |
| 699 | 2 | Professional rapport with | `(LLM tail)` | Haldon → Qavo Nogarys | adwd-tyrion-06 |
| 700 | 2 | Hated by | `(LLM tail)` | Tyrion Lannister → Cersei Lannister | adwd-tyrion-07 |
| 701 | 1 | sibling rivalry / resentment | `(LLM tail)` | Arya → Sansa | agot-arya-01 |
| 702 | 1 | deep closeness | `LOVES` | Arya → Jon Snow | agot-arya-01 |
| 703 | 1 | bonded to / loves | `BONDED_TO` | Arya → Nymeria | agot-arya-01 |
| 704 | 1 | dearest friend | `(LLM tail)` | Sansa → Jeyne Poole | agot-arya-01 |
| 705 | 1 | admires / follows | `RESPECTS` | Beth Cassel → Sansa | agot-arya-01 |
| 706 | 1 | infatuation | `(LLM tail)` | Sansa → Joffrey | agot-arya-01 |
| 707 | 1 | flattery toward | `(LLM tail)` | Joffrey → Sansa | agot-arya-01 |
| 708 | 1 | cautious greeting | `(LLM tail)` | Ghost → Nymeria | agot-arya-01 |
| 709 | 1 | wary approach | `(LLM tail)` | Nymeria → Ghost | agot-arya-01 |
| 710 | 1 | fawning toward | `(LLM tail)` | Septa Mordane → Myrcella | agot-arya-01 |
| 711 | 1 | eagerness to fight | `(LLM tail)` | Robb → Joffrey | agot-arya-01 |
| 712 | 1 | restrains / supports | `(LLM tail)` | Theon Greyjoy → Robb | agot-arya-01 |
| 713 | 1 | resemble | `(LLM tail)` | Robb, Sansa, Bran, Rickon → Tullys | agot-arya-01 |
| 714 | 1 | sister, hostile/estranged | `SIBLING_OF` | Arya → Sansa | agot-arya-02 |
| 715 | 1 | daughter, deep love/trust | `LOVES` | Arya → Ned Stark | agot-arya-02 |
| 716 | 1 | father, protective/understanding | `(LLM tail)` | Ned Stark → Arya | agot-arya-02 |
| 717 | 1 | grief/guilt over | `MOURNS` | Arya → Mycah | agot-arya-02 |
| 718 | 1 | duty/resentment | `(LLM tail)` | Ned Stark → Robert Baratheon | agot-arya-02 |
| 719 | 1 | teacher/student | `TUTORS` | Syrio Forel → Arya | agot-arya-02 |
| 720 | 1 | former servant | `(LLM tail)` | Syrio Forel → Sealord of Braavos | agot-arya-02 |
| 721 | 1 | loyalty/protectiveness toward | `(LLM tail)` | Arya → Jon Snow | agot-arya-02 |
| 722 | 1 | guard/fond of | `LOVES` | Fat Tom → Arya | agot-arya-02 |
| 723 | 1 | Daughter of, reports to | `(LLM tail)` | Arya Stark → Eddard Stark | agot-arya-03 |
| 724 | 1 | Misses, wishes for | `MOURNS` | Arya Stark → Jon Snow | agot-arya-03 |
| 725 | 1 | Condescends toward | `(LLM tail)` | Myrcella Baratheon → Arya (unrecognized) | agot-arya-03 |
| 726 | 1 | Follows sister's lead | `SIBLING_OF` | Tommen Baratheon → Myrcella Baratheon | agot-arya-03 |
| 727 | 1 | Flatters / relies on | `(LLM tail)` | Fat man (forked beard) → Stout man (torchbearer) | agot-arya-03 |
| 728 | 1 | Welcomes | `(LLM tail)` | Eddard Stark → Night's Watch | agot-arya-03 |
| 729 | 1 | Guards / serves | `GUARDS` | Desmond → Eddard Stark | agot-arya-03 |
| 730 | 1 | Teacher/protector of | `TUTORS` | Syrio Forel → Arya Stark | agot-arya-04 |
| 731 | 1 | Student/trusts | `TUTORS` | Arya Stark → Syrio Forel | agot-arya-04 |
| 732 | 1 | Hostile toward / attempting to capture | `OPPOSES` | Ser Meryn Trant → Arya Stark | agot-arya-04 |
| 733 | 1 | Hostile toward / attempts to capture | `OPPOSES` | Stableboy → Arya Stark | agot-arya-04 |
| 734 | 1 | Loves/misses | `LOVES` | Arya Stark → Jon Snow | agot-arya-04 |
| 735 | 1 | daughter of, desperate to save | `(LLM tail)` | Arya → Eddard Stark | agot-arya-05 |
| 736 | 1 | scowls at, puzzled by | `(LLM tail)` | Arya → Sansa Stark | agot-arya-05 |
| 737 | 1 | protects and disguises | `PROTECTS` | Yoren → Arya | agot-arya-05 |
| 738 | 1 | Bastard son of | `(LLM tail)` | Jon Snow → Eddard Stark | agot-bran-01 |
| 739 | 1 | Captain of household guard for | `(LLM tail)` | Jory Cassel → Eddard Stark | agot-bran-01 |
| 740 | 1 | Master of horse for | `(LLM tail)` | Hullen → Eddard Stark | agot-bran-01 |
| 741 | 1 | Excluded from / self-excludes from | `(LLM tail)` | Jon Snow → House Stark | agot-bran-01 |
| 742 | 1 | Regards thoughtfully | `(LLM tail)` | Ned Stark → Jon Snow | agot-bran-01 |
| 743 | 1 | Commands / asserts authority over | `COMMANDS` | Robb Stark → Theon Greyjoy | agot-bran-01 |
| 744 | 1 | Has coloring of | `(LLM tail)` | Robb Stark → House Tully | agot-bran-01 |
| 745 | 1 | Teacher/mentor to | `TUTORS` | Ned Stark → Bran Stark | agot-bran-01 |
| 746 | 1 | dreams of becoming | `DREAMS_OF` | Bran Stark → Knight | agot-bran-02 |
| 747 | 1 | angry at / distant from | `(LLM tail)` | Jon Snow → Everyone | agot-bran-02 |
| 748 | 1 | going with | `(LLM tail)` | Jon Snow → Benjen Stark | agot-bran-02 |
| 749 | 1 | sibling/sexual partner of | `(LLM tail)` | Cersei Lannister → Jaime Lannister | agot-bran-02 |
| 750 | 1 | pushes/attempts to kill | `(LLM tail)` | Jaime Lannister → Bran Stark | agot-bran-02 |
| 751 | 1 | loves (still) | `LOVES` | Robert Baratheon → Lyanna Stark | agot-bran-02 |
| 752 | 1 | fled from | `(LLM tail)` | Lysa Arryn → King's Landing | agot-bran-02 |
| 753 | 1 | shared bed with | `(LLM tail)` | Lysa Arryn → Jon Arryn | agot-bran-02 |
| 754 | 1 | threatens (implicitly) | `OPPOSES` | Cersei Lannister → Robin Arryn | agot-bran-02 |
| 755 | 1 | has authority over | `(LLM tail)` | Eddard Stark → Bran Stark | agot-bran-02 |
| 756 | 1 | storyteller/caretaker to | `(LLM tail)` | Old Nan → Bran Stark | agot-bran-02 |
| 757 | 1 | teacher/guardian to | `TUTORS` | Maester Luwin → Bran Stark | agot-bran-02 |
| 758 | 1 | serves/cares for | `SERVES` | Hodor → Bran Stark | agot-bran-02 |
| 759 | 1 | frightened of | `(LLM tail)` | Bran Stark → Heart tree | agot-bran-02 |
| 760 | 1 | Teacher / guide | `(LLM tail)` | Three-eyed crow → Bran | agot-bran-03 |
| 761 | 1 | Names and bonds with | `(LLM tail)` | Bran → Summer | agot-bran-03 |
| 762 | 1 | Protective companion | `COMPANION_OF` | Summer → Bran | agot-bran-03 |
| 763 | 1 | Concerned brother | `SIBLING_OF` | Robb → Bran | agot-bran-03 |
| 764 | 1 | Son, recalls father's courage | `(LLM tail)` | Bran → Eddard Stark | agot-bran-03 |
| 765 | 1 | Mother, separated from Bran | `(LLM tail)` | Catelyn → Bran | agot-bran-03 |
| 766 | 1 | Aware observer | `(LLM tail)` | Weirwood → Bran | agot-bran-03 |
| 767 | 1 | Threatening memory | `(LLM tail)` | Golden face → Bran | agot-bran-03 |
| 768 | 1 | brotherly affection | `LOVES` | Bran → Robb | agot-bran-04 |
| 769 | 1 | acting lord role | `(LLM tail)` | Robb → Winterfell | agot-bran-04 |
| 770 | 1 | emotional bond | `(LLM tail)` | Robb → Bran | agot-bran-04 |
| 771 | 1 | anger regarding | `(LLM tail)` | Robb → Benjen Stark (missing) | agot-bran-04 |
| 772 | 1 | mocking | `(LLM tail)` | Theon Greyjoy → Tyrion | agot-bran-04 |
| 773 | 1 | spends time with | `(LLM tail)` | Robb → Theon Greyjoy, Hallis Mollen | agot-bran-04 |
| 774 | 1 | caretaker / storyteller | `(LLM tail)` | Old Nan → Bran | agot-bran-04 |
| 775 | 1 | great-grandmother of | `PARENT_OF` | Old Nan → Hodor | agot-bran-04 |
| 776 | 1 | practical advisor | `(LLM tail)` | Maester Luwin → Robb | agot-bran-04 |
| 777 | 1 | intellectual engagement | `(LLM tail)` | Maester Luwin → Tyrion's saddle design | agot-bran-04 |
| 778 | 1 | Brother, looks up to | `SIBLING_OF` | Bran → Robb | agot-bran-05 |
| 779 | 1 | Distrust / dislike | `DISTRUSTS` | Bran → Theon Greyjoy | agot-bran-05 |
| 780 | 1 | Apparent friendship but anger | `COMPANION_OF` | Robb → Theon Greyjoy | agot-bran-05 |
| 781 | 1 | Sexual familiarity | `(LLM tail)` | Theon → Kyra | agot-bran-05 |
| 782 | 1 | Grief / fond memory | `MOURNS` | Bran → Jory Cassel | agot-bran-05 |
| 783 | 1 | Missing | `MOURNS` | Bran → Jon Snow | agot-bran-05 |
| 784 | 1 | Surrenders to / serves | `(LLM tail)` | Osha → Robb | agot-bran-05 |
| 785 | 1 | Contempt / hostility | `HATES` | Stiv → Bran | agot-bran-05 |
| 786 | 1 | Pragmatic self-interest | `(LLM tail)` | Osha → Bran | agot-bran-05 |
| 787 | 1 | Competitive / self-congratulatory | `(LLM tail)` | Theon → Robb | agot-bran-05 |
| 788 | 1 | Ambivalent memory | `(LLM tail)` | Bran → Tyrion Lannister | agot-bran-05 |
| 789 | 1 | Acting lord, receives counsel | `ADVISES` | Robb → Hallis Mollen | agot-bran-05 |
| 790 | 1 | brother, subordinate to | `SIBLING_OF` | Bran → Robb | agot-bran-06 |
| 791 | 1 | acting lord over | `(LLM tail)` | Robb → Northern bannermen | agot-bran-06 |
| 792 | 1 | private vulnerability with | `(LLM tail)` | Robb → Bran | agot-bran-06 |
| 793 | 1 | distraught about losing | `(LLM tail)` | Rickon → Robb | agot-bran-06 |
| 794 | 1 | initially hostile, then fiercely loyal to | `(LLM tail)` | Greatjon Umber → Robb | agot-bran-06 |
| 795 | 1 | unsettling presence toward | `(LLM tail)` | Roose Bolton → Robb | agot-bran-06 |
| 796 | 1 | blunt respect toward | `RESPECTS` | Maege Mormont → Robb | agot-bran-06 |
| 797 | 1 | currying favor with | `(LLM tail)` | Lord Hornwood → Robb | agot-bran-06 |
| 798 | 1 | informant/supplicant to | `(LLM tail)` | Osha → Bran | agot-bran-06 |
| 799 | 1 | misses, prays for | `MOURNS` | Bran → Eddard Stark | agot-bran-06 |
| 800 | 1 | understands | `(LLM tail)` | Bran → Sansa | agot-bran-06 |
| 801 | 1 | kinship (distant) with | `(LLM tail)` | Karstarks → Starks | agot-bran-06 |
| 802 | 1 | speaks of with familiarity | `(LLM tail)` | Osha → Mance Rayder | agot-bran-06 |
| 803 | 1 | exercises authority over | `(LLM tail)` | Bran → Maester Luwin | agot-bran-07 |
| 804 | 1 | mourns/grieves for | `MOURNS` | Bran → Eddard Stark | agot-bran-07 |
| 805 | 1 | frustrated by disability | `(LLM tail)` | Bran → (self) | agot-bran-07 |
| 806 | 1 | grieving/desperate for | `MOURNS` | Rickon → Eddard Stark | agot-bran-07 |
| 807 | 1 | rationalist / dismissive of magic | `(LLM tail)` | Maester Luwin → Osha | agot-bran-07 |
| 808 | 1 | contradicts | `(LLM tail)` | Osha → Maester Luwin | agot-bran-07 |
| 809 | 1 | loyal/obedient to | `(LLM tail)` | Osha → Starks | agot-bran-07 |
| 810 | 1 | gentle toward | `(LLM tail)` | Osha → Bran | agot-bran-07 |
| 811 | 1 | wild/dangerous | `(LLM tail)` | Shaggydog → Maester Luwin | agot-bran-07 |
| 812 | 1 | trains/disciplines | `TEACHES` | Ser Rodrik → Recruits | agot-bran-07 |
| 813 | 1 | refuses to enter | `(LLM tail)` | Hodor → Winterfell crypts | agot-bran-07 |
| 814 | 1 | habitual concern for children | `(LLM tail)` | Ned Stark → Catelyn | agot-catelyn-01 |
| 815 | 1 | foster-son of | `WARD_OF` | Ned Stark → Jon Arryn | agot-catelyn-01 |
| 816 | 1 | fellow ward with | `(LLM tail)` | Ned Stark → Robert Baratheon | agot-catelyn-01 |
| 817 | 1 | antipathy toward | `(LLM tail)` | Ned Stark → The Lannisters | agot-catelyn-01 |
| 818 | 1 | deep friendship with | `COMPANION_OF` | Ned Stark → Robert Baratheon | agot-catelyn-01 |
| 819 | 1 | raised banners to protect | `(LLM tail)` | Jon Arryn → Ned and Robert | agot-catelyn-01 |
| 820 | 1 | religious contrast with | `(LLM tail)` | Catelyn → Ned Stark | agot-catelyn-01 |
| 821 | 1 | seeks solace in | `SEEKS` | Ned Stark → Winterfell godswood | agot-catelyn-01 |
| 822 | 1 | built for | `(LLM tail)` | Ned Stark → Catelyn | agot-catelyn-01 |
| 823 | 1 | trust in / reliance on | `TRUSTS` | Ned Stark → Maester Luwin | agot-catelyn-01 |
| 824 | 1 | lord served by | `(LLM tail)` | Ned Stark → Jory | agot-catelyn-01 |
| 825 | 1 | Wife, political counselor | `ADVISES` | Catelyn Stark → Eddard Stark | agot-catelyn-02 |
| 826 | 1 | Was originally betrothed to | `BETROTHED_TO` | Catelyn Stark → Brandon Stark | agot-catelyn-02 |
| 827 | 1 | Married in place of his dead brother | `SIBLING_OF` | Eddard Stark → Catelyn Stark | agot-catelyn-02 |
| 828 | 1 | Deep bond, "closer than brothers" | `(LLM tail)` | Eddard Stark → Robert Baratheon | agot-catelyn-02 |
| 829 | 1 | Sister, shared childhood language | `SIBLING_OF` | Catelyn Stark → Lysa Arryn | agot-catelyn-02 |
| 830 | 1 | Grew up with | `(LLM tail)` | Catelyn Stark → Edmure Tully | agot-catelyn-02 |
| 831 | 1 | Father, protective | `(LLM tail)` | Eddard Stark → Jon Snow | agot-catelyn-02 |
| 832 | 1 | Father, trusts with governance | `(LLM tail)` | Eddard Stark → Robb Stark | agot-catelyn-02 |
| 833 | 1 | Protective, reluctant to separate from | `(LLM tail)` | Eddard Stark → Bran Stark | agot-catelyn-02 |
| 834 | 1 | Deep trust | `(LLM tail)` | Eddard Stark → Maester Luwin | agot-catelyn-02 |
| 835 | 1 | Trusted counselor and advisor to | `ADVISES` | Maester Luwin → Eddard & Catelyn Stark | agot-catelyn-02 |
| 836 | 1 | Concern for / mentoring | `TUTORS` | Benjen Stark → Jon Snow | agot-catelyn-02 |
| 837 | 1 | Slew in combat (recalled) | `(LLM tail)` | Eddard Stark → Ser Arthur Dayne | agot-catelyn-02 |
| 838 | 1 | Possible romantic connection (rumored) | `(LLM tail)` | Eddard Stark → Ashara Dayne | agot-catelyn-02 |
| 839 | 1 | Tension / "bad feeling" with | `(LLM tail)` | Robb Stark → Joffrey Baratheon | agot-catelyn-02 |
| 840 | 1 | Ensures exclusion of | `(LLM tail)` | Cersei Lannister → Robert's bastards | agot-catelyn-02 |
| 841 | 1 | Mother, devoted to the point of obsession | `(LLM tail)` | Catelyn → Bran | agot-catelyn-03 |
| 842 | 1 | Mother, neglectful (temporarily) | `(LLM tail)` | Catelyn → Rickon | agot-catelyn-03 |
| 843 | 1 | Mother, proud and mentoring | `TUTORS` | Catelyn → Robb | agot-catelyn-03 |
| 844 | 1 | Son, stepping into authority | `(LLM tail)` | Robb → Catelyn | agot-catelyn-03 |
| 845 | 1 | Brother, acting protector | `SIBLING_OF` | Robb → Bran | agot-catelyn-03 |
| 846 | 1 | Brother, frustrated caretaker | `SIBLING_OF` | Robb → Rickon | agot-catelyn-03 |
| 847 | 1 | Wife, resentful of Ned's departure | `RESENTS` | Catelyn → Eddard Stark | agot-catelyn-03 |
| 848 | 1 | Loyal advisor, persistent | `(LLM tail)` | Maester Luwin → Catelyn / Robb | agot-catelyn-03 |
| 849 | 1 | Master-at-arms, mentor | `TUTORS` | Ser Rodrik Cassel → Robb | agot-catelyn-03 |
| 850 | 1 | Loyal retainer | `(LLM tail)` | Ser Rodrik Cassel → Catelyn | agot-catelyn-03 |
| 851 | 1 | Ward, declares loyalty | `(LLM tail)` | Theon Greyjoy → Eddard Stark / House Stark | agot-catelyn-03 |
| 852 | 1 | Suspicion and hostility toward | `(LLM tail)` | Catelyn → Jaime Lannister / the Lannisters | agot-catelyn-03 |
| 853 | 1 | Sister | `SIBLING_OF` | Catelyn → Lysa Arryn | agot-catelyn-03 |
| 854 | 1 | Protector, bonded | `BONDED_TO` | Bran's direwolf → Bran | agot-catelyn-03 |
| 855 | 1 | Savior | `(LLM tail)` | Bran's direwolf → Catelyn | agot-catelyn-03 |
| 856 | 1 | New captain of the guard | `(LLM tail)` | Hallis Mollen → Robb | agot-catelyn-03 |
| 857 | 1 | Childhood acquaintance / object of affection | `LOVES` | Catelyn Stark → Petyr Baelish | agot-catelyn-04 |
| 858 | 1 | Romantic rival (historical) | `(LLM tail)` | Petyr Baelish → Brandon Stark | agot-catelyn-04 |
| 859 | 1 | Married (in place of Brandon) | `(LLM tail)` | Catelyn Stark → Eddard Stark | agot-catelyn-04 |
| 860 | 1 | Claims friendship with | `COMPANION_OF` | Petyr Baelish → Lysa Arryn | agot-catelyn-04 |
| 861 | 1 | Named / nicknamed | `(LLM tail)` | Edmure Tully → Petyr Baelish | agot-catelyn-04 |
| 862 | 1 | Was ward of | `(LLM tail)` | Petyr Baelish → Hoster Tully (implied) | agot-catelyn-04 |
| 863 | 1 | Partially trusts | `(LLM tail)` | Catelyn Stark → Petyr Baelish | agot-catelyn-04 |
| 864 | 1 | Likely betrayed trust of | `(LLM tail)` | Captain Moreo → Catelyn Stark | agot-catelyn-04 |
| 865 | 1 | Lost dagger in bet to | `(LLM tail)` | Littlefinger → Tyrion Lannister | agot-catelyn-04 |
| 866 | 1 | Defeated in jousting | `(LLM tail)` | Loras Tyrell → Ser Jaime Lannister | agot-catelyn-04 |
| 867 | 1 | Consulted | `(LLM tail)` | Ser Rodrik Cassel → Ser Aron Santagar | agot-catelyn-04 |
| 868 | 1 | traveling companion / protected by | `COMPANION_OF` | Catelyn Stark → Ser Rodrik Cassel | agot-catelyn-05 |
| 869 | 1 | accuses / arrests | `(LLM tail)` | Catelyn Stark → Tyrion Lannister | agot-catelyn-05 |
| 870 | 1 | characterized as unreliable by | `(LLM tail)` | Lord Walder Frey → Hoster Tully | agot-catelyn-05 |
| 871 | 1 | traveling companion of | `COMPANION_OF` | Tyrion Lannister → Yoren | agot-catelyn-05 |
| 872 | 1 | exposes identity of | `(LLM tail)` | Marillion → Catelyn Stark | agot-catelyn-05 |
| 873 | 1 | innkeeper hosting | `(LLM tail)` | Masha Heddle → Catelyn Stark | agot-catelyn-05 |
| 874 | 1 | disloyal to (historically) | `(LLM tail)` | Houses Darry, Ryger, Mooton → House Tully | agot-catelyn-05 |
| 875 | 1 | Niece, warmly affectionate | `UNCLE_OF` | Catelyn → Brynden Tully | agot-catelyn-06 |
| 876 | 1 | Protective uncle, candid advisor | `UNCLE_OF` | Brynden Tully → Catelyn | agot-catelyn-06 |
| 877 | 1 | Growing alliance with | `ALLIES_WITH` | Tyrion Lannister → Bronn | agot-catelyn-06 |
| 878 | 1 | Captor (increasingly uncertain) | `CAPTURES` | Catelyn → Tyrion Lannister | agot-catelyn-06 |
| 879 | 1 | Sister, hostile despite initial warmth | `SIBLING_OF` | Lysa Arryn → Catelyn | agot-catelyn-06 |
| 880 | 1 | Fiercely protective, smothering | `(LLM tail)` | Lysa Arryn → Robert Arryn | agot-catelyn-06 |
| 881 | 1 | Resentful contempt toward | `RESENTS` | Catelyn → Jon Snow | agot-catelyn-06 |
| 882 | 1 | In love with | `LOVES` | Mya Stone → Mychel Redfort | agot-catelyn-06 |
| 883 | 1 | Pitying of | `(LLM tail)` | Catelyn → Mya Stone | agot-catelyn-06 |
| 884 | 1 | Deferential to / serves | `(LLM tail)` | Lord Nestor Royce → Lysa Arryn | agot-catelyn-06 |
| 885 | 1 | Loyal but frustrated servant of | `(LLM tail)` | Ser Donnel Waynwood → Lysa Arryn | agot-catelyn-06 |
| 886 | 1 | Protective but critical of | `(LLM tail)` | Brynden Tully → Lysa Arryn | agot-catelyn-06 |
| 887 | 1 | Sardonic about his family | `(LLM tail)` | Tyrion Lannister → Jaime, Cersei, Tywin Lannister | agot-catelyn-06 |
| 888 | 1 | Dependent on / clings to | `(LLM tail)` | Robert Arryn → Lysa Arryn | agot-catelyn-06 |
| 889 | 1 | Sister (strained) | `SIBLING_OF` | Catelyn → Lysa | agot-catelyn-07 |
| 890 | 1 | Niece-uncle (trusting alliance) | `UNCLE_OF` | Catelyn → Brynden Tully | agot-catelyn-07 |
| 891 | 1 | Nephew-sister (ruptured) | `NEPHEW_OF` | Brynden Tully → Lysa | agot-catelyn-07 |
| 892 | 1 | Relies on as advisor | `(LLM tail)` | Catelyn → Ser Rodrik | agot-catelyn-07 |
| 893 | 1 | Mother (overprotective) | `(LLM tail)` | Lysa → Robert Arryn | agot-catelyn-07 |
| 894 | 1 | Surrounded by suitors | `(LLM tail)` | Lysa → Lord Hunter, Ser Lyn Corbray, Ser Morton Waynwood | agot-catelyn-07 |
| 895 | 1 | Champion-client | `(LLM tail)` | Tyrion → Bronn | agot-catelyn-07 |
| 896 | 1 | Champion/loyal servant | `(LLM tail)` | Ser Vardis → Lysa Arryn | agot-catelyn-07 |
| 897 | 1 | Former betrothed (memory) | `BETROTHED_TO` | Catelyn → Brandon Stark | agot-catelyn-07 |
| 898 | 1 | Unrequited love (memory) | `LOVES` | Petyr Baelish → Catelyn | agot-catelyn-07 |
| 899 | 1 | Nursed/cared for (past) | `(LLM tail)` | Lysa → Petyr Baelish | agot-catelyn-07 |
| 900 | 1 | Squired for Brandon / rejected by Petyr (past) | `(LLM tail)` | Edmure Tully → Brandon Stark / Petyr Baelish | agot-catelyn-07 |
| 901 | 1 | Father (protective, past) | `(LLM tail)` | Lord Hoster Tully → Catelyn / Petyr | agot-catelyn-07 |
| 902 | 1 | Captor (nominal) | `CAPTURES` | Catelyn → Tyrion | agot-catelyn-07 |
| 903 | 1 | Sister of (hostile) | `SIBLING_OF` | Catelyn → Lysa Arryn | agot-catelyn-08 |
| 904 | 1 | Sister-in-law of | `IN_LAW_OF` | Catelyn → Edmure Tully | agot-catelyn-08 |
| 905 | 1 | Accepts | `(LLM tail)` | Grey Wind → Catelyn | agot-catelyn-08 |
| 906 | 1 | Sons of | `(LLM tail)` | Ser Wylis/Wendel Manderly → Lord Wyman Manderly | agot-catelyn-08 |
| 907 | 1 | Ward of / companion to | `WARD_OF` | Theon Greyjoy → Robb | agot-catelyn-08 |
| 908 | 1 | Unsettled by | `(LLM tail)` | Catelyn → Roose Bolton | agot-catelyn-08 |
| 909 | 1 | Fears (respects) | `FEARS` | Robb → Roose Bolton | agot-catelyn-08 |
| 910 | 1 | Advised by | `(LLM tail)` | Robb → Catelyn | agot-catelyn-08 |
| 911 | 1 | Sees Ned in | `(LLM tail)` | Catelyn → Robb | agot-catelyn-08 |
| 912 | 1 | Sees Tully in | `(LLM tail)` | Catelyn → Robb | agot-catelyn-08 |
| 913 | 1 | Named castellan by | `(LLM tail)` | Ser Rodrik Cassel → Catelyn | agot-catelyn-08 |
| 914 | 1 | niece to | `UNCLE_OF` | Catelyn → Ser Brynden Tully | agot-catelyn-09 |
| 915 | 1 | serves as messenger for | `SERVES` | Theon Greyjoy → Ser Brynden / Robb | agot-catelyn-09 |
| 916 | 1 | bannerman to (unreliable) | `(LLM tail)` | Walder Frey → Hoster Tully | agot-catelyn-09 |
| 917 | 1 | friendlier with than expected | `COMPANION_OF` | Walder Frey → House Lannister | agot-catelyn-09 |
| 918 | 1 | heir to, waits on | `(LLM tail)` | Ser Stevron Frey → Walder Frey | agot-catelyn-09 |
| 919 | 1 | commands eastern foot force for | `COMMANDS` | Roose Bolton → Robb | agot-catelyn-09 |
| 920 | 1 | Mother of / fiercely protective | `PARENT_OF` | Catelyn → Robb | agot-catelyn-10 |
| 921 | 1 | Son of / obedient but growing independent | `PARENT_OF` | Robb → Catelyn | agot-catelyn-10 |
| 922 | 1 | Follows teachings of | `(LLM tail)` | Robb → Ned Stark | agot-catelyn-10 |
| 923 | 1 | Daughter of / deep affection | `PARENT_OF` | Catelyn → Hoster Tully | agot-catelyn-10 |
| 924 | 1 | Bonded to / shadows | `BONDED_TO` | Grey Wind → Robb | agot-catelyn-10 |
| 925 | 1 | Companion of / eager subordinate | `COMPANION_OF` | Theon Greyjoy → Robb | agot-catelyn-10 |
| 926 | 1 | Uncle and military advisor to | `UNCLE_OF` | Ser Brynden Tully → Catelyn / Robb | agot-catelyn-10 |
| 927 | 1 | Captured enemy of | `(LLM tail)` | Jaime Lannister → Robb / Catelyn | agot-catelyn-10 |
| 928 | 1 | Wants revenge on | `(LLM tail)` | Lord Karstark → Jaime Lannister | agot-catelyn-10 |
| 929 | 1 | Daughter and heir of | `(LLM tail)` | Dacey Mormont → Maege Mormont | agot-catelyn-10 |
| 930 | 1 | Ally who joined march | `ALLIES_WITH` | Lord Jason Mallister → Robb | agot-catelyn-10 |
| 931 | 1 | Cold hostility toward | `(LLM tail)` | Catelyn → Jaime Lannister | agot-catelyn-10 |
| 932 | 1 | Respects as adversary | `RESPECTS` | Robb → Jaime Lannister | agot-catelyn-10 |
| 933 | 1 | companion of / bonded to | `COMPANION_OF` | Robb → Grey Wind | agot-catelyn-11 |
| 934 | 1 | echoes / resembles | `(LLM tail)` | Robb → Eddard Stark | agot-catelyn-11 |
| 935 | 1 | estranged from / quarrels with | `(LLM tail)` | Hoster → Brynden Tully | agot-catelyn-11 |
| 936 | 1 | wants to see | `(LLM tail)` | Hoster → Lysa Arryn | agot-catelyn-11 |
| 937 | 1 | subordinate to / acting lord for | `SERVES` | Edmure → Hoster Tully | agot-catelyn-11 |
| 938 | 1 | represents | `(LLM tail)` | Stevron Frey → Walder Frey | agot-catelyn-11 |
| 939 | 1 | bereaved father of | `(LLM tail)` | Rickard Karstark → Torrhen Karstark, Eddard Karstark | agot-catelyn-11 |
| 940 | 1 | advocating for return of | `(LLM tail)` | Catelyn → Sansa Stark, Arya Stark | agot-catelyn-11 |
| 941 | 1 | fought duel with | `(LLM tail)` | Petyr Baelish → Brandon Stark | agot-catelyn-11 |
| 942 | 1 | Abuses/controls | `(LLM tail)` | Viserys → Daenerys | agot-daenerys-01 |
| 943 | 1 | Sells/trades | `(LLM tail)` | Viserys → Daenerys | agot-daenerys-01 |
| 944 | 1 | Hosts/patronizes | `(LLM tail)` | Illyrio → Viserys & Daenerys | agot-daenerys-01 |
| 945 | 1 | Flatters/manipulates | `(LLM tail)` | Illyrio → Viserys | agot-daenerys-01 |
| 946 | 1 | Arranges marriage between | `(LLM tail)` | Illyrio → Daenerys and Khal Drogo | agot-daenerys-01 |
| 947 | 1 | Mourns/longs for | `MOURNS` | Daenerys → The house with the red door | agot-daenerys-01 |
| 948 | 1 | Claims kingship over | `(LLM tail)` | Viserys → Westeros / Seven Kingdoms | agot-daenerys-01 |
| 949 | 1 | Exiled from | `(LLM tail)` | Ser Jorah Mormont → Westeros | agot-daenerys-01 |
| 950 | 1 | Buy peace from | `(LLM tail)` | Magisters of Pentos → Dothraki khals | agot-daenerys-01 |
| 951 | 1 | Claims support from | `(LLM tail)` | Viserys → Houses Tyrell, Redwyne, Darry, Greyjoy, and Dorne | agot-daenerys-01 |
| 952 | 1 | Controls/abuses | `COMMANDS` | Viserys → Dany | agot-daenerys-02 |
| 953 | 1 | Sold/traded | `(LLM tail)` | Viserys → Dany to Drogo | agot-daenerys-02 |
| 954 | 1 | Facilitated marriage of | `(LLM tail)` | Illyrio → Dany and Drogo | agot-daenerys-02 |
| 955 | 1 | Sworn sword to | `SWORN_TO` | Ser Jorah → Viserys | agot-daenerys-02 |
| 956 | 1 | Protective/respectful toward | `RESPECTS` | Ser Jorah → Dany | agot-daenerys-02 |
| 957 | 1 | Husband to | `(LLM tail)` | Drogo → Dany | agot-daenerys-02 |
| 958 | 1 | Mistress to | `(LLM tail)` | Dany → Irri, Jhiqui, Doreah | agot-daenerys-02 |
| 959 | 1 | Resents position below | `RESENTS` | Viserys → Dany | agot-daenerys-02 |
| 960 | 1 | Gentle/tender toward | `(LLM tail)` | Drogo → Dany | agot-daenerys-02 |
| 961 | 1 | Defies and asserts authority over | `OPPOSES` | Daenerys → Viserys | agot-daenerys-03 |
| 962 | 1 | Growing bond / love for | `LOVES` | Daenerys → The silver (horse) | agot-daenerys-03 |
| 963 | 1 | Evolving intimacy with | `(LLM tail)` | Daenerys → Khal Drogo | agot-daenerys-03 |
| 964 | 1 | Serves and advises | `SERVES` | Ser Jorah → Daenerys | agot-daenerys-03 |
| 965 | 1 | Tries to command | `COMMANDS` | Viserys → Ser Jorah | agot-daenerys-03 |
| 966 | 1 | Serves and teaches | `SERVES` | Doreah → Daenerys | agot-daenerys-03 |
| 967 | 1 | Ignored and used | `(LLM tail)` | Khal Drogo → Daenerys (early) | agot-daenerys-03 |
| 968 | 1 | Commanded by / assigned | `COMMANDS` | Khal Drogo → Irri | agot-daenerys-03 |
| 969 | 1 | Gave gifts to | `GIFTED_TO` | Illyrio Mopatis → Daenerys | agot-daenerys-03 |
| 970 | 1 | Offered hospitality to | `(LLM tail)` | Illyrio Mopatis → Viserys | agot-daenerys-03 |
| 971 | 1 | Enslaved by (in past) | `(LLM tail)` | Irri and Jhiqui → Khal Drogo | agot-daenerys-03 |
| 972 | 1 | Purchased from | `(LLM tail)` | Doreah → A pleasure house in Lys | agot-daenerys-03 |
| 973 | 1 | Growing independence from | `(LLM tail)` | Daenerys → Viserys | agot-daenerys-04 |
| 974 | 1 | Mystical connection to | `(LLM tail)` | Daenerys → Dragon eggs | agot-daenerys-04 |
| 975 | 1 | Threatens/intimidates | `OPPOSES` | Viserys → Daenerys | agot-daenerys-04 |
| 976 | 1 | Bound to | `(LLM tail)` | Cohollo → Khal Drogo | agot-daenerys-04 |
| 977 | 1 | wife/khaleesi of | `(LLM tail)` | Daenerys → Khal Drogo | agot-daenerys-05 |
| 978 | 1 | demands payment from | `(LLM tail)` | Viserys → Khal Drogo | agot-daenerys-05 |
| 979 | 1 | guards/threatens | `GUARDS` | Ser Jorah Mormont → Viserys | agot-daenerys-05 |
| 980 | 1 | is teaching Common Tongue to | `(LLM tail)` | Daenerys → Khal Drogo | agot-daenerys-05 |
| 981 | 1 | taught Dothraki phrases to | `(LLM tail)` | Jhiqui → Daenerys | agot-daenerys-05 |
| 982 | 1 | serves/alerts | `SERVES` | Doreah → Daenerys | agot-daenerys-05 |
| 983 | 1 | named child after | `(LLM tail)` | Daenerys → Rhaegar Targaryen | agot-daenerys-05 |
| 984 | 1 | raised/told family history to | `(LLM tail)` | Viserys → Daenerys | agot-daenerys-05 |
| 985 | 1 | prophesies for | `(LLM tail)` | Dosh khaleen → Daenerys/Rhaego | agot-daenerys-05 |
| 986 | 1 | attempted theft from | `(LLM tail)` | Viserys → Daenerys | agot-daenerys-05 |
| 987 | 1 | Wife / subordinate in public, persuader in private | `SERVES` | Daenerys → Khal Drogo | agot-daenerys-06 |
| 988 | 1 | Husband / authority figure, devoted | `(LLM tail)` | Khal Drogo → Daenerys | agot-daenerys-06 |
| 989 | 1 | Protector and advisor | `(LLM tail)` | Ser Jorah → Daenerys | agot-daenerys-06 |
| 990 | 1 | Devoted handmaid / protector | `(LLM tail)` | Doreah → Daenerys | agot-daenerys-06 |
| 991 | 1 | Handmaid, affectionate | `LOVES` | Irri → Daenerys | agot-daenerys-06 |
| 992 | 1 | Loyal khas warrior | `(LLM tail)` | Jhogo → Daenerys | agot-daenerys-06 |
| 993 | 1 | Rewards loyalty | `(LLM tail)` | Khal Drogo → Jhogo, Ser Jorah | agot-daenerys-06 |
| 994 | 1 | Grief / complicated memory | `MOURNS` | Daenerys → Viserys | agot-daenerys-06 |
| 995 | 1 | Hostile / threatens | `(LLM tail)` | Robert Baratheon → Daenerys | agot-daenerys-06 |
| 996 | 1 | Informant / ally | `ALLIES_WITH` | Illyrio Mopatis → Daenerys (via Ser Jorah) | agot-daenerys-06 |
| 997 | 1 | Respectful / protective of guest peace | `RESPECTS` | Byan Votyris → Daenerys | agot-daenerys-06 |
| 998 | 1 | Attempted assassin | `(LLM tail)` | Wine merchant → Daenerys | agot-daenerys-06 |
| 999 | 1 | Punisher | `(LLM tail)` | Daenerys → Wine merchant | agot-daenerys-06 |
| 1000 | 1 | wife of / devoted to | `(LLM tail)` | Dany → Drogo | agot-daenerys-07 |
| 1001 | 1 | husband of / supportive of | `(LLM tail)` | Drogo → Dany | agot-daenerys-07 |
| 1002 | 1 | advises / respects | `ADVISES` | Ser Jorah → Dany | agot-daenerys-07 |
| 1003 | 1 | corresponds with | `(LLM tail)` | Ser Jorah → Illyrio | agot-daenerys-07 |
| 1004 | 1 | hostile toward / mocking | `OPPOSES` | Qotho → Dany | agot-daenerys-07 |
| 1005 | 1 | protects / claims | `PROTECTS` | Dany → Mirri Maz Duur | agot-daenerys-07 |
| 1006 | 1 | healer of / obedient to | `(LLM tail)` | Mirri Maz Duur → Drogo | agot-daenerys-07 |
| 1007 | 1 | resentful of | `RESENTS` | Mago → Dany | agot-daenerys-07 |
| 1008 | 1 | dismissive of / dominant over | `DISTRUSTS` | Drogo → Qotho, Mago | agot-daenerys-07 |
| 1009 | 1 | reminded of Viserys by | `(LLM tail)` | Dany → Qotho | agot-daenerys-07 |
| 1010 | 1 | claims as slaves | `(LLM tail)` | Dany → Lhazareen women | agot-daenerys-07 |
| 1011 | 1 | echoes Dothraki customs | `(LLM tail)` | Irri → Dany | agot-daenerys-07 |
| 1012 | 1 | wife / desperate caretaker of | `(LLM tail)` | Dany → Drogo | agot-daenerys-08 |
| 1013 | 1 | commands (with difficulty) | `COMMANDS` | Dany → Qotho | agot-daenerys-08 |
| 1014 | 1 | refuses counsel of | `ADVISES` | Dany → Ser Jorah | agot-daenerys-08 |
| 1015 | 1 | rescued / protects | `RESCUES` | Dany → Eroeh | agot-daenerys-08 |
| 1016 | 1 | relies on for ritual | `(LLM tail)` | Dany → Mirri Maz Duur | agot-daenerys-08 |
| 1017 | 1 | hostile / threatening toward | `(LLM tail)` | Qotho → Dany | agot-daenerys-08 |
| 1018 | 1 | assists in killing | `(LLM tail)` | Jhogo → Haggo | agot-daenerys-08 |
| 1019 | 1 | threatens / hostile toward | `OPPOSES` | Cohollo → Dany | agot-daenerys-08 |
| 1020 | 1 | bound life to | `(LLM tail)` | Cohollo → Drogo | agot-daenerys-08 |
| 1021 | 1 | had been kind to | `(LLM tail)` | Cohollo → Dany | agot-daenerys-08 |
| 1022 | 1 | slave of | `(LLM tail)` | Mirri Maz Duur → Dany | agot-daenerys-08 |
| 1023 | 1 | performs blood ritual for | `(LLM tail)` | Mirri Maz Duur → Drogo | agot-daenerys-08 |
| 1024 | 1 | share one life with | `(LLM tail)` | Bloodriders (Qotho, Haggo, Cohollo) → Drogo | agot-daenerys-08 |
| 1025 | 1 | call him | `(LLM tail)` | Dothraki calling Ser Jorah → "The Andal" | agot-daenerys-08 |
| 1026 | 1 | father of (unborn) | `PARENT_OF` | Drogo → Rhaego | agot-daenerys-08 |
| 1027 | 1 | wife/lover of (ending) | `LOVER_OF` | Daenerys → Khal Drogo | agot-daenerys-09 |
| 1028 | 1 | mother of (bereaved) | `PARENT_OF` | Daenerys → Rhaego | agot-daenerys-09 |
| 1029 | 1 | protector/advisor of | `(LLM tail)` | Ser Jorah Mormont → Daenerys | agot-daenerys-09 |
| 1030 | 1 | holds responsible | `(LLM tail)` | Daenerys → Ser Jorah Mormont | agot-daenerys-09 |
| 1031 | 1 | connected to (mystically) | `(LLM tail)` | Daenerys → Dragon eggs | agot-daenerys-09 |
| 1032 | 1 | Claims queenship / heir to | `(LLM tail)` | Daenerys → Viserys Targaryen | agot-daenerys-10 |
| 1033 | 1 | Commands / sovereign | `COMMANDS` | Daenerys → Ser Jorah Mormont | agot-daenerys-10 |
| 1034 | 1 | Sworn to / loves | `SWORN_TO` | Ser Jorah Mormont → Daenerys | agot-daenerys-10 |
| 1035 | 1 | Condemns / sacrifices | `(LLM tail)` | Daenerys → Mirri Maz Duur | agot-daenerys-10 |
| 1036 | 1 | Conditional loyalty to | `(LLM tail)` | Rakharo → Daenerys | agot-daenerys-10 |
| 1037 | 1 | References past love for | `LOVES` | Ser Jorah → His lady wife | agot-daenerys-10 |
| 1038 | 1 | Thinks of / compares self to | `(LLM tail)` | Daenerys → Aegon (the Conqueror) | agot-daenerys-10 |
| 1039 | 1 | Deep old friendship with, now subject to | `COMPANION_OF` | Ned Stark → Robert Baratheon | agot-eddard-01 |
| 1040 | 1 | Enduring love/obsession for | `LOVES` | Robert Baratheon → Lyanna Stark | agot-eddard-01 |
| 1041 | 1 | Grief and love for | `MOURNS` | Ned Stark → Lyanna Stark | agot-eddard-01 |
| 1042 | 1 | Undying hatred for | `(LLM tail)` | Robert Baratheon → Rhaegar Targaryen | agot-eddard-01 |
| 1043 | 1 | Distrust and contempt for | `DISTRUSTS` | Ned Stark → Tywin Lannister | agot-eddard-01 |
| 1044 | 1 | Cold/hostile marriage with | `(LLM tail)` | Robert Baratheon → Cersei Lannister | agot-eddard-01 |
| 1045 | 1 | Protective of / controlling toward | `PROTECTS` | Jaime Lannister → Cersei Lannister | agot-eddard-01 |
| 1046 | 1 | Grief and admiration for | `MOURNS` | Robert Baratheon → Jon Arryn | agot-eddard-01 |
| 1047 | 1 | Grief and respect for | `MOURNS` | Ned Stark → Jon Arryn | agot-eddard-01 |
| 1048 | 1 | Frustration/contempt for | `(LLM tail)` | Robert Baratheon → Lysa Arryn | agot-eddard-01 |
| 1049 | 1 | Plans to join houses with | `(LLM tail)` | Robert Baratheon → Ned Stark | agot-eddard-01 |
| 1050 | 1 | Took as hostage/ward | `(LLM tail)` | Ned Stark → Theon Greyjoy | agot-eddard-01 |
| 1051 | 1 | Haunted by promise to | `(LLM tail)` | Ned Stark → Lyanna Stark | agot-eddard-01 |
| 1052 | 1 | Present at death of | `(LLM tail)` | Howland Reed → Lyanna Stark | agot-eddard-01 |
| 1053 | 1 | Old friend / king to Hand | `(LLM tail)` | Robert → Ned | agot-eddard-02 |
| 1054 | 1 | Frustrated spouse | `(LLM tail)` | Robert → Cersei | agot-eddard-02 |
| 1055 | 1 | Obsessive hatred | `(LLM tail)` | Robert → Targaryens (all) | agot-eddard-02 |
| 1056 | 1 | Undying love / grief | `MOURNS` | Robert → Lyanna Stark | agot-eddard-02 |
| 1057 | 1 | Guilt and concealment | `(LLM tail)` | Ned → Wylla / "his bastard" | agot-eddard-02 |
| 1058 | 1 | Moral opposition | `(LLM tail)` | Ned → Tywin Lannister | agot-eddard-02 |
| 1059 | 1 | Deep distrust | `(LLM tail)` | Ned → Jaime Lannister | agot-eddard-02 |
| 1060 | 1 | Trust / dismissal | `(LLM tail)` | Robert → Jaime Lannister | agot-eddard-02 |
| 1061 | 1 | Respect / inadequacy | `RESPECTS` | Ned → Jon Arryn | agot-eddard-02 |
| 1062 | 1 | Respect tinged with regret | `RESPECTS` | Robert → Jon Arryn | agot-eddard-02 |
| 1063 | 1 | Lord / failed justice | `(LLM tail)` | Ned → Jorah Mormont | agot-eddard-02 |
| 1064 | 1 | Spymaster serving | `(LLM tail)` | Varys → Robert | agot-eddard-02 |
| 1065 | 1 | Spy serving | `(LLM tail)` | Jorah Mormont → Varys | agot-eddard-02 |
| 1066 | 1 | Haunted by promise | `(LLM tail)` | Ned → Lyanna Stark | agot-eddard-02 |
| 1067 | 1 | Dismissed concern from | `(LLM tail)` | Robert → Ned | agot-eddard-02 |
| 1068 | 1 | Bannerman lord over | `(LLM tail)` | Ned → House Mormont | agot-eddard-02 |
| 1069 | 1 | Old friend, growing tension | `(LLM tail)` | Eddard Stark → Robert Baratheon | agot-eddard-03 |
| 1070 | 1 | Antagonism | `(LLM tail)` | Eddard Stark → Cersei Lannister | agot-eddard-03 |
| 1071 | 1 | King, conflicted | `(LLM tail)` | Robert Baratheon → Eddard Stark | agot-eddard-03 |
| 1072 | 1 | Past love | `LOVES` | Robert Baratheon → Ned's sister (Lyanna) | agot-eddard-03 |
| 1073 | 1 | Hostility | `(LLM tail)` | Arya Stark → Joffrey Baratheon | agot-eddard-03 |
| 1074 | 1 | Rage, betrayal | `(LLM tail)` | Arya Stark → Sansa Stark | agot-eddard-03 |
| 1075 | 1 | Evasion/fear | `FEARS` | Sansa Stark → Arya Stark / Joffrey Baratheon | agot-eddard-03 |
| 1076 | 1 | Lies/accuses | `(LLM tail)` | Joffrey Baratheon → Arya Stark | agot-eddard-03 |
| 1077 | 1 | Irritation with brother | `SIBLING_OF` | Robert Baratheon → Renly Baratheon | agot-eddard-03 |
| 1078 | 1 | Compassion, grief | `MOURNS` | Eddard Stark → Lady | agot-eddard-03 |
| 1079 | 1 | Reluctant host | `(LLM tail)` | Ser Raymun Darry → Robert Baratheon | agot-eddard-03 |
| 1080 | 1 | Reluctant servant | `(LLM tail)` | Barristan Selmy → Cersei Lannister | agot-eddard-03 |
| 1081 | 1 | distrusts / dislikes | `DISTRUSTS` | Ned → Varys | agot-eddard-04 |
| 1082 | 1 | distrusts / hostile toward | `DISTRUSTS` | Ned → Littlefinger | agot-eddard-04 |
| 1083 | 1 | reluctant political ally | `ALLIES_WITH` | Ned → Littlefinger | agot-eddard-04 |
| 1084 | 1 | husband, protector | `(LLM tail)` | Ned → Catelyn | agot-eddard-04 |
| 1085 | 1 | trusts as near-brother | `TRUSTS` | Catelyn → Littlefinger | agot-eddard-04 |
| 1086 | 1 | unrequited attachment to | `(LLM tail)` | Littlefinger → Catelyn | agot-eddard-04 |
| 1087 | 1 | former rival/defeated by | `(LLM tail)` | Littlefinger → Brandon Stark | agot-eddard-04 |
| 1088 | 1 | mocks / irreverent toward | `OPPOSES` | Renly → Robert Baratheon | agot-eddard-04 |
| 1089 | 1 | deferential to | `(LLM tail)` | Varys → Ned | agot-eddard-04 |
| 1090 | 1 | deferential, passive | `(LLM tail)` | Pycelle → Ned | agot-eddard-04 |
| 1091 | 1 | absent, neglectful ruler | `(LLM tail)` | Robert → The realm | agot-eddard-04 |
| 1092 | 1 | claims leverage over | `(LLM tail)` | Littlefinger → Varys | agot-eddard-04 |
| 1093 | 1 | orders military preparation against | `(LLM tail)` | Ned → House Lannister | agot-eddard-04 |
| 1094 | 1 | watches cautiously | `(LLM tail)` | Ned → Theon Greyjoy | agot-eddard-04 |
| 1095 | 1 | loyal escort to | `(LLM tail)` | Ser Rodrik → Catelyn | agot-eddard-04 |
| 1096 | 1 | Deflects suspicion toward | `(LLM tail)` | Pycelle → Varys | agot-eddard-05 |
| 1097 | 1 | Claims mentorship of | `TUTORS` | Pycelle → Maester Colemon | agot-eddard-05 |
| 1098 | 1 | Overruled | `(LLM tail)` | Pycelle → Maester Colemon | agot-eddard-05 |
| 1099 | 1 | Ally (claimed) of | `ALLIES_WITH` | Littlefinger → Catelyn Stark | agot-eddard-05 |
| 1100 | 1 | Took to godswood | `(LLM tail)` | Ned → Arya, Sansa | agot-eddard-05 |
| 1101 | 1 | presides over council in absence of | `(LLM tail)` | Ned → Robert | agot-eddard-06 |
| 1102 | 1 | commands/directs finances of | `COMMANDS` | Ned → Littlefinger | agot-eddard-06 |
| 1103 | 1 | investigates death of | `INVESTIGATES` | Ned → Jon Arryn | agot-eddard-06 |
| 1104 | 1 | rode with / closely associated with | `(LLM tail)` | Jon Arryn → Stannis Baratheon | agot-eddard-06 |
| 1105 | 1 | visited and questioned | `(LLM tail)` | Jon Arryn → Gendry | agot-eddard-06 |
| 1106 | 1 | accompanied but remained silent with | `(LLM tail)` | Stannis → Gendry | agot-eddard-06 |
| 1107 | 1 | is captain of guard for | `(LLM tail)` | Ned → Jory Cassel | agot-eddard-06 |
| 1108 | 1 | assigns command to | `COMMANDS` | Ned → Alyn | agot-eddard-06 |
| 1109 | 1 | master of apprentice | `(LLM tail)` | Tobho Mott → Gendry | agot-eddard-06 |
| 1110 | 1 | is bastard of (inferred) | `(LLM tail)` | Gendry → Robert Baratheon | agot-eddard-06 |
| 1111 | 1 | paid apprentice fee for | `(LLM tail)` | Unknown lord → Gendry | agot-eddard-06 |
| 1112 | 1 | shows portrait of | `(LLM tail)` | Renly → Margaery Tyrell | agot-eddard-06 |
| 1113 | 1 | compared appearance to | `(LLM tail)` | Renly → young Robert | agot-eddard-06 |
| 1114 | 1 | yearns for home with | `(LLM tail)` | Ned → Robb Stark, Jon Snow | agot-eddard-06 |
| 1115 | 1 | wary of / fretted by | `DISTRUSTS` | Ned → Varys | agot-eddard-06 |
| 1116 | 1 | finds Gendry has look of a warrior, offers future service to | `(LLM tail)` | Ned → Gendry | agot-eddard-06 |
| 1117 | 1 | deep old friendship with | `COMPANION_OF` | Eddard Stark → Robert Baratheon | agot-eddard-07 |
| 1118 | 1 | loathes marriage to | `HATES` | Robert Baratheon → Cersei Lannister | agot-eddard-07 |
| 1119 | 1 | still mourns/loves | `MOURNS` | Robert Baratheon → Lyanna Stark | agot-eddard-07 |
| 1120 | 1 | despairs of | `(LLM tail)` | Robert Baratheon → Joffrey Baratheon | agot-eddard-07 |
| 1121 | 1 | protective of / uneasy about training | `PROTECTS` | Eddard Stark → Arya Stark | agot-eddard-07 |
| 1122 | 1 | devoted student of | `(LLM tail)` | Arya Stark → Syrio Forel | agot-eddard-07 |
| 1123 | 1 | deep enmity with | `(LLM tail)` | Sandor Clegane → Gregor Clegane | agot-eddard-07 |
| 1124 | 1 | violent fury toward | `(LLM tail)` | Ser Gregor Clegane → Ser Loras Tyrell | agot-eddard-07 |
| 1125 | 1 | wagers against/banter with | `(LLM tail)` | Littlefinger → Lord Renly | agot-eddard-07 |
| 1126 | 1 | secret counselor to | `ADVISES` | Varys → Eddard Stark | agot-eddard-07 |
| 1127 | 1 | respects loyalty of | `RESPECTS` | Varys → Ser Barristan Selmy | agot-eddard-07 |
| 1128 | 1 | respected by / loyal to | `RESPECTS` | Ser Barristan Selmy → Robert Baratheon | agot-eddard-07 |
| 1129 | 1 | admits Joffrey lied about | `(LLM tail)` | Robert Baratheon → Sansa's direwolf incident | agot-eddard-07 |
| 1130 | 1 | bitter guilt about | `RESENTS` | Ned → Ser Hugh's death | agot-eddard-07 |
| 1131 | 1 | concedes victory to / gratitude | `(LLM tail)` | Loras Tyrell → Sandor Clegane | agot-eddard-07 |
| 1132 | 1 | sisterly civility toward | `(LLM tail)` | Sansa Stark → Arya Stark | agot-eddard-07 |
| 1133 | 1 | Defies / moral opposition | `OPPOSES` | Ned → Robert | agot-eddard-08 |
| 1134 | 1 | Mourns lost friendship | `MOURNS` | Ned → Robert | agot-eddard-08 |
| 1135 | 1 | Hates (enduringly) | `HATES` | Robert → Rhaegar Targaryen | agot-eddard-08 |
| 1136 | 1 | Serves / manipulates | `SERVES` | Varys → Robert | agot-eddard-08 |
| 1137 | 1 | Defers to pragmatism over | `(LLM tail)` | Renly → Jon Arryn's memory | agot-eddard-08 |
| 1138 | 1 | Sides with / respects | `RESPECTS` | Ser Barristan → Ned | agot-eddard-08 |
| 1139 | 1 | Previously showed mercy to | `(LLM tail)` | Robert → Ser Barristan | agot-eddard-08 |
| 1140 | 1 | Urged killing of | `(LLM tail)` | Roose Bolton → Ser Barristan | agot-eddard-08 |
| 1141 | 1 | Mocks / warns | `OPPOSES` | Littlefinger → Ned | agot-eddard-08 |
| 1142 | 1 | Claims to protect (ambiguously) | `(LLM tail)` | Littlefinger → Daenerys | agot-eddard-08 |
| 1143 | 1 | Avoids marrying | `(LLM tail)` | Littlefinger → Lady Tanda's daughter | agot-eddard-08 |
| 1144 | 1 | Suspects shared knowledge with | `(LLM tail)` | Ned → Stannis Baratheon | agot-eddard-08 |
| 1145 | 1 | Worries about consequences for | `(LLM tail)` | Ned → Catelyn Stark | agot-eddard-08 |
| 1146 | 1 | Sent raven to | `(LLM tail)` | Pycelle → Stannis Baratheon | agot-eddard-08 |
| 1147 | 1 | Investigates murder of | `INVESTIGATES` | Ned → Jon Arryn | agot-eddard-08 |
| 1148 | 1 | Monitors | `(LLM tail)` | Littlefinger → Jory Cassel | agot-eddard-08 |
| 1149 | 1 | former Hand to the king of | `(LLM tail)` | Eddard Stark → Robert Baratheon | agot-eddard-09 |
| 1150 | 1 | guide/informant to | `(LLM tail)` | Littlefinger → Eddard Stark | agot-eddard-09 |
| 1151 | 1 | loyal guard to | `(LLM tail)` | Jory Cassel → Eddard Stark | agot-eddard-09 |
| 1152 | 1 | hostile confrontation with | `(LLM tail)` | Jaime Lannister → Eddard Stark | agot-eddard-09 |
| 1153 | 1 | protective brother to | `SIBLING_OF` | Jaime Lannister → Tyrion Lannister | agot-eddard-09 |
| 1154 | 1 | clear-eyed about | `(LLM tail)` | Lyanna Stark → Robert Baratheon | agot-eddard-09 |
| 1155 | 1 | paternal feeling toward | `(LLM tail)` | Eddard Stark → Jon Snow | agot-eddard-09 |
| 1156 | 1 | grief/guilt about | `MOURNS` | Eddard Stark → Lyanna Stark | agot-eddard-09 |
| 1157 | 1 | offended by | `(LLM tail)` | Stannis Baratheon → Robert Baratheon | agot-eddard-09 |
| 1158 | 1 | allegedly murdered children of | `KILLS` | Cersei Lannister → Robert Baratheon | agot-eddard-09 |
| 1159 | 1 | familiar with | `(LLM tail)` | Littlefinger → Chataya | agot-eddard-09 |
| 1160 | 1 | treats | `(LLM tail)` | Grand Maester Pycelle → Eddard Stark | agot-eddard-09 |
| 1161 | 1 | Subordinate/Hand to | `SERVES` | Eddard Stark → Robert Baratheon | agot-eddard-10 |
| 1162 | 1 | Deep old friendship with tension | `COMPANION_OF` | Eddard Stark → Robert Baratheon | agot-eddard-10 |
| 1163 | 1 | Protects/shields | `PROTECTS` | Eddard Stark → Catelyn Stark | agot-eddard-10 |
| 1164 | 1 | Domestic violence/toxic marriage | `(LLM tail)` | Robert Baratheon → Cersei Lannister | agot-eddard-10 |
| 1165 | 1 | Obsessive grief/loss | `MOURNS` | Robert Baratheon → Lyanna Stark | agot-eddard-10 |
| 1166 | 1 | Grief/loyalty for | `MOURNS` | Eddard Stark → Jory Cassel | agot-eddard-10 |
| 1167 | 1 | Respect/bonds with | `RESPECTS` | Eddard Stark → Tower of Joy companions | agot-eddard-10 |
| 1168 | 1 | Specifically remembers | `(LLM tail)` | Eddard Stark → Howland Reed | agot-eddard-10 |
| 1169 | 1 | Bound by promise to | `(LLM tail)` | Eddard Stark → Lyanna Stark | agot-eddard-10 |
| 1170 | 1 | Fought against | `(LLM tail)` | Ned's companions (7) → Three Kingsguard | agot-eddard-10 |
| 1171 | 1 | Brother of the Kingsguard with | `SIBLING_OF` | Ser Arthur Dayne → Ser Gerold Hightower, Ser Oswell Whent | agot-eddard-10 |
| 1172 | 1 | Guarded/protected | `(LLM tail)` | Kingsguard (three) → Lyanna Stark | agot-eddard-10 |
| 1173 | 1 | Father of (unacknowledged bastard) | `PARENT_OF` | Robert Baratheon → Barra | agot-eddard-10 |
| 1174 | 1 | Watches Cersei's reaction to | `(LLM tail)` | Ned → Barra revelation | agot-eddard-10 |
| 1175 | 1 | Provided testimony to | `(LLM tail)` | Petyr Baelish → Robert Baratheon | agot-eddard-10 |
| 1176 | 1 | Acts as regent/Hand for | `(LLM tail)` | Eddard Stark → Robert Baratheon | agot-eddard-11 |
| 1177 | 1 | Defends / shields | `PROTECTS` | Grand Maester Pycelle → House Lannister | agot-eddard-11 |
| 1178 | 1 | Questions / probes | `(LLM tail)` | Littlefinger → Riverlord knights | agot-eddard-11 |
| 1179 | 1 | Eager to oppose | `(LLM tail)` | Ser Loras Tyrell → Gregor Clegane | agot-eddard-11 |
| 1180 | 1 | Denies / checks | `(LLM tail)` | Eddard Stark → Ser Loras Tyrell | agot-eddard-11 |
| 1181 | 1 | Judges as unwise | `(LLM tail)` | Eddard Stark → Edmure Tully | agot-eddard-11 |
| 1182 | 1 | Sends as messenger | `(LLM tail)` | Ned Stark → Ser Robar Royce | agot-eddard-11 |
| 1183 | 1 | Serves/reports to | `SERVES` | Pycelle → Cersei Lannister | agot-eddard-12 |
| 1184 | 1 | Furious with / opposes | `(LLM tail)` | Tywin Lannister → Eddard Stark | agot-eddard-12 |
| 1185 | 1 | Respects but sees as limited | `RESPECTS` | Eddard Stark → Ser Barristan Selmy | agot-eddard-12 |
| 1186 | 1 | Nickname | `(LLM tail)` | Ned's children (household) → Tomard | agot-eddard-12 |
| 1187 | 1 | Mocks/socializes with | `OPPOSES` | Littlefinger → Lady Tanda | agot-eddard-12 |
| 1188 | 1 | Lover of (since childhood) | `LOVER_OF` | Cersei Lannister → Jaime Lannister | agot-eddard-12 |
| 1189 | 1 | Mother of (by Jaime) | `PARENT_OF` | Cersei Lannister → Joffrey, Tommen, Myrcella | agot-eddard-12 |
| 1190 | 1 | Mourns/loves memory of | `MOURNS` | Robert Baratheon → Lyanna Stark | agot-eddard-12 |
| 1191 | 1 | Feels duty toward | `(LLM tail)` | Eddard Stark → Robert Baratheon | agot-eddard-12 |
| 1192 | 1 | Feels duty toward / mourns | `MOURNS` | Eddard Stark → Jon Arryn | agot-eddard-12 |
| 1193 | 1 | Attempts to seduce/manipulate | `(LLM tail)` | Cersei Lannister → Eddard Stark | agot-eddard-12 |
| 1194 | 1 | Attacks honor of | `ATTACKS` | Cersei Lannister → Eddard Stark | agot-eddard-12 |
| 1195 | 1 | Would kill for | `(LLM tail)` | Jaime Lannister → Cersei Lannister | agot-eddard-12 |
| 1196 | 1 | Mourns / associates with pale blue roses | `MOURNS` | Eddard Stark → Lyanna Stark | agot-eddard-12 |
| 1197 | 1 | Deep friendship, grief at impending loss | `MOURNS` | Eddard Stark → Robert Baratheon | agot-eddard-13 |
| 1198 | 1 | Trust and reliance | `(LLM tail)` | Robert Baratheon → Eddard Stark | agot-eddard-13 |
| 1199 | 1 | Estrangement / dismissiveness | `(LLM tail)` | Robert Baratheon → Cersei Lannister | agot-eddard-13 |
| 1200 | 1 | Watchful presence at deathbed | `(LLM tail)` | Cersei Lannister → Robert Baratheon | agot-eddard-13 |
| 1201 | 1 | Brotherly admiration mixed with pragmatism | `RESPECTS` | Renly Baratheon → Robert Baratheon | agot-eddard-13 |
| 1202 | 1 | Proposes alliance / political urgency | `ALLIES_WITH` | Lord Renly → Eddard Stark | agot-eddard-13 |
| 1203 | 1 | Refuses alliance on moral grounds | `ALLIES_WITH` | Eddard Stark → Lord Renly | agot-eddard-13 |
| 1204 | 1 | Guilt and devotion | `(LLM tail)` | Ser Barristan Selmy → Robert Baratheon | agot-eddard-13 |
| 1205 | 1 | Reassurance / respect | `RESPECTS` | Eddard Stark → Ser Barristan Selmy | agot-eddard-13 |
| 1206 | 1 | Suspicion / implication | `(LLM tail)` | Varys → Lancel Lannister | agot-eddard-13 |
| 1207 | 1 | Information broker | `(LLM tail)` | Varys → Littlefinger | agot-eddard-13 |
| 1208 | 1 | Political manipulation / self-interest | `(LLM tail)` | Littlefinger → Eddard Stark | agot-eddard-13 |
| 1209 | 1 | Professed love (used as leverage) | `LOVES` | Littlefinger → Catelyn Stark | agot-eddard-13 |
| 1210 | 1 | Moral contempt tempered by need | `(LLM tail)` | Eddard Stark → Littlefinger | agot-eddard-13 |
| 1211 | 1 | Guilt and remorse | `(LLM tail)` | Robert Baratheon → Daenerys Targaryen | agot-eddard-13 |
| 1212 | 1 | Protective commitment | `(LLM tail)` | Ned → Robert's bastards (Barra, Mya, Gendry) | agot-eddard-13 |
| 1213 | 1 | Deferential service | `(LLM tail)` | Grand Maester Pycelle → Robert Baratheon | agot-eddard-13 |
| 1214 | 1 | Contempt for his own reign | `HATES` | Robert Baratheon → Himself | agot-eddard-13 |
| 1215 | 1 | Echoed memory connection | `(LLM tail)` | Ned → Lyanna Stark | agot-eddard-13 |
| 1216 | 1 | Defiant/resentful toward | `RESENTS` | Sansa Stark → Eddard Stark | agot-eddard-14 |
| 1217 | 1 | Student/devoted to | `TUTORS` | Arya Stark → Syrio Forel | agot-eddard-14 |
| 1218 | 1 | Dutiful attendant to | `(LLM tail)` | Septa Mordane → Eddard Stark | agot-eddard-14 |
| 1219 | 1 | Deep grief for | `MOURNS` | Eddard Stark → Robert Baratheon | agot-eddard-14 |
| 1220 | 1 | Reliance on (misplaced) | `(LLM tail)` | Eddard Stark → Petyr Baelish | agot-eddard-14 |
| 1221 | 1 | Counted on support of | `(LLM tail)` | Eddard Stark → Renly Baratheon | agot-eddard-14 |
| 1222 | 1 | Allied with / fled with | `ALLIES_WITH` | Renly Baratheon → Loras Tyrell | agot-eddard-14 |
| 1223 | 1 | Hopes for / relies on (absent) | `(LLM tail)` | Eddard Stark → Stannis Baratheon | agot-eddard-14 |
| 1224 | 1 | Honor-bound loyalty to | `(LLM tail)` | Ser Barristan Selmy → Joffrey Baratheon | agot-eddard-14 |
| 1225 | 1 | Shocked/loyal to | `(LLM tail)` | Ser Barristan Selmy → Robert Baratheon (deceased) | agot-eddard-14 |
| 1226 | 1 | Demands loyalty from | `(LLM tail)` | Joffrey Baratheon → Small council | agot-eddard-14 |
| 1227 | 1 | Enraged by | `(LLM tail)` | Joffrey Baratheon → Eddard Stark | agot-eddard-14 |
| 1228 | 1 | Confused/dependent on | `(LLM tail)` | Myrcella Baratheon → Cersei Lannister | agot-eddard-14 |
| 1229 | 1 | Serves/betrays for | `SERVES` | Janos Slynt → Cersei Lannister (inferred) | agot-eddard-14 |
| 1230 | 1 | blames self for downfall of | `OPPOSES` | Eddard Stark → Robert Baratheon | agot-eddard-15 |
| 1231 | 1 | feels shame and sorrow toward | `(LLM tail)` | Eddard Stark → Jon Snow | agot-eddard-15 |
| 1232 | 1 | holds secret of | `(LLM tail)` | Eddard Stark → Lyanna Stark | agot-eddard-15 |
| 1233 | 1 | manipulates / pressures | `MANIPULATES` | Varys → Eddard Stark | agot-eddard-15 |
| 1234 | 1 | claims to have protected | `(LLM tail)` | Varys → Robert Baratheon | agot-eddard-15 |
| 1235 | 1 | orchestrated death of | `(LLM tail)` | Cersei Lannister → Robert Baratheon | agot-eddard-15 |
| 1236 | 1 | served as instrument of | `(LLM tail)` | Lancel Lannister → Cersei Lannister | agot-eddard-15 |
| 1237 | 1 | pleaded for life of | `(LLM tail)` | Sansa Stark → Eddard Stark | agot-eddard-15 |
| 1238 | 1 | crowned as queen of beauty | `(LLM tail)` | Rhaegar Targaryen → Lyanna Stark | agot-eddard-15 |
| 1239 | 1 | took vows before | `(LLM tail)` | Jaime Lannister → King Aerys | agot-eddard-15 |
| 1240 | 1 | fastened white cloak on | `(LLM tail)` | Ser Gerold Hightower → Jaime Lannister | agot-eddard-15 |
| 1241 | 1 | helped to feet | `(LLM tail)` | Ser Oswell Whent → Jaime Lannister | agot-eddard-15 |
| 1242 | 1 | owned | `(LLM tail)` | Rhaenys Targaryen → Balerion (the cat) | agot-eddard-15 |
| 1243 | 1 | is true heir of | `(LLM tail)` | Stannis Baratheon → Robert Baratheon | agot-eddard-15 |
| 1244 | 1 | marches south with army for | `(LLM tail)` | Robb Stark → Eddard Stark | agot-eddard-15 |
| 1245 | 1 | traveled with as youth | `(LLM tail)` | Varys → Troupe of mummers | agot-eddard-15 |
| 1246 | 1 | half-brother (acknowledged with pain) | `SIBLING_OF` | Jon Snow → Robb Stark | agot-jon-01 |
| 1247 | 1 | son (complicated) | `(LLM tail)` | Jon Snow → Eddard Stark | agot-jon-01 |
| 1248 | 1 | excluded by | `(LLM tail)` | Jon Snow → Catelyn Stark | agot-jon-01 |
| 1249 | 1 | nephew (warm affection) | `NEPHEW_OF` | Jon Snow → Benjen Stark | agot-jon-01 |
| 1250 | 1 | grudging mutual recognition | `(LLM tail)` | Jon Snow → Tyrion Lannister | agot-jon-01 |
| 1251 | 1 | admiration toward | `RESPECTS` | Jon Snow → Jaime Lannister | agot-jon-01 |
| 1252 | 1 | fascination toward | `(LLM tail)` | Jon Snow → Tyrion Lannister | agot-jon-01 |
| 1253 | 1 | sees through | `(LLM tail)` | Jon Snow → Cersei Lannister | agot-jon-01 |
| 1254 | 1 | hosts (formally) | `(LLM tail)` | Eddard Stark → Cersei Lannister | agot-jon-01 |
| 1255 | 1 | old friendship (strained) | `COMPANION_OF` | Eddard Stark → Robert Baratheon | agot-jon-01 |
| 1256 | 1 | cold/angry | `(LLM tail)` | Cersei Lannister → Robert Baratheon | agot-jon-01 |
| 1257 | 1 | twin to | `(LLM tail)` | Jaime Lannister → Cersei Lannister | agot-jon-01 |
| 1258 | 1 | brother (mocking affection) | `SIBLING_OF` | Tyrion Lannister → Jaime Lannister | agot-jon-01 |
| 1259 | 1 | ward of / ignores Jon | `WARD_OF` | Theon Greyjoy → Eddard Stark / Jon Snow | agot-jon-01 |
| 1260 | 1 | dominance over | `(LLM tail)` | Ghost → Mongrel dog | agot-jon-01 |
| 1261 | 1 | Brotherly love / deep bond | `LOVES` | Jon → Bran | agot-jon-02 |
| 1262 | 1 | Excluded outsider / target of hostility | `(LLM tail)` | Jon → Catelyn | agot-jon-02 |
| 1263 | 1 | Hostile rejection | `(LLM tail)` | Catelyn → Jon | agot-jon-02 |
| 1264 | 1 | Devoted, desperate mother | `(LLM tail)` | Catelyn → Bran | agot-jon-02 |
| 1265 | 1 | Close, affectionate brothers | `LOVES` | Jon → Robb | agot-jon-02 |
| 1266 | 1 | Brotherly concern for Jon | `(LLM tail)` | Robb → Jon | agot-jon-02 |
| 1267 | 1 | Deep affection / closest sibling bond | `LOVES` | Jon → Arya | agot-jon-02 |
| 1268 | 1 | Adoration / deep bond | `(LLM tail)` | Arya → Jon | agot-jon-02 |
| 1269 | 1 | Self-identifies as outsider to Stark family | `(LLM tail)` | Jon → Himself | agot-jon-02 |
| 1270 | 1 | Anticipation / respect | `RESPECTS` | Jon → Benjen Stark | agot-jon-02 |
| 1271 | 1 | Loyal companion / emotional support | `COMPANION_OF` | Ghost → Jon | agot-jon-02 |
| 1272 | 1 | Obedient companion | `COMPANION_OF` | Nymeria → Arya | agot-jon-02 |
| 1273 | 1 | Loyal companion | `COMPANION_OF` | Grey Wind → Robb | agot-jon-02 |
| 1274 | 1 | Antagonistic / chafing | `OPPOSES` | Arya → Septa Mordane | agot-jon-02 |
| 1275 | 1 | Conspiratorial exclusion | `CONSPIRES_WITH` | Arya → Sansa | agot-jon-02 |
| 1276 | 1 | Guilt / religious devotion | `(LLM tail)` | Catelyn → The Seven (Faith) | agot-jon-02 |
| 1277 | 1 | Growing into authority | `(LLM tail)` | Robb → Winterfell household | agot-jon-02 |
| 1278 | 1 | defeats in combat training | `DEFEATS` | Jon Snow → Grenn | agot-jon-03 |
| 1279 | 1 | feels contempt toward (initially) | `(LLM tail)` | Jon Snow → Night's Watch recruits | agot-jon-03 |
| 1280 | 1 | confronts | `(LLM tail)` | Grenn → Jon Snow | agot-jon-03 |
| 1281 | 1 | attacks | `ATTACKS` | Jon Snow → Toad | agot-jon-03 |
| 1282 | 1 | mentors/rebukes | `TUTORS` | Donal Noye → Jon Snow | agot-jon-03 |
| 1283 | 1 | misses (complex) | `MOURNS` | Jon Snow → Sansa Stark | agot-jon-03 |
| 1284 | 1 | rebuffs and distances from | `(LLM tail)` | Benjen Stark → Jon Snow | agot-jon-03 |
| 1285 | 1 | spends time with (as peer) | `(LLM tail)` | Benjen Stark → Jeor Mormont | agot-jon-03 |
| 1286 | 1 | receives counsel from | `ADVISES` | Jon Snow → Tyrion Lannister | agot-jon-03 |
| 1287 | 1 | shows compassion toward | `(LLM tail)` | Tyrion Lannister → Jon Snow | agot-jon-03 |
| 1288 | 1 | clashes with | `(LLM tail)` | Ser Alliser Thorne → Tyrion Lannister | agot-jon-03 |
| 1289 | 1 | offers to help/train | `(LLM tail)` | Jon Snow → Grenn | agot-jon-03 |
| 1290 | 1 | declares enmity toward | `(LLM tail)` | Ser Alliser Thorne → Jon Snow | agot-jon-03 |
| 1291 | 1 | forged weapon for | `(LLM tail)` | Donal Noye → Robert Baratheon | agot-jon-03 |
| 1292 | 1 | wonders about / questions | `(LLM tail)` | Jon Snow → Eddard Stark | agot-jon-03 |
| 1293 | 1 | cannot pray to | `(LLM tail)` | Jon Snow → The gods (old or new) | agot-jon-03 |
| 1294 | 1 | writes to | `(LLM tail)` | Robb Stark → Jon Snow (via Mormont) | agot-jon-03 |
| 1295 | 1 | Protector and emerging leader | `(LLM tail)` | Jon Snow → Samwell Tarly | agot-jon-04 |
| 1296 | 1 | Leader/respected figure among recruits | `RESPECTS` | Jon Snow → Pyp, Grenn, Halder, others | agot-jon-04 |
| 1297 | 1 | Loyal ally | `ALLIES_WITH` | Pyp → Jon Snow | agot-jon-04 |
| 1298 | 1 | Loyal ally (with initial reluctance) | `ALLIES_WITH` | Grenn → Jon Snow | agot-jon-04 |
| 1299 | 1 | Antagonist/tormentor | `(LLM tail)` | Ser Alliser Thorne → Jon Snow | agot-jon-04 |
| 1300 | 1 | Cruel authority | `(LLM tail)` | Ser Alliser Thorne → Samwell Tarly | agot-jon-04 |
| 1301 | 1 | Initially obedient to Thorne, later allied with Jon | `ALLIES_WITH` | Halder → Jon Snow | agot-jon-04 |
| 1302 | 1 | Hostile/defiant toward Jon | `(LLM tail)` | Rast → Jon Snow | agot-jon-04 |
| 1303 | 1 | Comfort/protection | `(LLM tail)` | Ghost → Samwell Tarly | agot-jon-04 |
| 1304 | 1 | Enforcer/weapon | `(LLM tail)` | Ghost → Rast | agot-jon-04 |
| 1305 | 1 | Abusive, threatening father | `(LLM tail)` | Lord Randyll Tarly → Samwell Tarly | agot-jon-04 |
| 1306 | 1 | Loving mother | `(LLM tail)` | Lady Tarly → Samwell Tarly | agot-jon-04 |
| 1307 | 1 | Displaced heir | `(LLM tail)` | Samwell Tarly → Dickon Tarly | agot-jon-04 |
| 1308 | 1 | Bannerman | `(LLM tail)` | House Tarly → House Tyrell | agot-jon-04 |
| 1309 | 1 | Estranged/excluded | `(LLM tail)` | Jon Snow → Catelyn Stark | agot-jon-04 |
| 1310 | 1 | Longing for connection | `(LLM tail)` | Jon Snow → Benjen Stark | agot-jon-04 |
| 1311 | 1 | Brother-like bond / memories | `SIBLING_OF` | Jon Snow → Robb Stark | agot-jon-04 |
| 1312 | 1 | Background friendship | `COMPANION_OF` | Dareon → Jon Snow | agot-jon-04 |
| 1313 | 1 | Intellectual respect / recalled connection | `RESPECTS` | Jon Snow → Tyrion Lannister | agot-jon-04 |
| 1314 | 1 | Authority over / contempt for | `COMMANDS` | Ser Alliser Thorne → The recruits | agot-jon-05 |
| 1315 | 1 | Friendship / protectiveness | `COMPANION_OF` | Jon Snow → Samwell Tarly | agot-jon-05 |
| 1316 | 1 | Loyalty / refusal to grieve | `MOURNS` | Jon Snow → Benjen Stark | agot-jon-05 |
| 1317 | 1 | Respect / seeks help from | `RESPECTS` | Jon Snow → Maester Aemon | agot-jon-05 |
| 1318 | 1 | Hostility / gatekeeping | `(LLM tail)` | Chett → Jon Snow | agot-jon-05 |
| 1319 | 1 | Mentorship / respect toward | `RESPECTS` | Maester Aemon → Jon Snow | agot-jon-05 |
| 1320 | 1 | Gratitude / remembrance | `(LLM tail)` | Jon Snow → Maester Luwin | agot-jon-05 |
| 1321 | 1 | Love / grief | `MOURNS` | Jon Snow → Bran Stark | agot-jon-05 |
| 1322 | 1 | Resentment / pain | `RESENTS` | Jon Snow → Catelyn Stark | agot-jon-05 |
| 1323 | 1 | Longing / sadness | `(LLM tail)` | Jon Snow → His unknown mother | agot-jon-05 |
| 1324 | 1 | Complex feeling (love, shame, confusion) | `LOVES` | Jon Snow → Eddard Stark | agot-jon-05 |
| 1325 | 1 | Bond / companionship | `(LLM tail)` | Ghost → Jon Snow | agot-jon-05 |
| 1326 | 1 | Acceptance of | `(LLM tail)` | Ghost → Samwell Tarly | agot-jon-05 |
| 1327 | 1 | Welcoming / formal hospitality | `(LLM tail)` | Bowen Marsh → Jon Snow | agot-jon-05 |
| 1328 | 1 | Failed to make warrior of | `(LLM tail)` | Lord Randyll Tarly → Samwell Tarly | agot-jon-05 |
| 1329 | 1 | Antagonism/target of | `(LLM tail)` | Jon Snow → Ser Alliser Thorne | agot-jon-06 |
| 1330 | 1 | Assigned to assist | `(LLM tail)` | Samwell Tarly → Maester Aemon | agot-jon-06 |
| 1331 | 1 | Temporarily replaces | `(LLM tail)` | Ser Jaremy Rykker → Benjen Stark | agot-jon-06 |
| 1332 | 1 | Keeps faith of | `(LLM tail)` | Jon Snow → The old gods | agot-jon-06 |
| 1333 | 1 | Forsakes | `(LLM tail)` | Sam Tarly → The Seven (Faith) | agot-jon-06 |
| 1334 | 1 | Self-identifies with | `(LLM tail)` | Jon Snow → Stark heritage / First Men | agot-jon-06 |
| 1335 | 1 | Recalls / respects | `RESPECTS` | Jon Snow → Benjen Stark | agot-jon-06 |
| 1336 | 1 | Deference to | `(LLM tail)` | Bowen Marsh → Sacred weirwood grove | agot-jon-06 |
| 1337 | 1 | Bonded to / protected by | `BONDED_TO` | Jon Snow → Ghost | agot-jon-07 |
| 1338 | 1 | Nephew of (believed son of brother) | `NEPHEW_OF` | Jon Snow → Benjen Stark | agot-jon-07 |
| 1339 | 1 | Sent by / serves | `(LLM tail)` | Samwell Tarly → Maester Aemon | agot-jon-07 |
| 1340 | 1 | Paternal authority over | `(LLM tail)` | Jeor Mormont → Jon Snow | agot-jon-07 |
| 1341 | 1 | Disappointment toward | `(LLM tail)` | Jeor Mormont → Jorah Mormont | agot-jon-07 |
| 1342 | 1 | Complicated rejection of | `(LLM tail)` | Jon Snow → Catelyn Stark | agot-jon-07 |
| 1343 | 1 | Loyalty and love toward | `LOVES` | Jon Snow → Eddard Stark | agot-jon-07 |
| 1344 | 1 | Brotherhood with (recalled) | `(LLM tail)` | Jon Snow → Robb Stark | agot-jon-07 |
| 1345 | 1 | Remembered friendship with | `COMPANION_OF` | Jon Snow → Tyrion Lannister | agot-jon-07 |
| 1346 | 1 | Blame toward | `(LLM tail)` | Jon Snow → Catelyn Stark | agot-jon-07 |
| 1347 | 1 | Observant veteran alongside | `(LLM tail)` | Dywen → Ser Jaremy Rykker | agot-jon-07 |
| 1348 | 1 | Uncanny responsiveness to | `(LLM tail)` | Mormont's raven → The situation | agot-jon-07 |
| 1349 | 1 | Accused of treason against | `(LLM tail)` | Eddard Stark → Joffrey Baratheon | agot-jon-07 |
| 1350 | 1 | Liege/steward to | `(LLM tail)` | Jon Snow → Jeor Mormont | agot-jon-08 |
| 1351 | 1 | Rewards/mentors | `TUTORS` | Jeor Mormont → Jon Snow | agot-jon-08 |
| 1352 | 1 | Loyal but conflicted friend to | `(LLM tail)` | Samwell Tarly → Jon Snow | agot-jon-08 |
| 1353 | 1 | Counsels/tests | `ADVISES` | Maester Aemon → Jon Snow | agot-jon-08 |
| 1354 | 1 | Collaborated with | `(LLM tail)` | Halder → Pate (builder) | agot-jon-08 |
| 1355 | 1 | Bought garnets for | `(LLM tail)` | Samwell Tarly → Jon Snow (Longclaw pommel) | agot-jon-08 |
| 1356 | 1 | Ashamed of | `(LLM tail)` | Jeor Mormont → Jorah Mormont | agot-jon-08 |
| 1357 | 1 | Returned Longclaw to | `(LLM tail)` | Mormont's sister → Jeor Mormont | agot-jon-08 |
| 1358 | 1 | Respected | `RESPECTS` | Mormont → Ser Barristan Selmy | agot-jon-08 |
| 1359 | 1 | Internal conflict about | `(LLM tail)` | Jon Snow → Night's Watch vows | agot-jon-08 |
| 1360 | 1 | Grieved for | `MOURNS` | Aemon → House Targaryen | agot-jon-08 |
| 1361 | 1 | Assisted | `(LLM tail)` | Rudge → Donal Noye | agot-jon-08 |
| 1362 | 1 | Brotherhood/deep friendship | `COMPANION_OF` | Jon Snow → Samwell Tarly | agot-jon-09 |
| 1363 | 1 | Brotherhood/loyalty conflict | `(LLM tail)` | Jon Snow → Robb Stark | agot-jon-09 |
| 1364 | 1 | Filial devotion/grief | `MOURNS` | Jon Snow → Eddard Stark | agot-jon-09 |
| 1365 | 1 | Commander/steward loyalty | `COMMANDS` | Jon Snow → Jeor Mormont | agot-jon-09 |
| 1366 | 1 | Reluctant conflict | `(LLM tail)` | Jon Snow → Pyp, Grenn, Halder, Toad, Matthar | agot-jon-09 |
| 1367 | 1 | Loyalty/protectiveness | `(LLM tail)` | Samwell Tarly → Jon Snow | agot-jon-09 |
| 1368 | 1 | Mentorship/authority | `TUTORS` | Jeor Mormont → Jon Snow | agot-jon-09 |
| 1369 | 1 | Respect/reliance | `RESPECTS` | Jeor Mormont → Maester Aemon | agot-jon-09 |
| 1370 | 1 | Strained love | `LOVES` | Jeor Mormont → Maege Mormont | agot-jon-09 |
| 1371 | 1 | Shame/grief | `MOURNS` | Jeor Mormont → Jorah Mormont | agot-jon-09 |
| 1372 | 1 | Intellectual respect | `RESPECTS` | Jon Snow → Tyrion Lannister | agot-jon-09 |
| 1373 | 1 | Moral reflection | `(LLM tail)` | Jon Snow → Maester Aemon | agot-jon-09 |
| 1374 | 1 | Longing/guilt | `(LLM tail)` | Jon Snow → Bran Stark, Arya Stark | agot-jon-09 |
| 1375 | 1 | Leadership in the rescue | `(LLM tail)` | Pyp → Jon's friend group | agot-jon-09 |
| 1376 | 1 | Tactical authority | `(LLM tail)` | Halder → Jon's friend group | agot-jon-09 |
| 1377 | 1 | Resents / mocks (privately) | `RESENTS` | Will → Ser Waymar Royce | agot-prologue |
| 1378 | 1 | Resents / near-insubordinate toward | `RESENTS` | Gared → Ser Waymar Royce | agot-prologue |
| 1379 | 1 | Fellow ranger, shared unease with | `(LLM tail)` | Gared → Will | agot-prologue |
| 1380 | 1 | Subordinate to / respects authority of | `RESPECTS` | Will → Mormont | agot-prologue |
| 1381 | 1 | Respects knowledge of | `RESPECTS` | Will → Maester Aemon | agot-prologue |
| 1382 | 1 | Treated by | `HEALS` | Gared → Maester Aemon | agot-prologue |
| 1383 | 1 | Invokes / fights for | `(LLM tail)` | Ser Waymar Royce → Robert (the king) | agot-prologue |
| 1384 | 1 | Caught / gave choice to | `(LLM tail)` | Mallister freeriders → Will | agot-prologue |
| 1385 | 1 | Frustrated with / embarrassed by | `(LLM tail)` | Sansa → Arya | agot-sansa-01 |
| 1386 | 1 | Loves and trusts | `LOVES` | Sansa → Lady | agot-sansa-01 |
| 1387 | 1 | Performatively chivalrous toward | `(LLM tail)` | Joffrey → Sansa | agot-sansa-01 |
| 1388 | 1 | Guards / obeys | `GUARDS` | Sandor Clegane → Joffrey | agot-sansa-01 |
| 1389 | 1 | Directs / controls | `(LLM tail)` | Cersei → Joffrey | agot-sansa-01 |
| 1390 | 1 | Governs / teaches | `(LLM tail)` | Septa Mordane → Sansa and Arya | agot-sansa-01 |
| 1391 | 1 | Playful / teasing toward | `(LLM tail)` | Renly Baratheon → Sansa | agot-sansa-01 |
| 1392 | 1 | Teased by / teases | `(LLM tail)` | Renly Baratheon → Ser Barristan Selmy | agot-sansa-01 |
| 1393 | 1 | Terrifies | `(LLM tail)` | Ser Ilyn Payne → Sansa | agot-sansa-01 |
| 1394 | 1 | Wishes were different | `(LLM tail)` | Sansa → Arya | agot-sansa-01 |
| 1395 | 1 | Indulgent toward | `(LLM tail)` | Eddard Stark → Arya | agot-sansa-01 |
| 1396 | 1 | Companion/friend | `COMPANION_OF` | Sansa → Jeyne Poole | agot-sansa-02 |
| 1397 | 1 | Redirected hatred toward | `(LLM tail)` | Sansa → Cersei | agot-sansa-02 |
| 1398 | 1 | Awe/attraction toward | `(LLM tail)` | Sansa → Ser Loras Tyrell | agot-sansa-02 |
| 1399 | 1 | Fear evolving to empathy toward | `FEARS` | Sansa → Sandor Clegane | agot-sansa-02 |
| 1400 | 1 | Possessive/commanding toward | `COMMANDS` | Joffrey → Sandor Clegane | agot-sansa-02 |
| 1401 | 1 | Deep hatred toward | `(LLM tail)` | Sandor Clegane → Gregor Clegane | agot-sansa-02 |
| 1402 | 1 | Burned/brutalized | `(LLM tail)` | Gregor Clegane → Sandor Clegane | agot-sansa-02 |
| 1403 | 1 | Deliberately killed | `(LLM tail)` | Gregor Clegane → Young knight from the Vale | agot-sansa-02 |
| 1404 | 1 | Silently furious at | `(LLM tail)` | Cersei → Robert | agot-sansa-02 |
| 1405 | 1 | Diplomatically manages | `(LLM tail)` | Renly → Robert | agot-sansa-02 |
| 1406 | 1 | Past romantic attachment to | `(LLM tail)` | Littlefinger → Catelyn Stark | agot-sansa-02 |
| 1407 | 1 | Unsettling interest in | `(LLM tail)` | Littlefinger → Sansa | agot-sansa-02 |
| 1408 | 1 | Contempt for knighthood | `HATES` | Sandor → (institution) | agot-sansa-02 |
| 1409 | 1 | Covered up abuse by | `(LLM tail)` | Sandor's father → Gregor Clegane | agot-sansa-02 |
| 1410 | 1 | Sons/grandsons/bastard of | `(LLM tail)` | Six Frey knights + Martyn Rivers → Walder Frey | agot-sansa-02 |
| 1411 | 1 | Heir of | `HEIR_TO` | Ser Andar Royce → Yohn Royce | agot-sansa-02 |
| 1412 | 1 | Younger son of | `(LLM tail)` | Ser Robar Royce → Yohn Royce | agot-sansa-02 |
| 1413 | 1 | Romantic idealization | `(LLM tail)` | Sansa Stark → Joffrey Baratheon | agot-sansa-03 |
| 1414 | 1 | Antagonism/sibling rivalry | `(LLM tail)` | Sansa Stark → Arya Stark | agot-sansa-03 |
| 1415 | 1 | Unsettling attention toward | `(LLM tail)` | Petyr Baelish → Sansa Stark | agot-sansa-03 |
| 1416 | 1 | Conciliation toward | `(LLM tail)` | Arya Stark → Sansa/Ned | agot-sansa-03 |
| 1417 | 1 | Fear/revulsion toward | `FEARS` | Sansa Stark → Ilyn Payne | agot-sansa-03 |
| 1418 | 1 | Confined by | `(LLM tail)` | Sansa Stark → Cersei Lannister | agot-sansa-04 |
| 1419 | 1 | Manipulated by | `MANIPULATES` | Sansa Stark → Cersei Lannister | agot-sansa-04 |
| 1420 | 1 | Distances herself from | `(LLM tail)` | Sansa Stark → Arya Stark | agot-sansa-04 |
| 1421 | 1 | Fixated on | `(LLM tail)` | Petyr Baelish → Sansa Stark | agot-sansa-04 |
| 1422 | 1 | Possesses | `(LLM tail)` | Varys → Eddard's seal | agot-sansa-04 |
| 1423 | 1 | Trusts naively | `TRUSTS` | Sansa Stark → Joffrey Baratheon | agot-sansa-04 |
| 1424 | 1 | Previously informed on | `(LLM tail)` | Sansa Stark → Eddard Stark | agot-sansa-04 |
| 1425 | 1 | Shunned by | `(LLM tail)` | Sansa Stark → Lords at court | agot-sansa-05 |
| 1426 | 1 | Controls/monitors | `COMMANDS` | Cersei Lannister → Sansa Stark | agot-sansa-05 |
| 1427 | 1 | Appointed to serve | `(LLM tail)` | Sandor Clegane → Joffrey Baratheon | agot-sansa-05 |
| 1428 | 1 | Refuses subordination to | `SERVES` | Sandor Clegane → Kingsguard traditions | agot-sansa-05 |
| 1429 | 1 | Conditionally grants mercy to | `(LLM tail)` | Joffrey Baratheon → Eddard Stark | agot-sansa-05 |
| 1430 | 1 | Opposes mercy for | `OPPOSES` | Pycelle → Eddard Stark | agot-sansa-05 |
| 1431 | 1 | Questions | `(LLM tail)` | Littlefinger → Sansa Stark | agot-sansa-05 |
| 1432 | 1 | Sets terms for | `(LLM tail)` | Cersei → Eddard Stark | agot-sansa-05 |
| 1433 | 1 | Thinks of/worries about | `(LLM tail)` | Sansa Stark → Arya Stark | agot-sansa-05 |
| 1434 | 1 | Dominates/abuses | `(LLM tail)` | Joffrey → Sansa | agot-sansa-06 |
| 1435 | 1 | Betrothed to (against her will) | `BETROTHED_TO` | Sansa → Joffrey | agot-sansa-06 |
| 1436 | 1 | Protects/advises (roughly) | `PROTECTS` | Sandor Clegane → Sansa | agot-sansa-06 |
| 1437 | 1 | Serves (but with independent judgment) | `SERVES` | Sandor Clegane → Joffrey | agot-sansa-06 |
| 1438 | 1 | Controls (through Joffrey) | `COMMANDS` | Cersei → Sansa | agot-sansa-06 |
| 1439 | 1 | Advises/restrains | `ADVISES` | Cersei → Joffrey | agot-sansa-06 |
| 1440 | 1 | Sycophantic loyalty to | `(LLM tail)` | Janos Slynt → Joffrey | agot-sansa-06 |
| 1441 | 1 | Recalls advice of | `(LLM tail)` | Sansa → Petyr Baelish | agot-sansa-06 |
| 1442 | 1 | Mourns/concerned for | `MOURNS` | Cersei → Jaime Lannister | agot-sansa-06 |
| 1443 | 1 | uncle, disciplinarian | `UNCLE_OF` | Tyrion → Joffrey | agot-tyrion-01 |
| 1444 | 1 | affection/gratitude despite differences | `LOVES` | Tyrion → Jaime | agot-tyrion-01 |
| 1445 | 1 | distaste/hostility toward | `(LLM tail)` | Cersei → Tyrion | agot-tyrion-01 |
| 1446 | 1 | twin, co-conspirator | `CONSPIRES_WITH` | Jaime → Cersei | agot-tyrion-01 |
| 1447 | 1 | bodyguard, obedient | `(LLM tail)` | Sandor Clegane → Joffrey | agot-tyrion-01 |
| 1448 | 1 | mocking/contemptuous toward | `(LLM tail)` | Sandor Clegane → Tyrion | agot-tyrion-01 |
| 1449 | 1 | dismissive authority toward | `(LLM tail)` | Tyrion → Sandor Clegane | agot-tyrion-01 |
| 1450 | 1 | cruel indifference toward | `(LLM tail)` | Joffrey → Bran Stark | agot-tyrion-01 |
| 1451 | 1 | gentle concern toward | `(LLM tail)` | Tommen → Bran Stark | agot-tyrion-01 |
| 1452 | 1 | concern toward | `(LLM tail)` | Myrcella → Bran Stark | agot-tyrion-01 |
| 1453 | 1 | wary suspicion toward | `(LLM tail)` | Tyrion → Jaime and Cersei | agot-tyrion-01 |
| 1454 | 1 | veiled threat toward | `(LLM tail)` | Jaime → Tyrion | agot-tyrion-01 |
| 1455 | 1 | casual disregard toward | `(LLM tail)` | Jaime → Robert | agot-tyrion-01 |
| 1456 | 1 | sympathy toward | `(LLM tail)` | Robert → Eddard Stark | agot-tyrion-01 |
| 1457 | 1 | intellectual respect toward | `RESPECTS` | Tyrion → Winterfell's library | agot-tyrion-01 |
| 1458 | 1 | paternal kindness toward | `(LLM tail)` | Tyrion → Tommen and Myrcella | agot-tyrion-01 |
| 1459 | 1 | Reluctant traveling companion / mutual antagonism | `COMPANION_OF` | Tyrion → Benjen Stark | agot-tyrion-02 |
| 1460 | 1 | Mentoring / kinship of outsiders | `TUTORS` | Tyrion → Jon Snow | agot-tyrion-02 |
| 1461 | 1 | Bonded with / protected by | `BONDED_TO` | Jon Snow → Ghost | agot-tyrion-02 |
| 1462 | 1 | Hostility / wariness toward | `(LLM tail)` | Ghost → Tyrion | agot-tyrion-02 |
| 1463 | 1 | Protective uncle | `UNCLE_OF` | Benjen Stark → Jon Snow | agot-tyrion-02 |
| 1464 | 1 | Admiration / comparison | `RESPECTS` | Tyrion → Jaime Lannister (brother) | agot-tyrion-02 |
| 1465 | 1 | Disillusionment toward | `(LLM tail)` | Jon Snow → Night's Watch | agot-tyrion-02 |
| 1466 | 1 | Distaste toward | `(LLM tail)` | Benjen Stark → Lannisters (as a family) | agot-tyrion-02 |
| 1467 | 1 | Captor / escort of | `CAPTURES` | Yoren → Two peasant recruits | agot-tyrion-02 |
| 1468 | 1 | mocks / antagonizes | `OPPOSES` | Tyrion → Ser Alliser Thorne | agot-tyrion-03 |
| 1469 | 1 | respects / is moved by | `RESPECTS` | Tyrion → Maester Aemon | agot-tyrion-03 |
| 1470 | 1 | respects / praises | `RESPECTS` | Maester Aemon → Tyrion | agot-tyrion-03 |
| 1471 | 1 | appeals to / trusts | `(LLM tail)` | Mormont → Tyrion | agot-tyrion-03 |
| 1472 | 1 | pities / respects | `RESPECTS` | Tyrion → Mormont | agot-tyrion-03 |
| 1473 | 1 | friendship / trust | `COMPANION_OF` | Jon Snow → Tyrion | agot-tyrion-03 |
| 1474 | 1 | loves / misses | `LOVES` | Jon Snow → Benjen Stark | agot-tyrion-03 |
| 1475 | 1 | loves / worries about | `LOVES` | Jon Snow → Bran Stark | agot-tyrion-03 |
| 1476 | 1 | persecutes | `(LLM tail)` | Ser Alliser Thorne → Jon Snow | agot-tyrion-03 |
| 1477 | 1 | privately doubts efficacy of | `(LLM tail)` | Tyrion → Robert, Tywin, Jaime | agot-tyrion-03 |
| 1478 | 1 | grieves / is estranged from | `MOURNS` | Mormont → His son (Jorah, implied) | agot-tyrion-03 |
| 1479 | 1 | tolerant of | `(LLM tail)` | Ghost → Tyrion | agot-tyrion-03 |
| 1480 | 1 | forced into service | `(LLM tail)` | Tywin Lannister → Thorne, Rykker | agot-tyrion-03 |
| 1481 | 1 | hostile toward / indebted to | `OPPOSES` | Tyrion → House Stark | agot-tyrion-04 |
| 1482 | 1 | planning revenge against | `(LLM tail)` | Tyrion → Kurleket, Lharys, Mohor, Ser Willis Wode, Bronn, Chiggen, Marillion | agot-tyrion-04 |
| 1483 | 1 | grief/bitterness over | `MOURNS` | Tyrion → Jaime Lannister (the mare) | agot-tyrion-04 |
| 1484 | 1 | contempt/cruelty toward | `HATES` | Tyrion → Marillion | agot-tyrion-04 |
| 1485 | 1 | neutral toward | `(LLM tail)` | Yoren → Both parties | agot-tyrion-04 |
| 1486 | 1 | boasts about (sexually) | `(LLM tail)` | Petyr Baelish → Catelyn Stark | agot-tyrion-04 |
| 1487 | 1 | Torments/controls | `(LLM tail)` | Mord → Tyrion | agot-tyrion-05 |
| 1488 | 1 | Bribes/manipulates | `(LLM tail)` | Tyrion → Mord | agot-tyrion-05 |
| 1489 | 1 | Accuses publicly | `(LLM tail)` | Lysa Arryn → Tyrion | agot-tyrion-05 |
| 1490 | 1 | Dependent on / protected by | `(LLM tail)` | Robert Arryn → Lysa Arryn | agot-tyrion-05 |
| 1491 | 1 | Claims custody of | `(LLM tail)` | Catelyn Stark → Tyrion | agot-tyrion-05 |
| 1492 | 1 | Sister (tense) | `SIBLING_OF` | Catelyn Stark → Lysa Arryn | agot-tyrion-05 |
| 1493 | 1 | Ignores / overrides | `(LLM tail)` | Lysa Arryn → Catelyn Stark | agot-tyrion-05 |
| 1494 | 1 | Brother, relies on reputation of | `SIBLING_OF` | Tyrion → Jaime Lannister | agot-tyrion-05 |
| 1495 | 1 | Served loyally | `(LLM tail)` | Ser Vardis Egen → Jon Arryn | agot-tyrion-05 |
| 1496 | 1 | Named champion by | `(LLM tail)` | Ser Vardis Egen → Lysa Arryn | agot-tyrion-05 |
| 1497 | 1 | Reluctant to fight | `(LLM tail)` | Ser Vardis Egen → Tyrion | agot-tyrion-05 |
| 1498 | 1 | Champions | `(LLM tail)` | Bronn → Tyrion | agot-tyrion-05 |
| 1499 | 1 | Carried | `(LLM tail)` | Bronn → Tyrion | agot-tyrion-05 |
| 1500 | 1 | Wary interest in | `(LLM tail)` | Tyrion → Bronn | agot-tyrion-05 |
| 1501 | 1 | Useful to | `(LLM tail)` | Marillion → Tyrion | agot-tyrion-05 |
| 1502 | 1 | Eager to kill | `(LLM tail)` | Multiple Vale knights → Tyrion | agot-tyrion-05 |
| 1503 | 1 | Son/heir of | `(LLM tail)` | Ser Albar Royce → Lord Nestor Royce | agot-tyrion-05 |
| 1504 | 1 | Employer/patron of | `(LLM tail)` | Tyrion → Bronn | agot-tyrion-06 |
| 1505 | 1 | Mutual pragmatic respect with | `RESPECTS` | Tyrion → Bronn | agot-tyrion-06 |
| 1506 | 1 | Lasting grief over | `MOURNS` | Tyrion → Tysha (unnamed wife) | agot-tyrion-06 |
| 1507 | 1 | Served then abandoned | `(LLM tail)` | Bronn → Catelyn Stark | agot-tyrion-06 |
| 1508 | 1 | Contempt toward / negotiates with | `HATES` | Tyrion → Gunthor son of Gurn | agot-tyrion-06 |
| 1509 | 1 | Offers alliance to | `ALLIES_WITH` | Tyrion → Stone Crows | agot-tyrion-06 |
| 1510 | 1 | Paid debt to | `(LLM tail)` | Tyrion → Mord | agot-tyrion-06 |
| 1511 | 1 | Cruelly punished | `(LLM tail)` | Tywin Lannister → Tyrion | agot-tyrion-06 |
| 1512 | 1 | Arranged deception of | `(LLM tail)` | Jaime Lannister → Tyrion | agot-tyrion-06 |
| 1513 | 1 | Son, treated with contempt | `(LLM tail)` | Tyrion → Tywin | agot-tyrion-07 |
| 1514 | 1 | Nephew/uncle | `NEPHEW_OF` | Tyrion → Kevan | agot-tyrion-07 |
| 1515 | 1 | Brother (compared to) | `SIBLING_OF` | Tyrion → Jaime | agot-tyrion-07 |
| 1516 | 1 | Uneasy leader/captive of | `(LLM tail)` | Tyrion → Clansmen (collectively) | agot-tyrion-07 |
| 1517 | 1 | Father, dismissive of | `(LLM tail)` | Tywin → Tyrion | agot-tyrion-07 |
| 1518 | 1 | Brother, defers to his authority | `SIBLING_OF` | Tywin → Kevan | agot-tyrion-07 |
| 1519 | 1 | Follows but threatens | `(LLM tail)` | Shagga → Tyrion | agot-tyrion-07 |
| 1520 | 1 | Considers irrelevant | `(LLM tail)` | Tywin → Walder Frey | agot-tyrion-07 |
| 1521 | 1 | Plans to deal with | `(LLM tail)` | Tywin → Stannis Baratheon | agot-tyrion-07 |
| 1522 | 1 | Contemptuous father to | `HATES` | Tywin → Tyrion | agot-tyrion-08 |
| 1523 | 1 | Seeks approval from / resents | `SEEKS` | Tyrion → Tywin | agot-tyrion-08 |
| 1524 | 1 | Compares himself unfavorably to | `(LLM tail)` | Tyrion → Jaime | agot-tyrion-08 |
| 1525 | 1 | Employs / relies on | `(LLM tail)` | Tyrion → Bronn | agot-tyrion-08 |
| 1526 | 1 | Defers to / speaks for | `(LLM tail)` | Kevan → Tywin | agot-tyrion-08 |
| 1527 | 1 | Commander of (nominal) | `COMMANDS` | Tyrion → Mountain clans | agot-tyrion-08 |
| 1528 | 1 | Assigned under | `(LLM tail)` | Tyrion → Gregor Clegane | agot-tyrion-08 |
| 1529 | 1 | Strategically manipulates | `(LLM tail)` | Tywin → Tyrion | agot-tyrion-08 |
| 1530 | 1 | Welcoming toward | `(LLM tail)` | Conn son of Coratt → Tyrion | agot-tyrion-08 |
| 1531 | 1 | Master to | `(LLM tail)` | Tyrion → Podrick Payne | agot-tyrion-08 |
| 1532 | 1 | Loves (brother) | `LOVES` | Tyrion → Jaime | agot-tyrion-09 |
| 1533 | 1 | Lover | `LOVER_OF` | Tyrion → Shae | agot-tyrion-09 |
| 1534 | 1 | Grudging reliance on | `(LLM tail)` | Tywin → Tyrion | agot-tyrion-09 |
| 1535 | 1 | Values | `(LLM tail)` | Tywin → Jaime | agot-tyrion-09 |
| 1536 | 1 | Condemns decisions of | `(LLM tail)` | Tywin → Joffrey | agot-tyrion-09 |
| 1537 | 1 | Disguised protégée of | `DISGUISED_AS` | Arya → Yoren | acok-arya-01 |
| 1538 | 1 | Deep love and longing for | `LOVES` | Arya → Jon Snow | acok-arya-01 |
| 1539 | 1 | Mourning | `MOURNS` | Arya → Eddard Stark | acok-arya-01 |
| 1540 | 1 | Student of (recalled) | `TUTORS` | Arya → Syrio Forel | acok-arya-01 |
| 1541 | 1 | Antagonized by | `OPPOSES` | Arya → Lommy Greenhands | acok-arya-01 |
| 1542 | 1 | Antagonized by, then dominates | `(LLM tail)` | Arya → Hot Pie | acok-arya-01 |
| 1543 | 1 | Protects / defends | `PROTECTS` | The Bull → Arya | acok-arya-01 |
| 1544 | 1 | Fears (after fight) | `FEARS` | Lommy → Arya | acok-arya-01 |
| 1545 | 1 | Recruiter/escort for | `MEMBER_OF` | Yoren → Night's Watch | acok-arya-01 |
| 1546 | 1 | Connected to unnamed messenger regarding | `(LLM tail)` | Yoren → Eddard Stark | acok-arya-01 |
| 1547 | 1 | Gave Needle to | `GIFTED_TO` | Jon Snow → Arya | acok-arya-01 |
| 1548 | 1 | recalls teachings of | `(LLM tail)` | Arya → Syrio Forel | acok-arya-02 |
| 1549 | 1 | rallies to defend | `(LLM tail)` | Hot Pie → Arya/the group | acok-arya-02 |
| 1550 | 1 | rally to defend | `(LLM tail)` | Tarber, Cutjack, Kurz, Koss, Reysen, Dobber → Yoren's party | acok-arya-02 |
| 1551 | 1 | wants to capture | `(LLM tail)` | Queen Cersei → Gendry | acok-arya-02 |
| 1552 | 1 | companion of (involuntary) | `COMPANION_OF` | Jaqen H'ghar → Rorge, Biter | acok-arya-02 |
| 1553 | 1 | rebuked by | `(LLM tail)` | Lommy → The Bull | acok-arya-02 |
| 1554 | 1 | Shares food with / companionship | `(LLM tail)` | Arya → Gendry | acok-arya-03 |
| 1555 | 1 | Subordinate to / protected by | `SERVES` | Arya → Yoren | acok-arya-03 |
| 1556 | 1 | Wary companionship | `(LLM tail)` | Arya → Hot Pie | acok-arya-03 |
| 1557 | 1 | Contempt for / mocked by | `HATES` | Arya → Rorge | acok-arya-03 |
| 1558 | 1 | Polite interaction with | `(LLM tail)` | Arya → Jaqen H'ghar | acok-arya-03 |
| 1559 | 1 | Believes is father's only bastard | `(LLM tail)` | Arya → Jon | acok-arya-03 |
| 1560 | 1 | Former apprentice to | `(LLM tail)` | Gendry → Master Mott | acok-arya-03 |
| 1561 | 1 | Wanted by | `(LLM tail)` | Gendry → The queen (Cersei) | acok-arya-03 |
| 1562 | 1 | Speculates about parentage of | `(LLM tail)` | Lommy → Gendry | acok-arya-03 |
| 1563 | 1 | Protector / leader of | `(LLM tail)` | Yoren → Entire party | acok-arya-03 |
| 1564 | 1 | Hunting partner of | `(LLM tail)` | Kurz → Koss | acok-arya-03 |
| 1565 | 1 | Disciplinarian toward | `(LLM tail)` | Murch → Rorge, Biter | acok-arya-03 |
| 1566 | 1 | Peacekeeper | `(LLM tail)` | Reysen → Hot Pie, Lommy | acok-arya-03 |
| 1567 | 1 | Confides in | `(LLM tail)` | Hot Pie → Arya | acok-arya-03 |
| 1568 | 1 | trusts and follows | `TRUSTS` | Arya → Yoren | acok-arya-04 |
| 1569 | 1 | grudging comradeship | `(LLM tail)` | Arya → Hot Pie | acok-arya-04 |
| 1570 | 1 | annoyance toward | `(LLM tail)` | Arya → Lommy | acok-arya-04 |
| 1571 | 1 | remembers with fondness | `(LLM tail)` | Arya → Syrio Forel | acok-arya-04 |
| 1572 | 1 | complicated choice toward | `(LLM tail)` | Arya → Jaqen H'ghar, Rorge, Biter | acok-arya-04 |
| 1573 | 1 | pleading/manipulative toward | `(LLM tail)` | Jaqen H'ghar → Arya | acok-arya-04 |
| 1574 | 1 | demanding toward | `(LLM tail)` | Rorge → Everyone | acok-arya-04 |
| 1575 | 1 | loyal to Yoren until overwhelmed | `SERVES` | Koss → Yoren | acok-arya-04 |
| 1576 | 1 | loyal fighter | `(LLM tail)` | Dobber → Yoren | acok-arya-04 |
| 1577 | 1 | Leads/protects | `COMMANDS` | Arya → The group | acok-arya-05 |
| 1578 | 1 | Respects/values | `RESPECTS` | Gendry → Arya | acok-arya-05 |
| 1579 | 1 | Newly deferential toward | `(LLM tail)` | Gendry → Arya | acok-arya-05 |
| 1580 | 1 | Advocates yielding | `(LLM tail)` | Lommy → Everyone | acok-arya-05 |
| 1581 | 1 | Cherishes | `(LLM tail)` | Arya → Needle | acok-arya-05 |
| 1582 | 1 | Clings to | `(LLM tail)` | Weasel → Arya | acok-arya-05 |
| 1583 | 1 | admires/mourns | `MOURNS` | Arya → Syrio Forel | acok-arya-06 |
| 1584 | 1 | stole Needle from | `(LLM tail)` | Polliver → Arya | acok-arya-06 |
| 1585 | 1 | took horned helm from | `(LLM tail)` | Dunsen → Gendry | acok-arya-06 |
| 1586 | 1 | serves as interrogator for | `SERVES` | The Tickler → Ser Gregor | acok-arya-06 |
| 1587 | 1 | supervises with | `(LLM tail)` | Goodwife Amabel → Goodwife Harra | acok-arya-06 |
| 1588 | 1 | assigns Arya to | `(LLM tail)` | Goodwife Amabel → Weese | acok-arya-06 |
| 1589 | 1 | understeward of | `(LLM tail)` | Weese → Wailing Tower | acok-arya-06 |
| 1590 | 1 | accompanied by | `(LLM tail)` | Lord Beric Dondarrion → Red priest (unnamed) | acok-arya-06 |
| 1591 | 1 | disguised as servant to | `DISGUISED_AS` | Arya → Weese | acok-arya-07 |
| 1592 | 1 | tries to help | `(LLM tail)` | Hot Pie → Arya | acok-arya-07 |
| 1593 | 1 | brutal master to | `(LLM tail)` | Weese → Arya | acok-arya-07 |
| 1594 | 1 | forced reconciliation with | `(LLM tail)` | Vargo Hoat → Ser Harys Swyft | acok-arya-07 |
| 1595 | 1 | owes debt to | `(LLM tail)` | Jaqen H'ghar → Arya | acok-arya-07 |
| 1596 | 1 | kills for | `KILLS` | Jaqen H'ghar → Arya | acok-arya-07 |
| 1597 | 1 | dispenses justice over | `(LLM tail)` | Lord Tywin → Lannister host | acok-arya-07 |
| 1598 | 1 | Fears / hates | `FEARS` | Arya → Weese | acok-arya-08 |
| 1599 | 1 | Relies on / commands | `COMMANDS` | Arya → Jaqen H'ghar | acok-arya-08 |
| 1600 | 1 | Protective alliance with | `ALLIES_WITH` | Arya → Gendry | acok-arya-08 |
| 1601 | 1 | Identifies with | `(LLM tail)` | Arya → Robb Stark | acok-arya-08 |
| 1602 | 1 | Threatens / fears | `OPPOSES` | Rorge → Arya / Jaqen | acok-arya-08 |
| 1603 | 1 | Dominates / abuses | `(LLM tail)` | Weese → Arya | acok-arya-08 |
| 1604 | 1 | Has bed-companion | `COMPANION_OF` | Weese → Unnamed woman | acok-arya-08 |
| 1605 | 1 | Commands van for | `COMMANDS` | Ser Gregor Clegane → Lord Tywin | acok-arya-08 |
| 1606 | 1 | Mutual hatred with | `(LLM tail)` | Vargo Hoat → Ser Amory Lorch | acok-arya-08 |
| 1607 | 1 | protects identity from | `PROTECTS` | Arya → Rorge, Biter, Glover | acok-arya-09 |
| 1608 | 1 | coerces/manipulates | `(LLM tail)` | Arya → Jaqen H'ghar | acok-arya-09 |
| 1609 | 1 | conflicted friendship with | `COMPANION_OF` | Arya → Jaqen H'ghar | acok-arya-09 |
| 1610 | 1 | frustrated alliance with | `ALLIES_WITH` | Arya → Gendry | acok-arya-09 |
| 1611 | 1 | mocks class distance with | `OPPOSES` | Gendry → Arya | acok-arya-09 |
| 1612 | 1 | bound by oath to | `(LLM tail)` | Jaqen H'ghar → Arya | acok-arya-09 |
| 1613 | 1 | gives gift/instruction to | `(LLM tail)` | Jaqen H'ghar → Arya | acok-arya-09 |
| 1614 | 1 | switches allegiance to | `(LLM tail)` | Vargo Hoat → Roose Bolton | acok-arya-09 |
| 1615 | 1 | executes/punishes | `EXECUTES` | Roose Bolton → Ser Amory Lorch | acok-arya-09 |
| 1616 | 1 | supervised by | `(LLM tail)` | Arya → Pinkeye (Mebble) | acok-arya-09 |
| 1617 | 1 | feels homesick for | `(LLM tail)` | Arya → Winterfell | acok-arya-09 |
| 1618 | 1 | feels fear toward | `FEARS` | Arya → Jaqen (as wizard) | acok-arya-09 |
| 1619 | 1 | mentions as master | `(LLM tail)` | Gendry → Lucan | acok-arya-09 |
| 1620 | 1 | long service to | `(LLM tail)` | Ben Blackthumb → Harrenhal (multiple lords) | acok-arya-09 |
| 1621 | 1 | resents/angry at | `RESENTS` | Arya → Gendry | acok-arya-10 |
| 1622 | 1 | follows/trusts | `(LLM tail)` | Gendry → Arya | acok-arya-10 |
| 1623 | 1 | leads (poorly) | `COMMANDS` | Ser Aenys Frey → Frey forces | acok-arya-10 |
| 1624 | 1 | pressure | `(LLM tail)` | Frey lords → Roose Bolton | acok-arya-10 |
| 1625 | 1 | loyal to (nominally) | `SERVES` | Roose Bolton → Robb Stark | acok-arya-10 |
| 1626 | 1 | betrothed to (broken) | `BETROTHED_TO` | Elmar Frey → A princess (unnamed) | acok-arya-10 |
| 1627 | 1 | serves as squire to | `SERVES` | Elmar Frey → Roose Bolton | acok-arya-10 |
| 1628 | 1 | mourns/is crazed over | `MOURNS` | Goodwife Amabel → Goodwife Harra | acok-arya-10 |
| 1629 | 1 | intimidates | `(LLM tail)` | Rorge → Arya | acok-arya-10 |
| 1630 | 1 | will give Harrenhal to | `(LLM tail)` | Bolton → Vargo Hoat | acok-arya-10 |
| 1631 | 1 | sends to destruction (inferred) | `(LLM tail)` | Bolton → Tallhart and Glover | acok-arya-10 |
| 1632 | 1 | castellan appointed by | `(LLM tail)` | Ser Rodrik Cassel → Catelyn Stark | acok-bran-01 |
| 1633 | 1 | resents / jealous of | `RESENTS` | Bran Stark → The Walders | acok-bran-01 |
| 1634 | 1 | resents being corrected by | `RESENTS` | Bran Stark → Maester Luwin | acok-bran-01 |
| 1635 | 1 | storyteller to | `(LLM tail)` | Old Nan → Bran Stark | acok-bran-01 |
| 1636 | 1 | pack bond with | `(LLM tail)` | Summer → Shaggydog | acok-bran-01 |
| 1637 | 1 | feels displaced by | `(LLM tail)` | Bran Stark → The Walders taking Jon's room | acok-bran-01 |
| 1638 | 1 | ward/dependent | `(LLM tail)` | Bran → Hodor | acok-bran-02 |
| 1639 | 1 | bullies | `(LLM tail)` | Little Walder → Hodor | acok-bran-02 |
| 1640 | 1 | vassal to | `(LLM tail)` | Lord Manderly → Robb Stark | acok-bran-02 |
| 1641 | 1 | protective/advisory toward | `(LLM tail)` | Osha → Bran | acok-bran-02 |
| 1642 | 1 | Acting lord / representative of | `(LLM tail)` | Bran → Robb Stark | acok-bran-03 |
| 1643 | 1 | Looks up to / misses | `MOURNS` | Bran → Lord Eddard | acok-bran-03 |
| 1644 | 1 | Defiant attachment to | `(LLM tail)` | Rickon → Catelyn Stark | acok-bran-03 |
| 1645 | 1 | Mentor/advisor to | `TUTORS` | Ser Rodrik → Bran | acok-bran-03 |
| 1646 | 1 | Servant/carrier of | `(LLM tail)` | Hodor → Bran | acok-bran-03 |
| 1647 | 1 | Reluctant tolerance of | `(LLM tail)` | Bran → Little Walder and Big Walder | acok-bran-03 |
| 1648 | 1 | Great friend to | `(LLM tail)` | Howland Reed → Lord Eddard Stark | acok-bran-03 |
| 1649 | 1 | Sworn fealty to | `(LLM tail)` | Meera and Jojen → House Stark / Bran | acok-bran-03 |
| 1650 | 1 | Generous guest to | `(LLM tail)` | Lord Wyman Manderly → Winterfell | acok-bran-03 |
| 1651 | 1 | Grief/isolation | `MOURNS` | Lady Hornwood → (general) | acok-bran-03 |
| 1652 | 1 | Camaraderie with | `COMPANION_OF` | Hother Umber → Mors Umber | acok-bran-03 |
| 1653 | 1 | Supernatural awareness of | `(LLM tail)` | Jojen → Summer | acok-bran-03 |
| 1654 | 1 | friendship/affection | `LOVES` | Bran → Meera Reed | acok-bran-04 |
| 1655 | 1 | uneasy interaction | `(LLM tail)` | Bran → Jojen Reed | acok-bran-04 |
| 1656 | 1 | mission toward | `(LLM tail)` | Jojen → Bran | acok-bran-04 |
| 1657 | 1 | authority over / tutors | `COMMANDS` | Maester Luwin → Bran | acok-bran-04 |
| 1658 | 1 | compares to Arya | `(LLM tail)` | Bran → Meera Reed | acok-bran-04 |
| 1659 | 1 | pack bond | `(LLM tail)` | Summer → Shaggydog | acok-bran-04 |
| 1660 | 1 | sent children to fulfill green dream | `(LLM tail)` | Howland Reed → Bran/Winterfell | acok-bran-04 |
| 1661 | 1 | relied on counsel of | `ADVISES` | Eddard Stark → Maester Luwin | acok-bran-04 |
| 1662 | 1 | angry with | `(LLM tail)` | Ser Rodrik → Bolton's bastard / Lord Manderly | acok-bran-04 |
| 1663 | 1 | seized/married | `(LLM tail)` | Bolton's bastard → Lady Hornwood | acok-bran-04 |
| 1664 | 1 | took castle of | `(LLM tail)` | Lord Manderly → Lady Hornwood | acok-bran-04 |
| 1665 | 1 | mentors/teaches | `TUTORS` | Jojen Reed → Bran | acok-bran-05 |
| 1666 | 1 | callous/ambitious | `(LLM tail)` | Big Walder Frey → Ser Stevron Frey | acok-bran-05 |
| 1667 | 1 | denial about | `(LLM tail)` | Rickon Stark → Eddard Stark | acok-bran-05 |
| 1668 | 1 | disturbed by | `(LLM tail)` | Bran → Both Walders | acok-bran-05 |
| 1669 | 1 | serves/carries | `SERVES` | Osha → Bran | acok-bran-05 |
| 1670 | 1 | abused/murdered | `KILLS` | Bastard of Bolton → Lady Hornwood | acok-bran-05 |
| 1671 | 1 | fighting | `(LLM tail)` | Manderly knights → Dreadfort men | acok-bran-05 |
| 1672 | 1 | may claim | `(LLM tail)` | Roose Bolton → Hornwood lands | acok-bran-05 |
| 1673 | 1 | Pack brother of | `SIBLING_OF` | Summer → Shaggydog | acok-bran-06 |
| 1674 | 1 | Captures / conquers | `CAPTURES` | Theon → Winterfell / Bran | acok-bran-06 |
| 1675 | 1 | Claims wardship over | `(LLM tail)` | Theon → Bran, Rickon | acok-bran-06 |
| 1676 | 1 | Yields to (under duress) | `(LLM tail)` | Bran → Theon | acok-bran-06 |
| 1677 | 1 | Critical of (retrospective) | `(LLM tail)` | Maester Luwin → Theon | acok-bran-06 |
| 1678 | 1 | Self-blaming | `(LLM tail)` | Maester Luwin → Himself | acok-bran-06 |
| 1679 | 1 | Wants | `(LLM tail)` | Rickon → Catelyn Stark | acok-bran-06 |
| 1680 | 1 | Foresaw this event | `(LLM tail)` | Jojen → The ironborn attack | acok-bran-06 |
| 1681 | 1 | Overpowers | `(LLM tail)` | Osha → Stygg | acok-bran-06 |
| 1682 | 1 | wargs into / spiritually bonded with | `WARGS_INTO` | Bran → Summer | acok-bran-07 |
| 1683 | 1 | submits to | `(LLM tail)` | Shaggydog → Summer | acok-bran-07 |
| 1684 | 1 | protects/comforts | `PROTECTS` | Meera → Bran | acok-bran-07 |
| 1685 | 1 | leads/makes tactical decisions for | `COMMANDS` | Osha → The group | acok-bran-07 |
| 1686 | 1 | final counsel to | `ADVISES` | Maester Luwin → Bran | acok-bran-07 |
| 1687 | 1 | clings to / dependent on | `(LLM tail)` | Rickon → Hodor | acok-bran-07 |
| 1688 | 1 | takes charge of | `(LLM tail)` | Osha → Rickon | acok-bran-07 |
| 1689 | 1 | identifies as | `(LLM tail)` | Bran → Winterfell | acok-bran-07 |
| 1690 | 1 | mercy toward | `(LLM tail)` | Osha → Maester Luwin | acok-bran-07 |
| 1691 | 1 | recalls connection with | `(LLM tail)` | Bran → Jon Snow | acok-bran-07 |
| 1692 | 1 | second son of | `(LLM tail)` | Ser Emmon Frey → Lord Walder Frey | acok-catelyn-01 |
| 1693 | 1 | speaks for | `(LLM tail)` | Edmure Tully → Hoster Tully / Riverrun | acok-catelyn-01 |
| 1694 | 1 | captain of guard for | `(LLM tail)` | Ser Robin Ryger → House Tully | acok-catelyn-01 |
| 1695 | 1 | ward/companion of | `COMPANION_OF` | Theon Greyjoy → Robb Stark | acok-catelyn-01 |
| 1696 | 1 | serves as catspaw of | `SERVES` | Gregor Clegane → Lord Tywin Lannister | acok-catelyn-01 |
| 1697 | 1 | raids | `(LLM tail)` | Lord Beric Dondarrion → Lord Tywin's forces | acok-catelyn-01 |
| 1698 | 1 | envoy/mother serving | `(LLM tail)` | Catelyn → Robb | acok-catelyn-02 |
| 1699 | 1 | married to (political alliance) | `ALLIES_WITH` | Renly → Margaery Tyrell | acok-catelyn-02 |
| 1700 | 1 | close with / shares confidences | `(LLM tail)` | Renly → Ser Loras Tyrell | acok-catelyn-02 |
| 1701 | 1 | devotion/love toward | `LOVES` | Brienne → Renly | acok-catelyn-02 |
| 1702 | 1 | offered alliance to (rejected) | `ALLIES_WITH` | Renly → Ned Stark | acok-catelyn-02 |
| 1703 | 1 | dismisses claim of | `(LLM tail)` | Renly → Stannis | acok-catelyn-02 |
| 1704 | 1 | demands fealty from | `(LLM tail)` | Renly → Robb | acok-catelyn-02 |
| 1705 | 1 | is guarded toward | `(LLM tail)` | Catelyn → Renly | acok-catelyn-02 |
| 1706 | 1 | loyal to / escorts | `SERVES` | Ser Wendel Manderly → Catelyn | acok-catelyn-02 |
| 1707 | 1 | besieges | `(LLM tail)` | Stannis → Storm's End (Renly's garrison) | acok-catelyn-02 |
| 1708 | 1 | Bitter rivalry / refuses to yield | `RESENTS` | Stannis → Renly | acok-catelyn-03 |
| 1709 | 1 | Contempt and dismissal | `HATES` | Renly → Stannis | acok-catelyn-03 |
| 1710 | 1 | Failed diplomatic effort | `(LLM tail)` | Catelyn → Stannis and Renly | acok-catelyn-03 |
| 1711 | 1 | Reliance on / closeness with | `(LLM tail)` | Renly → Ser Loras | acok-catelyn-03 |
| 1712 | 1 | Brought suspicions to | `(LLM tail)` | Stannis → Jon Arryn | acok-catelyn-03 |
| 1713 | 1 | Loyalty to / envoy for | `SERVES` | Catelyn → Robb Stark | acok-catelyn-03 |
| 1714 | 1 | Mourning / longing for | `MOURNS` | Catelyn → Eddard Stark | acok-catelyn-03 |
| 1715 | 1 | Anxiety for | `(LLM tail)` | Catelyn → Sansa, Arya | acok-catelyn-03 |
| 1716 | 1 | Longing for / duty toward | `(LLM tail)` | Catelyn → Her dying father (unnamed) | acok-catelyn-03 |
| 1717 | 1 | Second son / independence from | `(LLM tail)` | Ser Robar Royce → Bronze Yohn Royce | acok-catelyn-03 |
| 1718 | 1 | Military counsel | `ADVISES` | Lord Randyll Tarly → Renly | acok-catelyn-03 |
| 1719 | 1 | Strategic counsel (overruled) | `ADVISES` | Lord Mathis Rowan → Renly | acok-catelyn-03 |
| 1720 | 1 | Mockery of | `(LLM tail)` | Renly → Stannis's wife and daughter | acok-catelyn-03 |
| 1721 | 1 | Mother, grieving separation | `MOURNS` | Catelyn → Robb, Bran, Rickon, Arya, Sansa | acok-catelyn-04 |
| 1722 | 1 | Widow, mourning | `MOURNS` | Catelyn → Eddard Stark | acok-catelyn-04 |
| 1723 | 1 | Daughter, worried | `(LLM tail)` | Catelyn → Hoster Tully | acok-catelyn-04 |
| 1724 | 1 | Daughter, remembering | `(LLM tail)` | Catelyn → Lady Minisa Tully | acok-catelyn-04 |
| 1725 | 1 | Protective ally | `ALLIES_WITH` | Catelyn → Brienne | acok-catelyn-04 |
| 1726 | 1 | Obedient service (new) | `(LLM tail)` | Brienne → Catelyn | acok-catelyn-04 |
| 1727 | 1 | Younger brother, rival | `SIBLING_OF` | Renly → Stannis | acok-catelyn-04 |
| 1728 | 1 | Values/respects | `RESPECTS` | Renly → Barristan Selmy | acok-catelyn-04 |
| 1729 | 1 | Hostile / accusatory | `(LLM tail)` | Ser Emmon Cuy → Brienne | acok-catelyn-04 |
| 1730 | 1 | Advisor, urges aggression | `(LLM tail)` | Lord Rowan → Renly | acok-catelyn-04 |
| 1731 | 1 | Tactical advisor | `(LLM tail)` | Randyll Tarly → Renly | acok-catelyn-04 |
| 1732 | 1 | Political envoy | `(LLM tail)` | Catelyn → Renly | acok-catelyn-04 |
| 1733 | 1 | Suspects / blames | `(LLM tail)` | Catelyn → Cersei Lannister | acok-catelyn-04 |
| 1734 | 1 | Accepts service of | `(LLM tail)` | Catelyn → Brienne | acok-catelyn-05 |
| 1735 | 1 | Wants to kill | `(LLM tail)` | Brienne → Stannis | acok-catelyn-05 |
| 1736 | 1 | Concerned for / authority over | `(LLM tail)` | Catelyn → Edmure | acok-catelyn-05 |
| 1737 | 1 | Bristles at / defers to | `(LLM tail)` | Edmure → Catelyn | acok-catelyn-05 |
| 1738 | 1 | Wishes for guidance from | `(LLM tail)` | Catelyn → Brynden Tully | acok-catelyn-05 |
| 1739 | 1 | Grieves for / tends to | `MOURNS` | Catelyn → Lord Hoster | acok-catelyn-05 |
| 1740 | 1 | Confuses with Lysa / guilt toward | `(LLM tail)` | Lord Hoster → Catelyn (as Lysa) | acok-catelyn-05 |
| 1741 | 1 | Harbors rage toward | `(LLM tail)` | Catelyn → Cersei Lannister | acok-catelyn-05 |
| 1742 | 1 | Wary respect toward | `RESPECTS` | Catelyn → Tyrion Lannister | acok-catelyn-05 |
| 1743 | 1 | Ambivalence toward | `(LLM tail)` | Catelyn → Jon Snow | acok-catelyn-05 |
| 1744 | 1 | Half-brother to | `SIBLING_OF` | Martyn Rivers → Ser Perwyn Frey | acok-catelyn-05 |
| 1745 | 1 | sister/loving concern | `SIBLING_OF` | Catelyn → Edmure | acok-catelyn-06 |
| 1746 | 1 | mother/worried | `(LLM tail)` | Catelyn → Robb | acok-catelyn-06 |
| 1747 | 1 | dutiful daughter | `(LLM tail)` | Catelyn → Lord Hoster | acok-catelyn-06 |
| 1748 | 1 | seeks approval from | `SEEKS` | Edmure → Lord Hoster | acok-catelyn-06 |
| 1749 | 1 | unrequited devotion to | `(LLM tail)` | Brienne → Renly | acok-catelyn-06 |
| 1750 | 1 | interrogates/distrusts | `(LLM tail)` | Catelyn → Ser Cleos Frey | acok-catelyn-06 |
| 1751 | 1 | dutiful marriage (past) | `(LLM tail)` | Catelyn → Ned Stark | acok-catelyn-06 |
| 1752 | 1 | prior betrothal (past) | `BETROTHED_TO` | Catelyn → Brandon Stark | acok-catelyn-06 |
| 1753 | 1 | resentment/coldness (past) | `RESENTS` | Catelyn → Petyr Baelish | acok-catelyn-06 |
| 1754 | 1 | complex resentment | `(LLM tail)` | Catelyn → Jon Snow | acok-catelyn-06 |
| 1755 | 1 | distrusts/blames | `DISTRUSTS` | Catelyn → Tyrion Lannister | acok-catelyn-06 |
| 1756 | 1 | grudging acknowledgment | `(LLM tail)` | Catelyn → Tyrion Lannister | acok-catelyn-06 |
| 1757 | 1 | cold indifference | `(LLM tail)` | Roose Bolton → Ramsay Bolton | acok-catelyn-06 |
| 1758 | 1 | calculating obedience | `(LLM tail)` | Roose Bolton → Robb Stark | acok-catelyn-06 |
| 1759 | 1 | military trust | `(LLM tail)` | Edmure → Lord Jason Mallister | acok-catelyn-06 |
| 1760 | 1 | longing for counsel | `ADVISES` | Catelyn → Septon Osmynd | acok-catelyn-06 |
| 1761 | 1 | awed memory of | `(LLM tail)` | Brienne → A singer from across the narrow sea | acok-catelyn-06 |
| 1762 | 1 | loyalty/enthusiasm | `(LLM tail)` | Ser Desmond → Edmure | acok-catelyn-06 |
| 1763 | 1 | mother of (grieving) | `PARENT_OF` | Catelyn → Bran, Rickon | acok-catelyn-07 |
| 1764 | 1 | mother of (fearful for) | `PARENT_OF` | Catelyn → Sansa, Arya | acok-catelyn-07 |
| 1765 | 1 | sworn lady to | `(LLM tail)` | Catelyn → Brienne | acok-catelyn-07 |
| 1766 | 1 | daughter of (devoted) | `PARENT_OF` | Catelyn → Lord Hoster | acok-catelyn-07 |
| 1767 | 1 | captor of (adversarial) | `CAPTURES` | Catelyn → Jaime Lannister | acok-catelyn-07 |
| 1768 | 1 | attempted killer of | `(LLM tail)` | Jaime → Bran Stark | acok-catelyn-07 |
| 1769 | 1 | brother of (protective) | `SIBLING_OF` | Jaime → Tyrion | acok-catelyn-07 |
| 1770 | 1 | formerly served (conflicted) | `SERVES` | Jaime → Aerys Targaryen | acok-catelyn-07 |
| 1771 | 1 | served under | `(LLM tail)` | Jaime → Gerold Hightower | acok-catelyn-07 |
| 1772 | 1 | rival/enemy of | `(LLM tail)` | Jaime → Robb Stark | acok-catelyn-07 |
| 1773 | 1 | distrusts/reassesses | `DISTRUSTS` | Catelyn → Petyr Baelish | acok-catelyn-07 |
| 1774 | 1 | betrayer of | `(LLM tail)` | Theon Greyjoy → Stark family | acok-catelyn-07 |
| 1775 | 1 | father of (remembered) | `PARENT_OF` | Lord Hoster → Brandon Stark (opinion) | acok-catelyn-07 |
| 1776 | 1 | king/lord of | `(LLM tail)` | Robb → Rickard Karstark's loyalty | acok-catelyn-07 |
| 1777 | 1 | Named first of Queensguard | `(LLM tail)` | Daenerys → Ser Jorah | acok-daenerys-01 |
| 1778 | 1 | Loves romantically | `LOVES` | Ser Jorah → Daenerys | acok-daenerys-01 |
| 1779 | 1 | Conflicted love/hate for | `LOVES` | Ser Jorah → Lynesse Hightower | acok-daenerys-01 |
| 1780 | 1 | Fled justice of | `(LLM tail)` | Ser Jorah → Eddard Stark | acok-daenerys-01 |
| 1781 | 1 | Won tourney, defeated | `(LLM tail)` | Ser Jorah → Jaime Lannister | acok-daenerys-01 |
| 1782 | 1 | Chief concubine to | `(LLM tail)` | Lynesse Hightower → Tregar Ormollen | acok-daenerys-01 |
| 1783 | 1 | Grateful to / remembers | `(LLM tail)` | Daenerys → Doreah | acok-daenerys-01 |
| 1784 | 1 | Took the black | `(LLM tail)` | Jorah's father → Night's Watch | acok-daenerys-01 |
| 1785 | 1 | Hosts | `(LLM tail)` | Xaro Xhoan Daxos → Daenerys | acok-daenerys-02 |
| 1786 | 1 | Courts/seeks to influence | `(LLM tail)` | Pyat Pree → Daenerys | acok-daenerys-02 |
| 1787 | 1 | Trusts but cannot fully love | `TRUSTS` | Daenerys → Ser Jorah | acok-daenerys-02 |
| 1788 | 1 | Distrusts sorcery because of | `DISTRUSTS` | Daenerys → Mirri Maz Duur | acok-daenerys-02 |
| 1789 | 1 | Views as enemy (dead) | `(LLM tail)` | Daenerys → Robert Baratheon | acok-daenerys-02 |
| 1790 | 1 | Views as traitor | `(LLM tail)` | Daenerys → Eddard Stark | acok-daenerys-02 |
| 1791 | 1 | Scorns/pities | `(LLM tail)` | Daenerys → Viserys | acok-daenerys-02 |
| 1792 | 1 | Compares Dany favorably to | `(LLM tail)` | Ser Jorah → Rhaegar | acok-daenerys-02 |
| 1793 | 1 | Awed by | `(LLM tail)` | Quhuru Mo → Daenerys / Dragons | acok-daenerys-02 |
| 1794 | 1 | Call Qartheen | `(LLM tail)` | Dothraki → "Milk Men" | acok-daenerys-02 |
| 1795 | 1 | Views Jorah as having dual perception of her | `(LLM tail)` | Daenerys → Ser Jorah | acok-daenerys-02 |
| 1796 | 1 | courts/uses | `(LLM tail)` | Xaro Xhoan Daxos → Daenerys | acok-daenerys-03 |
| 1797 | 1 | advises/protects | `ADVISES` | Ser Jorah → Daenerys | acok-daenerys-03 |
| 1798 | 1 | sold/arranged marriage of | `(LLM tail)` | Illyrio Mopatis → Daenerys | acok-daenerys-03 |
| 1799 | 1 | loyal to (past) | `SERVES` | Lord Redwyne → Aerys Targaryen (Dany's father) | acok-daenerys-03 |
| 1800 | 1 | Protective advisor | `(LLM tail)` | Ser Jorah → Daenerys | acok-daenerys-04 |
| 1801 | 1 | Patron/suitor | `(LLM tail)` | Xaro Xhoan Daxos → Daenerys | acok-daenerys-04 |
| 1802 | 1 | Guide then antagonist | `(LLM tail)` | Pyat Pree → Daenerys | acok-daenerys-04 |
| 1803 | 1 | Bonded protector | `BONDED_TO` | Drogon → Daenerys | acok-daenerys-04 |
| 1804 | 1 | Longing/mourning | `MOURNS` | Daenerys → Ser Willem Darry | acok-daenerys-04 |
| 1805 | 1 | Memory/longing | `(LLM tail)` | Daenerys → House with the red door | acok-daenerys-04 |
| 1806 | 1 | Distrust/hostility | `DISTRUSTS` | Ser Jorah → Xaro Xhoan Daxos | acok-daenerys-04 |
| 1807 | 1 | Predatory/parasitic | `(LLM tail)` | The Undying → Daenerys | acok-daenerys-04 |
| 1808 | 1 | Deceptive | `(LLM tail)` | Illusory wizards → Daenerys | acok-daenerys-04 |
| 1809 | 1 | Hostile toward / attacks | `OPPOSES` | Pyat Pree → Daenerys | acok-daenerys-04 |
| 1810 | 1 | advised by/protected by | `(LLM tail)` | Daenerys → Ser Jorah | acok-daenerys-05 |
| 1811 | 1 | refuses/distrusts | `(LLM tail)` | Daenerys → Xaro Xhoan Daxos | acok-daenerys-05 |
| 1812 | 1 | expelled/rejected | `(LLM tail)` | Xaro Xhoan Daxos → Daenerys | acok-daenerys-05 |
| 1813 | 1 | rescued by | `RESCUES` | Daenerys → Arstan Whitebeard | acok-daenerys-05 |
| 1814 | 1 | recognizes | `(LLM tail)` | Arstan Whitebeard → Ser Jorah | acok-daenerys-05 |
| 1815 | 1 | named to | `(LLM tail)` | Ser Jorah → Queensguard | acok-daenerys-05 |
| 1816 | 1 | squired by | `(LLM tail)` | Strong Belwas → Arstan Whitebeard | acok-daenerys-05 |
| 1817 | 1 | attempted assassination | `(LLM tail)` | Sorrowful Men → Daenerys | acok-daenerys-05 |
| 1818 | 1 | Loyal vassal of | `(LLM tail)` | Davos → Stannis Baratheon | acok-davos-01 |
| 1819 | 1 | Old acquaintance of | `(LLM tail)` | Davos → Salladhor Saan | acok-davos-01 |
| 1820 | 1 | Raised to knighthood | `(LLM tail)` | Stannis → Davos | acok-davos-01 |
| 1821 | 1 | Uses / relies on | `(LLM tail)` | Stannis → Melisandre | acok-davos-01 |
| 1822 | 1 | Grief for / resentment toward | `MOURNS` | Stannis → His parents (Steffon, Cassana) | acok-davos-01 |
| 1823 | 1 | Devout follower of | `(LLM tail)` | Queen Selyse → Melisandre / R'hllor | acok-davos-01 |
| 1824 | 1 | Mercenary ally of | `ALLIES_WITH` | Salladhor Saan → Stannis | acok-davos-01 |
| 1825 | 1 | Skeptic toward | `(LLM tail)` | Salladhor Saan → Stannis / Lightbringer | acok-davos-01 |
| 1826 | 1 | Priestess serving | `(LLM tail)` | Melisandre → Stannis | acok-davos-01 |
| 1827 | 1 | Opposed by (privately) | `(LLM tail)` | Melisandre → Davos | acok-davos-01 |
| 1828 | 1 | Serves as maester to | `SERVES` | Maester Pylos → Stannis | acok-davos-01 |
| 1829 | 1 | Ancestor provided brides to | `(LLM tail)` | Lord Velaryon → Targaryen princes | acok-davos-01 |
| 1830 | 1 | Scorns | `(LLM tail)` | Allard → The burning of the Seven | acok-davos-01 |
| 1831 | 1 | Withdrew support from | `(LLM tail)` | Guncer Sunglass → Stannis | acok-davos-01 |
| 1832 | 1 | Defended the sept against | `(LLM tail)` | Ser Hubard Rambton → The queen's men | acok-davos-01 |
| 1833 | 1 | Declared for | `(LLM tail)` | House Florent → Renly | acok-davos-01 |
| 1834 | 1 | Loyal service; truthful counsel | `SERVES` | Davos → Stannis | acok-davos-02 |
| 1835 | 1 | Trusts and values | `TRUSTS` | Stannis → Davos | acok-davos-02 |
| 1836 | 1 | Depends on / follows visions of | `(LLM tail)` | Stannis → Melisandre | acok-davos-02 |
| 1837 | 1 | Fears and distrusts | `FEARS` | Davos → Melisandre | acok-davos-02 |
| 1838 | 1 | Grudging dependence on | `(LLM tail)` | Stannis → His bannermen lords | acok-davos-02 |
| 1839 | 1 | Defends/protects | `PROTECTS` | Ser Cortnay Penrose → Edric Storm | acok-davos-02 |
| 1840 | 1 | Grief/love for | `MOURNS` | Stannis → Renly Baratheon | acok-davos-02 |
| 1841 | 1 | Foremost supporter of | `(LLM tail)` | Lord Alester Florent → Stannis | acok-davos-02 |
| 1842 | 1 | Kinsman of | `(LLM tail)` | Lord Alester Florent → Edric Storm | acok-davos-02 |
| 1843 | 1 | Maternal grandfather of | `PARENT_OF` | Lord Estermont → Stannis | acok-davos-02 |
| 1844 | 1 | Knew from childhood | `(LLM tail)` | Penrose → Brienne | acok-davos-02 |
| 1845 | 1 | Lieutenant to | `(LLM tail)` | Lord Meadows → Ser Cortnay Penrose | acok-davos-02 |
| 1846 | 1 | Suspects treachery from | `(LLM tail)` | Stannis → Cersei Lannister | acok-davos-02 |
| 1847 | 1 | Displeased with | `(LLM tail)` | Salladhor Saan → Ser Imry / Stannis | acok-davos-03 |
| 1848 | 1 | Respects (grudgingly) | `RESPECTS` | Davos → Salladhor Saan | acok-davos-03 |
| 1849 | 1 | Eager for glory | `(LLM tail)` | Allard → (self) | acok-davos-03 |
| 1850 | 1 | Friendship/brotherhood | `COMPANION_OF` | Jon Snow → Samwell Tarly | acok-jon-01 |
| 1851 | 1 | Loyalty/conflicted bond to | `(LLM tail)` | Jon Snow → Robb Stark | acok-jon-01 |
| 1852 | 1 | Uncle/nephew bond with | `NEPHEW_OF` | Jon Snow → Benjen Stark | acok-jon-01 |
| 1853 | 1 | Chose vows over | `(LLM tail)` | Maester Aemon → The Iron Throne | acok-jon-01 |
| 1854 | 1 | Father who made Sam unsafe | `(LLM tail)` | Sam's father (Randyll Tarly) → Samwell Tarly | acok-jon-01 |
| 1855 | 1 | Remembers/dreams of | `(LLM tail)` | Jon Snow → Othor (wight) | acok-jon-01 |
| 1856 | 1 | Unspoken pact | `(LLM tail)` | Night's Watch → Members | acok-jon-01 |
| 1857 | 1 | Steward/serves | `(LLM tail)` | Jon Snow → Jeor Mormont | acok-jon-02 |
| 1858 | 1 | Remembers/misses | `MOURNS` | Jon Snow → Arya Stark | acok-jon-02 |
| 1859 | 1 | Growing confidence | `(LLM tail)` | Samwell Tarly → Self | acok-jon-02 |
| 1860 | 1 | Companionable pessimism | `(LLM tail)` | Dolorous Edd → Jon Snow | acok-jon-02 |
| 1861 | 1 | Unease about | `(LLM tail)` | Dywen → The forest | acok-jon-02 |
| 1862 | 1 | Steward/squire serving | `(LLM tail)` | Jon Snow → Lord Commander Mormont | acok-jon-03 |
| 1863 | 1 | Friendship/protectiveness | `COMPANION_OF` | Jon Snow → Samwell Tarly | acok-jon-03 |
| 1864 | 1 | Resentful hostility from | `RESENTS` | Jon Snow → Chett | acok-jon-03 |
| 1865 | 1 | Mockery from | `(LLM tail)` | Jon Snow → Lark the Sisterman | acok-jon-03 |
| 1866 | 1 | Warm camaraderie with | `COMPANION_OF` | Jon Snow → Dolorous Edd | acok-jon-03 |
| 1867 | 1 | Friendly familiarity with | `COMPANION_OF` | Jon Snow → Dywen | acok-jon-03 |
| 1868 | 1 | Distant affection for | `LOVES` | Jon Snow → Sansa and Arya | acok-jon-03 |
| 1869 | 1 | Moral connection to | `(LLM tail)` | Jon Snow → Ned Stark | acok-jon-03 |
| 1870 | 1 | Pragmatic tolerance of | `(LLM tail)` | Mormont → Craster | acok-jon-03 |
| 1871 | 1 | Domination over | `(LLM tail)` | Craster → His wives/daughters | acok-jon-03 |
| 1872 | 1 | Hostility/contempt toward | `(LLM tail)` | Craster → Night's Watch | acok-jon-03 |
| 1873 | 1 | Desperate appeal to | `(LLM tail)` | Gilly → Jon Snow | acok-jon-03 |
| 1874 | 1 | Sympathy/intervention for | `(LLM tail)` | Sam Tarly → Gilly | acok-jon-03 |
| 1875 | 1 | Vouches for | `(LLM tail)` | Thoren Smallwood → Craster | acok-jon-03 |
| 1876 | 1 | Former assignment to | `(LLM tail)` | Chett → Maester Aemon | acok-jon-03 |
| 1877 | 1 | Serves as steward to | `SERVES` | Jon Snow → Lord Commander Mormont | acok-jon-04 |
| 1878 | 1 | Bond/warging connection with | `WARGS_INTO` | Jon Snow → Ghost | acok-jon-04 |
| 1879 | 1 | Protective/warning behavior toward | `ADVISES` | Ghost → Jon Snow | acok-jon-04 |
| 1880 | 1 | Mentors / respects | `RESPECTS` | Lord Commander Mormont → Jon Snow | acok-jon-04 |
| 1881 | 1 | Dismissive/adversarial toward | `(LLM tail)` | Thoren Smallwood → Jon Snow | acok-jon-04 |
| 1882 | 1 | Chafes under command of | `COMMANDS` | Thoren Smallwood → Lord Commander Mormont | acok-jon-04 |
| 1883 | 1 | Concern/grief for | `MOURNS` | Jon Snow → Benjen Stark | acok-jon-04 |
| 1884 | 1 | Distrusts but uses | `DISTRUSTS` | Lord Commander Mormont → Craster | acok-jon-04 |
| 1885 | 1 | Gives food to / looks after | `(LLM tail)` | Jon Snow → Grenn | acok-jon-04 |
| 1886 | 1 | Recognizes lineage of | `(LLM tail)` | Qhorin Halfhand → Jon Snow | acok-jon-05 |
| 1887 | 1 | Chose for mission | `(LLM tail)` | Qhorin Halfhand → Jon Snow | acok-jon-05 |
| 1888 | 1 | Trusted advisor to | `(LLM tail)` | Qhorin Halfhand → Jeor Mormont | acok-jon-05 |
| 1889 | 1 | Comrade to | `(LLM tail)` | Jon Snow → Dolorous Edd | acok-jon-05 |
| 1890 | 1 | Hopes for return of | `(LLM tail)` | Jon Snow → Benjen Stark | acok-jon-05 |
| 1891 | 1 | Disloyal toward | `(LLM tail)` | Chett → Jeor Mormont | acok-jon-05 |
| 1892 | 1 | Fearful, possibly insubordinate | `FEARS` | Lark the Sisterman → Night's Watch leadership | acok-jon-05 |
| 1893 | 1 | Aggressive/confident attitude toward | `(LLM tail)` | Thoren Smallwood → Wildlings | acok-jon-05 |
| 1894 | 1 | Cautious toward | `(LLM tail)` | Jarman Buckwell → Wildling leaders | acok-jon-05 |
| 1895 | 1 | Fellow ranger / climbing partner | `(LLM tail)` | Jon Snow → Stonesnake | acok-jon-06 |
| 1896 | 1 | Thinks of / misses | `MOURNS` | Jon Snow → Bran Stark | acok-jon-06 |
| 1897 | 1 | Thinks of / association | `(LLM tail)` | Jon Snow → Arya Stark | acok-jon-06 |
| 1898 | 1 | Seeks information about | `SEEKS` | Jon Snow → Benjen Stark | acok-jon-06 |
| 1899 | 1 | Feared / recognized by | `(LLM tail)` | Qhorin Halfhand → Ygritte | acok-jon-06 |
| 1900 | 1 | Supports Qhorin's position on | `(LLM tail)` | Squire Dalbridge → Ygritte | acok-jon-06 |
| 1901 | 1 | Supports execution of | `(LLM tail)` | Ebben → Ygritte | acok-jon-06 |
| 1902 | 1 | Offers defection to | `(LLM tail)` | Ygritte → Jon Snow | acok-jon-06 |
| 1903 | 1 | Disobeys | `(LLM tail)` | Jon Snow → Qhorin Halfhand | acok-jon-06 |
| 1904 | 1 | Mentor/tests | `TUTORS` | Qhorin Halfhand → Jon Snow | acok-jon-07 |
| 1905 | 1 | Former friend/brother of | `SIBLING_OF` | Qhorin Halfhand → Mance Rayder | acok-jon-07 |
| 1906 | 1 | Connected to (dream communication) | `(LLM tail)` | Jon Snow → Bran (implied brother) | acok-jon-07 |
| 1907 | 1 | Felt kinship/empathy toward | `(LLM tail)` | Jon Snow → Ygritte | acok-jon-07 |
| 1908 | 1 | Respects/seeks approval from | `RESPECTS` | Jon Snow → Qhorin Halfhand | acok-jon-07 |
| 1909 | 1 | Aggressive/impatient temperament | `(LLM tail)` | Ebben → (general) | acok-jon-07 |
| 1910 | 1 | Deserted from | `(LLM tail)` | Mance Rayder → Night's Watch | acok-jon-07 |
| 1911 | 1 | Obeys/follows orders of | `SERVES` | Jon Snow → Qhorin Halfhand | acok-jon-08 |
| 1912 | 1 | Bonded to/fights for | `BONDED_TO` | Ghost → Jon Snow | acok-jon-08 |
| 1913 | 1 | Attacks (on Jon's behalf) | `ATTACKS` | Ghost → Qhorin Halfhand | acok-jon-08 |
| 1914 | 1 | Advocates for/protects | `(LLM tail)` | Ygritte → Jon Snow | acok-jon-08 |
| 1915 | 1 | Previously spared | `(LLM tail)` | Jon Snow → Ygritte | acok-jon-08 |
| 1916 | 1 | Hostile toward/distrusts | `OPPOSES` | Rattleshirt → Jon Snow | acok-jon-08 |
| 1917 | 1 | Rival/antagonistic toward | `(LLM tail)` | Rattleshirt → Qhorin Halfhand | acok-jon-08 |
| 1918 | 1 | Brotherhood/fraternity with | `(LLM tail)` | Qhorin Halfhand → Jon Snow | acok-jon-08 |
| 1919 | 1 | Mocks/challenges | `OPPOSES` | Ragwyle → Rattleshirt | acok-jon-08 |
| 1920 | 1 | Democratic/free | `(LLM tail)` | Wildlings (group) → Each other | acok-jon-08 |
| 1921 | 1 | Hates/tracks | `HATES` | Eagle (skinchanger) → Jon Snow | acok-jon-08 |
| 1922 | 1 | paternal love / failed guardian | `LOVES` | Cressen → Stannis | acok-prologue |
| 1923 | 1 | paternal love | `LOVES` | Cressen → Robert, Renly | acok-prologue |
| 1924 | 1 | protective compassion | `(LLM tail)` | Cressen → Shireen | acok-prologue |
| 1925 | 1 | hatred / opposition | `HATES` | Cressen → Melisandre | acok-prologue |
| 1926 | 1 | cold dismissal | `(LLM tail)` | Stannis → Cressen | acok-prologue |
| 1927 | 1 | cold duty / no affection | `LOVES` | Stannis → Selyse | acok-prologue |
| 1928 | 1 | devoted attachment | `(LLM tail)` | Shireen → Patchface | acok-prologue |
| 1929 | 1 | trust / affection | `LOVES` | Shireen → Cressen | acok-prologue |
| 1930 | 1 | compassion / respect | `RESPECTS` | Davos → Cressen | acok-prologue |
| 1931 | 1 | dismissive superiority | `(LLM tail)` | Melisandre → Cressen | acok-prologue |
| 1932 | 1 | drowned with | `(LLM tail)` | Lord Steffon → Lady Baratheon (wife) | acok-prologue |
| 1933 | 1 | bond | `(LLM tail)` | Patchface → Shireen | acok-prologue |
| 1934 | 1 | respectful but supplanting | `RESPECTS` | Pylos → Cressen | acok-prologue |
| 1935 | 1 | Captive of / fears | `PRISONER_OF` | Sansa → Joffrey | acok-sansa-01 |
| 1936 | 1 | Prefers among captors | `(LLM tail)` | Sansa → Ser Arys Oakheart | acok-sansa-01 |
| 1937 | 1 | Resents / fears | `RESENTS` | Sansa → Ser Boros (Blount) | acok-sansa-01 |
| 1938 | 1 | Fears / dislikes | `FEARS` | Sansa → Ser Meryn Trant | acok-sansa-01 |
| 1939 | 1 | Complex regard for | `(LLM tail)` | Sansa → Sandor Clegane | acok-sansa-01 |
| 1940 | 1 | Saves life of | `(LLM tail)` | Sansa → Ser Dontos | acok-sansa-01 |
| 1941 | 1 | Former love turned revulsion | `LOVES` | Sansa → Joffrey | acok-sansa-01 |
| 1942 | 1 | Mocking toward | `(LLM tail)` | Joffrey → Tommen | acok-sansa-01 |
| 1943 | 1 | Dismissive toward | `(LLM tail)` | Joffrey → Tyrion | acok-sansa-01 |
| 1944 | 1 | Protects (indirectly) | `PROTECTS` | Sandor Clegane → Sansa | acok-sansa-01 |
| 1945 | 1 | Excited to see | `(LLM tail)` | Tommen → Tyrion | acok-sansa-01 |
| 1946 | 1 | Commands / furious with | `COMMANDS` | Cersei → Tywin | acok-sansa-01 |
| 1947 | 1 | Unwilling captives of | `(LLM tail)` | Redwyne twins → The Crown / Cersei | acok-sansa-01 |
| 1948 | 1 | captive of / subject to | `PRISONER_OF` | Sansa Stark → Joffrey Baratheon | acok-sansa-02 |
| 1949 | 1 | beaten by (on Joffrey's orders) | `(LLM tail)` | Sansa Stark → Ser Meryn Trant | acok-sansa-02 |
| 1950 | 1 | surveilled by | `(LLM tail)` | Sansa Stark → Cersei Lannister | acok-sansa-02 |
| 1951 | 1 | entering secret alliance with | `ALLIES_WITH` | Sansa Stark → Ser Dontos Hollard | acok-sansa-02 |
| 1952 | 1 | protects / escorts | `PROTECTS` | Sandor Clegane → Sansa Stark | acok-sansa-02 |
| 1953 | 1 | mocks / threatens | `OPPOSES` | Sandor Clegane → Sansa Stark | acok-sansa-02 |
| 1954 | 1 | blames for Lady's death | `OPPOSES` | Sansa Stark → Arya Stark | acok-sansa-02 |
| 1955 | 1 | led sortie against | `(LLM tail)` | Joffrey Baratheon → Smallfolk mob | acok-sansa-02 |
| 1956 | 1 | sent to the Wall | `(LLM tail)` | Tyrion Lannister → Janos Slynt | acok-sansa-02 |
| 1957 | 1 | grandfather served | `PARENT_OF` | Sandor Clegane → Lord Tytos Lannister | acok-sansa-02 |
| 1958 | 1 | abuses/dominates | `(LLM tail)` | Joffrey → Sansa | acok-sansa-03 |
| 1959 | 1 | secretly protects | `(LLM tail)` | Ser Dontos → Sansa | acok-sansa-03 |
| 1960 | 1 | antagonizes/disciplines | `OPPOSES` | Tyrion → Joffrey | acok-sansa-03 |
| 1961 | 1 | claims credit for | `(LLM tail)` | Joffrey → Eddard Stark's death | acok-sansa-03 |
| 1962 | 1 | controls (via proxy) | `COMMANDS` | Cersei → Joffrey | acok-sansa-03 |
| 1963 | 1 | dismisses/mocks | `(LLM tail)` | Tyrion → Lancel Lannister | acok-sansa-03 |
| 1964 | 1 | relies on for escape | `(LLM tail)` | Sansa → Dontos | acok-sansa-04 |
| 1965 | 1 | grudging respect/attraction to strength of | `RESPECTS` | Sansa → Sandor Clegane | acok-sansa-04 |
| 1966 | 1 | protective/confrontational toward | `(LLM tail)` | Sandor Clegane → Sansa | acok-sansa-04 |
| 1967 | 1 | advises / controls | `ADVISES` | Cersei → Sansa | acok-sansa-04 |
| 1968 | 1 | close bond with | `(LLM tail)` | Cersei → Jaime Lannister | acok-sansa-04 |
| 1969 | 1 | serves as spy for | `SERVES` | Dontos → Varys | acok-sansa-04 |
| 1970 | 1 | has unnamed friend aiding | `(LLM tail)` | Dontos → Sansa | acok-sansa-04 |
| 1971 | 1 | shames | `(LLM tail)` | Joffrey → Sansa | acok-sansa-04 |
| 1972 | 1 | was shamed by | `(LLM tail)` | Joffrey → Arya Stark | acok-sansa-04 |
| 1973 | 1 | Hostage/captive of | `(LLM tail)` | Sansa → Joffrey / House Lannister | acok-sansa-05 |
| 1974 | 1 | Gratitude toward / prayer for | `(LLM tail)` | Sansa → Sandor Clegane | acok-sansa-05 |
| 1975 | 1 | Uneasy subordination to | `SERVES` | Sansa → Cersei | acok-sansa-05 |
| 1976 | 1 | Possessive cruelty toward | `(LLM tail)` | Joffrey → Sansa | acok-sansa-05 |
| 1977 | 1 | Contemptuous mentorship of | `HATES` | Cersei → Sansa | acok-sansa-05 |
| 1978 | 1 | Use of | `(LLM tail)` | Cersei → Ser Ilyn Payne | acok-sansa-05 |
| 1979 | 1 | Shame about | `(LLM tail)` | Lady Tanda → Lollys | acok-sansa-05 |
| 1980 | 1 | Rides with | `(LLM tail)` | Ser Mandon Moore → Tyrion | acok-sansa-05 |
| 1981 | 1 | Controls/dominates | `COMMANDS` | Cersei → Sansa | acok-sansa-06 |
| 1982 | 1 | Resents gendered inequality with | `RESENTS` | Cersei → Jaime | acok-sansa-06 |
| 1983 | 1 | Protects (possessively) | `PROTECTS` | Cersei → Joffrey | acok-sansa-06 |
| 1984 | 1 | Secretly trusts | `(LLM tail)` | Sansa → Ser Dontos | acok-sansa-06 |
| 1985 | 1 | Has replaced | `(LLM tail)` | Ser Osmund Kettleblack → Sandor Clegane | acok-sansa-06 |
| 1986 | 1 | Mourns (implicitly) | `MOURNS` | Sansa → Eddard Stark | acok-sansa-06 |
| 1987 | 1 | Mother, protective authority over | `(LLM tail)` | Cersei → Joffrey | acok-sansa-07 |
| 1988 | 1 | Dismissive contempt toward | `(LLM tail)` | Cersei → Lancel | acok-sansa-07 |
| 1989 | 1 | Cousin, subordinate to | `COUSIN_OF` | Lancel → Cersei | acok-sansa-07 |
| 1990 | 1 | Compassion despite enmity toward | `(LLM tail)` | Sansa → Lancel | acok-sansa-07 |
| 1991 | 1 | Complicated fear/sympathy toward | `FEARS` | Sansa → Sandor Clegane | acok-sansa-07 |
| 1992 | 1 | Protective obsession toward | `(LLM tail)` | Sandor → Sansa | acok-sansa-07 |
| 1993 | 1 | Self-loathing, despair | `(LLM tail)` | Sandor → (self) | acok-sansa-07 |
| 1994 | 1 | Would-be protector/admirer of | `RESPECTS` | Ser Dontos → Sansa | acok-sansa-07 |
| 1995 | 1 | Low estimation of | `(LLM tail)` | Sansa → Ser Dontos | acok-sansa-07 |
| 1996 | 1 | Orders obedience from | `(LLM tail)` | Cersei → Osfryd Kettleblack | acok-sansa-07 |
| 1997 | 1 | Brief, hopeful longing for | `(LLM tail)` | Sansa → Robb Stark | acok-sansa-07 |
| 1998 | 1 | Grandfather / authority over | `PARENT_OF` | Tywin Lannister → Joffrey | acok-sansa-08 |
| 1999 | 1 | Sets aside betrothal to | `BETROTHED_TO` | Joffrey → Sansa Stark | acok-sansa-08 |
| 2000 | 1 | Agrees to marry | `(LLM tail)` | Joffrey → Margaery Tyrell | acok-sansa-08 |
| 2001 | 1 | Controls/instructs | `COMMANDS` | Cersei → Sansa | acok-sansa-08 |
| 2002 | 1 | Mother/protector of | `(LLM tail)` | Cersei → Joffrey | acok-sansa-08 |
| 2003 | 1 | Sworn to serve | `SWORN_TO` | Ser Loras → Joffrey (Kingsguard) | acok-sansa-08 |
| 2004 | 1 | Allied with / serves | `ALLIES_WITH` | Mace Tyrell → The Crown | acok-sansa-08 |
| 2005 | 1 | Brother of / acts for | `SIBLING_OF` | Ser Garlan → Margaery Tyrell | acok-sansa-08 |
| 2006 | 1 | Calls her "Jonquil" | `(LLM tail)` | Dontos → Sansa | acok-sansa-08 |
| 2007 | 1 | Granted lordship by | `(LLM tail)` | Petyr Baelish → Joffrey/Crown | acok-sansa-08 |
| 2008 | 1 | Whispering to | `(LLM tail)` | Varys → Petyr Baelish | acok-sansa-08 |
| 2009 | 1 | Hostage of | `(LLM tail)` | Sansa → Cersei/Crown | acok-sansa-08 |
| 2010 | 1 | Political marriage to | `(LLM tail)` | Tyrell alliance → Lannister/Crown | acok-sansa-08 |
| 2011 | 1 | Leers at | `(LLM tail)` | Osmund Kettleblack → Sansa | acok-sansa-08 |
| 2012 | 1 | Son returning to | `(LLM tail)` | Theon Greyjoy → Balon Greyjoy | acok-theon-01 |
| 2013 | 1 | Disappointed in / suspicious of | `(LLM tail)` | Balon Greyjoy → Theon Greyjoy | acok-theon-01 |
| 2014 | 1 | Favorable comparison to Theon | `(LLM tail)` | Balon Greyjoy → Asha Greyjoy | acok-theon-01 |
| 2015 | 1 | Former ward/hostage of | `(LLM tail)` | Theon Greyjoy → Eddard Stark | acok-theon-01 |
| 2016 | 1 | Affection for (as younger brother) | `SIBLING_OF` | Theon Greyjoy → Robb Stark | acok-theon-01 |
| 2017 | 1 | Contempt/rivalry toward | `HATES` | Theon Greyjoy → Jon Snow | acok-theon-01 |
| 2018 | 1 | Priest-uncle, chilly and pious | `UNCLE_OF` | Aeron Greyjoy → Theon Greyjoy | acok-theon-01 |
| 2019 | 1 | Devoted priest of | `(LLM tail)` | Aeron Greyjoy → Drowned God | acok-theon-01 |
| 2020 | 1 | Friendly with / missed | `MOURNS` | Theon Greyjoy → Patrek Mallister | acok-theon-01 |
| 2021 | 1 | Wary of ironborn; warned son away from | `DISTRUSTS` | Jason Mallister → Theon Greyjoy | acok-theon-01 |
| 2022 | 1 | Slayer of | `(LLM tail)` | Jason Mallister → Rodrik Greyjoy | acok-theon-01 |
| 2023 | 1 | Distant and suspicious toward | `(LLM tail)` | Catelyn Stark → Theon Greyjoy | acok-theon-01 |
| 2024 | 1 | Vowed to outlive | `(LLM tail)` | Balon Greyjoy → Robert Baratheon & Eddard Stark | acok-theon-01 |
| 2025 | 1 | Uncle of (absent/unsettling) | `UNCLE_OF` | Euron Greyjoy → Theon Greyjoy | acok-theon-01 |
| 2026 | 1 | Uncle of (old, cautious) | `UNCLE_OF` | Victarion Greyjoy → Theon Greyjoy | acok-theon-01 |
| 2027 | 1 | Mother of (absent, ill) | `PARENT_OF` | Lady Greyjoy → Theon Greyjoy | acok-theon-01 |
| 2028 | 1 | Servant/steward of | `(LLM tail)` | Helya → Balon Greyjoy | acok-theon-01 |
| 2029 | 1 | Loyal retainer of | `(LLM tail)` | Dagmer Cleftjaw → Balon Greyjoy | acok-theon-01 |
| 2030 | 1 | Brother (estranged) | `SIBLING_OF` | Theon → Asha | acok-theon-02 |
| 2031 | 1 | Son (seeking approval) | `(LLM tail)` | Theon → Balon | acok-theon-02 |
| 2032 | 1 | Favored child | `(LLM tail)` | Asha → Balon | acok-theon-02 |
| 2033 | 1 | Wary of uncle | `DISTRUSTS` | Theon → Euron | acok-theon-02 |
| 2034 | 1 | Respected by ironborn | `RESPECTS` | Asha → Ironborn generally | acok-theon-02 |
| 2035 | 1 | Stranger to ironborn | `(LLM tail)` | Theon → Ironborn generally | acok-theon-02 |
| 2036 | 1 | Master / somewhat fond | `(LLM tail)` | Theon → Wex | acok-theon-02 |
| 2037 | 1 | Tricks / tests | `(LLM tail)` | Asha → Theon | acok-theon-02 |
| 2038 | 1 | Resentful | `RESENTS` | Theon → Asha | acok-theon-02 |
| 2039 | 1 | Mother (absent, ill) | `(LLM tail)` | Lady Greyjoy → Theon | acok-theon-02 |
| 2040 | 1 | Squire / baseborn | `(LLM tail)` | Wex → Lord Botley | acok-theon-02 |
| 2041 | 1 | Former ward | `(LLM tail)` | Theon → Eddard Stark | acok-theon-02 |
| 2042 | 1 | nephew / subordinate tension | `NEPHEW_OF` | Theon Greyjoy → Aeron Damphair | acok-theon-03 |
| 2043 | 1 | commander (resented) | `COMMANDS` | Theon Greyjoy → Ironborn warriors | acok-theon-03 |
| 2044 | 1 | conflicted former friend | `(LLM tail)` | Theon Greyjoy → Benfred Tallhart | acok-theon-03 |
| 2045 | 1 | son seeking approval | `(LLM tail)` | Theon Greyjoy → Balon Greyjoy | acok-theon-03 |
| 2046 | 1 | sibling rivalry | `(LLM tail)` | Theon Greyjoy → Asha Greyjoy | acok-theon-03 |
| 2047 | 1 | deep affection / mentee | `LOVES` | Theon Greyjoy → Dagmer Cleftjaw | acok-theon-03 |
| 2048 | 1 | conflicted former ward | `(LLM tail)` | Theon Greyjoy → Eddard Stark | acok-theon-03 |
| 2049 | 1 | conflicted former companion | `COMPANION_OF` | Theon Greyjoy → Robb Stark | acok-theon-03 |
| 2050 | 1 | sworn man / loyal servant | `(LLM tail)` | Dagmer Cleftjaw → Balon Greyjoy | acok-theon-03 |
| 2051 | 1 | mentor / warmth | `TUTORS` | Dagmer Cleftjaw → Theon Greyjoy | acok-theon-03 |
| 2052 | 1 | priest / authority over the men | `(LLM tail)` | Aeron Damphair → Ironborn warriors | acok-theon-03 |
| 2053 | 1 | hatred / defiance | `HATES` | Benfred Tallhart → Theon Greyjoy | acok-theon-03 |
| 2054 | 1 | obedient to Theon after Todric's death | `(LLM tail)` | Old Botley (Fishwhiskers) → Theon Greyjoy | acok-theon-03 |
| 2055 | 1 | reliance / favoritism | `(LLM tail)` | Balon Greyjoy → Asha Greyjoy | acok-theon-03 |
| 2056 | 1 | threatened by/suspicious of | `(LLM tail)` | Theon → Reek | acok-theon-04 |
| 2057 | 1 | coerces | `(LLM tail)` | Theon → Farlen | acok-theon-04 |
| 2058 | 1 | grudging respect for counsel of | `RESPECTS` | Theon → Maester Luwin | acok-theon-04 |
| 2059 | 1 | resents/feels rejected by | `RESENTS` | Theon → Winterfell castle folk | acok-theon-04 |
| 2060 | 1 | foster-brother of (claimed only by Robb) | `WARD_OF` | Theon → Robb Stark | acok-theon-04 |
| 2061 | 1 | former servant of | `(LLM tail)` | Reek → Lord Bolton | acok-theon-04 |
| 2062 | 1 | mocked by | `(LLM tail)` | Walder Frey → Walder Frey (cousin) | acok-theon-04 |
| 2063 | 1 | betrayed/oath-broke | `(LLM tail)` | Osha → Theon | acok-theon-04 |
| 2064 | 1 | models self after | `(LLM tail)` | Theon → Eddard Stark | acok-theon-04 |
| 2065 | 1 | sibling rivalry / mutual contempt | `(LLM tail)` | Theon → Asha | acok-theon-05 |
| 2066 | 1 | lord / dependent | `(LLM tail)` | Theon → Reek | acok-theon-05 |
| 2067 | 1 | sexual violence toward | `(LLM tail)` | Theon → Kyra | acok-theon-05 |
| 2068 | 1 | fear of knowledge held by | `FEARS` | Theon → Reek | acok-theon-05 |
| 2069 | 1 | commands / subordinate to | `COMMANDS` | Asha → Balon Greyjoy | acok-theon-05 |
| 2070 | 1 | claims vengeance for | `(LLM tail)` | Theon → Rodrik and Maron Greyjoy | acok-theon-05 |
| 2071 | 1 | overlord / guards | `(LLM tail)` | Theon → Urzen, Kromm | acok-theon-05 |
| 2072 | 1 | conflicted identity | `(LLM tail)` | Theon → Stark household / Greyjoy heritage | acok-theon-05 |
| 2073 | 1 | Forsaken by father | `(LLM tail)` | Theon → Balon Greyjoy | acok-theon-06 |
| 2074 | 1 | Forsaken by sister | `SIBLING_OF` | Theon → Asha Greyjoy | acok-theon-06 |
| 2075 | 1 | Forsaken by uncle(s) | `UNCLE_OF` | Theon → Greyjoy uncle(s) | acok-theon-06 |
| 2076 | 1 | Dependent on / antagonistic toward | `(LLM tail)` | Theon → Maester Luwin | acok-theon-06 |
| 2077 | 1 | Former teacher of | `(LLM tail)` | Maester Luwin → Theon | acok-theon-06 |
| 2078 | 1 | Serves (by oath) | `SERVES` | Maester Luwin → Winterfell / Theon (as holder) | acok-theon-06 |
| 2079 | 1 | Commands (with declining authority) | `COMMANDS` | Theon → Black Lorren | acok-theon-06 |
| 2080 | 1 | Contemptuous obedience toward | `HATES` | Black Lorren → Theon | acok-theon-06 |
| 2081 | 1 | Former trainer of | `(LLM tail)` | Ser Rodrik → Theon | acok-theon-06 |
| 2082 | 1 | Dutiful to | `(LLM tail)` | Ser Rodrik → Catelyn Stark / House Stark | acok-theon-06 |
| 2083 | 1 | Hostage (as child) | `(LLM tail)` | Theon → Eddard Stark | acok-theon-06 |
| 2084 | 1 | Deceived | `(LLM tail)` | Ramsay → Theon | acok-theon-06 |
| 2085 | 1 | Killed (by treachery) | `KILLS` | Ramsay → Ser Rodrik | acok-theon-06 |
| 2086 | 1 | Master of (the original) | `(LLM tail)` | Ramsay → Reek | acok-theon-06 |
| 2087 | 1 | Used as decoy | `(LLM tail)` | Ramsay → Reek (original) | acok-theon-06 |
| 2088 | 1 | Subordinate (claims allegiance) | `SERVES` | Ramsay → Bolton (his father) | acok-theon-06 |
| 2089 | 1 | Rode beside in battle | `(LLM tail)` | Theon → Robb Stark | acok-theon-06 |
| 2090 | 1 | Recalls saving | `(LLM tail)` | Theon → Bran Stark | acok-theon-06 |
| 2091 | 1 | Siblings — hostile, manipulative, mistrustful | `DISTRUSTS` | Tyrion → Cersei | acok-tyrion-01 |
| 2092 | 1 | Serves (father appointed him) | `SERVES` | Tyrion → Tywin | acok-tyrion-01 |
| 2093 | 1 | Employer / protected by | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-01 |
| 2094 | 1 | Alliance of convenience | `ALLIES_WITH` | Tyrion → Timett son of Timett | acok-tyrion-01 |
| 2095 | 1 | Lover — tender, possessive, self-aware | `LOVER_OF` | Tyrion → Shae | acok-tyrion-01 |
| 2096 | 1 | Wary mutual respect / adversarial intelligence | `RESPECTS` | Tyrion → Varys | acok-tyrion-01 |
| 2097 | 1 | Suspicious, plans to confront | `(LLM tail)` | Tyrion → Littlefinger | acok-tyrion-01 |
| 2098 | 1 | Desires his rescue above all | `(LLM tail)` | Cersei → Jaime | acok-tyrion-01 |
| 2099 | 1 | Regent — frustrated by his defiance | `(LLM tail)` | Cersei → Joffrey | acok-tyrion-01 |
| 2100 | 1 | Orchestrated his death | `(LLM tail)` | Cersei → Robert Baratheon | acok-tyrion-01 |
| 2101 | 1 | Uses / distrusts | `(LLM tail)` | Cersei → Small council members | acok-tyrion-01 |
| 2102 | 1 | Elevated by | `(LLM tail)` | Janos Slynt → Littlefinger | acok-tyrion-01 |
| 2103 | 1 | Informed on / betrayed | `(LLM tail)` | Sansa Stark → Eddard Stark | acok-tyrion-01 |
| 2104 | 1 | Fond of / protects | `LOVES` | Joffrey → Sandor Clegane | acok-tyrion-01 |
| 2105 | 1 | Kingsguard — obeys Cersei | `SERVES` | Ser Mandon Moore → Cersei | acok-tyrion-01 |
| 2106 | 1 | Wary of, assesses as dangerous | `(LLM tail)` | Tyrion → Ser Mandon Moore | acok-tyrion-01 |
| 2107 | 1 | Serves / answers to | `SERVES` | Vylarr → Tyrion | acok-tyrion-01 |
| 2108 | 1 | acts as Hand/authority over | `(LLM tail)` | Tyrion → Janos Slynt | acok-tyrion-02 |
| 2109 | 1 | appoints | `(LLM tail)` | Tyrion → Ser Jacelyn Bywater | acok-tyrion-02 |
| 2110 | 1 | formerly served/was bought by | `SERVES` | Janos Slynt → Littlefinger | acok-tyrion-02 |
| 2111 | 1 | grateful to/serves | `(LLM tail)` | Ser Jacelyn Bywater → Tyrion | acok-tyrion-02 |
| 2112 | 1 | sellsword loyalty to | `(LLM tail)` | Bronn → Tyrion | acok-tyrion-02 |
| 2113 | 1 | clansman serving | `(LLM tail)` | Timett → Tyrion | acok-tyrion-02 |
| 2114 | 1 | suspects is controlled by Varys | `(LLM tail)` | Tyrion → Ser Jacelyn Bywater | acok-tyrion-02 |
| 2115 | 1 | restive/wants more from | `(LLM tail)` | Shae → Tyrion | acok-tyrion-02 |
| 2116 | 1 | Serves as Hand of the King to | `SERVES` | Tyrion → Joffrey | acok-tyrion-03 |
| 2117 | 1 | Politically manages / outmaneuvers | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-03 |
| 2118 | 1 | Is served by (squire) | `(LLM tail)` | Tyrion → Podrick Payne | acok-tyrion-03 |
| 2119 | 1 | Secret alliance / mutual wariness with | `ALLIES_WITH` | Tyrion → Varys | acok-tyrion-03 |
| 2120 | 1 | Distrusts / fears | `DISTRUSTS` | Tyrion → Littlefinger | acok-tyrion-03 |
| 2121 | 1 | Keeping secret lover | `LOVER_OF` | Tyrion → Shae | acok-tyrion-03 |
| 2122 | 1 | Antagonistic sibling rivalry with | `OPPOSES` | Cersei → Tyrion | acok-tyrion-03 |
| 2123 | 1 | Reserves special warmth for | `(LLM tail)` | Cersei → Jaime | acok-tyrion-03 |
| 2124 | 1 | Strategically aligned with / useful to | `(LLM tail)` | Littlefinger → Tyrion | acok-tyrion-03 |
| 2125 | 1 | Ingratiates himself with | `(LLM tail)` | Littlefinger → Cersei | acok-tyrion-03 |
| 2126 | 1 | Grateful to / cooperates with | `(LLM tail)` | Chataya → Tyrion | acok-tyrion-03 |
| 2127 | 1 | Covertly assists | `(LLM tail)` | Varys → Tyrion | acok-tyrion-03 |
| 2128 | 1 | Seeking attention of | `(LLM tail)` | Lady Tanda → Tyrion | acok-tyrion-03 |
| 2129 | 1 | Political rivalry with | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-04 |
| 2130 | 1 | Employs / trusts | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-04 |
| 2131 | 1 | Sardonic affection for | `LOVES` | Tyrion → Cersei | acok-tyrion-04 |
| 2132 | 1 | Courts / pursues | `(LLM tail)` | Lady Tanda → Tyrion | acok-tyrion-04 |
| 2133 | 1 | Formerly fostered with | `(LLM tail)` | Littlefinger → Tully family (Catelyn, Lysa, Hoster) | acok-tyrion-04 |
| 2134 | 1 | Knows about / taunts with | `(LLM tail)` | Littlefinger → The Valyrian steel dagger | acok-tyrion-04 |
| 2135 | 1 | Patronized / elevated | `(LLM tail)` | Jon Arryn → Littlefinger | acok-tyrion-04 |
| 2136 | 1 | Mourns / seeks justice for | `MOURNS` | Doran Martell → Elia Martell | acok-tyrion-04 |
| 2137 | 1 | Armed | `(LLM tail)` | Tyrion → Mountain clansmen | acok-tyrion-04 |
| 2138 | 1 | Serves (nervously) | `SERVES` | Podrick Payne → Tyrion | acok-tyrion-04 |
| 2139 | 1 | Assesses fighters | `(LLM tail)` | Bronn → Tallad | acok-tyrion-04 |
| 2140 | 1 | acting Hand of the King to | `(LLM tail)` | Tyrion → Joffrey | acok-tyrion-05 |
| 2141 | 1 | political rival / antagonistic sibling | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-05 |
| 2142 | 1 | professional respect | `RESPECTS` | Tyrion → Ser Jacelyn Bywater | acok-tyrion-05 |
| 2143 | 1 | patron / superior to | `(LLM tail)` | Tyrion → Hallyne the Pyromancer | acok-tyrion-05 |
| 2144 | 1 | fiercely protective mother to | `(LLM tail)` | Cersei → Myrcella | acok-tyrion-05 |
| 2145 | 1 | longing for / admires | `RESPECTS` | Cersei → Jaime | acok-tyrion-05 |
| 2146 | 1 | resentful of / dependent on | `RESENTS` | Cersei → Tywin | acok-tyrion-05 |
| 2147 | 1 | compares self unfavorably to men | `(LLM tail)` | Cersei → (general) | acok-tyrion-05 |
| 2148 | 1 | trusts (with reservation) | `TRUSTS` | Tyrion → Varys | acok-tyrion-05 |
| 2149 | 1 | deploys as Myrcella's shield | `(LLM tail)` | Tyrion → Ser Arys Oakheart | acok-tyrion-05 |
| 2150 | 1 | sues for peace with | `(LLM tail)` | Robb Stark → Tyrion / Lannisters | acok-tyrion-05 |
| 2151 | 1 | drives peace effort over | `(LLM tail)` | Lady Catelyn → Robb Stark | acok-tyrion-05 |
| 2152 | 1 | formerly supplanted by | `(LLM tail)` | Hallyne → Maesters of the Citadel | acok-tyrion-05 |
| 2153 | 1 | commands Moon Brothers guarding | `COMMANDS` | Crawn → Tyrion's tower | acok-tyrion-05 |
| 2154 | 1 | sibling rivalry / political adversary | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-06 |
| 2155 | 1 | political manipulation | `(LLM tail)` | Tyrion → Varys | acok-tyrion-06 |
| 2156 | 1 | admiration (performed or genuine) | `RESPECTS` | Varys → Tyrion | acok-tyrion-06 |
| 2157 | 1 | mutual distrust | `(LLM tail)` | Tyrion → Littlefinger | acok-tyrion-06 |
| 2158 | 1 | exposes and arrests | `(LLM tail)` | Tyrion → Pycelle | acok-tyrion-06 |
| 2159 | 1 | has been spying for | `(LLM tail)` | Pycelle → Cersei | acok-tyrion-06 |
| 2160 | 1 | lifelong loyalty (self-claimed) | `(LLM tail)` | Pycelle → House Lannister / Tywin | acok-tyrion-06 |
| 2161 | 1 | allowed to die | `(LLM tail)` | Pycelle → Jon Arryn | acok-tyrion-06 |
| 2162 | 1 | commands / bantering | `COMMANDS` | Tyrion → Shagga | acok-tyrion-06 |
| 2163 | 1 | contempt toward / antagonism | `HATES` | Tyrion → Ser Alliser | acok-tyrion-06 |
| 2164 | 1 | frustrated hostility toward | `(LLM tail)` | Ser Alliser → Tyrion | acok-tyrion-06 |
| 2165 | 1 | longing / fondness | `(LLM tail)` | Tyrion → Shae | acok-tyrion-06 |
| 2166 | 1 | nostalgic memory of | `(LLM tail)` | Tyrion → Jon Snow | acok-tyrion-06 |
| 2167 | 1 | grievance toward | `MOURNS` | Stannis → Renly / Robert | acok-tyrion-06 |
| 2168 | 1 | distrust of all three councilors | `DISTRUSTS` | Tyrion → Varys, Littlefinger, Pycelle | acok-tyrion-06 |
| 2169 | 1 | obstructionist toward | `(LLM tail)` | Pycelle → Tyrion | acok-tyrion-06 |
| 2170 | 1 | political rival | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-07 |
| 2171 | 1 | complicit in murder of | `(LLM tail)` | Lancel → Robert Baratheon | acok-tyrion-07 |
| 2172 | 1 | employs | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-07 |
| 2173 | 1 | uses as cover | `(LLM tail)` | Tyrion → Alayaya | acok-tyrion-07 |
| 2174 | 1 | lover of (Cersei's perspective) | `LOVER_OF` | Lancel → Cersei | acok-tyrion-07 |
| 2175 | 1 | relies on intelligence from | `(LLM tail)` | Tyrion → Varys | acok-tyrion-07 |
| 2176 | 1 | arrested | `(LLM tail)` | Tyrion → Pycelle | acok-tyrion-07 |
| 2177 | 1 | instructed | `(LLM tail)` | Tywin → Lancel | acok-tyrion-07 |
| 2178 | 1 | proprietor / host | `(LLM tail)` | Chataya → Tyrion | acok-tyrion-07 |
| 2179 | 1 | competing with | `(LLM tail)` | Dancy → Marei | acok-tyrion-07 |
| 2180 | 1 | learning from | `(LLM tail)` | Alayaya → Marei | acok-tyrion-07 |
| 2181 | 1 | twin of | `(LLM tail)` | Jaime → Cersei | acok-tyrion-07 |
| 2182 | 1 | Sibling rivalry, mutual suspicion | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-08 |
| 2183 | 1 | Acting Hand, authority over | `(LLM tail)` | Tyrion → Joffrey | acok-tyrion-08 |
| 2184 | 1 | Compares Tyrion to (favorably in words, unfavorably implied) | `(LLM tail)` | Cersei → Jaime | acok-tyrion-08 |
| 2185 | 1 | Self-interested maneuvering toward | `(LLM tail)` | Littlefinger → The Crown | acok-tyrion-08 |
| 2186 | 1 | Devotion / grief-rage for | `MOURNS` | Loras Tyrell → Renly Baratheon | acok-tyrion-08 |
| 2187 | 1 | Favors above other sons | `(LLM tail)` | Mace Tyrell → Loras Tyrell | acok-tyrion-08 |
| 2188 | 1 | Oldest friend of | `(LLM tail)` | Paxter Redwyne → Mace Tyrell | acok-tyrion-08 |
| 2189 | 1 | Employs, relies on | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-08 |
| 2190 | 1 | Uses for intelligence | `(LLM tail)` | Tyrion → Varys | acok-tyrion-08 |
| 2191 | 1 | Bodyguard to | `(LLM tail)` | Sandor Clegane → Joffrey | acok-tyrion-08 |
| 2192 | 1 | Loyal to (even after death) | `SERVES` | Ser Cortnay Penrose → Renly Baratheon | acok-tyrion-08 |
| 2193 | 1 | Unexpected affection toward | `LOVES` | Cersei → Tyrion | acok-tyrion-08 |
| 2194 | 1 | Childhood memory involving | `(LLM tail)` | Tyrion → Jaime and Cersei | acok-tyrion-08 |
| 2195 | 1 | Submitted to | `(LLM tail)` | Lord Alester Florent → Stannis Baratheon | acok-tyrion-08 |
| 2196 | 1 | Uncle/protector of | `UNCLE_OF` | Tyrion → Myrcella | acok-tyrion-09 |
| 2197 | 1 | Hostile uncle/guardian of | `UNCLE_OF` | Tyrion → Joffrey | acok-tyrion-09 |
| 2198 | 1 | Pragmatic protector of | `(LLM tail)` | Tyrion → Sansa Stark | acok-tyrion-09 |
| 2199 | 1 | Employer/wary trust of | `(LLM tail)` | Tyrion → Bronn | acok-tyrion-09 |
| 2200 | 1 | Informed by | `(LLM tail)` | Tyrion → Lancel Lannister | acok-tyrion-09 |
| 2201 | 1 | Receives honest counsel from | `ADVISES` | Tyrion → Ser Jacelyn Bywater | acok-tyrion-09 |
| 2202 | 1 | Charming/manipulating | `(LLM tail)` | Cersei → Lancel Lannister | acok-tyrion-09 |
| 2203 | 1 | Secretly employing | `(LLM tail)` | Cersei → Ser Osmund Kettleblack | acok-tyrion-09 |
| 2204 | 1 | Momentary ally of | `ALLIES_WITH` | Cersei → Tyrion | acok-tyrion-09 |
| 2205 | 1 | Cruel to | `(LLM tail)` | Joffrey → Tommen | acok-tyrion-09 |
| 2206 | 1 | Prioritizes king over | `(LLM tail)` | Ser Mandon Moore → Sansa Stark | acok-tyrion-09 |
| 2207 | 1 | Insolent toward | `(LLM tail)` | Bronn → Tyrion | acok-tyrion-09 |
| 2208 | 1 | Desperate for | `(LLM tail)` | Lady Tanda → Lollys | acok-tyrion-09 |
| 2209 | 1 | Spies on/for | `SPIES_ON` | Lancel → Tyrion | acok-tyrion-10 |
| 2210 | 1 | Lover of / depends on | `LOVER_OF` | Shae → Tyrion | acok-tyrion-10 |
| 2211 | 1 | Fears/opposes | `FEARS` | Cersei → Tyrion | acok-tyrion-10 |
| 2212 | 1 | Ambitious | `(LLM tail)` | Bronn → (general) | acok-tyrion-10 |
| 2213 | 1 | Threat to | `(LLM tail)` | Symon Silver Tongue → Tyrion | acok-tyrion-10 |
| 2214 | 1 | Opposes/co-opts | `OPPOSES` | Tyrion → Cersei | acok-tyrion-10 |
| 2215 | 1 | commands / sends into battle | `COMMANDS` | Tyrion → Shagga / Stone Crows | acok-tyrion-11 |
| 2216 | 1 | feels dependent on / affection for | `LOVES` | Tyrion → Shagga | acok-tyrion-11 |
| 2217 | 1 | respect mixed with humor toward | `RESPECTS` | Shagga → Tyrion | acok-tyrion-11 |
| 2218 | 1 | employer / commands | `COMMANDS` | Tyrion → Bronn | acok-tyrion-11 |
| 2219 | 1 | pragmatic loyalty to | `(LLM tail)` | Bronn → Tyrion | acok-tyrion-11 |
| 2220 | 1 | spying on via | `(LLM tail)` | Tyrion → Cersei through Ser Osmund Kettleblack | acok-tyrion-11 |
| 2221 | 1 | political patron of | `(LLM tail)` | Tyrion → High Septon (new) | acok-tyrion-11 |
| 2222 | 1 | protective uncle toward | `UNCLE_OF` | Tyrion → Tommen | acok-tyrion-11 |
| 2223 | 1 | does not miss | `MOURNS` | Tommen → Joffrey | acok-tyrion-11 |
| 2224 | 1 | father of / influence on | `PARENT_OF` | Lord Tywin → Tyrion | acok-tyrion-11 |
| 2225 | 1 | hedging allegiance | `(LLM tail)` | House Swann → Multiple kings | acok-tyrion-11 |
| 2226 | 1 | fearful subordinate to | `FEARS` | Hallyne → Tyrion | acok-tyrion-11 |
| 2227 | 1 | nostalgic ambivalence toward | `(LLM tail)` | Tyrion → Winterfell / the Starks | acok-tyrion-11 |
| 2228 | 1 | Sibling rivalry / mutual antagonism | `(LLM tail)` | Tyrion → Cersei | acok-tyrion-12 |
| 2229 | 1 | Serves (as Hand) | `SERVES` | Tyrion → Joffrey | acok-tyrion-12 |
| 2230 | 1 | Emulates / seeks to channel | `(LLM tail)` | Tyrion → Tywin Lannister | acok-tyrion-12 |
| 2231 | 1 | Admires recklessness of | `RESPECTS` | Tyrion → Jaime Lannister | acok-tyrion-12 |
| 2232 | 1 | Captured / holds hostage | `PRISONER_OF` | Cersei → Alayaya | acok-tyrion-12 |
| 2233 | 1 | Protective of / fears for | `PROTECTS` | Cersei → Joffrey, Tommen | acok-tyrion-12 |
| 2234 | 1 | Serves / informs | `SERVES` | Varys → Tyrion | acok-tyrion-12 |
| 2235 | 1 | Suspected of double-dealing by | `(LLM tail)` | Varys → Cersei | acok-tyrion-12 |
| 2236 | 1 | Attendant to | `(LLM tail)` | Shae → Lollys Stokeworth | acok-tyrion-12 |
| 2237 | 1 | Seeks favor from | `SEEKS` | Lady Tanda → Tyrion, Cersei | acok-tyrion-12 |
| 2238 | 1 | Uses as leverage | `(LLM tail)` | Tyrion → Tommen | acok-tyrion-12 |
| 2239 | 1 | Commands/directs (acting Hand) | `COMMANDS` | Tyrion → Joffrey | acok-tyrion-13 |
| 2240 | 1 | Confronts / overrides | `(LLM tail)` | Tyrion → Sandor Clegane | acok-tyrion-13 |
| 2241 | 1 | Relies on (grudgingly) | `(LLM tail)` | Tyrion → Ser Mandon Moore | acok-tyrion-13 |
| 2242 | 1 | Trust in (field command) | `TRUSTS` | Tyrion → Jacelyn Bywater | acok-tyrion-13 |
| 2243 | 1 | Trust in (operational) | `TRUSTS` | Tyrion → Bronn | acok-tyrion-13 |
| 2244 | 1 | Leads / inspires | `COMMANDS` | Tyrion → Sortie force | acok-tyrion-13 |
| 2245 | 1 | Subordinate to (in practice) | `SERVES` | Joffrey → Tyrion | acok-tyrion-13 |
| 2246 | 1 | Compares Stannis to | `(LLM tail)` | Tyrion → Lord Tywin | acok-tyrion-13 |
| 2247 | 1 | Contrasted with | `(LLM tail)` | Stannis → Robert Baratheon | acok-tyrion-13 |
| 2248 | 1 | Assessed (previously) | `(LLM tail)` | Jaime → Ser Mandon Moore | acok-tyrion-13 |
| 2249 | 1 | Lord to squire (protective) | `(LLM tail)` | Tyrion → Podrick Payne | acok-tyrion-14 |
| 2250 | 1 | Loyal squire, willing to die for lord | `(LLM tail)` | Podrick Payne → Tyrion | acok-tyrion-14 |
| 2251 | 1 | Commander, flanked by | `COMMANDS` | Tyrion → Ser Mandon Moore | acok-tyrion-14 |
| 2252 | 1 | Attempts to assassinate | `(LLM tail)` | Ser Mandon Moore → Tyrion | acok-tyrion-14 |
| 2253 | 1 | Battlefield ally | `ALLIES_WITH` | Tyrion → Ser Balon Swann | acok-tyrion-14 |
| 2254 | 1 | Brother, first thought when saved | `SIBLING_OF` | Tyrion → Jaime Lannister | acok-tyrion-14 |
| 2255 | 1 | Remembers with affection | `LOVES` | Tyrion → Shagga | acok-tyrion-14 |
| 2256 | 1 | Observes with understanding | `(LLM tail)` | Tyrion → Sandor Clegane | acok-tyrion-14 |
| 2257 | 1 | Fellow Kingsguard | `(LLM tail)` | Ser Balon Swann → Ser Mandon Moore | acok-tyrion-14 |
| 2258 | 1 | Fight back to back | `(LLM tail)` | Ser Balon Swann, Ser Mandon Moore → Each other | acok-tyrion-14 |
| 2259 | 1 | Admires enemy courage | `RESPECTS` | Tyrion → Stannis's men | acok-tyrion-14 |
| 2260 | 1 | distrusts / suspects murder plot by | `DISTRUSTS` | Tyrion → Cersei | acok-tyrion-15 |
| 2261 | 1 | suspects attempted assassination by (via proxy) | `(LLM tail)` | Tyrion → Ser Mandon Moore | acok-tyrion-15 |
| 2262 | 1 | gratitude and trust toward | `(LLM tail)` | Tyrion → Podrick Payne | acok-tyrion-15 |
| 2263 | 1 | longing / desire for | `(LLM tail)` | Tyrion → Shae | acok-tyrion-15 |
| 2264 | 1 | love / loss / bitterness toward | `LOVES` | Tyrion → Tysha | acok-tyrion-15 |
| 2265 | 1 | complex resentment and desire for approval from | `(LLM tail)` | Tyrion → Tywin | acok-tyrion-15 |
| 2266 | 1 | trusts more than Ballabar | `TRUSTS` | Tyrion → Frenken | acok-tyrion-15 |
| 2267 | 1 | controls / surveils | `COMMANDS` | Cersei → Tyrion | acok-tyrion-15 |
| 2268 | 1 | has displaced | `(LLM tail)` | Tywin → Tyrion | acok-tyrion-15 |
| 2269 | 1 | killed (in defense of Tyrion) | `KILLS` | Podrick Payne → Ser Mandon Moore | acok-tyrion-15 |
| 2270 | 1 | recalls assessment by | `(LLM tail)` | Tyrion → Jaime (about Ser Mandon) | acok-tyrion-15 |
| 2271 | 1 | trusts with her identity | `TRUSTS` | Arya → Gendry | asos-arya-01 |
| 2272 | 1 | conceals identity from | `(LLM tail)` | Arya → Hot Pie | asos-arya-01 |
| 2273 | 1 | misses / loves | `MOURNS` | Arya → Jon Snow | asos-arya-01 |
| 2274 | 1 | received gift/teaching from | `(LLM tail)` | Arya → Jaqen H'ghar | asos-arya-01 |
| 2275 | 1 | seeks / tries to reach | `SEEKS` | Arya → Robb Stark | asos-arya-01 |
| 2276 | 1 | identifies as daughter of | `(LLM tail)` | Arya → Ned Stark | asos-arya-01 |
| 2277 | 1 | stubborn determination | `(LLM tail)` | Gendry → — | asos-arya-01 |
| 2278 | 1 | has kill list including | `(LLM tail)` | Arya → Ser Gregor, Dunsen, Polliver, Raff the Sweetling, The Tickler, The Hound, Ser Ilyn, Ser Meryn, King Joffrey, Queen Cersei | asos-arya-01 |
| 2279 | 1 | speaks in unison with | `(LLM tail)` | Gendry → Arya | asos-arya-01 |
| 2280 | 1 | adversarial, then submitted | `(LLM tail)` | Arya → Lem Lemoncloak | asos-arya-02 |
| 2281 | 1 | married to / dominates | `(LLM tail)` | Sharna → Husband | asos-arya-02 |
| 2282 | 1 | innkeeper for | `(LLM tail)` | Sharna → Tom, Lem, Anguy | asos-arya-02 |
| 2283 | 1 | employed by / married to | `(LLM tail)` | Husband → Sharna | asos-arya-02 |
| 2284 | 1 | adopted by / works for | `(LLM tail)` | Serving boy / orphan → Sharna and Husband | asos-arya-02 |
| 2285 | 1 | loyal retainer / recognizes | `(LLM tail)` | Harwin → Arya Stark | asos-arya-02 |
| 2286 | 1 | surprising talent | `(LLM tail)` | Hot Pie → Tom Sevenstrings | asos-arya-02 |
| 2287 | 1 | former cupbearer to | `(LLM tail)` | Arya → Roose Bolton | asos-arya-02 |
| 2288 | 1 | Friendship / loss | `COMPANION_OF` | Arya → Hot Pie | asos-arya-03 |
| 2289 | 1 | Only true friend | `(LLM tail)` | Arya → Gendry | asos-arya-03 |
| 2290 | 1 | Emotional bond, guarded trust | `(LLM tail)` | Arya → Harwin | asos-arya-03 |
| 2291 | 1 | Paternal protectiveness toward | `(LLM tail)` | Harwin → Arya | asos-arya-03 |
| 2292 | 1 | Former loyalty to | `(LLM tail)` | Harwin → Eddard Stark | asos-arya-03 |
| 2293 | 1 | Leader of the party | `(LLM tail)` | Greenbeard → Lem, Tom, Anguy, Jack-Be-Lucky, Harwin | asos-arya-03 |
| 2294 | 1 | Healer / spiritual support to | `(LLM tail)` | Thoros → Beric Dondarrion | asos-arya-03 |
| 2295 | 1 | Former bond with | `(LLM tail)` | Arya → Nymeria | asos-arya-03 |
| 2296 | 1 | Kill-list enmity toward | `(LLM tail)` | Arya → Ser Gregor, Dunsen, Polliver, Raff the Sweetling, the Tickler, the Hound, Ser Ilyn, Ser Meryn, Cersei, Joffrey | asos-arya-03 |
| 2297 | 1 | Deference / affection toward | `LOVES` | Hot Pie → Arya | asos-arya-03 |
| 2298 | 1 | Compares to / identifies with | `(LLM tail)` | Harwin → Lyanna Stark / Arya | asos-arya-03 |
| 2299 | 1 | Orchestrated trap against | `(LLM tail)` | Tywin Lannister → Eddard Stark | asos-arya-03 |
| 2300 | 1 | Ambushed | `(LLM tail)` | Gregor Clegane → Beric Dondarrion's force | asos-arya-03 |
| 2301 | 1 | Stole horse from | `(LLM tail)` | Arya → Roose Bolton | asos-arya-03 |
| 2302 | 1 | Captive (for ransom) of | `(LLM tail)` | Arya → Brotherhood Without Banners | asos-arya-04 |
| 2303 | 1 | Trusts / has complicated bond with | `TRUSTS` | Arya → Harwin | asos-arya-04 |
| 2304 | 1 | Friendship / rivalry with | `COMPANION_OF` | Arya → Gendry | asos-arya-04 |
| 2305 | 1 | Resents being controlled by | `RESENTS` | Arya → The outlaws | asos-arya-04 |
| 2306 | 1 | Longs for / worries about rejection from | `MOURNS` | Arya → Catelyn Stark | asos-arya-04 |
| 2307 | 1 | Longs for / identifies with family of | `MOURNS` | Arya → Robb Stark | asos-arya-04 |
| 2308 | 1 | Remembers / taught by | `(LLM tail)` | Arya → Syrio Forel | asos-arya-04 |
| 2309 | 1 | Defends memory of | `PROTECTS` | Arya → King Robert | asos-arya-04 |
| 2310 | 1 | Former lovers with | `(LLM tail)` | Tom Sevenstrings → Lady Smallwood | asos-arya-04 |
| 2311 | 1 | Maternal protectiveness toward | `(LLM tail)` | Lady Smallwood → Arya | asos-arya-04 |
| 2312 | 1 | Protective of / familiar with | `PROTECTS` | Harwin → Arya | asos-arya-04 |
| 2313 | 1 | Former apprentice of | `(LLM tail)` | Gendry → Tobho Mott | asos-arya-04 |
| 2314 | 1 | Taken from master by | `(LLM tail)` | Gendry → Yoren | asos-arya-04 |
| 2315 | 1 | Drinking companion of | `COMPANION_OF` | Thoros of Myr → King Robert | asos-arya-04 |
| 2316 | 1 | Customer of | `(LLM tail)` | Thoros of Myr → Tobho Mott | asos-arya-04 |
| 2317 | 1 | Angry at / amused by | `(LLM tail)` | Lady Smallwood → Tom Sevenstrings | asos-arya-04 |
| 2318 | 1 | Has bad history with | `(LLM tail)` | Tom Sevenstrings → Lord Hoster's son | asos-arya-04 |
| 2319 | 1 | Lost family to | `(LLM tail)` | Jack-Be-Lucky → Lannisters / Lord Piper | asos-arya-04 |
| 2320 | 1 | Lost sons to | `(LLM tail)` | Lord Lychester → Robert's Rebellion | asos-arya-04 |
| 2321 | 1 | Husband serves | `(LLM tail)` | Lady Smallwood → Lord Vance | asos-arya-04 |
| 2322 | 1 | Feels kinship/protectiveness toward | `(LLM tail)` | Arya → Caged northmen | asos-arya-05 |
| 2323 | 1 | Conflicted anger toward | `(LLM tail)` | Arya → Caged northmen | asos-arya-05 |
| 2324 | 1 | Resents class difference with | `RESENTS` | Gendry → Arya | asos-arya-05 |
| 2325 | 1 | Confused/hurt by | `(LLM tail)` | Arya → Gendry | asos-arya-05 |
| 2326 | 1 | Familiar/affectionate toward | `LOVES` | Tansy → Brotherhood | asos-arya-05 |
| 2327 | 1 | Has a son by | `(LLM tail)` | Tom Sevenstrings → Unnamed woman at the Peach | asos-arya-05 |
| 2328 | 1 | Claims paternity from | `(LLM tail)` | Bella → King Robert Baratheon | asos-arya-05 |
| 2329 | 1 | Propositions | `(LLM tail)` | Bella → Gendry | asos-arya-05 |
| 2330 | 1 | Refutes rumor about | `(LLM tail)` | Arya → Lady Catelyn | asos-arya-05 |
| 2331 | 1 | Longs for connection with | `MOURNS` | Arya → Her wolf (dream) | asos-arya-05 |
| 2332 | 1 | Serves as guide/protector to | `SERVES` | Harwin → Arya | asos-arya-05 |
| 2333 | 1 | Desires the death of | `(LLM tail)` | Arya → Sandor Clegane | asos-arya-06 |
| 2334 | 1 | Angry at / calls liar | `(LLM tail)` | Arya → Sansa Stark | asos-arya-06 |
| 2335 | 1 | References with trust | `(LLM tail)` | Arya → Jory (Cassel) | asos-arya-06 |
| 2336 | 1 | Startled/awestruck by | `(LLM tail)` | Arya → Beric Dondarrion | asos-arya-06 |
| 2337 | 1 | Recognizes / contempt for | `(LLM tail)` | Sandor Clegane → Arya | asos-arya-06 |
| 2338 | 1 | Witnessed violence against | `(LLM tail)` | Sandor Clegane → Sansa Stark | asos-arya-06 |
| 2339 | 1 | Witnessed execution of | `(LLM tail)` | Sandor Clegane → Eddard Stark | asos-arya-06 |
| 2340 | 1 | Recognizes from tourneys | `(LLM tail)` | Sandor Clegane → Thoros of Myr | asos-arya-06 |
| 2341 | 1 | Distinguished from | `(LLM tail)` | Sandor Clegane → Gregor Clegane | asos-arya-06 |
| 2342 | 1 | Defeated in melees | `(LLM tail)` | Thoros of Myr → Sandor Clegane | asos-arya-06 |
| 2343 | 1 | Serves the memory of | `SERVES` | Beric Dondarrion → Robert Baratheon | asos-arya-06 |
| 2344 | 1 | Originally sent by | `(LLM tail)` | Beric Dondarrion → Eddard Stark | asos-arya-06 |
| 2345 | 1 | Sentences / fights | `(LLM tail)` | Beric Dondarrion → Sandor Clegane | asos-arya-06 |
| 2346 | 1 | Formerly admired by | `RESPECTS` | Beric Dondarrion → Jeyne Poole | asos-arya-06 |
| 2347 | 1 | Served by (squire) | `(LLM tail)` | Beric Dondarrion → Ned (squire) | asos-arya-06 |
| 2348 | 1 | Reluctant cooperation with | `(LLM tail)` | Mad Huntsman → Brotherhood | asos-arya-06 |
| 2349 | 1 | Protective of / restrains | `PROTECTS` | Harwin → Arya | asos-arya-06 |
| 2350 | 1 | Now worships | `(LLM tail)` | Harwin → R'hllor | asos-arya-06 |
| 2351 | 1 | Confronts / disarms | `(LLM tail)` | Lem Lemoncloak → Sandor Clegane / Arya | asos-arya-06 |
| 2352 | 1 | Brotherhood bowman, claims combat record | `(LLM tail)` | Anguy → Vargo Hoat, Gregor Clegane, Roose Bolton | asos-arya-06 |
| 2353 | 1 | Remembers the dead | `(LLM tail)` | Tom Sevenstrings → Multiple named victims | asos-arya-06 |
| 2354 | 1 | Helps | `(LLM tail)` | Tom Sevenstrings → Sandor Clegane | asos-arya-06 |
| 2355 | 1 | Grief/accusation toward | `MOURNS` | Jack-Be-Lucky → Sandor Clegane | asos-arya-06 |
| 2356 | 1 | Shocked by Beric's scars | `(LLM tail)` | Gendry → Beric Dondarrion | asos-arya-06 |
| 2357 | 1 | Awed by flaming sword | `(LLM tail)` | Gendry → (the magic itself) | asos-arya-06 |
| 2358 | 1 | resurrects / serves | `(LLM tail)` | Thoros → Lord Beric | asos-arya-07 |
| 2359 | 1 | worships / serves as instrument | `WORSHIPS` | Thoros → R'hllor | asos-arya-07 |
| 2360 | 1 | told stories about | `(LLM tail)` | Harwin → Eddard Stark | asos-arya-07 |
| 2361 | 1 | protective of / promises ransom | `PROTECTS` | Lord Beric → Arya Stark | asos-arya-07 |
| 2362 | 1 | pledges service to | `(LLM tail)` | Gendry → Brotherhood / Lord Beric | asos-arya-07 |
| 2363 | 1 | respects justice of | `RESPECTS` | Gendry → Lord Beric | asos-arya-07 |
| 2364 | 1 | mourns / wishes to resurrect | `MOURNS` | Arya → Eddard Stark | asos-arya-07 |
| 2365 | 1 | catalogs losses of | `(LLM tail)` | Arya → Jaqen, Hot Pie, Gendry, Lommy, Yoren, Syrio, Eddard | asos-arya-07 |
| 2366 | 1 | draws strength from | `(LLM tail)` | Arya → Jaqen H'ghar (via coin) | asos-arya-07 |
| 2367 | 1 | hostile toward / demands gold from | `OPPOSES` | Sandor Clegane → Lord Beric / Brotherhood | asos-arya-07 |
| 2368 | 1 | honors trial result for | `(LLM tail)` | Lord Beric → Sandor Clegane | asos-arya-07 |
| 2369 | 1 | defends Clegane's right to live | `PROTECTS` | Thoros → Sandor Clegane | asos-arya-07 |
| 2370 | 1 | misunderstands | `(LLM tail)` | Lem → Lord Beric's resurrections | asos-arya-07 |
| 2371 | 1 | fading bond with | `(LLM tail)` | Lord Beric → His past life | asos-arya-07 |
| 2372 | 1 | grateful to / hosts | `(LLM tail)` | Brown brothers → Brotherhood | asos-arya-07 |
| 2373 | 1 | objects to faith of | `(LLM tail)` | Young novice → Thoros / R'hllor | asos-arya-07 |
| 2374 | 1 | defends / argues for | `PROTECTS` | Lem → R'hllor | asos-arya-07 |
| 2375 | 1 | competitive camaraderie with | `COMPANION_OF` | Anguy → Jack-Be-Lucky | asos-arya-07 |
| 2376 | 1 | desires to learn from | `(LLM tail)` | Arya → Anguy | asos-arya-07 |
| 2377 | 1 | fiercely protective of | `(LLM tail)` | Arya → Eddard Stark (memory) | asos-arya-08 |
| 2378 | 1 | captured by | `(LLM tail)` | Arya → Sandor Clegane | asos-arya-08 |
| 2379 | 1 | revulsed by | `(LLM tail)` | Ghost of High Heart → Arya | asos-arya-08 |
| 2380 | 1 | existentially despairing | `(LLM tail)` | Lord Beric → Thoros | asos-arya-08 |
| 2381 | 1 | irritable about | `(LLM tail)` | Lem Lemoncloak → Arya | asos-arya-08 |
| 2382 | 1 | betrothed aunt to | `BETROTHED_TO` | Edric Dayne → Lord Beric | asos-arya-08 |
| 2383 | 1 | respectful of past | `RESPECTS` | Thoros → King Robert | asos-arya-08 |
| 2384 | 1 | personally connected to | `(LLM tail)` | Ghost of High Heart → Summerhall | asos-arya-08 |
| 2385 | 1 | Hostage/captive of (antagonistic) | `(LLM tail)` | Arya Stark → Sandor Clegane | asos-arya-09 |
| 2386 | 1 | Plans to ransom | `(LLM tail)` | Sandor Clegane → Arya Stark | asos-arya-09 |
| 2387 | 1 | Former protector of | `(LLM tail)` | Sandor Clegane → Sansa Stark | asos-arya-09 |
| 2388 | 1 | Rejected allegiance to | `(LLM tail)` | Sandor Clegane → House Lannister / Joffrey | asos-arya-09 |
| 2389 | 1 | Cheated | `(LLM tail)` | Sandor Clegane → Bent-backed ferryman | asos-arya-09 |
| 2390 | 1 | captive/charge of | `(LLM tail)` | Arya Stark → Sandor Clegane | asos-arya-10 |
| 2391 | 1 | rival/combatant (past) to | `(LLM tail)` | Sandor Clegane → Ser Donnel Haigh | asos-arya-10 |
| 2392 | 1 | Grief and desperate love | `MOURNS` | Arya → Robb Stark | asos-arya-11 |
| 2393 | 1 | Desperate love, desire to rescue | `LOVES` | Arya → Catelyn Stark | asos-arya-11 |
| 2394 | 1 | Protective (through violence) | `(LLM tail)` | Sandor Clegane → Arya | asos-arya-11 |
| 2395 | 1 | Memory of lost friendship | `COMPANION_OF` | Arya → Mycah | asos-arya-11 |
| 2396 | 1 | Killer of (recalled) | `(LLM tail)` | Sandor Clegane → Mycah | asos-arya-11 |
| 2397 | 1 | Former student | `(LLM tail)` | Arya → Syrio Forel | asos-arya-11 |
| 2398 | 1 | Betrayal of | `(LLM tail)` | House Frey → House Stark / Robb Stark | asos-arya-11 |
| 2399 | 1 | Bond with mount | `(LLM tail)` | Sandor Clegane → Stranger | asos-arya-11 |
| 2400 | 1 | Recalled friendship | `COMPANION_OF` | Arya → Gendry | asos-arya-11 |
| 2401 | 1 | Captive / reluctant companion of | `COMPANION_OF` | Arya Stark → Sandor Clegane | asos-arya-12 |
| 2402 | 1 | Feels used by | `(LLM tail)` | Arya Stark → Lord Beric Dondarrion | asos-arya-12 |
| 2403 | 1 | Spiritually bonded with | `BONDED_TO` | Arya Stark → Nymeria | asos-arya-12 |
| 2404 | 1 | Pack leader of | `(LLM tail)` | Nymeria → Wolf pack | asos-arya-12 |
| 2405 | 1 | Mourning / seeking | `MOURNS` | Nymeria → Catelyn Stark | asos-arya-12 |
| 2406 | 1 | Captor / protector of | `CAPTURES` | Sandor Clegane → Arya Stark | asos-arya-12 |
| 2407 | 1 | Former servant of / now independent from | `(LLM tail)` | Sandor Clegane → Joffrey Baratheon | asos-arya-12 |
| 2408 | 1 | Antagonistic toward (implied) | `OPPOSES` | Sandor Clegane → Gregor Clegane | asos-arya-12 |
| 2409 | 1 | Referenced past interaction with | `(LLM tail)` | Sandor Clegane → Sansa Stark | asos-arya-12 |
| 2410 | 1 | Fears reputation of | `FEARS` | Village elder → Sandor Clegane | asos-arya-12 |
| 2411 | 1 | Attached to / follows | `(LLM tail)` | Village elder's daughter → Arya Stark | asos-arya-12 |
| 2412 | 1 | Captor-captive / reluctant companionship | `CAPTURES` | Arya → Sandor Clegane | asos-arya-13 |
| 2413 | 1 | Recovers Needle from | `(LLM tail)` | Arya → Polliver (dead) | asos-arya-13 |
| 2414 | 1 | Enmity / estrangement | `(LLM tail)` | Sandor Clegane → Gregor Clegane | asos-arya-13 |
| 2415 | 1 | Confesses guilt toward | `(LLM tail)` | Sandor Clegane → Sansa Stark | asos-arya-13 |
| 2416 | 1 | Hatred tempered by complex feelings | `HATES` | Arya → Sandor Clegane | asos-arya-13 |
| 2417 | 1 | Memory / sisterly bond | `(LLM tail)` | Arya → Sansa Stark | asos-arya-13 |
| 2418 | 1 | Distant connection | `(LLM tail)` | Arya → Jon Snow | asos-arya-13 |
| 2419 | 1 | Protective nickname | `(LLM tail)` | Sandor Clegane → Sansa Stark | asos-arya-13 |
| 2420 | 1 | Cheats | `(LLM tail)` | Horse trader woman → Arya | asos-arya-13 |
| 2421 | 1 | Serves / recognizes the coin | `SERVES` | Captain of Titan's Daughter → Arya / Jaqen H'ghar's coin | asos-arya-13 |
| 2422 | 1 | Uses Jaqen H'ghar's teaching | `(LLM tail)` | Arya → Jaqen H'ghar (remembered) | asos-arya-13 |
| 2423 | 1 | Warg-bonded to | `WARGS_INTO` | Bran → Summer | asos-bran-01 |
| 2424 | 1 | Resistant student of | `(LLM tail)` | Bran → Jojen Reed | asos-bran-01 |
| 2425 | 1 | Mourns loss of | `MOURNS` | Bran → Winterfell | asos-bran-01 |
| 2426 | 1 | Teacher/guide to | `TUTORS` | Jojen Reed → Bran | asos-bran-01 |
| 2427 | 1 | Sibling tension with | `(LLM tail)` | Jojen Reed → Meera Reed | asos-bran-01 |
| 2428 | 1 | Protector/provider for | `(LLM tail)` | Meera Reed → Bran | asos-bran-01 |
| 2429 | 1 | Senses | `(LLM tail)` | Summer → Other Stark direwolves | asos-bran-01 |
| 2430 | 1 | Questions leadership of | `(LLM tail)` | Bran → Jojen | asos-bran-01 |
| 2431 | 1 | Considers loyalty of | `(LLM tail)` | Bran → Northern lords | asos-bran-01 |
| 2432 | 1 | carried by / dependent on | `(LLM tail)` | Bran Stark → Hodor | asos-bran-02 |
| 2433 | 1 | friendly teasing with | `COMPANION_OF` | Bran Stark → Meera Reed | asos-bran-02 |
| 2434 | 1 | hunts and provides for | `(LLM tail)` | Meera Reed → The group | asos-bran-02 |
| 2435 | 1 | hunts for | `(LLM tail)` | Summer → The group | asos-bran-02 |
| 2436 | 1 | protective (insists on secrecy) toward | `(LLM tail)` | Jojen Reed → Bran Stark | asos-bran-02 |
| 2437 | 1 | loyal to House Stark | `SERVES` | The Liddle → Bran Stark / House Stark | asos-bran-02 |
| 2438 | 1 | mourns / worries about | `MOURNS` | Bran Stark → Old Nan | asos-bran-02 |
| 2439 | 1 | uncertain judgment of | `(LLM tail)` | Bran Stark → Theon Greyjoy | asos-bran-02 |
| 2440 | 1 | misses and worries about | `MOURNS` | Bran Stark → Rickon Stark | asos-bran-02 |
| 2441 | 1 | feels gratitude toward | `(LLM tail)` | Bran Stark → The Liddle | asos-bran-02 |
| 2442 | 1 | finds shelter for | `(LLM tail)` | Summer → The group | asos-bran-02 |
| 2443 | 1 | responds to his name | `(LLM tail)` | Hodor → Bran Stark | asos-bran-02 |
| 2444 | 1 | shelters | `(LLM tail)` | The quiet wolf (in story) → The crannogman | asos-bran-02 |
| 2445 | 1 | sings sadly for / sought by the king to find mystery knight | `(LLM tail)` | The dragon prince (in story) → The assembled lords / the mystery knight | asos-bran-02 |
| 2446 | 1 | is carried by / depends on | `(LLM tail)` | Bran → Hodor | asos-bran-03 |
| 2447 | 1 | warges into (first time) | `WARGS_INTO` | Bran → Hodor | asos-bran-03 |
| 2448 | 1 | protects / leads | `PROTECTS` | Meera → Bran | asos-bran-03 |
| 2449 | 1 | advises / counsels | `ADVISES` | Jojen → Bran | asos-bran-03 |
| 2450 | 1 | wargs into (with difficulty) | `WARGS_INTO` | Bran → Hodor | asos-bran-04 |
| 2451 | 1 | brotherly affection for | `LOVES` | Bran → Jon Snow | asos-bran-04 |
| 2452 | 1 | decides to trust | `(LLM tail)` | Bran → Samwell Tarly | asos-bran-04 |
| 2453 | 1 | asks secrecy from | `(LLM tail)` | Bran → Samwell Tarly | asos-bran-04 |
| 2454 | 1 | considers best friend | `(LLM tail)` | Samwell Tarly → Jon Snow | asos-bran-04 |
| 2455 | 1 | guided by | `(LLM tail)` | Samwell Tarly → Coldhands | asos-bran-04 |
| 2456 | 1 | cannot pass | `(LLM tail)` | Coldhands → The Wall | asos-bran-04 |
| 2457 | 1 | ruled with | `(LLM tail)` | Night's King (story) → Corpse queen | asos-bran-04 |
| 2458 | 1 | violated guest right of | `(LLM tail)` | The Rat Cook (story) → The Andal king | asos-bran-04 |
| 2459 | 1 | loved but returned to justice | `LOVES` | Lord Ryswell (story) → Lord Ryswell's son | asos-bran-04 |
| 2460 | 1 | castellan of | `(LLM tail)` | Ser Desmond Grell → Riverrun | asos-catelyn-01 |
| 2461 | 1 | lifelong servant of | `(LLM tail)` | Ser Desmond Grell → House Tully | asos-catelyn-01 |
| 2462 | 1 | steward of | `SERVES` | Utherydes Wayn → Lord Hoster Tully | asos-catelyn-01 |
| 2463 | 1 | was married to | `(LLM tail)` | Lysa Arryn → Jon Arryn | asos-catelyn-01 |
| 2464 | 1 | arranged marriage of | `(LLM tail)` | Lord Hoster → Lysa to Jon Arryn | asos-catelyn-01 |
| 2465 | 1 | murdered (believed) | `KILLS` | Theon Greyjoy → Bran and Rickon | asos-catelyn-01 |
| 2466 | 1 | sent ravens to | `(LLM tail)` | Edmure → Lord Bolton (Roose) | asos-catelyn-01 |
| 2467 | 1 | freed | `(LLM tail)` | Catelyn → Jaime Lannister | asos-catelyn-01 |
| 2468 | 1 | escorting | `(LLM tail)` | Brienne → Jaime Lannister | asos-catelyn-01 |
| 2469 | 1 | conflict with | `(LLM tail)` | Catelyn → Edmure | asos-catelyn-01 |
| 2470 | 1 | Son, seeks forgiveness for his own act | `(LLM tail)` | Robb Stark → Catelyn Stark | asos-catelyn-02 |
| 2471 | 1 | Mother, seeking forgiveness | `(LLM tail)` | Catelyn Stark → Robb Stark | asos-catelyn-02 |
| 2472 | 1 | Hostile, accuses of treason | `(LLM tail)` | Lord Rickard Karstark → Catelyn Stark | asos-catelyn-02 |
| 2473 | 1 | Defends against Karstark | `PROTECTS` | Robb Stark → Catelyn Stark | asos-catelyn-02 |
| 2474 | 1 | Supportive but condescending | `(LLM tail)` | The Greatjon → Catelyn Stark | asos-catelyn-02 |
| 2475 | 1 | Sympathetic | `(LLM tail)` | Lady Mormont → Catelyn Stark | asos-catelyn-02 |
| 2476 | 1 | Warm, affectionate | `LOVES` | Ser Brynden Tully → Catelyn Stark | asos-catelyn-02 |
| 2477 | 1 | Strained, avoiding | `(LLM tail)` | Edmure Tully → Catelyn Stark | asos-catelyn-02 |
| 2478 | 1 | In love, protective | `LOVES` | Robb Stark → Jeyne Westerling | asos-catelyn-02 |
| 2479 | 1 | Dutiful acceptance, critical assessment | `(LLM tail)` | Catelyn Stark → Jeyne Westerling | asos-catelyn-02 |
| 2480 | 1 | Harshly critical | `(LLM tail)` | Ser Brynden Tully → Edmure Tully | asos-catelyn-02 |
| 2481 | 1 | Disappointed, rebuking | `(LLM tail)` | Robb Stark → Edmure Tully | asos-catelyn-02 |
| 2482 | 1 | Distancing himself from | `(LLM tail)` | Robb Stark → Grey Wind | asos-catelyn-02 |
| 2483 | 1 | Concerned, insistent | `(LLM tail)` | Catelyn Stark → Robb Stark (re: Grey Wind) | asos-catelyn-02 |
| 2484 | 1 | Anxious around | `(LLM tail)` | Jeyne Westerling → Grey Wind | asos-catelyn-02 |
| 2485 | 1 | Demands vengeance against | `(LLM tail)` | Lord Rickard Karstark → Jaime Lannister | asos-catelyn-02 |
| 2486 | 1 | Strategic counsel to | `ADVISES` | Catelyn Stark → Robb Stark | asos-catelyn-02 |
| 2487 | 1 | Broken alliance with | `ALLIES_WITH` | Robb Stark → House Frey | asos-catelyn-02 |
| 2488 | 1 | Rivalry/competition with | `(LLM tail)` | Edmure Tully → Robb Stark | asos-catelyn-02 |
| 2489 | 1 | Cool but courteous toward | `(LLM tail)` | Galbart Glover → Catelyn Stark | asos-catelyn-02 |
| 2490 | 1 | Almost icy toward | `(LLM tail)` | Jonos Bracken → Catelyn Stark | asos-catelyn-02 |
| 2491 | 1 | Eager squire to | `(LLM tail)` | Rollam Westerling → Robb Stark | asos-catelyn-02 |
| 2492 | 1 | Blames herself for actions that led to | `OPPOSES` | Catelyn → Tion Frey & Willem Lannister (deaths) | asos-catelyn-03 |
| 2493 | 1 | Blames directly | `OPPOSES` | Rickard Karstark → Catelyn | asos-catelyn-03 |
| 2494 | 1 | Defies / disowns as king | `OPPOSES` | Rickard Karstark → Robb | asos-catelyn-03 |
| 2495 | 1 | Executes (as king and kinsman) | `EXECUTES` | Robb → Rickard Karstark | asos-catelyn-03 |
| 2496 | 1 | Loyal enforcer to | `(LLM tail)` | Greatjon Umber → Robb | asos-catelyn-03 |
| 2497 | 1 | Urges clemency to | `(LLM tail)` | Edmure Tully → Robb | asos-catelyn-03 |
| 2498 | 1 | Pragmatic advisor to | `(LLM tail)` | Brynden Tully (Blackfish) → Robb | asos-catelyn-03 |
| 2499 | 1 | Assesses | `(LLM tail)` | Catelyn → Lysa Arryn | asos-catelyn-03 |
| 2500 | 1 | Seeks guidance from | `SEEKS` | Jeyne Westerling → Catelyn | asos-catelyn-03 |
| 2501 | 1 | Counsels / mentors | `TUTORS` | Catelyn → Jeyne Westerling | asos-catelyn-03 |
| 2502 | 1 | Devoted wife to | `(LLM tail)` | Jeyne Westerling → Robb | asos-catelyn-03 |
| 2503 | 1 | Provides fertility aid to | `(LLM tail)` | Jeyne's mother → Jeyne | asos-catelyn-03 |
| 2504 | 1 | Mourns / tends | `MOURNS` | Catelyn → Lord Hoster Tully | asos-catelyn-03 |
| 2505 | 1 | Models kingship on | `(LLM tail)` | Robb → Ned Stark | asos-catelyn-03 |
| 2506 | 1 | Deserted / betrayed | `(LLM tail)` | Karstark men → Robb | asos-catelyn-03 |
| 2507 | 1 | Seeks vengeance on | `SEEKS` | Rickard Karstark → Jaime Lannister | asos-catelyn-03 |
| 2508 | 1 | Claimed past loyalty to | `(LLM tail)` | Rickard Karstark → Robb / Ned Stark | asos-catelyn-03 |
| 2509 | 1 | Sister, advisor to | `SIBLING_OF` | Catelyn → Edmure | asos-catelyn-04 |
| 2510 | 1 | Daughter mourning | `MOURNS` | Catelyn → Lord Hoster | asos-catelyn-04 |
| 2511 | 1 | Liege lord, diplomatic to | `(LLM tail)` | Robb → Lothar Frey | asos-catelyn-04 |
| 2512 | 1 | In tension with | `(LLM tail)` | Robb → Catelyn | asos-catelyn-04 |
| 2513 | 1 | Husband, affectionate to | `LOVES` | Robb → Jeyne Westerling | asos-catelyn-04 |
| 2514 | 1 | Comfortable with | `(LLM tail)` | Robb → Rollam/Raynald Westerling | asos-catelyn-04 |
| 2515 | 1 | Grieving son of | `MOURNS` | Edmure → Lord Hoster | asos-catelyn-04 |
| 2516 | 1 | Shamed by failure before | `(LLM tail)` | Edmure → Brynden | asos-catelyn-04 |
| 2517 | 1 | Supportive uncle to | `UNCLE_OF` | Brynden → Edmure/Catelyn | asos-catelyn-04 |
| 2518 | 1 | Diplomatic envoy for | `(LLM tail)` | Lothar Frey → Lord Walder Frey | asos-catelyn-04 |
| 2519 | 1 | Distrust/contempt for | `DISTRUSTS` | Catelyn → Lord Walder Frey | asos-catelyn-04 |
| 2520 | 1 | Guilt over | `(LLM tail)` | Robb → Bran and Rickon (believed dead) | asos-catelyn-04 |
| 2521 | 1 | Guilt/hope regarding | `(LLM tail)` | Catelyn → Jaime Lannister release | asos-catelyn-04 |
| 2522 | 1 | Regret toward | `(LLM tail)` | Robb → Sansa | asos-catelyn-04 |
| 2523 | 1 | husband of, deeply attached to | `(LLM tail)` | Robb Stark → Jeyne Westerling | asos-catelyn-05 |
| 2524 | 1 | resents (somewhat) | `RESENTS` | Robb Stark → Catelyn Stark | asos-catelyn-05 |
| 2525 | 1 | mother of, advises | `(LLM tail)` | Catelyn Stark → Robb Stark | asos-catelyn-05 |
| 2526 | 1 | diplomatic envoy to | `(LLM tail)` | Lame Lothar Frey → Edmure Tully / Robb's court | asos-catelyn-05 |
| 2527 | 1 | brother of, avoids after rebuke | `SIBLING_OF` | Edmure Tully → Catelyn Stark | asos-catelyn-05 |
| 2528 | 1 | understanding toward | `(LLM tail)` | Maege Mormont → Catelyn Stark | asos-catelyn-05 |
| 2529 | 1 | serves/scouts for | `SERVES` | Galbart Glover → Robb Stark | asos-catelyn-05 |
| 2530 | 1 | trusts, wants as heir | `(LLM tail)` | Robb Stark → Jon Snow | asos-catelyn-05 |
| 2531 | 1 | distrusts (for succession) | `DISTRUSTS` | Catelyn Stark → Jon Snow | asos-catelyn-05 |
| 2532 | 1 | hopes in, worries for | `(LLM tail)` | Catelyn Stark → Brienne of Tarth | asos-catelyn-05 |
| 2533 | 1 | remembers fondly (childhood) | `(LLM tail)` | Catelyn Stark → Petyr Baelish | asos-catelyn-05 |
| 2534 | 1 | remembers with mixed feelings | `(LLM tail)` | Catelyn Stark → Eddard Stark, Brandon Stark | asos-catelyn-05 |
| 2535 | 1 | distrusted | `DISTRUSTS` | Hoster Tully → Walder Frey | asos-catelyn-05 |
| 2536 | 1 | protects, trusted with defense of | `(LLM tail)` | Brynden Tully (Blackfish) → Riverrun / Jeyne Westerling | asos-catelyn-05 |
| 2537 | 1 | unhappy at | `(LLM tail)` | Lynesse Hightower → Bear Island / the north | asos-catelyn-05 |
| 2538 | 1 | seized power from / murdered (Lord Botley) | `KILLS` | Euron Greyjoy → Balon Greyjoy's succession | asos-catelyn-05 |
| 2539 | 1 | assigns to Moat Cailin rearguard | `(LLM tail)` | Robb Stark → Roose Bolton | asos-catelyn-05 |
| 2540 | 1 | leads van for | `COMMANDS` | Greatjon → Robb Stark | asos-catelyn-05 |
| 2541 | 1 | offers refuge to | `(LLM tail)` | Jason Mallister → Catelyn Stark | asos-catelyn-05 |
| 2542 | 1 | perceives Seagard stay as | `(LLM tail)` | Catelyn Stark → imprisonment | asos-catelyn-05 |
| 2543 | 1 | strategic thinking about | `(LLM tail)` | Robb Stark → Victarion Greyjoy | asos-catelyn-05 |
| 2544 | 1 | Mother advising son | `(LLM tail)` | Catelyn → Robb | asos-catelyn-06 |
| 2545 | 1 | Owes amends to | `(LLM tail)` | Robb → Lord Walder Frey | asos-catelyn-06 |
| 2546 | 1 | Dominant/humiliating toward | `(LLM tail)` | Lord Walder Frey → Robb | asos-catelyn-06 |
| 2547 | 1 | Betrothed to (weeping) | `BETROTHED_TO` | Roslin → Edmure | asos-catelyn-06 |
| 2548 | 1 | Evaluates | `(LLM tail)` | Catelyn → Roslin | asos-catelyn-06 |
| 2549 | 1 | Gracious host toward | `(LLM tail)` | Lame Lothar → Catelyn | asos-catelyn-06 |
| 2550 | 1 | Brother worried about | `SIBLING_OF` | Ser Wendel Manderly → Ser Wylis Manderly | asos-catelyn-06 |
| 2551 | 1 | Recalls with comparison | `(LLM tail)` | Catelyn → Eddard Stark | asos-catelyn-06 |
| 2552 | 1 | Strategically separates | `(LLM tail)` | Robb → Ser Raynald Westerling | asos-catelyn-06 |
| 2553 | 1 | Sibling to | `(LLM tail)` | Benfrey → Roslin | asos-catelyn-06 |
| 2554 | 1 | Disparaging toward | `(LLM tail)` | Lord Walder → His own family | asos-catelyn-06 |
| 2555 | 1 | Mother of (mourning) | `PARENT_OF` | Catelyn → Bran, Rickon, Arya, Sansa | asos-catelyn-07 |
| 2556 | 1 | Widow of (mourning/longing) | `SPOUSE_OF` | Catelyn → Ned Stark | asos-catelyn-07 |
| 2557 | 1 | Newlywed husband of | `(LLM tail)` | Edmure → Roslin Frey | asos-catelyn-07 |
| 2558 | 1 | Bride of (with foreknowledge of massacre) | `(LLM tail)` | Roslin → Edmure | asos-catelyn-07 |
| 2559 | 1 | Obeys (grudgingly) | `SERVES` | Robb → Walder Frey | asos-catelyn-07 |
| 2560 | 1 | King of | `(LLM tail)` | Robb → Northern and river lords | asos-catelyn-07 |
| 2561 | 1 | Loyal followers of | `(LLM tail)` | Robb → Smalljon, Robin Flint, Dacey, Patrek Mallister | asos-catelyn-07 |
| 2562 | 1 | Threatens (veiled) | `OPPOSES` | Roose Bolton → Walder Frey | asos-catelyn-07 |
| 2563 | 1 | Orchestrates massacre of | `(LLM tail)` | Walder Frey → Robb Stark and his followers | asos-catelyn-07 |
| 2564 | 1 | Hostage-taker/killer of | `(LLM tail)` | Catelyn → Jinglebell (Aegon) | asos-catelyn-07 |
| 2565 | 1 | Complicit in massacre / kills | `(LLM tail)` | Ser Ryman Frey → Dacey Mormont | asos-catelyn-07 |
| 2566 | 1 | Hamstrings | `(LLM tail)` | Black Walder → One of the Vances | asos-catelyn-07 |
| 2567 | 1 | Shields/dies for | `(LLM tail)` | Smalljon Umber → Robb Stark | asos-catelyn-07 |
| 2568 | 1 | Drinking companion/rival of | `COMPANION_OF` | Greatjon Umber → Merrett Frey, Ser Whalen, Petyr Pimple | asos-catelyn-07 |
| 2569 | 1 | Loyal to (absent) | `SERVES` | Olyvar Frey → Robb Stark | asos-catelyn-07 |
| 2570 | 1 | Thinks of last | `(LLM tail)` | Robb → Grey Wind | asos-catelyn-07 |
| 2571 | 1 | Sends regards from | `(LLM tail)` | The killer (Bolton) → Jaime Lannister | asos-catelyn-07 |
| 2572 | 1 | Romantically pursues | `(LLM tail)` | Ser Jorah Mormont → Daenerys | asos-daenerys-01 |
| 2573 | 1 | Respects / served under | `RESPECTS` | Arstan Whitebeard → King Aerys II | asos-daenerys-01 |
| 2574 | 1 | Mixed feelings toward (deceased) | `(LLM tail)` | Daenerys → Viserys Targaryen | asos-daenerys-01 |
| 2575 | 1 | Recalls with love (deceased) | `LOVES` | Daenerys → Khal Drogo | asos-daenerys-01 |
| 2576 | 1 | Closest friend (deceased) | `(LLM tail)` | Rhaegar Targaryen → Arthur Dayne | asos-daenerys-01 |
| 2577 | 1 | Close companion (deceased) | `COMPANION_OF` | Rhaegar Targaryen → Jon Connington | asos-daenerys-01 |
| 2578 | 1 | Uncertain toward | `(LLM tail)` | Daenerys → Quaithe of the Shadow | asos-daenerys-01 |
| 2579 | 1 | Fears retaliation from | `FEARS` | Daenerys → Pyat Pree | asos-daenerys-01 |
| 2580 | 1 | deceives / maintains ruse against | `DECEIVES` | Daenerys → Kraznys mo Nakloz | asos-daenerys-02 |
| 2581 | 1 | serves / diplomatically protects | `SERVES` | Translator (slave girl) → Kraznys mo Nakloz | asos-daenerys-02 |
| 2582 | 1 | shows subtle honesty toward | `(LLM tail)` | Translator (slave girl) → Daenerys | asos-daenerys-02 |
| 2583 | 1 | owns / abuses | `OWNS` | Kraznys mo Nakloz → Translator (slave girl) | asos-daenerys-02 |
| 2584 | 1 | advises against slave purchase | `ADVISES` | Arstan Whitebeard → Daenerys | asos-daenerys-02 |
| 2585 | 1 | respects / values counsel of | `RESPECTS` | Daenerys → Arstan Whitebeard | asos-daenerys-02 |
| 2586 | 1 | trusts strategically | `TRUSTS` | Daenerys → Ser Jorah Mormont | asos-daenerys-02 |
| 2587 | 1 | mourns / yearns for | `MOURNS` | Daenerys → Khal Drogo | asos-daenerys-02 |
| 2588 | 1 | freed / asserts equality with | `(LLM tail)` | Daenerys → Irri | asos-daenerys-02 |
| 2589 | 1 | puzzled by Jorah's distrust of | `(LLM tail)` | Daenerys → Arstan Whitebeard | asos-daenerys-02 |
| 2590 | 1 | loyal to / familiar with | `SERVES` | Strong Belwas → Daenerys | asos-daenerys-02 |
| 2591 | 1 | increasingly difficult for | `(LLM tail)` | Drogon → Daenerys | asos-daenerys-02 |
| 2592 | 1 | absolute power over | `(LLM tail)` | Kraznys mo Nakloz → Unsullied | asos-daenerys-02 |
| 2593 | 1 | frees/takes into service | `(LLM tail)` | Daenerys → Missandei | asos-daenerys-03 |
| 2594 | 1 | rebukes/disciplines | `(LLM tail)` | Daenerys → Arstan Whitebeard | asos-daenerys-03 |
| 2595 | 1 | advises (disagreement) | `ADVISES` | Arstan Whitebeard → Daenerys | asos-daenerys-03 |
| 2596 | 1 | contempt/hatred toward | `HATES` | Daenerys → Kraznys mo Nakloz | asos-daenerys-03 |
| 2597 | 1 | familial bond | `(LLM tail)` | Missandei → Three unnamed Unsullied | asos-daenerys-03 |
| 2598 | 1 | authority over (lost) | `COMMANDS` | Old Grazdan → Unsullied | asos-daenerys-03 |
| 2599 | 1 | resents (memory) | `RESENTS` | Daenerys → Viserys | asos-daenerys-03 |
| 2600 | 1 | grief/loss for | `MOURNS` | Daenerys → Drogo | asos-daenerys-03 |
| 2601 | 1 | cryptic advisor to | `(LLM tail)` | Quaithe → Daenerys | asos-daenerys-03 |
| 2602 | 1 | follows | `(LLM tail)` | Sallor the Bald → Prendahl na Ghezn | asos-daenerys-04 |
| 2603 | 1 | attracted to / pledges loyalty to | `(LLM tail)` | Daario Naharis → Daenerys | asos-daenerys-04 |
| 2604 | 1 | romantically desires | `(LLM tail)` | Ser Jorah → Daenerys | asos-daenerys-04 |
| 2605 | 1 | rejects romantically | `(LLM tail)` | Daenerys → Ser Jorah | asos-daenerys-04 |
| 2606 | 1 | values as advisor | `(LLM tail)` | Daenerys → Ser Jorah | asos-daenerys-04 |
| 2607 | 1 | attempts to bribe | `(LLM tail)` | Grazdan mo Eraz → Daenerys | asos-daenerys-04 |
| 2608 | 1 | recalls / mourns | `MOURNS` | Daenerys → Mirri Maz Duur's prophecy | asos-daenerys-04 |
| 2609 | 1 | admires / curious about | `RESPECTS` | Daenerys → Rhaegar Targaryen | asos-daenerys-04 |
| 2610 | 1 | blamed / abused | `(LLM tail)` | Viserys → Daenerys | asos-daenerys-04 |
| 2611 | 1 | knew / served | `(LLM tail)` | Arstan Whitebeard → Rhaegar Targaryen | asos-daenerys-04 |
| 2612 | 1 | crowned | `(LLM tail)` | Rhaegar → Lyanna Stark | asos-daenerys-04 |
| 2613 | 1 | revere | `(LLM tail)` | Freed slaves → Daenerys | asos-daenerys-04 |
| 2614 | 1 | commands/queen of | `COMMANDS` | Daenerys → Aggo, Jhogo, Rakharo | asos-daenerys-05 |
| 2615 | 1 | trusts counsel of | `TRUSTS` | Daenerys → Ser Jorah | asos-daenerys-05 |
| 2616 | 1 | sexually attracted to | `(LLM tail)` | Daenerys → Daario Naharis | asos-daenerys-05 |
| 2617 | 1 | conflicted about/furious at | `(LLM tail)` | Daenerys → Ser Jorah | asos-daenerys-05 |
| 2618 | 1 | mother-figure to | `(LLM tail)` | Daenerys → Freedmen | asos-daenerys-05 |
| 2619 | 1 | jealous of / dislikes | `(LLM tail)` | Ser Jorah → Daario | asos-daenerys-05 |
| 2620 | 1 | adversarial toward | `(LLM tail)` | Arstan/Barristan → Ser Jorah | asos-daenerys-05 |
| 2621 | 1 | informed on | `(LLM tail)` | Ser Jorah → Daenerys | asos-daenerys-05 |
| 2622 | 1 | amiable toward | `(LLM tail)` | Brown Ben Plumm → Daenerys | asos-daenerys-05 |
| 2623 | 1 | affinity toward | `(LLM tail)` | Viserion → Brown Ben Plumm | asos-daenerys-05 |
| 2624 | 1 | servant/protector of | `(LLM tail)` | Strong Belwas → Daenerys | asos-daenerys-05 |
| 2625 | 1 | squire/attendant to | `(LLM tail)` | Arstan/Barristan → Strong Belwas | asos-daenerys-05 |
| 2626 | 1 | desires/courts | `(LLM tail)` | Daario → Daenerys | asos-daenerys-05 |
| 2627 | 1 | loyal soldier to | `(LLM tail)` | Grey Worm → Daenerys | asos-daenerys-05 |
| 2628 | 1 | former bodyguard to | `(LLM tail)` | Brown Ben Plumm → Oznak's uncle | asos-daenerys-05 |
| 2629 | 1 | playful affection toward | `LOVES` | Jhiqui → Strong Belwas | asos-daenerys-05 |
| 2630 | 1 | remembers / lost to wound | `(LLM tail)` | Dany → Khal Drogo | asos-daenerys-05 |
| 2631 | 1 | Queen/ruler over | `(LLM tail)` | Daenerys → Meereen | asos-daenerys-06 |
| 2632 | 1 | Fond of / trusts | `LOVES` | Daenerys → Missandei | asos-daenerys-06 |
| 2633 | 1 | Forgives/restores | `(LLM tail)` | Daenerys → Ser Barristan Selmy | asos-daenerys-06 |
| 2634 | 1 | Banishes | `(LLM tail)` | Daenerys → Ser Jorah Mormont | asos-daenerys-06 |
| 2635 | 1 | Loves/loved | `LOVES` | Ser Jorah → Daenerys | asos-daenerys-06 |
| 2636 | 1 | Former spy for | `(LLM tail)` | Ser Jorah → Varys | asos-daenerys-06 |
| 2637 | 1 | Devoted to / possessive of | `(LLM tail)` | Daario → Daenerys | asos-daenerys-06 |
| 2638 | 1 | Knows of | `(LLM tail)` | Missandei → Naath (homeland) | asos-daenerys-06 |
| 2639 | 1 | Proposes alliance/marriage to | `ALLIES_WITH` | King Cleon → Daenerys | asos-daenerys-06 |
| 2640 | 1 | Growing bolder | `(LLM tail)` | Dragons (all three) → — | asos-daenerys-06 |
| 2641 | 1 | Remembers with loss | `(LLM tail)` | Dany → Ser Willem Darry | asos-daenerys-06 |
| 2642 | 1 | rowed to Storm's End | `(LLM tail)` | Davos → Melisandre | asos-davos-01 |
| 2643 | 1 | converted | `(LLM tail)` | Melisandre → Selyse Baratheon | asos-davos-01 |
| 2644 | 1 | influenced/converted | `(LLM tail)` | Melisandre → Stannis Baratheon | asos-davos-01 |
| 2645 | 1 | originates from | `(LLM tail)` | Melisandre → Asshai | asos-davos-01 |
| 2646 | 1 | burned the Seven at urging of | `(LLM tail)` | Stannis → Melisandre | asos-davos-01 |
| 2647 | 1 | burned godswood at urging of | `(LLM tail)` | Stannis → Melisandre | asos-davos-01 |
| 2648 | 1 | served as oarmaster on | `(LLM tail)` | Maric Seaworth → Fury | asos-davos-01 |
| 2649 | 1 | served as second on | `(LLM tail)` | Matthos Seaworth → Black Betha | asos-davos-01 |
| 2650 | 1 | has wife | `(LLM tail)` | Davos → Unnamed wife | asos-davos-01 |
| 2651 | 1 | at war with | `(LLM tail)` | Stannis Baratheon → Joffrey | asos-davos-01 |
| 2652 | 1 | hatred/vendetta toward | `HATES` | Davos Seaworth → Melisandre | asos-davos-02 |
| 2653 | 1 | parental love for | `LOVES` | Davos Seaworth → Devan Seaworth | asos-davos-02 |
| 2654 | 1 | friendship toward | `COMPANION_OF` | Salladhor Saan → Davos Seaworth | asos-davos-02 |
| 2655 | 1 | owed service by | `(LLM tail)` | Salladhor Saan → Stannis Baratheon | asos-davos-02 |
| 2656 | 1 | isolation with | `(LLM tail)` | Stannis Baratheon → Melisandre | asos-davos-02 |
| 2657 | 1 | political partnership with | `(LLM tail)` | Queen Selyse → Lord Alester Florent | asos-davos-02 |
| 2658 | 1 | believes Mother saved him | `(LLM tail)` | Davos Seaworth → The Mother (deity) | asos-davos-02 |
| 2659 | 1 | playful with | `(LLM tail)` | Shireen Baratheon → Patchface | asos-davos-02 |
| 2660 | 1 | plays with/protective of | `(LLM tail)` | Edric Storm → Shireen Baratheon | asos-davos-02 |
| 2661 | 1 | Loyal subject/prisoner of | `(LLM tail)` | Davos → Stannis | asos-davos-03 |
| 2662 | 1 | Opposes/fears | `OPPOSES` | Davos → Melisandre | asos-davos-03 |
| 2663 | 1 | Suspects then exonerates | `(LLM tail)` | Davos → Salladhor Saan | asos-davos-03 |
| 2664 | 1 | Proselytizes/attempts to recruit | `(LLM tail)` | Melisandre → Davos | asos-davos-03 |
| 2665 | 1 | Former Hand to | `(LLM tail)` | Lord Alester Florent → Stannis | asos-davos-03 |
| 2666 | 1 | Mild kinship/sympathy toward | `(LLM tail)` | Davos → Lord Alester | asos-davos-03 |
| 2667 | 1 | Betrays (in Stannis's view) | `BETRAYS` | Lord Alester → Stannis | asos-davos-03 |
| 2668 | 1 | Loyal sworn man / new Hand | `(LLM tail)` | Davos → Stannis | asos-davos-04 |
| 2669 | 1 | Trusted counselor | `ADVISES` | Davos → Stannis | asos-davos-04 |
| 2670 | 1 | Trusts above all remaining lords | `TRUSTS` | Stannis → Davos | asos-davos-04 |
| 2671 | 1 | Coerces and threatens | `(LLM tail)` | Ser Axell → Davos | asos-davos-04 |
| 2672 | 1 | Bitter rival / antagonist | `RESENTS` | Ser Axell → Davos | asos-davos-04 |
| 2673 | 1 | Brother (calls him traitor) | `SIBLING_OF` | Ser Axell → Lord Alester Florent | asos-davos-04 |
| 2674 | 1 | Cellmate | `(LLM tail)` | Lord Alester → Davos | asos-davos-04 |
| 2675 | 1 | Condemned as traitor | `(LLM tail)` | Lord Alester → Stannis | asos-davos-04 |
| 2676 | 1 | Complex grief / resentment toward | `MOURNS` | Stannis → Robert Baratheon | asos-davos-04 |
| 2677 | 1 | Guilt and conflict toward | `(LLM tail)` | Stannis → Renly Baratheon | asos-davos-04 |
| 2678 | 1 | Claims no intent to harm | `(LLM tail)` | Stannis → Edric Storm | asos-davos-04 |
| 2679 | 1 | Relies on / defends | `(LLM tail)` | Stannis → Melisandre | asos-davos-04 |
| 2680 | 1 | Saved Davos's life | `(LLM tail)` | Melisandre → Davos | asos-davos-04 |
| 2681 | 1 | Murderous intent toward | `(LLM tail)` | Davos → Melisandre | asos-davos-04 |
| 2682 | 1 | Blames for sons' deaths | `OPPOSES` | Davos → Melisandre | asos-davos-04 |
| 2683 | 1 | Wants to sacrifice | `(LLM tail)` | Melisandre → Edric Storm | asos-davos-04 |
| 2684 | 1 | Refuses to sacrifice | `(LLM tail)` | Stannis → Edric Storm | asos-davos-04 |
| 2685 | 1 | Self-comparison (unfavorable) | `(LLM tail)` | Stannis → Robert | asos-davos-04 |
| 2686 | 1 | Values duty over desire | `(LLM tail)` | Stannis → The Iron Throne | asos-davos-04 |
| 2687 | 1 | Serves as Hand and counselor to | `SERVES` | Davos → Stannis | asos-davos-05 |
| 2688 | 1 | Husband of (strained) | `(LLM tail)` | Stannis → Selyse | asos-davos-05 |
| 2689 | 1 | Complex dynamic with | `(LLM tail)` | Stannis → Melisandre | asos-davos-05 |
| 2690 | 1 | Allies with / influences | `ALLIES_WITH` | Melisandre → Selyse | asos-davos-05 |
| 2691 | 1 | Follows / echoes | `(LLM tail)` | Ser Axell → Melisandre and Selyse | asos-davos-05 |
| 2692 | 1 | Resentful of (memory) | `RESENTS` | Stannis → Robert Baratheon | asos-davos-05 |
| 2693 | 1 | Allied with (secret) | `ALLIES_WITH` | Davos → Ser Gerald Gower, Ser Andrew Estermont, the Bastard of Nightsong | asos-davos-05 |
| 2694 | 1 | Friend and ally of | `ALLIES_WITH` | Salladhor Saan → Davos | asos-davos-05 |
| 2695 | 1 | Plays with / befriends | `(LLM tail)` | Shireen → Edric Storm | asos-davos-05 |
| 2696 | 1 | Asks after | `(LLM tail)` | Edric Storm → Stannis | asos-davos-05 |
| 2697 | 1 | Confided in | `(LLM tail)` | Stannis → Maester Cressen (formerly) | asos-davos-05 |
| 2698 | 1 | Killed by / ran afoul of | `KILLS` | Maester Cressen → Melisandre | asos-davos-05 |
| 2699 | 1 | Formerly served under | `SERVES` | Davos → Roro Uhoris (the Blind Bastard) | asos-davos-05 |
| 2700 | 1 | Serves as Hand / loyal to but defies in this instance | `SERVES` | Davos → Stannis | asos-davos-06 |
| 2701 | 1 | Opposes / fears the influence of | `OPPOSES` | Davos → Melisandre | asos-davos-06 |
| 2702 | 1 | Prays for the safety of | `(LLM tail)` | Davos → Devan Seaworth | asos-davos-06 |
| 2703 | 1 | Wishes to return to | `(LLM tail)` | Davos → Marya Seaworth | asos-davos-06 |
| 2704 | 1 | Grateful to / initially uncertain of | `(LLM tail)` | Davos → Maester Pylos | asos-davos-06 |
| 2705 | 1 | Advises / demands sacrifice from | `ADVISES` | Melisandre → Stannis | asos-davos-06 |
| 2706 | 1 | Torn between duty and morality regarding | `(LLM tail)` | Stannis → Edric Storm | asos-davos-06 |
| 2707 | 1 | Angry at but still listens to | `(LLM tail)` | Stannis → Davos | asos-davos-06 |
| 2708 | 1 | Fervent worshiper of | `(LLM tail)` | Queen Selyse → R'hllor | asos-davos-06 |
| 2709 | 1 | Fond of / concerned about | `LOVES` | Edric Storm → Shireen | asos-davos-06 |
| 2710 | 1 | Son of (acknowledged bastard) | `PARENT_OF` | Edric Storm → Robert Baratheon | asos-davos-06 |
| 2711 | 1 | Respected by / cooperates with | `RESPECTS` | Davos → Bastard of Nightsong, Ser Gerald, Ser Andrew, Lewys, Omer | asos-davos-06 |
| 2712 | 1 | Formerly sworn to | `(LLM tail)` | Ser Triston of Tally Hill → Lord Guncer Sunglass | asos-davos-06 |
| 2713 | 1 | Considers himself rightful king over | `(LLM tail)` | Stannis → Tommen Baratheon | asos-davos-06 |
| 2714 | 1 | son of (despised by) | `PARENT_OF` | Merrett Frey → Lord Walder Frey | asos-epilogue |
| 2715 | 1 | brother of (full) | `SIBLING_OF` | Merrett Frey → Ser Hosteen Frey | asos-epilogue |
| 2716 | 1 | co-plotter with | `(LLM tail)` | Lame Lothar Frey → Roose Bolton | asos-epilogue |
| 2717 | 1 | ordered | `(LLM tail)` | Lord Walder Frey → Red Wedding slaughter | asos-epilogue |
| 2718 | 1 | leader/judge of | `(LLM tail)` | Lady Stoneheart → Brotherhood Without Banners | asos-epilogue |
| 2719 | 1 | fellow squire of (past) | `(LLM tail)` | Merrett Frey → Jaime Lannister | asos-epilogue |
| 2720 | 1 | captured by (past) | `(LLM tail)` | Merrett Frey → Wenda the White Fawn | asos-epilogue |
| 2721 | 1 | died campaigning with | `(LLM tail)` | Ser Stevron Frey → Robb Stark | asos-epilogue |
| 2722 | 1 | uncle (great half-uncle) of | `UNCLE_OF` | Merrett Frey → Petyr Pimple | asos-epilogue |
| 2723 | 1 | prisoner/captive of | `(LLM tail)` | Jaime Lannister → Brienne of Tarth | asos-jaime-01 |
| 2724 | 1 | serves/is sworn to | `SERVES` | Brienne of Tarth → Catelyn Stark | asos-jaime-01 |
| 2725 | 1 | fawning/sycophantic toward | `(LLM tail)` | Ser Cleos Frey → Jaime Lannister | asos-jaime-01 |
| 2726 | 1 | sexual desire/obsessive attachment toward | `(LLM tail)` | Jaime Lannister → Cersei Lannister | asos-jaime-01 |
| 2727 | 1 | affection toward | `LOVES` | Jaime Lannister → Tyrion Lannister | asos-jaime-01 |
| 2728 | 1 | freed/released | `(LLM tail)` | Catelyn Stark → Jaime Lannister | asos-jaime-01 |
| 2729 | 1 | married to / terrorized by (in-law) | `IN_LAW_OF` | Ser Emmon Frey → Genna Lannister / Lord Tywin | asos-jaime-01 |
| 2730 | 1 | pursues on orders | `(LLM tail)` | Ser Robin Ryger → Jaime Lannister | asos-jaime-01 |
| 2731 | 1 | allegiance to | `(LLM tail)` | Lord Walder Frey → Riverrun (Tully) | asos-jaime-01 |
| 2732 | 1 | took Harrenhal from | `(LLM tail)` | Roose Bolton → Ser Amory Lorch | asos-jaime-01 |
| 2733 | 1 | burned castle of | `(LLM tail)` | Lord Tywin Lannister → Lord Jonos Bracken | asos-jaime-01 |
| 2734 | 1 | prisoner of / escorted by | `PRISONER_OF` | Jaime → Brienne | asos-jaime-02 |
| 2735 | 1 | loathing toward | `HATES` | Brienne → Jaime | asos-jaime-02 |
| 2736 | 1 | devotion to / mourning | `MOURNS` | Brienne → Renly Baratheon | asos-jaime-02 |
| 2737 | 1 | incestuous love for | `LOVES` | Jaime → Cersei Lannister | asos-jaime-02 |
| 2738 | 1 | affection/kinship toward | `LOVES` | Jaime → Tyrion Lannister | asos-jaime-02 |
| 2739 | 1 | ward of / taken in by | `WARD_OF` | The boy → The cook and his wife | asos-jaime-02 |
| 2740 | 1 | deference toward | `(LLM tail)` | Ser Cleos → Brienne | asos-jaime-02 |
| 2741 | 1 | squired for | `(LLM tail)` | Jaime → Ser Sumner Crakehall | asos-jaime-02 |
| 2742 | 1 | Antagonistic captor-captive evolving toward grudging respect | `OPPOSES` | Jaime → Brienne | asos-jaime-03 |
| 2743 | 1 | Cousin, indifferent | `COUSIN_OF` | Jaime → Cleos Frey | asos-jaime-03 |
| 2744 | 1 | Incestuous lover, obsessive bond | `LOVER_OF` | Jaime → Cersei | asos-jaime-03 |
| 2745 | 1 | Son, barely remembers her | `(LLM tail)` | Jaime → Lady Joanna | asos-jaime-03 |
| 2746 | 1 | Son, complicated loyalty | `(LLM tail)` | Jaime → Tywin Lannister | asos-jaime-03 |
| 2747 | 1 | Contempt toward, attempting to manipulate | `(LLM tail)` | Jaime → Urswyck | asos-jaime-03 |
| 2748 | 1 | Contempt and hostility toward | `HATES` | Jaime → Vargo Hoat | asos-jaime-03 |
| 2749 | 1 | Captor/protector, dutiful | `CAPTURES` | Brienne → Jaime | asos-jaime-03 |
| 2750 | 1 | Loyal servant | `(LLM tail)` | Brienne → Catelyn Stark | asos-jaime-03 |
| 2751 | 1 | Former servants, now betrayers | `(LLM tail)` | Brave Companions → House Lannister | asos-jaime-03 |
| 2752 | 1 | Currently serve | `(LLM tail)` | Brave Companions → Roose Bolton / King in the North | asos-jaime-03 |
| 2753 | 1 | Claims lordship granted by Lannisters | `(LLM tail)` | Vargo Hoat → Harrenhal | asos-jaime-03 |
| 2754 | 1 | Subordinate commander | `COMMANDS` | Urswyck → Vargo Hoat | asos-jaime-03 |
| 2755 | 1 | Cruel enforcer | `(LLM tail)` | Rorge → Brave Companions | asos-jaime-03 |
| 2756 | 1 | Resentful memory of | `RESENTS` | Jaime → Aerys II Targaryen | asos-jaime-03 |
| 2757 | 1 | motivates | `(LLM tail)` | Brienne → Jaime | asos-jaime-04 |
| 2758 | 1 | bound prisoner of | `(LLM tail)` | Jaime → Vargo Hoat | asos-jaime-04 |
| 2759 | 1 | reports death of | `(LLM tail)` | Jaime → Ser Cleos Frey | asos-jaime-04 |
| 2760 | 1 | implies knowledge of | `(LLM tail)` | Bolton → Jaime-Cersei incest | asos-jaime-04 |
| 2761 | 1 | memory of witnessing | `(LLM tail)` | Jaime → Deaths of Rickard and Brandon Stark | asos-jaime-04 |
| 2762 | 1 | growing trust/respect toward | `RESPECTS` | Jaime → Brienne | asos-jaime-05 |
| 2763 | 1 | guilt/resentment toward | `(LLM tail)` | Jaime → Ned Stark | asos-jaime-05 |
| 2764 | 1 | wary respect for | `RESPECTS` | Jaime → Roose Bolton | asos-jaime-05 |
| 2765 | 1 | loyalty toward | `SERVES` | Brienne → Catelyn Stark | asos-jaime-05 |
| 2766 | 1 | shock/naivety about | `(LLM tail)` | Brienne → Robb Stark's choices | asos-jaime-05 |
| 2767 | 1 | serves (nominally) | `SERVES` | Roose Bolton → Robb Stark | asos-jaime-05 |
| 2768 | 1 | maimed | `(LLM tail)` | Vargo Hoat → Jaime | asos-jaime-05 |
| 2769 | 1 | healer to | `(LLM tail)` | Qyburn → Jaime | asos-jaime-05 |
| 2770 | 1 | rescued by/protects | `RESCUES` | Jaime → Brienne | asos-jaime-06 |
| 2771 | 1 | threatens/manipulates | `OPPOSES` | Jaime → Steelshanks Walton | asos-jaime-06 |
| 2772 | 1 | desires/is faithful to | `(LLM tail)` | Jaime → Cersei | asos-jaime-06 |
| 2773 | 1 | is escorted by | `(LLM tail)` | Jaime → Steelshanks Walton | asos-jaime-06 |
| 2774 | 1 | is tended by | `(LLM tail)` | Jaime → Qyburn | asos-jaime-06 |
| 2775 | 1 | offers ransom for | `(LLM tail)` | Lord Selwyn → Brienne | asos-jaime-06 |
| 2776 | 1 | taunts/threatens | `(LLM tail)` | Jaime → Brave Companions | asos-jaime-06 |
| 2777 | 1 | hopes for patronage from | `(LLM tail)` | Qyburn → Tywin Lannister | asos-jaime-06 |
| 2778 | 1 | bitter toward (memory) | `RESENTS` | Jaime → Aerys II | asos-jaime-06 |
| 2779 | 1 | accuse | `(LLM tail)` | Dead Kingsguard (dream) → Jaime | asos-jaime-06 |
| 2780 | 1 | stands with | `(LLM tail)` | Brienne (dream) → Jaime | asos-jaime-06 |
| 2781 | 1 | Father of (secret) | `PARENT_OF` | Jaime → Joffrey | asos-jaime-07 |
| 2782 | 1 | Brother, protective | `SIBLING_OF` | Jaime → Tyrion | asos-jaime-07 |
| 2783 | 1 | Son, defiant | `(LLM tail)` | Jaime → Tywin | asos-jaime-07 |
| 2784 | 1 | Reluctant protector of | `(LLM tail)` | Jaime → Brienne | asos-jaime-07 |
| 2785 | 1 | Mourns/avenges | `MOURNS` | Loras → Renly | asos-jaime-07 |
| 2786 | 1 | Loyal to (deceased) | `SERVES` | Brienne → Renly | asos-jaime-07 |
| 2787 | 1 | Broken by news of | `(LLM tail)` | Brienne → Robb Stark / Catelyn Stark | asos-jaime-07 |
| 2788 | 1 | Annoyed by | `(LLM tail)` | Jaime → Qyburn | asos-jaime-07 |
| 2789 | 1 | Father, controlling | `(LLM tail)` | Tywin → Jaime | asos-jaime-07 |
| 2790 | 1 | Manipulative toward | `(LLM tail)` | Tywin → Cersei | asos-jaime-07 |
| 2791 | 1 | Discusses investigation of | `(LLM tail)` | Tywin → Tyrion | asos-jaime-07 |
| 2792 | 1 | Unfamiliar with | `(LLM tail)` | Osmund Kettleblack → Jaime | asos-jaime-07 |
| 2793 | 1 | Destroys | `(LLM tail)` | Gregor Clegane → Vargo Hoat | asos-jaime-07 |
| 2794 | 1 | Grim satisfaction toward | `(LLM tail)` | Jaime → Vargo Hoat | asos-jaime-07 |
| 2795 | 1 | feels unworthy compared to | `(LLM tail)` | Jaime → Barristan Selmy | asos-jaime-08 |
| 2796 | 1 | idolizes (past) | `(LLM tail)` | Jaime → Ser Arthur Dayne | asos-jaime-08 |
| 2797 | 1 | sees himself in | `(LLM tail)` | Jaime → Ser Loras | asos-jaime-08 |
| 2798 | 1 | secret paternal connection to | `(LLM tail)` | Jaime → Joffrey | asos-jaime-08 |
| 2799 | 1 | respects Brienne's (grudging) | `RESPECTS` | Ser Loras → Brienne | asos-jaime-08 |
| 2800 | 1 | torn between | `(LLM tail)` | Ser Balon → Jaime / his family | asos-jaime-08 |
| 2801 | 1 | thought absurd | `(LLM tail)` | Renly (as reported) → Brienne | asos-jaime-08 |
| 2802 | 1 | considering consulting | `(LLM tail)` | Jaime → Varys | asos-jaime-08 |
| 2803 | 1 | rejects/pushes away | `(LLM tail)` | Jaime → Cersei | asos-jaime-09 |
| 2804 | 1 | respects/trusts | `RESPECTS` | Jaime → Brienne | asos-jaime-09 |
| 2805 | 1 | manipulates/pleads with | `MANIPULATES` | Cersei → Jaime | asos-jaime-09 |
| 2806 | 1 | fears loss of | `FEARS` | Cersei → Tommen | asos-jaime-09 |
| 2807 | 1 | plans to remarry | `(LLM tail)` | Lord Tywin → Cersei | asos-jaime-09 |
| 2808 | 1 | loyalty/devotion to | `(LLM tail)` | Brienne → Jaime | asos-jaime-09 |
| 2809 | 1 | guilt/unease about | `(LLM tail)` | Jaime → Bran Stark | asos-jaime-09 |
| 2810 | 1 | Bonded to / warg of | `BONDED_TO` | Jon Snow → Ghost | asos-jon-01 |
| 2811 | 1 | Pretending to serve / secretly loyal to | `(LLM tail)` | Jon Snow → Night's Watch | asos-jon-01 |
| 2812 | 1 | Infiltrating | `(LLM tail)` | Jon Snow → Mance Rayder's wildlings | asos-jon-01 |
| 2813 | 1 | Guards/escorts (hostile) | `GUARDS` | Rattleshirt → Jon Snow | asos-jon-01 |
| 2814 | 1 | King / leader of | `(LLM tail)` | Mance Rayder → Free folk (all wildlings) | asos-jon-01 |
| 2815 | 1 | Husband / lover of | `LOVER_OF` | Mance Rayder → Dalla | asos-jon-01 |
| 2816 | 1 | Allied leader under | `ALLIES_WITH` | Styr (Magnar of Thenn) → Mance Rayder | asos-jon-01 |
| 2817 | 1 | Former comrade / enemy of | `(LLM tail)` | Mance Rayder → Qhorin Halfhand | asos-jon-01 |
| 2818 | 1 | Outrider/subordinate of | `SERVES` | The Weeper → Mance Rayder | asos-jon-01 |
| 2819 | 1 | Subordinate of (loose) | `SERVES` | Rattleshirt → Mance Rayder | asos-jon-01 |
| 2820 | 1 | Formerly stationed at | `(LLM tail)` | Mance Rayder → Shadow Tower | asos-jon-01 |
| 2821 | 1 | Wanted measure of | `(LLM tail)` | Mance Rayder → Benjen Stark | asos-jon-01 |
| 2822 | 1 | Conflicted admiration | `RESPECTS` | Jon Snow → Mance Rayder | asos-jon-02 |
| 2823 | 1 | Growing affection / sexual tension | `LOVES` | Jon Snow → Ygritte | asos-jon-02 |
| 2824 | 1 | Growing fondness | `(LLM tail)` | Jon Snow → Tormund Giantsbane | asos-jon-02 |
| 2825 | 1 | Loyalty / duty | `(LLM tail)` | Jon Snow → House Stark | asos-jon-02 |
| 2826 | 1 | Protective bond | `(LLM tail)` | Jon Snow → Ghost | asos-jon-02 |
| 2827 | 1 | Protective / romantic pursuit | `(LLM tail)` | Ygritte → Jon Snow | asos-jon-02 |
| 2828 | 1 | Left Rattleshirt's band for Tormund's | `(LLM tail)` | Ygritte → Tormund Giantsbane | asos-jon-02 |
| 2829 | 1 | Protective of Jon | `PROTECTS` | Tormund → Jon Snow | asos-jon-02 |
| 2830 | 1 | Antagonistic/mocking | `OPPOSES` | Tormund → Rattleshirt | asos-jon-02 |
| 2831 | 1 | Hostile / distrustful | `(LLM tail)` | Styr → Jon Snow | asos-jon-02 |
| 2832 | 1 | Commander / suspicious | `COMMANDS` | Mance Rayder → Jon Snow | asos-jon-02 |
| 2833 | 1 | Hostile/wary | `(LLM tail)` | Ghost → Varamyr's animals | asos-jon-02 |
| 2834 | 1 | Obedience to orders | `(LLM tail)` | Jon Snow → Qhorin Halfhand | asos-jon-02 |
| 2835 | 1 | Bonded to / sends away reluctantly | `BONDED_TO` | Jon Snow → Ghost | asos-jon-03 |
| 2836 | 1 | Considers Jon her man / "stolen" her | `(LLM tail)` | Ygritte → Jon Snow | asos-jon-03 |
| 2837 | 1 | Feels kinship with, wonders if still his sister | `SIBLING_OF` | Jon Snow → Arya Stark | asos-jon-03 |
| 2838 | 1 | Identifies as bastard of, questions parallel | `(LLM tail)` | Jon Snow → Eddard Stark | asos-jon-03 |
| 2839 | 1 | Feels displaced by / parallel to | `(LLM tail)` | Jon Snow → Theon Greyjoy | asos-jon-03 |
| 2840 | 1 | Dutiful memory of | `(LLM tail)` | Jon Snow → Maester Luwin | asos-jon-03 |
| 2841 | 1 | Commands / dominates | `COMMANDS` | Styr → Jon Snow | asos-jon-03 |
| 2842 | 1 | Resents sharing authority with | `RESENTS` | Styr → Jarl | asos-jon-03 |
| 2843 | 1 | Distrusts / watches | `DISTRUSTS` | Jarl → Jon Snow | asos-jon-03 |
| 2844 | 1 | Connected to via Val | `(LLM tail)` | Jarl → Mance Rayder | asos-jon-03 |
| 2845 | 1 | Commands absolutely | `COMMANDS` | Styr → The Thenns | asos-jon-03 |
| 2846 | 1 | Respects, feels guilt toward | `RESPECTS` | Jon Snow → Qhorin Halfhand | asos-jon-03 |
| 2847 | 1 | From same village as | `(LLM tail)` | Ygritte → Longspear (Ryk) | asos-jon-03 |
| 2848 | 1 | Likes | `(LLM tail)` | Jon Snow → Longspear (Ryk) | asos-jon-03 |
| 2849 | 1 | Helpful to | `(LLM tail)` | Grigg the Goat → Jon Snow | asos-jon-03 |
| 2850 | 1 | Romantic attachment / divided loyalty toward | `(LLM tail)` | Jon Snow → Ygritte | asos-jon-04 |
| 2851 | 1 | Bonded to / hopes for communication with | `BONDED_TO` | Jon Snow → Ghost | asos-jon-04 |
| 2852 | 1 | Romantic attachment to / frustration with | `(LLM tail)` | Ygritte → Jon Snow | asos-jon-04 |
| 2853 | 1 | Commands overall force / disdains | `COMMANDS` | The Magnar (Styr) → Jarl | asos-jon-04 |
| 2854 | 1 | Serves / represents | `SERVES` | Jarl → Mance Rayder | asos-jon-04 |
| 2855 | 1 | Fear / awe toward | `FEARS` | The Thenns → The Wall | asos-jon-04 |
| 2856 | 1 | Anger / hatred toward | `(LLM tail)` | Ygritte → The Wall | asos-jon-04 |
| 2857 | 1 | Lover / deeply conflicted bond | `LOVER_OF` | Jon Snow → Ygritte | asos-jon-05 |
| 2858 | 1 | Subordinate under duress | `SERVES` | Jon Snow → Styr (the Magnar) | asos-jon-05 |
| 2859 | 1 | Loyal to (secretly) | `SERVES` | Jon Snow → Night's Watch | asos-jon-05 |
| 2860 | 1 | Mourns/remembers | `MOURNS` | Jon Snow → Lord Eddard Stark | asos-jon-05 |
| 2861 | 1 | Yearns for connection with | `(LLM tail)` | Jon Snow → Ghost | asos-jon-05 |
| 2862 | 1 | Growing attachment (unwanted) | `(LLM tail)` | Jon Snow → Wildling raiders (Del, Bodger, Quort, etc.) | asos-jon-05 |
| 2863 | 1 | Scout/guide for | `(LLM tail)` | Grigg the Goat → Styr | asos-jon-05 |
| 2864 | 1 | Weather-predictor for | `(LLM tail)` | Lenn → The raiding party | asos-jon-05 |
| 2865 | 1 | Remembers instructions from | `(LLM tail)` | Jon Snow → Qhorin Halfhand | asos-jon-05 |
| 2866 | 1 | conflicted former lover of | `LOVER_OF` | Jon Snow → Ygritte | asos-jon-06 |
| 2867 | 1 | follows orders of | `(LLM tail)` | Jon Snow → Qhorin Halfhand | asos-jon-06 |
| 2868 | 1 | trusts and respects | `TRUSTS` | Jon Snow → Donal Noye | asos-jon-06 |
| 2869 | 1 | bonded to / worried about | `BONDED_TO` | Jon Snow → Ghost | asos-jon-06 |
| 2870 | 1 | friendship with (worried about) | `COMPANION_OF` | Jon Snow → Samwell Tarly | asos-jon-06 |
| 2871 | 1 | parallels himself with | `(LLM tail)` | Jon Snow → Eddard Stark | asos-jon-06 |
| 2872 | 1 | healer/authority over | `(LLM tail)` | Maester Aemon → Jon Snow | asos-jon-06 |
| 2873 | 1 | enemy of / torturer of | `OPPOSES` | Bolton's son → Theon Greyjoy | asos-jon-06 |
| 2874 | 1 | mutual enmity with | `(LLM tail)` | Cotter Pyke → Ser Denys Mallister | asos-jon-06 |
| 2875 | 1 | acting Lord Commander over | `COMMANDS` | Bowen Marsh → Castle Black | asos-jon-06 |
| 2876 | 1 | de facto commands | `COMMANDS` | Noye → Castle Black garrison | asos-jon-06 |
| 2877 | 1 | Former lover / deep attachment | `LOVER_OF` | Jon Snow → Ygritte | asos-jon-07 |
| 2878 | 1 | Antagonism / enmity | `(LLM tail)` | Jon Snow → Rast | asos-jon-07 |
| 2879 | 1 | Commanding / mentoring | `TUTORS` | Jon Snow → Satin | asos-jon-07 |
| 2880 | 1 | Respect for authority | `RESPECTS` | Jon Snow → Donal Noye | asos-jon-07 |
| 2881 | 1 | Respect / memory | `RESPECTS` | Jon Snow → Eddard Stark | asos-jon-07 |
| 2882 | 1 | Memory / shared youth | `(LLM tail)` | Jon Snow → Robb Stark | asos-jon-07 |
| 2883 | 1 | Hatred | `HATES` | Jon Snow → Styr | asos-jon-07 |
| 2884 | 1 | Distrusted by | `DISTRUSTS` | Jon Snow → Some Night's Watch brothers | asos-jon-07 |
| 2885 | 1 | Protected by stigma of bastardy | `PROTECTS` | Jon Snow → Everyone | asos-jon-07 |
| 2886 | 1 | Fights alongside / trusts | `(LLM tail)` | Satin → Jon Snow | asos-jon-07 |
| 2887 | 1 | Trusts / respects | `TRUSTS` | Owen the Oaf → Jon Snow | asos-jon-07 |
| 2888 | 1 | Strategic partnership | `(LLM tail)` | Donal Noye → Maester Aemon | asos-jon-07 |
| 2889 | 1 | Dying love | `LOVES` | Ygritte → Jon Snow | asos-jon-07 |
| 2890 | 1 | Trusts/delegates to | `TRUSTS` | Donal Noye → Jon Snow | asos-jon-08 |
| 2891 | 1 | Mentors/supports | `TUTORS` | Maester Aemon → Jon Snow | asos-jon-08 |
| 2892 | 1 | Kills/killed by | `KILLS` | Donal Noye → Mag the Mighty | asos-jon-08 |
| 2893 | 1 | Grateful/affectionate to | `LOVES` | Zei → Owen the Oaf | asos-jon-08 |
| 2894 | 1 | Recognizes/respects | `RESPECTS` | Jon Snow → Mag the Mighty | asos-jon-08 |
| 2895 | 1 | Irritates | `(LLM tail)` | Septon Cellador → Jon Snow / Donal Noye | asos-jon-08 |
| 2896 | 1 | Cares for / feels responsible for | `(LLM tail)` | Jon Snow → Wall defenders | asos-jon-09 |
| 2897 | 1 | Boosts morale of | `(LLM tail)` | Pyp → Defenders | asos-jon-09 |
| 2898 | 1 | Loyal to / follows | `SERVES` | Grenn → Jon Snow | asos-jon-09 |
| 2899 | 1 | Naive hopefulness | `(LLM tail)` | Owen → (general) | asos-jon-09 |
| 2900 | 1 | Hostile toward / accuses | `OPPOSES` | Janos Slynt → Jon Snow | asos-jon-09 |
| 2901 | 1 | Hostile toward / mocks | `OPPOSES` | Ser Alliser Thorne → Jon Snow | asos-jon-09 |
| 2902 | 1 | Defends / respects | `PROTECTS` | Maester Aemon → Jon Snow | asos-jon-09 |
| 2903 | 1 | Hostile toward / lies about | `OPPOSES` | Rattleshirt → Jon Snow | asos-jon-09 |
| 2904 | 1 | Previously trusted | `(LLM tail)` | Donal Noye → Jon Snow | asos-jon-09 |
| 2905 | 1 | Defends honor of | `PROTECTS` | Jon Snow → Eddard Stark | asos-jon-09 |
| 2906 | 1 | Commands/manipulates | `COMMANDS` | Janos Slynt → Jon Snow | asos-jon-10 |
| 2907 | 1 | Advises/manipulates | `ADVISES` | Alliser Thorne → Janos Slynt | asos-jon-10 |
| 2908 | 1 | Shame before | `(LLM tail)` | Jon Snow → Eddard Stark | asos-jon-10 |
| 2909 | 1 | Stole (married by capture) | `(LLM tail)` | Longspear Ryk → Munda | asos-jon-10 |
| 2910 | 1 | Contains/absorbed | `(LLM tail)` | Varamyr → Orell | asos-jon-10 |
| 2911 | 1 | Attacks/defeats | `ATTACKS` | Stannis Baratheon → Wildling host | asos-jon-10 |
| 2912 | 1 | Trains / mentors | `TEACHES` | Jon Snow → Satin | asos-jon-11 |
| 2913 | 1 | Summoned by / obeys | `SERVES` | Jon Snow → Stannis Baratheon | asos-jon-11 |
| 2914 | 1 | Serves as advisor / close counselor to | `SERVES` | Melisandre → Stannis Baratheon | asos-jon-11 |
| 2915 | 1 | Offers legitimization and lordship to | `(LLM tail)` | Stannis Baratheon → Jon Snow | asos-jon-11 |
| 2916 | 1 | Criticizes / distrusts | `(LLM tail)` | Stannis Baratheon → Janos Slynt | asos-jon-11 |
| 2917 | 1 | Valued / mourns | `MOURNS` | Stannis Baratheon → Donal Noye | asos-jon-11 |
| 2918 | 1 | Trusts and credits | `TRUSTS` | Stannis Baratheon → Davos Seaworth | asos-jon-11 |
| 2919 | 1 | Intends to execute | `(LLM tail)` | Stannis Baratheon → Mance Rayder | asos-jon-11 |
| 2920 | 1 | Exerts spiritual pressure on | `(LLM tail)` | Melisandre → Jon Snow | asos-jon-11 |
| 2921 | 1 | Conflicted with memory of | `(LLM tail)` | Stannis Baratheon → Robert Baratheon | asos-jon-11 |
| 2922 | 1 | trains regularly with | `TEACHES` | Jon Snow → Iron Emmett | asos-jon-12 |
| 2923 | 1 | bonds with (warg) | `WARGS_INTO` | Jon Snow → Ghost | asos-jon-12 |
| 2924 | 1 | childhood brothers with | `(LLM tail)` | Jon Snow → Robb Stark | asos-jon-12 |
| 2925 | 1 | resented by (memory) | `(LLM tail)` | Jon Snow → Catelyn Stark | asos-jon-12 |
| 2926 | 1 | nominated by | `(LLM tail)` | Jon Snow → Dolorous Edd | asos-jon-12 |
| 2927 | 1 | respected by | `RESPECTS` | Jon Snow → Ser Denys Mallister | asos-jon-12 |
| 2928 | 1 | warned/respected by | `RESPECTS` | Jon Snow → Cotter Pyke | asos-jon-12 |
| 2929 | 1 | unrealized connection to | `(LLM tail)` | Jon Snow → Val | asos-jon-12 |
| 2930 | 1 | offers to serve | `(LLM tail)` | Bowen Marsh → Jon Snow | asos-jon-12 |
| 2931 | 1 | pivots support to | `(LLM tail)` | Othell Yarwyck → Jon Snow | asos-jon-12 |
| 2932 | 1 | chooses | `(LLM tail)` | Mormont's raven → Jon Snow | asos-jon-12 |
| 2933 | 1 | backed by | `(LLM tail)` | Janos Slynt → Tywin Lannister | asos-jon-12 |
| 2934 | 1 | asked sacrifice of | `(LLM tail)` | Sam Tarly → Ser Denys Mallister | asos-jon-12 |
| 2935 | 1 | Bitter enemy / blames | `RESENTS` | Chett → Jon Snow | asos-prologue |
| 2936 | 1 | Intends to murder | `(LLM tail)` | Chett → Samwell Tarly | asos-prologue |
| 2937 | 1 | Leader of mutiny | `(LLM tail)` | Chett → Small Paul, Lark, Dirk, Softfoot, Sweet Donnel Hill, Clubfoot Karl, Maslyn, Sawwood, Lark's cousins | asos-prologue |
| 2938 | 1 | Former steward to | `(LLM tail)` | Chett → Maester Aemon | asos-prologue |
| 2939 | 1 | Subordinate conspirator to | `SERVES` | Small Paul → Chett | asos-prologue |
| 2940 | 1 | Conspirator with, friction | `CONSPIRES_WITH` | Lark the Sisterman → Chett | asos-prologue |
| 2941 | 1 | Persuades / allies with | `(LLM tail)` | Thoren Smallwood → Ser Mallador Locke | asos-prologue |
| 2942 | 1 | Disagrees with | `(LLM tail)` | Thoren Smallwood → Ser Ottyn Wythers | asos-prologue |
| 2943 | 1 | Bonded to / accompanied by | `BONDED_TO` | Mormont → Mormont's raven | asos-prologue |
| 2944 | 1 | Judged | `(LLM tail)` | Walder Rivers → Chett | asos-prologue |
| 2945 | 1 | Escorted to Wall | `(LLM tail)` | Yoren → Chett | asos-prologue |
| 2946 | 1 | Covets lifestyle of | `(LLM tail)` | Chett → Craster | asos-prologue |
| 2947 | 1 | Carried by/gratitude | `(LLM tail)` | Sam → Small Paul | asos-samwell-01 |
| 2948 | 1 | Self-loathing/obedience | `(LLM tail)` | Sam → Lord Randyll Tarly | asos-samwell-01 |
| 2949 | 1 | Subordinate/respect | `RESPECTS` | Sam → Jeor Mormont | asos-samwell-01 |
| 2950 | 1 | Promised raven by | `(LLM tail)` | Small Paul → Chett | asos-samwell-01 |
| 2951 | 1 | Protective of raven from | `PROTECTS` | Small Paul → Lark | asos-samwell-01 |
| 2952 | 1 | Tends ravens for | `(LLM tail)` | Sam → Maester Aemon | asos-samwell-01 |
| 2953 | 1 | Recalls/hears voices of | `(LLM tail)` | Sam → Alliser Thorne, Rast, Dickon, Lord Randyll | asos-samwell-01 |
| 2954 | 1 | Teased | `(LLM tail)` | Pyp → Grenn | asos-samwell-01 |
| 2955 | 1 | serves/attends | `SERVES` | Sam → Bannen | asos-samwell-02 |
| 2956 | 1 | friendship/comfort | `COMPANION_OF` | Sam → Grenn | asos-samwell-02 |
| 2957 | 1 | feels obligation toward | `(LLM tail)` | Sam → Gilly | asos-samwell-02 |
| 2958 | 1 | respects/trusts (dying) | `RESPECTS` | Mormont → Sam | asos-samwell-02 |
| 2959 | 1 | paternal toward | `(LLM tail)` | Mormont → Jorah (estranged) | asos-samwell-02 |
| 2960 | 1 | depends on/trusts | `(LLM tail)` | Gilly → Sam | asos-samwell-02 |
| 2961 | 1 | protector/companion of | `COMPANION_OF` | Sam → Gilly | asos-samwell-03 |
| 2962 | 1 | trusts/depends on | `TRUSTS` | Gilly → Sam | asos-samwell-03 |
| 2963 | 1 | fears/seeks approval from | `FEARS` | Sam → Lord Randyll | asos-samwell-03 |
| 2964 | 1 | rejected/demeaned | `(LLM tail)` | Lord Randyll → Sam | asos-samwell-03 |
| 2965 | 1 | mourns/remembers fondly | `MOURNS` | Sam → His mother | asos-samwell-03 |
| 2966 | 1 | former wife of | `(LLM tail)` | Gilly → Craster | asos-samwell-03 |
| 2967 | 1 | offers to be wife of | `(LLM tail)` | Gilly → Sam | asos-samwell-03 |
| 2968 | 1 | attack/oppose | `(LLM tail)` | Ravens (flock) → Wights | asos-samwell-03 |
| 2969 | 1 | threaten/surround | `(LLM tail)` | Wights → Gilly | asos-samwell-03 |
| 2970 | 1 | Romantic attachment | `(LLM tail)` | Samwell → Gilly | asos-samwell-04 |
| 2971 | 1 | Sad bond/protectiveness | `(LLM tail)` | Jon Snow → Val and the babe | asos-samwell-04 |
| 2972 | 1 | Devotion/loyalty | `(LLM tail)` | Val → Mance Rayder | asos-samwell-04 |
| 2973 | 1 | Nursing/care | `(LLM tail)` | Gilly → Mance Rayder's son | asos-samwell-04 |
| 2974 | 1 | Sworn brotherhood/close friendship | `COMPANION_OF` | Sam → Jon Snow | asos-samwell-04 |
| 2975 | 1 | Mentorship/honesty | `TUTORS` | Jon Snow → Sam | asos-samwell-04 |
| 2976 | 1 | Sworn brotherhood/emotional reunion | `(LLM tail)` | Sam → Dywen, Giant, Dolorous Edd | asos-samwell-04 |
| 2977 | 1 | Political alliance/endorsement | `ALLIES_WITH` | Bowen Marsh → Janos Slynt | asos-samwell-04 |
| 2978 | 1 | Political scheming | `(LLM tail)` | Ser Alliser Thorne → Othell Yarwyck | asos-samwell-04 |
| 2979 | 1 | Enmity/accusation | `(LLM tail)` | Ser Alliser Thorne → Jon Snow | asos-samwell-04 |
| 2980 | 1 | Enmity (received) | `(LLM tail)` | Jon Snow → Ser Alliser Thorne | asos-samwell-04 |
| 2981 | 1 | Suspicion/removal from duty | `(LLM tail)` | Bowen Marsh → Jon Snow | asos-samwell-04 |
| 2982 | 1 | Suppressed honesty / oath conflict | `(LLM tail)` | Sam → Jon Snow | asos-samwell-04 |
| 2983 | 1 | Oath of secrecy | `(LLM tail)` | Sam → Bran Stark, Jojen Reed, Coldhands | asos-samwell-04 |
| 2984 | 1 | Rescuer/debt-holder | `(LLM tail)` | Coldhands → Sam | asos-samwell-04 |
| 2985 | 1 | Political rivalry | `(LLM tail)` | Ser Denys Mallister → Cotter Pyke | asos-samwell-04 |
| 2986 | 1 | Complex filial resentment | `(LLM tail)` | Sam → Lord Randyll Tarly | asos-samwell-04 |
| 2987 | 1 | Complicated self-identity | `(LLM tail)` | Jon Snow → Ghost | asos-samwell-04 |
| 2988 | 1 | Haunted connection | `(LLM tail)` | Jon Snow → Robb Stark, Eddard Stark | asos-samwell-04 |
| 2989 | 1 | Awe/gratitude | `(LLM tail)` | Sam → Stannis Baratheon | asos-samwell-04 |
| 2990 | 1 | Anger/contempt | `(LLM tail)` | Sam → Joffrey, Tommen | asos-samwell-04 |
| 2991 | 1 | Protective mockery/friendship | `COMPANION_OF` | Pyp → Grenn | asos-samwell-04 |
| 2992 | 1 | Trust/admiration | `RESPECTS` | Grenn → Sam | asos-samwell-04 |
| 2993 | 1 | Service | `(LLM tail)` | Sam → Maester Aemon | asos-samwell-04 |
| 2994 | 1 | Mentors/manipulates | `TUTORS` | Maester Aemon → Sam | asos-samwell-05 |
| 2995 | 1 | Fawns on | `(LLM tail)` | Janos Slynt → Stannis | asos-samwell-05 |
| 2996 | 1 | Advises/promotes | `ADVISES` | Melisandre → Stannis | asos-samwell-05 |
| 2997 | 1 | Aware of identity | `(LLM tail)` | Stannis → Maester Aemon | asos-samwell-05 |
| 2998 | 1 | Respects militarily | `RESPECTS` | Stannis → Randyll Tarly | asos-samwell-05 |
| 2999 | 1 | Campaigns for | `(LLM tail)` | Sam → Jon Snow | asos-samwell-05 |
| 3000 | 1 | Trusted by | `(LLM tail)` | Jon Snow → Mormont, Noye, Halfhand | asos-samwell-05 |
| 3001 | 1 | Polite but detached toward | `(LLM tail)` | Ser Loras → Sansa | asos-sansa-01 |
| 3002 | 1 | Complex attachment to | `(LLM tail)` | Sansa → Sandor Clegane | asos-sansa-01 |
| 3003 | 1 | Warmly welcoming toward | `(LLM tail)` | Margaery → Sansa | asos-sansa-01 |
| 3004 | 1 | Interrogates/manipulates | `(LLM tail)` | Lady Olenna → Sansa | asos-sansa-01 |
| 3005 | 1 | Loved but exasperated by (late husband) | `LOVES` | Lady Olenna → Luthor Tyrell | asos-sansa-01 |
| 3006 | 1 | Tries to manage | `(LLM tail)` | Lady Alerie → Lady Olenna | asos-sansa-01 |
| 3007 | 1 | Sisterly with | `(LLM tail)` | Margaery → Ser Loras | asos-sansa-01 |
| 3008 | 1 | Grief/anger about | `MOURNS` | Ser Loras → Renly Baratheon | asos-sansa-01 |
| 3009 | 1 | Dreads | `(LLM tail)` | Sansa → Cersei Lannister | asos-sansa-01 |
| 3010 | 1 | Proposes match between | `(LLM tail)` | Lady Olenna → Sansa and Willas | asos-sansa-01 |
| 3011 | 1 | Commands wardrobe for | `COMMANDS` | Cersei Lannister → Sansa Stark | asos-sansa-02 |
| 3012 | 1 | Enjoys companionship of | `(LLM tail)` | Sansa Stark → Margaery Tyrell | asos-sansa-02 |
| 3013 | 1 | Treats as sister | `SIBLING_OF` | Margaery Tyrell → Sansa Stark | asos-sansa-02 |
| 3014 | 1 | Warns about Joffrey | `ADVISES` | Sansa Stark → Margaery Tyrell | asos-sansa-02 |
| 3015 | 1 | Dismisses Sansa's warning about | `ADVISES` | Margaery Tyrell → Joffrey Baratheon | asos-sansa-02 |
| 3016 | 1 | Leads/rules | `COMMANDS` | Elinor Tyrell → Alla Tyrell, Megga Tyrell | asos-sansa-02 |
| 3017 | 1 | Pitied by (mistakenly) | `(LLM tail)` | Sansa Stark → Megga Tyrell | asos-sansa-02 |
| 3018 | 1 | Pities and envies | `(LLM tail)` | Sansa Stark → Tyrell cousins | asos-sansa-02 |
| 3019 | 1 | Teaches harp to | `TEACHES` | Lady Leonette → Sansa Stark | asos-sansa-02 |
| 3020 | 1 | Reminds Sansa of | `(LLM tail)` | Lady Bulwer → Arya Stark | asos-sansa-02 |
| 3021 | 1 | Idealizes | `(LLM tail)` | Sansa Stark → Ser Loras Tyrell | asos-sansa-02 |
| 3022 | 1 | Acts as self-styled protector of | `(LLM tail)` | Ser Dontos Hollard → Sansa Stark | asos-sansa-02 |
| 3023 | 1 | Distrusts/rejects plan of | `DISTRUSTS` | Sansa Stark → Ser Dontos Hollard | asos-sansa-02 |
| 3024 | 1 | Warns Sansa about | `ADVISES` | Dontos Hollard → House Tyrell | asos-sansa-02 |
| 3025 | 1 | Forced conditions on | `(LLM tail)` | Mace Tyrell → Joffrey Baratheon | asos-sansa-02 |
| 3026 | 1 | Kingsguard protector of | `(LLM tail)` | Ser Loras Tyrell → Margaery Tyrell | asos-sansa-02 |
| 3027 | 1 | Recalls with complex emotion | `(LLM tail)` | Sansa Stark → Sandor Clegane | asos-sansa-02 |
| 3028 | 1 | Married to (forced, unconsummated) | `(LLM tail)` | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| 3029 | 1 | Desired by (hoped-for betrothal lost) | `BETROTHED_TO` | Sansa Stark → Willas Tyrell | asos-sansa-03 |
| 3030 | 1 | Previously married to | `(LLM tail)` | Tyrion Lannister → Tysha | asos-sansa-03 |
| 3031 | 1 | Obeys reluctantly | `SERVES` | Tyrion Lannister → Tywin Lannister | asos-sansa-03 |
| 3032 | 1 | Sexually threatens | `(LLM tail)` | Joffrey Baratheon → Sansa Stark | asos-sansa-03 |
| 3033 | 1 | Sympathetic but distanced from | `(LLM tail)` | Margaery Tyrell → Sansa Stark | asos-sansa-03 |
| 3034 | 1 | Ignores | `(LLM tail)` | Olenna Tyrell → Sansa Stark | asos-sansa-03 |
| 3035 | 1 | Distance from | `(LLM tail)` | Elinor, Alla, Megga Tyrell → Sansa Stark | asos-sansa-03 |
| 3036 | 1 | Humiliated by | `(LLM tail)` | Dontos Hollard → Joffrey Baratheon | asos-sansa-03 |
| 3037 | 1 | Previously warned | `ADVISES` | Dontos Hollard → Sansa Stark | asos-sansa-03 |
| 3038 | 1 | Innocent affection toward | `LOVES` | Tommen Baratheon → Sansa Stark | asos-sansa-03 |
| 3039 | 1 | Remembers kindness from | `(LLM tail)` | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| 3040 | 1 | Feels pity toward | `(LLM tail)` | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| 3041 | 1 | Shows restraint/honor toward | `(LLM tail)` | Tyrion Lannister → Sansa Stark | asos-sansa-03 |
| 3042 | 1 | Named | `(LLM tail)` | Willas Tyrell → Ser Garlan Tyrell | asos-sansa-03 |
| 3043 | 1 | Married to (unwilling) | `(LLM tail)` | Sansa → Tyrion | asos-sansa-04 |
| 3044 | 1 | Wary then sympathetic toward | `(LLM tail)` | Sansa → Podrick Payne | asos-sansa-04 |
| 3045 | 1 | Attempting trust with | `(LLM tail)` | Tyrion → Sansa | asos-sansa-04 |
| 3046 | 1 | Threatens / humiliates | `OPPOSES` | Joffrey → Sansa | asos-sansa-04 |
| 3047 | 1 | Controls information about | `COMMANDS` | Cersei → Sansa | asos-sansa-04 |
| 3048 | 1 | Supports / equips | `(LLM tail)` | Tywin → Joffrey | asos-sansa-04 |
| 3049 | 1 | Rebukes | `(LLM tail)` | Ser Garlan Tyrell → Joffrey | asos-sansa-04 |
| 3050 | 1 | Curries favor with | `(LLM tail)` | Mace Tyrell → Joffrey | asos-sansa-04 |
| 3051 | 1 | Serves (with attitude) | `SERVES` | Shae → Sansa | asos-sansa-04 |
| 3052 | 1 | Serves (deferentially) | `SERVES` | Brella → Sansa | asos-sansa-04 |
| 3053 | 1 | Manipulated ward/escaped prisoner | `(LLM tail)` | Sansa Stark → Petyr Baelish | asos-sansa-05 |
| 3054 | 1 | Puppet master / employer | `(LLM tail)` | Petyr Baelish → Ser Dontos Hollard | asos-sansa-05 |
| 3055 | 1 | Orders execution of | `(LLM tail)` | Petyr Baelish → Ser Dontos Hollard | asos-sansa-05 |
| 3056 | 1 | Rescuer / guide (catspaw) | `(LLM tail)` | Ser Dontos Hollard → Sansa Stark | asos-sansa-05 |
| 3057 | 1 | Saved his life previously | `(LLM tail)` | Sansa Stark → Ser Dontos Hollard | asos-sansa-05 |
| 3058 | 1 | Loyal subordinate | `SERVES` | Ser Lothor Brune → Petyr Baelish | asos-sansa-05 |
| 3059 | 1 | Estranged wife | `(LLM tail)` | Sansa Stark → Tyrion Lannister | asos-sansa-05 |
| 3060 | 1 | Relief at death of | `(LLM tail)` | Sansa Stark → Joffrey Baratheon | asos-sansa-05 |
| 3061 | 1 | Former lover / obsession | `LOVER_OF` | Petyr Baelish → Catelyn Stark | asos-sansa-05 |
| 3062 | 1 | Claims paternal affection for | `LOVES` | Petyr Baelish → Sansa Stark | asos-sansa-05 |
| 3063 | 1 | Received Harrenhal and title from | `(LLM tail)` | Petyr Baelish → Joffrey Baratheon | asos-sansa-05 |
| 3064 | 1 | Antagonist to / avoids | `(LLM tail)` | Petyr Baelish → Varys | asos-sansa-05 |
| 3065 | 1 | Protects / manipulates | `PROTECTS` | Petyr Baelish → Sansa Stark | asos-sansa-06 |
| 3066 | 1 | Used / discarded | `(LLM tail)` | Petyr Baelish → Dontos Hollard | asos-sansa-06 |
| 3067 | 1 | Cold toward / possessive of | `(LLM tail)` | Lysa Arryn → Sansa Stark | asos-sansa-06 |
| 3068 | 1 | Sexually assaults | `(LLM tail)` | Marillion → Sansa Stark | asos-sansa-06 |
| 3069 | 1 | kisses against her will / exerts control over | `(LLM tail)` | Petyr Baelish → Sansa Stark | asos-sansa-07 |
| 3070 | 1 | obsessed with / loves the memory of | `(LLM tail)` | Petyr Baelish → Catelyn Stark | asos-sansa-07 |
| 3071 | 1 | manipulates / murders | `MANIPULATES` | Petyr Baelish → Lysa Arryn | asos-sansa-07 |
| 3072 | 1 | frames for murder | `KILLS` | Petyr Baelish → Marillion | asos-sansa-07 |
| 3073 | 1 | jealous of / threatens | `(LLM tail)` | Lysa Arryn → Sansa Stark | asos-sansa-07 |
| 3074 | 1 | jealous of / resents | `(LLM tail)` | Lysa Arryn → Catelyn Stark | asos-sansa-07 |
| 3075 | 1 | poisoned at Petyr's instruction | `(LLM tail)` | Lysa Arryn → Jon Arryn | asos-sansa-07 |
| 3076 | 1 | dotes on / favors | `(LLM tail)` | Lysa Arryn → Marillion | asos-sansa-07 |
| 3077 | 1 | fears / is repulsed by | `FEARS` | Sansa Stark → Marillion | asos-sansa-07 |
| 3078 | 1 | dreads / fears | `(LLM tail)` | Sansa Stark → Robert Arryn (as husband) | asos-sansa-07 |
| 3079 | 1 | dislikes / resents | `(LLM tail)` | Robert Arryn → Sansa Stark | asos-sansa-07 |
| 3080 | 1 | desires / pursues | `(LLM tail)` | Marillion → Sansa Stark | asos-sansa-07 |
| 3081 | 1 | resents her father for | `RESENTS` | Lysa Arryn → Lord Hoster Tully | asos-sansa-07 |
| 3082 | 1 | forced to abort / forced marriage on | `(LLM tail)` | Lord Hoster Tully → Lysa Arryn | asos-sansa-07 |
| 3083 | 1 | claims Catelyn was dismissed by | `(LLM tail)` | Lysa Arryn → Petyr Baelish | asos-sansa-07 |
| 3084 | 1 | treats medically | `(LLM tail)` | Maester Colemon → Robert Arryn | asos-sansa-07 |
| 3085 | 1 | deceived / used false promises with | `(LLM tail)` | Petyr Baelish → Sansa Stark | asos-sansa-07 |
| 3086 | 1 | Employs / depends on | `(LLM tail)` | Tyrion → Bronn | asos-tyrion-01 |
| 3087 | 1 | Fears and suspects | `FEARS` | Tyrion → Cersei | asos-tyrion-01 |
| 3088 | 1 | Antagonistic submission to | `OPPOSES` | Tyrion → Tywin | asos-tyrion-01 |
| 3089 | 1 | Questions paternity of | `(LLM tail)` | Tywin → Tyrion | asos-tyrion-01 |
| 3090 | 1 | Mercenary loyalty to | `(LLM tail)` | Bronn → Tyrion | asos-tyrion-01 |
| 3091 | 1 | Disrespectful toward | `(LLM tail)` | Bronn → Tywin | asos-tyrion-01 |
| 3092 | 1 | Protective guilt toward | `(LLM tail)` | Tyrion → Alayaya | asos-tyrion-01 |
| 3093 | 1 | Protective secrecy toward | `(LLM tail)` | Tyrion → Shae | asos-tyrion-01 |
| 3094 | 1 | Bitter rivalry with | `RESENTS` | Tyrion → Cersei | asos-tyrion-01 |
| 3095 | 1 | Insists on finding | `(LLM tail)` | Tywin → Tyrek | asos-tyrion-01 |
| 3096 | 1 | Values instrumentally | `(LLM tail)` | Tywin → Gregor Clegane | asos-tyrion-01 |
| 3097 | 1 | Uneasy intelligence-sharing with | `(LLM tail)` | Tyrion → Varys | asos-tyrion-02 |
| 3098 | 1 | Antagonistic son of | `OPPOSES` | Tyrion → Tywin Lannister | asos-tyrion-02 |
| 3099 | 1 | Spies on Tyrion for | `SPIES_ON` | Varys → Tywin Lannister | asos-tyrion-02 |
| 3100 | 1 | Facilitates meetings for | `(LLM tail)` | Varys → Tyrion and Shae | asos-tyrion-02 |
| 3101 | 1 | Manipulates through implied sexual favors | `MANIPULATES` | Cersei → Ser Osmund Kettleblack | asos-tyrion-02 |
| 3102 | 1 | Report to / serve | `(LLM tail)` | Kettleblacks → Cersei Lannister | asos-tyrion-02 |
| 3103 | 1 | Serves as maidservant to (cover identity) | `SERVES` | Shae → Lollys Stokeworth | asos-tyrion-02 |
| 3104 | 1 | Feels protective toward / guilty about | `(LLM tail)` | Tyrion → Alayaya | asos-tyrion-02 |
| 3105 | 1 | Beds | `(LLM tail)` | Bronn → Alayaya and Marei | asos-tyrion-02 |
| 3106 | 1 | Creature of / loyal to | `(LLM tail)` | Grand Maester Pycelle → House Lannister | asos-tyrion-02 |
| 3107 | 1 | Potential threat to | `(LLM tail)` | Symon Silver Tongue → Tyrion and Shae | asos-tyrion-02 |
| 3108 | 1 | Nostalgic grief for | `MOURNS` | Tyrion → Tysha | asos-tyrion-02 |
| 3109 | 1 | Mourns / loves (unnamed person) | `MOURNS` | Ser Loras → (unnamed) | asos-tyrion-02 |
| 3110 | 1 | serves as vanguard for | `SERVES` | Kevan Lannister → Tywin Lannister | asos-tyrion-03 |
| 3111 | 1 | takes pleasure in suffering of | `(LLM tail)` | Tyrion Lannister → Cersei Lannister | asos-tyrion-03 |
| 3112 | 1 | refuses to obey | `SERVES` | Cersei Lannister → Tywin Lannister | asos-tyrion-03 |
| 3113 | 1 | feels no remorse toward | `(LLM tail)` | Tyrion Lannister → Pycelle | asos-tyrion-03 |
| 3114 | 1 | strategic alliance with | `ALLIES_WITH` | Tywin Lannister → House Tyrell | asos-tyrion-03 |
| 3115 | 1 | sexually used | `(LLM tail)` | Cersei Lannister → Lancel Lannister | asos-tyrion-03 |
| 3116 | 1 | may wish to silence | `(LLM tail)` | Cersei Lannister → Lancel Lannister | asos-tyrion-03 |
| 3117 | 1 | uses strategically | `(LLM tail)` | Tywin Lannister → Sansa Stark | asos-tyrion-03 |
| 3118 | 1 | thinks of brother re: Cersei's marriage | `SIBLING_OF` | Tyrion Lannister → Jaime Lannister | asos-tyrion-03 |
| 3119 | 1 | suspicious reaction to | `(LLM tail)` | Tywin Lannister → Westerling marriage | asos-tyrion-03 |
| 3120 | 1 | ominous toward | `(LLM tail)` | Tywin Lannister → House Westerling | asos-tyrion-03 |
| 3121 | 1 | broke oath to | `(LLM tail)` | Robb Stark → House Frey | asos-tyrion-03 |
| 3122 | 1 | recalls with fear | `FEARS` | Tyrion Lannister → Eyrie sky cells | asos-tyrion-03 |
| 3123 | 1 | unconsummated marriage | `(LLM tail)` | Tyrion → Sansa Stark | asos-tyrion-04 |
| 3124 | 1 | secret lover | `LOVER_OF` | Tyrion → Shae | asos-tyrion-04 |
| 3125 | 1 | blackmailed by | `(LLM tail)` | Tyrion → Symon Silver Tongue | asos-tyrion-04 |
| 3126 | 1 | orders murder of | `KILLS` | Tyrion → Symon Silver Tongue | asos-tyrion-04 |
| 3127 | 1 | son of (strained, subservient) | `PARENT_OF` | Tyrion → Tywin Lannister | asos-tyrion-04 |
| 3128 | 1 | relies on (reluctantly) | `(LLM tail)` | Tywin → Tyrion | asos-tyrion-04 |
| 3129 | 1 | squire | `(LLM tail)` | Tyrion → Podrick Payne | asos-tyrion-04 |
| 3130 | 1 | loyal to (for pay) | `SERVES` | Bronn → Tyrion | asos-tyrion-04 |
| 3131 | 1 | distrusts/resents | `DISTRUSTS` | Tyrion → Cersei | asos-tyrion-04 |
| 3132 | 1 | liked/respected | `RESPECTS` | Tyrion → Jeor Mormont | asos-tyrion-04 |
| 3133 | 1 | relied on | `(LLM tail)` | Tywin → Ser Kevan Lannister | asos-tyrion-04 |
| 3134 | 1 | grief-stricken over | `MOURNS` | Ser Kevan → Willem, Martyn, Lancel | asos-tyrion-04 |
| 3135 | 1 | created financial crisis for | `(LLM tail)` | Littlefinger → The Crown | asos-tyrion-04 |
| 3136 | 1 | knows about | `(LLM tail)` | Symon Silver Tongue → Shae | asos-tyrion-04 |
| 3137 | 1 | lord and squire | `(LLM tail)` | Tyrion → Podrick Payne | asos-tyrion-05 |
| 3138 | 1 | lord and sworn knight | `(LLM tail)` | Tyrion → Bronn | asos-tyrion-05 |
| 3139 | 1 | brother (substitute) | `SIBLING_OF` | Oberyn → Doran Martell | asos-tyrion-05 |
| 3140 | 1 | paramour/lover | `LOVER_OF` | Oberyn → Ellaria Sand | asos-tyrion-05 |
| 3141 | 1 | deep sibling bond | `(LLM tail)` | Oberyn → Elia Martell | asos-tyrion-05 |
| 3142 | 1 | vengeance-seeker | `(LLM tail)` | Oberyn → Gregor Clegane | asos-tyrion-05 |
| 3143 | 1 | implicit antagonist | `(LLM tail)` | Oberyn → Tywin Lannister | asos-tyrion-05 |
| 3144 | 1 | hatred from infancy | `HATES` | Cersei → Tyrion | asos-tyrion-05 |
| 3145 | 1 | deep love (past) | `LOVES` | Tywin → Joanna Lannister | asos-tyrion-05 |
| 3146 | 1 | favorite nephew | `NEPHEW_OF` | Tyrion → Gerion Lannister | asos-tyrion-05 |
| 3147 | 1 | cold host | `(LLM tail)` | Tywin → Oberyn's family | asos-tyrion-05 |
| 3148 | 1 | no ill will, correspondents | `(LLM tail)` | Oberyn → Willas Tyrell | asos-tyrion-05 |
| 3149 | 1 | contempt/blame | `HATES` | Oberyn → Mace Tyrell | asos-tyrion-05 |
| 3150 | 1 | strained service | `(LLM tail)` | Tyrion → Tywin Lannister | asos-tyrion-05 |
| 3151 | 1 | cold father | `(LLM tail)` | Tywin → Tyrion | asos-tyrion-05 |
| 3152 | 1 | natural son | `(LLM tail)` | Ser Daemon Sand → Ser Ryon Allyrion | asos-tyrion-05 |
| 3153 | 1 | mocking familiarity | `(LLM tail)` | Oberyn → Tyrion | asos-tyrion-05 |
| 3154 | 1 | investigated | `(LLM tail)` | Jon Arryn → Doran Martell / Sunspear | asos-tyrion-05 |
| 3155 | 1 | Strained marriage | `(LLM tail)` | Tyrion → Sansa | asos-tyrion-06 |
| 3156 | 1 | Subordinate/resentful toward | `RESENTS` | Tyrion → Tywin | asos-tyrion-06 |
| 3157 | 1 | Mastermind of | `(LLM tail)` | Tywin → Walder Frey | asos-tyrion-06 |
| 3158 | 1 | Shocked by | `(LLM tail)` | Ser Kevan → Joffrey | asos-tyrion-06 |
| 3159 | 1 | Pious devotion | `(LLM tail)` | Sansa → The old gods / Faith of the Seven | asos-tyrion-06 |
| 3160 | 1 | Demands justice from | `(LLM tail)` | Oberyn Martell → Tywin / the crown | asos-tyrion-06 |
| 3161 | 1 | Refuses to surrender | `(LLM tail)` | Tywin → Gregor Clegane | asos-tyrion-06 |
| 3162 | 1 | Physically abusive toward | `(LLM tail)` | Robert Baratheon → Joffrey | asos-tyrion-06 |
| 3163 | 1 | Pragmatic view of | `(LLM tail)` | Tywin → Elia Martell | asos-tyrion-06 |
| 3164 | 1 | Unconsummated husband of | `(LLM tail)` | Tyrion → Sansa | asos-tyrion-07 |
| 3165 | 1 | Shields from ugly truths | `(LLM tail)` | Tyrion → Sansa | asos-tyrion-07 |
| 3166 | 1 | Prays nightly in the | `(LLM tail)` | Sansa → Godswood | asos-tyrion-07 |
| 3167 | 1 | Wary alliance with | `ALLIES_WITH` | Tyrion → Varys | asos-tyrion-07 |
| 3168 | 1 | Placed Brella in Tyrion's household | `(LLM tail)` | Varys → Brella | asos-tyrion-07 |
| 3169 | 1 | Considers sending Shae to | `(LLM tail)` | Tyrion → Chataya | asos-tyrion-07 |
| 3170 | 1 | Fears punishment from | `FEARS` | Tyrion → Tywin Lannister | asos-tyrion-07 |
| 3171 | 1 | married to (strained) | `(LLM tail)` | Tyrion → Sansa | asos-tyrion-08 |
| 3172 | 1 | suspects/accuses (internally) | `(LLM tail)` | Tyrion → Joffrey | asos-tyrion-08 |
| 3173 | 1 | attempts to manage | `(LLM tail)` | Margaery → Joffrey | asos-tyrion-08 |
| 3174 | 1 | manipulates/interacts with | `MANIPULATES` | Lady Olenna → Sansa | asos-tyrion-08 |
| 3175 | 1 | needles | `(LLM tail)` | Lady Olenna → Tyrion | asos-tyrion-08 |
| 3176 | 1 | respects/defends | `RESPECTS` | Ser Garlan → Tyrion | asos-tyrion-08 |
| 3177 | 1 | dutiful but cold toward | `(LLM tail)` | Sansa → Tyrion | asos-tyrion-08 |
| 3178 | 1 | controlled by threat of | `(LLM tail)` | Joffrey → Tyrion | asos-tyrion-08 |
| 3179 | 1 | placed Dornishmen far from | `(LLM tail)` | Cersei → Tyrells | asos-tyrion-08 |
| 3180 | 1 | weakened, dependent on | `(LLM tail)` | Lancel → Ser Kevan | asos-tyrion-08 |
| 3181 | 1 | performs courtesy for | `(LLM tail)` | Sansa → Lancel, Lord Gyles, Elinor Tyrell, Jalabhar Xho | asos-tyrion-08 |
| 3182 | 1 | admires Sansa's social skill | `RESPECTS` | Tyrion → Sansa | asos-tyrion-08 |
| 3183 | 1 | accused by / opposed by | `(LLM tail)` | Tyrion → Cersei | asos-tyrion-09 |
| 3184 | 1 | served loyally by | `(LLM tail)` | Tyrion → Podrick Payne | asos-tyrion-09 |
| 3185 | 1 | judged by | `(LLM tail)` | Tyrion → Lord Tywin | asos-tyrion-09 |
| 3186 | 1 | intermediary for | `(LLM tail)` | Ser Kevan → Tywin | asos-tyrion-09 |
| 3187 | 1 | loves/defends | `LOVES` | Ser Kevan → Tywin | asos-tyrion-09 |
| 3188 | 1 | offers to champion | `(LLM tail)` | Prince Oberyn → Tyrion | asos-tyrion-09 |
| 3189 | 1 | distrusts/disdains | `DISTRUSTS` | Prince Oberyn → Cersei | asos-tyrion-09 |
| 3190 | 1 | married to (estranged) | `(LLM tail)` | Tyrion → Sansa Stark | asos-tyrion-09 |
| 3191 | 1 | believes poisoned Joffrey | `(LLM tail)` | Tyrion → Sansa | asos-tyrion-09 |
| 3192 | 1 | has already condemned | `(LLM tail)` | Mace Tyrell → Tyrion | asos-tyrion-09 |
| 3193 | 1 | offered children to | `(LLM tail)` | Lord Tywin → King Robert | asos-tyrion-09 |
| 3194 | 1 | Betrayed by (former lover) | `BETRAYS` | Tyrion → Shae | asos-tyrion-10 |
| 3195 | 1 | Self-blame regarding | `(LLM tail)` | Tyrion → Shae | asos-tyrion-10 |
| 3196 | 1 | Gratitude toward | `(LLM tail)` | Tyrion → Podrick Payne | asos-tyrion-10 |
| 3197 | 1 | Dependence on / alliance with | `ALLIES_WITH` | Tyrion → Prince Oberyn | asos-tyrion-10 |
| 3198 | 1 | Vengeance-driven motivation against | `(LLM tail)` | Prince Oberyn → Ser Gregor Clegane | asos-tyrion-10 |
| 3199 | 1 | Sibling devotion to | `(LLM tail)` | Prince Oberyn → Elia Martell | asos-tyrion-10 |
| 3200 | 1 | Political alliance proposed with | `ALLIES_WITH` | Prince Oberyn → Tyrion | asos-tyrion-10 |
| 3201 | 1 | Cold judgment of | `(LLM tail)` | Lord Tywin → Tyrion | asos-tyrion-10 |
| 3202 | 1 | Control of proceedings | `(LLM tail)` | Lord Tywin → The trial | asos-tyrion-10 |
| 3203 | 1 | Satisfaction at Tyrion's suffering | `(LLM tail)` | Cersei → Tyrion | asos-tyrion-10 |
| 3204 | 1 | Obedience to | `(LLM tail)` | Ser Gregor → Cersei | asos-tyrion-10 |
| 3205 | 1 | Killer of | `(LLM tail)` | Ser Gregor → Oberyn | asos-tyrion-10 |
| 3206 | 1 | Confessed rapist/murderer of | `KILLS` | Ser Gregor → Elia Martell | asos-tyrion-10 |
| 3207 | 1 | Lover of / paramour to | `LOVER_OF` | Ellaria Sand → Prince Oberyn | asos-tyrion-10 |
| 3208 | 1 | Abandoned by (in thought) | `(LLM tail)` | Tyrion → Ser Kevan | asos-tyrion-10 |
| 3209 | 1 | Planned betrothal with | `BETROTHED_TO` | Oberyn's mother → Joanna Lannister | asos-tyrion-10 |
| 3210 | 1 | Refused betrothal / insulted | `BETROTHED_TO` | Lord Tywin → Oberyn's mother / Dorne | asos-tyrion-10 |
| 3211 | 1 | Judge / questioner | `(LLM tail)` | Mace Tyrell → Tyrion | asos-tyrion-10 |
| 3212 | 1 | Mockery of (past) | `(LLM tail)` | Oberyn → Baelor Hightower | asos-tyrion-10 |
| 3213 | 1 | Kisses farewell | `(LLM tail)` | Jaime → Tyrion | asos-tyrion-11 |
| 3214 | 1 | Confesses guilt to | `(LLM tail)` | Jaime → Tyrion | asos-tyrion-11 |
| 3215 | 1 | Strikes in rage | `(LLM tail)` | Tyrion → Jaime | asos-tyrion-11 |
| 3216 | 1 | Swears vengeance against | `(LLM tail)` | Tyrion → Jaime | asos-tyrion-11 |
| 3217 | 1 | Deliberately wounds | `(LLM tail)` | Tyrion → Jaime | asos-tyrion-11 |
| 3218 | 1 | Watches depart with regret | `(LLM tail)` | Tyrion → Jaime | asos-tyrion-11 |
| 3219 | 1 | Commanded lie about Tysha | `COMMANDS` | Tywin → Jaime | asos-tyrion-11 |
| 3220 | 1 | Assists escape of | `(LLM tail)` | Varys → Tyrion | asos-tyrion-11 |
| 3221 | 1 | Feared by / distrusted by | `(LLM tail)` | Varys → Tyrion | asos-tyrion-11 |
| 3222 | 1 | Arranged testimony against | `(LLM tail)` | Cersei → Tyrion | asos-tyrion-11 |
| 3223 | 1 | In bed with | `(LLM tail)` | Shae → Tywin | asos-tyrion-11 |
| 3224 | 1 | Claimed loyalty to | `(LLM tail)` | Shae → Tyrion | asos-tyrion-11 |
| 3225 | 1 | Claims protector of | `(LLM tail)` | Tywin → Tyrion | asos-tyrion-11 |
| 3226 | 1 | Contempt for / anger toward | `HATES` | Tyrion → Tywin | asos-tyrion-11 |
| 3227 | 1 | Respects (grudging) | `RESPECTS` | Lester → Tyrion | asos-tyrion-11 |
| 3228 | 1 | Attempted murder of | `KILLS` | Joffrey → Brandon Stark | asos-tyrion-11 |
| 3229 | 1 | Suspected | `(LLM tail)` | Jaime → Joffrey | asos-tyrion-11 |
| 3230 | 1 | Poses as natural daughter of | `(LLM tail)` | Alayne → Petyr Baelish | affc-alayne-01 |
| 3231 | 1 | Acts as guardian/father figure with inappropriate undertones toward | `(LLM tail)` | Petyr Baelish → Alayne | affc-alayne-01 |
| 3232 | 1 | Caretaker/companion of | `COMPANION_OF` | Alayne → Robert Arryn | affc-alayne-01 |
| 3233 | 1 | Stepfather and Lord Protector of | `(LLM tail)` | Petyr Baelish → Robert Arryn | affc-alayne-01 |
| 3234 | 1 | Dependent on / obedient to (reluctantly) | `(LLM tail)` | Robert Arryn → Petyr Baelish | affc-alayne-01 |
| 3235 | 1 | Treats / serves | `(LLM tail)` | Maester Colemon → Robert Arryn | affc-alayne-01 |
| 3236 | 1 | Overrules medical judgment of | `(LLM tail)` | Petyr Baelish → Maester Colemon | affc-alayne-01 |
| 3237 | 1 | Ally/supporter of | `ALLIES_WITH` | Nestor Royce → Petyr Baelish | affc-alayne-01 |
| 3238 | 1 | Chief opponent of | `(LLM tail)` | Bronze Yohn Royce → Petyr Baelish | affc-alayne-01 |
| 3239 | 1 | Politically opposed to / estranged from | `(LLM tail)` | Nestor Royce → Bronze Yohn Royce | affc-alayne-01 |
| 3240 | 1 | Secret agent of | `(LLM tail)` | Lyn Corbray → Petyr Baelish | affc-alayne-01 |
| 3241 | 1 | Rivalrous with / resents | `(LLM tail)` | Lyn Corbray → Lyonel Corbray | affc-alayne-01 |
| 3242 | 1 | Allied against | `ALLIES_WITH` | Lords Declarant → Petyr Baelish | affc-alayne-01 |
| 3243 | 1 | Serves / protects | `SERVES` | Lothor Brune → Petyr Baelish | affc-alayne-01 |
| 3244 | 1 | Plans to corrupt / buy | `(LLM tail)` | Petyr Baelish → Benedar Belmore | affc-alayne-01 |
| 3245 | 1 | Plans to befriend | `(LLM tail)` | Petyr Baelish → Symond Templeton | affc-alayne-01 |
| 3246 | 1 | Plans to outlast / isolate | `(LLM tail)` | Petyr Baelish → Bronze Yohn Royce | affc-alayne-01 |
| 3247 | 1 | Predicts murder of | `KILLS` | Petyr Baelish → Gilwood Hunter | affc-alayne-01 |
| 3248 | 1 | Plans against | `(LLM tail)` | Petyr Baelish → Cersei Lannister | affc-alayne-01 |
| 3249 | 1 | Visited / acquainted with | `(LLM tail)` | Bronze Yohn → Stark family (Winterfell) | affc-alayne-01 |
| 3250 | 1 | Suspected of hastening death of | `(LLM tail)` | Gilwood Hunter → Lord Eon Hunter | affc-alayne-01 |
| 3251 | 1 | Caretaker/surrogate mother to | `(LLM tail)` | Alayne → Robert Arryn | affc-alayne-02 |
| 3252 | 1 | Clinging dependence on | `(LLM tail)` | Robert Arryn → Alayne | affc-alayne-02 |
| 3253 | 1 | Manipulator/controller of | `(LLM tail)` | Petyr Baelish → Alayne | affc-alayne-02 |
| 3254 | 1 | Obedience mixed with unease toward | `(LLM tail)` | Alayne → Petyr Baelish | affc-alayne-02 |
| 3255 | 1 | Unaware/indifferent toward | `(LLM tail)` | Mya Stone → Lothor Brune | affc-alayne-02 |
| 3256 | 1 | Developing friendship with | `COMPANION_OF` | Myranda Royce → Alayne | affc-alayne-02 |
| 3257 | 1 | Warming but guarded toward | `(LLM tail)` | Alayne → Myranda Royce | affc-alayne-02 |
| 3258 | 1 | Overrules/dismisses | `(LLM tail)` | Alayne → Maester Colemon | affc-alayne-02 |
| 3259 | 1 | Brokered marriage for | `(LLM tail)` | Petyr Baelish → Lord Lyonel Corbray | affc-alayne-02 |
| 3260 | 1 | Desired to marry | `(LLM tail)` | Myranda Royce → Harrold Hardyng | affc-alayne-02 |
| 3261 | 1 | Complex memory of | `(LLM tail)` | Alayne/Sansa → The Hound | affc-alayne-02 |
| 3262 | 1 | Nostalgic love for absent | `LOVES` | Mya Stone → Robert Baratheon (father) | affc-alayne-02 |
| 3263 | 1 | Plans the death of | `(LLM tail)` | Petyr Baelish → Robert Arryn | affc-alayne-02 |
| 3264 | 1 | passenger / ward of | `(LLM tail)` | Arya → Ternesio Terys | affc-arya-01 |
| 3265 | 1 | friendly acquaintance of | `COMPANION_OF` | Arya → Denyo | affc-arya-01 |
| 3266 | 1 | misses / only living brother | `SIBLING_OF` | Arya → Jon Snow | affc-arya-01 |
| 3267 | 1 | enemies / kill list | `OPPOSES` | Arya → Ser Gregor, Dunsen, Raff the Sweetling, Ser Ilyn, Ser Meryn, Queen Cersei | affc-arya-01 |
| 3268 | 1 | gives mercy to | `(LLM tail)` | Arya → Young man by the pool | affc-arya-01 |
| 3269 | 1 | priest at / authority over | `(LLM tail)` | The kindly man → House of Black and White | affc-arya-01 |
| 3270 | 1 | Student/novice under | `TUTORS` | Arya → The kindly man | affc-arya-02 |
| 3271 | 1 | Language partner with | `(LLM tail)` | Arya → The waif | affc-arya-02 |
| 3272 | 1 | Kitchen worker under | `(LLM tail)` | Arya → Umma | affc-arya-02 |
| 3273 | 1 | Deep attachment to | `(LLM tail)` | Arya → Needle / Jon Snow | affc-arya-02 |
| 3274 | 1 | Abandonment felt toward | `(LLM tail)` | Arya → Hot Pie, Gendry, Yoren, Lommy Greenhands, Harwin | affc-arya-02 |
| 3275 | 1 | Memory/respect toward | `RESPECTS` | Arya → Syrio Forel | affc-arya-02 |
| 3276 | 1 | Memory of servitude under | `(LLM tail)` | Arya → Weese, Roose Bolton | affc-arya-02 |
| 3277 | 1 | Testing/challenging | `(LLM tail)` | The kindly man → Arya | affc-arya-02 |
| 3278 | 1 | Knowing despite secrecy | `(LLM tail)` | The kindly man → Arya | affc-arya-02 |
| 3279 | 1 | Superior at lying game to | `(LLM tail)` | The waif → Arya | affc-arya-02 |
| 3280 | 1 | Given everything to | `(LLM tail)` | The waif → The Many-Faced God | affc-arya-02 |
| 3281 | 1 | Contempt/affection toward | `HATES` | Arya → The waif | affc-arya-02 |
| 3282 | 1 | Wolf-dream connection to | `(LLM tail)` | Arya → A wolf pack | affc-arya-02 |
| 3283 | 1 | Sworn to serve / searching for | `SWORN_TO` | Brienne → Sansa Stark | affc-brienne-01 |
| 3284 | 1 | Trusted by / given mission by | `(LLM tail)` | Brienne → Jaime Lannister | affc-brienne-01 |
| 3285 | 1 | Devoted to (dead) | `(LLM tail)` | Brienne → Renly Baratheon | affc-brienne-01 |
| 3286 | 1 | Promised service to (dead) | `(LLM tail)` | Brienne → Lady Catelyn Stark | affc-brienne-01 |
| 3287 | 1 | Boastful toward / patronizing to | `(LLM tail)` | Ser Creighton → Brienne | affc-brienne-01 |
| 3288 | 1 | Suspicious of / accuses | `(LLM tail)` | Ser Illifer → Brienne | affc-brienne-01 |
| 3289 | 1 | Rival hunter / competitor | `(LLM tail)` | Ser Shadrich → Brienne | affc-brienne-01 |
| 3290 | 1 | Hired escort of | `(LLM tail)` | Ser Shadrich → Hibald | affc-brienne-01 |
| 3291 | 1 | Debtor to | `(LLM tail)` | Ser Creighton → Naggle (innkeep) | affc-brienne-01 |
| 3292 | 1 | Reciprocates hospitality to | `(LLM tail)` | Brienne → Ser Creighton, Ser Illifer | affc-brienne-01 |
| 3293 | 1 | Respectful of (grudging) | `RESPECTS` | Brienne → Jaime Lannister | affc-brienne-01 |
| 3294 | 1 | Helped to escape by (inferred) | `(LLM tail)` | Sansa Stark → Ser Dontos the Red | affc-brienne-01 |
| 3295 | 1 | Showed courtesy to | `(LLM tail)` | Renly Baratheon → Brienne | affc-brienne-01 |
| 3296 | 1 | Sworn service / loyalty beyond death | `(LLM tail)` | Brienne → Catelyn Stark | affc-brienne-02 |
| 3297 | 1 | Complex emotional attachment | `(LLM tail)` | Brienne → Jaime Lannister | affc-brienne-02 |
| 3298 | 1 | Devotion / idealized love | `LOVES` | Brienne → Renly Baratheon | affc-brienne-02 |
| 3299 | 1 | Quest target | `(LLM tail)` | Brienne → Sansa Stark | affc-brienne-02 |
| 3300 | 1 | Suspicion then sympathy | `(LLM tail)` | Brienne → Podrick Payne | affc-brienne-02 |
| 3301 | 1 | Squire to (abandoned) | `SERVES` | Podrick Payne → Tyrion Lannister | affc-brienne-02 |
| 3302 | 1 | Wife (blamed for influencing) | `(LLM tail)` | Lady Serala (Lace Serpent) → Lord Denys Darklyn | affc-brienne-02 |
| 3303 | 1 | Spared / protected | `(LLM tail)` | Barristan Selmy → Dontos Hollard | affc-brienne-02 |
| 3304 | 1 | Broke betrothal with | `BETROTHED_TO` | Brienne → Humfrey Wagstaff | affc-brienne-02 |
| 3305 | 1 | Harsh mentor | `TUTORS` | Septa Roelle → Brienne | affc-brienne-02 |
| 3306 | 1 | Former maid of | `(LLM tail)` | Brella → Sansa Stark | affc-brienne-02 |
| 3307 | 1 | Rode with | `(LLM tail)` | Lord Rykker → Randyll Tarly | affc-brienne-02 |
| 3308 | 1 | Informant to | `(LLM tail)` | Dwarf holy brother → Brienne | affc-brienne-02 |
| 3309 | 1 | "Fooled a fool" | `(LLM tail)` | Nimble Dick → The fool at Maidenpool | affc-brienne-02 |
| 3310 | 1 | Military command | `COMMANDS` | Randyll Tarly → Joffrey's army at Duskendale | affc-brienne-02 |
| 3311 | 1 | protective mentor / reluctant companion | `COMPANION_OF` | Brienne → Podrick Payne | affc-brienne-03 |
| 3312 | 1 | mocking familiarity / unresolved guilt | `(LLM tail)` | Ser Hyle Hunt → Brienne | affc-brienne-03 |
| 3313 | 1 | fear and resentment | `FEARS` | Brienne → Lord Randyll Tarly | affc-brienne-03 |
| 3314 | 1 | dominance / authority | `(LLM tail)` | Lord Randyll Tarly → Lord Mooton | affc-brienne-03 |
| 3315 | 1 | conflicted memory of loathing and shared experience | `(LLM tail)` | Brienne → Ser Jaime Lannister | affc-brienne-03 |
| 3316 | 1 | loyalty and gratitude | `(LLM tail)` | Brienne → Lady Catelyn Stark | affc-brienne-03 |
| 3317 | 1 | mission devotion | `(LLM tail)` | Brienne → Sansa Stark | affc-brienne-03 |
| 3318 | 1 | mercenary guide | `(LLM tail)` | Dick Crabb → Brienne | affc-brienne-03 |
| 3319 | 1 | wary employer | `(LLM tail)` | Brienne → Dick Crabb | affc-brienne-03 |
| 3320 | 1 | squire (former) | `(LLM tail)` | Podrick Payne → Tyrion Lannister | affc-brienne-03 |
| 3321 | 1 | treated as servant, not son | `(LLM tail)` | Ser Cedric Payne → Podrick Payne | affc-brienne-03 |
| 3322 | 1 | corrupting influence | `(LLM tail)` | Ser Lorimer the Belly → Podrick Payne | affc-brienne-03 |
| 3323 | 1 | executioner | `(LLM tail)` | Lord Tywin Lannister → Ser Lorimer the Belly | affc-brienne-03 |
| 3324 | 1 | took charge of | `(LLM tail)` | Ser Kevan Lannister → Podrick Payne | affc-brienne-03 |
| 3325 | 1 | subordination (rebukes) | `SERVES` | Lord Randyll Tarly → Ser Hyle Hunt | affc-brienne-03 |
| 3326 | 1 | betrothed to (past, ended by death) | `BETROTHED_TO` | Brienne → Lord Caron's younger son | affc-brienne-03 |
| 3327 | 1 | distrusts/employs as guide | `DISTRUSTS` | Brienne → Nimble Dick | affc-brienne-04 |
| 3328 | 1 | yearns for/respects | `RESPECTS` | Brienne → Jaime Lannister | affc-brienne-04 |
| 3329 | 1 | guides (for gold) | `(LLM tail)` | Nimble Dick → Brienne | affc-brienne-04 |
| 3330 | 1 | ancestral pride in | `(LLM tail)` | Nimble Dick → Ser Clarence Crabb / House Crabb | affc-brienne-04 |
| 3331 | 1 | sold map to | `(LLM tail)` | Nimble Dick → Shagwell, Timeon, Pyg | affc-brienne-04 |
| 3332 | 1 | former members of | `(LLM tail)` | Shagwell, Timeon, Pyg → Brave Companions (Bloody Mummers) | affc-brienne-04 |
| 3333 | 1 | follows on orders of | `(LLM tail)` | Hyle Hunt → Randyll Tarly | affc-brienne-04 |
| 3334 | 1 | former enemy of/contempt for | `(LLM tail)` | Brienne → Hyle Hunt | affc-brienne-04 |
| 3335 | 1 | resents memory of | `RESENTS` | Brienne → Septa Roelle | affc-brienne-04 |
| 3336 | 1 | reveres memory of | `(LLM tail)` | Brienne → Ser Goodwin | affc-brienne-04 |
| 3337 | 1 | reportedly abducted | `(LLM tail)` | Sandor Clegane (the Hound) → Sansa Stark | affc-brienne-04 |
| 3338 | 1 | searching for | `SEEKS` | Beric Dondarrion → Sansa Stark | affc-brienne-04 |
| 3339 | 1 | killed (dismembered) | `KILLS` | Gregor Clegane (the Mountain) → Vargo Hoat | affc-brienne-04 |
| 3340 | 1 | Contempt/hostility toward | `HATES` | Randyll Tarly → Brienne | affc-brienne-05 |
| 3341 | 1 | Motivated by reward regarding | `(LLM tail)` | Hyle Hunt → Sansa Stark | affc-brienne-05 |
| 3342 | 1 | Serves as knight to | `SERVES` | Brienne → Podrick Payne | affc-brienne-05 |
| 3343 | 1 | Rules in place of | `RULES` | Randyll Tarly → Lord Mooton | affc-brienne-05 |
| 3344 | 1 | Guide/companion to | `COMPANION_OF` | Septon Meribald → Brienne's party | affc-brienne-05 |
| 3345 | 1 | Memory of past journey with | `(LLM tail)` | Brienne → Jaime | affc-brienne-05 |
| 3346 | 1 | Haunted by kills of | `(LLM tail)` | Brienne → Shagwell, Timeon, Pyg | affc-brienne-05 |
| 3347 | 1 | Seeks to punish | `SEEKS` | Dondarrion's brotherhood → Sandor Clegane | affc-brienne-05 |
| 3348 | 1 | Pity for/moved by | `(LLM tail)` | Brienne → Broken men | affc-brienne-05 |
| 3349 | 1 | Hunting/seeking to kill | `(LLM tail)` | Brienne → Sandor Clegane (the Hound) | affc-brienne-06 |
| 3350 | 1 | Sworn protector / questing for | `(LLM tail)` | Brienne → Sansa Stark | affc-brienne-06 |
| 3351 | 1 | Reluctant traveling companion | `COMPANION_OF` | Brienne → Ser Hyle Hunt | affc-brienne-06 |
| 3352 | 1 | Found, tended, and buried | `(LLM tail)` | Elder Brother → Sandor Clegane | affc-brienne-06 |
| 3353 | 1 | Counselor / protective toward | `ADVISES` | Elder Brother → Brienne | affc-brienne-06 |
| 3354 | 1 | Former knight who fought for | `(LLM tail)` | Elder Brother → Prince Rhaegar | affc-brienne-06 |
| 3355 | 1 | Hated / dreamed of killing | `(LLM tail)` | Sandor Clegane → Gregor Clegane | affc-brienne-06 |
| 3356 | 1 | Abducted / traveled with | `(LLM tail)` | Sandor Clegane → Arya Stark | affc-brienne-06 |
| 3357 | 1 | Poisoned/wounded | `(LLM tail)` | Prince Oberyn → Gregor Clegane | affc-brienne-06 |
| 3358 | 1 | Failed to protect | `(LLM tail)` | Ser Quincy Cox → People of Saltpans | affc-brienne-06 |
| 3359 | 1 | Dueled / complex bond with | `(LLM tail)` | Brienne → Jaime (Lannister) | affc-brienne-06 |
| 3360 | 1 | Bit the ear of | `(LLM tail)` | Brienne → Vargo Hoat | affc-brienne-06 |
| 3361 | 1 | Former warhorse of | `(LLM tail)` | Driftwood (Stranger) → Sandor Clegane | affc-brienne-06 |
| 3362 | 1 | Told Brienne about | `(LLM tail)` | Timeon → The Hound and Sansa/Arya | affc-brienne-06 |
| 3363 | 1 | Former keeper of | `(LLM tail)` | Masha Heddle → The crossroads inn | affc-brienne-06 |
| 3364 | 1 | Yearning/conflicted feelings toward | `(LLM tail)` | Brienne → Ser Jaime Lannister | affc-brienne-07 |
| 3365 | 1 | Deep grief/devotion to memory of | `MOURNS` | Brienne → Renly Baratheon | affc-brienne-07 |
| 3366 | 1 | Yearning for | `(LLM tail)` | Brienne → Lord Selwyn (father) / Tarth | affc-brienne-07 |
| 3367 | 1 | Desires marriage with (mercenary) | `(LLM tail)` | Ser Hyle Hunt → Brienne | affc-brienne-07 |
| 3368 | 1 | Fondness for memory of | `(LLM tail)` | Septon Meribald → Masha Heddle | affc-brienne-07 |
| 3369 | 1 | Compassion toward | `(LLM tail)` | Septon Meribald → The orphan children | affc-brienne-07 |
| 3370 | 1 | Suspicion/hostility toward | `(LLM tail)` | Gendry → Brienne's party (initially) | affc-brienne-07 |
| 3371 | 1 | Worship of | `(LLM tail)` | Gendry → The Lord of Light (R'hllor) | affc-brienne-07 |
| 3372 | 1 | Partnership/conflict with | `(LLM tail)` | Willow → Gendry | affc-brienne-07 |
| 3373 | 1 | Recognition of kinship between | `(LLM tail)` | Brienne → Gendry and Renly / Robert Baratheon | affc-brienne-07 |
| 3374 | 1 | Mentored by (memory) | `TUTORS` | Brienne → Ser Goodwin | affc-brienne-07 |
| 3375 | 1 | Violent aggression toward | `(LLM tail)` | The man in the Hound's helm → Willow / Brienne | affc-brienne-07 |
| 3376 | 1 | Savage attack on | `(LLM tail)` | Biter → Brienne | affc-brienne-07 |
| 3377 | 1 | Sworn service to (past) | `(LLM tail)` | Brienne → Catelyn Stark | affc-brienne-08 |
| 3378 | 1 | Defends / trusts | `PROTECTS` | Brienne → Jaime Lannister | affc-brienne-08 |
| 3379 | 1 | Loves (romantic) | `LOVES` | Brienne → Renly Baratheon | affc-brienne-08 |
| 3380 | 1 | Quest for | `(LLM tail)` | Brienne → Sansa Stark | affc-brienne-08 |
| 3381 | 1 | Demands death of | `(LLM tail)` | Lady Stoneheart → Jaime Lannister | affc-brienne-08 |
| 3382 | 1 | Serves (reluctantly) | `SERVES` | Thoros → Lady Stoneheart | affc-brienne-08 |
| 3383 | 1 | Gave life to resurrect | `GIFTED_TO` | Lord Beric Dondarrion → Lady Stoneheart | affc-brienne-08 |
| 3384 | 1 | Wears identity of | `(LLM tail)` | Lem → Sandor Clegane (The Hound) | affc-brienne-08 |
| 3385 | 1 | Took helm from corpse of | `(LLM tail)` | Lem → Rorge | affc-brienne-08 |
| 3386 | 1 | Healed | `(LLM tail)` | Jeyne Heddle → Brienne | affc-brienne-08 |
| 3387 | 1 | Fellow captive with | `(LLM tail)` | Hyle Hunt → Brienne | affc-brienne-08 |
| 3388 | 1 | Killed (stated) | `KILLS` | Brienne → Dog (Meribald's dog) | affc-brienne-08 |
| 3389 | 1 | Has hanged | `(LLM tail)` | Randyll Tarly → Brotherhood members | affc-brienne-08 |
| 3390 | 1 | Has wife and daughter (lost) | `(LLM tail)` | Lem → — | affc-brienne-08 |
| 3391 | 1 | Was betrothed to (past) | `BETROTHED_TO` | Brienne → Unnamed knight with griffin cloak | affc-brienne-08 |
| 3392 | 1 | Arranged marriage for | `(LLM tail)` | Brienne's father → Brienne | affc-brienne-08 |
| 3393 | 1 | Begged for resurrection of | `(LLM tail)` | Harwin → Catelyn | affc-brienne-08 |
| 3394 | 1 | Employer-employee | `(LLM tail)` | Cat/Arya → Brusco | affc-cat-of-the-canals-01 |
| 3395 | 1 | Roommates / quasi-siblings | `(LLM tail)` | Cat/Arya → Talea, Brea | affc-cat-of-the-canals-01 |
| 3396 | 1 | Student-teacher (service) | `(LLM tail)` | Cat/Arya → The kindly man | affc-cat-of-the-canals-01 |
| 3397 | 1 | Student-teacher (poisons) | `(LLM tail)` | Cat/Arya → The waif | affc-cat-of-the-canals-01 |
| 3398 | 1 | Wary mutual respect | `RESPECTS` | Cat/Arya → The waif | affc-cat-of-the-canals-01 |
| 3399 | 1 | Killer | `(LLM tail)` | Cat/Arya → Dareon | affc-cat-of-the-canals-01 |
| 3400 | 1 | Hostility / moral judgment | `(LLM tail)` | Cat/Arya → Dareon | affc-cat-of-the-canals-01 |
| 3401 | 1 | Sympathy | `(LLM tail)` | Cat/Arya → Little Narbo | affc-cat-of-the-canals-01 |
| 3402 | 1 | Complicated familiarity | `(LLM tail)` | Cat/Arya → The Sailor's Wife | affc-cat-of-the-canals-01 |
| 3403 | 1 | Suppressed kinship | `(LLM tail)` | Cat/Arya → Lysa Arryn | affc-cat-of-the-canals-01 |
| 3404 | 1 | Wolf-dreaming bond | `(LLM tail)` | Cat/Arya → Nymeria (implied) | affc-cat-of-the-canals-01 |
| 3405 | 1 | Grief / nightmare | `MOURNS` | Cat/Arya → Catelyn Stark (mother, unnamed) | affc-cat-of-the-canals-01 |
| 3406 | 1 | Companion (abandoned) | `COMPANION_OF` | Dareon → Sam | affc-cat-of-the-canals-01 |
| 3407 | 1 | Former partner | `(LLM tail)` | Tagganaro → Little Narbo | affc-cat-of-the-canals-01 |
| 3408 | 1 | Devotion to lost husband | `(LLM tail)` | The Sailor's Wife → Her first husband | affc-cat-of-the-canals-01 |
| 3409 | 1 | Employer | `(LLM tail)` | Merry → Lanna, Yna, Blushing Bethany, Sailor's Wife, Assadora | affc-cat-of-the-canals-01 |
| 3410 | 1 | Victim | `(LLM tail)` | The waif → Her stepmother | affc-cat-of-the-canals-01 |
| 3411 | 1 | Devoted | `(LLM tail)` | The waif → Her father | affc-cat-of-the-canals-01 |
| 3412 | 1 | Conflict | `(LLM tail)` | Quence → Allaquo | affc-cat-of-the-canals-01 |
| 3413 | 1 | Daughter of (grieving, complex) | `PARENT_OF` | Cersei → Tywin | affc-cersei-01 |
| 3414 | 1 | Twin sister / political tension | `SIBLING_OF` | Cersei → Jaime | affc-cersei-01 |
| 3415 | 1 | Hatred / fear | `HATES` | Cersei → Tyrion | affc-cersei-01 |
| 3416 | 1 | Mother / protective | `(LLM tail)` | Cersei → Tommen | affc-cersei-01 |
| 3417 | 1 | Mistrust / suspicion | `DISTRUSTS` | Cersei → Varys | affc-cersei-01 |
| 3418 | 1 | Early trust / patronage | `(LLM tail)` | Cersei → Qyburn | affc-cersei-01 |
| 3419 | 1 | Brother / strained | `SIBLING_OF` | Jaime → Cersei | affc-cersei-01 |
| 3420 | 1 | Uncle / mediator | `UNCLE_OF` | Kevan → Cersei, Jaime | affc-cersei-01 |
| 3421 | 1 | Service / opportunism | `(LLM tail)` | Qyburn → Cersei | affc-cersei-01 |
| 3422 | 1 | Informant | `(LLM tail)` | Shortear → Cersei | affc-cersei-01 |
| 3423 | 1 | Contempt / resentment (retroactive) | `HATES` | Cersei → Robert Baratheon | affc-cersei-01 |
| 3424 | 1 | Employed (sexual, denied by Cersei) | `(LLM tail)` | Tywin → Shae | affc-cersei-01 |
| 3425 | 1 | Twin sister of / estranged from | `SIBLING_OF` | Cersei → Jaime | affc-cersei-02 |
| 3426 | 1 | Daughter of (grieving) | `PARENT_OF` | Cersei → Tywin (deceased) | affc-cersei-02 |
| 3427 | 1 | Niece of / in conflict with | `UNCLE_OF` | Cersei → Kevan | affc-cersei-02 |
| 3428 | 1 | Former lover of / worries about | `LOVER_OF` | Cersei → Lancel | affc-cersei-02 |
| 3429 | 1 | Rival of | `OPPOSES` | Cersei → Margaery | affc-cersei-02 |
| 3430 | 1 | Politically opposed to | `(LLM tail)` | Cersei → Mace Tyrell | affc-cersei-02 |
| 3431 | 1 | Cultivating | `(LLM tail)` | Cersei → Taena Merryweather | affc-cersei-02 |
| 3432 | 1 | Employing / cautiously trusting | `(LLM tail)` | Cersei → Qyburn | affc-cersei-02 |
| 3433 | 1 | Cousin of / former lover of | `COUSIN_OF` | Lancel → Cersei | affc-cersei-02 |
| 3434 | 1 | Vigil for | `(LLM tail)` | Jaime → Tywin (deceased) | affc-cersei-02 |
| 3435 | 1 | Intimidated | `(LLM tail)` | Tywin (memory) → Lord Rykker | affc-cersei-02 |
| 3436 | 1 | mother, protector (possessive, fearful) | `FEARS` | Cersei → Tommen | affc-cersei-03 |
| 3437 | 1 | alienated from / contemptuous of | `(LLM tail)` | Cersei → Jaime | affc-cersei-03 |
| 3438 | 1 | dutiful but dismissed by | `(LLM tail)` | Jaime → Cersei | affc-cersei-03 |
| 3439 | 1 | hostile toward / distrusts | `OPPOSES` | Cersei → Mace Tyrell | affc-cersei-03 |
| 3440 | 1 | suspicious of / betrayed by (believed) | `(LLM tail)` | Cersei → Senelle | affc-cersei-03 |
| 3441 | 1 | cautious trust toward | `(LLM tail)` | Cersei → Lady Merryweather | affc-cersei-03 |
| 3442 | 1 | bitter estrangement from | `RESENTS` | Cersei → Kevan Lannister | affc-cersei-03 |
| 3443 | 1 | critical of / disappointed in | `(LLM tail)` | Kevan → Cersei | affc-cersei-03 |
| 3444 | 1 | performs affection toward | `LOVES` | Margaery → Cersei | affc-cersei-03 |
| 3445 | 1 | tender toward / protective of | `(LLM tail)` | Margaery → Tommen | affc-cersei-03 |
| 3446 | 1 | obedient and affectionate toward | `LOVES` | Tommen → Cersei | affc-cersei-03 |
| 3447 | 1 | fascinated by / trusting of | `(LLM tail)` | Tommen → Margaery | affc-cersei-03 |
| 3448 | 1 | very close to (resembles) | `(LLM tail)` | Loras Tyrell → Margaery Tyrell | affc-cersei-03 |
| 3449 | 1 | notices / attracted to | `(LLM tail)` | Cersei → Aurane Waters | affc-cersei-03 |
| 3450 | 1 | unexplained conversation with | `(LLM tail)` | Kevan → Ser Garlan Tyrell | affc-cersei-03 |
| 3451 | 1 | socializing with | `(LLM tail)` | Elinor → Aurane Waters | affc-cersei-03 |
| 3452 | 1 | dancing with | `(LLM tail)` | Megga → Ser Tallad the Tall | affc-cersei-03 |
| 3453 | 1 | serving as intermediaries for | `(LLM tail)` | Alla, Elinor, Megga → Margaery | affc-cersei-03 |
| 3454 | 1 | slides arm through / keeps company with | `(LLM tail)` | Cersei → Ser Osmund Kettleblack | affc-cersei-03 |
| 3455 | 1 | nostalgic bitterness toward (memory) | `(LLM tail)` | Cersei → Robert Baratheon | affc-cersei-03 |
| 3456 | 1 | testified against | `(LLM tail)` | Lady Merryweather → Tyrion Lannister | affc-cersei-03 |
| 3457 | 1 | uses/controls | `(LLM tail)` | Cersei → Qyburn | affc-cersei-04 |
| 3458 | 1 | uses as hostage | `(LLM tail)` | Cersei → Ser Harys Swyft | affc-cersei-04 |
| 3459 | 1 | sexual manipulation of | `(LLM tail)` | Cersei → Ser Osney Kettleblack | affc-cersei-04 |
| 3460 | 1 | growing intimacy with | `(LLM tail)` | Cersei → Taena Merryweather | affc-cersei-04 |
| 3461 | 1 | rivalry/comparison with | `(LLM tail)` | Cersei → Jaime Lannister | affc-cersei-04 |
| 3462 | 1 | attraction/assessment of | `(LLM tail)` | Cersei → Aurane Waters | affc-cersei-04 |
| 3463 | 1 | amusement toward | `(LLM tail)` | Cersei → Lord Gyles Rosby | affc-cersei-04 |
| 3464 | 1 | daughter married to | `(LLM tail)` | Ser Harys Swyft → Kevan Lannister | affc-cersei-04 |
| 3465 | 1 | teases | `(LLM tail)` | Megga (Tyrell cousin) → Ser Osney Kettleblack | affc-cersei-04 |
| 3466 | 1 | kind to | `(LLM tail)` | Margaery Tyrell → Ser Osney Kettleblack | affc-cersei-04 |
| 3467 | 1 | past lover of | `LOVER_OF` | Taena Merryweather → Unnamed Myrish sea captain | affc-cersei-04 |
| 3468 | 1 | hit | `(LLM tail)` | Robert Baratheon → Cersei | affc-cersei-04 |
| 3469 | 1 | lies to | `(LLM tail)` | Cersei → Taena Merryweather | affc-cersei-04 |
| 3470 | 1 | Mother, controlling | `(LLM tail)` | Cersei → Tommen | affc-cersei-05 |
| 3471 | 1 | Son, increasingly defiant | `(LLM tail)` | Tommen → Cersei | affc-cersei-05 |
| 3472 | 1 | Influences/manipulates | `(LLM tail)` | Margaery → Tommen | affc-cersei-05 |
| 3473 | 1 | Antagonist/rival | `(LLM tail)` | Cersei → Margaery | affc-cersei-05 |
| 3474 | 1 | Uses/commands | `COMMANDS` | Cersei → Osmund Kettleblack | affc-cersei-05 |
| 3475 | 1 | Fails to seduce | `(LLM tail)` | Osney Kettleblack → Margaery | affc-cersei-05 |
| 3476 | 1 | Flirtatious but guarded with | `(LLM tail)` | Margaery → Osney Kettleblack | affc-cersei-05 |
| 3477 | 1 | Considers a fool | `(LLM tail)` | Cersei → Osmund Kettleblack | affc-cersei-05 |
| 3478 | 1 | Loyal to / protective of | `SERVES` | Loras → Tommen | affc-cersei-05 |
| 3479 | 1 | Enabling/using | `(LLM tail)` | Cersei → Qyburn | affc-cersei-05 |
| 3480 | 1 | Serves/informs | `SERVES` | Qyburn → Cersei | affc-cersei-05 |
| 3481 | 1 | Increasingly hostile toward | `(LLM tail)` | Cersei → Jaime | affc-cersei-05 |
| 3482 | 1 | Still attracted to | `(LLM tail)` | Jaime → Cersei | affc-cersei-05 |
| 3483 | 1 | Uses attraction against | `(LLM tail)` | Cersei → Jaime | affc-cersei-05 |
| 3484 | 1 | Enjoys friendship with | `COMPANION_OF` | Cersei → Taena Merryweather | affc-cersei-05 |
| 3485 | 1 | Nostalgic longing for | `(LLM tail)` | Cersei → Rhaegar Targaryen | affc-cersei-05 |
| 3486 | 1 | Aunt, confidante (memory) | `UNCLE_OF` | Lady Genna → Cersei | affc-cersei-05 |
| 3487 | 1 | Father, promised | `(LLM tail)` | Tywin → Cersei | affc-cersei-05 |
| 3488 | 1 | Considers expendable | `(LLM tail)` | Cersei → Senelle | affc-cersei-05 |
| 3489 | 1 | Uses as spy and confidante | `(LLM tail)` | Cersei → Taena Merryweather | affc-cersei-06 |
| 3490 | 1 | Hostile rivalry (one-sided overt) | `(LLM tail)` | Cersei → Margaery Tyrell | affc-cersei-06 |
| 3491 | 1 | Political negotiation / mutual wariness | `(LLM tail)` | Cersei → The High Septon | affc-cersei-06 |
| 3492 | 1 | Grief and guilt over | `MOURNS` | Cersei → Joffrey Baratheon | affc-cersei-06 |
| 3493 | 1 | Emulates / admires | `RESPECTS` | Cersei → Tywin Lannister | affc-cersei-06 |
| 3494 | 1 | Protective / controlling toward | `(LLM tail)` | Cersei → Tommen Baratheon | affc-cersei-06 |
| 3495 | 1 | Fear and memory of | `FEARS` | Cersei → Maggy the Frog (implied) | affc-cersei-06 |
| 3496 | 1 | Sisterly devotion (presented) | `(LLM tail)` | Margaery → Ser Loras Tyrell | affc-cersei-06 |
| 3497 | 1 | Suspicion about | `(LLM tail)` | Cersei → Loras and Margaery | affc-cersei-06 |
| 3498 | 1 | Disciplinary authority over | `(LLM tail)` | High Septon → Septon Torbert | affc-cersei-06 |
| 3499 | 1 | Flatters and defers to | `(LLM tail)` | Taena Merryweather → Cersei | affc-cersei-06 |
| 3500 | 1 | Cultivates goodwill with | `(LLM tail)` | Margaery → Smallfolk | affc-cersei-06 |
| 3501 | 1 | Blames for Joffrey's death | `OPPOSES` | Cersei → House Tyrell | affc-cersei-06 |
| 3502 | 1 | Rivalry/contempt toward | `(LLM tail)` | Cersei → Margaery | affc-cersei-07 |
| 3503 | 1 | Calculating manipulation of | `(LLM tail)` | Cersei → Loras Tyrell | affc-cersei-07 |
| 3504 | 1 | Reliance on/trust in | `(LLM tail)` | Cersei → Qyburn | affc-cersei-07 |
| 3505 | 1 | Mild approval of | `(LLM tail)` | Cersei → Aurane Waters | affc-cersei-07 |
| 3506 | 1 | Intimate companion | `COMPANION_OF` | Cersei → Taena Merryweather | affc-cersei-07 |
| 3507 | 1 | Fury/contempt toward | `(LLM tail)` | Cersei → Falyse Stokeworth | affc-cersei-07 |
| 3508 | 1 | Hatred/bitter memory of | `HATES` | Cersei → Robert Baratheon | affc-cersei-07 |
| 3509 | 1 | Longing/fixation on | `(LLM tail)` | Cersei → Jaime Lannister | affc-cersei-07 |
| 3510 | 1 | Nostalgic desire for | `(LLM tail)` | Cersei → Rhaegar Targaryen | affc-cersei-07 |
| 3511 | 1 | Determination to destroy | `(LLM tail)` | Cersei → Bronn | affc-cersei-07 |
| 3512 | 1 | Contempt/suspicion toward | `HATES` | Cersei → Willas Tyrell | affc-cersei-07 |
| 3513 | 1 | Dominates/threatens | `(LLM tail)` | Bronn → Falyse | affc-cersei-07 |
| 3514 | 1 | Uses/manipulates | `(LLM tail)` | Cersei → Aurane Waters | affc-cersei-08 |
| 3515 | 1 | Concealed hostility toward | `(LLM tail)` | Cersei → Margaery Tyrell | affc-cersei-08 |
| 3516 | 1 | Mother of (controlling) | `PARENT_OF` | Cersei → Tommen | affc-cersei-08 |
| 3517 | 1 | Loyal to/loves | `SERVES` | Tommen → Margaery | affc-cersei-08 |
| 3518 | 1 | Serves/enables | `SERVES` | Qyburn → Cersei | affc-cersei-08 |
| 3519 | 1 | Haunted by | `(LLM tail)` | Cersei → Maggy the Frog | affc-cersei-08 |
| 3520 | 1 | Fixated on destroying | `(LLM tail)` | Cersei → Tyrion Lannister | affc-cersei-08 |
| 3521 | 1 | Displeasure toward | `(LLM tail)` | Cersei → Lancel Lannister | affc-cersei-08 |
| 3522 | 1 | Expected to wed | `(LLM tail)` | Young Cersei → Rhaegar Targaryen | affc-cersei-08 |
| 3523 | 1 | Wanted to marry | `(LLM tail)` | Melara Hetherspoon → Jaime Lannister | affc-cersei-08 |
| 3524 | 1 | Indifferent to fate of | `(LLM tail)` | Cersei → Falyse Stokeworth | affc-cersei-08 |
| 3525 | 1 | dominates/intimidates | `(LLM tail)` | Cersei → Pycelle | affc-cersei-09 |
| 3526 | 1 | manipulates/appoints | `MANIPULATES` | Cersei → Orton Merryweather | affc-cersei-09 |
| 3527 | 1 | plots to destroy | `(LLM tail)` | Cersei → Margaery Tyrell | affc-cersei-09 |
| 3528 | 1 | frames and brutalizes | `(LLM tail)` | Cersei → Blue Bard (Wat) | affc-cersei-09 |
| 3529 | 1 | sexual manipulation | `(LLM tail)` | Cersei → Osney Kettleblack | affc-cersei-09 |
| 3530 | 1 | invokes/measures self against | `(LLM tail)` | Cersei → Tywin Lannister | affc-cersei-09 |
| 3531 | 1 | serves as torturer | `SERVES` | Qyburn → Cersei | affc-cersei-09 |
| 3532 | 1 | serves both queens | `SERVES` | Pycelle → Cersei/Margaery | affc-cersei-09 |
| 3533 | 1 | invokes past loyalty to | `(LLM tail)` | Pycelle → Tywin Lannister | affc-cersei-09 |
| 3534 | 1 | volunteers to manipulate | `(LLM tail)` | Taena → Alla Tyrell | affc-cersei-09 |
| 3535 | 1 | considers granting lands to | `(LLM tail)` | Cersei → Aurane Waters | affc-cersei-09 |
| 3536 | 1 | performed for | `(LLM tail)` | Blue Bard → Margaery | affc-cersei-09 |
| 3537 | 1 | Ordered murder of | `KILLS` | Cersei → Previous High Septon | affc-cersei-10 |
| 3538 | 1 | Desperate need for | `(LLM tail)` | Cersei → Jaime Lannister | affc-cersei-10 |
| 3539 | 1 | Fears prophecy of | `FEARS` | Cersei → Maggy the Frog | affc-cersei-10 |
| 3540 | 1 | Tortures | `TORTURES` | The High Septon → Osney Kettleblack | affc-cersei-10 |
| 3541 | 1 | Take control from | `(LLM tail)` | Harys Swyft and Pycelle → Cersei | affc-cersei-10 |
| 3542 | 1 | Opposes (implied) | `OPPOSES` | Mace Tyrell → Cersei | affc-cersei-10 |
| 3543 | 1 | freed from cell (and bears guilt for consequences) | `(LLM tail)` | Jaime → Tyrion | affc-jaime-01 |
| 3544 | 1 | stands vigil for / feels no grief toward | `MOURNS` | Jaime → Lord Tywin | affc-jaime-01 |
| 3545 | 1 | forced cooperation / threatened | `(LLM tail)` | Jaime → Varys | affc-jaime-01 |
| 3546 | 1 | accused Cersei to | `(LLM tail)` | Tyrion → Jaime | affc-jaime-01 |
| 3547 | 1 | asked to serve as Hand / refused by | `(LLM tail)` | Cersei → Jaime | affc-jaime-01 |
| 3548 | 1 | ordered killing of turnkeys through | `(LLM tail)` | Cersei → Kettleblacks (Osmund, Osney, Osfryd) | affc-jaime-01 |
| 3549 | 1 | blamed for dungeon failures | `(LLM tail)` | Cersei → Ser Ilyn Payne | affc-jaime-01 |
| 3550 | 1 | accused of sleeping with | `(LLM tail)` | Cersei → Lancel, Osmund Kettleblack, Moon Boy | affc-jaime-01 |
| 3551 | 1 | refused to serve / knows incest secret | `(LLM tail)` | Kevan → Cersei, Jaime | affc-jaime-01 |
| 3552 | 1 | political advisor to | `(LLM tail)` | Jaime → Cersei | affc-jaime-01 |
| 3553 | 1 | compared to father by | `(LLM tail)` | Jaime → Cersei | affc-jaime-01 |
| 3554 | 1 | father figure / protective toward | `(LLM tail)` | Jaime → Tommen | affc-jaime-01 |
| 3555 | 1 | intimidated/harmed by (implied) | `(LLM tail)` | Tommen → Joffrey | affc-jaime-01 |
| 3556 | 1 | harsh mother to | `(LLM tail)` | Cersei → Tommen | affc-jaime-01 |
| 3557 | 1 | thinks of with tenderness / almost prays for | `(LLM tail)` | Jaime → Brienne of Tarth | affc-jaime-01 |
| 3558 | 1 | devoted to / mourns | `MOURNS` | Pycelle → Lord Tywin | affc-jaime-01 |
| 3559 | 1 | contempt for / views as dying | `HATES` | Jaime → Pycelle | affc-jaime-01 |
| 3560 | 1 | admiration for potential of | `RESPECTS` | Jaime → Loras Tyrell | affc-jaime-01 |
| 3561 | 1 | recalled mentorship by | `TUTORS` | Jaime → Ser Arthur Dayne | affc-jaime-01 |
| 3562 | 1 | confided in / trusted | `(LLM tail)` | Rhaegar → Jaime | affc-jaime-01 |
| 3563 | 1 | kept close out of fear of Tywin | `FEARS` | Aerys → Jaime | affc-jaime-01 |
| 3564 | 1 | revulsion toward / visualizes infidelity | `(LLM tail)` | Jaime → Osmund Kettleblack | affc-jaime-01 |
| 3565 | 1 | commands / rebukes | `COMMANDS` | Jaime → Boros Blount, Osmund Kettleblack | affc-jaime-01 |
| 3566 | 1 | political pawn (in Jaime's strategy) | `(LLM tail)` | Mace Tyrell → Cersei | affc-jaime-01 |
| 3567 | 1 | clever and pretty (Jaime's assessment) | `(LLM tail)` | Margaery → Tommen | affc-jaime-01 |
| 3568 | 1 | proud of lineage / boastful | `(LLM tail)` | Longwaters → Jaime | affc-jaime-01 |
| 3569 | 1 | disappeared (implied to be Varys) | `(LLM tail)` | Rugen → Varys | affc-jaime-01 |
| 3570 | 1 | Son of (mourning) | `PARENT_OF` | Jaime → Tywin Lannister | affc-jaime-02 |
| 3571 | 1 | Twin sibling of (estranged) | `(LLM tail)` | Jaime → Cersei Lannister | affc-jaime-02 |
| 3572 | 1 | Nephew of (attempting reconciliation) | `NEPHEW_OF` | Jaime → Ser Kevan Lannister | affc-jaime-02 |
| 3573 | 1 | Cousin of (suspicious of) | `COUSIN_OF` | Jaime → Lancel Lannister | affc-jaime-02 |
| 3574 | 1 | Former lover of (rejected by) | `LOVER_OF` | Jaime → Cersei Lannister | affc-jaime-02 |
| 3575 | 1 | Superior officer of | `(LLM tail)` | Jaime → Ser Loras Tyrell | affc-jaime-02 |
| 3576 | 1 | Respects the skill of | `RESPECTS` | Jaime → Ser Loras Tyrell | affc-jaime-02 |
| 3577 | 1 | Refuses to serve | `(LLM tail)` | Ser Kevan → Cersei Lannister | affc-jaime-02 |
| 3578 | 1 | Knows secret of | `(LLM tail)` | Ser Kevan → Jaime and Cersei | affc-jaime-02 |
| 3579 | 1 | Paranoid toward / politically isolated from | `(LLM tail)` | Cersei → Ser Kevan Lannister | affc-jaime-02 |
| 3580 | 1 | Uses as double agent | `(LLM tail)` | Cersei → Lady Taena Merryweather | affc-jaime-02 |
| 3581 | 1 | Enraged at | `(LLM tail)` | Cersei → Bronn | affc-jaime-02 |
| 3582 | 1 | Drinking heavily, compared to | `(LLM tail)` | Cersei → Robert Baratheon | affc-jaime-02 |
| 3583 | 1 | Compared to (by Jaime) | `(LLM tail)` | Cersei → Aerys II Targaryen | affc-jaime-02 |
| 3584 | 1 | Stood guard with | `(LLM tail)` | Jaime → Jon Darry | affc-jaime-02 |
| 3585 | 1 | Mother of (governs in name of) | `PARENT_OF` | Cersei → Tommen Baratheon | affc-jaime-02 |
| 3586 | 1 | Under influence of | `(LLM tail)` | Lancel → Unnamed septons | affc-jaime-02 |
| 3587 | 1 | Lord of / served by | `(LLM tail)` | Tywin Lannister → Lords of the west | affc-jaime-02 |
| 3588 | 1 | Secret sparring partner / developing bond | `(LLM tail)` | Jaime → Ser Ilyn Payne | affc-jaime-03 |
| 3589 | 1 | Boyhood friends | `(LLM tail)` | Jaime → Ser Addam Marbrand | affc-jaime-03 |
| 3590 | 1 | Protects / defends honor of | `PROTECTS` | Jaime → Brienne | affc-jaime-03 |
| 3591 | 1 | Distrusts / opposes | `DISTRUSTS` | Cersei → Loras Tyrell | affc-jaime-03 |
| 3592 | 1 | Warns Cersei about | `ADVISES` | Jaime → Qyburn | affc-jaime-03 |
| 3593 | 1 | Lost tongue on orders of | `(LLM tail)` | Ser Ilyn Payne → Aerys II Targaryen | affc-jaime-03 |
| 3594 | 1 | Former betrothed / despises | `BETROTHED_TO` | Red Ronnet → Brienne | affc-jaime-03 |
| 3595 | 1 | Devout follower | `(LLM tail)` | Ser Bonifer Hasty → Faith of the Seven | affc-jaime-03 |
| 3596 | 1 | Tortured / killed | `(LLM tail)` | Gregor Clegane → Vargo Hoat | affc-jaime-03 |
| 3597 | 1 | Castellan appointed by Jaime at | `(LLM tail)` | Ser Bonifer Hasty → Harrenhal | affc-jaime-03 |
| 3598 | 1 | Jests about kinship with | `(LLM tail)` | Strongboar (Ser Lyle) → Ser Roger Hogg | affc-jaime-03 |
| 3599 | 1 | Likely recommended | `(LLM tail)` | Orton Merryweather → Ser Bonifer Hasty | affc-jaime-03 |
| 3600 | 1 | Cousin / blood relative | `COUSIN_OF` | Jaime → Lancel | affc-jaime-04 |
| 3601 | 1 | Nephew (via brother Kevan) | `NEPHEW_OF` | Jaime → Lancel | affc-jaime-04 |
| 3602 | 1 | Uncle-nephew (Kevan is uncle) | `NEPHEW_OF` | Jaime → Ser Kevan | affc-jaime-04 |
| 3603 | 1 | Husband (unconsummated) | `(LLM tail)` | Lancel → Lady Amerei | affc-jaime-04 |
| 3604 | 1 | Daughter | `(LLM tail)` | Lady Amerei → Lady Mariya | affc-jaime-04 |
| 3605 | 1 | Confessed sins to | `(LLM tail)` | Lancel → The (dead) High Septon | affc-jaime-04 |
| 3606 | 1 | Complicity in death of | `(LLM tail)` | Lancel → Robert Baratheon | affc-jaime-04 |
| 3607 | 1 | Quarreled with | `(LLM tail)` | Lancel → Ser Kevan | affc-jaime-04 |
| 3608 | 1 | Increasingly disillusioned with | `(LLM tail)` | Jaime → Cersei | affc-jaime-04 |
| 3609 | 1 | Uses as confessor/sparring partner | `(LLM tail)` | Jaime → Ser Ilyn Payne | affc-jaime-04 |
| 3610 | 1 | Boastful rivalry / volunteering | `(LLM tail)` | Strongboar → The Hound / Lord Beric | affc-jaime-04 |
| 3611 | 1 | Memory/affection for | `LOVES` | Jaime → Tyrion | affc-jaime-04 |
| 3612 | 1 | Contempt mixed with pity for | `HATES` | Jaime → Lancel | affc-jaime-04 |
| 3613 | 1 | Witness/informant | `(LLM tail)` | Ser Arwood Frey → The company | affc-jaime-04 |
| 3614 | 1 | Former squire together with | `(LLM tail)` | Jaime → Merrett Frey | affc-jaime-04 |
| 3615 | 1 | Cousin, easy camaraderie | `COUSIN_OF` | Jaime → Ser Daven | affc-jaime-05 |
| 3616 | 1 | Nightly sparring partner | `(LLM tail)` | Jaime → Ser Ilyn Payne | affc-jaime-05 |
| 3617 | 1 | Nephew | `NEPHEW_OF` | Jaime → Genna Lannister | affc-jaime-05 |
| 3618 | 1 | Dominates/dismisses | `(LLM tail)` | Genna → Emmon Frey | affc-jaime-05 |
| 3619 | 1 | Loves/mourns | `LOVES` | Genna → Tywin Lannister | affc-jaime-05 |
| 3620 | 1 | Higher regard for | `(LLM tail)` | Genna → Tyrion Lannister | affc-jaime-05 |
| 3621 | 1 | Resentment/frustration | `RESENTS` | Ser Daven → Frey family | affc-jaime-05 |
| 3622 | 1 | Deference | `(LLM tail)` | Ser Daven → Kevan Lannister | affc-jaime-05 |
| 3623 | 1 | Growing distrust/disgust | `(LLM tail)` | Jaime → Cersei | affc-jaime-05 |
| 3624 | 1 | Conflicted obligation | `(LLM tail)` | Jaime → Catelyn Stark | affc-jaime-05 |
| 3625 | 1 | Pity | `(LLM tail)` | Jaime → Edmure Tully | affc-jaime-05 |
| 3626 | 1 | Vowed vengeance against | `(LLM tail)` | Daven → Karstark's killer | affc-jaime-05 |
| 3627 | 1 | Loved but complex | `LOVES` | Genna → Tywin | affc-jaime-05 |
| 3628 | 1 | Reluctant admiration | `RESPECTS` | Ser Daven → Blackfish | affc-jaime-05 |
| 3629 | 1 | Worried about | `(LLM tail)` | Genna → Jaime | affc-jaime-05 |
| 3630 | 1 | parleying adversary / grudging respect | `RESPECTS` | Jaime Lannister → Ser Brynden Tully | affc-jaime-06 |
| 3631 | 1 | cousin, military collaborator | `COUSIN_OF` | Jaime Lannister → Ser Daven Lannister | affc-jaime-06 |
| 3632 | 1 | commander over | `COMMANDS` | Jaime Lannister → Little Lew, Peck | affc-jaime-06 |
| 3633 | 1 | uncle-nephew by marriage, authority over | `NEPHEW_OF` | Jaime Lannister → Lord Emmon Frey | affc-jaime-06 |
| 3634 | 1 | nephew, respect for | `NEPHEW_OF` | Jaime Lannister → Lady Genna Lannister | affc-jaime-06 |
| 3635 | 1 | commander, contempt for | `COMMANDS` | Jaime Lannister → Ser Ryman Frey | affc-jaime-06 |
| 3636 | 1 | wariness toward | `(LLM tail)` | Jaime Lannister → Walder Rivers | affc-jaime-06 |
| 3637 | 1 | captor threatening | `CAPTURES` | Jaime Lannister → Edmure Tully | affc-jaime-06 |
| 3638 | 1 | uncle, protective of | `UNCLE_OF` | Ser Brynden Tully → Edmure Tully | affc-jaime-06 |
| 3639 | 1 | father desperate for | `(LLM tail)` | Lord Piper → Marq Piper | affc-jaime-06 |
| 3640 | 1 | contempt for father | `HATES` | Edwyn Frey → Ser Ryman Frey | affc-jaime-06 |
| 3641 | 1 | hostage-holder, threatening | `(LLM tail)` | Edwyn Frey → Lord Piper / Marq Piper | affc-jaime-06 |
| 3642 | 1 | husband, affection for | `LOVES` | Edmure Tully → Roslin Frey | affc-jaime-06 |
| 3643 | 1 | subservient husband | `(LLM tail)` | Lord Emmon Frey → Lady Genna Lannister | affc-jaime-06 |
| 3644 | 1 | complicated guilt toward | `(LLM tail)` | Jaime Lannister → Catelyn Stark | affc-jaime-06 |
| 3645 | 1 | comparing self to | `(LLM tail)` | Jaime Lannister → Tywin Lannister | affc-jaime-06 |
| 3646 | 1 | commands/manages | `COMMANDS` | Jaime → Emmon Frey | affc-jaime-07 |
| 3647 | 1 | dominates/manages | `(LLM tail)` | Genna Lannister → Emmon Frey | affc-jaime-07 |
| 3648 | 1 | interrogates/threatens | `(LLM tail)` | Jaime → Edmure Tully | affc-jaime-07 |
| 3649 | 1 | uncle/nephew loyalty | `NEPHEW_OF` | Edmure Tully → Brynden Tully | affc-jaime-07 |
| 3650 | 1 | aunt/nephew respect | `NEPHEW_OF` | Jaime → Genna Lannister | affc-jaime-07 |
| 3651 | 1 | loved/mourns | `MOURNS` | Jeyne Westerling → Robb Stark | affc-jaime-07 |
| 3652 | 1 | controls/overrides | `COMMANDS` | Lady Sybell → Jeyne Westerling | affc-jaime-07 |
| 3653 | 1 | protects/defends | `PROTECTS` | Jaime → Joy | affc-jaime-07 |
| 3654 | 1 | sparring partner/confidant | `(LLM tail)` | Jaime → Ser Ilyn Payne | affc-jaime-07 |
| 3655 | 1 | distancing from | `(LLM tail)` | Jaime → Cersei | affc-jaime-07 |
| 3656 | 1 | fatherly concern for | `(LLM tail)` | Jaime → Tommen | affc-jaime-07 |
| 3657 | 1 | ingratiates with | `(LLM tail)` | Tom of Sevenstreams → Jaime | affc-jaime-07 |
| 3658 | 1 | mother to | `(LLM tail)` | Dream woman (Joanna) → Jaime | affc-jaime-07 |
| 3659 | 1 | eager to fight | `(LLM tail)` | Strongboar → The Hound / Beric Dondarrion | affc-jaime-07 |
| 3660 | 1 | Serves (resentfully) | `SERVES` | Pate → Archmaester Walgrave | affc-prologue |
| 3661 | 1 | Resents/fears | `RESENTS` | Pate → Leo Tyrell | affc-prologue |
| 3662 | 1 | Controlled disdain toward | `HATES` | Alleras → Leo Tyrell | affc-prologue |
| 3663 | 1 | Calm authority among | `(LLM tail)` | Alleras → The group | affc-prologue |
| 3664 | 1 | Respects/fears (implied) | `RESPECTS` | Leo Tyrell → Archmaester Marwyn | affc-prologue |
| 3665 | 1 | Skeptical of / disapproves of | `DISTRUSTS` | Armen → Archmaester Marwyn | affc-prologue |
| 3666 | 1 | Accused | `(LLM tail)` | Maester Gormon → Pate | affc-prologue |
| 3667 | 1 | Mother, controls access to | `(LLM tail)` | Emma → Rosey | affc-prologue |
| 3668 | 1 | Confused about identity of | `(LLM tail)` | Walgrave → Pate / Cressen | affc-prologue |
| 3669 | 1 | Serves / sworn to | `SERVES` | Sam → Jon Snow | affc-samwell-01 |
| 3670 | 1 | Romantic feelings toward | `(LLM tail)` | Sam → Gilly | affc-samwell-01 |
| 3671 | 1 | Cares for / assists | `(LLM tail)` | Sam → Maester Aemon | affc-samwell-01 |
| 3672 | 1 | Uneasy alliance with | `ALLIES_WITH` | Jon Snow → Stannis Baratheon | affc-samwell-01 |
| 3673 | 1 | Mourns (believes dead) | `MOURNS` | Jon Snow → Bran Stark | affc-samwell-01 |
| 3674 | 1 | Resents (mild) | `RESENTS` | Pyp → Jon Snow | affc-samwell-01 |
| 3675 | 1 | Feels distance from | `(LLM tail)` | Grenn → Jon Snow | affc-samwell-01 |
| 3676 | 1 | Keeps secret from | `(LLM tail)` | Sam → Jon Snow | affc-samwell-01 |
| 3677 | 1 | Threatens (indirectly) | `OPPOSES` | Melisandre → Maester Aemon | affc-samwell-01 |
| 3678 | 1 | Traumatized | `(LLM tail)` | Lord Randyll Tarly → Sam | affc-samwell-01 |
| 3679 | 1 | protects/guards | `PROTECTS` | Samwell Tarly → Gilly | affc-samwell-02 |
| 3680 | 1 | tries to comfort | `(LLM tail)` | Samwell Tarly → Gilly | affc-samwell-02 |
| 3681 | 1 | physically attracted to | `(LLM tail)` | Samwell Tarly → Gilly | affc-samwell-02 |
| 3682 | 1 | respects/serves | `RESPECTS` | Samwell Tarly → Jon Snow | affc-samwell-02 |
| 3683 | 1 | entertains | `(LLM tail)` | Dareon → Blackbird's oarsmen | affc-samwell-02 |
| 3684 | 1 | drinks heavily | `(LLM tail)` | Dareon → (firewine) | affc-samwell-02 |
| 3685 | 1 | traveled with | `(LLM tail)` | Maester Aemon → Brynden Rivers (Bloodraven) | affc-samwell-02 |
| 3686 | 1 | escorted by | `(LLM tail)` | Maester Aemon → Ser Duncan | affc-samwell-02 |
| 3687 | 1 | switched babies / forced | `(LLM tail)` | Jon Snow → Gilly | affc-samwell-02 |
| 3688 | 1 | abused/shamed | `(LLM tail)` | Randyll Tarly → Samwell Tarly | affc-samwell-02 |
| 3689 | 1 | comforted/loved | `LOVES` | Sam's mother → Samwell Tarly | affc-samwell-02 |
| 3690 | 1 | cares for / serves | `(LLM tail)` | Sam → Maester Aemon | affc-samwell-03 |
| 3691 | 1 | resents / blames | `RESENTS` | Sam → Dareon | affc-samwell-03 |
| 3692 | 1 | blames / questions | `OPPOSES` | Sam → Jon Snow | affc-samwell-03 |
| 3693 | 1 | abandons / betrays | `(LLM tail)` | Dareon → Night's Watch | affc-samwell-03 |
| 3694 | 1 | neglects | `(LLM tail)` | Dareon → Sam, Gilly, Aemon | affc-samwell-03 |
| 3695 | 1 | helps / warns | `ADVISES` | Cat → Sam | affc-samwell-03 |
| 3696 | 1 | threaten / mock | `(LLM tail)` | Terro & friend → Sam | affc-samwell-03 |
| 3697 | 1 | ordered/arranged | `(LLM tail)` | Jon Snow → Baby swap (inferred) | affc-samwell-03 |
| 3698 | 1 | "marries" | `(LLM tail)` | Dareon → The Sailor's Wife | affc-samwell-03 |
| 3699 | 1 | punches / fights | `(LLM tail)` | Sam → Dareon | affc-samwell-03 |
| 3700 | 1 | mourns / reveres | `MOURNS` | Sam → Maester Aemon | affc-samwell-04 |
| 3701 | 1 | guilt-ridden intimacy | `(LLM tail)` | Sam → Gilly | affc-samwell-04 |
| 3702 | 1 | loves / desires | `LOVES` | Gilly → Sam | affc-samwell-04 |
| 3703 | 1 | fears (past) | `FEARS` | Gilly → Craster | affc-samwell-04 |
| 3704 | 1 | advises / cares for | `ADVISES` | Kojja Mo → Sam | affc-samwell-04 |
| 3705 | 1 | working taskmaster / comic ally | `ALLIES_WITH` | Xhondo → Sam | affc-samwell-04 |
| 3706 | 1 | gave away sword to repay | `GIFTED_TO` | Sam → Xhondo | affc-samwell-04 |
| 3707 | 1 | believes in / advocates for | `(LLM tail)` | Aemon → Daenerys Targaryen | affc-samwell-04 |
| 3708 | 1 | brother, nostalgic love | `SIBLING_OF` | Aemon → Egg (Aegon V) | affc-samwell-04 |
| 3709 | 1 | niece, affection | `UNCLE_OF` | Aemon → Rhaelle Targaryen | affc-samwell-04 |
| 3710 | 1 | distrusts interpretation of | `DISTRUSTS` | Aemon → Lady Melisandre | affc-samwell-04 |
| 3711 | 1 | complicated resentment | `(LLM tail)` | Sam → Lord Randyll Tarly (his father) | affc-samwell-04 |
| 3712 | 1 | affection (recalled) | `LOVES` | Sam → His sisters | affc-samwell-04 |
| 3713 | 1 | self-comparison, guilt | `(LLM tail)` | Sam → Dareon | affc-samwell-04 |
| 3714 | 1 | reverence for | `(LLM tail)` | Summer Islanders (crew) → The elderly / Maester Aemon | affc-samwell-04 |
| 3715 | 1 | Protective/romantic attachment to | `(LLM tail)` | Sam → Gilly | affc-samwell-05 |
| 3716 | 1 | Trust/affection toward | `LOVES` | Gilly → Sam | affc-samwell-05 |
| 3717 | 1 | Maternal love for | `LOVES` | Gilly → Dalla's babe | affc-samwell-05 |
| 3718 | 1 | Friendly/teasing toward | `COMPANION_OF` | Kojja Mo → Sam | affc-samwell-05 |
| 3719 | 1 | Friendly respect toward | `RESPECTS` | Sam → Kojja Mo | affc-samwell-05 |
| 3720 | 1 | Fear/complicated resentment of | `FEARS` | Sam → Lord Randyll Tarly | affc-samwell-05 |
| 3721 | 1 | Rejection of | `(LLM tail)` | Lord Randyll Tarly → Sam | affc-samwell-05 |
| 3722 | 1 | Deep loyalty to | `(LLM tail)` | Sam → Jon Snow | affc-samwell-05 |
| 3723 | 1 | Grief/reverence for | `MOURNS` | Sam → Maester Aemon | affc-samwell-05 |
| 3724 | 1 | Agent/loyal servant of | `(LLM tail)` | Alleras → Archmaester Marwyn | affc-samwell-05 |
| 3725 | 1 | Interest/respect toward | `RESPECTS` | Alleras → Maester Aemon | affc-samwell-05 |
| 3726 | 1 | Friendly helpfulness toward | `COMPANION_OF` | Alleras → Sam | affc-samwell-05 |
| 3727 | 1 | Contempt/mockery toward | `HATES` | Leo Tyrell → Sam | affc-samwell-05 |
| 3728 | 1 | General contempt toward | `(LLM tail)` | Leo Tyrell → Other novices/acolytes | affc-samwell-05 |
| 3729 | 1 | Childhood fear of | `FEARS` | Sam → Leo Tyrell | affc-samwell-05 |
| 3730 | 1 | Urgency/mission toward | `(LLM tail)` | Archmaester Marwyn → Daenerys Targaryen | affc-samwell-05 |
| 3731 | 1 | Commanding/protective toward | `COMMANDS` | Archmaester Marwyn → Sam | affc-samwell-05 |
| 3732 | 1 | Trust in | `TRUSTS` | Marwyn → Alleras | affc-samwell-05 |
| 3733 | 1 | Instinctive dislike of | `(LLM tail)` | Sam → Pate | affc-samwell-05 |
| 3734 | 1 | Helpful/accommodating toward | `(LLM tail)` | Pate → Sam | affc-samwell-05 |
| 3735 | 1 | Dependent on / conflicted about | `(LLM tail)` | Sansa → Petyr Baelish | affc-sansa-01 |
| 3736 | 1 | Protector / manipulator of | `(LLM tail)` | Petyr Baelish → Sansa | affc-sansa-01 |
| 3737 | 1 | Loyal to / dependent on | `SERVES` | Lord Nestor Royce → Petyr Baelish | affc-sansa-01 |
| 3738 | 1 | Coerced confessor for | `(LLM tail)` | Marillion → Petyr Baelish | affc-sansa-01 |
| 3739 | 1 | Attached to / dependent on | `(LLM tail)` | Robert Arryn → Sansa | affc-sansa-01 |
| 3740 | 1 | Guard/protector of | `(LLM tail)` | Ser Lothor Brune → Sansa | affc-sansa-01 |
| 3741 | 1 | Gaoler / torturer of | `(LLM tail)` | Mord → Marillion | affc-sansa-01 |
| 3742 | 1 | Favored | `(LLM tail)` | Lysa Arryn → Marillion | affc-sansa-01 |
| 3743 | 1 | Watches via | `(LLM tail)` | Petyr → Kettleblack / Brune | affc-sansa-01 |
| 3744 | 1 | Pities despite herself | `(LLM tail)` | Sansa → Marillion | affc-sansa-01 |
| 3745 | 1 | Blurs identity of | `(LLM tail)` | Petyr → Sansa / Catelyn | affc-sansa-01 |
| 3746 | 1 | Guards/protects | `GUARDS` | Areo Hotah → Prince Doran | affc-the-captain-of-guards-01 |
| 3747 | 1 | Demands war from | `(LLM tail)` | Obara Sand → Prince Doran | affc-the-captain-of-guards-01 |
| 3748 | 1 | Demands assassination from | `(LLM tail)` | Nymeria Sand → Prince Doran | affc-the-captain-of-guards-01 |
| 3749 | 1 | Proposes crowning Myrcella to | `(LLM tail)` | Tyene Sand → Prince Doran | affc-the-captain-of-guards-01 |
| 3750 | 1 | Resists/deflects | `(LLM tail)` | Prince Doran → All three Sand Snakes | affc-the-captain-of-guards-01 |
| 3751 | 1 | Orders arrest of | `(LLM tail)` | Prince Doran → Sand Snakes (all eight) | affc-the-captain-of-guards-01 |
| 3752 | 1 | Anticipates fighting | `(LLM tail)` | Areo Hotah → Ser Arys Oakheart | affc-the-captain-of-guards-01 |
| 3753 | 1 | Attends/guards | `(LLM tail)` | Ser Arys Oakheart → Princess Myrcella | affc-the-captain-of-guards-01 |
| 3754 | 1 | Sibling of (deceased) | `SIBLING_OF` | Doran Martell → Elia Martell | affc-the-captain-of-guards-01 |
| 3755 | 1 | Took/claimed | `(LLM tail)` | Oberyn Martell → Obara Sand | affc-the-captain-of-guards-01 |
| 3756 | 1 | Mother was from | `(LLM tail)` | Nymeria Sand → Volantis (noble blood) | affc-the-captain-of-guards-01 |
| 3757 | 1 | Mother was | `(LLM tail)` | Tyene Sand → A septa | affc-the-captain-of-guards-01 |
| 3758 | 1 | Sold to | `(LLM tail)` | Hotah → Bearded priests of Norvos | affc-the-captain-of-guards-01 |
| 3759 | 1 | "Wed" to | `(LLM tail)` | Hotah → His longaxe | affc-the-captain-of-guards-01 |
| 3760 | 1 | Supports as king | `(LLM tail)` | Aeron Greyjoy → Victarion Greyjoy | affc-the-drowned-man-01 |
| 3761 | 1 | Fears and opposes | `FEARS` | Aeron Greyjoy → Euron Greyjoy | affc-the-drowned-man-01 |
| 3762 | 1 | Brother of / brought bride for | `SIBLING_OF` | Victarion Greyjoy → Balon Greyjoy | affc-the-drowned-man-01 |
| 3763 | 1 | Champion of / supporter of | `(LLM tail)` | Tristifer Botley → Asha Greyjoy | affc-the-drowned-man-01 |
| 3764 | 1 | Advisor/ally of | `ALLIES_WITH` | Orkwood of Orkmont → Euron Greyjoy | affc-the-drowned-man-01 |
| 3765 | 1 | Has grandsons including | `(LLM tail)` | Erik Ironmaker → Thormor | affc-the-drowned-man-01 |
| 3766 | 1 | Father of (inferred) | `PARENT_OF` | Gylbert Farwynd → Three unnamed champions | affc-the-drowned-man-01 |
| 3767 | 1 | Slew | `KILLS` | The Grey King → Nagga | affc-the-drowned-man-01 |
| 3768 | 1 | Married | `(LLM tail)` | The Grey King → A mermaid wife | affc-the-drowned-man-01 |
| 3769 | 1 | Mocks / challenges | `OPPOSES` | Asha Greyjoy → Victarion Greyjoy | affc-the-drowned-man-01 |
| 3770 | 1 | Challenges | `(LLM tail)` | Asha Greyjoy → Erik Ironmaker | affc-the-drowned-man-01 |
| 3771 | 1 | Brother (younger) | `SIBLING_OF` | Victarion → Euron | affc-the-iron-captain-01 |
| 3772 | 1 | Brother | `SIBLING_OF` | Victarion → Aeron | affc-the-iron-captain-01 |
| 3773 | 1 | Lord Captain of | `(LLM tail)` | Victarion → Iron Fleet | affc-the-iron-captain-01 |
| 3774 | 1 | Impregnated wife of | `(LLM tail)` | Euron → Victarion | affc-the-iron-captain-01 |
| 3775 | 1 | Killed his salt wife because of | `KILLS` | Victarion → Euron | affc-the-iron-captain-01 |
| 3776 | 1 | Worships | `WORSHIPS` | Baelor Blacktyde → Seven (Faith of the Seven) | affc-the-iron-captain-01 |
| 3777 | 1 | Drowned | `(LLM tail)` | Euron → Sawane Botley | affc-the-iron-captain-01 |
| 3778 | 1 | Respects tradition of | `RESPECTS` | Victarion → No kinslaying | affc-the-iron-captain-01 |
| 3779 | 1 | Obeys commands of | `COMMANDS` | Victarion → Balon (when alive) | affc-the-iron-captain-01 |
| 3780 | 1 | Niece; deep affection and respect | `UNCLE_OF` | Asha Greyjoy → Lord Rodrik Harlaw | affc-the-krakens-daughter-01 |
| 3781 | 1 | Daughter; grief and avoidance | `MOURNS` | Asha Greyjoy → Lady Alannys Harlaw | affc-the-krakens-daughter-01 |
| 3782 | 1 | Daughter; complicated grief | `MOURNS` | Asha Greyjoy → Balon Greyjoy | affc-the-krakens-daughter-01 |
| 3783 | 1 | Sister; conflicted | `SIBLING_OF` | Asha Greyjoy → Theon Greyjoy | affc-the-krakens-daughter-01 |
| 3784 | 1 | Political rival / enmity | `(LLM tail)` | Asha Greyjoy → Euron Greyjoy (Crow's Eye) | affc-the-krakens-daughter-01 |
| 3785 | 1 | Captain commanding crew | `COMMANDS` | Asha Greyjoy → Crew of Black Wind | affc-the-krakens-daughter-01 |
| 3786 | 1 | Captor, shows care | `CAPTURES` | Asha Greyjoy → Lady Glover and children | affc-the-krakens-daughter-01 |
| 3787 | 1 | Former youthful lover; no current interest | `LOVER_OF` | Asha Greyjoy → Tristifer Botley | affc-the-krakens-daughter-01 |
| 3788 | 1 | Brother; burdened guardian | `SIBLING_OF` | Lord Rodrik Harlaw → Lady Alannys Harlaw | affc-the-krakens-daughter-01 |
| 3789 | 1 | Brother; weary tolerance | `SIBLING_OF` | Lord Rodrik Harlaw → Lady Gwynesse | affc-the-krakens-daughter-01 |
| 3790 | 1 | Guardian / political counsel | `ADVISES` | Lord Rodrik Harlaw → Asha Greyjoy | affc-the-krakens-daughter-01 |
| 3791 | 1 | Feudal lord; commands loyalty | `COMMANDS` | Lord Rodrik Harlaw → Harlaw vassals (Volmarks, Stonetrees, Kennings, Myres) | affc-the-krakens-daughter-01 |
| 3792 | 1 | Designated successor | `(LLM tail)` | Lord Rodrik Harlaw → Ser Harras Harlaw (the Knight) | affc-the-krakens-daughter-01 |
| 3793 | 1 | Devoted / unrequited love | `LOVES` | Tristifer Botley → Asha Greyjoy | affc-the-krakens-daughter-01 |
| 3794 | 1 | Son; grieving | `MOURNS` | Tristifer Botley → Sawane Botley | affc-the-krakens-daughter-01 |
| 3795 | 1 | Dispossessed lord | `(LLM tail)` | Tristifer Botley → Euron Greyjoy | affc-the-krakens-daughter-01 |
| 3796 | 1 | Murdered (alleged) | `KILLS` | Euron Greyjoy → Balon Greyjoy | affc-the-krakens-daughter-01 |
| 3797 | 1 | Buying loyalty | `(LLM tail)` | Euron Greyjoy → Various lords and captains | affc-the-krakens-daughter-01 |
| 3798 | 1 | Mother; mourning | `MOURNS` | Lady Alannys Harlaw → Theon, Rodrik, Maron Greyjoy | affc-the-krakens-daughter-01 |
| 3799 | 1 | Sister; claims inheritance | `SIBLING_OF` | Lady Gwynesse → Lord Rodrik Harlaw | affc-the-krakens-daughter-01 |
| 3800 | 1 | Former guardian | `(LLM tail)` | Baelor Blacktyde → Tristifer Botley | affc-the-krakens-daughter-01 |
| 3801 | 1 | Suitor (via daughter) | `(LLM tail)` | Hotho Harlaw → Lord Rodrik Harlaw | affc-the-krakens-daughter-01 |
| 3802 | 1 | lover of (deceased) | `LOVER_OF` | Arianne Martell → Ser Arys Oakheart | affc-the-princess-in-the-tower-01 |
| 3803 | 1 | close cousin/like a sister to | `COUSIN_OF` | Arianne Martell → Tyene Sand | affc-the-princess-in-the-tower-01 |
| 3804 | 1 | loves (familial) | `LOVES` | Arianne Martell → All Sand Snakes | affc-the-princess-in-the-tower-01 |
| 3805 | 1 | husband of (estranged) | `(LLM tail)` | Prince Doran Martell → Lady Mellario | affc-the-princess-in-the-tower-01 |
| 3806 | 1 | brother of (deceased) | `SIBLING_OF` | Prince Doran Martell → Prince Oberyn Martell | affc-the-princess-in-the-tower-01 |
| 3807 | 1 | seeks vengeance for | `SEEKS` | Prince Doran Martell → Elia Martell (sister, deceased) | affc-the-princess-in-the-tower-01 |
| 3808 | 1 | guardian/ward of | `(LLM tail)` | Prince Doran Martell → Myrcella Baratheon | affc-the-princess-in-the-tower-01 |
| 3809 | 1 | secretly betrothed Arianne to | `BETROTHED_TO` | Prince Doran Martell → Unnamed betrothed (dead by molten gold) | affc-the-princess-in-the-tower-01 |
| 3810 | 1 | shield of (formerly) | `(LLM tail)` | Areo Hotah → Lady Mellario | affc-the-princess-in-the-tower-01 |
| 3811 | 1 | escaped from | `(LLM tail)` | Darkstar / Ser Gerold Dayne → Areo Hotah | affc-the-princess-in-the-tower-01 |
| 3812 | 1 | formerly bedded | `(LLM tail)` | Garin → Cedra | affc-the-princess-in-the-tower-01 |
| 3813 | 1 | sought to marry | `(LLM tail)` | Daemon Sand → Arianne Martell | affc-the-princess-in-the-tower-01 |
| 3814 | 1 | natural daughter of | `(LLM tail)` | Ellaria Sand → Harmen Uller | affc-the-princess-in-the-tower-01 |
| 3815 | 1 | fostered | `WARD_OF` | Anders Yronwood → Quentyn Martell | affc-the-princess-in-the-tower-01 |
| 3816 | 1 | historical enemies of | `(LLM tail)` | House Fowler → House Yronwood | affc-the-princess-in-the-tower-01 |
| 3817 | 1 | friends of | `(LLM tail)` | Fowler twins (Jeyne & Jennelyn) → Nymeria Sand (Nym) | affc-the-princess-in-the-tower-01 |
| 3818 | 1 | bedmaid of (formerly) | `(LLM tail)` | Belandra → Lady Mellario | affc-the-princess-in-the-tower-01 |
| 3819 | 1 | childhood friends (the company of five) | `(LLM tail)` | Arianne Martell → Tyene, Garin, Drey, Spotted Sylva | affc-the-princess-in-the-tower-01 |
| 3820 | 1 | refused suitor | `(LLM tail)` | Arianne Martell → Lord Renly Baratheon | affc-the-princess-in-the-tower-01 |
| 3821 | 1 | never met (blocked by Doran) | `(LLM tail)` | Arianne Martell → Willas Tyrell | affc-the-princess-in-the-tower-01 |
| 3822 | 1 | caught and returned | `(LLM tail)` | Prince Oberyn → Arianne and Tyene | affc-the-princess-in-the-tower-01 |
| 3823 | 1 | childhood friend of | `(LLM tail)` | Frynne → Arianne | affc-the-princess-in-the-tower-01 |
| 3824 | 1 | Priest/prophet of | `(LLM tail)` | Aeron Greyjoy → Drowned God | affc-the-prophet-01 |
| 3825 | 1 | Fears/dreads | `FEARS` | Aeron Greyjoy → Euron Greyjoy | affc-the-prophet-01 |
| 3826 | 1 | Scorned by | `(LLM tail)` | Aeron Greyjoy → Balon Greyjoy | affc-the-prophet-01 |
| 3827 | 1 | Favored successor | `(LLM tail)` | Balon Greyjoy → Asha Greyjoy | affc-the-prophet-01 |
| 3828 | 1 | Banished | `(LLM tail)` | Balon Greyjoy → Euron Greyjoy | affc-the-prophet-01 |
| 3829 | 1 | Eldest brother of | `SIBLING_OF` | Balon Greyjoy → Euron, Victarion, Urrigon, Aeron | affc-the-prophet-01 |
| 3830 | 1 | Claimed | `(LLM tail)` | Euron Greyjoy → Seastone Chair | affc-the-prophet-01 |
| 3831 | 1 | Killed (by drowning) | `KILLS` | Euron Greyjoy → Sawane Botley | affc-the-prophet-01 |
| 3832 | 1 | Elder brother of | `SIBLING_OF` | Euron Greyjoy → Victarion Greyjoy | affc-the-prophet-01 |
| 3833 | 1 | Has no love for | `LOVES` | Victarion Greyjoy → Euron Greyjoy | affc-the-prophet-01 |
| 3834 | 1 | Father of nine sons | `PARENT_OF` | Quellon Greyjoy → Harlon, Quenton, Donel, Balon, Euron, Victarion, Urrigon, Aeron, Robin | affc-the-prophet-01 |
| 3835 | 1 | Married (first wife) | `(LLM tail)` | Quellon Greyjoy → Woman of the Stonetrees | affc-the-prophet-01 |
| 3836 | 1 | Married (second wife) | `(LLM tail)` | Quellon Greyjoy → Sunderly of Saltcliffe | affc-the-prophet-01 |
| 3837 | 1 | Married (third wife) | `(LLM tail)` | Quellon Greyjoy → Piper of Pinkmaiden Castle | affc-the-prophet-01 |
| 3838 | 1 | Punished (mutilated) | `(LLM tail)` | Balon Greyjoy → Green-land maester | affc-the-prophet-01 |
| 3839 | 1 | Sailed with | `(LLM tail)` | Dagmer Cleftjaw → Young Balon | affc-the-prophet-01 |
| 3840 | 1 | Leader of conspiracy | `CONSPIRES_WITH` | Arianne Martell → Drey, Sylva, Garin, Darkstar | affc-the-queenmaker-01 |
| 3841 | 1 | Milk siblings / lifelong companions | `(LLM tail)` | Arianne Martell → Garin | affc-the-queenmaker-01 |
| 3842 | 1 | Dearest friends | `(LLM tail)` | Arianne Martell → Drey, Spotted Sylva | affc-the-queenmaker-01 |
| 3843 | 1 | Sexual attraction / wariness | `(LLM tail)` | Arianne Martell → Darkstar | affc-the-queenmaker-01 |
| 3844 | 1 | Rivalry / resentment | `(LLM tail)` | Arianne Martell → Quentyn Martell | affc-the-queenmaker-01 |
| 3845 | 1 | Resentment / defiance toward | `RESENTS` | Arianne Martell → Doran Martell | affc-the-queenmaker-01 |
| 3846 | 1 | Suggested romantic interest | `(LLM tail)` | Darkstar → Arianne Martell | affc-the-queenmaker-01 |
| 3847 | 1 | Contempt / provocation | `HATES` | Darkstar → Ser Arys Oakheart | affc-the-queenmaker-01 |
| 3848 | 1 | Jealousy | `(LLM tail)` | Darkstar → Arthur Dayne | affc-the-queenmaker-01 |
| 3849 | 1 | Devotion / loyalty | `(LLM tail)` | Ser Arys Oakheart → Arianne Martell | affc-the-queenmaker-01 |
| 3850 | 1 | Protective duty | `(LLM tail)` | Ser Arys Oakheart → Princess Myrcella | affc-the-queenmaker-01 |
| 3851 | 1 | Sent as ward (blood debt) | `(LLM tail)` | Doran Martell → Quentyn Martell → Lord Ormond Yronwood | affc-the-queenmaker-01 |
| 3852 | 1 | Anger / estrangement | `(LLM tail)` | Lady Mellario → Doran Martell | affc-the-queenmaker-01 |
| 3853 | 1 | Cousin / ally | `COUSIN_OF` | Arianne Martell → Lady Nym (Nymeria Sand) | affc-the-queenmaker-01 |
| 3854 | 1 | Cousin / close friend | `COUSIN_OF` | Arianne Martell → Tyene Sand | affc-the-queenmaker-01 |
| 3855 | 1 | Uncle / formative influence | `UNCLE_OF` | Prince Oberyn Martell → Arianne Martell | affc-the-queenmaker-01 |
| 3856 | 1 | Serves / loyal instrument | `SERVES` | Areo Hotah → Doran Martell | affc-the-queenmaker-01 |
| 3857 | 1 | Cyvasse opponent / betrothed | `BETROTHED_TO` | Myrcella Baratheon → Trystane Martell | affc-the-queenmaker-01 |
| 3858 | 1 | Decoy / distant kin | `(LLM tail)` | Rosamund → Myrcella Baratheon | affc-the-queenmaker-01 |
| 3859 | 1 | Brother, rival, resentful subordinate | `SIBLING_OF` | Victarion → Euron | affc-the-reaver-01 |
| 3860 | 1 | Brother, loyal memory | `SIBLING_OF` | Victarion → Balon | affc-the-reaver-01 |
| 3861 | 1 | Brother, sympathetic but frustrated | `SIBLING_OF` | Victarion → Aeron | affc-the-reaver-01 |
| 3862 | 1 | Half-sister, paternalistic concern | `SIBLING_OF` | Victarion → Asha | affc-the-reaver-01 |
| 3863 | 1 | Possessor / complicated feelings | `(LLM tail)` | Victarion → The dusky woman | affc-the-reaver-01 |
| 3864 | 1 | Respected enemy | `RESPECTS` | Victarion → Ser Talbert Serry | affc-the-reaver-01 |
| 3865 | 1 | King, manipulator | `(LLM tail)` | Euron → Victarion | affc-the-reaver-01 |
| 3866 | 1 | Oppressor | `(LLM tail)` | Euron → Lord Hewett | affc-the-reaver-01 |
| 3867 | 1 | Sexual predator | `(LLM tail)` | Euron → Falia Flowers | affc-the-reaver-01 |
| 3868 | 1 | Executed | `(LLM tail)` | Euron → Baelor Blacktyde | affc-the-reaver-01 |
| 3869 | 1 | King, strategic gift-giver | `(LLM tail)` | Euron → Ser Harras, Andrik, Volmark, Nute | affc-the-reaver-01 |
| 3870 | 1 | Political opponent | `(LLM tail)` | Rodrik Harlaw → Euron | affc-the-reaver-01 |
| 3871 | 1 | Ambitious subordinate | `SERVES` | Hotho Harlaw → Rodrik Harlaw | affc-the-reaver-01 |
| 3872 | 1 | Cautious ally | `ALLIES_WITH` | Drumm → Rodrik Harlaw | affc-the-reaver-01 |
| 3873 | 1 | Dismissive | `(LLM tail)` | Nute → Rodrik Harlaw | affc-the-reaver-01 |
| 3874 | 1 | Spiritual opposition | `(LLM tail)` | Aeron → Euron | affc-the-reaver-01 |
| 3875 | 1 | Boyhood friend | `(LLM tail)` | Ser Harras Harlaw → Rodrik Greyjoy | affc-the-reaver-01 |
| 3876 | 1 | Descendant through mother | `(LLM tail)` | Maron Volmark → Black Harren | affc-the-reaver-01 |
| 3877 | 1 | Rapist | `(LLM tail)` | Left-Hand Lucas Codd → Lord Hewett's daughter | affc-the-reaver-01 |
| 3878 | 1 | Captured/enslaved | `(LLM tail)` | Euron → Four Qartheen warlocks | affc-the-reaver-01 |
| 3879 | 1 | Paternal affection for | `LOVES` | Arys Oakheart → Myrcella Baratheon | affc-the-soiled-knight-01 |
| 3880 | 1 | Daughter of / politically opposed to | `PARENT_OF` | Arianne Martell → Doran Martell | affc-the-soiled-knight-01 |
| 3881 | 1 | Close as sisters with | `(LLM tail)` | Arianne Martell → Tyene Sand | affc-the-soiled-knight-01 |
| 3882 | 1 | Imprisoned | `IMPRISONS` | Doran Martell → Sand Snakes | affc-the-soiled-knight-01 |
| 3883 | 1 | Father of, possibly disinheriting | `(LLM tail)` | Doran Martell → Arianne Martell | affc-the-soiled-knight-01 |
| 3884 | 1 | Fostered by | `WARD_OF` | Quentyn Martell → Lord Anders Yronwood | affc-the-soiled-knight-01 |
| 3885 | 1 | Ashamed of serving | `(LLM tail)` | Arys Oakheart → Joffrey Baratheon | affc-the-soiled-knight-01 |
| 3886 | 1 | Conflicted admiration for | `RESPECTS` | Arys Oakheart → Arianne Martell | affc-the-soiled-knight-01 |
| 3887 | 1 | Compared favorably to | `(LLM tail)` | Myrcella Baratheon → Tommen Baratheon | affc-the-soiled-knight-01 |
| 3888 | 1 | Parallel drawn with | `(LLM tail)` | Cersei Lannister / Robert Baratheon → Myrcella / Trystane | affc-the-soiled-knight-01 |
| 3889 | 1 | Terrorized by / enslaved to | `(LLM tail)` | Theon → Ramsay Bolton | adwd-a-ghost-in-winterfell-01 |
| 3890 | 1 | Interrogated by / subject of | `(LLM tail)` | Theon → Roose Bolton | adwd-a-ghost-in-winterfell-01 |
| 3891 | 1 | Opposes / despises | `OPPOSES` | Wyman Manderly → House Frey | adwd-a-ghost-in-winterfell-01 |
| 3892 | 1 | Distrusts / threatens | `DISTRUSTS` | Lady Dustin → House Frey | adwd-a-ghost-in-winterfell-01 |
| 3893 | 1 | Threaten then recruit | `(LLM tail)` | Holly/Rowan → Theon | adwd-a-ghost-in-winterfell-01 |
| 3894 | 1 | Held by loyalty to | `(LLM tail)` | Northern lords → "The girl" (fake Arya) | adwd-a-ghost-in-winterfell-01 |
| 3895 | 1 | Haunted by guilt toward | `(LLM tail)` | Theon → Miller's wife and sons, Mikken, Farlen | adwd-a-ghost-in-winterfell-01 |
| 3896 | 1 | protects / cares for | `PROTECTS` | Meera → Jojen | adwd-bran-01 |
| 3897 | 1 | reassures | `(LLM tail)` | Jojen → Meera | adwd-bran-01 |
| 3898 | 1 | guides / protects | `(LLM tail)` | Coldhands → Bran | adwd-bran-01 |
| 3899 | 1 | hungry for / restrained from | `(LLM tail)` | Summer → The elk | adwd-bran-01 |
| 3900 | 1 | hopes for reconnection with | `(LLM tail)` | Bran → Shaggydog, Nymeria, Ghost | adwd-bran-01 |
| 3901 | 1 | serves / sent by | `SERVES` | Coldhands → Three-eyed crow | adwd-bran-01 |
| 3902 | 1 | recalls stories from | `(LLM tail)` | Bran → Old Nan | adwd-bran-01 |
| 3903 | 1 | was saved by | `(LLM tail)` | Sam → Coldhands | adwd-bran-01 |
| 3904 | 1 | warging/controlling | `WARGS_INTO` | Bran → Hodor | adwd-bran-02 |
| 3905 | 1 | protective caretaker of | `(LLM tail)` | Meera Reed → Jojen Reed | adwd-bran-02 |
| 3906 | 1 | guide/protector of | `(LLM tail)` | Coldhands → Bran and company | adwd-bran-02 |
| 3907 | 1 | rescuer/guide of | `(LLM tail)` | Leaf (child of the forest) → Bran and company | adwd-bran-02 |
| 3908 | 1 | has been watching | `(LLM tail)` | The Greenseer → Bran | adwd-bran-02 |
| 3909 | 1 | formerly a member of | `(LLM tail)` | The Greenseer → Night's Watch | adwd-bran-02 |
| 3910 | 1 | love/affection for | `LOVES` | Bran → Meera Reed | adwd-bran-02 |
| 3911 | 1 | excluded from cave by | `(LLM tail)` | Coldhands → The cave's wards | adwd-bran-02 |
| 3912 | 1 | watched | `(LLM tail)` | The Greenseer → Bran's lord father (Ned Stark) | adwd-bran-02 |
| 3913 | 1 | Student / apprentice to | `TUTORS` | Bran → Lord Brynden | adwd-bran-03 |
| 3914 | 1 | Warging into (ethically fraught) | `WARGS_INTO` | Bran → Hodor | adwd-bran-03 |
| 3915 | 1 | Emotional dependence on / affection for | `LOVES` | Bran → Meera Reed | adwd-bran-03 |
| 3916 | 1 | Growing bitterness about | `(LLM tail)` | Meera → Their journey | adwd-bran-03 |
| 3917 | 1 | Resignation to | `(LLM tail)` | Jojen → His fate | adwd-bran-03 |
| 3918 | 1 | Merged with / dependent on | `(LLM tail)` | Lord Brynden → Weirwood tree | adwd-bran-03 |
| 3919 | 1 | Haunted by memories of | `(LLM tail)` | Lord Brynden → A brother he loved, a brother he hated, a woman he desired | adwd-bran-03 |
| 3920 | 1 | Guardian / guide to | `(LLM tail)` | Leaf → Bran and companions | adwd-bran-03 |
| 3921 | 1 | Longing for / missing | `MOURNS` | Bran → Robb, Arya, Sansa, Rickon, Jon | adwd-bran-03 |
| 3922 | 1 | Fear of becoming | `FEARS` | Bran → Lord Brynden | adwd-bran-03 |
| 3923 | 1 | Serve / sustain | `(LLM tail)` | Singers → Lord Brynden | adwd-bran-03 |
| 3924 | 1 | twin sister of | `SIBLING_OF` | Cersei → Jaime Lannister | adwd-cersei-01 |
| 3925 | 1 | accuser of | `(LLM tail)` | Lancel Lannister → Cersei | adwd-cersei-01 |
| 3926 | 1 | Lord Regent for | `(LLM tail)` | Ser Kevan → Tommen Baratheon | adwd-cersei-01 |
| 3927 | 1 | serves as justiciar to | `SERVES` | Randyll Tarly → Tommen Baratheon | adwd-cersei-01 |
| 3928 | 1 | serves as lord admiral to | `SERVES` | Paxter Redwyne → Tommen Baratheon | adwd-cersei-01 |
| 3929 | 1 | in custody of | `(LLM tail)` | Margaery Tyrell → Randyll Tarly | adwd-cersei-01 |
| 3930 | 1 | with | `(LLM tail)` | Margaery Tyrell → Tommen Baratheon | adwd-cersei-01 |
| 3931 | 1 | defended | `(LLM tail)` | Arys Oakheart → Myrcella Baratheon | adwd-cersei-01 |
| 3932 | 1 | went off with | `(LLM tail)` | Jaime Lannister → Brienne of Tarth | adwd-cersei-01 |
| 3933 | 1 | holds prisoners for | `(LLM tail)` | Qyburn → Cersei | adwd-cersei-01 |
| 3934 | 1 | Lover / desires rescue from | `LOVER_OF` | Cersei → Jaime | adwd-cersei-02 |
| 3935 | 1 | Mother desperate for | `(LLM tail)` | Cersei → Tommen | adwd-cersei-02 |
| 3936 | 1 | Mother (bereaved) of | `(LLM tail)` | Cersei → Joffrey | adwd-cersei-02 |
| 3937 | 1 | Hates / vows revenge on | `HATES` | Cersei → Septa Scolera | adwd-cersei-02 |
| 3938 | 1 | Ally of / relies on | `ALLIES_WITH` | Cersei → Qyburn | adwd-cersei-02 |
| 3939 | 1 | Contempt for / politically opposed to | `HATES` | Cersei → Ned Stark | adwd-cersei-02 |
| 3940 | 1 | Feared / hated | `(LLM tail)` | Cersei → Tyrion | adwd-cersei-02 |
| 3941 | 1 | Daughter of / reveres | `PARENT_OF` | Cersei → Tywin | adwd-cersei-02 |
| 3942 | 1 | Humiliated / expelled | `(LLM tail)` | Tywin → Tytos's mistress | adwd-cersei-02 |
| 3943 | 1 | Haunted by prophecy of | `(LLM tail)` | Cersei → Maggy the Frog | adwd-cersei-02 |
| 3944 | 1 | Guilt/unease toward | `(LLM tail)` | Cersei → Melara Hetherspoon | adwd-cersei-02 |
| 3945 | 1 | Protective uncle / disapproving of | `UNCLE_OF` | Ser Kevan → Cersei | adwd-cersei-02 |
| 3946 | 1 | Disobeyed plan of | `(LLM tail)` | Joffrey → Cersei (and Varys, Littlefinger) | adwd-cersei-02 |
| 3947 | 1 | wary reliance on | `(LLM tail)` | Daenerys → Skahaz mo Kandaq | adwd-daenerys-01 |
| 3948 | 1 | is bonded to | `BONDED_TO` | Daenerys → Viserion | adwd-daenerys-01 |
| 3949 | 1 | misses/desires | `MOURNS` | Daenerys → Daario Naharis | adwd-daenerys-01 |
| 3950 | 1 | politically assessing | `(LLM tail)` | Daenerys → Hizdahr zo Loraq | adwd-daenerys-01 |
| 3951 | 1 | contempt tempered by need | `HATES` | Daenerys → Meereenese nobles | adwd-daenerys-01 |
| 3952 | 1 | opposes/moderates | `OPPOSES` | Reznak mo Reznak → Skahaz mo Kandaq | adwd-daenerys-01 |
| 3953 | 1 | petitions | `(LLM tail)` | Hizdahr zo Loraq → Daenerys | adwd-daenerys-01 |
| 3954 | 1 | serves as envoy for | `SERVES` | Lord Ghael → Cleon | adwd-daenerys-01 |
| 3955 | 1 | romantic desire for | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-02 |
| 3956 | 1 | maternal/protective of | `(LLM tail)` | Daenerys → Missandei | adwd-daenerys-02 |
| 3957 | 1 | devotion to | `(LLM tail)` | Missandei → Daenerys | adwd-daenerys-02 |
| 3958 | 1 | relies on / trusts | `(LLM tail)` | Daenerys → Skahaz mo Kandaq | adwd-daenerys-02 |
| 3959 | 1 | conflicted authority over | `(LLM tail)` | Daenerys → Rhaegal, Viserion | adwd-daenerys-02 |
| 3960 | 1 | loss/grief over | `MOURNS` | Daenerys → Drogon | adwd-daenerys-02 |
| 3961 | 1 | persistent petitioner to | `(LLM tail)` | Hizdahr zo Loraq → Daenerys | adwd-daenerys-02 |
| 3962 | 1 | cryptic guide to | `(LLM tail)` | Quaithe → Daenerys | adwd-daenerys-02 |
| 3963 | 1 | guilt/anguish over | `(LLM tail)` | Daenerys → Hazzea | adwd-daenerys-02 |
| 3964 | 1 | Distrusts but needs | `DISTRUSTS` | Daenerys → Xaro Xhoan Daxos | adwd-daenerys-03 |
| 3965 | 1 | Desires/seeks to manipulate | `(LLM tail)` | Xaro → Daenerys | adwd-daenerys-03 |
| 3966 | 1 | Desires romantically | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-03 |
| 3967 | 1 | Devoted to (as queen) | `(LLM tail)` | Barristan → Daenerys | adwd-daenerys-03 |
| 3968 | 1 | Remembers with mixture of contempt and pity | `(LLM tail)` | Daenerys → Viserys | adwd-daenerys-03 |
| 3969 | 1 | Protects violently | `PROTECTS` | Strong Belwas → Daenerys | adwd-daenerys-03 |
| 3970 | 1 | Desperate supplicant turned hostile | `(LLM tail)` | Lord Ghael → Daenerys | adwd-daenerys-03 |
| 3971 | 1 | Fearful servitor | `FEARS` | Reznak mo Reznak → Daenerys | adwd-daenerys-03 |
| 3972 | 1 | Fierce ally | `ALLIES_WITH` | Skahaz mo Kandaq → Daenerys | adwd-daenerys-03 |
| 3973 | 1 | Eager to serve/sail | `(LLM tail)` | Groleo → Daenerys | adwd-daenerys-03 |
| 3974 | 1 | Responsible for/duty toward | `(LLM tail)` | Daenerys → People of Meereen | adwd-daenerys-03 |
| 3975 | 1 | Feels guilty about | `(LLM tail)` | Daenerys → Hazzea | adwd-daenerys-03 |
| 3976 | 1 | Queen/captor of hostages (but fond) | `CAPTURES` | Daenerys → Qezza, Grazhar | adwd-daenerys-04 |
| 3977 | 1 | Blood relative (cousin) | `COUSIN_OF` | Galazza Galare → Qezza, Grazhar | adwd-daenerys-04 |
| 3978 | 1 | Sibling | `(LLM tail)` | Qezza → Grazhar | adwd-daenerys-04 |
| 3979 | 1 | Political advisor | `(LLM tail)` | Galazza Galare → Daenerys | adwd-daenerys-04 |
| 3980 | 1 | Suitor/proposed consort | `(LLM tail)` | Hizdahr zo Loraq → Daenerys | adwd-daenerys-04 |
| 3981 | 1 | Aggressive advisor (in tension with Dany) | `(LLM tail)` | Skahaz mo Kandaq → Daenerys | adwd-daenerys-04 |
| 3982 | 1 | Trusts more than Hizdahr | `TRUSTS` | Daenerys → Skahaz mo Kandaq | adwd-daenerys-04 |
| 3983 | 1 | Sexually desires / is drawn to | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-04 |
| 3984 | 1 | Desires / courts | `(LLM tail)` | Daario Naharis → Daenerys | adwd-daenerys-04 |
| 3985 | 1 | Loyal protector / disapproving advisor | `(LLM tail)` | Ser Barristan → Daenerys | adwd-daenerys-04 |
| 3986 | 1 | Was "fond" of (not love) | `LOVES` | Rhaegar Targaryen → Elia Martell | adwd-daenerys-04 |
| 3987 | 1 | Forced marriage (no fondness) | `(LLM tail)` | Aerys II → Rhaella | adwd-daenerys-04 |
| 3988 | 1 | Political alignment with | `(LLM tail)` | Hizdahr → Galazza Galare | adwd-daenerys-04 |
| 3989 | 1 | Kills own men for disloyalty | `KILLS` | Daario → His serjeants | adwd-daenerys-04 |
| 3990 | 1 | Feels unsafe around (emotionally) | `(LLM tail)` | Daenerys → Daario | adwd-daenerys-04 |
| 3991 | 1 | Rival/opposed faction to | `(LLM tail)` | Skahaz (Kandaq) → Hizdahr (Loraq) | adwd-daenerys-04 |
| 3992 | 1 | Identifies with (reluctantly) | `(LLM tail)` | Daenerys → Daario | adwd-daenerys-04 |
| 3993 | 1 | Feels comfort/safety from memory of | `(LLM tail)` | Daenerys → Drogo | adwd-daenerys-04 |
| 3994 | 1 | commands / frustrated with | `COMMANDS` | Daenerys → Groleo | adwd-daenerys-05 |
| 3995 | 1 | desires / misses | `MOURNS` | Daenerys → Daario Naharis | adwd-daenerys-05 |
| 3996 | 1 | misses / conflicted about | `MOURNS` | Daenerys → Ser Jorah Mormont | adwd-daenerys-05 |
| 3997 | 1 | compares favorably | `(LLM tail)` | Ser Barristan → Daenerys to Rhaegar | adwd-daenerys-05 |
| 3998 | 1 | trains/mentors | `TEACHES` | Ser Barristan → Orphan boys (knight candidates) | adwd-daenerys-05 |
| 3999 | 1 | accusing gaze toward | `(LLM tail)` | Astapori weaver → Daenerys | adwd-daenerys-05 |
| 4000 | 1 | sent away (political sacrifice) | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-05 |
| 4001 | 1 | rules / mother figure to | `RULES` | Daenerys → The Astapori refugees | adwd-daenerys-06 |
| 4002 | 1 | desires / becomes lovers with | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-06 |
| 4003 | 1 | mourns betrayal by | `MOURNS` | Daenerys → Brown Ben Plumm | adwd-daenerys-06 |
| 4004 | 1 | thinks of with pain/confusion | `(LLM tail)` | Daenerys → Ser Jorah Mormont | adwd-daenerys-06 |
| 4005 | 1 | rivals / argues with | `(LLM tail)` | Irri → Jhiqui | adwd-daenerys-06 |
| 4006 | 1 | opposes / distrusts | `OPPOSES` | Ser Barristan → Daario Naharis | adwd-daenerys-06 |
| 4007 | 1 | killed (a mutinous serjeant) | `KILLS` | Daario → Unnamed serjeant | adwd-daenerys-06 |
| 4008 | 1 | negotiates on behalf of | `(LLM tail)` | Hizdahr → Yunkai | adwd-daenerys-06 |
| 4009 | 1 | serves / close to | `SERVES` | Missandei → Daenerys | adwd-daenerys-06 |
| 4010 | 1 | Betrothed to / marries | `BETROTHED_TO` | Daenerys → Hizdahr zo Loraq | adwd-daenerys-07 |
| 4011 | 1 | Jealous of / hostile toward | `(LLM tail)` | Daario → Hizdahr zo Loraq | adwd-daenerys-07 |
| 4012 | 1 | Dismissive of / hostile toward | `DISTRUSTS` | Daario → Quentyn Martell | adwd-daenerys-07 |
| 4013 | 1 | Resistant to counsel from | `ADVISES` | Daenerys → Galazza Galare | adwd-daenerys-07 |
| 4014 | 1 | Protective of / disapproving of Daario with | `PROTECTS` | Barristan Selmy → Daenerys | adwd-daenerys-07 |
| 4015 | 1 | Unattracted to | `(LLM tail)` | Daenerys → Quentyn Martell | adwd-daenerys-07 |
| 4016 | 1 | Supports Ghiscari match | `(LLM tail)` | Skahaz mo Kandaq → Hizdahr/Meereen | adwd-daenerys-07 |
| 4017 | 1 | Devoted advisor to | `(LLM tail)` | Missandei → Daenerys | adwd-daenerys-07 |
| 4018 | 1 | Bought by / received payment from | `(LLM tail)` | Daario → Dornishmen (implied) | adwd-daenerys-07 |
| 4019 | 1 | Remembers with love | `LOVES` | Daenerys → Khal Drogo | adwd-daenerys-07 |
| 4020 | 1 | In service of | `(LLM tail)` | Strong Belwas → Daenerys | adwd-daenerys-07 |
| 4021 | 1 | Companion/protector of | `COMPANION_OF` | Gerris Drinkwater → Quentyn Martell | adwd-daenerys-07 |
| 4022 | 1 | desires / tries to renounce | `(LLM tail)` | Daenerys → Daario Naharis | adwd-daenerys-08 |
| 4023 | 1 | considers alliance with | `ALLIES_WITH` | Daenerys → Quentyn Martell | adwd-daenerys-08 |
| 4024 | 1 | is comforted by | `(LLM tail)` | Daenerys → Missandei | adwd-daenerys-08 |
| 4025 | 1 | respects lineage of | `RESPECTS` | Ser Barristan → Quentyn Martell | adwd-daenerys-08 |
| 4026 | 1 | removed from power | `(LLM tail)` | Hizdahr zo Loraq → Skahaz mo Kandaq (Shavepate) | adwd-daenerys-08 |
| 4027 | 1 | furious with | `(LLM tail)` | Daario Naharis → Quentyn's group | adwd-daenerys-08 |
| 4028 | 1 | blood feud with | `(LLM tail)` | Loraq (house) → Kandaq (house) | adwd-daenerys-08 |
| 4029 | 1 | married to (tense, transactional) | `(LLM tail)` | Daenerys → Hizdahr zo Loraq | adwd-daenerys-09 |
| 4030 | 1 | mother of (reconnection) | `PARENT_OF` | Daenerys → Drogon | adwd-daenerys-09 |
| 4031 | 1 | promotes/controls | `(LLM tail)` | Hizdahr → Fighting pits | adwd-daenerys-09 |
| 4032 | 1 | flash of anger toward | `(LLM tail)` | Hizdahr → Daenerys | adwd-daenerys-09 |
| 4033 | 1 | refuses audience with | `(LLM tail)` | Daenerys → Quentyn Martell | adwd-daenerys-09 |
| 4034 | 1 | demands | `(LLM tail)` | Tattered Prince → Pentos | adwd-daenerys-09 |
| 4035 | 1 | recalls with tenderness | `(LLM tail)` | Daenerys → Khal Drogo | adwd-daenerys-09 |
| 4036 | 1 | rider/bonded to | `BONDED_TO` | Daenerys → Drogon | adwd-daenerys-10 |
| 4037 | 1 | longs for / lover | `MOURNS` | Daenerys → Daario Naharis | adwd-daenerys-10 |
| 4038 | 1 | ambivalent wife | `(LLM tail)` | Daenerys → Hizdahr zo Loraq | adwd-daenerys-10 |
| 4039 | 1 | mourns/misses | `MOURNS` | Daenerys → Jorah Mormont | adwd-daenerys-10 |
| 4040 | 1 | complex grief | `MOURNS` | Daenerys → Viserys Targaryen | adwd-daenerys-10 |
| 4041 | 1 | suspects poisoner | `(LLM tail)` | Daenerys → Hizdahr / Reznak / Yunkai'i / Sons of Harpy | adwd-daenerys-10 |
| 4042 | 1 | counselor/admirer | `RESPECTS` | Jorah (voice) → Daenerys | adwd-daenerys-10 |
| 4043 | 1 | mysterious guide | `(LLM tail)` | Quaithe → Daenerys | adwd-daenerys-10 |
| 4044 | 1 | former ko of Drogo / hostile | `(LLM tail)` | Khal Jhaqo → Daenerys | adwd-daenerys-10 |
| 4045 | 1 | bloodrider to | `(LLM tail)` | Mago → Khal Jhaqo | adwd-daenerys-10 |
| 4046 | 1 | rival to | `(LLM tail)` | Ko Pono → Daenerys (Drogo's khalasar) | adwd-daenerys-10 |
| 4047 | 1 | Serves as Hand | `SERVES` | Davos → Stannis Baratheon | adwd-davos-01 |
| 4048 | 1 | Abandoned | `(LLM tail)` | Salladhor Saan → Stannis Baratheon | adwd-davos-01 |
| 4049 | 1 | Former friend of | `(LLM tail)` | Salladhor Saan → Davos | adwd-davos-01 |
| 4050 | 1 | Sworn vassal of | `(LLM tail)` | Godric Borrell → Triston Sunderland | adwd-davos-01 |
| 4051 | 1 | Host to | `(LLM tail)` | Godric Borrell → Davos | adwd-davos-01 |
| 4052 | 1 | Marriage pact with | `(LLM tail)` | Lord Walder Frey → Wyman Manderly | adwd-davos-01 |
| 4053 | 1 | Killed son of | `KILLS` | The Freys → Wyman Manderly | adwd-davos-01 |
| 4054 | 1 | Let pass | `(LLM tail)` | Lord Godric's father → Ned Stark | adwd-davos-01 |
| 4055 | 1 | Rules | `RULES` | Petyr Baelish → The Vale | adwd-davos-01 |
| 4056 | 1 | Allegedly fathered bastard with | `(LLM tail)` | Ned Stark → Fisherman's daughter | adwd-davos-01 |
| 4057 | 1 | serves as Hand/envoy | `SERVES` | Davos → Stannis | adwd-davos-02 |
| 4058 | 1 | lost four sons in service to | `(LLM tail)` | Davos → Stannis | adwd-davos-02 |
| 4059 | 1 | allied fleet commander of | `COMMANDS` | Salladhor Saan → Stannis | adwd-davos-02 |
| 4060 | 1 | ship captain transporting | `(LLM tail)` | Casso Mogat → Davos | adwd-davos-02 |
| 4061 | 1 | seeking alliance with | `ALLIES_WITH` | Robett Glover → Wyman Manderly | adwd-davos-02 |
| 4062 | 1 | brought the Faith to | `(LLM tail)` | Manderly (house) → White Harbor / the North | adwd-davos-02 |
| 4063 | 1 | disrespects/insults | `(LLM tail)` | Ser Axell Florent → Davos | adwd-davos-02 |
| 4064 | 1 | former master of | `(LLM tail)` | Roro Uhoris → Davos (as cabin boy) | adwd-davos-02 |
| 4065 | 1 | cousin and garrison commander to | `COUSIN_OF` | Ser Marlon Manderly → Lord Wyman Manderly | adwd-davos-03 |
| 4066 | 1 | good-father to | `(LLM tail)` | Lord Wyman Manderly → Lady Leona | adwd-davos-03 |
| 4067 | 1 | former vassal of | `(LLM tail)` | Lord Wyman Manderly → Robb Stark | adwd-davos-03 |
| 4068 | 1 | fearful/protective regarding | `FEARS` | Lady Leona → Ser Wylis Manderly | adwd-davos-03 |
| 4069 | 1 | apparent agreement with | `(LLM tail)` | Lord Wyman Manderly → Rhaegar Frey | adwd-davos-03 |
| 4070 | 1 | weeps for | `(LLM tail)` | Lord Wyman Manderly → Wendel Manderly | adwd-davos-03 |
| 4071 | 1 | ancient oath to | `(LLM tail)` | Manderlys → House Stark | adwd-davos-03 |
| 4072 | 1 | loyalty despite misgivings to | `(LLM tail)` | Davos Seaworth → Stannis Baratheon | adwd-davos-03 |
| 4073 | 1 | loyal servant of | `(LLM tail)` | Davos → King Stannis | adwd-davos-04 |
| 4074 | 1 | grieving father of | `MOURNS` | Davos → his dead older sons | adwd-davos-04 |
| 4075 | 1 | gaoler/threat to | `(LLM tail)` | Garth → Davos | adwd-davos-04 |
| 4076 | 1 | sympathetic keeper of | `(LLM tail)` | Therry → Davos | adwd-davos-04 |
| 4077 | 1 | chief gaoler / storyteller to | `(LLM tail)` | Ser Bartimus → Davos | adwd-davos-04 |
| 4078 | 1 | saved life of | `(LLM tail)` | Ser Bartimus → Wyman Manderly | adwd-davos-04 |
| 4079 | 1 | secretly loyal to | `(LLM tail)` | Wyman Manderly → House Stark | adwd-davos-04 |
| 4080 | 1 | father of (deceased) | `PARENT_OF` | Wyman Manderly → Wendel Manderly | adwd-davos-04 |
| 4081 | 1 | grandfather of | `PARENT_OF` | Wyman Manderly → Wylla, Wynafryd | adwd-davos-04 |
| 4082 | 1 | good-daughter of | `(LLM tail)` | Lady Leona → Wyman Manderly | adwd-davos-04 |
| 4083 | 1 | deceiving | `(LLM tail)` | Wyman Manderly → Freys (Jared, Rhaegar, Symond) | adwd-davos-04 |
| 4084 | 1 | spying on / bribing | `(LLM tail)` | Symond Frey → Wyman Manderly's household | adwd-davos-04 |
| 4085 | 1 | former squire to | `(LLM tail)` | Wex → Theon Greyjoy | adwd-davos-04 |
| 4086 | 1 | captured and flaying | `(LLM tail)` | Ramsay → Theon Greyjoy | adwd-davos-04 |
| 4087 | 1 | forced marriage to / murdered | `KILLS` | Ramsay → Lady Hornwood | adwd-davos-04 |
| 4088 | 1 | allied with / complicit with | `ALLIES_WITH` | Roose Bolton → Freys | adwd-davos-04 |
| 4089 | 1 | demands submission from | `(LLM tail)` | Roose Bolton → Northern lords | adwd-davos-04 |
| 4090 | 1 | asks service of | `(LLM tail)` | Manderly → Davos | adwd-davos-04 |
| 4091 | 1 | bedding | `(LLM tail)` | Therry's mother → Two guardsmen | adwd-davos-04 |
| 4092 | 1 | spreading lies about | `(LLM tail)` | Freys → Robb Stark | adwd-davos-04 |
| 4093 | 1 | Lord Regent governing in name of | `(LLM tail)` | Kevan Lannister → Tommen Baratheon | adwd-epilogue |
| 4094 | 1 | Political tension/alliance with | `ALLIES_WITH` | Kevan Lannister → Mace Tyrell | adwd-epilogue |
| 4095 | 1 | Guardianship/containment of | `(LLM tail)` | Kevan Lannister → Cersei Lannister | adwd-epilogue |
| 4096 | 1 | Familial duty toward | `(LLM tail)` | Kevan Lannister → Cersei Lannister | adwd-epilogue |
| 4097 | 1 | Loyalty to memory of | `SERVES` | Kevan Lannister → Tywin Lannister | adwd-epilogue |
| 4098 | 1 | Hand of the King to | `(LLM tail)` | Mace Tyrell → Tommen Baratheon | adwd-epilogue |
| 4099 | 1 | Father protecting | `(LLM tail)` | Mace Tyrell → Margaery Tyrell | adwd-epilogue |
| 4100 | 1 | Sworn to / serves | `SWORN_TO` | Randyll Tarly → Mace Tyrell | adwd-epilogue |
| 4101 | 1 | Viewed by Kevan as | `(LLM tail)` | Randyll Tarly → The real danger | adwd-epilogue |
| 4102 | 1 | Subdued submission to | `(LLM tail)` | Cersei Lannister → Kevan Lannister | adwd-epilogue |
| 4103 | 1 | Twin bond with | `(LLM tail)` | Cersei Lannister → Jaime Lannister | adwd-epilogue |
| 4104 | 1 | Serves/supports | `SERVES` | Varys → Aegon (pretender) | adwd-epilogue |
| 4105 | 1 | Views suspiciously | `(LLM tail)` | Kevan Lannister → Robert Strong | adwd-epilogue |
| 4106 | 1 | Nephew of (blood relation estranged from) | `NEPHEW_OF` | Ronnet Connington → Jon Connington | adwd-epilogue |
| 4107 | 1 | Remembers Tywin stripped and paraded | `(LLM tail)` | Kevan (memory) → Tytos's mistress | adwd-epilogue |
| 4108 | 1 | fond memory of | `(LLM tail)` | Jaime → Tyrion | adwd-jaime-01 |
| 4109 | 1 | shocked by condition of | `(LLM tail)` | Jaime → Brienne | adwd-jaime-01 |
| 4110 | 1 | besieging/rival of | `(LLM tail)` | Jonos Bracken → Tytos Blackwood | adwd-jaime-01 |
| 4111 | 1 | bold/flirtatious with | `(LLM tail)` | Hildy → Jaime | adwd-jaime-01 |
| 4112 | 1 | grieving father | `MOURNS` | Tytos Blackwood → Lucas Blackwood, Robert Blackwood | adwd-jaime-01 |
| 4113 | 1 | eager/naive toward | `(LLM tail)` | Hoster Blackwood → Jaime | adwd-jaime-01 |
| 4114 | 1 | harsh with | `(LLM tail)` | Jaime → Hoster Blackwood | adwd-jaime-01 |
| 4115 | 1 | knowledgeable about | `(LLM tail)` | Hoster Blackwood → Blackwood-Bracken history | adwd-jaime-01 |
| 4116 | 1 | bound by quest to | `(LLM tail)` | Brienne → Jaime | adwd-jaime-01 |
| 4117 | 1 | merciful toward | `(LLM tail)` | Jaime → Pennytree villagers | adwd-jaime-01 |
| 4118 | 1 | Bond with / wargs into | `WARGS_INTO` | Jon Snow → Ghost | adwd-jon-01 |
| 4119 | 1 | Commands (new/uncomfortable) | `COMMANDS` | Jon Snow → Dolorous Edd | adwd-jon-01 |
| 4120 | 1 | Defies / maintains independence from | `OPPOSES` | Jon Snow → Stannis Baratheon | adwd-jon-01 |
| 4121 | 1 | Threatens / pressures | `OPPOSES` | Stannis Baratheon → Jon Snow | adwd-jon-01 |
| 4122 | 1 | Attempts to cultivate / warns | `ADVISES` | Lady Melisandre → Jon Snow | adwd-jon-01 |
| 4123 | 1 | Wary of / distrusts | `DISTRUSTS` | Jon Snow → Lady Melisandre | adwd-jon-01 |
| 4124 | 1 | Grieves / remembers | `MOURNS` | Jon Snow → Robb Stark | adwd-jon-01 |
| 4125 | 1 | Conflicted regard for | `(LLM tail)` | Jon Snow → Sansa Stark | adwd-jon-01 |
| 4126 | 1 | Controls / uses | `COMMANDS` | Stannis Baratheon → Lady Melisandre | adwd-jon-01 |
| 4127 | 1 | Resents / frustrated by | `RESENTS` | Stannis Baratheon → Northern lords | adwd-jon-01 |
| 4128 | 1 | Taunts / challenges | `(LLM tail)` | Ser Godry Farring → Jon Snow | adwd-jon-01 |
| 4129 | 1 | Dismisses / ignores | `(LLM tail)` | Jon Snow → Ser Godry Farring | adwd-jon-01 |
| 4130 | 1 | Serves / supports | `SERVES` | Samwell Tarly → Jon Snow | adwd-jon-01 |
| 4131 | 1 | Mentors / encourages | `TUTORS` | Jon Snow → Samwell Tarly | adwd-jon-01 |
| 4132 | 1 | Follows / accompanies | `(LLM tail)` | Mormont's raven → Jon Snow | adwd-jon-01 |
| 4133 | 1 | Demands execution of | `(LLM tail)` | Stannis Baratheon → Mance Rayder | adwd-jon-01 |
| 4134 | 1 | Declared allegiance to | `(LLM tail)` | Arnolf Karstark → Stannis Baratheon | adwd-jon-01 |
| 4135 | 1 | trusts/relies on | `TRUSTS` | Jon Snow → Maester Aemon | adwd-jon-02 |
| 4136 | 1 | motherly protectiveness | `(LLM tail)` | Gilly → Her own son and Dalla's son | adwd-jon-02 |
| 4137 | 1 | allied with/pleading for | `ALLIES_WITH` | Val → Mance Rayder | adwd-jon-02 |
| 4138 | 1 | Grieves separation from | `MOURNS` | Jon Snow → Sam, Aemon, Gilly | adwd-jon-03 |
| 4139 | 1 | Desires/admires | `RESPECTS` | Jon Snow → Val | adwd-jon-03 |
| 4140 | 1 | Remembers/compares | `(LLM tail)` | Jon Snow → Ygritte | adwd-jon-03 |
| 4141 | 1 | Forced distance from | `(LLM tail)` | Jon Snow → Pyp, Grenn | adwd-jon-03 |
| 4142 | 1 | Political authority over | `(LLM tail)` | Stannis Baratheon → Wildling captives | adwd-jon-03 |
| 4143 | 1 | Serves under / disagrees with | `SERVES` | Bowen Marsh → Jon Snow | adwd-jon-03 |
| 4144 | 1 | Former member of | `(LLM tail)` | Mance Rayder → Night's Watch | adwd-jon-03 |
| 4145 | 1 | Successor to | `(LLM tail)` | Sigorn → His father (previous Magnar of Thenn) | adwd-jon-03 |
| 4146 | 1 | Knew briefly / respected | `RESPECTS` | Jon Snow → Tyrion Lannister | adwd-jon-03 |
| 4147 | 1 | Serves (Lord Commander) | `SERVES` | Jon Snow → Night's Watch | adwd-jon-04 |
| 4148 | 1 | Advises (Lord Steward) | `ADVISES` | Bowen Marsh → Jon Snow | adwd-jon-04 |
| 4149 | 1 | Serves/companions | `SERVES` | Dolorous Edd → Jon Snow | adwd-jon-04 |
| 4150 | 1 | Attempts to recruit/elevate | `(LLM tail)` | Stannis → Jon Snow | adwd-jon-04 |
| 4151 | 1 | Refuses fealty to | `(LLM tail)` | Jon Snow → Stannis | adwd-jon-04 |
| 4152 | 1 | Advises (strategic) | `ADVISES` | Jon Snow → Stannis | adwd-jon-04 |
| 4153 | 1 | Controls/binds | `COMMANDS` | Melisandre → Rattleshirt | adwd-jon-04 |
| 4154 | 1 | Gives (as gift) | `(LLM tail)` | Stannis → Rattleshirt (to Jon) | adwd-jon-04 |
| 4155 | 1 | Antagonizes/disrespects | `OPPOSES` | Ser Godry → Jon Snow | adwd-jon-04 |
| 4156 | 1 | Defends/mediates | `PROTECTS` | Ser Justin Massey → Jon Snow | adwd-jon-04 |
| 4157 | 1 | Won't fight | `(LLM tail)` | Mors Umber → Hother Umber | adwd-jon-04 |
| 4158 | 1 | Claims belongs to (Winterfell) | `(LLM tail)` | Jon Snow → Sansa Stark | adwd-jon-04 |
| 4159 | 1 | Plans campaign against | `(LLM tail)` | Stannis → Boltons | adwd-jon-04 |
| 4160 | 1 | Aspires to win | `(LLM tail)` | Ser Justin Massey → Val | adwd-jon-04 |
| 4161 | 1 | Disagree with | `(LLM tail)` | Night's Watch rangers → Bowen Marsh | adwd-jon-04 |
| 4162 | 1 | Blames/resents | `OPPOSES` | Stannis → King's men from Dragonstone | adwd-jon-04 |
| 4163 | 1 | Feels grudge from (childhood) | `(LLM tail)` | Jon Snow → Lysa Arryn | adwd-jon-04 |
| 4164 | 1 | Conflicts with | `(LLM tail)` | Jon Snow → Bowen Marsh | adwd-jon-05 |
| 4165 | 1 | Mourns / misses | `MOURNS` | Jon Snow → Maester Aemon | adwd-jon-05 |
| 4166 | 1 | Remembers / respects | `RESPECTS` | Jon Snow → Mance Rayder | adwd-jon-05 |
| 4167 | 1 | Sibling of | `SIBLING_OF` | Halleck → Harma Dogshead | adwd-jon-05 |
| 4168 | 1 | Frustrated by | `(LLM tail)` | Jon Snow → Othell Yarwyck | adwd-jon-05 |
| 4169 | 1 | Commander sending on dangerous mission | `COMMANDS` | Jon Snow → Ser Alliser Thorne | adwd-jon-06 |
| 4170 | 1 | Antagonistic toward / hostile to | `OPPOSES` | Ser Alliser Thorne → Jon Snow | adwd-jon-06 |
| 4171 | 1 | Acknowledges as brother despite dislike | `SIBLING_OF` | Jon Snow → Ser Alliser Thorne | adwd-jon-06 |
| 4172 | 1 | Mentor/trainer to | `TUTORS` | Jon Snow → Arron, Emrick, Jace | adwd-jon-06 |
| 4173 | 1 | Combative challenger to | `(LLM tail)` | Rattleshirt → Jon Snow | adwd-jon-06 |
| 4174 | 1 | Protective of / loyal to | `PROTECTS` | Iron Emmett → Jon Snow | adwd-jon-06 |
| 4175 | 1 | Bonded companion to | `COMPANION_OF` | Ghost → Jon Snow | adwd-jon-06 |
| 4176 | 1 | Unusually warm toward | `(LLM tail)` | Ghost → Melisandre | adwd-jon-06 |
| 4177 | 1 | Seeks alliance with / offers help to | `SEEKS` | Melisandre → Jon Snow | adwd-jon-06 |
| 4178 | 1 | Protective love for | `LOVES` | Jon Snow → Arya Stark | adwd-jon-06 |
| 4179 | 1 | Guilt toward / mourning for | `MOURNS` | Jon Snow → Benjen Stark | adwd-jon-06 |
| 4180 | 1 | Nostalgic for | `(LLM tail)` | Jon Snow → Robb Stark | adwd-jon-06 |
| 4181 | 1 | Respects teaching of | `RESPECTS` | Jon Snow → Ser Rodrik Cassel | adwd-jon-06 |
| 4182 | 1 | Complex resentment toward | `(LLM tail)` | Jon Snow → Lady Catelyn | adwd-jon-06 |
| 4183 | 1 | Claims marriage to | `(LLM tail)` | Ramsay Bolton → Arya Stark | adwd-jon-06 |
| 4184 | 1 | Political authority over Northern lords | `(LLM tail)` | Roose Bolton → Lord Dustin, Lady Cerwyn, Ryswells, House Umber | adwd-jon-06 |
| 4185 | 1 | Loyal/humorous companion to | `COMPANION_OF` | Dolorous Edd → Jon Snow | adwd-jon-06 |
| 4186 | 1 | respects / works with | `RESPECTS` | Jon Snow → Iron Emmett | adwd-jon-07 |
| 4187 | 1 | remembers / learned from | `(LLM tail)` | Jon Snow → Ygritte | adwd-jon-07 |
| 4188 | 1 | loves / fears for | `LOVES` | Jon Snow → Arya Stark | adwd-jon-07 |
| 4189 | 1 | identifies with / honors | `(LLM tail)` | Jon Snow → Eddard Stark | adwd-jon-07 |
| 4190 | 1 | grudgingly admires but distrusts | `RESPECTS` | Jon Snow → Mance Rayder | adwd-jon-07 |
| 4191 | 1 | distrusts (inherited) | `DISTRUSTS` | Jon Snow → Roose Bolton | adwd-jon-07 |
| 4192 | 1 | strategically regards | `(LLM tail)` | Jon Snow → Stannis Baratheon | adwd-jon-07 |
| 4193 | 1 | mourns / honors | `MOURNS` | Jon Snow → Donal Noye | adwd-jon-07 |
| 4194 | 1 | mediates between | `(LLM tail)` | Leathers → Jon Snow and the giant | adwd-jon-07 |
| 4195 | 1 | fear | `FEARS` | Wildlings (grove) → Night's Watch | adwd-jon-07 |
| 4196 | 1 | allied with / commands | `ALLIES_WITH` | Stannis Baratheon → Mountain clans (Flint, Norrey, Wull, Liddle) | adwd-jon-07 |
| 4197 | 1 | admired as a boy | `RESPECTS` | Jon Snow → Daeron I (the Young Dragon) | adwd-jon-07 |
| 4198 | 1 | sends on mission / trusts | `(LLM tail)` | Jon Snow → Val | adwd-jon-08 |
| 4199 | 1 | respects / cooperates with | `RESPECTS` | Val → Jon Snow | adwd-jon-08 |
| 4200 | 1 | broke promise to | `(LLM tail)` | Jon Snow → Stannis | adwd-jon-08 |
| 4201 | 1 | opposes / resents | `OPPOSES` | Bowen Marsh → Jon Snow | adwd-jon-08 |
| 4202 | 1 | uncomfortable deference to | `(LLM tail)` | Othell Yarwyck → Jon Snow | adwd-jon-08 |
| 4203 | 1 | values as ally | `ALLIES_WITH` | Jon Snow → Wun Wun | adwd-jon-08 |
| 4204 | 1 | inquired about death of | `(LLM tail)` | Val → Jarl | adwd-jon-08 |
| 4205 | 1 | steals from | `(LLM tail)` | Mormont's raven → Jon Snow | adwd-jon-08 |
| 4206 | 1 | offers alliance to (via Val) | `ALLIES_WITH` | Jon Snow → Tormund Giantsbane | adwd-jon-08 |
| 4207 | 1 | kinsman/Queen's Hand to | `(LLM tail)` | Ser Axell Florent → Queen Selyse | adwd-jon-09 |
| 4208 | 1 | true allegiance of queen's men | `(LLM tail)` | Melisandre → Queen's men | adwd-jon-09 |
| 4209 | 1 | guest/ward of | `(LLM tail)` | Wun Wun → Night's Watch | adwd-jon-09 |
| 4210 | 1 | fool to | `(LLM tail)` | Patchface → Princess Shireen | adwd-jon-09 |
| 4211 | 1 | fled from / opposes | `(LLM tail)` | Alys Karstark → Arnolf Karstark & Cregan Karstark | adwd-jon-09 |
| 4212 | 1 | plans to betray | `(LLM tail)` | Arnolf Karstark → Stannis Baratheon | adwd-jon-09 |
| 4213 | 1 | pursuing | `(LLM tail)` | Cregan Karstark → Alys Karstark | adwd-jon-09 |
| 4214 | 1 | formerly betrothed to | `BETROTHED_TO` | Alys Karstark → Daryn Hornwood | adwd-jon-09 |
| 4215 | 1 | creditor to | `(LLM tail)` | Iron Bank → Iron Throne / Robert Baratheon | adwd-jon-09 |
| 4216 | 1 | potential supporter of | `(LLM tail)` | Iron Bank → Stannis Baratheon | adwd-jon-09 |
| 4217 | 1 | Gives away in marriage | `(LLM tail)` | Jon Snow → Alys Karstark | adwd-jon-10 |
| 4218 | 1 | Warm rapport / protective | `(LLM tail)` | Jon Snow → Alys Karstark | adwd-jon-10 |
| 4219 | 1 | Disdainful toward | `HATES` | Ser Malegorn → Satin | adwd-jon-10 |
| 4220 | 1 | Hostile/aggressive | `(LLM tail)` | Ser Patrek → General | adwd-jon-10 |
| 4221 | 1 | Adversarial / captor | `CAPTURES` | Jon Snow → Cregan Karstark | adwd-jon-10 |
| 4222 | 1 | Hostile contempt toward | `(LLM tail)` | Cregan Karstark → Jon Snow | adwd-jon-10 |
| 4223 | 1 | Claims right to | `(LLM tail)` | Cregan Karstark → Alys Karstark | adwd-jon-10 |
| 4224 | 1 | Politically allied with | `ALLIES_WITH` | Jon Snow → Old Flint / The Norrey | adwd-jon-10 |
| 4225 | 1 | Warns / watches over | `ADVISES` | Melisandre → Jon Snow | adwd-jon-10 |
| 4226 | 1 | Pressures / manipulates | `(LLM tail)` | Ser Axell Florent → Jon Snow | adwd-jon-10 |
| 4227 | 1 | Wet nurses provided for | `(LLM tail)` | Old Flint / Norrey → Monster (Mance's child) | adwd-jon-10 |
| 4228 | 1 | Former antagonist to | `(LLM tail)` | Glendon Hewett → Jon Snow | adwd-jon-10 |
| 4229 | 1 | Childhood acquaintance | `(LLM tail)` | Alys Karstark → Jon Snow (and Robb) | adwd-jon-10 |
| 4230 | 1 | Negotiating partner / mutual respect | `RESPECTS` | Jon Snow → Tormund Giantsbane | adwd-jon-11 |
| 4231 | 1 | Commander (reluctant political subordinate) | `COMMANDS` | Jon Snow → Queen Selyse | adwd-jon-11 |
| 4232 | 1 | Attraction (suppressed) | `(LLM tail)` | Jon Snow → Val | adwd-jon-11 |
| 4233 | 1 | Antagonistic | `OPPOSES` | Jon Snow → Bowen Marsh | adwd-jon-11 |
| 4234 | 1 | Wary respect | `RESPECTS` | Jon Snow → The Norrey / Old Flint | adwd-jon-11 |
| 4235 | 1 | Bonded | `BONDED_TO` | Jon Snow → Ghost | adwd-jon-11 |
| 4236 | 1 | Grief | `MOURNS` | Tormund → Dormund, Torwynd (dead sons) | adwd-jon-11 |
| 4237 | 1 | Love/pride | `LOVES` | Tormund → Munda (daughter) | adwd-jon-11 |
| 4238 | 1 | Father-in-law (grudging) | `IN_LAW_OF` | Tormund → Longspear Ryk | adwd-jon-11 |
| 4239 | 1 | Loyalty/debt | `(LLM tail)` | Val → Jon Snow | adwd-jon-11 |
| 4240 | 1 | Protective/horror | `(LLM tail)` | Val → Shireen Baratheon | adwd-jon-11 |
| 4241 | 1 | Warm | `(LLM tail)` | Val → Ghost | adwd-jon-11 |
| 4242 | 1 | Condescension | `(LLM tail)` | Queen Selyse → Val | adwd-jon-11 |
| 4243 | 1 | Anxiety | `(LLM tail)` | Queen Selyse → Ghost / Wun Wun | adwd-jon-11 |
| 4244 | 1 | Friendly/curious | `COMPANION_OF` | Shireen → Val | adwd-jon-11 |
| 4245 | 1 | Gallant/attracted | `(LLM tail)` | Ser Patrek → Val | adwd-jon-11 |
| 4246 | 1 | Opposition (reluctant compliance) | `(LLM tail)` | Othell Yarwyck → Jon Snow | adwd-jon-11 |
| 4247 | 1 | Loyalty/defense | `(LLM tail)` | Leathers → Jon Snow | adwd-jon-11 |
| 4248 | 1 | Grudging acceptance | `(LLM tail)` | Old Flint → Jon Snow | adwd-jon-11 |
| 4249 | 1 | Tests Jon's resolve | `(LLM tail)` | The Norrey → Jon Snow | adwd-jon-11 |
| 4250 | 1 | Cautious alliance with | `ALLIES_WITH` | Jon Snow → Tormund Giantsbane | adwd-jon-12 |
| 4251 | 1 | Bond with (direwolf) | `(LLM tail)` | Jon Snow → Ghost | adwd-jon-12 |
| 4252 | 1 | Takes as page | `(LLM tail)` | Jon Snow → Dryn | adwd-jon-12 |
| 4253 | 1 | Guilt toward (dream) | `(LLM tail)` | Jon Snow → Robb Stark | adwd-jon-12 |
| 4254 | 1 | Distrusts (some) | `DISTRUSTS` | Jon Snow → His own brothers | adwd-jon-12 |
| 4255 | 1 | Nostalgic kinship with | `(LLM tail)` | Jon Snow → Bran, Arya, Robb | adwd-jon-12 |
| 4256 | 1 | Respect/adversarial warmth toward | `RESPECTS` | Tormund → Jon Snow | adwd-jon-12 |
| 4257 | 1 | Stiff obedience toward | `(LLM tail)` | Bowen Marsh → Jon Snow | adwd-jon-12 |
| 4258 | 1 | Cryptic kinship claim toward | `(LLM tail)` | Borroq → Jon Snow | adwd-jon-12 |
| 4259 | 1 | Offers service to | `(LLM tail)` | Soren Shieldbreaker → Jon Snow | adwd-jon-12 |
| 4260 | 1 | Reports to / requests help from | `(LLM tail)` | Cotter Pyke → Jon Snow | adwd-jon-12 |
| 4261 | 1 | Allied with / trusts | `ALLIES_WITH` | Jon Snow → Tormund Giantsbane | adwd-jon-13 |
| 4262 | 1 | Dismissive of / antagonistic toward | `DISTRUSTS` | Queen Selyse → Jon Snow | adwd-jon-13 |
| 4263 | 1 | Advises / warns | `ADVISES` | Melisandre → Jon Snow | adwd-jon-13 |
| 4264 | 1 | Used by | `(LLM tail)` | Gerrick Kingsblood → Queen Selyse | adwd-jon-13 |
| 4265 | 1 | Unsettles | `(LLM tail)` | Borroq → Jon Snow / Castle Black | adwd-jon-13 |
| 4266 | 1 | Commands (prisoner) | `COMMANDS` | Jon Snow → Cregan Karstark | adwd-jon-13 |
| 4267 | 1 | seeks to manipulate/win trust of | `SEEKS` | Melisandre → Jon Snow | adwd-melisandre-01 |
| 4268 | 1 | half in love with / fears / worships | `LOVES` | Devan Seaworth → Melisandre | adwd-melisandre-01 |
| 4269 | 1 | protects (secretly) | `PROTECTS` | Melisandre → Devan Seaworth | adwd-melisandre-01 |
| 4270 | 1 | controls via glamor magic | `COMMANDS` | Melisandre → Mance Rayder | adwd-melisandre-01 |
| 4271 | 1 | owes life to / grudgingly cooperates with | `(LLM tail)` | Mance Rayder → Melisandre | adwd-melisandre-01 |
| 4272 | 1 | owes life to | `(LLM tail)` | Mance Rayder → Jon Snow | adwd-melisandre-01 |
| 4273 | 1 | disagrees with/resents | `(LLM tail)` | Bowen Marsh → Jon Snow | adwd-melisandre-01 |
| 4274 | 1 | commands/silences | `COMMANDS` | Jon Snow → Bowen Marsh | adwd-melisandre-01 |
| 4275 | 1 | clashed with | `(LLM tail)` | Mance (as Rattleshirt) → Bowen Marsh | adwd-melisandre-01 |
| 4276 | 1 | interprets as enemy's servants | `(LLM tail)` | Melisandre → The wooden-faced man and wolf-faced boy | adwd-melisandre-01 |
| 4277 | 1 | sees as doomed people | `PERCEIVED_AS` | Melisandre → The free folk/wildlings | adwd-melisandre-01 |
| 4278 | 1 | bound by vows regarding | `(LLM tail)` | Jon Snow → Arya Stark | adwd-melisandre-01 |
| 4279 | 1 | feels no fear for herself | `FEARS` | Melisandre → R'hllor | adwd-melisandre-01 |
| 4280 | 1 | master/controller of | `(LLM tail)` | Varamyr → One Eye, Stalker, Sly | adwd-prologue |
| 4281 | 1 | killed and consumed | `KILLS` | Varamyr → Haggon | adwd-prologue |
| 4282 | 1 | stole beast from | `(LLM tail)` | Varamyr → Haggon | adwd-prologue |
| 4283 | 1 | served/followed | `(LLM tail)` | Varamyr → Mance Rayder | adwd-prologue |
| 4284 | 1 | last companion of | `COMPANION_OF` | Varamyr → Thistle | adwd-prologue |
| 4285 | 1 | lied to | `(LLM tail)` | Varamyr → Thistle | adwd-prologue |
| 4286 | 1 | attempted to seize body of | `(LLM tail)` | Varamyr → Thistle | adwd-prologue |
| 4287 | 1 | killed (accidentally via warging) | `KILLS` | Varamyr (as Lump) → Bump | adwd-prologue |
| 4288 | 1 | gave away | `GIFTED_TO` | Varamyr's father → Varamyr | adwd-prologue |
| 4289 | 1 | rejected | `(LLM tail)` | Varamyr's mother → Varamyr | adwd-prologue |
| 4290 | 1 | hated | `(LLM tail)` | Orell (in eagle) → Jon Snow | adwd-prologue |
| 4291 | 1 | recognized gift in | `(LLM tail)` | Varamyr → Jon Snow | adwd-prologue |
| 4292 | 1 | mates with | `(LLM tail)` | One Eye → Sly | adwd-prologue |
| 4293 | 1 | former controller of | `(LLM tail)` | Varamyr → Shadowcat, snow bear, eagle (Orell's) | adwd-prologue |
| 4294 | 1 | terror/exploitation of | `(LLM tail)` | Varamyr → Village women | adwd-prologue |
| 4295 | 1 | Captor / torturer | `CAPTURES` | Ramsay Bolton → Reek | adwd-reek-01 |
| 4296 | 1 | Captive / forced servant | `(LLM tail)` | Reek → Ramsay Bolton | adwd-reek-01 |
| 4297 | 1 | Son (legitimized) | `(LLM tail)` | Ramsay Bolton → Lord Roose Bolton | adwd-reek-01 |
| 4298 | 1 | Betrothed | `BETROTHED_TO` | Ramsay Bolton → Arya Stark | adwd-reek-01 |
| 4299 | 1 | Arranging marriage for | `(LLM tail)` | Lord Roose Bolton → Ramsay Bolton | adwd-reek-01 |
| 4300 | 1 | Married and killed | `(LLM tail)` | Ramsay Bolton → Lady Hornwood | adwd-reek-01 |
| 4301 | 1 | Attempted escape with | `(LLM tail)` | Reek → Kyra | adwd-reek-01 |
| 4302 | 1 | Hunted and punished | `(LLM tail)` | Ramsay Bolton → Kyra | adwd-reek-01 |
| 4303 | 1 | Kennel master for | `(LLM tail)` | Ben Bones → Ramsay Bolton | adwd-reek-01 |
| 4304 | 1 | Punished by | `(LLM tail)` | Grunt → Lord Roose Bolton | adwd-reek-01 |
| 4305 | 1 | Retainers / favorites of | `(LLM tail)` | The Bastard's Boys → Ramsay Bolton | adwd-reek-01 |
| 4306 | 1 | Guest of, hostile toward Reek | `(LLM tail)` | Mail-byrnie lord → Ramsay Bolton | adwd-reek-01 |
| 4307 | 1 | Slave/creature of | `(LLM tail)` | Reek → Ramsay Bolton | adwd-reek-02 |
| 4308 | 1 | Psychological dominion over | `(LLM tail)` | Ramsay Bolton → Reek | adwd-reek-02 |
| 4309 | 1 | Natural son of | `(LLM tail)` | Ramsay Bolton → Roose Bolton | adwd-reek-02 |
| 4310 | 1 | Recognizes true identity of | `(LLM tail)` | Reek → Jeyne Poole | adwd-reek-02 |
| 4311 | 1 | Mercy-kills | `(LLM tail)` | Reek → Ralf Kenning | adwd-reek-02 |
| 4312 | 1 | Defeated (at kingsmoot) | `(LLM tail)` | Euron Greyjoy → Victarion Greyjoy | adwd-reek-02 |
| 4313 | 1 | Distrusts/fears assassination | `DISTRUSTS` | Roose Bolton → Crannogmen (implied) | adwd-reek-02 |
| 4314 | 1 | Former acquaintance of | `(LLM tail)` | Reek → Robb Stark | adwd-reek-02 |
| 4315 | 1 | Former antagonist of | `(LLM tail)` | Reek → Roose Bolton | adwd-reek-02 |
| 4316 | 1 | Friend of (posed identity) | `COMPANION_OF` | Jeyne Poole → Sansa Stark | adwd-reek-02 |
| 4317 | 1 | Dominates/owns | `(LLM tail)` | Ramsay Bolton → Reek (Theon) | adwd-reek-03 |
| 4318 | 1 | Father, controls | `(LLM tail)` | Roose Bolton → Ramsay Bolton | adwd-reek-03 |
| 4319 | 1 | Resents authority of | `RESENTS` | Ramsay Bolton → Roose Bolton | adwd-reek-03 |
| 4320 | 1 | Distanced from | `(LLM tail)` | Big Walder → Little Walder / Ramsay | adwd-reek-03 |
| 4321 | 1 | Cannot abide | `(LLM tail)` | Lady Barbrey Dustin → Ramsay Bolton | adwd-reek-03 |
| 4322 | 1 | Holds grudge against | `(LLM tail)` | Lady Barbrey Dustin → Ned Stark (deceased) | adwd-reek-03 |
| 4323 | 1 | Oddly fond of | `LOVES` | Roose Bolton → Lady Walda Bolton | adwd-reek-03 |
| 4324 | 1 | Married (past, deceased) | `(LLM tail)` | Roose Bolton → Roose's second wife | adwd-reek-03 |
| 4325 | 1 | Controls through gifts | `COMMANDS` | Roose Bolton → Ramsay's mother | adwd-reek-03 |
| 4326 | 1 | Inseparable from (past) | `(LLM tail)` | Ramsay Bolton → The first Reek | adwd-reek-03 |
| 4327 | 1 | Admires (grudgingly) | `RESPECTS` | Roose Bolton → Domeric Bolton | adwd-reek-03 |
| 4328 | 1 | Suspects betrayal from | `(LLM tail)` | Roose Bolton → Lord Wyman Manderly | adwd-reek-03 |
| 4329 | 1 | Serves as agent for | `SERVES` | Arnolf Karstark → Roose Bolton | adwd-reek-03 |
| 4330 | 1 | Trusts (slightly) | `TRUSTS` | Ben Bones → Reek | adwd-reek-03 |
| 4331 | 1 | Coerced by | `(LLM tail)` | Harwood Stout → Ramsay Bolton | adwd-reek-03 |
| 4332 | 1 | Warging ability | `WARGS_INTO` | Arya → The tomcat | adwd-the-blind-girl-01 |
| 4333 | 1 | Love/longing | `LOVES` | Arya → Jon Snow | adwd-the-blind-girl-01 |
| 4334 | 1 | Affection (memory) | `LOVES` | Arya → Eddard Stark | adwd-the-blind-girl-01 |
| 4335 | 1 | Resentment (memory) | `RESENTS` | Arya → Sansa and friends | adwd-the-blind-girl-01 |
| 4336 | 1 | Hatred/kill list | `HATES` | Arya → Ser Gregor, Dunsen, Raff, Ser Ilyn, Ser Meryn, Cersei | adwd-the-blind-girl-01 |
| 4337 | 1 | Justified killing | `(LLM tail)` | Arya → Dareon | adwd-the-blind-girl-01 |
| 4338 | 1 | Kindness/charity | `(LLM tail)` | Pynto → Blind Beth (Arya) | adwd-the-blind-girl-01 |
| 4339 | 1 | Recognition/affection | `LOVES` | The cat → Arya | adwd-the-blind-girl-01 |
| 4340 | 1 | Pack leader | `(LLM tail)` | Nymeria → Her grey cousins (wolf pack) | adwd-the-blind-girl-01 |
| 4341 | 1 | Tests/challenges | `(LLM tail)` | The kindly man → Arya | adwd-the-blind-girl-01 |
| 4342 | 1 | Enslaved | `(LLM tail)` | Lyseni pirates → Wildling women and children | adwd-the-blind-girl-01 |
| 4343 | 1 | Protector / sworn to | `(LLM tail)` | Barristan Selmy → Daenerys Targaryen | adwd-the-discarded-knight-01 |
| 4344 | 1 | Sworn Brother (former) | `SIBLING_OF` | Barristan Selmy → Prince Lewyn Martell | adwd-the-discarded-knight-01 |
| 4345 | 1 | Respect for | `RESPECTS` | Barristan Selmy → Daenerys Targaryen | adwd-the-discarded-knight-01 |
| 4346 | 1 | King / husband of | `(LLM tail)` | Hizdahr zo Loraq → Daenerys Targaryen | adwd-the-discarded-knight-01 |
| 4347 | 1 | Suspicion / displeasure toward | `(LLM tail)` | Hizdahr zo Loraq → Quentyn Martell | adwd-the-discarded-knight-01 |
| 4348 | 1 | Paramour | `(LLM tail)` | Daenerys Targaryen → Daario Naharis | adwd-the-discarded-knight-01 |
| 4349 | 1 | Captain of | `(LLM tail)` | Daario Naharis → Stormcrows | adwd-the-discarded-knight-01 |
| 4350 | 1 | Wife and family in | `(LLM tail)` | Groleo → Pentos | adwd-the-discarded-knight-01 |
| 4351 | 1 | Protectors of | `(LLM tail)` | Goghor, Spotted Cat, Belaquo, Khrazz → Hizdahr zo Loraq | adwd-the-discarded-knight-01 |
| 4352 | 1 | Showed mercy to | `(LLM tail)` | Prince Duncan (Prince of Dragonflies) → Young Barristan | adwd-the-discarded-knight-01 |
| 4353 | 1 | Provided equipment to | `(LLM tail)` | Lord Dondarrion → Young Barristan | adwd-the-discarded-knight-01 |
| 4354 | 1 | Sellsword accompanying | `(LLM tail)` | Bloodbeard → Yunkish delegation | adwd-the-discarded-knight-01 |
| 4355 | 1 | Desires/pursues | `(LLM tail)` | Quentyn Martell → Daenerys Targaryen | adwd-the-dragontamer-01 |
| 4356 | 1 | Led by / sent by father | `(LLM tail)` | Quentyn Martell → Doran Martell | adwd-the-dragontamer-01 |
| 4357 | 1 | Friendship (strained) | `COMPANION_OF` | Quentyn Martell → Gerris Drinkwater | adwd-the-dragontamer-01 |
| 4358 | 1 | Friendship/reliance | `COMPANION_OF` | Quentyn Martell → Archibald Yronwood | adwd-the-dragontamer-01 |
| 4359 | 1 | Misses / regrets not visiting | `MOURNS` | Quentyn Martell → His mother (Norvoshi wife of Doran) | adwd-the-dragontamer-01 |
| 4360 | 1 | Protective of / fights for | `PROTECTS` | Archibald Yronwood → Quentyn Martell | adwd-the-dragontamer-01 |
| 4361 | 1 | Unhappy marriage | `(LLM tail)` | Doran Martell → His Norvoshi wife (Quentyn's mother) | adwd-the-dragontamer-01 |
| 4362 | 1 | Has paramour | `(LLM tail)` | Daenerys Targaryen → Unnamed (paramour) | adwd-the-dragontamer-01 |
| 4363 | 1 | Serves under / allied with | `SERVES` | Pretty Meris → Tattered Prince | adwd-the-dragontamer-01 |
| 4364 | 1 | former Hand to / devoted to memory of | `(LLM tail)` | Jon Connington → Rhaegar Targaryen | adwd-the-griffin-reborn-01 |
| 4365 | 1 | lord of (reclaimed) | `(LLM tail)` | Jon Connington → Griffin's Roost | adwd-the-griffin-reborn-01 |
| 4366 | 1 | disdains / finds inadequate | `HATES` | Jon Connington → Homeless Harry Strickland | adwd-the-griffin-reborn-01 |
| 4367 | 1 | doubts worthiness of | `(LLM tail)` | Jon Connington → Ser Rolly Duckfield | adwd-the-griffin-reborn-01 |
| 4368 | 1 | kinsman / captor of | `CAPTURES` | Jon Connington → Raymund, Alynne, Ronald Storm | adwd-the-griffin-reborn-01 |
| 4369 | 1 | cousin of (deceased) | `COUSIN_OF` | Jon Connington → Ser Ronald Connington | adwd-the-griffin-reborn-01 |
| 4370 | 1 | opposed / failed to capture | `(LLM tail)` | Jon Connington → Robert Baratheon | adwd-the-griffin-reborn-01 |
| 4371 | 1 | recalls advice from | `(LLM tail)` | Jon Connington → Myles Toyne (Blackheart) | adwd-the-griffin-reborn-01 |
| 4372 | 1 | disparages (in memory) | `(LLM tail)` | Jon Connington → Princess Elia | adwd-the-griffin-reborn-01 |
| 4373 | 1 | insists on keeping | `(LLM tail)` | Prince Aegon → Ser Rolly Duckfield as Kingsguard | adwd-the-griffin-reborn-01 |
| 4374 | 1 | asserts authority over | `(LLM tail)` | Prince Aegon → Jon Connington | adwd-the-griffin-reborn-01 |
| 4375 | 1 | opposes (strategically) | `OPPOSES` | Homeless Harry Strickland → Jon Connington | adwd-the-griffin-reborn-01 |
| 4376 | 1 | suggests alliance with | `ALLIES_WITH` | Ser Brendel Byrne → Stannis Baratheon | adwd-the-griffin-reborn-01 |
| 4377 | 1 | counsels / proposes to | `ADVISES` | Haldon Halfmaester → Jon Connington | adwd-the-griffin-reborn-01 |
| 4378 | 1 | fighting alongside | `(LLM tail)` | Ronnet Connington (Red Ronnet) → Jaime Lannister | adwd-the-griffin-reborn-01 |
| 4379 | 1 | led assault on | `(LLM tail)` | Franklyn Flowers → Griffin's Roost | adwd-the-griffin-reborn-01 |
| 4380 | 1 | prescribed treatment for | `(LLM tail)` | Lady Lemore → Greyscale (via Jon Connington) | adwd-the-griffin-reborn-01 |
| 4381 | 1 | Bitter rival/brother of | `SIBLING_OF` | Victarion → Euron Greyjoy | adwd-the-iron-suitor-01 |
| 4382 | 1 | Subordinate to (resentfully) | `SERVES` | Victarion → Euron Greyjoy | adwd-the-iron-suitor-01 |
| 4383 | 1 | Uses/confides in | `(LLM tail)` | Victarion → Dusky woman | adwd-the-iron-suitor-01 |
| 4384 | 1 | Strikes/disciplines | `(LLM tail)` | Victarion → Ralf the Limper | adwd-the-iron-suitor-01 |
| 4385 | 1 | Trust/alliance with | `ALLIES_WITH` | Victarion → Moqorro | adwd-the-iron-suitor-01 |
| 4386 | 1 | Gave (as gift/burden) to | `GIFTED_TO` | Euron → Victarion | adwd-the-iron-suitor-01 |
| 4387 | 1 | Gave (as imposed maester) to | `GIFTED_TO` | Euron → Victarion | adwd-the-iron-suitor-01 |
| 4388 | 1 | Stole from | `(LLM tail)` | Euron → Victarion | adwd-the-iron-suitor-01 |
| 4389 | 1 | Won kingsmoot over | `(LLM tail)` | Euron → Victarion and Aeron | adwd-the-iron-suitor-01 |
| 4390 | 1 | Healer/priest to | `(LLM tail)` | Moqorro → Victarion | adwd-the-iron-suitor-01 |
| 4391 | 1 | Previously assaulted | `(LLM tail)` | Burton Humble → Maester Kerwin | adwd-the-iron-suitor-01 |
| 4392 | 1 | Sexually assaulted | `(LLM tail)` | Four unnamed crewmen → Maester Kerwin | adwd-the-iron-suitor-01 |
| 4393 | 1 | Killed (recalled) | `KILLS` | Victarion → Serry | adwd-the-iron-suitor-01 |
| 4394 | 1 | Uneasy co-conspirator with | `CONSPIRES_WITH` | Barristan → Skahaz mo Kandaq | adwd-the-kingbreaker-01 |
| 4395 | 1 | Suspects/arrests | `(LLM tail)` | Barristan → Hizdahr zo Loraq | adwd-the-kingbreaker-01 |
| 4396 | 1 | Disapproves of but defends | `(LLM tail)` | Barristan → Daario Naharis | adwd-the-kingbreaker-01 |
| 4397 | 1 | Mentor to | `TUTORS` | Barristan → Tumco Lho, Larraq, Red Lamb | adwd-the-kingbreaker-01 |
| 4398 | 1 | Warns/protects | `ADVISES` | Barristan → Missandei | adwd-the-kingbreaker-01 |
| 4399 | 1 | Loved (unrequited) | `LOVES` | Barristan → Ashara Dayne | adwd-the-kingbreaker-01 |
| 4400 | 1 | Served but was not fully trusted by | `(LLM tail)` | Barristan → Rhaegar Targaryen | adwd-the-kingbreaker-01 |
| 4401 | 1 | Claims control over | `(LLM tail)` | Skahaz → Brazen Beasts | adwd-the-kingbreaker-01 |
| 4402 | 1 | Plans to imprison | `IMPRISONS` | Skahaz → Marghaz zo Loraq | adwd-the-kingbreaker-01 |
| 4403 | 1 | Consort/king to | `(LLM tail)` | Hizdahr → Daenerys | adwd-the-kingbreaker-01 |
| 4404 | 1 | Consults with | `(LLM tail)` | Hizdahr → Reznak, Marghaz, Galazza Galare | adwd-the-kingbreaker-01 |
| 4405 | 1 | Chose/loved | `LOVES` | Rhaegar → Lyanna Stark | adwd-the-kingbreaker-01 |
| 4406 | 1 | Rival lover with | `LOVER_OF` | Bittersteel → Bloodraven | adwd-the-kingbreaker-01 |
| 4407 | 1 | Father who allowed sons' love matches | `LOVES` | Aegon V → His three sons | adwd-the-kingbreaker-01 |
| 4408 | 1 | Shares doubts with | `(LLM tail)` | Marselen → Barristan | adwd-the-kingbreaker-01 |
| 4409 | 1 | Prisoner/hostage of | `(LLM tail)` | Asha Greyjoy → Stannis Baratheon | adwd-the-kings-prize-01 |
| 4410 | 1 | Dismisses/rejects | `(LLM tail)` | Stannis Baratheon → Asha Greyjoy | adwd-the-kings-prize-01 |
| 4411 | 1 | Cautious rapport with | `(LLM tail)` | Asha Greyjoy → Alysane Mormont | adwd-the-kings-prize-01 |
| 4412 | 1 | Courts/is attracted to | `(LLM tail)` | Justin Massey → Asha Greyjoy | adwd-the-kings-prize-01 |
| 4413 | 1 | Tolerates for advantage | `(LLM tail)` | Asha Greyjoy → Justin Massey | adwd-the-kings-prize-01 |
| 4414 | 1 | Recalls wisdom of | `(LLM tail)` | Asha Greyjoy → Balon Greyjoy | adwd-the-kings-prize-01 |
| 4415 | 1 | Accuses/distrusts | `(LLM tail)` | Lord Peasebury → Big Bucket Wull | adwd-the-kings-prize-01 |
| 4416 | 1 | Insist on marching for | `(LLM tail)` | Northmen (clansmen) → "Ned's girl" / Eddard Stark's memory | adwd-the-kings-prize-01 |
| 4417 | 1 | Oppose/resent | `(LLM tail)` | Southron lords → Northern clansmen | adwd-the-kings-prize-01 |
| 4418 | 1 | Push for sacrifice from | `(LLM tail)` | Queen's men → Stannis Baratheon | adwd-the-kings-prize-01 |
| 4419 | 1 | Refuses sacrifice from | `(LLM tail)` | Stannis Baratheon → Queen's men | adwd-the-kings-prize-01 |
| 4420 | 1 | Relies on (absent) | `(LLM tail)` | Stannis Baratheon → Melisandre | adwd-the-kings-prize-01 |
| 4421 | 1 | Admires/worships | `RESPECTS` | Harwood Fell → Robert Baratheon | adwd-the-kings-prize-01 |
| 4422 | 1 | Serves as second-in-command to | `SERVES` | Ser Richard Horpe → Stannis Baratheon | adwd-the-kings-prize-01 |
| 4423 | 1 | Recalls failure with | `(LLM tail)` | Asha Greyjoy → Theon Greyjoy | adwd-the-kings-prize-01 |
| 4424 | 1 | Surrogate father / protector | `(LLM tail)` | Jon Connington → Aegon | adwd-the-lost-lord-01 |
| 4425 | 1 | Devoted loyalty / love | `LOVES` | Jon Connington → Rhaegar Targaryen | adwd-the-lost-lord-01 |
| 4426 | 1 | Resentment / forced cooperation | `RESENTS` | Jon Connington → Varys | adwd-the-lost-lord-01 |
| 4427 | 1 | Resentment / distrust | `RESENTS` | Jon Connington → Illyrio Mopatis | adwd-the-lost-lord-01 |
| 4428 | 1 | Diminished trust | `(LLM tail)` | Jon Connington → Haldon | adwd-the-lost-lord-01 |
| 4429 | 1 | Fondness | `(LLM tail)` | Jon Connington → Lady Lemore | adwd-the-lost-lord-01 |
| 4430 | 1 | Deep friendship / grief | `MOURNS` | Jon Connington → Myles Toyne | adwd-the-lost-lord-01 |
| 4431 | 1 | Old comradeship | `(LLM tail)` | Jon Connington → Franklyn Flowers | adwd-the-lost-lord-01 |
| 4432 | 1 | Influenced by | `(LLM tail)` | Aegon → Tyrion Lannister | adwd-the-lost-lord-01 |
| 4433 | 1 | Asserts independence from | `(LLM tail)` | Aegon → Jon Connington | adwd-the-lost-lord-01 |
| 4434 | 1 | Protective caution toward | `(LLM tail)` | Lemore → Aegon | adwd-the-lost-lord-01 |
| 4435 | 1 | Reluctant allegiance | `(LLM tail)` | Harry Strickland → Aegon | adwd-the-lost-lord-01 |
| 4436 | 1 | Enthusiastic support | `(LLM tail)` | Franklyn Flowers → Aegon | adwd-the-lost-lord-01 |
| 4437 | 1 | Support / allegiance | `(LLM tail)` | Tristan Rivers → Aegon | adwd-the-lost-lord-01 |
| 4438 | 1 | Rose through the ranks under | `(LLM tail)` | Connington (past) → Myles Toyne | adwd-the-lost-lord-01 |
| 4439 | 1 | Hatred of | `HATES` | Franklyn Flowers → House Fossoway | adwd-the-lost-lord-01 |
| 4440 | 1 | Cautious assessment of | `(LLM tail)` | Strickland → Daenerys | adwd-the-lost-lord-01 |
| 4441 | 1 | Suggests deception of | `(LLM tail)` | Gorys Edoryen → The Yunkishmen | adwd-the-lost-lord-01 |
| 4442 | 1 | Claims lineage from | `(LLM tail)` | Aegon → Rhaegar and Elia | adwd-the-lost-lord-01 |
| 4443 | 1 | Intended betrothed to | `BETROTHED_TO` | Quentyn Martell → Daenerys Targaryen | adwd-the-merchants-man-01 |
| 4444 | 1 | Close companion / defers to judgment of | `COMPANION_OF` | Quentyn Martell → Gerris Drinkwater | adwd-the-merchants-man-01 |
| 4445 | 1 | Close companion of | `COMPANION_OF` | Quentyn Martell → Ser Archibald Yronwood | adwd-the-merchants-man-01 |
| 4446 | 1 | Mourns / feels the loss most keenly of | `MOURNS` | Quentyn Martell → Maester Kedry | adwd-the-merchants-man-01 |
| 4447 | 1 | Youthful infatuation with | `(LLM tail)` | Quentyn Martell → Ynys Yronwood | adwd-the-merchants-man-01 |
| 4448 | 1 | Awkward romantic history with | `(LLM tail)` | Quentyn Martell → The Drinkwater twins | adwd-the-merchants-man-01 |
| 4449 | 1 | Serves / obeys mission from | `SERVES` | Quentyn Martell → Doran Martell | adwd-the-merchants-man-01 |
| 4450 | 1 | Fears the scorn of | `FEARS` | Quentyn Martell → The Sand Snakes | adwd-the-merchants-man-01 |
| 4451 | 1 | Friend / traveling companion of | `COMPANION_OF` | Gerris Drinkwater → Quentyn Martell | adwd-the-merchants-man-01 |
| 4452 | 1 | Views as a game / does not fully grasp danger | `(LLM tail)` | Gerris Drinkwater → The mission | adwd-the-merchants-man-01 |
| 4453 | 1 | Suffers severe seasickness | `(LLM tail)` | Ser Archibald Yronwood → Ships | adwd-the-merchants-man-01 |
| 4454 | 1 | Sent | `(LLM tail)` | Doran Martell → Maester Kedry | adwd-the-merchants-man-01 |
| 4455 | 1 | Recruited for / allied with | `ALLIES_WITH` | The Windblown → Yunkai | adwd-the-merchants-man-01 |
| 4456 | 1 | forced servant / instrument | `(LLM tail)` | Theon → Roose Bolton | adwd-the-prince-of-winterfell-01 |
| 4457 | 1 | terrorized by / subjugated to | `(LLM tail)` | Theon → Ramsay Bolton | adwd-the-prince-of-winterfell-01 |
| 4458 | 1 | pity and guilt toward | `(LLM tail)` | Theon → Jeyne Poole | adwd-the-prince-of-winterfell-01 |
| 4459 | 1 | complicated former ward of | `(LLM tail)` | Theon → Eddard Stark | adwd-the-prince-of-winterfell-01 |
| 4460 | 1 | cruel husband to | `(LLM tail)` | Ramsay → Jeyne Poole | adwd-the-prince-of-winterfell-01 |
| 4461 | 1 | claims legitimacy from | `(LLM tail)` | Ramsay → House Stark | adwd-the-prince-of-winterfell-01 |
| 4462 | 1 | uses and manipulates | `(LLM tail)` | Roose Bolton → Theon | adwd-the-prince-of-winterfell-01 |
| 4463 | 1 | political schemer against | `(LLM tail)` | Roose Bolton → Stannis Baratheon | adwd-the-prince-of-winterfell-01 |
| 4464 | 1 | confidante / political observer to | `(LLM tail)` | Lady Dustin → Theon | adwd-the-prince-of-winterfell-01 |
| 4465 | 1 | potential obstacle to | `(LLM tail)` | Lady Dustin → Roose Bolton | adwd-the-prince-of-winterfell-01 |
| 4466 | 1 | outwardly loyal, inwardly hostile toward | `(LLM tail)` | Lord Manderly → Boltons and Freys | adwd-the-prince-of-winterfell-01 |
| 4467 | 1 | provider of feast to | `(LLM tail)` | Lord Manderly → Wedding guests | adwd-the-prince-of-winterfell-01 |
| 4468 | 1 | aggressive military counsel to | `ADVISES` | Ser Hosteen Frey → Roose Bolton | adwd-the-prince-of-winterfell-01 |
| 4469 | 1 | entertainer at | `(LLM tail)` | Abel (bard) → Wedding feast | adwd-the-prince-of-winterfell-01 |
| 4470 | 1 | desperate dependent on | `(LLM tail)` | Jeyne Poole → Theon | adwd-the-prince-of-winterfell-01 |
| 4471 | 1 | recalls with guilt | `(LLM tail)` | Theon → Bran and Rickon | adwd-the-prince-of-winterfell-01 |
| 4472 | 1 | Serves / protects (loyal to absent queen) | `SERVES` | Barristan Selmy → Daenerys Targaryen | adwd-the-queens-hand-01 |
| 4473 | 1 | Respects cautiously | `RESPECTS` | Barristan Selmy → Archibald Yronwood | adwd-the-queens-hand-01 |
| 4474 | 1 | Antagonizes / disrespects | `OPPOSES` | Skahaz mo Kandaq → Barristan Selmy | adwd-the-queens-hand-01 |
| 4475 | 1 | Blames / resents | `OPPOSES` | Gerris Drinkwater → Daenerys Targaryen | adwd-the-queens-hand-01 |
| 4476 | 1 | Loyal to (in death) | `SERVES` | Archibald Yronwood → Quentyn Martell | adwd-the-queens-hand-01 |
| 4477 | 1 | Dominates / silences | `(LLM tail)` | Archibald Yronwood → Gerris Drinkwater | adwd-the-queens-hand-01 |
| 4478 | 1 | Serves (diplomatic envoy) | `SERVES` | Galazza Galare → Barristan Selmy | adwd-the-queens-hand-01 |
| 4479 | 1 | Mocks / disrespects | `OPPOSES` | The Widower → Barristan Selmy | adwd-the-queens-hand-01 |
| 4480 | 1 | Loyal / obedient to | `(LLM tail)` | Grey Worm → Barristan Selmy | adwd-the-queens-hand-01 |
| 4481 | 1 | Made pact with | `(LLM tail)` | Quentyn Martell → The Tattered Prince | adwd-the-queens-hand-01 |
| 4482 | 1 | Unifying force for | `(LLM tail)` | Daenerys Targaryen → All Meereen factions | adwd-the-queens-hand-01 |
| 4483 | 1 | Sworn protector of; devoted loyalty to | `(LLM tail)` | Barristan Selmy → Daenerys Targaryen | adwd-the-queensguard-01 |
| 4484 | 1 | Cautious alliance forming with | `ALLIES_WITH` | Barristan Selmy → Skahaz mo Kandaq | adwd-the-queensguard-01 |
| 4485 | 1 | Mentor/trainer of | `TUTORS` | Barristan Selmy → His squires/lads | adwd-the-queensguard-01 |
| 4486 | 1 | Haunted by failure to protect | `(LLM tail)` | Barristan Selmy → Aerys, Rhaegar, Elia, Aegon (baby), Rhaenys, Robert, Jaehaerys | adwd-the-queensguard-01 |
| 4487 | 1 | Feels inadequate compared to | `(LLM tail)` | Barristan Selmy → Daario Naharis | adwd-the-queensguard-01 |
| 4488 | 1 | Systematically removes | `(LLM tail)` | Hizdahr zo Loraq → Daenerys's loyalists | adwd-the-queensguard-01 |
| 4489 | 1 | Relies on as protectors | `(LLM tail)` | Hizdahr zo Loraq → Pit fighters (Goghor, Khrazz, Spotted Cat, Belaquo) | adwd-the-queensguard-01 |
| 4490 | 1 | Commands (officially) through cousin | `COMMANDS` | Hizdahr zo Loraq → Brazen Beasts / Marghaz zo Loraq | adwd-the-queensguard-01 |
| 4491 | 1 | Hates; accuses of poisoning | `HATES` | Skahaz mo Kandaq → Hizdahr zo Loraq | adwd-the-queensguard-01 |
| 4492 | 1 | Claims continued loyalty of | `(LLM tail)` | Skahaz mo Kandaq → Brazen Beasts | adwd-the-queensguard-01 |
| 4493 | 1 | Loyal to; takes commands only from | `SERVES` | Grey Worm → Daenerys Targaryen | adwd-the-queensguard-01 |
| 4494 | 1 | Refused to serve | `(LLM tail)` | Grey Worm → Hizdahr zo Loraq | adwd-the-queensguard-01 |
| 4495 | 1 | Loves and is devoted to | `LOVES` | Missandei → Daenerys Targaryen | adwd-the-queensguard-01 |
| 4496 | 1 | Bonded rider of | `BONDED_TO` | Daenerys Targaryen → Drogon | adwd-the-queensguard-01 |
| 4497 | 1 | Fond of (as are Daenerys) | `LOVES` | Selmy → Cupbearers (Mezzara, Miklaz, Qezza) | adwd-the-queensguard-01 |
| 4498 | 1 | Guarded/companionship | `(LLM tail)` | Asha Greyjoy → Alysane Mormont | adwd-the-sacrifice-01 |
| 4499 | 1 | Wary dependence | `(LLM tail)` | Asha Greyjoy → Justin Massey | adwd-the-sacrifice-01 |
| 4500 | 1 | Mutual hostility | `(LLM tail)` | Asha Greyjoy → Clayton Suggs | adwd-the-sacrifice-01 |
| 4501 | 1 | Siblings (barely recognized) | `(LLM tail)` | Asha Greyjoy → Theon Greyjoy | adwd-the-sacrifice-01 |
| 4502 | 1 | Loyalty from | `(LLM tail)` | Asha Greyjoy → Tristifer Botley | adwd-the-sacrifice-01 |
| 4503 | 1 | Right-hand man to | `(LLM tail)` | Clayton Suggs → Godry Farring | adwd-the-sacrifice-01 |
| 4504 | 1 | Mutual antagonism with | `(LLM tail)` | Clayton Suggs → Justin Massey | adwd-the-sacrifice-01 |
| 4505 | 1 | Subordinate to / intimidated by | `SERVES` | Justin Massey → Richard Horpe | adwd-the-sacrifice-01 |
| 4506 | 1 | Authorizes | `(LLM tail)` | Stannis Baratheon → Queen's men (Godry, Suggs, Penny) | adwd-the-sacrifice-01 |
| 4507 | 1 | Withdrawn from | `(LLM tail)` | Stannis Baratheon → His lords | adwd-the-sacrifice-01 |
| 4508 | 1 | Vocal supporter of | `(LLM tail)` | Arnolf Karstark → Stannis Baratheon | adwd-the-sacrifice-01 |
| 4509 | 1 | Physical dependence on | `(LLM tail)` | Arnolf Karstark → Arthor Karstark | adwd-the-sacrifice-01 |
| 4510 | 1 | Faction tension with | `(LLM tail)` | Northmen → Southerners | adwd-the-sacrifice-01 |
| 4511 | 1 | Religious conflict with | `(LLM tail)` | Queen's men → Northern lords (Flint, Wull) | adwd-the-sacrifice-01 |
| 4512 | 1 | Stigmatized by | `(LLM tail)` | Lord Peasebury → Other lords | adwd-the-sacrifice-01 |
| 4513 | 1 | Seeks audience with | `SEEKS` | Tycho Nestoris → Stannis Baratheon | adwd-the-sacrifice-01 |
| 4514 | 1 | Transaction with | `(LLM tail)` | Sybelle Glover → Tycho Nestoris | adwd-the-sacrifice-01 |
| 4515 | 1 | Gave Theon/girl to | `GIFTED_TO` | Mors Umber → Tycho Nestoris's party | adwd-the-sacrifice-01 |
| 4516 | 1 | Close friend / advisor to | `COMPANION_OF` | Ser Gerris Drinkwater → Quentyn Martell | adwd-the-spurned-suitor-01 |
| 4517 | 1 | Close friend / loyal companion to | `COMPANION_OF` | Ser Archibald Yronwood → Quentyn Martell | adwd-the-spurned-suitor-01 |
| 4518 | 1 | Ward/foster son of | `WARD_OF` | Quentyn Martell → Lord Yronwood | adwd-the-spurned-suitor-01 |
| 4519 | 1 | Former betrothed/suitor of | `BETROTHED_TO` | Quentyn Martell → Daenerys Targaryen | adwd-the-spurned-suitor-01 |
| 4520 | 1 | Former member/deserter of | `(LLM tail)` | Quentyn Martell → The Windblown | adwd-the-spurned-suitor-01 |
| 4521 | 1 | Negotiating employer of | `(LLM tail)` | Quentyn Martell → The Tattered Prince | adwd-the-spurned-suitor-01 |
| 4522 | 1 | Hostile toward / mistrustful of | `OPPOSES` | The Tattered Prince → Quentyn Martell | adwd-the-spurned-suitor-01 |
| 4523 | 1 | Hired by / contracted with | `(LLM tail)` | The Windblown → Yunkai | adwd-the-spurned-suitor-01 |
| 4524 | 1 | Allied with / urging action from | `ALLIES_WITH` | Bloodbeard → Yunkai | adwd-the-spurned-suitor-01 |
| 4525 | 1 | Captive / psychologically enslaved by | `(LLM tail)` | Theon Greyjoy → Ramsay Bolton | adwd-the-turncloak-01 |
| 4526 | 1 | Forced servitor to | `(LLM tail)` | Theon Greyjoy → Ramsay Bolton | adwd-the-turncloak-01 |
| 4527 | 1 | Reluctant protector / guilty toward | `(LLM tail)` | Theon Greyjoy → Jeyne Poole | adwd-the-turncloak-01 |
| 4528 | 1 | Abuser of | `(LLM tail)` | Ramsay Bolton → Jeyne Poole | adwd-the-turncloak-01 |
| 4529 | 1 | Controls / commands | `COMMANDS` | Roose Bolton → Ramsay Bolton | adwd-the-turncloak-01 |
| 4530 | 1 | Controls access / holds | `COMMANDS` | Roose Bolton → All occupants of Winterfell | adwd-the-turncloak-01 |
| 4531 | 1 | Political advisor / critic to | `(LLM tail)` | Lady Dustin → Roose Bolton / Ramsay Bolton | adwd-the-turncloak-01 |
| 4532 | 1 | Identifies with / parallels | `(LLM tail)` | Lady Dustin → Theon Greyjoy | adwd-the-turncloak-01 |
| 4533 | 1 | Coerced ally of | `ALLIES_WITH` | Whoresbane Umber → Bolton/Frey coalition | adwd-the-turncloak-01 |
| 4534 | 1 | Hostile toward (implied) | `OPPOSES` | Hornwood men → Ramsay Bolton | adwd-the-turncloak-01 |
| 4535 | 1 | Seeks information from | `SEEKS` | Rowan → Theon Greyjoy | adwd-the-turncloak-01 |
| 4536 | 1 | Entertainer / serves | `(LLM tail)` | Abel → Ramsay Bolton / Bolton court | adwd-the-turncloak-01 |
| 4537 | 1 | Conflicted love for | `LOVES` | Theon Greyjoy → House Stark / the Starks | adwd-the-turncloak-01 |
| 4538 | 1 | Unenthusiastic participant in | `(LLM tail)` | Lord Wyman Manderly → Bolton coalition | adwd-the-turncloak-01 |
| 4539 | 1 | Uncomfortable outsiders in | `(LLM tail)` | Freys (Aenys, Hosteen) → The North / Bolton coalition | adwd-the-turncloak-01 |
| 4540 | 1 | Had spies within | `(LLM tail)` | Lady Dustin → Robb Stark's host | adwd-the-turncloak-01 |
| 4541 | 1 | Fostered with | `WARD_OF` | Brandon Stark (Ned's brother) → Old Lord Dustin at Barrowton | adwd-the-turncloak-01 |
| 4542 | 1 | Employs identity of | `(LLM tail)` | Arya → Cat of the Canals | adwd-the-ugly-little-girl-01 |
| 4543 | 1 | Employer-employee of | `(LLM tail)` | Arya → Brusco | adwd-the-ugly-little-girl-01 |
| 4544 | 1 | Kills (indirectly) | `KILLS` | Arya → The old man (target) | adwd-the-ugly-little-girl-01 |
| 4545 | 1 | Learned from | `(LLM tail)` | Arya → Red Roggo | adwd-the-ugly-little-girl-01 |
| 4546 | 1 | Recalls / models | `(LLM tail)` | Arya → Jaqen H'ghar | adwd-the-ugly-little-girl-01 |
| 4547 | 1 | Harbors revenge against | `(LLM tail)` | Arya → Ser Gregor, Dunsen, Raff the Sweetling, Ser Ilyn, Ser Meryn, Queen Cersei | adwd-the-ugly-little-girl-01 |
| 4548 | 1 | Performs with | `(LLM tail)` | Tagganaro → Casso, King of Seals | adwd-the-ugly-little-girl-01 |
| 4549 | 1 | Victim of | `(LLM tail)` | The dead girl (face donor) → Her father | adwd-the-ugly-little-girl-01 |
| 4550 | 1 | Captain of guards / devoted servant | `(LLM tail)` | Areo Hotah → Prince Doran | adwd-the-watcher-01 |
| 4551 | 1 | Former paramour of | `(LLM tail)` | Ellaria Sand → Oberyn Martell (dead) | adwd-the-watcher-01 |
| 4552 | 1 | Daughters of | `(LLM tail)` | Sand Snakes → Oberyn Martell (dead) | adwd-the-watcher-01 |
| 4553 | 1 | Flirts with | `(LLM tail)` | Arianne → Ser Balon Swann | adwd-the-watcher-01 |
| 4554 | 1 | Wary of / resists | `DISTRUSTS` | Ser Balon Swann → Arianne | adwd-the-watcher-01 |
| 4555 | 1 | Mocking yet loyal toward | `(LLM tail)` | Tyene Sand → Prince Doran | adwd-the-watcher-01 |
| 4556 | 1 | Distrusts (initially) | `DISTRUSTS` | Prince Doran → Sand Snakes | adwd-the-watcher-01 |
| 4557 | 1 | Corrects Nym about Ellaria | `(LLM tail)` | Prince Doran → Lady Nym | adwd-the-watcher-01 |
| 4558 | 1 | Planning with | `(LLM tail)` | Prince Doran → Quentyn Martell | adwd-the-watcher-01 |
| 4559 | 1 | Plotting against | `(LLM tail)` | Doran/Arianne → Cersei/Iron Throne | adwd-the-watcher-01 |
| 4560 | 1 | lovers | `LOVER_OF` | Asha → Qarl the Maid | adwd-the-wayward-bride-01 |
| 4561 | 1 | unrequited devotion from | `(LLM tail)` | Asha → Tris Botley | adwd-the-wayward-bride-01 |
| 4562 | 1 | forced marriage to | `(LLM tail)` | Asha → Erik Ironmaker | adwd-the-wayward-bride-01 |
| 4563 | 1 | political enemy of | `(LLM tail)` | Asha → Euron Greyjoy | adwd-the-wayward-bride-01 |
| 4564 | 1 | niece mentored by | `UNCLE_OF` | Asha → Rodrik the Reader | adwd-the-wayward-bride-01 |
| 4565 | 1 | captain/commander of | `COMMANDS` | Asha → Her ironborn crew | adwd-the-wayward-bride-01 |
| 4566 | 1 | devotion/service to | `(LLM tail)` | Tris Botley → Asha | adwd-the-wayward-bride-01 |
| 4567 | 1 | obedience/disregard toward | `(LLM tail)` | Qarl the Maid → Erik Ironmaker | adwd-the-wayward-bride-01 |
| 4568 | 1 | pursuer of | `(LLM tail)` | Euron → Aeron Greyjoy (Damphair) | adwd-the-wayward-bride-01 |
| 4569 | 1 | desperate mother to | `(LLM tail)` | Sybelle Glover → Gawen Glover, infant daughter | adwd-the-wayward-bride-01 |
| 4570 | 1 | eagerness for battle | `(LLM tail)` | Cromm → — | adwd-the-wayward-bride-01 |
| 4571 | 1 | unrequited interest in | `(LLM tail)` | Hagen's daughter → Tris Botley | adwd-the-wayward-bride-01 |
| 4572 | 1 | sexual encounter with | `(LLM tail)` | Hagen's daughter → Six-Toed Harl | adwd-the-wayward-bride-01 |
| 4573 | 1 | political enemy/threat to | `(LLM tail)` | Ramsay Bolton → Asha and ironborn | adwd-the-wayward-bride-01 |
| 4574 | 1 | mother fixated on | `(LLM tail)` | Lady Alannys → Theon | adwd-the-wayward-bride-01 |
| 4575 | 1 | poses as squire to | `(LLM tail)` | Quentyn Martell → Archibald Yronwood (Greenguts) | adwd-the-windblown-01 |
| 4576 | 1 | son of / sent by | `PARENT_OF` | Quentyn Martell → Prince Doran | adwd-the-windblown-01 |
| 4577 | 1 | counsels/advises | `ADVISES` | Gerris Drinkwater → Quentyn Martell | adwd-the-windblown-01 |
| 4578 | 1 | friends with (gambling) | `(LLM tail)` | Archibald Yronwood → Beans, Books, Old Bill Bone | adwd-the-windblown-01 |
| 4579 | 1 | serves as right hand to | `SERVES` | Caggo → The Tattered Prince | adwd-the-windblown-01 |
| 4580 | 1 | serves as left hand to | `SERVES` | Denzo D'han → The Tattered Prince | adwd-the-windblown-01 |
| 4581 | 1 | commands (mission) | `COMMANDS` | Pretty Meris → Westerosi defection group | adwd-the-windblown-01 |
| 4582 | 1 | killed slave girl of | `KILLS` | Caggo → Lucifer Long | adwd-the-windblown-01 |
| 4583 | 1 | dispatched brother to the Sorrows | `SIBLING_OF` | The Tattered Prince → Ser Orson Stone | adwd-the-windblown-01 |
| 4584 | 1 | killed boy of | `KILLS` | The Tattered Prince → Lewis Lanster | adwd-the-windblown-01 |
| 4585 | 1 | fears/dreads meeting | `FEARS` | Quentyn Martell → Daenerys Targaryen | adwd-the-windblown-01 |
| 4586 | 1 | childhood friends with | `(LLM tail)` | Quentyn Martell → Gerris Drinkwater & Archibald Yronwood | adwd-the-windblown-01 |
| 4587 | 1 | fears/is terrorized by | `FEARS` | Theon → Ramsay Bolton | adwd-theon-01 |
| 4588 | 1 | identity conflict with | `(LLM tail)` | Theon → Reek (persona) | adwd-theon-01 |
| 4589 | 1 | protects/commits to | `PROTECTS` | Abel → Theon | adwd-theon-01 |
| 4590 | 1 | distrusts/despises | `DISTRUSTS` | Rowan → Theon | adwd-theon-01 |
| 4591 | 1 | terrorized by/conditioned to | `(LLM tail)` | Jeyne Poole → Ramsay Bolton | adwd-theon-01 |
| 4592 | 1 | murderous hatred toward | `(LLM tail)` | Ser Hosteen Frey → Wyman Manderly | adwd-theon-01 |
| 4593 | 1 | provokes/defies | `(LLM tail)` | Wyman Manderly → Freys | adwd-theon-01 |
| 4594 | 1 | argues with | `(LLM tail)` | Ramsay Bolton → Roose Bolton | adwd-theon-01 |
| 4595 | 1 | dominates/terrorizes | `(LLM tail)` | Ramsay Bolton → His men (Bastard's Boys) | adwd-theon-01 |
| 4596 | 1 | reclaims identity | `(LLM tail)` | Theon → Himself | adwd-theon-01 |
| 4597 | 1 | loyal to/follows | `SERVES` | Holly → Abel | adwd-theon-01 |
| 4598 | 1 | squire/cousin to | `COUSIN_OF` | Big Walder → Little Walder | adwd-theon-01 |
| 4599 | 1 | rescued/escorted | `RESCUES` | Varys → Tyrion | adwd-tyrion-01 |
| 4600 | 1 | compelled rescue of | `(LLM tail)` | Jaime → Tyrion | adwd-tyrion-01 |
| 4601 | 1 | hosts/shelters | `(LLM tail)` | Illyrio → Tyrion | adwd-tyrion-01 |
| 4602 | 1 | friend/ally of | `ALLIES_WITH` | Illyrio → Varys | adwd-tyrion-01 |
| 4603 | 1 | seeks death of | `SEEKS` | Cersei → Tyrion | adwd-tyrion-01 |
| 4604 | 1 | grieves/obsesses over | `MOURNS` | Tyrion → Tysha | adwd-tyrion-01 |
| 4605 | 1 | forced rape of | `(LLM tail)` | Lord Tywin → Tysha | adwd-tyrion-01 |
| 4606 | 1 | serves/allies with | `SERVES` | Illyrio → "a dragon with three heads" | adwd-tyrion-01 |
| 4607 | 1 | sent to Wall | `(LLM tail)` | Tyrion → Janos Slynt | adwd-tyrion-01 |
| 4608 | 1 | Host / patron to | `(LLM tail)` | Illyrio → Tyrion | adwd-tyrion-02 |
| 4609 | 1 | Deep friendship / partnership with | `COMPANION_OF` | Illyrio → Varys | adwd-tyrion-02 |
| 4610 | 1 | Devoted to memory of | `(LLM tail)` | Illyrio → Serra | adwd-tyrion-02 |
| 4611 | 1 | Supporter / conspirator for | `CONSPIRES_WITH` | Illyrio → Daenerys | adwd-tyrion-02 |
| 4612 | 1 | Former patron of | `(LLM tail)` | Illyrio → Viserys | adwd-tyrion-02 |
| 4613 | 1 | Haunted by killing of | `(LLM tail)` | Tyrion → Tywin | adwd-tyrion-02 |
| 4614 | 1 | Guilt / horror over | `(LLM tail)` | Tyrion → Shae | adwd-tyrion-02 |
| 4615 | 1 | Grief / longing for | `MOURNS` | Tyrion → Tysha | adwd-tyrion-02 |
| 4616 | 1 | Violently conflicted with | `(LLM tail)` | Tyrion → Jaime | adwd-tyrion-02 |
| 4617 | 1 | Sold/gave Daenerys to | `(LLM tail)` | Illyrio → Khal Drogo | adwd-tyrion-02 |
| 4618 | 1 | Attempted incest with | `(LLM tail)` | Viserys → Daenerys | adwd-tyrion-02 |
| 4619 | 1 | Originally from | `(LLM tail)` | Varys → Myr | adwd-tyrion-02 |
| 4620 | 1 | Former bravo, lived by blade | `(LLM tail)` | Illyrio → (youth) | adwd-tyrion-02 |
| 4621 | 1 | Married (first) | `(LLM tail)` | Illyrio → Prince of Pentos's cousin | adwd-tyrion-02 |
| 4622 | 1 | Childhood affection for | `LOVES` | Tyrion → Gerion Lannister | adwd-tyrion-02 |
| 4623 | 1 | Founded | `(LLM tail)` | Bittersteel → Golden Company | adwd-tyrion-02 |
| 4624 | 1 | Patron → dependent / traveling under his protection | `(LLM tail)` | Tyrion → Illyrio | adwd-tyrion-03 |
| 4625 | 1 | Benefactor / emotionally attached | `(LLM tail)` | Illyrio → Young Griff | adwd-tyrion-03 |
| 4626 | 1 | Serves / knighted by | `SERVES` | Duck (Ser Rolly) → Griff | adwd-tyrion-03 |
| 4627 | 1 | Former squire | `(LLM tail)` | Duck → Harry Strickland | adwd-tyrion-03 |
| 4628 | 1 | Intellectual rivalry / testing | `(LLM tail)` | Haldon → Tyrion | adwd-tyrion-03 |
| 4629 | 1 | Camaraderie / amusement | `COMPANION_OF` | Duck → Tyrion | adwd-tyrion-03 |
| 4630 | 1 | Reluctant superior → distrustful subordinate | `SERVES` | Griff → Tyrion | adwd-tyrion-03 |
| 4631 | 1 | Projects father dynamic onto | `(LLM tail)` | Tyrion → Griff | adwd-tyrion-03 |
| 4632 | 1 | Ambivalent toward / claims murderous intent | `(LLM tail)` | Tyrion → Jaime | adwd-tyrion-03 |
| 4633 | 1 | Killed (confirmed) | `KILLS` | Tyrion → Tywin | adwd-tyrion-03 |
| 4634 | 1 | Claims to have poisoned (unverified) | `(LLM tail)` | Tyrion → Joffrey | adwd-tyrion-03 |
| 4635 | 1 | Bitterness / resentment toward | `(LLM tail)` | Tyrion → Tywin (recalled) | adwd-tyrion-03 |
| 4636 | 1 | Fond recollection | `(LLM tail)` | Tyrion → Gerion Lannister | adwd-tyrion-03 |
| 4637 | 1 | Father-son (claimed) | `(LLM tail)` | Griff → Young Griff | adwd-tyrion-03 |
| 4638 | 1 | Claims maternal connection to Tyrosh | `(LLM tail)` | Young Griff → (deceased mother) | adwd-tyrion-03 |
| 4639 | 1 | Beat severely / enemy | `(LLM tail)` | Duck → Lorent Caswell | adwd-tyrion-03 |
| 4640 | 1 | Devoted to deceased wife | `(LLM tail)` | Illyrio → Serra | adwd-tyrion-03 |
| 4641 | 1 | Moral authority over company | `(LLM tail)` | Septa Lemore → Duck, others | adwd-tyrion-03 |
| 4642 | 1 | Commands / controls | `COMMANDS` | Griff → Tyrion | adwd-tyrion-04 |
| 4643 | 1 | Father figure / commander | `COMMANDS` | Griff → Young Griff | adwd-tyrion-04 |
| 4644 | 1 | Sexual desire | `(LLM tail)` | Tyrion → Septa Lemore | adwd-tyrion-04 |
| 4645 | 1 | Indifferent to / tolerant of | `(LLM tail)` | Ysilla → Yandry's glancing | adwd-tyrion-04 |
| 4646 | 1 | Trains / sparring partner | `TEACHES` | Duck (Ser Rolly) → Young Griff | adwd-tyrion-04 |
| 4647 | 1 | Defeats | `DEFEATS` | Young Griff → Duck | adwd-tyrion-04 |
| 4648 | 1 | Rough camaraderie | `COMPANION_OF` | Duck → Tyrion | adwd-tyrion-04 |
| 4649 | 1 | Tutors | `TUTORS` | Haldon → Young Griff | adwd-tyrion-04 |
| 4650 | 1 | Intellectual rival | `(LLM tail)` | Tyrion → Haldon | adwd-tyrion-04 |
| 4651 | 1 | Resentment / dark satisfaction | `RESENTS` | Tyrion → Tywin Lannister | adwd-tyrion-04 |
| 4652 | 1 | Guilt / longing | `(LLM tail)` | Tyrion → Tysha | adwd-tyrion-04 |
| 4653 | 1 | Puppet master | `(LLM tail)` | Illyrio → Griff, Duck, the company | adwd-tyrion-04 |
| 4654 | 1 | Maternal / feeding | `(LLM tail)` | Ysilla → Young Griff | adwd-tyrion-04 |
| 4655 | 1 | Disciplinary | `(LLM tail)` | Ysilla → Duck | adwd-tyrion-04 |
| 4656 | 1 | Spiritual tutor | `(LLM tail)` | Septa Lemore → Young Griff | adwd-tyrion-04 |
| 4657 | 1 | Warmly teasing | `(LLM tail)` | Septa Lemore → Tyrion | adwd-tyrion-04 |
| 4658 | 1 | Guarded assessment | `(LLM tail)` | Tyrion → Young Griff | adwd-tyrion-04 |
| 4659 | 1 | Father figure to | `(LLM tail)` | Griff → Young Griff | adwd-tyrion-05 |
| 4660 | 1 | Protective of / devoted to | `PROTECTS` | Septa Lemore → Young Griff | adwd-tyrion-05 |
| 4661 | 1 | Superstitious/pious | `(LLM tail)` | Ysilla → The Rhoyne/supernatural | adwd-tyrion-05 |
| 4662 | 1 | Rationalist counterpoint to | `(LLM tail)` | Haldon Halfmaester → Ysilla | adwd-tyrion-05 |
| 4663 | 1 | Grief/betrayal toward | `MOURNS` | Tyrion → Jaime Lannister | adwd-tyrion-05 |
| 4664 | 1 | Unresolved longing for | `(LLM tail)` | Tyrion → Tysha | adwd-tyrion-05 |
| 4665 | 1 | Dear friend of | `(LLM tail)` | Jon Connington (Griff) → Rhaegar Targaryen | adwd-tyrion-05 |
| 4666 | 1 | Patron/briber of | `(LLM tail)` | Illyrio Mopatis → Nyessos (Triarch of Volantis) | adwd-tyrion-05 |
| 4667 | 1 | Married to / partnered with | `(LLM tail)` | Yandry → Ysilla | adwd-tyrion-05 |
| 4668 | 1 | Rescued from drowning | `RESCUES` | Griff → Tyrion | adwd-tyrion-06 |
| 4669 | 1 | Protected | `(LLM tail)` | Young Griff → Tyrion | adwd-tyrion-06 |
| 4670 | 1 | Tests/monitors | `(LLM tail)` | Haldon → Tyrion | adwd-tyrion-06 |
| 4671 | 1 | Compares self to | `(LLM tail)` | Tyrion → Joffrey (re: angering princes) | adwd-tyrion-06 |
| 4672 | 1 | Superior cyvasse player to | `(LLM tail)` | Qavo → Tyrion | adwd-tyrion-06 |
| 4673 | 1 | Proclaims | `(LLM tail)` | Benerro → Daenerys as Azor Ahai | adwd-tyrion-06 |
| 4674 | 1 | Bribed by | `(LLM tail)` | Nyessos (triarch) → Yunkai'i / Grazdan mo Eraz | adwd-tyrion-06 |
| 4675 | 1 | Captures | `CAPTURES` | Knight with bear surcoat → Tyrion | adwd-tyrion-06 |
| 4676 | 1 | Shame toward | `(LLM tail)` | Tyrion → Westerosi whore | adwd-tyrion-06 |
| 4677 | 1 | Former agent of | `(LLM tail)` | Jorah Mormont → Varys | adwd-tyrion-07 |
| 4678 | 1 | Betrayed by | `BETRAYS` | Jorah Mormont → Lynesse | adwd-tyrion-07 |
| 4679 | 1 | Guilty about | `(LLM tail)` | Tyrion Lannister → Tysha | adwd-tyrion-07 |
| 4680 | 1 | Former slave/wife of | `(LLM tail)` | The widow → Vogarro | adwd-tyrion-07 |
| 4681 | 1 | Concerned about | `(LLM tail)` | Tyrion Lannister → Griff/Aegon | adwd-tyrion-07 |
| 4682 | 1 | feels pity for / tentative friendship forming | `COMPANION_OF` | Tyrion → Penny | adwd-tyrion-08 |
| 4683 | 1 | blames / slowly forgiving | `OPPOSES` | Penny → Tyrion | adwd-tyrion-08 |
| 4684 | 1 | tense cohabitation / mutual irritation | `(LLM tail)` | Tyrion → Jorah Mormont | adwd-tyrion-08 |
| 4685 | 1 | obsessed longing for | `(LLM tail)` | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-08 |
| 4686 | 1 | proselytizing interest in | `(LLM tail)` | Moqorro → Tyrion | adwd-tyrion-08 |
| 4687 | 1 | distrustful wariness toward | `DISTRUSTS` | Tyrion → Moqorro | adwd-tyrion-08 |
| 4688 | 1 | conflicted feelings about | `(LLM tail)` | Tyrion → Jaime Lannister | adwd-tyrion-08 |
| 4689 | 1 | haunted by / guilt toward | `(LLM tail)` | Tyrion → Tywin Lannister | adwd-tyrion-08 |
| 4690 | 1 | lingering attachment to | `(LLM tail)` | Tyrion → Tysha | adwd-tyrion-08 |
| 4691 | 1 | guilt and memory regarding | `(LLM tail)` | Tyrion → Symon Silver Tongue (unnamed singer) | adwd-tyrion-08 |
| 4692 | 1 | devotion to memory of | `(LLM tail)` | Penny → Oppo | adwd-tyrion-08 |
| 4693 | 1 | superstitious about | `(LLM tail)` | Ship's crew → Penny | adwd-tyrion-08 |
| 4694 | 1 | superstitious affection for | `LOVES` | Ship's crew → Tyrion | adwd-tyrion-08 |
| 4695 | 1 | targeted dwarfs for bounty | `(LLM tail)` | Cersei → Tyrion | adwd-tyrion-08 |
| 4696 | 1 | forbade Gerion's voyage | `(LLM tail)` | Tywin → Gerion Lannister | adwd-tyrion-08 |
| 4697 | 1 | performing partner / reluctant ally | `ALLIES_WITH` | Tyrion → Penny | adwd-tyrion-09 |
| 4698 | 1 | antagonistic cohabitation | `OPPOSES` | Tyrion → Jorah Mormont | adwd-tyrion-09 |
| 4699 | 1 | unrequited devotion (inferred by Tyrion) | `(LLM tail)` | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-09 |
| 4700 | 1 | protective (pragmatic) | `(LLM tail)` | Jorah Mormont → Tyrion and Penny | adwd-tyrion-09 |
| 4701 | 1 | romantic interest / emotional dependence | `(LLM tail)` | Penny → Tyrion | adwd-tyrion-09 |
| 4702 | 1 | pity / admiration without desire | `RESPECTS` | Tyrion → Penny | adwd-tyrion-09 |
| 4703 | 1 | guilt and recurring memory | `(LLM tail)` | Tyrion → Shae | adwd-tyrion-09 |
| 4704 | 1 | recurring haunting | `(LLM tail)` | Tyrion → Tywin Lannister | adwd-tyrion-09 |
| 4705 | 1 | contempt / dark memory | `HATES` | Tyrion → Joffrey Baratheon | adwd-tyrion-09 |
| 4706 | 1 | warm memory | `(LLM tail)` | Tyrion → Gerion Lannister | adwd-tyrion-09 |
| 4707 | 1 | conflicted memory | `(LLM tail)` | Tyrion → Sansa Stark | adwd-tyrion-09 |
| 4708 | 1 | nostalgia / attraction | `(LLM tail)` | Tyrion → Lemore | adwd-tyrion-09 |
| 4709 | 1 | devotion | `(LLM tail)` | Penny → Pretty Pig and Crunch | adwd-tyrion-09 |
| 4710 | 1 | prophetic authority | `(LLM tail)` | Moqorro → Tyrion | adwd-tyrion-09 |
| 4711 | 1 | hostile/suspicious toward | `(LLM tail)` | Crew → Tyrion | adwd-tyrion-09 |
| 4712 | 1 | Fellow slave / protective toward | `(LLM tail)` | Tyrion → Penny | adwd-tyrion-10 |
| 4713 | 1 | Calculating potential manipulation of | `(LLM tail)` | Tyrion → Brown Ben Plumm | adwd-tyrion-10 |
| 4714 | 1 | Interested in Tyrion (identity/value) | `(LLM tail)` | Brown Ben Plumm → Tyrion | adwd-tyrion-10 |
| 4715 | 1 | Overseer/authority over | `(LLM tail)` | Nurse → Tyrion, Penny, Jorah | adwd-tyrion-10 |
| 4716 | 1 | Master of / possessive toward | `(LLM tail)` | Yezzan zo Qaggaz → His "treasures" (dwarfs, Sweets, others) | adwd-tyrion-10 |
| 4717 | 1 | Supreme commander / guest of honor | `COMMANDS` | Yurkhaz zo Yunzak → Yezzan zo Qaggaz | adwd-tyrion-10 |
| 4718 | 1 | Favored treasure of | `(LLM tail)` | Sweets → Yezzan zo Qaggaz | adwd-tyrion-10 |
| 4719 | 1 | Conflicted about / doesn't hate | `(LLM tail)` | Tyrion → Jorah Mormont | adwd-tyrion-10 |
| 4720 | 1 | Broken/devastated by news of | `(LLM tail)` | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-10 |
| 4721 | 1 | Rival bidder / predatory buyer | `(LLM tail)` | Zahrina → Jorah Mormont | adwd-tyrion-10 |
| 4722 | 1 | Contempt for / fear of | `HATES` | Tyrion → Yezzan zo Qaggaz | adwd-tyrion-10 |
| 4723 | 1 | Inferior cyvasse player to | `(LLM tail)` | Brown Ben Plumm → Tyrion | adwd-tyrion-10 |
| 4724 | 1 | Emotionally dependent on | `(LLM tail)` | Penny → Crunch (her dog) | adwd-tyrion-10 |
| 4725 | 1 | Remembers killing | `(LLM tail)` | Tyrion → Shae | adwd-tyrion-10 |
| 4726 | 1 | Poisoned / killed | `(LLM tail)` | Tyrion → Nurse | adwd-tyrion-11 |
| 4727 | 1 | Protective of / lies to | `PROTECTS` | Tyrion → Penny | adwd-tyrion-11 |
| 4728 | 1 | Compares to Sansa Stark | `(LLM tail)` | Tyrion → Penny | adwd-tyrion-11 |
| 4729 | 1 | Strategic approach toward | `(LLM tail)` | Tyrion → Brown Ben Plumm | adwd-tyrion-11 |
| 4730 | 1 | Guilt/responsibility toward | `(LLM tail)` | Tyrion → Ser Jorah Mormont | adwd-tyrion-11 |
| 4731 | 1 | Dominates / violent toward | `(LLM tail)` | Scar → Tyrion | adwd-tyrion-11 |
| 4732 | 1 | Views as moderate | `(LLM tail)` | Tyrion → Yezzan zo Qaggaz | adwd-tyrion-11 |
| 4733 | 1 | Contempt/pity for | `HATES` | Tyrion → Ser Jorah Mormont | adwd-tyrion-11 |
| 4734 | 1 | Known to / former associate | `(LLM tail)` | Mormont → Brown Ben Plumm | adwd-tyrion-11 |
| 4735 | 1 | Startled/wary of | `(LLM tail)` | Kasporio → Mormont | adwd-tyrion-11 |
| 4736 | 1 | Killed (prior) | `KILLS` | Tyrion → Tywin Lannister | adwd-tyrion-11 |
| 4737 | 1 | Hostility anticipated from | `(LLM tail)` | Tyrion → Barristan Selmy | adwd-tyrion-11 |
| 4738 | 1 | Previously tried to acquire | `(LLM tail)` | Brown Ben Plumm → Tyrion and Penny | adwd-tyrion-11 |
| 4739 | 1 | Asserts kinship via house allegiance | `(LLM tail)` | Tyrion → Brown Ben Plumm | adwd-tyrion-11 |
| 4740 | 1 | Opposed | `(LLM tail)` | Yezzan zo Qaggaz → Bloodbeard | adwd-tyrion-11 |
| 4741 | 1 | Favored peace with | `(LLM tail)` | Yezzan zo Qaggaz → Meereen | adwd-tyrion-11 |
| 4742 | 1 | Joins/becomes member of | `(LLM tail)` | Tyrion → Second Sons | adwd-tyrion-12 |
| 4743 | 1 | Works for/under | `(LLM tail)` | Tyrion → Inkpots | adwd-tyrion-12 |
| 4744 | 1 | Commands/captains | `COMMANDS` | Brown Ben Plumm → Second Sons | adwd-tyrion-12 |
| 4745 | 1 | Verbally spars with | `(LLM tail)` | Tyrion → Kasporio | adwd-tyrion-12 |
| 4746 | 1 | Protective concealment of | `(LLM tail)` | Brown Ben → Tyrion | adwd-tyrion-12 |
| 4747 | 1 | Caretaker/guardian toward | `(LLM tail)` | Tyrion → Penny | adwd-tyrion-12 |
| 4748 | 1 | Dependent on/resistant to | `(LLM tail)` | Penny → Tyrion | adwd-tyrion-12 |
| 4749 | 1 | Attachment to | `(LLM tail)` | Penny → Pretty Pig, Crunch | adwd-tyrion-12 |
| 4750 | 1 | Contempt toward (private) | `HATES` | Tyrion → Cersei | adwd-tyrion-12 |
| 4751 | 1 | Nostalgia for | `(LLM tail)` | Kem → King's Landing / Flea Bottom | adwd-tyrion-12 |
| 4752 | 1 | Fellow member of | `(LLM tail)` | Jorah Mormont → Second Sons | adwd-tyrion-12 |
| 4753 | 1 | Assesses military situation for | `(LLM tail)` | Jorah → Tyrion | adwd-tyrion-12 |
| 4754 | 1 | Plans to manipulate | `(LLM tail)` | Tyrion → Second Sons | adwd-tyrion-12 |
| 4755 | 1 | Idealizes former master | `(LLM tail)` | Penny → Yezzan | adwd-tyrion-12 |
| 4756 | 1 | Corrects/disillusions | `(LLM tail)` | Tyrion → Penny | adwd-tyrion-12 |
| 4757 | 1 | Smith for | `(LLM tail)` | Hammer → Second Sons | adwd-tyrion-12 |
| 4758 | 1 | Apprentice to | `(LLM tail)` | Nail → Hammer | adwd-tyrion-12 |
| 4759 | 1 | Serjeant over | `(LLM tail)` | Snatch → Kem | adwd-tyrion-12 |
| 4760 | 1 | Relies on / uses | `(LLM tail)` | Victarion → Moqorro | adwd-victarion-01 |
| 4761 | 1 | Serves / flatters | `SERVES` | Moqorro → Victarion | adwd-victarion-01 |
| 4762 | 1 | Sexual possession of | `(LLM tail)` | Victarion → The dusky woman | adwd-victarion-01 |
| 4763 | 1 | Admires / seeks to surpass | `RESPECTS` | Victarion → Balon Greyjoy | adwd-victarion-01 |
| 4764 | 1 | Distant from | `(LLM tail)` | Victarion → Aeron Greyjoy | adwd-victarion-01 |
| 4765 | 1 | Fear / shun | `FEARS` | Iron Fleet crew → Moqorro | adwd-victarion-01 |
| 4766 | 1 | Theological opponent of | `(LLM tail)` | Moqorro → Drowned God religion | adwd-victarion-01 |
| 4767 | 1 | Remembers defeat by | `(LLM tail)` | Victarion → Stannis Baratheon | adwd-victarion-01 |

---

## Draft Deterministic HINT_TO_EDGE Map

> Only confidently-mapped phrases. Ambiguous ones left in LLM tail.
> Coverage is measured against total rows (some high-freq hints are unmapped).

| Hint Phrase (normalized) | Edge Type | Rows Covered |
|--------------------------|-----------|-------------|
| commands | `COMMANDS` | 100 |
| distrusts | `DISTRUSTS` | 92 |
| serves | `SERVES` | 67 |
| hostile toward | `OPPOSES` | 66 |
| protective of | `PROTECTS` | 65 |
| mourns | `MOURNS` | 59 |
| father of | `PARENT_OF` | 55 |
| contempt for | `HATES` | 52 |
| fears | `FEARS` | 43 |
| killed | `KILLS` | 43 |
| kills | `KILLS` | 37 |
| contempt toward | `HATES` | 34 |
| brother of | `SIBLING_OF` | 31 |
| son of | `PARENT_OF` | 29 |
| trusts | `TRUSTS` | 29 |
| bonded to | `BONDED_TO` | 27 |
| betrothed to | `BETROTHED_TO` | 26 |
| resents | `RESENTS` | 26 |
| hates | `HATES` | 25 |
| daughter of | `PARENT_OF` | 24 |
| protects | `PROTECTS` | 24 |
| hostility toward | `OPPOSES` | 23 |
| loyal to | `SERVES` | 23 |
| mother of | `PARENT_OF` | 22 |
| sister of | `SIBLING_OF` | 20 |
| married to | `SPOUSE_OF` | 20 |
| grieves for | `MOURNS` | 20 |
| manipulates | `MANIPULATES` | 19 |
| opposes | `OPPOSES` | 18 |
| dismissive of | `DISTRUSTS` | 16 |
| blames | `OPPOSES` | 16 |
| contemptuous of | `HATES` | 16 |
| hatred toward | `HATES` | 13 |
| allied with | `ALLIES_WITH` | 13 |
| longs for | `MOURNS` | 13 |
| threatens | `OPPOSES` | 12 |
| respects | `RESPECTS` | 12 |
| cousin of | `COUSIN_OF` | 12 |
| grief for | `MOURNS` | 12 |
| antagonistic toward | `OPPOSES` | 11 |
| wife of | `SPOUSE_OF` | 11 |
| mocks | `OPPOSES` | 11 |
| formerly served | `SERVES` | 11 |
| defiant toward | `OPPOSES` | 10 |
| sworn to | `SWORN_TO` | 10 |
| suspicious of | `DISTRUSTS` | 10 |
| wary of | `DISTRUSTS` | 10 |
| protective toward | `PROTECTS` | 10 |
| friendship with | `COMPANION_OF` | 10 |
| authority over | `COMMANDS` | 9 |
| loves | `LOVES` | 9 |
| protected by | `PROTECTS` | 9 |
| fears for | `FEARS` | 9 |
| fear of | `FEARS` | 9 |
| betrays | `BETRAYS` | 9 |
| misses | `MOURNS` | 9 |
| commander | `COMMANDS` | 9 |
| defies | `OPPOSES` | 8 |
| lover of | `LOVER_OF` | 8 |
| seeks | `SEEKS` | 8 |
| protective concern for | `PROTECTS` | 8 |
| defends | `PROTECTS` | 7 |
| niece of | `UNCLE_OF` | 7 |
| squire to | `SERVES` | 7 |
| loyalty to | `SERVES` | 7 |
| controls | `COMMANDS` | 7 |
| loyal service to | `SERVES` | 7 |
| grudging respect for | `RESPECTS` | 7 |
| former lover of | `LOVER_OF` | 7 |
| contempt | `HATES` | 6 |
| advises | `ADVISES` | 6 |
| resentment toward | `RESENTS` | 6 |
| husband of | `SPOUSE_OF` | 6 |
| distrust toward | `DISTRUSTS` | 6 |
| friend of | `COMPANION_OF` | 6 |
| loved | `LOVES` | 6 |
| bitter toward | `RESENTS` | 6 |
| commander of | `COMMANDS` | 6 |
| fond of | `LOVES` | 6 |
| despises | `HATES` | 6 |
| conspires with | `CONSPIRES_WITH` | 5 |
| half-brother of | `SIBLING_OF` | 5 |
| ward of | `WARD_OF` | 5 |
| serves/protects | `SERVES` | 5 |
| distrustful of | `DISTRUSTS` | 5 |
| distrust | `DISTRUSTS` | 5 |
| close friendship with | `COMPANION_OF` | 5 |
| commands/leads | `COMMANDS` | 5 |
| companion of | `COMPANION_OF` | 5 |
| childhood companion of | `COMPANION_OF` | 5 |
| subordinate to | `SERVES` | 5 |
| warns | `ADVISES` | 5 |
| captor of | `CAPTURES` | 5 |
| friendship | `COMPANION_OF` | 5 |
| mentors | `TUTORS` | 5 |
| obeys | `SERVES` | 5 |
| secret lover of | `LOVER_OF` | 5 |
| student of | `TUTORS` | 4 |
| loyal to memory of | `SERVES` | 4 |
| fears/resents | `FEARS` | 4 |
| seeks alliance with | `SEEKS` | 4 |
| seeks vengeance against | `SEEKS` | 4 |
| serves as hand to | `SERVES` | 4 |
| commands/controls | `COMMANDS` | 4 |
| leads | `COMMANDS` | 4 |
| negotiates with | `NEGOTIATES_WITH` | 4 |
| uncle of | `UNCLE_OF` | 4 |
| killed by | `KILLS` | 4 |
| enemy of | `OPPOSES` | 4 |
| trusts / relies on | `TRUSTS` | 4 |
| admires | `RESPECTS` | 4 |
| bonded with | `BONDED_TO` | 4 |
| mistrusts | `DISTRUSTS` | 4 |
| grieving for | `MOURNS` | 4 |
| brother to | `SIBLING_OF` | 4 |
| cousin to | `COUSIN_OF` | 4 |
| holds captive | `PRISONER_OF` | 4 |
| warg bond with | `WARGS_INTO` | 4 |
| disdains | `HATES` | 4 |
| affectionate toward | `LOVES` | 4 |
| resentful toward | `RESENTS` | 4 |
| grudging respect toward | `RESPECTS` | 4 |
| co-conspirator with | `CONSPIRES_WITH` | 4 |
| serves under | `SERVES` | 3 |
| rescued | `RESCUES` | 3 |
| counsels | `ADVISES` | 3 |
| trusts and relies on | `TRUSTS` | 3 |
| commands / trusts | `COMMANDS` | 3 |
| mocks/antagonizes | `OPPOSES` | 3 |
| contemptuous toward | `HATES` | 3 |
| close friend of | `COMPANION_OF` | 3 |
| loathes | `HATES` | 3 |
| antagonizes | `OPPOSES` | 3 |
| advises/serves | `ADVISES` | 3 |
| loyal to / serves | `SERVES` | 3 |
| fears/distrusts | `FEARS` | 3 |
| distrust of | `DISTRUSTS` | 3 |
| guards | `GUARDS` | 3 |
| manipulates / tests loyalty of | `MANIPULATES` | 3 |
| manipulates/controls | `MANIPULATES` | 3 |
| terrified of | `FEARS` | 3 |
| fears/avoids | `FEARS` | 3 |
| commands/owns | `COMMANDS` | 3 |
| member of | `MEMBER_OF` | 3 |
| prisoner of | `PRISONER_OF` | 3 |
| rescues | `RESCUES` | 3 |
| sister of (deceased) | `SIBLING_OF` | 3 |
| companion | `COMPANION_OF` | 3 |
| was betrothed to | `BETROTHED_TO` | 3 |
| widow of | `SPOUSE_OF` | 3 |
| fearful of | `FEARS` | 3 |
| sister to | `SIBLING_OF` | 3 |
| holds hostage | `PRISONER_OF` | 3 |
| friendly with | `COMPANION_OF` | 3 |
| loved (past) | `LOVES` | 3 |
| loyal subordinate to | `SERVES` | 3 |
| granddaughter of | `PARENT_OF` | 3 |
| under command of | `COMMANDS` | 3 |
| proposes alliance with | `ALLIES_WITH` | 3 |
| affection for | `LOVES` | 3 |
| warns/advises | `ADVISES` | 3 |
| bitter resentment | `RESENTS` | 3 |
| employs / commands | `COMMANDS` | 3 |
| traveling companion | `COMPANION_OF` | 3 |
| bitter about | `RESENTS` | 3 |
| grandson of | `PARENT_OF` | 3 |
| remembers/mourns | `MOURNS` | 3 |
| warns dany about | `ADVISES` | 3 |
| imprisons | `IMPRISONS` | 3 |
| recalls with respect | `RESPECTS` | 3 |
| murderer of | `KILLS` | 3 |
| loyal companion to | `COMPANION_OF` | 3 |
| murdered | `KILLS` | 3 |
| conspired with | `CONSPIRES_WITH` | 3 |
| remembers / mourns | `MOURNS` | 3 |
| friendly acquaintance | `COMPANION_OF` | 3 |
| commander/master | `COMMANDS` | 3 |
| uneasy alliance | `ALLIES_WITH` | 3 |
| subordinate of | `SERVES` | 3 |
| misses/mourns | `MOURNS` | 3 |
| protects / serves | `PROTECTS` | 2 |
| fears judgment from | `FEARS` | 2 |
| mourns/grieves | `MOURNS` | 2 |
| loves/trusts | `LOVES` | 2 |
| executes | `EXECUTES` | 2 |
| advisor to | `ADVISES` | 2 |
| serves as scout commander for | `SERVES` | 2 |
| serves as lord bannerman to | `SERVES` | 2 |
| seeks counsel from | `SEEKS` | 2 |
| bitterness toward | `RESENTS` | 2 |
| mother of (unborn) | `PARENT_OF` | 2 |
| protects/advises | `PROTECTS` | 2 |
| serves/assists | `SERVES` | 2 |
| mourns / loves | `MOURNS` | 2 |
| loyal service | `SERVES` | 2 |
| investigates | `INVESTIGATES` | 2 |
| hatred for | `HATES` | 2 |
| grieves for / fears for | `MOURNS` | 2 |
| half-brother | `SIBLING_OF` | 2 |
| half-sister | `SIBLING_OF` | 2 |
| mocks and demeans | `OPPOSES` | 2 |
| protector of | `PROTECTS` | 2 |
| mourns/worries for | `MOURNS` | 2 |
| close friendship | `COMPANION_OF` | 2 |
| disciplinarian over | `COMMANDS` | 2 |
| resentment / dark fantasy toward | `RESENTS` | 2 |
| captive of | `PRISONER_OF` | 2 |
| accompanies | `TRAVELS_WITH` | 2 |
| commands respect from | `COMMANDS` | 2 |
| disguised as | `DISGUISED_AS` | 2 |
| owns/commands | `OWNS` | 2 |
| bonded to / wargs into | `BONDED_TO` | 2 |
| heir to | `HEIR_TO` | 2 |
| seeks marriage with | `SEEKS` | 2 |
| bonded to / warg connection | `BONDED_TO` | 2 |
| trusts/confides in | `TRUSTS` | 2 |
| commands/trusts | `COMMANDS` | 2 |
| resentment | `RESENTS` | 2 |
| distrusts (partially) | `DISTRUSTS` | 2 |
| commands/mentors | `COMMANDS` | 2 |
| commands / mentors | `COMMANDS` | 2 |
| contemptuous | `HATES` | 2 |
| protects (reluctantly) | `PROTECTS` | 2 |
| serves blindly | `SERVES` | 2 |
| serves loyally | `SERVES` | 2 |
| dismissive of uncle | `DISTRUSTS` | 2 |
| commands/relies on | `COMMANDS` | 2 |
| commands / employs | `COMMANDS` | 2 |
| serves/advises | `SERVES` | 2 |
| leads / commands | `COMMANDS` | 2 |
| leads/commands | `COMMANDS` | 2 |
| transactional with | `CONTRACTED_WITH` | 2 |
| captured | `CAPTURES` | 2 |
| respects memory of | `RESPECTS` | 2 |
| serves / loyal to | `SERVES` | 2 |
| trains | `TEACHES` | 2 |
| protects / is guarded by | `PROTECTS` | 2 |
| serves/champions | `SERVES` | 2 |
| heals | `HEALS` | 2 |
| commands/sends | `COMMANDS` | 2 |
| mourning mother | `MOURNS` | 2 |
| commands (lord commander) | `COMMANDS` | 2 |
| guards (friendly) | `GUARDS` | 2 |
| allies with | `ALLIES_WITH` | 2 |
| respects/mourns | `RESPECTS` | 2 |
| respects the memory of | `RESPECTS` | 2 |
| serves as kingsguard | `SERVES` | 2 |
| gave gift to | `GIFTED_TO` | 2 |
| mourns/regrets failing | `MOURNS` | 2 |
| contempt toward past | `HATES` | 2 |
| brother of (grieving) | `SIBLING_OF` | 2 |
| serves/devoted to | `SERVES` | 2 |
| mourns / remembers | `MOURNS` | 2 |
| hostile to | `OPPOSES` | 2 |
| seeks to use | `SEEKS` | 2 |
| wargs into / skinchanges | `WARGS_INTO` | 2 |
| resents / hates | `RESENTS` | 2 |
| political rival of | `OPPOSES` | 2 |
| rules/commands | `RULES` | 2 |
| murders | `KILLS` | 2 |
| grieves / believes dead | `MOURNS` | 2 |
| guest of | `GUEST_OF` | 2 |
| antagonized by / distrusted by | `OPPOSES` | 2 |
| leads vanguard for | `COMMANDS` | 2 |
| student/trainee | `TUTORS` | 2 |
| nephew of | `NEPHEW_OF` | 2 |
| student/acolyte of | `TUTORS` | 2 |
| brother of (dead) | `SIBLING_OF` | 2 |
| disdain for | `HATES` | 2 |
| longs for / loves | `MOURNS` | 2 |
| protective older brother | `SIBLING_OF` | 2 |
| relies on counsel of | `ADVISES` | 2 |
| companion to | `COMPANION_OF` | 2 |
| brother-in-law of | `IN_LAW_OF` | 2 |
| mother, counselor to | `ADVISES` | 2 |
| former betrothed of | `BETROTHED_TO` | 2 |
| recalls with affection | `LOVES` | 2 |
| warned | `ADVISES` | 2 |
| obeys / serves | `SERVES` | 2 |
| former subordinate of | `SERVES` | 2 |
| misses deeply | `MOURNS` | 2 |
| camaraderie | `COMPANION_OF` | 2 |
| love / longing | `LOVES` | 2 |
| admiration for | `RESPECTS` | 2 |
| disdain toward | `HATES` | 2 |
| admired by | `RESPECTS` | 2 |
| sardonic camaraderie with | `COMPANION_OF` | 2 |
| pragmatic alliance with | `ALLIES_WITH` | 2 |
| grief for / loss | `MOURNS` | 2 |
| misses/longs for | `MOURNS` | 2 |
| remembers with grief | `MOURNS` | 2 |
| warging bond with | `WARGS_INTO` | 2 |
| devoted service / love | `LOVES` | 2 |
| alliance with | `ALLIES_WITH` | 2 |
| great-niece of | `PARENT_OF` | 2 |
| warns against | `ADVISES` | 2 |
| bitter resentment toward | `RESENTS` | 2 |
| remembers/respects | `RESPECTS` | 2 |
| grudging respect | `RESPECTS` | 2 |
| grief/longing for | `MOURNS` | 2 |
| secret alliance with | `ALLIES_WITH` | 2 |
| overlord / war commander | `COMMANDS` | 2 |
| bitter enemy of | `RESENTS` | 2 |
| employs/commands | `COMMANDS` | 2 |
| loyal subordinate of | `SERVES` | 2 |
| was fond of | `LOVES` | 2 |
| grief/loss toward | `MOURNS` | 2 |
| uncle to | `UNCLE_OF` | 2 |
| former brother of | `SIBLING_OF` | 2 |
| memory / affection | `LOVES` | 2 |
| friendly toward | `COMPANION_OF` | 2 |
| friendship/dependency | `COMPANION_OF` | 2 |
| grief/guilt toward | `MOURNS` | 2 |
| grief/loss | `MOURNS` | 2 |
| longs for / mourns | `MOURNS` | 2 |
| mistrust | `DISTRUSTS` | 2 |
| political rival / bitter enemy | `RESENTS` | 2 |
| grief/resentment toward | `MOURNS` | 2 |
| former lover | `LOVER_OF` | 2 |
| misses / would turn to | `MOURNS` | 2 |
| uncle | `UNCLE_OF` | 2 |
| warging bond | `WARGS_INTO` | 2 |
| subordinate dissatisfied with | `SERVES` | 2 |
| secretly allied with | `ALLIES_WITH` | 2 |
| grief/longing | `MOURNS` | 2 |
| nostalgic affection | `LOVES` | 2 |
| subordinate captain to | `SERVES` | 2 |
| leader/commander of | `COMMANDS` | 2 |
| deep closeness | `LOVES` | 1 |
| bonded to / loves | `BONDED_TO` | 1 |
| teacher/student | `TUTORS` | 1 |
| guards / serves | `GUARDS` | 1 |
| teacher/protector of | `TUTORS` | 1 |
| student/trusts | `TUTORS` | 1 |
| hostile toward / attempting to capture | `OPPOSES` | 1 |
| hostile toward / attempts to capture | `OPPOSES` | 1 |
| loves/misses | `LOVES` | 1 |
| protects and disguises | `PROTECTS` | 1 |
| commands / asserts authority over | `COMMANDS` | 1 |
| teacher/mentor to | `TUTORS` | 1 |
| dreams of becoming | `DREAMS_OF` | 1 |
| loves (still) | `LOVES` | 1 |
| threatens (implicitly) | `OPPOSES` | 1 |
| teacher/guardian to | `TUTORS` | 1 |
| serves/cares for | `SERVES` | 1 |
| distrust / dislike | `DISTRUSTS` | 1 |
| contempt / hostility | `HATES` | 1 |
| mourns/grieves for | `MOURNS` | 1 |
| trains/disciplines | `TEACHES` | 1 |
| foster-son of | `WARD_OF` | 1 |
| seeks solace in | `SEEKS` | 1 |
| trust in / reliance on | `TRUSTS` | 1 |
| sister of (hostile) | `SIBLING_OF` | 1 |
| ward of / companion to | `WARD_OF` | 1 |
| fears (respects) | `FEARS` | 1 |
| serves as messenger for | `SERVES` | 1 |
| commands eastern foot force for | `COMMANDS` | 1 |
| mother of / fiercely protective | `PARENT_OF` | 1 |
| son of / obedient but growing independent | `PARENT_OF` | 1 |
| daughter of / deep affection | `PARENT_OF` | 1 |
| bonded to / shadows | `BONDED_TO` | 1 |
| companion of / eager subordinate | `COMPANION_OF` | 1 |
| respects as adversary | `RESPECTS` | 1 |
| companion of / bonded to | `COMPANION_OF` | 1 |
| mourns/longs for | `MOURNS` | 1 |
| controls/abuses | `COMMANDS` | 1 |
| sworn sword to | `SWORN_TO` | 1 |
| resents position below | `RESENTS` | 1 |
| defies and asserts authority over | `OPPOSES` | 1 |
| serves and advises | `SERVES` | 1 |
| serves and teaches | `SERVES` | 1 |
| gave gifts to | `GIFTED_TO` | 1 |
| threatens/intimidates | `OPPOSES` | 1 |
| guards/threatens | `GUARDS` | 1 |
| serves/alerts | `SERVES` | 1 |
| advises / respects | `ADVISES` | 1 |
| hostile toward / mocking | `OPPOSES` | 1 |
| protects / claims | `PROTECTS` | 1 |
| dismissive of / dominant over | `DISTRUSTS` | 1 |
| commands (with difficulty) | `COMMANDS` | 1 |
| rescued / protects | `RESCUES` | 1 |
| threatens / hostile toward | `OPPOSES` | 1 |
| father of (unborn) | `PARENT_OF` | 1 |
| mother of (bereaved) | `PARENT_OF` | 1 |
| commands / sovereign | `COMMANDS` | 1 |
| sworn to / loves | `SWORN_TO` | 1 |
| distrust and contempt for | `DISTRUSTS` | 1 |
| protective of / controlling toward | `PROTECTS` | 1 |
| distrusts / dislikes | `DISTRUSTS` | 1 |
| distrusts / hostile toward | `DISTRUSTS` | 1 |
| trusts as near-brother | `TRUSTS` | 1 |
| mocks / irreverent toward | `OPPOSES` | 1 |
| commands/directs finances of | `COMMANDS` | 1 |
| investigates death of | `INVESTIGATES` | 1 |
| wary of / fretted by | `DISTRUSTS` | 1 |
| loathes marriage to | `HATES` | 1 |
| protective of / uneasy about training | `PROTECTS` | 1 |
| respects loyalty of | `RESPECTS` | 1 |
| defies / moral opposition | `OPPOSES` | 1 |
| mourns lost friendship | `MOURNS` | 1 |
| hates (enduringly) | `HATES` | 1 |
| serves / manipulates | `SERVES` | 1 |
| mocks / warns | `OPPOSES` | 1 |
| investigates murder of | `INVESTIGATES` | 1 |
| protects/shields | `PROTECTS` | 1 |
| brother of the kingsguard with | `SIBLING_OF` | 1 |
| father of (unacknowledged bastard) | `PARENT_OF` | 1 |
| defends / shields | `PROTECTS` | 1 |
| serves/reports to | `SERVES` | 1 |
| respects but sees as limited | `RESPECTS` | 1 |
| mocks/socializes with | `OPPOSES` | 1 |
| mother of (by jaime) | `PARENT_OF` | 1 |
| mourns/loves memory of | `MOURNS` | 1 |
| attacks honor of | `ATTACKS` | 1 |
| mourns / associates with pale blue roses | `MOURNS` | 1 |
| contempt for his own reign | `HATES` | 1 |
| student/devoted to | `TUTORS` | 1 |
| allied with / fled with | `ALLIES_WITH` | 1 |
| serves/betrays for | `SERVES` | 1 |
| blames self for downfall of | `OPPOSES` | 1 |
| manipulates / pressures | `MANIPULATES` | 1 |
| half-brother (acknowledged with pain) | `SIBLING_OF` | 1 |
| ward of / ignores jon | `WARD_OF` | 1 |
| deep affection / closest sibling bond | `LOVES` | 1 |
| antagonistic / chafing | `OPPOSES` | 1 |
| defeats in combat training | `DEFEATS` | 1 |
| attacks | `ATTACKS` | 1 |
| authority over / contempt for | `COMMANDS` | 1 |
| resentment / pain | `RESENTS` | 1 |
| bonded to / protected by | `BONDED_TO` | 1 |
| nephew of (believed son of brother) | `NEPHEW_OF` | 1 |
| resents / mocks (privately) | `RESENTS` | 1 |
| resents / near-insubordinate toward | `RESENTS` | 1 |
| respects knowledge of | `RESPECTS` | 1 |
| treated by | `HEALS` | 1 |
| loves and trusts | `LOVES` | 1 |
| guards / obeys | `GUARDS` | 1 |
| contempt for knighthood | `HATES` | 1 |
| heir of | `HEIR_TO` | 1 |
| manipulated by | `MANIPULATES` | 1 |
| trusts naively | `TRUSTS` | 1 |
| controls/monitors | `COMMANDS` | 1 |
| opposes mercy for | `OPPOSES` | 1 |
| betrothed to (against her will) | `BETROTHED_TO` | 1 |
| protects/advises (roughly) | `PROTECTS` | 1 |
| serves (but with independent judgment) | `SERVES` | 1 |
| controls (through joffrey) | `COMMANDS` | 1 |
| advises/restrains | `ADVISES` | 1 |
| mourns/concerned for | `MOURNS` | 1 |
| mocks / antagonizes | `OPPOSES` | 1 |
| respects / is moved by | `RESPECTS` | 1 |
| respects / praises | `RESPECTS` | 1 |
| loves / misses | `LOVES` | 1 |
| loves / worries about | `LOVES` | 1 |
| grieves / is estranged from | `MOURNS` | 1 |
| hostile toward / indebted to | `OPPOSES` | 1 |
| contempt/cruelty toward | `HATES` | 1 |
| contempt toward / negotiates with | `HATES` | 1 |
| contemptuous father to | `HATES` | 1 |
| seeks approval from / resents | `SEEKS` | 1 |
| loves (brother) | `LOVES` | 1 |
| disguised protégée of | `DISGUISED_AS` | 1 |
| deep love and longing for | `LOVES` | 1 |
| mourning | `MOURNS` | 1 |
| student of (recalled) | `TUTORS` | 1 |
| antagonized by | `OPPOSES` | 1 |
| protects / defends | `PROTECTS` | 1 |
| fears (after fight) | `FEARS` | 1 |
| recruiter/escort for | `MEMBER_OF` | 1 |
| gave needle to | `GIFTED_TO` | 1 |
| companion of (involuntary) | `COMPANION_OF` | 1 |
| contempt for / mocked by | `HATES` | 1 |
| trusts and follows | `TRUSTS` | 1 |
| loyal to yoren until overwhelmed | `SERVES` | 1 |
| leads/protects | `COMMANDS` | 1 |
| respects/values | `RESPECTS` | 1 |
| serves as interrogator for | `SERVES` | 1 |
| disguised as servant to | `DISGUISED_AS` | 1 |
| kills for | `KILLS` | 1 |
| fears / hates | `FEARS` | 1 |
| threatens / fears | `OPPOSES` | 1 |
| commands van for | `COMMANDS` | 1 |
| protects identity from | `PROTECTS` | 1 |
| mocks class distance with | `OPPOSES` | 1 |
| executes/punishes | `EXECUTES` | 1 |
| resents/angry at | `RESENTS` | 1 |
| leads (poorly) | `COMMANDS` | 1 |
| loyal to (nominally) | `SERVES` | 1 |
| betrothed to (broken) | `BETROTHED_TO` | 1 |
| serves as squire to | `SERVES` | 1 |
| mourns/is crazed over | `MOURNS` | 1 |
| resents / jealous of | `RESENTS` | 1 |
| resents being corrected by | `RESENTS` | 1 |
| authority over / tutors | `COMMANDS` | 1 |
| serves/carries | `SERVES` | 1 |
| captures / conquers | `CAPTURES` | 1 |
| wargs into / spiritually bonded with | `WARGS_INTO` | 1 |
| protects/comforts | `PROTECTS` | 1 |
| leads/makes tactical decisions for | `COMMANDS` | 1 |
| serves as catspaw of | `SERVES` | 1 |
| loyal to / escorts | `SERVES` | 1 |
| contempt and dismissal | `HATES` | 1 |
| loyalty to / envoy for | `SERVES` | 1 |
| mourning / longing for | `MOURNS` | 1 |
| grieves for / tends to | `MOURNS` | 1 |
| half-brother to | `SIBLING_OF` | 1 |
| seeks approval from | `SEEKS` | 1 |
| resentment/coldness (past) | `RESENTS` | 1 |
| distrusts/blames | `DISTRUSTS` | 1 |
| mother of (grieving) | `PARENT_OF` | 1 |
| mother of (fearful for) | `PARENT_OF` | 1 |
| daughter of (devoted) | `PARENT_OF` | 1 |
| brother of (protective) | `SIBLING_OF` | 1 |
| formerly served (conflicted) | `SERVES` | 1 |
| distrusts/reassesses | `DISTRUSTS` | 1 |
| father of (remembered) | `PARENT_OF` | 1 |
| loves romantically | `LOVES` | 1 |
| trusts but cannot fully love | `TRUSTS` | 1 |
| distrusts sorcery because of | `DISTRUSTS` | 1 |
| advises/protects | `ADVISES` | 1 |
| loyal to (past) | `SERVES` | 1 |
| distrust/hostility | `DISTRUSTS` | 1 |
| hostile toward / attacks | `OPPOSES` | 1 |
| rescued by | `RESCUES` | 1 |
| serves as maester to | `SERVES` | 1 |
| loyal service; truthful counsel | `SERVES` | 1 |
| trusts and values | `TRUSTS` | 1 |
| fears and distrusts | `FEARS` | 1 |
| defends/protects | `PROTECTS` | 1 |
| respects (grudgingly) | `RESPECTS` | 1 |
| serves as steward to | `SERVES` | 1 |
| distrusts but uses | `DISTRUSTS` | 1 |
| seeks information about | `SEEKS` | 1 |
| respects/seeks approval from | `RESPECTS` | 1 |
| bonded to/fights for | `BONDED_TO` | 1 |
| attacks (on jon's behalf) | `ATTACKS` | 1 |
| hostile toward/distrusts | `OPPOSES` | 1 |
| mocks/challenges | `OPPOSES` | 1 |
| hates/tracks | `HATES` | 1 |
| hatred / opposition | `HATES` | 1 |
| captive of / fears | `PRISONER_OF` | 1 |
| resents / fears | `RESENTS` | 1 |
| fears / dislikes | `FEARS` | 1 |
| protects (indirectly) | `PROTECTS` | 1 |
| commands / furious with | `COMMANDS` | 1 |
| captive of / subject to | `PRISONER_OF` | 1 |
| protects / escorts | `PROTECTS` | 1 |
| mocks / threatens | `OPPOSES` | 1 |
| blames for lady's death | `OPPOSES` | 1 |
| antagonizes/disciplines | `OPPOSES` | 1 |
| controls (via proxy) | `COMMANDS` | 1 |
| advises / controls | `ADVISES` | 1 |
| serves as spy for | `SERVES` | 1 |
| contemptuous mentorship of | `HATES` | 1 |
| controls/dominates | `COMMANDS` | 1 |
| resents gendered inequality with | `RESENTS` | 1 |
| protects (possessively) | `PROTECTS` | 1 |
| mourns (implicitly) | `MOURNS` | 1 |
| controls/instructs | `COMMANDS` | 1 |
| sworn to serve | `SWORN_TO` | 1 |
| allied with / serves | `ALLIES_WITH` | 1 |
| brother of / acts for | `SIBLING_OF` | 1 |
| contempt/rivalry toward | `HATES` | 1 |
| wary of ironborn; warned son away from | `DISTRUSTS` | 1 |
| uncle of (absent/unsettling) | `UNCLE_OF` | 1 |
| uncle of (old, cautious) | `UNCLE_OF` | 1 |
| mother of (absent, ill) | `PARENT_OF` | 1 |
| wary of uncle | `DISTRUSTS` | 1 |
| deep affection / mentee | `LOVES` | 1 |
| hatred / defiance | `HATES` | 1 |
| resents/feels rejected by | `RESENTS` | 1 |
| foster-brother of (claimed only by robb) | `WARD_OF` | 1 |
| fear of knowledge held by | `FEARS` | 1 |
| commands / subordinate to | `COMMANDS` | 1 |
| serves (by oath) | `SERVES` | 1 |
| commands (with declining authority) | `COMMANDS` | 1 |
| contemptuous obedience toward | `HATES` | 1 |
| killed (by treachery) | `KILLS` | 1 |
| serves (father appointed him) | `SERVES` | 1 |
| serves / answers to | `SERVES` | 1 |
| formerly served/was bought by | `SERVES` | 1 |
| serves as hand of the king to | `SERVES` | 1 |
| distrusts / fears | `DISTRUSTS` | 1 |
| antagonistic sibling rivalry with | `OPPOSES` | 1 |
| mourns / seeks justice for | `MOURNS` | 1 |
| serves (nervously) | `SERVES` | 1 |
| trusts (with reservation) | `TRUSTS` | 1 |
| commands moon brothers guarding | `COMMANDS` | 1 |
| commands / bantering | `COMMANDS` | 1 |
| contempt toward / antagonism | `HATES` | 1 |
| distrust of all three councilors | `DISTRUSTS` | 1 |
| loyal to (even after death) | `SERVES` | 1 |
| spies on/for | `SPIES_ON` | 1 |
| fears/opposes | `FEARS` | 1 |
| opposes/co-opts | `OPPOSES` | 1 |
| commands / sends into battle | `COMMANDS` | 1 |
| father of / influence on | `PARENT_OF` | 1 |
| serves (as hand) | `SERVES` | 1 |
| protective of / fears for | `PROTECTS` | 1 |
| serves / informs | `SERVES` | 1 |
| seeks favor from | `SEEKS` | 1 |
| commands/directs (acting hand) | `COMMANDS` | 1 |
| trust in (field command) | `TRUSTS` | 1 |
| trust in (operational) | `TRUSTS` | 1 |
| leads / inspires | `COMMANDS` | 1 |
| distrusts / suspects murder plot by | `DISTRUSTS` | 1 |
| trusts more than ballabar | `TRUSTS` | 1 |
| controls / surveils | `COMMANDS` | 1 |
| killed (in defense of tyrion) | `KILLS` | 1 |
| trusts with her identity | `TRUSTS` | 1 |
| seeks / tries to reach | `SEEKS` | 1 |
| trusts / has complicated bond with | `TRUSTS` | 1 |
| resents being controlled by | `RESENTS` | 1 |
| defends memory of | `PROTECTS` | 1 |
| protective of / familiar with | `PROTECTS` | 1 |
| resents class difference with | `RESENTS` | 1 |
| serves as guide/protector to | `SERVES` | 1 |
| serves the memory of | `SERVES` | 1 |
| protective of / restrains | `PROTECTS` | 1 |
| worships / serves as instrument | `WORSHIPS` | 1 |
| protective of / promises ransom | `PROTECTS` | 1 |
| respects justice of | `RESPECTS` | 1 |
| mourns / wishes to resurrect | `MOURNS` | 1 |
| hostile toward / demands gold from | `OPPOSES` | 1 |
| defends clegane's right to live | `PROTECTS` | 1 |
| defends / argues for | `PROTECTS` | 1 |
| betrothed aunt to | `BETROTHED_TO` | 1 |
| mourning / seeking | `MOURNS` | 1 |
| antagonistic toward (implied) | `OPPOSES` | 1 |
| fears reputation of | `FEARS` | 1 |
| hatred tempered by complex feelings | `HATES` | 1 |
| serves / recognizes the coin | `SERVES` | 1 |
| mourns loss of | `MOURNS` | 1 |
| teacher/guide to | `TUTORS` | 1 |
| loyal to house stark | `SERVES` | 1 |
| mourns / worries about | `MOURNS` | 1 |
| protects / leads | `PROTECTS` | 1 |
| advises / counsels | `ADVISES` | 1 |
| wargs into (with difficulty) | `WARGS_INTO` | 1 |
| steward of | `SERVES` | 1 |
| defends against karstark | `PROTECTS` | 1 |
| blames herself for actions that led to | `OPPOSES` | 1 |
| blames directly | `OPPOSES` | 1 |
| defies / disowns as king | `OPPOSES` | 1 |
| executes (as king and kinsman) | `EXECUTES` | 1 |
| seeks guidance from | `SEEKS` | 1 |
| mourns / tends | `MOURNS` | 1 |
| seeks vengeance on | `SEEKS` | 1 |
| distrust/contempt for | `DISTRUSTS` | 1 |
| resents (somewhat) | `RESENTS` | 1 |
| serves/scouts for | `SERVES` | 1 |
| distrusts (for succession) | `DISTRUSTS` | 1 |
| distrusted | `DISTRUSTS` | 1 |
| leads van for | `COMMANDS` | 1 |
| betrothed to (weeping) | `BETROTHED_TO` | 1 |
| mother of (mourning) | `PARENT_OF` | 1 |
| threatens (veiled) | `OPPOSES` | 1 |
| loyal to (absent) | `SERVES` | 1 |
| respects / served under | `RESPECTS` | 1 |
| close companion (deceased) | `COMPANION_OF` | 1 |
| fears retaliation from | `FEARS` | 1 |
| deceives / maintains ruse against | `DECEIVES` | 1 |
| serves / diplomatically protects | `SERVES` | 1 |
| owns / abuses | `OWNS` | 1 |
| advises against slave purchase | `ADVISES` | 1 |
| respects / values counsel of | `RESPECTS` | 1 |
| trusts strategically | `TRUSTS` | 1 |
| mourns / yearns for | `MOURNS` | 1 |
| loyal to / familiar with | `SERVES` | 1 |
| advises (disagreement) | `ADVISES` | 1 |
| contempt/hatred toward | `HATES` | 1 |
| authority over (lost) | `COMMANDS` | 1 |
| resents (memory) | `RESENTS` | 1 |
| commands/queen of | `COMMANDS` | 1 |
| trusts counsel of | `TRUSTS` | 1 |
| loves/loved | `LOVES` | 1 |
| hatred/vendetta toward | `HATES` | 1 |
| opposes/fears | `OPPOSES` | 1 |
| betrays (in stannis's view) | `BETRAYS` | 1 |
| trusts above all remaining lords | `TRUSTS` | 1 |
| blames for sons' deaths | `OPPOSES` | 1 |
| serves as hand and counselor to | `SERVES` | 1 |
| allies with / influences | `ALLIES_WITH` | 1 |
| allied with (secret) | `ALLIES_WITH` | 1 |
| killed by / ran afoul of | `KILLS` | 1 |
| formerly served under | `SERVES` | 1 |
| serves as hand / loyal to but defies in this instance | `SERVES` | 1 |
| opposes / fears the influence of | `OPPOSES` | 1 |
| advises / demands sacrifice from | `ADVISES` | 1 |
| son of (acknowledged bastard) | `PARENT_OF` | 1 |
| son of (despised by) | `PARENT_OF` | 1 |
| brother of (full) | `SIBLING_OF` | 1 |
| serves/is sworn to | `SERVES` | 1 |
| prisoner of / escorted by | `PRISONER_OF` | 1 |
| loathing toward | `HATES` | 1 |
| ward of / taken in by | `WARD_OF` | 1 |
| antagonistic captor-captive evolving toward grudging respect | `OPPOSES` | 1 |
| contempt and hostility toward | `HATES` | 1 |
| loyalty toward | `SERVES` | 1 |
| serves (nominally) | `SERVES` | 1 |
| rescued by/protects | `RESCUES` | 1 |
| threatens/manipulates | `OPPOSES` | 1 |
| father of (secret) | `PARENT_OF` | 1 |
| mourns/avenges | `MOURNS` | 1 |
| loyal to (deceased) | `SERVES` | 1 |
| respects brienne's (grudging) | `RESPECTS` | 1 |
| respects/trusts | `RESPECTS` | 1 |
| manipulates/pleads with | `MANIPULATES` | 1 |
| fears loss of | `FEARS` | 1 |
| bonded to / warg of | `BONDED_TO` | 1 |
| guards/escorts (hostile) | `GUARDS` | 1 |
| protective of jon | `PROTECTS` | 1 |
| antagonistic/mocking | `OPPOSES` | 1 |
| bonded to / sends away reluctantly | `BONDED_TO` | 1 |
| commands / dominates | `COMMANDS` | 1 |
| resents sharing authority with | `RESENTS` | 1 |
| distrusts / watches | `DISTRUSTS` | 1 |
| commands absolutely | `COMMANDS` | 1 |
| bonded to / hopes for communication with | `BONDED_TO` | 1 |
| commands overall force / disdains | `COMMANDS` | 1 |
| serves / represents | `SERVES` | 1 |
| loyal to (secretly) | `SERVES` | 1 |
| mourns/remembers | `MOURNS` | 1 |
| trusts and respects | `TRUSTS` | 1 |
| bonded to / worried about | `BONDED_TO` | 1 |
| friendship with (worried about) | `COMPANION_OF` | 1 |
| enemy of / torturer of | `OPPOSES` | 1 |
| hatred | `HATES` | 1 |
| distrusted by | `DISTRUSTS` | 1 |
| protected by stigma of bastardy | `PROTECTS` | 1 |
| trusts / respects | `TRUSTS` | 1 |
| trusts/delegates to | `TRUSTS` | 1 |
| kills/killed by | `KILLS` | 1 |
| loyal to / follows | `SERVES` | 1 |
| hostile toward / accuses | `OPPOSES` | 1 |
| hostile toward / mocks | `OPPOSES` | 1 |
| defends / respects | `PROTECTS` | 1 |
| hostile toward / lies about | `OPPOSES` | 1 |
| defends honor of | `PROTECTS` | 1 |
| commands/manipulates | `COMMANDS` | 1 |
| advises/manipulates | `ADVISES` | 1 |
| attacks/defeats | `ATTACKS` | 1 |
| trains / mentors | `TEACHES` | 1 |
| serves as advisor / close counselor to | `SERVES` | 1 |
| trusts and credits | `TRUSTS` | 1 |
| trains regularly with | `TEACHES` | 1 |
| bonded to / accompanied by | `BONDED_TO` | 1 |
| protective of raven from | `PROTECTS` | 1 |
| serves/attends | `SERVES` | 1 |
| respects/trusts (dying) | `RESPECTS` | 1 |
| trusts/depends on | `TRUSTS` | 1 |
| fears/seeks approval from | `FEARS` | 1 |
| mourns/remembers fondly | `MOURNS` | 1 |
| advises/promotes | `ADVISES` | 1 |
| respects militarily | `RESPECTS` | 1 |
| commands wardrobe for | `COMMANDS` | 1 |
| leads/rules | `COMMANDS` | 1 |
| teaches harp to | `TEACHES` | 1 |
| distrusts/rejects plan of | `DISTRUSTS` | 1 |
| threatens / humiliates | `OPPOSES` | 1 |
| controls information about | `COMMANDS` | 1 |
| serves (with attitude) | `SERVES` | 1 |
| serves (deferentially) | `SERVES` | 1 |
| protects / manipulates | `PROTECTS` | 1 |
| manipulates / murders | `MANIPULATES` | 1 |
| fears / is repulsed by | `FEARS` | 1 |
| resents her father for | `RESENTS` | 1 |
| fears and suspects | `FEARS` | 1 |
| antagonistic submission to | `OPPOSES` | 1 |
| antagonistic son of | `OPPOSES` | 1 |
| spies on tyrion for | `SPIES_ON` | 1 |
| manipulates through implied sexual favors | `MANIPULATES` | 1 |
| serves as maidservant to (cover identity) | `SERVES` | 1 |
| mourns / loves (unnamed person) | `MOURNS` | 1 |
| serves as vanguard for | `SERVES` | 1 |
| son of (strained, subservient) | `PARENT_OF` | 1 |
| loyal to (for pay) | `SERVES` | 1 |
| distrusts/resents | `DISTRUSTS` | 1 |
| hatred from infancy | `HATES` | 1 |
| deep love (past) | `LOVES` | 1 |
| contempt/blame | `HATES` | 1 |
| fears punishment from | `FEARS` | 1 |
| manipulates/interacts with | `MANIPULATES` | 1 |
| respects/defends | `RESPECTS` | 1 |
| loves/defends | `LOVES` | 1 |
| distrusts/disdains | `DISTRUSTS` | 1 |
| betrayed by (former lover) | `BETRAYS` | 1 |
| contempt for / anger toward | `HATES` | 1 |
| respects (grudging) | `RESPECTS` | 1 |
| serves / protects | `SERVES` | 1 |
| enemies / kill list | `OPPOSES` | 1 |
| student/novice under | `TUTORS` | 1 |
| contempt/affection toward | `HATES` | 1 |
| sworn to serve / searching for | `SWORN_TO` | 1 |
| squire to (abandoned) | `SERVES` | 1 |
| betrothed to (past, ended by death) | `BETROTHED_TO` | 1 |
| distrusts/employs as guide | `DISTRUSTS` | 1 |
| resents memory of | `RESENTS` | 1 |
| searching for | `SEEKS` | 1 |
| killed (dismembered) | `KILLS` | 1 |
| contempt/hostility toward | `HATES` | 1 |
| serves as knight to | `SERVES` | 1 |
| rules in place of | `RULES` | 1 |
| seeks to punish | `SEEKS` | 1 |
| defends / trusts | `PROTECTS` | 1 |
| loves (romantic) | `LOVES` | 1 |
| serves (reluctantly) | `SERVES` | 1 |
| gave life to resurrect | `GIFTED_TO` | 1 |
| killed (stated) | `KILLS` | 1 |
| daughter of (grieving, complex) | `PARENT_OF` | 1 |
| hatred / fear | `HATES` | 1 |
| contempt / resentment (retroactive) | `HATES` | 1 |
| daughter of (grieving) | `PARENT_OF` | 1 |
| niece of / in conflict with | `UNCLE_OF` | 1 |
| rival of | `OPPOSES` | 1 |
| cousin of / former lover of | `COUSIN_OF` | 1 |
| hostile toward / distrusts | `OPPOSES` | 1 |
| loyal to / protective of | `SERVES` | 1 |
| serves/informs | `SERVES` | 1 |
| blames for joffrey's death | `OPPOSES` | 1 |
| hatred/bitter memory of | `HATES` | 1 |
| contempt/suspicion toward | `HATES` | 1 |
| mother of (controlling) | `PARENT_OF` | 1 |
| loyal to/loves | `SERVES` | 1 |
| serves/enables | `SERVES` | 1 |
| manipulates/appoints | `MANIPULATES` | 1 |
| serves as torturer | `SERVES` | 1 |
| serves both queens | `SERVES` | 1 |
| fears prophecy of | `FEARS` | 1 |
| tortures | `TORTURES` | 1 |
| opposes (implied) | `OPPOSES` | 1 |
| contempt for / views as dying | `HATES` | 1 |
| commands / rebukes | `COMMANDS` | 1 |
| son of (mourning) | `PARENT_OF` | 1 |
| nephew of (attempting reconciliation) | `NEPHEW_OF` | 1 |
| cousin of (suspicious of) | `COUSIN_OF` | 1 |
| respects the skill of | `RESPECTS` | 1 |
| mother of (governs in name of) | `PARENT_OF` | 1 |
| protects / defends honor of | `PROTECTS` | 1 |
| distrusts / opposes | `DISTRUSTS` | 1 |
| contempt mixed with pity for | `HATES` | 1 |
| loves/mourns | `LOVES` | 1 |
| resentment/frustration | `RESENTS` | 1 |
| contempt for father | `HATES` | 1 |
| commands/manages | `COMMANDS` | 1 |
| controls/overrides | `COMMANDS` | 1 |
| protects/defends | `PROTECTS` | 1 |
| serves (resentfully) | `SERVES` | 1 |
| resents/fears | `RESENTS` | 1 |
| respects/fears (implied) | `RESPECTS` | 1 |
| skeptical of / disapproves of | `DISTRUSTS` | 1 |
| serves / sworn to | `SERVES` | 1 |
| mourns (believes dead) | `MOURNS` | 1 |
| resents (mild) | `RESENTS` | 1 |
| threatens (indirectly) | `OPPOSES` | 1 |
| protects/guards | `PROTECTS` | 1 |
| respects/serves | `RESPECTS` | 1 |
| resents / blames | `RESENTS` | 1 |
| blames / questions | `OPPOSES` | 1 |
| mourns / reveres | `MOURNS` | 1 |
| loves / desires | `LOVES` | 1 |
| fears (past) | `FEARS` | 1 |
| advises / cares for | `ADVISES` | 1 |
| gave away sword to repay | `GIFTED_TO` | 1 |
| distrusts interpretation of | `DISTRUSTS` | 1 |
| contempt/mockery toward | `HATES` | 1 |
| trust in | `TRUSTS` | 1 |
| loyal to / dependent on | `SERVES` | 1 |
| guards/protects | `GUARDS` | 1 |
| sibling of (deceased) | `SIBLING_OF` | 1 |
| fears and opposes | `FEARS` | 1 |
| brother of / brought bride for | `SIBLING_OF` | 1 |
| father of (inferred) | `PARENT_OF` | 1 |
| slew | `KILLS` | 1 |
| mocks / challenges | `OPPOSES` | 1 |
| killed his salt wife because of | `KILLS` | 1 |
| worships | `WORSHIPS` | 1 |
| respects tradition of | `RESPECTS` | 1 |
| loves (familial) | `LOVES` | 1 |
| brother of (deceased) | `SIBLING_OF` | 1 |
| seeks vengeance for | `SEEKS` | 1 |
| fostered | `WARD_OF` | 1 |
| fears/dreads | `FEARS` | 1 |
| killed (by drowning) | `KILLS` | 1 |
| father of nine sons | `PARENT_OF` | 1 |
| resentment / defiance toward | `RESENTS` | 1 |
| contempt / provocation | `HATES` | 1 |
| serves / loyal instrument | `SERVES` | 1 |
| daughter of / politically opposed to | `PARENT_OF` | 1 |
| fostered by | `WARD_OF` | 1 |
| opposes / despises | `OPPOSES` | 1 |
| distrusts / threatens | `DISTRUSTS` | 1 |
| protects / cares for | `PROTECTS` | 1 |
| serves / sent by | `SERVES` | 1 |
| student / apprentice to | `TUTORS` | 1 |
| fear of becoming | `FEARS` | 1 |
| serves as justiciar to | `SERVES` | 1 |
| serves as lord admiral to | `SERVES` | 1 |
| hates / vows revenge on | `HATES` | 1 |
| ally of / relies on | `ALLIES_WITH` | 1 |
| contempt for / politically opposed to | `HATES` | 1 |
| daughter of / reveres | `PARENT_OF` | 1 |
| contempt tempered by need | `HATES` | 1 |
| opposes/moderates | `OPPOSES` | 1 |
| serves as envoy for | `SERVES` | 1 |
| distrusts but needs | `DISTRUSTS` | 1 |
| protects violently | `PROTECTS` | 1 |
| trusts more than hizdahr | `TRUSTS` | 1 |
| kills own men for disloyalty | `KILLS` | 1 |
| commands / frustrated with | `COMMANDS` | 1 |
| trains/mentors | `TEACHES` | 1 |
| rules / mother figure to | `RULES` | 1 |
| mourns betrayal by | `MOURNS` | 1 |
| opposes / distrusts | `OPPOSES` | 1 |
| killed (a mutinous serjeant) | `KILLS` | 1 |
| serves / close to | `SERVES` | 1 |
| betrothed to / marries | `BETROTHED_TO` | 1 |
| dismissive of / hostile toward | `DISTRUSTS` | 1 |
| protective of / disapproving of daario with | `PROTECTS` | 1 |
| respects lineage of | `RESPECTS` | 1 |
| mother of (reconnection) | `PARENT_OF` | 1 |
| mourns/misses | `MOURNS` | 1 |
| serves as hand | `SERVES` | 1 |
| killed son of | `KILLS` | 1 |
| rules | `RULES` | 1 |
| serves as hand/envoy | `SERVES` | 1 |
| father of (deceased) | `PARENT_OF` | 1 |
| allied with / complicit with | `ALLIES_WITH` | 1 |
| loyalty to memory of | `SERVES` | 1 |
| sworn to / serves | `SWORN_TO` | 1 |
| serves/supports | `SERVES` | 1 |
| nephew of (blood relation estranged from) | `NEPHEW_OF` | 1 |
| commands (new/uncomfortable) | `COMMANDS` | 1 |
| defies / maintains independence from | `OPPOSES` | 1 |
| threatens / pressures | `OPPOSES` | 1 |
| wary of / distrusts | `DISTRUSTS` | 1 |
| grieves / remembers | `MOURNS` | 1 |
| controls / uses | `COMMANDS` | 1 |
| resents / frustrated by | `RESENTS` | 1 |
| serves / supports | `SERVES` | 1 |
| trusts/relies on | `TRUSTS` | 1 |
| allied with/pleading for | `ALLIES_WITH` | 1 |
| grieves separation from | `MOURNS` | 1 |
| serves under / disagrees with | `SERVES` | 1 |
| serves (lord commander) | `SERVES` | 1 |
| advises (lord steward) | `ADVISES` | 1 |
| serves/companions | `SERVES` | 1 |
| advises (strategic) | `ADVISES` | 1 |
| controls/binds | `COMMANDS` | 1 |
| antagonizes/disrespects | `OPPOSES` | 1 |
| defends/mediates | `PROTECTS` | 1 |
| blames/resents | `OPPOSES` | 1 |
| mourns / misses | `MOURNS` | 1 |
| sibling of | `SIBLING_OF` | 1 |
| antagonistic toward / hostile to | `OPPOSES` | 1 |
| protective of / loyal to | `PROTECTS` | 1 |
| seeks alliance with / offers help to | `SEEKS` | 1 |
| respects teaching of | `RESPECTS` | 1 |
| respects / works with | `RESPECTS` | 1 |
| loves / fears for | `LOVES` | 1 |
| distrusts (inherited) | `DISTRUSTS` | 1 |
| mourns / honors | `MOURNS` | 1 |
| allied with / commands | `ALLIES_WITH` | 1 |
| respects / cooperates with | `RESPECTS` | 1 |
| opposes / resents | `OPPOSES` | 1 |
| antagonistic | `OPPOSES` | 1 |
| distrusts (some) | `DISTRUSTS` | 1 |
| allied with / trusts | `ALLIES_WITH` | 1 |
| dismissive of / antagonistic toward | `DISTRUSTS` | 1 |
| advises / warns | `ADVISES` | 1 |
| commands (prisoner) | `COMMANDS` | 1 |
| seeks to manipulate/win trust of | `SEEKS` | 1 |
| protects (secretly) | `PROTECTS` | 1 |
| controls via glamor magic | `COMMANDS` | 1 |
| commands/silences | `COMMANDS` | 1 |
| sees as doomed people | `PERCEIVED_AS` | 1 |
| killed and consumed | `KILLS` | 1 |
| killed (accidentally via warging) | `KILLS` | 1 |
| gave away | `GIFTED_TO` | 1 |
| betrothed | `BETROTHED_TO` | 1 |
| distrusts/fears assassination | `DISTRUSTS` | 1 |
| friend of (posed identity) | `COMPANION_OF` | 1 |
| resents authority of | `RESENTS` | 1 |
| controls through gifts | `COMMANDS` | 1 |
| serves as agent for | `SERVES` | 1 |
| trusts (slightly) | `TRUSTS` | 1 |
| resentment (memory) | `RESENTS` | 1 |
| hatred/kill list | `HATES` | 1 |
| protective of / fights for | `PROTECTS` | 1 |
| serves under / allied with | `SERVES` | 1 |
| cousin of (deceased) | `COUSIN_OF` | 1 |
| opposes (strategically) | `OPPOSES` | 1 |
| gave (as gift/burden) to | `GIFTED_TO` | 1 |
| gave (as imposed maester) to | `GIFTED_TO` | 1 |
| killed (recalled) | `KILLS` | 1 |
| serves as second-in-command to | `SERVES` | 1 |
| resentment / forced cooperation | `RESENTS` | 1 |
| resentment / distrust | `RESENTS` | 1 |
| hatred of | `HATES` | 1 |
| close companion / defers to judgment of | `COMPANION_OF` | 1 |
| close companion of | `COMPANION_OF` | 1 |
| mourns / feels the loss most keenly of | `MOURNS` | 1 |
| serves / obeys mission from | `SERVES` | 1 |
| fears the scorn of | `FEARS` | 1 |
| serves / protects (loyal to absent queen) | `SERVES` | 1 |
| respects cautiously | `RESPECTS` | 1 |
| antagonizes / disrespects | `OPPOSES` | 1 |
| blames / resents | `OPPOSES` | 1 |
| loyal to (in death) | `SERVES` | 1 |
| serves (diplomatic envoy) | `SERVES` | 1 |
| mocks / disrespects | `OPPOSES` | 1 |
| commands (officially) through cousin | `COMMANDS` | 1 |
| hates; accuses of poisoning | `HATES` | 1 |
| loyal to; takes commands only from | `SERVES` | 1 |
| loves and is devoted to | `LOVES` | 1 |
| seeks audience with | `SEEKS` | 1 |
| gave theon/girl to | `GIFTED_TO` | 1 |
| close friend / advisor to | `COMPANION_OF` | 1 |
| close friend / loyal companion to | `COMPANION_OF` | 1 |
| ward/foster son of | `WARD_OF` | 1 |
| hostile toward / mistrustful of | `OPPOSES` | 1 |
| allied with / urging action from | `ALLIES_WITH` | 1 |
| controls / commands | `COMMANDS` | 1 |
| controls access / holds | `COMMANDS` | 1 |
| hostile toward (implied) | `OPPOSES` | 1 |
| seeks information from | `SEEKS` | 1 |
| fostered with | `WARD_OF` | 1 |
| kills (indirectly) | `KILLS` | 1 |
| wary of / resists | `DISTRUSTS` | 1 |
| distrusts (initially) | `DISTRUSTS` | 1 |
| lovers | `LOVER_OF` | 1 |
| son of / sent by | `PARENT_OF` | 1 |
| serves as right hand to | `SERVES` | 1 |
| serves as left hand to | `SERVES` | 1 |
| commands (mission) | `COMMANDS` | 1 |
| killed slave girl of | `KILLS` | 1 |
| killed boy of | `KILLS` | 1 |
| fears/dreads meeting | `FEARS` | 1 |
| fears/is terrorized by | `FEARS` | 1 |
| protects/commits to | `PROTECTS` | 1 |
| distrusts/despises | `DISTRUSTS` | 1 |
| loyal to/follows | `SERVES` | 1 |
| rescued/escorted | `RESCUES` | 1 |
| seeks death of | `SEEKS` | 1 |
| grieves/obsesses over | `MOURNS` | 1 |
| serves/allies with | `SERVES` | 1 |
| serves / knighted by | `SERVES` | 1 |
| killed (confirmed) | `KILLS` | 1 |
| commands / controls | `COMMANDS` | 1 |
| trains / sparring partner | `TEACHES` | 1 |
| defeats | `DEFEATS` | 1 |
| tutors | `TUTORS` | 1 |
| resentment / dark satisfaction | `RESENTS` | 1 |
| protective of / devoted to | `PROTECTS` | 1 |
| rescued from drowning | `RESCUES` | 1 |
| captures | `CAPTURES` | 1 |
| betrayed by | `BETRAYS` | 1 |
| blames / slowly forgiving | `OPPOSES` | 1 |
| distrustful wariness toward | `DISTRUSTS` | 1 |
| antagonistic cohabitation | `OPPOSES` | 1 |
| contempt / dark memory | `HATES` | 1 |
| contempt for / fear of | `HATES` | 1 |
| protective of / lies to | `PROTECTS` | 1 |
| contempt/pity for | `HATES` | 1 |
| killed (prior) | `KILLS` | 1 |
| commands/captains | `COMMANDS` | 1 |
| contempt toward (private) | `HATES` | 1 |
| serves / flatters | `SERVES` | 1 |
| admires / follows | `RESPECTS` | 1 |
| sister, hostile/estranged | `SIBLING_OF` | 1 |
| daughter, deep love/trust | `LOVES` | 1 |
| grief/guilt over | `MOURNS` | 1 |
| guard/fond of | `LOVES` | 1 |
| misses, wishes for | `MOURNS` | 1 |
| follows sister's lead | `SIBLING_OF` | 1 |
| protective companion | `COMPANION_OF` | 1 |
| concerned brother | `SIBLING_OF` | 1 |
| brotherly affection | `LOVES` | 1 |
| great-grandmother of | `PARENT_OF` | 1 |
| brother, looks up to | `SIBLING_OF` | 1 |
| apparent friendship but anger | `COMPANION_OF` | 1 |
| grief / fond memory | `MOURNS` | 1 |
| missing | `MOURNS` | 1 |
| acting lord, receives counsel | `ADVISES` | 1 |
| brother, subordinate to | `SIBLING_OF` | 1 |
| blunt respect toward | `RESPECTS` | 1 |
| misses, prays for | `MOURNS` | 1 |
| grieving/desperate for | `MOURNS` | 1 |
| deep friendship with | `COMPANION_OF` | 1 |
| wife, political counselor | `ADVISES` | 1 |
| was originally betrothed to | `BETROTHED_TO` | 1 |
| married in place of his dead brother | `SIBLING_OF` | 1 |
| sister, shared childhood language | `SIBLING_OF` | 1 |
| trusted counselor and advisor to | `ADVISES` | 1 |
| concern for / mentoring | `TUTORS` | 1 |
| mother, proud and mentoring | `TUTORS` | 1 |
| brother, acting protector | `SIBLING_OF` | 1 |
| brother, frustrated caretaker | `SIBLING_OF` | 1 |
| wife, resentful of ned's departure | `RESENTS` | 1 |
| master-at-arms, mentor | `TUTORS` | 1 |
| sister | `SIBLING_OF` | 1 |
| protector, bonded | `BONDED_TO` | 1 |
| childhood acquaintance / object of affection | `LOVES` | 1 |
| claims friendship with | `COMPANION_OF` | 1 |
| traveling companion / protected by | `COMPANION_OF` | 1 |
| traveling companion of | `COMPANION_OF` | 1 |
| niece, warmly affectionate | `UNCLE_OF` | 1 |
| protective uncle, candid advisor | `UNCLE_OF` | 1 |
| growing alliance with | `ALLIES_WITH` | 1 |
| captor (increasingly uncertain) | `CAPTURES` | 1 |
| sister, hostile despite initial warmth | `SIBLING_OF` | 1 |
| resentful contempt toward | `RESENTS` | 1 |
| in love with | `LOVES` | 1 |
| sister (strained) | `SIBLING_OF` | 1 |
| niece-uncle (trusting alliance) | `UNCLE_OF` | 1 |
| nephew-sister (ruptured) | `NEPHEW_OF` | 1 |
| former betrothed (memory) | `BETROTHED_TO` | 1 |
| unrequited love (memory) | `LOVES` | 1 |
| captor (nominal) | `CAPTURES` | 1 |
| sister-in-law of | `IN_LAW_OF` | 1 |
| niece to | `UNCLE_OF` | 1 |
| friendlier with than expected | `COMPANION_OF` | 1 |
| uncle and military advisor to | `UNCLE_OF` | 1 |
| ally who joined march | `ALLIES_WITH` | 1 |
| subordinate to / acting lord for | `SERVES` | 1 |
| protective/respectful toward | `RESPECTS` | 1 |
| growing bond / love for | `LOVES` | 1 |
| tries to command | `COMMANDS` | 1 |
| commanded by / assigned | `COMMANDS` | 1 |
| wife / subordinate in public, persuader in private | `SERVES` | 1 |
| handmaid, affectionate | `LOVES` | 1 |
| grief / complicated memory | `MOURNS` | 1 |
| informant / ally | `ALLIES_WITH` | 1 |
| respectful / protective of guest peace | `RESPECTS` | 1 |
| resentful of | `RESENTS` | 1 |
| refuses counsel of | `ADVISES` | 1 |
| wife/lover of (ending) | `LOVER_OF` | 1 |
| references past love for | `LOVES` | 1 |
| deep old friendship with, now subject to | `COMPANION_OF` | 1 |
| enduring love/obsession for | `LOVES` | 1 |
| grief and love for | `MOURNS` | 1 |
| grief and admiration for | `MOURNS` | 1 |
| grief and respect for | `MOURNS` | 1 |
| undying love / grief | `MOURNS` | 1 |
| respect / inadequacy | `RESPECTS` | 1 |
| respect tinged with regret | `RESPECTS` | 1 |
| past love | `LOVES` | 1 |
| evasion/fear | `FEARS` | 1 |
| irritation with brother | `SIBLING_OF` | 1 |
| compassion, grief | `MOURNS` | 1 |
| reluctant political ally | `ALLIES_WITH` | 1 |
| claims mentorship of | `TUTORS` | 1 |
| ally (claimed) of | `ALLIES_WITH` | 1 |
| assigns command to | `COMMANDS` | 1 |
| deep old friendship with | `COMPANION_OF` | 1 |
| still mourns/loves | `MOURNS` | 1 |
| secret counselor to | `ADVISES` | 1 |
| respected by / loyal to | `RESPECTS` | 1 |
| bitter guilt about | `RESENTS` | 1 |
| sides with / respects | `RESPECTS` | 1 |
| protective brother to | `SIBLING_OF` | 1 |
| grief/guilt about | `MOURNS` | 1 |
| allegedly murdered children of | `KILLS` | 1 |
| subordinate/hand to | `SERVES` | 1 |
| deep old friendship with tension | `COMPANION_OF` | 1 |
| obsessive grief/loss | `MOURNS` | 1 |
| grief/loyalty for | `MOURNS` | 1 |
| respect/bonds with | `RESPECTS` | 1 |
| lover of (since childhood) | `LOVER_OF` | 1 |
| feels duty toward / mourns | `MOURNS` | 1 |
| deep friendship, grief at impending loss | `MOURNS` | 1 |
| brotherly admiration mixed with pragmatism | `RESPECTS` | 1 |
| proposes alliance / political urgency | `ALLIES_WITH` | 1 |
| refuses alliance on moral grounds | `ALLIES_WITH` | 1 |
| reassurance / respect | `RESPECTS` | 1 |
| professed love (used as leverage) | `LOVES` | 1 |
| defiant/resentful toward | `RESENTS` | 1 |
| deep grief for | `MOURNS` | 1 |
| nephew (warm affection) | `NEPHEW_OF` | 1 |
| admiration toward | `RESPECTS` | 1 |
| old friendship (strained) | `COMPANION_OF` | 1 |
| brother (mocking affection) | `SIBLING_OF` | 1 |
| brotherly love / deep bond | `LOVES` | 1 |
| close, affectionate brothers | `LOVES` | 1 |
| anticipation / respect | `RESPECTS` | 1 |
| loyal companion / emotional support | `COMPANION_OF` | 1 |
| obedient companion | `COMPANION_OF` | 1 |
| loyal companion | `COMPANION_OF` | 1 |
| conspiratorial exclusion | `CONSPIRES_WITH` | 1 |
| mentors/rebukes | `TUTORS` | 1 |
| misses (complex) | `MOURNS` | 1 |
| receives counsel from | `ADVISES` | 1 |
| leader/respected figure among recruits | `RESPECTS` | 1 |
| loyal ally | `ALLIES_WITH` | 1 |
| loyal ally (with initial reluctance) | `ALLIES_WITH` | 1 |
| initially obedient to thorne, later allied with jon | `ALLIES_WITH` | 1 |
| brother-like bond / memories | `SIBLING_OF` | 1 |
| background friendship | `COMPANION_OF` | 1 |
| intellectual respect / recalled connection | `RESPECTS` | 1 |
| friendship / protectiveness | `COMPANION_OF` | 1 |
| loyalty / refusal to grieve | `MOURNS` | 1 |
| respect / seeks help from | `RESPECTS` | 1 |
| mentorship / respect toward | `RESPECTS` | 1 |
| love / grief | `MOURNS` | 1 |
| complex feeling (love, shame, confusion) | `LOVES` | 1 |
| recalls / respects | `RESPECTS` | 1 |
| loyalty and love toward | `LOVES` | 1 |
| remembered friendship with | `COMPANION_OF` | 1 |
| rewards/mentors | `TUTORS` | 1 |
| counsels/tests | `ADVISES` | 1 |
| respected | `RESPECTS` | 1 |
| grieved for | `MOURNS` | 1 |
| brotherhood/deep friendship | `COMPANION_OF` | 1 |
| filial devotion/grief | `MOURNS` | 1 |
| commander/steward loyalty | `COMMANDS` | 1 |
| mentorship/authority | `TUTORS` | 1 |
| respect/reliance | `RESPECTS` | 1 |
| strained love | `LOVES` | 1 |
| shame/grief | `MOURNS` | 1 |
| intellectual respect | `RESPECTS` | 1 |
| subordinate to / respects authority of | `RESPECTS` | 1 |
| companion/friend | `COMPANION_OF` | 1 |
| fear evolving to empathy toward | `FEARS` | 1 |
| possessive/commanding toward | `COMMANDS` | 1 |
| fear/revulsion toward | `FEARS` | 1 |
| refuses subordination to | `SERVES` | 1 |
| uncle, disciplinarian | `UNCLE_OF` | 1 |
| affection/gratitude despite differences | `LOVES` | 1 |
| twin, co-conspirator | `CONSPIRES_WITH` | 1 |
| intellectual respect toward | `RESPECTS` | 1 |
| reluctant traveling companion / mutual antagonism | `COMPANION_OF` | 1 |
| mentoring / kinship of outsiders | `TUTORS` | 1 |
| bonded with / protected by | `BONDED_TO` | 1 |
| protective uncle | `UNCLE_OF` | 1 |
| admiration / comparison | `RESPECTS` | 1 |
| captor / escort of | `CAPTURES` | 1 |
| pities / respects | `RESPECTS` | 1 |
| friendship / trust | `COMPANION_OF` | 1 |
| grief/bitterness over | `MOURNS` | 1 |
| sister (tense) | `SIBLING_OF` | 1 |
| brother, relies on reputation of | `SIBLING_OF` | 1 |
| mutual pragmatic respect with | `RESPECTS` | 1 |
| lasting grief over | `MOURNS` | 1 |
| offers alliance to | `ALLIES_WITH` | 1 |
| nephew/uncle | `NEPHEW_OF` | 1 |
| brother (compared to) | `SIBLING_OF` | 1 |
| brother, defers to his authority | `SIBLING_OF` | 1 |
| commander of (nominal) | `COMMANDS` | 1 |
| lover | `LOVER_OF` | 1 |
| subordinate to / protected by | `SERVES` | 1 |
| admires/mourns | `MOURNS` | 1 |
| relies on / commands | `COMMANDS` | 1 |
| protective alliance with | `ALLIES_WITH` | 1 |
| has bed-companion | `COMPANION_OF` | 1 |
| conflicted friendship with | `COMPANION_OF` | 1 |
| frustrated alliance with | `ALLIES_WITH` | 1 |
| feels fear toward | `FEARS` | 1 |
| looks up to / misses | `MOURNS` | 1 |
| mentor/advisor to | `TUTORS` | 1 |
| grief/isolation | `MOURNS` | 1 |
| camaraderie with | `COMPANION_OF` | 1 |
| friendship/affection | `LOVES` | 1 |
| relied on counsel of | `ADVISES` | 1 |
| mentors/teaches | `TUTORS` | 1 |
| abused/murdered | `KILLS` | 1 |
| pack brother of | `SIBLING_OF` | 1 |
| final counsel to | `ADVISES` | 1 |
| ward/companion of | `COMPANION_OF` | 1 |
| married to (political alliance) | `ALLIES_WITH` | 1 |
| devotion/love toward | `LOVES` | 1 |
| offered alliance to (rejected) | `ALLIES_WITH` | 1 |
| bitter rivalry / refuses to yield | `RESENTS` | 1 |
| military counsel | `ADVISES` | 1 |
| strategic counsel (overruled) | `ADVISES` | 1 |
| mother, grieving separation | `MOURNS` | 1 |
| widow, mourning | `MOURNS` | 1 |
| protective ally | `ALLIES_WITH` | 1 |
| younger brother, rival | `SIBLING_OF` | 1 |
| values/respects | `RESPECTS` | 1 |
| wary respect toward | `RESPECTS` | 1 |
| sister/loving concern | `SIBLING_OF` | 1 |
| prior betrothal (past) | `BETROTHED_TO` | 1 |
| longing for counsel | `ADVISES` | 1 |
| captor of (adversarial) | `CAPTURES` | 1 |
| conflicted love/hate for | `LOVES` | 1 |
| bonded protector | `BONDED_TO` | 1 |
| longing/mourning | `MOURNS` | 1 |
| grief for / resentment toward | `MOURNS` | 1 |
| mercenary ally of | `ALLIES_WITH` | 1 |
| grief/love for | `MOURNS` | 1 |
| maternal grandfather of | `PARENT_OF` | 1 |
| friendship/brotherhood | `COMPANION_OF` | 1 |
| uncle/nephew bond with | `NEPHEW_OF` | 1 |
| remembers/misses | `MOURNS` | 1 |
| friendship/protectiveness | `COMPANION_OF` | 1 |
| resentful hostility from | `RESENTS` | 1 |
| warm camaraderie with | `COMPANION_OF` | 1 |
| friendly familiarity with | `COMPANION_OF` | 1 |
| distant affection for | `LOVES` | 1 |
| bond/warging connection with | `WARGS_INTO` | 1 |
| protective/warning behavior toward | `ADVISES` | 1 |
| mentors / respects | `RESPECTS` | 1 |
| chafes under command of | `COMMANDS` | 1 |
| concern/grief for | `MOURNS` | 1 |
| fearful, possibly insubordinate | `FEARS` | 1 |
| thinks of / misses | `MOURNS` | 1 |
| mentor/tests | `TUTORS` | 1 |
| former friend/brother of | `SIBLING_OF` | 1 |
| obeys/follows orders of | `SERVES` | 1 |
| paternal love / failed guardian | `LOVES` | 1 |
| paternal love | `LOVES` | 1 |
| cold duty / no affection | `LOVES` | 1 |
| trust / affection | `LOVES` | 1 |
| compassion / respect | `RESPECTS` | 1 |
| respectful but supplanting | `RESPECTS` | 1 |
| former love turned revulsion | `LOVES` | 1 |
| entering secret alliance with | `ALLIES_WITH` | 1 |
| grandfather served | `PARENT_OF` | 1 |
| grudging respect/attraction to strength of | `RESPECTS` | 1 |
| uneasy subordination to | `SERVES` | 1 |
| cousin, subordinate to | `COUSIN_OF` | 1 |
| complicated fear/sympathy toward | `FEARS` | 1 |
| would-be protector/admirer of | `RESPECTS` | 1 |
| grandfather / authority over | `PARENT_OF` | 1 |
| sets aside betrothal to | `BETROTHED_TO` | 1 |
| affection for (as younger brother) | `SIBLING_OF` | 1 |
| priest-uncle, chilly and pious | `UNCLE_OF` | 1 |
| friendly with / missed | `MOURNS` | 1 |
| brother (estranged) | `SIBLING_OF` | 1 |
| respected by ironborn | `RESPECTS` | 1 |
| resentful | `RESENTS` | 1 |
| nephew / subordinate tension | `NEPHEW_OF` | 1 |
| commander (resented) | `COMMANDS` | 1 |
| conflicted former companion | `COMPANION_OF` | 1 |
| mentor / warmth | `TUTORS` | 1 |
| grudging respect for counsel of | `RESPECTS` | 1 |
| forsaken by sister | `SIBLING_OF` | 1 |
| forsaken by uncle(s) | `UNCLE_OF` | 1 |
| subordinate (claims allegiance) | `SERVES` | 1 |
| siblings — hostile, manipulative, mistrustful | `DISTRUSTS` | 1 |
| alliance of convenience | `ALLIES_WITH` | 1 |
| lover — tender, possessive, self-aware | `LOVER_OF` | 1 |
| wary mutual respect / adversarial intelligence | `RESPECTS` | 1 |
| fond of / protects | `LOVES` | 1 |
| kingsguard — obeys cersei | `SERVES` | 1 |
| secret alliance / mutual wariness with | `ALLIES_WITH` | 1 |
| keeping secret lover | `LOVER_OF` | 1 |
| sardonic affection for | `LOVES` | 1 |
| professional respect | `RESPECTS` | 1 |
| longing for / admires | `RESPECTS` | 1 |
| resentful of / dependent on | `RESENTS` | 1 |
| admiration (performed or genuine) | `RESPECTS` | 1 |
| grievance toward | `MOURNS` | 1 |
| lover of (cersei's perspective) | `LOVER_OF` | 1 |
| devotion / grief-rage for | `MOURNS` | 1 |
| unexpected affection toward | `LOVES` | 1 |
| uncle/protector of | `UNCLE_OF` | 1 |
| hostile uncle/guardian of | `UNCLE_OF` | 1 |
| receives honest counsel from | `ADVISES` | 1 |
| momentary ally of | `ALLIES_WITH` | 1 |
| lover of / depends on | `LOVER_OF` | 1 |
| feels dependent on / affection for | `LOVES` | 1 |
| respect mixed with humor toward | `RESPECTS` | 1 |
| employer / commands | `COMMANDS` | 1 |
| protective uncle toward | `UNCLE_OF` | 1 |
| does not miss | `MOURNS` | 1 |
| fearful subordinate to | `FEARS` | 1 |
| admires recklessness of | `RESPECTS` | 1 |
| captured / holds hostage | `PRISONER_OF` | 1 |
| subordinate to (in practice) | `SERVES` | 1 |
| commander, flanked by | `COMMANDS` | 1 |
| battlefield ally | `ALLIES_WITH` | 1 |
| brother, first thought when saved | `SIBLING_OF` | 1 |
| remembers with affection | `LOVES` | 1 |
| admires enemy courage | `RESPECTS` | 1 |
| love / loss / bitterness toward | `LOVES` | 1 |
| misses / loves | `MOURNS` | 1 |
| friendship / loss | `COMPANION_OF` | 1 |
| deference / affection toward | `LOVES` | 1 |
| friendship / rivalry with | `COMPANION_OF` | 1 |
| longs for / worries about rejection from | `MOURNS` | 1 |
| longs for / identifies with family of | `MOURNS` | 1 |
| drinking companion of | `COMPANION_OF` | 1 |
| familiar/affectionate toward | `LOVES` | 1 |
| longs for connection with | `MOURNS` | 1 |
| formerly admired by | `RESPECTS` | 1 |
| grief/accusation toward | `MOURNS` | 1 |
| competitive camaraderie with | `COMPANION_OF` | 1 |
| respectful of past | `RESPECTS` | 1 |
| grief and desperate love | `MOURNS` | 1 |
| desperate love, desire to rescue | `LOVES` | 1 |
| memory of lost friendship | `COMPANION_OF` | 1 |
| recalled friendship | `COMPANION_OF` | 1 |
| captive / reluctant companion of | `COMPANION_OF` | 1 |
| spiritually bonded with | `BONDED_TO` | 1 |
| captor / protector of | `CAPTURES` | 1 |
| captor-captive / reluctant companionship | `CAPTURES` | 1 |
| warg-bonded to | `WARGS_INTO` | 1 |
| friendly teasing with | `COMPANION_OF` | 1 |
| misses and worries about | `MOURNS` | 1 |
| warges into (first time) | `WARGS_INTO` | 1 |
| brotherly affection for | `LOVES` | 1 |
| loved but returned to justice | `LOVES` | 1 |
| murdered (believed) | `KILLS` | 1 |
| warm, affectionate | `LOVES` | 1 |
| in love, protective | `LOVES` | 1 |
| strategic counsel to | `ADVISES` | 1 |
| broken alliance with | `ALLIES_WITH` | 1 |
| counsels / mentors | `TUTORS` | 1 |
| sister, advisor to | `SIBLING_OF` | 1 |
| daughter mourning | `MOURNS` | 1 |
| husband, affectionate to | `LOVES` | 1 |
| grieving son of | `MOURNS` | 1 |
| supportive uncle to | `UNCLE_OF` | 1 |
| brother of, avoids after rebuke | `SIBLING_OF` | 1 |
| seized power from / murdered (lord botley) | `KILLS` | 1 |
| brother worried about | `SIBLING_OF` | 1 |
| widow of (mourning/longing) | `SPOUSE_OF` | 1 |
| obeys (grudgingly) | `SERVES` | 1 |
| drinking companion/rival of | `COMPANION_OF` | 1 |
| recalls with love (deceased) | `LOVES` | 1 |
| grief/loss for | `MOURNS` | 1 |
| recalls / mourns | `MOURNS` | 1 |
| admires / curious about | `RESPECTS` | 1 |
| playful affection toward | `LOVES` | 1 |
| fond of / trusts | `LOVES` | 1 |
| proposes alliance/marriage to | `ALLIES_WITH` | 1 |
| parental love for | `LOVES` | 1 |
| friendship toward | `COMPANION_OF` | 1 |
| trusted counselor | `ADVISES` | 1 |
| bitter rival / antagonist | `RESENTS` | 1 |
| brother (calls him traitor) | `SIBLING_OF` | 1 |
| complex grief / resentment toward | `MOURNS` | 1 |
| resentful of (memory) | `RESENTS` | 1 |
| friend and ally of | `ALLIES_WITH` | 1 |
| fond of / concerned about | `LOVES` | 1 |
| respected by / cooperates with | `RESPECTS` | 1 |
| uncle (great half-uncle) of | `UNCLE_OF` | 1 |
| affection toward | `LOVES` | 1 |
| married to / terrorized by (in-law) | `IN_LAW_OF` | 1 |
| devotion to / mourning | `MOURNS` | 1 |
| incestuous love for | `LOVES` | 1 |
| affection/kinship toward | `LOVES` | 1 |
| cousin, indifferent | `COUSIN_OF` | 1 |
| incestuous lover, obsessive bond | `LOVER_OF` | 1 |
| captor/protector, dutiful | `CAPTURES` | 1 |
| subordinate commander | `COMMANDS` | 1 |
| resentful memory of | `RESENTS` | 1 |
| growing trust/respect toward | `RESPECTS` | 1 |
| wary respect for | `RESPECTS` | 1 |
| bitter toward (memory) | `RESENTS` | 1 |
| brother, protective | `SIBLING_OF` | 1 |
| husband / lover of | `LOVER_OF` | 1 |
| allied leader under | `ALLIES_WITH` | 1 |
| outrider/subordinate of | `SERVES` | 1 |
| subordinate of (loose) | `SERVES` | 1 |
| conflicted admiration | `RESPECTS` | 1 |
| growing affection / sexual tension | `LOVES` | 1 |
| commander / suspicious | `COMMANDS` | 1 |
| feels kinship with, wonders if still his sister | `SIBLING_OF` | 1 |
| respects, feels guilt toward | `RESPECTS` | 1 |
| fear / awe toward | `FEARS` | 1 |
| lover / deeply conflicted bond | `LOVER_OF` | 1 |
| subordinate under duress | `SERVES` | 1 |
| conflicted former lover of | `LOVER_OF` | 1 |
| acting lord commander over | `COMMANDS` | 1 |
| de facto commands | `COMMANDS` | 1 |
| former lover / deep attachment | `LOVER_OF` | 1 |
| commanding / mentoring | `TUTORS` | 1 |
| respect for authority | `RESPECTS` | 1 |
| respect / memory | `RESPECTS` | 1 |
| dying love | `LOVES` | 1 |
| mentors/supports | `TUTORS` | 1 |
| grateful/affectionate to | `LOVES` | 1 |
| recognizes/respects | `RESPECTS` | 1 |
| summoned by / obeys | `SERVES` | 1 |
| valued / mourns | `MOURNS` | 1 |
| bonds with (warg) | `WARGS_INTO` | 1 |
| respected by | `RESPECTS` | 1 |
| warned/respected by | `RESPECTS` | 1 |
| bitter enemy / blames | `RESENTS` | 1 |
| subordinate conspirator to | `SERVES` | 1 |
| conspirator with, friction | `CONSPIRES_WITH` | 1 |
| subordinate/respect | `RESPECTS` | 1 |
| friendship/comfort | `COMPANION_OF` | 1 |
| protector/companion of | `COMPANION_OF` | 1 |
| sworn brotherhood/close friendship | `COMPANION_OF` | 1 |
| mentorship/honesty | `TUTORS` | 1 |
| political alliance/endorsement | `ALLIES_WITH` | 1 |
| protective mockery/friendship | `COMPANION_OF` | 1 |
| trust/admiration | `RESPECTS` | 1 |
| mentors/manipulates | `TUTORS` | 1 |
| loved but exasperated by (late husband) | `LOVES` | 1 |
| grief/anger about | `MOURNS` | 1 |
| treats as sister | `SIBLING_OF` | 1 |
| warns about joffrey | `ADVISES` | 1 |
| dismisses sansa's warning about | `ADVISES` | 1 |
| warns sansa about | `ADVISES` | 1 |
| desired by (hoped-for betrothal lost) | `BETROTHED_TO` | 1 |
| obeys reluctantly | `SERVES` | 1 |
| previously warned | `ADVISES` | 1 |
| innocent affection toward | `LOVES` | 1 |
| loyal subordinate | `SERVES` | 1 |
| former lover / obsession | `LOVER_OF` | 1 |
| claims paternal affection for | `LOVES` | 1 |
| frames for murder | `KILLS` | 1 |
| bitter rivalry with | `RESENTS` | 1 |
| nostalgic grief for | `MOURNS` | 1 |
| refuses to obey | `SERVES` | 1 |
| strategic alliance with | `ALLIES_WITH` | 1 |
| thinks of brother re: cersei's marriage | `SIBLING_OF` | 1 |
| recalls with fear | `FEARS` | 1 |
| secret lover | `LOVER_OF` | 1 |
| orders murder of | `KILLS` | 1 |
| liked/respected | `RESPECTS` | 1 |
| grief-stricken over | `MOURNS` | 1 |
| brother (substitute) | `SIBLING_OF` | 1 |
| paramour/lover | `LOVER_OF` | 1 |
| favorite nephew | `NEPHEW_OF` | 1 |
| subordinate/resentful toward | `RESENTS` | 1 |
| wary alliance with | `ALLIES_WITH` | 1 |
| admires sansa's social skill | `RESPECTS` | 1 |
| dependence on / alliance with | `ALLIES_WITH` | 1 |
| political alliance proposed with | `ALLIES_WITH` | 1 |
| confessed rapist/murderer of | `KILLS` | 1 |
| lover of / paramour to | `LOVER_OF` | 1 |
| planned betrothal with | `BETROTHED_TO` | 1 |
| refused betrothal / insulted | `BETROTHED_TO` | 1 |
| commanded lie about tysha | `COMMANDS` | 1 |
| attempted murder of | `KILLS` | 1 |
| caretaker/companion of | `COMPANION_OF` | 1 |
| ally/supporter of | `ALLIES_WITH` | 1 |
| allied against | `ALLIES_WITH` | 1 |
| predicts murder of | `KILLS` | 1 |
| developing friendship with | `COMPANION_OF` | 1 |
| nostalgic love for absent | `LOVES` | 1 |
| friendly acquaintance of | `COMPANION_OF` | 1 |
| misses / only living brother | `SIBLING_OF` | 1 |
| memory/respect toward | `RESPECTS` | 1 |
| respectful of (grudging) | `RESPECTS` | 1 |
| devotion / idealized love | `LOVES` | 1 |
| broke betrothal with | `BETROTHED_TO` | 1 |
| harsh mentor | `TUTORS` | 1 |
| military command | `COMMANDS` | 1 |
| protective mentor / reluctant companion | `COMPANION_OF` | 1 |
| fear and resentment | `FEARS` | 1 |
| subordination (rebukes) | `SERVES` | 1 |
| yearns for/respects | `RESPECTS` | 1 |
| guide/companion to | `COMPANION_OF` | 1 |
| reluctant traveling companion | `COMPANION_OF` | 1 |
| counselor / protective toward | `ADVISES` | 1 |
| deep grief/devotion to memory of | `MOURNS` | 1 |
| mentored by (memory) | `TUTORS` | 1 |
| was betrothed to (past) | `BETROTHED_TO` | 1 |
| wary mutual respect | `RESPECTS` | 1 |
| grief / nightmare | `MOURNS` | 1 |
| companion (abandoned) | `COMPANION_OF` | 1 |
| twin sister / political tension | `SIBLING_OF` | 1 |
| mistrust / suspicion | `DISTRUSTS` | 1 |
| brother / strained | `SIBLING_OF` | 1 |
| uncle / mediator | `UNCLE_OF` | 1 |
| twin sister of / estranged from | `SIBLING_OF` | 1 |
| former lover of / worries about | `LOVER_OF` | 1 |
| mother, protector (possessive, fearful) | `FEARS` | 1 |
| bitter estrangement from | `RESENTS` | 1 |
| performs affection toward | `LOVES` | 1 |
| obedient and affectionate toward | `LOVES` | 1 |
| past lover of | `LOVER_OF` | 1 |
| uses/commands | `COMMANDS` | 1 |
| enjoys friendship with | `COMPANION_OF` | 1 |
| aunt, confidante (memory) | `UNCLE_OF` | 1 |
| grief and guilt over | `MOURNS` | 1 |
| emulates / admires | `RESPECTS` | 1 |
| fear and memory of | `FEARS` | 1 |
| intimate companion | `COMPANION_OF` | 1 |
| ordered murder of | `KILLS` | 1 |
| stands vigil for / feels no grief toward | `MOURNS` | 1 |
| devoted to / mourns | `MOURNS` | 1 |
| admiration for potential of | `RESPECTS` | 1 |
| recalled mentorship by | `TUTORS` | 1 |
| kept close out of fear of tywin | `FEARS` | 1 |
| former lover of (rejected by) | `LOVER_OF` | 1 |
| warns cersei about | `ADVISES` | 1 |
| former betrothed / despises | `BETROTHED_TO` | 1 |
| cousin / blood relative | `COUSIN_OF` | 1 |
| nephew (via brother kevan) | `NEPHEW_OF` | 1 |
| uncle-nephew (kevan is uncle) | `NEPHEW_OF` | 1 |
| memory/affection for | `LOVES` | 1 |
| cousin, easy camaraderie | `COUSIN_OF` | 1 |
| nephew | `NEPHEW_OF` | 1 |
| loved but complex | `LOVES` | 1 |
| reluctant admiration | `RESPECTS` | 1 |
| parleying adversary / grudging respect | `RESPECTS` | 1 |
| cousin, military collaborator | `COUSIN_OF` | 1 |
| commander over | `COMMANDS` | 1 |
| uncle-nephew by marriage, authority over | `NEPHEW_OF` | 1 |
| nephew, respect for | `NEPHEW_OF` | 1 |
| commander, contempt for | `COMMANDS` | 1 |
| captor threatening | `CAPTURES` | 1 |
| uncle, protective of | `UNCLE_OF` | 1 |
| husband, affection for | `LOVES` | 1 |
| uncle/nephew loyalty | `NEPHEW_OF` | 1 |
| aunt/nephew respect | `NEPHEW_OF` | 1 |
| loved/mourns | `MOURNS` | 1 |
| controlled disdain toward | `HATES` | 1 |
| uneasy alliance with | `ALLIES_WITH` | 1 |
| comforted/loved | `LOVES` | 1 |
| helps / warns | `ADVISES` | 1 |
| working taskmaster / comic ally | `ALLIES_WITH` | 1 |
| brother, nostalgic love | `SIBLING_OF` | 1 |
| niece, affection | `UNCLE_OF` | 1 |
| affection (recalled) | `LOVES` | 1 |
| trust/affection toward | `LOVES` | 1 |
| maternal love for | `LOVES` | 1 |
| friendly/teasing toward | `COMPANION_OF` | 1 |
| friendly respect toward | `RESPECTS` | 1 |
| fear/complicated resentment of | `FEARS` | 1 |
| grief/reverence for | `MOURNS` | 1 |
| interest/respect toward | `RESPECTS` | 1 |
| friendly helpfulness toward | `COMPANION_OF` | 1 |
| childhood fear of | `FEARS` | 1 |
| commanding/protective toward | `COMMANDS` | 1 |
| advisor/ally of | `ALLIES_WITH` | 1 |
| brother (younger) | `SIBLING_OF` | 1 |
| brother | `SIBLING_OF` | 1 |
| obeys commands of | `COMMANDS` | 1 |
| niece; deep affection and respect | `UNCLE_OF` | 1 |
| daughter; grief and avoidance | `MOURNS` | 1 |
| daughter; complicated grief | `MOURNS` | 1 |
| sister; conflicted | `SIBLING_OF` | 1 |
| captain commanding crew | `COMMANDS` | 1 |
| captor, shows care | `CAPTURES` | 1 |
| former youthful lover; no current interest | `LOVER_OF` | 1 |
| brother; burdened guardian | `SIBLING_OF` | 1 |
| brother; weary tolerance | `SIBLING_OF` | 1 |
| guardian / political counsel | `ADVISES` | 1 |
| feudal lord; commands loyalty | `COMMANDS` | 1 |
| devoted / unrequited love | `LOVES` | 1 |
| son; grieving | `MOURNS` | 1 |
| murdered (alleged) | `KILLS` | 1 |
| mother; mourning | `MOURNS` | 1 |
| sister; claims inheritance | `SIBLING_OF` | 1 |
| lover of (deceased) | `LOVER_OF` | 1 |
| close cousin/like a sister to | `COUSIN_OF` | 1 |
| secretly betrothed arianne to | `BETROTHED_TO` | 1 |
| eldest brother of | `SIBLING_OF` | 1 |
| elder brother of | `SIBLING_OF` | 1 |
| has no love for | `LOVES` | 1 |
| leader of conspiracy | `CONSPIRES_WITH` | 1 |
| cousin / ally | `COUSIN_OF` | 1 |
| cousin / close friend | `COUSIN_OF` | 1 |
| uncle / formative influence | `UNCLE_OF` | 1 |
| cyvasse opponent / betrothed | `BETROTHED_TO` | 1 |
| brother, rival, resentful subordinate | `SIBLING_OF` | 1 |
| brother, loyal memory | `SIBLING_OF` | 1 |
| brother, sympathetic but frustrated | `SIBLING_OF` | 1 |
| half-sister, paternalistic concern | `SIBLING_OF` | 1 |
| respected enemy | `RESPECTS` | 1 |
| ambitious subordinate | `SERVES` | 1 |
| cautious ally | `ALLIES_WITH` | 1 |
| paternal affection for | `LOVES` | 1 |
| imprisoned | `IMPRISONS` | 1 |
| conflicted admiration for | `RESPECTS` | 1 |
| warging/controlling | `WARGS_INTO` | 1 |
| love/affection for | `LOVES` | 1 |
| warging into (ethically fraught) | `WARGS_INTO` | 1 |
| emotional dependence on / affection for | `LOVES` | 1 |
| longing for / missing | `MOURNS` | 1 |
| twin sister of | `SIBLING_OF` | 1 |
| lover / desires rescue from | `LOVER_OF` | 1 |
| protective uncle / disapproving of | `UNCLE_OF` | 1 |
| is bonded to | `BONDED_TO` | 1 |
| misses/desires | `MOURNS` | 1 |
| loss/grief over | `MOURNS` | 1 |
| fearful servitor | `FEARS` | 1 |
| fierce ally | `ALLIES_WITH` | 1 |
| queen/captor of hostages (but fond) | `CAPTURES` | 1 |
| blood relative (cousin) | `COUSIN_OF` | 1 |
| was "fond" of (not love) | `LOVES` | 1 |
| desires / misses | `MOURNS` | 1 |
| misses / conflicted about | `MOURNS` | 1 |
| resistant to counsel from | `ADVISES` | 1 |
| remembers with love | `LOVES` | 1 |
| companion/protector of | `COMPANION_OF` | 1 |
| considers alliance with | `ALLIES_WITH` | 1 |
| rider/bonded to | `BONDED_TO` | 1 |
| longs for / lover | `MOURNS` | 1 |
| complex grief | `MOURNS` | 1 |
| counselor/admirer | `RESPECTS` | 1 |
| allied fleet commander of | `COMMANDS` | 1 |
| seeking alliance with | `ALLIES_WITH` | 1 |
| cousin and garrison commander to | `COUSIN_OF` | 1 |
| fearful/protective regarding | `FEARS` | 1 |
| grieving father of | `MOURNS` | 1 |
| grandfather of | `PARENT_OF` | 1 |
| forced marriage to / murdered | `KILLS` | 1 |
| political tension/alliance with | `ALLIES_WITH` | 1 |
| grieving father | `MOURNS` | 1 |
| bond with / wargs into | `WARGS_INTO` | 1 |
| attempts to cultivate / warns | `ADVISES` | 1 |
| mentors / encourages | `TUTORS` | 1 |
| desires/admires | `RESPECTS` | 1 |
| knew briefly / respected | `RESPECTS` | 1 |
| remembers / respects | `RESPECTS` | 1 |
| commander sending on dangerous mission | `COMMANDS` | 1 |
| acknowledges as brother despite dislike | `SIBLING_OF` | 1 |
| mentor/trainer to | `TUTORS` | 1 |
| bonded companion to | `COMPANION_OF` | 1 |
| protective love for | `LOVES` | 1 |
| guilt toward / mourning for | `MOURNS` | 1 |
| loyal/humorous companion to | `COMPANION_OF` | 1 |
| grudgingly admires but distrusts | `RESPECTS` | 1 |
| fear | `FEARS` | 1 |
| admired as a boy | `RESPECTS` | 1 |
| values as ally | `ALLIES_WITH` | 1 |
| offers alliance to (via val) | `ALLIES_WITH` | 1 |
| formerly betrothed to | `BETROTHED_TO` | 1 |
| disdainful toward | `HATES` | 1 |
| adversarial / captor | `CAPTURES` | 1 |
| politically allied with | `ALLIES_WITH` | 1 |
| warns / watches over | `ADVISES` | 1 |
| negotiating partner / mutual respect | `RESPECTS` | 1 |
| commander (reluctant political subordinate) | `COMMANDS` | 1 |
| wary respect | `RESPECTS` | 1 |
| bonded | `BONDED_TO` | 1 |
| grief | `MOURNS` | 1 |
| love/pride | `LOVES` | 1 |
| father-in-law (grudging) | `IN_LAW_OF` | 1 |
| friendly/curious | `COMPANION_OF` | 1 |
| cautious alliance with | `ALLIES_WITH` | 1 |
| respect/adversarial warmth toward | `RESPECTS` | 1 |
| half in love with / fears / worships | `LOVES` | 1 |
| feels no fear for herself | `FEARS` | 1 |
| last companion of | `COMPANION_OF` | 1 |
| captor / torturer | `CAPTURES` | 1 |
| oddly fond of | `LOVES` | 1 |
| admires (grudgingly) | `RESPECTS` | 1 |
| warging ability | `WARGS_INTO` | 1 |
| love/longing | `LOVES` | 1 |
| affection (memory) | `LOVES` | 1 |
| recognition/affection | `LOVES` | 1 |
| sworn brother (former) | `SIBLING_OF` | 1 |
| respect for | `RESPECTS` | 1 |
| friendship (strained) | `COMPANION_OF` | 1 |
| friendship/reliance | `COMPANION_OF` | 1 |
| misses / regrets not visiting | `MOURNS` | 1 |
| disdains / finds inadequate | `HATES` | 1 |
| kinsman / captor of | `CAPTURES` | 1 |
| suggests alliance with | `ALLIES_WITH` | 1 |
| counsels / proposes to | `ADVISES` | 1 |
| bitter rival/brother of | `SIBLING_OF` | 1 |
| subordinate to (resentfully) | `SERVES` | 1 |
| trust/alliance with | `ALLIES_WITH` | 1 |
| uneasy co-conspirator with | `CONSPIRES_WITH` | 1 |
| mentor to | `TUTORS` | 1 |
| warns/protects | `ADVISES` | 1 |
| loved (unrequited) | `LOVES` | 1 |
| plans to imprison | `IMPRISONS` | 1 |
| chose/loved | `LOVES` | 1 |
| rival lover with | `LOVER_OF` | 1 |
| father who allowed sons' love matches | `LOVES` | 1 |
| admires/worships | `RESPECTS` | 1 |
| devoted loyalty / love | `LOVES` | 1 |
| deep friendship / grief | `MOURNS` | 1 |
| intended betrothed to | `BETROTHED_TO` | 1 |
| friend / traveling companion of | `COMPANION_OF` | 1 |
| recruited for / allied with | `ALLIES_WITH` | 1 |
| aggressive military counsel to | `ADVISES` | 1 |
| cautious alliance forming with | `ALLIES_WITH` | 1 |
| mentor/trainer of | `TUTORS` | 1 |
| bonded rider of | `BONDED_TO` | 1 |
| fond of (as are daenerys) | `LOVES` | 1 |
| subordinate to / intimidated by | `SERVES` | 1 |
| former betrothed/suitor of | `BETROTHED_TO` | 1 |
| coerced ally of | `ALLIES_WITH` | 1 |
| conflicted love for | `LOVES` | 1 |
| niece mentored by | `UNCLE_OF` | 1 |
| captain/commander of | `COMMANDS` | 1 |
| counsels/advises | `ADVISES` | 1 |
| dispatched brother to the sorrows | `SIBLING_OF` | 1 |
| squire/cousin to | `COUSIN_OF` | 1 |
| friend/ally of | `ALLIES_WITH` | 1 |
| deep friendship / partnership with | `COMPANION_OF` | 1 |
| supporter / conspirator for | `CONSPIRES_WITH` | 1 |
| grief / longing for | `MOURNS` | 1 |
| childhood affection for | `LOVES` | 1 |
| camaraderie / amusement | `COMPANION_OF` | 1 |
| reluctant superior → distrustful subordinate | `SERVES` | 1 |
| father figure / commander | `COMMANDS` | 1 |
| rough camaraderie | `COMPANION_OF` | 1 |
| grief/betrayal toward | `MOURNS` | 1 |
| feels pity for / tentative friendship forming | `COMPANION_OF` | 1 |
| superstitious affection for | `LOVES` | 1 |
| performing partner / reluctant ally | `ALLIES_WITH` | 1 |
| pity / admiration without desire | `RESPECTS` | 1 |
| supreme commander / guest of honor | `COMMANDS` | 1 |
| admires / seeks to surpass | `RESPECTS` | 1 |
| fear / shun | `FEARS` | 1 |

---

## Unmapped Tail (LLM work)

> 2,969 distinct phrases covering 3,638 rows (49.5% of total).  
> These go to Haiku for hint → edge-type classification.

| Hint Phrase (normalized) | Count | Example A → B | Chapter |
|--------------------------|-------|---------------|---------|
| remembers fondly | 17 | Arya → Needle | asos-arya-02 |
| longing for | 12 | Arya → Jon Snow | agot-arya-02 |
| attracted to | 11 | Lady Hornwood → Ser Rodrik | acok-bran-02 |
| bond with | 10 | Bran → Summer | agot-bran-04 |
| conflicted about | 10 | Arya → Jaqen H'ghar | acok-arya-07 |
| guilt toward | 9 | Ned → Sansa | agot-eddard-04 |
| remembers | 9 | Eddard Stark → Rhaegar Targaryen | agot-eddard-09 |
| Accuses | 9 | Varys → Eddard Stark | agot-sansa-04 |
| Recalls fondly | 8 | Arya Stark → Robb Stark | agot-arya-04 |
| relies on | 8 | Robb → Maester Luwin | agot-bran-04 |
| critical of | 7 | Septa Mordane → Arya | agot-arya-01 |
| resembles | 7 | Arya → Ned Stark | agot-arya-01 |
| worries about | 7 | Arya → Bran Stark | agot-arya-05 |
| Supports | 7 | Farlen → Palla | acok-bran-06 |
| champion of | 7 | Oznak zo Pahl → Meereen's Great Masters | asos-daenerys-05 |
| Pities | 7 | Sansa Stark → Margaery Tyrell | asos-sansa-05 |
| Supporter of | 7 | Rodrik the Reader → Asha Greyjoy | affc-the-drowned-man-01 |
| remembers teaching of | 6 | Arya → Syrio Forel | agot-arya-05 |
| dislikes | 6 | Robert Baratheon → Stannis Baratheon | agot-bran-02 |
| dominates | 6 | Summer → Shaggydog | agot-bran-07 |
| concern for | 6 | Catelyn → Lysa Arryn | agot-catelyn-01 |
| devoted to | 6 | Barra's mother → Robert Baratheon | agot-eddard-09 |
| Suspects | 6 | Eddard Stark → Tywin Lannister | agot-eddard-11 |
| Complex feelings toward | 6 | Tyrion → Jaime Lannister | agot-tyrion-06 |
| recalls | 6 | Arya → Jory Cassel | acok-arya-02 |
| Favors | 6 | Cersei → Lancel Lannister | acok-tyrion-04 |
| Betrayed | 6 | Roose Bolton → Robb Stark | asos-jon-11 |
| dependent on | 5 | Bran → Hodor | agot-bran-06 |
| defeated in joust | 5 | Rhaegar Targaryen → Brandon Stark | agot-eddard-15 |
| Cruel toward | 5 | Joffrey → Mycah | agot-sansa-01 |
| Dismisses | 5 | Joffrey Baratheon → Ser Barristan Selmy | agot-sansa-05 |
| served by | 5 | Ramsay Snow → Reek | acok-bran-02 |
| Cares for | 5 | Maester Vyman → Lord Hoster | acok-catelyn-05 |
| desires | 5 | Reek → Palla | acok-theon-05 |
| feels guilt toward | 5 | Arya → Gendry, Hot Pie | asos-arya-01 |
| advocates for | 5 | The wild wolf (in story) → The quiet wolf | asos-bran-02 |
| Queen served by | 5 | Daenerys → Irri | adwd-daenerys-03 |
| alienated from | 4 | Arya → Household guard (Jory, Harwin, Alyn, etc.) | agot-arya-02 |
| opposition | 4 | Ned Stark → The council | agot-arya-02 |
| Accuses of murder | 4 | Lysa Arryn → Cersei Lannister / the Lannisters | agot-catelyn-02 |
| bannerman to | 4 | Lord Jason Mallister → House Tully | agot-catelyn-05 |
| declared king by | 4 | Robb → Jon Umber (Greatjon) | agot-catelyn-11 |
| bloodrider of | 4 | Qotho → Khal Drogo | agot-daenerys-05 |
| feels abandoned by | 4 | Jon Snow → Benjen Stark | agot-jon-03 |
| Steward to | 4 | Jon Snow → Jeor Mormont | agot-jon-07 |
| Pity toward | 4 | Sansa Stark → Jon Snow | agot-sansa-03 |
| Attacked | 4 | Sandor Clegane → Jeyne Poole's quarters | agot-sansa-04 |
| Previously served | 4 | Ser Barristan Selmy → King Aerys II Targaryen | agot-sansa-05 |
| uses | 4 | Roose Bolton → Qyburn | acok-arya-10 |
| threatened by | 4 | Lady Hornwood → Ramsay Snow | acok-bran-02 |
| served | 4 | Reek → Bastard of Bolton | acok-bran-05 |
| Former ward of | 4 | Theon → Eddard Stark | acok-bran-06 |
| disrespects | 4 | Lord Randyll Tarly → Robb Stark | acok-catelyn-02 |
| Condemns | 4 | Robb → Theon Greyjoy | asos-catelyn-06 |
| haunted by memory of | 4 | Tyrion → Tysha | asos-tyrion-09 |
| Protective father of | 3 | Eddard Stark → Arya Stark | agot-arya-03 |
| knew | 3 | Yoren → Eddard Stark | agot-arya-05 |
| defers to | 3 | High Septon → Joffrey | agot-arya-05 |
| kindness toward | 3 | Tyrion → Bran | agot-bran-04 |
| Surveils | 3 | Varys → Catelyn Stark, Ser Rodrik | agot-catelyn-04 |
| Estranged from | 3 | Brynden Tully → Lord Hoster Tully | agot-catelyn-06 |
| feared by | 3 | Grey Wind → Riverrun guards | agot-catelyn-11 |
| Abuses | 3 | Viserys → Doreah | agot-daenerys-04 |
| Teacher to | 3 | Jhiqui → Daenerys | agot-daenerys-04 |
| claims descent from | 3 | Daenerys → Aegon the Conqueror | agot-daenerys-09 |
| paired with (formal) | 3 | Robb Stark → Myrcella Baratheon | agot-jon-01 |
| taunts | 3 | Toad → Jon Snow | agot-jon-03 |
| bonds with | 3 | Jon Snow → Ghost | agot-jon-03 |
| Service to | 3 | Chett → Maester Aemon | agot-jon-05 |
| Antagonism with | 3 | Jon Snow → Ser Alliser Thorne | agot-jon-07 |
| Angry at | 3 | Jon Snow → Samwell Tarly | agot-jon-08 |
| Kind toward | 3 | Ser Barristan Selmy → Sansa | agot-sansa-01 |
| Disapproves of | 3 | Septa Mordane → Jory Cassel | agot-sansa-02 |
| Protective authority over | 3 | Eddard Stark → Sansa and Arya | agot-sansa-03 |
| Infatuation with | 3 | Jeyne Poole → Beric Dondarrion | agot-sansa-03 |
| Served alongside | 3 | Ser Barristan Selmy → Ser Gerold Hightower | agot-sansa-05 |
| Enforcer for | 3 | Ser Meryn Trant → Joffrey | agot-sansa-06 |
| Assesses as dangerous | 3 | Tywin → Stannis Baratheon | agot-tyrion-09 |
| sympathetic to | 3 | Innkeeper → Night's Watch | acok-arya-02 |
| Knows true identity of | 3 | Yoren → Arya | acok-arya-03 |
| Frustrated with | 3 | Arya → Lommy | acok-arya-05 |
| grateful to | 3 | Robett Glover → Arya (as Weasel) | acok-arya-09 |
| caretaker of | 3 | Maester Luwin → Bran Stark | acok-bran-01 |
| thinks of | 3 | Bran → Jon Snow | acok-bran-02 |
| Swears fealty to | 3 | Reek → Theon / House Greyjoy | acok-bran-06 |
| Feels betrayed by | 3 | Bran → Osha | acok-bran-06 |
| political tension with | 3 | Robb Stark → Catelyn Stark | acok-catelyn-01 |
| Compared to | 3 | Renly → Robert Baratheon | acok-catelyn-03 |
| memory of | 3 | Catelyn → Lysa Arryn | acok-catelyn-07 |
| Named bloodrider | 3 | Daenerys → Rakharo | acok-daenerys-01 |
| Handmaid to | 3 | Irri → Daenerys | acok-daenerys-01 |
| Former husband of | 3 | Ser Jorah → Lynesse Hightower | acok-daenerys-01 |
| Named for / honors | 3 | Drogon → Khal Drogo | acok-daenerys-01 |
| Sworn protector (bloodrider) | 3 | Jhogo → Daenerys | acok-daenerys-04 |
| sent by | 3 | Arstan Whitebeard → Illyrio Mopatis | acok-daenerys-05 |
| Leader of | 3 | Ser Axell Florent → The queen's men | acok-davos-01 |
| Brotherhood with | 3 | Jon Snow → Ebben, Squire Dalbridge | acok-jon-06 |
| devoted follower | 3 | Selyse → Melisandre / R'hllor | acok-prologue |
| Sympathetic toward | 3 | Tyrion → Sansa | acok-sansa-01 |
| avoids | 3 | Ser Horas Redwyne → Sansa | acok-sansa-03 |
| Rivalry with | 3 | Joffrey → Robb Stark | acok-sansa-05 |
| Abandons | 3 | Cersei → Sansa | acok-sansa-07 |
| Loyal squire to | 3 | Wex → Theon | acok-theon-06 |
| Sibling rivalry with | 3 | Tyrion → Cersei | acok-tyrion-09 |
| considers trusting | 3 | Tyrion → Bronn | acok-tyrion-15 |
| kinship with | 3 | Arya → Wolves | asos-arya-01 |
| partner/comrade | 3 | Tom Sevenstrings → Lem Lemoncloak | asos-arya-02 |
| Religious devotion to | 3 | Thoros of Myr → R'hllor | asos-arya-06 |
| lost to | 3 | Lord Beric → Ser Burton Crakehall | asos-arya-07 |
| concerned for | 3 | Thoros → Lord Beric | asos-arya-08 |
| Master of | 3 | Sandor Clegane → Stranger (horse) | asos-arya-09 |
| sibling bond with | 3 | Meera Reed → Jojen Reed | asos-bran-02 |
| conflicted feelings toward | 3 | Daenerys → Ser Jorah Mormont | asos-daenerys-02 |
| captained | 3 | Dale Seaworth → Wraith | asos-davos-01 |
| manipulated | 3 | Cersei (memory) → Jaime (memory) | asos-jaime-02 |
| Appointed | 3 | Tywin Lannister → Roose Bolton | asos-jon-11 |
| opposed by | 3 | Jon Snow → Janos Slynt | asos-jon-12 |
| Romantic/sexual exploitation | 3 | Dareon → Lanna | affc-cat-of-the-canals-01 |
| Suspicion | 3 | Cersei → Stannis Baratheon | affc-cersei-01 |
| Exiled by | 3 | Euron → Balon | affc-the-iron-captain-01 |
| Punished | 3 | Balon Greyjoy → Quellon's third wife (Piper) | affc-the-prophet-01 |
| Lord of | 3 | Gorold Goodbrother → Hammerhorn | affc-the-prophet-01 |
| gaoler to | 3 | Septa Unella → Cersei | adwd-cersei-01 |
| Considers betrayer | 3 | Cersei → Lancel | adwd-cersei-02 |
| is served by | 3 | Daenerys → Irri | adwd-daenerys-01 |
| Knew / recalled | 3 | Reek → Arya Stark | adwd-reek-01 |
| Property of | 3 | Tyrion → Yezzan zo Qaggaz | adwd-tyrion-10 |
| Financial debtor to | 3 | Tyrion → Brown Ben Plumm | adwd-tyrion-12 |
| comparison/memory | 2 | Ned Stark → Lyanna Stark | agot-arya-02 |
| Reports to | 2 | Yoren → Eddard Stark | agot-arya-03 |
| Asks about | 2 | Arya Stark → Desmond | agot-arya-03 |
| Former service to | 2 | Syrio Forel → The Sealord of Braavos | agot-arya-04 |
| overrules | 2 | Joffrey → Cersei Lannister | agot-arya-05 |
| mocked | 2 | Sansa and Jeyne Poole → Ser Horas and Ser Hobber Redwyne | agot-arya-05 |
| attempts to intervene | 2 | Varys → Joffrey | agot-arya-05 |
| Contrasts with | 2 | Jon Snow → Robb Stark | agot-bran-01 |
| frustration with | 2 | Bran → Old Nan | agot-bran-04 |
| dependence on | 2 | Bran → Hodor | agot-bran-04 |
| connection to | 2 | Tyrion → Jon Snow | agot-bran-04 |
| delivers news to | 2 | Yoren → Robb, Bran | agot-bran-04 |
| Aggressive protector | 2 | Summer → Hali | agot-bran-05 |
| Deep resentment toward | 2 | Catelyn Stark → Jon Snow | agot-catelyn-02 |
| Lives in the shadow of | 2 | Eddard Stark → Brandon Stark | agot-catelyn-02 |
| Caretaker | 2 | Old Nan → Catelyn | agot-catelyn-03 |
| Informed | 2 | Varys → Petyr Baelish | agot-catelyn-04 |
| rivals with | 2 | House Blackwood → House Bracken | agot-catelyn-05 |
| Old friend of | 2 | Howland Reed → Ned Stark | agot-catelyn-08 |
| emulates | 2 | Robb → Ned Stark | agot-catelyn-09 |
| Sworn protector of | 2 | Hallis Mollen → Catelyn | agot-catelyn-10 |
| childhood acquaintance of | 2 | Catelyn → Petyr Baelish | agot-catelyn-11 |
| Has had sexual relations with | 2 | Illyrio → Doreah | agot-daenerys-02 |
| Physically abuses | 2 | Viserys → Daenerys | agot-daenerys-03 |
| proud of | 2 | Khal Drogo → Daenerys | agot-daenerys-05 |
| conflicted loyalty toward | 2 | Daenerys → Viserys Targaryen | agot-daenerys-05 |
| visiting peer of | 2 | Khal Jommo → Khal Drogo | agot-daenerys-05 |
| Maternal bond | 2 | Daenerys → Rhaego (unborn) | agot-daenerys-06 |
| slaps | 2 | Dany → Eroeh | agot-daenerys-08 |
| romantic attachment to | 2 | Ser Jorah → Dany | agot-daenerys-08 |
| violent toward | 2 | Haggo → Mirri Maz Duur | agot-daenerys-08 |
| antagonist of | 2 | Daenerys → Mirri Maz Duur | agot-daenerys-09 |
| Reluctant loyalty to | 2 | Jhogo → Daenerys | agot-daenerys-10 |
| Longing / duty-bound separation | 2 | Ned → Catelyn Stark | agot-eddard-02 |
| Kingsguard to | 2 | Ser Boros Blount → Robert | agot-eddard-02 |
| Father, protector | 2 | Eddard Stark → Arya Stark | agot-eddard-03 |
| Protective mother | 2 | Cersei Lannister → Joffrey Baratheon | agot-eddard-03 |
| remembers with complicated feeling | 2 | Ned → Robert | agot-eddard-04 |
| Overprotective of | 2 | Lysa Arryn → Robert Arryn | agot-eddard-05 |
| yearns for | 2 | Ned → Catelyn Stark | agot-eddard-06 |
| made armor for | 2 | Tobho Mott → Renly Baratheon | agot-eddard-06 |
| infatuated with | 2 | Sansa Stark → Ser Loras Tyrell | agot-eddard-07 |
| Depends on | 2 | Ned → Vayon Poole | agot-eddard-08 |
| guard to | 2 | Heward → Eddard Stark | agot-eddard-09 |
| Shows mercy to | 2 | Eddard Stark → Cersei Lannister | agot-eddard-12 |
| Longing for family | 2 | Ned → Catelyn, Bran, Robb, Rickon | agot-eddard-13 |
| Protective father | 2 | Eddard Stark → Sansa Stark | agot-eddard-14 |
| claims to serve | 2 | Varys → The realm | agot-eddard-15 |
| cold toward | 2 | Cersei Lannister → Eddard Stark | agot-jon-01 |
| resented by father | 2 | Tyrion Lannister → Tywin Lannister | agot-jon-01 |
| Assigned to serve | 2 | Jon Snow → Lord Commander Mormont | agot-jon-06 |
| Worries for | 2 | Jon Snow → Sansa/Arya (his sisters) | agot-jon-08 |
| Bond with direwolf | 2 | Jon Snow → Ghost | agot-jon-09 |
| Kill | 2 | The Others → Ser Waymar Royce | agot-prologue |
| Idolizes | 2 | Sansa → Joffrey | agot-sansa-01 |
| Hostile/contemptuous toward | 2 | Robert → Cersei | agot-sansa-02 |
| Defiance toward | 2 | Arya Stark → Sansa Stark | agot-sansa-03 |
| Takes custody of | 2 | Petyr Baelish → Jeyne Poole | agot-sansa-04 |
| Pleads on behalf of | 2 | Sansa Stark → Eddard Stark | agot-sansa-05 |
| Shows sympathy toward | 2 | Varys → Ser Barristan Selmy | agot-sansa-05 |
| Indifferent toward | 2 | Ser Meryn Trant → Sansa | agot-sansa-06 |
| Master-servant | 2 | Tyrion → Morrec | agot-tyrion-02 |
| Employer of | 2 | Tyrion → Bronn | agot-tyrion-07 |
| Sardonic toward | 2 | Tyrion → Tywin | agot-tyrion-07 |
| Complicated feelings toward | 2 | Arya → Sansa | acok-arya-01 |
| courteous toward | 2 | Jaqen H'ghar → Arya | acok-arya-02 |
| Scout for | 2 | Koss → Yoren | acok-arya-03 |
| combat partnership | 2 | Arya → Gendry | acok-arya-04 |
| remembers with longing | 2 | Arya → Her brothers (Jon especially) | acok-arya-04 |
| assists | 2 | Chiswyck → The Tickler | acok-arya-06 |
| recalls praying with | 2 | Arya → Her mother | acok-arya-06 |
| loyal follower of | 2 | Chiswyck → Ser Gregor | acok-arya-07 |
| orders death of | 2 | Arya → Chiswyck | acok-arya-07 |
| hostile rivalry with | 2 | Ser Amory Lorch → Vargo Hoat | acok-arya-09 |
| remembers/channels | 2 | Arya → Syrio Forel | acok-arya-10 |
| befriends | 2 | Rickon Stark → The Walders | acok-bran-01 |
| aggressive toward | 2 | Shaggydog → Little Walder Frey | acok-bran-01 |
| callous toward | 2 | Little Walder Frey → Ser Stevron Frey | acok-bran-05 |
| agrees with | 2 | Bran → Big Walder | acok-bran-05 |
| Claims allegiance to | 2 | Theon → Balon Greyjoy | acok-bran-06 |
| commits to accompany | 2 | Jojen → Bran | acok-bran-07 |
| king over | 2 | Robb Stark → Greatjon Umber | acok-catelyn-01 |
| defeated | 2 | Brienne → Ser Loras | acok-catelyn-02 |
| Compassion for | 2 | Catelyn → Brienne | acok-catelyn-03 |
| Sworn service | 2 | Ser Robar Royce → Renly | acok-catelyn-03 |
| Devoted to (deceased) | 2 | Brienne → Renly | acok-catelyn-05 |
| desires vengeance against | 2 | Catelyn → Theon Greyjoy | acok-catelyn-07 |
| Former ko of | 2 | Khal Pono → Khal Drogo | acok-daenerys-01 |
| Competes for Dany's favor with | 2 | Pyat Pree → Xaro Xhoan Daxos | acok-daenerys-02 |
| empathizes with | 2 | Daenerys → Viserys | acok-daenerys-03 |
| descends from | 2 | Daenerys → Rhaegar Targaryen | acok-daenerys-05 |
| Attempted to kill | 2 | Maester Cressen → Melisandre | acok-davos-01 |
| Former sworn protector of | 2 | Bryce Caron → Renly | acok-davos-02 |
| Pride in | 2 | Davos → His sons | acok-davos-03 |
| Rejects | 2 | Davos → R'hllor / Lord of Light | acok-davos-03 |
| Antagonism toward | 2 | Thoren Smallwood → Jon Snow and Sam | acok-jon-01 |
| Challenges authority of | 2 | Thoren Smallwood → Lord Commander Mormont | acok-jon-01 |
| Seeking | 2 | Jon Snow → Benjen Stark | acok-jon-03 |
| Friend to | 2 | Jon Snow → Samwell Tarly | acok-jon-05 |
| Claims kinship with | 2 | Ygritte → Starks / Jon Snow | acok-jon-06 |
| Sacrifices self for | 2 | Squire Dalbridge → The ranging party | acok-jon-07 |
| Attacked by | 2 | Ghost → Eagle (skinchanger-controlled) | acok-jon-07 |
| Feels loss/separation from | 2 | Jon Snow → Bran, Rickon, Robb | acok-jon-08 |
| loyalty | 2 | Davos → Stannis | acok-prologue |
| political refusal | 2 | Stannis → Robb Stark | acok-prologue |
| Uneasy around | 2 | Sansa → Ser Mandon (Moore) | acok-sansa-01 |
| indebted to | 2 | Ser Dontos Hollard → Sansa Stark | acok-sansa-02 |
| Envoy of | 2 | Theon Greyjoy → Robb Stark | acok-theon-01 |
| Remembered negatively | 2 | Theon Greyjoy → Rodrik Greyjoy | acok-theon-01 |
| awaits/fears judgment of | 2 | Theon → Asha Greyjoy | acok-theon-04 |
| served/took orders from | 2 | Janos Slynt → Cersei | acok-tyrion-02 |
| Sycophantic toward | 2 | Pycelle → Cersei | acok-tyrion-03 |
| Politically opposes | 2 | Stannis → Joffrey / Cersei / Lannisters | acok-tyrion-03 |
| Married to (unhappily) | 2 | Stannis → Selyse Florent | acok-tyrion-03 |
| Former connection to | 2 | Littlefinger → Catelyn Stark | acok-tyrion-04 |
| obedient to | 2 | Vylarr → Tyrion | acok-tyrion-06 |
| patron of | 2 | Cersei → Pycelle | acok-tyrion-07 |
| Protective mother of | 2 | Cersei → Joffrey | acok-tyrion-08 |
| Verbal sparring, rivalry | 2 | Varys → Littlefinger | acok-tyrion-08 |
| Cruelty toward | 2 | Joffrey → Sansa Stark | acok-tyrion-08 |
| Abusive toward | 2 | Joffrey → Sansa Stark | acok-tyrion-09 |
| Comforts | 2 | Myrcella → Tommen | acok-tyrion-09 |
| approves of | 2 | Tyrion → Ser Balon Swann | acok-tyrion-11 |
| relies on for intelligence | 2 | Tyrion → Varys | acok-tyrion-11 |
| Supports authority of | 2 | Ser Mandon Moore → Tyrion | acok-tyrion-13 |
| Distressed about | 2 | Joffrey → His ships | acok-tyrion-13 |
| Compares himself to | 2 | Tyrion → Aegon the Conqueror | acok-tyrion-13 |
| rivalry / resentment toward | 2 | Tyrion → Jaime | acok-tyrion-15 |
| former student of | 2 | Arya → Syrio Forel | asos-arya-01 |
| prays to | 2 | Arya → Old gods / tree gods | asos-arya-02 |
| Vengeful toward | 2 | Mad Huntsman → Lannisters/westermen | asos-arya-05 |
| Former sworn shield of | 2 | Sandor Clegane → Joffrey Baratheon | asos-arya-06 |
| Confesses killing | 2 | Sandor Clegane → Mycah | asos-arya-06 |
| wants dead | 2 | Arya → Sandor Clegane, Gregor Clegane, Dunsen, Polliver, Raff, the Tickler, Ser Ilyn, Ser Meryn, Joffrey, Cersei | asos-arya-07 |
| attached to | 2 | Ghost of High Heart → "Jenny's song" | asos-arya-08 |
| connected to | 2 | Edric Dayne → Jon Snow | asos-arya-08 |
| predatory toward | 2 | Sandor Clegane → Arya | asos-arya-08 |
| Hopes for rescue from | 2 | Arya Stark → Lord Beric Dondarrion / Brotherhood | asos-arya-09 |
| desperately seeks reunion with | 2 | Arya Stark → Robb Stark | asos-arya-10 |
| Dominant over | 2 | Summer → Wild wolf pack | asos-bran-01 |
| follows guidance of | 2 | Bran Stark → Jojen Reed | asos-bran-02 |
| wants to reunite with | 2 | Bran → Jon Snow | asos-bran-03 |
| guides | 2 | Jojen Reed → Bran | asos-bran-04 |
| married (past) | 2 | Jorah Mormont → Lynesse Hightower | asos-catelyn-05 |
| plans to use | 2 | Robb Stark → Howland Reed | asos-catelyn-05 |
| valued | 2 | Eddard Stark → Howland Reed | asos-catelyn-05 |
| Controlling toward | 2 | Lord Walder Frey → His family | asos-catelyn-06 |
| Reports to / serves | 2 | Roose Bolton → Robb | asos-catelyn-06 |
| Mother figure to | 2 | Daenerys → Drogon, Rhaegal, Viserion | asos-daenerys-01 |
| Knighted and close to | 2 | Rhaegar Targaryen → Myles Mooton | asos-daenerys-01 |
| romantic interest in | 2 | Ser Jorah Mormont → Daenerys | asos-daenerys-02 |
| maternal bond with | 2 | Daenerys → Drogon, Viserion | asos-daenerys-02 |
| serve | 2 | Irri, Jhiqui → Daenerys | asos-daenerys-04 |
| knighted | 2 | Stannis Baratheon → Davos | asos-davos-01 |
| Tends | 2 | Porridge (gaoler) → Davos | asos-davos-03 |
| Burned | 2 | Melisandre → Guncer Sunglass | asos-davos-03 |
| Conflicted toward | 2 | Stannis → Edric Storm | asos-davos-05 |
| Ambivalent toward | 2 | Stannis → R'hllor worship | asos-davos-06 |
| Replaced | 2 | Maester Pylos → Maester Cressen | asos-davos-06 |
| family bond | 2 | Jaime → Cersei | asos-jaime-04 |
| compares | 2 | Jaime → Gregor Clegane / bear | asos-jaime-06 |
| Coordinated with | 2 | Tywin → Roose Bolton | asos-jaime-07 |
| political control over | 2 | Lord Tywin → Tommen | asos-jaime-09 |
| Informant for | 2 | Craster → Night's Watch | asos-jon-01 |
| Hostile | 2 | Rattleshirt → Jon Snow | asos-jon-02 |
| reported killer of | 2 | Theon Greyjoy → Bran Stark | asos-jon-06 |
| Chose | 2 | Qhorin Halfhand → Jon Snow | asos-jon-08 |
| Dismissed by | 2 | Donal Noye → Slynt | asos-jon-09 |
| Compares self unfavorably to | 2 | Jon Snow → Robb Stark | asos-jon-10 |
| resent | 2 | Brothers (multiple) → Craster | asos-samwell-02 |
| self-loathing | 2 | Sam → Himself | asos-samwell-02 |
| Enmity | 2 | Craster → Mance Rayder | asos-samwell-04 |
| Uncomfortable with | 2 | Stannis → Melisandre | asos-samwell-05 |
| Humiliates | 2 | Joffrey Baratheon → Tyrion Lannister | asos-sansa-03 |
| Paramour of | 2 | Prince Oberyn → Ellaria Sand | asos-sansa-04 |
| Suspects / accuses | 2 | Cersei Lannister → Tyrion Lannister | asos-sansa-05 |
| Marries | 2 | Petyr Baelish → Lysa Arryn | asos-sansa-06 |
| Assesses contemptuously | 2 | Petyr Baelish → Cersei Lannister | asos-sansa-06 |
| Obsessively devoted to | 2 | Lysa Arryn → Petyr Baelish | asos-sansa-06 |
| Grateful toward | 2 | Kingslanders → House Tyrell | asos-tyrion-01 |
| dominates/controls | 2 | Tywin Lannister → Tyrion Lannister | asos-tyrion-03 |
| pressures | 2 | Tywin → Tyrion | asos-tyrion-04 |
| Domineering control over | 2 | Tywin → Joffrey | asos-tyrion-06 |
| Threatened | 2 | Cersei → Robert Baratheon | asos-tyrion-06 |
| Considers marrying Shae to | 2 | Tyrion → Bronn | asos-tyrion-07 |
| Desecrated the corpse of | 2 | The Freys → Robb Stark | asos-tyrion-07 |
| abandoned by | 2 | Tyrion → Bronn | asos-tyrion-09 |
| Brutalized | 2 | Tywin → Tysha | asos-tyrion-11 |
| Political manipulation of | 2 | Petyr Baelish → Lady Waynwood | affc-alayne-02 |
| believes dead | 2 | Arya → Bran Stark | affc-arya-01 |
| tested by | 2 | Arya → The kindly man | affc-arya-01 |
| Trained | 2 | Ser Goodwin → Brienne | affc-brienne-02 |
| Suspicion of | 2 | Brienne → Ser Shadrich | affc-brienne-02 |
| defeated in mêlée | 2 | Brienne → Ronnet Connington | affc-brienne-04 |
| Quest loyalty to | 2 | Brienne → Sansa Stark | affc-brienne-05 |
| Old friend / regular visitor | 2 | Septon Meribald → Elder Brother | affc-brienne-06 |
| Vow sworn to | 2 | Brienne → Jaime (Lannister) | affc-brienne-06 |
| Hunting outlaws from | 2 | Randyll Tarly → Maidenpool | affc-brienne-06 |
| Performs marriages | 2 | Ezzelyno → Happy Port whores and customers | affc-cat-of-the-canals-01 |
| Romantically interested in | 2 | Megga Tyrell → Mark Mullendore | affc-cersei-06 |
| Flatters | 2 | Orton Merryweather → Cersei | affc-cersei-07 |
| Evaluates/uses | 2 | Cersei → Osmund Kettleblack | affc-cersei-08 |
| compares to Robert | 2 | Cersei → Osney Kettleblack | affc-cersei-09 |
| claimed to have killed | 2 | Tyrion → Joffrey | affc-jaime-01 |
| Formerly married to | 2 | Lady Mariya → Merrett Frey | affc-jaime-04 |
| fondness for | 2 | Jaime → Gerion Lannister | affc-jaime-07 |
| suspects/accuses | 2 | Edwyn Frey → Black Walder | affc-jaime-07 |
| Failed by / submitted to | 2 | Pate → Archmaester Vaellyn | affc-prologue |
| nurses | 2 | Gilly → Dalla's son | affc-samwell-02 |
| bullied | 2 | Horas Redwyne → Young Samwell Tarly | affc-samwell-02 |
| saved | 2 | Xhondo → Sam | affc-samwell-04 |
| Deep distrust of | 2 | Archmaester Marwyn → The Citadel ("grey sheep") | affc-samwell-05 |
| Resented | 2 | Ser Marwyn Belmore → Marillion | affc-sansa-01 |
| Rivals | 2 | Victarion → Euron | affc-the-iron-captain-01 |
| Has support of | 2 | Asha → House Harlaw (Rodrik the Reader) | affc-the-iron-captain-01 |
| childhood companions with | 2 | Arianne Martell → Nymeria Sand (Nym) | affc-the-princess-in-the-tower-01 |
| not close to | 2 | Arianne Martell → Quentyn Martell | affc-the-princess-in-the-tower-01 |
| Protector | 2 | Arianne Martell → Princess Myrcella | affc-the-queenmaker-01 |
| Raped | 2 | Euron → Victarion's wife | affc-the-reaver-01 |
| Works with | 2 | Lady Dustin → Roose Bolton | adwd-a-ghost-in-winterfell-01 |
| Possessive of | 2 | Ramsay Bolton → Yellow Dick | adwd-a-ghost-in-winterfell-01 |
| is advised by | 2 | Daenerys → Reznak mo Reznak | adwd-daenerys-06 |
| Suitor to | 2 | Quentyn Martell → Daenerys | adwd-daenerys-07 |
| affected by | 2 | Strong Belwas → Honeyed locusts | adwd-daenerys-09 |
| queen to | 2 | Daenerys → Ser Barristan Selmy | adwd-daenerys-10 |
| kin to | 2 | Ser Jared Frey → Jinglebell | adwd-davos-03 |
| conditional allegiance to | 2 | Manderly → King Stannis | adwd-davos-04 |
| Tensions with | 2 | Jon Snow → Bowen Marsh | adwd-jon-03 |
| Religious authority over | 2 | Melisandre → Queen's men | adwd-jon-03 |
| Aspires to | 2 | Ser Richard Horpe → Winterfell | adwd-jon-04 |
| wishes present | 2 | Jon Snow → Sam Tarly | adwd-jon-08 |
| Father | 2 | Tormund → Toregg | adwd-jon-11 |
| Disapproval | 2 | Queen Selyse → Jon Snow | adwd-jon-11 |
| Swears allegiance to | 2 | Morna White Mask → Jon Snow | adwd-jon-12 |
| Squire serving | 2 | Big Walder Frey → Ramsay Bolton | adwd-reek-01 |
| Longing for / regret | 2 | Quentyn Martell → Gwyneth Yronwood | adwd-the-dragontamer-01 |
| sent to capture | 2 | Ser Tristan Rivers → Crow's Nest (House Morrigen) | adwd-the-griffin-reborn-01 |
| Hostility from | 2 | Moqorro → Dusky woman | adwd-the-iron-suitor-01 |
| Loyal protector of | 2 | Barristan → Daenerys Targaryen | adwd-the-kingbreaker-01 |
| Eager for battle | 2 | Symon Stripeback → Yunkai'i | adwd-the-kingbreaker-01 |
| Support | 2 | Laswell Peake → Aegon | adwd-the-lost-lord-01 |
| Guarded by | 2 | The old man → The tall thin guard | adwd-the-ugly-little-girl-01 |
| Professional rapport with | 2 | Haldon → Qavo Nogarys | adwd-tyrion-06 |
| Hated by | 2 | Tyrion Lannister → Cersei Lannister | adwd-tyrion-07 |
| sibling rivalry / resentment | 1 | Arya → Sansa | agot-arya-01 |
| dearest friend | 1 | Sansa → Jeyne Poole | agot-arya-01 |
| infatuation | 1 | Sansa → Joffrey | agot-arya-01 |
| flattery toward | 1 | Joffrey → Sansa | agot-arya-01 |
| cautious greeting | 1 | Ghost → Nymeria | agot-arya-01 |
| wary approach | 1 | Nymeria → Ghost | agot-arya-01 |
| fawning toward | 1 | Septa Mordane → Myrcella | agot-arya-01 |
| eagerness to fight | 1 | Robb → Joffrey | agot-arya-01 |
| restrains / supports | 1 | Theon Greyjoy → Robb | agot-arya-01 |
| resemble | 1 | Robb, Sansa, Bran, Rickon → Tullys | agot-arya-01 |
| father, protective/understanding | 1 | Ned Stark → Arya | agot-arya-02 |
| duty/resentment | 1 | Ned Stark → Robert Baratheon | agot-arya-02 |
| former servant | 1 | Syrio Forel → Sealord of Braavos | agot-arya-02 |
| loyalty/protectiveness toward | 1 | Arya → Jon Snow | agot-arya-02 |
| Daughter of, reports to | 1 | Arya Stark → Eddard Stark | agot-arya-03 |
| Condescends toward | 1 | Myrcella Baratheon → Arya (unrecognized) | agot-arya-03 |
| Flatters / relies on | 1 | Fat man (forked beard) → Stout man (torchbearer) | agot-arya-03 |
| Welcomes | 1 | Eddard Stark → Night's Watch | agot-arya-03 |
| daughter of, desperate to save | 1 | Arya → Eddard Stark | agot-arya-05 |
| scowls at, puzzled by | 1 | Arya → Sansa Stark | agot-arya-05 |
| Bastard son of | 1 | Jon Snow → Eddard Stark | agot-bran-01 |
| Captain of household guard for | 1 | Jory Cassel → Eddard Stark | agot-bran-01 |
| Master of horse for | 1 | Hullen → Eddard Stark | agot-bran-01 |
| Excluded from / self-excludes from | 1 | Jon Snow → House Stark | agot-bran-01 |
| Regards thoughtfully | 1 | Ned Stark → Jon Snow | agot-bran-01 |
| Has coloring of | 1 | Robb Stark → House Tully | agot-bran-01 |
| angry at / distant from | 1 | Jon Snow → Everyone | agot-bran-02 |
| going with | 1 | Jon Snow → Benjen Stark | agot-bran-02 |
| sibling/sexual partner of | 1 | Cersei Lannister → Jaime Lannister | agot-bran-02 |
| pushes/attempts to kill | 1 | Jaime Lannister → Bran Stark | agot-bran-02 |
| fled from | 1 | Lysa Arryn → King's Landing | agot-bran-02 |
| shared bed with | 1 | Lysa Arryn → Jon Arryn | agot-bran-02 |
| has authority over | 1 | Eddard Stark → Bran Stark | agot-bran-02 |
| storyteller/caretaker to | 1 | Old Nan → Bran Stark | agot-bran-02 |
| frightened of | 1 | Bran Stark → Heart tree | agot-bran-02 |
| Teacher / guide | 1 | Three-eyed crow → Bran | agot-bran-03 |
| Names and bonds with | 1 | Bran → Summer | agot-bran-03 |
| Son, recalls father's courage | 1 | Bran → Eddard Stark | agot-bran-03 |
| Mother, separated from Bran | 1 | Catelyn → Bran | agot-bran-03 |
| Aware observer | 1 | Weirwood → Bran | agot-bran-03 |
| Threatening memory | 1 | Golden face → Bran | agot-bran-03 |
| acting lord role | 1 | Robb → Winterfell | agot-bran-04 |
| emotional bond | 1 | Robb → Bran | agot-bran-04 |
| anger regarding | 1 | Robb → Benjen Stark (missing) | agot-bran-04 |
| mocking | 1 | Theon Greyjoy → Tyrion | agot-bran-04 |
| spends time with | 1 | Robb → Theon Greyjoy, Hallis Mollen | agot-bran-04 |
| caretaker / storyteller | 1 | Old Nan → Bran | agot-bran-04 |
| practical advisor | 1 | Maester Luwin → Robb | agot-bran-04 |
| intellectual engagement | 1 | Maester Luwin → Tyrion's saddle design | agot-bran-04 |
| Sexual familiarity | 1 | Theon → Kyra | agot-bran-05 |
| Surrenders to / serves | 1 | Osha → Robb | agot-bran-05 |
| Pragmatic self-interest | 1 | Osha → Bran | agot-bran-05 |
| Competitive / self-congratulatory | 1 | Theon → Robb | agot-bran-05 |
| Ambivalent memory | 1 | Bran → Tyrion Lannister | agot-bran-05 |
| acting lord over | 1 | Robb → Northern bannermen | agot-bran-06 |
| private vulnerability with | 1 | Robb → Bran | agot-bran-06 |
| distraught about losing | 1 | Rickon → Robb | agot-bran-06 |
| initially hostile, then fiercely loyal to | 1 | Greatjon Umber → Robb | agot-bran-06 |
| unsettling presence toward | 1 | Roose Bolton → Robb | agot-bran-06 |
| currying favor with | 1 | Lord Hornwood → Robb | agot-bran-06 |
| informant/supplicant to | 1 | Osha → Bran | agot-bran-06 |
| understands | 1 | Bran → Sansa | agot-bran-06 |
| kinship (distant) with | 1 | Karstarks → Starks | agot-bran-06 |
| speaks of with familiarity | 1 | Osha → Mance Rayder | agot-bran-06 |
| exercises authority over | 1 | Bran → Maester Luwin | agot-bran-07 |
| frustrated by disability | 1 | Bran → (self) | agot-bran-07 |
| rationalist / dismissive of magic | 1 | Maester Luwin → Osha | agot-bran-07 |
| contradicts | 1 | Osha → Maester Luwin | agot-bran-07 |
| loyal/obedient to | 1 | Osha → Starks | agot-bran-07 |
| gentle toward | 1 | Osha → Bran | agot-bran-07 |
| wild/dangerous | 1 | Shaggydog → Maester Luwin | agot-bran-07 |
| refuses to enter | 1 | Hodor → Winterfell crypts | agot-bran-07 |
| habitual concern for children | 1 | Ned Stark → Catelyn | agot-catelyn-01 |
| fellow ward with | 1 | Ned Stark → Robert Baratheon | agot-catelyn-01 |
| antipathy toward | 1 | Ned Stark → The Lannisters | agot-catelyn-01 |
| raised banners to protect | 1 | Jon Arryn → Ned and Robert | agot-catelyn-01 |
| religious contrast with | 1 | Catelyn → Ned Stark | agot-catelyn-01 |
| built for | 1 | Ned Stark → Catelyn | agot-catelyn-01 |
| lord served by | 1 | Ned Stark → Jory | agot-catelyn-01 |
| Deep bond, "closer than brothers" | 1 | Eddard Stark → Robert Baratheon | agot-catelyn-02 |
| Grew up with | 1 | Catelyn Stark → Edmure Tully | agot-catelyn-02 |
| Father, protective | 1 | Eddard Stark → Jon Snow | agot-catelyn-02 |
| Father, trusts with governance | 1 | Eddard Stark → Robb Stark | agot-catelyn-02 |
| Protective, reluctant to separate from | 1 | Eddard Stark → Bran Stark | agot-catelyn-02 |
| Deep trust | 1 | Eddard Stark → Maester Luwin | agot-catelyn-02 |
| Slew in combat (recalled) | 1 | Eddard Stark → Ser Arthur Dayne | agot-catelyn-02 |
| Possible romantic connection (rumored) | 1 | Eddard Stark → Ashara Dayne | agot-catelyn-02 |
| Tension / "bad feeling" with | 1 | Robb Stark → Joffrey Baratheon | agot-catelyn-02 |
| Ensures exclusion of | 1 | Cersei Lannister → Robert's bastards | agot-catelyn-02 |
| Mother, devoted to the point of obsession | 1 | Catelyn → Bran | agot-catelyn-03 |
| Mother, neglectful (temporarily) | 1 | Catelyn → Rickon | agot-catelyn-03 |
| Son, stepping into authority | 1 | Robb → Catelyn | agot-catelyn-03 |
| Loyal advisor, persistent | 1 | Maester Luwin → Catelyn / Robb | agot-catelyn-03 |
| Loyal retainer | 1 | Ser Rodrik Cassel → Catelyn | agot-catelyn-03 |
| Ward, declares loyalty | 1 | Theon Greyjoy → Eddard Stark / House Stark | agot-catelyn-03 |
| Suspicion and hostility toward | 1 | Catelyn → Jaime Lannister / the Lannisters | agot-catelyn-03 |
| Savior | 1 | Bran's direwolf → Catelyn | agot-catelyn-03 |
| New captain of the guard | 1 | Hallis Mollen → Robb | agot-catelyn-03 |
| Romantic rival (historical) | 1 | Petyr Baelish → Brandon Stark | agot-catelyn-04 |
| Married (in place of Brandon) | 1 | Catelyn Stark → Eddard Stark | agot-catelyn-04 |
| Named / nicknamed | 1 | Edmure Tully → Petyr Baelish | agot-catelyn-04 |
| Was ward of | 1 | Petyr Baelish → Hoster Tully (implied) | agot-catelyn-04 |
| Partially trusts | 1 | Catelyn Stark → Petyr Baelish | agot-catelyn-04 |
| Likely betrayed trust of | 1 | Captain Moreo → Catelyn Stark | agot-catelyn-04 |
| Lost dagger in bet to | 1 | Littlefinger → Tyrion Lannister | agot-catelyn-04 |
| Defeated in jousting | 1 | Loras Tyrell → Ser Jaime Lannister | agot-catelyn-04 |
| Consulted | 1 | Ser Rodrik Cassel → Ser Aron Santagar | agot-catelyn-04 |
| accuses / arrests | 1 | Catelyn Stark → Tyrion Lannister | agot-catelyn-05 |
| characterized as unreliable by | 1 | Lord Walder Frey → Hoster Tully | agot-catelyn-05 |
| exposes identity of | 1 | Marillion → Catelyn Stark | agot-catelyn-05 |
| innkeeper hosting | 1 | Masha Heddle → Catelyn Stark | agot-catelyn-05 |
| disloyal to (historically) | 1 | Houses Darry, Ryger, Mooton → House Tully | agot-catelyn-05 |
| Fiercely protective, smothering | 1 | Lysa Arryn → Robert Arryn | agot-catelyn-06 |
| Pitying of | 1 | Catelyn → Mya Stone | agot-catelyn-06 |
| Deferential to / serves | 1 | Lord Nestor Royce → Lysa Arryn | agot-catelyn-06 |
| Loyal but frustrated servant of | 1 | Ser Donnel Waynwood → Lysa Arryn | agot-catelyn-06 |
| Protective but critical of | 1 | Brynden Tully → Lysa Arryn | agot-catelyn-06 |
| Sardonic about his family | 1 | Tyrion Lannister → Jaime, Cersei, Tywin Lannister | agot-catelyn-06 |
| Dependent on / clings to | 1 | Robert Arryn → Lysa Arryn | agot-catelyn-06 |
| Relies on as advisor | 1 | Catelyn → Ser Rodrik | agot-catelyn-07 |
| Mother (overprotective) | 1 | Lysa → Robert Arryn | agot-catelyn-07 |
| Surrounded by suitors | 1 | Lysa → Lord Hunter, Ser Lyn Corbray, Ser Morton Waynwood | agot-catelyn-07 |
| Champion-client | 1 | Tyrion → Bronn | agot-catelyn-07 |
| Champion/loyal servant | 1 | Ser Vardis → Lysa Arryn | agot-catelyn-07 |
| Nursed/cared for (past) | 1 | Lysa → Petyr Baelish | agot-catelyn-07 |
| Squired for Brandon / rejected by Petyr (past) | 1 | Edmure Tully → Brandon Stark / Petyr Baelish | agot-catelyn-07 |
| Father (protective, past) | 1 | Lord Hoster Tully → Catelyn / Petyr | agot-catelyn-07 |
| Accepts | 1 | Grey Wind → Catelyn | agot-catelyn-08 |
| Sons of | 1 | Ser Wylis/Wendel Manderly → Lord Wyman Manderly | agot-catelyn-08 |
| Unsettled by | 1 | Catelyn → Roose Bolton | agot-catelyn-08 |
| Advised by | 1 | Robb → Catelyn | agot-catelyn-08 |
| Sees Ned in | 1 | Catelyn → Robb | agot-catelyn-08 |
| Sees Tully in | 1 | Catelyn → Robb | agot-catelyn-08 |
| Named castellan by | 1 | Ser Rodrik Cassel → Catelyn | agot-catelyn-08 |
| bannerman to (unreliable) | 1 | Walder Frey → Hoster Tully | agot-catelyn-09 |
| heir to, waits on | 1 | Ser Stevron Frey → Walder Frey | agot-catelyn-09 |
| Follows teachings of | 1 | Robb → Ned Stark | agot-catelyn-10 |
| Captured enemy of | 1 | Jaime Lannister → Robb / Catelyn | agot-catelyn-10 |
| Wants revenge on | 1 | Lord Karstark → Jaime Lannister | agot-catelyn-10 |
| Daughter and heir of | 1 | Dacey Mormont → Maege Mormont | agot-catelyn-10 |
| Cold hostility toward | 1 | Catelyn → Jaime Lannister | agot-catelyn-10 |
| echoes / resembles | 1 | Robb → Eddard Stark | agot-catelyn-11 |
| estranged from / quarrels with | 1 | Hoster → Brynden Tully | agot-catelyn-11 |
| wants to see | 1 | Hoster → Lysa Arryn | agot-catelyn-11 |
| represents | 1 | Stevron Frey → Walder Frey | agot-catelyn-11 |
| bereaved father of | 1 | Rickard Karstark → Torrhen Karstark, Eddard Karstark | agot-catelyn-11 |
| advocating for return of | 1 | Catelyn → Sansa Stark, Arya Stark | agot-catelyn-11 |
| fought duel with | 1 | Petyr Baelish → Brandon Stark | agot-catelyn-11 |
| Abuses/controls | 1 | Viserys → Daenerys | agot-daenerys-01 |
| Sells/trades | 1 | Viserys → Daenerys | agot-daenerys-01 |
| Hosts/patronizes | 1 | Illyrio → Viserys & Daenerys | agot-daenerys-01 |
| Flatters/manipulates | 1 | Illyrio → Viserys | agot-daenerys-01 |
| Arranges marriage between | 1 | Illyrio → Daenerys and Khal Drogo | agot-daenerys-01 |
| Claims kingship over | 1 | Viserys → Westeros / Seven Kingdoms | agot-daenerys-01 |
| Exiled from | 1 | Ser Jorah Mormont → Westeros | agot-daenerys-01 |
| Buy peace from | 1 | Magisters of Pentos → Dothraki khals | agot-daenerys-01 |
| Claims support from | 1 | Viserys → Houses Tyrell, Redwyne, Darry, Greyjoy, and Dorne | agot-daenerys-01 |
| Sold/traded | 1 | Viserys → Dany to Drogo | agot-daenerys-02 |
| Facilitated marriage of | 1 | Illyrio → Dany and Drogo | agot-daenerys-02 |
| Husband to | 1 | Drogo → Dany | agot-daenerys-02 |
| Mistress to | 1 | Dany → Irri, Jhiqui, Doreah | agot-daenerys-02 |
| Gentle/tender toward | 1 | Drogo → Dany | agot-daenerys-02 |
| Evolving intimacy with | 1 | Daenerys → Khal Drogo | agot-daenerys-03 |
| Ignored and used | 1 | Khal Drogo → Daenerys (early) | agot-daenerys-03 |
| Offered hospitality to | 1 | Illyrio Mopatis → Viserys | agot-daenerys-03 |
| Enslaved by (in past) | 1 | Irri and Jhiqui → Khal Drogo | agot-daenerys-03 |
| Purchased from | 1 | Doreah → A pleasure house in Lys | agot-daenerys-03 |
| Growing independence from | 1 | Daenerys → Viserys | agot-daenerys-04 |
| Mystical connection to | 1 | Daenerys → Dragon eggs | agot-daenerys-04 |
| Bound to | 1 | Cohollo → Khal Drogo | agot-daenerys-04 |
| wife/khaleesi of | 1 | Daenerys → Khal Drogo | agot-daenerys-05 |
| demands payment from | 1 | Viserys → Khal Drogo | agot-daenerys-05 |
| is teaching Common Tongue to | 1 | Daenerys → Khal Drogo | agot-daenerys-05 |
| taught Dothraki phrases to | 1 | Jhiqui → Daenerys | agot-daenerys-05 |
| named child after | 1 | Daenerys → Rhaegar Targaryen | agot-daenerys-05 |
| raised/told family history to | 1 | Viserys → Daenerys | agot-daenerys-05 |
| prophesies for | 1 | Dosh khaleen → Daenerys/Rhaego | agot-daenerys-05 |
| attempted theft from | 1 | Viserys → Daenerys | agot-daenerys-05 |
| Husband / authority figure, devoted | 1 | Khal Drogo → Daenerys | agot-daenerys-06 |
| Protector and advisor | 1 | Ser Jorah → Daenerys | agot-daenerys-06 |
| Devoted handmaid / protector | 1 | Doreah → Daenerys | agot-daenerys-06 |
| Loyal khas warrior | 1 | Jhogo → Daenerys | agot-daenerys-06 |
| Rewards loyalty | 1 | Khal Drogo → Jhogo, Ser Jorah | agot-daenerys-06 |
| Hostile / threatens | 1 | Robert Baratheon → Daenerys | agot-daenerys-06 |
| Attempted assassin | 1 | Wine merchant → Daenerys | agot-daenerys-06 |
| Punisher | 1 | Daenerys → Wine merchant | agot-daenerys-06 |
| wife of / devoted to | 1 | Dany → Drogo | agot-daenerys-07 |
| husband of / supportive of | 1 | Drogo → Dany | agot-daenerys-07 |
| corresponds with | 1 | Ser Jorah → Illyrio | agot-daenerys-07 |
| healer of / obedient to | 1 | Mirri Maz Duur → Drogo | agot-daenerys-07 |
| reminded of Viserys by | 1 | Dany → Qotho | agot-daenerys-07 |
| claims as slaves | 1 | Dany → Lhazareen women | agot-daenerys-07 |
| echoes Dothraki customs | 1 | Irri → Dany | agot-daenerys-07 |
| wife / desperate caretaker of | 1 | Dany → Drogo | agot-daenerys-08 |
| relies on for ritual | 1 | Dany → Mirri Maz Duur | agot-daenerys-08 |
| hostile / threatening toward | 1 | Qotho → Dany | agot-daenerys-08 |
| assists in killing | 1 | Jhogo → Haggo | agot-daenerys-08 |
| bound life to | 1 | Cohollo → Drogo | agot-daenerys-08 |
| had been kind to | 1 | Cohollo → Dany | agot-daenerys-08 |
| slave of | 1 | Mirri Maz Duur → Dany | agot-daenerys-08 |
| performs blood ritual for | 1 | Mirri Maz Duur → Drogo | agot-daenerys-08 |
| share one life with | 1 | Bloodriders (Qotho, Haggo, Cohollo) → Drogo | agot-daenerys-08 |
| call him | 1 | Dothraki calling Ser Jorah → "The Andal" | agot-daenerys-08 |
| protector/advisor of | 1 | Ser Jorah Mormont → Daenerys | agot-daenerys-09 |
| holds responsible | 1 | Daenerys → Ser Jorah Mormont | agot-daenerys-09 |
| connected to (mystically) | 1 | Daenerys → Dragon eggs | agot-daenerys-09 |
| Claims queenship / heir to | 1 | Daenerys → Viserys Targaryen | agot-daenerys-10 |
| Condemns / sacrifices | 1 | Daenerys → Mirri Maz Duur | agot-daenerys-10 |
| Conditional loyalty to | 1 | Rakharo → Daenerys | agot-daenerys-10 |
| Thinks of / compares self to | 1 | Daenerys → Aegon (the Conqueror) | agot-daenerys-10 |
| Undying hatred for | 1 | Robert Baratheon → Rhaegar Targaryen | agot-eddard-01 |
| Cold/hostile marriage with | 1 | Robert Baratheon → Cersei Lannister | agot-eddard-01 |
| Frustration/contempt for | 1 | Robert Baratheon → Lysa Arryn | agot-eddard-01 |
| Plans to join houses with | 1 | Robert Baratheon → Ned Stark | agot-eddard-01 |
| Took as hostage/ward | 1 | Ned Stark → Theon Greyjoy | agot-eddard-01 |
| Haunted by promise to | 1 | Ned Stark → Lyanna Stark | agot-eddard-01 |
| Present at death of | 1 | Howland Reed → Lyanna Stark | agot-eddard-01 |
| Old friend / king to Hand | 1 | Robert → Ned | agot-eddard-02 |
| Frustrated spouse | 1 | Robert → Cersei | agot-eddard-02 |
| Obsessive hatred | 1 | Robert → Targaryens (all) | agot-eddard-02 |
| Guilt and concealment | 1 | Ned → Wylla / "his bastard" | agot-eddard-02 |
| Moral opposition | 1 | Ned → Tywin Lannister | agot-eddard-02 |
| Deep distrust | 1 | Ned → Jaime Lannister | agot-eddard-02 |
| Trust / dismissal | 1 | Robert → Jaime Lannister | agot-eddard-02 |
| Lord / failed justice | 1 | Ned → Jorah Mormont | agot-eddard-02 |
| Spymaster serving | 1 | Varys → Robert | agot-eddard-02 |
| Spy serving | 1 | Jorah Mormont → Varys | agot-eddard-02 |
| Haunted by promise | 1 | Ned → Lyanna Stark | agot-eddard-02 |
| Dismissed concern from | 1 | Robert → Ned | agot-eddard-02 |
| Bannerman lord over | 1 | Ned → House Mormont | agot-eddard-02 |
| Old friend, growing tension | 1 | Eddard Stark → Robert Baratheon | agot-eddard-03 |
| Antagonism | 1 | Eddard Stark → Cersei Lannister | agot-eddard-03 |
| King, conflicted | 1 | Robert Baratheon → Eddard Stark | agot-eddard-03 |
| Hostility | 1 | Arya Stark → Joffrey Baratheon | agot-eddard-03 |
| Rage, betrayal | 1 | Arya Stark → Sansa Stark | agot-eddard-03 |
| Lies/accuses | 1 | Joffrey Baratheon → Arya Stark | agot-eddard-03 |
| Reluctant host | 1 | Ser Raymun Darry → Robert Baratheon | agot-eddard-03 |
| Reluctant servant | 1 | Barristan Selmy → Cersei Lannister | agot-eddard-03 |
| husband, protector | 1 | Ned → Catelyn | agot-eddard-04 |
| unrequited attachment to | 1 | Littlefinger → Catelyn | agot-eddard-04 |
| former rival/defeated by | 1 | Littlefinger → Brandon Stark | agot-eddard-04 |
| deferential to | 1 | Varys → Ned | agot-eddard-04 |
| deferential, passive | 1 | Pycelle → Ned | agot-eddard-04 |
| absent, neglectful ruler | 1 | Robert → The realm | agot-eddard-04 |
| claims leverage over | 1 | Littlefinger → Varys | agot-eddard-04 |
| orders military preparation against | 1 | Ned → House Lannister | agot-eddard-04 |
| watches cautiously | 1 | Ned → Theon Greyjoy | agot-eddard-04 |
| loyal escort to | 1 | Ser Rodrik → Catelyn | agot-eddard-04 |
| Deflects suspicion toward | 1 | Pycelle → Varys | agot-eddard-05 |
| Overruled | 1 | Pycelle → Maester Colemon | agot-eddard-05 |
| Took to godswood | 1 | Ned → Arya, Sansa | agot-eddard-05 |
| presides over council in absence of | 1 | Ned → Robert | agot-eddard-06 |
| rode with / closely associated with | 1 | Jon Arryn → Stannis Baratheon | agot-eddard-06 |
| visited and questioned | 1 | Jon Arryn → Gendry | agot-eddard-06 |
| accompanied but remained silent with | 1 | Stannis → Gendry | agot-eddard-06 |
| is captain of guard for | 1 | Ned → Jory Cassel | agot-eddard-06 |
| master of apprentice | 1 | Tobho Mott → Gendry | agot-eddard-06 |
| is bastard of (inferred) | 1 | Gendry → Robert Baratheon | agot-eddard-06 |
| paid apprentice fee for | 1 | Unknown lord → Gendry | agot-eddard-06 |
| shows portrait of | 1 | Renly → Margaery Tyrell | agot-eddard-06 |
| compared appearance to | 1 | Renly → young Robert | agot-eddard-06 |
| yearns for home with | 1 | Ned → Robb Stark, Jon Snow | agot-eddard-06 |
| finds Gendry has look of a warrior, offers future service to | 1 | Ned → Gendry | agot-eddard-06 |
| despairs of | 1 | Robert Baratheon → Joffrey Baratheon | agot-eddard-07 |
| devoted student of | 1 | Arya Stark → Syrio Forel | agot-eddard-07 |
| deep enmity with | 1 | Sandor Clegane → Gregor Clegane | agot-eddard-07 |
| violent fury toward | 1 | Ser Gregor Clegane → Ser Loras Tyrell | agot-eddard-07 |
| wagers against/banter with | 1 | Littlefinger → Lord Renly | agot-eddard-07 |
| admits Joffrey lied about | 1 | Robert Baratheon → Sansa's direwolf incident | agot-eddard-07 |
| concedes victory to / gratitude | 1 | Loras Tyrell → Sandor Clegane | agot-eddard-07 |
| sisterly civility toward | 1 | Sansa Stark → Arya Stark | agot-eddard-07 |
| Defers to pragmatism over | 1 | Renly → Jon Arryn's memory | agot-eddard-08 |
| Previously showed mercy to | 1 | Robert → Ser Barristan | agot-eddard-08 |
| Urged killing of | 1 | Roose Bolton → Ser Barristan | agot-eddard-08 |
| Claims to protect (ambiguously) | 1 | Littlefinger → Daenerys | agot-eddard-08 |
| Avoids marrying | 1 | Littlefinger → Lady Tanda's daughter | agot-eddard-08 |
| Suspects shared knowledge with | 1 | Ned → Stannis Baratheon | agot-eddard-08 |
| Worries about consequences for | 1 | Ned → Catelyn Stark | agot-eddard-08 |
| Sent raven to | 1 | Pycelle → Stannis Baratheon | agot-eddard-08 |
| Monitors | 1 | Littlefinger → Jory Cassel | agot-eddard-08 |
| former Hand to the king of | 1 | Eddard Stark → Robert Baratheon | agot-eddard-09 |
| guide/informant to | 1 | Littlefinger → Eddard Stark | agot-eddard-09 |
| loyal guard to | 1 | Jory Cassel → Eddard Stark | agot-eddard-09 |
| hostile confrontation with | 1 | Jaime Lannister → Eddard Stark | agot-eddard-09 |
| clear-eyed about | 1 | Lyanna Stark → Robert Baratheon | agot-eddard-09 |
| paternal feeling toward | 1 | Eddard Stark → Jon Snow | agot-eddard-09 |
| offended by | 1 | Stannis Baratheon → Robert Baratheon | agot-eddard-09 |
| familiar with | 1 | Littlefinger → Chataya | agot-eddard-09 |
| treats | 1 | Grand Maester Pycelle → Eddard Stark | agot-eddard-09 |
| Domestic violence/toxic marriage | 1 | Robert Baratheon → Cersei Lannister | agot-eddard-10 |
| Specifically remembers | 1 | Eddard Stark → Howland Reed | agot-eddard-10 |
| Bound by promise to | 1 | Eddard Stark → Lyanna Stark | agot-eddard-10 |
| Fought against | 1 | Ned's companions (7) → Three Kingsguard | agot-eddard-10 |
| Guarded/protected | 1 | Kingsguard (three) → Lyanna Stark | agot-eddard-10 |
| Watches Cersei's reaction to | 1 | Ned → Barra revelation | agot-eddard-10 |
| Provided testimony to | 1 | Petyr Baelish → Robert Baratheon | agot-eddard-10 |
| Acts as regent/Hand for | 1 | Eddard Stark → Robert Baratheon | agot-eddard-11 |
| Questions / probes | 1 | Littlefinger → Riverlord knights | agot-eddard-11 |
| Eager to oppose | 1 | Ser Loras Tyrell → Gregor Clegane | agot-eddard-11 |
| Denies / checks | 1 | Eddard Stark → Ser Loras Tyrell | agot-eddard-11 |
| Judges as unwise | 1 | Eddard Stark → Edmure Tully | agot-eddard-11 |
| Sends as messenger | 1 | Ned Stark → Ser Robar Royce | agot-eddard-11 |
| Furious with / opposes | 1 | Tywin Lannister → Eddard Stark | agot-eddard-12 |
| Nickname | 1 | Ned's children (household) → Tomard | agot-eddard-12 |
| Feels duty toward | 1 | Eddard Stark → Robert Baratheon | agot-eddard-12 |
| Attempts to seduce/manipulate | 1 | Cersei Lannister → Eddard Stark | agot-eddard-12 |
| Would kill for | 1 | Jaime Lannister → Cersei Lannister | agot-eddard-12 |
| Trust and reliance | 1 | Robert Baratheon → Eddard Stark | agot-eddard-13 |
| Estrangement / dismissiveness | 1 | Robert Baratheon → Cersei Lannister | agot-eddard-13 |
| Watchful presence at deathbed | 1 | Cersei Lannister → Robert Baratheon | agot-eddard-13 |
| Guilt and devotion | 1 | Ser Barristan Selmy → Robert Baratheon | agot-eddard-13 |
| Suspicion / implication | 1 | Varys → Lancel Lannister | agot-eddard-13 |
| Information broker | 1 | Varys → Littlefinger | agot-eddard-13 |
| Political manipulation / self-interest | 1 | Littlefinger → Eddard Stark | agot-eddard-13 |
| Moral contempt tempered by need | 1 | Eddard Stark → Littlefinger | agot-eddard-13 |
| Guilt and remorse | 1 | Robert Baratheon → Daenerys Targaryen | agot-eddard-13 |
| Protective commitment | 1 | Ned → Robert's bastards (Barra, Mya, Gendry) | agot-eddard-13 |
| Deferential service | 1 | Grand Maester Pycelle → Robert Baratheon | agot-eddard-13 |
| Echoed memory connection | 1 | Ned → Lyanna Stark | agot-eddard-13 |
| Dutiful attendant to | 1 | Septa Mordane → Eddard Stark | agot-eddard-14 |
| Reliance on (misplaced) | 1 | Eddard Stark → Petyr Baelish | agot-eddard-14 |
| Counted on support of | 1 | Eddard Stark → Renly Baratheon | agot-eddard-14 |
| Hopes for / relies on (absent) | 1 | Eddard Stark → Stannis Baratheon | agot-eddard-14 |
| Honor-bound loyalty to | 1 | Ser Barristan Selmy → Joffrey Baratheon | agot-eddard-14 |
| Shocked/loyal to | 1 | Ser Barristan Selmy → Robert Baratheon (deceased) | agot-eddard-14 |
| Demands loyalty from | 1 | Joffrey Baratheon → Small council | agot-eddard-14 |
| Enraged by | 1 | Joffrey Baratheon → Eddard Stark | agot-eddard-14 |
| Confused/dependent on | 1 | Myrcella Baratheon → Cersei Lannister | agot-eddard-14 |
| feels shame and sorrow toward | 1 | Eddard Stark → Jon Snow | agot-eddard-15 |
| holds secret of | 1 | Eddard Stark → Lyanna Stark | agot-eddard-15 |
| claims to have protected | 1 | Varys → Robert Baratheon | agot-eddard-15 |
| orchestrated death of | 1 | Cersei Lannister → Robert Baratheon | agot-eddard-15 |
| served as instrument of | 1 | Lancel Lannister → Cersei Lannister | agot-eddard-15 |
| pleaded for life of | 1 | Sansa Stark → Eddard Stark | agot-eddard-15 |
| crowned as queen of beauty | 1 | Rhaegar Targaryen → Lyanna Stark | agot-eddard-15 |
| took vows before | 1 | Jaime Lannister → King Aerys | agot-eddard-15 |
| fastened white cloak on | 1 | Ser Gerold Hightower → Jaime Lannister | agot-eddard-15 |
| helped to feet | 1 | Ser Oswell Whent → Jaime Lannister | agot-eddard-15 |
| owned | 1 | Rhaenys Targaryen → Balerion (the cat) | agot-eddard-15 |
| is true heir of | 1 | Stannis Baratheon → Robert Baratheon | agot-eddard-15 |
| marches south with army for | 1 | Robb Stark → Eddard Stark | agot-eddard-15 |
| traveled with as youth | 1 | Varys → Troupe of mummers | agot-eddard-15 |
| son (complicated) | 1 | Jon Snow → Eddard Stark | agot-jon-01 |
| excluded by | 1 | Jon Snow → Catelyn Stark | agot-jon-01 |
| grudging mutual recognition | 1 | Jon Snow → Tyrion Lannister | agot-jon-01 |
| fascination toward | 1 | Jon Snow → Tyrion Lannister | agot-jon-01 |
| sees through | 1 | Jon Snow → Cersei Lannister | agot-jon-01 |
| hosts (formally) | 1 | Eddard Stark → Cersei Lannister | agot-jon-01 |
| cold/angry | 1 | Cersei Lannister → Robert Baratheon | agot-jon-01 |
| twin to | 1 | Jaime Lannister → Cersei Lannister | agot-jon-01 |
| dominance over | 1 | Ghost → Mongrel dog | agot-jon-01 |
| Excluded outsider / target of hostility | 1 | Jon → Catelyn | agot-jon-02 |
| Hostile rejection | 1 | Catelyn → Jon | agot-jon-02 |
| Devoted, desperate mother | 1 | Catelyn → Bran | agot-jon-02 |
| Brotherly concern for Jon | 1 | Robb → Jon | agot-jon-02 |
| Adoration / deep bond | 1 | Arya → Jon | agot-jon-02 |
| Self-identifies as outsider to Stark family | 1 | Jon → Himself | agot-jon-02 |
| Guilt / religious devotion | 1 | Catelyn → The Seven (Faith) | agot-jon-02 |
| Growing into authority | 1 | Robb → Winterfell household | agot-jon-02 |
| feels contempt toward (initially) | 1 | Jon Snow → Night's Watch recruits | agot-jon-03 |
| confronts | 1 | Grenn → Jon Snow | agot-jon-03 |
| rebuffs and distances from | 1 | Benjen Stark → Jon Snow | agot-jon-03 |
| spends time with (as peer) | 1 | Benjen Stark → Jeor Mormont | agot-jon-03 |
| shows compassion toward | 1 | Tyrion Lannister → Jon Snow | agot-jon-03 |
| clashes with | 1 | Ser Alliser Thorne → Tyrion Lannister | agot-jon-03 |
| offers to help/train | 1 | Jon Snow → Grenn | agot-jon-03 |
| declares enmity toward | 1 | Ser Alliser Thorne → Jon Snow | agot-jon-03 |
| forged weapon for | 1 | Donal Noye → Robert Baratheon | agot-jon-03 |
| wonders about / questions | 1 | Jon Snow → Eddard Stark | agot-jon-03 |
| cannot pray to | 1 | Jon Snow → The gods (old or new) | agot-jon-03 |
| writes to | 1 | Robb Stark → Jon Snow (via Mormont) | agot-jon-03 |
| Protector and emerging leader | 1 | Jon Snow → Samwell Tarly | agot-jon-04 |
| Antagonist/tormentor | 1 | Ser Alliser Thorne → Jon Snow | agot-jon-04 |
| Cruel authority | 1 | Ser Alliser Thorne → Samwell Tarly | agot-jon-04 |
| Hostile/defiant toward Jon | 1 | Rast → Jon Snow | agot-jon-04 |
| Comfort/protection | 1 | Ghost → Samwell Tarly | agot-jon-04 |
| Enforcer/weapon | 1 | Ghost → Rast | agot-jon-04 |
| Abusive, threatening father | 1 | Lord Randyll Tarly → Samwell Tarly | agot-jon-04 |
| Loving mother | 1 | Lady Tarly → Samwell Tarly | agot-jon-04 |
| Displaced heir | 1 | Samwell Tarly → Dickon Tarly | agot-jon-04 |
| Bannerman | 1 | House Tarly → House Tyrell | agot-jon-04 |
| Estranged/excluded | 1 | Jon Snow → Catelyn Stark | agot-jon-04 |
| Longing for connection | 1 | Jon Snow → Benjen Stark | agot-jon-04 |
| Hostility / gatekeeping | 1 | Chett → Jon Snow | agot-jon-05 |
| Gratitude / remembrance | 1 | Jon Snow → Maester Luwin | agot-jon-05 |
| Longing / sadness | 1 | Jon Snow → His unknown mother | agot-jon-05 |
| Bond / companionship | 1 | Ghost → Jon Snow | agot-jon-05 |
| Acceptance of | 1 | Ghost → Samwell Tarly | agot-jon-05 |
| Welcoming / formal hospitality | 1 | Bowen Marsh → Jon Snow | agot-jon-05 |
| Failed to make warrior of | 1 | Lord Randyll Tarly → Samwell Tarly | agot-jon-05 |
| Antagonism/target of | 1 | Jon Snow → Ser Alliser Thorne | agot-jon-06 |
| Assigned to assist | 1 | Samwell Tarly → Maester Aemon | agot-jon-06 |
| Temporarily replaces | 1 | Ser Jaremy Rykker → Benjen Stark | agot-jon-06 |
| Keeps faith of | 1 | Jon Snow → The old gods | agot-jon-06 |
| Forsakes | 1 | Sam Tarly → The Seven (Faith) | agot-jon-06 |
| Self-identifies with | 1 | Jon Snow → Stark heritage / First Men | agot-jon-06 |
| Deference to | 1 | Bowen Marsh → Sacred weirwood grove | agot-jon-06 |
| Sent by / serves | 1 | Samwell Tarly → Maester Aemon | agot-jon-07 |
| Paternal authority over | 1 | Jeor Mormont → Jon Snow | agot-jon-07 |
| Disappointment toward | 1 | Jeor Mormont → Jorah Mormont | agot-jon-07 |
| Complicated rejection of | 1 | Jon Snow → Catelyn Stark | agot-jon-07 |
| Brotherhood with (recalled) | 1 | Jon Snow → Robb Stark | agot-jon-07 |
| Blame toward | 1 | Jon Snow → Catelyn Stark | agot-jon-07 |
| Observant veteran alongside | 1 | Dywen → Ser Jaremy Rykker | agot-jon-07 |
| Uncanny responsiveness to | 1 | Mormont's raven → The situation | agot-jon-07 |
| Accused of treason against | 1 | Eddard Stark → Joffrey Baratheon | agot-jon-07 |
| Liege/steward to | 1 | Jon Snow → Jeor Mormont | agot-jon-08 |
| Loyal but conflicted friend to | 1 | Samwell Tarly → Jon Snow | agot-jon-08 |
| Collaborated with | 1 | Halder → Pate (builder) | agot-jon-08 |
| Bought garnets for | 1 | Samwell Tarly → Jon Snow (Longclaw pommel) | agot-jon-08 |
| Ashamed of | 1 | Jeor Mormont → Jorah Mormont | agot-jon-08 |
| Returned Longclaw to | 1 | Mormont's sister → Jeor Mormont | agot-jon-08 |
| Internal conflict about | 1 | Jon Snow → Night's Watch vows | agot-jon-08 |
| Assisted | 1 | Rudge → Donal Noye | agot-jon-08 |
| Brotherhood/loyalty conflict | 1 | Jon Snow → Robb Stark | agot-jon-09 |
| Reluctant conflict | 1 | Jon Snow → Pyp, Grenn, Halder, Toad, Matthar | agot-jon-09 |
| Loyalty/protectiveness | 1 | Samwell Tarly → Jon Snow | agot-jon-09 |
| Moral reflection | 1 | Jon Snow → Maester Aemon | agot-jon-09 |
| Longing/guilt | 1 | Jon Snow → Bran Stark, Arya Stark | agot-jon-09 |
| Leadership in the rescue | 1 | Pyp → Jon's friend group | agot-jon-09 |
| Tactical authority | 1 | Halder → Jon's friend group | agot-jon-09 |
| Fellow ranger, shared unease with | 1 | Gared → Will | agot-prologue |
| Invokes / fights for | 1 | Ser Waymar Royce → Robert (the king) | agot-prologue |
| Caught / gave choice to | 1 | Mallister freeriders → Will | agot-prologue |
| Frustrated with / embarrassed by | 1 | Sansa → Arya | agot-sansa-01 |
| Performatively chivalrous toward | 1 | Joffrey → Sansa | agot-sansa-01 |
| Directs / controls | 1 | Cersei → Joffrey | agot-sansa-01 |
| Governs / teaches | 1 | Septa Mordane → Sansa and Arya | agot-sansa-01 |
| Playful / teasing toward | 1 | Renly Baratheon → Sansa | agot-sansa-01 |
| Teased by / teases | 1 | Renly Baratheon → Ser Barristan Selmy | agot-sansa-01 |
| Terrifies | 1 | Ser Ilyn Payne → Sansa | agot-sansa-01 |
| Wishes were different | 1 | Sansa → Arya | agot-sansa-01 |
| Indulgent toward | 1 | Eddard Stark → Arya | agot-sansa-01 |
| Redirected hatred toward | 1 | Sansa → Cersei | agot-sansa-02 |
| Awe/attraction toward | 1 | Sansa → Ser Loras Tyrell | agot-sansa-02 |
| Deep hatred toward | 1 | Sandor Clegane → Gregor Clegane | agot-sansa-02 |
| Burned/brutalized | 1 | Gregor Clegane → Sandor Clegane | agot-sansa-02 |
| Deliberately killed | 1 | Gregor Clegane → Young knight from the Vale | agot-sansa-02 |
| Silently furious at | 1 | Cersei → Robert | agot-sansa-02 |
| Diplomatically manages | 1 | Renly → Robert | agot-sansa-02 |
| Past romantic attachment to | 1 | Littlefinger → Catelyn Stark | agot-sansa-02 |
| Unsettling interest in | 1 | Littlefinger → Sansa | agot-sansa-02 |
| Covered up abuse by | 1 | Sandor's father → Gregor Clegane | agot-sansa-02 |
| Sons/grandsons/bastard of | 1 | Six Frey knights + Martyn Rivers → Walder Frey | agot-sansa-02 |
| Younger son of | 1 | Ser Robar Royce → Yohn Royce | agot-sansa-02 |
| Romantic idealization | 1 | Sansa Stark → Joffrey Baratheon | agot-sansa-03 |
| Antagonism/sibling rivalry | 1 | Sansa Stark → Arya Stark | agot-sansa-03 |
| Unsettling attention toward | 1 | Petyr Baelish → Sansa Stark | agot-sansa-03 |
| Conciliation toward | 1 | Arya Stark → Sansa/Ned | agot-sansa-03 |
| Confined by | 1 | Sansa Stark → Cersei Lannister | agot-sansa-04 |
| Distances herself from | 1 | Sansa Stark → Arya Stark | agot-sansa-04 |
| Fixated on | 1 | Petyr Baelish → Sansa Stark | agot-sansa-04 |
| Possesses | 1 | Varys → Eddard's seal | agot-sansa-04 |
| Previously informed on | 1 | Sansa Stark → Eddard Stark | agot-sansa-04 |
| Shunned by | 1 | Sansa Stark → Lords at court | agot-sansa-05 |
| Appointed to serve | 1 | Sandor Clegane → Joffrey Baratheon | agot-sansa-05 |
| Conditionally grants mercy to | 1 | Joffrey Baratheon → Eddard Stark | agot-sansa-05 |
| Questions | 1 | Littlefinger → Sansa Stark | agot-sansa-05 |
| Sets terms for | 1 | Cersei → Eddard Stark | agot-sansa-05 |
| Thinks of/worries about | 1 | Sansa Stark → Arya Stark | agot-sansa-05 |
| Dominates/abuses | 1 | Joffrey → Sansa | agot-sansa-06 |
| Sycophantic loyalty to | 1 | Janos Slynt → Joffrey | agot-sansa-06 |
| Recalls advice of | 1 | Sansa → Petyr Baelish | agot-sansa-06 |
| distaste/hostility toward | 1 | Cersei → Tyrion | agot-tyrion-01 |
| bodyguard, obedient | 1 | Sandor Clegane → Joffrey | agot-tyrion-01 |
| mocking/contemptuous toward | 1 | Sandor Clegane → Tyrion | agot-tyrion-01 |
| dismissive authority toward | 1 | Tyrion → Sandor Clegane | agot-tyrion-01 |
| cruel indifference toward | 1 | Joffrey → Bran Stark | agot-tyrion-01 |
| gentle concern toward | 1 | Tommen → Bran Stark | agot-tyrion-01 |
| concern toward | 1 | Myrcella → Bran Stark | agot-tyrion-01 |
| wary suspicion toward | 1 | Tyrion → Jaime and Cersei | agot-tyrion-01 |
| veiled threat toward | 1 | Jaime → Tyrion | agot-tyrion-01 |
| casual disregard toward | 1 | Jaime → Robert | agot-tyrion-01 |
| sympathy toward | 1 | Robert → Eddard Stark | agot-tyrion-01 |
| paternal kindness toward | 1 | Tyrion → Tommen and Myrcella | agot-tyrion-01 |
| Hostility / wariness toward | 1 | Ghost → Tyrion | agot-tyrion-02 |
| Disillusionment toward | 1 | Jon Snow → Night's Watch | agot-tyrion-02 |
| Distaste toward | 1 | Benjen Stark → Lannisters (as a family) | agot-tyrion-02 |
| appeals to / trusts | 1 | Mormont → Tyrion | agot-tyrion-03 |
| persecutes | 1 | Ser Alliser Thorne → Jon Snow | agot-tyrion-03 |
| privately doubts efficacy of | 1 | Tyrion → Robert, Tywin, Jaime | agot-tyrion-03 |
| tolerant of | 1 | Ghost → Tyrion | agot-tyrion-03 |
| forced into service | 1 | Tywin Lannister → Thorne, Rykker | agot-tyrion-03 |
| planning revenge against | 1 | Tyrion → Kurleket, Lharys, Mohor, Ser Willis Wode, Bronn, Chiggen, Marillion | agot-tyrion-04 |
| neutral toward | 1 | Yoren → Both parties | agot-tyrion-04 |
| boasts about (sexually) | 1 | Petyr Baelish → Catelyn Stark | agot-tyrion-04 |
| Torments/controls | 1 | Mord → Tyrion | agot-tyrion-05 |
| Bribes/manipulates | 1 | Tyrion → Mord | agot-tyrion-05 |
| Accuses publicly | 1 | Lysa Arryn → Tyrion | agot-tyrion-05 |
| Dependent on / protected by | 1 | Robert Arryn → Lysa Arryn | agot-tyrion-05 |
| Claims custody of | 1 | Catelyn Stark → Tyrion | agot-tyrion-05 |
| Ignores / overrides | 1 | Lysa Arryn → Catelyn Stark | agot-tyrion-05 |
| Served loyally | 1 | Ser Vardis Egen → Jon Arryn | agot-tyrion-05 |
| Named champion by | 1 | Ser Vardis Egen → Lysa Arryn | agot-tyrion-05 |
| Reluctant to fight | 1 | Ser Vardis Egen → Tyrion | agot-tyrion-05 |
| Champions | 1 | Bronn → Tyrion | agot-tyrion-05 |
| Carried | 1 | Bronn → Tyrion | agot-tyrion-05 |
| Wary interest in | 1 | Tyrion → Bronn | agot-tyrion-05 |
| Useful to | 1 | Marillion → Tyrion | agot-tyrion-05 |
| Eager to kill | 1 | Multiple Vale knights → Tyrion | agot-tyrion-05 |
| Son/heir of | 1 | Ser Albar Royce → Lord Nestor Royce | agot-tyrion-05 |
| Employer/patron of | 1 | Tyrion → Bronn | agot-tyrion-06 |
| Served then abandoned | 1 | Bronn → Catelyn Stark | agot-tyrion-06 |
| Paid debt to | 1 | Tyrion → Mord | agot-tyrion-06 |
| Cruelly punished | 1 | Tywin Lannister → Tyrion | agot-tyrion-06 |
| Arranged deception of | 1 | Jaime Lannister → Tyrion | agot-tyrion-06 |
| Son, treated with contempt | 1 | Tyrion → Tywin | agot-tyrion-07 |
| Uneasy leader/captive of | 1 | Tyrion → Clansmen (collectively) | agot-tyrion-07 |
| Father, dismissive of | 1 | Tywin → Tyrion | agot-tyrion-07 |
| Follows but threatens | 1 | Shagga → Tyrion | agot-tyrion-07 |
| Considers irrelevant | 1 | Tywin → Walder Frey | agot-tyrion-07 |
| Plans to deal with | 1 | Tywin → Stannis Baratheon | agot-tyrion-07 |
| Compares himself unfavorably to | 1 | Tyrion → Jaime | agot-tyrion-08 |
| Employs / relies on | 1 | Tyrion → Bronn | agot-tyrion-08 |
| Defers to / speaks for | 1 | Kevan → Tywin | agot-tyrion-08 |
| Assigned under | 1 | Tyrion → Gregor Clegane | agot-tyrion-08 |
| Strategically manipulates | 1 | Tywin → Tyrion | agot-tyrion-08 |
| Welcoming toward | 1 | Conn son of Coratt → Tyrion | agot-tyrion-08 |
| Master to | 1 | Tyrion → Podrick Payne | agot-tyrion-08 |
| Grudging reliance on | 1 | Tywin → Tyrion | agot-tyrion-09 |
| Values | 1 | Tywin → Jaime | agot-tyrion-09 |
| Condemns decisions of | 1 | Tywin → Joffrey | agot-tyrion-09 |
| Antagonized by, then dominates | 1 | Arya → Hot Pie | acok-arya-01 |
| Connected to unnamed messenger regarding | 1 | Yoren → Eddard Stark | acok-arya-01 |
| recalls teachings of | 1 | Arya → Syrio Forel | acok-arya-02 |
| rallies to defend | 1 | Hot Pie → Arya/the group | acok-arya-02 |
| rally to defend | 1 | Tarber, Cutjack, Kurz, Koss, Reysen, Dobber → Yoren's party | acok-arya-02 |
| wants to capture | 1 | Queen Cersei → Gendry | acok-arya-02 |
| rebuked by | 1 | Lommy → The Bull | acok-arya-02 |
| Shares food with / companionship | 1 | Arya → Gendry | acok-arya-03 |
| Wary companionship | 1 | Arya → Hot Pie | acok-arya-03 |
| Polite interaction with | 1 | Arya → Jaqen H'ghar | acok-arya-03 |
| Believes is father's only bastard | 1 | Arya → Jon | acok-arya-03 |
| Former apprentice to | 1 | Gendry → Master Mott | acok-arya-03 |
| Wanted by | 1 | Gendry → The queen (Cersei) | acok-arya-03 |
| Speculates about parentage of | 1 | Lommy → Gendry | acok-arya-03 |
| Protector / leader of | 1 | Yoren → Entire party | acok-arya-03 |
| Hunting partner of | 1 | Kurz → Koss | acok-arya-03 |
| Disciplinarian toward | 1 | Murch → Rorge, Biter | acok-arya-03 |
| Peacekeeper | 1 | Reysen → Hot Pie, Lommy | acok-arya-03 |
| Confides in | 1 | Hot Pie → Arya | acok-arya-03 |
| grudging comradeship | 1 | Arya → Hot Pie | acok-arya-04 |
| annoyance toward | 1 | Arya → Lommy | acok-arya-04 |
| remembers with fondness | 1 | Arya → Syrio Forel | acok-arya-04 |
| complicated choice toward | 1 | Arya → Jaqen H'ghar, Rorge, Biter | acok-arya-04 |
| pleading/manipulative toward | 1 | Jaqen H'ghar → Arya | acok-arya-04 |
| demanding toward | 1 | Rorge → Everyone | acok-arya-04 |
| loyal fighter | 1 | Dobber → Yoren | acok-arya-04 |
| Newly deferential toward | 1 | Gendry → Arya | acok-arya-05 |
| Advocates yielding | 1 | Lommy → Everyone | acok-arya-05 |
| Cherishes | 1 | Arya → Needle | acok-arya-05 |
| Clings to | 1 | Weasel → Arya | acok-arya-05 |
| stole Needle from | 1 | Polliver → Arya | acok-arya-06 |
| took horned helm from | 1 | Dunsen → Gendry | acok-arya-06 |
| supervises with | 1 | Goodwife Amabel → Goodwife Harra | acok-arya-06 |
| assigns Arya to | 1 | Goodwife Amabel → Weese | acok-arya-06 |
| understeward of | 1 | Weese → Wailing Tower | acok-arya-06 |
| accompanied by | 1 | Lord Beric Dondarrion → Red priest (unnamed) | acok-arya-06 |
| tries to help | 1 | Hot Pie → Arya | acok-arya-07 |
| brutal master to | 1 | Weese → Arya | acok-arya-07 |
| forced reconciliation with | 1 | Vargo Hoat → Ser Harys Swyft | acok-arya-07 |
| owes debt to | 1 | Jaqen H'ghar → Arya | acok-arya-07 |
| dispenses justice over | 1 | Lord Tywin → Lannister host | acok-arya-07 |
| Identifies with | 1 | Arya → Robb Stark | acok-arya-08 |
| Dominates / abuses | 1 | Weese → Arya | acok-arya-08 |
| Mutual hatred with | 1 | Vargo Hoat → Ser Amory Lorch | acok-arya-08 |
| coerces/manipulates | 1 | Arya → Jaqen H'ghar | acok-arya-09 |
| bound by oath to | 1 | Jaqen H'ghar → Arya | acok-arya-09 |
| gives gift/instruction to | 1 | Jaqen H'ghar → Arya | acok-arya-09 |
| switches allegiance to | 1 | Vargo Hoat → Roose Bolton | acok-arya-09 |
| supervised by | 1 | Arya → Pinkeye (Mebble) | acok-arya-09 |
| feels homesick for | 1 | Arya → Winterfell | acok-arya-09 |
| mentions as master | 1 | Gendry → Lucan | acok-arya-09 |
| long service to | 1 | Ben Blackthumb → Harrenhal (multiple lords) | acok-arya-09 |
| follows/trusts | 1 | Gendry → Arya | acok-arya-10 |
| pressure | 1 | Frey lords → Roose Bolton | acok-arya-10 |
| intimidates | 1 | Rorge → Arya | acok-arya-10 |
| will give Harrenhal to | 1 | Bolton → Vargo Hoat | acok-arya-10 |
| sends to destruction (inferred) | 1 | Bolton → Tallhart and Glover | acok-arya-10 |
| castellan appointed by | 1 | Ser Rodrik Cassel → Catelyn Stark | acok-bran-01 |
| storyteller to | 1 | Old Nan → Bran Stark | acok-bran-01 |
| pack bond with | 1 | Summer → Shaggydog | acok-bran-01 |
| feels displaced by | 1 | Bran Stark → The Walders taking Jon's room | acok-bran-01 |
| ward/dependent | 1 | Bran → Hodor | acok-bran-02 |
| bullies | 1 | Little Walder → Hodor | acok-bran-02 |
| vassal to | 1 | Lord Manderly → Robb Stark | acok-bran-02 |
| protective/advisory toward | 1 | Osha → Bran | acok-bran-02 |
| Acting lord / representative of | 1 | Bran → Robb Stark | acok-bran-03 |
| Defiant attachment to | 1 | Rickon → Catelyn Stark | acok-bran-03 |
| Servant/carrier of | 1 | Hodor → Bran | acok-bran-03 |
| Reluctant tolerance of | 1 | Bran → Little Walder and Big Walder | acok-bran-03 |
| Great friend to | 1 | Howland Reed → Lord Eddard Stark | acok-bran-03 |
| Sworn fealty to | 1 | Meera and Jojen → House Stark / Bran | acok-bran-03 |
| Generous guest to | 1 | Lord Wyman Manderly → Winterfell | acok-bran-03 |
| Supernatural awareness of | 1 | Jojen → Summer | acok-bran-03 |
| uneasy interaction | 1 | Bran → Jojen Reed | acok-bran-04 |
| mission toward | 1 | Jojen → Bran | acok-bran-04 |
| compares to Arya | 1 | Bran → Meera Reed | acok-bran-04 |
| pack bond | 1 | Summer → Shaggydog | acok-bran-04 |
| sent children to fulfill green dream | 1 | Howland Reed → Bran/Winterfell | acok-bran-04 |
| angry with | 1 | Ser Rodrik → Bolton's bastard / Lord Manderly | acok-bran-04 |
| seized/married | 1 | Bolton's bastard → Lady Hornwood | acok-bran-04 |
| took castle of | 1 | Lord Manderly → Lady Hornwood | acok-bran-04 |
| callous/ambitious | 1 | Big Walder Frey → Ser Stevron Frey | acok-bran-05 |
| denial about | 1 | Rickon Stark → Eddard Stark | acok-bran-05 |
| disturbed by | 1 | Bran → Both Walders | acok-bran-05 |
| fighting | 1 | Manderly knights → Dreadfort men | acok-bran-05 |
| may claim | 1 | Roose Bolton → Hornwood lands | acok-bran-05 |
| Claims wardship over | 1 | Theon → Bran, Rickon | acok-bran-06 |
| Yields to (under duress) | 1 | Bran → Theon | acok-bran-06 |
| Critical of (retrospective) | 1 | Maester Luwin → Theon | acok-bran-06 |
| Self-blaming | 1 | Maester Luwin → Himself | acok-bran-06 |
| Wants | 1 | Rickon → Catelyn Stark | acok-bran-06 |
| Foresaw this event | 1 | Jojen → The ironborn attack | acok-bran-06 |
| Overpowers | 1 | Osha → Stygg | acok-bran-06 |
| submits to | 1 | Shaggydog → Summer | acok-bran-07 |
| clings to / dependent on | 1 | Rickon → Hodor | acok-bran-07 |
| takes charge of | 1 | Osha → Rickon | acok-bran-07 |
| identifies as | 1 | Bran → Winterfell | acok-bran-07 |
| mercy toward | 1 | Osha → Maester Luwin | acok-bran-07 |
| recalls connection with | 1 | Bran → Jon Snow | acok-bran-07 |
| second son of | 1 | Ser Emmon Frey → Lord Walder Frey | acok-catelyn-01 |
| speaks for | 1 | Edmure Tully → Hoster Tully / Riverrun | acok-catelyn-01 |
| captain of guard for | 1 | Ser Robin Ryger → House Tully | acok-catelyn-01 |
| raids | 1 | Lord Beric Dondarrion → Lord Tywin's forces | acok-catelyn-01 |
| envoy/mother serving | 1 | Catelyn → Robb | acok-catelyn-02 |
| close with / shares confidences | 1 | Renly → Ser Loras Tyrell | acok-catelyn-02 |
| dismisses claim of | 1 | Renly → Stannis | acok-catelyn-02 |
| demands fealty from | 1 | Renly → Robb | acok-catelyn-02 |
| is guarded toward | 1 | Catelyn → Renly | acok-catelyn-02 |
| besieges | 1 | Stannis → Storm's End (Renly's garrison) | acok-catelyn-02 |
| Failed diplomatic effort | 1 | Catelyn → Stannis and Renly | acok-catelyn-03 |
| Reliance on / closeness with | 1 | Renly → Ser Loras | acok-catelyn-03 |
| Brought suspicions to | 1 | Stannis → Jon Arryn | acok-catelyn-03 |
| Anxiety for | 1 | Catelyn → Sansa, Arya | acok-catelyn-03 |
| Longing for / duty toward | 1 | Catelyn → Her dying father (unnamed) | acok-catelyn-03 |
| Second son / independence from | 1 | Ser Robar Royce → Bronze Yohn Royce | acok-catelyn-03 |
| Mockery of | 1 | Renly → Stannis's wife and daughter | acok-catelyn-03 |
| Daughter, worried | 1 | Catelyn → Hoster Tully | acok-catelyn-04 |
| Daughter, remembering | 1 | Catelyn → Lady Minisa Tully | acok-catelyn-04 |
| Obedient service (new) | 1 | Brienne → Catelyn | acok-catelyn-04 |
| Hostile / accusatory | 1 | Ser Emmon Cuy → Brienne | acok-catelyn-04 |
| Advisor, urges aggression | 1 | Lord Rowan → Renly | acok-catelyn-04 |
| Tactical advisor | 1 | Randyll Tarly → Renly | acok-catelyn-04 |
| Political envoy | 1 | Catelyn → Renly | acok-catelyn-04 |
| Suspects / blames | 1 | Catelyn → Cersei Lannister | acok-catelyn-04 |
| Accepts service of | 1 | Catelyn → Brienne | acok-catelyn-05 |
| Wants to kill | 1 | Brienne → Stannis | acok-catelyn-05 |
| Concerned for / authority over | 1 | Catelyn → Edmure | acok-catelyn-05 |
| Bristles at / defers to | 1 | Edmure → Catelyn | acok-catelyn-05 |
| Wishes for guidance from | 1 | Catelyn → Brynden Tully | acok-catelyn-05 |
| Confuses with Lysa / guilt toward | 1 | Lord Hoster → Catelyn (as Lysa) | acok-catelyn-05 |
| Harbors rage toward | 1 | Catelyn → Cersei Lannister | acok-catelyn-05 |
| Ambivalence toward | 1 | Catelyn → Jon Snow | acok-catelyn-05 |
| mother/worried | 1 | Catelyn → Robb | acok-catelyn-06 |
| dutiful daughter | 1 | Catelyn → Lord Hoster | acok-catelyn-06 |
| unrequited devotion to | 1 | Brienne → Renly | acok-catelyn-06 |
| interrogates/distrusts | 1 | Catelyn → Ser Cleos Frey | acok-catelyn-06 |
| dutiful marriage (past) | 1 | Catelyn → Ned Stark | acok-catelyn-06 |
| complex resentment | 1 | Catelyn → Jon Snow | acok-catelyn-06 |
| grudging acknowledgment | 1 | Catelyn → Tyrion Lannister | acok-catelyn-06 |
| cold indifference | 1 | Roose Bolton → Ramsay Bolton | acok-catelyn-06 |
| calculating obedience | 1 | Roose Bolton → Robb Stark | acok-catelyn-06 |
| military trust | 1 | Edmure → Lord Jason Mallister | acok-catelyn-06 |
| awed memory of | 1 | Brienne → A singer from across the narrow sea | acok-catelyn-06 |
| loyalty/enthusiasm | 1 | Ser Desmond → Edmure | acok-catelyn-06 |
| sworn lady to | 1 | Catelyn → Brienne | acok-catelyn-07 |
| attempted killer of | 1 | Jaime → Bran Stark | acok-catelyn-07 |
| served under | 1 | Jaime → Gerold Hightower | acok-catelyn-07 |
| rival/enemy of | 1 | Jaime → Robb Stark | acok-catelyn-07 |
| betrayer of | 1 | Theon Greyjoy → Stark family | acok-catelyn-07 |
| king/lord of | 1 | Robb → Rickard Karstark's loyalty | acok-catelyn-07 |
| Named first of Queensguard | 1 | Daenerys → Ser Jorah | acok-daenerys-01 |
| Fled justice of | 1 | Ser Jorah → Eddard Stark | acok-daenerys-01 |
| Won tourney, defeated | 1 | Ser Jorah → Jaime Lannister | acok-daenerys-01 |
| Chief concubine to | 1 | Lynesse Hightower → Tregar Ormollen | acok-daenerys-01 |
| Grateful to / remembers | 1 | Daenerys → Doreah | acok-daenerys-01 |
| Took the black | 1 | Jorah's father → Night's Watch | acok-daenerys-01 |
| Hosts | 1 | Xaro Xhoan Daxos → Daenerys | acok-daenerys-02 |
| Courts/seeks to influence | 1 | Pyat Pree → Daenerys | acok-daenerys-02 |
| Views as enemy (dead) | 1 | Daenerys → Robert Baratheon | acok-daenerys-02 |
| Views as traitor | 1 | Daenerys → Eddard Stark | acok-daenerys-02 |
| Scorns/pities | 1 | Daenerys → Viserys | acok-daenerys-02 |
| Compares Dany favorably to | 1 | Ser Jorah → Rhaegar | acok-daenerys-02 |
| Awed by | 1 | Quhuru Mo → Daenerys / Dragons | acok-daenerys-02 |
| Call Qartheen | 1 | Dothraki → "Milk Men" | acok-daenerys-02 |
| Views Jorah as having dual perception of her | 1 | Daenerys → Ser Jorah | acok-daenerys-02 |
| courts/uses | 1 | Xaro Xhoan Daxos → Daenerys | acok-daenerys-03 |
| sold/arranged marriage of | 1 | Illyrio Mopatis → Daenerys | acok-daenerys-03 |
| Protective advisor | 1 | Ser Jorah → Daenerys | acok-daenerys-04 |
| Patron/suitor | 1 | Xaro Xhoan Daxos → Daenerys | acok-daenerys-04 |
| Guide then antagonist | 1 | Pyat Pree → Daenerys | acok-daenerys-04 |
| Memory/longing | 1 | Daenerys → House with the red door | acok-daenerys-04 |
| Predatory/parasitic | 1 | The Undying → Daenerys | acok-daenerys-04 |
| Deceptive | 1 | Illusory wizards → Daenerys | acok-daenerys-04 |
| advised by/protected by | 1 | Daenerys → Ser Jorah | acok-daenerys-05 |
| refuses/distrusts | 1 | Daenerys → Xaro Xhoan Daxos | acok-daenerys-05 |
| expelled/rejected | 1 | Xaro Xhoan Daxos → Daenerys | acok-daenerys-05 |
| recognizes | 1 | Arstan Whitebeard → Ser Jorah | acok-daenerys-05 |
| named to | 1 | Ser Jorah → Queensguard | acok-daenerys-05 |
| squired by | 1 | Strong Belwas → Arstan Whitebeard | acok-daenerys-05 |
| attempted assassination | 1 | Sorrowful Men → Daenerys | acok-daenerys-05 |
| Loyal vassal of | 1 | Davos → Stannis Baratheon | acok-davos-01 |
| Old acquaintance of | 1 | Davos → Salladhor Saan | acok-davos-01 |
| Raised to knighthood | 1 | Stannis → Davos | acok-davos-01 |
| Uses / relies on | 1 | Stannis → Melisandre | acok-davos-01 |
| Devout follower of | 1 | Queen Selyse → Melisandre / R'hllor | acok-davos-01 |
| Skeptic toward | 1 | Salladhor Saan → Stannis / Lightbringer | acok-davos-01 |
| Priestess serving | 1 | Melisandre → Stannis | acok-davos-01 |
| Opposed by (privately) | 1 | Melisandre → Davos | acok-davos-01 |
| Ancestor provided brides to | 1 | Lord Velaryon → Targaryen princes | acok-davos-01 |
| Scorns | 1 | Allard → The burning of the Seven | acok-davos-01 |
| Withdrew support from | 1 | Guncer Sunglass → Stannis | acok-davos-01 |
| Defended the sept against | 1 | Ser Hubard Rambton → The queen's men | acok-davos-01 |
| Declared for | 1 | House Florent → Renly | acok-davos-01 |
| Depends on / follows visions of | 1 | Stannis → Melisandre | acok-davos-02 |
| Grudging dependence on | 1 | Stannis → His bannermen lords | acok-davos-02 |
| Foremost supporter of | 1 | Lord Alester Florent → Stannis | acok-davos-02 |
| Kinsman of | 1 | Lord Alester Florent → Edric Storm | acok-davos-02 |
| Knew from childhood | 1 | Penrose → Brienne | acok-davos-02 |
| Lieutenant to | 1 | Lord Meadows → Ser Cortnay Penrose | acok-davos-02 |
| Suspects treachery from | 1 | Stannis → Cersei Lannister | acok-davos-02 |
| Displeased with | 1 | Salladhor Saan → Ser Imry / Stannis | acok-davos-03 |
| Eager for glory | 1 | Allard → (self) | acok-davos-03 |
| Loyalty/conflicted bond to | 1 | Jon Snow → Robb Stark | acok-jon-01 |
| Chose vows over | 1 | Maester Aemon → The Iron Throne | acok-jon-01 |
| Father who made Sam unsafe | 1 | Sam's father (Randyll Tarly) → Samwell Tarly | acok-jon-01 |
| Remembers/dreams of | 1 | Jon Snow → Othor (wight) | acok-jon-01 |
| Unspoken pact | 1 | Night's Watch → Members | acok-jon-01 |
| Steward/serves | 1 | Jon Snow → Jeor Mormont | acok-jon-02 |
| Growing confidence | 1 | Samwell Tarly → Self | acok-jon-02 |
| Companionable pessimism | 1 | Dolorous Edd → Jon Snow | acok-jon-02 |
| Unease about | 1 | Dywen → The forest | acok-jon-02 |
| Steward/squire serving | 1 | Jon Snow → Lord Commander Mormont | acok-jon-03 |
| Mockery from | 1 | Jon Snow → Lark the Sisterman | acok-jon-03 |
| Moral connection to | 1 | Jon Snow → Ned Stark | acok-jon-03 |
| Pragmatic tolerance of | 1 | Mormont → Craster | acok-jon-03 |
| Domination over | 1 | Craster → His wives/daughters | acok-jon-03 |
| Hostility/contempt toward | 1 | Craster → Night's Watch | acok-jon-03 |
| Desperate appeal to | 1 | Gilly → Jon Snow | acok-jon-03 |
| Sympathy/intervention for | 1 | Sam Tarly → Gilly | acok-jon-03 |
| Vouches for | 1 | Thoren Smallwood → Craster | acok-jon-03 |
| Former assignment to | 1 | Chett → Maester Aemon | acok-jon-03 |
| Dismissive/adversarial toward | 1 | Thoren Smallwood → Jon Snow | acok-jon-04 |
| Gives food to / looks after | 1 | Jon Snow → Grenn | acok-jon-04 |
| Recognizes lineage of | 1 | Qhorin Halfhand → Jon Snow | acok-jon-05 |
| Chose for mission | 1 | Qhorin Halfhand → Jon Snow | acok-jon-05 |
| Trusted advisor to | 1 | Qhorin Halfhand → Jeor Mormont | acok-jon-05 |
| Comrade to | 1 | Jon Snow → Dolorous Edd | acok-jon-05 |
| Hopes for return of | 1 | Jon Snow → Benjen Stark | acok-jon-05 |
| Disloyal toward | 1 | Chett → Jeor Mormont | acok-jon-05 |
| Aggressive/confident attitude toward | 1 | Thoren Smallwood → Wildlings | acok-jon-05 |
| Cautious toward | 1 | Jarman Buckwell → Wildling leaders | acok-jon-05 |
| Fellow ranger / climbing partner | 1 | Jon Snow → Stonesnake | acok-jon-06 |
| Thinks of / association | 1 | Jon Snow → Arya Stark | acok-jon-06 |
| Feared / recognized by | 1 | Qhorin Halfhand → Ygritte | acok-jon-06 |
| Supports Qhorin's position on | 1 | Squire Dalbridge → Ygritte | acok-jon-06 |
| Supports execution of | 1 | Ebben → Ygritte | acok-jon-06 |
| Offers defection to | 1 | Ygritte → Jon Snow | acok-jon-06 |
| Disobeys | 1 | Jon Snow → Qhorin Halfhand | acok-jon-06 |
| Connected to (dream communication) | 1 | Jon Snow → Bran (implied brother) | acok-jon-07 |
| Felt kinship/empathy toward | 1 | Jon Snow → Ygritte | acok-jon-07 |
| Aggressive/impatient temperament | 1 | Ebben → (general) | acok-jon-07 |
| Deserted from | 1 | Mance Rayder → Night's Watch | acok-jon-07 |
| Advocates for/protects | 1 | Ygritte → Jon Snow | acok-jon-08 |
| Previously spared | 1 | Jon Snow → Ygritte | acok-jon-08 |
| Rival/antagonistic toward | 1 | Rattleshirt → Qhorin Halfhand | acok-jon-08 |
| Brotherhood/fraternity with | 1 | Qhorin Halfhand → Jon Snow | acok-jon-08 |
| Democratic/free | 1 | Wildlings (group) → Each other | acok-jon-08 |
| protective compassion | 1 | Cressen → Shireen | acok-prologue |
| cold dismissal | 1 | Stannis → Cressen | acok-prologue |
| devoted attachment | 1 | Shireen → Patchface | acok-prologue |
| dismissive superiority | 1 | Melisandre → Cressen | acok-prologue |
| drowned with | 1 | Lord Steffon → Lady Baratheon (wife) | acok-prologue |
| bond | 1 | Patchface → Shireen | acok-prologue |
| Prefers among captors | 1 | Sansa → Ser Arys Oakheart | acok-sansa-01 |
| Complex regard for | 1 | Sansa → Sandor Clegane | acok-sansa-01 |
| Saves life of | 1 | Sansa → Ser Dontos | acok-sansa-01 |
| Mocking toward | 1 | Joffrey → Tommen | acok-sansa-01 |
| Dismissive toward | 1 | Joffrey → Tyrion | acok-sansa-01 |
| Excited to see | 1 | Tommen → Tyrion | acok-sansa-01 |
| Unwilling captives of | 1 | Redwyne twins → The Crown / Cersei | acok-sansa-01 |
| beaten by (on Joffrey's orders) | 1 | Sansa Stark → Ser Meryn Trant | acok-sansa-02 |
| surveilled by | 1 | Sansa Stark → Cersei Lannister | acok-sansa-02 |
| led sortie against | 1 | Joffrey Baratheon → Smallfolk mob | acok-sansa-02 |
| sent to the Wall | 1 | Tyrion Lannister → Janos Slynt | acok-sansa-02 |
| abuses/dominates | 1 | Joffrey → Sansa | acok-sansa-03 |
| secretly protects | 1 | Ser Dontos → Sansa | acok-sansa-03 |
| claims credit for | 1 | Joffrey → Eddard Stark's death | acok-sansa-03 |
| dismisses/mocks | 1 | Tyrion → Lancel Lannister | acok-sansa-03 |
| relies on for escape | 1 | Sansa → Dontos | acok-sansa-04 |
| protective/confrontational toward | 1 | Sandor Clegane → Sansa | acok-sansa-04 |
| close bond with | 1 | Cersei → Jaime Lannister | acok-sansa-04 |
| has unnamed friend aiding | 1 | Dontos → Sansa | acok-sansa-04 |
| shames | 1 | Joffrey → Sansa | acok-sansa-04 |
| was shamed by | 1 | Joffrey → Arya Stark | acok-sansa-04 |
| Hostage/captive of | 1 | Sansa → Joffrey / House Lannister | acok-sansa-05 |
| Gratitude toward / prayer for | 1 | Sansa → Sandor Clegane | acok-sansa-05 |
| Possessive cruelty toward | 1 | Joffrey → Sansa | acok-sansa-05 |
| Use of | 1 | Cersei → Ser Ilyn Payne | acok-sansa-05 |
| Shame about | 1 | Lady Tanda → Lollys | acok-sansa-05 |
| Rides with | 1 | Ser Mandon Moore → Tyrion | acok-sansa-05 |
| Secretly trusts | 1 | Sansa → Ser Dontos | acok-sansa-06 |
| Has replaced | 1 | Ser Osmund Kettleblack → Sandor Clegane | acok-sansa-06 |
| Mother, protective authority over | 1 | Cersei → Joffrey | acok-sansa-07 |
| Dismissive contempt toward | 1 | Cersei → Lancel | acok-sansa-07 |
| Compassion despite enmity toward | 1 | Sansa → Lancel | acok-sansa-07 |
| Protective obsession toward | 1 | Sandor → Sansa | acok-sansa-07 |
| Self-loathing, despair | 1 | Sandor → (self) | acok-sansa-07 |
| Low estimation of | 1 | Sansa → Ser Dontos | acok-sansa-07 |
| Orders obedience from | 1 | Cersei → Osfryd Kettleblack | acok-sansa-07 |
| Brief, hopeful longing for | 1 | Sansa → Robb Stark | acok-sansa-07 |
| Agrees to marry | 1 | Joffrey → Margaery Tyrell | acok-sansa-08 |
| Mother/protector of | 1 | Cersei → Joffrey | acok-sansa-08 |
| Calls her "Jonquil" | 1 | Dontos → Sansa | acok-sansa-08 |
| Granted lordship by | 1 | Petyr Baelish → Joffrey/Crown | acok-sansa-08 |
| Whispering to | 1 | Varys → Petyr Baelish | acok-sansa-08 |
| Hostage of | 1 | Sansa → Cersei/Crown | acok-sansa-08 |
| Political marriage to | 1 | Tyrell alliance → Lannister/Crown | acok-sansa-08 |
| Leers at | 1 | Osmund Kettleblack → Sansa | acok-sansa-08 |
| Son returning to | 1 | Theon Greyjoy → Balon Greyjoy | acok-theon-01 |
| Disappointed in / suspicious of | 1 | Balon Greyjoy → Theon Greyjoy | acok-theon-01 |
| Favorable comparison to Theon | 1 | Balon Greyjoy → Asha Greyjoy | acok-theon-01 |
| Former ward/hostage of | 1 | Theon Greyjoy → Eddard Stark | acok-theon-01 |
| Devoted priest of | 1 | Aeron Greyjoy → Drowned God | acok-theon-01 |
| Slayer of | 1 | Jason Mallister → Rodrik Greyjoy | acok-theon-01 |
| Distant and suspicious toward | 1 | Catelyn Stark → Theon Greyjoy | acok-theon-01 |
| Vowed to outlive | 1 | Balon Greyjoy → Robert Baratheon & Eddard Stark | acok-theon-01 |
| Servant/steward of | 1 | Helya → Balon Greyjoy | acok-theon-01 |
| Loyal retainer of | 1 | Dagmer Cleftjaw → Balon Greyjoy | acok-theon-01 |
| Son (seeking approval) | 1 | Theon → Balon | acok-theon-02 |
| Favored child | 1 | Asha → Balon | acok-theon-02 |
| Stranger to ironborn | 1 | Theon → Ironborn generally | acok-theon-02 |
| Master / somewhat fond | 1 | Theon → Wex | acok-theon-02 |
| Tricks / tests | 1 | Asha → Theon | acok-theon-02 |
| Mother (absent, ill) | 1 | Lady Greyjoy → Theon | acok-theon-02 |
| Squire / baseborn | 1 | Wex → Lord Botley | acok-theon-02 |
| Former ward | 1 | Theon → Eddard Stark | acok-theon-02 |
| conflicted former friend | 1 | Theon Greyjoy → Benfred Tallhart | acok-theon-03 |
| son seeking approval | 1 | Theon Greyjoy → Balon Greyjoy | acok-theon-03 |
| sibling rivalry | 1 | Theon Greyjoy → Asha Greyjoy | acok-theon-03 |
| conflicted former ward | 1 | Theon Greyjoy → Eddard Stark | acok-theon-03 |
| sworn man / loyal servant | 1 | Dagmer Cleftjaw → Balon Greyjoy | acok-theon-03 |
| priest / authority over the men | 1 | Aeron Damphair → Ironborn warriors | acok-theon-03 |
| obedient to Theon after Todric's death | 1 | Old Botley (Fishwhiskers) → Theon Greyjoy | acok-theon-03 |
| reliance / favoritism | 1 | Balon Greyjoy → Asha Greyjoy | acok-theon-03 |
| threatened by/suspicious of | 1 | Theon → Reek | acok-theon-04 |
| coerces | 1 | Theon → Farlen | acok-theon-04 |
| former servant of | 1 | Reek → Lord Bolton | acok-theon-04 |
| mocked by | 1 | Walder Frey → Walder Frey (cousin) | acok-theon-04 |
| betrayed/oath-broke | 1 | Osha → Theon | acok-theon-04 |
| models self after | 1 | Theon → Eddard Stark | acok-theon-04 |
| sibling rivalry / mutual contempt | 1 | Theon → Asha | acok-theon-05 |
| lord / dependent | 1 | Theon → Reek | acok-theon-05 |
| sexual violence toward | 1 | Theon → Kyra | acok-theon-05 |
| claims vengeance for | 1 | Theon → Rodrik and Maron Greyjoy | acok-theon-05 |
| overlord / guards | 1 | Theon → Urzen, Kromm | acok-theon-05 |
| conflicted identity | 1 | Theon → Stark household / Greyjoy heritage | acok-theon-05 |
| Forsaken by father | 1 | Theon → Balon Greyjoy | acok-theon-06 |
| Dependent on / antagonistic toward | 1 | Theon → Maester Luwin | acok-theon-06 |
| Former teacher of | 1 | Maester Luwin → Theon | acok-theon-06 |
| Former trainer of | 1 | Ser Rodrik → Theon | acok-theon-06 |
| Dutiful to | 1 | Ser Rodrik → Catelyn Stark / House Stark | acok-theon-06 |
| Hostage (as child) | 1 | Theon → Eddard Stark | acok-theon-06 |
| Deceived | 1 | Ramsay → Theon | acok-theon-06 |
| Master of (the original) | 1 | Ramsay → Reek | acok-theon-06 |
| Used as decoy | 1 | Ramsay → Reek (original) | acok-theon-06 |
| Rode beside in battle | 1 | Theon → Robb Stark | acok-theon-06 |
| Recalls saving | 1 | Theon → Bran Stark | acok-theon-06 |
| Employer / protected by | 1 | Tyrion → Bronn | acok-tyrion-01 |
| Suspicious, plans to confront | 1 | Tyrion → Littlefinger | acok-tyrion-01 |
| Desires his rescue above all | 1 | Cersei → Jaime | acok-tyrion-01 |
| Regent — frustrated by his defiance | 1 | Cersei → Joffrey | acok-tyrion-01 |
| Orchestrated his death | 1 | Cersei → Robert Baratheon | acok-tyrion-01 |
| Uses / distrusts | 1 | Cersei → Small council members | acok-tyrion-01 |
| Elevated by | 1 | Janos Slynt → Littlefinger | acok-tyrion-01 |
| Informed on / betrayed | 1 | Sansa Stark → Eddard Stark | acok-tyrion-01 |
| Wary of, assesses as dangerous | 1 | Tyrion → Ser Mandon Moore | acok-tyrion-01 |
| acts as Hand/authority over | 1 | Tyrion → Janos Slynt | acok-tyrion-02 |
| appoints | 1 | Tyrion → Ser Jacelyn Bywater | acok-tyrion-02 |
| grateful to/serves | 1 | Ser Jacelyn Bywater → Tyrion | acok-tyrion-02 |
| sellsword loyalty to | 1 | Bronn → Tyrion | acok-tyrion-02 |
| clansman serving | 1 | Timett → Tyrion | acok-tyrion-02 |
| suspects is controlled by Varys | 1 | Tyrion → Ser Jacelyn Bywater | acok-tyrion-02 |
| restive/wants more from | 1 | Shae → Tyrion | acok-tyrion-02 |
| Politically manages / outmaneuvers | 1 | Tyrion → Cersei | acok-tyrion-03 |
| Is served by (squire) | 1 | Tyrion → Podrick Payne | acok-tyrion-03 |
| Reserves special warmth for | 1 | Cersei → Jaime | acok-tyrion-03 |
| Strategically aligned with / useful to | 1 | Littlefinger → Tyrion | acok-tyrion-03 |
| Ingratiates himself with | 1 | Littlefinger → Cersei | acok-tyrion-03 |
| Grateful to / cooperates with | 1 | Chataya → Tyrion | acok-tyrion-03 |
| Covertly assists | 1 | Varys → Tyrion | acok-tyrion-03 |
| Seeking attention of | 1 | Lady Tanda → Tyrion | acok-tyrion-03 |
| Political rivalry with | 1 | Tyrion → Cersei | acok-tyrion-04 |
| Employs / trusts | 1 | Tyrion → Bronn | acok-tyrion-04 |
| Courts / pursues | 1 | Lady Tanda → Tyrion | acok-tyrion-04 |
| Formerly fostered with | 1 | Littlefinger → Tully family (Catelyn, Lysa, Hoster) | acok-tyrion-04 |
| Knows about / taunts with | 1 | Littlefinger → The Valyrian steel dagger | acok-tyrion-04 |
| Patronized / elevated | 1 | Jon Arryn → Littlefinger | acok-tyrion-04 |
| Armed | 1 | Tyrion → Mountain clansmen | acok-tyrion-04 |
| Assesses fighters | 1 | Bronn → Tallad | acok-tyrion-04 |
| acting Hand of the King to | 1 | Tyrion → Joffrey | acok-tyrion-05 |
| political rival / antagonistic sibling | 1 | Tyrion → Cersei | acok-tyrion-05 |
| patron / superior to | 1 | Tyrion → Hallyne the Pyromancer | acok-tyrion-05 |
| fiercely protective mother to | 1 | Cersei → Myrcella | acok-tyrion-05 |
| compares self unfavorably to men | 1 | Cersei → (general) | acok-tyrion-05 |
| deploys as Myrcella's shield | 1 | Tyrion → Ser Arys Oakheart | acok-tyrion-05 |
| sues for peace with | 1 | Robb Stark → Tyrion / Lannisters | acok-tyrion-05 |
| drives peace effort over | 1 | Lady Catelyn → Robb Stark | acok-tyrion-05 |
| formerly supplanted by | 1 | Hallyne → Maesters of the Citadel | acok-tyrion-05 |
| sibling rivalry / political adversary | 1 | Tyrion → Cersei | acok-tyrion-06 |
| political manipulation | 1 | Tyrion → Varys | acok-tyrion-06 |
| mutual distrust | 1 | Tyrion → Littlefinger | acok-tyrion-06 |
| exposes and arrests | 1 | Tyrion → Pycelle | acok-tyrion-06 |
| has been spying for | 1 | Pycelle → Cersei | acok-tyrion-06 |
| lifelong loyalty (self-claimed) | 1 | Pycelle → House Lannister / Tywin | acok-tyrion-06 |
| allowed to die | 1 | Pycelle → Jon Arryn | acok-tyrion-06 |
| frustrated hostility toward | 1 | Ser Alliser → Tyrion | acok-tyrion-06 |
| longing / fondness | 1 | Tyrion → Shae | acok-tyrion-06 |
| nostalgic memory of | 1 | Tyrion → Jon Snow | acok-tyrion-06 |
| obstructionist toward | 1 | Pycelle → Tyrion | acok-tyrion-06 |
| political rival | 1 | Tyrion → Cersei | acok-tyrion-07 |
| complicit in murder of | 1 | Lancel → Robert Baratheon | acok-tyrion-07 |
| employs | 1 | Tyrion → Bronn | acok-tyrion-07 |
| uses as cover | 1 | Tyrion → Alayaya | acok-tyrion-07 |
| relies on intelligence from | 1 | Tyrion → Varys | acok-tyrion-07 |
| arrested | 1 | Tyrion → Pycelle | acok-tyrion-07 |
| instructed | 1 | Tywin → Lancel | acok-tyrion-07 |
| proprietor / host | 1 | Chataya → Tyrion | acok-tyrion-07 |
| competing with | 1 | Dancy → Marei | acok-tyrion-07 |
| learning from | 1 | Alayaya → Marei | acok-tyrion-07 |
| twin of | 1 | Jaime → Cersei | acok-tyrion-07 |
| Sibling rivalry, mutual suspicion | 1 | Tyrion → Cersei | acok-tyrion-08 |
| Acting Hand, authority over | 1 | Tyrion → Joffrey | acok-tyrion-08 |
| Compares Tyrion to (favorably in words, unfavorably implied) | 1 | Cersei → Jaime | acok-tyrion-08 |
| Self-interested maneuvering toward | 1 | Littlefinger → The Crown | acok-tyrion-08 |
| Favors above other sons | 1 | Mace Tyrell → Loras Tyrell | acok-tyrion-08 |
| Oldest friend of | 1 | Paxter Redwyne → Mace Tyrell | acok-tyrion-08 |
| Employs, relies on | 1 | Tyrion → Bronn | acok-tyrion-08 |
| Uses for intelligence | 1 | Tyrion → Varys | acok-tyrion-08 |
| Bodyguard to | 1 | Sandor Clegane → Joffrey | acok-tyrion-08 |
| Childhood memory involving | 1 | Tyrion → Jaime and Cersei | acok-tyrion-08 |
| Submitted to | 1 | Lord Alester Florent → Stannis Baratheon | acok-tyrion-08 |
| Pragmatic protector of | 1 | Tyrion → Sansa Stark | acok-tyrion-09 |
| Employer/wary trust of | 1 | Tyrion → Bronn | acok-tyrion-09 |
| Informed by | 1 | Tyrion → Lancel Lannister | acok-tyrion-09 |
| Charming/manipulating | 1 | Cersei → Lancel Lannister | acok-tyrion-09 |
| Secretly employing | 1 | Cersei → Ser Osmund Kettleblack | acok-tyrion-09 |
| Cruel to | 1 | Joffrey → Tommen | acok-tyrion-09 |
| Prioritizes king over | 1 | Ser Mandon Moore → Sansa Stark | acok-tyrion-09 |
| Insolent toward | 1 | Bronn → Tyrion | acok-tyrion-09 |
| Desperate for | 1 | Lady Tanda → Lollys | acok-tyrion-09 |
| Ambitious | 1 | Bronn → (general) | acok-tyrion-10 |
| Threat to | 1 | Symon Silver Tongue → Tyrion | acok-tyrion-10 |
| pragmatic loyalty to | 1 | Bronn → Tyrion | acok-tyrion-11 |
| spying on via | 1 | Tyrion → Cersei through Ser Osmund Kettleblack | acok-tyrion-11 |
| political patron of | 1 | Tyrion → High Septon (new) | acok-tyrion-11 |
| hedging allegiance | 1 | House Swann → Multiple kings | acok-tyrion-11 |
| nostalgic ambivalence toward | 1 | Tyrion → Winterfell / the Starks | acok-tyrion-11 |
| Sibling rivalry / mutual antagonism | 1 | Tyrion → Cersei | acok-tyrion-12 |
| Emulates / seeks to channel | 1 | Tyrion → Tywin Lannister | acok-tyrion-12 |
| Suspected of double-dealing by | 1 | Varys → Cersei | acok-tyrion-12 |
| Attendant to | 1 | Shae → Lollys Stokeworth | acok-tyrion-12 |
| Uses as leverage | 1 | Tyrion → Tommen | acok-tyrion-12 |
| Confronts / overrides | 1 | Tyrion → Sandor Clegane | acok-tyrion-13 |
| Relies on (grudgingly) | 1 | Tyrion → Ser Mandon Moore | acok-tyrion-13 |
| Compares Stannis to | 1 | Tyrion → Lord Tywin | acok-tyrion-13 |
| Contrasted with | 1 | Stannis → Robert Baratheon | acok-tyrion-13 |
| Assessed (previously) | 1 | Jaime → Ser Mandon Moore | acok-tyrion-13 |
| Lord to squire (protective) | 1 | Tyrion → Podrick Payne | acok-tyrion-14 |
| Loyal squire, willing to die for lord | 1 | Podrick Payne → Tyrion | acok-tyrion-14 |
| Attempts to assassinate | 1 | Ser Mandon Moore → Tyrion | acok-tyrion-14 |
| Observes with understanding | 1 | Tyrion → Sandor Clegane | acok-tyrion-14 |
| Fellow Kingsguard | 1 | Ser Balon Swann → Ser Mandon Moore | acok-tyrion-14 |
| Fight back to back | 1 | Ser Balon Swann, Ser Mandon Moore → Each other | acok-tyrion-14 |
| suspects attempted assassination by (via proxy) | 1 | Tyrion → Ser Mandon Moore | acok-tyrion-15 |
| gratitude and trust toward | 1 | Tyrion → Podrick Payne | acok-tyrion-15 |
| longing / desire for | 1 | Tyrion → Shae | acok-tyrion-15 |
| complex resentment and desire for approval from | 1 | Tyrion → Tywin | acok-tyrion-15 |
| has displaced | 1 | Tywin → Tyrion | acok-tyrion-15 |
| recalls assessment by | 1 | Tyrion → Jaime (about Ser Mandon) | acok-tyrion-15 |
| conceals identity from | 1 | Arya → Hot Pie | asos-arya-01 |
| received gift/teaching from | 1 | Arya → Jaqen H'ghar | asos-arya-01 |
| identifies as daughter of | 1 | Arya → Ned Stark | asos-arya-01 |
| stubborn determination | 1 | Gendry → — | asos-arya-01 |
| has kill list including | 1 | Arya → Ser Gregor, Dunsen, Polliver, Raff the Sweetling, The Tickler, The Hound, Ser Ilyn, Ser Meryn, King Joffrey, Queen Cersei | asos-arya-01 |
| speaks in unison with | 1 | Gendry → Arya | asos-arya-01 |
| adversarial, then submitted | 1 | Arya → Lem Lemoncloak | asos-arya-02 |
| married to / dominates | 1 | Sharna → Husband | asos-arya-02 |
| innkeeper for | 1 | Sharna → Tom, Lem, Anguy | asos-arya-02 |
| employed by / married to | 1 | Husband → Sharna | asos-arya-02 |
| adopted by / works for | 1 | Serving boy / orphan → Sharna and Husband | asos-arya-02 |
| loyal retainer / recognizes | 1 | Harwin → Arya Stark | asos-arya-02 |
| surprising talent | 1 | Hot Pie → Tom Sevenstrings | asos-arya-02 |
| former cupbearer to | 1 | Arya → Roose Bolton | asos-arya-02 |
| Only true friend | 1 | Arya → Gendry | asos-arya-03 |
| Emotional bond, guarded trust | 1 | Arya → Harwin | asos-arya-03 |
| Paternal protectiveness toward | 1 | Harwin → Arya | asos-arya-03 |
| Former loyalty to | 1 | Harwin → Eddard Stark | asos-arya-03 |
| Leader of the party | 1 | Greenbeard → Lem, Tom, Anguy, Jack-Be-Lucky, Harwin | asos-arya-03 |
| Healer / spiritual support to | 1 | Thoros → Beric Dondarrion | asos-arya-03 |
| Former bond with | 1 | Arya → Nymeria | asos-arya-03 |
| Kill-list enmity toward | 1 | Arya → Ser Gregor, Dunsen, Polliver, Raff the Sweetling, the Tickler, the Hound, Ser Ilyn, Ser Meryn, Cersei, Joffrey | asos-arya-03 |
| Compares to / identifies with | 1 | Harwin → Lyanna Stark / Arya | asos-arya-03 |
| Orchestrated trap against | 1 | Tywin Lannister → Eddard Stark | asos-arya-03 |
| Ambushed | 1 | Gregor Clegane → Beric Dondarrion's force | asos-arya-03 |
| Stole horse from | 1 | Arya → Roose Bolton | asos-arya-03 |
| Captive (for ransom) of | 1 | Arya → Brotherhood Without Banners | asos-arya-04 |
| Remembers / taught by | 1 | Arya → Syrio Forel | asos-arya-04 |
| Former lovers with | 1 | Tom Sevenstrings → Lady Smallwood | asos-arya-04 |
| Maternal protectiveness toward | 1 | Lady Smallwood → Arya | asos-arya-04 |
| Former apprentice of | 1 | Gendry → Tobho Mott | asos-arya-04 |
| Taken from master by | 1 | Gendry → Yoren | asos-arya-04 |
| Customer of | 1 | Thoros of Myr → Tobho Mott | asos-arya-04 |
| Angry at / amused by | 1 | Lady Smallwood → Tom Sevenstrings | asos-arya-04 |
| Has bad history with | 1 | Tom Sevenstrings → Lord Hoster's son | asos-arya-04 |
| Lost family to | 1 | Jack-Be-Lucky → Lannisters / Lord Piper | asos-arya-04 |
| Lost sons to | 1 | Lord Lychester → Robert's Rebellion | asos-arya-04 |
| Husband serves | 1 | Lady Smallwood → Lord Vance | asos-arya-04 |
| Feels kinship/protectiveness toward | 1 | Arya → Caged northmen | asos-arya-05 |
| Conflicted anger toward | 1 | Arya → Caged northmen | asos-arya-05 |
| Confused/hurt by | 1 | Arya → Gendry | asos-arya-05 |
| Has a son by | 1 | Tom Sevenstrings → Unnamed woman at the Peach | asos-arya-05 |
| Claims paternity from | 1 | Bella → King Robert Baratheon | asos-arya-05 |
| Propositions | 1 | Bella → Gendry | asos-arya-05 |
| Refutes rumor about | 1 | Arya → Lady Catelyn | asos-arya-05 |
| Desires the death of | 1 | Arya → Sandor Clegane | asos-arya-06 |
| Angry at / calls liar | 1 | Arya → Sansa Stark | asos-arya-06 |
| References with trust | 1 | Arya → Jory (Cassel) | asos-arya-06 |
| Startled/awestruck by | 1 | Arya → Beric Dondarrion | asos-arya-06 |
| Recognizes / contempt for | 1 | Sandor Clegane → Arya | asos-arya-06 |
| Witnessed violence against | 1 | Sandor Clegane → Sansa Stark | asos-arya-06 |
| Witnessed execution of | 1 | Sandor Clegane → Eddard Stark | asos-arya-06 |
| Recognizes from tourneys | 1 | Sandor Clegane → Thoros of Myr | asos-arya-06 |
| Distinguished from | 1 | Sandor Clegane → Gregor Clegane | asos-arya-06 |
| Defeated in melees | 1 | Thoros of Myr → Sandor Clegane | asos-arya-06 |
| Originally sent by | 1 | Beric Dondarrion → Eddard Stark | asos-arya-06 |
| Sentences / fights | 1 | Beric Dondarrion → Sandor Clegane | asos-arya-06 |
| Served by (squire) | 1 | Beric Dondarrion → Ned (squire) | asos-arya-06 |
| Reluctant cooperation with | 1 | Mad Huntsman → Brotherhood | asos-arya-06 |
| Now worships | 1 | Harwin → R'hllor | asos-arya-06 |
| Confronts / disarms | 1 | Lem Lemoncloak → Sandor Clegane / Arya | asos-arya-06 |
| Brotherhood bowman, claims combat record | 1 | Anguy → Vargo Hoat, Gregor Clegane, Roose Bolton | asos-arya-06 |
| Remembers the dead | 1 | Tom Sevenstrings → Multiple named victims | asos-arya-06 |
| Helps | 1 | Tom Sevenstrings → Sandor Clegane | asos-arya-06 |
| Shocked by Beric's scars | 1 | Gendry → Beric Dondarrion | asos-arya-06 |
| Awed by flaming sword | 1 | Gendry → (the magic itself) | asos-arya-06 |
| resurrects / serves | 1 | Thoros → Lord Beric | asos-arya-07 |
| told stories about | 1 | Harwin → Eddard Stark | asos-arya-07 |
| pledges service to | 1 | Gendry → Brotherhood / Lord Beric | asos-arya-07 |
| catalogs losses of | 1 | Arya → Jaqen, Hot Pie, Gendry, Lommy, Yoren, Syrio, Eddard | asos-arya-07 |
| draws strength from | 1 | Arya → Jaqen H'ghar (via coin) | asos-arya-07 |
| honors trial result for | 1 | Lord Beric → Sandor Clegane | asos-arya-07 |
| misunderstands | 1 | Lem → Lord Beric's resurrections | asos-arya-07 |
| fading bond with | 1 | Lord Beric → His past life | asos-arya-07 |
| grateful to / hosts | 1 | Brown brothers → Brotherhood | asos-arya-07 |
| objects to faith of | 1 | Young novice → Thoros / R'hllor | asos-arya-07 |
| desires to learn from | 1 | Arya → Anguy | asos-arya-07 |
| fiercely protective of | 1 | Arya → Eddard Stark (memory) | asos-arya-08 |
| captured by | 1 | Arya → Sandor Clegane | asos-arya-08 |
| revulsed by | 1 | Ghost of High Heart → Arya | asos-arya-08 |
| existentially despairing | 1 | Lord Beric → Thoros | asos-arya-08 |
| irritable about | 1 | Lem Lemoncloak → Arya | asos-arya-08 |
| personally connected to | 1 | Ghost of High Heart → Summerhall | asos-arya-08 |
| Hostage/captive of (antagonistic) | 1 | Arya Stark → Sandor Clegane | asos-arya-09 |
| Plans to ransom | 1 | Sandor Clegane → Arya Stark | asos-arya-09 |
| Former protector of | 1 | Sandor Clegane → Sansa Stark | asos-arya-09 |
| Rejected allegiance to | 1 | Sandor Clegane → House Lannister / Joffrey | asos-arya-09 |
| Cheated | 1 | Sandor Clegane → Bent-backed ferryman | asos-arya-09 |
| captive/charge of | 1 | Arya Stark → Sandor Clegane | asos-arya-10 |
| rival/combatant (past) to | 1 | Sandor Clegane → Ser Donnel Haigh | asos-arya-10 |
| Protective (through violence) | 1 | Sandor Clegane → Arya | asos-arya-11 |
| Killer of (recalled) | 1 | Sandor Clegane → Mycah | asos-arya-11 |
| Former student | 1 | Arya → Syrio Forel | asos-arya-11 |
| Betrayal of | 1 | House Frey → House Stark / Robb Stark | asos-arya-11 |
| Bond with mount | 1 | Sandor Clegane → Stranger | asos-arya-11 |
| Feels used by | 1 | Arya Stark → Lord Beric Dondarrion | asos-arya-12 |
| Pack leader of | 1 | Nymeria → Wolf pack | asos-arya-12 |
| Former servant of / now independent from | 1 | Sandor Clegane → Joffrey Baratheon | asos-arya-12 |
| Referenced past interaction with | 1 | Sandor Clegane → Sansa Stark | asos-arya-12 |
| Attached to / follows | 1 | Village elder's daughter → Arya Stark | asos-arya-12 |
| Recovers Needle from | 1 | Arya → Polliver (dead) | asos-arya-13 |
| Enmity / estrangement | 1 | Sandor Clegane → Gregor Clegane | asos-arya-13 |
| Confesses guilt toward | 1 | Sandor Clegane → Sansa Stark | asos-arya-13 |
| Memory / sisterly bond | 1 | Arya → Sansa Stark | asos-arya-13 |
| Distant connection | 1 | Arya → Jon Snow | asos-arya-13 |
| Protective nickname | 1 | Sandor Clegane → Sansa Stark | asos-arya-13 |
| Cheats | 1 | Horse trader woman → Arya | asos-arya-13 |
| Uses Jaqen H'ghar's teaching | 1 | Arya → Jaqen H'ghar (remembered) | asos-arya-13 |
| Resistant student of | 1 | Bran → Jojen Reed | asos-bran-01 |
| Sibling tension with | 1 | Jojen Reed → Meera Reed | asos-bran-01 |
| Protector/provider for | 1 | Meera Reed → Bran | asos-bran-01 |
| Senses | 1 | Summer → Other Stark direwolves | asos-bran-01 |
| Questions leadership of | 1 | Bran → Jojen | asos-bran-01 |
| Considers loyalty of | 1 | Bran → Northern lords | asos-bran-01 |
| carried by / dependent on | 1 | Bran Stark → Hodor | asos-bran-02 |
| hunts and provides for | 1 | Meera Reed → The group | asos-bran-02 |
| hunts for | 1 | Summer → The group | asos-bran-02 |
| protective (insists on secrecy) toward | 1 | Jojen Reed → Bran Stark | asos-bran-02 |
| uncertain judgment of | 1 | Bran Stark → Theon Greyjoy | asos-bran-02 |
| feels gratitude toward | 1 | Bran Stark → The Liddle | asos-bran-02 |
| finds shelter for | 1 | Summer → The group | asos-bran-02 |
| responds to his name | 1 | Hodor → Bran Stark | asos-bran-02 |
| shelters | 1 | The quiet wolf (in story) → The crannogman | asos-bran-02 |
| sings sadly for / sought by the king to find mystery knight | 1 | The dragon prince (in story) → The assembled lords / the mystery knight | asos-bran-02 |
| is carried by / depends on | 1 | Bran → Hodor | asos-bran-03 |
| decides to trust | 1 | Bran → Samwell Tarly | asos-bran-04 |
| asks secrecy from | 1 | Bran → Samwell Tarly | asos-bran-04 |
| considers best friend | 1 | Samwell Tarly → Jon Snow | asos-bran-04 |
| guided by | 1 | Samwell Tarly → Coldhands | asos-bran-04 |
| cannot pass | 1 | Coldhands → The Wall | asos-bran-04 |
| ruled with | 1 | Night's King (story) → Corpse queen | asos-bran-04 |
| violated guest right of | 1 | The Rat Cook (story) → The Andal king | asos-bran-04 |
| castellan of | 1 | Ser Desmond Grell → Riverrun | asos-catelyn-01 |
| lifelong servant of | 1 | Ser Desmond Grell → House Tully | asos-catelyn-01 |
| was married to | 1 | Lysa Arryn → Jon Arryn | asos-catelyn-01 |
| arranged marriage of | 1 | Lord Hoster → Lysa to Jon Arryn | asos-catelyn-01 |
| sent ravens to | 1 | Edmure → Lord Bolton (Roose) | asos-catelyn-01 |
| freed | 1 | Catelyn → Jaime Lannister | asos-catelyn-01 |
| escorting | 1 | Brienne → Jaime Lannister | asos-catelyn-01 |
| conflict with | 1 | Catelyn → Edmure | asos-catelyn-01 |
| Son, seeks forgiveness for his own act | 1 | Robb Stark → Catelyn Stark | asos-catelyn-02 |
| Mother, seeking forgiveness | 1 | Catelyn Stark → Robb Stark | asos-catelyn-02 |
| Hostile, accuses of treason | 1 | Lord Rickard Karstark → Catelyn Stark | asos-catelyn-02 |
| Supportive but condescending | 1 | The Greatjon → Catelyn Stark | asos-catelyn-02 |
| Sympathetic | 1 | Lady Mormont → Catelyn Stark | asos-catelyn-02 |
| Strained, avoiding | 1 | Edmure Tully → Catelyn Stark | asos-catelyn-02 |
| Dutiful acceptance, critical assessment | 1 | Catelyn Stark → Jeyne Westerling | asos-catelyn-02 |
| Harshly critical | 1 | Ser Brynden Tully → Edmure Tully | asos-catelyn-02 |
| Disappointed, rebuking | 1 | Robb Stark → Edmure Tully | asos-catelyn-02 |
| Distancing himself from | 1 | Robb Stark → Grey Wind | asos-catelyn-02 |
| Concerned, insistent | 1 | Catelyn Stark → Robb Stark (re: Grey Wind) | asos-catelyn-02 |
| Anxious around | 1 | Jeyne Westerling → Grey Wind | asos-catelyn-02 |
| Demands vengeance against | 1 | Lord Rickard Karstark → Jaime Lannister | asos-catelyn-02 |
| Rivalry/competition with | 1 | Edmure Tully → Robb Stark | asos-catelyn-02 |
| Cool but courteous toward | 1 | Galbart Glover → Catelyn Stark | asos-catelyn-02 |
| Almost icy toward | 1 | Jonos Bracken → Catelyn Stark | asos-catelyn-02 |
| Eager squire to | 1 | Rollam Westerling → Robb Stark | asos-catelyn-02 |
| Loyal enforcer to | 1 | Greatjon Umber → Robb | asos-catelyn-03 |
| Urges clemency to | 1 | Edmure Tully → Robb | asos-catelyn-03 |
| Pragmatic advisor to | 1 | Brynden Tully (Blackfish) → Robb | asos-catelyn-03 |
| Assesses | 1 | Catelyn → Lysa Arryn | asos-catelyn-03 |
| Devoted wife to | 1 | Jeyne Westerling → Robb | asos-catelyn-03 |
| Provides fertility aid to | 1 | Jeyne's mother → Jeyne | asos-catelyn-03 |
| Models kingship on | 1 | Robb → Ned Stark | asos-catelyn-03 |
| Deserted / betrayed | 1 | Karstark men → Robb | asos-catelyn-03 |
| Claimed past loyalty to | 1 | Rickard Karstark → Robb / Ned Stark | asos-catelyn-03 |
| Liege lord, diplomatic to | 1 | Robb → Lothar Frey | asos-catelyn-04 |
| In tension with | 1 | Robb → Catelyn | asos-catelyn-04 |
| Comfortable with | 1 | Robb → Rollam/Raynald Westerling | asos-catelyn-04 |
| Shamed by failure before | 1 | Edmure → Brynden | asos-catelyn-04 |
| Diplomatic envoy for | 1 | Lothar Frey → Lord Walder Frey | asos-catelyn-04 |
| Guilt over | 1 | Robb → Bran and Rickon (believed dead) | asos-catelyn-04 |
| Guilt/hope regarding | 1 | Catelyn → Jaime Lannister release | asos-catelyn-04 |
| Regret toward | 1 | Robb → Sansa | asos-catelyn-04 |
| husband of, deeply attached to | 1 | Robb Stark → Jeyne Westerling | asos-catelyn-05 |
| mother of, advises | 1 | Catelyn Stark → Robb Stark | asos-catelyn-05 |
| diplomatic envoy to | 1 | Lame Lothar Frey → Edmure Tully / Robb's court | asos-catelyn-05 |
| understanding toward | 1 | Maege Mormont → Catelyn Stark | asos-catelyn-05 |
| trusts, wants as heir | 1 | Robb Stark → Jon Snow | asos-catelyn-05 |
| hopes in, worries for | 1 | Catelyn Stark → Brienne of Tarth | asos-catelyn-05 |
| remembers fondly (childhood) | 1 | Catelyn Stark → Petyr Baelish | asos-catelyn-05 |
| remembers with mixed feelings | 1 | Catelyn Stark → Eddard Stark, Brandon Stark | asos-catelyn-05 |
| protects, trusted with defense of | 1 | Brynden Tully (Blackfish) → Riverrun / Jeyne Westerling | asos-catelyn-05 |
| unhappy at | 1 | Lynesse Hightower → Bear Island / the north | asos-catelyn-05 |
| assigns to Moat Cailin rearguard | 1 | Robb Stark → Roose Bolton | asos-catelyn-05 |
| offers refuge to | 1 | Jason Mallister → Catelyn Stark | asos-catelyn-05 |
| perceives Seagard stay as | 1 | Catelyn Stark → imprisonment | asos-catelyn-05 |
| strategic thinking about | 1 | Robb Stark → Victarion Greyjoy | asos-catelyn-05 |
| Mother advising son | 1 | Catelyn → Robb | asos-catelyn-06 |
| Owes amends to | 1 | Robb → Lord Walder Frey | asos-catelyn-06 |
| Dominant/humiliating toward | 1 | Lord Walder Frey → Robb | asos-catelyn-06 |
| Evaluates | 1 | Catelyn → Roslin | asos-catelyn-06 |
| Gracious host toward | 1 | Lame Lothar → Catelyn | asos-catelyn-06 |
| Recalls with comparison | 1 | Catelyn → Eddard Stark | asos-catelyn-06 |
| Strategically separates | 1 | Robb → Ser Raynald Westerling | asos-catelyn-06 |
| Sibling to | 1 | Benfrey → Roslin | asos-catelyn-06 |
| Disparaging toward | 1 | Lord Walder → His own family | asos-catelyn-06 |
| Newlywed husband of | 1 | Edmure → Roslin Frey | asos-catelyn-07 |
| Bride of (with foreknowledge of massacre) | 1 | Roslin → Edmure | asos-catelyn-07 |
| King of | 1 | Robb → Northern and river lords | asos-catelyn-07 |
| Loyal followers of | 1 | Robb → Smalljon, Robin Flint, Dacey, Patrek Mallister | asos-catelyn-07 |
| Orchestrates massacre of | 1 | Walder Frey → Robb Stark and his followers | asos-catelyn-07 |
| Hostage-taker/killer of | 1 | Catelyn → Jinglebell (Aegon) | asos-catelyn-07 |
| Complicit in massacre / kills | 1 | Ser Ryman Frey → Dacey Mormont | asos-catelyn-07 |
| Hamstrings | 1 | Black Walder → One of the Vances | asos-catelyn-07 |
| Shields/dies for | 1 | Smalljon Umber → Robb Stark | asos-catelyn-07 |
| Thinks of last | 1 | Robb → Grey Wind | asos-catelyn-07 |
| Sends regards from | 1 | The killer (Bolton) → Jaime Lannister | asos-catelyn-07 |
| Romantically pursues | 1 | Ser Jorah Mormont → Daenerys | asos-daenerys-01 |
| Mixed feelings toward (deceased) | 1 | Daenerys → Viserys Targaryen | asos-daenerys-01 |
| Closest friend (deceased) | 1 | Rhaegar Targaryen → Arthur Dayne | asos-daenerys-01 |
| Uncertain toward | 1 | Daenerys → Quaithe of the Shadow | asos-daenerys-01 |
| shows subtle honesty toward | 1 | Translator (slave girl) → Daenerys | asos-daenerys-02 |
| freed / asserts equality with | 1 | Daenerys → Irri | asos-daenerys-02 |
| puzzled by Jorah's distrust of | 1 | Daenerys → Arstan Whitebeard | asos-daenerys-02 |
| increasingly difficult for | 1 | Drogon → Daenerys | asos-daenerys-02 |
| absolute power over | 1 | Kraznys mo Nakloz → Unsullied | asos-daenerys-02 |
| frees/takes into service | 1 | Daenerys → Missandei | asos-daenerys-03 |
| rebukes/disciplines | 1 | Daenerys → Arstan Whitebeard | asos-daenerys-03 |
| familial bond | 1 | Missandei → Three unnamed Unsullied | asos-daenerys-03 |
| cryptic advisor to | 1 | Quaithe → Daenerys | asos-daenerys-03 |
| follows | 1 | Sallor the Bald → Prendahl na Ghezn | asos-daenerys-04 |
| attracted to / pledges loyalty to | 1 | Daario Naharis → Daenerys | asos-daenerys-04 |
| romantically desires | 1 | Ser Jorah → Daenerys | asos-daenerys-04 |
| rejects romantically | 1 | Daenerys → Ser Jorah | asos-daenerys-04 |
| values as advisor | 1 | Daenerys → Ser Jorah | asos-daenerys-04 |
| attempts to bribe | 1 | Grazdan mo Eraz → Daenerys | asos-daenerys-04 |
| blamed / abused | 1 | Viserys → Daenerys | asos-daenerys-04 |
| knew / served | 1 | Arstan Whitebeard → Rhaegar Targaryen | asos-daenerys-04 |
| crowned | 1 | Rhaegar → Lyanna Stark | asos-daenerys-04 |
| revere | 1 | Freed slaves → Daenerys | asos-daenerys-04 |
| sexually attracted to | 1 | Daenerys → Daario Naharis | asos-daenerys-05 |
| conflicted about/furious at | 1 | Daenerys → Ser Jorah | asos-daenerys-05 |
| mother-figure to | 1 | Daenerys → Freedmen | asos-daenerys-05 |
| jealous of / dislikes | 1 | Ser Jorah → Daario | asos-daenerys-05 |
| adversarial toward | 1 | Arstan/Barristan → Ser Jorah | asos-daenerys-05 |
| informed on | 1 | Ser Jorah → Daenerys | asos-daenerys-05 |
| amiable toward | 1 | Brown Ben Plumm → Daenerys | asos-daenerys-05 |
| affinity toward | 1 | Viserion → Brown Ben Plumm | asos-daenerys-05 |
| servant/protector of | 1 | Strong Belwas → Daenerys | asos-daenerys-05 |
| squire/attendant to | 1 | Arstan/Barristan → Strong Belwas | asos-daenerys-05 |
| desires/courts | 1 | Daario → Daenerys | asos-daenerys-05 |
| loyal soldier to | 1 | Grey Worm → Daenerys | asos-daenerys-05 |
| former bodyguard to | 1 | Brown Ben Plumm → Oznak's uncle | asos-daenerys-05 |
| remembers / lost to wound | 1 | Dany → Khal Drogo | asos-daenerys-05 |
| Queen/ruler over | 1 | Daenerys → Meereen | asos-daenerys-06 |
| Forgives/restores | 1 | Daenerys → Ser Barristan Selmy | asos-daenerys-06 |
| Banishes | 1 | Daenerys → Ser Jorah Mormont | asos-daenerys-06 |
| Former spy for | 1 | Ser Jorah → Varys | asos-daenerys-06 |
| Devoted to / possessive of | 1 | Daario → Daenerys | asos-daenerys-06 |
| Knows of | 1 | Missandei → Naath (homeland) | asos-daenerys-06 |
| Growing bolder | 1 | Dragons (all three) → — | asos-daenerys-06 |
| Remembers with loss | 1 | Dany → Ser Willem Darry | asos-daenerys-06 |
| rowed to Storm's End | 1 | Davos → Melisandre | asos-davos-01 |
| converted | 1 | Melisandre → Selyse Baratheon | asos-davos-01 |
| influenced/converted | 1 | Melisandre → Stannis Baratheon | asos-davos-01 |
| originates from | 1 | Melisandre → Asshai | asos-davos-01 |
| burned the Seven at urging of | 1 | Stannis → Melisandre | asos-davos-01 |
| burned godswood at urging of | 1 | Stannis → Melisandre | asos-davos-01 |
| served as oarmaster on | 1 | Maric Seaworth → Fury | asos-davos-01 |
| served as second on | 1 | Matthos Seaworth → Black Betha | asos-davos-01 |
| has wife | 1 | Davos → Unnamed wife | asos-davos-01 |
| at war with | 1 | Stannis Baratheon → Joffrey | asos-davos-01 |
| owed service by | 1 | Salladhor Saan → Stannis Baratheon | asos-davos-02 |
| isolation with | 1 | Stannis Baratheon → Melisandre | asos-davos-02 |
| political partnership with | 1 | Queen Selyse → Lord Alester Florent | asos-davos-02 |
| believes Mother saved him | 1 | Davos Seaworth → The Mother (deity) | asos-davos-02 |
| playful with | 1 | Shireen Baratheon → Patchface | asos-davos-02 |
| plays with/protective of | 1 | Edric Storm → Shireen Baratheon | asos-davos-02 |
| Loyal subject/prisoner of | 1 | Davos → Stannis | asos-davos-03 |
| Suspects then exonerates | 1 | Davos → Salladhor Saan | asos-davos-03 |
| Proselytizes/attempts to recruit | 1 | Melisandre → Davos | asos-davos-03 |
| Former Hand to | 1 | Lord Alester Florent → Stannis | asos-davos-03 |
| Mild kinship/sympathy toward | 1 | Davos → Lord Alester | asos-davos-03 |
| Loyal sworn man / new Hand | 1 | Davos → Stannis | asos-davos-04 |
| Coerces and threatens | 1 | Ser Axell → Davos | asos-davos-04 |
| Cellmate | 1 | Lord Alester → Davos | asos-davos-04 |
| Condemned as traitor | 1 | Lord Alester → Stannis | asos-davos-04 |
| Guilt and conflict toward | 1 | Stannis → Renly Baratheon | asos-davos-04 |
| Claims no intent to harm | 1 | Stannis → Edric Storm | asos-davos-04 |
| Relies on / defends | 1 | Stannis → Melisandre | asos-davos-04 |
| Saved Davos's life | 1 | Melisandre → Davos | asos-davos-04 |
| Murderous intent toward | 1 | Davos → Melisandre | asos-davos-04 |
| Wants to sacrifice | 1 | Melisandre → Edric Storm | asos-davos-04 |
| Refuses to sacrifice | 1 | Stannis → Edric Storm | asos-davos-04 |
| Self-comparison (unfavorable) | 1 | Stannis → Robert | asos-davos-04 |
| Values duty over desire | 1 | Stannis → The Iron Throne | asos-davos-04 |
| Husband of (strained) | 1 | Stannis → Selyse | asos-davos-05 |
| Complex dynamic with | 1 | Stannis → Melisandre | asos-davos-05 |
| Follows / echoes | 1 | Ser Axell → Melisandre and Selyse | asos-davos-05 |
| Plays with / befriends | 1 | Shireen → Edric Storm | asos-davos-05 |
| Asks after | 1 | Edric Storm → Stannis | asos-davos-05 |
| Confided in | 1 | Stannis → Maester Cressen (formerly) | asos-davos-05 |
| Prays for the safety of | 1 | Davos → Devan Seaworth | asos-davos-06 |
| Wishes to return to | 1 | Davos → Marya Seaworth | asos-davos-06 |
| Grateful to / initially uncertain of | 1 | Davos → Maester Pylos | asos-davos-06 |
| Torn between duty and morality regarding | 1 | Stannis → Edric Storm | asos-davos-06 |
| Angry at but still listens to | 1 | Stannis → Davos | asos-davos-06 |
| Fervent worshiper of | 1 | Queen Selyse → R'hllor | asos-davos-06 |
| Formerly sworn to | 1 | Ser Triston of Tally Hill → Lord Guncer Sunglass | asos-davos-06 |
| Considers himself rightful king over | 1 | Stannis → Tommen Baratheon | asos-davos-06 |
| co-plotter with | 1 | Lame Lothar Frey → Roose Bolton | asos-epilogue |
| ordered | 1 | Lord Walder Frey → Red Wedding slaughter | asos-epilogue |
| leader/judge of | 1 | Lady Stoneheart → Brotherhood Without Banners | asos-epilogue |
| fellow squire of (past) | 1 | Merrett Frey → Jaime Lannister | asos-epilogue |
| captured by (past) | 1 | Merrett Frey → Wenda the White Fawn | asos-epilogue |
| died campaigning with | 1 | Ser Stevron Frey → Robb Stark | asos-epilogue |
| prisoner/captive of | 1 | Jaime Lannister → Brienne of Tarth | asos-jaime-01 |
| fawning/sycophantic toward | 1 | Ser Cleos Frey → Jaime Lannister | asos-jaime-01 |
| sexual desire/obsessive attachment toward | 1 | Jaime Lannister → Cersei Lannister | asos-jaime-01 |
| freed/released | 1 | Catelyn Stark → Jaime Lannister | asos-jaime-01 |
| pursues on orders | 1 | Ser Robin Ryger → Jaime Lannister | asos-jaime-01 |
| allegiance to | 1 | Lord Walder Frey → Riverrun (Tully) | asos-jaime-01 |
| took Harrenhal from | 1 | Roose Bolton → Ser Amory Lorch | asos-jaime-01 |
| burned castle of | 1 | Lord Tywin Lannister → Lord Jonos Bracken | asos-jaime-01 |
| deference toward | 1 | Ser Cleos → Brienne | asos-jaime-02 |
| squired for | 1 | Jaime → Ser Sumner Crakehall | asos-jaime-02 |
| Son, barely remembers her | 1 | Jaime → Lady Joanna | asos-jaime-03 |
| Son, complicated loyalty | 1 | Jaime → Tywin Lannister | asos-jaime-03 |
| Contempt toward, attempting to manipulate | 1 | Jaime → Urswyck | asos-jaime-03 |
| Loyal servant | 1 | Brienne → Catelyn Stark | asos-jaime-03 |
| Former servants, now betrayers | 1 | Brave Companions → House Lannister | asos-jaime-03 |
| Currently serve | 1 | Brave Companions → Roose Bolton / King in the North | asos-jaime-03 |
| Claims lordship granted by Lannisters | 1 | Vargo Hoat → Harrenhal | asos-jaime-03 |
| Cruel enforcer | 1 | Rorge → Brave Companions | asos-jaime-03 |
| motivates | 1 | Brienne → Jaime | asos-jaime-04 |
| bound prisoner of | 1 | Jaime → Vargo Hoat | asos-jaime-04 |
| reports death of | 1 | Jaime → Ser Cleos Frey | asos-jaime-04 |
| implies knowledge of | 1 | Bolton → Jaime-Cersei incest | asos-jaime-04 |
| memory of witnessing | 1 | Jaime → Deaths of Rickard and Brandon Stark | asos-jaime-04 |
| guilt/resentment toward | 1 | Jaime → Ned Stark | asos-jaime-05 |
| shock/naivety about | 1 | Brienne → Robb Stark's choices | asos-jaime-05 |
| maimed | 1 | Vargo Hoat → Jaime | asos-jaime-05 |
| healer to | 1 | Qyburn → Jaime | asos-jaime-05 |
| desires/is faithful to | 1 | Jaime → Cersei | asos-jaime-06 |
| is escorted by | 1 | Jaime → Steelshanks Walton | asos-jaime-06 |
| is tended by | 1 | Jaime → Qyburn | asos-jaime-06 |
| offers ransom for | 1 | Lord Selwyn → Brienne | asos-jaime-06 |
| taunts/threatens | 1 | Jaime → Brave Companions | asos-jaime-06 |
| hopes for patronage from | 1 | Qyburn → Tywin Lannister | asos-jaime-06 |
| accuse | 1 | Dead Kingsguard (dream) → Jaime | asos-jaime-06 |
| stands with | 1 | Brienne (dream) → Jaime | asos-jaime-06 |
| Son, defiant | 1 | Jaime → Tywin | asos-jaime-07 |
| Reluctant protector of | 1 | Jaime → Brienne | asos-jaime-07 |
| Broken by news of | 1 | Brienne → Robb Stark / Catelyn Stark | asos-jaime-07 |
| Annoyed by | 1 | Jaime → Qyburn | asos-jaime-07 |
| Father, controlling | 1 | Tywin → Jaime | asos-jaime-07 |
| Manipulative toward | 1 | Tywin → Cersei | asos-jaime-07 |
| Discusses investigation of | 1 | Tywin → Tyrion | asos-jaime-07 |
| Unfamiliar with | 1 | Osmund Kettleblack → Jaime | asos-jaime-07 |
| Destroys | 1 | Gregor Clegane → Vargo Hoat | asos-jaime-07 |
| Grim satisfaction toward | 1 | Jaime → Vargo Hoat | asos-jaime-07 |
| feels unworthy compared to | 1 | Jaime → Barristan Selmy | asos-jaime-08 |
| idolizes (past) | 1 | Jaime → Ser Arthur Dayne | asos-jaime-08 |
| sees himself in | 1 | Jaime → Ser Loras | asos-jaime-08 |
| secret paternal connection to | 1 | Jaime → Joffrey | asos-jaime-08 |
| torn between | 1 | Ser Balon → Jaime / his family | asos-jaime-08 |
| thought absurd | 1 | Renly (as reported) → Brienne | asos-jaime-08 |
| considering consulting | 1 | Jaime → Varys | asos-jaime-08 |
| rejects/pushes away | 1 | Jaime → Cersei | asos-jaime-09 |
| plans to remarry | 1 | Lord Tywin → Cersei | asos-jaime-09 |
| loyalty/devotion to | 1 | Brienne → Jaime | asos-jaime-09 |
| guilt/unease about | 1 | Jaime → Bran Stark | asos-jaime-09 |
| Pretending to serve / secretly loyal to | 1 | Jon Snow → Night's Watch | asos-jon-01 |
| Infiltrating | 1 | Jon Snow → Mance Rayder's wildlings | asos-jon-01 |
| King / leader of | 1 | Mance Rayder → Free folk (all wildlings) | asos-jon-01 |
| Former comrade / enemy of | 1 | Mance Rayder → Qhorin Halfhand | asos-jon-01 |
| Formerly stationed at | 1 | Mance Rayder → Shadow Tower | asos-jon-01 |
| Wanted measure of | 1 | Mance Rayder → Benjen Stark | asos-jon-01 |
| Growing fondness | 1 | Jon Snow → Tormund Giantsbane | asos-jon-02 |
| Loyalty / duty | 1 | Jon Snow → House Stark | asos-jon-02 |
| Protective bond | 1 | Jon Snow → Ghost | asos-jon-02 |
| Protective / romantic pursuit | 1 | Ygritte → Jon Snow | asos-jon-02 |
| Left Rattleshirt's band for Tormund's | 1 | Ygritte → Tormund Giantsbane | asos-jon-02 |
| Hostile / distrustful | 1 | Styr → Jon Snow | asos-jon-02 |
| Hostile/wary | 1 | Ghost → Varamyr's animals | asos-jon-02 |
| Obedience to orders | 1 | Jon Snow → Qhorin Halfhand | asos-jon-02 |
| Considers Jon her man / "stolen" her | 1 | Ygritte → Jon Snow | asos-jon-03 |
| Identifies as bastard of, questions parallel | 1 | Jon Snow → Eddard Stark | asos-jon-03 |
| Feels displaced by / parallel to | 1 | Jon Snow → Theon Greyjoy | asos-jon-03 |
| Dutiful memory of | 1 | Jon Snow → Maester Luwin | asos-jon-03 |
| Connected to via Val | 1 | Jarl → Mance Rayder | asos-jon-03 |
| From same village as | 1 | Ygritte → Longspear (Ryk) | asos-jon-03 |
| Likes | 1 | Jon Snow → Longspear (Ryk) | asos-jon-03 |
| Helpful to | 1 | Grigg the Goat → Jon Snow | asos-jon-03 |
| Romantic attachment / divided loyalty toward | 1 | Jon Snow → Ygritte | asos-jon-04 |
| Romantic attachment to / frustration with | 1 | Ygritte → Jon Snow | asos-jon-04 |
| Anger / hatred toward | 1 | Ygritte → The Wall | asos-jon-04 |
| Yearns for connection with | 1 | Jon Snow → Ghost | asos-jon-05 |
| Growing attachment (unwanted) | 1 | Jon Snow → Wildling raiders (Del, Bodger, Quort, etc.) | asos-jon-05 |
| Scout/guide for | 1 | Grigg the Goat → Styr | asos-jon-05 |
| Weather-predictor for | 1 | Lenn → The raiding party | asos-jon-05 |
| Remembers instructions from | 1 | Jon Snow → Qhorin Halfhand | asos-jon-05 |
| follows orders of | 1 | Jon Snow → Qhorin Halfhand | asos-jon-06 |
| parallels himself with | 1 | Jon Snow → Eddard Stark | asos-jon-06 |
| healer/authority over | 1 | Maester Aemon → Jon Snow | asos-jon-06 |
| mutual enmity with | 1 | Cotter Pyke → Ser Denys Mallister | asos-jon-06 |
| Antagonism / enmity | 1 | Jon Snow → Rast | asos-jon-07 |
| Memory / shared youth | 1 | Jon Snow → Robb Stark | asos-jon-07 |
| Fights alongside / trusts | 1 | Satin → Jon Snow | asos-jon-07 |
| Strategic partnership | 1 | Donal Noye → Maester Aemon | asos-jon-07 |
| Irritates | 1 | Septon Cellador → Jon Snow / Donal Noye | asos-jon-08 |
| Cares for / feels responsible for | 1 | Jon Snow → Wall defenders | asos-jon-09 |
| Boosts morale of | 1 | Pyp → Defenders | asos-jon-09 |
| Naive hopefulness | 1 | Owen → (general) | asos-jon-09 |
| Previously trusted | 1 | Donal Noye → Jon Snow | asos-jon-09 |
| Shame before | 1 | Jon Snow → Eddard Stark | asos-jon-10 |
| Stole (married by capture) | 1 | Longspear Ryk → Munda | asos-jon-10 |
| Contains/absorbed | 1 | Varamyr → Orell | asos-jon-10 |
| Offers legitimization and lordship to | 1 | Stannis Baratheon → Jon Snow | asos-jon-11 |
| Criticizes / distrusts | 1 | Stannis Baratheon → Janos Slynt | asos-jon-11 |
| Intends to execute | 1 | Stannis Baratheon → Mance Rayder | asos-jon-11 |
| Exerts spiritual pressure on | 1 | Melisandre → Jon Snow | asos-jon-11 |
| Conflicted with memory of | 1 | Stannis Baratheon → Robert Baratheon | asos-jon-11 |
| childhood brothers with | 1 | Jon Snow → Robb Stark | asos-jon-12 |
| resented by (memory) | 1 | Jon Snow → Catelyn Stark | asos-jon-12 |
| nominated by | 1 | Jon Snow → Dolorous Edd | asos-jon-12 |
| unrealized connection to | 1 | Jon Snow → Val | asos-jon-12 |
| offers to serve | 1 | Bowen Marsh → Jon Snow | asos-jon-12 |
| pivots support to | 1 | Othell Yarwyck → Jon Snow | asos-jon-12 |
| chooses | 1 | Mormont's raven → Jon Snow | asos-jon-12 |
| backed by | 1 | Janos Slynt → Tywin Lannister | asos-jon-12 |
| asked sacrifice of | 1 | Sam Tarly → Ser Denys Mallister | asos-jon-12 |
| Intends to murder | 1 | Chett → Samwell Tarly | asos-prologue |
| Leader of mutiny | 1 | Chett → Small Paul, Lark, Dirk, Softfoot, Sweet Donnel Hill, Clubfoot Karl, Maslyn, Sawwood, Lark's cousins | asos-prologue |
| Former steward to | 1 | Chett → Maester Aemon | asos-prologue |
| Persuades / allies with | 1 | Thoren Smallwood → Ser Mallador Locke | asos-prologue |
| Disagrees with | 1 | Thoren Smallwood → Ser Ottyn Wythers | asos-prologue |
| Judged | 1 | Walder Rivers → Chett | asos-prologue |
| Escorted to Wall | 1 | Yoren → Chett | asos-prologue |
| Covets lifestyle of | 1 | Chett → Craster | asos-prologue |
| Carried by/gratitude | 1 | Sam → Small Paul | asos-samwell-01 |
| Self-loathing/obedience | 1 | Sam → Lord Randyll Tarly | asos-samwell-01 |
| Promised raven by | 1 | Small Paul → Chett | asos-samwell-01 |
| Tends ravens for | 1 | Sam → Maester Aemon | asos-samwell-01 |
| Recalls/hears voices of | 1 | Sam → Alliser Thorne, Rast, Dickon, Lord Randyll | asos-samwell-01 |
| Teased | 1 | Pyp → Grenn | asos-samwell-01 |
| feels obligation toward | 1 | Sam → Gilly | asos-samwell-02 |
| paternal toward | 1 | Mormont → Jorah (estranged) | asos-samwell-02 |
| depends on/trusts | 1 | Gilly → Sam | asos-samwell-02 |
| rejected/demeaned | 1 | Lord Randyll → Sam | asos-samwell-03 |
| former wife of | 1 | Gilly → Craster | asos-samwell-03 |
| offers to be wife of | 1 | Gilly → Sam | asos-samwell-03 |
| attack/oppose | 1 | Ravens (flock) → Wights | asos-samwell-03 |
| threaten/surround | 1 | Wights → Gilly | asos-samwell-03 |
| Romantic attachment | 1 | Samwell → Gilly | asos-samwell-04 |
| Sad bond/protectiveness | 1 | Jon Snow → Val and the babe | asos-samwell-04 |
| Devotion/loyalty | 1 | Val → Mance Rayder | asos-samwell-04 |
| Nursing/care | 1 | Gilly → Mance Rayder's son | asos-samwell-04 |
| Sworn brotherhood/emotional reunion | 1 | Sam → Dywen, Giant, Dolorous Edd | asos-samwell-04 |
| Political scheming | 1 | Ser Alliser Thorne → Othell Yarwyck | asos-samwell-04 |
| Enmity/accusation | 1 | Ser Alliser Thorne → Jon Snow | asos-samwell-04 |
| Enmity (received) | 1 | Jon Snow → Ser Alliser Thorne | asos-samwell-04 |
| Suspicion/removal from duty | 1 | Bowen Marsh → Jon Snow | asos-samwell-04 |
| Suppressed honesty / oath conflict | 1 | Sam → Jon Snow | asos-samwell-04 |
| Oath of secrecy | 1 | Sam → Bran Stark, Jojen Reed, Coldhands | asos-samwell-04 |
| Rescuer/debt-holder | 1 | Coldhands → Sam | asos-samwell-04 |
| Political rivalry | 1 | Ser Denys Mallister → Cotter Pyke | asos-samwell-04 |
| Complex filial resentment | 1 | Sam → Lord Randyll Tarly | asos-samwell-04 |
| Complicated self-identity | 1 | Jon Snow → Ghost | asos-samwell-04 |
| Haunted connection | 1 | Jon Snow → Robb Stark, Eddard Stark | asos-samwell-04 |
| Awe/gratitude | 1 | Sam → Stannis Baratheon | asos-samwell-04 |
| Anger/contempt | 1 | Sam → Joffrey, Tommen | asos-samwell-04 |
| Service | 1 | Sam → Maester Aemon | asos-samwell-04 |
| Fawns on | 1 | Janos Slynt → Stannis | asos-samwell-05 |
| Aware of identity | 1 | Stannis → Maester Aemon | asos-samwell-05 |
| Campaigns for | 1 | Sam → Jon Snow | asos-samwell-05 |
| Trusted by | 1 | Jon Snow → Mormont, Noye, Halfhand | asos-samwell-05 |
| Polite but detached toward | 1 | Ser Loras → Sansa | asos-sansa-01 |
| Complex attachment to | 1 | Sansa → Sandor Clegane | asos-sansa-01 |
| Warmly welcoming toward | 1 | Margaery → Sansa | asos-sansa-01 |
| Interrogates/manipulates | 1 | Lady Olenna → Sansa | asos-sansa-01 |
| Tries to manage | 1 | Lady Alerie → Lady Olenna | asos-sansa-01 |
| Sisterly with | 1 | Margaery → Ser Loras | asos-sansa-01 |
| Dreads | 1 | Sansa → Cersei Lannister | asos-sansa-01 |
| Proposes match between | 1 | Lady Olenna → Sansa and Willas | asos-sansa-01 |
| Enjoys companionship of | 1 | Sansa Stark → Margaery Tyrell | asos-sansa-02 |
| Pitied by (mistakenly) | 1 | Sansa Stark → Megga Tyrell | asos-sansa-02 |
| Pities and envies | 1 | Sansa Stark → Tyrell cousins | asos-sansa-02 |
| Reminds Sansa of | 1 | Lady Bulwer → Arya Stark | asos-sansa-02 |
| Idealizes | 1 | Sansa Stark → Ser Loras Tyrell | asos-sansa-02 |
| Acts as self-styled protector of | 1 | Ser Dontos Hollard → Sansa Stark | asos-sansa-02 |
| Forced conditions on | 1 | Mace Tyrell → Joffrey Baratheon | asos-sansa-02 |
| Kingsguard protector of | 1 | Ser Loras Tyrell → Margaery Tyrell | asos-sansa-02 |
| Recalls with complex emotion | 1 | Sansa Stark → Sandor Clegane | asos-sansa-02 |
| Married to (forced, unconsummated) | 1 | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| Previously married to | 1 | Tyrion Lannister → Tysha | asos-sansa-03 |
| Sexually threatens | 1 | Joffrey Baratheon → Sansa Stark | asos-sansa-03 |
| Sympathetic but distanced from | 1 | Margaery Tyrell → Sansa Stark | asos-sansa-03 |
| Ignores | 1 | Olenna Tyrell → Sansa Stark | asos-sansa-03 |
| Distance from | 1 | Elinor, Alla, Megga Tyrell → Sansa Stark | asos-sansa-03 |
| Humiliated by | 1 | Dontos Hollard → Joffrey Baratheon | asos-sansa-03 |
| Remembers kindness from | 1 | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| Feels pity toward | 1 | Sansa Stark → Tyrion Lannister | asos-sansa-03 |
| Shows restraint/honor toward | 1 | Tyrion Lannister → Sansa Stark | asos-sansa-03 |
| Named | 1 | Willas Tyrell → Ser Garlan Tyrell | asos-sansa-03 |
| Married to (unwilling) | 1 | Sansa → Tyrion | asos-sansa-04 |
| Wary then sympathetic toward | 1 | Sansa → Podrick Payne | asos-sansa-04 |
| Attempting trust with | 1 | Tyrion → Sansa | asos-sansa-04 |
| Supports / equips | 1 | Tywin → Joffrey | asos-sansa-04 |
| Rebukes | 1 | Ser Garlan Tyrell → Joffrey | asos-sansa-04 |
| Curries favor with | 1 | Mace Tyrell → Joffrey | asos-sansa-04 |
| Manipulated ward/escaped prisoner | 1 | Sansa Stark → Petyr Baelish | asos-sansa-05 |
| Puppet master / employer | 1 | Petyr Baelish → Ser Dontos Hollard | asos-sansa-05 |
| Orders execution of | 1 | Petyr Baelish → Ser Dontos Hollard | asos-sansa-05 |
| Rescuer / guide (catspaw) | 1 | Ser Dontos Hollard → Sansa Stark | asos-sansa-05 |
| Saved his life previously | 1 | Sansa Stark → Ser Dontos Hollard | asos-sansa-05 |
| Estranged wife | 1 | Sansa Stark → Tyrion Lannister | asos-sansa-05 |
| Relief at death of | 1 | Sansa Stark → Joffrey Baratheon | asos-sansa-05 |
| Received Harrenhal and title from | 1 | Petyr Baelish → Joffrey Baratheon | asos-sansa-05 |
| Antagonist to / avoids | 1 | Petyr Baelish → Varys | asos-sansa-05 |
| Used / discarded | 1 | Petyr Baelish → Dontos Hollard | asos-sansa-06 |
| Cold toward / possessive of | 1 | Lysa Arryn → Sansa Stark | asos-sansa-06 |
| Sexually assaults | 1 | Marillion → Sansa Stark | asos-sansa-06 |
| kisses against her will / exerts control over | 1 | Petyr Baelish → Sansa Stark | asos-sansa-07 |
| obsessed with / loves the memory of | 1 | Petyr Baelish → Catelyn Stark | asos-sansa-07 |
| jealous of / threatens | 1 | Lysa Arryn → Sansa Stark | asos-sansa-07 |
| jealous of / resents | 1 | Lysa Arryn → Catelyn Stark | asos-sansa-07 |
| poisoned at Petyr's instruction | 1 | Lysa Arryn → Jon Arryn | asos-sansa-07 |
| dotes on / favors | 1 | Lysa Arryn → Marillion | asos-sansa-07 |
| dreads / fears | 1 | Sansa Stark → Robert Arryn (as husband) | asos-sansa-07 |
| dislikes / resents | 1 | Robert Arryn → Sansa Stark | asos-sansa-07 |
| desires / pursues | 1 | Marillion → Sansa Stark | asos-sansa-07 |
| forced to abort / forced marriage on | 1 | Lord Hoster Tully → Lysa Arryn | asos-sansa-07 |
| claims Catelyn was dismissed by | 1 | Lysa Arryn → Petyr Baelish | asos-sansa-07 |
| treats medically | 1 | Maester Colemon → Robert Arryn | asos-sansa-07 |
| deceived / used false promises with | 1 | Petyr Baelish → Sansa Stark | asos-sansa-07 |
| Employs / depends on | 1 | Tyrion → Bronn | asos-tyrion-01 |
| Questions paternity of | 1 | Tywin → Tyrion | asos-tyrion-01 |
| Mercenary loyalty to | 1 | Bronn → Tyrion | asos-tyrion-01 |
| Disrespectful toward | 1 | Bronn → Tywin | asos-tyrion-01 |
| Protective guilt toward | 1 | Tyrion → Alayaya | asos-tyrion-01 |
| Protective secrecy toward | 1 | Tyrion → Shae | asos-tyrion-01 |
| Insists on finding | 1 | Tywin → Tyrek | asos-tyrion-01 |
| Values instrumentally | 1 | Tywin → Gregor Clegane | asos-tyrion-01 |
| Uneasy intelligence-sharing with | 1 | Tyrion → Varys | asos-tyrion-02 |
| Facilitates meetings for | 1 | Varys → Tyrion and Shae | asos-tyrion-02 |
| Report to / serve | 1 | Kettleblacks → Cersei Lannister | asos-tyrion-02 |
| Feels protective toward / guilty about | 1 | Tyrion → Alayaya | asos-tyrion-02 |
| Beds | 1 | Bronn → Alayaya and Marei | asos-tyrion-02 |
| Creature of / loyal to | 1 | Grand Maester Pycelle → House Lannister | asos-tyrion-02 |
| Potential threat to | 1 | Symon Silver Tongue → Tyrion and Shae | asos-tyrion-02 |
| takes pleasure in suffering of | 1 | Tyrion Lannister → Cersei Lannister | asos-tyrion-03 |
| feels no remorse toward | 1 | Tyrion Lannister → Pycelle | asos-tyrion-03 |
| sexually used | 1 | Cersei Lannister → Lancel Lannister | asos-tyrion-03 |
| may wish to silence | 1 | Cersei Lannister → Lancel Lannister | asos-tyrion-03 |
| uses strategically | 1 | Tywin Lannister → Sansa Stark | asos-tyrion-03 |
| suspicious reaction to | 1 | Tywin Lannister → Westerling marriage | asos-tyrion-03 |
| ominous toward | 1 | Tywin Lannister → House Westerling | asos-tyrion-03 |
| broke oath to | 1 | Robb Stark → House Frey | asos-tyrion-03 |
| unconsummated marriage | 1 | Tyrion → Sansa Stark | asos-tyrion-04 |
| blackmailed by | 1 | Tyrion → Symon Silver Tongue | asos-tyrion-04 |
| relies on (reluctantly) | 1 | Tywin → Tyrion | asos-tyrion-04 |
| squire | 1 | Tyrion → Podrick Payne | asos-tyrion-04 |
| relied on | 1 | Tywin → Ser Kevan Lannister | asos-tyrion-04 |
| created financial crisis for | 1 | Littlefinger → The Crown | asos-tyrion-04 |
| knows about | 1 | Symon Silver Tongue → Shae | asos-tyrion-04 |
| lord and squire | 1 | Tyrion → Podrick Payne | asos-tyrion-05 |
| lord and sworn knight | 1 | Tyrion → Bronn | asos-tyrion-05 |
| deep sibling bond | 1 | Oberyn → Elia Martell | asos-tyrion-05 |
| vengeance-seeker | 1 | Oberyn → Gregor Clegane | asos-tyrion-05 |
| implicit antagonist | 1 | Oberyn → Tywin Lannister | asos-tyrion-05 |
| cold host | 1 | Tywin → Oberyn's family | asos-tyrion-05 |
| no ill will, correspondents | 1 | Oberyn → Willas Tyrell | asos-tyrion-05 |
| strained service | 1 | Tyrion → Tywin Lannister | asos-tyrion-05 |
| cold father | 1 | Tywin → Tyrion | asos-tyrion-05 |
| natural son | 1 | Ser Daemon Sand → Ser Ryon Allyrion | asos-tyrion-05 |
| mocking familiarity | 1 | Oberyn → Tyrion | asos-tyrion-05 |
| investigated | 1 | Jon Arryn → Doran Martell / Sunspear | asos-tyrion-05 |
| Strained marriage | 1 | Tyrion → Sansa | asos-tyrion-06 |
| Mastermind of | 1 | Tywin → Walder Frey | asos-tyrion-06 |
| Shocked by | 1 | Ser Kevan → Joffrey | asos-tyrion-06 |
| Pious devotion | 1 | Sansa → The old gods / Faith of the Seven | asos-tyrion-06 |
| Demands justice from | 1 | Oberyn Martell → Tywin / the crown | asos-tyrion-06 |
| Refuses to surrender | 1 | Tywin → Gregor Clegane | asos-tyrion-06 |
| Physically abusive toward | 1 | Robert Baratheon → Joffrey | asos-tyrion-06 |
| Pragmatic view of | 1 | Tywin → Elia Martell | asos-tyrion-06 |
| Unconsummated husband of | 1 | Tyrion → Sansa | asos-tyrion-07 |
| Shields from ugly truths | 1 | Tyrion → Sansa | asos-tyrion-07 |
| Prays nightly in the | 1 | Sansa → Godswood | asos-tyrion-07 |
| Placed Brella in Tyrion's household | 1 | Varys → Brella | asos-tyrion-07 |
| Considers sending Shae to | 1 | Tyrion → Chataya | asos-tyrion-07 |
| married to (strained) | 1 | Tyrion → Sansa | asos-tyrion-08 |
| suspects/accuses (internally) | 1 | Tyrion → Joffrey | asos-tyrion-08 |
| attempts to manage | 1 | Margaery → Joffrey | asos-tyrion-08 |
| needles | 1 | Lady Olenna → Tyrion | asos-tyrion-08 |
| dutiful but cold toward | 1 | Sansa → Tyrion | asos-tyrion-08 |
| controlled by threat of | 1 | Joffrey → Tyrion | asos-tyrion-08 |
| placed Dornishmen far from | 1 | Cersei → Tyrells | asos-tyrion-08 |
| weakened, dependent on | 1 | Lancel → Ser Kevan | asos-tyrion-08 |
| performs courtesy for | 1 | Sansa → Lancel, Lord Gyles, Elinor Tyrell, Jalabhar Xho | asos-tyrion-08 |
| accused by / opposed by | 1 | Tyrion → Cersei | asos-tyrion-09 |
| served loyally by | 1 | Tyrion → Podrick Payne | asos-tyrion-09 |
| judged by | 1 | Tyrion → Lord Tywin | asos-tyrion-09 |
| intermediary for | 1 | Ser Kevan → Tywin | asos-tyrion-09 |
| offers to champion | 1 | Prince Oberyn → Tyrion | asos-tyrion-09 |
| married to (estranged) | 1 | Tyrion → Sansa Stark | asos-tyrion-09 |
| believes poisoned Joffrey | 1 | Tyrion → Sansa | asos-tyrion-09 |
| has already condemned | 1 | Mace Tyrell → Tyrion | asos-tyrion-09 |
| offered children to | 1 | Lord Tywin → King Robert | asos-tyrion-09 |
| Self-blame regarding | 1 | Tyrion → Shae | asos-tyrion-10 |
| Gratitude toward | 1 | Tyrion → Podrick Payne | asos-tyrion-10 |
| Vengeance-driven motivation against | 1 | Prince Oberyn → Ser Gregor Clegane | asos-tyrion-10 |
| Sibling devotion to | 1 | Prince Oberyn → Elia Martell | asos-tyrion-10 |
| Cold judgment of | 1 | Lord Tywin → Tyrion | asos-tyrion-10 |
| Control of proceedings | 1 | Lord Tywin → The trial | asos-tyrion-10 |
| Satisfaction at Tyrion's suffering | 1 | Cersei → Tyrion | asos-tyrion-10 |
| Obedience to | 1 | Ser Gregor → Cersei | asos-tyrion-10 |
| Killer of | 1 | Ser Gregor → Oberyn | asos-tyrion-10 |
| Abandoned by (in thought) | 1 | Tyrion → Ser Kevan | asos-tyrion-10 |
| Judge / questioner | 1 | Mace Tyrell → Tyrion | asos-tyrion-10 |
| Mockery of (past) | 1 | Oberyn → Baelor Hightower | asos-tyrion-10 |
| Kisses farewell | 1 | Jaime → Tyrion | asos-tyrion-11 |
| Confesses guilt to | 1 | Jaime → Tyrion | asos-tyrion-11 |
| Strikes in rage | 1 | Tyrion → Jaime | asos-tyrion-11 |
| Swears vengeance against | 1 | Tyrion → Jaime | asos-tyrion-11 |
| Deliberately wounds | 1 | Tyrion → Jaime | asos-tyrion-11 |
| Watches depart with regret | 1 | Tyrion → Jaime | asos-tyrion-11 |
| Assists escape of | 1 | Varys → Tyrion | asos-tyrion-11 |
| Feared by / distrusted by | 1 | Varys → Tyrion | asos-tyrion-11 |
| Arranged testimony against | 1 | Cersei → Tyrion | asos-tyrion-11 |
| In bed with | 1 | Shae → Tywin | asos-tyrion-11 |
| Claimed loyalty to | 1 | Shae → Tyrion | asos-tyrion-11 |
| Claims protector of | 1 | Tywin → Tyrion | asos-tyrion-11 |
| Suspected | 1 | Jaime → Joffrey | asos-tyrion-11 |
| Poses as natural daughter of | 1 | Alayne → Petyr Baelish | affc-alayne-01 |
| Acts as guardian/father figure with inappropriate undertones toward | 1 | Petyr Baelish → Alayne | affc-alayne-01 |
| Stepfather and Lord Protector of | 1 | Petyr Baelish → Robert Arryn | affc-alayne-01 |
| Dependent on / obedient to (reluctantly) | 1 | Robert Arryn → Petyr Baelish | affc-alayne-01 |
| Treats / serves | 1 | Maester Colemon → Robert Arryn | affc-alayne-01 |
| Overrules medical judgment of | 1 | Petyr Baelish → Maester Colemon | affc-alayne-01 |
| Chief opponent of | 1 | Bronze Yohn Royce → Petyr Baelish | affc-alayne-01 |
| Politically opposed to / estranged from | 1 | Nestor Royce → Bronze Yohn Royce | affc-alayne-01 |
| Secret agent of | 1 | Lyn Corbray → Petyr Baelish | affc-alayne-01 |
| Rivalrous with / resents | 1 | Lyn Corbray → Lyonel Corbray | affc-alayne-01 |
| Plans to corrupt / buy | 1 | Petyr Baelish → Benedar Belmore | affc-alayne-01 |
| Plans to befriend | 1 | Petyr Baelish → Symond Templeton | affc-alayne-01 |
| Plans to outlast / isolate | 1 | Petyr Baelish → Bronze Yohn Royce | affc-alayne-01 |
| Plans against | 1 | Petyr Baelish → Cersei Lannister | affc-alayne-01 |
| Visited / acquainted with | 1 | Bronze Yohn → Stark family (Winterfell) | affc-alayne-01 |
| Suspected of hastening death of | 1 | Gilwood Hunter → Lord Eon Hunter | affc-alayne-01 |
| Caretaker/surrogate mother to | 1 | Alayne → Robert Arryn | affc-alayne-02 |
| Clinging dependence on | 1 | Robert Arryn → Alayne | affc-alayne-02 |
| Manipulator/controller of | 1 | Petyr Baelish → Alayne | affc-alayne-02 |
| Obedience mixed with unease toward | 1 | Alayne → Petyr Baelish | affc-alayne-02 |
| Unaware/indifferent toward | 1 | Mya Stone → Lothor Brune | affc-alayne-02 |
| Warming but guarded toward | 1 | Alayne → Myranda Royce | affc-alayne-02 |
| Overrules/dismisses | 1 | Alayne → Maester Colemon | affc-alayne-02 |
| Brokered marriage for | 1 | Petyr Baelish → Lord Lyonel Corbray | affc-alayne-02 |
| Desired to marry | 1 | Myranda Royce → Harrold Hardyng | affc-alayne-02 |
| Complex memory of | 1 | Alayne/Sansa → The Hound | affc-alayne-02 |
| Plans the death of | 1 | Petyr Baelish → Robert Arryn | affc-alayne-02 |
| passenger / ward of | 1 | Arya → Ternesio Terys | affc-arya-01 |
| gives mercy to | 1 | Arya → Young man by the pool | affc-arya-01 |
| priest at / authority over | 1 | The kindly man → House of Black and White | affc-arya-01 |
| Language partner with | 1 | Arya → The waif | affc-arya-02 |
| Kitchen worker under | 1 | Arya → Umma | affc-arya-02 |
| Deep attachment to | 1 | Arya → Needle / Jon Snow | affc-arya-02 |
| Abandonment felt toward | 1 | Arya → Hot Pie, Gendry, Yoren, Lommy Greenhands, Harwin | affc-arya-02 |
| Memory of servitude under | 1 | Arya → Weese, Roose Bolton | affc-arya-02 |
| Testing/challenging | 1 | The kindly man → Arya | affc-arya-02 |
| Knowing despite secrecy | 1 | The kindly man → Arya | affc-arya-02 |
| Superior at lying game to | 1 | The waif → Arya | affc-arya-02 |
| Given everything to | 1 | The waif → The Many-Faced God | affc-arya-02 |
| Wolf-dream connection to | 1 | Arya → A wolf pack | affc-arya-02 |
| Trusted by / given mission by | 1 | Brienne → Jaime Lannister | affc-brienne-01 |
| Devoted to (dead) | 1 | Brienne → Renly Baratheon | affc-brienne-01 |
| Promised service to (dead) | 1 | Brienne → Lady Catelyn Stark | affc-brienne-01 |
| Boastful toward / patronizing to | 1 | Ser Creighton → Brienne | affc-brienne-01 |
| Suspicious of / accuses | 1 | Ser Illifer → Brienne | affc-brienne-01 |
| Rival hunter / competitor | 1 | Ser Shadrich → Brienne | affc-brienne-01 |
| Hired escort of | 1 | Ser Shadrich → Hibald | affc-brienne-01 |
| Debtor to | 1 | Ser Creighton → Naggle (innkeep) | affc-brienne-01 |
| Reciprocates hospitality to | 1 | Brienne → Ser Creighton, Ser Illifer | affc-brienne-01 |
| Helped to escape by (inferred) | 1 | Sansa Stark → Ser Dontos the Red | affc-brienne-01 |
| Showed courtesy to | 1 | Renly Baratheon → Brienne | affc-brienne-01 |
| Sworn service / loyalty beyond death | 1 | Brienne → Catelyn Stark | affc-brienne-02 |
| Complex emotional attachment | 1 | Brienne → Jaime Lannister | affc-brienne-02 |
| Quest target | 1 | Brienne → Sansa Stark | affc-brienne-02 |
| Suspicion then sympathy | 1 | Brienne → Podrick Payne | affc-brienne-02 |
| Wife (blamed for influencing) | 1 | Lady Serala (Lace Serpent) → Lord Denys Darklyn | affc-brienne-02 |
| Spared / protected | 1 | Barristan Selmy → Dontos Hollard | affc-brienne-02 |
| Former maid of | 1 | Brella → Sansa Stark | affc-brienne-02 |
| Rode with | 1 | Lord Rykker → Randyll Tarly | affc-brienne-02 |
| Informant to | 1 | Dwarf holy brother → Brienne | affc-brienne-02 |
| "Fooled a fool" | 1 | Nimble Dick → The fool at Maidenpool | affc-brienne-02 |
| mocking familiarity / unresolved guilt | 1 | Ser Hyle Hunt → Brienne | affc-brienne-03 |
| dominance / authority | 1 | Lord Randyll Tarly → Lord Mooton | affc-brienne-03 |
| conflicted memory of loathing and shared experience | 1 | Brienne → Ser Jaime Lannister | affc-brienne-03 |
| loyalty and gratitude | 1 | Brienne → Lady Catelyn Stark | affc-brienne-03 |
| mission devotion | 1 | Brienne → Sansa Stark | affc-brienne-03 |
| mercenary guide | 1 | Dick Crabb → Brienne | affc-brienne-03 |
| wary employer | 1 | Brienne → Dick Crabb | affc-brienne-03 |
| squire (former) | 1 | Podrick Payne → Tyrion Lannister | affc-brienne-03 |
| treated as servant, not son | 1 | Ser Cedric Payne → Podrick Payne | affc-brienne-03 |
| corrupting influence | 1 | Ser Lorimer the Belly → Podrick Payne | affc-brienne-03 |
| executioner | 1 | Lord Tywin Lannister → Ser Lorimer the Belly | affc-brienne-03 |
| took charge of | 1 | Ser Kevan Lannister → Podrick Payne | affc-brienne-03 |
| guides (for gold) | 1 | Nimble Dick → Brienne | affc-brienne-04 |
| ancestral pride in | 1 | Nimble Dick → Ser Clarence Crabb / House Crabb | affc-brienne-04 |
| sold map to | 1 | Nimble Dick → Shagwell, Timeon, Pyg | affc-brienne-04 |
| former members of | 1 | Shagwell, Timeon, Pyg → Brave Companions (Bloody Mummers) | affc-brienne-04 |
| follows on orders of | 1 | Hyle Hunt → Randyll Tarly | affc-brienne-04 |
| former enemy of/contempt for | 1 | Brienne → Hyle Hunt | affc-brienne-04 |
| reveres memory of | 1 | Brienne → Ser Goodwin | affc-brienne-04 |
| reportedly abducted | 1 | Sandor Clegane (the Hound) → Sansa Stark | affc-brienne-04 |
| Motivated by reward regarding | 1 | Hyle Hunt → Sansa Stark | affc-brienne-05 |
| Memory of past journey with | 1 | Brienne → Jaime | affc-brienne-05 |
| Haunted by kills of | 1 | Brienne → Shagwell, Timeon, Pyg | affc-brienne-05 |
| Pity for/moved by | 1 | Brienne → Broken men | affc-brienne-05 |
| Hunting/seeking to kill | 1 | Brienne → Sandor Clegane (the Hound) | affc-brienne-06 |
| Sworn protector / questing for | 1 | Brienne → Sansa Stark | affc-brienne-06 |
| Found, tended, and buried | 1 | Elder Brother → Sandor Clegane | affc-brienne-06 |
| Former knight who fought for | 1 | Elder Brother → Prince Rhaegar | affc-brienne-06 |
| Hated / dreamed of killing | 1 | Sandor Clegane → Gregor Clegane | affc-brienne-06 |
| Abducted / traveled with | 1 | Sandor Clegane → Arya Stark | affc-brienne-06 |
| Poisoned/wounded | 1 | Prince Oberyn → Gregor Clegane | affc-brienne-06 |
| Failed to protect | 1 | Ser Quincy Cox → People of Saltpans | affc-brienne-06 |
| Dueled / complex bond with | 1 | Brienne → Jaime (Lannister) | affc-brienne-06 |
| Bit the ear of | 1 | Brienne → Vargo Hoat | affc-brienne-06 |
| Former warhorse of | 1 | Driftwood (Stranger) → Sandor Clegane | affc-brienne-06 |
| Told Brienne about | 1 | Timeon → The Hound and Sansa/Arya | affc-brienne-06 |
| Former keeper of | 1 | Masha Heddle → The crossroads inn | affc-brienne-06 |
| Yearning/conflicted feelings toward | 1 | Brienne → Ser Jaime Lannister | affc-brienne-07 |
| Yearning for | 1 | Brienne → Lord Selwyn (father) / Tarth | affc-brienne-07 |
| Desires marriage with (mercenary) | 1 | Ser Hyle Hunt → Brienne | affc-brienne-07 |
| Fondness for memory of | 1 | Septon Meribald → Masha Heddle | affc-brienne-07 |
| Compassion toward | 1 | Septon Meribald → The orphan children | affc-brienne-07 |
| Suspicion/hostility toward | 1 | Gendry → Brienne's party (initially) | affc-brienne-07 |
| Worship of | 1 | Gendry → The Lord of Light (R'hllor) | affc-brienne-07 |
| Partnership/conflict with | 1 | Willow → Gendry | affc-brienne-07 |
| Recognition of kinship between | 1 | Brienne → Gendry and Renly / Robert Baratheon | affc-brienne-07 |
| Violent aggression toward | 1 | The man in the Hound's helm → Willow / Brienne | affc-brienne-07 |
| Savage attack on | 1 | Biter → Brienne | affc-brienne-07 |
| Sworn service to (past) | 1 | Brienne → Catelyn Stark | affc-brienne-08 |
| Quest for | 1 | Brienne → Sansa Stark | affc-brienne-08 |
| Demands death of | 1 | Lady Stoneheart → Jaime Lannister | affc-brienne-08 |
| Wears identity of | 1 | Lem → Sandor Clegane (The Hound) | affc-brienne-08 |
| Took helm from corpse of | 1 | Lem → Rorge | affc-brienne-08 |
| Healed | 1 | Jeyne Heddle → Brienne | affc-brienne-08 |
| Fellow captive with | 1 | Hyle Hunt → Brienne | affc-brienne-08 |
| Has hanged | 1 | Randyll Tarly → Brotherhood members | affc-brienne-08 |
| Has wife and daughter (lost) | 1 | Lem → — | affc-brienne-08 |
| Arranged marriage for | 1 | Brienne's father → Brienne | affc-brienne-08 |
| Begged for resurrection of | 1 | Harwin → Catelyn | affc-brienne-08 |
| Employer-employee | 1 | Cat/Arya → Brusco | affc-cat-of-the-canals-01 |
| Roommates / quasi-siblings | 1 | Cat/Arya → Talea, Brea | affc-cat-of-the-canals-01 |
| Student-teacher (service) | 1 | Cat/Arya → The kindly man | affc-cat-of-the-canals-01 |
| Student-teacher (poisons) | 1 | Cat/Arya → The waif | affc-cat-of-the-canals-01 |
| Killer | 1 | Cat/Arya → Dareon | affc-cat-of-the-canals-01 |
| Hostility / moral judgment | 1 | Cat/Arya → Dareon | affc-cat-of-the-canals-01 |
| Sympathy | 1 | Cat/Arya → Little Narbo | affc-cat-of-the-canals-01 |
| Complicated familiarity | 1 | Cat/Arya → The Sailor's Wife | affc-cat-of-the-canals-01 |
| Suppressed kinship | 1 | Cat/Arya → Lysa Arryn | affc-cat-of-the-canals-01 |
| Wolf-dreaming bond | 1 | Cat/Arya → Nymeria (implied) | affc-cat-of-the-canals-01 |
| Former partner | 1 | Tagganaro → Little Narbo | affc-cat-of-the-canals-01 |
| Devotion to lost husband | 1 | The Sailor's Wife → Her first husband | affc-cat-of-the-canals-01 |
| Employer | 1 | Merry → Lanna, Yna, Blushing Bethany, Sailor's Wife, Assadora | affc-cat-of-the-canals-01 |
| Victim | 1 | The waif → Her stepmother | affc-cat-of-the-canals-01 |
| Devoted | 1 | The waif → Her father | affc-cat-of-the-canals-01 |
| Conflict | 1 | Quence → Allaquo | affc-cat-of-the-canals-01 |
| Mother / protective | 1 | Cersei → Tommen | affc-cersei-01 |
| Early trust / patronage | 1 | Cersei → Qyburn | affc-cersei-01 |
| Service / opportunism | 1 | Qyburn → Cersei | affc-cersei-01 |
| Informant | 1 | Shortear → Cersei | affc-cersei-01 |
| Employed (sexual, denied by Cersei) | 1 | Tywin → Shae | affc-cersei-01 |
| Politically opposed to | 1 | Cersei → Mace Tyrell | affc-cersei-02 |
| Cultivating | 1 | Cersei → Taena Merryweather | affc-cersei-02 |
| Employing / cautiously trusting | 1 | Cersei → Qyburn | affc-cersei-02 |
| Vigil for | 1 | Jaime → Tywin (deceased) | affc-cersei-02 |
| Intimidated | 1 | Tywin (memory) → Lord Rykker | affc-cersei-02 |
| alienated from / contemptuous of | 1 | Cersei → Jaime | affc-cersei-03 |
| dutiful but dismissed by | 1 | Jaime → Cersei | affc-cersei-03 |
| suspicious of / betrayed by (believed) | 1 | Cersei → Senelle | affc-cersei-03 |
| cautious trust toward | 1 | Cersei → Lady Merryweather | affc-cersei-03 |
| critical of / disappointed in | 1 | Kevan → Cersei | affc-cersei-03 |
| tender toward / protective of | 1 | Margaery → Tommen | affc-cersei-03 |
| fascinated by / trusting of | 1 | Tommen → Margaery | affc-cersei-03 |
| very close to (resembles) | 1 | Loras Tyrell → Margaery Tyrell | affc-cersei-03 |
| notices / attracted to | 1 | Cersei → Aurane Waters | affc-cersei-03 |
| unexplained conversation with | 1 | Kevan → Ser Garlan Tyrell | affc-cersei-03 |
| socializing with | 1 | Elinor → Aurane Waters | affc-cersei-03 |
| dancing with | 1 | Megga → Ser Tallad the Tall | affc-cersei-03 |
| serving as intermediaries for | 1 | Alla, Elinor, Megga → Margaery | affc-cersei-03 |
| slides arm through / keeps company with | 1 | Cersei → Ser Osmund Kettleblack | affc-cersei-03 |
| nostalgic bitterness toward (memory) | 1 | Cersei → Robert Baratheon | affc-cersei-03 |
| testified against | 1 | Lady Merryweather → Tyrion Lannister | affc-cersei-03 |
| uses/controls | 1 | Cersei → Qyburn | affc-cersei-04 |
| uses as hostage | 1 | Cersei → Ser Harys Swyft | affc-cersei-04 |
| sexual manipulation of | 1 | Cersei → Ser Osney Kettleblack | affc-cersei-04 |
| growing intimacy with | 1 | Cersei → Taena Merryweather | affc-cersei-04 |
| rivalry/comparison with | 1 | Cersei → Jaime Lannister | affc-cersei-04 |
| attraction/assessment of | 1 | Cersei → Aurane Waters | affc-cersei-04 |
| amusement toward | 1 | Cersei → Lord Gyles Rosby | affc-cersei-04 |
| daughter married to | 1 | Ser Harys Swyft → Kevan Lannister | affc-cersei-04 |
| teases | 1 | Megga (Tyrell cousin) → Ser Osney Kettleblack | affc-cersei-04 |
| kind to | 1 | Margaery Tyrell → Ser Osney Kettleblack | affc-cersei-04 |
| hit | 1 | Robert Baratheon → Cersei | affc-cersei-04 |
| lies to | 1 | Cersei → Taena Merryweather | affc-cersei-04 |
| Mother, controlling | 1 | Cersei → Tommen | affc-cersei-05 |
| Son, increasingly defiant | 1 | Tommen → Cersei | affc-cersei-05 |
| Influences/manipulates | 1 | Margaery → Tommen | affc-cersei-05 |
| Antagonist/rival | 1 | Cersei → Margaery | affc-cersei-05 |
| Fails to seduce | 1 | Osney Kettleblack → Margaery | affc-cersei-05 |
| Flirtatious but guarded with | 1 | Margaery → Osney Kettleblack | affc-cersei-05 |
| Considers a fool | 1 | Cersei → Osmund Kettleblack | affc-cersei-05 |
| Enabling/using | 1 | Cersei → Qyburn | affc-cersei-05 |
| Increasingly hostile toward | 1 | Cersei → Jaime | affc-cersei-05 |
| Still attracted to | 1 | Jaime → Cersei | affc-cersei-05 |
| Uses attraction against | 1 | Cersei → Jaime | affc-cersei-05 |
| Nostalgic longing for | 1 | Cersei → Rhaegar Targaryen | affc-cersei-05 |
| Father, promised | 1 | Tywin → Cersei | affc-cersei-05 |
| Considers expendable | 1 | Cersei → Senelle | affc-cersei-05 |
| Uses as spy and confidante | 1 | Cersei → Taena Merryweather | affc-cersei-06 |
| Hostile rivalry (one-sided overt) | 1 | Cersei → Margaery Tyrell | affc-cersei-06 |
| Political negotiation / mutual wariness | 1 | Cersei → The High Septon | affc-cersei-06 |
| Protective / controlling toward | 1 | Cersei → Tommen Baratheon | affc-cersei-06 |
| Sisterly devotion (presented) | 1 | Margaery → Ser Loras Tyrell | affc-cersei-06 |
| Suspicion about | 1 | Cersei → Loras and Margaery | affc-cersei-06 |
| Disciplinary authority over | 1 | High Septon → Septon Torbert | affc-cersei-06 |
| Flatters and defers to | 1 | Taena Merryweather → Cersei | affc-cersei-06 |
| Cultivates goodwill with | 1 | Margaery → Smallfolk | affc-cersei-06 |
| Rivalry/contempt toward | 1 | Cersei → Margaery | affc-cersei-07 |
| Calculating manipulation of | 1 | Cersei → Loras Tyrell | affc-cersei-07 |
| Reliance on/trust in | 1 | Cersei → Qyburn | affc-cersei-07 |
| Mild approval of | 1 | Cersei → Aurane Waters | affc-cersei-07 |
| Fury/contempt toward | 1 | Cersei → Falyse Stokeworth | affc-cersei-07 |
| Longing/fixation on | 1 | Cersei → Jaime Lannister | affc-cersei-07 |
| Nostalgic desire for | 1 | Cersei → Rhaegar Targaryen | affc-cersei-07 |
| Determination to destroy | 1 | Cersei → Bronn | affc-cersei-07 |
| Dominates/threatens | 1 | Bronn → Falyse | affc-cersei-07 |
| Uses/manipulates | 1 | Cersei → Aurane Waters | affc-cersei-08 |
| Concealed hostility toward | 1 | Cersei → Margaery Tyrell | affc-cersei-08 |
| Haunted by | 1 | Cersei → Maggy the Frog | affc-cersei-08 |
| Fixated on destroying | 1 | Cersei → Tyrion Lannister | affc-cersei-08 |
| Displeasure toward | 1 | Cersei → Lancel Lannister | affc-cersei-08 |
| Expected to wed | 1 | Young Cersei → Rhaegar Targaryen | affc-cersei-08 |
| Wanted to marry | 1 | Melara Hetherspoon → Jaime Lannister | affc-cersei-08 |
| Indifferent to fate of | 1 | Cersei → Falyse Stokeworth | affc-cersei-08 |
| dominates/intimidates | 1 | Cersei → Pycelle | affc-cersei-09 |
| plots to destroy | 1 | Cersei → Margaery Tyrell | affc-cersei-09 |
| frames and brutalizes | 1 | Cersei → Blue Bard (Wat) | affc-cersei-09 |
| sexual manipulation | 1 | Cersei → Osney Kettleblack | affc-cersei-09 |
| invokes/measures self against | 1 | Cersei → Tywin Lannister | affc-cersei-09 |
| invokes past loyalty to | 1 | Pycelle → Tywin Lannister | affc-cersei-09 |
| volunteers to manipulate | 1 | Taena → Alla Tyrell | affc-cersei-09 |
| considers granting lands to | 1 | Cersei → Aurane Waters | affc-cersei-09 |
| performed for | 1 | Blue Bard → Margaery | affc-cersei-09 |
| Desperate need for | 1 | Cersei → Jaime Lannister | affc-cersei-10 |
| Take control from | 1 | Harys Swyft and Pycelle → Cersei | affc-cersei-10 |
| freed from cell (and bears guilt for consequences) | 1 | Jaime → Tyrion | affc-jaime-01 |
| forced cooperation / threatened | 1 | Jaime → Varys | affc-jaime-01 |
| accused Cersei to | 1 | Tyrion → Jaime | affc-jaime-01 |
| asked to serve as Hand / refused by | 1 | Cersei → Jaime | affc-jaime-01 |
| ordered killing of turnkeys through | 1 | Cersei → Kettleblacks (Osmund, Osney, Osfryd) | affc-jaime-01 |
| blamed for dungeon failures | 1 | Cersei → Ser Ilyn Payne | affc-jaime-01 |
| accused of sleeping with | 1 | Cersei → Lancel, Osmund Kettleblack, Moon Boy | affc-jaime-01 |
| refused to serve / knows incest secret | 1 | Kevan → Cersei, Jaime | affc-jaime-01 |
| political advisor to | 1 | Jaime → Cersei | affc-jaime-01 |
| compared to father by | 1 | Jaime → Cersei | affc-jaime-01 |
| father figure / protective toward | 1 | Jaime → Tommen | affc-jaime-01 |
| intimidated/harmed by (implied) | 1 | Tommen → Joffrey | affc-jaime-01 |
| harsh mother to | 1 | Cersei → Tommen | affc-jaime-01 |
| thinks of with tenderness / almost prays for | 1 | Jaime → Brienne of Tarth | affc-jaime-01 |
| confided in / trusted | 1 | Rhaegar → Jaime | affc-jaime-01 |
| revulsion toward / visualizes infidelity | 1 | Jaime → Osmund Kettleblack | affc-jaime-01 |
| political pawn (in Jaime's strategy) | 1 | Mace Tyrell → Cersei | affc-jaime-01 |
| clever and pretty (Jaime's assessment) | 1 | Margaery → Tommen | affc-jaime-01 |
| proud of lineage / boastful | 1 | Longwaters → Jaime | affc-jaime-01 |
| disappeared (implied to be Varys) | 1 | Rugen → Varys | affc-jaime-01 |
| Twin sibling of (estranged) | 1 | Jaime → Cersei Lannister | affc-jaime-02 |
| Superior officer of | 1 | Jaime → Ser Loras Tyrell | affc-jaime-02 |
| Refuses to serve | 1 | Ser Kevan → Cersei Lannister | affc-jaime-02 |
| Knows secret of | 1 | Ser Kevan → Jaime and Cersei | affc-jaime-02 |
| Paranoid toward / politically isolated from | 1 | Cersei → Ser Kevan Lannister | affc-jaime-02 |
| Uses as double agent | 1 | Cersei → Lady Taena Merryweather | affc-jaime-02 |
| Enraged at | 1 | Cersei → Bronn | affc-jaime-02 |
| Drinking heavily, compared to | 1 | Cersei → Robert Baratheon | affc-jaime-02 |
| Compared to (by Jaime) | 1 | Cersei → Aerys II Targaryen | affc-jaime-02 |
| Stood guard with | 1 | Jaime → Jon Darry | affc-jaime-02 |
| Under influence of | 1 | Lancel → Unnamed septons | affc-jaime-02 |
| Lord of / served by | 1 | Tywin Lannister → Lords of the west | affc-jaime-02 |
| Secret sparring partner / developing bond | 1 | Jaime → Ser Ilyn Payne | affc-jaime-03 |
| Boyhood friends | 1 | Jaime → Ser Addam Marbrand | affc-jaime-03 |
| Lost tongue on orders of | 1 | Ser Ilyn Payne → Aerys II Targaryen | affc-jaime-03 |
| Devout follower | 1 | Ser Bonifer Hasty → Faith of the Seven | affc-jaime-03 |
| Tortured / killed | 1 | Gregor Clegane → Vargo Hoat | affc-jaime-03 |
| Castellan appointed by Jaime at | 1 | Ser Bonifer Hasty → Harrenhal | affc-jaime-03 |
| Jests about kinship with | 1 | Strongboar (Ser Lyle) → Ser Roger Hogg | affc-jaime-03 |
| Likely recommended | 1 | Orton Merryweather → Ser Bonifer Hasty | affc-jaime-03 |
| Husband (unconsummated) | 1 | Lancel → Lady Amerei | affc-jaime-04 |
| Daughter | 1 | Lady Amerei → Lady Mariya | affc-jaime-04 |
| Confessed sins to | 1 | Lancel → The (dead) High Septon | affc-jaime-04 |
| Complicity in death of | 1 | Lancel → Robert Baratheon | affc-jaime-04 |
| Quarreled with | 1 | Lancel → Ser Kevan | affc-jaime-04 |
| Increasingly disillusioned with | 1 | Jaime → Cersei | affc-jaime-04 |
| Uses as confessor/sparring partner | 1 | Jaime → Ser Ilyn Payne | affc-jaime-04 |
| Boastful rivalry / volunteering | 1 | Strongboar → The Hound / Lord Beric | affc-jaime-04 |
| Witness/informant | 1 | Ser Arwood Frey → The company | affc-jaime-04 |
| Former squire together with | 1 | Jaime → Merrett Frey | affc-jaime-04 |
| Nightly sparring partner | 1 | Jaime → Ser Ilyn Payne | affc-jaime-05 |
| Dominates/dismisses | 1 | Genna → Emmon Frey | affc-jaime-05 |
| Higher regard for | 1 | Genna → Tyrion Lannister | affc-jaime-05 |
| Deference | 1 | Ser Daven → Kevan Lannister | affc-jaime-05 |
| Growing distrust/disgust | 1 | Jaime → Cersei | affc-jaime-05 |
| Conflicted obligation | 1 | Jaime → Catelyn Stark | affc-jaime-05 |
| Pity | 1 | Jaime → Edmure Tully | affc-jaime-05 |
| Vowed vengeance against | 1 | Daven → Karstark's killer | affc-jaime-05 |
| Worried about | 1 | Genna → Jaime | affc-jaime-05 |
| wariness toward | 1 | Jaime Lannister → Walder Rivers | affc-jaime-06 |
| father desperate for | 1 | Lord Piper → Marq Piper | affc-jaime-06 |
| hostage-holder, threatening | 1 | Edwyn Frey → Lord Piper / Marq Piper | affc-jaime-06 |
| subservient husband | 1 | Lord Emmon Frey → Lady Genna Lannister | affc-jaime-06 |
| complicated guilt toward | 1 | Jaime Lannister → Catelyn Stark | affc-jaime-06 |
| comparing self to | 1 | Jaime Lannister → Tywin Lannister | affc-jaime-06 |
| dominates/manages | 1 | Genna Lannister → Emmon Frey | affc-jaime-07 |
| interrogates/threatens | 1 | Jaime → Edmure Tully | affc-jaime-07 |
| sparring partner/confidant | 1 | Jaime → Ser Ilyn Payne | affc-jaime-07 |
| distancing from | 1 | Jaime → Cersei | affc-jaime-07 |
| fatherly concern for | 1 | Jaime → Tommen | affc-jaime-07 |
| ingratiates with | 1 | Tom of Sevenstreams → Jaime | affc-jaime-07 |
| mother to | 1 | Dream woman (Joanna) → Jaime | affc-jaime-07 |
| eager to fight | 1 | Strongboar → The Hound / Beric Dondarrion | affc-jaime-07 |
| Calm authority among | 1 | Alleras → The group | affc-prologue |
| Accused | 1 | Maester Gormon → Pate | affc-prologue |
| Mother, controls access to | 1 | Emma → Rosey | affc-prologue |
| Confused about identity of | 1 | Walgrave → Pate / Cressen | affc-prologue |
| Romantic feelings toward | 1 | Sam → Gilly | affc-samwell-01 |
| Cares for / assists | 1 | Sam → Maester Aemon | affc-samwell-01 |
| Feels distance from | 1 | Grenn → Jon Snow | affc-samwell-01 |
| Keeps secret from | 1 | Sam → Jon Snow | affc-samwell-01 |
| Traumatized | 1 | Lord Randyll Tarly → Sam | affc-samwell-01 |
| tries to comfort | 1 | Samwell Tarly → Gilly | affc-samwell-02 |
| physically attracted to | 1 | Samwell Tarly → Gilly | affc-samwell-02 |
| entertains | 1 | Dareon → Blackbird's oarsmen | affc-samwell-02 |
| drinks heavily | 1 | Dareon → (firewine) | affc-samwell-02 |
| traveled with | 1 | Maester Aemon → Brynden Rivers (Bloodraven) | affc-samwell-02 |
| escorted by | 1 | Maester Aemon → Ser Duncan | affc-samwell-02 |
| switched babies / forced | 1 | Jon Snow → Gilly | affc-samwell-02 |
| abused/shamed | 1 | Randyll Tarly → Samwell Tarly | affc-samwell-02 |
| cares for / serves | 1 | Sam → Maester Aemon | affc-samwell-03 |
| abandons / betrays | 1 | Dareon → Night's Watch | affc-samwell-03 |
| neglects | 1 | Dareon → Sam, Gilly, Aemon | affc-samwell-03 |
| threaten / mock | 1 | Terro & friend → Sam | affc-samwell-03 |
| ordered/arranged | 1 | Jon Snow → Baby swap (inferred) | affc-samwell-03 |
| "marries" | 1 | Dareon → The Sailor's Wife | affc-samwell-03 |
| punches / fights | 1 | Sam → Dareon | affc-samwell-03 |
| guilt-ridden intimacy | 1 | Sam → Gilly | affc-samwell-04 |
| believes in / advocates for | 1 | Aemon → Daenerys Targaryen | affc-samwell-04 |
| complicated resentment | 1 | Sam → Lord Randyll Tarly (his father) | affc-samwell-04 |
| self-comparison, guilt | 1 | Sam → Dareon | affc-samwell-04 |
| reverence for | 1 | Summer Islanders (crew) → The elderly / Maester Aemon | affc-samwell-04 |
| Protective/romantic attachment to | 1 | Sam → Gilly | affc-samwell-05 |
| Rejection of | 1 | Lord Randyll Tarly → Sam | affc-samwell-05 |
| Deep loyalty to | 1 | Sam → Jon Snow | affc-samwell-05 |
| Agent/loyal servant of | 1 | Alleras → Archmaester Marwyn | affc-samwell-05 |
| General contempt toward | 1 | Leo Tyrell → Other novices/acolytes | affc-samwell-05 |
| Urgency/mission toward | 1 | Archmaester Marwyn → Daenerys Targaryen | affc-samwell-05 |
| Instinctive dislike of | 1 | Sam → Pate | affc-samwell-05 |
| Helpful/accommodating toward | 1 | Pate → Sam | affc-samwell-05 |
| Dependent on / conflicted about | 1 | Sansa → Petyr Baelish | affc-sansa-01 |
| Protector / manipulator of | 1 | Petyr Baelish → Sansa | affc-sansa-01 |
| Coerced confessor for | 1 | Marillion → Petyr Baelish | affc-sansa-01 |
| Attached to / dependent on | 1 | Robert Arryn → Sansa | affc-sansa-01 |
| Guard/protector of | 1 | Ser Lothor Brune → Sansa | affc-sansa-01 |
| Gaoler / torturer of | 1 | Mord → Marillion | affc-sansa-01 |
| Favored | 1 | Lysa Arryn → Marillion | affc-sansa-01 |
| Watches via | 1 | Petyr → Kettleblack / Brune | affc-sansa-01 |
| Pities despite herself | 1 | Sansa → Marillion | affc-sansa-01 |
| Blurs identity of | 1 | Petyr → Sansa / Catelyn | affc-sansa-01 |
| Demands war from | 1 | Obara Sand → Prince Doran | affc-the-captain-of-guards-01 |
| Demands assassination from | 1 | Nymeria Sand → Prince Doran | affc-the-captain-of-guards-01 |
| Proposes crowning Myrcella to | 1 | Tyene Sand → Prince Doran | affc-the-captain-of-guards-01 |
| Resists/deflects | 1 | Prince Doran → All three Sand Snakes | affc-the-captain-of-guards-01 |
| Orders arrest of | 1 | Prince Doran → Sand Snakes (all eight) | affc-the-captain-of-guards-01 |
| Anticipates fighting | 1 | Areo Hotah → Ser Arys Oakheart | affc-the-captain-of-guards-01 |
| Attends/guards | 1 | Ser Arys Oakheart → Princess Myrcella | affc-the-captain-of-guards-01 |
| Took/claimed | 1 | Oberyn Martell → Obara Sand | affc-the-captain-of-guards-01 |
| Mother was from | 1 | Nymeria Sand → Volantis (noble blood) | affc-the-captain-of-guards-01 |
| Mother was | 1 | Tyene Sand → A septa | affc-the-captain-of-guards-01 |
| Sold to | 1 | Hotah → Bearded priests of Norvos | affc-the-captain-of-guards-01 |
| "Wed" to | 1 | Hotah → His longaxe | affc-the-captain-of-guards-01 |
| Supports as king | 1 | Aeron Greyjoy → Victarion Greyjoy | affc-the-drowned-man-01 |
| Champion of / supporter of | 1 | Tristifer Botley → Asha Greyjoy | affc-the-drowned-man-01 |
| Has grandsons including | 1 | Erik Ironmaker → Thormor | affc-the-drowned-man-01 |
| Married | 1 | The Grey King → A mermaid wife | affc-the-drowned-man-01 |
| Challenges | 1 | Asha Greyjoy → Erik Ironmaker | affc-the-drowned-man-01 |
| Lord Captain of | 1 | Victarion → Iron Fleet | affc-the-iron-captain-01 |
| Impregnated wife of | 1 | Euron → Victarion | affc-the-iron-captain-01 |
| Drowned | 1 | Euron → Sawane Botley | affc-the-iron-captain-01 |
| Political rival / enmity | 1 | Asha Greyjoy → Euron Greyjoy (Crow's Eye) | affc-the-krakens-daughter-01 |
| Designated successor | 1 | Lord Rodrik Harlaw → Ser Harras Harlaw (the Knight) | affc-the-krakens-daughter-01 |
| Dispossessed lord | 1 | Tristifer Botley → Euron Greyjoy | affc-the-krakens-daughter-01 |
| Buying loyalty | 1 | Euron Greyjoy → Various lords and captains | affc-the-krakens-daughter-01 |
| Former guardian | 1 | Baelor Blacktyde → Tristifer Botley | affc-the-krakens-daughter-01 |
| Suitor (via daughter) | 1 | Hotho Harlaw → Lord Rodrik Harlaw | affc-the-krakens-daughter-01 |
| husband of (estranged) | 1 | Prince Doran Martell → Lady Mellario | affc-the-princess-in-the-tower-01 |
| guardian/ward of | 1 | Prince Doran Martell → Myrcella Baratheon | affc-the-princess-in-the-tower-01 |
| shield of (formerly) | 1 | Areo Hotah → Lady Mellario | affc-the-princess-in-the-tower-01 |
| escaped from | 1 | Darkstar / Ser Gerold Dayne → Areo Hotah | affc-the-princess-in-the-tower-01 |
| formerly bedded | 1 | Garin → Cedra | affc-the-princess-in-the-tower-01 |
| sought to marry | 1 | Daemon Sand → Arianne Martell | affc-the-princess-in-the-tower-01 |
| natural daughter of | 1 | Ellaria Sand → Harmen Uller | affc-the-princess-in-the-tower-01 |
| historical enemies of | 1 | House Fowler → House Yronwood | affc-the-princess-in-the-tower-01 |
| friends of | 1 | Fowler twins (Jeyne & Jennelyn) → Nymeria Sand (Nym) | affc-the-princess-in-the-tower-01 |
| bedmaid of (formerly) | 1 | Belandra → Lady Mellario | affc-the-princess-in-the-tower-01 |
| childhood friends (the company of five) | 1 | Arianne Martell → Tyene, Garin, Drey, Spotted Sylva | affc-the-princess-in-the-tower-01 |
| refused suitor | 1 | Arianne Martell → Lord Renly Baratheon | affc-the-princess-in-the-tower-01 |
| never met (blocked by Doran) | 1 | Arianne Martell → Willas Tyrell | affc-the-princess-in-the-tower-01 |
| caught and returned | 1 | Prince Oberyn → Arianne and Tyene | affc-the-princess-in-the-tower-01 |
| childhood friend of | 1 | Frynne → Arianne | affc-the-princess-in-the-tower-01 |
| Priest/prophet of | 1 | Aeron Greyjoy → Drowned God | affc-the-prophet-01 |
| Scorned by | 1 | Aeron Greyjoy → Balon Greyjoy | affc-the-prophet-01 |
| Favored successor | 1 | Balon Greyjoy → Asha Greyjoy | affc-the-prophet-01 |
| Banished | 1 | Balon Greyjoy → Euron Greyjoy | affc-the-prophet-01 |
| Claimed | 1 | Euron Greyjoy → Seastone Chair | affc-the-prophet-01 |
| Married (first wife) | 1 | Quellon Greyjoy → Woman of the Stonetrees | affc-the-prophet-01 |
| Married (second wife) | 1 | Quellon Greyjoy → Sunderly of Saltcliffe | affc-the-prophet-01 |
| Married (third wife) | 1 | Quellon Greyjoy → Piper of Pinkmaiden Castle | affc-the-prophet-01 |
| Punished (mutilated) | 1 | Balon Greyjoy → Green-land maester | affc-the-prophet-01 |
| Sailed with | 1 | Dagmer Cleftjaw → Young Balon | affc-the-prophet-01 |
| Milk siblings / lifelong companions | 1 | Arianne Martell → Garin | affc-the-queenmaker-01 |
| Dearest friends | 1 | Arianne Martell → Drey, Spotted Sylva | affc-the-queenmaker-01 |
| Sexual attraction / wariness | 1 | Arianne Martell → Darkstar | affc-the-queenmaker-01 |
| Rivalry / resentment | 1 | Arianne Martell → Quentyn Martell | affc-the-queenmaker-01 |
| Suggested romantic interest | 1 | Darkstar → Arianne Martell | affc-the-queenmaker-01 |
| Jealousy | 1 | Darkstar → Arthur Dayne | affc-the-queenmaker-01 |
| Devotion / loyalty | 1 | Ser Arys Oakheart → Arianne Martell | affc-the-queenmaker-01 |
| Protective duty | 1 | Ser Arys Oakheart → Princess Myrcella | affc-the-queenmaker-01 |
| Sent as ward (blood debt) | 1 | Doran Martell → Quentyn Martell → Lord Ormond Yronwood | affc-the-queenmaker-01 |
| Anger / estrangement | 1 | Lady Mellario → Doran Martell | affc-the-queenmaker-01 |
| Decoy / distant kin | 1 | Rosamund → Myrcella Baratheon | affc-the-queenmaker-01 |
| Possessor / complicated feelings | 1 | Victarion → The dusky woman | affc-the-reaver-01 |
| King, manipulator | 1 | Euron → Victarion | affc-the-reaver-01 |
| Oppressor | 1 | Euron → Lord Hewett | affc-the-reaver-01 |
| Sexual predator | 1 | Euron → Falia Flowers | affc-the-reaver-01 |
| Executed | 1 | Euron → Baelor Blacktyde | affc-the-reaver-01 |
| King, strategic gift-giver | 1 | Euron → Ser Harras, Andrik, Volmark, Nute | affc-the-reaver-01 |
| Political opponent | 1 | Rodrik Harlaw → Euron | affc-the-reaver-01 |
| Dismissive | 1 | Nute → Rodrik Harlaw | affc-the-reaver-01 |
| Spiritual opposition | 1 | Aeron → Euron | affc-the-reaver-01 |
| Boyhood friend | 1 | Ser Harras Harlaw → Rodrik Greyjoy | affc-the-reaver-01 |
| Descendant through mother | 1 | Maron Volmark → Black Harren | affc-the-reaver-01 |
| Rapist | 1 | Left-Hand Lucas Codd → Lord Hewett's daughter | affc-the-reaver-01 |
| Captured/enslaved | 1 | Euron → Four Qartheen warlocks | affc-the-reaver-01 |
| Close as sisters with | 1 | Arianne Martell → Tyene Sand | affc-the-soiled-knight-01 |
| Father of, possibly disinheriting | 1 | Doran Martell → Arianne Martell | affc-the-soiled-knight-01 |
| Ashamed of serving | 1 | Arys Oakheart → Joffrey Baratheon | affc-the-soiled-knight-01 |
| Compared favorably to | 1 | Myrcella Baratheon → Tommen Baratheon | affc-the-soiled-knight-01 |
| Parallel drawn with | 1 | Cersei Lannister / Robert Baratheon → Myrcella / Trystane | affc-the-soiled-knight-01 |
| Terrorized by / enslaved to | 1 | Theon → Ramsay Bolton | adwd-a-ghost-in-winterfell-01 |
| Interrogated by / subject of | 1 | Theon → Roose Bolton | adwd-a-ghost-in-winterfell-01 |
| Threaten then recruit | 1 | Holly/Rowan → Theon | adwd-a-ghost-in-winterfell-01 |
| Held by loyalty to | 1 | Northern lords → "The girl" (fake Arya) | adwd-a-ghost-in-winterfell-01 |
| Haunted by guilt toward | 1 | Theon → Miller's wife and sons, Mikken, Farlen | adwd-a-ghost-in-winterfell-01 |
| reassures | 1 | Jojen → Meera | adwd-bran-01 |
| guides / protects | 1 | Coldhands → Bran | adwd-bran-01 |
| hungry for / restrained from | 1 | Summer → The elk | adwd-bran-01 |
| hopes for reconnection with | 1 | Bran → Shaggydog, Nymeria, Ghost | adwd-bran-01 |
| recalls stories from | 1 | Bran → Old Nan | adwd-bran-01 |
| was saved by | 1 | Sam → Coldhands | adwd-bran-01 |
| protective caretaker of | 1 | Meera Reed → Jojen Reed | adwd-bran-02 |
| guide/protector of | 1 | Coldhands → Bran and company | adwd-bran-02 |
| rescuer/guide of | 1 | Leaf (child of the forest) → Bran and company | adwd-bran-02 |
| has been watching | 1 | The Greenseer → Bran | adwd-bran-02 |
| formerly a member of | 1 | The Greenseer → Night's Watch | adwd-bran-02 |
| excluded from cave by | 1 | Coldhands → The cave's wards | adwd-bran-02 |
| watched | 1 | The Greenseer → Bran's lord father (Ned Stark) | adwd-bran-02 |
| Growing bitterness about | 1 | Meera → Their journey | adwd-bran-03 |
| Resignation to | 1 | Jojen → His fate | adwd-bran-03 |
| Merged with / dependent on | 1 | Lord Brynden → Weirwood tree | adwd-bran-03 |
| Haunted by memories of | 1 | Lord Brynden → A brother he loved, a brother he hated, a woman he desired | adwd-bran-03 |
| Guardian / guide to | 1 | Leaf → Bran and companions | adwd-bran-03 |
| Serve / sustain | 1 | Singers → Lord Brynden | adwd-bran-03 |
| accuser of | 1 | Lancel Lannister → Cersei | adwd-cersei-01 |
| Lord Regent for | 1 | Ser Kevan → Tommen Baratheon | adwd-cersei-01 |
| in custody of | 1 | Margaery Tyrell → Randyll Tarly | adwd-cersei-01 |
| with | 1 | Margaery Tyrell → Tommen Baratheon | adwd-cersei-01 |
| defended | 1 | Arys Oakheart → Myrcella Baratheon | adwd-cersei-01 |
| went off with | 1 | Jaime Lannister → Brienne of Tarth | adwd-cersei-01 |
| holds prisoners for | 1 | Qyburn → Cersei | adwd-cersei-01 |
| Mother desperate for | 1 | Cersei → Tommen | adwd-cersei-02 |
| Mother (bereaved) of | 1 | Cersei → Joffrey | adwd-cersei-02 |
| Feared / hated | 1 | Cersei → Tyrion | adwd-cersei-02 |
| Humiliated / expelled | 1 | Tywin → Tytos's mistress | adwd-cersei-02 |
| Haunted by prophecy of | 1 | Cersei → Maggy the Frog | adwd-cersei-02 |
| Guilt/unease toward | 1 | Cersei → Melara Hetherspoon | adwd-cersei-02 |
| Disobeyed plan of | 1 | Joffrey → Cersei (and Varys, Littlefinger) | adwd-cersei-02 |
| wary reliance on | 1 | Daenerys → Skahaz mo Kandaq | adwd-daenerys-01 |
| politically assessing | 1 | Daenerys → Hizdahr zo Loraq | adwd-daenerys-01 |
| petitions | 1 | Hizdahr zo Loraq → Daenerys | adwd-daenerys-01 |
| romantic desire for | 1 | Daenerys → Daario Naharis | adwd-daenerys-02 |
| maternal/protective of | 1 | Daenerys → Missandei | adwd-daenerys-02 |
| devotion to | 1 | Missandei → Daenerys | adwd-daenerys-02 |
| relies on / trusts | 1 | Daenerys → Skahaz mo Kandaq | adwd-daenerys-02 |
| conflicted authority over | 1 | Daenerys → Rhaegal, Viserion | adwd-daenerys-02 |
| persistent petitioner to | 1 | Hizdahr zo Loraq → Daenerys | adwd-daenerys-02 |
| cryptic guide to | 1 | Quaithe → Daenerys | adwd-daenerys-02 |
| guilt/anguish over | 1 | Daenerys → Hazzea | adwd-daenerys-02 |
| Desires/seeks to manipulate | 1 | Xaro → Daenerys | adwd-daenerys-03 |
| Desires romantically | 1 | Daenerys → Daario Naharis | adwd-daenerys-03 |
| Devoted to (as queen) | 1 | Barristan → Daenerys | adwd-daenerys-03 |
| Remembers with mixture of contempt and pity | 1 | Daenerys → Viserys | adwd-daenerys-03 |
| Desperate supplicant turned hostile | 1 | Lord Ghael → Daenerys | adwd-daenerys-03 |
| Eager to serve/sail | 1 | Groleo → Daenerys | adwd-daenerys-03 |
| Responsible for/duty toward | 1 | Daenerys → People of Meereen | adwd-daenerys-03 |
| Feels guilty about | 1 | Daenerys → Hazzea | adwd-daenerys-03 |
| Sibling | 1 | Qezza → Grazhar | adwd-daenerys-04 |
| Political advisor | 1 | Galazza Galare → Daenerys | adwd-daenerys-04 |
| Suitor/proposed consort | 1 | Hizdahr zo Loraq → Daenerys | adwd-daenerys-04 |
| Aggressive advisor (in tension with Dany) | 1 | Skahaz mo Kandaq → Daenerys | adwd-daenerys-04 |
| Sexually desires / is drawn to | 1 | Daenerys → Daario Naharis | adwd-daenerys-04 |
| Desires / courts | 1 | Daario Naharis → Daenerys | adwd-daenerys-04 |
| Loyal protector / disapproving advisor | 1 | Ser Barristan → Daenerys | adwd-daenerys-04 |
| Forced marriage (no fondness) | 1 | Aerys II → Rhaella | adwd-daenerys-04 |
| Political alignment with | 1 | Hizdahr → Galazza Galare | adwd-daenerys-04 |
| Feels unsafe around (emotionally) | 1 | Daenerys → Daario | adwd-daenerys-04 |
| Rival/opposed faction to | 1 | Skahaz (Kandaq) → Hizdahr (Loraq) | adwd-daenerys-04 |
| Identifies with (reluctantly) | 1 | Daenerys → Daario | adwd-daenerys-04 |
| Feels comfort/safety from memory of | 1 | Daenerys → Drogo | adwd-daenerys-04 |
| compares favorably | 1 | Ser Barristan → Daenerys to Rhaegar | adwd-daenerys-05 |
| accusing gaze toward | 1 | Astapori weaver → Daenerys | adwd-daenerys-05 |
| sent away (political sacrifice) | 1 | Daenerys → Daario Naharis | adwd-daenerys-05 |
| desires / becomes lovers with | 1 | Daenerys → Daario Naharis | adwd-daenerys-06 |
| thinks of with pain/confusion | 1 | Daenerys → Ser Jorah Mormont | adwd-daenerys-06 |
| rivals / argues with | 1 | Irri → Jhiqui | adwd-daenerys-06 |
| negotiates on behalf of | 1 | Hizdahr → Yunkai | adwd-daenerys-06 |
| Jealous of / hostile toward | 1 | Daario → Hizdahr zo Loraq | adwd-daenerys-07 |
| Unattracted to | 1 | Daenerys → Quentyn Martell | adwd-daenerys-07 |
| Supports Ghiscari match | 1 | Skahaz mo Kandaq → Hizdahr/Meereen | adwd-daenerys-07 |
| Devoted advisor to | 1 | Missandei → Daenerys | adwd-daenerys-07 |
| Bought by / received payment from | 1 | Daario → Dornishmen (implied) | adwd-daenerys-07 |
| In service of | 1 | Strong Belwas → Daenerys | adwd-daenerys-07 |
| desires / tries to renounce | 1 | Daenerys → Daario Naharis | adwd-daenerys-08 |
| is comforted by | 1 | Daenerys → Missandei | adwd-daenerys-08 |
| removed from power | 1 | Hizdahr zo Loraq → Skahaz mo Kandaq (Shavepate) | adwd-daenerys-08 |
| furious with | 1 | Daario Naharis → Quentyn's group | adwd-daenerys-08 |
| blood feud with | 1 | Loraq (house) → Kandaq (house) | adwd-daenerys-08 |
| married to (tense, transactional) | 1 | Daenerys → Hizdahr zo Loraq | adwd-daenerys-09 |
| promotes/controls | 1 | Hizdahr → Fighting pits | adwd-daenerys-09 |
| flash of anger toward | 1 | Hizdahr → Daenerys | adwd-daenerys-09 |
| refuses audience with | 1 | Daenerys → Quentyn Martell | adwd-daenerys-09 |
| demands | 1 | Tattered Prince → Pentos | adwd-daenerys-09 |
| recalls with tenderness | 1 | Daenerys → Khal Drogo | adwd-daenerys-09 |
| ambivalent wife | 1 | Daenerys → Hizdahr zo Loraq | adwd-daenerys-10 |
| suspects poisoner | 1 | Daenerys → Hizdahr / Reznak / Yunkai'i / Sons of Harpy | adwd-daenerys-10 |
| mysterious guide | 1 | Quaithe → Daenerys | adwd-daenerys-10 |
| former ko of Drogo / hostile | 1 | Khal Jhaqo → Daenerys | adwd-daenerys-10 |
| bloodrider to | 1 | Mago → Khal Jhaqo | adwd-daenerys-10 |
| rival to | 1 | Ko Pono → Daenerys (Drogo's khalasar) | adwd-daenerys-10 |
| Abandoned | 1 | Salladhor Saan → Stannis Baratheon | adwd-davos-01 |
| Former friend of | 1 | Salladhor Saan → Davos | adwd-davos-01 |
| Sworn vassal of | 1 | Godric Borrell → Triston Sunderland | adwd-davos-01 |
| Host to | 1 | Godric Borrell → Davos | adwd-davos-01 |
| Marriage pact with | 1 | Lord Walder Frey → Wyman Manderly | adwd-davos-01 |
| Let pass | 1 | Lord Godric's father → Ned Stark | adwd-davos-01 |
| Allegedly fathered bastard with | 1 | Ned Stark → Fisherman's daughter | adwd-davos-01 |
| lost four sons in service to | 1 | Davos → Stannis | adwd-davos-02 |
| ship captain transporting | 1 | Casso Mogat → Davos | adwd-davos-02 |
| brought the Faith to | 1 | Manderly (house) → White Harbor / the North | adwd-davos-02 |
| disrespects/insults | 1 | Ser Axell Florent → Davos | adwd-davos-02 |
| former master of | 1 | Roro Uhoris → Davos (as cabin boy) | adwd-davos-02 |
| good-father to | 1 | Lord Wyman Manderly → Lady Leona | adwd-davos-03 |
| former vassal of | 1 | Lord Wyman Manderly → Robb Stark | adwd-davos-03 |
| apparent agreement with | 1 | Lord Wyman Manderly → Rhaegar Frey | adwd-davos-03 |
| weeps for | 1 | Lord Wyman Manderly → Wendel Manderly | adwd-davos-03 |
| ancient oath to | 1 | Manderlys → House Stark | adwd-davos-03 |
| loyalty despite misgivings to | 1 | Davos Seaworth → Stannis Baratheon | adwd-davos-03 |
| loyal servant of | 1 | Davos → King Stannis | adwd-davos-04 |
| gaoler/threat to | 1 | Garth → Davos | adwd-davos-04 |
| sympathetic keeper of | 1 | Therry → Davos | adwd-davos-04 |
| chief gaoler / storyteller to | 1 | Ser Bartimus → Davos | adwd-davos-04 |
| saved life of | 1 | Ser Bartimus → Wyman Manderly | adwd-davos-04 |
| secretly loyal to | 1 | Wyman Manderly → House Stark | adwd-davos-04 |
| good-daughter of | 1 | Lady Leona → Wyman Manderly | adwd-davos-04 |
| deceiving | 1 | Wyman Manderly → Freys (Jared, Rhaegar, Symond) | adwd-davos-04 |
| spying on / bribing | 1 | Symond Frey → Wyman Manderly's household | adwd-davos-04 |
| former squire to | 1 | Wex → Theon Greyjoy | adwd-davos-04 |
| captured and flaying | 1 | Ramsay → Theon Greyjoy | adwd-davos-04 |
| demands submission from | 1 | Roose Bolton → Northern lords | adwd-davos-04 |
| asks service of | 1 | Manderly → Davos | adwd-davos-04 |
| bedding | 1 | Therry's mother → Two guardsmen | adwd-davos-04 |
| spreading lies about | 1 | Freys → Robb Stark | adwd-davos-04 |
| Lord Regent governing in name of | 1 | Kevan Lannister → Tommen Baratheon | adwd-epilogue |
| Guardianship/containment of | 1 | Kevan Lannister → Cersei Lannister | adwd-epilogue |
| Familial duty toward | 1 | Kevan Lannister → Cersei Lannister | adwd-epilogue |
| Hand of the King to | 1 | Mace Tyrell → Tommen Baratheon | adwd-epilogue |
| Father protecting | 1 | Mace Tyrell → Margaery Tyrell | adwd-epilogue |
| Viewed by Kevan as | 1 | Randyll Tarly → The real danger | adwd-epilogue |
| Subdued submission to | 1 | Cersei Lannister → Kevan Lannister | adwd-epilogue |
| Twin bond with | 1 | Cersei Lannister → Jaime Lannister | adwd-epilogue |
| Views suspiciously | 1 | Kevan Lannister → Robert Strong | adwd-epilogue |
| Remembers Tywin stripped and paraded | 1 | Kevan (memory) → Tytos's mistress | adwd-epilogue |
| fond memory of | 1 | Jaime → Tyrion | adwd-jaime-01 |
| shocked by condition of | 1 | Jaime → Brienne | adwd-jaime-01 |
| besieging/rival of | 1 | Jonos Bracken → Tytos Blackwood | adwd-jaime-01 |
| bold/flirtatious with | 1 | Hildy → Jaime | adwd-jaime-01 |
| eager/naive toward | 1 | Hoster Blackwood → Jaime | adwd-jaime-01 |
| harsh with | 1 | Jaime → Hoster Blackwood | adwd-jaime-01 |
| knowledgeable about | 1 | Hoster Blackwood → Blackwood-Bracken history | adwd-jaime-01 |
| bound by quest to | 1 | Brienne → Jaime | adwd-jaime-01 |
| merciful toward | 1 | Jaime → Pennytree villagers | adwd-jaime-01 |
| Conflicted regard for | 1 | Jon Snow → Sansa Stark | adwd-jon-01 |
| Taunts / challenges | 1 | Ser Godry Farring → Jon Snow | adwd-jon-01 |
| Dismisses / ignores | 1 | Jon Snow → Ser Godry Farring | adwd-jon-01 |
| Follows / accompanies | 1 | Mormont's raven → Jon Snow | adwd-jon-01 |
| Demands execution of | 1 | Stannis Baratheon → Mance Rayder | adwd-jon-01 |
| Declared allegiance to | 1 | Arnolf Karstark → Stannis Baratheon | adwd-jon-01 |
| motherly protectiveness | 1 | Gilly → Her own son and Dalla's son | adwd-jon-02 |
| Remembers/compares | 1 | Jon Snow → Ygritte | adwd-jon-03 |
| Forced distance from | 1 | Jon Snow → Pyp, Grenn | adwd-jon-03 |
| Political authority over | 1 | Stannis Baratheon → Wildling captives | adwd-jon-03 |
| Former member of | 1 | Mance Rayder → Night's Watch | adwd-jon-03 |
| Successor to | 1 | Sigorn → His father (previous Magnar of Thenn) | adwd-jon-03 |
| Attempts to recruit/elevate | 1 | Stannis → Jon Snow | adwd-jon-04 |
| Refuses fealty to | 1 | Jon Snow → Stannis | adwd-jon-04 |
| Gives (as gift) | 1 | Stannis → Rattleshirt (to Jon) | adwd-jon-04 |
| Won't fight | 1 | Mors Umber → Hother Umber | adwd-jon-04 |
| Claims belongs to (Winterfell) | 1 | Jon Snow → Sansa Stark | adwd-jon-04 |
| Plans campaign against | 1 | Stannis → Boltons | adwd-jon-04 |
| Aspires to win | 1 | Ser Justin Massey → Val | adwd-jon-04 |
| Disagree with | 1 | Night's Watch rangers → Bowen Marsh | adwd-jon-04 |
| Feels grudge from (childhood) | 1 | Jon Snow → Lysa Arryn | adwd-jon-04 |
| Conflicts with | 1 | Jon Snow → Bowen Marsh | adwd-jon-05 |
| Frustrated by | 1 | Jon Snow → Othell Yarwyck | adwd-jon-05 |
| Combative challenger to | 1 | Rattleshirt → Jon Snow | adwd-jon-06 |
| Unusually warm toward | 1 | Ghost → Melisandre | adwd-jon-06 |
| Nostalgic for | 1 | Jon Snow → Robb Stark | adwd-jon-06 |
| Complex resentment toward | 1 | Jon Snow → Lady Catelyn | adwd-jon-06 |
| Claims marriage to | 1 | Ramsay Bolton → Arya Stark | adwd-jon-06 |
| Political authority over Northern lords | 1 | Roose Bolton → Lord Dustin, Lady Cerwyn, Ryswells, House Umber | adwd-jon-06 |
| remembers / learned from | 1 | Jon Snow → Ygritte | adwd-jon-07 |
| identifies with / honors | 1 | Jon Snow → Eddard Stark | adwd-jon-07 |
| strategically regards | 1 | Jon Snow → Stannis Baratheon | adwd-jon-07 |
| mediates between | 1 | Leathers → Jon Snow and the giant | adwd-jon-07 |
| sends on mission / trusts | 1 | Jon Snow → Val | adwd-jon-08 |
| broke promise to | 1 | Jon Snow → Stannis | adwd-jon-08 |
| uncomfortable deference to | 1 | Othell Yarwyck → Jon Snow | adwd-jon-08 |
| inquired about death of | 1 | Val → Jarl | adwd-jon-08 |
| steals from | 1 | Mormont's raven → Jon Snow | adwd-jon-08 |
| kinsman/Queen's Hand to | 1 | Ser Axell Florent → Queen Selyse | adwd-jon-09 |
| true allegiance of queen's men | 1 | Melisandre → Queen's men | adwd-jon-09 |
| guest/ward of | 1 | Wun Wun → Night's Watch | adwd-jon-09 |
| fool to | 1 | Patchface → Princess Shireen | adwd-jon-09 |
| fled from / opposes | 1 | Alys Karstark → Arnolf Karstark & Cregan Karstark | adwd-jon-09 |
| plans to betray | 1 | Arnolf Karstark → Stannis Baratheon | adwd-jon-09 |
| pursuing | 1 | Cregan Karstark → Alys Karstark | adwd-jon-09 |
| creditor to | 1 | Iron Bank → Iron Throne / Robert Baratheon | adwd-jon-09 |
| potential supporter of | 1 | Iron Bank → Stannis Baratheon | adwd-jon-09 |
| Gives away in marriage | 1 | Jon Snow → Alys Karstark | adwd-jon-10 |
| Warm rapport / protective | 1 | Jon Snow → Alys Karstark | adwd-jon-10 |
| Hostile/aggressive | 1 | Ser Patrek → General | adwd-jon-10 |
| Hostile contempt toward | 1 | Cregan Karstark → Jon Snow | adwd-jon-10 |
| Claims right to | 1 | Cregan Karstark → Alys Karstark | adwd-jon-10 |
| Pressures / manipulates | 1 | Ser Axell Florent → Jon Snow | adwd-jon-10 |
| Wet nurses provided for | 1 | Old Flint / Norrey → Monster (Mance's child) | adwd-jon-10 |
| Former antagonist to | 1 | Glendon Hewett → Jon Snow | adwd-jon-10 |
| Childhood acquaintance | 1 | Alys Karstark → Jon Snow (and Robb) | adwd-jon-10 |
| Attraction (suppressed) | 1 | Jon Snow → Val | adwd-jon-11 |
| Loyalty/debt | 1 | Val → Jon Snow | adwd-jon-11 |
| Protective/horror | 1 | Val → Shireen Baratheon | adwd-jon-11 |
| Warm | 1 | Val → Ghost | adwd-jon-11 |
| Condescension | 1 | Queen Selyse → Val | adwd-jon-11 |
| Anxiety | 1 | Queen Selyse → Ghost / Wun Wun | adwd-jon-11 |
| Gallant/attracted | 1 | Ser Patrek → Val | adwd-jon-11 |
| Opposition (reluctant compliance) | 1 | Othell Yarwyck → Jon Snow | adwd-jon-11 |
| Loyalty/defense | 1 | Leathers → Jon Snow | adwd-jon-11 |
| Grudging acceptance | 1 | Old Flint → Jon Snow | adwd-jon-11 |
| Tests Jon's resolve | 1 | The Norrey → Jon Snow | adwd-jon-11 |
| Bond with (direwolf) | 1 | Jon Snow → Ghost | adwd-jon-12 |
| Takes as page | 1 | Jon Snow → Dryn | adwd-jon-12 |
| Guilt toward (dream) | 1 | Jon Snow → Robb Stark | adwd-jon-12 |
| Nostalgic kinship with | 1 | Jon Snow → Bran, Arya, Robb | adwd-jon-12 |
| Stiff obedience toward | 1 | Bowen Marsh → Jon Snow | adwd-jon-12 |
| Cryptic kinship claim toward | 1 | Borroq → Jon Snow | adwd-jon-12 |
| Offers service to | 1 | Soren Shieldbreaker → Jon Snow | adwd-jon-12 |
| Reports to / requests help from | 1 | Cotter Pyke → Jon Snow | adwd-jon-12 |
| Used by | 1 | Gerrick Kingsblood → Queen Selyse | adwd-jon-13 |
| Unsettles | 1 | Borroq → Jon Snow / Castle Black | adwd-jon-13 |
| owes life to / grudgingly cooperates with | 1 | Mance Rayder → Melisandre | adwd-melisandre-01 |
| owes life to | 1 | Mance Rayder → Jon Snow | adwd-melisandre-01 |
| disagrees with/resents | 1 | Bowen Marsh → Jon Snow | adwd-melisandre-01 |
| clashed with | 1 | Mance (as Rattleshirt) → Bowen Marsh | adwd-melisandre-01 |
| interprets as enemy's servants | 1 | Melisandre → The wooden-faced man and wolf-faced boy | adwd-melisandre-01 |
| bound by vows regarding | 1 | Jon Snow → Arya Stark | adwd-melisandre-01 |
| master/controller of | 1 | Varamyr → One Eye, Stalker, Sly | adwd-prologue |
| stole beast from | 1 | Varamyr → Haggon | adwd-prologue |
| served/followed | 1 | Varamyr → Mance Rayder | adwd-prologue |
| lied to | 1 | Varamyr → Thistle | adwd-prologue |
| attempted to seize body of | 1 | Varamyr → Thistle | adwd-prologue |
| rejected | 1 | Varamyr's mother → Varamyr | adwd-prologue |
| hated | 1 | Orell (in eagle) → Jon Snow | adwd-prologue |
| recognized gift in | 1 | Varamyr → Jon Snow | adwd-prologue |
| mates with | 1 | One Eye → Sly | adwd-prologue |
| former controller of | 1 | Varamyr → Shadowcat, snow bear, eagle (Orell's) | adwd-prologue |
| terror/exploitation of | 1 | Varamyr → Village women | adwd-prologue |
| Captive / forced servant | 1 | Reek → Ramsay Bolton | adwd-reek-01 |
| Son (legitimized) | 1 | Ramsay Bolton → Lord Roose Bolton | adwd-reek-01 |
| Arranging marriage for | 1 | Lord Roose Bolton → Ramsay Bolton | adwd-reek-01 |
| Married and killed | 1 | Ramsay Bolton → Lady Hornwood | adwd-reek-01 |
| Attempted escape with | 1 | Reek → Kyra | adwd-reek-01 |
| Hunted and punished | 1 | Ramsay Bolton → Kyra | adwd-reek-01 |
| Kennel master for | 1 | Ben Bones → Ramsay Bolton | adwd-reek-01 |
| Punished by | 1 | Grunt → Lord Roose Bolton | adwd-reek-01 |
| Retainers / favorites of | 1 | The Bastard's Boys → Ramsay Bolton | adwd-reek-01 |
| Guest of, hostile toward Reek | 1 | Mail-byrnie lord → Ramsay Bolton | adwd-reek-01 |
| Slave/creature of | 1 | Reek → Ramsay Bolton | adwd-reek-02 |
| Psychological dominion over | 1 | Ramsay Bolton → Reek | adwd-reek-02 |
| Natural son of | 1 | Ramsay Bolton → Roose Bolton | adwd-reek-02 |
| Recognizes true identity of | 1 | Reek → Jeyne Poole | adwd-reek-02 |
| Mercy-kills | 1 | Reek → Ralf Kenning | adwd-reek-02 |
| Defeated (at kingsmoot) | 1 | Euron Greyjoy → Victarion Greyjoy | adwd-reek-02 |
| Former acquaintance of | 1 | Reek → Robb Stark | adwd-reek-02 |
| Former antagonist of | 1 | Reek → Roose Bolton | adwd-reek-02 |
| Dominates/owns | 1 | Ramsay Bolton → Reek (Theon) | adwd-reek-03 |
| Father, controls | 1 | Roose Bolton → Ramsay Bolton | adwd-reek-03 |
| Distanced from | 1 | Big Walder → Little Walder / Ramsay | adwd-reek-03 |
| Cannot abide | 1 | Lady Barbrey Dustin → Ramsay Bolton | adwd-reek-03 |
| Holds grudge against | 1 | Lady Barbrey Dustin → Ned Stark (deceased) | adwd-reek-03 |
| Married (past, deceased) | 1 | Roose Bolton → Roose's second wife | adwd-reek-03 |
| Inseparable from (past) | 1 | Ramsay Bolton → The first Reek | adwd-reek-03 |
| Suspects betrayal from | 1 | Roose Bolton → Lord Wyman Manderly | adwd-reek-03 |
| Coerced by | 1 | Harwood Stout → Ramsay Bolton | adwd-reek-03 |
| Justified killing | 1 | Arya → Dareon | adwd-the-blind-girl-01 |
| Kindness/charity | 1 | Pynto → Blind Beth (Arya) | adwd-the-blind-girl-01 |
| Pack leader | 1 | Nymeria → Her grey cousins (wolf pack) | adwd-the-blind-girl-01 |
| Tests/challenges | 1 | The kindly man → Arya | adwd-the-blind-girl-01 |
| Enslaved | 1 | Lyseni pirates → Wildling women and children | adwd-the-blind-girl-01 |
| Protector / sworn to | 1 | Barristan Selmy → Daenerys Targaryen | adwd-the-discarded-knight-01 |
| King / husband of | 1 | Hizdahr zo Loraq → Daenerys Targaryen | adwd-the-discarded-knight-01 |
| Suspicion / displeasure toward | 1 | Hizdahr zo Loraq → Quentyn Martell | adwd-the-discarded-knight-01 |
| Paramour | 1 | Daenerys Targaryen → Daario Naharis | adwd-the-discarded-knight-01 |
| Captain of | 1 | Daario Naharis → Stormcrows | adwd-the-discarded-knight-01 |
| Wife and family in | 1 | Groleo → Pentos | adwd-the-discarded-knight-01 |
| Protectors of | 1 | Goghor, Spotted Cat, Belaquo, Khrazz → Hizdahr zo Loraq | adwd-the-discarded-knight-01 |
| Showed mercy to | 1 | Prince Duncan (Prince of Dragonflies) → Young Barristan | adwd-the-discarded-knight-01 |
| Provided equipment to | 1 | Lord Dondarrion → Young Barristan | adwd-the-discarded-knight-01 |
| Sellsword accompanying | 1 | Bloodbeard → Yunkish delegation | adwd-the-discarded-knight-01 |
| Desires/pursues | 1 | Quentyn Martell → Daenerys Targaryen | adwd-the-dragontamer-01 |
| Led by / sent by father | 1 | Quentyn Martell → Doran Martell | adwd-the-dragontamer-01 |
| Unhappy marriage | 1 | Doran Martell → His Norvoshi wife (Quentyn's mother) | adwd-the-dragontamer-01 |
| Has paramour | 1 | Daenerys Targaryen → Unnamed (paramour) | adwd-the-dragontamer-01 |
| former Hand to / devoted to memory of | 1 | Jon Connington → Rhaegar Targaryen | adwd-the-griffin-reborn-01 |
| lord of (reclaimed) | 1 | Jon Connington → Griffin's Roost | adwd-the-griffin-reborn-01 |
| doubts worthiness of | 1 | Jon Connington → Ser Rolly Duckfield | adwd-the-griffin-reborn-01 |
| opposed / failed to capture | 1 | Jon Connington → Robert Baratheon | adwd-the-griffin-reborn-01 |
| recalls advice from | 1 | Jon Connington → Myles Toyne (Blackheart) | adwd-the-griffin-reborn-01 |
| disparages (in memory) | 1 | Jon Connington → Princess Elia | adwd-the-griffin-reborn-01 |
| insists on keeping | 1 | Prince Aegon → Ser Rolly Duckfield as Kingsguard | adwd-the-griffin-reborn-01 |
| asserts authority over | 1 | Prince Aegon → Jon Connington | adwd-the-griffin-reborn-01 |
| fighting alongside | 1 | Ronnet Connington (Red Ronnet) → Jaime Lannister | adwd-the-griffin-reborn-01 |
| led assault on | 1 | Franklyn Flowers → Griffin's Roost | adwd-the-griffin-reborn-01 |
| prescribed treatment for | 1 | Lady Lemore → Greyscale (via Jon Connington) | adwd-the-griffin-reborn-01 |
| Uses/confides in | 1 | Victarion → Dusky woman | adwd-the-iron-suitor-01 |
| Strikes/disciplines | 1 | Victarion → Ralf the Limper | adwd-the-iron-suitor-01 |
| Stole from | 1 | Euron → Victarion | adwd-the-iron-suitor-01 |
| Won kingsmoot over | 1 | Euron → Victarion and Aeron | adwd-the-iron-suitor-01 |
| Healer/priest to | 1 | Moqorro → Victarion | adwd-the-iron-suitor-01 |
| Previously assaulted | 1 | Burton Humble → Maester Kerwin | adwd-the-iron-suitor-01 |
| Sexually assaulted | 1 | Four unnamed crewmen → Maester Kerwin | adwd-the-iron-suitor-01 |
| Suspects/arrests | 1 | Barristan → Hizdahr zo Loraq | adwd-the-kingbreaker-01 |
| Disapproves of but defends | 1 | Barristan → Daario Naharis | adwd-the-kingbreaker-01 |
| Served but was not fully trusted by | 1 | Barristan → Rhaegar Targaryen | adwd-the-kingbreaker-01 |
| Claims control over | 1 | Skahaz → Brazen Beasts | adwd-the-kingbreaker-01 |
| Consort/king to | 1 | Hizdahr → Daenerys | adwd-the-kingbreaker-01 |
| Consults with | 1 | Hizdahr → Reznak, Marghaz, Galazza Galare | adwd-the-kingbreaker-01 |
| Shares doubts with | 1 | Marselen → Barristan | adwd-the-kingbreaker-01 |
| Prisoner/hostage of | 1 | Asha Greyjoy → Stannis Baratheon | adwd-the-kings-prize-01 |
| Dismisses/rejects | 1 | Stannis Baratheon → Asha Greyjoy | adwd-the-kings-prize-01 |
| Cautious rapport with | 1 | Asha Greyjoy → Alysane Mormont | adwd-the-kings-prize-01 |
| Courts/is attracted to | 1 | Justin Massey → Asha Greyjoy | adwd-the-kings-prize-01 |
| Tolerates for advantage | 1 | Asha Greyjoy → Justin Massey | adwd-the-kings-prize-01 |
| Recalls wisdom of | 1 | Asha Greyjoy → Balon Greyjoy | adwd-the-kings-prize-01 |
| Accuses/distrusts | 1 | Lord Peasebury → Big Bucket Wull | adwd-the-kings-prize-01 |
| Insist on marching for | 1 | Northmen (clansmen) → "Ned's girl" / Eddard Stark's memory | adwd-the-kings-prize-01 |
| Oppose/resent | 1 | Southron lords → Northern clansmen | adwd-the-kings-prize-01 |
| Push for sacrifice from | 1 | Queen's men → Stannis Baratheon | adwd-the-kings-prize-01 |
| Refuses sacrifice from | 1 | Stannis Baratheon → Queen's men | adwd-the-kings-prize-01 |
| Relies on (absent) | 1 | Stannis Baratheon → Melisandre | adwd-the-kings-prize-01 |
| Recalls failure with | 1 | Asha Greyjoy → Theon Greyjoy | adwd-the-kings-prize-01 |
| Surrogate father / protector | 1 | Jon Connington → Aegon | adwd-the-lost-lord-01 |
| Diminished trust | 1 | Jon Connington → Haldon | adwd-the-lost-lord-01 |
| Fondness | 1 | Jon Connington → Lady Lemore | adwd-the-lost-lord-01 |
| Old comradeship | 1 | Jon Connington → Franklyn Flowers | adwd-the-lost-lord-01 |
| Influenced by | 1 | Aegon → Tyrion Lannister | adwd-the-lost-lord-01 |
| Asserts independence from | 1 | Aegon → Jon Connington | adwd-the-lost-lord-01 |
| Protective caution toward | 1 | Lemore → Aegon | adwd-the-lost-lord-01 |
| Reluctant allegiance | 1 | Harry Strickland → Aegon | adwd-the-lost-lord-01 |
| Enthusiastic support | 1 | Franklyn Flowers → Aegon | adwd-the-lost-lord-01 |
| Support / allegiance | 1 | Tristan Rivers → Aegon | adwd-the-lost-lord-01 |
| Rose through the ranks under | 1 | Connington (past) → Myles Toyne | adwd-the-lost-lord-01 |
| Cautious assessment of | 1 | Strickland → Daenerys | adwd-the-lost-lord-01 |
| Suggests deception of | 1 | Gorys Edoryen → The Yunkishmen | adwd-the-lost-lord-01 |
| Claims lineage from | 1 | Aegon → Rhaegar and Elia | adwd-the-lost-lord-01 |
| Youthful infatuation with | 1 | Quentyn Martell → Ynys Yronwood | adwd-the-merchants-man-01 |
| Awkward romantic history with | 1 | Quentyn Martell → The Drinkwater twins | adwd-the-merchants-man-01 |
| Views as a game / does not fully grasp danger | 1 | Gerris Drinkwater → The mission | adwd-the-merchants-man-01 |
| Suffers severe seasickness | 1 | Ser Archibald Yronwood → Ships | adwd-the-merchants-man-01 |
| Sent | 1 | Doran Martell → Maester Kedry | adwd-the-merchants-man-01 |
| forced servant / instrument | 1 | Theon → Roose Bolton | adwd-the-prince-of-winterfell-01 |
| terrorized by / subjugated to | 1 | Theon → Ramsay Bolton | adwd-the-prince-of-winterfell-01 |
| pity and guilt toward | 1 | Theon → Jeyne Poole | adwd-the-prince-of-winterfell-01 |
| complicated former ward of | 1 | Theon → Eddard Stark | adwd-the-prince-of-winterfell-01 |
| cruel husband to | 1 | Ramsay → Jeyne Poole | adwd-the-prince-of-winterfell-01 |
| claims legitimacy from | 1 | Ramsay → House Stark | adwd-the-prince-of-winterfell-01 |
| uses and manipulates | 1 | Roose Bolton → Theon | adwd-the-prince-of-winterfell-01 |
| political schemer against | 1 | Roose Bolton → Stannis Baratheon | adwd-the-prince-of-winterfell-01 |
| confidante / political observer to | 1 | Lady Dustin → Theon | adwd-the-prince-of-winterfell-01 |
| potential obstacle to | 1 | Lady Dustin → Roose Bolton | adwd-the-prince-of-winterfell-01 |
| outwardly loyal, inwardly hostile toward | 1 | Lord Manderly → Boltons and Freys | adwd-the-prince-of-winterfell-01 |
| provider of feast to | 1 | Lord Manderly → Wedding guests | adwd-the-prince-of-winterfell-01 |
| entertainer at | 1 | Abel (bard) → Wedding feast | adwd-the-prince-of-winterfell-01 |
| desperate dependent on | 1 | Jeyne Poole → Theon | adwd-the-prince-of-winterfell-01 |
| recalls with guilt | 1 | Theon → Bran and Rickon | adwd-the-prince-of-winterfell-01 |
| Dominates / silences | 1 | Archibald Yronwood → Gerris Drinkwater | adwd-the-queens-hand-01 |
| Loyal / obedient to | 1 | Grey Worm → Barristan Selmy | adwd-the-queens-hand-01 |
| Made pact with | 1 | Quentyn Martell → The Tattered Prince | adwd-the-queens-hand-01 |
| Unifying force for | 1 | Daenerys Targaryen → All Meereen factions | adwd-the-queens-hand-01 |
| Sworn protector of; devoted loyalty to | 1 | Barristan Selmy → Daenerys Targaryen | adwd-the-queensguard-01 |
| Haunted by failure to protect | 1 | Barristan Selmy → Aerys, Rhaegar, Elia, Aegon (baby), Rhaenys, Robert, Jaehaerys | adwd-the-queensguard-01 |
| Feels inadequate compared to | 1 | Barristan Selmy → Daario Naharis | adwd-the-queensguard-01 |
| Systematically removes | 1 | Hizdahr zo Loraq → Daenerys's loyalists | adwd-the-queensguard-01 |
| Relies on as protectors | 1 | Hizdahr zo Loraq → Pit fighters (Goghor, Khrazz, Spotted Cat, Belaquo) | adwd-the-queensguard-01 |
| Claims continued loyalty of | 1 | Skahaz mo Kandaq → Brazen Beasts | adwd-the-queensguard-01 |
| Refused to serve | 1 | Grey Worm → Hizdahr zo Loraq | adwd-the-queensguard-01 |
| Guarded/companionship | 1 | Asha Greyjoy → Alysane Mormont | adwd-the-sacrifice-01 |
| Wary dependence | 1 | Asha Greyjoy → Justin Massey | adwd-the-sacrifice-01 |
| Mutual hostility | 1 | Asha Greyjoy → Clayton Suggs | adwd-the-sacrifice-01 |
| Siblings (barely recognized) | 1 | Asha Greyjoy → Theon Greyjoy | adwd-the-sacrifice-01 |
| Loyalty from | 1 | Asha Greyjoy → Tristifer Botley | adwd-the-sacrifice-01 |
| Right-hand man to | 1 | Clayton Suggs → Godry Farring | adwd-the-sacrifice-01 |
| Mutual antagonism with | 1 | Clayton Suggs → Justin Massey | adwd-the-sacrifice-01 |
| Authorizes | 1 | Stannis Baratheon → Queen's men (Godry, Suggs, Penny) | adwd-the-sacrifice-01 |
| Withdrawn from | 1 | Stannis Baratheon → His lords | adwd-the-sacrifice-01 |
| Vocal supporter of | 1 | Arnolf Karstark → Stannis Baratheon | adwd-the-sacrifice-01 |
| Physical dependence on | 1 | Arnolf Karstark → Arthor Karstark | adwd-the-sacrifice-01 |
| Faction tension with | 1 | Northmen → Southerners | adwd-the-sacrifice-01 |
| Religious conflict with | 1 | Queen's men → Northern lords (Flint, Wull) | adwd-the-sacrifice-01 |
| Stigmatized by | 1 | Lord Peasebury → Other lords | adwd-the-sacrifice-01 |
| Transaction with | 1 | Sybelle Glover → Tycho Nestoris | adwd-the-sacrifice-01 |
| Former member/deserter of | 1 | Quentyn Martell → The Windblown | adwd-the-spurned-suitor-01 |
| Negotiating employer of | 1 | Quentyn Martell → The Tattered Prince | adwd-the-spurned-suitor-01 |
| Hired by / contracted with | 1 | The Windblown → Yunkai | adwd-the-spurned-suitor-01 |
| Captive / psychologically enslaved by | 1 | Theon Greyjoy → Ramsay Bolton | adwd-the-turncloak-01 |
| Forced servitor to | 1 | Theon Greyjoy → Ramsay Bolton | adwd-the-turncloak-01 |
| Reluctant protector / guilty toward | 1 | Theon Greyjoy → Jeyne Poole | adwd-the-turncloak-01 |
| Abuser of | 1 | Ramsay Bolton → Jeyne Poole | adwd-the-turncloak-01 |
| Political advisor / critic to | 1 | Lady Dustin → Roose Bolton / Ramsay Bolton | adwd-the-turncloak-01 |
| Identifies with / parallels | 1 | Lady Dustin → Theon Greyjoy | adwd-the-turncloak-01 |
| Entertainer / serves | 1 | Abel → Ramsay Bolton / Bolton court | adwd-the-turncloak-01 |
| Unenthusiastic participant in | 1 | Lord Wyman Manderly → Bolton coalition | adwd-the-turncloak-01 |
| Uncomfortable outsiders in | 1 | Freys (Aenys, Hosteen) → The North / Bolton coalition | adwd-the-turncloak-01 |
| Had spies within | 1 | Lady Dustin → Robb Stark's host | adwd-the-turncloak-01 |
| Employs identity of | 1 | Arya → Cat of the Canals | adwd-the-ugly-little-girl-01 |
| Employer-employee of | 1 | Arya → Brusco | adwd-the-ugly-little-girl-01 |
| Learned from | 1 | Arya → Red Roggo | adwd-the-ugly-little-girl-01 |
| Recalls / models | 1 | Arya → Jaqen H'ghar | adwd-the-ugly-little-girl-01 |
| Harbors revenge against | 1 | Arya → Ser Gregor, Dunsen, Raff the Sweetling, Ser Ilyn, Ser Meryn, Queen Cersei | adwd-the-ugly-little-girl-01 |
| Performs with | 1 | Tagganaro → Casso, King of Seals | adwd-the-ugly-little-girl-01 |
| Victim of | 1 | The dead girl (face donor) → Her father | adwd-the-ugly-little-girl-01 |
| Captain of guards / devoted servant | 1 | Areo Hotah → Prince Doran | adwd-the-watcher-01 |
| Former paramour of | 1 | Ellaria Sand → Oberyn Martell (dead) | adwd-the-watcher-01 |
| Daughters of | 1 | Sand Snakes → Oberyn Martell (dead) | adwd-the-watcher-01 |
| Flirts with | 1 | Arianne → Ser Balon Swann | adwd-the-watcher-01 |
| Mocking yet loyal toward | 1 | Tyene Sand → Prince Doran | adwd-the-watcher-01 |
| Corrects Nym about Ellaria | 1 | Prince Doran → Lady Nym | adwd-the-watcher-01 |
| Planning with | 1 | Prince Doran → Quentyn Martell | adwd-the-watcher-01 |
| Plotting against | 1 | Doran/Arianne → Cersei/Iron Throne | adwd-the-watcher-01 |
| unrequited devotion from | 1 | Asha → Tris Botley | adwd-the-wayward-bride-01 |
| forced marriage to | 1 | Asha → Erik Ironmaker | adwd-the-wayward-bride-01 |
| political enemy of | 1 | Asha → Euron Greyjoy | adwd-the-wayward-bride-01 |
| devotion/service to | 1 | Tris Botley → Asha | adwd-the-wayward-bride-01 |
| obedience/disregard toward | 1 | Qarl the Maid → Erik Ironmaker | adwd-the-wayward-bride-01 |
| pursuer of | 1 | Euron → Aeron Greyjoy (Damphair) | adwd-the-wayward-bride-01 |
| desperate mother to | 1 | Sybelle Glover → Gawen Glover, infant daughter | adwd-the-wayward-bride-01 |
| eagerness for battle | 1 | Cromm → — | adwd-the-wayward-bride-01 |
| unrequited interest in | 1 | Hagen's daughter → Tris Botley | adwd-the-wayward-bride-01 |
| sexual encounter with | 1 | Hagen's daughter → Six-Toed Harl | adwd-the-wayward-bride-01 |
| political enemy/threat to | 1 | Ramsay Bolton → Asha and ironborn | adwd-the-wayward-bride-01 |
| mother fixated on | 1 | Lady Alannys → Theon | adwd-the-wayward-bride-01 |
| poses as squire to | 1 | Quentyn Martell → Archibald Yronwood (Greenguts) | adwd-the-windblown-01 |
| friends with (gambling) | 1 | Archibald Yronwood → Beans, Books, Old Bill Bone | adwd-the-windblown-01 |
| childhood friends with | 1 | Quentyn Martell → Gerris Drinkwater & Archibald Yronwood | adwd-the-windblown-01 |
| identity conflict with | 1 | Theon → Reek (persona) | adwd-theon-01 |
| terrorized by/conditioned to | 1 | Jeyne Poole → Ramsay Bolton | adwd-theon-01 |
| murderous hatred toward | 1 | Ser Hosteen Frey → Wyman Manderly | adwd-theon-01 |
| provokes/defies | 1 | Wyman Manderly → Freys | adwd-theon-01 |
| argues with | 1 | Ramsay Bolton → Roose Bolton | adwd-theon-01 |
| dominates/terrorizes | 1 | Ramsay Bolton → His men (Bastard's Boys) | adwd-theon-01 |
| reclaims identity | 1 | Theon → Himself | adwd-theon-01 |
| compelled rescue of | 1 | Jaime → Tyrion | adwd-tyrion-01 |
| hosts/shelters | 1 | Illyrio → Tyrion | adwd-tyrion-01 |
| forced rape of | 1 | Lord Tywin → Tysha | adwd-tyrion-01 |
| sent to Wall | 1 | Tyrion → Janos Slynt | adwd-tyrion-01 |
| Host / patron to | 1 | Illyrio → Tyrion | adwd-tyrion-02 |
| Devoted to memory of | 1 | Illyrio → Serra | adwd-tyrion-02 |
| Former patron of | 1 | Illyrio → Viserys | adwd-tyrion-02 |
| Haunted by killing of | 1 | Tyrion → Tywin | adwd-tyrion-02 |
| Guilt / horror over | 1 | Tyrion → Shae | adwd-tyrion-02 |
| Violently conflicted with | 1 | Tyrion → Jaime | adwd-tyrion-02 |
| Sold/gave Daenerys to | 1 | Illyrio → Khal Drogo | adwd-tyrion-02 |
| Attempted incest with | 1 | Viserys → Daenerys | adwd-tyrion-02 |
| Originally from | 1 | Varys → Myr | adwd-tyrion-02 |
| Former bravo, lived by blade | 1 | Illyrio → (youth) | adwd-tyrion-02 |
| Married (first) | 1 | Illyrio → Prince of Pentos's cousin | adwd-tyrion-02 |
| Founded | 1 | Bittersteel → Golden Company | adwd-tyrion-02 |
| Patron → dependent / traveling under his protection | 1 | Tyrion → Illyrio | adwd-tyrion-03 |
| Benefactor / emotionally attached | 1 | Illyrio → Young Griff | adwd-tyrion-03 |
| Former squire | 1 | Duck → Harry Strickland | adwd-tyrion-03 |
| Intellectual rivalry / testing | 1 | Haldon → Tyrion | adwd-tyrion-03 |
| Projects father dynamic onto | 1 | Tyrion → Griff | adwd-tyrion-03 |
| Ambivalent toward / claims murderous intent | 1 | Tyrion → Jaime | adwd-tyrion-03 |
| Claims to have poisoned (unverified) | 1 | Tyrion → Joffrey | adwd-tyrion-03 |
| Bitterness / resentment toward | 1 | Tyrion → Tywin (recalled) | adwd-tyrion-03 |
| Fond recollection | 1 | Tyrion → Gerion Lannister | adwd-tyrion-03 |
| Father-son (claimed) | 1 | Griff → Young Griff | adwd-tyrion-03 |
| Claims maternal connection to Tyrosh | 1 | Young Griff → (deceased mother) | adwd-tyrion-03 |
| Beat severely / enemy | 1 | Duck → Lorent Caswell | adwd-tyrion-03 |
| Devoted to deceased wife | 1 | Illyrio → Serra | adwd-tyrion-03 |
| Moral authority over company | 1 | Septa Lemore → Duck, others | adwd-tyrion-03 |
| Sexual desire | 1 | Tyrion → Septa Lemore | adwd-tyrion-04 |
| Indifferent to / tolerant of | 1 | Ysilla → Yandry's glancing | adwd-tyrion-04 |
| Intellectual rival | 1 | Tyrion → Haldon | adwd-tyrion-04 |
| Guilt / longing | 1 | Tyrion → Tysha | adwd-tyrion-04 |
| Puppet master | 1 | Illyrio → Griff, Duck, the company | adwd-tyrion-04 |
| Maternal / feeding | 1 | Ysilla → Young Griff | adwd-tyrion-04 |
| Disciplinary | 1 | Ysilla → Duck | adwd-tyrion-04 |
| Spiritual tutor | 1 | Septa Lemore → Young Griff | adwd-tyrion-04 |
| Warmly teasing | 1 | Septa Lemore → Tyrion | adwd-tyrion-04 |
| Guarded assessment | 1 | Tyrion → Young Griff | adwd-tyrion-04 |
| Father figure to | 1 | Griff → Young Griff | adwd-tyrion-05 |
| Superstitious/pious | 1 | Ysilla → The Rhoyne/supernatural | adwd-tyrion-05 |
| Rationalist counterpoint to | 1 | Haldon Halfmaester → Ysilla | adwd-tyrion-05 |
| Unresolved longing for | 1 | Tyrion → Tysha | adwd-tyrion-05 |
| Dear friend of | 1 | Jon Connington (Griff) → Rhaegar Targaryen | adwd-tyrion-05 |
| Patron/briber of | 1 | Illyrio Mopatis → Nyessos (Triarch of Volantis) | adwd-tyrion-05 |
| Married to / partnered with | 1 | Yandry → Ysilla | adwd-tyrion-05 |
| Protected | 1 | Young Griff → Tyrion | adwd-tyrion-06 |
| Tests/monitors | 1 | Haldon → Tyrion | adwd-tyrion-06 |
| Compares self to | 1 | Tyrion → Joffrey (re: angering princes) | adwd-tyrion-06 |
| Superior cyvasse player to | 1 | Qavo → Tyrion | adwd-tyrion-06 |
| Proclaims | 1 | Benerro → Daenerys as Azor Ahai | adwd-tyrion-06 |
| Bribed by | 1 | Nyessos (triarch) → Yunkai'i / Grazdan mo Eraz | adwd-tyrion-06 |
| Shame toward | 1 | Tyrion → Westerosi whore | adwd-tyrion-06 |
| Former agent of | 1 | Jorah Mormont → Varys | adwd-tyrion-07 |
| Guilty about | 1 | Tyrion Lannister → Tysha | adwd-tyrion-07 |
| Former slave/wife of | 1 | The widow → Vogarro | adwd-tyrion-07 |
| Concerned about | 1 | Tyrion Lannister → Griff/Aegon | adwd-tyrion-07 |
| tense cohabitation / mutual irritation | 1 | Tyrion → Jorah Mormont | adwd-tyrion-08 |
| obsessed longing for | 1 | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-08 |
| proselytizing interest in | 1 | Moqorro → Tyrion | adwd-tyrion-08 |
| conflicted feelings about | 1 | Tyrion → Jaime Lannister | adwd-tyrion-08 |
| haunted by / guilt toward | 1 | Tyrion → Tywin Lannister | adwd-tyrion-08 |
| lingering attachment to | 1 | Tyrion → Tysha | adwd-tyrion-08 |
| guilt and memory regarding | 1 | Tyrion → Symon Silver Tongue (unnamed singer) | adwd-tyrion-08 |
| devotion to memory of | 1 | Penny → Oppo | adwd-tyrion-08 |
| superstitious about | 1 | Ship's crew → Penny | adwd-tyrion-08 |
| targeted dwarfs for bounty | 1 | Cersei → Tyrion | adwd-tyrion-08 |
| forbade Gerion's voyage | 1 | Tywin → Gerion Lannister | adwd-tyrion-08 |
| unrequited devotion (inferred by Tyrion) | 1 | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-09 |
| protective (pragmatic) | 1 | Jorah Mormont → Tyrion and Penny | adwd-tyrion-09 |
| romantic interest / emotional dependence | 1 | Penny → Tyrion | adwd-tyrion-09 |
| guilt and recurring memory | 1 | Tyrion → Shae | adwd-tyrion-09 |
| recurring haunting | 1 | Tyrion → Tywin Lannister | adwd-tyrion-09 |
| warm memory | 1 | Tyrion → Gerion Lannister | adwd-tyrion-09 |
| conflicted memory | 1 | Tyrion → Sansa Stark | adwd-tyrion-09 |
| nostalgia / attraction | 1 | Tyrion → Lemore | adwd-tyrion-09 |
| devotion | 1 | Penny → Pretty Pig and Crunch | adwd-tyrion-09 |
| prophetic authority | 1 | Moqorro → Tyrion | adwd-tyrion-09 |
| hostile/suspicious toward | 1 | Crew → Tyrion | adwd-tyrion-09 |
| Fellow slave / protective toward | 1 | Tyrion → Penny | adwd-tyrion-10 |
| Calculating potential manipulation of | 1 | Tyrion → Brown Ben Plumm | adwd-tyrion-10 |
| Interested in Tyrion (identity/value) | 1 | Brown Ben Plumm → Tyrion | adwd-tyrion-10 |
| Overseer/authority over | 1 | Nurse → Tyrion, Penny, Jorah | adwd-tyrion-10 |
| Master of / possessive toward | 1 | Yezzan zo Qaggaz → His "treasures" (dwarfs, Sweets, others) | adwd-tyrion-10 |
| Favored treasure of | 1 | Sweets → Yezzan zo Qaggaz | adwd-tyrion-10 |
| Conflicted about / doesn't hate | 1 | Tyrion → Jorah Mormont | adwd-tyrion-10 |
| Broken/devastated by news of | 1 | Jorah Mormont → Daenerys Targaryen | adwd-tyrion-10 |
| Rival bidder / predatory buyer | 1 | Zahrina → Jorah Mormont | adwd-tyrion-10 |
| Inferior cyvasse player to | 1 | Brown Ben Plumm → Tyrion | adwd-tyrion-10 |
| Emotionally dependent on | 1 | Penny → Crunch (her dog) | adwd-tyrion-10 |
| Remembers killing | 1 | Tyrion → Shae | adwd-tyrion-10 |
| Poisoned / killed | 1 | Tyrion → Nurse | adwd-tyrion-11 |
| Compares to Sansa Stark | 1 | Tyrion → Penny | adwd-tyrion-11 |
| Strategic approach toward | 1 | Tyrion → Brown Ben Plumm | adwd-tyrion-11 |
| Guilt/responsibility toward | 1 | Tyrion → Ser Jorah Mormont | adwd-tyrion-11 |
| Dominates / violent toward | 1 | Scar → Tyrion | adwd-tyrion-11 |
| Views as moderate | 1 | Tyrion → Yezzan zo Qaggaz | adwd-tyrion-11 |
| Known to / former associate | 1 | Mormont → Brown Ben Plumm | adwd-tyrion-11 |
| Startled/wary of | 1 | Kasporio → Mormont | adwd-tyrion-11 |
| Hostility anticipated from | 1 | Tyrion → Barristan Selmy | adwd-tyrion-11 |
| Previously tried to acquire | 1 | Brown Ben Plumm → Tyrion and Penny | adwd-tyrion-11 |
| Asserts kinship via house allegiance | 1 | Tyrion → Brown Ben Plumm | adwd-tyrion-11 |
| Opposed | 1 | Yezzan zo Qaggaz → Bloodbeard | adwd-tyrion-11 |
| Favored peace with | 1 | Yezzan zo Qaggaz → Meereen | adwd-tyrion-11 |
| Joins/becomes member of | 1 | Tyrion → Second Sons | adwd-tyrion-12 |
| Works for/under | 1 | Tyrion → Inkpots | adwd-tyrion-12 |
| Verbally spars with | 1 | Tyrion → Kasporio | adwd-tyrion-12 |
| Protective concealment of | 1 | Brown Ben → Tyrion | adwd-tyrion-12 |
| Caretaker/guardian toward | 1 | Tyrion → Penny | adwd-tyrion-12 |
| Dependent on/resistant to | 1 | Penny → Tyrion | adwd-tyrion-12 |
| Attachment to | 1 | Penny → Pretty Pig, Crunch | adwd-tyrion-12 |
| Nostalgia for | 1 | Kem → King's Landing / Flea Bottom | adwd-tyrion-12 |
| Fellow member of | 1 | Jorah Mormont → Second Sons | adwd-tyrion-12 |
| Assesses military situation for | 1 | Jorah → Tyrion | adwd-tyrion-12 |
| Plans to manipulate | 1 | Tyrion → Second Sons | adwd-tyrion-12 |
| Idealizes former master | 1 | Penny → Yezzan | adwd-tyrion-12 |
| Corrects/disillusions | 1 | Tyrion → Penny | adwd-tyrion-12 |
| Smith for | 1 | Hammer → Second Sons | adwd-tyrion-12 |
| Apprentice to | 1 | Nail → Hammer | adwd-tyrion-12 |
| Serjeant over | 1 | Snatch → Kem | adwd-tyrion-12 |
| Relies on / uses | 1 | Victarion → Moqorro | adwd-victarion-01 |
| Sexual possession of | 1 | Victarion → The dusky woman | adwd-victarion-01 |
| Distant from | 1 | Victarion → Aeron Greyjoy | adwd-victarion-01 |
| Theological opponent of | 1 | Moqorro → Drowned God religion | adwd-victarion-01 |
| Remembers defeat by | 1 | Victarion → Stannis Baratheon | adwd-victarion-01 |

---

*End of inventory.*
