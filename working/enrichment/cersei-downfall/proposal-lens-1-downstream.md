# Lens 1 — Downstream-causal / consequence
# Cersei's-downfall enrichment, S140

Scope: downstream consequences of `cersei-is-stripped-and-imprisoned` (dead-end); causal wiring of
`cersei-fills-in-the-arrest-warrants` (islanded); rearming → Faith Militant downstream; new nodes.

---

## NEW NODES

### 1. `murder-of-the-old-high-septon`
- **type:** event.incident
- **one-line identity:** Osney Kettleblack murders the old High Septon by suffocation, on Cersei's order
- **anchor quote + line:** `"She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."` — affc-cersei-10.md:243
- **note:** The murder is not shown on-page; it is confessed in this scene. Osney is the actor; Cersei is the principal. This is a prequil event to the arc whose existence is confirmed here, so it is properly mintable as a referenced-event node.

### 2. `margaery-tyrell-arrested-by-the-faith`
- **type:** event.capture
- **one-line identity:** The Faith arrests Margaery Tyrell and her cousins Megga, Elinor, and Alla on charges of adultery, fornication, and treason
- **anchor quote + line:** `"Megga Tyrell and Elinor Tyrell stand accused of lewdness, fornication, and conspiracy to commit high treason. Alla Tyrell has been charged with witnessing their shame and helping them conceal it. All this Queen Margaery has also been accused of, as well as adultery and high treason."` — affc-cersei-10.md:23
- **additional anchor (confinement):** `"The little queen had been confined atop one of the Great Sept's slender towers. Her cell was eight feet long and six feet wide..."` — affc-cersei-10.md:135

### 3. `cersei-demands-trial-by-the-faith`
- **type:** event.incident
- **one-line identity:** Imprisoned Cersei resolves to demand trial by battle with Jaime as her champion, and sends word to Riverrun
- **anchor quote + line:** `"It will have to be a trial by battle. There is no other way. 'Qyburn, for the love you bear me, I beg you, send a message for me. A raven if you can. A rider, if not. You must send to Riverrun, to my brother.'"` — affc-cersei-10.md:313
- **note:** This is the closing beat of affc-cersei-10 and the hinge into ADWD. It is the direct downstream of the imprisonment.

### 4. `walk-of-atonement` *(PROPOSE as NEW if no event node exists; baseline confirms only a custom node for the custom type, not an event node)*
- **type:** event.incident
- **one-line identity:** Cersei's barefoot walk of shame through King's Landing as penance demanded by the Faith, prior to her trial
- **anchor quote:** ANCHOR IS IN ADWD, NOT IN AFFC FILES — orchestrator to confirm from ADWD source before minting. The upstream imprisonment node already exists; this event's causal parent is `cersei-is-stripped-and-imprisoned` → `cersei-demands-trial-by-the-faith`. Cannot provide an AFFC verbatim anchor for the walk itself.
- **MINT STATUS:** Do not mint without ADWD anchor confirmation.

---

## EDGES

### Downstream from `cersei-is-stripped-and-imprisoned`

**E1.** `cersei-is-stripped-and-imprisoned --[CAUSES]--> cersei-demands-trial-by-the-faith`
| Tier | 1 | affc-cersei-10.md:313 |
| quote | `"It will have to be a trial by battle. There is no other way."` |
| rationale | Cersei's imprisonment directly forces her to abandon hope of rescue and resolve on trial by battle — this is the causal outcome named in the chapter's closing pages. Distinct downstream state, not a sub-beat. |

**E2.** `cersei-is-stripped-and-imprisoned --[CAUSES]--> margaery-tyrell-arrested-by-the-faith`
| Tier | 2 | affc-cersei-10.md:23 |
| quote | `"Megga Tyrell and Elinor Tyrell stand accused of lewdness, fornication, and conspiracy to commit high treason. Alla Tyrell has been charged with witnessing their shame and helping them conceal it."` |
| rationale | The Faith's power, once used against Cersei, simultaneously traps Margaery. The two arrests are contemporaneous outcomes of the same Faith empowerment. CAUSES is appropriate because the Faith's action against Cersei and Margaery is one unified sweep — but the two are distinct captures of distinct persons. Consider CONTEMPORARY_WITH as an alternative if the orchestrator prefers to avoid the CAUSES reading of simultaneous events. |
| ALTERNATIVE | `cersei-rearms-the-faith-and-forgives-the-debt --[ENABLES]--> margaery-tyrell-arrested-by-the-faith` may be cleaner (the rearming is the structural door-opener). See E3 below. |

**E3.** `cersei-rearms-the-faith-and-forgives-the-debt --[ENABLES]--> margaery-tyrell-arrested-by-the-faith`
| Tier | 1 | affc-cersei-10.md:23 |
| quote | `"Megga Tyrell and Elinor Tyrell stand accused of lewdness, fornication, and conspiracy to commit high treason."` |
| rationale | The Faith Militant could not have arrested a queen without the restored swords Cersei gave them. ENABLES = precondition/door-opener — the rearming made this arrest structurally possible. This complements E2 without duplicating it. |

**E4.** `cersei-is-stripped-and-imprisoned --[MOTIVATES]--> cersei-lannister`
| Tier | 1 | affc-cersei-10.md:307 |
| quote | `"No." He took her hand. "Hope remains. Your Grace has the right to prove your innocence by battle. My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him."` |
| rationale | The imprisonment drives Cersei's psychological state and decisive turn toward Qyburn's secret champion. MOTIVATES targets a character (Cersei). Note: the motivation edge is the psychological engine; the trial-node (E1) carries the resulting action. |

**E5.** `cersei-demands-trial-by-the-faith --[AGENT_IN]--> cersei-lannister`
| Tier | 1 | affc-cersei-10.md:313 |
| quote | `"Qyburn, for the love you bear me, I beg you, send a message for me. A raven if you can. A rider, if not. You must send to Riverrun, to my brother."` |
| rationale | Cersei is the sole agent initiating the demand and the message to Jaime. |

**E6.** `cersei-demands-trial-by-the-faith --[ADVISES]--> qyburn`
| Tier | 1 | affc-cersei-10.md:307 |
| quote | `"No." He took her hand. "Hope remains. Your Grace has the right to prove your innocence by battle. My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him. If you will only give the command . . ."` |
| rationale | Qyburn counsels Cersei toward the trial-by-battle path, citing Robert Strong. ADVISES is the correct type. |
| note | Preferred over INFORMS: Qyburn is actively shaping her decision, not merely conveying a fact. |

### Causal wiring: `cersei-fills-in-the-arrest-warrants` (islanded)

The warrants are filled immediately after Osney's confession floors the court and before Cersei visits the sept. The causal parent is `cersei-plots-against-margaery` (she conceived the warrant machinery) + the arrest list derives from the blue-bard torture session. The most natural chain:

**E7.** `cersei-confronts-and-arrests-the-blue-bard --[ENABLES]--> cersei-fills-in-the-arrest-warrants`
| Tier | 1 | affc-cersei-10.md:77 |
| quote | `"Ser Osfryd Kettleblack arrived as the ink was drying. Cersei had written in the names herself: Ser Tallad the Tall, Jalabhar Xho, Hamish the Harper, Hugh Clifton, Mark Mullendore, Bayard Norcross, Lambert Turnberry, Horas Redwyne, Hobber Redwyne, and a certain churl named Wat, who called himself the Blue Bard."` |
| rationale | The torture of the Blue Bard produced the list of names. The bard-arrest ENABLES the warrants by providing their content. Tommen signs blank warrants (l.75: "Tommen signed them blank") and Cersei fills them with names extracted from the blue bard's confession. |

**E8.** `cersei-fills-in-the-arrest-warrants --[CAUSES]--> margaery-tyrell-arrested-by-the-faith`
| Tier | 2 | affc-cersei-10.md:93 |
| quote | `"By the time the sun went down that day, all of the accused traitors were in custody."` |
| rationale | The warrants are the operative instrument. Osfryd executes them and the accused are swept up. This wires the islanded `fills-in-the-arrest-warrants` node into the arc. Note: the Margaery-arrest node is also proposed as new (E2 above); this edge links the warrant event → that outcome. If the orchestrator prefers not to use the new Margaery-arrest node, the warrants at minimum caused arrests of 10 named men — the causal path still holds. |

### Murder of the old High Septon

**E9.** `murder-of-the-old-high-septon --[AGENT_IN]--> osney-kettleblack`
| Tier | 1 | affc-cersei-10.md:243 |
| quote | `"She's the queen I fucked, the one sent me to kill the old High Septon. He never had no guards. I just come in when he was sleeping and pushed a pillow down across his face."` |
| rationale | Osney confesses on-page to having committed this murder. |

**E10.** `murder-of-the-old-high-septon --[AGENT_IN]--> cersei-lannister`
| Tier | 2 | affc-cersei-10.md:243 |
| quote | `"the one sent me to kill the old High Septon"` |
| rationale | Osney names Cersei as principal who sent him. Tier 2 because the claim comes from a confession under duress (though the AFFC text does not suggest this confession is false — Cersei's own POV confirms she plotted the old septon's death via other means and thought of "rid myself of this High Septon just as I did the other" at line 247). SUSPECTED_OF would understate what the text supports (Cersei's own internal monologue confirms it at l.247). AGENT_IN at Tier 2 is appropriate. |
| see | affc-cersei-10.md:247: `"I'll rid myself of this High Septon just as I did the other"` — internal confirmation. |

**E11.** `murder-of-the-old-high-septon --[TRIGGERS]--> osney-kettleblack-confesses-to-high-sparrow`
| Tier | 1 | affc-cersei-10.md:231 |
| quote | `"Ser Osney shall taste of that sweet milk in the afterlife. In The Seven-Pointed Star it is written that all sins may be forgiven, but crimes must still be punished. Osney Kettleblack is guilty of treason and murder, and the wages of treason are death."` |
| rationale | Under torture, Osney's confession of the murder (not just the sex claim) is what actually unravels Cersei's plot. The High Sparrow reveals it was the murder charge that made Osney truly confess the truth about Cersei. The murder — once pried out — is what TRIGGERS the reversal. |

### Rearming → downstream Faith consequences

**E12.** `cersei-rearms-the-faith-and-forgives-the-debt --[ENABLES]--> cersei-is-captured-in-the-sept`
| DEDUP CHECK | This edge ALREADY EXISTS per baseline (outgoing from `cersei-rearms-the-faith`) — **DO NOT RE-PROPOSE.** Listed here only to note the dedup catch. |

**E13** (instead): `cersei-rearms-the-faith-and-forgives-the-debt --[CAUSES]--> margaery-tyrell-arrested-by-the-faith`
→ Already captured as E3 above (ENABLES variant). See there.

---

## HARVEST

affc-cersei-09.md:121 / food / "ham studded with cloves and basted with honey and dried cherries" — dinner before the bard arrest; also "baked apples with a sharp white cheese"
affc-cersei-09.md:231 / drink / Cersei asks Taena for wine after Blue Bard torture: "My throat is raw. Be a sweet and pour me some wine."
affc-cersei-09.md:277 / food / Tommen's breakfast: "chattering about his kittens as he dribbled honey onto a chunk of hot black bread fresh from the ovens"
affc-cersei-09.md:263 / prophecy-quote / Maggy prophecy retold by Cersei to Taena: "Tyrion is the valonqar" + "valonqar = little brother" explanation — verbatim quote starting at l.267 worth anchoring to maggy-the-frog node
affc-cersei-10.md:49 / prophecy-quote / Cersei thinks prophecy failed: "No golden shrouds, no valonqar, I am free of your croaking malice at last" — ironic beat; vivid quote for prophecy-node
affc-cersei-10.md:71 / food / Tommen "fishing for cats" with fur mouse on a string
affc-cersei-10.md:267 / food / Prison meals: "a bowl of some waterly grey gruel," "bread and fish" — starvation/contrast register
affc-cersei-10.md:305 / quote / "All my lovely dromonds. Cersei almost laughed. 'My lord father used to say that bastards are treacherous by nature.'" — on Aurane Waters's desertion; load-bearing aurane-waters characterization
affc-cersei-08.md:8 / food / No specific food but: Loras sailing news arrives; Cersei and Waters sup on "bread and cheese and a bit of boiled beef with horseradish" — affc-cersei-08.md:41
affc-cersei-08.md:145 / quote / Qyburn on Robert Strong: "What he lacks in gallantry he will give you tenfold in devotion. He will protect your son, kill your enemies, and keep your secrets, and no living man will be able to withstand him." — first on-page introduction of Robert Strong's role; load-bearing
affc-cersei-07.md:121 / quote / Cersei on Qyburn's order for Robert Strong's armor: "The armorer thinks that I am mad. He assures me that no man is strong enough to move and fight in such a weight of plate." — Robert Strong origin detail

---

## NOTES

**Walk of atonement:** Cannot anchor in AFFC chapters — the walk itself is ADWD. The node is mintable but needs ADWD source anchor. Proposed above with explicit flag. The arc's upstream (imprisonment + confession demand) is complete in AFFC; the walk is the true downstream terminus. Recommend: orchestrator reads ADWD Cersei chapters to confirm anchor before minting, then wires `cersei-demands-trial-by-the-faith --[CAUSES]--> cersei-s-walk-of-atonement`.

**`cersei-fills-in-the-arrest-warrants` causal isolation:** The warrants are the mechanism by which the Blue Bard's false testimony is converted into state action. Wired above via ENABLES (from bard arrest) + CAUSES (→ margaery arrest). The warrants chronologically occur *between* Osney's confession scene (court scene, morning) and the arrest sweep (same day). They sit contemporaneously with the capture-in-the-sept, not after it — so `cersei-fills-in-the-arrest-warrants` is a *parallel* branch of `cersei-plots-against-margaery`, not a downstream of `cersei-is-captured-in-the-sept`.

**Kevan Lannister assumes regency:** Mentioned at affc-cersei-10.md:295 — "They have dispatched a raven to Casterly Rock, inviting your uncle to return to court and assume the regency." The regency is not yet confirmed as a completed event in AFFC text (the invitation is dispatched, Kevan hasn't yet arrived). A node `kevan-lannister-assumes-regency` would be mintable but only confirmed completed in ADWD. Flagged for orchestrator — out of scope for AFFC-only anchor rule unless orchestrator accepts the ADWD completion.

**Aurane Waters deserts with the fleet:** affc-cersei-10.md:303 — "Lord Waters raised sail, unshipped his oars, and took his fleet to sea." This is a clean downstream consequence of Cersei's arrest. A node `aurane-waters-deserts-with-the-fleet` is mintable with AFFC anchor. Not proposed here (it is a side-arc departure, not directly on the Cersei-downfall spine), but flagged as high-value enrichment for a separate arc or character-unit pass.

**Murder of old High Septon timing:** The murder occurred before the current arc (it was Cersei's method of deposing the fat high septon, referenced in passing across earlier chapters). It surfaces here as the charge that breaks Cersei. It is correctly an antecedent event that TRIGGERS the confession reversal — the node is proposed because it was absent from the baseline and its existence is now causal-load-bearing.

**Qyburn + Robert Strong:** Qyburn names Robert Strong as Cersei's unbeatable champion at affc-cersei-10.md:307. This is the closest AFFC comes to confirming Robert Strong's readiness. No explicit "creation event" is shown in these chapters (the backstory is in ch07 of Cersei: "the armorer thinks I am mad"). A `qyburn-creates-robert-strong` event node would be Tier 2 (implied off-page); flagged for a future character-unit pass on Robert Strong/Gregor Clegane.

**Dedup catches:**
- `cersei-rearms-the-faith-and-forgives-the-debt --[CAUSES]--> cersei-is-captured-in-the-sept` already exists — not re-proposed.
- `osney-kettleblack-confesses-to-high-sparrow --[TRIGGERS]--> cersei-is-captured-in-the-sept` already exists — not re-proposed.
- `faith-militant-uprising` confirmed as Aenys/Maegor-era historical node — not wired.
