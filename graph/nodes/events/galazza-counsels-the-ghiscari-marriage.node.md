---
name: "Galazza Counsels the Ghiscari Marriage"
type: event.incident
slug: galazza-counsels-the-ghiscari-marriage
aliases:
  - "Green Grace counsels the marriage"
  - "Galazza urges Dany to wed a Ghiscari king"
  - "the Green Grace's marriage counsel"
confidence: tier-1
era: current-narrative
containers: [essos]
occurred:
  ac_year: 300
  precision: year
  basis_source: narrative-prose
  basis_reliability: primary-source
  date_confidence: tier-2
  narrative_first: "adwd-daenerys-04"
pass_origin: curator-causal-arc-s121
node_version: 1
sort_keys:
  ac_year: 300
  book_order: null
  chapter_number: null
  chapter_label: null
  composite: "0300.0.000"
  reading_order: null
  basis: "year-only"
---

## Identity

The counsel of Galazza Galare, the Green Grace of Meereen, that Daenerys take a husband of old
Ghiscari blood to secure her rule (ADWD, Daenerys IV) — and her brokering of Hizdahr zo Loraq
specifically. This is the **proximate cause of the Hizdahr marriage**: it answers *why Hizdahr, why a
Ghiscari king at all*, where Dany's own internal drivers (the Sons-of-the-Harpy killings, the siege)
answer *why marry*.

The graph previously routed the marriage off a single `sons-of-the-harpy-kill-twenty-nine TRIGGERS
wedding` edge. That over-claimed immediacy (weeks of deliberation, the Green Grace's brokering, and an
explicit ninety-day bargain sit between the killings and the wedding) and implied a single spark when
the marriage is genuinely **many-to-one** (a convergence hub): the insurgency + the external siege +
the Green Grace's counsel + Dany's pragmatism. The TRIGGERS was dropped (S121); the killings' role is
carried honestly by the existing `sons-of-the-harpy-kill-twenty-nine MOTIVATES daenerys-targaryen`, and
this node supplies the proximate external cause.

## Participants

- **Galazza Galare** (the Green Grace) — `AGENT_IN` (the counsellor; she urges the Ghiscari marriage and
  brokers Hizdahr).

## Edges

- CAUSES → wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen (Tier-2)
- MOTIVATES → daenerys-targaryen (Tier-2; the counsel drives Dany's decision to take a Ghiscari king)

## Quotes

> "The Green Grace says that I must take a Ghiscari king," she said, flustered. "She urges me to wed the
> noble Hizdahr zo Loraq."
>
> —Daenerys, relaying the Green Grace's counsel (ADWD, Daenerys IV, adwd-daenerys-04.md:279)

> The Green Grace has the right of that. I need a king beside me, a king of old Ghiscari blood. Elsewise
> they will always see me as the uncouth barbarian who smashed through their gates...
>
> —Daenerys adopting the counsel's reasoning (adwd-daenerys-04.md:171)

## Flagged (not minted)

A second convergence cause — the Yunkish/external besiegers' explicit demand that Dany wed and crown
Hizdahr as the price of peace ("they would see us wed", adwd-daenerys-06.md:161) — is a real additional
`CAUSES` into the wedding, but its node mapping is murky (`second-siege-of-meereen` is the post-flight
siege). Left for the Essos enrichment pass.
