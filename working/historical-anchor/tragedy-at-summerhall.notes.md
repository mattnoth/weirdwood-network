# Tragedy at Summerhall — Historical Anchor Notes

**Hub slug:** `tragedy-at-summerhall`
**Date run:** 2026-06-15
**Starting edge count:** 0 outbound, 0 inbound (fully isolated)

## Edges Produced (7 total)

| Type | Count | Notes |
|------|-------|-------|
| LOCATED_AT | 1 | summerhall (place.location — confirmed exists) |
| VICTIM_IN | 3 | aegon-v-targaryen, duncan-targaryen, duncan-the-tall |
| AGENT_IN | 1 | aegon-v-targaryen (dual role: orderer of egg-hatching attempt AND victim; both emitted per task spec) |
| ATTENDS | 2 | rhaegar-targaryen (born at scene), jaehaerys-ii-targaryen (probable attendee) |
| PART_OF | 0 | No parent war in graph for this pre-Robert's Rebellion event |

## Provenance Split

| Tier | Count |
|------|-------|
| book-pass1 tier-2 | 2 (second-hand / recalled references — no direct narration of the event itself) |
| wiki-historical-anchor tier-2 | 5 |
| tier-1 | 0 — zero on-page direct narration of the event; all book quotes are retrospective recall |

## Book Quotes Used

- **adwd-the-kingbreaker-01.md:85** — Barristan's retrospective thought: "Treason and turmoil followed, as night follows day, ending at Summerhall in sorcery, fire, and grief." Used for Aegon V VICTIM_IN (tier-2, second-hand).
- **affc-samwell-04.md:21** — Maester Aemon to Sam: "the smoke was from the fire that devoured Summerhall on the day of his birth, the salt from the tears shed for those who died." Used for Rhaegar ATTENDS (born at scene, tier-2).

## Book Quotes Found but NOT Used for Edges

- **asos-arya-08.md:77** — Ghost of High Heart: "I gorged on grief at Summerhall, I need none of yours." — Confirms witness presence of the woods witch / Ghost of High Heart, but she has no resolved node. Listed under unresolved.
- **asos-daenerys-04.md:347-349** — Dany to Arstan: "It was the shadow of Summerhall that haunted him, was it not?" / "Yes. And yet Summerhall was the place the prince loved best." — Confirms Rhaegar's connection but adds no new participant.
- **adwd-daenerys-04.md:201** — "Summerhall." The word was fraught with doom. — Atmospheric; no new edge fact.
- **asos-davos-04.md:93** — Robert's battles at Summerhall during Robert's Rebellion (Grandison/Cafferen). These are from the *battles-at-summerhall* event (Robert's Rebellion era), NOT the 259 AC Tragedy. Correctly excluded.

## Unresolved Participants (no node → skipped)

- **Maester Corso** — named in wiki (sent letter before his death), no node in graph. Skip.
- **Woods witch / Ghost of High Heart** — wiki lists as probable survivor; on-page quote in asos-arya-08. Node `ghost-of-high-heart` — not checked; if it exists, this would be a valid ATTENDS candidate. Did not emit due to wiki listing her as only "probable" and her survival being uncertain.
- **Princess Rhaella Targaryen** — wiki lists as known survivor. Slug not checked in this pass; she is a probable ATTENDS candidate if her node exists.
- **Prince Aerys Targaryen** (later Aerys II) — wiki lists as probable attendee. Slug not checked; probable ATTENDS if node exists.
- **Princess Shaera Targaryen** — wiki lists as probable attendee. No slug checked.

## Dual-Role Note (Aegon V)

Aegon V received both `VICTIM_IN` (died in the fire) and `AGENT_IN` (ordered the dragon egg-hatching attempt that caused it). The task spec explicitly asked whether both roles should be emitted if "clearly supported" — both are well-supported by wiki and book text, so both are included. Evidence quotes are different for each edge.

## PART_OF Decision

No parent war edge emitted. The Tragedy at Summerhall (259 AC) preceded Robert's Rebellion by ~23 years. It is not a battle within any named war that has a node in the graph. The War of the Ninepenny Kings followed it, but Summerhall was not part of that war.

## Edge Type for Rhaegar

`ATTENDS` is the closest fit for "born at the scene." He is not a combatant, victim, or commander — he was an infant. The spec has no "BORN_AT" edge type, so ATTENDS is used with an explanatory note in asserted_relation.
