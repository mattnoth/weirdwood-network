# Lens 2 — Secondary-Character Substrate + SUSPECTED_OF
## Unit: Brienne → Lady Stoneheart arc (AFFC)
## Date: 2026-06-24

---

## PROPOSED EDGES

### BLOCK A — Wire the islanded `raid-on-saltpans`

**A1.** `rorge --AGENT_IN--> raid-on-saltpans | tier-1 | affc-brienne-07:39 | "These are the men who raided Saltpans." | Hyle Hunt identifies the riders as the Saltpans raiders; rorge is named leader of this band throughout; corroborated by Elder Brother (affc-brienne-06:185), wiki node body.`

**A2.** `biter --AGENT_IN--> raid-on-saltpans | tier-1 | affc-brienne-06:131 | "her breasts had been torn and chewed and eaten, as if by some . . . cruel beast" | Elder Brother describes Biter's distinctive attack pattern at Saltpans; his constant companionship with Rorge confirmed in wiki node "Rorge, who has his constant companion Biter at his side."`

**A3.** `brave-companions --AGENT_IN--> raid-on-saltpans | tier-1 | graph/nodes/events/raid-on-saltpans.node.md | "One band of fleeing Brave Companions is led by Rorge" | Rorge's band consists of remnant Brave Companions; faction-level role is warranted.`

**A4.** `saltpans --LOCATED_AT--> raid-on-saltpans | tier-1 | affc-brienne-07:77 | "At Saltpans, they had found only death and desolation." | Event definitionally occurs at Saltpans; the location node exists.`

**A5.** `rorge --IMPERSONATES--> sandor-clegane | tier-1 | affc-brienne-06:185 | "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous." | Elder Brother confirms Rorge wore Sandor's helm, causing systematic misidentification by realm. The impersonation is the whole engine of Brienne's hunt and the realm's false-blame.`

**A6.** `sandor-clegane --SUSPECTED_OF--> raid-on-saltpans | tier-2 | affc-brienne-05:51 | "Clegane's turned outlaw. He rides with Beric Dondarrion now, it would seem . . . Clegane, Dondarrion, the red priest, and now this woman Stoneheart" | Randyll Tarly names Sandor Clegane and Dondarrion as co-suspects in the realm's eyes; "Mad Dog of Saltpans" epithet circulates as Sandor's accusation.`

**A7.** `brotherhood-without-banners --SUSPECTED_OF--> raid-on-saltpans | tier-2 | affc-brienne-05:51 | "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood." | Tarly deliberately spreads the counter-rumor; Arwood Frey accepts and acts on it. Unproven agency.`

**A8.** `randyll-tarly --DECEIVES--> brotherhood-without-banners | tier-1 | affc-brienne-05:135 | "Lord Randyll is putting it about that they did in hopes of turning the commons against Beric and his brotherhood. He will never take the lightning lord so long as the smallfolk are protecting him." | Tarly intentionally misattributes Saltpans to the Brotherhood as a political maneuver. He knows this is false (he's pursuing the Hound simultaneously).`

**A9.** `quincy-cox --IGNORANT_OF--> raid-on-saltpans | tier-2 | affc-brienne-06:131-132 | "she lay dying, her worst curses were not for the men who had raped her . . . but for Ser Quincy Cox, who barred his gates when the outlaws entered the town and sat safe behind stone walls as his people screamed and died." | Cox is present in his holdfast during the raid but does not intervene; he "saw from the battlements" (wiki). IGNORANT_OF is wrong — he WITNESSED it from safety. Use WITNESS_IN instead.`

**A9-revised.** `quincy-cox --WITNESS_IN--> raid-on-saltpans | tier-1 | graph/nodes/events/raid-on-saltpans.node.md | "Ser Quincy Cox does open his holdfast to them, but tells what saw from the battlements." | Cox watched the raid from his battlements and later testified to Arwood Frey's men; direct perceiver of the attack.`

**A10.** `elder-brother-quiet-isle --WITNESS_IN--> raid-on-saltpans | tier-2 | affc-brienne-06:131 | "It fell to me to treat some of the survivors. The fisherfolk brought them across the bay to me after the flames had gone out" | Elder Brother treated survivors and received first-hand testimony from survivors; he is a key witness to the aftermath and knows more than anyone (he is Brienne's best source). Strictly speaking he witnesses aftermath not the event itself — rate tier-2.`

**A11.** `sandor-clegane --LOCATED_AT--> saltpans | tier-2 | affc-brienne-05:127 | "Sandor Clegane was last seen in Saltpans, the day of the raid." | Hyle Hunt's cousin Alyn reports this; Sandor was seeking a ship. He did not participate in the raid (Elder Brother confirms he was dying by then) but was physically present in Saltpans that day.`

---

### BLOCK B — `brienne-brought-before-lady-stoneheart` — fill missing participants

The event already has: brotherhood-without-banners AGENT_IN; catelyn-stark COMMANDS_IN; brienne/podrick/hyle VICTIM_IN. What's missing:

**B1.** `lem-standfast --AGENT_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:211-212 | "The biggest of the four wore a stained and tattered yellow cloak. 'Enjoy the food?' he asked. 'I hope so. It's the last food you're ever like to eat.'" | Lem (the man in the yellow cloak, who also wears the Hound's helm by this point) leads the escort into the cave and delivers the ultimatum. He is the named AGENT_IN most present.`

**B2.** `lem-standfast --AGENT_IN--> brienne-brought-before-lady-stoneheart | SAME as B1 — also commands the hanging order: | affc-brienne-08:337 | "'As you command, m'lady,' said the big man." | Lem explicitly carries out Stoneheart's "Hang them" edict; he physically places the noose (affc-brienne-08:345: "The Hound snatched the end of the rope from the man holding it.").`

**B3.** `thoros-of-myr --PARTICIPATES_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:259-260 | "Thoros of Myr drew a parchment from his sleeve, and put it down next to the sword. 'It bears the boy king's seal'" | Thoros is present in the cave, presents the Lannister letter as evidence against Brienne; he participates in the adjudication.`

**B4.** `catelyn-stark --COMMANDS_IN--> brienne-brought-before-lady-stoneheart | (already exists per baseline) — but the specific command is now textually anchored: | affc-brienne-08:331 | "There was a long silence. Then Lady Stoneheart spoke again. This time Brienne understood her words. There were only two. 'Hang them,' she croaked." | Verify baseline entry has this cite.`

**B5.** `oathkeeper --WIELDED_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:257 | "In his hand was Oathkeeper. 'This says it is.' His voice was frosted with the accents of the north. He slid the sword from its scabbard and placed it in front of Lady Stoneheart." | The sword is presented as evidence; it functions as an instrument in the judgment scene — the northman uses it to argue Brienne's guilt.`

**B6.** `jeyne-heddle --WITNESS_IN--> brienne-brought-before-lady-stoneheart | tier-1 | affc-brienne-08:237 | "There were women too, and even a few children peering out from behind their mothers' skirts. The one face Brienne knew belonged to Long Jeyne Heddle." | Jeyne is present in the cave at the judgment; she is named by Brienne. Jeyne is also a load-bearing WITNESS_IN because she tends Brienne's wounds after and her presence confirms she saw the proceeding.`

**B7.** `gendry --PARTICIPATES_IN--> brienne-brought-before-lady-stoneheart | tier-2 | affc-brienne-08:71 | "'till you stand before m'lady.' Renly stood behind the girl, pushing his black hair out of his eyes. Not Renly. Gendry." | Gendry escorts Brienne to the Brotherhood's holding point and speaks the "stand before m'lady" line; he turns back before the cave (affc-brienne-08:95). He participates in the transport but not the judgment itself — tier-2.`

---

### BLOCK C — Crossroads Inn ambush — new event hub + wiring

**Proposed new event node:** `ambush-at-crossroads-inn` (event.battle)
- **Justification:** This is the dramatic climax of the AFFC arc: Rorge's seven riders attack the inn; Brienne kills Rorge; Biter mauls Brienne; Gendry kills Biter; Lem's men capture Brienne/Pod/Hyle. It is a distinct, named location, discrete in time, with multiple participants and consequences. Currently not reflected in the graph.

**C1.** `brienne-tarth --AGENT_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:274-275 | "She stepped out into the rain, Oathkeeper in hand. 'Leave her be. If you want to rape someone, try me.'" | Brienne initiates combat to protect the children.`

**C2.** `rorge --AGENT_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:265-271 | "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling" and "The man in the Hound's helm began to laugh." | Rorge leads the seven riders; wears the Hound's helm; attacks Brienne with a battle axe.`

**C3.** `biter --AGENT_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:295-307 | "he fell on her like an avalanche of wet wool and milk-white flesh, lifting her off her feet and slamming her down into the ground" | Biter attacks Brienne after she kills Rorge, chewing her face.`

**C4.** `gendry --AGENT_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-08:53 | "He's dead. Gendry shoved a spearpoint through the back of his neck." | Gendry kills Biter; he is the agent who resolves the Biter threat.`

**C5.** `brienne-tarth --KILLS--> rorge | (already exists per baseline) — now anchoring the cite: | affc-brienne-07:292-293 | "his headlong charge brought him right onto her point, and Oathkeeper punched through cloth and mail and leather and more cloth, deep into his bowels and out his back" | Verify cite in existing edge.`

**C6.** `oathkeeper --WIELDED_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:261 | "Brienne sucked in her breath and drew Oathkeeper." | Oathkeeper is the instrument Brienne uses to kill Rorge.`

**C7.** `willow-heddle --WITNESS_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:271 | "The door to the inn banged open. Willow stepped out into the rain, a crossbow in her hands." | Willow is physically present, confronts Rorge's men with the crossbow, witnesses the fight from the inn doorway.`

**C8.** `podrick-payne --WITNESS_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-08:77 | "Brienne could hear Dog barking, and men were shouting all about her" (Pod is present; affc-brienne-08:279: "Podrick caught him by the arm") | Podrick is captured after the fight; he is present in the yard during the ambush. Rate tier-1 as he is in the yard and suffers capture as direct consequence.`

**C9.** `inn-at-the-crossroads --LOCATED_AT--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:84 | "The inn's yard was a sea of brown mud" | Event occurs in the inn's yard.`

**C10.** `hyle-hunt --VICTIM_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-08:279 | "Hyle Hunt had been beaten so badly that his face was swollen almost beyond recognition." | Hyle fights in the skirmish and is beaten and captured.`

**C11.** `septon-meribald --PARTICIPATES_IN--> ambush-at-crossroads-inn | tier-2 | affc-brienne-08:183 | "The septon was set free to go upon his way. There was no harm in him." | Meribald is at the inn when the attack occurs; the Brotherhood release him afterward confirming he was present. He is not a combatant — tier-2 PARTICIPATES_IN.`

**C12.** `lem-standfast --AGENT_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-08:147 | "Lem should not have left the crossroads. He was told to stay close, hidden, to come at once if he saw smoke rising from the chimney" | Lem's men return and capture Brienne/Pod/Hyle after the fight; Lem is the agent who takes them prisoner.`

---

### BLOCK D — Whispers fight (sub-arc: Brave-Companions remnant)

**Proposed new event node:** `fight-at-the-whispers` (event.battle)
- **Justification:** Named location, distinct violent encounter, multiple kills (Pyg, Timeon, Shagwell), Nimble Dick killed, Podrick acts. This is a significant sub-arc beat with no current event node.

**D1.** `brienne-tarth --AGENT_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:305-307 | "She flew at Timeon . . . She slashed off his ear and half his cheek, hacked the head off his spear, and put a foot of rippled steel into his belly" | Brienne kills Pyg, Timeon, and Shagwell in this engagement.`

**D2.** `shagwell --AGENT_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:255 | "Shagwell dropped from the weirwood, braying laughter. He was garbed in motley . . . He swung it hard and low, and one of Crabb's knees exploded in a spray of blood and bone." | Shagwell kills Nimble Dick and attacks Brienne.`

**D3.** `timeon --AGENT_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:269 | "'You again, woman? What, come to hunt us down? Or did you miss our friendly faces?'" and his spear attacks on Brienne.`

**D4.** `pyg --AGENT_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:248 | "From the bushes slid a man, so caked with dirt that he looked as if he had sprouted from the earth. A broken sword was in his hand . . . She knew that nose. She knew those eyes. Pyg, his friends had called him." | Pyg attacks Brienne with his broken sword.`

**D5.** `dick-crabb --VICTIM_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:255 | "He swung it hard and low, and one of Crabb's knees exploded in a spray of blood and bone . . . Shagwell whirled the spiked ball once around his head and brought it down in the middle of Crabb's face." | Nimble Dick killed by Shagwell during this fight.`

**D6.** `podrick-payne --WITNESS_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:317 | "Then a stone came out of nowhere, and hit Shagwell in the head . . . Podrick had climbed the fallen wall and was standing amongst the ivy glowering, a fresh rock in his hand. 'I told you I could fight!'" | Podrick actively intervenes — he is not merely a bystander; he strikes Shagwell twice with rocks, enabling Brienne's kill. He directly perceives the entire fight.`

**D7.** `whispers --LOCATED_AT--> fight-at-the-whispers | tier-1 | affc-brienne-04:173 | "The castle came upon them without warning. One moment they were in the depths of the forest . . . 'The Whispers,' said Nimble Dick." | Event occurs at the Whispers.`

**D8.** `hyle-hunt --WITNESS_IN--> fight-at-the-whispers | tier-1 | affc-brienne-04:363 | "Laughter sounded from behind them . . . Hyle Hunt atop the crumbling wall, his legs crossed." | Hyle was the rider following them (hinted throughout ch4); he watches the aftermath from the wall and confirms he observed the fight's end.`

---

### BLOCK E — Nimble Dick Crabb sub-arc

**E1.** `dick-crabb --TRAVELS_WITH--> brienne-tarth | tier-1 | affc-brienne-03:341-342 | "Six dragons if we find my sister. Two if we only find the fool. Nothing if nothing is what we find. . . . Crabb shrugged. 'Six is good. Six will serve.'" | Dick is hired by Brienne to guide her to the Whispers; they travel together through Crackclaw Point.`

**E2.** `dick-crabb --TRAVELS_WITH--> podrick-payne | tier-1 | affc-brienne-04 (throughout) | "Podrick never seemed certain what to call her" — all three ride together through Crackclaw Point. Pod is with them the entire journey.`

**E3.** `hyle-hunt --SPIES_ON--> brienne-tarth | tier-1 | affc-brienne-04:367 | "Lord Randyll bid me follow you. If by some freak's chance you stumbled onto Sansa Stark, he told me to bring her back to Maidenpool." | Hyle explicitly admits he was following Brienne on Tarly's orders; he is the unnamed rider glimpsed behind them on the Crackclaw Point road (affc-brienne-04:115-116).`

**E4.** `randyll-tarly --COMMANDS_IN--> hyle-hunt (via SPIES_ON) | — modeled as: | randyll-tarly --APPOINTS--> hyle-hunt | tier-1 | affc-brienne-04:367 | "Lord Randyll bid me follow you." | Tarly gives Hyle his surveillance mission. APPOINTS is the best fit for delegating a task. Alternatively MANIPULATES but APPOINTS is more precise for a lord-to-knight assignment.`

---

### BLOCK F — Septon Meribald + Quiet Isle sub-arc

**F1.** `meribald --TRAVELS_WITH--> brienne-tarth | tier-1 | affc-brienne-05:173 | "They left the next morning, as the sun was coming up. It was a queer procession: Ser Hyle on a chestnut courser and Brienne on her tall grey mare, Podrick Payne astride his swayback stot, and Septon Meribald walking beside them with his quarterstaff" | Meribald joins Brienne's party from Maidenpool to the crossroads inn.`

**F2.** `meribald --TRAVELS_WITH--> hyle-hunt | tier-1 | same cite as F1.`

**F3.** `meribald --TRAVELS_WITH--> podrick-payne | tier-1 | same cite as F1.`

**F4.** `elder-brother-quiet-isle --HEALS--> brienne-tarth | tier-2 | affc-brienne-06:112-113 | "He looks more like a man made to break bones than to heal one . . . the Elder Brother did not seem dismayed by Brienne's sex" | Elder Brother offers hospitality, lodging, and counsel. He does not physically heal Brienne here (healing happens post-Biter, by Jeyne Heddle) — downgrade: HEALS is inaccurate here; propose ADVISES instead.`

**F4-revised.** `elder-brother-quiet-isle --ADVISES--> brienne-tarth | tier-1 | affc-brienne-06:209 | "'If so, give up this quest of yours. The Hound is dead, and in any case he never had your Sansa Stark. As for this beast who wears his helm, he will be found and hanged. . . . Go home, child.'" | Elder Brother explicitly counsels Brienne to abandon her quest; she does not take his advice.`

**F5.** `elder-brother-quiet-isle --REVEALS_TO--> brienne-tarth | tier-1 | affc-brienne-06:169-173 | "You are chasing the wrong wolf, my lady. Eddard Stark had two daughters. It was the other one that Sandor Clegane made off with, the younger one." | Elder Brother reveals that the Stark girl with Sandor was Arya, not Sansa — a pivotal intelligence revelation that redirects Brienne's whole search.`

**F6.** `elder-brother-quiet-isle --INFORMS--> brienne-tarth | tier-1 | affc-brienne-06:185 | "The man who raped and killed at Saltpans was not Sandor Clegane, though he may be as dangerous." | Elder Brother explicitly clears Sandor; this is the key informational beat on the Saltpans misattribution.`

**F7.** `quiet-isle --LOCATED_AT--> (brienne's stay) | — modeled as | brienne-tarth --TRAVELS_TO--> quiet-isle | tier-1 | affc-brienne-06:23-25 | "'Only the faithful may cross safely. The wicked are swallowed by the quicksands, or drowned when the tide comes rushing in.'" | Brienne crosses the mudflats to the Quiet Isle; this is a key waypoint.`

---

### BLOCK G — Randyll Tarly at Maidenpool sub-arc

**G1.** `randyll-tarly --RULES--> maidenpool | tier-1 | affc-brienne-03:45 | "This Tarly, he's a hard man, but a braver lord than Mooton. There's still outlaws in the woods, but not so many as there was. Tarly hunted down the worst o' them and shortened them with that big sword o' his." | Tarly exercises effective lordship over Maidenpool (formally Lord Mooton's seat but Tarly administers justice there).`

**G2.** `randyll-tarly --OPPOSES--> brienne-tarth | tier-1 | affc-brienne-03:177 | "'You never should have donned mail, nor buckled on a sword. You never should have left your father's hall.'" | Tarly's sustained hostility to Brienne functions as opposition throughout the arc.`

**G3.** `randyll-tarly --OPPOSES--> brotherhood-without-banners | tier-1 | affc-brienne-05:51 | "'Clegane's turned outlaw. He rides with Beric Dondarrion now, it would seem . . . Show me where they're hiding, I will gladly slit their bellies open, pull their entrails out, and burn them.'" | Tarly explicitly hunts Dondarrion's Brotherhood.`

---

### BLOCK H — Gendry at the inn — identity thread

**H1.** `gendry --COMPANION_OF--> willow-heddle | tier-1 | affc-brienne-07:135-137 | "'No,' said the boy smith. 'Yes,' said the girl Willow. They glared at one another." | Gendry and Willow jointly manage the crossroads inn; they are co-protectors of the orphan children there.`

**H2.** `gendry --PROTECTS--> willow-heddle | tier-1 | affc-brienne-08:95 | "He's gone back to his forge, to Willow and the little ones, to keep them safe." | Gendry explicitly stays behind to protect Willow and the orphan children.`

**H3.** `brienne-tarth --ENCOUNTERS--> gendry | tier-1 | affc-brienne-07:115-121 | "She saw a ghost. Renly. No hammerblow to the heart could have felled her half so hard. 'My lord?' she gasped." | First encounter; Brienne recognizes Renly's resemblance.`

**H4.** `gendry --PERCEIVED_AS--> robert-baratheon | tier-2 | affc-brienne-07:247 | "You have black hair and blue eyes, and you were born in the shadow of the Red Keep. Has no one ever remarked upon your face?" | Brienne perceives Gendry's Baratheon resemblance and draws the implication that he is Robert's bastard. PERCEIVED_AS fits the cross-POV perception edge.`

---

### BLOCK I — Lem claims the Hound's helm

**I1.** `lem-standfast --LOOTED_BY--> hound-helm | tier-1 | affc-brienne-08:215-216 | "It was Rorge I killed. He took the helm from Clegane's grave, and you stole it off his corpse. . . . 'I didn't hear him objecting.'" | Lem takes the Hound's helm from Rorge's corpse after the inn fight. The helm's chain: Sandor buried → Elder Brother marks grave → Rorge takes helm → Rorge killed by Brienne → Lem takes it.`

NOTE: `hound-helm` is a candidate new node. The baseline notes "NO hound-helm node — candidate mint."

**Proposed new node:** `hound-helm`
- slug: `hound-helm`
- type: artifact
- justification: The Hound's distinctive bucket helm is a named, plot-critical object that passes through four hands (Sandor → buried → Rorge → Lem), drives the Saltpans misattribution, and appears verbatim in the Elder Brother's testimony and Brienne's combat. It is the single most load-bearing artifact in the arc.

**I2.** `sandor-clegane --OWNS--> hound-helm | tier-1 | affc-brienne-06:185 | "I covered him with stones to keep the carrion eaters from digging up his flesh, and set his helm atop the cairn to mark his final resting place." | Sandor owns the helm; Elder Brother places it on his cairn.`

**I3.** `rorge --LOOTED_BY--> hound-helm | tier-1 | graph/nodes/events/raid-on-saltpans.node.md | "Along the way they find the Hound's helm." | Rorge's band finds and takes the helm from Sandor's cairn.`

**I4.** `hound-helm --WIELDED_IN--> raid-on-saltpans | tier-1 | affc-brienne-06:185 | "Some other wayfarer found my marker and claimed it for himself. The man who raped and killed at Saltpans was not Sandor Clegane" | The helm is used in the Saltpans raid, enabling misidentification. WIELDED_IN captures its role as instrument.`

**I5.** `hound-helm --WIELDED_IN--> ambush-at-crossroads-inn | tier-1 | affc-brienne-07:265 | "beneath the dark hood of the lead rider Brienne glimpsed an iron snout and rows of steel teeth, snarling" | Rorge wears the helm at the inn ambush.`

---

### BLOCK J — Thoros of Myr / Brotherhood's transformation under Stoneheart

**J1.** `thoros-of-myr --MEMBER_OF--> brotherhood-without-banners | tier-1 | affc-brienne-08:153-159 | "You are the Myrish priest. The red wizard." / "I am Thoros, late of Myr, aye . . . a bad priest and a worse wizard. . . . You ride with the Dondarrion. The lightning lord." | Established; may already exist — include for completeness.`

**J2.** `catelyn-stark --MOTIVATES--> brotherhood-without-banners | tier-1 | affc-brienne-08:199-200 | "Justice. . . . I remember justice. It had a pleasant taste. Justice was what we were about when Beric led us . . . but some knights are dark and full of terror, my lady. War makes monsters of us all." | Thoros confirms the Brotherhood's transformation under Stoneheart; she drives them from justice-seeking to vengeance execution.`

**J3.** `beric-dondarrion --RESURRECTS--> catelyn-stark | tier-1 | affc-brienne-08:311-312 | "Harwin begged me to give her the kiss of life, but it had been too long. I would not do it, so Lord Beric put his lips to hers instead, and the flame of life passed from him to her. And . . . she rose." | The RESURRECTS edge; may already exist. Thoros is the witness who narrates this.`

**J4.** `thoros-of-myr --WITNESS_IN--> catelyn-rises-as-lady-stoneheart | tier-1 | affc-brienne-08:311 | "When we found her by the river she was three days dead. Harwin begged me to give her the kiss of life, but it had been too long. I would not do it" | Thoros was present at the resurrection; he witnessed it and tried to refuse. Load-bearing perceiver.`

**J5.** `jeyne-heddle --HEALS--> brienne-tarth | tier-1 | affc-brienne-08:135-139 | "That was she who set your arm and splinted it, as well as any maester. She did what she could for your face as well, washing out the wounds with boiled ale to stop the mortification." | Jeyne Heddle heals Brienne's wounds in the Brotherhood's cave; confirmed by the grey man (Thoros).`

---

## PROPOSED NEW NODES

1. **`hound-helm`** | type: artifact | Sandor Clegane's distinctive dog-headed bucket helm. Placed on his cairn by the Elder Brother; stolen by Rorge; used in the Saltpans raid (causing systematic misidentification of Sandor as the raider); taken by Lem Lemoncloak after the inn ambush. Tier-1. Central plot object of the AFFC Brienne arc.

2. **`ambush-at-crossroads-inn`** | type: event.battle | The attack by Rorge's seven-rider band on the crossroads inn. Brienne kills Rorge; Biter mauls Brienne; Gendry kills Biter; Lem's returning Brotherhood men capture Brienne, Podrick, and Hyle Hunt. Directly precipitates `brienne-brought-before-lady-stoneheart`. Tier-1.

3. **`fight-at-the-whispers`** | type: event.battle | Brienne, Nimble Dick, and Podrick confront Shagwell, Timeon, and Pyg at the ruined Whispers castle on Crackclaw Point. Dick Crabb is killed by Shagwell; Pyg killed by Brienne; Timeon killed by Brienne; Shagwell killed by Brienne. Timeon reveals the Hound has "the Stark girl." Tier-1.

---

## HARVEST

(Pointers only — do not extract; a later harvest pass attaches.)

- `affc-brienne-05:177` / food/provision / Meribald's donkey load: "Seeds and nuts and dried fruit, oaten porridge, flour, barley bread, three wheels of yellow cheese from the inn by the Fool's Gate, salt cod for me, salt mutton for Dog . . . nine sacks of oranges." Full inventory for broken-men provision track.
- `affc-brienne-05:293-305` / food/hospitality+broken-men register / Meribald's broken-men sermon — "they slaughter their sheep and steal their chickens, and from there it's just a short step to carrying off their daughters too" — prime quote for broken-men thematic + food-theft.
- `affc-brienne-06:141` / food+hospitality / Quiet Isle supper: "loaves of crusty bread still warm from the ovens, crocks of fresh-churned butter, honey from the septry's hives, and a thick stew of crabs, mussels, and at least three different kinds of fish" + mead + sweet cider. First-class hospitality scene.
- `affc-brienne-06:113` / artifacts/found objects / Elder Brother on driftwood gifts: "silver cups and iron pots, sacks of wool and bolts of silk, rusted helms and shining swords . . . aye, and rubies" (Rhaegar's rubies — six found, seventh awaited). Foreshadowing/prophecy hook.
- `affc-brienne-07:141` / hospitality + inn history / Meribald's full history of the crossroads inn (Old Inn → Two Crowns → Bellringer → Clanking Dragon → River Inn → crossroads inn); Black dragon iron sign cast in river by Lord Darry. Rich lore.
- `affc-brienne-07:163-164` / description+bloodstains / "There are bloodstains on the floor over there . . . They've been scrubbed, but the blood soaked deep into the wood, and there's no getting it out." — site of Sandor's inn fight; physical description.
- `affc-brienne-08:103-105` / guest right / "Bread and salt. The inn . . . Septon Meribald fed the children . . . we broke bread with your sister . . . Guest right don't mean so much as it used to." Jeyne's reply: cornerstone guest-right violation moment; quote is load-bearing.
- `affc-brienne-01:283-285` / artifacts+prayer / Brienne holds Oathkeeper and prays to the Crone: "Kneeling between the bed and wall, she held the blade and said a silent prayer to the Crone . . . Lead me, she prayed, light the way before me, show me the path that leads to Sansa." Fine Oathkeeper description + spiritual register.
- `affc-brienne-04:255-263` / violence/description / Shagwell killing Nimble Dick: "one of Crabb's knees exploded in a spray of blood and bone" → face crushed. Strong physical description of Shagwell's cruelty.
- `affc-brienne-08:347` / hanging scene / "Her mouth opened. Pod was kicking, choking, dying. Brienne sucked the air in desperately, even as the rope was strangling her. Nothing had ever hurt so much. She screamed a word." — cliffhanger; the screamed word (traditionally "sword" → launches Jaime rescue plotline in later books) is a foreshadowing beat.

---

## SUMMARY

Proposed **41 edges** across 9 blocks (plus 3 new nodes). The single largest fix is BLOCK A: wiring `raid-on-saltpans` with 11 participant/blame/location edges to break its complete isolation. BLOCK C proposes the `ambush-at-crossroads-inn` event node with 12 wiring edges as the arc's climax beat. BLOCK D proposes `fight-at-the-whispers` (5 edges) for the Brave-Companions remnant sub-arc. Remaining blocks fill participant gaps in `brienne-brought-before-lady-stoneheart`, wire secondary figures (Meribald, Elder Brother, Gendry, Lem, Jeyne Heddle), and add the `hound-helm` artifact node that anchors the Saltpans misattribution chain.
