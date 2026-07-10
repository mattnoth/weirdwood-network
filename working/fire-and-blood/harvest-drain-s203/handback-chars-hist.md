# Handback — packet-chars-hist.json (S203)

Rows from `packet-chars-hist.json` whose true home is NOT a node inside
graph/nodes/{characters,species,houses}/ — i.e. belongs to an event, location,
artifact, concept, medical, or other out-of-scope node type, or spans too many
entities to attach to one node. Each entry: verbatim row JSON + one line on
where it likely belongs (existing node path when found).

23 rows handed back, 0 duplicates dropped here (dup handling is on the attach
side — see final report).

{"row": 1, "snippet": "Th Tergaryen Raccession", "kind": "targaryen-history", "note": "regnal list of Targaryen kings 1-283 AC with parentage and epithets", "unit": "fab-lineages-and-family-tree-25", "line": 15}
-> Section-title/heading text, not a citable prose quote; underlying content is the full multi-king succession table (1–283 AC), not attributable to a single character/house node. Best candidate `graph/nodes/houses/house-targaryen.node.md` if a curator wants to build a proper regnal-list summary from scratch, but the located snippet itself isn't a usable verbatim quote.

{"row": 2, "snippet": "called by singers the Dance of the Dragons", "kind": "targaryen-history", "note": "civil war between Aegon II and Rhaenyra; both perished", "unit": "fab-lineages-and-family-tree-25", "line": 35}
-> Event fact. Home: `graph/nodes/events/dance-of-the-dragons.node.md` (exists).

{"row": 19, "snippet": "Thus did the Kingsguard come into being", "kind": "targaryen-history", "note": "Visenya founds the seven White Swords, vows modeled on the Night's Watch", "unit": "fab-reign-of-the-dragon-04", "line": 283}
-> Event fact (institution founding). Home: `graph/nodes/events/founding-of-the-kingsguard.node.md` (exists).

{"row": 26, "snippet": "These are the names of Aegon's Seven", "kind": "targaryen-history", "note": "roster of the original Kingsguard from the White Book", "unit": "fab-reign-of-the-dragon-04", "line": 295}
-> Event fact, same event as row 19. Home: `graph/nodes/events/founding-of-the-kingsguard.node.md` (exists).

{"row": 27, "snippet": "three kings reigned over the city, each on his own hill", "kind": "targaryen-history", "note": "Moon of the Three Kings, King's Landing under rival \"kings\" after Rhaenyra's flight", "unit": "fab-rhaenyra-overthrown-18-p01", "line": 265}
-> Event/period fact ("Moon of the Three Kings" / "Moon of Madness"), spans three separate pretender-kings (Trystane, Gaemon, the Shepherd) collectively — no single character/house home. No existing event node found for this period; candidate for a future event mint.

{"row": 61, "snippet": "wed Princess Jaehaera, the daughter of Queen Helaena by her brother King Aegon II", "kind": "targaryen-history", "note": "marriage uniting the two Targaryen branches", "unit": "fab-short-sad-reign-of-aegon-ii-19", "line": 287}
-> Wedding event. Home: `graph/nodes/events/wedding-of-aegon-iii-and-jaehaera.node.md` (exists).

{"row": 80, "snippet": "dragon contended with dragon in the sky", "kind": "targaryen-history", "note": "first dragon-vs-dragon battle since the Doom of Valyria", "unit": "fab-sons-of-the-dragon-05-p03", "line": 53}
-> Battle event (Maegor/Balerion vs Prince Aegon/Quicksilver). Home: `graph/nodes/events/battle-beneath-the-gods-eye.node.md` (exists).

{"row": 88, "snippet": "the king's sudden and secret marriage to his sister", "kind": "targaryen-history", "note": "secret Jaehaerys–Alysanne marriage triggers the rift with regents", "unit": "fab-surfeit-of-rulers-08-p01", "line": 35}
-> Wedding event. Home: `graph/nodes/events/wedding-of-jaehaerys-i-targaryen-and-alysanne-targaryen.node.md` (exists).

{"row": 114, "snippet": "the agreement that Grand Maester Munkun calls \"the Pact of Ice and Fire\"", "kind": "targaryen-history", "note": "Pact of Ice and Fire between Jacaerys and Cregan Stark", "unit": "fab-the-blacks-and-the-greens-16-p02", "line": 159}
-> Event/pact fact. Home: `graph/nodes/events/pact-of-ice-and-fire.node.md` (exists).

{"row": 125, "snippet": "seventh day of the seventh moon of the 131st year", "kind": "targaryen-history", "note": "dated coronation-wedding of Aegon III and Jaehaera", "unit": "fab-short-sad-reign-of-aegon-ii-19", "line": 287}
-> Wedding event, same event as row 61. Home: `graph/nodes/events/wedding-of-aegon-iii-and-jaehaera.node.md` (exists).

{"row": 133, "snippet": "Only one man in four survived the Winter Fever", "kind": "targaryen-history", "note": "mortality of the Winter Fever plague", "unit": "fab-the-hooded-hand-21", "line": 307}
-> Medical/plague fact, not character-specific. Home: `graph/nodes/medical/winter-fever.node.md` (exists).

{"row": 135, "snippet": "Oldtown almost three years earlier to cross the Sunset Sea", "kind": "targaryen-history", "note": "Sun Chaser expedition sets out to cross the Sunset Sea", "unit": "fab-the-long-reign-13", "line": 19}
-> Voyage/event fact about the ship, not the captain (Eustace Hightower) specifically. Home: `graph/nodes/events/departure-of-the-sun-chaser-west.node.md` (exists; see also `graph/nodes/artifacts/sun-chaser.node.md`).

{"row": 138, "snippet": "The winter of 59-60 AC was an exceptionally cruel one", "kind": "targaryen-history", "note": "severe winter strikes Westeros", "unit": "fab-the-long-reign-13", "line": 81}
-> General historical/weather event, not character-specific. Home: `graph/nodes/events/winter-of-59-60-ac.node.md` (exists).

{"row": 140, "snippet": "the Shivers came, and the Stranger walked the land", "kind": "targaryen-history", "note": "winter plague of 59 AC sweeps Westeros", "unit": "fab-the-long-reign-cont-14-p01", "line": 17}
-> Medical/plague fact. Home: `graph/nodes/medical/shivers.node.md` or `graph/nodes/events/the-shivers-plague.node.md` (both exist).

{"row": 147, "snippet": "The smallfolk of the time called it Lord Rogar's War", "kind": "targaryen-history", "note": "61 AC campaign against the second Vulture King", "unit": "fab-the-long-reign-cont-14-p01", "line": 187}
-> Campaign/war event, named in-text. Home: `graph/nodes/events/lord-rogars-war.node.md` (exists; see also `graph/nodes/events/third-dornish-war.node.md`).

{"row": 189, "snippet": "as this confrontation would later become known", "kind": "targaryen-history", "note": "the \"secret siege\" of Maegor's Holdfast named", "unit": "fab-the-lysene-spring-24-p02", "line": 29}
-> Event fact. Home: `graph/nodes/events/secret-siege.node.md` (exists).

{"row": 198, "snippet": "the gathering of the lords in 136 AC was the largest assembly of nobles", "kind": "targaryen-history", "note": "near-Great Council of 136 AC", "unit": "fab-the-lysene-spring-24-p02", "line": 119}
-> Political-assembly event fact, no single character/house home. No dedicated event node found for this 136 AC gathering (distinct from the Great Council of 101 AC); candidate for a future event mint.

{"row": 245, "snippet": "the how and when and why of what has become known as the Treasons of Tumbleton", "kind": "targaryen-history", "note": "disputed infiltration and defection at Tumbleton", "unit": "fab-the-red-dragon-and-the-gold-17-p03", "line": 215}
-> Named event ("Treasons of Tumbleton") describing the collective defection/infiltration, not one individual. Closest existing node: `graph/nodes/events/battle-of-tumbleton.node.md`; no dedicated "Treasons of Tumbleton" sub-event found. (Individual defector character nodes `hugh-hammer.node.md` / `ulf-white.node.md` exist if a curator prefers a character-level attach instead.)

{"row": 249, "snippet": "the dragons danced and died above the Gods Eye", "kind": "targaryen-history", "note": "Daemon and Aemond slay each other above the Gods Eye, 130 AC", "unit": "fab-the-red-dragon-and-the-gold-17-p04", "line": 263}
-> Battle event (mutual dragon-duel death). Home: `graph/nodes/events/battle-above-the-gods-eye.node.md` (exists).

{"row": 262, "snippet": "the Doctrine of Exceptionalism", "kind": "targaryen-history", "note": "doctrine crafted to justify Targaryen sibling marriage as a Valyrian exception", "unit": "fab-jaehaerys-and-alysanne-dragonstone-11", "line": 169}
-> Concept/doctrine fact, not a character or house. Home: `graph/nodes/concepts/doctrine-of-exceptionalism.node.md` (exists).

{"row": 290, "snippet": "the Winter Fever descended on Barrowton", "kind": "targaryen-history", "note": "plague reaches farther inland than ever before", "unit": "fab-war-and-peace-and-cattle-shows-22-p02", "line": 21}
-> Medical/plague fact. Home: `graph/nodes/medical/winter-fever.node.md` (exists; see also `graph/nodes/events/winter-fever-reaches-barrowton.node.md`).

{"row": 303, "snippet": "the Year of the Three Brides", "kind": "targaryen-history", "note": "49 AC named for three weddings: Rhaena, the Golden Wedding, Jaehaerys-Alysanne", "unit": "fab-surfeit-of-rulers-08-p01", "line": 37}
-> Named-year fact spanning three separate weddings/events, no single character/house home. No dedicated node found for "Year of the Three Brides" as such (only the source chapter file shares the name); candidate for a future event mint, or fold into the three individual wedding event nodes.

{"row": 306, "snippet": "the War for the White Cloaks", "kind": "targaryen-history", "note": "melees fill five Kingsguard vacancies at the Golden Wedding", "unit": "fab-birth-death-and-betrayal-10", "line": 53}
-> Named event (tourney/melee that filled Kingsguard vacancies at the Golden Wedding). Home: `graph/nodes/events/war-for-the-white-cloaks.node.md` (exists).
