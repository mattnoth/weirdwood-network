# Lens A — Arya Braavos Arc: Spine + Secondary Sub-Arcs
# Status: PROPOSED (not minted)
# Generated: 2026-06-26

---

## SECTION 1: NEW NODES

### Event Nodes

**E1**
- slug: `arya-departs-for-braavos`
- name: Arya departs Saltpans for Braavos
- type: event.incident
- scope: Arya sells Craven, presents Jaqen's iron coin to Captain Ternesio Terys on the Titan's Daughter at Saltpans; coin + "Valar morghulis" secures her cabin passage to Braavos.

**E2**
- slug: `arya-arrives-braavos-skull-test`
- name: Arya arrives at the House of Black and White — skull test
- type: event.deception
- scope: Yorko rows Arya ashore; she climbs to the HoBaW doors; the kindly man reveals a death-skull face to test her courage; she kisses it and eats the grave worm; he reveals his true (gentle old man) face and accepts her inside.
- Note: Models like `sansa-adopts-the-alayne-stone-identity` — this is the first identity-threshold event of the arc.

**E3**
- slug: `arya-becomes-novice-in-hobaw`
- name: Arya accepts novice status in the House of Black and White
- type: event.deception
- scope: Arya throws possessions into the canal (hides Needle under a step); answers the kindly man's truthfulness test; is accepted as a novice acolyte and given black-and-white robes. Parallel to `sansa-adopts-the-alayne-stone-identity` in mechanism (identity surrender ritual).

**E4**
- slug: `arya-assumes-cat-of-the-canals-identity`
- name: Arya assumes the "Cat of the Canals" identity
- type: event.deception
- scope: Kindly man assigns Arya the cover identity "Cat, orphan of King's Landing," sends her to work for Brusco selling shellfish at Ragman's Harbor; she begins reporting intelligence back to the HoBaW each dark moon.

**E5**
- slug: `arya-kills-dareon`
- name: Arya kills Dareon the deserter
- type: event.assassination
- scope: Cat of the Canals kills Dareon (Night's Watch deserter) in an alley near the Happy Port; his throat is slit, boots taken, body pushed into a canal. An unauthorized kill — she chose the target herself, not by FM assignment.

**E6**
- slug: `arya-blinding-punishment`
- name: Arya blinded by the kindly man as punishment for killing Dareon
- type: event.incident
- scope: Kindly man gives Arya warm milk (a slow-acting potion); she wakes blind the next morning. Explicitly framed as punishment for killing Dareon outside FM sanction.

**E7**
- slug: `arya-blind-girl-training`
- name: Arya's blind-girl training period (Blind Beth)
- type: event.incident
- scope: Arya trains blind for an extended period as "Blind Beth the beggar girl" — stick-fighting under anonymous tutor (revealed as kindly man), sensory training, poison lessons with waif, language study (High Valyrian / Lyseni / Pentoshi), lying game without eyes.

**E8**
- slug: `arya-wargs-the-tomcat-at-pyntos`
- name: Arya wargs into the tomcat at Pynto's tavern
- type: event.incident
- scope: While begging blind at Pynto's, Arya perceives the Lyseni sailors at their table through the tomcat's slitted yellow eyes — involuntary warg episode that gives her intelligence she could not have gained without sight.

**E9**
- slug: `arya-sight-restored`
- name: Arya's sight restored
- type: event.incident
- scope: After Arya identifies the kindly man as her stick-training antagonist (proving sensory mastery), the waif's milk-cup at supper has changed: she wakes next morning to see a tallow candle burning. Sight restored as reward for demonstrated mastery of the other senses.

**E10**
- slug: `arya-first-assassination-insurance-underwriter`
- name: Arya's first sanctioned FM assassination — the insurance underwriter
- type: event.assassination
- scope: Arya (as the "ugly girl" wearing a dead woman's face) executes the coin-swap assassination: she slits a shipowner's purse, palms a Westerosi gold dragon, plants it in the target's payment — the underwriter accepts the coin, pays it out; "his heart gave out." First kill on FM orders.

**E11**
- slug: `arya-receives-dead-girls-face`
- name: Arya receives a dead girl's face / earns acolyte robe
- type: event.incident
- scope: Kindly man takes Arya to the third-level sanctum (room of a thousand faces); she is given the ugly/broken face of a dead girl for the assassination mission, then given back the face of Arya Stark + full acolyte robes after success.

---

## SECTION 2: EDGES

All edges below are PROPOSED. Format: `(source, TYPE, target) | Tier | chapter:line | "verbatim quote" | rationale`

---

### CAUSAL SPINE

**SP-01**
`(arya-departs-for-braavos, ENABLES, arya-arrives-braavos-skull-test)` | Tier 1 | affc-arya-01.md:77 | "Our voyage is at an end. We make for the Chequy Port … There is no need for you to wait upon their pleasure. Gather your belongings. I shall lower a boat, and Yorko will put you ashore." | Departure → arrival. ENABLES: journey transition opens the door; Arya must walk through it.

**SP-02**
`(arya-arrives-braavos-skull-test, CAUSES, arya-becomes-novice-in-hobaw)` | Tier 1 | affc-arya-02.md:213 | "Yes," she said, and from that moment she was a novice in the House of Black and White." | Passing the skull test gains entry; the subsequent identity-surrender rituals across Arya I–II culminate in novice acceptance. CAUSES (produces-through-steps, not immediate).

**SP-03**
`(arya-becomes-novice-in-hobaw, ENABLES, arya-assumes-cat-of-the-canals-identity)` | Tier 1 | affc-arya-02.md:311–313 | "Along the wharves below the Drowned Town you will find a fishmonger named Brusco, a good man with a bad back. He has need of a girl to push his barrow and sell his cockles, clams, and mussels to the sailors off the ships. You shall be that girl." | Novice status is the precondition the kindly man requires before sending her into Braavos under a cover identity.

**SP-04**
`(arya-assumes-cat-of-the-canals-identity, CAUSES, arya-kills-dareon)` | Tier 1 | affc-cat-of-the-canals-01.md:141–143 | "He is a man of the Night's Watch, she thought, as he sang about some stupid lady throwing herself off some stupid tower because her stupid prince was dead … And the singer should be on the Wall." | Cat's daily wharfside presence is what puts her in Dareon's orbit; she would not have encountered him otherwise.

**SP-05**
`(arya-kills-dareon, CAUSES, arya-blinding-punishment)` | Tier 1 | adwd-the-blind-girl-01.md:141 | "I killed Cat when I killed that singer. The kindly man had told her that they would have taken her eyes from her anyway, to help her to learn to use her other senses, but not for half a year." | Explicitly stated causal connection: killing Dareon accelerated the blinding by ~6 months.

**SP-06**
`(arya-blinding-punishment, ENABLES, arya-blind-girl-training)` | Tier 1 | adwd-the-blind-girl-01.md:87–89 | "On the day she had woken blind, the waif took her by the hand and led her through the vaults and tunnels of the rock on which the House of Black and White was built, up the steep stone steps into the temple proper. 'Count the steps as you climb,' she had said." | Blindness is the precondition that opens the entire blind-training curriculum.

**SP-07**
`(arya-blind-girl-training, ENABLES, arya-wargs-the-tomcat-at-pyntos)` | Tier 1 | adwd-the-blind-girl-01.md:179 | "And for a time it seemed that she could see them too, through the slitted yellow eyes of the tomcat purring in her lap." | The begging rounds as Blind Beth are what put her in Pynto's, and being sightless creates the sensory deprivation that appears to lower the warging threshold.

**SP-08**
`(arya-blind-girl-training, ENABLES, arya-sight-restored)` | Tier 1 | adwd-the-blind-girl-01.md:189–193 | "I know that you're the one who has been hitting me." Her stick flashed out, and cracked against his fingers, sending his own stick clattering to the floor. … That evening Umma served salt-crusted crabs for supper. When her cup was presented to her, the blind girl wrinkled her nose and drank it down … And come the morning, when the night wolf left her and she opened her eyes, she saw a tallow candle burning where no candle had been the night before." | Demonstrated mastery of senses (identifying the kindly man) triggers the changed cup and sight restoration.

**SP-09**
`(arya-sight-restored, ENABLES, arya-first-assassination-insurance-underwriter)` | Tier 1 | adwd-the-ugly-little-girl-01.md:83–85 | "'Then on the morrow, you shall be Cat of the Canals again. Wear that face, watch, obey. And we will see if you are truly worthy to serve Him of Many Faces.' So the next day she returned to Brusco and his daughters." | Restoration of sight (and the trial that precedes it) qualifies her for the plague-faced priest's challenge and the assassination assignment.

**SP-10**
`(arya-first-assassination-insurance-underwriter, ENABLES, arya-receives-dead-girls-face)` | Tier 1 | adwd-the-ugly-little-girl-01.md:261–265 | "'You have much and more to learn, but it may be you are not hopeless.' That night they gave her back the face of Arya Stark. They brought a robe for her as well, the soft thick robe of an acolyte … 'On the morrow you will go to Izembaro to begin your first apprenticeship.'" | Successful assassination earns the face + acolyte robe + the Izembaro assignment.

---

### DEPARTURE EVENT — PARTICIPANT ROLES

**D-01**
`(arya-stark, AGENT_IN, arya-departs-for-braavos)` | Tier 1 | asos-arya-13.md:259 | "Arya crossed her arms against her chest. 'Valar morghulis,' she said, as loud as if she'd known what it meant." | Arya is the actor who presents the coin and triggers the departure.

**D-02**
`(ternesio-terys, AGENT_IN, arya-departs-for-braavos)` | Tier 1 | asos-arya-13.md:251 | "'This is the galleas Titan's Daughter, of the Free City of Braavos.'" + asos-arya-13.md:261 | "'Valar dohaeris,' he replied, touching his brow with two fingers. 'Of course you shall have a cabin.'" | Ternesio's recognition of the coin and his granting passage make him a co-agent in the departure event.

**D-03**
`(denyo-terys, WITNESS_IN, arya-departs-for-braavos)` | Tier 1 | affc-arya-01.md:15–19 | "'The star of home,' said Denyo. His father was shouting orders … Arya stood at the prow, one hand resting on the gilded figurehead … For half a heartbeat she let herself pretend that it was her home ahead." | Denyo is present and named as Arya's companion-witness at the prow during the final approach; he witnesses her arrival context throughout the voyage.

---

### SKULL TEST EVENT — PARTICIPANT ROLES

**ST-01**
`(kindly-man, AGENT_IN, arya-arrives-braavos-skull-test)` | Tier 1 | affc-arya-01.md:195 | "The priest lowered his cowl. Beneath he had no face; only a yellowed skull with a few scraps of skin still clinging to the cheeks, and a white worm wriggling from one empty eye socket. 'Kiss me, child,' he croaked, in a voice as dry and husky as a death rattle." | The kindly man administers the test.

**ST-02**
`(arya-stark, AGENT_IN, arya-arrives-braavos-skull-test)` | Tier 1 | affc-arya-01.md:197 | "Does he think to scare me? Arya kissed him where his nose should be and plucked the grave worm from his eye to eat it, but it melted like a shadow in her hand." | Arya is the one tested; her action (kissing the skull, eating the worm) is what passes the test.

**ST-03**
`(waif, WITNESS_IN, arya-arrives-braavos-skull-test)` | Tier 1 | affc-arya-01.md:145–167 | "A hand touched her arm. Arya spun away, but it was only a little girl: a pale little girl in a cowled robe … The girl said some words that Arya did not know … A voice behind her said, 'I do.'" | The waif is present and flanks the encounter; she witnesses Arya's skull-test and the kindly man's reveal.

---

### NOVICE ACCEPTANCE — PARTICIPANT ROLES

**NV-01**
`(arya-stark, AGENT_IN, arya-becomes-novice-in-hobaw)` | Tier 1 | affc-arya-02.md:155–167 | "Her floppy hat went next, then the gloves … Her dagger followed … Her swordbelt went into the canal. Her cloak, tunic, breeches, smallclothes, all of it. All but Needle … 'You'll be safe here,' she told Needle." | Arya performs the identity-stripping ceremony.

**NV-02**
`(kindly-man, COMMANDS_IN, arya-becomes-novice-in-hobaw)` | Tier 1 | affc-arya-02.md:97–103 | "He picked up her silver fork. 'This belongs to Arya of House Stark. All these things belong to her. There is no place for them here … Before you drink from the cold cup, you must offer up all you are to Him of Many Faces.'" | The kindly man issues the command that triggers the ceremony; Arya executes it.

**NV-03**
`(waif, WITNESS_IN, arya-becomes-novice-in-hobaw)` | Tier 1 | affc-arya-02.md:97 | "One night the waif happened to be passing and saw Arya at her swordplay. The girl did not say a word, but the next day, the kindly man walked Arya back to her cell." | The waif's sighting of Arya practicing with Needle is the precipitating observation that triggers the kindly man's command.

---

### CAT OF THE CANALS IDENTITY — PARTICIPANT ROLES

**CT-01**
`(arya-stark, AGENT_IN, arya-assumes-cat-of-the-canals-identity)` | Tier 1 | affc-arya-02.md:325–327 | "Could I be Cat?" / "Cat … Yes. Braavos is full of cats. One more will not be noticed. You are Cat, an orphan of …" / "King's Landing." | Arya proposes and accepts the identity.

**CT-02**
`(kindly-man, COMMANDS_IN, arya-assumes-cat-of-the-canals-identity)` | Tier 1 | affc-arya-02.md:311 | "Along the wharves below the Drowned Town you will find a fishmonger named Brusco, a good man with a bad back. He has need of a girl to push his barrow and sell his cockles, clams, and mussels to the sailors off the ships. You shall be that girl." | The kindly man authorizes and frames the identity.

**CT-03**
`(arya-assumes-cat-of-the-canals-identity, ALIAS_OF, arya-stark)` | Tier 1 | affc-cat-of-the-canals-01.md:23 | "I am a cat now, not a wolf. I am Cat of the Canals. The wolf dreams belonged to Arya of House Stark." | Explicit identity-alias statement in Arya's own interior monologue.

---

### KILLING OF DAREON — PARTICIPANT ROLES

**KD-01**
`(arya-stark, AGENT_IN, arya-kills-dareon)` | Tier 1 | affc-cat-of-the-canals-01.md:233 | "Dareon is dead. The black singer who was sleeping at the Happy Port. He was really a deserter from the Night's Watch. Someone slit his throat and pushed him into a canal, but they kept his boots." | Arya reports the kill as her own act; the "someone" is her cover admission.

**KD-02**
`(dareon, VICTIM_IN, arya-kills-dareon)` | Tier 1 | affc-cat-of-the-canals-01.md:233 | "Dareon is dead. The black singer who was sleeping at the Happy Port." | Dareon is the named victim.

**KD-03**
`(arya-kills-dareon, AGENT_IN, arya-stark)` | SKIP — covered by KD-01 above (same edge direction). [Using KD-01 formulation.]

**KD-04**
`(arya-kills-dareon, LOCATED_AT, braavos)` | Tier 1 | affc-cat-of-the-canals-01.md:157–163 | "Dareon was leaving too … They crossed a little bridge, and made their way down a crooked back street as the shadows of the day grew longer … 'Just so,' said Cat as they stepped into the gloom of a twisty little alley." | The alley near the Happy Port is in Braavos.

---

### BLINDING PUNISHMENT — PARTICIPANT ROLES

**BL-01**
`(kindly-man, AGENT_IN, arya-blinding-punishment)` | Tier 1 | affc-cat-of-the-canals-01.md:247–251 | "'My throat is dry. Do me a kindness and bring a cup of wine for me and warm milk for our friend Arya … When the milk came, Arya drank it down. It smelled a little burnt and had a bitter aftertaste. 'Go to bed now, child,' the kindly man said. 'On the morrow you must serve.'" + affc-cat-of-the-canals-01.md:255 "When she woke the next morning, she was blind." | The kindly man orders the milk and thereby administers the blinding.

**BL-02**
`(arya-stark, VICTIM_IN, arya-blinding-punishment)` | Tier 1 | affc-cat-of-the-canals-01.md:255 | "When she woke the next morning, she was blind." | Arya is blinded.

**BL-03**
`(waif, AGENT_IN, arya-blinding-punishment)` | Tier 2 | adwd-the-blind-girl-01.md:79 | "Each night at supper the waif brought her a cup of milk and told her to drink it down. The drink had a queer, bitter taste that the blind girl soon learned to loathe." | The waif is the one who delivers the ongoing blindness-maintenance cups; she likely administered the initial dose on the kindly man's orders. Tier 2: the initial dose in cat-of-the-canals is described as waif-fetched (per the kindly man's order at line 247), so participation is very strong but slightly indirect.

---

### BLIND-GIRL TRAINING — PARTICIPANT ROLES

**BT-01**
`(arya-stark, AGENT_IN, arya-blind-girl-training)` | Tier 1 | adwd-the-blind-girl-01.md:87–89 | "On the day she had woken blind, the waif took her by the hand and led her through the vaults and tunnels … 'Count the steps as you climb,' she had said. 'Let your fingers brush the wall. There are markings there, invisible to the eye, plain to the touch.' That was her first lesson." | Arya undergoes the training.

**BT-02**
`(waif, AGENT_IN, arya-blind-girl-training)` | Tier 1 | adwd-the-blind-girl-01.md:87–91 | "the waif took her by the hand and led her through the vaults … Poisons and potions were for the afternoons … the waif's more toxic concoctions even smell was less than safe." | The waif is the primary instructor during the blind period.

**BT-03**
`(kindly-man, AGENT_IN, arya-blind-girl-training)` | Tier 1 | adwd-the-blind-girl-01.md:123–127 | "'Who is there?' she asked. 'No one.' The voice was deep, harsh, cold … Wood clacked against wood … 'Good,' the voice said." + adwd-the-blind-girl-01.md:189 "I know that you're the one who has been hitting me." | The kindly man is Arya's secret stick-combat trainer during the blind period.

**BT-04**
`(waif, TUTORS, arya-stark)` | Tier 1 | adwd-the-blind-girl-01.md:87 | "the waif took her by the hand and led her through the vaults and tunnels of the rock on which the House of Black and White was built … 'Count the steps as you climb'" | Ongoing tutoring relationship, formalized during blind period.

---

### TOMCAT WARG — PARTICIPANT ROLES

**WG-01**
`(arya-stark, AGENT_IN, arya-wargs-the-tomcat-at-pyntos)` | Tier 1 | adwd-the-blind-girl-01.md:179 | "And for a time it seemed that she could see them too, through the slitted yellow eyes of the tomcat purring in her lap. One was old and one was young and one had lost an ear, but all three had the white-blond hair and smooth fair skin of Lys." | Arya is the warg.

**WG-02**
`(arya-stark, WARGS_INTO, arya-wargs-the-tomcat-at-pyntos)` | NEEDS_VOCAB: WARGS_INTO is in the locked list; but the target here is the event, not the cat itself. The correct formulation is (arya-stark, WARGS_INTO, [tomcat]) as a dyad edge, not a role on the event. Propose as a bare dyad: `(arya-stark, WARGS_INTO, [unnamed-pyntos-tomcat])`. Since there is no existing tomcat node and one would be single-use, I recommend NOT minting a node for it. Instead propose:

`(arya-stark, AGENT_IN, arya-wargs-the-tomcat-at-pyntos)` — already above as WG-01 — and use the event node as the reification.

---

### SIGHT RESTORED — PARTICIPANT ROLES

**SR-01**
`(arya-stark, AGENT_IN, arya-sight-restored)` | Tier 1 | adwd-the-blind-girl-01.md:199 | "And come the morning, when the night wolf left her and she opened her eyes, she saw a tallow candle burning where no candle had been the night before, its uncertain flame swaying back and forth like a whore at the Happy Port. She had never seen anything so beautiful." | Arya experiences the restoration.

**SR-02**
`(kindly-man, AGENT_IN, arya-sight-restored)` | Tier 1 | adwd-the-blind-girl-01.md:33 | "'Poor child,' said the kindly man. 'Would you like to have your eyes back? Ask, and you shall see.'" + adwd-the-blind-girl-01.md:147 "'You lie. And that is why you must now walk in darkness until you see the way. Unless you wish to leave us. You need only ask, and you may have your eyes back.'" | The kindly man holds the power over sight restoration; the changed cup that produces it is his decision.

**SR-03**
`(waif, AGENT_IN, arya-sight-restored)` | Tier 2 | adwd-the-blind-girl-01.md:195–199 | "When her cup was presented to her, the blind girl wrinkled her nose and drank it down in three long gulps. Then she gasped and dropped the cup. Her tongue was on fire … 'Wine will not help, and water will just fan the flames,' the waif told her. 'Eat this.'" | The waif presents the changed cup; the fire-drink is the mechanism that produces restored sight. Tier 2: causal link between fire-cup and restored sight is shown sequentially but not explicitly stated.

---

### FIRST FM ASSASSINATION — PARTICIPANT ROLES

**AS-01**
`(arya-stark, AGENT_IN, arya-first-assassination-insurance-underwriter)` | Tier 1 | adwd-the-ugly-little-girl-01.md:247 | "Her blade flashed out, smooth and quick, one deep slash through the velvet and he never felt a thing. Red Roggo would have smiled to see it. She slipped her hand through the gap, slit the purse open with the finger knife, filled her fist with gold." | Arya executes the coin-swap.

**AS-02**
`([unnamed-insurance-underwriter], VICTIM_IN, arya-first-assassination-insurance-underwriter)` | Tier 1 | adwd-the-ugly-little-girl-01.md:261 | "And with that coin and the others in his purse, he paid a certain man. Soon after that man's heart gave out. Is that the way of it? Very sad." | The unnamed old man is the target; death confirmed by kindly man.
- Note: The victim is unnamed throughout the chapter. His role is "insurance underwriter / binder-writer at the soup shop near Purple Harbor." Do NOT mint a node for him — he has zero graph utility without a slug. Record the Tier-1 quote on the event node as evidence_quote.

**AS-03**
`(kindly-man, COMMANDS_IN, arya-first-assassination-insurance-underwriter)` | Tier 1 | adwd-the-ugly-little-girl-01.md:71–81 | "'Give a certain man a certain gift. Can you do that?' … 'He is one of them. A stranger. No one you love, no one you hate, no one you have ever known. Will you kill him?' 'Yes.'" | The plague-faced priest (FM brother) assigns the task; the kindly man presides and confirms outcome.

**AS-04**
`([plague-face-priest], COMMANDS_IN, arya-first-assassination-insurance-underwriter)` | Tier 1 | adwd-the-ugly-little-girl-01.md:15–17 | "'I know this man,' she did hear a priest with the face of a plague victim say." + adwd-the-ugly-little-girl-01.md:71 | "'Give a certain man a certain gift. Can you do that?'" | The plague-faced priest (unnamed FM brother) issues the specific assignment. Note: he is not an existing node. Propose minting `plague-face-priest` as a character node — type: character, aliases: ["the plague-face priest"], affiliations: faceless-men — only if the synthesizer agrees.

---

### DEAD GIRL'S FACE / ACOLYTE PROMOTION — PARTICIPANT ROLES

**FA-01**
`(arya-stark, AGENT_IN, arya-receives-dead-girls-face)` | Tier 1 | adwd-the-ugly-little-girl-01.md:189 | "Arya bit her lip. She did not know what she wanted. If I leave, where will I go? … 'Do it,' she blurted out." | Arya consents and undergoes the procedure.

**FA-02**
`(kindly-man, AGENT_IN, arya-receives-dead-girls-face)` | Tier 1 | adwd-the-ugly-little-girl-01.md:173–195 | "The kindly man took the iron lantern off its hook and led her … to the steps at the rear of the temple … 'Sit,' the priest commanded … 'This will hurt,' he warned her, 'but pain is the price of power. Do not move.' Still as stone, she thought. She sat unmoving. The cut was quick, the blade sharp." | Kindly man administers the face-cutting and face-donning.

**FA-03**
`(waif, AGENT_IN, arya-receives-dead-girls-face)` | Tier 1 | adwd-the-ugly-little-girl-01.md:197 | "'Bring me the face,' said the kindly man. The waif made no answer, but she could hear her slippers whispering over the stone floor." | Waif retrieves and hands the face to the kindly man.

---

### SECONDARY SUB-ARC: TERNESIO TERYS

**TT-01**
`(ternesio-terys, CAPTAIN_OF, titans-daughter)` | Tier 1 | asos-arya-13.md:251 | "'This is the galleas Titan's Daughter, of the Free City of Braavos.'" + affc-arya-01.md:77 | "Tradesman-Captain Ternesio Terys wore no whiskers and kept his grey hair cut short and neat." | Ternesio is explicitly named as tradesman-captain.

**TT-02**
`(arya-stark, TRAVELS_TO, braavos)` | Tier 1 | affc-arya-01.md:17–19 | "The decks tilted, creaking, as the galleas Titan's Daughter heeled to starboard and began to come about … Arya stood at the prow, one hand resting on the gilded figurehead." | Travel event: Arya aboard Titan's Daughter arriving at Braavos.

---

### SECONDARY SUB-ARC: KINDLY MAN

**KM-01**
`(kindly-man, OFFICIATES, arya-arrives-braavos-skull-test)` | NEEDS_VOCAB: OFFICIATES is in the locked list; use for ceremonies/trials where someone presides. Retag as:
`(kindly-man, AGENT_IN, arya-arrives-braavos-skull-test)` — already covered in ST-01. Drop this entry.

**KM-02**
`(kindly-man, REVEALS_TO, arya-stark)` | Tier 1 | affc-arya-02.md:173–191 | "The tale of our beginnings … Men may whisper of the Faceless Men of Braavos, but we are older than the Secret City … The first Faceless Man was one who did." | Kindly man reveals FM origin story to Arya — a REVEALS_TO edge for the Valyrian slave-mine founding narrative. This is load-bearing for the theology arc.

**KM-03**
`(kindly-man, TEACHES, arya-stark)` | Tier 1 | affc-arya-02.md:203–207 | "A man does not need to be a wizard to know truth from falsehood, not if he has eyes. You need only learn to read a face. Look at the eyes. The mouth. The muscles here, at the corners of the jaw … Some liars blink. Some stare." | Explicit teaching of lie-detection. (Existing `kindly-man TEACHES arya` dyad confirmed; this is the book-chapter citation overlay for that dyad's specific content.)

---

### SECONDARY SUB-ARC: WAIF

**WF-01**
`(waif, TUTORS, arya-stark)` | Tier 1 | affc-arya-02.md:211 | "'She will teach you,' said the kindly man as the waif appeared outside her door. 'Starting with the tongue of Braavos. What use are you if you cannot speak or understand? And you shall teach her your own tongue. The two of you shall learn together, each from the other.'" | Waif formally assigned as language tutor.

**WF-02**
`(waif, TUTORS, arya-stark)` [Poison curriculum] | Tier 1 | affc-cat-of-the-canals-01.md:183 | "'Sweetsleep is the gentlest of poisons,' the waif told her, as she was grinding some with a mortar and pestle." | Poison curriculum: waif teaches Arya sweetsleep, tears of Lys, basilisk-blood paste.

Note: WF-01 and WF-02 are two cite-ref overlays for the same existing `waif TUTORS arya` dyad. Recommend recording both as separate evidence_quote rows on the same edge node.

**WF-03**
`(waif, DECEIVES, arya-stark)` | Tier 1 | affc-arya-02.md:219–223 | "The next day they began the lying game … 'Who are you?' the waif asked her once … 'Ten,' said Arya … The waif showed ten fingers. Then ten again, and yet again. Then six. Her face remained as smooth as still water … 'You're lying,' she said. The waif shook her head and showed her once again: ten and ten and ten and six." | The waif deliberately lies during the lying game as a training exercise — DECEIVES in context of structured pedagogy.

---

### SECONDARY SUB-ARC: BRUSCO / CAT IDENTITY MAINTENANCE

**BR-01**
`(brusco, EMPLOYED_BY, arya-stark)` | NEEDS_VOCAB: No EMPLOYS or EMPLOYED_BY in locked list. The correct formulation is the existing `arya SERVES brusco` dyad, which is already in dedup. Drop.

**BR-02**
`(arya-assumes-cat-of-the-canals-identity, LOCATED_AT, braavos)` | Tier 1 | affc-cat-of-the-canals-01.md:59 | "Cat headed for the Ragman's Harbor, as she did nine days of every ten." | Cat's home base is explicitly Ragman's Harbor, Braavos.

---

### NEEDLE HIDING — SUB-BEAT

**NE-01**
`(arya-hides-needle-on-hobaw-steps, SUB_BEAT_OF, arya-becomes-novice-in-hobaw)` | Tier 1 | affc-arya-02.md:165–167 | "'You'll be safe here,' she told Needle. 'No one will know where you are but me.' She pushed the sword and sheath behind the step, then shoved the stone back into place, so it looked like all the other stones. As she climbed back to the temple, she counted steps, so she would know where to find the sword again." | Hiding Needle is a sub-beat of the novice acceptance event — the one thing Arya withholds from the FM's demand for total surrender.

This requires a new node:
- slug: `arya-hides-needle-on-hobaw-steps`
- name: Arya hides Needle on the HoBaW steps
- type: event.deception
- scope: During the novice identity-stripping ritual, Arya throws all possessions into the canal but secretly hides Needle under a loose step on the temple stairway, counting the steps so she can retrieve it.

**NE-02**
`(arya-stark, AGENT_IN, arya-hides-needle-on-hobaw-steps)` | Tier 1 | affc-arya-02.md:165–167 | same quote as NE-01 | Arya is the sole agent.

**NE-03**
`(needle, OWNED, arya-stark)` — already likely exists; this is the cite-ref overlay:
`(needle, [edge TBD — OWNS?], arya-stark)` | Tier 1 | affc-arya-02.md:161 | "Needle was Robb and Bran and Rickon, her mother and her father, even Sansa. Needle was Winterfell's grey walls, and the laughter of its people." | The emotional ownership / symbolic meaning quote — high-value evidence_quote for any existing Needle-Arya edge.

---

## SECTION 3: PROPOSED NODE MINT — PLAGUE-FACE PRIEST

The priest who assigns the assassination is unnamed but is a distinct FM agent worth minting if he will appear in the graph for other reasons (he may be the same character as the "Faceless Man who was Jaqen" — this is theory-gated, do not assert). Proposed node:
- slug: `plague-face-priest`
- name: Plague-faced Faceless Man
- type: character
- aliases: ["the plague-face priest", "the priest with the face of a plague victim"]
- affiliations: faceless-men
- Note to synthesizer: Do NOT link to jaqen-hghar via SAME_AS — that is theory-gated.

---

## SUMMARY: SPINE SHAPE (6–10 lines)

The arc builds as a single causal chain with two major punishments that reshape Arya's training trajectory. The departure node (`arya-departs-for-braavos`) ENABLES arrival; arrival CAUSES — through multiple intermediate identity-surrender rituals — her novice acceptance (`arya-becomes-novice-in-hobaw`). Novice status ENABLES the Cat-of-the-Canals identity, which puts her in Dareon's orbit. Arya's unauthorized killing of Dareon (`arya-kills-dareon`) CAUSES an accelerated blinding (`arya-blinding-punishment`) — the arc's first major punitive hinge. The blinding ENABLES the full blind-girl training curriculum, which in turn ENABLES both the tomcat warg event (a sensory-deprivation side-effect) and eventually the sight restoration when she demonstrates mastery by identifying the kindly man. Sight restored ENABLES the first sanctioned FM assassination (the insurance underwriter coin-swap), and successful assassination ENABLES her receiving a dead girl's face and the full acolyte robe + dispatch to Izembaro. The key structural insight: this is not a smooth apprenticeship — it is a chain twice interrupted by punishment/loss (Dareon→blinding; assassination isolation via ugly-girl face), with each interruption deepening the FM conditioning. The Needle-hiding sub-beat is the moral seam: even at the moment of maximum identity surrender, something Stark-core survives.
