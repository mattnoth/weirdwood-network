---
name: "Aegon is revealed to the Golden Company"
type: event.incident
slug: aegon-revealed-to-the-golden-company
aliases: ["Aegon Targaryen revealed", "Connington reveals the prince", "the unveiling of Young Griff", "Aegon shown to the war council", "Griff reveals Aegon's identity"]
confidence: tier-1
era: war-of-the-five-kings
containers: [aegon]
pass_origin: s128-aegon-a1
node_version: 1
evidence_chapters:
  - ADWD The Lost Lord
occurred:
  ac_year: 300
  precision: year
  basis_source: book-chapter
  basis_reliability: pov-witnessed
  date_confidence: tier-2
---

## Identity

In ADWD The Lost Lord, [Jon Connington](jon-connington) ("Griff") presents the youth he has raised as his own son to [Harry Strickland](harry-strickland) and the captains of the [Golden Company](golden-company) as [Aegon Targaryen](aegon-targaryen-young-griff), firstborn son of Rhaegar and Princess Elia of Dorne — the prince long believed murdered as an infant in the Sack of King's Landing. Per the restoration plan, the child was secreted out of King's Landing by [Varys](varys) and raised in exile under the patronage of [Illyrio Mopatis](illyrio-mopatis). The unveiling converts the long-hidden conspiracy (the AGOT Varys/Illyrio plot) into an active claim: the council now has a living Targaryen to rally behind, and within the same scene it votes to sail west.

**Slug discipline:** this reveal concerns [`aegon-targaryen-young-griff`](aegon-targaryen-young-griff) (the ADWD claimant). The identity he claims — the historical infant [`aegon-targaryen-son-of-rhaegar`](aegon-targaryen-son-of-rhaegar), murdered in 283 AC — is a separate node. Whether the claimant truly *is* that infant (the Blackfyre / "mummer's dragon" question) is a gated theory, deliberately kept out of this causal map.

## Edges

(Causal/role edges live in `graph/edges/edges.jsonl`, S128 AEGON track / A1.) This reveal TRIGGERS [the Golden Company sails for Westeros](golden-company-sails-for-westeros) (the unveiling precipitates the war-council vote to invade). It is MOTIVATED upstream by [Varys](varys) — the orchestrator who shaped Aegon for rule (the AGOT `varys CONSPIRES_WITH illyrio-mopatis` dyad is the conspiracy seed). Arya Stark's witnessing of the tunnel meeting (AGOT) stays parked as a `WITNESS_IN` candidate (no causal edge — agency-collapse).

## Quotes

> "No man could have asked for a worthier son," Griff said, "but the lad is not of my blood, and his name is not Griff. My lords, I give you Aegon Targaryen, firstborn son of Rhaegar, Prince of Dragonstone, by Princess Elia of Dorne … soon, with your help, to be Aegon, the Sixth of His Name, King of Andals, the Rhoynar, and the First Men, and Lord of the Seven Kingdoms."

— Connington unveils the hidden prince to the war council. ADWD The Lost Lord, Jon Connington POV (`sources/chapters/adwd/adwd-the-lost-lord-01.md:127`)

> "Aegon has been shaped for rule since before he could walk. … Tommen has been taught that kingship is his right. Aegon knows that kingship is his duty, that a king must put his people first, and live and rule for them."

— Varys, on the conspiracy's purpose: a prince raised in secret for the throne (the seed this reveal pays off). ADWD Epilogue, Kevan Lannister POV (`sources/chapters/adwd/adwd-epilogue.md:297`)
