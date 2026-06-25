# Fresh Verification — Bran / Greenseer Arc Enrichment (S146)

**Verifier:** Independent fresh-verifier (no proposal access before this run)
**Date:** 2026-06-25
**run_id:** bran-enrichment-s146
**Method:** Direct chapter-file reads for every `verify:true` edge + all 4 post_verify_modifications. Quotes existence confirmed; this pass judges whether they MEAN what the edge claims.

---

## Verdict Table

| candidate_id | Verdict | Change (if ADJUST) | Reasoning |
|---|---|---|---|
| GD1 | CONFIRM | — | acok-bran-05:77 quote exact. Named drowned men (Alebelly, Septon Chayle, Mikken) all die in the sack. Jojen is the source, the sack is the target. DREAMS_OF correct, T1 correct (Jojen explicitly states this is a green dream he had). |
| GD2 | ADJUST | COLLAPSE: retire GD2; add `containers: [bran, wo5k]` tag to GD1 instead | acok-bran-05:81 quote is real ("In the dark of night the salt sea will flow over these walls") but it is Jojen's CONTINUATION of the same dream disclosure to Bran, not a structurally separate reader-facing signal. FORESHADOWS is a reader-facing edge type; the quote is in-world prophecy speech, not authorial foreshadowing. The DREAMS_OF edge (GD1) already captures the dream and its named victims. Adding a FORESHADOWS edge on the next sentence of the same speech is a double-count. DREAMS_OF covers the reader-facing function here — Jojen stating it aloud IS the gun being loaded for the reader. Collapse to GD1 only. |
| GD3 | CONFIRM | — | acok-bran-04:79 exact. "I dreamed of a winged wolf bound to earth with grey stone chains … It was a green dream, so I knew it was true." The winged wolf = Bran; the chains = his broken/unawakened condition; the crow pecking = Bloodraven trying to reach him. Fulfilled at arc terminus when Bran becomes a greenseer. DREAMS_OF, T1, target `bran-becomes-a-greenseer`: all correct. |
| GD4 | ADJUST | COLLAPSE: retire GD4; GD3 is sufficient | acok-bran-04:93 — "The crow sent us here to break your chains" — is Jojen's INTERPRETATION of the same dream, delivered two sentences later in the same passage. It is in-world speech, not a distinct predictive signal. FORESHADOWS for a reader-facing edge should be anchored in authorial technique, not a character's interpretive commentary. GD3 captures the dream; GD4 is redundant. T2 (vs GD3's T1) correctly reflects its interpretive nature, but the edge type is wrong for this quotation. Collapse — retire GD4. |
| GD5 | ADJUST | Change target from `robb-receives-false-news-of-brans-death` → `sack-of-winterfell` (or `theon-sacks-winterfell`); keep T2 | acok-bran-05:169 is real: "he was skinning off your faces with a long red blade." The dream is literally subverted: Reek (the Bastard's man, actually Ramsay Bolton) does NOT kill Bran and Rickon — the burned boys are miller's sons. The face-skinning image relates to Ramsay's subsequent actions in the sack context, not to Robb receiving false news. The false-news event is downstream of the sack deception; the DREAM points at the threat to Bran/Rickon during the sack, not at Robb's reaction to it. The subversion (miller's boys substituted) means the target should be the sack/deception event, not Robb's reception of news. Mis-targeted. T2 is correct (subverted dream, interpretive link). |
| GD6 | CONFIRM | — | acok-bran-05:177 is real: "I saw you and Rickon in your crypts, down in the dark with all the dead kings and their stone wolves." This IS a distinct second dream in the same conversation — GD5 is the face-skinning/Reek dream (line 169), GD6 is the crypts-survival vision (line 177). Jojen presents them sequentially as separate things he saw. DREAMS_OF `bran-and-rickon-survive-the-sack-in-the-crypts`, T1 (Jojen calls it a green dream and it literally happens). Do not collapse with GD5. |
| PR3 | CONFIRM | — | acok-bran-04:79: "It was a green dream, so I knew it was true." Jojen uses greensight to distinguish his prophetic dreams from ordinary dreams. Luwin independently calls it "greensight" (noted in the proposal). PRACTICES `greensight`, T2 is correct — the text does not call Jojen a "greenseer" (that title is reserved for the full tree-merged form), but he clearly practices the ability. T2 is appropriately hedged. |
| BR1 | CONFIRM | — | adwd-bran-03:45: "Never fear the darkness, Bran" is real and contextually correct. Bran is on his weirwood throne in the cave; Bloodraven (Lord Brynden) is delivering sustained instruction on greenseer practice — how to slip his skin, fly as raven, go into the roots. The full chapter shows weeks/months of this tutelage. TUTORS is the right type (stronger than TEACHES per the schema: one-on-one sustained magical mentorship). T1 is correct (explicitly described training in the text). |
| BR2 | ADJUST | Upgrade to T1 | adwd-bran-03:119: "Lord Brynden drew his life from the tree" is Leaf's statement directly to Bran (read in context: "Lord Brynden drew his life from the tree, Leaf told them"). The roots growing through his flesh are visually described in adwd-bran-02:193 in graphic detail (burrowing through thigh, emerging from shoulder). This is not interpretive — Leaf states it outright and the physical description confirms it. The bond is a T1 canon fact (stated twice, from two different angles). BONDED_TO is the right type for the root-fusion. Upgrade T2 → T1. |
| CF2 | ADJUST | Change type TEACHES → no edge (REJECT) | adwd-bran-03:25: "Most of him has gone into the tree" is Leaf EXPLAINING BLOODRAVEN'S CONDITION to the group, not teaching Bran a skill or discipline. Reading the full chapter, Leaf's communications with Bran are: (1) describing the singers' nature, (2) explaining Bloodraven's condition, (3) administering the weirwood paste ceremony. None of these is sustained didactic instruction; they are informational disclosures. The schema TEACHES implies a teacher-student relationship with deliberate skill transfer. Leaf answers questions and delivers contextual exposition. This is closer to REVEALS_TO or just prose context. Recommend REJECT — the CF2 edge overstates the relationship. The existing MEMBER_OF edge (CF1) is clean; nothing new is needed here for Leaf→Bran. |
| ME2 | CONFIRM | — | adwd-bran-02:113: "driving her frog spear deep into the wight's back" is exact. Meera directly intervenes to save Bran-in-Hodor's-body from a wight that had grabbed him. This is a discrete, acute rescue event, distinct from the ambient PROTECTS dynamic. RESCUES is the right type (point-in-time acute intervention). T1 (explicitly narrated). |
| HO1 | CONFIRM | Add as SECOND edge (distinct, do NOT collapse to existing cite) | adwd-bran-02:111: "suddenly he was Hodor" is exact. The combat warging at the cave approach is a qualitatively different event from the asos-bran-03 weirwood-pool instance: (1) it occurs under mortal threat, (2) Bran forcibly seizes Hodor against his resistance ("Hodor would curl up and hide"), (3) Bran wields Hodor's sword and decapitates a wight. The existing cite is the first/practice instance; this is the first combat instance. A SECOND edge on the same source→type→target relationship is justified when the new instance is notably distinct in context and stakes. Keep both. The existing edge supports the *pattern*; the new one supports the *escalation*. |
| RV1 | CONFIRM | — | adwd-bran-01:211: Coldhands answers Meera's "who is this three-eyed crow?" with "A friend. Dreamer, wizard, call him what you will. The last greenseer." Coldhands is the source, Meera is the recipient. REVEALS_TO is the right type for this identification. T2 is correct (partial disclosure — the NAME Brynden is not yet given; only the title "last greenseer"). |
| RV2 | CONFIRM | — | adwd-bran-03:19: "the name she gave me at her breast was Brynden" — Bloodraven's direct self-disclosure of his true name to Meera (who had asked). This is the explicit, T1-level identity revelation. REVEALS_TO `meera-reed`, T2 feels slightly conservative — this is a first-person name disclosure, which is T1. ADJUST: upgrade T2 → T1. |
| SB1 | CONFIRM | — | adwd-bran-02:91: "All around him, wights were rising from beneath the snow" — the wight ambush is clearly a sub-beat within the cave-arrival arc (same chapter, same journey-leg, same participants). SUB_BEAT_OF `bran-reaches-the-cave-of-the-three-eyed-crow` is correct. T2 (structural/interpretive) is appropriate. De-islands a stranded event node. |

---

## Post-Verify Modifications

| modification | Verdict | Reasoning |
|---|---|---|
| RE-POINT `coldhands SERVES three-eyed-crow` → target `brynden-rivers` | CONFIRM | Identity confirmed below. The three-eyed crow IS Brynden Rivers. Coldhands serves him, not the species-concept. The original cite (adwd-bran-01:73 "taking me to the three-eyed crow") is a character referring to Bloodraven by his then-unknown alias. Correct target is the character node. |
| RE-POINT `coldhands SWORN_TO three-eyed-crow` → target `brynden-rivers` | CONFIRM | Same identity logic. The sworn-loyalty is to the person, not the species concept. |
| RETIRE `three-eyed-crow TEACHES bran-stark` | CONFIRM | The "three-eyed crow" in early dreams is the same person as Brynden Rivers. The new `brynden-rivers TUTORS bran-stark` (BR1) supersedes it with the correct source node and stronger edge type. The species node should not hold an instructional edge. |
| RETIRE `three-eyed-crow HOLDS_TITLE lord` | CONFIRM | `brynden-rivers` already holds this title correctly. Retiring the mis-pointed edge on the species node is correct. The species node being islanded is the right outcome — it represents the early-book *appearance* form, and a future cross-identity pass (not SAME_AS) can address it. |

---

## Identity Verification: Is the Three-Eyed Crow Unambiguously Bloodraven?

**Yes, unambiguously, in T1 book text.**

- adwd-bran-02:195-197: When Bran asks "Are you the three-eyed crow?", the pale lord replies: "A … crow? Once, aye. Black of garb and black of blood." He confirms he was the three-eyed crow figure from Bran's dreams.
- adwd-bran-03:19: "The last greenseer, the singers called him, but in Bran's dreams he was still a three-eyed crow. When Meera Reed had asked him his true name, he made a ghastly sound that might have been a chuckle. 'I wore many names when I was quick, but even I once had a mother, and the name she gave me at her breast was Brynden.'"

The text explicitly links: the three-eyed crow (dream form) = the pale lord in the cave = Brynden = Brynden Rivers. The adwd-bran-02 "black of garb and black of blood" confirms the Night's Watch/bastard heritage consistent with Brynden Rivers' known history. This is not interpretive; it is directly stated.

**On the crow-form nuance:** The species node `three-eyed-crow` represents the dream-apparition that appears to Bran in agot (and to Jojen via the greendreams). Once the identity is revealed in adwd, those early appearances retroactively point at the same person. The surgery (re-pointing edges from the species node to `brynden-rivers`) is correct for all four listed edges. The species node should remain as an entity representing how Bloodraven appeared to Bran before the reveal — but no living edges should live there (instructional, loyalty, or title edges belong on the character). The islanding is correct.

---

## GD1/GD2 and GD3/GD4 Recommendation

**GD1/GD2:** KEEP GD1 (DREAMS_OF, T1); RETIRE GD2. The FORESHADOWS edge on the next sentence of the same dream disclosure is a double-count. DREAMS_OF already performs the reader-facing function here — the dream is described in Bran's POV chapter and the named victims all die. No separate FORESHADOWS edge is needed.

**GD3/GD4:** KEEP GD3 (DREAMS_OF, T1); RETIRE GD4. The "crow sent us here to break your chains" quote is Jojen's interpretation of the same dream, not an independent foreshadowing signal. FORESHADOWS should anchor on a distinct textual moment (authorial planting), not a character's gloss on a dream just described.

---

## Theory-Gate Check

No gated assertions found in the verified candidates:
- No time-travel claim
- No Bran-as-architect-of-events claim (the crypt dream at GD6 only records what Jojen saw happen, not Bran causing it)
- No Jojen-paste theory invocation (weirwood paste is present in PR1/adwd-bran-03, but the edge only asserts `bran-stark PRACTICES greensight`, not the identity of the paste ingredients)
- No Hodor-origin claim (HO1 records only the combat warging event)
- No Bloodraven-manipulates-events claim (BR1 is TUTORS, not a manipulation claim)

All green dreams are cited only against textually-occurring events. Theory gate: CLEAR.

---

## Summary

**10 CONFIRM / 4 ADJUST / 1 REJECT**

Adjustments: GD2 (collapse to GD1), GD4 (collapse to GD3), GD5 (re-target from `robb-receives-false-news` to `sack-of-winterfell`), BR2 (T2→T1), RV2 (T2→T1). All four post_verify_modifications confirmed.

One rejection: CF2 (`leaf TEACHES bran-stark`) — Leaf provides contextual exposition and administers the paste ceremony but does not conduct sustained didactic instruction; TEACHES overclaims the relationship.

**Highest-priority concern:** GD5's mis-target. The "Reek skinning your faces" dream points at the Theon/sack deception, not at Robb's downstream receipt of false news. Routing it to `robb-receives-false-news-of-brans-death` misframes the causal arc — the dream is about Bran/Rickon's danger in the sack, not about Robb's information state. Re-targeting to `sack-of-winterfell` (or `theon-sacks-winterfell`) corrects this.
