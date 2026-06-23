# S135 — Purple Wedding enrichment dip · DEDUP BASELINE

> What ALREADY EXISTS in the graph for the Purple Wedding cluster. **Do NOT re-propose any
> edge listed here.** Propose only NEW edges/nodes that deepen the cluster. Verbatim dump from
> `graph-query.py --neighbors` (2026-06-23, S135).

## The hub + its beats (SUB_BEAT_OF purple-wedding)

`purple-wedding` (event.wedding) — hub. OUT: `PART_OF war-of-the-five-kings`. Walks 0 causal
(by design — it's a reified hub; causality lives on the beats below, not the umbrella).
6 SUB_BEAT_OF children:
1. `wedding-ceremony-at-the-great-sept-of-baelor` (event.wedding) — the betrothal ceremony
2. `sansa-receives-the-poisoned-hairnet` (event.deception)
3. `death-of-joffrey-baratheon` (event.assassination)
4. `tyrion-accused-of-poisoning-joffrey` (event.incident)
5. `littlefinger-smuggles-sansa-out-of-kings-landing` (event.deception)
6. `tyrell-plot-revealed` (event.conspiracy)

## Existing causal chain (the spine — DO NOT re-propose)

`sansa-receives-the-poisoned-hairnet --CAUSES--> death-of-joffrey-baratheon --TRIGGERS-->
tyrion-accused-of-poisoning-joffrey --CAUSES--> trial-of-tyrion-lannister --TRIGGERS-->
gregor-confesses-and-kills-oberyn` (the chain then walks downstream into the Tywin's-death arc).

## Existing role / participant edges (DO NOT re-propose)

- death-of-joffrey-baratheon: `olenna-tyrell AGENT_IN`, `petyr-baelish COMMANDS_IN`,
  `joffrey-baratheon VICTIM_IN`, `LOCATED_AT red-keep`
- sansa-receives-the-poisoned-hairnet: `dontos-hollard AGENT_IN`, `petyr-baelish COMMANDS_IN`,
  `sansa-stark VICTIM_IN`, `LOCATED_AT red-keep`
- tyrion-accused-of-poisoning-joffrey: `cersei-lannister AGENT_IN`, `tyrion-lannister VICTIM_IN`,
  `LOCATED_AT red-keep`
- trial-of-tyrion-lannister: `tywin-lannister AGENT_IN`, `tyrion-lannister VICTIM_IN`,
  `LOCATED_AT red-keep`, `TRIGGERS gregor-confesses-and-kills-oberyn`
- littlefinger-smuggles-sansa-out-of-kings-landing: `petyr-baelish AGENT_IN`,
  `dontos-hollard AGENT_IN`, `sansa-stark VICTIM_IN`, `LOCATED_AT red-keep`
- tyrell-plot-revealed: `petyr-baelish AGENT_IN`, `house-tyrell AGENT_IN`, `sansa-stark VICTIM_IN`
- wedding-ceremony-at-the-great-sept-of-baelor: `joffrey-baratheon AGENT_IN`,
  `margaery-tyrell AGENT_IN`, `mace-tyrell ATTENDS`, `LOCATED_AT great-sept-of-baelor`

## Known GAPS (where enrichment yield is — for orientation, not a script)

- **No SUSPECTED_OF layer.** Olenna+Littlefinger are the true agents (wired). But the IN-WORLD
  false suspicion (Tyrion is blamed by Cersei/the realm; Sansa flees and is suspected) has no
  `SUSPECTED_OF` edges. This is the marquee whodunit substrate.
- **`tyrell-plot-revealed` is causally isolated** (0 causal in/out) — the Tyrell *motive*
  (protect Margaery from Joffrey's cruelty) is unwired to the killing.
- **Dontos Hollard's fate** — the cat's-paw is silenced (killed by Littlefinger) — no node/edge.
- **No upstream** into the hub's beats from the Joffrey-Margaery betrothal / Tyrell-Lannister
  alliance (cross-arc seam — lens 4). Candidate existing nodes:
  `littlefinger-brokers-tyrell-lannister-alliance`, `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery`.
- **Feast texture / food / objects** — the 77-course feast, the pigeon pie, the wedding wine,
  the dwarf jousters, the WO5K-pie, the amethyst hairnet "Strangler" crystals — no descriptive/
  object/quote depth attached.

## Source chapters (local, navigable — read these for cites)

- `sources/chapters/asos/asos-sansa-02.md` — the hairnet given (Dontos)
- `sources/chapters/asos/asos-sansa-03.md` — Joffrey/Margaery wedding ceremony
- `sources/chapters/asos/asos-sansa-04.md` — pre-feast
- `sources/chapters/asos/asos-sansa-05.md` — the feast, Joffrey's death, Sansa flees
- `sources/chapters/asos/asos-sansa-06.md` — escape; Littlefinger's confession (Olenna did it)
- `sources/chapters/asos/asos-tyrion-08.md` — the feast from Tyrion's POV (cruelty, cupbearer)
- `sources/chapters/asos/asos-tyrion-09.md` — Tyrion seized / accused
- `sources/chapters/asos/asos-tyrion-10.md` — the trial
- `sources/chapters/asos/asos-tyrion-03.md` — Kevan reveals the Tyrell plot
