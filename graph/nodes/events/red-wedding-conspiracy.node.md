---
name: "The Red Wedding conspiracy"
type: event.conspiracy
slug: red-wedding-conspiracy
aliases: ["the-frey-bolton-conspiracy", "walder-frey-conspires-with-roose-bolton", "the-plot-behind-the-red-wedding", "the-frey-lannister-bolton-plot"]
confidence: tier-1
era: war-of-the-five-kings
containers: [wo5k]
pass_origin: s107-causal-track
node_version: 1
occurred:
  ac_year: 299
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-recall
  date_confidence: tier-2
---

## Identity

After Robb Stark breaks his marriage pact, Lord Walder Frey turns to revenge. He conspires with Roose Bolton — Robb's own bannerman, who has wed Walder's granddaughter Walda — and secures the sanction and protection of Lord Tywin Lannister, Hand of the King, to bring House Frey back to the Iron Throne's side. The plot is to lure Robb and his host to the Twins under guest right, for the wedding of Edmure Tully and Roslin Frey, and slaughter them there. Tywin later admits he countenanced the scheme while assigning public blame to Walder. This conspiracy is the covert engine that produces the Red Wedding; it is modeled as a discrete event-hub wired causally INTO the Red Wedding (not as an umbrella parent over it).

> **Note (S107):** the three role edges (Walder Frey COMMANDS_IN, Roose Bolton AGENT_IN, Tywin Lannister COMMANDS_IN) are all ASOS-chapter-grounded. Lothar "Lame Lothar" Frey (the *arranger*) and Ryman Frey were deliberately NOT added — their roles are attested only in the wiki / Merrett Frey's AFFC account, not in an ASOS POV chapter. Add them later if a fuller conspirator roster is wanted (they'd be `AGENT_IN`, evidence_kind wiki / book-pass1 from AFFC).

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S107 causal-arc track — Walder Frey COMMANDS_IN (orderer), Roose Bolton AGENT_IN (the bannerman who turns), Tywin Lannister COMMANDS_IN (Tier-2, sanction-by-protection per his own later admission); TRIGGERED by [Robb's marriage to Jeyne Westerling](robb-weds-jeyne-westerling), this conspiracy CAUSES the [Red Wedding](red-wedding) and the death of [Robb Stark](robb-is-killed). Tier-2 causal links.)

## Quotes

> "Walder Frey is a peevish old man who lives to fondle his young wife and brood over all the slights he's suffered. I have no doubt he hatched this ugly chicken, but he would never have dared such a thing without a promise of protection."

— Tywin Lannister, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:205`)

> "The blood is on Walder Frey's hands, not mine."

— Tywin Lannister, ASOS Tyrion VI (`sources/chapters/asos/asos-tyrion-06.md:203`)

## Book Citations

> Lord Walder had ordered the slaughter of the Starks at Roslin's wedding, but it had been Lame Lothar who had plotted it out with Roose Bolton, all the way down to which songs would be played.

— Merrett Frey's POV, ASOS Epilogue (`sources/chapters/asos/asos-epilogue.md:31`) — book-cite upgrade: names Lothar as the operative planner alongside Bolton (the note in Identity that Lothar's role is "wiki / AFFC only" should be re-evaluated against this ASOS Epilogue attestation)

## Foreshadowing

> One of Robb's white banners lay on the ground, and one of the knights turned his horse and trampled over the direwolf as he spurred toward the gate. Several others did the same. [...] She thought she recognized Ser Perwyn Frey [...] and his bastard half brother Martyn Rivers as well [...] Close to forty men poured out through the castle gates [...]

— The Frey riders depart Riverrun in fury, trampling Robb's white direwolf banner into the ground — the visual omen of the Frey breach that becomes the Red Wedding. Catelyn POV, ASOS Catelyn II (`sources/chapters/asos/asos-catelyn-02.md:17`)
