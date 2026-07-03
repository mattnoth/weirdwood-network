---
slug: myrcella-is-maimed-by-darkstar
type: event.incident
name: "Myrcella is maimed by Darkstar"
aliases: ["Myrcella wounded", "Myrcella maimed", "Myrcella is wounded", "Myrcella is maimed", "the maiming of Myrcella", "maiming of Myrcella", "Darkstar maims Myrcella", "Myrcella loses her ear"]
confidence: tier-1
status: minted-causal-arc-s117
minted_at: 2026-06-20T00:00:00+00:00
evidence_chapters:
  - AFFC The Queenmaker
  - AFFC The Princess in the Tower
sort_keys:
  ac_year: null
  book_order: 4
  chapter_number: 22
  chapter_label: "AFFC The Queenmaker"
  composite: null
  reading_order: "4.022"
  basis: "chapter-only"
---

# Myrcella is maimed by Darkstar

In the chaos of Areo Hotah's ambush at the Greenblood, Ser Gerold Dayne — Darkstar —
turns his sword not on the prince's guardsmen but on the very princess the plot meant
to crown. He had argued at Shandystone that the surest way to start a war was to kill
Myrcella, not crown her; in the ambush he acts on it. He slashes at her head meaning
to take off the top of her skull, but her horse shies at the last instant, so the
blow instead opens her cheek to the bone and slices off her right ear. Maester
Caleotte saves her life, but her face is ruined forever. Darkstar flees into the deep
sand and is not caught. He is explicitly *not* the plot's betrayer — his strike was
sabotage to force the war Arianne never wanted, the deliberate maiming of a child
under Dornish protection.

## Quotes

> "...it would appear that her horse shied away from his at the last instant, else he would have taken off the top of the girl's skull. As it is, the slash opened her cheek down to the bone and sliced off her right ear. Maester Caleotte was able to save her life, but no poultice nor potion will ever restore her face."

— [Doran Martell](doran-martell) to [Arianne Martell](arianne-martell) on what Darkstar did to Myrcella, AFFC The Princess in the Tower (`sources/chapters/affc/affc-the-princess-in-the-tower-01.md:169`)

> Ser Gerold drew his sword. It glimmered in the starlight, sharp as lies. "This is how you start a war. Not with a crown of gold, but with a blade of steel."

— [Gerold Dayne](gerold-dayne) "Darkstar" foretelling the maiming at Shandystone, AFFC The Queenmaker (`sources/chapters/affc/affc-the-queenmaker-01.md:91`)

> Myrcella was on the ground, wailing, shaking, her pale face in her hands, blood streaming through her fingers.

— [Arianne Martell](arianne-martell) witnessing the maimed [Myrcella Baratheon](myrcella-baratheon) amid the ambush, AFFC The Queenmaker (`sources/chapters/affc/affc-the-queenmaker-01.md:291`)

## Notes
Minted S117 (2026-06-20) — the maiming of Myrcella, AFFC smoke-test fumble #4 (the
foreshadowed "Myrcella maimed" event). `event.incident`. Triggered by the ambush;
Darkstar's war-aim is his agency (captured in the node body + AGENT_IN role edge, not
a MOTIVATES edge, since MOTIVATES targets an actor). Distinct event from
`areo-hotah-springs-the-ambush` (Hotah's action) — this is Darkstar's act within it.
See worklog S117.
