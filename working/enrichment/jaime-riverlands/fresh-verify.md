# Fresh-Verify Audit — S159 Jaime/Riverlands Enrichment
Reviewer: fresh-verify-s159 (independent subagent, did not propose these edges)
Date: 2026-06-27
Chapters read: affc-jaime-06.md, affc-jaime-07.md, asos-jaime-09.md

---

## Per-Edge Verdicts

| ID | Type | Verdict | Reason |
|----|------|---------|--------|
| E1 | AGENT_IN | CONFIRM | affc-jaime-07:39 — Edmure "hauling down the direwolf of Stark in token of surrender" confirmed verbatim. |
| E2 | COMMANDS_IN | CONFIRM | affc-jaime-06:325 — Quote ("If I speak the command, my coz will bridge your moat") captures Jaime's command authority over the siege apparatus. The quote cites his threat rather than the act of surrender, but the COMMANDS_IN role is fully earned — he is the siege commander who coerced the yield. |
| E3 | LOCATED_AT | CONFIRM | Riverrun as the site of the surrender is unambiguous. |
| E4 | SUB_BEAT_OF | CONFIRM | affc-jaime-07:39 — "In the confusion of the castle changing hands" establishes the surrender as the resolving beat within the siege. Not redundant with E5 (SUB_BEAT_OF = structural membership; ENABLES = causal precondition — different semantic layers). |
| E5 | ENABLES | CONFIRM | affc-jaime-06:325 — Edmure confronted with "the ladders, the towers, the trebuchets, the rams" as the precondition making surrender his only option. ENABLES not CAUSES correctly models the coerced free choice. Gives siege-of-riverrun its first causal downstream. E4 and E5 coexist without incoherence. |
| E6 | MANIPULATES via_threat | CONFIRM | affc-jaime-06:325 — "I'll send him to you when he's born. With a trebuchet." The text does not establish this as a bluff — Jaime had the siege engines and the disposition to use them; Edmure yielded because he believed it. MANIPULATES via_threat is the right type (coercive threat, not deception). |
| E7 | ENABLES | CONFIRM | affc-jaime-07:167 — "By the next morning little remained of the Frey encampment but flies, horse dung, and Ser Ryman's gallows." Jaime ordered the torch in direct response to Daven asking what to do with the siege equipment after the Freys broke camp post-surrender. The causal chain (surrender → siege ends → Freys depart → question of materiel disposal → torch order) is present in the text. ENABLES is loose but honest. |
| E8 | AGENT_IN | CONFIRM | affc-jaime-07:37 — "My uncle is a strong swimmer. After dark, he pulled himself beneath the spikes." The Blackfish executes the escape. |
| E9 | AGENT_IN | CONFIRM | affc-jaime-07:37 — "We raised the portcullis on the Water Gate. Not all the way, just three feet or so." Edmure explicitly confesses to deliberately arranging the escape mechanism. He is an AGENT, not a bystander. Hidden-agency finding is correct. |
| E10 | LOCATED_AT | CONFIRM | affc-jaime-07:39 — "a black fish in a black river floating quietly downstream" — escape originates at Riverrun. |
| E11 | SUB_BEAT_OF | CONFIRM | affc-jaime-07:39 — "it had been the next morning before Jaime had been informed that the Blackfish was not amongst the prisoners" — escape is a beat within the siege's resolution. |
| E12 | ENABLES | ADJUST (note only) | affc-jaime-07:39 — The surrender provided cover/confusion, but the escape mechanism was PRE-PLANNED: Edmure raised the gate BEFORE hauling down the direwolf banner ("waited most of the day before hauling down the direwolf" implies the gate was already raised). ENABLES is still defensible — the confusion of the castle changing hands extended the window for undetected escape — but this is ENABLES-as-cover-window, not ENABLES-as-physical-precondition. Note patched to reflect this. |
| E13 | PARTICIPATES_IN | CONFIRM | affc-jaime-07:45 — "Ser Addam Marbrand was leading the search on the south side of the river." Correct first event-role edge for addam-marbrand. |
| **E14** | SUSPECTED_OF | **REJECT** | affc-jaime-07:45 — "Vance and Piper and their ilk were more like to help the Blackfish escape than clap him into fetters." This is Jaime's internal monologue expressing diffuse CLASS distrust, not a specific suspicion that Karyl Vance committed or abetted this escape. "Their ilk" signals the thought is about riverlords-in-general, not a pointed accusation. Crucially: Edmure confessed HE arranged the escape (Water Gate), the garrison "swore they knew nothing" and Jaime believed them (affc-jaime-07:199), and there is no textual signal of riverlord involvement. SUSPECTED_OF on a named individual requires more pointed suspicion than "this class of person would tend to help." Drop. |
| **E15** | SUSPECTED_OF | **REJECT** | Same passage, same reasoning as E14. Clement Piper is named alongside Vance in a general distrust-of-riverlords thought, not as a specifically suspected actor in this escape. Drop. |
| E16 | AGENT_IN | CONFIRM | affc-jaime-07:295 — "Put this in the fire." Jaime orders the letter burned. |
| E17 | LOCATED_AT | CONFIRM | affc-jaime-07:291 — "Jaime read it in the window seat, bathed in the light of that cold white morning." The scene is at Riverrun. |
| E18 | ENABLES | CONFIRM | affc-jaime-07:291 — The letter's content ("Come at once, she said. Help me. Save me.") is a plea from captivity (relayed by Qyburn). Cersei's imprisonment by the Faith is the upstream event that produced this desperate plea to Jaime. ENABLES is correct: the captivity is the precondition; Cersei writing and Qyburn relaying are the intermediate free acts that produce the letter Jaime receives. Cross-arc seam is honest. |
| E19 | VICTIM_IN | ADJUST (note only) | affc-jaime-07:291-295 — Cersei is not physically present; she is the absent sender whose plea is refused and burned. The harm is real (her situation is worsened by Jaime's non-response), but VICTIM_IN is being used for an absent party suffering the effect of a refusal rather than direct harm from the event itself. The edge is borderline-defensible but its schema use should be noted. Note patched to flag this. Tier-2 is appropriate. |
| E20 | NEGOTIATES_WITH | CONFIRM | affc-jaime-06 — "I'll return your nephew in exchange for them." The drawbridge parley is clearly a negotiation scene; NEGOTIATES_WITH fills a genuine gap (no jaime↔blackfish edge existed). The outcome (Blackfish's contemptuous refusal) is correctly not an edge. |
| E21 | REFORGED_INTO | CONFIRM | asos-jaime-09:283 — "had Ice melted down and reforged. There was enough metal for two new blades. You're holding one." Exact quote. |
| E22 | REFORGED_INTO | CONFIRM | asos-jaime-09:283 — Same passage establishes two blades from Ice; Widow's Wail is the twin. Quote approximation ("There was enough metal for two new blades") is valid. |
| E23 | GIFTED_TO | CONFIRM | asos-jaime-09:271 — "so the blade is wasted on me. Take it." The gift scene is unambiguous. The naming of Oathkeeper and the Catelyn-vow purpose are fully textual. |
| E24 | OWNS | CONFIRM | asos-jaime-09:271 — "Now it appears I have, so the blade is wasted on me." Jaime acknowledges possession before the gift. |

---

## Theory-Leakage Check

No Jaime-as-valonqar edges or prophetic-as-fact assertions found. No TWOW material. The _meta.note correctly flags both as gated to node-prose only.

---

## Structural Observations (for orchestrator hand-apply)

- **E14 and E15 DROPPED** — not in `drop` note_patch, they are in `drop` list.
- **E12 and E19 ADJUSTED** — note-only changes; no type or tier change required. Both remain ENABLES/VICTIM_IN at tier-2.
- No pre-existing bug_drop or bug_repoint issues found.

---

## Final Counts

- CONFIRM: 19 edges (E1–E13, E16–E18, E20–E24; including E19 which is adjusted note-only and kept)
- ADJUST (note-only): 2 edges (E12, E19)
- REJECT: 2 edges (E14, E15)
- Total reviewed: 24 edges
