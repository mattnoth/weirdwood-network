# Lens B — Whodunit / Hidden-agency + SUSPECTED_OF — A1.6 Kingsmoot / Euron proposal (S157)

> Chapters read: `affc-the-prophet-01.md`, `affc-the-iron-captain-01.md`, `affc-the-drowned-man-01.md`

---

## Proposed NEW nodes

### 1. `eurons-kingsmoot-gift-offering`
- **type:** event.incident
- **Summary:** Euron's mutes and mongrels open his chests and spill gifts before the captains and kings at the kingsmoot on Nagga's Hill — the material act of buying votes with spectacular plunder that wins him the driftwood crown. Distinct from the horn-sounding spectacle: this is the transactional bribe-offering that tips the cheering. Key captains who had been neutral (Hotho Harlaw, Gorold Goodbrother, Erik Ironmaker) visibly take gold and shout Euron's name immediately after.
- **Anchor quote:** "The mutes and mongrels from the Silence threw open Euron's chests and spilled out his gifts before the captains and the kings." `affc-the-drowned-man-01:195`

### 2. `euron-implicates-balon-in-wife-affair`
- **type:** event.incident
- **Summary:** Euron seduced / coerced Victarion's salt wife, got her with child, and then laughed openly when confronted by Victarion — forcing Victarion to do the killing himself and leaving Euron legally innocent of kinslaying while destroying Victarion's marriage and pride. Victarion recounts this as Euron's deliberate act: "He put a baby in her belly and made me do the killing."
- **Anchor quote:** "He put a baby in her belly and made me do the killing." `affc-the-iron-captain-01:269`

*(Note: a node `victarion-admits-euron-s-role-in-his-wife-s-death` already exists per baseline. `euron-implicates-balon-in-wife-affair` is the wrong slug — I will not mint a new event node here since the admission event IS already the existing node. See Dropped section.)*

---

## Proposed NEW edges

### Edge 1 — Euron manipulates the kingsmoot electorate via bribe
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `MANIPULATES` |
| Target | `kingsmoot-on-old-wyk` |
| Tier | Tier-1 |
| Qualifier | `via_bribe` |
| Quote | "The mutes and mongrels from the Silence threw open Euron's chests and spilled out his gifts before the captains and the kings. Then it was Hotho Harlaw the priest heard, as he filled his hands with gold." `affc-the-drowned-man-01:195` |
| Rationale | The text explicitly shows neutral captains (Hotho Harlaw, Gorold Goodbrother, Erik Ironmaker) shouting Euron's name *immediately after* taking his gold — a direct transactional vote-buy. Combined with the horn-spectacle, this is the mechanism by which Euron wins. MANIPULATES via_bribe is the right type: Euron used the captains as instruments to produce a crown. Target is the event node (the moot itself, the decision body). |

**Note:** MANIPULATES is Tier-1 REQUIRED-qualifier. Qualifier = `via_bribe`. Clean Tier-1 because the text directly shows the gift-spilling and the immediate chanting. This is the highest-value new agency edge.

---

### Edge 2 — Euron deceives his brothers (and the moot) about Balon's death timing
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `DECEIVES` |
| Target | `asha-greyjoy` |
| Tier | Tier-2 |
| Quote | "Three years you were gone from us, and yet Silence returns within a day of my lord father's death." `affc-the-iron-captain-01:165` |
| Rationale | Asha states the suspicious timing directly to Euron's face; Euron deflects with "I had heard the Storm God swept Balon to his death. Who is this man who slew him?" — a rhetorical move designed to create deniability while appearing to invite the accusation. His alibi (crew of mutes who can't testify) is itself a construction of deception. The DECEIVES edge (Tier-2: Asha's POV accusation is in-world, not omniscient narration; we can't *prove* the deception from published text alone) captures the in-world manipulation without asserting the murder proof. |

**[BORDERLINE]** — the deception is strongly implied but the published text never proves Euron lied about his whereabouts. Gate scrutinize.

---

### Edge 3 — Euron ASSAULTS Victarion's wife (the salt-wife seduction/rape)
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `ASSAULTS` |
| Target | `victarion-greyjoy` (the relational wound, the act was directed at Victarion via his wife) |
| Tier | Tier-1 |
| Quote | "He put a baby in her belly and made me do the killing." `affc-the-iron-captain-01:269` |
| Rationale | Victarion's own confession establishes as fact that Euron fathered a child on Victarion's salt wife. This is unambiguous from Victarion's POV. ASSAULTS is the right type (the act was a sexual assault of Victarion's household — the woman was killed, Victarion was the instrument). Target = Victarion because the existing node `victarion-admits-euron-s-role-in-his-wife-s-death` already reifies the event; this edge would add Euron as AGENT_IN that event or would model the dyadic grievance. |

**[BORDERLINE]** — check whether `euron AGENT_IN victarion-admits-euron-s-role-in-his-wife-s-death` would be cleaner (since that event node already exists). If so, prefer AGENT_IN over ASSAULTS. Proposing ASSAULTS as the dyadic form; the synthesis should pick the better shape.

---

### Edge 4 — Euron AGENT_IN the existing salt-wife event node
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `AGENT_IN` |
| Target | `victarion-admits-euron-s-role-in-his-wife-s-death` |
| Tier | Tier-1 |
| Quote | "He put a baby in her belly and made me do the killing. I would have killed him too, but Balon would have no kinslaying in his hall." `affc-the-iron-captain-01:269` |
| Rationale | The existing event node is named for Victarion's admission, but Euron is the actual agent of the underlying act. Euron AGENT_IN this event is the correct reification role (he performed the seduction/adultery that necessitated the killing). This is cleaner than a raw ASSAULTS dyad and slots into the existing event hub. Baseline shows `euron COMMANDS_IN victarion-admits-euron-s-role` — that's for Euron's putative authority in commissioning the act — but AGENT_IN for Euron as perpetrator of the seduction is DISTINCT from COMMANDS_IN and may be missing. **Dedup carefully: baseline lists `euron COMMANDS_IN victarion-admits-euron-s-role-in-his-wife-s-death` as already wired. If COMMANDS_IN is the existing edge, check whether AGENT_IN is also present; if not, this is a gap.** |

---

### Edge 5 — Aeron SUSPECTED_OF (new mechanism) — Aeron suspects Euron sent the storm / used dark means
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `SUSPECTED_OF` |
| Target | `death-of-balon-greyjoy` |
| Tier | Tier-2 |
| Quote | n/a — **DO NOT PROPOSE.** See Dropped section. |

*(Self-rejected — see below.)*

---

### Edge 6 — Euron MANIPULATES `victarion-greyjoy` via the commission (the dragon-horn trap)
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `MANIPULATES` |
| Target | `victarion-greyjoy` |
| Tier | Tier-1 |
| Qualifier | `via_false_information` |
| Quote | "And so shall we," Euron Greyjoy promised. "That horn you heard I found amongst the smoking ruins that were Valyria, where no man has dared to walk but me. You heard its call, and felt its power. It is a dragon horn, bound with bands of red gold and Valyrian steel graven with enchantments." `affc-the-drowned-man-01:185` |
| Rationale | Euron dispatches Victarion to fetch Daenerys using a horn Victarion believes will bind dragons — but the later text (ADWD Victarion chapters, already wired S132) shows Victarion planning to steal the commission's prize for himself. More importantly, the horn-sounding at the moot proves the horn burns its blower. Euron sent Victarion with a weapon Euron knew could kill the bearer. The manipulation is `via_false_information` (Euron presented the horn as a tool Victarion could safely wield). **[BORDERLINE]**: the text in these 3 chapters doesn't *prove* Euron knows the horn is deadly to its blower — that's confirmed later (ADWD). This is a Tier-2 interpretive read within the AFFC scope. Flagging borderline; gate should decide tier. |

**[BORDERLINE]** — the "Euron knows the horn kills" inference is strongest in ADWD; in AFFC it's implicit. Tier-2 safer.

---

### Edge 7 — Aeron OFFICIATES kingsmoot-on-old-wyk
| Field | Value |
|---|---|
| Source | `aeron-greyjoy` |
| Edge type | `OFFICIATES` |
| Target | `kingsmoot-on-old-wyk` |
| Tier | Tier-1 |
| Quote | "When the Damphair raised his bony hands the kettledrums and the warhorns fell silent, the drowned men lowered their cudgels, and all the voices stilled." `affc-the-drowned-man-01:37` |
| Rationale | Aeron is the priest who calls the moot, performs the opening invocation ("We were born from the sea…"), blesses candidates, and controls the ceremonial structure throughout. He OFFICIATES (performs the religious rite) — this is DISTINCT from his existing `aeron AGENT_IN kingsmoot-on-old-wyk` (participation). Baseline flags this as a potential gap ("BORDERLINE, check the text"). The text confirms he is the moot's ceremonial officiant. Tier-1 clean. |

*(This is not strictly a "whodunit" edge but falls in Lens B scope as a ritual authority edge that shapes Euron's path to power.)*

---

### Edge 8 — Euron VICTIM_IN / BANISHES: already-wired; do NOT re-propose.

### Edge 9 — Asha ACCUSES Euron (suspicion expressed in-world)
| Field | Value |
|---|---|
| Source | `asha-greyjoy` |
| Edge type | `SUSPECTED_OF` |
| Target | `death-of-balon-greyjoy` |
| Tier | Tier-2 |

**DECLINED** — `euron SUSPECTED_OF death-of-balon-greyjoy` already exists (S116). Adding `asha ACCUSES…` as a separate suspicion edge would require an ACCUSES edge type that is not in the locked vocabulary. The source of the existing SUSPECTED_OF edge already captures Asha's in-world accusation as evidence. Do not double-mint. See Dropped.

---

### Edge 10 — Silence (ship) → crew tongue-cutting
| Field | Value |
|---|---|
| Source | `euron-greyjoy` |
| Edge type | `ASSAULTS` |
| Target | `silence` |
| Tier | Tier-2 |

**DECLINED** — No verbatim text in these three chapters explicitly says "Euron cut out his crew's tongues." The text describes the crew as mutes and that they cannot speak, but doesn't prove Euron personally performed the mutilation. The mute crew is a known world-fact but not quotable from these chapters. Do not propose; see Dropped.

---

## Dropped / considered-but-rejected

1. **`euron SUSPECTED_OF death-of-balon-greyjoy` (any new form)** — ALREADY EXISTS (S116). Asha's direct confrontation ("Three years you were gone from us, and yet Silence returns within a day of my lord father's death") and Euron's alibis are the strongest in-world statement of this suspicion, but the suspicion node is already built. Baseline is explicit: do NOT re-propose. The mechanism Aeron imagines (the "Storm God's wrath") is his theological framing, not a new named suspicion entity — Aeron attributes Balon's death to the Storm God as divine agent, not to a human hireling; he does NOT explicitly say "Euron sent a hireling to cut the bridge ropes." A SUSPECTED_OF for "euron hired someone to push Balon" would be a reader inference beyond what these chapters assert. DECLINED.

2. **`euron ASSAULTS silence-crew` (tongue removal)** — No verbatim single-line quote in the three assigned chapters proves Euron cut out his crew's tongues personally. The mute crew is described ("a motley crew of mutes and mongrels spoke no word") but the act of mutilation is background world-fact, not narrated in these chapters with a quotable line. DECLINED for lack of verbatim anchor.

3. **New `SUSPECTED_OF` for Damphair's "dark means / hired killer" theory** — Aeron's POV in `affc-the-prophet-01` frames Balon's death as the Storm God's wrath ("The Storm God cast him down," line 75). He doesn't explicitly articulate "Euron sent a hireling." The closest is Aeron's dread of Euron's return ("I have seen the storm, and its name is Euron Crow's Eye," line 147) — but this is Aeron's theological/political fear, not a distinct causation theory beyond the existing SUSPECTED_OF. Adding a second mechanism-variant SUSPECTED_OF edge would be redundant. DECLINED.

4. **`euron MANIPULATES aeron-greyjoy`** — Euron taunts Aeron at the feast tent (the "godliest man ever to raise sail" speech) and the kingsmoot, driving Aeron to flee. However the taunt-to-flight sequence is better captured by existing `aeron FEARS euron` and `euron-seizes MOTIVATES aeron`. There's no clear MANIPULATES `via_*` qualifier that fits a philosophical taunt — it's not bribery, flattery, false information, threat, or seduction in the locked sense. Declined as over-reach; the existing fear/motivates chain covers it.

5. **`euron AGENT_IN victarion-admits-euron-s-role-in-his-wife-s-death` (Edge 4 above)** — Proposed but flagged for dedup against baseline COMMANDS_IN. The synthesis must verify whether AGENT_IN is already present. If COMMANDS_IN is the only existing edge, AGENT_IN fills a distinct gap (perpetrator vs. orderer). If both are already wired, drop this proposal.

6. **Second new event node for "Euron's gift-offering at kingsmoot"** — The existing `kingsmoot-on-old-wyk` event hub and the `euron AGENT_IN kingsmoot-on-old-wyk` cover participation. The gift-spilling is a sub-beat. But a `SUB_BEAT_OF` for it would require a node and is thin on its own. Declined in favor of the MANIPULATES edge (Edge 1) which captures the causal agency without needing a new sub-beat event node.

7. **Euron's speech as MANIPULATES via_flattery (the kingdoms promise)** — Euron's "I shall give you Lannisport. Highgarden. The Arbor…" speech is persuasion but functions as an outright false promise to the electorate, not a personal flattery of an individual. The existing MANIPULATES target in Edge 1 (`kingsmoot-on-old-wyk`) already covers the moot-winning mechanism; adding a second MANIPULATES via_flattery would be redundant.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| food | AFFC | `affc-the-prophet-01:47` | Aeron drinks from a leather skin of seawater — the priest's ritual drink, not food, but a notable "sustenance" beat |
| food | AFFC | `affc-the-prophet-01:185` | "Aeron broke his fast on a broth of clams and seaweed cooked above a driftwood fire" — vivid ironborn ascetic breakfast |
| food | AFFC | `affc-the-iron-captain-01:73` | Victarion feasts captains on "roast kid, salted cod, and lobster" — full kingsmoot eve feast menu |
| food | AFFC | `affc-the-iron-captain-01:73` | Aeron at that feast "ate fish and drank water" — priest's ascetic contrast to the captains' ale |
| food | AFFC | `affc-the-iron-captain-01:71` | "two Sparrs pressed a wineskin into his hands. He drank deep" — welcoming toast on the strand |
| food | AFFC | `affc-the-drowned-man-01:27` | "men wake from sleep…calling for their first horn of ale" before the moot begins |
| drink | AFFC | `affc-the-iron-captain-01:73` | "the captains quaffed enough ale to float the Iron Fleet" — scale of drinking at pre-moot feast |
| physical description | AFFC | `affc-the-iron-captain-01:37` | Silence described: "a single-masted galley, lean and low, with a dark red hull. Her sails…black as a starless sky. On her prow was a black iron maiden with one arm outstretched…no mouth." — full figurehead description |
| physical description | AFFC | `affc-the-iron-captain-01:43` | Silence crew: "Men black as tar stared out at him, and others squat and hairy as the apes of Sothoros. Monsters, Victarion thought." |
| physical description | AFFC | `affc-the-iron-captain-01:141` | Euron's appearance: "His hair was still black as a midnight sea, with never a whitecap to be seen, and his face was still smooth and pale beneath his neat dark beard. A black leather patch covered Euron's left eye, but his right was blue as a summer sky." |
| physical description | AFFC | `affc-the-iron-captain-01:141` | Euron's lips: "His smiling eye, thought Victarion. 'Crow's Eye,' he said. 'King Crow's Eye, brother.' Euron smiled. His lips looked very dark in the lamplight, bruised and blue." |
| physical description | AFFC | `affc-the-drowned-man-01:151` | Dragonbinder: "The horn he blew was shiny black and twisted, and taller than a man as he held it with both hands. It was bound about with bands of red gold and dark steel, incised with ancient Valyrian glyphs that seemed to glow redly as the sound swelled." |
| physical description | AFFC | `affc-the-drowned-man-01:155` | Dragonbinder burning its blower: "The cheeks of the tattooed man were so puffed out they looked about to burst…the glyphs were burning brightly, every line and letter shimmering with white fire." + "blood and blisters upon the lips of the man who'd sounded it" |
| physical description | AFFC | `affc-the-drowned-man-01:159` | "A thin wisp of smoke was rising from the horn" after sounding |
| physical description | AFFC | `affc-the-drowned-man-01:147` | Dragonbinder blower: "a monstrous man with a shaved head. Rings of gold and jade and jet glistened on his arms, and on his broad chest was tattooed some bird of prey, talons dripping blood." |
| physical description | AFFC | `affc-the-drowned-man-01:19` | Nagga's Hill / kingsmoot site: "four-and-forty monstrous stone ribs rose from the earth like the trunks of great pale trees…as wide around as a dromond's mast and twice as tall" |
| quote (load-bearing) | AFFC | `affc-the-iron-captain-01:145` | Euron's blasphemous creed: "Who knows more of gods than I?…I know them all. I have seen their peoples garland them with flowers, and shed the blood of goats and bulls and children in their names." — signature node quote for euron-greyjoy ## Quotes |
| quote (load-bearing) | AFFC | `affc-the-iron-captain-01:145` | "I am more devout than even you, Aeron. Perhaps it should be you who kneels to me for blessing." — Euron's blasphemy peak |
| quote (load-bearing) | AFFC | `affc-the-drowned-man-01:165` | Euron's kingsmoot claim: "Only one living kraken has never known defeat. Only one has never bent his knee." |
| quote (load-bearing) | AFFC | `affc-the-drowned-man-01:185` | Dragonbinder provenance claim: "That horn you heard I found amongst the smoking ruins that were Valyria, where no man has dared to walk but me." |
| quote (load-bearing) | AFFC | `affc-the-prophet-01:93` | Aeron on Euron vs Balon: "Better to be scorned by Balon the Brave than beloved of Euron Crow's Eye." |
| quote (load-bearing) | AFFC | `affc-the-prophet-01:169` | Aeron on Euron's ship: "The decks of Euron's ship were painted red, to better hide the blood that soaked them." |
| quote (load-bearing) | AFFC | `affc-the-iron-captain-01:269` | Victarion's confession: "He put a baby in her belly and made me do the killing. I would have killed him too, but Balon would have no kinslaying in his hall." |
| foreshadowing | AFFC | `affc-the-drowned-man-01:197` | Aeron's crisis of faith at moot's end: "Even a priest may doubt. Even a prophet may know terror…all he could hear was the scream of a rusted iron hinge." — links to The Forsaken TWOW (GATED; harvest pointer only) |
| hospitality | AFFC | `affc-the-prophet-01:185` | Aeron refuses Goodbrother's overnight hospitality: "He seldom slept beneath a castle roof, and never so far from the sea" — notable refusal of guest right |
| Victarion weapons/armor | AFFC | `affc-the-iron-captain-01:47` | Victarion's kingsmoot war-helm: "a tall black warhelm, wrought in the shape of an iron kraken, its arms coiled down around his cheeks to meet beneath his jaw" |
| kingsmoot gifts | AFFC | `affc-the-drowned-man-01:63` | Gylbert Farwynd's gifts: "sealskins and walrus tusks, arm rings made of whalebone, warhorns banded in bronze" — the thin offering that loses the moot |
| kingsmoot gifts | AFFC | `affc-the-drowned-man-01:75` | Erik Ironmaker's gifts: "a torrent of silver, bronze, and steel spilled forth; arm rings, collars, daggers, dirks, and throwing axes" |
| kingsmoot gifts | AFFC | `affc-the-drowned-man-01:97` | Drumm's gifts: "the niggard's gifts he'd brought them. No throne was ever bought with bronze" — the miser who loses |
| kingsmoot gifts | AFFC | `affc-the-drowned-man-01:105` | Victarion's gifts: "a cascade of silver, gold, and gems, a wealth of plunder" |
| kingsmoot gifts | AFFC | `affc-the-drowned-man-01:129` | Asha's gifts: pebbles from the Stony Shore, pinecones from Deepwood, turnips from Winterfell — the political theatrics of refusal |
