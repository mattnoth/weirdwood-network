# defiance-of-duskendale — Structural Attachment Notes

**Hub:** `defiance-of-duskendale` (event.battle, ~277 AC)
**Date produced:** 2026-06-15
**Starting edge count:** 0 outgoing, 0 incoming

## Attachment summary

| Edge type | Count |
|-----------|-------|
| LOCATED_AT | 1 |
| VICTIM_IN | 7 (aerys-ii-targaryen, dontos-hollard, serala-of-myr, jon-hollard, robin-hollard, house-darklyn, house-hollard) |
| AGENT_IN | 2 (barristan-selmy, denys-darklyn) |
| COMMANDS_IN | 1 (tywin-lannister) |
| **Total** | **11** |

## Evidence split

| Kind | Count |
|------|-------|
| Book-grounded tier-1 (verbatim chapter quote) | 4 |
| Wiki-only tier-2 | 7 |
| **Total** | **11** |

## Book-grounded edges (tier-1)

- **LOCATED_AT → duskendale** — adwd-the-queensguard-01.md:109 (Barristan reflection on Duskendale rescue)
- **VICTIM_IN aerys-ii-targaryen** — adwd-the-kingbreaker-01.md:69 (Barristan recalls bringing "queen's father safely out of Duskendale, where he was being held captive by a rebel lord")
- **AGENT_IN barristan-selmy** — asos-jaime-08.md:33 (Kingsguard White Book record: "Brought King Aerys II to safety during the Defiance of Duskendale, despite an arrow wound in the chest.")
- **COMMANDS_IN tywin-lannister** — adwd-the-kingbreaker-01.md:27 (Barristan recalls Tywin's ultimatum: "He had first heard those words from Tywin Lannister outside the walls of Duskendale. He gave me a day to bring out Aerys.")

## PART_OF decision

No `PART_OF` edge emitted. The Defiance of Duskendale (~277 AC) is a standalone political incident, not a named war. It predates Robert's Rebellion by ~5 years and is not a battle of any established war node in the graph. No PART_OF is warranted.

## Unresolved participants (named, no node found)

None — all named participants resolved to existing nodes.

## Deliberately skipped participants

- **Brienne of Tarth** — mentioned only as someone to whom the story is recounted in AFFC; she was not a participant.
- **Rhaegar Targaryen** — mentioned only as a hypothetical consequence ("Prince Rhaegar would have ascended the Iron Throne"). Not a participant in the event.
- **Cersei Lannister** — mentioned only as a hypothetical marriage prospect in Aerys's paranoid reasoning. Not a participant.
- **Rhaella Targaryen** — mentioned only as someone Aerys grew mistrustful of afterward. Not a participant in the event itself.

## Notes on edge type assignments

- **denys-darklyn**: typed AGENT_IN (not VICTIM_IN) because he was the instigator who took Aerys captive, making him the primary active agent despite his subsequent execution. His execution is captured by house-darklyn VICTIM_IN.
- **aerys-ii-targaryen**: typed VICTIM_IN because he was the captive/imprisoned king — the central victim role of the event, even though he survived.
- **dontos-hollard**: typed VICTIM_IN because the Defiance resulted in his family's annihilation and his own reduction to a jester; he survived only by extraordinary mercy.
- **house-darklyn** and **house-hollard**: house-level VICTIM_IN edges added because the collective attainder is the most notable outcome for the houses as entities, and specific named members (denys-darklyn, jon-hollard, robin-hollard, serala-of-myr) each carry their own edges.
