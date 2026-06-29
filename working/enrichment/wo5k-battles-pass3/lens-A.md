# WO5K-Battles Pass 3 — Lens A: Spicer-Betrayal Mechanism
<!-- Session: S166 | Date: 2026-06-28 | Model: claude-sonnet-4-6 -->

**Task:** Propose graph edges (and assess one candidate event node) for the Spicer-betrayal mechanism
revealed in AFFC: Tywin Lannister used Lady Sybell Spicer (née Westerling) to engineer Robb Stark's
fatal marriage from within. All quotes re-read and line-verified.

---

## Proposed new node

**Recommendation: YES — mint the event node.**

**Slug:** `jeyne-westerling-kept-barren`
**Type:** `event.deception`
**Display name:** Sybell Spicer Keeps Jeyne Westerling Barren

**Body (book-grounded only; mechanism/moon-tea EXCLUDED — GATED):**
On Tywin Lannister's orders, Lady Sybell Spicer ensured that Jeyne Westerling bore Robb Stark no
child during their marriage. Sybell confirmed this directly to Jaime Lannister at Riverrun after
Robb's death: "I made certain of that, as your lord father bid me." The act was part of the broader
understanding between Sybell and Tywin; a child would have extended the political threat of the
Young Wolf's line beyond his death. The specific means Sybell used are not stated in the published
books.

**Role edges on this node:**
- `sybell-spicer AGENT_IN jeyne-westerling-kept-barren`
- `jeyne-westerling VICTIM_IN jeyne-westerling-kept-barren`
- `tywin-lannister COMMANDS_IN jeyne-westerling-kept-barren`

**Why mint it:** Gives Jeyne a victim anchor, gives `COMMANDS_IN` a target that isn't Sybell's person
(Tywin commands the act, not the person), and gives the foreshadowing edge below a clean, specific
target rather than the broad marriage event. The book evidence for the act itself (line 79) is
unambiguous Tier-1 canon. The mechanism remains GATED.

---

## Proposed edges

### 1. MANIPULATES (Tywin → Sybell)

```
MANIPULATES | tywin-lannister | sybell-spicer | AFFC | affc-jaime-07 | TIER-1 | qualifier: via_promise | verify: false
```

**Primary quote (line 79):** `"I made certain of that, as your lord father bid me."`
affc-jaime-07:79

**Corroborating quote (line 81, the reward statement):** `"House Westerling has its pardon, and your
brother Rolph has been made Lord of Castamere."`
affc-jaime-07:81

**Corroborating quote (line 83, the marriage promise):** `"Your lord father promised me worthy
marriages for Jeyne and her younger sister."`
affc-jaime-07:83

**Qualifier rationale:** The lever Tywin used was a bundle of promised rewards — House Westerling's
pardon, Castamere for Rolph, and noble marriages for the Westerling daughters. `via_promise` is the
best enum fit. `via_bribe` was considered but `via_promise` is more precise (the rewards were pledged
in advance as inducements, not cash-in-hand payment after the fact). The bribe/promise line is blurry;
`via_promise` wins because Sybell confirms the rewards were *bid* to her (past tense by Jaime at line
81 as settled facts), fitting "I will do X if you do Y."

**Rationale:** Tywin did not deal with Sybell directly on-page; the channel is confirmed by Sybell's
own words ("your lord father bid me") and by Jaime confirming the rewards have already been
delivered (line 81). The mechanism was the promise package (pardon + Castamere + marriages). Distinct
from the existing `sybell-spicer CONSPIRES_WITH tywin-lannister` dyad — this names Tywin as the
*actor* using Sybell as an instrument, not peers conspiring.

---

### 2. BETRAYS (Sybell → Robb)

```
BETRAYS | sybell-spicer | robb-stark | AFFC | affc-jaime-07 | TIER-1 | qualifier: none | verify: false
```

**Primary quote (line 79):** `"I made certain of that, as your lord father bid me."`
affc-jaime-07:79

**Corroborating characterization (line 97 — Jaime's internal voice):**
`"Jaime had to wonder how much Lord Gawen knew about his wife's scheming."`
affc-jaime-07:97

**Rationale:** Sybell was the mother-in-law of Robb Stark (her king and good-son) and lived under his
protection after the Crag fell. She owed him the minimum loyalty a subject owes a king, and as a
family member she owed him more. Instead she actively sabotaged his marriage on Tywin's orders
(ensuring no heir, suppressing Robb's reproductive line). This is a distinct edge from the existing
`sybell-spicer CONSPIRES_WITH tywin-lannister` (which captures the Sybell↔Tywin dyad); BETRAYS names
Robb as the *victim* of that conspiracy. The verb is confirmed by the chapter's framing — Jaime calls
it "scheming," Jeyne calls her mother's actions an injustice, and the chapter positions Sybell as the
betrayer throughout. Tier-1: Sybell's own words confirm the act.

---

### 3. AGENT_IN (Sybell → jeyne-westerling-kept-barren)

```
AGENT_IN | sybell-spicer | jeyne-westerling-kept-barren | AFFC | affc-jaime-07 | TIER-1 | qualifier: none | verify: false
```

**Quote (line 79):** `"I made certain of that, as your lord father bid me."`
affc-jaime-07:79

**Rationale:** Sybell is the active agent of the keeping-barren event. "I made certain of that" is
unambiguous first-person agency.

---

### 4. VICTIM_IN (Jeyne → jeyne-westerling-kept-barren)

```
VICTIM_IN | jeyne-westerling | jeyne-westerling-kept-barren | AFFC | affc-jaime-07 | TIER-1 | qualifier: none | verify: false
```

**Quote (line 73):** `"It was mine. You had no right. Robb had it made for me. I loved him."`
affc-jaime-07:73

**Rationale:** Jeyne is the direct object of Sybell's covert act. Quote at line 73 captures her
distress and her mother's prior aggression (crown removal), establishing the mother-as-persecutor
dynamic. The kept-barren act itself is stated by Sybell (line 79) with Jeyne's involvement as object
implicit ("She is not [pregnant]" → "I made certain of that"). Tier-1.

---

### 5. COMMANDS_IN (Tywin → jeyne-westerling-kept-barren)

```
COMMANDS_IN | tywin-lannister | jeyne-westerling-kept-barren | AFFC | affc-jaime-07 | TIER-1 | qualifier: none | verify: false
```

**Quote (line 79):** `"I made certain of that, as your lord father bid me."`
affc-jaime-07:79

**Corroborating (line 67 — Jaime's internal framing):**
`"Tywin Lannister was not a man to overlook such details."`
affc-jaime-07:67

**Rationale:** "Your lord father bid me" directly attributes the command to Tywin. Jaime's internal
gloss at line 67 ("not a man to overlook such details") reinforces that this was deliberate
orchestration from Tywin, not Sybell's freelance initiative. Tier-1.

Note on line 67: affc-jaime-07:67 reads: `"She is not," said Lady Sybell, as her daughter struggled
to escape. "I made certain of that, as your lord father bid me." Jaime nodded. Tywin Lannister was
not a man to overlook such details.` — The "such details" line is line 79's immediate sequel; it
appears on line 79–80 as one prose block. Re-verified: the full passage is at lines 79–80 in the
file. The Tywin characterization line is actually line 80: `"Jaime nodded. Tywin Lannister was not a
man to overlook such details."` Use affc-jaime-07:80 for that clause.

**Corrected corroborating cite:** `"Tywin Lannister was not a man to overlook such details."`
affc-jaime-07:80

---

### 6. FORESHADOWS (Grey Wind → jeyne-westerling-kept-barren)

```
FORESHADOWS | grey-wind | jeyne-westerling-kept-barren | ASOS | asos-catelyn-02 | TIER-2 | qualifier: none | verify: true
```

**Quote (line 189):** `"He bares his teeth every time Ser Rolph comes near him."`
asos-catelyn-02:189

**Rationale:** Grey Wind's reaction is directed at Rolph Spicer (Sybell's brother, castellan of the
Crag). The wolf's supernatural intuition, as Catelyn reads it, connects to the broader Spicer family
treachery — Rolph was the first Spicer in Robb's circle and a visible representative of that lineage.
The foreshadowed event is the Spicer-engineered sabotage (jeyne-westerling-kept-barren), which is the
mechanism of the Westerling marriage trap. Target is the new event node rather than the broader
marriage event because that's what Grey Wind's nose is effectively pointing at: the hidden betrayal
embedded in the marriage, not the marriage itself.

**FORESHADOWS target selection note:** The existing spine already has `robb-weds-jeyne-westerling`
as a node; pointing to the new `jeyne-westerling-kept-barren` node gives the foreshadowing a more
precise target (the covert sabotage, not the marriage itself) and avoids colliding with any existing
wolf-foreshadowing edge on the marriage node. `verify: true` because foreshadowing is interpretive.

---

### 7. NON-INVOLVEMENT edge: UNINVOLVED_IN (Raynald → jeyne-westerling-kept-barren)

**Recommendation: SKIP for now.** UNINVOLVED_IN is not a standard edge type in the locked vocabulary.
The fact is important but better handled as a qualifier or prose note on the event node body than as a
novel edge type. See Dropped section below.

---

### 8. Additional clean edge: RECEIVES_REWARD (Sybell / Rolph — via existing nodes)

The Castamere reward is already in the graph (`rolph-spicer HOLDS_TITLE lord-of-castamere`). The
marriage promises to Jeyne and her sister are NOT in the graph. Propose:

```
RECEIVES_PROMISE | sybell-spicer | jeyne-westerling | AFFC | affc-jaime-07 | TIER-1 | qualifier: none | verify: false
```
**Wait** — `RECEIVES_PROMISE` is not in the locked vocabulary. This should not be minted.

**Alternative: PROMISED_TO as a loose attribute on the event node body.** The marriages Tywin promised
are captured in the event node body above and in the existing node prose for Sybell. No new edge
proposed here — the Castamere reward web already covers the material in the dedup list.

---

## Dedup — found but not re-proposed

The following relationships were confirmed present in the chapter text but are marked as already in the
graph per the task brief:

1. **`sybell-spicer CONSPIRES_WITH tywin-lannister`** — Sybell's own words (line 79) confirm this.
   Already exists (Tier-1). Not re-proposed.

2. **`rolph-spicer HOLDS_TITLE lord-of-castamere`** and related Castamere reward edges — confirmed at
   line 81. Already exist. Not re-proposed.

3. **`grey-wind OPPOSES rolph-spicer`** — confirmed at asos-catelyn-02:189. Already exists. Not
   re-proposed. (Note: the FORESHADOWS edge proposed above is distinct — it names the treachery event
   as target, not Rolph personally.)

4. **Marriage spine** (`storming-of-the-crag ENABLES robb-weds-jeyne-westerling`, etc.) — confirmed
   by overall chapter context. Already exist.

5. **`sybell-spicer COMMANDS jeyne-westerling`** — implied by line 79 and the crown-taking at line 71.
   Already exists.

6. **`gawen-westerling SPOUSE_OF sybell-spicer`** — confirmed by line 101 (affc-jaime-05) and line 97
   (affc-jaime-07 "Lord Gawen"). Already exists.

---

## Dropped

**Raynald Westerling non-involvement as a named edge.** Line 87: `"Raynald knew nought of any . . .
of the understanding with your lord father."` This is clean book canon and worth noting, but
`UNINVOLVED_IN` is not in the locked vocabulary, and a denial-of-involvement is an awkward graph
primitive. Better handled: add a prose note to the `raynald-westerling` node (or the event node body)
citing affc-jaime-07:87. NOT proposed as a novel edge type — that would require a worklog Active
Decision to add to the vocabulary.

**Rolph Spicer as co-conspirator.** Rolph is Sybell's brother and was castellan at the Crag when it
fell (asos-catelyn-02:95, affc-jaime-05:101). He is the proximate Spicer that Grey Wind reacted to,
and he received Castamere. But the chapter does NOT state Rolph knew about or participated in the
"understanding" — Sybell presents this as her own arrangement with Tywin. Raynald's non-knowledge
(line 87) does not prove Rolph's non-knowledge, but it also does not confirm his involvement. Tywin
would have worked through Sybell alone (cleaner chain of control). DROPPED: no edge connecting Rolph
to the kept-barren event — evidence insufficient.

**`ENABLES` edge from `jeyne-westerling-kept-barren` to `red-wedding-conspiracy`.** The causal logic
is: no heir from Robb → continued Lannister military pressure / no incentive to preserve Robb → Red
Wedding proceeds. But the chapter does not make this causal chain explicit; it is a plausible inference,
not a stated connection. The ENABLES chain on the marriage spine already captures the mechanism
(`robb-weds-jeyne-westerling TRIGGERS red-wedding-conspiracy`). Adding a second ENABLES from the
kept-barren event would be duplicative and the causal link is analytical, not book-stated. DROPPED.

**Jeyne's torn mourning clothes as a `MOURNS` edge.** Line 111 (affc-jaime-07): Jeyne rides with
downcast eyes, clothes torn as mourning. Clear characterization but `MOURNS` already implied by
`robb-stark SPOUSE_OF jeyne-westerling`. Dropped as redundant.

---

## Harvest

Notable finds from these chapters, flagged for the harvest queue:

- **affc-jaime-07:69** — Appearance: Jeyne Westerling described in detail ("willowy girl, no more
  than fifteen or sixteen... chestnut curls... soft brown eyes of a doe... breasts the size of
  apples"). First-class appearance extract for `jeyne-westerling` node.

- **affc-jaime-07:71** — Object: Sybell Spicer described wearing "a necklace of golden seashells"
  (house sigil as jewelry). Appearance/object detail for `sybell-spicer` node.

- **affc-jaime-07:93** — Character: Joy Hill identified as Gerion Lannister's natural daughter
  ("my late uncle Gerion's natural daughter"). Relationship: `joy-hill CHILD_OF gerion-lannister`
  (possible node gap — Joy Hill may not be in the graph).

- **affc-jaime-07:97** — Quote: Jaime calls Sybell "the son of some scheming turncloak bitch"
  (actually directed at Rolph, context: "No more than I want Joy to marry the son of some scheming
  turncloak bitch"). Load-bearing characterization of the Spicer treachery from Jaime's POV.

- **affc-jaime-05:101** — Relationship: Lord Gawen Westerling is held captive at Seagard by Jason
  Mallister. `gawen-westerling PRISONER_OF jason-mallister` (check if this edge exists).

- **asos-catelyn-02:95** — Introduce moment: Robb formally presents all the Westerlings + Sybell +
  Rolph to Catelyn in the Great Hall. Rich character description paragraph (Raynald: "young, lean,
  rough-hewn... thick mop of chestnut hair"). Appearance for `raynald-westerling`.

- **asos-catelyn-05:29** — Key passage: Catelyn reflects "Grey Wind was at the king's side once more.
  Where he belongs." after Rolph's dispatch. Strong narratorial commentary on the wolf's protective
  function. Quote-worthy for the `grey-wind` node.
