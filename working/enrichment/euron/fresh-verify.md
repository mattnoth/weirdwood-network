# Fresh-Verify Adjudication — S157 Kingsmoot/Euron Enrichment Dip
**Adjudicator:** independent fresh-verify agent  
**Date:** 2026-06-27  
**Edges reviewed:** 37 (7 flagged `verify:true` + glance at all)  
**Chapters read:** affc-the-iron-captain-01, affc-the-drowned-man-01, affc-the-reaver-01, affc-the-krakens-daughter-01, affc-the-prophet-01

---

## FLAGGED EDGES (verify:true)

### E3 — `euron COMMANDS_IN taking-of-the-shields`
**Verdict: CONFIRM**

The text is decisive. Reaver-01:67: "Euron had sent Torwold Browntooth and the Red Oarsman up the Mander with a dozen swift longships, so the lords of the Shield Islands would spill forth in pursuit." Reaver-01:57: "Where was he? Back on Oakenshield, lazing in a castle." Euron devised the entire tactical plan (the decoy fleet, the timed assault on the depleted islands, sailing into the evening sun to evade the beacons) but was NOT personally present during the assault. COMMANDS_IN (orderer-not-present) is the precisely correct type. Victarion has BOTH AGENT_IN (boards and fights) AND COMMANDS_IN (directs the fleet action from Iron Victory) — that dual assignment for Victarion is also sound; Euron gets COMMANDS_IN only.

---

### E15 — `aeron OFFICIATES kingsmoot-on-old-wyk`
**Verdict: CONFIRM**

Drowned-man-01:37: "When the Damphair raised his bony hands the kettledrums and the warhorns fell silent, the drowned men lowered their cudgels, and all the voices stilled." He opens by reciting the liturgy ("We were born from the sea, and to the sea we must return"), announces the crown vacancy, repeatedly calls the formula "Who shall be king over us?", blesses Victarion's brow with seawater (drowned-man-01:101: "Brother, give me blessing… Aeron uncorked his waterskin and poured a stream of seawater down upon his brow"), and controls the floor throughout. This is unambiguously performing the ritual role, not merely attending. OFFICIATES is genuinely distinct from his AGENT_IN (general participant role). Confirmed.

---

### E17 — `cragorn AGENT_IN kingsmoot-on-old-wyk`
**Verdict: CONFIRM (identity link is sound)**

The question is whether the kingsmoot hornblower (drowned-man-01:147-159) is identifiable as Cragorn, named only in reaver-01:243-247.

Drowned-man-01:147: "It was one of Euron's mongrels winding the call, a monstrous man with a shaved head." Line 159: "the muscles in his chest twitched... the glyphs were burning brightly... blood and blisters upon the lips of the man who'd sounded it." Reaver-01:243-247 (Euron to Victarion in private): "Cragorn's died, you know. / 'Who?' / 'The man who blew my dragon horn. When the maester cut him open, his lungs were charred as black as soot.'"

The identity link is sound: there is only one person in the text who blew Dragonbinder. The reaver-01 passage is Euron naming him post-hoc and reporting his death from the charred-lung consequence described at the kingsmoot itself. No ambiguity — there is no competing candidate. AGENT_IN is correct. Tier-1 is defensible given the explicit cross-chapter referent.

---

### E32 — `eurons-mongrel-sons CREW_OF silence`
**Verdict: ADJUST — Tier-2 is correct, but the node-identity claim is weaker than the note implies; add a clarifying note**

Iron-captain-01:43-44: "On her decks a motley crew of mutes and mongrels spoke no word as the Iron Victory drew nigh. Men black as tar stared out at him, and others squat and hairy as the apes of Sothoros." This is the Silence's crew.

The node `eurons-mongrel-sons` is motivated by reaver-01:223-225: "One of Euron's mongrel sons stood behind him, a boy of ten with woolly hair and skin the color of mud" (delivering a message at the feast), and reaver-01:265: "Baseborn mongrels, born of whores and weepers." The word "mongrels" appears in both the crew description and in Euron's own characterization of his bastard sons, but the textual conflation is loose. The Silence's "mutes and mongrels" crew description encompasses far more than just his bastard sons — men black as tar, ape-like creatures from Sothoros, plus actual mutes (who can't be the same as mere bastard sons). The bastard-son messenger at the feast is one instance of a mongrel-son in context, but conflating the entire `eurons-mongrel-sons` node with the Silence crew (as if the crew node = his bastard sons) over-collapses two overlapping but distinct groups.

**Adjust:** Keep the edge at Tier-2 but change the note to: "The Silence is crewed by 'a motley crew of mutes and mongrels' (iron-captain-01:43). The node eurons-mongrel-sons captures Euron's bastard sons who appear to serve aboard and run his errands; the crew is broader (mutes, exotic foreigners) but his bastard sons are part of it. Tier-2 reflects that the node is a subset of the actual crew rather than fully coextensive."

---

### E33 — `euron MANIPULATES hotho-harlaw via_bribe`
**Verdict: CONFIRM**

Drowned-man-01:195: "Then it was Hotho Harlaw the priest heard, as he filled his hands with gold. Gorold Goodbrother shouted out as well…" The sequence is clear: Euron's mutes pour his gold before the captains; Hotho specifically "fills his hands" with it and immediately shouts Euron's name. This is transactional vote-purchase. The petyr MANIPULATES nestor via_bribe precedent is apt — a willing bribe-taker is still being manipulated instrumentally toward a political outcome by the briber. The "manipulation" framing is the standard graph interpretation for this edge type; the note's Tier-2 caveat (the "willing" angle is interpretive) is appropriate and honest. CONFIRM.

Note: the krakens-daughter-01:231 adds context — "the Crow's Eye has been buying friends at every hand" — consistent with the same pattern.

---

### E34 — `kingsmoot-on-old-wyk MOTIVATES victarion-greyjoy`
**Verdict: CONFIRM**

Iron-captain-01:27: "But when the Damphair's summons came, the call to kingsmoot, then all was changed. Aeron speaks with the Drowned God's voice, Victarion reminded himself, and if the Drowned God wills that I should sit the Seastone Chair… The next day he gave command of Moat Cailin to Ralf Kenning and set off."

This is textbook MOTIVATES: the kingsmoot-event (via its summons) is what breaks Victarion's prior stasis and directly causes his departure from Moat Cailin. The agent's note that it "routes Victarion's decision through the event" is correct but that is exactly what MOTIVATES is for (event→character causal influence). Tier-2 is appropriately cautious. CONFIRM.

---

### E37 — `euron AGENT_IN burning-of-the-lannister-fleet`
**Verdict: CONFIRM at Tier-2 (do NOT drop; the agency dispute itself is evidence)**

Iron-captain-01:265-267: Victarion says "With mine own hands I flung the first torch onto his flagship." Asha replies: "The Crow's Eye hatched the scheme."

The meta-note has it right: this is shared agency with contested credit. Victarion as executor (E36, Tier-1, book-proven) and Euron as planner (E37, Tier-2, Asha's claim) are compatible and both warranted. Asha's attribution is not an untrustworthy source — she is presenting this as established family history ("they talk only of the Crow's Eye… the way he burnt Lord Tywin's fleet at Lannisport"). Euron AGENT_IN at Tier-2 accurately captures plan-level agency; the contested-credit dispute is part of the Victarion-Euron grievance layer (already in the node prose, not an edge). The evidence is strong enough for Tier-2 AGENT_IN. CONFIRM.

---

## NEGATIVE CONTROLS

### Drop of `taking-of-the-shields CAUSES anarchy-in-the-reach`
**Verdict: DROP WAS CORRECT**

The node `anarchy-in-the-reach` (if it exists) is a wiki-stub for the Gardener-era historical Reach anarchy (long before AFFC). The AFFC consequence of the taking-of-the-shields is Tyrell mobilization and Reach hostility — an event correctly handled in node prose rather than minted as a separate event node conflated with the historical name. The drop was correct.

---

### Theory-gate check
**Verdict: CLEAN — no theory-gated edges were minted**

- E31 `euron OWNS dragonbinder`: note explicitly states "The Valyria-theft / Joramun=Horn provenance reading stays node-prose, GATED." The edge itself is pure possession, Tier-1, supported by drowned-man-01:185: "That horn you heard I found amongst the smoking ruins that were Valyria." No theory assertion embedded.
- E16 `dragonbinder WIELDED_IN kingsmoot-on-old-wyk`: captures the sounding-event only (supported by drowned-man-01:147-159). No dragon-binding efficacy or Joramun claim asserted.
- No edge asserts Euron↔Bloodraven connection, the dusky-woman's identity, or Euron-as-eldritch-herald.
- Theory-gate is clean.

---

### E35 — `victarion KILLS victarion-greyjoys-third-wife`
**Verdict: CONFIRM**

Iron-captain-01:269: "He put a baby in her belly and made me do the killing." The confession is direct and unambiguous — Victarion acknowledges killing her himself, at Balon's implicit command (to avoid kinslaying Euron). The edge targets Victarion's own act only; the note correctly keeps Euron's culpability (seduction/rape ambiguity) in node-prose rather than a separate edge. Tier-1 is justified.

---

## GLANCE AT REMAINING EDGES (non-flagged)

All 30 non-flagged edges were spot-checked against the chapter text. Brief findings:

- **E1/E2** (Victarion AGENT_IN + COMMANDS_IN taking-of-the-shields): Reaver-01 throughout. Solid.
- **E4** (victarion-slays-multiple-defenders SUB_BEAT_OF taking-of-the-shields): Reaver-01:21, 37-43. Correct de-islanding.
- **E5** (LOCATED_AT shield-islands): Reaver-01:69. Correct.
- **E6** (harras-harlaw AGENT_IN): Reaver-01:163 ("The Knight took Grimston by himself"). Correct.
- **E7** (nute-the-barber AGENT_IN): Reaver-01:21 ("Nute the Barber send a throwing axe"). Correct.
- **E8** (torwold-browntooth AGENT_IN): Reaver-01:67 ("Euron had sent Torwold Browntooth and the Red Oarsman up the Mander"). Correct — decoy participation counts.
- **E9** (ragnor-pyke AGENT_IN): Reaver-01:21 ("glimpsed Ragnor Pyke in his rusted mail") + :53 ("He gave the captured ship to Ragnor Pyke"). Correct.
- **E10-E13** (Euron APPOINTS four shield-lords): Reaver-01:181. Exact text present. Correct.
- **E14** (kingsmoot LOCATED_AT naggas-hill): Drowned-man-01:19. Correct.
- **E16** (dragonbinder WIELDED_IN kingsmoot): Drowned-man-01:147-159. Correct.
- **E18-E20** (Gylbert, Erik, Dunstan AGENT_IN kingsmoot): Drowned-man-01:57, 73, 91. Each makes explicit claim. Correct.
- **E21** (dunstan-drumm WIELDS red-rain): Drowned-man-01:91. Correct.
- **E22-E23** (Qarl, Tristifer PARTICIPATES_IN kingsmoot): Drowned-man-01:117. Named as Asha's champions. Correct.
- **E24** (baelor-blacktyde PARTICIPATES_IN kingsmoot): Drowned-man-01:35. Present in the crowd, shouts for Asha at :137. Correct.
- **E25** (rodrik-harlaw UNCLE_OF asha-greyjoy): Krakens-daughter-01:15 ("her favorite uncle"). Maternal uncle confirmed (Alannys Harlaw's brother). Correct.
- **E26** (rodrik-harlaw ADVISES asha-greyjoy): Krakens-daughter-01:143 ("do not sail into this storm"). Correct.
- **E27** (rodrik-harlaw PARTICIPATES_IN kingsmoot): Drowned-man-01:135 ("shouted Rodrik the Reader"). Correct.
- **E28** (rodrik-harlaw ALLIES_WITH asha-greyjoy): Krakens-daughter-01:99 ("I sent the summons. In your name"). Correct.
- **E29** (euron CAPTAIN_OF silence): Reaver-01:199 ("I have taken the Silence on longer voyages than this"). Correct.
- **E30** (victarion CAPTAIN_OF iron-victory): Reaver-01:53 ("clambered back up onto his own Iron Victory"). Correct.
- **E31** (euron OWNS dragonbinder): Drowned-man-01:185. Correct; possession-only.
- **E36** (victarion AGENT_IN burning-of-the-lannister-fleet): Iron-captain-01:265 ("With mine own hands I flung the first torch"). Correct.

**One minor observation — E24, baelor-blacktyde:**  
The note mentions "Euron later executes him for it." This is correct (reaver-01:97: "Euron's mutes and mongrels had cut him into seven parts") but this is the Reaver chapter *after* the kingsmoot, not a minted edge. No over-assertion in E24 itself. The execution isn't wired as a separate edge in this dip — that's acceptable (out of scope for this unit), and shouldn't be added now without a separate deliberate decision.

---

## SUMMARY

| Verdict | Count | Edge IDs |
|---------|-------|----------|
| CONFIRM | 36 | E1–E16, E17–E31, E33–E37 |
| ADJUST | 1 | E32 |
| REJECT | 0 | — |

**ADJUST detail:**
- **E32** (`eurons-mongrel-sons CREW_OF silence`): Keep at Tier-2. Update the note to clarify that the node represents a subset of the Silence crew (Euron's bastard sons appear among the crew) rather than being coextensive with the full "mutes and mongrels" crew description. The edge relationship itself is sound; the note as written implies tighter identity than the text proves.
