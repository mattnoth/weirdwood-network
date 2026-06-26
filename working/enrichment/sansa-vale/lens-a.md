# Lens A — Sansa / Vale Arc: Spine + Secondary Sub-Arcs
# Date: 2026-06-25
# Source chapters: asos-sansa-05, asos-sansa-06, asos-sansa-07, affc-sansa-01, affc-alayne-01, affc-alayne-02

---

## PROPOSED NEW NODES

### NODE-1: `death-of-lysa-arryn`
- **Name:** Death of Lysa Arryn
- **Type:** event.death
- **Rationale:** Pivotal POV-confirmed murder — Littlefinger pushes Lysa through the Moon Door with the words "Only Cat." This is the axle of the entire Vale arc: it removes Sansa's protector, triggers the framing of Marillion, creates the power vacuum that enables the Lords Declarant confrontation, and is the moment LF's control over the Vale is fully consolidated. Confirmed by multiple witnesses including Marillion (gasps "You … you …") and Sansa. Requires its own event node; far too consequential to model as an edge alone.

### NODE-2: `sansa-adopts-alayne-stone-identity`
- **Name:** Sansa adopts the Alayne Stone identity
- **Type:** event.deception
- **Rationale:** LF's instructions aboard the Merling King constitute a discrete deception event: he names the cover story (bastard daughter, Braavosi mother, raised by the Faith), assigns a new name, and Sansa internalizes it as her primary self-presentation for the rest of the series. This is the formative identity-creation moment; it is distinct from individual instances of being-called-Alayne. Used as the origin node for the DISGUISED_AS cross-identity edge from `sansa-stark` to `alayne-stone-identity` (see dedup notes — "Alayne Stone" is already an alias on `sansa-stark`, so this event explains the genesis of that alias).

### NODE-3: `littlefinger-bribes-nestor-royce-with-gates-of-the-moon`
- **Name:** Littlefinger bribes Nestor Royce with the Gates of the Moon
- **Type:** event.deception / event.incident
- **Rationale:** LF presents Nestor with a forged (or at minimum, unauthorised) grant making the Keepership hereditary, signed by himself as Lord Protector rather than by Robert Arryn. This is a distinct manipulative act that splits Nestor from the Lords Declarant coalition and secures LF's political survival. The self-incriminating signature is a deliberate leverage device ("if you are removed, Lord Nestor's claim … will suddenly be called into question") — textually explicit and worth capturing as an event node because it anchors a MANIPULATES edge with a distinct mechanism.

### NODE-4: `trial-of-petyr-baelish-before-the-lords-declarant`
- **Name:** Trial of Petyr Baelish before the Lords Declarant
- **Type:** event.trial (or event.confrontation)
- **Rationale:** Six Lords Declarant climb the Eyrie to demand LF's removal, threatening military force. Lyn Corbray draws Lady Forlorn. LF negotiates a one-year reprieve. This is a sustained political confrontation with multiple named actors, a near-outbreak of violence, and a concrete settlement — it merits its own event node rather than being flattened into a single edge.

### NODE-5: `harry-the-heir-betrothal-plan`
- **Name:** Harry the Heir betrothal plan
- **Type:** event.betrothal (or event.conspiracy)
- **Rationale:** LF's plan to betroth "Alayne Stone" to Harrold Hardyng, then reveal her as Sansa Stark at the wedding to rally the Vale lords to retake Winterfell. This is explicitly LF's long-term endgame — not yet executed as of these chapters, but the plan itself is a discrete event (the contract is made with Lady Waynwood; the reveal is planned for the future). Capturing it as a node allows the arc to extend forward into TWOW without requiring unpublished material.

---

## SPINE EDGES (causal skeleton)

All edges are Tier 1 (direct POV text) unless marked Tier 2.

---

### 1. CAUSES: `littlefinger-smuggles-sansa-out-of-kings-landing` → `death-of-dontos-hollard`
*Note: `death-of-dontos-hollard` may already exist as a node; if not, flag as a missing node. The murder is POV-confirmed in asos-sansa-05.*

Actually Dontos's death is the immediate consequence of the smuggling operation, but more precisely: LF executes him as part of the same operation. Model this as:

**`petyr-baelish` KILLS `dontos-hollard`**
- Quote: "Ser Lothor dipped his torch. Three men stepped to the gunwale, raised crossbows, fired. One bolt took Dontos in the chest as he looked up, punching through the left crown on his surcoat."
- Cite: `sources/chapters/asos/asos-sansa-05.md:127`
- Tier: 1
- Rationale: POV-direct, Lothor acts on LF's command ("Ser Lothor, the reward"). KILLS requires the actor; LF is the orderer. Consider also: `lothor-brune` AGENT_IN `death-of-dontos` (Lothor physically fires, or orders the bolt). Since KILLS is available and LF directly commands it, the principal chain reads as LF KILLS via Lothor. Flag for COMMANDS_IN vs. KILLS disambiguation.

---

### 2. ENABLES: `littlefinger-smuggles-sansa-out-of-kings-landing` → `sansa-adopts-alayne-stone-identity`
- Quote: "Varys has informers everywhere. If Sansa Stark should be seen in the Vale, the eunuch will know within a moon's turn … So we shall tell Lysa's people that you are my natural daughter."
- Cite: `sources/chapters/asos/asos-sansa-06.md:105`
- Tier: 1
- Rationale: The escape from KL is the precondition that necessitates the false identity. ENABLES (precondition) is the correct type.

---

### 3. CAUSES: `sansa-adopts-alayne-stone-identity` → `wedding-of-petyr-baelish-and-lysa-arryn`
- Tier: 2 (interpretive)
- Rationale: The identity construction is the vehicle by which Sansa is introduced to Lysa as Alayne, making the wedding feasible — if Sansa were known as Sansa Stark, Lysa would not have accepted the arrangement quietly. However, the causal arrow here is indirect; ENABLES is more precise than CAUSES.

**ENABLES: `sansa-adopts-alayne-stone-identity` → `wedding-of-petyr-baelish-and-lysa-arryn`**
- Quote: "Lysa will not come alone. Before she arrives, we must be clear on who you are."
- Cite: `sources/chapters/asos/asos-sansa-06.md:101`
- Tier: 1
- Rationale: The identity deception is explicitly constructed to precede and enable Lysa's arrival and marriage.

---

### 4. CAUSES: `wedding-of-petyr-baelish-and-lysa-arryn` → `death-of-lysa-arryn`
- Quote: "'Only Cat.' He gave her a short, sharp shove. Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone."
- Cite: `sources/chapters/asos/asos-sansa-07.md:301-303`
- Tier: 1
- Rationale: The marriage places Lysa and LF in the High Hall together; her jealousy over LF's kiss of Sansa triggers the confrontation that ends in her murder. The wedding is the direct causal precursor.

**Role edges on `death-of-lysa-arryn`:**
- `petyr-baelish` AGENT_IN `death-of-lysa-arryn`
  - Quote: "'Only Cat.' He gave her a short, sharp shove."
  - Cite: `sources/chapters/asos/asos-sansa-07.md:301`
  - Tier: 1
- `lysa-arryn` VICTIM_IN `death-of-lysa-arryn`
  - Quote: "Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone."
  - Cite: `sources/chapters/asos/asos-sansa-07.md:303`
  - Tier: 1
- `sansa-stark` WITNESS_IN `death-of-lysa-arryn`
  - Quote: "Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone. She never screamed."
  - Cite: `sources/chapters/asos/asos-sansa-07.md:303`
  - Tier: 1 — Sansa is explicitly present, physically adjacent, and is dragged away from the Moon Door seconds before. The text shows her seeing the death.
- `marillion` WITNESS_IN `death-of-lysa-arryn`
  - Quote: "Marillion gasped, 'You … you …'"
  - Cite: `sources/chapters/asos/asos-sansa-07.md:305`
  - Tier: 1 — Marillion witnesses and reacts; this is the direct basis for the framing scheme.
- `moon-door` — attach as location. NEEDS_VOCAB: no `OCCURS_AT` edge type confirmed in locked vocab. Flag for vocab expansion or use a note field.

**Additional edge on the murder event:**
- `petyr-baelish` KILLS `lysa-arryn`
  - Quote: "'Only Cat.' He gave her a short, sharp shove."
  - Cite: `sources/chapters/asos/asos-sansa-07.md:301`
  - Tier: 1

---

### 5. CAUSES: `death-of-lysa-arryn` → `lord-nestor-and-the-knights-call-for-marillion-s-death`
- Quote: "'Bring him up, Lord Petyr. Let us write an end to this sorry business.' … 'The man must die,' Ser Marwyn Belmore declared … 'He should have followed Lady Lysa out the Moon Door.'"
- Cite: `sources/chapters/affc/affc-sansa-01.md:163-186`
- Tier: 1
- Rationale: The death directly occasions Nestor's ascent, the presentation of Marillion's coerced confession, and the demand for execution. Without the death there is no framing.

**`petyr-baelish` DECEIVES `nestor-royce` (via Marillion's false confession)**
- Quote: "We have come to an agreement, Marillion and I. Mord can be most persuasive. And if our singer disappoints us and sings a song we do not care to hear, why, you and I need only say he lies."
- Cite: `sources/chapters/affc/affc-sansa-01.md:33-34`
- Tier: 1

**`sansa-stark` PARTICIPATES_IN `lord-nestor-and-the-knights-call-for-marillion-s-death`**
- Quote: "'I saw … I was with the Lady Lysa when … when Marillion … pushed her.' And she told the tale again, hardly hearing the words as they spilled out of her."
- Cite: `sources/chapters/affc/affc-sansa-01.md:135`
- Tier: 1 — Sansa delivers the false testimony that seals Marillion's fate.

---

### 6. CAUSES: `lord-nestor-and-the-knights-call-for-marillion-s-death` → `littlefinger-bribes-nestor-royce-with-gates-of-the-moon`
- Quote: "I know Lord Nestor, sweetling … Our lies will profit him."
- Cite: `sources/chapters/affc/affc-sansa-01.md:37-38`
- Tier: 1 (the bribe is made in the same meeting, explicitly as a payment for Nestor's cooperation/silence)
- Rationale: The trial scene and the bribe are presented as a single political operation by LF. The bribe is the consolidation move that secures Nestor after the testimony.

**`petyr-baelish` MANIPULATES `nestor-royce` (via_hereditary_grant)**
- Quote: "You see the wonders that can be worked with lies and Arbor gold?"
- Cite: `sources/chapters/affc/affc-sansa-01.md:245`
- Tier: 1

---

### 7. CAUSES: `littlefinger-bribes-nestor-royce-with-gates-of-the-moon` → `trial-of-petyr-baelish-before-the-lords-declarant`
- Tier: 2 (structural: the bribe splits Nestor from the Lords Declarant coalition, but the trial happens at a distinct later point in affc-alayne-01)
- Rationale: Nestor's cooperation is a precondition for LF surviving the Lords Declarant confrontation — he sits on LF's side of the table during the trial. The bribe ENABLES the political outcome of the trial.

**ENABLES: `littlefinger-bribes-nestor-royce-with-gates-of-the-moon` → `trial-of-petyr-baelish-before-the-lords-declarant`**
- Quote: "By now they may have climbed as far as Stone … Lord Nestor is showing them up."
- Cite: `sources/chapters/affc/affc-alayne-01.md:59`
- Tier: 1 — Nestor actively escorts the Lords Declarant to the Eyrie, and sides with LF in the trial.

---

### 8. CAUSES: `trial-of-petyr-baelish-before-the-lords-declarant` → `harry-the-heir-betrothal-plan`
- Quote: "Petyr took her hand in his own … 'I have made a marriage contract for you … You are promised to Harrold Hardyng, sweetling.'"
- Cite: `sources/chapters/affc/affc-alayne-02.md:433-441`
- Tier: 1 (the betrothal is announced immediately after the trial + descent sequence, as LF's long-game answer to the Lords Declarant threat)
- Rationale: The trial establishes the political need for a Vale power-base; the betrothal is LF's strategic response.

**Role edges on `harry-the-heir-betrothal-plan`:**
- `petyr-baelish` AGENT_IN `harry-the-heir-betrothal-plan`
  - Quote: "I have made a marriage contract for you."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:433`
  - Tier: 1
- `sansa-stark` PROPOSED_AS_BRIDE in `harry-the-heir-betrothal-plan`
  - Quote: "You are promised to Harrold Hardyng, sweetling, provided you can win his boyish heart."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:441`
  - Tier: 1
- `harrold-hardyng` BETROTHED_TO `sansa-stark` (as Alayne Stone)
  - Quote: "You are promised to Harrold Hardyng, sweetling."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:441`
  - Tier: 1

---

### Supplementary spine edges

**`petyr-baelish` DECEIVES `lysa-arryn` (via Alayne cover story)**
- Quote: "My lady, allow me to present you Alayne Stone."
- Cite: `sources/chapters/asos/asos-sansa-06.md:215`
- Tier: 1

**`lysa-arryn` MARRIES_OFF `robert-arryn` (attempts betrothal to Sansa)**
- Quote: "How would you like to marry your cousin, the Lord Robert?"
- Cite: `sources/chapters/asos/asos-sansa-06.md:343`
- Tier: 1 — Lysa explicitly proposes this marriage.
- Note: This plan is superseded by LF's betrothal to Harry, making it an unrealised competing plan. Use PROPOSED_AS_BRIDE or NEEDS_VOCAB: `ATTEMPTED_BETROTHAL`.

**`murder-of-jon-arryn` CAUSES `lysa-arryn` [state: displaced, paranoid, isolated]**
- This arc presupposes prior events. The connection: Lysa's remark in asos-sansa-07 ("I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said") confirms the `murder-of-jon-arryn` → `lysa-accuses-tyrion-of-poisoning-jon-arryn` chain is already in the graph. Wire the downstream: `lysa-accuses-tyrion-of-poisoning-jon-arryn` CAUSES `wedding-of-petyr-baelish-and-lysa-arryn` (Lysa's paranoia + LF's manipulation isolate her from the realm and into LF's arms) — Tier 2 interpretive.

---

## SECONDARY-CHARACTER SUB-ARCS

### Marillion
- **Existing node:** `marillion`
- **Sub-arc:** Lysa's favourite singer → attempted assault on Sansa (asos-sansa-06) → sole witness to LF murdering Lysa → coerced false confession (Mord's torture) → sky-cell imprisonment → singing from sky cells → death (referenced as fact in affc-alayne-01)

**Edges:**
- `marillion` PARTICIPATES_IN `death-of-lysa-arryn` (as witness, then tool of the cover-up)
  - Quote: "Marillion gasped, 'You … you …'"
  - Cite: `sources/chapters/asos/asos-sansa-07.md:305`
  - Tier: 1

- `petyr-baelish` DECEIVES `marillion` (coerced confession)
  - Quote: "We have come to an agreement, Marillion and I. Mord can be most persuasive."
  - Cite: `sources/chapters/affc/affc-sansa-01.md:33`
  - Tier: 1

- `marillion` PARTICIPATES_IN `lord-nestor-and-the-knights-call-for-marillion-s-death`
  - Quote: "'Good lords, I beg your forgiveness … I loved her so, I could not bear to see her in another's arms … a madness seized me …'"
  - Cite: `sources/chapters/affc/affc-sansa-01.md:172-174`
  - Tier: 1 — Marillion delivers the false confession in person.

**Harvest note on Marillion's assault:** asos-sansa-06:263-286 — attempted rape of Sansa at the Fingers, stopped by Lothor Brune. NEEDS_VOCAB: no `ASSAULTS` edge type confirmed. Flag for `THREATENS` or `ATTEMPTED_ASSAULT`. This is also a sub-arc of the Lothor Brune sub-arc.

---

### Mya Stone
- **Existing node:** `mya-stone`
- **Sub-arc:** bastard daughter of Robert Baratheon (recognised by readers, but never acknowledged by him — Alayne notices "those are his eyes, and she has his hair too, the thick black hair he shared with Renly") → mule-warden of the descent route → guides Sansa/Robert down the mountain → emotional backstory (Mychel Redfort abandoned her) → Lothor Brune attracted to her

**Edges:**
- `mya-stone` PARTICIPATES_IN `descent-from-the-eyrie` (new minor event, or just an edge — see below)
  - Quote: "Mya Stone gave a crisp command, and two of Sky's men-at-arms swung the gates open."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:253`
  - Tier: 1 — Mya leads the descent.
  - Note: `descent-from-the-eyrie` might not warrant its own event node; it is a travel/transition beat. If it does not get a node, model Mya's role via GUARDS (she physically guards/guides the descent party).

**NEEDS_VOCAB: parent-identity revelation.** Sansa observes Mya has Robert Baratheon's eyes and hair. There is no `BIOLOGICAL_CHILD_OF` or `PARENTAGE_OBSERVED` edge type in the locked vocabulary. Flag: NEEDS_VOCAB: `UNACKNOWLEDGED_CHILD_OF` or note in Mya's node prose.
- Quote: "Those are his eyes, and she has his hair too, the thick black hair he shared with Renly."
- Cite: `sources/chapters/affc/affc-alayne-02.md:182`
- Tier: 1 (POV recognition)

---

### Mychel Redfort
- **Existing node:** `mychel-redfort`
- **Sub-arc:** was Lyn Corbray's squire → seduced Mya Stone → abandoned her to wed a daughter of Yohn Royce (arranged by Lord Horton Redfort)

**Edges:**
- `mychel-redfort` DECEIVES `mya-stone` (abandoned betrothal/relationship)
  - Quote: "Mychel was the best young swordsman in the Vale, and gallant … or so poor Mya thought, till he wed one of Bronze Yohn's daughters. Lord Horton gave him no choice in the matter, I am sure, but it was still a cruel thing to do to Mya."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:309`
  - Tier: 1 (reported via Myranda)

- NEEDS_VOCAB: `FORMER_SQUIRE_OF` or use existing `SERVES` in past tense context.
  - Mychel was Lyn Corbray's squire: "He used to be Lyn Corbray's squire."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:308`

---

### Lothor Brune
- **Existing node:** `lothor-brune`
- **Sub-arc:** LF's agent on the Merling King → stops Marillion's assault on Sansa (asos-sansa-06) → becomes Eyrie captain of guards (replaces Ser Marwyn Belmore) → leads Sansa/Robert's descent → interested in Mya Stone

**Edges:**
- `lothor-brune` AGENT_IN `littlefinger-smuggles-sansa-out-of-kings-landing`
  - Quote: "Ser Lothor Brune stood beside him with a torch."
  - Cite: `sources/chapters/asos/asos-sansa-05.md:117`
  - Tier: 1

- `lothor-brune` GUARDS `sansa-stark`
  - Quote: "Lord Petyr said watch out for you."
  - Cite: `sources/chapters/asos/asos-sansa-06.md:287`
  - Tier: 1

- `petyr-baelish` MANIPULATES `lothor-brune` (via loyalty/service)
  - Tier: 2 — implied by LF explaining "Brune is close-mouthed by nature" and his service; the text says Oswell (Kettleblack) watches Brune for LF, and Brune watches Kettleblack. This is a mutual-surveillance arrangement, not straightforward manipulation. Flag for NEEDS_VOCAB: `SURVEILS` or note in node prose.

---

### Lyn Corbray
- **Existing node:** `lyn-corbray`
- **Sub-arc:** Lords Declarant member → draws Lady Forlorn at the trial (nearly triggers violence) → revealed by LF to be a secret LF agent paid in "gold and boys and promises" — the performance of hostility is manufactured

**Edges:**
- `lyn-corbray` PARTICIPATES_IN `trial-of-petyr-baelish-before-the-lords-declarant`
  - Quote: "Littlefinger will talk you out of your smallclothes if you listen long enough. The only way to settle his sort is with steel." He drew his longsword."
  - Cite: `sources/chapters/affc/affc-alayne-01.md:273`
  - Tier: 1

- `petyr-baelish` MANIPULATES `lyn-corbray` (via_gold_and_boys_and_promises)
  - Quote: "Ser Lyn will remain my implacable enemy … And how shall you reward him for this service? With gold and boys and promises, of course."
  - Cite: `sources/chapters/affc/affc-alayne-01.md:339-343`
  - Tier: 1 — explicitly confirmed by LF to Sansa

---

### Myranda Royce
- **Existing node:** `myranda-royce`
- **Sub-arc:** Nestor's daughter, keeps the Gates of the Moon → meets Sansa/Alayne on the mountain descent → probes Sansa for information → potential ally or informant — LF warned Sansa about her

**Edges:**
- `myranda-royce` PARTICIPATES_IN (descent from the Eyrie)
  - Quote: "Lady Myranda Royce … knelt in a patch of snow to kiss his hand and cheeks."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:222-224`
  - Tier: 1 — Myranda physically joins the descent party.

- NEEDS_VOCAB: `BEFRIENDS` or `OBSERVES` — Myranda's probing conversation with Sansa is a form of low-level intelligence gathering that has no clean edge type. Note in prose.

- `myranda-royce` PARTICIPATES_IN `harry-the-heir-betrothal-plan` (indirectly — she was previously considered as a bride for Harry)
  - Quote: "My lord father had hoped to marry me to Harry, but Lady Waynwood would not hear of it."
  - Cite: `sources/chapters/affc/affc-alayne-02.md:289`
  - Tier: 1 — her failed candidacy provides context for the LF betrothal.

---

### The Lords Declarant
- **Existing node:** `lords-declarant` (faction)
- **Individual members present at trial:** `yohn-royce`, `nestor-royce`, `lyn-corbray` (confirmed above); plus Benedar Belmore, Symond Templeton, Horton Redfort, Anya Waynwood, Gilwood Hunter. Check for individual nodes for Belmore/Templeton/Redfort/Waynwood/Hunter — they are named but likely only partial nodes.
- **Sub-arc:** coalition forms after Lysa's death → besieges Gates of the Moon → sends ultimatum → rides to Eyrie trial → Nestor defects → LF negotiates one-year truce → coalition fractures (Waynwood at Lyonel Corbray's wedding, per affc-alayne-02)

**Edges:**
- `lords-declarant` PARTICIPATES_IN `trial-of-petyr-baelish-before-the-lords-declarant`
  - Quote: "Alayne knew their names as well as her own. Benedar Belmore … Symond Templeton … Horton Redfort … Anya Waynwood … Gilwood Hunter … And Yohn Royce, mightiest of them all."
  - Cite: `sources/chapters/affc/affc-alayne-01.md:21`
  - Tier: 1

- `lords-declarant` CAUSES `trial-of-petyr-baelish-before-the-lords-declarant`
  - Quote: "The six had gathered at Runestone after Lysa Arryn's fall, and there made a pact together, vowing to defend Lord Robert, the Vale, and one another."
  - Cite: `sources/chapters/affc/affc-alayne-01.md:21`
  - Tier: 1

---

### Sweetrobin (Robert Arryn)
- **Existing node:** `robert-arryn`
- **Sub-arc:** orphaned by Lysa's death → traumatised, has worsening shaking fits → kept sedated with sweetsleep (suggested by LF, reluctantly given by Maester Colemon) → coddled/managed by Sansa/Alayne → descended from Eyrie → introduced to Harry as future companion

**Edges:**
- `robert-arryn` WARD_OF `petyr-baelish`
  - Quote: "Until your sixteenth name day, I rule the Eyrie."
  - Cite: `sources/chapters/affc/affc-alayne-01.md:71`
  - Tier: 1

- NEEDS_VOCAB: `ENDANGERED_BY` — LF's sweetsleep scheme is a slow poisoning of Robert, though not framed as murder in these chapters. The maester's warning ("it does not leave the flesh, and in time …") makes the threat implicit. Cannot use KILLS (not dead yet) or VICTIM_IN (no event node). Note in Robert's node under "Known threats."

- `colemon` PARTICIPATES_IN (sweetsleep administration)
  - Quote: "Sweetsleep … one small pinch … perhaps, perhaps. Not too much, and not too often, yes, I might try …"
  - Cite: `sources/chapters/affc/affc-alayne-01.md:89`
  - Tier: 1 — Colemon acquiesces against his medical judgment.

---

### Nestor Royce
- **Existing node:** `nestor-royce`
- **Sub-arc:** Keeper of the Gates → receives forged hereditary grant → sides with LF against Lords Declarant → escorts Lords Declarant to trial but votes with LF

**Edges:**
- `nestor-royce` PARTICIPATES_IN `trial-of-petyr-baelish-before-the-lords-declarant`
  - Quote: "Nestor Royce had been silent all this while, but now he spoke up loudly. 'I once hoped to wed Lady Lysa myself … It happens that she chose Lord Littlefinger, and entrusted her son to his care.'"
  - Cite: `sources/chapters/affc/affc-alayne-01.md:253`
  - Tier: 1

- `petyr-baelish` MANIPULATES `nestor-royce` (via_hereditary_grant) — see spine edge #6 above.

- `gates-of-the-moon` RULES `nestor-royce` edge already exists in graph (confirmed by query). The bribe event explains the genesis of that RULES edge and should be cited back to `littlefinger-bribes-nestor-royce-with-gates-of-the-moon`.

---

## DEDUP NOTES

1. **`alayne-baelish` ≠ Sansa.** Query confirmed: `alayne-baelish` is Petyr Baelish's MOTHER (Alayne of Braavos). The "Alayne Stone" alias correctly lives on `sansa-stark` as a frontmatter alias. The `sansa-adopts-alayne-stone-identity` event node proposed above explains the genesis of that alias and should cite back to `sansa-stark` — do NOT create a second `alayne-stone` character node.

2. **`alayne-royce` ≠ Sansa.** There is a real historical `alayne-royce` (or similar) in the Vale. Never conflate with Sansa's alias. This arc does not require that node.

3. **`the-fingers` does NOT exist as a location node.** Graph query returned no match (closest match was `high-king-of-the-vale-the-fingers-and-the-mountains-of-the-moon` — a title node, not a place). However, `fingers` DOES exist as a node (`place.location`). The query for `the-fingers` failed; `fingers` succeeded. Use slug `fingers` for Littlefinger's ancestral seat. Confirm with: `python3 scripts/graph-query.py fingers`.

4. **`gates-of-the-moon` EXISTS.** Node confirmed; type `place.location`; has RULES edge to `nestor-royce`. Use this slug.

5. **`robert-arryn` is the correct slug for Sweetrobin.** The instruction note is confirmed — NOT `robin-arryn`.

6. **`petyr-baelish` is the only node for Littlefinger.** No separate `littlefinger` node. All LF edges use `petyr-baelish`.

7. **`lords-declarant` node exists as a faction node with zero outbound edges.** The trial event will be its first meaningful edge wiring.

8. **`colemon` is the correct slug for Maester Colemon.** `maester-colemon` returns no result; `colemon` resolves correctly.

9. **`dontos-hollard` — verify existence before writing KILLS edge.** The execution in asos-sansa-05 is POV-confirmed. If the node exists, wire `petyr-baelish` KILLS `dontos-hollard`. If absent, propose as a new node (event.death: `death-of-dontos-hollard`).

10. **`alayne-i-the-winds-of-winter` — do NOT wire.** This is a TWOW (unpublished) node. The betrothal plan proposed here (`harry-the-heir-betrothal-plan`) is the canon AFFC endpoint; the Winds chapter would be downstream. Confirmed not to wire per task instructions.

11. **`olenna-tyrell` exists.** The confession in asos-sansa-07 — Lysa's rant reveals that LF orchestrated Jon Arryn's murder and told her to blame the Lannisters — directly implicates Olenna Tyrell as the Joffrey poisoner (confirmed by LF on the ship in asos-sansa-06: "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you"). The spine of the Purple Wedding is upstream of this arc (not this arc's job) but these chapters contain crucial confirmation text. See HARVEST.

---

## HARVEST

Pointers only — chapter:line / kind / note

### asos-sansa-05.md
- 11:13 / quote / "Joffrey is dead," she told the trees — iconic opening; grief vs. relief
- 21-23 / object / The silver hair net with black amethysts from Asshai — poison delivery device; Sansa describes the missing stone. Key artifact evidence.
- 43 / quote / "There was murder in them!" — Sansa confronts Dontos about the poison; load-bearing accusation
- 53 / witness / Sansa's realisation that Tyrion's arrest will implicate her: "They will think I was part of it as well" — mental state evidence
- 91-93 / quote / Sansa's descent of the cliff: "Be brave, she told herself. Be brave, like a lady in a song." — voice/character development
- 127 / object / Dontos's House Hollard surcoat (three gold crowns on black chief) — worn to his death; identity marker
- 135 / quote / "All he did he did at my behest … I dared not befriend you openly … I knew he would be the perfect catspaw." — LF's manipulation thesis statement
- 143 / quote / "Come to the godswood tonight if you want to go home." — ironic foreshadowing of "home" as a lie
- 167 / quote / "Always keep your foes confused … Sometimes the best way to baffle them is to make moves that have no purpose, or even seem to work against you." — LF's strategic doctrine; key character voice
- 171 / quote / "In a better world, you might have been mine … My loyal loving daughter …" — LF's Catelyn obsession made explicit to Sansa; load-bearing psychology

### asos-sansa-06.md
- 83-84 / food / Sansa arrives at the Fingers: Petyr offers wine; "an Arbor vintage … It tasted of oak and fruit and hot summer nights." Sansa trying to keep it down after seasickness.
- 89 / food / "Grisel … bring some food up … some fruit … oranges and pomegranates"
- 133-135 / food / Pomegranates — LF loosening seeds with his dagger, bringing them to his mouth; charged with intimacy; eating the blood orange, juice on his mouth. Extended food-as-seduction sequence.
- 197 / food / Quail, venison, and roast boar at the wedding feast; mead; singer plays "Seasons of My Love"
- 245-251 / food / Wedding feast in detail — trestle tables, torches at dusk, the bedding ceremony. Mead and marriage: "mead and marriage had taken years off Lady Lysa."
- 257-259 / witness / Marillion introduces himself to Sansa as "Marillion" at the post-wedding feast — first in-person encounter; she is alert but tired.
- 287 / quote / "Lord Petyr said watch out for you" — Lothor's understated heroism; minimal-dialogue character voice.
- 311 / quote / Lysa's monologue about Jon Arryn: "his seed was old and weak. All my babies died but Robert, three girls and two boys." — fertility/tragedy; also sets up the fragility of the Arryn succession.
- 335 / quote / "A man will tell you poison is dishonorable, but a woman's honor is different." — Lysa's rationalisation of Joffrey's murder; also hints at her own poison use against Jon Arryn.
- 347 / quote / Lysa's marriage plan for Robert + Sansa: "The ravens should bring us the word from King's Landing once the Imp's head rolls. You and Robert can be wed the next day" — dark comedy of the plan.

### asos-sansa-07.md
- 22-44 / description / The snow castle of Winterfell — detailed construction of Sansa's replica; "the snow fell and the castle rose." Extended memory/homesickness passage; godswood without a heart tree.
- 97 / quote / LF kisses Sansa in the snow: "He tasted of mint." — sensory detail; the kiss triggers Lysa's confrontation
- 167-171 / quote / LF describes Olenna Tyrell: "A fearsome old harridan, and not near as frail as she pretends … I praised him to the skies, to be sure … whilst my men spread disturbing tales amongst Lord Tyrell's servants." — load-bearing quote on Purple Wedding conspiracy; LF's role in setting it up.
- 184-193 / quote / LF explains how Olenna removed the poison stone: "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you." — definitively names Olenna as the poisoner (POV-confirmed via Sansa's reaction: "She raised a hand to her mouth")
- 213 / quote / Lysa confesses: "That was the night I stole up to his bed … He told me he loved me then, but he called me Cat" — key backstory for LF's psychology
- 275-276 / quote / Lysa's moon-tea confession: "They murdered him with moon tea, with tansy and mint and wormwood, a spoon of honey and a drop of pennyroyal. It wasn't me, I never knew, I only drank what Father gave me" — confirms Hoster Tully forced Lysa to abort LF's baby. Load-bearing cross-arc evidence (Hoster's node; also implicates the old Maester of Riverrun).
- 283 / quote / Lysa to LF: "I saw you kissing in the snow. She's just like her mother. Catelyn kissed you in the godswood, but she never meant it … Why did you love her best? It was me, it was always meeee!" — Lysa's emotional collapse; excellent character voice
- 287 / quote / "You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said." — THE confession: Lysa poisoned Jon Arryn on LF's orders. Load-bearing quote for `murder-of-jon-arryn` arc. Cite: asos-sansa-07.md:287
- 295 / quote / "My sweet silly jealous wife … I've only loved one woman, I promise you." / "Lysa Arryn smiled tremulously. 'Only one? Oh, Petyr, do you swear it? Only one?' 'Only Cat.'" — "Only Cat" — the last words before the murder. Iconic; canonical evidence quote for `death-of-lysa-arryn`.

### affc-sansa-01.md
- 17-18 / description / Marillion in his sky cell: "If the Eyrie had been made like other castles, only rats and gaolers would have heard the dead man singing." — framing; the sky cells as prison.
- 25 / quote / "I'd sooner suffer his singing than listen to his sobbing." — LF's chilling pragmatism about Marillion's captivity
- 55-56 / food / Arbor gold wine — LF and Nestor drink a full flagon; LF serves it as part of the bribery sequence. "Lies and Arbor gold."
- 115-117 / quote / Sansa's internal monologue on Petyr/Littlefinger duality: "He was Petyr, her protector, warm and funny and gentle … but he was also Littlefinger … And Littlefinger was no friend of hers. When Joff had her beaten, the Imp defended her, not Littlefinger." — strong character-voice internal assessment; worth quoting in Sansa's node.
- 155 / description / Marillion's hands: white silk gloves covering tortured fingers; "Fat Maddy claimed that Mord had taken off three of his fingers." — physical evidence of Mord's torture methods.

### affc-alayne-01.md
- 29-31 / food / Robert demands soft-boiled eggs and back bacon but there are none; only porridge and honey due to Lords Declarant siege cutting off food supply. Sweetrobin refuses porridge.
- 36-37 / food / Sweetrobin wants more sweetmilk (sweetsleep in milk); refused by Maester Colemon as "too soon." Colemon's warning: "it does not leave the flesh."
- 53 / quote / LF to Alayne: "I despise porridge. I'd sooner break my fast with a kiss." — character voice; food as pretext for intimacy.
- 87-89 / food / Sweetsleep administered: "A pinch of sweetsleep in his milk … Just a pinch, to calm him and stop his wretched shaking." LF overriding maester's judgment.
- 101 / food / Mulled red wine with honey and raisins; sharp white cheese; bread baked for twenty. Sansa organising hospitality for the Lords Declarant.
- 337-343 / quote / LF reveals Lyn Corbray is his paid agent: "Ser Lyn will remain my implacable enemy … With gold and boys and promises, of course. Ser Lyn is a man of simple tastes, my sweetling. All he likes is gold and boys and killing." — load-bearing; confirms LF's double game with Corbray.

### affc-alayne-02.md
- 33-34 / food / Robert wants berries and cream or warm bread and butter; no kitchens lit; Alayne promises lemon cakes at the Gates of the Moon.
- 65 / food / Robert complains "Maester Colemon put something vile in my milk last night, I could taste it." — sweetsleep administered without Robert's consent.
- 83-87 / food / Sweetrobin offers Alayne "sweetmilk" (sweetsleep) and honeycombs as inducement to stay in bed; Robert's relationship with sweetsleep framed as a comfort addiction.
- 89 / food / Promise of lemon cakes at the Gates of the Moon — Alayne uses lemon cakes as behaviour management for Robert. "A hundred? Could I have a hundred?"
- 182 / witness / Mya Stone's parentage — Sansa identifies her as Robert Baratheon's daughter by eye colour and black hair ("he shared [it] with Renly"). Unremarked by other characters. Harvest as parentage-witness note.
- 265-266 / food / At Snow waycastle: "a hot meal of stewed goat and onions. She ate with Mya and Myranda." — meal during the harrowing descent.
- 288-296 / description / Myranda Royce's physical description: "short, fleshy woman … soft-bodied and sweet-smelling, broad of hip, thick of waist, and extremely buxom. Her thick chestnut curls framed round red cheeks." Also: "I had one [husband] once, but I killed him … He died on top of me."
- 305 / quote / Myranda on Marillion: "I bedded that pretty boy Marillion. I did not know he was a monster. He sang beautifully, and could do the sweetest things with his fingers." — Myranda as additional Marillion victim/witness; also evidence of Marillion's sexual behaviour pattern.
- 355 / quote / On the high stone saddle: "It sounds like a wolf, thought Sansa. A ghost wolf, big as mountains." — foreshadowing / Direwolf motif; Sansa's identity bleeding through Alayne.
- 365-367 / quote / Mya Stone's memory of being thrown in the air: "He stands as tall as the sky, and he throws me up so high it feels as though I'm flying … Then one day he wasn't. Men come and go. They lie, or die, or leave you. A mountain is not a man, though, and a stone is a mountain's daughter. I trust my father, and I trust my mules." — load-bearing quote on Mya's psychology and Robert Baratheon's role as her unknown father.
- 433-467 / quote / LF's full betrothal reveal + Arryn succession genealogy: "Harry, the Eyrie, and Winterfell. That's worth another kiss now, don't you think?" — the plan's full exposition. Multiple citable quotes; most important: "when they come together for his wedding, and you come out with your long auburn hair, clad in a maiden's cloak of white and grey with a direwolf emblazoned on the back … every knight in the Vale will pledge his sword to win you back your birthright." This is Sansa's arc endpoint (in published canon). Cite: affc-alayne-02.md:467.
