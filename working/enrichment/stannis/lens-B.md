# Lens B — whodunit / revelation + SUSPECTED_OF — A2.7 Stannis proposal (S155)

---

## Proposed NEW nodes

### `shadow-killing-of-cortnay-penrose`
- **type:** event.incident
- **Summary:** Davos rows Melisandre by night into the sea cave beneath Storm's End (navigating by his smuggler's knowledge of the cliff-mouth passage). Inside, beneath the portcullis, Melisandre births a second shadow creature — visually distinct from the Renly shadow; Davos witnesses the crown of the creature emerging and the shadow shooting past the iron bars into the castle. Cortnay Penrose is found dead the next day, Storm's End yielded. This is a SEPARATE incident from `shadow-assassination-of-renly` (which happened in Renly's tent before the parley ended).
- **Anchor quote:** "He had only an instant to look at it before it was gone, twisting between the bars of the portcullis and racing across the surface of the water, but that instant was long enough." — `acok-davos-02:353`

---

### `leeching-of-edric-storm`
- **type:** event.incident
- **Summary:** In the Chamber of the Painted Table at Dragonstone, Melisandre draws three leeches swollen with Edric Storm's king's blood, throws them one by one into a brazier's hot coals, and names "the usurper Joffrey, the usurper Balon, the usurper Robb." Stannis stands present and commands the demonstration. Davos witnesses. This is the king's-blood ritual; the three named kings subsequently die — but the causal link is THEORY-GATED and must not be proposed as an edge. Edric Storm is the VICTIM; Melisandre the AGENT; Stannis the commander.
- **Anchor quote:** "I saw you burn some leeches." / "And two false kings are dead." — `asos-davos-05:89–92` (quote line 89 for Davos's words; the leeching itself is described at lines 14–16)
- **Alternate anchor (the act itself):** "He could smell the burning blood again, and hear the leech hissing and spitting on the brazier's hot coals." — `asos-davos-05:15`

---

### `alester-florent-peace-treason`
- **type:** event.incident
- **Summary:** Alester Florent, serving as Stannis's Hand, secretly composes a peace letter to Lord Tywin Lannister (conveyed via Salladhor Saan's contact in King's Landing) proposing that Stannis surrender his claim, retract the bastardy accusation against Joffrey, and accept lordship of Dragonstone and Storm's End — sealing the deal by wedding Shireen to Tommen. Stannis had not authorized this. Axell Florent discovers the letter; Alester is imprisoned and later burned. Distinct from the generic `alester BETRAYS stannis` edge — this is the event node for the act itself.
- **Anchor quote:** "I penned a letter. Salladhor Saan swore that he had a man who could get it to King's Landing, to Lord Tywin." — `asos-davos-03:143`

---

### `stannis-discovery-of-royal-bastardy`
- **type:** event.incident
- **Summary:** Before Robert's death, Stannis (with or alongside Jon Arryn) uncovered the fact that Joffrey, Tommen, and Myrcella are the children of Jaime and Cersei, not Robert. This drove Stannis to flee King's Landing to Dragonstone and forms the root justification for his Iron Throne claim. Evidenced in Stannis's letter read aloud (acok-davos-01) and in Catelyn's reflection. The event is referenced but never shown in POV; it is inferred from the declaration letter and from Catelyn's line "Ned must have known, and Lord Arryn before him."
- **Anchor quote (Stannis's declaration letter):** "my beloved brother Robert, our late king, left no trueborn issue of his body, the boy Joffrey, the boy Tommen, and the girl Myrcella being abominations born of incest between Cersei Lannister and her brother Jaime the Kingslayer" — `acok-davos-01:179`

---

### `renly-s-death-vision-stannis`
- **NOTE:** baseline.md already names `renly-s-death-reflection` as an existing node (stannis AGENT_IN it). Do NOT re-propose this node — it exists. Instead propose edges against it below.

---

## Proposed NEW edges

> Key: **[BORDERLINE]** = gate should scrutinize; all others are high-confidence. Tier-2 = strong inference/unproven-but-load-bearing; Tier-1 = verbatim book quote proves it.

---

### Cortnay Penrose / shadow-killing-of-cortnay-penrose (the second shadow)

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 1 | melisandre | AGENT_IN | shadow-killing-of-cortnay-penrose | Tier-1 | "Melisandre had thrown back her cowl and shrugged out of the smothering robe. Beneath, she was naked, and huge with child." `acok-davos-02:351` | She physically births the shadow in the sea cave. |
| 2 | stannis-baratheon | COMMANDS_IN | shadow-killing-of-cortnay-penrose | Tier-1 | "Ser Cortnay will be dead within the day. Melisandre has seen it in the flames of the future." `acok-davos-02:239` | Stannis foreknows and authorizes; he told Davos "What do you think I made you a knight for" [paraphrase], and commands Davos to row her in. |
| 3 | davos-seaworth | PARTICIPATES_IN | shadow-killing-of-cortnay-penrose | Tier-1 | "Only land a boat beneath the castle, unseen, in the black of night. Can you do that?" `acok-davos-02:258` + "And so it was that he found himself once more crossing Shipbreaker Bay in the dark of night, steering a tiny boat with a black sail." `acok-davos-02:277` | Davos rows Mel to the sea cave; he is the enabler/participant, not a combatant. |
| 4 | cortnay-penrose | VICTIM_IN | shadow-killing-of-cortnay-penrose | Tier-1 | "Ser Cortnay will be dead within the day." `acok-davos-02:239`; Mel and Davos explicitly go to effect his death. Cortnay refuses to yield (`acok-davos-02:46–47`). | Confirmed by context; Penrose's death is the stated purpose of the mission. |
| 5 | davos-seaworth | WITNESS_IN | shadow-killing-of-cortnay-penrose | Tier-1 | "He knew that shadow. As he knew the man who'd cast it." `acok-davos-02:355` | Davos sees the shadow birth in full; textbook WITNESS_IN qualification. |
| 6 | shadow-killing-of-cortnay-penrose | LOCATED_AT | storms-end | Tier-1 | "he found himself once more crossing Shipbreaker Bay in the dark of night…The seaward side of Storm's End perched upon a pale white cliff" `acok-davos-02:277–337` | Sea cave is beneath Storm's End's cliffs. |
| 7 | siege-of-storms-end-299 | ENABLES | shadow-killing-of-cortnay-penrose | Tier-1 | "I will have quiet. Storm's End stands alone, and I am out of patience." `acok-davos-02:37`; the siege is the immediate military context that makes the shadow mission necessary. | ENABLES, not CAUSES — the mission is a free choice Stannis makes within the siege. |
| 8 | shadow-killing-of-cortnay-penrose | CAUSES | storms-end-yields | **[BORDERLINE]** Tier-2 | No direct quote of the surrender in these chapters; Cortnay's death implies yielding given the stated context ("Lord Meadows is not as stonehead stubborn as I was" `acok-davos-02:231`). | If `storms-end-yields` is already an edge or node, dedup. If not, this is the natural causal link. Gate should verify whether the surrender node exists. |
| 9 | stannis-baratheon | SUSPECTED_OF | shadow-killing-of-cortnay-penrose | **[BORDERLINE — NOTE]** | The killing is NOT a SUSPECTED_OF for Stannis — it is Tier-1 COMMANDS_IN (he gives the direct order). SUSPECTED_OF would be incorrect here. Dropping this; see Dropped section. | |

---

### Catelyn + Brienne witness Renly's death (acok-catelyn-04)

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 10 | catelyn-stark | WITNESS_IN | shadow-assassination-of-renly | Tier-1 | "it was only the king's shadow shifting against the silken walls…she saw Renly's sword still in its scabbard, sheathed still, but the shadowsword…" `acok-catelyn-04:93` | Catelyn explicitly sees the shadow sword strike Renly. Classic WITNESS_IN. |
| 11 | brienne-of-tarth | WITNESS_IN | shadow-assassination-of-renly | Tier-1 | "Your Gr—no!" cried Brienne the Blue when she saw that evil flow" `acok-catelyn-04:97`; she holds the dying king. | Brienne is directly present and perceives the killing. |
| 12 | catelyn-stark | REVEALS_TO | brienne-of-tarth | Tier-1 | "I saw a shadow. I thought it was Renly's shadow at the first, but it was his brother's." `acok-catelyn-04:129` | Catelyn explains what she saw to Brienne; REVEALS_TO (person→person, the truth about the shadow). |
| 13 | brienne-of-tarth | VOWS_TO | stannis-baratheon | Tier-1 | "I will kill him," the tall homely girl declared. "With my lord's own sword, I will kill him. I swear it. I swear it. I swear it." `acok-catelyn-04:135` | Brienne's explicit vow of vengeance on Stannis, confirmed triple oath in text. |

---

### The renly-s-death-reflection / MOTIVATES substrate

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 14 | renly-s-death-reflection | MOTIVATES | stannis-baratheon | Tier-1 | "I dream of it sometimes. Of Renly's dying. A green tent, candles, a woman screaming. And blood." `acok-davos-02:189` | Stannis confesses the kinslaying haunts his dreams; the nightmare guilt drives him (MOTIVATES → character, not event). The reflection event is causally ISLANDED (baseline says cIn=0 on this node); this is the missing inbound wire. |
| 15 | shadow-assassination-of-renly | MOTIVATES | stannis-baratheon | Tier-2 | "I did love him, Davos…I will go to my grave thinking of my brother's peach." `acok-davos-02:193` | The broader guilt of the kinslaying motivates Stannis's haunted quality; complements edge 14. **[BORDERLINE]** — the `renly-s-death-reflection` sub-event may be the better handle; use whichever is cleaner at synthesis. |

---

### Twincest-revelation / Stannis's claim root

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 16 | stannis-discovery-of-royal-bastardy | MOTIVATES | stannis-baratheon | Tier-2 | "There's proof of a sort at Storm's End. Robert's bastard…If men were to see him, and then look again at Joffrey and Tommen, they could not help but wonder" `acok-davos-01:221` | The discovery of the incest is the root of his entire claim; MOTIVATES his declaring himself king. |
| 17 | murder-of-jon-arryn | ENABLES | stannis-discovery-of-royal-bastardy | Tier-2 | "Ned must have known, and Lord Arryn before him. Small wonder that the queen had killed them both." `acok-catelyn-04:35` | Jon Arryn's investigation (and subsequent murder) is linked in Catelyn's thought to the discovery that both she and Stannis made. ENABLES = the investigation was the precondition; Arryn's death is what forced Stannis to act. **[BORDERLINE]** — Catelyn's line is Catelyn's deduction, not Stannis's direct statement; Tier-2 is appropriate. |
| 18 | stannis-baratheon | INVESTIGATES | stannis-discovery-of-royal-bastardy | Tier-2 | "And you have no proof. Of this incest. No more than you did a year ago." `acok-davos-01:219` | Stannis had been investigating/knew before Robert's death; Davos's reply confirms Stannis had no new proof, implying prior investigation. |
| 19 | stannis-discovery-of-royal-bastardy | ENABLES | stannis-s-iron-throne-claim | Tier-2 | (Stannis's declaration letter, read aloud in `acok-davos-01:179`) — the bastardy finding IS his stated legal basis. If `stannis-s-iron-throne-claim` is already an edge/node, dedup. | The discovery is the legal predicate for the claim; without it there is no claim. |
| 20 | stannis-baratheon | DISTRUSTS | cersei-lannister | **DEDUP — EXISTS** | baseline already lists "stannis DISTRUSTS cersei" | Do not re-propose. |
| 21 | stannis-baratheon | SUSPECTED_OF | murder-of-robert-baratheon | **[BORDERLINE]** Tier-2 | "I have no doubt that Cersei had a hand in Robert's death." `acok-davos-02:185` — Stannis believes Cersei; he does not believe he himself is suspected. | Actually this is the WRONG direction — Stannis suspects CERSEI. See below for `cersei SUSPECTED_OF murder-of-robert`. |
| 22 | cersei-lannister | SUSPECTED_OF | murder-of-robert-baratheon | Tier-2 | "I have no doubt that Cersei had a hand in Robert's death. I will have justice for him. Aye, and for Ned Stark and Jon Arryn as well." `acok-davos-02:185` | Stannis explicitly states in-world suspicion that Cersei caused Robert's death. SUSPECTED_OF (Tier-2, unproven in the text of these chapters). |

---

### Leeching of Edric Storm

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 23 | melisandre | AGENT_IN | leeching-of-edric-storm | Tier-1 | "He could smell the burning blood again, and hear the leech hissing and spitting on the brazier's hot coals." `asos-davos-05:15` | Melisandre performs the ritual; the burning is the act itself. Confirmed in `asos-davos-05:87–92`. |
| 24 | edric-storm | VICTIM_IN | leeching-of-edric-storm | Tier-1 | "You have seen what even a little of that blood could do—" / "I saw you burn some leeches." `asos-davos-05:87–89` | The leeches are explicitly fat with Edric's king's blood; Davos confirms he witnessed it. |
| 25 | stannis-baratheon | COMMANDS_IN | leeching-of-edric-storm | Tier-2 | "Two is not three. Kings can count as well as smugglers." `asos-davos-05:115` — Stannis stands present and engaged; he has not stopped Mel. The meeting in the Painted Table chamber is commanded by him. **[BORDERLINE]** — text does not show a direct order; PARTICIPATES_IN may be safer. | |
| 25b | stannis-baratheon | PARTICIPATES_IN | leeching-of-edric-storm | Tier-2 | Same as above; he is in the chamber, responds to the act, does not forbid it. Alternative to COMMANDS_IN if gate prefers. | |
| 26 | davos-seaworth | WITNESS_IN | leeching-of-edric-storm | Tier-1 | "I saw you burn some leeches." `asos-davos-05:89` | Davos directly confirms he witnessed the leech burning. |
| 27 | melisandre | SACRIFICES | edric-storm | **DEDUP — EXISTS** | baseline: "melisandre SACRIFICES edric-storm" already exists. | Do not re-propose. |

---

### Alester Florent's peace treason / revelation beat

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 28 | alester-florent | AGENT_IN | alester-florent-peace-treason | Tier-1 | "I penned a letter. Salladhor Saan swore that he had a man who could get it to King's Landing, to Lord Tywin." `asos-davos-03:143` | Alester is the direct author and executor of the treasonous letter. |
| 29 | alester-florent | BETRAYS | stannis-baratheon | **DEDUP — EXISTS** | baseline: "alester BETRAYS stannis" exists. | Do not re-propose the dyadic edge. The event node is new. |
| 30 | davos-seaworth | REVEALS_TO | stannis-baratheon | Tier-2 | (Implicitly — Davos learns of the treason in `asos-davos-03` and is the Hand; the mechanics of how Stannis is eventually told are off-screen in these chapters.) **[BORDERLINE]** — text shows Davos learning of it from Alester directly, but the REVEALS_TO-king chain is off-screen here. Dropping this unless a direct-quote path exists in asos-davos-04/06. | |
| 31 | axell-florent | IMPRISONS | alester-florent | Tier-1 | Ser Axell gives a curt nod. "Let the traitors enjoy each other's company." `asos-davos-03:99` + guards fling Alester into Davos's cell. | Axell directly orders the imprisonment; text is unambiguous. |
| 32 | alester-florent-peace-treason | REVEALS_TO | davos-seaworth | Tier-1 | "I penned a letter…to Lord Tywin. His lordship is a…a man of reason, and my terms…the terms were fair…" `asos-davos-03:143–151` | Alester confesses directly to Davos in the cell. |
| 33 | salladhor-saan | CONSPIRES_WITH | alester-florent | Tier-2 | "Salladhor Saan swore that he had a man who could get it to King's Landing" `asos-davos-03:143` | Salladhor facilitates the delivery of the treason letter; knowing complicity. **[BORDERLINE]** — Salladhor's motive is opportunistic self-interest, not ideological; but the text shows knowing cooperation in the act. Tier-2. |

---

### Davos's rescue of Edric Storm

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 34 | davos-seaworth | RESCUES | edric-storm | Tier-2 | "He will not do it," said Davos. "He could not harm his own blood." `asos-davos-05:177` + Davos's building coalition of "king's men" (`asos-davos-05:171–172`) and his persistent advocacy throughout the chapter. **[BORDERLINE]** — the ACTUAL act of smuggling Edric off Dragonstone happens in asos-davos-06, not in the assigned chapters. Proposal is logically correct but the anchor quote for the completed rescue is outside assigned chapters. Flagging as **[BORDERLINE]** — synthesizer should confirm via asos-davos-06. | If text in asos-davos-05 shows the departure, quote it; if not, the edge belongs to the asos-davos-06 chapter. |

---

### Salladhor Saan's abandonment / betrayal

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 35 | salladhor-saan | BETRAYS | stannis-baratheon | **DEDUP — EXISTS** | baseline: "salladhor BETRAYS stannis" listed. | Do not re-propose. Check if the specific episode (abandoning Dragonstone to return to sea, `asos-davos-05:183`) is a new facet or already captured. Since baseline entry is non-specific, this may already cover it. |

---

### Melisandre / Stannis / R'hllor conversion — supplementary edges

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 36 | melisandre | ADVISES | stannis-baratheon | Tier-1 | "Give me the boy for R'hllor, and the ancient prophecy shall be fulfilled." `asos-davos-05:61` | Mel directly advises Stannis to sacrifice Edric. ADVISES fills the gap named in baseline ("no ADVISES in the web"). |
| 37 | stannis-baratheon | WORSHIPS | rhllor | Tier-1 | Melisandre: "R'hllor, come to us in our darkness…" and Stannis watches impassively then draws the sword `acok-davos-01:21–51`; "he said, 'I know little and care less of gods, but the red priestess has power'" `acok-davos-01:257` + "the fiery heart of R'hllor" on his banners (`acok-davos-03:81`). **[BORDERLINE]** — Stannis is publicly converted (burns the Seven, uses R'hllor language in his seal, carries the fiery heart on banners) but privately skeptical. Tier-2 may be more honest: `stannis WORSHIPS rhllor | Tier-2 | public conversion, private doubt`. |
| 38 | melisandre | MANIPULATES | stannis-baratheon | Tier-2 | "She has broken him, as a man breaks a horse. She would ride him to power if she could" `asos-davos-02:15` | Davos's perception that Mel manipulates Stannis. MANIPULATES is in the vocab. **[BORDERLINE]** — this is Davos's POV interpretation, not a proven fact; Tier-2/SUSPECTED_OF territory. Proposing as Tier-2. |
| 39 | davos-seaworth | DISTRUSTS | melisandre | Tier-1 | "It was her! Mother, don't forsake us. It was her who burned you, the red woman, Melisandre, her!" `asos-davos-01:59` | Davos's active distrust of Mel, textbook DISTRUSTS. |
| 40 | burning-of-the-seven-at-dragonstone | MOTIVATES | davos-seaworth | Tier-1 | "He felt ill as he watched them burn…The gods had never meant much to Davos the smuggler…Yet he felt ill" `acok-davos-01:25`; "Even when she killed old Maester Cressen, even then, you did nothing." `asos-davos-01:61` | The burning of the Seven is explicitly what troubles Davos's conscience and motivates his eventual resolve to kill Mel. |

---

### Renly's claim / Stannis-Renly parley / whodunit accusations

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 41 | catelyn-stark | SUSPECTED_OF | shadow-assassination-of-renly | Tier-2 | "I believe it was Lady Stark who slew the king. She had journeyed all the way from Riverrun…" `acok-davos-02:69` | Lord Alester Florent publicly suspects Catelyn of Renly's murder — in-world accusation. SUSPECTED_OF (unproven, she didn't do it). |
| 42 | brienne-of-tarth | SUSPECTED_OF | shadow-assassination-of-renly | Tier-2 | "It was Brienne. Ser Emmon Cuy swore as much before he died." `acok-davos-02:71` | Lord Caron's in-world accusation; baseline notes Brienne is blamed but she is innocent. |
| 43 | catelyn-stark | REVEALS_TO | ser-robar-royce | Tier-1 | "I swear it, you know me, it was Stannis killed him. I swear it, I swear it, I saw." `acok-catelyn-04:117` | Catelyn explicitly names Stannis to Robar Royce as the killer through sorcery. |

---

### Night's Watch letter — discovery beat

| # | Source | Edge | Target | Tier | Quote + cite | Rationale |
|---|--------|------|--------|------|--------------|-----------|
| 44 | davos-seaworth | INVESTIGATES | nights-watch-plea-to-five-kings | Tier-1 | "Davos suddenly realized just what he was reading…'King Stannis never saw this letter, you are quite certain?'" `asos-davos-05:269–283` | Davos discovers and acts on the Night's Watch letter; the discovery MOTIVATES Stannis's eventual decision to march north. This is the revelation beat for the WHY-STANNIS-MARCHES-NORTH motive. |
| 45 | nights-watch-plea-to-five-kings | MOTIVATES | stannis-baratheon | Tier-2 | "Soon comes the cold, and the night that never ends" + Davos thinking of Melisandre's warning; Davos's resolve to bring it to Stannis is explicit: "King Stannis never saw this letter" — implying he intends to. `asos-davos-05:287`. **[BORDERLINE]** — the actual delivery to Stannis is in asos-davos-06. The intention is clear here. | Anchor quote: "I was frightened, Maester. Davos was remembering a tale Salladhor Saan had told him, of how Azor Ahai tempered Lightbringer by thrusting it through the heart of the wife he loved. He slew his wife to fight the dark." `asos-davos-05:291` — the letter triggers Davos's resolve to save Edric AND bring the letter forward. |

---

## Dropped / considered-but-rejected

1. **`stannis SUSPECTED_OF shadow-killing-of-cortnay-penrose`** — WRONG edge type. The text shows Stannis COMMANDS_IN (direct order, `acok-davos-02:239`), not suspicion. SUSPECTED_OF is only for unproven agency; this is proven in the text. Dropped.

2. **`salladhor-saan BETRAYS stannis` (the letter episode)** — DEDUP: baseline already has `salladhor BETRAYS stannis`. The specific letter-courier role might be a new facet, but the generic edge covers it.

3. **`leeching FORESHADOWS/CAUSES death-of-joffrey / death-of-robb / death-of-balon`** — GATED. Explicitly prohibited in HARD RULES. The three named kings die, but asserting the leeching caused them asserts the magic mechanics. Node-prose only.

4. **`stannis WIELDS lightbringer`** — Assigned to Lens C per baseline GAP #8. Leaving to that lens; I found the key text ("That sword was not Lightbringer, my friend" `acok-davos-01:125`) in Salladhor's dialogue — dropped to harvest.

5. **`melisandre PRACTICES shadowbinding`** — Plausible concept edge but `shadowbinding` node may not exist; leaving for Lens A (R'hllor conversion). I've proposed AGENT_IN on both shadow events instead.

6. **`davos-seaworth REVEALS_TO stannis-baratheon` (Alester's treason)** — off-screen in assigned chapters; the delivery is implied but not quoted. Dropped pending asos-davos-04/06.

7. **`alester-florent CONSPIRES_WITH tywin-lannister`** — the letter was sent TO Tywin but no response is shown; Alester acted unilaterally. CONSPIRES_WITH implies mutual agreement; not warranted here. Dropped.

8. **`nights-watch-plea-to-five-kings CAUSES stannis-moves-to-the-wall`** — Causal ladder violation: the letter ENABLES the decision at most (a precondition); Davos's argument and Stannis's choice are what produces the move. Dropped in favor of MOTIVATES and ENABLES handled in the WHY-MARCHES-NORTH substrate.

9. **`ser-robar-royce WITNESS_IN shadow-assassination-of-renly`** — Robar did NOT see the shadow; he arrived after, was told by Catelyn. The WITNESS_IN requires the prose show the character "actually SEES it." Robar came in post-hoc with the other knights and saw the dead king, not the shadow. Dropped.

10. **Brienne's oath to kill Stannis as CONSPIRES_WITH Catelyn** — Brienne makes a personal vow, not a conspiracy with Catelyn. VOWS_TO is the correct edge (brienne VOWS_TO [avenge-renly] / kill stannis), not CONSPIRES_WITH.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | ACOK | acok-catelyn-04:27 | "Catelyn had not eaten today…food had lost its savor in a world without Ned" — grief-starvation; notable emotional register |
| food | ACOK | acok-davos-01:147 | Salladhor: "Minced lamb with pepper and roasted gull stuffed with mushrooms and fennel and onion" — Salladhor's dinner on the Valyrian; vivid food detail |
| food | ACOK | acok-davos-01:97 | Salladhor eating grapes "marvelously sweet"; seeds dribbled on lip and flicked away; Davos orders ale |
| food/hardship | ACOK | acok-catelyn-04:61 | "When Mace Tyrell laid siege to Storm's End, Stannis ate rats rather than open his gates" — the rat-eating backstory verbatim |
| food/hardship | ACOK | acok-davos-02:196 | "The stink of horse dung was heavy in the air, mingled with the woodsmoke and the smell of cooking meat" — camp food at Storm's End |
| food/hardship | ASOS | asos-davos-01:19–20 | Davos surviving on tiny crabs from the strand, smashing them on rocks to suck meat from claws and guts from shells |
| food | ASOS | asos-davos-02:17 | Captain Khorane's snails and lampreys that made Davos ill; "his stomach could not tolerate the snails and lampreys" |
| food | ASOS | asos-davos-02:49 | Salladhor: "white cheese and a bowl of those cracked green olives" + hot red wine with cloves + lime |
| food | ASOS | asos-davos-03:21 | Prison gaoler "Lamprey" brings half a lamprey pie — "so rich he could not keep it down, but even so, it was a rare treat for a prisoner" |
| food | ASOS | asos-davos-03:19 | Prison porridge, sometimes sweetened with honey or poured milk — gaoler "Porridge" |
| physical_desc | ACOK | acok-davos-01:21 | Stannis: "his jaw hard as stone under the blue-black shadow of his tight-cropped beard…dressed more richly than was his wont" |
| physical_desc | ACOK | acok-davos-02:107 | Stannis up close: "His face had grown haggard, and he had dark circles under his eyes" — post-Renly haunted look |
| physical_desc | ACOK | acok-davos-02:351 | Melisandre's shadow-birth: "naked, and huge with child. Swollen breasts hung heavy against her chest, and her belly bulged as if near to bursting…her skin seemed to glow with a light of its own" — key description for Mel node |
| physical_desc | ASOS | asos-davos-05:161 | Dragonstone castle described at length: gargoyles, grotesques, wyverns, the Great Hall dragon lying on belly with men entering through open mouth, kitchens as curled dragon, Sea Dragon Tower, the Windwyrm — major descriptive passage |
| hospitality | ASOS | asos-davos-02:17 | Captain Khorane gives Davos his cabin, clothes, new boots; insists on sharing provisions — true sailor hospitality; guest-relationship |
| hospitality | ASOS | asos-davos-02:49 | Salladhor embraces Davos, kisses three times, orders hot wine, cheese, olives — pirate hospitality |
| hospitality | ACOK | acok-davos-01:89 | "Salladhor Saan sat eating grapes from a wooden bowl. When he spied Davos, he beckoned him closer. 'Ser knight, come sit with me. Eat a grape. Eat two.'" |
| quote_load_bearing | ACOK | acok-davos-02:193 | Stannis: "I did love him, Davos. I know that now. I swear, I will go to my grave thinking of my brother's peach." — key character quote for Stannis node ## Quotes |
| quote_load_bearing | ACOK | acok-davos-01:257 | Stannis: "I know little and care less of gods, but the red priestess has power." — core statement on Stannis's pragmatic conversion |
| quote_load_bearing | ACOK | acok-davos-01:253 | Stannis: "I stopped believing in gods the day I saw the Windproud break up across the bay. Any gods so monstrous as to drown my mother and father would never have my worship, I vowed." — key backstory quote |
| quote_load_bearing | ACOK | acok-davos-02:165 | Stannis: "A good act does not wash out the bad, nor a bad act the good. Each should have its own reward. You were a hero and a smuggler." — character-defining justice quote |
| quote_load_bearing | ACOK | acok-catelyn-04:95 | "'Cold,' said Renly in a small puzzled voice, a heartbeat before the steel of his gorget parted like cheesecloth beneath the shadow of a blade that was not there." — the Renly death moment verbatim |
| foreshadowing | ASOS | asos-davos-05:291 | Davos: "He was remembering a tale Salladhor Saan had told him, of how Azor Ahai tempered Lightbringer by thrusting it through the heart of the wife he loved. He slew his wife to fight the dark. If Stannis is Azor Ahai come again, does that mean Edric Storm must play the part of Nissa Nissa?" — foreshadows Shireen's fate (theory-gated reading; point only) |
| foreshadowing | ASOS | asos-davos-02:199–201 | Patchface sings: "Fool's blood, king's blood, blood on the maiden's thigh, but chains for the guests and chains for the bridegroom, aye aye aye" — Patchface prophecy; possible Red Wedding foreshadowing |
| artifact | ACOK | acok-davos-01:125 | Salladhor: "That sword was not Lightbringer, my friend" — key quote for Lightbringer node; the false-Lightbringer assessment |
| artifact | ACOK | acok-davos-01:41–51 | Stannis draws the sword from the fire: "jade-green flames swirling around cherry-red steel" then "point of the sword into the damp earth and beat out the flames against his leg" — vivid Lightbringer description |
| magic | ACOK | acok-davos-02:331 | Mel: "Dark walls that no shadow can pass—ancient, forgotten, yet still in place." — Storm's End's spell-wards; critical for understanding WHY a second shadow had to be born at sea |
| magic | ACOK | acok-davos-02:334 | Mel: "Shadows are the servants of light, the children of fire. The brightest flame casts the darkest shadows." — key shadow-magic doctrine for node prose |
| magic | ASOS | asos-davos-03:53 | Mel in the cell: "the king's fires burn so low I dare not draw off any more to make another son. It might well kill him." — reveals shadow-birth depletes Stannis's life-fire; important mechanics for node prose (NOT theory edges, prose only) |
