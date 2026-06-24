# Cersei's downfall — enrichment baseline (S140)
Generated Tue Jun 23 22:28:34 CDT 2026

Spine (S114): assassination-of-tywin CAUSES cersei-rearms-the-faith CAUSES cersei-is-captured-in-the-sept CAUSES cersei-is-stripped-and-imprisoned; margaery-plot CAUSES {blue-bard-arrest, osney-confesses}; osney-confesses TRIGGERS capture

==================================================================
## --neighbors cersei-rearms-the-faith-and-forgives-the-debt
========================================================================
NEIGHBORS: cersei-rearms-the-faith-and-forgives-the-debt
  Cersei rearms the Faith Militant and forgives the crown debt (event.incident)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-rearms-the-faith-and-forgives-the-debt.node.md

OUTGOING (1 edges — cersei-rearms-the-faith-and-forgives-the-debt is source)
------------------------------------------------------------------------
  [CAUSES]  (1 edge)
    -> cersei-is-captured-in-the-sept
       ref  : sources/chapters/affc/affc-cersei-10.md:249
       quote: "There were women waiting for her there, more septas and silent sisters too ... t..."

INCOMING (3 edges — cersei-rearms-the-faith-and-forgives-the-debt is target)
------------------------------------------------------------------------
  [AGENT_IN]  (2 edges)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-06.md:273
       quote: "As you wish. This debt shall be forgiven, and King Tommen will have his blessing..."
    <- high-sparrow
       ref  : sources/chapters/affc/affc-cersei-06.md:265
       quote: "The Faith Militant reborn ... If His Grace were to allow me to restore the ancie..."
  [CAUSES]  (1 edge)
    <- assassination-of-tywin-lannister
       ref  : sources/chapters/affc/affc-cersei-06.md:279
       quote: "Even her lord father could have done no better. At a stroke, she had rid King's ..."

========================================================================
SUMMARY: cersei-rearms-the-faith-and-forgives-the-debt  |  1 outgoing, 3 incoming  (4 total)

==================================================================
## --neighbors cersei-plots-against-margaery
========================================================================
NEIGHBORS: cersei-plots-against-margaery
  Cersei plots against Margaery (event.conspiracy)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-plots-against-margaery.node.md

OUTGOING (2 edges — cersei-plots-against-margaery is source)
------------------------------------------------------------------------
  [CAUSES]  (2 edges)
    -> cersei-confronts-and-arrests-the-blue-bard
       ref  : sources/chapters/affc/affc-cersei-09.md:163
       quote: "Liar! Cersei smashed the lute across the singer's face so hard the painted wood ..."
    -> osney-kettleblack-confesses-to-high-sparrow
       ref  : sources/chapters/affc/affc-cersei-09.md:311
       quote: "No, you must take yourself to the Great Sept of Baelor this very night and speak..."

INCOMING (3 edges — cersei-plots-against-margaery is target)
------------------------------------------------------------------------
  [AGENT_IN]  (2 edges)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-08.md
       quote: "She reasons Jaime cannot be relied on; considers methods (sickness, knife, pillo..."
    <- qyburn
       ref  : sources/chapters/affc/affc-cersei-08.md
       quote: "Qyburn | Serves/enables | Cersei | guides her toward killing Margaery; acts as h..."
  [VICTIM_IN]  (1 edge)
    <- margaery-tyrell
       ref  : sources/chapters/affc/affc-cersei-08.md
       quote: "Cersei | Concealed hostility toward | Margaery Tyrell — plans to destroy her; Qy..."

========================================================================
SUMMARY: cersei-plots-against-margaery  |  2 outgoing, 3 incoming  (5 total)

==================================================================
## --neighbors cersei-confronts-and-arrests-the-blue-bard
========================================================================
NEIGHBORS: cersei-confronts-and-arrests-the-blue-bard
  Cersei confronts and arrests the Blue Bard (event.capture)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-confronts-and-arrests-the-blue-bard.node.md

OUTGOING (0 edges — cersei-confronts-and-arrests-the-blue-bard is source)
------------------------------------------------------------------------
  (none)

INCOMING (4 edges — cersei-confronts-and-arrests-the-blue-bard is target)
------------------------------------------------------------------------
  [AGENT_IN]  (2 edges)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-09.md
       quote: "She asks to see his lute, then smashes it across his face and accuses him of bed..."
    <- orton-merryweather
       ref  : sources/chapters/affc/affc-cersei-09.md
       quote: "Orton Merryweather has him taken to the dungeons."
  [CAUSES]  (1 edge)
    <- cersei-plots-against-margaery
       ref  : sources/chapters/affc/affc-cersei-09.md:163
       quote: "Liar! Cersei smashed the lute across the singer's face so hard the painted wood ..."
  [VICTIM_IN]  (1 edge)
    <- blue-bard
       ref  : sources/chapters/affc/affc-cersei-09.md
       quote: "Cersei smashes lute across his face, has him tortured, forces false confession."

========================================================================
SUMMARY: cersei-confronts-and-arrests-the-blue-bard  |  0 outgoing, 4 incoming  (4 total)

==================================================================
## --neighbors osney-kettleblack-confesses-to-high-sparrow
========================================================================
NEIGHBORS: osney-kettleblack-confesses-to-high-sparrow
  Osney Kettleblack confesses to the High Sparrow (event.incident)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/osney-kettleblack-confesses-to-high-sparrow.node.md

OUTGOING (1 edges — osney-kettleblack-confesses-to-high-sparrow is source)
------------------------------------------------------------------------
  [TRIGGERS]  (1 edge)
    -> cersei-is-captured-in-the-sept
       ref  : sources/chapters/affc/affc-cersei-10.md:243
       quote: "That one there. She's the queen I fucked, the one sent me to kill the old High S..."

INCOMING (4 edges — osney-kettleblack-confesses-to-high-sparrow is target)
------------------------------------------------------------------------
  [AGENT_IN]  (1 edge)
    <- osney-kettleblack
       ref  : sources/chapters/affc/affc-cersei-10.md:243
       quote: "That one there. She's the queen I fucked, the one sent me to kill the old High S..."
  [CAUSES]  (1 edge)
    <- cersei-plots-against-margaery
       ref  : sources/chapters/affc/affc-cersei-09.md:311
       quote: "No, you must take yourself to the Great Sept of Baelor this very night and speak..."
  [COMMANDS_IN]  (1 edge)
    <- high-sparrow
       ref  : sources/chapters/affc/affc-cersei-10.md:27
       quote: "Ser Osney Kettleblack has confessed his carnal knowledge of the queen to the Hig..."
  [VICTIM_IN]  (1 edge)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-10.md:243
       quote: "She's the queen I fucked, the one sent me to kill the old High Septon."

========================================================================
SUMMARY: osney-kettleblack-confesses-to-high-sparrow  |  1 outgoing, 4 incoming  (5 total)

==================================================================
## --neighbors cersei-is-captured-in-the-sept
========================================================================
NEIGHBORS: cersei-is-captured-in-the-sept
  Cersei is captured in the sept (event.capture)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-is-captured-in-the-sept.node.md

OUTGOING (2 edges — cersei-is-captured-in-the-sept is source)
------------------------------------------------------------------------
  [CAUSES]  (1 edge)
    -> cersei-is-stripped-and-imprisoned
       ref  : sources/chapters/affc/affc-cersei-10.md:249
       quote: "Inside the cell three silent sisters held her down as a septa named Scolera stri..."
  [LOCATED_AT]  (1 edge)
    -> great-sept-of-baelor
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "seize her at the altar of the Mother"

INCOMING (5 edges — cersei-is-captured-in-the-sept is target)
------------------------------------------------------------------------
  [AGENT_IN]  (1 edge)
    <- the-faith
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Women — septas and silent sisters — seize her at the altar of the Mother. A scor..."
  [CAUSES]  (1 edge)
    <- cersei-rearms-the-faith-and-forgives-the-debt
       ref  : sources/chapters/affc/affc-cersei-10.md:249
       quote: "There were women waiting for her there, more septas and silent sisters too ... t..."
  [COMMANDS_IN]  (1 edge)
    <- high-sparrow
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "The High Septon | Imprisons | Cersei | Arrests her on charges of murder, treason..."
  [TRIGGERS]  (1 edge)
    <- osney-kettleblack-confesses-to-high-sparrow
       ref  : sources/chapters/affc/affc-cersei-10.md:243
       quote: "That one there. She's the queen I fucked, the one sent me to kill the old High S..."
  [VICTIM_IN]  (1 edge)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Women — septas and silent sisters — seize her at the altar of the Mother. A scor..."

========================================================================
SUMMARY: cersei-is-captured-in-the-sept  |  2 outgoing, 5 incoming  (7 total)

==================================================================
## --neighbors cersei-is-stripped-and-imprisoned
========================================================================
NEIGHBORS: cersei-is-stripped-and-imprisoned
  Cersei is stripped and imprisoned (event.capture)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-is-stripped-and-imprisoned.node.md

OUTGOING (1 edges — cersei-is-stripped-and-imprisoned is source)
------------------------------------------------------------------------
  [LOCATED_AT]  (1 edge)
    -> great-sept-of-baelor
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Women — septas and silent sisters — seize her at the altar of the Mother. A scor..."

INCOMING (4 edges — cersei-is-stripped-and-imprisoned is target)
------------------------------------------------------------------------
  [AGENT_IN]  (1 edge)
    <- scolera
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Septa Scolera strips her bare, even her smallclothes."
  [CAUSES]  (1 edge)
    <- cersei-is-captured-in-the-sept
       ref  : sources/chapters/affc/affc-cersei-10.md:249
       quote: "Inside the cell three silent sisters held her down as a septa named Scolera stri..."
  [COMMANDS_IN]  (1 edge)
    <- high-sparrow
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "The High Septon | Imprisons | Cersei | Arrests her on charges of murder, treason..."
  [VICTIM_IN]  (1 edge)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Three silent sisters hold her down while Septa Scolera strips her bare, even her..."

========================================================================
SUMMARY: cersei-is-stripped-and-imprisoned  |  1 outgoing, 4 incoming  (5 total)

==================================================================
## --neighbors faith-militant-uprising
========================================================================
NEIGHBORS: faith-militant-uprising
  Faith Militant uprising (event.battle)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/faith-militant-uprising.node.md

OUTGOING (1 edges — faith-militant-uprising is source)
------------------------------------------------------------------------
  [PRECEDES]  (1 edge)
    -> battle-beneath-the-gods-eye

INCOMING (10 edges — faith-militant-uprising is target)
------------------------------------------------------------------------
  [PART_OF]  (8 edges)
    <- battle-at-stonebridge
       ref  : wiki:Battle_at_Stonebridge
    <- battle-at-the-great-fork
       ref  : wiki:Battle_at_the_Great_Fork
    <- burning-of-jeyne-poore
       ref  : wiki:Burning_of_Jeyne_Poore
    <- burning-of-the-sept-of-remembrance
       ref  : wiki:Burning_of_the_Sept_of_Remembrance
    <- burning-of-the-seats-of-the-pious-lords
       ref  : wiki:Burning_of_the_seats_of_the_pious_lords
    <- hunt-of-the-poor-fellows
       ref  : wiki:Hunt_of_the_Poor_Fellows
    <- nights-watch-rebellion-of-50-ac
       ref  : wiki:Night's_Watch_rebellion_of_50_AC
    <- submission-of-oldtown
       ref  : wiki:Submission_of_Oldtown
  [PRECEDES]  (2 edges)
    <- second-dornish-war
    <- vulture-hunt

========================================================================
SUMMARY: faith-militant-uprising  |  1 outgoing, 10 incoming  (11 total)

==================================================================
## --neighbors cersei-fills-in-the-arrest-warrants
========================================================================
NEIGHBORS: cersei-fills-in-the-arrest-warrants
  Cersei fills in the arrest warrants (event.capture)
  File: /Users/mnoth/source/asoiaf-chat/graph/nodes/events/cersei-fills-in-the-arrest-warrants.node.md

OUTGOING (0 edges — cersei-fills-in-the-arrest-warrants is source)
------------------------------------------------------------------------
  (none)

INCOMING (12 edges — cersei-fills-in-the-arrest-warrants is target)
------------------------------------------------------------------------
  [AGENT_IN]  (2 edges)
    <- cersei-lannister
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names... Gives them to Ser Osfryd."
    <- ser-osfryd
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "Gives them to Ser Osfryd."
  [VICTIM_IN]  (10 edges)
    <- tallad
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: Ser Tallad..."
    <- jalabhar-xho
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Jalabhar Xho..."
    <- hamish-the-harper
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Hamish the Harper..."
    <- hugh-clifton
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Hugh Clifton..."
    <- mark-mullendore
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Mark Mullendore..."
    <- bayard-norcross
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Bayard Norcross..."
    <- lambert-turnberry
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Lambert Turnberry..."
    <- horas-redwyne
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Horas Redwyne..."
    <- hobber-redwyne
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... Hobber Redwyne..."
    <- wat-the-blue-bard
       ref  : sources/chapters/affc/affc-cersei-10.md
       quote: "She writes in ten names: ... and Wat the Blue Bard."

========================================================================
SUMMARY: cersei-fills-in-the-arrest-warrants  |  0 outgoing, 12 incoming  (12 total)

