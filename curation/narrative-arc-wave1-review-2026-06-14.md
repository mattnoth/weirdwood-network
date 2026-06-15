# Narrative-Arc Wave 1 — Independent Review
**Date:** 2026-06-15
**Reviewer:** Independent review agent (fresh, did not write drafts)
**Model:** claude-sonnet-4-6
**Scope:** Red Wedding draft + Joffrey Poisoning draft
**Prototype reference:** Q5 `incident-at-the-trident` in `curation/s95-quarantine-resolutions-2026-06-13.md`
**Method:** Local sources only. All evidence quotes verified against actual chapter files via grep + line reads. All slugs verified against `graph/nodes/`. No web fetches.

---

## Overall Verdicts

| Arc | Verdict | Must-Fix Issues |
|---|---|---|
| Red Wedding | **MINT-WITH-FIXES** | 5 must-fix, 1 design question |
| Joffrey Poisoning | **MINT-WITH-FIXES** | 3 must-fix, 2 vocab gaps to resolve |

Neither draft needs rework from scratch. Both are structurally sound with the right shape and good evidence coverage. The issues are fixable before emit.

---

## RED WEDDING ARC (`red-wedding-conspiracy`)

### Verified Clean (Red Wedding)

The following were spot-checked and found correct:

1. **`asos-catelyn-02.md:133`** — "And you," she said softly, "have lost the Freys." — VERBATIM confirmed at line 133. The TRIGGERS edge quotes this plus line 135 continuation; citing `:133` as the start line is acceptable.
2. **`asos-catelyn-04.md:209`** — "You are then instructed to offer Lord Tully the hand of my sister, the Lady Roslin, a maid of sixteen years." — VERBATIM confirmed at line 209.
3. **`asos-catelyn-07.md:99`** — The Rains of Castamere passage ("players in the gallery…began to play a very different sort of song") — VERBATIM confirmed at line 99.
4. **`asos-catelyn-07.md:113`** — Grey Wind howl ("crash of distant battle, and closer the wild howling of a wolf") — VERBATIM confirmed at line 113.
5. **`asos-tyrion-06.md:41`** — "Roslin caught a fine fat trout…Her brothers gave her a pair of wolf pelts for her wedding." — VERBATIM confirmed at line 41.
6. **`asos-tyrion-06.md:125`** — Tyrion's "plotting this" + Tywin's "I mislike that word" — confirmed lines 125 and 127. (Note: the JSON's spliced quote with "…" between them is acceptable notation; the two Tywin lines cited are real.)
7. **`asos-tyrion-06.md:205`** — "I have no doubt he hatched this ugly chicken…" — VERBATIM confirmed at line 205.
8. **`asos-tyrion-06.md:207`** — "The price was cheap by any measure…Roose Bolton becomes Warden of the North." — VERBATIM confirmed at line 207.
9. **`asos-epilogue.md:169`** and **`:171`** — Both Merrett quotes VERBATIM confirmed.
10. **`asos-arya-07.md:97`** — Thoros Last Kiss description — VERBATIM confirmed at line 97.
11. **`asos-arya-12.md:89`** — Nymeria retrieves body — VERBATIM confirmed at line 89.
12. **`asos-catelyn-02.md:99`** — Robb presents Jeyne ("great honor to present you the Lady Jeyne Westerling") — VERBATIM confirmed at line 99.
13. All character slugs verified as live nodes: `grey-wind`, `beric-dondarrion`, `nymeria-direwolf` (disambiguated correctly from `nymeria` = Princess Nymeria of the Rhoyne), `walder-frey`, `roose-bolton`, `tywin-lannister`, `robb-stark`, `lothar-frey` (aliases include "Lame Lothar" — confirmed correct character), `roslin-frey`, `jeyne-westerling`, `catelyn-stark`.
14. All claimed-existing event slugs verified live: `red-wedding`, `catelyn-is-killed`, `robb-is-killed`, `catelyn-secures-guest-right`, `the-wedding-feast-proceeds`, `grey-wind-attacks`, `red-wedding-revealed`, `merrett-attempts-to-defend-his-innocence-in-the-red-wedding`, `jaime-demands-the-red-wedding-captives`.
15. `event.conspiracy` confirmed in `reference/architecture.md` entity-type table (row 117).
16. None of the 5 proposed new slugs exist yet: `red-wedding-conspiracy`, `robb-breaks-frey-marriage-pact`, `frey-bolt-offer-edmure-roslin`, `death-of-grey-wind`, `catelyn-is-resurrected-as-lady-stoneheart` — clean new mints, no duplicates.
17. Tier-2 assignments for Grey Wind victim edge and Beric agent edge are correct and well-justified in the draft (6.1, 6.2).

---

### Issues Found (Red Wedding)

**Issue RW-1 — WRONG LINE NUMBER (must-fix): TRIGGERS `frey-bolt-offer-edmure-roslin TRIGGERS red-wedding` cites `:219` for the "It must happen" quote, but that quote is at line 251.**

- Edge in question: the TRIGGERS edge in §2b, `source_slug:"frey-bolt-offer-edmure-roslin"`, `target_slug:"red-wedding"`.
- Cited: `evidence_ref:"sources/chapters/asos/asos-catelyn-04.md:219"`, `evidence_quote:"\"It must happen,\" said Catelyn, though not gladly. \"I have no more wish to suffer Walder Frey's insults and complaints than you do, Brother, but I see little choice here. Without this wedding, Robb's cause is lost. Edmure, we must accept.\""`
- Actual line 219: `"Lame Lothar spread his hands. 'My brother has a soldier's bluntness, but what he says is true. It is my lord father's wish that this marriage take place at once.'"` — a completely different quote.
- Actual line 251: "It must happen," said Catelyn… — confirmed verbatim.
- **Fix:** Change `evidence_ref` to `sources/chapters/asos/asos-catelyn-04.md:251`.

---

**Issue RW-2 — SCOPE-TEST VIOLATION (must-fix): `death-of-grey-wind` is proposed as SUB_BEAT_OF `red-wedding-conspiracy` (the arc parent) but it happened physically at the Twins DURING the massacre — it is a beat OF `red-wedding`, not a direct beat of the conspiracy.**

- The draft's asserted_relation says "direct consequence-beat of the conspiracy, occurring simultaneously with Robb's killing." The phrase "occurring simultaneously with Robb's killing" confirms it happened DURING the red-wedding event, not before or after.
- Per the parent-shape rule: Grey Wind's death happens WITHIN `red-wedding`'s scope, not the conspiracy parent's scope. The conspiracy parent holds planning beats (pre-event) and aftermath beats (post-event). An event occurring inside the feast-hall/Twins compound during the massacre is a sub-beat of the massacre, not of the conspiracy.
- The TRIGGERS edge `red-wedding TRIGGERS death-of-grey-wind` is correctly scoped at the event level.
- **Fix:** Remove `SUB_BEAT_OF death-of-grey-wind -> red-wedding-conspiracy`. Instead, add `SUB_BEAT_OF death-of-grey-wind -> red-wedding` (death-of-grey-wind is a sub-beat of the massacre event). The arc can still reach it via `red-wedding-conspiracy → [SUB_BEAT_OF] red-wedding → [TRIGGERS] death-of-grey-wind`.

---

**Issue RW-3 — CIRCULAR TRIGGER (must-fix): `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy` creates a sub-beat that triggers its own parent.**

- The draft proposes BOTH `robb-breaks-frey-marriage-pact SUB_BEAT_OF red-wedding-conspiracy` AND `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy`.
- Semantically: can a beat trigger the event it is already part of? The Q5 Trident prototype has no case of a sub-beat triggering its own parent — the only TRIGGERS in Q5 goes between siblings (`cersei-maneuvers TRIGGERS death-of-mycah`), not from child to parent.
- The TRIGGERS from child to parent is logically odd: if the broken pact is a sub-beat OF the conspiracy, the conspiracy is already defined as including it; saying the broken pact "triggers" the conspiracy means the conspiracy both contains its own cause and was triggered by it.
- **Fix:** Drop the `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy` TRIGGERS edge. The causal relationship is already implied by the arc tree: the broken pact is the initiating sub-beat, chronologically first. If a TRIGGERS is needed for traversal, use `robb-breaks-frey-marriage-pact TRIGGERS frey-bolt-offer-edmure-roslin` (currently omitted but causally correct: the broken pact is what causes Walder to construct the Edmure lure). The draft's §4 Q4 correctly identifies this as valid but omitted it as "redundant" — it's actually the cleaner choice vs. the circular parent-trigger.

---

**Issue RW-4 — DESIGN-MEMO DEVIATION (must-fix or explicit sanction from Matt): Role edges on the parent hub (`red-wedding-conspiracy`) contradict the design memo.**

- The design memo (`working/narrative-arcs-design-memo-2026-06-13.md`, line 33) states: **"Role edges live at the BEAT level only (parent has zero direct role edges — all participants attach at sub-beats). This matches Red Wedding precedent."**
- The Red Wedding draft proposes `COMMANDS_IN tywin-lannister -> red-wedding-conspiracy`, `COMMANDS_IN walder-frey -> red-wedding-conspiracy`, and `AGENT_IN roose-bolton -> red-wedding-conspiracy` — all on the parent hub.
- The Q5 Trident prototype confirms: `incident-at-the-trident` has zero direct role edges; all participants attach at sub-beats.
- The draft's rationale (Tywin/Walder/Roose operate at the arc level, not any single beat) is defensible but it is a deliberate deviation from the design memo's stated rule.
- **This requires an explicit call from Matt** before emit. Two options:
  - (A) Keep role edges on parent: update the design memo to allow "conspiracy-architect" role edges on conspiracy-type parent hubs. This is arguably the right call for `event.conspiracy` nodes where the planners are distinct from the executors.
  - (B) Move to sub-beats: attach Tywin/Walder to `robb-breaks-frey-marriage-pact` (Walder's reaction starts the conspiracy) and to `red-wedding` itself (Walder commands at the Twins). Attach Roose to `red-wedding` (he's the on-the-ground Bolton at the Twins). This preserves the "zero role edges on parent" rule.
  - **Recommendation:** (A) with design-memo update. The `event.conspiracy` type is specifically about the planning layer; the conspiracy architects don't appear at any single sub-beat — they appear across the whole arc. Hanging them on the parent is the correct semantic for this node type.

---

**Issue RW-5 — MINOR: Quote in TRIGGERS `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy` spans two non-adjacent lines (:133 and :135) but cites only :133.**

- Not an error — citing the start line is standard practice (Q5 uses the same convention). Flagged as minor.
- **Fix:** Optional — could improve to `:133-135` or split into two evidence refs. Low priority.

---

**Issue RW-6 — SLUG NAME (cosmetic, Matt's call):** `frey-bolt-offer-edmure-roslin` is awkward ("bolt offer" reads as crossbow). The draft flags this (§6.7). Alternatives: `lothar-delivers-roslin-offer` or `frey-offer-edmure-roslin-marriage`. No blocking issue; the graph functions either way.

---

## JOFFREY POISONING ARC (`joffrey-poisoning-conspiracy`)

### Verified Clean (Joffrey)

1. **`asos-sansa-02.md:71`** — "The night of Joffrey's wedding, that's not so long, wear the silver hair net and do as I told you" — VERBATIM confirmed at line 71.
2. **`asos-tyrion-08.md:101`** — "The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net. 'I was very sorry to hear about your losses,' she said as she tugged and fiddled." — VERBATIM confirmed at line 101.
3. **`asos-sansa-05.md:23`** — "The web of spun silver hung from her fingers…Black amethysts from Asshai. One of them was missing. Sansa lifted the net for a closer look. There was a dark smudge in the silver socket where the stone had fallen out." — VERBATIM confirmed at line 23.
4. **`asos-sansa-05.md:105`** — "Not far. Ser Dontos took her hand in his own and rubbed it gently. Your friend is near, waiting for you." — VERBATIM confirmed at line 105.
5. **`asos-sansa-05.md:127`** — "One bolt took Dontos in the chest as he looked up, punching through the left crown on his surcoat." — VERBATIM confirmed at line 127.
6. **`asos-sansa-05.md:135`** — "He sold you for a promise of ten thousand dragons. Your disappearance will make them suspect you in Joffrey's death…A bag of dragons buys a man's silence for a while, but a well-placed quarrel buys it forever…All he did he did at my behest." — VERBATIM confirmed at line 135 (the full Littlefinger speech).
7. **`asos-sansa-06.md:145`** — "Ser Dontos the Red was a skin of wine with legs…all Dontos had to do was lead you from the castle…and make certain you wore your silver hair net." — VERBATIM confirmed at line 145.
8. **`asos-sansa-06.md:183`** — "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you." — VERBATIM confirmed at line 183.
9. **`asos-sansa-06.md:193`** — "Be that as it may. Lady Olenna was not about to let Joff harm her precious darling granddaughter…" — VERBATIM confirmed at line 193.
10. **`asos-sansa-06.md:55`** — "The two old men waded out up to their thighs to lift Sansa from the boat so she would not get her skirts wet. Oswell and Lothor splashed their way ashore." — VERBATIM confirmed at line 55.
11. All character slugs verified live: `petyr-baelish`, `dontos-hollard`, `sansa-stark`, `olenna-tyrell`, `lothor-brune`.
12. All claimed-existing event slugs verified live: `purple-wedding`, `death-of-joffrey-baratheon`, `wedding-ceremony-at-the-great-sept-of-baelor`, `tyrell-plot-revealed`, `killing-of-dontos-hollard`.
13. None of the 4 proposed new slugs exist yet: `joffrey-poisoning-conspiracy`, `dontos-delivers-hairnet-to-sansa`, `olenna-takes-stone-from-hairnet`, `sansa-s-escape-from-kings-landing` — clean new mints.
14. All Tier-2 assignments for Littlefinger-sourced edges are correct. The draft is appropriately rigorous: every Littlefinger reveal quote stays at Tier-2, per Flag 2 and the unreliable-narrator rule.
15. `event.conspiracy` and `event.deception` confirmed in architecture.md.
16. `event.conspiracy` parent node at Tier-2: correct — the conspiracy's details come from Littlefinger's self-serving account.

---

### The Olenna On-Page Claim (Review Requirement #5)

**Finding: VERIFIED AS ON-PAGE but attribution of the ACT is inferred, not stated.**

The `asos-tyrion-08.md:101` text IS genuinely on-page Tyrion POV:

> "The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net."

Tyrion WITNESSES Olenna touching Sansa's hairnet. This is not Littlefinger's testimony — it is in-chapter narration from Tyrion's POV.

However: the text shows Olenna "fussing" and "straightening" the hairnet. It does NOT say she removed a stone. The inference that she removed the Strangler crystal is confirmed retrospectively by Littlefinger in Sansa VI, but is not explicitly stated in Tyrion VIII.

**Tier ruling:** The `AGENT_IN olenna-tyrell -> olenna-takes-stone-from-hairnet` edge is correctly Tier-2. The on-page scene establishes she had physical access to the hairnet; the interpretation that she removed a stone requires Littlefinger's later testimony to confirm. Tier-2 is the correct conservative call — do not promote to Tier-1. The scene grounds the Tier-2 (it's not purely inferential; there IS on-page physical evidence), but the specific act of stone-removal is not stated in the scene itself.

**Implication:** The draft's handling is correct as written. No change needed.

---

### Issues Found (Joffrey)

**Issue JF-1 — CHAPTER/REF MISMATCH (must-fix): Three edges have `evidence_chapter` saying `"asos-sansa-05"` but `evidence_ref` pointing to `asos-sansa-06.md`.**

All three quotes ARE verbatim-correct in `asos-sansa-06.md` at the cited lines. The bug is the chapter label.

Affected edges:

a) `COMMANDS_IN petyr-baelish -> dontos-delivers-hairnet-to-sansa`:
   - Has `evidence_chapter:"asos-sansa-05"`, `evidence_ref:"sources/chapters/asos/asos-sansa-06.md:145"`
   - Fix: change `evidence_chapter` to `"asos-sansa-06"`.

b) `TRIGGERS death-of-joffrey-baratheon -> killing-of-dontos-hollard`:
   - Has `evidence_chapter:"asos-sansa-05"`, `evidence_ref:"sources/chapters/asos/asos-sansa-06.md:145"`
   - Fix: change `evidence_chapter` to `"asos-sansa-06"`. Also note: the evidence_quote `"Ser Dontos the Red was a skin of wine with legs…"` is Littlefinger explaining why Dontos had to be killed AFTER the fact (retrospectively in Sansa VI). The causal direction is not directly stated at this quote — it's an explanation, not a witnessed trigger. But Tier-2 is already assigned and the quote does establish the causal mechanism. Acceptable with Tier-2 as-is.

c) `AGENT_IN lothor-brune -> sansa-s-escape-from-kings-landing`:
   - Has `evidence_chapter:"asos-sansa-05"`, `evidence_ref:"sources/chapters/asos/asos-sansa-06.md:55"`
   - Fix: change `evidence_chapter` to `"asos-sansa-06"`. The quote ("Oswell and Lothor splashed their way ashore") is actually from the Fingers arrival scene in Sansa VI (they've already escaped and are landing), not from the escape itself. The escape scene (Sansa V) has Lothor at the galley (`she saw someone — Ser Lothor Brune stood beside him with a torch` at `asos-sansa-05.md:117`). Either line is valid evidence, but the `evidence_ref` should match the `evidence_chapter`. Two options: (i) use `asos-sansa-05.md:117` ("Ser Lothor Brune stood beside him with a torch") with `evidence_chapter:"asos-sansa-05"`; or (ii) keep `:55` in sansa-06 and fix the chapter label to `"asos-sansa-06"`. Option (i) is the stronger quote for the escape event specifically. Recommend option (i).

---

**Issue JF-2 — VOCAB GAP (must-fix before emit): `RECIPIENT_IN` and `UNWITTING_INSTRUMENT_IN` are NOT in locked vocab.**

The draft correctly flags this in §5 Q5 but the fix must be resolved before emit, not deferred. Fallback options per the draft:

- `dontos-delivers-hairnet-to-sansa` / Sansa role: use `ATTENDS` (weakest; Sansa received the hairnet, she didn't merely attend). Better fallback: the draft's suggestion to use `ATTENDS` works minimally; actually, since the hairnet delivery is the event and Sansa is its recipient, the edge could be omitted (the beat's meaning is captured by the other role edges) or use `VICTIM_IN` on the grounds that Sansa is an unknowing instrument-victim of the delivery.
- `olenna-takes-stone-from-hairnet` / Sansa role: `VICTIM_IN` is the better fallback (Sansa is the instrument-victim whose presence enables the crime), slightly off semantically but defensible.
- **Recommendation for vocab expansion:** `RECIPIENT_IN` is worth adding — it has clear future utility (trial verdicts, gift/bequest events, prophecy recipients). Add to architecture.md before emit with a PR from Matt, then use it. `UNWITTING_INSTRUMENT_IN` is more specialized; defer and use `VICTIM_IN` for this wave.

---

**Issue JF-3 — VOCAB GAP (must-fix before emit): `event.escape` is NOT in locked vocab.**

Confirmed absent from `reference/architecture.md` event-type table. The draft flags this (§5 Flag 4 and §7 checklist item 1).
- **Fix:** Use `event.incident` for `sansa-s-escape-from-kings-landing` (established fallback per the draft). Do not mint with `event.escape`.

---

## Open Design Questions — Recommendations

### Red Wedding: Include Lady Stoneheart beat or close at Robb's death?

**Recommendation: INCLUDE `catelyn-is-resurrected-as-lady-stoneheart` as the arc terminus.**

Rationale:
1. The parent-shape rule explicitly says "post-event consequences attach to the CONSPIRACY parent." The resurrection is the most consequential downstream node — it is what makes the conspiracy narratively incomplete (it spawns a revenge arc).
2. For agent traversal, the most common arc question is "what resulted from the Red Wedding conspiracy?" The answer to that question should include Lady Stoneheart.
3. The resurrection's TRIGGERS provenance is clean and Tier-2 grounded (Beric's Last Kiss mechanism established verbatim in Arya VII; Nymeria retrieval established verbatim in Arya XII; the fact of Catelyn's survival established verbatim in the Epilogue).
4. Closing at Robb's death leaves the graph without a way to reach Lady Stoneheart from the arc entry point. Any agent asking "who survived the Red Wedding conspiracy changed?" gets no answer.

The Lady Stoneheart retribution thread (Frey hangings, Wyman's pies) correctly belongs to a downstream arc and is not included here.

---

### Joffrey: Arc boundary — where does it end?

**Recommendation: INCLUDE `sansa-s-escape-from-kings-landing` as the arc's exit beat (wider boundary).**

Rationale:
1. Littlefinger commissioned both missions in the same operative instruction to Dontos ("lead you from the castle AND make certain you wore your silver hair net" — one sentence, one agent, one commissioning). The escape is part of the operational design, not an afterthought.
2. `killing-of-dontos-hollard` (which the draft already includes) is no more or less "part of the conspiracy" than the escape — Dontos's killing is operational cleanup. If the killing is in scope, the escape is too.
3. Sansa's disappearance is explicitly engineered by Littlefinger to frame Tyrion. This is conspiracy design, not mere downstream consequence — it's integral to "getting away with it."
4. The arc ends cleanly: Sansa reaches the Fingers and Littlefinger reveals the conspiracy. The trail goes cold. Any further Sansa arc at the Eyrie is a different causal chain.

---

### Joffrey: Sansa's "unwitting instrument" role — vocab gap

**Recommendation: Mint `RECIPIENT_IN` and use it; defer `UNWITTING_INSTRUMENT_IN`.**

`RECIPIENT_IN` cleanly captures Sansa's role on `dontos-delivers-hairnet-to-sansa` (she received the object that was the poison vector) without claiming she was harmed or that she acted. It is genuinely additive vocabulary — the graph already has `AGENT_IN`, `VICTIM_IN`, `COMMANDS_IN`, and `ATTENDS`; there is no current type for "entity that receives/bears the object of an event."

Concrete semantics: `sansa-stark RECIPIENT_IN dontos-delivers-hairnet-to-sansa` = Sansa is the party to whom the delivery was made. This is factual, verifiable, and generates useful queries (e.g., "what objects were delivered to Sansa?").

For `olenna-takes-stone-from-hairnet`: use `VICTIM_IN` for Sansa (she's the instrument-victim whose presence enables the crime; the stone is taken FROM her hairnet without her knowledge or consent). The semantics are slightly off ("victim" implies harm; Sansa isn't directly harmed here), but it's the closest available type and the wrongness is minimal — her presence is exploited.

`UNWITTING_INSTRUMENT_IN` could be added in a future vocab session after seeing whether this role recurs. Candidates: Edmure Tully at the Twins (instrument of the lure), Walder III "Walder" at the poisoned-cup (if Joffrey's cupbearer), various other "pawn" roles in ASOIAF conspiracies. Probably merits addition — but not blocking wave-1 emit.

---

## Summary Table — All Issues

| ID | Draft | Type | Severity | Fix |
|---|---|---|---|---|
| RW-1 | Red Wedding | Wrong line number — TRIGGERS frey-bolt-offer TRIGGERS red-wedding cites `:219` for "It must happen" quote; actual line is `:251` | **MUST-FIX** | Change evidence_ref to `asos-catelyn-04.md:251` |
| RW-2 | Red Wedding | Scope violation — `death-of-grey-wind` SUB_BEAT_OF conspiracy parent; should be SUB_BEAT_OF `red-wedding` (happens during massacre) | **MUST-FIX** | Move SUB_BEAT_OF to `red-wedding`; TRIGGERS already correctly scoped |
| RW-3 | Red Wedding | Circular TRIGGERS — sub-beat triggers its own parent (`robb-breaks TRIGGERS red-wedding-conspiracy`) | **MUST-FIX** | Drop this TRIGGERS; replace with `robb-breaks TRIGGERS frey-bolt-offer-edmure-roslin` if cross-beat causation needed |
| RW-4 | Red Wedding | Design-memo deviation — role edges on parent hub contradicts "parent has zero direct role edges" rule | **Matt's call** | Option A: sanction deviation for event.conspiracy type + update design memo. Option B: move to sub-beats. Recommendation: Option A. |
| RW-5 | Red Wedding | Minor: TRIGGERS quote spans :133-:135, cited as :133 only | cosmetic | Optional: extend to :133-135 |
| RW-6 | Red Wedding | Slug name `frey-bolt-offer-edmure-roslin` is awkward | cosmetic | Matt's call |
| JF-1a | Joffrey | Chapter/ref mismatch — `COMMANDS_IN petyr-baelish -> dontos-delivers-hairnet` has chapter sansa-05 but ref sansa-06.md:145 | **MUST-FIX** | Change evidence_chapter to `"asos-sansa-06"` |
| JF-1b | Joffrey | Chapter/ref mismatch — `TRIGGERS death-of-joffrey -> killing-of-dontos` has chapter sansa-05 but ref sansa-06.md:145 | **MUST-FIX** | Change evidence_chapter to `"asos-sansa-06"` |
| JF-1c | Joffrey | Chapter/ref mismatch — `AGENT_IN lothor-brune -> sansa-s-escape` has chapter sansa-05 but ref sansa-06.md:55 | **MUST-FIX** | Either fix chapter to sansa-06, or switch to asos-sansa-05.md:117 ("Ser Lothor Brune stood beside him with a torch") which is stronger evidence for the escape itself |
| JF-2 | Joffrey | `RECIPIENT_IN` / `UNWITTING_INSTRUMENT_IN` not in locked vocab | **MUST-FIX before emit** | Add `RECIPIENT_IN` to architecture.md; use it for Sansa on delivery beat. Use `VICTIM_IN` for Sansa on stone-removal beat. Defer `UNWITTING_INSTRUMENT_IN`. |
| JF-3 | Joffrey | `event.escape` not in locked vocab | **MUST-FIX before emit** | Use `event.incident` for `sansa-s-escape-from-kings-landing` |

---

## Final Notes

**Both drafts show rigorous self-awareness.** The uncertainty flags in §6 (Red Wedding) and the open design questions in §5 (Joffrey) accurately identify the real risks — the review has independently confirmed most of those flags. The main issues (RW-1 wrong line number, JF-1 chapter mismatches) are mechanical mistakes that do not undermine the underlying research quality.

**The Olenna on-page claim (review requirement #5) holds up:** the physical act of touching the hairnet IS on-page in `asos-tyrion-08.md:101` (Tyrion POV, verbatim). The interpretation that she removed the Strangler is retroactively confirmed by Littlefinger in Sansa VI. Tier-2 is correct and well-assigned. No tier change needed.

**The Red Wedding arc's use of role edges on the parent hub (RW-4) is the most significant unresolved design question.** It's not a research error — it's a deliberate deviation from the design memo's stated pattern, with a coherent rationale. Matt should sanction it (or override it) before the mint session proceeds, so the design memo can be updated accordingly.

**Count of must-fix issues:**
- Red Wedding: 3 must-fix (RW-1, RW-2, RW-3) + 1 Matt-call (RW-4)
- Joffrey: 5 must-fix (JF-1a, JF-1b, JF-1c, JF-2, JF-3)
