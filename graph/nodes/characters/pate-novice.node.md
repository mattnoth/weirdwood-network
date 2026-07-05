---
name: "Pate (novice)"
type: character.human
slug: pate-novice
aliases: ["Pate", "Pate the Novice"]
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Pate_(novice)"
bucket_id: characters-other-o-p
prompt_version: v1-manual
node_version: 1
pass_origin: manual-backfill-session41
---

## Identity

Pate is a novice of the [Citadel](wiki:Citadel) in [Oldtown](wiki:Oldtown), the POV character of the AFFC prologue. He arrived at the Citadel at age thirteen from the westerlands and had been there for five years at the time of his death (approximately age eighteen). He has no chain links after five years and is known by other novices as a slow learner. He tends [Archmaester Walgrave](wiki:Walgrave)'s white ravens; senile Walgrave sometimes confuses him with someone named "[Cressen](wiki:Cressen)." He is in love with Rosey, daughter of Emma the innkeeper at the Quill and Tankard.

Pate previously stole an iron key from Archmaester Walgrave's strongbox; the key opens every door in the Citadel. He arranged to sell it to a mysterious alchemist for a golden dragon — the price Emma set for Rosey's maidenhead.

## Edges

- LOCATED_AT: Citadel
- CULTURE_OF: Westermen (track_b: Culture)
- SERVES: Walgrave [tends his ravens]
- LOVES: Rosey
- KILLED_BY: alchemist [poisoned coin exchange, AFFC Prologue]
- KILLED_BY: jaqen-hghar [the alchemist is Jaqen H'ghar in disguise — Tier 2, confirmed by ADWD/TWOW signalling]
- DECEIVED_BY: alchemist [false identity, false bargain]
- DIED_AT: Oldtown [Quill and Tankard area, AFFC Prologue]

## Narrative Arc

### A Feast for Crows — Prologue

At the Quill and Tankard inn in [Oldtown](wiki:Oldtown), Pate drinks with fellow Citadel students [Mollander](wiki:Mollander), [Armen](wiki:Armen), [Alleras the Sphinx](wiki:Alleras), and [Lazy Leo Tyrell](wiki:Leo_Tyrell) and they discuss reports of living dragons in the east. Lazy Leo reveals that a glass candle is burning in [Archmaester Marwyn](wiki:Marwyn)'s chambers. After the group disperses at dawn, Pate walks through Oldtown until the mysterious alchemist he has been waiting for appears on the river road.

Pate exchanges the stolen archmaester's key for a golden dragon coin. He bites the coin to verify it is genuine; it feels warm against his palm. Shortly after the exchange, Pate collapses in an alley — his heart hammering, legs turning to water — and dies.

The alchemist is later revealed (via authorial signalling across AFFC/ADWD) to be [Jaqen H'ghar](wiki:Jaqen_H'ghar), a Faceless Man who appears to have taken Pate's face and his place at the Citadel.

## Notes

- This node was created manually in Session 41 (2026-05-11) to fill a gap in the wiki crawl. The case-insensitive macOS filesystem collapsed `Pate_(Novice)` and `Pate_(novice)` to the same disk entry; the canonical-lowercase page never landed and the cached entry is just a redirect HTML. The node content here is reconstructed from the AFFC Prologue Pass 1 extraction (`extractions/mechanical/affc/affc-prologue.extraction.md`) rather than from the wiki body, so the prose is thinner than a Stage-1 agent emission. A future re-crawl of `Pate_(novice)` would enable full prose backfill.
- The dual `KILLED_BY` edges (alchemist + jaqen-hghar) follow the impersonation-redirect rule (memory: `project_impersonation_edges_redirect.md`). Stage 4 SAME_AS work between `alchemist` and `jaqen-hghar` will collapse these naturally.

## Quotes

> Spotted Pate the pig boy was the hero of a thousand ribald stories: a good-hearted, empty-headed lout who always managed to best the fat lordlings, haughty knights, and pompous septons who beset him.

— AFFC (Prologue), `sources/chapters/affc/affc-prologue.md:129`

> But those were stories. In the real world pig boys never fared so well.

— AFFC (Prologue), `sources/chapters/affc/affc-prologue.md:129`
