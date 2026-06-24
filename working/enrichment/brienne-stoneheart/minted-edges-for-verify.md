# Minted edges (S141 Brienne-Stoneheart) — 40 edges to adversarially verify

1. `rorge --AGENT_IN--> raid-on-saltpans` | tier-1 | sources/chapters/affc/affc-brienne-08.md:215
   quote: "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse."
   asserted: Brienne names Rorge as the Saltpans raider (he wore Sandor's helm). AGENT_IN = physical actor. The node previously had 0 participant edges.
   verified_by: (structural, verified=None)

2. `biter --AGENT_IN--> raid-on-saltpans` | tier-2 | sources/chapters/affc/affc-brienne-06.md:131
   quote: "her breasts had been torn and chewed and eaten, as if by some . . . cruel beast."
   asserted: The Elder Brother's account of a Saltpans victim eaten alive matches Biter's signature cannibalism (he is Rorge's constant companion per the raid node body). Tier-2: the 'cruel beast' identification is strong inference, not a named cite.
   verified_by: pending-fresh-verify-s141

3. `brave-companions --ENABLES--> raid-on-saltpans` | tier-1 | sources/chapters/affc/affc-brienne-04.md:273
   quote: "We all went our own ways, after we left Harrenhal. Urswyck and his lot rode south for Oldtown. Rorge thought he might slip out at Saltpans."
   asserted: The Brave Companions' dissolution at Harrenhal dispersed the remnant; Rorge's band fled toward Saltpans seeking a ship, putting them in position to sack it. ENABLES = distal door-opener.
   verified_by: pending-fresh-verify-s141

4. `capture-of-harrenhal --ENABLES--> raid-on-saltpans` | tier-2 | sources/chapters/affc/affc-brienne-04.md:273
   quote: "We all went our own ways, after we left Harrenhal."
   asserted: The Lannister recapture of Harrenhal (the Mountain killing Hoat) ended the Brave Companions' hold and scattered them — without that dissolution there is no Rorge-band at Saltpans. Cross-arc seam (Harrenhal/Lannister arc -> Brienne arc). Tier-2: the link is wiki-corroborated; the AFFC quote names the leaving-of-Harrenhal but not the capture-event by name.
   verified_by: pending-fresh-verify-s141

5. `raid-on-saltpans --LOCATED_AT--> saltpans` | tier-1 | sources/chapters/affc/affc-brienne-06.md:131
   quote: "They burned everything at Saltpans, save the castle."
   asserted: Event location is definitional; the islanded node had no LOCATED_AT. LOCATED_AT = event -> place.
   verified_by: (structural, verified=None)

6. `elder-brother-quiet-isle --ENABLES--> raid-on-saltpans` | tier-1 | sources/chapters/affc/affc-brienne-06.md:185
   quote: "set his helm atop the cairn to mark his final resting place. That was a grievous error."
   asserted: The Elder Brother's placing of Sandor's helm on the grave-cairn (which Rorge then found and wore) is the inadvertent precondition for the misattributed raid — he himself calls it 'a grievous error.' ENABLES = accidental door-opener, not CAUSES.
   verified_by: pending-fresh-verify-s141

7. `raid-on-saltpans --MOTIVATES--> brienne-tarth` | tier-1 | sources/chapters/affc/affc-brienne-05.md:127
   quote: "Sandor Clegane was last seen in Saltpans, the day of the raid. Afterward he rode west, along the Trident."
   asserted: The Saltpans raid (falsely attributed to the Hound) pivots Brienne's quest toward hunting Sandor along the Trident. MOTIVATES = event -> character (motive moves a person).
   verified_by: pending-fresh-verify-s141

8. `randyll-tarly --DECEIVES--> brotherhood-without-banners` | tier-1 | sources/chapters/affc/affc-brienne-05.md:135
   quote: "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood."
   asserted: Tarly deliberately spreads a false rumor blaming the Saltpans raid on Beric's Brotherhood to strip their popular support. DECEIVES = deliberate false narrative aimed at the organization (he hunts the Hound simultaneously, so he knows it's false).
   verified_by: pending-fresh-verify-s141

9. `quincy-cox --WITNESS_IN--> raid-on-saltpans` | tier-2 | sources/chapters/affc/affc-brienne-06.md:131
   quote: "her worst curses were not for the men who had raped her, nor the monster who devoured her living flesh, but for Ser Quincy Cox, who barred his gates when the outlaws entered the town and sat safe behind stone walls as his people screamed and died."
   asserted: Cox watched the raid from his holdfast battlements (per the dying woman's curse + the raid node body 'tells what saw from the battlements') and did nothing. WITNESS_IN = load-bearing perceiver. Tier-2: text-anchor is the survivor's curse, not Cox's own POV.
   verified_by: pending-fresh-verify-s141

10. `sandor-clegane --OWNS--> hound-helm` | tier-1 | sources/chapters/affc/affc-brienne-06.md:185
   quote: "I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place."
   asserted: The dog's-head greathelm is Sandor's signature piece; the Elder Brother marks his grave with it. OWNS = possessor -> artifact.
   verified_by: (structural, verified=None)

11. `hound-helm --LOOTED_BY--> rorge` | tier-1 | sources/chapters/affc/affc-brienne-08.md:215
   quote: "He took the helm from Clegane's grave, and you stole it off his corpse."
   asserted: Rorge takes the helm off Sandor's grave-cairn. LOOTED_BY = artifact -> new holder (the transactional taking).
   verified_by: (structural, verified=None)

12. `hound-helm --WIELDED_IN--> raid-on-saltpans` | tier-2 | sources/chapters/affc/affc-brienne-06.md:185
   quote: "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous."
   asserted: Rorge wore the helm during the Saltpans raid, which is precisely what made the realm misattribute it to Sandor. WIELDED_IN = artifact -> event (instrument of the misattribution). Tier-2: the wearing-at-Saltpans is established by the misID, not shown on-page.
   verified_by: pending-fresh-verify-s141

13. `hound-helm --WIELDED_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:265
   quote: "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling."
   asserted: Rorge wears the dog's-head helm leading the inn attack (Brienne's face is mashed against it as she kills him). WIELDED_IN = artifact -> event.
   verified_by: (structural, verified=None)

14. `hound-helm --LOOTED_BY--> lem` | tier-1 | sources/chapters/affc/affc-brienne-08.md:215
   quote: "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse."
   asserted: Lem Lemoncloak strips the helm off Rorge's corpse after the inn fight and wears it himself. LOOTED_BY = artifact -> new holder. (`lem` = Lem Lemoncloak, aliases incl. 'The Hound (III)'.)
   verified_by: (structural, verified=None)

15. `ambush-at-crossroads-inn --LOCATED_AT--> inn-at-the-crossroads` | tier-1 | sources/chapters/affc/affc-brienne-07.md:85
   quote: "The inn's yard was a sea of brown mud that sucked at the hooves of the horses."
   asserted: The ambush takes place in the crossroads inn's yard. LOCATED_AT = event -> place.
   verified_by: (structural, verified=None)

16. `rorge --AGENT_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:265
   quote: "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling."
   asserted: Rorge leads the seven-rider band against the inn, wearing the Hound's helm. AGENT_IN.
   verified_by: (structural, verified=None)

17. `biter --AGENT_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:295
   quote: ". . . and Biter crashed into her, shrieking."
   asserted: Biter falls on Brienne after she kills Rorge, mauling and biting her. AGENT_IN.
   verified_by: (structural, verified=None)

18. `brienne-tarth --AGENT_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:275
   quote: "She stepped out into the rain, Oathkeeper in hand. “Leave her be. If you want to rape someone, try me.”"
   asserted: Brienne initiates combat to protect Willow and the children, killing Rorge. AGENT_IN.
   verified_by: (structural, verified=None)

19. `gendry --AGENT_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-08.md:53
   quote: "He's dead. Gendry shoved a spearpoint through the back of his neck."
   asserted: Gendry kills Biter, resolving the threat that was killing Brienne. AGENT_IN. (The dyadic `gendry KILLS biter` already exists; this is the event-role edge.)
   verified_by: (structural, verified=None)

20. `oathkeeper --WIELDED_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:293
   quote: "Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back, rasping as it scraped along his spine."
   asserted: Oathkeeper is the instrument Brienne uses to kill Rorge at the inn. WIELDED_IN = artifact -> event.
   verified_by: (structural, verified=None)

21. `brienne-tarth --VICTIM_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-07.md:305
   quote: "She saw his teeth, yellow and crooked, filed into points. When they closed on the soft meat of her cheek, she hardly felt it."
   asserted: Brienne is mauled (face bitten, arm broken) by Biter and left near death. VICTIM_IN complements her AGENT_IN — she fights AND is grievously wounded.
   verified_by: (structural, verified=None)

22. `willow-heddle --AGENT_IN--> ambush-at-crossroads-inn` | tier-2 | sources/chapters/affc/affc-brienne-07.md:271
   quote: "The door to the inn banged open. Willow stepped out into the rain, a crossbow in her hands."
   asserted: Willow confronts the raiders with a crossbow, defending the inn and the orphan children. AGENT_IN. Tier-2: she is driven back before loosing.
   verified_by: pending-fresh-verify-s141

23. `hyle-hunt --VICTIM_IN--> ambush-at-crossroads-inn` | tier-1 | sources/chapters/affc/affc-brienne-08.md:279
   quote: "Hyle Hunt had been beaten so badly that his face was swollen almost beyond recognition."
   asserted: Hyle fights in the skirmish and is beaten and captured by the Brotherhood. VICTIM_IN.
   verified_by: (structural, verified=None)

24. `ambush-at-crossroads-inn --CAUSES--> brienne-brought-before-lady-stoneheart` | tier-1 | sources/chapters/affc/affc-brienne-08.md:71
   quote: "“M'lady means for you to answer for your crimes.”"
   asserted: The Brotherhood's capture of the survivors at the inn leads directly to Brienne being hauled before Lady Stoneheart. CAUSES = distinct downstream event; forward-wires the new node into the spine.
   verified_by: pending-fresh-verify-s141

25. `fight-at-the-whispers --LOCATED_AT--> whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:173
   quote: "“The Whispers,” said Nimble Dick. “Have a listen. You can hear the heads.”"
   asserted: The fight occurs at the ruined castle of the Whispers on Crackclaw Point. LOCATED_AT = event -> place.
   verified_by: (structural, verified=None)

26. `brienne-tarth --AGENT_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:319
   quote: "Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur."
   asserted: Brienne kills Pyg, Timeon, and Shagwell at the Whispers. AGENT_IN. (The dyadic KILLS edges already exist; this is the event-role edge.)
   verified_by: (structural, verified=None)

27. `shagwell --AGENT_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:255
   quote: "He swung it hard and low, and one of Crabb's knees exploded in a spray of blood and bone."
   asserted: Shagwell ambushes from the weirwood and kills Nimble Dick. AGENT_IN.
   verified_by: (structural, verified=None)

28. `pyg --AGENT_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:247
   quote: "From the bushes slid a man, so caked with dirt that he looked as if he had sprouted from the earth."
   asserted: Pyg attacks Brienne with a broken sword at the Whispers. AGENT_IN.
   verified_by: (structural, verified=None)

29. `timeon --AGENT_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:273
   quote: "The Dornishman hefted his spear."
   asserted: Timeon, the Dornish Brave Companion, fights Brienne with his spear at the Whispers. AGENT_IN.
   verified_by: (structural, verified=None)

30. `dick-crabb --VICTIM_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:263
   quote: "Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch."
   asserted: Nimble Dick Crabb is killed by Shagwell at the Whispers. VICTIM_IN.
   verified_by: (structural, verified=None)

31. `dick-crabb --KILLED_BY--> shagwell` | tier-1 | sources/chapters/affc/affc-brienne-04.md:263
   quote: "Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face. There was a sickening crunch."
   asserted: Shagwell crushes Crabb's face with the triple morningstar. KILLED_BY = victim -> killer (dyadic).
   verified_by: (structural, verified=None)

32. `podrick-payne --AGENT_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:325
   quote: "Podrick had climbed the fallen wall and was standing amongst the ivy glowering, a fresh rock in his hand. “I told you I could fight!” he shouted down."
   asserted: Podrick stones Shagwell from the wall, stunning him so Brienne can finish him. AGENT_IN (active combatant, not mere witness).
   verified_by: (structural, verified=None)

33. `oathkeeper --WIELDED_IN--> fight-at-the-whispers` | tier-1 | sources/chapters/affc/affc-brienne-04.md:319
   quote: "Oathkeeper was alive in her hands. She had never been so quick. The blade became a grey blur."
   asserted: Brienne wields Oathkeeper to kill Pyg and Timeon at the Whispers. WIELDED_IN = artifact -> event.
   verified_by: (structural, verified=None)

34. `red-wedding --MOTIVATES--> catelyn-stark` | tier-1 | sources/chapters/affc/affc-brienne-08.md:323
   quote: "She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye."
   asserted: The Red Wedding's slaughter is the explicit motive source for all of Lady Stoneheart's vengeance. MOTIVATES = event -> character. Cross-arc seam: the ASOS Red Wedding arc drives the AFFC Brienne arc's antagonist.
   verified_by: pending-fresh-verify-s141

35. `catelyn-stark --MOTIVATES--> lem` | tier-2 | sources/chapters/affc/affc-brienne-08.md:323
   quote: "She wants to feed the crows, like they did at the Red Wedding. Freys and Boltons, aye."
   asserted: Lady Stoneheart's vengeance drives Lem Lemoncloak, her operational enforcer who runs the hangings and speaks her will. MOTIVATES = character -> character. Tier-2: Lem relays her wants; her motivating role is interpretive.
   verified_by: pending-fresh-verify-s141

36. `lem --AGENT_IN--> brienne-brought-before-lady-stoneheart` | tier-1 | sources/chapters/affc/affc-brienne-08.md:333
   quote: "“As you command, m'lady,” said the big man."
   asserted: Lem (the big man in the yellow cloak, now wearing the Hound's helm) carries out Stoneheart's 'Hang them' order. AGENT_IN.
   verified_by: (structural, verified=None)

37. `thoros --PARTICIPATES_IN--> brienne-brought-before-lady-stoneheart` | tier-1 | sources/chapters/affc/affc-brienne-08.md:259
   quote: "Thoros of Myr drew a parchment from his sleeve, and put it down next to the sword. “It bears the boy king's seal and says the bearer is about his business.”"
   asserted: Thoros presents the Lannister letter as evidence against Brienne at the tribunal. PARTICIPATES_IN = non-combat involvement in the event.
   verified_by: (structural, verified=None)

38. `brienne-brought-before-lady-stoneheart --MOTIVATES--> brienne-tarth` | tier-2 | sources/chapters/affc/affc-brienne-08.md:327
   quote: "She says that you must choose. Take the sword and slay the Kingslayer, or be hanged for a betrayer. The sword or the noose, she says. Choose, she says. Choose."
   asserted: The sword-or-noose ultimatum forces Brienne's choice and her screamed word that ends the chapter. MOTIVATES = event -> character; the honest de-dead-end of the previously 0-outgoing tribunal node, WITHOUT asserting the cliffhanger's resolution (no fabricated hanging-death node).
   verified_by: pending-fresh-verify-s141

39. `elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth` | tier-1 | sources/chapters/affc/affc-brienne-06.md:169
   quote: "You are chasing the wrong wolf, my lady. Eddard Stark had two daughters. It was the other one that Sandor Clegane made off with, the younger one."
   asserted: The Elder Brother reveals it was Arya, not Sansa, with the Hound — redirecting Brienne's search. REVEALS_TO = revealer -> recipient.
   verified_by: (structural, verified=None)

40. `elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth` | tier-1 | sources/chapters/affc/affc-brienne-06.md:185
   quote: "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous."
   asserted: The Elder Brother clears Sandor of the Saltpans atrocity, exposing the helm-driven misattribution. REVEALS_TO = revealer -> recipient. (Records the revelation, which happened on-page regardless of the gravedigger-lives subtext — no claim about Sandor's actual death is minted.)
   verified_by: (structural, verified=None)

