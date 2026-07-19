# D&E Harvest Sidecar — LOCATE-STATS

> Generated: 2026-07-19T21:26:20+00:00  
> harvest source: /Users/mnoth/source/asoiaf-chat/working/dunk-egg-pass1/harvest-dunk-egg.jsonl  
> S222 follow-up: ellipsis segmentation (Tier 2) + dialogue-tag-strip split (Tier 3) + located_ambiguous (2-5 hit fragments) added.  

## Totals

| Stage | Count |
|-------|-------|
| Raw harvest lines | 372 |
| Parsed rows | 372 |
|  -> needed embedded-slash rejoin | 4 |
| Unparseable rows | 0 |
| Routed to causal-spine-seeds.jsonl (NOT drained this session) | 75 |
| Drainable rows (locate attempted) | 297 |
|  -> located (unique hit) | 243 |
|  -> located_ambiguous (2-5 hits, best fragment) | 8 |
|  -> NOT located | 46 |

## Per-book totals (parsed rows)

| Book | Count |
|------|-------|
| TMK | 133 |
| THK | 124 |
| TSS | 115 |

## Per-kind breakdown (drainable kinds only; causal-spine excluded)

| Kind | Total | Located | Ambiguous | Not Located | Located % | Located+Ambiguous % | No-candidate rows |
|------|-------|---------|-----------|-------------|-----------|----------------------|--------------------|
| targaryen-history | 97 | 82 | 3 | 12 | 84.5% | 87.6% | 0 |
| cross-identity | 63 | 50 | 0 | 13 | 79.4% | 79.4% | 0 |
| description | 42 | 37 | 0 | 5 | 88.1% | 88.1% | 0 |
| hospitality | 26 | 20 | 0 | 6 | 76.9% | 76.9% | 0 |
| foreshadow-hook | 23 | 19 | 3 | 1 | 82.6% | 95.7% | 0 |
| prophecy | 22 | 20 | 2 | 0 | 90.9% | 100.0% | 0 |
| food | 21 | 12 | 0 | 9 | 57.1% | 57.1% | 0 |
| other | 3 | 3 | 0 | 0 | 100.0% | 100.0% | 0 |

## causal-spine (staged, not drained)

75 rows written to `causal-spine-seeds.jsonl` — these seed a future event-wiring slice, not processed further this session.

## Fragment grep-stage counts (candidate-level, across all drainable rows)

| Stage | Count |
|-------|-------|
| exact (Tier 1) | 223 |
| normalized (Tier 1 fallback) | 10 |
| ellipsis-segmented (Tier 2) | 58 |
| dialogue-tag-strip (Tier 3) | 3 |
| none (fragment ungrounded on every tier) | 50 |

## Not-located rows with ZERO candidate fragments (no quotes, pointer <5 words)

0 row(s):

(none)

## Tier 2/3 recoveries (first 30) — ellipsis-segmented / dialogue-tag-strip hits

30 shown (of 61 total Tier-2/3 grounded candidates):

| Book | Kind | Stage | Cite Line | Span | Parts | Harvest Line |
|------|------|-------|-----------|------|-------|--------------|
| THK | cross-identity | ellipsis-segmented | 1309 | 0 | I did not think to enter the lists at As@1309 | so I brought no armor. My son was good e@1309 | 16 |
| THK | prophecy | ellipsis-segmented | 1159 | 0 | My dreams are not like yours, Ser Duncan@1159 | I dreamed of you and a dead dragon@1159 | 18 |
| THK | prophecy | dialogue-tag-strip | 75 | 0 | I dreamed of you.@75 | You stay away from me@75 | 61 |
| THK | targaryen-history | ellipsis-segmented | 433 | 0 | the third was older, well worn, and show@433 | Dunk could not read the letters@433 | 76 |
| THK | cross-identity | dialogue-tag-strip | 581 | 0 | Ser Damon Lannister!@581 | The Grey Lion! He's Lord of Casterly Roc@581 | 89 |
| THK | food | ellipsis-segmented | 517 | 0 | fresh bread@517 | a bit of cheese@517 | good cheese at one of the stalls@517 | 95 |
| THK | foreshadow-hook | ellipsis-segmented | 865 | 0 | the youngest boy was with him@865 | They left Summerhall together but never @865 | 101 |
| THK | cross-identity | ellipsis-segmented | 955 | 2 | It was him shaved my head@955 | mine is like Aerion's and my father's@957 | 109 |
| THK | description | ellipsis-segmented | 1143 | 0 | Aerion@1143 | used to come into my bedchamber at night@1143 | 116 |
| THK | targaryen-history | ellipsis-segmented | 1479 | 0 | Baelor of House Targaryen, Prince of Dra@1479 | heir apparent to the Iron Throne@1479 | 135 |
| TSS | targaryen-history | ellipsis-segmented | 709 | 0 | it was the kinslayer who turned the tide@709 | King Aerys is his creature@709 | 177 |
| TSS | targaryen-history | ellipsis-segmented | 859 | 2 | The last died in the spring@859 | a wise old king and two young princes fu@861 | 179 |
| TSS | hospitality | ellipsis-segmented | 609 | 0 | You'd best not take any food or drink@609 | The Red Widow poisoned all her husbands@609 | 184 |
| TSS | targaryen-history | ellipsis-segmented | 1109 | 0 | Ser Eustace chose the black dragon over @1109 | His sons paid for his treason with their@1109 | 191 |
| TSS | food | ellipsis-segmented | 917 | 0 | This is an Arbor vintage@917 | the poison gives it a special piquance@917 | 192 |
| TSS | description | ellipsis-segmented | 929 | 0 | the dark green glow of wildfire@929 | they piled them in the Dragonpit@929 | Lord Rivers commanded the pyromancers to@929 | 194 |
| TSS | description | ellipsis-segmented | 1141 | 0 | She loved the boy, and him her@1141 | it was Addam she wept for after the Redg@1141 | 199 |
| TSS | description | ellipsis-segmented | 1093 | 0 | As the river is called the Mander, thoug@1093 | The world changes, ser@1093 | 200 |
| TSS | targaryen-history | ellipsis-segmented | 1253 | 0 | if Fireball had not been slain on the ev@1253 | if Quickfinger had not been caught with @1253 | so many if s@1253 | 206 |
| TSS | foreshadow-hook | ellipsis-segmented | 1193 | 2 | all bastards are born to betrayal@1193 | in the end he would prove himself a trai@1195 | 209 |
| TSS | description | ellipsis-segmented | 1257 | 0 | I bought my head back with my daughter's@1257 | twenty when she died, a silent sister@1257 | 211 |
| TSS | targaryen-history | ellipsis-segmented | 1437 | 2 | The last of the green kings perished on @1437 | Afterward the blades were gathered up, a@1439 | 216 |
| TMK | targaryen-history | ellipsis-segmented | 27 | 0 | remember our true king across the water@27 | the Black Dragon sired seven sons@27 | 233 |
| TMK | targaryen-history | ellipsis-segmented | 213 | 4 | House Peake did hold three castles once,@213 | You fight for the Black Dragon@217 | 235 |
| TMK | hospitality | ellipsis-segmented | 159 | 0 | Come, ride with us to Whitewalls@159 | celebrate his new marriage@159 | 238 |
| TMK | cross-identity | ellipsis-segmented | 381 | 0 | war between Lord Rivers and Prince Maeka@381 | the Hand against the heir@381 | 245 |
| TMK | targaryen-history | ellipsis-segmented | 349 | 0 | Aegon the Unworthy@349 | legitimized them all upon his deathbed@349 | the Great Bastards@349 | 247 |
| TMK | targaryen-history | ellipsis-segmented | 413 | 0 | The old king gave him the sword@413 | Blackfyre@413 | in place of Daeron's@413 | 248 |
| TMK | targaryen-history | ellipsis-segmented | 329 | 0 | When the Black Dragon rose@329 | Both perished on the Redgrass Field@329 | 249 |
| TMK | hospitality | ellipsis-segmented | 321 | 0 | Ser Maynard has a bag of apples@321 | I have pickled eggs and onions@321 | the makings of a feast@321 | 253 |

## located_ambiguous examples (first 30)

8 shown (of 8 total):

| Book | Kind | Pointer | Best Fragment Hit-Count | Harvest Line |
|------|------|---------|--------------------------|--------------|
| THK | targaryen-history | "heir apparent to the Iron Throne" | 2 | 22 |
| TSS | targaryen-history | "A thousand eyes, and one" | 3 | 145 |
| TSS | foreshadow-hook | "How many eyes does Lord Bloodraven have? A thousand eyes, and one" | 2 | 166 |
| TSS | foreshadow-hook | "How many eyes does Lord Bloodraven have? A thousand eyes, and one" | 2 | 195 |
| TMK | foreshadow-hook | "How many eyes does Lord Bloodraven have? A thousand eyes, and one" | 2 | 268 |
| TMK | targaryen-history | "Lord Sunderland fought for the Black Dragon, ser... He bears the heads of three pale ladi | 2 | 290 |
| TMK | prophecy | "My dreams do not lie" | 2 | 324 |
| TMK | prophecy | "I dreamed that you were all in white from head to heel, with a long pale cloak flowing fr | 2 | 351 |

## Not-located examples (first 50, includes rows WITH candidates that failed to ground on every tier)

| Book | Kind | Pointer | # Candidates Tried | Harvest Line |
|------|------|---------|---------------------|--------------|
| THK | cross-identity | the bald stableboy "Egg" | 2 | 1 |
| THK | cross-identity | a black knight in white scale armor | 1 | 3 |
| THK | food | lamb roasted with a crust of herbs, duck cooked with cherries and lemons | 2 | 10 |
| THK | hospitality | a goat basted with honey and herbs | 1 | 11 |
| THK | description | the elm tree on a sunset field with a shooting star | 2 | 13 |
| THK | cross-identity | "Ser Duncan the Tall" | 2 | 15 |
| THK | targaryen-history | "the last dragon... None of her eggs had ever hatched. Some say King Aegon poisoned her" | 1 | 21 |
| THK | targaryen-history | "My brother Aemon... is off at the Citadel now, learning to be a maester" | 1 | 24 |
| THK | hospitality | "a goat basted with honey and herbs" | 1 | 26 |
| TSS | hospitality | "This is an Arbor vintage, very fine, and the poison gives it a special piquance" | 1 | 47 |
| TSS | description | "the maesters shaved it off" | 1 | 49 |
| THK | food | lamb roasted with a crust of herbs; duck cooked with cherries and lemons | 1 | 63 |
| THK | cross-identity | "Ser Duncan the Tall" | 2 | 66 |
| THK | cross-identity | "blue eyes, very dark, almost purple" | 1 | 75 |
| THK | food | lamb, duck, sausages, woodsmoke and bacon across the tourney field | 1 | 79 |
| THK | cross-identity | "I cut it off, brother. I didn't want to look like you." | 1 | 96 |
| THK | targaryen-history | "the king's fourth son... Daeron is a sot, Aerion is vain and cruel, the third son... a ma | 1 | 98 |
| THK | food | "break their fast on goose eggs, fried bread, and bacon" | 1 | 104 |
| THK | targaryen-history | "Like Aegon the Dragon. How many Aegons have been king? Four." | 1 | 110 |
| THK | targaryen-history | "the blood of the dragon. Silver-gold hair and purple eyes" | 1 | 113 |
| THK | cross-identity | "My son was good enough to lend me his [armor]" | 2 | 123 |
| THK | hospitality | "A knight who remembered his vows." | 1 | 127 |
| THK | targaryen-history | "I have sent Aerion to Lys." | 1 | 137 |
| TSS | targaryen-history | "King Maegor who took Coldmoat from us, when Lord Ormond Osgrey spoke out against his supp | 1 | 169 |
| TSS | cross-identity | "He's his brother, and the finest battle commander in the realm since Uncle Baelor died" | 1 | 204 |
| TSS | targaryen-history | "He legitimized the lot upon his deathbed; not only the Great Bastards like Bloodraven, Bi | 1 | 205 |
| TSS | hospitality | "the walls and towers of Coldmoat had vanished... She struck my envoy, who came to her ben | 1 | 212 |
| TSS | description | "dragons red and black... chequy lions, old shields, battered boots... papers stamped with | 1 | 217 |
| TSS | description | "the Red Widow, Rohanne of the Coldmoat... coal-black mare decked out in strands of silver | 1 | 218 |
| TSS | cross-identity | "A signet. Gold and onyx... Where did you find this? / In a boot. Wrapped in rags and stuf | 1 | 219 |
| TSS | food | "They washed them down with ale... He ate four of the eggs. Egg ate two" | 1 | 222 |
| TMK | targaryen-history | "he perches on King Aerys's shoulder and caws into his ear" | 1 | 231 |
| TMK | food | "they brewed a fine brown ale... a slice off the roast, a bit of duck, a bowl of stew" | 1 | 237 |
| TMK | targaryen-history | "Bittersteel sits in exile, where ... plotting with the sons of Daemon Blackfyre" | 1 | 250 |
| TMK | food | "It's wild boar, well peppered, and served with onions, mushrooms, and mashed neeps" | 1 | 252 |
| TMK | food | "In place of suckling pig, they got salt pork soaked in almond milk and peppered" | 1 | 271 |
| TMK | targaryen-history | "Bittersteel be buggered. No bastard can be trusted, not even him. A few victories will br | 1 | 279 |
| TMK | cross-identity | "keep my hair shaved or dyed, and tell no man my true name" | 1 | 283 |
| TMK | targaryen-history | "his father's fiery sigil... Fireball's son" | 1 | 295 |
| TMK | hospitality | "the foul potion... avoid rich foods, strong drink, and further blows between your eyes" | 1 | 302 |
| TMK | cross-identity | "born of a camp follower. Jenny... fed the lad the tale... about him being Fireball's seed | 1 | 315 |
| TMK | description | "a single pale white eye... no more than the moonstone brooch that pinned his cloak... som | 2 | 334 |
| TMK | cross-identity | "the man who'd called himself the Fiddler ... '—is Daemon, aye ... The Black Dragon.'" | 1 | 339 |
| TMK | food | "a bowl o' brown, they called such fare in the pot shops of King's Landing ... a film of g | 1 | 341 |
| TMK | cross-identity | "A single white dragon announced the presence of the King's Hand, Lord Brynden Rivers. Blo | 1 | 346 |
| TMK | foreshadow-hook | "Were I to guess, I'd say someone climbed up inside the privy shaft ... A child could do i | 1 | 361 |

## Commands run

```
python3 scripts/dunk-egg-harvest-locate.py --harvest /Users/mnoth/source/asoiaf-chat/working/dunk-egg-pass1/harvest-dunk-egg.jsonl --out-dir /Users/mnoth/source/asoiaf-chat/working/dunk-egg-graph-ingest/harvest
```

