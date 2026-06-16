# Mode 3 Grounded-Agent Dip — 2026-06-15

## 1. Graph State at Test Time

```
Node files (*.node.md)  :   8,528
Edge count              :  21,993
Unique edge endpoints   :   5,950
Orphan endpoints        :      62
Unique edge types       :     125
```

Key edge-type counts relevant to this dip:
- KILLS: 115, VICTIM_IN: 338, AGENT_IN: 363, COMMANDS_IN: 175
- WIELDED_IN: 10, ATTENDS: 42, SUB_BEAT_OF: 66
- CROWNS_QUEEN_OF_LOVE_AND_BEAUTY: 1, TRIGGERS: 2
- BORN_AT: 835, SWORN_TO: 4148, PARENT_OF: 1686

---

## 2. Per-Query Results Table

| # | Query | Resolver phrase tried → result | Graph's answer | Ground truth (file) | Grade | Failure mode |
|---|-------|-------------------------------|----------------|---------------------|-------|-------------|
| 1 | Who killed Robb Stark? | `"Robb Stark's death"` → **HIT** `robb-is-killed`; `"Robb Stark"` → **HIT-CHARACTER** `robb-stark` | `--neighbors robb-is-killed`: AGENT_IN ← roose-bolton ("A man in dark armor and pale pink cloak…thrust his longsword through Robb's heart"); COMMANDS_IN ← walder-frey; VICTIM_IN ← robb-stark | `asos-catelyn-07.md:135`: "A man in dark armor and a pale pink cloak spotted with blood stepped up to Robb. 'Jaime Lannister sends his regards.' He thrust his longsword through her son's heart, and twisted." Roose Bolton confirmed. | **correct** | — |
| 2 | Who ordered the Red Wedding? | `"the Red Wedding"` → **HIT** `red-wedding` | `--event-participants red-wedding` (12 beats, 44 role edges): COMMANDS_IN from **tywin-lannister** (via `red-wedding-revealed` beat, quote: "Tywin confirms he and Walder Frey planned it; says no one was told who didn't need to know"), **walder-frey** (multiple beats), **roose-bolton** (multiple beats) | `asos-tyrion-06.md`: Tywin confirms joint plan with Walder Frey; coded message from Frey; Roose Bolton rewarded with Warden of the North. Three co-architects confirmed. | **correct** | — |
| 3 | Who crowned Lyanna Stark Queen of Love and Beauty? | `"Lyanna crowned queen of love and beauty"` → **CANDIDATES** (fuzzy, score=0.75 for `queen-of-love-and-beauty`); `"Lyanna Stark"` → **HIT-CHARACTER** `lyanna-stark` | Via `--neighbors lyanna-stark`: INCOMING `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY ← rhaegar-targaryen` (ref: `agot-eddard-15.md:45`, quote: "Ned remembered the moment when all the smiles died, when Prince Rhaegar Targaryen urged his horse past his own wife…to lay the queen of beauty's laurel in Lyanna's lap."). Also `--path rhaegar-targaryen lyanna-stark` confirms this direct edge. | `agot-eddard-15.md:45`: "Prince Rhaegar Targaryen urged his horse past his own wife, the Dornish princess Elia Martell, to lay the queen of beauty's laurel in Lyanna's lap. He could see it still: a crown of winter roses, blue as frost." | **partial** | `slug-discoverability` — first resolver phrase "Lyanna crowned queen of love and beauty" returned only a fuzzy CANDIDATE (the concept node `queen-of-love-and-beauty`, which itself has 0 edges). Consumer agent must pivot to character lookup to find the answer. The data is excellent once you reach `lyanna-stark`. |
| 4 | What weapon killed Robb Stark? | `"weapon that killed Robb Stark"` → **MISS** (no confident match; fuzzy top=`robb-is-killed` score=0.70) | `--neighbors robb-is-killed`: VICTIM_IN quote says "He thrusts his longsword through Robb's heart." No WIELDED_IN edge on this event. (Correct restraint: the weapon is a generic unnamed longsword — no named artifact node warranted.) | `asos-catelyn-07.md:135`: "He thrust his longsword through her son's heart, and twisted." Weapon = unnamed longsword. Per schema rules, no WIELDED_IN edge is correct. But the answer ("a longsword") lives only in the VICTIM_IN evidence quote, not as a structured edge. | **partial** | `prose-only` — the weapon is named in the evidence_quote on the VICTIM_IN edge, but there is no structured edge type that expresses "killed with X type of weapon" for generic weapons. A consumer agent reading only edge_types gets "Roose Bolton killed Robb" but must read the quote string to learn it was a longsword. Also note: resolver MISS on the natural "weapon that killed Robb" phrase — the event node is unreachable without the user already knowing it's `robb-is-killed`. |
| 5 | Who fought at the Tourney at Harrenhal? | `"Tourney at Harrenhal"` → **HIT** `tourney-at-harrenhal` | `--neighbors tourney-at-harrenhal`: ATTENDS (16): aerys-ii-targaryen, eddard-stark, lyanna-stark, elia-martell, jon-arryn, eon-hunter, jaime-lannister, gerold-hightower, howland-reed, benjen-stark, ashara-dayne, oberyn-martell, jon-connington, mace-tyrell, richard-lonmouth, walter-whent. FIGHTS_IN (8): rhaegar-targaryen, barristan-selmy, arthur-dayne, brandon-stark, yohn-royce, robert-baratheon, knight-of-the-laughing-tree, oswell-whent. | `agot-eddard-15.md` and `asos-bran-02.md`: Rhaegar jousted (defeated Brandon, Yohn Royce, Arthur Dayne, Barristan); Robert fought in the melee; the Knight of the Laughing Tree competed. Attendance list matches chapter text. | **correct** | — |
| 6 | What is the connection between Tywin Lannister and Gregor Clegane? | `"Tywin Lannister"` → **HIT-CHARACTER** `tywin-lannister`; `"Gregor Clegane"` → **HIT-CHARACTER** `gregor-clegane` | `--path tywin-lannister gregor-clegane`: 4 direct edges: `tywin-lannister --[COMMANDS]--> gregor-clegane` (quote: Arya fearing both); `gregor-clegane --[SERVES]--> tywin-lannister` ("Clegane is no more than Lord Tywin's catspaw"); `gregor-clegane --[SWORN_TO]--> tywin-lannister` ("Ser Gregor Clegane stood bannerman to Lord Tywin Lannister."); `tywin-lannister --[PROTECTS]--> gregor-clegane` ("No other knight in the realm inspires such terror in our enemies"). | Chapter text confirms: Gregor is Tywin's bannerman and instrument, sent on raids; Tywin protects him from consequences. All four edges accurate. | **correct** | — |
| 7 | Who attended Ned Stark's execution? | `"Ned Stark's execution"` → **HIT** `execution-of-eddard-stark`; `"execution of Eddard Stark"` → **HIT** | `--neighbors execution-of-eddard-stark`: AGENT_IN ← ilyn-payne; COMMANDS_IN ← joffrey-baratheon; VICTIM_IN ← eddard-stark; WIELDED_IN ← ice; LOCATED_AT → great-sept-of-baelor. No ATTENDS edges. | `agot-arya-05.md:141–163`: Present: Joffrey (commands the beheading), Cersei (beside Joffrey), Sansa (weeping), Arya (watching from crowd outside), High Septon, Ilyn Payne (executes), Sandor Clegane (Hound, white cloak), Varys, Kingsguard, Janos Slynt (gold cloaks). The graph captures only commander + agent + victim + weapon. All witnesses missing: Sansa, Cersei, Varys, Sandor, High Septon, Arya. | **partial** | `dark-vocab` — ATTENDS has 42 edges graph-wide but none on this event. No WITNESSES or PRESENT_AT edge type. The execution hub is otherwise well-formed (Ilyn Payne, Ice, Joffrey confirmed); attendance is just structurally absent. |
| 8 | Jon Snow: relation to Ned, sworn to, and where born? | `"Jon Snow"` → **HIT-CHARACTER** `jon-snow` | `--path jon-snow eddard-stark`: direct edge `eddard-stark --[PARENT_OF]--> jon-snow`. `--neighbors jon-snow`: SWORN_TO → nights-watch, SWORN_TO → house-stark. No BORN_AT edge on jon-snow found in raw edges. | Wiki: "Jon Snow is the bastard son of Eddard Stark." Night's Watch confirmed. Birthplace: wiki lists "Born 283 AC" with no explicit location (Tower of Joy is reader inference; Jon himself doesn't know). The wiki's infobox has no "Born at" location field. | **partial** | `prose-only` (birthplace) — PARENT_OF Ned ✓, SWORN_TO Night's Watch ✓, but Jon has zero BORN_AT edges. The wiki itself omits a birth-location field (it's a theory/inference), so this is an acceptable gap given the source. However a consumer agent asking "where was Jon born?" gets no answer at all. |
| 9 | What set the Trident incident in motion? | `"incident at the Trident"` → **HIT** `incident-at-the-trident` | `--event-participants incident-at-the-trident` (4 beats, 16 role edges): Beats: `cersei-maneuvers-for-lady-s-death`, `ned-kills-lady`, `ned-claims-the-execution`, `death-of-mycah`. TRIGGERS edge: `cersei-maneuvers-for-lady-s-death` → `death-of-mycah`. AGENT_IN: eddard-stark, cersei-lannister, ilyn-payne, sandor-clegane. | `agot-eddard-03.md:47–113`: The actual trigger is Joffrey drawing his sword on Mycah/Arya at the Trident (prior chapter, agot-arya chapter missing from graph as a beat). The incident node captures the *aftermath* (Cersei's political maneuver, Ned killing Lady, Sandor killing Mycah) but not the precipitating *cause* (Joffrey attacking Arya/Mycah). No `joffrey-attacks-arya-at-trident` event node exists. | **partial** | `hub-pre-mint` — the hub `incident-at-the-trident` exists but covers only consequence beats. The precipitating Joffrey/Arya fight node is missing entirely. A consumer agent reading the beats sees consequences without cause. |
| 10 | What were the consequences of the Battle of the Trident? | `"Battle of the Trident"` → **HIT** `battle-of-the-trident` | `--neighbors battle-of-the-trident`: PART_OF → roberts-rebellion; LOCATED_AT → ruby-ford; COMMANDS_IN: robert-baratheon, rhaegar-targaryen, lewyn-martell; FIGHTS_IN: 8 fighters; VICTIM_IN: rhaegar-targaryen. No TRIGGERS, ENABLES, or causal edges pointing to consequences (sack-of-kings-landing, Robert's coronation, Tower of Joy, etc.). | Wiki Aftermath: Rhaegar's death opened King's Landing; Aerys sent Rhaella + Viserys to Dragonstone; Eddard raced the Lannisters to King's Landing; Tywin arrived first → Sack of King's Landing; Robert took the throne; Mace Tyrell yielded; Ned went to Tower of Joy. None of this chain is represented as causal edges. | **partial** | `dark-vocab` — no TRIGGERS or consequence chain edges from the battle hub. The graph records *who was there* and *who won* but not *what happened next*. The `decisive-rebel-victory` target slug in the node file is ORPHAN (no node file exists for it). |

---

## 3. Tally

- **Correct**: 4 / 10 (Q1, Q2, Q5, Q6)
- **Partial**: 6 / 10 (Q3, Q4, Q7, Q8, Q9, Q10)
- **Failed**: 0 / 10

---

## 4. Failure-Mode Taxonomy

| Mode | Count | Queries |
|------|-------|---------|
| `slug-discoverability` | 2 | Q3 (fuzzy miss on "Lyanna crowned queen of love and beauty"), Q4 (MISS on "weapon that killed Robb Stark") |
| `prose-only` | 2 | Q4 (weapon type only in evidence quote string), Q8 (Jon's birthplace not structured) |
| `dark-vocab` | 2 | Q7 (no ATTENDS/WITNESSES edges on execution), Q10 (no TRIGGERS/causal chain from battle hub) |
| `hub-pre-mint` | 1 | Q9 (no precipitating Joffrey/Arya fight beat node) |

Note: Q3 carries `slug-discoverability` (resolver doesn't route natural "who crowned Lyanna" phrasing to an event node or to Lyanna's node directly); the underlying data on `lyanna-stark` is excellent once reached via the character route. Q4 carries both `slug-discoverability` and `prose-only`.

---

## 5. What Works Well

- **Major event hubs are well-built and traversable.** The Red Wedding hub (12 beats, 44 role edges, 17 participants) is a showcase of the reification model. Querying it as a consumer agent with `--event-participants red-wedding` surfaces Tywin's ordering role, Walder Frey's orchestration, Roose Bolton's execution, and the individual kills — all with chapter quotes.
- **Named-weapon WIELDED_IN is correctly restrained.** `robb-is-killed` has no WIELDED_IN edge (unnamed longsword), while `execution-of-eddard-stark` has Ice correctly tagged. The schema rule is applied consistently.
- **Resolver is strong on exact-match natural phrases.** 7 out of 10 "first attempt" phrases hit cleanly (HIT or HIT-CHARACTER). Both forms of Q7 hit immediately. Q9 hit on "incident at the Trident."
- **Character relationship paths are rich.** Q6 (Tywin/Gregor): 4 direct typed edges + 10 2-hop bridges covering every dimension of the relationship. Q8 (Jon/Ned): 6 direct edges; PARENT_OF correctly points from Ned to Jon.
- **Historical tourney hub has real participant density.** Q5: 24 total edges (16 ATTENDS + 8 FIGHTS_IN) with verbatim chapter quotes.
- **Causal TRIGGERS edges exist at the beat level.** In Q9, `cersei-maneuvers-for-lady-s-death --[TRIGGERS]--> death-of-mycah` shows the pattern is available; it just needs to be applied more broadly.

---

## 6. Routing Recommendation

**Single highest-leverage next move: (d) new edge-type vocab — specifically WITNESSES/PRESENT_AT, and causal TRIGGERS propagated from event beats to external consequences.**

Justification by candidate:

**(a) Fix the alias resolver:** Low-yield now. The resolver hits 7/10 first-attempt natural phrases cold. The two MISS/fuzzy cases (Q3, Q4) are edge cases — Q3 misses because "who crowned Lyanna" routes to a concept node instead of lyanna-stark or a dedicated crowning-event node; Q4 misses because there is no "weapon" concept node to resolve to. These are solvable but fixing them doesn't unlock more data — the data is already there on the character node.

**(b) Historical structural-attachment:** Not the bottleneck. The tourney hub (Q5) already has 24 rich participant edges. The Battle of the Trident hub (Q10) has fighter + commander edges. The gap isn't participant attachment — it's *consequence* edges pointing forward in time.

**(c) Narrative-arc reification:** Not the bottleneck for THIS dip's failures. The Red Wedding arc reification (12 beats, 44 edges) works perfectly. The Q9 gap (missing Joffrey/Arya fight node) is a `hub-pre-mint` issue — one missing beat node, not a missing arc layer. The Q10 gap is causal-edge vocabulary, not arc structure. Narrative-arc reification (causal chain hubs *above* events) would help long-range traversal ("what caused Robert's rebellion?") but doesn't fix the immediate gaps found here.

**The dominant recurring gap is missing consequence edges.** Q7 has no attendance witnesses. Q10 has no outward causal edges from the battle. Q9's hub is missing its precipitating beat. All three are fixed by the same intervention: (1) add WITNESSES/PRESENT_AT (or expand ATTENDS) to capture who was present at key events, and (2) add TRIGGERS/ENABLES edges from event hubs to their historical consequences (battle → sack, battle → Tower of Joy, etc.).

**Is narrative-arc reification the bottleneck?** No. The two fully-failed arc-chain questions (Q9, Q10) fail due to missing causal vocabulary and a missing beat node, not due to missing arc-level parent hubs. The existing arc structure (Red Wedding hub) performs excellently. Adding a "Robert's-rebellion-arc" parent hub would not help a consumer agent find "what happened after the Battle of the Trident" — the gap is the TRIGGERS edges from `battle-of-the-trident` to `sack-of-kings-landing`, which requires vocabulary-level intervention, not another hub layer.

---

## 7. Bottom Line

The graph handles *who did what and to whom* extremely well — the Red Wedding, the tourney at Harrenhal, and character relationship traversals are graph-quality highlights. The resolver is reliable for 7/10 natural phrases cold. The primary weakness is **temporal-consequence vocabulary**: once an event is encoded, the graph records participants but doesn't structurally connect the event to its historical aftermath via causal edges (TRIGGERS, ENABLES, CAUSES). A secondary gap is **attendance/witness coverage** — execution and battle hubs encode agents and victims but not the named witnesses present on page. Addressing these two gaps (causal consequence edges + ATTENDS expansion to witnesses) would convert most of the 6 partials to correct results without touching the resolver or minting new arc-layer hubs.
