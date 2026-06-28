# Fresh Verify — WO5K Battles PASS 2 (S164)

Verifier: independent fresh-verify subagent  
Date: 2026-06-28  
Sources checked: `acok-sansa-03.md`, `acok-catelyn-06.md`, `asos-catelyn-02.md`

---

## Line-number key (for audit)

Line numbers in the source files are literal file line numbers including the YAML header block (which occupies lines 1–9 in all three files). The prose begins at line 11.

- `acok-sansa-03:153` → file line 153 = the paragraph with Tyrion's account of Oxcross casualties.
- `acok-sansa-03:157` → file line 157 = Tyrion's "Our forces still hold the stronghold…" sentence.
- `acok-catelyn-06:79` → file line 79 = Maester Vyman's raven-dispatch line.
- `asos-catelyn-02:143` → file line 143 = Robb's narration of the storming + fever.
- `asos-catelyn-02:185` → file line 185 = Robb's Grey Wind kill-tally line.

---

## Per-edge verdicts

| ID | Type | Source → Target | Verdict | One-line reason |
|----|------|-----------------|---------|-----------------|
| E1 | ENABLES | robb-proclaimed-king-in-the-north → battle-of-oxcross | CONFIRM-WITH-NOTE-PATCH | Quote is verbatim and present; edge type honest; antecedent recommendation: keep (see below) |
| E2 | ENABLES | battle-of-oxcross → taking-of-ashemark | CONFIRM | Quote verbatim; Oxcross→Ashemark sequence established by Robb's own words; ENABLES correct |
| E3 | ENABLES | taking-of-ashemark → storming-of-the-crag | CONFIRM | Quote verbatim; Ashemark-as-waypoint to Crag confirmed by Vyman's raven relay logic |
| E4 | COMMANDS_IN | robb-stark → storming-of-the-crag | CONFIRM | "we took it by storm one night" verbatim (line 143); Robb commanded the assault |
| E5 | AGENT_IN | robb-stark → storming-of-the-crag | CONFIRM | "I broke the main gate with a ram" verbatim (line 143) |
| E6 | AGENT_IN | jon-umber-son-of-jon → storming-of-the-crag | CONFIRM-WITH-NOTE-PATCH | Quote verbatim; slug note below |
| E7 | AGENT_IN | walder-frey-son-of-ryman → storming-of-the-crag | CONFIRM-WITH-NOTE-PATCH | Quote verbatim; slug note below |
| E8 | FIGHTS_IN | grey-wind → storming-of-the-crag | CONFIRM | "Grey Wind killed a man at the Crag" verbatim (line 185) |
| E9 | COMMANDS_IN | rolph-spicer → storming-of-the-crag | CONFIRM-WITH-NOTE-PATCH | Quote verbatim; COMMANDS_IN defensible for defending castellan; see below |
| E10 | LOCATED_AT | storming-of-the-crag → crag | CONFIRM | "The Crag was weakly garrisoned, so we took it by storm one night" verbatim (line 143) |
| E11 | HEALS | jeyne-westerling → robb-stark | CONFIRM-WITH-NOTE-PATCH | Quote imprecise; see below |
| E12 | VICTIM_IN | lymond-vikary → battle-of-oxcross | CONFIRM | "along with Ser Lymond Vikary" verbatim (line 153) |
| E13 | FIGHTS_IN | grey-wind → taking-of-ashemark | CONFIRM | "another at Ashemark" verbatim (line 185); read in full: "another at Ashemark, and six or seven at Oxcross" — Crag kill is first, Ashemark second |
| E14 | KILLS | rickard-karstark → stafford-lannister | CONFIRM | "Lord Rickard Karstark drove a lance through his chest" verbatim (line 153); genuine new dyad |

---

## Detailed findings

### E1 — `robb-proclaimed-king-in-the-north ENABLES battle-of-oxcross`

**Cited line (acok-sansa-03:157):**
> "Our forces still hold the stronghold at the Golden Tooth, and they swear he did not pass."

**Verbatim check:** PASS. The exact string appears at line 157 in Tyrion's speech to Sansa: "Our forces still hold the stronghold at the Golden Tooth, and they swear he did not pass."

**Edge-type reasoning (ENABLES vs CAUSES vs PRECEDES):**

ENABLES is honest here. "CAUSES" would imply the crowning mechanically compelled the Oxcross battle — it did not; Robb exercised sovereign offensive initiative. "PRECEDES" would be mere chronology with no causal relationship asserted. ENABLES correctly models: *the status change (sovereign king → free to wage offensive war beyond Riverrun's relief) was the precondition Robb's choice walked through.* Tyrion's own bafflement ("The only mystery is how your brother reached him. Our forces still hold the stronghold at the Golden Tooth, and they swear he did not pass") establishes the offensive reach as an autonomous, surprising, freely-chosen act — exactly what ENABLES implies.

**Antecedent recommendation:** KEEP `robb-proclaimed-king-in-the-north`. The curator's reasoning is sound: `battle-of-the-camps ENABLES robb-proclaimed-king-in-the-north` already exists, so chaining from the crowning maintains a clean linear spine (Camps → Crowning → Oxcross) rather than forking both Camps and Crowning as separate antecedents to Oxcross. `battle-of-the-camps` would be a *more distal* precondition; the crowning is the direct status-unlock that licensed the westward offensive. Keep as-is.

**NOTE-PATCH:** The quote is the right passage but is *inferential anchor* evidence (Tyrion's surprise at the route), not a direct cause-sentence. The proposed note already says Tier-2 inferential. The patch recommendation: the `note` field should explicitly call out that the anchor establishes *offensive reach / autonomous choice*, not a causal arrow from the crowning per se. Tier-2 is correctly applied. No rejection warranted.

**VERDICT: CONFIRM-WITH-NOTE-PATCH** (note only — no data field needs changing; tier already set to tier-2).

---

### E2 — `battle-of-oxcross ENABLES taking-of-ashemark`

**Cited line (acok-sansa-03:153):**
> "Knights were trampled to death in their pavilions, and the rabble woke in terror and fled, casting aside their weapons to run the faster."

**Verbatim check:** PASS. The exact string "Knights were trampled to death in their pavilions, and the rabble woke in terror and fled" is present at line 153.

**Sequence check:** The Oxcross→Ashemark sequence is confirmed by Robb's own account in asos-catelyn-02:185: "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross." (Listed in inverse order of recency but all three battles named.) The quote anchors Oxcross's character (Stafford's raw host destroyed), supporting the inference that its destruction opened the Westerlands interior. The wiki prose cited in the note ("After the Battle of Oxcross … takes castles … including Ashemark") is consistent with the local text.

**ENABLES vs CAUSES:** Correct. The Oxcross victory was the *military precondition* (destroyed the only organized Lannister force blocking the interior); Robb freely chose to exploit it by raiding deeper. Not CAUSES, not PRECEDES.

**VERDICT: CONFIRM**

---

### E3 — `taking-of-ashemark ENABLES storming-of-the-crag`

**Cited line (acok-catelyn-06:79):**
> "At last word he was marching toward the Crag, the seat of House Westerling," said Maester Vyman. "If I dispatched a raven to Ashemark, it may be that they could send a rider after him."

**Verbatim check:** The proposed quote is "At last word he was marching toward the Crag, the seat of House Westerling" — PASS. This exact phrase appears at line 79.

**Sequence confirmation:** The raven-relay logic ("dispatch a raven *to Ashemark*, it may be that they could send a rider after him") places Ashemark between Riverrun and the Crag as a waypoint where messengers can be relayed. This confirms Ashemark was taken (it's a safe Stark-controlled relay point) and that the Crag was the *next* objective after it.

**ENABLES correctness:** Taking Ashemark positioned the host to march toward the Crag (Ashemark as waypoint/staging, not as cause of the storming). ENABLES is the right type: the raid through Ashemark enabled the host to reach and attack the Crag. Tier-2 inferential — correct.

**VERDICT: CONFIRM**

---

### E4 — `robb-stark COMMANDS_IN storming-of-the-crag`

**Cited line (asos-catelyn-02:143):**
> "The Crag was weakly garrisoned, so we took it by storm one night. Black Walder and the Smalljon led scaling parties over the walls, while I broke the main gate with a ram."

**Verbatim check for E4 quote ("we took it by storm one night"):** PASS. Exact string present at line 143.

**COMMANDS_IN:** Correct. Robb led the assault ("we took it") and it is distinct from his personal gate-breaking role (E5). Dual role pattern is a known valid graph pattern.

**VERDICT: CONFIRM**

---

### E5 — `robb-stark AGENT_IN storming-of-the-crag`

**Verbatim check ("I broke the main gate with a ram"):** PASS. Exact string at line 143.

**VERDICT: CONFIRM**

---

### E6 — `jon-umber-son-of-jon AGENT_IN storming-of-the-crag`

**Verbatim check ("Black Walder and the Smalljon led scaling parties over the walls"):** PASS. Exact string at line 143.

**Slug check for jon-umber-son-of-jon:** "The Smalljon" is the Greatjon's son. The candidates note confirms: "the Smalljon (= jon-umber-son-of-jon, the Greatjon's son — NOT jon-umber)." The slug `jon-umber-son-of-jon` correctly disambiguates from `jon-umber` (the Greatjon himself). In the hall scene (line 27), "the Greatjon and his son" are both present, confirming the son exists as a distinct entity. Slug is correct; the distinction from the Greatjon node (`jon-umber`) is necessary and accurate.

**NOTE-PATCH:** No data change needed. Minor documentation note: the Greatjon's given name is Jon Umber, so "the Smalljon" is also Jon Umber (son). The slug `jon-umber-son-of-jon` is the canonical disambiguator. This is already handled correctly.

**VERDICT: CONFIRM-WITH-NOTE-PATCH** (slug correct; note is clarificatory only)

---

### E7 — `walder-frey-son-of-ryman AGENT_IN storming-of-the-crag`

**Verbatim check:** Same line as E6 — PASS.

**Slug check for walder-frey-son-of-ryman:** "Black Walder" is indeed Walder Frey's great-grandson via Ryman. Robb himself names "Black Walder" at line 155 of asos-catelyn-02: "Black Walder … went so far as to say that his sisters would not be loath to wed a widower." The candidates note flags: "walder-frey-son-of-ryman (the alias-bearing wiki-canonical node — NOT the black-walder-frey twin; node-dup flagged for small-fixes)." This is a known deferred dup issue; the slug used here is the wiki-canonical node. The edge itself is correct regardless of which slug wins the eventual dedup.

**NOTE-PATCH:** No data change needed. The node-dup flag is correctly deferred to small-fixes.

**VERDICT: CONFIRM-WITH-NOTE-PATCH** (slug tentatively correct per current wiki-canonical node; dup resolution deferred)

---

### E8 — `grey-wind FIGHTS_IN storming-of-the-crag`

**Cited line (asos-catelyn-02:185):**
> "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross."

**Verbatim check ("Grey Wind killed a man at the Crag"):** PASS. Exact string at line 185.

**FIGHTS_IN vs KILLS:** FIGHTS_IN is the right aggregate participation type here (there is no named victim at the Crag, so KILLS would require a target; FIGHTS_IN captures active participation without a named victim node).

**VERDICT: CONFIRM**

---

### E9 — `rolph-spicer COMMANDS_IN storming-of-the-crag`

**Cited line (asos-catelyn-02:143):**
> "I took an arrow in the arm just before Ser Rolph yielded us the castle."

**Verbatim check ("I took an arrow in the arm just before Ser Rolph yielded us the castle"):** PASS. Exact string at line 143.

**COMMANDS_IN for a defending castellan who yielded:** This is the most interpretively interesting edge in the roster cluster. COMMANDS_IN is applied on the defending side — Rolph Spicer "was castellan at the Crag when we took it" (line 95: Robb's introduction of Ser Rolph to Catelyn). As castellan he held formal command of the garrison, even a weak one. Yielding IS the final command act of a garrison commander. The edge direction is source=rolph-spicer, target=storming-of-the-crag, which is correct: he COMMANDS_IN the event (on the losing side). The curator's note already flags "note the side: this is the losing/defending command."

Is COMMANDS_IN the right type for a yielding castellan? It models his role as the decision-maker who commanded the defense (however briefly) and chose to yield — which is a command act. The alternative would be AGENT_IN, but that undersells his specific decision-making authority. COMMANDS_IN + the note is defensible and accurate. The edge is complementary to Robb's attacking COMMANDS_IN (E4), which is an established pattern.

**NOTE-PATCH:** The note correctly flags the side distinction. A future query layer will need to filter on side; for now the note is adequate documentation.

**VERDICT: CONFIRM-WITH-NOTE-PATCH** (correct; note about defending side is present and sufficient)

---

### E10 — `storming-of-the-crag LOCATED_AT crag`

**Verbatim check ("The Crag was weakly garrisoned, so we took it by storm one night"):** PASS. Line 143.

**LOCATED_AT direction:** source=event, target=location. Correct.

**VERDICT: CONFIRM**

---

### E11 — `jeyne-westerling HEALS robb-stark`

**Proposed quote:** "she nursed me until the fever passed"

**Actual text at asos-catelyn-02:143:**
> "Jeyne had me taken to her own bed, and she nursed me until the fever passed."

**Verbatim check:** The proposed quote "she nursed me until the fever passed" is a SUBSTRING of the sentence "she nursed me until the fever passed" — specifically, it is a verbatim substring starting mid-sentence. The full sentence reads: "Jeyne had me taken to her own bed, and she nursed me until the fever passed."

**Issue:** The quote is verbatim as a substring, but omits the crucial prior clause that names the healer's identity ("Jeyne had me taken to her own bed"). The evidence quote as written ("she nursed me until the fever passed") does not name Jeyne — a reader without context could not tell who "she" is. The HEALS source is `jeyne-westerling`, so the edge itself is correctly attributed, but the evidence_quote loses the referential anchor.

**NOTE-PATCH:** Recommended fix: extend the quote to the full sentence: "Jeyne had me taken to her own bed, and she nursed me until the fever passed." This is still a single verbatim contiguous sentence from line 143 and makes the healer explicit.

**HEALS type:** Correct direction (source=healer, target=healed). Tier-1 book-verbatim is appropriate.

**VERDICT: CONFIRM-WITH-NOTE-PATCH** (extend quote to full sentence to make "she" referentially unambiguous)

---

### E12 — `lymond-vikary VICTIM_IN battle-of-oxcross`

**Cited line (acok-sansa-03:153):**
> "Ser Rubert Brax is also dead, along with Ser Lymond Vikary, Lord Crakehall, and Lord Jast."

**Verbatim check ("along with Ser Lymond Vikary"):** PASS. The phrase "along with Ser Lymond Vikary" is a verbatim substring of the full sentence at line 153.

**VICTIM_IN:** Correct — Lymond Vikary is named among the dead at Oxcross.

**VERDICT: CONFIRM**

---

### E13 — `grey-wind FIGHTS_IN taking-of-ashemark`

**Cited line (asos-catelyn-02:185):**
> "Grey Wind killed a man at the Crag, another at Ashemark, and six or seven at Oxcross."

**Verbatim check ("another at Ashemark"):** PASS. The phrase "another at Ashemark" is a verbatim substring of line 185.

**Note on quote completeness:** The proposed quote "another at Ashemark" is minimal. Read in context, "another" refers to another man killed (Grey Wind killed one at the Crag, *another* at Ashemark). The referent is clear from context. However, the minimum extractable quote that makes sense standalone would be: "Grey Wind killed a man at the Crag, another at Ashemark." The current quote is technically verbatim; the fuller form is more auditable.

**VERDICT: CONFIRM** (quote is verbatim; longer form would be cleaner but not required)

---

### E14 — `rickard-karstark KILLS stafford-lannister`

**Cited line (acok-sansa-03:153):**
> "Lord Rickard Karstark drove a lance through his chest."

**Verbatim check:** PASS. Exact string "Lord Rickard Karstark drove a lance through his chest" appears at line 153 in Tyrion's account of Oxcross.

**Full context from line 153:**
> "Ser Stafford was slain as he chased after a horse. Lord Rickard Karstark drove a lance through his chest."

The KILLS edge correctly identifies Stafford as the victim (the prior sentence names him). The proposed source (`rickard-karstark`) and target (`stafford-lannister`) are correct.

**New dyad check:** The candidate note states "no KILLS/KILLED_BY/EXECUTES edge for Stafford existed." This is a genuine gap — Stafford's VICTIM_IN battle-of-oxcross existed, but no actor was assigned the kill. Rickard's AGENT_IN battle-of-oxcross also existed (general participant role). The KILLS edge adds a specific dyadic kill relationship, distinct from both. Pattern is identical to the established Jaime KILLS dyads that coexist with VICTIM_IN roles, which is a known valid pattern.

**VERDICT: CONFIRM**

---

## SUMMARY

| Verdict | Count | IDs |
|---------|-------|-----|
| CONFIRM | 8 | E2, E4, E5, E8, E10, E12, E13, E14 |
| CONFIRM-WITH-NOTE-PATCH | 6 | E1, E6, E7, E9, E11, (E13 borderline) |
| REJECT | 0 | — |

**Total: 14 confirmed (0 rejected). 6 note patches recommended.**

### Note-patch summary (no data rejections — all patches are minor):

| ID | Patch |
|----|-------|
| E1 | Note should explicitly state the quote establishes *offensive autonomous choice*, not causal mechanism from crowning. Tier-2 already correct. |
| E6 | No data change; clarificatory note: Smalljon slug `jon-umber-son-of-jon` is correct and necessary to distinguish from Greatjon `jon-umber`. |
| E7 | No data change; node-dup (`walder-frey-son-of-ryman` vs `black-walder-frey`) remains correctly flagged for deferred small-fixes. |
| E9 | No data change; note about defending/losing-side command role is present and sufficient. |
| E11 | **Extend quote** from "she nursed me until the fever passed" → "Jeyne had me taken to her own bed, and she nursed me until the fever passed" to make the healer referentially explicit. Single contiguous sentence, still verbatim. |
| E13 | Quote "another at Ashemark" is minimally verbatim; optional upgrade to "Grey Wind killed a man at the Crag, another at Ashemark" for standalone readability. |

### E1 antecedent verdict (explicit):

**KEEP `robb-proclaimed-king-in-the-north` as the antecedent.** The alternative (`battle-of-the-camps`) is the more distal precondition; the crowning is the direct status-unlock that licenses the westward offensive. The linear spine `battle-of-the-camps → robb-proclaimed-king-in-the-north → battle-of-oxcross` is cleaner than a fork. No re-point recommended.

---

*All quotes verified against file line numbers. Sources: `acok-sansa-03.md` (line 153, 157), `acok-catelyn-06.md` (line 79), `asos-catelyn-02.md` (lines 143, 185, 95).*
