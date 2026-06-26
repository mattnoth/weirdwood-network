# B2 Robert Strong — Proposal
Session: S151 | Model: claude-sonnet-4-6 | Date: 2026-06-26

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|--------------|----------------|------|
| E01 | gregor-clegane | AFFLICTED_BY | manticore-venom | T1 | affc | affc-cersei-02.md:193 | "The poison on the Viper's spear was manticore venom from the east, I would stake my life on that." | Qyburn diagnosis; manticore-venom node exists + islanded |
| E02 | gregor-clegane | VICTIM_IN | creation-of-robert-strong | T1 | affc | affc-cersei-02.md:209 | "mayhaps I might move Ser Gregor to the dungeons? His screams will not disturb you there, and I will be able to tend to him more freely." | NEW event node; Gregor's dying body is the subject of Qyburn's work |
| E03 | qyburn | AGENT_IN | creation-of-robert-strong | T1 | affc | affc-cersei-02.md:219–221 | "The Mountain is yours. Do what you will with him, but confine your studies to the black cells." + "I wished to understand the nature of death, so I opened the bodies of the living." | Core causal agent; Citadel-expulsion quote confirms forbidden-arts basis |
| E04 | cersei-lannister | ENABLES | creation-of-robert-strong | T1 | affc | affc-cersei-02.md:219 | "The Mountain is yours. Do what you will with him, but confine your studies to the black cells. When he dies, bring me his head." | She gives Qyburn Gregor's body + free rein + funding (gold from Gyles) |
| E05 | cersei-lannister | COMMANDS_IN | creation-of-robert-strong | T1 | affc | affc-cersei-07.md:131 | "I have placed your order. The armorer thinks that I am mad. He assures me that no man is strong enough to move and fight in such a weight of plate." | Cersei commissions the armor — direct command act in the creation process |
| E06 | creation-of-robert-strong | ENABLES | cersei-resolves-on-trial-by-combat | T1 | affc / adwd | affc-cersei-10.md:307–309 | "My queen, your champion stands ready. There is no man in all the Seven Kingdoms who can hope to stand against him." | Qyburn tells imprisoned Cersei the champion is ready — the seam; cersei-resolves-on-trial-by-combat node confirmed |
| E07 | qyburn | PRACTICES | necromancy | T1 | affc | affc-cersei-02.md:217 | "I wished to understand the nature of death, so I opened the bodies of the living. For that crime the grey sheep shamed me and forced me into exile." | necromancy node exists + islanded; this is the explicit Citadel-expulsion justification |
| E08 | robert-strong | AGENT_IN | cersei-resolves-on-trial-by-combat | T2 | adwd | adwd-cersei-02.md:187 | "May I have the honor of presenting our newest member of the Kingsguard? This is Ser Robert Strong." | Robert Strong IS the champion Cersei is banking on; AGENT_IN the resolution event |
| E09 | robert-strong | MEMBER_OF | kingsguard | T1 | adwd | adwd-epilogue.md:103 | "His Grace named Ser Robert to the Kingsguard" | kingsguard node exists with 95 incoming edges; robert-strong already has SWORN_TO kingsguard (wiki-sourced); this is book-sourced T1 confirm |
| E10 | creation-of-robert-strong | PRECEDES | cersei-resolves-on-trial-by-combat | T1 | affc/adwd | affc-cersei-10.md:307 | "your champion stands ready" | Temporal: creation completes before Cersei resolves; redundant given E06 ENABLES — include ENABLES only, drop PRECEDES |
| E11 | robert-strong-theories | SUSPECTED_OF | — | — | — | — | — | SUSPECTED_OF requires an event target; this edge type doesn't apply to the theories node. See GATED-IDENTITY NOTE instead. Skip. |

**Final edge count (after dedup + drops): 9 new edges (E01–E09; E10 dropped as redundant with E06; E11 not valid)**

Dedup skips from baseline-intra.tsv:
- `oberyn-martell POISONS gregor-clegane` — EXISTS, skipped
- `cersei-lannister COMMANDS/CONSPIRES_WITH/TRUSTS qyburn` — ALL EXIST, skipped
- `cersei-lannister ENABLES qyburn` — EXISTS (generic); E04 here targets the new event node, not qyburn directly — valid new edge
- `robert-strong SWORN_TO kingsguard` — EXISTS (wiki-sourced); E09 is a separate book-sourced T1 confirmation edge with different evidence_kind

---

## New nodes proposed

### `creation-of-robert-strong`

```yaml
slug: creation-of-robert-strong
type: event.incident
aliases:
  - Qyburn's experiments on Gregor Clegane
  - the making of Robert Strong
  - Qyburn's work in the black cells
confidence: tier-1
containers: [cersei-downfall]
```

**Gloss:** Qyburn's clandestine experiments on the poisoned, dying body of Gregor Clegane in the black cells of the Red Keep, conducted with Cersei Lannister's sanction and funding, culminating in the appearance of the silent giant "Ser Robert Strong." The event spans AFFC (Cersei II, V, VII) through ADWD (Cersei II).

**Cite:** affc-cersei-02.md:209–221 (Gregor moved to dungeons, Qyburn given free rein); affc-cersei-07.md:121–131 (armor commissioned, Qyburn hints at the champion); affc-cersei-05.md:221 ("that foul thing screaming in the darkness"); adwd-cersei-02.md:181–191 (Robert Strong appears, named to Kingsguard).

---

## GATED-IDENTITY NOTE

**The books never confirm that Ser Robert Strong is the reanimated Gregor Clegane.** This is heavily implied but remains unconfirmed through the end of ADWD. The on-page evidence, presented conservatively:

1. **Timing:** Gregor Clegane is moved to Qyburn's dungeon "laboratory" while dying of manticore venom (AFFC Cersei II). His death is subsequently announced and a head is dispatched to Dorne — but the head is never shown on-page to be Gregor's (AFFC Cersei IV: "Ser Gregor perished of his wounds").
2. **Size:** Robert Strong is "eight feet tall or maybe taller, with legs as thick around as trees, he had a chest worthy of a plow horse" (ADWD Cersei II:181). Gregor Clegane was described throughout as an 8-foot giant.
3. **Silence and vow:** "Ser Robert has taken a holy vow of silence" — Qyburn's framing; Meryn Trant reports he "took neither food nor drink," Boros Blount says he had never seen the man use the privy (ADWD Epilogue:101).
4. **Never removes armor / face never seen:** "He does not speak, he will not show his face, he is never seen without his armor" (ADWD Epilogue:99).
5. **Kevan's inference:** "We do not even know if he's alive… Dead men do not shit. Kevan Lannister had a strong suspicion of just who this Ser Robert really was beneath that gleaming white armor." (ADWD Epilogue:101) — the text validates the reader inference without confirming it.
6. **Qyburn's background:** Explicitly expelled from the Citadel for "opening the bodies of the living" to "understand the nature of death" — necromancy/vivisection (AFFC Cersei II:217).

**Do NOT mint:** `robert-strong SAME_AS gregor-clegane`, `qyburn RESURRECTS gregor-clegane`, or `gregor-clegane TRANSFORMS_INTO robert-strong`. The `creation-of-robert-strong` event node + `gregor-clegane VICTIM_IN creation-of-robert-strong` + `robert-strong AGENT_IN cersei-resolves-on-trial-by-combat` encodes the structural relationship without asserting the identity. The `robert-strong-theories` node (currently islanded) can receive: `robert-strong-theories FORESHADOWS cersei-resolves-on-trial-by-combat` or similar — but that requires synthesis-level decision.

---

## NEW-TYPE-REQUEST

None. All edges above use live vocabulary types.

---

## Unresolved slugs

- `manticore-venom` — node EXISTS (`graph/nodes/medical/manticore-venom.node.md`), currently islanded (0 edges). E01 wires it for the first time.
- `necromancy` — node EXISTS (`graph/nodes/concepts/necromancy.node.md`), currently islanded. E07 wires it; the node's own prose already states Qyburn was expelled for necromancy experiments (cross-check: consistent).
- `robert-strong-theories` — node EXISTS, islanded. Not wired here (no safe non-gated edge available without synthesis decision).
- `citadel` — node exists; Qyburn's expulsion from the Citadel is the backstory for E07 but the `qyburn PRACTICES necromancy` edge + the Citadel-expulsion quote sufficiently encode the story without a separate `qyburn BANISHES citadel` edge (direction would be wrong anyway — Citadel expelled Qyburn, not vice versa). FLAG for synthesis: a `citadel BANISHES qyburn` edge (if BANISHES applies to institutions) would be high-value but needs type-check.

---

## Notes for synthesis

- E06 (`creation-of-robert-strong ENABLES cersei-resolves-on-trial-by-combat`) is the key sub-plot seam. Without it, the two sub-graphs are unconnected.
- E07 (`qyburn PRACTICES necromancy`) wires two islanded nodes and directly grounds Qyburn's motivation/capability.
- E01 (`gregor-clegane AFFLICTED_BY manticore-venom`) wires a third islanded node and connects the ASOS combat to the AFFC creation event chain.
- The `cersei-lannister COMMANDS_IN creation-of-robert-strong` vs. `ENABLES creation-of-robert-strong` question: both E04 (ENABLES — she gives Qyburn the body) and E05 (COMMANDS_IN — she orders the armor) are valid; they capture different causal moments. Synthesis may prefer to keep only the higher-value one (E04 ENABLES) and drop E05 as redundant — flagging here.
