# EVAL — Stratified Dispute-Axis Audit (design §7.2)

**Date:** 2026-07-07 · **Auditor:** fresh read-only verifier (Fable) · **Units:** recon-heirs-15-p02 (primary), recon-sons-05-p01 (cross-check)

---

## GATE VERDICT: **FAIL** (tier-inflation axis)

| Rate | Formula (per spec: missed / untagged-audited, over-tags / tagged-audited) | Result | Gate (>10% = FAIL) |
|---|---|---|---|
| **Over-tag rate (deflation)** | 0 over-tags / 7 tagged audited | **0.0%** | PASS |
| **Missed-hedge rate (inflation)** | 7 missed / 26 untagged audited | **26.9%** | **FAIL** |
| — edges only (strata b+c) | 6 / 18 | 33.3% | FAIL |
| — most-conservative sensitivity¹ | 2 hard-missed distinct claims / 23 | 8.7% | borderline |

¹ Sensitivity: dedup the exile cluster (E59 + EV18-agent + EV18-patient + daemon merge bullet = one underlying claim) and downgrade the two insinuation-class LOVER_OF edges to UNSURE. Even then the failure is material: the single deduped claim mints **four tier-1 graph artifacts plus an event node whose slug bakes the disputed cause into its name** (`daemon-exiled-after-the-rhaenyra-scandal`). The gate decision does not hinge on the counting convention.

**Worst finding:** F&B lines 107–125 open an explicitly flagged disputed zone ("here we must look to our more dubious chroniclers" → "Here is where our sources diverge") and close it with "Of the aftermath, these things are certain" (which certifies *only* that Daemon returned to the Stepstones). The sentence "Instead King Viserys sent him into exile, never to return to the Seven Kingdoms on pain of death" sits **inside Mushroom's version** — Eustace's version says only "told his brother to depart"; Runciter says only "the brothers quarreled again, and Prince Daemon departed"; "others assert" Alicent's urging. It even follows "purportedly" by one sentence. Yet it produced tier-1 untagged: edge E59 (BANISHES), role edges EV18-agent + EV18-patient, the event node `daemon-exiled-after-the-rhaenyra-scandal`, edge E60 (Lyonel's death-counsel, same parenthetical), and the daemon-targaryen merge-plan bullet. Mushroom's gossip minted as verified canon, six artifacts deep.

---

## Stratum a — ALL tagged edges in p02 (7/7) · over-tags: 0

| Edge | Claim | Tag | Hedge in scope (verbatim) | Verdict |
|---|---|---|---|---|
| E36 | LOVER_OF alicent→viserys (pre-Aemma bed) | t2 disputed, src=mushroom | "A few even cast doubt on Lady Alicent's virtue… These calumnies were never proved, though Mushroom repeats them in his Testimony" (:51) | OK |
| E57 | LOVER_OF daemon→rhaenyra (seduction) | t2 disputed, src=eustace | "Eustace, the less salacious of the two, writes that Prince Daemon seduced his niece" (:113) | OK |
| E58 | TEACHES daemon→rhaenyra ("lessons") | t2 disputed, src=mushroom | "if Mushroom can be believed" (:117) | OK |
| E70 | LOVES criston→rhaenyra (bedchamber confession) | t2 disputed, src=eustace | "That night, Septon Eustace reports, Ser Criston Cole slipped into the princess's bedchamber" (:143) | OK |
| E71 | COURTS rhaenyra→criston (White Sword Tower) | t2 disputed, src=mushroom | "Mushroom tells a very different tale. In his version, it was Princess Rhaenyra who went to Ser Criston" (:149) | OK |
| E72 | LOVER_OF harwin→rhaenyra (took her innocence) | t2 disputed, src=mushroom | "according to Mushroom, who claims to have found them in bed at break of day" (:155) | OK |
| E82 | LOVER_OF rhaenyra→harwin (solace in his arms) | t2 disputed, src=mushroom | "Yet Mushroom contradicts himself, for elsewhere in his Testimony he claims" (:175) | OK |

Every tag is genuinely hedged, correct chronicler, correct tier cap. Zero deflation. (Minor note on E36: the primary rumor source is anonymous court murmuring, Mushroom is the repeater — `src=mushroom` still defensible as the named chronicler.)

## Stratum b — 12 untagged tier-1 edges from p02, adversarially chosen · missed: 6

| Edge | Claim | Hedge in scope | Verdict |
|---|---|---|---|
| **E59** | BANISHES viserys→daemon ("sent him into exile… on pain of death", :123) | Entire passage under "Here is where our sources diverge" (:113); "he purportedly told his brother" one sentence prior; exile-on-pain-of-death is Mushroom's version only (Eustace: "told his brother to depart"; Runciter: quarrel + departure; others: Alicent's urging); "Of the aftermath, these things are certain" (:125) certifies only the Stepstones return | **MISSED-HEDGE** |
| **E60** | ADVISES lyonel→viserys (argued for Daemon's death, :123) | Same parenthetical, same Mushroom-tale scope, "purportedly" in-paragraph | **MISSED-HEDGE** |
| **EV18-agent** | viserys AGENT_IN daemon-exiled-after-the-rhaenyra-scandal (:123) | Same as E59; node slug additionally asserts the disputed *cause* ("the Rhaenyra scandal" — Runciter names no cause) | **MISSED-HEDGE** |
| **EV18-patient** | daemon VICTIM_IN same event (:123) | Same | **MISSED-HEDGE** |
| **E75** | LOVER_OF laenor→joffrey-lonmouth (:161) | Flat text says only "the groom's favorite… known as the Knight of Kisses"; the romantic substance is hedged: "was said to prefer their company" (:137), "Mushroom tells us that Ser Laenor spent every hour of those days at his bedside and wept bitterly" (:167–169). LOVER_OF asserts more than the flat text ever does | **MISSED-HEDGE** (insinuation-class) |
| **E81** | LOVER_OF laenor→qarl-correy (:173) | Flat text: "found a new favorite"; the bed-sharing is Mushroom's: "Mushroom concurs, but adds that Qarl Correy oft shared that bed as well" (:175) | **MISSED-HEDGE** (insinuation-class) |
| E84 | PARENT_OF laenor→jacaerys (:181) | Legal parentage is the flat societal fact, but scope is saturated with paternity-undermining material: "Whatever the truth of these tales" (:179), pointed brown-hair/pug-nose vs. Valyrian-features contrast (:179–181). Also quote-grounding is off — the quote proves Corlys→Laenor parentage, not Laenor→Jace | UNSURE (note-worthy, not counted) |
| E1 | OPPOSES otto→daemon (:15) | "Mushroom, Septon Eustace, Grand Maester Runciter, and all our other sources **concur**" — explicit consensus; correctly untagged | OK |
| E26 | LOVER_OF daemon→mysaria (:39) | "taking his paramour Mysaria with him" — flat narrator; "his concubine" flat (:43) | OK |
| E49 | OPPOSES alicent→rhaenyra (:87) | "The amity… had proved shortlived, for both Rhaenyra and Alicent aspired to be the first lady of the realm" — flat | OK |
| E69 | MANIPULATES viserys→rhaenyra (heir ultimatum, :139) | Ultimatum narrated flatly; the in-scope hedges (Eustace: fell at his knees / Mushroom: spat in his face) cover only her *reaction* — correctly discriminated | OK |
| E73 | HATES criston→rhaenyra (:157) | "However it happened, whether the princess scorned the knight or he her" hedges the *cause*; the outcome ("turned to loathing and disdain") is asserted flatly by the narrator — correctly tier-1 | OK |

## Stratum c — 6 untagged tier-1 edges from sons-05-p01 (cross-check) · missed: 0

| Edge | Claim | Hedge check | Verdict |
|---|---|---|---|
| E44 | ASSAULTS harren-the-red→gargon-qoherys (genital mutilation, :173) | Flat narrator; no chronicler framing | OK |
| E51 | CAPTURES orys→walter-wyl (:207) | Flat | OK |
| E52 | ASSAULTS orys→walter-wyl (hand/feet "usury", :207–208) | Flat narrator (the only hedged bit nearby — "his son Davos always said he died content" — was correctly NOT extracted) | OK |
| E53 | ASSAULTS wyl-of-wyl→orys ("Your father took my hand", :207) | Direct speech by the victim, corroborated by flat narrator epithets "Orys One-Hand" / "son of the Widow-lover" | OK |
| E57 | KILLS goren-greyjoy→lodos (:205) | Flat | OK |
| EV7-agent | alyssa AGENT_IN birth-of-aegon-son-of-aenys (:93) | "born to Lady Alyssa and fathered by Prince Aenys" — flat narrator, explicitly correcting Maegor's boast | OK |

**The 0.0 disputed_rate is genuine, not hedge-blindness.** The unit's hedged material correctly produced *no* edges at all: the Aenys-bastardy rumor ("a few even dared suggest that His Grace was not the boy's true sire", :19), Maegor's cat-butchering ("Supposedly… men said…though more like this tale was a calumny", :35–37), Visenya's Blackfyre remark ("she is reported to have said", :163–165), and Deria's double game ("was rumored to be sending them men, money, and supplies", :207) — all skipped. This is a flat-asserting chronicle stretch and the extractor read it as such.

## Stratum d — 8 merge-plan prose bullets from p02 · missed: 1

| Bullet (slug, cite) | Claim | Hedge check | Verdict |
|---|---|---|---|
| **daemon-targaryen** b5 (:123) | "a scandal over Rhaenyra led Viserys to exile him" | Asserts scandal-as-cause + exile flatly; the scandal is Eustace/Mushroom only, exile-decree Mushroom only, whole passage source-diverged (:113) | **MISSED-HEDGE** |
| rhaenyra-targaryen b2 (:141) | "the center of two rival accounts of scandal involving her uncle and Cole" | Dispute encoded IN the prose — model handling | OK |
| harwin-strong b2 (:155) | "Mushroom names him the man who took Rhaenyra's innocence" | Attribution carried inline — correct | OK |
| laenor-velaryon b1 (:137) | "had never shown interest in women" | Flat narrator sentence; the hedged clause ("was said to prefer their company") not asserted | OK |
| laenor-velaryon b2 (:173) | "preferred High Tide and favorites such as Ser Qarl Correy" | Stays at the text's euphemism level ("favorite"), unlike edge E81 | OK |
| joffrey-lonmouth b1 (:161) | "was Laenor's favorite; Rhaenyra's husband gave him a garter" | Same — flat euphemism preserved, no lover claim | OK |
| alicent-hightower b1 (:51) | "had read to the dying King Jaehaerys" | Flat; Mushroom's salacious embellishment correctly excluded | OK |
| mysaria b1 (:43) | paramour, pregnancy, dragon's egg | Flat narrator | OK |

## Pattern notes

1. **Sentence-local hedges are handled perfectly; passage-scope dispute framing is invisible.** All 7 tags fire on hedges *inside or adjacent to* the quoted sentence ("if Mushroom can be believed", "Septon Eustace reports"). All 4 hard misses are sentences that carry no local attribution but sit inside a zone the narrator explicitly opened as disputed ("here we must look to our more dubious chroniclers" :107, "Here is where our sources diverge" :113) and closed with "Of the aftermath, these things are certain" (:125). The extractor needs a *dispute-zone* concept: everything between a divergence marker and a certainty marker inherits the hedge unless the narrator re-asserts ("that is beyond dispute", "both agree"). Even "purportedly" one sentence upstream didn't rescue E59.
2. **Insinuation-inflation subtype:** F&B's narrator encodes same-sex relationships as flat euphemism ("favorite", "Knight of Kisses") and puts the explicit content in Mushroom's mouth. The edge layer upgraded euphemism+hedged-corroboration to explicit `LOVER_OF` at tier-1 (E75, E81) — asserting more than the flat text does. Notably the merge-plan prose handled the identical material correctly, so this is an edge-typing problem, not a reading problem.
3. **Event-node minting propagates the miss multiplicatively:** one un-hedged sentence became 1 relation edge + 2 role edges + 1 event node + 1 prose bullet, and the node slug hard-codes the disputed cause ("…after-the-rhaenyra-scandal"). Dispute detection must run *before* event-node minting.
4. **Zero over-tagging, and genuinely good discriminations exist** (E1 sources-concur → tier-1; E73 disputed-cause/certain-outcome split; E69 ultimatum vs. hedged reaction; sons-05-p01's clean 0.0 rate with all hedged material correctly skipped). The failure is one-directional: inflation only. A prompt fix targeting patterns 1–3 should not cost tier-1 yield on flat chronicle text.

## Recommended fix targets (for the reconciler/extractor prompt)

- Add explicit dispute-zone open/close markers to the hedge lexicon: "our sources diverge/differ", "dubious chroniclers", "tell another tale", "In his version", closed by "these things are certain", "that is beyond dispute", "both agree", "all the chronicles agree", "sources concur".
- Rule: a claim inside an open dispute zone is tagged with the version's chronicler even when the sentence itself has no attribution.
- Rule: `LOVER_OF` (and other sexual/romantic types) at tier-1 requires a flat narrator assertion; "favorite"/"was said to prefer" + chronicler-attributed detail caps at tier-2 disputed.
- Rule: event nodes minted from claims inside a dispute zone inherit disputed/tier-2 and must not encode the disputed cause in the slug.
