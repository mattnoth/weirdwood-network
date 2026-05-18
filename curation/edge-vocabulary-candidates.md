# Edge Vocabulary — Candidate Additions

> **What this is:** Proposed new edge types for `reference/architecture.md` § "Edge Types (Relationship Categories)". These are candidates surfaced ahead of Stage 4 prose-edge classification (Session 53, 2026-05-13), based on relationships present in ASOIAF prose that don't cleanly fit any of the current locked types.
>
> **Status of each entry:** `proposed` (here for review), `under-review` (Matt looking at it), `accepted` (added to architecture.md), `rejected` (rejected with reason — kept here for posterity so it doesn't get re-proposed).
>
> **Process to formally adopt:**
> 1. Matt reviews this file, marks each entry `accepted` or `rejected`.
> 2. For each `accepted` entry, append a row to `reference/architecture.md` § "Edge Types" in the appropriate subsection.
> 3. If the type is producible by wiki infobox, also add to `FIELD_EDGE_MAP` in `scripts/wiki-infobox-parser.py` and re-run the parser. *(None of Session 53's accepted types are infobox-producible — they're all prose-derived.)*
> 4. Update the prose-edge-classifier vocabulary expansion in `.claude/agents/prose-edge-classifier.md`.
> 5. Mark the entry `accepted` and date it.
>
> **Source of truth for the actual vocabulary remains `reference/architecture.md`.** This file is the proposal/review surface, not the canonical list. Once an entry is accepted, the row in architecture.md is authoritative.
>
> **Companion surface:** `working/edge-vocabulary-gaps.md` — agent-filed gap questions aggregated by `scripts/build-vocab-gap-log.py`. These are *empirical* gaps discovered during classification runs. This file is *prospective* — types I expect we'll need based on knowing the corpus.

---

## Session 53 Review Outcome (2026-05-13)

**Accepted: 13 new types + 1 reverse-direction note. Rejected: 0. Marginal/deferred: 4 coverage-gap topics.**

Master vocabulary went from ~100 types (14 subsections) → ~114 types (15 subsections) with a new **Magic & Supernatural** subsection. All 14 new types are *prose-derived only* (no infobox source), so `scripts/wiki-infobox-parser.py` was NOT modified — only `reference/architecture.md` and `.claude/agents/prose-edge-classifier.md`.

Live canonical count after adoption: **114** (`scripts/build-edge-type-counts.py` confirms). 56 unpopulated types are Stage 4's targets (was 42 before adoption; the 14 new types are all 0-instance until classifier runs).

Matt's inline review notes from his 2026-05-13 pass are preserved verbatim in each entry below.

---

## Proposed (Session 53, 2026-05-13) — all reviewed

> Matt's inline notes preserved verbatim. Each entry now reflects review outcome.

Yes - Dreams also play an intregal part and are connected to prophecy as well (targaryeans are known to have prophetic dreams.) Worth an edge. 
### `DREAMS_OF`

**Category:** Prophecy (per Matt's "connected to prophecy" note — Targaryen prophetic-dreaming lineage)
**Directionality:** Dreamer → Subject
**Status:** **accepted 2026-05-13** → added to architecture.md § Prophecy subsection.

**Definition:** A character has a recurring or significant dream/vision about a person, place, event, or symbol. Distinct from `FORESHADOWS` (which is a narrative-craft edge: detail X foreshadows event Y for the reader) — `DREAMS_OF` is an in-world dream relation.

**Why not `FORESHADOWS`:** dreams that are *in-world* (Bran's three-eyed-crow visions, Dany's House of the Undying visions, Jojen's greendreams) are dream-content, not narrative foreshadowing. The same vision might foreshadow nothing (red herring) or fulfill literally; that's a separate question about the dream's relation to events. `FORESHADOWS` is a reader-facing meta-edge; `DREAMS_OF` is a character-facing edge.

**Why not `KNOWS`:** dreams aren't reliable knowledge. Bran dreams of his father in the crypt before knowing he's dead — that's not knowledge until confirmed.

**Examples:**
- Bran DREAMS_OF the three-eyed crow (AGOT Bran II onward)
- Daenerys DREAMS_OF Rhaegar / Aerys / her unborn child (multiple)
- Jojen DREAMS_OF the sea coming to Winterfell (ACOK Bran chapters)
- Theon DREAMS_OF the dead at the feast at Winterfell (ADWD)
- Jaime DREAMS_OF Brienne in a weirwood-stump cave (ASOS)

Estimated corpus coverage: 40-80 dream-relation pairs across the 5 books (Bran alone has dozens).

---

### `WARGS_INTO`

Aboslutely should be an entity type. 
**Category:** Magic & Supernatural (new subsection — see Matt's "Bonded to works" note, which produced both WARGS_INTO and BONDED_TO as a paired-but-distinct set)
**Directionality:** Warg → Vessel
**Status:** **accepted 2026-05-13** → added to architecture.md § Magic & Supernatural.

**Definition:** A warg / skinchanger inhabits the consciousness of an animal or (rarely) a person. Distinct from `BONDED_TO` (which is the static relationship) — `WARGS_INTO` is the active mental occupation moments.

**Examples:**
- Bran WARGS_INTO Summer (AGOT onward), Hodor (ACOK onward), the heart tree (ADWD)
- Arya WARGS_INTO Nymeria (recurring dreams from ACOK)
- Varamyr Sixskins WARGS_INTO his wolf, eagle, shadowcat, etc. (ADWD Prologue)
- Orell WARGS_INTO his eagle (ACOK-ASOS)
- Jon Snow WARGS_INTO Ghost (low-key throughout; explicit ADWD)

Corpus coverage: 6-12 warg-animal pairs.

---

### `SACRIFICES`

Yes - examples are perfect. 
**Category:** Magic & Supernatural (ritual context — see Matt's note that this is distinct from combat killing)
**Directionality:** Sacrificer → Victim
**Status:** **accepted 2026-05-13** → added to architecture.md § Magic & Supernatural.

**Definition:** Deliberate ritual or magical killing where the act has supernatural/symbolic purpose, distinct from regular violence. Often involves fire, blood, or invocation of a deity.

**Examples:**
- Mirri Maz Duur SACRIFICES Drogo (or Khal-Drogo's life-essence) (AGOT)
- Daenerys SACRIFICES her unborn child / Mirri / herself in the pyre (AGOT) **— Matt's refinement: she sacrifices her unborn child to do magic on the dragon eggs (Drogo's pyre = the hatching ritual)**
- Stannis (via Melisandre) SACRIFICES leeched blood of Edric Storm (ASOS)
- Stannis SACRIFICES Penny's brother / Alester Florent / Mance(?) / Shireen(?) (ADWD)
- Craster SACRIFICES his sons to the Others (recurring lore)

Corpus coverage: 15-25 ritual sacrifice events.

---

### `RESURRECTS`

Yup. def need this. RESRRECTS over raises. ie catlyn does this as well when she is stone heart at the end of AFFC we learn this i think.
*(Note: Matt's read on Catelyn-as-Stoneheart was that she resurrects others — actually she's the one who got resurrected (by Beric, ASOS Epilogue). As Lady Stoneheart she hangs Freys, not resurrects them. Keeping Catelyn as RESURRECTED target, not resurrector.)*

**Category:** Magic & Supernatural
**Directionality:** Resurrector → Resurrected
**Status:** **accepted 2026-05-13** as `RESURRECTS` (not `RAISES`, per Matt's preference) → added to architecture.md § Magic & Supernatural.

**Definition:** One character returns another from death via supernatural means. Distinct from `HEALS` (medical), distinct from `KILLED_BY` (semantic reverse). **Also absorbed:** Qyburn's reanimation of the Mountain + Red Priest revivals broadly (Thoros, Moqorro) — both moved here from the HEALS list per Matt's notes that "Qyburn is more zombie situation" and "Red Priests mostly resurrect."

**Examples:**
- Thoros of Myr RESURRECTS Beric Dondarrion (ASOS, 6+ times)
- Beric Dondarrion RESURRECTS Catelyn Stark → Lady Stoneheart (ASOS Epilogue)
- Coldhands — RESURRECTED by an unknown force (Children of the Forest? probably) — implied throughout ADWD
- Patchface — drowned-and-resurrected, prophetic afterward (ACOK onward)
- Qyburn RESURRECTS the Mountain → "Ser Robert Strong" (AFFC-ADWD)
- Red Priests broadly perform this (Thoros, Moqorro)
- Possibly Jon Snow at the end of ADWD (cliffhanger; theory-tier)

Corpus coverage: 8-15 resurrection events (Mountain + Red Priest expansion pushed range up).

---

### `VOWS_TO`

Yes, good. Breaking VOW may be something we should look at.
*(Matt's "Breaking VOW" follow-on → added paired type `BREAKS_VOW` to capture oath-breaking arcs.)*

**Category:** Political & Authority
**Directionality:** Vow-maker → Recipient
**Status:** **accepted 2026-05-13** → added to architecture.md § Political & Authority. **Paired `BREAKS_VOW` also added** (Vow-breaker → Vow-recipient).

**Definition:** A personal, named oath made by one character to another. Distinct from `SWORN_TO` (feudal allegiance to a house/lord, structural) — `VOWS_TO` is a one-off promise with named recipient.

**Examples:**
- Ned VOWS_TO Lyanna (to protect her son? canonical R+L=J reading) (pre-AGOT, backstory)
- Brienne VOWS_TO Renly (Kingsguard oath); VOWS_TO Catelyn (find Sansa) (ACOK-ASOS-AFFC)
- Jaime VOWS_TO Catelyn (deliver her daughters) (ASOS)
- Jon VOWS_TO Mance (?) / Stannis / Night's Watch (multiple)
- Arya VOWS_TO herself (her prayer list)

**`BREAKS_VOW` examples:**
- Jaime BREAKS_VOW (Kingsguard oath, by killing Aerys) (pre-AGOT)
- Theon BREAKS_VOW (foster-bond to Robb, capturing Winterfell) (ACOK)
- Robb BREAKS_VOW (Frey betrothal, by marrying Jeyne Westerling) (ASOS — and the Red Wedding is the consequence)
- The Boltons BREAKS_VOW (guest right at the Red Wedding) (ASOS)

Corpus coverage: ~30-60 vow relations + ~10-15 named oath-breakings.

---

### `TUTORS`

YES! love it

**Category:** Knowledge & Information
**Directionality:** Tutor → Student
**Status:** **accepted 2026-05-13** → added to architecture.md § Knowledge & Information.

**Definition:** Sustained formal one-on-one mentorship — narrower than `TEACHES`.

**Examples:**
- Syrio Forel TUTORS Arya Stark (water-dancing)
- Maester Cressen TUTORS Stannis & Robert & Renly (childhood)
- Maester Aemon TUTORS Samwell Tarly (raven-keeper training, ASOS-AFFC)
- Septa Mordane TUTORS Sansa
- Tyrion TUTORS Tommen briefly (ASOS)
- Old Nan TUTORS Bran in stories (informal but sustained)
- Faceless Men TUTORS Arya (AFFC-ADWD Braavos)

Corpus coverage: 20-40 tutoring relations.

---

### `HEALS`

Yes probably, but unclear
*(Matt's clarifying notes on Qyburn and Red Priests pushed those examples to RESURRECTS instead. HEALS now narrowed strictly to medical/maester treatment of the living.)*

**Category:** Knowledge & Information
**Directionality:** Healer → Healed
**Status:** **accepted 2026-05-13** (narrowed scope) → added to architecture.md § Knowledge & Information.

**Definition:** Medical or maester treatment — restoration of a living body, NOT resurrection of the dead (use `RESURRECTS`).

**Examples (narrowed):**
- Maester Luwin HEALS Bran (after fall)
- Maester Aemon HEALS Sam (recurring)
- Mirri Maz Duur claims to HEAL Drogo (subverted; she actually SACRIFICES him — the wiki edge would be both: claim of HEALS, reality of SACRIFICES)
- Sandor Clegane is HEALED BY an unnamed septon (ASOS-AFFC; off-page)
- Maester Pylos / Cressen / Pycelle (various)

**Moved to RESURRECTS:**
- ~~Qyburn HEALS the Mountain~~ → `RESURRECTS` (reanimation)
- ~~Red Priests broadly HEAL~~ → `RESURRECTS` (they mostly revive the dead)

Corpus coverage: 20-40 healing events (narrowed from 30-50 after RESURRECTS reassignment).

---

### `POISONS`

Yes
**Category:** Military & Conflict
**Directionality:** Poisoner → Poisoned
**Status:** **accepted 2026-05-13** → added to architecture.md § Military & Conflict.

**Definition:** Specific form of `KILLS` / `EXECUTES` via poison. Distinct because **method matters narratively** in ASOIAF — Joffrey's poisoning is a major plot point; the precise poison (strangler) and source matter for whodunnit.

**Examples:**
- Olenna POISONS Joffrey (ASOS Red Wedding-adjacent)
- Cressen attempts to POISON Melisandre & himself (ACOK Prologue)
- Tyrion is wrongly accused of POISONING Joffrey
- Quaithe / Pyat Pree attempt to POISON Daenerys (ACOK House of the Undying)
- Lysa POISONS Jon Arryn (backstory, revealed AGOT/ASOS)
- Maester Cressen self-POISONS (ACOK Prologue)
- Sansa's tears at Joffrey's wedding (theory tier: she POISONED him via Tyrion's cup)

Corpus coverage: 12-20 poisoning events.

---

### `CURSES`

Yes
**Category:** Magic & Supernatural (new subsection)
**Directionality:** Curser → Cursed
**Status:** **accepted 2026-05-13** → added to architecture.md § Magic & Supernatural.

**Definition:** A character or magical force lays a curse on another character, place, or thing. May overlap with `PROPHESIED_BY` when the curse takes prophetic form (Maggy → Cersei).

**Examples:**
- The Curse of Harrenhal (collective; multiple lords have died as castellans)
- Mirri Maz Duur CURSES Drogo / Daenerys (AGOT — "when the sun rises in the west...")
- Maggy the Frog CURSES Cersei (the Valonqar prophecy; AFFC)
- Old Nan tells of the curse on Night's King

Corpus coverage: 8-15 curse events.

---

### `MARRIES_OFF`

I think yes

**Category:** Kinship & Family
**Directionality:** Arranger → Married-off person
**Status:** **accepted 2026-05-13** → added to architecture.md § Kinship & Family.

**Definition:** A parent / overlord / king arranges a marriage for another person. Distinct from `SPOUSE_OF` (the marriage itself) — captures the arranger's agency as a political instrument.

**Examples:**
- Tywin MARRIES_OFF Cersei to Robert; Tyrion to Sansa; planned Cersei to Loras
- Walder Frey MARRIES_OFF his daughters/granddaughters constantly
- Catelyn MARRIES_OFF Robb (broken; ASOS)
- Olenna MARRIES_OFF Margaery serially (Renly → Joffrey → Tommen)
- Doran MARRIES_OFF Arianne (planned, to Viserys; AFFC)

Corpus coverage: 25-50 marriage-arrangement relations.

---

### `RANSOMS`

Yes
**Category:** Military & Conflict
**Directionality:** Ransomer → Captive
**Status:** **accepted 2026-05-13** → added to architecture.md § Military & Conflict.

**Definition:** Pays or negotiates for a captive's release. Distinct from `CAPTURES` (the taking) and `PRISONER_OF` (the state).

**Examples:**
- Catelyn proposes to RANSOM Jaime for Sansa & Arya (ASOS)
- Tywin RANSOMS various captured Lannister men post-Battle of the Whispering Wood
- Mance Rayder RANSOMS the Stark girls / the spearwives in ADWD (planned)
- Stannis collects RANSOMS from the mountain clans (off-page lore)

Corpus coverage: 5-15 ransom events.

---

### `FOSTERS` / `FOSTERED_BY`

Yes, intregal ie theon fostered_by starks. tough to say whether this should also be ward of
*(Resolved as reverse-direction note on existing `WARD_OF` — same pattern as HELD_BY for HOLDS_TITLE. One edge type, two emit directions.)*

**Status:** **accepted 2026-05-13 as reverse-direction note on `WARD_OF`** — `FOSTERED_BY` is a permitted reverse-direction emission of `WARD_OF`, semantically equivalent. Documented in the WARD_OF row in architecture.md. No new edge type added.

This means:
- `Theon WARD_OF Eddard` and `Eddard FOSTERED_BY (reverse) Theon` are the same edge, two directions.
- Query layer treats them as identical.

---

### `IMPRISONS`

Captures, and then imprisons. Make sense? or temporal qualifier. Leave that one to you.
*(My call: kept as new type. The state vs event distinction is real — Cersei imprisoning Tyrion in the Red Keep cells isn't a "capture" since he was already at court.)*

**Category:** Military & Conflict
**Directionality:** Imprisoner → Imprisoned
**Status:** **accepted 2026-05-13** → added to architecture.md § Military & Conflict.

**Definition:** Holds a captive in named confinement (cell, dungeon, tower) — distinct from `CAPTURES` (battlefield event) and `PRISONER_OF` (the captive's state). Captures the institutional/judicial act of confinement.

**Examples:**
- Cersei IMPRISONS Tyrion (Red Keep cells, post-Joffrey)
- The High Sparrow IMPRISONS Cersei & Margaery (AFFC-ADWD)
- Tywin IMPRISONS Tyrion (post-Joffrey-death trial)
- Hizdahr zo Loraq IMPRISONS / Daenerys IMPRISONED in pyramid context
- Walder Frey IMPRISONS Edmure (post-Red Wedding)

Corpus coverage: 10-20 imprisonment events.

---

## Bonus type — added Session 53 from Matt's coverage-gap notes

### `BONDED_TO`

*(Matt's coverage-gap note: "Bonded to works... because the one guy is bonded to the animal he wargs into?")*

**Category:** Magic & Supernatural (new subsection)
**Directionality:** Symmetric
**Status:** **accepted 2026-05-13** → added to architecture.md § Magic & Supernatural.

**Definition:** Static magical bond between two beings — broader and more permanent than `WARGS_INTO` (the active occupation moment). Captures the underlying bond that makes warging possible, plus dragon-rider bonds (which are NOT warging in canon), plus weirwood-bond.

**Examples:**
- Daenerys BONDED_TO Drogon (dragon-rider)
- Rhaegal BONDED_TO Jon (theory tier — Aegon/Rhaegal connection)
- Bran BONDED_TO Summer (lifelong pairing, separate from active warging)
- Bran BONDED_TO the three-eyed crow / weirwood network (ADWD)
- Varamyr BONDED_TO his beasts collectively
- Direwolves BONDED_TO their Stark children (collective; one each)

Corpus coverage: 10-20 bonded pairs.

---

## Coverage gaps — Matt's review (deferred to vocabulary-gap workflow during Stage 4)

Yes. Rape, Has sex with or lover, ALLIES WITH question - idk, leave that to you. Bonded to works... because the one guy is bonded to the animal he wargs into? Hmmmm Member of faction is probably important. might be enough but idk if anything besides that deserves a brother hood band bond. Unless it also applies to bonds like the stark family, lannisters etc

**Decisions on Matt's coverage-gap notes:**

- **Sexual relations beyond LOVER_OF** — Matt: "Has sex with or lover" raised. **Deferred:** the distinction between LOVER_OF, HAS_SEX_WITH, RAPES, and PURCHASED (slave-trade) matters narratively (Tysha, Drogo-Daenerys, Tyrion's brothels) but the right granularity depends on what the classifier actually surfaces. Letting Stage 4 file `vocabulary-gap` questions as it encounters these in prose. The 3-example threshold ensures we'll only add types that actually need expressing.
- **Political faction shifts** — Matt: "ALLIES_WITH... idk, leave that to you." **Deferred.** Theon's Stark↔Greyjoy oscillation, Brienne's Renly→Catelyn→Jaime, Jaime's Cersei→honor → these are character arcs, not simple ALLIES_WITH edges. May need a new SHIFTED_ALLEGIANCE type, but waiting for empirical signal.
- **Dragon-rider bonding** — Resolved via the new `BONDED_TO` type (see above).
- **Sworn brotherhood / family bond** — Matt: "Member of faction is probably important. might be enough." **No new type added.** `MEMBER_OF` covers Night's Watch / Brotherhood Without Banners / Faceless Men. The Stark/Lannister/Greyjoy family-bond is already covered by `SIBLING_OF`, `PARENT_OF`, etc. + house membership.

**Stage 4 protocol for these:** if the classifier hits prose like "Tyrion raped Tysha" or "Jorah purchased Daenerys's body" and no existing type fits, it should file a `vocabulary-gap` question to `working/wiki/pass2-buckets/questions-for-matt.jsonl` with ≥3 example sentences. The aggregator at `scripts/build-vocab-gap-log.py` will surface these to `working/edge-vocabulary-gaps.md` for review.

---

## Rejected (kept here so they aren't re-proposed)

*(none from Session 53 — Matt accepted all 13 proposed types plus 1 reverse-direction note.)*

---

## Proposed (Session 53b, 2026-05-13) — Artifact lifecycle

> Surfaced when working through Ice's empty Edges section as a Stage 4 substrate example. The current Possession & Ownership subsection has 4 types (`WIELDS`, `OWNS`, `ANCESTRAL_WEAPON_OF`, `FORGED_BY`) — all steady-state, none transactional or temporal-lifecycle. ASOIAF leans heavily on artifact history: theft (Ice from House Stark), reforging (Ice → Widow's Wail + Oathkeeper), gifting (Longclaw from Jeor to Jon), use-in-named-events (Ice used in execution-of-Eddard). Without these types, Stage 4 will systematically miss artifact-lifecycle edges across every Valyrian steel sword, every dragon-glass weapon, every ancestral horn.

### `LOOTED_BY` / `SEIZED_BY`

**Category:** Possession & Ownership (or Military & Conflict)
**Directionality:** Artifact → Looter
**Status:** proposed

**Definition:** An artifact taken via violence or conquest, distinct from `OWNS` (steady-state) and `INHERITED_BY` (peaceful succession). Captures the *transactional* moment of transfer.

**Examples:**
- Ice LOOTED_BY House Lannister (after Eddard's execution; taken from his body)
- Lightbringer (Azor Ahai's sword) LOOTED_BY various claimants in legendary history
- Dragonbinder LOOTED_BY Victarion Greyjoy (Euron's gift, but taken from Slaver's Bay history)
- Robert's warhammer LOOTED_BY post-Trident (post-Battle, the weapons fate)

Corpus coverage: 15-30 artifact-theft events (Ice + Heartsbane history + various ancestral weapons changing hands).

---

### `REFORGED_INTO`

**Category:** Possession & Ownership
**Directionality:** Original artifact → Resulting artifact(s)
**Status:** proposed

**Definition:** An artifact is materially transformed into a new artifact (or multiple). The original ceases to exist as such; the new artifact(s) inherit material and lineage. Particularly relevant for Valyrian steel which can only be reforged, not created anew.

**Examples:**
- Ice REFORGED_INTO Widow's Wail (Tywin's reforge for Joffrey)
- Ice REFORGED_INTO Oathkeeper (Tywin's reforge for Jaime → Brienne)
- Brightroar LOST (not reforged — sank in Valyria; useful contrast for the type's scope)

Corpus coverage: 3-8 reforge events. Lower volume but very high narrative weight.

---

### `GIFTED_TO` / `BESTOWED_ON`

**Category:** Possession & Ownership
**Directionality:** Artifact → Recipient (with `gifter` qualifier)
**Status:** proposed

**Definition:** Deliberate transfer of an artifact from one person to another as a gift or honor, distinct from `OWNS` (steady-state) and `INHERITED_BY` (death-succession). Captures voluntary transfer.

**Examples:**
- Longclaw GIFTED_TO Jon Snow (Jeor Mormont; ACOK)
- Oathkeeper GIFTED_TO Brienne (Jaime; ASOS/AFFC)
- Widow's Wail GIFTED_TO Joffrey (Tywin; ASOS wedding gift)
- Dragonbinder GIFTED_TO Victarion (Euron; AFFC kingsmoot)
- Heartsbane (Tarly) — not gifted, inherited; useful contrast
- Various Lannister wedding gifts

Corpus coverage: 20-40 named-gift events.

---

### `INHERITED_BY`

**Category:** Kinship & Family OR Possession & Ownership
**Directionality:** Artifact → Heir
**Status:** proposed

**Definition:** Artifact passed via inheritance from a deceased holder to their heir. Distinct from `HEIR_TO` (which is person → person/title relation) — this is artifact-specific.

**Examples:**
- Ice INHERITED_BY Eddard (from Rickard; pre-AGOT)
- Ice INHERITED_BY Robb (from Eddard; pre-Red Wedding)
- Heartsbane INHERITED_BY (Tarly succession history)
- Storm's End armory (lots of inheritance chains in Baratheon line)

Could collapse into `OWNS` with temporal qualifier, but the inheritance moment matters narratively (especially for ancestral weapons).

Corpus coverage: 15-30 inheritance events.

---

### `WIELDED_IN` / `USED_IN`

**Category:** Possession & Ownership OR Military & Conflict
**Directionality:** Artifact → Event
**Status:** proposed

**Definition:** An artifact was used in a named event. Distinct from `WIELDS` (person → artifact possession state) — this is artifact → event use. Enables queries like "what happened with Ice?" or "which weapons were at the Trident?"

**Examples:**
- Ice WIELDED_IN execution-of-eddard-stark (Sept of Baelor, AGOT)
- Robert's warhammer WIELDED_IN battle-of-the-trident (vs Rhaegar)
- Lightbringer WIELDED_IN the-battle-for-the-dawn (legendary)
- Longclaw WIELDED_IN the wight-fight-at-castle-black (AGOT)
- Dawn WIELDED_IN combat-at-the-tower-of-joy

Corpus coverage: 30-60 artifact-in-event uses.

---

### `EXECUTED_WITH` *(possibly redundant with WIELDED_IN — flag for review)*

**Category:** Military & Conflict
**Directionality:** Victim → Weapon
**Status:** proposed (marginal — may collapse into WIELDED_IN as a query against execution-events)

**Definition:** A specific person was executed with a specific weapon. Captures the poetic-detail edges that ASOIAF privileges (Eddard executed with his own sword Ice; Will the deserter executed by Eddard with Ice).

**Examples:**
- Eddard EXECUTED_WITH Ice (Sansa's nightmare also references this)
- Gared (NW deserter) EXECUTED_WITH Ice (AGOT prologue / Bran I)
- Olyver Bracken EXECUTED_WITH Ice (50 AC; in Origins)

**Recommendation:** Lean toward absorbing into `WIELDED_IN` + `EXECUTES` overlap, with query layer doing the join. But if Matt prefers the dedicated type for narrative-precision queries, add it. Mark as marginal in the architecture row.

Corpus coverage: 10-15 named-weapon executions.

---

### `MADE_OF`

*(Surfaced 2026-05-13 during Sonnet's smoke test on Longclaw — Sonnet filed `q-2026-05-13-longclaw-002` to `questions-for-matt.jsonl` after hitting "the blade is of Valyrian steel" with no fitting type. Matt independently asked about this same edge type. Two signals → formal proposal.)*

**Category:** Possession & Ownership
**Directionality:** Artifact → Material
**Status:** proposed

**Definition:** An artifact is composed of a specific material. Distinct from `FORGED_BY` (which is artifact → smith, the creator). Material composition is a queryable property — "show me all Valyrian steel weapons," "show me all dragonglass artifacts," "show me what's made of dragonbone" — that the current vocabulary cannot express without misusing other types.

**Why distinct from `FORGED_BY`:** the smith and the material are categorically different. Donal Noye repaired Longclaw — that's a smith relationship (or close to one). Valyrian steel is the substance Longclaw is made of — that's a material relationship. Conflating them (as Haiku did in its smoke test by emitting `longclaw → valyrian-steel FORGED_BY`) corrupts the graph because queries like "who forged Longclaw?" would return the material as an answer.

**Type contract:**
- Source: `object.artifact` (or potentially `object.text` for in-world books "made of" parchment etc.)
- Target: `object.material` (`object.material` was added as an entity type in Session 29; existing material nodes include `valyrian-steel`, `dragonglass`, `dragonbone`, `weirwood` as a material, `gold` as a material vs `gold-dragon` as a coin, etc.)

**Examples:**
- Ice MADE_OF Valyrian steel
- Longclaw MADE_OF Valyrian steel
- Heartsbane, Oathkeeper, Widow's Wail, Needle, Dawn, Dark Sister, Blackfyre — all MADE_OF Valyrian steel
- Sam Tarly's dagger MADE_OF dragonglass
- The horn at the Fist of the First Men cache MADE_OF dragonglass (theory tier; weakened)
- The Horn of Joramun MADE_OF (uncertain; aurochs horn? mammoth?)
- Robert's warhammer MADE_OF steel + spike of antler in handle (could be two MADE_OF edges with qualifier)
- Bows of the Children of the Forest MADE_OF weirwood
- Crowns: Aegon I's MADE_OF Valyrian steel + rubies; the Iron Throne MADE_OF a thousand surrendered swords (interesting case — could also be `FORGED_BY: aegon-i-targaryen` since Aegon's dragons did the work)

Corpus coverage: 40-80 artifact-material pairs. **Highest-volume of the artifact-history proposals** because nearly every named weapon has a material call-out in its wiki page.

**Note on the Iron Throne edge case:** the Iron Throne is famously made *from* a thousand surrendered swords. That's not really "Valyrian steel" or a single material — it's a melted-together amalgam. `MADE_OF` with qualifier `["thousand surrendered swords, fused by dragonflame"]` covers it. The `FORGED_BY` direction is separately interesting (Aegon I + Balerion's dragonflame).

**Compatible with existing types:** MADE_OF doesn't conflict with WIELDS, OWNS, ANCESTRAL_WEAPON_OF, or FORGED_BY. It adds a new dimension (substance) orthogonal to the existing person-artifact relations.

---

## Coverage gaps surfaced 2026-05-13 (Session 53b) — flag for thought

When working through Ice as an example, also surfaced:

- **Artifact destruction edges** — Brightroar lost in Valyria; the broken pieces of Heartsbane's predecessor; various warhammer shafts splintering. Probably `DESTROYED_IN` paired with `WIELDED_IN`.
- **Artifact loss/missing edges** — Dawn returned to House Dayne after Tower of Joy; the original Lightbringer's fate unknown. Distinct from LOOTED_BY (no known taker) and DESTROYED_IN (still might exist somewhere).
- **Materials → artifacts** — Dragonglass weapons (Sam's dagger), dragonbone bows. Could use `MADE_FROM` (artifact → material) — distinct from `FORGED_BY` (artifact → smith).

Defer pending classifier surfacing.

## Accepted (canonical row lives in architecture.md)

| Type | Subsection | Accepted | Notes |
|------|-----------|----------|-------|
| `MARRIES_OFF` | Kinship & Family | 2026-05-13 | — |
| `VOWS_TO` | Political & Authority | 2026-05-13 | — |
| `BREAKS_VOW` | Political & Authority | 2026-05-13 | Paired with VOWS_TO and SWORN_TO |
| `POISONS` | Military & Conflict | 2026-05-13 | — |
| `RANSOMS` | Military & Conflict | 2026-05-13 | — |
| `IMPRISONS` | Military & Conflict | 2026-05-13 | Distinct from CAPTURES (state vs event) |
| `TUTORS` | Knowledge & Information | 2026-05-13 | Narrower than TEACHES |
| `HEALS` | Knowledge & Information | 2026-05-13 | Narrowed to medical only; resurrection-adjacent examples moved to RESURRECTS |
| `WARGS_INTO` | Magic & Supernatural (new) | 2026-05-13 | Active occupation moments |
| `BONDED_TO` | Magic & Supernatural (new) | 2026-05-13 | Static bond underlying warging + dragon-rider + weirwood |
| `SACRIFICES` | Magic & Supernatural (new) | 2026-05-13 | Ritual/magical killing |
| `RESURRECTS` | Magic & Supernatural (new) | 2026-05-13 | Includes Red Priest revivals + Mountain reanimation |
| `CURSES` | Magic & Supernatural (new) | 2026-05-13 | May overlap with PROPHESIED_BY |
| `DREAMS_OF` | Prophecy | 2026-05-13 | Targaryen prophetic-dreaming lineage etc. |
| `FOSTERED_BY` | (reverse of WARD_OF) | 2026-05-13 | Not a new type; documented as reverse-direction emission on WARD_OF |

**Total: 14 new types adopted into architecture.md + 1 reverse-direction note. Vocabulary went from 100 → 114 across 14 → 15 subsections.**
