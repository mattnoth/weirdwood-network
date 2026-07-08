# EVAL — Stratified Dispute-Axis Audit v2 (re-run after reconciler dispute-proximity quarantine)

**Date:** 2026-07-07 · **Auditor:** fresh read-only verifier (Fable) · **Units:** recon-heirs-15-p02 (primary), recon-sons-05-p01 (cross-check), recon-heirs-15-p01 (quarantine rows only) · **Prior audit:** EVAL-dispute-axis-audit.md (GATE FAIL, 26.9% missed-hedge)

---

## GATE VERDICT: **PASS**

| Rate | Formula | Result | Gate (>10% = FAIL) |
|---|---|---|---|
| **Missed-hedge rate (inflation)** | 0 missed / 26 untagged audited (strata b+c+d) | **0.0%** | PASS |
| **Over-tag rate (deflation)** | 0 over-tags / 7 tagged audited (stratum a) | **0.0%** | PASS |
| False-hold rate (stratum e, non-gating) | 10 false holds / 19 quarantine rows | **52.6%** | reported only |

**The fix landed.** All seven of the prior audit's misses are quarantined, not emitted: E59 BANISHES (held, row 3), E60 ADVISES-death-counsel (row 4), the `daemon-exiled-after-the-rhaenyra-scandal` event + both EV18 role edges (event held row 12, so the role edges were never minted — the slug with the disputed cause is gone from `new_node_slugs`), insinuation LOVER_OF laenor→joffrey (row 5) and laenor→qarl (row 11), and the daemon merge-plan exile bullet (row 14). Nothing hedged escaped into the emitted set in any of the three strata, and no correctly-flat claim was newly over-tagged. The cost moved where it was designed to move: into quarantine review volume, where roughly half the held rows are flat public facts (details in stratum e).

**Worst residual finding (non-gating):** the strong-terms lexicon has no weak-hedge forms — "it was said", "men said", "was said to", "reportedly", "is reported to have said", "rumored", "supposedly", "legend says". The live near-miss: PROTECTS criston→alicent (:171) sits inside "**It was said** that Queen Alicent did not share his displeasure, however; soon after, she asked that Ser Criston Cole be made her personal protector" — it was held only because a Mushroom *nickname parenthetical* ("or Brokenbones, as Mushroom had it") coincidentally shares the hard-wrapped line. A unit with "it was said" material more than one line from any chronicler name would emit tier-1 untagged. Zero actual escapes in these three units, but the protection there is luck, not design.

---

## Stratum a — ALL tagged edges in p02 candidates.json (7/7) · over-tags: 0

| Edge | Claim | Tag | Hedge in scope (verbatim, p02) | Verdict |
|---|---|---|---|---|
| E36 | LOVER_OF alicent→viserys (pre-Aemma bed) | t2 disputed, src=mushroom | "These calumnies were never proved, though Mushroom repeats them in his Testimony" (:51) | OK |
| E57 | LOVER_OF daemon→rhaenyra (seduction) | t2 disputed, src=eustace | "Eustace, the less salacious of the two, writes that Prince Daemon seduced his niece" (:113) | OK |
| E58 | TEACHES daemon→rhaenyra ("lessons") | t2 disputed, src=mushroom | "if Mushroom can be believed" (:117) | OK |
| E70 | LOVES criston→rhaenyra (bedchamber confession) | t2 disputed, src=eustace | "That night, Septon Eustace reports…" (:143–145) | OK |
| E71 | COURTS rhaenyra→criston (White Sword Tower) | t2 disputed, src=mushroom | "Mushroom tells a very different tale. In his version…" (:149) | OK |
| E72 | LOVER_OF harwin→rhaenyra (took her innocence) | t2 disputed, src=mushroom | "according to Mushroom, who claims to have found them in bed" (:155) | OK |
| E82 | LOVER_OF rhaenyra→harwin (solace in his arms) | t2 disputed, src=mushroom | "Yet Mushroom contradicts himself, for elsewhere in his Testimony" (:175) | OK |

Identical tag set to the prior run; every tag genuinely hedged, correct chronicler, tier capped at 2. Zero deflation — the quarantine did not cause over-tagging of pass-through rows.

## Stratum b — 12 untagged tier-1 edges from p02 EMITTED set, adversarially chosen · missed: 0

| Edge | Claim | Hedge check (±10 lines) | Verdict |
|---|---|---|---|
| E73 | HATES criston→rhaenyra (:157) | "However it happened, whether the princess scorned the knight or he her" hedges only the *cause*; "turned to loathing and disdain" is flat narrator | OK |
| E69 | MANIPULATES viserys→rhaenyra, heir ultimatum (:139) | Ultimatum flat; Eustace/Mushroom hedges cover only her reaction (fell at knees vs. spat), and "both agree that in the end she consented" certifies the outcome | OK |
| E84 | PARENT_OF laenor→jacaerys (:181), **qualifier now `claimed`** | Legal parentage is the flat societal frame; paternity doubt (:179 "Whatever the truth of these tales") is now encoded in the qualifier rather than ignored — improvement over the prior run's bare tier-1 | OK |
| E66 | COURTS harwin→rhaenyra (:131) | "paid court to the princess, as did the Hand's eldest son" — flat suitor list | OK |
| E49 | OPPOSES alicent→rhaenyra (:87) | "both Rhaenyra and Alicent aspired to be the first lady of the realm" — flat | OK |
| E55 | SWORN_TO daemon→viserys (:103) | Public act before "lords and commons", flat narration | OK |
| E61 | APPOINTS viserys→criston LC (:125) | Inside "Of the aftermath, these things are certain" — explicitly certified zone | OK |
| E74 | SPOUSE_OF rhaenyra→laenor (:161) | Wedding flat; "all agreed that they made a handsome couple". Note: "the fool Mushroom" (in Rhaenyra's retinue) is on this line yet E74 correctly emitted — certainty-rescue or scope handling worked | OK |
| E20 | PROTECTS criston→rhaenyra (:23) | "Rhaenyra begged her father to name Ser Criston her own personal shield" — flat | OK |
| E3 | DEPOSES viserys→daemon (:15) | Line contains "Mushroom, Septon Eustace, Grand Maester Runciter, and all our other sources **concur**" — consensus marker correctly rescued the whole line's edges (E1, E2, E3) despite two strong terms present | OK |
| E34 | PARENT_OF otto→alicent (:49–51) | "eighteen-year-old daughter of the King's Hand" — flat; the Mushroom material on :51 disputes her virtue, not her parentage | OK |
| EV22-agent | rhaenyra AGENT_IN takes-dragonstone (:127) | Continuation of the "these things are certain" aftermath; flat | OK |

## Stratum c — 6 untagged tier-1 edges from sons-05-p01 · missed: 0

| Edge | Claim | Hedge check | Verdict |
|---|---|---|---|
| E53 | ASSAULTS wyl-of-wyl→orys ("Your father took my hand", :207) | Victim's direct speech + flat narrator epithets "Orys One-Hand" / "son of the Widow-lover" | OK |
| E52 | ASSAULTS orys→walter-wyl (hands/feet "usury", :207) | Flat narrator; the only hedged bit ("his son Davos always said he died content") was correctly not extracted | OK |
| E57 | KILLS goren→lodos (:205) | Flat | OK |
| E58 | DEFEATS allard-royce→jonos-arryn (:195) | Flat | OK |
| EV7-agent | alyssa AGENT_IN birth-of-aegon-son-of-aenys (:93) | "born to Lady Alyssa and fathered by Prince Aenys" — flat narrator explicitly correcting Maegor's boast | OK |
| EV14-patient | lodos VICTIM_IN invasion-of-the-iron-islands (:205) | Flat | OK |

The unit's genuinely hedged material still produced zero artifacts (Aenys bastardy rumor :19, Maegor cat-butchering "Supposedly… men said… calumny" :35–37, Visenya's "she is reported to have said" :163–165, Deria "was rumored to be sending them men" :207) — its empty dispute-review.jsonl reflects a clean flat-asserting unit, not a dead quarantine.

## Stratum d — 8 merge-plan prose bullets from p02 · missed: 0

| Bullet (slug, cite) | Claim | Hedge check | Verdict |
|---|---|---|---|
| rhaenyra-targaryen b2 (:141) | "center of two rival accounts of scandal involving her uncle and Cole… forced to consent… bore a son in 114 AC" | Dispute encoded in the prose itself; consent certified by "both agree" | OK |
| harwin-strong b2 (:155) | "Mushroom names him the man who took Rhaenyra's innocence" | Attribution carried inline — model handling | OK |
| laenor-velaryon b1 (:137) | "had never shown interest in women" | Flat narrator sentence; hedged clause ("was said to prefer their company") not asserted | OK |
| laenor-velaryon b2 (:173) | "preferred High Tide and favorites such as Ser Qarl Correy" | Stays at the text's flat euphemism level ("favorite") | OK |
| joffrey-lonmouth b1 (:161) | "was Laenor's favorite; Rhaenyra's husband gave him a garter" | Flat euphemism preserved, no lover claim | OK |
| mysaria b1+b2 (:43) | paramour, pregnancy, dragon's egg, sent back to Lys, miscarriage | Flat narrator throughout | OK |
| alicent-hightower b1 (:83) | "wed Viserys in 106 AC and bore him Aegon, Helaena, Aemond, and Daeron" | Flat (the read-to-Jaehaerys bullet that shared a line with Mushroom material was held, leaving this single clean bullet) | OK |
| otto-hightower b4 (:91) | "As Alicent's father he became the loudest of her supporters, and in 109 AC Viserys stripped him of his chain" | Flat | OK |

The daemon-targaryen entry no longer contains the exile bullet — it stops at "crowned himself King of the Stepstones" (:81), with the scandal-exile claim held in quarantine (row 14). This is the exact prior stratum-d miss, fixed.

## Stratum e — quarantine precision: all 17 p02 rows + 2 p01 rows · false holds: 10/19 (52.6%)

Criterion: REASONABLE = claim genuinely inside/adjacent to hedged material (adjudicator would tag, rephrase, or re-ground it); FALSE = flat public fact held, pure review cost. Non-gating.

| # | Row (kind, claim, line) | Held via | Verdict | Why |
|---|---|---|---|---|
| 1 | edge LOVER_OF daemon→mysaria (p02:39) | romance-class-untagged | **FALSE** | "taking his **paramour** Mysaria" — flat narrator; the blanket romance rule's by-design cost. Adjudicator emits unchanged (was the prior audit's OK exemplar E26) |
| 2 | edge UNCLE_OF daemon→rhaenyra (p02:113) | mushroom | REASONABLE (borderline) | The kinship fact is flat and asserted elsewhere (:105 "her favorite uncle"), but the located quote ("his niece the princess") is drawn from inside Eustace's disputed seduction account — adjudicator re-grounds the quote, so the hold does real work |
| 3 | edge BANISHES viserys→daemon (p02:123) | mushroom | **REASONABLE** | The prior audit's worst miss — exile-on-pain-of-death is Mushroom's version only. Core fix target, correctly caught |
| 4 | edge ADVISES lyonel→viserys, death counsel (p02:123) | mushroom | **REASONABLE** | Same Mushroom-tale parenthetical, "purportedly" in-paragraph. Core fix target |
| 5 | edge LOVER_OF laenor→joffrey (p02:161) | romance-class-untagged | **REASONABLE** | Insinuation class: flat text says only "favorite… Knight of Kisses"; the romantic substance is Mushroom's. Adjudicator tags t2 or downgrades type |
| 6 | edge KILLS criston→joffrey (p02:167) | mushroom | **FALSE** | The tourney kill is flat narrator ("the blows he rained down… cracked his helm… Ser Joffrey died"); Mushroom on the line only for the "Brokenbones" nickname and the bedside-weeping detail |
| 7 | edge ATTACKS criston→harwin (p02:167) | mushroom | **FALSE** | "He left Breakbones with a broken collarbone and a shattered elbow" — flat; same nickname-parenthetical trigger |
| 8 | edge ALLIES_WITH criston→alicent (p02:171) | mushroom | **FALSE** | "having gone over entirely to the queen's party, the greens" — flat narrator |
| 9 | edge PROTECTS criston→alicent (p02:171) | mushroom | REASONABLE (borderline) | The protector request arguably sits under "**It was said** that Queen Alicent did not share his displeasure, however; soon after, she asked…" — a weak hedge the lexicon doesn't know; held by lucky Mushroom-nickname proximity. Right outcome, wrong mechanism |
| 10 | edge COMPANION_OF harwin→rhaenyra (p02:171) | mushroom | **FALSE** | "becoming the foremost of the blacks, ever at Rhaenyra's side at feast and ball and hunt" — flat narrator |
| 11 | edge LOVER_OF laenor→qarl (p02:173) | romance-class-untagged | **REASONABLE** | Insinuation class: flat text says "found a new favorite"; bed-sharing is Mushroom's (:175). Prior miss E81, correctly caught |
| 12 | event "Daemon exiled after the Rhaenyra scandal" (p02:123) | mushroom | **REASONABLE** | Disputed cause baked into the name; holding it before minting killed the node slug + both role edges. The multiplicative-propagation fix working as designed |
| 13 | event "Death of Joffrey Lonmouth at the wedding tourney" (p02:167) | mushroom | **FALSE** | The death is flat narrator, certain; same nickname-parenthetical trigger as #6/#7 |
| 14 | prose daemon-targaryen, scandal-exile bullet (p02:123) | mushroom | **REASONABLE** | Prior stratum-d miss, correctly caught |
| 15 | prose alicent-hightower, read-to-Jaehaerys bullet (p02:51) | mushroom | **FALSE** | "the girl who had read to King Jaehaerys as he lay dying" is flat narrator; Mushroom's adjacent claim embellishes the same scene but the bullet asserts only the flat part (prior audit passed this exact bullet as emitted-OK) |
| 16 | prose harwin-strong, foremost-of-blacks bullet (p02:171) | mushroom | **FALSE** | Flat narrator (see #10) |
| 17 | prose joffrey-lonmouth, death bullet (p02:167) | mushroom | **FALSE** | Flat narrator (see #13) |
| 18 | edge LOVER_OF daemon→mysaria (p01:183) | romance-class-untagged | **REASONABLE** | "a certain Lysene dancing girl soon became his **favorite**" — euphemism-level quote upgraded to LOVER_OF; exactly the insinuation pattern the rule exists for (the flat "paramour" corroboration is in a different unit) |
| 19 | prose mushroom, chronicle-burned bullet (p01:203) | mushroom | **FALSE** | "King Baelor the Blessed decreed that every copy of Mushroom's chronicle should be burned" — flat historical fact. Self-referential trap: any prose *about* a chronicler always contains his name |

**False-hold rate: 10/19 = 52.6%.** All 9 reasonable holds include every one of the prior audit's 7 misses (counting the event hold as covering both role edges) — quarantine recall on the known failure set is 100%.

## Pattern notes

1. **The fix's mechanism is sound and its recall on the target class is perfect in this sample.** Passage-scope dispute framing (the :107–:125 exile cluster) and insinuation-class romance edges — the two prior failure modes — are fully intercepted. The certainty-rescue also demonstrably works in both directions: ":15 sources concur" and ":19 all the chronicles agree" let consensus-zone edges (E1/E2/E3, E10) pass despite chronicler names on the line, and the ":125 these things are certain" zone emitted E61/EV20/EV22 cleanly.
2. **Dominant false-hold driver: chronicler-name-as-character, not as source.** 8 of 10 false holds fire on "mushroom" appearing in a non-attributive role — nickname parentheticals ("prompting Mushroom to name him 'Brokenbones'", "or Brokenbones, as Mushroom had it", :167/:171), Mushroom as a member of Rhaenyra's retinue (:161), Mushroom as prose *subject* (p01:203). Lines 167 and 171 alone account for 7 false holds. A cheap precision fix: treat `mushroom`/`eustace` as hedge triggers only in attributive frames (tells/says/claims/reports/according to/Testimony/insists/names within N tokens), or whitelist known nickname parentheticals. The self-referential trap (#19) needs a special case: prose bullets whose *entity* is a chronicler will always self-trigger.
3. **Line granularity amplifies both catch and cost.** These are hard-wrapped page-extraction files, so one "line" can span most of a paragraph and ±1 line can span three; a single non-attributive "Mushroom" quarantines every artifact from ~2 paragraphs of flat tourney narration. Sentence-window proximity would cut most of the 52.6% without losing the real catches (all of which have the hedge in the same sentence or same version-scope).
4. **Residual lexicon gap — weak narrator hedges (the worst remaining escape risk).** "it was said", "men said", "was said to", "reportedly", "is reported to have said", "rumored", "supposedly", "legend says" are all absent from the strong-terms list. In these units they cost nothing — the extractor skipped that material or (row #9) a chronicler name happened to share the line — but F&B uses these forms *away* from chronicler names routinely (p02:83 "His Grace is reported to have said", p02:33 "legend says", sons:207 "rumored"). First unit where the extractor lifts an artifact from such a sentence with no Mushroom/Eustace within ±1 line, it emits tier-1 untagged. Recommend adding the said/reported/rumored/supposedly/legend family as strong terms (they are near-zero false-positive as *attributive* phrases).
5. **Blanket romance-hold splits 3 reasonable / 2 false in this sample** (#5, #11, #18 vs #1 flat-"paramour", and #1's p02 twin is the only flat one; p01 #18 is euphemism-grade). Cheap refinement: exempt untagged LOVER_OF/PARAMOUR_OF whose quote itself contains the narrator's own flat vocabulary ("paramour", "concubine", "mistress") — those words are the narrator asserting, not insinuating.
6. **E84 (laenor PARENT_OF jacaerys) now carries `qualifier: claimed`** — the paternity-doubt saturation the prior audit flagged as UNSURE is now encoded rather than ignored. Reasonable resting state for the legal-parentage pattern.

## Bottom line

Both gated rates are 0.0% — the reconciler quarantine closed the tier-inflation channel without inducing over-tagging, and the emitted graph surface for these units is now clean on the dispute axis. The cost is a ~53% false-hold rate in the review queue (10 flat facts across 19 rows, concentrated on two hard-wrapped lines where Mushroom appears as a character), which is tolerable at smoke scale but worth the two cheap precision fixes (attributive-frame check for chronicler names; sentence-window proximity) before a full-book run, plus the weak-hedge lexicon additions to close the one demonstrated near-miss mechanism.
