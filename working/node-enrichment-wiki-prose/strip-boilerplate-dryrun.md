# Strip-boilerplate dry-run report (read-only, no graph writes)

Total nodes with boilerplate: **6711**
- Rich (has other body content already): **5490**
- Thin (Identity+Edges only, nothing else): **1221**

## Type-gloss variants (count)

-  2509  character.human
-   901  location
-   528  title
-   408  character
-   344  meta.chapter
-   334  species
-   263  artifact (named weapon, ship, or object)
-   243  noble house
-   222  event.battle
-   155  text/book/song
-   153  place.location
-    70  food or drink
-    65  organization/faction
-    61  culture/people
-    55  organization.house
-    54  battle/event
-    46  religion/faith
-    45  fan theory / interpretive framework
-    44  organization.faction
-    35  tournament/tourney
-    28  magical concept/practice
-    21  war
-    18  character.dragon
-    17  artifact
-    15  place.region
-    14  religion or divine entity
-    12  region
-    10  concept
-     8  dragon
-     8  event.war
-     5  culture
-     5  faction
-     4  human
-     4  material
-     3  organization.religion
-     2  prophecy
-     1  object.artifact
-     1  text

## RICH nodes — Shape A (strip tail only) sample rows

These already have real body content below Identity; stripping the tail leaves a harmless one-line stub.

### _conflicts
- `graph/nodes/_conflicts/house-warrick-houses-other-h-w-2026-04-28T04-56-33.node.md`
  - before: House Warrick is a organization.house from the AWOIAF wiki.
  - after:  House Warrick is a organization.house.

### artifacts
- `graph/nodes/artifacts/adventure.node.md`
  - before: Adventure is an artifact (named weapon, ship, or object) from the AWOIAF wiki.
  - after:  Adventure is an artifact (named weapon, ship, or object).
- `graph/nodes/artifacts/arakh.node.md`
  - before: Arakh is a artifact from the AWOIAF wiki.
  - after:  Arakh is a artifact.
- `graph/nodes/artifacts/arbor-queen.node.md`
  - before: Arbor Queen is a artifact from the AWOIAF wiki.
  - after:  Arbor Queen is a artifact.

### chapters
- `graph/nodes/chapters/a-clash-of-kings-chapter-1.node.md`
  - before: A Clash of Kings-Chapter 1 is a meta.chapter from the AWOIAF wiki.
  - after:  A Clash of Kings-Chapter 1 is a meta.chapter.
- `graph/nodes/chapters/a-clash-of-kings-chapter-10.node.md`
  - before: A Clash of Kings-Chapter 10 is a meta.chapter from the AWOIAF wiki.
  - after:  A Clash of Kings-Chapter 10 is a meta.chapter.
- `graph/nodes/chapters/a-clash-of-kings-chapter-11.node.md`
  - before: A Clash of Kings-Chapter 11 is a meta.chapter from the AWOIAF wiki.
  - after:  A Clash of Kings-Chapter 11 is a meta.chapter.

### characters
- `graph/nodes/characters/a-certain-man.node.md`
  - before: A certain man is a character from the AWOIAF wiki.
  - after:  A certain man is a character.
- `graph/nodes/characters/abelar-hightower.node.md`
  - before: Abelar Hightower is a character from the AWOIAF wiki.
  - after:  Abelar Hightower is a character.
- `graph/nodes/characters/addam-frey.node.md`
  - before: Addam Frey is a character.human from the AWOIAF wiki.
  - after:  Addam Frey is a character.human.

### concepts
- `graph/nodes/concepts/alchemy.node.md`
  - before: Alchemy is a magical concept/practice from the AWOIAF wiki.
  - after:  Alchemy is a magical concept/practice.
- `graph/nodes/concepts/battle-fever.node.md`
  - before: Battle fever is a concept from the AWOIAF wiki.
  - after:  Battle fever is a concept.
- `graph/nodes/concepts/bloodmage.node.md`
  - before: Bloodmage is a magical concept/practice from the AWOIAF wiki.
  - after:  Bloodmage is a magical concept/practice.

### customs
- `graph/nodes/customs/barrow.node.md`
  - before: Barrow is a species from the AWOIAF wiki.
  - after:  Barrow is a species.
- `graph/nodes/customs/bedding.node.md`
  - before: Bedding is a species from the AWOIAF wiki.
  - after:  Bedding is a species.
- `graph/nodes/customs/blood-price.node.md`
  - before: Blood price is a species from the AWOIAF wiki.
  - after:  Blood price is a species.

### events
- `graph/nodes/events/aegon-the-uncrowneds-rebellion.node.md`
  - before: Aegon the Uncrowned's rebellion is a event.battle from the AWOIAF wiki.
  - after:  Aegon the Uncrowned's rebellion is a event.battle.
- `graph/nodes/events/aegons-conquest.node.md`
  - before: Aegon's Conquest is a event.battle from the AWOIAF wiki.
  - after:  Aegon's Conquest is a event.battle.
- `graph/nodes/events/aegons-coronations.node.md`
  - before: Aegon's coronations is a battle/event from the AWOIAF wiki.
  - after:  Aegon's coronations is a battle/event.

### factions
- `graph/nodes/factions/adventurers.node.md`
  - before: Adventurers is an organization/faction from the AWOIAF wiki.
  - after:  Adventurers is an organization/faction.
- `graph/nodes/factions/alchemists-guild.node.md`
  - before: Alchemists' Guild is a organization.faction from the AWOIAF wiki.
  - after:  Alchemists' Guild is a organization.faction.
- `graph/nodes/factions/ancient-guild-of-spicers.node.md`
  - before: Ancient Guild of Spicers is a organization.faction from the AWOIAF wiki.
  - after:  Ancient Guild of Spicers is a organization.faction.

### foods
- `graph/nodes/foods/alcoholic-beverages.node.md`
  - before: Alcoholic beverages is a food or drink from the AWOIAF wiki.
  - after:  Alcoholic beverages is a food or drink.
- `graph/nodes/foods/apple.node.md`
  - before: Apple is a food or drink from the AWOIAF wiki.
  - after:  Apple is a food or drink.
- `graph/nodes/foods/aurochs.node.md`
  - before: Aurochs is a food or drink from the AWOIAF wiki.
  - after:  Aurochs is a food or drink.

### houses
- `graph/nodes/houses/barrow-kings.node.md`
  - before: Barrow Kings is a noble house from the AWOIAF wiki.
  - after:  Barrow Kings is a noble house.
- `graph/nodes/houses/house-ambrose.node.md`
  - before: House Ambrose is a noble house from the AWOIAF wiki.
  - after:  House Ambrose is a noble house.
- `graph/nodes/houses/house-antaryon.node.md`
  - before: House Antaryon is a organization.house from the AWOIAF wiki.
  - after:  House Antaryon is a organization.house.

### languages
- `graph/nodes/languages/astapori-language.node.md`
  - before: Astapori language is a species from the AWOIAF wiki.
  - after:  Astapori language is a species.
- `graph/nodes/languages/braavosi-language.node.md`
  - before: Braavosi language is a species from the AWOIAF wiki.
  - after:  Braavosi language is a species.
- `graph/nodes/languages/common-tongue.node.md`
  - before: Common Tongue is a species from the AWOIAF wiki.
  - after:  Common Tongue is a species.

### locations
- `graph/nodes/locations/acorn-hall.node.md`
  - before: Acorn Hall is a place.location from the AWOIAF wiki.
  - after:  Acorn Hall is a place.location.
- `graph/nodes/locations/acorn-water.node.md`
  - before: Acorn Water is a location from the AWOIAF wiki.
  - after:  Acorn Water is a location.
- `graph/nodes/locations/aegon-rhaenys-and-visenya-islands.node.md`
  - before: Aegon, Rhaenys, and Visenya (islands) is a location from the AWOIAF wiki.
  - after:  Aegon, Rhaenys, and Visenya (islands) is a location.

### materials
- `graph/nodes/materials/amber.node.md`
  - before: Amber is a species from the AWOIAF wiki.
  - after:  Amber is a species.
- `graph/nodes/materials/amethyst.node.md`
  - before: Amethyst is a species from the AWOIAF wiki.
  - after:  Amethyst is a species.
- `graph/nodes/materials/beryl.node.md`
  - before: Beryl is a species from the AWOIAF wiki.
  - after:  Beryl is a species.

### medical
- `graph/nodes/medical/blindeye.node.md`
  - before: Blindeye is a species from the AWOIAF wiki.
  - after:  Blindeye is a species.
- `graph/nodes/medical/bloody-flux.node.md`
  - before: Bloody flux is a species from the AWOIAF wiki.
  - after:  Bloody flux is a species.
- `graph/nodes/medical/brownleg.node.md`
  - before: Brownleg is a species from the AWOIAF wiki.
  - after:  Brownleg is a species.

### prophecies
- `graph/nodes/prophecies/the-prince-that-was-promised.node.md`
  - before: The prince that was promised is a prophecy from the AWOIAF wiki.
  - after:  The prince that was promised is a prophecy.

### religions
- `graph/nodes/religions/bakkalon.node.md`
  - before: Bakkalon is a religion/faith from the AWOIAF wiki.
  - after:  Bakkalon is a religion/faith.
- `graph/nodes/religions/black-goat.node.md`
  - before: Black Goat is a religion or divine entity from the AWOIAF wiki.
  - after:  Black Goat is a religion or divine entity.
- `graph/nodes/religions/boash.node.md`
  - before: Boash is a religion or divine entity from the AWOIAF wiki.
  - after:  Boash is a religion or divine entity.

### species
- `graph/nodes/species/ape.node.md`
  - before: Ape is a species from the AWOIAF wiki.
  - after:  Ape is a species.
- `graph/nodes/species/badger.node.md`
  - before: Badger is a species from the AWOIAF wiki.
  - after:  Badger is a species.
- `graph/nodes/species/basilisk.node.md`
  - before: Basilisk is a species from the AWOIAF wiki.
  - after:  Basilisk is a species.

### texts
- `graph/nodes/texts/a-caution-for-young-girls.node.md`
  - before: A Caution for Young Girls is a text/book/song from the AWOIAF wiki.
  - after:  A Caution for Young Girls is a text/book/song.
- `graph/nodes/texts/a-consideration-of-history.node.md`
  - before: A Consideration of History is a text/book/song from the AWOIAF wiki.
  - after:  A Consideration of History is a text/book/song.
- `graph/nodes/texts/a-rose-of-gold.node.md`
  - before: A Rose of Gold is a text/book/song from the AWOIAF wiki.
  - after:  A Rose of Gold is a text/book/song.

### theories
- `graph/nodes/theories/death-of-laenor-velaryon-and-harwin-strong-theories.node.md`
  - before: Death of Laenor Velaryon and Harwin Strong/Theories is a fan theory / interpretive framework from the AWOIAF wiki.
  - after:  Death of Laenor Velaryon and Harwin Strong/Theories is a fan theory / interpretive framework.
- `graph/nodes/theories/frey-pies-theories.node.md`
  - before: Frey Pies/Theories is a fan theory / interpretive framework from the AWOIAF wiki.
  - after:  Frey Pies/Theories is a fan theory / interpretive framework.

### titles
- `graph/nodes/titles/acolyte-alchemists-guild.node.md`
  - before: Acolyte (Alchemists' Guild) is a title from the AWOIAF wiki.
  - after:  Acolyte (Alchemists' Guild) is a title.
- `graph/nodes/titles/archer.node.md`
  - before: Archer is a title from the AWOIAF wiki.
  - after:  Archer is a title.
- `graph/nodes/titles/archon-of-tyrosh.node.md`
  - before: Archon of Tyrosh is a title from the AWOIAF wiki.
  - after:  Archon of Tyrosh is a title.

## THIN nodes — Shape A vs alternatives (Matt's decision)

These have NOTHING else in the node body — Identity + Edges only. Shape A leaves a contentless
one-line stub; alternatives are dropping the line entirely or composing a real sentence (LLM, later).

### _conflicts
- `graph/nodes/_conflicts/aerys-targaryen.node.md`
  - before:   Aerys Targaryen is a character from the AWOIAF wiki.
  - Shape A (strip tail):  Aerys Targaryen is a character.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/_conflicts/tourney-of-maidenpool.node.md`
  - before:   Tourney of Maidenpool is a tournament/tourney from the AWOIAF wiki.
  - Shape A (strip tail):  Tourney of Maidenpool is a tournament/tourney.
  - Shape B (drop line):   *(Identity section left empty)*

### artifacts
- `graph/nodes/artifacts/brave-magister.node.md`
  - before:   Brave Magister is an artifact (named weapon, ship, or object) from the AWOIAF wiki.
  - Shape A (strip tail):  Brave Magister is an artifact (named weapon, ship, or object).
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/artifacts/esgred-ship.node.md`
  - before:   Esgred (ship) is an artifact (named weapon, ship, or object) from the AWOIAF wiki.
  - Shape A (strip tail):  Esgred (ship) is an artifact (named weapon, ship, or object).
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/artifacts/hags-teeth.node.md`
  - before:   Hag's Teeth is an artifact (named weapon, ship, or object) from the AWOIAF wiki.
  - Shape A (strip tail):  Hag's Teeth is an artifact (named weapon, ship, or object).
  - Shape B (drop line):   *(Identity section left empty)*

### characters
- `graph/nodes/characters/abelon.node.md`
  - before:   Abelon is a character from the AWOIAF wiki.
  - Shape A (strip tail):  Abelon is a character.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/characters/addam-of-hull.node.md`
  - before:   Addam of Hull is a character from the AWOIAF wiki.
  - Shape A (strip tail):  Addam of Hull is a character.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/characters/addam-rivers.node.md`
  - before:   Addam Rivers is a character from the AWOIAF wiki.
  - Shape A (strip tail):  Addam Rivers is a character.
  - Shape B (drop line):   *(Identity section left empty)*

### concepts
- `graph/nodes/concepts/aeromancer.node.md`
  - before:   Aeromancer is a magical concept/practice from the AWOIAF wiki.
  - Shape A (strip tail):  Aeromancer is a magical concept/practice.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/concepts/maegi.node.md`
  - before:   Maegi is a magical concept/practice from the AWOIAF wiki.
  - Shape A (strip tail):  Maegi is a magical concept/practice.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/concepts/night-lands.node.md`
  - before:   Night lands is a culture from the AWOIAF wiki.
  - Shape A (strip tail):  Night lands is a culture.
  - Shape B (drop line):   *(Identity section left empty)*

### customs
- `graph/nodes/customs/customs.node.md`
  - before:   Customs is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Customs is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/customs/jewelry.node.md`
  - before:   Jewelry is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Jewelry is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/customs/polygamy.node.md`
  - before:   Polygamy is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Polygamy is a species.
  - Shape B (drop line):   *(Identity section left empty)*

### events
- `graph/nodes/events/alayne-i-the-winds-of-winter.node.md`
  - before:   Alayne I (The Winds of Winter) is a event.battle from the AWOIAF wiki.
  - Shape A (strip tail):  Alayne I (The Winds of Winter) is a event.battle.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/events/ashford-tourney.node.md`
  - before:   Ashford Tourney is a tournament/tourney from the AWOIAF wiki.
  - Shape A (strip tail):  Ashford Tourney is a tournament/tourney.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/events/attack-on-old-wyk.node.md`
  - before:   Attack on Old Wyk is a event.battle from the AWOIAF wiki.
  - Shape A (strip tail):  Attack on Old Wyk is a event.battle.
  - Shape B (drop line):   *(Identity section left empty)*

### factions
- `graph/nodes/factions/asshaii.node.md`
  - before:   Asshai'i is a culture/people from the AWOIAF wiki.
  - Shape A (strip tail):  Asshai'i is a culture/people.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/factions/astapori.node.md`
  - before:   Astapori is a culture/people from the AWOIAF wiki.
  - Shape A (strip tail):  Astapori is a culture/people.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/factions/braavosi.node.md`
  - before:   Braavosi is a culture/people from the AWOIAF wiki.
  - Shape A (strip tail):  Braavosi is a culture/people.
  - Shape B (drop line):   *(Identity section left empty)*

### foods
- `graph/nodes/foods/foods-and-beverages.node.md`
  - before:   Foods and beverages is a food or drink from the AWOIAF wiki.
  - Shape A (strip tail):  Foods and beverages is a food or drink.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/foods/mackerel.node.md`
  - before:   Mackerel is a food or drink from the AWOIAF wiki.
  - Shape A (strip tail):  Mackerel is a food or drink.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/foods/octopod.node.md`
  - before:   Octopod is a food or drink from the AWOIAF wiki.
  - Shape A (strip tail):  Octopod is a food or drink.
  - Shape B (drop line):   *(Identity section left empty)*

### houses
- `graph/nodes/houses/azure-emperors.node.md`
  - before:   Azure emperors is a noble house from the AWOIAF wiki.
  - Shape A (strip tail):  Azure emperors is a noble house.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/houses/grey-emperors.node.md`
  - before:   Grey emperors is a noble house from the AWOIAF wiki.
  - Shape A (strip tail):  Grey emperors is a noble house.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/houses/house-algood.node.md`
  - before:   House Algood is a noble house from the AWOIAF wiki.
  - Shape A (strip tail):  House Algood is a noble house.
  - Shape B (drop line):   *(Identity section left empty)*

### languages
- `graph/nodes/languages/ibbenese-language.node.md`
  - before:   Ibbenese language is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Ibbenese language is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/languages/languages.node.md`
  - before:   Languages is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Languages is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/languages/pronunciation-guide.node.md`
  - before:   Pronunciation guide is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Pronunciation guide is a species.
  - Shape B (drop line):   *(Identity section left empty)*

### locations
- `graph/nodes/locations/adakhakileki.node.md`
  - before:   Adakhakileki is a location from the AWOIAF wiki.
  - Shape A (strip tail):  Adakhakileki is a location.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/locations/amberly.node.md`
  - before:   Amberly is a place.location from the AWOIAF wiki.
  - Shape A (strip tail):  Amberly is a place.location.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/locations/antler-river.node.md`
  - before:   Antler River is a location from the AWOIAF wiki.
  - Shape A (strip tail):  Antler River is a location.
  - Shape B (drop line):   *(Identity section left empty)*

### materials
- `graph/nodes/materials/basalt.node.md`
  - before:   Basalt is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Basalt is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/materials/black-stone.node.md`
  - before:   Black stone is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Black stone is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/materials/carnelian.node.md`
  - before:   Carnelian is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Carnelian is a species.
  - Shape B (drop line):   *(Identity section left empty)*

### medical
- `graph/nodes/medical/bronze-pate.node.md`
  - before:   Bronze pate is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Bronze pate is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/medical/dancing-plague.node.md`
  - before:   Dancing plague is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Dancing plague is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/medical/green-fever.node.md`
  - before:   Green fever is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Green fever is a species.
  - Shape B (drop line):   *(Identity section left empty)*

### prophecies
- `graph/nodes/prophecies/the-song-of-ice-and-fire.node.md`
  - before:   The Song Of Ice And Fire is a prophecy from the AWOIAF wiki.
  - Shape A (strip tail):  The Song Of Ice And Fire is a prophecy.
  - Shape B (drop line):   *(Identity section left empty)*

### religions
- `graph/nodes/religions/aquan-the-red-bull.node.md`
  - before:   Aquan the Red Bull is a religion/faith from the AWOIAF wiki.
  - Shape A (strip tail):  Aquan the Red Bull is a religion/faith.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/religions/balerion-god.node.md`
  - before:   Balerion (god) is a religion/faith from the AWOIAF wiki.
  - Shape A (strip tail):  Balerion (god) is a religion/faith.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/religions/black-goat-of-qohor.node.md`
  - before:   Black Goat of Qohor is a religion or divine entity from the AWOIAF wiki.
  - Shape A (strip tail):  Black Goat of Qohor is a religion or divine entity.
  - Shape B (drop line):   *(Identity section left empty)*

### species
- `graph/nodes/species/bestiary.node.md`
  - before:   Bestiary is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Bestiary is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/species/chimera.node.md`
  - before:   Chimera is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Chimera is a species.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/species/coral.node.md`
  - before:   Coral is a species from the AWOIAF wiki.
  - Shape A (strip tail):  Coral is a species.
  - Shape B (drop line):   *(Identity section left empty)*

### texts
- `graph/nodes/texts/a-cask-of-ale.node.md`
  - before:   A Cask of Ale is a text/book/song from the AWOIAF wiki.
  - Shape A (strip tail):  A Cask of Ale is a text/book/song.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/texts/a-thousand-eyes-and-one.node.md`
  - before:   A Thousand Eyes, and One is a text/book/song from the AWOIAF wiki.
  - Shape A (strip tail):  A Thousand Eyes, and One is a text/book/song.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/texts/account-of-the-war-of-the-ninepenny-kings.node.md`
  - before:   Account of the War of the Ninepenny Kings is a text/book/song from the AWOIAF wiki.
  - Shape A (strip tail):  Account of the War of the Ninepenny Kings is a text/book/song.
  - Shape B (drop line):   *(Identity section left empty)*

### theories
- `graph/nodes/theories/aegon-targaryen-son-of-rhaegar-theories.node.md`
  - before:   Aegon Targaryen (son of Rhaegar)/Theories is a fan theory / interpretive framework from the AWOIAF wiki.
  - Shape A (strip tail):  Aegon Targaryen (son of Rhaegar)/Theories is a fan theory / interpretive framework.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/theories/alleras-theories.node.md`
  - before:   Alleras/Theories is a fan theory / interpretive framework from the AWOIAF wiki.
  - Shape A (strip tail):  Alleras/Theories is a fan theory / interpretive framework.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/theories/azor-ahai-theories.node.md`
  - before:   Azor Ahai/Theories is a fan theory / interpretive framework from the AWOIAF wiki.
  - Shape A (strip tail):  Azor Ahai/Theories is a fan theory / interpretive framework.
  - Shape B (drop line):   *(Identity section left empty)*

### titles
- `graph/nodes/titles/acolyte.node.md`
  - before:   Acolyte is a title from the AWOIAF wiki.
  - Shape A (strip tail):  Acolyte is a title.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/titles/admiral-of-the-narrow-sea.node.md`
  - before:   Admiral of the Narrow Sea is a title from the AWOIAF wiki.
  - Shape A (strip tail):  Admiral of the Narrow Sea is a title.
  - Shape B (drop line):   *(Identity section left empty)*
- `graph/nodes/titles/alchemists-of-lys.node.md`
  - before:   Alchemists of Lys is a title from the AWOIAF wiki.
  - Shape A (strip tail):  Alchemists of Lys is a title.
  - Shape B (drop line):   *(Identity section left empty)*
