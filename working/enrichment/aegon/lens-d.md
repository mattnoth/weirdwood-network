# Lens D — Existing-Node ↔ Existing-Node Causal Wiring
## AEGON / Golden Company Enrichment Pass 1 (S147)

> **Lens:** D (highest-value structural lens — cross-node causal seams no topic lens owns)
> **Scope:** `landing-of-the-golden-company` full-chain + surrounding nodes; KL endgame; greyscale sub-thread; GC founding; broken contract.
> **Method:** `graph-query.py --neighbors`, `--full-chain`, direct node reads, chapter verification.
> **Live graph verified:** 2026-06-25. Full-chain = 17 edges (matches baseline). Spine already includes `landing CAUSES siege`, `landing MOTIVATES assassinations`, `jon-connington MOTIVATES siege` — those are BUILT, confirmed below.

---

## Pre-flight: Live Spine Status (verified against graph, NOT the baseline document)

The baseline snapshot described these as "dark" — they are **already wired** in the live graph:

| Edge | Status |
|------|--------|
| `golden-company-sails-for-westeros CAUSES landing-of-the-golden-company` | **BUILT** |
| `aegon-revealed-to-the-golden-company TRIGGERS golden-company-sails-for-westeros` | **BUILT** |
| `aegon-targaryen-young-griff MOTIVATES golden-company-sails-for-westeros` | **BUILT** |
| `tyrion-lannister MOTIVATES golden-company-sails-for-westeros` | **BUILT** |
| `exile-of-jon-connington ENABLES aegon-revealed-to-the-golden-company` | **BUILT** |
| `varys MOTIVATES aegon-revealed-to-the-golden-company` | **BUILT** |
| `landing-of-the-golden-company CAUSES siege-of-storms-end-300` | **BUILT** |
| `jon-connington MOTIVATES siege-of-storms-end-300` | **BUILT** |
| `landing-of-the-golden-company MOTIVATES assassinations-of-pycelle-and-kevan-lannister` | **BUILT** |
| `varys AGENT_IN assassinations-of-pycelle-and-kevan-lannister` | **BUILT** |
| `kevan-lannister VICTIM_IN assassinations...` | **BUILT** |
| `pycelle VICTIM_IN assassinations...` | **BUILT** |
| `aegor-rivers FOUNDED golden-company` | **BUILT** |

This is good news: many baseline "dark" seams were built by other sessions or concurrent lens passes before this one. The lens-D work is to find the REMAINING structural seams those passes missed.

---

## Proposed Seams

### Seam 1 — `stone-men-attack-the-shy-maid ENABLES jon-connington` [greyscale infection]

**source --TYPE--> target:** `stone-men-attack-the-shy-maid` --`ENABLES`--> `jon-connington` [AFFLICTED_BY `greyscale` character-state]

Actually this needs two sub-edges for structural clarity:

**Edge 1a:** `stone-men-attack-the-shy-maid --CAUSES--> jon-connington` [character: greyscale condition, expressed as AFFLICTED_BY]

**The right model:** The attack is the proximate cause of Connington's greyscale infection — he contracts it by plunging into the Rhoyne to pull Tyrion up. This means:

- `jon-connington --AFFLICTED_BY--> greyscale` (character→condition edge, Tier-1)
- `stone-men-attack-the-shy-maid --CAUSES--> <greyscale-infection-of-jon-connington>` (but this requires a mint — see below)

**Agency check:** No agency-collapse here. The attack DIRECTLY causes Connington's infection: he jumps into diseased water to rescue Tyrion. The causal chain is `attack → Connington pulls Tyrion from Rhoyne → exposed to stone-men/diseased water → contracts greyscale`. No mediated decisions.

**HIT/NEW-NODE:** The simplest well-grounded seam here is:
- `jon-connington --AFFLICTED_BY--> greyscale` — **HIT** (both nodes exist; this edge is DARK — 0 AFFLICTED_BY edges exist in the entire graph)

The deeper `stone-men-attack CAUSES infection` seam **requires a NEW NODE** (`greyscale-infection-of-jon-connington`, event.incident) to model cleanly. Without the event node, the attack→greyscale path is a character→concept hop (not an event→character causal edge), which is structurally awkward. The lens-D proposal is therefore:

**Primary proposal (HIT, no mint):**
`jon-connington --AFFLICTED_BY--> greyscale`

| Tier | 1 (direct Tier-1 book evidence) |
|------|---|
| Source | `adwd-the-griffin-reborn-01.md:141` |
| Quote | "I should have let the damned dwarf drown." (internal monologue confirming he contracted greyscale by rescuing Tyrion from the Rhoyne during the stone-men attack; adwd-tyrion-06.md:21 confirms: "it was Lemore who forced the water from your lungs after Griff had pulled you up") |
| Status | HIT (both `jon-connington` and `greyscale` nodes exist; AFFLICTED_BY is in locked vocab; edge is DARK) |
| Rationale | AFFLICTED_BY is the correct type for a character's disease/condition relationship. The infection is established on-page in two Tyrion POV chapters (the attack in tyrion-05; the aftermath in tyrion-06) and Jon's own POV (griffin-reborn-01:141). No agency-collapse (Connington is the one who contracted it, not a mediated choice). |

**Secondary proposal (log for future mint, greyscale-clock seam):**

`stone-men-attack-the-shy-maid --ENABLES--> [greyscale-infection-of-jon-connington]` (NEW-NODE-NEEDED)
`[greyscale-infection-of-jon-connington] --MOTIVATES--> siege-of-storms-end-300` (death-clock haste)

The death-clock → haste seam is strong but needs the infection-event node to avoid conflating `stone-men-attack MOTIVATES siege` (agency-collapse — the attack doesn't directly MOTIVATE the siege, the *infection's* death sentence does). **Log for mint in a future step; the AFFLICTED_BY edge is the immediate deliverable.**

**Supporting quote (adwd-the-lost-lord-01.md:239):**
> "Death, he knew, but slow. I still have time. A year. Two years. Five. Some stone men live for ten. Time enough to cross the sea, to see Griffin's Roost again."

This is Connington's internal reasoning directly linking his greyscale (death-clock) to his campaign urgency — the `MOTIVATES` relationship flows from the condition (`greyscale`) to his choices, but the cleanest graph structure is the AFFLICTED_BY dyad on the character node first.

---

### Seam 2 — `assassinations-of-pycelle-and-kevan-lannister` → KL endgame terminus

**The KL endgame collapse: is there a downstream node?**

**Investigated:** `cersei-resolves-on-trial-by-combat`, `cersei-is-captured-in-the-sept`, `cersei-is-stripped-and-imprisoned`, `cersei-rearms-the-faith-and-forgives-the-debt`, `faith-militant-uprising`. None of these are the downstream of the assassinations — they are all AFFC events (pre-ADWD) that precede Kevan's regency, not consequences of his death.

**Finding:** There is NO built KL endgame event node representing "Kevan's reconciliation project" or "Kevan's regency succeeds/collapses." The Kevan regency is documented only in `adwd-epilogue.md` (Kevan's POV) and exists only as character prose on `kevan-lannister`. No event node = no clean CAUSES target.

**What the text says:**
`adwd-epilogue.md:285`: "you were threatening to undo all the queen's good work, to reconcile Highgarden and Casterly Rock, bind the Faith to your little king, unite the Seven Kingdoms under Tommen's rule."

The `assassinations` node currently has **0 outgoing edges** (verified). The causal target — "the collapse of Kevan's stabilization / Tommen's unity" — **does not exist as a graph node**. It would require minting a new event node (`kevan-lannister-regency` or similar) to wire this seam, which is out of scope for lens-D (lens-D finds existing-node seams; mints belong to other lenses/sessions).

**Result:** UNBUILDABLE without a mint. Logged below in "Investigated but no clean seam."

However: one non-mint edge IS possible:
**`assassinations-of-pycelle-and-kevan-lannister --PREVENTS--> kevan-lannister [reconciling-the-realm]`**

PREVENTS is in the locked vocab. The semantic is: the assassinations PREVENT Kevan from executing his reconciliation project. The edge is character→event, which is backward from how PREVENTS usually works (event→event). **This is a valid structural edge only if we model it as:**

`assassinations-of-pycelle-and-kevan-lannister --PREVENTS--> <kevan-reconciles-realm-event>` (NEW-NODE-NEEDED)

Without the target event node this seam is also UNBUILDABLE cleanly. Do not model it as `assassinations PREVENTS kevan-lannister` (the person, not an event).

---

### Seam 3 — GC founding: `aegor-rivers FOUNDED golden-company`

**Pre-check result: ALREADY BUILT.**

`aegor-rivers --FOUNDED--> golden-company` exists in the live graph, with a strong Tier-1 book cite:
- ref: `sources/chapters/adwd/adwd-tyrion-02.md:139`
- quote: "Bittersteel saw the strength of House Blackfyre scattering to the four winds, so he gathered the survivors around him and formed the Golden Company."

**Status:** HIT, already built. No proposal needed. The founding fact is correctly captured without touching the Blackfyre-loyalty → Aegon theory (which is gated).

---

### Seam 4 — `greyscale --MOTIVATES--> jon-connington` [death-clock drives haste]

Once `jon-connington --AFFLICTED_BY--> greyscale` is wired (Seam 1), this becomes a viable second hop:

**Edge:** `greyscale --MOTIVATES--> jon-connington` [his haste, his refusal of caution]

**Agency check:** Here the edge direction and type need care. The condition (greyscale) MOTIVATES the character (Connington) to act with urgency. This is character-state → character motivation. In vocab: MOTIVATES (target is usually a person OR an event). The greyscale condition as source, Connington as target: `greyscale MOTIVATES jon-connington`.

BUT: this is structurally thin — MOTIVATES from a medical condition to a person is an unusual hop that doesn't give the graph a traversal anchor (it doesn't let you query "what caused the Storm's End siege" and get the greyscale). The richer structural form would be:

`[greyscale-infection-of-jon-connington] --MOTIVATES--> siege-of-storms-end-300`

Which again requires the event-mint. **Without the mint, log as harvest; do NOT propose a greyscale→character MOTIVATES that has no useful traversal purpose.**

**Decision: defer to future mint step.** The AFFLICTED_BY dyad (Seam 1) is the correct immediate deliverable.

---

### Seam 5 — `golden-company CONTRACTED_WITH <Yunkai/Volantis>` [broken contract]

**The text:** adwd-the-lost-lord-01:135 and :165 discuss the GC breaking the Yunkai envoy's offer and "one broken contract is stain enough." The GC was at Volon Therys, not Yunkai or Volantis. Harry Strickland says "I will not honor his agreement if I could, but how?" — this refers to the secret pact with Illyrio/Myles Toyne (sail to Daenerys), not the Yunkai offer.

**Node check:** Does `yunkai` or `volantis` exist as a target?
- The Yunkai offer was never accepted — the GC did NOT contract with Yunkai. Gorys Edoryen suggests "feign acceptance" but it was declined. No `CONTRACTED_WITH yunkai` edge is warranted.
- The broken contract is the Toyne-Illyrio secret pact (sail to Daenerys). `illyrio-mopatis` exists. But: the "broken contract" is really the CANCELED plan, not a formal contract breach.

**Status:** UNBUILDABLE as a `CONTRACTED_WITH` edge. The Yunkai offer was refused; the Illyrio pact is better modeled as `illyrio-mopatis CONSPIRES_WITH varys` (already built) + the sailing-west decision. There is no clean `golden-company CONTRACTED_WITH <node>` to wire without fabricating a contract that wasn't accepted.

---

## Summary of Proposals

| # | Edge | Type | Both exist? | Status | Priority |
|---|------|------|------------|--------|----------|
| 1 | `jon-connington --AFFLICTED_BY--> greyscale` | AFFLICTED_BY | YES (both HIT) | DARK — propose | HIGH |
| 2 | `assassinations PREVENTS kevan-regency-project` | PREVENTS | greyscale → NEW-NODE-NEEDED | UNBUILDABLE without mint | defer |
| 3 | `aegor-rivers FOUNDED golden-company` | FOUNDED | YES | **ALREADY BUILT** | done |
| 4 | `greyscale MOTIVATES siege-of-storms-end-300` (via infection event) | MOTIVATES | event = NEW-NODE-NEEDED | UNBUILDABLE without mint | defer |
| 5 | `golden-company CONTRACTED_WITH yunkai` | CONTRACTED_WITH | yunkai = would be HIT but contract was refused | FABRICATION RISK | skip |

**Net deliverable: 1 high-value clean edge (Seam 1 AFFLICTED_BY).**

---

## Investigated but No Clean Seam

### A. `assassinations` → KL endgame collapse (the 0-outgoing problem)

The `assassinations-of-pycelle-and-kevan-lannister` node has 0 outgoing edges. The causal target — the collapse of Kevan's Highgarden/Casterly-Rock reconciliation and Tommen's destabilized rule — exists only in prose (adwd-epilogue:285), not as a graph event node. The ADWD epilogue's KL endgame events (Cersei's trial arc, the Walk of Shame) are AFFC-set and are already wired in a different container thread (`cersei-is-captured-in-the-sept` → `cersei-is-stripped-and-imprisoned` → `cersei-resolves-on-trial-by-combat`). None of these is the downstream of the Kevan assassination — they are its CONTEXT (they're why Kevan came to KL), not its consequence.

**Conclusion:** A mint `kevan-named-lord-regent` or `tommen-regency-destabilized` event node would be required to wire this seam. That mint is HIGH VALUE (would resolve the 0-outgoing problem) but is out of scope for this lens. Flagged for the mint-lens or a future enrichment step.

### B. Greyscale death-clock → Storm's End haste (deeper seam)

The structural seam `stone-men-attack-the-shy-maid --ENABLES--> [greyscale-infection-event] --MOTIVATES--> siege-of-storms-end-300` is strongly text-grounded (adwd-the-griffin-reborn-01:141, :173; adwd-the-lost-lord-01:239) but requires minting `greyscale-infection-of-jon-connington` as an event.incident. Without that node, the only clean existing-node seam is the AFFLICTED_BY dyad (Seam 1). Flagged for mint.

### C. `golden-company CONTRACTED_WITH` Yunkai or Illyrio/Toyne

The GC's contract situation is:
1. The Toyne-Illyrio secret pact (sail to Daenerys) = not a formal CONTRACTED_WITH but a CONSPIRES_WITH arrangement. `varys CONSPIRES_WITH illyrio-mopatis` is already built.
2. The Yunkai envoy's offer = refused. No accepted contract; no CONTRACTED_WITH warranted.
3. Myr's previous contract (Disputed Lands) = mentioned in passing but the GC already left it. No node for the Myr contract.

**Conclusion:** No clean CONTRACTED_WITH seam for the GC in the AEGON arc. The broken-contract theme is better captured in node prose on `golden-company` or `golden-company-sails-for-westeros` than as a causal edge.

### D. `aegor-rivers` → additional GC seams

Beyond the already-built `FOUNDED` edge, `aegor-rivers` has no other clean AEGON-arc seam in the current graph. The Bittersteel/Bloodraven rivalry (Shiera Seastar love triangle) is wired as a `LOVER_OF` dyad. The Blackfyre-loyalty angle (why the GC would follow Aegon) is GATED (theory). No new edges here.

### E. The Dany/Meereen convergence

Confirmed GATED (TWOW). The `landing PRECEDES hizdahr-wedding` edge was already deleted at build-step-0 per baseline. Do not resurrect or re-examine.

---

## Harvest

*(Incidental finds during chapter reads — POINT, don't extract. Append to `working/harvest-queue.md`.)*

| status | kind | book | ref | note | session |
|--------|------|------|-----|------|---------|
| open | quote | adwd | `sources/chapters/adwd/adwd-the-griffin-reborn-01.md:141` | Connington's greyscale self-revelation: "I should have let the damned dwarf drown." — dark humor, self-condemnation, reveals the infection vector; evidence for `jon-connington AFFLICTED_BY greyscale` + the rescue during stone-men attack | 2026-06-25 lens-d |
| open | quote | adwd | `sources/chapters/adwd/adwd-tyrion-06.md:21` | Haldon to Tyrion: "it was Lemore who forced the water from your lungs after Griff had pulled you up. You were as cold as ice, and your lips were blue." — confirms Connington rescued Tyrion by plunging into Rhoyne; the infection event | 2026-06-25 lens-d |
| open | quote | adwd | `sources/chapters/adwd/adwd-tyrion-06.md:67` | Haldon to Tyrion (vinegar-bathing): "You swallowed half the river. You may be going grey even now, turning to stone from inside out, starting with your heart and lungs." — greyscale-exposure foreshadowing for Tyrion; companion to Connington's infection; hospitality/medical detail | 2026-06-25 lens-d |
| open | description | adwd | `sources/chapters/adwd/adwd-epilogue.md:285` | Varys to dying Kevan: "you were threatening to undo all the queen's good work, to reconcile Highgarden and Casterly Rock, bind the Faith to your little king, unite the Seven Kingdoms under Tommen's rule." — evidence for the FUTURE mint `kevan-reconciles-realm` event (the thing the assassinations PREVENT); high-value causal evidence | 2026-06-25 lens-d |
| open | quote | adwd | `sources/chapters/adwd/adwd-tyrion-05.md:157` | Tyrion to Aegon during stone-men attack: "if the stone men had taken Yandry or Griff or our lovely Lemore, we would have grieved for them and gone on. Lose you, and this whole enterprise is undone, and all those years of feverish plotting by the cheesemonger and the eunuch will have been for naught" — reveals Tyrion already knows Aegon's identity; strong evidence for Tyrion's MOTIVATES edge on the sail-west decision | 2026-06-25 lens-d |
| open | quote | adwd | `sources/chapters/adwd/adwd-the-lost-lord-01.md:239` | Connington's death-clock internal: "Death, he knew, but slow. I still have time. A year. Two years. Five. Some stone men live for ten. Time enough to cross the sea, to see Griffin's Roost again. To end the Usurper's line for good and all, and put Rhaegar's son upon the Iron Throne." — the `greyscale MOTIVATES his campaign haste` seam; evidence for future event-node mint | 2026-06-25 lens-d |

---

## Mint Flag (for future step)

Two high-value event nodes are needed to unlock the blocked seams above. These are NOT proposals for this session (lens-D proposes existing-node seams only), but flagged for the build step:

1. **`greyscale-infection-of-jon-connington`** (event.incident, `[aegon]`)
   - Source: `adwd-tyrion-05.md:231–234` (Tyrion dragged under) + `adwd-tyrion-06.md:21` (Connington pulled him up) + `adwd-the-griffin-reborn-01.md:141` (Connington's POV revealing the infection)
   - Enables: `stone-men-attack-the-shy-maid --ENABLES--> [infection]` and `[infection] --MOTIVATES--> siege-of-storms-end-300`

2. **`kevan-reconciles-the-realm`** or **`kevan-lannister-regency`** (event.incident, `[wo5k]` — NOT aegon-owned but cross-container terminus)
   - Source: `adwd-epilogue.md:285` (Varys describes what Kevan was doing)
   - Enables: `assassinations-of-pycelle-and-kevan-lannister --PREVENTS--> [kevan-reconciles-realm]` (resolves the 0-outgoing problem on `assassinations`)
