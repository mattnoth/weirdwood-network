# Plate 3 Hub Review Queue — Triage List

**Generated:** 2026-06-07 22:50:24
**Source:** working/edge-modeling/plate3-full/hub-review-queue.jsonl

## Reason buckets

- **borderline-single-agent** — 75 entries
- **non-harming-multi-agent** — 32 entries
- **fuzzy-match** — 2 entries

---

## How to triage

For each entry below, decide one of:
- **KEEP-DYAD** — leave existing direct edges in edges.jsonl (e.g. KILLS / BETRAYS); do NOT mint an event hub.
- **MINT-HUB** — promote to a real event-node at Plate 5 (move from hub-review-queue.jsonl → minted-event-nodes/).
- **DROP** — micro-beat / not worth reifying / shouldn't be in the graph.

---

## borderline-single-agent

**What this means:** LLM said is_nary=true but only emitted 1 AGENT_IN + ≤1 VICTIM_IN + 0 COMMANDS_IN. Effectively a clean dyad. Per D8 design, clean dyads should NOT be reified — direct edge is correct.

**Default action:** KEEP-DYAD.

- arya-kills-the-stableboy-with-needle — Arya kills the stableboy with Needle
- street-rumors-about-robert-s-death — Street rumors about Robert's death
- arya-sees-the-tower-of-the-hand-under-attack — Arya sees the Tower of the Hand under attack
- dawn-breaks-and-the-battle-ends — Dawn breaks and the battle ends
- multiple-deaths-at-the-wedding — Multiple deaths at the wedding
- a-boy-is-run-down-and-killed — A boy is run down and killed
- ser-jorah-fights-and-kills-qotho — Ser Jorah fights and kills Qotho
- dany-mercy-kills-drogo-at-dawn — Dany mercy-kills Drogo at dawn
- gregor-kills-his-horse-and-attacks-loras — Gregor kills his horse and attacks Loras
- littlefinger-s-final-betrayal — Littlefinger's final betrayal
- the-watching-others-kill-royce — The watching Others kill Royce
- gared-attributes-the-deaths-to-cold — Gared attributes the deaths to cold
- will-discovers-the-bodies-have-vanished — Will discovers the bodies have vanished
- nymeria-attacks-joffrey — Nymeria attacks Joffrey
- arya-attacks-joffrey — Arya attacks Joffrey
- a-captive-girl-is-beheaded — A captive girl is beheaded
- arya-kills-the-postern-guard — Arya kills the postern guard
- fool-s-jest-about-kinslayer-kingslayer — Fool's jest about "Kinslayer/Kingslayer"
- the-undying-attack-dany — The Undying attack Dany
- sorrowful-man-assassination-attempt — Sorrowful Man assassination attempt
- ghost-kills-craster-s-rabbits — Ghost kills Craster's rabbits
- davos-boards-and-captures-white-hart — Davos boards and captures White Hart
- eagle-attacks-ghost — Eagle attacks Ghost
- cressen-offers-the-poisoned-cup-to-melisandre — Cressen offers the poisoned cup to Melisandre
- cressen-drinks-the-poisoned-wine-and-dies — Cressen drinks the poisoned wine and dies
- theon-threatens-systematic-executions — Theon threatens systematic executions
- tyrion-confronts-slynt-about-ned-stark-s-execution — Tyrion confronts Slynt about Ned Stark's execution
- aron-santagar-killed — Aron Santagar killed
- tyrion-assesses-the-battle-situation — Tyrion assesses the battle situation
- tyrion-reasons-the-battle-was-won — Tyrion reasons the battle was won
- battlefield-delirium-dream — Battlefield delirium-dream
- thoros-at-the-siege-of-pyke — Thoros at the siege of Pyke
- arya-questions-the-prisoners — Arya questions the prisoners
- beric-killed — Beric killed
- three-squires-attack-the-crannogman — Three squires attack the crannogman
- robb-sentences-karstark-to-death — Robb sentences Karstark to death
- dawn-execution-in-the-godswood — Dawn execution in the godswood
- catelyn-takes-jinglebell-hostage — Catelyn takes Jinglebell hostage
- davos-declares-intent-to-kill-melisandre — Davos declares intent to kill Melisandre
- chett-goes-to-kill-sam-anyway — Chett goes to kill Sam anyway
- sam-kills-the-other-with-dragonglass — Sam kills the Other with dragonglass
- bannen-dies — Bannen dies
- craster-attacks — Craster attacks
- sam-stabs-paul-with-dragonglass — Sam stabs Paul with dragonglass
- ravens-attack-the-wights — Ravens attack the wights
- joffrey-dies — Joffrey dies
- tyrion-declares-his-innocence-and-demands-trial-by-battle — Tyrion declares his innocence and demands trial by battle
- tywin-dies — Tywin dies
- tyrion-falsely-confesses-to-joffrey-s-murder — Tyrion falsely confesses to Joffrey's murder
- the-kindly-man-explains-the-nature-of-death-and-the-candles — The kindly man explains the nature of death and the candles
- brienne-fights-and-kills-the-man-in-the-hound-s-helm — Brienne fights and kills the man in the Hound's helm
- brienne-invokes-guest-right — Brienne invokes guest right
- pate-s-death — Pate's death
- jaime-ends-the-council-and-announces-attack-at-first-light — Jaime ends the council and announces attack at first light
- battle-concluded — Battle concluded
- sea-battle-at-the-mouth-of-the-mander — Sea battle at the mouth of the Mander
- cersei-denies-murder-charges — Cersei denies murder charges
- hostage-decree — Hostage decree
- dany-dresses-in-her-tokar-with-baby-pearls-for-the-wedding — Dany dresses in her tokar with baby pearls for the wedding
- dany-surveys-the-siege-from-the-terrace — Dany surveys the siege from the terrace
- drogon-kills-the-boar-with-black-fire — Drogon kills the boar with black fire
- mock-battle — Mock battle
- davos-captured-in-sisterton — Davos captured in Sisterton
- wun-wun-kills-ser-patrek — Wun Wun kills Ser Patrek
- varamyr-fails-and-dies — Varamyr fails and dies
- ramsay-promises-food-and-care-for-prisoners — Ramsay promises food and care for prisoners
- the-kindly-man-s-teaching-about-killing — The kindly man's teaching about killing
- hizdahr-taken-prisoner — Hizdahr taken prisoner
- post-ceremony-music — Post-ceremony music
- theon-climbs-the-inner-wall-battlements — Theon climbs the inner wall battlements
- quentyn-martell-dies — Quentyn Martell dies
- forest-battle-begins — Forest battle begins
- tyrion-finds-poisonous-mushrooms — Tyrion finds poisonous mushrooms
- holly-killed — Holly killed
- galley-crews-put-to-death-slaves-freed — Galley crews put to death; slaves freed

---

## non-harming-multi-agent

**What this means:** Multiple agents acting without harm (0 VICTIM + 0 COMMANDS). Usually journey/council/observation beats. Mostly DROP unless they're a legit n-ary council vote / coronation / ceremony.

**Default action:** DROP. Spot-check for legit coronations / vows / pacts.

- the-direwolves-howl-from-a-kill — The direwolves howl from a kill
- robb-presents-his-battle-plan — Robb presents his battle plan
- the-battle-rages-through-the-night — The battle rages through the night
- pre-wedding-dinner-at-the-manse — Pre-wedding dinner at the manse
- dany-rides-through-the-battlefield-aftermath — Dany rides through the battlefield aftermath
- stallion-heart-ceremony — Stallion heart ceremony
- stallion-sacrifice — Stallion sacrifice
- they-approach-the-battleground-at-the-ford — They approach the battleground at the ford
- tyrion-arms-for-battle — Tyrion arms for battle
- shaggydog-kills-the-dying-horse — Shaggydog kills the dying horse
- theon-arms-for-battle — Theon arms for battle
- joffrey-s-role-in-battle-debated — Joffrey's role in battle debated
- wedge-advances-along-the-walls — Wedge advances along the walls
- catelyn-secures-guest-right — Catelyn secures guest right
- waiting-during-the-battle — Waiting during the battle
- ser-axell-and-queen-selyse-attribute-the-deaths-to-r-hllor — Ser Axell and Queen Selyse attribute the deaths to R'hllor
- nightfire-prayer-ceremony — Nightfire prayer ceremony
- night-attack-begins — Night attack begins
- they-depart-for-the-wedding — They depart for the wedding
- wedding-feast-and-bedding — Wedding feast and bedding
- joffrey-s-wedding-feast-planned — Joffrey's wedding feast planned
- wedding-ceremony-at-the-great-sept-of-baelor — Wedding ceremony at the Great Sept of Baelor
- wedding-feast — Wedding feast
- shagwell-attacks — Shagwell attacks
- arianne-and-doran-argue-about-the-plot-s-consequences — Arianne and Doran argue about the plot's consequences
- wedding-ceremony-at-the-temple-of-the-graces — Wedding ceremony at the Temple of the Graces
- jon-attends-the-wedding-feast — Jon attends the wedding feast
- wedding-ceremony-begins — Wedding ceremony begins
- conspiracy-meeting-in-armory — Conspiracy meeting in armory
- theon-leads-jeyne-holly-and-frenya-toward-battlements-gate — Theon leads Jeyne, Holly, and Frenya toward Battlements Gate
- arrive-at-battlements-gate — Arrive at Battlements Gate
- the-cart-travels-through-the-siege-camp — The cart travels through the siege camp

---

## fuzzy-match (queue_review)

**What this means:** LLM did NOT classify; resolver found a medium-confidence fuzzy match to an existing event-node.

- siege-of-storm-s-end-recalled → fuzzy-matched siege-of-storms-end-299 (score 0.833)
- siege-of-storm-s-end-recalled → fuzzy-matched siege-of-storms-end-299 (score 0.833)
