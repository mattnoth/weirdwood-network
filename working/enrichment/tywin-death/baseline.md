# BASELINE — Tywin's Death enrichment (Session 139, pass 1)

The unit = the **assassination-of-tywin-lannister** event-arc (the ASOS Tyrion XI escape +
its upstream trial chain). The S109 causal SPINE is already built and well-wired. This pass
ENRICHES the off-spine substrate: trial participants, the Shae betrayal, Oberyn's motive,
the murder instruments (objects), Varys's escape role, Jaime's guilt-motive, and descriptive
depth. **PROPOSE only — do not mint.** Dedup every proposal against the edges/nodes below.

## Source chapters (read these directly; cite VERBATIM with exact begin-line)
- `sources/chapters/asos/asos-tyrion-08.md` (324 lines) — trial opens, witness parade begins
- `sources/chapters/asos/asos-tyrion-09.md` (420 lines) — Shae testifies ("my giant of Lannister"); Tyrion's confession-speech; demands trial by combat
- `sources/chapters/asos/asos-tyrion-10.md` (252 lines) — trial by combat: Oberyn (champion) vs Gregor; Oberyn poisons Gregor with manticore venom but is killed
- `sources/chapters/asos/asos-tyrion-11.md` (270 lines) — Jaime frees Tyrion; Tysha reveal; Tyrion strangles Shae with the Hand's chain; shoots Tywin on the privy with a crossbow; Varys spirits him away

## EXISTING NODES in/around the cluster (DO NOT re-propose these)
**Events:** assassination-of-tywin-lannister (hub, event.assassination) · trial-of-tyrion-lannister (event.trial) · gregor-confesses-and-kills-oberyn (event.death) · jaime-frees-tyrion-from-the-black-cells (event.incident) · jaime-reveals-the-truth-of-tysha (event.incident) · tyrion-kills-shae-in-tywins-bed (event.death) · tyrion-accused-of-poisoning-joffrey (event) · tyrion-resolves-to-wed-shae-to-ser-tallad (event) · murder-of-elia-martell-and-rhaegars-children (event) · purple-wedding · death-of-joffrey-baratheon · arrest-of-the-sand-snakes
**Characters:** tyrion-lannister · tywin-lannister · jaime-lannister · cersei-lannister · oberyn-martell · gregor-clegane · shae · varys · tysha · mace-tyrell · ellaria-sand · elia-martell · tallad
**Objects/Concepts:** widows-wail (artifact) · manticore-venom (concept.medical) · hand-of-the-king (title)
**Places:** tower-of-the-hand · black-cells · red-keep · red-keep

**NO node exists for** (mint candidates if load-bearing + grounded): the crossbow Tywin is killed with · the Hand's chain-of-office Shae is strangled with · Oberyn's poisoned spear (artifact) · a Varys-smuggles-Tyrion / Tyrion-flees-into-exile beat.

## EXISTING EDGES (35) — dedup target
```
assassination-of-tywin-lannister CAUSES cersei-rearms-the-faith-and-forgives-the-debt
assassination-of-tywin-lannister LOCATED_AT tower-of-the-hand
assassination-of-tywin-lannister PART_OF war-of-the-five-kings
cersei-lannister AGENT_IN tyrion-accused-of-poisoning-joffrey
cersei-lannister COMMANDS_IN gregor-confesses-and-kills-oberyn
death-of-joffrey-baratheon TRIGGERS tyrion-accused-of-poisoning-joffrey
gregor-clegane AGENT_IN gregor-confesses-and-kills-oberyn
gregor-confesses-and-kills-oberyn CAUSES jaime-frees-tyrion-from-the-black-cells
gregor-confesses-and-kills-oberyn CAUSES arrest-of-the-sand-snakes
jaime-frees-tyrion-from-the-black-cells CAUSES jaime-reveals-the-truth-of-tysha
jaime-frees-tyrion-from-the-black-cells LOCATED_AT black-cells
jaime-lannister AGENT_IN jaime-frees-tyrion-from-the-black-cells
jaime-lannister AGENT_IN jaime-reveals-the-truth-of-tysha
jaime-reveals-the-truth-of-tysha CAUSES assassination-of-tywin-lannister
jaime-reveals-the-truth-of-tysha CAUSES tyrion-kills-shae-in-tywins-bed
jaime-reveals-the-truth-of-tysha LOCATED_AT black-cells
jaime-reveals-the-truth-of-tysha MOTIVATES tyrion-lannister
oberyn-martell VICTIM_IN gregor-confesses-and-kills-oberyn
shae VICTIM_IN tyrion-resolves-to-wed-shae-to-ser-tallad
shae VICTIM_IN tyrion-kills-shae-in-tywins-bed
tallad VICTIM_IN tyrion-resolves-to-wed-shae-to-ser-tallad
trial-of-tyrion-lannister LOCATED_AT red-keep
trial-of-tyrion-lannister TRIGGERS gregor-confesses-and-kills-oberyn
tyrion-accused-of-poisoning-joffrey CAUSES trial-of-tyrion-lannister
tyrion-accused-of-poisoning-joffrey LOCATED_AT red-keep
tyrion-accused-of-poisoning-joffrey SUB_BEAT_OF purple-wedding
tyrion-kills-shae-in-tywins-bed LOCATED_AT tower-of-the-hand
tyrion-lannister AGENT_IN tyrion-resolves-to-wed-shae-to-ser-tallad
tyrion-lannister AGENT_IN assassination-of-tywin-lannister
tyrion-lannister AGENT_IN tyrion-kills-shae-in-tywins-bed
tyrion-lannister VICTIM_IN tyrion-accused-of-poisoning-joffrey
tyrion-lannister VICTIM_IN trial-of-tyrion-lannister
tywin-lannister AGENT_IN trial-of-tyrion-lannister
tywin-lannister VICTIM_IN assassination-of-tywin-lannister
varys COMMANDS_IN jaime-frees-tyrion-from-the-black-cells
```

## CAUSAL SPINE (for orientation)
death-of-joffrey TRIGGERS tyrion-accused → CAUSES trial → TRIGGERS gregor-kills-oberyn → CAUSES jaime-frees → CAUSES jaime-reveals-tysha → CAUSES assassination-of-tywin (+ CAUSES tyrion-kills-shae; MOTIVATES tyrion)
