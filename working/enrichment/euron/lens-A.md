# Lens A — spine + secondary-character sub-arcs — A1.6 Kingsmoot / Euron proposal (S157)

## Proposed NEW nodes

### 1. `naggas-hill` · Nagga's Hill / the Grey King's Hall · `place.location`
The sacred hill on Old Wyk where the kingsmoot is held. Crowned by 44 fossilized ribs of the sea-dragon Nagga, which served as the beams of the Grey King's longhall. The nine stone steps and the arch of bones are the ritual space where the ironborn crown their kings.
> "On the crown of the hill four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees." — affc-the-drowned-man-01:19

### 2. `naggas-cradle` · Nagga's Cradle · `place.location`
The holy bay of Old Wyk into which Victarion sails, and around which the longships of the kingsmoot gather. Distinct from Nagga's Hill/the hill above.
> "The wind was blowing from the north as the Iron Victory came round the point and entered the holy bay called Nagga's Cradle." — affc-the-iron-captain-01:11

### 3. `gylbert-farwynd` · Gylbert Farwynd · `character.human`
Lord of the Lonely Light, the westernmost of the Iron Islands; the first claimant to rise at the kingsmoot. Proposes to lead the ironborn to a mythical land beyond the Sunset Sea; his claim collapses quickly. Possibly a skychanger; his eyes shift from grey to blue "as changeable as the seas."
> "I am Gylbert Farwynd, Lord of the Lonely Light," the lord told the kingsmoot." — affc-the-drowned-man-01:57

### 4. `dunstan-drumm` · Dunstan Drumm · `character.human`
Lord of House Drumm, Old Wyk; kingsmoot claimant and bearer of the Valyrian steel sword Red Rain. His speech at the kingsmoot dwells too long on ancient Drumm glory and his miserly gifts fail to buy votes.
> "The Drumm came next, another old man, though not so old as Erik. He climbed the hill on his own two legs, and on his hip rode Red Rain, his famous sword, forged of Valyrian steel in the days before the Doom." — affc-the-drowned-man-01:91

### 5. `erik-ironmaker` · Erik Ironmaker · `character.human`
Erik Anvil-Breaker, Lord of House Ironmaker; kingsmoot claimant, eighty-eight years old. He cannot rise from his chair when Asha challenges him, which dooms his claim. Later betrothed to Asha by Euron in absentia — the forced marriage event node exists (`euron-weds-asha-to-erik-ironmaker-in-absentia`), but the character node may be absent. (Dedup note: baseline.md lists `euron-weds-asha-to-erik-ironmaker-in-absentia` as an existing event node; `erik-ironmaker` himself is not listed among existing character nodes — propose him here.)
> "I am Erik Ironmaker, for them who's blind. Erik the Just. Erik Anvil-Breaker." — affc-the-drowned-man-01:73

### 6. `hagen-the-horn` · Hagen the Horn (Euron's hornblower) · `character.human`
The monstrous, shave-headed, tattooed man who sounds Dragonbinder at the kingsmoot. His chest bears a tattooed bird of prey with bleeding talons. His lips blister and bleed from sounding the horn; Cragorn is later named as the hornblower (affc-the-reaver-01: line 243 confirms "Cragorn's died"), but at the kingsmoot the blower is not named "Hagen" in the AFFC text — see note in Dropped section. The hornblower is one of Euron's mutes/mongrels.
> "It was one of Euron's mongrels winding the call, a monstrous man with a shaved head." — affc-the-drowned-man-01:147

**[NODE DROPPED — see Dropped section]** The text does not name this character "Hagen" in these chapters; the name appears in later material. Withdraw this node proposal.

### 6 (revised). `cragorn` · Cragorn (Euron's hornblower) · `character.human`
The man who blew Dragonbinder at the kingsmoot; named by Euron in conversation with Victarion at Lord Hewett's Town. His lungs were "charred as black as soot" — he died from sounding the horn.
> "Cragorn's died, you know... The man who blew my dragon horn. When the maester cut him open, his lungs were charred as black as soot." — affc-the-reaver-01:244–247

### 7. `iron-victory` · Iron Victory · `object.artifact`
Victarion Greyjoy's flagship. The ship that leads the Iron Fleet into Nagga's Cradle and that Victarion commands during the taking of the Shields.
> "The wind was blowing from the north as the Iron Victory came round the point and entered the holy bay called Nagga's Cradle." — affc-the-iron-captain-01:11

### 8. `red-rain` · Red Rain · `object.artifact`
Valyrian steel greatsword owned by House Drumm (specifically Dunstan Drumm). Noted at the kingsmoot; Victarion covets it. Named as belonging to "Hilmar Drumm the Cunning" in origin, who took it from an armored knight.
> "on his hip rode Red Rain, his famous sword, forged of Valyrian steel in the days before the Doom." — affc-the-drowned-man-01:91

*(Note: Baseline lists Red Rain only in the context of Drumm's description; the node itself may already exist in the graph. If it does, skip. If absent, propose.)*

---

## Proposed NEW edges

### A. Victarion / Iron Victory / Taking of the Shields (filling the critical gap)

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `victarion-greyjoy` | `COMMANDS_IN` | `taking-of-the-shields` | Tier-1 | — | "The drums were pounding out a battle beat as the Iron Victory swept forward" / Euron "still needs me to fight his battles" — affc-the-reaver-01:11 + 71 | Victarion personally leads the assault on the Shields from the Iron Victory; the Reaver chapter is entirely his command of that battle. |
| `victarion-greyjoy` | `AGENT_IN` | `taking-of-the-shields` | Tier-1 | — | "He vaulted over the gunwale, landing on the deck below with his golden cloak billowing behind him." — affc-the-reaver-01:13 | Victarion personally fights in the assault, not just commands it. |
| `victarion-slays-multiple-defenders` | `SUB_BEAT_OF` | `taking-of-the-shields` | Tier-1 | — | "He vaulted over the gunwale, landing on the deck below... Left and right he laid about, hewing off the first man's arm at the elbow, cleaving through the shoulder of the second." — affc-the-reaver-01:13 | Links the islanded combat beat under its parent event. |
| `victarion-greyjoy` | `CAPTAIN_OF` | `iron-victory` | Tier-1 | — | "The wind was blowing from the north as the Iron Victory came round the point and entered the holy bay called Nagga's Cradle." — affc-the-iron-captain-01:11 | Victarion is unambiguously captain of Iron Victory (distinct from his CAPTAIN_OF iron-fleet faction role). |
| `nute-the-barber` | `AGENT_IN` | `taking-of-the-shields` | Tier-1 | — | "glimpsed... Nute the Barber send a throwing axe spinning through the air to catch a man in the chest." — affc-the-reaver-01:21 | Nute fights alongside Victarion in the assault. |

### B. Kingsmoot site + officiant

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `kingsmoot-on-old-wyk` | `LOCATED_AT` | `naggas-hill` | Tier-1 | — | "On the crown of the hill four-and-forty monstrous stone ribs rose from the earth... Nine wide steps had been hewn from the stony hilltop." — affc-the-drowned-man-01:19 | The kingsmoot takes place under Nagga's ribs on this specific hill; the site has no edges. |
| `kingsmoot-on-old-wyk` | `LOCATED_AT` | `naggas-cradle` | Tier-1 | — | "The wind was blowing from the north as the Iron Victory came round the point and entered the holy bay called Nagga's Cradle." — affc-the-iron-captain-01:11 | The bay IS the gathering point for the longships / the moot's staging area. |
| `aeron-greyjoy` | `OFFICIATES` | `kingsmoot-on-old-wyk` | Tier-1 | — | "When the Damphair raised his bony hands the kettledrums and the warhorns fell silent... 'We were born from the sea, and to the sea we all return,' Aeron began..." — affc-the-drowned-man-01:36–37 | Aeron conducts the entire rite: calls the names, receives claims, pours the drowning-blessing on Victarion. This is distinct from his AGENT_IN (general participant). |

### C. The Reader (rodrik-harlaw) sub-arc

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `rodrik-harlaw` | `UNCLE_OF` | `asha-greyjoy` | Tier-1 | `relation:maternal_uncle` | "Lord Rodrik Harlaw was... her favorite uncle." / Alannys Harlaw was Balon's wife → Rodrik is Alannys's brother → Asha's maternal uncle — affc-the-krakens-daughter-01:15 | The kinship is explicit; Rodrik is Alannys Harlaw's brother. Fills the core_in=0 gap on rodrik-harlaw. |
| `rodrik-harlaw` | `SUPPORTS` | `asha-greyjoy` | Tier-1 | — | "'VICTORY!' shouted Rodrik the Reader, his hands cupped about his mouth. 'Victory, and Asha!'" — affc-the-drowned-man-01:135 | First public declaration of support at the kingsmoot. |
| `rodrik-harlaw` | `PARTICIPATES_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "Rodrik the Reader had left his books, it would seem." / "And there's old Drumm's Thunderer, with Blacktyde's Nightflyer beside her... Sea Song, aye." — affc-the-iron-captain-01:34 | Rodrik attends despite predicting he would not; his presence at Oakenshield post-Shields confirms he completed the journey. |
| `rodrik-harlaw` | `OWNS` | `ten-towers` | Tier-1 | — | "Ten Towers was the seat of the Lord of Harlaw." / "She climbed quickly, to the fifth story and the room where her uncle read." — affc-the-krakens-daughter-01:51 | Lord Rodrik's seat, the castle where the Asha chapter begins. (Dedup check: not listed in existing web.) |
| `asha-greyjoy` | `GUEST_OF` | `rodrik-harlaw` | Tier-1 | — | "She found him hunched over a table by a window, surrounded by parchment scrolls..." / Asha comes to Ten Towers seeking support — affc-the-krakens-daughter-01:55 | Asha's visit to Ten Towers, summoned by Rodrik, is the Kraken's Daughter chapter. |
| `rodrik-harlaw` | `ADVISES` | `asha-greyjoy` | Tier-1 | — | "Your fight is hopeless." / "Stay, and I shall name you heir to the Ten Towers." — affc-the-krakens-daughter-01:135 + 191 | Rodrik gives Asha explicit counsel to abandon the kingsmoot; the advisory relationship is central to the chapter. |
| `tristifer-botley` | `PARTICIPATES_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "She set the collar on her head... 'Here, my champions.' They pushed past Victarion's three to stand below her: Qarl the Maid, Tristifer Botley, and the knight Ser Harras Harlaw..." — affc-the-drowned-man-01:117 | Tris acts as one of Asha's three champions at the kingsmoot. |
| `qarl-the-maid` | `PARTICIPATES_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "'If you liked the Shadow so well, go back there,' called out pink-cheeked Qarl the Maid, one of Asha's champions." — affc-the-drowned-man-01:167 | Qarl is Asha's champion at the kingsmoot. |

### D. Dragonbinder possession / Cragorn / the sounding

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `euron-greyjoy` | `OWNS` | `dragonbinder` | Tier-1 | — | "That horn you heard I found amongst the smoking ruins that were Valyria..." — affc-the-drowned-man-01:185 | Euron explicitly claims ownership of Dragonbinder; it is his until given to Victarion. |
| `dragonbinder` | `WIELDED_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "The horn he blew was shiny black and twisted, and taller than a man as he held it with both hands. It was bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled." — affc-the-drowned-man-01:151 | Dragonbinder is sounded at the kingsmoot; it is wielded as an instrument in this event (distinct from the S132 voyage-sounding). |
| `cragorn` | `AGENT_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "It was one of Euron's mongrels winding the call, a monstrous man with a shaved head... The hornblower's breath failed at last." — affc-the-drowned-man-01:147 + 159 | Cragorn blows Dragonbinder at the kingsmoot; "Cragorn" is the name given in affc-the-reaver-01 for the man who blew the horn and died of it. |
| `cragorn` | `VICTIM_IN` | `cragorn-dies-from-dragonbinder` | Tier-1 | — | "Cragorn's died, you know... When the maester cut him open, his lungs were charred as black as soot." — affc-the-reaver-01:243–247 | (See also the node below.) |

**Note on `cragorn-dies-from-dragonbinder`:** This death is an event node that does not yet exist but is clearly implied in the text. It is a separate event from the kingsmoot-sounding. Proposing as a new event node:

`cragorn-dies-from-dragonbinder` · `event.death` — Death of Cragorn after sounding Dragonbinder at the kingsmoot; his lungs were charred black.
> "Cragorn's died, you know... When the maester cut him open, his lungs were charred as black as soot." — affc-the-reaver-01:244+247

### E. Kingsmoot claimants + their champion edges

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `gylbert-farwynd` | `AGENT_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "I am Gylbert Farwynd, Lord of the Lonely Light," the lord told the kingsmoot." — affc-the-drowned-man-01:57 | Gylbert is the first claimant to speak at the moot; his AGENT_IN is missing. |
| `dunstan-drumm` | `AGENT_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "The Drumm came next... He climbed the hill on his own two legs, and on his hip rode Red Rain..." — affc-the-drowned-man-01:91 | Dunstan Drumm is the third claimant; his AGENT_IN is missing. |
| `erik-ironmaker` | `AGENT_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "'Aye, me!' the man roared from where he sat... 'I am Erik Ironmaker, for them who's blind.'" — affc-the-drowned-man-01:73 | Erik is the second claimant; his AGENT_IN is missing. |
| `dunstan-drumm` | `HOLDS_TITLE` | `lord-of-old-wyk` | Tier-2 | `title:"Lord of Old Wyk"` | "The Drumm came next, another old man... and on his hip rode Red Rain" + contextually from his role — affc-the-drowned-man-01:91 | [BORDERLINE] Drumm is lord of Old Wyk but this is inferred from his standing / context; not directly stated in these chapters. Consider if the node `lord-of-old-wyk` exists. |
| `dunstan-drumm` | `WIELDS` | `red-rain` | Tier-1 | — | "on his hip rode Red Rain, his famous sword, forged of Valyrian steel in the days before the Doom." — affc-the-drowned-man-01:91 | Dunstan carries Red Rain at the kingsmoot. |
| `victarion-greyjoy` | `PARTICIPATES_IN` | `asha-claims-the-kingsmoot` | Tier-2 | — | "She pushed past Victarion's three to stand below her..." / Victarion's champions and Victarion himself are present and addressed during Asha's claim — affc-the-drowned-man-01:107 | [BORDERLINE] Victarion is present and a foil for Asha's speech; but he does not perform an action in her claim sub-beat beyond being addressed. May be too thin. |

### F. Silence node (0 edges → light it)

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `euron-greyjoy` | `CAPTAIN_OF` | `silence` | Tier-1 | — | "Silence was still out to sea when Balon died, or so it is claimed." / "Silence looks both cruel and fast. On her prow was a black iron maiden..." — affc-the-krakens-daughter-01:95 + affc-the-iron-captain-01:37 | Euron is the captain of Silence; the ship has 0 edges in the graph. |
| `silence` | `CREW_OF` | `euron-greyjoy` | [DROP — wrong direction; CAPTAIN_OF handles this] | — | — | Drop this reverse — CAPTAIN_OF captures the captain/ship relationship. |

### G. Asha sub-arc beats not yet wired

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `asha-greyjoy` | `PARTICIPATES_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "Asha wrenched free of the Barber's hand... she was Balon Greyjoy's daughter, and the crowd was curious to hear her speak." — affc-the-drowned-man-01:107–108 | Dedup check: `asha AGENT_IN asha-claims-the-kingsmoot` already EXISTS; but `asha AGENT_IN kingsmoot-on-old-wyk` also supposedly exists per baseline. Mark as dedup unless missing. |
| `rodrik-harlaw` | `MOTIVATES` | `asha-greyjoy` | Tier-2 | — | "Stay, and I shall name you heir to the Ten Towers... But she will come to Old Wyk, no matter what he says." — affc-the-krakens-daughter-01:191 + 205 | [BORDERLINE] Rodrik's opposition galvanizes Asha's resolve rather than motivating a choice directly; but the text suggests his refusal to endorse her claim pushes her to go. May be too interpretive. |
| `asha-greyjoy` | `TRAVELS_TO` | `naggas-hill` | Tier-1 | — | "She had beached her beneath Norne Goodbrother's castle and rode across the island." — affc-the-iron-captain-01:101 | Asha travels overland to Old Wyk for the moot. |

### H. Victarion grief / resentment routed via MOTIVATES (not event-CAUSES)

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `kingsmoot-on-old-wyk` | `MOTIVATES` | `victarion-greyjoy` | Tier-1 | — | "But when the Damphair's summons came, the call to kingsmoot, then all was changed... the next day he gave command of Moat Cailin to Ralf Kenning and set off overland." — affc-the-iron-captain-01:27 | The kingsmoot summons is what drives Victarion to abandon Moat Cailin; this is a character-decision route. |
| `aeron-greyjoy` | `MOTIVATES` | `victarion-greyjoy` | Tier-1 | — | "Aeron speaks with the Drowned God's voice, Victarion reminded himself, and if the Drowned God wills that I should sit the Seastone Chair..." — affc-the-iron-captain-01:27 | Aeron's summons is the explicit trigger for Victarion's decision. (Distinct from the existing `euron-seizes MOTIVATES aeron` spine edge.) |

### I. Aeron's post-kingsmoot rebellion

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `aeron-greyjoy` | `VOWS_TO` | `aeron-vows-to-raise-the-ironborn-smallfolk` | Tier-1 | `vow:"I shall go to Great Wyk, to Harlaw, to Orkmont, to Pyke itself. In every town and village shall my words be heard."` | "I shall go to Great Wyk, to Harlaw, to Orkmont, to Pyke itself. In every town and village shall my words be heard. No godless man may sit the Seastone Chair!" — affc-the-reaver-01:95 | Aeron's declaration is a formal vow; connects character to the event node that exists in the spine. |
| `baelor-blacktyde` | `VICTIM_IN` | `euron-executes-baelor-blacktyde` | Tier-1 | — | "Nightflyer was seized, Lord Blacktyde delivered to the king in chains. Euron's mutes and mongrels had cut him into seven parts, to feed the seven green land gods he worshiped." — affc-the-reaver-01:97 | Blacktyde is the victim; `euron EXECUTES baelor-blacktyde` ALREADY EXISTS per baseline, but `baelor-blacktyde VICTIM_IN` the execution event is unwired. |
| `baelor-blacktyde` | `PARTICIPATES_IN` | `kingsmoot-on-old-wyk` | Tier-1 | — | "Lord Baelor Blacktyde in his sable cloak stood beside The Stonehouse in ragged sealskin." — affc-the-drowned-man-01:35 | Blacktyde attends and shouts for Asha: "'ASHA QUEEN!' Lord Baelor Blacktyde echoed." — affc-the-drowned-man-01:137. |

### J. Shield lords installed (the Reaver chapter — dedup needed)

Baseline says `kingsmoot-on-old-wyk CAUSES taking-of-the-shields` but the four shield lords named by Euron in the Reaver chapter are potentially unlinked:

| source | edge | target | Tier | qualifier | evidence quote + cite | rationale |
|---|---|---|---|---|---|---|
| `ser-harras-harlaw` | `AGENT_IN` | `taking-of-the-shields` | Tier-1 | — | "The Knight took Grimston by himself. He planted his standard beneath the castle and defied the Grimms to face him." — affc-the-reaver-01:163 | Ser Harras Harlaw single-handedly takes Greyshield; named as Lord of Greyshield in reward. |
| `euron-greyjoy` | `APPOINTS` | `ser-harras-harlaw` | Tier-1 | — | "'So rise, Ser Harras Harlaw, Lord of Greyshield.'" — affc-the-reaver-01:181 | Euron formally installs Harras as Lord of Greyshield. |
| `euron-greyjoy` | `APPOINTS` | `andrik-the-unsmiling` | Tier-1 | — | "'Rise, Andrik the Unsmiling, Lord of Southshield.'" — affc-the-reaver-01:181 | Euron installs Andrik as Lord of Southshield. |
| `euron-greyjoy` | `APPOINTS` | `maron-volmark` | Tier-1 | — | "'Rise, Maron Volmark, Lord of Greenshield.'" — affc-the-reaver-01:181 | Euron installs Maron Volmark as Lord of Greenshield. |
| `euron-greyjoy` | `APPOINTS` | `nute-the-barber` | Tier-1 | — | "'And rise, Nute the Barber, Lord of Oakenshield.'" — affc-the-reaver-01:181 | Euron installs Nute as Lord of Oakenshield. |
| `andrik-the-unsmiling` | `AGENT_IN` | `taking-of-the-shields` | Tier-2 | — | Andrik is rewarded with Southshield and is present among Drumm's champions at the kingsmoot — baseline already lists him as a participant; the text does not show him fighting at the Shields directly. [BORDERLINE] | Inferred from his reward + presence, not directly described fighting there. |
| `maron-volmark` | `AGENT_IN` | `taking-of-the-shields` | Tier-2 | — | "Rise, Maron Volmark, Lord of Greenshield" — rewarded with a shield lordship, implying participation. [BORDERLINE] | Same caveat as Andrik; rewarded but not shown fighting directly. |

---

## Dropped / considered-but-rejected

- **`euron SUSPECTED_OF death-of-balon-greyjoy`** — ALREADY EXISTS per baseline. Not re-proposed.
- **`balon BANISHES euron`** — ALREADY EXISTS. Not re-proposed.
- **`aeron AGENT_IN kingsmoot-on-old-wyk`** — ALREADY EXISTS per baseline §Already-wired. Not re-proposed.
- **`asha AGENT_IN kingsmoot-on-old-wyk`** — ALREADY EXISTS. Not re-proposed.
- **`euron AGENT_IN kingsmoot-on-old-wyk`** — ALREADY EXISTS. Not re-proposed.
- **`victarion AGENT_IN kingsmoot-on-old-wyk`** — ALREADY EXISTS. Not re-proposed.
- **`rodrik-harlaw OPPOSES euron`** — ALREADY EXISTS per baseline §Kin/feudal. Not re-proposed.
- **`rodrik-harlaw ADVISES balon`** — ALREADY EXISTS per baseline §Kin/feudal. Not re-proposed.
- **`rodrik-harlaw RULES house-harlaw / ten-towers`** — ALREADY EXISTS per baseline. Not re-proposed.
- **`hotho-harlaw SERVES rodrik-harlaw`** — ALREADY EXISTS per baseline. Not re-proposed.
- **`dragonbinder GIFTED_TO victarion-greyjoy`** — ALREADY EXISTS per baseline §The voyage cluster. Not re-proposed.
- **`victarion RESENTS euron`** — ALREADY EXISTS per baseline §Already-wired. Not re-proposed.
- **`asha SPOUSE_OF erik-ironmaker`** — ALREADY EXISTS (`kingsmoot-on-old-wyk CAUSES euron-weds-asha-to-erik-ironmaker-in-absentia` and `asha VICTIM_IN euron-weds-asha`). Not re-proposed.
- **Drowned God ← Aeron CLERGY_OF** — ALREADY EXISTS. Not re-proposed.
- **`euron MANIPULATES kingsmoot-electorate (via_bribe)`** — The text clearly shows Euron buying votes ("the Silence returned with holds full of treasure... the Crow's Eye has been buying friends at every hand" — affc-the-krakens-daughter-01:231). However, `kingsmoot-electorate` is not an existing node slug and minting an abstract collective target for MANIPULATES is too loose. Propose in note form for Lens D (cross-arc); drop from this lens.
- **`euron MANIPULATES kingsmoot-on-old-wyk (via_bribe)`** — MANIPULATES target must be a CHARACTER, not an event. Rejected: type mismatch.
- **`hagen-the-horn` node** — Not named "Hagen" in these AFFC chapters. Withdrew. Using `cragorn` (named in affc-the-reaver-01) instead.
- **`victarion PARTICIPATES_IN asha-claims-the-kingsmoot`** — Too thin; Victarion is present but his role is as foil/addressed-party, not active participant. Rejected.
- **`rodrik-harlaw MOTIVATES asha-greyjoy`** — Rodrik's opposition stiffens Asha's resolve but the text frames this as her own will ("She was no Gwynesse"), not a clear motivating push from him. Borderline; left to gate scrutiny; marginally proposed above but flagged [BORDERLINE].
- **`euron WIELDS dragonbinder at kingsmoot`** — Euron does not blow the horn himself; his mongrel (Cragorn) does. `dragonbinder WIELDED_IN kingsmoot-on-old-wyk` + `cragorn AGENT_IN` captures this cleanly.
- **Aeron calls/TRIGGERS the kingsmoot** — The kingsmoot is convened by Aeron's summons; the spine already has `euron-seizes-the-seastone-chair CAUSES kingsmoot-on-old-wyk`. Aeron's AGENT_IN is already wired. Adding a TRIGGERS from the summons to the event would double-route the causal chain. DROPPED.
- **TWOW content: Falia Flowers** — The bastard girl at Oakenshield is named "Falia" in this chapter (affc-the-reaver-01:173: "Falia is concerned for your fine gowns"), but the Falia Flowers character node is TWOW-gated per the hard rules. She appears here under her first name only, without surname. PROPOSE edge from this chapter is NOT gated since she appears in a published chapter — however, her node with surname "Flowers" is TWOW-only per LENS-SHARED. Note this for synthesis gate: the Oakenshield bastard girl appears in AFFC-the-reaver-01 and can receive an edge from this chapter IF a node exists for her without TWOW content.
- **The "dusky woman" — descriptive only, identity GATED** — The dusky woman is present throughout Victarion's chapters; her description is harvested below but no identity edges proposed (GATED per hard rules).
- **`victarion KILLS ser-talbert-serry`** — Victarion forces Talbert Serry over the side into the sea (affc-the-reaver-01:35–36). Most likely drowned but text says "most like the man had drowned" — not confirmed. The edge would be Tier-2 at best. Potentially a new event `victarion-defeats-ser-talbert-serry` SUB_BEAT_OF taking-of-the-shields. [BORDERLINE — for synthesis gate.]
- **`euron CAPTAIN_OF silence`** — Proposed below; dedup check: not listed in baseline's 230 edges. Kept.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | AFFC | affc-the-prophet-01:185 | "Aeron broke his fast on a broth of clams and seaweed cooked above a driftwood fire" — the Damphair's austere ironborn breakfast |
| food | AFFC | affc-the-iron-captain-01:73 | "Victarion might feast half a hundred famous captains on roast kid, salted cod, and lobster" — the Iron Fleet feast-tent menu before kingsmoot |
| food | AFFC | affc-the-iron-captain-01:73 | "Aeron came as well. He ate fish and drank water, whilst the captains quaffed enough ale to float the Iron Fleet." — Aeron's ascetic contrast at the feast |
| food | AFFC | affc-the-drowned-man-01:27 | "thralls, children, and women toward the rear... stirring coals into new life and gutting fish for the captains and the kings to break their fasts" — kingsmoot dawn meal prep |
| food | AFFC | affc-the-drowned-man-01:27 | "the dawnlight touched the stony strand, and he watched men wake from sleep, throwing aside their sealskin blankets as they called for their first horn of ale" — kingsmoot morning ale |
| food | AFFC | affc-the-reaver-01:145 | "riotous feast... roast ox, rare and bloody, and stuffed ducks as well, and buckets of fresh crabs... eating off solid silver platters" — the feast at Lord Hewett's Town after the Shields fall |
| food | AFFC | affc-the-reaver-01:155 | "Ralf the Limper, the captain of the Lord Quellon... A great victory, Lord Captain" + Victarion eats with Ralf at Oakenshield feast |
| food | AFFC | affc-the-krakens-daughter-01:43 | "There's cold beef in the kitchens. And mustard in a big stone jar, from Oldtown." — Three-Tooth describes what's available for Asha's crew at Ten Towers; mustard from Oldtown |
| food | AFFC | affc-the-krakens-daughter-01:44 | "We had a rough crossing. I want something hot in their bellies." — Asha demands hot food for her crew after rough seas |
| food | AFFC | affc-the-reaver-01:167–168 | "eight of them: her ladyship herself... her daughters and good-daughters" made to serve naked at table; "serving wenches wore fine woolens and plush velvets" at the feast — the humiliation of Lady Hewett and her ladies serving at table |
| food | AFFC | affc-the-reaver-01:193 | "There is no wine so sweet as wine taken from a foe." — Victarion drinks with the rest in a bitter toast to the Shield lords |
| food | AFFC | affc-the-reaver-01:102 | "Fetch me another skin of wine... a skin of sour red... the captain took it up on deck... He drank half the skin and poured the rest into the sea for all the men who'd died." — shipboard libation ritual |
| food | AFFC | affc-the-reaver-01:255–259 | "a strange black wine that flowed as thick as honey... It looks more blue than black. It was thick and oily, with a smell like rotted flesh." — Euron's shade-of-the-evening warlock wine; Victarion spits it out |
| quote | AFFC | affc-the-iron-captain-01:37 | "Silence looked both cruel and fast. On her prow was a black iron maiden with one arm outstretched. Her waist was slender, her breasts high and proud... she had no mouth." — vivid description of the Silence's figurehead |
| quote | AFFC | affc-the-iron-captain-01:141–142 | "'King Crow's Eye, brother.' Euron smiled. His lips looked very dark in the lamplight, bruised and blue." — Euron's blue lips, the smiling eye |
| quote | AFFC | affc-the-drowned-man-01:151 | "The horn he blew was shiny black and twisted, and taller than a man as he held it with both hands. It was bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled." — Dragonbinder description at the kingsmoot |
| quote | AFFC | affc-the-drowned-man-01:155 | "aaaaaaaRRREEEEEEEEEEEeeeeeeeeeeeeeeeeeeeeeeeeeeeee... It was a terrible sound, a wail of pain and fury that seemed to burn the ears." — the sound of Dragonbinder being blown |
| quote | AFFC | affc-the-drowned-man-01:159 | "a thin wisp of smoke was rising from the horn, and the priest saw blood and blisters upon the lips of the man who'd sounded it. The bird on his chest was bleeding too." — physical aftermath of Cragorn blowing Dragonbinder |
| quote | AFFC | affc-the-krakens-daughter-01:94–95 | "Silence was still out to sea when Balon died, or so it is claimed. Even so, I will agree that Euron's return was... timely, shall we say?" — the Reader's measured phrasing about Euron's suspicious timing |
| quote | AFFC | affc-the-reaver-01:57 | "He stole my wife and he stole my throne, and now he steals my glory." — Victarion's internal articulation of his grievances against Euron |
| description | AFFC | affc-the-iron-captain-01:43–44 | "Men black as tar stared out at him, and others squat and hairy as the apes of Sothoros. Monsters, Victarion thought." — the Silence's mute-and-mongrel crew at the kingsmoot |
| description | AFFC | affc-the-krakens-daughter-01:55 | Lord Rodrik Harlaw: "neither fat nor slim; neither tall nor short; neither ugly nor handsome. His hair was brown, as were his eyes, though the short, neat beard he favored had gone grey." — the Reader's physical description |
| description | AFFC | affc-the-reaver-01:63 | "The Mander is open to us now, as it was of old. It was a lazy river, wide and slow and treacherous with snags and sandbars." — strategic analysis of the Mander as waterway |
| description | AFFC | affc-the-drowned-man-01:19 | "On the crown of the hill four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees. She fed on krakens and leviathans and drowned whole islands in her wrath, yet the Grey King had slain her and the Drowned God had changed her bones to stone..." — Nagga's Hill / Grey King's Hall description |
| foreshadowing | AFFC | affc-the-reaver-01:84 | "Euron is known to keep wizards and foul sorcerers on that red ship of his. They sent some spell among us, so we could not hear the sea." — Aeron's claim that sorcery swayed the kingsmoot |
| foreshadowing | AFFC | affc-the-reaver-01:96 | "Even his drowned men knew not where. They said the Crow's Eye only laughed when he was told." — Euron's response to Aeron's flight foreshadows his later hunting of Aeron (spine node `euron-hunts-aeron-damphair`). |
| hospitality | AFFC | affc-the-iron-captain-01:73 | "Victarion might feast half a hundred famous captains on roast kid, salted cod, and lobster" — the Iron Fleet's feast-tent at the kingsmoot, used to build political support |
| hospitality | AFFC | affc-the-reaver-01:167–175 | Lord Hewett's ladies forced to serve wine at table naked on Euron's order — Euron violates the hospitality convention grotesquely at Oakenshield |
| hospitality | AFFC | affc-the-krakens-daughter-01:41–44 | Asha asks Three-Tooth for "something hot in their bellies" for her crew and for warm beds for Lady Glover and her children — hospitality as political tool and personal care |
