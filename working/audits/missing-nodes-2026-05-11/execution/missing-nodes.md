# Missing graph-node candidates — 2026-05-11

> Audit of wiki pages cached in `sources/wiki/_raw/` that have no graph node at their canonical kebab slug.
> Three buckets, sorted by signal strength (Pass 1 chapter mentions > wiki backlinks > nothing).

- **Total wiki pages indexed**: 17,657
- **Total graph nodes**: 7,583
- **Unpromoted pages (excluding `skip` category)**: 1,170
- **Pass-1-referenced unpromoted (bucket A)**: 138
- **Highly-backlinked unpromoted (bucket B)**: 83
- **Tail unpromoted (bucket C)**: 949

## Case-collision redirect crawl bugs

The case-insensitive macOS HFS+ filesystem collapsed `<Name>` and `<name>` to one disk entry during the original wiki crawl. **125 cached pages** are redirect-only and the canonical-content variant never made it to disk. Re-crawling these specific pages would require a narrow exception fetch (per CLAUDE.md).

| Filename | Redirect target |
|---|---|
| `House_Words.json` | House words |
| `High_Road.json` | High road |
| `Red_Priest.json` | Red priest |
| `Trade_Talk.json` | Trade talk |
| `Rosby_Road.json` | Rosby road |
| `Children_of_the_Forest.json` | Children of the forest |
| `Lyman_(Archmaester).json` | Lyman (archmaester) |
| `Free_Folk.json` | Free folk |
| `Known_World.json` | Known world |
| `Rock_King.json` | Rock king |
| `Valar_Morghulis.json` | Valar morghulis |
| `Beyond_the_Wall_(Book).json` | Beyond the Wall (book) |
| `POV_Character.json` | POV character |
| `Dake_(Guard).json` | Dake (guard) |
| `Damon_Dance-For-Me.json` | Damon Dance-for-Me |
| `Roland_Crakehall_(Lord).json` | Roland Crakehall (lord) |
| `All-For-Joffrey.json` | All-for-Joffrey |
| `Landed_Knight.json` | Landed knight |
| `Red_Comet.json` | Red comet |
| `Lymond_(Disambiguation).json` | Lymond (disambiguation) |
| `Ice_Dragon.json` | Ice dragon |
| `Red_Raven_(Free_Folk).json` | Red Raven (free folk) |
| `Chief_Undergaoler.json` | Chief undergaoler |
| `Old_Gods.json` | Old gods |
| `Roone_(Maester).json` | Roone (maester) |
| `The_Princess_and_The_Queen,_or,_The_Blacks_and_The_Greens.json` | The Princess and the Queen, or, the Blacks and the Greens |
| `Harmune_(Archmaester).json` | Harmune (archmaester) |
| `Two_Hearts_That_Beat_As_One.json` | Two Hearts That Beat as One |
| `Helicent_(Hound).json` | Helicent (hound) |
| `King_In_The_North.json` | King in the North |
| `Finger_Dance.json` | Finger dance |
| `Pate_(Novice).json` | Pate (novice) |
| `Willow_(Hound).json` | Willow (hound) |
| `Starved_Man.json` | Starved man |
| `Drowned_Men.json` | Drowned men |
| `Great_Voyages.json` | Great voyages |
| `Grand_Master.json` | Grand master |
| `Hammer_of_the_Waters.json` | Hammer of the waters |
| `Seventy-nine_Sentinels.json` | Seventy-nine sentinels |
| `Gerold_(Archmaester).json` | Gerold (archmaester) |
| `House_Lake_(North).json` | House Lake (north) |
| `Queen_of_Love_and_Beauty.json` | Queen of love and beauty |
| `Narrow_Sea.json` | Narrow sea |
| `Stallion_Who_Mounts_the_World.json` | Stallion who mounts the world |
| `Trial_of_Seven.json` | Trial of seven |
| `Dothraki_Sea.json` | Dothraki sea |
| `Erryk_(Guard).json` | Erryk (guard) |
| `First_Night.json` | First night |
| `River_Road.json` | River road |
| `Master_of_Whisperers.json` | Master of whisperers |
| ... | _75 more_ |

## Bucket A — Pass 1 references them (138 pages)

These wiki pages exist but Pass 1 mentions them across the chapter corpus with NO graph node to resolve to. **Highest backfill priority.**

| Page | Slug | Pass 1 mentions | Wiki in-edges | Bytes | Type guess | Top categories |
|---|---|---|---|---|---|---|
| Godswood | `godswood` | 36 | 31 | 36,366 | unknown | Godswoods, Old gods, Terms |
| Flea Bottom | `flea-bottom` | 31 | 30 | 51,403 | unknown | King's Landing |
| Old Gods | `old-gods` | 22 | 61 | 910 | unknown | - |
| Seastone Chair | `seastone-chair` | 14 | 37 | 27,123 | unknown | House Greyjoy, Ironborn culture, Thrones |
| Chataya's brothel | `chatayas-brothel` | 12 | 11 | 32,278 | unknown | Brothels in King's Landing, Chataya's brothel |
| Black cells | `black-cells` | 11 | 46 | 37,174 | unknown | Prisons, Red Keep, Terms |
| Queen's Men | `queens-men` | 9 | 43 | 926 | unknown | - |
| Unsullied | `unsullied` | 9 | 68 | 55,403 | unknown | Astapor, Eunuchs, Slave soldiers |
| Cinnamon Wind | `cinnamon-wind` | 8 | 19 | 12,416 | unknown | Swan ships |
| Valyrian steel dagger | `valyrian-steel-dagger` | 8 | 4 | 953 | unknown | - |
| Black Wind | `black-wind` | 7 | 2 | 19,936 | unknown | Crew of the Black Wind, House Greyjoy ships, Ironborn longships |
| Hobb | `hobb` | 7 | 3 | 937 | unknown | - |
| Maidenvault | `maidenvault` | 7 | 16 | 15,247 | unknown | Buildings, Red Keep |
| Malaquo | `malaquo` | 7 | 1 | 927 | unknown | - |
| Nyessos | `nyessos` | 7 | 0 | 930 | unknown | - |
| Gunthor son of Gurn | `gunthor-son-of-gurn` | 6 | 0 | 907 | unknown | - |
| Harma | `harma` | 6 | 8 | 928 | unknown | - |
| Iron Victory | `iron-victory` | 6 | 3 | 18,398 | unknown | Crew of the Iron Victory, House Greyjoy ships, Ironborn longships |
| Qezza | `qezza` | 6 | 3 | 922 | unknown | - |
| Valar Morghulis | `valar-morghulis` | 6 | 8 | 931 | unknown | - |
| Crossroads Inn | `crossroads-inn` | 5 | 39 | 949 | unknown | - |
| Doniphos | `doniphos` | 5 | 0 | 939 | unknown | - |
| Pretty Pig | `pretty-pig` | 5 | 6 | 4,323 | unknown | Pigs |
| Rookery | `rookery` | 5 | 15 | 37,574 | unknown | Order of the maesters, Ravens, Terms |
| The Ship | `the-ship` | 5 | 1 | 934 | unknown | - |
| Ulmer | `ulmer` | 5 | 4 | 952 | unknown | - |
| Castle Stair | `castle-stair` | 4 | 4 | 6,449 | unknown | Stairs, Streets, White Harbor |
| Daenerys Stormborn | `daenerys-stormborn` | 4 | 0 | 940 | unknown | - |
| Frozen Shore | `frozen-shore` | 4 | 8 | 23,142 | unknown | Places beyond the Wall |
| King Maegor | `king-maegor` | 4 | 0 | 940 | unknown | - |
| _108 more in JSON sidecar_ | | | | | | |

## Bucket B — Heavily wiki-backlinked but Pass 1 silent (83 pages)

Other wiki pages reference these (≥10 backlinks) but no chapter mentions them. Often historical figures from D&E or TWOIAF — relevant to graph traversal but not to the main narrative arc.

| Page | Slug | Pass 1 mentions | Wiki in-edges | Bytes | Type guess | Top categories |
|---|---|---|---|---|---|---|
| Blacks | `blacks` | 0 | 138 | 79,944 | event.war | Blacks, Dance of the Dragons, Organizations |
| Greens | `greens` | 0 | 127 | 56,982 | event.war | Dance of the Dragons, Greens, Organizations |
| Maiden | `maiden` | 0 | 77 | 23,488 | unknown | Terms |
| Fool | `fool` | 0 | 70 | 61,927 | unknown | Jesters |
| Mountain's men | `mountains-men` | 0 | 65 | 60,021 | unknown | House Clegane retainers |
| Khalasar | `khalasar` | 0 | 63 | 6,932 | unknown | Dothraki culture, Khalasars, Terms |
| Dragonflame | `dragonflame` | 0 | 61 | 62,637 | unknown | Dragons |
| Slavery | `slavery` | 0 | 56 | 95,436 | unknown | Slavery |
| Hound | `hound` | 0 | 45 | 32,204 | unknown | Brave Companions, Brotherhood Without Banners, Collective nicknames |
| Royal progress | `royal-progress` | 0 | 45 | 61,464 | unknown | House Targaryen, Monarchs, Terms |
| Age of Heroes | `age-of-heroes` | 0 | 43 | 29,473 | unknown | History, Terms, Westeros |
| Thoros of Myr | `thoros-of-myr` | 0 | 43 | 904 | unknown | - |
| March on Winterfell | `march-on-winterfell` | 0 | 42 | 43,694 | unknown | House Baratheon of Dragonstone, House Bolton battles, House Frey battles |
| Eunuch | `eunuch` | 0 | 39 | 53,002 | unknown | Eunuchs |
| Silk | `silk` | 0 | 37 | 143,457 | unknown | Clothing |
| Dwarf | `dwarf` | 0 | 36 | 35,749 | unknown | Articles with unsourced statements, Dwarfs, Pages using hatnote template directly |
| Rattleshirt | `rattleshirt` | 0 | 36 | 924 | unknown | - |
| Andal | `andal` | 0 | 35 | 904 | unknown | - |
| Trial of Seven | `trial-of-seven` | 0 | 35 | 928 | unknown | - |
| Named after | `named-after` | 0 | 31 | 910 | unknown | - |
| Purple eyes | `purple-eyes` | 0 | 31 | 59,918 | unknown | Characters with purple eyes, House Blackfyre, House Dayne |
| Redwyne fleet | `redwyne-fleet` | 0 | 31 | 33,056 | unknown | Fleets, House Redwyne, Redwyne fleet |
| Crypt of Winterfell | `crypt-of-winterfell` | 0 | 29 | 52,320 | unknown | House Stark, Winterfell |
| Lackwit | `lackwit` | 0 | 25 | 13,270 | unknown | Lackwits, Terms |
| Armament | `armament` | 0 | 24 | 174,018 | object.artifact | Science and technology, Weapons |
| Blackfyre Pretenders | `blackfyre-pretenders` | 0 | 24 | 90,453 | unknown | Blackfyre Rebellions, House Blackfyre |
| Outlaws | `outlaws` | 0 | 24 | 20,630 | unknown | Articles that are Stubs, Outlaws |
| The Bloody Hand | `the-bloody-hand` | 0 | 24 | 10,879 | unknown | Plays |
| Velaryon fleet | `velaryon-fleet` | 0 | 24 | 50,184 | unknown | Fleets, House Velaryon, House Velaryon ships |
| Battle at Winterfell | `battle-at-winterfell` | 0 | 23 | 1,000 | unknown | - |
| _53 more in JSON sidecar_ | | | | | | |

## Bucket C — Tail (949 pages)

Low signal — no Pass 1 mention, <10 wiki backlinks. Mostly minor characters, list/disambiguation pages, and very peripheral entries. Probably fine to leave unpromoted.
