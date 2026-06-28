# Fresh-Verify Report: A2.5 WO5K-Battles (S163, PASS 1)

Verifier: independent fresh-verify subagent (no prior context)
Date: 2026-06-28
Sources read: candidates.json, agot-catelyn-08.md, agot-catelyn-09.md, agot-catelyn-10.md, agot-catelyn-11.md

---

## A. CAUSAL SPINE (E1–E4)

### E1 — `battle-on-the-green-fork ENABLES battle-in-the-whispering-wood`
**CONFIRM**

Quote check (cat-08:151): "When Lord Tywin gets word that we've come south, he'll march north to engage our main host, leaving our riders free to hurry down the west bank to Riverrun."

The quote is a verbatim contiguous substring of line 151 and matches candidates.json exactly. Robb's plan laid out explicitly: foot + Bolton march the kingsroad as a feint (the Green Fork engagement draws Tywin north), while cavalry cross the Twins and fall on Jaime. ENABLES is correct — Tywin's response to the Green Fork attack was a free choice; the battle opened the window but did not force Robb's cavalry attack. PRECEDES already exists (temporal); this is the causal precondition. Tier-2 is appropriate (Robb's stated plan, not witnessed outcome).

### E2 — `battle-in-the-whispering-wood ENABLES battle-of-the-camps`
**CONFIRM**

Quote check (cat-10:135): "You may have lopped the head off the snake, but three quarters of the body is still coiled around my father's castle."

Verbatim match confirmed. Catelyn's metaphor makes the causal logic explicit: capturing Jaime ("the head") removes the commander of the three besieging camps ("the body"), which are now leaderless. The Blackfish had already established that Jaime's outriders were eliminated (cat-10:31: "those that saw us did not live to tell of it"), so the camps are also blind. ENABLES is correct — the Wood created the precondition (leaderlessness + lost scouts), but Robb still had to choose and execute the three-camp assault. Strongest link in the spine. CONFIRM.

### E3 — `battle-of-the-camps ENABLES robb-proclaimed-king-in-the-north`
**CONFIRM**

Quote check (cat-11:143): "Word of the victory at Riverrun had spread to the fugitive lords of the Trident, drawing them back."

Verbatim match confirmed. The text makes the causal logic explicit: the twin victories (Whispering Wood + Camps) re-assembled the northern lords and "fugitive lords of the Trident" at the Riverrun war council. It was this assembled audience that the Greatjon then moved to proclaim Robb king (cat-11:209–215). The proclamation text shows lords like Blackwood, Bracken, Mallister — river lords who "had never been ruled from Winterfell" — rising to declare, which is only possible because the Camps victory had gathered them at Riverrun. 

Coexistence with `execution-of-eddard-stark CAUSES robb-proclaimed-king-in-the-north` is clean and non-duplicative: Ned's execution supplied the grievance/motive; the Camps victory supplied the military momentum that gathered the audience. Both are necessary, neither is sufficient. ENABLES (precondition, not cause) is correct. CONFIRM.

### E4 — `siege-of-riverrun ENABLES battle-of-the-camps`
**CONFIRM (with note)**

Quote check (cat-10:35): "There is no other way to besiege Riverrun, yet still, that will be their undoing."

Verbatim match confirmed. The Blackfish is explaining, before the battle, why the rivers' geography *forces* Jaime's host into three separate camps — and that this dispersal "will be their undoing." The chain is explicit in the text: three rivers → three camps → sequential vulnerability → the Camps assault.

**Not tautological**: the siege and the Camps assault are distinct events. The siege imposed the three-camp dispersal as a structural reality; the Camps assault then exploited that dispersal. Without the siege forcing that geometry, Lannister forces could have consolidated in a single defensible position.

**Not wrong direction**: siege-of-riverrun created the dispersal that battle-of-the-camps exploited. ENABLES is correct (precondition), Tier-3 is appropriate (inferential, no verbatim statement of the completed causal chain — only the Blackfish predicting it pre-battle).

**Note worth patching**: the candidates.json note correctly identifies E4 and E2 as "distinct (E2 = leaderlessness; E4 = geometry)." This distinction holds. The note is accurate.

CONFIRM.

---

## B. TIER-2 ROLE/SEAM EDGES (E13, E14, E22)

### E13 — `jason-mallister FIGHTS_IN battle-in-the-whispering-wood`
**CONFIRM (Tier-2 appropriate)**

Quote check (cat-10:45): "Lord Jason Mallister had brought his power out from Seagard to join them as they swept around the headwaters of the Blue Fork and galloped south."

Cat-10:83: "To east and west, the trumpets of the Mallisters and Freys blew vengeance."

Jason Mallister joined Robb's host before the battle and his forces were present and fighting at the Wood (the Mallister trumpets are explicitly part of the battle's signal-and-attack sequence at cat-10:83). His son Patrek rode in Robb's personal battle guard (cat-10:53), confirming the Mallister contingent's deep integration. Jason himself commanded the Seagard force, so FIGHTS_IN (his forces fought) is correct. No individual combat action line for Jason personally, so Tier-2 is honest. 

**Edge quote in candidates.json** is "Lord Jason Mallister had brought his power out from Seagard to join them" — verbatim match at cat-10:45. CONFIRM.

### E14 — `theon-greyjoy FIGHTS_IN battle-in-the-whispering-wood`
**CONFIRM (Tier-2 appropriate, with note)**

Cat-10:53: Theon Greyjoy is explicitly named as one of Robb's battle guard ("Theon Greyjoy, no less than five of Walder Frey's vast brood"). He rode into the fight with Robb.

Cat-10:101: "A mob of men followed him up the slope, dirty and dented and grinning, with Theon and the Greatjon at their head."

Cat-11:117: Theon is recounting the battle in first person: "we rode out of the darkness with sword and lance." The first-person plural "we rode out" places Theon among the attackers. The "I saw him tear one man's arm" refers to Grey Wind (not Theon killing), but Theon is describing events he participated in.

The candidates.json note cites "kills men in the battle (ACOK)" — this is wiki/ACOK-derived, not from these chapters. The AGOT book text supports Theon as a battle guard member who charged with Robb and survived, but no individual kill is stated in these four chapters. Tier-2 is the right call: present and fighting per battle guard assignment + first-person "we rode out," but no book-text combat kill act in AGOT.

**Edge quote** is "with Theon and the Greatjon at their head" — verbatim at cat-10:101 (post-battle, not mid-combat). This is acceptable for presence/participant evidence; the battle guard membership (cat-10:53) is the stronger combat-role citation. Note in candidates.json should reference cat-10:53 as the primary cite, with cat-10:101 as corroborating.

CONFIRM. **Note patch**: recommend adding cat-10:53 as primary evidence cite ("Theon Greyjoy" named in Robb's battle guard).

### E22 — `gawen-westerling VICTIM_IN battle-in-the-whispering-wood`
**CONFIRM (Tier-2 appropriate)**

Quote check (cat-10:137): "Lord Westerling, Lord Banefort, Ser Garth Greenfield, Lord Estren, Ser Tytos Brax, Mallor the Dornishman…" — named in Theon's list of captives "taken close to a hundred knights captive, and a dozen lords bannermen."

Context: Theon is speaking immediately after the Whispering Wood battle in the same chapter (cat-10). The battle-of-the-camps is off-page in cat-11 (Lord Hoster says "last night, when it began" at cat-11:63, referring to the Camps attack as a prior event). So this captive list is unambiguously from the Whispering Wood, not the Camps.

Entity resolution: "Lord Westerling" = the lord of House Westerling = Gawen Westerling. AFFC affc-jaime-05:101 explicitly names "Lord Gawen Westerling" as the adult lord of House Westerling, confirming the resolution. No other Westerling lord is named in AGOT. Tier-2 (name-resolution inference) is honest.

The candidates.json correctly notes this as a PASS-2 seam: Gawen's capture eventually brings Robb to the Crag. CONFIRM.

---

## C. SPOT-CHECK TIER-1 EDGES (3 sampled)

### E16 — `jaime-lannister KILLS torrhen-karstark`
**CONFIRM**

Cat-10:133: "he took Torrhen's hand off" — verbatim. Cat-10:129: Robb confirms "Torrhen and Eddard. And Daryn Hornwood as well" as dead. Unambiguous Tier-1. CONFIRM.

### E12 — `maege-mormont AGENT_IN battle-in-the-whispering-wood`
**CONFIRM**

Cat-10:77: "Here was the call of Maege Mormont's warhorn, a long low blast that rolled down the valley from the east, to tell them that the last of Jaime's riders had entered the trap." — verbatim. Maege's signal-horn was the literal trigger for the trap. AGENT_IN is correct (not FIGHTS_IN — she acted as the trigger, not a front-line combatant in the text). CONFIRM.

### E9 — `brynden-tully COMMANDS_IN battle-in-the-whispering-wood`
**CONFIRM**

Cat-10:31: "Robb had given the Blackfish three hundred picked men, and sent them ahead to screen his march." — verbatim. The Blackfish commanded the screen that blinded Jaime's outriders and set the lure. COMMANDS_IN is correct. CONFIRM.

---

## D. BUG-DROP ADJUDICATIONS

### Bug 1: `roose-bolton CAPTURES jaime-lannister`
**DROP — CONFIRMED**

Cat-09:257: "The larger part of the northern host, pikes and archers and great masses of men-at-arms on foot, remained upon the east bank under the command of Roose Bolton. Robb had commanded him to continue the march south, to confront the huge Lannister army coming north under Lord Tywin."

Roose Bolton was on the EAST bank of the Green Fork with the foot host, ordered to march south toward Tywin Lannister. He was not with the cavalry that crossed the Twins and went to the Whispering Wood. There is zero textual basis for Roose Bolton capturing Jaime. The correct event: Robb's cavalry (west bank force) captured Jaime at the Whispering Wood, with jaime-lannister VICTIM_IN (E8) being the correct reification. DROP confirmed.

### Bug 2: `catelyn-stark CAPTURES jaime-lannister`
**DROP — CONFIRMED**

Cat-10:87: "Catelyn sat on her horse, unmoving, with Hal Mollen and her guard around her, and she waited... She was high on the ridge, and the trees hid most of what was going on beneath her."

Catelyn remained on the ridge, protected by Hal Mollen's guard of 30 men, throughout the battle. She explicitly could not see the fighting ("she could not claim she had seen the battle," cat-10:93).

Cat-10:101: "Between them [Theon and the Greatjon] they dragged Ser Jaime Lannister. They threw him down in front of her horse." Jaime was already captured and being dragged when brought to Catelyn.

Cat-10:117: "Take him away and put him in irons," Catelyn said." — This is a custody order, not a capture. She received a prisoner already taken. DROP confirmed.

### Bug 3: `robb-stark PRISONER_OF jaime-lannister`
**DROP — CONFIRMED**

This edge is directionally inverted. The book text establishes the opposite: Jaime was Robb's prisoner (captured at the Whispering Wood, put in irons per Catelyn's order, cat-10:117). Robb was never Jaime's prisoner at any point in these chapters or in the broader narrative. The correct edge `jaime-lannister PRISONER_OF robb-stark` exists separately. This triple is a factual inversion and must be dropped. DROP confirmed.

---

## SUMMARY

| ID | Verdict |
|----|---------|
| E1 | CONFIRM |
| E2 | CONFIRM |
| E3 | CONFIRM |
| E4 | CONFIRM |
| E5–E12 | CONFIRM (spot-checked E9, E12) |
| E13 | CONFIRM (Tier-2 appropriate) |
| E14 | CONFIRM (Tier-2 appropriate; note: add cat-10:53 as primary cite) |
| E15–E21 | CONFIRM (Tier-1 direct observations) |
| E22 | CONFIRM (Tier-2 appropriate) |
| bug roose-bolton CAPTURES jaime | DROP |
| bug catelyn-stark CAPTURES jaime | DROP |
| bug robb-stark PRISONER_OF jaime | DROP |

**0 edges dropped from E1-E22. All 3 pre-existing buggy edges confirmed for drop.**

The spine is clean: E1→E2→E3 form a well-supported causal chain. E4 (siege geometry) is legitimate but inferential (Tier-3 honest). The Tier-2 role/seam edges (E13, E14, E22) are supported at exactly the evidence level claimed. The Tier-1 KILLS/VICTIM_IN/COMMANDS_IN/AGENT_IN edges are directly verbatim-supported.
