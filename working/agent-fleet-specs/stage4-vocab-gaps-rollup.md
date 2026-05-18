# Stage 4 — Vocab-Gap Rollup (2026-05-18)

Source: `working/wiki/pass2-buckets/questions-for-matt.jsonl` (68 total rows)

Normalized: `working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl`

**Canonical vocab loaded from architecture.md:** 132 edge types.

## Distribution by question_type (normalized)
- `vocabulary-gap`: 36
- `vocab-gap`: 17
- `other`: 6
- `vocab_gap`: 5
- `infrastructure`: 2
- `disambiguation`: 1
- `cross-identity`: 1

## Already resolved

These proposed types are NOW in the canonical vocab (architecture.md). The gap rows are stale — they were filed before the type was added.

- **ATTENDS** — 2 row(s) filed before adoption
- **BETROTHED_TO** — 1 row(s) filed before adoption
- **COUSIN_OF** — 2 row(s) filed before adoption
- **DEPICTED_IN** — 1 row(s) filed before adoption
- **GIFTED_TO** — 1 row(s) filed before adoption
- **KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON** — 1 row(s) filed before adoption
- **MADE_OF** — 1 row(s) filed before adoption
- **MILK_BROTHER_OF** — 1 row(s) filed before adoption
- **NURSED_BY / WET_NURSE_OF** — 1 row(s) filed before adoption
- **UNCLE_OF|NEPHEW_OF** — 1 row(s) filed before adoption

## Open gaps — to be decided this session

Each gap below lists every example evidence we have.

### `AFFLICTED_BY` — 1 occurrence(s)

- `albin-massey` → `shivers` [section=## Origins]
  > Lord Albin perished during the harsh winter of 59 AC from the Shivers.

### `ASSAULTS` — 2 occurrence(s)

- `owen-inchfield` → `brienne-tarth` [section=## Narrative Arc] [batch=batch-0046]
  > A pair of Renly's men, Ser Owen Inchfield and Ser Raymun Fossoway, had told her that if she wanted to enter a melee, she had to be willing to be treated as a man, then attempted to have their way with her. Ser Randyll Tarly stopped them.
  - _description:_ No canonical edge type covers one character physically attacking or attempting to assault another. ASSAULTS is the obvious proposed type. Should we add ASSAULTS(person->person) to the locked vocabulary? Alternatively ATTACKS? The incident with Owen/Brienne is the clearest example but this pattern wi
- `mandon-moore` → `?` [batch=batch-0073]

### `ATTACKS` — 1 occurrence(s)

- `gerold-dayne` → `myrcella-baratheon` [section=## Narrative Arc / ### A Feast for Crows]
  > Amidst the fighting, Gerold attempts to kill Myrcella. Her horse rears, however, and Darkstar succeeds only in slicing off her ear and scarring her face.

### `BRIBES` — 1 occurrence(s)

- `?` → `?` [batch=batch-0008]

### `BUILT` — 1 occurrence(s)

- `?` → `?` [batch=batch-0008]

### `CHILD_OF` — 1 occurrence(s)

- `edric-dayne` → `lord-dayne-father-of-edric` [batch=batch-0014]
  > Edric Dayne is the son of Lord Dayne (his father).

### `COMMISSIONED` — 1 occurrence(s)

- `triston-hightower` → `starry-sept` [section=## Origins]
  > Lord Triston raised the Starry Sept in Robeson's honor after his passing.

### `COMPANION_OF` — 1 occurrence(s)

- `patrek-mallister` → `edmure-tully` [section=## Appearances & Description]
  > He is good friends with Ser Edmure Tully, the heir to Riverrun.

### `COMPETES_IN` — 1 occurrence(s)

- `clarence-charlton` → `wedding-tourney-at-whitewalls` [section=## Narrative Arc] [batch=batch-0010]
  > Clarence Charlton participates in the tourney at Whitewalls. Sandor Clegane unhorsed Renly Baratheon at the Hand's tourney. Gregor Clegane defeated Balon Swann at the Hand's tourney.
  - _description:_ Should COMPETES_IN be added for tournament participation? Current vocab has FIGHTS_IN for battles/wars only — tournament jousts/melee participation have no type. Pattern appears across many characters (clarence-charlton, sandor-clegane, gregor-clegane, and likely 50+ others). COMPETES_IN(character →

### `CONTRACTED_WITH` — 1 occurrence(s)

- `denys-harte` → `faceless-men` [section=## Origins]
  > Denys hired the Faceless Men to assassinate a rival in King's Landing.

### `COURTED` — 1 occurrence(s)

- `cleyton-caswell` → `rohanne-webber` [section=## Origins] [batch=batch-0009]
  > Cleyton Caswell was a suitor who sought to court Rohanne Webber
  - _description:_ Should COURTED (suitor→object-of-courtship) be added? Rohanne Webber famously had many suitors. COURTED is distinct from BETROTHED_TO (no formal betrothal) and MARRIED (no marriage). The suitor relationship is plot-relevant in the Dunk & Egg stories. Alternatively, would ALLIED_WITH do as a fallback

### `COURTS` — 1 occurrence(s)

- `eon-hunter` → `lysa-arryn` [section=## Narrative Arc]
  > Eon is one of Lysa Arryn's suitors after the death of Lord Jon Arryn. As such, he sends wine from his own cellars as a gift to Lysa.

### `CREW_OF` — 1 occurrence(s)

- `gevin-harlaw` → `sea-bitch` [section=## Narrative Arc]
  > Gevin is listed among the crew of *Sea Bitch*.

### `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` — 1 occurrence(s)

- `simon-dondarrion` → `daenerys-targaryen-daughter-of-jaehaerys-i` [batch=batch-0014]
  > Simon Dondarrion crowned Daenerys Targaryen (daughter of Jaehaerys I) Queen of Love and Beauty at a tourney.
  - _description:_ Crowning someone Queen of Love and Beauty at a tournament is a specific meaningful relationship (romantic honor / political statement) with no canonical edge type. Mapped to ATTENDS (simon → daenerys) which doesn't capture the relational act. Should a specific edge type exist, or should CROWNS_QUEEN

### `DAUGHTER_IN_LAW_OF` — 1 occurrence(s)

- `alerie-hightower` → `olenna-tyrell` [section=## Narrative Arc]
  > Alerie echoes her good-mother, Lady Olenna Tyrell, that King Tommen I Baratheon should share a bed with Margaery

### `DEFEATED_BY` — 1 occurrence(s)

- `?` → `?` [batch=batch-0001]

### `DIED_OF` — 2 occurrence(s)

- `donnel-hightower` → `shivers` [section=## Origins]
  > Later that same year, Lord Donnel died from the Shivers.
- `medrick-manderly` → `winter-fever` [section=## Origins]
  > Lord Desmond and the childless Medrick died of Winter Fever four days apart in 132 AC

### `GREAT_UNCLE_OF` — 1 occurrence(s)

- `harrold-hardyng` → `jon-arryn` [section=## Origins]
  > the infant Harrold became the heir presumptive of his great-uncle Jon Arryn, Lord of the Eyrie.

### `GUARDIAN_OF` — 1 occurrence(s)

- `jon-connington` → `aegon-targaryen-son-of-rhaegar` [section=## Biography] [batch=batch-0011]
  > Jon Connington raised and protected Young Griff (Aegon Targaryen) for approximately 12 years in exile across Essos

### `HOSTED_BY / HOST_OF` — 1 occurrence(s)

- `lord-dondarrion-father-of-simon` → `jaehaerys-i-targaryen` [batch=batch-0014]
  > Lord Dondarrion hosted King Jaehaerys I Targaryen and Queen Alysanne at Blackhaven.
  - _description:_ HOSTED_BY / HOST_OF: GUEST_OF(guest → host) exists but HOST_OF(host → guest) does not. When a lord hosts royalty, the lord is the source_slug but there is no canonical edge for 'A hosted B at their castle.' Mapped to CONTEMPORARY_WITH. Also: should GUEST_OF be used instead (inverting direction from 

### `HOST_OF` — 1 occurrence(s)

- `ralph-buckler` → `oberyn-martell` [section=## Narrative Arc] [batch=batch-0007]
  > Lord Buckler hosts Prince Oberyn Martell and his entourage
  - _description:_ Should HOST_OF (host→guest, inverse of GUEST_OF) be added? ralph-buckler hosts oberyn-martell. GUEST_OF (guest→host) exists but no inverse. Would HOST_OF be a redundant symmetric equivalent, or a distinct directed type?

### `KINSMAN_OF` — 1 occurrence(s)

- `arthor-celtigar` → `bartimos-celtigar` [section=## Origins] [batch=batch-0009]
  > Arthor was in the manse of his kinsman, Lord Bartimos Celtigar
  - _description:_ Should KINSMAN_OF be added for unspecified kinship (cousin, uncle, etc.) where the exact degree is unknown? Currently emitting RELATED_TO as fallback, but that's very generic. KINSMAN_OF would be more semantically specific. Alternatively, should we infer the specific degree from other evidence, or j

### `LIAISED_WITH` — 1 occurrence(s)

- `mylenda-caron` → `walder-frey-son-of-ryman` [section=## Appearances & Description] [batch=batch-0009]
  > Mylenda is rumored to have had an affair with Walder Frey, the son of Ryman Frey
  - _description:_ Should LOVERS_WITH or LIAISED_WITH be added for rumored/attested affairs? Current vocab has no type for romantic liaisons that aren't formal marriages. ALLIED_WITH is too political; RELATED_TO is wrong (no kinship). This pattern recurs for bastard-producing affairs and noble scandal relationships.

### `MEMORIALIZED_IN` — 1 occurrence(s)

- `robeson` → `starry-sept` [section=## Origins]
  > Lord Triston raised the Starry Sept in Robeson's honor after his passing.

### `NAMED_AFTER` — 1 occurrence(s)

- `rickard-karstark` → `rickard-stark` [batch=batch-0049]
  > Rickard Karstark was named after Lord Rickard Stark
  - _description:_ No edge type exists for naming/eponym relationships. NAMED_AFTER or NAMESAKE_OF would cover cases where a person is named in honor of another person.

### `NAMED_FOR` — 1 occurrence(s)

- `gwynesse-harlaw` → `widows-tower-ten-towers` [section=## Origins]
  > One of the towers of the castle was renamed the Widow's Tower in her honor.

### `PARTICIPATES_IN` — 1 occurrence(s)

- `medrick-manderly` → `hour-of-the-wolf` [section=## Origins]
  > During the Hour of the Wolf after the war, Medrick agreed to transport those men taking the black

### `PETITIONED` — 1 occurrence(s)

- `?` → `?` [batch=batch-0005]
  > barba-bolton: Barba petitioned Aegon III to send food to the North if he didn't choose her as queen

### `PROPOSED_AS_BRIDE` — 1 occurrence(s)

- `hotho-harlaws-daughter` → `victarion-greyjoy` [section=## Narrative Arc]
  > Hotho offers his support to Victarion Greyjoy and offers the Lord Captain his daughter for his queen.

### `PURCHASED_FROM|SOLD_TO|TRANSACTS_WITH` — 1 occurrence(s)

- `henly-ashford` → `duncan-the-tall` [section=## Narrative Arc] [batch=batch-0001]
  > Henly Ashford purchases a horse (Sweetfoot) from Duncan the Tall at the tourney at Ashford Meadow.
  - _description:_ Clear commercial transaction between characters — no type in current 121-type vocab covers commerce/purchase between persons. Emitted OWNS→sweetfoot for the resulting ownership. The purchaser→seller relationship has no home. Recommend PURCHASED_FROM(buyer→seller) or similar.

### `RELATED_TO` — 1 occurrence(s)

- `horas-harroway` → `alys-harroway` [section=## Origins]
  > every family member of hers present in King's Landing was executed. Horas was thrown onto the spikes of the dry moat around Maegor's Holdfast.

### `REPUTED_AS` — 1 occurrence(s)

- `patrice-hightower` → `magic` [batch=batch-0037]
  > She was a reputed witch
  - _description:_ Character has a social reputation for being a magic practitioner or witch. No existing type covers attribution of a trait/reputation to a character. PERCEIVED_AS requires both endpoints to be characters. HAS_ATTRIBUTE would fit but does not exist. Proposed: REPUTED_AS(character -> concept/trait) for

### `RESURRECTED_BY` — 1 occurrence(s)

- `beric-dondarrion` → `thoros-of-myr` [batch=batch-0014]
  > Thoros of Myr resurrected Beric Dondarrion multiple times via the Lord of Light.
  - _description:_ RESURRECTED_BY (resurrected → resurrector): RESURRECTS(resurrector → resurrected) exists but the reverse direction has no canonical type. When beric-dondarrion is the source_slug, there is no correct edge. Mapped to CONTEMPORARY_WITH as fallback. Should RESURRECTED_BY be added as the reverse of RESU

### `SERVED_BY|EMPLOYS` — 1 occurrence(s)

- `?` → `?` [batch=batch-0005]
  > ramsay-snow→reek: Ramsay employed Reek as a serving man; SERVES(reek→ramsay) is inverse only

### `SLAIN_BY_WEAPON|KILLED_WIELDING` — 1 occurrence(s)

- `?` → `?` [batch=batch-0012]
  > slain by Orphan-Maker

### `STEP_PARENT_OF` — 1 occurrence(s)

- `bethany-hightower` → `samantha-tarly` [section=## Origins]
  > During the Dance of the Dragons, her father married again to Samantha Tarly, but Ormund died in the First Battle of Tumbleton.

### `USES_AS_SIGIL` — 1 occurrence(s)

- `?` → `?` [batch=batch-0001]

## Untyped vocab-gap rows (no extractable proposed_type)

7 row(s) had question_type=vocabulary-gap but no extractable proposed_type field. These need manual inspection or must be re-filed in canonical schema.

- row#12 `melisandre` → `glamor / shadow-child / nightfire`
  - Melisandre creates and employs shadow children (concept.magic) and glamors (concept.magic), and holds nightfires (concept.magic) as priestly practice. These are clear relational edges — she is the pra…
- row#13 `melisandre` → `wedding-of-sigorn-and-alys-karstark`
  - Melisandre officiates/performs the wedding ceremony at the Wedding of Sigorn and Alys Karstark (event.battle in the node graph). The relationship is 'character officiates at event' but no vocabulary t…
- row#16 `maelys-i-blackfyre` → `daemon-i-blackfyre`
  - Several Blackfyre characters are described as descendants of Daemon I Blackfyre or other ancestors. The natural edge direction ANCESTOR_OF(ancestor→descendant) exists, but the candidate shape presents…
- row#17 `baelor-blacktyde` → `kingsmoot-of-299-ac`
  - Baelor Blacktyde attended the kingsmoot on Old Wyk where Euron Greyjoy was crowned. ATTENDS has already been proposed (q-2026-05-14-characters-house-baratheon-of-dragonstone-014) for social/ceremonial…
- row#18 `bennarion-botley` → `germund-botley`
  - Kinship vocabulary lacks uncle/nephew (and aunt/niece) types. PARENT_OF covers one generation; SIBLING_OF covers same generation; ANCESTOR_OF covers more than one generation. Uncle/nephew is one gener…
- row#19 `germund-botley` → `kingsmoot`
  - Kingsmoot attendance reinforces prior gap (q-2026-05-14-batch-0004-vocab-gap-002 for ATTENDS). Germund Botley listed as one of Euron's champions at the kingsmoot — political assembly attendance, not a…
- row#20 `alysanne-bracken` → `gregor-clegane`
  - No edge type exists for sexual violence victimization. Five Bracken sisters (Alysanne, Barbara, Bess, Catelyn, Jayne) each have wiki prose stating they were raped by Gregor Clegane during the Burning …
