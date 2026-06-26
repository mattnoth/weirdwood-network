# Fresh-Verify Report — Theon Greyjoy / Reek Enrichment Dip
**Reviewer:** independent fresh-verify agent  
**Date:** 2026-06-25  
**Source:** candidates.json (run_id: theon-reek-enrichment-s149)

---

## Verdict Table

| id | edge (source -TYPE-> target) | CONFIRM / ADJUST / REJECT | reason (text-grounded) |
|----|------------------------------|---------------------------|------------------------|
| **A. Cross-identity** | | | |
| X1 | ramsay-snow IMPERSONATES reek | **CONFIRM** | Text is definitive (acok-theon-06:247): Ramsay swapped clothes with the original servant after arranging his death, then presented himself as "Reek" to be captured. IMPERSONATES is correct — he is literally passing as another named person, not merely disguising himself in a generic costume. SAME_AS would be wrong (they are distinct people). Note: the quote in the candidate file is accurate but only captures Ramsay's confession mid-sentence; the full context ("By the time they put that arrow through his back, I'd smeared myself with the girl's filth and dressed in his rags") confirms the model. |
| **B. Agency calls** | | | |
| W2 | mance-rayder AGENT_IN the-winterfell-murders | **ADJUST → SUSPECTED_OF** | The text is deliberately ambiguous. Theon says "It was you" to Holly/Rowan (adwd-a-ghost-in-winterfell-01:263), and Holly deflects with "How could it be us? We're women." This is a non-denial-denial, not an admission. The spearwives never confirm agency for Yellow Dick etc. on-page in ADWD (only Rowan confirms "he stank as bad as you. A pig of a man" re: Yellow Dick — an opinion, not an admission of killing). GRRM withholds the confirmation. Mance commands the spearwives, so he bears any guilt they bear, but the text does not confirm the murders as canon fact. AGENT_IN asserts the act; SUSPECTED_OF (Tier 2) is the correct modeling for deliberately-coy attribution. The node body's exclusion of Little Walder's murder is correct — Rowan explicitly disclaims it twice ("This was no work of ours," "That was not us. I told you"). |
| W3 | rowan AGENT_IN the-winterfell-murders | **ADJUST → SUSPECTED_OF** | Same reasoning as W2. Rowan is the spearwife who most forcefully deflects the accusation. She grabs Theon's throat when he repeats it. The text-as-written supports SUSPECTED_OF for all spearwives on the murders (excluding Little Walder, which is a clean REJECT for them). Tier 2 is appropriate. |
| W4 | theon-greyjoy SUSPECTED_OF the-winterfell-murders | **CONFIRM** | In-world suspicion is canon: Ser Aenys Frey points to Theon, Lady Dustin exonerates him on physical grounds ("Hold a dagger? He hardly has the strength to hold a spoon" — adwd-a-ghost-in-winterfell-01:183). SUSPECTED_OF never asserts the act; the in-world false accusation makes this a valid graph edge. Correct as-proposed. |
| **C. Causal / seam edges** | | | |
| F7 | trail-followed-north-northwest CAUSES theon-fakes-the-deaths | **CONFIRM** | Proximate cause is clearly on-page: the hunt fails ("Somehow Osha and the wretched boys were eluding him" — acok-theon-04:193), Reek suggests the mill, and this directly triggers the substitution killings. The failed trail is the proximate forcing condition. |
| F8 | theon-fakes-the-deaths CAUSES robb-receives-false-news | **CONFIRM (with note)** | The deception produces the false news; the candidate note is correct that this is a more proximate cause than the existing `capture-of-winterfell CAUSES robb-receives-false-news`. Flag the capture edge for review/re-point at finalize: `capture-of-winterfell` enables Theon's position to fake the deaths, but the news Robb receives is specifically about the deaths, not the capture. The candidate's note about this is sound; the capture-edge should be re-pointed or noted as over-distal for this particular downstream. |
| B1 | sack-of-winterfell ENABLES breaking-of-theon-greyjoy | **CONFIRM** | The capture-at-sack is explicitly cited by Theon ("who captured me at Winterfell" — adwd-reek-02:125). ENABLES is the right type — the sack is the enabling condition; the breaking happens later at the Dreadfort. The causal chain (sack→captured→Dreadfort→broken) is not over-distal for ENABLES; CAUSES would overstate the directness. Tier 2 appropriate given the cross-arc gap. |
| M2 | fall-of-moat-cailin ENABLES wedding-of-ramsay | **CONFIRM** | Directly supported: Roose's host passes through the cleared ruins three days after the surrender and marches north (adwd-reek-02:209). The wedding is staged at Winterfell after that march. ENABLES is correct — the fall removes the logistical block. |
| W6 | the-winterfell-murders ENABLES theon-and-jeyne-escape-winterfell | **CONFIRM** | The murders fuel the Frey-Manderly brawl; Roose sends both factions out the main gates to fight Stannis (adwd-theon-01:75: "Ser Hosteen, assemble your knights and men-at-arms by the main gates"). This depletes the interior garrison and creates the escape window Mance's plan exploits. The causal chain (murders→brawl→dispersal→diminished garrison→escape window) is supported. ENABLES is correct — the murders are not the proximate trigger of the escape itself (the brawl is), but they ENABLE the precondition. |
| E9 | theon-and-jeyne-escape-winterfell TRIGGERS pink-letter-delivered | **CONFIRM** | The pink letter explicitly demands the escaped pair back: "I want my bride back… And I want my Reek. Send them to me, bastard" (adwd-jon-13:235). The escape is the direct antecedent Ramsay names. TRIGGERS is apt — the escape causes the letter to be sent. Cross-container seam is solid. |
| S2 | wedding-of-ramsay MOTIVATES stannis-baratheon | **CONFIRM (with caution)** | Roose's strategic reasoning is directly quoted (adwd-reek-03:163): "His clansmen will not abandon the daughter of their precious Ned to such as you. Stannis must march or lose them." The MOTIVATES target is stannis-baratheon (the person), which is architecturally correct. The reasoning is Roose's inference about Stannis's motivation — but it proves accurate in-world (Stannis does march). Tier 2 is right given the inferential layer; the edge is sound. |
| S3 | theon-greyjoy-taken-as-ward MOTIVATES theon-greyjoy | **CONFIRM** | Theon himself articulates the wound in the parley scene (acok-theon-06:131): "The noose I wore was not made of hempen rope, that's true enough, but I felt it all the same. And it chafed, Ser Rodrik. It chafed me raw." First-person statement that the ward years installed the chafe that drove his need to prove himself. MOTIVATES (the person) is correct architecture. Tier 1 warranted — direct quote. |
| S1 | bolton-forces-attack CAUSES sack-of-winterfell | **CONFIRM** | The text is unambiguous: Ramsay's Dreadfort men cut down Theon's ironborn and torch the castle (acok-theon-06:261: "burn it, burn it all"). CAUSES is the right type — the attack directly produces the sack. |
| **D. Retirements** | | | |

---

## Retirements

| id | edge | verdict | reason |
|----|------|---------|--------|
| R1 | theon-greyjoy KILLS bran-stark | **SAFE-TO-DROP** | Factually false by the text. Theon explicitly reflects in the godswood that "Bran and Rickon … They were only miller's sons, from the mill by the Acorn Water" (adwd-a-ghost-in-winterfell-01:247). The killed boys are the miller's sons; Bran is alive and a POV character. The replacement modeling (`bran-stark VICTIM_IN theon-fakes-the-deaths-of-bran-and-rickon`) is precisely correct — Bran is the victim of a deception about his death, not an actual killing. Drop is correct and the replacement is the right edge. |
| R2 | wedding-of-ramsay PRECEDES wedding-of-hizdahr | **SAFE-TO-DROP** | Cross-continent chronology noise. No causal, thematic, or narrative link between Ramsay's Bolton-Stark wedding in Winterfell and Hizdahr's wedding in Meereen. Pure PRECEDES spine artifact. |
| R3 | fall-of-moat-cailin PRECEDES purple-wedding | **SAFE-TO-DROP** | Cross-book chronology noise. The Purple Wedding is a Reach/Tyrell plot against Joffrey in King's Landing; Moat Cailin is a Neck/Bolton/ironborn event. No causal or narrative connection. |
| R4 | taking-of-deepwood-motte PRECEDES purple-wedding | **SAFE-TO-DROP** | Same as R3. Cross-book chronology noise; no causal or narrative link between Stannis's Deepwood Motte action and the Purple Wedding. |

---

## Theory Leakage Sweep

No theory leakage detected. The dip is evidence-only:
- No Azor Ahai / Lightbringer claim is attached to the escape or any Theon edge.
- No TWOW-forward plot is asserted (the escape ending is the text ending — the jump; no assertion about what happens in the snow).
- The "Theon reclaims his name" beat is folded into the escape node body and is grounded in the text (adwd-theon-01:265: "Theon Greyjoy. I … I have brought some women for you" — he names himself to the guard). No redemption-prophecy framing.
- The pink-letter seam correctly routes through an existing node; no TWOW speculation appended.

## Quote Accuracy Check

All checked quotes are accurate to the source text:
- X1 quote (acok-theon-06:247): accurate.
- F7 quote (acok-theon-04:193): accurate.
- W2/W3 quote (adwd-a-ghost-in-winterfell-01:263): accurate to the godswood confrontation scene. The quote "Go on. Do me, the way you did the others. Yellow Dick and the rest. It was you" is Theon's accusation, not the women's admission — the note correctly captures this ambiguity.
- M2 quote (adwd-reek-02:209): accurate ("Three days later, the vanguard of Roose Bolton's host threaded its way through the ruins").
- W6 quote (adwd-theon-01:75): accurate ("Ser Hosteen, assemble your knights and men-at-arms by the main gates").
- E9 quote (adwd-jon-13:235): accurate. Note: the full demand is "I want my bride back… And I want my Reek. Send them to me, bastard" — the quote in the candidate is an accurate condensation.
- S2 quote (adwd-reek-03:163): accurate ("Stannis must march or lose them").
- B1 quote (adwd-reek-02:125): accurate ("who captured me at Winterfell").

Minor note: B5 (skinner PARTICIPATES_IN breaking-of-theon-greyjoy) — the candidate quote (adwd-reek-01:87: "Sour Alyn. Skinner. Yellow Dick.") lists the Bastard's Boys who are present and participate in the Dreadfort captivity apparatus. Skinner is the named flayer. PARTICIPATES_IN at Tier 2 is accurate; Skinner's flaying role is confirmed by the text (Reek knows the pain of flaying from Skinner's blade — adwd-reek-01:115 and adwd-reek-03). The quote is a name-list reference, not a direct flaying-attribution; Tier 2 is appropriate.

## Node-Alias Hygiene

**Recommendation: CONFIRM the conservative call. Do NOT add bare "Reek" to theon-greyjoy.**

Rationale: There are three distinct bearers of "Reek" in the text:
1. **Reek (I):** the original servant (the `reek` node) — this is the primary referent of bare "Reek" in ACOK.
2. **Ramsay-as-Reek:** modeled as `ramsay-snow IMPERSONATES reek` in ACOK (X1 edge).
3. **Theon-as-Reek (III):** theon-greyjoy with alias "Reek (III)" — the ADWD identity.

Adding bare "Reek" to theon-greyjoy would create a direct collision with the `reek` node's primary name, breaking alias resolution (the resolver would return two distinct nodes for the same query). The bracketed forms "Reek (III)" and "Reek (I)" are the correct disambiguation, matching GRRM's own parenthetical usage across the series. A disambiguation note in both node bodies (as specified in the candidate) handles bare-query ambiguity at the prose level without corrupting slug resolution. This is the right call.

---

## Summary

**Counts:** CONFIRM 13, ADJUST 2, REJECT 0 (retirements: 4× SAFE-TO-DROP)

**The AGENT_IN-vs-SUSPECTED_OF call for W2/W3 (mance-rayder and rowan):** ADJUST both to SUSPECTED_OF. GRRM deliberately withholds confirmation — Holly deflects ("How could it be us? We're women"), Rowan twice denies Little Walder's murder, and no spearwife ever on-page admits the Yellow Dick / Ryswell groom killings. AGENT_IN asserts the act as canon fact; SUSPECTED_OF is the correct type for deliberately-coy attribution and matches the graph's policy for unproven-but-load-bearing agency. The node body correctly excludes Little Walder from spearwife responsibility.

**R1 retire (theon-greyjoy KILLS bran-stark):** SAFE-TO-DROP. The edge is factually false — Bran is alive; Theon's own inner monologue in the godswood confirms the killed boys were miller's sons, not Starks. The replacement `bran-stark VICTIM_IN theon-fakes-the-deaths-of-bran-and-rickon` is the correct modeling.

**Systemic concerns:** None major. The causal chain edges (F7→F8, B1, M2, W6, E9) are all well-grounded in proximate text. One flag: the existing `capture-of-winterfell CAUSES robb-receives-false-news` edge should be reviewed for re-pointing or type-downgrade at finalize, since F8 (`theon-fakes-the-deaths CAUSES robb-receives-false-news`) is the more proximate cause and both cannot be equally "causes" of the same downstream node. The capture enables the position; the deception is what produces the false news content Robb receives.
