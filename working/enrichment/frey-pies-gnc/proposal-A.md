# Proposal A — GNC Causal Spine + Structure
Session 151, Lens A (causal spine / hub / Wylis thread)
Date: 2026-06-26

---

## New nodes proposed

### 1. `grand-northern-conspiracy`
- **type:** `event.conspiracy`
- **aliases:** ["Grand Northern Conspiracy", "the northern conspiracy", "the mummer's farce", "North remembers plot"]
- **gloss:** The secret pact among northern lords (led by Wyman Manderly, with Robett Glover) to publicly submit to Bolton/Frey rule while covertly working to restore the Starks — recovering Rickon Stark from Skagos, secretly supporting Stannis, and eliminating Frey representatives.
- **primary book cite:** `sources/chapters/adwd/adwd-davos-04.md:125` — "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done."
- **note:** No node exists for this. `frey-pies-theories` is a zero-edge orphan wiki-theory node; this is a distinct canonical PLOT event, not a theory, and should be a separate hub node. `wyman-manderly` already has `CONSPIRES_WITH stannis-baratheon` (a dyad edge from the fake-execution node); the hub collects the *full conspiracy* breadth.

### 2. `manderly-bakes-the-frey-pies`
- **type:** `event.incident`
- **aliases:** ["the Frey pies", "the pork pies at the Winterfell wedding", "Manderly serves the pies", "the wedding pies"]
- **gloss:** At the Ramsay Bolton–Arya Stark wedding feast at Winterfell, Wyman Manderly personally serves three enormous pork pies — widely understood to contain Rhaegar, Jared, and Symond Frey, who disappeared en route — and then calls for a singer to play "The Rat Cook."
- **primary book cite:** `sources/chapters/adwd/adwd-the-prince-of-winterfell-01.md:129` — "three great wedding pies, as wide across as wagon wheels … chunks of seasoned pork swimming in a savory brown gravy … 'The best pie you have ever tasted, my lords.'"
- **note:** Confirmed absent from graph. The three Frey slugs exist (`rhaegar-frey`, `jared-frey`, `symond-frey`); `rat-cook` exists as `object.text`.

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|--------------|----------------|------|
| A1 | wyman-manderly-stages-fake-execution-of-davos | SUB_BEAT_OF | grand-northern-conspiracy | T1 | adwd | adwd-davos-04.md:125 | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done." | Fake execution is the deception step of the GNC. Dedup: no existing SUB_BEAT_OF from this event to any hub — confirmed. |
| A2 | learning-about-manderly-s-hostage | SUB_BEAT_OF | grand-northern-conspiracy | T2 | adwd | adwd-davos-04.md:111 | "I did not dare defy King's Landing so long as my last living son remained a captive." | The hostage-constraint event is a precondition beat of the GNC (explains why conspiracy had to be secret). Node has 0 outgoing edges — confirmed. |
| A3 | wyman-manderly | AGENT_IN | grand-northern-conspiracy | T1 | adwd | adwd-davos-04.md:125 | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home." | Wyman is the architect. Dedup: wyman already has CONSPIRES_WITH stannis-baratheon and AGENT_IN davos-seaworth-captured — no AGENT_IN grand-northern-conspiracy exists. |
| A4 | davos-seaworth | AGENT_IN | grand-northern-conspiracy | T1 | adwd | adwd-davos-04.md:211 | "That is my price, Lord Davos. Smuggle me back my liege lord, and I will take Stannis Baratheon as my king." | Davos is recruited as the operative. Dedup: davos has AGENT_IN on earlier beats (davos-seaworth-captured etc.) but not on the conspiracy hub. |
| A5 | robett-glover | AGENT_IN | grand-northern-conspiracy | T1 | adwd | adwd-davos-04.md:61–65 | "Robett Glover, if it please, my lord … Moat Cailin has fallen … I must have a man who's sailed in darker waters." | Glover is the second co-conspirator in the secret chamber; he speaks for northern lords. Note: verify slug `robett-glover` exists before minting — if not, flag for Lens B. |
| A6 | grand-northern-conspiracy | ENABLES | stannis-march-on-winterfell | T2 | adwd | adwd-davos-04.md:175 | "I can deliver King Stannis the allegiance of all the lands east of the White Knife … All this I pledge to do if you will meet my price." | Manderly's secret heavy-horse pledge + Oldcastle/Widow's Watch alignment is what makes Stannis's northern campaign viable. Causal direction: GNC→march. Dedup: stannis-march-on-winterfell has 4 incoming edges; none from wyman/gnc — confirmed clean. |
| A7 | manderly-bakes-the-frey-pies | SUB_BEAT_OF | grand-northern-conspiracy | T2 | adwd | adwd-a-ghost-in-winterfell-01.md:89 | "The road has many dangers, ser. I gave your brothers guest gifts when we took our leave of White Harbor." | The pie incident is the vengeance/execution step of the GNC. Direction: small-beat → parent. |
| A8 | wyman-manderly | AGENT_IN | manderly-bakes-the-frey-pies | T1 | adwd | adwd-the-prince-of-winterfell-01.md:129 | "Wyman Manderly himself served, presenting the first steaming portions to Roose Bolton and his fat Frey wife … 'The best pie you have ever tasted, my lords.'" | Wyman personally serves. Dedup: wyman has no existing AGENT_IN manderly-bakes-the-frey-pies (node is new). |
| A9 | rhaegar-frey | VICTIM_IN | manderly-bakes-the-frey-pies | T2 | adwd | adwd-a-ghost-in-winterfell-01.md:89 | "Rhaegar of the round shoulders, with his glib tongue … They brought home Wendel's bones. The road has many dangers, ser." | Strong implication: Hosteen demands to know where they are; Wyman's answer is the "road has many dangers" brush-off after the pies appeared. Gated: treat as T2 strong-implication, not T1. Dedup: rhaegar-frey has 0 victim edges. |
| A10 | jared-frey | VICTIM_IN | manderly-bakes-the-frey-pies | T2 | adwd | adwd-a-ghost-in-winterfell-01.md:89 | "Bold Ser Jared, so swift to draw his steel … The road has many dangers, ser." | Same sourcing as A9. Dedup: jared-frey has 0 victim edges. |
| A11 | symond-frey | VICTIM_IN | manderly-bakes-the-frey-pies | T2 | adwd | adwd-a-ghost-in-winterfell-01.md:89 | "Symond the spymaster, always clinking coins … The road has many dangers, ser." | Same sourcing as A9. Dedup: symond-frey has 0 victim edges. |
| A12 | manderly-bakes-the-frey-pies | ECHOES | rat-cook | T1 | adwd | adwd-the-prince-of-winterfell-01.md:175 | "We should have a song about the Rat Cook … Singer, give us a song about the Rat Cook." | Wyman literally calls for the Rat Cook song immediately after serving the pies — the parallel is stated in text, not inferred. `rat-cook` exists as object.text. Direction: incident→text (ECHOES). |
| A13 | learning-about-manderly-s-hostage | MOTIVATES | wyman-manderly | T1 | adwd | adwd-davos-04.md:111 | "I did not dare defy King's Landing so long as my last living son remained a captive." | The hostage constraint is what forced Wyman's public submission; its resolution (Wylis home) enables the GNC to activate. Direction: event→person (MOTIVATES targets the motivated actor per convention). Dedup: learning-about-manderly-s-hostage has 0 outgoing edges — confirmed clean. |
| A14 | wylis-manderly | PRISONER_OF | iron-throne | T1 | adwd | adwd-davos-03.md:109 | "The Lady Leona is wife to Lord Wyman's son Ser Wylis, presently a captive of the Lannisters." | Wylis is the Lannister/Iron-Throne hostage that backs the constraint. `iron-throne` is likely an existing node. Dedup: wylis-manderly has VICTIM_IN learning-about-manderly-s-hostage already (baseline-intra.tsv line 48) — PRISONER_OF is a different edge type and a separate fact. |
| A15 | frey-pies-theories | SUBJECT_OF_PROPHECY | manderly-bakes-the-frey-pies | T2 | adwd | — | — | SKIP — rethought: frey-pies-theories is a fan-theory wiki node, not a prophecy. Better linkage is for synthesis step to decide how to bridge the orphan node. Do NOT propose this edge. |

**Retraction of A15:** After reflection, `SUBJECT_OF_PROPHECY` is the wrong edge type — frey-pies-theories is a speculative/theory node, not a prophecy subject. The right wire is probably `frey-pies-theories CITED_BY manderly-bakes-the-frey-pies` or `PART_OF` in reverse, but that requires Lens B / synthesis to adjudicate. Leaving A15 out of the final count.

**Final edge count: 14 proposed edges (A1–A14).**

---

## Dedup collisions skipped

- `wyman-manderly CONSPIRES_WITH stannis-baratheon` already exists (confirmed via --neighbors). Did NOT re-propose it.
- `wyman-manderly AGENT_IN davos-seaworth-captured` already exists. Did NOT re-propose.
- `wylis-manderly VICTIM_IN learning-about-manderly-s-hostage` already in baseline-intra.tsv. Did NOT re-propose.
- `iron-throne AGENT_IN learning-about-manderly-s-hostage` already in baseline (the hostage beat incoming). A14 adds `wylis-manderly PRISONER_OF iron-throne` which is a different relation.

---

## Node slugs not resolved

- `robett-glover` (A5) — used in the secret chamber scene but slug not verified in graph. If absent, Lens B or synthesis should propose it as a new node before A5 can mint.
- `iron-throne` (A14) — referenced in baseline as AGENT_IN the hostage node; almost certainly an existing node, but not explicitly verified via --neighbors.

---

## NEW-TYPE-REQUEST

*(none — all proposed edges use types from the locked 170-word vocabulary)*

---

## Harvest queue entries

See rows appended to `working/harvest-queue.md` below.

```
| open | food | adwd | adwd-the-prince-of-winterfell-01.md:129 | Feast menu at Ramsay's wedding: cod cakes, winter squash, neeps, wheel cheese, mutton slabs, beef ribs, three pork pies — all furnished by Manderly. "hills of neeps and great round wheels of cheese, on smoking slabs of mutton and beef ribs charred almost black" | S151 frey-pies |
| open | food | adwd | adwd-the-prince-of-winterfell-01.md:129 | Drinks at feast: black stout, yellow beer, red/gold/purple wines, Arbor gold — "brought up from the warm south on fat-bottomed ships and aged in his deep cellars" | S151 frey-pies |
| open | food | adwd | adwd-the-prince-of-winterfell-01.md:131 | Manderly eats six portions of the pies (two from each), "smacking his lips and slapping his belly" — grotesque hospitality/gluttony inversion | S151 frey-pies |
| open | food | adwd | adwd-davos-04.md:93 | Wylis's welcome-home feast: "lamprey pie and venison with roasted chestnuts" in the Merman's Court | S151 frey-pies |
| open | hospitality | adwd | adwd-a-ghost-in-winterfell-01.md:89 | Wyman's "guest gifts" line — palfreys to Freys on departure from White Harbor as cover for disappearance; sinister hospitality inversion | S151 frey-pies |
| open | quote | adwd | adwd-the-prince-of-winterfell-01.md:175 | "We should have a song about the Rat Cook … Singer, give us a song about the Rat Cook." — Manderly muttering drunkenly as carried from hall; load-bearing canonical tie between pies and the legend | S151 frey-pies |
| open | quote | adwd | adwd-davos-04.md:125 | "My son Wendel came to the Twins a guest. He ate Lord Walder's bread and salt, and hung his sword upon the wall to feast with friends. And they murdered him." — Wyman's grief speech; guest-right violation framing | S151 frey-pies |
| open | foreshadowing | adwd | adwd-the-prince-of-winterfell-01.md:149 | Lady Dustin: "He does not have the belly for it, for all his girth." — dramatic irony: she misreads Wyman completely | S151 frey-pies |
| open | foreshadowing | adwd | adwd-the-prince-of-winterfell-01.md:153 | Dustin on Roose: "No dish so much as touches Roose's lips until he sees Lord Wyman eat of it first." — Roose suspects treachery in the pies but can't prove it | S151 frey-pies |
| open | appearance | adwd | adwd-the-prince-of-winterfell-01.md:129 | Ramsay "hacked off slices with his falchion" — physicality of the pie-cutting scene | S151 frey-pies |
```
