# Lens B — Assassination Conspiracy + Whodunit + Revelation Events
## Jon Snow / the Wall enrichment dip (S145)

> PROPOSE ONLY. Do not mint, do not write to graph.
> Dedup checks run against `graph/nodes/` (find) and `graph/edges/edges.jsonl` (grep).

---

## THREAD 1 — The Bowen-Marsh Assassination Conspiracy (the Shieldhall + the Whodunit)

### NODE PROPOSALS

---

**Slug:** `the-shieldhall-speech`
**Type:** event
**Natural SPACED aliases:** "Shieldhall speech", "Jon's Shieldhall address", "Jon reads the Pink Letter", "march on Winterfell announcement"
**Gloss:** Jon Snow assembles the leading men of Castle Black and the free folk in the Shieldhall, reads aloud the Pink Letter from Ramsay Bolton, announces he will ride south to Winterfell alone, and calls for volunteers to stand with him — a unilateral breach of the Night's Watch oath that becomes the immediate trigger the conspirators react to.
**Dedup status:** MISSING — `find graph/nodes -name "the-shieldhall-speech.node.md"` returns nothing. `shieldhall` (location) EXISTS and is the correct venue node; `the-shieldhall-speech` (event) does not exist.
**Rationale:** The baseline explicitly flags this as the missing causal beat. The current wire is `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly` — it collapses the intermediate speech. The speech is where Jon's decision crystallizes and becomes public; it is what the conspirators react to, not the letter itself. Without this node the causal chain skips the most important step: Marsh and Yarwyck visibly leave the hall as Jon finishes speaking (jon-13:299), confirming the speech is their decision point.

---

### EDGE PROPOSALS — Shieldhall rewire

**E-B1** Causal rewire (step 1 of 2):
`pink-letter-delivered --ENABLES--> the-shieldhall-speech`
- Tier: 1
- Verbatim quote: "No. I ride south." Then Jon read them the letter Ramsay Snow had written.
- cite_ref: adwd-jon-13.md:287
- Dedup status: NEW — no existing `pink-letter-delivered ENABLES/TRIGGERS the-shieldhall-speech` edge in edges.jsonl.
- Rationale: `ENABLES` not `TRIGGERS` because the Pink Letter is the precipitating document but not the immediate spark — Jon could have read the letter privately and done nothing public. He *chooses* to read it aloud in the Shieldhall. The letter makes the speech possible; the speech is its own act.

**E-B2** Causal rewire (step 2 of 2):
`the-shieldhall-speech --TRIGGERS--> jon-is-stabbed-repeatedly`
- Tier: 1
- Verbatim quote: "Yarwyck and Marsh were slipping out, he saw, and all their men behind them. It made no matter. He did not need them now."
- cite_ref: adwd-jon-13.md:299
- Dedup status: NEW. Replaces the collapsed `pink-letter-delivered TRIGGERS jon-is-stabbed-repeatedly` wire (existing edge). The existing edge should be preserved but supplemented with this intermediate node so the chain reads: `pink-letter-delivered ENABLES the-shieldhall-speech TRIGGERS jon-is-stabbed-repeatedly`. Do NOT delete the existing direct edge without curator sign-off; propose the add-on only.
- Rationale: The conspirators' exit is the moment of decision — Marsh leaves as Jon calls for volunteers. This is `TRIGGERS` not `ENABLES` because the speech is the proximate stimulus: the Shieldhall address makes Jon's vow-breaking public and irreversible in the conspirators' eyes.

**E-B3** Spatial:
`the-shieldhall-speech --LOCATED_AT--> shieldhall`
- Tier: 1
- Verbatim quote: "When Jon and Tormund entered, a sound went through the hall, like wasps stirring in a nest."
- cite_ref: adwd-jon-13.md:279
- Dedup status: NEW.

**E-B4** Jon calls the assembly:
`jon-snow --AGENT_IN--> the-shieldhall-speech`
- Tier: 1
- Verbatim quote: "Spread the word. I want all the leading men in the Shieldhall when the evening watch begins."
- cite_ref: adwd-jon-13.md:113
- Dedup status: NEW.

---

### EDGE PROPOSALS — Conspirators / SUSPECTED_OF layer

The Shieldhall seating is explicit (adwd-jon-13:283): "To his left he saw Marsh and Yarwyck. Othell was surrounded by his builders, whilst Bowen had Wick Whittlestick, Left Hand Lew, and Alf of Runnymudd beside him."

After the speech, Marsh and Yarwyck leave together (jon-13:299). The stabbing follows shortly after outside Hardin's Tower (jon-13:317–325). The text shows Wick slashing first (throat), then Marsh stabbing the belly. A third dagger hits Jon between the shoulder blades; a fourth knife is unspecified. The text never names a third or fourth assailant explicitly.

**E-B5** Left Hand Lew — SUSPECTED_OF:
`left-hand-lew --SUSPECTED_OF--> jon-is-stabbed-repeatedly`
- Tier: 2
- Verbatim quote (proximity only, not act): "Bowen had Wick Whittlestick, Left Hand Lew, and Alf of Runnymudd beside him."
- cite_ref: adwd-jon-13.md:283
- Dedup status: NEW. Node `left-hand-lew` EXISTS.
- Rationale for SUSPECTED_OF (not AGENT_IN): Left Hand Lew is seated with Bowen Marsh's faction at the Shieldhall speech — he is unambiguously in the inner circle of the conspirators (Bowen's immediate company). However, the text names only Wick and Bowen as the attackers who actually stab Jon. The third dagger is described from Jon's POV as simply "the third dagger" with no named wielder. Assigning AGENT_IN to Lew would go beyond the text. SUSPECTED_OF = Tier-2, unproven participation, load-bearing because the faction seating is explicit and the stabbing had multiple knives.

**E-B6** Alf of Runnymudd — SUSPECTED_OF:
`alf-of-runnymudd --SUSPECTED_OF--> jon-is-stabbed-repeatedly`
- Tier: 2
- Verbatim quote (same): "Bowen had Wick Whittlestick, Left Hand Lew, and Alf of Runnymudd beside him."
- cite_ref: adwd-jon-13.md:283
- Dedup status: NEW. Node `alf-of-runnymudd` EXISTS.
- Rationale: Same as E-B5. Alf is in Bowen's Shieldhall cluster; no text confirms he strikes Jon. SUSPECTED_OF Tier-2.

**E-B7** Othell Yarwyck — SUSPECTED_OF:
`othell-yarwyck --SUSPECTED_OF--> jon-is-stabbed-repeatedly`
- Tier: 2
- Verbatim quote: "Yarwyck and Marsh were slipping out, he saw, and all their men behind them."
- cite_ref: adwd-jon-13.md:299
- Dedup status: NEW. Node `othell-yarwyck` EXISTS. Note: an existing `MOTIVATES bowen-marsh` chain covers the grievance substrate but no Yarwyck-specific conspiracy edge exists in edges.jsonl.
- Rationale: Yarwyck leaves with Marsh in lockstep at the precise moment of the conspirators' decision. He has been Marsh's closest partner in opposing Jon throughout ADWD (jon-13:139–165, jon-11 throughout). The wiki and the text strongly imply complicity — but no text shows Yarwyck handling a knife. SUSPECTED_OF Tier-2 is the correct read: he is not proven to have stabbed Jon and may have simply walked away before the violence; his departure is consistent with foreknowledge and cowardice rather than active participation. Do NOT assign AGENT_IN without further textual evidence.

**E-B8** Yarwyck MOTIVATES grievance (free folk):
`jon-allows-free-folk-through-the-wall --MOTIVATES--> othell-yarwyck`
- Tier: 2
- Verbatim quote: "When Jon settled Stonedoor on Soren Shieldbreaker, Yarwyck complained that it was too isolated … As for Borroq, Othell Yarwyck claimed the woods north of Stonedoor were full of wild boars."
- cite_ref: adwd-jon-13.md:149
- Dedup status: CHECK — the existing MOTIVATES edge targets `bowen-marsh` not `othell-yarwyck`; a Yarwyck-specific MOTIVATES is new.
- Rationale: Yarwyck's objections to every free-folk decision mirror Marsh's exactly (jon-13:149–163). The same causal logic that links the free-folk decree to Marsh's grievance applies to Yarwyck. This mirrors the existing E-22423 edge structure.

---

## THREAD 2 — The Mance / "Rattleshirt" Glamour Deception

### NODE SITUATION

**CRITICAL DEDUP FINDING:** There is NO separate `rattleshirt` node. The `lord-of-bones` node EXISTS at `graph/nodes/characters/lord-of-bones.node.md` and already carries aliases: `["Rattleshirt", "Lord o' Bones", "Bag o' Bones", "Bag of Bones", "Mance Rayder"]`.

The alias `"Mance Rayder"` in the `lord-of-bones` node is a PROBLEM: it conflates two separate people. The `lord-of-bones` node correctly represents Rattleshirt (the real person burned at the stake). `mance-rayder` is a SEPARATE existing node. The inclusion of "Mance Rayder" as an alias on `lord-of-bones` reflects the glamour confusion — the burned man appeared to be Mance — but this alias should be a DISGUISED_AS edge, not a name-alias.

**No new NODE needed** for Rattleshirt — `lord-of-bones` IS Rattleshirt. However, the alias situation is worth a curator note.

### EDGE PROPOSALS — Glamour / IMPERSONATES

**E-B9** The glamour (direction: who impersonates whom):
`mance-rayder --IMPERSONATES--> lord-of-bones`
- Tier: 1
- Verbatim quote: "She burned the Lord of Bones." / "Jon Snow's grey eyes grew wider. 'Mance?' / 'Lord Snow.' Mance Rayder did not smile."
- cite_ref: adwd-melisandre-01.md:259–255
- Dedup status: NEW. `IMPERSONATES` is in the locked vocabulary (Identity & Disguise, currently unpopulated). No existing IMPERSONATES edge in edges.jsonl for these slugs.
- Rationale: Mance Rayder actively performs as Rattleshirt/Lord of Bones — wears the bone armor, adopts his presence at Castle Black, allows himself to be identified as Rattleshirt. Direction: `mance-rayder IMPERSONATES lord-of-bones` (the actor → the role). The schema precedent for direction is the impersonator as source.

**E-B10** Melisandre AGENT_IN the glamour event:
`melisandre --AGENT_IN--> mance-rayder-brought-to-execution`
- Tier: 1
- Verbatim quote: "Melisandre touched the ruby at her neck and spoke a word. … The bones remained … But the widow's peak dissolved."
- cite_ref: adwd-melisandre-01.md:245–251
- Dedup status: CHECK — `mance-rayder-brought-to-execution` EXISTS (in baseline). Check existing edges for Melisandre AGENT_IN that event. If none exists, this is new. She is the architect of the substitution; she speaks the word that dispels the glamour.
- Note: The glamour was placed BEFORE the execution — Melisandre glamoured Rattleshirt to appear as Mance, and glamoured Mance to appear as Rattleshirt. The reveal in adwd-melisandre-01 is the dispelling, but the casting predates the chapter.

**E-B11** The ruby as instrument — Melisandre controls Lord of Bones:
`melisandre --MANIPULATES--> lord-of-bones`
- Tier: 1
- Verbatim quote: "In the black iron fetter about his wrist, the ruby seemed to pulse. … 'I feel it when I sleep. Warm against my skin, even through the iron. Soft as a woman's kiss. Your kiss.'"
- cite_ref: adwd-melisandre-01.md:97
- Dedup status: CHECK edges.jsonl for existing melisandre MANIPULATES lord-of-bones — likely new. `MANIPULATES` is a populated type (3 instances).
- Rationale: Melisandre controls Rattleshirt (Lord of Bones) via the ruby fetter. This is active coercive control, not just knowing his plans. `MANIPULATES` fits; `DECEIVES` would apply to the world (she deceives the Watch), but her relationship to Rattleshirt is coercive control.

**E-B12** The execution — who actually burns:
`lord-of-bones --VICTIM_IN--> mance-rayder-brought-to-execution`
- Tier: 1
- Verbatim quote: "She burned the Lord of Bones."
- cite_ref: adwd-melisandre-01.md:259
- Dedup status: CHECK — the existing `mance-rayder-brought-to-execution` event likely has `mance-rayder VICTIM_IN` (he appeared to be the victim). `lord-of-bones VICTIM_IN` would be the corrective Tier-1 edge (the actual victim). Both should coexist; the Mance-as-VICTIM edge may be Tier-2 (appearance, not reality) and needs a curator note on the existing edge's confidence.

**E-B13** The burned man's last words (load-bearing quote):
Additional evidence_quote for E-B12:
> "No, mercy. This is not right, I'm not the king, they—"
> — Lord of Bones as "Mance Rayder" upon seeing Melisandre's cage
(from `lord-of-bones.node.md` Quotes section, sourced adwd-10)

This verbatim quote is already captured in the `lord-of-bones` node Quotes section. Attach to E-B12 as corroborating evidence. No separate edge needed.

**E-B14** Curator note (alias hygiene, not an edge proposal):
The alias `"Mance Rayder"` on `lord-of-bones.node.md` should be replaced with a `DISGUISED_AS` edge: `lord-of-bones --DISGUISED_AS--> mance-rayder` (Tier-1, adwd). The current alias creates a resolver collision — querying "Mance Rayder" could land on the Lord of Bones node. FLAG for curator action; do not auto-fix.

---

## THREAD 3 — Hardhome as a Revelation-Event

### NODE PROPOSALS

**Slug:** `hardhome-catastrophe`
**Type:** event
**Natural SPACED aliases:** "Hardhome disaster", "fall of Hardhome", "dead things in the water", "Cotter Pyke's letter from Hardhome", "Hardhome rescue failure"
**Gloss:** Cotter Pyke's fleet reaches Hardhome to rescue thousands of wildling refugees; a catastrophe unfolds — ships lost, wights in the water and woods, wildlings eating their own dead, rescue attempts violently repelled. The Hardhome letter reporting this disaster reaches Jon Snow at Castle Black, becomes a revelation-beat that confirms the Others are already moving and drives the urgency of Jon's wildling-integration decisions.
**Dedup status:** MISSING as an event. `hardhome` (location) EXISTS. No event node for the disaster exists. Check: `find graph/nodes -name "hardhome-catastrophe.node.md"` returns nothing.
**Rationale:** The Hardhome letter is the in-text confirmation of the supernatural threat that underpins Jon's entire arc — "Dead things in the woods. Dead things in the water." (adwd-jon-12:263). It is what transforms Jon's policy decisions from pragmatic to existential. Without this event node, the MOTIVATES chain from Hardhome into Jon's wildling-integration decree (and thus back to the conspiracy) is invisible.

**Note on scope:** The novel event at Hardhome (the battle/massacre) occurs off-page in ADWD — it is known only through the letter. The letter is a revelation-event from Jon's POV. The actual Hardhome battle is shown in the AGOT/TV material but NOT in the novels yet. The node should represent the **revelation** (the letter arriving), not the battle itself (which is unnarrated in ADWD).

---

### EDGE PROPOSALS — Hardhome revelation

**E-B15** The revelation-event:
`hardhome-catastrophe --TRIGGERS--> jon-allows-free-folk-through-the-wall`
- Tier: 2 — causal sequence is real but indirect (the disaster is one of several motivating factors; Jon had already been moving toward the free-folk integration; the letter accelerates and confirms)
- Actually: on reflection the direction is inverted — Jon had ALREADY brought Tormund's people through by adwd-jon-12. The Hardhome letter ARRIVES AFTER the free-folk decree. Corrected proposal:

`hardhome-catastrophe --MOTIVATES--> jon-snow`
- Tier: 2
- Verbatim quote: "Dead things in the woods. Dead things in the water. Jon Snow rolled up the parchment, frowning. Night falls, he thought, and now my war begins."
- cite_ref: adwd-jon-12.md:271
- Dedup status: NEW. No existing `hardhome-catastrophe MOTIVATES jon-snow` edge (event node is new).
- Rationale: `MOTIVATES` routes agency through Jon as the person who acts on the revelation. The letter confirms his existential reasoning for the Shieldhall address — specifically, when he says "we have had reports of dead things in the wood" at the Shieldhall (jon-13:283). It is the evidence behind the march-on-Hardhome plan that becomes the Shieldhall address. Causal chain: `hardhome-catastrophe MOTIVATES jon-snow` → `jon-snow AGENT_IN the-shieldhall-speech`.

**E-B16** Location tag:
`hardhome-catastrophe --LOCATED_AT--> hardhome`
- Tier: 1
- cite_ref: adwd-jon-12.md:263 (letter header: "At Hardhome, with six ships.")
- Dedup status: NEW.

**E-B17** The letter as evidence-event connecting Hardhome to the Shieldhall:
`hardhome-catastrophe --ENABLES--> the-shieldhall-speech`
- Tier: 2
- Verbatim quote: "I summoned you to make plans for the relief of Hardhome … Thousands of the free folk are gathered there, trapped and starving, and we have had reports of dead things in the wood."
- cite_ref: adwd-jon-13.md:283
- Dedup status: NEW.
- Rationale: The Hardhome catastrophe is the stated reason for the Shieldhall assembly. Without the Hardhome disaster Jon would not have changed the ranging plan; without the Pink Letter he would have gone himself. Together these two events force the Shieldhall speech: `hardhome-catastrophe ENABLES the-shieldhall-speech` + `pink-letter-delivered ENABLES the-shieldhall-speech`.

**E-B18** Cotter Pyke's role:
`cotter-pyke --AGENT_IN--> hardhome-catastrophe`
- Tier: 1
- Verbatim quote: "Cotter Pyke had made his angry mark below." (the letter's author)
- cite_ref: adwd-jon-12.md:267
- Dedup status: CHECK `cotter-pyke` node existence. If node exists, edge is new.

---

## COMPLETE CAUSAL CHAIN SUMMARY (proposed graph after minting)

```
hardhome-catastrophe ──ENABLES──> the-shieldhall-speech
pink-letter-delivered ──ENABLES──> the-shieldhall-speech
the-shieldhall-speech ──TRIGGERS──> jon-is-stabbed-repeatedly

hardhome-catastrophe ──MOTIVATES──> jon-snow ──AGENT_IN──> the-shieldhall-speech

[EXISTING, do not re-propose:]
pink-letter-delivered ──TRIGGERS──> jon-is-stabbed-repeatedly  (keep; now a shortcut through the new intermediate)
jon-allows-free-folk-through-the-wall ──MOTIVATES──> bowen-marsh
execution-of-janos-slynt ──MOTIVATES──> bowen-marsh
bowen-marsh ──AGENT_IN──> jon-is-stabbed-repeatedly
wick-whittlestick ──AGENT_IN──> jon-is-stabbed-repeatedly
```

---

## HARVEST

- adwd-jon-13.md:93 / food / Jon's breakfast that he barely eats — duck's eggs fried in drippings, strip of bacon, two sausages, blood pudding, half a loaf; raven steals the bacon; Jon manages bread and half an egg and one sip of sausage (washed down with ale to get the taste out); atmospheric meal before the stabbing chapter
- adwd-jon-13.md:195–197 / food + character / Tormund's arrival: "roaring for a horn of ale and something hot to eat"; ice in beard; immediately riffing on Gerrick Kingsblood's "little red cock"
- adwd-jon-13.md:21 / food + hospitality + humor / Queen Selyse's knights billeted at Castle Black; Tormund: "Afraid of being carried off, is she? … I always wanted me one with a mustache." — hospitality/gender customs contrast foreshadowing for the giants
- adwd-melisandre-01.md:71 / food + description / Melisandre's breakfast: "nettle tea, a boiled egg, and bread with butter. Fresh bread, if you please, not fried" — the red priestess's quotidian meal; notable because she says R'hllor provides nourishment but she "should eat" anyway; the domesticity undercuts her mystique
- adwd-melisandre-01.md:85–98 / description / "Rattleshirt" (actually Mance) described: widow's peak, close-set dark eyes, pinched cheeks, mustache wriggling "like a worm above a mouthful of broken brown teeth," cloaked in shadows, ruby on wrist pulsing; excellent physical description for the description-layer track
- adwd-prologue.md:39 / grim register / Varamyr's survivors eating their dead: "Those who escaped the black-cloaked crows … Some died of hunger, some of cold, some of sickness. Others were slain by those who had been their brothers-in-arms" — and the wolves' feast on the refugees (prologue:27 — eating flesh of the mother and child); starvation-driven cannibalism in the wildling diaspora after the Wall battle
- adwd-jon-12.md:263 / revelation-event / The Hardhome letter verbatim: "Wildlings eating their own dead. Dead things in the woods. … Dead things in the water." — load-bearing quote for the `hardhome-catastrophe` event node's evidence_quote
- adwd-jon-13.md:273 / location description + atmosphere / Shieldhall described: "one of the older parts of Castle Black, a long drafty feast hall of dark stone, its oaken rafters black with the smoke of centuries" — shields catalog; location enrichment for the `shieldhall` node
- adwd-jon-08.md:93 / food + atmosphere / Jon's pre-dawn breakfast returned by Edd after Val's departure: duck's eggs fried in drippings, strip of bacon, two sausages, blood pudding, half a loaf; raven steals the bacon immediately — almost verbatim repeated in jon-13 (GRRM callback); harvest for pattern-of-repetition track
- adwd-melisandre-01.md:25–26 / foreshadowing + description / Melisandre's fire-vision: "a wooden face, corpse white … a boy with a wolf's face threw back his head and howled" — Bloodraven + Bran vision; relevant to Bloodraven enrichment track (cross-track find); homeless quote, attach to bloodraven node

---

## SUMMARY FOR ORCHESTRATOR

**6 nodes proposed:** `the-shieldhall-speech` (event, NEW), `hardhome-catastrophe` (event, NEW). No other new nodes — `lord-of-bones` already exists (covers Rattleshirt), `rattleshirt` is not a separate slug.

**18 edge proposals:**
- Shieldhall rewire (E-B1 to E-B4): `pink-letter-delivered ENABLES the-shieldhall-speech TRIGGERS jon-is-stabbed-repeatedly` — this is the marquee structural addition
- Conspirators (E-B5 to E-B8): `left-hand-lew`, `alf-of-runnymudd`, `othell-yarwyck` all get `SUSPECTED_OF` Tier-2 (text = faction seating + exit, not confirmed stabbing); Yarwyck gets a parallel `MOTIVATES` grievance edge
- Glamour (E-B9 to E-B13): `mance-rayder IMPERSONATES lord-of-bones` (first use of IMPERSONATES type); `melisandre AGENT_IN mance-rayder-brought-to-execution`; `melisandre MANIPULATES lord-of-bones`; `lord-of-bones VICTIM_IN mance-rayder-brought-to-execution`
- Hardhome (E-B15 to E-B18): new event node wired into the causal chain; `hardhome-catastrophe ENABLES the-shieldhall-speech` + `MOTIVATES jon-snow`

**Key decisions:**
- **Shieldhall node:** MINT. The speech is a distinct, load-bearing event; collapsing Pink Letter → stabbing misrepresents the conspirators' decision point.
- **Conspirators:** Wick + Bowen = `AGENT_IN` (text explicit). Lew + Alf + Yarwyck = `SUSPECTED_OF` (faction seating / exit confirmed; knife-in-hand not confirmed). Do NOT assert Yarwyck or Lew as AGENT_IN — the text does not show them stabbing Jon.
- **Glamour model:** `mance-rayder IMPERSONATES lord-of-bones` (first use of the `IMPERSONATES` type). No new node for Rattleshirt — `lord-of-bones` IS Rattleshirt. FLAG the `"Mance Rayder"` alias on lord-of-bones as a collision hazard; propose curator swap to `DISGUISED_AS` edge.
- **Hardhome node:** `hardhome-catastrophe` (event) is new and load-bearing; `hardhome` (location) already exists. The revelation is the letter, not the off-page battle.
