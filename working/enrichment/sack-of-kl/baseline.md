# Baseline — Sack of King's Landing cluster (S142, the last L1 remnant — a double-dip)

> Built from `graph-query.py --neighbors`. This is the dedup baseline — lenses must NOT
> re-propose anything already present here. **This arc is ALREADY PARTLY ENRICHED** (core
> wired in the RR pass S133; the Elia→Oberyn seam in the Tywin's-death pass S139). It is a
> flagged **low-marginal-yield double-dip** — propose only genuinely NEW, well-grounded
> off-spine substrate; expect a smaller harvest than a fresh arc. Quality over quantity.

## The hub — `sack-of-kings-landing` (event.battle) — ALREADY DENSE
- OUT: `CAUSES coronation-of-robert-i-baratheon`; `LOCATED_AT kings-landing`; `PART_OF roberts-rebellion`.
- IN: AGENT_IN {jaime-lannister, gregor-clegane, amory-lorch}; CAUSES {battle-of-the-trident, pycelle-opens-the-gates-of-kings-landing}; COMMANDS_IN {tywin-lannister}; VICTIM_IN {aerys-ii-targaryen, elia-martell, rhaenys-targaryen-daughter-of-rhaegar, aegon-targaryen-son-of-rhaegar}.
- **4 SUB_BEAT_OF children already attached:** `pycelle-opens-the-gates-of-kings-landing`, `aerys-commands-the-city-burned`, `slaying-of-aerys-ii-the-kingslaying`, `murder-of-elia-martell-and-rhaegars-children`.

## The 4 existing sub-beats — what each already has
- **`pycelle-opens-the-gates-of-kings-landing`** (event.deception): CAUSES + SUB_BEAT_OF sack; LOCATED_AT kings-landing; pycelle AGENT_IN. (well-wired)
- **`aerys-commands-the-city-burned`** (event.incident): SUB_BEAT_OF sack; LOCATED_AT kings-landing; `TRIGGERS slaying-of-aerys-ii-the-kingslaying`; aerys-ii-targaryen COMMANDS_IN. **Only 1 inbound — the wildfire-plot is NOT wired to it.**
- **`slaying-of-aerys-ii-the-kingslaying`** (event.assassination): SUB_BEAT_OF sack; LOCATED_AT kings-landing; jaime AGENT_IN; aerys VICTIM_IN; `wildfire-plot MOTIVATES` it; `aerys-commands-the-city-burned TRIGGERS` it. **No outgoing causal/reputational consequence** (Jaime's "Kingslayer" stain is unwired).
- **`murder-of-elia-martell-and-rhaegars-children`** (event.assassination): SUB_BEAT_OF sack; LOCATED_AT kings-landing; gregor+amory AGENT_IN; tywin COMMANDS_IN; elia/rhaenys/aegon VICTIM_IN; `MOTIVATES eddard-stark` (the Ned-named-it-murder rift) + `MOTIVATES oberyn-martell` (S139 seam → Tywin's death). (rich)

## The wildfire thread — partly built, NOT integrated into the sack
- **`wildfire-plot`** (event.battle — the 283AC cache-placement): OUT `MOTIVATES slaying-of-aerys`, `PART_OF roberts-rebellion`, `PRECEDES assault-on-dragonstone`; IN rossart AGENT_IN, aerys COMMANDS_IN, `battle-of-ashford PRECEDES`. **NOT a SUB_BEAT_OF the sack, NOT wired to `aerys-commands-the-city-burned`.** Only Rossart is wired of the three pyromancers.
- **`wildfire` (object)** exists. **`wildfire-trap-on-the-blackwater`** (S138 Blackwater node) exists — **S138 DELIBERATELY did NOT wire it to `wildfire-plot`** (kept the Aerys-283 cache and the Blackwater battle separate). A surviving-caches ENABLES seam is *possible* but contested — handle with extreme care, flag as inference, do NOT conflate the two nodes.

## Existing character/object nodes available as edge endpoints (DON'T re-mint; wire to these)
- **Pyromancers / alchemists:** `rossart` (AGENT_IN wildfire-plot already), `belis`, `garigus` (the two other pyromancers Jaime hunted), `qarlton-chelsted` (the Hand who balked → Aerys burned him).
- **Lannister sackers:** `tywin-lannister`, `jaime-lannister`, `gregor-clegane`, `amory-lorch`, `roland-crakehall` (the Kingsguard who found Jaime on the throne / brought Tywin's men in).
- **The murdered & royals:** `aerys-ii-targaryen`, `elia-martell`, `aegon-targaryen-son-of-rhaegar`, `rhaenys-targaryen-daughter-of-rhaegar`, `rhaegar-targaryen`, `lyanna-stark`.
- **Witnesses / aftermath actors:** `eddard-stark` (finds Jaime on the throne), `robert-baratheon` (condones — "I see no babes, only dragonspawn"), `varys` (the babe-swap — THEORY-GATED), `pycelle`, `oberyn-martell`.
- **Trident Kingsguard (context):** `jonothor-darry`, `lewyn-martell`, `barristan-selmy`.
- **Objects/places:** `wildfire`, `iron-throne` (slug is `iron-throne`, NOT `the-iron-throne`), `kings-landing`, `coronation-of-robert-i-baratheon`.

## Where the yield MIGHT be (gap thesis — but this arc is thin/already-dipped)
1. **Integrate the wildfire-plot into the sack** — `wildfire-plot ENABLES aerys-commands-the-city-burned` (the caches are the precondition of the burn-order); SUB_BEAT_OF the sack? (the plot predates the sack — careful). Wire `belis`/`garigus` AGENT_IN wildfire-plot; `qarlton-chelsted VICTIM_IN` (burned for balking).
2. **The pyromancer-hunt** — Jaime "slew him first" (Rossart), then hunted Belis & Garigus. A `jaime-hunts-the-pyromancers` beat OR AGENT_IN/KILLS edges. (Check: is the killing on-page or wiki?)
3. **Jaime found on the Iron Throne by Ned** — the iconic revelation beat (AGOT Eddard); seeds the Ned↔Jaime contempt + the Kingslayer reputation. WITNESS / a beat-node?
4. **The political aftermath** — Tywin lays the wrapped bodies before the throne; Robert condones; the Lannister-Baratheon alliance / Tywin's pardon + Jaime kept in the Kingsguard. Wires Robert's complicity + the Robert↔Ned rift.
5. **The Kingslayer-reputation consequence** — `slaying-of-aerys CAUSES/MOTIVATES` Jaime's lifelong stain (his whole identity arc). Find a target node or note as character-arc.
6. **Object/quote depth** — the wildfire substance & cache-locations; the Iron Throne; the crimson Lannister cloaks the babes were wrapped in; the rubies of Rhaegar (Trident — maybe out of scope).
7. **THEORY-GATED (evidence-only, never assert):** the Aegon babe-swap (Varys SUSPECTED_OF / a substituted-child reading) — surface to the theories track, do NOT mint a claim that the smashed babe wasn't Aegon.

## Chapter files (read these directly — line-check every cite)
- The Kingslaying + wildfire + Jaime's confession: `sources/chapters/asos/asos-jaime-05.md` (the bath/wildfire confession to Brienne), `asos-jaime-02.md`, `asos-jaime-08.md` (the white-book entry).
- Tywin's justification + the murder of Elia/children + Oberyn's account: `sources/chapters/asos/asos-tyrion-06.md`, `asos-tyrion-09.md`, `asos-tyrion-10.md`.
- Pycelle opens the gates: `sources/chapters/acok/acok-tyrion-06.md`.
- Ned finds Jaime on the throne / Robert condones / the bodies: `sources/chapters/agot/agot-eddard-*.md` (esp. agot-eddard-02 — "Ned had named that murder; Robert called it war").
