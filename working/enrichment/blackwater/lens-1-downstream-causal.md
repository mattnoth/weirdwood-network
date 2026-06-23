# Lens 1 — Downstream-Causal / Consequence
# Battle of the Blackwater enrichment dip (S138)
# Generated: 2026-06-23

> Lens mandate: Find causal/consequence structure the spine lacks — off-spine causal beats
> WITHIN and immediately downstream of the battle. PROPOSE ONLY — no minting.
> Deduped against baseline.md.

---

## PROPOSED NODES

### Node A: `wildfire-trap-on-the-blackwater`

- **Slug:** `wildfire-trap-on-the-blackwater`
- **Type:** `event.battle` (a deliberate tactical operation within the battle)
- **Name:** "Wildfire trap on the Blackwater"
- **Identity:** Tyrion's pre-placed hulks filled with wildfire jars are ignited when Swordfish rams a hulk, triggering a chain of wildfire explosions that destroys most of both fleets on the Blackwater Rush.
- **Dedup check:** `ls graph/nodes/events/ | grep wildfire` → only `wildfire-plot` (the Aerys 283AC node). No Blackwater wildfire node exists. Safe to propose.
- **Outgoing causal edge that justifies it:** This event directly TRIGGERS the raising of the chain (the fleet is now burning and trapped) AND CAUSES the destruction of the fleet. It is the decisive tactical event inside the battle — not constitutive of `battle-of-the-blackwater` as a whole; it is a sub-beat with its own causal outputs.
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-davos-03.md:131:
> "With a grinding, splintering, tearing crash, Swordfish split the rotted hulk asunder. She burst like an overripe fruit, but no fruit had ever screamed that shattering wooden scream. From inside her Davos saw green gushing from a thousand broken jars, poison from the entrails of a dying beast, glistening, shining, spreading across the surface of the river . . ."

acok-davos-03.md:135 (the ignition itself):
> "Then he heard a short sharp woof, as if someone had blown in his ear. Half a heartbeat later came the roar. The deck vanished beneath him, and black water smashed him across the face"

acok-tyrion-13.md:19 (Tyrion's POV confirms the hull-mechanism):
> "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames."

---

### Node B: `blackwater-chain-raised`

- **Slug:** `blackwater-chain-raised`
- **Type:** `event.battle`
- **Name:** "Chain raised on the Blackwater"
- **Identity:** Bronn commands the winch towers to raise the great chain boom across the mouth of the Blackwater Rush after Stannis's fleet has entered the river, trapping the burning fleet inside and preventing escape to Blackwater Bay.
- **Dedup check:** `ls graph/nodes/events/ | grep chain` → nothing. Safe.
- **Outgoing causal edge that justifies it:** CAUSES the physical destruction of the surviving fleet (ships pile up against the chain, burning). ENABLES no new military crossing for Stannis — the chain's raising is the decisive containment step that turns a wildfire attack into a complete fleet annihilation.
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-davos-03.md:145–147:
> "The chain. Gods save us, they've raised the chain.
> Where the river broadened out into Blackwater Bay, the boom stretched taut, a bare two or three feet above the water. Already a dozen galleys had crashed into it, and the current was pushing others against them. Almost all were aflame, and the rest soon would be."

acok-tyrion-13.md:27 (Tyrion's inner account of timing):
> "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep; the chain was ponderous heavy, and the great winches turned but slowly, creaking and rumbling. The whole of the usurper's fleet would have passed by the time the first glimmer of metal could be seen beneath the water. The links would emerge dripping wet, some glistening with mud, link by link by link, until the whole great chain stretched taut. King Stannis had rowed his fleet up the Blackwater, but he would not row out again."

---

### Node C: `sandor-clegane-refuses-to-sortie`

- **Slug:** `sandor-clegane-refuses-to-sortie`
- **Type:** `event.incident`
- **Name:** "Sandor Clegane refuses to lead the sortie"
- **Identity:** Sandor Clegane, terrified by the wildfire conflagration, refuses to obey Tyrion's order to lead another sortie from the King's Gate — the key moment that forces Tyrion to lead the sortie himself.
- **Dedup check:** `ls graph/nodes/events/ | grep sandor` → `sandor-cleganes-trial-by-combat` only (a later event). No "refuses" node. Safe.
- **Outgoing causal edge that justifies it:** CAUSES `tyrion-leads-sortie-at-the-kings-gate` (proposed Node D). Without Sandor's refusal there is no leadership void, no Tyrion-led sortie. The refusal is the proximate cause — Tyrion explicitly reasons through it in the text.
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-tyrion-13.md:53–57 (the confrontation):
> "No." A shadow detached itself from the shadow of the wall, to become a tall man in dark grey armor. Sandor Clegane wrenched off his helm with both hands and let it fell to the ground. [...] "Bugger that. And you."

acok-tyrion-13.md:66–67 (Tyrion registers the cause):
> "He is afraid, Tyrion realized, shocked. The Hound is frightened. He tried to explain their need. [...] 'I've lost half my men. Horse as well. I'm not taking more into that fire.'"

acok-tyrion-13.md:73 (leadership void diagnosed):
> "Without a leader, they would refuse as well, and Ser Mandon . . . a dangerous man, Jaime said, yes, but not a man other men would follow."

---

### Node D: `tyrion-leads-sortie-at-the-kings-gate`

- **Slug:** `tyrion-leads-sortie-at-the-kings-gate`
- **Type:** `event.battle`
- **Name:** "Tyrion leads the sortie at the King's Gate"
- **Identity:** Tyrion Lannister personally leads a cavalry sortie out the sally port of the King's Gate, routing Stannis's men from the battering ram and fighting along the riverfront — nearly dying in the process.
- **Dedup check:** `ls graph/nodes/events/ | grep tyrion` → no Blackwater sortie node. `a-knight-attacks-tyrion-s-shield` is a different stub (Mandon's attack). Safe.
- **Outgoing causal edge that justifies it:** ENABLES the defense of the King's Gate (the ram is driven back). Also the scene that puts Tyrion on the "bridge of ships" where Mandon Moore attempts his assassination. This node is the causal parent of the Mandon Moore attack (already stubbed as `a-knight-attacks-tyrion-s-shield`) and of Tyrion's wounding.
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-tyrion-13.md:77–88 (the decision and departure):
> "This is madness, he thought, but sooner madness than defeat. Defeat is death and shame. 'Very well, I'll lead the sortie.'"

acok-tyrion-13.md:87–88:
> "'You won't hear me shout out Joffrey's name,' he told them. 'You won't hear me yell for Casterly Rock either. This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!'"

acok-tyrion-14.md:21–23 (the charge, ram dispersed):
> "Beneath the gate men were turning, hurriedly trying to brace for the shock. Tyrion lifted his axe and shouted, 'King's Landing!' [...] The battering ram crashed down into the mud, forgotten in an instant as its handlers fled or turned to fight."

---

### Node E: `joffrey-recalled-to-the-red-keep`

- **Slug:** `joffrey-recalled-to-the-red-keep`
- **Type:** `event.incident`
- **Name:** "Joffrey recalled to the Red Keep by Cersei"
- **Identity:** Cersei orders Osfryd Kettleblack to fetch Joffrey back from the Mud Gate to the safety of Maegor's Holdfast during the battle — against the advice of Lancel Lannister and Tyrion's prior arrangement.
- **Dedup check:** `ls graph/nodes/events/ | grep joffrey` → `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` (downstream aftermath node). No "recalled" node. Safe.
- **Outgoing causal edge that justifies it:** TRIGGERS the gold cloak morale collapse (Lancel is explicit: "When they saw the king leaving, they lost all heart"). This is the decisive morale break on the defender side that nearly costs the city before Tywin's relief arrives.
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-sansa-07.md:13–14 (Lancel's diagnosis, the direct downstream morale statement):
> "Why did you have them fetch Joffrey back to the castle? The gold cloaks are throwing down their spears and running, hundreds of them. When they saw the king leaving, they lost all heart."

acok-sansa-06.md:79–82 (Cersei's order, Lancel protest):
> "'No!' Lancel was so angry he forgot to keep his voice down. [...] 'Let him stay where he is, he's the king—'"
> "'He's my son.' Cersei Lannister rose to her feet."

---

### Node F: `garlan-tyrell-routs-stannis-as-renlys-ghost`

- **Slug:** `garlan-tyrell-routs-stannis-as-renlys-ghost`
- **Type:** `event.battle`
- **Name:** "Garlan Tyrell routs Stannis wearing Renly's armor"
- **Identity:** Ser Garlan Tyrell, wearing Renly Baratheon's distinctive green armor with golden antlers, leads the relief vanguard into Stannis's rear. Former Renly supporters — who comprise much of Stannis's host — break ranks, many shouting "Lord Renly" and switching sides, deciding the battle.
- **Dedup check:** `ls graph/nodes/events/ | grep garlan` → nothing. `ls graph/nodes/events/ | grep renly` → nothing related. Safe.
- **Outgoing causal edge that justifies it:** CAUSES `stannis-retreats-to-dragonstone` (already existing node). This is the immediate on-field cause of Stannis's rout — the text identifies it as the vanguard action that "plunged through Stannis like a lance through a pumpkin." It also causes the slaying of Guyard Morrigen (a distinct downstream beat, but low enough priority that a role edge may suffice).
- **SUB_BEAT_OF:** `battle-of-the-blackwater`
- **Grounding chapter:line + verbatim contiguous quote:**

acok-sansa-07.md:145 (Dontos's account, the decisive moment):
> "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers! Lord Renly with his tall spear in his hand! They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well. It was Renly, it was Renly, it was Renly!"

acok-sansa-07.md:137 (result):
> "Lord Stannis is dead, Lord Stannis is fled, no one knows, no one cares, his host is broken, the danger's done. Slaughtered, scattered, or gone over, they say."

Bronn's account (already quoted on hub node, ASOS Tyrion I):
> "Most of Stannis's host had been Renly's to start, and they went right back over at the sight of him in that shiny green armor."

---

## PROPOSED EDGES

### E-1: `wildfire-trap-on-the-blackwater` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-tyrion-13.md:19 |
| Quote: "He saw another of the hulks he'd stuffed full of King Aerys's fickle fruits engulfed by the hungry flames." |
| Rationale: The wildfire trap is a discrete sub-event inside the battle (specific actors, specific moment of ignition) that warrants its own node for causal-graph wiring. SUB_BEAT_OF, not CAUSES, because the trap is constitutively part of the battle — but as a node it needs the parent link. |

---

### E-2: `wildfire-trap-on-the-blackwater` --TRIGGERS--> `blackwater-chain-raised`
| Tier: 2 | chapter:line: acok-davos-03.md:135 + acok-tyrion-13.md:27 |
| Quote (Davos): "Then he heard a short sharp woof, as if someone had blown in his ear. Half a heartbeat later came the roar." |
| Rationale: TRIGGERS (not CAUSES) because the chain was pre-set and Bronn raises it the moment Stannis's flagship passes — the wildfire going off is the signal to raise. The wildfire's ignition is the immediate "spark" with no decisional gap before chain-raising. Tyrion's own account confirms the sequencing: "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep." The two events are near-simultaneous and the ignition is the signal trigger. Agency-check: Bronn acts on a pre-arranged signal, so no independent free-choice mediates — TRIGGERS holds. |

---

### E-3: `blackwater-chain-raised` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-davos-03.md:145–147 |
| Quote: "The chain. Gods save us, they've raised the chain. Where the river broadened out into Blackwater Bay, the boom stretched taut, a bare two or three feet above the water." |
| Rationale: The chain-raising is a discrete command action (Bronn at the winch towers) inside the battle. SUB_BEAT_OF locates it within the parent event. |

---

### E-4: `blackwater-chain-raised` --CAUSES--> `battle-of-the-blackwater` [fleet destruction outcome]
**Alternative framing — this edge may better be expressed as a PARTICIPANT ROLE on the existing downstream edges rather than a new CAUSES edge to the hub. The chain's destruction of the fleet is part of what the battle IS. Flag for orchestrator.**

NOTE: The chain CAUSES the physical fleet destruction (ships pile into it burning), but since the hub node already captures "the fleet was destroyed" as a consequence of the battle, wiring CAUSES from `blackwater-chain-raised` → `battle-of-the-blackwater` risks constitutive-beat agency-collapse. Safer: leave the chain's consequence implicit via SUB_BEAT_OF (E-3) and add role edges for Bronn COMMANDS_IN `blackwater-chain-raised`. The orchestrator should evaluate whether a distinct "destruction of Stannis's fleet" event node is warranted (vs. sub-beat stubs).

---

### E-5: `sandor-clegane-refuses-to-sortie` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-tyrion-13.md:53 |
| Quote: "No." A shadow detached itself from the shadow of the wall, to become a tall man in dark grey armor. Sandor Clegane wrenched off his helm with both hands and let it fall to the ground." |
| Rationale: Discrete incident inside the battle. |

---

### E-6: `sandor-clegane-refuses-to-sortie` --CAUSES--> `tyrion-leads-sortie-at-the-kings-gate`
| Tier: 2 | chapter:line: acok-tyrion-13.md:73 + :77 |
| Quote: "Without a leader, they would refuse as well [...] 'Very well, I'll lead the sortie.'" |
| Rationale: CAUSES (mediation allowed): Sandor's refusal produces a command vacuum; Tyrion reasons through the options and concludes he must go himself. The mediation (Tyrion's decision) is light — there is no viable alternative actor named or considered. MOTIVATES would also fit (it drives Tyrion's decision), but MOTIVATES must target a character not an event. CAUSES is the right type here. Agency-check: Tyrion exercises volition in stepping up, but Sandor's refusal is the specific precipitating condition that makes Tyrion's sortie necessary — without the refusal there is no vacancy to fill. |

---

### E-7: `tyrion-leads-sortie-at-the-kings-gate` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-tyrion-13.md:88 |
| Quote: "Tyrion unsheathed his axe, wheeled the stallion around, and trotted toward the sally port." |
| Rationale: Discrete sub-battle action inside the main battle. |

---

### E-8: `tyrion-leads-sortie-at-the-kings-gate` --ENABLES--> `a-knight-attacks-tyrion-s-shield`
| Tier: 2 | chapter:line: acok-tyrion-14.md:67–71 |
| Quote: "it was only at the very last, as their fingers brushed across the gap, that something niggled at him . . . Ser Mandon was holding out his left hand, why . . . Was that why he reeled backward, or did he see the sword after all? He would never know. The point slashed just beneath his eyes" |
| Rationale: ENABLES (door-opener): Tyrion's sortie is what puts him on the bridge of ships in an isolated, exposed position. Without the sortie, Mandon has no opportunity. The assassination attempt is not a guaranteed product of the sortie (Mandon exercises his own murderous choice), so CAUSES would overclaim — ENABLES preserves Mandon's agency as the actual actor. |

---

### E-9: `joffrey-recalled-to-the-red-keep` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-sansa-06.md:81 |
| Quote: "'He's my son.' Cersei Lannister rose to her feet." |
| Rationale: Discrete command decision inside the battle context. |

---

### E-10: `joffrey-recalled-to-the-red-keep` --TRIGGERS--> `defender-morale-collapse-at-mud-gate`
**NOTE:** No existing node for "defender morale collapse." This may be too granular for a separate node — the collapse is better captured as a CAUSES edge from `joffrey-recalled-to-the-red-keep` directly to the parent battle hub, or as a role edge. Flag for orchestrator.

**Alternative cleaner formulation (avoid minting morale-collapse node):**

### E-10-alt: `cersei-lannister` --CAUSES--> `battle-of-the-blackwater` [morale collapse beat]
This doesn't require a new node but also doesn't capture the causal chain well. The cleanest graph-edge is:

### E-10-actual: `joffrey-recalled-to-the-red-keep` --CAUSES--> `stannis-retreats-to-dragonstone`
**REJECT** — too many links skipped (morale collapse → defenders break → Stannis nearly wins → Tywin arrives → Stannis retreats). The actual causal connection is too mediated for CAUSES or TRIGGERS to `stannis-retreats-to-dragonstone`.

**Recommended:** Propose `joffrey-recalled-to-the-red-keep` --CAUSES--> `battle-of-the-blackwater` [as a contributing-cause edge on the battle hub, not on a downstream node]. The battle hub's existing edges (`battle-of-the-blackwater` CAUSES downstream) already absorb the chain. Lancel's line ("they lost all heart") is the causal mechanism — but the consequence is internal to the battle's outcome, not a separate post-battle event. Wire as role/participant enrichment rather than a new node.

---

### E-11: `garlan-tyrell-routs-stannis-as-renlys-ghost` --SUB_BEAT_OF--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-sansa-07.md:145 |
| Quote: "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers!" |
| Rationale: Discrete sub-battle action — vanguard charge — inside the main battle. |

---

### E-12: `garlan-tyrell-routs-stannis-as-renlys-ghost` --CAUSES--> `stannis-retreats-to-dragonstone`
| Tier: 2 | chapter:line: acok-sansa-07.md:137 + :145 |
| Quote: "his host is broken, the danger's done. Slaughtered, scattered, or gone over, they say." |
| Rationale: CAUSES (mediation allowed): Garlan's vanguard charge, with the psychological "Renly's ghost" effect breaking former-Renly troops, is the decisive on-field cause of Stannis's rout. Stannis's retreat to Dragonstone is the immediate military consequence. The existing causal spine has `battle-of-the-blackwater` CAUSES `stannis-retreats-to-dragonstone` — this edge sharpens the attribution to the decisive sub-beat. Agency-check: Stannis chooses to retreat, but the military situation produced by Garlan's charge leaves him no alternative (his host is broken). CAUSES is the right tier — not TRIGGERS (too fast; Stannis clearly processes the situation before retreating). |

---

### E-13: `garlan-tyrell` --IMPERSONATES--> `renly-baratheon`
| Tier: 2 | chapter:line: acok-sansa-07.md:145 |
| Quote: "It was Lord Renly! Lord Renly in his green armor, with the fires shimmering off his golden antlers!" |
| Rationale: IMPERSONATES is the exact type for deliberate in-universe identity fraud — Garlan wears Renly's distinctive armor to create the "ghost" effect. The baseline notes the `impersonation-edges-redirect` rule (attach to the impersonator), and Garlan is the impersonator. This is a character→character edge, not event-sourced, so it goes directly from Garlan to Renly with the battle as context. Evidence_kind: book-pass1. IMPERSONATES is a single locked type — no NEEDS_VOCAB. |

---

### E-14: `sandor-clegane` --FIGHTS_IN--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-davos-03.md:87 |
| Quote: "Davos recognized the dog's-head helm of the Hound. A white cloak streamed from his shoulders as he rode his horse up the plank onto the deck of Prayer, hacking down anyone who blundered within reach." |
| Rationale: Sandor is active in the battle before his refusal. FIGHTS_IN is the participant role. |

---

### E-15: `bronn` --COMMANDS_IN--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-tyrion-13.md:27 |
| Quote: "Bronn would have whipped the oxen into motion the moment Stannis's flagship passed under the Red Keep" |
| Rationale: Bronn commands the winch towers (chain operation) — a specific tactical role within the battle. COMMANDS_IN is the right type (he commands the chain detail, a sub-unit). The hub's Aftermath section confirms: "Bronn, knighted as Ser Bronn of the Blackwater for commanding at the winch towers." |

---

### E-16: `imry-florent` --COMMANDS_IN--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-davos-03.md:15 |
| Quote: "Stannis Baratheon had commanded the assault on Dragonstone sixteen years before, but this time he had chosen to ride with his army, trusting Fury and the command of his fleet to his wife's brother Ser Imry" |
| Rationale: Imry Florent is fleet commander — COMMANDS_IN is the exact role. Critical for the "Imry rows past the chain" causal thread. The hub's Narrative Arc names him but no role edge exists per the baseline. |

---

### E-17: `davos-seaworth` --FIGHTS_IN--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-davos-03.md:115–117 |
| Quote: "He drew his sword and led them over the rail himself. The crew of the White Hart met them at the rail, but Black Betha's men-at-arms swept over them in a screaming steel tide. Davos fought through the press, looking for the other captain" |
| Rationale: Davos fights directly in the battle — boards White Hart. FIGHTS_IN. The spine currently has no participant role edge for Davos on the hub. |

---

### E-18: `tyrion-lannister` --COMMANDS_IN--> `battle-of-the-blackwater`
| Tier: 1 | chapter:line: acok-tyrion-13.md:11 |
| Quote: "Motionless as a gargoyle, Tyrion Lannister hunched on one knee atop a merlon. [...] He was dimly aware of the gold cloaks cheering from the hoardings." |
| Rationale: Tyrion is the overall defense commander for the King's Landing side. COMMANDS_IN. This role edge is absent from the hub per baseline. |

---

### E-19: `podrick-payne` --KILLS--> `mandon-moore`
| Tier: 1 | chapter:line: acok-tyrion-14.md:73 + acok-tyrion-15.md:141 |
| Quote (acok-tyrion-14.md:73): "And suddenly he lurched to the left, staggering into the rail. Wood split, and Ser Mandon Moore vanished with a shout and a splash."
Quote (acok-tyrion-15.md:141): [Pod] "I n-never meant to k-k-k-k-" / "Dead? You're, certain? Dead?" / "Drowned." |
| Rationale: Pod shoves Mandon Moore off the deck; Mandon drowns. KILLS is correct — Pod is the direct actor, Mandon drowns as an immediate consequence. The `a-knight-attacks-tyrion-s-shield` stub node exists but has no role edges. This KILLS edge uses the existing node as scene context but is a character→character edge: Pod KILLS Mandon. |

---

### E-20: `podrick-payne` --RESCUES--> `tyrion-lannister`
| Tier: 1 | chapter:line: acok-tyrion-14.md:75 |
| Quote: "An instant later, the hulls came slamming together again, so hard the deck seemed to jump. Then someone was kneeling over him. 'Jaime?' he croaked [...] 'Be still, my lord, you're hurt bad.' A boy's voice, that makes no sense, thought Tyrion. It sounded almost like Pod." |
| Rationale: Podrick saves Tyrion by killing Mandon Moore and tending to him. RESCUES is the exact type. Character→character edge; the battle is the scene. |

---

### E-21: `mandon-moore` --ATTACKS--> `tyrion-lannister`
| Tier: 1 | chapter:line: acok-tyrion-14.md:68–69 |
| Quote: "Ser Mandon was holding out his left hand, why . . . Was that why he reeled backward, or did he see the sword after all? He would never know. The point slashed just beneath his eyes, and he felt its cold hard touch and then a blaze of pain." |
| Rationale: ATTACKS is the correct type (Mandon strikes Tyrion; Tyrion survives). The `a-knight-attacks-tyrion-s-shield` stub exists — this edge enriches that stub's participant wiring. KILLS would be wrong (Tyrion survives). |

---

### E-22: `cersei-lannister` --SUSPECTED_OF--> `a-knight-attacks-tyrion-s-shield`
| Tier: 2 | chapter:line: acok-tyrion-15.md:97 |
| Quote: "Cersei must have paid him to see that I never came back from the battle. Why else? I never did Ser Mandon any harm that I know of. [...] Another gift from my sweet sister." |
| Rationale: SUSPECTED_OF (unproven actor → event): Tyrion believes Cersei ordered Mandon to kill him, but has no proof — it is a strong in-universe suspicion, not confirmed. This is precisely what SUSPECTED_OF is for. The stub `a-knight-attacks-tyrion-s-shield` is the target event. |

---

### E-23: `garlan-tyrell` --KILLS--> `guyard-morrigen`
| Tier: 2 | chapter:line: acok-sansa-07.md:145 |
| Quote: "They say he killed Ser Guyard Morrigen himself in single combat, and a dozen other great knights as well." |
| Rationale: KILLS. The source is Dontos's hearsay account ("they say"), so Tier-2. Garlan KILLS Guyard Morrigen during the vanguard charge. This is a Tier-2 character→character edge rooted in `garlan-tyrell-routs-stannis-as-renlys-ghost` as scene. |

---

## HARVEST

*(One-line pointers: chapter:line / kind / note. Over-capture is the goal.)*

### Food & Drink
- acok-tyrion-12.md:49 / food / Tyrion-Cersei dinner: "creamy chestnut soup, crusty hot bread, and greens dressed with apples and pine nuts"
- acok-tyrion-12.md:49 / food / same dinner: "lamprey pie, honeyed ham, buttered carrots, white beans and bacon, and roast swan stuffed with mushrooms and oysters"
- acok-tyrion-12.md:115 / food / dessert course: "blackberry tarts"
- acok-sansa-06.md:11 / drink / Cersei drinking Arbor gold during battle: "a golden vintage from the Arbor, fruity and rich. The queen was drinking heavily"
- acok-sansa-06.md:23 / food / battle-night meal: "a salad of apples, nuts, and raisins"
- acok-sansa-06.md:61 / food / battle-night: "Crabclaw pies followed the salad. Then came mutton roasted with leeks and carrots, served in trenchers of hollowed bread."
- acok-sansa-06.md:61 / behavior / Lollys gorges and vomits
- acok-sansa-06.md:61 / drink / Lord Gyles: "coughed, drank, coughed, drank, and passed out"
- acok-sansa-06.md:115 / food / final course: "goat cheese served with baked apples. The scent of cinnamon filled the hall"
- acok-tyrion-12.md:59 / food / provenance: "We have Lady Tanda to thank for the pig" — ham source/gift-as-bribe
- acok-sansa-07.md:47 / drink / battle aftermath: women "called for more wine"
- acok-tyrion-15.md:37 / medical-drink / Tyrion forced milk of the poppy via copper funnel
- acok-tyrion-15.md:92–93 / drink / Tyrion insists on wine (not poppy): "pale amber wine," drinks two cups before looking in mirror

### Physical / Clothing Descriptions
- acok-davos-03.md:39 / clothing / Davos: "a jerkin of boiled leather and a pothelm at his feet were his only armor. [...] Ser Imry and the other highborn captains did not share his view; they glittered as they paced their decks."
- acok-tyrion-13.md:53 / description / Sandor's wound: "A gash above one eye had sent a wash of blood down across the Hound's old burn scars, masking half his face."
- acok-tyrion-13.md:71 / drink / Sandor's breakdown: "Water? Fuck your water. Bring me wine." — classic Sandor/wine pairing
- acok-tyrion-14.md:13–14 / description / Mandon Moore: "his dead eyes shining passionlessly through his helm. He rode a coal-black horse barded all in white, with the pure white shield of the Kingsguard"
- acok-tyrion-14.md:37 / description / Tyrion's battle-arm: "His arm was red to the elbow, glistening in the light off the river."
- acok-tyrion-14.md:45 / description / Balon Swann: "Every bit of Ser Balon was spattered with gore and smudged by smoke. [...] Bits of brain and bone clung to [his mace's] head."
- acok-tyrion-15.md:95 / description / Tyrion's wound: "The gash was long and crooked, starting a hair under his left eye and ending on the right side of his jaw. Three-quarters of his nose was gone, and a chunk of his lip."
- acok-sansa-06.md:19 / description / Cersei at battle night: "She wore a low-cut gown of deep green velvet that brought out the color of her eyes. Her golden hair tumbled across her bare shoulders"
- acok-sansa-07.md:65–66 / description / Sandor in Sansa's bedroom: "all black and green, the blood on his face dark as tar, his eyes glowing like a dog's in the sudden glare. Then the light faded and he was only a hulking darkness in a stained white cloak."
- acok-sansa-07.md:103 / description / Sandor's stench: "a stink of sweat and sour wine and stale vomit, and over it all the reek of blood, blood, blood."
- acok-sansa-07.md:129 / description / Sandor's cloak aftermath: "She found his cloak on the floor, twisted up tight, the white wool stained by blood and fire."

### Notable Quotes (load-bearing)
- acok-tyrion-13.md:25 / quote-foreshadowing / Tyrion on wildfire: "An arrow could be aimed, and a spear, even the stone from a catapult, but wildfire had a will of its own. Once loosed, it was beyond the control of mere men."
- acok-tyrion-13.md:17 / quote / Tyrion watching: "It was a half victory. It will not be enough."
- acok-tyrion-13.md:87 / quote / Tyrion's speech to sortie: "This is your city Stannis means to sack, and that's your gate he's bringing down. So come with me and kill the son of a bitch!"
- acok-tyrion-14.md:39 / quote / battle-fever description: "You don't feel your wounds then, or the ache in your back from the weight of the armor, or the sweat running down into your eyes. You stop feeling, you stop thinking, you stop being you, there is only the fight"
- acok-tyrion-14.md:51 / quote / Tyrion to Balon Swann re: Stannis's bold men crossing: "Those are brave men. Let's go kill them."
- acok-sansa-07.md:73–74 / quote / Sandor in Sansa's room: "Don't you want to ask who's winning the battle, little bird?" / "Who?" / "I only know who's lost. Me."
- acok-tyrion-15.md:97 / quote / Tyrion's scar diagnosis: "'Most like?' His snort of laughter turned into a wince of pain. There would be a scar, to be sure. [...] It was not as if his face had ever been fit to look at."

### Foreshadowing / Thematic Beats
- acok-tyrion-13.md:15 / foreshadowing / Tyrion compares wildfire to dragonfire: "Like dragonfire. Tyrion wondered if Aegon the Conqueror had felt like this as he flew above his Field of Fire." — direct Targaryen/fire foreshadowing
- acok-tyrion-14.md:43 / poignant-detail / Knight offers gauntlet in surrender — "still had the knight's hand in it"
- acok-tyrion-15.md:13–19 / foreshadowing-like / Tyrion's dream of grey world of the dead: "My work, thought Tyrion Lannister. They died at my command." — survivor guilt, thematic weight
- acok-sansa-07.md:109–123 / notable / Sansa sings "Gentle Mother" prayer under Sandor's dagger — the one song she remembers; religious/female-agency beat
- acok-sansa-06.md:44 / observation / Cersei on Kettleblacks: "Ser Osmund had taken Sandor Clegane's place by Joffrey's side" — social-capital tracking during the battle night
- acok-davos-03.md:83 / observation / Melisandre sent to Dragonstone before battle, Stannis's decision: "Lord Bryce Caron said, 'Your Grace, if the sorceress is with us, afterward men will say it was her victory, not yours.'" — credit/legitimacy dynamics

### Hospitality / Guest Dynamics
- acok-sansa-06.md:31 / hospitality / Cersei on her "hens": "So it behooves me to give their women my protection." — guest-protection as political calculation, not warmth
- acok-sansa-06.md:57 / violence-of-hospitality / Servants caught sneaking out: Cersei orders Ilyn Payne to kill them, heads on pikes — anti-hospitality, terror-discipline
- acok-sansa-06.md:65 / hospitality-denial / Cersei refuses refugees at the castle gate: "Command them to return to their homes. If they won't go, have our crossbowmen kill a few."

---

## NOTES

### NEEDS_VOCAB: None
All proposed edge types are in the locked 170-type vocabulary. No invented types required.

### Dedup collisions / flags

1. **`wildfire-plot` vs. `wildfire-trap-on-the-blackwater`:** The baseline calls this out explicitly. My proposed node is a DIFFERENT event (ACOK 299 AC, the Blackwater hulk-trap) vs. `wildfire-plot` (AGOT flashback, Aerys 283 AC plan to burn the city). No collision — slugs are distinct, events are distinct.

2. **`a-knight-attacks-tyrion-s-shield` (existing stub):** This stub is a near-empty Plate-3 artifact. My proposed edges E-8, E-21, E-22 enrich it by adding: (a) ENABLES from the sortie node; (b) ATTACKS from Mandon to Tyrion; (c) SUSPECTED_OF from Cersei. The stub body does not preclude these — it has no existing edges.

3. **`the-antler-men-conspiracy` (existing stub):** Baseline says "wiring its participants/victims is fair game." My lens read acok-tyrion-13.md:41 (Joffrey flings the Antler Men from the trebuchets during the battle). This is a KILLS-style edge (Cersei/Joffrey EXECUTES the Antler Men) and a connection to the conspiracy node, but it falls under Lens 2 (role/participant) more than downstream-causal. Flagged for Lens 2 to pick up rather than doubling here. No causal outgoing edge from the Antler Men's execution that isn't already captured by existing nodes.

4. **Joffrey-recalled causal chain:** I flagged in E-10 that the cleanest wire is NOT a new "morale collapse" node but rather direct enrichment of the Joffrey-recall incident's causal contribution. The morale collapse is strongly implied but is internal-to-battle — it's the mechanism by which `battle-of-the-blackwater` produces `stannis-retreats-to-dragonstone`. The Joffrey-recall node (E) + Cersei as actor + Lancel as witness is the right granularity; minting a "defender morale collapse" intermediate node is not clearly worth the graph overhead unless Lens 2 or 3 has specific evidence for it.

5. **Imry Florent "rows past the chain":** The text (acok-davos-03.md:29, 37, 51) shows Ser Imry's tactics as recklessly overconfident (no probing ships, smash in headlong, four times as many ships so no need for caution). Davos explicitly identifies the trap but is overruled. However, nowhere in the text does Imry "row past the chain" as a distinct decision — the chain was NOT raised while the fleet entered (it was raised after). Imry led the fleet into a wildfire trap because he didn't detect the hulks. The "command error" was entering the river without scouting and not noticing the hulks/chain towers. A `imry-florent-command-error` node could be proposed, but the causal mechanism is complex (Imry's overconfidence → failure to scout → fleet enters trap → wildfire → chain raised → destruction). This is more a character-attribution than a discrete event with its own outgoing causal edge. The existing COMMANDS_IN edge (E-16) + DEFEATS language on the hub is sufficient without a new event node. Flagged as low-priority; deferring.

6. **Sansa as witness in Maegor's:** Sansa observes battle events (burning sky, Cersei's orders) from Maegor's Holdfast, not directly from the river. A WITNESS_IN edge for Sansa to `battle-of-the-blackwater` could be proposed, but the text is indirect — she sees the sky's reflection, not the battle itself. Deferred pending Lens 2 (role/participant) assessment.

### Uncertainty flags

- E-2 (wildfire TRIGGERS chain): The text is slightly ambiguous about whether Bronn's signal was "flagship passes" vs. "wildfire goes off." Tyrion says "the moment Stannis's flagship passed under the Red Keep" — which is before the wildfire. So the wildfire may not literally trigger the chain; the flagship's passage may be the actual signal. If so, E-2 should be revised to: `wildfire-trap-on-the-blackwater` and `blackwater-chain-raised` are near-simultaneous sub-beats of the same moment rather than sequentially caused. NEEDS orchestrator review of the exact timing.

- E-12 (`garlan-tyrell-routs-stannis` CAUSES `stannis-retreats-to-dragonstone`): The existing spine already has `battle-of-the-blackwater` CAUSES `stannis-retreats-to-dragonstone`. Adding a sub-beat CAUSES the same downstream creates a two-path DAG (sub-beat → outcome AND hub → outcome). This is probably fine for graph traversal (the sub-beat is a more precise attribution), but the orchestrator should decide if both edges are wanted.
