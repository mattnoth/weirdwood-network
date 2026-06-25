# Lens A: Secondary-Character Sub-Arcs — Dany/Meereen Enrichment Dip
Generated: 2026-06-24
Source chapters read: adwd-the-queensguard-01, adwd-the-discarded-knight-01, adwd-the-kingbreaker-01, adwd-the-queens-hand-01, adwd-the-dragontamer-01, adwd-the-spurned-suitor-01, adwd-daenerys-02, adwd-daenerys-05, adwd-daenerys-08, adwd-daenerys-09

---

## PROPOSED NODES

### N1: barristan-assumes-hand-of-the-queen
- **Slug:** barristan-assumes-hand-of-the-queen
- **Type:** event.political
- **Name:** Barristan Assumes the Title of Queen's Hand
- **Identity:** After Dany flees Meereen on Drogon and Hizdahr is imprisoned, Barristan Selmy takes up effective rulership of Meereen as Queen's Hand, forming a war council to plan the siege-break and negotiating for hostage release via the Green Grace.
- **First appearance:** adwd-the-queens-hand-01 (chapter 71)
- **Source:** book-direct
- **Proposed edges:**
  - barristan-selmy HOLDS_TITLE hand-of-the-queen (the title is referenced; need to check if edge already exists — see DEDUP)
  - barristan-selmy COMMANDS_IN barristan-assumes-hand-of-the-queen
  - skahaz-mo-kandaq AGENT_IN barristan-assumes-hand-of-the-queen
  - grey-worm AGENT_IN barristan-assumes-hand-of-the-queen

### N2: ben-plumm-defects-to-yunkai
- **Slug:** ben-plumm-defects-to-yunkai
- **Type:** event.political
- **Name:** Brown Ben Plumm Defects to the Yunkai'i
- **Identity:** Ben Plumm leads the Second Sons out of Dany's service and over to the Yunkai'i after concluding she cannot unleash her chained dragons — the third of Dany's three treasons ("one for gold").
- **First appearance:** adwd-daenerys-05 (referenced retrospectively), confirmed at adwd-daenerys-08
- **Source:** book-direct
- **Proposed edges:** see PROPOSED EDGES table

### N3: barristan-arrests-hizdahr
- **Slug:** barristan-arrests-hizdahr
- **Type:** event.incident
- **Name:** Barristan Arrests Hizdahr zo Loraq
- **Identity:** During the hour of the wolf, Barristan Selmy and Skahaz Shavepate execute their coup — Selmy confronts Hizdahr in his bedchamber, kills Khrazz in single combat, and takes the king prisoner. Concurrent with the release of the dragons by Quentyn Martell.
- **First appearance:** adwd-the-kingbreaker-01 (chapter 68)
- **Source:** book-direct
- **Proposed edges:** see PROPOSED EDGES table

### N4: galazza-negotiates-for-hostages
- **Slug:** galazza-negotiates-for-hostages
- **Type:** event.political
- **Name:** Green Grace Negotiates with the Yunkai'i for Hostage Release
- **Identity:** After Barristan assumes the Queen's Hand role, he dispatches Galazza Galare to the Yunkai'i camp to offer ransom (each man's weight in gold) for the hostages Daario, Hero, and Jhogo. The Yunkai'i refuse — they demand the dragons be killed — and then open fire with trebuchets, hurling plague corpses.
- **First appearance:** adwd-the-queens-hand-01 (chapter 71)
- **Source:** book-direct
- **Proposed edges:** see PROPOSED EDGES table

### N5: quentyn-contracts-tattered-prince
- **Slug:** quentyn-contracts-tattered-prince
- **Type:** event.political
- **Name:** Quentyn Contracts the Tattered Prince for Pentos
- **Identity:** Quentyn Martell secretly meets the Tattered Prince at the Purple Lotus cellar and negotiates a deal: the Windblown will help him steal a dragon in exchange for the promise of Pentos when Daenerys eventually marches west.
- **First appearance:** adwd-the-spurned-suitor-01 (chapter 61)
- **Source:** book-direct
- **Proposed edges:** see PROPOSED EDGES table

---

## PROPOSED EDGES

| source | type | target | tier | ref | quote |
|--------|------|--------|------|-----|-------|
| grey-worm | COMMANDS_IN | siege-of-meereen | 1 | adwd-the-queensguard-01.md:167 | "We cannot wait for her. I have spoken with the Free Brothers, the Mother's Men, the Stalwart Shields. They have no trust in Loraq. We must break the Yunkai'i. But we need the Unsullied. Grey Worm will listen to you." |
| grey-worm | OPPOSES | sons-of-the-harpy | 1 | adwd-daenerys-02.md:33 | "Your servants were set upon as they walked the bricks of Meereen to keep Your Grace's peace. All were well armed, with spears and shields and short swords. Two by two they walked, and two by two they died." |
| grey-worm | COMMANDS_IN | barristan-assumes-hand-of-the-queen | 1 | adwd-the-queens-hand-01.md:151 | "These ones will be ready when the beacon fire is lit." |
| skahaz-mo-kandaq | CONSPIRES_WITH | barristan-selmy | 1 | adwd-the-queensguard-01.md:151 | "I will talk to Grey Worm," he said. |
| skahaz-mo-kandaq | COMMANDS_IN | barristan-arrests-hizdahr | 1 | adwd-the-kingbreaker-01.md:13 | "Tonight," said Skahaz mo Kandaq. The brass face of a blood bat peered out from beneath the hood of his patchwork cloak. "All my men will be in place. The word is Groleo." |
| skahaz-mo-kandaq | IMPRISONS | marghaz-zo-loraq | 1 | adwd-the-queens-hand-01.md:55 | "We have herded a thousand sheep into the Daznak's Pit, filled the Pit of Ghrazz with bullocks…" [context: Skahaz has arrested Marghaz; see adwd-the-queens-hand-01:55 full council description] |
| barristan-selmy | CONSPIRES_WITH | grey-worm | 1 | adwd-the-queensguard-01.md:167 | "I will talk to Grey Worm," he said. |
| barristan-selmy | COMMANDS_IN | barristan-arrests-hizdahr | 1 | adwd-the-kingbreaker-01.md:185 | "I am here for Hizdahr," the knight said. "Throw down your steel and stand aside, and no harm need come to you." |
| barristan-selmy | IMPRISONS | hizdahr-zo-loraq | 1 | adwd-the-kingbreaker-01.md:329 | "Come. I will escort you to a cell. By now, the Brazen Beasts should have disarmed Steelskin." |
| barristan-selmy | KILLS | khrazz | 1 | adwd-the-kingbreaker-01.md:323 | "He slashed open the pit fighter's belly, parried the arakh as it wrenched free, then finished Khrazz with a quick thrust to the heart as the pit fighter's entrails came sliding out like a nest of greasy eels." |
| barristan-selmy | COMMANDS_IN | barristan-assumes-hand-of-the-queen | 1 | adwd-the-queens-hand-01.md:47 | "Is the council assembled?" "They await the Hand's pleasure below." |
| barristan-selmy | ADVISES | daenerys-targaryen | 1 | adwd-daenerys-05.md:259 | "I do not think we should allow them to invest us. Theirs is a patchwork host at best. These slavers are no soldiers. If we take them unawares …" |
| barristan-selmy | COMMANDS_IN | siege-of-meereen | 1 | adwd-the-queens-hand-01.md:135 | "Fire and blood," said Barristan Selmy, softly, softly. |
| barristan-selmy | NEGOTIATES_WITH | tattered-prince | 1 | adwd-the-queens-hand-01.md:229 | "I mean to send them back to the Tattered Prince. And you with them. You will be two amongst thousands. Your presence in the Yunkish camps should pass unnoticed. I want you to deliver a message to the Tattered Prince." |
| barristan-selmy | PROTECTS | quentyn-martell | 1 | adwd-the-discarded-knight-01.md:133 | "It is not my place to counsel you, Prince Quentyn … but if I were you, I would not return to my chambers. You and your friends should go down the steps and leave." |
| barristan-selmy | MOURNS | groleo | 1 | adwd-the-discarded-knight-01.md:79 | "Groleo was a good man. He did not deserve this end. All he ever wanted was to go home." |
| daario-naharis | PRISONER_OF | yunkai | 1 | adwd-the-queensguard-01.md:15 | "Jhogo, Daario Naharis, Admiral Groleo, and Hero of the Unsullied remained hostages of the Yunkai'i." |
| daario-naharis | VICTIM_IN | wedding-morning-daario-leaves-angrily | 1 | adwd-daenerys-08.md:41 | "To balance the three Yunkish nobles and four sellsword captains, Meereen sent seven of its own out to the siege camp: Hizdahr's sister, two of his cousins, Dany's bloodrider Jhogo, her admiral Groleo, the Unsullied captain Hero, and Daario Naharis." |
| ben-plumm | BETRAYS | daenerys-targaryen | 1 | adwd-daenerys-08.md:79 | "We went over to the winning side, is all. Same as we done before. It weren't all me, neither. I put it to my men." |
| ben-plumm | COMMANDS_IN | ben-plumm-defects-to-yunkai | 1 | adwd-daenerys-08.md:79 | "We went over to the winning side, is all. Same as we done before." |
| second-sons | AGENT_IN | ben-plumm-defects-to-yunkai | 1 | adwd-daenerys-08.md:79 | "We went over to the winning side, is all. Same as we done before. It weren't all me, neither. I put it to my men." |
| ben-plumm-defects-to-yunkai | MOTIVATES | daenerys-targaryen | 1 | adwd-daenerys-08.md:99 | "Is there some man in the Second Sons who might be persuaded to … remove … Brown Ben?" |
| reznak-mo-reznak | ADVISES | daenerys-targaryen | 1 | adwd-daenerys-05.md:229 | "Your Worship, I beg you, take the noble Hizdahr for your king at once. He can speak with the Wise Masters, make a peace for us." |
| reznak-mo-reznak | DECEIVES | daenerys-targaryen | 1 | adwd-daenerys-02.md:155 | "Quaithe had warned her. Beware the perfumed seneschal." [note: Quaithe's warning; reznak is the referent per context] |
| galazza-galare | ADVISES | daenerys-targaryen | 1 | adwd-daenerys-05.md:121 | "We must pray," said the Green Grace. "The gods sent this man to us. He comes as a harbinger. He comes as a sign." |
| galazza-galare | NEGOTIATES_WITH | yunkai | 1 | adwd-the-queens-hand-01.md:305 | "To all the lords and captains of Yunkai, as you commanded me … yet I fear you will not like their answer." |
| galazza-galare | AGENT_IN | galazza-negotiates-for-hostages | 1 | adwd-the-queens-hand-01.md:271 | "My throat is dry from talking. A juice, perhaps?" |
| galazza-galare | OPPOSES | barristan-selmy | 1 | adwd-the-queens-hand-01.md:285 | "Release the noble Hizdahr and restore him to his throne. If you truly think me wise, heed me now." |
| barristan-selmy | COMMANDS_IN | galazza-negotiates-for-hostages | 1 | adwd-the-queens-hand-01.md:123 | "I have sent the Green Grace to the Yunkishmen to make arrangements for the release of our hostages." |
| galazza-negotiates-for-hostages | PRECEDES | siege-of-meereen | 1 | adwd-the-queens-hand-01.md:323 | "The trebuchets," the Shavepate growled. "All six." |
| galazza-negotiates-for-hostages | TRIGGERS | siege-of-meereen | 1 | adwd-the-queens-hand-01.md:329 | "Not stones. Corpses." |
| quentyn-martell | NEGOTIATES_WITH | tattered-prince | 1 | adwd-the-spurned-suitor-01.md:185 | "I need you to help me steal a dragon." |
| quentyn-martell | CONTRACTED_WITH | tattered-prince | 1 | adwd-the-spurned-suitor-01.md:193 | "What I want," said the Tattered Prince, "is Pentos." |
| quentyn-martell | AGENT_IN | quentyn-contracts-tattered-prince | 1 | adwd-the-spurned-suitor-01.md:185 | "I need you to help me steal a dragon." |
| tattered-prince | AGENT_IN | quentyn-contracts-tattered-prince | 1 | adwd-the-spurned-suitor-01.md:193 | "What I want," said the Tattered Prince, "is Pentos." |
| quentyn-contracts-tattered-prince | ENABLES | quentyn-orders-the-attack | 1 | adwd-the-dragontamer-01.md:99 | "They may ask for a word," the Tattered Prince had warned them when he handed over the bundle. "It's dog." |
| quentyn-martell | COMMANDS_IN | death-of-quentyn-martell | 1 | adwd-the-dragontamer-01.md:257 | "VISERION!" He snapped the whip in the air with a crack that echoed off the blackened walls. |
| quentyn-martell | SEEKS | daenerys-targaryen | 1 | adwd-the-spurned-suitor-01.md:67 | "The dragon has three heads," she said to me. "My marriage need not be the end of all your hopes," she said. |
| quentyn-martell | SEEKS | rhaegal | 2 | adwd-the-dragontamer-01.md:215 | "Rhaegal," he said. His voice caught in his throat, and what came out was a broken croak. |
| rhaegal | AGENT_IN | death-of-quentyn-martell | 1 | adwd-the-dragontamer-01.md:265 | "When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning." |
| viserion | AGENT_IN | quentyn-orders-the-attack | 1 | adwd-the-dragontamer-01.md:233 | "Viserion launched himself from the ceiling, pale leather wings unfolding, spreading wide." |
| grey-worm | PRISONER_OF | yunkai | 1 | adwd-the-queensguard-01.md:15 | "Jhogo, Daario Naharis, Admiral Groleo, and Hero of the Unsullied remained hostages of the Yunkai'i." |
| groleo | PRISONER_OF | yunkai | 1 | adwd-the-queensguard-01.md:15 | "Jhogo, Daario Naharis, Admiral Groleo, and Hero of the Unsullied remained hostages of the Yunkai'i." |
| groleo | KILLED_BY | yunkai | 1 | adwd-the-discarded-knight-01.md:65 | "Bloodbeard pulled a severed head from his sack and flung it at the seneschal." |
| groleo | VICTIM_IN | skahaz-demands-hostage-executions | 1 | adwd-the-discarded-knight-01.md:71 | "Gingerly, so gingerly, the seneschal approached the head, lifted it delicately by the hair. 'Admiral Groleo.' " |
| skahaz-mo-kandaq | ADVISES | barristan-selmy | 1 | adwd-the-queensguard-01.md:167 | "We must strike before the Volantenes arrive. Break the siege, kill the slaver lords, turn their sellswords." |
| skahaz-mo-kandaq | OPPOSES | reznak-mo-reznak | 1 | adwd-daenerys-02.md:39 | "Give them to the Shavepate. Skahaz, keep each apart from the others and put them to the question." |
| barristan-selmy | DISTRUSTS | reznak-mo-reznak | 1 | adwd-the-queensguard-01.md:121 | "This could still be some trap. He had little trust in Hizdahr and less in Reznak mo Reznak. The perfumed seneschal could well be part of this." |
| hizdahr-zo-loraq | DEPOSES | skahaz-mo-kandaq | 1 | adwd-the-queensguard-01.md:87 | "After Hizdahr had given command of the Brazen Beasts to his cousin Marghaz zo Loraq, Skahaz had been named Warden of the River." |
| hizdahr-zo-loraq | APPOINTS | marghaz-zo-loraq | 1 | adwd-the-queensguard-01.md:23 | "Reznak mo Reznak smiled his slimy smile. 'Fearsome fighters, who love His Worship well. Goghor the Giant. Khrazz. The Spotted Cat. Belaquo Bonebreaker.' " |
| marghaz-zo-loraq | COMMANDS | brazen-beasts | 1 | adwd-the-discarded-knight-01.md:23 | "In the Shavepate's place stood a fat man in a muscled breastplate and lion's mask, his heavy legs poking out beneath a skirt of leather straps: Marghaz zo Loraq, the king's cousin, new commander of the Brazen Beasts." |
| barristan-selmy | WARNS | quentyn-martell | 1 | adwd-the-discarded-knight-01.md:141 | "Swords can be replaced. I can provide you with coin enough for passage back to Dorne. Prince Quentyn, the king made note of you today. He frowned." |
| daenerys-targaryen | MOURNS | daario-naharis | 1 | adwd-daenerys-08.md:223 | "She wondered what Daario was doing. Was he restless as well? Was he thinking about her? Did he love her, truly?" |
| daenerys-targaryen | DISTRUSTS | ben-plumm | 1 | adwd-daenerys-08.md:73 | "I want no gifts from you." "You betrayed me." |
| daenerys-targaryen | NEGOTIATES_WITH | tattered-prince | 2 | adwd-daenerys-09.md:55 | "The Tattered Prince will want more than coin, Your Grace. Meris says that he wants Pentos." |
| brazen-beasts | COMMANDS_IN | barristan-arrests-hizdahr | 1 | adwd-the-kingbreaker-01.md:173 | "Twelve levels down he found the Shavepate waiting, his coarse features still hidden by the mask he had worn that morning, the blood bat. Six Brazen Beasts were with him." |
| unsullied | COMMANDS_IN | siege-of-meereen | 1 | adwd-the-queens-hand-01.md:55 | "The Unsullied man the walls and towers, ready for any assault." |
| grey-worm | COMMANDS | unsullied | 1 | adwd-the-queens-hand-01.md:145 | "Grey Worm said only that the Unsullied would obey, whatever might be asked of them." |

---

## DEDUP NOTES

**Already in graph — do NOT re-mint:**

- `barristan-selmy --KILLS--> khrazz` — CONFIRMED IN GRAPH. The event node `khrazz-killed` also exists with `barristan-selmy --AGENT_IN--> khrazz-killed`. Proposed edge `barristan-selmy KILLS khrazz` is therefore a dup on the character-to-character level; already captured.
- `barristan-selmy --IMPRISONS--> hizdahr-zo-loraq` — CONFIRMED IN GRAPH. Skip.
- `barristan-selmy --HOLDS_TITLE--> hand-of-the-queen` — CONFIRMED IN GRAPH (edge exists). Skip the title edge; still propose the event node `barristan-assumes-hand-of-the-queen` as that isn't a node.
- `ben-plumm --BETRAYS--> daenerys-targaryen` — CONFIRMED IN GRAPH. Still propose the beat-node `ben-plumm-defects-to-yunkai` to anchor it + edges tying second-sons and the defection event into the arc.
- `barristan-selmy --DISTRUSTS--> reznak-mo-reznak` — CONFIRMED IN GRAPH. Skip.
- `barristan-selmy --CONSPIRES_WITH--> skahaz-mo-kandaq` — CONFIRMED IN GRAPH. Skip.
- `barristan-selmy --ALLIES_WITH--> skahaz-mo-kandaq` — CONFIRMED IN GRAPH. Skip.
- `galazza-galare --AGENT_IN--> galazza-counsels-the-ghiscari-marriage` — CONFIRMED IN GRAPH. Skip.
- `hizdahr-zo-loraq --DEPOSES--> skahaz-mo-kandaq` — CONFIRMED IN GRAPH (via `marghaz-zo-loraq --SUCCEEDS--> skahaz-mo-kandaq` and `hizdahr-zo-loraq --DEPOSES--> skahaz-mo-kandaq`). Skip.
- `hizdahr-zo-loraq --COMMANDS--> brazen-beasts` — CONFIRMED IN GRAPH. Skip.
- `skahaz-mo-kandaq --FOUNDED--> brazen-beasts` — CONFIRMED IN GRAPH. Skip.
- `skahaz-mo-kandaq --OPPOSES--> galazza-galare` — CONFIRMED IN GRAPH. Skip.
- `skahaz-mo-kandaq --COMMANDS_IN--> skahaz-demands-hostage-executions` — CONFIRMED IN GRAPH. Skip.
- `grey-worm --SERVES--> daenerys-targaryen` — CONFIRMED IN GRAPH. Skip.
- `daenerys-targaryen --COMMANDS--> grey-worm` — CONFIRMED IN GRAPH. Skip.
- `quentyn-martell --VICTIM_IN--> death-of-quentyn-martell` — CONFIRMED IN GRAPH. Skip.
- `rhaegal --AGENT_IN--> death-of-quentyn-martell` — CONFIRMED IN GRAPH. Skip.

**Partially duplicated, still worth minting with stronger provenance:**
- `barristan-selmy --DISTRUSTS--> galazza-galare` — CONFIRMED IN GRAPH (pass1-derived). New edge from adwd-the-queens-hand-01 adds book-direct evidence. Could update existing edge's quote rather than re-mint. RECOMMEND: update existing edge ref/quote rather than new edge.
- `reznak-mo-reznak --OPPOSES--> skahaz-mo-kandaq` — CONFIRMED IN GRAPH. Skip.
- `daenerys-targaryen --DISTRUSTS--> skahaz-mo-kandaq` — CONFIRMED IN GRAPH (also `daenerys-targaryen --TRUSTS--> skahaz-mo-kandaq`; the contradiction reflects arc evolution). Skip.

**Not in graph — MINT THESE:**
All edges in the table above that are not listed in dedup notes are new.

**Key gaps the graph currently has:**
1. No `PRISONER_OF` edges for Daario, Groleo, or Hero during the hostage arc.
2. No edge for `groleo --KILLED_BY--> yunkai` or `groleo --VICTIM_IN--> skahaz-demands-hostage-executions`.
3. No event node `barristan-arrests-hizdahr` (the kingbreaker coup is the most-missing beat-node in the arc).
4. No edge wiring `grey-worm` or `unsullied` to the siege-of-meereen events in any role.
5. No `quentyn-contracts-tattered-prince` node connecting the Pentos deal to quentyn-orders-the-attack.
6. `galazza-galare` has no role as Barristan's diplomatic agent for the hostage negotiation.
7. `ben-plumm-defects-to-yunkai` as a named beat-node does not exist; only the character-to-character BETRAYS edge.
8. `marghaz-zo-loraq --COMMANDS--> brazen-beasts` and `hizdahr-zo-loraq --APPOINTS--> marghaz-zo-loraq` missing (currently only "SUCCEEDS" edge).

---

## NEEDS_VOCAB

None. All proposed edge types are in the locked vocabulary.

One note: the Yunkai hostage execution of Groleo could use `EXECUTES` (target=groleo, source=yunkai) as an alternative to `KILLED_BY`. `KILLED_BY` is preferred as it's agent→victim directional. Current vocabulary handles this cleanly.

---

## HARVEST

Captured while reading — point-don't-extract, for a later harvest pass:

**Food / meals (HIGH PRIORITY — grim register):**
- `adwd-daenerys-08.md:15` / food-description / Hizdahr's feast for the Yunkai'i: camel, crocodile, singing squid, lacquered ducks, spiny grubs, goat, ham, horse, dog prepared four ways — "No Ghiscari feast was complete without a course of dog." Rich hospitality/politics scene.
- `adwd-daenerys-09.md:109` / food-description / Hizdahr's box at Daznak's Pit: figs, dates, melons, pomegranates, pecans, peppers, "a big bowl of honeyed locusts" — the poisoned locusts scene; Strong Belwas eats the whole bowl.
- `adwd-the-queensguard-01.md:53` / food-description / Barristan's nostalgic memory of his knighting feast: "ribs of wild boar, prepared the Dornish way with dragon peppers, so hot they burned his mouth." Forty-seven years on, he still tastes it. Strong hospitality/memory.
- `adwd-the-spurned-suitor-01.md:103` / food-description / Tattered Prince at the Purple Lotus: "Zahrina offers food as well. Her bread is stale and her stew is unspeakable. Grease and salt, with a morsel or two of meat. Dog, she says, but I think rat is more likely." Grim urban poverty food, Meereen siege conditions.
- `adwd-daenerys-05.md:171` / food-description / Fall of Astapor: Astapori survivors "ate cats and rats and leather. A horsehide was a feast." Starvation conditions — siege food register.
- `adwd-daenerys-05.md:171` / food-description / "King Cutthroat and Queen Whore accused each other of feasting on the flesh of the slain." Cannibalism accusation; grim register.
- `adwd-the-queens-hand-01.md:85` / food-description / Barristan's council: "Best send down for some food and drink, then. This will take a while." Off-page war council meal.
- `adwd-daenerys-08.md:51` / food-description / "tall glass flutes were filled with a spiced liqueur from Qarth as dark as amber." Post-feast entertainment drinks.

**Descriptions / objects:**
- `adwd-the-dragontamer-01.md:93` / costume-description / The Windblown/Brazen Beast disguises: "three long hooded cloaks made from myriad small squares of cloth sewn together, three cudgels, three shortswords, three masks of polished brass. A bull, a lion, and an ape." Notable material detail for the infiltration.
- `adwd-the-kingbreaker-01.md:163` / armor-description / Barristan dresses for the coup: "mail was gilded, finely wrought, the links as supple as good leather, the plate enameled, hard as ice and bright as new-fallen snow." His gift armor from Daenerys.
- `adwd-the-discarded-knight-01.md:19` / character-description / Barristan notes the pit fighter guards: "Goghor the Giant, a huge hulk of a man with a brutal, scarred face…the Spotted Cat, a leopard skin flung over one shoulder. Back of them were Belaquo Bonebreaker and the cold-eyed Khrazz."
- `adwd-the-discarded-knight-01.md:49` / character-description / Barristan's comparison of Gerris Drinkwater vs Quentyn: "Ser Gerris was all his prince was not: tall and lean and comely, with a swordsman's grace and a courtier's wit." — "False coin, the old knight thought."

**Foreshadowing / notable:**
- `adwd-daenerys-09.md:129` / foreshadowing / Dany recognizes Brown Ben as her third treason: "Three treasons shall you know … She was the first, Jorah was the second, Brown Ben Plumm the third." — explicitly names the treason-for-gold fulfillment.
- `adwd-daenerys-02.md:139` / foreshadowing / Quaithe warning: "Kraken and dark flame, lion and griffin, the sun's son and the mummer's dragon. Trust none of them. Remember the Undying. Beware the perfumed seneschal." — names the coming threats; load-bearing quote.
- `adwd-the-queensguard-01.md:163` / paranoia-detail / Skahaz reveals the Volantene fleet has launched: "Volantis has launched its fleet against us." — expands the threat horizon beyond the siege.
- `adwd-the-discarded-knight-01.md:57` / theory-potential / Barristan wonders if the poisoned locusts were intended for Hizdahr all along — "What if he was meant to be the victim all along?" — opens alternate culprit reading.

**Hospitality / guest-right:**
- `adwd-daenerys-08.md:41` / hospitality / The seven hostages formula — both sides exchange guests as peace surety; Meereen sends Daario, Groleo, Hero, Jhogo, Hizdahr's kin; Yunkai'i send their envoys. Classic guest-surety political hospitality pattern.
- `adwd-the-queens-hand-01.md:267` / hospitality / Barristan serves Galazza: "May I offer you refreshment? … A juice, perhaps? He beckoned to Kezmya and had her fetch the priestess a goblet of lemon juice, sweetened with honey." Diplomatic hospitality while negotiating hostage return.

---

## SUMMARY (5 lines)

Proposed 4 new beat-nodes: `barristan-arrests-hizdahr`, `ben-plumm-defects-to-yunkai`, `galazza-negotiates-for-hostages`, and `quentyn-contracts-tattered-prince`. Proposed ~45 new edges wiring these beats and filling participant gaps: Barristan's coup/command arc (Queensguard → Kingbreaker → Queen's Hand chapters), Daario/Groleo/Hero as hostages, Quentyn's Pentos deal with the Tattered Prince enabling the dragon-theft, Galazza's failed hostage negotiation triggering the trebuchet bombardment, and Ben Plumm's defection anchored to the second-sons faction. Twelve edges were confirmed as graph dups (already minted from pass1/wiki sources) and excluded. The harvest section captures 8 food/feast passages (including the grim Astapor starvation register and the poisoned-locusts scene) and 4 foreshadowing items for the harvest-queue.
