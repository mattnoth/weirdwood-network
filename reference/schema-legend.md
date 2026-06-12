# Weirwood Network — Schema Legend

> **Generated:** 2026-06-12  
> **Sources:** `reference/architecture.md` (edge vocab + tiers + direction conventions),
> `scripts/build-edge-type-counts.py` (canonical 166-type list, node-file counts),
> `graph/edges/edges.jsonl` (4,760 live prose-derived edges),
> `graph/nodes/*/` (8,516 total files; 253 in `_conflicts/` staging → **8,263 active nodes**),
> `reference/edge-qualifier-vocab.md` (qualifier enums — see that file for full enums)  
> **Sync rule (CLAUDE.md rule 6):** when architecture.md changes, update this file to match.
> Counts are regenerable: re-run `build-edge-type-counts.py` (node-embedded totals) + count
> `edges.jsonl` separately for prose-pipeline totals.
>
> **Two edge stores — what each count column means:**  
> - `edges.jsonl` — the **canonical/citable store** (4,760 rows; prose-derived + reified events).  
>   Queryable today; every row has `evidence_kind`, `evidence_quote`, `confidence_tier`.  
> - `node-embedded (wiki)` — wiki-infobox fields encoded as edge bullets in node frontmatter
>   (21,087 instances across 58 types). These are display-layer data from the AWOIAF infoboxes;
>   they are **NOT yet in edges.jsonl**. A greenlit infobox-merge track (2026-06-11) will land
>   them as `evidence_kind: wiki-infobox` rows (~17k expected). Until that merge completes,
>   these edges are invisible to `edges.jsonl` queries.

---

## Edge Types by Family

**166 canonical types. 58 populated in node-embedded (wiki-infobox) layer (21,087 instances; NOT yet in edges.jsonl).
111 appear in edges.jsonl prose pipeline (4,760 rows). 0 drift types.**

Qualifiers: 8 types REQUIRE a qualifier; 9 allow optional. All others MUST NOT carry one.
See `reference/edge-qualifier-vocab.md` for full enum values.
Qualifier-required (Tier 1): `SIBLING_OF SPOUSE_OF PARENT_OF WARD_OF HOLDS_TITLE VOWS_TO MANIPULATES SWORN_TO`
Qualifier-optional (Tier 2): `BETROTHED_TO LOVER_OF KILLS CONTRACTED_WITH DECEIVES REVEALS_TO ATTACKS GUEST_OF IN_LAW_OF`

### Kinship & Family (21 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `PARENT_OF` | Biological or adoptive parent | parent → child | 3,095 | 41 |
| `SIBLING_OF` | Brother/sister (full, half, step, milk) | symmetric | 121 | 51 |
| `SPOUSE_OF` | Married to (note state: current/former/widowed) | symmetric | 663 | 40 |
| `BETROTHED_TO` | Formally engaged/promised in marriage | symmetric | 9 | 27 |
| `LOVER_OF` | Romantic/sexual relationship outside marriage | symmetric | 182 | 46 |
| `WARD_OF` | Fostered by / raised by; not biological | ward → guardian | 5 | 5 |
| `ANCESTOR_OF` | Distant lineage (2+ generations) | ancestor → descendant | 2 | 1 |
| `HEIR_TO` | Designated successor (person → person or title) | heir → holder | 206 | 14 |
| `CADET_BRANCH_OF` | Junior house derived from senior house | cadet → parent house | 30 | 0 |
| `MARRIES_OFF` | Arranger orchestrates a marriage for another | arranger → married-off person | 0 | 6 |
| `UNCLE_OF` | One-hop uncle/aunt shortcut | uncle/aunt → nephew/niece | 0 | 25 |
| `NEPHEW_OF` | Reverse of UNCLE_OF | nephew/niece → uncle/aunt | 0 | 16 |
| `COUSIN_OF` | Cousin shortcut (first/second/etc.) | symmetric | 0 | 21 |
| `MILK_BROTHER_OF` | Shared wet-nurse (e.g., Jon Snow & Edric Dayne) | symmetric | 0 | 2 |
| `NURSED_BY` | Child was wet-nursed by this person | child → nurse | 0 | 2 |
| `WET_NURSE_OF` | Reverse of NURSED_BY | nurse → child | 0 | 0 |
| `COURTS` | Active suitor pursuing marriage | suitor → object-of-courtship | 0 | 29 |
| `PROPOSED_AS_BRIDE` | Third party offers a woman as bride candidate | proposer → proposed bride | 0 | 0 |
| `STEP_PARENT_OF` | Step-parent (marital consequence, not PARENT_OF) | step-parent → step-child | 0 | 1 |
| `STEP_CHILD_OF` | Reverse of STEP_PARENT_OF | step-child → step-parent | 0 | 0 |
| `IN_LAW_OF` | Marriage-affinity (good-mother, mother-in-law, etc.) | symmetric | 0 | 11 |

### Political & Authority (15 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `RULES` | Holds authority over a location or domain | ruler → location | 562 | 4 |
| `OVERLORD_OF` | Feudal superior | overlord → vassal | 582 | 5 |
| `SWORN_TO` | Feudal allegiance (house-to-house or person-to-house) | vassal → lord | 4,143 | 84 |
| `COMMANDS` | Military or organizational command | commander → subordinate | 3 | 171 |
| `SERVES` | Service relationship (maester, squire, servant) | server → served | 66 | 255 |
| `ADVISES` | Counsel relationship (Hand, maester, septa) | advisor → advised | 1 | 0 |
| `HOLDS_TITLE` | Person holds a named office or title | person → title | 3,931 | 0 |
| `HELD_BY` | Reverse of HOLDS_TITLE (on title nodes) | title → person/house | 24 | 0 |
| `SUCCEEDS` | Succeeded someone in a role | successor → predecessor | 192 | 3 |
| `CLAIMS` | Asserts right to title/throne/domain | claimant → claimed | 4 | 10 |
| `APPOINTS` | Grants a position to someone | appointer → appointed | 0 | 21 |
| `DEPOSES` | Removes someone from power | deposer → deposed | 0 | 3 |
| `VOWS_TO` | Personal named oath made to another | vow-maker → recipient | 0 | 10 |
| `BREAKS_VOW` | Breaking of a personal vow or sworn oath | vow-breaker → vow-recipient | 0 | 2 |
| `BANISHES` | Royal/political act of exile | banisher → banished | 0 | 7 |

### Factional & Diplomatic (9 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `MEMBER_OF` | Belongs to a faction, order, or organization | person → faction | 31 | 11 |
| `FOUNDED` | Created an organization, house, or institution | founder → founded | 81 | 1 |
| `ALLIES_WITH` | Political alliance (note if temporary/forced) | symmetric | 3 | 91 |
| `OPPOSES` | Active opposition or enmity | symmetric | 8 | 265 |
| `MANIPULATES` | One party unknowingly used by another | manipulator → target | 3 | 0 |
| `BETRAYS` | Broke faith, oath, or alliance | betrayer → betrayed | 2 | 39 |
| `NEGOTIATES_WITH` | Diplomatic engagement (may not conclude) | symmetric | 0 | 16 |
| `CONTRACTED_WITH` | Formal hire/commission for specific service | contractor → contracted party | 0 | 16 |
| `CONSPIRES_WITH` | Secret joint plot | symmetric | 0 | 19 |

### Military & Conflict (27 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `FIGHTS_IN` | Combatant in battle/war/tournament | person → event | 234 | 0 |
| `COMMANDS_IN` | Command role OR orderer/instigator of event | person → event/war | 4 | 157 |
| `PART_OF` | Battle is a component of a war | battle → war | 1 | 0 |
| `SUB_BEAT_OF` | Fine-grained beat within a parent event (NOT alias) | beat → parent event | 0 | 51 |
| `KILLS` | Directly causes death | killer → killed | 31 | 102 |
| `KILLED_BY` | Reverse of KILLS (on victim nodes) | killed → killer | 2 | 1 |
| `EXECUTES` | Formal/judicial killing | executor → executed | 1 | 11 |
| `CAPTURES` | Takes prisoner | captor → captive | 4 | 18 |
| `PRISONER_OF` | Held captive | prisoner → captor | 5 | 30 |
| `BESIEGES` | Conducts siege of a location | besieger → location | 0 | 2 |
| `DEFEATS` | Wins against in battle/conflict | victor → defeated | 352 | 19 |
| `DUELS` | Single combat | symmetric | 3 | 4 |
| `POISONS` | Killing or attempted-killing via poison | poisoner → poisoned | 0 | 4 |
| `RANSOMS` | Pays or negotiates for a captive's release | ransomer → captive | 0 | 1 |
| `PRISONER_EXCHANGE_FOR` | Symmetric body-for-body swap | symmetric (captive ↔ captive) | 0 | 0 |
| `IMPRISONS` | Judicial/institutional act of confinement | imprisoner → imprisoned | 0 | 9 |
| `GUARDS` | Physical custody (protective or confinement) | custodian → subject | 0 | 35 |
| `KILLED_WITH` | Death attributed to a specific named artifact | victim → artifact | 0 | 0 |
| `KNIGHTED_BY` | Granted knighthood | knight → dubber | 0 | 0 |
| `BESTOWS_KNIGHTHOOD_ON` | Reverse of KNIGHTED_BY | dubber → knight | 0 | 4 |
| `ATTACKS` | Generic physical violence (not death; see KILLS) | attacker → target | 0 | 43 |
| `ASSAULTS` | Sexual violence (explicit prose only) | assailant → victim | 0 | 11 |
| `PARTICIPATES_IN` | Non-combat active involvement in named event | person → event | 0 | 0 |
| `RESCUES` | Single-moment extraction from danger | rescuer → rescued | 0 | 17 |
| `TORTURES` | Deliberate sustained physical torment | torturer → tortured | 0 | 11 |
| `AGENT_IN` | Executor/agent of a reified event hub | person/house → event | 0 | 335 |
| `VICTIM_IN` | Victim/patient of a reified event hub | person/house → event | 0 | 316 |

### Knowledge & Information (15 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `IGNORANT_OF` | Critically lacks information others have | person → information | 0 | 2 |
| `SEEKS` | Pursuing knowledge, artifact, or person | seeker → sought | 1 | 52 |
| `REVEALS_TO` | Discloses information | revealer → recipient | 0 | 4 |
| `DECEIVES` | Deliberately misleads | deceiver → deceived | 0 | 13 |
| `DECEIVED_BY` | Reverse of DECEIVES | deceived → deceiver | 1 | 2 |
| `HOARDS` | Suppresses knowledge | hoarder → knowledge | 0 | 0 |
| `INVESTIGATES` | Actively trying to learn or prove something | investigator → subject | 0 | 2 |
| `TEACHES` | Transmits knowledge or skill (general) | teacher → student | 3 | 19 |
| `TUTORS` | Sustained formal one-on-one mentorship | tutor → student | 0 | 32 |
| `HEALS` | Medical treatment/restoration (not resurrection) | healer → healed | 0 | 16 |
| `AFFLICTED_BY` | Character suffers from named disease/affliction (living) | character → concept.medical | 0 | 0 |
| `DIED_OF` | Death caused by named disease/condition (post-mortem) | character → concept.medical | 0 | 0 |
| `SPIES_ON` | Active surveillance of a target | person → surveilled | 0 | 7 |
| `INFORMS` | Ongoing reporting to handler/spymaster | person → handler | 0 | 0 |
| ~~`KNOWS`~~ | *Deprecated S63 (2026-05-21) — 82.3% fallback rate; deferred to future pass* | — | 0 | 0 |

### Emotional & Perceptual (13 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `PERCEIVED_AS` | How POV character sees another (with notes) | perceiver → perceived | 0 | 1 |
| `TRUSTS` | Places confidence in | truster → trusted | 0 | 84 |
| `DISTRUSTS` | Lacks confidence in, suspects | distruster → distrusted | 0 | 204 |
| `RESPECTS` | Holds in high regard | respecter → respected | 1 | 136 |
| `FEARS` | Afraid of (person, faction, or thing) | fearer → feared | 0 | 91 |
| `LOVES` | Deep emotional attachment (familial/romantic/platonic) | lover → loved | 2 | 119 |
| `HATES` | Deep enmity or loathing | hater → hated | 0 | 173 |
| `MOURNS` | Grieves for (dead person, lost thing) | mourner → mourned | 0 | 141 |
| `PROTECTS` | Acts as guardian or defender | protector → protected | 3 | 157 |
| `RESENTS` | Harbors bitterness toward | resenter → resented | 0 | 122 |
| `COMPANION_OF` | Close personal friendship/camaraderie | symmetric | 0 | 156 |
| `REPUTED_AS` | Collective reputation without named perceiver | character → concept | 0 | 0 |
| `ENCOUNTERS` | Plot-significant face-to-face meeting (verb gate enforced) | symmetric | 0 | 0 |

### Spatial & Temporal (10 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `LOCATED_AT` | Entity at location (with book/chapter timestamp) | entity → location | 26 | 79 |
| `SEAT_OF` | Primary location of a house or faction | location → house/faction | 338 | 0 |
| `TRAVELS_TO` | Movement to a destination | traveler → destination | 0 | 0 |
| `TRAVELS_WITH` | Co-presence on road or in retinue/court | symmetric | 0 | 17 |
| `BORN_AT` | Birthplace | person → location | 881 | 2 |
| `DIED_AT` | Place of death | person → location | 924 | 0 |
| `BURIED_AT` | Place of burial | person → location | 50 | 0 |
| `IMPRISONED_AT` | Captive's place of confinement | captive → location | 0 | 0 |
| `CONTEMPORARY_WITH` | Events overlap in time | symmetric | 0 | 0 |
| `REGION_OF` | Location belongs to a geographic region | location → region | 615 | 0 |
| ~~`LOCATED_IN`~~ | *Deprecated early-parser synonym — normalize to `LOCATED_AT` on read* | — | 0 | 0 |

### Possession & Ownership (15 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `WIELDS` | Currently bears/uses a weapon/artifact (NOT animals) | person → artifact | 2 | 1 |
| `OWNS` | Possesses (castles, ships, animals — broader than wields) | owner → owned | 91 | 7 |
| `ANCESTRAL_WEAPON_OF` | Hereditary weapon of a house | weapon → house | 15 | 0 |
| `FORGED_BY` | Creator/smith of an artifact | creator → artifact | 0 | 0 |
| `MADE_OF` | Artifact composed of a material | artifact → material | 0 | 0 |
| `LOOTED_BY` | Artifact taken by force from prior holder | artifact → new holder | 0 | 0 |
| `REFORGED_INTO` | Original artifact transformed into new artifact | original → resulting | 0 | 0 |
| `GIFTED_TO` | Deliberate voluntary transfer as gift | artifact → recipient | 0 | 6 |
| `INHERITED_BY` | Passed via inheritance from deceased | artifact → heir | 0 | 0 |
| `WIELDED_IN` | Artifact used in a named event | artifact → event | 0 | 10 |
| `EXECUTED_WITH` | Person executed with a specific named weapon | victim → weapon | 0 | 0 |
| `PURCHASED_FROM` | Transactional acquisition via purchase | buyer → seller | 0 | 1 |
| `BUILT` | Character built/oversaw construction of a structure | builder → structure | 0 | 1 |
| `CAPTAIN_OF` | Captain of a named vessel | captain → vessel | 0 | 5 |
| `CREW_OF` | Non-captain crew member of a named vessel | crew → vessel | 0 | 2 |

### Identity & Disguise (4 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `ALIAS_OF` | Known by another name (substitution test: same entity) | alias → true identity | 1 | 0 |
| `DISGUISED_AS` | Actively pretending to be someone/something else | person → disguise identity | 1 | 2 |
| `SAME_AS` | Two references resolve to same entity | symmetric | 1 | 0 |
| `IMPERSONATES` | Pretending to be a specific other person | impersonator → impersonated | 0 | 1 |

> ALIAS_OF substitution test: two strings are aliases iff swapping one for the other in any sentence about the entity does NOT change truth value. Granularity differences (sub-beat ↔ parent event) are NOT aliases; use SUB_BEAT_OF.

### Magic & Supernatural (6 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `WARGS_INTO` | Warg actively occupies animal/person consciousness | warg → vessel | 0 | 7 |
| `BONDED_TO` | Permanent magical bond (rider↔dragon, warg↔wolf) | symmetric | 0 | 25 |
| `SACRIFICES` | Ritual/magical killing with supernatural purpose | sacrificer → victim | 0 | 3 |
| `RESURRECTS` | Returns dead to life (distinct from HEALS) | resurrector → resurrected | 0 | 1 |
| `CURSES` | Lays a curse (Mirri, Maggy the Frog, Harrenhal) | curser → cursed | 0 | 0 |
| `PRACTICES` | Actively practices a named magical discipline | character → concept.magic | 0 | 0 |

### Cultural & Religious (6 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `CULTURE_OF` | Person belongs to a cultural group | person → culture | 3,447 | 0 |
| `WORSHIPS` | Follows or serves a deity/religion | person → religion | 92 | 7 |
| `SACRED_TO` | Location or artifact is holy to a religion | entity → religion | 0 | 0 |
| `CLERGY_OF` | Serves as religious official | person → religion | 3 | 2 |
| `OFFICIATES` | Performs ritual role at a named event | character → event | 0 | 0 |
| `NAMED_AFTER` | Named in honor of another entity | entity → namesake | 0 | 3 |

### Narrative & Literary (7 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `DEPICTED_IN` | Character subject of in-world text/song/ballad | character → text | 0 | 0 |
| `FORESHADOWS` | Detail A is a Chekhov's gun for Event B | detail → event | 0 | 0 |
| `PARALLELS` | Mirrors thematically (full mirroring) | symmetric | 0 | 14 |
| `SUBVERTS` | Inverts expectation set by B | subverter → subverted | 0 | 0 |
| `ECHOES` | Weaker than PARALLELS — structural/verbal similarity | echo → source | 0 | 1 |
| `CONTRASTS` | Deliberate opposition in characterization/outcome | symmetric | 0 | 6 |
| `WRITTEN_BY` | Authorship of in-world text | text → author | 1 | 0 |

### Prophecy (6 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `FULFILLS` | Event fulfills prophecy (confirmed) | event → prophecy | 0 | 0 |
| `APPEARS_TO_FULFILL` | Possible fulfillment, may be red herring | event → prophecy | 0 | 0 |
| `SUBVERTS_PROPHECY` | Contradicts expected fulfillment | event → prophecy | 0 | 0 |
| `PROPHESIED_BY` | Who made the prophecy | prophecy → prophet | 0 | 0 |
| `SUBJECT_OF_PROPHECY` | Person/event the prophecy is about | person → prophecy | 0 | 0 |
| `DREAMS_OF` | In-world prophetic/significant dream/vision | dreamer → subject | 0 | 7 |

### Evidentiary — Theory Support (3 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `SUPPORTS` | Textual passage supports a theory | evidence → theory | 0 | 0 |
| `CONTRADICTS` | Textual passage undermines a theory | evidence → theory | 0 | 4 |
| `CITED_BY` | Theory attributed to source/community | theory → source | 0 | 0 |

### Causal & Plot (5 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `CAUSES` | Event A leads to Event B | cause → effect | 2 | 0 |
| `PREVENTS` | Action A blocks Event B | preventer → prevented | 0 | 1 |
| `ENABLES` | Condition A makes Event B possible | enabler → enabled | 0 | 1 |
| `MOTIVATES` | Event/condition drives a character's actions | motivation → actor | 0 | 0 |
| `TRIGGERS` | Immediate spark (narrower than CAUSES) | trigger → result | 0 | 0 |

### Hospitality & Custom (5 types)

| Type | Meaning | Direction | node-embedded (wiki) | edges.jsonl |
|------|---------|-----------|----------------------|-------------|
| `GUEST_OF` | Under someone's roof by custom | guest → host | 0 | 404 |
| `VIOLATES_GUEST_RIGHT` | Broke the sacred hospitality compact | violator → victim | 0 | 50 |
| `GRANTS_SAFE_CONDUCT` | Promised safe passage | grantor → recipient | 0 | 2 |
| `ATTENDS` | Present at named event as guest/witness (not combatant) | person → event | 0 | 2 |
| `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` | Tournament champion crowns recipient with laurel | champion → recipient | 0 | 1 |

---

## Node Types

**8,516 total node files across 19 type directories + 2 staging dirs. 253 files in `_conflicts/` staging → 8,263 active nodes.**

| Directory | Files | Primary type(s) | Key frontmatter fields |
|-----------|-------|-----------------|------------------------|
| `characters/` | 3,925 | `character.human`, `character.dragon` | name, slug, aliases, born, died, culture, allegiance |
| `houses/` | 556 | `organization.house` | name, slug, sigil, words, seat, head, overlord |
| `locations/` | 1,097 | `place.location`, `place.region` | name, slug, ruler, region, defensive_features |
| `events/` | 583 | `event.battle`, `event.incident`, `event.death`, `event.capture`, `event.wedding` | name, slug, type, location, participants |
| `chapters/` | 344 | `meta.chapter` | book, chapter_number, pov_character, wiki_source |
| `titles/` | 542 | `title` | name, slug, holders, succession |
| `factions/` | 191 | `organization.faction`, `concept.culture` | name, slug, purpose, leadership, headquarters |
| `artifacts/` | 282 | `object.artifact` | name, slug, material, current_holder |
| `species/` | 188 | `species` | name, slug, habitat, abilities |
| `texts/` | 159 | `object.text` | name, slug, author, subject |
| `theories/` | 45 | `concept.theory` | name, slug, evidence_for, evidence_against, confidence_tier |
| `religions/` | 63 | `organization.religion` | name, slug, deities, clergy_hierarchy, sacred_sites |
| `concepts/` | 57 | `concept.magic`, `concept.custom`, `concept.culture`, `concept.prophecy` | name, slug, rules, practitioners |
| `foods/` | 74 | `object.food` | name, slug, regions, ingredients, culture |
| `materials/` | 58 | `object.material` | name, slug, composition, regions, uses |
| `customs/` | 37 | `concept.custom` | name, slug, regions, cultures |
| `languages/` | 26 | `concept.language` | name, slug, speakers, regions, script |
| `medical/` | 34 | `concept.medical` | name, slug, effects, regions, treatment, mortality |
| `prophecies/` | 2 | `concept.prophecy` | name, slug, prophet, text, candidates |
| `_conflicts/` | 253 | (staging) mixed — character.human, event.battle dominant | promotion-pending nodes |
| `_unclassified/` | 0 | (staging) empty | — |

**Multi-type entity policy:** one node per real-world entity; `type` is the PRIMARY identity; other facets emerge via edges. Examples: Free Folk → `concept.culture` (polity-ness via MEMBER_OF + FIGHTS_IN edges); Children of the Forest → `species` (faction-ness via FIGHTS_IN + magic edges). The Citadel → `place.location`; Faith of the Seven → `organization.religion`.

---

## Confidence Tiers

| Tier | Label | Description | Usage rule |
|------|-------|-------------|------------|
| 1 | Verified Canon | Explicitly stated in text, no ambiguity | Ground truth. Tier 1 is **earned by verbatim book quote.** |
| 2 | Strong Inference | Not stated directly, inferable with high confidence | Near-fact; note the inferential step. Wiki assertions cap at Tier 2. |
| 3 | Community Consensus | Widely accepted theory with strong textual support | Leading theory; flag as unconfirmed. |
| 4 | Plausible Speculation | Reasonable theory, some support, significant uncertainty | Possibility; note competing interpretations. |
| 5 | Crackpot | Entertaining, minimal evidence | Include; clearly label. |

---

## evidence_kind Values

Every edge row in `edges.jsonl` carries an `evidence_kind` field recording the authority of its source.

| Value | Meaning | Live count |
|-------|---------|-----------|
| `book-pass1` | Pass 1 mechanical extraction — verbatim book prose; highest authority | 3,809 |
| `book-pass1-reified` | Pass 1 row promoted to a reified event-hub edge (AGENT_IN / VICTIM_IN / COMMANDS_IN) | 897 |
| `plate4-wiki-cluster` | Plate 4 wiki-cluster chapter-beat minting (SUB_BEAT_OF edges, wiki chapter summaries) | 51 |
| `book-curator` | Hand-curated by Matt; highest-trust manual entry | 3 |
| `wiki-entity` | Stage 4 prose-edge classifier: wiki page prose links to another entity | 0 (reserved) |
| `wiki-chapter-summary` | Stage 4 prose-edge classifier: co-mention in wiki chapter-summary paragraph | 0 (reserved) |
| `wiki-infobox` | Infobox-parser structured fields (SWORN_TO, PARENT_OF, CULTURE_OF, etc.) — **incoming; merge track greenlit 2026-06-11** | 0 in jsonl (21,087 in node files) |

**Downstream filter rules:**  
- **Book-grounded only** (highest-confidence prose): `evidence_kind in {book-pass1, book-pass1-reified, book-curator}` — 4,709 rows today.  
- **Everything including wiki** (post-infobox-merge): add `wiki-infobox` to the filter set. The ~17k infobox rows are NOT in edges.jsonl yet; they are currently only accessible via per-node frontmatter bullets. After the greenlit merge lands, both filters will work against `edges.jsonl` uniformly.  
- **Node-embedded queries today**: must read node frontmatter directly (e.g., `graph-query.py`) — these edges bypass `edges.jsonl` entirely until the merge completes.

---

## Footer

**Full spec:** `reference/architecture.md` — entity hierarchy, edge family definitions, direction conventions, qualifier enums, infobox→edge mapping, multi-type policy, spoiler gating.  
**Qualifier enums:** `reference/edge-qualifier-vocab.md` — Tier 1 (required) and Tier 2 (optional) enum values per edge type.  
**Graph traversal:** `scripts/graph-query.py <slug>` — prints a node's frontmatter, outbound edges (with ALIAS→ / ORPHAN resolution status), and top inbound references. Flags: `--edges-only`, `--inbound-only`, `--json`.  
**Live counts:** re-run `python3 scripts/build-edge-type-counts.py --check-only` for node-embedded edge totals; count `edges.jsonl` separately for prose-pipeline totals.
