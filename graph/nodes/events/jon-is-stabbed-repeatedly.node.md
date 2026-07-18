---
slug: jon-is-stabbed-repeatedly
type: event.incident
name: "Jon is stabbed repeatedly"
aliases: ["the assassination of Jon Snow", "the Night's Watch mutiny against Jon Snow", "Jon Snow is stabbed", "For the Watch"]
confidence: tier-1
era: war-of-the-five-kings
containers: [north, jon]
merged_from: mutiny-at-castle-black
wiki_source: "https://awoiaf.westeros.org/index.php/Mutiny_at_Castle_Black"
status: merged-s126
node_version: 2
evidence_chapters:
  - ADWD Jon XIII
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
sort_keys:
  ac_year: 300
  book_order: 5
  chapter_number: 70
  chapter_label: "ADWD Jon XIII"
  composite: "0300.5.070"
  reading_order: "5.070"
  basis: "year+chapter"
---

# Jon is stabbed repeatedly

> **Merge note:** This node absorbs the former `mutiny-at-castle-black` wiki node (now a `same_as` redirect). "Jon is stabbed repeatedly" and the "Mutiny at Castle Black" are the same ADWD Jon XIII event; this is the canonical survivor — it carries the curated role-edge structure (Jon VICTIM_IN; Bowen Marsh / Wick Whittlestick AGENT_IN; BETRAYS edges; LOCATED_AT Castle Black) and is the NORTH-container hard terminus. The tier-1 wiki Origins prose was ported here from the redirect.

## Identity

The mutiny at [Castle Black](castle-black): the assassination of Lord Commander [Jon Snow](jon-snow) by officers of the Night's Watch. Weeks after [Stannis Baratheon](stannis-baratheon) departs for [Winterfell](winterfell), Jon receives a taunting [letter](bastard-letter) purportedly from [Ramsay Bolton](ramsay-snow), addressed to "Bastard," which claims Stannis has been defeated and [Mance Rayder](mance-rayder) captured, and demands hostages and fealty. Jon reads it in disgust, relinquishes command of an impending ranging to [Hardhome](hardhome), and announces in the Shieldhall that he will ride south against the Boltons — asking wildlings and black brothers alike to join him of their own volition rather than ordering it. As he leaves the hall, [Bowen Marsh](bowen-marsh), Wick Whittlestick, and other conspirators fall on him with daggers, weeping "For the Watch." The stabbing is the NORTH container's hard terminus; what follows is TWOW territory and is deliberately not modeled here.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`. Upstream: the [Pink Letter](pink-letter-delivered) TRIGGERS this mutiny (Tier-2 — Jon's Shieldhall march announcement is the specific spark); the accumulating grievances that motivate the conspirators route through [Bowen Marsh](bowen-marsh) via MOTIVATES edges from the [Slynt execution](execution-of-janos-slynt) and the [free-folk decree](jon-allows-free-folk-through-the-wall) — a deliberate agency-preserving topology, NOT a blunt event→event CAUSES into the stabbing. Roles: [Jon Snow](jon-snow) VICTIM_IN; [Bowen Marsh](bowen-marsh) + Wick Whittlestick AGENT_IN; LOCATED_AT [Castle Black](castle-black).)

## Quotes

> Then Bowen Marsh stood there before him, tears running down his cheeks. "For the Watch." He punched Jon in the belly. When he pulled his hand away, the dagger stayed where he had buried it.

— The mutiny: Bowen Marsh delivers the fatal blow. Jon POV, ADWD Jon XIII (`sources/chapters/adwd/adwd-jon-13.md:323`)

## Foreshadowing

Melisandre warned Jon Snow directly in the Shieldhall exchange weeks earlier:

> "Ice, I see, and daggers in the dark. Blood frozen red and hard, and naked steel. It was very cold."

— Melisandre to Jon Snow, ADWD Jon I (`sources/chapters/adwd/adwd-jon-01.md:321`) — direct foreshadowing of this event; she specifies "daggers in the dark" (the conspirators attack from behind/ambush) and "ice" (the Wall setting). Tier-1 cite.

## Notes
Survivor of the S126 `mutiny-at-castle-black` → `jon-is-stabbed-repeatedly` merge (N4 of the NORTH spine build). Origins prose ported from the tier-1 wiki node; the redirect's lone junk PRECEDES edge (`battle-on-the-green-fork PRECEDES …`, a bogus cross-year chronology artifact) was dropped at merge.
