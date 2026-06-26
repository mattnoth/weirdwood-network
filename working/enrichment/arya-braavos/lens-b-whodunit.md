# Lens B — Whodunit / Revelation / Unproven Agency
## Arya Stark's Braavos / House of Black and White Arc

_Chapters covered: asos-arya-13, affc-arya-01, affc-arya-02, affc-cat-of-the-canals-01, adwd-the-blind-girl-01, adwd-the-ugly-little-girl-01_

---

## IDENTITY-LAYER MODEL SUMMARY (6–10 lines)

**ALIAS_OF arya-stark** (maintained identities, Arya inhabits them as a cover self, no literal face-swap):
- `salty` — shipboard name given by crew, accepted and inhabited through the Braavos crossing (AFFC Arya I). Arya consciously plays the role ("Salty was from Saltpans"). Tier 1.
- `cat-of-the-canals` — full constructed persona with backstory (orphan from King's Landing, oarmaster's daughter), assigned by the kindly man; Arya lives as Cat for months in Brusco's household. The text explicitly names her inner self as Cat during this period. Parallel to Sansa-as-Alayne-Stone. Tier 1.
- `no-one` — the contested identity the FM demand; Arya performs it inside the HoBaW but the text makes clear her heart of hearts resists it throughout. Functionally a DISGUISED_AS or aspirational alias, never truly assumed. Best modeled as ALIAS_OF with a note flag. Tier 1.

**DISGUISED_AS** (costume/mummer's-art faces layered on, not literal skin-wearing):
- `blind-beth` — begging persona assembled by the waif (shaved head, pox scars, mummer's mole); Arya deploys Beth while physically blind; a mummer's-art disguise, not a Faceless-Men skin. Tier 1.
- `ugly-little-girl` — a **literal worn skin** (a dead girl's face, physically applied in the sanctum with a blade); she experiences the dead woman's trauma as the face bonds. This is the one canonical instance of actual face-wearing in the arc. Tier 1.

**Key distinction:** Salty / Cat / No-one / Blind-Beth = performed personas (ALIAS_OF or DISGUISED_AS via costume/mummery). Ugly-little-girl = a worn skin (DISGUISED_AS with sub-kind = worn-face). The skins in the sanctum are physically flayed from the dead; the ugly face is the first one Arya actually wears.

---

## NEW NODES

### N1 — `the-insurance-underwriter` (character)
- Type: character
- Description: Unnamed elderly Braavosi maritime insurance binder-writer operating out of a soup shop near the Purple Harbor. Targeted for assassination after an unnamed petitioner prayed to the Many-Faced God and paid the FM's price. Killed when Arya (as Cat/ugly-girl) engineered a Westerosi gold dragon coin into his purse, which he then paid to his own murderer.
- Source: adwd-the-ugly-little-girl-01, lines 89–261

### N2 — `salty` (alias node)
- Type: alias / persona
- Description: Arya's cover identity on the Titan's Daughter, named by the crew after Saltpans. No constructed backstory beyond the name; she adopts it passively.
- Source: affc-arya-01, line 25

### N3 — `cat-of-the-canals` (alias node)
- Type: alias / persona
- Description: Arya's full constructed identity in Braavos — orphan girl from King's Landing, oarmaster's daughter, sent off ship in Braavos. Assigned by the kindly man. Used for months selling shellfish at Ragman's Harbor.
- Source: affc-arya-02, lines 325–333; affc-cat-of-the-canals-01

### N4 — `blind-beth` (alias node)
- Type: alias / persona
- Description: Arya's begging persona during her blind period: shaved head, pox scars applied by the waif, mummer's mole. A mummer's-art disguise, not a literal skin.
- Source: adwd-the-blind-girl-01, lines 17, 151–155

### N5 — `ugly-little-girl-face` (alias node)
- Type: alias / persona
- Description: The literal skin of a dead woman, physically applied by the kindly man in the sanctum. The girl had been beaten by her father; wearing her face, Arya experienced her residual trauma. Given to Arya to commit her first FM kill without exposing Cat or Beth.
- Source: adwd-the-ugly-little-girl-01, lines 171–213

### N6 — `the-lying-game` (event)
- Type: event
- Description: Daily exercise between Arya and the waif (later including the kindly man) in which each asks questions and the other may answer truly or falsely; the questioner must identify truth from lie. Primary training mechanism for FM lie-detection discipline. Escalated to tactile reading during Arya's blind period.
- Source: affc-arya-02, lines 229–235; adwd-the-blind-girl-01, line 95

---

## EDGES

### IDENTITY LAYERS

**E1**
`(salty, ALIAS_OF, arya-stark)` | Tier 1 | affc-arya-01:25 | "They called her Salty, since she'd come aboard at Saltpans, near the mouth of the Trident. It was as good a name as any, she supposed."
_Rationale:_ Passively assumed cover name, no face-swap or backstory; Arya inhabits it as herself-in-disguise. ALIAS_OF is right (she is not pretending to be a specific other person, just unnamed).

**E2**
`(cat-of-the-canals, ALIAS_OF, arya-stark)` | Tier 1 | affc-arya-02:325–327 | "She hesitated. 'I could be Cat?' 'Cat.' He considered. 'Yes. Braavos is full of cats. One more will not be noticed. You are Cat, an orphan of . . .'"
_Rationale:_ Full constructed persona with assigned backstory. Exactly parallel to `sansa-adopts-the-alayne-stone-identity` — kindly man explicitly names and builds the cover as a functional shell identity. Should be modeled the same way.

**E3**
`(blind-beth, ALIAS_OF, arya-stark)` | Tier 1 | adwd-the-blind-girl-01:31 | "Beth. She had known a Beth once, back at Winterfell when she was Arya Stark. Maybe that was why she'd picked the name. Or maybe it was just because it went so well with blind."
_Rationale:_ Arya-chosen name; paired with waif-applied mummer's-art disguise (pox scars, shaved head, mole). Performance identity, not literal skin.

**E4**
`(arya-stark, DISGUISED_AS, blind-beth)` | Tier 1 | adwd-the-blind-girl-01:151 | "the blind girl tied a strip of rag around her head to hide her useless eyes, found her begging bowl, and asked the waif to help her don Beth's face. The waif had shaved her head for her when they took her eyes; a mummer's cut, she called it . . . Instead she gave her pox scars and a mummer's mole on one cheek with a dark hair growing from it."
_Rationale:_ Physical disguise applied by the waif — this is the active donning of the Beth costume.

**E5**
`(arya-stark, DISGUISED_AS, ugly-little-girl-face)` | Tier 1 | adwd-the-ugly-little-girl-01:199–201 | "Then came a tug and a soft rustling as the new face was pulled down over the old. The leather scraped across her brow, dry and stiff, but as her blood soaked into it, it softened and turned supple. . . . a terrible sense of fear filled her, and she heard a noise, a hideous crunching noise, accompanied by blinding pain. A face floated in front of her, fat, bearded, brutal, his mouth twisted with rage."
_Rationale:_ Literal worn skin (physically applied from the sanctum's face-wall). DISGUISED_AS is the closest vocabulary fit; sub-kind = worn-face. The dead woman's trauma bleeds through as Arya wears it — that is the distinction from a mummer's disguise.

NEEDS_VOCAB: The gap between DISGUISED_AS-via-costume (Blind-Beth) and DISGUISED_AS-via-literal-skin (ugly-little-girl) may warrant a sub-type flag in the edge record, but the vocab doesn't distinguish them. Flag this for the next vocab review.

---

### REVEALS_TO EDGES

**E6**
`(kindly-man, REVEALS_TO, arya-stark)` | Tier 1 | affc-arya-02:173 | "The tale of our beginnings. If you would be one of us, you had best know who we are and how we came to be. Men may whisper of the Faceless Men of Braavos, but we are older than the Secret City. Before the Titan rose, before the Unmasking of Uthero, before the Founding, we were."
_Rationale:_ Kindly man reveals the FM origin story to Arya — the Valyrian slave mines, the first gift, the founding of the order. This is a gated revelation: he gives it only after she surrenders her treasures and commits to the path.
_Note: load-bearing quote to the founding event; if an event node for `faceless-men-founding` exists or is created, chain this as evidence._

**E7**
`(waif, REVEALS_TO, arya-stark)` | Tier 1 | affc-cat-of-the-canals-01:195 | "I was born the only child of an ancient House, my noble father's heir. . . . When I was six my father wed again. His new wife treated me kindly until she gave birth to a daughter of her own. Then it was her wish that I should die, so her own blood might inherit my father's wealth. . . . Instead, she thought to poison me herself. It left me as you see me now, but I did not die."
_Rationale:_ Waif reveals her own backstory — poisoning by stepmother, consequent dwarfed growth, delivery to HoBaW. The revelation is a teaching moment (truth/lie parsing) and establishes what the FM's "gift" cost her family. Tier 1 because the waif herself confirms substantial truth ("There is truth in it").

**E8**
`(kindly-man, REVEALS_TO, arya-stark)` | Tier 1 | adwd-the-ugly-little-girl-01:125–133 | "He is writing each a binder. If their ships are lost in a storm or taken by pirates, he promises to pay them for the value of the vessel and all its contents. . . . It is one thing to write such a binder, though, and another to make good on it."
_Rationale:_ Kindly man explains the insurance underwriter's profession, which enables Arya to understand why someone would pray for his death. This is the intelligence briefing that contextualizes the kill assignment.

---

### INFORMS EDGES

**E9**
`(arya-stark, INFORMS, kindly-man)` | Tier 1 | affc-cat-of-the-canals-01:35–45 | "'Learn three new things before you come back to us,' the kindly man had commanded Cat, when he sent her forth into the city. She always did. . . . 'What do you know that you did not know when you left us?' he would always ask her."
_Rationale:_ Arya-as-Cat is functioning as a systematic intelligence gatherer for the FM; the kindly man debriefs her on every return. The three-things obligation is a structured INFORMS relationship: she is their eyes in the harbor.

**E10**
`(arya-stark, INFORMS, kindly-man)` | Tier 1 | adwd-the-blind-girl-01:183–185 | "I know why the Sealord seized the Goodheart. She was carrying slaves. Hundreds of slaves, women and children, roped together in her hold. . . . I know where the slaves came from. They were wildlings from Westeros, from a place called Hardhome."
_Rationale:_ Blind-Beth's begging at Pynto's yields political intelligence (slave ship seizure, Hardhome wildlings) that Arya reports to the kindly man. The FM are clearly using her as a harbor intelligence asset. Most specific of the three-things instances — load-bearing content.

**E11**
`(arya-stark, SPIES_ON, faceless-men)` | Tier 2 | affc-arya-02:245–249 | "She was allowed as many blankets as she wished. . . . 'When you are not pouring, you must stand as still as if you had been carved of stone,' the kindly man told her. 'It would be best if you were blind and deaf as well. You may hear things, but you must let them pass in one ear and out the other. Do not listen.' Arya heard much and more that night, but almost all of it was in the tongue of Braavos."
_Rationale:_ Arya observes the FM priests' inner meeting while serving as cup-bearer — a soft SPIES_ON: she is not authorized to listen but absorbs what she can. Tier 2 because her comprehension is limited and she hides the warg-vision from the kindly man.
_Alternative read: she is a WITNESS_IN the gathering; SPIES_ON captures the covert observation intent better. Proposer prefers SPIES_ON._

---

### DECEIVES EDGES (Lying-Game / Lie-Detection)

**E12**
`(kindly-man, DECEIVES, arya-stark)` | Tier 1 | affc-arya-02:17 | "You lie. All men lie when they are afraid. Some tell many lies, some but a few. Some have only one great lie they tell so often that they almost come to believe it . . . though some small part of them will always know that it is still a lie, and that will show upon their faces."
_Rationale:_ Kindly man sees through Arya's denial immediately and articulates the FM doctrine of lie-detection. This is the load-bearing opener of the deception dynamic — he establishes he can read her perfectly.
_Edge direction note: DECEIVES = the subject tries to deceive the object and fails here. We want the reverse: kindly-man SEES THROUGH arya-stark's DECEIVES attempts. Vocab doesn't have a see-through edge; DECEIVES (arya→kindly-man, failed) is the better framing. See E13._

**E13**
`(arya-stark, DECEIVES, kindly-man)` | Tier 1 | affc-arya-02:15–17 | "'Child,' said the kindly man one day, 'what are those names you whisper of a night?' 'I don't whisper any names,' she said. 'You lie,' he said."
_Rationale:_ Arya attempts to conceal her kill-list (= her true self/purpose) with a flat denial; he sees through it immediately. This edge represents the recurring, load-bearing deception pattern: Arya lies → kindly man (or waif) exposes it. Tier 1 because the text explicitly confirms the lie and the exposure. Mark as `failed_deception = true` if schema allows.

**E14**
`(waif, DECEIVES, arya-stark)` | Tier 1 | affc-arya-02:233–237 | "The waif showed ten fingers. Then ten again, and yet again. Then six. Her face remained as smooth as still water. She can't be six-and-thirty, Arya thought. 'You're lying,' she said. The waif shook her head and showed her once again."
_Rationale:_ The waif's age-claim (six-and-thirty) is the lying game's first successful deception against Arya — she guesses wrong, the waif's claim turns out true. The waif also subsequently claims she lied about the lie, then denies that too. This is the node of radical uncertainty that the lying game is built around.

**E15**
`(arya-stark, DECEIVES, waif)` | Tier 1 | affc-arya-02:221–223 | "'No one,' Arya answered, in Braavosi. 'You lie,' said the waif. 'You must lie gooder.'"
_Rationale:_ Arya's "no one" answer fails against the waif, establishing waif also has the FM lie-detection. This documents the mentor → novice deception-training loop.

---

### MOTIVATES / CAUSES EDGES

**E16**
`(dareon, MOTIVATES, arya-stark)` | Tier 1 | affc-cat-of-the-canals-01:143 | "He is a man of the Night's Watch, she thought. . . . And the singer should be on the Wall. When Dareon had first appeared at the Happy Port, Arya had almost asked if he would take her with him back to Eastwatch, until she heard him telling Bethany that he was never going back."
_Rationale:_ Dareon's confessed desertion activates Arya's Stark-justice framework — she decides he must die as a deserter. This MOTIVATES her decision to kill him. Note the specific mechanism: she has Ned's "the man who passes the sentence should swing the sword" code active internally.

**E17**
`(kindly-man, MOTIVATES, arya-stark)` | Tier 2 | adwd-the-blind-girl-01:143–147 | "'And are you a god, to decide who should live and who should die?' he asked her. . . . 'All men must die. We are but death's instruments, not death himself. When you slew the singer, you took god's powers on yourself. We kill men, but we do not presume to judge them. Do you understand?' No, she thought. 'Yes,' she said. 'You lie. And that is why you must now walk in darkness until you see the way.'"
_Rationale:_ Kindly man's rebuke (she judged Dareon as a deserter, which is not FM doctrine) directly MOTIVATES the blinding. CAUSES is too strong — the blinding is the priest's chosen consequence, not automatic. MOTIVATES captures that the rebuke creates the condition.

---

### AGENCY EDGES (confirmed kills)

**E18**
`(arya-stark, AGENT_IN, the-insurance-underwriter-dies)` | Tier 1 | adwd-the-ugly-little-girl-01:259–261 | "'It wasn't stealing. I took one of his, but I left him one of ours.' The kindly man understood. 'And with that coin and the others in his purse, he paid a certain man. Soon after that man's heart gave out. Is that the way of it? Very sad.'"
_Rationale:_ Arya engineers the underwriter's death via coin-swap: a Westerosi dragon (FM-poisoned or FM-marked) enters the underwriter's purse through the shipowner she "robbed" (allowing her to substitute coins). The underwriter pays the coin out, then dies of apparent heart failure. Text confirms the mechanism and the kindly man acknowledges it. This is Arya's first official FM kill. AGENT_IN not KILLS because the death is indirect (no weapon, "heart gave out").

**E19 — SUSPECTED_OF**
`(unnamed-petitioner, SUSPECTED_OF, contracting-underwriter-death)` | Tier 2 | adwd-the-ugly-little-girl-01:135 | "One of them must hate him. One of them came to the House of Black and White and prayed for the god to take him. She wondered who it had been, but the kindly man would not tell her."
_Rationale:_ The text establishes that someone paid the FM's price to have the underwriter killed — a captain or shipowner who was denied a claim. The identity is deliberately withheld in-text ("kindly man would not tell her"). This is genuine unproven agency. SUSPECTED_OF is the right edge; capped Tier 2. The petitioner node is unnamed but the edge class is real.
_Note: if `unnamed-petitioner` is too vague for a node, mark as a dangling evidence note on the underwriter's node instead._

---

### CONTRACTED_WITH EDGES

**E20**
`(unnamed-petitioner, CONTRACTED_WITH, many-faced-god)` | Tier 2 | adwd-the-ugly-little-girl-01:135 | "One of them came to the House of Black and White and prayed for the god to take him."
_Rationale:_ The FM kill is framed as a prayer + sacrifice to the Many-Faced God, not a direct mercenary contract. The petitioner offers "all he had" (consistent with FM doctrine established in the origin story). CONTRACTED_WITH captures the FM's own framing — the god accepts the prayer, the FM execute it.

**E21**
`(faceless-men, CONTRACTED_WITH, many-faced-god)` | Tier 1 | affc-arya-02:191 | "He moved amongst the slaves and would hear them at their prayers. . . . All gods have their instruments. . . . and he was that god's instrument. That very night he chose the most wretched of the slaves . . . and freed him from his bondage. The first gift had been given."
_Rationale:_ The FM origin story frames the entire order as instruments of the Many-Faced God, operating under divine contract since Valyria. CONTRACTED_WITH (FM → MFG) is the structural edge; it is the theological basis for every kill the FM undertake.

---

## NOTES / FLAGS

- **NEEDS_VOCAB: worn-face sub-kind.** The arc distinguishes mummer's-art disguise (Blind Beth — costume + prosthetics) from literal FM skin-wearing (ugly-little-girl). Both map to DISGUISED_AS but the graph loses the mechanistic distinction. Suggest an optional `method` field on DISGUISED_AS: `mummery` vs `worn-face`.
- **DEDUP NOTE: arya KILLS dareon** already exists as a node/edge. E16 (MOTIVATES) is new and distinct — it links Dareon's desertion to Arya's decision, not the kill itself.
- **E17 blinding:** If a `kindly-man-blinds-arya` event node exists, wire E17 as MOTIVATES toward it. If not, it can float as a character→character MOTIVATES for now.
- **Harvest note (adwd-the-blind-girl-01:183–185):** The Hardhome slave-ship intelligence Arya gathers at Pynto's is a cross-arc thread (Hardhome wildlings, Sealord's seizure of the Goodheart). Touches the wildling/Wall arc. Flag for a Harvest pass — the Goodheart seizure is a standalone event with potential cross-character edges.
