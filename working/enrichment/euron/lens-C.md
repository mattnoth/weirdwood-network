# Lens C — Descriptive / Quote / Object Depth — A1.6 Kingsmoot / Euron proposal (S157)

## Proposed NEW nodes

None. All targeted objects (silence, iron-victory, dragonbinder, naggas-hill, seastone-chair) already exist as nodes per baseline.md. No new node is warranted from the descriptive/object layer.

---

## Proposed NEW edges

### CAPTAIN_OF — ships

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| euron-greyjoy | CAPTAIN_OF | silence | Tier 1 | "Even at anchor Silence looked both cruel and fast." `affc-the-iron-captain-01:37` (also: "Euron Crow's Eye … *Silence* was still out to sea" `affc-the-krakens-daughter-01:95`) — Euron's self-identification as her captain is implicit in every scene; the explicit arrival + "my sails" framing confirmed by `affc-the-reaver-01:199`: "I have taken the Silence on longer voyages than this" | Euron speaks of Silence as his own ship in first-person; `euron CAPTAIN_OF silence` is the priority gap edge in baseline.md |
| victarion-greyjoy | CAPTAIN_OF | iron-victory | Tier 1 | "The wind was blowing from the north as the Iron Victory came round the point" `affc-the-iron-captain-01:11`; "he clambered back up onto his own Iron Victory" `affc-the-reaver-01:53` | baseline.md Gap #3 — iron-victory has 0 edges; Victarion's captaincy is stated repeatedly |

### CREW_OF — the Silence's mute crew

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| eurons-mongrel-sons | CREW_OF | silence | Tier 1 | "On her decks a motley crew of mutes and mongrels spoke no word as the Iron Victory drew nigh. Men black as tar stared out at him, and others squat and hairy as the apes of Sothoros." `affc-the-iron-captain-01:43` | The Silence's crew are consistently identified as "mutes and mongrels" / Euron's sons; baseline Gap #2. |

### LOCATED_AT / kingsmoot site

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| kingsmoot-on-old-wyk | LOCATED_AT | naggas-hill | Tier 1 | "On the crown of the hill four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees." `affc-the-drowned-man-01:19`; "I summon all of you! … Point your prow toward Old Wyk, where stood the Grey King's Hall. … Seek the hill of Nagga" `affc-the-prophet-01:213` | baseline.md Gap #6 — naggas-hill has 0 edges; the kingsmoot explicitly takes place on Nagga's hill |

### OFFICIATES — Aeron at the kingsmoot

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| aeron-greyjoy | OFFICIATES | kingsmoot-on-old-wyk | Tier 1 | "It was there beneath the arch of Nagga's ribs that his drowned men found him … 'Is it time?' Rus asked. Aeron gave a nod" `affc-the-drowned-man-01:31`; Aeron calls each claimant, blesses Victarion, presides throughout | baseline.md Gap #6 — Aeron's AGENT_IN already exists but OFFICIATES (the ceremonial presider role) is distinct and unwired; he runs the rite, calls each claimant, blesses each contender |

### GIFTED_TO — Dragonbinder

| source | edge | target | Tier | qualifier | quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| dragonbinder | GIFTED_TO | victarion-greyjoy | Tier 1 | — | "He [Euron] glanced at the priest." / The horn is sounded at the kingsmoot, then ADWD confirms Euron gives Victarion the horn to bring Daenerys; the kingsmoot chapter shows the horn in Euron's possession and wielded by his mongrel: "The horn he blew was shiny black and twisted, and taller than a man as he held it with both hands. It was bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled." `affc-the-drowned-man-01:151` | baseline.md Gap #4 — Dragonbinder core_in=0; possession/gifting edges unwired. **[BORDERLINE — the gifting scene itself is in ADWD, not AFFC; the horn's existence and sounding at the kingsmoot is AFFC-quotable, but the explicit "Euron gives it to Victarion" is ADWD. Flag for orchestrator.** |

### euron OWNS dragonbinder

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| euron-greyjoy | OWNS | dragonbinder | Tier 1 | "That horn you heard I found amongst the smoking ruins that were Valyria … It is a dragon horn, bound with bands of red gold and Valyrian steel graven with enchantments." `affc-the-drowned-man-01:185` | Euron explicitly claims ownership and provenance of the horn in published AFFC text; this edge is clean and AFFC-quotable |

### UNCLE_OF — Reader/Asha

| source | edge | target | Tier | qualifier | quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| rodrik-harlaw | UNCLE_OF | asha-greyjoy | Tier 1 | maternal | "my favorite uncle" `affc-the-krakens-daughter-01:15`; "my nuncle of Ten Towers" `affc-the-iron-captain-01:239` — he is Alannys Harlaw's brother (Asha's mother) | baseline.md Gap #5 — rodrik-harlaw core_in=0; `UNCLE_OF` is a Tier-1 type requiring qualifier: `maternal` (he is Lady Alannys Harlaw's brother) |

### PARTICIPATES_IN — Reader at kingsmoot

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| rodrik-harlaw | PARTICIPATES_IN | kingsmoot-on-old-wyk | Tier 1 | "'VICTORY!' shouted Rodrik the Reader, his hands cupped about his mouth. 'Victory, and Asha!'" `affc-the-drowned-man-01:135` | baseline.md Gap #5 — Reader's role at the moot unwired; he shouts Asha's name, a load-bearing narrative beat |

### ALLIES_WITH / SUPPORTS Asha at moot

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| rodrik-harlaw | SUPPORTS | asha-greyjoy | Tier 1 | "I sent the summons. In your name, for the love I bear you and your mother." `affc-the-krakens-daughter-01:99`; shouted her name at moot (above) | baseline.md: rodrik-harlaw core_in=0; clean Tier-1 support edge; note: `ALLIES_WITH asha` is listed in the dedup under "Asha web" — check if this is distinct. The baseline says `ALLIES_WITH house-harlaw` for asha, but not `rodrik SUPPORTS asha` specifically. Propose as additional edge. **[BORDERLINE — ALLIES_WITH asha may cover this; propose SUPPORTS as the specific individual reading]** |

### SUB_BEAT_OF — combat island

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| victarion-slays-multiple-defenders | SUB_BEAT_OF | taking-of-the-shields | Tier 1 | "The Iron Victory swept forward, her ram cutting through the choppy green waters … Victarion slew another man, and another." `affc-the-reaver-01:11-21` | baseline.md Gap #1 — `victarion-slays-multiple-defenders` is causally ISLANDED (cOut=0); the chapter is THE REAVER = the taking; this SUB_BEAT_OF is the explicit link |

### AGENT_IN / COMMANDS_IN — taking-of-the-shields

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| victarion-greyjoy | COMMANDS_IN | taking-of-the-shields | Tier 1 | "The Iron Victory swept forward … Greyshield, Greenshield, and Southshield fell before the sun came up. Oakenshield lasted half a day longer." `affc-the-reaver-01:11,69` | baseline.md Gap #1 — participant roles for `taking-of-the-shields` are entirely unwired |
| victarion-greyjoy | AGENT_IN | taking-of-the-shields | Tier 1 | "He vaulted over the gunwale, landing on the deck below with his golden cloak billowing behind him." `affc-the-reaver-01:13` | Victarion personally fights and boards; both COMMANDS_IN and AGENT_IN are warranted (he both orders and personally kills) |

### Lords installed on the Shields

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| euron-greyjoy | APPOINTS | harras-harlaw | Tier 1 | "Rise, Ser Harras Harlaw, Lord of Greyshield." `affc-the-reaver-01:181` | Euron formally grants lordship; APPOINTS fits (he grants office/title). **Check if harras-harlaw node exists.** |
| euron-greyjoy | APPOINTS | nute-the-barber | Tier 1 | "Rise, Nute the Barber, Lord of Oakenshield." `affc-the-reaver-01:181` | Same appointment scene |
| euron-greyjoy | APPOINTS | andrik-the-unsmiling | Tier 1 | "Rise, Andrik the Unsmiling, Lord of Southshield." `affc-the-reaver-01:181` | Same appointment scene |
| euron-greyjoy | APPOINTS | maron-volmark | Tier 1 | "Rise, Maron Volmark, Lord of Greenshield." `affc-the-reaver-01:181` | Same appointment scene |

### The forced absentia marriage: Asha's champions

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| harras-harlaw | PARTICIPATES_IN | kingsmoot-on-old-wyk | Tier 1 | "Qarl the Maid, Tristifer Botley, and the knight Ser Harras Harlaw, whose sword Nightfall was as storied as Dunstan Drumm's Red Rain." `affc-the-drowned-man-01:117` | Harras Harlaw stands as Asha's champion at the moot; load-bearing role |
| tristifer-botley | PARTICIPATES_IN | kingsmoot-on-old-wyk | Tier 1 | same line `affc-the-drowned-man-01:117` | Tristifer stands as Asha's champion |
| qarl-the-maid | PARTICIPATES_IN | kingsmoot-on-old-wyk | Tier 1 | same line `affc-the-drowned-man-01:117` | Qarl stands as Asha's champion |

### Baelor Blacktyde — executed by Euron after kingsmoot

| source | edge | target | Tier | quote + chapter:line | rationale |
|---|---|---|---|---|---|
| euron-greyjoy | KILLS | baelor-blacktyde | Tier 1 | "Euron's mutes and mongrels had cut him into seven parts, to feed the seven green land gods he worshiped." `affc-the-reaver-01:97` | baseline.md lists `euron EXECUTES baelor-blacktyde` — CHECK: if that edge already exists, skip. If KILLS is a distinct edge from EXECUTES in the vocabulary, this may already be covered. Mark **[BORDERLINE — dedup: `euron EXECUTES baelor-blacktyde` already in dedup list]** |

### MANIPULATES — Euron at the kingsmoot (gold)

| source | edge | target | Tier | qualifier | quote + chapter:line | rationale |
|---|---|---|---|---|---|---|
| euron-greyjoy | MANIPULATES | kingsmoot-on-old-wyk | Tier 2 | via_bribe | "The mutes and mongrels from the Silence threw open Euron's chests and spilled out his gifts before the captains and the kings." `affc-the-drowned-man-01:195`; also: "Euron … has been buying friends at every hand … the Crow's Eye has been buying friends at every hand." `affc-the-krakens-daughter-01:231` | baseline.md Gap #8: Euron's gold-buying of the moot is explicit. Target is an event, not a character — **[BORDERLINE — MANIPULATES target per rules must be a character or could apply to a collective event? The locked-type note says target is typically an actor. If event-target is disallowed, reroute as `euron MANIPULATES iron-fleet` or propose as node-prose only.]** |

---

## Dropped / considered-but-rejected

- **`euron SUSPECTED_OF death-of-balon-greyjoy`** — already in dedup. Do NOT re-propose.
- **`balon BANISHES euron`** — already in dedup.
- **`euron CLAIMS seastone-chair`** — already in dedup.
- **Dragonbinder provenance (Valyria-theft, Joramun=horn-of-winter reading)** — GATED theory. Node-prose only per instructions.
- **Dusky woman identity** — GATED. Her silence/sewn mouth is descriptive; the relationship `victarion COMPANION_OF dusky-woman` is already wired per baseline (S132 voyage cluster).
- **`euron GIFTED_TO victarion (dusky-woman)`** — the generic `euron GIFTED_TO victarion` is already in the dedup list (S116). The dusky woman is the specific gift; proposing it would re-assert the existing generic. The text supports the specificity: "As a reward for his leal service, the new-crowned king had given Victarion the dusky woman" (`affc-the-reaver-01:99`), but the base edge exists. Drop.
- **`dragonbinder GIFTED_TO victarion` (AFFC-specific)** — the gifting is not explicitly in AFFC; it is implied by ADWD. Flagged as BORDERLINE above; the orchestrator should verify the ADWD cite before minting.
- **Falia Flowers (Hewett's bastard daughter)** — TWOW-named character. Her appearance at the feast (`affc-the-reaver-01:169-173`) is AFFC canon but her surname Falia Flowers is TWOW-revealed. Propose node-prose pointer only (see Harvest); do NOT mint a node or name-edge.
- **`taking-of-the-shields CAUSES mander-open-to-ironborn`** — no existing node for this strategic consequence. The Reader's statement (`affc-the-reaver-01:131`) warns of Tyrell enmity but no clean existing Reach node to wire without minting new events. Node-prose / Harvest pointer only.
- **`euron MANIPULATES captains-and-kings (kingsmoot electorate)` as a new character-set node** — would require minting a collective node. Not warranted; MANIPULATES above targets the event.
- **`harras-harlaw HOLDS_TITLE lord-of-greyshield`** — requires confirming harras-harlaw node slug exists. Propose via APPOINTS above instead.
- **Shade-of-the-evening (warlock wine)** — object appears in one scene (`affc-the-reaver-01:255-259`); Euron offers it to Victarion. Interesting artifact but no existing node and minting it is outside this lens's priority; harvest pointer.
- **`euron KILLS baelor-blacktyde` vs `euron EXECUTES baelor-blacktyde`** — baseline dedup already has `euron EXECUTES baelor-blacktyde`. Drop KILLS to avoid double-edge; EXECUTES covers the kill.
- **`aeron OFFICIATES kingsmoot` vs `aeron AGENT_IN kingsmoot`** — AGENT_IN already wired per dedup. OFFICIATES is the priest-presider role, distinct; kept in proposal as additional edge.
- **The driftwood crown as artifact node** — the crown is mentioned as the prize given to the winner (`driftwood crown` placed on Euron's head, `affc-the-reaver-01:77`). No existing node in baseline for driftwood-crown; minting it is low-priority vs. the gap edges. Harvest pointer.
- **Gylbert Farwynd (Lonely Light claimant)** — minor claimant at the moot; `PARTICIPATES_IN kingsmoot` is warranted but he is a very thin character node. Flag as low-priority for orchestrator; not a gap target.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food/drink | AFFC | affc-the-prophet-01:47 | Aeron drinks from leather skin of seawater — "The priest pulled out the cork and took a swallow." Salt water as sacred/ritual drink, the Drowned God's "blessing" |
| food/drink | AFFC | affc-the-prophet-01:185 | "Aeron broke his fast on a broth of clams and seaweed cooked above a driftwood fire." — priest's meal: clam broth + seaweed, cooked over driftwood. Ironborn austerity register |
| food/drink | AFFC | affc-the-iron-captain-01:72-73 | Victarion's feast for captains: "roast kid, salted cod, and lobster. Aeron came as well. He ate fish and drank water, whilst the captains quaffed enough ale to float the Iron Fleet." — Ironborn feast food + priest's contrasting water-and-fish austerity |
| food/drink | AFFC | affc-the-iron-captain-01:71 | "two Sparrs pressed a wineskin into his hands. He drank deep, wiped his mouth" — wineskin passed around on the strand pre-feast |
| food/drink | AFFC | affc-the-drowned-man-01:27 | "thralls and salt wives begin to move about, stirring coals into new life and gutting fish for the captains and the kings to break their fasts … men wake from sleep, throwing aside their sealskin blankets as they called for their first horn of ale." — kingsmoot dawn: gutted fish + first horn of ale |
| food/drink | AFFC | affc-the-reaver-01:144-145 | The sack-feast at Lord Hewett's: "there was roast ox, rare and bloody, and stuffed ducks as well, and buckets of fresh crabs … The serving wenches wore fine woolens and plush velvets … Lady Hewett and her ladies" serving — ironborn eating captive lord's food off silver platters |
| food/drink | AFFC | affc-the-reaver-01:101 | "He drank half the skin and poured the rest into the sea for all the men who'd died." — wine poured as sea-libation for the dead; ritual/hospitality register |
| food/drink | AFFC | affc-the-reaver-01:195 | Euron orders resupply: "take every sack of grain and cask of beef, and as many sheep and goats as we can carry … Our decks will stink of pigs and chickens on the voyage east" — shipboard provisions list for the eastern voyage |
| food/drink | AFFC | affc-the-krakens-daughter-01:43 | "There's cold beef in the kitchens. And mustard in a big stone jar, from Oldtown." — Ten Towers' cold hospitality to Asha's crew; mustard from Oldtown detail |
| food/drink | AFFC | affc-the-reaver-01:255-259 | Euron offers Victarion "shade-of-the-evening, the wine of the warlocks … thick and oily, with a smell like rotted flesh … Seen up close, it looked more blue than black." — warlock wine artifact; Euron's dark possession |
| physical description | AFFC | affc-the-iron-captain-01:37 | The Silence's figurehead: "On her prow was a black iron maiden with one arm outstretched. Her waist was slender, her breasts high and proud, her legs long and shapely. A windblown mane of black iron hair streamed from her head, and her eyes were mother-of-pearl, but she had no mouth." — VIVID quote for silence node ## Quotes |
| physical description | AFFC | affc-the-iron-captain-01:113 | "The Silence was amongst the ships they passed. Victarion's gaze was drawn to the iron figurehead at her prow, the mouthless maiden with the windblown hair and outstretched arm. Her mother-of-pearl eyes seemed to follow him. She had a mouth like any other woman, till the Crow's Eye sewed it shut." — second Silence figurehead description + the dusky-woman parallel |
| physical description | AFFC | affc-the-iron-captain-01:137-141 | Euron's appearance: "His hair was still black as a midnight sea … his face was still smooth and pale beneath his neat dark beard. A black leather patch covered Euron's left eye, but his right was blue as a summer sky." + "His lips looked very dark in the lamplight, bruised and blue." — canonical Euron description for node ## Quotes |
| physical description | AFFC | affc-the-iron-captain-01:43 | Silence's crew: "Men black as tar stared out at him, and others squat and hairy as the apes of Sothoros. Monsters, Victarion thought." — mute-crew description |
| physical description | AFFC | affc-the-drowned-man-01:151 | Dragonbinder: "The horn he blew was shiny black and twisted, and taller than a man as he held it with both hands. It was bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled." — VIVID quote for dragonbinder node ## Quotes |
| physical description | AFFC | affc-the-drowned-man-01:145 | Dragonbinder's sound: "Bright and baneful was its voice, a shivering hot scream that made a man's bones seem to thrum within him." — sensory description, quote for dragonbinder |
| physical description | AFFC | affc-the-drowned-man-01:159 | Dragonbinder's aftermath: "A thin wisp of smoke was rising from the horn, and the priest saw blood and blisters upon the lips of the man who'd sounded it. The bird on his chest was bleeding too." — cost of sounding the horn |
| physical description | AFFC | affc-the-drowned-man-01:19 | Nagga's ribs: "On the crown of the hill four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees. … Nagga had been the first sea dragon, the mightiest ever to rise from the waves." — naggas-hill node ## Quotes |
| physical description | AFFC | affc-the-iron-captain-01:11-13 | Iron Victory + Nagga's Cradle: "The wind was blowing from the north as the Iron Victory came round the point and entered the holy bay called Nagga's Cradle … the ribs of Nagga rose from the earth like the trunks of great white trees, as wide around as a dromond's mast and twice as tall." — iron-victory node description; also naggas-hill/naggas-cradle co-located |
| physical description | AFFC | affc-the-reaver-01:99 | Dusky woman: "her tongue had been torn out, but elsewise she was undamaged, and beautiful besides, with skin as brown as oiled teak." — dusky-woman node ## Quotes |
| physical description | AFFC | affc-the-iron-captain-01:44 | Victarion's kraken armor: "tall black warhelm, wrought in the shape of an iron kraken, its arms coiled down around his cheeks to meet beneath his jaw" — Victarion's signature warhelm description |
| foreshadowing | AFFC | affc-the-reaver-01:247 | Euron on Cragorn's death: "The man who blew my dragon horn. When the maester cut him open, his lungs were charred as black as soot." — foreshadows cost of sounding Dragonbinder (Cragorn = the hornblower at the kingsmoot; `affc-the-drowned-man-01:147` shows blood/blisters; this is the follow-up confirmation) |
| quote / load-bearing | AFFC | affc-the-reaver-01:199 | Euron's Valyria claim: "I am the storm, my lord. The first storm, and the last. I have taken the Silence on longer voyages than this, and ones far more hazardous. Have you forgotten? I have sailed the Smoking Sea and seen Valyria." — euron-greyjoy node ## Quotes; Valyria claim |
| quote / load-bearing | AFFC | affc-the-drowned-man-01:185 | Dragonbinder provenance: "That horn you heard I found amongst the smoking ruins that were Valyria, where no man has dared to walk but me." — euron-greyjoy + dragonbinder node ## Quotes |
| quote / load-bearing | AFFC | affc-the-prophet-01:169 | Red hull + Victarion's assessment: "The decks of Euron's ship were painted red, to better hide the blood that soaked them." — silence node ## Quotes (the red decks detail) |
| religion/ritual | AFFC | affc-the-prophet-01:13-15 | Drowning ritual: Aeron pushes Emmond's head under, calls drowned men to hold him, kisses of life. Full description of the initiation rite — Drowned God religious protocol |
| religion/ritual | AFFC | affc-the-drowned-man-01:25 | Aeron's all-night prayer at Nagga's ribs before the kingsmoot; "Aeron Damphair reached within himself for his god and discovered only silence" at the moot's climax |
| hospitality | AFFC | affc-the-krakens-daughter-01:41-45 | Asha instructs Three-Tooth: "They had a rough crossing. I want something hot in their bellies." Three-Tooth offers "cold beef in the kitchens. And mustard in a big stone jar, from Oldtown." Asha insists on hot food for her crew and warmth for the Glover captives. |
| artifact | AFFC | affc-the-reaver-01:227 | Euron's red leather eye patch mentioned: "He wore the sable cloak he took from Blacktyde, his red leather eye patch, and nothing else." — Blacktyde's sable cloak taken as loot; eye patch detail |
| geography | AFFC | affc-the-iron-captain-01:11 | "Nagga's Cradle" = name for the holy bay of Old Wyk where ships anchor for the kingsmoot; distinct from Nagga's hill. Relevant for location disambiguation: naggas-hill vs naggas-cradle (the bay). |
