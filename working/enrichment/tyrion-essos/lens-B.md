# Lens B — whodunit / hidden-agency + SUSPECTED_OF — A2.4 Tyrion / Essos proposal (S161)

Chapters read: adwd-tyrion-01, adwd-tyrion-02, adwd-tyrion-03, adwd-tyrion-06, adwd-tyrion-07, adwd-tyrion-08.

---

## Proposed NEW nodes

### 1. `illyrio-delivers-tyrion-to-aegon-mission`
- **Slug:** `illyrio-delivers-tyrion-to-aegon-mission`
- **Name:** Illyrio Delivers Tyrion to the Aegon Mission
- **Type:** event.incident
- **Body:** Illyrio Mopatis smuggles Tyrion out of Pentos in a litter, escorts him partway along the Valyrian road, hands him off to Haldon and Duck at Ghoyan Drohe, and transfers six chests of supplies/court clothing—setting Tyrion in motion as an asset for the Aegon/Daenerys plan. The handoff is Illyrio's final direct act in the Pentos episode.
- **Anchor quote:** "I will rejoin you in Westeros. That I swear, by my sweet Serra's hands." — adwd-tyrion-03:103

### 2. `jorah-captures-tyrion`
- **Slug:** `jorah-captures-tyrion`
- **Name:** Jorah Mormont Captures Tyrion at Selhorys
- **Type:** event.incident
- **Body:** Jorah Mormont, hiding in the shadows of a Selhorys brothel, confronts the drunk Tyrion and seizes him to bring to Daenerys as a "gift" to win back her favour. Tyrion, too drunk to resist, submits without a fight. Jorah then chains him in iron manacles and marches him to Volantis.
- **Anchor quote:** "'Deliver you,' the knight said, 'to the queen.'" — adwd-tyrion-06:347

### 3. `oppo-killed-by-sailors-in-volantis`
- **Slug:** `oppo-killed-by-sailors-in-volantis`
- **Name:** Oppo Killed by Sailors in Volantis
- **Type:** event.incident
- **Body:** A group of five drunken sailors from the Seven Kingdoms pursued Oppo (Groat) and Penny after seeing their dwarf-jousting show in a Volantis square. Mistaking Oppo for Tyrion Lannister, they beheaded him. Penny was spared because they realized she was a girl. The killing is directly attributable to Cersei's bounty on Tyrion's head creating lethal confusion. Triggers Penny's grief-driven attack on Tyrion.
- **Anchor quote:** "'There were five of them, drunk. They saw us jousting in the square and followed us. When they realized I was a girl they let me go, but they took my brother and killed him. They cut his head off.'" — adwd-tyrion-07:387

### 4. `penny-attacks-tyrion-at-merchants-house`
- **Slug:** `penny-attacks-tyrion-at-merchants-house`
- **Name:** Penny's Attack on Tyrion at the Merchant's House
- **Type:** event.incident
- **Body:** Penny, in man's clothes and wielding a knife, rushes Tyrion in the common room of the Merchant's House in Volantis. She blames Tyrion for her brother Oppo's death (sailors killed Oppo mistaking him for Tyrion). Tyrion deflects with a thrown flagon; Ser Jorah physically stops Penny and disarms her. The attack ends with Penny weeping and the widow of the waterfront intervening.
- **Anchor quote:** "'She's a girl, he realized all at once, a girl dressed up in man's clothes. And she means to gut me with that knife.'" — adwd-tyrion-07:371

### 5. `widow-of-the-waterfront-brokers-passage-to-meereen`
- **Slug:** `widow-of-the-waterfront-brokers-passage-to-meereen`
- **Name:** Widow of the Waterfront Brokers Passage to Meereen
- **Type:** event.incident
- **Body:** After Jorah Mormont is rebuffed and nearly threatened by the widow of the waterfront, Tyrion's honest declaration of his motives (and the Penny spectacle) shifts the widow's mind. She arranges passage on the cog Selaesori Qhoran, bound for Qarth but fated (per Benerro's fire-reading) never to reach it—i.e. destined to reach Meereen's theatre of war. She asks only that Tyrion carry her message to Daenerys: "Tell her we are waiting. Tell her to come soon."
- **Anchor quote:** "'Two days from now, the cog Selaesori Qhoran will set sail for Qarth by way of New Ghis … Be on her when she sails.'" — adwd-tyrion-07:413

### 6. `tyrion-deduces-griff-is-jon-connington`
- **Slug:** `tyrion-deduces-griff-is-jon-connington`
- **Name:** Tyrion Deduces Griff is Jon Connington
- **Type:** event.incident
- **Body:** Tyrion reasons out Griff's true identity—exiled lord, disguised colouring (dyed blue hair over red), refusal to name himself a knight or lord—and raises it covertly in conversation, dropping "Lord Connington was the prince's dearest friend, was he not?" Griff does not deny it. Tyrion also deduces that Young Griff is Aegon Targaryen, son of Rhaegar.
- **Anchor quote:** "'Not as your false father did. Lord Connington was the prince's dearest friend, was he not?'" — adwd-tyrion-06:107

---

## Proposed NEW edges

### Causal / event-role edges for NEW event nodes

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| illyrio-mopatis | AGENT_IN | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "I will rejoin you in Westeros. That I swear, by my sweet Serra's hands." adwd-tyrion-03:103 | Illyrio organises the handoff, loads the supply chests, sends Tyrion forward |
| tyrion-lannister | VICTIM_IN | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "Yollo, he is called." adwd-tyrion-03:68 | Tyrion is the object delivered, given a false name by Illyrio |
| haldon | AGENT_IN | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "He was as tall as Griff now. Three days ago he knocked Duck into a horse trough." adwd-tyrion-03:47 | Haldon and Duck receive the handoff at Illyrio's instruction |
| rolly-duckfield | AGENT_IN | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "He rides," Tyrion broke in, before the lord of cheese could answer for him adwd-tyrion-03:61 | Duck physically carries Tyrion to the Shy Maid |
| varys-smuggles-tyrion-out-of-kings-landing | ENABLES | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "My house is yours. Any friend of my friend across the water is a friend to Illyrio Mopatis, yes." adwd-tyrion-01:65 | Varys's smuggling delivers Tyrion to Illyrio; the Pentos sojourn is the next step |
| illyrio-delivers-tyrion-to-aegon-mission | ENABLES | stone-men-attack-the-shy-maid | Tier-2 | — | "The Sorrows. I was lost in the Sorrows." adwd-tyrion-06:15 | Tyrion being placed on the Shy Maid is what puts him in the Sorrows |
| jorah-mormont | AGENT_IN | jorah-captures-tyrion | Tier-1 | — | "'Deliver you,' the knight said, 'to the queen.'" adwd-tyrion-06:347 | Jorah performs the seizure |
| tyrion-lannister | VICTIM_IN | jorah-captures-tyrion | Tier-1 | — | "Tyrion could no more outrun him than outfight him." adwd-tyrion-06:345 | Tyrion is the captive |
| jorah-captures-tyrion | LOCATED_AT | selhorys | Tier-1 | — | "He dreamt of his lord father and the Shrouded Lord. … 'Our dead dwarf has returned to us,' Haldon said." adwd-tyrion-06:13 (arrival in Selhorys context) / "The dwarf could no more outrun him than outfight him." adwd-tyrion-06:345 | The brothel in Selhorys is where capture occurs |
| jorah-captures-tyrion | TRIGGERS | penny-attacks-tyrion-at-merchants-house | Tier-1 | — | "'It was him they wanted. They thought Oppo was him.'" adwd-tyrion-07:397 | The sailors-killing-Oppo is itself triggered by Jorah bringing Tyrion to Volantis; Penny finds them at the Merchant's House because of that chain |
| penny | AGENT_IN | penny-attacks-tyrion-at-merchants-house | Tier-1 | — | "She's a girl, he realized all at once, a girl dressed up in man's clothes. And she means to gut me with that knife." adwd-tyrion-07:371 | Penny initiates the attack |
| tyrion-lannister | VICTIM_IN | penny-attacks-tyrion-at-merchants-house | Tier-1 | — | "Tyrion rolled on one side as she buried the knife blade in the floorboards" adwd-tyrion-07:373 | Tyrion is the target |
| jorah-mormont | AGENT_IN | penny-attacks-tyrion-at-merchants-house | Tier-1 | — | "Mormont had her by the collar with one hand. With the other he wrenched the dagger from her grasp." adwd-tyrion-07:377 | Jorah stops the attack |
| oppo-killed-by-sailors-in-volantis | TRIGGERS | penny-attacks-tyrion-at-merchants-house | Tier-1 | — | "'They killed him.' … 'It was him they wanted. They thought Oppo was him.'" adwd-tyrion-07:383,397 | Oppo's killing is the direct cause of Penny's attack on Tyrion |
| oppo-killed-by-sailors-in-volantis | LOCATED_AT | volantis | Tier-1 | — | "She was younger than the others, slim and pretty, with long silvery hair. Lyseni, at a guess … but the man whose lap she filled was from the Seven Kingdoms." adwd-tyrion-07:339 (Volantis context throughout ch 07) | Volantis is where the sailors killed Oppo |
| oppo | VICTIM_IN | oppo-killed-by-sailors-in-volantis | Tier-1 | — | "'They took my brother and killed him. They cut his head off.'" adwd-tyrion-07:387 | Oppo is killed |
| penny | WITNESS_IN | oppo-killed-by-sailors-in-volantis | Tier-1 | — | "'They saw us jousting in the square and followed us. When they realized I was a girl they let me go'" adwd-tyrion-07:387 | Penny sees/survives the event |
| penny-attacks-tyrion-at-merchants-house | TRIGGERS | widow-of-the-waterfront-brokers-passage-to-meereen | Tier-2 | — | "Volantis is no safe place for dwarfs, it seems … I think I had best help you after all." adwd-tyrion-07:405 | The dwarf fight in the widow's common room shifts her mind; she decides to help |
| widow-of-the-waterfront | AGENT_IN | widow-of-the-waterfront-brokers-passage-to-meereen | Tier-1 | — | "'Two days from now, the cog Selaesori Qhoran will set sail … Be on her when she sails.'" adwd-tyrion-07:413 | The widow arranges the passage |
| jorah-mormont | PARTICIPATES_IN | widow-of-the-waterfront-brokers-passage-to-meereen | Tier-1 | — | "'We need swift passage to Meereen.'" adwd-tyrion-07:297 | Jorah makes the request |
| widow-of-the-waterfront-brokers-passage-to-meereen | ENABLES | selaesori-qhoran-voyage | Tier-2 | — | "Be on her when she sails." adwd-tyrion-07:413 | The widow's brokerage is what gets them on the Selaesori Qhoran |

### MOTIVATES edges (hidden agency / motive layer)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| desire-to-win-back-daenerys-favour | MOTIVATES | jorah-mormont | Tier-1 | — | "'To serve her. Defend her. Die for her, if need be.'" adwd-tyrion-07:357 | Jorah's stated and consistent motive for seizing Tyrion and going to Meereen |
| grief-over-oppo | MOTIVATES | penny | Tier-1 | — | "'They killed him.' All the fight went out of her at that." adwd-tyrion-07:383 | Grief over Oppo's death drives Penny's attack on Tyrion and her desolate arc aboard ship |

Note: `desire-to-win-back-daenerys-favour` is not a graph node; use `jorah-mormont MOTIVATES jorah-mormont` is wrong structure. Correct idiom per architecture is to propose a MOTIVATES edge sourced from an *event or state* node that drives the character. Propose as:

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| daenerys-banishes-jorah | MOTIVATES | jorah-mormont | Tier-1 | — | "'To serve her. Defend her. Die for her, if need be.'" adwd-tyrion-07:357 | Daenerys's banishment of Jorah is why he needs to bring her a gift; his motive for the capture |
| oppo-killed-by-sailors-in-volantis | MOTIVATES | penny | Tier-1 | — | "'They killed him.' All the fight went out of her at that. She hung limply in Mormont's grasp as her eyes filled with tears." adwd-tyrion-07:383 | Oppo's murder is what motivates Penny's attack on Tyrion and her later grief arc |

### DECEIVES / DISGUISED_AS edges (Tyrion's false identities)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| tyrion-lannister | DISGUISED_AS | hugor-hill | Tier-1 | — | "'in Pentos I am Yollo,' he said quickly, 'but my mother named me Hugor Hill.'" adwd-tyrion-03:69 | Tyrion adopts Hugor Hill as his travelling alias; used throughout the river voyage and Selhorys |
| illyrio-mopatis | DECEIVES | haldon | Tier-2 | via_false_information | "Illyrio spoke up quickly. 'Yollo, he is called.'" adwd-tyrion-03:67 | Illyrio provides the false name "Yollo" to Haldon and Duck before Tyrion corrects it to Hugor Hill |
| tyrion-lannister | DECEIVES | jorah-mormont | Tier-2 | via_false_information | "'I am as much his creature as you are. We ought not be at odds.'" adwd-tyrion-07:161 | Tyrion tries (unsuccessfully) to manipulate Jorah by claiming shared allegiance to Varys |

### MANIPULATES edges (Tyrion's social engineering)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| tyrion-lannister | MANIPULATES | aegon-targaryen-young-griff | Tier-1 | via_flattery | "'I lied. Trust no one. And keep your dragon close.'" adwd-tyrion-06:155 | Tyrion uses flattery then a deliberate lie during cyvasse to provoke Aegon and plant the "go west" strategy — a classic via_false_information / via_flattery manipulation |
| tyrion-lannister | MANIPULATES | aegon-targaryen-young-griff | Tier-1 | via_false_information | "'I told you, I know our little queen … she will fly to your side as fast as wind and water can carry her.'" adwd-tyrion-06:147 | Tyrion uses false certainty about Daenerys's character to steer Aegon toward the Dorne-first strategy; he cannot actually know this |

NOTE: `tyrion MANIPULATES aegon` already exists per baseline (dedup). These entries add the QUALIFIER specificity missing from the base dyad — the synthesis can decide whether to enrich the existing edge with qualifiers or treat as new distinct edges.

### CONSPIRES_WITH / INFORMS edges (Illyrio/Varys whodunit layer)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| illyrio-mopatis | INFORMS | tyrion-lannister | Tier-1 | — | "'Not Stannis. Nor Myrcella.' The yellow smile widened. 'Another. Stronger than Tommen, gentler than Stannis, with a better claim than the girl Myrcella.'" adwd-tyrion-01:267 | Illyrio reveals the existence of a third claimant ("a dragon with three heads") to Tyrion as a recruitment pitch |
| varys | CONSPIRES_WITH | illyrio-mopatis | Tier-1 | — | "'We were young together, two green boys in Pentos … Secrets are worth more than silver or sapphires, Varys claimed.'" adwd-tyrion-02:79,87 | Illyrio's own testimony of the Varys partnership, narrated to Tyrion |

NOTE: `varys CONSPIRES_WITH illyrio` and `illyrio CONSPIRES_WITH varys` already exist per baseline (dedup). The INFORMS edge (illyrio→tyrion) about the third claimant is NEW.

### SEEKS / TRAVELS_TO / REVEALED_TO edges

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| jorah-mormont | SEEKS | daenerys-targaryen | Tier-1 | — | "'To serve her. Defend her. Die for her, if need be.'" adwd-tyrion-07:357 | Jorah's declared objective when meeting the widow of the waterfront |
| jorah-mormont | TRAVELS_TO | volantis | Tier-1 | — | "By the time they reached Volantis, the sky was purple to the west" adwd-tyrion-07:11 | Jorah travels to Volantis after the Selhorys capture |
| tyrion-lannister | REVEALS_TO | aegon-targaryen-young-griff | Tier-1 | — | "'Not as your false father did. Lord Connington was the prince's dearest friend, was he not?'" adwd-tyrion-06:107 | Tyrion reveals to Aegon that he has deduced Griff's true identity as Jon Connington |
| tyrion-lannister | REVEALS_TO | aegon-targaryen-young-griff | Tier-1 | — | "'Aye. And when the pisswater prince was safely dead, the eunuch smuggled you across the narrow sea to his fat friend the cheesemonger'" adwd-tyrion-06:115 | Tyrion lays out Aegon's own origin story to him with ironic distance — a reveal of how much Tyrion has already deduced |
| widow-of-the-waterfront | REVEALS_TO | jorah-mormont | Tier-1 | — | "'She will never reach Qarth. Benerro has seen it in his fires.'" adwd-tyrion-07:419 | The widow reveals to Jorah that the Selaesori Qhoran will not reach Qarth — i.e., it will be redirected toward Meereen |

### SUSPECTED_OF edges (honest / Tier-2)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| cersei-lannister | SUSPECTED_OF | oppo-killed-by-sailors-in-volantis | Tier-2 | — | "'A gift for my sweet sister. He was another dwarf.'" adwd-tyrion-08:153 | Tyrion infers that Cersei's bounty on his head created the misidentification that killed Oppo. Also paralleled by a juggler in Tyrosh killed the same way. The book leaves the "who sent these specific sailors" entirely unproven — but the causal trail to Cersei's bounty is the only logic on offer. Tier-2, not Tier-1. |
| cersei-lannister | SUSPECTED_OF | death-of-juggler-in-tyrosh | Tier-2 | — | "'A gift for my sweet sister. He was another dwarf.'" adwd-tyrion-08:153 | Penny's account of the Tyroshi juggler (another dwarf) found dismembered in the Temple of Trios; Tyrion infers Cersei's agents. Unproven in text. **[BORDERLINE]** — the inference is Tyrion's, not confirmed. |

### Wiring the ISLANDED `varys-smuggles-tyrion-out-of-kings-landing` forward

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| varys-smuggles-tyrion-out-of-kings-landing | ENABLES | illyrio-delivers-tyrion-to-aegon-mission | Tier-1 | — | "My house is yours. Any friend of my friend across the water is a friend to Illyrio Mopatis, yes." adwd-tyrion-01:65 | Smuggling Tyrion to Pentos is the precondition for Illyrio's delivery of him to Griff's mission |

### New person/relationship dyads (NOT already in baseline)

| source | edge type | target | Tier | qualifier | verbatim quote + cite | rationale |
|--------|-----------|--------|------|-----------|-----------------------|-----------|
| penny | MOURNS | oppo | Tier-1 | — | "'He was my last family, and now he's gone too.'" adwd-tyrion-08:221 | Penny's grief for her slain brother |
| penny | COMPANION_OF | tyrion-lannister | Tier-2 | — | "Soon they began to take their meals together." adwd-tyrion-08:253 | Penny and Tyrion become shipboard companions on the Selaesori Qhoran after reconciling |
| widow-of-the-waterfront | INFORMS | tyrion-lannister | Tier-1 | — | "'Tell her we are waiting. Tell her to come soon.'" adwd-tyrion-07:423 | The widow charges Tyrion with a message to Daenerys, establishing an INFORMS relationship |
| moqorro | REVEALS_TO | tyrion-lannister | Tier-1 | — | "'Dragons,' Moqorro said … 'Dragons old and young, true and false, bright and dark. And you. A small man with a big shadow, snarling in the midst of all.'" adwd-tyrion-08:49 | Moqorro reveals his fire-vision to Tyrion, including Tyrion's own presence in it — establishing their relationship and the prophecy thread |
| tyrion-lannister | DISTRUSTS | illyrio-mopatis | Tier-1 | — | "And any friend of Varys the Spider is someone I will trust just as far as I can throw him." adwd-tyrion-01:67 | Explicit internal statement; Tyrion distrusts Illyrio from first meeting |
| tyrion-lannister | DISTRUSTS | varys | Tier-1 | — | "I should have killed the eunuch as well." adwd-tyrion-01:45 | Tyrion's explicit retrospective distrust of Varys for his role in his fate |
| tyrion-lannister | FEARS | cersei-lannister | Tier-1 | — | "There is half a world between Volantis and King's Landing, and much and more can happen along the way, ser." adwd-tyrion-07:113 | Tyrion acknowledges Cersei's reach and her desire for his head; the mushrooms in his boot are his death-escape from capture |
| illyrio-mopatis | DECEIVES | tyrion-lannister | Tier-2 | via_false_information | "'I am an old man, grown weary of this world and its treacheries. Is it so strange that I should wish to do some good before my days are done?'" adwd-tyrion-02:39 | Tyrion explicitly thinks "Liar" after this statement; Illyrio conceals his true motive for backing Aegon |

---

## Dropped / considered-but-rejected

- **`illyrio POISONS tyrion` / mushroom assassination attempt** — Illyrio's mushroom offer is ambiguous; he calls them not poisoned and eats them himself. The text (adwd-tyrion-01:209: "The mushrooms are not poisoned.") does not support a POISONS edge. SUSPECTED_OF could apply but the probability is extremely low given Illyrio proves they are safe. Dropped.
- **`tyrion MANIPULATES jon-connington (as Griff)`** — Tyrion probes Griff to confirm identity but does not genuinely manipulate him in these chapters; Griff remains cold and dismissive. Tyrion's attempts fail. Dropped.
- **`tyrion SPIES_ON aegon-targaryen-young-griff`** — The cyvasse scene is manipulation and information-gathering but not SPIES_ON (no concealment, overt conversation). Dropped.
- **`illyrio GIFTED_TO tyrion`** — The girl "bought to please the king" is offered to Tyrion but this is personal hospitality, not a graph-significant GIFTED_TO transfer. Dropped.
- **`tyrion VOWS_TO daenerys`** — No vow or oath in these chapters. The "leal servant" statement to Griff is rhetoric. Dropped.
- **`haldon INFORMS griff / jon-connington`** — Griff is ALREADY in the existing Shy-Maid household web (baseline DEDUP HOT ZONE). Do not re-mint. Dropped.
- **Re-proposing `jorah CAPTURES tyrion`** (bare dyad) — Exists per baseline. Proposed event node instead; roles attach to the event rather than re-proposing the dyad.
- **`tyrion MANIPULATES qavo-nogarys via cyvasse`** — The cyvasse game is explicitly about extracting information (Haldon's stated purpose); Tyrion's role is secondary and Qavo is not meaningfully manipulated — he answers Haldon's questions freely. Dropped.
- **`benerro PROPHESIED_BY daenerys`** — theory-gated (Azor Ahai / prophecy reading). Dropped.
- **`illyrio CONSPIRES_WITH varys`** — already in baseline. Dropped (duplicates both directions).
- **`tyrion MANIPULATES aegon`** — already exists in baseline. The two new entries above add qualifier specificity; the synthesis will decide whether to treat as enrichment of the existing edge or new variants.
- **Oppo's true name `Groat`** — noted in adwd-tyrion-08:85 ("Her brother had gone by the name of Groat, though his true name had been Oppo"). Penny's brother is `oppo`; the alias `groat` should be added to his node's frontmatter aliases. Note for synthesis: add `groat` as alias to `oppo` node.
- **`penny ALIAS_OF`** — her name is not a disguise; just a stage name. Not an ALIAS_OF edge.
- **`jorah-mormont BETRAYS daenerys`** — already in baseline. Dropped.
- **Journey travel nodes (Pentos → Ghoyan Drohe → Selhorys)** — pure travel sequence; LENS-SHARED.md warns against fabricating causal ladders from travel. Left as node-prose.

---

## Harvest

| kind | book | chapter:line | note |
|------|------|-------------|------|
| food | ADWD | adwd-tyrion-01:179 | "a broth of crab and monkfish, and cold egg lime soup"; "quails in honey, a saddle of lamb, goose livers drowned in wine, buttered parsnips, and suckling pig" — the first Pentos feast at Illyrio's table |
| food | ADWD | adwd-tyrion-01:183 | Tyrion spears a goose liver on the point of his knife; the feast meal after the mushroom standoff |
| food | ADWD | adwd-tyrion-01:187 | "Mushrooms … Kissed with garlic and bathed in butter" — the potentially poisoned mushrooms; vivid set-piece |
| food | ADWD | adwd-tyrion-01:213 | "a heron stuffed with figs, veal cutlets blanched with almond milk, creamed herring, candied onions, foul-smelling cheeses, plates of snails and sweetbreads, and a black swan in her plumage" |
| food | ADWD | adwd-tyrion-01:247 | "bowls of black cherries in sweet cream" — dessert; Tyrion wounded at the implication Myrcella would die |
| food | ADWD | adwd-tyrion-02:31 | "spiced sausage that morning, washed down with a dark smokeberry brown. Jellied eels and Dornish reds filled their afternoon. Come evening there were sliced hams, boiled eggs, and roasted larks stuffed with garlic and onions, with pale ales and Myrish fire wines" — litter journey food sequence |
| food | ADWD | adwd-tyrion-02:121 | "cold capon and a relish made of carrots, raisins, and bits of lime and orange" — horse-change stop during litter journey |
| food | ADWD | adwd-tyrion-02:155 | Illyrio produces a bag of roasted chestnuts; garlic snails from his own gardens |
| food | ADWD | adwd-tyrion-02:96 | Blackberry wine "so sweet that it drew more flies than honey" — Tyrion's morning-after drink |
| food | ADWD | adwd-tyrion-03:147 | "salt pork and cold white beans, washed down with ale" — first simple meal after the litter's rich food; Tyrion finds it a "pleasant change" |
| food | ADWD | adwd-tyrion-06:295 | "plate of roasted goat served on a bed of sliced onions … spiced and fragrant, charred outside and red and juicy within" — supper at the Painted Turtle in Selhorys |
| food | ADWD | adwd-tyrion-07:247 | "warm soft flatbread, pink fish roe, honey sausage, and fried locusts, washed down with a bittersweet black ale" — Tyrion's breakfast at the Merchant's House, in chains |
| food | ADWD | adwd-tyrion-07:179 | "a roasted duck" — Jorah tosses Tyrion half a duck while he is chained to the wall; Tyrion has to retrieve it with his face |
| food | ADWD | adwd-tyrion-08:117 | "buttered beets, cold fish stew, and biscuits that could have been used to drive nails" — shipboard supper on the Selaesori Qhoran; Penny enters |
| food | ADWD | adwd-tyrion-08:253 | "Soon they began to take their meals together" — Tyrion and Penny's shipboard reconciliation over shared meals |
| drink | ADWD | adwd-tyrion-01:107 | Tyrion finds Lord Runceford Redwyne's private stock strongwine in Illyrio's cellar: "a purple so dark that it looked almost black" |
| drink | ADWD | adwd-tyrion-07:183 | "The ale was sweet as well. It tasted of fruit." — Jorah brings Tyrion ale while chained; description of Volantene ale |
| description | ADWD | adwd-tyrion-01:55 | Illyrio description: "grotesque fat man with a forked yellow beard … His bedrobe was large enough to serve as a tourney pavilion … huge white belly and a pair of heavy breasts that sagged like sacks of suet covered with coarse yellow hair" |
| description | ADWD | adwd-tyrion-01:159 | Illyrio's rings: "onyx and opal, tiger's eye and tourmaline, ruby, amethyst, sapphire, emerald, jet and jade, a black diamond, and a green pearl" |
| description | ADWD | adwd-tyrion-03:185 | Shy Maid description: "old ramshackle single-masted poleboat … a broad beam and a shallow draft … Her paintwork was a muddy greyish brown, mottled and flaking" |
| description | ADWD | adwd-tyrion-07:71 | Temple of the Lord of Light in Volantis: "Seven save me, that's got to be three times the size of the Great Sept of Baelor … A hundred hues of red, yellow, gold, and orange … Its slender towers twisted ever upward, frozen flames dancing" |
| quote (load-bearing) | ADWD | adwd-tyrion-07:299-311 | Tyrion's reaction to hearing "Meereen" — "One word. Tyrion Lannister's world turned upside down. One word. Meereen. Or had he misheard? One word. Meereen, he said Meereen, he's taking me to Meereen. Meereen meant life." — vivid internal pivot moment; strong candidate for node ## Quotes |
| quote (load-bearing) | ADWD | adwd-tyrion-07:423 | Widow of the waterfront's message: "Tell her we are waiting. Tell her to come soon." — key political-context line for the Volantene slave/freedman community's relationship to Daenerys |
| quote (load-bearing) | ADWD | adwd-tyrion-08:49 | Moqorro's fire-vision: "'Dragons old and young, true and false, bright and dark. And you. A small man with a big shadow, snarling in the midst of all.'" — Tyrion's role in the prophecy/fire-vision chain |
| quote (load-bearing) | ADWD | adwd-tyrion-02:71 | Illyrio: "I did not think Daenerys would survive for long amongst the horselords." — his candid early assessment of Daenerys |
| hospitality | ADWD | adwd-tyrion-01:65 | "My house is yours" — Illyrio's formal welcome of Tyrion to his manse; explicitly hospitality language |
| hospitality | ADWD | adwd-tyrion-01:197 | "In the Seven Kingdoms it is considered a grave breach of hospitality to poison your guest at supper" — Tyrion's invocation of guest-right to deflect the mushroom offer; the mushroom scene as hospitality-violation framing |
| foreshadowing | ADWD | adwd-tyrion-07:95 | Tyrion observes that Benerro's prophecy has room for "just one hero" — not two Targaryens — foreshadowing the friction between the Aegon and Daenerys factions |
| foreshadowing | ADWD | adwd-tyrion-08:285 | Moqorro's shadow-vision: "A tall and twisted thing with one black eye and ten long arms, sailing on a sea of blood" — likely refers to Euron Greyjoy; candidate foreshadowing link |
| homeless find | ADWD | adwd-tyrion-03:103 | Illyrio's farewell: "Tell the boy I am sorry that I will not be with him for his wedding" — odd phrasing; the "boy's wedding" is presumably Aegon's planned marriage to Daenerys; a notable Illyrio slip showing how deep his planning for Aegon goes |
| homeless find | ADWD | adwd-tyrion-02:165 | Serra's silver locket: Illyrio's dead second wife, "big blue eyes and pale golden hair streaked by silver" from "a Lysene pillow house" — Illyrio genuinely mourns her; keeps her hands in his bedchamber; this is his stated emotional motivation beneath the political one; load-bearing for his character node |
| homeless find | ADWD | adwd-tyrion-03:103 | Illyrio swears "by my sweet Serra's hands" — confirming Serra's centrality to Illyrio's emotional life even when swearing oaths |
