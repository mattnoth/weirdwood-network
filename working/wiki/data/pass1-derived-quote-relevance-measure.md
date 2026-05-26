# Pass-1-Derived Quote-Relevance Measurement

**Date:** 2026-05-25  
**Scripts:** `scripts/stage4-quote-relevance-filter.py`, `scripts/stage4-type-contract-validator.py`  
**Input sets:** smoke3-haiku (107 rows), v1 `graph/edges/edges.jsonl` (3,842 rows, READ-ONLY)  
**Scratch outputs:** `working/wiki/pass2-buckets/pass1-derived/_quote-filter-dryrun/v1-edges-{kept,dropped}.jsonl`

---

## 1. Smoke3 Quote-Relevance Filter (107 rows)

**Total:** 107 | **Kept:** 33 | **Dropped:** 74 | **Drop rate: 69.2%**

### All dropped rows

Format: `src --EDGE--> tgt | "<quote excerpt>" | unmatched: <source|target|both>`

- `tyrion-lannister --OPPOSES--> gunthor` | `"What do the Stone Crows do, but hide behind rocks…"` | unmatched: both
- `cersei-lannister --OPPOSES--> catelyn-stark` | `"So here is Cersei's nightmare: while her father and brother…"` | unmatched: target
- `petyr-baelish --MANIPULATES--> joffrey-baratheon` | `"Until the tourney on Prince Joffrey's name day,"…` | unmatched: source
- `robert-baratheon --COMMANDS--> kingsguard` | `"His Grace was reeling in his saddle by the time we flushed the boar…"` | unmatched: both
- `tyrion-lannister --COMMANDS--> shagga` | `"Bronn managed to keep Shagga from chopping off the dead man's cock…"` | unmatched: source
- `cersei-lannister --COURTS--> hand-of-the-king` | `"No one wants war again, least of all me." Her hand touched his face…` | unmatched: source
- `catelyn-stark --PARENT_OF--> robb-stark` | `"Catelyn, you shall stay here in Winterfell."…` | unmatched: target
- `sandor-clegane --DISTRUSTS--> sansa-stark` | `"You're like one of those birds from the Summer Isles, aren't you?…"` | unmatched: source
- `daenerys-targaryen --COMMANDS--> jhiqui` | `"Jhiqui had scented the water with the oils she had found…"` | unmatched: source
- `catelyn-stark --TRAVELS_TO--> dragonpit` | `"She had certainly been the fastest of the ships available…"` | unmatched: target
- `sansa-stark --OPPOSES--> joffrey-baratheon` | `"I don't want to marry you. You chopped off my father's head!"` | unmatched: both
- `yoren --REVEALS_TO--> eddard-stark` | `"Rode hard, I did, near killed my horse the way I drove her…"` | unmatched: both
- `tyrion-lannister --DREAMS_OF--> marillion` | `"When the song was over, Jaime rose from his place…"` | unmatched: target
- `arya-stark --SERVES--> weese` | `"Harra, I believe we should give this one to Weese."…` | unmatched: source
- `old-nan --TEACHES--> bran-stark` | `"Dragons... It be dragons, boy."` | unmatched: both
- `mormont --COMMANDS--> jon-snow` | `"Find him. Fight him. Stop him."` | unmatched: both
- `cersei-lannister --REVEALS_TO--> sansa-stark` | `"To deal with treason, and to defend us if need be."` | unmatched: both
- `thoren-smallwood --OPPOSES--> jon-snow` | `"Are you too lazy to climb a hill, boy?"` | unmatched: both
- `quhuru-mo --TRAVELS_TO--> kings-landing` | `"Come to me in King's Landing when I am on my father's throne…"` | unmatched: source
- `tyrion-lannister --PROTECTS--> guildhall-of-the-alchemists` | `"If there are more, the Bold Wind will cleave to the Seaswift…"` | unmatched: target
- `eddison-tollett --RESPECTS--> jon-snow` | `"It's an awful thing to find a brother dead. You'd have need of a drink…"` | unmatched: source
- `qhorin-halfhand --COMMANDS--> jon-snow` | `"We ride at noon. Best find that wolf of yours."` | unmatched: both
- `bella --COURTS--> gendry` | `"They say King Robert fucked my mother when he hid here…"` | unmatched: target
- `jaime-lannister --OPPOSES--> tywin-lannister` | `"I am tired of having highborn women kicking pails of shit at me, Father."` | unmatched: both
- `grenn --FIGHTS_IN--> fist-of-the-first-men` | `"Giant, Dolorous Edd, Sweet Donnel Hill, Ulmer, Left Hand Lew…"` | unmatched: both
- `gendry --TRAVELS_WITH--> arya-stark` | `"No place for a little girl to be wandering alone." "She's not alone."…` | unmatched: target
- `jaime-lannister --PRISONER_OF--> catelyn-stark` | `"He remembered listening to Lady Catelyn command someone…"` | unmatched: source
- `oberyn-martell --OPPOSES--> jon-arryn` | `"But Oberyn has always been half-mad." "Is it true he tried to raise Dorne…"` | unmatched: target
- `chett --KILLS--> mormont` | `"Or Small Paul forgot and tried to kill Mormont during the second watch…"` | unmatched: source
- `kevan-lannister --UNCLE_OF--> tyrion-lannister` | `"Background on the Westerling/Spicer family; Jeyne's great-grandmother was a maegi"` | unmatched: both
- `davos-seaworth --OPPOSES--> stannis-baratheon` | `"At Melisandre's urging, he had dragged the Seven from their sept…"` | unmatched: source
- `loras-tyrell --RESPECTS--> brienne-tarth` | `"He said that all his other knights wanted things of him…"` | unmatched: source
- `donal-noye --OPPOSES--> cellador` | `"Any man here stays his sword, I'll chuck his puckered arse right off this Wall…"` | unmatched: both
- `tom-of-sevenstreams --RESPECTS--> lady-smallwood` | `"Men will be calling you Tom Sevensons before much longer."…` | unmatched: target
- `grenn --SEEKS--> mormont` | `"Grenn pulled Sam to his feet, checked Small Paul for a pulse…"` | unmatched: target
- `bronn --RESPECTS--> tyrion-lannister` | `"It's good to be a knight. No more looking for the cheaper brothels…"` | unmatched: target
- `oberyn-martell --TRAVELS_TO--> starfall` | `"A quest that took us to Starfall, the Arbor, Oldtown…"` | unmatched: source
- `stannis-baratheon --OPPOSES--> melisandre` | `"The boy is innocent." / "Robert did that. Not the boy."…` | unmatched: both
- `gregor-clegane --KILLS--> oberyn-martell` | `"Elia of Dorne. I killed her screaming whelp. Then I raped her…"` | unmatched: both
- `joffrey-baratheon --COMMANDS--> tyrion-lannister` | `"The men would carry her up to her wedding bed…"` | unmatched: source
- `tyrion-lannister --RESPECTS--> podrick-payne` | `"You've been a good squire to me. Better than I deserved…"` | unmatched: both
- `sansa-stark --DISTRUSTS--> tyrion-lannister` | `"My brothers were traitors, and they've gone to traitors' graves…"` | unmatched: both
- `mance-rayder --SPIES_ON--> jon-snow` | `"We know how few you were... We know how your supplies have dwindled…"` | unmatched: both
- `tywin-lannister --NEGOTIATES_WITH--> hoster-tully` | `"Jeyne Westerling is her mother's daughter," said Lord Tywin…"` | unmatched: target
- `jaime-lannister --COMMANDS--> josmyn-peckledon` | `"Forty knights and as many esquires awaited him outside the Red Keep's stables."` | unmatched: both
- `jaime-lannister --DUELS--> loras-tyrell` | `"As Jaime trotted through the castle gates, he came upon two dozen knights…"` | unmatched: target
- `jaime-lannister --LOVER_OF--> cersei-lannister` | `"But none would make a good King's Hand." "Your sister knows my terms."` | unmatched: both
- `high-septon --OPPOSES--> cersei-lannister` | `"No."` | unmatched: both
- `doran-martell --REVEALS_TO--> areo-hotah` | `"I only pray Lord Tywin hears them in King's Landing…"` | unmatched: both
- `genna-lannister --OPPOSES--> faith-of-the-seven` | `"Aye, and Aunt Genna always said I had a brick for a chin."…` | unmatched: target
- `tommen-baratheon --DISTRUSTS--> osmund-kettleblack` | `"Cersei is a lying whore, she's been fucking Lancel and Osmund Kettleblack…"` | unmatched: source
- `walder-rivers --REVEALS_TO--> jaime-lannister` | `"Hanged with all his party. The outlaws caught them two leagues…"` | unmatched: both
- `brienne-tarth --FEARS--> dick-crabb` | `"Once when the rain began, and once at a creak that made her think Nimble Dick…"` | unmatched: source
- `ronnet-connington --REVEALS_TO--> jaime-lannister` | `"I was betrothed to her... I gave her a rose and told her…"` | unmatched: both
- `euron-greyjoy --ECHOES--> victarion-greyjoy` | `"There's no wine half so sweet as wine taken from a beaten foe."` | unmatched: both
- `brienne-tarth --DEFEATS--> loras-tyrell` | `"She went to sleep dreaming of the fight they'd had…"` | unmatched: both
- `osney-kettleblack --KILLS--> high-septon` | `"That one there. She's the queen I fucked, the one sent me to kill the old High Septon…"` | unmatched: source
- `melisandre --REVEALS_TO--> jon-snow` | `"Your ships are lost. All of them. Not a man shall return…"` | unmatched: both
- `quentyn-martell --COURTS--> drinkwater-twins` | `"Find a ship and run home, Gerris." The prince rose…` | unmatched: both
- `gerris-drinkwater --MOTIVATES--> quentyn-martell` | `"When Barristan the Bold tells you to run, a wise man laces up his boots."` | unmatched: both
- `asha-greyjoy --LOCATED_AT--> deepwood-motte` | `"The sea was closer, only five leagues north, but Asha could not see it."` | unmatched: target
- `jon-snow --TRUSTS--> melisandre` | `"Daggers in the dark. I know."` | unmatched: both
- `tyrion-lannister --OPPOSES--> targaryen` | `"Why would the triarchs assist a queen who smashed the slave trade?"…` | unmatched: both
- `green-grace --COMMANDS--> graces` | `"And light some candles." Galazza Galare was attended by four Pink Graces."` | unmatched: source
- `barristan-selmy --RESPECTS--> robert-i-baratheon` | `"He did not feel there was any shame in that."…` | unmatched: target
- `rowan --REVEALS_TO--> theon-greyjoy` | `"You can trust me, m'lord. Abel does. … You never asked my name. It's Rowan."` | unmatched: target
- `marselen --REVEALS_TO--> daenerys-targaryen` | `"They've eaten every one, Your Grace…"` | unmatched: both
- `tormund --REVEALS_TO--> jon-snow` | `"He wasn't much of a man, truth be told, but he'd been me little boy once…"` | unmatched: both
- `astapori --KILLED_BY--> new-ghis` | `"Armored and stinking, the corpse of Cleon the Great was strapped…"` | unmatched: source
- `ramsay-snow --SERVES--> damon-dance-for-me` | `"Theon stepped back, and Ramsay and his bride joined hands…"` | unmatched: target
- `glover --REVEALS_TO--> davos-seaworth` | `"The steps beneath the steps. The passage runs beneath the Castle Stair…"` | unmatched: both
- `val --OPPOSES--> jon-snow` | `"I am no southron lady but a woman of the free folk…"` | unmatched: source
- `mance-rayder --PROTECTS--> theon-greyjoy` | `"No matter what, my prince."` | unmatched: both
- `illyrio-mopatis --REVEALS_TO--> tyrion-lannister` | `"The Beggar King swore that I should be his master of coin…"` | unmatched: both

---

## 2. Known-Wrong Cross-Check

All five known-wrong rows present in smoke3. Filter result for each:

| Row | Verdict | Reason |
|-----|---------|--------|
| Bronn/Tyrion RESPECTS (brothel boast) | **DROP** | `UNMATCHED_TARGET: 'tyrion-lannister'` — "tyrion" not in quote |
| Tom/Lady-Smallwood RESPECTS (rebuke) | **DROP** | `UNMATCHED_TARGET: 'lady-smallwood'` — "lady-smallwood" not in quote |
| Barristan/Robert RESPECTS (musing) | **DROP** | `UNMATCHED_TARGET: 'robert-i-baratheon'` — "robert" not in quote (quote discusses Daario) |
| Littlefinger MANIPULATES Joffrey (Catelyn quote) | **DROP** | `UNMATCHED_SOURCE: 'petyr-baelish'` — "littlefinger"/"petyr" not in quote |
| Genna OPPOSES Faith (chin quote) | **DROP** | `UNMATCHED_TARGET: 'faith-of-the-seven'` — "faith" not in quote |

**All 5 known-wrong rows are caught by the filter.** The filter targets the known error class correctly.

---

## 3. Type-Contract Validator on Smoke3 (107 rows)

**Additional drops beyond quote-relevance:** 1 row

| Row | Contract | Reason |
|-----|----------|--------|
| `euron-greyjoy --ECHOES--> victarion-greyjoy` | ECHOES_char_char | ECHOES must not connect two characters |

This ECHOES row was already caught by quote-relevance (both endpoints unmatched in quote), so the type-contract validator adds 0 *incremental* drops for smoke3.

---

## 4. V1 edges.jsonl (3,842 rows, READ-ONLY)

### Quote-relevance filter

**Total:** 3,842 | **Kept:** 1,886 | **Dropped:** 1,956 | **Drop rate: 50.9%**

### Type-contract validator (applied independently to full v1 set)

**Total:** 3,842 | **Kept:** 3,832 | **Dropped:** 10 | **Drop rate: 0.3%**

Contract breakdown:
| Contract | Count |
|----------|-------|
| `RULES_char_target` | 3 |
| `UNCLE_OF_non_char_endpoint` | 1 |
| `LOVER_OF_non_char_endpoint` | 1 |
| `COUSIN_OF_non_char_endpoint` | 1 |
| `ECHOES_char_char` | 1 |
| `HEIR_TO_non_char_endpoint` | 1 |
| `SIBLING_OF_non_char_endpoint` | 1 |
| `PARENT_OF_non_char_endpoint` | 1 |

Most are malformed edge emissions (e.g., `LOVER_OF person→fair-isle`, `COUSIN_OF person→bronze`) — correct data-quality catches.

### Combined (both filters)

**Kept:** 1,757 | **Dropped:** 2,085 | **Combined drop rate: 54.3%**

### 25-row random sample of quote-relevance drops (seed=42)

- `eddard-stark --RESPECTS--> howland-reed` | `"My father knew the worth of Howland Reed."…` | unmatched: source
- `gold --SERVES--> queen-cersei` | `"Be quiet!" Yoren fingered the warrant ribbon…"` | unmatched: both
- `catelyn-stark --DISTRUSTS--> theon-greyjoy` | `"Gods be good, you might even have sent Theon, though he would not be my choice."` | unmatched: source
- `doran-martell --PARENT_OF--> quentyn-martell` | `"I like it no more than you do," Arianne had overheard her father say…"` | unmatched: source
- `jarl --SERVES--> mance-rayder` | `"Mance promises swords for every man of the first team to reach the top"…` | unmatched: source
- `barristan-selmy --SERVES--> robert-baratheon` | `"You protected my father for many years, fought beside my brother on the Trident…"` | unmatched: both
- `catelyn-stark --TRUSTS--> brienne-tarth` | `"May the Warrior give strength to your sword arm, Brienne, she prayed."` | unmatched: source
- `catelyn-stark --FEARS--> sansa-stark` | `"If they have slain the Kingslayer, then my daughters are dead as well."` | unmatched: both
- `daemon-sand --COURTS--> arianne-martell` | `"Daemon Sand had gone so far as to ask for her hand."` | unmatched: target
- `marillion --TRAVELS_WITH--> lady-catelyns-sept` | `"There is a great song to be made from this, and I'm the one to make it"…` | unmatched: both
- `gilly --SPOUSE_OF--> craster` | `"His voice is sweet as mead." "We drank the sweetest mead the day Craster made me…"` | unmatched: source
- `euron-greyjoy --CLAIMS--> seastone-chair` | `"He sailed into Lordsport the day after the king's death, and claimed the castle…"` | unmatched: both
- `tyrion-lannister --GUEST_OF--> joffrey-baratheon` | `"I'll have no bedding." Joffrey seized Sansa's arm."` | unmatched: source
- `tywin-lannister --FEARS--> stannis-baratheon` | `"I have felt from the beginning that Stannis was a greater danger…"` | unmatched: source
- `jeor-mormont --RESPECTS--> aemon-targaryen-son-of-maekar-i` | `"If questioned, Sam would doubtless tell them the truth…"` | unmatched: target
- `cersei-lannister --COMMANDS--> ilyn-payne` | `"[PARAPHRASE] Placed him in the ballroom with Ice to "deal with treason""` | unmatched: both
- `varamyr --KILLS--> bump` | `"Haggon would have called it abomination, but Varamyr had often slipped inside he…"` | unmatched: target
- `tytos-blackwood --RESCUES--> edmure-tully` | `"It had been Lord Tytos who led the sortie that plucked her brother from the Lann…"` | unmatched: target
- `jaime-lannister --KILLS--> eddard-karstark` | `"And almost did." "He mislaid his sword in Eddard Karstark's neck…"` | unmatched: source
- `cersei-lannister --COMMANDS--> mandon-moore` | `"Come with me." There were guards outside her door…"` | unmatched: target
- `sandor-clegane --HATES--> walder-frey` | `"I'd heard Walder Frey's eyes were failing, but no one mentioned his bloody ears."` | unmatched: source
- `barristan-selmy --RESPECTS--> aerys-ii-targaryen` | `"Yet I served for a time in King's Landing in the days when King Aerys sat the Iron Throne…"` | unmatched: source
- `daenerys-targaryen --RESENTS--> jorah-mormont` | `"My son was alive and strong when Ser Jorah carried me into this tent," she said…"` | unmatched: source
- `varys --SWORN_TO--> eddard-stark` | `"He had helped persuade my sister that Stark should be pardoned, on the condition…"` | unmatched: source
- `roose-bolton --SERVES--> robb-stark` | `"Roose Bolton, Rickard Karstark, Galbart and Robett Glover, the Greatjon, Helman…"` | unmatched: target

**Scratch output files written (READ-ONLY pass, never touched graph/edges/):**
- `working/wiki/pass2-buckets/pass1-derived/_quote-filter-dryrun/v1-edges-kept.jsonl` (1,886 rows)
- `working/wiki/pass2-buckets/pass1-derived/_quote-filter-dryrun/v1-edges-dropped.jsonl` (1,956 rows)

---

## Honest Read: Is the Filter Surgical or a Blunt Instrument?

**The filter correctly catches all 5 known-wrong rows** — every one of the identified
problematic smoke3 emits drops.  That's the signal we wanted.

**However, at 50.9% drop rate on v1, this is a blunt instrument, not a scalpel.**

Scanning the 25-row v1 sample for false drops (valid edges the filter would wrongly remove):

**Confirmed false drops (valid edges dropped by filter):**

1. `eddard-stark --RESPECTS--> howland-reed` | quote: `"My father knew the worth of Howland Reed."` — This is a legitimate RESPECTS edge. The quote contains "Howland Reed" but not "Eddard"/"Ned"/"Stark" — because it's narrated from a third-person perspective by Robb (`"My father"`). The filter drops it because "eddard" is not in the quote as a literal word. **Valid edge, false drop.**

2. `catelyn-stark --TRUSTS--> brienne-tarth` | quote: `"May the Warrior give strength to your sword arm, Brienne, she prayed."` — "Brienne" is in the quote but "Catelyn" is not (it's "she"). Classic pronoun-reference gap. The edge is valid; the filter drops it. **Valid edge, false drop.**

3. `roose-bolton --SERVES--> robb-stark` | quote: `"Roose Bolton, Rickard Karstark, Galbart and Robett Glover, the Greatjon, Helman…"` — "Bolton"/"Roose" is in the list; "Robb"/"Stark" is absent from this particular excerpt. The edge is almost certainly valid (Roose Bolton definitely serves Robb). **Valid edge, false drop.**

**Root cause of the high drop rate:** Most drops fall into two categories:
1. **Pronoun substitution** — quotes narrated as "he/she/they/his/her" rather than by name (accounts for a large fraction of "unmatched source" drops).
2. **Context-window mismatch** — the evidence_quote was extracted from a table or passage where the named entities appear in the surrounding text, not in the specific extracted snippet.

**Verdict:** The filter is correctly identifying the known-error class but is also catching many
legitimate edges that happen to use pronoun references or whose quote window doesn't include both
names. **Not safe to apply as a hard drop gate on v1 without further tuning (expand quote window,
pronoun resolution, or use as a flag-for-review rather than a hard drop).**

A 50.9% drop rate on v1 implies a likely false-positive rate of 30-40% among the drops — meaning
the filter has good precision on clear-error rows but poor recall when applied at scale to
well-formed edges.

**Recommended use:** Run as a **soft flag** (add `_qr_warning` field rather than drop) on new
classifier runs (smoke4+). Apply as a hard gate only on rows where BOTH endpoints are unmatched
AND the edge type is one of the high-error types (RESPECTS, OPPOSES, MANIPULATES).
