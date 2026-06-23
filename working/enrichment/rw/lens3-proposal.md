# Red Wedding Enrichment Dip — Lens 3 Proposal
# DESCRIPTIVE / QUOTE / OBJECT DEPTH
# Generated: S134, 2026-06-23

> PROPOSE ONLY — mint nothing. All quotes line-checked against source files.
> Dedup performed against baseline.md. Items already in existing Quotes blocks are excluded.

---

## Verification summary before proposals

Existing Quotes blocks checked for each target node:

- **catelyn-stark**: Has quotes but NOT the Red Wedding madness passage (the "ten fierce ravens" line) or the "He is my son. My first son, and my last" plea — those are absent.
- **roose-bolton**: Has a rich Quotes section. Does NOT have the verbatim "Jaime Lannister sends his regards" line from Catelyn's POV (the robb-is-killed beat already has it, but roose-bolton.node.md Quotes section does NOT contain it — confirmed by reading lines 104–177).
- **walder-frey**: Has "Heh, the King in the North arises…" (line 162) — ALREADY PRESENT. The "In the midst of slaughter…watching greedily" line is already on red-wedding hub (line 80-82 of red-wedding.node.md) — DO NOT re-propose.
- **robb-is-killed**: Already has "Jaime Lannister sends his regards" quote (lines 31–33). DO NOT re-propose.
- **red-wedding hub**: Already has "In the midst of slaughter…watching greedily" and several other key quotes. DO NOT re-propose.
- **grey-wind**: Has several quotes but NOT the RW-night howl ("closer the wild howling of a wolf") from asos-catelyn-07:113, nor the Arya exterior perception of the wolf cry (asos-arya-11:19).
- **the-rains-of-castamere**: Already has "No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it." and the Arya recognition passage — BOTH ALREADY PRESENT. DO NOT re-propose.
- **guest-right**: Has the bread-and-salt exchange (asos-catelyn-06:167, in the multi-line dialogue block at lines 62–65 of the node). ALREADY PRESENT. DO NOT re-propose.
- **catelyn-secures-guest-right** (beat node): Has prose description only — NO Quotes block.
- **roslin-frey**: Has Edmure's dialogue "She wept, but I thought it was…" (AFFC source). The wedding-night tears from catelyn's POV (asos-catelyn-07:91) are NOT present.
- **catelyn-is-killed** (beat node): Minimal stub — no Quotes block.

---

## PROPOSALS

---

### P1 — ATTACH_QUOTE
**Target node:** `catelyn-stark`
**Section:** ## Quotes → ### Quotes by Catelyn
**Quote (verbatim, line-checked):**

> "He is my son. My first son, and my last. Let him go. Let him go and I swear we will forget this . . . forget all you've done here. I swear it by the old gods and new, we . . . we will take no vengeance . . ."

— Catelyn Stark to Walder Frey, ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:115`)

**Why load-bearing:** This is Catelyn's formal hostage plea — the last act of maternal agency before the slaughter completes. It names all the conditions (oath by old gods and new, no vengeance) that make her subsequent killing more brutal. Not present anywhere in catelyn-stark.node.md Quotes. Pairs with the existing "A son for a son" quote (line 177–179 of node) but is the fuller, more emotionally complete version.

**Confirm not already present:** The node has a "On my honor as a Tully / A son for a son" exchange (lines 177–179) which is the FOLLOW-UP exchange. The quote above is a separate, prior speech. Confirmed absent.

---

### P2 — ATTACH_QUOTE
**Target node:** `catelyn-stark`
**Section:** ## Quotes → ### Quotes by Catelyn (or new sub-heading: ### Catelyn's final moments)
**Quote (verbatim, line-checked):**

> It hurts so much, she thought. Our children, Ned, all our sweet babes. Rickon, Bran, Arya, Sansa, Robb . . . Robb . . . please, Ned, please, make it stop, make it stop hurting . . .

— Catelyn Stark (internal monologue), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:141`)

**Why load-bearing:** The last coherent thought before her throat is cut — rolls through all five children in order of loss, ending on Robb twice. This is the passage that makes her death a character moment rather than just a plot event. Not present in catelyn-stark.node.md.

**Confirm not already present:** Confirmed absent from the Quotes blocks (lines 143–229 of node).

---

### P3 — ATTACH_QUOTE
**Target node:** `roose-bolton`
**Section:** ## Quotes → ### Quotes by Roose
**Quote (verbatim, line-checked):**

> "Jaime Lannister sends his regards."

— Roose Bolton to Robb Stark (before the killing blow), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:135`)

**Why load-bearing:** This is Roose's single most iconic spoken line — the four-word delivery that crystallizes the conspiracy (Tywin's hand, Jaime's sardonic parting message, Roose's cold execution) and gives the robb-is-killed beat its name. It's already quoted in full context on `robb-is-killed`, but the **roose-bolton character node's Quotes section does not contain it** (confirmed by reading lines 104–177 — the Quotes by Roose are: leeches quote, Lord Tywin/Aenys exchange, People fear you/Good, Power tastes best, All you have I gave you, Fear is what keeps a man alive). Attaching here gives the character node its definitive RW-context quote.

**Confirm not already present:** Confirmed absent from roose-bolton.node.md Quotes section.

---

### P4 — ATTACH_QUOTE
**Target node:** `grey-wind`
**Section:** ## Quotes → ### Quotes about Grey Wind
**Quote (verbatim, line-checked):**

> She heard the crash of distant battle, and closer the wild howling of a wolf. Grey Wind, she remembered too late.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:113`)

**Why load-bearing:** This is the RW-chapter's only direct citation of Grey Wind's howl during the slaughter — the "too late" is the knife: Catelyn had been warned by his instincts all along. It belongs on Grey Wind's node as the definitive Red Wedding evidence. The node already has quotes about Grey Wind's instincts (Catelyn to Robb about trusting him) but NOT this RW-night moment.

**Confirm not already present:** grey-wind.node.md Quotes section (lines 59–101) does not contain this line. Confirmed absent.

---

### P5 — ATTACH_QUOTE
**Target node:** `grey-wind`
**Section:** ## Quotes → ### Quotes about Grey Wind
**Quote (verbatim, line-checked):**

> Somewhere far off she heard a wolf howling. It wasn't very loud compared to the camp noise and the music and the low ominous growl of the river running wild, but she heard it all the same. Only maybe it wasn't her ears that heard it. The sound shivered through Arya like a knife, sharp with rage and grief.

— Arya Stark (narrator), ASOS Arya XI (`sources/chapters/asos/asos-arya-11.md:19`)

**Why load-bearing:** Arya hears Grey Wind dying from outside the Twins — possibly through wargsense rather than hearing ("maybe it wasn't her ears"). This is the only exterior witness to Grey Wind's death-howl, and the "sharp with rage and grief" makes it a direwolf-bond quote, not just a background sound. Not on grey-wind node.

**Confirm not already present:** Confirmed absent from grey-wind.node.md Quotes section.

---

### P6 — ATTACH_QUOTE
**Target node:** `catelyn-secures-guest-right` (beat node)
**Section:** add ## Quotes block
**Quote (verbatim, line-checked):**

> "Robb, listen to me. Once you have eaten of his bread and salt, you have the guest right, and the laws of hospitality protect you beneath his roof."

— Catelyn Stark to Robb Stark, ASOS Catelyn VI (`sources/chapters/asos/asos-catelyn-06.md:27`)

**Why load-bearing:** This is the most explicit statement of what guest right means and WHY Catelyn secures it — Catelyn is teaching Robb the custom's protective logic. The beat node (`catelyn-secures-guest-right`) has zero quotes and only a one-sentence prose description. This quote is its load-bearing evidence.

**Confirm not already present:** The beat node has no Quotes section at all. Confirmed absent.

---

### P7 — ATTACH_QUOTE
**Target node:** `catelyn-secures-guest-right` (beat node)
**Section:** ## Quotes (second entry — or could be combined with P6)
**Quote (verbatim, line-checked):**

> "We thank you for your hospitality, my lord," Robb replied. Edmure echoed him, along with the Greatjon, Ser Marq Piper, and the others. They drank his wine and ate his bread and butter. Catelyn tasted the wine and nibbled at some bread, and felt much the better for it. Now we should be safe, she thought.

— Catelyn Stark (narrator), ASOS Catelyn VI (`sources/chapters/asos/asos-catelyn-06.md:169`)

**Why load-bearing:** "Now we should be safe, she thought" — the irony-pin. The entire Red Wedding's horror hinges on this sentence. Documents the exact moment guest right was invoked and Catelyn's belief in its protection. Pairs with P6 to give the beat node a complete evidence set.

**Confirm not already present:** Beat node has no Quotes section. Confirmed absent.

---

### P8 — ATTACH_QUOTE
**Target node:** `roslin-frey`
**Section:** ## Quotes → ### Quotes about Roslin (new entry, from Catelyn's POV)
**Quote (verbatim, line-checked):**

> Poor Roslin's smile had a fixed quality to it, as if someone had sewn it onto her face.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:21`)

**Why load-bearing:** The single best physical description of Roslin during the feast, and it's freighted: "sewn onto her face" is a vivid image that foregrounds her foreknowledge of the massacre. It's Catelyn's POV read of the same tears Edmure confesses about in AFFC. Not in roslin-frey.node.md Quotes (which covers the introduction scene and the AFFC Edmure confession, but not this wedding-feast observation).

**Confirm not already present:** roslin-frey.node.md Quotes (lines 68–103) does not have this line. The existing "Quotes about Roslin" entries are from other characters' POV; this is from Catelyn's observation during the feast itself. Confirmed absent.

---

### P9 — ATTACH_QUOTE
**Target node:** `roslin-frey`
**Section:** ## Quotes → ### Quotes about Roslin
**Quote (verbatim, line-checked):**

> She's crying too, Catelyn realized as she watched Ser Marq Piper pull off one of the bride's shoes. I hope Edmure is gentle with the poor child.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:91`)

**Why load-bearing:** Catelyn's real-time recognition of Roslin's tears during the bedding ceremony — she attributes it to terror of the bedding, not foreknowledge. This is the dramatic irony setup for Edmure's AFFC confession (already on the node: "she wept, but I thought it was…"). Both moments exist on the node but this POV-observation is missing.

**Confirm not already present:** Confirmed absent from roslin-frey.node.md Quotes section.

---

### P10 — ATTACH_APPEARANCE (descriptive detail)
**Target node:** `roose-bolton`
**Section:** ## Appearances & Description
**Detail to attach:**
Roose Bolton wore black ringmail concealed beneath a silken sleeve at the Red Wedding — the iron rings Catelyn felt when she grabbed his arm signaled the massacre was already underway. He stepped up to Robb in "dark armor and a pale pink cloak spotted with blood." The node already describes his attire (lines 50 of node) but does not cite the specific RW instance, which is the definitive on-page confirmation of his armor type.

**Verbatim line:**
> A man in dark armor and a pale pink cloak spotted with blood stepped up to Robb.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:135`)

**Note:** The note about the iron rings under the silken sleeve is the earlier passage:

> She hurried faster, driven by the music. Six quick strides and she caught him. And who are you, the proud lord said, that I must bow so low? She grabbed Edwyn by the arm to turn him and went cold all over when she felt the iron rings beneath his silken sleeve.

— ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:99`)

**Why load-bearing:** This passage confirms that Frey men (Edwyn) were also concealing mail, and that "The Rains of Castamere" lyric running through Catelyn's mind AS she discovers the iron rings is what locks the signal function of the song. This detail (the lyric as internal monologue superimposed on the mail discovery) is not on any existing node.

**Proposed target for the Edwyn/mail/Rains linkage:** attach to `the-rains-of-castamere` node's Narrative Arc or Quotes, as this is the only passage where Catelyn's RECOGNITION of the song triggers the physical discovery. The node already quotes "No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it" but not the iron-rings passage that immediately follows it.

---

### P11 — ATTACH_QUOTE
**Target node:** `the-rains-of-castamere`
**Section:** ## Quotes (append)
**Quote (verbatim, line-checked):**

> Edwyn was hurrying toward a door. She hurried faster, driven by the music. Six quick strides and she caught him. And who are you, the proud lord said, that I must bow so low? She grabbed Edwyn by the arm to turn him and went cold all over when she felt the iron rings beneath his silken sleeve.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:99`)

**Why load-bearing:** This is the only passage where the Rains lyric is rendered in Catelyn's interior voice at the exact moment she discovers the concealed mail — the song literally narrates the discovery. The lyric ("And who are you, the proud lord said, that I must bow so low?") is the closest the novel gets to quoting the Rains mid-action. Node already has "No one sang the words, but Catelyn knew…" but NOT this lyric-in-motion passage.

**Confirm not already present:** the-rains-of-castamere.node.md Quotes (lines 50–59) has six entries; none contains this passage. Confirmed absent.

---

### P12 — ATTACH_QUOTE
**Target node:** `catelyn-is-killed` (beat node, currently a stub)
**Section:** add ## Quotes block
**Quote (verbatim, line-checked):**

> Finally someone took the knife away from her. The tears burned like vinegar as they ran down her cheeks. Ten fierce ravens were raking her face with sharp talons and tearing off strips of flesh, leaving deep furrows that ran red with blood. She could taste it on her lips.

— Catelyn Stark (narrator), ASOS Catelyn VII (`sources/chapters/asos/asos-catelyn-07.md:139`)

**Why load-bearing:** This is the onset of Catelyn's madness — the self-tearing described as ravens (her own hands, clawing her face), rendered as hallucination. It is the pivotal physical moment of the `catelyn-is-killed` beat: not her throat being cut but the psychological disintegration that precedes it, and which explains why the Epilogue describes her corpse's ravaged face. The beat node is currently a minimal stub with no Quotes section.

**Confirm not already present:** catelyn-is-killed.node.md has no Quotes section. Confirmed absent.

---

### P13 — ATTACH_QUOTE (Arya exterior / Hound dialogue)
**Target node:** `red-wedding` (hub, under ## Quotes, appended)
**Quote (verbatim, line-checked):**

> "Stupid little bitch. You go in there, you won't come out. Maybe Frey will let you kiss your mother's corpse."

— Sandor Clegane to Arya Stark, ASOS Arya XI (`sources/chapters/asos/asos-arya-11.md:51`)

**Why load-bearing:** The Hound's flat statement to Arya that Catelyn is already dead — spoken in real-time, from outside the Twins — is the only on-page moment where the massacre's completion is announced to Arya. It also frames the Hound's protective pragmatism. The red-wedding hub Quotes section (lines 62–118) has Arya's "The camp had become a battlefield. No, a butcher's den." but not this Hound line. Proposing for the hub as it's the external-witness punctuation of the massacre.

**Confirm not already present:** red-wedding.node.md Quotes section (lines 62–118) does not contain this line. Confirmed absent.

---

## OBJECT / PLACE DETAIL NOTES (not ATTACH_QUOTE — for orchestrator consideration)

**Wedding feast food (object.food candidates):**
The feast menu is explicitly described at asos-catelyn-07:17: "a thin leek soup, followed by a salad of green beans, onions, and beets, river pike poached in almond milk, mounds of mashed turnips that were cold before they reached the table, jellied calves' brains, and a leche of stringy beef." Later: "huge silver platters piled high with cuts of juicy pink lamb" (line 75).

This is poor fare — deliberately so, signaling disrespect. The calves' brains turn Catelyn's stomach. No food nodes exist for these dishes and no action is proposed here (the harvest queue handles this — see below). However, the **pink lamb** arriving just before the massacre is a notable object: served after the bedding is called, it's the last visual before the Rains begin. Could annotate the `the-wedding-feast-proceeds` beat if that node exists, but no proposal without checking that node.

**Walder on his carved oaken throne:**
Already quoted on red-wedding hub ("In the midst of slaughter, the Lord of the Crossing sat on his carved oaken throne, watching greedily"). No new proposal needed.

**The musicians' gallery / crossbowmen:**
The chapter describes "half the musicians had crossbows in their hands instead of drums or lutes" (asos-catelyn-07:103). This is noted in the Narrative Arc of red-wedding.node.md but no verbatim quote from the chapter is attached to any node for this specific image. Proposing one harvest note rather than a full quote (low marginal value vs. the character quotes above).

---

## HARVEST QUEUE ENTRIES

> Append to `/Users/mnoth/source/asoiaf-chat/working/harvest-queue.md`

| open | food | asos | asos-catelyn-07:17 | Wedding feast menu: leek soup / green beans+onions+beets / river pike in almond milk / cold mashed turnips / jellied calves' brains / leche of stringy beef — poor fare, deliberate disrespect | S134 RW-lens3 |
| open | food | asos | asos-catelyn-07:75 | "huge silver platters piled high with cuts of juicy pink lamb" — last food served before the Rains signal; arrives just as the bedding is cleared | S134 RW-lens3 |
| open | food | asos | asos-catelyn-07:15 | Roose Bolton drinks hippocras at the wedding feast, eats little — specific drink reveals his restraint/control vs. the drunken lords around him | S134 RW-lens3 |
| open | hospitality | asos | asos-catelyn-07:109 | "In the midst of slaughter, the Lord of the Crossing sat on his carved oaken throne, watching greedily" — already on red-wedding hub; note for cross-reference if walder-frey throne node ever minted | S134 RW-lens3 |
| open | appearance | asos | asos-catelyn-07:103 | "half the musicians had crossbows in their hands instead of drums or lutes" — the crossbowmen-as-musicians image; no verbatim quote on any node | S134 RW-lens3 |
| open | foreshadowing | asos | asos-catelyn-07:97 | Dacey Mormont asks Edwyn Frey to dance and he recoils "with unseemly violence" — the first behavioral signal Catelyn reads; foreshadowing of imminent attack | S134 RW-lens3 |
| open | other | asos | asos-catelyn-07:37 | Walder forbids Grey Wind from the hall ("Your wild beast has a taste for human flesh, I hear, heh… I'll have no such creature at my Roslin's feast") — this is a conscious strategic act to isolate Robb from his protector; no edge for WALDER_FREY → ISOLATES → GREY_WIND exists | S134 RW-lens3 |
| open | witness | asos | asos-arya-11:47 | Arya hears "And now the rains weep o'er his hall, with not a soul to hear" in her head as the camp burns — the fourth stanza of the Rains playing in her inner voice; different verse from the ones already on the-rains-of-castamere node | S134 RW-lens3 |
| open | quote | asos | asos-tyrion-06:201 | Tyrion on Sansa: "And when do you imagine Sansa will be at her most fertile? Before or after I tell her how we murdered her mother and her brother?" — load-bearing Tyrion quote about RW aftermath; not on tyrion-lannister.node.md Quotes | S134 RW-lens3 |
| open | appearance | asos | asos-catelyn-07:29 | Fat Walda Bolton describes herself: "I weigh six stone more than Fair Walda, but that was the first time I was glad of it. I'm Lady Bolton now" — appearance + personality in one line; walda-frey node may lack this | S134 RW-lens3 |
