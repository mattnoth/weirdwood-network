# Variant-generation collisions — step 4b (S190)

Generated: 2026-07-07T03:30:11.021858+00:00


152 phrase(s) (across 2 table(s)) where a deterministically-generated plural/possessive/article variant collided with an existing alias for a DIFFERENT slug. Logged for review, not auto-resolved — the existing PRIORITY_ORDER means a real alias/name/slug always wins over a generated variant; these are cases where TWO OR MORE real slugs are already tied to the target phrase, so no single winner exists even before the variant arrived.


## Table: event-alias-lookup.json (18 phrase(s))


### `the andal invasion`

- slug=`andal-invasion` source=`variant-article` raw="variant of 'andal invasion'"
- slug=`coming-of-the-andals` source=`variant-article` raw="variant of 'andal invasion'"

### `the ashford tourney`

- slug=`ashford-tourney` source=`variant-article` raw="variant of 'ashford tourney'"
- slug=`tourney-at-ashford-meadow` source=`variant-article` raw="variant of 'ashford tourney'"

### `the battle of the crag`

- slug=`battle-of-the-crag` source=`variant-article` raw="variant of 'battle of the crag'"
- slug=`storming-of-the-crag` source=`variant-article` raw="variant of 'battle of the crag'"

### `the battle of torrhens square`

- slug=`battle-of-torrhens-square` source=`variant-article` raw="variant of 'battle of torrhens square'"
- slug=`fight-at-torrhens-square` source=`variant-article` raw="variant of 'battle of torrhens square'"

### `the battle of tumbleton`

- slug=`battle-of-tumbleton` source=`variant-article` raw="variant of 'battle of tumbleton'"
- slug=`first-battle-of-tumbleton` source=`variant-article` raw="variant of 'battle of tumbleton'"

### `the battle of whispering wood`

- slug=`battle-in-the-whispering-wood` source=`variant-article` raw="variant of 'battle of whispering wood'"
- slug=`battle-of-whispering-wood` source=`variant-article` raw="variant of 'battle of whispering wood'"

### `the battle of yunkai`

- slug=`battle-near-yunkai` source=`variant-article` raw="variant of 'battle of yunkai'"
- slug=`battle-of-yunkai` source=`variant-article` raw="variant of 'battle of yunkai'"

### `the blackfyre rebellion`

- slug=`blackfyre-rebellion` source=`variant-article` raw="variant of 'blackfyre rebellion'"
- slug=`first-blackfyre-rebellion` source=`variant-article` raw="variant of 'blackfyre rebellion'"

### `the coming of the andals`

- slug=`coming-of-the-andals` source=`variant-article` raw="variant of 'coming of the andals'"
- slug=`andal-invasion` source=`variant-article` raw="variant of 'coming of the andals'"

### `the conquest of dorne`

- slug=`conquest-of-dorne` source=`variant-article` raw="variant of 'conquest of dorne'"
- slug=`the-conquest-of-dorne` source=`variant-article` raw="variant of 'conquest of dorne'"

### `the greyjoy rebellion`

- slug=`greyjoy-rebellion` source=`variant-article` raw="variant of 'greyjoy rebellion'"
- slug=`greyjoys-rebellion` source=`variant-article` raw="variant of 'greyjoy rebellion'"

### `the lodos the twice-drowned's rebellion`

- slug=`lodos-the-twice-drowneds-revolt` source=`variant-article` raw='variant of "lodos the twice-drowned\'s rebellion"'
- slug=`lodos-the-twice-drowneds-rebellion` source=`variant-article` raw='variant of "lodos the twice-drowned\'s rebellion"'

### `the lord rogars war`

- slug=`lord-rogars-war` source=`variant-article` raw="variant of 'lord rogars war'"
- slug=`third-dornish-war` source=`variant-article` raw="variant of 'lord rogars war'"

### `the mummer's farce`

- slug=`grand-northern-conspiracy` source=`variant-article` raw='variant of "mummer\'s farce"'
- slug=`wyman-manderly-stages-fake-execution-of-davos` source=`variant-article` raw='variant of "mummer\'s farce"'

### `the regent wars`

- slug=`regency-of-aegon-iii` source=`variant-article` raw="variant of 'regent wars'"
- slug=`regent-wars` source=`variant-article` raw="variant of 'regent wars'"

### `the siege of storm's end`

- slug=`siege-of-storms-end` source=`variant-article` raw='variant of "siege of storm\'s end"'
- slug=`siege-of-storms-end-299` source=`variant-article` raw='variant of "siege of storm\'s end"'
- slug=`siege-of-storms-end-300` source=`variant-article` raw='variant of "siege of storm\'s end"'

### `the tourney at storms end`

- slug=`lord-steffons-tourney` source=`variant-article` raw="variant of 'tourney at storms end'"
- slug=`tourney-at-storms-end` source=`variant-article` raw="variant of 'tourney at storms end'"

### `the tourney of maidenpool`

- slug=`tourney-at-maidenpool` source=`variant-article` raw="variant of 'tourney of maidenpool'"
- slug=`tourney-of-maidenpool` source=`variant-article` raw="variant of 'tourney of maidenpool'"

## Table: all-node-alias-lookup.json (134 phrase(s))


### `bastards`

- slug=`bastards` source=`all-node-slug:characters` raw=''
- slug=`bastard` source=`variant-plural` raw=''

### `bloodroyals`

- slug=`bloodroyal` source=`variant-plural` raw=''
- slug=`the-bloodroyal` source=`variant-plural` raw=''

### `bones`

- slug=`bones` source=`all-node-slug:locations` raw=''
- slug=`bone` source=`variant-plural` raw=''

### `captain of the guards`

- slug=`captain-of-the-guards` source=`all-node-slug:factions` raw=''
- slug=`captain-of-the-guard` source=`variant-plural` raw=''

### `justiciars`

- slug=`justiciar` source=`variant-plural` raw=''
- slug=`master-of-laws` source=`variant-plural` raw=''

### `keyholder`

- slug=`keyholder` source=`all-node-slug:titles` raw=''
- slug=`keyholders` source=`variant-plural` raw=''

### `keyholders`

- slug=`keyholders` source=`all-node-slug:titles` raw=''
- slug=`keyholder` source=`variant-plural` raw=''

### `king of winters`

- slug=`king-in-the-north` source=`variant-plural` raw=''
- slug=`king-of-winter` source=`variant-plural` raw=''

### `king's of winter`

- slug=`king-in-the-north` source=`variant-possessive` raw=''
- slug=`king-of-winter` source=`variant-possessive` raw=''

### `lord treasurers`

- slug=`lord-treasurer` source=`variant-plural` raw=''
- slug=`master-of-coin` source=`variant-plural` raw=''

### `lord's treasurer`

- slug=`lord-treasurer` source=`variant-possessive` raw=''
- slug=`master-of-coin` source=`variant-possessive` raw=''

### `maesters`

- slug=`maesters` source=`all-node-slug:factions` raw=''
- slug=`maester` source=`variant-plural` raw=''

### `sparrow`

- slug=`sparrow` source=`all-node-slug:species` raw=''
- slug=`sparrows` source=`variant-plural` raw=''

### `spymasters`

- slug=`master-of-whisperers` source=`variant-plural` raw=''
- slug=`spymaster` source=`variant-plural` raw=''

### `stewards`

- slug=`stewards` source=`all-node-slug:factions` raw=''
- slug=`steward` source=`variant-plural` raw=''

### `the addam of hull`

- slug=`addam-of-hull` source=`variant-article` raw=''
- slug=`addam-velaryon` source=`variant-article` raw=''

### `the aemon targaryen`

- slug=`aemon-targaryen-son-of-maekar-i` source=`variant-article` raw=''
- slug=`aemon-targaryen` source=`variant-article` raw=''

### `the andal`

- slug=`jorah-mormont` source=`variant-article` raw=''
- slug=`andals` source=`variant-article` raw=''

### `the archer`

- slug=`anguy` source=`variant-article` raw=''
- slug=`archer` source=`variant-article` raw=''

### `the arya stark`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`jeyne-poole` source=`variant-article` raw=''

### `the aurochs`

- slug=`grenn` source=`variant-article` raw=''
- slug=`aurochs` source=`variant-article` raw=''

### `the ben`

- slug=`ben` source=`variant-article` raw=''
- slug=`edmund-blackwood` source=`variant-article` raw=''

### `the betrayer`

- slug=`hugh-hammer` source=`variant-article` raw=''
- slug=`ulf-white` source=`variant-article` raw=''

### `the black betha`

- slug=`black-betha` source=`variant-article` raw=''
- slug=`betha-blackwood` source=`variant-article` raw=''

### `the black bride`

- slug=`elinor-costayne` source=`variant-article` raw=''
- slug=`jeyne-westerling-wife-of-maegor-i` source=`variant-article` raw=''
- slug=`elinor-costayne` source=`variant-article` raw=''
- slug=`rhaena-targaryen-daughter-of-aenys-i` source=`variant-article` raw=''

### `the black pearl of braavos`

- slug=`bellegere-otherys` source=`variant-article` raw=''
- slug=`bellenora-otherys` source=`variant-article` raw=''
- slug=`bellegere-otherys` source=`variant-article` raw=''
- slug=`bellonara-otherys` source=`variant-article` raw=''

### `the blind beth`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`arya-trains-blind-and-regains-her-sight` source=`variant-article` raw=''

### `the bloodroyal`

- slug=`bloodroyal` source=`variant-article` raw=''
- slug=`the-bloodroyal` source=`variant-article` raw=''

### `the boy`

- slug=`bastards-bastard` source=`variant-article` raw=''
- slug=`boy-thrall` source=`variant-article` raw=''
- slug=`bastards-bastard` source=`variant-article` raw=''
- slug=`boy` source=`variant-article` raw=''

### `the boy king`

- slug=`daeron-i-targaryen` source=`variant-article` raw=''
- slug=`joffrey-baratheon` source=`variant-article` raw=''
- slug=`daeron-i-targaryen` source=`variant-article` raw=''
- slug=`tommen-baratheon` source=`variant-article` raw=''

### `the broken nose`

- slug=`broken-nose` source=`variant-article` raw=''
- slug=`rorge` source=`variant-article` raw=''

### `the cass`

- slug=`cass` source=`variant-article` raw=''
- slug=`cassandra-baratheon` source=`variant-article` raw=''

### `the cat`

- slug=`catelyn-stark` source=`variant-article` raw=''
- slug=`spotted-cat` source=`variant-article` raw=''
- slug=`catelyn-stark` source=`variant-article` raw=''
- slug=`cat` source=`variant-article` raw=''

### `the cat of the canals`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`arya-becomes-cat-of-the-canals` source=`variant-article` raw=''

### `the clanker lord`

- slug=`chezdhar-zo-rhaezn` source=`variant-article` raw=''
- slug=`grazdhan-zo-rhaezn` source=`variant-article` raw=''
- slug=`chezdhar-zo-rhaezn` source=`variant-article` raw=''
- slug=`maezon-zo-rhaezn` source=`variant-article` raw=''

### `the coming of the andals`

- slug=`andal-invasion` source=`variant-article` raw=''
- slug=`coming-of-the-andals` source=`variant-article` raw=''

### `the conquest of dorne`

- slug=`the-conquest-of-dorne` source=`variant-article` raw=''
- slug=`conquest-of-dorne` source=`variant-article` raw=''

### `the damon the devout`

- slug=`damon-hightower` source=`variant-article` raw=''
- slug=`damon-morrigen` source=`variant-article` raw=''

### `the dance of the dragons`

- slug=`the-dance-of-the-dragons` source=`variant-article` raw=''
- slug=`dance-of-the-dragons` source=`variant-article` raw=''

### `the dancer`

- slug=`dancer` source=`variant-article` raw=''
- slug=`dhazzar` source=`variant-article` raw=''

### `the dog`

- slug=`sandor-clegane` source=`variant-article` raw=''
- slug=`dog` source=`variant-article` raw=''

### `the dragon queen`

- slug=`daenerys-targaryen` source=`variant-article` raw=''
- slug=`rhaenyra-targaryen` source=`variant-article` raw=''

### `the dragon twin`

- slug=`baela-targaryen` source=`variant-article` raw=''
- slug=`rhaena-targaryen-daughter-of-daemon` source=`variant-article` raw=''

### `the duck`

- slug=`rolly-duckfield` source=`variant-article` raw=''
- slug=`duck` source=`variant-article` raw=''

### `the esgred`

- slug=`asha-greyjoy` source=`variant-article` raw=''
- slug=`esgred` source=`variant-article` raw=''

### `the false knight`

- slug=`rickard-thorne` source=`variant-article` raw=''
- slug=`willis-fell` source=`variant-article` raw=''

### `the frog`

- slug=`quentyn-martell` source=`variant-article` raw=''
- slug=`frog` source=`variant-article` raw=''

### `the garin the great`

- slug=`garin-the-great` source=`variant-article` raw=''
- slug=`shrouded-lord` source=`variant-article` raw=''

### `the giant`

- slug=`bedwyck` source=`variant-article` raw=''
- slug=`giants` source=`variant-article` raw=''

### `the goat`

- slug=`vargo-hoat` source=`variant-article` raw=''
- slug=`goat` source=`variant-article` raw=''

### `the goldenhand`

- slug=`garth-vii-gardener` source=`variant-article` raw=''
- slug=`jaime-lannister` source=`variant-article` raw=''

### `the greybeard`

- slug=`greenbeard` source=`variant-article` raw=''
- slug=`hugh-grandison` source=`variant-article` raw=''

### `the griffin`

- slug=`jon-connington` source=`variant-article` raw=''
- slug=`griffin` source=`variant-article` raw=''

### `the haggon`

- slug=`haggon` source=`variant-article` raw=''
- slug=`varamyr` source=`variant-article` raw=''

### `the hagon the terrible`

- slug=`hagon-hoare` source=`variant-article` raw=''
- slug=`hagon-the-terrible` source=`variant-article` raw=''

### `the hammer`

- slug=`baelor-targaryen-son-of-daeron-ii` source=`variant-article` raw=''
- slug=`hammer` source=`variant-article` raw=''

### `the hardhand`

- slug=`hardhand` source=`variant-article` raw=''
- slug=`harwyn-hoare` source=`variant-article` raw=''

### `the hero`

- slug=`harghaz` source=`variant-article` raw=''
- slug=`hero` source=`variant-article` raw=''

### `the horse`

- slug=`hareth-moles-town` source=`variant-article` raw=''
- slug=`horse` source=`variant-article` raw=''

### `the iron king`

- slug=`balon-greyjoy` source=`variant-article` raw=''
- slug=`iron-king` source=`variant-article` raw=''

### `the joff`

- slug=`joffrey-baratheon` source=`variant-article` raw=''
- slug=`joffrey-velaryon` source=`variant-article` raw=''

### `the jonquil`

- slug=`jonquil` source=`variant-article` raw=''
- slug=`sansa-stark` source=`variant-article` raw=''

### `the justiciar`

- slug=`justiciar` source=`variant-article` raw=''
- slug=`master-of-laws` source=`variant-article` raw=''

### `the king in the north`

- slug=`king-in-the-north` source=`variant-article` raw=''
- slug=`robb-proclaimed-king-in-the-north` source=`variant-article` raw=''

### `the king of the giants`

- slug=`mag-mar-tun-doh-weg` source=`variant-article` raw=''
- slug=`king-of-the-giants` source=`variant-article` raw=''

### `the king of winter`

- slug=`king-in-the-north` source=`variant-article` raw=''
- slug=`king-of-winter` source=`variant-article` raw=''

### `the kingsmoot`

- slug=`kingsmoot` source=`variant-article` raw=''
- slug=`kingsmoot-on-old-wyk` source=`variant-article` raw=''

### `the knight`

- slug=`harras-harlaw` source=`variant-article` raw=''
- slug=`knight` source=`variant-article` raw=''

### `the last dragon`

- slug=`last-dragon` source=`variant-article` raw=''
- slug=`rhaegar-targaryen` source=`variant-article` raw=''

### `the last greenseer`

- slug=`brynden-rivers` source=`variant-article` raw=''
- slug=`three-eyed-crow` source=`variant-article` raw=''

### `the laughing lion`

- slug=`laughing-lion` source=`variant-article` raw=''
- slug=`tytos-lannister` source=`variant-article` raw=''

### `the lemon`

- slug=`lem` source=`variant-article` raw=''
- slug=`lemon` source=`variant-article` raw=''

### `the little queen`

- slug=`daenaera-velaryon` source=`variant-article` raw=''
- slug=`margaery-tyrell` source=`variant-article` raw=''

### `the lorath`

- slug=`jaqen-hghar` source=`variant-article` raw=''
- slug=`lorath` source=`variant-article` raw=''

### `the lord brynden`

- slug=`brynden-rivers` source=`variant-article` raw=''
- slug=`three-eyed-crow` source=`variant-article` raw=''

### `the lord of bones`

- slug=`lord-of-bones` source=`variant-article` raw=''
- slug=`mance-rayder` source=`variant-article` raw=''

### `the lord renly`

- slug=`lord-renly` source=`variant-article` raw=''
- slug=`garlan-tyrell` source=`variant-article` raw=''

### `the lord stokeworth`

- slug=`bronn` source=`variant-article` raw=''
- slug=`lord-stokeworth` source=`variant-article` raw=''

### `the lord treasurer`

- slug=`lord-treasurer` source=`variant-article` raw=''
- slug=`master-of-coin` source=`variant-article` raw=''

### `the manticore`

- slug=`amory-lorch` source=`variant-article` raw=''
- slug=`manticore` source=`variant-article` raw=''

### `the merry`

- slug=`meralyn` source=`variant-article` raw=''
- slug=`meredyth-crane` source=`variant-article` raw=''
- slug=`meralyn` source=`variant-article` raw=''
- slug=`merianne-frey` source=`variant-article` raw=''

### `the monkey`

- slug=`pypar` source=`variant-article` raw=''
- slug=`monkey` source=`variant-article` raw=''

### `the mother of dragons`

- slug=`mother-of-dragons` source=`variant-article` raw=''
- slug=`dragon-hatching-on-drogo-pyre` source=`variant-article` raw=''

### `the mouse`

- slug=`marilda-of-hull` source=`variant-article` raw=''
- slug=`mouse` source=`variant-article` raw=''

### `the mummer's farce`

- slug=`grand-northern-conspiracy` source=`variant-article` raw=''
- slug=`wyman-manderly-stages-fake-execution-of-davos` source=`variant-article` raw=''

### `the ned`

- slug=`eddard-stark` source=`variant-article` raw=''
- slug=`edric-dayne` source=`variant-article` raw=''

### `the night wolf`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`nymeria-direwolf` source=`variant-article` raw=''

### `the nymeria`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`nymeria-direwolf` source=`variant-article` raw=''
- slug=`arya-stark` source=`variant-article` raw=''
- slug=`nymeria` source=`variant-article` raw=''

### `the pate`

- slug=`alchemist` source=`variant-article` raw=''
- slug=`high-septon-stonemason` source=`variant-article` raw=''
- slug=`alchemist` source=`variant-article` raw=''
- slug=`pate-novice` source=`variant-article` raw=''
- slug=`alchemist` source=`variant-article` raw=''
- slug=`steely-pate` source=`variant-article` raw=''

### `the plague face`

- slug=`kindly-man` source=`variant-article` raw=''
- slug=`plague-face` source=`variant-article` raw=''

### `the pork pies`

- slug=`pork-pie` source=`variant-article` raw=''
- slug=`manderly-bakes-the-frey-pies` source=`variant-article` raw=''

### `the prince of dragonstone`

- slug=`maegor-i-targaryen` source=`variant-article` raw=''
- slug=`prince-of-dragonstone` source=`variant-article` raw=''

### `the prince that was promised`

- slug=`aegon-targaryen-son-of-rhaegar` source=`variant-article` raw=''
- slug=`daenerys-targaryen` source=`variant-article` raw=''
- slug=`aegon-targaryen-son-of-rhaegar` source=`variant-article` raw=''
- slug=`rhaegar-targaryen` source=`variant-article` raw=''
- slug=`aegon-targaryen-son-of-rhaegar` source=`variant-article` raw=''
- slug=`stannis-baratheon` source=`variant-article` raw=''
- slug=`aegon-targaryen-son-of-rhaegar` source=`variant-article` raw=''
- slug=`the-prince-that-was-promised` source=`variant-article` raw=''

### `the qohorik`

- slug=`vargo-hoat` source=`variant-article` raw=''
- slug=`qohorik` source=`variant-article` raw=''

### `the quent`

- slug=`quent` source=`variant-article` raw=''
- slug=`quentyn-martell` source=`variant-article` raw=''

### `the rabbit`

- slug=`faezhar-zo-faez` source=`variant-article` raw=''
- slug=`rabbit` source=`variant-article` raw=''

### `the randa`

- slug=`myranda-royce` source=`variant-article` raw=''
- slug=`randa` source=`variant-article` raw=''

### `the rat`

- slug=`rast` source=`variant-article` raw=''
- slug=`rat` source=`variant-article` raw=''

### `the renly's ghost`

- slug=`garlan-tyrell` source=`variant-article` raw=''
- slug=`garlan-tyrell-routs-stannis-as-renly-s-ghost` source=`variant-article` raw=''

### `the rob`

- slug=`rob` source=`variant-article` raw=''
- slug=`robert-i-baratheon` source=`variant-article` raw=''

### `the rose lord`

- slug=`leo-tyrell-longthorn` source=`variant-article` raw=''
- slug=`mace-tyrell` source=`variant-article` raw=''

### `the rugen`

- slug=`rugen` source=`variant-article` raw=''
- slug=`varys` source=`variant-article` raw=''

### `the sam the slayer`

- slug=`samwell-tarly` source=`variant-article` raw=''
- slug=`sam-kills-the-other` source=`variant-article` raw=''

### `the sea lion`

- slug=`leo-costayne` source=`variant-article` raw=''
- slug=`lymond-hightower` source=`variant-article` raw=''

### `the sea snake`

- slug=`corlys-velaryon` source=`variant-article` raw=''
- slug=`sea-snake` source=`variant-article` raw=''

### `the ser`

- slug=`gregor-clegane` source=`variant-article` raw=''
- slug=`ser` source=`variant-article` raw=''

### `the ser stupid`

- slug=`hosteen-frey` source=`variant-article` raw=''
- slug=`ser-stupid` source=`variant-article` raw=''

### `the she-bear`

- slug=`alysane-mormont` source=`variant-article` raw=''
- slug=`maege-mormont` source=`variant-article` raw=''

### `the shrouded lord`

- slug=`garin-the-great` source=`variant-article` raw=''
- slug=`shrouded-lord` source=`variant-article` raw=''

### `the silent sister`

- slug=`catelyn-stark` source=`variant-article` raw=''
- slug=`silent-sisters` source=`variant-article` raw=''

### `the silver`

- slug=`silver-mare` source=`variant-article` raw=''
- slug=`silver` source=`variant-article` raw=''

### `the smiler`

- slug=`justin-massey` source=`variant-article` raw=''
- slug=`smiler` source=`variant-article` raw=''

### `the snail`

- slug=`uthor-underleaf` source=`variant-article` raw=''
- slug=`snail` source=`variant-article` raw=''

### `the snake`

- slug=`corlys-velaryon` source=`variant-article` raw=''
- slug=`oberyn-martell` source=`variant-article` raw=''
- slug=`corlys-velaryon` source=`variant-article` raw=''
- slug=`snake` source=`variant-article` raw=''

### `the sphinx`

- slug=`alleras` source=`variant-article` raw=''
- slug=`sphinx` source=`variant-article` raw=''

### `the spider`

- slug=`varys` source=`variant-article` raw=''
- slug=`spider` source=`variant-article` raw=''

### `the spymaster`

- slug=`master-of-whisperers` source=`variant-article` raw=''
- slug=`spymaster` source=`variant-article` raw=''

### `the squirrel`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`geoff` source=`variant-article` raw=''
- slug=`arya-stark` source=`variant-article` raw=''
- slug=`squirrel` source=`variant-article` raw=''

### `the stone head`

- slug=`halder` source=`variant-article` raw=''
- slug=`stone-head` source=`variant-article` raw=''

### `the talon`

- slug=`talon` source=`variant-article` raw=''
- slug=`oswin-arryn` source=`variant-article` raw=''

### `the three-eyed crow`

- slug=`brynden-rivers` source=`variant-article` raw=''
- slug=`three-eyed-crow` source=`variant-article` raw=''

### `the turnip`

- slug=`tom-turnip` source=`variant-article` raw=''
- slug=`turnip` source=`variant-article` raw=''

### `the ty`

- slug=`ty` source=`variant-article` raw=''
- slug=`tywin-frey` source=`variant-article` raw=''

### `the usurper`

- slug=`robert-i-baratheon` source=`variant-article` raw=''
- slug=`usurper` source=`variant-article` raw=''

### `the varys`

- slug=`rugen` source=`variant-article` raw=''
- slug=`varys` source=`variant-article` raw=''

### `the vulture`

- slug=`vulture-king-jaehaerys-i` source=`variant-article` raw=''
- slug=`vulture` source=`variant-article` raw=''

### `the wat barleycorn`

- slug=`wat-barleycorn` source=`variant-article` raw=''
- slug=`wet-wat` source=`variant-article` raw=''

### `the weasel`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`weasel` source=`variant-article` raw=''

### `the wet nurse`

- slug=`tyrek-lannister` source=`variant-article` raw=''
- slug=`wet-nurse` source=`variant-article` raw=''

### `the will`

- slug=`will` source=`variant-article` raw=''
- slug=`willam-wells` source=`variant-article` raw=''
- slug=`will` source=`variant-article` raw=''
- slug=`willam` source=`variant-article` raw=''

### `the winged knight`

- slug=`artys-i-arryn` source=`variant-article` raw=''
- slug=`winged-knight` source=`variant-article` raw=''

### `the wolf girl`

- slug=`arya-stark` source=`variant-article` raw=''
- slug=`lyanna-stark` source=`variant-article` raw=''
- slug=`arya-stark` source=`variant-article` raw=''
- slug=`sansa-stark` source=`variant-article` raw=''

### `the woods witch`

- slug=`ghost-of-high-heart` source=`variant-article` raw=''
- slug=`woods-witch` source=`variant-article` raw=''

### `warlocks`

- slug=`warlocks` source=`all-node-slug:factions` raw=''
- slug=`warlock` source=`variant-plural` raw=''
