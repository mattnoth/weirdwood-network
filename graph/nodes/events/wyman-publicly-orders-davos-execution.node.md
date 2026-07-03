---
slug: wyman-publicly-orders-davos-execution
type: event.execution
name: "Wyman publicly orders Davos's execution"
aliases: ["Lord Wyman orders the execution of Davos", "Wyman commands Ser Marlon to execute Davos", "Wyman's execution order at the Merman's Court", "lord-wyman-orders-execution"]
status: minted-plate3
minted_at: 2026-06-07T20:39:49.176195+00:00
renamed_at: 2026-06-12T00:00:00+00:00
evidence_chapters:
  - ADWD Davos III
sort_keys:
  ac_year: null
  book_order: 5
  chapter_number: 20
  chapter_label: "ADWD Davos III"
  composite: null
  reading_order: "5.020"
  basis: "chapter-only"
---

# Wyman publicly orders Davos's execution

Beat 2 of the Wyman Manderly deception arc (`wyman-manderly-stages-fake-execution-of-davos`). Immediately after publicly arresting Davos in the Merman's Court (beat 1), Wyman commands his cousin Ser Marlon Manderly to take Davos to the Wolf's Den, behead him, cut off his hands, and return head and hands before supper "with an onion in Davos's teeth." The order is theatrical, staged for Frey envoys and the Iron Throne's informants — the actual beheading (beat 3) is performed on an unnamed substitute criminal who resembles Davos, while Davos himself goes to comfortable Wolf's Den captivity and then on to Stannis as Wyman's secret envoy (ADWD Davos IV).

The order itself is real enough to satisfy witnesses; the substitution is what makes it a deception. Cited in Cersei's small-council recap (AFFC Cersei IV) as "Lord Manderly ordered the execution of the Onion Lord."

## Edges
Role edges (Wyman → COMMANDS_IN, Marlon → AGENT_IN, Davos → VICTIM_IN, Wolf's Den → LOCATED_AT) live in `graph/edges/edges.jsonl`. SUB_BEAT_OF → `wyman-manderly-stages-fake-execution-of-davos` added in the S93 restructure batch.

## Notes
Renamed S93 (2026-06-12) from `lord-wyman-orders-execution` — original slug ambiguous about whether the order or the executed body referred to Davos. The new slug names Wyman as the orderer and clarifies the deception layer attaches one level up (the parent `event.deception` hub).
