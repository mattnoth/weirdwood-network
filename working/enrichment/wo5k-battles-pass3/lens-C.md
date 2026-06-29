# Lens C — Causal Wiring (Cross-Arc Seams)

Session: S166 · wo5k-battles-pass3 · 2026-06-28

---

## Proposed causal edges

### 1. `battle-at-duskendale ENABLES red-wedding-conspiracy`

| field | value |
|---|---|
| edge_type | `ENABLES` |
| source_slug | `battle-at-duskendale` |
| target_slug | `red-wedding-conspiracy` |
| book | ASOS |
| chapter (stem) | `asos-catelyn-04` |
| tier | Tier-2 |
| verify | true |

**Verbatim quote + line:**

> "A third of my foot, lost for Duskendale?"

— `asos-catelyn-04:91` (Robb to Catelyn, reported in free indirect style from Catelyn's recollection)

**Rationale:** ENABLES, not CAUSES. The Duskendale loss destroyed roughly one-third of Robb's infantry, materially thinning his host and making the Red Wedding betrayal militarily decisive — a small Frey/Bolton force could now overwhelm him without requiring open battle against a full northern army. But the conspiracy was a free, deliberate choice by Walder Frey and Roose Bolton; the attrition removed a deterrent, it did not force the plot. This mirrors the established karstark precedent exactly: `karstark-host-deserts-robb ENABLES red-wedding-conspiracy`. TRIGGERS and CAUSES are both too strong — neither Frey nor Bolton had to conspire just because Robb's foot was thin.

---

### 2. `fighting-at-the-fords-of-the-trident ENABLES red-wedding-conspiracy`

| field | value |
|---|---|
| edge_type | `ENABLES` |
| source_slug | `fighting-at-the-fords-of-the-trident` |
| target_slug | `red-wedding-conspiracy` |
| book | ASOS |
| chapter (stem) | `asos-catelyn-06` |
| tier | Tier-2 |
| verify | true |

**Verbatim quote + line:**

> "Two-thirds of my strength was on the north side when the Lannisters attacked those still waiting to cross. Norrey, Locke, and Burley men chiefly, with Ser Wylis Manderly and his White Harbor knights as rear guard. I was on the wrong side of the Trident, powerless to help them. Ser Wylis rallied our men as best he could, but Gregor Clegane attacked with heavy horse and drove them into the river. As many drowned as were cut down."

— `asos-catelyn-06:281` (Roose Bolton to Catelyn and Robb, at the Twins eve of the Red Wedding)

**Rationale:** ENABLES, not CAUSES. Roose's account is delivered at the Twins, just before the massacre — he is describing why his own host has arrived depleted. The riders lost at the ford (Norrey, Locke, Burley; Wylis Manderly's White Harbor knights taken captive) were Stark-loyal northern infantry: their destruction meant Robb's rearguard at the Twins was composed overwhelmingly of Dreadfort men, i.e., Bolton's own loyalists. The battle thus made the conspiracy viable in two compounding ways: it thinned the Stark-aligned host, and it placed Bolton's own unthinned troops in the rear. This is not double-counting with edge 1 — Duskendale destroyed Glover/Tallhart foot (center of the northern army), the ford fighting destroyed Stark-loyal rear guard and concentrated Bolton's loyalists. Both losses independently precondition the conspiracy.

**On whether this MOTIVATES roose-bolton:** The text strongly implies Bolton engineered the ford loss deliberately — he "delayed too long before leaving Harrenhal" (his own admission), allowing Clegane to catch the still-crossing men. But this reads as a SUSPECTED motivation rather than a stated one; it crosses into theory territory (Roose as deliberate traitor from early in the campaign). The `MOTIVATES roose-bolton` edge would be a Tier-3 causal claim at best. Recommend: leave that to the `SUSPECTED_OF` edge type (per arc-enrichment backlog precedent) rather than adding a `MOTIVATES` edge here. The cleaner spine is ENABLES→conspiracy.

---

### Adjudication: do both edges stand?

Yes. They are not double-counting. The two losses are independently grounded:

- **Duskendale** (`asos-catelyn-04:91`): "A third of my foot" — Glover/Tallhart infantry shattered by Randyll Tarly before the army ever arrived at the Twins.
- **Ford of the Trident** (`asos-catelyn-06:281`): Stark-loyal rear-guard infantry drowned/captured by Gregor Clegane, with Roose deliberately stranded on the far bank.

Both thin the host; neither subsumes the other. Keep both. They mirror the karstark edge with different mechanism and timing.

---

## Foreshadowing resolution

### Row 983 — `agot-catelyn-09:241` — the Frey marriage pact

**The text at agot-catelyn-09:241:**

> "And you are to wed one of his daughters, once the fighting is done," she finished. "His lordship has graciously consented to allow you to choose whichever girl you prefer. He has a number he thinks might be suitable."

(The full pact comes across lines 237–241; the betrothal term for Robb appears at line 241. Arya↔Elmar is at line 237: "it is agreed that she will marry Lord Walder's youngest son, Elmar, when the two of them come of age.")

**Resolution: quote-attach onto `robb-weds-jeyne-westerling`**

There is no standalone event node for the Frey crossing pact itself (the AGOT Catelyn IX negotiation). A FORESHADOWS edge (Detail→Event) would require a source node; without a "frey-marriage-pact" event node, the edge has nowhere to attach cleanly. Minting a new node is out of scope for this lens.

The right move is a `## Quotes` attachment onto `robb-weds-jeyne-westerling` — which is the exact node where the broken pact lives. This gives the verbatim foundation text (the promise that Robb will later violate) a book-chapter citation inside the node that already models the consequence.

**Proposed quote block for `robb-weds-jeyne-westerling` `## Quotes`:**

> "And you are to wed one of his daughters, once the fighting is done. His lordship has graciously consented to allow you to choose whichever girl you prefer."

— Catelyn Stark to Robb Stark, AGOT Catelyn IX (`sources/chapters/agot/agot-catelyn-09.md:241`) — the Frey marriage pact: the vow Robb swears as the price of crossing the Twins, which he later breaks by wedding Jeyne Westerling. Upgrades the node's Tier-2 wiki cite to a navigable Tier-1 book citation for the promise's origin.

**Why not a FORESHADOWS edge:**  
- `robb-stark CONTRACTED_WITH walder-frey` and `robb-stark BREAKS_VOW house-frey` are already the dyadic layer.  
- The minting instructions say do not invent new nodes (required to be the FORESHADOWS source here).  
- The quote-attach is higher value: it gives the `robb-weds-jeyne-westerling` node its origin cite (AGOT Catelyn IX) alongside the consequence quotes (ASOS Catelyn II), completing the promise→breach arc in one node.

---

### Row 999 — `asos-catelyn-02:189` — Grey Wind bares teeth at Ser Rolph Spicer

**Covered by Lens A.** Lens A is handling the `grey-wind FORESHADOWS` edge for this item. No action from Lens C.

---

## Dropped

### A. `fighting-at-the-fords-of-the-trident MOTIVATES roose-bolton`

Dropped. Roose's self-incriminating account of "I delayed too long" (`asos-catelyn-06:281`) implies calculation, but the text does not state motivation explicitly in his own words. This is the Suspected-traitor reading of Roose, which is theory-adjacent (Tier-3 at best). The `SUSPECTED_OF` edge type (per arc-enrichment backlog) is the right vehicle — not `MOTIVATES`. Left for a dedicated Roose enrichment dip.

### B. Any further battle → conspiracy ENABLES edges beyond these two

Considered: `battle-on-the-green-fork` (ACOK Tyrion early) — but that was Tywin routing Roose's force, not a loss to Robb's strength (Roose survived and kept his army largely intact). No ENABLES case.

Considered: `death-of-ser-stevron-frey-announced` — but Stevron's death (Oxcross campaign) weakened the Frey faction's internal moderating voice, which is a plausible path to Walder's vengeance being easier to execute. However, this is speculative; the text does not establish a causal link between Stevron's absence and the conspiracy's feasibility. Dropped as sequence-only trap.

### C. `battle-at-duskendale CAUSES red-wedding-conspiracy`

Dropped in favor of ENABLES. CAUSES would imply the conspiracy flows directly from the defeat; in fact it flows from the broken marriage pact (`robb-weds-jeyne-westerling TRIGGERS red-wedding-conspiracy` is already in the spine). Duskendale made the conspiracy safe to attempt, not inevitable.

### D. A direct `battle-at-duskendale ENABLES red-wedding` (skipping the conspiracy hub)

Dropped. The spine models `red-wedding-conspiracy CAUSES red-wedding`. Adding a direct arc from battle attrition to the Red Wedding event would bypass the conspiracy hub and create a confused fan-in on `red-wedding`. Wire to the conspiracy hub only, per existing architecture.
