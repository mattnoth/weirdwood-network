# Lens B proposal — deception / revelation / whodunit / descriptive depth
# Session S151 | 2026-06-26
# Researcher: orchestrator (Sonnet 4.6)

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|-------------|----------------|------|
| B1 | wyman-manderly | DECEIVES | roose-bolton | T1 | adwd | adwd-the-prince-of-winterfell-01.md:153 | "Watch him. Watch how he watches Manderly. No dish so much as touches Roose's lips until he sees Lord Wyman eat of it first." | Roose suspects/watches but is deceived as to Wyman's true loyalty/plan; BASELINE has wyman DECEIVES house-frey and cersei-lannister but NOT roose-bolton |
| B2 | wyman-manderly | REVEALS_TO | davos-seaworth | T1 | adwd | adwd-davos-04.md:125 | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home." | The "no traitor" disclosure; full conspiracy revealed; no REVEALS_TO edge in baseline or wyman node |
| B3 | davos-seaworth | SEEKS | rickon-stark | T1 | adwd | adwd-davos-04.md:211 | "Smuggle me back my liege lord, and I will take Stannis Baratheon as my king." | Wyman's price to Davos = retrieve Rickon from Skagos; mission's instrument; no SEEKS davos→rickon in baseline |
| B4 | wyman-manderly | SEEKS | rickon-stark | T1 | adwd | adwd-davos-04.md:211 | "Roose Bolton has Lord Eddard's daughter. To thwart him White Harbor must have Ned's son … and the direwolf." | Wyman is the political actor driving the Rickon retrieval; Davos is the instrument; both edges needed |
| B5 | davos-seaworth | TRAVELS_TO | skagos | T1 | adwd | adwd-davos-04.md:213–224 | "But there were other places in this world where men were known to break their fast on human flesh." | Chapter ends with Wex's dagger pointing to Skagos on the map; Skagos named directly in davos-seaworth node prose (line 119 of node); no TRAVELS_TO davos→skagos in baseline |
| B6 | wyman-manderly | PARALLELS | rat-cook | T1 | adwd | adwd-the-prince-of-winterfell-01.md:175 | "We should have a song about the Rat Cook," he was muttering, as he staggered past Theon, leaning on his knights. | Wyman invokes the Rat Cook story *immediately after* serving the pies — the parallel is explicit in-text (baked-guest revenge); rat-cook node exists at texts/rat-cook.node.md; 0 incoming edges on rat-cook |
| B7 | wyman-manderly | CONSPIRES_WITH | robett-glover | T1 | adwd | adwd-davos-04.md:65 | "Robett Glover took up the tale." | Glover is present at the secret meeting, volunteers Wex's intelligence, co-proposes the Rickon mission; active co-conspirator, not just a neighbor; check baseline: wyman CONSPIRES_WITH stannis-baratheon exists, but not glover |
| B8 | barbrey-dustin | SUSPECTED_OF | wyman-manderly-great-northern-conspiracy | T2 | adwd | adwd-the-prince-of-winterfell-01.md:149 | "The fat man would like to kill us all, I do not doubt, but he does not have the belly for it, for all his girth." | Dustin is NOT in the conspiracy — she misreads Wyman as craven. The wiki node confirms she "fails to see through" his behavior. SUSPECTED_OF is wrong here; see note. DROPPING — this is a DISTRUSTS / misperception, not membership |
| B9 | wyman-manderly | VIOLATES_GUEST_RIGHT | ser-jared-frey | T1 | adwd | adwd-the-prince-of-winterfell-01.md:129–131 | "Ramsay hacked off slices with his falchion and Wyman Manderly himself served, presenting the first steaming portions to Roose Bolton and his fat Frey wife, the next to Ser Hosteen and Ser Aenys…" | Wyman has eaten the Freys (his guests) in pies and now serves them; direct mirror of the Rat Cook; Jared/Rhaegar/Symond Frey were Wyman's guests at White Harbor before disappearing on road to Winterfell (T1 via wiki; in-text, the three pies = three missing Freys). Note: verify Jared is the right slug; also applies to rhaegar-frey and symond-frey |
| B10 | wyman-manderly | VIOLATES_GUEST_RIGHT | rhaegar-frey | T1 | adwd | adwd-the-prince-of-winterfell-01.md:129–131 | (same feast scene — three pies, three missing Freys) | Parallel to B9; rhaegar-frey slug TBD |
| B11 | wyman-manderly | VIOLATES_GUEST_RIGHT | symond-frey | T1 | adwd | adwd-the-prince-of-winterfell-01.md:125 | "the arrogant Ser Jared and his nephew Rhaegar … Behind them both stands Symond, clinking coins." | Symond named as Wyman's White Harbor guest/spy; then disappears; baseline has wyman VIOLATES_GUEST_RIGHT davos-seaworth (the feigned arrest) and walder-frey VGR for Red Wedding victims — but NOT wyman→Freys for the pies. These are the strongest T1 irony edges in the arc. |

**Note on B8:** Barbrey Dustin's role is OBSERVER, not conspirator. She DISTRUSTS wyman-manderly (thinks him craven). The DISTRUSTS edge belongs in the graph but is already partially covered by barbrey-dustin DISTRUSTS house-frey (baseline). Propose: `barbrey-dustin DISTRUSTS wyman-manderly` T2 (she underestimates him). No SUSPECTED_OF here — wrong shape.

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|-------------|----------------|------|
| B8-revised | barbrey-dustin | DISTRUSTS | wyman-manderly | T2 | adwd | adwd-the-prince-of-winterfell-01.md:149 | "The fat man would like to kill us all, I do not doubt, but he does not have the belly for it, for all his girth. Under that sweaty flesh beats a heart as craven and cringing as … well … yours." | Dustin publicly dismisses Manderly as a coward — she's wrong; the irony is load-bearing; no existing DISTRUSTS barbrey→wyman in baseline |

---

## New nodes proposed

None required. All targets resolve to existing nodes:
- `rat-cook` → `graph/nodes/texts/rat-cook.node.md` ✓
- `skagos` → `graph/nodes/locations/skagos.node.md` ✓
- `rickon-stark` → `graph/nodes/characters/rickon-stark.node.md` ✓
- `davos-seaworth` → `graph/nodes/characters/davos-seaworth.node.md` ✓
- `robett-glover` — needs slug check (likely exists; Deepwood Motte lord, appears in baseline prep)

**Unresolved slugs:**
- `robett-glover` — probable but not verified via graph-query; synthesizer should confirm
- `ser-jared-frey`, `rhaegar-frey`, `symond-frey` — likely exist (Frey family tree coverage in Pass 2); synthesizer verify before minting B9–B11

---

## Quotes to home

These are load-bearing verbatim quotes for the target node's `## Quotes` section, NOT edges:

| target_slug | verbatim_quote | cite |
|-------------|----------------|------|
| wyman-manderly | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home." | adwd-davos-04.md:125 |
| wyman-manderly | "My son Wendel came to the Twins a guest. He ate Lord Walder's bread and salt, and hung his sword upon the wall to feast with friends. And they murdered him." | adwd-davos-04.md:125 |
| wyman-manderly | "The best pie you have ever tasted, my lords. Wash it down with Arbor gold and savor every bite. I know I shall." | adwd-the-prince-of-winterfell-01.md:129 |
| wyman-manderly | "I am too fat to sit a horse, as any man with eyes can plainly see. … My body has become a prison more dire than the Wolf's Den." | adwd-davos-04.md:171 |
| wyman-manderly | "The rancor I showed you in the Merman's Court was a mummer's farce put on to please our friends of Frey." | adwd-davos-04.md:105 |
| wyman-manderly | "It's not a king I need but a smuggler." | adwd-davos-04.md:179 |
| wyman-manderly | "We should have a song about the Rat Cook." | adwd-the-prince-of-winterfell-01.md:175 |
| rat-cook | (scene anchor) Wyman invokes the Rat Cook song immediately after serving the three pies at the wedding feast — the parallel is in-chapter, not wiki-derived | adwd-the-prince-of-winterfell-01.md:175 |
| barbrey-dustin | "The fat man would like to kill us all, I do not doubt, but he does not have the belly for it, for all his girth. Under that sweaty flesh beats a heart as craven and cringing as … well … yours." | adwd-the-prince-of-winterfell-01.md:149 |
| davos-seaworth | "But there were other places in this world where men were known to break their fast on human flesh." | adwd-davos-04.md:223 |

---

## NEW-TYPE-REQUEST

*(empty — all proposed edge types are in the 170-type vocabulary)*

---

## Dedup collisions skipped

- `wyman-manderly DECEIVES house-frey` — already in baseline (both baseline-intra.tsv and baseline-edges.tsv); NOT re-proposed
- `wyman-manderly DECEIVES cersei-lannister` — already in baseline; NOT re-proposed
- `wyman-manderly VIOLATES_GUEST_RIGHT davos-seaworth` — already in baseline-intra.tsv; NOT re-proposed
- `wyman-manderly CONSPIRES_WITH stannis-baratheon` — already in wyman-manderly.node.md OUTGOING; NOT re-proposed
- `roose-bolton DISTRUSTS wyman-manderly` — already in baseline-intra.tsv; NOT re-proposed (captured roose's awareness; B1 captures Wyman's deception of Roose, distinct direction)
