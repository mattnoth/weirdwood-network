# Lens C — Descriptive / Quote / Object Depth — A2.6 Jaime / Riverlands proposal (S159)

Session S159 | Model: claude-sonnet-4-6

## Proposed NEW nodes

None proposed. All relevant artifact nodes already exist (`oathkeeper`, `ice`, `widows-wail`,
`valyrian-steel`, `godswood-of-riverrun`, `great-hall-of-riverrun`, `riverrun`). No new object
node is warranted by my chapter readings — see the golden-hand note in the Dropped section.

---

## Proposed NEW edges

All six core object edges below are the highest-value targets (baseline confirms all have
zero incoming or near-zero). Deduped against the full baseline; none already exist.

---

### 1. `ice REFORGED_INTO oathkeeper`

| Field | Value |
|---|---|
| Source | `ice` |
| Edge type | `REFORGED_INTO` |
| Target | `oathkeeper` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"had Ice melted down and reforged. There was enough metal for two new blades. You're holding one."` |
| Cite | `asos-jaime-09:283` |
| Rationale | Jaime explicitly tells Brienne the provenance: Ice → Oathkeeper (and Widow's Wail). REFORGED_INTO = original artifact → resulting artifact. Single contiguous substring of line 283 of asos-jaime-09.md. |

---

### 2. `ice REFORGED_INTO widows-wail`

| Field | Value |
|---|---|
| Source | `ice` |
| Edge type | `REFORGED_INTO` |
| Target | `widows-wail` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"had Ice melted down and reforged. There was enough metal for two new blades."` |
| Cite | `asos-jaime-09:283` |
| Rationale | Same speech confirms two blades from Ice. Widow's Wail is the second (Joffrey's, per `asos-tyrion-04` and existing `joffrey-baratheon OWNS widows-wail`). The Oathkeeper quote above covers both; this is the logical twin. |

---

### 3. `oathkeeper GIFTED_TO brienne-tarth`

| Field | Value |
|---|---|
| Source | `oathkeeper` |
| Edge type | `GIFTED_TO` |
| Target | `brienne-tarth` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"Take it."` (preceded immediately by `"the blade is wasted on me."`) — using the fuller clause: `"so the blade is wasted on me. Take it."` |
| Cite | `asos-jaime-09:271` |
| Rationale | Jaime hands Brienne the sword and names it Oathkeeper. This is the marquee gift beat. `GIFTED_TO` = artifact → recipient. The VOWS_TO (brienne VOWS_TO jaime) and COMPANION_OF dyad edges (built S141) are character-to-character; this artifact→character gift is the missing link. |

---

### 4. `jaime-lannister OWNS oathkeeper`

| Field | Value |
|---|---|
| Source | `jaime-lannister` |
| Edge type | `OWNS` |
| Target | `oathkeeper` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"There was a time that I would have given my right hand to wield a sword like that. Now it appears I have, so the blade is wasted on me."` |
| Cite | `asos-jaime-09:271` |
| Rationale | Tywin gives the sword to Jaime (his father's gift, the "mocking" gift referenced at line 23 of the same chapter: "not quite so cruel as the gift his father had sent him"). Jaime holds it before gifting it — he is its owner-in-transit. OWNS is the right type (he receives it as a gift from Tywin, who had it forged for him). Immediately before the GIFTED_TO beat. |

**[BORDERLINE note]:** Alternatively `tywin-lannister GIFTED_TO jaime-lannister` for the same beat. The direct evidence in this chapter is: Kevan says "the gift was heartfelt" (line 33) and Jaime says "the gift his father had sent him" (line 23). The actual gifting scene is off-page (prior to this chapter). I'm proposing `jaime OWNS` as the presence-in-hand fact; the orchestrator may additionally want `tywin GIFTED_TO jaime` routed to asos-tyrion-04 evidence ("It is meant for my son," line 183). I am NOT proposing the Tywin edge here because the give-to-Jaime scene is not in my assigned chapters.

---

### 5. `oathkeeper MADE_OF valyrian-steel`

| Field | Value |
|---|---|
| Source | `oathkeeper` |
| Edge type | `MADE_OF` |
| Target | `valyrian-steel` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"Is this Valyrian steel? I have never seen such colors."` |
| Cite | `asos-jaime-09:269` |
| Rationale | Brienne asks the question; Jaime's implicit confirmation is the context. The explicit book-cite confirmation is even cleaner one chapter earlier in the Brienne POV: "Valyrian steel, spell-forged" (`affc-brienne-01:283`). Proposing from the Jaime-chapter line — the question from someone holding the sword, answered by Jaime's entire response, confirms the material beyond doubt. The valyrian-steel node exists. |

---

### 6. `widows-wail MADE_OF valyrian-steel`

| Field | Value |
|---|---|
| Source | `widows-wail` |
| Edge type | `MADE_OF` |
| Target | `valyrian-steel` |
| Tier | Tier 1 |
| Qualifier | none |
| Quote | `"Valyrian steel?"` `"Yes," Lord Tywin said, in a tone of deep satisfaction.` — using the contiguous quote: `"Only one metal could be beaten so thin and still have strength enough to fight with, and there was no mistaking those ripples, the mark of steel that has been folded back on itself many thousands of times."` |
| Cite | `asos-tyrion-04:161` |
| Rationale | The two swords are made from the same steel. Tyrion's observation at the presentation scene establishes both swords (the second is revealed on line 177-179 as a sibling). Widows-wail has `joffrey-baratheon OWNS widows-wail` (from purple-wedding enrichment) but no MADE_OF. This closes the gap. Note: my assigned chapters are the Jaime/AFFC set; this cite is from `asos-tyrion-04`, which is where the physical description occurs. The gate should verify this is an in-scope cite — it is canonical book text that directly proves the material claim. |

**[BORDERLINE]:** The cite is outside my assigned chapter list. However, the material fact is fully established in my assigned chapter `asos-jaime-09:269` for oathkeeper (both swords are the same steel), and `asos-tyrion-04:161` is the cleanest source for widows-wail. I am flagging this for the orchestrator to confirm or re-anchor.

---

### 7. `jaime-lannister LOCATED_AT godswood-of-riverrun` [BORDERLINE — structural not object]

| Field | Value |
|---|---|
| Source | `jaime-lannister` |
| Edge type | `LOCATED_AT` |
| Target | `godswood-of-riverrun` |
| Tier | Tier 3 |
| Qualifier | none |
| Quote | `"When morning broke the snow was ankle deep, and deeper in the godswood, where drifts had piled up under the trees."` |
| Cite | `affc-jaime-07:283` |
| Rationale | Jaime is at Riverrun throughout this chapter. The godswood-of-riverrun has 0 incoming edges. The snow observation is from Riverrun and the godswood is mentioned as part of the castle. However, this is a weak LOCATED_AT — Jaime doesn't enter the godswood himself in this chapter. **[BORDERLINE]:** The godswood mention is incidental to Jaime's location; the node has zero edges but the cite doesn't cleanly place JAIME in the godswood. Routing to Harvest instead; not proposing this edge. (Strike it — see Dropped.)

---

### Summary of live proposals

| # | Edge | Tier | Cite |
|---|---|---|---|
| 1 | `ice REFORGED_INTO oathkeeper` | Tier 1 | asos-jaime-09:283 |
| 2 | `ice REFORGED_INTO widows-wail` | Tier 1 | asos-jaime-09:283 |
| 3 | `oathkeeper GIFTED_TO brienne-tarth` | Tier 1 | asos-jaime-09:271 |
| 4 | `jaime-lannister OWNS oathkeeper` | Tier 1 | asos-jaime-09:271 |
| 5 | `oathkeeper MADE_OF valyrian-steel` | Tier 1 | asos-jaime-09:269 |
| 6 | `widows-wail MADE_OF valyrian-steel` | Tier 1 [BORDERLINE cite] | asos-tyrion-04:161 |

---

## Dropped / considered-but-rejected

- **`jaime-lannister LOCATED_AT godswood-of-riverrun`** — Jaime doesn't enter the godswood personally in the chapter; the mention at affc-jaime-07:283 is atmospheric (snow drifts "deeper in the godswood"). Weak structural cite, borderline Tier 3, routed to Harvest.

- **`jaime-lannister LOCATED_AT great-hall-of-riverrun`** — Jaime is in "Hoster Tully's solar" and the castle generally (affc-jaime-07), not explicitly placed in the great hall by name. Cannot find a clean verbatim cite placing him there specifically. Dropped.

- **`jaime-lannister WIELDS oathkeeper`** — Considered for the OWNS→GIFTED_TO transit. The text does not show Jaime actually swinging or using the sword. He receives it (off-page) and gives it to Brienne. OWNS is the correct type for a weapon held-but-not-wielded. WIELDS requires the artifact to be the instrument of a specific act; per LENS-SHARED the target of WIELDS is the artifact but the event context is an action-scene. No action-scene with Jaime wielding Oathkeeper exists.

- **`tywin-lannister GIFTED_TO jaime-lannister` (sword/oathkeeper)** — The gifting is referenced obliquely in my assigned chapter (asos-jaime-09 lines 23, 33) but the actual giving scene is off-page. The clean cite for this would be in asos-tyrion-04. Not in my assigned chapters, so I am not proposing it; the orchestrator may route this to Lens D or the synthesis pass.

- **`jaime-lannister GIFTED_TO brienne-tarth` (character→character for the mission)** — Already exists in the built Brienne dyad (VOWS_TO, PROTECTS, COMPANION_OF per baseline). The artifact-centric edge `oathkeeper GIFTED_TO brienne-tarth` (proposal #3) captures the object dimension without duplicating the person-to-person web.

- **Golden hand as new `object.artifact` node** — Considered. The golden prosthetic hand (`affc-jaime-03:119`: "The hand was wrought of gold, very lifelike, with inlaid nails of mother-of-pearl, its fingers and thumb half closed so as to slip around a goblet's stem"; `affc-jaime-07:63`: "flattened it beneath his golden hand") is a recurring object that functions narratively (Jaime uses it to strike Connington at affc-jaime-03:343). However: (a) it is a prosthetic extension of Jaime's character, not a separate artifact that changes hands or has independent agency, (b) it has no wiki node of its own (it's described within Jaime's wiki page), (c) there are no graph edges it could anchor independently that aren't already captured by the maiming event (`vargo-hoat TORTURES jaime`, built S141). **Decision: route vivid descriptions to Harvest; do NOT propose a node.** If the graph later needs object-depth edges (WORN_BY or similar) a future pass can add them with a dedicated node then. Too thin for the graph's current resolution.

- **Blackfish escape mechanism edges** — `brynden-tully LOCATED_AT water-gate-of-riverrun` or similar — the Water Gate of Riverrun doesn't have its own node. The Blackfish escape event node is Lens A/B territory (event-causal gap #2). The physical description of the Water Gate (affc-jaime-07:37) goes to Harvest.

- **`siege-of-riverrun LOCATED_AT riverrun`** — Already exists per baseline (DEDUP list states "LOCATED_AT riverrun" is live). Not re-proposed.

- **`oathkeeper WIELDED_IN` (new events)** — The two WIELDED_IN edges (the Whispers fight, the crossroads inn fight) are already built per S141 baseline. Not re-proposed.

- **Tobho Mott edges** — The armorer who reforges Ice is in `asos-tyrion-04` (not my assigned chapters). The `FORGED_BY` edge type exists in vocabulary. If the gate wants `ice FORGED_BY tobho-mott` (though strictly re-forged, not forged), that is a good proposal for synthesis — I am not proposing it as it is not in my chapter scope and the cite is outside my assigned files.

---

## Harvest

| kind | book | chapter:line | note |
|---|---|---|---|
| physical-description | ASOS | asos-jaime-09:269 | Brienne slides Oathkeeper free: "Blood and black the ripples shone. A finger of reflected light ran red along the edge." — vivid Valyrian-steel visual |
| physical-description | ASOS | asos-tyrion-04:169 | Tyrion observes the coloring: "Most Valyrian steel was a grey so dark it looked almost black… But blended into the folds was a red as deep as the grey. The two colors lapped over one another without ever touching, each ripple distinct, like waves of night and blood upon some steely shore." — definitive description of both swords' coloring |
| physical-description | ASOS | asos-tyrion-04:179 | Second sword (Jaime's/Oathkeeper): "This one was thicker and heavier, a half-inch wider and three inches longer… Three fullers, deeply incised, ran down the second blade from hilt to point." |
| quote-anchor | ASOS | asos-jaime-09:271 | "A sword so fine must bear a name. It would please me if you would call this one Oathkeeper." — the naming line; node ## Quotes candidate |
| quote-anchor | ASOS | asos-jaime-09:283 | "So you'll be defending Ned Stark's daughter with Ned Stark's own steel, if that makes any difference to you." — the thematic resonance line; node ## Quotes candidate for both oathkeeper.node.md and brienne-tarth.node.md |
| physical-description | AFFC | affc-jaime-03:119 | Golden hand described: "The hand was wrought of gold, very lifelike, with inlaid nails of mother-of-pearl, its fingers and thumb half closed so as to slip around a goblet's stem." — full physical description |
| physical-description | AFFC | affc-jaime-03:343 | Golden hand used as weapon: "Jaime's golden hand cracked him across the mouth so hard the other knight went stumbling down the steps." — Jaime strikes Red Ronnet Connington for mocking Brienne |
| food | AFFC | affc-jaime-03:125 | Hayford supper: "the invitation came down from the castle for him to sup with Lady Hayford's castellan… a course of trout was served" — first named food moment on the march |
| food | AFFC | affc-jaime-03:101 | Blackberries: "Little Lew Piper came galloping up with a helm full of blackberries, Jaime ate a handful and told the boy to share the rest with his fellow squires and Ser Ilyn Payne." |
| food | AFFC | affc-jaime-03:157 | Dead horse salted: "He gave orders for the rest of the carcass to be cut apart and salted down; it might be they would need the meat." — wartime provisioning detail |
| food | AFFC | affc-jaime-04:111 | Darry feast: bean-and-bacon soup; then a river pike baked in a crust of herbs and crushed nuts; venison and capons stuffed with leeks and mushrooms mentioned (Lady Amerei's feast for Jaime) |
| food | AFFC | affc-jaime-04:213 | Sparrows eating: "gathered round a dozen cookfires to warm their hands against the chill of dusk and watch fat sausages spit and sizzle above the flames" |
| food | AFFC | affc-jaime-07:173 | Hoster Tully's red wine: "Come, let's drink some more of Hoster Tully's good red wine" — Jaime and Ilyn drinking in Riverrun; "The wine was a deep red, sweet and heavy." |
| physical-description | AFFC | affc-jaime-07:37 | Blackfish's escape mechanism: "We raised the portcullis on the Water Gate. Not all the way, just three feet or so. Enough to leave a gap under the water, though the gate still appeared to be closed. My uncle is a strong swimmer. After dark, he pulled himself beneath the spikes." — structural detail of Riverrun's Water Gate |
| physical-description | AFFC | affc-jaime-07:39 | Blackfish in the river: "A moonless night, bored guards, a black fish in a black river floating quietly downstream." — vivid escape image |
| physical-description | AFFC | affc-jaime-07:283 | Snow in the godswood: "When morning broke the snow was ankle deep, and deeper in the godswood, where drifts had piled up under the trees." — Riverrun's godswood first snow of winter |
| quote-anchor | AFFC | affc-jaime-07:291 | Cersei's letter text: "Come at once, she said. Help me. Save me. I need you now as I have never needed you before. I love you. I love you. I love you. Come at once." — the full plea; node ## Quotes candidate for jaime-burns-cerseis-letter event when minted |
| quote-anchor | AFFC | affc-jaime-07:295 | The refusal: "Jaime rolled the parchment up again, as tight as one hand would allow, and handed it to Peck. 'No,' he said. 'Put this in the fire.'" — the marquee rupture line; node ## Quotes candidate |
| physical-description | AFFC | affc-jaime-07:277 | The snowflake on the letter: "A snowflake landed on the letter. As it melted, the ink began to blur." — load-bearing symbolic image |
| physical-description | AFFC | affc-jaime-07:249 | Silent sister dream: "it was not Cersei. She was all in grey, a silent sister. A hood and veil concealed her features, but he could see the candles burning in the green pools of her eyes." — the Joanna/silent-sister dream; the green-eyed woman says "Count your hands, child." |
| physical-description | AFFC | affc-jaime-07:265 | Dream stump: "'Count your hands, child.' One. One hand, clasped tight around the sword hilt. Only one." |
| food | AFFC | affc-jaime-07:207 | Garrison provisioned: "Each man was allowed three days' food and the clothing on his back" — austere departure terms for Tully garrison |
| hospitality | AFFC | affc-jaime-04:43-44 | Darry maester offers feast: "Lady Amerei wished to welcome you herself, but she is seeing to the preparation of a feast in your honor." — typical siege-era hospitality offer |
| food | ASOS | asos-jaime-09:23 | Jaime broods: "the gift his father had sent him" — references the sword-as-gift obliquely; the food/drink at this level is the wine Cersei smells of (not a food beat per se) |
| physical-description | AFFC | affc-jaime-03:75-76 | Pycelle's beard and decline: "Pycelle looked not only old, but feeble… his beard had been magnificent, white as snow and soft as lambswool… concealed all manner of unsavory things." — vivid character description (cross-reference: affc-jaime-01:75) |
| physical-description | ASOS | asos-jaime-09:267 | Oathkeeper unwrapped: "He reached down under the Lord Commander's chair and brought it out, wrapped in folds of crimson velvet. Brienne approached… reached out a huge freckled hand, and flipped back a fold of cloth. Rubies glimmered in the light." — the presentation moment |
