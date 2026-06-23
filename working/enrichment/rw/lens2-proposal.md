# Red Wedding enrichment dip — Lens 2 proposals (S134)
## Secondary-character sub-arcs + SUSPECTED_OF / WITNESS substrate

Dedup verified against `baseline.md`. All NEW_NODE proposals verified non-existent via `find graph/nodes`.
All NEW_EDGE proposals verified not already present via `graph-query.py --neighbors`.

---

## NEW_EDGE proposals

---

### E1 — Lothar Frey AGENT_IN red-wedding-conspiracy (the actual planner)
- **kind:** NEW_EDGE
- **edge:** `lothar-frey --AGENT_IN--> red-wedding-conspiracy`
- **tier:** Tier-1
- **chapter:line:** `asos-epilogue.md:31`
- **verbatim quote:** "Lord Walder had ordered the slaughter of the Starks at Roslin's wedding, but it had been Lame Lothar who had plotted it out with Roose Bolton, all the way down to which songs would be played."
- **rationale:** Merrett's POV explicitly names Lothar as the operational architect of the conspiracy (not merely present). Lothar currently has only `CONSPIRES_WITH roose-bolton` — that dyadic edge should be KEPT but the event-hub role edge is missing. This is the highest-value gap in the planner tier.

---

### E2 — Lothar Frey COMMANDS_IN red-wedding (tents + gallery detail)
- **kind:** NEW_EDGE
- **edge:** `lothar-frey --COMMANDS_IN--> red-wedding`
- **tier:** Tier-1
- **chapter:line:** `asos-epilogue.md:165`
- **verbatim quote:** "Lothar rigged the tents to collapse and put the crossbowmen in the gallery with the musicians"
- **rationale:** Merrett explicitly attributes the two key tactical preparations (tent collapse + crossbow gallery) to Lothar. He operationally commanded these preparations, making him a COMMANDS_IN on the hub event itself, not just the conspiracy.

---

### E3 — Black Walder Frey AGENT_IN the-camp-becomes-a-battlefield
- **kind:** NEW_EDGE
- **edge:** `black-walder-frey --AGENT_IN--> the-camp-becomes-a-battlefield`
- **tier:** Tier-1
- **chapter:line:** `asos-epilogue.md:165`
- **verbatim quote:** "Bastard Walder led the attack on the camps"
- **rationale:** Merrett names Black Walder as the commander of the camp assault. Currently the beat has only `house-frey AGENT_IN`. Individual command is more granular and higher value. ("Bastard Walder" = Black Walder Rivers/Frey, Walder Frey's bastard — same as `black-walder-frey` node.)
- **UNSURE flag:** The epilogue calls him "Bastard Walder." The node slug `black-walder-frey` may be a *different* Walder — the legitimate son "Black Walder Rivers." Orchestrator should confirm: is `black-walder-frey` Ser Black Walder Rivers or the bastard Walder? The epilogue's "Bastard Walder" is the illegitimate one. If they are different characters, this proposal needs a new node. Per current graph, the epilogue at line 23 already cites `black-walder-frey` with this chapter as source, so the node appears to be used for the bastard. Proceed with flag.

---

### E4 — Roose Bolton WITNESS_IN robb-is-killed
- **kind:** NEW_EDGE
- **edge:** `roose-bolton --WITNESS_IN--> robb-is-killed`
- **tier:** Tier-1
- **chapter:line:** `asos-catelyn-07.md:135`
- **verbatim quote:** "A man in dark armor and a pale pink cloak spotted with blood stepped up to Robb. 'Jaime Lannister sends his regards.' He thrust his longsword through her son's heart, and twisted."
- **rationale:** Roose Bolton is already AGENT_IN robb-is-killed (he is the killer). The WITNESS_IN is therefore redundant — do NOT emit this. **Retract E4.** (The killer is the most proximate witness; AGENT_IN already covers it.)

---

### E4 (revised) — Catelyn Stark WITNESS_IN robb-is-killed
- **kind:** NEW_EDGE
- **edge:** `catelyn-stark --WITNESS_IN--> robb-is-killed`
- **tier:** Tier-1
- **chapter:line:** `asos-catelyn-07.md:135`
- **verbatim quote:** "He thrust his longsword through her son's heart, and twisted."
- **prose proof of sight:** Catelyn is the POV; she describes watching Roose step up to Robb, hears "Jaime Lannister sends his regards," and sees the sword thrust. Her presence is unambiguous. Immediately after she screams "Robb!" (line 135-136). She SEES the killing blow.
- **rationale:** Catelyn is currently ATTENDS the-wedding-feast-proceeds and VICTIM_IN catelyn-is-killed, but has no WITNESS_IN on robb-is-killed. This is the most emotionally and narratively charged witness moment in the entire scene. High value.

---

### E5 — Catelyn Stark WITNESS_IN catelyn-secures-guest-right (ALREADY BUILT — skip)
- Baseline shows `catelyn-stark AGENT_IN catelyn-secures-guest-right`. AGENT_IN already encodes her active role; WITNESS_IN would be redundant. Drop.

---

### E5 (renumbered) — Smalljon Umber AGENT_IN robb-is-killed (protective act)
- **kind:** NEW_EDGE
- **edge:** `jon-umber-son-of-jon --AGENT_IN--> robb-is-killed`
- **tier:** Tier-1
- **chapter:line:** `asos-catelyn-07.md:103`
- **verbatim quote:** "She saw Smalljon Umber wrestle a table off its trestles. Crossbow bolts thudded into the wood, one two three, as he flung it down on top of his king."
- **rationale:** The Smalljon actively shields Robb from crossbow bolts, placing his body between king and killers — he is an AGENT_IN the kill event (as defender/shield). His later decapitation (line 107) is noted but no individual node exists for the Smalljon's death. This edge attaches his protective heroism to the hub beat.
- **UNSURE flag:** Confirm `jon-umber-son-of-jon` is the Smalljon (the son of Greatjon). The node slug suggests it; verify.

---

### E6 — Jon Umber (Greatjon) VICTIM_IN robb-is-killed (captured, not killed — resists)
- **kind:** NEW_EDGE
- **edge:** `jon-umber --VICTIM_IN--> robb-is-killed`
- **tier:** Tier-1 (with note)
- **chapter:line:** `asos-epilogue.md:47`
- **verbatim quote:** "after Roslin had been bedded the Greatjon still managed to snatch the sword of the first man to accost him and break his arm in the snatching. It had taken eight of them to get him into chains, and the effort had left two men wounded, one dead, and poor old Ser Leslyn Haigh short half an ear. When he couldn't fight with his hands any longer, Umber had fought with his teeth."
- **rationale:** The Greatjon is currently `AGENT_IN the-bedding-ceremony-begins` only. He is a VICTIM_IN (captured but surviving) of the massacre hub. The bite-off-fingers detail (teeth fighting) is from this passage. The beat `robb-is-killed` is the closest hub beat; alternatively this attaches to `red-wedding` hub directly.
- **note:** Attach to `red-wedding` hub (the overall massacre) rather than the `robb-is-killed` sub-beat, since his capture happened after Robb was already down and spans the whole event. Prefer: `jon-umber --VICTIM_IN--> red-wedding`.

---

### E7 — Roslin Frey WITNESS_IN robb-is-killed (she knew, she wept before)
- **kind:** NEW_EDGE (SUSPECTED_OF variant considered, rejected)
- **edge:** Considered `roslin-frey --WITNESS_IN--> robb-is-killed`, but she had already been bedded (carried from hall before massacre) — she did NOT see Robb killed. She knew the plan (her foreknowledge is in her weeping during the feast). **Gate fails: she was removed from the hall before the killing blows.** Drop witness edge.
- **Alternate proposal E7:** `roslin-frey --SUSPECTED_OF--> red-wedding-conspiracy`
  - **tier:** Tier-2 (cap for SUSPECTED_OF)
  - **chapter:line:** `asos-catelyn-07.md:101`
  - **verbatim quote:** "Olyvar, she thought, and Perwyn, Alesander, all absent. And Roslin wept..."
  - **rationale:** Catelyn's dawning recognition explicitly links Roslin's pre-massacre weeping to foreknowledge. Roslin did not plan the massacre but knew it was coming — SUSPECTED_OF (Tier-2) captures "unproven agency as aware participant." Her weeping is the in-text tell. This is a high-value SUSPECTED_OF substrate.

---

### E8 — The Rains of Castamere AGENT_IN red-wedding (used as massacre signal)
- **kind:** NEW_EDGE
- **edge:** `the-rains-of-castamere --AGENT_IN--> red-wedding`
- **tier:** Tier-1
- **chapter:line:** `asos-catelyn-07.md:99`
- **verbatim quote:** "She did not answer him. Instead she went after Edwyn Frey. The players in the gallery had finally gotten both king and queen down to their name-day suits. With scarcely a moment's respite, they began to play a very different sort of song. No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it."
- **chapter:line (Arya corroboration):** `asos-arya-11.md:25`
- **verbatim quote (Arya):** "For once the same song was coming from both castles. I know this song, Arya realized suddenly."
- **rationale:** The Rains of Castamere node currently has zero edges. The song is the operational signal for the massacre. AGENT_IN is the right type: the song is the instrument that triggers the attack, not merely background music. Catelyn recognizes it; Arya recognizes it from both castles simultaneously. This is the most causal instrumentality the song has in the entire text — its most important moment.

---

### E9 — Merrett Frey ATTENDS red-wedding (explicit presence)
- **kind:** NEW_EDGE
- **edge:** `merrett-frey --ATTENDS--> red-wedding`
- **tier:** Tier-1
- **chapter:line:** `asos-epilogue.md:45-47`
- **verbatim quote:** "Lame Lothar had summoned him to discuss his role in Roslin's wedding. 'You shall have one task and one task only, Merrett, but I believe you are well suited to it. I want you to see to it that Greatjon Umber is so bloody drunk that he can hardly stand, let alone fight.' And even that I failed at."
- **rationale:** Merrett currently has only `AGENT_IN merrett-attempts-to-defend-his-innocence-in-the-red-wedding` — a post-RW event. He lacks any edge to the Red Wedding event hub itself. He was physically present and had an assigned role (drunkard handler). This grounds his later plea-for-innocence in actual event participation.

---

### E10 — Merrett Frey AGENT_IN red-wedding-conspiracy (assigned role)
- **kind:** NEW_EDGE
- **edge:** `merrett-frey --AGENT_IN--> red-wedding-conspiracy`
- **tier:** Tier-2 (he was assigned a sub-task; not a planner)
- **chapter:line:** `asos-epilogue.md:45`
- **verbatim quote:** "Lame Lothar had summoned him to discuss his role in Roslin's wedding. 'You shall have one task and one task only, Merrett... I want you to see to it that Greatjon Umber is so bloody drunk that he can hardly stand, let alone fight.'"
- **rationale:** Merrett was tasked with neutralizing the Greatjon — a conspiracy sub-task. Tier-2 because he denies being a planner and his role is functional/minor, but he was knowingly assigned a conspiracy role. Tier-2 (not Tier-1) because "role in Roslin's wedding" could be read innocuously; however the context (getting the Greatjon drunk "so he can't fight") makes it clear it was conspiracy prep.

---

### E11 — Lothar Frey CONSPIRES_WITH roose-bolton (already EXISTS — skip)
- Baseline check: this edge already exists on `lothar-frey`. Confirmed via `--neighbors lothar-frey`. Drop.

---

### E12 — Edwyn Frey AGENT_IN red-wedding (the mail-shirt reveal + first move)
- **kind:** NEW_EDGE
- **edge:** `edwyn-frey --AGENT_IN--> red-wedding`
- **tier:** Tier-1
- **chapter:line:** `asos-catelyn-07.md:99`
- **verbatim quote:** "She grabbed Edwyn by the arm to turn him and went cold all over when she felt the iron rings beneath his silken sleeve."
- **rationale:** Edwyn Frey's hidden mail and his move toward the door is Catelyn's first physical proof the massacre is beginning. He is actively evading to allow it to proceed — an agent role. `edwyn-frey` node exists, has 0 edges to any RW event. This is a textually anchored, high-signal gap.

---

### E13 — Roose Bolton AGENT_IN robb-is-killed — ALREADY EXISTS. Skip.
- Confirmed via `--neighbors robb-is-killed`. Drop.

---

### E14 — Arya Stark WITNESS_IN the-camp-becomes-a-battlefield
- **kind:** NEW_EDGE
- **edge:** `arya-stark --WITNESS_IN--> the-camp-becomes-a-battlefield`
- **tier:** Tier-1
- **chapter:line:** `asos-arya-11.md:21-47`
- **verbatim quote:** "The camp had become a battlefield. No, a butcher's den. The flames from the feasting tents reached halfway up the sky... Everywhere swords were singing... She saw two knights ride down a running man."
- **prose proof of sight:** Arya is the POV of `asos-arya-11.md`; she watches the tents collapse, the Frey riders pour out, the burning camp, men being cut down. She SEES it all from outside the walls.
- **rationale:** The camp-becomes-a-battlefield beat's existing edges don't include any WITNESS_IN. Arya's exterior view is the only on-page witness perspective of the camp slaughter (Catelyn's POV is interior). This is a high-value witness substrate: Arya's traumatic exterior witnessing seeds her grief, kill-list expansion, and future arc.

---

### E15 — Arya Stark WITNESS_IN grey-wind-attacks (hears wolf, sees camp aftermath)
- **kind:** NEW_EDGE (PARTIAL — see below)
- **edge:** `arya-stark --WITNESS_IN--> grey-wind-attacks`
- **tier:** Tier-2 (she hears/senses, does not see Grey Wind die directly)
- **chapter:line:** `asos-arya-11.md:19`
- **verbatim quote:** "Somewhere far off she heard a wolf howling. It wasn't very loud compared to the camp noise and the music and the low ominous growl of the river running wild, but she heard it all the same. Only maybe it wasn't her ears that heard it. The sound shivered through Arya like a knife, sharp with rage and grief."
- **rationale:** Arya perceives Grey Wind's howl through her warg-bond (the "not her ears" qualifier). She does not visually see Grey Wind killed; the desecration (head sewn on Robb's body) she learns later. WITNESS_IN gate is borderline — she perceives but it is not visual. Flag as UNSURE: the prose-bond perception may not clear the visual-sight gate. Orchestrator to decide if warg-perception counts as WITNESS_IN or if this warrants a new edge type.
- **UNSURE flag:** Warg-bond howl perception vs. visual sight. Consider leaving as harvest queue item instead.

---

## HARVEST QUEUE additions

Appended to `working/harvest-queue.md` below. (Notation: per spec.)

| open | quote | asos | asos-catelyn-07.md:131 | Catelyn's threat with Jinglebell's throat — "On my honor as a Tully, on my honor as a Stark, I will trade your boy's life for Robb's" — verbatim hostage-negotiation quote, high value for Catelyn node ## Quotes | S134 RW-lens2 |
| open | quote | asos | asos-catelyn-07.md:135 | "Jaime Lannister sends his regards" — canonical Roose Bolton line, should be ## Quotes on roose-bolton node | S134 RW-lens2 |
| open | quote | asos | asos-epilogue.md:31 | "all the way down to which songs would be played" — Lothar as music-signal planner, extends Castamere signal significance | S134 RW-lens2 |
| open | appearance | asos | asos-catelyn-07.md:75 | Lame Lothar at the feast — "Lame Lothar said something amusing to Ser Hosteen" — establishes Lothar physically present in the hall during the feast | S134 RW-lens2 |
| open | food | asos | asos-catelyn-07.md:17 | Red Wedding feast menu — leek soup, green beans/onions/beets, river pike in almond milk, cold mashed turnips, jellied calves' brains, stringy beef leche — "poor fare to set before a king" | S134 RW-lens2 |
| open | quote | asos | asos-arya-11.md:45-46 | "Dead. Do you think they'd slaughter his men and leave him alive?" — the Hound tells Arya her brother is dead; Arya's first knowledge | S134 RW-lens2 |

---

## Summary

**Counts:** 11 actionable NEW_EDGE proposals (E1–E3, E4rev, E5, E6, E7-alt, E8, E9, E10, E12, E14) + 1 UNSURE (E15) + 1 harvest-only (E5-first/E7-witness retracted on gate-fail).

**3 highest-value proposals:**

1. **E1 + E2 (Lothar Frey as planner):** The Epilogue is the only place the Red Wedding's operational architecture is named on-page. Lothar rigged the tents, planted the crossbowmen, and plotted with Roose — but currently has no event-hub role edges. This is the single biggest gap in the conspiracy tier.

2. **E8 (The Rains of Castamere as massacre signal):** The song node has zero edges. It is the operational trigger — played from both castles simultaneously to signal the attack. AGENT_IN on the red-wedding hub is the most consequential single edge this node could receive.

3. **E4rev (Catelyn WITNESS_IN robb-is-killed):** Catelyn is the POV character who watches Roose kill her son. Her witnessing of Robb's death is the emotional and narrative core of the chapter, yet she has no WITNESS_IN edge on that beat. Adds both structural completeness and query value (who witnessed the king's murder?).
